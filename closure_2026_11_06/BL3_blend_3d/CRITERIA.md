# BL3 frozen criteria: curved-3D crossing ladder for AC21's iter_6 stiffness repair

Frozen before any BL3 script or number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing; adoption of
the repair stays with the owner. Lane id BL3 checked free (`ls closure_2026_11_06/`, `git log --all | grep BL3`:
no hits) before this file was written.

## What is open

- AC21 (63242d3e1e) iter_1 T3, with Lean: classical H^s theory across a transverse switch needs F a pure power
  Pi^m near 0 with m > d + 2. In d = 3 that is m > 5. The iter_6 blend is pure Pi^6 near 0 (below b/2), C^4
  blended to (gamma/2) Pi^2 above b; b = rho_DE for v3s, b = X for AC2q.
- AC22 (23b4be92bf) PASSED C1 and C2 on a curved-2D (circle) ladder to N = 51200, with the m = 4 control holding
  a finite second-derivative jump (the d = 2 count, m > 4, seen). The 3D count m > 5 is analytic only.

## Analysis (what a 3D ladder can and cannot see)

- In this harness the stiffness force is h = F'(Pi)/gamma and the label acceleration is a = -d h / d r. With
  transverse data Pi ~ c (r - 1)_+ and F ~ Pi^m, a ~ (r - 1)_+^(m-2) at short time, so the first velocity
  derivative that jumps across the switch is order k = m - 2. AC22's map of the count onto velocity statistics:
  dimension d needs the jumps of orders 1..d to vanish (k = m - 2 > d, i.e. m > d + 2). In d = 2: n3 (m = 3) jumps
  at order 1, m4 at order 2 (fails d = 2), m5 passes. In d = 3: m5 jumps at order 3 and must FAIL; m6 jumps first
  at order 4 and should PASS.
- Honest limit, stated before the run: the jump order k = m - 2 is set by the 1D normal profile, so the ladder
  sees it in any dimension. What the 3D geometry adds is (i) the 3D Jacobian J = volume ratio (spherical
  compression, stronger focusing than the circle), which drives the crossing events, and (ii) the 3D curvature
  terms in the jump statistics. The threshold k > d itself is the analytic map (AC21 T3), not something a ladder
  derives. The ladder checks that in 3D geometry m5 carries a finite third-derivative jump, m6 and the iter_6 form
  do not, and the crossing does not collapse.
- Geometry choice (frozen): curved 3D, spherically symmetric switch on the sphere r = 1 (a special case of
  axisymmetric). Non-radial (l >= 1) perturbations are NOT tested; the label is scoped to that.

## Scheme

- AC22's scheme with the Jacobian generalised to dimension d: Lagrangian labels on r in [0.25, 3.25], cell
  measure X^d / d, Pi carried per cell (charge m_i = Pi_0 * measure_0), h evaluated per cell, RK4, dt = 0.1 da,
  t_meas = 0.01, t_max = 2.0. iter_6 form from AC21 iter_6 form.json, local Horner pieces (AC22's code).
- d = 3 for the graded rows; d = 2 only for the KA.
- Ladder: N = 800, 1600, 3200, 6400, 12800, 25600, 51200.
- Data: AC22's (v3s: Pi_0 = tanh(2.5 (r-1)) + 0.1 sin(2 (r-1)); AC2q: 2b tanh(...) + 0.1 b sin(...);
  v_0 = 0.1 cos(1.3 (r-1)) + 0.05; compatible: tanh(2.5 (r-1))^3). Same data, new geometry (the 3D runs are new).

## Rows (d = 3)

- Form rows (iter_6): v3s b = 0.2, 0.4, 0.8; AC2q b = X at 0.2, 0.4.
- Count rows: m5 (h = Pi^4, F ~ Pi^5, the boundary, must fail C3); m6 (h = Pi^5, F ~ Pi^6 pure, should pass).
- Controls: n3 (h = Pi^2), m4 (h = Pi^3), v3s max form (h = Pi), compatible (v3s max form on compatible data).

## Statistics per row

- D, D2, D_inf, D2_inf, r, r2, p, T_half, T0, sigma_half, sigma_0, LEGACY: exactly AC22's definitions and code
  (one-sided fits 4 / 8 cells, uncentred, last-four-rung log-log slopes).
- D3(N) (new): jump in d^3V/dr^3 at t_meas, 6 x (difference of leading coefficients of one-sided cubic fits over
  12 cells each side, fitted in X - X_interface). D3_inf = 2 D3(Nmax) - D3(Nmax/2); r3 = |D3(Nmax/2)|/|D3(Nmax)|.
- D4(N) (report only, not graded): same with quartic fits over 16 cells.
- Analytic yardstick (short-time leading order, a = -dh/dr with Pi_0'(1) = 2.7): m5's expected
  D3 = -t_meas * 24 * 2.7^4 = -12.75; m4's expected D2 = -t_meas * 6 * 2.7^3 = -1.181 (AC22 measured -1.175).

## Lines

- C1 PASS (row): AC22's C1 line unchanged (|D_inf| <= 0.1 |D_n3(Nmax)|, p >= 0.8 or |D(Nmax)| <= 1e-6,
  sigma_half >= -0.15 or no event, sigma_0 > -0.35 or no event), yardsticks from the d = 3 controls.
- C2 PASS (row): |D2_inf| <= 0.1 |D2_inf(m4)|.
- C3 PASS (row): |D3_inf| <= 0.1 |D3_inf(m5)|.
- Controls (all must hold, else NO VERDICT):
  - n3 kink: r in [0.9, 1.1] and |D_inf| >= 0.5 |D(Nmax)|.
  - m4: passes C1; r2 in [0.8, 1.25] and |D2_inf| >= 0.5 |D2(Nmax)|.
  - m5 (the 3D boundary): passes C1 and C2; r3 in [0.8, 1.25], |D3_inf| >= 0.5 |D3(Nmax)|, and D3_inf within
    15% of the analytic -12.75 (the statistic measures what the count says).
  - v3s collapse: sigma_half <= -0.35 or sigma_0 <= -0.35 or r < 0.9.
  - compatible: |D(Nmax)| <= 0.1 |D_n3(Nmax)|.
  - m6 (pure Pi^6): passes C1, C2 and C3. If m6 fails while m5 holds, the statistic cannot resolve the count at
    this ladder: NO VERDICT, not FAIL.
- KA (d = 2, all seven rungs): rows form_v3s_b0.4, control_m4 and control_v3s rerun with d = 2 must reproduce
  AC22's ac22.json D and D2 to relative 1e-8 and T_half, T0 to absolute 1e-9. Fail -> NO VERDICT (code drift).
- MUTATE (BL3_MUTATE=1, separate outputs bl3_MUTATE.*): the m5 row graded by the form-row C3 line against the
  analytic yardstick (|D3_inf| <= 0.1 * 12.75) must FAIL (exit 1). If m5 passes, the statistic is blind: NO VERDICT.

## Labels

- PASS 3D (curved 3D, spherical switch): KA holds, every control holds, m6 passes, every form row passes C1, C2
  and C3, MUTATE bites. Scope: PN charge-velocity system, local in time, transverse data, spherical symmetry
  (non-radial modes untested), shocks and soft-side folds untouched, the dimension count itself analytic.
- FAIL 3D (row named): a form row misses a line while KA, controls and m6 hold.
- NO VERDICT (bracket stated): KA fails, a control fails, m6 fails, or MUTATE does not bite. The bracket is
  which counts the ladder did resolve (e.g. "C1/C2 seen, C3 not resolved at N <= 51200").

## Compute

- nice 15, 3 workers (machine shared; load ~13 at freeze). Each finished (row, N) job is appended to
  parts.jsonl at once; a restart skips finished jobs (preemptible; SIGTERM stops the pool and exits cleanly).
  Per-worker RSS is small (arrays of N <= 51200). Script `bl3.py`, outputs `bl3.json`, `bl3.out`; every margin
  in the README is read from the JSON.
