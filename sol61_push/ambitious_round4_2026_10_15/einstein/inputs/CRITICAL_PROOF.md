# A dynamical critical charged/baryonic sphere with a moving Maxwell boundary

VC3-CRITICAL-INTERFACE-001, 15 October 2026. An actual joined two-fluid
Newtonian rest-mass-gravity/current-kinetic model: no held central body,
positive critical dark charge, finite baryonic and dark masses, a counted
moving wall, true Maxwell vacuum outside, and positive complete **radial**
quadratic energy. Both static species equations, Gauss and the wall equation
are solved. This is a new high-pressure composite body with chosen EOSs,
surface phase and tension, not the original galaxy law or a full Einstein
theory. Nonspherical health, a wall carrier and production remain open.

## 1. Actual varied species, phase and energy

There are two separately conserved massive currents: ordinary baryons b with
q_b=0, and charged dark matter c with the actual critical charge-to-rest-mass
ratio `q_c/m_c=zeta=sqrt(4piG)>0`. Let rho_a be rest mass density. Both obey
chosen stiff barotropes

\[
 P_a=K_a\rho_a^2,\quad
 \epsilon_a=\rho_a c^2+P_a,\quad
w_a=2K_a\rho_a,\quad H_a=\rho_a c^2+2P_a.
\]

In the Newtonian source and material conservation laws rho_a means lab
rest-density, equal to proper rest-density on the static state. The inherited
current action supplies H_a/c^2 for its quadratic kinetic coefficient. This
is the explicitly defined hybrid convention, not a covariant gravity claim.

The material gauge frame is the varied **dark current** frame U_c. Ordinary
baryons are not included in it. Use the inherited dark current minimal
coupling, the electric law D=E/(1+E/D0), and the smooth occupied-center beta
specified in the pinned vacuum proof. Both species occupy the same finite
ball and meet one impermeable advected wall at R. Their radial boundary
displacements equal the wall displacement. There is no interspecies
conversion, material flux, surface charge or uncounted pressure reservoir.
Outside R is the frame-independent Maxwell action and no matter.

Newtonian gravity is sourced by both rest densities and the wall's entire
rest mass. Internal, gauge and kinetic energies do not source Poisson's
equation in this defined hybrid. The fluid kinetic coefficients are the
actual current values H_a/c^2, not bare rho_a. Radial velocity is parallel
to E and adds no constitutive transverse boost energy.

The wall has constant tension sigma>0, area energy 4pi sigma R^2, rest mass
`m_w=4pi sigma R^2/c^2` and positive quadratic inertia m_w. These are the
small-velocity terms of an area action. With separately conserved total
masses M_b,M_c, its complete Newtonian gravitational contribution is

\[
 V_w=4\pi\sigma R^2
 -\frac{4\pi G\sigma(M_b+M_c)R}{c^2}
 -\frac{8\pi^2G\sigma^2R^3}{c^4}.                       \tag{1}
\]

The second and third terms are wall/matter and wall self-gravity. The wall's
interior potential is spatially constant, so these terms do not change bulk
hydrostatic gradients. Their work when R moves is retained.

The potential energy is the two internal energies, the full Newtonian
self/cross energy of rho_b+rho_c, the Gauss-constrained electric Hamiltonian
inside and outside the phase boundary, and (1). The corresponding current
actions, common impermeability constraints, gauge actions and area wall
give a reciprocal variational model. This does not assert a relativistic
metric or relativistic wall-gravity junction.

## 2. The actual finite-ball two-fluid equilibrium

At a co-moving static electric state the first varied dark-frame term
vanishes; it has not been removed by freezing U. All first beta B^2
variations also vanish. Thus the exact rest-mass comparison equations are

\[
 m_a'=4\pi r^2\rho_a,\quad
 g=G(m_b+m_c)/r^2,\quad D=\zeta m_c/(4\pi r^2),\quad
 E=D/(1-D/D_0),                                      \tag{2}
\]

\[
 w_b'=-g,\qquad w_c'=-g+\zeta E,
 \quad m_a(0)=0,\quad w_a(0)=2K_a\rho_{a0}.            \tag{3}
\]

At critical charge zeta E=Gm_c/[r^2(1-x)], x=D/D0. Therefore define the
finite-ball enthalpy maps

\[
 T_b=w_{b0}-G\int_0^r\frac{m_b+m_c}{s^2}ds,
\]

\[
 T_c=w_{c0}-G\int_0^r\frac{m_b}{s^2}ds
       +G\int_0^r\frac{m_c x}{(1-x)s^2}ds,\qquad
 m_a(s)=4\pi\int_0^s z^2\frac{w_a(z)}{2K_a}dz.         \tag{4}
\]

Choose the following assigned dimensionally consistent scales:

```
R=D0=rho_b0=1, c=100, G=1/100000000,
rho_c0=f=1341/250, Kc=1/100, Kb=f(1+f)/100.
```

These EOS constants, density ratio, phase and wall are inputs. The total
mass ratio is an output close to f, not an exactly imposed cosmological
abundance or a production result.

Use the closed box `.99*w_a0<=w_a<=w_a0` in the relative sup norm
`||dw||=max_a sup |dw_a|/w_a0`. With pi<4, zeta<1/2500. Every state in
this box has

\[
 x\le\frac{\zeta\rho_{c0}R}{3D_0}
 <\frac f{7500}<X:=1/1000.                            \tag{5}
\]

Also `.99*rho_b0>rho_c0*X/(1-X)`. Hence the bracket in the dark inward
force stays positive and both maps decrease from their central values.
Their maximal drops are bounded respectively by

\[
 B_b=\frac83G(1+f),\qquad B_c=\frac83G,
\]

strictly below `.01*w_b0` and `.01*w_c0`. Thus (4) maps the box into itself.
For a perturbation of its argument, `|dm_a(s)|<=4pi rho_a0 s^3||dw||/3`.
The derivative of `m_c*x/(1-x)` with respect to m_c is `(1-x)^-2-1`.
The two normalized Lipschitz bounds are consequently

\[
 q_b\le\frac{8G(1+f)}{3w_{b0}},\qquad
 q_c\le\frac{8G[1+f((1-X)^{-2}-1)]}{3w_{c0}},
 \quad \max(q_b,q_c)<10^{-6}.                         \tag{6}
\]

The maps therefore have an actual unique common fixed point in this box,
obtained by convergent successive iteration. The integral equations give
regular center limits m_a=O(r^3), g,D=O(r). Both densities are positive
throughout the finite ball, with their own hydrostatic equations satisfied.
In particular

\[
 \rho_a\ge.99\rho_{a0},\quad
 P_a\ge(.99)^2P_{a0}>\frac{49}{50}P_{a0},\quad
 M_b+M_c<\frac{16}{3}(1+f).                            \tag{7}
\]

No field profile or central species is held fixed in this construction.

## 3. True Maxwell vacuum and a counted moving wall

There is no surface charge: D is continuous and its exterior is
`D(r)=zeta M_c/(4pi r^2)`. The interior electric Hamiltonian jump over
Maxwell is

\[
 \Delta H=D_0^2[-x-\log(1-x)-x^2/2],\quad
 0<\Delta H<\frac{D_0^2x^3}{3(1-x)},\quad
 \Delta H_D=E-D.                                     \tag{8}
\]

For the actual boundary D_b supplied by (2), (5) bounds Delta H below 10^-9.
Varying the common material radius at fixed M_b,M_c and sigma yields

\[
 P_b(R)+P_c(R)=P_{\rm ext}(R)
 =\Delta H(D_b)+\frac{2\sigma}R
 -\frac{G\sigma(M_b+M_c)}{c^2R^2}
 -\frac{6\pi G\sigma^2}{c^4}.                         \tag{9}
\]

This includes the wall's rest mass and every wall gravitational work term.
Set `P0=P_b0+P_c0`. The quadratic
`A sigma-B sigma^2=P_b(R)+P_c(R)-Delta H`,
`A=2/R-G(M_b+M_c)/(c^2R^2)`, `B=6piG/c^4`, has a unique weak positive
root below `sigma_test=51P0R/100`: its load is positive by (7)--(8), and
at sigma_test the quadratic exceeds P0 on its increasing branch. These are
strict rational bounds for the assigned scales. Choose that root once and
hold sigma fixed under perturbations.

This is an actual global two-fluid/wall equilibrium and an actual exterior
Maxwell vacuum. Both matter masses, charge `zeta M_c`, wall rest energy,
wall gravity and finite electric energy are counted. Source formation and
wall microphysics are not derived. Positive boundary densities and the
change of exterior phase avoid the old smooth zero-density taper premise.

## 4. Independently derived coupled radial operator and full energy

Let xi_b,xi_c be regular radial material displacements, and
`d_a=xi_a'+2xi_a/r`. The boundary constraints are
`xi_b(R)=xi_c(R)=xi_R`; both species are separately impermeable there.
The interior density perturbations and field perturbations are

\[
 \delta\rho_a=-\rho_a d_a-\xi_a\rho_a',\quad
 \delta P_a=-2P_a d_a-\xi_a P_a',
\]

\[
 \delta g=-4\pi G(\rho_b\xi_b+\rho_c\xi_c),\quad
 \delta D=-\zeta\rho_c\xi_c,\quad
 \delta E=H''\delta D,\quad H''=(1-x)^{-2}.             \tag{10}
\]

Do not omit the background gravitational density force. Linearized species
momentum is

\[
 (H_b/c^2)\ddot\xi_b=-(\delta P_b)'-g\delta\rho_b-\rho_b\delta g,
\]

\[
 (H_c/c^2)\ddot\xi_c=-(\delta P_c)'-(g-\zeta E)\delta\rho_c
                         -\rho_c\delta g+\zeta\rho_c\delta E.
\]

Using g'=4piG(rho_b+rho_c)-2g/r and
`E'=H''(zeta rho_c-2D/r)` gives the exact symmetric radial equations

\[
 (H_b/c^2)\ddot\xi_b=(2P_b d_b)'+4\rho_bg\xi_b/r
                   -4\pi G\rho_b\rho_c(\xi_b-\xi_c),
\]

\[
 (H_c/c^2)\ddot\xi_c=(2P_c d_c)'+4\rho_cg\xi_c/r
 -4\pi G\rho_b\rho_c(\xi_c-\xi_b)
 -2\zeta\rho_c(E+H''D)\xi_c/r.                       \tag{11}
\]

The apparently dangerous local charged-density electric term cancels against
the background electric gradient, leaving the last **positive restoring**
term in the energy below. The mutual-gravity term is the displayed positive
relative-displacement square; it is not guessed from a frozen-core theorem.

At the moving boundary, the interior Lagrangian field variation is
`Delta D=delta D+xi_R D'=-2D_b xi_R/R`, equal to the exterior variation.
Thus the charged finite-density edge adds no omitted independent surface
charge term. The summed material/wall boundary equation is

\[
 -[2P_b d_b+2P_c d_c]_R=P_{\rm ext}'(R)\xi_R
                                  +\sigma\ddot\xi_R/c^2,
\]

\[
 P_{\rm ext}'=-2D_b(E_b-D_b)/R-2\sigma/R^2
                 +2G\sigma(M_b+M_c)/(c^2R^3).          \tag{12}
\]

Integrating (11) with (12) gives the conserved potential form

\[
 \begin{split}
 Q/(4\pi)={}&\sum_a\int_0^R2P_a d_a^2r^2dr
 -4\int_0^Rgr(\rho_b\xi_b^2+\rho_c\xi_c^2)dr\\
 &+4\pi G\int_0^R\rho_b\rho_c(\xi_b-\xi_c)^2r^2dr\\
 &+2\zeta\int_0^R\rho_c(E+H''D)r\xi_c^2dr
 +P_{\rm ext}'(R)R^2\xi_R^2,
 \end{split}                                                     \tag{13}
\]

with the full current and wall inertia

\[
 I/(4\pi)=\sum_a\int_0^R(\rho_a+2P_a/c^2)\xi_a^2r^2dr
                             +\sigma R^2\xi_R^2/c^2.   \tag{14}
\]

Both chemical first integrals may be nonzero constants. Their second-order
path terms cancel against the separately conserved M_b,M_c constraints.
The common finite-density moving edge is treated by (12), not by pretending
each Eulerian mass tangent vanishes at the fixed background radius. Equations
(13)--(14) are the constrained quadratic comparison energy for this single
joined model. Monopole Gauss dynamics has no independent radiation mode;
nonspherical gauge/interface modes require a different analysis.

## 5. Positive complete radial form for the actual equilibrium

Put `J_a=integral_0^R d_a^2r^2 dr`. Cauchy and the regular center give

\[
 \int_0^R\xi_a^2r^2dr\le R^2J_a/6,\quad
 \xi_R^2\le(J_b+J_c)/(6R).
\]

Since `g<=Omega^2 r`, `Omega^2=4piG(rho_b0+rho_c0)/3`, discard only the
positive coupling/electric squares and positive last term in (12). Then

\[
 Q/(4\pi)\ge C_bJ_b+C_cJ_c,
\]

\[
 C_a=2P_{a,\min}-\frac23\rho_{a0}\Omega^2R^2
                    -\frac{D_b(E_b-D_b)+\sigma/R}{3}.  \tag{15}
\]

For the assigned scales, use (7), pi<4, x_b<X and sigma<sigma_test. Entirely
rational arithmetic gives

\[
 C_b>14/25=.56,\qquad C_c>9/20=.45.
\]

Thus Q is positive for every nonzero admissible radial two-fluid/wall
displacement, not merely a homology family. The actual current inertia is
also bounded by this norm:

\[
 I/(4\pi)\le\frac16\left[
 R^2\max_a(\rho_{a0}+2P_{a0}/c^2)+\sigma R/c^2\right](J_b+J_c).
\]

The explicit rational bounds give a positive Rayleigh lower bound above 1/2
in the assigned time units. This is a comparison-form statement for suitable
finite-energy radial linear solutions, not a full nonlinear evolution or a
spectral-domain theorem for all sectors of the covariant theory.

## 6. Occupied principal domain and exact remaining implications

For the charged Gamma2 EOS, `H_c(1-s_c^2)=rho_c c^2`. Throughout this actual
interior, that is at least `.99*f*10000`, whereas
`hc=E^2x<=X^3/(1-X)^2<2*10^-9`. The dark-frame principal cone therefore has
a large strict margin; at E=0 use the smooth occupied-center coefficient.
The ordinary baryon sound speed is also below c. At the finite edge the
specified reciprocal action changes to Maxwell and no material frame is
required outside. This local bulk statement does not establish nonspherical
boundary or nonzero-magnetic-background health.

Closed in this chosen hybrid: both dynamical species' global static force
balance, critical dark charge bookkeeping, finite actual masses, reciprocal
Maxwell matching with no held source, wall rest mass and gravity, moving-edge
constraints, and a positive complete radial two-fluid/gauge/wall energy.

Still open: microscopic EOS and wall/phase selection, a covariant metric and
wall junction, all angular/gauge/background sectors, nonlinear free-boundary
evolution, formation and abundance, conversion, galaxy/lensing/cosmological
predictions and empirical gates. The high-pressure wall-supported body does
not reproduce the old pressureless algebraic galaxy law. This result closes
a defined joined mathematical model, not the full physical theory.
