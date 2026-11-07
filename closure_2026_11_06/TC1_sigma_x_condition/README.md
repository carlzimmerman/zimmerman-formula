# TC1: the Sigma > X condition on the QX19 one action: FIRES (frozen label)

Criteria: CRITERIA.md (4f3d3efa6b), committed alone before any script. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing; the owner adopts. Footings graded separately.

Scripts and outputs:
- `tc1_runs.py`: AC10's 12-row AC2q subset, rerun with AC2q's stiffness and with QX19's blend stiffness, ladder
  N = 2000/4000, 48 runs checkpointed in `runs/` (about 25 min on 4 workers). AC10's file is imported read-only.
- `tc1.py`: all checks and the label; writes `tc1.json` / `tc1.out` (exit 0).
- MUTATE: `TC1_MUTATE=1 python3 .../tc1.py` writes `tc1_MUTATE.json` / `tc1_MUTATE.out` and exits 1, as required.
- Lean: not compiled. This machine has no Mathlib build, and fetching one would rewrite the shared `.lake` other
  sessions use. The certificate is sympy (S1, S2), with numerical KA checks.

## What decides it

QX19's density F = b^2 f(Sigma/b), b = X, equals AC2q's [max(Sigma,0)]^2/2, together with both of its first
derivatives, on the open set O = {Sigma > X} union {Sigma < 0}. This is exact in sympy (S1): f = q^2/2 for q >= 1 and
f = 0 for q <= 0. The two actions differ only in the layer 0 < Sigma < X. Any solution that stays in O is a solution
of both, with the same history.

## Results

| Check | Result |
|---|---|
| S1 | PASS: F = Sigma^2/2 with dF/dSigma, dF/dX equal for Sigma >= X; F = 0 for Sigma <= 0; layer differs (f(1/2) - 1/8 = -0.082) |
| S2 | PASS: on TC03's on-branch, Sigma/X - 2 = 2D/r^2 exactly, which is 0 at the background. The margin keeping \|Sigma/X - 2\| <= 1/2 is eps1 = 0.125 z0 (z0 <= 1e-2) to 0.115 z0 (z0 = 0.45). Also c^2 = z/(z+(1-z)^2) = CHAIN E4, and G = 3(1-z)(1-2z+4z^2-z^3)/(1-z+z^2)^2 >= 2.33 on (0, 1/2] |
| **J3** | **HOLDS.** For eps < eps1(z0), the box B' = B n {\|Sigma/X - 2\| <= 1/2} is a valid bootstrap box (FORMATION s4: T0(B') > 0; s5: T_k <= C_eps/k < T0(B')). So TC03's catastrophe holds verbatim for A2. At physical z0 ~ 1e-17, TC03's own family needs dr/r below ~1e-18 |
| KA1 | PASS: TC03 pulse slope ratio 8.00000000 |
| KA2 | PASS: 81 comparison rows; blow-up at <= 0.569 of the bound 2/(kappa Q0); cone Q - P non-decreasing |
| KA3 | PASS: AC2q rerun = AC10's stored fold times on 24 rung pairs, max deviation 0.0 |
| P0 / P1 | PASS: homogeneous Sigma/X = 2 state with Q0 = 0 gives IN, NO FIRE; with cone data gives IN, FIRES at 0.105 <= 0.2 |
| MUTATE (b = 4X) | bites: S1_row fails and all 4 clock-only rows read LAYER; exit 1 |

**N1, physical planar rows.** A cold clock stream crosses a baryon sheet (X14 F2 / AC10 setup; radii 11 and 156 kpc;
w 68.75 km/s). QX19 fold = AC2q fold on every row.

| Row (both footings) | Interior Sigma/X before the fold | Region | QX19 vs AC2q fold | Fold time |
|---|---|---|---|---|
| clock-only | 2 to 10.5 | IN | identical (0 to 2e-13) | 9.0-9.6 Myr (11 kpc), 183-200 Myr (156 kpc) |
| phantom | 183 to 2.2e5 | IN | <= 8e-11 | same |
| soft | -2.5e5 to -179 | OFF-SIDE (Sigma < 0, also A2 = A1) | <= 7.8e-5 | same; canonical 11 kpc ladder 1.16e-3 (not converged) |

- All 8 IN rows are converged folds (ladder <= 4.0e-4). Each fold comes in at least 69 times below the age of
  13.8 Gyr.
- X is not evolved by the PN code. Its shift is bounded by (v w/c)^2 <= 1.5e-7, so the region margin cannot close.
- In the soft rows, the edge taper crosses the layer in 0.09-0.3 % of the edge cell-samples. The graded interior
  cells never do.

**N2, static census (reported).** Spherical QUMOND phantom density gives Sigma/X = 2 + rho_ph/rho_DE.
- SPARC, 175 galaxies, 3389 radii: 100 % IN, both footings. Minimum Sigma/X is 992 (canonical) and 748 (alt).
- X-COP, 12 clusters (5 gas-only: no stellar file on disk): 100 % IN. Minimum is 45 and 35.
- No static radius sits in the layer. A time-independent regular solution cannot have a finite-time catastrophe.

**Other configurations.**
- FRW: Sigma/X = 2 and Q = 0, so it does not fire.
- Linear growth: in the region for dips d >= -X. Being linear, it does not fire.
- Moving Sun: NO VERDICT. The record has no nonlinear verdict yet (AC15/AC24), and it is not graded here.

## Label: FIRES

- **Region named.** Planar cold-clock streams crossing a baryon sheet at galaxy radii, in clock-only and phantom
  interiors with Sigma/X >= 2. The clock congruence folds (v' unbounded, v and X finite) within 9 Myr to 200 Myr, on
  both footings. The QX19 action folds at the same time as AC2q, because the state never enters the blend layer.
- **QX19 rows lost:** none of the 10 PASS rows. Under the frozen reading, none of them asserts global regularity.
  - The well-posedness row is re-scoped to local-in-time. Classical solutions of the one action break down in finite
    time on physical data.
  - The scorecard's "Nonlinear fold" row (RUNNING) now reads: folds fire, same as AC2q / v3s.
- **The CONDITIONAL is removed.** The QX19 PASS rows hold unconditionally as the static, linear and local statements
  they are.
- **Open.** What happens after the fold: postbreak continuation (CHAIN N8) and shock physics. So does whether the
  static galaxy states are reached through folding collapse. These are not graded here.

Reading (post-result, not a label): the catastrophe that matters physically is AC10's fold, not TC03's constructed
family. TC03's family needs dr/r ~ z0 ~ 1e-17. Physical perturbations sit at Sigma/X ~ 1e2-1e5 (or Sigma < 0), far
from the layer. So the blend never acts on them, and it can neither cause nor cure the fold.

Side note for another lane: qx19.py evaluates its blend with expanded high-degree rationals in float. Near q = 1 this
gives about 1e-4 cancellation error (f'(1) prints 1.000095; exact 1). TC1 evaluates in a shifted Horner form. QX19's
C-check margins are much larger than 1e-4, but the numbers there are float-limited.
