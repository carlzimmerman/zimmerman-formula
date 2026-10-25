# CCT-008 result: a supported endpoint exists in a statistical-field extension

There is a constructive improvement over the failed collapse runs. At a common eta=1500 pc km/s, positive bound-mode occupations reproduce all four previously chosen cold profiles. The Sextans construction retains ~425 million Msun overall while placing only ~8.62 million Msun inside 486 pc. It has a density-preserving net-spin storage channel. Direct spherical self-gravity evolution leaves the constructed envelopes nearly stationary, including a small breathing perturbation of Sextans. This is an approximate stationary density-matrix construction, not successful formation from the old coherent collapse initial condition.

## What changed

The previous eta=3000 benchmark was incompatible with the exact chosen Draco and Leo I target profiles already at the kinetic-energy/virial level. Analytic amplitude-gradient energy is T_Q/M=15 eta²/(28 b²). The corresponding ceilings are 2763 and 2483 pc km/s for those two targets. This corrects a structural problem that stronger cooling could not fix.

The new value was selected by a disclosed scan. At eta=2000 the finite spectral fit still misses the Leo I 5% aperture criterion (5.84%); eta=1500 fits all four. Neither this parameter nor the cold supply is derived from cosmology.

## Finite reconstruction and data diagnostics

The refined library has 6144 radial cells, rmax=20 cold scales, L<=80 and up to 48 radial states/l. All fitted occupations are nonnegative and use negative-energy eigenstates. Maximum enclosed-mass discrepancy at 60 apertures spanning 0.08..12 cold scales:

| Galaxy | Maximum aperture discrepancy | Cold mass inside stellar half-light radius |
|---|---:|---:|
| Draco | 0.0905% | 11.609 million Msun |
| Sextans | 0.0192% | 8.623 million Msun |
| Fornax | 0.0313% | 17.477 million Msun |
| Leo I | 0.3411% | 6.715 million Msun |

Maximum cold-potential discrepancy is below 0.25%; truncating the Plummer tail at 20 scales omits ~0.374% mass. The outermost-cell potential discrepancy includes that tail. (The normalization target uses the last interior radius.)

Static stellar diagnostics retain the calibrated global dispersions: Draco 9.5499, Fornax 12.1000 and Leo I 9.2896 km/s. These profiles were chosen using those moments, so this is retained calibration, not a new independent observational prediction. Sextans' actual 298-position conditional survey fit differs from its reference by 2 Delta NLL=-0.00109, numerically negligible. Its survey/anisotropy/stellar-model limitations remain inherited from CCT-006. No live-star heating result is supplied here.

A deliberate L<=4 control with 160 radial states/l fails Sextans by 68.46% in the maximum relative enclosed-mass criterion, versus 0.0192% for the refined full library. This supports high angular support as a missing endpoint channel in that finite library. It is not a universal lower bound on angular degree for all possible profiles. Different successful occupation fits are not unique.

## Net spin, not merely angular dispersion

Biasing +m versus -m at fixed pair sum leaves the density exactly unchanged; an independent spherical-harmonic check verifies this to floating-point precision. Sextans' refined fit has constructive net-j capacity ~7277 pc km/s. The old source angular SHAPE, rescaled to eta=1500, has j~1178 pc km/s. Storing all of its benchmark source J in the final Sextans mass requires ~2521 pc km/s, below that capacity. This establishes storage capacity without adding mass or extra stellar gravity.

For the particular compact fits and the old oversized common source prescription, Draco/Fornax/Leo I still require export of at least ~98.4/99.65/99.91% of the source spin. Those are fit-dependent bookkeeping requirements; changing supply or permitted outer profiles changes them. The common source prescription still does not predict the four retained inventories.

## Direct evolution

A separate radial solver reconstructs the occupied eigenfunctions, then evolves their shared self-consistent Poisson potential, with fixed baryonic Newtonian potential and no density renormalization. This tests the spherical density-matrix extension, not the coherent 3-D parent. The isolated radial box is reflecting at 20 scales, so these are remnant-response tests, not escape/cooling measurements.

| Run | Duration in cold dynamical units | Maximum absolute enclosed-fraction change | Maximum relative energy drift |
|---|---:|---:|---:|
| Draco, dt=.02 | 10 | 0.0000120 | 1.26e-9 |
| Sextans, dt=.02 | 10 | 0.00364 | 5.87e-5 |
| Sextans, dt=.01 | 20 | 0.000932 | 3.70e-6 |
| Fornax, dt=.01 | 20 | 0.0000580 | 1.05e-8 |
| Leo I, dt=.01 | 20 | 0.000150 | 1.08e-9 |
| Sextans, breathing kick, dt=.01 | 20 | 0.0140 | 4.20e-5 |
| Sextans, breathing kick, dt=.005 | 20 | 0.0144 | 1.10e-5 |

The kick imposes radial velocity v_r=0.01 r in code units. In the refined kicked case, cold mass inside Sextans' stellar aperture varies by -6.71% to +0.80% from its initial value. This is a real central force variation; it must not be sold as zero stellar disturbance. The unperturbed dt dependence shows finite splitting error and warrants further refinement before precision lifetime claims. Twenty Sextans units are about 1.03 Gyr for this target scaling. Maximum mass drift in these runs is below 2e-12.

## Checks, source history and limits

`verification.json` records independent analytic integral identities, the density-preserving spin identity, static stellar-force diagnostics and input hashes. `spectrum_v1.py` preserves early runs before the Sextans baryonic profile was corrected to its two components. `spectrum_v2.py` preserves the refined all-l producer before adding the explicit parity switch. `evolve_v1.py` preserves the producer before adding a stellar-aperture diagnostic. The JSON run pins identify the precise producer bytes; archived hashes resolve them.

The even-l reconstruction also passes the 5% endpoint criterion (Draco 4.48%, Sextans 0.0196%, Fornax 2.09%, Leo I 2.26%). The old even-m seed restriction is separate and unresolved. Successful fits do not establish a connected formation trajectory.

Largest observed process RSS was 992,952,320 bytes, below 1 GB but close; future full-library refinements must use a more memory-efficient column representation. Response runs used less than 100 MB each. No shared production job or frozen criterion was changed.

The remaining physical obligation is sharply defined: a coherent or justified coarse-grained collapse must populate the supported envelope, conserve mass/energy/vector spin including outgoing waves, select the different retained supplies and survive nonspherical and stellar-heating tests. `MECHANISM.md` gives the explicit conservative interaction and the seed-symmetry issue. This result supplies a viable conditional endpoint and corrects a parameter obstruction; it does not complete the theory.
