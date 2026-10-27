# LD-5: separate numerical saturation cap from reservoir support

LD-3 includes a converged n192 domain2 state but fails the .05dex law gate;
its domain4 state hits the arbitrary .97 cap. Neither is a success.
Use n128 quadratic mesh, domain4, K=3,10,30, beta1000,k120,tau1, starting
from that mobile-density n192 state. Raising the exact-evaluation branch
to u=.9999 and inequality cap to .9997 eliminates the earlier artificial
.97 wall without permitting u>=1. Active-cap states remain inadmissible.
Increasing free-phase entropy explicitly tests whether pressure can keep
unconverted source out of the interior; it is not predicted by the formula.
Density, phase and outer reservoir remain variable. Edge mass, actual law
and both stationarity residuals are mandatory. Results require subsequent
mesh/domain/displacement and alternate-start checks before a solution claim.
