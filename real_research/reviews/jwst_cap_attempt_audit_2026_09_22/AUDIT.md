# Audit of cap counterexamples and absorption prerequisite

No new physical result or novelty claim is accepted. The cap lower bound is
still unresolved by Qwen. This audit uses exact angular integrals and input
constraints to reject alleged counterexamples; it does not prove the cap bound.

Four nominal checked records are rejected:

- 3435a8a3125d4183bfbc5a9bd209e62c inserts Var=M^2/20 without derivation.
  The earlier uniform theorem already gives Var>=M^2/10. Its actual main
  payload is false, its numbers satisfy the proposed inequality, and its
  positive/negative predicates differ. A weak bound is not a false bound.
- b14ad15b5a154f1383ae626eec43e1e8 labels 0.1*integral(k*r^2) a variance,
  explicitly calls it a placeholder, and forces negative=False.
- 96384ee15ce140468c2b450e4ff8cdf4 uses a discontinuous step with r0=d/M.
  Its actual mean is 1/80, not the declared 1/2. Correct constraint radius
  is sqrt(2*d/M). Its variance formula 2*I*sqrt(M) is unsupported.
- 246122c269c04e089fa5a96ea2fbc686 repeats that proxy, optimizes without
  enforcing 0<=k<=M or checking optimizer success/constraint residuals, and
  forces control booleans. At M=1,d=1/2 the only admissible continuous
  profile is k=1: integral r*(1-k)=0 with nonnegative continuous integrand
  forces k=1 for r>0 and then at zero. Its radial moment must be 1/3.

Exact independent angular integration gives E[mu^2]=2/5,
K[z^2]=3*s/10+z^2/10 and E[(z_new-z)^2]=3*s/10+11*z^2/10.
The guessed 0.375*(s+z^2) bracket is false. These are local jump identities;
their integration through stopping still needs a written argument. Do not
replace an expected occupation integral by a radial integral equality.

The most useful actual code is f0773c84727d48feaac1155b82ebf844. It now
implements competing exponential absorption/scattering/boundary events,
retains escapes only, computes D=T-x_exit dot u_exit in both implementations,
and uses the centered ratio-estimator standard error. These correct earlier
failures. Its original broad escape probability test (0.1<p<0.9) and demand
that both weak-alpha mean negative checks fail remain inadequate; identical
main/positive seeds also provide no independent replication.

verify.py loads its unchanged function definitions (excluding the top-level
main), supplies fresh disjoint seeds and tests both mean and escape probability
against exp(-alpha*T)-weighted conservative paths. Each of six runs has
32,000 photons. For alpha=.1 and .5, respectively:

    mean difference / combined SE = -0.7954, -0.2256
    escape difference / combined SE = 0.2569, -0.6338
    deliberately mismatched alpha escape z = 42.6899, 75.6387
    weighted effective sample size = 31884.2, 30364.6

All 15 checks pass and the certified manifest validates. Four-SE agreement
and six-SE negative thresholds were fixed before running. This is finite
numerical calibration, conditional on sampling and the reviewed code. It does
not establish an absorption theorem, full solver correctness, observational
fit, or novelty. No literature novelty search was warranted for these standard
calibration identities. The initial manifest command rejected a missing seed
field before execution; correcting the audit contract did not change any
research-worker setting or run.

Next: Qwen must implement the actual cap bracket/generator certificate as a
small prerequisite, with the same computed angular predicate in every mode.
For absorption, replace the broad probability check with the comparison above,
retain disjoint positive seeds, and calibrate alpha=0 separately (absorption
distance infinity). Do not claim a discovery from this prerequisite.
