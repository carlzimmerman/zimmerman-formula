# A replacement that repairs the exterior and passes the wall stress tests

2026-10-14. CGR-001–010. Base negative-kinetic obstruction: checkpoint `416fb583764a93d38443ee706d0709074b709b8d`. Actual run revisions, input hashes and limits are recorded separately in each manifest. Self-reviewed mathematics; no independent author review or experimental validation.

**The specified homogeneous-exterior negative-kinetic problem is repaired by an explicit new action.** After eliminating gravitational constraints, all six propagating exterior modes have positive quadratic energy for every nonzero wave number, with group speeds below c. The selected action also passes all 120 specified finite planar-wall Hamiltonian tests, including the high axial momenta that defeated earlier candidates. The prescribed background is preserved exactly. A complete three-dimensional finite wall, physical carrier and engine are still unproved.

## The selected action and its mechanism

Keep S0 and the framed strain density defined explicitly in [the base-action derivation](RETUNED_CANDIDATE.md), with **r = 1, Kc = 1, L = 4, μ = 2, A = 1**. Signature −+++, c = hbar = 1, reduced Planck mass Mp. Four scalar fields ΦA have invertible gradients and a timelike clock. The target is

\[
ds_*^2=-dt^2+dx^2+dy^2+[dz+b(x,y,z)dt]^2,
\qquad H_{AB}(\Phi)=M_p^2R_{AB}[g_*](\Phi).
\]

S0 is Einstein gravity plus `−H_AB(Φ)∂ΦA·∂ΦB/2`. This inverse-designed source encodes the target geometry. The strain terms, quadratic in the difference between the material inverse metric and its target, vanish with first variation on the background. They are not identified with observed cold particles.

The normalized clock, spatial projection, expansion and acceleration are

\[
U_\mu=-\frac{\partial_\mu\Phi^0}{\sqrt{-\partial\Phi^0\cdot\partial\Phi^0}},
\quad P^{\mu\nu}=g^{\mu\nu}+U^\mu U^\nu,\quad
\Theta=\nabla_\mu U^\mu,\quad
\mathfrak a_\mu=U^\nu\nabla_\nu U_\mu.
\]

Remove the original negative Q-square regulator and use

\[
\mathcal L_{\Theta,a}=
\frac{M_p^2}{2}[\Theta-\Theta_*(\Phi)]^2
+\frac{M_p^2}{2}\mathfrak a_\mu\mathfrak a^\mu,
\qquad \Theta_*=-\partial_z b.
\]

The target has unit lapse, Θ = −bz and acceleration zero, for arbitrary smooth static b. These new terms preserve the entire target solution, including its material equations. Their first functional variations vanish.

The final addition is **derivative elasticity of the spatial material strain**. With I,J = 1,2,3, define

\[
C^{IJ}=P^{\mu\nu}\partial_\mu\Phi^I\partial_\nu\Phi^J-\delta^{IJ},
\]

\[
\boxed{\mathcal L_C=\frac{M_p^2}{8}\sum_{I,J}
\left[(U^\mu\partial_\mu C^{IJ})^2
-\frac12P^{\mu\nu}\partial_\mu C^{IJ}\partial_\nu C^{IJ}\right].}
\]

The total selected action is S0 plus its specified strain density plus LΘ,a and LC, all under √−g. The sums include both off-diagonal orders. The assigned elastic wave-speed parameter is 1/√2. These are hypothetical couplings, not measured material constants.

In unitary gauge ΦA = xA, the exact ADM identities are

\[
C^{IJ}=\gamma^{IJ}-\delta^{IJ},\qquad
U\cdot\partial C^{IJ}=
\frac{\dot C^{IJ}-\beta^i\partial_i C^{IJ}}{N}.
\]

The spatial projection follows directly from `g^{ij}=γ^{ij}−βiβj/N²` and `U^i=−βi/N`. Thus this operator depends on the spatial metric and its first time derivative, with no lapse or shift time derivative in this gauge. Its covariant appearance does not warrant assuming a healthy theory, but its time-derivative content is explicit. The target spatial metric is the identity for **any b**, so C = 0 and ∂C = 0. LC and its first functional variations vanish on the entire target; the exact inverse source remains a solution.

Mechanically, the normalized expansion square cancels the negative trace part of the gravitational kinetic expression:

\[
K_{ij}K^{ij}-K^2+(K-K_*)^2
=K_{ij}K^{ij}-2KK_*+K_*^2.
\]

The acceleration term stiffens the lapse constraint. Derivative elasticity then gives the spatial material strain its own kinetic and gradient energy, preventing the reduced stiffness from dwindling with increasing wave number in the tested wall sectors. This is a changed action, not removing unwanted wavelengths or declaring them unphysical.

The cancellation is an exact **unreduced** kinetic identity; it does not by itself prove reduced wall positivity. The physical constraint reduction is part of the next results. The acceleration operator has established precedent in preferred-foliation theories ([Blas, Pujolàs and Sibiryakov, arXiv:0909.3525v1, equations 6–12](https://arxiv.org/pdf/0909.3525v1)); their different theory does not certify this action.

## Exact reduced exterior result

Work in the homogeneous exterior rest frame. Set D = Mp²/h, τ = t/√D, q = Dk² > 0, and Ω² = Dω². A dot below is a τ derivative. The vector direction can be rotated to z. Put hxx = hyy = 2ζ, hzz = 2(ζ+e), and Y = ζ+e.

Before derivative elasticity, exact lapse/shift elimination gives

\[
\mathcal L_{\rm base,scalar}
=\dot\zeta^2+\frac2{q+4}\dot Y^2
-\left(q+2+\frac2{q+1}\right)\zeta^2-2Y^2.
\]

The lapse α and scalar shift divergence b_s are `α=−2qζ/(1+q)` and `b_s=q dotY/(q+4)`. LC does not change these exterior constraints, since its linear material strain is −hij and its target derivative vanishes. Its scalar quadratic contribution is

\[
\Delta\mathcal L_{\rm scalar}
=\dot\zeta^2+\frac12\dot Y^2-\frac q2\zeta^2-\frac q4Y^2.
\]

Consequently the selected scalar kinetic and restoring matrices, in the (ζ,Y) basis, are diagonal:

\[
K=\operatorname{diag}\left(4,1+\frac4{q+4}\right),
\qquad
G=\operatorname{diag}\left(3q+4+\frac4{q+1},4+\frac q2\right).
\]

Both are strictly positive for every q > 0, with kinetic lower bounds independent of wave number. Their Hamiltonian is `p^T K^−1 p/2 + x^T G x/2`, hence positive for nonzero perturbations. No long-wavelength interval is discarded.

The full six-mode spectrum is

| Physical mode | Multiplicity | Ω² | Reduced kinetic coefficient |
|---|---:|---|---|
| Clock–gravity scalar | 1 | `3q/4+1+1/(q+1)` | 4 |
| Material scalar | 1 | `q/2+2` | `1+4/(q+4)` |
| Transverse vector | 2 | `q/2+32/(q+16)` | `1/2+4/(q+8)` |
| Transverse tensor | 2 | `3q/4+2` | 1 |

The vector and tensor normalizations match the specified off-diagonal metric amplitudes. All six are physical after eliminating lapse/shift. Exactly k = 0 SVT decomposition is excluded, with positive continuous frequency limits. Rotational symmetry extends this **homogeneous** calculation to every propagation direction.

For any Ω² = f(q), `vg²/c²=q[f'(q)]²/f(q)`. The clock branch has `−1/4<f'<3/4` and `f>3q/4`, giving `vg²/c²<3/4`. The vector has `3/8<f'<1/2` and `f>q/2`, giving `vg²/c²<1/2`. The other scalar and tensor similarly obey bounds 1/2 and 3/4. Thus every propagating exterior group speed is below c, analytically for all q > 0. In particular, the new tensor wave speed tends to √3/2 c in this hypothetical medium; **compatibility with observed gravity has not been established**.

This is a quadratic model calculation, not a causal-front or UV theorem. Its lapse constraint is elliptic; sub-light propagating group speeds do not exclude instantaneous constraint response. Preferred-foliation literature explicitly notes this distinction ([Ivanov and Sibiryakov, arXiv:1402.4964v2, footnote 4](https://arxiv.org/pdf/1402.4964v2)). No observational bounds from these historical papers are imported as current constraints.

## The wall tests that the final action passes

Use periodic planar target `b(x)=V sin(x/2)`, with flat target spatial metric and nonzero background curvature. Retain every spatial metric component, lapse and shift, all coefficient derivatives, the inverse Ricci source and mixed velocity/position terms. The full ADM quadratic form is reduced by a lapse/shift Schur complement; mixed terms are retained. Positive reduced kinetic A and restoring C give positive Hamiltonian by completing `(p−Bx)^T A^−1(p−Bx)/2+x^T Cx/2`.

CGR-010 covers exactly the same 120 cases that exposed failures in the preceding construction:

- N = 9, 17, 25 periodic collocation points;
- V = 0, 0.1, 0.3, 0.6;
- `(ky,kz)=(0,0),(0,1),(1,0),(1,1),(0.5,1),(1,0.5),(0,10),(0,20),(0,50),(0,100)`.

**All 120 reduced kinetic and restoring matrices are positive** at the declared numerical threshold. All 30 flat controls reproduce the independently derived six-mode spectrum with relative error below 10^−8. The run records the actual extrema, errors and input hashes in [results](elastic_wall_run_v1/calculation/results.json). CGR-009 independently derives the final homogeneous scalar/vector spectra and analytic speed inequalities; CGR-010 assembles the full metric action instead of substituting those spectra into the wall matrix.

Additional validation includes an independent Einstein-Hilbert ΓΓ-versus-ADM scalar Euler check and 30 exact rational nonzero-background local-jet checks of nonlinear extrinsic/source/clock/acceleration/strain expansions. These checks reduce sign/normalization risk; they are not an independent scientific review or a continuum wall proof.

The normalized Θ and projected Q squares agree through quadratic order on these exterior/planar targets because `Q=−Θ/N`, Θ* = 0, N* = 1. CGR-005 verifies that transfer. **A spherical wall generally has bz nonzero, so its normalized-Θ action needs a new reduced analysis.** The exact general-b background preservation does extend there; the planar stability tests do not.

This evidence is finite-dimensional and periodic. Collocation coefficient products may alias, and a few refinements do not prove continuum positivity. Selected transverse momenta are not an all-angle inhomogeneous theorem. The target is a wall control, not a finite physical interface or an accelerated craft.

## Failed constructions retained and why the action changed

| Construction | Decisive result | Response |
|---|---|---|
| Original negative regulator | Physical scalar kinetic determinant negative for all 0<q<L | Replace its sign and normalize the clock expansion |
| Positive regulator with Kc4,L100,A1.5 | Exterior energy positive; 24/48 high-axial wall cases have negative restoring energy | Retune the slow material/clock sector |
| Retuned Kc1,L4,A1 without LC | Exterior healthy; 15/120 wall cases still negative restoring energy | Add derivative elasticity, rather than exclude those momenta |
| Selected same coefficients plus LC | Exterior all-q energy/speed proof; 120/120 specified wall matrices positive | Next obligation is full 3D continuum wall/interface |

The old and retuned wall failures retained positive kinetic matrices; indefinite restoring energy is not automatically a proof of an imaginary-frequency instability when mixed terms are present. We use the stronger positive-Hamiltonian criterion throughout. No general no-go theorem follows from any row.

The earlier sign-only route also had unbounded high-q group speeds without lapse-gradient stiffness. The earlier fixed-D coefficient taper crossed a kinetic degeneracy at r = 2/3 before derivative elasticity was added. That taper obstruction belongs to that specified earlier family; it is **not** silently imported into the final extended action.

## Exact remaining implication

The original exterior ghost has an explicit mathematical repair and reproducible evidence. To turn it into a complete geometric source still requires:

1. A reduced **three-dimensional normalized-Θ continuum wall** calculation, with bz nonzero, physical interface conditions and control of all momenta. The new uniform kinetic bounds make a perturbative operator estimate a concrete next route, but no such theorem is asserted here.
2. An exterior/interface compatible with acceptable gravity, without strongly coupled or negative-energy confined modes; nonlinear preparation and evolution; constraint-sector causal response and a physical validity range.
3. A material realization, energy supply, craft backreaction, acceleration and conserved hardware/fuel budget. The steady target remains inverse-designed.
4. An actual interaction connecting this medium to the separately hypothesized χ/S baryon-conversion fuel. Identical terminology does not provide that connection.

No activation sphere curvature, black-hole/horizon trigger, or working cold-energy drive has been derived. This is a substantive replacement of the failed construction, not a claim that all propulsion requirements are complete.

Evidence: ten completed runs contain **638 mathematical assertions**, with all scientific counterexamples retained. One earlier failed implementation run is also preserved: SymPy could not decide an unsimplified positive relational expression, corrected by factoring in the next frozen script. Counts are not physical evidence. See [CURRENT.txt](CURRENT.txt), [reproduction](REPRODUCE.txt), [self-review](SELF_REVIEW.txt), [intermediate action 1](EARLY_CANDIDATE.md) and [intermediate action 2](RETUNED_CANDIDATE.md). No novelty or priority claim is made.
