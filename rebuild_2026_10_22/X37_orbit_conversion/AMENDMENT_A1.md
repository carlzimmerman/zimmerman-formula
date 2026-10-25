# X37 AMENDMENT A1 (pre-result: written with the script, before any graded number)

The frozen MUTATE line (§5) says the flipped exponent, f = exp(+N_orb/N★) capped at 1, must fail **K2**. That cannot
bite. Capped, the mutated f is identically 1, and K2 checks the unconverted (f = 1) quadrature, so it passes by
construction. The mutation does bite **K1**'s N★ → 0 limit: the mutated model keeps everything instead of returning C*.
The MUTATE requirement is therefore read as "`--mutate` must fail K1". Nothing else changes.

K2 is implemented with the substitution u = r^{3/4}. For f ≡ 1 the trapezoid rule is then exact, so K2 tests the
normalisation and the substitution, as frozen.

## A2 (POST-RESULT, implementation only)

RUN1 (`_RUN1` files, kept) failed K1's N★ → ∞ limit at 0.99923 instead of 1 to 1e-6. Cause: f was zeroed outside r_ta and
then averaged into the trapezoid. That half-weights the cell straddling r_ta, even though du = 0 beyond r_ta already
(u = min(r/r_ta, 1)^{3/4}). The zeroing is removed; the model is unchanged. RUN1's classes and grades are shown beside the
rerun in the README.
