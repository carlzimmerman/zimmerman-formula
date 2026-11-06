# PF08 mean-momentum reduction

The differentiated-constraint diagnostic finds represented canonical-rate
errors ~1.1–1.5e-7 at legacy n255/n511 raw-momentum stopping states, versus
~1.6e-12 at t=1. The saved nonconstant p_lambda is redundant: every stage
reconstructs it from beta,r_mom and its mean. Make that elimination explicit.

Evolve only lambda, beta, mean(p_lambda), r_mom; reconstruct the full spatial
p_lambda on the evaluation grid. This is a constrained formulation, not
permission to discard a physical equation. Validate against the former state
representation at t=.5/1. Require the represented differentiated momentum-
constraint rate to agree with canonical p_lambda,t to relative1e-6. Continue
checking full reconstructed constraints, domain margins and every physical
field's upper-third spectrum <=1e-3. Record the full-grid rate discrepancy too.
The previous raw residual remains a diagnostic of an auxiliary truncation,
but is no longer an equation on the independent saved state.

Use inherited n/dt/evaluation bounds. Check temporal and spatial convergence
at shared resolved times; numerical accuracy stops still are not physical
singularities. Preserve full independent state and reconstructed polarization
derivative for exact restarts. No smoothing or postshock rule is introduced.
