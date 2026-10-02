# Open queue — the calc session ("Calculation review and next steps"), 2026-10-01 (night)

**Status: idle. Nothing is running and nothing has been fetched today.** Every on-disk lane of the owner's queue is done; what remains is gated on downloads, which need the owner's explicit yes **in this session's own chat** (a relayed yes from another session is not an approval; the peer said so too).

## UPDATE (after the owner's explicit "yes approve all the downloads" in this chat, 10-01 night): every item of the approved list is closed
| item | lane | hashes (criteria / stage A / SELFTEST / measurement) | outcome |
|---|---|---|---|
| lane J MIGHTEE-HI | **CFG279** | 99aec4107 + addendum 9e241f43c / – / d3d406288 / 7cecb04bc | no public per-galaxy sample exists (published fit values only); FLAT vs H(z) NOT POSSIBLE; the anchored a1 flips sign with the M/L choice |
| lane F PKS 0529-549 | **CFG275** | 4108d99e9 / c81be9e8c / bddebde63 / 093132b4c | 7 of 8 rows at the baryon floor; all near-Newtonian |
| lane G GN20 | **CFG276** | bc2ed906d / baa2abed3 / 58e95e1d4 / 231d32a8c | near-Newtonian; floor by 0.04 dex only (not informative) |
| lane I Lelli+23 | **CFG278** | 9a45bbdae + addendum 4d8e526d5 / b617f991b / 1f1aada8a / 9878bfcec | zC-400569 floor; zC-488879 first CONDITIONED roots (set by the SED mass) |
| BUDHIES width frame | CFG260 README addendum | 4809d47f0 | rest-frame widths (Gogate+ Eq. lw1) |
| BUDHIES local control | **CFG281** | b766cf43e / bb6956707 / 1eed4e943 / 4b0d76369 | local chain s* = 1.45 (+0.05 dex vs SPARC) but NOT CALIBRATED by the frozen precision rule; rho = 0.18; BUDHIES stays off the chart |
| lane H stellar masses | **CFG282** | 3af1cf10d (+ e111bcc30) / 0689c3250 / 763255cb6 / 0f0ef264e | SGP-2 and BRI1335 floors; SGP-1 root <= 22 (or a floor by 0.013 dex); no row can recover a0 |
| CFG267 audit addenda | CFG229, CFG271, CFG274 READMEs | cf497f5d1, fe73d2932 | the audit's statements, not verified by me |
Not on the approved list and NOT fetched: the HZ9 ALMA cube, the MIGHTEE-HI cubes, L_[CII] for HZ9 (CFG271's follow-up), the CFG268 shortlist (ADF22.1 = Rizzo+26 arXiv 2604.07440 and Umehata+25 arXiv 2410.22155; KDS / AMAZE tables; the Big Wheel) — each needs a new yes in this chat.

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

**2026-10-02 (addendum, append-only):** ALPAKA 24 (ADF22.5, z 3.094) route 1 (gas only, everything on disk, nothing fetched) is done as **CFG283** (criteria e46390c14, stage A + script ac39f69c3, SELFTEST e642ab2c4, measurement + MUTATE + README b20adfc0e): B1 (α_CO,min 0.8) ROOT s\* ≤ 27.6, VACUOUS under the frozen rule; B2 (Galactic 4.36) FLOOR; the dynamics allow α_CO ≲ 3.25 (3.0 under FLAT, 2.2 under a₀ ∝ H(z), post hoc), so the row measures the gas conversion, not a₀. **Route 2 (a literature stellar mass for ADF22.5) is FETCH-GATED and NOT done; the MIGHTEE-HI cubes likewise: both are put to the owner in the calc chat (a relay is not an approval).** CFG IDs 281, 282, 283 are used; 284–285 are free.
