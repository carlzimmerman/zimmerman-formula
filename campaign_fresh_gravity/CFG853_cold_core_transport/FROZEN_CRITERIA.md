# CFG853 FROZEN CRITERIA: granular (fragment) dynamical-friction transport of the dSph cold core

Owner block 850-859. CFG853 checked unused on 2026-10-19 at HEAD e3fc772b5: no directory, no LEDGER row, no commit message
mentions it. This file is written and committed alone, before any script exists. kappa = 1/2 is FITTED; both footings are
graded separately and never pooled; no dark-matter species is added; not "theory closed".

## 1. Question

The handoff (sol61_push/HANDOFF_TO_CLAUDE_COLD_CORE_TRANSPORT_2026-10-19.txt) asks for a physical way, inside the framework,
for cold mass to shed energy AND angular momentum and concentrate in Draco and Sextans without over-boosting Fornax and Leo I.

One mechanism is tested: the free cold energy is fragmented into self-bound lumps of mass m (as in ARGON11's low-density
branch), and the lumps sink by gravitational (Chandrasekhar) dynamical friction against the LIGHT populations (diffuse cold
energy, settled cold, stars; gas while present). Friction removes orbital energy and angular momentum together and deposits
them in the light populations: a reciprocal cold -> light heat/torque transport. It needs no new interaction, it is internal
to each dwarf (so a priori host-, gas-loss- and age-independent, as CFG843/838/839/852/860/827 require), and it is the
gravitational part of the handoff's fragment route. The non-gravitational part (fragment capture/fusion, M100 action) is NOT
tested here.

Does one law (one m, one fragment fraction, one reservoir recipe) deliver the Draco and Sextans cores while keeping Fornax and
Leo I (and Draco and Sextans themselves) within their allowed excess, without overheating the stars?

## 2. Fixed inputs (no new data, nothing downloaded)

- I1 dwarfs: real_research/data/dsph/lvd_dwarf_mw.csv rows (M_V, rhalf_sph_physical = Plummer a, vlos_sigma,
  vlos_sigma_em) for Draco, Sextans, Fornax, Leo I. Upsilon_V from CFG827 cfg827_results.json (SFH, [M/H] -1.31):
  Draco, Fornax, Leo I. Sextans Upsilon_V = 2 (assumption, as in CE-FM-084; it has no SFH row).
- I2 baseline (the handoff / CE-FM-084 convention): M* = Upsilon 10^(0.4(4.83 - M_V)), R = 4a/3, p = 64/125,
  y = G p M*/(R^2 a0), s = min[p(sqrt(1/4 + 1/y) - 1/2), 5.364]. Total cold stock 53.64 M* (retention 0.1, ratio 5.364:
  inputs, not measurements). Remaining reservoir M_rem = (53.64 - s) M*. Needed extra inside R:
  M_x = M*[3 R sigma^2/(G M*) - p - s]; F = M_x/M_rem. Allowed extra A: the same with sigma + 2 sigma_err.
- I3 footings: canonical a0 = 9.3603e-11 m/s^2 and alt a0 = 1.1312e-10 (5.364 and 0.1 unchanged). Constants
  G 6.674e-11, M_sun 1.989e30, pc 3.0857e16.
- I4 catchment radius r_ta: CFG822 cfg822_results.json canonical rows (Draco 26.34, Sextans 25.16, Fornax 105.51,
  Leo I 65.16 kpc), used for both footings.
- I5 CFG861 cfg861_results.json per-system delta (binary shift, dex in g) for the reported Sextans/Draco variants.

## 3. Model (declared; the same law for all four dwarfs)

- M1 reservoir: M_rem lies outside R with dM/dr = mu = const (rho ~ r^-2) from R to r_out.
  G1 (record catchment): r_out = r_ta. G2 (compact; the handoff's 5R virial-cloud scale, with the more centrally weighted
  r^-2 profile): r_out = 5R.
- M2 composition: a fraction phi of the reservoir (at every radius) is in lumps of mass m; 1 - phi is light (diffuse). One
  common phi for all dwarfs: phi = max(F_Draco, F_Sextans), the smallest common value that can deliver both cores.
- M3 initial mass model (static): stars Plummer (M*, a); settled cold s M* inside R with M_s(r) = s M* r/R; reservoir
  mu (r - R) beyond R (lumps + light). V_c(r)^2 = G M(r)/r.
- M4 friction: lumps on circular orbits sink by Chandrasekhar friction against the LIGHT background
  rho_l(r) = rho*(r) + (1 - phi) mu/(4 pi r^2) for r > R:
  d(r V_c)/dt = -r 4 pi G^2 m rho_l lnL B(1)/V_c^2, B(X) = erf X - 2X exp(-X^2)/sqrt(pi), X = 1 (sigma_l = V_c/sqrt 2).
  Arrival time at R from r_i: t = I(r_i)/(G^2 m lnL), I(r_i) = int_R^{r_i} [d(r V_c)/dr] V_c^2/(4 pi r rho_l B(1)) dr.
  Delivery is inside-out. With a common product Q = G^2 m lnL t, the delivered lump mass is M_del = phi mu (r_d - R) with
  I(r_d) = Q, capped at phi M_rem. lnL is common to all dwarfs; this is permissive for any dwarf with larger r V_c^2 than
  Draco (its true lnL at fixed m is larger, so it would receive more). The script prints r V_c^2 to show which.
- M5 heating (Rosenbluth, light species): a light test species (mass << m) in a Maxwellian field of lumps (rho_L, 1D sigma_L)
  gains d<v^2>/dt = 8 sqrt(2 pi) G^2 m rho_L lnL sigma_L^2/(sigma_L^2 + sigma_s^2)^(3/2), independent of its own mass
  (= 4 sqrt(pi) G^2 m rho_L lnL/sigma for equal sigma). So the energy the sinking lumps lose is shared by all light species
  equally per unit mass. Equal sigma is permissive (colder stars would take more).

## 4. Graded tests (each in G1 and G2, each footing)

- T2 (primary, four dwarfs, one law). r_F,i = R_i + M_x,i/(phi mu_i). Q* = max(I_Draco(r_F,D), I_Sextans(r_F,S)). With Q*,
  each of the four must receive M_del <= A. T2 PASSES only if all four pass. Otherwise it FAILS; the script reports
  M_del/A for each dwarf.
- T1 (stellar receiver; applies if the stars exist while the transport runs).
  E_sh = phi mu int_R^{r_F} Delta_eps(min(r, 2R) -> R) dr is the minimum orbital energy the delivered lumps lose while
  crossing [R, 2R]. Delta_eps is the circular-orbit specific-energy difference in the quasi-static potential at that lump's
  arrival: inner mass, plus lumps from inside r already delivered inside R, plus the light reservoir, plus lumps beyond r
  still in place.
  Receivers (a generous region [0, 3R]; lumps excluded) = stars inside 3R + s M* + (1 - phi) mu (min(3R, r_out) - R).
  Delta_eps* = E_sh/M_recv. Tolerance: Delta_eps_tol = V_c,need(R)^2 ln 10 with V_c,need^2 = 3 sigma_obs^2. Exceeding it
  would mean the stars were born >= 10x more compact than today. T1 FAILS for a dwarf if Delta_eps* > Delta_eps_tol.

## 5. Class (per footing; the two footings are reported separately and never pooled)

- **EXCLUDED**: T2 FAILS in G1 and in G2. Sub-label "and stars cannot be the receiver" if T1 also FAILS for Draco or
  Sextans in both geometries; "stellar receiver not excluded" otherwise. Sub-label "(Sextans-independent)" if T2-D (section
  6) also fails via Fornax or Leo I in both geometries; "(via Sextans inputs)" otherwise.
- **CONDITIONAL (compact reservoir only)**: T2 FAILS in G1 but PASSES in G2.
- **VIABLE CANDIDATE**: T2 PASSES in G1. If T1 then fails, the label is "CANDIDATE, pre-stellar (gas-receiver) epoch only".

## 6. Reported, not graded (cannot change the class; the README must say if any of them would flip T1 or T2)

- T2-D (Sextans-independent): phi = F_Draco, Q = I_Draco(r_F,D), guards Fornax and Leo I only.
- R1 persisting lumps (no coalescence after arrival), with delivery just completing at t*. Then m cancels:
  Delta_eps_post = 2 sqrt(pi) [3/(4 pi R^3 sigma)] phi mu int_R^{r_F} [I(r_F) - I(r)] dr, with lnL_heat/lnL = 1. Compared
  with the tolerance.
- R2 relaxation (lump-lump, gravothermal) channel:
  - (a) stars gain 1/2 x 4 sqrt(pi) x 0.34 sigma^2 = 1.205 sigma^2 per lump relaxation time (t_r = 0.34 sigma^3/(G^2 m rho lnL)),
    independent of m;
  - (b) energy growth |E_f|/|E_i| with E = W/2. Initial: inner mass with stars p M* + the M1 reservoir. Final: the needed
    M(<R) = 3 R sigma^2/G as a uniform sphere (least bound; SIS variant), with the remainder dispersed to E = 0. The escaper
    specific energy this needs is compared with sigma^2/2 (diffusive escapers leave with E ~ 0+).
- R3 angular momentum: the net-spin fraction lambda_crit for which J, deposited with the same mass share as E, spins the stars
  to v_rot = 0.5 sigma at r = 1.5R.
- R4 variants:
  - Sextans sigma binary-corrected (CFG861 delta: sigma x 10^(delta/2)) and sigma - 2 sigma_err;
  - strict tolerance ln 2;
  - per-dwarf phi_i = F_i in T1 (a knob, most permissive);
  - total background (lumps + light) in M4;
  - initial static potential in T1;
  - G0 for T1 (all undelivered light placed in [R, 2R]).
- D1 diagnostic: the four needed extra masses, and whether one non-decreasing extra-mass profile M_x(r) could satisfy every
  pair: (needed at sigma - 2 sigma_err) at the smaller R <= (allowed) at the larger R.

## 7. Controls

- K1: reproduce the handoff / CE-FM-084 numbers (canonical) to 1e-4 relative:
  - baseline sigma: Draco 4.334, Fornax 11.242, Leo I 7.468;
  - F: Draco 0.469303, Sextans 0.988540, Fornax 0.0130695, Leo I 0.0345131;
  - M_rem: 2.77236e7, 2.53958e7, 9.90289e8, 1.88437e8.
- K2 (M5):
  - the massless-test rate, averaged by quadrature over the test Maxwellian, matches the closed form to 1e-6 relative;
  - sympy verifies 2 v h' + 2 h = (4 n/sqrt pi) X exp(-X^2)/v for the Maxwellian Rosenbluth h.
- K3 (M4): in a singular isothermal background, M4 reproduces t = 1.17 r^2 V_c/(G m lnL) (BT08 eq. 8.13) to 1%.
- K4: the Plummer fraction M(<4a/3)/M = 0.512.
- MUTATE (CFG853_MUTATE=1, separate output files): inject sigma_obs,i for all four dwarfs so that M_x,i equals the M4
  delivery at Draco's own Q (phi held at the main-run value, sigma_err unchanged), in each geometry. T2 must then PASS, so
  the class must change. If it does not, the README must say the MUTATE did not bite.

Resources: 1 core, nice -n 19, numpy/scipy/sympy, < 1 GB, seconds to minutes. The running 1024^3 jobs are not touched.
