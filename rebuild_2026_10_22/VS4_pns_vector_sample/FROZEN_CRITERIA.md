# VS4_pns_vector_sample: FROZEN CRITERIA, committed alone before any offset

Owner's yes, 2026-11-02, to downloading arXiv e-print 1712.05833 (Pulsoni+2018, 5,583,930 bytes, sha256 d7d964a0...c6c4f) after "settle it then". **Not blind:** VS1 to VS3 are known; the slow-rotator dispersion figure was viewed, and central labels of the slow rotators were listed before this file. kappa = 1/2 FITTED. Footings never pooled. Reinstates nothing; cold sector stays retired. Not theory closed. Nothing here says the data favour the framework.

## Question
At fixed mass, on one tracer and one method, does the outer excess follow slow rotation, being central, or neither?

## Data
The paper tabulates no dispersions and its new catalogues are not in the source. Binned PN dispersions, errors and radii are read from the vector paths of `SR1_sigma.pdf` and `FR1-3_sigma.pdf`: navy markers and their error bars only, not the grey interpolated curves or the stars. Axis ticks are read from each panel's rendering and recorded in the script. D, R_e, ellipticity and systemic velocity from the paper's tables. These values come from a figure and stay labelled as such. Sample: galaxies in the paper with an ATLAS3D JAM row and class in Emsellem+11; JAM quality 0 kept and flagged.

## Offset
CFG492's law path unchanged: nu_mono, Hernquist a = R_e/1.8153, `jam_mass` from ATLAS3D scaled to the paper's distance, Hernquist PN tracer, beta = 0, exact projection. Radius: major-axis distance x R_e x sqrt(1 - eps). Outer bins R > max(R_e, 2 kpc); offset = mean log10(sigma_obs/sigma_law). Error: the mean bin error in dex over sqrt(N bins), reported; the fit uses residual scatter.

## Central label
VS2's rule on 2MRS. **Primary window changed to 1000 kpc and 1000 km/s, chosen after seeing labels**, because at 500 km/s NGC 4552 (361 km/s, in Virgo) reads central through the velocity cut alone. 500/500 and 300/500 are reported.

## Fit
OLS, each footing: O = c + m (log M - mean) + s Slow + k Central, errors from residuals. Slow non-centrals are counted.

## Labels, same on both footings, otherwise FOOTING-DEPENDENT
- **SETTLED ROTATION:** at least 4 slow non-centrals; s >= +0.10 at > 3 sigma; |k| < 1 sigma; and s > 2 sigma both without JAM quality 0 and at 500/500.
- **SETTLED ENVIRONMENT:** k >= +0.10 at > 3 sigma; |s| < 1 sigma; same two robustness checks on k.
- **SPLIT NOT REAL:** s + 2 sigma < +0.10 and k + 2 sigma < +0.10.
- **LEANS ROTATION / LEANS ENVIRONMENT:** the coefficient >= +0.10 at > 2 sigma and the other under 1 sigma, without the settled conditions.
- **UNDECIDED** otherwise.

## Controls, before the label is read
- **C1 extraction:** overlap galaxies against CFG492's committed O_PN, canonical. RMS difference above 0.05 dex means NO VERDICT. Different catalogues folding and binning are expected, so this is a tolerance on method, set from about 0.08 dex galaxy scatter.
- **C2 axes:** a marker count per panel is printed against the rendering, and the outermost tick of each axis is checked against a frame edge.
- **MUTATE:** slow labels shuffled within mass terciles; s must fall below 2 sigma on the same seed. Failure means NO VERDICT. Outputs named by mode.

## Reported limits
Dispersions are read from a published figure, smoothed by the paper's method. Isotropic Jeans. Environment is a magnitude rule. An offset is not a halo, and no mechanism is tested.
