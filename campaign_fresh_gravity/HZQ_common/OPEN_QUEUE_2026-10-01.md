# Open queue — the calc session ("Calculation review and next steps"), 2026-10-01 (night)

**Status: idle. Nothing is running and nothing has been fetched today.** Every on-disk lane of the owner's queue is done; what remains is gated on downloads, which need the owner's explicit yes **in this session's own chat** (a relayed yes from another session is not an approval; the peer said so too).

## Done today (each re-run from a git archive by the orchestrator and recorded in STANDING)
CFG258 (MIGHTEE pre-flight, mocks only), CFG259 (UFD variants), CFG260 (BUDHIES; width frame unresolved), CFG261 (KiDS absolute levels), CFG262 (MUSE-DARK by route), **CFG270 (lane A, KMOS3D 192 fits)**, **CFG271 (lane B, HZ9)**, CFG272 (lane C, ALPAKA five), CFG273 (lane D, Danhaive gold 41; README addendum 42b45bfc0), CFG274 (lane E, Amvrosiadis eight), **CFG277 (lane H, Roman-Oliveira four discs)**, **CFG280 (lane K, published SINS AO)**. Each directory has a README.md first; the points files are in the `chart_a0z_points.csv` shape. All results are class D/S or upper bounds: **no law statement anywhere**.

## Open — all waiting for the owner's explicit yes in this chat (state source, expected size and a hard cap before any fetch; log URL, bytes and sha256 in the `data_assembly` manifests)
| id | item | what it needs | note |
|---|---|---|---|
| lane F (CFG275) | PKS 0529-549 | Lin+ arXiv:2411.08958 (the [CI](2-1) rotation curve) | the gas masses of arXiv:2411.04290 Table 5 are already on disk (`multitracer_gas`) |
| lane G (CFG276) | GN20 | the Hodge+2012 table and arXiv:2510.17804 (NOEMA + radiative-transfer gas) | the Übler+24 DysmalPy tables (arXiv:2403.03192) are partly on disk |
| lane I (CFG278) | Lelli+23, zC-400569 and zC-488879 | the rotation-curve data or figure (the on-disk table has only the mean V_rot; the masses are the authors' fits, class D) | |
| lane J (CFG279) | MIGHTEE-HI / LADUMA real data, z 0.02–0.09 | the public RAR sample of arXiv:2608.03576 (and the paper) | use CFG258's frozen estimators and controls |
| BUDHIES (CFG260 follow-up) | the width frame (observed vs rest) | Gogate+2020 text, arXiv:2302.12197 | CFG260's chain gives s\* 0.10 (observed-frame) / 0.26 (rest) and is not a calibrated point |
| **BUDHIES local control (NEW; the owner's choice 10-01, not on the earlier seven-item list)** | calibrate the width → V → baryon chain on a same-pipeline local HI sample | ALFALFA HI widths + SDSS colours (a catalogue cross-match; source, expected size and a hard cap to be stated before any fetch) | **BUDHIES stays OFF the chart, not even as an open marker, until the chain is calibrated**; the chart README records "computed, chain not calibrated" with CFG260's hash d7eeb195b |
| lane H follow-up | stellar masses of BRI1335-0417 and SGP38326-1/-2 | the literature look-up named in CFG197 | adding stars cannot lift CFG277's floors and can only lower the SGP bounds |
| (optional) HZ9 | a cube-based fit | the ALMA [CII] cube, several GB | not needed: the corpus-ring lane (CFG271) is done; only if the owner prefers a cube fit |

ID block: this session holds CFG210–229, 260–262 and 270–285 (275, 276, 278, 279 reserved for the fetch-gated lanes above; 281–285 free).

**2026-10-01 night (addendum):** the High-z peer re-relayed the owner's "keep going" for lanes A, B, H and K after they were finished; all four are done and pushed (CFG270 b2e86a913, CFG271 a18b17d72, CFG277 0f6c4cd58, CFG280 396299a9f; the chart should use CFG280's overlap-free row PT2_new). Nothing new was started; the only addition to the open list is the BUDHIES local control above.
