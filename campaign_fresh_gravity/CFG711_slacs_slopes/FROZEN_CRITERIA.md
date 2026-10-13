# CFG711 FROZEN CRITERIA: does the law predict each SLACS lens's total density slope from its light? (block CFG710–719)

Date: 2026-10-13. Committed ALONE before any CFG711 code or number. κ = ½ FITTED; footings separate; cold energy mass required; no
particle species; not "theory closed"; nothing will be phrased as "the data favour the framework".

## 0. Data and what has been seen
Auger+2010 (SLACS X, arXiv 1007.2880) Table 1 from the paper's TeX (`_external_data/slacs_auger2010/T_lens_data.tex`): per lens
r_e,V (kpc), σ_e/2, log M* (Chabrier, Salpeter; context only), log M(<r_e/2) (total projected, lensing-anchored), f_DM, γ′ ± err.
Their γ′ is a power-law total density fitted to the lensing mass and σ_e/2 with an isotropic Jeans model and a Hernquist tracer.
**Seen before freezing:** the table rows were printed (γ′ column visible); the literature mean ⟨γ′⟩ = 2.078, intrinsic scatter 0.16.
No per-lens prediction or correlation has been computed. Motivation: CFG710 (one lens) — slope predicted from light 2.23–2.30, measured 2.234.

## 1. Prediction per lens (light + the law; the only mass input is the lensing M(<r_e/2) for normalisation)
- Stars: Hernquist (a = r_e/1.8153), M* free; total 3-D mass M(r) = from g = ν_mono(g_N/a0) g_N (the record's kernel, h-table form).
- Normalise M* so the law's PROJECTED total inside r_e/2 equals the tabulated M(<r_e/2).
- σ_pred: isotropic Jeans, Hernquist tracer, luminosity-weighted line-of-sight dispersion inside a circular aperture r_e/2.
- γ′_pred: the slope of the power-law total density (same projected mass inside r_e/2, same tracer, same isotropic Jeans, same
  aperture) that reproduces σ_pred — i.e. exactly Auger's mapping applied to the law's model. Both footings.
## 2. Statistics and verdict (per footing)
- T1 level: median Δ = γ′_pred − γ′_obs, bootstrap σ. CONSISTENT if |median Δ| ≤ 0.10; INCONSISTENT if |median Δ| > 0.20 and > 3σ_boot;
  TENSION otherwise. Also median Δlog σ (pred − obs), reported.
- **T2 per-lens (the distinctive test):** Spearman ρ between γ′_pred and γ′_obs. PREDICTIVE if ρ > 0 at p < 0.01; NOT PREDICTIVE if
  p ≥ 0.05; WEAK otherwise. Also: does the law reduce scatter — rms(γ′_obs − γ′_pred) vs rms(γ′_obs − ⟨γ′_obs⟩), reported.
- Context only: implied M* vs SPS Chabrier/Salpeter (the record's CFG33 IMF question).
## 3. MUTATE (`CFG711_MUTATE=1`, exit 1 iff both bite)
M1: a0 → 0 (pure stars) must raise median γ′_pred by > 0.3. M2: shuffle the r_e column across lenses must lower Spearman ρ by > 0.2.
