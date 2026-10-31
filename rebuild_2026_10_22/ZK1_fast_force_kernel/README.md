# ZK1_fast_force_kernel: the zooms' force sum in compiled code, about 60× faster on one core, with the same results

Criteria: `FROZEN_CRITERIA.md` (c7d8c2518b), committed before any comparison. `x48_force.c`, `build.sh`, `x48_fast.py`, `zk1_check.py`, `zk1_k3.py`. κ = ½ FITTED. Not theory closed.

`x48_zoom.py` isn't edited. `x48_fast.py` imports it and replaces its `accel` with the same softened direct sum and Λ term, in C. Numpy built a 700 MB array per chunk and called `pow`; the C loop vectorises. On an M4 Max core under load, N = 57,777 takes 1.8 s a force, against 118 s. A zoom that took two days takes under an hour.

## All checks pass
| Check | Result |
|---|---|
| **K1** force, three real particle sets | max \|Δa\|/median \|a\| 9.4e-14, 1.6e-13, 3.2e-13; median \|Δa\|/\|a\| 4e-15 to 6e-15 |
| **K2** 20 steps with each kernel | max \|Δx\| 2.7e-16, max \|Δv\| 4.6e-15; dt sums identical |
| **K3** full reruns from the ICs, 10¹³ ng 48, seeds 1–3 | same step counts (894, 1132, 969); η_S 8.83, 18.66, 13.65 and c_nfw 3.75, 7.75, 5.60 unchanged; \|Δ ln M(<r)\| median 0.0000, max 0.005 |
| **MUTATE** ε × 1.01 | fails K1, as it must |

K3 also says something about the zooms: at this level rounding doesn't grow into a visible profile difference over a full run, so seed-to-seed scatter is real sample variance, not chaos.

## What it changed
A4's last two zooms finished in minutes. ZN1 now runs all nine seeds at 10¹², 10¹³, 10¹⁴. X80 and A5 run in hours. Live-disc runs (LC1) became affordable. Each switched run's folder holds `ZK1_SWITCHED`.

`compute_queue/YIELD` holds the heavy queue (L1's 512³ runs, X1's lattice) while these run, so nothing competes for cores. Remove it to release the queue.
