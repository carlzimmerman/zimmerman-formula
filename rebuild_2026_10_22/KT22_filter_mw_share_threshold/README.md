# KT22_filter_mw_share_threshold: alt PASSES WITHIN +2 SIGMA (9 cells at thick share 0.20, none at 0.16); canonical NEEDS MORE THAN +2 SIGMA (none at 0.16 or 0.20; KT17 found its first passes at 0.35)

Criteria: `FROZEN_CRITERIA.md`, alone first, confirmed landed. `kt22.py` (KT18's code with the fk 0.12 cells copied at 0.16 and 0.20), `kt22.out`, `kt22.json`, `kt22.log`, `kt22.time`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Register K833. 11 minutes, 0.64 GB.

450 in-prior cells per footing per share.

| | canonical 0.16 | canonical 0.20 | alt 0.16 | alt 0.20 |
|---|---|---|---|---|
| pass all four | 0 | 0 | 0 | **9** |
| L1 v_c / L3 Ou | 12 / 0 | 19 / 0 | 70 / 32 | 76 / 46 |
| lowest K with v_c in line | 70.2 | 69.6 | 68.5 | 67.9 |
| best D | 1.52 (Ou 91) | 1.36 (Ou 81) | 1.00 (v_c 222.5, K 70.8, Ou 59) | 0.88 |

Alt's 9 passing cells: all BV2 (thick R_d 2.0 kpc), R_d 2.6, M_bb 2.12e10 (one at 1.76e10), Sigma_b 50.5 (one at 53.9); v_c 222.2-223.3, K 68.3-70.7, Ou 52-57. Strict h fails in all (3.26-3.35 vs 2.72 +- 0.30). Q5 doubled grid on the best: dK +0.05, dv +0.08.

## Reading
- **The threshold sits between 0.16 and 0.20 on alt.** Alt's best at 0.16 is on the edge (D 1.00); at 0.20 it passes. Canonical's outer curve (Ou) is the line it can't meet below 0.35.
- **Independent share measurements (PROVISIONAL web lookup, 2026-11-03, not on disk):** star counts (BH&G16) 0.107; Mackereth+2017 APOGEE high-α, ratio 18 %, share about 0.15; Lian+2022 (MNRAS, DOI 10.1093/mnras/stac1151) APOGEE chemical thick disc 5.62 against thin 15.69 Msun/pc^2, **share 0.264**, scale height 0.85 kpc; Lian's [Fe/H] > -0.5 subset 3.76, share 0.19. The definitions differ (geometric vs chemical), and the measurements span 0.11 to 0.26.
- So alt's Milky Way pass needs the chemical-thick-disc share (Lian's metal-rich subset or all of it), not the star-count one, and it still sits at Sigma_b and M_bb at the high edge of their priors. Canonical needs more than any of the measured shares.

## Checks
C1 KT18's best cell per footing re-solved, v_c and K identical (0.0 relative). C2 smoothing mass within 1.2e-3 on all eight lightest and heaviest cells. Exit 0. MUTATE not rerun (KT17's covers the code path), as frozen.
