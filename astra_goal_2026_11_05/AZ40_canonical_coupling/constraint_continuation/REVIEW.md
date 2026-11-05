# Self-audit of the scoped continuation

Primary verdict: **proved as written** for the restricted statements in
RESULT.md sections1-5 and SWITCHED_CLOCK.md. This verdict is NOT for a healthy
complete covariant action. Author self-review only; no independent reviewer.

Claim card: (i) on an exact scalar-only flat FRW, P=0,Q=1,Lstar=0 branch,
H!=0,k_com!=0, the reduced scalar action has two nondegenerate velocity
coordinates and an unforced-to-zero conserved clock momentum; (ii) smooth
static Newtonian solutions with fixed source, a_phi!=0,0<|P|<a and the stated
bound have nonnegative second variation in the stated boundary class;
(iii) switched stiffness preserves a strictly convex clock velocity functional
in a fixed finite Galerkin leading-order system. No generalization across
missing hypotheses is part of these claims.

Dependency graph: action definitions -> normalized-clock variation and ADM
expansion -> constraint elimination -> rank/Routh equations; separately
Newtonian lapse elimination -> orthogonal-projector identity -> joint Hessian
of U -> static scalar equation -> positive-function factorization -> sufficient
bound. Switched extension uses only pointwise convexity, finite-dimensional
coercivity, the variational definition of a conjugate, and a quadratic bound.

Passed obligations:
- Independent phi and tau; signature and K versus M normalization explicit.
- Background scalar stress and clock/P first variations included; P=0 W is
  twice differentiable even though the standalone magnitude is not at zero.
- Lapse/shift solved, not set to zero; determinant excludes H=0,k=0.
- Time-dependent R^3 integration by parts retained; mass checked using KG and
  Raychaudhuri; canonical limit recovered independently of clock sign.
- Local finite-k momenta distinguished from integrated total Noether charge.
- The zero-clock-momentum sector is invariant only in the stated linear/leading
  systems; no nonlinear invariance or compulsory initial-data selection claimed.
- Static negative Schur term reconstructed exactly; its background force is
  retained rather than discarded under a new variable name.
- All discarded static second-variation pieces are nonnegative, including the
  transverse projector restoration after conservative local subtraction.
- Gradient remainder a'''/a' retained; its deletion fails both the general
  identity and a hand-evaluable nonzero-gradient witness.
- Boundary term vanishes under stated perturbation conditions; p=0 and a'=0
  excluded from division and strictness claims.
- AC1 force-subtracted BVPs recognized as different background equations; their
  results are not silently inherited by the new static inequality.
- Switched convexity proof uses the actual positive part; no Hessian/Fourier
  multiplier falsely assigned at the switching surface. Existence/coercivity
  claim is finite-dimensional, not an unproved infinite-dimensional minimizer.
- Super-Hubble solutions labeled leading asymptotics; full conformal equation
  retains k_com. No finite-k exactness asserted for the power-law approximations.

Exact executable corroboration:36/36 main; clock-sign mutation32/36, gradient-
remainder mutation34/36, each failing its intended invariants. These counts
support implementation, not a global mathematical theorem by enumeration.

External leaf: primary Maldacena v5 section2 agrees with the unmodified
Einstein/scalar ADM conventions. Its theorem content does not extend to the
new clock sector. All new implications are reconstructed internally here.

Not addressed: full charged-background nonlinear constraint rank, switching
continuum existence/regularity, realistic cosmological/local matching,
observational gates, global nonlinear clock health, or normalization selection.
The known exact caustic branch remains an obstruction to unrestricted smooth
independent-clock evolution. A positive static energy estimate cannot remove it.

Next discriminators: evaluate the corrected B_J bound with controlled BVP
errors; derive the charged covariant constraint operator; for a proposed clock
regularizer or the separate single-clock candidate, recompute its own sourced
background and check whether the timelike foliation persists. Those routes
remain open. No exhausted-route or full-action-completion verdict is entered.

Section8 corollary additionally checked: on the exact geodesic branch all
terms in E_mu and F_Q vanish, so the covariant current is identically zero.
AC1's characteristic crossing therefore survives even that stronger condition.
The conclusion is lack of an unconditional smoothness guarantee from zero
current, not failure of every physical initial-data selection. This corollary
uses an internal explicit construction, not a new numerical test.

Proofreading self-review: RESULT.md, SWITCHED_CLOCK.md, REVIEW.md, CONTRACT.md
and REPRODUCE.md. Notation, boundary qualifications and source scope checked;
no mathematical-token correction made. Remaining mathematical limitations are
listed above rather than disguised as typographical repairs.
