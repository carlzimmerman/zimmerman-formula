#!/usr/bin/env bash
# reproduce_all.sh -- re-runs every script behind mnras_a0_lambda_v3.tex (v3.4) and rebuilds the PDF.
# Usage (from anywhere):  bash reproduce_all.sh          Exit status is non-zero if any script or the build fails.
# It rewrites only the paper's own products in this directory (paper_numbers.out/.json, the six figures, the PDF) and
# writes logs to reproduce_outputs/ (git-ignored).  No file outside this directory is changed: the one lane that writes a
# results file (L332) runs in scratch mirrors.  The .bbl is NOT refreshed by plain tectonic: after a bibliography change,
# regenerate it with `tectonic --keep-intermediates` in a scratch copy and copy the .bbl back (SUBMISSION_CHECKLIST.md).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
OUT="$HERE/reproduce_outputs"; mkdir -p "$OUT"
cd "$ROOT"
echo "[1/9] estimator A (Tully-Fisher intercept, Table 3)"
( cd real_research/reviews && python3 mi_btfr_intercept_kappa_door_2026.py > "$OUT/estimator_A.out" 2>&1 )
grep -h "kappa_hat = 0.465 +- 0.076" "$OUT/estimator_A.out" | head -1
echo "[2/9] earlier form of estimator B (fixed bulge mass-to-light ratio), as a check"
python3 real_research/reviews/mi_distance_free_gbar_estimator_sparc_2026.py > "$OUT/estimator_B_fixed_bulge.out" 2>&1
grep -h "kappa = 0.551" "$OUT/estimator_B_fixed_bulge.out" | head -1
echo "[3/9] H0-convention audit (paper_numbers.py also runs it, for estimator A's Hubble-flow weight)"
python3 real_research/reviews/kappa_h0_convention_audit_2026.py > "$OUT/h0_convention_audit.out" 2>&1
grep -h "OPERATIVE" "$OUT/h0_convention_audit.out" | head -2
echo "[4/9] KMOS3D replication of the RC100 pattern (L332; read by paper_numbers.py), run in a scratch mirror so that its"
echo "      results JSON outside this directory is not rewritten; the mirror's JSON must equal the committed one"
l332_mirror () {   # $1 = mirror directory, $2 = RC100 transcription to place under the lane's expected name
  rm -rf "$1"; mkdir -p "$1/real_research/data/kmos3d" "$1/real_research/dark_sector_2026"
  cp real_research/data/kmos3d/k3d_fnlsp_table_v3.fits "$1/real_research/data/kmos3d/"
  cp real_research/data/kmos3d_ubler2017.csv "$1/real_research/data/"
  cp "$2" "$1/real_research/data/rc100_nestorshachar2023_table3.csv"
  cp real_research/dark_sector_2026/L332_kmos3d_trend_replication.py real_research/dark_sector_2026/L323_rc100_framework_vs_lcdm_stress.py "$1/real_research/dark_sector_2026/"
}
MIR0="$OUT/l332_committed_mirror"; l332_mirror "$MIR0" real_research/data/rc100_nestorshachar2023_table3.csv
( cd "$MIR0" && python3 real_research/dark_sector_2026/L332_kmos3d_trend_replication.py > "$OUT/L332_kmos3d.out" 2>&1 )
grep -h "4/5 checks pass" "$OUT/L332_kmos3d.out" | head -1
cmp -s "$MIR0/real_research/dark_sector_2026/L332_kmos3d_trend_replication_results.json" real_research/dark_sector_2026/L332_kmos3d_trend_replication_results.json \
  && echo "   the mirror's results JSON is byte-identical to the committed one (which paper_numbers.py reads)" \
  || { echo "   FAIL: L332 does not reproduce its committed results JSON"; exit 1; }
echo "[5/9] L332 again in scratch mirrors with the CORRECTED (arXiv v1) and the PUBLISHED (journal; the input since v3.2) RC100 tables: the KMOS3D lines the paper uses must not move"
for TAB in CORRECTED PUBLISHED; do
  MIR="$OUT/l332_rc100_${TAB}_mirror"; l332_mirror "$MIR" "real_research/data/rc100_nestorshachar2023_table3_${TAB}.csv"
  ( cd "$MIR" && python3 real_research/dark_sector_2026/L332_kmos3d_trend_replication.py > "$OUT/L332_kmos3d_RC100_${TAB}.out" 2>&1 )
  diff <(grep -E "\[(PASS|FAIL)\] (T1|K1)|not in RC100" "$OUT/L332_kmos3d.out") <(grep -E "\[(PASS|FAIL)\] (T1|K1)|not in RC100" "$OUT/L332_kmos3d_RC100_${TAB}.out") \
    && echo "   T1, K1 and the RC100 overlap count are identical with the ${TAB} table" \
    || { echo "   FAIL: the KMOS3D lines move with the ${TAB} RC100 table"; exit 1; }
  rm -rf "$MIR"
done
rm -rf "$MIR0"
echo "[6/9] the earlier profile likelihood (Section 3.6; paper_numbers.py replicates its committed table with estimator C's code)"
python3 real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.py > "$OUT/profile_likelihood_footing.out" 2>&1
diff <(grep -A6 "THE THREE-HYPOTHESIS COMPARISON" "$OUT/profile_likelihood_footing.out") \
     <(grep -A6 "THE THREE-HYPOTHESIS COMPARISON" real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out) \
  && echo "   the hypothesis table reproduces the committed output" \
  || { echo "   FAIL: the profile likelihood does not reproduce its committed table"; exit 1; }
echo "[7/9] paper_numbers.py"
python3 "$HERE/paper_numbers.py" > "$HERE/paper_numbers.out" 2>&1 || { grep -A4 "^RESULT" "$HERE/paper_numbers.out"; echo "   FAIL: paper_numbers.py"; exit 1; }
grep -A4 "^RESULT" "$HERE/paper_numbers.out"
echo "[8/9] make_figures.py"
python3 "$HERE/make_figures.py" | tail -1
echo "[9/9] LaTeX build"
( cd "$HERE" && tectonic mnras_a0_lambda_v3.tex > "$OUT/tectonic.log" 2>&1 ) || { echo "   FAIL: tectonic build (see reproduce_outputs/tectonic.log)"; exit 1; }
echo "built mnras_a0_lambda_v3.pdf"
echo "ALL STEPS PASSED"
