# CFG840 — robustness of CFG829 (isolated late-type lensing at the dwarfs' accelerations)

Criteria: `FROZEN_CRITERIA.md` (bb354e8da, before the script). Run: `python3 cfg840.py` (MUTATE `CFG840_MUTATE=1`). Seconds.
CFG829's loader and amplitude function are reused unchanged.

## Result — CLASS: **FRAGILE** (by the frozen rule), with a robust core
| variant (blue/disc lenses) | A | (A − 1)/σ | (2.75 − A)/σ |
|---|---|---|---|
| primary (= CFG829) | 1.016 ± 0.086 | +0.2 | +20.2 |
| window −0.3 dex | **1.229 ± 0.096** | **+2.4** | +15.8 |
| window +0.3 dex | 1.022 ± 0.084 | +0.3 | +20.5 |
| window widened to 1e-14 | 1.068 ± 0.072 | +0.9 | +23.5 |
| lens M★ −0.2 dex | **1.312 ± 0.118** | **+2.6** | +12.2 |
| lens M★ +0.2 dex | 0.902 ± 0.069 | −1.4 | +26.9 |
| Sérsic n < 2 (disc-like) | 1.066 ± 0.086 | +0.8 | +19.7 |
| alt footing | 0.928 ± 0.078 | −0.9 | +23.3 |

GAMA all-isolated (V4) 1.72 ± 0.21 vs KiDS all-isolated 1.44 ± 0.05: consistent (z +1.3).

- **Fragile part:** "isolated late types sit exactly on the law" does not survive every variant. Shifting the window 0.3 dex
  lower, or lowering B21's lens stellar masses by 0.2 dex, puts blue lenses 1.23–1.31× above the law (> 2σ). The honest
  statement is: isolated late types sit within ~0.1 dex of the law at these g_bar (A between 0.90 and 1.31 over the variants).
- **Robust part:** in every variant the dwarfs' ×2.75 is excluded by ≥ 12σ. The dwarf excess is not reproduced by isolated
  late-type galaxies at the same g_bar under any of these choices.
- CFG829's reading is amended accordingly (note appended there and in THEORY_CANONICAL v3).

## Controls
- K1 PASS: the primary reproduces CFG829 exactly. MUTATE bites: g_obs × 2.75 makes every variant fail.

κ = ½ fitted; cold energy mass required; not theory closed.
