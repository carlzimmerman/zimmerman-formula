# A1: independent controls and isolated refinement

The initial dressed runs complete. Before attempting the bare control, review
found that the zero-rank feedback matrix was not handled by the original
square-root implementation. A new unit control reproduced that exception.
response_v2.py treats zero feedback as the identity. The dressed physics and
matrices are unchanged. Original code and runs remain immutable.

Review also found that the first ODE-residual diagnostic scaled with forcing
amplitude. It was not a relative residual. Version 2 divides by amplitude
as well as source norm and names the result explicitly. It adds an independent
high-frequency current sum rule; none of these edits retunes a physical result.

The joint baseline ladder reaches <1% differences in all five integrated
works at levels 1 and 2. It does not isolate individual errors or guarantee
long-time response convergence. Authorize isolated changes to L quadrature
(40→64→96 if needed), radial count (10→12→16 if needed), Fourier harmonics
(24→32), orbit phases (1024→2048), Krylov count (768→1152→1536 if needed),
and the same pulse duration (20→40 dynamical-time units). These controls
discriminate orbital quadrature, spatial representation, spectral truncation,
time evolution and narrow/coherent resonance behavior. They do not change
the frozen forcing frequency set or choose a favorable physical state.

Run bare controls at identical final grids and pulse choices. Publish any
unresolved convergence, including core-restricted work and late-time moments.
Every execution retains the original per-run resource caps.
