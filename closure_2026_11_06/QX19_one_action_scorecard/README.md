# QX19: one-action scorecard, AC2q with the Pi^6 blend

Criteria: FROZEN_CRITERIA.md (d65980ffcd), committed alone before any script. Lane rules: ../SWARM_BRIEF.md.
Adopts nothing; the owner adopts. Kappa = 1/2 FITTED; not theory closed.

**The one action.** AC2q (AC7; full field equations in QX17A) with its stiffness kink [max(Sigma,0)]^2/2,
Sigma = D.P + 2X, replaced by AC21 iter_6's blend F = b^2 f(Sigma/b), with b = X. The blend is a pure Pi^6 near 0,
C4, convex, and exactly Sigma^2/2 for Sigma >= b. Column 2 is v3s with the same blend and b = rho_DE. No new
constant: b comes from the a0 law's own scale.

Scripts and outputs:
- `qx19.py` (sympy + numerics, about 2 min, one thread); outputs `qx19.json` / `qx19.out`.
- MUTATE: `QX19_MUTATE=1`, outputs `qx19_MUTATE.*`.
- Lean: `fable_independent_2026/lean_2026/QX19_scorecard.lean` has 6 theorems, 0 sorry, standard axioms only. Its
  MUTATE twin fails on exactly its 3 false claims.

## Carries: what the blend could have broken (each proved, none assumed)

| Carry | Result | How |
|---|---|---|
| C1a, c_T = c | CARRY | sympy, AC9 T1 method with F a **generic** function: no (dh)^2 term and only total-derivative h dh terms, both models |
| C1b, tensor mass | CARRY | over the whole layer q in [0,1], dv/c at 100 Hz is <= 5.8e-46 (AC2q alt), 3.4e-46 (AC2q canonical), 2.1e-46 / 1.4e-46 (v3s). The GW170817 band is ~1e-15 |
| C2, lensing slip | CARRY | sympy: dL/d(d_i Psi) = F'(Sigma) gamma P_i exactly, so the blend's change is an F/F' part plus a total divergence. Both bounded by Delta0 = 0.082, Delta1 = 0.342: <= 5.9e-15 relative (line 1e-6) |
| C3, PPN / Cassini | CARRY | AC21 statics change <= 2.0e-5 on C6P's margin 4.8e7 (Lean `cassini_margin`); the stiffness enters beyond O(GM), so PPN gamma = beta = 1 carries |
| C4, FRW health | CARRY | sympy exact: f = q^2/2 for q >= 1, F = Sigma^2/2 there, dF/db = 0. FRW sits at q = 2 (Lean `frw_point`), and any dip d >= -X stays exact (`frw_pert`), so AC7 Q1 carries unchanged |
| C5, PN sign | CARRY | f(0) = f'(0) = 0 exactly and f'' >= 0 (20001 points, AC21 `layer_nonneg`): convex, so AC21 T7 gives B >= s |
| C6, well-posedness | CARRY | f = (122363904/44610575) q^6 exactly on [0,1/2], so m = 6 > d + 2 = 5 (Lean `power_ok`); AC22 curved-2D C1/C2 PASS |
| C7, slow roots | CARRY | by C4 the linear FRW operator is unchanged, so AC23 PASS (HARMLESS, scoped) holds for the blended action |
| C8, SPARC / galaxy statics | CARRY | phantom change <= 5e-5 x max f'' (6.24) = 3.1e-4, i.e. 1.4e-4 dex < 1e-3, so QX8's exact-field PASS stands |
| C9, galaxy linear health | CARRY | layer stiffness gamma f'' lies in [0, 6.24 gamma]: positive and bounded, so no Gamma ~ k branch (AC7 Q2) |

Controls:
- MUTATE-1 (planted c P^2 (d_z h_+)^2) makes C1a FAIL.
- MUTATE-2 (near-zero power m = 4) makes C6 FAIL, and also C4, because its moments no longer close. Exit 1.

## SCORECARD: every gate, for the one action (AC2q + Pi^6 blend)

| Gate | Label for the one action | Evidence |
|---|---|---|
| SPARC / RAR, exact field | **PASS** both footings | QX8 + C8 |
| Solar System, Cassini, PPN | **PASS** | C6P, V3W W1, AC8 + C3 |
| GW speed / tensor mass | **PASS** | AC9 + C1 |
| Galaxy lensing = dynamics | **PASS** | V3W W3, AC9 + C2 |
| PN sign, all directions (HF limit) | **PASS, scoped** | AC17 + C5 |
| Well-posedness across the switch | **PASS** (3D analytic, curved 2D converged) | AC21, AC22 + C6 |
| FRW health | **PASS** | AC7 Q1 + C4 |
| Galaxy linear health | **PASS** | AC7 Q2 + C9 |
| Slow frozen roots (eps_phi <= 0.5) | **PASS (HARMLESS, scoped)**; eps_phi = 2 NO VERDICT | AC23 + C7 |
| Static limit = v3s | **PASS** | AC8 + C3/C8 |
| FG1 Upsilon-tilt row (exact field) | **FAIL canonical** (+0.170 vs 0.15), PASS alt | QX11 |
| X-ray ellipticals (G7 line) | **FAIL** at the line, both footings (+0.21 / +0.19 dex; 1.2-1.3 sigma) | QX18 |
| Clusters (X-COP, groups) | **FAIL**, no-go over the action's static terms and every extension tried | QX2, QX5, QX6, QX12, QX13 |
| CMB lensing / linear growth | **FAIL** inside the action; cold-sector window KILLED | QX3, QX7, QX10 |
| AGC 114905 | **FAIL** (EFE excluded by the census) | QX4, QX14 |
| Malin 1 | **FAIL** | QX4 |
| FN6 window source | **FAIL** (post-result control) | AC19 |
| Nonlinear fold | RUNNING | AC14 |
| Moving Sun, nonlinear | NO VERDICT as frozen, all graded numbers <= 0.25 of their lines; powered rerun RUNNING | AC15, AC24 |
| Constraint causality | RUNNING | AC18 |
| kappa | FITTED (Lean: not derivable) | KAPPA_LOGIC_2026_10_20 |
| a0(z), wide binaries | wait on data | AT2, Gaia DR4 |

Blend effect on the failing gates: none of them can be rescued by the blend. Its largest effect anywhere is
<= 1.4e-4 dex (C8), while the smallest miss is FG1's Upsilon tilt, 0.020 over its 0.15 line; the stiffness does not enter that statistic beyond C8's bound.

**Reading.** One action is consistent across every galaxy-, Solar-System-, wave- and well-posedness gate. It fails
at hot systems (X-ray ellipticals, groups, clusters), at the CMB, and on two individual UDGs. The repair that makes
it well-posed costs nothing elsewhere.
