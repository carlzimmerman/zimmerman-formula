# Proof audit provenance and obligations

This is Codex self-review of the supersolution it supplied in v5, with an
independent calculation relative to Qwen's generated verification code. It is
not independent mathematical peer review. Qwen is the continuing research
worker; no second remote model or paid referee was used.

Verdict: proved as written within the stated stochastic model, by self-review.
certified_v2/ records all 19 algebra/enclosure checks passing; its manifest
validates. verify_v2.py uses exact expansion/cancellation. The original
verify.py/certified/ run timed out in heuristic symbolic simplification and is
preserved as a failed execution, not mathematical evidence. The analytic
bound is independent of the prior Monte Carlo values.

Claim: the fixed smooth radial cloud has Var(D)<273/50<32/5, conditional on
the central conservative unpolarized Thomson transport process in THEOREM.md.

Dependency chain: stated stochastic process -> angular generator -> explicit
smooth majorant -> nonpositive drift and outgoing boundary inequality ->
finite-horizon expectation inequality -> integrable escape limit -> exact
central upper bound -> variance inequality using separately derived E[D]=4.
No simulated variance is used to set a coefficient or prove any arrow.

The pathwise expectation identity can also be seen directly: on each flight,
integrate the derivative of a test function and add its changes at collisions.
The collision sum has compensator integral k(Kf-f) dt. Before a fixed stopping
horizon, the jump magnitude is bounded and the expected collision count is at
most rate_bound times that horizon. Therefore the compensated sum is integrable
and has zero expectation. Apply this to time-augmented G stopped at T wedge n.
The escape-tail bound then supplies domination as n increases. This verifies
the needed martingale integrability rather than silently treating a local
martingale as a martingale at unbounded T. The primary source is in SOURCES.md.

| Obligation | Evidence |
| --- | --- |
| Physical domain and Thomson moments | Explicit angular integration and sphere geometry in THEOREM.md |
| Correct backward operator | Full symbolic differentiation in verify.py |
| Entire interior drift sign | Residual factors as -4Aa z^2/[3(a+s)^2] |
| Entire outgoing boundary | Exact square, not a grid |
| Negative fixture | Missing offset gives a negative value at an admissible interior boundary angle |
| Finite escape and square integrability | Bounded-rate geometric tail |
| Correct comparison sign and stopping limit | Time-augmented G and dominated convergence |
| Central constant below threshold | Exact rational series and interval arithmetic |
| Novelty | Unverified; established methods and adjacent timing results identified |
| JWST observational confirmation | Out of scope; no response measurements tested |

The original nominal passes ce309f808d1b4cafbe0d109efcc4bd89 and
8080c7571c264c02b4ccee2ee7b15adb contain explicit placeholder booleans. The first
also substitutes the simulated second moment as a guessed supersolution value;
the second uses unbounded-error trapezoidal quadrature. Their arguments claim
computations absent from their code. Both remain rejected as proof evidence.
The valid rational-series leaf in ce309f80 is retained conceptually: equal
floating displays of its exact lower/upper fractions alone do not invalidate
the underlying rational enclosure. Later rejection16503071 inserts an erroneous
linear residual instead of differentiating q'=1-c+kb/2. Its claimed failure
does not refute the explicit majorant.
