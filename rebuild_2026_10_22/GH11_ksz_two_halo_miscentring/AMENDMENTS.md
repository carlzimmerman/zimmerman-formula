# GH11 amendments (after the first run failed K3 and K4; that run's Q2 and Q3 are discarded)

The first run gave b = 0 in every fit, so its "BUDGET SUPPLIED" had no two-halo removal at all. Three defects:

1. **Projected hole (design error in the frozen text).** R_hole removed every neighbour within 1 Mpc on the sky, including unrelated galaxies along the line of sight. That carves a hole in the projected field, so disc − ring goes negative. **Fix:** exclude a neighbour only if it is likely same-halo: R < R_hole **and** |Δv| < 500 km/s. The ±2000 km/s window and R_hole values are unchanged. The 500 km/s value is new, picked after this failure.
2. **K4 compared unlike positions.** Rotated lenses were compared with displaced positions around the unrotated lenses, so footprint differences failed the null. **Fix:** displaced positions are taken around the rotated lens.
3. **Normalisation.** T_n was divided by its maximum, which was a tiny value when most of T_n was negative; K3 failed from this. **Fix:** normalise by max |T_n|.

Criteria, classes and every other choice stand.

4. **Half-grid shift (code bug, found after run 2).** The template in run 2 had the same shape for all weights and holes, so it was an artefact. Two centred images were convolved without an ifftshift, so the template sat half a grid (22′) from the lens. K4 passed because the artefact was the same in the null. **Fix:** ifftshift the gas image in the convolution. Run 2's Q2 and Q3 are discarded too. Gas models were not affected (K1).

5. **No further template fix (decision after run 3).** All checks pass in run 3, but the template's shape is set by the hole: T_n is negative to 7′ with R_hole 1 Mpc, and much shallower with 0.5 Mpc, which moves A(1.8) from 0.54 to 0.84. Three tries is enough, and a fourth would be tuning, so the template is reported as unusable. No result depends on picking a hole.
