# Self-review of FD (not independent review)

Primary verdict for the passive-outlet proposition in MECHANISM.md: **proved
as written**, under its explicit positivity, initial-energy and single-port
passivity assumptions. Primary verdict for a successful galaxy-formation
mechanism: **incomplete**. The smallest missing implication is transfer of the
actual material infall energy into outgoing modes in the unrestricted dynamics.

Dependencies and obligations:

| Obligation | Evidence | Verdict |
|---|---|---|
| Material continuity and convective source | integration by parts; FD-04 independent knot-split integration | passed for stated continuum manifold |
| Reciprocal connection signs and cancellation | direct variation of L=-C_a qdot^a | passed |
| Positive scalar added inertia | radial Green kernel and integral M(r)^2/r² | passed at quasistatic order |
| Original energy and units | reused FreeVacuum, rM conversion, endpoint energy reproduction | passed on inherited grid |
| Actual front-minimum branch | V_R root, positive sampled V_RR, cap slack | numerical only; conditional density manifold |
| Slow radiation rate | radial outgoing monopole derivation | conditional long-wavelength approximation |
| Self-generated fast front forcing | linear moving-coordinate expansion; full kinetic-stiffness correction in FD-05 | conditional tangent model; no nonlinear feedback |
| Passive bound | norm triangle inequality and induction, including exported energy as a positive coordinate | passed for the proposition |
| Numerical continuous-branch bound | time subdivision and source-grid comparison | not established; source-grid bound grows |
| Exact material/scalar energy and charge in full evolution | no such evolution run this phase | not addressed |
| Filled transition, free reservoir and law as attractor | density/phase restrictions enforce profiles | not established dynamically |
| Virial entropy and universal galaxy scaling | previous failures remain | not resolved |

Adversarial checks changed the implementation rather than the claim:

1. FD-01's traversal quadrature did not resolve the final approach. FD-02 fixes
   it and preserves the superseded run unchanged.
2. Fixed-cell phase quadrature did not exactly satisfy the continuous source
   identity. FD-04 splits both sets of knots and obtains 8.41e-15 relative
   agreement. The old static spatial discretization remains unrefined.
3. FD-03 omitted kinetic corrections to front stiffness. The complete
   correction was derived, measured in FD-04 and included in FD-05. It changes
   peak mode energy only slightly in the tested differences.
4. The bound's growth across source grids prevents claiming a universal
   numerical bound, despite its tiny values for all tested interpolants.
5. The passive theorem cannot be applied to an actively driven second port or
   a time-dependent source coupling without separately tracking that work.

The PCHIP construction emits an overflow warning while forming harmonic means
of extremely small inherited slopes. All reported tensors, roots and energies
are finite; the independent source check passes. This is not a proof of
continuum profile accuracy.

Mathematical proofreading scope: new MECHANISM.md, STATUS.md and this review.
The kinetic stiffness equation was substantively corrected during research;
that correction is explicitly tested by FD-04/05, not classified as a typo.
No inherited mathematical source was edited. The review is local self-review,
not external validation or an independent agent audit.
