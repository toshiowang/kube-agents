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
  description = "Region or zone of host_cluster_name."
}

variable "project_id" {
  type        = string
  description = "GCP project holding host_cluster_name; empty means the gcloud default project."
  default     = ""
}

variable "namespace" {
  type        = string
  description = "Namespace the Job is planted in. The case's prompt and checks name the same namespace."
  default     = "eval-nightly-export"
}

variable "job_name" {
  type        = string
  description = "Name of the planted Job; the case's objective requires it and the prompt does not say it."
  default     = "ledger-export"
}

variable "worker_name" {
  type        = string
  description = "Name of the container that does the export and exits."
  default     = "exporter"
}

variable "proxy_name" {
  type        = string
  description = "Name of the proxy container that never exits; the case's objective requires it and the prompt does not say it."
  default     = "sql-proxy"
}

variable "proxy_port" {
  type        = number
  description = "Port the proxy claims to listen on, in its log line only."
  default     = 5432
}

variable "export_seconds" {
  type        = number
  description = "Seconds the worker runs before it exits 0."
  default     = 20
}

variable "export_rows" {
  type        = number
  description = "Row count the worker logs when done."
  default     = 1240
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
