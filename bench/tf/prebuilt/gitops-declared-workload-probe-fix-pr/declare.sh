#!/bin/bash
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

# The repository half of the gitops-declared-workload-probe-fix-pr stack:
# `declare` cuts a scratch branch from the default branch's head and writes
# the declared manifest on it; `undeclare` deletes the branch, which also
# closes any pull request opened against it. The default branch is never
# written. Runs with the runner's GitHub credential (BENCH_GITHUB_TOKEN,
# else GITHUB_TOKEN, else gh's own login).
set -euo pipefail

readonly DECLARE_API="https://api.github.com"
readonly DECLARE_COMMIT_MESSAGE="declare the slow-start ledger workload for the probe fix case"

declare_require() { # <name>
  if [ -z "${!1:-}" ]; then
    echo "ERROR: $1 is not set; the stack's provisioner passes it." >&2
    exit 1
  fi
}

declare_token() {
  if [ -n "${BENCH_GITHUB_TOKEN:-}" ]; then printf '%s' "$BENCH_GITHUB_TOKEN"; return; fi
  if [ -n "${GITHUB_TOKEN:-}" ]; then printf '%s' "$GITHUB_TOKEN"; return; fi
  gh auth token
}

declare_api() { # <method> <path> [json-body]; an empty path is the repository itself
  local method="$1" path="$2" body="${3:-}" url="$DECLARE_API/repos/$DECLARE_REPO"
  if [ -n "$path" ]; then url="$url/$path"; fi
  if [ -n "$body" ]; then
    curl -fsS -X "$method" -H "Authorization: Bearer $DECLARE_TOKEN" -H "Accept: application/vnd.github+json" "$url" -d "$body"
  else
    curl -fsS -X "$method" -H "Authorization: Bearer $DECLARE_TOKEN" -H "Accept: application/vnd.github+json" "$url"
  fi
}

declare_require DECLARE_REPO; declare_require DECLARE_BRANCH
DECLARE_TOKEN="$(declare_token)"
readonly DECLARE_TOKEN

case "${1:-}" in
  declare)
    declare_require DECLARE_PATH; declare_require DECLARE_MANIFEST
    # A leftover branch of this name is this stack's own: delete it first so
    # the branch always starts from the default branch's current head.
    if declare_api GET "git/ref/heads/$DECLARE_BRANCH" >/dev/null 2>&1; then
      echo "Deleting the leftover branch $DECLARE_BRANCH before declaring."
      declare_api DELETE "git/refs/heads/$DECLARE_BRANCH" >/dev/null
    fi
    default_branch="$(declare_api GET "" | python3 -c 'import json,sys; print(json.load(sys.stdin)["default_branch"])')"
    base_sha="$(declare_api GET "git/ref/heads/$default_branch" | python3 -c 'import json,sys; print(json.load(sys.stdin)["object"]["sha"])')"
    declare_api POST "git/refs" "$(python3 -c 'import json,sys; print(json.dumps({"ref": "refs/heads/"+sys.argv[1], "sha": sys.argv[2]}))' "$DECLARE_BRANCH" "$base_sha")" >/dev/null
    content_b64="$(printf '%s' "$DECLARE_MANIFEST" | base64 | tr -d '\n')"
    declare_api PUT "contents/$DECLARE_PATH" "$(python3 -c 'import json,sys; print(json.dumps({"message": sys.argv[1], "content": sys.argv[2], "branch": sys.argv[3]}))' "$DECLARE_COMMIT_MESSAGE" "$content_b64" "$DECLARE_BRANCH")" >/dev/null
    echo "Declared $DECLARE_PATH on $DECLARE_REPO branch $DECLARE_BRANCH (from $default_branch at ${base_sha:0:9})."
    ;;
  undeclare)
    if declare_api GET "git/ref/heads/$DECLARE_BRANCH" >/dev/null 2>&1; then
      declare_api DELETE "git/refs/heads/$DECLARE_BRANCH" >/dev/null
      echo "Deleted branch $DECLARE_BRANCH on $DECLARE_REPO."
    else
      echo "Branch $DECLARE_BRANCH on $DECLARE_REPO is already gone."
    fi
    ;;
  *)
    echo "usage: declare.sh declare|undeclare" >&2
    exit 2
    ;;
esac
