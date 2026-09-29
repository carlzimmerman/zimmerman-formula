#!/usr/bin/env bash
# Build and verify the puzzle_32pi Lean bridge certificates.
#   ./verify_bridges.sh            builds the 8 modules in dependency order, audits every theorem, runs every MUTATE control
# Exit 0 iff: (a) every main file compiles with no error and no sorry; (b) every theorem (110) depends only on
# [propext, Classical.choice, Quot.sound]; (c) every mutated theorem FAILS to compile; (d) every refutation twin compiles.
# Uses the toolchain of the READ-ONLY library fable_independent_2026/lean_2026 (only `lake env` is queried); writes only here.
set -u
cd "$(dirname "$0")"
STD='\[propext, Classical.choice, Quot.sound\]'
MODS="H1_bpst H2_s4_euler H3_horizon_area_lambda H4_graviton H5_freefall H6_nonembed H7_p09_reduction Bridges32pi"
fail=0
echo "== 1. main modules (build order) =="
for m in $MODS; do
  ./lean.sh -o "$m.lean" > "$m.out" 2>&1; rc=$?
  n=$(grep -c "depends on axioms" "$m.out"); e=$(grep -c "error" "$m.out")
  s=$(grep -c "sorry" "$m.out"); b=$(grep "depends on axioms" "$m.out" | grep -v -E "$STD" | wc -l | tr -d ' ')
  echo "$m: exit $rc, headline #print axioms: $n, errors: $e, sorry mentions: $s, non-standard axioms: $b"
  if [ "$rc" != "0" ] || [ "$e" != "0" ] || [ "$s" != "0" ] || [ "$b" != "0" ]; then fail=1; fi
done
echo "== 2. source scan for sorry / admit / axiom / native_decide in the main files =="
bad=$(grep -n -E "\bsorry\b|\badmit\b|^axiom |^ *axiom |native_decide" $(for m in $MODS; do echo $m.lean; done) | wc -l | tr -d ' ')
echo "matches: $bad"; [ "$bad" = "0" ] || fail=1
echo "== 3. full axiom audit: every theorem of the 8 modules =="
python3 gen_axioms.py
./lean.sh Axioms_all.lean > Axioms_all.out 2>&1
want=$(grep -c "^#print axioms" Axioms_all.lean); got=$(grep -c "depends on axioms" Axioms_all.out)
nonstd=$(grep "depends on axioms" Axioms_all.out | grep -v -E "$STD" | wc -l | tr -d ' ')
err=$(grep -c "error" Axioms_all.out)
echo "theorems: $want, audited: $got, non-standard: $nonstd, errors: $err"
{ [ "$want" = "$got" ] && [ "$nonstd" = "0" ] && [ "$err" = "0" ] && [ "$want" -gt 0 ]; } || fail=1
echo "== 4. MUTATE controls (false variants must FAIL; refutation twins must COMPILE) =="
totm=0; totr=0
for m in $MODS; do
  f="${m}_MUTATE"
  ./lean.sh "$f.lean" > "$f.out" 2>&1
  nm=$(grep -c "^theorem M[0-9]" "$f.lean")
  # names of false variants (not *_refuted) and of twins
  mut=$(grep -o "^theorem M[0-9][A-Za-z0-9_]*" "$f.lean" | sed 's/theorem //' | grep -v "_refuted$")
  ref=$(grep -o "^theorem M[0-9][A-Za-z0-9_]*" "$f.lean" | sed 's/theorem //' | grep "_refuted$")
  nfail=0; nmut=0; nok=0; nref=0
  for t in $mut; do
    nmut=$((nmut+1))
    if grep "'$t' depends on axioms" "$f.out" | grep -q sorryAx; then nfail=$((nfail+1)); fi
  done
  for t in $ref; do
    nref=$((nref+1))
    if grep "'$t' depends on axioms" "$f.out" | grep -q -E "$STD$" && ! grep "'$t' depends on axioms" "$f.out" | grep -q sorryAx; then nok=$((nok+1)); fi
  done
  echo "$f: false variants $nmut, failed to compile $nfail; refutation twins $nref, compiled $nok; error lines: $(grep -c error "$f.out")"
  totm=$((totm+nmut)); totr=$((totr+nref))
  { [ "$nmut" = "$nfail" ] && [ "$nref" = "$nok" ] && [ "$nmut" -gt 0 ]; } || fail=1
done
echo "total false variants: $totm (all must fail); total refutation twins: $totr (all must compile)"
echo "== 5. Mathlib check: is the transcendence of pi available? =="
if grep -rn "Transcendental" ../../../../fable_independent_2026/lean_2026/.lake/packages/mathlib/Mathlib --include=*.lean 2>/dev/null | grep -qE "π|Real\.pi|transcendental_pi"; then echo "FOUND transcendence of pi in Mathlib (revisit H7)"; else echo "not in Mathlib (only Lindemann/AnalyticalPart); H7 uses irrational_pi + an explicit hypothesis"; fi
echo "== 6. independent numerical cross-check of the stated numbers (mpmath / sympy / scipy) =="
python3 h_numeric_crosscheck.py > h_numeric_crosscheck.out 2>&1; rc=$?
echo "h_numeric_crosscheck.py: exit $rc, $(tail -1 h_numeric_crosscheck.out) checks+controls passed"; [ "$rc" = "0" ] || fail=1
if [ "$fail" = "0" ]; then echo "VERIFY: PASS"; else echo "VERIFY: FAIL"; fi
exit $fail
