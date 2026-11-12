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

# The scenario driver for bench/tasks/quota-requires-limits-no-limitrange.
#
# It plants a namespace with a ResourceQuota on cpu and memory requests and
# limits, and a one-replica Deployment whose container sets no resources
# block. The quota admission plugin refuses every pod the ReplicaSet creates
# ("must specify limits.cpu, ..."), so the Deployment shows 0 of 1 with a
# ReplicaFailure condition and no pod exists. The fix is a LimitRange with
# container defaults, which the LimitRanger plugin applies before the quota
# is checked, not an edit to every manifest.
#
# The shape holds on a Standard host: Autopilot admission writes requests
# onto every container before the quota plugin runs.

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
    apiVersion: v1
    kind: ResourceQuota
    metadata:
      name: "${var.quota_name}"
      labels:
        managed-by: kube-agents-bench
    spec:
      hard:
        requests.cpu: "2"
        requests.memory: 4Gi
        limits.cpu: "4"
        limits.memory: 8Gi
    ---
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
          securityContext:
            runAsNonRoot: true
            runAsUser: 65534
            seccompProfile:
              type: RuntimeDefault
          containers:
            - name: "${var.container_name}"
              image: busybox:1.36
              command: ["sh", "-c", "sleep infinity"]
  MANIFEST
}

module "plant" {
  source = "../../modules/namespaced-plant"

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.namespace
  stack                 = "quota-requires-limits-no-limitrange"
  labels                = local.ci_labels
  manifest              = local.manifest
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
