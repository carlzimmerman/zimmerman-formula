# AZ20 — FAIL universal physical-normalization selection

κ = ½ FITTED; not theory closed

This tests a new dynamical stabilization proposal: two auxiliary response sectors exchanged by q->-q, with normalizations eta exp(q) and eta exp(-q). Unlike AZ19's one-sector feedback, the relative normalization cannot be displaced at first order by a source. The proposed symmetry is a hypothesis. It fixes only a ratio unless the common physical normalization eta is fixed independently; eta is deliberately not set to1.

Eliminating each nondynamical chi before differentiating gives

E(B)/s²=y²+B^-2[C-1-2/(1+By)-2ln(1+By)], y=g/s.

The paired energy is the average at B=eta exp(q) and B=eta exp(-q). q=0 is exactly stationary for every y, and its energy equals the original response at B=eta. The average preserves the unit high-acceleration Newtonian normalization; no hidden doubling of the source coupling is used.

## What the candidate actually selects

The low-source response slope is eta(exp(q)+exp(-q)). At the symmetry point it is2eta, so the physical coefficient is conditionally kappa=1/(2eta). Relative equality exp(q)=1 does NOT mean the original KT2 physical normalization is1. Naming the ratio b would otherwise hide precisely the missing premise.

The vacuum energy at q=0 is s²(C-3)/eta² before the1/(8piG) prefactor. If that same sector is identified with the density in s=c sqrt(G rho), consistency gives (C-3)/(8pi eta²)=1. This is a relation between two unfixed quantities, not a selection of eta. The independent vacuum offset C is not removed by exchange symmetry. No target value is inserted for it.

## Source stability, varied with auxiliaries eliminated

Let x=eta y. The q curvature is (s²/eta²)h(x), where

A(x)=C-1-2/(1+x)-2ln(1+x),
h(x)=4A(x)+6x²/(1+x)²+2x²(x-1)/(1+x)³.

Exact limits are h(0)=4(C-3) and h(x)+8ln x ->4C+4 at large x. Thus a vacuum local minimum requires C>3, but for every finite C the symmetric point eventually has negative curvature in the unrestricted source domain. The exchange symmetry ensures stationarity, not stability at arbitrary source strength. An independently derived cutoff could restrict that statement's physical applicability; no cutoff is chosen here. Even with such a cutoff, the unfixed common normalization remains a separate obstruction.

The auxiliary constraint matters. Holding chi fixed during the q variation changes the curvature; at synthetic x=1 the error is exactly1/2. Unequal sector weights likewise break stationarity. These are controlled changes to the mechanism, not retuning to obtain a favorable value.

## Evidence and limits

All twelve frozen controls pass. Exact symbolic checks cover elimination, stationary exchange point, vacuum curvature, high-source asymptotic, the two mutations, response slope and remaining vacuum freedom. Lean checks the exact rational reciprocal-pair symmetry and its failure under unequal weights; the deliberate false equality exits1. Accepted proof axioms are standard, with no sorry. The Lean file certifies these finite algebra controls, not the full variational action or a physical kappa derivation.

Both footing labels have the same mechanism FAIL and physical-kappa NOT EVALUABLE. eta, C and the positive modulus kinetic coefficient remain unspecified/FITTED if selected. The pair of auxiliary sectors is a model assumption. No new particle species or cold component is adopted. No covariant completion or independent observational second prediction was obtained. Nothing has been pushed.

The useful design constraint is stricter than AZ19's: a symmetry can protect a relative stationary point while leaving the absolute response/vacuum matching free. A further mechanism must fix that invariant common scale AND maintain stability over its physically derived source domain. Adding a potential or cutoff selected to enforce the desired answer is not a solution.
