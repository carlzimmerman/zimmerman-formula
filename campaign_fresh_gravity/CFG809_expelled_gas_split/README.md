# CFG809: H-EX with the supply split (expelled share free). FAIL (1 of 3), now OVERSHOOTS

The split is implemented as stated. K2: free = 5.364 (bc − retained) to within 1.6% (median, eRASS1). K1: the ALL control
reproduces CFG727 exactly.

| | eRASS1 MID / OUTER | eRASS1 terciles MID | ACCEPT OUTER | eFEDS |
|---|---|---|---|---|
| ALL (no free; = CFG808) | 1.40 / 0.89 | 1.02 / 1.65 / 1.45 | 0.92 PASS | χ² 29.4 FAIL |
| CFG727 (free = supply − law of condensed) | 0.93 / 1.05 | 1.29 / 1.32 / 0.64 | 0.48 FAIL | 19.4 PASS |
| **CFG809 H-EX split** (canonical) | **0.76 / 0.64** (Z −5 / −6) | 0.64 / **0.93** / 0.69 | 0.50 FAIL | **15.9, p 0.044 PASS** (alt p 0.087) |

**Verdict: FAIL** (eFEDS passes; eRASS1 and ACCEPT fail by overshooting). Same result on both kernels and both footings.

**Reading.**
- Freeing the **whole** expelled share is too much mass.
  - eRASS1 is overshot in both outer bands and in the low and high terciles. Only the middle tercile fits.
  - ACCEPT is overshot ×2.
  - eFEDS groups fit best of any rule so far.
- The data sit **between** "no free cold energy" (ALL: short ×1.4) and "all expelled cold energy free and bound" (H-EX:
  over ×1.3).
- A physical candidate, **not** a fit: freed cold energy keeps the orbital energy of its infall. The unbound part should
  leave the catchment with the expelled gas, and only the bound part stays. The framework's own Method A tracks this energy
  (CFG637 E_res), so the bound fraction can be **derived** rather than chosen. That is the next lane.

MUTATE M1 (free removed) gives MID 1.38; M2 (shuffled) gives 0.72. Both bite.

κ fitted; not theory closed.

**Note added (CFG812 finding):** in eRASS1 and ACCEPT the catchment f_ret is pinned at 0.60 by the condensed-fraction floor (condensed fixed at 0.20 M_gas), so census/retention changes did not act there; see CFG812 README.
