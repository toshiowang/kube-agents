#!/bin/bash
# Copyright 2026 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Step two of the storage-immediate-binding-zonal-pd-affinity-conflict stack:
# wait for the planted claim to bind, read the zone its volume landed in, and
# create the Deployment pinned to another zone of the same cluster. Runs
# after the namespaced-plant module created the namespace and the claim, and
# plants only inside that namespace, so the module's destroy removes
# everything this script made.
set -euo pipefail

readonly PIN_BIND_TIMEOUT_SECONDS=180
readonly PIN_BIND_POLL_SECONDS=5
readonly PIN_ZONE_LABEL="topology.kubernetes.io/zone"
readonly PIN_IMAGE="busybox:1.36"

pin_require() { # <name>: the variable must be set and non-empty
  if [ -z "${!1:-}" ]; then
    echo "ERROR: $1 is not set; the stack's provisioner passes it." >&2
    exit 1
  fi
}

pin_require PIN_HOST_CLUSTER; pin_require PIN_HOST_LOCATION; pin_require PIN_NAMESPACE
pin_require PIN_CLAIM; pin_require PIN_WORKLOAD; pin_require PIN_CONTAINER; pin_require PIN_MOUNT_PATH

kubeconfig_dir="$(mktemp -d)"
trap 'rm -rf "$kubeconfig_dir"' EXIT
KUBECONFIG="$kubeconfig_dir/config"
export KUBECONFIG

project="${PIN_PROJECT:-}"
if [ -z "$project" ]; then
  project="$(gcloud config get-value project 2>/dev/null || true)"
fi
if [ -z "$project" ]; then
  echo "ERROR: no project id. Pass project_id or set a gcloud default project." >&2
  exit 1
fi
gcloud container clusters get-credentials "$PIN_HOST_CLUSTER" \
  --location "$PIN_HOST_LOCATION" --project "$project" --quiet

# 1. The claim binds on its own under Immediate binding; wait for the volume.
volume=""
deadline=$((SECONDS + PIN_BIND_TIMEOUT_SECONDS))
while [ "$SECONDS" -lt "$deadline" ]; do
  volume="$(kubectl --namespace "$PIN_NAMESPACE" get persistentvolumeclaim "$PIN_CLAIM" -o jsonpath='{.spec.volumeName}')"
  phase="$(kubectl --namespace "$PIN_NAMESPACE" get persistentvolumeclaim "$PIN_CLAIM" -o jsonpath='{.status.phase}')"
  if [ "$phase" = "Bound" ] && [ -n "$volume" ]; then
    break
  fi
  sleep "$PIN_BIND_POLL_SECONDS"
done
if [ -z "$volume" ]; then
  echo "ERROR: $PIN_CLAIM in $PIN_NAMESPACE did not bind within ${PIN_BIND_TIMEOUT_SECONDS}s; the built-in class may not bind Immediate on this cluster." >&2
  kubectl --namespace "$PIN_NAMESPACE" describe persistentvolumeclaim "$PIN_CLAIM" >&2 || true
  exit 1
fi

# 2. The zone the volume landed in, from the first zone-keyed node affinity
# term (`topology.gke.io/zone` on a migrated or CSI volume, the legacy keys
# on an older one).
volume_zone="$(kubectl get persistentvolume "$volume" \
  -o jsonpath='{range .spec.nodeAffinity.required.nodeSelectorTerms[*].matchExpressions[*]}{.key}={.values[0]}{"\n"}{end}' \
  | grep '/zone=' | head -n 1 | cut -d= -f2 || true)"
if [ -z "$volume_zone" ]; then
  echo "ERROR: volume $volume carries no zone in its node affinity; the scenario needs a zonal volume." >&2
  exit 1
fi

# 3. Another zone of the same cluster, from the cluster's own location list.
other_zone=""
for zone in $(gcloud container clusters describe "$PIN_HOST_CLUSTER" \
  --location "$PIN_HOST_LOCATION" --project "$project" --format='value(locations)' | tr ';' ' '); do
  if [ "$zone" != "$volume_zone" ]; then
    other_zone="$zone"
    break
  fi
done
if [ -z "$other_zone" ]; then
  echo "ERROR: $PIN_HOST_CLUSTER has no zone other than $volume_zone; the scenario needs a cluster spanning two zones." >&2
  exit 1
fi
echo "Volume $volume is in $volume_zone; pinning $PIN_WORKLOAD to $other_zone."

# 4. The workload, pinned where its volume is not.
kubectl --namespace "$PIN_NAMESPACE" create -f - <<MANIFEST
apiVersion: apps/v1
kind: Deployment
metadata:
  name: "$PIN_WORKLOAD"
  labels:
    app: "$PIN_WORKLOAD"
    managed-by: kube-agents-bench
spec:
  replicas: 1
  selector:
    matchLabels:
      app: "$PIN_WORKLOAD"
  template:
    metadata:
      labels:
        app: "$PIN_WORKLOAD"
    spec:
      automountServiceAccountToken: false
      nodeSelector:
        $PIN_ZONE_LABEL: "$other_zone"
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: "$PIN_CONTAINER"
          image: $PIN_IMAGE
          command: ["sh", "-c", "sleep infinity"]
          volumeMounts:
            - name: scratch
              mountPath: "$PIN_MOUNT_PATH"
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 50m
              memory: 64Mi
      volumes:
        - name: scratch
          persistentVolumeClaim:
            claimName: "$PIN_CLAIM"
MANIFEST
echo "Planted $PIN_WORKLOAD in $PIN_NAMESPACE on $PIN_HOST_CLUSTER, pinned to $other_zone with its volume in $volume_zone."
