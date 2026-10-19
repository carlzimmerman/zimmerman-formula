# RESULT: nonradial stability and MeV continuation of the diffuse mixed condensate

Checkpoint **CL-2F-2026-10-19-01** (parent EKG-2026-10-19-C). PLAN.md was committed alone
before any script (commit e3fc772b5). The action is unchanged throughout. The theory is
not closed, and nothing here closes it.

## Answer

**YES, within a stated scope.** Here "stable" means classical *linear* stability, and the
claim rests on three pieces:
- the **axial** sector is stable in **exact GR**;
- the **polar** sector is stable at **leading (Newtonian-gravity) order**, with a measured
  GR correction of order 1e-4;
- the stability is followed along a continuation in the action's one free parameter, at a
  fixed central amplitude.

What holds within that scope:
- **Existing benchmark (Gamma = 1e-8).** The diffuse mixed state is stable in every l >= 1
  sector. The only exceptions are the three exact translation zero modes at l = 1, and
  those are symmetries, not instabilities.
- **Continuation.** The branch neither folds nor loses stability from Gamma = 1e-8 down to
  5.6e-12 (full-GR equilibria) and 1e-12 (stability spectra). Below that it runs smoothly
  into the Gamma -> 0 Thomas-Fermi (TF) limit, whose hydrodynamic spectrum is positive.
- **Endpoint.** At Gamma_phys = 7.61e-43 the action is exactly the MeV benchmark. Using the
  TF interior plus a boundary layer whose thickness scales as Gamma^(1/3), the state is a
  condensate star of about **3.45 M_sun** with radius **R ≈ 1.06e8 m** and compactness
  **C99 = 5.05e-5**. Its pulsation periods are 1 to 4 minutes.

What this does **not** establish:
- a full-GR polar (l >= 2) spectrum;
- a rigorous interval enclosure of any spectrum;
- nonlinear or quantum/many-body stability;
- formation, abundance or lifetime;
- that the endpoint is "the same charge". The branch label is the central amplitude, so
  the charge scales as Gamma^(-3/2).

## 1. Setup (as declared)

- Units are m = lambda_tot = 1, with u* = 0.02 and r_lambda = 2 held fixed.
- The one varied parameter is Gamma = G m^2/lambda_tot.
- Recomputed from sigma_0/m = 0.3 cm^2/g:
  - lambda_tot = 0.0088129203;
  - g = 2168.000 eV;
  - g_hat = 0.0230940108;
  - **Gamma_phys = 7.6125e-43** (4 pi Gamma = 9.566e-42).
  These match the brief.
- Branch label: central f_c = 0.009888264649 (units m/sqrt(lambda_tot)). In the TF limit
  this is x_c = 0.4, central Omega_c = 1.0000533.

## 2. Nonradial stability at the benchmark (Gamma = 1e-8)

### 2.1 Axial sector — exact GR (`axial_master.py`, `results/axial/axial.json`)

Scalar perturbations are all polar. For complex scalars, an axial metric perturbation h
gives delta L = 0 and L = p_t, so exactly delta T_mn = -p_t h_mn.

sympy linearizes the Einstein tensor in Regge–Wheeler gauge (l = 2, 3, explicit
Legendre) and eliminates h0 using the (theta, phi) equation. With
Z = e^(nu-lam) h1/r and the tortoise coordinate it finds:

**V_ax = e^(2nu) [ l(l+1)/r^2 − 6Gm/r^3 + 4piG(rho − p_r) ]**

- p_t cancels identically.
- The vacuum limit reproduces Regge–Wheeler (difference 0).
- The Z' coefficient check is 0.
- Angular separation holds.

For this action rho − p_r = 2V >= 0 (positive-square potential), so
V_ax >= e^(2nu)(l(l+1) − 6Gm/r)/r^2. The Andreasson bound 2Gm/r <= 48/49 is already
verified in the parent packet. Together these give **V_ax > 0 for every l >= 2 and every
regular static solution of this action, at any compactness**.

With a positive potential, the conserved wave energy (outgoing radiative boundary
condition) excludes growing axial modes. On the benchmark profile:

| l | min r^2 V_ax |
|---|---|
| 2 | 5.99878 |
| 3 | 11.99756 |
| 10 | 109.9777 |

The maximum deviation from the flat value l(l+1)/r^2 is 2.0e-4.

For l = 1, the axial sector contains only the stationary rotation/gauge mode, and scalar
matter has no source for it.

### 2.2 Polar sector — leading-order NR-GPP model (labelled approximation)

`nr_gpp.py` implements the nonrelativistic two-component Gross–Pitaevskii–Poisson
reduction of the same action. The linearized Newtonian potential is solved in every
l-sector (no Cowling approximation).

**Proposition (proved here; uses one standard external theorem).** Assume a stationary
NR-GPP state with mu < 0 satisfies hypothesis H1: f, x > 0 and f', x' < 0, with
exponential tails. Then for all l >= 1:
- L-^(l) >= c_l > 0;
- L+^(1) >= 0, and its kernel is exactly the translations;
- L+^(l) >= c'_l > 0 for l >= 2.

So the conserved quadratic energy is coercive on every l >= 2 sector, and positive on
l = 1 apart from translations. No growing mode exists, for all l at once.

Proof:
- **(a) Cooperative structure.** L± = −Δ_l + V±(r) − K_l. The off-diagonal entries of V±
  are −2g f < 0. The gravity term K_l = (Gamma/2) D C_l D has nonnegative kernel, with
  C_l = 4pi(−Δ_l)^(-1) and kernel 4pi r_<^l / ((2l+1) r_>^(l+1)). Hence e^(−tL) is
  positivity-improving (Trotter product with a Metzler matrix exponential, Dyson series
  for K). Irreducibility holds because f > 0.
- **(b) Essential spectrum (Weyl).** It is [2|mu|, ∞), because V± tends to
  diag(−2mu, Delta − 8mu) and K_l is compact.
- **(c) Perron–Frobenius.** Reed–Simon IV, Thm XIII.44, external and standard: the
  ground state below the essential spectrum is simple with a positive eigenvector, so any
  one-signed eigenvector is the ground state.
- **(d) Kernels.** L-^(0)(f, 2x) = 0 (U(1) phase), and L+^(1)(f', x') = 0 (translation).
  Both vectors are one-signed.
- **(e) Monotonicity in l.** L-^(l) − L-^(0) = l(l+1)/r^2 > 0. Also
  L+^(l) − L+^(1) = (l(l+1) − 2)/r^2 + (K_1 − K_l), and K_1 − K_l >= 0 because
  −Δ_1 <= −Δ_l implies (−Δ_1)^(-1) >= (−Δ_l)^(-1).

Strict positivity with a gap follows from (b). The radial l = 0 sector is NOT covered by
this proof: L+^(0) has one negative direction. That sector is tested separately below
with the charge constraint and the Vakhitov–Kolokolov criterion.

**Numerics** (`results/partN/`, `summary_partN.json`):
- Six discretizations, all passing every declared acceptance criterion C1–C5:
  - D1 second-order finite differences, h = 8, 5.33, 4 at R_box = 8000, plus
    R_box = 10000;
  - D2 sine-DVR (spectral), N = 1000, 1500.
- Sigma is in units of m.
- s^2 = sigma^2/(4 pi Gamma q_c), with q_c = 2(f_c^2 + 4x_c^2) = 2.252e-4.

| l | lowest S+ (energy) | lowest S- | sigma_1, sigma_2 | s^2_1 | GR-transfer margin |
|---|---|---|---|---|---|
| 0 | 4.837e-6 at fixed charge (one negative unconstrained: VK n = 1) | 4.957e-7 with phase quotiented | 2.30417e-6, 5.2369e-6 | 0.1876 | 18 |
| 1 | 1.1e-13 (translation); next 7.184e-6 | 1.692e-7 | translation \|sigma\| < 1e-9; then 3.8258e-6 | 0.5172 | 50 |
| 2 | 4.515e-6 | 3.914e-7 | 1.90169e-6, 4.8627e-6 | 0.1278 | 12 |
| 3 | 5.093e-6 | 6.657e-7 | 2.6224e-6 | 0.2430 | 24 |
| 4 | 5.429e-6 | 9.906e-7 | 3.1751e-6 | 0.3562 | 35 |
| 8 | 6.724e-6 | 2.765e-6 | 5.1139e-6 | 0.9241 | 90 |
| 16 | 1.0903e-5 | 8.335e-6 | 1.00023e-5 | 3.535 | 343 |

Checks behind the table:
- **Signs (C1).** Identical in every discretization and domain.
- **D1 vs D2 frequencies (C2).** Agree to ≤ 4.3e-6 (l ≤ 8) and ≤ 1.8e-5 (l = 16).
- **Translation mode (C3).** Eigenvalue ratio ≤ 6.2e-8 (FD) and ≤ 1.2e-11 (DVR). Overlap
  with (f', x') ≥ 0.9999999998.
- **Stationarity and phase kernel (C4).** Stationarity residual ≤ 7.4e-13. Phase-kernel
  residual ~1e-16 (exact discrete Ward identity).
- **H1 (C5).** Holds on every background.
- **Monotonicity in l.** The lowest S+ and S- increase with l, as the proof requires.

**Continuum and tail:**
- All listed modes lie below the Phi threshold 4.809e-5 (the X threshold is 4.96e-4), so
  they are genuine discrete modes.
- A negative L+ direction would need kinetic wavenumber below 0.0192 m. The grids resolve
  0.39–0.79 m.
- The edge and tail are resolved smooth profiles, not a TF surface. Moving the box from
  8000 to 10000 changes nothing at the quoted precision.
- **Radial Vakhitov–Kolokolov check:** n(L+^(0)) = 1 and dN/dmu = −4.03e11 < 0. This
  agrees with the positive constrained eigenvalue.

**GR calibration.** The NR-GPP lowest radial frequency is 2.30417e-6. The independent
full-GR constrained ADM value (run_018) is 2.303833e-6. The relative difference is
+1.41e-4 to +1.48e-4 across the six discretizations, against a declared bar of 1e-2. For
comparison, eps = max(1 − omega, 2GM/r, 1 − alpha_c) = 1.03e-4.

**Instability sign check (compact control, G = 8.5e-5, h_c = 0.02).** NR-GPP
reproduces the known instability:

| run | constrained S+ min | sigma^2 | gamma |
|---|---|---|---|
| R600, N1500 | −6.25e-9 | −1.258e-12 | 1.12e-6 |
| R600, N2399 | −5.80e-9 | −1.294e-12 | 1.14e-6 |
| R450, N1500 | −5.93e-9 | −1.218e-12 | 1.10e-6 |

- The full-GR growth rate is 1.411e-6, so the NR rate is 0.78–0.81 of it. PASS (the
  declared bar was within a factor 2).
- The VK check agrees: dN/dmu = +1.9e3 > 0.
- This control is a poor NR target: at fixed h_c its NR f_c is 21% off the GR value, and
  its s^2 ≈ −3.8e-7 is about 5 orders of magnitude closer to zero than the diffuse margins.

**GR transfer (argument with stated limits, not a theorem):**
- Every non-symmetry NR sigma^2 for l >= 1 exceeds the declared threshold
  100·eps·(4 pi Gamma q_c) by factors of 12–343.
- l = 1 translations and boosts are exact symmetries of the asymptotically flat system.
- For l >= 2, GR adds a gravitational-wave continuum. It carries positive canonical
  energy and no U(1) charge, so radiation can only lower delta^2(H − omega Q). With a
  positive matter Hessian it damps; it cannot drive growth. The background is
  non-rotating with no negative-energy mode, so no CFS-type route exists.
- The quadrupole damping quality factor is roughly C^(-5/2) ~ 1e10.
- What is not here: a full-GR polar QNM calculation.

## 3. Continuation toward Gamma_phys at fixed f_c

### 3.1 Full-GR equilibria (C1)

Source: `gr_continue.py`, `results/gr/continue_*.json`. This is an independent
re-implementation that reproduces the saved benchmark at step 0:

- omega = 0.9999519202156224, against the saved .156226 (difference 2e-16);
- M_ADM = 2.266852e7 and Q = 2.266904e7, within 1.3e-12 of the saved values;
- R99 within 9.5e-8 of the saved value.

| Gamma | 1 − omega | v = Gamma^1.5 M_ADM | z99 = sqrt(Gamma) R99 | C99 | nodes |
|---|---|---|---|---|---|
| 1e-8 | 4.80798e-5 | 2.266852e-5 | 0.463136 | 4.89457e-5 | 10001 |
| 1e-9 | 4.80029e-5 | 2.255256e-5 | 0.448803 | 5.02504e-5 | 12299 |
| 1e-10 | 4.79985e-5 | 2.254099e-5 | 0.446477 | 5.04864e-5 | 19912 |
| 1e-11 | 4.79983e-5 | 2.253983e-5 | 0.446257 | 5.05087e-5 | 31721 |
| 5.6234e-12 | 4.79983e-5 | 2.253977e-5 | 0.446247 | 5.05097e-5 | 38896 |
| **TF limit (C2)** | **4.79984e-5** | **2.253970e-5** | **0.446234** | **5.05109e-5** | TOV |

Steps at 3.16e-9, 3.16e-10, 3.16e-11 and 1.78e-11 are in the JSON.

Every accepted step passes its checks:
- collocation rms residual ≤ 5.0e-7;
- independent 4th-order finite-difference r-form KG residual ≤ 2.8e-6;
- Hamiltonian-constraint residual ≤ 1e-10;
- Simpson mass/charge quadratures agree to ≤ 2.1e-13;
- profiles are monotone;
- M_ADM/(mQ) = 0.99997688 throughout.

How the observables approach the TF limit:
- The deviations of M, Q and z99 approach Gamma^1.00 scaling (quantum-pressure order).
  At Gamma_phys they would be ≲ 1e-36 relative.
- 1 − omega converges to the TF value down to the ~6e-7 relative precision floor of the
  BVP tolerance.

Edge boundary layer:
- Measured at a level scaled with the layer density, z(f^2 = 0.0464·Gamma^(1/3) f_c^2)
  − z_s, the edge length scales with **exponent 0.3338**. Local exponents run
  0.337 → 0.3330. This is the Airy/Painlevé-II prediction of 1/3 (pass band 0.25–0.45).
- Fixed-level crossings give 0.41 and 0.37. They drift, as expected, because the layer's
  own density scale is ~Gamma^(1/3).

The continuation stopped at Gamma = 3.16e-12. There the rms residual was 1.24e-6 at the
60k-node memory cap. This is **methodological** (the 1/Gamma singular perturbation), not
a fold: every observable is monotone and converging, and the TF structure exists at
Gamma = 0.

### 3.2 Stability along the path (C3) and the Gamma = 0 anchor (C4)

Sources: NR-GPP `results/partC3/summary_C3.json`, and the independent hydrodynamic
eigenproblem of the TF star in `tf_limit.py`.

| s^2 | 1e-8 | 1e-9 | 1e-10 | 1e-11 | 1e-12 | **hydro, Gamma = 0** |
|---|---|---|---|---|---|---|
| l=0 fundamental | 0.18760 | 0.19081 | 0.19126 | 0.19131 | 0.19132 | **0.19132** |
| l=1 (first after translation) | 0.51718 | 0.52951 | 0.53145 | 0.53173 | 0.53176 | **0.53177** |
| l=2 f-mode | 0.12779 | 0.12632 | 0.12611 | 0.12609 | 0.12609 | **0.12609** |
| l=3 | 0.24300 | 0.23544 | 0.23429 | 0.23413 | 0.23411 | **0.23411** |
| l=4 | 0.35622 | 0.33505 | 0.33162 | 0.33113 | 0.33106 | **0.33106** |

- Second modes are in the JSON.
- At every Gamma:
  - all monitored s^2 > 0;
  - H1 holds;
  - n(L+^(0)) = 1 and dN/dmu < 0;
  - two-resolution agreement ≤ 2.2e-5, against the declared bar of 1e-2.
- Deviations from the anchor shrink as about Gamma^0.85 and reach 2e-6 to 2e-5 at
  Gamma = 1e-12, which is the discretization floor there.
- The hydro anchor converges under grid refinement (400/800/1600 cells). Its l = 1
  translation goes to 0 as h^2.

**Verdict on the path: it survives.** There is no sign change and no fold, and the
spectrum converges to a positive Gamma = 0 limit. The NR transfer margin is set by eps,
and eps stays at about 1.03e-4 along the branch, since C and 1 − omega are
Gamma-independent at leading order.

One soft direction to note: the lowest charge-constrained **energy** eigenvalue of
L+^(0) falls as about Gamma^0.33 (4.8e-6 → 2.6e-7 from 1e-8 to 1e-12):
- This is a surface-layer mode with eigenvalue ~1/d^2 and d ∝ Gamma^(-1/6).
- It stays positive at every computed Gamma.
- It is a boundary-layer scale, not a trend toward a sign change; the frequencies above
  converge.
- Its GR correction is O(eps) of the same small scale (argument only, not computed).

### 3.3 Endpoint at Gamma_phys = 7.6125e-43 (`endpoint.py`, `results/endpoint.json`)

At leading TF order with the stated corrections:

| quantity | value |
|---|---|
| R_surface | 1.062e8 m |
| R99 | 1.009e8 m |
| M_ADM | 3.85e60 MeV = 6.86e30 kg = 3.45 M_sun |
| Q | 3.85e60 charge units |
| C99 | 5.051e-5 |
| 1 − omega | 4.80e-5 |
| central Phi amplitude | 0.105 MeV |
| edge layer thickness | ~7e-5 m (layer-scaled measure) |
| l=0 fundamental period | 204 s |
| l=2 f-mode period | 251 s |
| l=1 first-mode period | 122 s |
| l=3 period | 184 s |
| l=4 period | 155 s |

Fitted gradient corrections at the endpoint are ≲ 1e-14 relative. The largest, 1e-14,
comes from a poorly determined last-pair exponent of a second mode.

This "same intensive state" is a stellar-mass object. By contrast, a
**fixed-charge** continuation at Q_hat = 2.27e7 would leave the TF regime: its binding
would be ~(Gamma Q_hat)^2 ~ 3e-70 of the rest energy, at radius ~1e22 m. That object is
not analyzed, and no verdict is given for it.

## 4. Separate status, as the brief requested

| item | status |
|---|---|
| Equilibrium existence | full-field numerical down to 5.6e-12; TF limit plus a verified Gamma^(1/3) edge scaling beyond that. Not a full-field certificate at Gamma_phys. |
| Radial continuum | NR-GPP high-resolution spectra plus a high-k coercivity bound; GR-calibrated to 1.5e-4. No rigorous enclosure. |
| Angular (l >= 1) | axial: exact GR, analytic positivity for any compactness; polar: Newtonian-order theorem plus numerics plus O(eps) transfer argument. |
| Nonlinear, quantum, formation, lifetime, abundance | not addressed. |

## 5. Deviations from PLAN and failures (disclosed)

1. **First GR launch.** It failed because the benchmark NPZ has no collocation arrays. The
   seed loader was fixed and the run relaunched. That log was discarded because it held a
   home path.
2. **One run exceeded the 2 GB cap.** The run at Gamma = 1e-11 with a 300k-node cap peaked
   at **4.3 GB RSS for about 20 s** (`results/gr_failed_300k/`). The 1024³ job was
   unaffected: it was still running afterwards and swap use was 29 MB. All later runs were
   capped at 60k nodes, with peaks ≤ 1.55 GB.
3. **Collocation tolerance below 3.16e-11.** The tolerance was loosened from 1e-7 to 5e-7
   (declared acceptance ≤ 1e-6), and log-midpoint steps were added. The tol-1e-7 attempt at
   1.78e-11 is kept in `results/gr_failed_tol1e-7/`.
4. **Newton iteration count.** Newton for G1e-8_N1500 ran to maxit = 60 at rel 1.6e-13, the
   roundoff floor above the 1e-13 target. This is accepted under C4 (≤ 1e-10).
5. **Ill-conditioning warnings at 1e-12.** The Gamma = 1e-12 Newton solves emitted
   LinAlgWarning (rcond ~1e-17, a scaling issue). The final residuals were checked directly
   at ≤ 1e-15.
6. **Output directory renamed.** Outputs were written to `out/` and renamed to `results/`
   for commit, because `out/` is gitignored. The summaries were regenerated from
   `results/`.

## 6. Files

- Scripts: `common.py`, `nr_gpp.py`, `axial_master.py`, `gr_continue.py`, `tf_limit.py`,
  `summarize_partN.py`, `summarize_C3.py`, `endpoint.py`.
- Drivers: `run.sh`, `partN.sh`, `seq2.sh`–`seq5.sh`, `partC3.sh`.
- Outputs are under `results/`, and `MANIFEST.json` gives SHA256 for every committed file.
- Newton iteration logs (`*.log`) are gitignored by repo convention and not committed;
  final residuals are in each run JSON.
- Runs used 1 thread at nice 19.
