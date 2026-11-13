# Independent cold-shell cosmology diagnostic

This is a newly specified Newtonian gravitational reference, **not** the DT2/v3
charge equation, its numerical correction, or an adopted theory completion.
The prescribed background is flat matter plus Lambda with Omega_c=.26,
Omega_b=.05, Omega_Lambda=.69, and H0=70 km/s/Mpc. Initial redshift is 10.
The cold fluid is pressureless. Baryons outside the central excess remain
homogeneous. The central excess is a prescribed Plummer mass, 10^10.45 Msun,
softening 1 kpc, ramped linearly from zero over 1 Gyr. This injection does not
derive or conserve a baryonic assembly inventory. No absorption is allowed.

For initial physical radius xi, cold mass M_c(xi)=4 pi rho_c,i xi^3/3 is exact
and includes the inner ball. Let r=xi u and A=G M_c(xi)/xi^3. Before a caustic,

    u_ddot = -A/u^2 + B_bg(t) u
             -G M_b(t) u / (xi^2 u^2 + epsilon^2)^(3/2),
    A = Omega_c H0^2/(2 a_i^3),
    B_bg = -Omega_b H0^2/(2 a^3) + Omega_Lambda H0^2.

Initial u=1, u_dot=H(a_i). Time is physical Gyr, with the exact flat matter/Lambda
age relation. Finite shells span xi=1..2000 kpc. A separate xi->0 marker controls
the first central singularity; it is not a point mass and absorbs no mass.

## Exact analytical homogeneous benchmark (specified before execution)

Set central M_b=0. Substitute u=a/a_i. The cold term is
-Omega_c H0^2 a_i^-3/(2u^2)=-Omega_c H0^2 u/(2a^3).
Adding homogeneous baryons and Lambda gives

    u_ddot/u = -Omega_m H0^2/(2a^3) + Omega_Lambda H0^2
             = a_ddot/a.

Initial position and velocity agree, so uniqueness of the smooth ODE for u>0
gives u=a/a_i. All shells remain outward moving despite negative early-time
acceleration. A numerical trajectory must reproduce both position and velocity
to 2e-7 relative through z=0 before central runs receive physical interpretation.

## Central focusing without an arbitrary cutoff

The central-limit equation has external F=B(t)u, where
B=B_bg-GM_b(t)/epsilon^3. Use u=s^2, dt/dtau=s^2, w=ds/dtau and
E=u_dot^2/2-A/u. Then

    s'=w, w'=E s/2+F s^3/2, E'=2 w s F, t'=s^2,
    2w^2-A-E s^2=0.

The regularized system is smooth at s=0, where w^2=A/2. Stop at its first
downward zero. Continuing through it would introduce an unprescribed bounce.
Finite shells use their physical u,u_dot equations with the same monotone clock.
The energy-constraint residual and an independent physical-time implementation
of the finite-shell forces must agree within declared tolerances.

An independent algebraic reviewer confirmed these equations and the following
ordering argument. For xi_2>xi_1>=0, R=u_2/u_1 and C(t)=GM_b(t)>=0,

    (u_1^2 R_dot)_dot = A/u_1 (R-R^-2)
      + C u_1^2 R [(xi_1^2 u_1^2+epsilon^2)^(-3/2)
                   -(xi_2^2 u_1^2 R^2+epsilon^2)^(-3/2)].

When R>=1 the right side is nonnegative. The shared initial conditions R=1,
R_dot=0 preserve R>=1. Thus the radius map remains ordered before central-limit
focusing. Finite-shell ordering is also monitored numerically. The central
density grows as u_center^-3 and diverges there: this is a central focusing
singularity in the specified reference, not a demonstrated DT2 fold.

## Bounded execution and interpretation

Run homogeneous N=130 first; then central N=130 and260, with time tolerances
2e-10/1e-12 and2e-11/1e-13 respectively. Each run is limited to55 CPU seconds,
60 wall seconds, one numerical-library thread and1 MiB console output. Preserve
sampled trajectories and v2 provenance manifests. Stop at central focusing,
finite-shell crossing, or z=0; never infer a settled halo from a truncated run.
The pressureless reference is independent of a0, so separate a0 footings are
identical here. A run starting q=1331 can dilute; report its actual density range,
not an unsupported claim that all shells remain at q>=1331.

Failure of the homogeneous benchmark blocks interpretation. Passing it validates
only this specified reference. A central event surviving here means that a
prescribed central source can trigger a genuine singularity even with a consistent
background; it does not validate old DT2 event times or its transport equations.
