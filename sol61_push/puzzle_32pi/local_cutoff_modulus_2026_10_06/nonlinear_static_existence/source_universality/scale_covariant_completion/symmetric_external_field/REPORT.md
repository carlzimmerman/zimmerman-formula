# A distinct external-field angular prediction of the symmetric candidate

The repaired symmetric candidate reproduces the parent's spherical acceleration law but has a different nonspherical response. Its actual constant-external-field linearized operator gives a deep-MOND perpendicular/parallel force ratio tending to 1/sqrt(2), rather than the QUMOND control's 3/4. The first angular correction is linked to the same free lambda as the spherical deficit and response moment. These are predictions of the declared NR branch, not a Cassini quadrupole, orbit likelihood, global covariant solution, or a selected vacuum coefficient.

## Action, external field and operational source
Use the corrected parent `covariant_vacuum_dictionary/REPORT.md` (66e0b010...) and its actual exchange-symmetric averaged-inverse interaction. Zero twin matter and the specified decaying perturbation boundary conditions give

div[mu(x) grad phi*]=Omega G_n rho,
Delta(phi+phihat)=Omega G_n rho,
phi=(phi*+Phi_N)/2,
x=|grad phi*|/a0.

On the eliminated auxiliary branch, write e=b(y)/[1+(y/T)^2], b=sqrt(1+1/y)−1, q_T=lambda T, x=y(1+2e), mu=y/x. Define D=d[y(1+e)]/dy, retaining T_y. Then dx/dy=2D−1. Here y is a constitutive coordinate; it equals the actual source Newton acceleration in the spherical branch. It is not generally the Newton acceleration of a nonspherical external environment.

Choose a finite nonzero uniform external star gradient a0 x_e n_hat, and perturb it with a weak source. Its local y_e is defined by the admitted stationary branch. An external uniform sum-potential gradient is an independent boundary datum; one may choose an aligned spherical-compatible benchmark, but the response below only requires the external star gradient. The observable internal physical force is −grad delta phi. This distinguishes the source dictionary from merely calling an interaction coordinate an observed acceleration.

The admitted sufficient interval 0<lambda<5/192 ensures the local inverse and positive source operator along this branch. Linearization requires |grad delta phi*| much smaller than a0 x_e over the region of use. A point distribution below is a formal Green source of this constant-coefficient operator, or a far-zone leading mass monopole matched to a body if the nonlinear inner solution exists. It is not an exact all-radius nonlinear point-body solution. No existence or global external-field embedding is proved here.

## Fully eliminated linear response
Vary both the auxiliary field and star slope: delta T=T_x delta x. Therefore

A_ij=mu delta_ij+x mu_x n_i n_j=mu[delta_ij+L n_i n_j],
L=d ln mu/d ln x=1/[mu(2D−1)]−1.

Let h=1+L. Its transverse eigenvalues are mu>0 and its longitudinal eigenvalue is mu h=1/(2D−1)>0. Freezing T would replace D by a different partial derivative, and changes the angular prediction. Static ellipticity of this operator is not full covariant metric/scalar kinetic health.

For a source mass m in spatial n>=3, take the axis n_hat as z, transverse distance R, and Omega as the unit (n−1)-sphere area. The exact Green solution of A_ij partial_i partial_j delta phi*=Omega G_n m delta^n(r) is

delta phi*=−G_n m/[(n−2)mu sqrt(h)] [R^2+z^2/h]^−(n−2)/2.

To verify charge, set z=sqrt(h) z_tilde. The operator becomes mu times the ordinary Laplacian and delta^n(r)=delta^n(r_tilde)/sqrt(h). Using Delta r^(2−n)=−(n−2)Omega delta fixes both the factor (n−2) and sqrt(h). The solution vanishes at infinity in n>=3. An ellipsoidal Gaussian surface carries exactly Omega G_n m flux.

The Newton Green potential is −G_n m/[(n−2)r^(n−2)], so physical delta phi is their half sum. At u=cos(theta) its potential enhancement over Newton is

E_n(u)=(1/2){1+[mu sqrt(h)]^−1 [1−u^2+u^2/h]^−(n−2)/2}.

Radial force enhancement is the same E_n; an angular force component also exists away from the symmetry axes. On the axes that component vanishes. Thus

E_perp=(1/2)[1+1/(mu sqrt(h))],
E_parallel=(1/2)[1+h^((n−3)/2)/mu].

Only in n=3 does E_parallel=(1+1/mu)/2=1+e=nu(y_e). One must not extend this simplification to arbitrary n. The general-n result keeps calibrated G_n and its Gauss normalization.

## Deep angular response and differentiable expansion
The parent deep force deficit is A(lambda)=sqrt(7lambda/8). An asymptotic little-o expression alone cannot be differentiated. To justify the required derivatives, put h0=y^(1/4), U=T/y^(7/8). Rescale the exact stationarity integral t=yv. It becomes

lambda U^4=4 integral_0^1 v^(5/2) sqrt(1+h0^4 v)/(1+h0 v^2/U^2)^2 dv
             −4h0^2 integral_0^1 v^3/(1+h0 v^2/U^2)^2 dv.

This is analytic in real h0 near zero and positive U near K=(8/(7lambda))^(1/4); its implicit derivative with respect to U at (0,K) is 4lambda K^3, nonzero. Uniform bounded denominators permit differentiation under the finite integral. Its unique local analytic branch has

U=K[1−(7/22)A h0+O(h0^2)].

This yields differentiable series

x=2sqrt(y)[1−A y^(1/4)+O(sqrt(y))],
mu=(sqrt(y)/2)[1+A y^(1/4)+O(sqrt(y))],
2D−1=y^−1/2[1−(3/2)A y^(1/4)+O(sqrt(y))],
L=1+A y^(1/4)+O(sqrt(y)).

In particular h tends to 2. In n=3 the angular enhancement normalized by the parallel value tends to 1/sqrt(2−u^2). Its perpendicular/parallel ratio has the sharper prediction

R_ang=E_perp/E_parallel=2^−1/2[1−(A/4)y_e^(1/4)+O(sqrt(y_e))].

Define B=lim[y_e→0] y_e^−1/4[2^−1/2−R_ang]. Then B=A/(4sqrt(2)) and B^2=7lambda/256. This is an extra local-response observable beyond the matched spherical force law. Expressing it against a measured external physical acceleration would require the external-field boundary/source dictionary, not an automatic substitution of y_e.

The audited moment inequality Cresp A^2<7pi^2/128 implies the sharp conditional response relation

0<Cresp B^2<7pi^2/4096,
lim[lambda→0] Cresp B^2=7pi^2/4096.

It relates two features of this specific interaction; Cresp becomes Lambda only under the parent's unresolved covariant vacuum admission and chosen UV normalization. Lambda remains free. No measured angular ratio, fit or target insertion is performed here.

## QUMOND primary control and relationship to Claude p57
The comparison is to a different action, not a transfer of its response. [Milgrom, arXiv:0911.5464v2](https://arxiv.org/pdf/0911.5464v2), equations 63,67–69, gives the QUMOND external-dominated equation and distinguishes it from the nonlinear Poisson operator. In the control, linearizing Delta psi=div[nu grad Phi_N] gives Delta psi=nu_e[Delta Phi_N+K_e partial_z^2 Phi_N], K_e=d ln nu/d ln y. Its three-dimensional point Green response is

psi_Q=−G_3 m nu_e/r [1+(K_e/2)sin^2(theta)].

This can be independently verified away the source and distributionally: partial_z^2(−Gm/r) has a 4pi Gm delta/3 part, fixing the angular mean. In deep MOND K_e tends to −1/2, so perpendicular/parallel tends to 3/4, unlike the symmetric candidate's 1/sqrt(2). Equation 63 states the equivalent expression in the primary paper's inverse-function notation. The preferred axes need not coincide in a general external environment.

Claude p57's original QUMOND external-field/quadrupole calculation is therefore relevant as a distinct-action control, but its likelihood, continuum moment inversion and higher multipoles cannot be imported into this symmetric candidate. The new arrow closed here is an actual nonspherical local source-response prediction. The missing arrow is a global covariant/external-environment solution and a separately derived observable analysis. No recombination, thermodynamic cold phase, particle identity, or world novelty claim is made.

## Evidence
checks.py tests the Green PDE and flux Jacobian, exact source/IFT coefficients, and bounded 45-digit stationary-root evaluations at five declared (lambda,y) pairs plus two derivative-control neighbors. Controls remove actual auxiliary response in D, replace the angular prediction by QUMOND, or remove the Green sqrt(h) charge normalization. Contract/provenance and standard run manifests record actual source hashes and resource caps. Analytic statements above do not follow merely from sample success.
