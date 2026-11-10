# CO2 FROZEN CRITERIA: form B's clustering amplitude, pinned with large-angle polarisation, against lensing

Committed alone, before any CO2 script exists and before any CO2 number is computed.
TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt
(1.1312e-10 m/s^2), graded separately, never pooled. Kappa = 1/2 FITTED; not theory closed. Cold dark energy; no particle.
A fail is reported as a fail, first, in plain words. Nothing here can turn form B into a pass.

## 1. Why

CO1 (`closure_2026_11_09/CO1_form_b_cosmology_computed/`, result a38567b1a8 on origin) found that form B's cosmology rows
hold, and that the amplitude is the unsolved part: the primary-CMB fit it rests on (F1A's B2 cold fit) has no data below
L 30, so the optical depth tau and with it A_s are weakly held (tau 0.070 / 0.073, sigma8 0.8405 / 0.8429). The owner's go
of 2026-11-09 ("Yes, pin it", then "keep swinging") is to pin it. **No download is needed:** the Planck 2018 low-L EE
likelihood table is already on disk (`_external_data/cobaya_2026_10_22/packages/data/planck_2018_lowE_native/prob_table.txt`,
outside the repository, fetched on 2026-10-22 by another lane).

## 2. The pinned fit (per footing)

- **Data:** F1A's PA (Planck PR4 CamSpec cut + ACT DR6, its own likelihood code, executed read-only) plus the Planck 2018
  SimAll EE table, L 2 to 29. chi2_E = -2 sum over L of table[int(D_L^EE / 1e-4 muK^2), L - 2], the published rule
  (Cobaya's `planck_2018_lowl.EE`, transcribed), calibration 1. The optimiser sees the table linearly interpolated between
  steps; every reported chi2_E is the exact lookup.
- **Model and fit:** F1A's B2 cold rule unchanged: theta = (omega_b, omega_d, ln 1e10 A_s, n_s, tau), h from the footing,
  massless neutrinos, CAMB as F1A calls it, F1A's bounds and simplex steps. Nelder-Mead, two starts, at most 250
  evaluations each: (a) F1A's stored best fit; (b) the same with tau 0.055 and ln A_s lowered by 2 (tau_F1A - 0.055). The
  lower chi^2 is the pinned fit.
- **Reported:** tau; its width along the A_s exp(-2 tau) direction from chi^2 at tau +- 0.004 with the other parameters
  held (this understates the profile width, and is said so); chi2_E at F1A's unpinned fit; the change in PA.

## 3. Rows and lines (per footing)

**P1. The pinned fit is adequate.** Delta_cal' = [PA + chi2_E at the pinned fit] - [chi2_cal + chi2_E at the calibration
point], the calibration point being the likelihood package's own test cosmology as F1A's `do_cal` builds it. Line (QX15
L1's): Delta_cal' <= 9 PASS.

**P2. CMB lensing at the pinned amplitude.** CO1's C2, unchanged, at the pinned fit: PR4 bandpowers (L 8 to 400), CLASS;
lines: shape chi^2 <= 18.48 and |A - 1| <= 2 sigma_A.

**P3. Growth rate at the pinned fit.** CO1's C3, unchanged: DESI DR1 f sigma8, every bin within 2 err on both panels.

**P4. Raw KiDS-1000 at the pinned amplitude (the row this lane exists for).** CO1's C5 machinery (CFG592's library part
on CFG596's S0 run, executed unchanged; the same 104 points). Model: S0 x R_tot (form B's layout, CO1's `co1_hm.json`),
moved from the engine's sigma8 0.811 to the pinned fit's sigma8 (CLASS).
- *Amplitude move, primary: the run's own response.* A nonlinear spectrum responds to the linear amplitude by more than
  the linear factor. The response is measured on the S0 run itself: alpha(k) = d ln P / d ln D^2 between neighbouring
  snapshots (node z 0: snapshots z 0.2562 and 0; node 0.5: 0.7548 and 0.2562; node 1: 1 and 0.7548), running median over
  five k bins, clipped to [1, 3]. P'(k, node) = P(k, node) x f^alpha(k), f = (sigma8 / 0.811)^2. This treats a change of
  amplitude as a change of epoch at fixed linear shape, which is what the run can supply.
- *Bracket:* the constant factor f (alpha = 1; CO1's bracket). It understates the move.
- Statistic: the absolute chi^2 of the fit (CFG592's nuisances and priors) and p = chi^2 survival at N = 104, as CFG596
  prints it. Lines: p >= 0.05 CONSISTENT; 0.0027 <= p < 0.05 TENSION; p < 0.0027 EXCLUDED AT 3 SIGMA.
- Reported beside it: the same for S0 alone and for S0 x R_bar; the sigma8 at which the fit is best (chi^2 minimised over
  f with the response scaling) with its Delta chi^2 = 1 width; DES Y3 through the same path.

## 4. Label (per footing)

- **AMPLITUDE HOLDS:** P1, P2, P3 PASS and P4 CONSISTENT.
- **AMPLITUDE IN TENSION WITH RAW KiDS:** P1, P2, P3 PASS and P4 TENSION.
- **AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA:** P1, P2, P3 PASS and P4 EXCLUDED AT 3 SIGMA.
- **PINNED FIT INADEQUATE** if P1 fails; **LENSING ROW FAILS** / **GROWTH ROW FAILS** if P2 / P3 fails (named).
- NO VERDICT if a known answer fails or a mutation arm does not bite.
Every label carries: "for form B as stated, gravity-only S0, nothing ejecting gas beyond R200c; inherited halo list in R".

## 5. Brackets (reported, never graded)

- One 0.06 eV neutrino at the pinned parameters (CLASS): sigma8 and P4's p with it. The fit itself keeps F1A's massless
  setting; this bracket is not a refit.
- P4 with R_tot replaced by 1 (S0 alone) and by CO1's prefactor-0 bracket (the layout that lowers the power most).
- P4 at CO1's unpinned sigma8, both scalings (CO1's constant-factor numbers are the known answer for one of them).

## 6. Known answers

- KA1: the transcribed low-L EE reader at the package's published test point (omega_b 0.022383, omega_c 0.12011,
  100 theta_MC 1.040909, ln 1e10 A_s 3.0448, n_s 0.96605, tau 0.0543, A_planck 1.00044, one 0.06 eV neutrino; CAMB):
  chi2_E = 396.04 within 0.3 (the test's own tolerance is 0.11; CAMB version and settings differ).
- KA2: with the low-L term off, the objective at F1A's stored best fit equals its stored PA (0.1); F1A's calibration
  cosmology replays chi2_cal 3805.37 (0.1).
- KA3: interpolated against exact chi2_E at the pinned fit: within 0.1.
- KA4: the shear path with alpha = 1 at CO1's sigma8 reproduces CO1's bracket (162.04 / 165.18, 0.01); with f = 1 either
  scaling returns CO1's S0 x R_tot (144.95 / 146.01, 0.01).
- KA5: the response is 1 on linear scales: median alpha over k < 0.12 h/Mpc within 0.15 of 1 at each node (before
  clipping).

## 7. MUTATE

- M1 (the pin has teeth): at the pinned fit, tau forced to 0.10 along the A_s exp(-2 tau) direction must raise chi2_E by
  at least 9.
- M2 (P4 has teeth): sigma8 forced to 0.90 must give p < 0.0027 under the primary scaling.
- M3 (the response matters): the primary scaling must give a larger chi^2 than the constant factor at the pinned sigma8
  whenever the pinned sigma8 exceeds 0.811.

## 8. Disclosures

- Seen before the freeze: all of CO1, including raw KiDS p for form B at sigma8 0.811 (0.013 / 0.012), at 0.824 (0.0055 /
  0.0047, post hoc there) and at 0.8405 / 0.8429 (0.0015 / 0.0009), all with the constant factor. The published Planck
  2018 optical depth (about 0.054 +- 0.007) is known to me. P4's lines (0.05 and 3 sigma) are conventional, but they are
  chosen with those numbers in view; that is a limit of this lane.
- Hand estimate (unverified, before any code): tau 0.055 to 0.060; sigma8 about 0.828; PR4 lensing amplitude within
  1 sigma of the prediction; raw KiDS p about 0.004 with the constant factor and lower with the response, so the label is
  expected to be TENSION or EXCLUDED AT 3 SIGMA, near the line between them.
- What the label would and would not say. S0 is a gravity-only run, and form B states no process that removes gas from
  haloes; the KiDS row is graded for the form as stated. A fail here is the weak-lensing amplitude tension that any
  cold-component fit to the CMB carries; it is not peculiar to form B, and form B does not relieve it.
- The low-L table is Planck 2018 (SimAll); the high-L spectra are PR4. No LCDM parameter file is read; the calibration
  point in P1 is the likelihood package's own test cosmology, used as a yardstick for adequacy as in F1A and QX15.
