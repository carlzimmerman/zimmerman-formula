# Two-sided minimizing completion: local construction and null-jet obstruction

The actual positive-invariant source reconstruction admits a real, local absolute-remainder extension that retains its auxiliary minimum and limiting slope 1/2. Its leading timelike TT velocity curvature has the unfavorable sign. An odd-remainder extension reverses that restricted sign, but with the same auxiliary potential it has no stationary point at positive auxiliary modulus. More decisively, **every continuation retaining the positive source envelope fails C² regularity at arbitrarily small nonzero null metric first-jets**. This is a precise obstruction to an ordinary C² open-neighborhood Lorentzian completion of this eliminated invariant action, not a theorem excluding nonsmooth actions, all bimetric theories, or all constrained solutions.

## Declared action and inherited dictionary

Use the exchange-symmetric candidate already reconstructed in the parent covariant dictionary:

\[
 S=-K\int d^{n+1}x\{\sqrt{-g}R+\sqrt{-\hat g}\hat R
 -2[(-g)(-\hat g)]^{1/4}f(k)\chi_n a_0^2\mathcal M(z,T)\}+S_m[g]+\hat S_m[\hat g],
\]
\[
 K>0,\quad \chi_n={n-1\over2(n-2)},\quad
 z=-{\Upsilon_{\rm sym}\over2\chi_n a_0^2},\quad
 \Upsilon_{\rm sym}=\tfrac12(g^{\mu\nu}+\hat g^{\mu\nu})
 (C^\alpha{}_{\mu\lambda}C^\lambda{}_{\nu\alpha}
 -C^\alpha{}_{\mu\nu}C^\lambda{}_{\alpha\lambda}).
\]

Here n≥3, C is the difference of Levi-Civita connections, the primary R convention is opposite the conventional healthy Einstein-Hilbert convention, α=β=1, and f(k) is exchange-even with f(1)=1. T is an algebraic auxiliary modulus, not a spacetime kinetic field. This is the repaired symmetric contraction, not an assertion that a g-only contraction is exchange-symmetric. This report preserves the existing **spherical/aligned** source law. Its generic nonspherical NR equation is not QUMOND. It adds no NR-invisible curvature counterterm.

For z>0 write x=√z and define the fixed-T local source chart

\[
 b(y)=\sqrt{1+1/y}-1,\quad e(y,T)={b(y)\over1+(y/T)^2},\quad
 d=ye,\quad x=y+2d,\quad q(y,T)=2\int_0^y t e(t,T)dt,
\]
\[
 B(z,T)=q(y,T)+2d^2,\qquad
 \mathcal M_+(z,T)=-A_{\rm off}+B(z,T)-\lambda T^2/2.
\]

The inverse y(x,T) is used only where x_y>0. The source minimizing branch obeys q_T|y=λT. The inherited offset is independent of this equation. The conditional common-metric vacuum dictionary remains Λ/a₀²=χ_n A_off/2; adopting the parent UV normalization A_off=2C_resp does not select C_resp or λ. No numerical target is inserted.

## Vary the auxiliary at fixed invariant

The fixed-x chain matters. From x_T=2y e_T and q_Ty=2y e_T,

\[
 y_T|x=-{2y e_T\over x_y},\qquad
 \mathcal M_T|x=q_T|y-\lambda T,
\]
\[
 \mathcal M_{TT}|x=q_{TT}-\lambda-{(2y e_T)^2\over x_y}.
\]

The auxiliary energy has the opposite sign to M. At stationarity, direct integral differentiation gives

\[
 \lambda-q_{TT}=16T^2\int_0^y{t^3b(t)\over(T^2+t^2)^3}dt>0,
\quad
 H_T=-\mathcal M_{TT}|x=\lambda-q_{TT}+{(2y e_T)^2\over x_y}>0.
\]

This proves a strict **local** auxiliary minimum on an admitted inverse chart. It does not prove a global minimum across all T, including the separately defined boundary T=0. Near the source origin,

\[
 T_{\min}(y)=\left({8\over7\lambda}\right)^{1/4}y^{7/8}[1+O(y^{1/4})],
 \quad H_T\longrightarrow4\lambda.
\]

Taking z=0 first instead leaves the direct auxiliary energy curvature λ. The order-of-limits discrepancy and divergent mixed derivatives are real; a smooth joint Hessian at (z,T)=(0,0) has not been obtained.

## Source envelope fixes the first nonlinear term

Let a_d=√(7λ/8). The audited source IFT yields

\[
 x=2\sqrt y[1-a_dy^{1/4}+O(\sqrt y)],\qquad
 y={x^2\over4}[1+2a_d\sqrt{x/2}+O(x)].
\]

The exact envelope slope is m=M_eff,z=d/x=1/2−y/(2x), so

\[
 m(z)=\tfrac12-\tfrac18\sqrt z-{a_d\over4\sqrt2}z^{3/4}+O(z),
\]
\[
 \mathcal M_{\rm eff,+}(z)=-A_{\rm off}+{z\over2}
 -{z^{3/2}\over12}-{a_d\over7\sqrt2}z^{7/4}+O(z^2).
\]

In particular M_zz∼−1/(16√z). The coefficient −1/12 is fixed by the actual source law, independent of λ; it is not a new fit parameter. The envelope is C¹ at zero with a Hölder-1/2 slope, but not C² as a function of z.

## Two minimal real continuations

Set r=|z| and R_joint(r,T)=B(r,T)−r/2. All formulas below are local in the same x_y>0 chart.

The **absolute-remainder** extension is

\[
 \mathcal M_{\rm abs}(z,T)=-A_{\rm off}+z/2+R_{\rm joint}(|z|,T)-\lambda T^2/2.
\]

It equals the existing action for z>0. For z<0 it is −A_off+B(r,T)−r−λT²/2, and its T derivative and H_T are unchanged. Thus the same T_min(r) gives a real local minimum. Its eliminated value is −A_off+z/2+R_eff(|z|), where R_eff(r)=M_eff,+(r)+A_off−r/2. Its negative-side slope is 1−m(r)>1/2, tending to 1/2 at the origin. This realizes a source-continuous critical slope without asserting unique continuation. The direct T=0 axis still differs: B(r,0)=0 gives positive-side slope zero and negative-side slope one. Selecting the minimizing envelope does not make the original joint action C².

The **odd-remainder** extension is

\[
 \mathcal M_{\rm odd}(z,T)=-A_{\rm off}+z/2+
 \operatorname{sgn}(z)R_{\rm joint}(|z|,T)-\lambda T^2/2.
\]

For z<0 it simplifies to −A_off−B(r,T)−λT²/2, hence

\[
 \mathcal M_T=-q_T-\lambda T<0\quad(T>0).
\]

It has no positive-T stationary point in this chart. Inserting the old T_min by hand would give a favorable-looking negative-side envelope with slope m(r), but would not eliminate the displayed action. The boundary T=0 is a separate case; this argument does not exclude boundary stationarity. Reversing the auxiliary potential sign on the negative side restores the old positive root, but there M_TT=+H_T, so the auxiliary energy curvature is negative: the retained point becomes a local maximum. These are two explicit continuation tests, not an exhaustive theorem about arbitrary modifications of the joint functional.

## Restricted derivative-sign and null tests

At a coincident-position, flat coefficient jet choose mean-zero planar transverse-traceless polarization with tr(e²)=2, relative amplitude d, velocity v=∂ₜd and spatial derivative w=∂_zd. Then

\[
 \Upsilon_{\rm sym}=(v^2-w^2)/2,\quad
 z={w^2-v^2\over4\chi_n a_0^2},\quad
 L_{\rm EH,rel}=K(v^2-w^2)/4.
\]

The interaction linear term z/2 cancels this derivative quadratic action exactly. For timelike w=0 the absolute envelope leaves

\[
 L_{\rm abs,rel}=-{K|v|^3\over48\sqrt{\chi_n}a_0}+O(|v|^{7/2}),\quad
 {\partial^2L\over\partial v^2}=-{K|v|\over8\sqrt{\chi_n}a_0}+O(|v|^{3/2})<0.
\]

The prescribed odd envelope has the opposite leading sign. A scalar-type single-polarization truncation of that odd envelope is proportional to P(X)=sgn(X)|X|^{3/2}, X=(v²−w²)/2. Its P_X is positive on both sides; the timelike sound ratio P_X/(P_X+2XP_XX)=1/2 and spacelike longitudinal ratio is 2. These are **restricted coefficient/principal screens**. Finite anisotropic metric backgrounds may mix lapse, shift and other metric perturbations, and no on-shell admission/full constraint reduction is proved here. Accordingly the absolute sign is not promoted to a full physical bimetric ghost theorem, nor the odd scalar calculation to a healthy full completion or a causal cone claim.

There is nevertheless a continuation-independent off-shell regularity obstruction. At any nonzero null jet v=w>0, the map to z has nonzero derivative in w. Approach from the unchanged source side w=v+ε:

\[
 \lim_{\epsilon\downarrow0}\sqrt\epsilon\,
 \partial_w^2\left[-{z^{3/2}\over12}\right]_{w=v+\epsilon}
 =-{1\over16}\left({v\over2\chi_n a_0^2}\right)^{3/2}\ne0.
\]

The z^{7/4} correction is less singular and cannot cancel this. Thus the Hessian diverges at nonzero null jets using only z>0 data; a negative-z continuation cannot repair it. These are explicit metric first-jets, not arbitrary unconstrained connection tensors. They can be arbitrarily close to C=0. The remainder is O(||C||³) with gradient O(||C||²), so its second Fréchet derivative at C=0 exists and vanishes, but it is not C² on any open neighborhood of that point containing the null jets. The full eliminated action is C¹ across these jets. T_min∼const |z|^{7/8} is continuous and not C¹ in z; at C=0 it is O(||C||^{7/4}) with first Fréchet derivative zero, but is not twice differentiable there and has divergent transverse derivative at nonzero null jets.

## Exact remaining implication and evidence scope

An ordinary C² invariant-only eliminated completion on an open Lorentzian first-jet neighborhood is obstructed by the retained source law itself. A domain restricting the relevant jets, a nonsmooth variational/PDE construction, an uneliminated auxiliary dynamical completion, or extra operators is a changed premise requiring its own source matching and constraint audit. We have not proved that a constrained physical solution must encounter the problematic jets. The absolute extension supplies a concrete local minimum, but not a full healthy source-to-vacuum bridge; the odd extension supplies a restricted good sign but fails the actual auxiliary elimination. Neither selects the offset or λ, and none closes the original coefficient/cold-sector problem.

checks.py uses exact SymPy identities plus three 60-digit local stationary examples, each with 150 bisection steps. Preflight was 33/33 and is development evidence only. Authoritative bounded runner results and hashes are recorded separately in RUNS.md. REPORT is excluded from the execution-artifact set; the declared chart/provenance/source inputs are pinned. There is no claim of global-literature novelty or universal proof from the three examples.
