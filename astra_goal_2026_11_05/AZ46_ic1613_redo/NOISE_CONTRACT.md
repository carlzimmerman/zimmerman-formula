# AZ46 physical-noise implementation, before mock fits

Use the frozen SeedSequence([20261105,46,weight_index,foot_index,mock_index]),
with NA/R mapped to 0/1, canonical/alt to 0/1, and law/slow mocks to 0/1.
Generate standard-normal native cropped pixels in channel-major, row-major
order with NumPy's default_rng. Keep the full native spectral range and
physical crop. Each channel is convolved periodically with its own CLEAN
beam, pixel-integrated at the native pixel size with supersampling5.
Apply the inherited spectral [1/4,1/2,1/4] kernel with nearest extension
at the two ends of the full native channel range, then average spatial
blocks to the requested rung. Only then select the prepared mask's spectral
range. Thus different spatial rungs use the same physical noise realization,
even if their masks select different channel ranges. Three rolling native
planes suffice; never allocate the whole native noise cube.

Normalize the resulting noise by its population standard deviation over
the complete trimmed cube, including unmasked voxels, to the prepared
weighting/rung's measured voxel rms. Do not subtract its realized mean.
Record seed, rms before/after scaling, mean and scale factor. Rung pairing
holds before this deterministic rms normalization; compare unscaled block
averages in the implementation known answer. Do not claim a measured full
interferometric covariance: beam and Hanning correlations are an explicit
synthetic convention inherited from FN4a, not a visibility/noise model.

The signal uses the primary stellar mass2.88e7, thickness200pc, centre0,
PA73.7, systemic velocity-232.2, inclination35 and sigma9. Compute the
law's pressure-supported rotation on that prepared cube; multiply rotation
by1 or0.505 for the two mocks, then beam-convolve and locally normalize by
the unchanged conditional forward model before adding noise. Preserve each
cube's own observed intensity template, mask and sampling lattice. These
mocks calibrate that conditional model; they do not test mask recovery.

Implementation checks (distinct from frozen fit-based KA1/KA2): streamed
versus full-array reference and exact shared-field block averaging within
1e-12 absolute, requested rms within1e-12 relative, exact deterministic
repeat and seed separation, and stop callback at a channel boundary.
A seeded64-channel64x64 fixture checks lag-one spatial correlation against
the discrete beam autocorrelation and interior spectral correlation against
2/3, each within0.05 absolute. An uncorrelated-noise mutation must fail
these same correlation lines. These tolerances are fixed before the fixture
is run and do not replace any physical or convergence acceptance gate.

Kappa = 1/2 FITTED; not theory closed.
