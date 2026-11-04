# FN4_galaxy_rows_data: Brouwer+21's lenses rebuilt (−1.7 %) and the lensing gap stands on them; the Local Group field moves nothing; IC 1613 and the discs wait on downloads; the Milky Way waits on new observations

Item 4 of the finish push. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Start with `READINESS.md`: per row, what was tried, which inputs could move it, and what is on disk or must be downloaded.

| Lane | Row | Label | Commits | Failed checks | Needs |
|---|---|---|---|---|---|
| FN4c Brouwer+21 lens rebuild | KiDS lensing | **REBUILD MATCHES** (255,052 against 259,383, −1.7 %; −0.1 % post-result); **GAP STANDS** on both footings (A1 +0.085 / +0.046 dex; LE1 +0.089 / +0.050) | d62a6b6b53 criteria; 7f4f3e98ce; ae9bd592c8 | stage-2 MUTATE (masses ×2) did not bite; first run peaked at 25 GB RSS (fixed, rerun identical) | optional: MAG_GAAP_r for all rows (ESO TAP, about 30 MB) |
| FN4b Local Group external field | dwarfs, IC 1613 | **FIELD MOVES NOTHING**, both footings; T1 **NO TREND** in every class (all ρ > 0, the opposite of an EFE) | 814c665549 criteria; 79658c0ec8 | none | nothing |
| FN4a IC 1613 cube model (council CW7) | IC 1613 | criteria frozen, not run | a616530a1a | | the owner's yes for the LITTLE THINGS cube and moment maps (host unreachable today; size not obtained) and the V/B images (20.2 MB) |
| FN4d Local Group discs by star counts (council CY4) | Milky Way (generic discs) | criteria frozen, not run | 694b0087f5 | | the owner's yes for resolved-star maps and HI curves (VizieR sizes not obtained today) |
| FN4e HI-selected lenses (council CY6) | KiDS lensing | criteria frozen; stage 0 runs on disk, not yet run | c03a803b3b | | nothing for stage 0 |

**Milky Way vertical force:** no lane. The deciding input is K_z(R₀) measured without a Newtonian potential family, which is a new-observation item (UX5). A measured thick-disc share from APOGEE DR17 (3.97 GB + 0.65 GB) would only bear on the alt footing inside a filter family that CZ5 already rules out on Cassini.

**What changed on the record today:** NV2's and LAM1's failed rebuilds trace to comoving distances (+62.8 %) and a masked neighbour pool (+14.2 %); the authors' code uses D_A and keeps masked rows as neighbours. The ledger's "Local Group external field from a new estimator: not built" is now built, and it moves nothing.

κ = ½ FITTED. Not theory closed.
