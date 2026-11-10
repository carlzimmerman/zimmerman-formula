# DG1 amendment A1 (POST HOC: run 2's numbers were seen): G5's L_need on the adiabatic edge

TEST lane; relabels nothing. kappa = 1/2 FITTED; not theory closed. Committed alone, before the rerun that produces the
committed outputs.

## What was wrong

The frozen G5 says: "L_need,i solves P(L) = Delta_B,i on the edge (L_need = 1 if Delta_B,i <= 0)". The script took
L_need = infinity whenever P(L = 1e6) < Delta_B,i, i.e. it assumed P rises with L for all L. That holds on the NR edge
(g_hist - g_N rises with L because gl'(x) > 1) but not on the AD edge. On the AD edge P(L) rises to a ceiling and then falls:
a very large loss blows the cold shells far out, so the cold mass left inside r_1/2 shrinks, and P goes negative for
L >~ 1e3. Example at central values (canonical): Coma Berenices P_AD = +0.55 at L = 30, +0.62 at 100, -1.30 at 1e6, target
+0.50. A root exists near L = 22, but the script returned infinity. Draco's ceiling is +0.28 at L about 30 against a target
+0.63, so infinity is right there.

Run 2 (canonical and alt) printed G5 FAIL on the AD edge with "median L need inf" in all three graded classes. Part of that
is this bug.

## The fix (to the frozen definition, nothing else)

L_need = the smallest L in [1, 1e6] with P(L) = Delta_B,i. It is found by scanning log10 L on 241 points in [0, 6] and running
brentq on the first sign change. It is infinity only if the ceiling max_L P(L) is below Delta_B,i. Each row's AD ceiling
and the L where it is reached are printed. The NR edge is unchanged; a check prints the largest change of NR's L_need,
which must be below 1e-4 relative.

## Also disclosed (no change to any rule)

- **Run 1** stopped at KA4 before any grading. The AD edge at L = 1 gave P = 3.1e-6 against the frozen "exactly", because the
  cold mass at r_1/2 was interpolated between shell-grid points. r_1/2 was put on the shell grid, and KA4 then reads
  0.0e+00. No graded number existed at that point.
- **G2's plant power on the AD edge is 0.50 on canonical**, exactly at the frozen line (< 0.5 reads NO POWER). The frozen
  rule is applied as written: 0.50 has power. RESULT.md states what the label would rest on if it fell below.
- numpy's matmul on this machine (macOS Accelerate) raises spurious divide-by-zero / overflow RuntimeWarnings for finite
  inputs (a random 1000 x 10 product does it too). The permutation statistics were checked finite.

kappa = 1/2 FITTED; not theory closed. Relabels nothing.
