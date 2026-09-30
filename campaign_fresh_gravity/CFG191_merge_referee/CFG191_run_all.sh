#!/usr/bin/env bash
# Re-run of every CFG191 script, main then MUTATE=1; prints each exit code.  Usage: ZF_REPO=<repo> bash CFG191_run_all.sh   (from anywhere)
# Expected: main exits 0 for every script; MUTATE=1 exits 1 for every script (the control bites).
# Times: s1-s5 < 15 s each; s5b ~4 min main / ~2 min MUTATE; s5c ~3 min per mode.
# CFG191_compare_cfg179.py is PHASE 2: it reads CFG179's text outputs and must only be run after all of the above were saved (it is last).
cd "$(dirname "$0")"
for s in CFG191_s1_theorem CFG191_s2_coma_udg CFG191_s3_solar_q2 CFG191_s4_scorecard CFG191_s5_dr4_mapping CFG191_s5b_pipeline_tier2 CFG191_s5c_picard_check; do
  python3 $s.py > /dev/null 2> $s.err; echo "$s main rc=$?"
  MUTATE=1 python3 $s.py > /dev/null 2> ${s}_MUTATE.err; echo "$s MUTATE=1 rc=$?"
done
python3 CFG191_verdict.py; echo "CFG191_verdict rc=$?"
python3 CFG191_compare_cfg179.py > /dev/null; echo "CFG191_compare_cfg179 rc=$?"
