# Full J1 covariant vector construction and determinant

This follow-up supersedes the *open full-vector task*, not the frozen parent angular report. The exact ghost determinant, its action and all parent files remain unchanged. The coordinator suggested the Cartesian equivariant tensor basis and the quaternion-intertwiner route. The Cartesian Hessian projection, Gram, wall matrices, ten-channel mixed determinant and exact asymptotic wall algebra were calculated here. The coordinator and fresh reviewers separately supplied/check the translation and symplectic rank arguments; their eventual receipts are separate evidence.

Use p=e_z, n=x/r, K=t/sinh t, h=coth t-1/t, D_i=partial_i+A_i cross, A_i=(1-K)(e_i cross n)/t, D4=ad(hn). The reduced vector amplitude is a_mu=u_mu/t. Each of the following seven tensors occupies spatial rows i and adjoint columns a:

B0=delta_ia(n·p), B1=n_i p_a, B2=p_i n_a, B3=n_i n_a(n·p), B4=epsilon_iab p_b, B5=n_i(n cross p)_a, B6=(n cross p)_i n_a.

B7,B8,B9 occupy A4 only and equal p_a,n_a(n·p),(n cross p)_a. They span all10 total-J1 radial amplitudes per magnetic quantum number; the remaining apparent epsilon tensor is dependent. Angular integration is normalized by4pi.

The exact constant Gram G_ab=integral B_a·B_b has blocks (indices0..3),(4..6),(7..8),(9):

G_0..3=[[1,1/3,1/3,1/3],[1/3,1,1/3,1/3],[1/3,1/3,1,1/3],[1/3,1/3,1/3,1/3]],
G_4..6=[[2,-2/3,2/3],[-2/3,2/3,0],[2/3,0,2/3]],
G_7..8=[[1,1/3],[1/3,1/3]], G_99=2/3.

Starting from the actual F=partial A-partial A+A cross A and H_mu_nu=-D_lambdaD_lambda delta_mu_nu-2adF_mu_nu, applying H to each B_b/t gives V_ab(t) B_a/t. There are no first radial derivatives after the unitary reduced change because Ar=0. The complete exact matrix, with independent symbols K,h,Kprime,hprime, is in runs/derive-001/operator.json, field V_raw. All ten Cartesian remainders vanish on n·n=1, and G V=V^T G exactly. This specifies the full covariant vector operator without guessing scalar copies.

The exact profile is anti-self-dual in epsilon1234=+1 conventions: Fij=-epsilonijk Fk4. This only fixes which quaternion chirality commutes with it; it changes no spectrum. A constant G-orthonormal S, supplied explicitly in operator.json, puts Vc=S^T G V S in a Euclidean reduced norm. Its origin centrifugal eigenvalues are l(l+1) with l=[0,0,1,1,1,1,2,2,2,3]. Smooth Cartesian origin data give columns t^(l+1)e_l and their regular Frobenius expansions. The l0 constant reduced irregular branches are excluded even though square-integrable. The Gram change is constant and identical in the reference, so no background-dependent field measure is removed.

The raw wall matrices are simple. T selects rows0,2,4,6,7,8,9. N gives normal adjoint coefficients in the independent p,n(n·p),n cross p basis:

N u=(u1,u0+u2+u3,-u4+u5).

The actual operator-domain wall data are T u=0 and N(uprime+u/x)=0. They fix the tangential connection and A4 and set background divergence zero. These are7D+3R, not all Dirichlet. If Z embeds three normal coefficients into raw rows1,3,5, PN=ZN is the Gram-orthogonal rank3 normal projection; PD=I-PN. The exact V splits into two invariant5blocks: A=(0,1,2,3,9) with3D+2R and B=(4,5,6,7,8) with4D+1R.

Let Y be the canonical regular zero-energy fundamental matrix with the origin normalization above. The actual boundary determinant is

F(x)=det([T S Y(x); N S(Yprime(x)+Y(x)/x)]).

For the unbroken K=1,h=0 reference, Yref=diag(x^(l+1)) and
Fref=(5103/8)x20.
The power is sum(l+1)-3=23-3. Thus Dvec=F/Fref fixes the common normalization and mixed domain. The regular-interval matrix determinant theorem is used at positive origin cutoff. Common centrifugal cutoff normalizations have determinant epsilon^-13/(3^4 5^3 7); this cancels between background and reference before epsilon tends to zero. This is an explicit singular-origin extension, not an unqualified invocation of a regular theorem at zero.

## Orthogonal full-bulk check

Define self-dual constant complex structures (J_a)_ij=epsilon_ija,(J_a)_i4=delta_ia,(J_a)_4i=-delta_ai. They commute with the anti-self-dual curvature. T0=D and Ta=J_a D satisfy H T=T M, and P^dagger Ta=0 for a=1,2,3. To project to total vectorJ1, use:

- longitudinal: T0 on the three ghostJ1 harmonics;
- transverse ghostJ0: J_p D on c=n f;
- transverse ghostJ1: sum_ab epsilon_abp J_a D on the three ghost harmonics polarized by e_b;
- transverse ghostJ2: sum_a J_a D on Y_a=n_a(n·p)-p_a/3 and its radial/electric/magnetic adjoint harmonics.

The last three ghost sectors contain1+3+3 radial channels. Writing the full10-column map as A*d/dt+B(t), the code independently constructs A,B from first covariant derivatives, without using the Hessian projection. It verifies the two complete matrix coefficient identities
V A-2Bprime=A Ug,
V B-Bsecond=A Ugprime+B Ug,
where Ug=diag(ghostJ1,ghostJ0,ghostJ1,ghostJ2). Its constant principal matrix A has determinant1/6 and generic A+B has rank10. This validates all ten bulk channels by an orthogonal first-order construction. It is not a finite-wall scalar cancellation: the actual mixed boundary determinant F is integrated directly.

## Translation and finite-wall nonzero spectrum

For fixed p, put b=hprime,c=Kh/t. The exact translation variation has
phi=c p+(b-c)n(n·p),
a_i=c(e_i cross p)-(b-c)(n cross p)_i n.
Its reduced raw coordinates are
u4=-Kh,u6=-t hprime+Kh,u7=Kh,u8=t hprime-Kh,
all others zero. Direct substitution in the actual10x10 Hessian gives H u=0, and the independently constructed P^dagger gives G=0. Its normal wall trace is N u=(0,0,Kh), so its Robin defect is exponential. Its tangential/A4 Dirichlet defects include plus/minus(t hprime-Kh), with an algebraic1/x tail. It is not an exact finite-wall zero mode and is retained in every unprimed determinant.

There is a direct finite-wall kernel argument. The BPS action with fixed tangential connection and fixed phi has nonnegative quadratic form equal to the squared linearized Bogomolny equations plus background-gauge square. A zero eigenfunction therefore solves the first-order linearized Bogomolny system and G=0. At the wall its only free trace is a_r. Solve M c=0 inward with c(x)=0,cprime(x)=a_r(x). Then P c solves the same first-order system and has identical full vector wall values. First-order radial uniqueness makes a=P c for t>0. Smooth a forces c smooth at the origin (D_i c=a_i cannot support a singular or direction-dependent constant branch). Dirichlet ghost positivity then gives c=0 and a=0. Thus no exact vector zero is removed; the finite positive lifted translation remains present.

## Far-field algebra and the remaining global premise

The full operator gives exactly, after dropping exponential profile terms,
Vc_infty=M0-2M0/t+M2/t²,
[M0,M2]=[M0,PN]=0.
Neutral mass0 centrifugal values are0,2,2,6. Charged mass1 values are0,0,2,2,6,6. Each5block has charged C=0,2,6. BlockA has neutral C=0,6; blockB has neutral C=2,2. The charge/neutral split respects the wall projections.

Charged growing zero-energy functions have
u_C=e^t/t[1+a1/t+a2/t²+...],
a1=(2-C)/2, a2=(6-C)a1/4.
Since the normal functional is uprime+u/t, its coefficient through1/t is the same as for Dirichlet value. The sum over six charged a1 is-2.

The translation neutral tail is vminus/t, vminus=-B6+B8. The orthogonal neutral C2 growing direction is vplus*t², vplus=(B6+2B8)/sqrt2. The neutral C0,C6 directions are v0=B2 and v6=(3B3-B2)/sqrt2, both normalized in G. The exact neutral-regular ghostJ1 mode can be chosen with no charged growth: its neutral c=nY[t+A/t²] plus exponential terms, and its covariant gradient has reduced vector g0=v0*t-sqrt2*A*v6/t² plus exponential terms. Existence follows by cancelling the single charged growth of the two regular RE solutions; if the remaining neutral growing coefficient vanished, one would obtain an impossible L² zero of the positive ghost operator.

For a regular neutral blockA companion h with C6 growth, the conserved Wronskian with g0 fixes the C0 constant coefficient. After eliminating C0 growth, g0=v0*t+gamma*v6/t² and h=v6*t³+5gamma*v0+delta*v6/t². Hence neutral scattering affects the boundary determinant first at relative order t^-3. The same is true in blockB: its growing direction is vplus*t² plus an O(t^-1) admixture, while translation supplies vminus/t.

These choices require the regular vector space to have precisely one non-growing direction per magnetic quantum number, supplied by translation. The coordinator's symplectic argument is: regular-origin L and non-growing infinity S are10-dimensional Lagrangian subspaces of the20-dimensional conserved-Wronskian phase space. W(g0,s)=0 eliminates the only non-L² non-growing branch, neutral C0 constant, so L intersection S is exactly the L² kernel. If the primary charge-one BPS kernel count gives only translations inJ1, its dimension is1 per magnetic number. Thus the growing projection of L has rank9. Its unique cokernel is paired with translation, whose neutral C2-decay coefficient is nonzero; consequently charged growth has full rank6 and the residual neutral growth has rank3. The primary kernel/domain application has now been audited separately in ../../reviews/kernel_rank/RAW_DERIVATION_v1.md using the exact primary versions in its SOURCES_v1.md. It is not established by finite numerical agreement or by the local algebra run. REMAINDER_CONTROL.md closes the exact outer-mode and mixed-wall remainder qualification.

With that source-audited global premise and the exterior Schur proof in REMAINDER_CONTROL.md, the exact mixed-boundary algebra gives F~C e^(6x)x^-2[1-2/x+O(x^-2)], and
logDvec=6x-22logx+Cvec-2/x+O(x^-2),
logZ_J1=-3x+15logx+Cz+3/x+O(x^-2).
The finite symbolic boundary check finds one neutral derivative factor1/x in blockA and none inblockB; each normalized5block boundary polynomial begins1-1/x+1/(2x²). The polynomial recorded by the script is exact only for its charged trial functions truncated through1/x². Its displayed cubic and quartic coefficients are not full asymptotic coefficients: the chargedC0 growing solution has a nonterminating inverse-power series. Thus even the1/x² logarithmic term cancels if all stated neutral/global hypotheses hold. No inverse coefficient was fitted from the finite-radius values.
