# Vacuum limit obstruction, a narrowed occupied phase, and a reciprocal interface

VC3-VAC-001, 15 October 2026. Conditional research result, not closure of the
physical theory. The source copies and actual checkout are pinned in
`inputs/source_manifest.json`. No prior proof or canonical law is amended.

There are three distinct conclusions: a positive Maxwell magnetic coefficient
cannot extend continuously over the **whole** old occupied cone branch; an
explicit smaller occupied phase repairs that coefficient limit and the occupied
electric origin; and a separate Maxwell exterior has a variational matching
condition that differs from a zero-pressure fluid edge. The latter supplies a
concrete interface candidate, not a solved or stable global interface.

## 1. Exact obstruction on the entire old branch

Use c=1, D0>0, E=|E_U|, t=(1+E/D0)^-1, x=1-t, p=t^2, and the effective
material inertia h=h_s(1-s_s^2)>0. The material current is timelike. On a
co-moving pure-electric background the inherited all-angle discriminator is

\[
 F(\beta)=p-\beta-
 \frac{E^2(t-\beta)^2}{h+E^2(t-\beta)}.
\]

The perpendicular sector makes this necessary as well as sufficient for the
strict metric-cone bound in the inherited positive-kinetic family. Multiplying
by the positive denominator gives

\[
 N(\beta)=h(p-\beta)-E^2(t-\beta)(t-p).
\]

Here hc=E^2 x and E^2(t-p)=t hc. On h>hc, N is strictly decreasing in beta.
Consequently the exact admitted interval is

\[
 0<\beta<\beta_L
 =p\frac{h-h_c}{h-t h_c}
 =p\frac{\delta}{\delta+x},\qquad
 \delta=\frac h{h_c}-1>0.                              \tag{1}
\]

For example take x>0 tending to zero, E=D0 x/(1-x), and
h=hc(1+x^2). These are all strict occupied-branch points, yet

\[
 0<\beta<\frac{(1-x)^2 x}{1+x}\longrightarrow0.        \tag{2}
\]

No beta satisfying this cone bound everywhere on h>hc has a continuous
extension at (E,h)=(0,0) with **any positive** vacuum value, in particular the
Maxwell value one. The obstruction is not specific to the old quarter patch.
More generally, beta approaching one requires delta/x tending to infinity;
delta/x tending to k in [0,infinity) bounds limsup beta by k/(1+k).

This proves no global impossibility for a different electric law, different
principal degrees of freedom, selected background path, different allowed
domain, discontinuous phase, or a theory tolerating a wider cone. It is a
necessary obstruction within the inherited action and strict metric cone.
The regular-core atmosphere has h~r^-5 and hc~r^-6, hence delta~r and
x~r^-2; it is far from the obstructing paths. A failure on the entire branch
must not be relabeled a failure of that selected asymptotic background.

## 2. Explicit coefficient on a narrowed occupied phase

Fix a chosen kappa>0 and retain only

\[
 \mathcal W_\kappa=\{E>0,\ h\ge(1+\kappa)h_c(E)\},
\]

together with E=0,h>0. Define

\[
 \eta=\frac h{D_0^2+h},\quad
 a=\frac{D_0\eta}{16},\quad
 \beta_0=1-\frac\eta2,\quad
 \beta_* =\frac{\beta_L}{1+x}.                         \tag{3}
\]

The parent beta_* has 0<beta_*<beta_L<p<t for E>0. Let chi(s) be a smooth
cutoff in [0,1], equal to one for s<=1/4 and zero for s>=1. Explicitly take
j(z)=exp(-1/z) for z>0 and zero otherwise and
chi(s)=j(1-s)/[j(1-s)+j(s-1/4)]. Define beta=beta0 directly for
E^2<=a^2/4. Elsewhere use

\[
 \beta=\chi(E^2/a^2)\beta_0+
       [1-\chi(E^2/a^2)]\beta_*.                      \tag{4}
\]

This construction also makes sense on the full occupied strict branch, but
only its restriction to W_kappa has the Maxwell joint limit asserted here.
On the blend E<=a one has

\[
 e:=E/D_0\le\eta/16,\quad
 E^2/h\le\eta/256,\quad
 p\ge1-2e,\quad
 t>\beta_0.
\]

Thus the denominator is at least h and 0<t-beta0<1, so

\[
 F(\beta_0)\ge\eta/2-2e-E^2/h
 \ge\frac{95\eta}{256}>0.                           \tag{5}
\]

Also hc/h=(E^2/h)x<=eta^2/4096<1; the parent endpoint is defined in the
blend. N is affine in beta, so (4) retains N>0 and 0<beta<t. This is an
all-angle statement through the inherited theorem, not angular sampling.

At every h>0, a>0 and beta is exactly beta0(h) in an electric-vector
neighborhood of zero. It is smooth there jointly with positive density and
removes the old magnetic |E_U| B_U^2 defect. The electric Le remains C2,
not C3, at its electric origin; no smoother action or nonlinear PDE theorem
is asserted. At E=0 the transverse gauge speed squared is beta0 in (1/2,1).

For h,E tending jointly to zero within W_kappa, eta tends to zero and
delta>=kappa. Equations (1) and (3) give

\[
 \beta_0\to1,\qquad
 \beta_*=(1-x)^2\frac{\delta}{\delta+x}\frac1{1+x}
 \to1
\]

uniformly in delta>=kappa. Hence every blend also tends to one. This replaces
the old quarter patch's two different coefficient limits on this domain.
The Plummer tail eventually lies in every fixed W_kappa and has chi=0,
because E~r^-2 while a~h~r^-5. Its coefficient therefore tends to one.

This is a new constitutive postulate. It does not define U at J=0, cover
finite radiation fields with vanishing matter, establish nonzero magnetic
background health, or provide a uniform nonlinear tail neighborhood. A
continuous scalar coefficient is less than a covariant vacuum action.

## 3. Why simply removing the frame fails for the unchanged electric law

Consider a Lorentz invariant parity-even vacuum action L(X,Y), with
X=(E^2-B^2)/2 and Y=E dot B. Reproducing the old electric function on B=0
requires L_X(E^2/2,0)=D/E=t. The longitudinal electric Hessian is p=t^2.
For a wavevector perpendicular to the electric background, the polarization
with electric perturbation parallel to E has magnetic perturbation
perpendicular to E. It has delta Y=0; parity makes L_XY vanish at Y=0.
Its magnetic coefficient is therefore beta=t and its exact vacuum squared
speed is

\[
 c_\perp^2=t/p=1/t=1+E/D_0>1.                        \tag{6}
\]

Changing L_YY affects the other polarization, not this obstruction. Thus this
common frame-free completion of the unchanged law does not satisfy the
desired metric cone in any positive electric neighborhood of vacuum. A
separate Maxwell phase evades (6) by changing the electric law there.

## 4. A reciprocal sharp Maxwell phase and its matching equations

Let a timelike material interface Sigma enclose an occupied region Omega.
Take one gauge potential with continuous tangential pullback, a separately
conserved interior matter current with J dot N=0 at the interface, and the
chosen action

\[
 S=\int_\Omega\sqrt{-g}\,[L_{\rm fluid}+L_e(E_U)
                         -\beta(E_U,h)B_U^2/2]
   +\int_{\Omega^c}\sqrt{-g}\,[-F_{\mu\nu}F^{\mu\nu}/4]
   -\sigma\int_\Sigma\sqrt{-\gamma}.
                                                               \tag{7}
\]

The interface is advected with the material boundary; particles do not
exchange with an uncounted reservoir. The outside Maxwell term is independent
of U and remains defined for actual vacuum and radiation. The constant
surface tension sigma>=0 is an additional postulate; its rest energy is
sigma times area and must be counted. There is no surface charge or current
in (7). Bulk sources lie inside and are counted separately.

Gauge variation gives continuity of normal D and tangential H, while the
Bianchi equation gives continuity of normal B and tangential E. In a static
spherical pure-electric interface of radius R this reduces to

\[
 D_b=D_{\rm in}=D_{\rm out}=Q/(4\pi R^2),\quad
 E_{\rm in}=D_b/(1-D_b/D_0),\quad E_{\rm out}=D_b.       \tag{8}
\]

Normal interface displacement gives the reciprocal normal stress balance.
In the static flat-space spherical limit it is

\[
 P_b-H_{\rm in}(D_b)+H_{\rm out}(D_b)=2\sigma/R,        \tag{9}
\]

where H_in=E D-Le and H_out=D^2/2. The signs can be checked without stress
conventions: at fixed enclosed charge, changing R differentiates field energy
by 4 pi R^2(H_in-H_out), matter energy by -4 pi R^2 P_b, and wall energy
by 8 pi sigma R. Setting their sum to zero gives (9).

For the retained law,

\[
 L_e=D_0 E-D_0^2\log(1+E/D_0),\quad
 H_{\rm in}=D_0^2[-x-\log(1-x)],\quad
 H_{\rm in}-H_{\rm out}
 =D_0^2[-x-\log(1-x)-x^2/2]>0\quad(0<x<1).             \tag{10}
\]

The last sign follows from derivative x^2/(1-x)>0 and zero value at x=0.
A zero-pressure edge therefore cannot satisfy this no-surface-charge,
nonnegative-tension matching. A **positive-density, positive-pressure sharp
edge** can; this bypasses the earlier smooth zero-density taper obstruction
by changing both its domain and exterior law, with explicit surface work.

An exact local algebraic witness takes D0=c=rho_b=1, x_b=1/2, sigma=0,
Gamma=6/5, P_b=log(2)-5/8>0, and K=P_b/rho_b^(6/5).
Then E_in=1, E_out=1/2 and (9) holds. The full polytropic EOS gives

\[
 h_{\rm eff}=\rho_b+24P_b/5>1>h_c=1/2,
\]

so this surface state also lies inside W_1 and admits (4). Positive sigma
simply adds 2 sigma/R to the required pressure, increasing h_eff for this
assigned EOS. This witness verifies local state and traction compatibility;
it is **not** a global hydrostatic solution, a radial interface stability
result, or a derivation of K, sigma, the phase boundary or charged core.
The exterior electric energy is finite, 2 pi D_b^2 R^3. Gauge and mechanical
matching are now consequences of one specified action, rather than assigned
unreciprocated boundary forces.

Equation (7) changes the model. The material-density jump, selected phase
domain, permeability and optional wall stock are inputs. Gravity adds the
appropriate metric and junction equations and the wall's gravitational mass;
none is solved here. A moving-wall spectrum can overturn stability even when
both bulk principal cones pass. The prior movable-boundary counterexample
is consequently still relevant.

## 5. Executable consequence and audit scope

`check_vacuum.py` checks symbolic numerator/bound identities, explicit
counterlimits, the safe blend estimates, narrowed-domain uniform limit
factors, the Lorentz invariant polarization control, and reciprocal energy
derivatives. A finite rational grid tests the inherited cone with the new
parent beta_*; it does not establish the uniform theorem. The computation
contract, bounded run manifest and source hashes specify the exact evidence.

The actionable next discriminator is a global free-boundary equilibrium
followed by its constrained fluid/gauge/interface Hessian, counting central
and surface sources. The coefficient construction by itself does not settle
that problem. No observational gate, production calculation, full Einstein
solution or universal vacuum completion is claimed.
