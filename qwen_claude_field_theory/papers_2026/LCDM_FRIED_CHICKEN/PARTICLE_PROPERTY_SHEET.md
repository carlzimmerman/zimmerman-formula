# Effective particle property sheet for the a0 law

Effective description in the rival's language. Not a claim that a particle exists, and the framework has none. Not deposited. Stands on the a0 law only; the cold sector stays retired (owner 11-01). Numbers from `scripts/recipe8.out`, `recipe9.out`, `recipe10.out`. Spherical, isotropic, order of magnitude. kappa = 1/2 FITTED; not theory closed.

| Property | Value | Status |
|---|---|---|
| Spin | boson, if it condenses | assumed |
| Mass | 9.2 to 13.7 eV | condensate gate, frozen, thresholds are my choice |
| Production | non-thermal; f theta_i about 5e11 GeV at 10 eV by misalignment | order of magnitude; thermal at 11.3 eV would be hot |
| Self-interaction | sigma/m 1.9 cm^2/g without Bose enhancement, 1e-3 to 6e-3 with it | one scatter in 13 Gyr, medians at the last measured radius |
| Field equation | div[ y/(a0 - y) grad phi ] = 4 pi G rho_b, y = abs(grad phi) | exact, 3.9e-13 on 3373 points; spherical check only |
| Force limit | y never exceeds a0 | follows from the law |
| Stiffness ratio | (2 a0 - y)/(a0 - y), median 2.56, up to 81 on SPARC | diverges as y approaches a0 |
| Energy scale | Lambda = 0.708 meV at alpha = 1, 0.316 of rho_DE^(1/4) = 2.241 meV | the tie is written in by hand |
| Baryon coupling | long-range; contact scattering would need 0.63 to 40 cm^2/g | fifth force needed |
| Phase space | collisionless route from NFW allowed in 139 of 171 | necessary only |
| Energy to form | median 0.516 of all supernova energy at 100 % coupling | above 1 in 28 galaxies |

**Prediction.** Inside the window, galaxies condense and clusters at 100 kpc do not, so the law should stop working in clusters at a scale set by m. That follows from how the bounds were chosen: the cluster bound was imposed because the law misses there. It needs a new data test before it counts.

**Open problems, each one fatal if left open**
1. **Double counting.** If the scalar supplies y, a halo with the required shape adds a second y. If the halo supplies it, the scalar does nothing. CFG122 gave standard Berezhiani-Khoury a scoped no-go against the target density, and nothing here solves that.
2. **Solar System.** y/a0 = 1.0000 at 1 AU and Saturn. PAPER58 records the unscreened law failing Cassini by 2.44 to 4.59 times. A local condensate does not switch this off, so a screening term is required.
3. **Lensing.** Law 276.1 on 60 KiDS points, fails; the scalar needs a lensing coupling that is not specified here.
4. **Dark energy.** Nothing derives Lambda from rho_DE. kappa stays fitted.
5. **Early universe.** A condensed species at 10 eV has not been run through the CMB or structure growth. HF1 and VW1 are warnings on nearby families, not this model.
6. **Causality.** The diverging stiffness ratio has not been checked against a time-dependent background.
7. **The window.** It is narrow and rests on my thresholds: the 100 kpc radius, point-mass clusters, the unit criterion for condensation. No sensitivity run yet.
