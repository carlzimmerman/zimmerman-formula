# EUC17 AMENDMENT A2 (POST HOC)

Committed alone, 2026-11-13, **after** the as-frozen run (0fc36cf7bc) and with its numbers known. Post hoc throughout.
The as-frozen word stays first in the RESULT: **NOT EVALUABLE** (check K0 failed). Everything read under A2 is
labelled A2.

## 1. Why K0 failed, and the change

K0 failed on one number: the upper bootstrap bound of f₂₅ for the EUC10 reading (11 lenses), 0.818 against the
committed 0.909, on both footings. Every point value, every other bound and every committed word reproduced.

The bound of a fraction on N lenses moves in steps of 1/N (here 1/11 = 0.091). Which step a resample lands on
depends on the order of the lenses in the array, and the reading is rebuilt here from the committed per-lens file,
whose row order is not the source lane's internal order. The frozen 0.01 tolerance on bounds cannot hold for a
fraction on 11 lenses. This is a design error in the check, not a difference in any statistic.

**Change:** for the readings rebuilt from committed per-lens columns (R3, the EUC10 reading, EUC1's conditional
readings), the tolerance on the bootstrap bounds of a **fraction** (f₂₅, f₀) is max(0.01, 1/N). The tolerance on
the bounds of b_med stays 0.01, and the point tolerances of A1 stay.

## 2. Script correction (not a change of criteria)

The as-frozen script passed bracket F5 (lenses with n > 9.5 dropped) through the 5 % "no mask" rule of criteria §1.
That rule is for lenses without a mask file. F5 drops 8.6 % of P on purpose, so the rule fired and every row printed
FRAGILE (F5). Under A2 the rule counts only lenses without a mask file, as the criteria say. The words before the
rule are in the as-frozen results file and equal the primary words in every row.

## 3. One post hoc reading, declared here before it is computed: T (wings removed)

The frozen guard S1 says a corrected scale that sits well above scales built on total magnitudes is a reason to
doubt the extrapolated wings. S1 found a median correction of 0.071 dex on P, but 0.13 to 0.15 dex on the wide
lenses and up to 0.56 dex on single lenses. The primary correction keeps EUC1's infinite Sérsic body, so part of
its mass lies beyond the region where light was measured.

**T:** the primary body with every star beyond the sphere of the mask radius removed,
`M_3D(<r) = (M★ / f) × M3D_frac(min(r, R_mask))`. Inside the mask it is the primary body; outside there is nothing.
Its in-mask projected mass is slightly below the catalogued mass (the line-of-sight wings are gone), so T is the
less generous reading. Computed with EUC1's own engine for R1 and R2 (source at infinity) and for R3 (certified
source redshifts as stored, four decimals), law S, both footings, with the rows' own statistics and words.

T sets no label and changes no word. It answers one question: do the corrected numbers rest on stars beyond the
observed region?

Checks for T: **KT1** with the cut removed the code returns the primary corrected boosts to 1e-9; **KT2** for R3 the
engine at the stored source redshifts reproduces the committed per-lens boosts to 2e-3, otherwise T is not computed
for R3 and the RESULT says so.

## 4. What does not change

The correction, the rows, the lines, the words, the brackets, the twins and the guards. No row is called a pass.
