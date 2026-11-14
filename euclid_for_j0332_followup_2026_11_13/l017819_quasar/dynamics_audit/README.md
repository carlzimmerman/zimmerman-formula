# L017819 native DESI stellar-dispersion audit

Research resumed with explicit user authorization after the preserved `PAUSED_HANDOFF.md`. Three bounded runs completed on 2026-11-13 local time (2026-11-14 UTC). The historical `fit_dispersion.py` remains unchanged; it is not an evidence-generating version.

**Best surviving result:** a conservative absorption-window fit gives **221.36 km/s**, with conditional profile crossings **201.81–242.61 km/s at Δχ²=1** and **183.75–266.34 km/s at Δχ²=4**. This is an independent reduction of the existing DESI photons, not independent spectroscopy. It supports Guo's central value near 222 km/s but does **not** validate a complete uncertainty of ±15 km/s. Source-window treatment matters, and no unique full uncertainty or stellar-mass prior is supplied here.

## How to use this result

For a conditional dynamics calculation, retain `run_02/primary_split.json`'s full dispersion/velocity profile as one explicitly labeled likelihood fixture. Its minimum is σ=221.3584213 km/s, velocity offset +17.5874850 km/s relative to z=0.3202209572, χ²=1786.980674 on 1776 retained pixels. The quoted intervals are linearly interpolated profile crossings, not marginal Bayesian credible intervals. They condition on the stellar templates, smooth additive quasar continuum, masking, Gaussian LOSVD and diagonal pipeline noise.

Carry `run_03`'s alternatives as separate sensitivity fixtures. Do **not** combine their scatter into a newly measured Gaussian uncertainty, average profile scores across different pixel selections, multiply Guo/FastSpec likelihoods as independent data, or identify one control as the uniquely true dispersion. The conservative joint configurations cluster near 220–230 km/s; allowing more of the region around source Mg II gives about 244–245 km/s. The next improvement would require a defensible quasar/Fe II or stellar-abundance treatment, additional spectral information, or an explicit model for these uncertainties—not further arbitrary mask selection to obtain a chosen result.

No aperture correction, rotation separation, Jeans fit, new stellar mass or gravity inference was performed. The measured quantity remains a blended-fiber spectral broadening estimate. The 0.75 arcsec radius fiber is not known to be centered on the fitted galaxy light: its mean position is offset 0.2980 arcsec from the catalogue coordinate, with the actual light-center offset still to be applied by the dynamics model.

## Data and forward model

- Native B and R flux, inverse variance, masks and 11-diagonal DESI response arrays come from sibling `desi_spectrum/target_coadd.npz`, TARGETID **39633153882587315**, coadd row 141. The target-specific extraction has its own `validation.json` and HTTP-range provenance. No full-parent-coadd checksum is claimed.
- Wavelength samples remain on the native 0.8 Å vacuum grid. Only finite flux, positive inverse variance and zero native mask pixels are fitted.
- Twenty-four E-MILES nuisance templates span ages 1, 1.5849, 2.5119, 3.9811, 6.3096 and 10 Gyr and metallicities −0.71, −0.40, 0 and +0.22. This restricted library is not a measured stellar population or mass-to-light ratio. The local NPZ hash matches previously recorded provenance; its optical FWHM array is 2.51 Å throughout the fitted region.
- E-MILES air wavelengths are converted to vacuum. The template Gaussian width is subtracted in variance from the requested stellar broadening before applying the measured instrument response. This local wavelength-space Gaussian approximation is explicitly benchmarked; it is not exact general deconvolution.
- The original DESI response, including negative entries, is applied with scipy DIA offsets `[5,4,3,2,1,0,-1,-2,-3,-4,-5]`. Neither transpose nor row renormalization is used. Both stellar templates **and the incident smooth continuum** pass through this response in the authoritative runs.
- Stellar-template weights are nonnegative; independent additive Legendre continua per window have unrestricted coefficients. Velocity and Gaussian dispersion are nonlinear parameters. Linear weights and continua are profiled by weighted QR projection and nonnegative least squares. No physical quasar/Fe II template, multiplicative continuum, non-solar abundance library or higher LOSVD moment is fitted.

The conservative primary uses lens-rest vacuum windows **B: 3800–4380 Å** and **R: 4950–5500 Å**, degree-four continua, with specified foreground narrow-line and terrestrial-sky masks. In expanded-window controls R begins at 4400 Å and masks of ±100, ±200 or ±300 observed Å surround source Mg II at 2799.12×2.210 Å. All selections, bounds and starts are explicit in the frozen code and contracts. Dispersion bounds are 100–450 km/s and velocity bounds ±300 km/s; reported authoritative optima are interior.

Primary conventions are documented in the cached [DESI response implementation](https://raw.githubusercontent.com/desihub/desispec/main/py/desispec/resolution.py), [pPXF template README](https://raw.githubusercontent.com/micappe/ppxf_data/main/README.md), and [pPXF SDSS example](https://github.com/micappe/ppxf_examples/blob/main/ppxf_example_population_gas_sdss.ipynb). The example identifies the MILES air-wavelength convention. Cached originals and retrieval hashes are under `inputs/`. This custom native-response fit is not a reproduction of the undocumented details of Guo's pPXF analysis.

## Numerical and observational controls

The independent diagonal-index calculation agrees with the official DESI constructor to ≤4.44×10⁻¹⁶. Eighteen analytic Gaussian-line tests (three lines, three dispersions, two samplings) recover input dispersions with maximum error 0.00237 km/s. A noiseless planted mixture at σ=250, velocity=37 km/s recovers 249.98398 and 36.99843. This injection tests the optimizer and finite identifiability within the model; it is not independent astrophysical validation. Refining template quadrature from 0.9 to 0.3 Å shifts the corrected real-data result by **−0.00555 km/s**. Interpolation does not add genuine template resolution.

| Corrected response configuration | Best σ, km/s | Δχ²=1 profile interval, km/s |
|---|---:|---:|
| Primary conservative joint | 221.36 | 201.81–242.61 |
| Continuum degree 2 | 220.35 | 202.36–240.78 |
| Continuum degree 6 | 223.47 | 203.41–245.28 |
| Continuum degree 8 | 222.44 | 202.24–244.35 |
| Templates older than 3 Gyr | 221.20 | 201.73–242.48 |
| Remove Mg b region from joint fit | 227.93 | 204.74–254.03 |
| Expanded window, Mg II ±100 Å | 244.03 | 223.90–265.84 |
| Expanded window, Mg II ±200 Å | 245.08 | 224.13–267.69 |
| Expanded window, Mg II ±300 Å | 225.09 | 205.32–246.57 |
| Remove 12 response-normalization outlier pixels | 224.48 | 204.40–246.50 |
| Blue window alone | 255.43 | 223.32–291.80 |
| Red window alone | 189.19 | 165.94–215.23 |

The individual feature controls are Ca H/K 249.49 (201.86–306.51), G band 240.71 (202.96–283.77), Mg b 205.24 (170.55–247.88), and Fe window 190.60 (158.61–228.24) km/s at Δχ²=1. Their broad intervals overlap; no single feature establishes the entire blue–red difference. These are not mutually independent complete stellar-population measurements.

The corrected blue-minus-red difference is **66.2341 km/s**. In 48 seeded conditional Gaussian noise injections of the reconstructed shared best model, **4/48** produced an absolute difference at least that large. The simulated difference quantiles (2.5,16,50,84,97.5 percent) were −53.49, −32.63, +1.31, +47.95, +81.34 km/s. All 96 band fits converged, none hit dispersion bounds, and the largest two-start disagreement was 0.145 km/s. This is a finite conditional model-check frequency, not a calibrated astrophysical p-value or proof that unmodeled effects are absent. It suggests that the observed split alone need not establish a failed common-dispersion model.

Primary standardized-residual RMS is 1.0083 in B and 0.9972 in R. The adjacent-pixel mean residual products are −0.0117 and +0.0547 respectively; these are descriptive checks, not a full noise-covariance model. Figures `run_02/dispersion_audit.png` and `run_03/controls_and_noise.png` were visually inspected.

## What happened to run_01

`run_01` is preserved and numerically completed, but its 211.20 km/s headline is **superseded**. It passed the analytic and injection checks while placing the additive continuum directly in observed-pixel space. That is an incomplete physical forward model at non-unit instrument-response rows. Twelve retained pixels have response-row sums differing from unity by more than 1%. Applying the same DESI response to all incident light gives 221.36 km/s in `run_02`; removing those pixels gives 224.48. The original benchmarks remain useful, but run_01 is not the adopted spectral fixture. This illustrates why internal injection success alone is insufficient scientific validation.

## Comparison with published reductions

Guo's 222.26 km/s has primary-profile Δχ²≈0.0019, essentially at this conditional minimum. FastSpec v3's 284.418 and v2's 317.619 km/s have primary-profile Δχ²≈7.19 and 14.41. With the less-conservative ±200 Å source-line mask these fall to approximately 2.74 and 8.11. These are same-spectrum conditional fit penalties, **not independent-data significance levels or a formal rejection of either pipeline**. Root's `fastspec_crosscheck/` documents those target-specific values and their photometric/blend limitations. The present audit favors Guo's central scale under conservative absorption masking while leaving complete uncertainty unresolved.

## Contracts, provenance and terminal state

Each `contract_0N.json` lists its exact input closure. Each `run_0N_command.txt` records the complete authorized runner command. All three v2 manifests validate against current inputs; each records `completed`, exit status 0, a 300-second cap and one numerical-library thread. Actual runner times were 18.36, 14.18 and 83.27 seconds. Computational outcome: **finite numerical checks passed; observational interpretation remains conditional on the stated model and controls**.

Actual coverage: run_01 has six spectral configurations, one sampling control, eighteen analytic-line cases and one injection; run_02 has eight spectral configurations, eighteen analytic-line cases and one injection; run_03 has eight spectral configurations, one sampling control and 48 two-band noise injections. Run_03's contract retains analytic-case bound metadata from the earlier contract, but its assertion and script do not rerun those analytic cases; no additional analytic coverage is claimed.

| Evidence | SHA-256 |
|---|---|
| run_02/result.json | `7be4f12de38b1ab7f45cde1360531d4dc40ed9bd1e4570cf64b78e0e928bf06b` |
| run_02/manifest.json | `7a41c2953d9228ed94a3490272e5ed21d5241fea407e5715f41f17ec29334b8d` |
| run_03/result.json | `dee48c636ee776fa45f3b828442511e018a56ebd3169954b2372d0a179c0e846` |
| run_03/manifest.json | `df6edc06e7f40668305b5ce1dc4bd13755fc9c4c30ec80d5bdbde12c8ca6b760` |

Run_01 session **97643**, run_02 session **32510**, and run_03 session **52027** all returned terminal exit 0. No numerical job remains live from this task. No shared program/handoff file or Git state was edited. Additional unrelated working-tree changes are outside this audit's scope.
