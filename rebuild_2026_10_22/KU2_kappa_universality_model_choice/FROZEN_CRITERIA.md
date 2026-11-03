# KU2_kappa_universality_model_choice — FROZEN CRITERIA (before any script or number)

Question: KU1 found NO POWER because the ten DynPop JAM models disagree on the slow-minus-fast offset (HDUs 6-7 give +0.24,
the other eight -0.04 to +0.07; statistical error 0.018). Does choosing the model per galaxy by DynPop's own fit quality settle
it?

κ = 1/2 FITTED. Footings 9.3603e-11 and 1.1312e-10, never pooled. Not theory closed. Nothing here says the data favour the
framework. No download (same file as KU1).

**Not blind:** KU1's per-model D values above are known. I have **not** looked at chi2_dof in any model, nor which model fits
which class better. Excluding HDUs 6-7 by hand would be tuning to KU1's result, so it is not allowed as a primary.

## Unchanged from KU1
Sample cuts, slow/fast definition (Cappellari 2016), r_half accelerations, M* (NSA elpetro, log as stored, no h conversion),
board law with simple nu, matched cells (0.2 dex M*, 0.1 dex sigma_Re), D statistic, bootstrap (2000), M* systematic, labels
(NO POWER if sigma_D > 0.06; UNIVERSAL |D| <= 2 sigma; DIFFERS > 3 sigma; NOT SEPARATED between), checks C1-C3, MUTATE.

## Changed: the mass model
- **Primary:** for each galaxy, the model with the lowest chi2_dof among the ten (finite chi2_dof and log_Mt_rhalf required;
  ties go to the lower HDU number). Its log_Mt_rhalf and rhalf_arcsec are used.
- **sigma_model** = |D(primary) - D(second-lowest chi2_dof per galaxy)|, replacing KU1's spread over all ten.
- Printed: the fraction of slow and of fast galaxies whose chosen model is each HDU; the median chi2_dof of the chosen and
  second models.
- **Beside, not graded and labelled post-hoc:** D with HDUs 6-7 removed from the ten (median of the other eight), and D with
  only HDUs 6-7.

## Reading rule stated in advance
If the chosen model is HDU 6 or 7 for one class far more often than for the other, the class difference in D is at least
partly a model-selection effect; this is printed and stated beside the label, not used to change it.

## Checks (added to KU1's)
- C4: every galaxy in the sample gets a chosen model; no NaN in the chosen log_Mt_rhalf.
Exit 0 only if C1-C4 pass. MUTATE writes `*_MUTATE.*`, exit 1.
