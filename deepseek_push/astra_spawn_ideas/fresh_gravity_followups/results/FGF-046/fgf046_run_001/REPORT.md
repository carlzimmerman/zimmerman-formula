# FGF046 author report

Outcome: supports_scoped_claim. Acceptance remains unreviewed pending a
separate pinned review. Exclusive ownership was reserved by the dispatcher;
this author wrote only this assigned run directory.

The exact compact C1,1 polynomial now has a directly constructed positive C1
solution of both forced isothermal fluid equations on an interior characteristic
cone. The proof solves successive linear transport equations by elementary
characteristic ODE iteration, contracts in the uniform norm, and proves C1
convergence using a uniform Lipschitz spatial-gradient bound. Pressure and
force remain present. No existence/shock theorem is imported, and no data
smoothing is performed.

The positive guaranteed time is
T_N=min(tau,1/(8M),R/(4S_N)) >= c_* N^-4 for all sufficiently large N,
where all constants and actual initial norms are specified in DERIVATION
(4)-(6),(17)-(19). The initial Lipschitz-gradient bound is O(N^7), explicitly
retained. Its contribution cancels from this sufficient time gate; it remains
load bearing for derivative convergence. This is a proved lower bound, not a
numerically estimated or sharp lifespan.

The sufficient continuation gate requires a buffered interior compact interval,
positive finite density, bounded velocity and first invariant derivatives,
and a uniform Lipschitz bound on those derivatives. A trace and restart
construction establishes the gate. The higher bound is not silently inferred
from first derivatives. Thus no unconditional classification of an earlier
endpoint as first-gradient blowup is claimed.

Local uniqueness proves extension independence and identifies the hydrostatic
zero-velocity control. The actual C1 solution satisfies the full energy identity,
including pressure work, fixed-potential interaction and moving-boundary terms.
The FGF045 conditional upper obstruction applies to every continuation of this
same constructed germ that covers its cone and satisfies its stated large-N
gates. It does not construct a shock or a global wall solution.

Both acceleration footings and constant-vacuum, frozen-H and evolving-H
branches remain distinct. The frozen-field residual is still C(n-rho); this
is not coupled-gravity existence or physical closure.

Verification: all eight ancestry SHA256 pins matched. This fact was checked
after initial source reading but before proof development; no mismatch was
found. The root correction was read and respected. Mathematical executable
runs: zero. The commands field is empty under the proof-only exception;
administrative source reads, metadata SHA256/JSON checks, and scoped file
writes are not presented as mathematical tests. No installations, network,
services or commits were used. No new stage33 author/root/reviewer evidence
was read before finalization.

Proof-audit self-review: proved as written for the scoped theorem, with the
obligation matrix in DERIVATION Section 11. This is not an independent audit.
Mathematical proofreading covered the full new derivation. Routine edits
clarified that relative energy density is nonnegative, while its flux need
not be, and that the field residual is generally nonzero. The local kinetic
energy symbol K was explicitly defined. No mathematical operator, coefficient,
hypothesis or conclusion was changed by proofreading. No remaining local
notation issue was identified. No LaTeX build was needed for Markdown.

Limitations: no first-gradient-only continuation theorem, endpoint/shock
classification, post-breakdown solution, full boundary evolution, evolving-H
energy closure, dynamic gravity, physical reservoir, metric/photon/DOF,
observational/instrument claim, or theory closure. There is no missing step
inside the stated construction and higher-norm gate identified by self-review;
independent review remains required. If a stronger endpoint result is desired,
the next discriminating analytic task is to control the Lipschitz gradient
norm from explicit lower norms on a buffered moving cone. That enhancement
was deliberately not claimed here.
