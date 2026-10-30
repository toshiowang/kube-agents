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

# The scenario driver for bench/tasks/security-expiring-node-bootstrap-and-webhook-certs.
#
# It plants a TLS Secret whose certificate expires five days after the apply,
# the shape of a webhook serving certificate about to lapse. The compliance
# audit is expected to miss the pattern today.
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

      certdir="$(mktemp -d)"
      openssl req -x509 -newkey rsa:2048 -nodes -days 5 -subj "/CN=strict-policy-webhook.${local.ns}.svc" \
        -keyout "$certdir/tls.key" -out "$certdir/tls.crt" >/dev/null 2>&1
      kubectl create namespace "${local.ns}" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
      kubectl label namespace "${local.ns}" --overwrite created-by-stack=security-expiring-node-bootstrap-and-webhook-certs managed-by=kube-agents-bench >/dev/null
      kubectl -n "${local.ns}" create secret tls "${local.target}" --cert "$certdir/tls.crt" --key "$certdir/tls.key" --dry-run=client -o yaml | kubectl apply -f -
      kubectl -n "${local.ns}" label secret "${local.target}" --overwrite managed-by=kube-agents-bench
      rm -rf "$certdir"
      if ! kubectl get namespace "${local.ns}" >/dev/null 2>&1; then
        kubectl create namespace "${local.ns}"
        kubectl label namespace "${local.ns}" --overwrite \
          managed-by="${local.ci_labels["managed-by"]}" \
          build-id="${local.ci_labels["build-id"]}" \
          pull-number="${local.ci_labels["pull-number"]}" \
          created-by-stack=security-expiring-node-bootstrap-and-webhook-certs
      fi
      kubectl apply -f - <<'MANIFEST'
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: admission-webhook-tls-cert-note
        namespace: ${local.ns}
        labels:
          managed-by: kube-agents-bench
      data:
        note: "the TLS Secret admission-webhook-tls-cert beside this ConfigMap carries a certificate that expires in five days"
      MANIFEST
      echo "Planted scenario security-expiring-node-bootstrap-and-webhook-certs on ${var.host_cluster_name}."
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
      kubectl -n "${self.triggers.namespace}" delete secret "${self.triggers.target}" --ignore-not-found
      kubectl -n "${self.triggers.namespace}" delete configmap admission-webhook-tls-cert-note --ignore-not-found
      if [ "$(kubectl get namespace "${self.triggers.namespace}" -o jsonpath='{.metadata.labels.created-by-stack}' 2>/dev/null)" = "security-expiring-node-bootstrap-and-webhook-certs" ]; then
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
