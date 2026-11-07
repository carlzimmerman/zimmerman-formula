# F1A: independent audit of fact F1 (the primary CMB needs a cold component of ~5.56 x baryons; baryons-only fails; the khronon clock cannot cluster)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Audit lane (cold dark energy; no particle). Footings graded
separately, never pooled.
- Criteria: FROZEN_CRITERIA.md (56879e50da), committed alone before any script or graded number.
- Amendment A1 (78d0c6f7fa), committed before any graded number: CAMB replaces CLASS for the fits (memory), and CLASS
  is kept as a Pcut check.
- Scripts:
  - f1a.py (own likelihoods, fits, G4 code, M2), run by run_fits.sh, which writes parts/*.json and run_fits.log (gitignored, not committed).
  - f1a_grade.py assembles f1a.json / f1a.out and f1a_MUTATE.json / f1a_MUTATE.out.
- One thread, under nice. Fits peak at 0.86-0.91 GB, G4 at 0.08 GB. KA-P peaked at 1.81 GB for 10 s; that is disclosed
  in A1 and was not rerun. Nothing downloaded.

## Label: F1 CONFIRMED on both footings

| | canonical | alt |
|---|---|---|
| B2 PA chi2, cold / baryons-only | 3740.16 / 176,655.7 | 3740.30 / 170,414.7 |
| **G1** DeltaMB on B2 | **+172,915.6** | **+166,674.4** |
| G1 DeltaMB on B1 (record background; same for both footings) | +180,012.5 | +180,012.5 |
| **G2** Delta_cal (chi2_cal 3805.37) | **-65.21** (adequate) | **-65.07** (adequate) |
| **G3** R = omega_d / omega_b at the B2 best fit | **5.410** (0.973 of 5.562, inside 10 %) | **5.412** (0.973) |
| B2 best fit omega_b / omega_d / h / n_s / tau | 0.02236 / 0.1209 / 0.674 / 0.967 / 0.070 | 0.02234 / 0.1209 / 0.674 / 0.967 / 0.073 |
| B1 best fit omega_d (omega_b 0.0215, H0 65, n_s 0.95 fixed); R | 0.1254; R 5.83 (PA chi2 3830.19) | same |
| **G4** clock sign | REPRODUCED | REPRODUCED |
| Cold fit with HMCode lensing (reported) | 3741.26 | 3741.56 |
| CLASS minus CAMB on Pcut at the cold best fit | +3.82 | +3.84 |
| Label | **CONFIRMED** | **CONFIRMED** |

The cold component is needed, with R 5.41 against the record's 5.56. That is 2.7 % low and inside the frozen 10 %. My
numbers sit on QX15's to the second decimal: its PA 3741.08 / 3741.15, its best fit omega_b 0.02236, omega_d 0.1209,
h 0.674. The 0.9-unit offset in PA chi2 matches the gap between QX15's chi2_cal (3805.80) and mine (3805.37). The
"5.562" is a background-fixed ratio. On the record's own fixed background (B1), R is 5.83, and the fit is about 90
chi2 worse than B2.

## Step 2: what QX15's grader imports

- **Clean:** QX15's graded L1 and MB paths (qx15.py + qx15_like.py with CAMB) import nothing from QX3 or QX10. F1 does
  not sit on the bad Limber kernel. GL1's statement holds for the primary-CMB fits.
- **Not clean:** QX15's cell path (`do_cells`: C1-C4 Delta_cell and the P1 power control) execs QX10 iter_1's `jcheck`.
  - `jcheck` execs QX3 iter3's solver.
  - It carries a copy of the weight `w = ((chis - chi)/(chi chis))^2 (1+z)^2 / H`, then divides by chi^2, with no k^-4.
    GL2 confirmed that this kernel is wrong.
  - So QX15's cell Delta_cell and P1 numbers sit on the wrong kernel and need the GL1/GL3 re-statement. F1 does not.

## The clock no-go: equation and sign check

- **The equation (QX3 iter1 C1, Lean `clock_jeans`):** a field with sound speed c_s clusters only on scales
  k < k_J, where k_J^2 = 4 pi G rho_phi / c_s^2.
  - The clock has c_s^2 = 1 and rho_phi <= rho_total.
  - With 4 pi G rho_total = (3/2) H^2 (flat), k_J^2 <= (3/2) H^2. So the Jeans length is at least the Hubble length,
    and the clock cannot cluster inside the horizon.
  - QX3's C2 puts the largest (k_J / k)^2 at 0.0065.
- **My check:** CLASS-free Newtonian-gauge fluid code (Ma & Bertschinger, phi = psi, adiabatic start at a = 1e-6, to
  z = 1100) on the B2 canonical best fit.

| k (/Mpc) | delta_dust | Q_X1 (clock, rho_DE, w -0.95) | Q_X2 (stiff, the full cold density) |
|---|---|---|---|
| 0.02 | -8.79 | 3.4e-11 | 0.0109 |
| 0.05 | -26.8 | 3.7e-12 | 0.0016 |
| 0.10 | -49.7 | 8.1e-13 | 0.0007 |
| 0.20 | -81.9 | 1.8e-13 | 0.0003 |
| 0.30 | -108.1 | 8.6e-14 | 0.0002 |

- KA-G4 (X = dust) gives Q = 1.000 at every k.
- Even a stiff field holding the whole needed density gets at most 0.16 % of the dust's density contrast for
  k >= 0.05. The baryon contrast drops by up to half without the cold dust: -19.5 vs -26.8 at k 0.05, -50.5 vs -108.1 at
  k 0.3.
- The no-go's sign is reproduced: a c_s^2 = 1 component cannot stand in for the cold one at recombination.

## Known answers and MUTATE (f1a_MUTATE.json)

**Known answers (all PASS):**
- KA-A: 790.965 (vs 790.96).
- KA-P: 11321.687 (vs QX15's 11321.74).
- KA-G4: Q = 1 within 1e-3.

**M1 (baryons-only must fail by QX15's Delta): PASS.**
- DeltaMB +172,915.6 / +166,674.4 against QX15's +172,848 / +166,612.
- The ratio is 1.0004 on both footings. My independent likelihood reproduces the record's number to 0.04 %.

**M2 (omega_b 0.0300 at the cold best fit): PASS.**
- The first TT peak moves from ell 221 to 224 / 225.
- chi2(PA) rises by +11,982 / +13,211.

## Disclosed

- **Theory code (A1).** CAMB is the Boltzmann code, as QX15's is. The audit's independence is in the likelihood code
  (own CamSpec and ACT SACC readers), the background rule, the fits and the CLASS Pcut check.
  - CLASS and CAMB differ by 3.8 on Pcut at the cold fits, and by 0.7 on B1.
  - At the baryons-only fits they differ by 177-212, on chi2 near 1e5 (0.2 %). This does not touch any line.
- **The baryons-only fits are pinned at bracket edges:**
  - n_s at 1.3 (B2) and tau at 0.15 (B1, alt B2).
  - Foreground amplitudes at 50, calibrations at 1.1, and A_act up to 1.31.
  - QX15's MB fit was also at the n_s edge. Wider brackets could lower chi2_MB, but a deficit of ~1.7e5 cannot close
    to 25. The same holds for QX15.
- **Nelder-Mead budget.** Two starts of 300 evaluations. The cold fits land on QX15's best fit independently, and the
  B2 MB fits used 564-600 evaluations.
- **Warnings.** run_fits.log (local, gitignored) carries numpy matmul RuntimeWarnings (Accelerate BLAS). Every chi2 is finite, and the
  known answers pass at the same code path.
- **B1 is run once.** a0 does not enter B1, so it is the same for both footings, as frozen.

## One sentence

An independent likelihood (own CamSpec NPIPE and ACT DR6 readers) on the footing background reproduces F1:
- baryons-only fails by +172,916 / +166,674 chi2 (QX15's numbers to 0.04 %);
- the cold fit beats the published test cosmology by 65 chi2;
- the needed amount is omega_d / omega_b = 5.41, 2.7 % under the record's 5.56;
- own Newtonian-gauge code shows a c_s^2 = 1 clock reaching at most ~1e-11 of the dust contrast at z 1100;
- F1's fits never touch the k^-4-less Limber kernel, which only QX15's cell readings use.

Kappa = 1/2 FITTED; not theory closed.
