# KL1 FROZEN CRITERIA: which survey and comparison assumptions carry form B's weak-lensing amplitude gap

Committed alone, before any KL1 script exists and before any KL1 number is computed.
TEST lane. Relabels nothing, adopts nothing, is not registered. **kappa = 1/2 FITTED; not theory closed.** Footings canonical
(a0 9.3603e-11) and alt (1.1312e-10 m/s^2) are graded separately, never pooled. The component is cold dark energy, a gravitating
field component, never a particle. CO2's label (AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA as frozen, TENSION once the reference
run's realisation is corrected) is not changed by this lane. Lane id KL1 checked free (`ls`, `git log --all --grep KL1`) on
2026-11-10.

## 1. Why

CO2 (`closure_2026_11_09/CO2_form_b_amplitude_pinned/`, criteria 2bd776c60d) pinned form B's amplitude with Planck 2018 low-L EE
(sigma8 0.8271) and found raw KiDS-1000 xi+- best at sigma8 0.736 +- 0.016 for form B's spectrum, 5.1 to 5.8 KiDS widths below
the pin; P4 chi^2 157.89 / 159.35 on 104 points, p 0.0026 / 0.0021. The owner (2026-11-10, relayed by the closure chat) asked
which assumptions of the people who reduced the data, or of ours in the comparison, carry the gap, and what is left when each is
replaced by what the framework or newer data supports, looking just as hard for assumptions that make it worse.

## 2. Machinery (inherited, executed unchanged unless a row below changes one named thing)

- CFG592's library part (`campaign_fresh_gravity/CFG592_cosmic_shear_likelihood/cfg592_native.py`, everything above
  `# --- run`), executed as CO2's `co2_shear.py` executes it: projection, Hankel transforms, survey loaders (published cuts),
  nuisances and priors (KiDS: five correlated delta-z with KiDS-1000's SOM covariance + one alignment amplitude; DES: four
  delta-z, four shear biases, alignment amplitude and redshift power), the support mask (point kept if >= 0.9 of its absolute
  integrand lies inside the run's [k_lo, k_hi]), the L-BFGS-B fit with its two starts.
- CO2's model: CFG596's gravity-only S0 run (one 100 Mpc/h box, 1024^3) x R_tot (CO1's `co1_hm.json`, form B's layout), moved
  from the engine's sigma8 0.811 to a target sigma8 by the run's own response alpha(k) (CO2 section 3, unchanged).
- p = chi^2_data survival at N, as CO2. Lines (CO2's, unchanged): p >= 0.05 CONSISTENT; 0.0027 <= p < 0.05 TENSION;
  p < 0.0027 EXCLUDED AT 3 SIGMA.
- Best sigma8 and width: CO2's rule (chi^2 total on the grid 0.70 to 0.90 step 0.0125, parabola through the five points around
  the minimum, width = Delta chi^2 = 1). If the minimum is at a grid edge the grid is extended by 0.0125 steps (at most to 0.60 /
  1.00). Gap = (target sigma8 - best) / width, with Delta chi^2 (target minus best) beside it.
- KL1 needs its own copy of the fit (for a replaced covariance and the alignment variants). It must reproduce CFG592's `fit`
  exactly when nothing is replaced (KA0).

## 3. Known answers (all before any row is graded; a failed KA makes the rows that use it NO VERDICT)

- **KA0** (CO2 replayed through KL1's code): P4 chi^2 157.89 / 159.35 (0.01); KiDS best sigma8 0.7358 / 0.7341 (0.0005) with
  width 0.0162 / 0.0161 (0.0005); DES Y3 at the pin 74.69 / 74.67 (0.01); N = 104 KiDS, 52 DES.
- **KA1** (A1 harness): (i) KL1's patched theory with the neutrino mass set to 0 and no neutrino term in h reproduces CO2's stored
  PA at CO2's pinned parameters (0.1) and its exact chi2_E (0.01); (ii) CLASS sigma8 with one 0.06 eV neutrino at CO2's pinned
  parameters reproduces CO2's bracket 0.8152 (0.0005).
- **KA2** (A2 covariance): at the fiducial (section 5), with the effective area fitted as in A2,
  (i) over the published-kept points where my noise term is >= 0.8 of my Gaussian diagonal, the 16th to 84th percentile range of
  published / mine lies inside [0.85, 1.15];
  (ii) over the published-kept points where my noise term is < 0.5 of my Gaussian diagonal, the median of published / mine lies in
  [0.95, 1.6] and no point is below 0.80 (published may exceed a Gaussian covariance through non-Gaussian, super-sample and
  shear-bias terms; it must not fall well below it);
  (iii) reported, not a gate: the fitted area beside the survey's own quoted effective area (quoted as context), and the median
  |r_pub - r_mine| of the correlation coefficients over the kept points.
  If (i) or (ii) has fewer than 5 points it reads NOT EVALUABLE, and a post hoc amendment must say how to swing harder before A2
  is graded.
- **KA3** (A3 gas): (i) with f_ret = 1 everywhere and no extra grid points the modified layout returns CO1's stored R_tot to
  1e-9; (ii) with f_ret = 1 and the inserted grid points, to 2e-3 relative, max over k <= 10 h/Mpc; (iii) every modified layout
  conserves M(<r_ta) = M_ta to 1e-9 and is non-decreasing.
- **KA4**: CO2's response check (KA5 there) reproduced: median raw alpha below k 0.12 within 0.15 of 1 at each node.

## 4. Rows, in this order. A1 is the baseline for A2 to A5; then all together.

Each row reports, per footing and per data set (KiDS-1000, DES Y3): chi^2 (with prior, as CO2 quotes), chi^2_data, N, p, label by
CO2's lines, the survey's best sigma8 with width, the gap in widths and Delta chi^2. For KiDS also the delta-z pulls (fitted
uncorrelated shifts minus their prior means, in prior widths) at the target and at the best sigma8.

**A0. CO2 as graded** (= KA0).

**A1. The neutrino floor (baseline for A2 to A5).** Oscillation experiments require a summed mass of at least about 0.059 eV; the
floor is one massive neutrino of 0.06 eV (2.046 massless).
- Refit: CO2's `co2_fit.py` objective (F1A's PA + Planck 2018 SimAll low-L EE, the interpolated table for the optimiser, the
  exact lookup reported) with F1A's CAMB call replaced by the same call with `mnu=0.06, num_massive_neutrinos=1, nnu=3.046`,
  and the canonical footing's h rule extended by the neutrino density today, h^2 = w + omega_b + omega_d + omega_r + omega_nu,
  omega_nu = 0.06 / 93.14 (the alt rule h^2 = w is unchanged). F1A's bounds and simplex steps; Nelder-Mead, at most 250
  evaluations per start; starts (a) CO2's pinned theta, (b) the same with tau 0.058 and ln 1e10 A_s raised by 2 (0.058 - tau).
  The lower total is the refit.
- Target sigma8 = CLASS sigma8 (total matter) at the refit with the neutrino, as `co2_rows.class_B(pr, nu=True)`.
- Reported: the refit's PA and chi2_E against CO2's pinned fit (the neutrino must not cost the CMB fit more than 9 in total;
  if it does, A1 is flagged PINNED FIT INADEQUATE WITH THE FLOOR and A2 to ALL still run, flagged); tau, ln A_s, omega_d.
- Reported variant A1s (not graded): the linear shape of the neutrino suppression on top of the sigma8 move, the factor
  [P_lin,nu(k) / P_lin,0(k)] x (sigma8_0 / sigma8_nu)^2 at z 0 from CLASS at the refit (massless twin: the same parameters with
  N_ur 3.046), applied at every node.

**A2. The covariance at the model.** Both published covariances are analytic and evaluated at the survey's fiducial; their
signal terms scale with the signal. For a goodness-of-fit p of a model, the covariance should be the model's.
- My Gaussian covariance G(model), for all published xi+- points of the survey (270 KiDS, 400 DES), from the model's own
  tomographic C_ell (nominal delta-z, no alignment):
  Cov_pq = 1 / (2 pi A) sum_ell ell d(ell) Jbar_p(ell) Jbar_q(ell) [C^ik C^jl + C^il C^jk + C^ik N^jl + N^ik C^jl + C^il N^jk +
  N^il C^jk] + delta_(same theta bin, same sign) (delta_ik delta_jl + delta_il delta_jk) 2 s_i^2 s_j^2 / (n_i n_j A Omega_bin),
  with Jbar the bin-averaged J0 (xi+) or J4 (xi-) on CFG592's fine ell grid and sub-bin rule, N^ij = delta_ij s_i^2 / n_i, s_i and
  n_i the per-component shape noise and effective density in each survey's FITS header (KiDS NZ_SOURCE SIG_E_i / NGAL_i; DES
  nz_source SIG_E_i / NGAL_i), Omega_bin = pi (theta_hi^2 - theta_lo^2) of the published bin, no pure-noise term between xi+ and
  xi-. Every Gaussian term scales as 1 / A.
- Area: A is fitted once per survey so that the median of published / G(fid) over the noise-dominated points (my noise >= 0.8
  of my Gaussian diagonal, published-kept) is 1.
- Fiducial: form B's spectrum at the survey's own best sigma8 from row A0 (the published covariance was evaluated at a cosmology
  that fits its own data, so its signal level on these points is the best-fit level). Reported edges: fiducial sigma8 +- 0.02.
- The rest R = C_pub - G(fid) (non-Gaussian, super-sample and shear-bias terms, plus whatever my Gaussian misses) is scaled point
  by point: R_pq (s_p s_q)^(gamma / 2), s_p = xi_model(p) / xi_fid(p) at nominal nuisances, no alignment, clipped to [0.5, 3].
  **Graded: gamma = 2** (super-sample and shear-bias terms go as the signal squared). Two-edged bracket, reported: gamma = 0
  (rest held at the published fiducial) and gamma = 3 (rest steeper than the signal squared, as a halo trispectrum).
- C(model) = G(model) + R (s s)^(gamma/2), subset to the kept points. If it is not positive definite the row reads NO VERDICT.
- The graded p uses C at the target. The scan uses C at each grid sigma8 (chi^2 only). Reported beside it: the scan with
  ln det C(sigma8) added (the full Gaussian likelihood), which penalises high amplitude.

**A3. The gas where RB1 measured it.** RB1 (`closure_2026_11_09/RB1_form_b_hot_systems/`) measured on raw X-ray data that groups
hold 0.60 of form B's expected baryons inside R500, rising with depth (slope +0.160). CO1's layout keeps every baryon of a group or
cluster inside R200c.
- Scope: CO1's group / cluster regime only (v_vir > v_stiff). The galaxy regime already spreads its uncondensed baryons over the
  Lagrangian region and is unchanged.
- f_ret(M500), primary: RB1's 176-system ladder with KVM18 stars (`rb1.json`, gate2 extended_GS4 median_fret_gas_by_mass, kvm
  column): 0.674, 0.592, 0.800, 0.920, 1.095 at log M500 [Msun] 13.25, 13.75, 14.25, 14.75, 15.25, linear in log M500 between,
  held at the end values outside, capped at 1 (B's ceiling). Bracket (reported): slope +0.160 through (13.75, 0.592), capped at 1.
- M500 from the layout's own M(<r) (500 times the critical density, rho_c = M200c / (200 (4 pi / 3) r200c^3)), converted with the
  halo model's h (M[Msun] = M[Msun/h] / h).
- The move: inside R500 the gas cumulative mass is multiplied by s so that stars + gas inside R500 = f_ret x the layout's own
  baryons inside R500 (if the gas is too little, all of it goes, flagged). The removed mass Delta M is put back between R500 and
  an outer edge R_out with M(<r) rising linearly in r (density ~ r^-2), all of it inside R_out. The cold component is held as the
  layout has it. **Graded edge: R_out = r_ta** (form B's own statement: the gas left R500 but not the turnaround region).
  Reported edge: R_out = R200c.
- R_tot' = 1 + (P_B' - P_Lta) / P_std through CO1's halo model (CFG556 library, read-only), z 0 ratio applied at every node, as
  CO1 and CO2 apply R_tot.

**A4. The redshift calibration.**
- Reported at every row: the KiDS delta-z pulls the fit takes at the target and at the best sigma8.
- Row A4 (on A1): the delta-z (and for DES the shear-bias) prior widths doubled (CFG592's `widen = 2`). This is a proxy for "the
  calibration was off by more than its stated width"; it is not newer data. Newer data is Part B (KiDS-Legacy).
- Context only, not a number in any verdict: what Wright et al. 2025 (A&A 703, A158; arXiv:2503.19441; read 2026-11-10, a web
  read, PROVISIONAL) report in Appendix I.1 for KiDS-1000 re-analysed with the Legacy redshift calibration (tension with Planck in
  their Hellinger measure: 1.42 sigma in S8 for KiDS-1000 with the Legacy calibration; 0.85 sigma for Legacy on the KiDS-1000
  footprint; the Legacy S8 0.815 +0.016 -0.021; Section 6 attributes about two thirds of the reduction in tension to redshift
  estimation and calibration). No per-bin shift for KiDS-1000's n(z) was found there, so none is applied in Part A.

**A5. The brackets that can go against form B** (each on A1, then each on ALL; reported, never graded):
- A5a long modes: CO2's R2 splice (CFG411's 200 Mpc/h S0 run below k 0.5) and, above k 0.5, the box-size deficit: the S0 nodes
  times the median of P_L200 / P_L100 over 0.5 <= k <= 1.0 at that node (whatever its sign). Second realisation (CFG424, seed 360)
  reported beside it.
- A5b resolution: the support mask with k_hi halved (points need >= 0.9 of the integrand below 4.02 h/Mpc).
- A5c1 alignment off. A5c2 (KiDS only) alignment with a free redshift power eta in [-5, 5] about z 0.62 (DES's form; start 0).
- A5d cuts: support threshold 0.8, and 0.7 (more of the published points).

**ALL.** A1 + A2 (gamma 2) + A3 (r_ta edge). Reported beside it: A2's edges, A3's R200c edge and its power-law f_ret, + A4, and
each A5 bracket.

## 5. MUTATE (separately named outputs, `*_MUTATE*`)

- **MA1**: at the A1 refit parameters, one neutrino of 0.6 eV must lower CLASS sigma8 by at least 0.03.
- **MA2**: KA2 rerun with every n_i halved must FAIL (ii) (the area fit absorbs an overall factor, not the change of the noise
  share).
- **MA3**: f_ret = 0.2 for every group / cluster (edge r_ta) must move R_tot at k 1 by at least 0.05 and KiDS chi^2 at the A1
  target by at least 2.
- **MP4**: under ALL's settings, sigma8 forced to 0.90 must still give KiDS p < 0.0027 (the covariance at the model must not make
  the gate toothless).
A MUTATE arm that does not bite makes the rows it guards NO VERDICT.

## 6. Labels (frozen rule)

- Per row, per data set, per footing: CO2's lines on p.
- **Per data set (KiDS-1000, DES Y3), per footing: the ALL row's label.**
- **Overall, per footing:** AMPLITUDE CONSISTENT WITH RAW LENSING if both data sets read CONSISTENT at ALL; TENSION if the worse
  reads TENSION; EXCLUDED if either reads EXCLUDED AT 3 SIGMA; NO VERDICT if a KA guarding ALL fails or MP4 does not bite.
- Part A grades KiDS-1000 and DES Y3 only (the newest releases on disk). **Unless Part B is run, the overall label is for
  KiDS-1000 and DES Y3 only**, and says so.
- Every label carries: "for form B with the neutrino floor, its own layout with RB1's gas, the covariance at the model;
  gravity-only S0 box; inherited halo list".

## 7. What would count AGAINST form B (stated before any number)

- ALL leaves KiDS-1000 at TENSION or EXCLUDED on either footing.
- The A5 brackets that go against (A5a's box deficit, A5b, A5c1) push ALL back below 0.0027.
- MP4 fails to bite (the covariance step would then have hidden the gap, not explained it).
- The pinned amplitude needs KiDS delta-z pulls beyond 2 prior widths in any bin at ALL.
- The neutrino floor costs the CMB fit more than 9.
- DES Y3 reads worse at ALL than CO2's p 0.050.
- The gap in widths at ALL stays above 3.

## 8. Hand estimate (written before any code; unverified)

- KA0 reproduces. A1: refit sigma8 0.815 to 0.819; KiDS p 0.006 to 0.010 (TENSION), gap 4.8 to 5.1 widths; DES p 0.07 to 0.10.
- A2 (gamma 2): KiDS chi^2 down by 8 to 20, p 0.01 to 0.04 (TENSION); gap on the chi^2-only scan 4 to 5 widths, larger with
  ln det; DES p 0.1 to 0.2. Edges: gamma 0 about half the drop, gamma 3 a little more.
- A3 (r_ta): Delta chi^2 -3 to -10; R200c edge -1 to -4. A4: pulls of order 1 width toward lower redshift in the upper bins;
  widen 2 gains 3 to 6.
- ALL: KiDS p 0.02 to 0.08 (TENSION 60 %, CONSISTENT 35 %, EXCLUDED 5 %); gap 3 to 4 widths; DES CONSISTENT. Overall label most
  likely TENSION (for KiDS-1000 and DES Y3 only).
- A5: alignment off +5 to +15 in chi^2; A5a's net small; support 0.7 adds points with similar p.
- Part B (not run here): the Legacy release is likely worth 1 to 2 more widths; the closure chat's guess (5 widths to 1 or 2 with
  the release, about 1 more from A1 to A3) is more generous than mine for A1 to A3.

## 9. Part B

Only after the owner's go, relayed by the closure chat. Its criteria are written and committed alone before the tarball is opened
(`FROZEN_CRITERIA_PARTB.md`). The tarball goes in its own new folder under `_external_data/` (untracked), is treated as untrusted
data (scripts elsewhere, read with `python3 -I`), and its URL, date and sha256 are recorded in the lane.

## 10. Disclosures

- Seen before the freeze: all of CO2 and CO1 (every number quoted in section 1), RB1's tables, the headers of the two survey
  files (shape noise and densities; DES carries pair counts), KiDS-1000's release config (its "iterative covariance" chain, whose
  maximum posterior has S8 0.764), and the Wright et al. text quoted in A4. No KL1 number exists.
- The geometry (Omega_m 0.3138, h 0.6736 of the S0 engine) is CO2's and is not changed; form B's pinned Omega_m is 0.315.
- The A2 fiducial is a proxy (the survey's best fit for form B's spectrum), not the survey's own fiducial cosmology.
- No LCDM-calibrated machinery enters a verdict: no halofit / HMCode, no hydro feedback table, no survey posterior. The published
  covariances are measurement products and are used as CO2 used them; A2 replaces their signal terms with the model's.
