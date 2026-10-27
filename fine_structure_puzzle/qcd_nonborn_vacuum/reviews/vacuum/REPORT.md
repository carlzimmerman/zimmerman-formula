# Independent vacuum normalization and source-admission audit

**Primary verdict: conditional on a named input.** The unconditioned sphere response and its charge derivative are correct finite-regulator identities, with the fixed-physics contact prescription and limiting hypotheses stated by the author. They leave the physical sphere coefficient and derivative undetermined. Bai--Chen's flat-vacuum estimate cannot be admitted as a connected susceptibility bound from its displayed pointwise inequality alone: the missing input is a QCD-specific comparison of the **renormalized, connected, contact-prescribed scalar zero-momentum response with the topological susceptibility**. Even granting that comparison would not determine the sphere coefficient.

All full-theory A, R and physical alpha remain **unset**. No author file or shared cache was changed.

## Independence and exact revisions

`PRETARGET.md` was saved before reading either author's derivation or code, and before reading the mathematical content of either source. `CRITICAL_SOURCE_PRETARGET.md` was saved after reading Bai--Chen, before opening `vacuum_global/DERIVATION.md` or the coordinator LET packet. Their initial SHA-256 values are pinned in `INPUTS.json`. Thus the two critical deductions were reconstructed without the author's formula or verdict. Later code comparison and tests are informed audit work, not claimed blind replication.

Reviewed frozen global derivation SHA-256:
`32fde2450bd0dd3355d9d2cce6b4fa26c407f69301194f3ea47139d6e5056264`.
Reviewed global code SHA-256:
`809c9bd20d771767a300845881e3f00be2f1ff3554408ddd44270f48d3c12d5c`.
The complete before/after pins for all 27 author artifacts, including the coordinator derivation, inputs, sources, code and results, are in `INPUTS.json` and `run_001/RESULTS.json`. No pin changed. The 12 historical upstream science pins in global `INPUTS.json` also match current bytes; see `UPSTREAM_PIN_CHECK.json`.

## Reconstructed claim and dependency graph

The input is one common finite positive regulated measure exp(-S(t,u)), with all integration-variable Jacobians absorbed into S, W=-log Z, V=Omega exp(4t), H=exp(-t), and rho=W_t/(4V). The t path fixes renormalized physics. The u path must specify which other renormalized parameters are fixed. Derivatives require finite moments and justified differentiation under the integral.

The logical dependencies are:

1. normalized differentiation -> W_t=E[S_t] and W_tt=E[S_tt]-Var(S_t);
2. volume differentiation -> E_defect=W_tt-4W_t=4V rho_t;
3. a differentiable small-H expansion with remainder q_t=o(H) -> A=-lim H^3 E_defect/(4Omega);
4. a complete mixed action derivative -> E_defect,u and its finite-H covariance bound;
5. a valid differentiated limit, with q_tu=o(H) or sufficient local uniformity -> A_u=-lim H^3 E_defect,u/(4Omega);
6. actual sphere QCD/QED moments and uniform continuum/large-radius control -> a physical value or useful bound.

Steps 1, 2 and 4 are internal algebra. Steps 3 and 5 are explicitly conditional limiting implications. Step 6 is the unevaluated physical leaf. A flat mass gap, raw positivity, a bag constant, or finite thermal Rindler data does not supply it.

## Decisive normalization/contact calculation

In the author's notation X=S_t, Y=S_tt, J=S_u, B=Y-4X and C=S_ttu-4S_tu,

    E_defect = E[B]-Var(X),
    E_defect,u = E[C]-Cov(B,J)-2Cov(X,S_tu)+kappa_3(X,X,J).

Writing F=B-(X-E[X])^2 gives exactly

    E_defect,u = E[C]-2Cov(X,S_tu)-Cov(F,J),
    |E_defect,u| <= |E[C]|+2 sigma_X sigma_Stu+sigma_F sigma_J.

This matches the sign-reversed pre-target M=-exp(t)rho_t. The volume term, S_tt contact and mixed contacts are necessary. An absolute common c-number b(u)exp(3t) changes the extracted coefficient despite leaving normalized fluctuation probabilities unchanged. A common cosmological density cancels exactly. The higher projector K and its u derivative, including the fourth cumulant, also have the stated signs and coefficients.

The author's H^(-3+delta) cancellation premise implies vanishing estimators as written. It is a sufficient conditional premise, not evidence that actual QCD satisfies it. The CS bound can discard cancellations and is not necessary for a small response. Continuum-renormalized products cannot inherit positivity merely by deleting regulator contacts or identity subtractions.

## Bai--Chen exact source and admission

Primary PDF: Yang Bai and Ting-Kuo Chen, *QCD Vacuum Energy and Its Implication for Quark Nugget Stability*, arXiv:2502.20241v2, 26 May 2026. SHA-256:
`321d0ace593afe44b9e57f2433af3a3bd09d80864f5dccc8ba79de34750cdd5a`.
Read manuscript pp. 5--6, section 2.2, equations 2.8--2.14, against the [official versioned HTML](https://arxiv.org/html/2502.20241v2). This is a zero-temperature flat-vacuum/bag estimate using a leading small-mass and one-loop simplification, not a compact sphere computation.

Let S and Q be integrated Euclidean scalar and pseudoscalar insertions with the common positive normalization. Hodge positivity gives S>=|Q|. At theta=0, E[Q]=0, so

    E[S^2]>=E[Q^2],
    Var(S)>=Var(Q)-E[S]^2.

It does not yield Var(S)>=Var(Q). The independently chosen positive parity law with probabilities (1/4,1/2,1/4), S=1 and Q=(-1,0,1) has Var(S)=0, Var(Q)=1/2 and satisfies the raw order. It can be represented algebraically by changing the selfdual/anti-selfdual components of a two-form at fixed total norm. It is a counterexample to the abstract inference from positivity and the pointwise bound, not a QCD ensemble and not a counterexample to the anomalous Ward identity.

A finite LET scalar response needs a connected/vacuum-subtracted interpretation: a literal raw zero-momentum integral also contains V times the squared nonzero scalar condensate. At nonzero momentum the disconnected part is a delta distribution, while the Fourier kernel is not a positive spacetime weight. Dropping the delta then taking momentum to zero therefore does not retain the raw positivity proof. Coincident products and renormalization contacts require a common prescription. The source may intend additional QCD structure; this audit does not infer that its numerical bound is physically false. The coordinator correctly restricts its finite counterexample to this logical admission test.

Source authentication and formula extraction pass. The direct raw-to-connected inference is refuted. The physical flat bound remains conditional on the separate connected/contact comparison leaf. A fixed flat contribution W0=E0(u)V has (d_t^2-4d_t)W0=0 and hence contributes no A or A_u; this says nothing about the curved remainder.

## Actual Rindler source and restricted implication

Primary PDF: Braguta, Goy, Dey and Roenko, arXiv:2602.20970v2, banner 14 May 2026, manuscript dated 15 May 2026. SHA-256:
`3e5730eac456b4c7264c3e19393eae1b5b32ff25330ab3e2fb37f0343aadf57a`.
Checked the supplied exact PDF sections II.2 and III.A--C, equations 24--34, with the [official versioned HTML](https://arxiv.org/html/2602.20970v2). The HTML displayed manuscript date differs from the PDF; the exact PDF hash/banner supplies the pinned version evidence here. No theorem depends on the displayed date difference.

The action is pure SU(3) at finite thermal period, real acceleration, centered open z boundaries and periodic remaining directions. Rindler is flat away from the horizon. Its Polyakov observable is an external static-quark probe. These facts exclude a direct interpretation as absolute compact-S4 vacuum stress.

At fixed bare beta, lattice spacing, domain and thermal period, its action has

    S(eta)=beta sum_z [E_z/(1+eta z)+(1+eta z)B_z],
    S_eta(0)=beta sum z(B_z-E_z),
    S_eta_eta(0)=2beta sum z^2 E_z.

The general Hessian is E[S_eta_eta]-Var(S_eta), independently of reflection symmetry, and has no implied sign. Finite compact integration gives a real analytic W locally throughout the horizon-free real interval. The improved action includes a negative rectangle coefficient, so termwise positivity of the E_z insertion cannot be assumed.

The stronger evenness assertion requires discrete reflection covariance of the **weighted loop and boundary prescription**. Equation 34 specifies clover-type averages of four plaquettes and four rectangles. With the conventional site-centered four-quadrant definition these loop sets map to their reflected sets; ReTr removes orientation inversion, and Haar measure is invariant. A single anchored plaquette would instead shift its anchor and could invalidate the simple weight transformation. The paper does not fully specify its open-boundary clover omissions, weights or implementation. Therefore actual simulation-action evenness is not certified here. **If** both clover placement and boundary treatment are reflection-covariant, the link change of variables exchanges eta with -eta, Z is even and W_eta(0)=0. The independent reflected fixture tests that explicitly paired realization only. See `SOURCE_REFLECTION_NOTE.md`.

This verifies the author's finite derivative/Hessian implication and its reflection implication **under the explicit discrete covariance hypothesis**. Its derivatives hold bare parameters fixed; a renormalized fixed-physics continuation requires the corresponding bare-coupling, matching and contact trajectory. Moreover |eta|max|z|<1 shrinks with z extent. Even when finite even analyticity holds, it alone does not exclude a limiting |acceleration| term or prove derivative/thermodynamic interchange. No curvature identification eta=H is supplied or admitted.

## Obligation matrix

| Obligation | Result |
|---|---|
| Normalized finite-measure Weyl response and mixed contacts | Passed, analytic reconstruction and separate implementation |
| Higher projector K and K_u signs/cumulants | Passed in stated finite-regulator setting |
| CS bound under real positive measure, finite moments | Passed analytically; fixture radical comparison is supplementary numerical checking |
| Author global finite coverage | Passed: 16 five-state jets, 12 common-term fixtures, finite source-action reflection checks; no QCD claim |
| Coordinator finite counterexample and coverage | Passed: 24 cases, 4,368 configurations, 4,588 recorded assertions; independently checked all stored row moments |
| Bai--Chen pointwise-to-raw inequality | Passed under common positive regulated products |
| Bai--Chen raw-to-connected/contact comparison from positivity alone | Failed; smallest counterexample above |
| Physical Bai--Chen bag bound with an additional QCD comparison theorem | Conditional, not refuted by this audit |
| Rindler contact Hessian | Passed at finite fixed-bare regulator, independently of reflection |
| Rindler exact finite reflection/zero first derivative | Conditional on reflection-covariant clover placement and boundary treatment; actual source implementation not certified |
| Flat bag/Rindler data to target compact-S4 A or A_u | Inapplicable directly; physical bridge absent |
| Renormalized fixed-physics sphere moments and uniform limits | Conditional, unmeasured physical leaf |
| Full A, R, alpha determination | Not addressed by these algebra fixtures; unset |

## Computation, provenance and residual limits

Author programs were inspected, not executed. Both existing v2 manifests validate as completed/current with the installed validator. The global author result has 221 exact checks; the coordinator result has the counts above. The global script tests a rational squared relaxation of the CS triangle bound, not an exact radical expression; the inequality itself follows analytically.

The separate `check_independent.py` constructs normalized exp/log partition functions and differentiates them directly with SymPy. It imports neither author program and does not use their jet or set-partition implementations. It checks E, E_u, K and K_u in three independent three-state nonlinear actions with nonzero mixed contacts, a different parity counterexample, all 24 stored LET moment rows using analytic product factorization, metric normalization and a distinct reflected source-action fixture. It completed **132 checks in 3.796442 seconds**. Its v2 record `run_001/manifest.json` validates against the repository; status is `completed`. Bounds were 55 seconds wall, 45 seconds per-process CPU, 65,536 combined log bytes and one conventional numerical-library thread. No RLIMIT_AS was requested on macOS. All 32 declared execution inputs and the separately checked source hashes were unchanged.

The report does not convert finite symbolic checks into a continuum theorem. The smallest physical continuation is to define one absolutely normalized sphere QCD/QED regulator, retain its full X,Y,J,S_tu,S_ttu contacts on a fixed-renormalized-physics path, and establish the limiting cancellations and derivative uniformity. For Bai--Chen source admission specifically, first obtain a derivation of its connected, renormalized, contact-compatible scalar/topological comparison. These are separate obligations.
