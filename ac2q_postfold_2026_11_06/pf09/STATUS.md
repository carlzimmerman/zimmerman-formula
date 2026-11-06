# PF09: finite-regularity evolution, native breakdown, and singular selection

The finite-regularity/local-constraint gap from PF08 is closed in the explicitly
stated periodic planar strong-solution class. An independently audited argument
now establishes existence of native finite-gradient breakdown for a family of
small-amplitude, sufficiently narrow compressive packets. The question of a
uniquely selected singular native continuation remains open.

## Local evolution and constraint propagation

The native hold-law cusp is retained. Uniform-arclength clock gauge, a periodic
first-order auxiliary inverse, uniform first-derivative estimates, and an L2
stability/compactness argument give a unique local jointly Lipschitz strong
solution. Smooth approximants are proof devices on uniformly regular intervals;
no smoothed hold law, viscosity or postbreak prescription is adopted.

All six defining/matter/Einstein residuals satisfy a homogeneous transport system
along the clock. This was derived off the constraint surface, including the
actual commutator, rather than assumed from Bianchi identities. Zero initial
constraints therefore remain zero. A constrained continuation estimate shows
that a finite endpoint with controlled physical domains, length, lower fields
and a,K can be extended; the W_PP cusp does not independently stop evolution.

Proof: LOCAL_EVOLUTION.md; precise independent audit and necessary completion
of its estimates: review/LOCAL_EVOLUTION_AUDIT.md. Exact residual equations:
review/RESIDUAL_PROPAGATION.md. Eight symbolic checks pass in residual001;
its manifest validates. These checks support algebra, not the analytic theorem
by themselves. Continuous dependence is in C(time;L2) on bounded Lipschitz
classes, not asserted in the full W1,infinity norm.

## Full coupled breakdown within the stated subfamily

The constant-potential proof combines this local theory with:

- a width-independent exact auxiliary/ADM initial constraint construction;
- a covariant total-variation estimate controlling the nonlocal auxiliary rates;
- exact conformal Einstein wave equations with bounded algebraic stress sources;
- a weighted characteristic equation with a strictly compressive quadratic term
  and only bounded/linear-gradient remainder.

For fixed sufficiently small packet amplitude delta, width epsilon can be taken
small enough that |a|+|K| becomes unbounded by clock time C epsilon/delta.
Here a=e(log r) and K is the clock congruence expansion. Before that endpoint,
clock/cap/hyperbolicity margins, r,A,P, rapidity and regular conformal metric
coefficients/first derivatives stay controlled. The native coupled fields do
not prevent every compressive fold. This is not a curvature-singularity theorem.

See COMPACT_BOOTSTRAP.md and review/COMPACT_BOOTSTRAP_AUDIT.md, together with
PF08 principal_review/RIEMANN_SOURCES.md. The latter's previously conditional
local-theory input is supplied by PF09 in this class; its historical file is
retained unchanged. No numerical refinement trend is used as the proof.

VARIABLE_POTENTIAL.md derives the additional scalar force and auxiliary source
for a regular positive rolling V(phi), with a0(phi)^2=xi G V(phi) and constant
gamma. Four exact checks pass in potential001. The independent audit
review/VARIABLE_POTENTIAL_AUDIT.md verifies that the local evolution, constraints
and packet-breakdown proof extend to a positive C2 rolling potential on a
compact clock interval with the stated cap margins. The result is therefore
not restricted to a constant-potential numerical fixture.

The result concerns arbitrarily narrow continuum packets. It does not prove
that every initial datum breaks, determine an astrophysical event time, or
establish that the earlier numerical fixture reaches a particular singularity.
Any independent physical UV-validity restriction requires a separate assessment.

## Singular continuation: exact decision boundary

Prebreak uniqueness is established in the stated strong class. Strong global
survival for all admissible data is ruled out by the packet result. Predicting
past breakdown therefore needs an enlarged solution/admissibility framework.
That is a mathematical completion obligation, not yet proof of necessary new
fields or a modified physical action.

The PF07 bounded-layer exclusions remain valid with their original assumptions.
Four additional restricted exclusions now have independent audits:

- A cap excursion beyond separated outer traces has transverse-stress cost at
  least c/epsilon; a uniform per-clock-slice stress bound excludes it. A finite
  spacetime measure bound alone does not exclude intermittent excursions.
- An unbounded invariant r cannot carry timelike surface stress under bounded
  rapidity, lower clock/cap margins, uniform slice stress control, strong Pi
  matching and controlled clock/coarea geometry. This removes an upper-r bound
  from that restricted no-stress result.
- Bounded polarization jumps produce only pure multiplier dust stress. Under
  the additional multiplier-weighted tangential-clock trace condition, it
  cannot connect strictly on-branch endpoints. Pure open-off/open-off dust
  jumps are also excluded by the native hold-law/Einstein secant condition.
- A boost-only stress concentration also vanishes for bounded invariant state,
  strong uniform Pi matching, regular metric contractions and finite total stress
  measures. A boost-independent trace identity supplies the exclusion without
  separately bounding the opposing boost terms.

See review/SINGULAR_STRESS_AUDIT.md, review/POLARIZATION_JUMP_AUDIT.md and
review/BOOST_TRACE_AUDIT.md. These exclusions do not establish that all singular
native limits fail.

A concrete algebraic test shows why their union is insufficient. Native high-r
constitutive concentrations and opposite off-branch boosted concentrations can
sum to a nonzero finite stress tangent to a timelike interface. Six exact checks
in combined001 verify those tensor limits. COMBINED_DEFECT_TEST.md explicitly
constructs only constitutive states, **not fields satisfying the differential
constraints or a native continuation from given data**. It refutes a purely
algebraic universal no-stress argument, not uniqueness of native evolution.
The next discriminator is whether the full differential equations and clock
compatibility exclude or realize this simultaneous mechanism.

No fixed general singular class has been shown to admit a native continuation
uniquely selected by the same smooth incoming data. Nor have two such actual
native continuations been constructed. Combined invariant/boost escape, clock degeneration,
intermittent cap concentration, singular geometry or unidentified bulk/stress
oscillation defects are not eliminated merely by naming them.

The defensible classification is: **AC2q's coupled strong evolution can break;
its postbreak predictive completion is still unestablished.** The claim that
new physics is unavoidable, as opposed to a well-defined native singular
completion, remains unproved.
