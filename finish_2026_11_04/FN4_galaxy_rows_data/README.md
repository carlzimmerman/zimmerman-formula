# FN4_galaxy_rows_data: no galaxy row moves. Brouwer+21's lenses are rebuilt (−1.7 %) and the lensing gap stands; the Local Group field moves nothing; IC 1613's cube is NOT EVALUABLE by its frozen checks, but read post-result the law fails it at every inclination; the Milky Way's thick share is NOT MEASURABLE without APOGEE's selection function

Item 4 of the finish push. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. `READINESS.md` lists, per row, what was tried, which inputs could move it, and what is on disk or downloadable. The owner approved the FN4a and FN4f downloads on 2026-11-04.

| Lane | Row | Label | Commits | Failed checks | Needs |
|---|---|---|---|---|---|
| FN4c Brouwer+21 lens rebuild | KiDS lensing | **REBUILD MATCHES** (255,052 against 259,383, −1.7 %; −0.1 % post-result); **GAP STANDS** on both footings (A1 +0.085 / +0.046 dex; LE1 +0.089 / +0.050) | d62a6b6b53 criteria; 7f4f3e98ce; ae9bd592c8 | stage-2 MUTATE (masses ×2) did not bite; first run peaked at 25 GB RSS (fixed, rerun identical) | optional: MAG_GAAP_r for all rows (ESO TAP, about 30 MB) |
| FN4b Local Group external field | dwarfs, IC 1613 | **FIELD MOVES NOTHING**, both footings; T1 **NO TREND** in every class (all ρ > 0, the opposite of an EFE) | 814c665549 criteria; 79658c0ec8 | none | nothing |
| FN4a IC 1613 cube (council CW7) | IC 1613 | **NOT EVALUABLE** (S0a, S0b and M_free's χ²_red line fail). Post-result: the law fails the cube at every i 15–60°, with or without non-circular terms (best Δχ² +993 / +5,606 against 83.7); the cube prefers i 53.5° | a616530a1a criteria; 131401cc29 fetch, amendments; db14eb9fac | S0a, S0b; M_free χ²_red 4.05; `ic1613_ubvcalib.txt` not obtainable; RSS up to 1.8 GB in the mocks | nothing new |
| FN4f Milky Way thick share (APOGEE) | Milky Way | **NOT MEASURABLE**: without the selection function the share follows the assumed thin scale height (0.16–0.62; 0.253 at h_lo 0.30, post-result) | b12986c195 criteria; 781ce6a8b3 fetch; 67dfb75501 amendments; bbe016eff5 | KA3 (trough finder), KA4 (1″ position test; IDs match 100 %), band width 0.92 | the selection function, or a thin-disc scale height to about ±0.02 kpc |
| FN4d Local Group discs by star counts (council CY4) | Milky Way (generic discs) | criteria frozen, not run | 694b0087f5 | | the owner's yes for resolved-star maps and HI curves |
| FN4e HI-selected lenses (council CY6) | KiDS lensing | criteria frozen; stage 0 runs on disk, not yet run | c03a803b3b | | nothing for stage 0 |

**What changed on the record today:**
- NV2's and LAM1's failed rebuilds trace to comoving distances and a masked neighbour pool.
- The ledger's unbuilt Local Group field estimator is built, and moves nothing.
- IC 1613's inclination lever does not rescue the law in its cube. The label stays NOT EVALUABLE because the frozen stage-0 and χ² lines were not met.
- The Milky Way's thick share cannot be placed without APOGEE's selection function.

κ = ½ FITTED. Not theory closed.
