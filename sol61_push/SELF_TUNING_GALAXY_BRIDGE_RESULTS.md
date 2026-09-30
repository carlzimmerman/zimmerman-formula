# Self-tuning is a possible vacuum repair, but needs a different galaxy bridge

Status: primary-source extraction plus a restricted algebraic compatibility
test. This is not a constructed theory or a derivation of 32π.

## Authenticated source and boundary

Stephen Appleby and Eric V. Linder, *The Well-Tempered Cosmological Constant:
The Horndeski Variations*, arXiv:2009.01720v1, 3 September 2020,
https://arxiv.org/html/2009.01720v1, checked 30 September 2026.
The arXiv-rendered text identifies its version. Sections 2 and 5.1 were read.
No PDF was retained or literature cache initialized.

Their Eq. (11) imposes degeneracy at an arbitrary specified H_c; Eqs.
(12)–(14) additionally require scalar dependence in the Friedmann constraint
and nonzero evolution coefficients. Their example, Eqs. (61)–(69), contains
H_c in action functions. On shell, phi=c0+c1 exp(3H_c t); its constraint is

    V+(T−3H_c²M)c0−3H_c²Mpl²+6√2 H_c s=0.

Here V translates the paper's Lambda (vacuum energy density), T its lambda³,
and the project's curvature Lambda is 3H_c². The authors discuss future
gradient instability and a growing effective Planck mass for portions of this
example in Sec. 5.1. This source supports classical vacuum cancellation, not
a predicted galaxy coefficient. No stability claim for a combined theory is
imported.

Search boundary: arXiv primary text plus a SciSpace semantic query about
well-tempered tadpole scalars coupled to galaxy polarization. SciSpace found
the original 2018 well-tempering paper, among other candidates; those additional
full texts were not checked. This is an adjacent-result check, not a novelty
survey or exclusion of all self-tuning models.

## New project application: a direct linear bridge fails the shift test

The source motivates testing vacuum cancellation via an additive scalar shift.
For a minimally coupled tadpole sector take a schematic nondifferentiated
Lagrangian, with T nonzero,

    L = −V−T phi−Kc phi P³.

Derivative-only terms are invariant under a constant phi shift. The simultaneous
transformation phi→phi+epsilon, V→V−T epsilon cancels the change in the first
two terms exactly. The galaxy term changes by

    delta L = −Kc epsilon P³.

Thus identifying the vacuum-canceling scalar directly with the coefficient of
our cubic galaxy operator destroys this simple vacuum-shift equivalence when
P is nonzero. This is a local action identity, not proof that no more elaborate
combined equations can self-tune. Nonminimal curvature couplings can also
change the shift dictionary; the source example's constraint responds by
delta c0=−delta V/(T−3H_c²M), provided that denominator is nonzero.

More generally replace phi in the galaxy coefficient by a smooth f(phi).
Exact invariance under every constant shift, with no compensating changes to
other couplings, requires f(phi+epsilon)=f(phi). Differentiating at epsilon=0
gives f'=0 on each connected field domain. Therefore such a coefficient must
be constant. Treating its change as a boundary term would require a separate
identity: the cubic polarization operator in our action has nonzero local
field variation and is not supplied as a topological density.

There is a second concern on the checked rolling background. For a linear
coefficient Kc phi its time derivative is 3H_c Kc c1 exp(3H_c t). Except for
a constant-field special case, the bare galaxy coefficient evolves. Assuming
a fixed local Newton dictionary and identifying a0bare with its inverse would
then give d ln(a0bare)/dt=−phi_dot/phi wherever phi is nonzero. Those dictionary
assumptions are unproved for this extension; the formula is a warning about
the direct identification, not an observational exclusion.

## What survives as a research route

A coefficient depending on shift-invariant quantities such as X=−(∂phi)²/2
passes this particular algebraic shift test. It still modifies the field
equations and must be included when deriving degeneracy, source matching,
and stability. Passing the symmetry test does not choose that function or
its normalization. Keeping a separate galaxy scalar instead also passes this
test, but retains the independent galaxy coupling already exposed in
VACUUM_OFFSET_SELECTION_RESULTS.md.

This changes the next action: test a shift-invariant derivative bridge in a
single action and derive its constraints, rather than importing vacuum
cancellation and retaining an unprotected linear galaxy coefficient. The
construction must still select H_c/a0=√(32π/3) without assigning that ratio as
an action parameter. The checked source does not supply this relation.

## Reproducible finite verification

self_tuning_galaxy_bridge.py checks six exact SymPy identities. Its contract
and bounded-run manifest record the script, output, software and execution.
The functional invariance argument above is analytic, not established by
sampling. No nonlinear trajectory, galaxy solution, or new observational test
was performed.
