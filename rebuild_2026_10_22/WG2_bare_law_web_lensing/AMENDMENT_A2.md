# WG2 Amendment A2: POST-RESULT, written after every run's r was visible

## K4 fails as frozen
K4 compares the measured and input initial power. As frozen it uses the mean of the per-bin ratios over 0.01-0.1 h Mpc⁻¹, and it reads **1.979: FAIL**. So the lane as frozen reads **NOT EVALUABLE**, and that stays on record.

The per-bin ratios show why. They sit at 0.93-1.07 except at the nodes of the baryons-only transfer function d_b(k), where the input power at the bin centre is near zero:

| k (h Mpc⁻¹) | ratio |
|---|---|
| 0.028 | 17.71 |
| 0.087 | 5.82 |
| 0.055 | 1.52 |
| 0.059 | 1.27 |
| 0.024 | 1.22 |

- With no cold term, d_b keeps its acoustic sign changes at z 50.
- The mean of ratios is not a sound statistic for a field with nodes. The initial conditions are right:
  - median per-bin ratio 1.004;
  - ratio of summed power 0.970.

## A2a: K4b
K4b is the ratio of summed measured to input power over the same bins, with the same 10 % tolerance. It reads 0.970: PASS. Labels are reported two ways:
- as frozen: NOT EVALUABLE;
- under A2: K1-K3 plus K4b.

## A2b: grader code fix
This changes no rule. The run files hold the steps actually taken: the 200 log steps plus the snapshot epochs merged into the grid, 219 or 220. The first grade matched on 200 and so found no members. The grader now reads the requested step count from the run tag, and the step-taken count is kept beside it.

## Robustness of the A2 labels to the initial normalisation
- Under R1, r moves from 11.4 to 14.1 across a factor 4 in A_s (B2, TIE).
- The member closest to a threshold is R0 B1 A_s 4e-9, at r 0.307 against 0.5.
- An initial-power error of the size K4 might have flagged (factor 2) would not move any R1 label. It could move only that one R0 member.

κ = ½ FITTED; not theory closed.
