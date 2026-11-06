# QX15: likelihood-level primary CMB (Planck PR4 CamSpec + ACT DR6 CMB-only)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

Criteria: FROZEN_CRITERIA.md (local 1df9dcc3e9, origin 3ae5192a6b), committed and pushed before any graded number.
Amendments: AMENDMENTS.md. A1 was made before any graded number; A2 is post-result and disclosed.

Scripts:
- qx15_like.py: a reusable grader. It takes a dict of D_ell TT/TE/EE spectra and returns profiled chi^2 for P (full
  CamSpec), Pcut and A (ACT); PA = Pcut + A.
- qx15.py: the runner.

Outputs: qx15.json/.out; qx15_MUTATE.json/.out; parts/; logs/.

The owner approved the data download in chat on 11-06.

## Labels (both footings, never pooled)

| Quantity | canonical | alt | Line | Label |
|---|---|---|---|---|
| L1: footing background + cold component, PA, Delta vs chi2_cal (3805.80) | 3741.08, Delta -64.72 | 3741.15, Delta -64.65 | <= 9 PASS | **PASS** |
| K-acc (lmax 7000 / lpa 4 vs lmax 9000 / lpa 8) | +0.190 | +0.191 | <= 2 | pass |
| (a) Control: baryons-only + the law (MB), Delta | +172,848 | +166,612 | > 25 FAIL required | FAIL, **bites** |
| P1 power control (flat S = 0.5), Delta_cell | +192.5 | +189.9 | > 25 required | **bites** |
| Cell C1 (2.61 Mpc, p 4.25), Delta_cell | +0.66 | +0.67 | <= 4 PASS | **PASS** |
| Cell C2 (1.47, 3.5) | +0.27 | +0.28 | <= 4 | **PASS** |
| Cell C3 (8.25, 5.625) | +5.95 | +6.03 | 4-25 | **TENSION** |
| Cell C4 (2.15, 3.75) | +0.57 | +0.58 | <= 4 | **PASS** |
| MUTATE M-A (p = 0, smooth sector; CLASS) | +35,081 | +34,937 | > 25 FAIL required | FAIL, **bites** (fits sit on the n_s = 1.3 bracket edge; any fit they could reach is far worse) |

Best fits:
- canonical: h 0.6741, omega_b 0.02236, omega_d 0.1209, ln(1e10 A_s) 3.062, n_s 0.9674, tau 0.063.
- alt: h 0.6740, with the same parameters to 1e-4.
- tau is free; there are no low-L data.

Reported, not graded, at each main best fit with nuisances re-profiled (parts/report_P_A.json):
- full CamSpec TTTEEE: chi^2 10552.6 / 10552.4 for N = 9915;
- ACT alone: 159.0 / 159.4 for N = 135.
- For comparison, at the published NPIPE test cosmology: 10603.7 and 196.7.

## What this does to the record

- **QX10 iter_1's NO VERDICT is replaced.** iter_1 failed J1, its conservative late-lensing bound, on every cell. At
  the likelihood level, with the cell's own Jeans suppression S(L) applied to C_L^phiphi and a local refit:
  - C1, C2 and C4 are harmless (Delta_cell <= 0.67);
  - C3 is a TENSION (+6).
  - The planted flat 50 % suppression costs about +190, so the test has power.
- **The footing background passes L1 at the likelihood level on both footings.** h is fixed by a0 (0.674), with a
  cold component.
- **The window stays KILLED by QX10 G6** (host galaxies retain the sector, and KiDS lensing is over-predicted). This
  lane sharpens only the CMB side: the sector's primary-CMB and lensing footprint is not what kills it.
- **This is not independent evidence (QX10's disclosure carries over).**
  - Both footings give h = 0.674 because their a0 values were built from the dark-energy and total densities.
  - A component that is cold at z >= 10 gives the standard cold-component primary spectrum.
  - The PASS shows that the framework's fixed-h background and the sector do not spoil PR4 + ACT. It does not show
    that the framework predicts the peaks.

## Known answers

- **KA-A: PASS.** The ACT-lite test point gives 790.965 against 790.96.
- **KA-P as frozen: FAIL**, -15.60 at the frozen high accuracy with CAMB 1.6.6. A1 traces this to theory settings,
  not the likelihood code. With the published test's own settings, CAMB 2.0.5 in an isolated scratch venv installed
  from PyPI, this lane's unchanged likelihood code gives **11337.337 against 11337.34**. KA is read through that
  check (KA-P2, parts/ka_p2.json).
- **Side finding, at the same published test point.** Profiling the nuisances lowers the CamSpec chi^2 by 732, from
  11337.3 to 10605.5: amp_143 16.9 against 10.4, and amp_217 10.7 against 18.7. The published nuisances are a code
  test point, not the CamSpec-only optimum. This doesn't touch any label, because chi2_cal and every graded fit are
  profiled in the same way.
- **Custom-lensing path.** At S = 1 it reproduces CAMB's standard lensed spectra (Delta chi^2 0.000).

## Disclosed

- A1: KA-P FAIL as frozen; KA-P2; fit precision changed from lpa 1 to lpa 4, chosen at the calibration point only;
  two lpa-1 fits killed unread (logs/killed_lpa1/).
- A2: the first MB fits returned NaN. CAMB's HMCode fails at omch2 ~ 0, and the NaN poisoned the fit's best-point
  tracker. The first grade printed that NaN as "FAIL / bites", which was void. The fix is linear lensing for MB, as in
  QX10's CLASS MB; the MB fits were then rerun. The first files are in logs/MB_nan_first/.
- One crash fix before any cell number: CAMB needs C_L^phiphi out to Params.max_l (logs/crash_clpp_maxl/).
- The cell S(L) values come from QX10 jcheck's Limber solver (read-only reuse). Full k-grid coverage ends at
  L = 917, and S is held beyond that, as frozen. That understates the high-L suppression.
- There are no low-L data (no L < 30 TT, no low-L EE). The CMB-only data cannot settle tau.
- numpy on macOS Accelerate raises spurious "divide by zero in matmul" flags. They are suppressed; every value is
  finite and checked.

## Data (owner-approved; _external_data/qx15_cmb_primary/, not committed)

Total downloaded: 91,246,221 bytes (91.2 MB) of data plus reference source text. Additionally, the camb 2.0.5,
numpy, scipy and astropy wheels from PyPI went into an isolated scratch venv for KA-P2 only.

Key files:
- CamSpec_NPIPE.zip: 85,421,478 bytes, sha256 1978dd0c148a87678b4cf07340401814a3bc81b5cb87dbdccb76565a3a883e15
  (github.com/CobayaSampler/planck_native_data release v1).
- dr6_data_cmbonly.tar.gz: 286,990 bytes, sha256 3f057c2569211ada03759530b74848b322edc3d68d66b6b8c2db0679547dbbd8
  (lambda.gsfc.nasa.gov/data/act/pspipe/sacc_files/).
- act_dr6_cmb_sacc.fits: 5,391,360 bytes, sha256 9506da7b…19ad (ACTCollaboration/DR6-ACT-lite repo copy; not
  used for grading).
- The rest is the Cobaya and ACT likelihood source, read as text only (never executed): planck_2018_CamSpec_python.py,
  the NPIPE CamSpec yaml/py files, test_cosmo_planck_NPIPE.py, test_cosmo_planck_2018.py, common_cosmo.py,
  input_database.py, camb.py, act_dr6_cmbonly.py, test_act.py and PlanckActCut.py.

The full URL, size and sha256 list is in download_log.txt, copied to this lane as download_log.txt.
