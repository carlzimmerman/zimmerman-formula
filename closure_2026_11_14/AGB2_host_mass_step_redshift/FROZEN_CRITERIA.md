# AGB2 — the progenitor-age slope tested on host galaxies: the host-mass step against redshift in Pantheon+ (FROZEN, before any number)

2026-11-14. Owner: "Yes, swing AGB2". A test of a published claim on public data.
It adopts nothing and edits no ledger. No script of this lane is in the repository when this file is committed.

## Why
Son et al. (arXiv:2510.13121; "S25") say a supernova's standardised brightness falls with its progenitor's age at
0.030 mag/Gyr, and that because progenitors were younger in the past the distances drift with redshift. Lane AGB1
(`closure_2026_11_13/AGB1_progenitor_age_bias/`) measured the size of that drift from distances alone, where a drift
with redshift has to be told apart from the expansion history itself.
The same slope makes a second prediction in which the expansion history cancels. **At one redshift**, supernovae in
massive hosts come from older stars than supernovae in small hosts, so they must be brighter after standardisation;
and because that age gap closes towards high redshift (every galaxy was young then), **the host-mass step must
shrink with redshift at a rate the slope fixes.** This lane measures that, and then puts the two measurements of the
slope together.

## Data
1. **Pantheon+** table and STAT+SYS covariance (`_external_data/pantheonplus_dr/PantheonPlusSH0ES.dat`, 1,701 light
   curves of 1,543 supernovae; `PantheonPlusSH0ES_STAT+SYS.cov`), public release, on disk since 2026-10-12.
   Columns used: zHD, zHEL, m_b_corr, mB, x1, c, HOST_LOGMASS, HOST_LOGMASS_ERR, CID, IDSURVEY.
   The covariance is symmetrised, (C + Cᵀ)/2 (the file is symmetric to 3 × 10⁻⁸); a sub-sample uses its sub-block.
2. **AGB1's committed outputs** (`agb1_A_full.json`, `agb1_A_des_only.json`, `agb1_results.json`) and AGB1's fitter
   (`agb1_run.py`, `agb1_template.py`), imported unchanged, for the joint part only.

**Samples.** `all` (primary): 0.01 < zHD ≤ 1.0 and HOST_LOGMASS > 5: 1,563 rows; 716 low-mass (log M < 10), 847
high-mass (log M ≥ 10, the Pantheon+ step location). `measured`: `all` with 0 < HOST_LOGMASS_ERR < 2 and the mass not
equal to the catalogue's fill values 7.000 or 11.500: 1,251 rows (542 low, 709 high). `k1`: every row with zHD > 0.01
(1,590), for check K1 only. Rows above z = 1 are left out because 14 of the 25 carry the fill value 10.000, which
sits on the step.

**What was looked at before this freeze.** Redshifts, host masses and their errors, survey codes, x1 and c (as
columns of the design matrix), and the covariance, for the counts above and the power forecast below. No fit to any
magnitude was made. One summary line (count, mean, upper quartile, maximum) of the m_b_corr column was printed while
listing the table. On record from 2026-07-20 (`real_research/snia_massstep_acceleration_test.py`): the raw host-mass
step in Pantheon+ has the textbook sign and size, and the published magnitudes have it removed on average. Nothing
on record or seen here says how either step changes with redshift. The author knows AGB1's result.

## The host-age model (built before the freeze; no supernova magnitude was read to build it)
The galaxy model of Childress, Wolf & Zahid (2014, arXiv:1409.2951; "C14"), the paper S25's own redshift correction
is built on. Recipe as read from the web (PROVISIONAL, summariser):
- star-forming main sequence Ψ(M, z) = 2.00 e^{1.33 z} (M/10¹⁰)^0.7 M⊙/yr (C14 Eq. 4), used at every redshift;
- mass quenching: the rate is multiplied by p_Q = ½[1 − erf((log M − log M_Q(z))/σ_Q)], σ_Q = 1.5,
  log M_Q = 10.43 + 0.9 log(1+z) for z ≤ 1.5 and 8.56 + 5.6 log(1+z) above (Eqs. 6, 7; base 10);
- stellar mass loss f_ml(t) = 0.046 ln(t/0.276 Myr + 1) (Eq. 5);
- a galaxy starts as a 10⁶ M⊙ seed at a formation time and is integrated forward; flat Ω_m = 0.30, H0 = 70;
- progenitor ages of its supernovae at time t are distributed as SFR(t − τ) × Φ(τ) (Eq. 2), with the delay-time
  distribution AGB1 used: Φ(t) ∝ (t/t_p)^α/((t/t_p)^{α−s} + 1), t_p = 0.3 Gyr, s = −1, α = 20 (α is my recollection;
  the page read did not print it).
Here (`agb2_galaxy.py`): 541 formation times from 13 Gyr of lookback to now, every 24 Myr; time step 4 Myr; the
growth term stepped exactly in M^0.3 and the surviving mass summed over all earlier steps. At a given redshift mass is
monotonic in formation time, so (log M, z) fixes the star-formation history and hence the age distribution.
τ̄(M, z) is its **mean** (primary: a linear law acting on each supernova gives group means that depend on the mean
age only) or its **median** (fork: the statistic of AGB1's template). Tabulated on z = 0 … 1.6 (step 0.02) and
log M = 7.5 … 12.4 (step 0.05), bilinear in between; catalogue masses are clipped to that range (the model is flat
below 8).
Values computed before the freeze, mean age in Gyr at log M = 8, 9, 10, 10.5, 11, 11.5, 12:
z = 0: 1.02, 1.65, 3.07, 4.47, 6.48, 8.71, 10.45; z = 0.5: 0.68, 1.02, 1.74, 2.42, 3.43, 4.64, 5.73;
z = 1.0: 0.48, 0.67, 1.05, 1.40, 1.93, 2.60, 3.28. Median at z = 0: 0.77, 1.14, 2.20, 3.87, 7.56, 10.53, 11.42.

**The two templates** (slope 0.030 mag/Gyr, sign as in AGB1: a younger progenitor makes the published modulus larger).
- **Step run** (primary; what the title says): D_i = 0.030 × Δτ(z_i) × (L_i − ½), with L_i = 1 for a low-mass host
  and 0 for a high-mass one, and Δτ(z) = the mean of τ̄(M_j, z) over the sample's high-mass hosts minus the mean over
  its low-mass hosts (the sample's own two groups, aged to redshift z by the model; grid of 0.01 in z).
  For `all`, mean age: Δτ = 3.45, 3.31, 3.08, 2.68, 2.33, 1.79, 1.38, 1.07 Gyr at z = 0.02, 0.05, 0.1, 0.2, 0.3, 0.5,
  0.7, 0.9, so the step the slope predicts is 0.104, 0.099, 0.092, 0.080, 0.070, 0.054, 0.041, 0.032 mag.
- **Per host** (second reading; leans on the model's age at every mass, not only on the gap between two groups):
  D_i = −0.030 × τ̄(M_i, z_i).

## Part H — the host measurement
**Model, linear, solved by generalised least squares with the full covariance:**
y_i = Σ_b o_b [z_i in bin b] + g (L_i − ½) + A × D_i (+ a x1_i + b c_i in reading R).
- o_b: one free offset per redshift bin, 20 equal-count bins of the sample in use. They absorb the expansion history,
  the absolute magnitude and any selection effect common to both host groups.
- g: a free constant step. It absorbs whatever part of the host-mass step does not change with redshift (the survey's
  own correction in reading P; dust or anything else in reading R). **So A is measured from the change of the step
  with redshift (step run), or from that plus the shape in mass that a step at 10¹⁰ cannot copy (per host). The size
  of the step itself is never counted as evidence for age.**
- **Reading R (primary): nothing removed.** y = mB − μ_fid, with a and b free (the stretch and colour coefficients);
  no bias correction and no host correction. μ_fid = 5 log₁₀[(1 + zHEL) D_M(zHD)] for flat Ω_m = 0.334 (any smooth
  error in it goes into the bin offsets).
- **Reading P: the published corrections kept.** y = m_b_corr − μ_fid.
- A = 0: no dependence on age beyond a constant step. A = 1: the S25 slope acting on the model's ages.
  Δχ²(A = a) = (Â − a)²/σ_A² (the model is linear, so the profile is exactly a parabola).

**Frozen words.**
- **H1, step run, judged on (`all`, reading R, mean age, 20 bins):**
  AGE BIAS EXCLUDED AT 3 SIGMA if Δχ²(A=1) ≥ 9 and Δχ²(A=0) < 4;
  AGE BIAS DISFAVOURED if 4 ≤ Δχ²(A=1) < 9 and Δχ²(A=0) < 4;
  AGE BIAS REQUIRED AT 3 SIGMA if Δχ²(A=0) ≥ 9 and Δχ²(A=1) < 4;
  AGE BIAS FAVOURED if 4 ≤ Δχ²(A=0) < 9 and Δχ²(A=1) < 4;
  UNDECIDED if both are < 4; NEITHER if both are ≥ 4 (AGB1's W1 rules).
  Second word: ROBUST if each of four forks, changed one at a time, gives the same first word, else FRAGILE, naming
  which: reading P; median age; 40 bins; sample `measured`.
- **H2, per host:** the same rules and the same four forks with the per-host template.
  It is reported beside H1 and does not enter the joint words.

**Power, forecast from the design and the covariance alone (no magnitude):** σ_A = 0.40 for H1 (0.32 median, 0.40
with 40 bins, 0.51 on `measured`, 0.40 in reading P) and 0.10 for H2 (0.07, 0.10, 0.15, 0.10). So H1 by itself can
exclude one of A = 0, A = 1 at 3σ only if the best fit lies well outside [0, 1]; its use is in the joint. H2 has four
times the grip and four times the reliance on the model.

**Known-answer checks (judged before the words are read).**
- **KG, the galaxy model.** (i) log M_Q(0.35) within 0.01 of C14's anchor 10.55 and the two branches equal at z = 1.5
  to 0.005 (computed: 10.547; 10.788 both). (ii) C14: "a rapid transition between 10.0 ≤ log M ≤ 11.5": at z = 0 at
  least half of the rise of the mean age between log M 8 and 12 falls inside 10.0–11.5 (an even rise would put
  0.375 there; computed 0.598). (iii) C14: massive galaxies today formed their stars in about 1 Gyr, 8–10 Gyr ago
  (approximate words): for the track ending at log M = 11.5, half of the stars formed by a lookback in [8, 11.5] Gyr
  and the middle half within 2 Gyr (computed 10.92; 1.28). (iv) halving the time step moves no tabulated age by more
  than 0.05 Gyr (computed 0.004).
- **K1, loader and covariance.** Supernovae alone, flat ΛCDM, m_b_corr with the full covariance on `k1`, offset
  profiled: target Ω_m = 0.334 ± 0.018 (Brout et al. 2022, from memory, PROVISIONAL). Pass: |ΔΩ_m| ≤ 0.009 (half a
  sigma: best fit against posterior mean).
- **K2, the raw step.** Reading R on `all`, the constant step alone (no template): g in [0.02, 0.09] mag, low-mass
  hosts fainter (published values without a dust-based bias model run 0.04–0.07; the 2026-07-20 script found the
  textbook value).
- **K3, mutation twins (exit 3 on pass, 4 on fail).** y replaced by the model's own prediction (fixed bin offsets,
  g = 0.05, a = −0.15, b = 3.1 in reading R) plus A_true × D, no noise, A_true = 1 and 0, both templates, both
  readings. Pass each: |Â − A_true| ≤ 10⁻⁶ and χ²_min ≤ 10⁻⁸.
- **K4, the error bar.** Host masses shuffled among supernovae inside each redshift bin (by CID, so duplicate light
  curves stay together; numpy default_rng seed 20261114; 400 draws), primary configuration, both templates. A
  shuffle removes any real link between host and brightness. Pass each: |mean Â| ≤ 0.2 σ_A and the scatter of Â
  within [0.8, 1.25] σ_A (400 draws fix the mean to 0.05 σ and the scatter to 4 %; the rest of the allowance is for
  the correlated part of the covariance, which a shuffle does not reproduce).
If KG, K1, K3 or K4 fails, H1 and H2 are **NOT EVALUABLE** (numbers still reported as a reading). If K2 fails,
reading R is NOT EVALUABLE; H1 and H2 are then judged on reading P and their second word is FRAGILE (no R).

## Part J — the two measurements of the slope together
**Assumption, stated once:** one slope acts in both places, and each template is taken as built (AGB1's redshift
template from the cosmic star-formation history; this lane's from the C14 galaxies). The two age models are not the
same model: the C14 galaxies, weighted by C14's z = 0 mass function, give a median progenitor age of 3.2 Gyr today
against 6.7 Gyr for AGB1's template (computed before the freeze; reported, not a check).
- χ²_J(A) = [AGB1 Part A profile on `full`, the committed grid −1.0 … 2.0 in steps of 0.1, cubic spline]
  + (A − Â_H1)²/σ_H1², with Â_H1, σ_H1 from H1's primary configuration. The two terms are independent: different
  supernova compilations, and the host term uses only differences inside redshift bins.
- **J1, joint amplitude:** W1's six words on Δχ²_J(A=0) and Δχ²_J(A=1), measured from the joint minimum.
  Second word: ROBUST if the same first word comes out with AGB1's `des_only` profile, with H1's reading-P amplitude,
  and with both; else FRAGILE, naming which.
- **J2, today, and J3, ever, with the host measurement as a prior on A.** With f(A), t(A), n(A) the best χ² of AGB1's
  Part A model at fixed A when free, with q0 = 0 imposed, and with q(z) ≥ 0 imposed on 0 ≤ z ≤ 2.33:
  Δχ²_today = min_A[t + prior] − min_A[f + prior], Δχ²_never = min_A[n + prior] − min_A[f + prior], prior = (A − Â_H1)²/σ_H1².
  t on the grid −1.0 … 2.0 in steps of 0.1 and n in steps of 0.25, AGB1's fitter and starts, cubic splines, minima on a
  grid of 0.001. q0_J = the q0 of AGB1's free fit at the joint best A (linear between grid points).
  J2: ACCELERATING TODAY if q0_J < 0 and Δχ²_today ≥ 4; DECELERATING TODAY if q0_J > 0 and Δχ²_today ≥ 4; else SIGN
  NOT SETTLED. J3: NEVER-ACCELERATED EXCLUDED AT 3 SIGMA if Δχ²_never ≥ 9; DISFAVOURED if 4 ≤ … < 9; ALLOWED if < 4.
  Judged on AGB1 `full` with H1's primary amplitude; printed for the other three combinations, no second word.
- **KJ, harness.** With no prior the machinery must return AGB1's own numbers: Δχ²(A=0) and Δχ²(A=1) of
  `agb1_results.json` to 0.02; re-fitted f at A = 0 and 1 equal to the committed profile to 10⁻³; Δχ²_today and
  Δχ²_never at A = 0 and A = 1 equal to AGB1's fork values to 0.01. A joint minimum on the edge of the A grid is
  flagged. If KJ fails, J1–J3 are NOT EVALUABLE. If H1 is NOT EVALUABLE, so are J1–J3.

## Reported only (no frozen word)
- The constant step measured band by band (z 0.01–0.05, 0.05–0.15, 0.15–0.30, 0.30–0.50, 0.50–1.00), both readings,
  beside the step the slope predicts at A = 1, and a straight line through the five (mag per unit z). Model-free.
- Reading R with g fixed at 0 ("every bit of the host-mass step is age"): the amplitude that reading would need.
- Model forks of H1 and H2: C14's alternate quenching mass (Eq. 11, log M_Q = 10.077 + 0.636 z); the short-delay
  delay-time distribution of AGB1's T_W (slope −1.13 from 40 Myr); the model evaluated at masses ± 0.2 dex.
- Sample forks of H1 and H2: z ≤ 0.7; one survey group dropped at a time (SDSS = IDSURVEY 1, SNLS = 4, PS1 = 15,
  DES = 10, Foundation = 150, the other low-z sets together).
- The joint amplitude with H2 in the place of H1; the difference between Â_H1 and AGB1's best A in units of their
  combined error.

## What the result may and may not say
- A here is slope × (the model's age gap between hosts). **If real hosts differ less in progenitor age than C14's
  galaxies do, the true slope is larger than the fitted A by that factor**, and this lane cannot tell the two apart.
  S25 themselves argue that host mass tracks age poorly. The band-by-band steps are given so that any other age model
  can be laid over them.
- The C14 recipe is a web reading and one deterministic galaxy per mass; real galaxies of one mass differ. For a
  linear law only the mean age at each mass matters, and the model's mean is what is used.
- Reading R has no bias corrections: a selection effect that differs between host groups and grows with redshift
  would look like a run. Host masses are noisier at high redshift, which moves hosts across 10¹⁰, waters the step
  down there and so **pushes reading R towards A > 0**. Reading P keeps the survey's corrections, which were fitted
  to these same supernovae with separate low- and high-redshift dust parameters and may already have absorbed part
  of a run, which **pushes reading P towards A = 0**. That is why the second word needs both.
- A step that changes with redshift is not proof of age (dust can change too), and a step that does not change
  rules out only this slope with this model. Words are read as one degree of freedom (4 = 2σ, 9 = 3σ).
- The joint words hold only under the stated assumption. They do not replace AGB1's words, which stand as written.
- Nothing here grades this repository's framework; no a0 is used.

## Files and order
`agb2_galaxy.py` (the model; prints the table above), `agb2_run.py MODE` (checks and Part H; `agb2_<MODE>.json`,
`.out`), `agb2_joint.py` (Part J), `agb2_collect.py` (applies checks and words; `agb2_results.json`, `agb2_collect.out`).
This file is committed alone, before any script. The scripts are committed next, before any real-data number; until
then only KG and the K3 twins (neither reads a measured magnitude) are run, in a scratch copy, to debug plumbing.
Any change after this commit is a dated amendment committed alone before the re-run, and both readings are reported.

kappa = 1/2 FITTED; not theory closed.
