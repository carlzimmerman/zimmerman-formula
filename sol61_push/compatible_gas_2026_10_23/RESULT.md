# Energy-consistent gas and density-dependent molecular cooling

**Outcome: substantially improved energy accounting, but no resolved, stable bound core or selected remnant mass.** Three spatial resolutions point to an unresolved cold cusp and a gas concentration whose size follows the field-grid scale. The outer enclosed mass is much more converged. Cooling saturation supplies a physical thermal scale; it does not arrest the coupled central collapse in these tests. This is evidence against the tested spherical realization as a demonstrated mass-selection mechanism, not a no-go theorem for the action.

## What changed and what passed

Replaced Eulerian baryons with conserved-mass moving gas shells. Their gravity force is derived from the same deposited gravitational energy used by the cold component. Pressure and artificial-viscosity forces use the same geometric work in the internal-energy equation. RK4 evolves thermal energy directly; no temperature floor or global energy redistribution is applied. The expansion-work budget includes the bulk-viscosity term. Replaced the old nH=100/cm3 cooling cutoff with a continuous low-density-to-LTE transition. Molecular abundance remains prescribed; chemistry is not derived.

Finite-difference checks verify the semidiscrete energy identity (~5e-11 relative initially; below3e-9 at the tested cooled z8 and z6 states with an appropriate difference step). Gas force-gradient errors decrease with the difference step and reach8.1e-7 or better. A closed compressive gas exercise preserves positive thermal energy, entropy and energy. A standard strong-shock convergence suite is still outstanding. Homogeneous expansion and signed cold-orbit parity checks pass.

Before central cold passage, the n128 absolute accumulated energy defect is about2.1e-9; the previous gas solver had defects around1e-5 near that stage. At z8, endpoint defects for n128/256/512 are +2.67e-7, -1.33e-7, -4.31e-7. The maximum defect over each history is retained separately. At n128, halving the timestep reduces the maximum defect from4.42e-7 to6.90e-8 and changes aperture masses by only a few parts per million. Improvement in this budget does not certify binding: a full-action localized escape/surface-flux calculation is still absent.

## Decisive spatial test

All three rows reach z8 with the same initial .05 sine seed, seed size and prescribed fH2=.001. Moving gas shells can be far narrower than the fixed field grid. The gas radius below encloses a fixed53361 Msun (0.1% of initial gas mass); it is **not an identified remnant radius**. Radii use volume-consistent interpolation in postprocessing.

| Radial cells | Field cell [pc] | Peak nH [cm^-3] | Fixed-gas-mass radius [pc] | Central cold contrast | Cold mass in first field cell [Msun] |
|---:|---:|---:|---:|---:|---:|
|128|110.1|163|14.03|7182|980401|
|256|55.06|2691|5.879|28618|488262|
|512|27.53|24825|3.500|123577|263537|

The fixed gas-mass radius remains only0.11–0.13 field cells at every resolution. Peak cold density increases by factors3.98 and4.32 on doubling resolution, while central cell mass falls by factors0.498 and0.540. This is consistent with an unresolved approximately r^-2 cusp; it does not prove a unique continuum cusp law or exclude a much smaller core. It does rule out treating these central grid peaks as converged finite cores.

By contrast, total mass inside0.321485kpc is4.738,4.812,4.821 million Msun. The last refinement changes this aperture mass by0.185%. **A converged aperture mass is not a converged core.** The densest gas cell has T~74,79,327K across these resolutions; even its thermal state is not converged. The n512 peak is about27 times its local cooling critical density, so merely crossing the LTE transition has not produced resolution-independent arrest.

The n256 continuation reaches z6. Aperture mass grows from4.812 to11.384 million Msun. Its field cell also expands from55 to71pc. This is ongoing accretion, not evidence for a detached remnant with a mass plateau. It cannot alone rule out a smaller quasi-steady centre, but that centre is unresolved here. No survival-over-dynamical-times binding certificate is obtained.

## Controls and the physical insight

At n128 and z8, changing prescribed fH2 from0 to1e-4 to1e-3 changes maximum nH from3.08 to46.44 to162.97/cm3. The no-molecule control reaches temperatures where omitted atomic cooling becomes relevant and is a numerical control, not a complete thermal model. The smaller-seed run (half radius, one-eighth available mass) reaches only0.268/cm3; initially smooth baryons reach0.0111/cm3. These controls change multiple parts of the initial state and are not matched primordial transfer-function realizations. They show dependence, not a predicted cosmological occupation fraction.

The cooling law gives a sharper physical distinction. At fixed temperature and molecular abundance, ignoring CMB subtraction, tcool/tff is proportional to nH^(-1/2)+nH^(1/2)/ncrit. It is minimized at ncrit. Thus LTE saturation provides a **thermal bottleneck**. For T200K the adopted rate gives ncrit758/cm3, a gas-only isothermal Jeans estimate3276Msun, and minimum tcool/tff=.902 for fH2=.001 but9.02 for fH2=.0001. These are conditional analytic estimates, not simulated or action-selected core masses. Temperature, chemistry, external cold gravity and assembly still determine which scale is encountered. See DERIVATION.md and the primary-rate sources in SOURCES.md.

## Dwarfs, rotation curves, clusters and growth

No preservation certificate is justified. There is no converged remnant mass/profile or abundance to insert into dwarf, rotation-curve or cluster fits, and no metric lensing completion has been tested. Keeping action parameters fixed does not establish that newly condensed matter preserves old fits.

Within the adopted CMB-floor prescription, homogeneous gas after z100 is below Tcmb, so the molecular loss and its linearization vanish near the background. Artificial viscosity is quadratic in perturbations. These additions therefore leave the inherited linear calculation unchanged in that restricted setting. Its quasistatic k1/Mpc retained growth is about.95565: the existing roughly4.4% deficit remains unresolved. This phase does not claim a new full-field linear integration or observational pass.

The next decisive requirement is a central solution whose physical radius and mass stop following the cold/field resolution, with a full-action binding and escape test. This requires resolving collisionless phase space and nonradial support/transport, alongside chemical abundance evolution and justified primordial initial histories. More accurate gas cooling alone has not supplied that missing support in the present realization.

## Evidence

Exact run inputs, argv, bounds and hashes are in each manifest. `analysis_v2/result.json` contains endpoint comparisons and late energy checks; `analysis_v2/profiles.png` shows spatial profiles and accretion. AUDIT.md retains the initial typo, cancellation-sensitive failed check, central-orbit guard stops and pre-execution analysis-path rejection. Numerical checks are self-reviewed, not independently replicated. No full theory success is claimed.
