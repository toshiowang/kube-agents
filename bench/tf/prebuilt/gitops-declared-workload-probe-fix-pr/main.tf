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

# The scenario driver for bench/tasks/gitops-declared-workload-probe-fix-pr.
#
# The slow-start liveness shape, declared: the same manifest is committed
# to the install's GitOps repository on a scratch branch, under the layout
# the repository already uses (clusters/<cluster>/<namespace>/<name>.yaml),
# and planted live through the namespaced-plant module. The case asks for
# the fix through the change process, so the product must find the manifest
# in the repository, edit the probe there and open a pull request against
# the scratch branch, applying nothing to the cluster. The branch is created
# from the default branch's head and deleted on destroy, which also closes
# any pull request opened against it; the default branch is never written.

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
  ci_labels = {
    "managed-by"  = "kube-agents-bench"
    "build-id"    = var.prow_build_id != "" ? var.prow_build_id : "local"
    "pull-number" = var.prow_pull_number != "" ? var.prow_pull_number : "none"
  }

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

  # The declared copy carries the namespace, as a repository manifest does.
  declared_manifest = replace(local.manifest, "metadata:\n  name: \"${var.workload_name}\"\n", "metadata:\n  name: \"${var.workload_name}\"\n  namespace: \"${var.namespace}\"\n")
  declared_path     = "clusters/${var.gitops_cluster_dir}/${var.namespace}/${var.workload_name}.yaml"
  declare_script    = "${path.module}/declare.sh"
}

module "plant" {
  source = "../../modules/namespaced-plant"

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.namespace
  stack                 = "gitops-declared-workload-probe-fix-pr"
  labels                = local.ci_labels
  manifest              = local.manifest
}

# The declared copy in the repository, on a scratch branch cut from the
# default branch's head; destroy deletes the branch.
resource "null_resource" "declare" {
  triggers = {
    repo     = var.gitops_repo
    branch   = var.gitops_branch
    path     = local.declared_path
    manifest = sha256(local.declared_manifest)
    script   = filesha256(local.declare_script)
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = "bash '${local.declare_script}' declare"
    environment = {
      DECLARE_REPO     = var.gitops_repo
      DECLARE_BRANCH   = var.gitops_branch
      DECLARE_PATH     = local.declared_path
      DECLARE_MANIFEST = local.declared_manifest
    }
  }

  provisioner "local-exec" {
    when        = destroy
    on_failure  = continue
    interpreter = ["/bin/bash", "-c"]
    command     = "bash \"$DECLARE_SCRIPT\" undeclare"
    environment = {
      DECLARE_SCRIPT = "${path.module}/declare.sh"
      DECLARE_REPO   = self.triggers.repo
      DECLARE_BRANCH = self.triggers.branch
    }
  }
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
