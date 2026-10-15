# Two explicit replacements for the failed boundary mechanism

The [harmonic no-go](NO_GO.md) closes the stronger-amplitude route for the old action. It does not prohibit changing that action. These alternatives address the exact uncontrolled variable rather than increasing the coefficient that missed it.

## 1. Keep the lapse constraint everywhere at the flat rest state

Remove the quadratic clock/lapse mass **globally**, and remove the acceleration-square term globally. Keep nonnegative compact shift and spatial strain masses, θ, and κ. In the flat theory, the quadratic mass density is now

\[
2h_s|v|^2-\tfrac12h_m|Q|^2,
\qquad h_s,h_m\ge0,
\]

with no hclock α² and no A|∇α|². The lapse is a multiplier imposing R1(Q)=0 on all of R³, not only outside the body. This is a different action from retaining that mass in the core and tapering it outside.

Use smooth sufficiently decaying constrained fields and stationary bounded smooth compact constitutive profiles. With u=uTT+Dζ, v=ζ+w, the Einstein kinetic identity gives

\[
J={M^2\over8}\|u^{TT}\|_2^2+{M^2\over8}\int\kappa|u|^2
+{M^2\over4}\|\operatorname{curl}w\|_2^2
+{M^2\over2}\int\theta(\operatorname{div}w)^2
+2\int h_s|w+\zeta|^2.
\]

Every term is nonnegative. The last three form a nonnegative affine minimization, finite at w=0. Taking their minimum in the associated completed energy space gives

\[
T_{\rm red}(u)\ge{M^2\over8}[\|u^{TT}\|_2^2+\int\kappa|u|^2].
\]

The static constrained energy is exactly

\[
V(Q)={M^2\over8}[\|\nabla Q^{TT}\|_2^2+\int\kappa s^2|\nabla Q|^2]
+\tfrac12\int h_m|Q|^2\ge0.
\]

Thus E2=Tred+V is nonnegative for arbitrary three-dimensional perturbations, arbitrary wavelengths and arbitrary shapes of these compact profiles. This extends the previous massless-cap result to a finite body with positive spatial and shift masses. It is a continuum quadratic proof, not an inference from the test grids. Conservation holds for existing smooth finite-energy solutions with no flux at infinity. Vacuum gauge null directions, degenerating kinetic density, and well-posedness remain to be analyzed; a globally coercive norm or nonlinear theorem is not asserted.

The harmonic witness is now forbidden: its compactly cut-off Hessian velocity has nonzero R1(u) in the core and cannot satisfy the **global** lapse constraint. The construction removes the unwanted clock degree of freedom in the linear rest problem instead of trying to stabilize it at a material boundary.

### Covariant specification and its limit

In the old source action replace the framed clock coefficient (h−Hnn)(S00)²/8 by −Hnn(S00)²/8, keeping the other shift/spatial strain terms. Set A=0. At the rest background H=0 this deletes the lapse mass exactly and implements the theorem. Repair squares still vanish with their first variations on the assigned target, so this change preserves the inverse-engineered stationary background. It does not prove that the lapse remains a constraint on that curved background or nonlinearly.

Indeed the old curved-core joint kinetic square includes |u−Dv−αE0|², with E0=−Dβ*. Even without an explicit lapse mass, its α² coefficient is nonzero where E0≠0. A full Hamiltonian constraint analysis is needed there; the simple flat multiplier proof cannot be imported. Removing α² about one background is not a nonlinear degree-of-freedom theorem.

This caveat is consistent with the established massive-gravity literature. [Dubovsky, hep-th/0409124v2, introduction and sections 3–4](https://arxiv.org/pdf/hep-th/0409124), discusses special zero-clock-mass linear phases and the need to control higher-order operators. Our derivative-elastic, spatially localized action is not identified with that paper's homogeneous mass-only models, and none of its parameter windows is imported. [Hassan, Rosen and Schmidt-May, 1109.3230v2](https://arxiv.org/pdf/1109.3230), proves nonlinear constraint removal for a different specified potential family; it supplies context for the missing analysis, not a theorem about this action. No novelty claim is made.

## 2. Penalize gradients of the material velocity relative to the clock

If the clock mass is retained, the counterexample exposes the missing penalty: harmonic shifts have zero divergence in the body but large shear. Define material normal velocity B^I=Uμ∂μΦI and its target value B*I=−b(Φ)δIz. The difference ZI=B^I−B*I vanishes on the target. Add the covariant operator

\[
L_{\rm shear}={M^2\lambda(\Phi)\over2}
\sum_I P^{\mu\nu}\partial_\mu Z^I\partial_\nu Z^I,\qquad\lambda\ge0.
\]

This term and its first variation vanish on the assigned target. In unitary gauge P00=P0i=0 and Pij=γij; B^I=−βI/N. Therefore it contains spatial derivatives of shift/lapse and no time derivatives of either. In the flat rest quadratic action it is +M²λ|∇v|²/2. Its positive sign is an auxiliary stiffness, not an assumption of positive physical energy after elimination.

There is an exact positive result for the formerly dangerous core-supported velocities. Suppose u has compact support where θ=1, and λ≥1/(1+κ) there. After integrating the Einstein shift form, the only indefinite cross term is −M²u:sym∇v/2. Pointwise on that support,

\[
{1+\kappa\over8}|u|^2-\tfrac12u:S+{\lambda\over2}|\nabla v|^2
={1+\kappa\over8}|u-2S/(1+\kappa)|^2
+\tfrac12[\lambda|\nabla v|^2-|S|^2/(1+\kappa)]\ge0,
\]

where S=sym∇v and |S|≤|∇v|. The remaining curl, θ-divergence and shift-mass terms are nonnegative. Hence this operator blocks the entire core-supported harmonic counterexample family; it does not merely move that family's threshold to higher k. For κ=4, λ≥1/5 in the core suffices for this statement.

The proof does not cover every velocity extending through the phase transition, the full curved wall, or nonlinear stability. The new operator also changes material dynamics and must be justified microscopically. It is a mathematically explicit route, not a measured interaction between cold energy and baryons.

## Finite checks

[Replacement run v2](replacement_run_v2/calculation/results.json) retains the old negative control and tests the globally zero-clock-mass and shear-penalized versions with full six-component constrained matrices, multiple transverse momenta and two z resolutions. Independent TT projection verifies the first replacement's kinetic lower bound and static energy identity. Near-zero numerical negatives remain at the 10^-10 scale; the continuum theorem, rather than rounding them away, supports the first replacement's scoped positivity.

The shear version's passing finite tests are supplementary evidence only. Its all-mode continuum statement remains open. Neither alternative supplies the physical negative-stress material, a validated controller coupling, or a powered launch with payload backreaction.
