# FGF-023: balanced responsive-scale hydrostatic slab

2026-09-30. Worker /root/coupled_dynamics. Exact conditional derivation,
proof-only; no literature mechanism, observations or novelty assertion.
This is the inherited unfiltered Q/R scalar diagnostic extension, not the
operative filtered-MONO metric theory.

## 1. Action, units and exact equilibrium

Write C=4piG, tau=K/c²>0, sigma=J/v_chi²>0 with constant J>0, and cs²>0.
The field Lagrangian is

  [tau phi_t²/2-W(|phi_x|;a_ref exp chi)
   +sigma chi_t²/2-J chi_x²/2-U(chi)]/C,
  U=S0[cosh(2chi)-1]/4, S0>0.

Matter is an isothermal barotropic fluid with kinetic energy rho v²/2,
internal energy e(rho)=cs² rho[log(rho/rho_*)-1], and coupling -rho phi.
Thus p=rho e'-e=cs²rho and e''=cs²/rho. The arbitrary rho_*>0 changes only
the mass multiplier, not the equations. This is the same pressure-fluid
closure as the fixed-scale slab. The scalar force on matter is -phi_x.

Restrict to a finite patch x in [0,d] with g=phi_x>0. This restriction avoids
the zero-gradient degeneracy; no continuation through g=0 is claimed.
Define B=b(g,a)=F^(-1)(g;a), A=b_g>0, q=gA-B, T=-W_chi=gb-2W.
For Q and R, q>0. Retain Q F=sqrt(B²+aB) and R
F=B/[1-exp(-sqrt(B/a))] separately throughout. Exact static equations are

  B'=C rho,      cs² rho'=-rho g,
  phi'=g=F(B;a_ref exp chi),
  chi'=w,       J w'=U'(chi)-T(g,a).                    (E)

In particular A g'-q chi'=C rho. There is no subtraction of rho, uniform
support acceleration, extra matter species or prescribed cancellation force.
Incoming B(0)>0 is a gravitational boundary datum on a finite patch. This is
not a globally isolated, centered object with B(0)=0.

A valid existence construction: choose B(0)=B_i>0, rho(0)=rho_i>0,
chi(0)=0, w(0)=w_i>0 and phi(0)=0, with all coefficients above fixed and
finite. The right sides of (E) are smooth on B>0,rho>0,finite chi. Local ODE
existence gives a solution on some positive interval. By continuity choose
d small enough that w>w_i/2, rho>rho_i/2 and g>0. Then both rho and chi
are genuinely nonconstant: rho'<0 and chi'>0. B is increasing, and
rho=rho_i exp[-integral_0^x g(s)ds/cs²]>0. No cosh equilibrium at a constant
affine gravitational background is assumed. In fact chi''(0)=-T(g_i,a_ref)/J
is nonzero and negative; this is allowed in a short patch with w_i>0.

Set Dirichlet background values phi(0),phi(d),chi(0),chi(d) equal to those
induced by this actual IVP. The wall pressure equals the background pressure
at each wall. The fluid mass is the IVP-induced integral, fixed subsequently.
The wall tractions and imposed field values define a boundary-maintained slab;
they are not volume forces in its Euler or field equations. This proves
existence for an induced boundary family, not for arbitrary preassigned pairs
of wall values or a prescribed global mass. The exact flux balance is
B(d)-B(0)=C integral_0^d rho dx: the source is the MOND constitutive flux.

Use perturbations xi=psi=eta=0 at both walls, where xi is material fluid
displacement, psi=delta phi and eta=delta chi. No perturbation of field flux
is imposed in addition to these values. Impermeable walls imply
integral delta rho dx=-[rho xi]_0^d=0. The natural domain is real H1_0
triples, or smooth triples dense in it. Only longitudinal motion is treated.

## 2. Full quadratic energy and boundary flux

With r=delta rho=-(rho xi)' (here r is an Eulerian density perturbation,
not a radius), the linearized equations on the actual varying background are

  xi_tt=-[cs² r/rho+psi]',
  tau psi_tt-(A psi'-q eta)'=-C r,
  sigma eta_tt-J eta''+m eta-q psi'=0,
  m=U''-T_chi=U''-2T+gq.                              (L)

The derivatives in the second equation act on A and q as well as the fields.
They must not be replaced with constant coefficients. The scale equation
follows by delta T=q psi'+T_chi eta, so no q' term belongs in that equation.

The kinetic and potential quadratic forms are

  2K2=integral[rho xi_t²+(tau psi_t²+sigma eta_t²)/C] dx,
  2V2=integral[cs²((rho xi)')²/rho-2(rho xi)'psi
               +(A psi'²-2q eta psi'+J eta'²+m eta²)/C] dx.  (V)

The fluid second variation is valid at fixed total mass: hydrostatic balance
makes e'(rho)+phi constant, so higher-order density variations in a
mass-preserving perturbation multiply only the mass constraint. Field first
variations vanish by (E) and fixed field boundary values. There are no
additional omitted first-variation bulk terms proportional to chi' or rho'.

Direct substitution of (L) yields the complete quadratic energy boundary flux

  d(K2+V2)/dt = [(A psi'-q eta)psi_t/C
                  +J eta' eta_t/C-rho xi_t(cs² r/rho+psi)]_0^d.  (B1)

It vanishes for the stated fixed endpoint values. K2 is strictly positive in
nonzero perturbation velocities by assumption; no kinetic sign is inferred
from a rotation curve or from the background equations.

## 3. Corrected factorization and gradient terms

Expand the density square and integrate the term 2cs²rho' xi xi'. The
remaining displacement coefficient is

  cs²(rho'^2/rho-rho'')=rho g'
                       =C rho²/A+rho q chi'/A.

Integrating the density-potential interaction contributes
2rho xi psi' and the endpoint -2rho xi psi. Completing its combined field
square with -2q eta psi'/C therefore gives exactly

  2V2=integral { cs²rho xi'²
       +(A/C)[psi'+(C rho xi-q eta)/A]²
       +(J/C)eta'²+(M/C)eta²
       +(rho q/A)[chi' xi²+2xi eta] } dx
       +[cs²rho' xi²-2rho xi psi]_0^d,                 (F)

where M=m-q²/A. The displayed boundary term vanishes under the selected walls.
There are no discarded scale boundary terms in (F), since J eta'² has not
been integrated by parts there; the scale boundary term in time conservation
is explicitly in (B1).

The cosh potential has U''-2U'=S0 exp(-2chi). Applying the *nonuniform*
scale equilibrium J chi''=U'-T, rather than the uniform identity U'=T, gives

  M=S0 exp(-2chi)+Bq/A+2J chi''.                       (M)

Thus the positive uniform-field Schur identity from SD1 does NOT transfer
unchanged to a nonuniform slab. The chi'' term and the residual displacement
terms in (F) are exact required corrections. Even positive U'' alone does
not determine the full sign. No actual unstable slab is asserted here.

## 4. Explicit sufficient stability criterion and existence of survivors

For the given compact smooth background let

  rho_min=min rho>0, M_min=min M,
  N=max max[-rho q chi'/A,0], R=max |rho q/A|,
  alpha=cs²rho_min*pi²/d²-N,
  beta=(J*pi²/d²+M_min)/C.

All maxima/minima are over the slab. Assume

  alpha>0, beta>0, alpha*beta>R².                     (S)

Dropping the nonnegative completed psi square, applying the Dirichlet
Poincare inequality to xi and eta, and bounding the mixed integral by
2R ||xi||_2 ||eta||_2 give

  2V2 >= alpha ||xi||_2²+beta ||eta||_2²
                  -2R ||xi||_2 ||eta||_2 >=0.

Condition (S) makes this 2-by-2 form strictly positive whenever xi or eta is
nonzero. If xi=eta=0, (F) leaves integral A psi'²/C, positive for nonzero
Dirichlet psi. Hence V2 is strictly positive for every nonzero admissible
triple. With smooth bounded coefficients, strict margins also give coercivity:
reserve sufficiently small positive portions of the xi'² and eta'² terms
before the Poincare estimate, retaining (S); the square then controls psi'
using those reserved terms and L2 bounds. Positive K2 gives a positive
self-adjoint generalized longitudinal eigenproblem, with conserved positive
linear perturbation energy on this finite wall problem.

This sufficient condition is non-vacuous without a numerical spectrum.
Restrict the same valid local IVP to [0,d] as d decreases to zero. rho_min tends
to rho_i>0 while N,R,M_min remain finite. Therefore alpha and beta diverge
positively as d^-2 and alpha*beta as d^-4; (S) holds for all sufficiently
small d. Because w_i>0 and rho'<0 persist on such intervals, these are actual
responsive-scale, nonconstant-density equilibria. The result selects short
slabs with induced endpoint data, not an arbitrary astrophysical size or
parameters measured in a real system. Its stability is linear and conditional.

## 5. Eliminating the fields and the precise fixed-scale comparison

The field quadratic operator on Dirichlet (psi,eta) is

  Fop=[[ -partial_x A partial_x, partial_x(q .)],
       [ -q partial_x,           -J partial_x²+m ]].

The cross entries are adjoints with these boundary conditions. Under (S),
restriction to xi=0 proves Fop positive. Write f=(r,0). Minimizing V2 over
fields at fixed xi gives w_*=-C Fop^(-1) f and

  2Veff=integral cs² r²/rho dx-C <f,Fop^(-1) f>.        (SC)

For an explicit boundary check, first minimize only over psi in (F). Put
h=C rho xi-q eta. Dirichlet psi requires integral psi'=0. The minimizing
profile satisfies A psi'+h=s with constant
s=(integral h/A)/(integral 1/A), leaving the positive rank-one contribution

  (integral h/A dx)²/[C integral 1/A dx].               (D)

The completed square cannot generally be set to zero pointwise. Formula (SC)
uses the full Dirichlet inverse and retains this constraint automatically.
Our sufficient estimate discards (D) safely; it does not assert it vanishes.

This static Schur form is positive under (S) by the full bound just proved.
It is not automatically manifestly positive without a condition such as (S).
No universal instability or positivity claim outside that sufficient region
is earned. Static minimization is a potential-energy argument; it is not an
instantaneous elimination of the two dynamical fields when tau,sigma>0.

For the formal q=0 decoupling, g'=C rho/A, the mixed/chi' residuals vanish,
and (F) is the FGF-015 square plus the independent scale form
integral(J eta'²+m eta²)/C. The latter still needs its own positive bound.
Freezing eta=0 alone on a nonuniform chi background does NOT recover FGF-015:
the term rho q chi' xi²/A remains. Recovering the fixed-scale form requires
eta=0 and chi'=0. For Q/R with rho>0 and q>0, constant chi is incompatible
with the finite-J scale equation across varying g, as SD1 already proved.
The FGF-015 case is therefore the separately fixed-scale model, not a hidden
exact subfamily obtained by setting one perturbation to zero here.

## 6. Framework interpretation, dimensions and limits

J has units acceleration² length²; U,m,M have units acceleration²; q has
units acceleration; chi is dimensionless; xi has units length and psi units
velocity². In (S), alpha multiplies integral xi² and beta multiplies integral
eta², so alpha*beta and R² have the same units. The normalization C is never
silently set to one in the proof or source equation.

The reference a_ref may separately be 9.3619e-11 or 1.1279e-10 m/s² and obey
its adopted core definition a_ref=kappa c sqrt(G rho_Lambda,ref). The theorem
holds for either positive value: it does not fit or select a normalization.
Constant-vacuum reference and a frozen comparison a_ref=a0 E(z),
E²=.315(1+z)^3+.685, define separate stationary coefficient families. No
real-time H(z) trajectory is solved, and no cosmological friction is inserted.
The actual local scale a(x)=a_ref exp chi(x) varies. If the framework instead
requires that actual a satisfy the pointwise constant-vacuum relation, this
responsive-scale family remains incompatible. Positive perturbation energy
does not repair that physical interpretation.

No M local action is supplied or inferred from the registered M radial law.
No force-to-missing-mass conversion, cluster likelihood, metric/photon action,
3D or nonlinear stability, free-wall theorem, global isolated slab, arbitrary
boundary solvability, historical novelty or theory closure follows. This
proof-only pass closes the specified short-slab sufficient-positivity branch,
while leaving finite astrophysical domain sizes and boundary realism open.

A useful next discriminating task is an independently checked hydrostatic
slab on a prescribed physical interval with independently constrained endpoint
fields: compute whether (S) holds; if not, inspect its full quadratic operator.
Failure of a sufficient bound is not itself an instability certificate.
