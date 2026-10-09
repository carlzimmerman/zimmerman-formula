#!/bin/bash
# CFG506: run every box sequentially (one 512^3 load at a time), then diagnostics and scoring. Logs in ../../../_external_data/cfg506_work/
cd "$(dirname "$0")"
W=../../../_external_data/cfg506_work
for K in "$@"; do
  nice -n 15 python3 -u cfg506_box.py "$K" > "$W/log_$K.txt" 2>&1
  echo "$K rc=$?" >> "$W/run_506.log"
done
