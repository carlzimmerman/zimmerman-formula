# CDE-L4C boosted PPN — VERDICT: alpha_3 = O(1), STRUCTURAL KILL (2026-09-01)

**CDE-L4C dies at PPN, exactly as predicted, and for the DEEP reason that it PASSED the DOF count: the
MOND lapse equation C_MOND is a SECOND-CLASS CONSTRAINT (rank-4 Dirac calc), hence INSTANTANEOUS
(omega-independent, elliptic 1/k^2 response), hence alpha_3 = O(1). The same property that removes the
scalar graviton (N_grav=2) forces the preferred-frame instantaneity that violates alpha_3. Excluded by
~1e19x (pulsar |alpha_3|<4e-20) / ~1e6x (LLR |alpha_3|<4e-7).**

Script: `cde_l4c_ppn_alpha3.py` (boosted (k,omega) response, negative control passes).

## The mechanism (the DC-019/York pincer, now proven for CDE-L4C)
- A constraint has NO time-kinetic term => its response is the c_s^2 -> oo limit R = 1/k^2, OMEGA-INDEPENDENT
  (instantaneous). A propagating (retarded) carrier has R = 1/(k^2 - omega^2/c_s^2), which carries an O(w^2)
  RETARDATION term (frame velocity w enters via omega = k.w for a boosted source).
- alpha_3 = 0 IFF the interaction is retarded/momentum-conserving. The instantaneous constraint LACKS the
  retardation term the covariant theory needs, so a preferred-frame residual survives at O(w^2/c^2):
  **g00 residual = -w^2/(c^2 k^2)  =>  alpha_3 = -1 (representative O(1) value).**
- NEGATIVE CONTROL: a retarded carrier at speed c gives ZERO residual => alpha_3 = 0. That branch requires a
  PROPAGATING scalar -- exactly the scalar graviton CDE-L4C removed to get N_grav=2.

## THE PINCER (airtight for the preferred-foliation local class)
  N_grav=2  <=>  MOND carried by a second-class CONSTRAINT (no propagating scalar)
           <=>  MOND response INSTANTANEOUS (elliptic, omega-independent)
           <=>  alpha_3 = O(1)  (no retardation to conserve momentum).
**You cannot have N_grav=2 AND alpha_3=0 for a MOND theory: alpha_3=0 needs a retarded (propagating) carrier
= the scalar graviton that N_grav=2 removes.** The Laplacian trick frees the FLRW zero mode but does NOT make
the k!=0 constraint retarded. This closes CDE-L4C and, with it, the whole strict-2-DOF preferred-foliation
local-constraint route -- it is the DC-019/York wall, now with the mechanism fully exposed.

## Scope / honesty
Principal (k,omega) extraction of the retardation structure. The exact alpha_3 coefficient (-1 here) needs the
full boosted 1PN solve; but alpha_3 = O(1) vs 0 is structurally FORCED and robust (it is the presence/absence
of the retardation term, not a fine coefficient). Layer A (a0 = c^2 sqrt(Lambda/32pi)) untouched.

## Final CDE-L4C scorecard
PASSED (principal level): exact kernel mu=1-e^{-y} + deep-MOND cubic; GR recovery; a0<->Lambda promotion
(a0^2=GV/4); no-slip Phi=Psi; the lambda-steal Dirac-preservation crux (the sf61 killer -- EVADED); the DOF
count N_grav=2 (rank-4 second-class ACs, det ~ k^8 lambda_par^2, Phi,Psi nonzero+sourced).
DIES: PPN alpha_3 = O(1). It got further than any previous strict-2-DOF attempt, then hit the same
preferred-frame wall. Verdict: STRUCTURAL KILL at PPN.
