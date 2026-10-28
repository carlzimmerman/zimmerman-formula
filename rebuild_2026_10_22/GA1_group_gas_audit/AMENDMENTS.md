# GA1 amendments

## A1 (POST-RESULT, committed alone before the rerun): Step 0's random-number order

**What happened.** The first run (`run1.log`, kept) failed K0. The point D reproduced HG2 exactly (−0.2940), but the
bootstrap interval came out [−0.5221, −0.0848] against HG2's [−0.511, −0.076].

**Cause.** The script drew HG2's bootstrap with a fresh generator, before the power estimate. HG2 and HO1 draw the power
estimate first, then the bootstrap, from one `default_rng(SEED)`.

**Fix (code order only; no rule, sample or statistic changes).**
- Power, then bootstrap, from one generator seeded with SEED, as HG2 does.
- K0 compares against HO1's own reproduced values (`lo0`, `hi0`, `D0`) rather than the rounded −0.511 / −0.076.

**What the first run showed.** Every audited variant classed GAS AUDIT DOES NOT HELP on both footings. The PRIMARY gap
was 0.668 against 0.523 unaudited, with the base picture's D_pred above zero in every variant. The interval shift
(≈ 0.01 dex) cannot change any class. The rerun is the graded run.
