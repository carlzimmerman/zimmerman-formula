# Reciprocity audit of source filtered gravity

Checkpoint RA20261103-c8b2586. This audits the field map explicitly stated in
KT14 and inherited by the fixed-width KT17/KT25 construction. It does not
replace their numerical scores, establish a covariant theory, or reinstate a
retired sector. The new result is a structural consistency check on that map.

## Claim and verdict

Let S be convolution with a fixed normalized Gaussian, N the Newtonian
potential operator, and Q[rho] the ordinary QUMOND potential with the simple
nu function. The implemented potential is

    F[rho] = N rho + (Q-N)[S rho].

With ordinary universal matter coupling, this map is **not in general the
functional derivative of a twice differentiable static energy of rho**.
Its linear response fails reciprocity on an explicit positive-density
periodic background. This obstruction concerns the stated map and coupling,
not every possible nonlocal, dynamical, or modified-inertia theory.

Implementation locator: `rebuild_2026_10_22/KT14_filtered_phantom_mw/kt14.py`,
`solve`, which sets `Phi = PhiN + LU.qumond(PNx) - PNx`.

## Derivation

Use a common periodic or compatible self-adjoint Poisson domain, fixing the
potential gauge and external field. Write P=Delta^{-1} on zero-mean sources,
N=4 pi G P, u=u_ext+grad N S rho, and A(u)=[nu(|u|/a0)-1]u, where u_ext is
the fixed external gradient (zero is allowed). The phantom potential
is P div A(u). At a nonzero-field background its derivative with respect to
its own source is

    B = 4 pi G P div M(x) grad P,
    M = [nu-1] I + (nu'/a0) u tensor u / |u|.

M is symmetric. Integration by parts therefore gives B*=B, subject to the
stated boundary conditions. For fixed S=S*, the implemented map has

    DF = N + B S,
    (DF)* = N + S B.

The second variation of an energy must be symmetric. The required condition
is [B,S]=0. Multiplication by the spatially varying M generally does not
commute with Gaussian smoothing. Gaussian self-adjointness alone does not
make B S symmetric.

## Explicit counterexample in the actual simple nu law

Set 4 pi G=a0=1 on the 2 pi periodic planar domain, with the mean density
subtracted in Poisson's equation and a fixed external Newtonian gradient 1.
Take Gaussian width sigma>0, s_n=exp(-sigma^2 n^2/2), and

    rho(x)=rho_c-(epsilon/s_1) sin x,
    rho_c>epsilon/s_1, 0<epsilon<1.

The total filtered Newtonian gradient is u=1+epsilon cos x>0. Both source
variations f_1=cos x and f_2=cos 2x have zero total mass and preserve positivity
at sufficiently small amplitude. For nu(u)=1/2+sqrt(1/4+1/u),

    m(u)=A'(u)=(u+2)/(2 sqrt(u^2+4u))-1/2,
    m'(u)=-2/(u^2+4u)^(3/2)<0.

With the mean integral inner product,

    b_12=<f_1,B f_2>=-<m(u) sin x sin 2x>/2 > 0.

The sign follows exactly by pairing cos x and -cos x: m decreases strictly,
so the integral of 2 m(1+epsilon cos x) sin^2(x) cos x is negative. Hence

    <f_1,DF f_2>-<f_2,DF f_1>=b_12(s_2-s_1) != 0.

This is an analytic counterexample; midpoint quadrature in the accompanying
script checks the normalization and sign at sigma=.7, epsilon=.2. It is a
periodic external-field problem, not a simulation of an isolated galaxy.
For a width depending only on total mass, these zero-mass variations keep
that width fixed and the same necessary-condition failure persists.

## What an energy construction actually gives

If U_N and U_ph are the Newtonian and QUMOND phantom reduced energies, define

    U_new[rho]=U_N[rho]+U_ph[S rho].

The chain rule gives

    Phi_new = N rho + S* (Q-N)[S rho].

For a fixed isotropic Gaussian, S*=S. The additional outer filter is required
by this particular construction. Its response is N+S* B S, which is symmetric.
For a translation- and rotation-invariant fixed S, the reduced interaction
also has those symmetries. These facts do not select sigma or demonstrate
relativistic causality, stability, or observational agreement.

If S depends on local fields or density, the derivative is instead
D(rho -> S[rho]rho)* applied to the phantom potential. Extra terms from the
filter dependence must be retained. Merely inserting a local width into each
output row is not this variation. The full derivative might have several
terms; no unique adaptive action is claimed here.

## Relation to previous work

The general adjoint/variation principle is established mathematics, not a
novel physics claim. The repo already contains older two-sided constructions:
CFG653 uses a high-pass response on both sides; its limits and observational
failures concern that different operator. In particular,
`qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md:26` explicitly
contains the outer S* in its filtered nu_mono equation. L340 inherits that
older static sector, while AS471 is a proposed discrete-adjoint certificate.
None supplies a missing outer
operator in the actual KT14 source-only implementation. An amended operator
earns its own empirical grades.

Milgrom's QUMOND action, arXiv:0911.5464v2, equation (3), provides the standard
variational starting point. His generalized QUMOND paper,
arXiv:2305.01589v2, sections II–III, gives a related action-based way of making
the response depend on additional spatial information. Neither source proves
that this proposed filtered completion passes the repository's constraints.

## First discriminating continuation

Hold the constant-width operator fixed and check whether its variational
completion preserves the narrow Milky Way and Cassini window, using exactly
the same matter coupling and source in both systems. Before a parameter
search, verify source-response reciprocity, the Newtonian and zero-width
limits, and the ordinary field equation on a common multidimensional grid.
Use source splitting and separated host/satellite controls before adopting
a system-mass rule. A failure ends this completion at the tested premise;
it does not justify tuning a new local width after each failed object.

This is a proposed continuation backed by a new audit result. It has not
been assigned an astrophysical PASS or used to alter any seal or owner decision.

## Review and finite verification

An isolated review agent independently checked the derivative, two-mode
normalization, monotonicity sign, positive-density domain, and constant-total-
mass qualification. The root coordinator authenticated the external papers.
Agreement is review provenance, not a substitute for the displayed proof.

The bounded run `reciprocity_run/manifest.json` completed and its manifest
validated. At sigma=.7 and epsilon=.2 the two reciprocal cross responses are
0.0017058629236758362 and 0.0035575464090079347. Their difference is
-0.0018516834853320985, stable from 64 to 4096 quadrature points. Zero width
and homogeneous-background controls vanish within floating error. The
variational completion's two cross responses coincide. Those corrected
responses follow from the analytic Hessian formula; they are not a separate
astrophysical solver validation.
