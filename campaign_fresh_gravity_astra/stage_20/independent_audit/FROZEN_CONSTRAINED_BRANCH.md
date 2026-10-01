# Independent FGF034 fixed-wall, fixed-mass branch derivation

Auditor /root/metric_intake. Derived from task034 and pinned023/033 action and quadratic form before reading any new worker or root proof. No formula preview was received. Fix one interval [0,D], endpoint values of phi and chi, total mass M>0 and physical C=4piG,cs²,J and other inherited coefficients. At the base lambda0 assume a smooth regular Q equilibrium with rho>0, phi'>0 uniformly on the closed interval and the inherited full form Q0 coercive on H1_0 triples after fixed positive component reference scalings. V is not chosen and its global equilibrium is not assumed for the local branch.

## Density elimination and actual nonlinear map

Hydrostatic cs² rho'=-rho phi' gives the exact fixed-mass density

 rho(phi)=M exp(-phi/cs²)/Z(phi), Z=integral exp(-phi/cs²).

The normalization is essential. Its derivative in direction psi is

 r[psi]=-(rho/cs²)(psi-mean_rho psi), mean_rho psi=(integral rho psi)/M.

Thus integral r=0; freezing the normalization would violate mass preservation. Use affine base fields plus corrections in X=(H²(0,D) intersect H1_0(0,D))², and Y=L²(0,D)². On a small X-open neighborhood phi'>g_min/2>0 by the one-dimensional embedding H² into C1, and chi remains bounded. Then a=a_c exp(chi+lambda)>0, b_Q(g,a)=(sqrt(a²+4g²)-a)/2 and all constitutive derivatives are smooth on a compact positive set. Composition/multiplication in these one-dimensional Sobolev spaces, together with positive Z, give a continuously Frechet differentiable map

 F(phi,chi,lambda)=( -partial_x b(phi',a)+C rho(phi),
                    -J chi''+U'(chi)-T(phi',a)) in Y.

This is the actual nonlinear equilibrium map; no formal H1 energy differentiability alone is invoked. Its zero enforces MOND B'=C rho, both fixed field traces, hydrostatic balance and fixed total mass. Incoming flux is allowed to adjust and is not separately fixed.

## Reduced elliptic derivative and coercivity gate

At the base let A=b_g>0, q=T_g, s=T_chi=2T-gq, m=U''-s. The field derivative is

 DF(psi,eta)=( -(A psi'-q eta)' +C r[psi],
              -J eta''-q psi'+m eta).

Its weak symmetric form divided by C is

 a_red[(psi,eta)]=integral(A psi'²-2q eta psi'+J eta'²+m eta²)/C
                   -integral rho(psi-mean_rho psi)²/cs².

This is exactly the Schur minimization of the full Q0 over mass-preserving fluid density r. The fluid expression cs² r²/rho+2r psi, constrained by integral r=0, minimizes at r=r[psi]. The density/displacement map is a bounded isomorphism H1_0 -> L²_zero via r=-(rho xi)' and

 xi(x)=-[integral_0^x r(y)dy]/rho(x).

Both endpoint traces vanish precisely when integral r=0. Smooth positive rho and bounded rho' make this map and its inverse bounded. Consequently the exact fluid minimizer xi_psi is admissible, and a_red=Q0(xi_psi,psi,eta) inherits a strictly positive H1_0 field coercivity constant from the full Q0. There is no silently frozen fluid or extra density mode.

For any L² right-hand pair, coercivity gives a unique weak H1_0 solution. It is a strong X solution: the second equation gives eta'' in L² because psi' and eta are in L²; the first gives (A psi'-q eta)' in L². Hence A psi'-q eta is H1, and the smooth positive A and smooth q imply psi' in H1. This yields H² regularity and a bounded inverse X<-Y, with estimates using the base coefficient bounds and the weak coercivity bound. There is no arbitrary forcing compatibility condition because field fluxes, unlike Dirichlet values, are not fixed.

Thus DF:X->Y is a bounded bijection with bounded inverse. Applying the local implicit-function argument to this C1 map supplies a unique local C1 branch (phi_lambda,chi_lambda) near the base, with identical field endpoints and mass. Density follows smoothly from the normalization formula. Positivity of rho and phi' persists on this neighborhood; coefficients remain elliptic there. No global continuation, fold statement or all-reference family is established. The parameter range is existential and unquantified.

## Response and susceptibility

The explicit parameter derivative is F_lambda=(q',-s). In the full fixed-mass displacement representation u_lambda=(xi_lambda,phi_lambda_derivative,chi_lambda_derivative), differentiating stationary equations gives

 a0(u_lambda,v)+ell(v)=0 for every v in H1_0 triples,
 ell(v)=-(1/C) integral(q psi_v'+s eta_v).

The integration by parts in q' has no endpoint contribution because psi_v=0. The exact hydrostatic derivative r[phi_lambda_derivative] supplies xi_lambda using the mass-zero formula above. With z defined by a0(z,v)=ell(v), uniqueness gives u_lambda=-z. The full inverse includes fluid response; a field-only inverse with density held fixed would yield the wrong z.

Define R(lambda)=integral T(phi_lambda',a_c exp(chi_lambda+lambda))/C. Chain rule gives

 R'=integral s/C + integral(q phi_lambda_derivative'+s chi_lambda_derivative)/C
    =integral s/C -ell(u_lambda)
    =integral s/C+beta, beta=ell(z)=Q0[z]>=0.

No conclusion R'>=0 follows from beta>=0 alone because s need not be positive. Only at an actual autonomous equilibrium intersection V'(lambda)=R(lambda) is the FGF033 Schur margin Delta=V''-integral s/C-beta=V''-R'. No potential is fitted and no intersection is asserted. Delta=0 is a zero linear margin, not a fold/hysteresis or nonlinear stability conclusion.

## Negative control: the old IVP derivative is not this response

Varying reference at fixed left IVP data generally changes total mass M(lambda), right phi and chi values even at the same D. Its density derivative includes the additional term rho M'/M:

 rho_lambda=rho M'/M-(rho/cs²)(phi_lambda-mean_rho phi_lambda).

If xi(0)=0, the displacement reconstructed from that density has xi(D)=-M'/rho(D), which is not an impermeable perturbation unless M'=0. The field derivatives also have nonzero right traces in general, unlike X. The weak inverse on H1_0 therefore cannot be substituted directly.

For local equilibrium energy differentiated along a varying-boundary/mass family, first variations explicitly include the chemical multiplier h0 M' and the boundary contribution [B phi_lambda+J chi' chi_lambda]/C, in addition to -R. Here h0=e'(rho)+phi is the constant hydrostatic multiplier. Thus the fixed-constraint envelope and susceptibility do not carry over after those terms are discarded. The original fixed-left source flux is likewise a different parameter constraint from fixed field endpoints.

Both positive a0 normalizations are separate base hypotheses; frozen H references are static coefficients and actual H histories are not derived. This is a local Q diagnostic BVP response theorem contingent on actual base regularity/coercivity. No RAR/M action, filtered-MONO or metric/photon transfer, physical V, local vacuum mechanism, calibration, global branch or theory closure follows. No mathematical computation executed.
