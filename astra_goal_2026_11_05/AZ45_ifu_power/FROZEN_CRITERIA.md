# AZ45 — nonlinear synthetic IFU S/N and sample-size forecast (lane11)

Freeze before generating or fitting this lane's cubes. Kappa=1/2 FITTED;
not theory closed. Existing FN3/FN3b failure reports and engines were read.
This is a new conditional forecast, not a repair of those records. No
observed cube, survey fitted mass or cosmological distance is a new input.

## Contract and input decisions

Use the nonlinear `fn3_cube.py` forward model and law fitter, with the
stellar MGE, constant-Sigma gas and drift conventions documented there.
Do not call fn3_k2.setup, planck15, Native, DC14Mass or mu_mol_t20: the old
setup converts survey SED masses using a Planck15 distance, and Native
also imports a retired cold-background fit. Such imports would not be
framework-native evidence for this run.

Instead forecast a declared synthetic target population. Twelve equally
weighted templates are the Cartesian product of z={0.6,1.0,1.4}, stellar
log10(M/Msun)={9.5,10.5}, and inclination={35,65} degrees. For every
template set angular half-light radius0.4arcsec, physical half-light
radius2kpc (thus geometric scale5kpc/arcsec), Sersic n1, PA30deg, intrinsic
dispersion25km/s, line ratio0.7, total model flux1000 arbitrary units,
PSF FWHM0.6arcsec and Moffat beta2.8. H2 mass is0.3 times the reference
stellar mass. These are DESIGN ASSUMPTIONS, not measurements, derived
distances or predicted galaxy properties. The common geometric scale
is an observing-design convention; it is not an expansion history.

Use25x25 spatial pixels at0.2arcsec and25 spectral channels1.25Angstrom
wide, centred on the redshifted doublet midpoint. Use both fixed a0
footings separately:9.3603e-11 and1.1312e-10m/s2. No claimed healthy
redshift carrier is available (AZ42); here a flat reference a0 is a
hypothesis, not a sealed action prediction.

## Synthetic experiment

Follow the K2'' mass-residual diagnostic: flat truth has Delta=0;
rise truth has Delta=0.60(z-1) dex in log stellar mass at fixed reference
H2 and a0. This is the old diagnostic's mass-residual rise, NOT literally
an injected a0(z) law. Conversion of the result to an a0 slope requires
the newly computed response levers below. Report that distinction.

Use three independent realizations per template (36 galaxies per base
population). SeedStream=SeedSequence([20261105,45,template_id,replicate]);
draw gas with6*10**Normal(0,0.15)Msun/pc2, rejecting draws outside(0,15).
Draw one standard-normal noise cube per realization, held across S/N,
footings, truth scenarios and resolution pairs to reduce comparison noise.
The matched-filter S/N grid is30,60,120,240, with sigma=norm(model)/SNR.
Use own-rung forward truth and fit at each numerical rung; a separate
cross-rung truth/model comparison below prevents self-consistency alone
from being called convergence.

For each realization/scenario/SNR/footing fit both cases: HI free in[0,15]
and HI fixed6. Fit all FN3 geometry, dispersion and stellar-mass parameters,
using fn3_k2.bounds conventions but constructing the bounds locally.
The reference stellar mass is known in this synthetic experiment; real
SED errors are not silently folded into it. Use two deterministic starts:
reference geometry/mass/HI6, and x0+0.2,y0-0.2,lc+0.2,flux*0.9,
rhalf*1.1,n1.1,inc+2,PA+3,line ratio0.8,dispersion30,logM+0.2,HI8
(omit free HI for fixed case). Take the smallest finite chi2. Max nfev400
per start, same FN3 finite-difference fitter. Status<=0, nonfinite values,
or disagreement of accepted starts in Delta by>0.05dex is UNRESOLVED,
not a recovered population member. Report boundary hits within1e-4 of
the parameter interval as diagnostics. Never select only good recoveries.

## Controls and mutation (no copied -0.30 line)

Before noisy fits, compute a noise-free reference and doubled-a0 refit
for each template/footing/HI-case/rung at HI6, using the same two-start
fitter. The own-engine mutation lever is the doubled-minus-reference
fitted stellar-mass residual. Do not assume -log10(2): the stellar, H2
and HI partition and non-deep accelerations change it. Also compute
central local a0 log-derivatives at steps0.01 and0.005dex from noise-free
refits, retaining the geometry and HI nuisance freedom. Lever agreement
must be<=0.02 in absolute slope and the noiseless fits must be resolved.

MUTATE uses a0 doubled in each flat-truth noisy fit, in a separate output
tree. Its median shift minus the template-specific noise-free lever must
have magnitude<=0.07dex per redshift third. The original flat-residual
bias check must fail in at least one third for the mutation to bite;
otherwise report an ineffective control, not a pass. Report all levers
and failures. The doubled-a0 test is distinct from the smaller-step
derivative convergence test.

Known answers: (1) channel-integrated Gaussian probability from an
independent erf implementation agrees with the engine's ndtr differences
to1e-12 absolute; (2) PSF kernel DC normalization within1e-12; (3) with
all nuisance parameters held at truth, a one-dimensional noise-free
stellar-mass minimization from a0-correct synthetic cube recovers logM
within0.001dex for both footings; (4) a Gaussian linear-regression
population fixture has the exact analytic slope/variance, and independent
seeded draws cover its95% interval within binomial3-sigma uncertainty.
The restricted recovery check does not validate the full nonlinear fit.

## Sample-size scan and labels

At every S/N/HI-case/footing, first require all36 fits in each scenario
and all36 mutation fits resolved and numerically converged. No imputation.
Recovery gates inherited from the K2'' design: flat median Delta in each
third within0+/-0.07dex; flat slope within0+/-0.10; rising slope within
0.60+/-0.10. Slope is OLS on the three equal-weight bin means, with actual
z centres0.6,1.0,1.4; distinguish this from old FN3's Theil-Sen estimator.

Forecast independent populations of N={36,72,144,288,576,1152}, with equal
thirds, by stratified resampling of the fitted per-template residuals
(four templates equally represented per third, realization drawn with
replacement). This extrapolates the declared finite target population;
it is not additional observed galaxies or independent cube realizations.
Compute each realization's bin-mean slope and standard error from the
within-third sample variance. Add assumed common redshift-trend floors
sigma_s,sys={0,0.10,0.20}dex per unit z in quadrature. A redshift-independent
common offset cancels from this slope. Floors are explicit DESIGN
ASSUMPTIONS, not the inherited FN3b budget. The intrinsic fitted-residual
spread already includes the planted gas scatter and synthetic noise.

Detection requires slope>3*sigma_total. With512 and1024 identical-prefix
resamples (SeedSequence([20261105,4500,SNR,N,foot_index,HI_index])), report
rise power and flat false-positive rate, each with Wilson95% intervals.
Conditional WINDOW requires all recovery/control/convergence gates,
lower95% power>=0.80 and upper95% false-positive<=0.05. Monte Carlo rates
must change by<=0.03 across512/1024 and gate labels must agree. If all
grid cells fail power after valid calibration, FAIL within this grid;
calibration/control/numerical failure means NO VERDICT for affected cells.
Report the complete grid, not only a best sample. No universal minimum
sample size or physical a0(z) discrimination follows from this population.

## Numerical resolution, provenance and execution

Rung1: original os3, Hermite8, radial interpolation300. Rung2: os4,
Hermite12, radial interpolation600. For every graded fit require Delta
change<=0.01dex, population slopes<=0.02dex/z, and unchanged gate flags.
Compare the noise-free forward cubes across rungs at the same physical
parameters: norm difference/norm fine<=0.005. A miss stays UNRESOLVED.
Do not widen any line after seeing the results.

Each fit is checkpointable independently; SIGTERM/SIGINT set a flag,
checked inside residual evaluations and between fits, with atomic fsync
writes. Resume must skip only source-hash-matched complete records and
reproduce a small uninterrupted run exactly in scientific fields. Record
package versions, source hashes, timing and memory separately. One thread.
Benchmark the known-answer/one-fit pilot under1GB and minutes; the full
multi-hour grid belongs in heavyq after the light-tier work, never a
background shell job. Preserve required unfinished queue work as pending;
do not substitute a Fisher forecast for the requested nonlinear fits.

All new files stay in this lane. No source-engine changes, downloads,
deposits, messages, or real-cube acquisition. Commands and queued-job
contracts will accompany the implementation; criteria are committed alone.
