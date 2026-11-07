# F1A amendment A1 (before any graded number)

Kappa = 1/2 FITTED; not theory closed.

**What was seen before this amendment.** KA-A 790.965, KA-P 11321.69, and my chi2_cal 3802.38 (CLASS theory). Also memory:
- CLASS at l_max_scalars 6900-7500 with lensing peaks at 0.94-1.36 GB RSS by itself, which breaks the < 1 GB rule.
- CAMB 1.6.6 at lmax 7000 (lens_potential_accuracy 1) peaks at 0.21 GB and takes 0.3 s.

KA-P peaked at 1.81 GB for 10 s. The full float32 covariance plus the mapped file was resident; no 1024^3 run was live.
That is disclosed. KA-P is not rerun.

**Change.** Every graded fit uses CAMB 1.6.6 as the theory code: lmax 7000, lens_potential_accuracy 1, linear lensing
(NonLinear_none), N_eff 3.046, no massive neutrinos. CLASS is kept as an independent theory check:
- at each best fit, CLASS at l_max 3500 (inside 1 GB) recomputes the Pcut part;
- the CAMB-vs-CLASS difference in chi2(Pcut) is reported.

chi2_cal is recomputed with CAMB at the Cobaya NPIPE test cosmology (cosmomc_theta as published, mnu 0.06). The CLASS
value 3802.38 is reported.

**Not changed.** Lines, labels, backgrounds, likelihood code, MUTATE. The likelihood code stays independent of QX15's.
The theory code is now the same Boltzmann code as QX15 (CAMB), so the audit's independence is in the likelihood, the
background rule and the fits, plus the CLASS check on Pcut. This is disclosed.
