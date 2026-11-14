L017819 SAME-FIELD LENSING / DYNAMICS CHECK
2026-11-13 America/New_York

Outcome: conditional kinematic compatibility, not a calibrated theory pass.
The original breakthrough/full-theory-certification objective remains open.

The final nonnegative-host image fits at fixed logsourceprecision2 give
infinite-total stellar masses2.323954874e11 and2.144492008e11 Msun for the
run04/run03 light fixtures. Feeding their actual oblate AQUAL force fields
into a cylindrical Jeans model predicts fiber RMS205.65–216.03km/s over
b=.8,1,1.2 and seeingFWHM.8,1.2,1.6arcsec. Satoh k=1 central dispersions
are205.35–215.75km/s. Every sampled case has nonnegative azimuthal moments
and zero reported light fraction failing the specified Satoh tolerance.
The DESI absorption-profile minimum is221.36km/s, with conditional
DeltaChi2=1 crossings201.81–242.61. These scales are compatible under the
stated models; this is not a combined posterior or a complete error budget.

The nativeFITS WCS maps DESI MEAN_FIBER_RA/DEC to localpixels
(46.61610734,48.94705331). Relative to fittedlight, the aperture offset is
west−.14394110,north−.10203393arcsec (separationabout.1764arcsec).
This differs from the catalogue-position separation; all calculations use
the actual pixel-to-sky convention. Fiber radius=.75arcsec, lensz=
.32022095721117494,sourcez=1.210,scale=4.80283270817kpc/arcsec.

Sensitivity at FIXED mass2.329069979e11Msun, primaryprofile,b1,seeing1.2:
Newtonian stars only204.41km/s; a0/2:208.23; fixeda0:211.46; 2a0:216.98.
Primary spectral profile penalties at these predictions are approximately
.80,.49,.25,.11. They are descriptive evaluations of one conditional
spectrum likelihood, not profile likelihood ratios between gravity models.
Stellar mass and light were NOT refitted for these alternative laws.
The factor-four a0 range moves the prediction8.75km/s, smaller than the
conditional statistical spectral width and source-window sensitivity.
Do not call the Newtonian stars-only control a dark-matter cosmology fit.

Numerical evidence:
- benchmark_01 is an intentionally preserved FAILED v1 Plummer check.
  Its low-order pressure integral/derivative was insufficiently accurate.
- benchmark_02 uses separate v2 code. Plummer intrinsic errors<.043%;
  analytic aperture second moments at0/45/90deg agree within.0065%.
- independent_review uses a flattenedGaussian tracer in a harmonic force,
  with independent GaussHermite sky integration: secondmoment error<9e-5.
- fields_01 vs fields_02 doubles momentgrid440→880, outerextent300→600Re,
  aperture200→400nodes, azimuth64→96, LOS160→240. Actual high-n predictions
  change≤.00264km/s. Physical forcegrid320x64→448x80 changes≤.016km/s.
- fields_03 updates both fields to the SS6 Gaussian-host mass optima.
- fields_04 uses actual direct fields at the NONNEGATIVE-host lnprecision2
  mass optima. This is the final physical-source mass fixture for this route.
- a0_sensitivity_01 independently doubles bothManda0. Fieldarrays and
  aperturesecondmoments scale by2 at recorded floating precision.
- summary_04/result.json and a0_kinematics.png are the final comparison.
All completed runs have boundedv2 provenance. An evidence-valid manifest
for a failed run is not a successful numerical benchmark.

Implementation/conventions and the primary Cappellari2008 source mapping
are in DERIVATION.txt. Run manifests preserve exact argv and input hashes.
To reproduce a plain numerical command into a NEW directory:
/private/tmp/forj0332-fit-venv/bin/python euclid_for_j0332_followup_2026_11_13/l017819_quasar/joint_dynamics/run_jeans_v3.py --mode fields --fields euclid_for_j0332_followup_2026_11_13/l017819_quasar/joint_dynamics/fields_04.json --output /private/tmp/l017819-jeans-reproduction
For a provenance-recorded rerun, reuse fields_contract_04.json with the
installed computation-audit bounded runner, every execution_artifact as an
input, and a fresh output/result directory. Never overwrite an evidence run.
Python3.9.6,NumPy1.26.4,SciPy1.13.1,Astropy6.0.1 were used.

Scope limits: edge-on oblateconstant-M/L tracer; cylindricalalignment and
constantb, where beta_z=1−1/b (not sphericalanisotropy); noBH/gas/gradient,
no measuredseeing, no full nonnegativeDF proof, no higherLOSVD moments.
Satohk1 makes sigma_phi=sigma_R; it is fully isotropic onlywhenb1.
Reported light beyond the momentgrid is tiny, but is not a rigorous moment
errorbound; domain-extension is a finite convergence check. The adopted
AQUAL model is the isolated smooth unscreened branch at a0=9.3603e-11,
not the complete screened action. An arbitraryline-of-sight convergence
is not a self-consistent AQUAL external field. Galaxy profiles remain
SIE-deblend-dependent sensitivity fixtures. Imagingresiduals remain large
and the standardcontrol fits better, even with positivehost mass refits.
No joint stellarSEDprior is justified by the multiband audit.

FINAL FAIR NEWTONIAN CONTROL

fields_05 uses the same light-centred density and physical-source constraints,
but Newtonian stars-only gravity, with mass refitted. Newton masses are
2.97968e11 and2.75352e11Msun; imagechi2 is34.45/35.83 lower than AQUAL.
FiberRMS scenarios224.82–236.82km/s also overlap the DESI interval.
This removes the SIEcenter/shape confounder but does not remove the shared
foreground/source and noise limitations. No calibratedgravity preference,
exclusion or darkmattercosmologycomparison follows. The v4 loader explicitly
reads mu_one and uses a Newtonian outer force for these files.
