# Independent audit of the layer obstructions

Date: 2026-10-28. Reviewer: fresh isolated proof-audit subagent
`/root/audit_layer_obstructions`. The candidate was not edited.

**Normalized claim.** There exist (i) a sequence of compact, bounded-degree,
local product Schrodinger Hamiltonians with their actual positive ground
states, uniform conditional gaps on every block of fixed size, but vanishing
whole-layer discarded gaps, even for the specified extensive retained
algebra; (ii) a fixed-coefficient local oscillator sequence with the analogous
failure when retaining pair means; and (iii) a four-state reversible Markov
form whose conditional-average Schur form and metric-normalized Schur form
are both non-Markov.

**Primary verdict: proved as written.** This verdict covers these explicit
counterexamples and their stated scope. It does not identify any example
with an SU(N) Wilson vacuum, prove a failure on cubic lattices, or decide a
Yang--Mills mass gap. No correctness finding requires a change to the
audited candidate.

## Revision and dependencies

The authoritative candidate is
`real_research/yang_mills_layer_2026_10_28/obstructions/PROOF.md`,
SHA-256 `8bb7e20d713d1d72ee5f9899e0e1abadc783a5f14ff1552b0f5e229ad0dee8c3`.
The exact checker is `obstructions/check.py`, SHA-256
`19584b4fe18dbc53009814df8d07e96b90748bf46001e6f2d6da2c797c8d625a`.
The run contract has SHA-256
`bab37bd539934ad7a2cacfa58989d695a3ac9344949d3e6e57aa13b950885444`.
These content hashes control the review despite concurrent changes to the
repository's unrelated Git state.

Dependency graph:

1. Positive explicit circle kernel -> normalized tree Markov measure ->
   positive vacuum and local Schrodinger potential -> conditional density
   comparison and exact covariance -> admissible full-gradient Q witness.
2. Positive Dirichlet-chain precision -> explicit oscillator vacuum ->
   one-cell conditional precision and independent retained/fast factors ->
   exact discarded gap and rational vanishing-gap witness.
3. Original four-state conductances and masses -> orthogonal conditional
   P/Q decomposition -> energy minimization -> graph metric -> exact
   contraction violations.

The load-bearing statements are derived internally. Basic circle/product
Poincare comparison and Gaussian diagonalization are used with the stated
normalizations. The finite checker supports algebra and enumeration only;
it is not the evidence for the universal size quantifiers. No circular
dependency or unchecked Yang--Mills identification is used.

## Obligation matrix

| Obligation | Result | Decisive check |
|---|---|---|
| Compact actual-vacuum identity | Passed | With F=log psi, V=Delta F+|grad F|^2=Delta psi/psi; integration by parts gives the displayed ground form. |
| Positivity, uniqueness, domains | Passed | Every finite density is smooth and strictly positive on a connected compact torus; zero gradient implies a constant ground-transform function. |
| Fixed local interactions | Passed | At most three incident edges enter each W_v; at most four star terms contain any coordinate. Bounds on p', p'' imply the claimed uniform bounds on W_v. |
| All fixed-size conditional blocks | Passed | At most 3m edge factors vary, giving a density ratio at most 129^(3m); the comparison uses the variance minimization formula. |
| Rotor covariance and counting | Passed | First Fourier coefficient 30/41 gives covariance t_1^distance/2; a leaf has 2^(d-1) partners at distance 2d. |
| Full Q witness and retained algebra | Passed | The (theta, eta) -> (theta, zeta) integer torus map preserves Haar measure; theta and zeta are independent, hence P f_k=0. |
| Fast-fiber metric | Passed | Fixed-zeta tangent is (1,-1), of squared norm two; its energy is (partial_theta-partial_eta)^2/2, bounded by the full pair energy. |
| Local Gaussian actual vacuum | Passed | Direct differentiation gives the stated potential; the squared precision has range two cells and uniformly bounded coefficients. |
| Gaussian full discarded operator | Passed | The r law is independent of c; conditional Gaussian Poincare gives the lower bound and a first r eigenfunction constant in c attains it. |
| Four-state conditional Schur algebra | Passed | Recomputed from the original masses and conductances; D=4 and the minimizing within-block deviation has coefficient (b-c)/4. |
| Graph metric and normalization | Passed | The lift norm adds (b-c)^2/48; on coarse mass 1/3 this gives G=I+vv^T/16 and the displayed K. |
| Non-Markovness | Passed | Absolute-value contraction increases both energies on z=(0,1,-1). |
| Universal size conclusions | Passed analytically | Exact formulas hold for every finite k and n; their stated limits follow directly. |
| Actual Wilson/cubic/physical-sector identification | Out of scope | The candidate explicitly disclaims these identifications. |
| Continuum mass gap or novelty | Out of scope | Neither is asserted or established. |

## Reconstructed decisive steps

For the compact example, independent expansion gives
`kappa=1+(60/41)cos(t)+(24/41)cos(2t)+(4/41)cos(3t)`.
Its positive minimum is 1/41 and maximum is 129/41. The bound on the
conditional density ratio is therefore 129 per incident edge, independent
of the normalizing constant and exterior configuration. The potential
formula includes both edge second derivatives and the cross terms from
the squared sum of first derivatives; it does not silently omit those
star interactions. The derivative estimates give
`|b| <= 384+192^2=37248`, the negative bound `-3*37248/2=-55872`,
and the absolute bound `55872+(3*192)^2/4=138816` as stated.

The leaf-pair formula yields
`Var(f_k)/(2^k/2)=1+sum_{d=1}^k 2^(d-1)*(30/41)^(2d)`.
This is exactly the candidate's bracket. Its gradient energy is `2^k/2`
because each leaf marginal is Haar. This tests the full gradient rather
than a fiber-only surrogate. Adding the independent eta variables leaves
that energy unchanged and makes the same function an admissible Q vector
for the explicitly prescribed nonconstant retained algebra. The k=0
case also satisfies the formula. The tree geometry is essential to this
particular witness and is correctly separated from cubic geometry.

For the Gaussian model, the precision is `I direct-sum L_n`, rather than
the oscillator potential matrix itself. Squaring that precision is what
produces the local potential. Keeping this distinction gives the exact
conditional one-cell eigenvalues 1 and 2. The rational witness verifies
`L_n [i(n+1-i)/2]_i = 1`, including n=1, and therefore its Rayleigh
quotient is `12/((n+1)(n+2))`. This alone is sufficient for the negative
inference even without invoking the exact Gaussian gap formula.

For the four-state example, substituting `q=(t,-t,0,0)` into the original
energy produces the coefficient `4t^2+2t(c-b)`. Minimization and the fine
L2 norm give exactly the displayed S and G. Their simultaneous eigenvectors
have eigenvalue pairs `(0,1)`, `(1/2,9/8)`, `(3,1)`, so K has eigenvalues
`0,4/9,3`. The absolute-value energies are respectively `1/3 -> 2/3`
and `8/27 -> 2/3`. Thus Markovness fails in the actual coarse probability
algebra before as well as after normalization. This is conditional-average
elimination, so ordinary boundary-value Kron reduction is not implicated.

## Computation checks

Read the checker and its contract before running it. The code uses only
exact integer and `fractions.Fraction` arithmetic for acceptance. The
tree enumeration covers every ordered leaf pair at each stated depth;
the Gaussian tests cover every stated n; the four-state test starts from
the original conductances, rather than merely comparing hard-coded output
matrices. The checker verifies a supplied minimizing lift; the analytic
reconstruction above independently verifies that it is the minimizer.

Executed independently with Python 3.9.6:

```text
python3 real_research/yang_mills_layer_2026_10_28/obstructions/check.py --output /tmp/ym_obstructions_audit_result.json
```

Exit status 0. All exact checks passed: rotor depths 0 through 5,
Gaussian sizes 1 through 20, and the four-state example. The rerun JSON
equals the archived `obstructions/run001/result.json` exactly. Separately
recomputed every input and output hash in `run001/manifest.json`; all
matched. This establishes the reported finite checks and artifact
integrity, not an all-volume Yang--Mills computation.

## Remaining gap and safe use

There is no remaining proof gap in these three restricted counterexample
statements. Their strongest safe use is to reject automatic implications
from fixed-block conditional control, generic locality, or conditional
Schur elimination. They do not reject an argument that adds a proved
Yang--Mills-specific influence estimate, suitable fast-mode geometry,
or a different stable class of coarse operators.

The next substantive check belongs to those additional hypotheses for
the actual SU(N) Wilson vacuum; larger numerical checks of these examples
would not supply that missing input. Review provenance is an independent
subagent reconstruction within the same AI-assisted session, not
independent human peer review or a claim that model agreement proves
correctness.
