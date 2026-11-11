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

# The scenario driver for bench/tasks/workload-liveness-kills-slow-start-no-startupprobe.
#
# It plants a one-replica Deployment whose container sleeps through a
# warm-up before it serves its health path, under a livenessProbe that
# allows 15 seconds (periodSeconds 5, failureThreshold 3) and no
# startupProbe. The kubelet kills the container before it ever serves, so
# the pod crash-loops with a climbing restart count; the readinessProbe on
# the same path keeps it out of Ready for the whole cycle. The grace period
# is one second because busybox `sh` as PID 1 ignores SIGTERM, and a 30 s
# wait per cycle would hide the loop behind long Terminating phases.
#
# The health path and the workload name are the planted nouns the case's
# objective reads: neither is in the prompt, and an answer that did not read
# the pod spec or its events cannot name them. The file served after the
# warm-up exists, so the probe passes once the container is up: the defect
# is the missing startupProbe, not a wrong path.

terraform {
  required_version = ">= 1.5.0"
}

locals {
  ci_labels = {
    "managed-by"  = "kube-agents-bench"
    "build-id"    = var.prow_build_id != "" ? var.prow_build_id : "local"
    "pull-number" = var.prow_pull_number != "" ? var.prow_pull_number : "none"
  }

  # /tmp because the container runs as nobody and the image root is not
  # writable by that user.
  serve_root = "/tmp/www"
  command    = "sleep ${var.warmup_seconds} && mkdir -p ${local.serve_root}${dirname(var.health_path)} && echo ok > ${local.serve_root}${var.health_path} && exec httpd -f -p ${var.health_port} -h ${local.serve_root}"

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
              command: ["sh", "-c", "${local.command}"]
              ports:
                - name: http
                  containerPort: ${var.health_port}
              livenessProbe:
                httpGet:
                  path: "${var.health_path}"
                  port: ${var.health_port}
                periodSeconds: 5
                failureThreshold: 3
              readinessProbe:
                httpGet:
                  path: "${var.health_path}"
                  port: ${var.health_port}
                periodSeconds: 5
                failureThreshold: 3
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
  stack                 = "workload-liveness-kills-slow-start-no-startupprobe"
  labels                = local.ci_labels
  manifest              = local.manifest
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
