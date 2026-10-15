# A dynamical controller in one action

2026-10-14. C3W-003/004 and the formal energy extension below. The six-mode infinite-domain wall theorem is in [PROOF.md](PROOF.md). This document supplies an exact stationary controller completion and an analytic sufficient stiffness criterion. It does not supply a numerical controller specification, a finite-energy launch trajectory or cold-fuel realization.

## 1. Why replacing V by a knob is insufficient

Fix a smooth dimensionless profile σ(x), with b = Vσ and the source action of the wall theorem. Its inverse-source coefficients, target inverse metric in the strains, and Θ* all depend on V. Merely changing V in that action is changing assigned coefficients, not operating a demonstrated engine.

Promote V to a dimensionless scalar Λ and add canonical kinetic energy `−Fc² ∂Λ·∂Λ/2`, with constant Fc > 0. For the target family, define H_AB(Φ,Λ) as the Ricci coefficients of the metric with **constant parameter** Λ, evaluated at Φ. This prescription does not assume a variable-Λ target is already a solution.

On a constant Λ = V target, every new strain/repair density and its first variation vanishes. The controller field equation still gets the inverse-source force

\[
-\frac12\partial_VH_{AB}\,g_*^{AB}
=-\frac{M_p^2V}{4}
(\partial_x^2+\partial_y^2+4\partial_z^2)\sigma^2.
\]

The derivative of H is taken before contracting with the fixed target inverse metric. C3W-003 derives the identity from the complete coordinate Ricci tensor. The right-hand side varies across the wall. A spatially uniform potential U(Λ) alone generally cannot cancel it pointwise.

## 2. Exact derivative-current completion

Let E_A^μ be the inverse material Jacobian:

\[
E_A^\mu\partial_\mu\Phi^B=\delta_A^B.
\]

Introduce the fixed internal matrix A = diag(1,1,4), and add

\[
\boxed{\mathcal L_{\rm ctrl}
=-\frac{F_c^2}{2}\partial\Lambda\cdot\partial\Lambda
+J^\mu\partial_\mu\Lambda,\qquad
J^\mu=-\frac{M_p^2\Lambda}{4}
E_I^\mu A^{IJ}\partial_{\Phi^J}(\sigma^2).}
\]

There is no controller potential here. E is a vector under spacetime coordinate changes, and the action remains covariant. On the target Φ = x, E_I^μ = δIμ, √−g = 1 and Λ is constant. Both added densities vanish. Their metric and Φ variations vanish because they contain a derivative of Λ. The Λ variation of the current term is −∇μJμ, which equals

\[
+\frac{M_p^2V}{4}(\partial_x^2+\partial_y^2+4\partial_z^2)\sigma^2.
\]

It cancels the source force exactly. Thus **all constant V backgrounds in the allowed range belong to one specified covariant action** containing Λ. They are not solutions obtained by silently changing constants between runs. This is an inverse-designed controller, not a known laboratory coupling.

In unitary gauge the current term uses only spatial derivatives of Λ, since E_I^0 = 0. It introduces no lapse/shift time derivative or additional controller time derivative beyond the canonical kinetic term.

## 3. Exact controller gradient cost

A spatially varying controller needs its own energy analysis. A useful exact restriction is γ = I, N = 1, β = Λ(x)σ ez. The strain is zero pointwise on this restriction, but the actual curvature contains gradients of Λ that were not included in H_AB's constant-parameter definition. The current must not be dropped.

After one spatial integration by parts, the Einstein, inverse-source, current and Θ terms give

\[
F_{\Lambda,\rm geom}
=M_p^2\int\sigma^2\left[
\frac14((\partial_x\Lambda)^2+(\partial_y\Lambda)^2)
+\frac12(\partial_z\Lambda)^2\right]d^3x.
\]

C3W-004 verifies the local identity before integration: the difference is `−Mp² ∂z(Λ²σ∂zσ)`. This is a contribution to the **static Lagrangian**, so its positive sign requires compensation to obtain positive restoring energy. It is not available fuel.

The canonical controller contributes, to quadratic order around Λ = V,

\[
\frac{F_c^2}{2}\left[(\dot\ell-b\partial_z\ell)^2-|\nabla\ell|^2\right],
\qquad \ell=\delta\Lambda.
\]

For |σ|≤1 and |b|≤B, its static part is bounded above by `−Fc²(1−B²)||∇ℓ||²/2`. The pure controller sector is therefore restoring if `Fc²(1−B²)>Mp²`. This condition by itself does not control mixed controller/metric disturbances.

## 4. Sufficient mixed-energy criterion

Here is a precise analytic route that includes those disturbances, with an explicitly defined but not numerically evaluated coefficient norm. Keep the hypotheses of the wall theorem, with

\[
a=\frac18-\frac52B^2>0,\qquad
c=\frac1{2D}-13g^2-\frac32\eta>0,
\qquad \|Q\|_X^2=a\|\nabla Q\|_2^2+c\|Q\|_2^2.
\]

Change auxiliary variables to w = v−σℓ ez, with α unchanged. This is an invertible local field redefinition, not deletion of a mode. At Q = ℓ = 0 the joint velocity/auxiliary form is precisely the positive form of the wall proof plus `Fc²||dotℓ||²/2`: no other part of the unitary action contains dotΛ. Hence reduced kinetic energy remains positive for all seven physical variables.

For static trial auxiliaries α = w = 0, the metric-only form is Fb[Q], and the controller-only form is the one just derived. Write the remaining mixed contribution as Bmix[Q,ℓ]. The local ADM action contains at most first spatial derivatives of these perturbations after integration by parts. In any independent symmetric-matrix basis q for Q, its mixed density divided by Mp² can be written

\[
\ell\,a_0\cdot q+\ell\sum_j b_j\cdot\partial_jq
+\sum_i\partial_i\ell\left[c_i\cdot q+\sum_jd_{ij}\cdot\partial_jq\right].
\]

These coefficient arrays are uniquely defined after choosing this ADM representative by its mixed second variation. They are finite combinations of the smooth bounded background/profile coefficients and their derivatives. The symbol a0 here is an array, distinct from the coercivity constant a and from clock acceleration.

The constant-speed family is an exact solution of this **one action**. Its tangent is Q = 0, α = w = 0, ℓ constant. Differentiating its metric Euler equation gives `a0−Σj∂j bj=0`. Thus integrating by parts removes every undifferentiated ℓ term in Bmix:

\[
\frac{B_{\rm mix}}{M_p^2}=
\int\sum_i\partial_i\ell\left[(c_i-b_i)\cdot q
+\sum_jd_{ij}\cdot\partial_jq\right]d^3x.
\]

Let C0 and C1 be sup operator-norm bounds of these two coefficient arrays, using the Frobenius norm for Q, and define

\[
C_{\rm mix}=\sqrt{C_0^2/c+C_1^2/a}.
\]

They are finite for the fixed smooth profile and bounded speed interval; they do not depend on Fc, because the canonical controller has no metric/controller cross term at a constant Λ background. This defines a computable geometric norm, not a fitted experimental parameter. Then

\[
|B_{\rm mix}|\le M_p^2C_{\rm mix}\|Q\|_X\|\nabla\ell\|_2.
\]

Completing the scalar square and using the positive auxiliary Hessian as in the wall proof yields the sufficient criterion

\[
\boxed{F_c^2(1-B^2)>M_p^2(1+C_{\rm mix}^2).}
\]

Under this condition the reduced static Lagrangian is bounded above by

\[
-\frac{M_p^2}{2}\|Q\|_X^2
-\frac12\left[F_c^2(1-B^2)-M_p^2(1+C_{\rm mix}^2)\right]
\|\nabla\ell\|_2^2.
\]

Together with the joint kinetic estimate this is an analytic **existence criterion** for positive quadratic energy of the coupled controller theory. The controller is massless along its stationary family; use decaying ℓ in the homogeneous H¹ energy space, and dotℓ∈L². No uniform controller L² mass gap is claimed. The coefficient-array argument proves finiteness and sufficiency, but we have **not expanded the full mixed arrays, certified a numerical Cmix, or run an independent seven-mode matrix audit**. A concrete numerical controller stiffness and a controller propagation analysis therefore remain open. The independent 3D matrix audit in this package tests the six-mode wall theorem with Λ fixed, not this enlarged theory.

## 5. Why this is not yet launch

Changing Λ uniformly in time over R³ would cost `Fc² dotΛ²/2` per unit volume. A nonzero uniform dotΛ has infinite kinetic energy in this infinite medium. Stationary speed states cannot be joined by treating a global parameter as a cost-free instantaneous throttle.

A finite-energy route must use localized controller disturbances and solve the coupled time-dependent geometry, clock/material fields, controller and payload together. The stationary energy proof and the formal mixed-energy criterion do not supply that trajectory, its radiation or its work budget. The geometric and controller fields have not been tied to the separate χ/S conversion source. This document closes the fixed-coefficient stationary-controller equation, while preserving the actual finite-energy launch obligation.
