# CFG829 — does weak lensing show the dwarfs' excess at the dwarfs' own accelerations?

Criteria: `FROZEN_CRITERIA.md` (b941b73ce, before the script). Run: `python3 cfg829.py` (MUTATE `CFG829_MUTATE=1`). Seconds.
Data: Brouwer et al. 2021 (KiDS-1000 lensing RAR of isolated galaxies), public ESD profiles + covariances on disk.

## Result — CLASS (blue lenses, ν_e, canonical): **LAW HOLDS AT LOW g**
Window = the dwarfs' range, 10^−13.3 ≤ g_bar < 10^−11.9 m/s². A = full-covariance amplitude of the data over the law.

| lenses | A (canonical, ν_e) | dex | (A − 1)/σ | (2.75 − A)/σ | alt footing A |
|---|---|---|---|---|---|
| **blue, u−r < 2.5 (late types)** | **1.016 ± 0.086** | **+0.007** | **+0.2** | **+20.2** | 0.928 ± 0.078 |
| red, u−r > 2.5 (early types) | 1.587 ± 0.076 | +0.201 | +7.7 | +15.3 | 1.448 ± 0.070 |
| all isolated | 1.439 ± 0.050 | +0.158 | +8.8 | +26.4 | 1.313 ± 0.045 |
| isolated dwarf lenses (B21 Fig 10) | 1.397 ± 0.174 | +0.145 | +2.3 | +7.8 | 1.274 ± 0.158 |

(The simple-ν kernel gives the same numbers to 0.001.)
- **Isolated late-type galaxies sit exactly on the law at the accelerations where the satellite dwarfs sit 2.75× above it.**
  The dwarf excess is excluded in isolated discs at 20σ. Even B21's isolated low-mass lenses are 7.8σ below the dwarf value.
- So CFG828's ultra-low-acceleration excess is **not a failure of the law's deep regime**. It belongs to the satellite
  dwarfs (MW and M31 companions): tides / non-equilibrium, binaries, the host's field, or their baryon/kinematic accounting.
- The red-lens excess (+0.20 dex) is the known early-type excess (theory open item), seen here at low g too.
- **Positive for the framework:** the galaxy law, with κ fitted on discs, holds for isolated late types down to
  g_bar ≈ 7 × 10⁻¹⁴ m/s² with no extra parameter.

## Controls
- K1 PASS: blue lenses in the calibration window [10^−11.9, 10^−10.9) give A = 0.79 ± 0.14 (2 points), within 3σ of SPARC.
- MUTATE bites: g_obs × 2.75 → LAW-SHAPE.
- Caveats: lensing assumed to trace the dynamical g (as CFG801–805); B21's g_bar (stars + cold-gas estimate) used as published.

κ = ½ fitted; cold energy mass required; not theory closed.
