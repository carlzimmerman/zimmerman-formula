# Collision response of an energy current

Status: the resonant collision operator damps a linear angular energy-current
perturbation in the evolving homogeneous bath. Four finite grids agree on
substantial but incomplete damping over the tested interval. This supplies
an angular transport response; it is not a conductivity or a spatial halo
heat-flow calculation.

## Angular perturbation and reaction geometry

Use the isotropic nonrelativistic energy grids and physical normalization
from COUPLED_KINETICS.md. Add small dipoles around an arbitrary z axis:

    f(e,n)=A [a(e)+epsilon a1(e) n_z],
    F(ec,N)=A [b(ec)+epsilon b1(ec) N_z].

This is a derivative at epsilon=0, not an assertion that a finite perturbation
of arbitrary size is positive. The isotropic a,b evolve with source/daughter
conversion; they are not held at a thermal equilibrium or fixed bath.

Write p_i=sqrt(2e_i), P=2sqrt(ec-1) in units m u. On the reaction triangle,

    c12 = n1 dot n2 = (e1+e2-2)/(p1 p2),
    c1 = n1 dot N = (P^2+p1^2-p2^2)/(2 P p1),
    c2 = n2 dot N = (P^2+p2^2-p1^2)/(2 P p2).

For d1=a2-b, d2=a1-b, d3=a1+a2+1/A, the three linearized angular fluxes
are, with a1dip,a2dip referring to dipole amplitudes rather than backgrounds,

    daughter 1: d1 a1dip + d2 a2dip c12 - d3 b1 c1,
    daughter 2: d1 a1dip c12 + d2 a2dip - d3 b1 c2,
    source:     d1 a1dip c1 + d2 a2dip c2 - d3 b1.

The daughter terms enter with negative sign, the source term with positive
sign, and all use the same pair weights as the isotropic collision operator.
These factors follow by averaging each partner's dipole over the allowed
azimuth around the particle whose equation is being evaluated. They are
not an assumed isotropization time.

The identities P c1=p1+p2 c12 and p1 c1+p2 c2=P ensure exact conservation
of the discrete leading-order momentum moment. An additional load-bearing
check is the equilibrium drift mode: for classical equilibrium backgrounds
a=1/(e-mu), b=1/(ec-2mu), the dipoles a1=a^2 p and b1=b^2 P have zero
linearized collision term. This tests that the operator does not spuriously
damp a common bulk velocity.

## A current without leading-order bulk flow

Start with the same daughter Gaussian spectrum and zero sources. Choose

    a1(e)=a(e) p(e) (e-C),
    C = sum wp p^2 a e / sum wp p^2 a,
    b1=0.

Then the leading nonrelativistic momentum moment

    Pz proportional to sum wp p a1 + sum wc P b1

is zero. The nonrelativistic excess-energy current is

    Jex proportional to sum wp e p a1 + sum wc ec (P/2) b1.

Both expressions omit their common angular factor epsilon/3 and dimensional
normalizations; current ratios do not depend on these factors. The velocity
factors p and P/2 are those of the retained NR dispersion. The leading
rest-energy current is proportional to the conserved-charge mass current,
which vanishes in this frame. Jex therefore probes heat-like energy motion
relative to that flow, not the damping of a bulk drift. Statements about
momentum here are at the retained NR order, not an exact relativistic
zero-momentum frame construction.

## Finite response

At density 1e-21 kg/m^3, initial one-dimensional dispersion 200 km/s and
the previously chosen microscopic parameters, the finest emax=8 grid gives:

| Time | Remaining current Jex/Jex(0) |
|---|---:|
| 0 | 1 |
| 0.278 Gyr | 0.86300 |
| 1.392 Gyr | 0.68032 |
| 2.784 Gyr | 0.62017 |
| 5.569 Gyr | 0.57051 |

The current relaxes substantially but remains more than half its initial
value at the endpoint. No e-folding time has been measured, and the response
is not well represented by substituting the earlier 0.856 Gyr rest-source
mode time into an exponential heat-relaxation model. The bath is changing
its species composition and energy distribution throughout this test.

At 5.569 Gyr, current ratios for 64,128,256 shells with emax=8 are 0.572410,
0.570213,0.570511. The last refinement changes the ratio by 0.000298.
Doubling emax from 8 to 16 at fixed de=0.0625 changes it by 0.0000477.
These are finite convergence diagnostics, not certified continuum errors.

## Verification and implications

`kinetic_heat_current.py` evolves the isotropic bath and angular dipoles
together. All 28 checks pass. Relative charge and energy errors are below
3.2e-15; the absolute momentum residual normalized by the initial current is
below 2.1e-15. Reaction-triangle projection identities and the equilibrium
drift zero mode pass independently of the trajectory. Its manifest is
`kinetic_heat_current_run/manifest.json` and validates. This is self-reviewed
finite evidence within the assumed incoherent kinetic closure.

The same interaction used by the production model can change an angular
energy current without violating the conserved moments. That is a more
specific transport ingredient than population exchange alone. However,
this calculation has no spatial gradients or streaming. It imposes a
current and studies collision response; it does not predict which direction
a halo would send energy or how much heat a core exports.

A local diffusion law would require an appropriate near-equilibrium and
scale-separation limit. Neither is established by the evolving bath here.
Spatial transport with gravitational orbits, boundaries, condensates and
closure checks is still needed. No target halo profile, vacuum coupling,
baryonic mass scaling or acceleration coefficient has been derived.
