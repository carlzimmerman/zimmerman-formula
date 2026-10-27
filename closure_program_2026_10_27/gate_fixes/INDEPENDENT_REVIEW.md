# Coordinator review of X57 and X64 corrections

Reviewer: root coordinator, distinct from the correction author selector_audit.
Reviewed 2026-10-27 against the actual correction source and saved outputs.
This is an analytical/source review, not a full rerun of the inherited
M1–M4, CLASS, EPS, or survey processing.

**X57: correction accepted in its stated scope.** Entry into an inclusive
two-sigma band from above requires max(0,pred-meas-2*s). Dividing by pred is
necessary before comparison to a fractional response budget. Predictions
already inside the band require zero repair; predictions below it cannot be
repaired by a downward change. The implementation handles all three cases.
The saved four-cell values agree with the coordinator's earlier independent
recalculation. Withdrawing R4b from the general-profile verdict removes M6's
sole alternative-footing failure. It does not prove the inherited D is an
achievable deficit, a rigorous general bound, or a physical solution.

The positive spherical shell is a valid shear-sign counterexample. Inside
the shell, u=sqrt(1-R^2/a^2)<1 and
1/(1+u)-1/(2u)=(u-1)/(2u(1+u))<0. Outside, the shell acts as a point mass in
projection. This refutes nonnegative-density-implies-positive-shear; no
stability or formation conclusion follows.

**C6R: the common-radius implementation is consistent with its explicit new
name and profile conventions.** At r*=sqrt(G M_catalog/a0), the point-mass
force is a0 and the ratio reduces to sqrt(2/nu(1)). For a Plummer source the
implemented potential GM/sqrt(r^2+a^2) and enclosed mass
Mr^3/(r^2+a^2)^(3/2) are evaluated at this same r*. The beta-profile formula
uses the enclosed-mass term GM(<r)/r plus the finite outer-shell integral;
beyond its cutoff this reduces to GM_total/r. The uniform hot-gas sphere
uses the corresponding interior quadratic potential and exterior point-mass
potential, with the compact contribution counted once. The denominator uses
the law's acceleration of the enclosed baryon mass, not catalogue mass when
the source is extended.

Because Groups, SPARC large and the MW use the same point-mass convention,
their primary-label C6R intervals tie. Strict separation cannot follow from
this key. Conversely, removing the predeclared unconstrained Groups/Clusters
T1 labels changes the separation problem: its positive G gaps are a genuine
change to the finite calculation. Neither inference establishes that these
source approximations are correct enough for a mechanism. Host potentials,
extended discs and tracer profiles require further physical validation.

The retained distinction between the eight-key primary failure, the
reported G-label separation, and the 2/120 null relabelling frequency is
correct. Seven candidate intervals are inherited, not independently
recomputed or revalidated. The correction author's targeted regressions and
201-input provenance are documented separately; this review does not turn
those implementation checks into observational validation.
