# FROZEN A36: the logotropic dark fluid (unified DM + DE) as a swoop of the law and the tie

Frozen before any A36 number from SPARC or the backgrounds. Script `scripts/recipe37.py`, output `scripts/recipe37.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing (disclosed): only the papers' quoted constants below, and analytic arithmetic done while reading them (kappa readings of G Sigma0 about 0.10, of the paper's g = G M_h/r_h^2 about 0.15, of the paper's a0 = g/f_b about 0.87; the r^-1 envelope of a pure logotrope gives a dark acceleration that rises to a ceiling near 1.5 G Sigma0, about 0.3 a0). No SPARC fit, no gate number, no background number was computed.

## Source equations (web reading 11-04, PROVISIONAL; read through ar5iv summaries, not the PDF)

Chavanis, arXiv 2201.05903 ("Predictions from the logotropic model: the universal surface density of dark matter halos and the present proportion of dark matter and dark energy"), as quoted by the reader:
- EoS (type II, eq. 38): P = A ln(rho_dm/rho_P), rho_P = c^5/(hbar G^2) (eq. 5).
- A = B rho_Lambda c^2 (eq. 12), B = 1/ln(rho_P/rho_Lambda) = 3.53e-3 (eq. 13), rho_Lambda = Lambda/(8 pi G) (eq. 3). The reader reports A fixed by identification: "If we identify" the fluid's asymptotic energy density with rho_Lambda c^2.
- Background (eq. 44, 45, 52): eps = Omega_dm0 eps0/a^3 + A(1/B + 3 ln a); H^2/H0^2 = Omega_dm0/a^3 + Omega_de0 (1 + 3 B ln a). So rho_DE(a)/rho_DE0 = 1 + 3 B ln a, and A/B = rho_Lambda c^2 = rho_DE0 c^2 today.
- Halo (eq. 146, 147): theta = rho0/rho, xi = (4 pi G rho0^2/A)^(1/2) r, (1/xi^2) d/dxi (xi^2 dtheta/dxi) = 1/theta, theta(0) = 1, theta'(0) = 0 (logotropic Lane-Emden, n = -1).
- r_h: rho(r_h) = rho0/4, theta(xi_h) = 4, xi_h = 5.85, theta'_h = 0.693 (eq. 149, 150).
- Sigma0 = rho0 r_h = 5.85 (A/4 pi G)^(1/2) (eq. 156); Sigma0 = (B/32)^(1/2) (xi_h/pi) c sqrt(Lambda)/G = 0.01955 c sqrt(Lambda)/G = 133 Msun/pc^2 (eq. 159; Lambda in s^-2 units).
- M_h = 4 pi (theta'_h/xi_h) rho0 r_h^3 = 1.49 Sigma0 r_h^2 (eq. 151, 157).
- Surface gravity g = G M_h/r_h^2 = 2.76e-11 m/s^2 = 0.0419 H0 c (eq. 166, 170); Tully-Fisher v_h^4 = 1.49 Sigma0 G^2 M_h with f_b = M_b/M_h ~ 0.17 (eq. 168, 169).
- a0: "a0 = g/f_b ... of order H0 c/4 = 1.65e-10 m/s^2"; the model is stated to be "completely different from the MOND theory".
- Halo is dark matter only; baryons not in the hydrostatic equation. Large-r: rho ~ 1/r (eq. 148, quoted by the reader as (A/8 pi G)^(1/2)/r; the ODE above gives theta -> xi/sqrt 2, i.e. rho -> (A/2 pi G)^(1/2)/r; the script checks the ODE and uses the ODE, and the coefficient discrepancy is reported as a reading issue). The paper says the logotropic profile is valid in the core and expects an envelope (r^-2 or r^-3) for finite mass.
- arXiv 2603.21302 (2026) abstract, as quoted by the reader: the r^-1 profile "may explain the universal surface density", the model "accounts for the universal gravitational acceleration felt by a test particle and for the Tully-Fisher relation" and "can thus provide an alternative to ... MOND". It also gives Lambda in terms of the electron mass and constants (not used here).

Implemented natively: rho_Lambda = rho_DE0 = Ode0 rho_crit0 of lib.py's cosmology (H0 67.4, Om0 0.315), B = 1/ln(rho_P/rho_DE0) from that, A = B rho_DE0 c^2, Sigma0 = xi_h (A/4 pi G)^(1/2) with xi_h from my own ODE solution. Checks printed: xi_h vs 5.85, theta'_h vs 0.693, 1.49, B vs 3.53e-3, Sigma0 vs 133 Msun/pc^2, 0.01955.

Dark acceleration of the published halo: g_DM(r) = G M(r)/r^2 = 4 pi G (Sigma0/xi_h) theta'(xi_h r/r_h) (exact, from d(xi^2 theta')/dxi = xi^2/theta). The halo is added to SPARC's g_b (lib.py, Y_disk 0.5, Y_bul 0.7). Shape is universal; Sigma0 fixed; the only per-galaxy quantity the papers allow is r_h (equivalently rho0 or M_h).

## (a) SPARC recipes (A fixed by Lambda in every row; Sigma0 never fitted except row L4, a disclosed non-published probe)

- L0, 0 knobs: the paper's own halo-baryon rule, M_h = M_b/f_b with f_b = 0.17 (paper), r_h = (M_h/(1.49 Sigma0))^(1/2). M_b = lib's g.Mb.
- L1, 1 global knob: same rule with f_b fitted (log f_b in [-3, 0]) on all galaxies; holdout: f_b fitted on GS[::2], graded on GS[1::2].
- L2, 1 knob per galaxy (171): log10 r_h per galaxy fitted to the law (bounds r_h 0.05 to 500 kpc), A fixed. Count at-bound galaxies. No holdout is meaningful for per-galaxy freedom (stated); reported for transparency as rms over GS[1::2].
- L3, 1 knob per galaxy, self-consistent variant (not as published, disclosed): logotropic hydrostatics in the baryon plus own potential, A d(1/rho)/dr = g_b + G M_dm/r^2, dM/dr = 4 pi r^2 rho, rho0 per galaxy fitted (log bounds +-3 decades about L2's rho0), A fixed. Tests whether letting the fluid feel the baryons buys the law's shape.
- L4 (probe, not the model): L2 with Sigma0 multiplied by one global factor fitted, to show which Sigma0 the law would need; counted as 1 + 171 knobs.
Each graded by lib.grade (E1 <= 0.02, E2 <= 0.04, E3 <= 0.02 against the law; rms to observed also printed). Holdout <= 0.025 for L1.
Expected in advance: all fail E3 at the high-g_b end and E1, because the logotrope's dark acceleration has a universal ceiling ~0.3 a0 while the law's g_obs - g_b reaches 0.62 a0 at g_b = a0; L2 better than L0; L4 wants Sigma0 several times larger.

## (b) The implied acceleration scale on G1 to G5

Readings, all with c sqrt(G rho_DE0) = 2 A0 as the denominator: (i) G Sigma0; (ii) the paper's g = G M_h/r_h^2 = 1.49 G Sigma0; (iii) the paper's a0 = g/f_b with f_b = 0.17 and with Ob0/Om0; (iv) the halo's asymptotic ceiling g_inf = G M(r)/r^2 at r -> infinity; (v) a_fit = lib.fit_a on the L2 recipe pooled (what the law sees). Primary for G1 is (iii) with the paper's f_b = 0.17, since it is the paper's own a0.
- G1 kappa_eff within 0.05 dex of 0.5.
- G2: Sigma0 ∝ sqrt(B rho_Lambda) with B = 1/ln(rho_P/rho_Lambda): slope d ln Sigma0/d ln rho_Lambda computed by finite difference over rho_Lambda x {0.5, 2} (all readings (i) to (iv) share it; (iii) also if f_b fixed). 0.50 +- 0.05.
- G3: A is an EoS constant, so Sigma0(z) is constant; a(z)/a(0) = 1 in the bands, stated by construction (halos formed at z keep the same Sigma0).
- G4: readings (i) to (iv) universal by construction; also the per-galaxy a_i = lib.fit_a on each L2 galaxy curve, rms of log a_i over galaxies with log M_h (L2) in 11 to 12.5, <= 0.1 dex.
- G5: halo gravity at measured radii: passes if g_DM >= 0.1 a0 at 1 to 30 kpc for the median L2 galaxy; printed.
- Cassini: not applicable (no force modification; dark fluid only), stated.

## (c) Tracking (GT) and whether the Lambda dependence is derived or imposed

- C1 own background: rho_DE(z)/rho_DE0 = 1 + 3 B ln a; Sigma0 constant; GT dev = -0.5 log10[rho_DE(z)/rho_DE0] at z 1, 1.5, 2.33, tolerance 0.05. Also w_DE0 = P_de/eps_de today (from eq. 44, 51 reading: the DE part has w = -1 - B/(1 + 3 B ln a)), printed.
- C2 A29 backgrounds B0, B1, B1p, B1u, B2, B3, B4, B5 (frozen w0, wa, EDE as in FROZEN_A29.md, recomputed here in closed form; check against A29's rho_DE ratios 1.018/0.874/0.668 for B1 etc.). Two readings: C2a A is a constant of the EoS (the model): a flat, GT dev = -0.5 log10 ratio; C2b A re-identified by hand as B rho_DE(z) c^2 at each z: tracks identically, counted as a hand term (the A10 rule). Note stated: no logotropic EoS produces these CPL histories; the logotrope has one history (C1).
- Derived vs imposed verdict, written from the equations: sqrt(A/G) is the only surface density a logotrope's hydrostatics can form (dimensional, from P = A ln rho), so Sigma0 ∝ sqrt(A) is derived; A = B rho_Lambda c^2 is fixed by identifying the fluid's late-time energy density with rho_Lambda. Within the unified-fluid model this is one constant playing both roles (not a second hand term); its value is fitted to rho_DE0 as Lambda is in LCDM, and B is set by the choice of rho_P as reference density.

## RESULTS (written after the run; criteria above unchanged)

One run, 7 s, peak memory 52 MB, single thread; no bug found, no wrong output to keep. Line numbers refer to `scripts/recipe37.out`.

Checks (l.3-6): my ODE gives xi_h 5.845, theta'_h 0.6935, 1.491 (paper 5.85, 0.693, 1.49); B 3.532e-3; Sigma0 131.6 Msun/pc^2 with prefactor 0.01955 (paper 133 with its rho_Lambda 5.96e-27; ours 5.85e-27). The ODE's tail is theta -> xi/sqrt 2, i.e. rho -> (A/2 pi G)^(1/2)/r, not the (A/8 pi G)^(1/2)/r the reader quoted for eq. 148 (l.4-5): a reading issue, the ODE is used.

Mechanism (l.8): the published halo's dark acceleration is g_DM = 4 pi G (Sigma0/xi_h) theta'(xi), which rises monotonically to a universal ceiling 2.79e-11 m/s^2 = 0.298 a0 (the r^-1 envelope). The law needs g_obs - g_b = 0.618 a0 at g_b = a0 and only ~ sqrt(g_b a0) at low g_b. Per-galaxy r_h only moves where the ceiling is reached; it cannot change the ceiling. So the curve undershoots the law at high g_b and overshoots at low g_b in every row.

(a) SPARC, against the law:
- L0, 0 knobs (paper's f_b 0.17): E1 0.1511, E2 0.2313, E3 0.1883 (l.11). FAIL.
- L1, 1 knob f_b: E1 0.1292, E2 0.2255, E3 0.2485 (l.17); f_b went to its upper bound 1.0 (l.16, disclosed; f_b > 1 would mean halos lighter than their baryons); holdout 0.1349 (l.20). FAIL. No r_h rule can beat L2, since L2 minimises each galaxy separately.
- L2, r_h per galaxy (171 knobs), Sigma0 fixed: E1 0.1026, E2 0.1876, E3 0.1384 (l.23); bins +0.138 at log g_b -12 and -0.097 at -10.5 (l.24); 2 r_h at bound; median r_h 1.52 kpc, log M_h 5.7 to 11.0 (l.53): the fit shrinks halos so the ceiling acts at all radii. FAIL.
- L3, self-consistent in baryon potential (not as published), rho0 per galaxy: E1 0.1851, E2 0.2648, E3 0.2217 (l.31); 10 grid-edge minima. FAIL, worse than L2.
- L4 probe, Sigma0 free globally + r_h per galaxy (172 knobs): best Sigma0 x 0.79 (105 Msun/pc^2), E1 0.0956, E3 0.1286 (l.36-37). FAIL. So freeing Sigma0 does not rescue the shape; the expectation that the law would want a larger Sigma0 was wrong (the fit trades high-g_b undershoot against low-g_b overshoot).
- Against observed: L2 rms 0.219 dex (l.25).

(b) Acceleration readings (l.43-48), kappa_eff vs 0.5: G Sigma0 0.098, g = G M_h/r_h^2 0.146, PRIMARY a0 = g/f_b 0.859 (f_b 0.17) and 0.933 (Ob0/Om0), ceiling 0.149: all FAIL G1. Only the pooled a_fit of the failed L2 curves, 0.533 (l.48), lands in the window; it is a fit of the law to a curve of the wrong shape (E1 0.10), not a scale of the model. G2 slope 0.5018 (l.50) PASS: Sigma0 ∝ sqrt(B rho_Lambda), with B's log giving the +B/2. G3 PASS by construction (l.51). G4: readings i-iv universal by construction; the frozen per-galaxy check is empty (0 L2 galaxies in log M_h 11-12.5, l.52-53, a deviation: the window does not apply to these small halos); over all 171 per-galaxy a_i rms 0.204 dex, which would FAIL. G5 PASS (l.54-56): g_DM 0.27-0.30 a0 at 1-30 kpc. Cassini not applicable.

(c) Tracking: C1 own background, rho_DE(z)/rho_DE0 = 1 + 3B ln a = 0.987 at z 2.33, GT dev +0.003 (l.60) PASS, trivially: the logotrope's DE is Lambda to 1.3 %, with w0 = -1 - B = -1.0035 (l.61), slightly phantom, the opposite side from the DESI-like rows. C2a, A held as the EoS constant (the model): GT fails in B1 (+0.088), B1p (+0.076), B1u (+0.096), B3 (-0.154) at z 2.33 and passes in B0, B2 (-0.046, marginal), B4, B5 (l.62-76): it passes only where rho_DE barely moves, i.e. it is flat, not tracking. C2b, A re-identified as B rho_DE(z) c^2 at each z, tracks identically: a hand term (A10 rule). No logotropic EoS yields these CPL histories; the logotrope has one history.

Derived vs imposed: given P = A ln(rho/rho_P), hydrostatics can form only one surface density, sqrt(A/G), so Sigma0 ∝ sqrt(A) and the 0.5 slope are DERIVED from the EoS form. The Lambda link is IMPOSED: A = B rho_Lambda c^2 comes from identifying the fluid's late-time energy density with rho_Lambda (the paper's own "if we identify"). Inside the unified-fluid model that is one constant doing both jobs, which is native and the cleanest version of the tie on record in this folder; but its value is fitted to rho_DE0 as Lambda is in LCDM, B depends on choosing rho_P as reference, and the constant does not move with z, so in evolving backgrounds the scale stays flat.

Verdict: the logotrope carries a native sqrt(rho_Lambda) surface density (G2, G3, G5 pass; GT passes in its own nearly-Lambda background), but its acceleration readings miss G1 by 0.23 to 0.71 dex, its halo shape cannot make the law (E1 0.10 at 171 knobs, 0.15 at 0 knobs; universal ceiling 0.30 a0), and with A constant it does not track evolving rho_DE(z). As expected on E1-E3; L4's direction was not as expected (disclosed).

Deviations: G4 window empty (reported on all 171); L1 f_b at its upper bound; L3 has 10 grid-edge minima; eq. 148 coefficient reading mismatch (ODE used). Provisional: all equations through web summaries of arXiv 2201.05903 and the 2603.21302 abstract; f_b 0.17 and the a0 = g/f_b reading are the paper's as summarised; A29 w0, wa values from memory (as in A29).

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
