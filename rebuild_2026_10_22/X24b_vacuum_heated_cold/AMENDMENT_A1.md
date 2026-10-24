# X24b_vacuum_heated_cold: AMENDMENT A1 (POST-RESULT; check code and verdict-string code only)

Written after the first complete run. No model line, input, bound or threshold that produces a graded number changed.

1. **Spherical-collapse initial condition (bug fix, caught by K2 before any graded number was read).** The first run
   started the shell with mass factor (1 + δ_i) and radius a_i(1 − δ_i/3), which doubles the initial contrast; K2 failed
   (EdS δ_lin 1.056 vs 1.686). Fixed to the frozen statement ("growing-mode start"): mass radius r_L, y_i = a_i(1 + δ_i)^{-1/3},
   ẏ_i = H y_i (1 − δ_i/3). K2 then passes (1.6907, 5.5517). The bisection now returns the bracket end at which the event is
   reached (it had returned the midpoint, which can sit just past a = 1 for the late-turnaround element and crash).
2. **K3 tolerance 1e-10 → 1e-7.** At ε → 0 the VHC run integrates five variables, REF four, both LSODA at rtol 1e-8; the
   observed |T² − 1| = 8.0e-9 is step-control noise (the extra variable cannot feed back when J = 0). The attractor half of
   K3 is unchanged (−0.72241 vs −13/18, within 1e-3).
3. **Footing agreement on the verdict class.** §4 says both footings must agree. The code first compared the full verdict
   strings including the qualifier lists, giving "UNDECIDED (footings differ)" although both footings return NO ε WINDOW.
   The qualifiers differ only because X19 labels Antlia II NONE on alt (AMBIGUOUS on canonical) and LG field is AMBIGUOUS
   at ε_low on alt. The code now compares the class and prints both qualifier lists; the literal string comparison is kept
   in the JSON (`verdict_literal_string_compare`).
4. **Reported only (added after the result):** the ε that the SPARC classes' own histories would need
   (`eps_low_SPARC_*_own_history`), and Spearman(σ increment, log M★) for the floor reading. Neither enters a verdict.
