# HL2_combined_mass_pairs: NO GAP [SOURCE-DEPENDENT] as frozen, conditional on HL1's AMENDMENT_A1. Post-result, all three samples, 81 clusters: g = +0.031 ± 0.020. A labelled bracket, never a framework grade

Criteria: `FROZEN_CRITERIA.md` (da7b5808f7, committed alone), `AMENDMENT_A1.md`. `hl2.py`, `hl2.out`, `hl2_results.json`, `hl2_MUTATE.out`, `hl2_post.py`, `hl2_post.out`, `FETCH_LOG.md`. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework.

## Frozen read
K1 dropped Okabe + Martino (width 4.45 % against 3 %, offset −3.3 %), so the graded set is Mahdavi+13 and Zhang+10. **g = +0.031 ± 0.035 on 53 unique clusters: NO GAP.** Dropping Zhang gives +0.069 ± 0.043, NOT POWERED, hence [SOURCE-DEPENDENT]. Weak as a verdict, because it rests on a thin second source. Note that 9 of Zhang's 12 overlap Mahdavi's.

## Post-result, not graded
| Set | n | g | SE | would read |
|---|---|---|---|---|
| Okabe + Martino alone | 47 | +0.031 | 0.034 | NO GAP |
| Mahdavi + Okabe + Martino | 78 | +0.042 | 0.028 | NO GAP |
| **All three** | **81** | **+0.031** | **0.020** | **NO GAP** |

K1's width likely comes from Martino's table giving one r500 per cluster beside two instruments' masses (see `hl2_post.out`). That's my reading; it doesn't restore the source to the grade. The two big samples disagree cluster by cluster, though: on their 19 shared clusters g is −0.022 (Mahdavi) and +0.033 (Okabe + Martino), and M_WL differs by 0.106 dex in the median, a calibration difference flagged by K4.

## What this changes
1. **The 0.12 gap LF1 left doesn't appear as lensing against hydrostatic on the same clusters.** All three samples read about +0.03; 0.12 is over 4 SE from the post-result combined value. So hydrostatic bias of that size isn't what these published pairs show.
2. **This corrects HL1's post-result reading.** There, one sample's Y_WL and Y_hyd sat near LF1 and X-COP, and I called it suggestive. Okabe + Martino doesn't repeat it: its log Y_hyd is −0.106 ± 0.013, well below X-COP's −0.04.
3. **Lensing shares at R500 are low in every sample, including those not using KiDS:**

| Sample | log Y_WL | log Y_hyd | f★ 0.034 |
|---|---|---|---|
| Mahdavi+13 | −0.097 ± 0.022 | −0.046 ± 0.023 | |
| Zhang+10 | −0.066 ± 0.030 | −0.048 ± 0.039 | |
| Okabe + Martino | −0.126 ± 0.041 | −0.106 ± 0.013 | |
| LF1 M3, own read, KiDS | −0.115 ± 0.054 | | |
| X-COP | | −0.042 | |

So a KiDS-only shear bias looks unlikely as the whole of LF1's deficit. Inside R500 a share below cosmic isn't itself a failure of the fair-share rule, which is set at R₂₀₀. It's X-COP's hydrostatic share at 1.5 R500 (−0.011) that reaches the cosmic value.

4. **What's left of the tension is sample or radius, not mass method.** Candidates: X-COP's clusters being gas-rich or otherwise unusual; gas between R500 and R₂₀₀ that eRASS1 clusters don't have; LF1's cylinder, with its unresolved outer term. These pairs stop at R500, so none of them tests the outskirts, which is where G-OUT-M3 lives.

## Limits
Published NFW fits and published calibrations; X-ray-luminous samples; WL noise is common to the three masses in Mahdavi and Zhang, and not in Okabe + Martino, where each is at its own radius. M_hydro above and below 5.4e14 gives −0.010 ± 0.050 and +0.063 ± 0.037; z above and below 0.232, +0.086 ± 0.055 and +0.022 ± 0.052. None is a trend.

## Checks and disclosures
K3 Mahdavi alone reproduces HL1's g, PASS. K2 parse PASS; 3 of Martino's 50 lack an Okabe M500 match by name and aren't paired (A115S, Zw1231, A1758). K4 flags Okabe's M_WL against both others (−0.106, +0.198). I checked this for a unit error: the table is in h⁻¹, converted at h 0.7, correct by the paper's macro. MUTATE swap and shuffle BITE. Rerun identical. Frozen radius rule removed by A1 before pairing, since it cut on the statistic. Zhang's lack of z means only name matching there. The first runs failed in the parser before any g.
