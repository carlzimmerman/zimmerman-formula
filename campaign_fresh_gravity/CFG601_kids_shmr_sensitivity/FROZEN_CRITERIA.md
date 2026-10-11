# CFG601 FROZEN CRITERIA: how far the KiDS verdicts move when the SHMR is swapped, scaled or removed (CFG594 flagged this unchecked)

Written 2026-10-10 before any CFG601 script exists or any CFG601 number is computed. Inputs read so far are committed results only.

Standing settings as CFG600 (kappa = 1/2 FITTED; footings never pooled; nu_mono; candidate B; cold energy mass required; nothing downloaded; nice 10; not "theory closed"; RAW data vs framework-native only).

## 1. Where the SHMR enters (from the code, CFG529 / CFG531)
(i) the HOD leaked-satellite environment grid E (per SHMR, scaled to the measured f30 fraction 0.1686); (ii) the stripping window and mixing fraction of the own profile (fo, tr_W30); (iii) the rank-one covariance term delta delta^T (behroozi - moster). The law's own profile uses the baryon mass and r_ta,law and has NO SHMR.

## 2. Variants (machinery as CFG600, read-only)
- **S0 base:** CFG531 as committed (moster model, delta in the covariance).
- **S1 swap:** Moster alone (no delta) and Behroozi alone (model = behroozi, no delta).
- **S2 scale:** the leaked fraction used in E and in the own mixing scaled by 0.5 and 1.5 (proxy for the SHMR normalisation uncertainty; clipped to [0, 1]); the HOD grid shape unchanged.
- **S3 removed (bound, no verdict weight):** E = 0, no stripping (own = full), no delta. CFG529 showed the environment is needed for validity; this row bounds the SHMR-driven part only.
Statistics per variant, per construction and footing: eps K-in, K9 (Z); CENSUS chi2 and p; the early-minus-late K9 difference and the CFG531 CARRIED label.

## 3. Verdict (per footing, over S1 and S2 only)
- **ROBUST TO THE SHMR:** the K9 significance class (Z >= 3 or not, both constructions) and the CARRIED label are unchanged in every S1 and S2 variant.
- **SENSITIVE:** any S1 or S2 variant changes the K9 class or the CARRIED label.
Also report, from committed JSON only, CFG536's Moster vs Behroozi held-out Z (swap only; CFG536 is not re-run).

## 4. Controls and MUTATE
- K1: S0 reproduces CFG531's committed BASE eps and CARRIED labels (1e-6).
- K2: S1 Moster-alone reproduces S0 with delta set to zero analytically (same model, different covariance), reported.
- **MU1:** scale the leaked fraction by 3 (a deliberately wrong SHMR); the K9 class or the census chi2 must change on at least one footing, else the test has no teeth.
- **MU2:** shuffle the lens stellar masses entering the weights between groups is not available without a table rebuild, so MU2 = S3 removed with the data's covariance unchanged must differ from S0 by more than 1 sigma in eps on at least one footing; if not, the SHMR term is irrelevant by this statistic and is reported as such.
