# X50 AMENDMENT A1 (POST-RESULT, check implementation only; committed alone before the rerun)

Run 1 (kept as `x50_phantom_floor_run1_K1FAIL.out` / `_results_run1_K1FAIL.json`) ended UNDECIDED (checks) because K1's
"Q monotone and < 1 on 1e-6..1e8" sub-test failed. Cause: floating-point cancellation, not physics. The script evaluated
the sympy form Q = √y √(y+4)/2 − y/2, which loses all digits for y ≳ 3e7 (the first non-increasing step is at
y = 3.5e7). The other K1 sub-tests passed (lim Q = 1; dS/dy = ν − 1; S closed form vs quadrature 8e-15).

Fix (implementation only):
1. K1 evaluates Q in the cancellation-free identity Q = y(ν − 1) = 1/ν(y), which sympy verifies symbolically in the
   script (the identity is added to K1 as a sub-test, so K1 becomes stricter, not looser). The grid, the limit test, the
   tolerances and every other check are unchanged.
2. A3's central log-slope for the spherical-equivalent exponential disc printed an unsimplified sympy expression; it is
   now evaluated at y_c = 0.1, 1, 10 (reported only).
3. The dwarf section's reported X49-reproduction flag used EM1's rounded Mpc for ρ_c; it now uses X49's own constant
   (reported only; it does not enter any class).

No graded quantity, gate, class, data choice or MUTATE rule changes. The graded lines of run 1 must reappear unchanged.
