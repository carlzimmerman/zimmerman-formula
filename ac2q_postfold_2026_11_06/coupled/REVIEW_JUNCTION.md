# Independent audit of the coupled junction claim

Primary verdict: **correct only after a stated restriction**.

Claim reviewed: defect-free continuous-field planar stationary corners cannot
use an ordinary metric derivative jump to evade PF02's same-sign on-branch
obstruction; uniformly controlled stationary negative-divergence layers cannot
carry the missing impulse. Sources: `JUNCTION_RESULT.md`, sections 1–3,
and `../DERIVATION.md`, section 4. This independent subagent audit inspected
the raw arguments; symbolic pass counts were not treated as universal proofs.
No theorem statement or implementation was changed by this review.

## Dependencies and obligations

| Implication | Status | Reason |
| --- | --- | --- |
| Reduced metric conjugate fluxes | passed | Direct differentiation gives the displayed pi_alpha, pi_beta and pi_P. |
| Flux continuity implies normal metric derivative continuity | passed under stated regularity | First beta_x, then alpha_x follow; Mpl^2 must be positive and metric nondegenerate. |
| A stationary interface implies the displayed stationary D | failed as a general implication | A stationary surface can have evolving tangential field traces. |
| Stationary field profiles reduce the matter corner to PF02 | passed | The ell=P_x+2P beta_x substitution and Hamiltonian cancellation are exact. |
| PF02 strict convexity | passed for gamma>0, s_local>0, epsilon<1/3 | The displayed third derivative is strictly positive for 0<v<1; reflection covers negative velocities. |
| Strict on-branch endpoints imply a uniform A>1 limit | conditional | Endpoints must have strictly on-branch limiting states, not merely be strictly on branch at each family member. |
| Uniform normal currents bound off-branch P_x | passed with uniform A-1 gap | The coefficient multiplying P_x then has a uniform nonzero lower bound. |
| Bounded signed action excludes cap excursions | not asserted; correctly rejected | The text correctly requires a separate positive stiffness integral bound. |

## Decisive algebra

The metric flux identities require no inverse matter Hessian:

    [pi_alpha]=2 Mpl^2 exp(2 beta)[beta_x]=0,
    [pi_beta-2P pi_P]=2 Mpl^2 exp(2 beta)[alpha_x+beta_x]=0.

Continuous P and continuous pi_P therefore force both derivative jumps to
vanish. This is a valid necessary condition even though omitted conformal
Einstein constraints have not been solved. It does not prove existence.

For stationary profiles, with ell=P_x+2P beta_x, the matter contribution
to the normal Hamiltonian includes P_x pi_P+beta_x(2P pi_P)=ell pi_P.
The continuous metric derivative terms then drop from the jump. At common
metric values the rescaling to local s and local ell is invertible, so PF02's
Legendre and convexity argument applies. There is no remaining metric impulse
in this regular stationary class.

For a merely stationary interface the general expression instead contains

    D=exp(-alpha) C [P_x+2P beta_x+v(P_t+2P beta_t)].

The omitted tangential term can depend on v, so the exact PF02 reduced
function is not obtained simply by common metric rescaling. Bounded temporal
derivatives do not make this finite term zero. The cheapest valid restriction
is to state explicitly alpha=alpha(x), beta=beta(x), P=P(x), and
phi=s t+psi(x) for the regular-corner theorem. A time-dependent generalization
would need a new argument and is not supplied here.

The range 0<=gamma*s_local^2<1/3 must be read together with gamma>0 and
s_local>0. PF02 divides by gamma in the partial Legendre transform. The
negative-layer q bound also divides by gamma. Gamma=0 is not covered by
these proofs; it cannot silently be included through the epsilon notation.

## Negative-sheet hypotheses

The off-branch formula is correct:

    pi_phi=exp(alpha+2 beta) v C^3(P_x+2P beta_x)/s
            +exp(2 beta) s v(1+2 gamma B).

For fixed gamma>0, regular uniformly bounded/nondegenerate metric factors,
fixed s>0, uniform timelike separation, bounded explicit sources and temporal
current variation, and endpoint limits giving A>=1+delta with delta>0,
the polarization flux bound gives bounded q_plus. On the off branch C=A,
so |v| is uniformly bounded away from zero. Bounded scalar normal current
then bounds P_x algebraically. This proves the claimed exclusion within
these bounds without relying on an ambiguous product of delta distributions.

However, strict positivity q_endpoint(epsilon)>0 for every thin layer is not
alone a uniform gap. If its endpoint limits approach q=0 and v=0, A can
approach 1. The coefficient of P_x then degenerates; a bounded current does
not imply a uniform derivative bound. The statement should require strictly
on-branch limiting endpoints (or directly A>=1+delta). This is a gap in
the written uniform-bound implication, not a constructed solution of the
full coupled equations.

Normal current boundedness itself is a necessary estimate, not a consequence
of bounded potential derivatives alone in arbitrary time-dependent layers.
The expressly assumed temporal current bounds and bounded metric gradients
are needed in the flux balance. The result correctly excludes rapidly
time-dependent layers, singular metrics, cap approaches without the extra
coercive bound, and oscillatory weak limits.

## Strongest safe statement and next check

For stationary field profiles with continuous nondegenerate metric, phi and
P, finite one-sided derivatives, positive Mpl^2 and gamma, bounded sources,
no surface action or concentration defect, same-sign nonzero velocities,
and 0<gamma*s_local^2<1/3, the necessary conjugate-flux conditions exclude
the nontrivial PF02 on-branch corner even after native metric coupling.
Under the additional quantitative uniform layer bounds above, off-branch
negative sheets cannot evade that restricted obstruction.

The cheapest next action is to tighten those hypotheses in the statement.
No additional numerical test can establish the missing universal stationary-
surface or degenerating-endpoint claim. No inference of smooth-data shock
formation, global failure, or universal weak-solution nonexistence follows.

Review provenance: independent delegated proof audit, 2026-11-06. Read-only
shell inspection of the stated files and direct symbolic reasoning; no
external theorem or literature dependency was used.

Audited SHA-256 revisions (before any author restriction edits):

    JUNCTION_RESULT.md 9f89269bd90a3592e8b915c40561d1d9870819de1b2974384abe0f7b7d5f632b
    ../DERIVATION.md e74dfd20da201c9e294b7bcbfaee36ee9be46061cc5295dd15a1f0b620a0635a
