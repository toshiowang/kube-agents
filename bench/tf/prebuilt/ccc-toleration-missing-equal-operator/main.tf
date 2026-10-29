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

# The scenario driver for bench/tasks/ccc-toleration-missing-equal-operator.
#
# It plants a ComputeClass and a two-replica Deployment that targets the class
# through the nodeSelector and tolerates the class taint with a toleration that
# names the value but omits `operator: Equal`, the hand-written shape the
# scenario describes. No node carries the class, so the pods stay Pending. The
# stockout-prevention audit is expected to miss the pattern today.
#
# Isolation class: namespace-scoped. Teardown removes what this stack created and
# deletes the namespace only when this stack created it.

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
  ns     = var.namespace
  target = var.target_resource_name
  ci_labels = {
    "managed-by"  = "kube-agents-bench"
    "build-id"    = var.prow_build_id != "" ? var.prow_build_id : "local"
    "pull-number" = var.prow_pull_number != "" ? var.prow_pull_number : "none"
  }
}

resource "null_resource" "scenario" {
  triggers = {
    namespace     = local.ns
    target        = local.target
    host_cluster  = var.host_cluster_name
    host_location = var.host_cluster_location
    host_project  = var.project_id
    manifest      = sha256(join("|", [local.ns, local.target, var.host_cluster_name]))
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
          created-by-stack=ccc-toleration-missing-equal-operator
      fi
      kubectl apply -f - <<'MANIFEST'
      apiVersion: cloud.google.com/v1
      kind: ComputeClass
      metadata:
        name: general-ccc
        labels:
          managed-by: kube-agents-bench
      spec:
        priorities:
          - nodepools: ["general-ccc-pool"]
        nodePoolAutoCreation:
          enabled: false
        whenUnsatisfiable: DoNotScaleUp
      ---
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: batch-worker-a
        namespace: ${local.ns}
        labels:
          app: batch-worker-a
          managed-by: kube-agents-bench
      spec:
        replicas: 2
        selector:
          matchLabels:
            app: batch-worker-a
        template:
          metadata:
            labels:
              app: batch-worker-a
          spec:
            automountServiceAccountToken: false
            nodeSelector:
              cloud.google.com/compute-class: general-ccc
            tolerations:
              - key: cloud.google.com/compute-class
                value: general-ccc
                effect: NoSchedule
            containers:
              - name: worker
                image: registry.k8s.io/pause:3.10
                resources:
                  requests:
                    cpu: 10m
                    memory: 16Mi
                  limits:
                    memory: 32Mi
      MANIFEST
      echo "Planted scenario ccc-toleration-missing-equal-operator on ${var.host_cluster_name}."
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
      kubectl -n "${self.triggers.namespace}" delete deployment "${self.triggers.target}" --ignore-not-found --wait=false
      kubectl delete computeclass general-ccc --ignore-not-found --wait=false
      if [ "$(kubectl get namespace "${self.triggers.namespace}" -o jsonpath='{.metadata.labels.created-by-stack}' 2>/dev/null)" = "ccc-toleration-missing-equal-operator" ]; then
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
