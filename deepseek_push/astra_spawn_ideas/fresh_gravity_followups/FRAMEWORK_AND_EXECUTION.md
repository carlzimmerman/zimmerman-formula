# Common instructions for every follow-up worker

Repository root: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Scientific parent: `campaign_fresh_gravity_astra/stage_03/README.md`.
Inherited base Git: eccd1c0e59459b5ec1acf2e916fb7a05a7f67971. The working tree
is shared and dirty: pin actual source bytes, not Git alone.

## Mandatory framework

Use a = kappa c sqrt(G rho_Lambda), with kappa adopted, not newly derived.
Carry a(0)=9.3619e-11 and 1.1279e-10 m/s² when making dimensional predictions.
Primary vacuum branch: constant a for constant rho_Lambda. Separate comparison:
a(z)=a(0)E(z), E²=.315(1+z)³+.685. An H-dependent history is not automatically
the same physical model as constant vacuum density. Pressure relation
a²=kappa²G(-p) equals the vacuum relation only for p=-rho_Lambda c².

For B>0, keep Q: F=sqrt(B²+aB), and R:
F=B/[1-exp(-sqrt(B/a))], distinct. M is the inherited monotone radial branch
and must use its registered implementation when explicitly requested. Never
replace a MOND source requirement with a Newtonian missing mass. Dimensionless
tests may set a_ref=1 if the dimensional restoration and both normalizations
are recorded. Physical scale, vacuum interpretation and empirical normalization
are separate assumptions.

Derive forward from these equations and source-pinned campaign findings. Do not
import a literature mechanism or assert historical novelty. Existing local
observations remain evidence with their own modeling and calibration assumptions.
No fabricated data, confidence interval, covariance or instrument independence.

## Worker execution

Read the task and specified sources only as needed. Check source hashes first;
report a mismatch instead of silently using a changed premise. Write a short
derivation before coding. Define units, signs, support, boundary conditions,
parameter box, stopping rule and negative control. Prefer one discriminating
calculation to a large unmotivated sweep. No pip installs, downloads, service
launches, commits, publications or messages to unrelated chats are needed.

Each numerical process has a requested 120-second wall bound and one numeric
library thread; the dispatcher must enforce and record the actual bounds.
These are per-process limits, not claims that a whole reasoning task finishes
in 120 seconds. Use deterministic controls; record fixed seeds for sampling.
Limit logs to 1 MiB and scientific output to the smallest sufficient tables.
Do not claim a memory limit unless actually enforced. Use the existing
computation-audit runner and validator for load-bearing experiments.

Return `result.json`, `DERIVATION.md`, executable code when used, raw results,
manifest and a limitations paragraph in the claimed run directory. Record
exact commands, environment, input/output hashes, actual tested ranges and
failed checks. Keep an unresolved result unresolved. An exception or a failed
test is not a scientific refutation until its cause is understood.

## Promotion gates

Allowed worker outcomes: `supports_scoped_claim`, `counterexample`,
`inconclusive`, `blocked_on_data`, `implementation_failure`. These are worker
reports, not orchestrator acceptance. Accepted evidence requires a separate
review record that pins the result hash and explicitly scopes the verdict.
Distinguish exact algebra, binary64 tests, noiseless synthetic recovery, real
data reductions and observational likelihoods. Never turn a finite search into
a universal theorem or a likelihood-free discrepancy into a significance.

No standalone lensing, cosmology or global stability claim follows from a
radial acceleration fit. Any new field or coupling is an added hypothesis;
check whether it changes the user's pointwise scale-vacuum relation.
