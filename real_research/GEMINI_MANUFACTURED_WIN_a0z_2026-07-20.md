# Gemini's "manufactured win" on a₀(z) — logged, diagnosed, corrected (2026-07-20)

**What happened.** In a chat handed to Carl, Gemini derived the framework's a₀(z)
evolution under DESI/CPL dark energy and concluded that the framework *"geometrically
demands a positive a₁ slope … requiring the high-redshift acceleration scale to climb
exactly as the MUSE-DARK III data observed."* Presented as a confirmation ("the
observational mic-drop"). **It is not a confirmation — it is a manufactured win.** The
correct calculation on the framework's *own* canonical footing gives a small **bump then
a DECLINE**, so the MUSE/MSA-3D rise is a **tension against** the framework, not a match.
Logged here because Carl's #1 rule penalizes manufacturing a win as hard as caving.

## What Gemini got RIGHT (so this stays fair, not a reflexive dismissal)
1. CPL density: ρ_DE(z) = ρ_DE(0)·(1+z)^{3(1+w0+wa)}·exp(−3 wa z/(1+z)). ✅
2. Used the **correct footing**: a₀ ∝ √ρ_DE (dark-energy-only), not √ρ_total. ✅
3. Closed form a₀(z)/a₀(0) = (1+z)^{(3/2)(1+w0+wa)}·exp(−(3/2) wa z/(1+z)). ✅
4. First-order Taylor a₀(z) ≈ a₀(0)[1 + (3/2)(1+w0) z]; wa cancels at O(z). ✅ (algebra only)

## The ERROR (where the win is manufactured)
Gemini extrapolated the **linear** term to z~1 and dropped wa. But the O(z²) term it threw
away is wa-driven and, for DESI values (w0≈−0.8, wa≈−0.75), **negative and ~4× the linear
term's reach**:

    a₀(z)/a₀(0) = 1 + (3/2)(1+w0) z + (3/4)[ wa − (1+w0) + (3/2)(1+w0)² ] z² + O(z³)
    DESI-DR2 (w0=−0.83, wa=−0.75):  ≈ 1 + 0.26 z − 0.66 z²
    => the rise REVERSES near z ≈ 0.29 (a ~+3% bump), then DECLINES.

So the linear slope is only meaningful for z ≪ 0.3, and MUSE/MSA-3D live at z = 0.5–1.7 —
exactly where the dropped wa term dominates. Extrapolating linearly to z=1 gives +30% when
the **exact** canonical curve gives ≈ −1%.

| z | EXACT canonical √ρ_DE (DR2) | Gemini linear (dropped wa) | error |
|---|---|---|---|
| 0.5 | 1.04 (+4%) | 1.15 | +10% |
| 1.0 | **0.99 (−1%)** | 1.30 | +31% |
| 1.5 | **0.92 (−8%)** | 1.45 | +57% |
| 3.0 | **0.70** | 1.90 | — |

A strong monotonic RISE only appears under the **rival** footing a₀ ∝ √ρ_total ∼ H(z),
which the canonical dark-energy-only footing **rejects**. Gemini picked the right footing
in step 2, then broke it in the low-z linearization to force the MUSE match.

## The CORRECT law (canonical modified-inertia, use this everywhere)
    a₀(z)/a₀(0) = (1+z)^{(3/2)(1+w0+wa)} · exp[ −(3/2) wa z/(1+z) ]
  * ΛCDM (w0=−1, wa=0): flat (a₀ = const).
  * DESI-DR2 (−0.83, −0.75): bump +3% at z≈0.29 → decline → 0.70 at z=3.
  * DESI-DR1 (−0.45, −1.79): bump +15% at z≈0.44 → decline → 0.57 at z=3.
  * Everything dissolves to constant-a₀ if w→−1.

## Honest standing vs the data
The framework's canonical branch is **bump-then-decline**; MUSE-DARK III (reported rise,
~doubling by z~1) and the independent NIRSpec MSA-3D inversion (this repo,
`msa3d_a0z_confrontation.py` / `_robustness.py`: rising inferred a₀, slope +1.7…+2.1)
both **lean AGAINST** it. That is a **TENSION**, not a kill (absolute a₀ is M/L-degenerate;
the MSA-3D slope exceeds even √ρ_total → z-correlated systematics; dissolves if w→−1). The
decisive clean test remains the z≳3 BTFR-offset sign — **not** a₀(z).

## Artifacts (committed, runnable)
- `real_research/a0_value_and_cpl_evolution_check.py` — 9.36-vs-9.42 input check + exact-vs-linear.
- `real_research/a0z_evolution_correct.py` — the correct law + the figure.
- `real_research/figures/a0z_evolution_gemini_vs_correct.jpg` — the visual.
- Also settled: **a₀=9.42 was just Planck-with-BAO inputs** (H0=67.66, Ω_Λ=0.6889) vs Carl's
  canonical (67.4, 0.6847) → a₀=9.36; ~0.6% input choice, same formula, value is quarantined.
