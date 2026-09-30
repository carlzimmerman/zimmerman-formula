#!/usr/bin/env bash
# Build and verify the puzzle_32pi Lean certificates of wave 2-4 (this directory).
#   ./verify_bridges2.sh            builds the 9 modules in dependency order, audits every theorem, runs every MUTATE control
# Exit 0 iff: (a) every main file compiles with no error and no sorry; (b) every theorem depends only on
# [propext, Classical.choice, Quot.sound]; (c) every mutated theorem FAILS to compile; (d) every refutation twin compiles;
# (e) the independent numerical cross-check passes; (f) every false variant fails by an error in its own lines and every twin is error-free.
# Uses the toolchain of the READ-ONLY library fable_independent_2026/lean_2026 (only `lake env` is queried); writes only here.
set -u
cd "$(dirname "$0")"
STD='\[propext, Classical.choice, Quot.sound\]'
MODS="P1_wall_dS P2_sds_surface_gravity P3_record_iff P4_macdowell_mansouri P5_ext_thermo P6_dimension P7_offset_family P8_omega_lambda PuzzleChain"
fail=0
echo "== 1. main modules (build order) =="
for m in $MODS; do
  ./lean.sh -o "$m.lean" > "$m.out" 2>&1; rc=$?
  n=$(grep -c -E "depends on axioms|does not depend on any axioms" "$m.out"); e=$(grep -c "error" "$m.out")
  s=$(grep -c "sorry" "$m.out"); b=$(grep "depends on axioms" "$m.out" | grep -v -E "$STD" | wc -l | tr -d ' ')
  echo "$m: exit $rc, headline #print axioms: $n, errors: $e, sorry mentions: $s, non-standard axioms: $b"
  if [ "$rc" != "0" ] || [ "$e" != "0" ] || [ "$s" != "0" ] || [ "$b" != "0" ]; then fail=1; fi
done
echo "== 2. source scan for sorry / admit / axiom / native_decide in the main files =="
bad=$(grep -n -E "\bsorry\b|\badmit\b|^axiom |^ *axiom |native_decide" $(for m in $MODS; do echo $m.lean; done) | wc -l | tr -d ' ')
echo "matches: $bad"; [ "$bad" = "0" ] || fail=1
echo "== 3. full axiom audit: every theorem of the 9 modules =="
python3 gen_axioms2.py
./lean.sh Axioms_all2.lean > Axioms_all2.out 2>&1
want=$(grep -c "^#print axioms" Axioms_all2.lean); got=$(grep -c -E "depends on axioms|does not depend on any axioms" Axioms_all2.out)
nonstd=$(grep "depends on axioms" Axioms_all2.out | grep -v -E "$STD" | wc -l | tr -d ' ')
err=$(grep -c "error" Axioms_all2.out)
echo "theorems: $want, audited: $got, non-standard: $nonstd, errors: $err"
{ [ "$want" = "$got" ] && [ "$nonstd" = "0" ] && [ "$err" = "0" ] && [ "$want" -gt 0 ]; } || fail=1
echo "== 4. MUTATE controls (false variants must FAIL; refutation twins must COMPILE) =="
totm=0; totr=0
for m in $MODS; do
  f="${m}_MUTATE"
  ./lean.sh "$f.lean" > "$f.out" 2>&1
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
  { [ "$nmut" = "$nfail" ] && [ "$nref" = "$nok" ] && [ "$nmut" -gt 0 ] && [ "$nmut" = "$nref" ]; } || fail=1
done
echo "total false variants: $totm (all must fail); total refutation twins: $totr (all must compile)"
echo "-- own-failure check: every false variant must contain a Lean error inside its OWN lines (not inherit a sorry); every twin must be error-free --"
python3 check_mutant_errors.py; [ "$?" = "0" ] || fail=1
echo "== 5. Mathlib check: is the transcendence of pi available? =="
if grep -rn "Transcendental" ../../../../fable_independent_2026/lean_2026/.lake/packages/mathlib/Mathlib --include=*.lean 2>/dev/null | grep -qE "π|Real\.pi|transcendental_pi"; then echo "FOUND transcendence of pi in Mathlib (revisit the conditional theorems)"; else echo "not in Mathlib (only Lindemann/AnalyticalPart); the conditional theorems use irrational_pi + an explicit hypothesis Transcendental Q pi"; fi
echo "== 6. independent numerical / symbolic cross-check (mpmath / sympy / numpy) =="
python3 h2_numeric_crosscheck.py > h2_numeric_crosscheck.out 2>&1; rc=$?
echo "h2_numeric_crosscheck.py: exit $rc, $(tail -1 h2_numeric_crosscheck.out) checks+controls passed"; [ "$rc" = "0" ] || fail=1
if [ "$fail" = "0" ]; then echo "VERIFY: PASS"; else echo "VERIFY: FAIL"; fi
exit $fail
