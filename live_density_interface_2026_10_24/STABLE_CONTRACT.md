# LD-17: stable nonlinear field energy in the tensor implementation

LD-16's directional check failed. Step sweep showed cancellation rather than
an analytic derivative disagreement: errors4.5e-6 at step1e-6 versus1.3e-8 at
step1e-4. The tensor port evaluated -log1p(-u)-u directly in the very small-u
infinite tail, losing digits before multiplying by t^-4. The parent model
already uses a small-u series; restore that known numerical safeguard, with
sum u^j/j through j10 for u<.01. No force or physical energy is changed.
Require the directional check at THREE step sizes, all below1e-7; do not
relax the failed tolerance. Repeat feasible cold benchmarks and joint front/
seed tests with compatible gravity/W quadrature and stable tail evaluation.
Earlier tight optimizer stopping claims remain provisional numerical evidence.
