# PB1_seeds_vs_quench: FROZEN CRITERIA, committed alone before any script or number

Kappa = 1/2 FITTED. Not theory closed. No dark-matter particle. Nothing here says the data favour the framework.
No downloads. Small job: one thread, analytic + 1D ODEs, minutes.

**Not blind.** Known before this file: EB1 (isolated sphere under R1 collapses 1e6 Msun at z 11-12), EB1b (with the
web's own field e(z) from WG2's R1 box, 0.026 a0 at z 50 to 0.006 at z 10, nothing collapses before z ~0.5 and the
A2744-QSO1 gate is NO everywhere), WG2-WG6 (R1 fails the CMB-lensing shape), QX3 (growth inside the action fails).
One input number was looked at before this file, to choose the drag treatment: CLASS (WG2 settings) gives x_e
2.3e-4 at z 50, z_drag 1059; the Compton drag rate on baryons is ~1e-5 H at z 50 and ~1 H near z 800-1000.
No PB1 result has been computed.

**A PBH population is a MASS component that must be paid for.** Here it is added on top of B2 (Omega_PBH =
f Omega_b in E(a), in the background acceleration and in the clustering mass). Nothing in this lane says where that
mass comes from, or whether f is allowed (that is PB2). This lane maps only what is NEEDED.

## Question
Under WG2's web rule R1 with EB1b's external field e(z), do primordial black holes of mass M (M_p) and abundance f
break the quench, so that (i) an A2744-QSO1-like hole is reached by z 7.0451 with Eddington growth from the PBH seed,
and (ii) galaxy-mass baryon structure (1e9-1e11 Msun) collapses by z ~3-6? R0 (Newton) is the control.

## Definitions
- **f = Omega_PBH / Omega_b** (PBH mass density over the cosmic baryon density), monochromatic mass M_p.
  Comoving number density n_p = f rho_b0 / M_p. E(a)^2 = Omega_r a^-4 + [Omega_b (1 + f) + Omega_fld] a^-3 + Omega_L,
  Omega_L = 1 - Omega_b (1 + f) - Omega_fld - Omega_r (flat). f = 0 is exactly EB1's B2.
- Inputs exactly EB1 / EB1b: WG2's CLASS settings, B2 background, a0kit footings (canonical 9.3542e-11, alt
  1.1356e-10 m/s^2, never pooled), TIE (flat a0), simple nu(y) = 1/2 + sqrt(1/4 + 1/y), scalar EFE
  nu((|g_N| + e a0) / a0), e(z) = WG2 snapshot percentile of |g_N| / a0 per footing, linear in ln(1+z) (EB1b's
  e_of_z, imported read-only), R1 boost on for z <= z_on = 50 (WG2's turn-on), Newton before. QSO1: z 7.0451,
  log M_BH in {6.9, 7.6, 7.7} (L324). Salpeter time from EB1 (T_SAL), eps 0.1 primary (t_E = 50.05 Myr), 0.2 reported.
- Baryon release: Compton drag on baryon bulk motion, Gamma_d = (4/3)(rho_gamma / rho_b) x_e n_H sigma_T c, with
  x_e(z) and T_b(z) from CLASS thermodynamics (same settings), drag toward the photon (Hubble) frame. Applied at all z
  in every stage. Gas sound speed c_b^2 from CLASS.

## Method
**(a) Point seed (secondary infall).** One PBH of mass M_p; baryon shells of Lagrangian baryon mass M_b = m M_p,
m on a log grid 1e-1..1e8 (4 per decade), only shells with f m < 1 (beyond that the shell encloses other PBHs: that
is regime (b)). Start z_s = 3000 (tight coupling), r = a R_L(M_b), v = H r. Shell equation
  d2r/dt2 = -(4 pi G / 3)[rho_b (1+f) + rho_fld + 2 rho_r - 2 rho_L] r - nu G dM / r^2 - Gamma_d (v - H r),
  dM = M_p + M_b - (4 pi / 3)(1 + f) rho_b r^3 (= M_p (1 - f m) at the start),
  nu = 1 (R0, and R1 before z_on); R1 after z_on: nu((|g_N| + e(z) a0) / a0), g_N = G dM / r^2.
Collapse: r <= 1e-3 r_max after turnaround (EB1). Pressure: a collapsed shell counts as bound only if
nu_ta G (M_p + M_b) / r_ta >= xi c_b^2(z_ta), xi = 1 primary, xi = 0 reported (NOPRESS).
M_bound(z) = largest M_b of a bound collapsed shell with z_coll >= z.

**(b) Poisson isocurvature.** White noise in the PBHs, P_p = 1 / n_p (comoving), not Silk-damped.
Linear stage, per comoving k, from y = a / a_eq = 1e-2 to z_on: two species, PBH (pressureless, no drag) and baryons
(drag Gamma_d, pressure c_b^2 k^2 / a^2), d2 delta_i / dt2 + 2 H d delta_i / dt (+ Gamma_d for baryons)
= 4 pi G (rho_p delta_p + rho_b delta_b) (- c_b^2 k^2 / a^2 delta_b). IC: delta_p = Meszaros growing solution of
unit initial amplitude at y0, delta_b = 0. Transfer T_b(k), T_p(k) per unit initial delta_p.
sigma_iso^2(M_b) = int dk k^2 / (2 pi^2) P_p W^2(k R_L) T_cl(k)^2, T_cl = (T_b + f T_p) / (1 + f) (clustering-mass
contrast), k cut at the mean PBH separation k_int = (6 pi^2 n_p)^(1/3). Growth rate f_M from the same ODE.
Adiabatic part: EB1's sigma_f (CLASS baryon field), added in quadrature, rate weighted by variance.
Validity: (b) used only where N = f M_b / M_p >= 10 (Gaussian-ish Poisson counts). M_b in {1e5, ..., 1e12}.
Nonlinear stage: EB1b's shell from z_on, delta_0 = nu_pk sigma_tot, nu_pk in {3, 5}, clustering mass (1 + f) M_b,
R0 and R1, drag included (negligible after z_on).
Diagnostic only (no label): rms field of the iso mode at 8 M_b at z_on over e(z_on); delta_b / delta_p at z_on.

**Integrator.** One vectorised RK4 with per-shell adaptive step (dt = eta min(t, r/|v|, t_dyn)), drag applied as
an exact exponential on the peculiar velocity each step. Checked by KA1 / KA4 / MU1 below.

**QSO1 growth.** M_BH(t_start = t(z = 1000)) = M_p; dM_BH/dt = M_BH / t_E while M_BH < M_p + eta_f M_res(t),
otherwise M_BH = M_p + eta_f M_res(t) (supply ceiling). eta_f = 1 primary (maximal, so a NO is robust), 0.1
reported. M_res(t) = max(M_bound(t) from (a), baryon mass of the largest 5-sigma (b) clump collapsed by t, used only
where that clump holds >= 1 PBH on average, N >= 1). nu_pk 3 reported.

## Grid
M_p in {1e1, 1e2, ..., 1e9} Msun, f in {1e-10, 1e-9, ..., 1}: 99 cells, both footings, R0 and R1.
Readings: e median (primary), p05, p95. Variants (reported, used only for CONDITIONAL): ZON_REL (R1 boost on from
z 1000, e(z) above z 50 extrapolated as the power law of WG2's z 30-50 segment), PBH-EFE (for (a): e_tot =
sqrt(e_web^2 + e_H^2), Holtsmark field e_H = 2.603 G M_p n_phys^(2/3) / a0), NOPRESS (xi = 0).

## Gates (per cell, per footing)
- **G_i QSO1:** PASS if M_BH(z 7.0451) >= 10^7.7 (headline); 10^6.9 reported. Cells with M_p >= 10^7.7 are marked
  TRIVIAL (the seed already is the hole) and do not count toward QUENCH BROKEN. n_p reported per cell (no gate:
  abundance is EB2's question).
- **G_ii galaxy:** PASS if a 3-sigma (b) clump of M_b = 1e10 collapses by z >= 3, or (a) gives M_bound(z 3) >= 1e10
  with seeds common enough, f 1e10 / M_p >= 1e-3. EARLY if z >= 6. 1e9 and 1e11 reported.
- **Primary:** R1, e median, z_on 50, xi 1, eta_f 1, eps 0.1.

## Lane label
- **QUENCH BROKEN**: some non-trivial cell passes G_i and G_ii in primary, both footings.
- **PARTIAL**: in primary, both footings, only one gate has passing (non-trivial) cells.
- **CONDITIONAL**: nothing passes in primary, something passes in a variant or p05.
- **NOT BROKEN**: no cell passes either gate anywhere.
Also reported: R0 map (if R0 passes the same cells, the Newtonian seed effect does it and the law is not needed
there), minimal M_p, minimal f per M_p, min f M_p, and which mechanism sets each boundary.

## Known-answer checks (all must pass for any label)
- **KA1** f = 0: the (b) pipeline reproduces EB1b's stored tables canonical|p05, canonical|med, alt|p05, alt|med:
  same collapse / no-collapse pattern, max |d ln(1 + z_coll)| <= 1e-3 (integrator and drag differ from EB1b's DOP853).
- **KA2** seed-effect scaling: on a radiation + matter test background (all matter clustering, PBH fraction f_pbh
  = 0.01 of matter, rest CDM-like, no drag, no pressure), the linear ODE gives delta_m = f_pbh delta_i (1 + 3 y / 2)
  (i.e. delta ~ f (1 + z_eq) / (1 + z)) to 1e-3 at y = 1, 10, 100.
- **KA3** white-noise top-hat: sigma_p^2 with T = 1 equals M_p / (f M_b) = 1 / N to 1 %.
- **KA4** point seed, EdS, R0, no drag, no pressure: the shell with excess dM / M_b = d turns around at
  delta_lin = 1.0624 and collapses at delta_lin = 1.6865 (delta_lin = (3/5) d a / a_i), both to 1 %.

## MUTATE controls (in-run, must behave as stated)
- **MU1** planted e = 0: (b) at f = 0 reproduces EB1's isolated-sphere R1 table (primary, both footings) to 1e-3 in
  ln(1 + z); (a) M_bound(z 7) with e = 0 >= with e(z) for every M_p, strictly larger for at least one.
- **MU2** planted e = 1e3: R1 reduces to R0, (a) M_bound(z) and (b) z_coll agree with R0 to 1 %; G_ii R1 map = R0 map.
- **MU3** planted no drag: (a) M_bound(z 100) without drag >= with drag, strictly larger for some M_p (drag bites).
- **PB1_MUTATE=1** (env): P_iso multiplied by 0; KA3 must FAIL and the run exits 1 (writes *_MUTATE outputs).

## Limits stated now
Spherical, monochromatic, one seed per shell set, no PBH accretion feedback or heating (both would make binding
harder: a NO is robust, a PASS is not), no PBH mergers, scalar EFE ansatz, R1 is a rule, not the action, and fails
CMB lensing elsewhere. e(z) from a 12.5 h^-1 Mpc mesh is a lower bound on the ambient field.
