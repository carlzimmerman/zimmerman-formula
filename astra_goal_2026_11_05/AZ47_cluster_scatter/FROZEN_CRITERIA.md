# AZ47 new G3 bookkeeping regrade, frozen after scatter measurement

Kappa=1/2 FITTED; not theory closed. Protocol75abae6f8b preceded the
measurement. Freeze scatter.json SHA256
07ab94b63fa6e9cb030c4c6408aa6ce5b2e48f548b08ec13b0dbf7e917e83adb
before any candidate evaluation under this regrade. No BK2 files change.

## Measured input and limits

Four complete training clusters: A1795,A2142,A644,ZW1215. Three untouched
holdout clusters: A2029,A2319,A85. At x={.1,.2,.3,.5,.7}, empirical
mass-ratio scatter is {.0680160923,.0764009311,.0785021633,.1059399246,
.0668666612}dex. All10 measurement/known-answer/precision checks pass.
The5x5 empirical covariance has rank3. Radial correlations range.632–.997.
Noise subtraction before PSD projection gives four negative eigenvalues;
the positive remainder is rank1. Thus a scalar scatter inflation cannot
stand in for an empirically calibrated independent-point chi-square test.

Freeze the full intrinsic PSD covariance C_int from that file, not only
its diagonal. This is an explicit estimation assumption conditioned on
four clusters and unknown within-cluster measurement covariance. Also
retain all leave-one-cluster-out C_int estimates for sensitivity. No
holdout is used to choose C_int. No candidate-specific residuals enter
its estimation, and no systematic mean radial trend is subtracted from
the candidate's mismatch to make it pass.

## Regrade population and calculations

Regrade every retained hit in the on-disk BK2 L1/L2 real and scrambled-
control harvests on both footings, using the original formula decoding,
leaf definitions and train/control transformations. Stream files in
bounded chunks. Keep duplicate-hit counts distinct from unique formulas;
no exhaustive grammar-census claim is possible because prefiltered-out
expressions were not retained. Do not rerun or extend the closed search.
Evaluate all archived stage2 near-miss formulas as a separately labelled
small pilot, not as a substitute for the retained-harvest census.

For each candidate and cluster, d=log10(go/F). Nonfinite/nonpositive
predictions are rejected. Keep original G3 LINE mean/rms thresholds
.05/.10dex and original level Zm (cluster-mean standard error plus.12dex
HSE floor) unchanged. Reproduce original Z_shape with original diagonal
D=se^2+sm^2 and unweighted residual mean as an anchor.

Two new diagnostics, clearly distinguished:

1. Diagonal bookkeeping: add diag(C_int) to each radial D entry and
   recompute the original unweighted-mean Z_shape formula. This ignores
   correlations; report counts but do not treat it as the primary regrade.
2. Covariance-aware conditional shape: each cluster block is
   V_c=diag(D_c)+C_int. Use all blocks to fit ONE common GLS intercept,
   mu=(1^T V^-1 d)/(1^T V^-1 1), and Q=(d-mu)^T V^-1(d-mu).
   Set Z_cov=(Q-(N-1))/sqrt(2(N-1)). The conditional ERR flag requires
   abs(original Zm)<=2 and Z_cov<=2. Repeat with each leave-one-out
   frozen covariance, without dropping clusters from the grading set.
   A stable conditional flag must agree for every covariance estimate.

Report both a0 footings separately. For exact original anchors use BK2's
stored canonical9.360324825027975e-11; the new goal footing is9.3603e-11.
Evaluate the new canonical regrade at the goal value, report the tiny
normalization difference explicitly, and never modify stored references.
Alt remains1.1312e-10. Candidate constants remain FITTED/selected by BK2;
adding scatter does not undo search selection or cure other gate failures.

## Controls and numerical checks

Known answers: reproduce archived stage2 G3 mean,rms,Zm,Z_shape within
1e-8 relative or1e-10 absolute at the exact old footing; compare block
GLS with an independent dense solve to1e-10 absolute; on a diagonal
equal-variance fixture recover ordinary mean/chi-square; on a constant
residual recover Q=0; adding covariance must not decrease the minimized
Q (check the correct direction: Q_with_cov <= Q_without_cov).

MUTATE sets C_int=0 in a separate output tree. Its legacy-mean diagnostic
must recover old Z_shape to1e-8 relative or1e-10 absolute. A predeclared
synthetic fixture of four five-point clusters with D=.01^2 I,
C_int=.1^2 I and residual vector[-.1,-.05,0,.05,.1] repeated per cluster
must be accepted with covariance and rejected with zero covariance.
For real retained hits report how many conditional flags the omission
changes; if none change, state that the real-data control is ineffective.
Never manufacture a real candidate pass to make the mutation bite.

Stream chunk sizes1000/2000; counts/flags exact, extrema and reported
statistics<=1e-10 relative, same-size rerun scientific output byte-identical.
Verify matrix results against40/80-digit arithmetic on the law anchor and
one saved near miss per footing. Any missing identity, stale input,
unmatched formula or inconsistent pair makes that census UNDECIDED.

## Interpretation and execution

Conditional WINDOW means some retained formulas pass the covariance-aware
ERR flag stably across leave-one-out covariances; FAIL means none do after
all retained hits are processed with controls/pairs passing. Mixed flags
are UNDECIDED for those formulas. This is a G3 bookkeeping result only,
not a new BK2 survivor or a replacement for other gates. A calibrated
population-level G3 p-value remains NO VERDICT because four clusters,
estimated covariance, missing radial measurement covariances and the
original search selection do not justify treating Z_cov as standard normal.

One thread, bounded memory. Pilot may run in minutes under1GB; any full
harvest processing exceeding the light-job envelope uses heavyq after
the light-tier work, with atomic rolling checkpoints, SIGTERM/resume and
input hashes. Full retained-hit totals, both-footing main/mutation outputs,
known answers, convergence pairs, and README are required before final
lane completion. A pilot-only result must remain IN PROGRESS.
