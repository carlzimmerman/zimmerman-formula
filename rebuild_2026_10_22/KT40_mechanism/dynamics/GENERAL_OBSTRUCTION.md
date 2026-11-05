# A conditional obstruction to local curvature quenching with cold matter

**Theorem.** Fix a nonzero vector g0 and a unit vector n. Consider an
instantaneous nonrelativistic gravitational law specified by a local scalar
energy E(g,H), with H symmetric, and the full variational field equations

    Delta psi=4piG rho,
    Delta Phi=(1/2) div E_g-(1/2) partial_i partial_j E_Hij.

Assume E is C² in a neighborhood of every jet (g0,h nn), h>0. Define
f(h)=E(g0,h nn). Suppose

    lim_(h→infinity) f(h)=L, with L finite,
    f(h0)>L for at least one h0>0.

Then there exists h*>0 with

    N(n)=(1/2) E_HH(g0,h*nn)[nn,nn]=(1/2) f''(h*)>0.

The local Newtonian jet

    psi(r)=g0.r+(h*/2)(n.r)²

has rho0=h*/(4piG)>0. Coupling this field law to a pressureless ordinary
continuity/Euler matter closure gives a frozen-coefficient high-frequency
growing branch along n,

    gamma(k) ~ k sqrt[h* f''(h*)/2],  k→infinity.

Consequently this closure does not have a uniform short-wavelength growth
bound on all such positive-density local backgrounds. The frozen linear
system is not well posed in ordinary Sobolev norms in that direction unless
a cutoff or additional restoring matter/field physics is supplied.

## Proof of the energy-curve step

Choose h2>h0 with f(h2)<f(h0), possible because f(h0)>L and f tends to L.
The mean value theorem gives h1 in (h0,h2) with f'(h1)<0. Suppose, for
contradiction, f''(h)<=0 for all h>=h1. Then f'(h)<=f'(h1)<0 there, and

    f(h)<=f(h1)+(h-h1)f'(h1) → -infinity.

This contradicts the finite limit. Thus f'' is positive at some h*>h1.
The chain rule identifies it with the rank-one Hessian second variation.
No monotonicity of f, convexity assumption, numerical scan, power law or
particular MOND interpolation is used.

## Proof of the dynamical implication

The exact frozen symbol derived in DERIVATION.md is
delta Phi_hat=[K(n)+N(n)k²]delta psi_hat. Mixed gradient/Hessian derivatives
cancel by symmetry of E's second variation. The ordinary continuity and
Euler equations, with positive rho0 and no pressure, then give

    partial_t² delta rho_hat
      =4piG rho0[K(n)+N(n)k²] delta rho_hat.

At the identified jet, 4piG rho0=h* and N=f''/2>0, so the displayed
growth asymptotic follows in a local comoving frame. A constant laboratory
background velocity v0 supplies the leading Doppler shift
omega to omega-k_vector.v0, without changing the exponential growth rate;
constant translation is not a lower-order term. Background gradients and a
finite K contribute lower-order terms in the comoving principal calculation.
The jet is Poisson-admissible with positive local density; it is not being asserted
to be a stationary global galaxy. One may regard the polynomial as the
local part of a uniform-density source plus a harmonic external tidal field.

## Application to the KT39 family

For the fixed simple-Q primitive, g0!=0 and any ell>0, p>0 for which the
required C² neighborhood exists,

    f(h)=|g0|² R[x+(ell² h²/a0²)**p],
    x=|g0|²/a0².

R(z)>1 for finite z>0 and R(z)→1 as z→infinity. Hence f(h)>|g0|² at
every finite h and f(h)→|g0|². For p=9/8, and indeed every positive power
at these nonzero-H jets, the smoothness hypothesis holds. The theorem
therefore applies. Merely choosing another power cannot give this local
family a bounded pressureless high-k response on every positive-density
background while preserving those energy endpoint properties.

The value L=|g0|² is the Newtonian *energy* endpoint. A finite energy limit
alone does not prove that all derivatives have the Newtonian force limit;
that stronger physical statement is not needed for the obstruction.

## Exact scope and escape conditions

This is a restriction on the specified local E(g,H), instantaneous elliptic
field equations and cold-fluid closure. It is not a relativistic ghost
theorem, a collisionless stability theorem, an observational exclusion of
every modified-gravity mechanism, or proof that the unstable jet occurs in
the fitted Milky Way. The actual MW probes and finite-pressure completion
must be checked independently.

Finite pressure can remove the leading growing branch if
c_s²>=4piG rho0 N(n) in every direction; the equality case still requires
lower-order analysis. For several components the matrix criterion in
DERIVATION.md applies. Additional fields with their own dynamics, genuine
nonlocal response, a physical short-distance cutoff, or a different energy
endpoint structure are outside the theorem and require their own checks.
An assumed stable background or a numerical grid cutoff is not by itself
a derived physical completion.

Proof provenance: mechanism_dynamics derived the argument from the local
action and ordinary matter equations; root requested this exact generalized
claim for independent audit. The argument is analytic and does not rely on
the finite jet experiment. Historical KT39 equations remain unchanged.
