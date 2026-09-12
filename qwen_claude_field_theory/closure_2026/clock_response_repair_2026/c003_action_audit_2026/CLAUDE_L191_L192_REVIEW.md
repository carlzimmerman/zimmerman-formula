# Action-derived discriminators after Claude L191/L192

## Outcome

**The full theory remains OPEN. L191's original-gate certification and
L192's claimed exact-dust attractor are not established.** This continuation
adds an action-derived anisotropic principal calculation and an exact,
Lean-checked obstruction to L192's proposed marginal-state formula. It does
not rule out all gradient-mediated clock theories or establish global novelty.

Reviewed source commits: `9b97161a6` (L190/L191), `5fdec3d9a` (L192), and
`1b72e4751` (Hermes search). All existing source/coefficient files were left
unchanged. The adjacent `05d0eb98a` current-density repair was read for
coordination; none of its separate sector certificates is used to claim
closure of this clock action.

## The strongest new calculation

For the existing action's **fixed-metric, gamma=0 principal subsystem**,

\[
 L=P(X,\tau)-V(\tau)+\sqrt{-\partial\tau\cdot\partial\tau}\,W(Y,\tau),
 \qquad \bar\tau=s t,\quad \bar\chi=Qt+\mathbf v\cdot\mathbf x,
\]

vary both fields before eliminating the clock constraint. Freeze coefficient
jets only for this local principal calculation. Write

\[
 z=(\mathbf v\cdot\hat{\mathbf k})^2,\quad p=P_X,\ r=P_{XX},
 \quad C=W_Y+2zW_{YY},\quad K=2p+4Q^2r,
\]
\[
 F=W-2Q^2C-2zW_Y,\quad
 G=2p-4rz-\frac{2sC(W-2zW_Y)}F.
\]

For k!=0 and F!=0 the computed clock Schur complement gives

\[
 K c^2+8Qr(\mathbf v\cdot\hat{\mathbf k})c-G=0.
\]

The derivation uses the raw invariant Hessian, not assigned speeds or ranks.
It recovers L186 exactly at Y=0. L192's continuation instead substitutes
X for Q^2 in the temporal kinetic coefficient and misses mixed-derivative
and constraint terms. Adding W_YY alone does not repair those omissions.

At **L192's proposed marginal condition**
`s=p(W-2Q^2 C)/(W C)`, the actual quarter-discriminant of this subsystem is

\[
\boxed{\Xi=16Q^2r^2z+KG
 =-8pz\left(r+\frac{KQ^2C W_Y}{WF}\right)<0.}
\]

The strict sign requires p,r,z,W,F>0 and Q^2,C,W_Y>=0; the marginal
substitution additionally requires C!=0. Hence there is **no real
characteristic speed** at the claimed nontransverse marginal point on this
elimination branch. At the first stored longitudinal root, the computed
speeds are approximately `-0.00942634 +/- 0.00674881 i` (c=1 units).
This counterexample is to the proposed principal continuation, not a
full Einstein/cubic stability theorem or a solved anisotropic cosmology.

[Exact derivation and executed tests](../l192_principal_audit_2026/REPORT.md)
and [four Lean lemmas](L192Discriminant.lean) agree. The latter certify the
algebraic reduction, negative factorization, sign, and absence of a real
quadratic root; the action-to-symbol mapping is separately derived and
independently audited, not formalized tensor calculus.

L192 also uses reference qbar rather than the physical q of the sourced
background while printing the physical logarithm margin. The audit records
both and tests the algebraic defect after correcting that distinction.

## Two independent requirements that remain

First, a zero of a speed is not an attracting trajectory. The exact geometric
identity is

\[
 \dot Y=2D\chi\cdot(DQ+Qa)-2K_{ij}D^i\chi D^j\chi.
\]

[The tracking calculation](GRADIENT_TRACKING.md) identifies the source the
action must produce to offset dilution and follow a moving Y*. L192's V3
only checks opposite signs at two externally selected gradients; it does
not compute this source or its restoring response. Its Lean uniqueness
lemma assumes monotonicity and continuity, not dynamical attraction.

Second, exact dust needs the Hilbert stress to have pressureless eigenvalues;
zero sound speed alone is insufficient. The independent same-subsystem
[metric-stress audit](../l192_stress_audit_2026/REPORT.md) varies all ten
inverse-metric components and evaluates the unchanged constitutive function
at the claimed roots. No pressure offset or coefficient is retuned.
At a=1 and the stored transverse root, the source convention gives
`L/U=0.0303992606` while its trial sound speed is approximately zero.
The repeated spatial mixed-stress eigenvalues are L, so this is a
frame-independent pressure obstruction to exact dust. All 20 tested
root/epoch/Q-convention cases have nonzero transverse pressure in this
gamma=0 stress evaluation. They are not claimed on-shell cosmologies.

## Other executable checks from the latest work

- [L191 reconciliation](l191_reconciliation/REPORT.md): source-selected
  kick velocities differ between footings; the spiral ceiling is relaxed
  from 0.105 to 0.14175; the boundary comparison changes velocity too; the
  observable is an annulus, not enclosed mass. The independent controls
  drift, and rare central orbits have large errors. Thus the benchmark is
  not a converged physical retention prediction.
- [Five Lean no-event lemmas](POISSON_FLOOR.md): independent Poisson marking
  in a common prescribed force gives expected retention >=exp(-n).
  At n=2, exp(-2)>21/200, so stronger kicks alone cannot meet the original
  spiral ceiling. Self-consistent force changes can evade the common-flow
  assumption and have not been excluded.
- [Hermes objective counterexample](../fixed_action_initial_data_2026/hermes_objective_audit_2026/REPORT.md):
  total coded loss `8.88e-16`, yet a^3 rho varies by 14.62%. The slope-only
  dust test is not an exact conservation-law test. The synthetic input is
  an implementation counterexample, not a replacement physical history.

## What this removes, and what it leaves

Removed: the shortcut from a zero of L192's substituted formula to exact
dust, attraction, or a completed cosmology. Removed: treating L191's relaxed
point-estimate gate as the original gate, or zero optimizer loss as an
action-derived solution. No meaningful percentage of the unrestricted
theory space has been eliminated.

The next unavoidable calculation is a nonzero-gradient background satisfying
the **same fixed action's** equations, with the full Einstein/cubic
constraint reduction, all propagation directions, stress eigenvalues, and
the tracking-source response evaluated on that solution. One soft direction
is not cold dust. A reconstructed coefficient history is not this calculation.
The y=0, k=0, global a0, MOND law, PPN, lensing, CMB and galaxy/cluster gates
remain separate obligations of that one theory, not interchangeable results
from other models.

## Credit and novelty boundary

Carl Zimmerman's no-new-particle clock/field requirements and depletion
question motivate this investigation. Claude L192 supplied the proposed
gradient-criticality direction; this audit supplies its missing local
variation and a falsifiable obstruction. This is newly computed work in the
repository, not a priority claim. The no-event decomposition overlaps
published decay-halo accounting, explicitly cited in POISSON_FLOOR.md.

Mathbox research-program, computation-audit and proof-audit guided the split
between exact algebra, bounded numerical evidence and unproved physical
correspondence; independent agents checked the main principal derivation.
Successful test exits certify their stated checks, not a law of nature.
