# CFG565: ΛCDM-with-feedback's RAR acceleration scale RISES with redshift (×4.9 at z = 2.5); the framework's a₀ tracking ρ_DE FALLS (~0.8). Opposite signs, ~0.8 dex apart

Criteria 6b46ce8a7 (committed before the script). Script `cfg565_gdagger_z.py` (~2 min, niced). It reuses CFG476/477's data, statistic and DC14 code. κ = ½ fitted.

| z | feedback-ΛCDM g†(z)/g†(0), median (16–84%) | framework: a₀ tracking ρ_DE (record) | flat a₀ | a₀ ∝ H(z) |
|---|---|---|---|---|
| 1.0 | 1.20 (1.02–1.90) | ~1.0 | 1.0 | 1.77 |
| 2.0 | 2.82 (1.52–8.20) | ~0.87 | 1.0 | 3.0 |
| 2.5 | **4.88 (2.01–9.70)** | **~0.80** | 1.0 | 3.7 |

**Verdict: FEEDBACK RISES** (the 16th percentile at z = 2.5 is 2.01, above 1.3).

**Reading.**
- With the standard redshift dependence of the stellar-to-halo relation and of concentrations, plus DC14 cores, the emergent RAR scale in ΛCDM rises steeply with z. That agrees in sign with the record's Magneticum note (×2.3–3 by z ≈ 2) and with a₀ ∝ H(z) in size.
- The framework predicts the **opposite sign**: a₀ ≈ 0.8 of local at z = 2.5 if it tracks DESI-like dark energy.
- The gap at z = 2.5 is a factor of ~6 (≈ 0.8 dex), about three times the record's 0.25-dex mass-calibration floor (CFG54). So **a₀(z ≈ 2–2.5) separates "feedback arranges the cold mass" from "a₀ is tied to Λ" by sign and by a margin that survives the calibration wall.** The data needed are still resolved inner kinematics plus gas maps (CFG385/475).
- **What drives the rise:** the MUTATE run (halos frozen at z = 0, size evolution kept) gives 0.57. Denser high-z halos drive it up; smaller galaxies alone would push it down.

**Controls.**
- **K1 FAILED narrowly as frozen:** z = 0 g† = 1.003e-10 against CFG477's 9.686e-11, a 3.6% miss against a 3% tolerance. The redshift-dependent SHMR code path and seed differ; this is kept and disclosed.
- K2 PASS (Moster z-terms vanish at z = 0).
- MUTATE (halos frozen at z = 0): 4.88 → 0.57, detected (exit 1).

**Scope and caveats.**
- DC14 is used at its z = 0 calibration.
- Galaxy sizes scale as (1+z)^−0.75 at fixed baryon mass, applied to SPARC's z = 0 baryon distributions.
- The spread is large (16–84% at z = 2.5: 2.0–9.7), but the sign is robust.
- The record's earlier "ΛCDM-native +0.33 dex" (no feedback, a different construction) is smaller than this lane's +0.69 dex.

One-line summary: CFG565 feedback-ΛCDM g†(z) RISES (×1.2 / 2.8 / 4.9 at z = 1 / 2 / 2.5) vs the framework's ~0.8: an opposite-sign, ~0.8-dex discriminator at z ≈ 2.5 that clears the calibration floor.
