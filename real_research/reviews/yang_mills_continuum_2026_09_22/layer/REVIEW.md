# YM-C3 self-review

**Primary verdict: incomplete, with the missing implication being a
volume-uniform discarded-sector estimate for the actual weak-coupling
Yang–Mills Hamiltonians through successive exact elimination.**

The positive result proved here is restricted to the precisely defined
covariant quadratic model. The two counterexamples refute specific proposed
extensions, not that positive result or the Yang–Mills target.

## Dependency audit

| Step | Verdict | Decisive check |
|---|---|---|
| Tree transport gives a covariant average | Passed | Orthogonality gives A_R A_R^*=I; endpoint gauge factors cancel along each tree |
| Block means imply a whole-layer gradient bound | Passed | Exact variance identity, path length and edge congestion; sum over disjoint cubes without a volume factor |
| Gradient bound implies a vacuum-precision bound | Passed for the quadratic model | sqrt(K)>=K/sqrt(4d+1), then compression to ker A_R; no reversed square-root/compression inequality |
| Precision bound implies discarded quantum coercivity | Passed for the quadratic model | Diagonalize the Gaussian fiber precision, use its Hermite Poincare spectrum, and integrate conditional variances |
| epsilon may tend to zero in constants | Passed | gamma is independent of epsilon in (0,1]; no normalized zero-mass infinite-volume density is asserted |
| Repeated exact Schur elimination stays quadratic | Refuted | First two retained excitation levels are 6/5 and 84/29, not harmonic multiples |
| Wilson magnetic Hessian is positive on all discarded backgrounds | Refuted | SU(2) central-flux background and an explicit divergence-free, block-mean-zero circulation give negative Hessian |
| Negative potential Hessian refutes a quantum gap | Invalid inference, explicitly excluded | The vacuum-transformed form remains nonnegative; curvature is only one possible sufficient route |
| Nonlinear whole-layer bound and induction | Not established | Actual compact-link vacuum and generated coarse operators are uncontrolled by this proof |

The Gaussian conditional mean depends on the coarse variables, but its
covariance does not. This is why its fiber bound integrates without a
mixing assumption. No analogous fact about the nonlinear vacuum was used.
The tree bound applies to site vectors with prescribed transports; it is
not itself a theorem identifying a physical Yang–Mills fluctuation Hessian.

For the Fock counterexample, the retained sector is one-dimensional at each
particle number. H_n>=n and bounded graph operators ensure that the first
two computed levels really are the first two nonzero eigenvalues of the
normalized operator. The example distinguishes Hilbert-space Schur reduction
from Gaussian marginalization; it does not imply that multiscale estimates
in a larger operator class are impossible.

For the Wilson counterexample, all link matrices are genuine SU(2)
matrices. Even periodic side lengths ensure the central-flux configuration
exists. The variation has zero discrete divergence and zero componentwise
block means, but nonzero curl. Thus the negative direction is not removed
by discarding pure gauge or constant modes. The counterexample already
occurs in spatial dimension three.

## Reproducible checks

`checks.py` and `contract.json` were executed with the computation-audit
bounded runner (90-second wall limit, one numerical-library thread,
1,000,000-byte output cap). The actual invocation, input/output SHA-256
hashes, environment and execution result are in `run/manifest.json`.

- Four specified covariant tree examples: exact rational LDL decompositions,
  totaling 63 positive pivots, plus exact average-kernel and transport checks.
- Four actual central SU(2) lattice configurations: dimensions 2 and 3,
  torus sides 4 and 6; all plaquettes equal -I, the circulation is divergence
  free with zero block means, and its magnetic Hessian is respectively
  -5b/x and -7b/x.
- One two-mode Schur example: exact algebraic matrices in particle sectors
  one and two; metric-normalized eigenvalues 6/5 and 84/29.
- The derivative of 1+cos(tc/2) at t=0 is checked symbolically as -c^2/4.

Execution completed successfully and `validate_manifest.py ... --root .`
accepted the record. These are finite normalization/object checks supporting
the prose derivations, not a numerical verification of Yang–Mills theory.

Proofreading covered the new proof, contract and source record. Review is
self-review, not an independent or formally mechanized mathematical audit.
No prior mathematical proof file was altered. The root README is updated as
the live entrypoint; its YM-C2 hash remains a historical hash of the version
in input commit 01b05ecab, not a hash of the revised entrypoint.
