# Microscopic vacuum calculation: what was obtained

The numerical vacuum ratio is still unselected. This checkpoint calculates
a radiative stiffness from an explicit particle model, identifies a failure
of its proposed halo portal, and derives a more structured collective-model
relation. The complete gravitating vacuum energy and a viable halo parent
have not been established.

## Strongest new formula: the collective SU(5) model

For the specified renormalizable singlet-plus-two-adjoint model, the
common-threshold leading-log approximation gives

    V_model=f^2 lambda^2/(lambda^2+30h^2),
    g_*^2=(29/200)lambda_*^2,

    B_curv/V_model = 29/[12(16pi^2)^2]
       * h_*^2 lambda_*^2(16h_*^2+13lambda_*^2)
                               /(lambda_*^2+30h_*^2).

Here B_curv=U_ss/9 for s=ln(|T|/v). Both the positive energy and the
curvature come from this model; no scalar-potential B was assigned.
Stationarity fixes g/lambda on the radiative critical surface. The
couplings h and lambda remain inputs, and the field location depends on
RG boundary data. This is a leading-log radial result with explicit
threshold, gravity and portal qualifications, not a full microscopic
derivation of a universal acceleration coefficient.

The SU(5) factors were checked using all 24 explicit generators. Nine
coupling-flow integrations reproduce the formula within 4.30e-7 relatively
and show positive curvature. For h=lambda=1 the ratio is 9.06596e-5.
Across the prescribed h,lambda={0.3,0.6,1} grid it ranges from 7.34342e-7
to 9.06596e-5. No coupling was selected by the old 0.002329458 target.

A useful obstruction remains even inside this approximation: scaling
all dimensionless couplings by t preserves the critical relation and
the tree V_model at fixed f and h/lambda, but scales B_curv/V_model by
t^4. Thus the stationary-vacuum condition has not eliminated parameter
freedom. Refining thresholds could improve the physical model, but cannot
by itself be described as a mechanism selecting the remaining couplings.

Read [INVERTED_HIERARCHY.md](INVERTED_HIERARCHY.md) for definitions,
derivation, accuracy and missing full-spectrum obligations.

## The first fully enumerated spectrum test

The four-superfield O'Raifeartaigh trial yields a calculable one-loop
function c(x;r,y), with

    B_curv/V_model=lambda^2 x0^2 c''(x0)
                              /[9(1+lambda^2 c(x0))].

All nine r,y cases reproduce a metastable radial minimum with positive
transverse tree masses. Independent 65-digit curvature checks agree to
1.52e-11 relatively. However, eight cases encounter a negative-pressure
response before the tested transverse instability cutoff. The ninth has
no pressure-zero in that tested interval and its transverse branch ends.
A stable scalar vacuum is therefore insufficient for the intended matter
closure. See [SPECTRUM_RESULT.md](SPECTRUM_RESULT.md).

The general discriminator derived along the way is

    dP/dln rho=5U_s(U_ss-3U_s)/[9(2U_s+U_ss)].

On a radially stable positive-source branch, positive compressibility
requires U_ss>3U_s. The trial relative-motion portal itself is still an
assumption rather than a prediction of either microscopic superpotential.

## A separate steep-potential route

Massive supersymmetric SU(2) gauge theory with five vectorlike pairs
provides a holomorphic contribution proportional to |X|^3, assuming a
controlled canonical metric and heavy thresholds. It can supply the steep
term needed by the halo pressure. If an orthogonal breaking sector has
decreasing energy with logarithmic slope -a, while the steep sector has
slope b, the conditional stationary ratio is

    B_curv/V=ab/9+(a b_s-b a_s)/[9(a+b)].

This route is not a completed assembly. A simple singlet linear F term
has the wrong one-loop sign for the decreasing contribution. Placing the
terms in the same F direction introduces interference and possible SUSY
zeros. These gaps are explicit in [RG_CONTINUATION.md](RG_CONTINUATION.md).

## Full vacuum energy remains a physical obligation

The supergravity calculation with specified canonical K and W gives a
positive leading F energy. An absent W0, controlled Kahler corrections,
sub-Planckian hierarchy and no extra sectors are assumptions that must
survive matching. Rigid SUSY does not determine a cosmological offset.
The collective model also needs its full gauged thresholds, transverse
quantum stability and infrared dynamics checked. No observational fits or
metastable lifetimes were computed.

All three bounded run records completed and passed 33 named checks. This
includes algebraic identities, finite-spectrum controls and numerical
cross-checks; the count is not a proof certificate. Review is by the author,
with no independent-agent audit. The exact records and hashes are in
[VERIFICATION.json](VERIFICATION.json); the continuation is in
[HANDOFF.md](HANDOFF.md). The prior results and these substantive checkpoints
have been committed and pushed incrementally to origin/main.
