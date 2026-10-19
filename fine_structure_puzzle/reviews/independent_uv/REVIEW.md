# Independent UV audit

Primary verdict: **conditional on named inputs**: the universal one-loop gravity-step equations and the supplied MSbar weak/strong/Yukawa boundary matching. The fixed-point algebra and quoted reduced-SM numerical values survive this audit. Neither absolute alpha, empirical input independence, global inverse-fit uniqueness, nor a gravity calculation follows.

This is a fresh subagent review of FSP-000, Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty workspace, on 2026-10-19 UTC. The reviewer read raw equations/code/results/manifests and exact-version primary sources. The author’s `uv_selection/REPORT.md` and coordinator’s `reviews/UV_MATRIX_REVIEW.md` were not read. No files outside `reviews/independent_uv/` were changed. Independence concerns the reasoning session and numerical formulation; common model/source assumptions remain.

## Claim card and dependency graph

For real symmetric positive semidefinite H=GG^T, fixed real symmetric positive-definite B, constant scalar F=16 pi^2 f_g>0, and t=ln(mu), audit

`dH/dt = (H B H - F H)/(8 pi^2)`.

The claims are: unique **invertible fixed point**, its matter-sector stability at fixed F; continuum of finite-scale matrices approaching a rank-one interacting endpoint; fixed-point top/bottom difference ratios for exactly two specified mixed Abelian models; and one distinct reduced-SM inverse boundary experiment.

Dependencies are:

1. Charge tables + one-loop trace weights -> B; triangular beta equations + g1^2=(5/3)gY^2 -> the H equation.
2. H equation + invertibility -> H*=F B^-1; fixed F -> its linearization.
3. H equation + positivity -> whitened projector fixed points and explicit continuum.
4. Two nonzero Yukawa fixed points + universal f_y + charge norms -> Yukawa difference; full-rank H* -> gravity-independent ratio.
5. Reduced-SM equations + supplied boundary data + chosen crossover + chosen interacting branch -> numerical inverse fit. This branch does not inherit the B-L/chi matter content or ratios.

Leaves 1 and 4 use checked primary equations. Leaves 2 and 3 are algebra below. Leaf 5 uses floating integration and conditional physical matching, not a theorem about the full theory.

## Obligation matrix

| Obligation | Outcome | Scope |
|---|---|---|
| Exact-version charge and beta transcription | passed | Carone v1 tables I-II, equations (3)-(5),(16)-(18) |
| Unique invertible fixed H | passed | B positive definite, F>0; excludes singular fixed points |
| Matter stability sign/normalization | passed | fixed F, t=ln(mu), positive Jacobian eigenvalues +2 f_g |
| Rank-one endpoint admits continuum | passed | explicit positive-definite finite-scale family, fixed endpoint |
| Mixed-model Yukawa ratio | passed | both Yukawas nonzero and full-rank Abelian fixed point |
| Reduced SM central numbers | computationally verified | one independent local solve, float64, stated cutoffs/tolerances |
| Second crossover number | computationally verified | independent forward integration at supplied fitted parameters |
| Local parameter determination | conditional | supplied finite-difference Jacobian supports local rank; no certified bound |
| Global uniqueness over branches/parameters | not addressed | neither the scripts nor this bounded review prove it |
| No direct electromagnetic numerical input in inverse code | passed | inspected dependency path; no gY/alpha_em target used |
| Empirically independent weak/MSbar matching | conditional | imported extraction was not independently reconstructed |
| Exact gravity/full flavor/thresholds/alpha(0) | out of scope | not computed |

## Decisive algebra and signs

Invertible fixed H satisfies H B H=F H, so B H=F I and H*=F B^-1. Conversely this H* is positive definite and fixed. Its derivative on any symmetric perturbation D is

`[D B H* + H* B D - F D]/(8 pi^2) = F D/(8 pi^2) = 2 f_g D`.

Thus all three two-by-two symmetric matter directions have **positive** beta-Jacobian eigenvalue +2 f_g. They are UV repulsive for increasing t. If critical exponents mean minus the beta Jacobian, those exponents are -2 f_g. The source script instead rescales vector fields by 16 pi^2, yielding its listed +2F. None of these is the stability spectrum of a jointly evolving matter-plus-gravity system. In this autonomous positive-matrix system, convergence to the full-rank endpoint itself requires the constant trajectory H=H*: the whitened eigenvalues below show that any initial eigenvalue below 1 tends to 0 and any above 1 encounters a pole.

Set X=B^(1/2) H B^(1/2)/F. Then X'=2 f_g(X^2-X); its positive-semidefinite fixed points are orthogonal projectors. For any fixed rank-one projector P and any 0<c<1,

`X(t)=P+a(t)(I-P), a(t)=c/[c+(1-c)exp(2 f_g(t-t0))]`

is positive definite at every finite t>=t0 and tends to the **same** interacting endpoint P. Different c give different finite-scale H. This supplies the smallest counterexample to any stronger claim that “an interacting UV endpoint” alone selects a unique finite-scale coupling matrix. It does not contradict uniqueness of the invertible fixed point itself.

At a rank-one P the symmetric X equation has eigenvalues (+2 f_g,0,-2 f_g). The script’s triangular-coupling eigenvalues are (+2 f_g,0,-f_g): at gY=0 the map G -> GG^T is singular and the missing normal H component is quadratic in gY. The different normal eigenvalue is therefore expected, not a sign error.

Writing q_u,q_d for the right-handed quark charge vectors, subtracting beta_yt/yt and beta_yb/yb gives, at two nonzero Yukawa fixed points,

`D_y = yt*^2-yb*^2 = q_u^T H* q_u - q_d^T H* q_d`.

The common left-doublet, non-Abelian and universal Yukawa-gravity terms cancel. In the stated triangular convention gY^2=H11-H12^2/H22. At full rank this is F/B11. Direct two-by-two inversion gives:

| Model | B | det B | D_y/F | D_y/gY*^2 |
|---|---|---|---|---|
| B-L | [[41/6,16/3],[16/3,11]] | 841/18 | 2/841 | 41/2523 |
| chi | [[41/6,-2/9],[-2/9,497/27]] | 20369/162 | 18/20369 | 123/20369 |

These ratios are independent of F inside the stated branch. Their absolute scale is not. One cannot substitute measured low-energy Yukawa differences directly into this UV identity without the intervening model flow.

## Independent numerical assertion

`independent_squared.py` does not import or execute `inverse_bvp.py`. It integrates k_i=1/g_i^2 and u=yt^2,v=yb^2 as state variables; gY^2 is also a state below the step. Above the step k_i'=2 f_g k_i-2 b_i/(16 pi^2). As an orthogonal invariant it integrates

`d ln(u/v)/dt = [6(u-v)-2 gY^2]/(16 pi^2)`.

For the reduced SM UV branch, h*=16 pi^2 f_g/(41/6), u*=v*+h*/3 and f_y=(6v*+h*/12)/(16 pi^2). One local root solve began at (f_g,v*)=(0.0062,5.3e-6); it did not use gY or alpha as a target. No scan was performed.

| Quantity | Independent central fit | Supplied central result |
|---|---|---|
| crossover GeV | 1.22089e19 | 1.22089e19 |
| f_g | 0.006297365033156366 | 0.006297365030974549 |
| f_y | 7.699706472032779e-5 | 7.69970646936368e-5 |
| y_t(mt) | 0.9349999999999928 | 0.9350000000000532 |
| y_b(mt) | 0.013599999999999878 | 0.013600000000001817 |
| gY(mt) | 0.3126631747885685 | 0.3126631747521843 |

The gY difference is 3.64e-11. The independent ratio-integral discrepancy is 9.72e-14; inverse gauge boundary errors are <=3.19e-12 relative. Reducing the UV log-span from 4000 to 2000 while tightening tolerance changed Yukawas by <=3.36e-12 relative. These are numerical consistency checks, not interval-certified error bounds.

A forward check at the supplied fitted parameters for crossover 2.435e18 GeV gives gY(mt)=0.3203507536154436, with both Yukawa targets accurate to 4.14e-11 relative. That second case was not independently refitted. The supplied Jacobian determinant about 0.032 and nonzero singular values support local identification only. A successful solver and local Jacobian do not prove absence of other roots or other UV branches.

## Source and input independence checks

[Carone, *Implications of asymptotic safety in two minimal Z-prime models*, arXiv:2512.12044v1, 12 December 2025](https://arxiv.org/html/2512.12044v1): authenticated title/version/author; checked tables I-II, equations (3)-(5),(8),(13),(16)-(18), and Appendix A. The transcribed charges/coefficient signs match. Its F=1.5473 is calibrated from hypercharge; the script uses it only in fields explicitly labelled `illustration_only`. It cannot support an independent absolute prediction. Appendix A supplies the imported boundary values but does not establish independent matching here.

[Eichhorn and Held, *Mass difference for charged quarks from asymptotically safe quantum gravity*, arXiv:1803.04027v2, 23 October 2018](https://arxiv.org/html/1803.04027v2): authenticated title/version/authors; equations (1)-(5) match the reduced-SM normalization and nonzero-Yukawa branch used by the inverse experiment. The step scale and present-day boundary choices are additional declared experiment assumptions.

The inverse calculation has no direct electromagnetic or hypercharge numerical input. This is a code-level dependency statement. Its measured weak coupling and MSbar Yukawa data are inputs; their extraction, electroweak matching, correlations and thresholds were not audited. In particular a tabulated weak coupling can be obtained using electromagnetic observables, although independent measurement strategies are possible. Thus this review neither proves empirical noncircularity nor finds an unavoidable algebraic circle in the inverse code. The input file correctly records that limit.

## Commands, provenance and remaining gap

The authoritative new run is `run-001/manifest.json`, status `completed`, runtime 0.808283 s, Python 3.9.6 / NumPy 1.26.2 / SciPy 1.11.4, macOS arm64. The installed mathbox runner imposed 60 s wall / 50 s per-process CPU caps and conventional one-thread library environment settings; the latter do not certify an actual thread count. Exact argv, unchanged input hashes, output hashes and limits are in that manifest. The launch was:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract fine_structure_puzzle/reviews/independent_uv/contract.json --input fine_structure_puzzle/reviews/independent_uv/independent_squared.py --input fine_structure_puzzle/uv_selection/inverse_inputs.json --input fine_structure_puzzle/uv_selection/inverse-002/result.json --output fine_structure_puzzle/reviews/independent_uv/run-001 --result fine_structure_puzzle/reviews/independent_uv/run-001/result.json --timeout 60 --max-output-bytes 100000 --max-cpu-seconds 50 --max-threads 1 -- python3 fine_structure_puzzle/reviews/independent_uv/independent_squared.py --output fine_structure_puzzle/reviews/independent_uv/run-001/result.json
```

All three manifests, supplied `uv_selection/run-003`, supplied `uv_selection/inverse-002`, and new `independent_uv/run-001`, passed the installed `validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula` hash validation. Historical scripts were inspected rather than rerun. Source full text was not retained; exact-version URLs are the source locators, with no invented local source hash. `HASHES.json` pins the inspected local files and this report.

The smallest remaining implication for an absolute alpha claim is the bridge from these conditional truncated-model relations and imported matched inputs to a uniquely selected, empirically independent physical electromagnetic prediction. No such bridge is supplied here. The strongest safe result is the branch-qualified exact algebra plus the independently reproduced reduced-SM correlation. The cheapest next check for a precision-independence claim is an explicit observable-to-MSbar input/matching dependency table; no broader numerical search is justified by this audit.
