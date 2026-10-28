# Exact all-halo lens rejection bound: frozen before support arithmetic

Motivation from independent source inspection after the first scalar results: the frozen KiDS score requires
`chi2_ENV - chi2_pureHalo < 0`. X53's corrected ENV profile equals the pure-halo profile whenever all interpolation
grid nodes that carry nonzero lens weight select halo. Both predictions then undergo the same projection and
two-halo fitting, so their chi squared values coincide and the strict inequality fails. This algebraic equality
does not require likelihood continuity or monotonicity with L.

For each fixed footing define, over contributing X53 stellar-grid nodes j,

    Lbound_f = max_j (floor_X53,f/(A*S_cached_A(M200_j)))^(4/5)/q(M200_j).

If L>Lbound_f, all contributing nodes select halo and the strict comparison necessarily fails. Hence
`L<=Lbound_f` is a necessary condition for a pass of this frozen scorer. It is not sufficient. This is a statement
about the implemented finite interpolating scorer, not about a continuous physical population or a universal
empirical lensing window. It does not prove that any L satisfying it passes other calibration lines.

The bound is computed from the actual existing NPZ inventory, original native-distance mapping and fixed LMG
stellar grid. Compute the nonnegative interpolation weights onto LMG exactly as np.interp's clamped linear
mapping, retaining all nodes with strictly positive aggregate weight. Zero/negative/nonfinite input lens weights
and invalid distances must be reported; negative weights stop the nonnegative-support argument. Use the existing
EM1 background-A Mb-to-M200 relation, original gas conversion, X53 cached collapse table and floor units.

Checks: native bin sizes and positive weight counts reported; sparse support weights reproduce direct np.interp
weighted averages on three fixed test vectors (ones, node index, index squared) to relative 1e-12; aggregate
weights sum to original positive lens weight sums to relative 1e-12; selected-node bound implies all support
nodes halo at Lbound*(1+1e-6); at least one support node floor at Lbound*(1-1e-6); repeated output is identical;
mutation corrupts one support coefficient and must fail interpolation/sum checks. Source and data input hashes
are checked stable; manifest records versions, argv and measured RSS. No projection or likelihood is evaluated.

The already frozen sole challenge remains Lcrit_X43_A_canonical(12.3). This bound does not select any new L.
Do not infer a lower group/core L bound from cached score grids. Branch changes and halo-profile redistribution
make a whole-scorer monotonicity or continuity argument unsupported without additional proof.
