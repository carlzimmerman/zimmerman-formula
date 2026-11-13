# MWT1 FROZEN CRITERIA: which data-side assumptions does RAW1's hot 30-40 kpc bin rest on?

Written 2026-11-13, before any script of this lane and before any number of this lane. TEST lane. Adopts nothing,
relabels nothing (RAW1, HOT1 and LMC1 keep their labels), registers nothing.

## 0. What is known beforehand (disclosed)

Read in full before writing: RAW1 (`closure_2026_11_12/RAW1_halo_stars_direct/`: RESULT, FROZEN_CRITERIA, A1, A2,
raw1.py, raw1_model.py, raw1_results.json), HOT1 RESULT (with the lead's post hoc), LMC1 RESULT. So these numbers
are known: per-bin counts 865 / 264 / 241 / 125; sigma_los 97.24, 106.74, 92.62, 95.30 km/s; alpha 5.289 +/- 0.169;
beta 0.659 +/- 0.018 (per bin 0.671, 0.685, 0.441); RAW1's f table (30-40 bin: census 1.205 / 1.155, rc 1.135 /
1.114, sigma_f 0.054 to 0.058); HOT1: the 30-40 bin's dipole 43 km/s toward (l 56, b +39), permutation p 0.048;
dispersion with that dipole removed 104.6 (neighbours 96.9, 92.2); Sgr 15-30 deg stars colder (103.4) than
>= 30 deg (108.4); close pairs are the cold part of the bin; north 107.3 / south 103.4; LMC1: the framework's LMC
moves each bin's dispersion by under 2 per cent. Also seen before freezing: the catalogue's column names and
that 6,327 rows hold 5,461 distinct TARGETIDs (repeat observations exist). No velocity, distance, logg or
parallax value was read in this lane before this file.

Data: the file RAW1 used (`MWS_BHB.fits`, DESI DR1 MWS BHB VAC v1.0, sha256 5669c821...5246, held outside the
repository; the script checks the hash and takes the path as its argument). Nothing is downloaded.

## 1. Statistic, line, footings (all RAW1's, unchanged)

RAW1's sample (S1-S6, Sgr band 15 deg, |v_gsr| <= 400, R0 8.122, solar velocity (12.9, 245.6, 7.78)), bins
20-30, 30-40, 40-55, 55-80 kpc, and RAW1's statistic: per bin f = observed / predicted dispersion from
v_i ~ N(mu, f^2 P_i + e_i^2), P_i the spherical Jeans prediction sigma_r^2(r_i)(1 - beta sin^2 eta_i);
sigma_f = stat (profile) + alpha + beta in quadrature, as RAW1's `f_full`. RAW1's machinery is copied, not
edited; RAW1's model module is imported read-only and its sha256 recorded.
Line: the framework's no-field line g = nu(g_b/a0) g_b, nu(y) = 1/(1 - exp(-sqrt y)); external field DROPPED as in
RAW1 (owner note 2026-11-12: unchanged inside 300 kpc). Cases graded: FW census (McMillan 2017 baryons) and FW rc
(stars at the rotation-curve mass), each on canonical and alt. Headline label = FW census, per footing; FW rc is
labelled by the same rule and reported. RAW1's module uses a0 = 9.36e-11 / 1.13e-10; the known answer needs that
exactly. One reported row repeats the nominal with a0 = 9.3603e-11 / 1.1312e-10 (the standing values) to show
the difference. Comparators H (DESI NFW) and N are reported under every check, not graded.
Word per bin: PASS if |f - 1| <= 2 sigma_f, HOT if f > 1 + 2 sigma_f, COLD if f < 1 - 2 sigma_f. Row label as
RAW1 (PASSES / FAILS HOT / FAILS COLD / FAILS COLD AND HOT).
Under masks alpha and beta stay at RAW1's nominal values (masks act on the velocity sample only; disclosed
simplification); under distance shifts the whole measurement (alpha, beta) is redone as RAW1 did.

## 2. Checks (every check applied to EVERY bin; the word of every bin reported)

(E) Equilibrium. Per bin: mean v_gsr and its error; a dipole fit v_i ~ N(mu + D . n_i, f^2 P_i + e_i^2), n_i the
line-of-sight unit vector in Galactocentric axes, (mu, D) exact weighted least squares for each f, f profiled;
D's amplitude, direction (l, b) and errors; LR = 2 Delta lnL against no dipole, p from chi2 with 3 dof. f and the
dispersion with the fitted dipole removed. Excess kurtosis and Sarle's bimodality coefficient of the standardised
residuals z_i = (v_i - mu)/sqrt(s^2 + e_i^2), p from 2,000 Gaussian Monte Carlo samples with the bin's own errors
(two-sided for kurtosis, one-sided high for bimodality). Kurtosis and bimodality are diagnostics only; no
correction is derived from them.
DETECTED (enters the combination): dipole LR p < 0.01 in any bin; then a dipole is fitted in every bin.

(S) Substructure. S1: Sgr band widened to |B_Sgr| < 25 deg (Majewski frame, RAW1's code). DETECTED if, in any bin,
the stars at 15 <= |B| < 25 differ from those at |B| >= 25 in (mean, dispersion), LR p < 0.01 with 2 dof.
S2: position-velocity overdensity mask. Neighbours of a star: heliocentric angle < 10 deg, |Delta r_gc| < 5 kpc,
|Delta v_gsr| < 25 km/s, searched over the whole 20-80 sample. Null: 200 seeded shuffles of v_gsr among the stars of
each radial bin. A star is flagged if it has k >= 2 neighbours and fewer than 2 of its 200 null counts reach k
(per-star p < 0.01). Mask = flagged stars. DETECTED if, in any bin, the flagged count exceeds the 99th percentile
of the null flagged count (each null shuffle graded by the same rule against the other 199, leave-one-out).
Disclosed: a shuffle null also responds to sky-scale mean offsets (HOT1's lesson).

(L) Clean sample (contamination, logg). Stars the catalogue's own spectroscopic gravity marks as high gravity (blue
straggler-like): LOGG > 3.75 and LOGG_ERR < 0.25. Removed in every bin. DETECTED if the cut removes at least one
star in 20-80 kpc. Velocity dispersion of the removed stars reported. Bracket thresholds 3.5 and 4.0.

(D) Tracer density. D-data: the sample's own broken power law (RAW1's likelihood and windows), break fixed at 25
and at 30 kpc, inner and outer slopes free; the outer slope continues beyond 80 kpc. DETECTED if, at either break,
2 Delta lnL against the single slope > 6.63 (p < 0.01, 1 dof); the better break (higher lnL) is used, the other
is a bracket. If the fitted outer slope is <= 2 beta + 0.5 (Jeans integral not convergent), D-data is NOT
EVALUABLE at that break. Plainly: the sample's window reaches about 45 kpc, so it cannot measure the slope
beyond that, and it cannot test its own completeness model (flat in magnitude), which sets alpha.
D-lit (untestable alternative, from RAW1's own disclosed reference values, section 1 of its criteria): inner
slope 2.5, outer slope 4.0 or 4.5, break 25 or 30 kpc (four forms); sigma_f's alpha part as nominal.

(B) Anisotropy. B-data: a beta profile, piecewise constant on RAW1's bins, at the per-bin values the stars' own
proper motions give (RAW1's fit re-run, usable-bin rule as RAW1); a bin that is not usable (55-80) and beyond 80
take the last measured value; the Jeans integral solved for a variable beta exactly (integrating factor
exp(int 2 beta / s ds)); beta's sigma_f part from shifting all measured betas by +/- their own sigma together, and
for 55-80 from beta(>= 55) at 0.2 / 0.8. DETECTED if per-bin betas differ from one constant, LR p < 0.01 with
(k - 1) dof over the usable bins. B-bracket (untestable alternative): constant beta 0.2 and 0.8 in every bin;
it counts for DEPENDS only if the 30-40 bin's own beta does not exclude it at more than 3 sigma. What the proper
motions can say at 30-40 kpc: median tangential error vs dispersion, reported.

(X) Distances and errors. X-err: velocity-error scale from repeat observations (rows sharing a TARGETID, both
finite with VRAD_ERR > 0): z = (v1 - v2)/sqrt(e1^2 + e2^2), scale s = 1.4826 MAD(z), 1,000-bootstrap error;
DETECTED if |s - 1| > 2.576 x its error; then e_i -> s e_i for every star. (RAW1 already deconvolves the quoted
errors; the X-err row is RAW1's deconvolution with the data's own error scale.) X-dist (untestable alternative):
catalogue distances x0.9 and x1.1, whole measurement redone. Diagnostic: per bin, Gaia parallaxes (zero point
-0.017 mas, PROVISIONAL from memory) against 1/d, inverse-variance mean ratio and error: says how well the
data themselves fix the distance scale.

(F) Footprint and symmetry. Per bin: sky coverage (fraction of the sphere within 5 deg of a bin star, 20,000
seeded random points); f in Galactic north / south (LR p, 1 dof) and in the four quadrants (b sign x l < / >= 180,
groups with >= 15 stars, LR p with k - 1 dof). F-corr: f = equal-weight mean of north and south f (stat error
half the quadrature sum; alpha and beta parts propagated the same way); not evaluable in a bin with < 15 stars in
a hemisphere (plain f used there). DETECTED if the hemisphere LR p < 0.01 in any bin. Spherical symmetry
diagnostic: f in Galactocentric polar cones (|z_gc|/r > 0.5) vs the rest, LR p; diagnostic only (no flattened
Jeans model is computed: the data cannot be turned into a correction here).

## 3. The combination and the label

Combination C = every DETECTED correction together, applied to every bin, in this order: L (logg), S1, S2 masks;
X-err scale; D-data density; B-data profile; E dipole (fitted per bin); F-corr (with the dipole fitted on the whole
bin and subtracted first).
Each check is also reported alone, applied whether DETECTED or not (marked "forced" when not detected).

Per case (FW model x footing), on the 30-40 bin:
1. NO POWER if under C the 30-40 bin has fewer than 100 stars or sigma_f > 0.10.
2. FAIL REMOVED BY <named> if the bin's word under C, or under a single DETECTED check, is PASS (named: the single
   detected checks that pass it alone; else "the combination"). Report whether any bin that passes in RAW1 then
   fails, and the row label. A HIT, not a pass of the theory: it awaits an independent re-grade.
3. FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST <named> if the bin stays HOT under C but turns PASS under an
   untestable alternative applied on top of C (X-dist x0.9 / x1.1; D-lit four forms; B-bracket where it counts).
4. FAIL SURVIVES EVERY CHECK otherwise.
FRAGILE (appended) if the word changes under a bracket applied to C: S1 width 20 / 30 (if S1 in C), S2 per-star
p < 0.001 / < 0.05 (if S2 in C), logg 3.5 / 4.0 (if L in C), the other break (if D-data in C), beta(>= 55) 0.2 / 0.8
(if B-data in C).
A forced (not detected) check that passes the bin is reported, but does not by itself give REMOVED.

## 4. Twins, known answers, mutations

Known answers (the script stops before any label if one fails):
K0 RAW1 reproduced with no check: counts 865 / 264 / 241 / 125; per-bin sigma_los, alpha, beta, and every FW f and
   sigma_f within 5e-4 of `raw1_results.json`.
K1 the variable-beta Jeans solver with a constant beta equals RAW1's sr2_profile to 1e-6 (relative) on 20-80 kpc.
K2 the dipole fit with D fixed at zero equals RAW1's fit_f to 1e-6.
K3 SI: g of FW census canonical at 30 kpc gives M = g r^2/G equal to raw1_model.M_of_g to 1e-9, and V = sqrt(g r)
   in km/s printed.
Twins (null effect must leave the word unchanged):
T1 random masks: for every mask check (L, S1, S2, and the masks of C together), 100 seeded masks removing the same number of stars from
   each bin; the first is the twin (its 30-40 word must equal RAW1's for every case); the 2.5-97.5 per cent range
   of the f shifts is reported, and a mask check "moves" a bin only if its shift lies outside that range.
T2 dipole twin: the dipole fit on v_gsr shuffled within each bin (seeded); it must not be DETECTED in the 30-40 bin.
Mutations (separate `*_MUTATE*` output): M1 inject a 40 km/s dipole toward (l, b) = (300, +20) into the 40-55 kpc
bin; check E must DETECT it (p < 0.01), recover the amplitude within 2 sigma and the direction within 30 deg, and
the f after dipole removal must lie within 0.02 of that bin's un-mutated dipole-removed f. M2 plant a 25-star cold
group (velocities mean + N(0, 10 km/s)) on the 25 bin stars nearest a seeded 40-55 kpc star in angle with
|Delta r| < 5 kpc; S2 must flag at least 15 of them.

## 5. Expectation and hand estimate (written before any number)

- E: by HOT1 the 30-40 dipole is near p 0.05, so likely NOT DETECTED at 0.01; forced, it lowers sigma by about 2
  per cent (f 1.205 -> about 1.18 census canonical, still HOT; rc alt 1.114 -> about 1.09, PASS).
- S1, S2: likely make the bin hotter (HOT1: the Sgr-near and the clumped stars are the cold part).
- L: unknown; probably few stars, small effect.
- D-data: the sample's own slope is about 5.3 to 5.4 everywhere it sees, so a break is likely not detected.
  D-lit: shallower slopes raise the prediction; for a flat curve sr^2 = V^2/(alpha - 2 beta), alpha 4.25 instead of
  5.29 raises the predicted dispersion by about 16 per cent, so the 30-40 bin passes, but with inner slope 2.5
  the 20-30 bin goes strongly COLD (as RAW1's two-slope did).
- B-data: beta 0.44 outside 40 kpc lowers the predicted sigma at 30-40 by up to about 3 per cent: slightly hotter.
- X-err: under 1 per cent. X-dist x1.1: f down by about 0.04 to 0.08: census alt and the rc lines may pass,
  census canonical marginal.
- F: north and south agree within errors (HOT1): not detected.
Expected labels: census canonical FAIL SURVIVES EVERY CHECK or FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST
(distance scale / tracer density beyond the window); census alt FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST
(distance scale). Not expected: FAIL REMOVED by a detected check.

## 6. Changes

Never edited after this commit. Departures only as dated AMENDMENT files committed alone, as-frozen reading first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
