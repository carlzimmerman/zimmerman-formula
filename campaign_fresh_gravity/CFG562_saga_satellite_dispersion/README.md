# CFG562: SAGA satellite dispersions. Frozen verdict LAW-FLAT in both footings, but the result is FRAGILE to interlopers: the data sit ABOVE every model, and with a fitted interloper fraction the law, the f_ret 0.10/0.18 edge and NFW are all within Δ(−2 ln L) ≤ 4.2

**Ledger line:** CFG562 SAGA DR3 (101 MW analogues, 359 satellites at 30–300 kpc) stacked LOS dispersion, 2 host-mass × 4 radial bins: frozen verdict LAW-FLAT in both footings (χ²/8: law 8.75 / 5.99, p 0.36 / 0.65; supply edge f_ret 0.18 31.3 / 30.4; f_ret 0.10 15.3 / 13.3; NFW Moster+DM14 23.8, p 0.0025; NFW with SAGA's Lim+17 halo masses 11.3, p 0.18). Every observed bin is above every model (by 10–60 km/s), and with a fitted uniform interloper component all of these are within Δ(−2 ln L) ≤ 4.2 (fitted fractions 0.21–0.38): the binned preference reflects the high dispersions, and the interlopers could produce them. Only an edge at ≲ 100 kpc (f_ret ≈ 1) is robustly excluded. Forecast power: the binned test separates the edge from the law only at f_ret ≥ 0.18. Controls K1–K3 and both injections pass; MUTATE (NFW velocities) is detected (law p 9e-6, exit 1). κ fitted; the cold mass is still required, amount free; not a measurement of a₀; not theory closed.

Criteria `ac7e7cf84` (committed alone before any script). Script `cfg562_saga_dispersion.py` (~2 min). Data: SAGA DR3 Tables C1/C3 (Mao+2024, ApJ 976, 117), `data/`, sha256 in `FETCH_LOG.md` and checked by the script.

## Setup (as frozen)
- M_b = M* + 1.33 M_HI (79 hosts with HI), else 1.2 M*; log M_b 10.16–10.99, median 10.58. Point-mass baryons. No external field.
- (a) the law with ν_mono; (b) CFG398 supply edge: Keplerian on M_b(1 + 5.364/f_ret) beyond r_edge; (c) Moster+13 abundance matching + Dutton–Macciò NFW + baryons; (c′) NFW at SAGA's Lim+17 halo masses (reported).
- Isotropic Jeans with a power-law tracer fitted to the stacked radii (γ_t = 1.99), extended to 1 Mpc. Truncated-Gaussian MLE (|Δv| < 275 km/s, ε = 20 km/s). Bootstrap over hosts. Each model is binned by pushing mock velocities at the real positions through the same estimator.
- **SAGA hosts' r_edge (median):** canonical 405 kpc (f_ret 0.10) / 226 kpc (0.18); alt 368 / 206 kpc. Inside r_edge, settling and the bare law are the same model. With f_ret 0.10 most hosts' edge lies outside SAGA's 300 kpc aperture, so the test can only reach high retention.

## Primary result (all samples, 8 bins, diagonal errors)
| bin (kpc) | low-mass σ_obs | law (can) | edge 0.18 | NFW | high-mass σ_obs | law | edge 0.18 | NFW |
|---|---|---|---|---|---|---|---|---|
| 30–60 | 139 ± 40 | 94 | 89 | 90 | 196 ± 150 | 120 | 117 | 146 |
| 60–110 | 152 ± 43 | 91 | 81 | 80 | 137 ± 38 | 116 | 109 | 134 |
| 110–190 | 106 ± 19 | 92 | 72 | 71 | 141 ± 46 | 112 | 99 | 119 |
| 190–300 | 102 ± 12 | 86 | 57 | 60 | 132 ± 18 | 104 | 82 | 99 |

χ² (8 dof): law canonical 8.75, alt 5.99; edge 0.10: 15.3 / 13.3; edge 0.18: 31.3 / 30.4; edge 1.0: 102.5; NFW 23.8; NFW-Lim 11.3. The full-covariance values are within 2 of these.
Frozen rule: Δχ²(edge 0.18 − law) = 22.5 / 24.4 > 9, and the law has p > 0.01, so the verdict is **LAW-FLAT** in both footings. NFW-PREFERRED is not met.

## Why this does not show the edge is absent or the law is right
- **The data are above every model.** The law "wins" because it predicts the highest dispersion. A uniform interloper population inside SAGA's ±275 km/s window raises the measured dispersion in exactly this way. With a fitted uniform interloper component, the unbinned −2 ln L values are: law 4419.7 (can) / 4418.9 (alt), edge 0.10 4419.4, edge 0.18 4423.0 / 4422.3, NFW 4420.8, NFW-Lim 4424.1. The fitted interloper fractions are 0.21–0.38. On that likelihood the measurement **does not discriminate** among them. Edge 1.0 (r_edge ≈ 75 kpc) is still excluded (4467.8, Δ ≈ +48).
- NFW's binned rejection depends on the halo-mass recipe. Lim+17 group masses pass (p 0.18).
- An NFW mock (MUTATE) is classified SUPPLY EDGE SEEN: NFW and the f_ret 0.18 edge give nearly the same falling profile. A future "edge seen" would therefore not tell the edge apart from LCDM.
- **Power.** The forecast Δχ²(edge − law) with the data's errors reaches 9 only at f_ret ≥ 0.18 in both footings (0.10 → 1.5 / 2.4). Mock data from the edge model have smaller dispersions, and therefore smaller errors, so the injection recovers 0.18 at a median Δχ² of 68 (20/20). The forecast is conservative.
- **Variants (law / edge 0.18 / NFW χ², canonical):** Gold+Silver 8.5 / 32.2 / 22.7; all-host 4-bin stack 11.2 / 31.7 / 18.4 (law p 0.024); ε = 0: 10.6 / 35.6 / 27.5; ε = 40: 5.8 / 22.9 / 16.7; β = 0.3: 7.7 / 33.3 / 24.7; r_t = 0.6 Mpc: 14.6 / 33.5 / 27.7; r_t = 3 Mpc: 6.1 / 33.6 / 24.3. The verdict ordering holds in every variant.

## Controls
- K1: reproduces CFG398's committed x values exactly (max relative deviation 0). r_edge at log M_b 10.6 / 11.0: canonical 417 / 661 kpc (f 0.10), 233 / 370 kpc (0.18); alt 379 / 601 and 212 / 336 kpc. These match the brief's ranges.
- K2 (Jeans in a log potential, 126.50 vs 126.49 km/s) and K3 (estimator, 118.5 vs 120) pass.
- K-INJ: f_ret 0.18 recovered in 20/20 mocks (median Δχ² 68); f_ret 1.0 best in 20/20. Both pass.
- MUTATE (velocities drawn from NFW): law χ² 37.6 (p 9e-6) → detected, exit 1. Its verdict is "SUPPLY EDGE SEEN" (edge 0.18 χ² 6.9 vs NFW 9.8), which shows the edge/NFW degeneracy above.

## Departures / disclosures
- Per-object velocity errors are not tabulated by SAGA. ε = 20 km/s was declared, and 0 and 40 km/s are reported.
- The tracer slope comes from the stacked counts without completeness weighting, and the power-law projection is untruncated (declared).
- The interloper sensitivity was a frozen *reported* item, not a verdict input. The headline above gives it equal weight because it changes the reading.

## Owner items
- An interloper-aware rerun is needed before LAW-FLAT can be cited. Options: SAGA's own interloper rate (Paper III's background redshift Table C2, 10.8 MB, not fetched), or a mixture model frozen as primary. Either needs a new frozen criterion; Table C2 also needs a fetch go.
