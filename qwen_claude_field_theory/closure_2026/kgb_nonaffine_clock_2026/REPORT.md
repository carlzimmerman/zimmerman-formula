# Non-affine clock: exact parameter reduction and cosmology audit

2026-09-10. **Full-theory status: OPEN.** This checkpoint improves a
particle-free clock construction and proves conditional exclusions; it does
not certify a universal action or a new empirical law.

## One action, one global acceleration scale

We retain the physical-metric action

\[
S=\int d^4x\sqrt{-g}\left[
F(X)R+\frac{3F_X^2}{2F}(\nabla X)^2+P(X)-G(X)\Box\phi
\right]+S_m[g,\psi],\qquad X=-\tfrac12(\nabla\phi)^2.
\]

There are no dark-matter particle fields. The clock scalar is explicit, not
hidden as an auxiliary constraint. A constant vacuum term can be contained in
P; no new derivation of its value or relation to a0 is claimed. This is a known
derivative-conformal action family, not a newly discovered class; see the
versioned sources in the predecessor's `extension/SOURCES.md` and
[Langlois et al.](https://arxiv.org/abs/1711.07403v2).

The exterior tests use the SAME fixed a0 as a unit/input, with c=a0=m=1. They do
not fit a0 separately to a galaxy, use local matter density in a0, or replace
constant sqrt(rho_Lambda) by H(z). The numerical value and fitted one-half
coefficient of Carl's relation are not derived here. Nor has the conversion
from bare coupling to measured Newton constant been derived. See
`variation/GLOBAL_SOURCE.md` for the dimensionful source map and its gaps.

## Strongest exact result: eliminate a whole coefficient axis

Write f=F_X, j=F_XX, z=X', U=(psi')^2/B for the static clock
phi=-t+psi(r). Varying the action, including its total scalar current, gives
the actual three-equation inverse for (z',P_X,G_X). Its independently computed
determinant and j-dependence are

\[
\det M_3=\frac{4fz(2X+U)}{B\psi' r},\qquad
\partial_j(z',P_X,G_X)=(-z^2/f,0,0).
\]

This is an inverse-equation matrix, **not a canonical Poisson matrix**. Its
regularity conditions and removable pressure fold are in `variation/REPORT.md`.
The EF field-map Jacobian D=2(F-Xf) is a separate condition; it is not a factor
of this determinant. The primary highest-velocity Hessian is degenerate, but
the complete primary/secondary Dirac chain has not been proved.

For the inverse-derived local vacuum scalar principal matrix, define
K=M00, b=M01, R=M11, T=M22=M33, beta=U/(2X)>0 and I=K-T/beta. The exact
curvature direction changes only K and T, preserving R, b and I. Provided
R<0, the EF map is invertible, and the curvature's kinetic slope is nonzero,

\[
\boxed{\text{some real }F_{XX}\text{ gives bounded local scalar energy and a
strict EF light-cone interior}\quad\Longleftrightarrow\quad I+R>2|b|.}
\]

Lean proves the real-variable equivalence and accessibility for nonzero slope;
SymPy independently checks the action-to-pencil identities. The Lean file
does NOT formalize the entire field-theory derivation. For zero slope, the
unchanged matrix must be tested directly; for R>=0, this bounded-energy
criterion already fails. The isotropic choice T=R is more restrictive and
is not used as a necessary condition.

The same calculation proves that a shared j **cannot repair the first
preservation of an already matched common-mass P_X or G_X**: the j slopes
cancel between masses. Thus arbitrary F_XX scans cannot solve that gate.
This excludes a repair mechanism, not every possible universal action.

## Numerical construction: beyond the old boundary, not full closure

The following are finite reproducible calculations, not continuous numerical
proofs. Full rows, sampled action values, tolerances, exact commands and output
are retained by `run_suite.py` and its execution manifest.

- Fixed quadratic F: 144 local jets, 55 pass the tested local EF criteria.
  Eleven fixed-curvature continuations include one unhealthy seed and ten
  health-limited trajectories; none reaches the requested y=100 endpoint.
- Entire-real-j test on 105 background points: 12 are excluded for every j,
  and 93 admit an explicitly evaluated healthy local choice. This is not a
  measure or exhaustive count of the full functional parameter space.
- A prescribed constructive policy takes
  delta=min((I+R-2|b|)/2,-R/(2beta)), K=I-delta, T=-beta delta, and solves for j.
  It evolves ONE F,f,P,G along a monotonic X trajectory using w=fz. In
  particular F'=w, f'=jz, w'=f*z'|j=0, G'=G_X z; P follows its preserved
  radial equation. No independent P_XX/G_XX tuning or missing j' term is used.
- Starting at y=.1, epsilon=1e-6, F=.525, f=.05, X=.5, the controlled
  construction crosses the old affine boundary y≈.140417 and reaches
  y≈2.49819. A disclosed relative window guard stops it before the
  zero-width limit becomes numerically unreliable. Half-step and guard
  refinements, accepted points and interpolation midpoints are checked.
  This endpoint is NOT an exact no-go value or a proof that all policies fail.

The scalar-norm range is only approximately .5 to .50000295. It does not
specify F/P/G over a cosmological trajectory. The interior of this finite
exterior trajectory has passed the tested vacuum principal diagnostics;
physical nonlinear energy, higher regularity, and strong coupling remain open.

The spherical exponential profile and B=1+2rg are **imposed targets** of the
inverse, not a derived nonspherical baryon-sourced MOND law. The weak-field
acceleration proxy is not exactly the relativistic circular/support
acceleration. epsilon is not yet calibrated by an interior solution. A
one-mass reconstructed action is not evidence that the SAME functions work
for all masses. The full Phi/Psi/lensing/time-delay claims therefore remain
unproved even though the imposed metric has the intended leading no-slip form.

## CMB safety: use the same clock and its actual matter coupling

The independent cosmology lane derives the homogeneous action and mapped
fluid variation. Under C=2F, D=C-XC_X and chi=X/C, physical minimal matter is
not generally EF-minimal. In particular

\[
\rho_{m,E}=\frac{C\rho_m-3XC_Xp_m}{C^2D},\qquad
p_{m,E}=p_m/C^2.
\]

For dust this is rho_m/(CD), not rho_m/C^2. Its clock-current and homogeneous
kinetic terms must be included; radiation's trace contribution vanishes.
The same-action expansion/time mapping, scalar energy/current, and homogeneous
velocity-Hessian reduction are checked in `cosmology/`. These are prerequisites
for FLRW, not a CMB spectrum or a complete cosmological stability test.

A globally extrapolated fixed quadratic F has additional finite clock-norm
barriers: positive j reaches D=0, negative j reaches F=0 on the increasing-X
seed-connected branch. This does not show cosmology must cross either boundary,
and does not exclude a nonquadratic completion. Merely sharing the galaxy
two-jet leaves early-time energy undetermined; the audit constructs that
ambiguity explicitly.

`LATEST_REVIEW.md` audits concurrent L121/L122 and the new kernel Lean proofs.
Their isolated positivity statements are useful. Their claims that all
propagating scalars are eliminated, constant global a0 is excluded, or only
one architecture remains are not established. Neither a0/(cH) nor a literal
True assertion is a CMB calculation. For comparison, the distinct
[Skordis–Zlosnik construction](https://arxiv.org/abs/2007.00082v3) computes
cosmological spectra from its own equations; its success cannot be transferred
to this action.

The subsequent concurrent L123 claim that every regular shift-symmetric
scalar has an unavoidable a^-6 density tail is false. The separately varied,
standard counterexample P(X)=X^N has

\[
c_s^2=\frac1{2N-1},\qquad
\rho\propto a^{-6N/(2N-1)},\qquad
3<\frac{6N}{2N-1}\le4\quad(N\ge2).
\]

Nine exact tests and three conditional Lean lemmas are in `l123_review/`.
N=2 is a nonstiff radiation-like control; large N makes the positive sound
speed arbitrarily small. This refutes a claimed exhaustive exclusion; it does
not prove a CMB fit, exact dust, or strong-coupling safety. It is NOT substituted
for the F/P/G action's missing cosmology. L123's one-bracket-zero theorem also
does not certify an added sector as ghost-free.

## Unchanged full-gravity requirements

| Gate | Current evidence / missing calculation |
|---|---|
| Exact exponential MOND, BTFR, Newtonian limit | Imposed spherical exterior; derive baryon interior, measured G and nonspherical PDE. |
| Galaxies, clusters, lensing, time delays | No new empirical validation; common sourced physical metric required. |
| Two tensors, separately counted healthy clock | Primary degeneracy checked; full physical Dirac closure and rank sectors open. |
| Ordinary matter Ward identity | Physical minimal-coupling identity retained; EF matter terms derived, not dropped. |
| Phi/Psi and PPN beta/gamma/alpha_i | No full sourced PPN calculation or assigned parameter values. |
| Tensor speed and positive energy | Regular positive-F conformal sector; global physical constraint/matter analysis outstanding. |
| Scalar/vector stability and causality | Local vacuum scalar EF evidence only; physical coupled and FLRW modes unproved. |
| Expanding FLRW and CMB | Homogeneous equations/matter map derived; background, perturbations and spectra unsolved. |
| Strong coupling; k=0 and y=0 | Not certified; local positivity excludes y=0 and does not control zero modes. |
| Universal a0 and a0–Lambda coefficient | Global input retained; source calibration and first-principles coefficient unproved. |

Next unavoidable calculation: solve and preserve common F/P/G data for
multiple sourced masses, using the exact j-independent compatibility gaps
before optimizing curvature. Match baryonic interiors and common cosmological
clock data; evolve those SAME functions with the mapped fluids, then derive
their finite-wavelength perturbations and CMB transfer functions. Do not spend
a Boltzmann parameter scan on an action that is still defined separately per
exterior.

Credit: Carl's fixed exponential target, fitted a0–Lambda relation, primordial
clock direction, and explicit request to distinguish global from local a0
set the research problem. Mathbox research/computation/proof audits guided the
exact-versus-numerical separation, source review and conditional Lean scope.
The new interval and algebra are research progress, not a completed theory.

Verification details, including the failed recompile of the separate concurrent
Lean file, are in `EXECUTION.md`; exact commands/statuses are in `COMMANDS.json`
and `SUPPLEMENT_COMMANDS.json`. No full-suite success is asserted by hiding
that environment failure.
