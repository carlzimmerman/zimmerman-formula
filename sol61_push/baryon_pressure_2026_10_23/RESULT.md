# Baryonic pressure and thermal history: result

**Collapse survives the tested gas pressure and shock heating, but no resolved, stable, mass-selected bound core is certified.** This phase replaces pressureless baryons with a finite-volume ideal gas, follows local compression and Compton exchange, and tests a prescribed molecular-rich cooling branch. These are materially stronger tests than the earlier collisionless-baryon runs. They still do not derive a realistic primordial chemical/field history or establish dwarf, rotation-curve, cluster or cosmological compatibility.

## What the gas calculation changes

The gas has pressure, adiabatic compression, shock heating and local temperature evolution. Gamma=5/3, neutral mean molecular weight1.22 and residual electron fraction2e-4 are explicit assumptions. The cold particles and reciprocal fields retain the preceding action. The background remains imposed EdS and the geometry spherical. An initial barotropic approximation was stopped at gas crossing; it was not used to fake post-shock evolution.

A first hydrodynamic energy update failed by making a local temperature negative despite excellent global energy accounting. That failure was traced, retained and corrected. The accepted update uses the same gravitational acceleration in momentum and local energy, with its finite-grid global energy defect measured rather than concealed. See AUDIT.md.

## Collapse at z=10

The initial cold displacement amplitude is .05 at z=1100. Unless stated otherwise, baryons initially have the same displacement/velocity. All masses below are deposited cold mass inside a fixed physical 0.3215 kpc sphere, **not** measured remnant masses.

| Gas treatment / seed | Cells | Peak cold contrast | Cold aperture mass (solar masses) | Maximum gas temperature (K) |
|---|---:|---:|---:|---:|
| Compton + nonradiative ideal gas |256|839.9|354,781|609.4|
| Same, finer |512|1,980.3|358,473|629.2|
| Molecular-rich cooling sensitivity |512|1,983.8|358,473|562.5|
| Initially homogeneous baryons, same cold seed |256|9.07|37,607|21.7|
| Initially homogeneous baryons, matched initial total mode |256|22.09|64,422|50.2|
| Half seed radius, same amplitude |256|23.21|56,928|48.3|

For comparison, the previous pressureless512-cell case had a cold peak of9,504 and aperture mass434,356. Thus the gas model reduces that fixed-aperture mass by about17.5% and substantially softens the concentration. It does not eliminate collapse for the deliberately overdense equal-species seed.

The refined gas grid has0.02252 kpc cells, placing14.27 cells across the reference radius. Nevertheless the cold peak rises2.36-fold on refinement, and the innermost cold shell lies at about0.000106 kpc, far below one cell. Aperture mass agrees to1.04%, but a resolved aperture is not a resolved central structure. The baryonic aperture mass changes from320,201 to354,049 solar masses, about10.6%; gas convergence is weaker. Timestep halving changes the cold aperture mass by about1e-6 fractionally, so these differences are spatial, not temporal.

Half the initial radius means one-eighth the available background matter. Its aperture mass is only.159 of the full-radius case. The initially homogeneous-baryon control also changes the initial total matter perturbation, not just gas temperature; it is a history sensitivity, not a uniquely isolated pressure effect. A further control raises the cold seed to .05/f_c=.0593214 while leaving baryons initially homogeneous, matching the initial total matter displacement to first order. It still gives only64,422 solar masses and a cold peak22.09 at z=10. This does not match nonlinear density, the field state or a primordial spectrum, but shows that the contrast is not explained solely by the lower first-order total amplitude of the original smooth-baryon control. No common action-selected core mass emerges from this small sample. This is not a universal no-go statement.

## Binding and persistence gates

Atz10 the fine nonradiative candidate has negative isolated Newtonian energy, including gas internal energy and total physical rather than merely peculiar velocities: approximately-1.34e-5 in inherited units inside the reference aperture. But its full-box numerical work/heat defect is+1.03e-5, of comparable magnitude. The positive field energy in the box is1.91e-4; assigning it to a local object requires a field-tail, background and flux calculation that has not been done. A negative Newtonian number cannot certify binding in this theory.

Continued evolution gives an aperture mass 547,756 at z=9.527, already53% higher than at z=10, with work residual.00102. There is no observed plateau over this interval. Thez8 endpoint reaches2.57e6 solar masses but its relative work residual.01086 fails the declared.005 threshold . That endpoint is exploratory, not accepted evidence for a remnant or its mass. This phase has not established late stability.

## Molecular cooling and physical initial histories

Using the source-checked low-density H–H2 cooling coefficient, the finez10 central conditions give an instantaneous cooling/free-fall ratio of approximately874,8.74 or.874 for assumed molecular fractions10^-6,10^-4 or10^-3 per hydrogen atom. These are conditional timescale estimates, not calculated chemical abundances.

The molecular-rich evolution imposes the10^-3 fraction below z=100 and a CMB-floor approximation; it is deliberately a sensitivity case. Byz10 it lowers the maximum gas temperature from629 K to562 K while barely changing mass inside0.32 kpc. Cooling has only begun to affect the innermost gas over this interval. The continuation makes cooling important later: at z=9.527 its maximum temperature is823 K versus1817 K without molecular cooling, while both aperture masses are about547,756 solar masses and work residuals about.00104. It subsequently stops near z=8.920 at the cooling-fit density boundary, with work residual.0267 also failing the.005 criterion . That stopped endpoint cannot certify a stable cooled core. This does not establish that a real cloud acquires the prescribed molecular fraction. The prescribed fraction, onset and radiation treatment are documented in COOLING_CONTRACT.md.

The action still does not choose the primordial baryon density/velocity spectrum, field history or chemical state. A realistic initial-condition calculation must evolve the coupled baryon/photon/field system and recombination; neither equal species amplitudes nor zero baryon amplitude is presented as that prediction.

## Structural insight and cosmological growth

Gas pressure supplies a thermodynamic scale, but it does not automatically supply a selected **cold** core mass. In the frozen-background, linear quasistatic-polarization limit, the baryon/cold response matrix has determinant

 det M=-J_c q^2(J_b+c_s^2)/(1+q^2)<0.

Thus one instantaneous growing eigenmode remains for any finite positive gas pressure when the cold component is pressureless. Pressure slows this mode; it does not produce a universal hard mass cutoff. This restricted derivation is not a theorem about nonlinear collapse in the expanding full theory.

A separate linear calculation evolves gas temperature perturbations rather than assigning a fixed sound speed. The full dynamical-field campaign timed out and has no result. In the explicitly **quasistatic** replacement, growth at k=1/Mpc retains.955654 of the equal-seed dust reference without gas pressure and.955651 with the thermal pressure history. The new pressure term therefore does not repair the previous roughly4–5% growth deficit. The imposed no-reionization EdS thermal history toz0 is a diagnostic, not an observational cosmology. Lower growth for the initially homogeneous-baryon case also includes its lower initial total amplitude and must not be misrepresented as pure pressure suppression.

Dwarf fits, rotation curves, cluster distributions and lensing remain untested with an assembled population; preservation is not certified. The reference mass 1.095e7 solar masses remains a wavelength convention, not a formed-core prediction. No observed systems were refitted.

The remaining bottlenecks are specific: a positivity-preserving, sufficiently accurate gravity/gas energy scheme for localized binding through late infall; a converged central structure in nonradial geometry; and a derived thermal/chemical/field preparation. This work demonstrates gas-modified collapse under controlled assumptions, not the requested complete core-population mechanism.
