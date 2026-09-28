# AS006 scoped intake: algebra retained, filter transfer needs qualification

Read-only intake of the newly returned primary-catalog result. No primary
claim, worker artifact, index or owner assignment was modified.
Result SHA256 `290b66f38551ce6747cca1c799253d0ec447d7a83c58a604889df4eea0ee6d9d`.
All 11 listed input hashes and six artifact hashes match current bytes.
Coordinator read the raw derivation and Lean source, but did not run Lean or
the author's numerical code; its process metadata is reported, not independently
authenticated by this intake. The claim remains owned by its recorded dispatcher.

## Exact accepted subset

For positive G,M,a,r, setting rM=sqrt(G M/a), x=r/rM and B=G M/r² gives
B/a=x^(-2), directly by substitution. Therefore a specified algebraic kernel
g=B psi(B/a) gives g/a=x^(-2)psi(x^(-2)). The two a normalizations merely
change the dimensional map under these assumptions. This exact identity does
not derive the kernel, its asymptotic limits, kappa, or a filtered field solution.

## Qualifications required before broader reuse

1. The raw theorem's quantifier "every kernel" does not imply its appended
   deep-MOND and Newtonian limits. The first additionally needs
   sqrt(y) psi(y)->1 as y->0; the second needs psi(y)->1 as y->infinity.
   The deliberately different psi=1 is a counterexample to the general deep
   limit, not a counterexample to a registered branch. The Lean deep identity
   takes sqrt(a B) as its expression; it does not prove arbitrary-kernel
   asymptotics. Retain the identity and require branch-specific asymptotics.
2. The exact-claim phrase equating xi->0 and r>>xi mixes an exact limit with
   a scale-separated approximation. Section 8 and the result's limitations
   correctly admit the second scale and restrict their computed transfer to
   |grad S u|. Use that narrower scope consistently.
3. Section 8 states a lower floor on xi, then evaluates exponentially small
   argument corrections using particular small xi values. A lower bound is
   not an upper bound on the correction: increasing xi at fixed r increases
   smoothing. The quoted galactic suppression cannot be uniform over all
   xi above that floor. This intake neither authenticates that floor's
   observational source nor derives a new bound on xi.
4. A small correction in grad S u does not bound the outer adjoint filter
   acting on the nonlinear response current. The author correctly lists that
   field solution as an unresolved implication. Do not promote the broader
   "inherits ... beyond any observable precision" sentence to a final-force
   result before that implication is proved.

## New narrow audit target from the missing outer-filter step

In Euclidean R³ on a source-free annulus, take the leading deep radial
response current j=C n/r = C x/r², C=sqrt(G M a)>0. Componentwise direct
differentiation gives Delta j=-2 C n/r³. Thus the formal small-t expansion
exp(t Delta)j=j+t Delta j+... with t=xi²/2 has a local leading correction
-xi² C n/r³, of relative order xi²/r², not exponential order. The Newtonian
gradient current G M n/r² is harmonic on the same annulus and does not have
this local first correction. This is a proposed local audit calculation,
not yet a proved expansion of the full singular point-source solution.

To use it for the operative filtered MONO force, independently establish the
radial flux reduction including the absence of an extra origin delta source,
the action of S* in the specified measure, dependence of j on the inner S,
and uniform remainder/boundary control. No literature mechanism is imported.
Both a footings enter C separately; constant vacuum and frozen-H histories
remain distinct. A large-radius expansion is also distinct from a small-xi
limit at fixed r. This is a focused continuation of an actual returned gap,
not a duplicate unfiltered scaling calculation or an accepted full-theory result.
