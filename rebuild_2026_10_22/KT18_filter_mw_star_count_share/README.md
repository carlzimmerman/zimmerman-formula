# KT18_filter_mw_star_count_share: ONLY ABOVE STAR-COUNT SHARE on both footings. At the star-count thick share 0.12, no in-prior cell passes the Milky Way under KT17's eps = 0.55 filter; alt misses narrowly (best D 1.12)

Criteria: `FROZEN_CRITERIA.md` (94562be676, with KT19 and KT20's), alone first, confirmed landed. `kt18.py` (KT17's code, Cassini and dwarf parts removed, cells restricted to fk = 0.12, all passing cells stored), `kt18.out`, `kt18.json`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Register K829.

450 in-prior cells per footing with thick share 0.12 (BV and BV2).

| | canonical | alt |
|---|---|---|
| passing all four | **0** | **0** |
| cells passing L1 v_c / L3 Ou | 7 / 0 | 58 / 28 |
| lowest K with v_c in line | 71.2 | 68.8 |
| best cell | BV2, Sigma_b 53.9, M_bb 2.12e10, v_c 220.8, K 72.7, Ou 103, D 1.72 | BV, Sigma_b 53.9, M_bb 2.12e10, ht 0.35, hk 1.08, v_c 220.9, K 71.3, Ou 64, D 1.12 |

## Reading
- **KT17's Milky Way pass needs more thick disc than star counts give.** At the measured share the filter still pulls K down (alt reaches 68.8 at the v_c line), but no single cell holds v_c, K, the K profile and Ou's outer curve together. Alt's best misses K by 0.5 and Ou by 4, at Sigma_b and M_bb +2 sigma.
- So the honest form of KT17's MW result: **passes only at thick share 0.26 or above, about +3.5 sigma from star counts.** That's a real weakening of the lead. Not excluded: the box has no share between 0.12 and 0.26, and the 0.12 +- 0.04 value is itself one paper's star counts (PROVISIONAL in RF1).
- KT17's other passes (dwarfs, Cassini) don't depend on this.

## Checks
No fk 0.12 cell was in KT17's stored list, so there's nothing to reproduce directly. C2 mass checks pass (within 1.2e-3). The code path is KT17's, whose MUTATE covers it; not rerun, as frozen.
