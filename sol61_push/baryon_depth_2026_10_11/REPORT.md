# The missing input for a fixed Bullet prediction

2026-10-11. Frozen criteria commit `6f44ad37c`. This identifies a measurement
ambiguity; it does not identify cold energy, derive its action, or exclude the
framework. The previous round-lensing result is unchanged.

## Result and exact reason

A projected gas map does not uniquely determine the baryonic mass enclosed in
a sphere about a specified galaxy. Consequently it does not uniquely determine
the framework's R6 spherical settled target at that centre.

Let the observer's depth coordinate be z and translate a gas component by d:

`rho_d(x,y,z) = rho_0(x,y,z-d)`.

For any integrable local emissivity function F, substitution u=z-d gives
`integral F(rho_d) dz = integral F(rho_0) du`.
Thus gas column density, optically thin X-ray emission measure, and thermal
SZ pressure are unchanged if the temperature/composition are uniform, or
translated along with that component. These statements use parallel sightlines
and the thin-lens approximation; they do not claim exact equality of distance
weights for cosmologically separated planes. The stars remain fixed.

In contrast, integration over the FIXED sphere x^2+y^2+z^2<r^2 is not invariant
under the translation. Calling the resulting mass Mb(r;d), the prescribed
round target is

`Mc(r;d) = [nu_mono(G Mb(r;d)/(r^2 a0))-1] Mb(r;d)`.

We hold the galaxy centre and host assignment fixed to exhibit this ambiguity.
Changing that assignment introduces another unresolved input; the example does
not establish how a self-consistent merger should assign its gas to hosts.
Nor does it claim the nonspherical baryonic force itself is spherical.

## Bounded numerical illustration

One gas Gaussian has mass 1e14 solar masses and width 150 kpc; one fixed stellar
Plummer component has mass 1e12 solar masses and scale 30 kpc. Gas depths are
0,150,450,900 kpc. These deliberately specified numbers are NOT Bullet data or
allowed observational bounds. No mass fit or additional theory constant is
introduced. We use the actual repaired kernel-defining statements from the
PM source, extracted by AST without importing its transfer/growth machinery.
Source hashes and selected statement names are recorded.

| Radius (kpc) | Mc(depth=900)/Mc(depth=0), canonical | Same ratio, alt |
|---:|---:|---:|
| 30 | 0.888243 | 0.878118 |
| 100 | 0.501127 | 0.481788 |
| 250 | 0.228975 | 0.216581 |
| 500 | 0.157555 | 0.152128 |

Footings are the literal owner values 9.36e-11 and 1.13e-10 m/s^2, separately.
The simulation files use slightly more precise values; this example does not
silently substitute them. Supply truncation, settling evolution and gas motion
are not computed. These are required cold-mass targets, not realized halos.

The run passed **88/88 checks**: analytic enclosed mass against independent
radial quadrature, projected density and emission integrals against independent
line-of-sight quadrature, positive density, monotonic enclosed mass, central
and total-mass limits, footing-independent baryons, and normalization/ignored-
depth MUTATE controls. The verified range is exactly the frozen depths/radii;
the integral substitution supplies the general projection argument.

For a displaced spherical Gaussian with width s, the enclosed fraction used is

`F(r,d) = (erf((r+d)/(sqrt(2)s))+erf((r-d)/(sqrt(2)s)))/2`
`         + s/(sqrt(2pi)d) [exp(-(r+d)^2/(2s^2))-exp(-(r-d)^2/(2s^2))]`.

The d=0 limit is `erf(r/(sqrt(2)s))-sqrt(2/pi)(r/s)exp(-r^2/(2s^2))`.
The independent integrand is the angular-averaged radial mass probability,
`r/(sqrt(2pi)s d) [exp(-(r-d)^2/(2s^2))-exp(-(r+d)^2/(2s^2))]`.
Its integral from zero to r gives F. Proof/formula review was performed by the
same author; there was no independent agent audit or novelty claim.

## Source check: what the released gas products supply

[Rihtarsic et al., arXiv:2601.22245v2, section 4.2](https://arxiv.org/html/2601.22245v2)
describes a gas model inferred from Chandra imaging and spectra, then used as
a fixed projected map. It is an observation-based reconstruction with geometry
assumptions, not a direct measurement of three-dimensional host-enclosed mass.
The public member catalogue inspected in the preceding lane supplies positions,
F277W magnitudes and redshifts; it is not a stellar-mass catalogue.

[Halverson et al., arXiv:0807.4208, sections 5.4–5.6](https://www.osti.gov/servlets/purl/979015)
compares SZ and X-ray data. Its displayed SZ map has 85-arcsecond resolution and
does not resolve the subcluster. Its gas-mass inference adopts temperature and
spheroidal geometry assumptions. Its quoted mass-weighted temperature uses an
X-ray-inferred electron column, so importing both as independent mass constraints
would require checking their covariance. We do not import its cosmology-derived
gas masses into a framework verdict. This is an older source, not a new release.

Search scope on 2026-10-11: public web queries for Bullet joint SZ/X-ray depth,
gas maps, and APEX-SZ release products; read the above primary full texts.
This was a targeted input-dependency audit, not an exhaustive survey of available
SZ observations. No claim that finer data do not exist follows. The exact
translation argument is elementary projection mathematics, with no novelty claim.

## Consequence for the next theory test

Do not subtract a supposedly unique settled prediction built from a projected
gas map and an unstated depth. First declare measured stellar masses, the 3D
gas-component geometry and its uncertainties, and a derived host-assignment
rule for the merger. Forward-model the same baryon parameters into X-ray/SZ
observables and into the framework's enclosed-mass target. Propagate this allowed
geometry into the raw-image residual calculation, separately for both footings.
Lensing can itself constrain geometry jointly; the example does not make a joint
inference impossible. Geometry is an observational nuisance, not a new force
coefficient, but it cannot be chosen solely to make the theory pass.

Only then ask whether the shared unsettled mass budget supplies the residual
deflection. The circular/positive-3D lensing bounds already built provide that
necessary-condition test. A successful fit still leaves action, kinetics,
growth and all other success conditions open. CFG629's placeholder reservoir
is a diagnostic, not a solution to these missing inputs. No Claude files or
sealed predictions were edited; kappa remains fitted.
