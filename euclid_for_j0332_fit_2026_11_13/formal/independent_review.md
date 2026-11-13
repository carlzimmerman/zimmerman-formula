# Independent audit of the local AQUAL scaling certificate

**Normalized claim:** The nine declarations in `AqualScaling.lean` establish
exact identities over real normed spaces: positive joint flux scaling, its
propagation through fixed linear finite-volume and projection maps, elementary
mass-sheet/source-coordinate identities, and a one-way square-root density
scaling identity. Their explicit hypotheses are part of each claim.

**Primary verdict: proved as written.** The mathematical declarations are
correct under their stated hypotheses. Independent recompilation succeeded.
No empirical measurement, PDE existence result, numerical-accuracy result,
physical-prior admissibility theorem, or novelty claim follows from this
verdict. The README explicitly maintains those limits.

## Claim card and fresh derivation

The coefficient domain is the real numbers. E is any real normed additive
commutative group with a real normed-space structure. F is finite; V is an
arbitrary index type. Potential fields are functions V→R. No Euclidean
finite-dimensionality, regularity, boundary-value existence, density profile,
or spherical symmetry is assumed. In this review, `F(g,a)` denotes the Lean
expression `flux a g`; the field is written first in the prose notation.

1. **Flux:** For k>0, `||k g||=k||g||`. Hence
   `||k g||/(ka+||k g||)=||g||/(a+||g||)`, and multiplication by kg gives
   `F(kg,ka)=kF(g,a)`. Real division is total in Lean, so cancellation by the
   nonzero k works even when `a+||g||=0`. Such cases are algebraic, not physical.
   For physical a>0 the denominator is positive; g=0 gives flux zero without
   a singular case. The theorem does not assert this identity for negative k.

2. **Finite-volume residual and solution scaling:** The supplied gradient is
   an R-linear map from potentials to face fields. Each face normal is an
   R-linear map into R. Their linearity, flux homogeneity, finite distributivity,
   and scaling the scalar source by k give `R(ka,kPhi,ks)=kR(a,Phi,s)`.
   Substituting R=0 proves the zero-residual declaration. This is one generic
   finite-volume row; applying it row by row requires the actual rows to have
   this representation. The claim does not certify a mesh, a discretization,
   solver iteration, uniqueness, or existence. An empty F gives R=−s and
   still satisfies the identity. Signed weights and arbitrary real sources
   cause no mathematical problem.

3. **Fixed-a counterexample:** In E=R, `F(2,1)=4/3`, whereas `2F(1,1)=1`.
   This disproves a general fixed-a homogeneity law. It does not claim that
   every fixed-a scaling fails; g=0 or k=1 are immediate exceptions.

4. **Deflection projection:** The hypothesis is an R-linear map from
   potentials into functions E→E. Evaluation at a fixed theta preserves
   scalar multiplication, giving `P(kPhi)(theta)=kP(Phi)(theta)` for every
   real k. Linearity of the physical LOS integral, its convergence, numerical
   interpolation/tail handling, and fixed distance factors are not proved.

5. **Lens map and external convergence:** Direct expansion gives
   `theta−[k alpha(theta)+(1−k)theta]=k[theta−alpha(theta)]` for every real k.
   Substituting `alpha_total=alpha_gal+kappa theta` yields the external-sheet
   coefficient `k kappa+1−k`. The entire original reduced deflection scales,
   including any original shear or other additive lens-plane term.

6. **Surface brightness:** For k≠0, multiplication of the transformed source
   coordinate by k⁻¹ restores the old coordinate. Evaluating any function
   `source:E→R` there proves the displayed identity. No continuity,
   nonnegative brightness, finite source flux, or source prior is assumed.
   The identity is sufficient for identical ideal brightness when the source
   is redefined as stated; it is not a classification of all transformations
   preserving images.

7. **Density relation:** For k>0,
   `sqrt(k² rho)=|k|sqrt(rho)=k sqrt(rho)` and scalar multiplication by the
   arbitrary coefficient gives the conclusion. This proves that the chosen
   density transformation is sufficient under the postulate. It does not
   derive the postulate, determine the coefficient, or prove a converse.
   Lean's real square root is zero for negative arguments, so the formal
   identity also includes nonphysical rho≤0 cases. A positive physical a0
   from a positive coefficient requires rho>0. Recovering rho from a0 needs
   the corresponding injective physical domain; coefficient=0 is a simple
   obstruction to an unrestricted converse.

## Dependency graph

- **Library proof leaves:** real norm scaling and scalar multiplication;
  nonzero-factor cancellation for total real division; linear-map
  homogeneity; finite-sum distributivity; real-module algebra; inverse scalar
  cancellation; real square-root multiplication and `sqrt(k²)=|k|`.
- **Internal:** norm scaling/cancellation → flux theorem → finite-volume
  residual theorem → zero-residual theorem.
- **Internal, separate branch:** linear-map hypothesis → projection theorem.
- **Internal, separate branch:** module algebra → mass-sheet lens equation →
  inverse scalar cancellation → brightness identity. The external-convergence
  identity is a direct module-algebra expansion.
- **Internal, separate branch:** square-root library identities → density
  scaling identity.
- **Application assumptions:** the implemented discretization and projection
  instantiate these maps; boundary data scale homogeneously; the same geometry
  is used; transformed external convergence and source remain physically
  admissible; the density postulate applies. These are not theorem outputs.

There is no circular proof dependency. No physical literature theorem is a
load-bearing premise of the nine formal identities. Historical priority was
not investigated because the reviewed files make no novelty claim.

## Obligation matrix

| Obligation | Status | Evidence or limitation |
|---|---|---|
| Typing, quantifiers, norm and scalar domains | Passed | Raw definitions and theorem signatures reconstructed above |
| Positive flux scaling, including g=0 | Passed | Norm scaling and cancellation; compiler checked |
| Finite sums, empty-face case and source sign | Passed | No positivity of weights/source needed |
| Linear boundary treatment | Conditional | Linear gradient assumed; fixed nonzero boundary offsets must also scale or be included in an extended linear variable |
| Exact-zero residual preservation | Passed | Direct consequence of residual homogeneity |
| Numerical solver/continuum PDE interpretation | Not addressed | Neither is represented or proved in this file |
| Projection linearity and fixed cosmological geometry | Conditional | Explicit linear-map hypothesis, not verified implementation |
| Lens equation and external-convergence coefficient | Passed | Direct expansion; no missing term |
| Brightness identity for k≠0 | Passed | Exact inverse cancellation |
| Priors, physical sheet realization and nonlinear environment | Not addressed | An additive lens-plane sheet is stipulated; physical realizability in an AQUAL environment is not proved |
| Density square-root identity | Passed | One-way statement; physical-domain interpretation stays conditional |
| Empirical or novelty inference | Out of scope | README explicitly disclaims both |

## Interpretation cautions, not failures of the formal statements

The source comment at line 98 says images are unchanged “only after” the
specified source redefinition. Read this as describing the sufficient
construction being certified. The theorem proves no necessity or uniqueness;
for example a constant source can preserve brightness without changing its
function. Similarly “corresponds” near the density statement must not be read
as an unrestricted converse. The README's actual implications are stated
one way and avoid these overreadings.

The conditional imaging family is a valid algebraic obstruction to identifying
all of its parameters from unrestricted ideal image brightness alone. It is
not an obstruction after all independent priors/data are included. In
particular, fixed or tightly constrained external convergence, source size,
stellar mass/IMF, or other observables can remove parts of the family. A
physical external mass distribution cannot be assumed to superpose linearly
with an AQUAL galaxy merely because an additive lens-plane deflection has
been written down. The files do not certify that physical realization.

Holding the lensing geometry fixed is essential. Changing a postulated physical
dark-energy density in a cosmological solution need not preserve the distances
inside the projection. The README states this restriction. Likewise the
fixed density/length scales of the screened v3s action are outside this
homogeneity certificate.

## Compiler and provenance checks

On 2026-11-13, this reviewer independently ran, from
`/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026`:

```bash
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/euclid_for_j0332_fit_2026_11_13/formal/AqualScaling.lean
lake env lean --version
```

The accepted file exited 0. All nine `#print axioms` outputs listed only
`propext`, `Classical.choice`, and `Quot.sound`; none listed `sorryAx`.
The version was Lean 4.34.0-rc2, commit
`6a10ac8c22beadecabdbb0919c2b50214762f91d`. The canonical Lake manifest pins
mathlib revision `85e3a25e006c35636f0e53b0e9296caca2685bc0`.
No canonical project or Lean source file was edited by this review.

All five before/after input hashes in `certificate_provenance.json` matched
current files. The accepted compile log and mutation compile log both matched
their recorded hashes; the mutation source matched its recorded hash. The
mutation log records nonzero compilation with the intended unclosed k-versus-k²
flux identity. Its `sorryAx` output occurs in this rejected compilation and
is not evidence against the successfully compiled accepted file. The mutation
was inspected, not independently rerun.

The helper's axiom-dependency JSON field is hard-coded, so the actual printed
compiler dependency output is the decisive evidence; in this run it agrees.
No empirical computation result is used as a premise of the proof verdict.

## Exact remaining gap and safest claim

There is no remaining proof gap in the nine statements as written. To promote
this certificate into a guarantee about the actual analysis pipeline, one
must establish that its fixed-boundary gradient/projection/tail implementation
satisfies the formal hypotheses and that the transformed model lies inside
the physical/statistical model class. That application bridge is deliberately
outside the certificate. The cheapest next check is a numerical joint-scaling
invariance test of the complete fixed-geometry forward model, including its
outer-tail prescription and external-sheet/source transformation; that would
still be finite implementation evidence, not a replacement for these proofs.

**Review provenance:** separate subagent reviewer, not the Lean author. The
reviewer previously audited the numerical field module but had not authored
this Lean certificate. The raw statements were read before author self-audit
claims were assessed. This is an independent derivation and recompile, not a
second proof-author self-review; it is not independent of the shared Lean
kernel, mathlib dependencies, or underlying model family.

Exact artifacts audited:

- `AqualScaling.lean` SHA-256:
  `a32d3b6e36a0a769e1af60986bc17561903fe851a2e3402e22577e45a0d3b998`.
- `README.md` SHA-256:
  `702b03a937fac9b385e0c6b214dec99749e747ca23ec77f7227bb50eb86e6a5c`.
- `certificate_provenance.json` SHA-256:
  `1d22f8163ff51cb0dee1dfaeff42ca90dc67aeba18dc538dceecbe67eafa0530`.
