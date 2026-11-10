# KL1R FROZEN CRITERIA: a blind, independent regrade of KL1 Part B (form B's weak-lensing amplitude against raw KiDS-Legacy)

Committed alone, before any KL1R script exists and before any KL1R number is computed. TEST lane, quarantined: adopts nothing,
relabels nothing, registers nothing. **kappa = 1/2 FITTED; not theory closed.** Footings canonical (a0 9.3603e-11) and alt
(1.1312e-10 m/s^2) are graded separately, never pooled. The component is cold dark energy, a gravitating field component, never a
particle. Lane id KL1R checked free (`ls closure_2026_11_10`, `git log --all --grep KL1R`: no hit) on 2026-11-10.

## 0. What is adopted, as written

KL1's criteria, quoted by file and commit, with nothing changed except where section 2 says how an open point is read:

- Part A: `closure_2026_11_10/KL1_lensing_amplitude_survey_assumptions/FROZEN_CRITERIA.md`, commit **99a42c78ef** (read as it
  stands in that commit; the file was committed alone, before any KL1 script or number, and has not been changed since).
- Part B: `FROZEN_CRITERIA_PARTB.md`, commit **d26939ed4f**.
- Amendment PB1 (how Part B is read on the Legacy files): `AMENDMENT_PB1.md`, commit **7787483300**.
- Amendment A1 (post hoc: MA2b, the DES reading): `AMENDMENT_A1.md`, commit **e01d1b9a35**.
- The fetch log: `FETCH_LOG_PARTB.md`, commit **0965901c16** (tarball path and sha256
  `7fdf214cbb54e51d5ca385d79a4590750d3c5dc9fe6803460bab8ed841c57f77`).

The graded object is therefore KL1 Part B: rows B0, B1, B2, B3, BALL on KiDS-Legacy (and DES Y3's rows A0, A1, A2, A3, ALL,
because Part B's overall label is the worse of Legacy and DES Y3 at their ALL rows), both footings, with Part B's known answers
KB1 to KB4, its MUTATE arms MB1 and MB2, Part A's known answers and arms that guard the rows used (KA1 to KA4, MA1, MA2, MA3), and
A1's MA2b. Labels by CO2's lines on p (p >= 0.05 CONSISTENT; 0.0027 <= p < 0.05 TENSION; p < 0.0027 EXCLUDED AT 3 SIGMA), the
overall label by Part A section 6 applied as Part B section 5 says. The frozen reading is reported first; the A1 reading beside it.

## 1. Blindness and what I have seen (disclosed before any number)

- Read in KL1's folder: only the four criteria files above, and Part A's criteria as committed in 99a42c78ef (Part B says
  "everything not named here is as there", so its rows B1, B2, B3 cannot be built without it; it was committed before any KL1
  number). Not opened: KL1's `RESULT.md`, any `kl1*.py`, `*.out`, `*.json`, `parts/`; KL1 commit messages after d26939ed4f not read
  on purpose; not searched in memory or chats; the closure chat's rerun folder `closure_2026_11_10/_kl1_rerun_tmp` not opened.
- **The blindness is NOT clean, and I say so before computing.** Before this lane started, text placed in my context by the
  harness and the brief showed some of KL1's landed numbers: the subject lines of KL1's result commits (in the session's initial
  git snapshot), one memory-index line and the lane brief. What I saw: KL1's Part B reads NO VERDICT as frozen (MA2 cannot bite on
  DES) and AMPLITUDE CONSISTENT WITH RAW LENSING under A1; Legacy p about 0.11 / 0.10 and DES Y3 p about 0.16; Legacy best sigma8
  about 0.788 / 0.786 +- 0.012, 2.1 / 2.3 widths below 0.812; KiDS-1000 TENSION (p about 0.038); a neutrino refit sigma8 about
  0.8121; and from the criteria text itself, MB2's move 0.46 / 0.47 width and DES's 3 / 4 points under MA2. I did not look for
  more. The mitigation is procedural: every choice below is frozen before any code, my code is written from the criteria text and
  the pre-KL1 machinery only, and no setting is changed after a number is seen (any change is an amendment, committed alone and
  marked post hoc).
- Also seen before this freeze: all of CO1, CO2 (criteria, scripts, outputs), CFG592's library, F1A's CAMB call, RB1's f_ret table.
  The KiDS-Legacy files have NOT been opened by me; only PB1's description of them is known.

## 2. Choices the adopted criteria leave open (fixed now)

**2.1 Machinery and form B's spectrum.** CFG592's library part (`cfg592_native.py` above its `# --- run` line) executed unchanged
as CO2's `co2_shear.py` executes it (projection, Hankel, KiDS-1000 and DES loaders, `theory`, `fit`, `support_mask`, `subset`,
`Pmat`). The model is CO2's exactly: CFG596's S0 run x R (CO1's `co1_hm.json` primary `R_tot`, or my gas-moved R for B3 / BALL),
moved from 0.811 to the target sigma8 by the run's own response alpha(k) (CO2's construction: snapshot pairs, five-bin running
median, clip [1, 3]). The uncorrected S0 nodes are graded (as CO2 and KL1 Part A section 2). My own code, in this folder, does:
- the Legacy loader (PB1 items 1 to 7) and a 6-bin nuisance block written for it: six decorrelated shifts x with unit Gaussian
  priors about PB1's means, dz = L x (L the lower Cholesky factor of `Nz_covariance.txt`), bounds mean +- 5, one NLA amplitude in
  [-6, 6]; L-BFGS-B with two starts (A 0.5 and -0.5), maxiter 400, ftol 1e-12, gtol 1e-8 (CFG592's KiDS settings). No shear-bias
  parameter (PB1 item 5). Data vector order = the FITS xiP rows then the xiM rows, matched to COVMAT (PB1 item 1); KB1 checks it.
- Legacy n(z): the NZ_SOURCE weights read as given; `kernels` interpolates them onto CFG592's z grid (to 3.5) and renormalises
  (PB1 item 7); the fraction beyond 3.5 is reported.
- The Legacy support mask as CFG592's (>= 0.9 of the absolute integrand inside the S0 run's k range), with the published cuts.
- DES Y3 rows use CFG592's DES loader, nuisances and `fit` unchanged.

**2.2 The neutrino floor (row B1 / A1's target), my own refit.** A new script, `kl1r_nu.py`: the objective is F1A's PA (imported
read-only from `closure_2026_11_07/F1A_primary_cmb_audit/f1a.py`) plus CO2's low-L EE term (`chi2E` from CO2's `co2_fit.py`,
interpolated for the optimiser, exact lookup reported). The CAMB call is F1A's `camb_theory` re-written in my file with
`mnu=0.06, num_massive_neutrinos=1, nnu=3.046` (everything else as F1A: lmax, lens_potential_accuracy 1, linear lensing). h rule:
canonical h^2 = (F1A's footing_h)^2 + 0.06 / 93.14; alt unchanged. F1A's bounds and simplex steps; Nelder-Mead, at most 250
evaluations per start; starts (a) CO2's pinned theta, (b) tau 0.058 and ln 1e10 A_s raised by 2 (0.058 - tau). The lower total is
the refit. Target = CLASS sigma8 (total matter) at the refit with one 0.06 eV neutrino, CLASS settings as CO2's `class_B(pr,
nu=True)` (re-written in my file). The CMB cost (refit total minus CO2's pinned total) is reported; above 9 the rows are flagged
PINNED FIT INADEQUATE WITH THE FLOOR and still run. The A1s shape variant is not computed (Part B's rows do not use it).
KA1: (i) my CAMB call with mnu 0, no neutrino in h, at CO2's pinned theta reproduces CO2's stored PA (0.1) and exact chi2_E (0.01);
(ii) my CLASS sigma8 with the neutrino at CO2's pinned parameters gives 0.8152 (0.0005). MA1: one 0.6 eV neutrino at the refit
lowers CLASS sigma8 by at least 0.03.

**2.3 The covariance at the model (row B2 / A2), how I build G.** Part A's A2 formula, with these readings:
- Units: densities n_i (arcmin^-2, header NGAL_i) converted to sr^-1; shape noise s_i = header SIG_E_i (per component); area A
  and bin solid angle Omega_bin = pi (theta_hi^2 - theta_lo^2) in sr; N^ij = delta_ij s_i^2 / n_i.
- C^ij(ell): the model's own GG spectra (no alignment) at nominal nuisances = the prior means (Legacy and KiDS: dz = L mu; DES:
  dz 0, no shear bias), computed on CFG592's 150 ell nodes and carried to its 12000-point fine grid by CFG592's own matrix MI
  (linear in ln ell of ell^2 C).
- Jbar_p(ell): the bin average of J0 (xi+) or J4 (xi-) over CFG592's 40 theta-weighted sub-angles of the published bin, times
  CFG592's high-ell TAPER; the integral is sum_ell ell dell over the fine grid. Bin edges: Legacy geomspace(2, 300, 10) arcmin
  (PB1 item 2); DES its ANGLEMIN / ANGLEMAX. xi+ / xi- cross blocks use J0 x J4. The pure-noise term only on (same bin, same
  sign) as written.
- "My noise term" in KA2's (i) / (ii) = the pure shape-noise term on the diagonal; "my Gaussian diagonal" = the full G diagonal.
  KA2 is evaluated over the published-kept points (published cuts only), at the fiducial.
- Area: A = 1 / median(C_pub / G_{A=1}) over the noise-dominated points (noise >= 0.8 of the diagonal), once per survey at the
  fiducial. Fiducial = form B's spectrum at the survey's own best sigma8 of its B0 / A0 row (published covariance, CO2's target).
  Reported: the fiducial +- 0.02 edges.
- R = C_pub - G(fid), scaled by (s_p s_q)^(gamma / 2), s_p = xi_model(p) / xi_fid(p) at nominal nuisances with no alignment,
  clipped to [0.5, 3]. Graded gamma 2; gamma 0 and 3 reported. C(model) subset to the kept points; not positive definite -> NO
  VERDICT. Graded p at the row's target; the scan recomputes C at each grid sigma8 (chi^2 only); ln det C reported beside it.
- MA2 (frozen): KA2 rerun with every n_i halved, area refitted, must FAIL (ii); MA2b (A1): every n_i doubled, must FAIL (ii). Run
  on Legacy and on DES. Frozen reading: MA2 guards the B2 / BALL rows (A2 / ALL for DES) of the survey it is run on; if it does not
  bite (including NOT EVALUABLE) those rows read NO VERDICT. A1 reading: DES's guarded rows are read by MA2b instead of MA2;
  Legacy keeps MA2 as frozen (A1 names only DES), with MA2b reported for it.

**2.4 The gas (row B3 / A3), my own layout move.** CO1's `co1_hm.py` (pre-KL1) is executed up to its results block to obtain
CFG556's library and CO1's `layout`, `set_population`, `ratios` unchanged. My cluster-regime variant (v_vir > v_stiff only) copies
CO1's cluster branch and changes one thing: the baryon cumulative mb(r) = stars(r) + gas(r) becomes stars(r) + gas'(r) with
gas'(r) = s gas(r) for r <= R500; gas(r) - dM + dM (r - R500) / (R_out - R500) for R500 < r <= R_out; gas(r) beyond, where
s = [f_ret mb(R500) - stars(R500)] / gas(R500) (all gas removed and flagged if negative), dM = (1 - s) gas(R500). The phantom and
cold terms are computed from the UNMOVED mb (the cold component held as the layout has it). R500 solves M(<r) = 500 rho_c (4 pi /
3) r^3 on the unmoved layout's total M(<r), rho_c = M200c / (200 (4 pi / 3) r200c^3); M500 in Msun = M500 [Msun/h] / h (halo
model h). R500 and R_out are inserted into the radial grid. f_ret(log M500): RB1's kvm column (0.674, 0.592, 0.800, 0.920, 1.095
at 13.25, 13.75, 14.25, 14.75, 15.25; read from `rb1.json` gate2 extended_GS4 and checked against these), linear in log M500,
held at the ends, capped at 1. Graded edge R_out = r_ta; reported: R_out = R200c and the power-law f_ret (slope 0.160 through
(13.75, 0.592), capped at 1). R' = 1 + (P_B' - P_Lta) / P_std, z 0 ratio at every node, as CO1 / CO2. KA3 (i) to (iii) as Part A.
MA3: f_ret = 0.2 everywhere in the cluster regime (edge r_ta) must move R at k 1 by >= 0.05 and the Legacy chi^2 at the B1 target
by >= 2 (Part A says "KiDS"; in Part B the KiDS data set is Legacy); DES's move reported.

**2.5 Brackets on BALL (reported, never graded).** A5c1: alignment off. A5a: CO2's post hoc R2 splice (CFG411's L 200 S0 run below
k 0.5, as `co2_posthoc.py` builds it) and, above k 0.5, the S0 nodes times the median of P_L200 / P_L100 over 0.5 <= k <= 1.0 at
that node; CFG424's seed-360 run beside it. Each on Legacy and DES, both footings.

**2.6 Scans and widths.** CO2's rule: chi^2 on the grid 0.70 to 0.90 step 0.0125 (extended by 0.0125 steps to at most 0.60 /
1.00 if the minimum is at an edge), parabola through the five points around the minimum, width at Delta chi^2 = 1; gap = (target
- best) / width. delta-z pulls = fitted x minus prior means (unit widths) at the target and at the best sigma8.

**2.7 MUTATE readings.** MB1 (sigma8 0.90 under BALL, covariance at that model) must give Legacy p < 0.0027; it is Part B's MP4: if
it does not bite, NO VERDICT (and it counts against form B). MB2: under B1's settings, KiDS-1000's five prior-mean shifts (L_K1000
mu_K1000, CFG592's values) each go to the Legacy bin of nearest n(z) mean redshift (on the file's n(z)); if two land on one Legacy
bin their mean is used; a Legacy bin that receives none keeps its own prior-mean shift; Legacy's decorrelated means are replaced by
L^-1 of the resulting shifts; it must move the Legacy best sigma8 by >= 0.5 width. Part B names no row that MB2 guards, so **my
frozen reading is: MB2 not biting is reported as a finding (the redshift calibration has no teeth here) and does not change the
label**; the strict alternative (MB2 guards every Legacy row -> NO VERDICT) is reported beside it.

**2.8 Known answers.** KB1 as PB1 item 7 reads it (weights sum to 1 within 0.01 per bin; 189 + 189 points, 6 bins, 21 pairs, 9
angular bins, COVMAT positive definite). KB2: my generalised loader and fit, applied to the KiDS-1000 file, reproduce CO2's P4
157.89 / 159.35 (0.01). KB3: KA2 on Legacy passes (i) and (ii), else B2 / BALL read NO VERDICT. KB4 reported (Legacy best sigma8
for form B beside KiDS-1000's 0.7358 / 0.7341 and Wright et al. 2025's S8 0.815 +0.016 -0.021, context). KA2 on DES guards DES's
A2 / ALL the same way. KA4 (CO2's response check) is rerun.

## 3. Labels

Per data set, per footing: the ALL row's label by CO2's lines. Overall (Part B), per footing: AMPLITUDE CONSISTENT WITH RAW
LENSING if Legacy and DES Y3 both read CONSISTENT at ALL; TENSION if the worse reads TENSION; EXCLUDED if either reads EXCLUDED
AT 3 SIGMA; NO VERDICT if a known answer or MUTATE arm guarding an ALL row fails (MA2 / MA2b as section 2.3, MA1, MA3, MB1).
Reported in this order: the frozen reading, then the A1 reading. Every label carries: "for form B with the neutrino floor, its own
layout with RB1's gas, the covariance at the model; gravity-only S0 box; inherited halo list".

Counts against form B (Part B section 5, adopted): BALL at TENSION or EXCLUDED on Legacy; the Legacy gap above 2 widths; MB1 not
biting.

## 4. Comparison with KL1

Only after this lane's RESULT.md (label first, numbers table) is committed do I open KL1's RESULT.md. The comparison is a section
added afterwards, number by number; a disagreement is a finding and is not edited toward KL1.

## 5. Hand estimate (contaminated; see section 1)

I cannot make a clean estimate: I have seen KL1's headline numbers. Without them I would have expected the neutrino floor to move
the target down by about 0.012 to 0.015, the Legacy best sigma8 for form B about 0.78 to 0.80, the covariance at the model to cut
chi^2 by 5 to 15 and the gas to gain a few in chi^2.
