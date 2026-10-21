# Independent completed-family audit

The saved calculations are internally reproducible within their declared
finite scope. They do **not** establish that the reconstructed preferred
model adequately fits the ordinary disk, and they are not a recovered joint
uncertainty distribution for its 206 nuisance parameters.

This review concerns the completed main family (104 labels), graphical
supplement (14 labels), and four numerical controls. The scan and its empirical
blank-sky comparison are reviewed separately in `stats_METHOD.md` and by the
statistical audit. No new shape fitting or renderer execution occurred here.
The independent audit imported no production modules.

## Frozen implementation and evidence

The reviewed `forward_model_v2.py` SHA256 is
`3ff79134be936f2a297d3cc948070ccee41df41ac657f106169076258b75a2aa`.
The three completed production-run manifests pin this same current renderer.
Their inputs and outputs validate against the current workspace, as does the
independent `audit/family_run001/manifest.json`.

Earlier `V2_NATIVE_REVIEW.md` records the independent analytic native-response
fixtures and split-side arm-quadrature checks. The anchored fine lattice and
exact native-node restriction correct the previous renderer's refinement
operator error. The tested native response improves with refinement; this is
finite numerical evidence, not exact certification of a CLEANed data cube's
unknown transfer function.

`check_family.py` independently reconstructs all 122 saved calibrations by
enumerating 27 lower/free/upper active sets for each three-column weighted
design. It also reconstructs the masks, source-flux coefficient bounds,
predictions, raw peak-fixed maps, residual metrics, singular values, explicit
0-to-3 diagnostic, control native-to-analysis rebinning, scenario identities,
and duplicate parameter sets. All 15 aggregated checks pass. Maximum absolute
coefficient difference is 5.00e-8; prediction difference is 4.64e-9 Jy km/s per
analysis bin. This verifies saved-result consistency; the audit is not another
independent astronomical dataset.

There are **118 labeled scenarios and 117 distinct parameter dictionaries**:
`joint_sobol_01` duplicates `nominal`. Counts should not be described as 118
independent fits or uncertainty samples. Relative training gates retain 76,
83, and 95 labels at 1.10, 1.25, and 1.50 times nominal RMS, respectively;
each includes the duplicate nominal dictionary.

## Calibration, conditioning, and amplitude limits

All 118 scenario optimizations converge and all three fixed component
columns have nonzero singular values. Their weighted design condition numbers
span 8.30 to 136.83. These are diagnostics of **only the three amplitude
columns with each geometry fixed**. They say nothing about identifiability of
the many geometry, lag, dispersion, density, and interpolation freedoms in
the original full fit.

Every scenario hits at least one amplitude bound. Both arms hit their upper
source-flux bounds in 72 of 118 labels. For the nominal reconstruction, the
coefficients are 0.99802, 1.14167, and 1.07853; the two arm coefficients sit at
their upper bounds. An explicit broader 0-to-3 amplitude diagnostic improves
nominal training RMS only from 8.1953 to 8.1148 blank-scatter units. Thus the
ordinary-disk mismatch is not closed merely by relaxing these amplitude
bounds.

The mass-calibrated width alternatives need careful interpretation. In
`width2_minus`, clipping the source-width perturbation at zero greatly reduces
the raw arm integral. Matching the separately quoted total arm flux then
requires a coefficient **14.36496**, at its lower mass-derived bound. This
case has training RMS 8.9099 and is retained even by the 1.10 relative gate.
Its peak density is consequently far outside the graphical peak-SBR readout
range. This is a conditional width/total-mass structural stress; it is not a
jointly source-constrained best fit or a draw within the graphical SBR error.
The retained raw peak-fixed maps make that change explicit. A finite global
rescaling does not restore emission at exactly zero-width finite-peak nodes.
The 0-to-3 diagnostic is correctly labeled with its actual coefficient range;
it is not a superset of source-bounded fits whose lower bounds exceed three.

The source component masses and allowed ranges come from fitting the same
galaxy cube. They are conditional normalization constraints, not independent
external priors. Published visual one-parameter deviations, digitization
readout errors, analyst-selected smooth modes, and structural alternatives
remain different sources of sensitivity. Thirty-two deterministic Sobol
points neither exhaust their 14-dimensional box nor provide probabilistic
coverage. Variance-matched Gaussian, sech-squared, and uniform height
alternatives use the appropriate scale conversions from the exponential
baseline.

## Actual residuals and numerical controls

The nominal RMS diagnostics in empirical blank-scatter units are:

| Region | Nominal | Cloud refined | Native plus cloud refined |
|---|---:|---:|---:|
| Training | 8.1953 | 8.1891 | 8.1893 |
| Validation | 1.14317 | 1.1432 | 1.1432 |
| Guarded validation | 1.05316 | 1.05263 | 1.05263 |

The best training RMS anywhere in the finite physical family is still 7.9289
(`phase1_plus`). These are correlated-data residual diagnostics, not
chi-squared statistics. A relative loss gate around an inadequate nominal
model cannot certify absolute model adequacy.

The independent saved-array reconstruction finds nominal-to-refined prediction
differences of 0.01769 scatter units RMS in validation and 0.01189 in guarded
validation. Turning off mean CIC-variance compensation produces 0.01317 and
0.00252, respectively, while its training prediction difference is 0.34145.
Those finite tested discrepancies are appropriately reported separately from
the data residuals. They do not bound all quadrature errors, the unknown
observational response, or numerical behavior across every perturbed geometry.
Equal or nearly equal aggregate RMS values alone would not prove that maps or
box sums agree; the actual prediction differences must be carried into the
specified scan, as the analysis does.

Training has 638 bins with centers at |z|<=10 arcsec (full footprint
|z|<=20). Validation has 2216 bins starting at centers |z|=50 (footprint40);
guarded validation has 1662 starting at centers70 (footprint60). Paired
known-feature exclusions and the stated beam/velocity guards are reproduced
exactly. Beam wings still couple these regions. The published preferred
shapes already used this same cube; neither this protected split nor the
previously examined WHISP data is a blind independent discovery holdout.

## Claim boundary

This is a physically meaningful 3D optically thin asymmetric disk/arm
**reconstruction with an executed finite sensitivity family**. Its unit,
normalization, side geometry, source quadrature, native projection, and saved
calibrations have explicit finite checks. It is not the exact unavailable
preferred TiRiFiC parameter file or implementation, a refit of that full
model, or propagation of a recovered full covariance.

The unresolved ordinary-disk mismatch limits both positive and negative
physical conclusions. A finite protected-box scan can describe whether an
integrated remainder is robust across its retained model alternatives and
empirical controls. It cannot prove that the whole cube has been explained,
establish a new gravitational interaction, exclude all weak signals, or
identify or exclude a physical memory state. Any sharper statement needs
both an adequate ordinary HI model and genuinely informative independent
measurement, not wider uncertainty envelopes alone.
