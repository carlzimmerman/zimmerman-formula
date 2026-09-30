#!/bin/bash
# CFG237 re-run (phase 2, before any CFG227 output is opened). Uses ZF_REPO or walks up from this directory.
set -u
cd "$(dirname "$0")"
for s in CFG237_main CFG237_classes CFG237_power CFG237_s1_anomaly CFG237_cristal_route CFG237_c7 CFG237_attacks_misc; do
  python3 $s.py > /dev/null 2>&1; echo "$s exit $?"
done
python3 CFG237_MUTATE.py
