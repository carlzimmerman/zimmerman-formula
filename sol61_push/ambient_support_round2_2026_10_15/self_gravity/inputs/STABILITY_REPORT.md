# Radial stability is conditional on the inner support

AS2-STABILITY-001, 15 October 2026. Independent derivation for the ambient-support
round. Analytic proof and counterexample; no numerical spectrum is used.

**Normalized claim and verdict: correct only after a stated restriction.** A
neutral polytropic atmosphere outside a *fixed impermeable* inner radius is
radially stable at the quadratic-energy level in a prescribed attractive
central potential. A quantitative small-self-gravity condition preserves that
statement for an actual self-consistent equilibrium. It is false that the same
atmosphere is stable independently of its inner support: a moving inner surface
against constant prescribed pressure has an explicit negative-energy radial
direction. These are Newtonian barotropic fluid statements, not a stability
theorem for the coupled current-frame gauge medium.

## 1. Object, hypotheses, and evidence boundary

Write `R=R0>0`, `mu_c=G M0>0`, and use the gas mass density `rho`, not the
charge-weighted density or the material number density of the gauge action.
The gas is neutral, has no direct background electric body force in the
restricted test, and obeys

\[
 P=K\rho^\gamma,\qquad K>0,\qquad
 \gamma=1+1/n,\qquad 3<n\leq6.
\]

The perturbations are isentropic with this same EOS (`delta P=c_s^2 delta rho`).
Entropy gradients, relative currents, frame-dependent constitutive forces,
magnetic perturbations, and motion of the central source are excluded. The
unperturbed potential is `Phi_c=-mu_c/r`, with zero at infinity. With

\[
 h(\rho)=\int_0^\rho {P'(s)\over s}\,ds
       =(n+1)K\rho^{1/n},\qquad
 c_s^2={dP\over d\rho}=h/n,
\]

the infinite-tail hydrostatic state has

\[
 h_0={\mu_c\over r},\qquad
 \rho_0=A r^{-n},\qquad
 A=\left[{\mu_c\over(n+1)K}\right]^n,
 \qquad M_s={4\pi A R^{3-n}\over n-3}.
\]

It has finite mass for `n>3`; internal and central-potential energies converge
for `n>2`. Its pressure at `R` is strictly positive. Hence its inner boundary
cannot be a gas-vacuum free surface. A wall, another fluid, or a derived
transition region is an additional physical ingredient.

The pinned current-frame sources establish why ambient support was proposed:
`MC_BOUNDARY_PROOF.md`, “Quantified alternatives,” item 2, explicitly lists retained ambient inertia as
a way to violate the vanishing-enthalpy premise of the charged-edge obstruction.
`RTM_REPORT.md`, Sections 3--4, explicitly does not certify lower-derivative
gravitational terms by its principal wave calculation. No theorem or operator
from the unrelated AG1 `A/r^2` fluid is imported here. These source statements
motivate the object; the stability proof below is reconstructed from Euler and
Poisson equations.

## 2. Fixed central potential: a direct energy proof

Let the domain `Omega={r>=R}` be fixed, with no normal fluid velocity at `R`
and no energy or mass flux at infinity. Set

\[
 u(\rho)={K\over\gamma-1}\rho^\gamma,\qquad
 E[\rho,v]=\int_\Omega\left[
 {1\over2}\rho|v|^2+u(\rho)+\rho\Phi_c\right]d^3x.
\]

Then `u'=h`, `u''=c_s^2/rho>0`, and `h_0+Phi_c=0`. Consequently the *exact*
relative energy is

\[
 E[\rho,v]-E[\rho_0,0]
 =\int_\Omega\left[{1\over2}\rho|v|^2+
 u(\rho)-u(\rho_0)-u'(\rho_0)(\rho-\rho_0)\right]d^3x\geq0.
\]

Equality requires zero velocity and the same density almost everywhere. This
identity requires the displayed integrals to exist; for dynamical conservation
it also requires a sufficiently regular Euler solution and the stated flux
conditions. It does not prove global smooth existence or prevent shocks.

The density Hessian is therefore

\[
 Q_U=\int_\Omega {c_s^2\over\rho_0}(\delta\rho)^2d^3x>0
 \quad\text{for nonzero density perturbations}.
\]

The familiar `gamma<4/3` slogan alone does not refute this state: the central
potential is prescribed, and a fixed inner wall changes the admissible
variations and their work. The usual isolated self-gravitating stellar scaling
argument cannot be transferred without those hypotheses.

## 3. Radial operator with the gravitational density term retained

For radial material displacement `xi(r,t)`, let

\[
 D=\xi'+2\xi/r,\qquad
 \Delta\rho=-\rho D,\quad
 \delta\rho=-\rho D-\xi\rho',\qquad
 \delta P=-\gamma P D-\xi P'.
\]

For either prescribed central gravity or the central-plus-self-gravitating
equilibrium, write `g=Phi_0'>0`, `P'=-rho g`. Linearized momentum is

\[
 \rho\ddot\xi=-(\delta P)'-g\,\delta\rho-\rho\,\delta g.
 \tag{1}
\]

In particular, `-g delta rho` is present. Substitution, before using Poisson,
gives

\[
 \rho\ddot\xi=(\gamma P D)'
       +\rho(2g/r-g')\xi-\rho\delta g.
 \tag{2}
\]

For prescribed central gravity, `g'= -2g/r`, `delta g=0`. For self-gravity
with fixed gas inner wall,

\[
 \delta m=-4\pi r^2\rho\xi,\quad
 \delta g=G\delta m/r^2=-4\pi G\rho\xi,\quad
 g'=4\pi G\rho-2g/r.
\]

Both cases thus yield the radial displacement equation

\[
 \boxed{\rho\ddot\xi=(\gamma P D)'+4\rho g\xi/r.}
 \tag{3}
\]

The cancellation in the self-gravitating case uses both the background
Poisson term and the perturbed gravitational force. Omitting either the
`-g delta rho` term or the perturbed self-force changes the test.

Suppressing an overall `4 pi`, the integrated normal-mode identity is

\[
 \omega^2\int_R^\infty\rho\xi^2r^2dr
 =\int_R^\infty\gamma P D^2r^2dr
   -4\int_R^\infty\rho g r\xi^2dr
   -[\gamma P r^2\xi D]_R^\infty.
 \tag{4}
\]

At a fixed wall `xi(R)=0`; infinity is treated by the finite-energy form
closure of smooth compactly supported perturbations and no flux. For the
nonselfgravitating power law, integration by parts gives the identity

\[
 \int\gamma P D^2r^2dr-4\int\rho g r\xi^2dr
 =\int\gamma P(D-n\xi/r)^2r^2dr
   +[\rho g r^2\xi^2]_R^\infty.
 \tag{5}
\]

The fixed-wall right-hand side is exactly `Q_U/(4 pi)`. Thus the apparently
destabilizing term in (3) does not imply a negative radial eigenvalue with
these boundary conditions. The linearized conserved energy is
`(1/2) integral rho |dot xi|^2 d^3x + (1/2) Q_U`.

There is no positive uniform frequency gap on the infinite exterior: a smooth
displacement supported in `r in [L,2L]` has Rayleigh quotient proportional to
`mu_c/L^3`, tending to zero. Energy positivity controls the density form norm,
not every unweighted displacement norm. Fluid relabeling/vorticity zero modes
are not supplied a restoring force by a density Hessian.

## 4. A quantitative weak-self-gravity certificate

This section is conditional on an *actual* smooth hydrostatic equilibrium with
the same EOS, central source fixed, zero enthalpy at infinity, and

\[
 0<h(r)\leq C\mu_c/r,\qquad C\geq1.
 \tag{6}
\]

It does not use the power-law reference profile as though it remained an exact
self-gravitating equilibrium. Define

\[
 \rho_{\rm ref}(R)=A R^{-n},\qquad
 \varepsilon={4\pi\rho_{\rm ref}(R)R^3\over(n-3)M_0},
 \qquad q=n\varepsilon C^{n-1}.
\]

For a radial Eulerian density perturbation, set
`delta m(r)=4 pi integral_R^r delta rho(s) s^2 ds`. At a fixed impermeable wall
`delta m(R)=0`; physical mass-preserving no-flux perturbations also have
`delta m(infinity)=0`. The self-gravity Hessian and compressibility Hessian are

\[
 Q_W=-G\int_R^\infty{(\delta m)^2\over r^2}dr,\qquad
 Q_U={1\over4\pi}\int_R^\infty
 {c_s^2\over\rho r^2}(\delta m')^2dr.
 \tag{7}
\]

The normalization of `Q_W` follows directly by integrating
`integral delta rho delta Phi d^3x` and using
`delta Phi'=G delta m/r^2`; it is the second derivative of gravitational
energy, with no extra `1/2`.

Put `J=integral_R^infinity r^(n-3)(delta m')^2 dr`. Weighted Cauchy and Tonelli
give

\[
 (\delta m(r))^2\leq J\int_R^r s^{3-n}ds,
\]

\[
 \int_R^\infty{(\delta m)^2\over r^2}dr
 \leq J\int_R^\infty\!s^{3-n}\left(\int_s^\infty r^{-2}dr\right)ds
 ={R^{3-n}\over n-3}J.
 \tag{8}
\]

The condition `n>3` is essential to this bound. Since
`c_s^2/rho=[(n+1)K]^n h^(1-n)/n`, (6) implies

\[
 {c_s^2\over4\pi\rho r^2}
 \geq {G M_0 C^{1-n}\over
 4\pi n\rho_{\rm ref}(R)R^n}\,r^{n-3}.
 \tag{9}
\]

Combining (7)--(9) proves

\[
 \boxed{|Q_W|\leq qQ_U,\qquad
 Q_U+Q_W\geq(1-q)Q_U.}
 \tag{10}
\]

Thus `q<1` supplies a positive radial quadratic energy for that actual
equilibrium and those fixed-wall/no-flux perturbations. The bound is sufficient,
not a sharp instability threshold. Failure of `q<1` is inconclusive. Existence
of (6) is a separate input, not proved by the inequality. The estimate is
coercive in the compressibility form norm; it does not open a uniform spectral
gap in the inertial norm or imply nonlinear/all-mode/coupled-gauge stability.

## 5. A moving constant-pressure inner surface is a counterexample

Replace the fixed wall by a material inner surface allowed to move, with a
prescribed constant inner pressure `P_in=P_0(R)>0`. Its correct boundary
condition is

\[
 \Delta P(R)=-\gamma P(R)D(R)=0.
 \tag{11}
\]

The pressure reservoir contributes potential energy
`-P_in (4 pi/3) R_inner^3`. This sign counts the work done when the inner
volume expands; the gas-energy first variation at hydrostatic equilibrium is
`+4 pi R^2 P_0(R) xi(R)`. Those first variations cancel at equal pressure.
Ignoring the reservoir or forbidding its volume variation silently returns to
a different boundary problem.

For the prescribed-central-potential atmosphere choose

\[
 \boxed{\xi(r)=\xi_0(R/r)^2,\qquad\xi_0\ne0.}
 \tag{12}
\]

It has `D=0` everywhere, satisfies (11), has no outer mass flux, and has finite
inertia and finite energy. Its exact volume-preserving finite displacement is

\[
 r\mapsto(r^3+3\eta\xi_0 R^2)^{1/3}
\]

for sufficiently small real `eta`, so the witness is an admissible material
variation, not a density perturbation outside the fluid domain. Gas internal
energy is constant under this map. The reservoir energy is linear in `eta`;
the central gravitational energy has a strictly negative second derivative.
Equation (4), including the pressure boundary condition, gives explicitly

\[
 {Q\over4\pi}=-4\int_R^\infty\rho_0 g r\xi^2dr
 =-{4 A\mu_c\xi_0^2 R^{-n}\over n+4}<0,
\]

\[
 {I\over4\pi}=\int_R^\infty\rho_0\xi^2r^2dr
 ={A\xi_0^2 R^{3-n}\over n+1},\qquad
 {Q\over I}=-{4\mu_c(n+1)\over(n+4)R^3}.
 \tag{13}
\]

The last quotient is the value on a trial displacement, not a claimed exact
eigenfrequency. Smooth cutoffs at large radius preserve its negative sign.
Hence regular finite-interval self-adjoint radial problems with this inner
pressure condition and a sufficiently remote fixed outer wall have a negative
lowest `omega^2`. On the infinite-domain self-adjoint realization, a negative
form direction gives negative spectral support and growing linear solutions.
No isolated-eigenvalue assertion is needed. The negative second variation and
its boundary dependence already refute support-independent stability.

The same `D=0` test also makes the bulk form negative in a self-gravitating
hydrostate, because `g>0`. If the inner surface is material, its displacement
changes the Eulerian cumulative mass by the moving lower-limit contribution;
counting it restores `delta m=-4 pi r^2 rho xi` and (3). This observation does
not assume the original pure power law is self-consistent after self-gravity.

## 6. What restoring support would have to specify

If the supporting inner pressure is a prescribed differentiable function
`P_in(R_inner)`, then

\[
 \gamma P D(R)=-P_{\rm in}'(R)\xi(R),\qquad
 {Q\over4\pi}=\int\gamma P D^2r^2dr
 -4\int\rho g r\xi^2dr-R^2P_{\rm in}'(R)\xi(R)^2.
 \tag{14}
\]

For the nonselfgravitating power law this is

\[
 {Q\over4\pi}=\int {c_s^2\over\rho r^2}(y')^2dr
 -R^2[\rho(R)g(R)+P_{\rm in}'(R)]\xi(R)^2,
 \qquad y=r^2\rho\xi.
 \tag{15}
\]

In particular `P_in'<=-rho g` is a simple sufficient condition for a
nonnegative form. This is a constitutive condition on the support, not a
property supplied by the atmosphere EOS. A dynamical wall or inner fluid also
has inertia, its own energy, and coupled modes; a pressure law alone does not
model those.

For completeness the sharp *form* boundary in this prescribed-pressure model
can be computed without a spectrum. The infimum of
`integral_R^infinity r^(n-3)(y')^2 dr` for a fixed nonzero `y(R)` and compactly
supported tails is zero for `3<n<=4`, and
`(n-4) R^(n-4) y(R)^2` for `n>4`. This follows by Cauchy with the resistance
`integral_R^infinity r^(3-n)dr`, with tapering profiles approaching the bound.
Therefore the nonselfgravitating form is nonnegative precisely when

\[
 P_{\rm in}'(R)\leq
 \begin{cases}
 -\rho(R)g(R),&3<n\leq4,\\
 -4\rho(R)g(R)/n,&4<n\leq6.
 \end{cases}
 \tag{16}
\]

At equality no uniform gap follows. For `n>4`, the trace-capacity minimizer
would have `xi proportional to r^2`; its inertia is infinite in the stated
range `n<=6`. This is why the assertion is an infimum approached by finite
cutoff tests, not a finite-inertia zero eigenfunction. Constant pressure fails
both branches. No such stiffness or material interface has been derived from
the current-frame gauge action in this report.

## 7. Audit obligations and remaining gap

| Obligation | Result | Evidence/scope |
|---|---|---|
| EOS and exact central hydrostate | Passed | Section 1; `h+Phi_c=0` |
| Fixed-wall radial second variation | Passed | Sections 2--3 |
| Retain `-delta rho grad Phi_0` | Passed | Equations (1)--(3) |
| Weak self-gravity automatically destabilizes | Refuted as a universal claim | Bound (10) gives a positive open regime, conditional on existence |
| Weak self-gravitating equilibrium exists | Conditional | Must be supplied separately with (6) |
| Fixed-wall positive spectral gap | Failed | Tail-localized tests give `O(L^-3)` |
| Boundary-independent radial stability | Refuted | Admissible witness (12)--(13) |
| Vacuum at the finite inner edge | Failed for this profile | `P(R)>0` |
| Natural halo interface/support | Not addressed | Requires support field/fluid/wall action and matching |
| Coupled gauge, frame, transverse, relative modes | Out of scope | Principal and lower-order blocks need a joint analysis |
| Nonlinear smooth evolution and formation | Not addressed | Energy identity does not prevent shocks or establish capture |
| Observational halo/law fit | Out of scope | The neutral support is not asserted to be the charged MOND profile |

The dependency graph is: specified EOS and prescribed potential -> exact
central hydrostate -> convex fixed-domain energy; Euler plus mass conservation
and (when used) Poisson -> radial operator; actual hydrostate envelope plus
weighted Cauchy -> small-self-gravity bound; specified pressure reservoir plus
material-domain variation -> negative moving-boundary direction. There is no
external theorem used as a load-bearing mathematical leaf. The spectral
interpretation assumes the indicated self-adjoint conservative radial
realization; the energy sign and counterexample are proved directly.

**Strongest safe statement:** fixed-inner-wall isentropic radial density/flow
perturbations admit positive quadratic energy at zero self-gravity and for
actual weak-self-gravitating equilibria with `q<1`. An inner pressure reservoir
with constant pressure fails this test. The cheapest consequential next step
is to supply a regular core or derive the inner support's action and stiffness,
then include its perturbations. Appending the word “ambient” to a prescribed
inertial density does not complete this boundary obligation.

## 8. Source and verification record

Source bytes are the immutable copies under `../inputs/` and the companion
`source_manifest.json`, checkpoint `AS2-2026-10-15-01`, snapshot Git
`880c56463f022a2a38bd63692971c8a16403b22c`, requested recent-work base Git
`283acbcffe1c6c4a5e8f9860f66e43c4e3808ab3`. The source manifest distinguishes
tracked and untracked inputs. Canonical and shared files were read only.
The proof uses no fitted values, external literature theorem, numerical grid,
or sampled spectral sign. `PROVENANCE.json` records source verification and
the hash of this report. This is an independent reconstruction of the fluid
calculation; the source reports are not asserted to have already proved it.
