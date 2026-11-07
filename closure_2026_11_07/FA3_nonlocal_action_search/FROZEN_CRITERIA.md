# FA3 frozen criteria: three nonlocal / history candidates (I1, I3, I4 of IDEAS.md)

Frozen before any FA3 script or FA3 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle.
Footings graded separately, never pooled: canonical a0 9.360324825027975e-11 m/s^2, Lstar 21.7 pc; alt
1.1312035414413022e-10, 22.9 pc. Compute: one thread, nice 15, under 1 GB RSS, minutes; preemptible (no state kept).
No downloads. Every input is already committed and is used read-only.

## 0. Shared machinery and gates

- **Static gates G1-G8:** GB1 (criteria e9464bc8ce). gb1.py is exec'd read-only up to its "main" marker, as SE2 does.
  Lines, data and resampling are unchanged. A candidate is a function of GB1 features plus the history features named
  below. GB1's rule holds: a needed feature that is None makes the row NO VERDICT, and the bracket reading is reported
  but never replaces the graded cell.
- **Web gate W1:** SV5 iter_1 (criteria 247d2eaa2f). sv5_web.py's realise / delta_k / fields / project machinery is
  imported read-only (seed 5, 128^3, 2000 Mpc, ZG = 0.25 ... 50). PASS line: |r - 1| <= 3 sigma_A, with sigma_A
  read from SV5 (0.024, so 0.072).
  - A candidate changes only the phantom field W = (nu - 1) g_N on the web. V = g_N + W_cand replaces V = nu g_N in
    the same B(k) and projection.
  - F_web (OQ1/OQ2 line <= 0.005) is reported as max over ZG of the mass-weighted mean of |W_cand| / |W_law|.
- **Known answers (KA FAIL = stop and fix the loader; nothing graded):**
  - KA1: GB1 L0 class means reproduce GB1's KA1 to 1e-6 per footing (canonical X 0.467499, E 0.209888, S 0.027383,
    G0 0.358644, G1 0.195519; alt 0.434523, 0.188763, -0.000603, 0.320274, 0.158280). The L0 G1-G8 statistics
    reproduce gb1.json's L0 numbers to 1e-9.
  - KA2: with the memory off (W_cand = W_law), W1 reproduces SV5 iter_1's r from sv5_iter1.json to 1e-6 relative per
    footing (74.7 canonical / 89.4 alt). Also K1 below.
  - K1 (I1 machinery): with tau -> 0 (kernel = delta(s)), I1's r equals KA2's r to 1e-6 relative.
- **Labels per candidate:**
  - **SURVIVES**: PASS on G1-G8 and W1, both footings. It still owes field equations, causality and well-posedness.
  - **FAIL (rows)**: any FAIL on either footing, with the rows named.
  - **NO VERDICT (rows)**: no FAIL but some NO VERDICT, with the bracket reading.
  - The residue arm (G2, G3, G5) and the web arm (W1) are also reported separately, so that a candidate that closes one
    wall is visible even when it fails the other.
- **Constants:** each candidate has at most one, set by galaxies (G1 SPARC) and never per class. I3 and I4 have none.

## 1. I1: causal memory of the phantom (retarded kernel along the flow)

- **Model.** W_eff(t) = integral_0^t K(s) W_law(t - s) ds along worldlines. The graded family is
  K = e^{-s/tau}/tau (the local relaxation form n.grad W = (W_law - W)/tau), so N(t) = 1 - e^{-t/tau}. Cosmic time
  t(z) comes from the SV5 solver's background (QX3 iter3: H(z) = M.Hubble), integrated from z = 3400. t0 = t(0).
- **Hosts (generous to the candidate).** Every GB1 system is taken to have held its present W since t = 0, so
  S_host = 1 - e^{-t0/tau} and the candidate is (b = 1, F = S_host). The KiDS lens epoch is also taken at t0 (generous).
- **tau set by galaxies.** tau_gal = the largest tau for which G1 PASSES, per footing. Bisection in log10 tau over
  [1e-3, 1e3] t0, tolerance 1e-3 dex. tau_gal is the one constant.
- **Web.** At each lensing z_j in ZG, W_eff = sum over snapshots z_i >= z_j of w_ij W(z_i). Here w_ij is the kernel
  weight of the interval [t(z_{i+1}), t(z_i)], each snapshot is held piecewise-constant back to the next earlier one,
  and W(50) is held back to t = 0. Graded: r and W1 at tau_gal.
- **Kernel-free check (graded as a check, reported as the theorem's two inputs).**
  - (a) The fraction of web cells, mass-weighted, where |W(z_i)| >= |W(z_{i-1})| (earlier snapshot not smaller), for
    every adjacent ZG pair, and the mass-weighted mean cosine between W(z_i) and W(z_j).
  - (b) |W|/a0 at the KiDS K1 lens points (GB1 features). The bound uses the largest value, at the inner points that
    still need S ~ 1; the outer points give no bound.
  - Theorem reading: S_web(t) >= (min ratio) N(t) and S_host <= N(t) a0/|W_host|. It is stated for any positive kernel
    if (a) holds at >= 0.99 of the mass with cosine >= 0.99.
- **Reported only (no knob scan; nothing is chosen from it):** r and G1 at tau / t0 in {0.01, 0.1, 1, 10, 100}.
- **MUTATE (separate outputs, must bite):**
  - M1: planted growing web source W(t') = W(t_j) (t'/t_j)^4, at tau = 10 t0. W1 must PASS (|r - 1| <= 0.072) on both
    footings, which shows the grader can see a memory pass.
  - M2: Newton (F = 0). G1 must FAIL.
- **Expected (stated now): FAIL (W1).**

## 2. I3: formation-epoch a0 memory with a built z_f

- **z_f.** (1 + z_f)^3 = rho_bar / (Delta_c Omega_m rho_c0), with z_f = 0 if the right side is < 1.
  - rho_bar = 3 M_dyn / (4 pi r^3), M_dyn = v^2 r / G from GB1's feature v. For dispersion-measured systems (Coma UDGs,
    dSphs) v^2 is replaced by 3 sigma^2.
  - Omega_m = (ob + od)/h^2 and rho_c0 = 3 H0^2/(8 pi G), both from the SV5 solver's background (read-only). Graded:
    Delta_c = 18 pi^2. Reported: 5.55 (turnaround).
- **a0 history.** r_z = a0(z_f)/a0(0) from GB1's RZ_TAB (CFG689 primary values), held at 0.91 beyond z 2.33. The
  candidate is GB1's F2 with the feature rz filled per point.
  - Brackets (reported): r_z = 1.21 everywhere (68 % envelope top) and 1.12 (SV5 iter_3 native maximum).
- **Web.** The linear web has not assembled, so it keeps today's a0: W1 = KA2's r.
- **MUTATE M1 (must bite):** planted r_z = (1 + z_f)^2. The X-COP G2 mean must move by >= 0.1 dex from the graded run
  on both footings.
- **Expected (stated now): FAIL (G2-G7, W1); max shift 0.041 dex.**

## 3. I4: conserved phantom charge (ratchet + merger additivity)

- **Model.** m = mu N_eff. The charge Q^2 = G (m a0) M_b, so the candidate is g_pred = g_law(g_N; m a0) (direct
  offset Delta = log10(g_pred / g_law(g_N; a0))). In deep MOND the phantom scales as sqrt(m). mu = M_b,max / M_b (>= 1)
  and N_eff = (sum sqrt m_i)^2 / sum m_i (>= 1). m = 1 gives L0 exactly.
  - Pre-freeze change, from the adversarial review: the IDEAS draft wrote g_N + [g_law(m g_N) - m g_N]. That form
    caps the phantom at a0 for any m, so it is not the charge rule. It is replaced here before any number.
- **Features.** mu and N_eff are carried by no class, so G1-G7 are NO VERDICT. G8 takes mu = N_eff = 1 for the Sun:
  its lifetime mass loss < 1e-3 changes nothing at the gate's precision, and this is stated, not fitted.
- **Bracket fills (frozen now):**
  - X-COP and groups: N_eff in {1, 2, 4, 8, 16}, mu = 1.
  - SPARC, ellipticals and dSphs: N_eff in {1, 2}, mu = 1. KiDS: the four (early, late) N_eff combinations in
    {1, 2} x {1, 2}, mu = 1 (early types may be merger products while late types are not). G6 applies the same N_eff
    to the dSphs and to its SPARC anchor.
  - Coma UDGs: N_eff = 1, and mu in {1, median, 84th percentile, max} of 1/(1 - f_gas,gal) over SPARC galaxies whose
    M* (Upsilon_disc 0.5, Upsilon_bul 0.7) lies in the Coma UDGs' M* range (min-max of S1's rows, per footing).
    f_gas,gal = vg2/vb2 at the last kept radius (QX5's SPARC loader). This assumes all gas stripped and all stars kept.
    If fewer than 3 SPARC galaxies fall in the range, it is widened by 0.25 dex steps until >= 3, and the width is
    reported.
- **Residue-arm reading (reported):** the m that zeroes each class's mean residual (X-COP, groups f* 0.5, Coma UDGs) per
  footing, set against the brackets above.
- **Web.** The linear web is unbound and carries no charge: W1 = KA2's r.
- **MUTATE M1 (must bite):** planted N_eff = 8 for every class including SPARC. G1 must FAIL on both footings.
- **Expected (stated now): FAIL (W1); NO VERDICT (G1-G7) with brackets.**

## 4. Outputs

fa3.py writes fa3.json / fa3.out. fa3.py --mutate writes fa3_MUTATE.json / fa3_MUTATE.out. RESULT.md gives the
candidate x gate x footing table with margins read from the JSON. Any change after this freeze is disclosed in
RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
