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

variable "host_cluster_name" {
  type        = string
  description = "Name of the cluster the scenario is planted on; arrives as TF_VAR_host_cluster_name from the runner."
}

variable "host_cluster_location" {
  type        = string
  description = "Region or zone of host_cluster_name. The scenario needs a cluster that enforces NetworkPolicy (Dataplane V2)."
}

variable "project_id" {
  type        = string
  description = "GCP project holding host_cluster_name; empty means the gcloud default project."
  default     = ""
}

variable "server_namespace" {
  type        = string
  description = "Namespace of the server, its Service and the ingress policy. The case's checks name it."
  default     = "eval-payments"
}

variable "client_namespace" {
  type        = string
  description = "Namespace of the client whose requests are denied. The case's prompt and checks name it."
  default     = "eval-checkout"
}

variable "server_name" {
  type        = string
  description = "Name of the server Deployment and its Service; the case's objective requires it and the prompt does not say it."
  default     = "payments-api"
}

variable "server_port" {
  type        = number
  description = "Port the server container serves on; the Service maps 80 to it."
  default     = 8080
}

variable "policy_name" {
  type        = string
  description = "Name of the planted ingress NetworkPolicy; the case's objective requires it and the prompt does not say it."
  default     = "payments-ingress-lockdown"
}

variable "client_name" {
  type        = string
  description = "Name of the client Deployment in the other namespace."
  default     = "checkout-web"
}

variable "client_role" {
  type        = string
  description = "Label value the policy admits with a podSelector alone, carried by the client in the other namespace."
  default     = "payments-client"
}

variable "loop_seconds" {
  type        = number
  description = "Seconds between client requests."
  default     = 10
}

variable "prow_build_id" {
  type        = string
  description = "Prow BUILD_ID of the run creating this infra."
  default     = ""
}

variable "prow_pull_number" {
  type        = string
  description = "Pull request number the run belongs to."
  default     = ""
}
