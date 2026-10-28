# IP28-F: footing evidence audit, criteria frozen before new execution

Base checkpoint: 7954d48377463cafcae3e8dbb09454134aef384f (dirty shared tree).
Scope: independently enumerate stored finite grades, audit the meaning of the
SPARC gate, preserve both footings, and decide what the present evidence licenses.
No raw-data refit, new physical parameter, or change to existing lanes.

Assertions tested:
1. Recompute CF1/CF2/CL1/CL2/CL3 grade counts from each lane's result JSON;
   compare with LEE1's census. Compare the 24 stored draw failure lists with pass flags.
2. On CL3's three levels and BS1's primary point, separate the residual threshold
   rms <= 0.110 from the survey-calibration gate 0.50 <= median Upsilon <= 0.80.
   Verify the conjunction reproduces each stored SPARC pass flag.
3. Classify alt failures by line rather than claiming all individual observables fail.
   Do not interpret configurations as independent experiments or probabilities.
4. A mutation replaces the lower Upsilon gate by 0.40 and must disagree with stored
   flags; this diagnostic change is never adopted as a new grade.

Input ledger: result JSONs are derived numerical evidence; scorer sources define
the gate; Upsilon bounds are inherited survey-calibration judgments. This audit
adds no direct astronomical measurements. Full upstream inputs are not revalidated.
Finite results do not establish universal exclusion of a0 or a new theory mechanism.

Execution: one thread, nice 15, standard-library Python, seconds, <1 GB RSS.
Write only this new directory. No commits: .git is read-only in the current sandbox;
freeze tracked by file hashes and manifest, not represented as a committed preregistration.
