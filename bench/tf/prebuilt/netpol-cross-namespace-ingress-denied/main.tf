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

# The scenario driver for bench/tasks/netpol-cross-namespace-ingress-denied.
#
# Two namespaces. The server namespace holds a Deployment, its Service and an
# ingress NetworkPolicy that admits only pods carrying a client label, with a
# podSelector alone. A podSelector in a `from` entry selects pods in the
# policy's own namespace only, so the client in the other namespace, which
# carries that very label, is denied: its loop logs a failed request every
# few seconds while both pods stay Running. The fix is a namespaceSelector in
# the same `from` entry as the podSelector, not a wider policy.
#
# Two module instances, one per namespace, under one stack label; each
# instance's destroy removes its own namespace. The client is created after
# the server so its first log lines already show the denial.

terraform {
  required_version = ">= 1.5.0"
}

locals {
  ci_labels = {
    "managed-by"  = "kube-agents-bench"
    "build-id"    = var.prow_build_id != "" ? var.prow_build_id : "local"
    "pull-number" = var.prow_pull_number != "" ? var.prow_pull_number : "none"
  }

  server_manifest = <<-MANIFEST
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: "${var.server_name}"
      labels:
        app: "${var.server_name}"
        managed-by: kube-agents-bench
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: "${var.server_name}"
      template:
        metadata:
          labels:
            app: "${var.server_name}"
        spec:
          automountServiceAccountToken: false
          securityContext:
            runAsNonRoot: true
            runAsUser: 65534
            seccompProfile:
              type: RuntimeDefault
          containers:
            - name: app
              image: busybox:1.36
              command: ["sh", "-c", "mkdir -p /tmp/www && echo ok > /tmp/www/index.html && exec httpd -f -p ${var.server_port} -h /tmp/www"]
              ports:
                - name: http
                  containerPort: ${var.server_port}
              resources:
                requests:
                  cpu: 50m
                  memory: 64Mi
                limits:
                  cpu: 50m
                  memory: 64Mi
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: "${var.server_name}"
      labels:
        managed-by: kube-agents-bench
    spec:
      selector:
        app: "${var.server_name}"
      ports:
        - name: http
          port: 80
          targetPort: ${var.server_port}
    ---
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: "${var.policy_name}"
      labels:
        managed-by: kube-agents-bench
    spec:
      podSelector:
        matchLabels:
          app: "${var.server_name}"
      policyTypes: ["Ingress"]
      ingress:
        - from:
            - podSelector:
                matchLabels:
                  role: "${var.client_role}"
          ports:
            - protocol: TCP
              port: ${var.server_port}
  MANIFEST

  client_manifest = <<-MANIFEST
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: "${var.client_name}"
      labels:
        app: "${var.client_name}"
        managed-by: kube-agents-bench
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: "${var.client_name}"
      template:
        metadata:
          labels:
            app: "${var.client_name}"
            role: "${var.client_role}"
        spec:
          automountServiceAccountToken: false
          securityContext:
            runAsNonRoot: true
            runAsUser: 65534
            seccompProfile:
              type: RuntimeDefault
          containers:
            - name: app
              image: busybox:1.36
              command:
                - sh
                - -c
                - |
                  url="http://${var.server_name}.${var.server_namespace}.svc.cluster.local/"
                  while true; do
                    if wget -q -O /dev/null -T 3 "$url"; then
                      echo "request ok $url"
                    else
                      echo "request failed $url: timed out"
                    fi
                    sleep ${var.loop_seconds}
                  done
              resources:
                requests:
                  cpu: 50m
                  memory: 64Mi
                limits:
                  cpu: 50m
                  memory: 64Mi
  MANIFEST
}

module "server" {
  source = "../../modules/namespaced-plant"

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.server_namespace
  stack                 = "netpol-cross-namespace-ingress-denied"
  labels                = local.ci_labels
  manifest              = local.server_manifest
}

module "client" {
  source     = "../../modules/namespaced-plant"
  depends_on = [module.server]

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.client_namespace
  stack                 = "netpol-cross-namespace-ingress-denied"
  labels                = local.ci_labels
  manifest              = local.client_manifest
}

output "cluster_name" {
  value = module.server.cluster_name
}

output "cluster_location" {
  value = module.server.cluster_location
}
