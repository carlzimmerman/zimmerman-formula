# Moving-source branch audit

The selected moving-Sun solution remains NO VERDICT. This document
separates an exact conditional branch, its congruence limitation, and a
local charged-background response. Kappa = 1/2 FITTED; not theory closed.

## Why the static alpha ratio cannot be imported

AS3's AeST calculation is not v3s's action. Its useful methodological
point is that a source moving through the preferred frame must satisfy
the moving equations with omega=k.v. The static potential need not be
the potential carried by that source. Dividing a moving gravitomagnetic
coefficient by a different static branch's Newton constant does not compute
a physical alpha_1. No AS3 numerical alpha formula is transferred here.

## An exact conditional v3s GR branch

Take a GR metric and a local scalar tau satisfying

    g^{ab} partial_a tau partial_b tau = -1,
    n_a=-partial_a tau,  P^a=0.

Then Q=1 and n is geodesic: because n is a gradient,
n^a nabla_a n_b=n^a nabla_b n_a=(1/2)nabla_b(n^a n_a)=0.
The extra v3s terms have zero value and first variation:

- P.A varies as delta P.A+P.delta A, zero when P=A=0.
- The capped W obeys W(0)=W'(0)=0; its vector derivative also vanishes
  at P=0 because its leading small-P term is quadratic.
- F(s)=gamma max(s,0)^2/2 is C1 with F(0)=F'(0)=0. No nonexistent
  two-sided second derivative at s=0 is used.
- K(Q)=mu²(Q-1)^2/(2K) and its first derivative vanish at Q=1.

Thus the extra stress and field equations vanish, and the metric equations
reduce to GR wherever this smooth congruence exists. This verifies the
branch on v3s itself. Its metric has GR's alpha_1=alpha_2=0 when normalized
with that metric's own G. It says nothing about initial-data selection,
Galactic polarization matching, or a different static effective G.

The Schwarzschild known answer uses f=1-2M/r and
tau=E t+T(r), T'=sqrt(E²-f)/f. The code verifies Q²=1 and both normalized
acceleration components identically zero for symbolic E, and records
E=1,13/12,5/3. These radial examples validate the identity; they are not
the uniform incoming wind used in the next calculation. The mutant inserts
the flat-space T'=sqrt(E²-1) into Schwarzschild. Its normalized vector
still has unit norm, but Q is not1 and its acceleration is nonzero: the
extra-sector-free branch conditions fail.

## Incoming timelike geodesics and focusing

The asymptotic frame velocity is an assumption, not fixed by v3s. For each
tested v define r_c=GM/v², epsilon=v²/c², R=r/r_c, B=b_impact/r_c,
E=(1-epsilon)^(-1/2), lambda=tau_proper v/r_c. With angular momentum
L=E(v/c)b_impact, the exact Schwarzschild radial equations become

    R'' = -1/R² + E²B²/R³ - 3 epsilon E²B²/R^4,
    theta' = -E B/R²,
    T' = E/(1-2epsilon/R),  T=t_coordinate v/r_c,
    R'^2 = E²+2/R-E²B²/R²+2epsilon E²B²/R³.

The last expression avoids subtracting two nearly equal relativistic
energies. Incoming theta at R0 is pi minus the angular integral from
infinity. The energy equation independently supplies the turning radius.
The code checks this radius, conservation and numerical tolerance pairs.

Every main ray focuses at theta=0 downstream. Rotating such a ray through
all azimuths gives the same axis point with distinct transverse velocities;
the azimuthal separation r sin(theta) vanishes there. This is the caustic
warning for a single-valued geodesic congruence. It is not a singularity of
the Schwarzschild metric. All tested periapses exceed the declared solar
radius, so these trajectories do not rely on an interior metric model.

The focusing distances are near B² r_c/2; the exact relativistic trajectories
and their convergence checks, not that approximation, supply the result.
The flat-profile mutant has straight rays and no focusing. When those rays
are tested against Schwarzschild's invariant they violate its energy
conservation, as required. The mutant is inconsistent input, not an
alternative physical solution of v3s.

A local Hamilton-Jacobi geodesic flow can represent the branch before
crossing. Extending it through the caustic as one smooth tau is not justified.
Whether nonzero polarization/dust or different matched initial data provide
a regular moving solution is precisely the remaining nonlinear question.

## Charged-background forced oscillator

On the positive switched branch, freeze the local PN coefficients at
mu_K=0 and keep Poisson feedback. For each longitudinal Fourier mode,

    rho_tau_dot = -i k rho0 v,
    v_dot = i K rho_source/k
            -i [K(M_theta-1)/k + gamma k] rho_tau.

Hence

    rho_tau_ddot + Omega² rho_tau = K rho0 rho_source,
    Omega²=K rho0[M_theta-1+(L_star²/2)k²].

With source amplitude1 times exp(-i omega t), omega=k.v, and zero response
initial data, the exact solution is

    rho_tau = K rho0 [exp(-i omega t)-cos(Omega t)
                     +i(omega/Omega)sin(Omega t)]/(Omega²-omega²).

At resonance this has the finite limit

    rho_tau = K rho0 [sin(Omega t)/Omega
                     -t exp(-i Omega t)]/(2i Omega).

The script checks the equations and initial data symbolically, compares the
solution to an independent50-digit convolution, and integrates it at two
tolerances. A stationary denominator has a pole when the source velocity
component equals Omega/k. That does not make the switched-on finite-time
solution singular, and no observational exclusion follows from this test.

The numerical M_theta=(1+x_e)^2 is the longitudinal stiffness bracket,
not a full fixed-orientation anisotropic calculation. Nevertheless the
existence of a resonant direction is robust here: M_theta lies continuously
between the transverse and longitudinal Hessians; the maximal phase speed
is already below v. At zero velocity projection Omega²-(k.v)² is positive;
at parallel projection it is negative. A direction with zero denominator
therefore exists. This argument does not compute the three-dimensional wake.

The illustrative Galactic density, velocity, initial data and finite
one/ten-crossing-time window are all explicit. The largest Fourier transfer
in that window is not a long-time bound, not a real-space Solar force, and
not alpha_1. A pre-existing charged halo has different homogeneous data.

## Remaining physical calculation and self-review

The missing calculation matches a moving finite Sun to the Galactic
polarization and khronon flow, evolves the nonlinear switched constraints
and transport through the downstream region, and computes the resulting
metric response. It must determine whether the local geodesic branch is
selected and whether a regular continuation exists. Static CQ7/C6 profiles
or a bare-G ratio cannot answer that.

Self-review checked the exact action's first variation, distinguished
radial known answers from incoming rays, retained the Schwarzschild energy
test in the mutant, checked the turning radius independently, kept Poisson
feedback in the forced oscillator, and avoided treating a resonant
stationary formula as a finite-time divergence. No independent-agent review
was used. Full nonlinear matching and global congruence regularity remain
open; this lane supplies evidence and explicit obligations, not a full PASS.
