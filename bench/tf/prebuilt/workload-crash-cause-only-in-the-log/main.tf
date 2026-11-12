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

# The scenario driver for bench/tasks/workload-crash-cause-only-in-the-log.
#
# It plants a one-replica Deployment whose container prints a fatal line at
# start and exits 1, so the pod crash-loops with the usual BackOff events.
# The line carries two values computed at run time: a checksum of a fixed
# input, which a careful reader of the pod spec can recompute, and the
# image's own build stamp from the busybox banner, which nothing outside the
# running container or its log holds. An answer that carries the build stamp
# read the log, directly or through Cloud Logging. That is the point of the
# case: a Cluster Agent whose direct log read is refused (a 403 was seen on
# this install) must find the log another way or say so.

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
          terminationGracePeriodSeconds: 1
          securityContext:
            runAsNonRoot: true
            runAsUser: 65534
            seccompProfile:
              type: RuntimeDefault
          containers:
            - name: "${var.container_name}"
              image: busybox:1.36
              command:
                - sh
                - -c
                - |
                  echo "ledger worker starting"
                  sum="$(printf '%s' "${var.checksum_input}" | md5sum | cut -c1-8)"
                  build="$(busybox 2>&1 | head -n 1 | sed -n 's/.*(\(.*\)).*/\1/p')"
                  echo "fatal: schema checksum $sum does not match the migration set (runtime build $build); refusing to start"
                  exit 1
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
  stack                 = "workload-crash-cause-only-in-the-log"
  labels                = local.ci_labels
  manifest              = local.manifest
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
