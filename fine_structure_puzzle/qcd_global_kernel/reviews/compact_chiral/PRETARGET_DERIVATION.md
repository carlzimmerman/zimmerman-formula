# Independent compact SU(2) source-first derivation

2026-10-19; isolated reviewer `global_sphere_review`, new task. Saved before opening any `chiral_zero_mode/` target file. The completed `reviews/global_sphere/` files are read-only throughout this continuation. This is a compact leading-order collective-sector calculation, not a full-QCD sphere stress or a determination of alpha.

## Given action, trace, and local volume term

Write `U=a0 I+i a_j tau_j`, `a0^2+a1^2+a2^2+a3^2=1`, and normalize Haar measure to total mass one on S3. With the dimensionless two-flavor charge matrix `Q=I/6+tau3/2=diag(2/3,-1/3)`, let `s=a1^2+a2^2`. Pauli multiplication gives

`Tr(QUQUdagger)=2(1/6)^2+2(1/2)^2 R33=5/9-s`,

where `R33=1-2s`. In particular `Tr Q^2=5/9`; the trace is not simply `1-s`.

The LO Euclidean constant-mode mass action is `-F^2 M^2 V a0`. Urech's Minkowski LO term is `+C Tr(Q_phys U Q_phys Udagger)` with `Q_phys=eQ`; Euclidean weighting therefore gives `exp[y Tr(QUQUdagger)]` for `y=uCV`, `u=e^2`. The constant-mode partition is consequently

`Z_raw=N(V,F,...) exp(5y/9) Z(x,y)`,

`Z(x,y)=< exp(x a0-y s) >_Haar`, `x=F^2M^2V`.

The exposed U-independent term is `W_local=-5uCV/9`, which contributes `rho_local=-5uC/9` under the stipulated stress convention. Its value is part of the local vacuum matching convention; it cannot be hidden in the normalized Haar integral. In an SU(3)-embedded convention the numerical U-independent constant can differ, while the two-flavor orientation factor `exp(-ys)` is unchanged. Additional local electromagnetic vacuum terms remain independent inputs.

## Exact compact integral and axes

Use Hopf coordinates

`a1=sqrt(s) cos(theta)`, `a2=sqrt(s) sin(theta)`,

`a0=sqrt(1-s) cos(phi)`, `a3=sqrt(1-s) sin(phi)`.

The normalized Haar measure is `ds dtheta dphi/(4pi^2)` for `0<=s<=1`, both angles in `[0,2pi)`. Thus s is uniform before tilting, and integrating both angles proves the proposed reduction exactly:

`Z(x,y)=integral_0^1 ds exp(-ys) I0(x sqrt(1-s))`.

There is no missing factor two or endpoint Jacobian. `Z(0,0)=1`. The compact integral is entire in complex x,y; for real x,y it is strictly positive. It is even in x. For real nonnegative x,y no branch choice of W is needed.

The axes are

`Z(x,0)=2 I1(x)/x`, with its removable x=0 value one,

`Z(0,y)=(1-exp(-y))/y`, with its removable y=0 value one.

An absolutely convergent expansion useful for independent checks is

`Z(x,y)=sum_(n,k>=0) [(x^2/4)^n (-y)^k]/[n! (n+k+1)!]`.

This follows by expanding I0 and the exponential and evaluating the beta integral `integral s^k(1-s)^n ds=k! n!/(n+k+1)!`. It is a mathematical identity, not a claim that a low-order Taylor truncation controls all x,y.

The first log coefficients are

`log Z=x^2/8-y/2+y^2/24+x^2 y/48+O(x^4,y^3,x^2y^2)`.

The displayed mixed sign follows from `<a0^2 s>_Haar=1/12`, `<a0^2>=1/4`, and `<s>=1/2`.

## Fixed-parameter metric and charge derivatives

For this normalized mathematical integral set `W=-log Z`, `A=F^2M^2`, `B=uC`, `x=AV`, `y=BV`, and `V=8pi^2/(3H^4)`. At fixed A,B,

`H partial_H=-4D`, `D=x partial_x+y partial_y`,

`rho_Haar=D W/V=-A<a0>+B<s>`.

Expectations use the tilted normalized Haar weight. In particular

`W_x=-<a0>`, `W_y=<s>`,

`W_xx=-Var(a0)`, `W_yy=-Var(s)`, `W_xy=Cov(a0,s)`.

The fixed-input charge derivative is

`partial_u W=CV<s>`,

`partial_u rho_Haar=C[<s>+x Cov(a0,s)-y Var(s)]`.

The covariance terms are required: differentiating only the explicit `uC` in rho is incorrect. `partial_alpha=4pi partial_u` only for the declared source parameter `u=4pi alpha`.

At y=0 let `r(x)=I2(x)/I1(x)=partial_x log[2I1(x)/x]`. Rotational symmetry among a1,a2,a3 and integration by parts give

`<a0>=r`, `<s>=2r/x`, `r'=Var(a0)=1-r^2-3r/x`.

Hence

`rho_Haar(x,0)=-A r(x)`,

`partial_u rho_Haar|_(u=0)=2C r'(x)=2C Var(a0)`.

The x=0 limits are regular: `r~x/4`, `partial_u rho|0=C/2`. This positivity statement is for C>0 and the local-volume term removed; restoring `-5uC/9` shifts the charge slope by `-5C/9`.

At x=0 and real y,

`<s>=1/y-1/(exp(y)-1)`,

`rho_Haar=(1/V)[1-y/(exp(y)-1)]`,

`partial_u rho_Haar=C[((y-1)exp(y)+1)/(exp(y)-1)^2]`.

All apparent y=0 singularities are removable; use their series rather than subtracting rounded exponentials.

## Normalization-independent differences and absolute-stress hazard

The full functional measure has collective-coordinate Jacobians and a nonzero-mode functional factor. Writing `Z_full=N(V,F,...) exp(5y/9) Z(x,y)` does not prove that N is H-independent. A normalized Haar convention alone does not determine the absolute stress of a collective sector. In particular a raw `log V` from a saddle is not automatically a physical curvature response.

After specifying/removing the displayed local volume term, the coupling difference

`Delta W(x,y)=-log[Z(x,y)/Z(x,0)]`

cancels any common **u-independent** collective normalization. Its direct radius response is

`Delta rho=[D W(x,y)-x W_x(x,0)]/V`.

These are the preferable restricted observables. A coupling-dependent omitted nonzero-mode factor does not cancel and has not been computed. Neither does an independently matched local `u C_vac V` term cancel; its convention must remain explicit. An H-independent normalization f(u) changes raw Delta W by a constant in radius but leaves its metric derivative unchanged.

The compact integral replaces the treatment of the constant pion mode. The massive scalar determinant already includes that mode. Adding the compact partition to the full determinant counts it twice. A consistent matched construction must remove the Gaussian constant-mode factor before inserting the compact integral and track the collective/nonzero-mode measure and local vacuum convention together.

## Asymptotics, order of limits, and regime restrictions

For x large and `t=y/x` in a compact subset of `t>-1/2`, the saddle at U=I gives

`Z(x,y)~sqrt(2/pi) exp(x)/[x^(3/2)(1+2t)]`.

In particular `Delta W~log(1+2y/x)+O(1/x)`. At fixed positive A and fixed B, y/x=B/A is constant under volume variation, so this leading coupling difference has zero radius derivative. The normalized Haar raw stress has `-A+3/(2V)+O(V^-2)`; the `3/(2V)` coefficient depends on treating this normalized collective factor as a separate absolute partition and needs the preceding measure caveat.

At y=0, `r=1-3/(2x)+3/(8x^2)+O(x^-3)`, so

`partial_u rho_Haar|0=3C/x^2+O(x^-3)`.

For x=0 and y positive large, `Z~1/y`, `rho_Haar~1/V`, and `partial_u rho_Haar` tends exponentially to zero. Yet taking the charge derivative at u=0 first gives C/2 for every V. Thus in this massless mathematical model

`lim_(V->infinity) partial_u rho_Haar|0=C/2`

differs from the derivative of its pointwise large-volume limit at fixed u>=0. This is a charge boundary layer `uCV=O(1)`, not a full-QCD noncommutation theorem. For M>0 the fixed-mass saddle instead gives a vanishing derivative. The limits M->0, u->0, V->infinity are not interchangeable without specifying the scaling.

For completeness, a mathematical continuation to negative y has an alignment threshold in a fixed-ratio large-x limit: maximizing `x a0-y s` moves away from U=I when `y/x<-1/2`. Finite-volume Z remains analytic. No such threshold occurs for physical u>=0 and C>0, and this continuation is not evidence for a physical charge phase transition.

The controlled epsilon regime requires the sphere size L~1/H to obey FL>>1, while `M L<<1`, and analogously `Delta M_EM^2 L^2<<1`; zero-mode variables x,y are O(1). With `Delta M_EM^2=2uC/F^2`, these conditions agree with x,y O(1) and large FL. A formal H->0 sequence remaining in this regime scales `M^2~H^4/F^2` and `uC~H^4`; it holds neither the physical mass nor the physical charge fixed. Fixed nonzero mass/charge volume extrapolations leave this regime and require the nonzero modes and a matched p-regime treatment. Curved-background higher-order chiral operators and nonpionic QCD remain omitted.

The SU(2) group integral corresponds to a declared theta=0 flavor-group treatment. Fixed topological charge generally requires a different U(2) integral/determinant weight; it cannot be inferred from the same formula without a topology prescription.

## Primary-source authentication before target comparison

* R. Urech, *Virtual Photons in Chiral Perturbation Theory*, arXiv:hep-ph/9405341v2, 1994-06-27. Existing primary PDF `/tmp/fsp008_urech_9405341v2.pdf` SHA256 `ca10bd1ed23918ac43e250f83490ba75eb31d16ae417325ae86decef7cfc2085`; matching alternate cached copy verified. Cover/banner checked; official versioned PDF text inspected. Equations (1),(5),(8), printed p.2, verify the LO C operator, charge includes e in that source, and the charged mass shift `2e^2 C/F^2`. The two-flavor trace/Hopf reduction above is derived here rather than quoted from its SU(3) treatment.
* E. V. Shuryak and J. J. M. Verbaarschot, *Random matrix theory and spectral sum rules for the Dirac operator in QCD*, arXiv:hep-th/9212088v1, 1992-12-14, official arXiv PDF inspected. Its (3.10), printed p.8, states a **mass-dependent partition ratio** as an SU(Nf) integral; (4.2),(4.3), printed p.9, give the two-flavor Haar/Bessel result. This is a primary derivation within that paper's random-matrix model, matched there to the finite-volume chiral result; it does not independently establish absolute full-QCD metric normalization. Our x corresponds to `2m Sigma V` using `F^2 M^2=2m Sigma` for degenerate two-flavor LO masses.
* J. Gasser and H. Leutwyler, *Thermodynamics of chiral symmetry*, Phys. Lett. B188 (1987) 477-481, DOI `10.1016/0370-2693(87)91652-2`. Publisher metadata/abstract authenticate that the long-correlation-length finite-volume partition reduces to a flavor-group integral. Exact original full-text equations were not yet acquired, so this item is metadata/context support only, not an authenticated equation dependency.

The exact Haar/action calculation above is independent of the pending author package. No inference of full QCD or absolute gravitational normalization is supported by a finite-dimensional partition ratio alone.
