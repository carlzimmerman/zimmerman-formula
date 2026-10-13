# CFG712 FROZEN CRITERIA: SLACS imaging-only slopes (the CFG710 observable) predicted from light + the law — sealed before reading γ

Date: 2026-10-13. Block CFG710–719. Committed ALONE before any CFG712 code or number. κ = ½ FITTED; footings separate; cold
energy mass required; no particle species; not "theory closed"; nothing will say the data favour the framework.

## 0. Data and what has been seen
- **Slopes (scored only after sealing):** Etherington+2022 (arXiv 2202.09201, PyAutoLens imaging-only power-law fits to HST),
  Table "SLACS mass" (43 lenses): R_Ein,eff, γ, q, φ, external shear. **Seen:** the column headers; one row (J0008−0004, γ = 2.08)
  exposed while printing headers; the literature median 2.075 ± 0.024. No other γ value read.
- **Light + redshifts:** Auger+2009 (SLACS IX; record file `slacs_auger2009_lenses.tsv` used by h53/CFG33): z_l, z_s, R_e (I and V,
  de Vaucouleurs, HST). Matched by name.
- Motivation: CFG710 (B1938) matched on this observable (κ slope at θE), whereas CFG711's γ′ (lensing + dynamics) proved
  insensitive. Sensitivity here is checked by M1 before any score.

## 1. Prediction per lens (sealed before scoring)
Stars: circularised de Vaucouleurs (n = 4) with R_e(I) (primary; R_e(V) variant), Abel-deprojected; M* normalised so the law's
projected mass inside θE (= R_Ein,eff from Etherington — the only lensing input) equals Σ_cr π θE² (Planck18 distances); law with
the record's ν_mono via its h table; **γ_pred = 1 − dlnκ/dlnR at θE** (the CFG710 definition). Both footings.
`cfg712_predictions.json` is written and its sha256 committed BEFORE the scoring script reads the γ column.

## 2. Scoring (per footing; lenses present in both tables)
- **M1 tooth first:** pure stars (a0 → 0) must raise the median γ_pred by ≥ 0.15; else NOT DIAGNOSTIC (insensitive).
- T1 level: median Δ = γ_pred − γ_obs (bootstrap σ). CONSISTENT |Δ| ≤ 0.10; INCONSISTENT |Δ| > 0.20 and > 3σ; TENSION otherwise.
- T2 per-lens: Spearman ρ(γ_pred, γ_obs): PREDICTIVE ρ > 0, p < 0.01; NOT PREDICTIVE p ≥ 0.05 or ρ ≤ 0; WEAK otherwise.
- Context: B1938 (CFG710) shown on the same axes; stars-only predictions shown.
## 3. MUTATE (`CFG712_MUTATE=1`): M1 above; M2 shuffle R_e across lenses must lower ρ by > 0.2 (exit 1 iff both bite).
