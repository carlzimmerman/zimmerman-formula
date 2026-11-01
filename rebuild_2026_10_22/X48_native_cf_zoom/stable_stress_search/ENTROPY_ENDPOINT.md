# Entropy rearrangement and stable core endpoints

The cold radial pilot produces positive parcel entropies, but not a settled
entropy-ordered remnant. This continuation asks a narrower question: can the
measured entropy and available energy support a finite, radially stable core
without requiring a material parcel to lose entropy? It constructs endpoints;
it does not implement a mixing transport equation or establish reachability.

## Exact parcel construction

Use the equal-mass K values of the measured 64-shell t=8 result, with its
initial discrete energy and conserved mass. The input has SHA256
`26e7c8fa81642b578fbc3de7643b2d5cd5f943f4884a5faf80f6f9fad4f6e117`.
Every K is positive; its minimum is approximately 0.00681127 in the declared
normalization `G=rho_q=K_*=1`, `a0=sqrt(8pi)`.

Permute the complete equal-mass parcels into nondecreasing K order, preserving
their identities and entropy histogram. On each exact mass interval retain
its constant K. Multiply all coefficients by a single alpha>=1 only after
checking the energy budget. For the entropy coordinate

\[
 \sigma_i=(K_i/K_*)^{1/3},\qquad
 \sigma_i\longmapsto\alpha^{1/3}\sigma_i\ge\sigma_i,
\]

no original parcel needs to lose entropy. Permutation preserves the original
histogram; subsequent heating scales it, rather than preserving it unchanged.

Hydrostatics can be solved in enclosed cold mass m, with u=r^3:

\[
 \frac{du}{dm}=\frac{3}{4\pi\rho(P,K_i)},\qquad
 \frac{dP}{dm}=-\frac{G[m+M_b(r)]}{4\pi u^{4/3}}.
\]

Integrate separately on every parcel interval, keeping radius and pressure
continuous at contacts. A regular center supplies the startup limit; shoot
central pressure so the first pressure-free surface encloses the target mass.
The occupied EOS inverse has rho>=rho_q. There is vacuum beyond that surface.
Integrate energies using

\[
 \frac{dU}{dm}=K_iW(\rho),\qquad
 \frac{dV}{dm}=-\frac{Gm}{r},\qquad
 \frac{dE_b}{dm}=\Phi_b(r).
\]

First compute the sorted alpha=1 equilibrium. Only when its energy is below
the source energy is positive heating admissible. Search alpha>=1 for the
available energy, and check the actual final mass and energy residuals. On a
smooth stationary fixed-mass branch, the envelope identity

\[
 \frac{dE_{\rm eq}}{d\alpha}=\int K_{\rm base}(m)W(\rho)\,dm>0
\]

explains local monotonicity. Here W includes its latent constant 3rho_q/2.
Contact terms cancel through pressure and displacement continuity, and outer
boundary work vanishes at P=0. This identity is not a global branch-existence
or relaxation theorem.

The source energy is that of the N64 discretization. The continuum uniform
initial sphere has energy approximately -0.638338673, compared with the
recorded discrete value -0.638191859. Their relative difference is 2.30e-4;
matching the latter more accurately does not remove that spatial limitation.

## Exact parcel result

Current finite evidence is
[`exact_parcel_endpoint_snapshot/exact_refined/manifest.json`](exact_parcel_endpoint_snapshot/exact_refined/manifest.json),
with its matching result and source snapshot. The exact construction gives
sorted energy approximately -0.946074631 below the target -0.638191859.
Heating by alpha approximately 1.41932 matches that target. The entropy mass
integral is exactly preserved by sorting, approximately 0.669961624, then
increases to 0.752910841. The minimum parcelwise K ratio is alpha itself.

The refined endpoint has central density approximately 48.282rho_q and outer
radius 0.501100 in the pilot units. Its reported half-density radius is about
0.0453, in a profile with discrete contacts; it is not a converged physical
core-size prediction. The internal shooting residuals are 8.8e-12 in mass and
4.3e-10 in energy. Independent radial/enthalpy integration supports the stated
2e-6 numerical acceptance scale; those smaller shooting residuals are not
overall numerical error bounds.

At unchanged K(m), alpha and cold mass, smooth Plummer loading `Mb=0.3Mc`,
`b=0.1R_initial` gives:

| Cold mass shell | Retained radius with stress | Circular reference |
|---|---:|---:|
| 5% | 0.666561 | 0.440481 |
| 50% | 0.816560 | 0.644321 |

Central density becomes approximately 199.821rho_q and sampled half-density
radius approximately 0.0289. The external potential supplies work during
assembly; its loaded total energy is not required to equal the isolated
initial energy. No alpha refit or new entropy generation is used in this
quasistatic comparison.

All 63 contacts have outward nondecreasing K and nonincreasing density at
common pressure. The finite source has positive minimum K, but the formation
runs have not established a positive lower bound uniform in resolution. That
missing limit is relevant to whether a true continuum central core survives.

## Stability with material contacts

For an adiabatic radial mode, each parcel has Delta K=0 and
`A=rho P_rho>=2P`. At a contact require continuous displacement xi, equilibrium
pressure P, and Lagrangian traction Delta P=-AD, where `D=r eta'+3eta` and
`eta=xi/r`. There is no surface mass or surface tension.

The shellwise radial identity in `DERIVATION.md` has boundary term
`B=r^3 eta(4P eta-AD)`. Every interior difference `B(a-)-B(a+)` cancels.
Regularity and physical outer free traction remove the remaining boundaries.
The same positive radial gap follows:

\[
 \omega^2\ge8\pi G\rho_q/3>0.
\]

The appropriate moving gravitational interface condition is
`[delta g]+xi[g']=0`; Eulerian delta g need not be continuous at the
unperturbed density jump.

Within each constant-K parcel, bulk buoyancy is neutral. At continuous
positive P, the EOS has `P=K f(rho)` with f strictly increasing. An outward
increase in K therefore gives a downward density jump outward. The local
interface buoyancy term has restoring sign
`g(rho_inner-rho_outer)|xi_normal|^2` per area. This does not by itself prove
stability of every nonradial global mode. Reporting a sampled bulk N^2=0 would
not substitute for this contact analysis.

## Historical continuous proxy and its limitation

The preserved first proxy is in `entropy_endpoint_snapshot/`. It interpolates
K linearly between parcel centers. Its sorted equilibrium has energy below
the source; alpha approximately 1.41827 produces a finite energy-matched
sphere, with mass and energy errors of order 1e-7. It also resists the defined
smooth Plummer load more strongly than the circular-shell reference.

Concavity of K^(1/3) makes the proxy's integrated entropy slightly larger than
the discrete entropy. This does not imply parcelwise entropy increase:
independent review found an interval where the heated proxy coefficient is
only 0.94742 times that of the corresponding original constant parcel.
Therefore the proxy is evidence about a continuous aggregate-entropy
construction, not a certificate for the material source D_tK>=0 along every
original parcel. Exact mass intervals repair this specific missing implication.

The historical proxy contract calls its integrator DOP853; the actual code
uses the default solve_ivp method RK45. The record is preserved and this
correction is explicit. The root-level proxy run `endpoint_verification/`
corrects that method label but records an internal cap of 22 seconds while
its command requests 30; use the actual argv for that historical execution.
Neither proxy record is the final exact-parcel evidence.

## Remaining physical step

Even a successful exact-parcel endpoint is a necessary-consistency result.
Adiabatic rearrangement and positive entropy production must be generated by
an actual transport law or three-dimensional relaxation. The current bulk
source and spherical pilot do not establish that process. A diffuse halo
envelope, collisionless exterior, observed forest histories, and a rotating
baryonic disc remain separate model tests.
