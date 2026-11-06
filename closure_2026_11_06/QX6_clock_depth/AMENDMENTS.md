# QX6 amendments (POST-RESULT, labelled; written after the graded and MUTATE runs, before these checks run)

Graded and MUTATE outputs were produced first (qx6.out, qx6_MUTATE.out). Two frozen controls missed their lines:
- iter 2 MUTATE (amplitude x1e4) moved X-COP's mean by -0.179 canonical and -0.185 alt. The line was <= -0.2.
- iter 3 MUTATE (step at sqrt(k_g k_x), amplitude F_req median) gave X-COP rms 0.106 / 0.105 against the 0.10 line,
  so it did not pass G-X. With amplitude 1 it failed too. That control does not bite.

As frozen, the iter 2 and iter 3 grader-based labels therefore have no power. The amendments below are declared
before running. They can strengthen or weaken a FAIL. They cannot produce a PASS.

A1 (iter 2). Repeat the power control at amplitude x1e5. It bites if the mean moves by <= -0.2 on both
footings. iter 2's result rests on the analytic factor: the largest F - 1 the rho_DE tie allows is 2.5e-4,
against >= 1.1 needed. That factor does not depend on the grader.

A2 (iter 3). Does ANY single-step F pass G-X? F = A for k >= k_t, else 1. Grid: A from 1 to 10 in steps of 0.01;
k_t from 60 log points across W = (k_g, k_x), plus k_t in the X-COP key range (up to max X-COP key). This is a class
existence check, like iter 1's E1. If no (A, k_t) passes on a footing, single-step thresholds, coincidences included,
are DEAD on X-COP's profile shape alone, whatever their native origin. If some pass, report the region; it stays
CLUSTER-SET, a FAIL by rule.
