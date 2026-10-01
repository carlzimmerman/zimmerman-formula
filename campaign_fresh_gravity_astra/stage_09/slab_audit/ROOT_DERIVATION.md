# Independent root derivation for the FGF-023 review

Written while the FGF-023 author derives independently, 2026-09-30.
This is the local diagnostic SD1 Q/R action, not filtered MONO.
C=4piG; a=aref exp(chi); g=phi'>0, B=b(g,a), lambda=b_g>0,
q=g lambda-B=-b_chi, T=-W_chi, m=U''-T_chi, J>0, cs²>0.
Use U=S0[cosh(2chi)-1]/4 with S0>0. No imposed matter subtraction.

## Compatible background

On an interval not crossing B=0, solve the smooth first-order system
B'=C rho, rho'=-rho F(B,a)/cs², chi'=s,
s'=[U'(chi)-T(F(B,a),a)]/J and phi'=F(B,a).
Positive initial B,rho and finite chi,s give a local smooth solution with
B,rho>0 by local ODE existence and continuity. Choose the domain within that
existence interval. Its endpoint phi,chi values define fixed Dirichlet field
boundary data; fixed walls support endpoint pressures. This is a bounded
slab patch, not a symmetric self-gravitating slab with g=0 center, nor a
solution for arbitrary independently prescribed boundary values. There is no
uniform-density subtraction or artificial cancellation of the local force.
The mass of the equilibrium is fixed against perturbations.

## Full quadratic form

Use displacement xi=0 at both endpoints, psi=delta phi=0 and eta=delta chi=0
at both endpoints. Then delta rho=-(rho xi)' has zero integrated mass.
For isothermal internal energy e(rho)=cs² rho[ln(rho/rho_ref)-1],
e''=cs²/rho and e'(rho)+phi is constant by hydrostatic balance.
The constrained Hessian is therefore

2V=integral {cs²[(rho xi)']²/rho -2(rho xi)'psi
 +[lambda psi'²-2q eta psi'+J eta'²+m eta²]/C} dx.

The kinetic quadratic form is positive if tau=K/c²>0 and sigma=J/vchi²>0:
2T2=integral {rho xi_t²+(tau psi_t²+sigma eta_t²)/C} dx.
The constrained-density Hessian is legitimate because the first density
variation is a constant chemical potential; second-order total-mass variations
integrate to zero. No second-order matter term has simply been discarded.

Hydrostatic balance gives cs² rho'^2/rho-cs² rho''=rho g'.
The flux derivative is lambda g'-q chi'=C rho. After integrating the matter
terms and completing the potential-gradient square,

2V=integral {cs² rho xi'²
 +lambda/C [psi'+(C rho xi-q eta)/lambda]²
 +J eta'²/C +(m-q²/lambda)eta²/C
 +rho q chi' xi²/lambda +2rho q xi eta/lambda} dx
 +[cs² rho' xi²-2rho xi psi]_left^right.

The endpoint term vanishes under these walls. The extra last two volume terms
are why the fixed-scale FGF015 positive-square proof does not automatically
transfer. Freeze eta AND chi'=0 to recover its expression. Formally q=0 also
removes the new matter/scale terms. Setting eta=0 alone on a variable-scale
background leaves the chi' term. Likewise a field Schur bound alone does not
certify positivity of this coupled form.

## Explicit sufficient condition, not a necessary threshold

On a compact interval of length D define
A=cs² rho_min pi²/D² + inf(rho q chi'/lambda),
Bstar=J pi²/(C D²)+inf[(m-q²/lambda)/C],
Dmix=sup|rho q/lambda|.
Poincare on xi,eta, followed by Cauchy-Schwarz, bounds 2V below by the
nonnegative square plus
A||xi||²+Bstar||eta||²-2Dmix||xi||||eta||.
If A>0, Bstar>0 and A Bstar>Dmix², the potential is positive for every
nonzero admissible triple (xi,psi,eta). If xi=eta=0, the remaining square
forces psi'=0, hence psi=0 by Dirichlet conditions. On sufficiently short
subintervals of any smooth nondegenerate background these inequalities hold:
finite negative lower-order coefficients are dominated by D^-2 terms.
This is a sufficient longitudinal wall-stability condition. Failure of these
inequalities is inconclusive, not proof of an unstable mode.

Both a_ref normalizations 9.3619e-11 and 1.1279e-10 m/s² can be used as
separate positive inputs. A frozen a_ref=a0 E(z) snapshot is a distinct
comparison; neither an evolving H solution nor constant-vacuum identification
of the local dynamic a follows. No registered M action is assumed. No source
mass/discrepancy or instrument inference was computed. Boundary-supported
local slab stability does not establish free-boundary, global, nonlinear,
3D, zero-field, relativistic or filtered-MONO stability.
