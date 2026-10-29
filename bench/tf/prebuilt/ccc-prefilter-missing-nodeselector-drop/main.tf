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

# The scenario driver for bench/tasks/ccc-prefilter-missing-nodeselector-drop.
#
# It plants, on the host cluster, a ComputeClass with one node-pool priority
# and no auto-creation, and a three-replica Deployment that omits the
# `cloud.google.com/compute-class` nodeSelector. The Deployment asks for more
# CPU than any existing node can give, so its pods stay Pending the way the
# scenario's pods do while the autoscaler never simulates the ComputeClass
# pool for them. The stockout-prevention audit is expected to miss the
# pattern today (the case carries expected_fail: true); the planted state is
# what a fix would have to detect.
#
# WHY THE HOST CLUSTER. Every eval runner deploys the host; the seeded fleet
# clusters are shared fixtures no case may reshape. The host carries the
# ComputeClass API on every supported GKE version.
#
# WHY REQUESTS, NOT A MISSING POOL. The real symptom is pods that no standard
# pool can take and a ComputeClass pool the autoscaler will not consider. A
# CPU request above the node size gives the first half without a node pool
# change; the ComputeClass gives the second.
#
# Isolation class: namespace-scoped. Teardown deletes the namespace only when
# this stack created it.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = ">= 3.0.0"
    }
  }
}

locals {
  ns       = var.namespace
  workload = var.target_resource_name
  ccc      = var.compute_class_name
  ccc_pool = var.compute_class_pool
  ci_labels = {
    "managed-by"  = "kube-agents-bench"
    "build-id"    = var.prow_build_id != "" ? var.prow_build_id : "local"
    "pull-number" = var.prow_pull_number != "" ? var.prow_pull_number : "none"
  }
}

resource "null_resource" "untargeted_workload" {
  triggers = {
    namespace     = local.ns
    workload      = local.workload
    compute_class = local.ccc
    host_cluster  = var.host_cluster_name
    host_location = var.host_cluster_location
    host_project  = var.project_id
    manifest      = sha256(join("|", [local.ns, local.workload, local.ccc, local.ccc_pool, var.host_cluster_name]))
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = <<-EOT
      set -euo pipefail
      kubeconfig_dir="$(mktemp -d)"
      trap 'rm -rf "$kubeconfig_dir"' EXIT
      KUBECONFIG="$kubeconfig_dir/config"
      export KUBECONFIG
      project="${var.project_id}"
      if [ -z "$project" ]; then
        project="$(gcloud config get-value project 2>/dev/null || true)"
      fi
      if [ -z "$project" ]; then
        echo "ERROR: no project id. Pass -var project_id=... or set a gcloud default project." >&2
        exit 1
      fi
      gcloud container clusters get-credentials "${var.host_cluster_name}" \
        --location "${var.host_cluster_location}" --project "$project" --quiet
      if ! kubectl get namespace "${local.ns}" >/dev/null 2>&1; then
        kubectl create namespace "${local.ns}"
        kubectl label namespace "${local.ns}" --overwrite \
          managed-by="${local.ci_labels["managed-by"]}" \
          build-id="${local.ci_labels["build-id"]}" \
          pull-number="${local.ci_labels["pull-number"]}" \
          created-by-stack=ccc-prefilter-missing-nodeselector-drop
      fi
      kubectl apply -f - <<'MANIFEST'
      apiVersion: cloud.google.com/v1
      kind: ComputeClass
      metadata:
        name: ${local.ccc}
        labels:
          managed-by: kube-agents-bench
      spec:
        priorities:
          - nodepools: ["${local.ccc_pool}"]
        nodePoolAutoCreation:
          enabled: false
        whenUnsatisfiable: DoNotScaleUp
      ---
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: ${local.workload}
        namespace: ${local.ns}
        labels:
          app: ${local.workload}
          managed-by: kube-agents-bench
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: ${local.workload}
        template:
          metadata:
            labels:
              app: ${local.workload}
          spec:
            automountServiceAccountToken: false
            containers:
              - name: worker
                image: registry.k8s.io/pause:3.10
                resources:
                  requests:
                    cpu: "8"
                    memory: 64Mi
                  limits:
                    memory: 64Mi
      MANIFEST
      echo "Planted ${local.workload} (3 replicas, no compute-class nodeSelector) in ${local.ns} and ComputeClass ${local.ccc} on ${var.host_cluster_name}."
    EOT
  }

  provisioner "local-exec" {
    when        = destroy
    on_failure  = continue
    interpreter = ["/bin/bash", "-c"]
    command     = <<-EOT
      set -euo pipefail
      kubeconfig_dir="$(mktemp -d)"
      trap 'rm -rf "$kubeconfig_dir"' EXIT
      KUBECONFIG="$kubeconfig_dir/config"
      export KUBECONFIG
      project="${self.triggers.host_project}"
      if [ -z "$project" ]; then
        project="$(gcloud config get-value project 2>/dev/null || true)"
      fi
      gcloud container clusters get-credentials "${self.triggers.host_cluster}" \
        --location "${self.triggers.host_location}" --project "$project" --quiet
      kubectl -n "${self.triggers.namespace}" delete deployment "${self.triggers.workload}" --ignore-not-found --wait=false
      kubectl delete computeclass "${self.triggers.compute_class}" --ignore-not-found --wait=false
      if [ "$(kubectl get namespace "${self.triggers.namespace}" -o jsonpath='{.metadata.labels.created-by-stack}' 2>/dev/null)" = "ccc-prefilter-missing-nodeselector-drop" ]; then
        kubectl delete namespace "${self.triggers.namespace}" --ignore-not-found --wait=false
      fi
    EOT
  }
}

output "cluster_name" {
  value = var.host_cluster_name
}

output "cluster_location" {
  value = var.host_cluster_location
}
