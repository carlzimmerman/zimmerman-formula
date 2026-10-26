# IC1_inner_cluster_band — AMENDMENT A1 (POST-RESULT; numerics only; committed alone before the rerun)

**What happened.** Run 1 (`ic1b_fix_run1_K1FAIL.out`, kept) failed K1: B_iso vs direct quadrature, max relative
1.8e-6 against the frozen 1e-6. The other K1 parts passed (large-x 2.9e-3 < 2e-2, small-x 9.0e-7 < 1e-3, mass 4e-15).
K0 PASS on both footings. Class FAILS on both footings (seven OS1-passing MID/OUTER cells fail; G-IN-Mall goes to
+0.21 / +0.22).

**Cause.** Linear log–log interpolation of the Lane–Emden mass table, which has 6000 points over ξ = 1e-4 – 1e8. It is
a table-resolution error, not a physics change.

**Amendment.** The table grows to 30000 points over the same range. Nothing else changes:
- the K1 threshold stays 1e-6;
- the classes, the q rule and every other criterion are unchanged;
- the diagnostics are rerun with the same table, so D4 is consistent.

Run 1's class numbers are kept in the record. If the rerun's cells move by more than 0.01 in Z anywhere, the README says
so. If K1 still fails, the lane reports K1 FAIL; the tolerance is not moved.
