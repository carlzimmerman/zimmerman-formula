# AGB4 — the progenitor-age slope on published host ages (SDSS-II hosts, Pantheon+ magnitudes) (FROZEN, before any number)

2026-11-14. Owner: "Yes, look them up", "keep swinging", then a yes to three downloads. A test of a published claim
on public data. It adopts nothing and edits no ledger. No script of this lane is in the repository when this file is
committed.

## Why
AGB2 and AGB3 had to turn host mass or star-formation rate into an age with a model. The published slope,
0.030 mag/Gyr (Son et al., arXiv:2510.13121; "S25"), was measured against **host ages from fits to SDSS-II host
photometry** (the ages of Gupta et al. 2011 and Rose et al. 2019, as compiled by Chung et al. 2025). Those ages are
public for every SDSS-II supernova host. So the slope can be tested on the same kind of age it was measured on,
with **no age model**, in the uniform Pantheon+ magnitudes.

## Data
1. `sdsssn_master.dat2`, 9,420,067 bytes, sha256 fcf3c561…ae2803ae, from
   `data.sdss.org/sas/dr10/boss/papers/supernova/` (Sako et al. 2018): 10,258 SDSS-II candidates; host columns
   `age_Ravi` with `age_lo_Ravi`, `age_hi_Ravi` (FSPS fits after Gupta et al. 2011; Gyr), `logMass_Ravi`,
   `logSSFR_Ravi`, `age_Mat` (PEGASE fits); the table's own SALT2 fit (x0, x1, c, muerr).
2. Rose et al. (2019), `github.com/benjaminrose/MC-Age` (branch master): `results-summary.csv` (3,444 bytes; local
   and global ages of 103 hosts), `campbell_local.tsv`, `campbell_global.tsv`, `gupta_global.tsv`.
3. Pantheon+ (on disk, as in AGB2).
All fetched 2026-11-14 with the owner's yes, into `_external_data/agb4_sako2018_master/` and `agb4_rose2019_ages/`.
A third file the owner approved, the supplementary table of Chung et al. (2025, MNRAS 538, 3340), could not be
fetched: the publisher's site refused the automated request (HTTP 403) and that was not worked around.

**Samples.** `pp` (primary): the 321 Pantheon+ SDSS supernovae (IDSURVEY 1) matched to the Sako table by SDSS id,
with an FSPS age and a positive lower bound: 286 supernovae, z 0.07–0.38; 32 % in low-mass hosts; 86 hosts above
6 Gyr, 14 above 8. `rose`: the 66 of them with Rose ages. `big`: every SDSS-II object typed SNIa or zSNIa with an
FSPS age, the table's own SALT2 fit, |x1| < 3, |c| < 0.3 and 0.03 < z < 0.45: 1,092 (387 spectroscopic).

**What was looked at before this freeze.** The host columns, redshifts, types, stretch and colour, and the match:
all 321 matched; Pantheon+ and FSPS masses correlate at 0.85 with no offset; FSPS age against stretch correlates at
−0.47 and the share of low-stretch supernovae (x1 < −1) is 0.03, 0.06, 0.35, 0.47 for ages 2–4, 4–6, 6–8, 8–14 Gyr,
so these ages do sort progenitors; the PEGASE ages do not (correlation with stretch −0.11). Design-only forecasts.
**No magnitude has been fitted against any age.** The author knows the results of AGB1, AGB2, AGB3 and its post hoc
sections.

## The fit
Weighted least squares (AGB2 amendment 1), inside equal-count redshift bins:
y_i = Σ_b o_b [z_i in bin b] + g (L_i − ½) + A × D_i + a x1_i + b c_i, with **D_i = −0.030 mag/Gyr × (host age of i)**.
A = 1 is the published slope; A = 0 no dependence on host age. L_i = 1 for log M < 10 (Pantheon+ mass).
- `pp`: y = mB − μ_fid (reading R, primary; a, b free) or m_b_corr − μ_fid (reading P, no a, b); weights 1/C_ii of
  the Pantheon+ covariance; 8 bins. μ_fid flat Ω_m = 0.334.
- `big`: y = −2.5 log₁₀ x0 − μ_fid, a and b free; weights 1/(muerr² + 0.1²); 16 bins; mass from `logMass_Ravi`.
- `rose`: as `pp` with the Rose global age (and the local age), 4 bins.

**Frozen words (judged on `pp`, reading R, FSPS ages).**
- **M0, no mass step (g = 0).** This is how the published slope was measured. AGB3's U words:
  SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA if Â < 1 and Δχ²(A=1) ≥ 9; SLOPE OVERPREDICTS THE HOSTS (2 SIGMA) if Â < 1
  and 4 ≤ Δχ²(A=1) < 9; HOSTS AS LARGE AS THE SLOPE NEEDS if Δχ²(A=1) < 4; HOSTS LARGER THAN THE SLOPE NEEDS if Â > 1
  and Δχ²(A=1) ≥ 4.
- **M1, mass step free.** AGB1's W1 words on Δχ²(A=0), Δχ²(A=1) (AGE BIAS EXCLUDED AT 3 SIGMA / DISFAVOURED / REQUIRED
  AT 3 SIGMA / FAVOURED / UNDECIDED / NEITHER).
- Second word of each: ROBUST if the same first word comes out, one change at a time, for reading P; 12 bins; the
  sample `big`; and `pp` without the hosts whose stated age interval is wider than ± 2.5 Gyr; else FRAGILE naming which.
- **Power from the design alone:** σ_A = 0.19 (M0) and 0.21 (M1).

**Reported only.** The Rose global and local ages (forecast σ_A 0.24, 0.25); the PEGASE ages; `big` restricted to
its 387 spectroscopic supernovae; the split of the template at 6 Gyr (amplitude below and above); the low-stretch
share against age; the reliability of the FSPS age from stretch and host mass as witnesses (AGB3's post hoc method)
and the amplitude divided by it. On that last row: the published slope was itself measured on ages of this kind,
noise included, so the like-for-like comparison is the uncorrected one.

## Known-answer checks (judged before the words are read)
- **K1, the match.** All 321 Pantheon+ SDSS rows found by id; |zHD − table redshift| ≤ 0.03 for every row of `pp`;
  correlation of Pantheon+ mass with FSPS mass ≥ 0.80 (computed 0.85).
- **K2, the ages sort progenitors** (stretch only, no magnitude): low-stretch share for age ≥ 6 Gyr minus the share
  below 6 Gyr is at least 0.15 on `pp` (computed 0.32).
- **K3, mutation twins (exit 3 on pass, 4 on fail).** y replaced by fixed bin offsets + 0.05 (L − ½) where the step
  is free − 0.15 x1 + 3.1 c + A_true × D, A_true = 1 and 0, for M0 and M1 on `pp` and on `big`. Pass each:
  |Â − A_true| ≤ 10⁻⁶ and χ²_min ≤ 10⁻⁸.
- **K4, the error bar.** `pp`, reading R, M0 and M1: ages (with their host mass) shuffled among supernovae inside
  each redshift bin, seed 20261117, 400 draws: |mean Â| ≤ 0.2 σ_A, shuffle scatter within [0.8, 1.25] σ_A, and the
  sandwich error from the residuals within [0.8, 1.25] σ_A. Judged per configuration.
- **KR, Rose et al.'s own result (does not void the lane).** Their distance moduli (`campbell_local.tsv`) against
  their local ages: mean Hubble residual of hosts younger than 8 Gyr minus that of hosts older, after removing a
  flat Ω_m = 0.3 Hubble line: within 0.04 of their published 0.114 ± 0.039 mag (older hosts brighter). If it fails,
  only the Rose rows are NOT EVALUABLE.
M0 and M1 are NOT EVALUABLE if K1, K2 or K3 fails; a configuration that fails K4 loses its own word. Numbers are
still reported as a reading.

## What the result may and may not say
- 286 supernovae at z < 0.4, one survey. The word is about these hosts and these ages.
- The ages are fits to five-band host photometry and carry errors of about ± 1.7 Gyr against a spread of 1.6 Gyr
  inside a redshift bin. That shrinks any slope. The published slope was measured on such ages, so A = 1 is the
  like-for-like prediction; the noise-corrected row is reported beside it, not in its place.
- S25's own Hubble residuals and their exact list of 300 hosts were not available (see Data). This lane uses the
  same family of ages on the Pantheon+ standardisation of the SDSS spectroscopic sample, not their residuals.
- A host-age slope is not proof that age causes it; dust in young hosts is the usual alternative.
- Words are read as one degree of freedom (4 = 2σ, 9 = 3σ). AGB1's, AGB2's and AGB3's words stand as written.
- Nothing here grades this repository's framework; no a0 is used.

## Files and order
`agb4_data.py` (loaders), `agb4_run.py MODE` (checks and fits), `agb4_collect.py`. This file is committed alone,
before any script. The scripts are committed next, before any real-data number; until then only K1, K2, the
forecast and the K3 twins are run, in a scratch copy. Any change after this commit is a dated amendment committed
alone before the re-run, and both readings are reported.

kappa = 1/2 FITTED; not theory closed.
