# FGF-026: first endpoint zero and stability of the full continued slab

2026-09-30. Worker /root/coupled_dynamics. Conditional exact proof, not a
numerical continuation. The prior FGF-025 identity is inherited and attributed
there to the parent; this endpoint/domain proof is independently reconstructed
from the registered equilibrium and nonsingular quadratic form.

## 1. Fixed continuation, hypotheses and theorem

Keep one fixed set of initial data for the FGF-023 Q or R hydrostatic IVP
at x=0, with B(0),rho(0)>0, chi(0) finite and w(0)=chi'(0)>0. The data and
positive constants C=4piG, J, cs², tau=K/c², sigma=J/v_chi² and S0 do not
change while the right endpoint moves. The constitutive laws are separately

 Q: g=F(B;a)=sqrt(B²+aB),
 R: g=F(B;a)=B/[1-exp(-sqrt(B/a))],  a=a_ref exp chi.

Let A=b_g>0, q=gA-B>0, T=-W_chi, m=U''-T_chi,
M=m-q²/A, Rcoef=rho q/A>0 and U=S0[cosh(2chi)-1]/4.
Rcoef is a coefficient, not the R-law label. The background obeys

 B'=C rho,  cs²rho'=-rho g,  g=F(B;a),
 chi'=w,  Jw'=U'-T,
 A g'=C rho+q w,  Jw''=M w-C Rcoef.                  (1)

Assume a finite first zero D*>0 exists, with w>0 on [0,D*) and w(D*)=0,
and the solution is smooth and finite through x=D*, retaining B,rho,g>0.
In particular A,1/A,rho,1/rho,q,M and the required derivatives are bounded
on a neighborhood of [0,D*]. A regular endpoint permits a short ODE extension.
This is not a zero of gravitational g. Existence of a first zero for arbitrary
initial data is NOT asserted, and no specific continued orbit is computed.

For each right endpoint D, use the SAME IVP prefix [0,D], induced background
Dirichlet phi,chi values and wall tractions, and its induced total mass.
Perturbations xi,psi,eta lie in H1_0(0,D); each member has fixed total mass
because delta rho=-(rho xi)' has zero integral. The family changes its right
boundary data and total mass with D; it is not temporal evolution of one
fixed-boundary problem. No density subtraction or compensating volume force
appears in (1). This is not a fixed-mass family across D or a moving-wall
dynamical solution; mass is fixed only under perturbations of each member.

The theorem proved below is:
(a) the first zero is simple with w'(D*)<0;
(b) the original quadratic energy on the full interval [0,D*] is coercively
positive and has a strictly positive longitudinal spectral gap;
(c) for this same background continuation there is epsilon>0 such that the
full intervals [0,D] remain coercively positive for D*<=D<D*+epsilon.
These extended intervals contain negative w near their right endpoint.
Neither epsilon nor the gap is claimed uniform across families or quantified
by an unevaluated numerical constant.

A nonempty analytic first-turn subfamily can also be justified. This auxiliary
construction was supplied by /root during review and checked here: fix
B_i,rho_i>0 and chi_i=0, and vary only a small initial w_i>0. Then
w'(0)=-k with k=T(F(B_i,a_ref),a_ref)/J>0 independent of w_i. Uniform local
ODE continuity for initial w_i in a sufficiently small compact interval gives
one delta>0 with B,rho positive and w'<=-k/2 on [0,delta]. For
0<w_i<k delta/2, w reaches its first zero no later than 2w_i/k<delta.
This proves existence of some first-turn prefixes, without selecting numerical
initial data, a physical length or an observed endpoint. The general theorem
below applies to any regular first-turn prefix, including longer ones if they
exist; it does not use shortness of this auxiliary construction.

## 2. First-zero transversality

Positivity immediately to the left implies w'(D*)<=0. At a zero, (1) gives
w''(D*)=-C Rcoef(D*)/J<0. If w'(D*) were also zero, the Taylor expansion
w(D*-t)=w''(D*) t²/2+o(t²) would be negative for small t>0, a contradiction.
Hence w'(D*)<0. Put a_*=-w'(D*)>0. Then

 w(D*-t)=a_* t+O(t²),  w'/w=-1/t+O(1).                (2)

Thus w is comparable to D*-x near the wall. The continuation has w<0 just
to its right. No division by w will be used there.

## 3. Physical form domain and the singular-looking identity

The form domain at D* stays V=H1_0(0,D*)^3 for (xi,psi,eta). It is not
changed by a transformation eta/w. For every eta in H1_0, absolute
continuity and Cauchy-Schwarz yield

 |eta(x)|²/(D*-x) <= integral_x^D* |eta'(s)|² ds -> 0.  (3)

Combining (2)-(3) proves (w'/w)eta² ->0 at the right wall. At the left wall
w(0)>0 and eta(0)=0, so the analogous trace is zero. This handles the
endpoint term directly on the actual form domain.

We also need integrability, not only a formal endpoint limit. The elementary
Dirichlet Hardy bound

 integral_0^D* eta²/(D*-x)² dx <=4 integral_0^D* eta'² dx

follows first for smooth Dirichlet functions by integrating eta²/t² and
applying Cauchy-Schwarz, then by density. Together with (2) and regularity
away from the wall it proves eta/w is in L2 and

 w(eta/w)'=eta'-(w'/w)eta is in L2.

It also implies eta²/w is integrable. The mixed term involving xi is then
integrable; equivalently (eta+w xi)²/w is integrable by its elementary
two-square bound. Consequently all weighted integrals below are finite.

Importantly eta/w need NOT belong to H1_0 or have a finite right trace.
For example eta=t^(3/4) times a smooth cutoff near that wall belongs to
H1_0, whereas eta/w behaves as t^(-1/4). Treating the quotient as an ordinary
Dirichlet field would exclude valid perturbations. This tempting stronger
domain assumption is rejected and is not used.

## 4. Endpoint energy identity and strict positivity

The original nonsingular quadratic form is Q=2V,

 Q=integral { cs²[(rho xi)']²/rho-2(rho xi)'psi
       +(A psi'²-2q eta psi'+J eta'²+m eta²)/C } dx.     (4)

Its coefficients remain regular at D*. The positive kinetic form is

 2K2=integral {rho xi_t²+(tau psi_t²+sigma eta_t²)/C}dx.

On a truncated interval x<D*, the FGF-025 identity gives

 Q=integral {cs²rho xi'²
       +(A/C)[psi'+(C rho xi-q eta)/A]²
       +(J/C)w²[(eta/w)']²
       +(Rcoef/w)(eta+w xi)²} dx
   +[cs²rho'xi²-2rho xi psi+(J/C)(w'/w)eta²].           (5)

When applying this on [0,D*-delta], its upper boundary values must be kept;
they are not zero Dirichlet data on that artificial truncated endpoint.
Taking delta->0 is justified by Section 3 and H1 traces. Every displayed
boundary term tends to zero, and all integrals have finite limits. Thus (5)
with zero endpoint contribution holds on the full physical H1_0 domain.

Each integral term is nonnegative. If Q=0, the first gives xi'=0, hence
xi=0 by the walls. Since Rcoef/w>0 almost everywhere in the interior, the
fourth then gives eta=0. The second then gives psi'=0 and hence psi=0.
Therefore Q is strictly positive for every nonzero admissible perturbation.
This proof does not need a trace condition on eta/w at the zero wall.

The conserved quadratic energy flux remains

 [(A psi'-q eta)psi_t/C+J eta' eta_t/C
               -rho xi_t(cs² delta rho/rho+psi)]_0^D*=0

for fixed walls and smooth solutions, extending by the regular energy form.
The singular representation has not introduced an extra boundary flux.

## 5. Coercivity and spectral gap: a separate argument

Strict positivity alone does not ensure an infinite-dimensional gap.
Use the original regular form (4). Its leading derivative quadratic terms
are diagonal with coefficients cs²rho, A/C and J/C, uniformly positive on
the compact interval. All remaining terms have bounded coefficients and
at most one derivative. Young's inequality therefore gives constants
a>0 and b>=0, depending on this background, with

 Q[u]>=a ||u'||_2²-b ||u||_2², u=(xi,psi,eta).          (6)

This is also directly verified by expanding (rho xi)' and controlling
xi'xi, xi'psi and eta psi' against a chosen fraction of the positive
derivative terms. There are no hidden mixed highest-derivative terms.

Suppose there were no positive L2 gap. Since Q>=0, there would be u_n with
||u_n||_2=1 and Q[u_n]->0. Equation (6) bounds u_n in H1_0. A subsequence
converges weakly in H1_0 and strongly in L2 to u with ||u||_2=1.
The positive principal derivative part is weakly lower semicontinuous;
each bounded lower-order term converges using strong L2 and weak derivative
convergence. Thus Q[u]<=liminf Q[u_n]=0, contradicting strict positivity.
Therefore a background-dependent delta_*>0 exists such that

 Q[u]>=delta_* ||u||_2².                              (7)

Combining a small positive fraction of (6) with the remaining fraction of
(7) proves Q[u]>=c_* ||u||_H1² for some c_*>0. For example choose
0<theta<delta_*/(b+delta_*): theta times (6) plus (1-theta) times (7)
has positive derivative and L2 coefficients. This proves coercivity,
not merely absence of an exact zero mode.

The kinetic density matrix diag(rho,tau/C,sigma/C) has positive lower and
finite upper bounds. Its generalized Rayleigh quotient is consequently
bounded below by delta_*/m_max>0, where m_max is its upper coefficient bound
in a fixed choice of field units. The regular finite-interval form has
compact L2 embedding, so this yields the positive self-adjoint longitudinal
spectral gap. No numerical value of delta_* or c_* is claimed.

For dimensional precision, fix positive reference length L_ref, time T_ref
and energy-per-area E_ref, independent of the moving endpoint D. Use
s=x/L_ref and v=(xi/L_ref, psi/(L_ref²/T_ref²), eta), and define product L2/H1
norms by the sums of these dimensionless components and their s derivatives.
Apply the estimates to Q/E_ref in these fixed coordinates. Equivalent fixed
dimension-balancing weights give the same theorem. The kinetic quadratic form,
with the same field and energy scalings, restores the physical time units of
the generalized frequency squared. These fixed norm choices change constants,
never signs; no dimensionally mixed unweighted physical sum is intended.

## 6. Stable extension of the SAME full prefix

Use the regular ODE continuation on [0,D*+epsilon_0] with B,rho,g>0 and
bounded coefficients. Pull each full problem back to the fixed interval
s in [0,1] by x=D s and u(x)=v(s). Each field remains Dirichlet at s=0,1.
In the ORIGINAL form (4), derivative terms acquire 1/D and zeroth-order
terms acquire D, with background coefficients evaluated at D s. The mixed
terms transform consistently; using the expanded form includes rho'(D s).

Smooth background coefficients and D bounded away from zero imply a form
continuity estimate

 |Q_D^pull[v]-Q_D*^pull[v]|<=epsilon(D)||v||_H1(0,1)²,
 epsilon(D)->0 as D->D*.                              (8)

This is uniform in v: it follows by coefficient sup-norm convergence for
the derivative, mixed and zeroth-order terms. It does NOT use the singular
weighted coefficients 1/w, which cease to be suitable past the turn.

The established endpoint coercivity gives Q_D*^pull>=c_pull||v||_H1².
Choose epsilon>0 with epsilon(D)<c_pull/2 for
D*<=D<D*+epsilon. Then Q_D^pull>=c_pull||v||_H1²/2.
The pulled kinetic form also varies continuously and stays uniformly
positive/bounded on this small D range, so a positive longitudinal gap
persists locally in D.

The left initial data and the entire original prefix [0,D*] remain present;
the right wall alone is extended on the SAME continued solution. This is
not the previously known short symmetric patch centered at w=0. Negative w
appears near the new right wall, yet stability holds for a sufficiently small
extension because the original regular quadratic operator varies continuously.
No arbitrary-long continuation, second-turn or eventual instability is decided.

## 7. Dirichlet compatibility and static reductions

The potential square retains its exact minimum, with
h=C rho xi-q eta and Z_D=integral_0^D 1/A dx,

 min_psi integral A(psi'+h/A)²/C dx=(integral h/A)²/(C Z_D).

A is regular and positive through the turning point, so this wall constraint
has no singularity and is never discarded as an exact equality. The original
field operator remains the Dirichlet matrix
[[-partial A partial, partial(q .)],[-q partial,-J partial²+m]].
At D* and for the small stable extensions, restriction of the full coercive
form to xi=0 proves its positive invertibility; it is not inferred from U''.

After potential minimization the scale operator remains
L_eta=-J partial²+M+(l tensor l)/Z_D, l=q/A. Its positive inverse follows
from the full coercive field form and the bounded regular potential minimizer.
This preserves the previous static Schur formula with source
C Rcoef xi-l(integral C rho xi/A)/Z_D and factor -1/C in the eta subtraction.
Static minimization does not eliminate tau,sigma dynamical degrees of freedom.

## 8. Controls, rejected routes and scope

- A double first zero is impossible because its negative second derivative
  would force negative w just BEFORE the first zero. This is a one-sided
  first-zero conclusion, not a classification of every later zero.
- The trace estimate uses the tail integral of |eta'|², which tends to zero;
  merely eta(D*)=0 without H1 regularity would not justify the boundary limit.
- Requiring eta/w in H1_0 is false for the admitted t^(3/4) example.
- Declaring a gap solely because all nonzero vectors have positive energy
  would be incomplete. The regular-form estimate and compactness in Section 5
  are essential and explicitly supplied.
- Extending the weighted expression through w<0 and retaining a positivity
  interpretation is invalid. Section 6 instead uses coefficient continuity
  of the original nonsingular form on a fixed domain.
- A new small neighborhood around the turning point is not used as a
  substitute for the original full interval. A family member's mass and
  right boundary values change only as induced by the same IVP prefix.

No numerical experiment, spectrum, chosen dimensional length, measured wall
constraint or quantified extension size is supplied. The result is conditional
on a finite regular first zero along a fixed IVP; no claim that every IVP
reaches one. Its sign/gap conclusions are rigorous within this conditional
finite 1D boundary-maintained model.

The reference a_ref can separately equal 9.3619e-11 or 1.1279e-10 m/s²
under a_ref=kappa c sqrt(G rho_Lambda,ref), or be a distinct frozen H
comparison a0 sqrt[.315(1+z)^3+.685]. These are separate stationary families,
not a derived time-dependent H trajectory. Actual a=a_ref exp chi varies,
so literal pointwise constant-vacuum actual-a compatibility remains unresolved.
Source balance is MOND B'=C rho with the chosen Q/R F; no Newtonian
missing-mass replacement and no unregistered M local action is introduced.
No filtered-MONO, physical metric/photon, nonlinear/3D, free-wall,
observational or common-theory closure conclusion follows.

Next question: for a specified same-family continuation farther beyond the
first turn, locate a controlled loss of the ORIGINAL coercive gap, or prove
a further sufficient bound. Rechecking merely the first endpoint singularity
or another local centered patch would repeat a now-settled conditional step.
