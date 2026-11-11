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

# The scenario driver for bench/tasks/storage-immediate-binding-zonal-pd-affinity-conflict.
#
# It plants a claim on the cluster's built-in `standard` StorageClass, whose
# volumeBindingMode is Immediate on GKE Standard and Autopilot alike, so the
# zonal disk is provisioned the moment the claim is created, in a zone the
# scheduler had no say in. A second step then reads the zone the volume
# landed in and creates a one-replica Deployment pinned by nodeSelector to a
# different zone of the same cluster, mounting that claim. No node can
# satisfy both the selector and the volume's node affinity, so the pod stays
# Pending. The zone is read rather than chosen because a StorageClass that
# pins it would be a cluster-scoped plant the namespace destroy cannot
# remove, and the built-in class is the shape a customer's cluster has.
#
# The second step lives in the same namespace as the claim, so the module's
# destroy removes both; a failure in it fails the apply and the module's
# destroy clears the namespace on teardown.

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

  manifest = <<-MANIFEST
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: "${var.claim_name}"
      labels:
        app: "${var.workload_name}"
        managed-by: kube-agents-bench
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: "${var.storage_class}"
      resources:
        requests:
          storage: "${var.claim_size}"
  MANIFEST

  pin_script = "${path.module}/pin_workload.sh"
}

module "plant" {
  source = "../../modules/namespaced-plant"

  host_cluster_name     = var.host_cluster_name
  host_cluster_location = var.host_cluster_location
  project_id            = var.project_id
  namespace             = var.namespace
  stack                 = "storage-immediate-binding-zonal-pd-affinity-conflict"
  labels                = local.ci_labels
  manifest              = local.manifest
}

# Step two: wait for the claim to bind, read the volume's zone, and create the
# Deployment pinned to another zone. Destroy is the namespace delete the
# module runs.
resource "null_resource" "pin" {
  depends_on = [module.plant]

  triggers = {
    namespace = var.namespace
    workload  = var.workload_name
    claim     = var.claim_name
    script    = filesha256(local.pin_script)
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = "bash '${local.pin_script}'"
    environment = {
      PIN_HOST_CLUSTER  = var.host_cluster_name
      PIN_HOST_LOCATION = var.host_cluster_location
      PIN_PROJECT       = var.project_id
      PIN_NAMESPACE     = var.namespace
      PIN_CLAIM         = var.claim_name
      PIN_WORKLOAD      = var.workload_name
      PIN_CONTAINER     = var.container_name
      PIN_MOUNT_PATH    = var.mount_path
    }
  }
}

output "cluster_name" {
  value = module.plant.cluster_name
}

output "cluster_location" {
  value = module.plant.cluster_location
}
