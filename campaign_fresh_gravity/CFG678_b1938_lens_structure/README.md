> **ID NOTE: this lane is CFG710** (block CFG710–719, owner-assigned 2026-10-12). Its directory says CFG678, which another session
> also used the same day ("one-action contract"). Cite it as CFG710.

# CFG710: SEALED blind predictions for B1938+666's own mass structure (before the stage-2 lens fit was read)

Criteria ef9d750d0 (committed alone while CFG674 stage 2 ran; public timestamp on branch `sealed-2026-10-12-claude`).
`cfg710_dump_light.py` (stage-1 LIGHT only) → `cfg710_predict.py` → `cfg710_predictions.json`,
**sha256 ef0a780b56fa57c651908c16070f49b1832f794b5a08071fb00e73f99a664559**. MUTATE (a0 → 0) bites: γ 2.30 → 3.26.
κ = ½ FITTED; cold energy mass required; no particle species; not "theory closed".

**Disclosed before stage 2:** stage 1's second Sérsic (R_e = 30″, tiny intensity) is a sky/arc pedestal over the 1.2″ mask, not
stars; primary prediction V1 uses the compact Sérsic (R_e 0.227″, n 5, q 0.79, PA 130.4°). V2 (both) needs M* = 5e12 M☉ —
unphysical, reported only. A bug in the projected-mass integral (shell fraction) was found and fixed before sealing.

| prediction | canonical | alt |
|---|---|---|
| **P1 total density slope γ_eff at θE** (2 = isothermal) | **2.30** | **2.23** |
| 3-D mass-weighted slope 0.5–1.5 θE | 2.54 | 2.45 |
| stellar mass to reach θE = 0.443″ (M_E = 9.3e10 M☉) | 1.10e11 M☉ | 1.06e11 M☉ |
| g_N/a0 at θE; cold-energy fraction inside θE | 8.2; 18 % | 6.5; 21 % |
| **P2** mass PA = 130.4° ± 10°; q_M ∈ [0.79, 0.89] | same | same |
| **P3** m = 3, 4 multipole strengths ≤ 0.02 | same | same |

Pure stars would give γ = 3.26: in the framework the law, with no halo parameter, turns the steep stellar profile into a
near-isothermal total one at θE. Scoring (frozen): P1 CONSISTENT if |γ_meas − γ_pred| ≤ max(2σ, 0.10), TENSION ≤ 0.25,
INCONSISTENT beyond, NOT DIAGNOSTIC on a prior edge; P2/P3 by the tolerances above.

## PREVIEW (2026-10-13; no verdict weight — best-fit Nelder–Mead on the identical stage-2 model, no posterior)
`cfg710_preview_stage2nm.txt`, scored by the frozen `cfg710_score.py` → `cfg710_score_preview_NelderMead.json`:
slope **2.234** vs sealed 2.30 / 2.23 → CONSISTENT (Δ 0.061 / 0.008); mass PA 132.1° vs light 130.4° (Δ 1.7°) → aligned;
**q_M 0.924 vs frozen window [0.794, 0.894] → OUTSIDE (rounder by 0.03): P2 INCONSISTENT as previewed**; m3 0.002, m4 0.006 →
CONSISTENT. Caveats: single optimiser run, no σ; θE moved 0.443″ → 0.474″ (prediction normalised at 0.443″). The verdict waits for
the stage-2 posterior.

## RESULT (2026-10-13): scored on the maximum-likelihood fit; stage-2 posterior NOT RUN (frozen 12-h rule)
The Nautilus stage-2 search reached only 2,000 likelihood evaluations in 11 h 12 min (≈ 20 s each in the search; checkpoint
`checkpoint.hdf5`, n_like = 2000) and was stopped under the frozen 12-h rule: **posterior NOT RUN**. With no posterior σ, the
frozen tolerances apply unwidened (P1: 0.10; P2: the exact windows). Scored by `cfg710_score.py` on the Nelder–Mead
maximum-likelihood fit of the identical model (`cfg710_score_preview_NelderMead.json`):

| prediction (sealed before the fit) | measured | verdict |
|---|---|---|
| **P1 slope** 2.30 can / 2.23 alt | **2.234** | **CONSISTENT** (Δ 0.061 / 0.008) |
| **P2 alignment** PA 130.4° ± 10°; q_M ∈ [0.794, 0.894] | PA 132.1° (Δ 1.7°); **q_M 0.924** | **INCONSISTENT** (PA passes; axis ratio rounder than the window by 0.03) |
| **P3 multipoles** ≤ 0.02 | m3 0.002, m4 0.006 | **CONSISTENT** |

**Label: P1 CONSISTENT, P2 INCONSISTENT (axis ratio), P3 CONSISTENT; both footings; ML-only (posterior not run).**
Reading: from starlight plus the law, with no halo parameter, the predicted total slope matches the measured one (2.23–2.30 vs
2.234; pure stars 3.26); mass and light are aligned and multipole-free. The mass is rounder than the frozen window allowed — the
sign the framework expects (the cold-energy component is rounder than the stars), the size larger than predicted; not rescued.
Limits: one lens; ML point only; θE 0.443″ (prediction) vs 0.474″ (fit); ν_mono tail and spherical deprojection.
