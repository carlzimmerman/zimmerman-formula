# RAW1 FROZEN CRITERIA: the halo stars direct (DESI DR1 BHB, velocity-space test, no calibration)

Written 2026-11-12, before any velocity, distance, magnitude or proper-motion value of the catalogue was
read. Only the column names, formats, units and the row count (6,327 rows in RVTAB, FIBERMAP, GAIA) were
read. The theory-side numbers below (model masses) were computed from the model module `raw1_model.py`
before this file was written; they use no data. TEST lane. Adopts nothing.

## 0. Question

Using only the DESI DR1 blue horizontal branch stars themselves (their line-of-sight velocities, the
catalogue's distances, their Gaia proper motions, their magnitudes), with no simulation calibration, no
dark-halo functional form in the measurement and no prior from another paper's fit: are the stars at
20 to 80 kpc as hot as the framework's no-field line says they must be, through the spherical Jeans
equation? Footings: canonical a0 = 9.36e-11, alt a0 = 1.13e-10 m/s^2. Both reported, never pooled,
never chosen by outcome.

## 1. What is known beforehand (disclosed)

- Framework line, census baryons, no field, enclosed dynamical mass M = g r^2 / G [1e11 Msun]
  (canonical / alt): 20 kpc 1.639 / 1.765; 30 kpc 2.331 / 2.526; 40 kpc 3.010 / 3.273;
  50 kpc 3.683 / 4.012; 80 kpc 5.691 / 6.218. With the stars scaled to the rotation curve's need
  (7.08 / 6.42e10): 30 kpc 2.644 / 2.725; 50 kpc 4.143 / 4.308; 80 kpc 6.375 / 6.662.
  Newtonian census baryons: 0.65 to 0.67 at 30 to 80 kpc. DESI NFW (comparator H): 2.485 at 30,
  4.174 at 50, 6.204 at 80.
- The brief's check value at 80 kpc on alt is 6.219; this module gives 6.2183 (difference 0.01 per cent,
  rounding). Check K4 uses a 0.1 per cent tolerance, stated here before any run.
- DESI's published joint masses (calibrated on Auriga mocks): 2.65 (+0.14 -0.13) at 30 kpc and
  4.51 (+0.27 -0.26) at 50 kpc. The census line sits 12 / 5 per cent below at 30 kpc and 18 / 11 per cent
  below at 50 kpc (canonical / alt). In velocity terms the line predicts dispersions about 3 to 9 per cent
  below what DESI's masses imply.
- Literature, from memory, not checked here: halo BHB line-of-sight dispersions fall from about 110 km/s
  near 20 kpc to about 80 to 90 km/s near 50 to 80 kpc; BHB density slopes of about 2.5 inside and 4 to 4.5
  outside a break near 25 to 30 kpc (the break may sit inside our range); beta about 0.5 to 0.7 in the inner
  halo from Gaia proper motions.
- Hand expectation (disclosed): on census baryons the framework is more likely to FAIL HOT in the outer
  bins than to fail cold, and the rotation-curve stellar mass moves it toward PASSES; per-bin errors of
  4 to 8 per cent may not resolve a 3 to 9 per cent gap. Comparator N must fail hot by a factor near 2.

## 2. Data

DESI DR1 MWS BHB VAC v1.0, https://data.desi.lbl.gov/public/dr1/vac/dr1/mws-bhb/v1.0/MWS_BHB.fits,
8,591,040 bytes, sha256 5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246 (matches the
directory's checksum file). Held outside the repository. Read with astropy.io.fits under `python3 -I`.
HDUs used: RVTAB (VRAD, VRAD_ERR, PRIMARY, TARGET_RA, TARGET_DEC), FIBERMAP (DIST, MAG_DERED_G, ABS_MAG_G),
GAIA (SOURCE_ID, PMRA, PMDEC, PMRA_ERROR, PMDEC_ERROR, PMRA_PMDEC_CORR, RUWE). Rows are aligned across HDUs
(same TARGETID order); the script checks TARGETID equality row by row and stops if it fails.
The catalogue has no distance-error column (see assumption list).

## 3. Sample cuts (in this order)

S1. PRIMARY == True (the catalogue's unique-star flag; the documentation says this is the only cut needed).
S2. Finite VRAD, VRAD_ERR > 0, DIST > 0, finite MAG_DERED_G and ABS_MAG_G.
S3. Galactocentric frame: astropy `Galactocentric` with R0 = 8.122 kpc (GRAVITY 2018), z_sun = 20.8 pc
    (Bennett and Bovy 2019), solar velocity (12.9, 245.6, 7.78) km/s (Drimmel and Poggio 2018; these are
    astropy's v4.0 defaults, set explicitly). Positions from TARGET_RA, TARGET_DEC, DIST.
    Line-of-sight velocity in the Galactic standard of rest: v_gsr = VRAD + v_sun . n_hat, with n_hat the
    heliocentric unit vector of the star in Galactocentric Cartesian axes.
S4. Sagittarius band: remove |B_Sgr| < 15 deg at all distances. B_Sgr is the latitude in the heliocentric
    Sagittarius frame of Majewski et al. (2003): Galactic unit vector x_gal, then x_sgr = A B C D x_gal
    with D = R_z(180 + 3.75 deg), C = R_x(90 - 13.46 deg), B = R_z(180 + 14.111534 deg) (astropy
    `rotation_matrix`, passive convention) and A = diag(1, 1, -1); Lambda = atan2(y, x), B_Sgr = asin(z).
    This cut depends on direction only, so it leaves the distance likelihood of section 4.2 valid.
S5. Galactocentric radius 20 <= r_gc < 80 kpc.
S6. Velocity clip |v_gsr| <= 400 km/s (nominal). Variants: 350, 500, no clip.
No correction for the LMC (its reflex motion and its own pull are ignored; stated, not modelled).

## 4. Estimators

### 4.1 Line-of-sight dispersion per bin
Bins in r_gc: [20, 30), [30, 40), [40, 55), [55, 80) kpc. A bin with fewer than 30 stars is merged with its
inner neighbour (the first bin with its outer neighbour), repeated until every bin has >= 30.
Per bin, maximum likelihood with v_i ~ N(mu, sigma^2 + e_i^2), e_i = VRAD_ERR; mu and sigma free.
68 per cent interval on sigma from the profile likelihood (Delta lnL = 0.5, mu re-maximised).

### 4.2 Tracer density slope alpha
Model: n(r) proportional to r^-alpha. For each star, conditional on its direction and on its absolute
magnitude (ABS_MAG_G, which the catalogue derives from colour and which is taken as independent of
position), the distance likelihood is p(d | dir, M_g) = d^2 r_gc(d)^-alpha / Z_i, normalised over the
star's window W_i: the distances at which the same star would have dereddened g in [16, 20] (the MWS BHB
target magnitude range, from Cooper et al. 2023 as remembered here: PROVISIONAL, not re-read) AND
20 <= r_gc(d) < 80 kpc. Window edges from the catalogue's own distance: d_lim = DIST * 10^((g_lim - g)/5).
Only stars with 16 <= MAG_DERED_G <= 20 enter the alpha fit (all S1 to S6 stars enter the velocity fits).
Assumption made explicit: within [16, 20] the spectroscopic selection and success depend on sky position
only (the DESI team states the selection depends on sky position; flat success in magnitude is assumed).
Z_i by trapezoid on 400 log-spaced points in W_i. Single slope fitted over 20 to 80 kpc; 68 per cent
interval from Delta lnL = 0.5.
Variant (two-slope): broken power law, continuous at 40 kpc, slopes alpha_in (20 to 40) and alpha_out
(40 to 80); 2-parameter ML; one-sigma errors from the inverse Hessian.
Reported variant (not part of the label): faint limit g = 19.5 instead of 20.

### 4.3 Anisotropy beta from Gaia proper motions
Stars with SOURCE_ID > 0, finite PMRA, PMDEC and their errors, RUWE < 1.4.
Per star: observed velocity components along (n_hat, e_east, e_north): (VRAD, 4.74047 d mu_alpha*,
4.74047 d mu_delta) plus the projection of the solar velocity on each of the three unit vectors, which
gives the Galactocentric velocity projected on those three directions. Model: Galactocentric spherical
velocity Gaussian, mean (0, 0, vphi_bar) in (r, theta, phi), covariance diag(sr^2, st^2, st^2), with
st^2 = (1 - beta) sr^2; rotated into the star's (n, east, north) basis. Error covariance: VRAD_ERR^2 on n;
on (east, north) the proper-motion covariance (with PMRA_PMDEC_CORR) times (4.74047 d)^2 plus a distance
term (0.10 x the observed tangential velocity component)^2 on each, a 10 per cent distance error assumed
because the catalogue gives none. Free: sr, beta, vphi_bar (per fit).
Usable bin: >= 30 stars with proper motions AND the median per-component tangential velocity error
(proper-motion part only) <= the bin's ML line-of-sight dispersion from 4.1 AND the bin's own beta has a
one-sigma error <= 0.3.
Nominal beta: one constant, ML over all stars of the usable bins together; one-sigma from Delta lnL = 0.5
with sr and vphi_bar re-maximised. Per-bin betas reported.
If no bin is usable: beta = 0.5 nominal, one-sigma range the bracket [0.2, 0.8] (sigma_beta = 0.3).
For a bin that is not usable while others are: in that bin the beta range used for errors and fragility is
the bracket [0.2, 0.8] (sigma_beta = 0.3) around the nominal value clipped into it.

## 5. Prediction per star

sigma_r^2(r) = (1 / (n(r) r^(2 beta))) * integral_r^Rmax n(s) s^(2 beta) g(s) ds, n = s^-alpha (or the
broken law), g the model's radial acceleration, Rmax = 2 x 10^4 kpc (trapezoid on 4000 log-spaced points).
Per star the predicted line-of-sight variance is P_i = sigma_r^2(r_i) [1 - beta sin^2 eta_i], eta_i the
angle between the heliocentric line of sight and the Galactocentric radial direction at the star.
Derivation: n_hat = cos(eta) r_hat + sin(eta) t_hat with t_hat tangential; with no streaming,
Var(v . n_hat) = cos^2 eta sr^2 + sin^2 eta st^2 = sr^2 [1 - beta sin^2 eta].
Scale factor per bin: v_i ~ N(mu, f^2 P_i + e_i^2), mu and f free, f = observed / predicted dispersion.
sigma_f: profile-likelihood half-width (mean of the two sides), combined in quadrature with
(f(alpha + s_a) - f(alpha - s_a)) / 2 and (f(beta + s_b) - f(beta - s_b)) / 2 (for two-slope: each of the
two slopes in turn).

## 6. Models (same alpha and beta for all)

FW-census: framework no-field line, McMillan 2017 baryons (stars 5.49e10, cold gas 1.191e10), each footing.
FW-rc: same with the stars (bulge, thin, thick) scaled to 7.08e10 (canonical) / 6.42e10 (alt); gas fixed.
The external field (0.000160 / 0.000110 in kernel units) is dropped: it leaves the line unchanged inside
300 kpc (owner note 2026-11-12).
Comparator N: Newtonian, census baryons alone. Comparator H: NFW M200c = 1.19e12 Msun, c = 12, h = 0.6777.
Comparators are reported, not graded.

## 7. Labels (per FW model and footing)

PASSES: |f - 1| <= 2 sigma_f in every bin.
FAILS COLD: some bin has f < 1 - 2 sigma_f (stars colder than predicted), none hot; FAILS HOT: some bin has
f > 1 + 2 sigma_f, none cold; FAILS COLD AND HOT if both occur. Failing bins are named.
FRAGILE (appended): the label changes in any of: alpha at its 68 per cent ends (single slope); beta at its
68 per cent ends (or bracket ends where the bracket applies); the two-slope density; the clip variants 350,
500, none. Variants are graded with their own f and the nominal sigma_f.

Reported without label: direct Jeans enclosed mass at 30 and 50 kpc,
M(r) = r sr^2(r) (alpha + gamma_s - 2 beta) / G, with sr^2(r) = s0 (r / 40 kpc)^-gamma_s fitted by ML to the
line-of-sight velocities of all S1-S6 stars (v_i ~ N(mu, s0 (r_i/40)^-gamma_s [1 - beta sin^2 eta_i] + e_i^2),
mu, s0, gamma_s free), single-slope alpha, nominal beta. Error: 300 bootstrap resamples of the stars
(alpha and the dispersion law refitted in each, fixed seed 20261112), with beta's one-sigma shift added in
quadrature. Printed beside the FW lines and DESI's 2.65 (+0.14 -0.13) and 4.51 (+0.27 -0.26).

## 8. Known-answer checks (all must pass before any label; the script stops otherwise)

K1. Synthetic sample at the real stars' positions with their velocity and proper-motion errors, from a flat
    rotation curve at 200 km/s, alpha 4.5, beta 0.5 (sr^2 = V^2 / 3.5); synthetic distances for the alpha fit
    drawn from p(d | dir) with alpha = 4.5 inside each real star's window; seed 12345. The full pipeline
    (alpha fit, beta fit with the usable-bin rule, f per bin with the flat model) must return
    |f - 1| <= 2 sigma_f in every bin and alpha within 2 sigma of 4.5; beta within 2 sigma of 0.5 if fitted.
K2. Projection formula: beta = 0 gives P = sr^2 for any eta; beta = 1 gives P = sr^2 cos^2 eta; and a
    Monte Carlo of 10^6 velocities at eta = 60 deg, beta = 0.5 matches P to 1 per cent.
K3. Jeans integral for a flat curve V = 200 km/s against sr^2 = V^2 / (alpha - 2 beta) to 0.5 per cent at
    20, 40, 80 kpc for (alpha, beta) = (4.5, 0.5), (3.5, 0), (4.0, 0.8).
K4. FW-census enclosed mass at 80 kpc = 5.691 (canonical) and 6.219 (alt) x 1e11 within 0.1 per cent;
    SI check: V = 200 km/s at 50 kpc gives M = r V^2 / G = 4.65e11 Msun within 0.5 per cent.
K5. Sagittarius frame: the Sgr core (l, b) = (5.569, -14.166) deg maps to |Lambda| < 2 deg (or > 358) and
    |B_Sgr| < 2 deg.
K6. Data sanity (magnitudes and identifiers only, no kinematics): TARGETID equal across HDUs; fewer than
    1 per cent of S1-S2 stars have MAG_DERED_G outside [15.9, 20.1] (else the magnitude window is wrong and
    an amendment is required); DIST agrees with 10^((MAG_DERED_G - ABS_MAG_G + 5)/5) / 1000 to 1 per cent
    for >= 99 per cent of stars (if not, reported, and windows still scale from DIST).

## 9. Mutations (separate output file raw1_mut.out)

M1. Comparator N (census baryons, Newtonian) must FAIL HOT (expected in every bin).
M2. a0 x 16 in FW-census, each footing, must FAIL COLD.
A mutation that does not bite is reported as such; it does not change the labels.

## 10. Reported variations for the assumption list (not part of the label)

Faint limit 19.5; R0 = 8.275 kpc with solar velocity (11.1, 251.5, 8.59) (GRAVITY 2021 / Schoenrich 2010
style); Sgr band 10 and 20 deg and no Sgr cut; catalogue distances scaled by 0.95 and 1.05; beta fixed at
0.2 and 0.8; distance-error term 0 and 0.2 in 4.3. For each, f per bin for FW-census both footings and the
direct masses at 30 and 50 kpc.

## 11. Changes

Never edited after the freeze stamp. Any change goes in AMENDMENT_A1.md (dated, before the re-run),
with the failed run's output kept.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
