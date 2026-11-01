# SL2_inverse_core_ratio: THE VIRIAL LAW FAILS, SCALES DISAGREE, EVEN WITH ε FITTED. A IS FLAT NEAR 0.8 ACROSS SPARC, STILL BELOW 1 ON GROUPS, 1.22–1.80 ON CLUSTERS: NO CROSSING AT 10¹²

Criteria: `FROZEN_CRITERIA.md` (74f5323f29). `sl2.py`, `sl2.out`, `sl2_results.json`, `sl2_cluster_exact.json`. `INVENTORY_2026-11-01.md`: read-only record of the last two weeks, partly title-level; see its own header. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework. Not blind.

| Scale | lg M200 | A_req | Relay's curve |
|---|---|---|---|
| LITTLE THINGS | below 10 | 0.45–0.64 A; 0.45–0.67 B | |
| V 20–60 | 9.97 | 0.84 [0.73, 1.00] | 0.70 MISS |
| V 60–100 | 10.59 | 0.84 [0.69, 0.88] | |
| V 100–150 | 11.13 | 0.74 [0.64, 0.88] | 0.80 HIT |
| V 150–200 | 11.76 | 0.95 [0.80, 1.22] | |
| V 200–250 | 12.11 | 0.80 [0.70, 1.13] | 0.95–1.00 HIT |
| V 250–400 | 12.27 | 0.61 [0.43, 1.03] | |
| Groups, |Z| ≤ 1.5 | 12.76 | below 0.96 | 1.35 MISS |
| Clusters, all 15, exact, both footings | 14.48 | 1.22–1.80 | 2.30 MISS |
| X-COP | 15.4 | line never met; mean 0 near 1.3, rms 0.134 at 1.22 | |

**Reads:** not MONOTONIC on SPARC. **CROSSES AT 10¹²: NOT SUPPORTED:** A = 1 lies in 4 of 6 bins' intervals, including 10¹⁰, and groups stay below 1. A(Υ) at 0.55; 0.60 and the S-based values are in `sl2.out`.

**ε_req (W_core0):** 1.1–1.5e-4, 1.3–1.7e-4, 2.3–3.0e-4, 6.8–7.8e-4, 1.1–1.3e-3, 0.8–1.3e-3; groups negative; clusters 0.011–0.026. **NO OVERLAP.** Forward: bound on every system only for ε ≤ 1.1e-5, where gate is 43.5 (baseline 10.7). Halo-W normalisation doesn't change the verdict: clusters need 0.4–1.0, far above galaxies' upper bounds. q_contract zero on clusters was by hand, and ε fitted. Galaxy and cluster fractions differ by about 100, in line with OC1's 61.

**Post-result, reported only. One constant A on SPARC removes the tilt:** A 1.0 +0.52, 0.9 +0.31, 0.85 +0.13, 0.8 −0.21, Υ 0.78 → 0.56, ET1's six bins pass at 0.80. LITTLE THINGS doesn't, +0.086. So the 1.20 → 0.57 run behaves like an overall S normalisation near × 1.4, the 1.2–1.6 need/native ratio in CR2. Not derived. f_c = 0.84 lies nearby: coincidence until shown otherwise.

Checks: K1, K2, K3 pass; MUTATE bites. Inherits NR1's ANCHOR-DEPENDENT low masses.
