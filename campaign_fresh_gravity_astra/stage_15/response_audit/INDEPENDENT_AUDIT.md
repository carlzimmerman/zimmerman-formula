# FGF029 independent response and limited target audit

**Primary verdict: computationally verified only in a stated range.** The single added pressure-response column agrees with an independently implemented direct line-of-sight calculation across all fifteen inherited annuli. The finite support extension is consistent with the declared cached geometry/beam/mask model. No observed pressure extension, calibrated gradient, covariance or force inference is accepted.

Auditor `/root/metric_intake`, 2026-09-30. The implementation was fixed and hashed in `IMPLEMENTATION_FIXED.json` before reading the FGF029 worker source. It adapts the previously reviewed stage13 independent direct-LOS method using the new hat definition from the task, not the worker's Abel projector. Worker source was inspected only after this independent implementation was frozen and the bounded comparison launched. The script hash still matches that receipt. All writes are confined to this response-audit directory.

## Changed assumption and mathematical response

The old free pressure nodes through x=4 remain unchanged. A new free coefficient at x=5 is added, with the fixed zero endpoint moved from x=5 to x=6. Its basis function is h(r)=r−4 on[4,5], h(r)=6−r on[5,6], zero elsewhere. The old node4 hat still falls to zero at5: superposition with the new hat produces the new segment between the two free nodal values. Thus the old fifteen columns are legitimately retained, rather than silently redefined.

Only the new column is constructed. The observed-model rows remain the same twelve annuli through2 plus[2,3),[3,4),[4,5), with fixed post-convolution offset zero. There is no newly added [5,6) measurement row. Outer source material can still contribute to inner projected annuli through line-of-sight projection and the beam. This is an explicitly expanded synthetic source model, not extrapolated or measured actual pressure.

## Independent response calculation and controls

The new hat was integrated directly over positive line-of-sight distance on its two radial segments, using32-point Gauss–Legendre quadrature, then doubled. Each segment uses l_lower=sqrt(max(r_lower²−t²,0)) and l_upper=sqrt(r_upper²−t²) for t<r_upper. The fixed integrand is the new linear pressure hat evaluated at sqrt(t²+l²); the script does not call a candidate Abel primitive. Source projection is exactly zero for t>=6 by construction.

Spherical pixel radii were independently reconstructed using atan2 of the angular cross-product magnitude and dot product, the actual FITS WCS and inherited fiducial distance. It recovers DA=299.1293131965726 Mpc and theta_target=0.004185480809689986 rad. Map/mask WCS agreement at four corners and center is exact at the reported pixel precision. The minimum source-patch edge radius is8.830269576083204, exceeding the required support6.

The declared finite beam convention is unchanged: 512-square source, zero-padding to1024, angular pixel spacings in radians with longitude*cos(center declination), ell=2pi|frequency|, cached transfer and cutoff ell>17000, then central512 crop. The independent implementation uses NumPy FFT; the worker uses SciPy FFT. This is an independent numerical check of the same finite approximation, not authentication of its physical calibration or a proof of padding/flat-sky error control.

The fifteen annular weights are independently reconstructed from finite map/mask pixels with positive mask, normalized by their mask sums. Every resulting weight-array hash matches the pinned FGF028 geometry. All rows are nonempty and preserve a constant post-convolution offset. The outer three valid-pixel counts remain13036,18240,23474, all mask1. No observed y values were fitted, and pixel counts are not treated as independent noise counts.

Predeclared coefficient tolerance was absolute1e−10 plus relative2e−9*abs(reference). One bounded run passed, with no refinement or fullmatrix rebuild:

- Maximum difference on the first twelve rows:4.440892098500626e−16.
- Maximum difference on the last three rows:8.881784197001252e−16.
- Maximum across the entire new column:8.881784197001252e−16.

These are finite binary64 comparison errors, not uncertainty on a measured response or a continuum convergence certificate. The comparison covers the sole changed column; it does not independently reconstruct the unchanged fifteen columns.

## Worker source review after implementation freeze

The inspected `extend_support.py` uses exactly the two analytic segments[-4+r] on[4,5] and[6−r] on[5,6], retains the old matrix, and verifies radius, map/mask patches, transfer and every normalized weight hash against FGF028. Its support containment check is explicit. Direct LOS point checks include t=0, both new knots and the support endpoint. The new extended matrix appends the column without changing any old column; setting its amplitude to zero therefore recovers the old source model exactly. The old hats and new hat jointly define a continuous piecewise-linear sixteen-coefficient profile ending at fixed zero6.

The source/crop/beam operations and source support are consistent with the stated finite model. They do not establish that real pressure vanishes at6, that spherical symmetry or the fiducial distance is accurate, or that beam tails and map calibration errors are negligible. The same cached map supplies all rows, so no independent-observation assumption follows.

## Limited review of root target/null proof and code

The root `target_audit/DERIVATION.md`, `check.py` and completed record were inspected without another computation. Let U be the old invertible15-by15 pressure response, c the new column, and rU=L. For x the old pressure coefficients and s=p(5), exact modeled data satisfy x=U^-1 d−U^-1 c s. Hence target t=Lx=r d−(r c)s. The null direction v=(−U^-1 c,1) has target response mu=Lv=−r c. Nonzero mu, rather than dimension counting alone, proves target nonidentification.

The root code computes the null vector by exact rational row reduction of the complete15-by16 stored matrix, checks H v=0, solves the old full transpose independently and verifies mu=−r c. It preserves the original target coefficients at x=.9 and1.1, with zero coefficient on new p(5). The recorded mu is0.16303084957824435 in dimensionless pressure/target units. Thus the target rank grows from15 to16 when appended, while the measurement matrix stays rank15. Exactness is about rational interpretation of stored binary64 coefficients, not the continuum response.

For the new strict witnesses, the root uses an explicitly different rational baseline1e−5/(1+x)² at all sixteen free nodes, not the worker's exponential baseline. Both are synthetic extended-support profiles; neither is fitted to the actual map. Half the minimum positive nodal-gap ratio gives both-sign strict positivity/monotonicity and exact same model bins; the final p(5)>0-to-p(6)=0 gap is included. Root's reported fractional witness width0.0006991088561092925 and the worker's0.0004023457357931149 are different finite examples, not competing bounds or disagreement about mu. Neither is a maximal feasible width or a claimed explanation of an empirical discrepancy.

An extra row(a,b) has reduced response k=b−aU^-1c. In this one-dimensional nullspace, k!=0 identifies s and hence the target; k=0 leaves this ambiguity. The coordinate row selecting s is an algebraic positive control, and duplicating an old row is a negative control. The root also checks that fixing s=0 restores old identification and that an altered target fails the original target relation. No suitable additional physical measurement is thereby supplied.

The target-width formula |r c|Delta s is valid for exact old bins and an externally justified interval for s before imposing other feasibility constraints. It is not a confidence interval and does not invent a measured support uncertainty. This review accepts the algebraic implication and code logic; root owns its separate exact execution. No target/null computation was rerun here.

## Execution, pins and scope

The independent response check has a saved source, predeclared contract, implementation-freeze receipt and bounded `run_001/manifest.json`. The recorded command completed with exit0 under120 seconds wall,110 seconds per-process CPU and cooperative one-library-thread environment. No memory cap is claimed. Manifest validation returned `valid evidence record; mathematical interpretation requires review`. Exact run timing, environment, source/output hashes and input pins are preserved; the actual map, mask and beam are pinned, not replaced by invented response rows.

All hashes used in this review are in `audit_result.json`. No old script top-level was imported. No failed computational attempt or tolerance adjustment occurred. There was one changed-column check and no support sweep, annular redesign, data fit or separate force computation.

The accepted scientific scope is a reproducible finite response for one released outer pressure coefficient, with unchanged measurement weights, plus the scoped algebraic loss of target identification under that changed source-support premise. Actual support/calibration, noise/shared-map covariance, distance/geometry systematics, observed pressure and density/composition remain missing inputs. The additional source coefficient is not a newly observed component.

No MOND source or mass inference is made. A later bridge must preserve both registered a0 values, separate constant-vacuum and H(z) histories, and distinct Q/RAR/registered M laws while converting electron to total pressure and supplying density. This finding neither closes nor refutes the physical gravity theory; it identifies a specific source-support assumption on which the prior finite target recovery depended.
