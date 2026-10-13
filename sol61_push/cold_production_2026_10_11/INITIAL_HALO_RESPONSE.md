# The reaction starts a self-gravitating contraction

Status: the initial time derivatives of the coupled nonrelativistic
Boltzmann-Poisson moments show inward mass flow and a deepening potential
for the chosen Plummer initial state. This goes beyond source-only tracers,
but is a short-time expansion, not a finite-time halo evolution or proof of
an eventual equilibrium.

## Retained model and energy accounting

Use both source and daughter kinetic equations, their resonant collision
operator, and Poisson gravity sourced by the leading conserved mass density

    rho=m(nphi+2 nchi).

The source inertial mass is 2m at retained NR order, while its reaction gap
is DeltaE=m u^2 in natural units, or m_mass (u c)^2 in SI. Relativistic
mass-weighting corrections, contact mean-field stress and coherent field
correlations are omitted. The earlier contact-pressure comparison makes
that stress tiny for this example, but it is not exactly zero in the full
action. These are statements about the declared kinetic approximation.

Initially the daughters form the isotropic Plummer collisionless equilibrium
and no sources are occupied. Let R(r)>0 be source number production per
volume per time. For each reaction, daughter kinetic energies sum to
m u^2 ec and source kinetic energy is m u^2(ec-1). Hence

    dK/dt |_collision = -DeltaE R,
    dP/dt |_collision = -(2/3) DeltaE R = -S(r).

The pressure relation follows from isotropy and P=2K/3 for the kinetic
stress of either nonrelativistic species. Charge-weighted mass and total
momentum are conserved in the collision. Lost kinetic energy becomes the
source's extra rest energy; there is no radiated energy sink. The subsequent
gravitational potential energy must also be included in total energy.

In terms of the previous initial local charge-conversion rate cR=2R/nphi,

    S(r)=rho(r) (u c)^2 cR(r)/3.

This expression fixes the pressure change from the same microscopic rate,
instead of assigning a separate cooling function.

## Initial moment response

Let j be total mass current and Pi the kinetic stress tensor. The coupled
moments obey

    rho_dot + div j = 0,
    j_dot + div Pi = -rho grad Phi,
    laplacian Phi = 4 pi G rho.

At the initial equilibrium, j=0 and div Pi=-rho grad Phi, so
rho_dot=j_dot=rho_double_dot=0. The collisionless part of the initial
phase-space evolution is zero, while collisions give Pi_dot=-S I.
With the potential fixed to zero at infinity, Phi_dot=Phi_double_dot=0.
Differentiating the momentum and continuity equations now gives

    j_double_dot(0)=grad S,
    rho_triple_dot(0)=-laplacian S,
    Phi_triple_dot(0)=-4 pi G S.

The last result solves the differentiated Poisson equation with the same
boundary condition. It is the first self-consistent potential response,
not a prescribed force change. For a smooth solution, therefore,

    j_r(r,t) = S'(r) t^2/2 + o(t^2),
    M(<r,t)-M(<r,0) = -(2 pi/3) r^2 S'(r) t^3 + o(t^3),
    Phi(r,t)-Phi(r,0) = -(2 pi G/3) S(r) t^3 + o(t^3).

The enclosed-mass and potential formulas give the same force change under
G delta M/r^2=partial_r delta Phi. They involve finite enclosed radii. No
finite global second moment of the Plummer density is assumed; that model's
unweighted total radius-squared moment diverges.

## Why the response points inward

For the Plummer occupation, f(e,r)=C[esc(r)-e]_+^(7/2) with C independent
of radius. The resonance domain in (e1,e2) is independent of esc. Thus,
where production is nonzero,

    partial R/partial esc = (7/2) K0 integral f1 f2
                            [1/(esc-e1)+1/(esc-e2)] de1 de2 > 0.

Moving escape boundaries give no extra contribution because f vanishes
there. Since esc'(r)<0 for r>0, R'(r)<0 and S'(r)<0 throughout the active
region. The leading mass current is therefore inward, enclosed mass rises
at any fixed interior radius, and the potential becomes more negative.
Near the center laplacian S<0, so the initial central density change is
positive. Total mass remains conserved: an inner density increase is
balanced by depletion farther out.

This sign statement follows from the moment equations and positive integral;
it is not inferred just from a few radial samples. It applies to the
specified initial distribution and model, not arbitrary halos.

## Evaluated coefficients and checks

For the same rho0=1e-21 kg/m^3, sigma0=200 km/s and microscopic coupling,
write delta M/M=C_M(r)[t/(1 Myr)]^3+o(t^3) with the time units understood.
Representative coefficients are:

| Radius | C_M |
|---|---:|
| 3.00 kpc | 2.106e-7 |
| 7.51 kpc | 1.656e-7 |
| 15.01 kpc | 7.583e-8 |
| 30.03 kpc | 7.085e-9 |
| 60.05 kpc | 3.267e-11 |

The analogous central density coefficient is 2.207e-7 per Myr cubed.
These are initial Taylor coefficients, **not finite-time growth predictions**.
No remainder bound or valid extrapolation time has been computed.

`initial_halo_response.py` evaluates the pressure-loss integral and its
analytic gradient. Independent centered differences check the gradient,
and a central second-difference check verifies the density coefficient.
The initial Jeans force balance, exact fractional collision energy/stress
moments and quadrature refinement are also checked. All 38 checks pass;
`initial_halo_response_run/manifest.json` validates the inputs and result.
The analytical reduction and interpretation are self-reviewed.

## What this advances

The proposed interaction does more than populate a compact tracer component:
it starts a conservative, self-gravitating inward response of the combined
matter in this chosen initial halo. The mechanism is pressure reduction by
conversion into heavier sources, followed by orbital and gravitational
response. It does not require an imposed target temperature or energy loss
to an unspecified environment.

Later inverse reactions, daughter heating, transport and changing gravity
can alter or halt this trend. No stable core, collapse endpoint, universal
profile, baryonic scaling or vacuum-density acceleration law follows from
the sign of the initial derivatives. Those remain requirements of the
original cold-energy goal, rather than consequences established here.
