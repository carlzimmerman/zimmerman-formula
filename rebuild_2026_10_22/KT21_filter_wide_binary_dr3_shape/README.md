# KT21_filter_wide_binary_dr3_shape: BOTH CONSISTENT on both footings. The DR3 inner wide-binary shape is flat (Q +0.001 +- 0.028), Newton fits best (z +0.1), the filter sits at -1.1 sigma and plain QUMOND at -1.6 sigma; the two differ by only 0.014 in Q, so DR3 can't separate them

Criteria: `FROZEN_CRITERIA.md` with `kt21_sys.py` / `.out` / `.json` (the pre-data systematic), alone first, confirmed landed. `kt21.py`, `kt21.out`, `kt21.json`, `kt21_MUTATE.out`, `kt21_MUTATE.json`. No download; the 6,210-pair DR3 extract on disk; the Gaia DR4 pre-registration is untouched, and this is not a DR4 result. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Register K832. 7 s, 0.29 GB.

Q = ln median vtilde(2 <= y < 10) - ln median vtilde(y >= 10), y = g_N(s_proj) / a0. sigma_sys 0.020 (eccentricity 0.016, triples 0.012, noise 0.003).

| | canonical | alt |
|---|---|---|
| pairs in M / H | 2947 / 2051 | 3195 / 1582 |
| median vtilde M / H | 0.5527 / 0.5521 | 0.5525 / 0.5516 |
| Q_obs | +0.0011 +- 0.0280 | +0.0016 +- 0.0300 |
| Newton Q_pred, z | -0.0010, +0.08 | -0.0030, +0.15 |
| plain Q_pred, z | +0.0464, -1.62 | +0.0477, -1.54 |
| filter Q_pred, z | +0.0321, -1.11 | +0.0338, -1.07 |
| Labels | all three CONSISTENT | all three CONSISTENT |

Beside (g_e 2.32e-10; eccentricity index 1.0, 1.4): plain z -1.64 to -1.81, filter -1.13 to -1.32, Newton about -0.1. Same picture.

## Reading
- **The data are flat to 0.1 percent between the two bins**, where plain QUMOND with the simple nu predicts a 4.7 percent rise and the filter 3.3 percent. Both lean the wrong way by 1-1.6 sigma; Newton matches.
- **The filter doesn't remove the inner boost as much as KT20's table suggested.** KT20 compared the filter to plain at the same separation. In Q, both bins are suppressed, so the filter's rise between them stays about 70 percent of plain's.
- **DR3 can't decide between them here.** The gap between the two predictions is 0.014, half of sigma. sigma_sys (0.020) dominates the error; a decisive test needs it near 0.005, i.e. the eccentricity trend and triple fraction known per bin. That needs DR4's radial velocities and NSS screening, not more pairs.
- What it does say: if the flat inner shape holds at smaller errors, both laws as written (simple nu tail) are in trouble, the filter slightly less.

## Limits
Velocity rescale at the current r_3D, not orbits integrated in the modified potential; 1D external-field form; one eccentricity index per mock (others beside). The inner shape says nothing about the 10-20 kAU level.

## Checks
C1 gamma against KT20, 0.0 relative. C2 Newton Q_pred -0.001 / -0.003 (within 0.005). C3 bins 1582-3195 pairs. C4 bootstrap seeds 0.0196 / 0.0203 and 0.0224 / 0.0223. All pass, exit 0. MUTATE (nu = 1): the three Q_pred are identical, exit 1.
