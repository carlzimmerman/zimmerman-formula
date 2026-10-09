# Overall assessment, 2026-10-09 (candidate B: law switched off outside bound halos + cold energy)

κ = ½ is fitted. The two footings (9.36e-11 / 1.13e-10) are never pooled. The cold energy's mass is still required. This is not a closed theory. Every line below cites a committed lane.

## Passes
| front | result | lanes |
|---|---|---|
| Structure growth, zero-knob rule | 16/16 runs GROWTH OK, including two 512³ realisations; the broken control fails | CFG424–427, 439, 460; PAPER45 v2.1 |
| Growth with the census (depletion-consistent) placement | 256³ GROWTH OK on both footings (σ8 1.0028 / 1.0036, max\|P−1\| 0.023 / 0.030); MUTATE TENSION 0.139; K1 reproduces CFG424 to 1e-8. **512³ CONFIRMED** (σ8 1.0047, max\|P−1\| 0.0285) for k ≤ 1 only; small scales in tension (CFG521). Scope: resolved hosts are groups/clusters (census f_ret 0.43–0.90); the f_ret ≈ 0.10 galaxy regime is untested | CFG518 |
| Rotation curves (SPARC) | the census edge passes; round enclosed-mass rule within 0.02 dex of full QUMOND | CFG515, 516 |
| Milky Way vertical force | round cold energy beats the QUMOND phantom disc in 32/32 cells; MUTATE restores the rejection | CFG514, 516 |
| Early-type lensing levels | pass with the census edge (−0.05 / −0.12 vs B1) | CFG515 |
| Clusters | pass (blind, declared) | CFG515 |
| MW satellites | recover under the census edge (2/39 unbound) | CFG515 |

## Fails, or open with a known cause
| front | result | lanes |
|---|---|---|
| Local Group timing | was z +13.5 (CFG515: radial-only orbit, 4.4 km/s error only). With M31's tangential motion and full errors the census is at z_full +2.2 (+2.7 LMC, +3.0 M33): DATA-ISSUE, fragile. A derived shared-catchment rule (the pair shares one supply; f_LG 0.170, −28% mass) gives z_full −0.1 to +1.0 but still z +4.4 on the strict radial statistic. LG timing only weakly discriminates (allows common f_ret 0.12–0.30); it rejects f_ret = 1. Literature values PROVISIONAL (recalled) | CFG515, 522 |
| KiDS, alt footing | census edge +8.84 FAIL (canonical +3.20 PASS). CFG525: DATA-ISSUE from the isolation selection. On the strictly isolated f30 lenses (57k) the census edge passes both footings (−0.24 / +1.00) and still rejects f_ret = 1 (+53 / +62); the miss comes from the 124k less-isolated lenses (+22 / +31). No derived mechanism (shared catchments do nothing after the isolation cut). In the fixed ΛCDM-built environment (CFG503, leakage 0.223) the edge fails both footings (+19.4 / +20.5); reported, not adjudicated; an f30-matched environment is the next step | CFG515, 525 |
| Lensing environment ruler (ΛCDM-built) | MODEL STILL INADEQUATE: G1 and G2 pass, G3 fails at 50.9/15. With the measured leakage 0.223, CFG503's ΛCDM G1 passes (34.3 → 26.1); G3 not re-scored. Edge still about 300 above F_dd on both footings | CFG504, 520 |
| Lensing environment ruler (native) | INVALID: too many satellites in the box (0.34–0.43 vs the measured 0.223 ± 0.004). CALIBRATION FAILED: at 512³ the box cannot reach the flat measured parent fraction of about 0.31 (it resolves no hosts below log M_ta 11.9). Needs 1024³ or a zoom | CFG506, 519, 520 |
| SLUGGS centrals | CFG528/528b: GENUINE TENSION. With MEASURED GC profiles and anisotropy (six papers, owner-approved fetch), the joint best case leaves +0.07 / +0.06 dex mean (class 3.5σ / 2.8σ, statistical only). M87, NGC 4365 and NGC 5846 stay +0.09–0.14 dex; NGC 4374 clears. IMF, distance, hot gas, census edge and round rule all fail; the shallow-tracer escape is not supported by the data. Residual ≈ the 0.05–0.075 dex per-galaxy systematic, so per-galaxy Z overstate certainty. Not a foreground effect (velocity spreads; directions 49–88° from the Galactic centre agree) | CFG466, 492, 528 |
| Supply postulate | not derivable under G9 (six attacks) | CFG461, 462, 488, 490, 494, 497 |
| Chassis | A WORKS-CONDITIONAL (O(v) bounded; collapse item 2c open); B FAILS; C viable with conflicts | CFG469, 499, 500 |
| GR + cold-energy relaxation | DEAD | CFG489 |
| Small-scale power (k ≳ 2 h/Mpc) | NEW TENSION: once host interiors are resolved, P/P_S0 falls to 0.63 at k 4 (L 50) and 0.44 at k 8 (L 25), growing with time and NOT converged with resolution. f_ret = 1 shows it too; no-compensation does not. Cause: per-catchment compensation draws from dense cores, so halos are less concentrated. CFG524: drawing only from the unsettled reservoir (R2 literal, R1 alternative, both run) does NOT fix it (L50 k 4: 0.66 / 0.62; still deepens with resolution). In this engine the settled phantom sits in the outskirts, so the reservoir is mostly in the cores. Every per-catchment draw tried de-concentrates halos; no forced rule fixes it. CFG526: ENGINE ARTEFACT (both footings). The law's own halo (baryons + phantom inside the census edge) is as massive in the core as the S0 halo; the engine holds only 0.51–0.77 of it, the shortfall tracks the grid, and the no-compensation run sits within 0.05 dex of the law. Causes: the pressure-filtered MOND input plus the core draw. Against cosmic-shear suppression (KiDS/DES A_mod, PROVISIONAL): NOT DIAGNOSTIC, not excluded. Law-respecting rule: draw from outside the census edge, source from unfiltered baryons (CFG527). Growth passes hold for k ≤ 1 only. The galaxy-regime f_ret ≈ 0.1 test was NOT ACHIEVED (groups overwrite galaxy catchments) | CFG521 (CFG506 diag., CFG518) |

## Not diagnostic yet (data-limited)
- **κ:** 0.42 ± 0.10 (CFG493).
- **Data and probes:**
  - UFD infall (CFG463);
  - clusters vs the MW cold column, where any suppression is < 20% at 95% (CFG517);
  - bar friction (CFG560);
  - BX442 Keck (CFG437/438).
- **Theory questions:**
  - the origin of cold energy, which is an input (CFG507);
  - dark vs cold energy, two components (CFG508);
  - gravitational waves (CFG512).

## Live forks and new predictions
- a₀ tracking ρ_DE vs the tension −p_DE (CFG511).
- PBH window 10¹⁷–10²² g, with a LISA test (CFG510).
- Small-scale power 16–20% below S0 at k 2–3 h/Mpc at 512³ (CFG506 diagnostics; near the mesh limit).
- **Decisive data still to come:**
  - the Gaia DR4 K_z map and wide binaries (DR4 on 2 Dec 2026);
  - a₀ at z ≈ 2.5;
  - edge-on σ_z and HI flaring (round rule vs phantom disc ×1.6–3.6).

## Bottom line
The growth clash is close to dissolved on large scales (k ≤ 1), but resolved halo cores show a new small-scale power deficit caused by where the compensation draws cold energy from (CFG521). Census placement keeps growth OK (256³ both footings, 512³ confirmed; group-scale hosts only) while fixing early-type lensing, SPARC, satellites and clusters. KiDS on the alt footing passes on the strictly isolated lenses and misses on the less-isolated ones (a selection issue, CFG525); the Local Group timing miss was mostly a scoring simplification (CFG522), with a residual +4.4σ on the strict radial statistic. The lensing environment ruler is the remaining measurement problem. Its satellite input is now measured (0.223). With that input the edge stays about 300 worse than the best framework lens, and the native ruler needs a finer box (1024³ or a zoom) before it can judge.
