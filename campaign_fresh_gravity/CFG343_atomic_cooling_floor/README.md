# CFG343: atomic-cooling floor for the UFD cold mass

**Frozen rule output: "RESOLVES". Corrected reading: NOT. The frozen rule was flawed, and this is recorded rather than hidden.**

The rule graded on z alone. CFG317 already warned that its z(log R) falls as R grows because its frozen error floor grows, not because the offset closes.

At z_f = 8 the floor gives:
- M_cool = 3.8e7 Msun;
- median R_cool = 700 (log 2.85).

The UFD **offset is unchanged** at +0.32 dex (canonical) / +0.30 (alt). Only the error grew, which moved z from 3.8 to 1.6.

**The cooling floor is 6-8x short** of the R the UFDs need (log R_need 3.65-3.74). At z_f = 6 it is 4-5x short and the offset moves only to +0.22.

Controls:
- C1 passes: the normalisation is exact.
- C2 fails, kept: the classicals get median R_cool of about 5. Under rule S that is below their R_need of about 200, so it is harmless, but the frozen check was wrong.
- MUTATE passes: with T_vir = 1e3 K (H2 minihalos), R falls to 22.

**Lesson:** grade on the offset, not on z alone, whenever the error budget depends on the parameter being tested.
