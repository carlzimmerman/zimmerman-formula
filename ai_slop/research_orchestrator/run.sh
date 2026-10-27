#!/usr/bin/env bash
# Default: status. To grind: ./run.sh run --continuous
set -euo pipefail
cd "$(dirname "$0")"
PY="${ORCH_PYTHON:-/opt/homebrew/Caskroom/miniconda/base/bin/python3}"
exec "$PY" -B orchestrator.py "$@"
