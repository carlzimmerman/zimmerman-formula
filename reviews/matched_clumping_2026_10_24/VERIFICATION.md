# Verification

- Bounded primary run: completed, exit 0; ten implemented controls passed.
- Deliberate doubled-acceleration mutation: failed, exit 1 at the physical reconstruction assertion for Antlia II, as intended.
- Both manifests validated with computation-audit/scripts/validate_manifest.py and project root supplied. A valid mutation manifest records an expected failed computation.
- Separate readback checked every matched CSV Delta against log10(gobs)-log_gref.
- Separate Astropy units/constants reconstruction checked every cluster residual mass against the stored mass with relative tolerance 0.001 (constants differ slightly from the deliberately fixed analysis constants).
- Readback confirmed 42 cluster target radii, 29 unsupported dwarfs, and 26 dwarfs with zero reference galaxies.
- Generated comparison.png was visually inspected: both panels, axis labels, legends and sample distinctions render without clipping.
- git diff --check returned no whitespace errors for this lane.

The controls validate the stated calculation and output consistency, not the astrophysical equilibrium assumptions or absence of missing baryons. The report explicitly separates sampling uncertainty from systematics and effective residual mass from physical cold mass.
