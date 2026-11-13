# Exact scaling and conditional imaging degeneracy

`AqualScaling.lean` proves nine algebraic statements. It introduces no custom
axioms and uses no admitted proof. Lean reports only its standard dependencies
`propext`, `Classical.choice`, and `Quot.sound`.

For the simple-mu AQUAL flux

    F(g,a) = ||g||/(a+||g||) g,

the exact positive homogeneity is

    F(k g,k a) = k F(g,a),  k>0.

For a fixed finite-volume geometry, explicitly linear potential-to-gradient
maps, fixed linear face-normal maps and arbitrary fixed weights, scaling
potential, a0 and source together therefore scales each discrete residual
by k. A zero residual stays zero. Neither spherical symmetry nor a particular
density profile enters. The potential and density have to scale together:
the file also proves a concrete counterexample to scaling the field while
holding a0 fixed. A fixed linear deflection projection scales alpha by k.

This is a certificate of the stated algebra, not proof of a PDE solution's
existence, convergence or observational correctness. The gradient maps must
be linear; fixed nonzero boundary contributions have to be scaled too.
The LOS projection is a linear map hypothesis, not a certified implementation.
The physical domain is a0>0 and nonnegative baryonic density. The algebraic
flux theorem is stronger and permits any real a; Lean's total division for
other real a must not be given a physical interpretation.

The additional general lens-equation theorems establish the following exact
conditional obstruction to identifiability. If the entire reduced deflection
is changed to

    alpha'(theta) = k alpha(theta) + (1-k) theta,

then its lens equation becomes beta'=k beta. If the source is redefined by
S'(beta')=S(beta'/k), the predicted surface brightness is unchanged. This
requires k nonzero; the AQUAL physical application takes k positive. If the
original total deflection is alpha_gal+kappa_ext theta, the corresponding
external convergence is

    kappa_ext' = k kappa_ext + 1-k.

Consequently the *joint* family M'=k M, a0'=k a0, a scaled galaxy potential,
the stated external mass sheet, and the stated source rescaling can preserve
image brightness for the unscreened fixed-geometry branch. Scaling stellar
mass and a0 alone does not preserve images. The theorem does not say every
transformed convergence, mass, source or boundary condition satisfies the
physical priors. Independent stellar-mass/IMF constraints, external-convergence
information, source priors and other observables can constrain the family.
For positive k and the postulate a0=C sqrt(rho_DE), the file also verifies
that rho_DE'=k²rho_DE gives a0'=k a0. This does not derive the postulate or its
coefficient, and does not establish that the full screened v3s action has the
same scaling: its fixed density/length scales require separate analysis.
The density relation alone also does not assert that cosmological distances
remain fixed if the physical dark-energy density is varied; the lensing
scaling theorem explicitly keeps the lens geometry fixed.

This is not a novelty claim, a breakthrough claim, or an empirical pass/fail
certificate. Its role in FOR J0332 is to make an exact model degeneracy and
the assumptions that can break it explicit.

## Reproduce and inspect

From the repository root:

    python3 euclid_for_j0332_fit_2026_11_13/formal/verify_certificate.py

This invokes the existing canonical project's `lake env lean` using an
absolute path to the new file; it does not edit the canonical Lean project.
It records actual compiler/version logs, input SHA-256 values before and
after, execution results, and a deliberately false degree-two flux mutation.
The mutation is an expected compile failure and is not a certified theorem.
The accepted file must compile without `sorryAx`; the mutation must fail.

The proof dependency graph is norm scaling and real-field cancellation ->
flux homogeneity -> linear maps and finite sums -> residual/solution scaling;
linear projection -> deflection scaling; vector-module algebra -> transformed
lens equation -> inverse scalar cancellation -> identical brightness. The
vacuum-density statement uses the real square-root multiplication identity.

Self-audit checked zero field, empty face sets, arbitrary signed geometric
weights, positivity/nonzero scale assumptions, homogeneous boundary data,
and the distinction between changed deflections and unchanged images after
the additional mass sheet/source transformation. The root independently
reviewed the original flux/FV hypotheses and was asked to review the extensions.
