# A global finite neutral sphere with a moving Maxwell interface: fixed-core radial control

VC3-INTERFACE-001, 15 October 2026. This is a new specified Newtonian hybrid
control, not the original halo or a complete dynamical charged-core theory.
It supplies an actual global finite-mass equilibrium, a frame-free Maxwell
vacuum outside a material edge, counted surface energy and gravity, and a
positive interface-inclusive radial quadratic energy. Its central charged
body is prescribed and held. Its EOS, core, phase and surface tension are
inputs. Nonradial health and a physical surface carrier are not established.

The proof uses existence bounds rather than promoting a sampled ODE profile
to an exact solution. Copies of all inherited inputs are in `inputs/`.

## 1. Model and all counted stocks

Use c>0, spherical radius R, a conserved neutral material mass density rho,
and P=K rho^(6/5), K>0. Its Newtonian specific enthalpy is

\[
 w=6K\rho^{1/5},\quad c_N^2=w/5,\quad u=5K\rho^{6/5}.
\]

A fixed uniform central body has mass Mc>0, radius Rc<R, and enclosed mass
Mc(r)=Mc min[(r/Rc)^3,1]. It has a fixed uniform charge density on the same
ball, total charge Q=4 pi D_b R^2. This source is prescribed, not varied or
declared dynamically supported; source mechanical support is unresolved.
Its mass and charge enter the following equations separately.

The occupied region 0<=r<R contains the neutral current defining U. Use the
inherited electric law D=E/(1+E/D0), D0>0, and the smooth occupied-center
magnetic response in `../vacuum/PROOF.md`, restricted to its admitted cone
domain. The exterior r>R has the frame-independent Maxwell action. It
contains no matter or external charge: the prescribed body lies inside Rc.
The current is impermeable at the moving material boundary. There is no
surface charge, current or uncounted pressure reservoir. Purely spherical
motion produces no magnetic field; Gauss fixes D at every radius:

\[
 D(r)=\begin{cases}D_b R^2r/R_c^3&r\le R_c,\\
                   D_b R^2/r^2&r\ge R_c.\end{cases}       \tag{1}
\]

In (1), Q/(4 pi)=D_b R^2 is held fixed when the boundary moves; D_b denotes
its background value. Radial fluid velocity is parallel to E, so the varied
material frame adds no transverse boost energy in this sector.

The wall has constant tension sigma>0, rest energy 4 pi sigma R^2, rest mass
m_w(R)=4 pi sigma R^2/c^2, and positive quadratic radial inertia m_w. These
are the small-velocity terms of an area action. The chosen Newtonian model
also couples this entire rest mass to Poisson gravity. Gauge-field, internal
and kinetic energies do not source Poisson gravity in this truncation.
This rest-mass gravitational convention is explicit; no Einstein equation or
relativistic wall-gravity junction is claimed.

After eliminating the Newtonian potential, the conserved potential energy is

\[
 \mathcal E=\int_0^R4\pi r^2[u(\rho)+\rho\Phi_c]dr
             +W_{ss}+E_A(R)+V_w(R),\qquad
 W_{ss}=-\frac G2\iint\frac{\rho(x)\rho(y)}{|x-y|}dxdy,
                                                               \tag{2}
\]

where E_A is the occupied electric Hamiltonian integrated inside R and the
Maxwell electric Hamiltonian outside R. The finite central body's constant
self energy may be added without affecting variations. The wall contribution
includes its energy, its interaction with every interior rest mass and its
own shell self-gravity:

\[
 V_w=4\pi\sigma R^2
       -\frac{Gm_w(M_c+M_s)}R-\frac{Gm_w^2}{2R}
 =4\pi\sigma R^2-
   \frac{4\pi G\sigma(M_c+M_s)R}{c^2}
   -\frac{8\pi^2G\sigma^2R^3}{c^4}.                    \tag{3}
\]

Here Ms is the conserved total neutral rest mass, fixed during perturbations.
The shell theorem makes wall gravity constant throughout the interior, so it
does not change neutral hydrostatic gradients. Its work when R moves is
retained in (3). Together with fluid kinetic energy, wall kinetic energy
`m_w dot R^2/2`, fixed-source coupling and the stated gauge actions, (2)--(3)
define a reciprocal Newtonian variational control. Higher velocity and
post-Newtonian terms have not been added.

## 2. An actual self-gravitating neutral equilibrium on a finite ball

Fix a central density rho0 and set w0=6K rho0^(1/5). For 0<=r<=R solve

\[
 m_s'=4\pi r^2(w/6K)^5,\quad
 w'=-G[M_c(r)+m_s(r)]/r^2,\quad m_s(0)=0,\quad w(0)=w_0.
                                                               \tag{4}
\]

This includes neutral self-gravity, not merely an assigned support profile.
On the sup-norm interval `(1-epsilon)w0<=w<=w0`, the integral map

\[
 T[w](r)=w_0-G\int_0^r\frac{M_c(s)
                  +4\pi\int_0^s z^2[w(z)/(6K)]^5dz}{s^2}ds
                                                               \tag{5}
\]

maps the interval into itself provided

\[
 B_0:=G\left[\frac{M_c}{R_c}(3/2-R_c/R)
                        +\frac{2\pi\rho_0R^2}3\right]
 \le\epsilon w_0.                                     \tag{6}
\]

The central-source integral is finite and evaluated exactly. Since
`d rho/dw<=5rho0/w0`, the map's Lipschitz constant is at most

\[
 q=\frac{10\pi G\rho_0R^2}{3w_0}.                    \tag{7}
\]

For q<1 the successive maps converge uniformly to a unique solution in this
interval, with error bounded by the geometric series. Equation (5) then
gives the derivatives in (4), with the regular r=0 limits. The background is
positive, has finite mass and has positive boundary pressure Pb. For the first
iterate w1=T[w0], `||w-w1||<=q B0/(1-q)`. This is a constructive existence
and error bound, not a numerical shooting assumption.

## 3. The exact moving-wall equilibrium condition

Let x=D_b/D0 in (0,1). The no-surface-charge Maxwell matching has D continuous
and E_in=D_b/(1-x), E_out=D_b. Its electric energy-density jump is

\[
 \Delta H=D_0^2[-x-\log(1-x)-x^2/2]>0,
 \qquad \frac{d\Delta H}{dD}=E_{\rm in}-D.              \tag{8}
\]

For fixed Q and both conserved rest masses, varying R in (2) gives

\[
 P_b=P_{\rm ext}(R):=\Delta H(D_b)+\frac{V_w'(R)}{4\pi R^2}
 =\Delta H+\frac{2\sigma}R
  -\frac{G\sigma(M_c+M_s)}{c^2R^2}
  -\frac{6\pi G\sigma^2}{c^4}.                       \tag{9}
\]

All surface, electric and gravitational work is retained. In particular,
adding the wall mass to an inventory but omitting its gravitational work
would give a different boundary equation. A weak positive root sigma exists
if Pb>Delta H and the quadratic `A sigma-B sigma^2=Pb-Delta H`,
`A=2/R-G(Mc+Ms)/(c^2R^2)`, `B=6piG/c^4`, crosses this load on its increasing
branch. The root is `2(Pb-Delta H)/(A+sqrt(A^2-4B(Pb-Delta H)))`.
After this root is chosen, sigma is held fixed throughout perturbations.

## 4. Full radial energy, including neutral self-gravity and the moving wall

Let xi(r,t) be a regular radial material displacement, xi=O(r) at zero,
and define d=xi'+2xi/r. Conservation gives
`delta rho=-rho*d-xi*rho'`, `delta P=-Gamma*P*d-xi*P'`, with Gamma=6/5.
Interior shell gravity has zero gradient, while the central body is fixed.
Linearized neutral self-gravity satisfies `delta g_s=-4piG rho xi`.
Direct substitution in the Euler equation gives

\[
 \rho\ddot\xi=(\Gamma P d)'
             +\rho[4g/r-4\pi G\rho_c(r)]\xi,
 \quad g=G[M_c(r)+m_s(r)]/r^2.                         \tag{10}
\]

Both the gravitational density term and delta g_s have been included. Wall
inertia makes the linear boundary condition

\[
 -\Gamma P_b d(R)=P_{\rm ext}'(R)\xi(R)
                           +\frac\sigma{c^2}\ddot\xi(R).
                                                               \tag{11}
\]

For a harmonic mode its conserved radial quadratic form and inertia are

\[
 \frac Q{4\pi}=\int_0^R\Gamma P d^2r^2dr
 -\int_0^R\rho[4gr-4\pi G\rho_c r^2]\xi^2dr
 +P_{\rm ext}'(R)R^2\xi(R)^2,                         \tag{12}
\]

\[
 \frac I{4\pi}=\int_0^R\rho\xi^2r^2dr
                       +\frac{\sigma R^2}{c^2}\xi(R)^2.
                                                               \tag{13}
\]

The derivative holds Q, Mc, Ms and sigma fixed. It is

\[
 P_{\rm ext}'=-\frac{2D_b(E_{\rm in}-D_b)}R
              -\frac{2\sigma}{R^2}
              +\frac{2G\sigma(M_c+M_s)}{c^2R^3}.       \tag{14}
\]

The wall self-gravity term in P_ext is constant in R and has zero derivative.
The positive wall inertia must be placed in I; omitting it would change the
moving-boundary eigenproblem. Equations (12)--(14) also follow by second
variation of (2) on mass-preserving material paths.

No spherical gauge degree of freedom has been discarded: fixed Gauss charge
fixes D, spherical B is zero, and all electric variation is the explicitly
included phase-boundary work. Nonspherical electromagnetic waves and coupled
interface perturbations require an additional analysis.

## 5. A uniform sufficient bound and an explicit global example

Write `J=integral_0^R d^2 r^2 dr`. Regularity and Cauchy give

\[
 \xi(R)^2\le J/(3R),\qquad
 \int_0^R\xi^2r^2dr\le R^2J/6.                       \tag{15}
\]

For the uniform compact core, g<=Omega^2 r with
`Omega^2=G[Mc/Rc^3+4pi rho0/3]`. Drop the positive rho_c term in (12) and the
positive last term in (14). Since rho<=rho0 and P>=Pmin, one obtains

\[
 \frac Q{4\pi}\ge C J,\quad
 C=\Gamma P_{\min}-\frac23\rho_0\Omega^2R^2
              -\frac{2D_b(E_{\rm in}-D_b)+2\sigma/R}{3}.
                                                               \tag{16}
\]

Thus C>0 certifies the entire radial fluid/interface form, not a few chosen
homology vectors. It controls radial inertia as well:

\[
 I/(4\pi)\le[\rho_0R^2/6+\sigma R/(3c^2)]J.           \tag{17}
\]

Choose the following dimensionally consistent assigned units and parameters:

```
c=R=rho0=D0=1,  Gamma=6/5, K=1/100, G=1/1000000,
Mc=1/1000, Rc=1/2, Db=1/1000.
```

These are input scales, not a derivation of particle properties or cosmic
abundance. Then w0=3/50. Elementary pi<4 bounds give

\[
 B_0<10^{-6}(1/500+8/3)<w_0/100,\quad q<1/4500.
\]

Take epsilon=1/100. The actual solution has
`rho>=rho0*(99/100)^5` and
`Pmin>=P0*(99/100)^6>=47P0/50=47/5000`.
The total interior mass satisfies `Mc+Ms<16003/3000`. The electric load obeys
`0<Delta H<Db^3/[3(1-Db)]<10^-9`, far below Pb.
At the test tension `sigma_test=51/10000`,

\[
 A\sigma_{\rm test}-B\sigma_{\rm test}^2>P_0\ge P_b-\Delta H,
 \qquad A-2B\sigma_{\rm test}>0.
\]

Hence the actual wall equation has a unique weak positive root below .0051.
Its rest mass is below .0816 in these units; its gravitational terms have
already been included. The root is defined by the actual contracted profile,
not by substituting a homogeneous surrogate for that profile.

Finally the following entirely rational lower bound follows from (16):

\[
 C>\frac65\frac{47}{5000}
 -\frac{4006}{1125\cdot10^6}
 -\frac13\left[\frac2{999\cdot10^6}+\frac{51}{5000}\right]
 >\frac{39}{5000}>0.                                  \tag{18}
\]

This proves actual self-gravitating background existence and positive full
radial fluid/interface energy for the specified fixed-core hybrid model.
The wall and electric boundary are allowed to move, and neither is replaced
by an uncounted prescribed-pressure reservoir. A zero-tension interface is
a different problem and is not certified by this estimate.

For completeness the occupied principal gate is also available. The maximum
x occurs at Rc and is 1/250. Thus
`hc<=1/(250*249^2)`, while the relativistic EOS effective inertia is
`rho+24P/5>=rho>19/20`. There is a large strict h>hc margin everywhere inside.
At the electric origin use the explicitly smooth occupied-center coefficient;
at the finite edge the action changes to Maxwell. This does not assert health
on arbitrary magnetic backgrounds or for nonspherical interface modes.

## 6. What has and has not been closed

Closed in this defined control: regular finite-ball hydrostatic existence,
neutral self-gravity, finite counted interior and surface stocks, true Maxwell
vacuum outside the surface, reciprocal static traction, moving wall inertia,
wall gravitational work, and positive all-radial fluid/interface energy.

Open: the held central charged body's dynamical force balance and perturbation
energy; the wall carrier and its production, tension and permeability; all
nonspherical coupled modes; a smooth transition microphysics; a relativistic
metric completion; formation, abundance and empirical predictions. These new
inputs must not be presented as parameter-free deductions or as completion of
the original theory. This control gives a concrete reciprocal surface model
against which those missing physical mechanisms can be tested.
