# Original-input domain correction propagated

The original-input mass mismatch has now been propagated rather than ignored.
domain_propagation_001 forms halo delta boxes relative to the OLD baseline
mass enclosures, reconstructs all65 analytic law profiles, and derives positive
relative majorants for their extensions. No physical parameter or cut changes.

The exact review checks all223262 halo and234065 law coordinates. It strengthens
the perturbation majorant from the main analytic-interval budget3.209701e-15 to
3.257642253e-15 to cover the exported outward binary64 law boxes as well. The
uniform envelope scale is1.0000000000000033. These are derived error bounds,
not concentration or profile fits. The stronger review budget is authoritative.

The previous positive operation-path U majorants bound absolute ideal
projection of the extension by epsilon*sum(U). Clipping deltas to the old
boxes preserves their prior coefficient/anchor budget; projecting the excess
with the ideal map avoids double counting. Source and catalogue arithmetic
budgets scale by lambda: mass-dependent majorants are positive linear and
lambda>=1 also covers their additive underflow terms. The exact covariance,
four nuisance templates, witness and law cutoff remain unchanged.

All15 run controls and9 exact/self-adversarial review controls pass. Independent
70-digit algebraically different law evaluation validates325 selected values.
All arrays/errors are finite, input hashes stable, and the completed bounded
run manifest validates. The exact reviewed conditional dual lower becomes
569.5338626095037, versus feasible-law upper+9=163.34346325076024. Thus the
original-input analytic correction does not erase this conditional local gap.

Analytic interval scope: parent M,R and baryons are L-independent; columns
increase as L^(5/4); branch signs are fixed on[3.75,3.751]. The previously
proved decreasing logarithmic B slope gives nondecreasing compact halo mass
for r<R. At r>=R truncation fixes mass to M. The compact roots exist at the
lower endpoint; increasing column cannot cause saturation before the upper
endpoint. Root/peak domain checks satisfy the documented analytic source
limits. These facts justify analytic endpoint ordering, not every floating
optimization/libm branch or arithmetic operation in the original evaluator.

This is still not a real-L or global obstruction. Original floating solver,
libm, and the precise analytic-versus-numerical likelihood interpretation
remain to be reconciled. The fixed numerical law comparator upper is not
silently promoted to an analytic recomputation of that comparator. See
SOURCE_SOLVER_BRIDGE_ROUTE.md. No new observed passing or failing point is
claimed by this enclosure calculation.
