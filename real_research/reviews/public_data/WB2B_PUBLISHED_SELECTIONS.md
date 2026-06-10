# WB-2b — D1/D2 on published-grade selections + prediction-8 amendment

*C. Zimmerman, 2026-06-09. Per Fable: the WB-2 halt adjudicated my **loose hybrid**, not the dispute. Re-ran the two diagnostics under reconstructions of Chae's and Banik's cuts (`wb_published_selections.py`). The published samples were built to suppress what D1/D2 measured — so this asks: do they get below the thresholds?*

## The six-number table (same catalog, same scripts)
| selection | N | N_deep | D1 deep σ/v_N | D2 deep super-escape |
|---|---|---|---|---|
| my hybrid (ref) | 73,670 | 3,297 | 0.306 | 0.267 |
| **Chae-grade recon** | 13,547 | 1,671 | **0.211** | **0.196** |
| **Banik-grade recon** | 12,849 | 1,561 | **0.196** | **0.179** |

**Reading:** quality cuts reduce the floors (σ/v_N 0.31→0.20; super-escape 0.27→0.18) but **do NOT clean them** — both selections retain a **~0.2 deep-bin noise ratio (same order as the +2–11% MOND velocity signal)** and a **~18–20% super-escape fraction (still above the 15% line)**. This is Fable's "Chae-grade keeps a double-digit super-escape floor → a seed of why a 5σ can be extracted from a not-fully-clean sample."

## Caveat (fidelity — flagged, not buried)
These are **reconstructions targeting the published pair counts, NOT exact cut replications.** My Banik-grade came back **12,849, not his clean ~8,600** — so it is *not* Banik's actual sample; his RV/triple screen is more aggressive than my `|ΔRV|<4 km/s & both-RV-finite & p/σ>50`. **The definitive answer for the published samples needs the exact cuts transcribed from Chae 2023 (ApJ) and Banik+2024 — the clean next step.** What is robust here is the *trend* (quality cuts lower the floors but plateau at ~0.2, the signal's order), which is cut-detail-insensitive.

## Prediction-8 amendment (records first because it cuts against us)
The prediction table lists DR3 wide binaries as **KILL-class, "decisive now,"** with a +2–11% expected velocity boost. Tonight's diagnostics say the **deep-bin noise floor on accessible Gaia DR3 selections (~0.2 in σ/v_N) is the same order as that signal**, and the model-free super-escape floor stays ~18–20% even at published-quality cuts (in reconstruction). **Honest amendment: DR3 wide binaries may be SYSTEMATICS-LIMITED at the signal amplitude** — which would partly explain how two careful teams extract opposite 5σ-class verdicts from one catalog. **Shift the entry from "decisive now" to "decisive at DR4 astrometry (2026), with D1/D2 (noise floor + super-escape) as the gate any future claim must pass."** Subject to confirmation with the exact published cuts.

## Status
WB-3 (the MC pre-registration) is HELD per Fable — the substrate (which selection the MC adjudicates) is undecided until the exact-cut diagnostics land. Next clean step: transcribe Chae's and Banik's exact cuts (WebFetch the papers) and re-run, OR accept the cut-insensitive trend + amendment. No mock orbit drawn yet.
