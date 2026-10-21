# Effective binding mechanism in the explicit alternative action

The added neutral mediator supplies a concrete classical attraction in this **alternative matter action**. The audited local expansion is

\[
V_{\rm loc}(I)=I-0.01 I^2+0.0001 I^3+2.875\times10^{-8}I^4+O(I^5),\qquad I=|\Psi|^2.
\]

The attractive quartic and higher-density stabilization explain why charged, self-bound fragment candidates are plausible here. They do not derive a galactic cold medium, its abundance, its dwarf-dependent initial conditions or a physical formation history. This changes the original protected carrier action; it is not an algebraic recovery of that action's missing binding.

## Exact local elimination and expansion

Use the pinned parameters of `cold_completion_2026_10_20/common_action.py` and its `run_001/results.json`:

\[
V=I+M_X^2|X|^2+g(X^*\Psi^2+X\Psi^{*2})+\lambda I^2+a\chi I+U(\chi),
\]
\[
U(\chi)=\tfrac12M^2\chi^2-\tfrac18M\chi^3+\tfrac14\chi^4,
\quad M=100,\ a=200,\ M_X^2=4.0016,\ g=0.002168,
\quad \lambda=1.99+g^2/M_X^2.
\]

At fixed I, the neutral local minimum is unique because

\[
U''(\chi)=3(\chi-M/8)^2+61M^2/64>0.
\]

It satisfies `U'(chi)=-a I` and is negative for positive I. Set `z=chi/M` and `t=a I/M^3`. Its equation and formal small-t solution are

\[
z-\tfrac38z^2+z^3=-t,
\qquad z=-t+\tfrac38t^2+\tfrac{23}{32}t^3+O(t^4).
\]

For `w(I)=min_chi [U(chi)+a chi I]`, differentiation gives `w'(I)=a chi(I)`. Hence

\[
w(I)=-\frac{a^2}{2M^2}I^2+\frac{a^3}{8M^5}I^3
 +\frac{23a^4}{128M^8}I^4+O(I^5).
\]

The proposed `23/128` coefficient is correct. This is an expansion near I=0, with no asserted global radius of convergence.

For static, spatially homogeneous configurations, completing the X square gives

\[
M_X^2\left|X+\frac{g\Psi^2}{M_X^2}\right|^2
 +\left(\lambda-\frac{g^2}{M_X^2}\right)I^2.
\]

Thus `X=-g Psi^2/MX2`, and `lambda-g^2/MX2=1.99` exactly. Combining it with w yields the displayed local potential: the neutral-induced `-2 I^2` term exceeds the repulsive `+1.99 I^2` term by `0.01 I^2`. At very large I, the neutral minimum behaves as `w(I) ~ -(3/4)(a I)^(4/3)`, while the static X-reduced `+1.99 I^2` dominates. Stabilization therefore does not depend on extrapolating the truncated Taylor series to arbitrary density.

The independent local cubic-root check at I=50 gives

\[
\chi=-0.9961797389345873,\quad X=-0.0270891643342663,
\quad V_{\rm loc}=37.6764603507781,\quad V_{\rm loc}/I=0.753529207016<1.
\]

The fourth-order truncation gives 37.6796875, an 8.57e-5 relative error at this one point. This demonstrates a sub-rest local potential point in the fixed alternative action. It is not a theorem establishing a continuum finite-charge soliton, its ground state or its nonlinear stability; gradients, time-dependent charge storage and all field equations remain relevant.

## Rotating fragments and limits of the reduction

For a synchronized stationary carrier `Psi=e^(i omega t) f`, `X=e^(2i omega t) b`, the functional reduced at fixed omega is **E-omega Q**, not V. Dropping gradients only for this algebraic illustration gives

\[
W_\omega=(1-\omega^2)I+(M_X^2-4\omega^2)|b|^2
 +g(b^*f^2+b f^{*2})+\lambda I^2+a\chi I+U(\chi).
\]

When `MX2-4 omega^2>0`, its local X minimizer and value are

\[
b=-\frac{g f^2}{M_X^2-4\omega^2},\qquad
W_{\omega,\rm loc}=(1-\omega^2)I+
\left(\lambda-\frac{g^2}{M_X^2-4\omega^2}\right)I^2+w(I).
\]

Replacing the static denominator in V without also accounting for rotating kinetic energy and charge would mix different functionals. The finite-radius X equation instead involves `-Lap+MX2-4 omega^2`; the static physical configuration problem has `-Lap+MX2`. Their exact eliminations are spatially nonlocal. Neutral gradients likewise replace pointwise minimization with an elliptic problem. Dynamical elimination introduces retardation and homogeneous mediator excitations. A local potential is a controlled approximation only when the relevant gradient/time scales justify it; it is not a replacement for the full three-field action.

The separately audited `chi_dressed_initial_run_001` solves the **same finite-volume elliptic neutral equation** at fixed charged fields, rather than simply using the local Taylor series. Its lower E compares different initial preparations. No energy was radiated by constructing that preparation, and no cooling history was demonstrated.

## Outlet for actual excess energy, and the unresolved physics

An internal oscillation at frequency Omega can generate a quadratic second harmonic. In the positive-charge Psi branch its laboratory frequency is `nu=omega+2 Omega`; with `m_Psi=1`, propagating radiation requires

\[
(\omega+2\Omega)^2>1,\qquad\text{equivalently}\quad2\Omega>1-\omega
\]

for these positive frequencies. In the matched Q136000/Q140000 linear reference caches, `2 Omega=0.1207748123/0.1191740906` exceeds `1-omega=0.0879161643/0.0883866573`; the laboratory frequencies are 1.0328586480/1.0307874332. The displayed opposite Psi sideband, positive X sideband and neutral harmonic remain below their thresholds. This is a kinematic opening, not a computed amplitude, escape efficiency or finite-amplitude cooling rate. The escaping positive-charge wave carries physical energy and charge; its reduced energy is `E_wave-omega Q_wave`. Fixed-total-charge response and flux accounting must accompany a damping interpretation.

The head-on axisymmetric m=0 experiment has zero angular momentum and cannot test removal of galactic orbital angular momentum. A binding potential, a finite stationary branch, a merger excitation and an open radiation channel are different obligations. The current calculations must still establish their dynamical connection at the observed amplitudes, physical-unit calibration, surviving cold stock and a predicted history that favors Draco/Sextans without overboosting Fornax/Leo I. No dwarf-dependent normalization is generated by this local elimination.

## Audit record

`effective_binding_check.py`, frozen `effective_binding_contract.json` and `effective_binding_run_001` completed 15/15 exact-algebra/local-arithmetic controls; the manifest independently validates. No BVP, field evolution, spectrum or live Claude experiment was run. Sources and report bytes are pinned in `sources_effective_binding.json`.
