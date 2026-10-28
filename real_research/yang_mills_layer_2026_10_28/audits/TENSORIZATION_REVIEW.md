# Tensorization and actual-vacuum locality audit

**Normalized claim and primary verdict: correct only after a stated restriction.**
The conditional layer and compact-manifold criteria, the gauge-invariant
mixture counterexample, and the two-square SU(2) nonindependence calculation
are proved under their stated hypotheses. The connected-cluster calculation
in §6 needs its lattice class restricted to square plaquettes with four
distinct link variables. Its displayed first-order equation is false on
some degenerate periodic lattices permitted by the phrase “any fixed finite
lattice.” None of these statements establishes the unknown actual-vacuum
influence hypothesis at weak coupling or stability under quantum Schur
elimination.

Date: 2026-10-28. Reviewer: `/root/audit_layer_tensor`.
This is a separate-agent adversarial analytic audit, not formal verification
or human peer review. The reviewer inherited the program context, so it is
not represented as an author-blind review. The critical formulas below were
reconstructed from the definitions rather than accepted from the self-audit.
No candidate proof or shared status file was edited.

## Exact revision and scope

Audited artifact:
`real_research/yang_mills_layer_2026_10_28/tensorization/PROOF.md`

SHA-256:
`745d41a38cb6380b65cd164bf87a0a4c259cf173d790691d245607c6968ce9c7`.

Supporting source record:
`real_research/yang_mills_layer_2026_10_28/tensorization/SOURCES.md`

SHA-256:
`c34d60d345ffc9fdefac0e86bdb8581b4ed050190d7d609f8cde1e70975e8dde`.

The current checkout reported HEAD
`1180f5e8a4dae9b0513a6e40e453c58b19760a40` during review. Concurrent unrelated
changes are present; the artifact hashes identify this review. No applicable
`AGENTS.md` was found in the inspected ancestor paths or `real_research/`.
The target contract and published `sections/vacuum.tex` conventions were read.
The published fixed-block theorem is an input, not comprehensively re-audited
here. The old normalized-Schur counterexample is also outside this audit.

## Claim cards and dependency graph

1. **Conditional layer implication.** On each finite product of equal-size
   SU(N) link blocks, the actual smooth positive vacuum measure has every
   single-block conditional gradient gap at least `lambda_0`. If the total
   variation Dobrushin matrix at every fixed exterior has spectral radius
   at most `q<1`, uniformly over the chosen volumes, the full layer has
   gradient gap at least `(1-q) lambda_0`. Its physical energy lower bound
   is `x(1-q)lambda_0/(2a)` on the specified conditional-mean-zero subspace.
2. **Hessian implication.** On a finite product of compact connected
   boundaryless Riemannian manifolds, conditional gaps `lambda_i`, smooth
   log density `-W`, and mixed Hessian bounds `h_ij` give the gradient gap
   `rho` when the matrix with diagonal `lambda_i` and off-diagonal `-h_ij`
   dominates `rho I`. Application to Yang–Mills requires this additional
   matrix condition for its actual vacuum.
3. **Measure counterexample.** The displayed SU(2) gauge-invariant mixture
   has uniformly bounded fixed-block density ratios but physical-sector
   gradient gap at most `12/(epsilon^2 M)`.
4. **Actual two-square counterexample.** For the finite SU(2) Wilson operator
   on two ordinary adjacent square loops, two links sharing no plaquette
   are conditionally dependent in the actual vacuum for every sufficiently
   small nonzero real `g=2b/x^2`. For the original `b>=0` model, use positive
   `g`. This is a strong-coupling perturbative obstruction to exact
   conditional independence, not a large-influence or weak-coupling result.
5. **Perturbative support.** On a fixed nondegenerate square lattice,
   logarithmic vacuum coefficients at order `n` are sums of functions of
   connected clusters of at most `n` plaquettes. No uniform convergence or
   coefficient bound is included.

Dependencies:

- Actual ground-state transform and conditional local gaps → published input.
- Dobrushin variance tensorization → external Wu Theorem 2.1, verified below.
- Local gaps + that tensorization + conditional integration → claim 1.
- Conditional spectral theorem + product integration by parts + compact
  elliptic spectral decomposition → claim 2, internally checked.
- Haar character orthogonality + explicit mixture + Rayleigh quotient →
  claim 3, internally checked.
- Isolated eigenprojection perturbation + logarithmic eigenfunction
  equation + shared-link derivative calculation → claim 4, internally checked.
- The logarithmic recurrence + support-preserving product heat inverse →
  claim 5, internally checked on the stated restriction.
- Actual weak-coupling influence bounds and exact coarse-form stability →
  **unchecked assumptions/open obligations**, not consequences of the above.

There is no circular use of a global Yang–Mills gap in the positive criteria.

## Obligation matrix

| Obligation | Finding | Evidence and limitation |
|---|---|---|
| Discrete-metric source applicability | Passed | SU(N)^m with its Borel sigma-algebra has measurable diagonal; the discrete metric is explicitly allowed by Wu. Its second moment is bounded. |
| Total variation convention and constant | Passed | The source Wasserstein distance for the discrete metric is `sup_A |nu(A)-nu'(A)|`, exactly the candidate convention. |
| Conditional integration, projection and physical restriction | Passed | Integrating the fiber variance gives `||Q_F f||^2`; gauge actions preserve the coordinate subalgebra and the invariant measure. The finite-volume smooth conditional projection preserves the Sobolev domain. |
| Four-point oscillation influence certificate | Passed | Optimizing the likelihood-ratio extremal bound gives `tanh(Delta/4)`. Two geodesic integrations give `Delta <= D_i D_j h_ij`. |
| Compact-manifold cross identity and factor of two | Passed | Product connection produces the positive mixed-W Hessian term in equation (9); expanding `L^2` gives precisely the matrix off-diagonal contribution `-2 h_ij v_i v_j`. |
| Hessian criterion implies spectral gap | Passed | The compact weighted elliptic operator has constant kernel and a complete discrete eigenbasis; `||Lf||^2 >= rho <f,Lf>` excludes eigenvalues in `(0,rho)`. |
| Mixture normalization, gauge invariance and constants | Passed | Each signed product component integrates to one; its one-loop means are `+/- epsilon/4`; one-loop marginal of the mixture is product Haar. |
| Perturbative coefficient signs and source support | Passed | `T exp(ell)/exp(ell)=T ell-Gamma(ell,ell)`; the coefficient `2/9` in equation (15) is correct. |
| Two-square nonzero mixed term and conditional-dependence inference | Passed | Shared-edge derivatives yield `-sin(t/2)sin(s/2)/4`; nonzero mixed rectangle differences exclude an additive log density. |
| Finite-volume analytic remainder | Passed | `||S||<=2` and the free spectral gap `3/4` justify the stated rank-one resolvent circle near zero. Smooth elliptic regularity permits a norm in which the nonzero `g^2` coefficient dominates the remainder. |
| Connected-cluster support for nondegenerate squares | Passed | Carré-du-champ terms require shared link support; centered inverse of the product Laplacian does not enlarge support. |
| “Any fixed finite lattice” first-order equation | Failed as written | A one-site periodic plaquette need not have zero Haar mean; see the explicit counterexample below. |
| Actual Yang–Mills uniform influence input | Not addressed | Correctly identified as open in the candidate. |
| Uniform exact Schur iteration or continuum mass gap | Out of scope | No such conclusion is proved by these arguments. |

## Decisive reconstructions

### Two-square vacuum calculation

With `T=-Delta`, the logarithmic eigenfunction equation has the minus sign
before `Gamma(ell,ell)`. The first-order term is `ell_1=(F_p+F_q)/3`, since
each simple square contains four distinct fundamental links and `4 C_F=3`
for SU(2). The second-order mixed term is consequently `2 Gamma(F_p,F_q)/9`.
All other second-order terms lack at least one selected link and are killed
by `J=(I-E_u)(I-E_v)`.

At the identity values of the other links, the common-edge derivative in
the third Lie-algebra direction is `-sin(t/2)/2` for one loop and
`+sin(s/2)/2` for the oppositely oriented loop. The other two directions
vanish on this slice. Thus the candidate sign and coefficient are correct.
For example, choosing `t=s=pi` gives mixed rectangle difference `-1/4`.
This is a valid pointwise witness on the full smooth configuration space;
it does not replace the configuration space by a gauge-fixed surrogate.

The Haar projections commute with `T`. If the resulting `J ell_2` vanished,
equation (15) would force `J Gamma(F_p,F_q)=0`, contradicting that rectangle
witness. A nonzero leading coefficient of an analytic Banach-space-valued
series remains nonzero for all sufficiently small nonzero real parameters.
Finally, conditional independence for a positive smooth density forces its
logarithm to be additive in the two selected variables at almost every
exterior value, hence everywhere by continuity. This contradicts the witness.

### Mixture Rayleigh quotient

Haar character orthogonality gives `E h_i^2=1/4` and zero Haar mean. The
latent plus/minus mixture therefore contributes variance `epsilon^2/16`
to the average of the `h_i`. The supports of the loop gradients are
disjoint, and each loop marginal is Haar, so the energy of this average is
`M * (3/4)/M^2 = 3/(4M)`. The displayed upper bound `12/(epsilon^2 M)` follows.
The function is gauge invariant, so this is also a physical-sector witness.
It is not an actual local Wilson vacuum witness, as the candidate states.

### Required restriction in §6

On the one-site periodic SU(2) lattice, take a square plaquette represented
by the commutator `U V U^{-1} V^{-1}` and let
`F=Tr(U V U^{-1} V^{-1})/2`. Schur averaging first in `U` gives

`integral_U F = |Tr V|^2/4`.

Character orthogonality then gives `integral_{U,V} F=1/4`. Every smooth
`T ell_1` has zero Haar mean, so the displayed equation `T ell_1=S` is
impossible for this one-plaquette example. The actual first-order energy
would be `e_1=-1/4`.

The cheapest restriction is: **§6 concerns square plaquettes whose four
link variables are distinct**. Their Haar means vanish and each is a
Casimir eigenfunction with eigenvalue `4 C_F`, exactly as used in its proof.
Alternatively, a generalized centered recurrence can be supplied and
audited separately. This report does not silently repair the candidate.

## Source and computation checks

The exact primary source was opened through the web PDF reader:
[Liming Wu, arXiv:math/0611635v1](https://arxiv.org/pdf/math/0611635v1),
electronic reprint of *Annals of Probability* 34 (2006), 1960–1989,
DOI `10.1214/009117906000000368`. Checked on 2026-10-28:
PDF pages 4–6, the permitted measurable-space/discrete-metric setup,
definition (2.3), Theorem 2.1 and inequality (2.4). The exact variance
tensorization implication and its normalization match the candidate.
The actual Yang–Mills spectral-radius hypothesis remains additional.
No source byte hash is claimed because no local copy was retained.

No numerical or symbolic computation is load-bearing. The arithmetic,
two-direction Lie derivatives, representation averages and support
induction were checked analytically. `shasum -a 256` pinned the two reviewed
artifacts; `nl -ba`/`sed` were used to inspect the relevant raw sections.
No broad novelty search was performed and no novelty finding is made.

## Strongest safe outcome and exact remaining gap

After the explicit nondegenerate-square restriction, these are sound
conditional layer criteria, a gauge-invariant obstruction to deducing a
collective gap from fixed-block estimates alone, and a sound actual-vacuum
counterexample to bare-plaquette conditional independence. The perturbative
support statement is finite-volume and gives no coefficient-size estimate.

The missing positive implication remains an actual-vacuum influence or
mixed-Hessian bound uniform in the layer and exterior volume in a useful
coupling regime. The subsequent quantum coarse-graining comparison is an
independent missing implication. Neither is supplied by this review.

## Resolved addendum for the restricted revision

Date: 2026-10-28. Revised `tensorization/PROOF.md` SHA-256:
`9cb036f17adafcc6dd7cb5b5c2d56007cd5c9541850646453aeb2339cfd9d783`.

**Primary verdict for this revised artifact: proved as written.** This
verdict concerns its stated conditional implications, counterexamples and
finite-volume perturbative support statement; it does not establish the
additional actual Yang–Mills uniform influence hypotheses.

The revised opening of §6 explicitly requires four distinct link variables
in each square plaquette and excludes degenerate periodic plaquettes. Its
assertions that each plaquette function has zero Haar mean and is a
`T`-eigenfunction now match the proof of the centered first-order equation.
The restriction is consistent with the adjacent-square example in §5 and
with the later support induction. The original finding above is resolved
for this exact revised hash and is retained as historical evidence.

The reviewer read the revised paragraph and its downstream recurrence,
induction and scope conclusions. As a change-scope check, replacing only
that revised paragraph by its previous text in memory reconstructed the
exact previously reviewed SHA-256
`745d41a38cb6380b65cd164bf87a0a4c259cf173d790691d245607c6968ce9c7`.
Thus no other candidate bytes changed between these two revisions, and the
unaffected analytic checks above remain applicable. No candidate edits were
made by the reviewer.
