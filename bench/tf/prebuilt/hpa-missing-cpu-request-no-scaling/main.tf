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

# The scenario driver for bench/tasks/hpa-missing-cpu-request-no-scaling.
#
# It plants a one-replica Deployment whose container sets no resources
# block, and a HorizontalPodAutoscaler on it that targets CPU utilization.
# Utilization is usage over request, and with no request the metrics
# pipeline has nothing to divide by: the autoscaler reports
# FailedGetResourceMetric ("missing request for cpu") in its conditions and
# events, ScalingActive stays False, and the replica count never moves. The
# fix is a CPU request on the container, not a different metric.
#
# The shape holds on a Standard host: Autopilot admission writes requests
# onto every container, so the autoscaler there has a denominator.

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
          securityContext:
            runAsNonRoot: true
            runAsUser: 65534
            seccompProfile:
              type: RuntimeDefault
          containers:
            - name: "${var.container_name}"
              image: busybox:1.36
              command: ["sh", "-c", "mkdir -p /tmp/www && echo ok > /tmp/www/index.html && exec httpd -f -p ${var.port} -h /tmp/www"]
              ports:
                - name: http
                  containerPort: ${var.port}
    ---
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: "${var.workload_name}"
      labels:
        managed-by: kube-agents-bench
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: "${var.workload_name}"
      minReplicas: 1
      maxReplicas: ${var.max_replicas}
      metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: ${var.target_utilization}
  MANIFEST
}

module "plant" {
  source = "../../modules/namespaced-plant"

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.namespace
  stack                 = "hpa-missing-cpu-request-no-scaling"
  labels                = local.ci_labels
  manifest              = local.manifest
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
