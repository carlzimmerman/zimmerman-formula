# HOT1 FROZEN CRITERIA: where are the hot 30 to 40 kpc BHB stars?

Written 2026-11-12, before any position, velocity or proper motion of the 30 to 40 kpc stars (or of any
star) was looked at in this lane. Only RAW1's committed files (RESULT.md, FROZEN_CRITERIA.md, AMENDMENT_A1.md,
AMENDMENT_A2.md, raw1.py) were read. TEST lane. Adopts nothing.

## 0. Question

RAW1 found the 30 to 40 kpc bin of DESI DR1 BHB halo stars hotter than its neighbours. Are the hot stars a
localised stream or substructure, residue of the Sagittarius stream just outside RAW1's cut, or spread over
the whole sky?

## 1. What is known beforehand (disclosed)

- RAW1 graded sample (Sgr band 15 deg, |v_gsr| <= 400 km/s, 20 <= r < 80 kpc): 865 / 264 / 241 / 125 stars
  per bin; line-of-sight dispersions (ML, 68 per cent profile intervals): 20-30 97.24 [94.95, 99.63],
  30-40 106.74 [102.25, 111.57], 40-55 92.62 [88.51, 97.04], 55-80 95.30 km/s. Mean of the two neighbours
  of 30-40: 94.93 km/s.
- The excess of 30-40 over that mean is about 2.2 to 2.3 sigma (half-widths 4.66, 2.34, 4.27 combined:
  11.81 / 5.26 = 2.25). It may be a fluctuation. This lane says so in its result whatever the label.
- RAW1's Sgr band variants: 10 deg lowers f by 0.01 to 0.05; 20 deg raises f by 0.00 to 0.03; no cut lowers
  f by 0.06 to 0.30 (all bins together, not the 30-40 bin alone). The cut is RAW1's largest lever.
- RAW1's ratios f in 30-40 for the four framework cases: 1.205, 1.155, 1.135, 1.114 (errors near 0.055).
- RAW1 noted the 55-80 bin mean is -21.6 km/s, a hint of LMC-induced motion; not corrected.
- Known halo structure near 30 to 40 kpc, from memory (PROVISIONAL, not re-read): Sgr leading and trailing
  arms (mostly inside the cut, but the stream's latitude spread and its bifurcation reach beyond 15 deg);
  the Orphan-Chenab stream; the Hercules-Aquila and Virgo clouds (mostly nearer than 30 kpc); the LMC's
  reflex motion, a sky-wide dipole in v_gsr of order tens of km/s at these distances. A dipole is not a
  localised structure, but it inflates a bin's dispersion and could make L1 (below) fire on the cell with the
  largest offset; the per-cell means are reported so a reader can see this.
- Hand expectation (disclosed): most likely no single statistic fires at p < 0.01 (label DIFFUSE or
  UNDECIDED), because the excess is only about 2.3 sigma and a 264-star bin has little power; SAGITTARIUS
  RESIDUE is judged unlikely because Sgr debris is kinematically cold along a line of sight.
- DESIGN STUDY (disclosed): before freezing, the power of candidate L1 statistics was checked on fully
  synthetic positions (a 60 per cent sky cap, random, no catalogue data read; scratch script, not part of the
  lane) against the planted stream of section 5. A plain dispersion difference (cell vs rest, Welch-type
  standardisation of the mean squared deviation) reached p < 0.01 in only 25 per cent of 40 trials; a
  pooled-error dispersion z in 5 per cent; a signed two-group Gaussian likelihood ratio (cell's own mean and
  dispersion vs the bin's) in 88 per cent. Reason: a cold stream at +150 km/s in a 107 km/s halo adds little
  variance to a 30 to 60 star cell; it shows mainly as a shift of the cell's mean. L1 is therefore the signed
  likelihood ratio below; the plain dispersion difference is reported as L1b without a label.

## 2. Data

DESI DR1 MWS BHB VAC v1.0, https://data.desi.lbl.gov/public/dr1/vac/dr1/mws-bhb/v1.0/MWS_BHB.fits,
8,591,040 bytes, sha256 5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246. Held outside the
repository; path given on the command line; read with astropy under `python3 -I`.

## 3. Sample

Exactly RAW1's graded sample: RAW1's `load` and `build` functions (S1 PRIMARY; S2 finite VRAD, VRAD_ERR > 0,
DIST > 0, finite MAG_DERED_G and ABS_MAG_G; S3 astropy Galactocentric, R0 8.122 kpc, z_sun 20.8 pc, solar
velocity (12.9, 245.6, 7.78) km/s, v_gsr = VRAD + v_sun . n_hat; S4 |B_Sgr| >= 15 deg with RAW1's
Majewski 2003 matrix; S5 20 <= r < 80 kpc; S6 |v_gsr| <= 400 km/s), copied into this lane's script, not
imported. Amendment A1 changed only the alpha-fit window and A2 only the nuisance-mean maximisation; neither
changes which stars enter the dispersion. Velocity used: v_gsr. Dispersion estimator for every reported
dispersion: RAW1's `fit_disp` (ML, v ~ N(mu, sigma^2 + e^2), 68 per cent profile interval); half-width
h = (hi - lo) / 2.

Sample check (K-S): bin counts must equal 865 / 264 / 241 / 125, and fit_disp on 30-40 must give
106.74 +/- 0.05 km/s. Otherwise stop.

The test bin: 30 <= r < 40 kpc (264 stars). Control bins: 20-30 and 40-55.

## 4. Statistics (each on the stars of one bin; permutation nulls shuffle v_gsr among that bin's stars)

Notation: N stars, v_i = v_gsr, mu = unweighted mean of the bin, d_i = (v_i - mu)^2, MS(group) = mean of d_i
over the group. Measurement errors are ignored in L1 to L3 (the permutation null calibrates them; median
VRAD_ERR is small against 100 km/s, checked and reported).

HEALPix cells: the twelve base pixels of nside = 1, RING numbering, in Galactic coordinates
(theta = 90 deg - b, phi = l), implemented in the script from the Gorski et al. (2005) ang2pix_ring
formulae. Tests (K-H, before any data): (a) 10^6 isotropic random points (seed 101) put a fraction within
3 per cent (relative) of 1/12 into every cell; (b) the published nside = 1 pixel centres land in their own
pixel: pixel 0 at (theta, phi) = (acos(2/3), 45 deg), pixel 4 at (90 deg, 0), pixel 8 at (acos(-2/3),
45 deg), and pixel p at phi + 90 deg x k for k = 1, 2, 3 in the same ring gives p + k.

L1, sky localisation (labelled). For each cell c with n_c >= 15 stars:
  Lambda_c = N ln(MS(bin)) - n_c ln(var_c) - (N - n_c) ln(var_rest), var = variance about the group's own
  mean (ddof 0). T_c = Lambda_c if MS(c) > MS(rest), else 0 (only cells that add to the bin's dispersion
  about its mean count). L1 = max_c T_c; the top cell is the argmax (none if L1 = 0).
  p = (1 + #{null >= observed}) / (1 + Nperm).
L1b, reported, no label: max over the same cells of z_c = (MS(c) - MS(rest)) / sqrt(s_c^2/n_c + s_r^2/n_r),
  s = sample standard deviation of d_i in each group; same permutation null.
L2, Sagittarius proximity (labelled). Group A: 15 <= |B_Sgr| < 30 deg; group B: |B_Sgr| >= 30 deg.
  z = (MS(A) - MS(B)) / sqrt(s_A^2/n_A + s_B^2/n_B) as in L1b. One-sided p (A hotter): fraction of
  permutations with z >= observed (with the +1 rule). The two-sided p and the two groups' ML dispersions are
  reported.
L3, phase-space clumping (labelled). Pairs (i < j) with angular separation < 10 deg AND |v_i - v_j| < 30 km/s.
  Statistic: the count. One-sided p (more pairs than the null).
  Variant, reported: 5 deg and 20 km/s. Variant, reported: 3-D, stars with RAW1's usable proper motions
  (pmok); the Galactocentric velocity vector from v_gsr and the proper motions (RAW1's pm_arrays
  convention), pairs < 10 deg and |Delta V| < 50 km/s; null: shuffle the (v_r, v_theta, v_phi) triples among
  those stars and recompose each at its own position (keeps radial anisotropy exchangeable).
Nperm = 5000 for every observed statistic. Seeds: real bin 20261112 (L1, L1b and L2 share one permutation
set; L3 its own, seed 20261113; 3-D seed 20261114); control bins seeds 20261120 + bin index.

Reported without a label: ML dispersion in Galactic north (b > 0) and south (b < 0) separately and in the
sub-bins 30-35 and 35-40 kpc; the bin's mean v_gsr, excess kurtosis (scipy.stats.kurtosis, Fisher, bias
True) and a Shapiro-Wilk normality test of v_gsr; per-cell n, mean and ML dispersion; L1, L1b, L2, L3 on the
20-30 and 40-55 bins as a control on how often they fire.

Significance of the excess (always appended): z_ex = (s30 - (s20 + s40)/2) / sqrt(h30^2 + (h20^2 + h40^2)/4).

## 5. Known-answer checks (before any label; the script stops if one fails)

K-H  the HEALPix tests above.
K-S  the sample check above.
K-N  null calibration: 200 synthetic smooth bins (the real 30-40 positions and B_Sgr; v_i = mu_bin +
     N(0, s30_ML) + N(0, e_i), seed 31 + trial), each with 5000 permutations (seed 5000 + trial): each of L1,
     L2, L3 must fire at p < 0.05 in between 2 and 20 of the 200 (1 to 10 per cent).
K-P  planted stream (seed 4242): smooth synthetic bin as in K-N; choose one star of the bin at random; the 30
     stars nearest it on the sky are moved to uniform random positions inside a 10-deg-radius cap around it
     (their cells recomputed; their B_Sgr recomputed) and given v_gsr ~ N(+150, 15) km/s. L1 and L3 must
     both reach p < 0.01 (5000 permutations). L2 reported.

## 6. Labels (test bin)

- LOCALISED: L1 p < 0.01 AND fit_disp of the bin without the top cell's stars gives s_new <= 94.93 + h_new
  (no longer more than one of its own sigmas above the neighbours' mean).
- SAGITTARIUS RESIDUE: L2 one-sided p < 0.01 (stars nearer the plane hotter).
- CLUMPED: L3 p < 0.01.
- DIFFUSE: none of L1, L2, L3 has p < 0.05 AND the ML dispersions of the north and south halves are each
  above 94.93 km/s (point estimates).
- UNDECIDED otherwise.
More than one of the first three may apply. z_ex is always appended.

Post hoc (clearly marked, only if LOCALISED, SAGITTARIUS RESIDUE or CLUMPED): fit_disp with the identified
stars removed (top cell; group A; stars in at least one counted L3 pair, respectively) and RAW1's four f
values rescaled f_new = f_old x s_new / 106.74 (f_old 1.205, 1.155, 1.135, 1.114).

## 7. Mutation (separate output file)

M1: the bin's real v_gsr shuffled once (seed 777) and the whole labelled analysis re-run (5000
permutations, seeds as for the real bin). The label must not be LOCALISED, SAGITTARIUS RESIDUE or CLUMPED.
If it is, this is reported as a failed mutation.

## 8. Limits (to be stated)

264 stars; the DESI footprint covers part of the sky, so cells are unevenly filled and some have fewer than
15 stars; a diffuse result does not rule out a wide structure such as a shell or a sky-wide dipole; a
localised result does not identify the structure; L1 responds to mean offsets as well as to extra spread.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
