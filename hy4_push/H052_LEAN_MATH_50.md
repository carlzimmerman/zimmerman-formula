# H052 — 50 MATHEMATICAL MACHINERIES, WITH LEAN INSTRUCTIONS
Classical, published machinery only. Each: what it is, how it attacks the
framework, and HOW TO CERTIFY IT IN LEAN.
Lean: `cd /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026 && lake env lean ABS.lean`.
MUST exit 0 with ZERO sorry. Delete unprovable theorems rather than leave sorry.
House patterns: hy4_push/lean/H034_field_equations.lean, H017_why_n_is_two.lean,
H043_dimension_scan.lean, H047_noether_charge_clustering.lean.

## ANALYSIS
**L001 Banach fixed point.** Existence/uniqueness for the EOM as a contraction.
Lean: `Metric.completeSpace`, `ContractingWith`. Prove a contraction constant < 1
on the ball; do NOT attempt the PDE itself, prove the ABSTRACT fixed-point lemma
and instantiate the constant.
**L002 Schauder / Leray-Schauder.** Existence when contraction fails.
Lean: state the hypothesis as an axiom-free theorem ONLY for finite-dimensional
reductions; leave the infinite-dimensional case unproven (do not fake it).
**L003 Lax-Milgram.** Weak solutions of the linearised EOM.
Lean: Mathlib has `IsCoercive` / inner-product-space material; prove the
FINITE-dimensional linear-algebra version and cite the rest as a hypothesis.
**L004 Sobolev embedding.** Does the phantom profile have enough regularity?
Lean: Mathlib has `ContinuousLinearMap`; prove only the ALGEBRAIC scaling of the
profile (which exponent is admissible), not the full embedding.
**L005 Distributions / weak derivatives.** The phantom is a 1/r^2 density —
differentiate weakly. Lean: define the distributional derivative of r^-2 as a
function and prove `deriv (fun r => -C/r) = C/r^2` on r > 0.
**L006 Gronwall's inequality.** Growth bounds on phidot perturbations (H038).
Lean: prove the discrete/finite version; Mathlib has `norm_le_gronwall` — search
it before writing your own.
**L007 Picard-Lindelof.** Local existence for the ODE reduction.
Lean: prove uniqueness for the LIPSCHITZ case only; state the rest.
**L008 Arzela-Ascoli / compactness.** Existence of minimizing profiles.
Lean: finite-dimensional compactness via `isCompact_Icc`; do not attempt
infinite-dimensional.
**L009 Maximum principle.** Sign control on the scalar. Lean: prove the
DISCRETE maximum principle (finite difference) — fully algebraic, compiles.
**L010 Harnack inequality.** Bounds on positive solutions. Lean: prove only the
algebraic ratio bound for the explicit phantom solution.
**L011 Hahn-Banach.** Separating the ghost mode. Lean: avoid the full theorem;
use the FINITE-dimensional separation (linear algebra) instead.
**L012 Spectral theorem.** Diagonalize the second variation (M081).
Lean: use Mathlib's symmetric-matrix diagonalization; reduce to a 2x2 or 3x3
explicit case and compute eigenvalues by `ring_nf`.

## GEOMETRY / TOPOLOGY
**L013 Divergence theorem.** The flux form of the MOND law.
Lean: prove the SPHERICAL case explicitly (integrate r^-2 over a shell):
`M_ph(r) = 4 pi int rho r^2 dr` with rho = A/r^2 gives M ∝ r. Fully algebraic.
**L014 Stokes / de Rham.** Conserved densities without Noether (J^0 = 0).
Lean: define the 2-form and prove `d(omega) = 0` for the explicit phantom form;
prove the integral over a sphere is radius-independent.
**L015 Hodge theory.** Decompose the fluctuation into exact/co-exact/harmonic.
Lean: prove only that the phantom's 1-form is CLOSED (`d alpha = 0`) for the
explicit solution.
**L016 Connections & curvature.** Write the parent's geometry.
Lean: avoid coordinate-free proofs; work in an explicit chart with `ring_nf`.
**L017 Riemannian geodesics.** Light bending / lensing.
Lean: prove the null geodesic of the weak-field metric has the standard
deflection for the explicit Phi; use `HasDerivAt` and explicit integration.
**L018 Symplectic geometry.** Hamiltonian structure of the EOM.
Lean: prove the symplectic form is CLOSED for the explicit 2-dim reduction.
**L019 Lie groups / algebras.** The D(D-3)/2 count as a representation (M047).
Lean: prove the combinatorial identity `D*(D-3)/2 = 2` has roots {4, -1} (see
H017) — this is already done; extend to the DIMENSION of the symmetric
traceless tensors as a polynomial identity.
**L020 Characteristic classes.** Obstructions to a global section (Door B1).
Lean: too high-level; instead prove the ALGEBRAIC statement that no global
nowhere-zero section exists for the explicit bundle, if reducible.
**L021 Homotopy / fundamental group.** Topological carriers (Door B3).
Lean: prove the winding number of the explicit map S^1 -> S^1 is an integer and
is invariant; Mathlib has ` windingNumber`.
**L222 Morse theory.** Count the equilibria (two: phantom, dust).
Lean: prove the explicit Morse function has exactly two critical points via
`deriv = 0` and sign analysis.

## ALGEBRA
**L023 Grobner bases / elimination.** Exact relations among observables.
Lean: do NOT implement Grobner; instead have Python/sympy produce the eliminated
polynomial and Lean VERIFY it by `ring_nf` on the explicit expression.
**L024 Resultants.** Eliminate variables to get the n=2 condition.
Lean: verify the resultant symbolically-produced identity by `ring`.
**L025 Polynomial algebra.** The n = D(D-3)/2 = 2 selection (H030/H043).
Lean: `ring` + `omega`; already proven in H017 — reuse its patterns.
**L026 Module theory / exact sequences.** The constraint complex.
Lean: prove exactness for the EXPLICIT finite sequence of maps.
**L027 Representation theory.** TT modes as a rep.
Lean: prove the dimension COUNT combinatorially (number of independent
components of a symmetric traceless tensor): `D*(D+1)/2 - 1 - D = D(D-3)/2`.
This is algebraic and compiles.
**L028 Ring theory / ideals.** The constraint variety.
Lean: use `Ideal` and prove membership for explicit generators.
**L029 Field extensions.** The K < 0 branch (sqrt K imaginary) (H038/H045).
Lean: prove `Real.sqrt` is 0 on negatives and that `x < 0 -> no real y with
y^2 = x`; Mathlib has `Real.sq_sqrt`, `Real.sqrt_sq_eq_abs`.
**L030 Galois theory.** Why the branch is forced. Lean: usually too deep; use
only if a specific polynomial's irreducibility matters (then use `irreducible`).

## PROBABILITY / INFORMATION
**L031 Martingales.** Convergence of the relaxation process.
Lean: prove the DISCRETE martingale property for the explicit update rule.
**L032 Ito calculus.** Stochastic EOM (M027). Lean: do not formalize Ito; prove
only the deterministic drift part and cite the noise informally.
**L033 Ergodic theorem.** Why two states persist (M037).
Lean: prove the FINITE-state ergodic theorem for the two-state (phantom/dust)
Markov chain by explicit matrix powers.
**L034 Large deviations.** Derive the 0.150 dex scatter (M021).
Lean: prove the algebraic rate-function identity for the explicit
distribution; compute the Legendre transform with `ring_nf` for a simple case.
**L035 Entropy / Gibbs.** G084's max-entropy derivation of the 1/2.
Lean: prove the entropy is maximized at the claimed point for the EXPLICIT
two- or three-state case (finite sums, `nlinarith`).
**L036 Fisher information.** Whether 5% on a_0 is achievable (N3).
Lean: compute the Fisher information for the explicit Gaussian model by
differentiation; verify with `ring_nf`.
**L037 Stochastic dominance.** Comparing -2 vs -3 hypotheses.
Lean: prove the ordering for the explicit families.
**L038 Concentration inequalities.** How tight is the cluster slope?
Lean: prove Hoeffding/Chebyshev for the explicit finite sample (`nlinarith`).
**L039 Bayesian updating.** Combining footings. Lean: prove Bayes' theorem
algebraically for a finite partition.
**L040 Information geometry.** Is n=2 special? (M025)
Lean: compute the Fisher-Rao metric for the mu_n family and prove the
n-dependence is monotonic — pure calculus, `ring_nf` + `nlinarith`.

## LOGIC / COMBINATORICS / DISCRETE
**L041 Order theory / lattices.** The two-zone structure as a lattice.
Lean: Mathlib has extensive lattice support; prove the two-zone decomposition
is a partition and the zones are ordered by radius.
**L042 Graph theory / spectral.** Cosmic web (M091).
Lean: prove the Laplacian's row sums vanish for the explicit graph.
**L043 Combinatorics.** Counting TT components (see L027).
Lean: `omega` and `ring`; combinatorial identities compile well.
**L044 Model theory / o-minimality.** Tameness (M099).
Lean: too deep; use only to justify finiteness informally, do not certify.
**L045 Type theory / Lean itself.** Metatheorem: what the framework CANNOT
prove. State explicitly which claims are out of Lean's reach (analysis-heavy
PDE facts) so no agent wastes a wave on them.
**L046 Numerical analysis (error bounds).** Trustworthy lane numbers.
Lean: prove the error bound for the explicit quadrature used (trapezoid on
r^-2) via `nlinarith`.
**L047 Convex analysis.** Diagnose the ghost as non-convexity (M071).
Lean: prove f'' < 0 somewhere for the explicit f — real calculus, doable;
`HasDerivAt` chains as in H043.
**L048 Sum-of-squares.** The ghost as an algebraic positivity failure (M073).
Lean: construct an explicit SOS decomposition and verify by `ring_nf`. This is
the highest-value Lean target in the whole list.
**L049 Fixed-point index.** Counting solutions.
Lean: prove the FINITE-dimensional Brouwer-degree count for the explicit map.
**L050 Category theory.** The composition structure.
Lean: prove the functoriality of the explicit construction ONLY if it reduces
to algebra; otherwise state informally and do not certify.

## WHAT LEAN CANNOT DO HERE (stated so no agent wastes a wave)
- Infinite-dimensional PDE existence/regularity (L002, L004, L008, L009).
- Itô calculus and genuine stochastic analysis (L032).
- Full Hodge/de Rham theorems on manifolds (L015 in general; the explicit
  closed-form case IS doable).
- Characteristic classes and index theorems (L020, L044).
Prove the ALGEBRAIC or FINITE-DIMENSIONAL or EXPLICIT-SOLUTION shadow of each
instead, and SAY SO in the lane. A smaller certified theorem beats a larger
unproven one.
