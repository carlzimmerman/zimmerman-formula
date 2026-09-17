# navier_stokes_attempt — the a0-line vs Navier–Stokes Existence and Smoothness

Deepseek-track campaign folder (2026-09-17). The Clay NSE problem attacked
from the framework's measured law — the two-face response law
g_obs² = g_N² + a₀·g_N with a₀ = 9.3619e-11 m/s² (κ = ½, MEASURED), the
data-selected kernels, the measured window η ∈ [0.028, 0.203] and the floor
3.5. Record of the attack: pre-registered doors, kills, conditional theorem,
Lean-certified algebra, Galerkin evidence, honest Clay-scope verdict.

## The record at a glance

| File | Content | Status |
|---|---|---|
| N00_CAMPAIGN.md | the pre-registered doors (N1–N5), kill conditions, falsifier recipes, Clay-scope clause | the campaign constitution |
| N01_rheology.py/.out/_results.json | the a0-line read as a p-curl rheology: p_eff = 3/2 at deep, 2 at the Newtonian face; gates 9/5 and 11/5 unreachable in the O(1)-regime | 6/6 — DOOR N1 DEAD (the found result) |
| N02_dragcount.py/.out/_results.json | the certified a₀/2 cap; the sup-ODE count (linear-in-T, no global bound); lab-face numbers 11 orders below measurement | 6/6 — DOOR N2 DEAD |
| N03_supbarrier.py/.out/_results.json | the FORWARD theorem: ZNS[κ,ℓ₀] globally smooth at every fixed κ > 0 (sup barrier + Prodi–Serrin + continuation); survival gate pins κ ≤ 2.6e-8 (10 kpc); the allowed band is tight, not empty | 6/6 — theorem standing, coupling measurement-awaited |
| N04_galerkin.py/.out/_results.json/.png/.npz | Galerkin evidence: sup 4.22 → 4.06 → 3.15 → 1.63 down the drag ladder; barrier never violated; window-class flow diagnostic | 3/3 + diagnostics (equilibrium = N04b) |
| N04b_equilibrium.py/.out/_results.json/.png | N = 32 run to equilibrium: cd_03 equilibrates (0.0% drift); classical spin-up needs T ≳ 120–160 (honest FAILs); trajectory inequality 0 violations on 26M pairs; energy identity to 0.26% | 5/7 (2 registered as the next lane) |
| N05_window_theorem.py/.out/_results.json + N05_WINDOW_THEOREM.md | the WINDOW THEOREM: sup\|Du/Dt\| ≤ 3.5·a₀ ⇒ global smoothness (trajectory bound + Serrin); singularity formation requires window-exit | 17/17 — theorem standing |
| N06_drag_fingerprint.py/.out/_results.json | the PREDICTION: refined survival κ ≤ 2.6e-9; the eBTFR ladder sags 0.6–5% by z ≤ 1 with a high-mass-first tilt if the completion exists | 4/4 — the Kepler-grade falsifier (conditional) |
| lean/NSE_a0line.lean | the two faces certified: a₀/2 cap, deep sandwich, Newtonian face, window suppression | compiled exit 0 — 11 theorems, axioms clean |
| lean/NSE_vector_core.lean | the sup-argument algebra: u·((u·∇)u)-swap, (ω×u) ⊥ u | compiled exit 0 — 3 theorems, axioms clean |
| lean/NSE_barrier.lean | the invariant-set rungs: barrier pull-down, crossing, stretch-vs-drag count (+ the honest c=0 disproof) | compiled exit 0 — 4 theorems, axioms clean |
| N07_ACTION_DOOR.md + N07_action_door.py/.out/_results.json + N07_ACTION_DOOR_DERIVATION.md | **the missing door — the phantom as the action's fluid sector**: cusp D1 (1/r² exact), caustic channel D2 (τ_ff = 3.3e7 yr at 1 kpc), transfer D3 KILLED by the a₀/2 cap (toy: 45 km/s capped vs 207·c free), G03 residual named | 15/15 — the door closes by measurement |
| N08_openai_analysis.md + N08_openai.md | the OpenAI blowup record: theorem (C)/(D), construction anatomy, Lean inventory (2,659 files, same rc2 toolchain), controversy state; N5 floor-exit WITNESSED at τ ≈ 5e-7 | digest + verdict card |
| N09_* | the deep-sector clock table (τ_ff at 1–10 kpc) — folded into N07 D2 | via N07 |
| SPEC_A/B/C_*.md | the parallel-attack specs (Lean, window theorem, equilibrium numerics) | filed |

## The answer the framework gives (see N05_VERDICT.md)

1. The measured law, read as a fluid rheology, is shear-thinning exactly where
   it acts (p_eff → 3/2 at deep): the power-law regularity class is unreachable.
2. The law's only dimension-forced modification (the a₀/2-capped drag) is
   sub-regularizing: it cannot close the enstrophy gap (certified counts).
3. The minimal completion ZNS[κ, ℓ₀] carries a provable global-smoothness
   theorem at every fixed κ > 0 — and rotation support pins κ ≤ 2.6e-8, a band
   tight enough that window-class flows feel it on ≈ 3 Hubble times.
4. The WINDOW THEOREM: any classical flow whose material acceleration stays
   inside the measured floor (≤ 3.5·a₀) is globally smooth; a Clay singularity,
   if it exists, must exit the window — the singular regime is the law's
   Newtonian face.
5. CLAY SCOPE (boundary, not a claim): the κ → 0 / a₀ → 0 passage is the
   singular limit where the barrier constant diverges; the controlled passage
   through it is the Clay gap, named open. This campaign does not claim the
   Millennium problem; it claims the framework's verdict on it: the measured
   constants close the natural doors, certify a regularity domain below the
   floor, and place the Clay core on the Newtonian face of the law.

How to rerun: `python3 N0X_*.py | tee N0X_*.out` in this folder
(python3 from miniconda base: numpy/scipy/sympy/matplotlib present).
Lean: compile with `lake env lean` from fable_independent_2026/lean_2026.