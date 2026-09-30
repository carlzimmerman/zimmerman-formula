#!/usr/bin/env bash
# CFG230 run-all: main runs A..H (each must exit 0), then every MUTATE control with its frozen expected exit code.
# Usage: ZF_REPO=<repo root> bash CFG230_run_all.sh      (inside the repo the root is found by walking up from the script)
cd "$(dirname "$0")" || exit 2
out=CFG230_run_all.out; : > "$out"
say() { echo "$*" | tee -a "$out"; }
say "CFG230 run-all; repo=<repo>"
bad=0
for s in A_evidence_audit B_scaling_lemma C_shape_kernel D_reaction_energy_cold E_tail_bound F_incidence_pincers G_screening H_claims_audit; do
  python3 -B "CFG230_$s.py" > /dev/null 2>"CFG230_${s}.stderr"; rc=$?
  say "main   $s exit $rc (expected 0)"; [ $rc -ne 0 ] && bad=1
  [ -s "CFG230_${s}.stderr" ] || rm -f "CFG230_${s}.stderr"
done
# control, script, expected exit (1 = bites, 0 = does not bite)
while read -r m s e; do
  MUTATE=$m python3 -B "CFG230_$s.py" > /dev/null 2>&1; rc=$?
  st=OK; [ "$rc" -ne "$e" ] && { st=UNEXPECTED; bad=1; }
  say "MUTATE $m in $s exit $rc (frozen expectation $e) $st"
done <<'LIST'
M1 F_incidence_pincers 1
M2 F_incidence_pincers 0
M3 H_claims_audit 1
M4 C_shape_kernel 1
M4 E_tail_bound 1
M5 B_scaling_lemma 1
M5 E_tail_bound 1
M6 B_scaling_lemma 1
M7 F_incidence_pincers 1
M8 G_screening 1
M9 H_claims_audit 1
M9b H_claims_audit 0
LIST
say "run-all finished; unexpected outcomes: $bad"
exit 0
