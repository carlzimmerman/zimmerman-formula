# The 32π puzzle: a symmetry identity, constrained vector modes, and a tested clock escape

Date: 2026-10-02 (America/New_York). Standalone conversation-workspace research.

**Original goal: NOT DERIVED.** This work does not obtain a first-principles coefficient in

\[
a_0=\frac c2\sqrt{G\rho_\Lambda}=c^2\sqrt{\frac{\Lambda}{32\pi}}.
\]

It answers a different, necessary question left by the previous checkpoint: whether the missing kinetic coefficient in the proposed gauge vacuum is merely an unreduced gauge artifact. A symmetry identity and a vector constraint reduction now sharpen that question. A minimal extra-clock construction is also explicitly tested, not just suggested.

All proofs and implementations are self-reviewed. No claim of literature priority, a full nonlinear constraint classification, or a viable MOND theory is made. No GitHub repository was modified. The previous archives are unchanged.

## 1. Action class, definitions, and the new identity

Use natural units c=ħ=1, metric signature (-,+,+,+), and M_P²=(8πG)^(-1). In this note ρ and p are the **energy density and pressure of the gauge sector**, not the SI mass-density convention for ρ_Λ in the target formula.

Consider

\[
S=\int d^4x\sqrt{-g}\left[\frac{M_P^2}{2}R+\mathcal L(F^a_{\mu\nu},g_{\mu\nu})\right].
\]

Assumptions: the matter action is twice differentiable at the state; it is invariant under proper local Lorentz transformations and adjoint SO(3) rotations; it is minimally coupled; it depends algebraically on field strengths, with no covariant derivatives of F, explicit gauge-potential mass terms, nonminimal curvature dependence, or additional nonzero background tensors. Arbitrary invariant functions and parity-odd interactions are allowed. A constant vacuum term does not affect the argument.

On an isotropic triad,

\[
E_{ai}=E\delta_{ai},\qquad B_{ai}=B\delta_{ai},\qquad E^2+B^2>0,
\]

write ℓ(E,B)=L(E1,B1). First derivatives with respect to the matrices are p_E 1 and p_B 1, with p_E=ℓ_E/3 and p_B=ℓ_B/3. Let Z_E, Z_EB, and Z_B be the Hessian coefficients in the antisymmetric matrix sector. For an antisymmetric generator J with ||J||²=2, the quadratic variation is

\[
\delta^2\mathcal L/2=Z_E e^2+2Z_{EB}eb+Z_B b^2,
\quad \delta E=eJ,\quad\delta B=bJ.
\]

The normalization is fixed by this equation; no arbitrary polarization rescaling is hidden in Z_E.

### Proof from transformations, not a scan of potentials

An infinitesimal internal rotation and an infinitesimal Lorentz boost about the same axis give, respectively,

\[
(\delta E,\delta B)=(EJ,BJ),\qquad
(\delta E,\delta B)=(BJ,-EJ).
\]

Including their second variations, invariance of the scalar Lagrangian supplies three equations:

\[
E^2Z_E+2EBZ_{EB}+B^2Z_B=Ep_E+Bp_B,
\]
\[
B^2Z_E-2EBZ_{EB}+E^2Z_B=-Ep_E-Bp_B,
\]
\[
EB(Z_E-Z_B)+(B^2-E^2)Z_{EB}=Bp_E-Ep_B.
\]

Their unique solution at E²+B²>0 is

\[
\boxed{Z_E=\frac{Ep_E-Bp_B}{E^2+B^2},\qquad
Z_B=-Z_E,\qquad Z_{EB}=\frac{Bp_E+Ep_B}{E^2+B^2}.}
\]

Minimal metric variation on the triad gives

\[
\rho=E\ell_E-\ell,\qquad
p=\ell-\frac{E\ell_E+2B\ell_B}{3},
\]

hence the central identity:

\[
\boxed{Z_E\equiv Z_A=\frac{\rho+p}{2(E^2+B^2)}.}
\]

This is an exact statement under the listed assumptions. Checks against ten distinct invariant examples—including a nonpolynomial example and invariants invisible to the homogeneous ansatz—test the implementation, not the generality of the proof.

For a source-free isotropic de Sitter state in this class, Einstein's equation requires ρ+p=0, so Z_A=0. More generally, if this sector is the only contribution to ρ+p,

\[
Z_A=-\frac{M_P^2\dot H}{E^2+B^2}
=\frac{M_P^2H^2\epsilon_H}{E^2+B^2},\qquad
\epsilon_H=-\dot H/H^2.
\]

Thus the zero cannot be removed on an exact de Sitter state merely by choosing more algebraic, Lorentz/gauge-invariant functions of F. This is **not** a proof that every degenerate action is inconsistent: an action-wide constrained sector must be distinguished from a loss of rank occurring only on one background. Extra fields, curvature couplings, and derivative interactions lie outside the result.

## 2. The polynomial benchmark and physical vector constraints

The prior checkpoint studied

\[
\ell=\frac32(E^2-B^2)+\beta(18EB^2-6E^3)
+\gamma E^2B^2+\zeta(E^2-B^2)^2.
\]

It has the dimensionless example

\[
M_P^2=g_{\rm YM}=q=E=B=H=1,\quad
\beta=\frac16,\quad\gamma=2,\quad\zeta=\frac12.
\]

The background is a homogeneous attractor within the previously tested two-variable system. The chosen constants are not microscopic predictions and the example does not reproduce the observed vacuum density. The original 49-check checkpoint was rerun successfully in a separate copy; that is baseline reproduction, not a new full-theory certificate.

The symmetric-traceless and antisymmetric electric coefficients are

\[
A_s=1+6\beta E+\frac{4\zeta}{3}(E^2-B^2),\qquad
D=1-6\beta E+\frac{4\zeta}{3}(E^2-B^2).
\]

Here D=Z_A; it is unrelated to the dimensionless vacuum coefficient named D in the earlier microscopic matching note. At the benchmark A_s=2 and D=0.

### Finite-wavelength reduction

Choose a physical wave vector k along z. Fix the spatial metric vector gauge and the internal axial gauge δA_z^a=0. The latter is nonsingular only away from k=0 and k=|g_YM q|; these exceptional gauges are not used in the numerical tests.

Let m=g_YM q and σ=±1 label vector helicity. Keep the temporal gauge variable u_σ and the metric shift w_σ until varying them. Phase conventions can be chosen so that the velocity/constraint part of the quadratic Lagrangian is

\[
\frac{\mathcal L_{\rm vel,\sigma}}{a^3}
=\frac{A_s}{4}(v-ku)^2
+\frac D4[-v+(2\sigma m-k)u-2Bw]^2
+\frac{M_P^2k^2}{4}w^2.
\]

Here v is the velocity of the remaining vector amplitude. The scalar lapse does not mix with this vector-helicity block. Terms containing the fields but not their velocities do not modify this kinetic Schur complement.

Eliminating u and w gives L_vel/a³=K_σ v²/2 with

\[
\boxed{K_\sigma=
\frac{2A_sD M_P^2(k-\sigma m)^2}
{4A_sB^2D+M_P^2[A_sk^2+D(k-2\sigma m)^2]}.}
\]

This calculation retains both Gauss and gravitational momentum constraints. An independent 12-real-variable cosine/sine Fourier implementation reproduces the two helicity eigenvalues, each with its real-mode multiplicity.

At regular generic k,

\[
K_\sigma\big|_{D=0}=0,\qquad
\left.\frac{\partial K_\sigma}{\partial D}\right|_{D=0}
=2\frac{(k-\sigma m)^2}{k^2}>0.
\]

Also K_σ→2A_sD/(A_s+D) as k→∞. Consequently the missing second-order kinetic term survives the constraint reduction, and neighboring regular backgrounds have negative physical vector kinetic energy on the D<0 side. At D=0 itself the coefficient is zero, **not negative**. First-order terms, nonlinear constraint rank, and a possible strong-coupling scale are not inferred just from this zero.

For q=B=g_YM=M_P²=1, the same fixed action, and k=10:

| E | D | K_- | K_+ |
|---|---:|---:|---:|
| 0.999 | -0.0003326666667 | -0.0008052571490 | -0.0005389846158 |
| 1 | 0 | 0 | 0 |
| 1.001 | 0.000334 | 0.0008080751047 | 0.0005410150158 |

Each neighboring state has positive ρ, nonzero ℓ_EE, and H determined by the Friedmann constraint. These are admissible local homogeneous initial data, not new de Sitter fixed points and not observed cosmological parameters. A negative coefficient is a ghost sign in this regular vector block, rather than merely a Jeans growth mode.

## 3. The positive side is not automatically preserved by the dynamics

Near q=E=1, the independently differentiated homogeneous flow has

\[
J=\begin{pmatrix}-2&1/6\\44/5&-1\end{pmatrix},
\qquad\operatorname{tr}J=-3,\quad\det J=8/15.
\]

Although its two homogeneous perturbations decay, the kinetic quantity obeys

\[
\delta D=-\frac83\delta q+\frac13\delta E,
\qquad
\delta\dot D=\frac{124}{15}\delta q-\frac79\delta E.
\]

On the local D=0 surface, δE=8δq, so

\[
\boxed{\delta\dot D\big|_{D=0}=\frac{92}{45}\delta q.}
\]

For δq<0, the vector field points into D<0. The exact local D=0 curve is

\[
E_b(q)=\frac{3+\sqrt{16q^4-15}}4.
\]

An explicit initial condition q=0.999, E=E_b(0.999)+10^-5 has D≈3.2251×10^-6>0. A homogeneous ODE integration crosses D=0 at t≈0.00176651 in the benchmark units, and ends at D≈-3.2316×10^-5 at t=0.02. Refining the integrator reproduces the crossing. This does not claim a well-posed inhomogeneous evolution through the singular kinetic surface, and not every initial trajectory is claimed to cross it. It demonstrates that restricting initial data to D>0 is not, by itself, a dynamically protected prescription.

## 4. Execute an escape from the symmetry assumptions

An independent timelike clock changes the premises. Define

\[
u_\mu=-\frac{\nabla_\mu\tau}{\sqrt X},\qquad
X=-g^{\mu\nu}\nabla_\mu\tau\nabla_\nu\tau,
\qquad h_\mu{}^\nu=\delta_\mu{}^\nu+u_\mu u^\nu,
\]
\[
J_\mu=h_\mu{}^\nu T^{\rm YM}_{\nu\rho}u^\rho,
\qquad
\Delta\mathcal L=\frac{\lambda_{\rm phys}}2J_\mu J^\mu.
\]

T^YM is the stress tensor of the quadratic -F²/4 term, not the full nonlinear gauge stress. In the clock rest frame J is, up to the sign convention for electric fields, the gauge Poynting flux. It vanishes on an isotropic triad. Its square and its first variations therefore leave the homogeneous benchmark unchanged.

The presence of u is essential: the earlier Ward proof cannot hold u fixed while performing a boost of all physical fields. This is a covariant construction with an additional background field, not a counterexample inside the pure-L(F) class.

At the benchmark, use λ=λ_phys B_0² as a dimensionless coefficient (B_0=1 in the displayed units). The new antisymmetric Hessian pieces are

\[
\Delta Z_E=2\lambda,\quad
\Delta Z_B=2\lambda,\quad
\Delta Z_{EB}=-2\lambda.
\]

The leading large-k vector coefficients, after Gauss reduction, are

\[
K_V=\frac{4\lambda}{1+\lambda},\qquad
G_V=\frac{2(1-\lambda)}{1+\lambda},\qquad
c_V^2=\frac{G_V}{K_V}=\frac{1-\lambda}{2\lambda}.
\]

The principal vector sector has positive kinetic and spatial coefficients for 0<λ<1; 1/3≤λ<1 also gives c_V²≤1 in this background frame. For λ=2/3, K_V=8/5, G_V=2/5, c_V²=1/4. The mixed single-helicity velocity/curl term is a boundary term at constant coefficients and contributes only lower-order terms on de Sitter; it was not mistaken for a change in the principal speed.

This is a genuine limited repair of the vector sector. It is not a prediction of λ or a stability certificate for the added clock.

## 5. Test the clock rather than assume it is harmless

For the smallest explicit clock completion, add

\[
\mathcal L_\tau=\frac{\mu}{2}(X-1)^2,\qquad\mu>0,
\]

with τ=t on the background. Its background value and first derivative vanish, so it does not change the chosen vacuum. In the benchmark units μ is a positive normalized clock coefficient. No higher-spatial-derivative operators are included.

Keep τ=t+π, the lapse n, scalar shift S, temporal gauge field t_3, and the two scalar gauge perturbations x,y. Use spatially flat metric gauge, internal axial gauge, x and π cosine Fourier amplitudes and y,t_3,S sine amplitudes. The covariant action is expanded before the three constraints are eliminated.

The constraint determinant is proportional to

\[
-k^2[17k^2-68\lambda\mu+18\lambda].
\]

It is nonzero at sufficiently large k. The fully reduced high-frequency scalar kinetic matrix is

\[
K_S=\operatorname{diag}(60/17,4\lambda,4\mu)>0.
\]

A separate derivation gives the equivalent leading principal Lagrangian, up to boundary terms and a common positive spatial-average factor:

\[
\frac{\mathcal L_{S,\rm UV}}{a^3}
=\frac{30}{17}\dot x^2
-\frac4{17}k y\dot x
+\frac{110}{153}k^2y^2
+2\lambda(\dot y+kx-2k\pi)^2
+2\mu\dot\pi^2.
\]

The mixed terms must be retained in the characteristic equation. With s=(ω/k)², one branch has s=0 and the two nonzero branches obey

\[
\boxed{135\lambda\mu s^2+
\mu(48-18\lambda)s+
\lambda(55\mu+192)=0.}
\]

For the vector-healthy interval 0<λ<1 and μ>0, all three coefficients are strictly positive. Neither nonzero root can be real and nonnegative; roots are negative or complex. Thus this minimal clock completion has an unstable scalar principal part despite its positive scalar kinetic matrix and healthy vector principal modes.

For λ=2/3 and μ=1/10,

\[
s=-\frac15\pm\frac{2i\sqrt{7386}}{45}
\approx-0.2\pm3.81964i.
\]

The leading growing exponent has Γ/k≈1.41860. A full reduced frozen-coefficient matrix calculation approaches that value at increasing k. It is not a cosmological time evolution with the redshifting wave number integrated, nor a claim that arbitrarily large k lies within an unspecified EFT cutoff. A physical EFT exclusion requires an unstable band below its cutoff. The formal unregulated two-derivative principal-symbol problem is nevertheless definite.

The initial scalar-check script incorrectly constrained s to be real when asking a symbolic solver for complex roots; the verification failed rather than producing a false pass. The domain error was corrected, and all final checks pass. The old failure log is preserved and is not the final scientific status.

This rejects the **displayed minimal Poynting-square plus P(X) clock repair**, not all clock theories. Additional stiffness, higher-derivative, nonminimal, or other matter operators would be different theories and need their own constraint and weak-field analyses. Their parameters cannot be chosen to fit the half and then called derived.

## 6. What this says about the original coefficient

These results do not determine a0. The new vacuum's baryon/dipole response has not been derived, and no oscillatory formula from a different state is imported. The interaction coefficients and the clock coefficients are prescribed. The bare vacuum normalization and the observed small scale remain separate issues.

The genuine advance is a structural restriction on the attempted common-origin mechanism:

* In pure minimally coupled L(F), an exact isotropic de Sitter state has a vanishing antisymmetric electric coefficient by symmetry.
* In the explicit polynomial model, it vanishes after the relevant vector constraints are eliminated and has a negative-kinetic side arbitrarily close by. The homogeneous flow can cross from the positive side.
* Adding an explicit clock can restore the vector principal sector, but the simplest actual clock completion fails its scalar principal-symbol test.

None is a proof that no first-principles theory can yield the half. None is itself that derivation.

## 7. Reproduction and evidence

Run `python run_all.py`. The three new scripts execute **102 checks: 66 exact symbolic checks and 36 finite numerical checks**. Finite checks include expected unhealthy cases; a passing regression test is agreement with the stated calculation, not a stability pass. The separate original checkpoint rerun passed its original 49 checks and is not counted as new evidence.

The direct Lorentz-index contraction, transformation-orbit derivation, helicity Schur reduction, real Fourier matrix implementation, independently reconstructed scalar principal action, and refined homogeneous trajectory provide different representations of the load-bearing steps. They are not independent peer review. The scalar/tensor spectrum of more elaborate repairs, nonlinear Dirac analysis at the degenerate point, renormalization and galactic response are not supplied.

## 8. Sources and bounded attribution

The inherited cubic convention comes from Blanchet–Seraille, arXiv:2502.14686v2, equation (74). The isotropic SU(2) triad and homogeneous metric variation are standard in gauge-flation, arXiv:1102.1513v4. The two quartic additions, the specified clock test, and their coefficients are the explicit constructions tested in this conversation, not predictions attributed to those papers. Primary HTML was consulted in this continuation; no broad novelty search or downloaded full-paper source hash is claimed.
