# LR6 — STALE-REGISTER DISPOSITION AUDIT (Z8-wave, 2026-09-28)

Fresh verification: `lake env lean M01_alg_spine.lean` from
fable_independent_2026/lean_2026 — rc 0, zero sorry, all axiom prints ⊆
{propext, Classical.choice, Quot.sound} (full stdout: LR6_lean_stdout.txt).
Theorem-presence gate: j10i_window_decomp + the k04_* family ALL PRESENT.

Disposition of the register rows still carrying Lean status "open (M01)":

| register row | disposition | evidence |
|---|---|---|
| row 17 — J10-I = (r_B/R)·window, [4/3,2]·(r_B/R) bounds | Lean leg **CERTIFIED via M01 §4** (`j10i_window_decomp`), recompile-verified this tick | M01_alg_spine.lean + LR6_lean_stdout.txt |
| row 19 — K04 inversion bijection + third observable | Lean leg **CERTIFIED via M01 §5** (full bijection incl. the CORRECTED boundary `k04_qhat_gt_neg_one` (q̂ > −1 ⟺ 8·E[D] > −3 ln A, τ̂₀>0) and the honest refutation `k04_refutes_ed_three_halves` — the "E[D]<3/2 ⟺ q̂>−1" suggestion is FALSE, witness certified), recompile-verified this tick | M01_alg_spine.lean §5 + LR6_lean_stdout.txt |
| row 12 — atom law A = exp(−τ₀(1+q/3)) | **LABEL-ONLY / model-input** (K01 A-class): restates the engine's own sampling rule; a Lean certificate would be a definition restatement, not a discovery. NOT lane-worthy. Empirical legs (J09 MC 0.36826 vs exp(−1); K03 81/81) stand | K01_TAUTOLOGY_AUDIT.md standard |
| row 18 — J11 volume window (finite τ₀: 1.897/1.710/1.314) | stays **MEASURED** (quadrature+MC; no closed form known at finite τ₀). Its τ₀→0 numerator (chord 3/4 + q·5/12) is UNCONDITIONALLY certified by Z8 LR4c and engine-tested by Z8 MC5 | LR4c_results.json, MC5_results.json |

With rows 10/11 (LR1/LR2), 15 (LR5), 17/19 (M01 §4/§5), 12 (label-only), 18
(measured + certified thin-window leg): **no "open (M01)" Lean-leg door remains
in the register.**
