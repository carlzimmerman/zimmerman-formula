> Intermediate coefficient retuning without derivative elasticity. CGR-008 found positive energy in105/120cases, with15negative restoring matrices. The action and its homogeneous-exterior proof below remain defined, but selected construction now adds the operator in [the current report](REPORT.md). All numerical details of these failures are retained.

# Repairing the coupled clock–gravity model

2026-10-14. CGR-001–008. Base obstruction checkpoint `416fb583764a93d38443ee706d0709074b709b8d`. Actual run revisions and source hashes are pinned in each manifest. Mathematical self-review; no independent author or experimental validation.

**Outcome:** an explicit replacement removes the old homogeneous-exterior negative-kinetic mode for every nonzero wave number, after including gravity and eliminating its lapse/shift constraints. The selected theory has positive quadratic energy for all six propagating exterior modes and group speeds below c. It preserves the prescribed background. A first replacement failed a further moving-wall energy test; that failure prompted the final coefficient change described here. This is progress on the requested obstruction, not completion of a physical cold-energy engine.

## The replacement action

Keep the [inverse source and framed strains](../cold_inverse_source_2026_10_14/REPORT.md). Use signature −+++, c = hbar = 1 and reduced Planck mass Mp. Four scalar fields ΦA have an invertible material-coordinate map and timelike clock. For the smooth static target

\[
ds_*^2=-dt^2+dx^2+dy^2+[dz+b(x,y,z)dt]^2,
\]

start from

\[
S_0=\int\sqrt{-g}\left[\frac{M_p^2R}{2}
-\frac12H_{AB}(\Phi)\partial\Phi^A\cdot\partial\Phi^B\right],
\qquad H_{AB}(\Phi)=M_p^2R_{AB}[g_*](\Phi).
\]

This explicitly encodes the chosen geometry. It is not an independently identified physical material. At ΦA = xA and g = g*, its stress is Mp²Gμν[g*], and all four material equations follow from the Bianchi identity with invertible field gradients. The preceding source computation also checked them directly.

Define `B^{AB}=g^{μν}∂μΦA∂νΦB`, `S^{ab}=θ^a_A θ^b_B [B^{AB}−g*^{AB}(Φ)]`, using target coframe `(dt,dx,dy,dz+b dt)`. In that target normal frame set `Ht=H00/h`, `ci=H0i/h`, `Hs,ij=Hij/h`, and `Bmat=L I−Hs`. The selected quadratic strain density is

\[
\begin{split}
\frac{\mathcal L_{\rm strain}}h={}&\frac{K_c-H_t}{8}(S^{00})^2
+\frac12S_0^TB_{\rm mat}S_0-\frac12S^{00}(c\cdot S_0)
-\frac\mu4\sum_{ij}(S^{ij})^2\\
&+\sum_i c_i\left[\sum_jS^{0j}S^{ij}-\frac12S^{0i}\operatorname{tr}S\right],
\qquad \boxed{K_c=1,\ L=4,\ \mu=2.}
\end{split}
\]

Here h > 0 is constant; choose D = Mp²/h, so r = hD/Mp² = 1. The source coefficients ci are distinct from the acceleration below.

Normalize the clock, then form its expansion and proper acceleration:

\[
U_\mu=-\frac{\partial_\mu\Phi^0}{\sqrt{-\partial\Phi^0\cdot\partial\Phi^0}},
\quad \Theta=\nabla_\mu U^\mu,\qquad
\mathfrak a_\mu=U^\nu\nabla_\nu U_\mu.
\]

Replace the old negative projected-clock-curvature square by

\[
\boxed{\mathcal L_{\rm repair}
=\frac{M_p^2}{2}[\Theta-\Theta_*(\Phi)]^2
+\frac{M_p^2}{2}\mathfrak a_\mu\mathfrak a^\mu,
\qquad \Theta_*=-\partial_zb.}
\]

The total action is S0 plus these strain and repair densities under √−g. The old negative Q-square term is removed. Every target coefficient is a function of Φ in the covariant action. On the target, Θ = −bz, the lapse is one, and the clock acceleration is zero. Each new square has zero background value and zero first functional variation; so do the strains. Thus the entire original background solution is preserved for arbitrary smooth static b. CGR-005 independently checks the expansion and acceleration using the four-dimensional connection.

## Why the problematic kinetic term changes

In unitary gauge ΦA = xA, Θ is the ADM extrinsic-curvature trace K. The gravitational kinetic terms combine exactly as

\[
K_{ij}K^{ij}-K^2+(K-K_*)^2
=K_{ij}K^{ij}-2KK_*+K_*^2.
\]

The negative trace square cancels. The remaining **unreduced** spatial-velocity Hessian is positive for positive lapse and positive spatial metric; the term involving K* is linear in velocity. No new time derivative of lapse or shift occurs in this gauge. This identity is not by itself positivity of the physical reduced Hamiltonian: the constraints still have to be solved. They are solved explicitly below for the exterior and numerically in the specified wall controls.

The acceleration term gives spatial stiffness to the lapse: `a_i=∂i ln N`. This operator is established in preferred-foliation theories; see [Blas, Pujolàs and Sibiryakov, arXiv:0909.3525v1, equations 6–12](https://arxiv.org/pdf/0909.3525v1). That theory has a different matter/constraint sector. Its parameter ranges do not certify ours.

Several frozen scripts use `Q=P^{μν}∇μ∇νΦ0`, rather than Θ. In unitary gauge `Q=−Θ/N`. On the homogeneous exterior and on all planar b(x) targets used here, Θ* = 0 and N* = 1. Thus `δQ=−δΘ` and their positive squares have identical quadratic actions on those backgrounds. CGR-005 checks this transfer. **It does not transfer a planar calculation to a spherical wall where bz is nonzero.**

## Exact physical exterior spectrum

Set τ = t/√D and q = Dk² > 0 in the homogeneous exterior rest frame. Align the wave vector with z, put hxx = hyy = 2ζ, hzz = 2(ζ+e), and denote lapse/shift scalars by α and b_s. Rotational symmetry covers every direction in this exterior.

For general coefficients the positive-regulator scalar Lagrangian, divided by a positive normalization, is

\[
\begin{split}
\mathcal L_2={}&-3\dot\zeta^2-2\dot\zeta\dot e+2\dot\zeta b_s
+q\zeta^2+2q\alpha\zeta
+\frac r2(3\dot\zeta+\dot e-b_s)^2\\
&+\frac{rK_c+Aq}{2}\alpha^2+\frac{rL}{2q}b_s^2
-r\mu(3\zeta^2+2\zeta e+e^2).
\end{split}
\]

The selected acceleration coefficient is A = 1. The exact constraint solutions are

\[
\alpha=-\frac{2q\zeta}{rK_c+Aq},\qquad
b_s=\frac{q[(3r-2)\dot\zeta+r\dot e]}{r(q+L)}.
\]

The reduced scalar kinetic determinant is `L(6r−4)/(q+L)`, replacing the old `L(4+6r)/(q−L)`. Its Kee entry is rL/(q+L). Hence K is positive for all q > 0 when r > 2/3. The potential has Gee = 2rμ and determinant

\[
\det G=4r\mu\left[\frac{2q^2}{rK_c+Aq}-q+2r\mu\right].
\]

The bracket numerator is `(2−A)q²+r(2μA−Kc)q+2r²μKc`. In particular `r>2/3`, `L,μ,Kc>0`, `0<A<2`, `Kc<2μA` is an open energy-positive family for all q > 0. The final selected constants lie inside it. No wavelength is cut out to obtain this statement.

For those selected constants, put Y = ζ+e. Both scalars diagonalize exactly:

\[
\mathcal L_{\rm scalar}
=\dot\zeta^2+\frac2{q+4}\dot Y^2-f(q)\zeta^2-2Y^2,
\qquad f(q)=q+2+\frac2{q+1}>0.
\]

Their Hamiltonian is

\[
\mathcal H_{\rm scalar}
=\frac{p_\zeta^2}{4}+\frac{q+4}{8}p_Y^2
+f(q)\zeta^2+2Y^2>0.
\]

The six reduced propagating modes have Ω² = Dω² as follows:

| Mode | Multiplicity | Ω² |
|---|---:|---|
| Clock–gravity scalar | 1 | `q+2+2/(q+1)` |
| Material scalar | 1 | `q+4` |
| Transverse vector | 2 | `q/2+4` |
| Transverse tensor | 2 | `q+4` |

The vector kinetic coefficient is `4/(q+8)>0`; tensor kinetic energy is positive. These are reduced physical modes, with lapse and shift eliminated. All arbitrarily small positive q are included. The exactly homogeneous k = 0 SVT decomposition is excluded, with continuous positive frequency limits as q → 0.

The independent computation of the Einstein-Hilbert scalar bulk action from linearized Christoffels matches the ADM Euler derivatives. A second full ADM matrix construction reproduces the six-mode flat dispersion on every specified grid momentum. Agreement is not being inferred solely from a self-substituted matrix formula.

## Group speeds and their limits

For the clock branch, `vg/c = sqrt(q) f'(q)/sqrt(f(q))` and `f'=1−2/(q+1)²`. For q > 0, `−1<f'<1` and `f>q+2`, so

\[
\frac{v_g^2}{c^2}=\frac{q[f'(q)]^2}{f(q)}
<\frac q{q+2}<1.
\]

The material scalar and tensors have |vg| < c; vectors have |vg| < c/√2. This is an analytic all-q group-speed statement for the homogeneous quadratic model. Negative group speed on part of the clock branch is dispersion, not a negative kinetic mode. Massive phase velocities need not be below c.

The exterior lapse constraint is elliptic. These propagating group-speed bounds do **not** establish front causality, exclude instantaneous constraint response, or supply a UV completion. Such distinctions matter in preferred-foliation models; see [Ivanov and Sibiryakov, arXiv:1402.4964v2, footnote 4](https://arxiv.org/pdf/1402.4964v2). We do not identify their theory with ours or import historical phenomenological bounds. Compatibility with measured gravity is unproved.

## Moving-wall tests and the failure that changed the coefficients

The inhomogeneous control is a periodic planar target `b(x)=V sin(x/2)`. The full ADM quadratic action retains all six spatial metric components, lapse, three shift components, coefficient gradients, inverse Ricci source, and mixed position/velocity terms. We eliminate the nondynamical fields by Schur complement. Positive kinetic and restoring matrices imply positive quadratic Hamiltonian even with mixed terms, by completing the canonical momentum square.

The first repaired coefficients were Kc = 4, L = 100, μ = 2, A = 3/2. Its exterior all-q positivity proof is retained in [the intermediate derivation](EARLY_CANDIDATE.md). Twelve planar and 45 low-transverse-momentum cases passed. A subsequent high-axial-momentum test found negative restoring eigenvalues in **24 of 48** cases, at V = 0.3 or 0.6. Kinetic matrices remained positive. This falsifies extrapolation of the earlier bounded wall passes; it does not undo the exterior proof or by itself establish exponentially growing frequencies.

That first choice has asymptotic vector and material speeds about 0.141c and 0.2c. The wall's background shift can outrun them. For example at N = 9, V = 0.3, kz = 10, the minimum restoring eigenvalue is −0.100314 while the minimum kinetic eigenvalue is +0.0138330. The final Kc = 1, L = 4, A = 1 choice raises the vector asymptotic phase speed to c/√2 and the other branches to c while preserving sub-light propagating group speeds and exterior energy positivity. This is a discriminating coefficient change, not a deletion of failed test cases.

CGR-008 tests this final choice at N = 9, 17 and 25; V = 0, 0.1, 0.3 and 0.6; and transverse momenta `(ky,kz)` equal to `(0,0)`, `(0,1)`, `(1,0)`, `(1,1)`, `(0.5,1)`, `(1,0.5)`, `(0,10)`, `(0,20)`, `(0,50)`, `(0,100)`. The completed result has105/120positivecases, with15negative restoringmatrices (allkineticpositive); its precise summary is recorded in [current results](retuned_wall_run_v1/calculation/results.json) and [current decision view](CURRENT.txt). Thirty flat controls compare the full six-mode spectrum against the independent analytic expressions, with relative tolerance 10^−8.

The nonzero-background extrinsic/source/clock/acceleration operators and the framed-strain expansion are also checked against nonlinear local ADM second variations at two exact rational jets (CGR-004, 30 assertions). They test the operator expansion independently of its flat spectrum. The coefficient changes multiply the same checked operators; the normalized regulator transfer applies because Θ* = 0 here.

These are **finite periodic planar** tests. Coefficient products use collocation and may alias. Grid refinements are not a continuum estimate; selected transverse momenta are not all directions. This target is a curvature control, not a physical finite wall, spherical bubble, or launch solution.

## What remains and what failed

A sign change alone, without lapse-gradient stiffness, produces positive exterior energy for selected parameters but unbounded high-q group speeds. That motivated the acceleration operator. A smooth fixed-D taper of h from r = 1 to zero crosses r = 2/3 where the reduced scalar kinetic determinant vanishes, then enters a negative region. This is an obstruction to that specific local taper family, not a theorem against every interface. Retaining the normalized expansion term in the vacuum changes the vacuum theory and mode count; it is not a demonstrated interface matching ordinary GR.

The requested **homogeneous negative-kinetic repair is supplied**. Still open toward a physical geometric source:

1. The full normalized-Θ spherical wall where bz is nonzero: derive and bound its reduced continuum operator, including elliptic constraints and coefficient gradients. The planar transfer is insufficient there.
2. A physical exterior/interface with acceptable gravity and no confined negative-energy or strongly coupled modes.
3. Nonlinear preparation/evolution, constraint-sector causal response, radiative/strong-coupling control and agreement with measured gravity.
4. Actual material realization, conserved fuel/hardware budgets, craft backreaction, and acceleration. The background is still inverse-designed and steady.
5. A derived interaction linking this medium to the hypothetical χ/S-to-neutron conversion. The separate exhaust budget does not provide that link.

The ratio r is a theory-coefficient choice, not activation at a particular sphere curvature. No horizon or black-hole trigger is derived. No working cold-energy drive is claimed.

Evidence, retained implementation failure, exact run counts and reproduction are in [CURRENT.txt](CURRENT.txt), [SELF_REVIEW.txt](SELF_REVIEW.txt), and [REPRODUCE.txt](REPRODUCE.txt). This is a replacement-construction checkpoint with explicit unresolved obligations, not completion of the physical propulsion program or a claim of novelty.
