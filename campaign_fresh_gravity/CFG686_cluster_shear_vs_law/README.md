# CFG686 — measured cluster shear vs the law from each cluster's own gas (criteria 8cef73ea7; block CFG680–689)

Raw KiDS-1000 shear (21.2 M sources; record's validated estimator conventions) around ACCEPT clusters (raw Chandra n_e) in the KiDS
footprint; distances from raw DESI DR2 BAO; no NFW, no ΛCDM halo. **8 clusters** pass the source/random checks (z 0.07–0.32: 2PIGG
J0011.5, 2PIGG J2227.0, A1835, A2744, A3088, AC 114, MACS J1115.8, MACS J2229.7).

Stacked ΔΣ (M☉/pc²) at R = 0.18 … 2.49 Mpc: 275 ± 129, 163 ± 82, 137 ± 59, 124 ± 39, 101 ± 27, 75 ± 19, 49 ± 13, 42 ± 9.
A = ΔΣ_obs / ΔΣ_law (bootstrap over clusters), primary bracket (β_out fit, f* = 0.20):
| band | law, canonical | law, alt | Newtonian baryons only |
|---|---|---|---|
| INNER 0.15–0.5 Mpc | 2.70 ± 1.47 | 2.51 ± 1.29 | 6.86 ± 4.29 |
| MID 0.5–1.2 Mpc | 1.70 ± 0.35 (+1.97σ) | 1.57 ± 0.34 | 5.03 ± 1.02 |
| OUTER 1.2–3 Mpc | **1.02 ± 0.24** | **0.94 ± 0.24** | 3.52 ± 0.91 |
Brackets (β_out ± 0.5, f* 0.10–0.30): MID 1.50–1.79, OUTER 0.80–1.19; 14 of 18 cells LAW SUFFICES, 4 CORE EXCESS.

**Frozen verdict: LAW SUFFICES (both footings)** — with honest qualifiers:
- Baryons alone fall 3.5–5× short at 0.5–3 Mpc; the law's own lensing mass from the gas (ν_mono phantom) accounts for the OUTER
  shear (A ≈ 1.0). MID carries a 1.6–1.8× excess at ~2σ, just under the frozen threshold — the size of the classic MOND cluster
  residual in cores; read as a HINT of core cold energy, not a detection.
- INNER is NOT USABLE: it fails both nulls (M1 cross −1.07 ± 0.52, M2 randoms −0.76 ± 0.31 in A units).
- The OUTER prediction leans on extrapolated gas: Chandra data reach only 0.23–1.35 Mpc; 5 of 8 clusters use the β = 2 fallback.
- Shape-noise ΔΣ errors are underestimated ~1.6× (M1 cross-shear χ² 20.4/8, one bin at 0.56 Mpc −3σ); the band verdicts use the
  bootstrap over clusters, which is larger. N = 8 makes the bootstrap itself crude.
Protocol deviations (disclosed, outputs kept): RUN1 frozen 'last 3 bins' slope diverged on ACCEPT's fine noisy bins
(`*_RUN1_slopebug.*`) → outer-half fit with β = 2 fallback; RUN2 projection mishandled the r = R singularity (SIS self-test 0.79 at
0.38 Mpc, `*_RUN2_projbug.*`) → r = R cosh u substitution; RUN3 self-test 0.996–1.000.
MUTATE: M1 cross-shear MID −0.17 ± 0.26, OUTER +0.08 ± 0.17 (A units) ✓ except INNER; M2 randoms χ² 2.9/8 ✓; M3 a0 → 0 raises A to 3.5–6.9 ✓.
Inputs outside the repo: `_external_data/cfg686_inputs/accept/all_profiles.dat` (Wayback copy of the ACCEPT site, sha256 bb762dff…),
KiDS columns cached from the SOM-gold FITS (sha256 dcc2bf03…). κ fitted; cold energy mass required; not theory closed.
