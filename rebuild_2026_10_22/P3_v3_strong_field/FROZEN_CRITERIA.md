# P3_v3_strong_field: black holes, ringdown, neutron stars and strong coupling for v3. FROZEN CRITERIA

Written and committed before the lane script exists. Rules: `rebuild_2026_10_22/BRIEF.md`,
`covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. kappa = 1/2 is FITTED.
Footings canonical a0 = 9.36e-11 m/s^2 and alt a0 = 1.13e-10 m/s^2, never pooled. No dark-matter particle. Never
"theory closed"; nothing here says the data favour the framework. Tile verdict words: PASS / FAIL / OPEN.

## 0. What was read before freezing, and the not-blind statement

Read: `covariant_push_2026_10_22/THEORY_V3_DRAFT.md`; C4, C5, C8 READMEs and the C5 script (local quadratic matrix,
H8); I1 README; `explainers/make_status_board.py` (stale tiles: "Black holes (EHT, LIGO ringdown)" CFG318/319,
"Strong coupling" XC1/XC3, "Lapse condition, realistic matter" CFG312); CFG318, CFG319, CFG312 READMEs and CFG318's
frozen criteria (bound transcriptions) and SLy code; A69 report section 4 (loop-factor method).

**Not blind.** Before this file I did scratch work (not committed) and hand estimates:
- On fixed Schwarzschild, in khronon-adapted variables, every foliation tau = t + h(r) has F = gamma^rr = N^2 and
  s = N sqrt(N^2 - e) (e = 1 - 2M/r); the P-sector Lagrangian becomes r^2 p N' - r^2 W - (gamma_L/2) N^2 ((r^2 p)')^2/r^2;
  the khronon equation integrates once to s N E_N = C. P = 0 forces N' = 0, so the Painleve-Gullstrand (PG) foliation
  with P = 0 is an exact solution (exact Schwarzschild).
- Static foliation: |A| -> infinity at the horizon, so u -> a0 (the cap is reached) and the clock stress ~ (a0/K)|A|
  diverges like e^(-1/2) (expected singular).
- Screened limit (sigma = a0 L*^2/(2GM) >> 1): N is algebraic, (1 - N) sqrt(N^2 - e) r^2 = kappa N, with two branches
  (static-like outside, PG-like inside). Scratch: they meet at an X-point only for kappa* = 1.4938, r_c = 3.652 M,
  N_c = 0.768; the transonic solution has N(2M) = 1 - kappa*/4 = 0.627 (regular).
- Cap-saturated limit (sigma < 1/2, SMBH): N^2(N^2 - e) = c^2/(4 r^2 (1 + 2 sigma N/r)^2) has one root, no critical
  point; scratch: the cap condition w = N' + sigma (2N^2/r)' > 0 on r >= 2M holds for c = 0.01-1.0 and fails at c = 1.5
  (all sigma tried). So the khronon charge c is free there.
- Size estimates: deviations ~ a0 GM/c^4 = 1e-14 (M87*), 7e-18 (Sgr A*), 1e-22 (10 Msun); NS (R/L*)^2 ~ 3e-28.
- Strong coupling (hand estimate): on backgrounds with a phantom density div P0 > 0 the khronon perturbation pi gets
  gradient energy (div P0) (nabla pi)^2/2, so C5's omega = 0 pair may propagate there; the clock-nonlinearity cubic
  ~ (Z/2) pidot (nabla pi)^2 gives k_sc = sqrt(2) Z^(-1/8) G^(3/8); lab (Sun's hedgehog background) gives
  k(38.6 um)/k_sc ~ 0.05 (24 pc) to 0.1 (90 pc) bare. These estimates set no threshold below.

## 1. The theory tested (v3) and the scaled problem

v3 (THEORY_V3_DRAFT section 1): C5's unitary-gauge Lagrangian at beta = eta = gamma_F = 0, xi = 1,
L/(N sqrt h) = [R3 + K_ij K^ij - theta^2 + 2 mu_K^2 (1/N - 1)^2]/(4K) + P^i D_i ln N - W(u) - (gamma_L/2)(D.P)^2,
u = K|P|, K = 4 pi G, W'(u) = u a0/(K (a0 - u)) (the record's capped W, C8), gamma_L = K L*^2/2,
K(Q) = mu_K^2 (Q - 1)^2 with mu_K^-1 = 100 kpc (BS24 Eq. 39 cap, via C4). Matter couples to g only.

Static spherical sector: metric -e^(2 Phi) f dt^2 + dr^2/f + R(r)^2 dOmega^2, khronon tau = t + h(r), P = p e^mu (e the
unit radial vector orthogonal to n). Reduced action built covariantly in sympy; Euler-Lagrange in Phi, f, R, h, p.
Scaled units GM = c = 1: a_hat = a0 GM/c^4, sigma = a0 L*^2/(2 G M), p = (a_hat/K) p_tilde with |p_tilde| < 1 (the
cap), khronon charge c_hat = -C K/a_hat. Deviations from Schwarzschild are O(a_hat) (linear response; the foliation is
fixed at leading order by the khronon equation, a degenerate perturbation problem).

**Benchmarks (masses ILLUSTRATIVE; every verdict margin is insensitive to factor-2 changes):** M87* 6.5e9 Msun,
Sgr A* 4.3e6 Msun, stellar BHs 10 and 63 Msun (GW250114-like remnant), NS 1.4 Msun and M_max (SLy, CFG318's recalled
piecewise polytrope). L* in {20, 24, 90} pc, both footings. Dynamical-mass radius for the EHT mass: Sgr A* 2000 AU
(upper end of S-star orbits), M87* 100 pc (stellar-dynamics scale); both ILLUSTRATIVE. Inside L* the computed
near-zone m(r) is used; outside L* the unscreened strong-field law offset a0/g_N(r_dyn) is used.

## 2. Checks (script prints `ID PASS/FAIL value threshold`; exit 0 iff all PASS)

**Part A (sympy, exact):**
- A1: the covariant reduced P-sector Lagrangian on Schwarzschild equals r^2 p N' - r^2 W(Kp) - (gamma_L/2) N^2
  ((r^2 p)')^2/r^2 with N = (1/e - e h'^2)^(-1/2) and gamma^rr = N^2; residual 0.
- A2: PG-Schwarzschild (h' = sqrt(2M/r)/e, p = 0) solves all five Euler-Lagrange equations of the full reduced action
  (GR + P sector + K(Q)) for symbolic M, gamma_L, mu_K and any W with W(0) = W'(0) = 0; residual 0. And on
  Schwarzschild: p = 0 => N' = 0 (p equation) and, with mu_K > 0, N = 1 (khronon equation); residual 0.
- A3: on Schwarzschild the khronon equation is d/dr[s N E_N] = 0 with E_N = -(r^2 p)'(1 + gamma_L D)
  - mu_K^2 r^2 (1 - N)/(K N^3), D = N (r^2 p)'/r^2; the p equation is N' + gamma_L (N D)' = K W'(Kp); residual 0.
- A4: the stress components T^t_t, T^r_r, T^th_th from the reduced variations vanish identically at p = 0, Q = 1, and
  on every numerical background of Part B the radial conservation residual
  |(T^r_r)' + Phi_K' (T^r_r - T^t_t) + (2/r)(T^r_r - T^th_th)| / max|terms| <= 1e-5 on r in [2.3, 20] M, points
  within 0.05 M of a critical point excluded (Phi_K = ln sqrt(-g_tt); the static diagonal metric makes the flux
  T^t_r drop out of this component).

**Part B (stationary foliations, numeric):**
- B1 (static branch, every benchmark): 1 - u/a0 <= 1e-3 at e = 1e-8 (cap reached) and the fitted exponent
  d ln|T^r_r| / d ln e on e in [1e-10, 1e-6] lies in [-0.6, -0.4]. PASS = "static branch confirmed singular".
- B2 (screened, sigma >= 2): kappa* = sigma c* found by the X-point condition; the algebraic residual of the
  transonic N(r) <= 1e-10 on [1.2, 200] M; one-sided slopes at r_c agree within 1e-4; N(2M) > 0; u/a0 < 1 at
  r >= 2M for p_tilde(2M) in [0, 1] (the homogeneous q/r^2 mode is a nuisance, reported as a range);
  |N/sqrt(e) - 1| <= 1e-3 at r = 200 M (static-like exterior).
- B3 (cap-saturated, sigma < 1/2): for c in {0.01, 0.1, 0.3, 1.0}: N smooth through r = 2M with N(2M) > 0 and
  w = N' + sigma (N D)' > 0 on [2, 200] M (cap consistent); the largest valid c on a 0.05 grid is reported.
- B4 (intermediate, 1/2 <= sigma < 2, i.e. Sgr A* at 90 pc): the finite-a_hat ODE (regulator a_hat_reg in {1e-6,
  1e-7}) is validated by reproducing B2's kappa* at sigma = 1e3 within 1e-3 and B3's N(r) at sigma = 0.045, c = 0.3
  within 1e-4; then a regular solution (N(2M) > 0, smooth, static-like at 200 M) is found, or the case is OPEN.

**Part C (observables):**
- C1: at a_hat = 0 the code returns Schwarzschild exactly: b_c = 3 sqrt(3), r_ph = 3, r_ISCO = 6, Omega_ISCO =
  6^(-3/2), eikonal Omega_c = lambda_L = 1/(3 sqrt(3)), all within 1e-10.
- C2: response coefficients d ln X / d a_hat from a_hat_num = 1e-6 and 1e-7 agree within 1e-3 (linearity); the PG
  solution gives exactly 0.
Observables: shadow b_c (mass at r_dyn and, separately, mass at 50 M = "local"), r_ph, r_ISCO, Omega_ISCO, eikonal QNM
Omega_c and lambda_L (Cardoso et al. 2009 light-ring correspondence, ADOPTED as in CFG318; valid because c_T = 1).

**Part D (neutron stars):**
- D1: SLy TOV M_max = 2.0485 +- 0.002 Msun (CFG318's in-lane value).
- D2: the screened static P profile solves its equation with residual <= 1e-8 and u/a0 < 1 everywhere (cap not reached).
- D3: delta R/R and delta M/M at amplifications lambda = 1e21 and 1e22 of the P stress agree (after dividing by
  lambda) within 1e-3 (linear response).

**Part E (strong coupling and the ringdown channel):**
- E1 (sympy): the decoupling-limit (Stueckelberg tau = t + pi) quadratic action of v3 on a frozen background (uniform
  Q_bar, A0, P0, div P0 = d) has the form (1/2) Z(k) pidot^2 - (1/2) G (nabla pi)^2 with Z, G derived exactly; P
  integrated out at tree level.
- E2 (cross-check with C5's own linearisation, reused and generalised to N0 != 1 and div P0 = d, with the 1/N in
  K_ij restored): at d = 0, Q_bar = 1 it reproduces C5's omega = 0 pair (zero non-tensor roots); at d != 0 its
  non-tensor omega^2/k^2 agrees with E1's G/Z within 1e-2 at a WKB-valid point (k >> background gradients).
- E3 (sympy): cubic and quartic vertex coefficients of pi (pidot (nabla pi)^2, pidot^3, (nabla pi)^4) from K(Q), the
  clock's nonlinearity and W's cubic, exact in the stated truncation.
- E4: strong-coupling scale per vertex, A69-style: canonical normalisation, isotropic rescaling x -> x/c_pi,
  Lambda^2 = Z^(3/2) c_pi^(7/2)/|lambda_3| (and the quartic analogue); loop factor eps = (E/Lambda)^4 with
  E = c_pi k (static/off-shell probes) or max(omega, c_pi k).

**Declared observed systems for E4 (k, omega, background):** Eoet-Wash (k = 1/38.6 um, omega = 1e-3 s^-1, Earth
surface: Sun + Earth hedgehogs, Q_bar - 1 = 1e-6); planets (1 AU, 2 pi/yr); double pulsar (a = 8.79e8 m,
2 pi/2.45 h); LIGO BH (k = 1/r_g, omega = c/(3 sqrt 3 r_g), 10 and 63 Msun regular backgrounds); NS surface (1/12 km,
c/12 km); EHT (1/r_g of M87* and Sgr A*); galaxy (1/kpc, 200 km/s / 10 kpc, deep-MOND background); cosmology
(k = 10 h/Mpc, omega = H0, FRW: P0 = 0, Q_bar - 1 from BS25's Omega_K = 0.26, illustrative).

## 3. Verdict rules (one per tile)

- **V1 Black holes (EHT):** PASS iff (i) for every benchmark BH x L* x footing a stationary solution regular across the
  Killing horizon with a static-like exterior exists (B2/B3/B4), and (ii) every observable shift (shadow at r_dyn mass,
  local shadow, r_ph, r_ISCO, Omega_ISCO) has |delta| <= 1e-2 for all computed family members (c grid, q range).
  FAIL iff for some benchmark only Killing-horizon-singular stationary solutions exist, or some |delta| > 0.10 (the
  cited ~10% EHT size line). OPEN otherwise. Scope: non-rotating, stationary; interior r < 2M not used; moving and
  rotating v3 BHs not computed (reported as an open sub-item in the tile note).
- **V2 Ringdown:** PASS iff (i) the energy leakage into any non-tensor mode is <= 1e-2 of the GR damping per cycle
  (E1/E2 mixing bound on the BH backgrounds) and (ii) eikonal |delta f/f|, |delta tau/tau| <= 1e-2 for every
  benchmark. FAIL iff a shift or the leakage exceeds 3e-2 (GW250114's "few percent"). OPEN otherwise.
- **V3 Neutron stars:** PASS iff |delta R/R| at 1.4 Msun, |delta M_max/M_max| and the timing-mass offset (orbit radius
  1e9 m) are all <= 1e-2. FAIL iff any exceeds 0.1. OPEN otherwise.
- **V4 Strong coupling:** PASS iff E2 passes and eps <= 1e-2 (no 16 pi^2 credit) for every derived vertex at every
  declared system where the mode exists. FAIL iff E2 passes and eps/(16 pi^2) >= 1 for some declared system. OPEN
  otherwise (including E2 failing).
- **V5 Leaf/lapse condition in strong fields (static spherical; the v3 replacement of the CFG312 tile):** PASS iff on
  every regular benchmark solution (BH exteriors, NS) N > 0 and u < a0 strictly, so the radial leaf operator
  (principal coefficient gamma_L N sqrt(F)) is elliptic and the P functional strictly convex (C8's conditions).
  FAIL iff a regular solution reaches N = 0 or u = a0 at r >= 2M. Scope: spherical, static; non-spherical strong
  fields stay OPEN.

## 4. External bounds (record transcriptions; values PROVISIONAL where marked)

| bound | value used | source |
|---|---|---|
| EHT Sgr A* shadow size | ~10% of Kerr | EHT Sgr A* Paper VI, as transcribed in `campaign_fresh_gravity/CFG318_strong_field_bh/FROZEN_CRITERIA.md` L35-36 (PROVISIONAL) |
| EHT M87* | no percentage in the record; 10% working line, PROVISIONAL | same file L36 |
| ringdown (220 mode) | "within a few percent" (GW250114); +-30% per mode | same file L37-38 (PROVISIONAL) |
| NICER radius precision | ~10% (from memory, PROVISIONAL) | Miller et al. 2019, arXiv:1912.05705 (record index MY2019-128) |
| 2-Msun pulsar mass precision | ~5% (from memory, PROVISIONAL) | Cromartie et al. 2019, arXiv:1904.06759 (record index MY2019-160) |
| short-range gravity probe | Yukawa range < 38.6 um | Lee et al. 2020, arXiv:2002.11761, as transcribed in `real_research/reviews/toe_law/agentN4_tail_literature.md` L241 |
| record's old-chassis numbers | shadow 3.85e-12, QNM damping 2.04e-10, NS M_max 2.9e-9 | CFG318 README |

The verdict lines use strict floors (1e-2) below every cited bound, so the PROVISIONAL values cannot flip a PASS.

## 5. Assumption / input ledger

| ingredient | class | source |
|---|---|---|
| v3 action, W, gamma_L, xi = 1, beta = eta = gamma_F = 0 | FRAMEWORK-NATIVE | C4, C5, C8, THEORY_V3_DRAFT |
| K(Q) = mu_K^2 (Q-1)^2, mu_K^-1 = 100 kpc | literature via C4 (BS24 Eq. 7, 39), not on disk | C4 README |
| L* grid 20/24/90 pc; a0 footings | FITTED (kappa = 1/2) | D10, C5/C8 grids, doors BRIEF |
| benchmark masses, r_dyn | ILLUSTRATIVE | this file |
| SLy piecewise polytrope | external EOS, parameters as recalled in CFG318 (PROVISIONAL) | CFG318 script |
| Omega_K = 0.26 (FRW dust) | illustrative background only (BS25 via C5) | C5 README |
| eikonal QNM / light-ring correspondence | ADOPTED external method | CFG318 |
| loop-factor method | record method | A69 section 4 |

No LambdaCDM-processed or standard-MOND machinery enters any verdict; the unscreened strong-field law appears only as
the theory's own limit (AQUAL mu = x/(1+x)).

## 6. Mutation

`P3_MUTATE=1` sets the clock coefficient xi = 2 (C4/C5's mutation). A1 and A3 must FAIL (identity residuals != 0);
outputs go to `p3_v3_strong_field_MUTATE.out` and `p3_v3_strong_field_results_MUTATE.json`.

## 7. Compute

`OMP_NUM_THREADS=1 nice -n 15`, single thread, < 1 GB RSS, minutes; no downloads; no PM runs.

## AMENDMENT A1 (written after scratch prototyping, before the lane script exists)

- **(a) B1, POST-RESULT.** Scratch prototyping of the static branch (capped zone p_tilde = 1, N = sqrt(e)) gave
  T^r_r -> 0 (proportional to e), not e^(-1/2). The frozen B1 exponent line will therefore read FAIL; it is kept as
  frozen and kept FAIL. Added reading (not a frozen line, used by no verdict): the exponents of T^th_th and of the
  on-shell scalar Lagrangian density L_P (expected -1/2 from the prototype) and of the invariant T^mu_nu T^nu_mu
  (expected -1). If those diverge, the static branch is singular through its tangential stress.
- **(b) B2/B4, PRE-RESULT (no B4 number computed).** The homogeneous q/r^2 mode is scanned over p_tilde(2M) in
  [-1, 1] (P may point inward near the horizon; W depends on |P|); a member is valid only if |p_tilde| <= 1 on
  [2M, r_out]. B4's finite-a_hat regulated IVP is dropped: in a capped zone it is a stiff saddle (one growing mode in
  either direction). B4 instead uses the exact a_hat -> 0 constructions of B2 (type T, screened, transonic) and B3
  (type C, capped). Junction-type members (screened outside, capped inside) are not computed: in the a_hat -> 0 limit
  they carry thin shells that need the regulated layer. B4 PASS iff a valid T or C member exists for each
  1/2 <= sigma < 2 benchmark; otherwise that benchmark is OPEN.
- **(c) Part C, PRE-RESULT.** On tilted solutions the khronon flux gives r^2 T^r_t = c, so the static-frame T^t_t
  grows like 1/e near the horizon. The mass function therefore uses ingoing coordinates: m' = -4 pi r^2 T^v_v with
  T^v_v = T^t_t + T^r_t/e, and psi' = 4 pi r T_rr(EF) with T_rr(EF) = (T^r_r - T^t_t)/e - 2 T^r_t/e^2. Then
  A = e^(2 psi)(1 - 2m/r) and B = 1 - 2m/r. The dynamical mass is Keplerian, M_dyn = r^2 A'/2 at r_dyn. The added
  check: T^v_v and T_rr(EF) stay finite as r -> 2M on every regular member (|value| at r = 2.001 M <= 10 x the value
  at 2.5 M).

## AMENDMENT A2 (PRE-RESULT for Part E: no Part E number has been computed by any script)

- **Why E2 changes.** C5's local matrix freezes the background coefficients at one point. After integrations by parts,
  that drops every term proportional to a background gradient. On v3 backgrounds the khronon pair's gradient energy
  is entirely such a term (it comes from the phantom density div P0 and from the stiffness mismatch). A frozen-matrix
  omega^2/k^2 at d != 0 therefore cannot test E1's G.
- **New E2.**
  - (i) Kinetic coefficient. In C5's unitary-gauge expansion (beta = eta = gamma_F = 0, the 1/N in K_ij restored),
    restricted to the lapse perturbation n and the longitudinal p_z, integrate p_z out. The result must equal E1's
    P-sector kinetic coefficient Z_P(k) = k^2/(K M_kk + gamma_L k^2) under n = -pidot; residual 0.
  - (ii) Gradient coefficient. G is taken from the exact spherical khronon first integral (A3). Its linear response
    to a static radial tilt around the static foliation is c = r^2 h' G_eff. The code must reproduce the weak-field
    limit G_eff -> D.P (1 + gamma_L D.P) + mu_K^2 (Q_bar - 1)/K within 1e-3 at 1 - e <= 1e-4.
  - C5's own omega = 0 count is cited, not re-run.
- **E4 dispersion.** E4 uses c_pi^2 = G/Z: first order in background gradients, labelled ESTIMATE. Where G <= 0 the
  pair does not propagate stably; such systems are reported separately and are not scored as weakly coupled.
- **Ringdown mixing bound (V2 (i)).** The pi-metric mixing is eps_mix = sqrt(Z_P K) c_pi/omega. The energy
  leakage per cycle is bounded by eps_mix^2.
