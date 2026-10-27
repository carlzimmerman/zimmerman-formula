#!/bin/sh
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$script_dir/check_round2.py" "${1:-/tmp/horizon-round2-results.json}"
