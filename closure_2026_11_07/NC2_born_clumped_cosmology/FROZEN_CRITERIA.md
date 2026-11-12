# NC2 frozen criteria: cosmology of born-clumped cold dark energy (FRAMEWORK_CANDIDATE_2, lane NC2)

Frozen before any NC2 script or NC2 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane. Name: cold
dark energy (the component QX15 needs), never dark matter; no particle; no LCDM parameter values (backgrounds are QX15's
footing fits). Both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), never pooled. One thread per job, RSS < 1 GB,
no downloads (QX15's and P1D3's data are already on disk, owner-approved 11-06 / 10-27). Gates may be built by subagents;
every number in RESULT.md comes from committed scripts.

## 0. The object (candidate 2, sections 3-4)

- The cold component at QX15's mean abundance (each footing's main fit; R = omega_d/omega_b; R 5.562 is the QX12 native value
  quoted by the candidate) is born, before recombination, concentrated in clumps at future cluster/group nodes and absent
  elsewhere. Nothing removes it later; it is collisionless and gravitates.
- **Clump parameters (declared brackets, no fit):** component mass per clump M_cl in {1e13, 1e14 (primary), 1e15} Msun
  (groups to X-COP); comoving clump radius r_cl = Lagrangian radius of M_cl (1 + 1/R) at the mean matter density
  (gentlest; a collapsed clump is smaller and gives more small-scale power); fraction of the component in clumps f_in = 1
  primary (candidate: "absent where field galaxies form"); the f_in each gate tolerates is reported. NC1's clump spectrum
  replaces the M_cl brackets if it has landed when the gates run (stated in RESULT.md either way).
- **Large-scale readings of the clump field at birth (the component's isocurvature content S = delta_c - (3/4) delta_gamma
  on the primordial slice):**
  - **Z (the candidate's R2, bias b):** a fully correlated, scale-invariant CDI mode such that the cold component's density
    contrast at z_rec = 1090, k_p = 0.05 Mpc^-1 is b times the adiabatic-only value (b operationally defined there; sign
    and amplitude found from the CAMB transfer). b in {1, 1.2, 1.5, 2}; the tolerated b found by bisection on the line
    below.
  - **P (Poisson clumps):** clump positions uncorrelated with the adiabatic mode; P_S(k) = f_in^2 |u(k r_cl)|^2 / n_cl,
    n_cl = rho_c / M_cl, u = top-hat window. Uncorrelated with the adiabatic mode.
  - **C (compensated: the component rearranged locally, mass and momentum conserving):** P_S(k) = f_in^2 |u(k r_cl)|^2 min(1, (k r_cl)^4) /
    n_cl (the k^4 low-k tail of a local rearrangement). Uncorrelated.
  - **Implied b (peaks):** a population at future cluster nodes has n_cl(x) = n_cl [1 + b_L delta_L0(x)], b_L the
    Sheth-Tormen Lagrangian bias at nu = 1.686/sigma(M_cl (1 + 1/R), z = 0) on the footing fit's own linear power. The
    implied b at recombination = 1 + b_L delta_L0(k_p) / delta_c,ad(z_rec, k_p) (the clump modulation is primordial and
    does not wait for growth). Reported per M_cl; also b_L and 1 + b_L.

## 1. Gates

| Gate | Statistic | Line | Source |
|---|---|---|---|
| G1 primary CMB (R2 / K1) | QX15's grader (qx15_like.grade_spectra, P full CamSpec cut + ACT, PA) on CAMB spectra at each footing's main fit; for P and C: lensed adiabatic + unlensed isocurvature (iso lensing neglected, disclosed); for Z: CAMB's own mixed initial vector, lensed. Delta = chi^2_PA(model) - chi^2_PA(QX15 main). A short refit (5 params, Nelder-Mead <= 120 evaluations from the main fit) is run only when the no-refit Delta lies in 4-200 | QX15's cell rule: Delta <= 4 PASS, 4-25 TENSION, > 25 FAIL (no-refit Delta <= 4 is a PASS; a refit can only lower it) | QX15 |
| G2 CMB lensing L <= 400 (corrected kernel) | (a) the mean component: PR4 chi^2 (QX3 iter2's best_amp_chi2, A_s refit) of the lensing potential from CLASS at each footing's main fit; (b) the clumps: S(L) = C_L[P_tot]/C_L[P_ad] with GL1's limber_n at n = 4, P_tot = P_ad,lin + P_cl, P_cl(k) = f_in^2 f_c^2 |u|^2 / n_cl (comoving Poisson, constant in time; f_c = R/(1+R)); chi^2 of X_CLASS x S | chi^2 <= 18.48 AND Delta chi^2 (vs (a)) <= 4 | QX3 / GL1 |
| G3 forest 1D power z 2-4 (R6 / K2) | P1D3's DESI DR1 P1D table and covariance (755 bins, z 2.2-4.4; loader read-only, md5 as P1D3's S0a). The native forest model cannot fit the null (P1D1-P1D3: NOT DIAGNOSTIC), so the gate grades the RATIO: r(k, z) = P1D_NC / P1D_uniform of the linear 1D matter power (k_par in DESI's bins, s/km -> Mpc^-1 via the footing H(z)), and Delta chi^2_Asimov = d^T C^-1 d with d = (r - 1) x P1D_data. Two brackets of the clumped matter field: (i) linear + clumps: P_NC = P_lin [f_b + f_c (1 - f_in) + f_c f_in W(k)]^2 + P_cl, W(k) = |u(k r_cl)| (the component's own adiabatic small-scale power exists only through the clumps); (ii) inter-clump sightlines: the gas outside clumps grows on baryons alone after decoupling (D ∝ a^p, p = (sqrt(1 + 24 f_b,loc) - 1)/4 with the local matter = baryons, from z_dec 1090), P_NC = P_b,inter | Delta chi^2_Asimov <= 4 PASS, 4-25 TENSION, > 25 FAIL on BOTH brackets for a FAIL; also reported against L365's 10 % band | P1D3, L365 |
| G4 mu distortion | mu = int dln k Delta^2_S,eff(k) W_mu(k), W_mu(k) = 2.27 [exp(-(k/1360)^2 / (1 + (k/260)^0.3 + k/340)) - exp(-(k/32)^2)] (Chluba's adiabatic window), with the clump isocurvature power treated as if adiabatic (an upper bound: CDI heats photons only through potentials) | mu <= 9e-5 (FIRAS 95 %) AND the fraction of the clump power's mu integrand below k 50 reported (the candidate's "null below k 50") | FIRAS |

## 2. Labels

- Per gate x reading x M_cl x footing: PASS / TENSION / FAIL / NO VERDICT (a KA or MUTATE fails).
- **NC2 PASS** only if G1-G4 all pass at the primary (M_cl 1e14, f_in 1) under at least one large-scale reading that the
  candidate can claim (Z at the implied b, or P, or C). **K1 (R2) is triggered** if G1 fails at the implied b under Z and
  under P and C. **K2 (R6) is triggered** if G3 fails on both brackets. The f_in and M_cl each gate tolerates are reported.

## 3. Known answers

- KA1 (QX15): the grader at each footing's main fit with the plain adiabatic CAMB spectra reproduces qx15.json's chi^2_PA
  (3741.08 / 3741.15) to 1e-2.
- KA2 (GL1): limber_n at n = 4 with R = 1 gives S = 1; on the QX3 iter2 worst corner it reproduces GL1's shape row
  (1.005 / 1.006 / 1 / 0.991 / 0.984 / 0.980) to 1e-3; n = 0 reproduces iter2's limber_ratio exactly.
- KA3: G3's loader gives 755 bins and P1D3's md5; with f_in = 0 (uniform), r = 1 to 1e-12 and Delta chi^2 = 0.
- KA4 (CDI convention, reported, not graded): CAMB's pure CDI mode with the same primordial table as the adiabatic run
  gives C_10,iso / C_10,ad within a factor 1.5 of the Sachs-Wolfe ratio (2 f_c)^2, f_c = omega_c/omega_m (Theta_SW = -zeta/5
  adiabatic, -(2/5) f_c S isocurvature). It fixes the scale convention of P_S used by readings P and C.

## 4. MUTATE (separate outputs *_MUTATE.*; each must bite)

- M1 (R19): large-scale isocurvature at the same amplitude: the clump field's P_S at k_p = 0.05 placed in a scale-invariant
  (n_iso = n_s) uncorrelated CDI mode must FAIL G1 (Delta > 25).
- M2: a uniform component (f_in = 0, b = 1) must reproduce QX15 (KA1) and pass G1-G4.
- M3 (forest): f_in = 1 with r_cl x 0.1 (collapsed clumps) must FAIL G3 bracket (i).

## 5. Outputs

nc2_*.py write nc2_*.json / .out (and *_MUTATE.*). RESULT.md: gate x reading x M_cl x footing table, tolerated b and f_in,
kill lines triggered. Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
