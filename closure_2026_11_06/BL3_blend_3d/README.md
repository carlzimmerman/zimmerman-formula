# BL3: curved-3D crossing ladder for AC21's iter_6 Pi^6 blend: PASS 3D (spherical switch)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing; adoption of the repair stays with the owner.
Criteria: CRITERIA.md (5f66d85740), committed alone before the script or any number. Script bl3.py (AC22's ac22.py
with the cell measure X^d/d), outputs bl3.json / bl3.out (main), bl3_MUTATE.json / bl3_MUTATE.out (MUTATE),
per-job checkpoints parts.jsonl / bl3_MUTATE_parts.jsonl, logs run_main.txt / run_mutate.txt. Runtime about 35 min,
3 workers, nice 15, on a shared machine.

## Label

**PASS 3D (curved 3D, spherical switch r = 1, C1 C2 C3 on all five form rows).** KA reproduced, every control holds,
m6 passes, m5 fails C3 as the count says, MUTATE bites (exit 1).

## Rows (d = 3, ladder N = 800 ... 51200; numbers from bl3.json)

| row | D_inf | p | D2_inf | D3_inf | r3 | sigma_half | sigma_0 |
|---|---|---|---|---|---|---|---|
| form v3s b 0.2 | +5.4e-6 | 1.50 | +0.114 | +1.0e-2 | 2.000 | -0.023 | -0.077 |
| form v3s b 0.4 | +3.4e-7 | 1.04 | +7.1e-3 | -1.6e-3 | 2.000 | -0.010 | -0.139 |
| form v3s b 0.8 | +2.1e-8 | 1.00 | +4.4e-4 | +9.9e-4 | 2.000 | -0.005 | -0.080 |
| form AC2q b = X 0.2 | +4.6e-8 | 1.01 | +9.6e-4 | -1.1e-3 | 2.000 | -0.006 | -0.091 |
| form AC2q b = X 0.4 | +9.2e-8 | 1.01 | +1.9e-3 | -1.7e-3 | 2.000 | -0.007 | -0.105 |
| count m6 (pure Pi^6) | +7.0e-10 | 1.00 | +1.1e-5 | +3.2e-3 | 2.056 | -0.001 | -0.006 |
| **count m5 (boundary)** | +2.3e-7 | 1.01 | +6.4e-8 | **-12.68 (finite)** | 1.000 | -0.000 | -0.011 |
| control n3 | -0.138 (finite) | 0.99 | - | - | - | -0.000 | -0.001 |
| control m4 | +1.1e-9 | 1.00 | **-1.173 (finite)** | - | - | -0.000 | -0.002 |
| control v3s max | -611 (diverges) | - | - | - | - | **-0.501** | **-0.500** |
| control compatible | +1.8e-10 | 1.00 | -0.934 | - | - | -0.000 | -0.002 |

Lines and margins:
- C1: |D_inf| <= 0.1 |D_n3| = 0.0138. The largest form value is 5.4e-6.
- C2: |D2_inf| <= 0.1 * 1.173 = 0.117. The largest is 0.114, for v3s b 0.2. **This is the tightest margin.** Its
  D2 falls at exactly second order (r2 4.000), so it is converging, not stuck; it matches AC22's 2D value of 0.11.
- C3: |D3_inf| <= 0.1 * 12.68 = 1.27. The largest form value is 0.010.
- Crossing: sigma_half >= -0.15 everywhere (worst -0.023). sigma_0 > -0.35 everywhere (worst -0.139, v3s b 0.4).
- The 3D count is seen. The first velocity jump sits at order m - 2:
  - m4 holds a finite D2 jump;
  - m5 passes C1 and C2 and holds a finite D3 jump;
  - m6 and every form row have D3 going to zero.
  So m5 fails the d = 3 requirement (jumps of orders 1..3 must vanish, m > d + 2 = 5), and m6 passes it.

## Checks (verifying the pass as hard as a fail)

- **KA (d = 2).** form_v3s_b0.4, control_m4 and control_v3s rerun with d = 2 reproduce AC22's ac22.json D, D2,
  T_half and T0 at all seven rungs **bit for bit** (max relative difference 0.0, max absolute time difference 0.0).
- **m5 measures the analytic jump.** D3_inf -12.68 against -t 24 (2.7)^4 = -12.75, a ratio of 0.995, inside the
  15 % line. The same short-time formula gave m4's D2: -1.181 analytic against -1.173 in 3D and -1.175 in 2D.
- **D3 -> 0 in the form rows is not an extrapolation artefact (post-run check, not graded).** The raw D3 at
  Nmax is large: -618 for v3s b 0.2. It halves exactly per rung (r3 = 2.000). That is the leak of the order-4
  jump into a one-sided cubic fit, whose bias is L D4 / 2 with stencil L = 12 da:
  - v3s b 0.2: L D4/2 = -618.02 against a measured D3 of -618.02;
  - v3s b 0.4: -38.62 against -38.63.

  D4 itself matches the pure-Pi^6 prediction, D4 = -t A s^5 24 / b^4 with s = Pi_0'(1), to within 0.8 % in every
  form row. For m6, D4 = -t 120 (2.7)^5 = -172.2, against -172.0 measured. So the first jump is at order 4 in the
  form rows and in m6, and at order 3 in m5, as the count says.
- **MUTATE** (BL3_MUTATE=1): m5 graded through the form-row C3 line against the analytic yardstick. |D3_inf| = 12.68
  against a 1.27 line, so FAIL, exit 1. The statistic is not blind.
- v3s's max form collapses in 3D just as in 2D. sigma is -0.50 (AC16's N3b) and D diverges, so the raw switch
  stays ill-posed in 3D. The smoothed switch is not.

## Caveats on the record

- J = 0 events in the form rows drift slowly, more than in AC22's 2D run:
  - sigma_0 runs from -0.08 to -0.14, inside the -0.35 line;
  - v3s b 0.4 is -0.139 against -0.102 in 2D.

  iter_7's LEGACY two-rung ratio would fail three rows here: v3s b 0.4 1.126, v3s b 0.8 1.123 and AC2q b 0.4 1.188
  (report only, as in AC22). The J = 0 event comes after the J <= 1/2 event, in the window where ordinary stiff-side
  gas shocks form (AC20). A slow post-shock approach to zero is not excluded; it is a weak-solution matter, out of
  scope.
- **Spherical symmetry only.** The switch is the curved 3D sphere, with the 3D Jacobian and the curvature terms.
  Non-radial (l >= 1) modes are NOT tested.
- The ladder sees the jump order k = m - 2, which is set by the 1D normal profile. The threshold k > d, i.e.
  m > d + 2, is AC21's analytic map (iter_1 T3 and Lean), not something this ladder derives. What the ladder shows
  is the 3D geometry behaving as the count says, with the boundary case m = 5 failing and m = 6 passing.

## Scope

- PN charge-velocity system with a transverse switch, local in time, stiffness-only harness. AC2q enters as b = X
  with FRW background charge 2b, as in AC22.
- Shocks and soft-side folds are untouched. No data are graded and nothing is adopted.
