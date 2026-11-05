# Reproduce the exact checks

Requires Python3 and SymPy1.13.1 (recorded execution used Python3.13.9).
Run from the repository root; use new output paths to retain old evidence:

    python3 astra_goal_2026_11_05/AZ40_canonical_coupling/constraint_continuation/verify.py --mode main --out /tmp/az40-main.json
    python3 astra_goal_2026_11_05/AZ40_canonical_coupling/constraint_continuation/verify.py --mode clock_sign --out /tmp/az40-clock-sign.json
    python3 astra_goal_2026_11_05/AZ40_canonical_coupling/constraint_continuation/verify.py --mode drop_gradient --out /tmp/az40-drop-gradient.json

Expected process exits0,1,1 and check counts36/36,32/36,34/36.
The existing evidence/*/manifest.json files record the bounded execution
arguments, dependency versions, input/output hashes, repository checkpoint,
wall times and exit statuses. The two failed statuses are deliberate mutations.
No observational data, fitted parameters, random seeds or tolerance scan is used.

RESULT.md and SWITCHED_CLOCK.md contain the uniform mathematical arguments.
The code corroborates the listed symbolic identities, not every theorem in the
prose: finite-Galerkin convexity and the zero-current caustic corollary are
explicit analytic proofs, with author self-review in REVIEW.md.
