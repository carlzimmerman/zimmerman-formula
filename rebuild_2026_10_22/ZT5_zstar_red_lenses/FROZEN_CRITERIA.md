# ZT5_zstar_red_lenses — FROZEN CRITERIA (committed alone, before any script or number)

Runs Z★'s test **Z-T5** as frozen in `Z1_successor_design/TEST_PLAN.md` (0d1959a4f5): "Predicted red-to-law ΔΣ ratio
√(1 + (M_gas/M★)_blue,match) at matched M★ (RAW gas scaling on disk; if absent, STOP). **PASS**: S2's red inventory 1.313 /
1.200 within 2σ of the prediction per footing; blue stays at S2's 0.878 / 0.802." κ = ½ FITTED. Footings never pooled. No
dark-matter particle. Not "theory closed". Nothing here says the data favour the framework. One thread, < 1 GB, seconds.

## Implementation choices

- **Observed** (S2 committed, `S2_v3_lowg_lensing/s2_v3_lowg_lensing_results.json`, red R0 inventory at y_e = 0, the numbers
  the plan names): A_red = 1.313 ± 0.063 (canonical), 1.200 ± 0.058 (alt); blue 0.878 ± 0.074 / 0.802 ± 0.067. Check KS reads
  them from the JSON (tolerance 0.001 on the rounded plan values).
- **Red lenses' M★**: the record's KiDS lens catalogue `real_research/data/lensing_rar/lr_lenses.npz`, typ == 1 (u−r > 2.0,
  S2's membership), catalogue log M★ (h70). The prediction is averaged over these lenses (unweighted mean of √(1 + f_gas)).
- **RAW gas scaling (primary, G1)**: ALFALFA-SDSS (Durbala+20, `alfalfa_sdss_durbala2020_t2.tsv`): every row with logMHI,
  logMsT (Taylor M★) and g−i present; f_gas = 1.33 M_HI / M★; running median of log₁₀ f_gas in 0.1-dex M★ bins (bins with
  ≥ 20 galaxies), linear interpolation, flat extrapolation at the ends (fraction of red lenses outside the binned range
  reported). ALFALFA is HI-selected, so G1 is an **UPPER bound** on f_gas of blue galaxies at fixed M★, and so an upper bound
  on the prediction. Variant G1b (reported): only g−i ≤ 0.9.
- **G2 (SURVEY-CALIBRATION, reported only)**: B21/S2's cold-gas relation log₁₀ f_cold = −0.69 log M★ + 6.63.
- **Classes per footing (G1)**: PASS iff |A_red − pred| ≤ 2σ_A; FAIL otherwise; if FAIL with A_red > pred + 2σ_A, the fail
  holds a fortiori for any less biased gas sample (labelled ROBUST). The blue leg is by construction in Z★ (blue owners keep
  their gas: no release, law exact), stated, not computed. Overall Z-T5: PASS iff PASS on both footings; FAIL iff FAIL on
  both; else SPLIT.
- **Reported only (baseline consistency)**: S2's v3 model of the red lenses already carries B21 cold gas and a hot CGM of
  0.5 M★, so a baseline-consistent prediction is √[(1 + f_G1 + 0.5) / (1 + f_G2 + 0.5)], lens-averaged.

## Checks and `--mutate`

`zt5_red_lenses.py`: KS (S2 values), KG (G2 at log M★ 10.7 equals 10^(−0.753) to 1e-9), KN (≥ 1000 ALFALFA rows used; every
used bin ≥ 20), KR (RSS < 1 GB); exit 0 iff all pass. `--mutate`: M_HI multiplied by 0 (no gas) → the prediction is 1 and
check KM (prediction > 1) fails (exit 1). Outputs `zt5_red_lenses{,_MUTATE}.out`, `_results{,_MUTATE}.json`. Post-result
changes go in a dated AMENDMENT.
