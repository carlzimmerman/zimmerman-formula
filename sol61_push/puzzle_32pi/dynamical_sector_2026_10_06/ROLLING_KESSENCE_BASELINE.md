# Rolling k-essence baseline: a vacuum critical point is not a healthy MOND bridge

Base `81af81ba8a7207bca2bc4f13375c757feee7afcd`. This baseline supplies a concrete reference for the braiding escape. It concerns a minimally coupled shift-symmetric P(X) scalar, a constant independent vacuum density and Einstein gravity with positive coefficient K_E. Signature (−,+,...,+), c=1, d=n+1, n≥2, X=−(∂φ)²/2. It is not a no-go for braiding, higher derivatives, extra matter exchange or nonminimal gravity.

## Exact vacuum obstruction

For a homogeneous timelike scalar q=φdot≠0,

    ρφ=2X P_X−P, pφ=P,
    [a^n P_X q]dot=0,
    n(n−1)K_E H²/2=ρ_v+2X P_X−P,
    −(n−1)K_E Hdot=2X P_X.

An exact expanding de Sitter phase with constant vacuum therefore requires P_X=0 throughout its visited X values. Its scalar energy is −P(X). At an isolated root X₀, this is a fixed chosen action value and H changes when ρ_v changes. If a continuous root branch X₀(ρ_v) is invoked to keep H fixed while absorbing a continuously variable vacuum, P_X=0 along that branch makes P constant on its connected image. It cannot absorb the changing density. Time-dependent q on a connected zero-current plateau similarly has constant P. Disconnected roots can give distinct discrete branches, not a smooth adjustment to every vacuum shift.

Thus minimal rolling P(X) cannot self-adjust to the same exact H for an open interval of vacuum densities by this mechanism. A stationary q=0 endpoint or nonsmooth action lies outside the regular timelike assumptions and needs separate variation.

## Local static scalar block near that rolling state

Freeze a locally flat metric and q, and let φ=qt+ψ(r), u=ψ′ signed. This is a principal scalar-sector control, **not** a solved Einstein lapse/metric problem on de Sitter. Its X=X₀−u²/2. For C² P at the rolling critical point,

    P_X(X₀−u²/2)=−P_XX(X₀)u²/2+o(u²),
    P=P(X₀)+P_XX(X₀)u⁴/8+o(u⁴).

For a linear local source obtained, for example, by freezing a conformal massive worldline coupling at an epoch, the radial current outside that smooth source is

    r^(n−1) P_X u=αM/Ω_(n−1).

The conformal coupling changes particle masses over the rolling background and breaks the scalar shift symmetry where particles are present; it is not silently part of the source-free vacuum cancellation. This frozen equation checks a mass-normalized local response only. A physical global source/test metric, time evolution and its stress conservation dictionary remain necessary.

If P_XX(X₀)≠0, the leading current is cubic in u. Its formal radial solution has |u| proportional to M^(1/3)r^(−(n−1)/3), rather than the MOND M^(1/2)r^(−(n−1)/2). In four dimensions this gives r^(−2/3), not 1/r.

There is a stronger sign mismatch in the same frozen block. The temporal and static longitudinal/tangential principal coefficients are

    K_t=P_X+q²P_XX,
    K_r=P_X−u²P_XX,
    K_perp=P_X.

The quadratic action also contains −quP_XX δφdot ∂rδφ; it must be retained in a full characteristic calculation. At u=0, finite positive temporal kinetic energy requires P_XX(X₀)>0, since K_t=2X₀P_XX. For sufficiently small nonzero u, K_perp≈−P_XXu²/2 and K_r≈−3P_XXu²/2 are both negative. In the locally timelike tilted state, the scalar-rest-frame temporal coefficient is P_X+2XP_XX>0 while P_X<0, so the scalar principal symbol fails its ordinary hyperbolic positive-gradient test; the mixed term does not repair this sign. The formal attractive branch for a positive source α>0 would instead require the opposite sign, which gives a temporal ghost at the rolling state. A vanishing P_XX gives no finite nonzero quadratic temporal coefficient and requires a separate higher-order analysis.

This does not prove instability of a gravity-completed ghost-condensate model: lapse/shift mixing and stabilizing higher-spatial-derivative terms alter the complete operator. It does prove that the displayed regular minimal scalar block does not simultaneously supply a finite healthy temporal Hessian and a MOND static law. Restoring a positive linear static term gives the regular-response crossover of REGULAR_RESPONSE_SCREEN.md rather than an exact arbitrarily weak-source MOND branch.

## Trying to put the cubic directly at X₀

On the side X<X₀, choose

    P=P₀−B(X₀−X)^(3/2), B>0.

Then P_X=(3B/2)sqrt(X₀−X) and P_X u=(3B/(2sqrt2))u|u|, which is precisely a deep MOND-type scalar flux. But

    P_XX=−3B/[4sqrt(X₀−X)].

For q≠0, X₀>0, the coordinate temporal coefficient P_X+q²P_XX diverges negatively as u→0. This action is not C² at the rolling background and supplies no ordinary finite healthy quadratic time action there. Choosing the opposite sign repairs that sign only by reversing the static flux/stiffness. Taking X₀=0 removes the nonzero rolling clock and is a different branch.

The precise surviving route is therefore a **complete** derivative/mixing theory that changes these equations or principal coefficients and supplies its own source-mass/radius law. Kinetic braiding is being tested as that genuine escape, rather than treating a derivative bridge as an inert coefficient replacement. No 32π ratio has been inserted or selected by the baseline.

The exact controls in rolling_kessence_checks.py corroborate constant critical-vacuum energy, local exponents, Hessian signs and the shifted-cubic divergence. They do not solve cosmological galaxy matching, prove full constrained health or exclude all scalar-tensor theories.
