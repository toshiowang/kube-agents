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

# The scenario driver for bench/tasks/security-pss-restricted-refuses-unset-securitycontext.
#
# It plants a namespace labelled for Pod Security admission at `restricted`
# and a one-replica Deployment whose pod template sets no securityContext.
# The admission plugin refuses every pod the ReplicaSet creates, so the
# Deployment shows 0 of 1 with a ReplicaFailure condition and the ReplicaSet's
# FailedCreate events name the four fields the pod lacks. No pod ever exists:
# the evidence is in the events and the Deployment status, not in a pod.
#
# The label is written on the namespace at create (the module's extra_labels)
# because a label added after a pod was admitted would leave that pod running
# and the symptom unplanted.

terraform {
  required_version = ">= 1.5.0"
}

locals {
  ci_labels = {
    "managed-by"  = "kube-agents-bench"
    "build-id"    = var.prow_build_id != "" ? var.prow_build_id : "local"
    "pull-number" = var.prow_pull_number != "" ? var.prow_pull_number : "none"
  }

  manifest = <<-MANIFEST
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: "${var.workload_name}"
      labels:
        app: "${var.workload_name}"
        managed-by: kube-agents-bench
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: "${var.workload_name}"
      template:
        metadata:
          labels:
            app: "${var.workload_name}"
        spec:
          automountServiceAccountToken: false
          containers:
            - name: "${var.container_name}"
              image: busybox:1.36
              command: ["sh", "-c", "sleep infinity"]
              resources:
                requests:
                  cpu: 50m
                  memory: 64Mi
                limits:
                  cpu: 50m
                  memory: 64Mi
  MANIFEST
}

module "plant" {
  source = "../../modules/namespaced-plant"

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.namespace
  stack                 = "security-pss-restricted-refuses-unset-securitycontext"
  labels                = local.ci_labels
  extra_labels = {
    "pod-security.kubernetes.io/enforce" = var.enforce_level
  }
  manifest = local.manifest
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
