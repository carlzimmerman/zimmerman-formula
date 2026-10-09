# CFG513 FROZEN CRITERIA: the Milky Way's own cold-energy profile, and where an NFW assumption biases MW-based measurements

Written and committed alone, before any script of this lane exists and before any number of this lane is computed.
Seen before freezing (mental arithmetic only, disclosed): r_M = sqrt(G M_b/a0) is about 30 kpc for M_b = 6e10 (canonical);
the f_ret = 1 edge is then about 5.85 r_M = 175 kpc and the f_ret = 0.18 edge about 30 r_M = 900 kpc; the deep-law flat
speed (G M_b a0)^(1/4) is about 165 / 173 km/s. The record's numbers read while designing are cited by lane below.

kappa = 1/2 is FITTED. Both footings everywhere: canonical a0 = 9.36e-11, alt a0 = 1.13e-10 m/s^2. No dark-matter particle: the
cold energy's MASS is still required. Nothing here may be reported as "theory closed" or as the data favouring the framework.
On-disk data and offline computation only; no downloads. The Gaia DR4 preregistration files are READ ONLY (never edited).

## 1. The framework's Milky Way (construction declared)

- **Kernel:** nu_mono, the record's committed table (CFG4_common / CFG7_common, exec'd read-only).
- **Baryons (the record's):** M_b = 6.0e10 Msun primary (FG001 / CFG42 / CFG286 `MW_MB`); 7.3e10 census-high (CFG286) as variant.
  Component shapes from L172 (fable_independent_2026/L172_mw_outer_curve_and_fgal_ledger.py): Hernquist bulge (a = 0.7 kpc),
  exponential stellar disc (R_d = 2.6 kpc), exponential gas disc (R_d = 6.0 kpc), in L172's mass ratios 1.0 : 4.5 : 1.2,
  rescaled to the total M_b (6.0e10 -> bulge 0.896e10, disc 4.03e10, gas 1.075e10).
- **In-plane rotation curve:** V_c^2 = R nu_mono(g_N/a0) g_N with g_N the exact thin-disc (Bessel) + Hernquist midplane field.
- **Spherical profile (the cold-energy profile):** spherical baryon enclosed mass M_b(<r) (Hernquist exact; discs by the cylindrical
  enclosed fraction 1 - (1 + x) e^-x, x = r/R_d); g = nu_mono(G M_b(<r)/(r^2 a0)) G M_b(<r)/r^2; M_dyn(<r) = g r^2/G;
  phantom M_ph(<r) = M_dyn - M_b(<r) = the settled cold energy (candidate B); rho_ph = dM_ph/dr / (4 pi r^2).
- **Edge (PAPER45, zero knob):** cold supply M_cold = M_b (1 - f_b)/(f_ret f_b) with (1 - f_b)/f_b = 5.364 (CFG390); the edge
  r_edge solves M_ph(<r_edge) = M_cold (point-mass limit r_M/ln(1 + f_ret f_b/(1 - f_b)) = 5.85 r_M at f_ret = 1). Beyond the edge the
  cold energy is exhausted: M(<r) = M_b + M_cold (Keplerian); the catchment draw leaves no extra cold mass between r_edge and 500 kpc.
  **f_ret = 1** (PAPER45's self-consistent value) and **f_ret = 0.18** (the record's census, all collapsed phases; CFG365/CFG390)
  are both run and never pooled. **Bare law** (no edge; the reading CFG286/CFG433/CFG463 used) is run as the record's reference.
- **Ownership (FG001):** only the outermost bound system carries the phantom; no external-field effect (PAPER44).
  O-MW: the MW owns its phantom to its edge. O-LG: the Local Group (MW 6.0e10 + M31 1.2e11, CFG286) is the outermost bound system;
  then the MW-centric spherical profile is defined only inside the deep-law field-equality point toward M31,
  r_split = D sqrt(M_MW)/(sqrt(M_MW) + sqrt(M_M31)) with D = 780 kpc (FP11 / CFG30); radii beyond r_split are flagged as LG-owned.
  Profiles are tabulated 0.1-500 kpc.

## 2. NFW comparison halos (all with the same baryons, Newtonian)

- **N-F (the shape reference):** NFW (log M200c, log c free; rho_crit at h = 0.674) fitted to the framework's own in-plane V_c at the
  Ou+2024 radii (on disk, real_research/data/mw_rc_ou2024_table1.tsv) with Ou's random errors in quadrature with their stated systematic
  (3% at R <= 22 kpc, 15% beyond). This is what an RC analysis that assumed NFW would infer if the framework were true.
  **N-F+T:** the same plus two tracer constraints, the framework's own M(<50) and M(<100 kpc) with 15% errors (declared typical; recalled).
- **N-D (reported):** the same NFW fit to the Ou+2024 data themselves. The framework's own chi^2 against Ou+2024 and Eilers+2019
  (both on disk) is reported, with no fitting (a TEST, not a bias).
- **Literature (recalled, unverified; labelled as such in every output):** N-std M200c = 1.0e12, c = 10; N-McM McMillan 2017
  (rho_s = 0.00854 Msun/pc^3, r_s = 19.6 kpc); N-B08 / N-B16 the Bovy 2015 MWPotential14-class halo (r_s = 16 kpc) with
  M_vir = 0.8e12 / 1.6e12 as Fritz+2018 used (taken as M200c here); Eilers+2019 NFW M_vir 7.25e11 (reported only).

## 3. The bias metric and the verdict rule

For each measurement Q: **bias b_Q = (Q_assumed-NFW - Q_true-framework)**, expressed as a fraction of Q_true and in units of that
measurement's quoted error sigma_Q (on disk where available; otherwise recalled, unverified, and labelled).
**Verdict per measurement:** **MATERIAL BIAS** if |b_Q| > sigma_Q; **MINOR** if 0.3 sigma_Q < |b_Q| <= sigma_Q; **NONE** if
|b_Q| <= 0.3 sigma_Q. For object samples (satellites): MATERIAL if the median |b|/sigma > 1; MINOR if the median is 0.3-1 or >= 25%
of objects exceed 1 sigma; NONE otherwise. The verdict is computed per footing x f_ret (x M_b where stated); the row's headline is the
worst cell, and the cell range is printed. "Both directions": the reverse (NFW true, framework assumed) is the same |b| with the sign
flipped unless stated; where the reference changes (fitted quantities), the reverse is computed explicitly.

## 4. The measurements (each computed in the script; quoted-error source in brackets)

- **(a) Satellite orbits.** Fritz+2018 Gaia DR2 (on disk, _external_data/cfg433_work/src/UFDsmot_arx_final.tex, Tables 2 and 3;
  galactocentric distance from the on-disk LVD where the name maps). Pericentre and apocentre from the energy and angular momentum in
  a static spherical potential (exact turning points). Assumed: N-B08 and N-B16 (Fritz's own potentials). True: framework profiles.
  sigma = Fritz's quoted peri errors (Table 3, same potential). Also: the record's bare law vs the edge (the bias CFG433/CFG463/CFG286
  inherit from using the bare law), first-infall flags (apo > 300 kpc or unbound), and the radial period.
- **(b) MW mass.** (b1) M(<50), M(<100), M(<200), M(<300) and M200c inferred by N-F and N-F+T vs the framework's true M(<r) and its
  total (M_b + M_cold) [sigma: 15% for M(<r <= 100), 20% for M200 (recalled review ranges)]. (b2) Local Group timing: radial first
  approach from d = 0 at t = 0 to d = 780 kpc at t0 = 13.80 Gyr (CFG7_common) with relative acceleration -G[M_MW(<d) + M_M31(<d)]/d^2
  (+ Omega_L H0^2 d; with and without Lambda), M31 with the same rule; the framework's predicted v_r vs the measured -109.3 +- 4.4
  (on disk, FP11/CFG30), and the Kepler timing mass a point-mass analysis infers from the measured v_r vs the framework's true
  M_MW,tot + M_M31,tot. This is a TEST row as well as a bias row; a failure is reported as a failure.
- **(c) Local cold-energy density at the Sun (R0 = 8.178 kpc).** Framework spherical rho_ph(R0); framework midplane estimate
  (nu - 1) rho_b,mid (phantom disc; algebraic QUMOND at the midplane) and the slab-equivalent (nu - 1) Sigma_b(|z| < 1.1 kpc)/2.2 kpc
  with scale heights 0.3 kpc (stars) and 0.1 kpc (gas) declared. Assumed: N-F rho(R0) [sigma 20%, recalled].
- **(d) Wide binaries / Gaia DR4.** READ the prereg and amendments (never edit). Compute: the Galactic tide at the Sun with and
  without the phantom disc vs the prereg's Arm C statement (1.6-2.6e-31 s^-2; tide/internal about 3e-4 at 30 kAU); y_extN at the Sun
  from the framework baryon model vs the frozen values (g_ext 1.778e-10 primary / 2.078e-10 alt); the shift in each Arm's predicted
  gamma_v that the MW model could cause [sigma_tot = 0.1614/5.8 = 0.0278, derived from the prereg's own Arm A row].
- **(e) Microlensing optical depth.** LMC (l = 280.46, b = -32.89, D = 49.97 kpc) and SMC (l = 302.8, b = -44.3, D = 62 kpc)
  [recalled], the halo tau for framework profiles vs N-F and the recalled MACHO S-model (cored isothermal rho0 = 0.0079 Msun/pc^3,
  r_c = 5 kpc, R0 = 8.5); bias of an inferred compact-object halo fraction f proportional to tau_model ratio [threshold 25%, the
  quoted halo-model systematic, recalled]. Bulge (Baade's window) halo contribution reported.
- **(f) Streams.** V_c at GD-1 (r = 14 kpc), Pal 5 (19 kpc), Orphan (40 and 60 kpc), Sgr (100 kpc): N-F vs framework [sigma 2%
  for V_c (recalled stream precision)]. The effective flattening of the non-baryonic force at r = 14 kpc, 45 deg, algebraic QUMOND
  from the thin-disc Hankel field: q^2 = (z/R)(g_R/g_z) of the phantom part vs spherical NFW q = 1 [sigma_q 0.05, recalled].
- **(g) Solar system.** The difference in the Galactic tidal tensor at the Sun (framework incl. phantom disc vs N-F) against Cassini's
  Q2 = (3 +- 3)e-27 s^-2 (on disk, PAPER44); the vertical tide 4 pi G rho_0,total change for the detached-TNO / Oort secular models.
- **(h) EFE-rival host field.** g_ext(r) = V_c^2/r at 50/100/200 kpc, N-F vs framework; the shift in the EFE rival's deep-regime
  satellite dispersion, Delta log sigma = -1/2 Delta log g_ext [sigma 0.1 dex, recalled typical dwarf dispersion error].

## 5. Decisive-test flags

Each bias row states whether it touches DR4 (Arms A/B/C, settling Amdt 21), the satellites (CFG433, CFG463, CFG286), the UFDs, or the
no-EFE claims (PAPER44). A MATERIAL bias on any of these is flagged in the README headline.

## 6. Controls (load-bearing)

- C1: nu_mono point-mass edge equals r_M/ln(1 + f_ret f_b/(1 - f_b)) within 1% (deep regime; f_ret = 1 and 0.18).
- C2: the spherical profile's M_dyn at 200 kpc (bare law) equals the point-mass law within 1%; rho_ph >= 0 everywhere inside the edge.
- C3: the Kepler timing integrator reproduces the analytic radial Kepler solution (no Lambda) to 1e-4 in t0.
- C4: N-B08 / N-B16 orbits reproduce Fritz Table 3 central pericentres: median |Delta peri|/peri <= 15% for each potential.
- C5: the N-F fit recovers a known NFW + baryons curve (synthetic) to 1e-3 in M200c and c.
- C6 (reported): CFG484's host-fluid density at R0 (0.0049 / 0.0057 Msun/pc^3, P2 point mass) reproduced within 5% by the same formula.
- C7 (reported): deep-MOND two-body timing at FP11's nominal baryons is within 10% of CFG30's -175 / -191 km/s.

## 7. MUTATE (CFG513_MUTATE=1, separate outputs *_MUTATE.*)

The "true" profile in every row is replaced by the assumed NFW of that row (for N-F rows: N-F itself, refitted). Every bias must be
zero: |b| <= 1e-6 relative for direct rows and <= 1e-3 for refitted rows, and every verdict NONE. Any non-zero bias fails MUTATE.

## 8. Outputs

`cfg513_mw_profile.py` -> `cfg513.out`, `cfg513_results.json`, `cfg513_profiles.csv`, `cfg513_profile.png`; MUTATE ->
`cfg513_MUTATE.out`, `cfg513_results_MUTATE.json`. README with the bias table. Local commit only; nothing pushed.
