# Constraint-first localization: exact quadratic results

2026-10-15. Signature −+++, reduced Planck mass M, Frobenius norms count off-diagonal entries twice. These are self-reviewed quadratic theorems about specified actions. They do not prove nonlinear stability, a causal initial-value problem, a microscopic material, or powered propulsion.

## 1. The massless finite cap on all of R³

Let ΦA be four scalar material coordinates with invertible Jacobian and timelike clock Φ0. Define

\[
U_\mu=-{\partial_\mu\Phi^0\over\sqrt{-(\partial\Phi^0)^2}},\quad
P^{\mu\nu}=g^{\mu\nu}+U^\mu U^\nu,\quad
C^{IJ}=P^{\mu\nu}\partial_\mu\Phi^I\partial_\nu\Phi^J-\delta^{IJ},\quad
\Theta=\nabla_\mu U^\mu.
\]

Consider the covariant density

\[
\mathcal L={M^2\over2}R+{M^2\over2}\theta(\Phi)\Theta^2
+{M^2\over8}\kappa(\Phi)\sum_{IJ}
[(U\cdot\partial C^{IJ})^2-s^2(\Phi)P^{\mu\nu}\partial_\mu C^{IJ}\partial_\nu C^{IJ}].
\]

Here θ and κ are smooth bounded nonnegative functions of the three spatial material coordinates, with compact support. Assume 0<smin²≤s²≤1. There is **no** inverse Ricci source, strain mass, acceleration-square term, pump or payload in this theorem. Minkowski metric and ΦA=xA solve the field equations: C=Θ=0 and every added first variation vanishes. Outside the constitutive support the gravitational action is exactly Einstein's action and the material coordinates decouple.

Work in unitary gauge Φ=x. Put Qij=δγij, α=δN, v=δβ, u=Qdot, and Dv=∂ivj+∂jvi. Exactly C=γinverse−I; at first order C=−Q. The added terms contain no lapse or shift velocity. In this flat background they also supply no quadratic α² or ∇α². The lapse is therefore a multiplier imposing

\[
\mathcal R_1(Q)=\partial_i\partial_jQ_{ij}-\Delta\operatorname{tr}Q=0.
\]

A smooth solution satisfies the same constraint for u. The spatially integrated quadratic Lagrangian consists of

\[
{M^2\over8}\int[|u-Dv|^2-(\operatorname{tr}u-2\operatorname{div}v)^2
+\theta(\operatorname{tr}u-2\operatorname{div}v)^2
+\kappa(|u|^2-s^2|\nabla Q|^2)]
+L_{R,2}+{M^2\over2}\int\alpha\mathcal R_1(Q).
\]

All identities below first hold for smooth sufficiently decaying fields satisfying the constraint, then extend wherever the stated quadratic forms are defined. The zero Fourier point has measure zero in these R³ finite-energy identities; independent homogeneous infinite-volume modes are not inserted.

**Decomposition.** For k≠0 rotate k to the z direction. The constraint says Qxx+Qyy=0. Thus Q uniquely decomposes, up to the usual zero-frequency/gauge qualifications, as

\[
Q=Q^{TT}+D\xi,\qquad \operatorname{div}Q^{TT}=0,\quad\operatorname{tr}Q^{TT}=0.
\]

The three entries Qxz,Qyz,Qzz are supplied by ξ, and Qxx=−Qyy,Qxy are TT. The same decomposition holds for u. With u=uTT+Dζ, and w=v−ζ, Parseval and integration by parts give

\[
{1\over8}\int[|u-Dv|^2-(\operatorname{tr}u-2\operatorname{div}v)^2]
={1\over8}\|u^{TT}\|_2^2+{1\over4}\|\nabla\times w\|_2^2.
\]

Indeed ∫|Dw|²=2∫|∇w|²+2∫(div w)² and ∫|curl w|²=∫|∇w|²−∫(div w)². The θ term is nonnegative even when θ varies spatially. The choice v=ζ makes both this curl term and the θ square zero **everywhere**, so the minimum is attained in the homogeneous gradient energy class. The κ term has no v dependence at this order. Uniqueness of v is neither needed nor asserted.

The integrated spatial Einstein quadratic action, on the constraint surface, is

\[
L_{R,2}=-{M^2\over8}\|\nabla Q^{TT}\|_2^2.
\]

This follows either by substituting the same Fourier decomposition into the Cartesian quadratic curvature form, or by its integrated spatial gauge invariance. The executable check derives the Fourier identity directly.

Consequently the **exact** reduced quadratic action on the constraint space is

\[
L_{2,\rm red}={M^2\over8}\left[\|\dot Q^{TT}\|_2^2-\|\nabla Q^{TT}\|_2^2
+\int\kappa(|\dot Q|^2-s^2|\nabla Q|^2)\right].
\]

Its energy is

\[
E_2={M^2\over8}\left[\|\dot Q^{TT}\|_2^2+\|\nabla Q^{TT}\|_2^2
+\int\kappa(|\dot Q|^2+s^2|\nabla Q|^2)\right]\ge0.
\]

This proves nonnegative quadratic energy for arbitrary three-dimensional perturbations in this precisely defined finite, flat phase, with ordinary Einstein exterior. It is conserved for existing smooth finite-energy solutions with zero flux at infinity. It is a **seminorm** on the full Q space: material-coordinate perturbations in the κ=0 exterior can be gauge null directions. No uniform coercivity for all six unconstrained metric entries, no existence theorem across the degenerate boundary, and no nonlinear degree-of-freedom count follows from this identity.

For constant κ>0 the homogeneous physical branches are two tensors with squared normal speed (1+κs²)/(1+κ), two material vectors with squared speed s², and one material scalar with squared speed s². The transverse scalar removed by the lapse constraint is absent. At s²=1 all five branches are luminal in this homogeneous quadratic calculation. This is an explicit change from the previous s²=1/2 coefficient, not a re-interpretation of its subluminal tensor result. Spatially variable coefficients and elliptic constraint elimination require a separate causal/well-posedness analysis.

## 2. Removing the auxiliary masses before tapering

Return temporarily to homogeneous flat medium with θ=1, κ=4, s²=1/2. Let the strain mass h>0 vary as a parameter; in these formulas set M=1 and nondimensionalize distances with a fixed reference length, so h and k are dimensionless. Set the dimensionless acceleration coefficient A=h in these reference units. Thus A and h both approach zero; they are distinct dimensional coefficients before normalization. The original reference point is h=A=1.

For scalar velocity diag(a,a,c), the joint velocity/shift form is

\[
J={2a^2+(c-2kv)^2\over8}+{2a^2+c^2\over2}+2hv^2.
\]

Every term is nonnegative, uniformly in h≥0. For h>0 and k≠0 the reduced velocity matrix is

\[
K=\operatorname{diag}\left({5\over2},{k^2+5h\over k^2+4h}\right)>0.
\]

The lapse has coefficient (h+A k²)/2 and couples linearly as αk²a in the static action. Eliminating it adds the positive stiffness k⁴a²/[2(h+A k²)] to the energy. With A=h, the squared frequencies are

\[
\omega_a^2={k^2+4h+2k^4/[h(1+k^2)]\over5},\quad
\omega_c^2={(h+k^2/2)(k^2+4h)\over k^2+5h},
\]

\[
\omega_V^2={(h+k^2/2)(k^2+8h)\over k^2+10h}\quad(\text{twice}),\qquad
\omega_T^2={3k^2+4h\over5}\quad(\text{twice}).
\]

These are positive for h>0, all k²≥0. At fixed nonzero k, hωa²→2k⁴/[5(1+k²)]>0: the transverse scalar becomes infinitely stiff as the lapse multiplier is restored. At h=A=0 the lapse equation imposes a=0 for k≠0; the remaining branches match the constrained cap with κ=4. The k→0 and h→0 limits are nonuniform. This is not a uniformly regular adiabatic operation, and it does not establish that a physical controller can change these constitutive coefficients.

This explicitly avoids the previous common-taper ghost. It is a path of actions/local constitutive states, not yet a time-dependent solution in one microscopic theory.

## 3. A complete spatially staged planar interface

The prior section alone would not justify a spatial interface. The following separate result does.

Continue in the M=1 normalized units. Take flat background, fields depending on t,z only, and energy **per unit transverse area**. Choose smooth nonnegative strain h(z) and acceleration A(z) supported in [−L,L]. Let θ=1 and κ=4 on that whole interval. Outside it let θ,κ smoothly taper to zero with compact support. Keep s²=1/2. No inverse Ricci source is present. The mass terms are hα²/2+2h|v|²−h|Q|²/2, with acceleration A(α′)²/2. Work with sufficiently smooth decaying admissible solutions, or quadratic forms for which the auxiliary minimization exists. No division through a zero auxiliary mass is permitted.

Write

\[
Q=\begin{pmatrix}a+t&s&x\\s&a-t&y\\x&y&c\end{pmatrix}.
\]

Outside [−L,L], the lapse equation is a″=0. Decay on each exterior half-line forces a=0 there; smoothness gives a′=0 there too. The same holds for adot. The integrated Einstein spatial action is

\[
L_{R,2}=\int[(a')^2-(t')^2-(s')^2]/4.
\]

Inside [−L,L], θ=1 completes the kinetic numerator to |u−Dv|²/8, with the additional κ|u|²/8 and positive shift mass. Outside, adot=0 and the Einstein kinetic form itself is

\[
[\dot t^2+\dot s^2+(\dot x-v_x')^2+(\dot y-v_y')^2]/4\ge0.
\]

The remaining θ square and κ kinetic terms are nonnegative. Hence eliminating shift cannot introduce negative kinetic energy.

For the static form, inside the interval

\[
-L_{R,2}+\kappa s^2|Q'|^2/8\ge |Q'|^2/8,
\]

as a direct sum of squares. Outside, a′=0 and this same static energy is

\[
{1+\kappa s^2\over4}[(t')^2+(s')^2]
+{\kappa s^2\over4}[(x')^2+(y')^2]
+{\kappa s^2\over8}(c')^2\ge0.
\]

Add h|Q|²/2. The lapse-only quadratic form is nonnegative; its static elimination, when finite, only subtracts from the Lagrangian and therefore adds to the energy. Where it is a multiplier its constraint has already been imposed. Thus the full reduced planar quadratic energy is nonnegative. It is conserved for stationary profiles and existing smooth solutions without net flux at infinity. This establishes a spatially varying interface check including all six metric components and both types of auxiliaries, rather than an interpolation of dispersion relations.

It is an infinite planar slab, not a finite three-dimensional body. Arbitrary transverse momenta, a spherical boundary, and the curved moving core are **not** covered by this planar theorem. Nor does nonnegative energy establish well-posed evolution where material kinetic density vanishes. Those are substantial remaining obligations.
