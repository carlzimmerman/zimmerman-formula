# CFG510 FROZEN CRITERIA: can the cold energy be primordial black holes?

Committed alone, before any script or machine-computed number. Owner question (2026-10-08): "can the cold energy be
primordial black holes?" Terms: COLD ENERGY = the framework's cold, non-baryonic, collisionless, adiabatic component
(Omega_c/Omega_b = S = 5.364; its mass is required). PBHs need no new particle, which is why the lane matters. kappa = 1/2 is
FITTED; both footings (a0 = 9.36e-11 and 1.13e-10 m/s^2) scored separately, never pooled. Never "theory closed".
Offline only: theory plus numerics on on-disk data. Nothing is downloaded.

## 0. Record read before freezing

| item | what it says |
|---|---|
| L49 D1 (fable_independent_2026/L49_MINIMUM_ADDITION.md, T1/N1) | PBH-like macroscopic cold matter satisfies the cluster spec but is "a realisation of candidate A" and fails N1 identically: with the MOND kernel sourced by the TOTAL potential and an abundance-matched NFW halo at f = 1, median RAR residual -0.259 dex (canonical) / -0.283 (alt) = 1.82x overshoot. It is a DOUBLE-COUNTING failure: the kernel amplifies the added mass. L49 did NOT evaluate PBH mass-window constraints. |
| WORKING_MODEL_SETTLED_PHANTOM (10-06) + CFG423/424 | current picture: ordinary gravity from all real mass; the law sets a TARGET rho_ph[rho_b] read from baryons only; a conserved cold component relaxes to it in bound regions; supply S M_b, edge r_edge = r_M / ln(1/(1-f_b)) = 5.85 r_M |
| CFG461/462/488/490/494/497 | no mechanism supplies settling (temperature, edge, supply, binding cut): settling is a POSTULATE |
| CFG447 | an EFE-blind modified FORCE is excluded by DR3 (7.7 sigma); settling (real mass) is the only consistent ontology |
| CFG474 / CFG428 | cold energy is operationally CDM; the wave-field window is >= 3e-19 eV; one-Bose-field ledger dead |
| CFG472/473 | no pressure gives the target; the arranging mechanism needs an outward force and is nonlocal |
| CFG490 | the direct (phonon) coupling arm violates G9 and delivers only as a rule |
| CFG507 | origin still an input; three mechanisms RESTATEMENT/EXCLUDED |
| on-disk PBH constraint data | NONE (searched: no constraint curves on disk). Every literature bound below is RECALLED and UNVERIFIED; the curves that would verify them need the owner's go (list in section 6) |

## 1. Part A: L49 D1 re-examined in the current picture

- **K1 (control).** Read L49's .out: f = 1 median -0.259 (canonical); 10^0.259 = 1.82 within 0.01. PASS required.
- **A1 (accounting, not a test).** In the settled picture the law reads baryons only, and the settled cold mass IS the
  phantom (mass-conserving, inside r_edge). The predicted RAR is the law's, so the overshoot factor is 1 by construction for
  ANY collisionless cold component that settles. This is scored as "DISAPPEARS BY POSTULATE", never as a pass of a test.
  Verified numerically: on a Hernquist host, g_obs from (baryons + settled cold mass) equals a0-law(g_b) to 1e-6 relative.
- **A2 (collisionless equilibrium, a real test).** Can an ISOTROPIC collisionless population (PBHs have no pressure) sit
  in the phantom? Eddington inversion of rho_ph in the total potential (Hernquist baryons + phantom; both real mass),
  nu_mono(y) = 1/(1 - exp(-sqrt y)), M_b = 1e9, 10^10.5, 10^11.5 Msun, scored a = 0.3 r_M (a = 1 r_M reported), both footings,
  untruncated phantom (primary; the deep phantom is an SIS); truncated at r_edge reported only.
  PASS if f(E) >= -1e-3 max f over binding energies of r in [0.01, 100] r_M in all 6 scored cells.
  Control K2: inversion recovers the Plummer f(E) ~ E^(7/2) to 2%. FAIL of A2 does NOT exclude PBHs: it means the settled
  state needs anisotropy (a condition), stated as such.
- **A3 (PBH-specific dynamics).** Granularity: two-body relaxation time t_rlx = 0.1 N/ln N * t_cross with N = M_cold/m, and
  dynamical-friction sinking time from r = r_h (UFDs) or r_M (discs). m_rlx, m_df = the PBH mass where each equals 13.8 Gyr,
  for the record's MW UFDs (LVD csv, as CFG474) and the three disc hosts. Granularity changes the settled state only if
  m_PBH >= min(m_rlx, m_df). Reported: whether relaxation could itself BE the settling mechanism (only at m >= m_rlx).
- **A4 (route count, qualitative, stated).** Which record settling routes are open to PBHs: superfluid pressure (FL1): no;
  direct phonon coupling (CFG490): no (a black hole carries no baryon/phonon charge, so G9 holds automatically);
  khronon coupling (CFG381 +1): only via black-hole "sensitivities" in khronometric gravity (recalled, NOT computed);
  two-body relaxation: only above m_rlx.
- **Part A verdict.** "RESOLVED" requires a supplied settling mechanism. Under the postulate alone the x1.82 is
  "DISAPPEARS CONDITIONALLY (settling postulate)" if K1, A2 (or its anisotropic condition) and A3 (granularity irrelevant
  in the open window by >= 3 dex) hold; "SURVIVES" if A3 shows granularity in the window forces the halo off the phantom.

## 2. Part B: the mass window for f_PBH = 1 (monochromatic)

- **Band table (RECALLED, UNVERIFIED; f = 1 excluded).** Robust set:
  E1 evaporation (CMB anisotropy, extragalactic gamma, Voyager e+-, 511 keV) M < 1e17 g;
  E2 HSC/M31 microlensing 1e22 g - 1e-6 Msun; E3 EROS/MACHO 1e-7 - 30 Msun; E4 OGLE 1e-6 - 1e-2 Msun;
  E5 UFD/star-cluster heating >= 5 Msun; E6 wide binaries >= 30 Msun; E7 CMB accretion (spherical) >= 100 Msun;
  E8 LVK merger rate 0.5 - 300 Msun; E9 Lyman-alpha Poisson >= 60 Msun; E10 disc heating / dynamical friction >= 1e6 Msun;
  E11 incredulity/one-per-volume >= 1e21 Msun (ceiling of the grid).
  Maximal set (adds claimed/contested extensions): evaporation to 4e17 g; HSC lower edge 3e21 g; CMB disc accretion >= 1 Msun.
  NOT scored (retracted or disputed): GRB femtolensing; white-dwarf / neutron-star capture.
- **Open window.** Grid 1e10 g - 1e55 g at 0.01 dex; open = not inside any band. Window VIABLE needs >= 1 dex contiguous on
  both sets.
- **Derived cross-checks (D-checks).** D1 Hawking lifetime and temperature (naive photon-graviton formula, stated);
  D2 microlensing lower edge from wave optics (w = 8 pi G M/(c^2 lambda) = 1 at r-band) and finite source (R_E in source plane
  = R_sun, D_ls 50 kpc); D3 UFD heating bound computed from the record's UFDs (settled ontology: all M_dyn - M_b is real
  cold mass; dsigma^2/dt = 4 sqrt2 pi G^2 rho m lnL / sigma, lnL = 10, t = 10 Gyr; band edge = median over cold-dominated
  resolved UFDs); D4 LVK rate at f = 1 from the Sasaki-type formula (recalled, flagged) with a 1e-3 suppression;
  D5 Poisson isocurvature on CMB scales. Rule: a D-check disagreeing with its recalled edge by > 1 dex flags that band
  "UNSUPPORTED BY DERIVATION" (never silently removed or moved).
- **Framework-specific modifications (computed).** FM1: dynamical bounds use real mass in the settled ontology (no force
  relief; CFG447). FM2: microlensing optical depth to the LMC and to M31 for settled-phantom halos (truncated at r_edge +
  smooth unsettled reservoir at the cosmic mean) vs NFW (MW M200 1e12, M31 1.5e12, c = 10; recalled); if the ratio is in
  [0.5, 2] the microlensing bands are unchanged, else the band edges are flagged. Local cold density at the Sun (spherical;
  phantom disc NOT computed) reported for wide binaries.

## 3. Part C: formation and the amount

- Required beta (formation fraction) for f = 1, gamma = 0.2, g* = 106.75; sigma from Press-Schechter erfc with
  delta_c in {0.41, 0.45, 0.55}; P_zeta = (81/16) sigma^2 (recalled radiation-era factor); k at horizon entry.
- Compatibility: COMPATIBLE if the spike's k > 1e5 /Mpc (beyond CMB/LSS k <~ 1 and mu-distortion 1 - 1e4 /Mpc, recalled) and
  CMB-scale Poisson isocurvature < 1e-3 of A_s = 2.1e-9.
- Tuning: d ln f_PBH / d ln P_zeta, and the fractional precision on P_zeta that holds Omega_c h^2 within its 1% Planck error.
- **AMOUNT verdict:** PREDICTIVE only if the spike amplitude (or location) is fixed by something other than the demand
  Omega_PBH = Omega_c, with no new free constant. Otherwise RESTATEMENT. Formation temperature vs baryogenesis reported.

## 4. Part D: distinctive predictions (computed where possible)

Scalar-induced GW peak frequency and Omega_GW h^2 for window masses (vs LISA ~1e-12, recalled); Hawking tail of a
critical-collapse mass function (recalled form, gamma_c = 0.36) below 1e16 / 1e17 g; T_H; Solar-System flyby rate within
1 AU and impulse; microlensing wave-optics edge. Flagged recalled numbers throughout.

## 5. Overall verdict rule

- **EXCLUDED** (name the constraint) if no >= 1 dex open window exists in the robust table.
- **VIABLE** only if a window exists on both sets AND Part A is RESOLVED (a supplied mechanism). None is on the record, so
  VIABLE is not expected; that is stated now.
- **VIABLE-CONDITIONAL** otherwise, with every condition listed (settling postulate; recalled bounds; spike; any A2 anisotropy).
- AMOUNT: PREDICTIVE or RESTATEMENT per Part C.
- **MUTATE (`CFG510_MUTATE=1`):** (i) the scorer evaluated at 1 Msun, 1e-9 Msun, 1e15 g and 1e4 Msun must return EXCLUDED at
  each; (ii) the HSC lower edge moved to 1e17 g must close the window and return EXCLUDED overall. Both required; exit 1 if
  detected. Main run exits 0 iff controls K1, K2 pass.

## 6. Needs the owner's go (downloads; not done)

Constraint curves to replace the recalled bands: Carr, Kohri, Sendouda & Yokoyama 2021 review (arXiv:2002.12778) and Green &
Kavanagh 2021 (arXiv:2007.10722) compilations; HSC (Niikura+2019; Smyth+2020); EROS-2 (Tisserand+2007); MACHO; OGLE
(Niikura+2019b; Mroz+2024); Brandt 2016; Tyler+2023 (already cited in the citations index); Ali-Haimoud & Kamionkowski 2017;
Serpico+2020; LVK GWTC-3 rates; Laha 2019 / Boudaud & Cirelli 2019; Murgia+2019. Also the PBHbounds public compilation.
