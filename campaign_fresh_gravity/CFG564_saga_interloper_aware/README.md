# CFG564: SAGA satellite kinematics, interloper-aware. Frozen verdict LAW-FLAT in both footings, but NO model fits: the law is "best" only as the least-bad model, and SAGA's own background explains about a fifth to a third of the excess

**Ledger line:** CFG564 SAGA DR3 interloper-aware rerun of CFG562 (359 satellites, 101 hosts): SAGA's own redshift catalogue (Table C2; flat 275-1000 km/s sideband, magnitude-matched) gives a FIXED interloper fraction of only 0.044 (per radial bin 0.009/0.005/0.057/0.064), not the 0.21-0.38 CFG562's free fit needed. With it, the frozen verdict is LAW-FLAT in both footings (Delta(-2lnL): edge f_ret 0.18 +49.9/+51.7, NFW Moster +26.1/+33.7; edge 0.10 +12.0/+12.3, NFW-Lim +14.0/+21.5). But the law's goodness of fit is p < 0.002 (data -2lnL 4437 vs mock median 4330), and the scaled interloper fit wants 3-6x SAGA's background rate. All models under-predict the dispersion, and the excess sits inside +-275 km/s rather than in the sideband. With a free fraction the models stay within 3.5 (CFG562 reproduced 8/8). Edge 0.18 vs NFW: LOW-POWER (50% recovery). K3 shape-scale control failed (A 1.22 vs [0.8, 1.2], kept). MUTATE detected (NFW-PREFERRED, exit 1). kappa fitted; cold mass required, amount free; not a0; not theory closed.

Criteria `2c4c86f76` (committed alone before any script). Stage 1 (power, no velocities) `db3fa5c74`, committed before scoring.
Script `cfg564_saga_interloper.py` (`--stage power`, `--stage score`, `--mutate`; seconds each). Outputs `cfg564_{power,score,mutate}.out/_results.json`.
Data: C1/C3 from CFG562's copies. C2 (10.8 MB) is in `_external_data/cfg564/` (git-ignored). All sha256 values are in `FETCH_LOG.md` and checked by the script.

## Interloper estimate (frozen primary)
- C2 geometry check (K1): 99.7% of C3 satellites were found in C2. Recomputed R and dv match Rhost/DVhost (median 0.001 kpc, 0.8 km/s).
- C2 has 361 magnitude-matched objects in the window at 30-300 kpc, 359 of them SAGA satellites. Sideband counts 275-1000 km/s per bin: 1, 1, 15, 25. Expected interlopers 0.4/0.4/5.7/9.5 against 41/69/100/149 members, which is 15.9 of 359 in total.
- Variants: 275-2000 km/s sideband f_int 0.031/0.016/0.061/0.067. The sloped sideband fit (275-3000) has no slope (v_s at the grid top, so it equals the flat case).

## Power (stage 1, stated before scoring; 300 mocks per generator)
| generator | LAW-FLAT | SUPPLY EDGE | NFW-PREF | NON-DISC | median Delta(other - generator) |
|---|---|---|---|---|---|
| law (can / alt) | 0.89 / 0.92 | 0 | 0 | 0.11 / 0.08 | edge0.18 +26 / +33, NFW +21 / +26 |
| edge 0.18 | 0 | 0.50 / 0.41 | 0 | 0.50 / 0.59 | law +21 / +28, NFW +9.1 / +7.8 |
| edge 0.10 | 0.33 / 0.37 | 0.01 | 0.01 | 0.65 / 0.61 | law +3.0 / +4.4 |
| NFW | 0 | 0 / 0.01 | 0.50 / 0.49 | 0.50 | law +18 / +23, edge0.18 +10.5 / +9.1 |

The law-versus-rest call has power. Edge 0.18 and NFW are only about 50% separable, so any SUPPLY EDGE or NFW verdict here would be LOW-POWER: **an f_ret 0.18 edge and NFW remain hard to tell apart.** Edge 0.10 is mostly indistinguishable from the law (inside r_edge they are the same model).

## Result (stage 2)
- Primary, fixed f_int: **LAW-FLAT** in both footings. -2lnL values: law 4437.2 / 4429.7; edge 0.18 4487.1 / 4481.4; NFW 4463.3; NFW-Lim 4451.2.
  Edge 0.10: 4449.18 (can) / 4441.97 (alt); edge 1.0 4901.4 (excluded by about 460).
- The same verdict holds in the 275-2000 sideband, sloped sideband, beta 0.3 and Gold+Silver variants. Delta(edge 0.18) is +44 to +58 and Delta(NFW) +22 to +37.
- **The verdict cannot be read as "the law fits."** The goodness-of-fit p is 0/500 for the best model in both footings (the data sit about 107 / 79 above the law's mock median -2lnL). Every model under-predicts the dispersions, and the law wins because it predicts the highest dispersions, as in CFG562.
- **SAGA's background does not supply the interlopers CFG562's free fit needed.** Scaling the frozen shape (A x f_int) gives fitted A = 3.0-3.6 for the law and 5-6 for edge 0.18 and NFW. That is 3-6x the measured sideband rate, which rules out an uncorrelated background. Under free A: canonical NON-DISCRIMINATING (edge 0.18 +11.2, NFW +6.6), alt LAW-FLAT (+11.5, +10.6). Under a free constant f: NON-DISCRIMINATING in both footings (all models within 3.5, edge 0.10 -0.3 to -0.5).
- Reading: the high-|v| members are inside +-275 km/s, and the 275-1000 km/s shell near the hosts is nearly empty (2 objects inside 110 kpc). Two explanations fit this. Either they are bound members and every isolated-host model here is too low (baryon mass, external field and the point-mass treatment are not tested here), or they are correlated structure (group neighbours, splashback) confined to the window. This lane cannot separate the two.

## Controls
- K0 sha256: pass. K1 geometry: pass (relativistic dv formula used; cz - HRV also passes).
- K2 reproduces CFG562's free-f numbers 8/8 (-2lnL within 0.05, f within 0.002): pass.
- K3 injection: each generator (law, edge 0.18, NFW) has its own model at the lowest median -2lnL (pass). The shape-scale A recovered on 50 law mocks has median 1.22, outside the frozen [0.8, 1.2]: **FAILED, kept**. With f_int around 0.05, A is poorly constrained (grid up to 15.6), so the fitted-A values above carry roughly that much bias upward.
- MUTATE (NFW velocities + interlopers at fixed f_int): verdict NFW-PREFERRED (law +21.2 / +23.8) → detected, exit 1.

## Departures / disclosures
- f_int is stacked over hosts and taken flat in velocity. The tracer profile is not corrected for interlopers. Per-object velocity errors are not tabulated by SAGA, so eps = 20 km/s (as CFG562).
- The score run exits 1 because K3 failed. The verdict is unaffected (K3's A only concerns the reported free-shape variant).

## Owner items
- Do not cite LAW-FLAT as support for the law: no model fits (p < 0.002). The law is the least-bad of three isolated-host models.
- The open question is the origin of the excess (bound members versus correlated structure). Next steps could be host-environment splits (C1 count-MW, sep-massive) or a fitted host-mass offset. Each needs a new frozen criterion.
