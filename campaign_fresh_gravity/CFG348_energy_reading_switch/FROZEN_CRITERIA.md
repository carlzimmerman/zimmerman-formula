# CFG348: a switch that reads the baryonic specific ENERGY instead of the expansion? FROZEN CRITERIA

Written and committed alone, before any CFG348 script exists. Standing: kappa = 1/2 (FITTED, the only declared
constant); kernel nu_mono; causality criterion B; the switch reads BARYONS only (MS1-MS5: baryons, or the MOND-sector
density lap(Phi - v) = baryons + phantom with the carrier only as its mean), never the carrier or curvature; c_T = 1;
beta = 0; ownership = the outermost bound system carries the phantom (PAPER35 / FG001). No DM particle (the cold mass is
still required). Nothing here can say "theory closed". CFG347 (theta_b readers: PARTIAL, zero-constant no-go) is the
baseline; its files, DE12 and L341 are exec'd/read read-only.

## 1. The reader and the routes
Reader on the khronon leaves (CFG329: leaf constructions are diff-safe): eps_b = (1/2)|v_b|^2 + U, with v_b the baryon
velocity relative to the leaf normal n (the Hubble flow on FRW) and U a potential on the leaf with the leaf-average
subtracted from its source (the cosmological reference). Threshold exactly 0 (no constant).
- **MS check first (decides admissibility).** The chassis's own auxiliary U (C-H / L340 / CFG329) is read from the
  record: if its source is the total matter coupling to g (baryons + cold carrier), it is MS1's curvature/matter door
  and is NOT admissible (reported, not scored).
- **E1 baryonic potential (MS1 door d):** lap U_b = 4 pi G (rho_b - <rho_b>_leaf).
- **E2 MOND-sector potential (MS1 door c):** lap U_ms = lap(Phi - v) (baryons + phantom; carrier only as its mean).
- **Gate (slaved form):** L ⊃ B W(eps_b), W = S(-eps_b/eps_on), S = DE12's C-inf step: ON (W = 1) at eps_b <= -eps_on,
  OFF (W = 0) at eps_b >= 0. (The zero is the OFF edge; the opposite orientation is the MUTATE.)
  Width eps_on: (i) zero-constant framework velocity^2 a0 c / H0; (ii) the theory's own minimum from (c),
  eps_on,min = max over layers of [S'max v_B^2, sqrt(S''max) v_c v_B], v_B^2 = B/rho_b (one universal number = 1 constant).
- **E3 dynamical (CFG347 R3 structure):** S = Int sqrt(-g)[ -(Z/2)(d sigma)^2_{c_sigma} - (Z M^2/2) sigma^2 - C sigma eps_b ]
  with f = S(sigma); quasi-static sigma = -eps_b/eps_on, eps_on = Z M^2/C. Zero-constant: c_sigma = c, M in
  {H(z), 3H(z), a0/c}, eps_on = a0 c/H0. Reach/timing as CFG347 (b3).

## 2. Tests (DE12's 24 hosts via transition(), z in {0.25,1,2.5,4}, M_b in {1e10,1e11,1e12}, both footings, w = 0.25)
- **(a) FRW.** sympy: on flat FRW with Lambda, eps_b = 0 exactly (shell identity from Friedmann). PASS iff W = 0 on the
  background AND in a finite neighbourhood (as CFG347), AND L341's growth harness with the mean gate <W> over the
  linear (Phi, v) field (Gaussian, mean-field; L341's spectrum, k >= 0.02 h/Mpc) gives D/D_LCDM(z=0) = 1 within 1e-6.
- **(b) bound.** (b1) static: at r = 30 kpc on every host, W = 1 (eps <= -eps_on). E1: eps_b = (1/2) g r + U_b with
  U_b = -G M_b / r (isolated, most lenient; the leaf-mean subtraction only raises eps). E2: U_ms(r) = -Int_r^{r_ta} g dr'
  - g(r_ta) r_ta (CFG347's r_ta; Lambda omitted, which only lowers eps). (b2) fidelity: a 10% compression (delta = 0.1)
  at the orbital rate Omega(30 kpc), k = 1/kpc and 1/(10 kpc): delta eps = v_c Omega delta/k + nu 4 pi G rho_b delta/k^2
  (worst case: azimuthal compression + the MOND-amplified potential); require |delta W| <= 0.1 AND the gas compressive
  mode change |rho_b/(rho_b + B W'(eps +- delta eps)) - 1| <= 0.1 on all 24 hosts (both k, 1e6 K). (b3) E3 reach
  ell = c_sigma/M <= r_ta/3.89 and timing M >= sqrt3 H.
- **(c) transition.** H1 no ghost: m_perp = rho_b + B W' > 0 and m_par = rho_b + B (W' + W'' v_c^2) > 0 on the layers
  (velocity-reading gates change the inertia); H2 gradient: the U-dependence enters only through the elliptic constraint
  (contributions ~ k^-2), so principal speeds are the gas's; H3 Hadamard: growth bounded uniformly in k. Report the
  theory's width in length ell_eps = eps_on / |d eps/dr| at the eps = -eps_on/2 crossing, against 100 kpc and CFG337's
  ell_min (183-378 kpc C2 lenient; 2.9 Mpc C1).
- **Constant count:** every number beyond kappa = 1/2.

## 3. Decision (per route; overall = best route, order FP > COST > PARTIAL > NO-GO; MS-illegal routes not scored)
- **FIRST-PRINCIPLES SWITCH:** (a), (b), (c) all pass with 0 new constants.
- **CANDIDATE WITH COST:** all pass with n >= 1 constants.
- **PARTIAL:** two of three pass.
- **NO-GO:** otherwise; state the obstruction as a theorem (Lean) or an example.

## 4. Controls
- **C1** reproduce CFG347's theta_b (b) failure with its exact settings: x = 0.1 Omega(30 kpc)/theta_* = 0.29-6.6
  (theta_* = 3H) and 33-154 (a0/c), within 2%.
- **C2** GR limit (B = 0): m = rho_b, gas + Jeans, healthy.
- **MUTATE** (CFG348_MUTATE=1, outputs *_MUTATE.*): threshold sign flipped, W = 1 - S(eps/eps_on) (ON at eps <= 0):
  must put the switch ON on FRW and give chassis-like growth (ratio >= 3); exits 1.

## 5. Expectations (written now, may be wrong; kept)
The chassis U is sourced by all matter (carrier included) -> MS-illegal. E1 fails (b1): MOND-supported orbits beyond
~2 r_M exceed the baryons' Newtonian escape speed (eps_b > 0). E2 passes (b1) and the fidelity test (eps conserved,
no flicker in the saturated interior), but (a) fails: flat FRW sits exactly at eps = 0, so no finite OFF neighbourhood,
and linear wells (|Phi| ~ 1e-6..1e-5 c^2) are as deep as galactic ones, so the gate fires in linear overdensities.
E3 zero-constant fails (b3) by CFG347's T7 whatever it reads. Expected: PARTIAL or NO-GO.

## 6. Lean (Lean 4 + Mathlib, no sorry; `cd fable_independent_2026/lean_2026 && lake env lean <abs path>`)
FRW shell identity (eps = 0); baryonic escape theorem (nu > 2 => eps_b > 0; flat curve beyond 2 r_M => eps_b > 0);
no-ghost inequality for the velocity-reading gate; saturated-interior fidelity (W' = 0 => no change); nested-well
obstruction (linear OFF and host ON incompatible when |Phi_lin| >= |eps_host|) with numeric instances.

## 7. Protocol
Scripts only in this folder; no downloads; <= 4 processes; no other lane's files edited.
