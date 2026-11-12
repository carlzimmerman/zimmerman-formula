# Positive-baryon bounds and the limit of adding gravitational observables

Phase-2 root route, 12 November 2026. Publication base 8db464d4bc; actual input checkout cace4617bb6a518bf910b56a4c0ee8bddce7fa07. Exact input paths/hashes are in input.json. Status: restricted analytic bounds independently audited; deterministic interval feasibility evaluated, with no likelihood or statistical exclusion claim.

## 1. What survives arbitrary stellar gradients

Let r>0, g(r)>0 be a differentiable radial gravitational acceleration of an isolated spherical system, and a=a₀≥0. Let M_d=r²g/G denote a force-equivalent mass, not a baryonic mass. For either specified pointwise law, its inverse determines a baryonic mass M_b(r;a). A necessary physical condition is dM_b/dr≥0. This concerns actual baryons, not signed effective/phantom density.

For simple-μ,

    g_b=g²/(g+a),    M_b=r²g²/[G(g+a)].

With s=d ln g/d ln r,

    d ln M_b/d ln r = [(2+s)g+2(1+s)a]/(g+a).

Thus for −2<s<−1,

    a ≤ g(2+s)/[−2(1+s)].

For the quadratic law g²=g_b²+a g_b,

    sign(dM_b/dr) = sign[(2+s)g_b+(1+s)a],
    a ≤ g(2+s)/sqrt(−1−s),    −2<s<−1.

At s≥−1 neither condition supplies an upper bound on a. At s=−2 only a=0 can have nonnegative baryonic density; s<−2 violates positivity even in the Newtonian limit. These statements are scoped to the assumptions, and do not apply to an external-field-dominated, nonspherical or different modified-inertia system.

This identifies a measurement regime where arbitrary positive M/L cannot absorb every a₀: a sufficiently steep declining force. Flat circular speed has s=−1 and remains degenerate. Merely adding precise measurements in that limit does not fix the problem.

An independently established lower bound g_min=GM_min(<r)/r² on the spherical baryonic acceleration gives another one-sided condition:

    simple-μ: a ≤ g²/g_min − g;
    quadratic: a ≤ g²/g_min − g_min.

A negative right-hand side means that the stated baryon lower bound already exceeds the allowed mass. These are conditional lower-bound tests, not claims that Euclid photometry or a gas conversion factor alone supplies g_min. Disk force geometry cannot be replaced silently by GM/r².

## 2. A derivative-free shell test

Let r₂>r₁, M₂>M₁ be two force-equivalent masses and g_i=GM_i/r_i². If M₂/r₂<M₁/r₁, the implied baryon mass eventually decreases as a is increased. For simple-μ the crossing is exactly

    a_crit = g₁g₂(M₂−M₁)/(M₁g₁−M₂g₂).

Nondecreasing baryon mass requires a≤a_crit. For the quadratic law define

    m²=(M₁²r₂²−M₂²r₁²)/(r₂²−r₁²),
    a_crit=g₁(M₁/m−m/M₁).

The same upper-bound interpretation follows. These conditions avoid numerically differentiating an uncertain mass profile. They still need a joint error treatment before any inference about a measured galaxy.

Independent derivation, hypotheses and edge cases are recorded in the portal agent's POSITIVITY_AUDIT.md. The script checks the crossing and its sign on both sides for all finite eligible pairs among 13 radii.

## 3. DESI central values illustrate the test, but do not establish an exclusion

We use the 13 all-tracer calibrated values at 20–80kpc from [DESI DR2 Milky Way Table 4](https://arxiv.org/html/2611.05518v1#S6.SS1), copied from the existing DW1 implementation and checked against the primary table. They are inferred force/mass proxies with tracer, calibration and dynamical assumptions. No NFW-extrapolated M200 is used as an extra datum. The radial covariance is unavailable here.

The central values' tightest finite-shell bound occurs at 75–80kpc: 8.7118×10⁻¹²m/s² for simple-μ and 1.1745×10⁻¹¹m/s² for the quadratic law. Therefore those central curves imply decreasing baryonic mass in some shells when a₀ is fixed at either canonical or alternative footing. This is a property of the central proxy curve, **not a calibrated physical exclusion**.

To show the uncertainty limitation without inventing a covariance, transform each marginal interval into an allowed M_b interval at fixed a₀. A nondecreasing sequence exists exactly when every upper interval endpoint exceeds the running maximum of preceding lower endpoints. The code constructs a witness and transforms it back to the original mass intervals. This is a feasibility calculation; interval expansion is not a Gaussian significance or joint confidence region.

| Law | a₀, m/s² | Minimum common multiplier of quoted marginal half-widths permitting a monotone baryon sequence |
|---|---:|---:|
| Simple-μ |9.36e−11|0.59365|
| Simple-μ |1.13e−10|0.64264|
| Quadratic |9.36e−11|0.79866|
| Quadratic |1.13e−10|0.85426|

All four therefore admit a witness inside the displayed marginal intervals. These witnesses are not a measured stellar/gas distribution and need not lie in a high-probability region of the unknown joint posterior. Conversely, selecting a derivative or central shell alone cannot support an exclusion. A statistically meaningful version requires joint profile draws/covariance and the tracer/model uncertainty budget.

## 4. Why lensing cannot automatically break the remaining mass-gradient ambiguity

For any positive a, a spherical flat circular-speed field g=V²/r can be supported under simple-μ by

    M_b^(a)(<r)=V⁴r/[G(V²+ar)],
    dM_b^(a)/dr=V⁶/[G(V²+ar)²]>0.

Every member has the same g. If a specified no-slip metric completion makes the entire relevant metric identical—including its exterior/light-path continuation—then rotation, stellar orbital dynamics, lens deflection and gravitational redshift cannot distinguish these members. Adjusting a positive radial stellar M/L can preserve the observed luminosity profile as well.

This is a constructive local-galaxy identifiability obstruction. Matching g only at a few radii is insufficient to claim equal lensing, since deflection integrates over the light path; the counterexample uses the full common field. It does not rule out extra information from different metric completions, independently measured baryons, background cosmology or a constrained population law. It explains why more gravitational observables alone cannot universally replace non-gravitational baryon information.

## 5. Relation to the Euclid opportunity and existing work

The new data improve photometric geometry and identify targets. The standard ECLIPSE isothermal slope corresponds, in the spherical GR force interpretation, to s=−1: that imposed model lies precisely on the no-positivity-bound limit. Therefore its fitted slope cannot test the declining-force condition. Flexible profile reconstruction, a declared metric law and uncertainty propagation are necessary. A Sérsic light index is not an independent measurement of gravitational force slope.

This route reuses the positive flat-curve family from phase 1 and the published DW1 profile. Its additional content is the explicit local/finite-shell positivity boundary and interval-feasibility implementation. No broad literature novelty is asserted. The November 12 correction that distinguishes local density slope from mean enclosed-density slope remains in force.

## Computation and continuation

positivity_checks.py evaluates 5 symbolic identities, 78 shell pairs, 4 fixed-law/footing cases and 500 flat-family force-reconstruction points. run01/manifest.json is completed and validated. Floating tolerances check algebraic implementation; no observational likelihood, detection threshold or new theory pass is scored.

Next independent input: a covariance-aware force profile and constrained baryonic floor, or a specified nonspherical/external-field completion to which the spherical inverse does not apply. Repeating the central-curve calculation cannot replace those inputs.
