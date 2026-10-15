# A dynamical charged core exists, but the weak-neutral co-Plummer family is radially unstable

VC3-CORE-001, 15 October 2026. This removes the previously prescribed central mass/charge **at the level of an exact Newtonian rest-mass two-fluid equilibrium**. The required charged EOS is an inverse construction, not derived microphysics. A coupled conserved-mass radial energy test then gives a negative direction throughout the critical-charge weak-neutral family specified below. Thus this background is an advance in force balance and a failed stability candidate, not a completed theory.

## Actual conserved species and frame

There are two independently conserved massive number currents: a charged core c with q_c/m_c=b_q sqrt(4 pi G), and a neutral species s with q_s=0. Their rest densities are rho_c=m_c n_c and rho_s=m_s n_s. The constitutive frame is varied with **both** actual currents,

\[
 K^\mu=m_cJ_c^\mu+m_sJ_s^\mu,\qquad U^\mu=K^\mu/\sqrt{-K^2}.
\]

Use the inherited diagonal barotropic current action, minimal coupling +q_c J_c.A, electric law D=E/(1+E/D0), and an admitted positive magnetic response. The electromagnetic field energy does not source gravity in this Newtonian comparison; the gravitational source is exactly rho_c+rho_s. No external central density, held charge distribution, baryons, conversion, or background-subtracted charge is present. This is not the full Einstein/current solution.

At a co-moving static purely electric background, all first frame variations vanish by the previously derived identity E^mu F_mu nu=-E^2 U_nu and U.delta U=0; all first beta B^2 variations vanish too. Therefore the species equations are ordinary neutral hydrostatics and charged hydrostatics with the actual Gauss force. The choice of a magnetic response does not alter these background equations.

## Exact two-fluid background with a chosen charged EOS

Fix M>0, scale b>0 and f>0. Put

\[
 \rho_c={3Mb^2\over4\pi(r^2+b^2)^{5/2}},\quad
 \rho_s=f\rho_c,\quad
 M_c(<r)={Mr^3\over(r^2+b^2)^{3/2}},\quad
 \psi_c={GM\over\sqrt{r^2+b^2}},\quad
 \Phi=-(1+f)\psi_c.
\]

Both masses are finite, the densities are positive at every finite radius, and neither current requires a finite vacuum boundary. Here b is the length scale, distinct from the dimensionless charge ratio b_q. With t=r/b and

\[
 q_0={b_q GM\over a_0b^2},\quad
 x={D\over D_0}=q_0{t\over(1+t^2)^{3/2}},\quad
 x_{\max}={2q_0\over3\sqrt3},\quad D_0={a_0\over\sqrt{4\pi G}},
\]

the charged species acceleration is

\[
 {q_c\over m_c}E={b_q^2 g_c\over1-x},\qquad
 g_c={GM r\over(r^2+b^2)^{3/2}}.
\]

Charge and gravitational mass are therefore counted separately. The force balances are

\[
 P_s'=-\rho_s(1+f)g_c,\qquad
 P_c'=-\rho_cg_c\left(1+f-{b_q^2\over1-x}\right). \tag{1}
\]

The neutral EOS is the chosen n=5 polytrope P_s=K_s rho_s^(6/5), normalized so its specific enthalpy is w_s=(1+f)psi_c. To define a barotropic core EOS, set rho_*=3M/(4 pi b^3), y=(rho_c/rho_*)^(1/5)=1/sqrt(1+t^2), and

\[
 X(y)=q_0y^2\sqrt{1-y^2},\quad
 w_c(y)={GM\over b}\left[(1+f)y-b_q^2\int_0^y{dz\over1-X(z)}\right],
 \qquad P_c(\rho)=\int_0^\rho z\,w_c'(z)\,dz .            \tag{2}
\]

The prime on w_c in the pressure integral means derivative with respect to its density argument, not y. Then dw_c/dr equals the right side of (1) divided by rho_c, so (1) holds exactly. The pressure tends to zero at infinity. Its Newtonian sound speed is

\[
 c_{c,N}^2={dP_c\over d\rho_c}
 ={\psi_c\over5}\left(1+f-{b_q^2\over1-x}\right),\qquad
 c_{s,N}^2={(1+f)\psi_c\over5}.                         \tag{3}
\]

The strict condition

\[
 b_q^2<(1+f)(1-x_{\max})                               \tag{4}
\]

is sufficient and, for positivity of (3) everywhere, necessary. It gives positive w_c, P_c, and both compressibilities throughout the occupied equilibrium. The internal energy can be defined thermodynamically by epsilon_a=rho_a c^2+u_a and u_a=rho_a integral_0^rho_a P_a(z)/z^2 dz. This is a chosen continuum EOS. At the central density, X(y) has a square-root endpoint; P_c is C1 and its energy is C2 but higher smoothness is not established. No arbitrary smooth microphysical extension above rho_* is inferred.

For critical charge b_q=1, (4) becomes x_max<f/(1+f). Thus an exactly critical pressureless core with no neutral mass does not acquire inward support from the nonlinear electric law: its force is outward. A small neutral population and its own pressure can instead make (1) a genuine static solution.

## The coupled radial Hessian, with Gauss and both masses varied

Let delta m_c(r), delta m_s(r) be Eulerian enclosed rest-mass perturbations. Each vanishes at r=0 and infinity. Their densities are eta_a=delta m_a'/(4 pi r^2), and their radial displacements satisfy delta m_a=-4 pi r^2 rho_a xi_a. For smooth finite-energy perturbations, electrostatic Gauss fixes delta D=b_q sqrt(4 pi G) delta m_c/(4 pi r^2). The electric Hamiltonian Hessian is dE/dD=(1-x)^-2 in the radial direction. Therefore the full radial potential-energy second variation is

\[
 Q=\sum_a\int_0^\infty {c_{a,N}^2\over4\pi\rho_a r^2}
                  (\delta m_a')^2dr
 -G\int_0^\infty{(\delta m_c+\delta m_s)^2\over r^2}dr
 +G b_q^2\int_0^\infty{(\delta m_c)^2\over r^2(1-x)^2}dr. \tag{5}
\]

This retains the core-neutral gravity cross term and the nonlinear gauge Hessian. It is not the old fixed-source neutral Hessian. The chemical/electrostatic equilibrium first integrals are zero with the potentials normalized at infinity, so constraint-path second-order terms cancel in the usual energy expansion. Formula (5) is the Eulerian density/Gauss Hessian, not a Hessian of H(E) at fixed electric field.

Use r in units b, masses in units M, and Q in units GM^2/b. At critical charge write delta m_c=u and delta m_s=fv, and A(r)=(1+r^2)^2/(15r^2). Then

\[
 Q=\int_0^\infty\left\{
 A\left[\left(1+f-{1\over1-x}\right)u'^2
                 +f(1+f)v'^2\right]
 +{1\over r^2}\left[{u^2\over(1-x)^2}-(u+fv)^2\right]
 \right\}dr .                                        \tag{6}
\]

Electrostatic perturbations are admissible initial data of the dynamical gauge system, with magnetic field zero. The positive velocity/current-frame terms do not remove a negative potential-energy direction.

## A single finite-inertia trial rules out the entire weak-neutral critical family

Take **any** 0<f<=1/1000 with critical b_q=1 and positive compressibility (4). Choose the fixed radial test

\[
 u=Y={25r^3\over(1+r^2)^2(25+r^2)},\qquad v=kY,\quad k={8\over5}. \tag{7}
\]

At zero, Y=O(r^3); at infinity Y=O(r^-3). Thus both conserved masses vanish at both endpoints. The associated xi_a=O(1) at infinity, so integral rho_a xi_a^2 4 pi r^2 dr is finite. The density ratio eta_a/rho_a stays bounded, making these tangents admissible on sufficiently small positive-density paths.

Put phi=r/(1+r^2)^(3/2), so x=q0 phi. Define

\[
 I_A=\int A Y'^2={1375\pi\over93312},\quad
 I_B=\int {Y^2\over r^2}={3125\pi\over124416},\quad
 I_{B2}=\int {Y^2\phi^2\over r^2}={948125\pi\over429981696},
\]

and T=integral[-A Y'^2 phi+2Y^2 phi/r^2]. Exact rational integration after z=sqrt(1+r^2) gives

\[
 T={512521825\over16052649984}
 +{7152625\sqrt6\pi\over55037657088}
 -{7152625\sqrt6\arctan(\sqrt6/12)\over27518828544}>0. \tag{8}
\]

All unspecified integral limits are zero to infinity. Since x<1/1000 and

\[
 {1\over1-x}\ge1+x,\qquad
 {1\over(1-x)^2}\le1+2x+{3x^2\over(1-1/1000)^2},
\]

substitution in (6) yields the analytic upper bound

\[
 Q\le f[1+(1+f)k^2]I_A-(2fk+f^2k^2)I_B
             +q_0T+{3q_0^2 I_{B2}\over(1-1/1000)^2}.    \tag{9}
\]

Condition (4) implies q0<(3sqrt3/2)f/(1+f)<(13/5)f. Using T>0 and defining

\[
 L=(1+k^2)I_A-2kI_B+{13\over5}T,
 \quad B=k^2(I_A-I_B)
       +{3(13/5)^2 I_{B2}\over(1-1/1000)^2},
\]

one obtains Q/f <= L+fB <= L+B/1000. Exact rational interval arithmetic, using alternating arctangent series and Machin's identity for pi, certifies

\[
 B>0,\qquad -0.002369<L+B/1000<-0.002368<0.             \tag{10}
\]

Consequently **every** critical-charge co-Plummer background in 0<f<=1/1000 satisfying positive charged compressibility has this negative coupled radial energy direction. This is an analytic family obstruction; a finite eigenvalue scan is not being used to prove the universal statement.

The negative Hessian defeats positive-energy closure. With a positive kinetic form, a suitable self-adjoint spectral realization gives negative spectral support and linear growth; this report does not assume or prove a complete spectral-domain theorem for the full nonlinear current/gauge PDE. It does prove that the desired positive coupled radial energy cannot hold for this family.

## Explicit witness and interpretation

The assigned example b_q=1, f=1/1000, q0=1/400, GM/(bc^2)=10^-6 satisfies (4) strictly. Direct 60-digit quadrature of (6) on (7) gives approximately -5.6826476327e-6; the analytic upper bound (9) is approximately -5.6589240089e-6. Both are negative. They are in units GM^2/b, not an eigenfrequency.

This example can also pass the inherited local principal gate by a very large margin. For either species h_a(1-s_a^2)=rho_a[c^2+w_a-c_{a,N}^2] >=rho_a c^2[1-epsilon0(1+f)/5]. With actual mass weights in K, the harmonic h_* is at least (rho_c+rho_s)c^2 times the same bracket. Substitution of the Plummer charge field gives

\[
 {h_{\rm crit}\over h_*}\le
 {\epsilon_0q_0\over3(1+f)[1-\epsilon_0(1+f)/5]}
 {t^3\over(1+t^2)^2(1-x)^2}<10^{-9}.                  \tag{11}
\]

Here t^3/(1+t^2)^2<1/2, x<1/1000 and the bracket exceeds 999/1000. Thus principal-energy/cone health does not establish the coupled finite-radius density stability. At r=0 the inherited E>0 cone theorem needs the separately specified occupied-phase patch; the radial negative direction already exists away from any ambiguity of that point.

The next meaningful alteration must change the candidate, for example the charged/neutral density shapes, EOS choice, or extra reciprocal interactions. Merely increasing q0 within the positive-pressure co-Plummer window, or checking another homology direction, cannot remove (10). This obstruction does not rule out all charged pressure-supported cores, other f ranges, other charge ratios, or a controlled relativistic branch.

## Reproduction and limits

`check_core_v3.py` checks the exact background/Gauss/EOS identities, the five exact trial integrals, the normalized full radial Hessian, strict assigned-parameter inequalities, rational interval certificate (10), and independent high-precision quadrature. `computation_contract_v3.json` fixes its input revisions and bounds. The analytic inequalities above establish the family obstruction; the bounded computation audits the reduction and constants.

No arbitrary inverse EOS is described as derived microphysics; no cosmic abundance, charged-core population mechanism, conversion/settling history, empirical pass, Einstein closure, or nonlinear well-posedness is claimed. The preceding fixed-central-source positive neutral Hessian remains correct in its declared scope but cannot certify this moving-core system.

The preserved `run_v1` is an implementation failure in a maximum-value substitution assertion (missing parentheses), before the mathematical integral and interval checks. `check_core.py` and `DRAFT_PROOF_V1.md` preserve its exact draft inputs. It is not supporting evidence. `run_v2` is a successful draft run, archived because independent review corrected only the displacement tail from O(r^-2) to O(1). The inertia remains finite. `DRAFT_PROOF_V2.md` preserves its draft proof; `run_v3` is authoritative if successful.
