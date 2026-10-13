# Collisionless motion retains the stipulated mean-field pressure response

Status: linear expanding Vlasov-Hermite calculation for a single Maxwellian
component with the previously stipulated mean-field coefficient. It tests
whether replacing local fluid equilibrium by collisionless motion removes
the growth suppression. It does not derive that coefficient from the full
nonlinear two-field quantum theory.

## Explicit kinetic approximation

Retain the homogeneous background and initial scale factor a_i=0.001 of
PORTAL_COSMOLOGY.md. Let the one-dimensional background velocity dispersion
redshift as sigma(a)=sigma_0/a, with

    sigma_0=u c/[sqrt(3)(1+z_production)]=0.1730851 m/s.

This assigns a Maxwellian the variance of isotropic near-threshold daughters
redshifted from z_production=1e6. It is an imposed diagnostic distribution,
not the measured produced spectrum. Source/daughter reactions, source mass
differences, later velocity injection, radiation perturbations and baryonic
perturbations remain absent.

Use the frozen-intensity partial response C(a) derived from the saved
production sample as a local mean-field coefficient. The force potential
for a density Fourier perturbation delta is stipulated to be

    delta Phi_total=[C(a)-4 pi G rho_m a^2/k^2] delta.

The first term is the mean-field chemical-potential response per mass;
the second is Newtonian gravity. Assuming this force is a closure choice.
The calculation tests its collisionless consequence, not its microscopic
validity or the evolution of intensity correlations.

## Velocity-resolved hierarchy

Write w=v/sigma(a), which is constant along unforced expanding trajectories,
and expand the distribution perturbation in normalized probabilists'
Hermite polynomials with Gaussian weight exp(-w^2/2). If the coefficients
are h_n=(-i)^n z_n, the real hierarchy with prime=d/d ln a is

    z_n'=b[sqrt(n) z_(n-1)-sqrt(n+1) z_(n+1)]
               +F z_0 delta_(n,1),
    b=k sigma/(aH),
    F=k[C-4 pi G rho_m a^2/k^2]/(aH sigma).

The density perturbation is z_0. This follows from multiplication by w in
the streaming term and differentiation of the Gaussian in the force term.
The truncation sets z_(N+1)=0. Initial z_0=1 and z_1=-1/b(a_i) impose the
same density and density derivative as the earlier fluid calculation;
all higher moments start at zero. These are infinitesimal perturbation
amplitudes times a growth normalization, not order-one physical departures
from a nonnegative distribution.

As sigma tends to zero, bF retains the finite mean-field/gravity term,
while streaming stress corrections vanish. Eliminating z_1 then gives the
earlier cold fluid equation. Thus collective restoring forces do not
require rapid collisions or local thermal equilibrium in this model.

## Result and controls

Normalized final density amplitudes relative to the same pressureless
control are:

| k, Mpc^-1 | Fluid calculation | Collisionless kinetic calculation |
|---|---:|---:|
| 0.1 | 0.99739233 | 0.99739233 |
| 0.3 | 0.97669039 | 0.97669039 |
| 1 | 0.76033053 | 0.76033051 |
| 3 | -0.09881929 | -0.09881928 |
| 10 | 0.02473751 | 0.02473748 |

The negative entries are Fourier phase reversals. They are not negative
physical densities or observed power-spectrum ratios. The small kinetic
correction is consistent with a comoving free-streaming dispersion of only
0.0002882155 Mpc over the interval, much less than the pressure-wave travel
distance in the earlier calculation.

portal_vlasov.py compares Hermite truncations N=4 and N=8, refines ODE
tolerances, and decreases sigma by another factor of ten to check the cold
limit. An independent force-free control uses a 100-times larger dispersion
and N=12: an initially pure density perturbation follows the analytic
Gaussian phase-mixing result exp[-(k ell_free)^2/2]. The enlarged dispersion
is used only for this code control. All 16 checks pass and the manifest
validates provenance. No full eigenmode or kinetic convergence theorem is
claimed; the numerical signs and scale of suppression are robust within
the sampled hierarchy checks. The derivation is self-reviewed.

## What the test settles

For this mean-field model, lack of collisions does not remove the
restoring force or its effect on cosmological growth. The fluid result was
not relying solely on an assumption of rapid thermal equilibration.
This narrows the unresolved issue to the constitutive force itself and its
coupling to the evolving state, rather than replacing the fluid with free
particles while keeping an interaction energy in the action.

The underlying nonlinear intensity response remains stipulated. Actual
source/daughter distributions, resonant reactions, phase correlations,
and stress transport could modify it, and have not been solved here.
This is neither a cosmological observational exclusion nor a derived
halo law. The original cold-energy construction remains incomplete.
