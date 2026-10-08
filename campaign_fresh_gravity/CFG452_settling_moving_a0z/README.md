# CFG452: the T15/T16 settling budget with a0(z) tracking ρ_DE(z)

Criteria: `FROZEN_CRITERIA.md` (fa8a989af, committed alone before the script). Script: `cfg452_moving_a0z.py`.
Outputs: `cfg452_moving_a0z.out`, `cfg452_results.json` (MUTATE: `*_MUTATE.*`).

**Verdict: a0(z) DOES NOT CHANGE THE BUDGET'S VERDICT, and it nudges the budget slightly the wrong way.**

With a0(z) = κc√(Gρ_DE(z)) from the DESI DR2 chains (p13c), the cold fluid relaxes toward a moving kernel supply since
z = 2. The cluster overdraft deepens by 0.003–0.004 (primary curve) on both footings, and no verdict class changes.

## Why the effect is small and has this sign
- In DESI's evolving dark energy, a0 was *higher* than today over z ≈ 0.05–0.9 (peak 1.035 at z ≈ 0.4, Pantheon+). It was
  lower only before that (0.88 at z = 2).
- The settling rate is slow (Γτ = 0.33 at R500), so every epoch since z = 2 counts about equally, and most of that time is
  at z < 1.
- The effective supply is therefore 0.3% (Pantheon+) to 5% (no SN) **above** today's. More supply means more settled mass,
  which means a deeper overdraft.

## Key numbers (M_cold/M_b; flat → primary DESI+CMB+Pantheon+; range over all DE curves)

| item | canonical 9.3603e-11 | alt 1.1312e-10 |
|---|---|---|
| clusters b = 0 | −0.801 → −0.804 (−0.79 to −0.87) | −0.997 → −1.001 (−0.99 to −1.07) |
| clusters b = 0.3 | −0.309 → −0.312 | −0.505 → −0.509 |
| groups b = 0.3 | +0.256 → +0.252 (positive) | −0.044 → −0.049 (knife-edge) |
| V3 MW-30 infeasible above | 186.5 km/s (unchanged: set by today's S) | 194.2 km/s |
| V4 floor/cluster gap | 1.40× → 1.41× WEAKENED (1.39–1.49×) | 1.71× → 1.71× STANDS (1.69–1.80×) |
| T16 verbatim intersection | EMPTY → a single point [0.0199, 0.0199] | [0.0162, 0.0164] → [0.0160, 0.0164] |
| V5 frozen (MW M_b 7e10) | EMPTY | EMPTY |

- **Only the Pantheon+ q16 curve helps, and only by 0.01.** It is the lowest a0 history (0.82 at z = 2): clusters −0.791.
- **The no-SN DESI+CMB curve hurts most:** clusters −0.865 and gap 1.49×.
- **On the canonical footing the T16 window reopens to a single λ under most DE curves**, because the cluster upper bound
  drops to 0.0199. This is a knife-edge, not a pass.

## What it would take
MUTATE plants a0 at half its present value over the whole history since z = 2 (r = 0.5). Even then, the clusters at b = 0
stay negative on both footings (−0.41 canonical, −0.57 alt), and only b = 0.3 canonical crosses zero (+0.08). No
DESI-allowed a0(z) comes close to that: the lowest 68% curve is 0.82–1.02 over the window.

## Model and controls
- Model: relaxation dM/dt = Γ(S(t)M_b − M) from z = 2, Γ held. The time map is from flat ΛCDM (Ω_m 0.3), shape only, with τ
  held at 10.3 Gyr. λ = 0.028, ρ, the deficits (CFG450) and the conventions are held as in CFG451. Footings are never pooled.
- C1: with flat a0 every number reproduces CFG451 to 1e-6.
- C2: the p13c inputs match (0.8779 at z = 2; 0.827/0.782/0.798 at z = 2.5).
- MUTATE: the history is seen. The cluster b = 0 row rises by +0.39 / +0.43 and the headline flips to MATTERS.
- One tooling fix before any reading: numpy here has `trapz`, not `trapezoid`, so the first run crashed. Changing the call
  changed no numbers.

## Caveats
- The settled mass uses T15's R500 density and M_b for the whole history, with no halo growth since z = 2. A growing halo
  would weight late times even more, where DESI's a0 is above today's.
- Only the DE curve's median and the Pantheon+ 68% band were run, not the full chain posterior.
