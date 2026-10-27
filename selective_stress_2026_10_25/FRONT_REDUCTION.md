# Next executable reduction: independent infall, front and radiation

Status: an explicit conditional mechanical reduction, **not yet integrated**.
Its purpose is to replace the stipulated cosine potential of the successful
outlet tests by the actual existing energy. No formation conclusion is drawn.
SS-28 supplies a potential-landscape discriminator for this route.

## Material continuity and conversion source

Use dimensionless radial coordinates and the convention dV=r^2 dr. R in the
kinetic formulas means R_physical/rM; SS-28 tabulates its potential in kpc,
so that conversion is required when differentiating it. Let
rho(lambda,r)=(1-lambda)rho0(r)+lambda rho1(r), where rho0,rho1 are the
independently equilibrated all-F and formed endpoints. This is a deliberately
restricted density manifold. Define

    Q(r)=integral_0^r [rho1-rho0] s^2 ds,
    v_lambda=-Q/(r^2 rho), v=v_lambda lambdadot.

Then continuity holds exactly and total mass is unchanged. Both endpoint
densities are positive; this interpolation does not create an empty cell by
construction. That restriction is not evidence that unconstrained dynamics
keeps the transition filled.

Let theta(r,R)=theta_final(r+R_final-R), qT=sin^2(theta), with independent
front position R. Taking both species to share v is a positive-kinetic-energy
closure and minimizes transport energy for their fixed total current; it is
not a general collisionless distribution. Their actual conversion source is

    Gamma = rho (partial_t+v partial_r)qT
          = c_lambda lambdadot+c_R Rdot,
    c_lambda = rho v_lambda partial_r qT,
    c_R = -rho partial_r qT.

Thus conversion is confined to the front gradient, including the contribution
from matter crossing a stationary front. Merely differentiating rhoT at fixed
spatial coordinates would omit its advective current and invent bulk
conversion. The integral of Gamma is the time derivative of total T mass,
because the boundary T current vanishes.

## Positive kinetic metric

The exact transport inertia on this manifold is

    Gtransport_lambda,lambda = integral Q^2/(r^2 rho) dr.

In the stated alignment-dominated canonical completion, the induced internal
inertia uses the *convective* angular speed, not a prescribed global fraction:

    Tspin = (sigma^2/J) integral rho theta_r^2
                  (v_lambda lambdadot-Rdot)^2 dV.

Equivalently Gspin is the positive integral of the rank-one matrix generated
by (v_lambda,-1), with weight2sigma^2 rho theta_r^2/J. The chosen positive
carrier time action adds a nonnegative front inertia. These terms give a
positive metric G_ab wherever the front has nonzero support. A front coordinate
is singular at the exact all-F state, where no front exists; birth must start
from the independently derived unstable phase mode, not an arbitrary R pin.

Use V(lambda,R)=the original full energy evaluated on these profiles, with
all gravity, response, pressure, stiffness, volume and binding variations.
SS-28 checks that value directly. It is not -D sin^2(q), a target-law penalty,
or a fitted formation potential. Its two finer grids connect the endpoints
without a sampled energy barrier; that is not certification of a continuous
path or proof that a natural trajectory follows it.

## All reciprocal forces

After integrating the derivative-current interaction by parts, define

    C_a(q,chi)=g integral chi c_a(q,r) dV, q=(lambda,R).

The reduced Lagrangian is

    L=G_ab(q) qdot^a qdot^b/2 -V(q)
      +integral [chidot^2-c_s^2 |grad chi|^2]/2 dV
      -C_a(q,chi) qdot^a.

Its canonical Hamiltonian is

    H=(p+C)^T G^-1(p+C)/2+V
       +integral [Pi_chi^2+c_s^2 |grad chi|^2]/2 dV.

The material equations, retaining the metric and connection derivatives, are

    G_ab qddot^b + Christoffel_abc qdot^b qdot^c + partial_a V
      =(partial_b C_a-partial_a C_b) qdot^b
        +g integral c_a chidot dV,
    chiddot-c_s^2 Delta chi=-g c_a qdot^a.

The antisymmetric connection term does no work. Multiplying these equations
by their velocities shows exact cancellation of material/scalar exchange,
leaving only outgoing energy flux. This is the energy ledger to implement;
assigning lost optimizer energy to radiation is not an alternative derivation.
Static kinetic momenta can relax to zero, so the potential and its boundary
restoring derivatives are unchanged by the interaction.

## What the next test must decide

Integrate this action, or the less restricted complex-fluid action, while
tracking actual escaped energy, mass, shift charge, density positivity, radius
and the galaxy-law residual. Derive the source from the computed velocities.
Do not insert the full collapse energy into an initially supplied oscillator.

A constant mean Gamma produces a static particular scalar profile, not a
continuously radiating classical wave. In the far zone radiated power depends
on changes of the integrated Gamma. Therefore fast internal inertia alone
does not prove an adequate radiation pump under slow infall. The calculation
must measure front oscillations/bursts or a separately derived fluctuation
spectrum, rather than assume that each unit of converted mass automatically
exports a chosen energy.

If the two-coordinate model succeeds, release the density and phase-profile
constraints and repeat with independent material/vacuum fields. The kinetic
state and entropy of F and the common-coefficient multi-mass failure remain
separate obligations. SS-14/16 and SS-19/20 do not justify replacing the F
state by an arbitrary temperature chosen to make the law fit.
