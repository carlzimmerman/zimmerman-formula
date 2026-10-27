#!/usr/bin/env bash
# Explicit launchd entry point; no service is enabled by this file.
set -euo pipefail
cd "$(dirname "$0")"
[ ! -f "$HOME/.orch_env" ] || source "$HOME/.orch_env"
PY="${ORCH_PYTHON:-/opt/homebrew/Caskroom/miniconda/base/bin/python3}"
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/local/bin:$PATH"
exec "$PY" -B orchestrator.py run --continuous
