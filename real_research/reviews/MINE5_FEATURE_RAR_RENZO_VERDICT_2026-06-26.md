# MINE-5 Feature-level RAR / Renzo's rule — verdict (2026-06-26)

Script: `reviews/mine5_feature_rar_renzo.py` (numpy + real SPARC rotmod, 175 gal / 3389 pts).
ASSUME a0 = c² √(Λ/32π) = 9.36e-11 + dS-Unruh MODIFIED INERTIA.

NOVEL re-analysis the global-RAR-scatter test throws away: the WITHIN-galaxy radial
DERIVATIVE structure (bumps & wiggles, Renzo's rule), not the (g_bar,g_obs) cloud.

## LEVER A — within-galaxy LOCAL log-slope s = dln g_obs/dln g_bar  (PROVABLE NOW, positive)
Finite-difference local slope between adjacent radii, vs predicted s(g_bar)
(deep-MOND→0.5, Newtonian→1.0). Weighted regression s_obs = A + B·s_pred(g_bar):
- **B = 0.555 ± 0.055 → running slope locked to g_bar at ~10σ** (dSU/framework form).
- Δχ²(running vs flat constant slope) = **102** over 1247 adjacent pairs.
- Spearman(g_bar, s_obs) ρ=0.257, **p = 2.9e-20**.
- Binned ⟨s_obs⟩ rises monotonically 0.44→0.93 across g_bar/a0 ∈ [0.01, 60], matching
  the predicted 0.5→1.0 transition.

This is a FEATURE-level statistic (radial gradients), independent of and stronger than
the degenerate global-scatter a0 test.

BOTH-WAYS / what it is NOT:
- **a0- and interpolation-DEGENERATE vs MOND.** χ²: dSU 1399 ≈ McGaugh 1389 ≈ simple
  1391 (B = 0.56 / 0.76 / 0.74) — all three fit the running equally. Does NOT select
  the framework's dS-Unruh form over standard MOND. NON-diagnostic vs-MOND.
- B ≈ 0.55–0.76, NOT 1.0: the running is real at 10σ but at ~half predicted amplitude
  (finite-difference + per-point noise dilute the slope). A detection of the SHAPE, not
  a clean amplitude confirmation.
- "vs-ΛCDM" is real but SOFT: it's MOND-family-vs-naive-free-halo. Modern ΛCDM-on-SPARC
  emulators reproduce the RAR including its local slope → not a referee-proof ΛCDM kill,
  it's the known MOND-family RAR win re-expressed at feature level (do not re-bank a known
  degeneracy as new). Honest label: **distinct-vs-LCDM-only, MOND-shared.**

## LEVER B — feature-RESPONSE amplitude β (the ONLY MG-impossible lever) → BELOW NOISE
MG (QUMOND/AQUAL, strictly local in r): β=1. MI (dS-Unruh, inertia is an orbit functional):
β<1 (a localized g_bar feature is partially smeared over the orbit).
- The detrend-correlation estimator returned β=1.62±0.001 (626σ) — this is a CONVOLUTION-
  EDGE ARTIFACT of the 3-pt moving-average `mode='same'`, NOT physics. DISCARDED.
- Honest noise scoping: circular-orbit MI smearing is 2nd-order, ceiling ~0.5·(Δr/r) ≈ 5%
  of feature amplitude. SPARC per-feature S/N ≈ 2.7 (median 4.3% V error, Δr/r≈0.10).
  Resolving a ~1–5% amplitude suppression needs per-feature S/N ~20 → **below SPARC noise.**
- **VERDICT B: MG-vs-MI feature-smearing is a0/MG-DEGENERATE in hand.** Consistent with the
  banked backdrop: the σ-spread SIGN remains the only MG-impossible lever, and it needs
  future cluster-member/dwarf spectroscopy, not SPARC.

## NET
Most-creative in-hand positive = **Lever A**: a ~10σ, feature-level (Renzo's-rule)
confirmation that the SPARC local log-slope runs 0.5→1.0 locked to g_bar — distinct
vs naive-ΛCDM, but a0-/interpolation-degenerate vs MOND and ΛCDM-emulator-absorbable.
The genuinely MG-impossible lever (Lever B) stays below SPARC noise. NO manufactured win.
