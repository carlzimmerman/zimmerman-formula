# LD-13: retain unfinished states and test a resolved intermediate mesh

The n256 charged recovery exceeded its 240s cap before a final output; this
is resource-inconclusive, not instability. The n192 pressure refinement may
also remain unfinished. Use n128 quadratic mesh for the beta20 charge-free
candidate, enough to improve on n96 while reducing dense-SLSQP cost. Limit
each minimization to1000 iterations, save a full checkpoint every50, and
perform material+phase perturbations ±1kpc. Residuals, iteration limits and
intermediate checkpoint status remain explicit; a stopped state is not
called equilibrium. Same physical energy, conservative transfer and gates.
Every saved checkpoint can support a genuine resumed optimizer audit rather
than rerunning an inaccessible final state from scratch.
