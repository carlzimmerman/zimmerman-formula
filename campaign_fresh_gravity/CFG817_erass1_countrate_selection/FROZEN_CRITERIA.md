# CFG817 FROZEN CRITERIA: eRASS1 count-rate selection forward model for the gas-mass Eddington bias (committed before any script)

**Why.** CFG816's −ασ² correction is a small-σ approximation, and its MUTATE did not bite. This lane forward-models how
eRASS1 actually selects clusters (on X-ray counts) to get per-cluster E[M_gas,true | M_gas,obs, z, exposure]. It is data
side only: no cosmology and no theory change. Catalogue: Bulbul+2024 emain, 12,247 rows (VizieR; `_external_data/
cfg817_erass1_selection/erass1_sel.tsv`).

## Model, every ingredient fitted to the catalogue itself
1. **Completeness C(N), with N = CTS500 (source counts).** Fit dN/d ln N ∝ N^−γ to the high-count end, where the histogram
   is falling. C(N) = observed / extrapolated, smoothed by a logistic in ln N.
2. **Counts–mass relation:** ln(N/Exp) = a + β ln M_gas − 2 ln d_L(z) + c z, fitted on clusters with N above the 90%
   completeness point. Intrinsic scatter σ_int comes from the residuals. d_L is computed from a flat expansion with
   Ω_m = 0.315 and H₀ = 67.4, used only for an inverse-square flux distance.
3. **Measurement error:** σ_meas(ln M_gas) as a function of ln N, fitted to the catalogue's own (ln B − ln b)/2.
4. **Intrinsic mass function:** dN/d ln M ∝ M^−α, with α refitted to the completeness-weighted counts above the peak.
5. **Simulation per target cluster** (the 318 of CFG687), at its own z and exposure:
   - draw true M from (4) over a wide range;
   - predict N from (2) with σ_int, then Poisson;
   - detect with probability C(N);
   - draw the observed M with σ_meas(N);
   - E[ln M_true] is the kernel-weighted mean over detected draws with ln M_obs within 0.05 of the cluster's value.
   - The correction is exp(E[ln M_true] − ln M_obs).

**Rescoring.** As CFG816: models' ΔΣ rescaled by correction^0.47; terciles re-binned by the corrected mass; plain law,
CFG809 and CFG815 P.

## Readings
- **CONFIRMS CFG816** if the per-tercile median corrections agree with CFG816's (0.29 / 0.84 / 0.95) within a factor of
  1.5, AND CFG815 P's corrected terciles are monotonic.
- **REVISES** otherwise. Report the forward-modelled corrections either way.

## Controls
- K1: with no selection (C = 1) and σ_meas = 0, corrections equal 1 to within 1%.
- MUTATE (separate outputs): C = 1 (no selection, measurement scatter only). The low-mass correction must SHRINK compared
  with the primary. That is the selection tooth CFG816 lacked.

κ fitted; not theory closed. All fitted relations reported.
