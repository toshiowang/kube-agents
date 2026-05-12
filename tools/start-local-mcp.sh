#!/usr/bin/env bash
# Start the local gke-mcp binary in HTTP mode.
# Agents in containers reach this via http://host.docker.internal:9080/mcp.
#
# Port 9080 is used (not 8080) to avoid colliding with Scion's web dashboard.

set -euo pipefail

PORT="${GKE_MCP_PORT:-9080}"

if ! command -v gke-mcp >/dev/null 2>&1; then
  cat >&2 <<EOF
Error: 'gke-mcp' binary not found on PATH.

Install via:
  curl -sSL https://raw.githubusercontent.com/GoogleCloudPlatform/gke-mcp/main/install.sh | bash

Or build from source:
  go install github.com/GoogleCloudPlatform/gke-mcp@latest
EOF
  exit 1
fi

if ! gcloud auth application-default print-access-token >/dev/null 2>&1; then
  echo "Warning: ADC not available. Run 'gcloud auth application-default login' first." >&2
fi

echo "[gke-mcp] starting HTTP server on 0.0.0.0:$PORT"
echo "[gke-mcp] agents reach this at: http://host.docker.internal:$PORT/mcp"
exec gke-mcp --server-mode http --server-port "$PORT"
