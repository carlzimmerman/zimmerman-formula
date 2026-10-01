#!/bin/bash
# CFG244 full re-run: gate order H, A (then D only as a labelled POST-HOC extra because A binds), every MUTATE with its frozen expected exit code,
# then the verdict.  Usage: ZF_REPO=<repo root> bash CFG244_run_all.sh   (inside the repository the root is found by walking up).
# About 2 minutes on 14 processes.  No output prints an absolute home path.
cd "$(dirname "$0")" || exit 1
export PYTHONDONTWRITEBYTECODE=1
unexpected=0
run() {  # name expected_exit cmd...
  name=$1; exp=$2; shift 2
  "$@" > "run_${name}.log" 2>&1; obs=$?
  flag="ok"; if [ "$obs" != "$exp" ]; then flag="UNEXPECTED"; unexpected=$((unexpected+1)); fi
  echo "  $name: expected exit $exp, observed $obs  [$flag]"
}
echo "== main runs (frozen order) =="
run H_main 0 python3 CFG244_H_satellites.py
run A_main 0 python3 CFG244_A_infall_bound.py
run D_posthoc 0 python3 CFG244_D_distinctness_POSTHOC.py
echo "== MUTATE controls (exit 1 = the control bites; MA4 is the declared non-biting control) =="
for m in MH1 MH2 MH3 MH4 MH5; do run H_$m 1 env MUTATE=$m python3 CFG244_H_satellites.py; done
for m in MA1 MA2 MA3 MA5; do run A_$m 1 env MUTATE=$m python3 CFG244_A_infall_bound.py; done
run A_MA4 0 env MUTATE=MA4 python3 CFG244_A_infall_bound.py
run D_MD1 1 env MUTATE=MD1 python3 CFG244_D_distinctness_POSTHOC.py
echo "== verdict =="
python3 CFG244_verdict.py
echo "unexpected outcomes: $unexpected"
