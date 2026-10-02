#!/usr/bin/env bash
# reproduce_all.sh -- re-runs every script behind mnras_a0_lambda_v3.tex and rebuilds the PDF.
# Usage (from anywhere):  bash reproduce_all.sh          Exit status is non-zero if any script or the build fails.
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
echo "[3/9] H0-convention audit"
python3 real_research/reviews/kappa_h0_convention_audit_2026.py > "$OUT/h0_convention_audit.out" 2>&1
grep -h "OPERATIVE" "$OUT/h0_convention_audit.out" | head -2
echo "[4/9] KMOS3D replication of the RC100 pattern (L332; read by paper_numbers.py)"
python3 real_research/dark_sector_2026/L332_kmos3d_trend_replication.py > "$OUT/L332_kmos3d.out" 2>&1
grep -h "4/5 checks pass" "$OUT/L332_kmos3d.out" | head -1
echo "[5/9] L332 again in a scratch mirror with the CORRECTED RC100 transcription: the KMOS3D lines the paper uses must not move"
MIR="$OUT/l332_rc100fix_mirror"; rm -rf "$MIR"; mkdir -p "$MIR/real_research/data/kmos3d" "$MIR/real_research/dark_sector_2026"
cp real_research/data/kmos3d/k3d_fnlsp_table_v3.fits "$MIR/real_research/data/kmos3d/"
cp real_research/data/kmos3d_ubler2017.csv "$MIR/real_research/data/"
cp real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv "$MIR/real_research/data/rc100_nestorshachar2023_table3.csv"
cp real_research/dark_sector_2026/L332_kmos3d_trend_replication.py real_research/dark_sector_2026/L323_rc100_framework_vs_lcdm_stress.py "$MIR/real_research/dark_sector_2026/"
( cd "$MIR" && python3 real_research/dark_sector_2026/L332_kmos3d_trend_replication.py > "$OUT/L332_kmos3d_RC100FIX.out" 2>&1 )
diff <(grep -E "\[(PASS|FAIL)\] (T1|K1)|not in RC100" "$OUT/L332_kmos3d.out") <(grep -E "\[(PASS|FAIL)\] (T1|K1)|not in RC100" "$OUT/L332_kmos3d_RC100FIX.out") \
  && echo "   T1, K1 and the RC100 overlap count are identical with the corrected transcription" \
  || { echo "   FAIL: the KMOS3D lines move with the corrected RC100 transcription"; exit 1; }
rm -rf "$MIR"
echo "[6/9] profile likelihood on the two footings (Section 3.8; paper_numbers.py reads the committed output)"
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
