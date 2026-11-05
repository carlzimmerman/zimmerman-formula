# A named vacuum cancellation applied to the joint phase model

The original global sequestering prescription removes U0 from the conditional
matching calculation. This addresses the additive vacuum-offset problem in
the previous model. It does not fix criticality or the MOND coefficient.
The result is a necessary matching calculation for a proposed extension,
not a constructed protected covariant MOND action or a solved cosmology.

## Source and transfer boundary

[Kaloper and Padilla, arXiv1406.0711v2](https://arxiv.org/html/1406.0711v2),
section3 equations(14)-(16), gives the global trace-subtracted gravitational
equation for a protected matter sector. The averaging measure covers the
whole finite spacetime volume. Their protected-sector treatment does not
include graviton loops. We conditionally place the new amplitude potential
inside such a sector; no source proves that our polarization coupling has
the required protected embedding. The primary HTML was inspected, not
downloaded. The following application and scalar-history reduction are
our calculation, not results claimed by that paper.

Unlike K206, this test uses a homogeneous phase potential rather than the
spatially sparse halo energy. Unlike K279, no adjustable residual four-form
flux is added. Those earlier results remain valid within their scopes.

## Exact vacuum and trace bookkeeping

Use signature -+++, c=hbar=1. At zero polarization the amplitude potential is

    V(sigma)=U0-t sigma^2/2+A sigma^3/3, sigma>=0,
    m=t/A, Delta=t^3/(6A^2), V_f=U0-Delta.

Assume a canonical amplitude kinetic term. In spacetime dimension d its
stress trace is (d-2)dot(sigma)^2/2-d V. The general-d trace subtraction
below is our stated algebraic extension; the cited source supplies d=4.
Let Theta be the averaged trace of all remaining protected matter. The
vacuum density one would assign to the stationary minimum is

    epsilon_f=V_f-<V>+(d-2)<dot(sigma)^2>/(2d)+Theta/d.

U0 cancels exactly. The local sigma equation remains

    sigma_ddot+(d-1)H sigma_dot+V_sigma=0.

An integration by parts, with no endpoint term discarded, gives

    <dot(sigma)^2>=<sigma V_sigma>+E_boundary,
    E_boundary=[a^(d-1) sigma sigma_dot]_initial^final
                   / integral a^(d-1) dt.

This relation requires finite integrals and a regularized endpoint treatment
if a cosmological singularity is present. Declaring E_boundary=0 without
establishing those conditions is not justified.

For d=4, write x=sigma/m. The exact reduction is

    epsilon_f=Delta F,
    F=-1+(3/2)<x^2>-(1/2)<x^3>+(E_boundary+Theta)/(4Delta).

The brackets are weighted by the full spacetime volume. They are not
present-epoch values or a chosen averaging window. In particular the phase
gap Delta is not itself the residual gravitating energy.

This evaluates the would-be local vacuum term at the minimum. It does not
assert that a nontrivial solution reaches sigma=m, sigma_dot=0 at a regular
finite time: uniqueness of the canonical equation would then make that
solution stationary throughout its regular history. Actual late-time
matching needs an approach to the minimum or a controlled approximately
stationary era, together with the global constraints.

## A useful sign test, with its hypotheses explicit

Ignoring kinetic energy is not legitimate for a rolling phase. The simple
two-state potential-only limit would give epsilon_f=-f_early Delta, where
f_early is the earlier phase's volume fraction; this is only a bookkeeping
limit, not a canonical transition solution.

With the kinetic term included through the identity above, if the entire
history obeys0<=x<=1, E_boundary=0 and Theta<=0, then epsilon_f<=0. The
pointwise certificate is

    -1+(3/2)x^2-(1/2)x^3=-(1-x)(2+2x-x^2)/2<=0.

Positive residual energy would therefore require leaving at least one of
these hypotheses: overshoot, another positive trace contribution, nonzero
endpoint contribution, or additional dynamics. Such histories are not
excluded. No positive or negative residual is claimed for an actual universe
without solving its history. The sign test is not an all-sequestering no-go.

## Connection to the calculated force coefficient

On the previously conditional delta=0 response slice, and at fixed global
background in the local test-source limit,

    a_MOND=1/(K B h^3), K=4pi G,
    p_c=t/(Ah), lambda_phase=p_c/a_MOND.

A global constant subtraction has no local p-cubic derivative. Combining
the response with the residual above, for F>0, yields

    kappa^2=24pi(B/A)/(lambda_phase^3 F).

This is joint matching with U0 eliminated, but it is not a predicted number.
F must come from a self-consistent global solution, not an assigned history.
Its partial derivative in the diagnostic ratio is nonzero; that fact alone
does NOT prove it can vary freely among on-shell cosmologies.

There is a more direct restricted nonselection statement. In this specified
mean-field homogeneous p=0 model, the potential, canonical amplitude history
and homogeneous trace constraints do not contain B or h. The local force
coefficient does. Holding A,t and the homogeneous solution fixed while
changing h therefore preserves those equations and changes the local test-
source response. This is a physical coupling change with the gravitational
normalization fixed, not a field-unit change. It shows that homogeneous
sequestering alone cannot select the response in this construction.

This argument does not include inhomogeneous polarization in the full
historic average, curved-background quantum corrections, or a new symmetry
tying the couplings together. It cannot exclude a different shared microscopic
completion. Likewise this step supplies no protection for delta=0.

## Verification and next discriminating work

sequester.py passes11 exact checks. Omitting the historic potential subtraction
fails precisely vacuum-offset invariance and the two-state residual test.
Both records have validated input/output manifests. The additional B,h
homogeneous-independence argument is an analytic reading of the explicit
potential, not an independent covariant implementation audit. Self-review only.

The next construction must couple the response-generating sector to the
vacuum/history selector through a justified interaction or symmetry. Solving
more homogeneous histories while B,h remain absent from their equations
cannot determine them. If a shared interaction is supplied, the required
checks are its protected vacuum embedding, its actual kinetic terms and
criticality, and the resulting global/local matching. The goal remains open;
no fitted history, flux or coefficient has been substituted for that work.
