# Diagnostic continuation after sound-speed failure

The initial run stopped before stellar integration because max dP/dE exceeds 1.
Independent full-quadrature derivatives at three step sizes confirm ~1.074335
at the pressure-zero surface, so this is not merely table interpolation noise.
Preserve the failed run and its script snapshot. Continue the same TOV range as
a formal diagnostic, recording sound-speed ranges and explicitly rejecting a
physical causal perfect-fluid interpretation of its entire surface branch.
This does not establish acausal propagation of the underlying canonical scalar;
it exposes a limit of the adopted barotropic averaging. No radial-fluid stability
certificate or real-field star is claimed from this continuation.
