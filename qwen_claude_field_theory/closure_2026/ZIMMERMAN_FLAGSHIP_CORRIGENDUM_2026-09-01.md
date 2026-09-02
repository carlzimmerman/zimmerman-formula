# Corrigendum and stronger reframing: the variational-causality trilemma

This corrects the central theorem claim in `ZIMMERMAN_FLAGSHIP_2026.md` and the associated nonlocal-door verdict.

## Corrected status

The published **universal dark-field theorem is withdrawn**. Its two purported universal implications were not proved:

1. An instantaneous scalar response denominator was identified with `alpha_3`. A PPN parameter requires the full boosted metric solution in standard PPN gauge. The repository calculation supplied neither the required metric components nor the gauge map, so it did not calculate `alpha_3`.
2. Enclosed-mass dependence was identified with an independent dark field. Exact AQUAL is a counterexample to that inference: its local nonlinear action yields a vacuum first integral whose boundary flux is `G M_b`. The physical potential itself carries the integration constant; a separate dark field does not follow.

The Deffayet--Woodard ratio lock is also narrower than claimed. It follows for two densities sharing the same unsourced transport current. Their 2026 `rho` is a CDM-like cosmological density explicitly distinguished from baryonic `varrho`; it is not a universal proof that all MOND memory is slaved to baryons.

## Replacement proposition: ordinary-action/retarded-localization trilemma

Consider a nonlocal response introduced through an inverse hyperbolic operator and require all three:

1. the nonlocal equations arise from an ordinary, twice-differentiable, single-copy action;
2. the inverse kernel appearing in that action is strictly retarded;
3. a finite local auxiliary representation has no additional unconstrained mode or negative kinetic direction.

For the standard multiplier localization, these three requirements cannot hold simultaneously.

### Proof, part I: reciprocity

For an ordinary action `S[q]`, the quadratic kernel is the Hessian

    H_ab(t,t') = delta^2 S / delta q_a(t) delta q_b(t').

Commuting functional derivatives gives `H_ab(t,t')=H_ba(t',t)`. On a domain where its two-sided inverse exists, that inverse is symmetric. A strictly retarded kernel is triangular in time and nonsymmetric whenever a later response to an earlier source is nonzero. The two-time exact matrix witness is

    G_ret = [[1,0],[R_21,1]],  R_21 != 0,

which is not symmetric and therefore cannot itself be the inverse Hessian kernel of an ordinary one-copy action.

This does **not** say that local action theories cannot have retarded solutions. They can: initial data select the retarded Green function of a local Euler--Lagrange operator. The obstruction is specifically to placing the strictly retarded inverse itself inside an ordinary one-copy nonlocal action and then varying it as though it were a symmetric variational kernel.

### Proof, part II: localization and complete Dirac count

The standard local representation of one Fourier response mode is

    L = U_dot lambda_dot - k^2 U lambda + J lambda.

The velocity Hessian is computed, not assumed:

    W = [[0,1],[1,0]],  det W = -1,  rank W = 2.

Hence there are no primary constraints. With no primary constraints there is no secondary preservation chain and the Poisson-bracket matrix is the empty `0 x 0` matrix. The counts are

    F = 0, S = 0,
    N_config = (4 - 2F - S)/2 = 2.

This holds separately at `k=0` and `k!=0`. In diagonal variables the kinetic Hessian is `diag(1,-1)`, exposing one negative kinetic direction. Retarded history data can select a subspace of solutions, but the local action's Dirac algorithm does not generate that selection as a phase-space constraint.

### Proof, part III: the doubled route

An in-in/closed-time-path action can generate causal response after imposing contour boundary conditions. The repository's explicit Keldysh block is regular before those conditions, and promoting diagonal matching to a Cauchy constraint does not produce the required second-class reduction. Adding a direct multiplier makes the multiplier absorb the desired response equation. Thus the ordinary doubled and direct-multiplier repairs are excluded; a new explicitly constrained doubled action remains logically possible but unconstructed.

## Exact MOND counterexample to the old enclosed-mass premise

For

    G(y) = y^2 + 2(1+y) exp(-y) - 2,
    G'(y)/(2y) = 1-exp(-y),

the local action

    S_AQUAL = -a0^2/(8 pi G) int G(|grad Phi|/a0) d^3x - int rho Phi d^3x

varies to

    div[(1-exp(-|grad Phi|/a0)) grad Phi] = 4 pi G rho.

In spherical exterior vacuum,

    d/dr [r^2 mu(Phi'/a0) Phi'] = 0,
    r^2 mu(Phi'/a0) Phi' = G M_b.

The enclosed mass enters through the boundary flux. This directly falsifies the old inference “local vacuum equation cannot know enclosed mass, therefore an independent dark field is mandatory.”

## What remains scientifically strong

- The exact exponential constitutive law and its local ellipticity remain correct.
- The curvature-QUMOND candidate is dead under its explicitly stated action class because exact MOND forces a nonzero multiplier gradient while exact tensor luminality forces the multiplier to vanish pointwise.
- Standard finite localization of a causal nonlocal inverse has an action/ghost/constraint obstruction.
- Fixed field-independent spin-2 form factors preserve linear no slip but cannot produce the nonlinear MOND source homogeneity.
- Scalar-curvature field dependence restores nonlinearity only by adding the familiar scalar trace mode and a trace-free slip source.

These are scoped no-go results, not a universal theorem.

## Fried-chicken scorecard after correction

The global verdict is **OPEN**. No single action in the repository has verified all gates. The best surviving door is a genuinely nonlinear tensorial, non-rational, causal in-in construction with an explicit constrained phase space; the best elliptic door must evade the already proved tensor-luminality multiplier obstruction. The next unavoidable calculation is to write one such complete action and compute its full phase-space reduction before assigning PPN parameters.

## Reproducibility

Run from `qwen_claude_field_theory/closure_2026/nonlocal_door_2026/`:

    python3 test_nonlocal_universal_claim_audit_2026.py
    python3 nonlocal_universal_claim_audit_2026.py

The regression suite derives the AQUAL Euler equation, shared-current ratio law, action-kernel symmetry witness, localization Hessian, Legendre map, empty Dirac chain, `0 x 0` Poisson matrix, first/second-class counts, `k=0` and `k!=0` mode counts, and the missing provenance needed for a genuine PPN calculation.
