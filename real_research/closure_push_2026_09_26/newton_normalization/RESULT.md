# Measured Newton normalization: a constructive window and its physical cost

Checkpoint CD26-2. This is a result for a specified khronometric action family,
not a restriction on every possible gravity theory. Units are c=1.

**Version boundary:** this route tests the exponential AQUAL target pinned at
the start of CD26-2. During the run, external commit `9092fc0fd` amended the
operative project target to filtered `nu_mono` and preferred-foliation causal
criterion B. The exponential window and its numerical preferred-frame floor
below are branch results; they do not automatically transfer to `nu_mono`.
The asymptotic PPN formula still applies conditionally to the displayed
quadratic action. No metric-cone failure alone is a failure under criterion B.

## What changed

The old choice equated the bare Einstein coefficient with the Newton constant
measured by a static source. That equality is not automatic. Retain an explicit
positive constant C and take

\[
F_C(a)=2(1-C)a^2+4Ca_0^2[1-(1+x)e^{-x}],\qquad x=a/a_0.
\]

The static Einstein term plus this primitive is exactly

\[
-2a^2+F_C=-2Ca_0^2[x^2+2(1+x)e^{-x}-2].
\]

Consequently its general-source static equation has the target
\(\mu(x)=1-e^{-x}\), with **\(G_N=G_{\rm bare}/C\)**. This is an
integrated function in the action, not a choice of coefficients after variation.
The two eigenvalues of one half of its acceleration Hessian are

\[
E_T=2[1-C(1-e^{-x})],\qquad
E_L=2[1-C(1+(x-1)e^{-x})].
\]

The longitudinal response \(1+(x-1)e^{-x}\) has its exact global maximum
\(1+e^{-2}\) at x=2. Thus

\[
0<C<\frac1{1+e^{-2}}=0.880797\ldots
\quad\Longrightarrow\quad 0<E_T,E_L<2\quad(x>0).
\]

This repairs a genuine limitation of the C=1 branch: its negative
longitudinal tangent for x>1 is not forced by the AQUAL kernel alone.

## Same-action dynamical test

For the Einstein action plus \(F_C(a)-B K^2\), with B>0 and the tensor
kinetic/curvature normalization held fixed, eliminating the linear lapse and
longitudinal shift gives

\[
L_{\rm sc}=\kappa\dot\psi^2-rac{2(2-E)}E k^2\psi^2,
\quad\kappa=\frac{2(2+3B)}B,
\quad c_s^2=\frac{2(2-E)}{\kappa E}.
\]

For example, C=1/2 and B=1/10 give positive kinetic and gradient coefficients
at every positive acceleration, with a scalar principal speed below the
physical metric speed. This statement is about the frozen principal block.
At x=0, E=2 and its quadratic spatial stiffness vanishes; neither uniform
hyperbolicity nor nonlinear control at that point is established. Submetric
speed also does not by itself satisfy gravitational Cherenkov constraints.

The conserved planar tidal transfer was independently divided into its wave
pole and polynomial contact part. For the specified compact generator
\(R=-k^2F\), the polynomial degree is at most one in \(\omega^2/k^2\).
This limited test is not an all-source or nonlinear causality proof.

## Preferred-frame check from the moving source

We solved the scalar constraints with source conservation, included the
transverse shift, boosted the metric of a uniformly moving weak source to
its rest frame, and normalized by the **measured** G_N. This yields, in the
asymptotic high-acceleration action,

\[
E_\infty=2(1-C),\qquad
\alpha_1=-4E_\infty=-8(1-C),
\]
\[
\alpha_2=
\frac{E_\infty(E_\infty-B+2E_\infty B)}{B(2-E_\infty)}.
\]

The GR moving-source control is zero. The independent primary-source
cross-check is equations (48)–(49) of
[Yagi, Blas, Barausse and Yunes, arXiv:1311.7144v4](https://arxiv.org/pdf/1311.7144v4),
with their beta=0, alpha=E_infinity and lambda=B. These equations retain the
coupling dependence needed here; a small-coupling expansion would be unsuitable.

The all-x positive-tangent window consequently requires

\[
|\alpha_1|>\frac8{e^2+1}=0.953623\ldots .
\]

This is incompatible even with the conservative historical 1e-4 bound quoted
in that paper. We have not presented that historical number as a fresh 2026
observational analysis. Changing B, or a scalar clock's velocity direction,
cannot repair the transverse-source normalization in this family. A constant
rescaling of the entire Einstein coefficient is also only a change of units
for these dimensionless ratios. A successful extension must change an actual
physical response or the family assumptions.

## Cosmology and the dark-energy interpretation

Direct variation of the FRW minisuperspace lapse gives

\[
\frac{G_{\rm cosm}}{G_N}=\frac C{1+3B/2}.
\]

The homogeneous background has a=0 and F_C(0)=0. At large a, subtracting the
quadratic part of F_C leaves the constant 4Ca0^2, equivalent within that
asymptotic action to Lambda -> Lambda-2Ca0^2. This does **not** identify the
cosmological dark-energy density: the two limits differ, and Lambda remains
an action input. No value of the a0–Lambda proportionality constant is derived
by this normalization change.

The Newton/cosmological normalization cross-check is equations (5.30) and
(5.32) of
[Blas, Pujolas and Sibiryakov, arXiv:1007.3503v1](https://arxiv.org/pdf/1007.3503v1).
Its small-coupling preferred-frame approximation was not used for E of order one.

## Evidence and certification boundary

- `run2/manifest.json`: accepted bounded symbolic run, 22 checks; input and
  output hashes are recorded. `run1` is a preserved failed execution caused
  by imposing reality on individual Fourier amplitudes in SymPy. Its exact
  source is archived; the correction uses the complexified linear system.
- `PushNewton20260926.lean`: eight compiled theorems, including the actual
  exponential bound, attained maximum, positive tangent interval, measured-G
  identity, and preferred-frame lower-bound implication. Compiler exit 0;
  only propext, Classical.choice and Quot.sound occur in printed axioms.
- The action-to-perturbation and source-to-PPN derivations are exact symbolic
  calculations with explicit controls, not fully formalized field theory.
  The complete theory remains open.
