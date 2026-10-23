# Finite bound kinetic equilibria exist, but do not yet reproduce the required halo law

The identified-medium model admits finite, bound collisionless equilibria with an energy-defined edge and no reflecting wall. In a declared scan,24 of27 zero-stiffness trials reach such an edge;3 approach the polarization cap and are rejected. Including stiffness self-consistently gives8 finite bound cases out of9 further trials, with1 cap rejection. This advances the previous infinite streaming construction, but the finite solutions generally lie below the cold algebraic-law response and retain freely chosen distribution parameters.

These are numerical equilibria of the Newtonian identified-medium model with fixed baryons. They are not exact A33 metric/clock solutions, formed halos, stable attractors, a source selector or an observational success.

## Positive distribution and its self-consistent potential

Use dimensions GMb=a0=rM=1 and a fixed Plummer baryonic scale1:

    gNb=r/(1+r²)^(3/2).

Let m(r) be cold mass in Mb units, q=m/r²<1, and mu the effective potential seen by identified cold particles. The force is

    -mu'=-gNb+q²/(1-q)-gamma rho_hat'.

The dimensionless density satisfies m'=r² rho_hat. The gamma here is the corresponding dimensionless stiffness, not an additional cold thermodynamic pressure.

Choose the positive distribution

    f(Q)=F Q for Q>0, and0 otherwise,
    Q=Ecut-E-L²/(2ra²),
    E=v²/2+mu(r), Psi=Ecut-mu(r).

Energy and angular momentum are constants along stationary spherical characteristics, so this distribution is collisionless-stationary on a solved potential. Velocity integration gives

    rho_hat=A Psi^(5/2)/(1+r²/ra²),
    p_r=(2/7)rho_hat Psi,
    beta_anis=r²/(r²+ra²).

A>0 absorbs the positive phase-space normalization and density units. This is an established type of anisotropic distribution construction; it is chosen here, not derived as the outcome of collapse. Its central region is isotropic and its outer region is more radial, avoiding the singular central distribution of ANISOTROPIC_RESULT.md.

For gamma=0 the coupled equations are

    m'=r² rho_hat,
    Psi'=q²/(1-q)-gNb.

With stiffness, its local contribution gamma rho_hat to mu yields

    (1+gamma partial_Psi rho_hat) Psi'
       =q²/(1-q)-gNb-gamma (partial_r rho_hat)_Psi.

The denominator is positive. Thus the finite-stiffness distribution and density are solved together rather than adding stiffness after choosing a profile. The Jeans identity p_r'+2 beta_anis p_r/r=rho_hat Psi' is checked symbolically.

## An energy-defined finite edge

Integration starts at r=1e-6 with central Psi_c and regular m~A Psi_c^(5/2) r³/3. The first Psi=0 is a candidate edge. Density and radial pressure vanish there. The alternatives are q=0.99, recorded as cap proximity/rejection, or the outer search limit100.

Outside a candidate edge, cold mass is constant, density is zero and the stiffness force vanishes. The potential derivative is

    mu'=gNb-[m/r²]²/[1-m/r²].

For all accepted cases the edge force is inward. The ratio of the outward restoring term to gNb decreases throughout the exterior:

    d ln(R/gNb)/dr
       =3r/(1+r²)-3/r-2r/(r²-m)<0

when r²>m. Hence the edge sign guarantees inward force at every larger radius, not just at sampled radii. Integration to infinity gives a positive depth mu(infinity)-mu(edge). With mu(infinity)=0, Ecut=mu(edge)<0; occupied particles satisfy E<Ecut and are bound. Psi stays negative outside, so the distribution has no exterior population. This is a self-consistent confining transition, not a wall or an arbitrary density truncation.

## Scan and failures

The zero-stiffness scan used A=0.1,1,10; Psi_c=0.2,0.5,0.8; and ra=0.5,1,3. It returned24 finite cases. All three A10,Psi_c0.8 cases reached q=0.99 before an edge. Those trials do not establish nonexistence of all nearby solutions; they fail this construction's cap-avoidance condition.

The stiffness extension held A10,Psi_c0.5 and tested the following cases:

| gamma | ra | edge radius | cold mass/Mb | exterior potential depth | outcome |
|---|---:|---:|---:|---:|---|
| 0.0001 | 0.5 | 1.81161 | 0.0908420 | 0.482788 | bound |
| 0.0001 | 1 | 1.92172 | 0.181351 | 0.460016 | bound |
| 0.0001 | 3 | 2.08726 | 0.311703 | 0.428347 | bound |
| 0.01 | 0.5 | 1.91121 | 0.101950 | 0.463099 | bound |
| 0.01 | 1 | 2.05082 | 0.208144 | 0.436557 | bound |
| 0.01 | 3 | 2.28685 | 0.378457 | 0.396476 | bound |
| 0.1 | 0.5 | 3.49481 | 0.267119 | 0.274533 | bound |
| 0.1 | 1 | 5.69540 | 0.820684 | 0.171701 | bound |
| 0.1 | 3 | — | — | — | q reaches0.99 |

An intermediate commentary incorrectly described all9 stiff cases as bound; detailed inspection corrected that to8. The rejection is retained in the machine-readable result. Aggregate checks concern the accepted subset and must not be read as every parameter choice succeeding.

## Why this does not yet meet the research objective

Finite bound equilibria are not automatically the desired galactic profiles. For example, gamma0.01,ra1 gives total gravity gNb+q only0.6382 times the native cold algebraic-law value at half its edge radius. That is a model-to-model diagnostic, not an observational test. This family cannot be claimed to reproduce the law merely because it is positive and bound.

The distribution amplitude, central relative potential and anisotropy radius remain chosen. They determine cold mass and size; no conserved formation process has selected them. All particles here remain part of the identified/tethered medium. No free S4 population or environmental sourcing fraction is generated.

No linear or nonlinear stability calculation has been performed. The fact that f is positive and stationary does not exclude radial-orbit or other collective instabilities. Fixed baryons, negligible cosmological background and spherical symmetry are also material restrictions. Cosmological formation and the full relativistic parent remain open.

The meaningful next target is whether a finite positive distribution can remain sufficiently close to the native force-law profile over an extended interval, and whether that branch is dynamically stable and reachable. A successful equilibrium fit without those conditions would still leave the mechanism incomplete.

## Evidence

finite_kinetic_run/manifest.json and finite_stiff_run/manifest.json both validate; each has6 passing checks. Every accepted solution was repeated at tighter ODE tolerance: worst relative edge/mass change5.50e-7 for gamma0 and1.35e-8 for the stiff extension. Source files are finite_kinetic.py and finite_stiff_kinetic.py; rejected rows remain in their results. No new mutation, independent numerical method or inner-cutoff convergence scan was performed. The symbolic Jeans identity supplements but does not independently certify the ODE solutions. Review is self-review.
