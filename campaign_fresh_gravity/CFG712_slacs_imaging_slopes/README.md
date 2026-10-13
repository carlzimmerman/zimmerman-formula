# CFG712: SLACS imaging-only slopes vs light + the law — INCONSISTENT (canonical) / TENSION (alt); not predictive per lens

Criteria d73d64603 (alone first; block CFG710–719). Predictions sealed before the slope column was read: `cfg712_predict.py` →
`cfg712_predictions.json` (sha256 0034140e…5d2b, commit 7d2b2348e); stars-only and R_e(V) variants sealed too. Scorer
`cfg712_score.py` (verifies the hashes) → `cfg712.out`, `cfg712_results.json`. κ = ½ FITTED; cold energy mass required; not
"theory closed"; nothing here says the data favour the framework.

Data: Etherington+2022 (arXiv 2202.09201) imaging-only PyAutoLens power-law slopes for 43 SLACS lenses (θE used for
normalisation, γ only for scoring); Auger+2009 HST de Vaucouleurs R_e and redshifts (record file). Observable: κ slope at θE
(CFG710's definition).

| | canonical | alt |
|---|---|---|
| **M1 sensitivity** (stars-only − law, median) | **0.381 → bites** | |
| median γ_pred (law) / γ_obs / stars-only | 2.321 / 2.080 / 2.702 | 2.277 / 2.080 / 2.702 |
| **T1** median Δ = pred − obs | **+0.240 ± 0.054 → INCONSISTENT** | **+0.194 ± 0.050 → TENSION** |
| **T2** Spearman | −0.107 (p 0.49) → NOT PREDICTIVE | −0.093 → NOT PREDICTIVE |
| rms Δ vs observed scatter | 0.352 vs 0.226 | 0.324 vs 0.226 |

**Reading.** On the sensitive, imaging-only observable the law, fed each lens's light and normalised to its Einstein radius,
predicts slopes 0.19–0.24 too steep and does not rank lenses. SLACS lenses need more extended mass near θE ≈ 0.6 R_e than the law's
cold energy supplies — the same massive-early-type shortfall the record already holds (h53/B7: Einstein mass 14–18 % short; CFG580:
early-type shortfall is a limit of the law), now on an independent observable. **CFG710's B1938 match does not generalise:** there
θE ≈ 2 R_e, where the law's cold mass is larger. Caveats (not used to soften): de Vaucouleurs n = 4 for every lens rather than its own
Sérsic; Etherington's γ is a global power-law fit across the arc, not strictly local; ν_mono kernel.
