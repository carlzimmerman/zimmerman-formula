# Deep-regime a0_eff audit (2026-09-25)

`D01_deep_a0eff_ml_audit.py` (run from the repository root; `MUTATE=1` must fail) audits the "SPARC-deep a0_eff = 0.72 a0" channel
(deepseek_push L06 → N05) that anchors O04b's "joint deep a0_eff = 0.7172 ± 0.0593, 4.77σ below the canonical a0".

**Finding (load-bearing checks D1–D5 pass):** the 0.724 is reproduced exactly from its inputs, and those inputs are the corpus v7
per-galaxy disc mass-to-light ratios (median 1.17, 84th percentile 2.97, up to 15 on gas-rich dwarfs, applied to bulges too) that
multiply SPARC's own 3.6 µm curves. With 3.6 µm population ratios (0.5–0.7) the same statistic on the same rings is 1.39–1.87, and
the α = 1 moment estimator is itself biased 17–26 per cent high for data obeying the in-force kernel. O04b is therefore not a
measurement of a0 against the canonical value; the downstream "a0* ≈ 6.0–6.8e-11" (N01, ZD07–ZD11) inherits it.

**Against interest (D6 FAILED as pre-stated, D7 diagnoses):** fitted with the in-force kernel, the deep band g_bar < 0.1 a0 gives
κ = 0.34–0.44 when every point is weighted equally and 0.43–0.56 with the standard quality cut or error weighting (Υ_disc 0.5–0.7).
The deep band measures κ only to about ±0.1 once point selection is varied — it neither confirms ½ nor supports a 4.77σ deficit.
