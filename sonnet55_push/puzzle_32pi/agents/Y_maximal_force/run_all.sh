#!/bin/sh
# re-run every script of lane Y; exit 0 iff all exit 0
cd "$(dirname "$0")" || exit 1
rc=0
for f in y01_static_bookkeeping y02_cmetric_exact y03_cmetric_horizons y04_principle_table y05_consequences_and_data; do
  python3 "$f.py" > "$f.out" 2>&1 || rc=1
  printf '%s: ' "$f"; tail -n 1 "$f.out"
done
exit $rc
