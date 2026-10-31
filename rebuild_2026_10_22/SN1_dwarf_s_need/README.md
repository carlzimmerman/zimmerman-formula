# SN1_dwarf_s_need: on EM1's M200 no S fits the dwarfs, not one S and not a power law. Without M200, the classes share a minimum S of 46–64. The measured rule falls short on any M200 line

Criteria: `FROZEN_CRITERIA.md` (eeaf540c64), committed alone before any script or number. Scripts `sn1.py` (frozen), `sn1_post.py`, `sn1_post2.py` (written after seeing the frozen result, no verdict). κ = ½ FITTED. Footings never pooled; here they differ only in Monte Carlo s. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

## Frozen verdicts (same on both footings)
| | verdict | numbers (canonical) |
|---|---|---|
| **V1** one S, EM1's M200 | **NO ONE S** | best S 204, max \|Z\| 2.88: ultra-faints +2.88, LG field −2.88 |
| **V2** S9 (M200/1e9)^p | **COLLAPSE SLOPE EXCLUDED**; no p admitted | at p 0.24 best max \|Z\| 2.86, S9 1096 |
| **V3** join to ET1's bands | **NO JOIN** | V2's region is empty, so the join fails by default |
| **V4** S_min, no M200 | **ONE S_min** | band 46–64 |

**Why V1–V3 fail: the M200 line, more than S.** Ultra-faints and M31 others don't reach E = 0 at S = 3000 (+0.25, +0.24). M_need exceeds EM1's whole M200 in 15 of 31 ultra-faints, 4 of 25 bright M31, 2 of 5 M31 others, 1 of 8 classical, 0 of 13 field. No S can supply that.

| class | lg M200 (EM1) | S_need smooth | S_need Burkert | S_min (dex sd) |
|---|---|---|---|---|
| MW ultra-faint | 5.72 | not reached | not reached | 41 (0.11) |
| bright M31 | 7.46 | 374 | 809 | 31 (0.15) |
| M31 others | 6.49 | not reached | not reached | 78 (0.33) |
| MW classical | 7.60 | 117 | 192 | 71 (0.09) |
| LG field | 8.43 | 64 | 92 | 54 (0.08) |

S_min's Spearman: r₁₂ −0.24, M★ −0.02, g_N +0.31. The rule's S at lg M200 9 is 29.4, below every class's S_min. S_min is a lower bound: it puts each dwarf at its own peak, r₀ ∝ r₁₂. ONE S_min is overlap of class medians; system-to-system scatter is wide, and it doesn't say one halo family does this.

Smooth core at Σ_a0, EM1's M200 (E, Z), canonical: ultra-faint +0.413, +3.27; bright M31 +0.109, +1.03; M31 others +0.486, +1.41; classical +0.019, +0.13; field −0.128, −1.78. Alt fails ultra-faints +3.17 and field −2.18.

## Post-result, no verdict: free line lg M200 = a + b (lg M★ − 7)
EM1 in these terms: a 8.48, b 0.90.

**Measured rule × k, any line in a 6–11, b −0.2 to 1.6:**
| k | 1 | 1.25 | 1.5 | 2 | 2.5 | 3 | 4 |
|---|---|---|---|---|---|---|---|
| lines admitted | 0 | 0 | 0 | 0 | 48 | 42 | 42 |
| best max \|Z\| | 5.53 | 4.45 | 3.60 | 2.20 | 1.41 | 0.93 | 0.68 |

So **the collapse rule, as measured, fails with M200 freed: it is short by more than × 2.** × 2.5 gives about 130 at lg M200 10, above ET1's [52, 85] there, so that normalisation does not carry up to SPARC's lowest bin.

**Flat S inside ET1's lowest band (`sn1_post2.py`; a step 0.05, b −0.6 to 2):** S 56–89 is admitted, and S 50 only near the Z line.
| S | lines admitted | meeting EM1 at lg M★ 8, ± 0.3 dex | their b | lg M200 at lg M★ 4 (EM1 5.78) | best max \|Z\| |
|---|---|---|---|---|---|
| 50 | 136 | 74 | 0.15–0.60 | 7.2–8.6 | 1.67 |
| 56 | 328 | 130 | 0.10–0.85 | 6.15–8.75 | 1.30 |
| 63 | 414 | 118 | 0.10–0.85 | 6.15–8.9 | 1.15 |
| 71 | 373 | 77 | 0.05–0.85 | 6.1–9.05 | 0.89 |
| 79 | 312 | 57 | 0.05–0.85 | 6.1–9.2 | 0.90 |
| 89 | 285 | 46 | 0.05–0.90 | 6.05–9.3 | 1.28 |

Taken together: a flat S of about 56–85 at low mass, with M200 at least about × 2 above EM1 at lg M★ 4 and joining EM1 near lg M★ 8, puts all five classes inside |Z| < 2 and sits in ET1's lowest band. The lowest lines pass near the Z line, not at E = 0; well-centred lines need more M200 at the faint end.

**This is a floor again, a fit with two or three numbers, chosen after the result. It has no mechanism.** Its value is about 0.5–0.8 of Σ_a0. Σ_a0 itself is also admitted on free lines at dwarf masses, so the dwarfs alone don't exclude or select it; ET1's band and F's −0.110 gas-rich offset count against it at SPARC's low end. It was not graded on SPARC, LITTLE THINGS, or the ceilings, and S below the rule at higher mass would still need its own crossing.

## Deviations
- First `sn1.py` run used V2's S9 at step 0.02 by my slip; fixed to the frozen 0.01 and rerun. V2 remained empty. `sn1.out` is the rerun.
- Criteria quote Σ_a0 107.3 / 129.7 by hand; the script computes 106.9 / 129.2. No verdict depends on it.
- The criteria's V2 region is scanned with S clipped to the grid (lg 0.5–3.5).
- `sn1_post.py`'s first scan hits its grid edges in a and b (a 11, b −0.2, 1.6); treat those ranges as bounded by the grid.

## Checks
K1 X49 |d| 0. K2 RG1 |d| 0. K3 bound |d| 4.6e-5. Interpolation in `sn1_post.py`, median |d| 3e-4. MUTATE S × 0.5: S_need 373.6 → 747.2, 116.5 → 233.0, 63.6 → 127.2, exact doubling. BITES.

## Limits
EM1's relation and any free line have no scatter. Equilibrium assumed; no tides or stripping, which matter most for satellites with M_need > M200. Spherical, one r₁₂. ET1's bands assume Υ 0.50. No zoom below 1e10, so nothing here measures S there. |Z| < 2 on class medians is a loose test with few-system classes (M31 others, N 5).
