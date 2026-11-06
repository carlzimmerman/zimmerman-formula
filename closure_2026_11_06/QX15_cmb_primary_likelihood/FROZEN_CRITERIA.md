# QX15 frozen criteria: likelihood-level primary CMB (Planck PR4 CamSpec + ACT DR6 CMB-only)

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. The rules in
closure_2026_11_06/SWARM_BRIEF.md bind this lane. Both footings, never pooled. No dark-matter particle.

## Why

QX10 iter_1 graded the primary CMB on raw Planck PR3 spectra with diagonal errors. Its J1 late-lensing check was a
conservative bound, so iter_1 ended NO VERDICT. The owner approved, in chat on 11-06, downloading the PR4 and ACT primary
likelihood data. This lane grades at the likelihood level with full covariance. QX7 iter_4's window is already KILLED by
QX10 G6 (KiDS lensing). This lane can only sharpen the CMB side of the record; it cannot revive the window.

## Data (official distribution points; hashes in README)

- Planck PR4: CamSpec_NPIPE 12.6 (Rosenberg, Gratton & Efstathiou 2022), from Cobaya's official
  planck_native_data release v1. TTTEEE uses `use_cl = 143x143 217x217 143x217 TE EE`, as in Cobaya's
  `planck_NPIPE_highl_CamSpec.TTTEEE`. It has 9,915 points and covers L 30-2500. The likelihood is re-implemented from
  Cobaya's source: the power-law foreground residual model, the A_planck^2, calTE and calEE calibrations, and the
  Gaussian priors A_planck N(1, 0.0025) and calTE/calEE N(1, 0.01).
- ACT DR6 CMB-only (ACT-lite), dr6_data_cmbonly.fits v1.0 from LAMBDA. It has 135 bandpowers (TT, TE and EE, each
  45 bins over L 600-6125), the full covariance, bandpower windows, and the nuisances A_act and P_act, as in
  act_dr6_cmbonly.py.
- Headline combination PA: ACT plus CamSpec cut at the P-ACT convention (TT L <= 1000; TE and EE L <= 600). This
  avoids double-counting the shared sky. P (full CamSpec) and A (ACT alone) are also reported at the PA best fit, with
  nuisances re-profiled. They are reported, not graded.
- Nothing at low L: neither L < 30 TT nor low-L EE is used. tau is free in [0.01, 0.15]. The A_s-tau degeneracy is
  harmless for Delta chi^2.

## Theory

CAMB 1.6.6 with lmax 7000 and lens_potential_accuracy 1 for fits. The background is QX10's footing rule, frozen
there:
- canonical fixes omega_DE = 4 a0^2/(G c^2 rho_c100) and sets h^2 = omega_DE + omega_b + omega_d + omega_r;
- alt fixes h^2 = 4 a0^2/(G c^2 rho_c100).

Free parameters are omega_b, omega_d, ln(1e10 A_s), n_s and tau, with QX10's brackets. Nuisances are profiled at
each theory point with L-BFGS-B, using analytic gradients and Cobaya's prior ranges. No LCDM parameter enters any
model.

## Graded quantities and lines

- **KA-P / KA-A (code checks only, never inputs).** At Cobaya's published NPIPE test point (CAMB, given nuisances),
  the CamSpec TTTEEE chi^2 must equal 11337.34 within 1.0. At the DR6-ACT-lite test point (A_act = P_act = 1), the
  ACT chi^2 must equal 790.96 (= -2 x -395.48) within 1.0. Both use high accuracy (lmax 9000, lens_potential_accuracy
  8). If either check fails, the lane is NO VERDICT.
- **Yardstick chi2_cal.** My PA chi^2, profiled over nuisances, at Cobaya's published NPIPE test cosmology. It is a
  calibration of the gate, not an input to any model.
- **L1 (main fit adequacy), per footing.** Delta = chi2_main(PA) - chi2_cal, both nuisance-profiled. PASS if
  Delta <= 9; TENSION if 9 < Delta <= 25; FAIL if Delta > 25.
- **K-acc.** At each main best fit, |chi2(lmax 7000, lpa 1) - chi2(lmax 9000, lpa 8)| <= 2 on PA. Otherwise L1 is
  NO VERDICT.
- **(a) Control: baryons-only plus the law (QX10's MB; omega_cdm = 1e-7, same footing).** Fitted the same way. It must
  FAIL L1 (Delta > 25). If it does not, the gate has no power and the lane is NO VERDICT.
- **(b) Cells C1-C4 (QX10's pre-chosen cells; no new cell).** The cold component is the main fit's omega_d. The
  lensing potential is multiplied by the cell's Jeans suppression S(L): QX10 jcheck's Limber machinery (QX7 G2'
  solver), extended to L <= 7000. Beyond the solver's k-grid, S is held at its last covered value. This is declared
  here: it may understate high-L suppression, so a PASS there is weaker; a FAIL stands. Lensed spectra come from
  CAMB's lensing of the unlensed spectra with C_L^{phi phi} x S(L). Each cell gets a local refit of the 5 cosmological
  parameters, starting from its footing's main best fit (Nelder-Mead, at most 150 evaluations), with nuisances
  profiled. Then Delta_cell = chi2_cell(PA) - chi2_main(PA). PASS if Delta_cell <= 4; TENSION if 4 < Delta_cell <= 25;
  FAIL if Delta_cell > 25. This replaces QX10's J1 bound for these cells.
- **Power control for (b), P1.** A planted flat S = 0.5 at all L, run the same way, must give Delta_cell > 25. If it
  does not, the cell labels are NO VERDICT.

## MUTATE (separate outputs)

- M-A (p = 0: the sector smooth, with c_s^2 = 1). CAMB cannot add a second fluid, so this runs in CLASS 3.x with
  QX10's MA settings: a w0_fld = -1e-3 fluid with cs2_fld = 1 and abundance omega_d. Spectra go into the same
  likelihood code. It must FAIL L1. CLASS-versus-CAMB code differences (Cobaya reports about 7 in chi^2 for CamSpec)
  are far below the expected effect. If M-A or MB does not fail, the controls do not bite.

## Scope

The primary spectrum of a cold component on the footing background is the standard cold-component spectrum (QX10's
disclosure). L1 therefore tests whether the footing constraint, h fixed by a0, survives likelihood-level PR4 + ACT.
It is not independent evidence that the framework predicts the peaks. Labels cover only the cells and footings
above. A grader module (qx15_like.py) is left for reuse: it takes a dict of D_ell TT/TE/EE spectra and returns the
profiled chi^2 for P, A and PA.
