# CFG903 AMENDMENT A1: the completeness brackets (after stage A's first run, before any pair or lensing computation)

Committed together with the first-run stage script (`cfg903_stage.py`, `cfg903_lib.py` as they ran) and its outputs,
which are kept unchanged as `cfg903_stage_run1_K0e_fail.out` and `cfg903_stage_run1_K0e_fail_results.json`. This happened
after stage A's first full run and **before any neighbour-pair histogram, two-halo vector or χ² was computed**. Only the completeness treatment changes; everything else in
FROZEN_CRITERIA.md (bb665cf4f) stands.

## Finding

Stage A's sanity check K0e (finite completeness factors for every lens) **FAILED**:
- the frozen C1 gives R_c1 = 1.29 / 2.07 / 17.4 / 106.5 at z = 0.2 / 0.3 / 0.4 / 0.5;
- the frozen C2 is undefined above z ≈ 0.35, because no slice galaxy lies above m_lim(z).

**Cause: the frozen reference slices are not fair samples of the massive end.** Unmasked pool galaxies (log M★ > 7) by
photo-z slice:

| z_phot | n | n(log M★ ≥ 10.6) | n(log M★ ≥ 11) | max log M★ | brightest r |
|---|---|---|---|---|---|
| 0.06–0.08 (frozen C2 slice) | 18,823 | 0 | 0 | 10.30 | 15.3 |
| 0.10–0.12 (frozen C1 slice) | 35,976 | 80 | 0 | 10.80 | 15.3 |
| 0.15–0.17 | 42,558 | 1,991 | 25 | 11.20 | 16.0 |
| 0.20–0.22 | 48,531 | 7,638 | 396 | 11.30 | 16.3 |
| 0.25–0.27 | 50,540 | 17,301 | 1,520 | 11.45 | 16.7 |

Nothing brighter than r ≈ 15.3 is in the bright sample. The massive galaxies at z ≲ 0.15 are brighter than that, so
they are absent. The cause (a bright-end cut or saturation in the sample, or photo-z behaviour) was not investigated.

A ratio against such a slice measures that deficit, not the missing faint mass. So the frozen C1 and C2 factors are
unusable as defined.

## Replacement (the only change)

**Mass function: a complete-slab estimate.**
- Bins are 0.1 dex in log M★, from 8.5 to 12.0.
- The total-mass density per bin is
  ρ_tot(m) = Σ M_b (1 + 5.364 N(M_b)) / [χ(z_c)³ − χ(0.10)³].
  - The sum runs over unmasked pool galaxies with 0.10 ≤ z_phot < z_c(m).
  - N(M_b) is CFG902's declared fixed point.
  - z_c(m) = min(0.50, largest z on the 0.01 grid with m_lim(z) ≤ m). Over that range the bin is above the
    5th-percentile limit (m_lim as frozen).
- Bins with z_c < 0.12 are dropped; m_f is the lower edge of the lowest kept bin.
- The footprint area is common to every bin and cancels in every ratio.

**C1′ (primary): faint-end up-weighting.**
- The missing mass ρ_tot([m_f, m_lim(z_l))) is carried by the observed neighbours just above the limit.
- A neighbour with m_lim(z_l) ≤ log M★_j < m_lim(z_l) + 0.5 gets weight 1 + f(z_l), with
  f = ρ_tot([m_f, m_lim)) / ρ_tot([m_lim, m_lim + 0.5)).
- f = 0 where m_lim(z_l) ≤ m_f.
- Hosts and other massive neighbours are **not** scaled.
- Assumption stated: the missing faint galaxies cluster like the faintest observed ones.

**C0 (lower):** no correction (unchanged).

**C2′ (upper):**
- The whole neighbour sum (hosts included) is scaled by R_c′(z_l) = ρ_tot(≥ m_f) / ρ_tot(≥ m_lim(z_l)).
- This is the frozen C1's "same clustering per unit mass" assumption, with the slab mass function.

Randoms are clones and inherit the same per-lens factors and the same per-pair rule.

## Added diagnostic (reported only, no verdict weight)

Because the massive neighbours of lenses at z ≲ 0.15 are missing from the catalogue (the table above), the primary
two-halo vector is also computed from I0 lenses with z_l ≥ 0.17 only (variant v7, B21 weights, C1′). This shows how
large the low-z bright-end loss is. The rest of the primary is used for the verdict unchanged.

## Not changed

Classes and thresholds, all other brackets (W, I1/I2/I5, P0/P2, E0/E2, uniform weights, M1), the controls K0–K3 and
MUTATE, the score, and the compute limits.

κ = ½ FITTED; footings never pooled; framework-native; not theory closed.
