# Critical homogeneous continuation: exact nearby-rank witness

This separate supplement leaves the frozen REPORT.md and its b run inputs unchanged. It independently reconstructs the previously unresolved critical m=1/2 determinant for the declared regular linear continuation, allowing the free invisible S3 counterterm eta=−xi. Coincident rank1 does not persist on nearby homogeneous metric configurations at the physically relevant tensor mass-cancellation choice xi=3/8.

## Action and domain

Use precisely the frozen report's both-lapse homogeneous action: healthy two EH sectors, averaged Upsilon_sym, geometric-mean volume sqrt(NL)(ab)^(3/2), and added K(xi J+eta S3)/2. Set n=3,m=1/2,eta=−xi. Only **after** deriving the raw connections/invariants retain the positive position slice N=L=a=1,b=s^2 with s>0. The three independent velocity coordinates are (h1,h2,u)=(dot a/a,dot b/b,dot N/N−dot L/L). Nothing fixes their velocities or sets u=0 before variation.

The calculation is exact for the declared linear regular invariant interaction. For a nonlinear regular interaction it is also its velocity Hessian at zero-velocity offshell jets, since C=0 there and the M_zz gradient outer product vanishes. It is not the undefined negative-z auxiliary MOND continuation, not a moving off-coincident FRW solution, and not a proof that any witness obeys the lapse/evolution constraints. The full five-velocity Hessian also retains the common-lapse and auxiliary null directions established in REPORT.md.

## Independently factored determinant

Using the five raw contractions directly and differentiating the action gives

`det Hred=−27 K^3 s(s−1)^4(s+1)^2(s^2+1)^2(4xi−1)^2 P(s,xi)/8`,

`P=(xi+1)(s^6+2s^5+3s^4+3s^2+2s+1)+(4xi+2)s^3`.

This independently matches the root's proposed factorization exactly, with zero symbolic residual. At s=1 the reduced Hessian has rank1. At the exceptional xi=1/4 the action is homogeneous-relative-lapse independent, as shown in the frozen report, so its reduced rank is at most2; the executable verifies rank2 at s=2. No claim of a globally constant exceptional rank is made. A zero determinant by itself would not prove rank1 or a full secondary constraint.

For a safe nonzero-rank range, rewrite

`P/s^3=(xi+1) D(s)+16xi+14`,

`D=(s^3+s^−3−2)+2(s^2+s^−2−2)+3(s+s^−1−2)`.

Each summand equals (s^j−1)^2/s^j and is nonnegative, strictly positive for s!=1. Hence P>0 for every s>0,s!=1 when xi>=−7/8. In particular it is positive for the physically relevant xi>=0. Therefore in this range, excluding xi=1/4, the reduced rank is3 at every off-coincident point of this slice. The weaker bound xi>−1 alone would be false: at xi=−9/10,s=1 one has P=−2/5; continuity also gives negative P at nearby s!=1. Between −1 and −7/8 special P-zero surfaces can occur, so the factorization rather than an unqualified sign assertion controls that range.

## Critical tensor mass cancellation does not close this constraint gap

At n=3,m=1/2 the relative TT kinetic is zero and its de Sitter curvature coefficient is proportional to 3/2−4xi. The tensor mass-cancellation choice is xi=3/8. The exact determinant becomes

`−27 K^3 s(s−1)^4(s+1)^2(s^2+1)^2 [11s^6+22s^5+33s^4+28s^3+33s^2+22s+11]/256`.

It is nonzero for all s>0,s!=1. Near s=1,

`det Hred=−108 K^3(4xi−1)^2(8xi+7)(s−1)^4+O((s−1)^5)`,

and at xi=3/8 the coefficient is −270K^3. Thus tuning away both the critical TT kinetic and curvature equation does not also produce a globally degenerate homogeneous velocity Hessian. This is a separate constraint-admission obstruction within the specified regular representative, not evidence that a zero tensor coefficient is a ghost or that a homogeneous offshell jet is a physical galaxy.

The first remaining implication is still the full primary/secondary constraint and on-shell branch analysis. A rank-restoring neighborhood indicates that coincident linear degeneracy cannot be assumed to be a global primary constraint; it does not provide a physical mode count, a Hamiltonian sign after constraint reduction, or an EFT validity range. No lambda or32pi selection follows.

## Evidence/provenance

critical_checks.py independently reconstructs the actual homogeneous Lagrangian on this slice, differentiates its three-velocity Hessian, checks the full factorization, coincident/exceptional/mass-cancel ranks, reciprocal-square positivity identities and fourth-order near-coincidence coefficient. Three controls wrongly extrapolate rank1 globally, assert the loose positivity range, or equate TT mass cancellation with global Hessian degeneracy. Exact identities support the general statements; no numerical integration or Dirac reduction is claimed. The supplement has its own contract/provenance and fresh critical_* run folders, leaving frozen scientific inputs and historical runs intact.
