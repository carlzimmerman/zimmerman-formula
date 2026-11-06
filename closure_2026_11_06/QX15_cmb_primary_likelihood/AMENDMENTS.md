# QX15 amendments

Kappa = 1/2 FITTED; not theory closed.

## A1 (after the KA code checks, before any graded model number)

**KA-P as frozen: FAIL.** At the frozen high accuracy (CAMB 1.6.6, lmax 9000, lens_potential_accuracy 8), my CamSpec
chi^2 at Cobaya's published NPIPE test point is 11321.74, against 11337.34 (-15.60; line 1.0). That reading stays on
the record (logs/ka.txt, parts/ka.json). KA-A passes: 790.965 against 790.96 (+0.005).

**Cause: theory settings, not the likelihood code.** The published number is computed with Cobaya's own CAMB setup:
- set_for_lmax(2500, lens_potential_accuracy 1);
- halofit mead2020, BBN PArthENoPE_880.2, recfast_approx_model 'planck', nnu 3.044;
- CAMB 2.x (Cobaya master).

I installed CAMB 2.0.5 from PyPI in an isolated scratch venv and ran the test with those settings, then fed the
spectra to this lane's likelihood code (qx15_like.py, unchanged). Result: **11337.337 against 11337.34 (-0.003)**.
The CamSpec likelihood re-implementation is therefore verified, and KA-P is read as PASS by this amendment. The frozen
FAIL reading is disclosed above. Script: the KA-P2 check below, run in the scratch venv; it is not part of the graded
pipeline.

**Fit precision changed, lens_potential_accuracy 1 to 4.** The test showed that lensing precision moves chi^2 by about
10 on full CamSpec. I checked PA at the published calibration point only, which is not a graded model, with CAMB
1.6.6 and nuisances fixed:
- lpa 1 / lmax 7000 differs from lpa 8 / lmax 9000 by about 2.9 (Pcut +0.77, A -2.14), which would fail K-acc
  (line 2).
- lpa 4 / lmax 7000 is within 0.05.

All fits therefore use lmax 7000 and lpa 4. K-acc is unchanged: fit precision against lmax 9000 / lpa 8 at each main
best fit, |diff| <= 2. Two main fits had already started at lpa 1; I killed them before reading any number. Their logs
are kept, unread, in logs/killed_lpa1/.

**Cell S(L).** The solver's full k-grid coverage ends at L = 917 for all four cells. Below that edge, S declines
smoothly and monotonically (C3: 0.991 at L 100, 0.87 at 400, 0.49 at 900). Beyond it S is held at S(917), as frozen.
For Jeans suppression, holding understates the high-L suppression. QX10's S_L1000 of about 0.999 came from partial
z coverage past the edge; it is not physical.

## KA-P2 script (scratch venv, CAMB 2.0.5)

    p.set_cosmology(ombh2=0.02235048, omch2=0.12121379, cosmomc_theta=1.04240171e-2, tau=0.05, mnu=0.06,
                    num_massive_neutrinos=1, nnu=3.044, bbn_predictor='PArthENoPE_880.2_standard.dat')
    p.InitPower.set_params(As=exp(3.04920413)*1e-10, ns=0.96399503)
    p.set_for_lmax(2500, lens_potential_accuracy=1); p.NonLinearModel.set_params(halofit_version='mead2020')
    p.Recomb.set_params(recfast_approx_model='planck')
    -> qx15_like.CamSpec(P_FULL).chi2(D, published nuisances) = 11337.337
