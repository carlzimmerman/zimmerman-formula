# Independent audit: uniform finite response perturbations

**Verdict: proved as written.** The root proof is an exact conditional theorem over arbitrary real perturbations of one fixed finite response model. This audit accepts neither a numerical error radius nor an actual instrument error budget. The stronger fixed-synthetic-data statement is proved only with its explicitly added 2A<m gate.

## Claim card and independence

U is invertible 15 by 15 over the reals, c has fifteen entries, and L is a row target with zero coefficient on the sixteenth free pressure coefficient s. All vectors use the same declared pressure coordinates and rows use the same saved normalization. Let w=U inverse c, M=||U inverse||infinity, W=||w||infinity, r=L U inverse, K=||r||1, mu=−Lw. For arbitrary real E,e obeying induced ||E||infinity<=epsilon and ||e||infinity<=eta, the hypotheses are M epsilon<1 and gamma<|mu|. For a strictly positive decreasing baseline with appended fixed node zero, all sixteen successive gaps are positive.

Under these hypotheses the response null direction persists with target sign fixed, and a single positive step independent of E,e preserves both strict monotone witnesses. Their synthetic data may depend on the perturbed response. Under the additional 2A<m gate, correcting the baseline gives witnesses sharing one fixed nominal synthetic data vector for every response in the same uncertainty ball.

This subagent independently reconstructed the argument from root ROOT_DERIVATION.md and the task/pinned FGF029 ancestry. No new FGF031 worker or other independent-auditor material was read. Parent FGF029 raw derivation and selected reported rank/target/control information were inspected; its large exact output was not independently recomputed. No mathematical computation or numerical rerun occurred. Hashing was administrative.

## Dependency graph

Pinned finite U,c,L and invertibility (inherited exact saved-matrix evidence) -> induced norm inverse estimate -> exact null-direction perturbation -> nonzero target and rank16 augmentation -> strict-gap witness. Separately, baseline correction plus its norm bound -> nominal-data witness under the extra gap gate. There is no dependency on a gravitational source law, observational fit, continuum inverse result or physical uncertainty calibration.

## Obligation matrix and decisive checks

| Obligation | Status | Decisive check |
|---|---|---|
| Norm convention | Passed | Induced infinity norm is a maximum row sum. Entrywise alpha implies 15 alpha, not alpha. |
| Inverse identity | Passed | U+E=(I+E U inverse)U, so (U+E) inverse=U inverse (I+E U inverse) inverse. The geometric series is controlled by M epsilon<1. |
| Exact direction difference | Passed | (U+E)(w tilde−w)=e−Ew by using Uw=c. |
| Direction bound | Passed | Inverse norm is at most M/(1−M epsilon), giving delta=M(eta+epsilon W)/(1−M epsilon). |
| Sharper target bound | Passed | For any row r and matrix A, ||r A||1<=||r||1||A||infinity: sum over columns and then rows proves this directly. Thus the target bound uses K/(1−M epsilon), not an incorrectly transposed operator norm. |
| Comparison with coarse bound | Passed | K=||L U inverse||1<=||L||1 M. Hence the sharper gamma never exceeds ||L||1 delta. |
| Sign and ranks | Passed | mu tilde=−Lw tilde; gamma<|mu| keeps its sign and makes it nonzero. Rank H tilde is15 from its invertible old block. Its nullspace is exactly the span of (−w tilde,1); the augmented target is nonzero on it, so augmented rank is16. |
| Common monotonic step | Passed | ||v tilde||infinity<=Z=max(1,W+delta). With appended v16=0, every successive difference has absolute value at most2Z. h=m/(4Z) preserves each gap by at least m/2. |
| Fixed endpoint and positivity | Passed | The endpoint perturbation is exactly zero. The last gap is the last free pressure itself; keeping all gaps positive implies every free coefficient remains positive. |
| Target separation | Passed | The signed difference is2h mu tilde, so its magnitude is at least2h(|mu|−gamma)>0. Both profiles use the same perturbed operator and exactly the same perturbed baseline data. |
| Fixed-data correction | Passed | (U+E)(x+a)+(c+e)s0=Ux+cs0 when a=−(U+E) inverse(E x+e s0). Its infinity norm is at most A as printed. |
| Fixed-data gap gate | Passed | Extend a by a15=a16=0. Every baseline gap changes by at most2A. If2A<m, h0=(m−2A)/(4Z) gives gaps at least(m−2A)/2. The null pair shares the nominal d0 and has the stated nonzero target difference. |
| Scope of numerical radius | Passed as limitation | Root does not claim that 2A<m holds for any worker-selected radius. No radius is checked by this audit. |
| Controls and physical units | Passed | Zero perturbation recovers the direction and zero baseline correction. Threshold failure is inconclusive. Row/pressure unit changes require simultaneous transforms of all operators, targets, baselines and bounds. |

The sharper target bound can also be seen directly: put d=e−Ew and N=(I+E U inverse) inverse. Then mu tilde−mu=−r N d; |r N d|<=||r||1||N d||infinity<=K||N||infinity||d||infinity. This reconstructs the printed bound without any unjustified matrix-norm interchange.

For units, in a common response normalization U,E,c,e have data/pressure units, M has pressure/data units, w and Z are normalized direction components, and delta is dimensionless. Thus M epsilon is dimensionless. K has target/data units, mu and gamma have target/pressure units, h,h0,m,A have pressure units, and the separation bound has target units. Different row units require their declared normalization before these norms are meaningful. The proof explicitly fixes this convention.

## Controls, exclusions, and remaining implication

Invertibility alone is insufficient: a target can annihilate the surviving null direction. Strict inequality gamma<|mu| supplies the missing target condition. Weakly monotone baselines with m=0 are excluded and would not justify the positive common step. Omitting the final free-node-to-zero gap could lose positivity. Keeping p unchanged generally gives H tilde p different from d0; the corrected p bar, and the extra margin 2A<m, are essential for the stronger result. Assigning different nuisance operators to the two profiles is not used.

All seven task-pinned ancestor file hashes matched at audit packaging. This is source identity verification, not new verification of every parent numeric coefficient. Root theorem and exact parent algebra are the inspected mathematical sources. No external theorem or literature mechanism is imported beyond the elementary inverse-series argument reconstructed here.

The strongest accepted statement is uniform ambiguity for the exact finite response uncertainty set whenever the displayed inequalities hold; additionally the fixed nominal synthetic data version holds when2A<m. One exact rational certificate can establish a chosen mathematical radius, but it remains separate from calibrated instrumental/continuum uncertainty. Establishing such an actual error budget and an outer-pressure constraint sensitive to this mode remains an empirical obligation. No acceleration/mass is computed; any later conversion needs pressure/density calibration and the chosen distinct MOND Q/RAR/M law, both reference normalizations and separate vacuum/H histories. No physical metric or theory closure follows.
