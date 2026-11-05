# Diagnose the failed radial-box convergence check

The original evidence/spectrum run is retained as failed: every case misses
the2% low-mode ladder, by19-30%. Two40-cell cases have negative modes that
are absent at80/160. Constraint residuals are small, scaled condition numbers
are about1e10, and the independent Laplacian control converges normally.
These observations do not establish a physical instability or a code bug.

Hypothesis to discriminate: the midpoint mixed discretization is underresolved
on these background gradients. Hold the same background interpolants,
quadrature, boundary conditions, arithmetic and equations fixed; evaluate
the b=.1 cases at160,320,640 cells. The160-cell repeat must reproduce the
recorded eigenvalues. No tolerance or original outcome is changed. Continue
using the original2% low3 convergence criterion for the last pair and record
all discrepancies. This is a new refinement experiment, not a relabelled run.

The copied spectrum_refine.py changes only the selected case subset and cell
ladder; diff against spectrum.py is inspected before running. There is no
change to the variational Hessian or physics. Single-core bounded180s run,
under1GB. Unresolved result remains NO VERDICT. If it stalls, the next
discriminator is constraint conditioning versus fixed-interpolant/background
error, not repeated refinement without an identified convergence pattern.
