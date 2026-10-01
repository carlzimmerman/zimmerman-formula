# Independent FGF007 gradient-energy audit

**Verdict: implementation and finite assertion verified on the declared72 cases, subject to the stated high-precision numerical tolerances.** The accompanying analytic remainder and limit arguments pass. The small-background warning concerns relative approximation and normalized limits; both raw iterated energy limits are zero. No nonlinear PDE instability or ghost follows.

## Independence, representation and computation

The independent energy/limit derivation was frozen at2026-09-30T15:35:02.646053+00:00 before reading any new worker or root proof or receiving a formula preview. Its sources were task007 and the pinned stage03 dynamics action. A harmless initial document-writing syntax error is recorded in the receipt; it occurred before any file was written or mathematical run launched. The reviewer subsequently wrote its own source-energy code and ran it once before reading the worker implementation. A coordinator message describing the worker's representation arrived after the reviewer code was fixed and before that run; no implementation was copied or altered in response.

The reviewer uses t=sqrt(B/a) and a forward map f(y), where y=B/a, so source(t)=f(t²). Its integration-by-parts energy is

 w(x)=x t²-integral_0^t 2s source(s) ds.

This explicitly defines the f(s²) notation in the saved output. The worker instead computes direct subtracted-energy integrals: for RAR, integral_(t0)^(t1) (s²-t0²) source'(s) ds for parallel increments, with a separate primitive cross-check. The reviewer subtracts its independently calculated full primitives. For Q the worker's direct gradient integral is also different from the reviewer's source-coordinate construction. Both implementations share the same constitutive mathematics, mpmath library and the monotone RAR root bracket; they are independent code/energy-evaluation paths, not completely independent numerical libraries or interval methods.

The full grid is36 cases per law,72 total: two laws, three x=g0/a values .1,.01,.001, four amplitude ratios .001,.03,.3,1 and parallel-plus, parallel-minus, transverse orientations. The reviewer evaluates the same cases at80 and110 digits. It completed in1.065913 seconds under120-second wall,110-second CPU, one cooperative library-thread and1MiB log bounds, with no claimed memory/affinity cap. Its worst relative cross-precision discrepancy is approximately9.10e-69 for the remainder and normalized remainder, below the predeclared1e-55 tolerance. The worker's60/90-digit run completed in2.086607 seconds with its1e-40 checks passing. These are finite high-precision checks, not rigorous error enclosures.

## Constitutive inversion, signs and cancellation

Both laws use the exact mathematical inverse and energy definitions at fixed a>0. Q's stable inverse y=2x²/(sqrt(1+4x²)+1) avoids subtracting nearly equal radicals. RAR uses source(t)=t²/[-expm1(-t)]; its derivative is positive because2(exp(t)-1)>t. Also source(t)>=t, so [0,x] is a valid unique-root bracket. Both implementations special-case t=0, including the anti-parallel ratio1 endpoint; neither divides by the vanished source coordinate. The derivative 2t/source'(t) gives the correct parallel Hessian eigenvalue and t²/x the transverse one.

The exact mathematical increment after linear subtraction is

 D=w(|x e1+h|)-w(x)-y(x)h_parallel,
 H=[w''(x)h_parallel²+(y(x)/x)|h_transverse|²]/2.

For anti-parallel h_parallel=-rx, the linear contribution is PLUS y rx. Reversing it would give a negative decrement rather than the positive convexity remainder; the reviewer explicitly checks this mutant. Both D and H are positive on every nonzero declared perturbation. The anti-parallel ratio1 final gradient is exactly zero, which is allowed for the finite increment but is not a path uniformly bounded away from zero gradient.

The reviewer checks its Q source primitive against the independent analytic asinh expression, RAR root residuals, signed remainders, and primitive cancellation at both precisions. The worker independently checks direct-integral versus endpoint-primitive differences. These complementary paths are useful precisely because small r produces cancellation in full primitive subtraction.

After the independent run, an administrative comparison of the serialized outputs found agreement in sign, scientific exponent and the first40 significant digits for D,H and (D-H)/H at all72 cases:216 matching value pairs. OUTPUT_COMPARISON.json records that character-level comparison and its source hashes. It is not a separate quadrature or arithmetic error-bound computation. The worker's exact primitive/inversion and precision residuals were also inspected and lie within its declared tolerances.

## Analytic remainders and limits

The parallel Taylor coefficients agree with direct differentiation:

 (D-H)/H=+/-[x w'''(x)/(3w''(x))]r+O(r²).

For a transverse increment, the radial geometry removes the odd term and gives

 (D-H)/H=[x w''(x)/w'(x)-1]r²/4+O(r^4).

These are local fixed-nonzero-x expansions; their constants are not proved uniformly bounded over an arbitrary background interval. Both laws have w(x)~x³/3 in the deep limit, yielding the exact fixed-r limiting D/H values1+r/3,1-r/3 and2[(1+r²)^(3/2)-1]/(3r²). The transverse ratio is1+r²/4+O(r^4). Thus decreasing absolute background and perturbation at fixed nonzero ratio does not make the relative Taylor discrepancy vanish.

At x=0 the leading nonzero spatial energy is w(|h|)~|h|³/3 and the Hessian is zero. The small-amplitude cubic behavior is analytically derived; the six zero-background amplitude checks illustrate convergence rather than proving the limit. The adopted K=2 temporal kinetic coefficient stays positive. Vanishing spatial quadratic stiffness means the nonzero-background characteristic statement ceases to apply at zero; it does not prove a ghost or nonlinear ill-posedness.

For plus-parallel or transverse fixed h>0, x->0 gives D->w(h)>0 and H->0+, hence D/H diverges. In the other order, h->0 at fixed x gives D/H->1, followed by x->0 retaining1. This is normalized nonuniformity. Both raw D and raw D-H approach zero in either iterated order as x,h->0. The ratio is undefined at the exact zero-background point, and neither proof claims raw energy noncommutation. Along h=rx, both raw terms vanish as x³ while their ratio tends the stated nontrivial function of r.

## Finite quantified range, with denominators explicit

Across the declared laws, backgrounds and orientations, the worker and reviewer agree on the following finite maxima. These are proportions, not percentages or universal bounds outside the grid.

| amplitude/background r | max abs((D-H)/H) | max abs((H-D)/D) |
|---|---:|---:|
| .001 | .0003333320 | .0003334431 |
| .03 | .0099999609 | .0101009702 |
| .3 | .0999996846 | .1111107217 |
| 1 | .3333328000 | .4999988000 |

The different denominators matter, especially the anti-parallel ratio1 case: about one-third discrepancy relative to H can mean about one-half relative to D. This table quantifies the specified cases only; it is not an empirical error budget or a global percentage threshold for linearization. The exact asymptotic direction dependence is supplied by the analytic argument, not by extrapolating these rows.

## Provenance, units and remaining scope

Both manifests passed the computation-audit validator with the project root, and current input/output hashes, including before/after input equality, were verified. All final worker input/artifact pins match. Code, contracts, raw results and the independent freeze are preserved. No mathematical run failed or was repeated; there was one bounded reviewer run and one author run. No new root proof was read or audited here.

The dimensionless restoration is W=a²w, field energy density a²w/(4piG), and gradient a times the dimensionless vector. The worker retains both9.3619e-11 and1.1279e-10 m/s² and K=2. Frozen H-reference scaling at fixed x,r scales energies by E² and gradients by E; it does not represent fixed physical gradients or an evolving energy-conserving H model. A time-varying prescribed a would retain the prior W_a a_dot work term. No dimensional force or missing mass is inferred.

This closes the bounded relative-linearization audit. Q and RAR stay separate and no registered M action, operative filtered-MONO metric/photon coupling, real-data calibration, coupled-matter stability, global PDE theorem or theory closure is supplied. Further nonlinear or zero-field PDE statements require their own mathematical formulation and proof; this finite energy table cannot supply them.

## Exact pins

- `campaign_fresh_gravity_astra/stage_21/independent_audit/FROZEN_ENERGY_LIMITS.md`: `1b8069a2389bb17df3a3f51c4158b5bc93437ac7c422765894654d592529e7fe`
- `campaign_fresh_gravity_astra/stage_21/independent_audit/DERIVATION_FROZEN.json`: `52b0b9b84c2831991cf39f04cdc7e867999f0cbebb9f34983a7d00818de5ee61`
- `campaign_fresh_gravity_astra/stage_21/independent_audit/check_source_energy.py`: `a65da801c98c728cc34dee7c45818b25f30f0c0465e0f77d7cf56445a21b24b1`
- `campaign_fresh_gravity_astra/stage_21/independent_audit/contract.json`: `c2c5e2c6bd81d3a7d5dd6e5f98715e91951316b5ff5039fa441cea040c263744`
- `campaign_fresh_gravity_astra/stage_21/independent_audit/run_001/results.json`: `9302005082078b0d4407b1557b8d2d22aefdc0e643cd3fce9855859cafb5cf03`
- `campaign_fresh_gravity_astra/stage_21/independent_audit/run_001/manifest.json`: `8f4ec40c711a84f6a2dcb600e2b932d723b51b5824c60e75d096d758ca0b5f43`
- `campaign_fresh_gravity_astra/stage_21/independent_audit/OUTPUT_COMPARISON.json`: `912b53480ccae757cd6522e115ce136189f35d03706ff1d411ead263ac03e3b2`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/DERIVATION.md`: `c103dc2f252ef1be27458dff2ddf60895e33c3f0a680c1028fd5e19a4eab4104`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/check.py`: `181fcac6d29cc913ec7c2f72d6ac992267cafd16db9060c1981c028aede3b653`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/computation_contract.json`: `997af2cd039bc8db4bf320778eb915c1cc49d59a93707ffe2f4f7625828aa06b`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/REPORT.md`: `96e1eab8ff361d4dece50f5025f09a6bea70938a7ada0670455963895b2b9c01`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/result.json`: `165bc799422be7a8610a4fad3b45d55d1b4ec70c70e68c3f590ea7ba41f3d80d`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/numeric_001/results.json`: `8f2732a540a355478a91843d41c4c4567789df643fd29849c3b66dfb0e136071`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001/numeric_001/manifest.json`: `5beaaa2b2dcd364a0597a09630a36f786e88b8efa20ef6f4e73957ea7368ede5`
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-007.md`: `536e67844c83d28f7a50d8d1b2bd91cdb038fb904fd8d475c84e309aa07e8400`
- `campaign_fresh_gravity_astra/stage_03/dynamics_precision/DERIVATION.md`: `41ad39d1521e7d5b5d974e320478faecd944df8d4608b4869a566624244af3ae`
