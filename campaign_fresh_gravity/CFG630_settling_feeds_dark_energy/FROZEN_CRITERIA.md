# CFG630 FROZEN CRITERIA: settling energy feeds dark energy (2026-10-11)

Committed alone, before any script or number of this lane exists.

## 0. What is new relative to the record
- CFG549 R1 computed a settling trickle (2e-7 to 8.5e-7) from CFG541's E_sink per settled mass, with INSTANTANEOUS settling, a
  Sheth-Tormen collapsed fraction on CAMB, and a w = -1 sink.
- CFG542 (Pb) later DERIVED the sink: Q = rho_c alpha tau_ff 1_B 1_C grad(psi).grad(Phi), which in the overdamped (class-A) runs takes
  the whole potential drop (Q/dW = 1.000-1.001), not only E_sink (about 0.31 dW). CFG549 R3f only rescaled by that factor.
- CFG557 derived the RATE-LIMITED settled catchment s_c(M, t; alpha) (capture time t_cap = r_e/(alpha V_f)).
- This lane joins them: the cosmic settling POWER density Q(z; alpha) from (census f_ret baryons) x (s_c(M, t; alpha)) x (dW per settled
  mass from CFG542), integrated through the dark-energy continuity equation, with alpha carried as a bracket. It adds the a0(z) drift,
  the sign analysis for a canonical partner, and a measurability verdict. It does not re-derive anything CFG541/542/549/557 settled.

## 1. Construction (frozen)
- U(t) = rho_c0 * Int dlnM_ta f_ta(M, t) s_c(M, t; alpha) eps_W(M) : settled potential energy released per comoving volume.
  - f_ta: excursion-set mass fraction per lnM with the TURNAROUND barrier delta_ta(t) (candidate B's switch selects the turnaround ball,
    CFG557 D1). PRIMARY Press-Schechter; bracket Sheth-Tormen form on the same barrier. Linear spectrum and growth: the PM's own
    Eisenstein-Hu input (cfg557_lib, sigma8 0.811), flat background. INHERITED INGREDIENT (Gaussian ICs, LCDM-background linear growth
    and the excursion-set ansatz) -> every U(t) is labelled "HMF context"; bracketed by PS vs ST and by M_min in {1e6, 1e8, 1e10} Msun/h.
  - s_c: cfg557_lib's catchment fixed point (census f_ret baryons, point-mass supply edge, spherical-collapse t_reach, EPS main progenitor;
    the last two are inherited and PROVISIONAL as in CFG557), re-implemented with ONE change: if no shell is captured, s_c = 0 (CFG557
    returns the grid floor 0.02). alpha = 0 gives t_cap = inf, so s_c = 0 through the same code path.
  - eps_W = c_W V_f^2, V_f = (G M_b a0)^(1/4), M_b = f_ret f_b M_ta; c_W = CFG542 overdamped dW/(M_cat V_f^2) interpolated in log M_b
    between its MW and cluster points (clamped outside), per footing.
  - Ratchet: class A is one-sided, so U(t) is replaced by its running maximum (Q >= 0).
- Q(t) = a^-3 dU/dt (physical W/m^3). Dark energy: d(rho_DE c^2)/dt + 3H(1 + w_b) rho_DE c^2 = +Q with w_b = -1 (the framework's input
  background), normalised to today's rho_DE0 (the measured input). Matter sector loses the same energy (binding energy); total energy
  conservation is checked numerically.
- alpha: DECLARED BRACKET [0.5, 1.19]. Lower end: the lowest alpha the record ran (CFG541 / CFG557 / CFG620; CFG620 not robust at 0.5).
  Upper end: CFG542 K9 causality/stability bound for Pb at cosmic q (alpha_max = 1.186). Reported at alpha = 0.5, 0.75, 1, 1.19; alpha = 2
  and alpha -> inf (free-fall ceiling) are diagnostics outside the bracket.
- Both footings (9.3603e-11 / 1.1312e-10), never pooled. kappa = 1/2 FITTED (it cancels in the a0 ratio).

## 2. Reported quantities
Q(z = 0); Delta rho_DE/rho_DE0 at z = 0.5, 1, 2, 3 (rho_DE0 - rho_DE(z)); 1 + w_DE(z) = -Q/(3 H rho_DE c^2); CPL (w0, wa) on (i) the DE-own
rho_DE(z), (ii) the observer's effective DE (matter normalised as a^-3 today), (iii) the H(z)-fit projection of CFG549;
a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) and its log10 at z = 1, 2, 3.

## 3. Decision rules (frozen)
- TESTABILITY. Context precision (never a verdict yardstick for the model): DESI DR2 Gaussian sigma(w0), sigma(wa) as already written in
  CFG549's results JSON (smallest over the four chains); galaxy a0(z): the smallest a0 difference the record calls separable is 0.02 dex
  (CFG571: F-DESI vs F-flat <= 0.02 dex "can't be separated"), with a 0.15 dex per-disc systematic floor (CFG571) and CFG549 R2's
  required 0.007-0.04 dex per bin.
  - MEASURABLE if, anywhere in the alpha bracket and on either footing, |1 + w0| >= sigma(w0), or |wa| >= sigma(wa), or
    |Delta log10 a0(z)| >= 0.007 dex at some z <= 3.
  - BELOW SENSITIVITY if every one of those is below 1e-2 of its threshold.
  - otherwise MARGINAL.
- SIGN. PHANTOM-SIDE if 1 + w_DE(z) <= 0 at every z (rho_DE grows toward today); report whether any crossing of -1 occurs and the
  maximum q = Q/(3 H rho_DE c^2), which sets the width of the band in which a canonical partner phi is singular (it is regular only where
  its own 1 + w_phi >> q).
- PREDICTION LABEL. The alpha-bracket range of Delta rho_DE/rho_DE0(z) on the primary (PS, M_min 1e8) is the lane's prediction, labelled
  "HMF context" because f_ta is inherited.

## 4. Controls (must pass in the main run)
- K1 PS mass-fraction normalisation over nu: >= 0.999.
- K2 rho_DE(z) from quadrature and from an ODE integration agree to 1e-9 relative.
- K3 energy conservation: |d(a^3 rho_DE c^2)/dt + p_DE d(a^3)/dt - dU/dt| integrated <= 1e-6 of U(0).
- K4 Delta rho_DE/rho_DE0(z = 0) <= the ceiling "all cold energy settled at the cluster eps_W".
- K5 the CPL projection of exact Lambda returns (w0, wa) = (-1, 0) to 1e-6.
- K6 (REPORTED, no pass/fail) native check: route-H instantaneous settled-catchment fraction above the PM's resolved mass vs the PM's own
  switch-on mass fraction (CFG424 TA boxes, z = 1, 0.5, 0; read-only JSON). A native-anchored variant rescales the settled mass to the PM
  at those epochs; it is reported as context.

## 5. MUTATE (CFG630_MUTATE=1, writes *_MUTATE.*)
- MU1 alpha = 0: max |Delta rho_DE| must be exactly 0 and a0(z)/a0(0) exactly 1 at every z.
- MU2 settled mass x2 (s_c -> 2 s_c, eps_W fixed): Q and Delta rho_DE must scale by exactly 2 (relative error <= 1e-12).
Both must hold or the lane's pipeline is broken.

## 6. Expected (stated before running)
From CFG549 R1 x the CFG542 factor, the expectation is Delta rho_DE/rho_DE0 ~ 1e-7 to 3e-6, phantom side, and BELOW SENSITIVITY by many
orders. A result outside 1e-8 .. 6e-6 would point to a bug and is checked before it is reported.

Discipline: no LCDM or standard-MOND yardstick in any verdict (context only). "Cold energy"; its mass is required; no particle species.
Nothing here says the data favour the framework. Not "theory closed".
