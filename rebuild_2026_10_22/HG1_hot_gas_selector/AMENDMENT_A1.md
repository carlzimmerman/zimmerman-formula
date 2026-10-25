# HG1 AMENDMENT A1 (implementation, before any graded number)

Written after the first run stopped at K3, before any D, Δ, power or class was computed or seen.

**What happened.** The first run passed K1 (+0.4162) and K2, then failed K3: the maximum relative change in g_bar under a
×1.1 distance rescaling was 9.0. Cause: the eRASS1 match radius is a fixed 0.5 Mpc, so rescaling every distance also
moved groups across the match boundary and flipped their X flag (a FAINT group gaining gas, or the reverse). That tests
the matching rule, not g_bar.

**Change.** K3 now rescales the match radius with the distances (0.5 × 1.1 Mpc in the rescaled build), asserts that every
X flag is identical, and then checks g_bar. This is what §5 says K3 checks ("g_bar is unchanged when every distance is
scaled"). The primary sample, the 0.5 Mpc match radius, the statistic, the classes and every other line are unchanged.
