# Can the finite-band relative dipoles form a local medium?

This analytic continuation uses `relative_modes/RELATIVE_MODES.md`, equations
(18)-(25). It addresses its unconstructed many-host step, rather than
denying the single-host form-factor window.

## Separated diffuse hosts: incompatible scale requirements

A compact carrier of size R_d moving against a much larger compensating
host R_b has F_d-F_b approximately one only when

    k R_d << 1 << k R_b.

For independent separated hosts with number density nu and diffuse-host
filling f=(4pi/3)nu R_b^3<=1, the mean number of host centers in a probe-scale
ball of radius 1/k is

    N_probe = (4pi/3)nu/k^3 = f/(k R_b)^3 << 1.                (1)

A self-averaging local constitutive medium on scale 1/k requires many
independently responding sites per coarse volume, hence N_probe>>1. There is no
parametrically controlled simultaneous limit. Defining the probe length
as 2pi/k multiplies (1) by a fixed (2pi)^3 and does not repair the scale
separation limit. A finite marginal configuration must state its counting
error rather than assert a homogeneous local response.

For Gaussian profiles R_b is a declared effective radius, since their tails
are not compact. Any fixed choice R_b=C sigma_b only changes constants.
Deep on the form-factor plateau k sigma_b>>1, the same scale conflict holds.
The plateau is still a measurable response of a single object or a spatially
resolved sparse population. It is not by itself a local space-filling fluid.

Overlapping or common diffuse baryons evade the separated-host packing bound.
Their mass and inertia must then be counted once, and their response solved
as a shared field. Replacing them by a separate complete recoiling host for
each compact carrier would multiply the reservoir mass and oscillator
strength. Equation (1) excludes only the separated independent-host
homogenization; it does not exclude a different dense collective phase.

## The simplest shared reservoir has no positive gravity-only optical gap

As a discriminating calculation take two homogeneous, separately conserved,
barotropic fluids, with positive densities rho_d,rho_b and sound speeds
c_d,c_b. They interact by ordinary attractive Newtonian gravity only. This
is a conditional shared-reservoir model, not a claim that collisionless
baryons or the source-produced scalar state are already such fluids.
Precisely, use the standard mean-subtracted Jeans linearization, or a local
Jeans approximation: an unconfined homogeneous positive-density medium with
its unsubtracted Newtonian mean field is not an exact static equilibrium.

Linear continuity, Euler and Poisson give

    delta rho_a double-dot + c_a^2 k^2 delta rho_a
       - K rho_a (delta rho_d+delta rho_b)
       = -rho_a k^2 U_ext,       K=4piG.

In coordinates x_a=delta rho_a/sqrt(rho_a), the symmetric frequency matrix is

    D(k) = diag(c_d^2 k^2,c_b^2 k^2) - K v v^T,
    v=(sqrt(rho_d),sqrt(rho_b)).                              (2)

As k approaches zero through nonzero modes, its eigenvalues tend to
-K(rho_d+rho_b) and zero. Separately fixed total masses remove the exact
density zero modes. The first limiting eigenvalue is the usual
Jeans instability of the homogeneous gravitational medium; the compensated
relative vector is orthogonal to v and has no gravitational restoring
eigenvalue. Thus this medium does not acquire a positive optical frequency
sqrt(K rho) just by allowing a live common reservoir.

For positive sound speeds,

    det D = c_d^2 c_b^2 k^2
           [k^2-K(rho_d/c_d^2+rho_b/c_b^2)].                 (3)

If k^2 exceeds the bracket's critical value, D is positive definite: write
D=A^(1/2)[1-K A^(-1/2)vv^T A^(-1/2)]A^(1/2). Below it one eigenvalue is
negative. There is no stable infrared gapped relative branch in this model.
Uniform gravitational acceleration translates both components and leaves
their relative coordinate unforced, in agreement with the single-host
source analysis. Adding quantum pressure changes the diagonal by positive
k^4 terms and does not create a positive nonzero k=0 optical gap.

This is not a theorem about an inhomogeneous bound shared host, a lattice,
anisotropic stresses, finite boundaries, or nonbarotropic dynamics. Those
could supply distinct relative modes. A viable continuation must exhibit
that actual equilibrium and derive its full source and mode spectrum;
the homogeneous two-fluid replacement alone is insufficient.

The central missing step has therefore narrowed to a stable *inhomogeneous
shared state*, with many physical source-carrying modes per probe volume,
without double-counted baryon mass or gravitational spring energy. A linear
oscillator spectrum still needs a separate mechanism for the required
nonlinear saturation and its joint d-gap occupation distribution.
