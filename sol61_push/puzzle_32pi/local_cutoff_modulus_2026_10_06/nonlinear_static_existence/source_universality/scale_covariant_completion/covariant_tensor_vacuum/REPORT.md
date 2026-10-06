# Coincident-vacuum tensor test of the symmetric auxiliary BIMOND candidate

The source-continuous **conditional** vacuum completion has a degenerate relative-TT derivative block. This is a concrete same-action health obligation, not a ghost proof and not a 32π selector. The supplied positive-invariant source reconstruction alone does not define a Lorentzian vacuum Hessian. A de Sitter curvature term survives the derivative cancellation and must not be discarded.

## Actual action and source assumption
Use the repaired symmetric candidate from covariant_vacuum_dictionary/REPORT.md, not the primary unsymmetrized contraction:

S=−K∫[√g R+√ĝ Rhat−2(gĝ)^(1/4) f(k) χ_n a0² M(z,T)] + S_m[g]+S_hat[ĝ],
K=1/(16πG_EH)>0, k=(g/ĝ)^(1/4), f(k)=f(1/k), f(1)=1,
χ_n=(n−1)/(2(n−2)), z=−Υ_sym/(2χ_n a0²), n≥3,
Υ_sym=(g^(μν)+ĝ^(μν))U_(μν)/2,
U_(μν)=C^α_(μλ)C^λ_(να)−C^α_(μν)C^λ_(αλ), C=Γ−Γhat.

Curvature R is the primary paper's opposite-sign convention (its equation8). Thus −KR equals healthy conventional EH +KR_conventional. The averaged contraction is explicitly our candidate; f even alone would not make the primary g-contraction exchange invariant. At coincident metrics both contractions agree to quadratic order because U starts at order two.

For **spherical/aligned static source gradients**, x=|∇φ*|/a0 and y=|∇ΦN|/a0, the independently varied symmetric NR action gives
x=y(1+2e), M=q(y,T)+2y²e²−λT²/2−A,
e=(√(1+1/y)−1)/(1+(y/T)²), q=2∫_0^y t e(t,T)dt.
At fixed invariant x, M_T=q_T−λT, and M_z=e/(1+2e). On the positive minimizing auxiliary branch,
T∼(8/(7λ))^(1/4)y^(7/8), y/T→0, M_z→1/2.
This is not a generic nonspherical QUMOND response: its generic equations are div[(1−2M_z)∇φ*]=ΩGnρ and Δφ=ΩGnρ+div[M_z∇φ*]. We use only the radial source-limit slope, not an equality of the full nonspherical field theories.

Coincident empty metrics with T=0 have M0=−A and conventional Λ=χ_n a0² A/2. If Λ>0 they admit a common flat-slicing de Sitter metric with H²=2Λ/[n(n−1)]. The offset fixes this background once chosen; no λ selection is supplied.

## Conditional regular extension, exact TT connection calculation
Assume an eliminated covariant interaction exists on a two-sided neighborhood of z=0 and is differentiable there:
M_eff(z)=−A+m z+o(z), with m=1/2 retained from the minimizing source branch. This is an additional hypothesis, not an established property of the parametric source action. A homogeneous time-dependent TT perturbation has Υ>0 and z<0, so the negative-z extension is essential even to this test.

Write g_ij=a²(exp γ)_ij, ĝ_ij=a²(exp hatγ)_ij, g00=ĝ00=−1, shifts zero at background; γ and hatγ are spatial TT. Let d=γ−hatγ, s=(γ+hatγ)/2. Their determinant-one parametrization makes k=1 and both volume factors exactly independent of TT. At linear order,
C^0_(ij)=a²(H d_ij+dot d_ij/2),
C^i_(0j)=dot d_ij/2,
C^i_(jk)=(∂j d_ik+∂k d_ij−∂i d_jk)/2,
C^α_(αλ)=0.

Direct contraction, using transversality (spatial equalities can be understood under integration with vanishing surface terms), gives
Υ_sym^(2)=¼ tr[dot d²−a^−2(∂d)²]+H tr(d dot d).
The H term comes from C^0_(ij), and is lost by replacing the expanding background by Minkowski connections before variation. The inverse-metric averaging and volume variations do not contribute at this order since C_background=0.

Direct ADM EH reduction gives K/4 ∫a^n tr[dotγ²−a^−2(∂γ)²] for each metric. For example, a diagonal plus wave has spatial metric diag(exp u,exp(−u),1,...), extrinsic trace square difference −n(n−1)H²+dot u²/2 and spatial curvature −(∂u)²/(2a²). Thus the EH normalization does not rely on copying a tensor formula with another Planck-mass convention.

Since 2Kχ_n a0² m z=−KmΥ, the complete quadratic TT action (up to boundaries) is

S_TT²=K∫dt d^nx a^n {
  ½ tr[dot s²−a^−2(∂s)²]
 +(1−2m)/8 tr[dot d²−a^−2(∂d)²]
 +m/2 (nH²+dot H) tr d² }.

The constant M0, f(k), and their determinant factors generate no TT potential in this parametrization. The last term is exactly the integration by parts of −Km a^n H tr(d dot d); no extra cosmological mass is inferred from a frozen spatial metric. The expression has units K×(inverse time)² per volume: Υ and H² are inverse-length-squared in c=1 units.

For common de Sitter and m=1/2 the derivative coefficient vanishes, but the last term is K nH² tr d²/4. Its unsourced linear Euler equation is K nH² d/2=0. Thus d=0 algebraically for H≠0. At flat vacuum H=0 the entire relative-TT quadratic action vanishes. The mean tensor retains ordinary healthy kinetic and gradient terms. For comparison, a constant regular slope m≠1/2 produces
(1−2m)/8 (ddot d+nH dot d+p²d)−m(nH²+dot H)d/2=0;
this comparison is not a claim that the source-minimizing candidate can choose that slope independently.

## Constraint and order-of-limits scope
On an isotropic coincident background, scalar lapse, scalar auxiliary T, and scalar/vector shifts do not carry TT representations and cannot restore this missing derivative coefficient through quadratic constraint elimination. Under simultaneous (diagonal) infinitesimal diffeomorphisms the metric difference at a coincident background is invariant; nonzero-wave-number TT is a physical tensor sector, not the lapse gauge. The algebraic de Sitter equation can constrain the relative TT rather than propagate it at this order. Whether a nonlinear completion maintains an additional constraint, has an enhanced accidental linear symmetry, or becomes strongly coupled requires its full regular action and constraint count. A zero quadratic kinetic term is not by itself a negative-energy ghost.

The auxiliary origin is singular enough that elimination and quadratic expansion cannot be interchanged without proof. At every fixed positive T, y→0 gives M_z→1/2, whereas holding T=0 first yields e=0 and M(z,0)=−A on the supplied positive-z branch: its derivative slope is zero. At y=0 the auxiliary potential curvature λ is positive, but this does not invoke an implicit-function theorem across a joint action that is not C². Source elimination has T∼x^(7/4), and supplies the critical source limit; the strict T=0 branch is not the minimizing branch at finite positive source invariant. These different limiting slopes demonstrate the absence of a unique conventional joint vacuum Hessian. They do not prove a mathematical inconsistency of every possible nonsmooth completion.

A piecewise negative-z continuation could have a different timelike slope, but it would not satisfy the regular two-sided derivative hypothesis used above. It must be varied and audited as another specified action; a positive-z source result cannot certify it. Conversely, assuming a regular invariant extension cannot silently retain the vacuum-first EH tensor block while using the source-continuous critical slope.

## Result and smallest missing arrow
The explicit symmetric action passes its static radial reconstruction conditionally, but a regular source-continuous invariant vacuum extension forces a relative-TT derivative cancellation. In de Sitter that is an algebraic relative-TT equation, not an automatic ghost or a proof of a healthy nonlinear constraint. The current joint auxiliary action lacks the regularity and negative-invariant specification needed to decide which vacuum perturbation theory actually applies.

The next required object is a fully defined Lorentzian off-shell M(z,T), with an admitted auxiliary branch and nonlinear constraint analysis, or a changed action with an independently motivated operator restoring a controlled relative-TT block. Neither choice fixes λ or the vacuum moment. No numerical target, global no-go, full solution, matter growth, or cold abundance is claimed.

## Evidence
checks.py directly constructs raw TT connection arrays in n=3,4,5 (both polarizations), checks their traces and contractions, independently computes determinant-one ADM EH coefficients, curvature variation, and both noncommuting source limits. The general-n proof is the tensor-index derivation above; a finite dimension list alone is not its proof. Controls omit the H connection, use a wrong critical slope, or transplant vacuum-first expansion into the source-continuous conditional claim. These are deliberately inconsistent interpretations, not alternate physical actions ruled out by a check count. Sources and exact input hashes are pinned separately; REPORT is excluded from execution inputs so narrative run summaries do not stale computations.

Fresh main_a passed32/32 exact checks. control_H_a failed the three raw dimension contractions; control_slope_a and control_vacuum_a each failed the claimed source-continuous derivative cancellation. All four manifests independently validate against current input bytes. These expected failures are not stale historical runs. Commands, effective caps, exact software/input/output hashes and logs reside in runs/*/manifest.json; RUNS.json reconciles the finite assertions. No memory cap was applied.
