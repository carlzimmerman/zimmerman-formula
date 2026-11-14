# BJ1 AMENDMENT A1 (2026-11-14, written 15:19 EST by the clock): a round-off tolerance on known answer (iv)

Written and committed alone after the first run of the profile-level known answers (`bj1_ka_tables.py`, committed in
3534ec5782; no boxes, no data, no gate) and before any matter-level, rotation-curve, lensing or forest number of this
lane exists. It changes no layout, case, gate, twin, bracket, label or lane word.

**What happened.** FROZEN_CRITERIA.md (9e7ce0dfe6) section 2, item (iv), reads "C non-decreasing" with no tolerance,
while (i), (ii), (iii) and (v) carry one. On the tables the smallest step of C between neighbouring nodes is -3.0e-17 to
-1.8e-16 of C_tot (every z and footing), so (iv) read to the letter fails in all 24 forest (z, footing) cells. Every
other item passes in every cell: (i) 0, (ii) at most 6.9e-16, (iii) 0, (v) at most 6.1e-16, (vi) at most 6.2e-16 / 0,
(vii) 0.

**Why it is round-off and not the junction.** The negative steps are already in the law's own layout: C_B = M_B - Bar
as FRZ1's layout and FZS1's Bar give it has steps down to -4.3e-16 of C_tot on the same grids (z 2.2, 3.0, 4.4, both
footings, haloes below v*), and C_R = M_R - Bar has none. The cold component is a difference of two nearly equal
enclosed masses near the centre and where the law's halo has reached its cap, so it carries rounding of order 1e-16 of
the total. The same design error was made in XJ1 (its amendment A1): a tolerance was left off one item of a list whose
other items have one.

**The amendment.** Item (iv) is read as **min step >= -1e-12 C_tot** (the tolerance frozen for (i) to (iii)).

**A second change, to a check that is mine and not frozen.** The script's "t-free" check (section 3's "t-free check
(no factor anywhere)") was written as bit equality of each node's C to C_B, Q_k or C_R at that node; C is recovered
as M - Bar, and (Bar + C) - Bar is not C to the last bit, so that check failed everywhere at the 1e-16 level. It is
read with a 1e-12 relative tolerance (a factor different from 1 shows at 1e-3 or more). The criteria's own check is
"no factor anywhere": the code has none (`bj1_lib.budget_row`).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
