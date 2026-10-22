# Unsuccessful or deliberately rejected routes

These are analytic estimate failures/invalid transfers, not PDE counterexamples
and not failed numerical experiments. No numerical process was run.

1. Exact hydrostatic field collars after fast arrivals: FGF054's collar gate
   would require Bcap<V/max(cs,field speeds). It cannot justify traces here.
   Replacement: the actual wide-cone field subtraction (3.4) and fluid-only
   exterior wedges (4.1). No old stationary patching remains.
2. Estimate g-g0 by integrating p_X over the proposed full upper horizon:
   would need a gradient bound near an unknown endpoint. Replacement (3.4)
   differentiates only the known background and needs bounded source amplitudes.
3. Reuse a fixed-order-one initial cone with the crude centered invariants:
   its background density variation costs O(1), which does not yield the
   claimed V+O(e) speed margin. Replacement: an O(e) cone with coefficient
   Hrad=3+S Bcap/V, allowed arbitrarily large but fixed in e.
4. Drop the advective derivative when centering fluid invariants on q0(X):
   incorrect. Exact (4.2) retains the terms -c v q0_X and +c v q0_X.
5. Treat pressure, mass transfer or field stress as zero at +/-2e:
   false under the changed premise. Equations (5.1)--(6.6) retain each term.
   In particular using the endpoint field-stress O(e) bound as if it implied
   conserved P+Fm would be invalid; fluid R and the exact transfer identity
   avoid that unsupported step.
6. Transfer the old N-dependent lower time by substituting a finite V:
   changes the old normalization/coefficients. Section 7 instead fixes units
   and constructs new Pscale=V/e estimates, exact C1,1 traces and restarts.
7. Name the old stationary maximal-germ class after deleting its collars:
   not justified. The stated result uses actual contained-cone survival and
   same-domain lower existence only, as authorized in the task.

No route claiming low-Mach shock, endpoint type, physical parameter calibration,
physical closure or novelty was attempted. The threshold 15/2 is a sufficient
capacity/acoustic-buffer certificate, not a sharp PDE transition.
