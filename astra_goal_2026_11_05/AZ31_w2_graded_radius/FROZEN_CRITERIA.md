# AZ31 — W2 at its graded radius

Tier 1 lane 1. New criteria, not an amendment of V3X. Known V3X results have
been read: this is not a blind validation. Freeze before new solver outputs.
Kappa = 1/2 FITTED; not theory closed. Both footings separate:
9.3603e-11 and 1.1312e-10 m/s^2. L_star=24 pc is inherited and fitted.

## Mathematical and numerical contract

Use V3X's exact C6 Newton equations and existing lower-memory solver read-only.
Method A: shift 1e-12 on the row-scaled w block; three polish steps. Grid ladder
(40,64),(50,80),(60,96),(70,112), with (30,48) for the known-answer check.
Only Q2 at 100 Saturn radii is graded. Values at 1 and 10 radii are diagnostics.

K1: at (30,48) and (40,64), reproduce V3W's recorded 100-radius Q2 to relative
1e-6. This retains the original tolerance at the original graded observable,
and removes ungraded near-origin comparisons from this new lane only.
K2: independent Method B/COLAMD at (30,48),(40,64) agrees with Method A at
the graded radius to 1e-6. No known oversized B/MMD or (50,80) probe.
K3: at (70,112), shift 1e-10 vs 1e-12 changes graded Q2 by <=1e-6.

All production rungs: residual <1e-9; last two absolute differences shrink;
order-2 Richardson extrapolation from 60/70 differs from finest by <0.02;
observed order on 50/60/70 is in [1.5,2.5]; extrapolated Q2 and Route F have
the same sign and differ by <0.05 relative. These are the prior V3X numerical
error lines, not retuned observational bounds. RSS must remain below 1e9 bytes;
use the inherited child watchdog at 0.85e9 bytes.

Physical diagnostic: graded Q2 <=9e-27 s^-2 (V3X/C6P's carried convention).
This does not rerun the entire Cassini field grid or regrade other V3W items.

MUTATE: remove stiffness (L_star=0 in the solve), retain the 24 pc Route F
reference, and run the same four production rungs on each footing. It must
fail an actual physical/reference check, not a hard-coded mutation flag.
Mutation convergence and residuals are reported even if the physical test
fails. Separate output directories; no historical result overwrites.

PASS requires all primary numerical/known-answer checks. A converged
physical/reference disagreement is FAIL. Missing solves, excess memory,
unresolved precision/convergence give UNDECIDED or NOT EVALUABLE with cause.
Read final margins from new JSON. The old V3X label remains unchanged.

## Execution and provenance

Single-threaded, minutes per rung, checkpoint atomically after each rung.
Resume only from checkpoints whose source hashes and mode agree. SIGTERM
requests a safe yield; interruption during a child may require repeating that
one rung. No new grids are chosen based on outcomes. This is a light
sub-1GB calculation; heavier work is deferred to the queue.
Store exact inputs/hashes, software versions, elapsed time and memory with
each rung. No new downloads or inherited passing labels as computation.
