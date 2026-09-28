# MS1 intake: coupled-mode candidate, restricted background, audit pending

Origin: actual Astra agent `/root/proof_precision`, not a DeepSeek run.
Raw evidence stays in `campaign_fresh_gravity_astra/stage_04/matter_stability/`.
The coordinator validated the final run_003 manifest and read the result and
follow-up equations. The full first-order eigenvalue and ODE code has not been
independently audited by the coordinator.

The coordinator independently eliminated the linear density and scalar
perturbations. With x=omega², s=cs² k², A=c² lambda_eff k²/K and
J=4piG rho0 c² k²/K, the polynomial is

    x²-(A+s)x+As-J=0.

Its discriminant (A-s)²+4J is positive; the lower root is negative precisely
when cs² lambda_eff k²<4piG rho0. This confirms the threshold and its
independence of K under the declared positive-parameter assumptions. It does
not establish that a uniform matter background is a physical solution.

The report explicitly supplies a supported, mean-subtracted background for
that calculation. For a genuine hydrostatic isothermal slab, the separate
equations cs² rho'=-rho g and b'(g)g'=4piG rho yield

    Lrho=cs²/g, Lg=g b'(g)/(4piG rho),
    kJ² Lrho Lg=1.

Since min(Lrho,Lg)<=sqrt(Lrho Lg), k<kJ implies
k min(Lrho,Lg)<1. Thus a locally homogeneous unstable-mode interpretation
cannot be justified by a slowly varying patch in this particular slab. This
is a limitation of that approximation, not global stability of the slab.

Disposition: `candidate_received; provenance_validated; limited_algebra_checked`.
The growth-maximum formula, complete finite computation, proposed boundary
quadratic form and physical interpretation need the independent FGF-011 audit.
The worker's passing checks are retained as reported finite evidence, not
promoted wholesale by this intake. FGF-011 is released as an audit of a
candidate, not a downstream assumption that the candidate is fully accepted.
