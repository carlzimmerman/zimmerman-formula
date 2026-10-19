# CFG828 FROZEN CRITERIA: is the uniform dwarf excess about gravity at low acceleration, or about pressure-supported systems? (before any script)

**Why.** CFG827: with SFH-based stellar M/L, 25 of 28 independent dwarfs sit ~×2 in mass (σ ×1.45) above the galaxy law,
with no age dependence. Two readings make opposite predictions at MATCHED baryonic acceleration:
- **LAW-SHAPE:** the law itself under-predicts at low g_bar → rotating discs (SPARC) at the same g_bar sit above it too.
- **DISPERSION-SPECIFIC:** rotating discs at the same g_bar sit on the law; only pressure-supported dwarfs sit above
  (estimator, anisotropy, tides / non-equilibrium, or a real difference between the two classes).

## Rotation-supported sample (SPARC, Lelli+16; files on disk)
- Points from `real_research/data/sparc_data/*_rotmod.dat`; galaxy cuts from `SPARC_Lelli2016c.mrt`: Q ≤ 2, Inc ≥ 30°;
  point cut errV / Vobs < 0.10 (the Lelli+17 RAR cuts).
- g_obs = V_obs²/R; g_bar = (V_gas|V_gas| + 0.5 V_disk|V_disk| + 0.7 V_bul|V_bul|)/R (Υ_disk 0.5, Υ_bul 0.7 at 3.6 μm, the repo
  convention in `real_research/reviews/sparc_rar_honest.py`).

## Pressure-supported sample (CFG827 rows)
- The 36 dwarfs of CFG827 (28 out-of-sample + 8 MW training) with Υ_SFH at [M/H] −1.31, EXCLUDING the gas-rich rotating
  dIrrs whose gas CFG827 omits (WLM, NGC 6822, IC 1613, Leo A, Sagittarius dIrr, Pegasus dIrr) and M 32 (compact elliptical).
- r_1/2 = (4/3) r_h; g_obs(r_1/2) = 3σ²/r_1/2 (Wolf); g_bar(r_1/2) = G (M★/2) / r_1/2², M★ = Υ_SFH L_V.

## Law and residual
- g_law = g_bar ν(g_bar/a0), primary ν(y) = 1/(1 − e^{−√y}) (the kernel CFG821–827 use); bracket: the simple form solving
  g_N = g²/(g + a0). Canonical a0 = 9.3603e-11 (alt 1.1312e-10 reported). Residual Δ = log10(g_obs / g_law).

## Statistic and classes (primary ν, canonical)
- For each dwarf: Δ_SPARC(g_bar) = median Δ of SPARC points within ±0.15 dex of the dwarf's g_bar (requires ≥ 20 points;
  else the dwarf is "out of SPARC range"). D = Δ_dwarf − Δ_SPARC. Mean D over in-range dwarfs; error by bootstrap over
  dwarfs (2000 resamples, seed 828).
- **DISPERSION-SPECIFIC** if mean D > 0 with z ≥ 3.
- **LAW-SHAPE** if |z| < 2 AND the in-range SPARC median Δ (over the dwarfs' g_bar windows) ≥ +0.10 dex.
- **NOT DIAGNOSTIC** if fewer than 8 dwarfs are in SPARC range. **MIXED** otherwise.
- Report: SPARC Δ in g_bar bins (0.25 dex) over the whole range; the out-of-range dwarfs' Δ separately.

## Controls
- K1: SPARC overall median Δ within ±0.05 dex (the law is calibrated on SPARC-like discs).
- MUTATE (separate output): divide every dwarf σ by 1.45 → mean D must fall by ≈ 2 log10(1.45) ≈ 0.32 dex.

κ = ½ fitted; cold energy mass required; not theory closed.
