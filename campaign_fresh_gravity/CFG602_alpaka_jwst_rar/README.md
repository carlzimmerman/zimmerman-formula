# CFG602: JWST-baryon RAR points for ALPAKA IDs 1, 3, 13. NOT INFORMATIVE FOR a₀ (reported D only); control K1 FAILED as frozen

κ = ½ is fitted. Footings 9.36e-11 / 1.13e-10 never pooled. Cold energy's mass required. Not a closed theory. Numbers from `cfg602_results.json` / `cfg602.out`. **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (5415b66db). **Script:** `cfg602_alpaka_jwst_rar.py` (seconds; `MUTATE=1` writes `*_MUTATE.*`). Data on disk only; nothing downloaded.

Question: the JWST-informed baryon decomposition of arXiv:2601.03338 (NIRCam stars + ALMA gas; the paper itself never mentions MOND or a RAR) gives three discs with everything a RAR needs. Do they say anything about a₀?

## Result (D = g_obs/g_bar at R_ext, spherical shortcut; B_max = all baryons inside R_ext, B_half = half)
| disc | z | y (B_max → B_half, canonical) | D (B_max → B_half) | log(D/ν) at B_max / B_half | label |
|---|---|---|---|---|---|
| ID1 | 0.561 | 2.1 → 1.1 | 1.19 → 2.38 | −0.04±0.08 / +0.18±0.07 | BRACKET-DEPENDENT (consistent at B_max, outside 2σ at B_half) |
| ID3 | 1.445 | 48 → 24 | 0.50 → 1.00 | −0.30±0.12 / −0.00±0.11 | BRACKET-DEPENDENT; ill-conditioned |
| ID13 | 2.103 | 9.0 → 4.5 | 0.68 → 1.37 | −0.19±0.19 / +0.08±0.18 | CONSISTENT both brackets; ill-conditioned (y ≫ 1) |

alt footing: y about 17% lower, same D, same labels.

- **Verdict: NOT INFORMATIVE FOR a₀.** No disc is CONDITIONED (y ≤ 1 at B_max) and stable across the two brackets. The only low-y disc, ID1, sits at z = 0.56 (outside the 2–5 band) and its label flips with the unknown enclosed baryon fraction. ID13 (the only one at z > 2) is at y = 4.5–9, where ν_mono is 1.1–1.5 and a₀ barely matters (CFG240).
- **The JWST baryons do not change the picture of CFG272/CFG268.** With the paper's gas included, ID13's D rises or falls with the bracket but is consistent with the law either way; it cannot discriminate a₀ values.
- **MUTATE passes:** with V_ext × 2 every disc turns TENSION on both footings, so the label has teeth.

## Control that FAILED (reported as frozen)
- **K1 FAIL:** ID13's stars-only D from this lane's spherical shortcut is 0.343, against CFG272's committed 0.442 (tolerance 0.02). CFG272 used a disc model (stellar disc 3.34 kpc), not a point-mass shell, so my shortcut over-counts the enclosed baryon acceleration. The B_max/B_half brackets are therefore a spherical envelope, not a disc model; a decomposition-grade g_bar needs the paper's profiles (not tabulated).
- K2 passes (D identical across footings).

## Not said
No sentence says the data favour any law. The enclosed baryon fraction is not tabulated, so g_bar is bracketed, not measured. A proper JWST RAR for these discs needs the paper's radial baryon profiles (figures only) or the authors' tables.
