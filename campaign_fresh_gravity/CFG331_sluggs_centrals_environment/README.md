# CFG331: does the host environment remove the four SLUGGS centrals' excess?

**Verdicts (frozen criteria b0be6dc0c): R-own NOT SUPPORTED, R-bar NOT SUPPORTED, R-efe NOT SUPPORTED**, on both footings.

## Method
- Base: a copy of CFG330's K0 code (raw Forbes+17 GC velocities, JAM-calibrated law, γ = 3, isotropic, outer bins, ν_mono, κ = ½ FITTED).
- Host gas, all already on disk:
  - Lakhchaura+18 with CFG57's D1 convention for NGC 4374 and NGC 5846.
  - Fukazawa+06 for NGC 4365.
  - For M87: Lakhchaura, then Churazov+08, then Urban+11's Virgo slope to 1.2 Mpc.
- Members: 2MRS galaxies inside the outermost GC bin with |Δcz| < 3σ_V (KT17). Each is weighted by the central's mass scaled by its K-band flux ratio and placed at its projected radius, which gives an upper bound on its contribution.
- The readings follow PAPER35 §2 / FG001:
  - M87 and NGC 5846 are host centres.
  - NGC 4374 and NGC 4365 are accreted systems, so they get their own baryons only.

## Results (centrals' mean offset in dex; the other 12 stay at +0.056 canonical / +0.047 alt)

| reading | canonical | alt | drop of excess |
|---|---|---|---|
| K0 baseline | +0.224 | +0.213 | — |
| **R-own** | **+0.198** | **+0.187** | 15% / 16% |
| **R-bar** | +0.202 | +0.191 | 13% / 14% |
| R-barN (Newtonian gas, reported) | +0.215 | +0.206 | 5% |
| **R-efe** | +0.295 | +0.291 | −43% / −46% (EFE raises the offset) |

- **All four centrals are scorable.** Each has a measured gas profile.
- The measured gas fields are smaller than the GC radii for NGC 4374 (18 vs 22 kpc) and NGC 5846 (30 vs 54 kpc). Beyond the field the gas is the frozen power-law extrapolation.
- A group-scale X-ray profile is not on disk for NGC 5846 or NGC 4365.
- The largest single move is M87: +0.275 → +0.204 under R-own.
- Members barely matter. M87 has four small companions (ΔK +2.5 to +4.3, at 36–61 kpc) and NGC 5846 has one.
- R-efe: g_e is 0.23 a0 for NGC 4374 and 0.17 a0 for NGC 4365, and 0 at the exact centres. It can only enlarge the excess.

## Controls
- **C1 passes:** with host mass set to zero, every reading reproduces CFG330 K0 per galaxy to 1e-16.
- **C2 passes:** R-own leaves the 12 non-centrals unchanged as top-level systems.
  - An earlier draft wrongly added their own measured gas inside C2 and moved them by up to 0.0018 dex. That was fixed to match the frozen text, and it is reported separately: the mean is +0.0555 vs +0.0558.
- **C3 passes:** R-efe leaves the exact centres unchanged and lowers no offset.
- **MUTATE FAILS, and is kept:** with host mass ×10, the R-own mean only falls to +0.121 (canonical; a 61% drop) and does not go negative.
  - The pipeline responds to the host mass, but even ten times the measured host baryons do not close the excess.
  - So the measured environment is roughly an order of magnitude too small to explain it.

## Run
```
python3 campaign_fresh_gravity/CFG331_sluggs_centrals_environment/cfg331_environment.py
CFG331_MUTATE=1 python3 campaign_fresh_gravity/CFG331_sluggs_centrals_environment/cfg331_environment.py
```
