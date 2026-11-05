# Additional implementation controls, pre-result

Independent review of the initial code identified two control-scope gaps
and one domain-reporting correction. The original physical run and its
inputs remain unchanged.

1. Its `Newtonian_zero` evaluates a zero force through the orbital integrator.
   That tests the integrator only. The new control injects R=1 and all its
   derivatives zero through the actual shared primitive API, then executes
   the same Monopole construction, A, B, Gaussian-ball and orbital pathways.
2. Its plain-QUMOND control removes the curvature response entirely; it is
   not an omitted-return mutation. The new control evaluates the local B
   divergence without the outer Gaussian, differentiating b_r with three
   step sizes. At the .1pc and1pc widths its answer must differ from the
   full returned B by >1e-4 in acceleration/a0 in at least one retained
   planet/footing case. This is a code-discrimination control, not a proposed
   physical law or a change to any observational cut.
3. The initial `max_i1_argument` is the semimajor-axis value. The eccentric
   orbit reaches up to1+eccentricity times that radius. Report that larger
   bound and directly compare six/eight series terms there. It must stay
   below .02, the domain declared by the derivation.

All model-null outputs must be exactly zero; both omitted-return derivative
differences and the physical difference are reported. No old numerical
result or threshold is replaced.
