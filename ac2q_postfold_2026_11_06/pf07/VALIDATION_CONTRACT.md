# Independent checks of adapted/padded evolution

Before claiming a repaired solver, check exact Hamiltonian cancellation and
coordinate-chain equivalence to the original canonical RHS on a smooth test.
Compare padded homogeneous evolution with the closed form at t=.1 (<1e-8).
Compare a mode-4 perturbation with the independently derived two-field linear
ODE at t=.01, amplitudes 1e-8 and 1e-9, dt=.000625. Require relative beta
error <1e-2 and inspect amplitude scaling; no temporal convergence follows
from a subtraction-limited linear test.

For every saved padded run compare raw coarse and interpolated momentum
residuals with the reconstructed residual; record projection correction,
idempotence, and the fine-grid correction outside represented modes. Report
these separately. Require raw normalized momentum <=1e-7 for using a run as
converged evidence. Compare same-time fields on a common Fourier grid.
