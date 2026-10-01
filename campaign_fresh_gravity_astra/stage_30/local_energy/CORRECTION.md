# FGF043: time-integrability qualification for the general flux corollary

The original frozen ROOT_DERIVATION.md SHA256
45236fe01ee93bdcedbe785bcb2948d408b4ea05869aa81235095e2cfec2ca27
is preserved unchanged. The root-only auditor pressure_extrema identified that
the paragraph after estimate(2) passes from spatial L1 convergence to compact
spacetime residual convergence without explicitly imposing time integrability.
The later mention of uniform-in-time versions does not by itself supply that
missing hypothesis for a merely pointwise-in-time reading.

Correct interpretation: estimate(2) proves spatial flux convergence for each
comparison sequence. For time-dependent sequences, require its right-hand side
to tend to zero in L1(0,T), together with spacetime L1 convergence of full energy
density and field energy flux. A sufficient concrete hypothesis is the uniform-
in-time small-energy setup and corresponding fixed velocity cap from FGF042 on
a fixed finite time slab. Under those hypotheses, all these L1 spacetime limits
hold, and testing the density/flux derivatives gives the stated distributional
local-energy residual limit. Pointwise-in-time spatial convergence ALONE does
not justify integration over time and is not accepted as sufficient.

The stationary counterexample, initial and wall accounting, amplitude control,
all residual rates and the spatial estimate(2) are unchanged. No new computation
or stronger general evolution theorem follows. This clarification is credited
to the independent root-only audit cue, not represented as originally frozen.
