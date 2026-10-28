# EF1 amendments

## A1 (POST-RESULT, committed alone before the rerun): K1 compared the wrong power

**What happened.** The first run (`run1_K1FAIL.out`, kept) failed K1. The check compared √(vir) = 0.08411 against
ex = (2/9)√y = 0.00703. In X1's C3a convention, ex is the *squared* dispersion, so it must be compared with vir itself:
0.08411² = 0.00707 against 0.00703, which is 0.0026 dex and inside the 0.005 dex tolerance.

**Fix.** K1 compares log10(vir / ex). This changes the check only; no rule, input or graded number.

**What the first run showed.** BASIN FIELD DOES NOT HELP on both footings.
- IC 1613 stays at Z −6.75 canonical and −7.45 alt.
- The external-field shifts are ≤ 0.0035 dex for every field dwarf.
- K0 reproduced X1's tables exactly (|d| 0.0000).
