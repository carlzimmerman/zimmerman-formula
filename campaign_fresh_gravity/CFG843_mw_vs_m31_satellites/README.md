# CFG843 — MW vs M31 satellites: does the excess depend on the host?

Criteria: `FROZEN_CRITERIA.md` (e28f35029, before the script). Run: `python3 cfg843.py` (MUTATE `CFG843_MUTATE=1`). Seconds.

## Result — CLASS: **SAME**
- 12 MW and 12 M31 satellites (CFG828 Δ, Υ_SFH): offset at matched g_bar c (M31 − MW) = **+0.055 ± 0.117 dex**; means
  +0.36 (MW) and +0.33 (M31); slope b = −0.22 per dex of g_bar (the excess grows toward low acceleration).
- Below g_bar = 10^−11.9 (8 + 8): c = +0.053 ± 0.177, means +0.44 / +0.50: SAME.
- **Reading:** two different hosts and independent kinematic surveys give the same excess at the same internal
  acceleration. The excess is not environmental; it is a property of the faint dwarfs themselves (or of a systematic shared by
  all faint-dwarf kinematics). Together with CFG838/839 (no tidal signal) and CFG842 (no capture from the host), this points
  to the dwarfs' own formation, not their surroundings.

## Controls
- K1 PASS (pooled slope = polyfit). MUTATE bites: +0.3 dex on M31 → DIFFERENT.

κ = ½ fitted; cold energy mass required; not theory closed.
