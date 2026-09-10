# Joint-action search: constructive progress, not a completed theory

Base: `f109d3d8ce1cdab6b5f63bea75bca83a8d4798f9`.
See [sweep/README.md](sweep/README.md) for the parallel, resumable Mac search.
It makes no model/API calls. This package and the search are **OPEN**; the
specific refined control point is **rejected** by stability and higher tangency.

## Same theory, same acceleration scale

We keep the preceding explicit-clock action, in its regular invertible chart:

\[
S=\int d^4x\sqrt{-g}\left[F(X)R+\frac{3F_X^2}{2F}(\nabla X)^2
 +P(X)-G(X)\Box\phi\right]+S_m[g],\qquad X=-\tfrac12(\nabla\phi)^2.
\]

Here the function G(X) is not the Newton coupling. The clock is explicit and
is not relabeled as a nondynamical auxiliary. The action class is not claimed
new. One global a0=1 fixes units for both exterior targets; no local/per-halo
a0 is fitted. The coefficient 1/2 in the proposed a0–dark-energy relation
remains input, not a Lean-derived physical constant. No particle dark matter
is added.

The exponential target is imposed in an inverse problem; it is not yet a
forward prediction from a globally reconstructed action. In particular,
the target metric B=1+2rg enforces exactly vanishing physical radial pressure.
That is stronger than leading weak-field Phi=Psi. Failures of this target
chart do not exclude every metric satisfying observational no-slip. The eps
labels have not been calibrated to baryonic masses or measured G_N.

## A newly passed gate, followed immediately by falsification

Let f=F_X, j=F_XX, w=fX', and use the preceding checkpoint's exact operators
L0,L1 on normalized jets K=P_X/f, Gamma=G_X/f. For the two target states,

\[
E=A+fB,\quad A=L_0\Delta(K,\Gamma),\quad B=L_1\Delta(K,\Gamma),
\qquad N=(L_0+fL_1)E\big|_{f\ \mathrm{fixed}}.
\]

Common lower action jets require E=0; the next necessary condition is
N+jB=0 with **one common j**. These are action-function compatibility
conditions, not the Poisson-bracket matrix or nonlinear Dirac closure.

Varying the clock-gradient magnitude, rather than fixing the earlier sample,
produced a regular joint point at F=.525, X=.5, y1=.1, eps1=1e-6,
eps2=2e-6:

\[
U_1/\epsilon_1=4754.976244115166,\quad
y_2=0.1800733844321236,\quad U_2/\epsilon_2=3057.78268757124,
\quad f=3.299925878671733,\quad j=38.55121957649491.
\]

`refine_joint.py` independently solves all five actual action-jet differences
and both next-derivative differences at 60 and 80 decimal digits. At 80 digits
the largest scaled residual is below 7e-78. The original Einstein/current
checks also hold to numerical precision. This is not an interval-enclosed
existence proof or an invariant trajectory.

The next tests reject this point:

- Its two local Einstein-frame angular squared speeds are approximately
  **−0.10147060 and −0.10025493**, obtained as −M22/M00 with positive M00.
  The frozen scalar principal equation has an angular gradient instability.
- Writing k=F_XXX, preservation of N+jB=0 requires M+kB=0. The two
  components demand incompatible k. Increasing the order of the common
  action Taylor series cannot cure this mismatch at the fixed point.

Thus a new compatibility gate was genuinely passed, but this point is not a
candidate for a healthy complete gravity theory. The scanner distinguishes
optimizer convergence, numerical equation matching, local health, and the
queue for independent higher-precision verification.

## What has actually been eliminated?

There is **no defensible percentage of the full theory space eliminated**.
No finite-dimensional measure over all admissible actions has been defined.
Counts from a bounded scan cannot supply such a percentage.

1. [scaling/REPORT.md](scaling/REPORT.md) derives one redundant positive
   overall vacuum-action normalization. Scaling (F,w,f,j) together leaves
   the compatibility zeros and the implemented local health diagnostic
   unchanged. It cannot fix a failure. The sourced measured-G_N problem
   still depends on normalization.
2. [zero_braiding/REPORT.md](zero_braiding/REPORT.md) derives a conditional
   exclusion of the regular, static, timelike, zero-current, zero-braiding
   branch: its on-shell principal has M01=M11=0 and
   M00=[(v0²−v1²)/v1²]M22. Strict bounded scalar energy is impossible.
   This sign argument does not require B=1+2rg; other currents, braiding,
   clock types and singular charts remain outside it.
3. On the searched nonzero-braiding chart, common pressure is eliminated
   analytically and shared f,j are solved from the preservation equations.
   Two four-variable search modes remain. This is an equation reduction,
   not a percentage exclusion of healthy theories.

Five new Lean lemmas certify conditional real-algebra steps in (1) and (2).
They do not formalize action variation, the numerical root, its empirical
status, or a law of nature. No `sorry`-based certificate is accepted.

## Remaining construction, in order

Find a regular joint point with healthy local principal, refine it, require
the next and subsequent common derivatives to preserve the matched manifold,
then construct a common action over an interval and across a continuous mass
family. Source matching and independent physical Phi/Psi follow; imposed
target geometry cannot substitute for those calculations. Full constraints,
matter Ward identity, PPN, physical causal/strong-coupling analysis, FLRW,
k=0 and zero-field limits, measured G_N, and a CMB likelihood all remain
uncertified. No local search result is promoted to a CMB-safe theory.

Carl's request for a shared global acceleration scale, explicit clock rather
than particle dark matter, and gate-by-gate falsification fixes this search's
physical target. The scripts do not invent a derivation of his fitted
coefficient or claim novelty for the underlying scalar–tensor action class.
