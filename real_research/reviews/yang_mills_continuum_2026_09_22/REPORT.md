# Yang–Mills continuum attempt: exact progress and the remaining operator estimate

The original target is **not solved**. This checkpoint produces a precise
conditional multiscale route, a favorable ultraviolet gap budget, and exact
counterexamples to shortcuts that would otherwise make the route appear closed.
It does not add a continuum claim to the published preprint.

Base checkpoint YM-C1: `b73311096299e2f1816be00036ccdb2922bc44d4`.
See [CONTRACT.md](CONTRACT.md) for the actual target, ownership and conventions.
Concurrent repository commits occurred; the starting I15 proof and certificates
are unchanged from the assigned base. This work is in this new directory only.

## The substantive opening: retain the coarse norm

For a nonnegative, actual-vacuum-subtracted Hamiltonian split into retained
and discarded coordinates, write

    H = [[A,B*],[B,D]],  D>=d>0,
    S = A-B*D^{-1}B,
    G = I+B*D^{-2}B.

If the effective operator G^{-1/2} S G^{-1/2} has gap gamma>0, then

    gap(H) >= [gamma^{-1}+d^{-1}]^{-1}.

The proof is a completion of squares followed by a distance-to-vacuum
estimate. It permits a dressed fine vacuum. After successive EXACT
eliminations in their induced norms,

    gap(H_fine) >= [gap(H_terminal)^{-1}+sum_j d_j^{-1}]^{-1}.

Unlike a product of fixed per-scale losses, the inverse-gap cost can stay
finite over infinitely many ultraviolet scales. At physical scales
a_j=A L^{j-K}, with an illustrative inverse coupling s+q(K-j), a bound
d_j>=c x_j/a_j would give

    sum_j d_j^{-1} <= (A/c)[s/(L-1)+qL/(L-1)^2].

This is an exact summation under the stated model assumptions, not a
proved renormalization trajectory. In fact any polynomial weakening of
x_j in the number of ultraviolet scales is compatible with summability.
Thus ultraviolet depth by itself does not defeat this particular comparison.

[Full comparison, domain assumptions and scale proof](blocking/SCHUR_GAP.md).
[Terminal metric bound and alternative error accounting](rg/REPORT.md).
These are elementary analytic lemmas, not new Lean-certified operator theorems;
no claim of novelty is made.

The terminal norm need not be bounded everywhere by a constant. If S has
ordinary gap Delta and, on the complement Q of its vacuum,

    Q G Q <= M Q + eta S,

then gamma >= [M/Delta+eta]^{-1}. A comparison with our I15 endpoint would
still need the actual terminal form and vacuum, including every generated
interaction. Matching a running coupling to a Wilson coupling does not do it.

## Attempts that were actually tested

| Mechanism | Decisive result | Meaning for this program |
|---|---|---|
| Keep the strong-coupling gap while a tends to zero | Its physical lower bound grows like x/a; every finite-norm, strongly continuous cyclic limit collapses to the vacuum | The old bound cannot simply be carried unchanged to a finite-mass theory |
| Eliminate modes and keep only the Schur form S | An exact three-by-three family has gap(S)=gap(D)=1 but gap(H) tends to zero | The induced metric G is indispensable |
| Use bare electric product vacua to choose the retained space | A uniformly gapped product model has discarded-sector energy tending to zero exponentially in volume | True-vacuum dressing is needed before claiming a uniform D bound |
| Propagate a gap with polynomial additive RG errors | Exact two-state scale families satisfy that estimate and still lose their physical gap | Such error estimates alone cannot carry a continuum mass |
| Obtain weak-coupling coercivity from globally positive vacuum curvature | The Bakry–Emery tensor has negative trace in an actual one-plaquette SU(2) example | That sufficient curvature condition fails; this is not a no-go for the gap |
| Combine good single-cell/conditional gaps | An exact color-singlet oscillator family has uniform conditional gaps but a global gap tending to zero | The missing long-distance mixing estimate cannot be omitted |

The last example is a counterexample to an abstract local-to-global inference,
not an identification of the nonlinear Yang–Mills vacuum with a Gaussian.
The one-plaquette calculation also proves that its actual physical gap tends
to 2 sqrt(b) at weak coupling. It is collective large-volume behavior, rather
than the isolated plaquette, that this program still has to control.

Detailed proofs: [bare-projector obstruction](blocking/BARE_PROJECTOR_OBSTRUCTION.md),
[vacuum coercivity and weak-coupling analysis](vacuum/PROOF.md),
[RG error counterexamples](rg/REPORT.md).

## The continuum interface is also explicit

For the actual centered observable vectors, a common contraction at one
fixed physical time tau on every vector of a dense subspace,

    <u,exp(-tau H)u> <= q ||u||^2,  0<q<1,

gives a simple vacuum and mass gap at least -log(q)/tau. Convergent cutoff
Gram/time-correlation matrices permit this inequality to pass to the limit.
It must hold on all linear combinations, not only selected observables.

There must also be nonzero finite-energy spectral weight. A single convergent
observable family with norm squared at most M and positive time correlation
at least v>0 gives the finite upper mass bound log(M/v)/tau. Uniformly bounded
Rayleigh energy and nonvanishing norm supply such a witness by Jensen's
inequality. This is still conditional on an actual field/observable construction.

[Continuum transfer, finite-mass witnesses and six exact counterexamples](continuum/PROOF.md).
The official target includes both positive and finite mass and the quantum-field
axioms; it is not satisfied by spectral exclusion in a trivial Hilbert space.
Source: [Jaffe–Witten, section 4](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).

## Second cycle: an abstract limit can be built, but its field content is not automatic

The exact normalized graph maps U=J G^{-1/2} preserve norm, vacuum and
quadratic energy. Composing them preserves a terminal excited trial vector's
Rayleigh quotient, giving finite-energy witnesses at every cutoff.

For a genuinely compatible nested family across cutoffs, there is also a
constructive abstract limit: the embedded inverse Hamiltonians on the excited
sector increase and are bounded by the common inverse gap. Their strong limit
is injective, so its inverse defines a self-adjoint Hamiltonian with the same
positive lower gap. Continuous functional calculus gives convergence of the
positive-time semigroups. This preserves a finite-energy, nonzero excitation.
It is more than a formal assertion that a limit ought to exist.

Two limitations were checked rather than assumed away. First, separately
blocking each cutoff does not give this cross-cutoff compatibility: the fixed
coarse-scale forms, metrics and observable maps may vary with the ultraviolet
depth. Second, even compatible exact Schur systems with summable inverse-gap
cost can have a nonclosable common form. An explicit weighted rank-one example
has a perfectly good relaxed limiting Hamiltonian but loses a term of its
intended algebraic form. Thus neither nonexistence of every limit nor agreement
with the intended continuum dynamics can be inferred from form compatibility
alone.

[Graph-lift proof, abstract Hamiltonian construction, and exact counterexample](continuum/BLOCK_LIMIT.md).
The latter uses nonlocal projectors and is not a no-go theorem for a properly
local Yang–Mills construction. Its consequence is that the local observable
content and field-theory identification must be proved in the limit.

## Exact remaining mathematical obligations

1. Construct noncircular gauge-compatible block projections and interacting
   vacuum subtractions, and prove the discarded-sector bounds uniformly in
   volume and cutoff. Bare Casimir bounds do not provide them.
2. Control the exact coarse form AND induced metric at the finite physical
   scale A. Establish a terminal gap through a proved comparison, without
   discarding nonlocal or generated interactions or changing the vacuum.
3. Construct compatible renormalized observables and their continuum limits,
   including a nonvanishing finite-energy witness. Prove locality, relativistic
   covariance, the prescribed Yang–Mills short-distance content and the other
   axioms. A family of abstract Hamiltonian gaps is insufficient.

The weighted-vacuum route expresses item 1 as conditional coercivity for the
actual measure psi_0^2 dU. Conditional expectation onto retained variables
would preserve its constant vacuum exactly and avoid the bare-projector defect.
The measure and its volume-uniform multiscale estimates remain to be
constructed; assuming them would not be a proof.

## Evidence, review and continuation checkpoint

The block comparison received a separate AI-assisted derivation check. That
check found and corrected the ordinary-versus-induced kernel map and clarified
the unbounded-operator form domain. The root reconciled all returned arguments
and checked the critical matrix, oscillator, scale and spectral directions.
Review is not a formal proof certificate or human peer review.

Successful computation manifests in `blocking/run_exact/`, `rg/run/`, and
`vacuum/run/` validate. They contain exact finite algebra checks and bounded
numerical normalizations, with precise non-claims. The first block check had
an unintended floating division; its failed record is preserved and the exact
arithmetic correction is documented in [blocking review](blocking/REVIEW.md).

Primary-source checks are scoped and explicit. Chatterjee's checked theorem
runs from a strong all-boundary clustering hypothesis to confinement; it
does not establish the hypothesis needed here. Balaban's exact theorem text
was not acquired in this run and is not used as a proved dependency. No claim
that an inaccessible source closes or disproves the route is made.

The executed methods have reached specific missing operator estimates, not
a solution hidden in the scalar certificates. The next mathematical input
must control the interacting vacuum and long-distance coarse action. More
single-plaquette checks or sharper beta-function coefficients do not discharge
those obligations. This checkpoint preserves the proofs and failed shortcuts
for continuation without re-running the same claims.
