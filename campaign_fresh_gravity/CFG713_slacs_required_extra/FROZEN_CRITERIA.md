# CFG713 FROZEN CRITERIA: what extra mass do SLACS lenses require beyond stars + the law? (block CFG710–719)

Date: 2026-10-13. Committed ALONE before any CFG713 code or number. Uses CFG712's inputs (43 SLACS lenses: Etherington+2022 θE and
imaging-only γ — already read in CFG712; Auger+2009 light, z, SPS log M* Chabrier/Salpeter). κ = ½ FITTED; footings separate;
cold energy mass required; no particle species; not "theory closed". Inference lane: it measures what is missing; it scores two
hypotheses.

## Models per lens (de Vaucouleurs R_e(I), the law with ν_mono, Planck18 distances; κ slope at θE as in CFG712)
- **H-IMF (stars + law, M* free):** the only freedom is M*; θE fixes it. Report whether any M* reproduces γ_obs within its error
  (scan log M* over 9–13 ignoring θE): H-IMF EXCLUDED for a lens if no M* in [SPS Chabrier − 0.2, SPS Salpeter + 0.3] dex gives
  |γ − γ_obs| ≤ 1σ_obs while matching θE to 5 %. Population: H-IMF EXCLUDED if it fails for > 50 % of lenses.
- **H-X (stars + law + extra cold component ρ_x ∝ r^−2, i.e. isothermal):** two unknowns (M*, f_x = extra's share of the projected
  mass inside θE), two constraints (θE, γ_obs): solve per lens. Report median and spread of f_x, and the implied M* vs SPS
  (Chabrier / Salpeter offsets). f_x ∈ [0, 0.95]; lenses needing f_x outside are flagged.
- Diagnostics (no verdict): Spearman of f_x vs σ_e/2-free quantities available on disk (R_e in kpc, θE/R_e, log M*_SPS); f_x/(law's
  own cold fraction inside θE).
## MUTATE (`CFG713_MUTATE=1`): replace γ_obs by the law's own γ_pred → f_x must collapse to ≈ 0 (median |f_x| < 0.02) (exit 1 iff it bites).
