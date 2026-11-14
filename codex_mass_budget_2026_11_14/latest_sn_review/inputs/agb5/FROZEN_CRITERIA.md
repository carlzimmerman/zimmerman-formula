# AGB5 — the published age slope on the claim's own table, with a host-mass step allowed (FROZEN, before any new number)

2026-11-14. Owner: "I'll download it", then the file. A test of a published claim on its own published data.
It adopts nothing and edits no ledger. No script of this lane is in the repository when this file is committed.

## Why
AGB4 tested the slope on the same family of host ages in Pantheon+ magnitudes, and said a like-for-like run on the
claim's own table was still owed. The table is now on disk: the host ages and Hubble residuals of Chung et al.
(2025, MNRAS 538, 3340), which Son et al. (arXiv:2510.13121; "S25") take their 0.030 mag/Gyr from.
Chung et al. state that no mass-step correction was applied to those residuals. **So the question is one fit away:
on their ages and their residuals, does the slope survive when a host-mass step is allowed beside it?**

## Data
1. `staf497_supplemental_file.zip`, 5,118 bytes, sha256 c98883ad…44c40f04, downloaded by the owner from the journal
   page (DOI 10.1093/mnras/staf497) on 2026-11-14; copied to `_external_data/agb5_chung2025_ages/` and unpacked:
   `table1.dat` (199 hosts, the Gupta et al. 2011 sample: SDSS id, host age, age error, Hubble residual with the
   original value in brackets, residual error) and `table2.dat` (102 hosts, the Rose et al. 2019 sample: same
   columns, one residual). 33 hosts are in both; 268 different hosts in all.
2. The SDSS-II table of Sako et al. (2018), on disk since AGB4: host mass `logMass_Ravi` (for 187 of the 199 and 101
   of the 102), redshift, stretch. Pantheon+ (for one reported row).

**What is known from the paper** (web reading, PROVISIONAL): table 1's first residual carries a redshift correction
fitted on young hosts, the bracketed one is the original; table 2's residuals are from Campbell et al. (2013);
neither has a mass-step correction. Published slopes, mag/Gyr: with errors in both variables (LINMIX)
−0.062 ± 0.014 (table 2), −0.047 ± 0.015 (table 1), −0.037 ± 0.015 (table 1, original residuals); with their
hierarchical model −0.038 ± 0.007 (table 2), −0.025 ± 0.006 (table 1). The weighted mean of the last two is
−0.030 ± 0.005, the number S25 use.

**What was computed before this freeze: the published configurations only, as known-answer checks.**
- A plain weighted line (weights 1/(σ_HR² + 0.10²)) gives −0.0385 (table 2) and −0.0246 (table 1), the published
  hierarchical slopes to the third decimal. So 0.030 is, in effect, the plain slope.
- A structural fit with the stated age errors (`agb5_eiv.py`; the one-Gaussian case of LINMIX) gives
  −0.0626 ± 0.0136, −0.0482 ± 0.0154 and −0.0388 ± 0.0156, the three published LINMIX slopes.
- With no residual involved: the stated age errors (mean square 4.4 and 4.8 Gyr²) exceed the whole variance of the
  ages (4.0 and 4.3 Gyr²), so they cannot all be random error; stretch and host mass as witnesses give a reliability
  of 0.85 ± 0.14 (table 1) and 1.0 ± 0.35 (table 2). Low-mass hosts average 3.1 and 3.4 Gyr, the others 5.5 and
  6.2 Gyr; age and the low-mass flag correlate at −0.57 and −0.59.
- Design-only errors of the slope: 0.0051 and 0.0061 mag/Gyr with no step, 0.0067 and 0.0075 with a step free.
**No fit with a mass step has been run.** The author knows the results of AGB1 to AGB4.

## The fits
Per table: HR_i = α + β × age_i + g (L_i − ½), L_i = 1 for log M < 10 (FSPS mass of the SDSS-II table; hosts without
one are left out of the step fits). A = β / (−0.030 mag/Gyr), so A = 1 is the published slope.
- **Plain** (primary; it is what reproduces 0.030): weighted least squares, weights 1/(σ_HR² + 0.10²).
- **Structural** (errors in both variables as stated): `agb5_eiv.py`, a separate mean age for each mass group when
  the step is free.
- **Combined:** the inverse-variance mean of the two tables' slopes (what S25 did). The 33 shared hosts are
  counted in both, as in the published number; a fork drops them from table 1.

**Frozen words.**
- **L1, plain line with a mass step free, the two tables combined:** AGB1's W1 words on Δχ²(A=0), Δχ²(A=1), each
  (Â − a)²/σ² (AGE BIAS EXCLUDED AT 3 SIGMA / DISFAVOURED / REQUIRED AT 3 SIGMA / FAVOURED / UNDECIDED / NEITHER).
  Second word: ROBUST if the same first word comes out, one change at a time, for: table 1 alone; table 2 alone; the
  shared hosts dropped from table 1; table 1 with its original residuals; a redshift term added (HR also linear in z);
  the structural fit in the place of the plain line; else FRAGILE naming which.
- **L0, the same with no mass step** is a check, not a word (KA below): it must return A = 1.
- **Power from the design alone:** σ_A = 0.17 with the step free (0.13 without).

**Reported only.** The step g with and without the age term, per table; the slope inside each mass group; the
structural fit with the stated age errors scaled by 0.5 and by 0; the plain slope on Pantheon+ magnitudes for the
hosts of either table that are in Pantheon+ (AGB4's fit, 8 redshift bins, with these ages), with and without a step.

## Known-answer checks (judged before the word is read)
- **KA, the published slopes.** Plain line, no step: within 0.004 mag/Gyr of −0.038 (table 2) and −0.025 (table 1),
  and the combined slope within 0.004 of −0.030. Structural fit, no step: within 0.004 of −0.062, −0.047 and −0.037.
  (Computed above: all six inside 0.002.)
- **K1, the tables.** 199 and 102 rows parsed, 33 shared; every id found in the SDSS-II table; table 1's two
  residual columns differ (the correction is there).
- **K3, mutation twins (exit 3 on pass, 4 on fail).** HR replaced by 0.1 + 0.05 (L − ½) + A_true × (−0.030 × age), no
  noise, A_true = 1 and 0, both tables, plain fit with the step free: |Â − A_true| ≤ 10⁻⁶.
- **K4, the error bar.** Plain fit with the step free, each table: ages and masses shuffled together among hosts
  (seed 20261118, 400 draws): |mean Â| ≤ 0.2 σ_A and shuffle scatter within [0.8, 1.25] σ_A; and the error from a
  bootstrap over hosts (400 draws) within [0.8, 1.25] σ_A.
L1 is NOT EVALUABLE if KA, K1, K3 or K4 fails; numbers are still reported as a reading.

## What the result may and may not say
- Age and mass are tied together in these hosts (correlation −0.6). If the slope falls when a step is allowed, the
  data cannot tell a 0.030 mag/Gyr age law from a step in mass; that does not prove mass is the cause. If it stays,
  the published slope survives the standard correction on its own data.
- The residuals are the published ones, from two older analyses; nothing is re-standardised here except in the one
  reported Pantheon+ row.
- 268 hosts at z < 0.4. Words are read as one degree of freedom (4 = 2σ, 9 = 3σ).
- The paper's method details are a web reading. The known-answer checks show the tables and the two estimators
  reproduce its numbers.
- AGB1's to AGB4's words stand as written. Nothing here grades this repository's framework; no a0 is used.

## Files and order
`agb5_data.py` (loaders), `agb5_eiv.py` (structural fit), `agb5_run.py MODE` (checks and fits), `agb5_collect.py`.
This file is committed alone, before any script. The scripts are committed next, before any fit with a mass step.
Any change after this commit is a dated amendment committed alone before the re-run, and both readings are reported.

kappa = 1/2 FITTED; not theory closed.
