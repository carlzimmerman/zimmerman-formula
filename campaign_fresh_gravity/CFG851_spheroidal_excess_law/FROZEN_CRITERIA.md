# CFG851 FROZEN CRITERIA: one excess law for spheroidal systems? Calibrate on red lenses, predict the dSphs blind (before any script)

**Why.** CFG829/846/849/850: at low g_bar, spheroidal / gas-poor systems carry an excess over the law (red lenses ~+0.16 dex after
the M★ correction, satellite dSphs ~+0.4 dex), rotating / gas-rich ones do not. If the two are one phenomenon, a single relation
Δ_sph(g_bar) fitted on lenses (masses ~1e10–1e11 M_⊙, radii 30–3000 kpc) must predict the dSphs (1e5–1e7 M_⊙, 0.1–1 kpc).

## Calibration (red lenses only)
- B21 red (u−r > 2.5) isolated lenses, all 15 g_bar points, full covariance, CFG829 loader; M★ correction +0.123 dex on g_bar
  (CFG850 primary; uncorrected reported as bracket). g_law with ν_e, canonical a0 (alt reported).
- Model: Δ(g_bar) = b · max(0, log10(g†/g_bar)), i.e. g_obs = g_law(g_bar) · 10^Δ; two parameters b ≥ 0, g† > 0; fit by χ²
  with the covariance on g_obs. Report b, log g† and their 1σ ranges (Δχ² = 1 profiles).

## Blind prediction
- dSph sample = CFG828's pressure-supported dwarfs with g_bar < 10^−11.9 (Δ from CFG828, Υ_SFH). Predicted Δ at each dwarf's g_bar;
  compare the mean predicted with the mean observed; σ = √(SD_obs²/N + σ_pred²) with σ_pred from the calibration's 1σ range.
- **UNIFIED** if |Δ_obs − Δ_pred| < 2σ.
- **DSPHS ABOVE** if Δ_obs − Δ_pred ≥ 2σ (the dwarfs need more than the lens law gives).
- **DSPHS BELOW** if ≤ −2σ. **NOT DIAGNOSTIC** if the calibration leaves b unconstrained (1σ range includes 0 AND exceeds 1).
- Also reported (not classed): blue lenses' best-fit b (should be ~0 if the law is spheroidal-specific).

## Controls
- K1: b = 0 gives χ² of the law alone on red lenses (reproduce the CFG829-window amplitude sign).
- MUTATE (separate output): calibrate on BLUE lenses instead → must class DSPHS ABOVE (the disc law cannot predict the dwarfs).

κ = ½ fitted; cold energy mass required; not theory closed. A UNIFIED is an empirical regularity across scales, not a mechanism.
