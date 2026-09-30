# Exact radial closure and finite source-exterior tests

Verdict: the stated necessary radial vacuum system has been symbolically
closed and numerically integrated in finite examples. This is not a complete
source/cosmology solution or a derivation of 32π. Self-review, based on
5a027c670a and the action in EXPANSION_BRIDGE_RESULTS.md. No independent
referee or full covariant completeness check is claimed.

## Exact first-order system

Let B=lambda−1>0, S=3lambda−1, w=V/N, W=w/r,
theta=Theta>0 and u=U/M². Write

    a=P+3beta P²/(2theta), n=N'/N=exp(sigma)a,
    ctheta=B+2beta P³/theta³.

The radial metric combination (E_sigma−V E_V)/(r²N exp(sigma)),
verified directly by action variation, yields the algebraic constraint

    C=B theta²/2−2theta W−3W²
      +(1−exp(−2sigma))/r²−2exp(−sigma)a/r
      −P²−u−2beta P³/theta=0.

Subtracting it from the lapse equation gives exactly

    sigma'+n=r exp(sigma)(P'+2P/r).

The shift equation consequently becomes

    ctheta theta'=[3beta P²/theta²−2rW exp(sigma)]P'
                  −4W exp(sigma)P.

The trace definition gives

    W'=−theta/r−W[r exp(sigma)P'+2exp(sigma)P+3/r].

Together with n and the algebraic constraint, these supply a closed radial
system away from the additional denominator identified below. They satisfy
the necessary reduced lapse, shift, radial-metric and polarization equations.
This does not verify the angular/foliation equations omitted by the symmetry
reduction, a matter interior, or perturbative/nonlinear health.

For a cancellation-resistant derivative formula define t=exp(−sigma),
rest=B theta²/2−2theta W−3W²−P²−u−2beta P³/theta,
and let C_theta and C_W denote partial derivatives of C. Set

    tk=[3beta P²/theta²−2rW exp(sigma)]/ctheta,
    t0=−4W exp(sigma)P/ctheta,
    W0=−theta/r−W[2exp(sigma)P+3/r],

    D=−6beta tP/(theta r)−3beta P²/theta
      +2r exp(sigma)W(theta+3W)+C_theta tk,

    R=−6beta tP²/(theta r²)
      +2a[P−3beta P²/(2theta)]/r+2rest/r+C_W W0+C_theta t0.

Direct differentiation proves

    C'=D P'+R−2C/r.

Thus P'=−R/D preserves C=0; a small constraint error satisfies C'=−2C/r
in exact arithmetic. Three independent symbolic expressions are checked in
expansion_bridge_radial_identity.py: radial combination, gradient identity
and this derivative closure. They are algebraic checks by the same author,
not an independent full-theory audit.

## Numerical stabilization and declared example

The finite run uses H=1, beta=10, lambda=2, u=7.5, and labels the initial
flux by GM=1e−16. Units measure lengths in 1/H and accelerations in H.
This beta was chosen before the run and does not impose 32π: its conditional
ratio is 75. The mass label is not yet matched to a conserved material mass.

At r0=1e−6 choose P0=sqrt((2H/beta)GM)/r0, W0=−H and theta0=3H.
Solve C=0 for exp(−sigma0) using its positive quadratic root. The lapse
normalization is an arbitrary constant at this stage; orbital acceleration
depends on its logarithmic derivative, not that constant.

An exploratory direct evaluation suffered cancellation in
(1−exp(−2sigma))/r² and in large derivative terms. That is a numerical
implementation issue, not evidence of a physical singularity. The final script
uses expm1, a rationalized initial root and log1p; it evolves deltaW=W+H and
deltaTheta=theta−3H and subtracts the vacuum terms analytically. In particular,

    rest=H S deltaTheta+B deltaTheta²/2
         −2deltaTheta deltaW−3deltaW²−P²−2beta P³/theta.

This stabilization is exact for u=3SH²/2. The bounded run pins the final
implementation and its output. The earlier unpinned exploratory implementation
was superseded; no claim relies on its inaccurate constraint residual.

## Positive local result, with its precise scope

Two DOP853 integrations cover r=1e−6 to 1e−5, sampled at 64 logarithmic
points; the tighter run halves maximum log-radius step and tightens tolerances.
In this annulus P and theta stay positive and the metric is in its static
timelike domain. The reconstructed orbit acceleration uses the actual metric:

    g_orbit=n−exp(2sigma)w(sigma'w+w')/[1−exp(2sigma)w²].

The reduced comparison is GM/r²+sqrt((2H/beta)GM)/r. Its de Sitter background
term is −H²r, so the comparison below subtracts that known background rather
than interpreting it as a failure of the galaxy scale.

The finite output gives:

* maximum normalized lapse residual 8.33e−16 and shift residual 3.77e−17;
* maximum fractional drift of the effective flux r²(3beta P²/(2theta))/GM,
  1.296e−6;
* maximum relative difference between g_orbit+H²r and the reduced force,
  6.57e−7;
* maximum relative P difference between the two tolerances, below 1.7e−15.

These finite diagnostics support the local reduction for this initial-value
example. They do not establish a uniform approximation theorem, real galaxy
fit, interior source equilibrium, measured Newton constant or global matching.
The residuals are evaluated through different expressions of the same derived
system; their smallness is not an independent proof of covariant completeness.

## New global bottleneck and boundary-data sensitivity

Extend the same initial data toward r=0.01. Stop before D=0 at successive
D cutoffs −1e−4, −1e−5 and −1e−6. The stopping radii converge numerically
near 0.00107213585. The compatibility numerator R approaches approximately
−4.2536e−4, while P' changes from −4.25 to −42.5 to −425.4.
Theta remains positive and the static metric factor is positive, so this
tested event is not simply the theta pole or a metric horizon.

At D=0, a differentiable solution of this radial system requires R=0.
The finite evidence is consistent with a nonregular continuation of these
particular initial data. No exact singularity theorem or global exclusion is
claimed from three cutoffs. It identifies a concrete shooting condition that
was absent from the reduced MOND calculation.

Now change only the initial trace datum to

    deltaTheta0=factor beta P0³/[9(lambda−1)],

and resolve the initial metric constraint. Factors 0.5,1,2 all reach r=0.01
without triggering the −1e−5 denominator cutoff. Their outer P values are
about 1.115e−4, 1.139e−4 and 1.179e−4, respectively, with theta near
3.000003. They are not the decaying reduced profile (which would have
P about 4.47e−7 there), and no cosmological boundary is satisfied merely by
reaching the endpoint. Initial changes of order 1e−7 in theta substantially
alter the outer branch while leaving the local weak geometry close to vacuum.

This prevents treating the first near-fold trajectory as an exclusion of
the entire action. It also prevents declaring that regularity has selected
beta. Boundary data remain active physical unknowns.

## Next concrete research test

Shoot on the initial trace/shift data to seek D=R=0 compatibility and a
decaying cosmological branch, then verify all remaining equations and match
a conserved source interior. Holding beta fixed in that shooting test
distinguishes a boundary-data condition from an actual coupling selector.
If regular solutions exist for a continuum of beta, regularity cannot supply
32π; if a discrete value appears, it must survive changes of source mass,
interior and horizon conditions before being promoted to a physical result.
Vacuum-offset protection and causal/dynamical health remain separate unfinished
obligations. The original goal remains open.
