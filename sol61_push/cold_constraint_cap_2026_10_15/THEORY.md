# Finite-phase geometric transport: a precise candidate, with open obligations

2026-10-15. Base checkpoint 863b2cda565b1d7d874751e3ddb14a2ef6457bd3; the shared repository had advanced to fdd6693f3e003fc72bf6d550ec26599eabc8931b when this investigation began. This document assembles the strongest surviving candidate. **The physical propulsion theory is not complete.** The new results remove a specific flat-interface obstruction; they do not identify cold energy or prove an operating engine.

## What changes

A common window multiplying all stabilizers fails, as [previously derived](../cold_vacuum_interface_2026_10_15/REPORT.md). The replacement uses a spatial ordering: stop the lapse/shift mass and lapse-gradient terms in a flat collar while the expansion and derivative-elastic stabilizers remain strong; only farther out taper those remaining stabilizers to zero. The lapse then imposes a constraint instead of leaving a negative-energy scalar free to move.

The [new proofs](PROOF.md) establish three different statements, with different scopes:

| Statement | Established scope | Limit |
|---|---|---|
| Mass removal at fixed strong stabilizers | Exact homogeneous six-mode spectrum, every momentum | A path of constitutive parameters, not a powered trajectory |
| Finite massless cap | Nonnegative quadratic energy for all R³ perturbations satisfying the lapse constraint, arbitrary smooth compact nonnegative cap profiles | Flat background; degenerate energy; no existence/nonlinear theorem |
| Spatially staged massive interior and cap | Nonnegative full planar quadratic energy, all six metric components and lapse/shift, stationary variable profiles | Dependence on t,z only; infinite slab; not a spherical moving wall |

These are complementary results, not a proof obtained by silently gluing their conclusions. In particular, the curved 3D core and its general 3D massive-to-massless transition still need a joint estimate.

## One explicit finite-source candidate action

Use the previous material-coordinate construction and target

\[
ds_*^2=-dt^2+dx^2+dy^2+[dz+V\sigma(r)dt]^2,
\qquad\Phi_*^A=x^A.
\]

Here σ is the smooth spherical step: zero in the cabin, one outside the wall. Its derivatives are compactly supported. The target has flat spatial slices and a constant exterior shift, which is flat spacetime in a different chart. Define H_AB=M² Ricci_AB[g*] as a function of Φ, so H vanishes outside the curvature wall. This is an **inverse-engineered stress model**; it does not derive the material from known particles.

Let h(Φ)≥0 be the strain scale, supported in a region containing the curvature wall. Use the same framed inverse-metric strains S as in the [previous exact construction](../cold_3d_wall_2026_10_14/PROOF.md). Let Hnn,Hni,Hij denote the normal-frame components of H itself, without division by h. Set

\[
\begin{aligned}
L_{\rm strain}={h-H_{nn}\over8}(S^{00})^2
&+\tfrac12 S_0^T(4hI-H_s)S_0-\tfrac12S^{00}(H_n\cdot S_0)
-\tfrac h2\sum_{ij}(S^{ij})^2\\
&+\sum_iH_{ni}[\sum_jS^{0j}S^{ij}-\tfrac12S^{0i}\operatorname{tr}S].
\end{aligned}
\]

This expanded form stays defined where h=0. Writing H/h there would be invalid.

The gravitational/material candidate is

\[
\begin{aligned}
L_{\rm candidate}={M^2\over2}R
-\tfrac12H_{AB}(\Phi)\partial\Phi^A\cdot\partial\Phi^B
+L_{\rm strain}
+{M^2\theta(\Phi)\over2}(\Theta-\Theta_*)^2
+{M^2A(\Phi)\over2}a_\mu a^\mu\\
+{M^2\kappa(\Phi)\over8}\sum_{IJ}[(U\cdot\partial C^{IJ})^2-s^2(\Phi)P^{\mu\nu}\partial_\mu C^{IJ}\partial_\nu C^{IJ}].
\end{aligned}
\]

Definitions of U,P,C are in [the cap proof](PROOF.md); aμ=Uν∇νUμ and Θ*=−∂z(Vσ) in material coordinates. Choose θ=1, κ=K≥4 and s²=1/2 throughout the wall and the support of h,A. The original weak choice K=4 has adverse oblique finite evidence; K=64 is a stronger candidate for the next continuum audit, not a certified value. Make h and A vanish in a surrounding flat collar. Farther out smoothly taper θ and κ to zero. The option s²=1 in the outer massless region makes its homogeneous quadratic branches luminal; changing this coefficient must be included explicitly, and does not alter the older core result by assertion.

**Exact background statement.** Every added strain/repair term is a square or quadratic product whose value and first variation vanish on the target. Multiplying it by a fixed smooth material-coordinate coefficient preserves that property, even when the coefficient varies. The inverse Ricci source therefore still supports the prescribed stationary metric. Outside all constitutive support, H=h=A=θ=κ=0 and the gravitational/material action is Einstein gravity with decoupled Φ fields. This supplies an exact prescribed finite-source stationary background, not a proof of its stability or production. The fixed-V source is one action per chosen V unless the controller completion below is used.

The target's normal source energy remains negative in parts of the wall:

\[
T_{nn}=-{M^2\over4}[(\partial_x b)^2+(\partial_y b)^2].
\]

Localizing the repair medium does not manufacture this source or make it ordinary baryonic matter. The physical meaning of that negative background stress remains a fundamental unresolved input.

## A controller and an energy source are additional hypotheses

For a single action containing multiple steady speeds, replace the constant parameter V by Λ in the source and target coefficient definitions, taking parameter derivatives before tensor contraction. The previous derivative-current completion

\[
L_\Lambda=-\tfrac12F_c^2(\partial\Lambda)^2+J^\mu\partial_\mu\Lambda,
\quad
J^\mu=-{M^2\Lambda\over4}E_I^\mu\operatorname{diag}(1,1,4)^{IJ}\partial_{\Phi J}\sigma^2
\]

cancels the missing constant-Λ controller source. E is the inverse material-coordinate Jacobian. The current is compactly supported because ∂σ² is. Multiplying the vanishing repair squares by the new spatial profiles does not change this background cancellation. The current defines stationary states of a proposed fixed action; arbitrary Λ(t,x) does not automatically give a solution of its field equations.

The optical portal −F²/4+gp W Λ EμEμ/2 supplies an assumed way to transfer electromagnetic energy to Λ, with positive optical Hamiltonian when 1+gp WΛ>0. Its window W lies in the flat cabin. No measured gp or cold-carrier interaction determines this term. Retaining the canonical controller also retains an additional scalar outside the body; in that extended model the exterior is Einstein gravity **plus that scalar and Maxwell fields**, rather than pure vacuum gravity for every perturbation. The pure-cap theorem omits these additional fields.

The earlier seven-mode stiffness condition and large controller energy estimate were derived for the earlier unconfined construction. Their numerical or formal bounds cannot simply certify this new rank-changing finite interface. The finite construction requires a new coupled controller/material/payload analysis.

## What would make this a propulsion theory

A fully specified action is not sufficient evidence that its stress can be built, that its nonlinear dynamics are healthy, or that its stationary coordinate motion can be launched. The remaining logical dependencies are:

1. Prove or refute the full finite, curved 3D quadratic problem, including arbitrary transverse momenta and the constraint-rank transition. The planar theorem and massless all-R³ theorem do not cover their gluing.
2. Establish the nonlinear constraint count, evolution problem and boundary behavior where κ vanishes. Quadratic nonnegativity can hide modes with no quadratic kinetic term. Homogeneous wave speeds do not settle signal propagation after constraints are solved.
3. Identify a physical medium and source for H_AB and its negative wall stress; derive its couplings and experimentally bounded operating parameters. Calling it cold energy does not provide these data. No black-hole or horizon mechanism in the work currently supplies them.
4. Solve a finite-energy powered launch with the controller, source apparatus and payload backreaction. Derive the complete asymptotic energy and momentum budget from that same action. Prescribing V(t) is insufficient.
5. If a hypothetical carrier is to power the optical input, establish its existence, preparation, conversion channel, rate and losses. The earlier baryon-transfer/exhaust estimates were conditional on such additional interactions.

The transverse-momentum finite search has now been executed: the weak K=4 candidate shows negative kinetic directions, while stronger K=40,64,400 remove the large negatives in selected cases. The [numerical report](NUMERICS.md) records controls, residual near-zero negatives and threshold sensitivity. A weighted continuum constraint estimate for the stronger model is the next discriminator before a curved spherical stability claim. A useful physical test is identification of a carrier and an independently measurable interaction; equations with freely assigned source functions cannot substitute for it.

## Reproducibility and status

[The final exact run](run_v4/calculation/results.json) passes 29 identities. Earlier v1 and v2 are completed narrower runs. The retained v3 failure was a hand-entered sum-of-squares remainder coefficient, corrected from 3 to 4 for two transverse terms in v4; the spatial curvature expression and positive inequality did not change. All runs have frozen input/output manifests. The proofs receive an [adversarial self-review](REVIEW.md), not an independent review or novelty certificate.

The new result is a **constraint-first finite-phase candidate with rigorous flat and planar quadratic checks, adverse oblique evidence for its weak version, and a stronger version still under investigation**. The original physical theory remains incomplete for the reasons above. A working cold-energy drive has not been derived or demonstrated.
