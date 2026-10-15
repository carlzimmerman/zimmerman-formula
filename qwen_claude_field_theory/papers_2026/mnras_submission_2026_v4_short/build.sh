#!/usr/bin/env bash
# Build the short MNRAS manuscript.  Run from this directory.  Order: figure -> numbers (fails on any mismatch) -> PDF.
set -euo pipefail
cd "$(dirname "$0")"
python3 make_figure.py
python3 short_numbers.py
tectonic --keep-intermediates --keep-logs mnras_a0_lambda_short.tex
python3 - <<'PY'
import subprocess,re
t=subprocess.run(["pdfinfo","mnras_a0_lambda_short.pdf"],capture_output=True,text=True).stdout
print([l for l in t.splitlines() if l.startswith("Pages")])
PY
