# EUC21R against EUC21: COMPARISON

Written after `RESULT_BLIND.md` was committed (local `4927494fb7`; reading note `4265063117`). Only then did I open
EUC21's `RESULT.md`, its `euc21_results.json`, its run outputs and its driver.

kappa = 1/2 FITTED. Footings graded separately, never pooled. Adopts nothing; not pushed.

## Labels: full agreement

| Row, footing | EUC21 (lead) | EUC21R (blind) |
|---|---|---|
| Y1 canonical | ONLY A CUSP IS LEFT, UNCHANGED, ROBUST | ONLY A CUSP IS LEFT, UNCHANGED, ROBUST |
| Y1 alt | ONLY A CUSP IS LEFT, UNCHANGED, ROBUST | ONLY A CUSP IS LEFT, UNCHANGED, ROBUST |
| Y2 (footing-free) | WIDE LENSES HOLD MORE GAS PRESSURE, CHANGED, ROBUST | WIDE LENSES HOLD MORE GAS PRESSURE, CHANGED, ROBUST (the same on both footings) |

Both find no bracket tag on either row under the correction. Y1 keeps the same word in all five of ESZ1's brackets
and in F1a and F1b. On Y2 the CIB-deprojected map gives the same word, so the committed tag drops.

**Y2's CHANGED is now confirmed blind.** EUC21's limits say a blind re-grade is owed because one word changed; this
lane is that re-grade.

## Numbers: identical to the last byte

Each of the five runs has the same three ESZ1 output files (results file, per-lens file, log) in both lanes.
`cmp` finds all 15 pairs byte-identical: lead `f1` against my `harness`, `primary` against `corrected`, `F1a`, `F1b`
and `invert`. So every number derived from them agrees exactly. That covers the least predicted stacks, σ distances,
f_T, the model table, the brackets, Part C and its intervals, Part D, the cold-share reading and the check values.

Checks: both lanes pass every frozen check, and in both the twin exits 1 and bites. The lead's H5 is my R0 (ESZ1's
rules return the committed words from the committed file).

## Differences (none in a label or a computed number)

1. **Rounding slips in the prose, one on each side.**
   - Mine: `RESULT_BLIND.md` gives F1a's CIB-map Part C lower bound as +0.96. The value is +0.9549, so +0.95, which
     is what the lead wrote. The word is unaffected. I leave the committed blind file as it is and record the slip
     here.
   - Lead's: f_T for B30 on the alt footing is written 0.37. The value is 0.3646, so 0.36.
   - Lead's: "12 to 14 times" for the 100 kpc core's hiding factor. 1/f_T is 14.5 (canonical) and 12.2 (alt), so
     12 to 15.
2. **Route.** Both drivers use the same substitution text, asserted to match once. Both wrap EUC1's loader and
   redirect ESZ1's writes. They differ in mechanism:
   - The lead patches `builtins.open` for the whole process and executes the text as `__main__`.
   - I placed `open` in the executed module's own namespace and called its `main()`, turned off bytecode writes, and
     compared `git status --ignored` and the sha256 of every ESZ1 file before and after each run.
   - My runs took about 46 s each; the lead's notes say about 75 s.
3. **Reading of Y2.** The two readings agree in substance: the wide lenses' own stack did not move, the committed
   bound sat 0.20 below the line, and the new control set stacks lower (−2.14 ± 1.64, negative at 1.3 σ from zero
   in the lead's terms, 1.1 σ below the old −0.34 in mine). Each side adds one point:
   - **Lead:** the controls stay 0.18 dex lighter than the wide lenses.
   - **Mine:** only 15 of the 237 wide lenses keep their control. Even the twin, which moves the masses the other
     way, gives an excess (+5.30 [+1.15, +9.47]). So the committed NO EXCESS DETECTED was the fragile reading, and
     the word depends on which controls are drawn, a choice the criteria give no bracket for.

   Both say the word is not for or against the law.

## Bottom line

The blind re-grade confirms EUC21 on every label, footing and number. Y1 is ONLY A CUSP IS LEFT on both footings,
UNCHANGED and ROBUST: the cored hot-gas bodies stay excluded under the corrected stellar mass, at 10 to 64 σ.
Y2 changes to WIDE LENSES HOLD MORE GAS PRESSURE, ROBUST to F1a and F1b; the change comes from re-matched controls
and sits close to the line. Neither is a pass.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
