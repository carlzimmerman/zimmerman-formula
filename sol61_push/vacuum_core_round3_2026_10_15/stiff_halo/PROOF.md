# An exact finite stiffness-supported halo is a constrained global energy minimum

VC3-SH-001, 15 October 2026. **A nonrelativistic fixed-baryon construction.**
This supplies an actual compact regular-density halo, the already specified
S2 stiffness, positive counted cold matter and finite inventory, with a
free-support variational inequality. It does not supply a healthy relativistic
vacuum, dynamical baryons, a formation history or a new empirical prediction.
The baryon profile and numerical stiffness below are constructed inputs;
the inventory ratio 5.364 is imposed, not derived.

## Physical model and the stiffness dictionary

Use Newtonian rest-mass gravity, critical dark charge/mass
`q/m=zeta=sqrt(4 pi G)` and instantaneous electrostatics. Let
`P=D/zeta`, `rho=div P>=0`, total cold mass `M`, and a fixed nonnegative
baryon source. The actual cold current j is separately conserved with rho.
Its kinetic energy is `integral |j|^2/(2rho)`, defined as zero at rho=j=0
and infinite if rho=0,j!=0. In particular P is not identified with a particle
velocity and j is not silently equated to -P_dot in nonradial flows.

The electric Hamiltonian for the retained response is

\[
 H(D)=D_0^2[-x-\log(1-x)],\quad x=|D|/D_0,
 \quad D_0=a_0/\zeta.
\]

It is precisely `H(zeta P)=2pi G |P|^2+W(4pi G|P|)`, with the frozen
`4pi G W'(u)=u^2/(a0-u)` and W(0)=0. Critical-charge Coulomb self-energy
cancels the longitudinal Newtonian self-gravity. Eliminating those constraints
leaves the mechanical potential, up to a constant baryon self-energy,

\[
 V[P]=\int\left[{\kappa_G\over2}|P_T|^2+
 W(\kappa_G|P|)+{\gamma\over2}|\nabla P|^2
 -\nabla\Phi_b\cdot P\right]d^3x,\quad \kappa_G=4\pi G.       \tag{1}
\]

Here P_T is the transverse Helmholtz projection. This formula and its actual
current lift are independently derived in `../dynamical_lift/PROOF.md`.
No barotropic dark EOS is added to (1). For fields with the stated decay and
vanishing integration boundary terms,

\[
 \int|\nabla P|^2=\int[(\mathop{\rm div}P)^2+
                         |\mathop{\rm curl}P|^2].               \tag{2}
\]

Thus, in the radial sector, the chosen S2 stiffness supplies the internal
energy `gamma rho^2/2` and pressure `gamma rho^2/2`, exactly a Gamma=2
pressure. It must be counted once. Nonradial transverse/curl energy remains
in (1). This is a Newtonian electrostatic/current completion, not a proof
of the relativistic magnetic or radiative action.

## Exact positive-source example with nonzero stiffness

Set `G=a0=R=1` as units. Inside r<=1 prescribe the cold density

\[
 \rho=\rho_0(1-r^2/10-9r^4/10)
      =\rho_0(1-r^2)(1+9r^2/10),\quad
 \rho_0={105\over776\pi}.
\]

It is finite and positive at the center and positive for 0<=r<1, vanishing
continuously at r=1. Define

\[
 m(r)={r^3(350-21r^2-135r^4)\over1940},\quad
 u={m\over r^2},\quad k=\gamma\rho_0={101\over50958}.
\]

Then m'=4pi r²rho, M=m(1)=1/10 and
`0<=u<=35/194<1/5`; the constitutive pole is avoided. Choose

\[
 g_b(r)={u^2\over1-u}+k(r/5+18r^3/5),\qquad
 M_b(r)=r^2g_b(r)\quad (r\le1).                          \tag{3}
\]

Outside set m=M and Mb=Mb(1), so both material sources are compact. The
baryon field is continuous at the edge. The source is an inverse construction
chosen to demonstrate existence, not a profile inferred from observations.
It is nevertheless a real nonnegative finite mass density: direct algebra
makes

\[
 q(r)={(1-u)^2\over r^2}M_b'(r)
\]

a degree-fourteen rational polynomial. The exact checker expands it in the
Bernstein basis of degree fourteen on [0,1]; **all fifteen coefficients are
positive, with minimum 101/84930**. Since this basis is nonnegative and sums
to one, q>=101/84930 throughout that entire interval. Consequently

\[
 \rho_b={M_b'\over4\pi r^2}
 ={q(r)\over4\pi(1-u)^2}>0\quad(0\le r\le1).
\]

The origin is understood by its finite limit. This is an exact polynomial
positivity certificate, not a sampled grid. A source-density jump to zero
outside is allowed; no baryonic dynamics is inferred from this fixed source.
The constants give

\[
 M_b(1)={25\over1341},\qquad {M\over M_b}={1341\over250}=5.364,
 \quad \gamma={39188\pi\over2675295},\quad
 {L_*^2\over R^2}={\gamma\over2\pi}={19594\over2675295}.       \tag{4}
\]

The last relation uses the same frozen `gamma=kappa_G Lstar^2/2`.
Equations (3)--(4) choose the source and stiffness consistently with an
assigned inventory; they do not derive that inventory or Lstar.

## Interior Euler equation and the outside inequality

In spherical symmetry the stiffness pressure/current equation from (1) is

\[
 \gamma\rho'={u^2\over1-u}-g_b=:F(r).                    \tag{5}
\]

Equation (3) makes it hold identically at every occupied radius. At the
origin m=O(r³), P=O(r), and rho is finite. At the edge P and its radial
first derivative are continuous because rho approaches zero; rho' has a
finite jump. There is no spurious delta source in div P. Empty exterior
space has nonzero electrostatic flux `P=M rhat/(4pi r²)`.

The physical density constraint changes the empty-region Euler condition:
one must not impose force balance on nonexistent particles. Define

\[
 \psi(r)=\int_r^\infty F(s)ds,\qquad
 \lambda(r)=\psi(r)+\gamma\rho(r).
\]

It follows from (5) that lambda is constant, say mu, throughout the occupied
ball. Outside,

\[
 r^2F(r)={M^2\over r^2-M}-M_b,\qquad
 F(1)=-{101\over13410}<0,
\]

and the displayed right side is strictly decreasing for r>=1. Therefore
`F<0` outside, `lambda'=-F>0`, `lambda>=mu`, and lambda tends to zero
at infinity. In particular mu<0. These statements establish the required
outside variational inequality, not only the interior Euler equation.
This is the explicit finite-gamma step missing from a hypothetical
'if an equilibrium exists' stability statement.

## Global constrained minimum, including nonradial support changes

Take any admissible P with div P=rho>=0, the same finite mass M,
`kappa_G|P|<a0` almost everywhere, finite energy and boundary behavior allowing
the integrations above. Do not restrict its support or angular dependence.
For the radial candidate P0, the first derivative of (1) is

\[
 V'[P_0]=-\nabla\lambda.
\]

The transverse projection contributes zero there. The radial identities
`Delta P0=grad rho0` and (5) give the stated derivative also across the edge
in the weak sense. Pairing it with P-P0 and integrating by parts gives

\[
 \langle V'[P_0],P-P_0\rangle
 =\int\lambda(\rho-\rho_0)
 =\int(\lambda-\mu)\rho\ge0.                            \tag{6}
\]

The second equality uses fixed total mass and lambda=mu wherever rho0>0.
The last inequality follows from the outside condition just proved.

For `0<u<1`, the W Hessian eigenvalues have signs fixed by

\[
 4\pi W''(u)={u(2-u)\over(1-u)^2}>0,\qquad
 4\pi {W'(u)\over u}={u\over1-u}>0.
\]

W(|P|), the transverse square and the gradient square are convex, while the
baryon term is linear. The cone `rho>=0`, the field cap and fixed mass are
convex admissibility conditions. Thus (6) proves **V[P]>=V[P0] globally on
this class**, with uniqueness of the field under the finite-energy/decay
conditions. The positive gamma gradient term supplies strictness for a
nonzero field difference; constant differences are excluded by decay.

More precisely the energy difference is the sum of the nonnegative
outside term in (6), the W Bregman remainder, the transverse quadratic
remainder and `gamma/2 integral |grad(P-P0)|²`. Adding the positive kinetic
perspective `integral |j|²/(2rho)` gives a global mechanical relative-energy
bound, including variations that move the cold support boundary. It is not
merely a successful finite set of radial trial functions. Conservation and
energy stability are conditional on a sufficiently regular solution of the
defined Newtonian current dynamics; no global smooth evolution, damping,
formation basin or attractor theorem is supplied.

## Limits and independent evidence

The outside nonlinear electrostatic energy is defined without a material U
in this Newtonian Hamiltonian. It is not a submetric Lorentz vacuum or a
propagating radiation completion; `../lorentz/PROOF.md` shows why retaining
this law in a minimal Lorentz vacuum fails the requested metric cone. The
old occupied-medium hcrit gate cannot be applied through the vanishing
matter edge and pronounced healthy by this mechanical result.

Baryons remain fixed, the source profile is constructed, and stiffness and
inventory are chosen constants. The example is a finite-stock constructive
witness in a specified dynamical lift of S2 with physical positive-density
constraints, not a solution of the unconstrained S2 field variation in empty
space, a derivation of microphysics or a new galaxy fit. It closes the stated
nonrelativistic finite-halo existence/energy problem for one explicit member;
the full theory and its cosmological/metric/production obligations remain open.

`check_stiff_halo.py` checks all coefficients, forces, inventory, boundary
conditions and the exact fifteen-coefficient source certificate. The
analytic convexity and variational inequality establish the uniform energy
claim. Source snapshots, resource limits, code hashes and raw results are
recorded in the manifest. Independent review must check (6) and the scope
of the current/electrostatic lift, not only the polynomial arithmetic.
