# AGB3 — the progenitor-age slope against the DES hosts' measured star formation, and the sample's own age drift (FROZEN, before any number)

2026-11-14. Owner: "Yes, look up the DES host table", then "swing harder bro", then a yes to one download.
A test of a published claim on public data. It adopts nothing and edits no ledger. No script of this lane is in the
repository when this file is committed.

## Why
AGB1 measured the size of the Son et al. (arXiv:2510.13121; "S25") age correction from distances and left it
undecided. AGB2 tested the same slope on Pantheon+ host **masses**; its main weakness, stated there, is that host mass
may track progenitor age poorly, and its least model-bound word stayed undecided.
The DES team's per-supernova table carries, for every supernova of the Dovekie Hubble diagram, the host's stellar
mass **and its specific star-formation rate and rest-frame colour**. Star formation is what separates young
progenitors from old ones, so this table lets four sharper questions be put:
1. **Slope.** At one redshift, do supernovae in hosts whose measured star formation says "old" come out brighter
   than those in hosts that say "young", by the amount 0.030 mag/Gyr requires?
2. **Upper limit.** If every bit of what hosts do to supernova brightness is handed to age, how large can the slope be?
3. **The sample's own drift.** S25 applied the age history of the average galaxy in the universe. What do the ages of
   *these* hosts do with redshift, and what happens to "accelerating today" when the published slope acts on that?
4. **Young hosts only.** S25's own "evolution-free" test: with only supernovae in young, coeval hosts, is the
   expansion speeding up today?

## Data
1. **DES-Dovekie_Metadata.csv**, 1,269,831 bytes, sha256 45ad71f8…32c75388, fetched 2026-11-14 with the owner's yes from
   `github.com/des-science/DES-SN5YR`, branch `main`, folder `4_DISTANCES_COVMAT` (last commit touching the file
   f694603d1d, 2025-11-14); stored in `_external_data/agb3_des_dovekie_metadata/`. 1,820 rows, one per supernova.
   Columns used: CID, IDSURVEY, zHD, zHEL, MU, MUERR_RENORM, mB, x1, c, biasCor_mu, HOST_LOGMASS, HOST_LOGsSFR,
   HOST_COLOR, PROBCC_BEAMS.
2. The Dovekie Hubble diagram and STAT+SYS inverse covariance already on disk (`_external_data/cfg684_inputs/des5/`),
   DESI DR2 BAO, and AGB1's fitter (`agb1_run.py`, `agb1_template.py`), imported unchanged, for Parts S, J and E.
3. AGB2's galaxy model (`agb2_galaxy.py`) and joint arithmetic (`agb2_joint.joint`), imported unchanged; AGB2's
   committed outputs for two reported comparisons.

**Samples.** `des_only` (IDSURVEY 10): 1,623 rows, 532 low-mass (log M < 10), 1,091 high-mass. `full`: 1,820 rows
(594 / 1,226); the 197 others are the legacy low-redshift set. `pure`: `des_only` with PROBCC_BEAMS ≤ 0.1 (1,498;
472 / 1,026). `young`: log sSFR ≥ −9.5 (609: 586 DES, 23 legacy).
**Primary sample for the host fits is `des_only`**: its host photometry is homogeneous, and the legacy hosts' listed
star-formation rates behave differently (27 % of their low-mass hosts are listed as passive, against 0–3 % in DES).
`full` is a fork everywhere, and the primary where a low-redshift anchor is needed (Parts S and E).

**What was looked at before this freeze.** Every host column, redshifts, survey codes, classifier probabilities and
error columns. Two file-format checks: the table equals the distance file on disk row for row (zHD, MU; its
MUERR_RENORM is that file's MUERR), and mB + 0.169 x1 − 3.14 c − biasCor_mu − MU takes two values, 0.0334 mag apart
between the mass groups with 0.0007 scatter inside each, which is the published mass step (0.033). Power forecasts
from the design matrices. **No magnitude has been fitted against any host property or against redshift.** The author
knows the results of AGB1 and AGB2.

## Two host-age models (built before the freeze; no supernova magnitude was read)
- **Mass-only model:** the Childress et al. (2014) galaxies of AGB2, age from (log M, z).
- **Two-component model (new, `agb3_twocomp.py`): age from the host's measured specific star-formation rate s and z.**
  The host's stars are (1) a part formed at a constant rate s × M over the last T_c, and (2) an old part formed in
  one burst at formation redshift z_f = 3 (burst age T_f = t(z) − t(3); flat Ω_m 0.30, H0 70). The burst mass is
  whatever is left after the constant part, with AGB2's mass-loss law; if the constant part alone exceeds the mass
  there is no burst and T_c is shortened until it gives the mass. Progenitor ages follow SFR(t − τ) × Φ(τ) with
  AGB2's delay-time distribution; the age used is the mean. log s is clipped to [−13, −8]. Mass cancels: the age
  depends on s and z only.
  Mean age in Gyr at log s = −13, −12, −11, −10.5, −10, −9.5, −9, −8.5, −8:
  z 0.05: 10.67, 10.53, 9.34, 7.31, 4.23, 1.75, 0.76, 0.37, 0.13; z 0.5: 6.31, 6.27, 5.89, 5.14, 3.62, 1.75, 0.76,
  0.37, 0.13; z 1.0: 3.64, 3.63, 3.52, 3.30, 2.73, 1.70, 0.76, 0.37, 0.13.

**Three things the host table says before any magnitude is read.**
1. *Mass tracks star-formation age at least as strongly as AGB2's model assumed.* Age gap between the high-mass and
   low-mass hosts, two-component ages against the mass-only model, by redshift band (0.1–0.3, 0.3–0.5, 0.5–0.7,
   0.7–1.2): 3.23 / 2.22, 3.00 / 1.65, 3.04 / 1.33, 2.44 / 1.05 Gyr. Only the legacy band (z < 0.1) goes the other way,
   1.10 / 2.71. (For one and the same model galaxy the two-component age runs up to 1.2 Gyr older at high mass,
   because of the single burst; the ratios above are larger than that.)
2. *Old and young hosts are far apart.* Two-component age gap, red (colour > 1) minus blue hosts: 4.2 to 2.2 Gyr
   from z 0.1 to z 1; passive (log s < −11) minus star-forming: 5.9 to 2.3 Gyr. At 0.030 mag/Gyr that is 0.07 to
   0.18 mag.
3. *The sample's mean host age falls much less with redshift than the cosmic average.* Mean two-component age of
   the `full` sample at z = 0.03, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0: 5.77, 4.75, 3.45, 2.57, 2.88, 2.88, 2.46 Gyr. Almost all
   of the fall lies between the legacy set and DES. Inside `des_only` it is 3.4 Gyr at z 0.2 and 2.5 at z 1. The
   median age behind AGB1's template falls from 6.1 to 1.3 Gyr over z 0.05 to 1.

## Part D — the slope from the hosts (no cosmology)
**Model** (AGB2's, with its amendment 1): weighted least squares, weights 1/MUERR_RENORM²,
y_i = Σ_b o_b [z_i in bin b] + g (L_i − ½) + A × D_i (+ a x1_i + b c_i in reading R);
20 equal-count redshift bins of the sample in use; L_i = 1 for a low-mass host; μ_fid flat Ω_m = 0.330.
Readings: **R** (primary) y = mB − μ_fid, a and b free, nothing removed; **P** y = MU − μ_fid, as published;
**B** y = mB + 0.169 x1 − 3.14 c − biasCor_mu − μ_fid, the published standardisation and bias corrections with the
mass step undone.
Templates: **sfr** D_i = −0.030 × (two-component age of host i); **run** and **mass** as in AGB2 (mass-only model).
- **D2, per host, measured star formation, constant mass step free.** A = 1: the published slope acting on the
  two-component ages. Words: AGB1's W1 rules on Δχ²(A=0), Δχ²(A=1) (EXCLUDED AT 3 SIGMA / DISFAVOURED / REQUIRED AT
  3 SIGMA / FAVOURED / UNDECIDED / NEITHER, with "AGE BIAS" in front of the first four).
  Second word: ROBUST if each fork, one at a time, gives the same first word, else FRAGILE naming which: reading P;
  `full`; 40 bins; `pure`; z_f = 2; z_f = 5; **half template** (the same fit with the template halved, which stands
  for a star-formation measure that gets half of the age contrast wrong: Δχ²(A=1) becomes ((2Â − 1)/(2σ))², Δχ²(A=0)
  is unchanged).
- **U, the upper limit: the same template with no constant step (g = 0), reading R.** Whatever hosts do to
  brightness is counted as age. Words:
  SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA if Â < 1 and Δχ²(A=1) ≥ 9;
  SLOPE OVERPREDICTS THE HOSTS (2 SIGMA) if Â < 1 and 4 ≤ Δχ²(A=1) < 9;
  HOSTS AS LARGE AS THE SLOPE NEEDS if Δχ²(A=1) < 4;
  HOSTS LARGER THAN THE SLOPE NEEDS if Â > 1 and Δχ²(A=1) ≥ 4.
  Second word: the forks of D2 with reading B in the place of reading P, plus the mass-only per-host ages in the
  place of the two-component ages.
  **It is an upper limit only if nothing else makes supernovae in old hosts fainter after standardisation.** Every
  known effect goes the other way: dust (the usual reading of the mass step), core-collapse contaminants (faint, in
  star-forming hosts) and selection near the flux limit all make old hosts look brighter, as age would.
- **Power, from the design alone:** σ_A = 0.079 (D2) and 0.065 (U) on `des_only`; 0.055 and 0.050 on `full`.
- **Reported only.** D1, AGB2's step-run test on this sample (template **run**, constant step free): forecast
  σ_A 0.79 on `des_only` and 0.44 on `full`, so it cannot decide alone; its `des_only` value is combined by inverse
  variance with AGB2's Pantheon+ fit without that survey's DES supernovae. The per-host fit with mass-only ages
  (AGB2's H2 on this sample). Steps band by band (z 0–0.1, 0.1–0.3, 0.3–0.5, 0.5–0.7, 0.7–1.2) for three splits, mass
  at 10, log s at −10, colour at 1.0, readings R and P, beside what the slope predicts. The short-delay delay-time
  distribution. `full` in reading P.

## Part S — the sample's own age drift, through AGB1's cosmology fit
**Template T_H(z)** = 0.030 × [mean two-component age in the lowest redshift bin − mean age at z], from the means
of the hosts' ages in the 20 equal-count redshift bins of the sample, linear between bin mean redshifts and flat
outside them. Computed for `full` at z = 0.03, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0:
0.000, 0.005, 0.031, 0.070, 0.096, 0.094, 0.087, 0.088, 0.087, 0.090, 0.097, 0.099 mag
(AGB1's template over the same span: 0.000, 0.007, 0.024, 0.053, 0.077, 0.095, 0.111, 0.123, 0.132, 0.140, 0.147, 0.151).
For `des_only` (from its own hosts) it stays below 0.032 mag.
**Model:** AGB1's Part A exactly (BAO + supernovae, flat w0–wa, full covariance, same fitter and starts), with
μ_model + ℳ + A_H × T_H(z_HD). A_H = 1 is the published slope acting on the age drift of this sample.
Fits on `full`: A_H = 0, A_H = 1 and A_H free, each with q0 = 0 imposed and with q(z) ≥ 0 imposed.
- **S2, today, at A_H = 1** (W2 rule): ACCELERATING TODAY if q0 < 0 and Δχ²_today ≥ 4; DECELERATING TODAY if q0 > 0
  and Δχ²_today ≥ 4; else SIGN NOT SETTLED.
  Second word: ROBUST if the same word comes out for `des_only` (its own T_H); for T_H built from the mass-only ages;
  for z_f = 2; for z_f = 5; else FRAGILE naming which.
- **S3, ever, at A_H = 1** (W3 rule): NEVER-ACCELERATED EXCLUDED AT 3 SIGMA / DISFAVOURED / ALLOWED. Printed for the forks.
- Reported: A_H free with Δχ² at 0 and at 1; the correction applied host by host in the place of the smooth curve.
- **KS, harness.** A_H = 0 must return AGB1's A = 0 fork (Δχ²_today and Δχ²_never, `full` and `des_only`) to 0.01, and
  AGB1's own template at coefficient 1 must return its A = 1 fork to 0.01.

## Part J — slope from the hosts times drift from the hosts
D2's amplitude and error are used as a Gaussian prior on A_H (both are the slope in units of 0.030 mag/Gyr).
f, t, n: best χ² of the Part S model at fixed A_H when free, with q0 = 0, with q ≥ 0; grids −1.0 … 2.0 in steps of 0.1
(f, t) and 0.25 (n); AGB2's joint arithmetic. D2 uses contrasts inside redshift bins, the distances use the trend
across them, so the two are taken as independent.
- **J2, today,** and **J3, ever,** by the W2 and W3 rules, at the joint best A_H; judged on `full` with D2's primary fit.
  Second word of J2: ROBUST if the same word comes out with: `des_only` distances and T_H; D2 in reading P; the
  half-template prior (2Â ± 2σ); T_H from mass-only ages; **U's amplitude as the prior** (the case in which every host
  effect is age); else FRAGILE naming which.
- Reported: the joint amplitude and its Δχ² at 0 and 1.

## Part E — young hosts only (S25's "evolution-free" test, on this table)
Sample `young`: log s ≥ −9.5. In the two-component model such a host's progenitors average at most 1.72 Gyr at any
redshift; the subsample's mean age changes by 0.5 Gyr between z < 0.1 and z > 0.7 (2.9 Gyr for all hosts), and by
0.08 Gyr inside DES. AGB1's Part A model on these supernovae alone (sub-block of the covariance, taken as AGB1
takes it), published moduli, no age term: free, with q0 = 0, with q ≥ 0.
- **E2, today** (W2 rule) and **E3, ever** (W3 rule).
  Second word of E2: ROBUST if the same word comes out for blue hosts (colour ≤ 0.8; 733) in the place of `young`,
  and for log s ≥ −10 (1,145); else FRAGILE naming which.
- Reported: the complementary old-host subsample; the young DES supernovae alone (586, no low-redshift anchor).
- A subsample of 609 has about a third of the weight of the whole; SIGN NOT SETTLED here means "too few", not "no".

## Known-answer checks (judged before the words are read)
- **KM, the two-component model.** (i) A host with log s = −13 at z 0.05 has the burst age to 2 % (computed 10.67
  against 10.68). (ii) Constant star formation over 6 Gyr: the tabulated mean age equals direct quadrature to 0.001
  Gyr (1.9023 both). (iii) The mass-only model's own galaxies (log M 9 to 11.5, z 0.05 and 0.5), fed through the
  two-component model with their own s, come out within 1.5 Gyr of their mass-only age (largest computed 1.19).
- **K1, the table.** Equal to the distance file for all 1,820 supernovae (z to 10⁻⁵, MU and error to 10⁻⁴); the
  column identity gives a step of 0.033 ± 0.002 between the mass groups with scatter ≤ 0.002 inside each
  (computed 0.0334, 0.0007).
- **K2, the estimator on real magnitudes.** Reading B on `full`, constant step alone: g within 0.016 of the
  published γ = 0.033 ± 0.008 (two of its sigmas: their fit uses the full pipeline, this one bins and diagonal weights).
- **K3, mutation twins (exit 3 on pass, 4 on fail).** y replaced by fixed bin offsets (+ 0.05 (L − ½) where the step
  is free; − 0.15 x1 + 3.1 c in reading R) plus A_true × D, A_true = 1 and 0, for D1, D2 and U in readings R and P.
  Pass each: |Â − A_true| ≤ 10⁻⁶, χ²_min ≤ 10⁻⁸.
- **K4, the error bar** (AGB2 amendment 1's rule). `des_only`, reading R, for D1, D2 and U: hosts shuffled among
  supernovae inside each redshift bin (mass and star-formation rate moved together; seed 20261115; 400 draws):
  |mean Â| ≤ 0.2 σ_A, shuffle scatter within [0.8, 1.25] σ_A, and the sandwich error from the residuals within
  [0.8, 1.25] σ_A.
- **KS**, above.
Part D is NOT EVALUABLE if KM, K1, K2, K3 or K4 fails (K4 is judged per configuration: a failed configuration loses
its own word only). Parts S and E are NOT EVALUABLE if KM, K1 or KS fails. Part J needs D2 and Part S. Numbers are
still reported as a reading.

## What the result may and may not say
- The star-formation rates are the DES team's fits to broad-band host photometry, on a grid of templates. They are
  noisy. Noise mixes old and young hosts and makes any age signal look smaller, which pushes D2 and U towards A = 0.
  The half-template fork is there for that: a word that survives it holds even if half the contrast is noise.
- The two-component model is the simplest one that uses the measured rate: one burst plus a constant rate. The z_f
  forks move the burst. It is not a fit to each galaxy's history.
- Reading R has no bias corrections; the known selection effects push it towards A > 0. Reading P carries the
  survey's corrections and its mass step.
- Part S grants the published slope in full and changes only the age history, from the cosmic average to these
  hosts. If the host star-formation rates run too low at high redshift, the drift is understated; the mass-only
  fork does not use them. S2 is not a statement about the slope.
- Part E selects supernovae by host; the published bias corrections were made for the whole sample.
- U is an upper limit under the stated assumption, and D2 a measurement beyond a constant mass step. Neither says
  what causes a host dependence. Words are read as one degree of freedom (4 = 2σ, 9 = 3σ); cosmology words live
  inside the flat w0–wa family.
- AGB1's and AGB2's words stand as written. Nothing here grades this repository's framework; no a0 is used.

## Files and order
`agb3_twocomp.py` (the two-component model), `agb3_run.py MODE` (checks and Part D), `agb3_cosmo.py` (Parts S, J, E),
`agb3_collect.py` (checks and words; `agb3_results.json`, `agb3_collect.out`).
This file is committed alone, before any script. The scripts are committed next, before any real-data number; until
then only KM, the design-only forecast, K1 (file format) and the K3 twins are run, in a scratch copy.
Any change after this commit is a dated amendment committed alone before the re-run, and both readings are reported.

kappa = 1/2 FITTED; not theory closed.
