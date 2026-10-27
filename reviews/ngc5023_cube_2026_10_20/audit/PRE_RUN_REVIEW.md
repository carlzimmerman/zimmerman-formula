# Pre-run independent implementation inspection

Reviewed `cube_io.py` and `cube_analysis.py` on 20 October 2026 before
discovery output was available. This is a code/metadata review, not an
independent reconstruction of actual-cube numerical results. Root may amend
the code afterward; `PRE_RUN_PROVENANCE.json` pins the inspected version.

## Correct operations in the inspected version

- Actual primary FITS axis orders are `[channel, y, x]`, with dimensions
  `[69,1024,1024]` for HALOGAS and `[127,512,512]` for WHISP. Big-endian
  float32 and int16 data offsets/scales are explicit. The WHISP sentinel is
  detected before BSCALE/BZERO conversion and then set to NaN.
- The actual NCP headers have no unsupported rotation or CD/PC matrix.
  Northern-branch NCP forward/inverse formulas and FITS 1-based CRPIX usage
  are correct for these headers. `CRPIX3=0` in HALOGAS gives its first
  velocity 264.11999989 km/s, not 260 km/s. The legacy WHISP optical
  secondary reference is necessary. Both computed velocity axes increase,
  so the code's `np.interp` ordering is valid for these inputs.
- Native sky intensity is divided by the native Gaussian beam area, then
  convolved by a unit-normalized Gaussian whose covariance is target minus
  native covariance. This is the correct surface-brightness normalization;
  a target-beam area must not be multiplied in before angular integration.
- Reshaping `[60,60,150]` to `[10,6,6,10,15,10]`, summing axes `(1,3,5)` and
  multiplying by `4^2 * 4.12` correctly integrates the declared
  `40arcsec x 40arcsec x 24.72km/s` sample bins. Reversing all three binned
  axes compares opposite sky/velocity boxes.
- Center/velocity/PA perturbations leave candidate indices fixed. HR selects
  the candidate once; LR does not select a new one. Independent WHISP runs
  require a previously saved candidate rather than selecting from WHISP.
- The union of a moment0 source mask and its inverse is itself paired.
  This is an emission-*selection* mask; its noise conditioning still needs
  the qualifications below. Finite/common coverage is a separate condition.

## Required interpretation qualifications and recommended amendments

1. **Half-plane coverage.** `HALF=XX>0` excludes the entire central x=0
   bin, whose width is 40 arcsec, even though it contains non-self inversion
   pairs. Keep this as a declared central exclusion, or add a predetermined
   lexicographic tie rule using z. In the inspected code, the reported
   `paired_total_flux` is an aperture flux excluding this central bin, not
   the total galaxy flux.
2. **Control-specific covariance.** Center/PA/cubic/dewarp controls reuse
   baseline blank samples. Their amplitudes are valid sensitivity checks,
   but their quoted blank-scatter units are not exactly recalibrated under
   the changed operator. A source-selected threshold mask conditions its
   noise. Preserve descriptive terminology; do not claim a discovery p-value
   or compare these as exact standard-normal sigma.
3. **Incomplete spectral-response match.** HALOGAS has native Hanning
   smoothing in its header history. Similar channel spacings and 24.72-km/s
   integrated bins suppress sensitivity to native LSF differences, but do
   not constitute an exact matched-LSF convolution with WHISP. Include a
   common additional spectral-smoothing control if a small residual is close
   to the noise and its replication hinges on channel edges.
4. **Velocity reference.** HALOGAS has `SPECSYS=BARYCENT` and optical-barycentric
   history despite `CTYPE3=VELO-HEL`; WHISP uses legacy optical-heliocentric
   coordinates. Heliocentric/barycentric differences are small compared with
   the declared bins, but are not mathematically identical. The local
   metadata must preserve the actual header/history rather than calling all
   reference frames identical. The rest-frequency constants also differ
   slightly; the legacy secondary reference is the correct local anchor.
5. **Warp remains conditional.** The intensity-centroid dewarp is derived
   from the discovery data, clips at 30 arcsec, and uses positive weights.
   It can absorb true asymmetry and does not undo line-of-sight projection
   or reproduce the published asymmetric spiral/warp model. Its disappearance
   test is useful; survival cannot exclude that physical model.
6. **Baseline and image response.** Per-channel sky medians are a measured
   background correction and their values are saved. If the candidate is
   small, compare amplitudes with no or alternative blank-based subtraction.
   A restoring Gaussian is not the full dirty beam/deconvolution response;
   WHISP/HALOGAS residual sidelobes and brightness-dependent CLEAN effects
   remain potential source-region contaminants not guaranteed exchangeable
   with empty-sky apertures.
7. **WCS/units assumptions.** The beam-covariance calculation uses a local
   NCP pixel metric. This is appropriate at the small target extent but not
   a universal sky-projection formula. The independent cube's FK4/B1950
   center must have documented conversion provenance. `W.U.=5mJy/beam` must
   have primary instrument documentation; a matching-looking integrated flux
   cannot establish that scale. This review authenticates neither fact by
   reading intensity data.

The initial code has no use of LambdaCDM, a fitted gravitational halo,
stellar M/L or the project's acceleration law. Its physical blind spot
remains symmetric extra mass, which lies inside the null.
