# Frozen nonlinear-domain error propagation

Use nonlinear_001's original-input analytic halo endpoint enclosures; do not
rerun them. Reconstruct only65 analytic law profiles from its certified Ms,Mc
intervals and original G,a0 constants. Save outward law arrays. All127 branch
and124 root conditions are inherited with their original-input scope.

For each halo coordinate form delta from new endpoint bounds minus OLD
baseline bounds: dl=new_lower0-old_upper0, du=new_upper1-old_lower0. Compute
nonnegative extension outside the published old signed delta interval. Divide
by old_upper1, and take epsilon as the largest extension ratio across halos
and largest law-error/saved-law-mass ratio. Derive lambda>=1 from all
new_upper1/old_upper1 and new-law-upper/saved-law ratios. Both quantities are
numerical enclosure/error majorants derived from inputs, not physical fits.
Use directed basic-operation bounds; independently check exhaustive exact
rational inequalities afterwards. Any nonfinite/negative denominator fails.

The previous positive source-path majorants U are linear in mass and dominate
the absolute ideal projection map. Therefore new domain perturbation is at
most epsilon*sum_tail U per native row. This also covers differences of the
law profile. Clipping the halo delta to the old interval keeps its existing
coefficient/anchor budget valid; project the extension through the ideal map.
Scale previous source-forward and catalogue error bounds by lambda. Their
mass-dependent components are positive linear, while additive underflow
allowances remain bounded when multiplied by lambda>=1. In particular the
catalogue table B and its B+1 underflow expressions grow by at most lambda.
Use existing exact weights/covariance/dual/template and unchanged cutoff.
Do not scale or add the old anchor/coefficient budget twice.

Exact extra per row = prior_anchor_inflation + epsilon*sum(U)
 + lambda*(source_forward_error + catalogue_error).
Recompose the exact rational dual from original residual boxes. Stress checks
must confirm finite arrays, inherited controls, positive envelopes, root-side
and constant-M,R premises, and a wrong-mass/budget mutation. Independently
reconstruct selected law values at70digits. Resource wall600/CPU480, one thread,
source/input hashes before/after. If inconclusive, preserve the outcome.

Analytic compact-branch mass order uses the existing h-decreasing proof for
r<R; at r>=R the matched truncated halo mass is M, independent of L. Parent
M,R and baryons are constant in L, and columns increase as L^(5/4). Endpoint
compact roots imply no saturation in between. State these analytic premises
and source-domain restrictions explicitly. Original libm/root-solver and
floating continuum behavior are not certified here; no real-L/global claim.
