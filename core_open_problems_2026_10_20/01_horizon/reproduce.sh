#!/bin/sh
set -eu
# Portable reproduction; optional first argument selects the output JSON.
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$here/check_horizon.py" "${1:-$here/reproduced/results.json}"
