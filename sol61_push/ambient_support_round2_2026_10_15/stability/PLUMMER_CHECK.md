# Independent check of the regular-core Plummer alternative

AS2-STABILITY-002, 15 October 2026. This is a separate check of the regular-core
construction proposed by the root agent during the round. It does not replace
the exterior atmosphere or its moving-interface counterexample in `REPORT.md`.
No numerical computation or external theorem is used.

**Verdict: the proposed equilibrium normalization and sufficient Newtonian
density-Hessian bound are correct under the assumptions below.** A fixed
prescribed Plummer gravitating source plus a neutral, self-gravitating
`gamma=6/5` polytrope of the same Plummer shape has a positive fluid density
Hessian when its total mass is less than one quarter of the prescribed central
source mass. This has no artificial inner wall. It does not establish stability
of a dynamical central source or of the coupled gauge/frame system.

## 1. Exact object and hydrostatic normalization

Let `M0,b,K>0`. The prescribed source is fixed in space and has

\[
 \rho_b(r)={3M_0b^2\over4\pi}(r^2+b^2)^{-5/2},\qquad
 \Phi_b(r)=-{GM_0\over\sqrt{r^2+b^2}}.
\]

Let the neutral fluid have `rho_s=f rho_b`, `f>0`, so its mass is `Ms=f M0`.
Its own potential is `Phi_s=f Phi_b`. Write the positive total potential
magnitude

\[
 V=-\Phi_b-\Phi_s
  ={G M_0(1+f)\over\sqrt{r^2+b^2}}.
\]

For `P=K rho_s^(6/5)`, `h=6K rho_s^(1/5)` and `c_s^2=h/5`. With zero
enthalpy and potential at infinity, hydrostatic balance is precisely `h=V`.
It holds if and only if

\[
 f=\mu(1+f)^5,\qquad
 \mu={4\pi\over3M_0b^2}
       \left({G M_0\over6K}\right)^5.
 \tag{1}
\]

The normalization uses
`integral_0^infinity r^2(r^2+b^2)^(-5/2) dr=1/(3b^2)`.
The function `f/(1+f)^5` increases on `0<f<1/4`, attains
`4^4/5^5` at `f=1/4`, and decreases afterwards. Thus every
`0<mu<4^4/5^5` has a small branch with `0<f<1/4`. This is an exact existence
construction; no weak-field Newtonian claim is implied unless the separate
potential-depth condition `GM0(1+f)/(b c^2)<<1` is also imposed.

The equilibrium is regular at the origin, has no material interface, has
finite mass, and has a nonzero density at every finite radius. It tends to zero
only at infinity. A finite-radius charged subsystem may use this as candidate
ambient support, but its own forces and current-frame couplings still require
the full joint equations.

## 2. A direct kernel inequality, valid beyond radial perturbations

Let `delta rho` be any real density perturbation with finite compressibility
quadratic form

\[
 Q_U=\int_{\mathbb R^3}{c_s^2\over\rho_s}(\delta\rho)^2d^3x
 =\int_{\mathbb R^3}{V\over5\rho_s}(\delta\rho)^2d^3x.
\]

The fixed external potential contributes no density Hessian. The self-gravity
Hessian is

\[
 Q_W=-G\iint {\delta\rho(x)\delta\rho(y)\over|x-y|}d^3x\,d^3y.
\]

For `rho_s>0`, the elementary inequality

\[
 2|\delta\rho(x)\delta\rho(y)|\leq
 {\delta\rho(x)^2\over\rho_s(x)}\rho_s(y)
 +{\delta\rho(y)^2\over\rho_s(y)}\rho_s(x)
\]

can be integrated against the positive Newton kernel. As

\[
 G\int {\rho_s(y)\over|x-y|}d^3y
 =-\Phi_s(x)={f\over1+f}V(x),
\]

Tonelli first for the nonnegative majorant and then the triangle inequality
prove

\[
 \boxed{|Q_W|\leq {5f\over1+f}Q_U,\qquad
 Q_U+Q_W\geq {1-4f\over1+f}Q_U.}
 \tag{2}
\]

In particular the majorant is finite for the stated form domain, justifying
the signed integral. This proof is not a radial mass-coordinate substitution:
it covers arbitrary angular dependence in the Newtonian density Hessian.
Mass-preserving perturbations form a subset. In the symmetrized weighted
Newton operator, the positive Schur eigenfunction is
`sqrt(a) rho_s`, where `a=c_s^2/rho_s`, and the associated eigenvalue is
`5f/(1+f)`. This identifies the weight precisely; saying merely “eigenfunction
V” without the operator and its measure is ambiguous.

The contraction derivative of the normalization map `F(f)=mu(1+f)^5` at a
fixed point is also `F'(f)=5f/(1+f)`. This equality is consistent with the
energy calculation; a contraction statement is not used in place of the
kernel proof.

## 3. Scope of the stability conclusion

For `0<f<1/4`, adding the positive kinetic quadratic form gives a positive
Newtonian barotropic fluid energy in density and velocity. Under the
conservative linearized Euler-Poisson realization with regular origin and
finite-energy/no-flux infinity, this excludes a negative-energy density
instability. Density-free relabelings/vorticity remain neutral directions.
The estimate controls the compressibility norm and gives no uniform frequency
gap on the infinite tail.

The coefficient in (2) becomes zero at `f=1/4`. Saturation on unrestricted
density variations uses `delta rho` proportional to `rho_s`, which changes
the fluid mass. Therefore neither the equality point nor failure of this
sufficient bound proves instability in the physically mass-preserving class.

The following obligations remain separate:

* If the prescribed source is allowed to move, its kinetic, pressure, and
  gravitational cross terms must enter the same Hessian.
* The barotropic perturbations keep the same `K`; entropy or composition modes
  are not inferred from this density Hessian.
* Relativistic corrections require an actual relativistic equilibrium and its
  energy, even if the displayed Newtonian depth is small.
* Neutral matter entering a varied constitutive frame is not automatically a
  minimally coupled passive fluid. The static radial hydrostate and the full
  gauge/frame perturbation equations must be checked jointly.
* Quadratic energy positivity does not prove global nonlinear smoothness,
  formation, a microscopic EOS, or an observed halo mass profile.

This alternative removes the specific inner-wall obligation by replacing it
with a fixed regular-source assumption. It supplies a stronger conditional
fluid result than the exterior atmosphere, while leaving the gauge and
physical-identification obligations explicit.
