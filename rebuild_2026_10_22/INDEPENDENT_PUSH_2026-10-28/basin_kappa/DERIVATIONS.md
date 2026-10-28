# Basin mechanisms and kappa: derivations and scope

Base: `7954d48377463cafcae3e8dbb09454134aef384f`. The original target
(a condensation mechanism and a derivation of kappa) remains open.
This file supplies three scoped obstructions and an independently executable
turnaround calculation. These are nonrelativistic statements, not a new
covariant parent. Kappa = 1/2 remains FITTED.

## 1. Acceleration at first turnaround is not a galaxy-scale switch

Let M be the gravitating mass of a spherically symmetric isolated shell, with
no shell crossing. In the Newtonian diagnostic with a constant vacuum term,

    R'' = -GM/R^2 + H_Lambda^2 R.

For the shell's first maximum R0, R'(R0)=0. Energy conservation gives

    R'^2 = 2GM(1/R - 1/R0) + H_Lambda^2 (R^2 - R0^2).

This is a stipulated shell model. Applying it to baryons in the simple law,
or treating the shell mass as the BS1 catalogue mass, requires an additional
physical identification. No such identification is silently made here.

Define q = H_Lambda^2 R0^3/(GM). A shell that turns inward has 0 <= q < 1.
Integrating from R=0 at t=0 to R0 at t=t0 yields

    t0 sqrt(GM/R0^3) = I(q),
    I(q) = integral_0^1 du / sqrt[2(1/u-1) + q(u^2-1)].

With u=sin^2(theta), the endpoint-regular form is

    I(q) = integral_0^(pi/2)
           2 sin^2(theta) / sqrt[2-q sin^2(theta)(1+sin^2(theta))] dtheta.

Thus H_Lambda t0 = sqrt(q) I(q). The right side increases continuously
from zero to infinity: positivity gives strict monotonicity; near q=1 and
theta=pi/2 the integrand has the logarithmic endpoint divergence. Hence
there is one q for every positive H_Lambda t0.

At the boundary GM/R0^2 = a0,

    Mcrit_N,Lambda = q^2 a0^3/(G H_Lambda^4).

If H_Lambda=0, I(0)=pi/(2 sqrt(2)), so exactly

    R0^3 = 8GM t0^2/pi^2,
    Mcrit_N,0 = 64 a0^3 t0^4/(pi^4 G).

The static balance radius Rstat=(GM/H_Lambda^2)^(1/3) instead has q=1.
It is approached only at infinite first-turnaround time in this diagnostic.
Its threshold Mcrit_stat = a0^3/(G H_Lambda^4) is not the finite-age answer.

For the actual simple law, x=g/a0 and y=g_N/a0 obey y=x^2/(1+x).
Consequently g=a0 means g_N=a0/2. Postprocessing Newtonian turnaround
radii therefore changes the critical mass by exactly 1/8, because
g_N(R0) is proportional to M^(1/3). This postprocessing is not a dynamically
self-consistent modified-gravity collapse model.

For a distinct, internally self-consistent toy, put the simple law directly
into the spherical shell acceleration. Let rM=sqrt(GM/a0), s=R/rM, and

    U(s) = -(1+sqrt(1+4s^2))/(2s) + asinh(2s),
    U'(s) = [1+sqrt(1+4s^2)]/(2s^2) = g/a0.

The symbolically checked primitive gives

    beta = H_Lambda^2 rM/a0,
    J(beta,s0) = integral_0^s0 ds /
       sqrt[2(U(s0)-U(s)) + beta(s^2-s0^2)],
    H_Lambda t0 = sqrt(beta) J(beta,s0),
    Mcrit = beta^2 a0^3/(G H_Lambda^4).

Use s0=1 for the condition g_N=a0, or s0=sqrt(2) for g=a0.
Inward acceleration at the maximum requires beta < U'(s0)/s0.
At static balance with g=a0, beta=1/sqrt(2), so the static simple-law
threshold is a0^3/(2G H_Lambda^4). Neither toy constructs condensation.

The executed script checks both footings, three declared ages, adaptive versus
independent fixed-grid quadrature, SI reconstruction of the time and radius,
and positive energy radicands. The age input is externally calibrated in the
inherited record. Its 10–20 Gyr sensitivity bracket is reported in full.

## 2. A shell-theorem obstruction to a purely local basin trigger

**Claim BK-local.** A function of the local baryonic/cold densities, velocity
and gauge-invariant Newtonian/AQUAL force derivatives cannot reproduce the
rule "halo iff the total mass of the zero-velocity basin exceeds T" for all
smooth spherical pressureless initial conditions. This includes arbitrarily
many spatial derivatives at regular interior points 0<r<a, and local history
on a sufficiently short interval with no shell crossing anywhere relevant.
It excludes dependence on a new nonlocal
state, a prescribed outer boundary functional, absolute potential, or
unspecified derivative extensions of AQUAL.

**Construction.** Fix a basin radius R0 and an observation ball r<a. Put a
smooth, nonnegative spherical mass distribution of total enclosed mass T/4
inside R0, mostly concentrated in r<a/2. Include a common arbitrarily faint
smooth tracer density positive near R0, subtracting its enclosed mass from
the central distribution so that the total remains T/4. Choose the central
distribution as a smooth hollow bump supported away from r=0, and the
tracer hollow near r=0 as well. This avoids invoking smooth AQUAL evolution
through a positive-density center, where g instead behaves as sqrt(r).
Local histories below are restricted to regular shells before relevant
singularities or shell crossing. The velocity at R0
is then defined on occupied fluid, not assigned to vacuum. Compare this
configuration with the same distribution plus a smooth, nonnegative
annulus with total mass T in b<r<c, where a<b<c<R0. Such smooth bump functions
exist explicitly: a normalized multiple of exp[-1/((r-b)(c-r))] on (b,c),
zero outside, supplies the annulus. Both configurations can have the same
smooth radial velocity field, contracting inside R0 and vanishing at R0.
For example v_r = h r(r^2/R0^2-1), with h>0, is smooth at the origin.
Choose the common physical length small enough that both shells at R0 are
bound and accelerating inward; then this zero-velocity surface is consistent
with an infalling basin. The proof needs admissible instantaneous data, not
the assertion that these artificial initial data arose from a measured P(k).

Spherical AQUAL gives, on its regular radial branch,

    mu(g/a0) g = GM_enc(r)/r^2.

The function mu(x)x=x^2/(1+x) is strictly increasing for x>0. The enclosed
mass is identical for every r<b, so the complete local force fields there
are identical. Newtonian gravity is the same argument with mu=1. The
exterior annulus changes the potential only by a spatial constant in the
interior; absolute potential is not a local force observable. All local
density/velocity data and their force derivatives agree. Meanwhile the basin
masses are T/4 and 5T/4, so their required flags are opposite.

Any deterministic function of the identical local inputs has the same value
in the two configurations, proving the claim. In the spherical pressureless
evolution, shell ordering and enclosed masses stay fixed before shell
crossing. The inner histories therefore also agree on a sufficiently short
interval, so adding finite local time derivatives does not cure the
counterexample. The cosmological constant, if retained, adds the same
H_Lambda^2 r to both local accelerations.

**Implication.** The shared basin must be communicated through nonlocal
information, a boundary condition, or additional state. AQUAL's local force
argument by itself cannot carry the information in this class. This is not
a no-go for every possible basin mechanism, nor a refutation of BS1's
phenomenological flag. It applies to a larger initial-data class than the
actual Universe; restricting histories could invalidate its universality
premise, which then must be stated and demonstrated by the mechanism.

## 3. Dust-gravity-alone has no absolute collapse mass at fixed history

Take a spherical pressureless Newtonian solution before shell crossing,
with shell label chi, density rho, radius R(chi,t), and mass M(chi). If all
dimensionless initial density and velocity profiles are fixed, then for
every ell>0,

    R_ell = ell R,  M_ell = ell^3 M,  v_ell = ell v,  rho_ell = rho

solves the same equations at the same t and H_Lambda. Indeed every term of
R''=-GM/R^2+H_Lambda^2 R scales by ell. The continuity equation is also
preserved. Collapse/turnaround times and dimensionless retention fractions
evaluated on corresponding rescaled regions (or by scale-covariant definitions)
are identical. A fraction measured in a fixed physical aperture need not be.
Hence this dynamics alone cannot make condensation turn on at
one absolute M=T when it is absent at a rescaled mass with the same history.

Scope matters. Actual cosmological P(k), mass-dependent formation redshifts,
primordial dimensional scales, velocity dispersion, pressure, screening or
other microphysics can break this scaling. The simple-law term a0 already
breaks it, as the first-turnaround calculation quantifies. The theorem does
not refute the mass dependence of Sigma_coll(M), c_nat(M), or an inherited
nonlinear zoom result. It identifies what dust-gravity-alone cannot supply.

## 4. Kappa is a physical matching coefficient, not a field convention

This audits the normalization obstruction already present in the record;
it is not claimed as a newly discovered no-go. Consider the specified
nonrelativistic Lagrangian density

    L = -A F(B |grad psi|^2) - q rho psi,  A,B,q > 0.

The acceleration measured by matter is -grad phi, with phi=q psi.
Variation and conversion to phi give

    div[F'(B |grad phi|^2/q^2) grad phi] = q^2 rho/(2AB).

For the simple-law primitive

    F(z) = z - 2 sqrt(z) + 2 ln(1+sqrt(z)) + C,
    F'(z) = sqrt(z)/(1+sqrt(z)),

the physical high-acceleration coupling and transition scale are

    G_N = q^2/(8 pi A B),   a0 = q/sqrt(B).

A genuine field redefinition psi_new=ell psi changes q_new=q/ell and
B_new=B/ell^2. Both G_N and a0 remain exactly fixed. Thus
a0^2/(c^2 G_N rho_DE)=kappa^2 remains fixed when rho_DE is fixed.
Simply changing the fitted numerical kappa while holding G_N, rho_DE and
matter units fixed changes observable physics; it is not this convention.

The additive C is invisible to F', to the force equation, and to its
ellipticity conditions mu>0 and mu+x mu'>0 for x>0. If a covariant lift
identifies the same constant density term with vacuum energy,

    rho_DE c^2 = A C,

then and only then this class implies

    kappa^2 = 8 pi/C.

Consequently C=32 pi is equivalent to kappa=1/2; it is not forced by the
simple mu. The identity is conditional on the vacuum identification, which
this nonrelativistic Lagrangian cannot establish. Rescaling F and A together
does not remove the physical matching freedom: the full action stays the
same, while the normalized ratio is unchanged. A new principle would have
to fix this ratio or replace the identification, then survive an independent
observable test. No such principle is supplied here.

## 5. Adversarial audit and surviving gap

Review provenance: separate self-review, a fresh delegated independent audit,
and the root coordinator's independent algebra check. See INDEPENDENT_REVIEW.md
for the audited artifact hash, restrictions identified, and applied narrowing.

| obligation | outcome |
|---|---|
| distinguish zero radial velocity, inward acceleration and static balance | passed: q<1 versus q=1 |
| distinguish gravitational g_N, simple-law g, and net acceleration with vacuum | passed: separate columns and formulas |
| simple-law energy primitive and normalization redefinition | exact symbolic checks passed |
| quadrature numerical tolerance and original SI dimensions | executed checks passed on all declared cells |
| shell counterexample stays within smooth positive density, regular velocities | passed by bump construction; no delta shell needed |
| potential gauge / elliptic global dependence | restriction explicit; new global auxiliary excluded from claim |
| histories and P(k) cannot be silently fixed or scaled | restriction explicit; no claim against mass-dependent formation |
| vacuum identification from a covariant parent | not addressed; remains an assumption |
| derivation of BS1 condensation, L or kappa | not reached |

The narrowest live unresolved step is to exhibit a physical state variable
whose evolution actually acquires common basin information and changes the
stability of the cold component. A local force-only instability fails the
annulus discriminator; dust gravity with fixed dimensionless initial history
fails the similarity discriminator. A proposed nonlocal mechanism should be
tested first on these paired initial conditions before an expensive zoom.
That is a precise remaining obligation, not a proposed final field equation.
