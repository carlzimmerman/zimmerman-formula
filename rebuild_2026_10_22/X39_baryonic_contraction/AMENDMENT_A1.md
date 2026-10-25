# X39 AMENDMENT A1 (POST-RESULT, check code only)

RUN1 (`_RUN1` files, kept) failed K1's point-mass test (max rel 5.6). The test was mis-built: for the inner shells, the
closed form puts r_f below the radius grid (r_f ≈ k(1+F)r_i²/M_p < 10¹⁸ m), where interpolation clamps. The test now uses
only shells whose analytic r_f lies on the grid. The contraction code, the model and every graded number are unchanged;
the rerun reproduces RUN1's grades.

Also check code: the K1 test grid goes from 400 to 40 000 log points. At 400 points the log-linear interpolation error (1.3e-4) exceeded the 1e-6 line while the mutation sat at 0.47; the finer grid tests the solver, not the interpolation.
