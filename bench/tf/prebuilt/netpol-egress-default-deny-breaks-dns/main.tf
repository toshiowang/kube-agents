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

# The scenario driver for bench/tasks/netpol-egress-default-deny-breaks-dns.
#
# It plants a namespace whose only NetworkPolicy selects every pod and
# declares Egress with no rules, so on a Dataplane V2 cluster nothing leaves
# the namespace, name lookups included, and a client Deployment whose loop
# resolves an in-cluster name and logs each failure. The pod runs and never
# restarts: the evidence is the policy and the log, not a pod state. The fix
# is an egress rule to the cluster's DNS (UDP and TCP 53 to kube-dns, and the
# NodeLocal DNSCache address where it runs), not an open egress.

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
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: "${var.policy_name}"
      labels:
        managed-by: kube-agents-bench
    spec:
      podSelector: {}
      policyTypes: ["Egress"]
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
              command:
                - sh
                - -c
                - |
                  while true; do
                    if nslookup ${var.lookup_name} >/dev/null 2>&1; then
                      echo "lookup ok ${var.lookup_name}"
                    else
                      echo "lookup failed ${var.lookup_name}: no DNS server reachable"
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

module "plant" {
  source = "../../modules/namespaced-plant"

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.namespace
  stack                 = "netpol-egress-default-deny-breaks-dns"
  labels                = local.ci_labels
  manifest              = local.manifest
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
