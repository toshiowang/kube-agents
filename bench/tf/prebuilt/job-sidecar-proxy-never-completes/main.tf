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

# The scenario driver for bench/tasks/job-sidecar-proxy-never-completes.
#
# It plants a Job whose pod runs two regular containers: a worker that logs
# its export and exits 0 after a short sleep, and a proxy that runs forever.
# A Job's pod completes only when every regular container exits, so the pod
# stays Running with the worker Completed and the proxy up, and the Job
# never records a completion. The fix on a current GKE version is the native
# sidecar: the proxy moves to initContainers with restartPolicy Always, so
# it starts first and is stopped when the regular containers finish.

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
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: "${var.job_name}"
      labels:
        app: "${var.job_name}"
        managed-by: kube-agents-bench
    spec:
      backoffLimit: 0
      template:
        metadata:
          labels:
            app: "${var.job_name}"
        spec:
          restartPolicy: Never
          automountServiceAccountToken: false
          securityContext:
            runAsNonRoot: true
            runAsUser: 65534
            seccompProfile:
              type: RuntimeDefault
          containers:
            - name: "${var.worker_name}"
              image: busybox:1.36
              command: ["sh", "-c", "echo 'export started'; sleep ${var.export_seconds}; echo 'export done, ${var.export_rows} rows written'"]
              resources:
                requests:
                  cpu: 50m
                  memory: 64Mi
                limits:
                  cpu: 50m
                  memory: 64Mi
            - name: "${var.proxy_name}"
              image: busybox:1.36
              command: ["sh", "-c", "echo 'proxy listening on port ${var.proxy_port}'; exec sleep infinity"]
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
  stack                 = "job-sidecar-proxy-never-completes"
  labels                = local.ci_labels
  manifest              = local.manifest
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
