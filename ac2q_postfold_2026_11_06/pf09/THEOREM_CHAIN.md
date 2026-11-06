# PF09 theorem chain and precise classification boundary

Synthesis of independently audited internal proofs. Read the corresponding
review files for the precise operator, regularity, trace and coordinate details.
Definitions and all restrictions are part of the claim.

## Objects and scope

Periodic planar AC2q with positive C2 V(phi) on a compact clock interval and
a0(phi)²=xi G V(phi), constant gamma>0,
Khold=1/(2M)>0, no extra matter, native hold law and switch. Potential values
and derivatives are bounded on the interval with positive lower margins. Work initially
in a compact open on-branch neighborhood of a homogeneous D=0 state with
0<gamma r0²<1. The Cauchy data obey all six matter/geometry constraints.
Metric and clock are nondegenerate. W1,infinity refers to the promoted
first-order fields U=(r,A,P,beta,B,E,a,K) in uniform-arclength clock gauge;
the physical interpretation uses the propagated defining constraints.

## Local theorem

Compatible periodic W1,infinity data in this regime admit a unique local
W1,infinity strong solution, with the field equations holding almost everywhere
and distributionally and with every constraint preserved. Uniqueness is within
bounded Lipschitz solutions in the fixed gauge; continuous dependence is in L2
on sets with common compact/Lipschitz bounds. No high-Sobolev or C-infinity
regularity at generic polarization zeros is claimed.

A finite-time solution continues if its lower-field values, physical margins,
clock-slice length and |a|+|K| stay bounded, with positive lower margins and
uniform coercive inverse constants. The continuation derivative estimate is
linear in a_x,K_x once the constraints have propagated. Refer to
LOCAL_EVOLUTION.md and review/RESIDUAL_PROPAGATION.md for the construction.

## Breakdown theorem

For sufficiently small fixed packet amplitude delta, there is a family of
compatible periodic initial data indexed by packet width epsilon>0. The
invariant field amplitudes, initial geometric first derivatives and total
clock variation are bounded independently of epsilon, while a negative
weighted characteristic gradient has size at least c delta/epsilon.
The exact periodic auxiliary solve and ADM data are given in PF08
principal_review/RIEMANN_SOURCES.md section6.

The native solution of this family loses bounded |a|+|K| within clock time
at most C epsilon/delta when epsilon is sufficiently small. Until that event
(or an earlier loss of the same gradient control), r,A,P, clock rapidity,
regular conformal metric coefficients/first derivatives, cap and hyperbolicity
margins stay controlled. The compact bootstrap and Riccati estimates are in
COMPACT_BOOTSTRAP.md and PF08 RIEMANN_SOURCES.md. Thus native auxiliary and
Einstein feedback do not prevent all compressive breakdown in the as-written
continuum equations.

This is an existence-of-breakdown result for an allowed subfamily, not a
claim that every datum breaks, a cosmological or galaxy event-time prediction,
or evidence that the arbitrarily narrow packets lie below no physical cutoff.
An added UV-validity restriction would need to be stated and tested separately.

## What does and does not follow after breakdown

Strong-solution global predictivity would fail for this family. To predict
beyond the endpoint one needs a defined enlarged solution/admissibility class.
That requirement is a mathematical completion obligation. It is NOT a proof
that new fields, a new stress term, viscosity or other new physics is necessary.

PF07 excludes ordinary bounded stress-carrying layers under explicit assumptions.
PF09 positivity may narrow some further controlled limits. Neither theorem
excludes all unbounded/degenerate native limits, constructs two native
continuations of the same incoming data, or proves a unique singular native
continuation. The three-way universal classification therefore remains open
despite the local and breakdown theorems above.

Do not mistake uniqueness before breakdown, or uniqueness of the spatial
auxiliary inverse, for uniqueness after breakdown. No postbreak selection
principle has been added by the approximation construction: it is used only
on intervals with uniform Lipschitz bounds, where the native strong limit is
unique independently of the approximation.

## Reviewed dependencies

- Local construction: LOCAL_EVOLUTION.md and review/LOCAL_EVOLUTION_AUDIT.md.
- Off-constraint identities and propagation: review/RESIDUAL_PROPAGATION.md;
  residual001 records8 exact symbolic checks.
- Compact packet bootstrap: COMPACT_BOOTSTRAP.md and its independent audit.
- Initial family, genuine nonlinearity and Riccati comparison: PF08
  principal_review/RIEMANN_SOURCES.md, with its formerly conditional local
  input now supplied in this class.
- Rolling-potential extension: VARIABLE_POTENTIAL.md and its independent audit;
  potential001 records4 exact source checks.

The source proof files retain their original candidate labels and hashes; the
review files supply the completed audit status and necessary precise details.
No numerical trajectory or external smooth theorem substitutes for a proof leaf.
