# Powered clock equation and an exact constitutive compensation

Checkpoint CPC-001/002, 2026-10-15. This continues the proper-source action in
[CHB SOURCE](../cold_harmonic_boundary_2026_10_15/SOURCE.md) and the pure-core
current in [CLA PROOF](../cold_lapse_algebra_2026_10_15/PROOF.md). Their contents
are hashed as inputs in both computation manifests. Signature is −+++.
No derivative elasticity, acceleration square, shear regulator, or Θ square
is included. These statements apply to this specified action, not all cold-energy models.

## 1. Vary the clock in the complete controller action

Let E_A^μ ∂_μ Φ^B=δ_A^B, X=−(∂Φ⁰)²>0, U=−∂Φ⁰/√X,
P=g+UU, B^I=U·∂Φ^I, C^{IJ}=P∂Φ^I∂Φ^J−δ^{IJ}. Write

\[
S=\int\sqrt{-g}\left[{M^2R\over2}+F(\Phi^I,\Lambda,B,C)
-{F_c^2\over2}(\partial\Lambda)^2+A^I E_I^\mu\partial_\mu\Lambda\right],
\quad
A^I={M^2\Lambda\over4}(\partial_1\sigma^2,\partial_2\sigma^2,0)^I.
\]

Here F_c>0 is a constant. A is a vector of material coefficients; it is **not**
the constitutive stress coefficient A_IJ used in CHB. The material derivatives
of σ are taken with Λ held fixed. No coefficient depends explicitly on Φ⁰.

For δΦ⁰=π at fixed g, Λ and Φ^I, inverse-matrix differentiation gives

\[
\delta E_I^\mu=-E_0^\mu E_I^\nu\partial_\nu\pi.
\]

The pure-core variation is

\[
\delta F=-{P^{\mu\nu}\partial_\mu\Phi^I\over\sqrt X}
(F_{B^I}+2F_{C^{IJ}}B^J)\partial_\nu\pi.
\]

Therefore, after integration by parts, the exact total clock equation is

\[
\nabla_\nu\left[
{P^{\mu\nu}\partial_\mu\Phi^I\over\sqrt X}
(F_{B^I}+2F_{C^{IJ}}B^J)
+A^I(E_0^\mu\partial_\mu\Lambda)E_I^\nu\right]=0.
\]

The canonical Λ kinetic term has no clock variation at fixed metric and Λ.
In unitary gauge Φ^A=x^A, E_A^μ=δ_A^μ, P^{0μ}=0 and √X=1/N. Thus

\[
\boxed{\partial_i\left[N^2W^i+N\sqrt\gamma A^i\partial_t\Lambda\right]=0},
\qquad W^i=\sqrt\gamma\gamma^{ij}(F_{B^j}+2F_{C^{jI}}B^I).
\]

There is no time component of this clock current in this gauge. A dot means
coordinate ∂t in the material chart, not an invariant proper-time derivative.
The extra term cannot be omitted merely because the controller density itself
vanishes on a spatially homogeneous Λ(t): its clock variation is nonzero.

## 2. A simple ramp fails a necessary equation

On the instantaneous prescribed family N=1, γ=I, β=b e_z,
b=Λ(t)σ(x), B=B*=−b e_z, the core current is still

\[
W_*={M^2\over2}(\Psi_{xz},\Psi_{yz},-\Psi_{xx}-\Psi_{yy}),
\quad \Psi=b+b^3/3,
\quad \partial_iW_*^i=0.
\]

All spatial derivatives here are at the instantaneous uniform Λ. The clock
residual of this proposed ramp is exactly

\[
{M^2\Lambda\dot\Lambda\over4}\Delta_\perp(\sigma^2).
\]

For a nontrivial compact radial transition this Laplacian is not identically
zero. For example, restricting to z=0, an everywhere vanishing transverse
Laplacian would imply (s(σ²)_s)'=0; regularity and constancy outside would force
σ² constant on that plane. Hence Λ dotΛ≠0 fails the clock equation somewhere.
This is a failure of that ansatz, not a theorem forbidding acceleration.

There is a stronger local issue for lapse-only perturbations. For Λ≠0,
consider the radial wall's equatorial streamfunction
χ=−M²s Λ(1+Λ²σ²)σ_s/2. A smooth nondecreasing transition from 0 to 1
has a nonzero interior extremum of χ. At that extremum s>0, σ_s>0,
W*=0 and Ψ_ss+Ψ_s/s=0. Direct substitution gives

\[
\left.\partial_i A^i\right|_{\rm center}
={M^2\Lambda\sigma_s^2(1-\Lambda^2\sigma^2)
\over2(1+\Lambda^2\sigma^2)}.
\]

It is nonzero when |Λσ|<1. For N=1+εn, dotΛ=εv and the ansatz
β=NΛσ e_z (so B=B*), the order-ε clock equation is
2W*·∇n+v div A=0. Its first term vanishes at that center and its second
does not. Thus a regular perturbative lapse adjustment **alone** cannot repair
this particular ramp. This does not cover arbitrary lapse/shift/strain changes.

## 3. A compact shift correction solves the clock equation exactly

At γ=I, write q=B−B*. The specified constitutive completion is
F=F0+f·q+2h q² at C=0, with F_C=A_tensor=(F0 I−S*)/2.
Consequently the exact, affine response is

\[
W=W_*+Lq,\qquad L=4hI+F_0I-S_*.
\]

For the spatially homogeneous instantaneous controller, choose N=1 and

\[
\boxed{q=-\dot\Lambda L^{-1}A,\qquad
\delta\beta=+\dot\Lambda L^{-1}A.}
\]

Then W+dotΛ A=W* and its divergence vanishes identically. This statement is
exact for the clock equation, without truncating in dotΛ. It uses the full
quadratic constitutive completion; a different F changes the response.
The correction generally has transverse components and need not be purely
transverse, because L can mix longitudinal and transverse directions.

Invertibility is a stated condition, not automatic. For a bounded Λ interval,
the source jets are smooth, bounded and supported in a compact wall K.
Choose h with a positive plateau on a neighborhood of K and large enough that
4h≥||F0 I−S*||op+κ there, with κ>0. Then L≥κI on K. A vanishes off K;
the correction extends smoothly by zero through a collar before h tapers to
zero. No division by h at the vacuum interface is required. Pointwise,

\[
|\delta\beta|\le |\dot\Lambda|\,|A|/\kappa.
\]

This constructs admissible clock-current kinematics, not a solution of the
Einstein or controller equations. The choice of h is allowed by this inverse
source model; its physical realization is still unknown.

## 4. Backreaction and the other equations remain mandatory

At N=1, γ=I, the **core** normal-frame stress changes exactly by

\[
\delta\rho=4h B_*\cdot q+2h q^2,\quad
\delta j_i=-4h q_i,\quad
\delta S_{ij}=(f\cdot q+2h q^2)\delta_{ij}.
\]

These follow from ρ=F_B·B−F, j=−F_B and S=F I−2F_C.
They are not guaranteed to match the Einstein tensor of the corrected shift.
For homogeneous Λ, the canonical controller adds
ρ_Λ=F_c² dotΛ²/2, j_Λ=0 and S_Λ=F_c² dotΛ² I/2.
The J·∂Λ density and its metric variation vanish in this homogeneous unitary
configuration because J⁰=0 and ∂iΛ=0.

At fixed B,C before target substitution,

\[
F_\Lambda-F_{\Lambda*}=(f_\Lambda-4h B_{*\Lambda})\cdot q.
\]

The independent controller equation on this homogeneous ansatz therefore is

\[
F_c^2[-\ddot\Lambda+\dot\Lambda\,\partial_i\beta^i]
+(f_\Lambda-4hB_{*\Lambda})\cdot q=0.
\]

Here the stationary identity F_Λ*=div A cancels the background source.
This is a spatially resolved condition, not an ordinary acceleration law that
has been solved by choosing q. Neither it nor the ten metric equations can be
discarded after solving the clock equation.

## 5. Uniform control is not a finite-energy launch

For constant F_c>0, a spatially uniform nonzero dotΛ has canonical energy

\[
E_\Lambda(B_R)={2\pi\over3}F_c^2\dot\Lambda^2R^3\longrightarrow\infty.
\]

Outside the compact material source, all other candidate matter coefficients
vanish, whereas this positive kinetic density remains. It cannot be canceled
by a finite wall contribution. In the homogeneous exterior the controller
wave equation also requires ddotΛ=0 for N=1, γ=I and constant exterior shift.
Thus a uniform ramp is a local diagnostic and is not the proposed finite-energy
engine operation. A physical continuation needs spatially localized controller
data, the full coupled gravitational response, and a finite energy budget.

## Computational evidence

[Clock run v1](run_v1/calculation/results.json): 26 exact checks of inverse
Jacobian variation, variation sign via a direct perturbed clock, geometric
residual, center forcing, affine response, and compensation. A positive definite
rational response matrix checks the compensation sign; it does not establish
positivity of the actual wall's L. The plateau argument above supplies a
conditional analytical construction of positive L.

[Stress run v1](stress_run_v1/calculation/results.json): 9 exact checks of stress
response, differentiation at fixed B, the scalar wave operator, and the
infinite-volume energy formula/limit. The analytic compactness and radial
extremum arguments are proofs in this file, not finite numerical scans.
