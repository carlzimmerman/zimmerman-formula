# Differentiated momentum constraint diagnostic

The saved coarse p_lambda is redundant: its spatial part is reconstructed at
every RHS evaluation. Raw residual alone can penalize truncation of this
auxiliary field, while a meaningful consistency check asks whether the
reconstructed time derivative agrees with the native canonical equation.

Differentiate p_x=b_x(r+C S), C=2M²exp(4b)/p, S=2b_xx+3b_x²:
 (partial_x+b_x C S/p) p_t
 =b_xt p_beta+b_x[r_t+4C b_t S+C(2b_xxt+6b_x b_xt)].
Augment by the evolved mean p_t. Use the projected coarse b_t,r_t lifted to
the evaluation grid, solve this linear equation, and compare with the full
native canonical p_t. Record low represented and fine-only discrepancies,
normalized by max|p_t|. Criterion <=1e-6 in the represented part is a proposed
consistency requirement for a mean-only momentum formulation; it does not
by itself certify continuum accuracy or override spectral/domain stops.
Test t=1 reference and n255/n511 legacy stopping states as diagnostics.
