# CMB3 frozen criteria: an assumption audit of the inference "the CMB acoustic peaks require a cold non-baryonic component of ~5.4 x the baryons at z ~ 1100"

Frozen and committed alone, before any CMB3 script or graded number. Kappa = 1/2 FITTED; not theory closed. Adopts
nothing. Audit lane (cold dark energy, the cold component; no particle). Footings graded separately, never pooled:
canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2 (the record's values, as F1A). No LCDM parameter or background as a
premise: the background is F1A's B2 footing rule. One process at a time, RSS < 1 GB, no download.

**Lane id.** CMB3 is opened in CLOSURE_REGISTER (ba14429806) for this session. There is no CMB3 directory and no other
CMB3 commit. Siblings, not duplicated: CMB1 (a66f9d1254: Delta chi2 by L range and peak features, equality-only and
baryon-density-only fits) and CMB2 (3274689858: pre-recombination degrees of freedom of the action, incl. D3 matter
coupling and D4 the a0 law at z 1100). Where CMB3 touches their ground it READS their output if landed and cites it;
otherwise it says "pending CMB1/CMB2" and grades only its own lines.

## Known before this freeze (not blind)

- F1A RESULT (215ea5a09c, criteria 56879e50da, A1 78d0c6f7fa), its parts/*.json and f1a.py: B2 cold PA chi2 3740.16 /
  3740.30, baryons-only (MB) 176,655.7 / 170,414.7, DeltaMB +172,915.6 / +166,674.4, R 5.410 / 5.412; MB fits pinned at
  n_s 1.3, foreground amplitudes 50, Planck calibrations 1.1, A_act 1.27-1.31; B1 R 5.83; CAMB theory, linear lensing.
- WG1-WG4 (11-04, memory + record): CMB-lensing potentials sit at 0.003-0.22 a0 at z < few; law alone from a
  baryons-only start gets the lensing shape wrong (0.31x low to 11-14x high on the web).
- GL1-GL4: the k^-4-less Limber kernel touched only QX15's cells, never F1 (L1/MB).
- KX1 (e9c7e42786), NC3 (774ead884f), DEDUCTION F2 (SPARC f <= 0.33 / 0.19).
- API facts only (no likelihood evaluated): CAMB 1.6.6 has `Alens`, `nrun`, `nnu`, `YHe`, and
  `CAMBdata.get_lensed_cls_with_spectrum(clpp)`, which lenses the model's unlensed spectra with a supplied C_L^phiphi.

## Apparatus (cmb3.py; imports f1a.py's likelihood classes, footing rule and CAMB settings; nothing from QX3/QX10/QX15)

- Theory: CAMB 1.6.6, lmax 7000, lens_potential_accuracy 1, linear lensing, mnu 0, N_eff 3.046, YHe from CAMB's BBN
  rule unless freed (exactly F1A A1's call), plus the switches below.
- Likelihood: F1A's PA = CamSpec NPIPE P-ACT cut + ACT DR6 CMB-only, nuisances profiled (F1A box and priors unless A6).
- Fits: Nelder-Mead, ONE start at the F1A best fit of the same footing and mode (new parameters at their standard
  values), 250 evaluations for cold fits and 300 for MB fits (fewer than F1A's two starts; disclosed; a warm start can only
  lower chi2 from F1A's point, so every Delta below is an upper bound on what a longer fit would give for that fit).
- Statistic for every relaxed assumption X: DeltaMB_X = chi2_MB,X - chi2_cold,X (both refit under X), survival
  S_X = DeltaMB_X / DeltaMB_F1A, and R_X = omega_d / omega_b at the cold,X best fit, shift dR_X = R_X / R_F1A - 1.

## Labels (per assumption, per footing; the assumption's label needs both footings to agree, else SPLIT)

- **BREAKS:** DeltaMB_X <= 25 (baryons-only adequate once X is relaxed), or |dR_X| > 0.25 (the amount is set by X).
- **BENDS:** DeltaMB_X > 25 but S_X < 0.5, or 0.10 < |dR_X| <= 0.25.
- **HOLDS:** S_X >= 0.5 and |dR_X| <= 0.10.
- **NOT TESTABLE ON DISK:** the test needs data not on disk; the data named.
- **READING:** A5 (no run); stated with the record's numbers.

## The assumptions and their tests

**A1. GR linear perturbation theory governs the acoustic era (the a0 law is inert at z ~ 1100).**
- Background: c H(z) / a0 at z 1100 on the B2 cold best fit, both footings.
- Perturbations: from CAMB's Weyl transfer at z 1100 (`get_redshift_evolution`, var 'Weyl' = k^2 (phi+psi)/2), the rms
  Weyl potential per ln k, Phi_W(k) = |Weyl/k^2| sqrt(Delta^2_R(k)), and its physical gradient
  g(k) = c^2 Phi_W k (1+z) / Mpc, for comoving k in {0.02, 0.05, 0.1, 0.2, 0.3} /Mpc (scales 20-300 Mpc), on the cold AND
  the MB best fits. Cross-check with the brief's estimate g = (1/2) H(z)^2 delta r_phys for delta 1e-4 and 1e-3 at
  comoving 10-300 Mpc. y = g / a0 (a0(z) = a0: rho_DE constant on B2).
- Regime with the record's simple form nu(y) = (1 + sqrt(1 + 4/y)) / 2. The baryons-only universe needs the potential of
  (omega_b + omega_d) / omega_b = 1 + R, i.e. nu >= 6.41, i.e. y <= 0.027.
- Line (per footing): **HOLDS** if y >= 1 for every k on the MB fit (nu - 1 <= 0.62: no route to 6.4x). **BREAKS
  POSSIBLE** if y <= 0.027 at some k on the MB fit (the law could carry the amount; its still-vs-follows sign is CMB2
  D4's, cited). **BENDS** (law not inert, amplitude short of 6.4x) otherwise; the max nu - 1 is reported.
  The peak-ratio consequence of a modified Poisson equation is not recomputed here: CMB2 D4 owns it (cited if landed).

**A2. The theory is lensed with the model's own late-time lensing potential.**
- (a) A2-U: unlensed theory (C_L^phiphi = 0) against the lensed PR4 + ACT data. No delensed data vector exists on disk
  (CamSpec NPIPE and ACT DR6 CMB-only are lensed); this is the "no lensing" bound.
- (b) A2-T: theory lensed with A_phi x C_L^phiphi,ref, where the template ref is the F1A B2 cold best fit's own
  C_L^phiphi (per footing), held FIXED for both cold and MB fits; A_phi free in [0, 15]. This decouples the smoothing
  from each model's own late growth. The record has no single framework lensing amplitude (WG2: 0.31x to 11-14x of the
  data); the bracket [0, 15] contains every value it reports, so a free A_phi bounds every fixed choice in that range.
  The best-fit A_phi is reported for cold and MB.
- Both (a) and (b): cold and MB refits, both footings; DeltaMB_X, S_X, R_X; labels as above.

**A3. Standard recombination, Thomson coupling and N_eff.**
- A3-N: N_eff free in [1.0, 6.0] and YHe free in [0.10, 0.40] together (cold and MB refits, both footings). The B2
  canonical rule uses omega_r(N_eff) (F1A's OMR with 3.046 replaced by N_eff); disclosed.
- Photon-baryon coupling: whether the certified action modifies Thomson scattering, c_s or r_s other than through
  H(z) and the metric is CMB2 D3's question. CMB3 reads CMB2 D3 if landed: if D3 finds no khronon field in the matter
  equations, "no framework-native modification exists" is recorded with CMB2's hash; if not landed, "pending CMB2 D3".
- Label from A3-N by the common lines. Any recombination change beyond N_eff and YHe (varying alpha, m_e, extra
  ionising photons) is NOT TESTABLE in CAMB 1.6.6's standard call without a recombination code change; stated as
  such, with the reason (no framework-native source, if D3 says so).

**A4. Adiabatic, Gaussian, nearly scale-invariant initial conditions (n_s 0.95 on B1).**
- A4-P: n_s free in [0.50, 2.50], running nrun free in [-0.50, 0.50], ln(1e10 A_s) in [0.0, 5.0] (cold and MB refits,
  both footings).
- Degeneracy direction: at the cold best fit of A4-P, the chi2 Hessian in (omega_b, omega_d, ln A_s, n_s, tau, nrun) by
  central differences (steps 1.5e-4, 1.2e-3, 0.015, 0.004, 0.008, 0.008; nuisances profiled at each point), inverted to a
  covariance; reported: corr(omega_d, n_s), corr(omega_d, nrun), d omega_d / d n_s along the degeneracy, and the n_s
  shift that would move R by 10 %.
- Also reported (no new fit): B1 (n_s fixed 0.95) vs B2 (free n_s) R, 5.83 vs 5.41, from F1A.
- Isocurvature and non-Gaussian initial conditions: NOT TESTABLE in this apparatus (would need a CAMB isocurvature run
  of a component that is absent in MB); stated.

**A5. The identification "the component that sits still at z 1100 is the stuff that makes rotation curves flat".**
- READING, no run. Stated with the record's numbers: SPARC f <= 0.33 / 0.19 (DEDUCTION F2); KX1 (e9c7e42786) posterior
  excess of data over law -0.21 / +0.02 / +0.01 / +0.05 canonical and -0.25 / -0.02 / -0.03 / +0.01 alt across its bins;
  NC3 (774ead884f) members carry no residue (D +0.011 / +0.012 dex); NC4's host share as its RESULT states it. Label
  **BREAKS (by the record's own data)** if those numbers stand as recorded; the reading names what F1 does NOT say (it
  says nothing about where the component is today).

**A6. Foreground / calibration templates and priors (built around LCDM-like fits).**
- A6-F: nuisance box widened and priors removed: amps in [0, 1000], tilts in [-5, 10], A_planck, calTE, calEE in
  [0.5, 1.5] with NO Gaussian priors; A_act in [0.3, 3.0], P_act in [0.5, 1.5].
- Step 1 (point): re-profile the nuisances under A6-F at the four F1A B2 best fits (cold, MB, both footings).
- Step 2: MB refit under A6-F (both footings); the cold side uses the step-1 value (a cold refit can only lower
  chi2_cold, which can only RAISE DeltaMB; so DeltaMB_A6 here is an upper bound by at most that cold refit gain, which is
  reported as the step-1 cold change).
- Nuisance sensitivity: |DeltaMB_A6 / DeltaMB_F1A - 1| reported; "more than a few percent" means > 5 %. Label by the
  common lines.

## Known answers (must pass, else NO VERDICT)

- **KA-1 (replay of F1A's Delta):** PA chi2 at the four stored F1A B2 best fits, nuisance profile started at the stored
  nuisances: each within 0.1 of the stored value, so DeltaMB = +172,915.6 / +166,674.4 within 0.2.
- **KA-2 (replay of F1A's amount):** a 60-evaluation Nelder-Mead from each stored cold best fit (F1A apparatus, no switch)
  lowers chi2 by <= 1.0 and keeps R within 0.5 % of 5.410 / 5.412.
- **KA-3 (lensing path):** A2's path with the template = the model's own C_L^phiphi and A_phi = 1 reproduces the F1A
  chi2 at the cold best fit within 0.5 (both footings).
- **KA-4 (switch-off):** at the cold best fit, A3's path with N_eff 3.046 and YHe = CAMB's BBN value, A4's with nrun 0,
  and A6's code with F1A's box and priors each reproduce the stored chi2 within 0.1.

## MUTATE (separate outputs, cmb3_MUTATE.json)

- **M1 (the brief's):** at each MB best fit, omega_b doubled (canonical h from the footing rule; alt h fixed). From the
  theory TT D_ell, peak heights H1 (L 150-320), H2 (L 420-620), H3 (L 700-900) by the local maximum. PASS if H1/H2 moves by
  > 5 % AND the third peak is not restored: |(H3/H2)_mut / (H3/H2)_cold - 1| > 0.02 AND chi2_PA(mut) - chi2_cold > 25.
- **M2 (each switch reaches the likelihood):** at each cold best fit, A_phi = 3 (A2-T path), N_eff = 5.0 (A3), nrun =
  +0.10 (A4) each raise chi2_PA by > 25. PASS if all three do on both footings.
- If M1 or M2 fails, the lane label is NO VERDICT.

## RESULT

RESULT.md opens with "CMB3 RESULT (criteria <hash>):", each assumption's label on both footings, then one plain
paragraph: which assumptions are solid, which are the record's own to question, which (if any) are wrong by the
record's numbers. If the peak-ratio inference holds and only A5 breaks, it says exactly that.

Kappa = 1/2 FITTED; not theory closed.
