> Historical intermediate candidate, Kc4,L100,A1.5. CGR-006 subsequently found negative potential eigenvalues in24/48 high-axial-momentum wall cases. Its all-q homogeneous-exterior proof remains valid, but selected coefficients have been replaced; see [current report](REPORT.md). This file retains the intermediate derivation.

# A replacement for the failed clock–gravity construction

2026-10-14. CGR-001 through CGR-005. Mathematical self-review; no independent reviewer or physical validation. Starts from the failure recorded at checkpoint `416fb583764a93d38443ee706d0709074b709b8d`; actual run revisions are pinned separately in each manifest.

**Result:** there is an explicit replacement action that removes the previous negative-kinetic mode in the homogeneous exterior. All six reduced propagating modes have positive quadratic energy for every nonzero wave number, with group speeds below c. The prescribed background is preserved. Finite periodic planar-wall calculations also give positive reduced energy in all 57 cases tested, including oblique perturbations. These are a substantive repair of the specified obstruction, not a complete finite bubble, an empirically viable gravity theory, identified cold fuel, or a propulsion device.

## 1. The selected replacement action

Keep the [previous inverse source and strain definitions](../cold_inverse_source_2026_10_14/REPORT.md). Signature −+++, c = hbar = 1; Mp is the reduced Planck mass. Four scalar fields ΦA provide a timelike clock and invertible material-coordinate map. Set

\[
S_0=\int\sqrt{-g}\left[\frac{M_p^2}{2}R
 -\frac12 H_{AB}(\Phi)\partial_\mu\Phi^A\partial^\mu\Phi^B\right],
\quad H_{AB}(\Phi)=M_p^2R_{AB}[g_*](\Phi).
\]

The target is `ds*² = −dt² + dx² + dy² + [dz+b(x,y,z)dt]²`, with arbitrary smooth static b. The earlier bubble profile is one choice. H explicitly encodes its target geometry. This is an inverse-designed theory, not independently observed matter.

Use the same quadratic strain interactions as the prior source, with **Kc = 4**, **L = 100**, **μ = 2**, instead of Kc = 10^12. Keep h > 0 constant and choose D = Mp²/h. For completeness, in the target normal frame write Ht = H00/h, ai = H0i/h, Hs,ij = Hij/h and B = L I − Hs. With S00, S0i, Sij the framed inverse-metric strains, the added strain density is

\[
\frac{\mathcal L_{\mathrm{strain}}}{h}
=\frac{K_c-H_t}{8}(S^{00})^2
+\frac12 S_0^TBS_0-\frac12S^{00}(a\cdot S_0)
-\frac\mu4\sum_{ij}(S^{ij})^2
+\sum_i a_i\left[\sum_jS^{0j}S^{ij}-\frac12S^{0i}\operatorname{tr}S\right].
\]

Here ai denotes a **source coefficient**, not the clock acceleration defined next; the numerical scripts use Hn for this coefficient to avoid confusion. Strains are `S^{ab}=θ^a_A θ^b_B [g^{μν}∂μΦA∂νΦB−g*^{AB}(Φ)]`, with target coframe `(dt,dx,dy,dz+b dt)`.

Normalize the clock and introduce its expansion and proper acceleration:

\[
U_\mu=-\frac{\partial_\mu\Phi^0}{\sqrt{-\partial\Phi^0\cdot\partial\Phi^0}},
\quad \Theta=\nabla_\mu U^\mu,\quad
\mathfrak a_\mu=U^\nu\nabla_\nu U_\mu.
\]

**Replace the old negative Q-square regulator** by

\[
\boxed{\mathcal L_{\rm repair}
=+\frac{M_p^2}{2}[\Theta-\Theta_*(\Phi)]^2
 +\frac{3M_p^2}{4}\mathfrak a_\mu\mathfrak a^\mu,
\qquad \Theta_*=-\partial_z b.}
\]

The total action is S0 plus the strain and repair densities under √−g. There is no remaining old negative Q-square term. All functions of the target coordinates are functions of Φ in this covariant definition.

The target lapse is one. Its normalized expansion is −bz and its acceleration is zero, even for general b(x,y,z). Thus both new terms and their first functional variations vanish on the target; quadratic strains do too. All background Einstein and material-field equations remain exactly those of S0 and retain the preceding solution. This claim does not require treating the curvature as an external force after variation.

## 2. Why this changes the kinetic problem

In unitary gauge ΦA = xA, use ADM lapse N, shift β and spatial metric γ. The normalized expansion is the trace K of the extrinsic curvature. The Einstein kinetic term and the new square combine exactly:

\[
K_{ij}K^{ij}-K^2+(K-K_*)^2
=K_{ij}K^{ij}-2KK_*+K_*^2.
\]

The negative K² piece cancels. The remaining quadratic spatial-velocity form is positive for N > 0 and positive γ. In an orthonormal frame its Hessian with respect to `(Kxx,Kyy,Kzz,Kxy,Kxz,Kyz)` is proportional to `diag(1,1,1,2,2,2)`. The K* term is linear in velocity. None of the inverse source, strain potential, or acceleration term adds a lapse time derivative in this gauge. This is an exact **unreduced** kinetic identity. Eliminating lapse/shift can still change physical energy, so the next calculation is essential; this identity alone is not a full wall-stability theorem.

The acceleration term is geometric: in ADM, `a_i = ∂i ln N`. It adds spatial stiffness to the lapse constraint. It is an established operator type in preferred-foliation theories; see [Blas, Pujolàs and Sibiryakov, arXiv:0909.3525v1, equations 6–12](https://arxiv.org/pdf/0909.3525v1). Our extra material strain sector and inverse source differ, so that paper does not certify this construction or supply its parameter conditions.

The frozen runs CGR-001/002/003 first used a positive Q-square rather than normalized Θ. In unitary gauge `Q = −Θ/N`. Their backgrounds have N = 1 and Θ* = 0 (the homogeneous exterior and planar b(x) target). Hence `δQ = −δΘ`, and the two square regulators have **identical quadratic actions on precisely those backgrounds**. CGR-005 verifies the transfer and the general-b source preservation. On a spherical wall with bz nonzero their quadratic actions differ; the planar evidence is not silently extended there.

## 3. Full reduced exterior proof

Use the homogeneous exterior rest frame and define τ = t/√D, q = Dk² > 0, r = hD/Mp² = 1. A dot is a τ derivative. Align the wave vector with z and set hxx = hyy = 2ζ, hzz = 2(ζ+e). Rotational symmetry covers every direction. Lapse α and scalar shift divergence b_s are nondynamical.

With general positive parameters and acceleration coefficient A, the candidate positive-regulator scalar action is

\[
\begin{split}
\mathcal L_2={}&-3\dot\zeta^2-2\dot\zeta\dot e+2\dot\zeta b_s
+q\zeta^2+2q\alpha\zeta
+\frac r2(3\dot\zeta+\dot e-b_s)^2\\
&+\frac{rK_c+Aq}{2}\alpha^2+\frac{rL}{2q}b_s^2
-r\mu(3\zeta^2+2\zeta e+e^2).
\end{split}
\]

Here A = 3/2. Eliminating both constraints gives

\[
\alpha=-\frac{2q\zeta}{rK_c+Aq},\qquad
b_s=\frac{q[(3r-2)\dot\zeta+r\dot e]}{r(q+L)}.
\]

The scalar kinetic determinant changes from the old `L(4+6r)/(q−L)` to

\[
\det K=\frac{L(6r-4)}{q+L}.
\]

For r > 2/3 its diagonal entry Kee = rL/(q+L) is positive, so K is positive definite for every q > 0. This is a change of the action and couplings, not a deletion of the offending modes.

The scalar potential determinant is

\[
\det G=4r\mu\left[\frac{2q^2}{rK_c+Aq}-q+2r\mu\right].
\]

The bracket has numerator `(2−A)q²+r(2μA−Kc)q+2r²μKc`. Thus, for example, the open parameter family `r>2/3`, `L,μ,Kc>0`, `0<A<2`, `Kc<2μA` has positive scalar K and G for all q > 0. Gee = 2rμ > 0. The selected constants lie strictly inside this energy-positive family; energy positivity is not an isolated equality at a chosen wave number. This family statement concerns the exterior quadratic model only.

At the selected constants define Y = ζ+e. The entire reduced scalar action diagonalizes:

\[
\mathcal L_{\rm scalar}
=\dot\zeta^2+\frac{50}{q+100}\dot Y^2
-f(q)\zeta^2-2Y^2,\qquad
f(q)=\frac{q^2+4q+32}{3q+8}.
\]

Its Hamiltonian is

\[
\mathcal H_{\rm scalar}
=\frac{p_\zeta^2}{4}+\frac{q+100}{200}p_Y^2
+f(q)\zeta^2+2Y^2>0
\]

for any nonzero perturbation at q > 0. In particular

\[
f(q)=\frac{28}{9}+\frac{(3q-8)^2}{9(3q+8)}\ge\frac{28}{9}>0.
\]

There is no hidden long-wavelength negative energy left in these reduced exterior scalars. Unlike the previous band-only test, this includes arbitrarily small positive q. The exact homogeneous k = 0 SVT decomposition is excluded; the displayed frequencies have continuous positive limits there.

The dimensionless squared frequencies Ω² = Dω² are

| Modes | Multiplicity | Ω² | Kinetic sign |
|---|---:|---|---|
| Clock–gravity scalar ζ | 1 | `(q²+4q+32)/(3q+8)` | positive |
| Material scalar Y | 1 | `q/25+4` | positive |
| Transverse vector | 2 | `q/50+4` | positive; coefficient `100/(q+200)` |
| Transverse tensor | 2 | `q+4` | positive |

These are physical modes after lapse/shift elimination, not coordinate perturbations being counted as cures.

## 4. Propagating group speeds

For Ω² = f(q), `vg/c = sqrt(q) f'(q)/sqrt(f(q))`. Here

\[
f'(q)=\frac13-\frac{256}{3(3q+8)^2}.
\]

It increases from −1 to 1/3 and vanishes at q = 8/3. On `0<q≤8/3`, f ≥ 28/9 and |f'| ≤ 1, giving `vg²/c² ≤ 6/7 < 1`. On `q≥8/3`, f > q/3 and `0≤f'<1/3`, giving `vg²/c² < 1/3`. The other scalar, vector and tensor branches respectively have |vg| < 0.2c, c/√50, and c. The bounds are analytic for all q > 0 in this quadratic exterior, not inferred from finite samples. Negative group speed on part of the clock branch is dispersive backward propagation, not negative kinetic energy.

This does **not** prove a causal front, absence of instantaneous interactions, a UV completion, or a relativistic local response of the constraint sector. The lapse constraint is elliptic. Preferred-foliation literature explicitly distinguishes propagating modes and instantaneous interactions; see [Ivanov and Sibiryakov, arXiv:1402.4964v2, footnote 4](https://arxiv.org/pdf/1402.4964v2). Its theory is not identical to this one. No current observational bound is borrowed from either historical paper, and no claim of compatibility with measured gravity is made.

## 5. What happens in a spatially varying wall control

We also expanded the **full ADM action**, including its nonzero-background extrinsic curvature and the inverse Ricci source. For a periodic planar target `b(x)=V sin(x/2)`, use Fourier collocation at N = 9, 17 and 25 points. Retain all six spatial metric components, all four lapse/shift variables, and all mixed velocity/position terms. Reduce the full quadratic form by a lapse/shift Schur complement.

- CGR-002: transverse momenta zero, V = 0, 0.01, 0.1, 0.3: all **12** reduced kinetic and potential matrices positive.
- CGR-003: `(ky,kz)=(0,1),(1,0),(1,1),(0.5,1),(1,0.5)`, V = 0, 0.3, 0.6: all **45** reduced kinetic and potential matrices positive.
- At V = 0, the independent full ADM discretization reproduces all six analytic dispersions at every grid momentum, with relative errors below 10^−8 (actual errors recorded in outputs are near floating-point precision).
- CGR-004 checks the nonzero-background extrinsic-curvature, inverse-source, clock-regulator, acceleration, and framed-strain expansions against independent second variations of nonlinear local ADM expressions at two exact rational jets. All 30 assertions pass. This addresses correlated sign errors that a flat control alone could miss.

Positive reduced kinetic A and restoring C are sufficient for positive quadratic Hamiltonian even with the retained mixed term: `H = (p−Bq)^T A^−1(p−Bq)/2 + q^T Cq/2`. The numerical statement is finite-dimensional, stationary, and planar. The periodic target is a curvature control, not a finite physical bubble/interface. Collocation coefficient products have aliasing; a few grid refinements do not prove continuum positivity. Perturbation directions are sampled, not exhaustively reduced to an all-angle wall theorem.

## 6. Failed alternatives and remaining work

**Sign reversal and clock retuning alone:** scalar energy becomes positive, but without the acceleration term the clock frequency is `4−q+q²/2`; group speed grows without bound at high q. That fails the chosen group-speed objective. The acceleration term replaces this k^4 growth by the rational f(q) above.

**Simply tapering the repair away:** a continuous fixed-D taper of h from the repaired r = 1 phase to r = 0 crosses r = 2/3 where det K vanishes, and enters a negative-kinetic region at `0<r<2/3`. This is an obstruction to that fixed-coefficient local taper family, not to every physical interface. Derivative/interface terms can change the operator and must be derived rather than ignored. Keeping Mp²(Θ−Θ*)²/2 outside while h vanishes changes the vacuum theory and mode count; it is not a demonstrated GR-matching interface.

The **original homogeneous negative-kinetic obstruction is repaired** by the construction in sections 1–4. The remaining implications to a physical geometric engine are substantial:

1. Full spherical target with bz nonzero: derive the normalized-Θ reduced three-dimensional wall operator, retaining coefficient gradients and the elliptic constraints; prove continuum positivity or find its failure.
2. Physical exterior/interface: construct matching to an acceptable vacuum and test its localized modes, without treating finite numerical boxes as hardware or cutting out wavelengths.
3. Nonlinear preparation/evolution, strong coupling, constraint-sector causal response, and compatibility with observed gravity: not established by a quadratic Hamiltonian.
4. Actual material realization, controllable energy supply, craft backreaction and acceleration: not provided. The prescribed metric still encodes a chosen steady geometry.
5. No interaction connects this medium to the hypothetical χ/S conversion source. The separate propulsion budgets cannot be joined to it by relabeling both as cold energy.

The condition r > 2/3 is a ratio of assigned theory coefficients, not an activation radius or a sphere-curvature threshold. No horizon or black-hole trigger is derived.

## 7. Evidence status

**194 assertions** pass across five completed runs: 68 analytic exterior checks, 19 planar checks, 64 oblique checks, 30 nonlinear-jet checks, and 13 normalized-regulator checks. The first analytic run is retained as a failed implementation run: SymPy could not infer an unsimplified positive expression; v2 factors it before testing. No mathematical counterexample was suppressed. The claim rests on the derivations and stated finite tests, not assertion totals.

See [current decision view](CURRENT.txt), [reproduction](REPRODUCE.txt), and [self-review](SELF_REVIEW.txt). This checkpoint supplies a replacement and its evidence; it does not declare the larger propulsion program complete. No priority or novelty claim is made.
