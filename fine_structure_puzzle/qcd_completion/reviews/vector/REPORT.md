# Independent review of the full static J=1 vector calculation

Normalized claim: for the exact static SU(2) BPS fields and the auxiliary K=1,h=0 reference on the same ball, the ten-channel Cartesian gauge-fixed Hessian with smooth origin and relative 7D+3R wall gives the recorded determinant ratios at x=2,4,6,8,10; the complex ghost combines with magnetic multiplicity three. No large-radius or QCD claim is part of this review.

**Primary verdict: computationally verified only in the stated range.** The structural checks below pass exactly. The floating determinant values pass their declared finite stability criteria, but have no certified error bound. I audited the target numerical implementation and records; I did not repeat its ODE integration. My independent exact algebraic benchmark run completed and its v2 manifest validates. No structural error was found in the audited operator, origin data, wall, reference normalization, or ghost multiplicity.

This review covers the current code/runs only. No transverse_followup/REPORT.md existed when the review was requested; the coordinator explicitly authorized review of these exact artifacts while a separate asymptotic follow-up was being developed. Any later report or run needs an addendum.

## Exact revision and independence

The independent raw derivation was saved before opening the target vector code or outputs:
INDEPENDENT_RAW_DERIVATION.md, SHA256 68bc54fda84b72ab6ea8d4bb5a5e58bf75ddf822c1acfa305e0cc46dafe3d84a.

Audited target bytes:

| Artifact | SHA256 |
|---|---|
| derive_vector_v1.py | e1e9466b7a6338d181c1d091315d472eda791d2468795942beebe3f6db531439 |
| check_full_v1.py | 99fe9e9e7b1d48e0ebdd4bbb34f9a0eff963654440a7c2346a395a864c546093 |
| runs/derive-001/operator.json | 4e98fa28d208693d6559c8bf5b2dd4b1c05e4d5b88827c38fb21230ac645f6bd |
| runs/full-001/result.json | 055f120a5b9c38a36f66f01a145b1e8cad11908f424288a940b2b0d3ace3dd31 |

Repository commit recorded by all reviewed manifests is 9516ee01c79f35c04b7556050669ba77b0c98b99, with dirty=true. Target derive-001 and full-001 manifests both validated against current inputs and outputs. The immutable target files were preserved.

Independence is limited and explicit: the tensor basis, Gram, orbital multiplicities, wall form, translation, and manual gauge-gradient were derived before reading the targets. The audit then applies those benchmarks to the serialized target V and S. It does not independently reconstruct every Cartesian Hessian matrix entry or repeat the target floating ODE solve. This is a fresh orthogonal audit, not an author self-review.

## Dependency graph

1. Specified A,Phi and D convention -> actual F and BPS/YM equations. Internal exact calculation.
2. Cartesian H=-D² delta-2adF plus equivariant basis -> ten-channel V and constant G. Target exact Cartesian projection, independently checked by angular data, translation and gauge intertwiners.
3. Smooth analytic Cartesian background -> regular exponents and compatible Frobenius series. Representation/Taylor-degree argument and target exact resonance checks.
4. Relative wall -> seven Dirichlet rows plus three normal Robin rows. Independent trace derivation and exact matrix checks.
5. Common regular normalization and common mixed wall -> determinant boundary quotient to the free reference. Matched singular data and boundary matrices checked here; the general singular-endpoint determinant argument is inherited from the frozen parent report, rather than independently literature-audited in this review.
6. Finite numerical integration -> stored boundary determinant ratios and stability diagnostics. Target code/records audited; no independent integration or interval certification here.
7. Dirichlet ghost gradient pairing -> det transverse=det vector/det ghost; complex ghost and m multiplicity -> logZ_J1=3(logDghost-0.5logDvector). Exact pairing and stored arithmetic checked here.
8. Any inverse-radius coefficient -> uniform large-x control beyond these five data. Not addressed by the audited run.

## Obligation matrix

| Obligation | Status | Evidence / limit |
|---|---|---|
| Exact J1 spatial/temporal channel count | passed | Seven spatial plus three A4; independent orbital L multiplicities (2,4,3,1) |
| Angular Gram and positivity | passed | Independent Gram transformed exactly to target, G-orthonormal S and G V symmetry |
| Correct BPS curvature sign | passed | Given D convention gives B=-DPhi; matches target anti-self-duality |
| Cartesian H rather than scalar proxy | passed | Target computes original covariant H, exact closure all ten columns; independent translation and gauge checks |
| Smooth origin branches | passed | Reduced leading powers (1,1,2,2,2,2,3,3,3,4), correct orbital basis |
| Resonant origin recurrence | passed | Target checks zero resonance sources before assigning free admixtures zero; analytic Cartesian degree filtration explains compatibility |
| Sufficient stated Frobenius order | passed | Five corrections require potential terms through t8, all present; t10 additionally used for near-origin potential |
| Relative wall | passed | Tangential/A4 Dirichlet and normal u'+u/x, rank 7+3 |
| Free reference | passed | Exact independent evaluation 5103/8 times x20 |
| Gauge/ghost wall pairing | passed | Manual P has T A=0 and N(B+A/t)=0; H P=P M checked exactly |
| Finite normalization and restored column factors | passed | slogdet column normalization is reversed by sum log column norms |
| Quasi-zero retention | passed | No priming, eigenvalue deletion, or SVD truncation; SVD diagnostic only |
| Complex ghost / m multiplicity | passed | logZ_J1=3(logDghost-0.5logDvector), transverse log=logDvector-logDghost |
| Finite stability at five radii | passed as declared | Two floating settings agree; target run not independently repeated |
| Certified determinant error | conditional | No interval/validated propagation or uniform roundoff analysis |
| Large-radius inverse-power coefficient | not addressed | No inference from the five points is justified |
| Physical subtraction/QCD/charge normalization/alpha | out of scope | Auxiliary reference has different holonomy |

## Decisive independent checks

Let b=h'=(1-K²)/t² and c=Kh/t. For the declared signs,
F_i4=c e_i+(b-c)n_i n and F_ij=-epsilon_ijk F_k4.
The exact covariant translation in direction p is

a_i=c(e_i cross p)-(b-c)n(n cross p)_i,
a4=c p+(b-c)(n.p)n.

The target basis uses spatial rows and color columns. Its fifth tensor is minus the independent epsilon tensor; its sixth is T5-T6+T7 in the independent basis. After that basis conversion, the reduced translation coefficients are

u=(0,0,0,0,-Kh,0,Kh+(K²-1)/t,Kh,(1-K²)/t-Kh,0).

Substitution into the serialized operator gives -u''+V u=0 in every component as exact rational functions of t and z=exp(t). The independently derived adjoint gauge-gradient also gives Pdag u=0 exactly. This checks both the spin-curvature coupling and A4 coupling with a known nontrivial smooth solution.

The translation is not a zero mode of the finite-ball mixed domain: a4 and the spatial tangent trace are nonzero for every finite t>0. At large t, their neutral parts fall as t^-2. The finite determinant must retain any lifted positive small mode. The target does so: its log determinant uses the full boundary matrix; no singular values or eigenvalues are removed. The reported minimum boundary singular value is a conditioning diagnostic, not a measured fluctuation eigenvalue.

For an independent gauge check, write cghost=(f p+g(n.p)n+j(n cross p)), and U=t(f,g,j). Direct Cartesian differentiation gives vector reduced amplitudes A U'+B U, with derivative rows A_(1,f)=A_(3,g)=A_(5,j)=1 (zero-based target indices). The complete A,B are saved in runs/check-001/result.json. Both exact coefficient identities in H P=P M vanish, covering 60 scalar residuals. At a Dirichlet ghost wall, U=0 and its eigenvalue equation gives U''=0 there. The independently verified identities T A=0 and N(B+A/t)=0 then prove the mixed vector wall traces vanish. This tests the domain as well as the bulk intertwiner.

The free regular origin column with orbital l is x^(l+1)S_l. Seven wall rows evaluate the columns themselves; three evaluate derivatives plus 1/x. Hence the power is sum(l+1)-3=23-3=20. The exact remaining coefficient is

det stack(T S, N S diag(l+2))=5103/8.

Thus the target's hardcoded free divisor is correct for the stored S and row ordering.

## Finite numerical evidence and its limits

The audited full-001 run uses DOP853 on [epsilon,10] with two coupled changes:
(epsilon,rtol,atol,max_step)=(0.001,2e-10,2e-12,0.07) and
(0.002,3e-12,3e-14,0.035).
It evaluates only x=2,4,6,8,10. The tighter stored results are:

| x | log Dvector per m | log Z_J1 |
|---|---:|---:|
| 2 | -1.718410537625365 | 1.944832705758314 |
| 4 | -2.444136501726923 | 4.495056667290045 |
| 6 | 0.627493967761502 | 4.689116015797106 |
| 8 | 6.320815215355140 | 2.974539942495935 |
| 10 | 13.453003315007479 | 0.259786178296929 |

All five pass the declared 2e-5 log-stability and condition-times-machine-epsilon thresholds, with positive boundary determinant signs in both runs. The inter-run determinant changes are approximately 3.9845e-8 at all five radii. This near-constant difference is consistent with a common fundamental-solution normalization drift; it is not evidence of a uniform true-error bound. The two runs change cutoff and tolerance simultaneously, so they do not isolate either source of error.

The reported condition-number diagnostic concerns the final column-normalized boundary matrix. It does not by itself bound accumulated integration errors, cancellation in the profile/potential evaluation, singular-start truncation, or all intermediate conditioning. These limitations already appear in the target contract/non-claims; the numerical precision should not be promoted beyond that scope.

No fit or inverse-radius coefficient was computed in the reviewed target. Five finite points, even with the observed floating stability, do not control the large-x remainder. The next discriminating step is an exact large-x solution/boundary analysis or a separately bounded method reaching that regime with a controlled remainder. Repeating similar five-point fits would not close this gap.

## Computation records and commands

My contract was saved before execution at COMPUTATION_CONTRACT_v1.json. Its check_independent_v1.py reads only the immutable target operator and finite result; it never imports the target implementation. The bounded command is recorded verbatim in runs/check-001/manifest.json. Run status is completed, child runtime 4.13 seconds; all sixteen named checks passed. Its manifest validated with the installed computation-audit validator and the repository root.

The two target manifests were validated with the same validator and current repository root. They report completed, unchanged before/after input hashes, present result files, and zero exit. This supports freshness and provenance, not a mathematical error certificate.

No external theorem or source was newly fetched in this focused audit. The parent's singular-endpoint determinant justification is a declared inherited leaf. No physical QCD, charge-normalization, or alpha conclusion follows from this review.

