# Independent audit: nonlinear Q energy on the weighted crossing domain

Reviewer: /root/pressure_extrema. **Accepted scoped counterexample and
finite-energy-domain statement.** I read only the pinned ROOT_DERIVATION.md
for this new argument and independently reconstructed its inequalities,
constraint accounting and asymptotics. No new author or metric_intake proof
was read. No numerical experiment was run. No source correction is required.

## Global growth and exact energy increment

The elementary bounds 2s<=sqrt(a²+4s²)<=a+2s give
s-a/2<=b(s,a)<=s. Their integrals yield the first two quadratic bounds.
Subtracting s²/4-a²/4 from the lower quadratic expression gives
(s-a)²/4, proving the stronger lower bound. W>=0 follows separately from
b>=0. These are global inequalities valid at large gradients, not a
small-gradient extrapolation.

On the fixed finite interval with bounded a, v²<=4W(|v|,a)+a² proves
that finite field energy requires v in L2; W<=v²/2 proves sufficiency.
Since the background g is bounded and hence L2, the perturbed field has
finite energy exactly when psi_x is L2. Within the specified absolutely
continuous zero-wall class this is exactly H1_0. The statement concerns
the fixed-scale, fixed-density slice; it is not a classification of the
entire nonlinear matter/scale theory.

For psi in X_A, psi is bounded and psi_x is L1. Thus B psi_x and rho psi
are ordinary integrable quantities. Integration by parts using B_x=C rho
and the actual zero endpoint values gives the stated exact cancellation.
The fluid internal energy and scale energy are unchanged on this slice,
and the matter interaction changes by integral rho psi **once**. Consequently
equation (2) is the exact full static increment, including that interaction.
The signed-gradient convex tangent subtraction is nonnegative pointwise.
When the new field energy is infinite, only finite quantities have been
subtracted, so no undefined cancellation of infinities is present.

This is an energy-functional calculation off equilibrium; the new states
need not themselves solve the static equations. The source equation is
used for the fixed background. Replacing its MOND flux B by g would alter
the cancellation and is not permissible.

## Singular weighted direction and optional density path

The chosen P can be adjusted away from zero because a nonzero smooth
off-center bump has a finite positive integral against1/A. That adjustment
does not change its nonzero center value. Then psi'=P/A is L1, its weighted
square is integrable, and its unweighted square is not: near the center
P²/A² has a nonzero multiple of1/|x|. Its primitive has both zero outer
traces and belongs to X_A. Hence (0,psi,0) is in the linear form domain.

For every nonzero epsilon, g+epsilon psi_x cannot be L2, since otherwise
subtracting g and dividing by epsilon would make psi_x L2. The exact energy
increment is therefore infinite while the scaled V norm tends to zero.
No V-neighborhood of the background is a finite-valued exact-energy domain.

The optional coupled construction also checks. With c the weighted mean
of psi and d=rho(c-psi)/cs², d is bounded and has zero integral, its
displacement has zero traces, and h=cs²d/rho+psi=c is constant. The scale
component is zero and the same P meets the operator-domain flux conditions.
The Eulerian path rho+epsilon d stays uniformly positive for small epsilon,
since d/rho is bounded, and preserves total mass exactly. Its internal and
interaction terms remain finite. The unchanged singular field direction
still gives infinite exact field energy. The source explicitly and correctly
does not identify this additive density path with a finite material map.

## Dimensionful smooth concentration family

For beta=3/8 and the prescribed dimensional prefactors, change variables
x=L_ref delta y. Direct differentiation and integration give

    ||h_delta||²=(Psi_ref²/L_ref) I0 delta^(-1/4),
    ||psi_delta||²=Psi_ref² L_ref integral f² delta^(7/4).

Using A(x)~A_*sqrt(|x|) gives

    Q[0,psi_delta,0]
       =(Psi_ref² A_*/(C sqrt(L_ref))) I1 delta^(1/4)(1+o(1)).

The square-root weight convergence is dominated uniformly on the fixed
bump support by a constant times sqrt(|y|). Thus the leading coefficient,
including the factor1/sqrt(L_ref), is justified by integration rather than
formal pointwise substitution alone. Nonzero compactly supported f makes
both I0 and I1 positive. The V norm tends to zero; the unweighted gradient
norm diverges. The perturbations themselves are smooth and finite-energy
for every fixed positive delta.

The units also check. A is dimensionless, so A_* has inverse-square-root
length units. Both Psi_ref² A_*/(C sqrt(L_ref)) and Psi_ref²/(C L_ref)
have energy per transverse-area units. Delta is dimensionless. No physical
coupling or reference normalization is retuned along this family.

For the exact energy, write W(s,a)=s²/2+error with absolute error at most
as/2. Expanding |g+h_delta|² gives the leading integral h_delta²/2,
plus the listed g h_delta and g² terms. The bound on the W error also
contains integral a|g|=O(delta^(3/2)); this is absorbed by the displayed
O(delta^beta) estimate since beta=3/8. The other listed orders follow from
g=O(sqrt(|x|)), B=O(x), W(|g|,a)=O(|x|^(3/2)) and the compact support.
All those errors are negligible compared with delta^(-1/4).

It follows that the exact increment has the stated leading coefficient

    DeltaE=(Psi_ref² I0/(2 C L_ref)) delta^(-1/4)(1+o(1)).

The matter/source linear cancellation remains exact during this comparison.
Using the deep cubic energy for h_delta would be invalid because its
gradient amplitude grows rather than remaining uniformly deep-MOND.

## Precise consequence and surviving scope

With the stated convention Q=d²E and H2=Q/2, the ratio is explicitly

    DeltaE/(Q/2)
       ~ [I0/(A_*sqrt(L_ref) I1)] delta^(-1/2).

Thus exact energy is discontinuous at the background in the V topology,
even when the approaching sequence is restricted to smooth finite-energy
states. It cannot satisfy a local finite upper bound by KQ or a uniform
little-o quadratic Taylor remainder in that topology. Together with the
singular direction, this is a decisive failure of the proposed bare weighted
space as a nonlinear finite-action neighborhood, not an untested numerical
possibility.

The construction does not give evolution from small exact-energy data:
the smooth sequence has diverging exact energy and is not small in H1.
It therefore establishes no dynamical growth, ghost, nonlinear instability
or ill-posedness. The completed positive linear form, its transmission
operator and conservative linear evolution from FGF036 remain valid as
linear constructions.

Finite exact energy on this slice requires H1, but this proof supplies
neither a twice-Frechet Taylor theorem there nor preservation of H1 by the
weighted linear flow, a nonlinear solution map or a Cauchy theorem. Any
continuation must explicitly change and audit the nonlinear domain or
mechanism. Separate reference normalizations and history choices remain
separate backgrounds; no RAR/M/filtered-MONO, measured cluster, metric/photon,
gravitational-degree count or physical-theory closure follows.
