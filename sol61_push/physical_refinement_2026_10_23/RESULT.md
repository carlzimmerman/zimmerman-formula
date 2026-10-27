# Physical refinement and initial histories: result

**No resolved, mass-selected bound core is established.** The new spherical calculation resolves the inherited 0.3215 kpc radius and gives converged mass within that aperture. It also reaches shell crossing for a stronger seed. The central concentration itself remains unresolved and continues accreting. These are conditional numerical results for a radial, pressureless-baryon restriction, not a negative theorem about the full theory.

## Finite results

All quantities below are at z10, except the indicated continuation. Initial amplitudes refer to the central linear displacement contrast at z1100. Mass is cold mass integrated from the deposited density, not an inferred remnant mass.

| Seed | Radial cells | Physical cell (kpc) | Peak cold contrast | Cold mass inside 0.3215 kpc (solar masses) |
|---|---:|---:|---:|---:|
| .001 | 256 | .04505 | .06135 | 6,405 |
| .03 | 256 | .04505 | 6.12583 | 25,552 |
| .03 | 512 | .02252 | 6.13184 | 25,370 |
| .05 | 256 | .04505 | 2,658.98 | 436,666 |
| .05 | 512 | .02252 | 9,504.25 | 434,356 |
| .05, continued to z8 | 512 | .02753 | 76,604.02 | 2,776,826 |
| .05, half seed radius | 256 | .02252 | 95.6458 | 76,105 |

The reference radius spans 7.14 or 14.27 cells at z10. For the .03 seed, the peak changes by .10% and aperture mass by .71% on refinement; no cold shell crossing occurs. The aperture mass is about 430 times smaller than the inherited nominal 1.095e7 solar-mass scale. That nominal scale was a wavelength convention, not a predicted core mass.

For the .05 seed, the fixed-radius mass converges within .53%, while the peak increases by 3.57 times. The innermost cold shell moves from 3.51e-5 to 8.74e-6 kpc, far below either cell size; adjacent shell-order inversions rise from 5 to 10. This is consistent with unresolved radial focusing/caustic structure. It is not a resolved finite central core. By z8, the same-aperture mass is 6.39 times the z10 value. The sample provides no arrested remnant mass.

Halving seed radius reduces the fixed-aperture mass to .175 of the original. This is a different matter reservoir, not an ensemble mass function. Doubling the radius fails the declared chi>.1 guard at about z494.6, so that case has no z10 result and does not enter the table. No converged large-seed mass comparison is available.

## What drives collapse here

Replacing the baryonic fraction by cold matter while keeping the total background and seed amplitude fixed gives a peak cold contrast of 1.396 and no shell crossings at z10. This counterfactual changes both the source composition and its prepared field state; it does not isolate a single causal term. Nonetheless, the strong concentration is not robust to removal of the separately gravitating pressureless baryons. The physical treatment of gas pressure, shocks and thermal history is now a more consequential uncertainty than simply refining the reference aperture again.

The isolated Newtonian energy inside the reference aperture is negative in the strong runs, including when the radius floor varies from half to two cells. It is also negative in diffuse controls. It therefore cannot serve as a core certificate. In the fine strong z10 run it ranges from -2.64e-5 to -2.13e-5 in inherited energy units, whereas the positive field energy in the full box is 2.01e-4. Assigning all of that energy to the aperture gives no sufficient negative-energy test. This does not prove the object unbound; the full-action localized binding and radiation-flux calculation remains absent.

## Histories do not yet converge

The z2200 preparation is shot to a seed amplitude .01445776 so its cold sine displacement projection at z1100 matches .03 to 6.10e-5 fraction. Its fields and velocities are then evolved without resetting them. At z10 the cold peak is 7.35775, 20.1% above the fresh z1100 preparation, and the deposited aperture mass is 28,243 solar masses, 10.5% larger. Only one matter projection was matched, so this is residual preparation dependence, not a clean field-only perturbation experiment.

At z4400, the dust-scaled initial minimum has max |P|=.993193 and chi approximately 19.928, with a stationary residual 3.41e-12. It exceeds the conservative .985 polarization guard before evolution. This is a genuine large field excitation of this preparation, not a failed minimizer. It remains inside the formal |P|<1 potential domain; the guard failure is not a fundamental impossibility theorem. Small initial matter contrast does not guarantee a quiet initial field state.

## Numerical and observational status

The nonzero-seed accepted endpoint evolution runs have normalized expansion-work residuals below 9e-8. Halving the baseline timestep changes its peak by about 9e-8 fractionally and reduces the work error by four. The first initializer failed its residual gate and is retained but superseded. The force finite-difference check converges under step refinement. A strict absolute homogeneous field-force threshold remains failed at floating point roundoff; see AUDIT.md and the separate null-evolution control. No claim that every numerical gate passed is made.

Dwarf fits, rotation curves, cluster profiles/lensing and cosmological growth are **not certified preserved**. These calculations do not produce a three-dimensional population to place into those tests. The preceding reduced cosmological benchmark retained only 95.2–96.2% of reference growth at k=1/Mpc, below its stated 99% target; this local experiment neither fixes nor supersedes that issue. No observational refit was performed.

The strongest remaining discriminator is to derive the baryonic thermal/pressure history and the coupled field/metric initial state, then test nonradial collapse with physical refinement and a full-action binding/flux diagnostic. Continuing to label the present central peak a core, or fitting its aperture mass as a prediction, would skip the unresolved physics.
