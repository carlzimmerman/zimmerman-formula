#!/bin/bash
# CFG157 re-run.  Usage (from this directory):  ZF_REPO=<repo root> ./run_all.sh     (ZF_REPO only needed for the post-hoc Bcommon import)
# Expected exit codes: mains 0; MUTATE sign/kernel/target (g1) 1; MUTATE pm_target (b1) 1; posthoc 0.
cd "$(dirname "$0")" || exit 2
export PYTHONDONTWRITEBYTECODE=1
rc=()
python3 cfg157_g1.py > /dev/null; rc+=("g1 main:$?")
for m in sign kernel target; do MUTATE=$m python3 cfg157_g1.py > /dev/null; rc+=("g1 MUTATE=$m:$?"); done
python3 cfg157_b1.py > /dev/null; rc+=("b1 main:$?")
MUTATE=pm_target python3 cfg157_b1.py > /dev/null; rc+=("b1 MUTATE=pm_target:$?")
python3 cfg157_posthoc_numono.py > /dev/null; rc+=("posthoc numono:$?")
printf '%s\n' "${rc[@]}" | tee run_all.out
