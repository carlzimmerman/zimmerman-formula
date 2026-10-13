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
