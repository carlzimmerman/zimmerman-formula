#!/usr/bin/env bash
# reproduce_all.sh -- re-runs every script behind mnras_a0_lambda_v2.tex and rebuilds the PDF.
# Usage (from anywhere):  bash reproduce_all.sh          Exit status is non-zero if any script or the build fails.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
OUT="$HERE/reproduce_outputs"; mkdir -p "$OUT"
cd "$ROOT"
echo "[1/6] estimator A (Tully-Fisher intercept, Table 3)"
( cd real_research/reviews && python3 mi_btfr_intercept_kappa_door_2026.py > "$OUT/estimator_A.out" 2>&1 )
grep -h "kappa_hat = 0.465 +- 0.076" "$OUT/estimator_A.out" | head -1
echo "[2/6] earlier form of estimator B (fixed bulge mass-to-light ratio), as a check"
python3 real_research/reviews/mi_distance_free_gbar_estimator_sparc_2026.py > "$OUT/estimator_B_fixed_bulge.out" 2>&1
grep -h "kappa = 0.551" "$OUT/estimator_B_fixed_bulge.out" | head -1
echo "[3/6] H0-convention audit"
python3 real_research/reviews/kappa_h0_convention_audit_2026.py > "$OUT/h0_convention_audit.out" 2>&1
grep -h "OPERATIVE" "$OUT/h0_convention_audit.out" | head -2
echo "[4/6] paper_numbers.py"
python3 "$HERE/paper_numbers.py" > "$HERE/paper_numbers.out" 2>&1; tail -1 "$HERE/paper_numbers.out"
echo "[5/6] make_figures.py"
python3 "$HERE/make_figures.py" | tail -1
echo "[6/6] LaTeX build"
( cd "$HERE" && tectonic mnras_a0_lambda_v2.tex > "$OUT/tectonic.log" 2>&1 ) && echo "built $HERE/mnras_a0_lambda_v2.pdf"
echo "ALL STEPS PASSED"
