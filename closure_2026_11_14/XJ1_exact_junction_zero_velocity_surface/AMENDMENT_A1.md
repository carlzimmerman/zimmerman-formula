# XJ1 AMENDMENT A1 (2026-11-14, about 12:10 EST): a round-off tolerance on known answer KA-E (iv)

Written and committed after the profile-level known answers were run (`xj1_ka_tables.py`, no boxes, no data) and before
any box, flux, matter-power or lensing number of this lane exists. It changes no case, gate, twin, bracket or label rule.

**What happened.** FROZEN_CRITERIA.md (ef8ccdde98) section 4, KA-E (iv), reads "t >= 0" with no tolerance, while (i),
(ii) and (iii) carry one. On the tables the smallest t is -4.0e-16 to -7.3e-16 at z 2.2 to 2.8 (both footings): for the
lightest haloes the law's halo has reached its cap C_tot inside R_set, so t = [C_tot - C_B(R_set)] / [C_tot - C_R(R_set)]
is the ratio of a difference of two equal numbers to a finite number, zero to rounding. Read to the letter, (iv) fails
in 7 of 24 (z, footing) cells. Every other item passes in every cell: (i) 0, (ii) at most 6.7e-16, (iii) 0, (v) 0 / 0,
(vi) 0; KA-Z passes ((i) 0; (ii) 0.46 kpc against the 0.6 kpc line).

**The amendment.** KA-E (iv) is read as **t >= -1e-12** (the tolerance already frozen for (i) and (v)). The design
error is mine: a tolerance was left off one item of a list whose other items have one.

**What it means physically, stated before any gate number.** t = 0 means the law's halo, unscaled, already holds the
halo's whole cold component inside R_set, so under the exact junction nothing of it is left between R_set and r_ta.
That is the case for the lightest haloes at z 2.2 to 2.8 (t rises with redshift: smallest t 0.09 / 0 at z 2.8, 0.26 /
0.10 at z 3.0, 0.79 / 0.72 at z 4.4). The layout stays non-decreasing ((iii) is exactly 0).

Post hoc to the tables, prior to every graded number. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
