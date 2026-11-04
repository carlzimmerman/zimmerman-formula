# Independent KT38 Solar derivation review

Verdict: the new beta-product derivatives, scaled scalar derivatives,
finite-core contact powers and fixed-eta/lambda Gaussian STF limit in
`../cassini/DERIVATION.md` are correct as written. This is a read-only
analytic review, not a second Solar numerical run or a claim for arbitrary
regulators.

Recomputed beta=2lambda²s, beta'=2lambda²s', beta''=2lambda²s'' and both
product derivatives of D=beta*xR'. The stated D'' contains every beta',
beta'', x'', z'', and squared-z' term. The scaled identities follow from
R'=Q'/z-Q/z² and successive differentiation; E',E'' retain their exact
product-rule meanings, not derivatives of f alone.

For the core, z>=4lambda⁴g⁴/r⁴ and s<=sqrt(z) imply
D_xx=O(lambda² z^-2). After the angular cancellations the three radial
bounds are r^9/g^7, r^13/g^11 and |gp-gt|r^6/g^6, with the displayed
lambda powers. Gaussian rescaling g=sigma^-2 f(r/sigma) gives sigma^23,
sigma^35,sigma^15; the rescaled integrands are O(v²) at zero and grow as
v^23,v^35,v^15 at infinity. This proves the uniform delta powers23,35,15
for sigma<=delta. The decreasing enclosed mean density supplies the
uniform high-z threshold over the entire core. Contacts scale as k^-5
lambda^-6=sigma^15 lambda^-6. The exterior B tail is r^-15 because beta
now supplies an extra r^-6; the A tail stays r^-7.

Together with the inherited angular Green/contact identities and compact
exterior convergence, these steps prove the stated Gaussian STF limit for
fixed positive eta and lambda. They do not define nonlinear products of
point-source distributions or interchange the lambda and source-width
limits. All original qualifications are retained.

Reviewer: response_obstruction. Reviewed-file SHA256 pins:

* `rebuild_2026_10_22/KT38_weak_field_curvature/cassini/DERIVATION.md`: `f88a03a66e95f64e0a06228b73da3514f7fb26d0c1a8ea7e27bc6a586d1e05b9`
* `rebuild_2026_10_22/KT38_weak_field_curvature/analytic/law.py`: `06ce3b23eebb90093d9cb1ef5dee650e370baa0ca29f5524838eeef6ac23f263`
* `rebuild_2026_10_22/KT37_generalized_action/cassini/DERIVATION.md`: `921a0313a4a9e8dd20f37061ccd116bd0ad26358d1178b01b169bfe345d98904`
* `rebuild_2026_10_22/KT37_generalized_action/cassini/REGULARIZATION_PROOF.md`: `e908b73a1b11c74bb31494f5413113a40a7607ffd3ec7b886ce75997a649f6d4`
