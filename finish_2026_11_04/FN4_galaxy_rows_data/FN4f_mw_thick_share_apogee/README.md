# FN4f_mw_thick_share_apogee: NOT MEASURABLE. Without APOGEE's selection function the count ratio fixes only 1/h_hi − 1/h_lo, so the thick share follows the assumed thin scale height (0.16 to 0.62) and cannot place the law's Milky Way cells

Criteria `FROZEN_CRITERIA.md` (committed alone before any download); amendments `AMENDMENTS.md` (A1 join, A2 units, A3 flags, A4 bins), committed before any number. Data: the two owner-approved APOGEE DR17 files (`fn4f_fetch.json`; no selection function). κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## Label (frozen): NOT MEASURABLE
Three frozen conditions fire (`fn4f_share.out`):

| Check | Result | Line |
|---|---|---|
| KA1 planted two-population sample | PASS: 0.2018 and h_hi 0.917 recovered (true 0.20, 0.90) | 0.01, 0.05 kpc |
| KA2 the α-bimodality at [Fe/H] −0.3 | PASS, 0.147 | 0.10–0.22 |
| **KA3 thick scale height** | **FAIL: h_hi 1.686 kpc** | 0.54–1.26 kpc |
| **KA4 join** | **FAIL: 91.5 %** | ≥ 99 % |
| **Band width** | **0.92** (B = [0.102, 1.023]) | ≤ 0.15 |

Stage B (placing the cells) was not reached. The record stands as it was: X5's box carries share 0.2633, where form R has 1 canonical and 6 alt in-prior passing cells; forms A and Q pass nowhere from 0.12 to 0.35.

## Why, checked as hard as a pass would be
- **KA4 is the position test, not the join.** APOGEE_ID and TELESCOPE agree on 100.000 % of the 733,901 rows (the tables are row-matched). My amendment A1 also required positions within 1″. astroNN's positions differ by more than 1″ for about 7 % of rows (likely another epoch, PROVISIONAL) and are missing for 1.8 %. The tolerance was not widened. The post-result run shows the join choice changes the share by 0.001.
- **KA3 is the frozen trough finder.** The KDE minimum between [Mg/Fe] 0.05 and 0.25 sat on the window edge in 8 of 10 [Fe/H] bins: below [Fe/H] −0.4 the low-α sequence is too sparse to leave a trough. The fitted line, [Mg/Fe] = 0.227 + 0.267 [Fe/H], slopes the wrong way.
- **The band is the estimator, without a selection function.** With the line fixed, the result still depends on the assumed thin scale height h_lo. The table below uses the standard APOGEE line instead (post-result, `fn4f_post.out`); κ is −2.35 per kpc.

| assumed h_lo (kpc) | implied h_hi (kpc) | thick share |
|---|---|---|
| 0.20 | 0.38 | 0.159 |
| 0.25 | 0.60 | 0.195 |
| 0.30 | 1.01 | 0.253 |
| 0.35 | 1.96 | 0.359 |
| 0.40 | 6.52 | 0.620 |

At the box's middle value (h_lo 0.30) the share is 0.253, with h_hi 1.0 kpc inside KA3's range. That sits beside X5's 0.263 and the chemical 0.264. But the frozen h_lo range alone moves it from 0.195 to 0.359. The count ratio cannot separate the two scale heights. Each population's own vertical profile needs the survey's selection function, which the owner knew was missing. **So the share is not measured here. It would be, given the selection function or an independent thin-disc scale height to about ±0.02 kpc.**

## MUTATE
`FN4F_MUTATE=1` ([Mg/Fe] shuffled): κ collapses to −0.019 per kpc, h_hi = h_lo = 0.30, KA3 fails, label NOT MEASURABLE, exit 1, as required. The real run reads NOT MEASURABLE too, so here the twin cannot tell the two apart.

## What would make this measurable
APOGEE DR17's selection function (not approved, not fetched), or an independent thin-disc scale height at the Sun to about ±0.02 kpc. With either, the frozen estimator plus the standard split would place the cells. The trough finder would also need replacing; that is a new freeze.

## Files and compute
`fn4f_fetch.py` and `.json` (the download); `fn4f_share.py` and `.out`/`.json` (the frozen run; `_MUTATE` twin); `fn4f_post.py` and `.out`/`.json` (post-result). `cache/cols.npz` (gitignored) holds the columns read from the two tables. One thread; 98 s; max RSS 0.82 GB. Rerun: `fn4f_share.json` byte-identical.

κ = ½ FITTED. Not theory closed.
