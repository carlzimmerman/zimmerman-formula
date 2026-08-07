# E01 — Fix the OOM that killed the local run
COST: S | script: patch in place, plus `mi_oom_fix_check_2026.py`

> ENGINEERING / DATA task. Import `TOOLS/mi_constants.py` — never retype a constant.
> `../02_HOUSE_RULES.md` and `../03_NUMERIC_HAZARDS.md` apply.

## The problem
The qwen run died out of memory. Cause: `03_kubo_program/` builds **dense N×N matrices** at N up to 4096
(~134 MB each in float64) and holds several at once, then iterates Picard 80 times over them.

## Do
1. Confirm the diagnosis: find the allocations and report peak memory as a function of N.
2. Replace the iteration with the **exact triangular solve**. The Volterra operator is unit lower-triangular,
   so `det(I − q²K) = 1` for every coupling and the resolvent always exists — no iteration is needed at all.
   `scipy.linalg.solve_triangular` on a banded/sparse form, or forward substitution row by row.
3. Report the new peak memory and the speedup, and verify the answer matches the old converged rows.
4. **Watch for overflow:** forward substitution at N = 4096 overflows to inf for large q². Work in log space
   or cap the range, and say which.

## Settles if
Same answers, order-of-magnitude less memory, and the previously non-converged rows now solve exactly — which
is also what showed those rows were the artefact.
