# X32_bullet_cold_sector: does the X26 cold sector end up with the gas or with the galaxies in the Bullet Cluster?

Criteria: `FROZEN_CRITERIA.md` (57ff3e7df4, committed alone, before any script or number). `AMENDMENT_A1.md` (committed with
the script, before any graded number) records three changes:
- A1.1: the frozen M_sub fallback applies;
- A1.2: dt 0.1 Myr, N 5000;
- A1.3: a third, conservative fluid placement, F-c.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. The cold sector is gravitating field mass, never a
particle, in both readings. Not "theory closed". Nothing here says the data favour the framework. Every number below comes
from `x32_bullet_cold_sector.out` / `_results.json`.

## Verdict (frozen classes): **UNDECIDED** (check failure K4), both footings

| footing | (C) collisionless, σ_1D = c_s | (F) perfect fluid, c_s |
|---|---|---|
| canonical | EXCLUDED (fails in all 4 combinations) | TENSION |
| alt | EXCLUDED (fails in all 4 combinations) | TENSION |

**K4 fails.** At the low sheet c_s with v = 2700 km/s (canonical 556, alt 595 km/s), no cold mass can make up the main
aperture. The main's cold nucleus keeps only 0.003 / 0.005 of itself (see below), so the normalisation stalls at a residual
of 0.70 / 0.67. By the stop rule the lane verdict is UNDECIDED. The per-reading classes above are reported as computed. The
answer is **not** "fluid excluded, collisionless allowed".

## What happens, reading by reading

### The law alone (baryons + v3 phantom, no cold; reported)

Both peaks sit on the gas: δ = 0.19 (main) and 0.32 (sub), 40 / 51 kpc from the gas. Δκ is negative at both peaks. This
reproduces h57's 57-F with the v3 kernel. The law follows the baryons, and the baryons are mostly gas.

### (F) perfect fluid

- Mach v/c_s at 2700 km/s: 3.67–4.86 (canonical) / 3.55–4.54 (alt). At 4740 km/s: 6.44–8.53 / 6.23–7.97. The gas itself has
  Mach 3.0 (M06).
- **Under pressure stripping (frozen F-a, F-b) the fluid stays with the gas.** The sub's fluid peak lands on the bullet gas
  (δ = 0.00, |Z| = 5.12) and the sub's Δκ comes out negative, in every combination on both footings. F-a also puts the main
  peak on the main gas.
- **But at the sheet c_s the fluid is not an extended medium.** As an equilibrium tracer in the record-calibrated wells, it is
  a dense nucleus:
  - Gunn–Gott ram-to-thermal ratio at the sub's centre ≈ 0.0;
  - r_strip 1.5–3.2 kpc, yet f_core 0.90–0.98, i.e. nearly all of the sub's fluid lies inside the unstripped radius.

  Momentum, not pressure, then decides where it goes. Under A1.3's inelastic columns (F-c), the nuclei punch through each
  other and the peaks land on the galaxies (δ = 1.00 in 6 of 8 combinations). F-c then fails or is in tension only on the
  BCG1 aperture mass (Z_O3 +2.5 to +4.4 where the amount is sane). That gives F = TENSION on both footings, from the
  v = 4740 combinations (canonical c_s 736; alt c_s 761).
- **F's verdict therefore depends on the placement rule, not on the physics being settled.** If the fluid is extended, it
  goes with the gas and fails. If it is the dense nucleus that the sheet c_s implies here, it does not.

### (C) collisionless, σ_1D = c_s (σ_3D = √3 c_s)

- **The sub's cold nucleus survives intact:** f_ret = 1.000, Δx = 0.0 kpc in all 8 runs.
- **The main's cold nucleus is disrupted** by the head-on (b = 0) passage of the compact sub well (a ≈ 26 kpc):

  | v | f_ret (main), canonical | f_ret (main), alt | lag Δx toward the sub |
  |---|---|---|---|
  | 2700 km/s | 0.003–0.037 | 0.005–0.049 | 119–243 kpc (all runs) |
  | 4740 km/s | 0.52–0.59 | 0.52–0.59 | |

- So the main lensing peak falls back onto the main gas: δ = 0.24–0.48, |Z| 2.7–4.2, with Δκ_main negative in all 8.
- **Amount cap:** at c_s_max with v = 2700, A_tot = 5.6e15 (canonical) / 4.1e15 (alt), against a cap of 5.364 M_b = 1.28e15.
- **Reported, b = 150 kpc (PROVISIONAL).** f_ret(main) is 0.07–0.14 at 2700 km/s and 0.87–0.96 at 4740 km/s, with lags of
  82–155 kpc.
- **Reported, a CDM-like tracer** (σ_1D = 1311 / 1183 km/s, about V_c/√2 of each well): f_ret(main) 0.80 / 1.02, lag 9.1 /
  1.2 kpc. It survives where the sheet-c_s component does not.

## Predicted offsets against the observed ones (model frame; observed peaks on the galaxies, 209.4 / 194.1 kpc from the plasma)

| reading | main peak–gas offset (δ) | sub peak–gas offset (δ) |
|---|---|---|
| law alone | 40 kpc (0.19) | 51 kpc (0.32) |
| F-a / F-b (pressure) | 0 kpc (0.00) / ≈201–210 kpc (0.96–1.00) | 0 kpc (0.00) |
| F-c (momentum) | 210 kpc (1.00) | 158 kpc (1.00) in 6 of 8 combinations; 85 kpc / 267 kpc in the two runaway-A ones |
| C, b = 0 | 40–100 kpc (0.19–0.48) | 158 kpc (1.00) |
| observed | 209.4 kpc (δ = 1) | 194.1 kpc (δ = 1) |

The model frame's galaxy–gas separations are 210 / 158 kpc. Clowe's κ̄ normalisation differs from Σ_crit 1.827e9, so only
the sign of Δκ is graded.

## Numbers and provenance

- **Sheet c_s at the KT median:** canonical 556–736, alt 595–761 km/s (X26 JSON `energy`; K0a recomputes it to 1.2e-3).
- **Baryons and the BCG / gas positions:** the h57 Plummer model, Famaey 2026 Table 1 as transcribed (K0b reproduces the h57
  masses to 8e-5).
- **Lensing masses within 300 kpc:** 3.5e14 / 2.3e14 (h57; Rihtaršič+2026 via Famaey).
- **Σ_crit:** 1.827e9 (h57).
- **Clowe 2006 Table 2:** coordinates, κ̄ and the 8σ significance (`bullet_data_table.py`; K0c gives 209.4 / 194.1 /
  721.5 kpc).
- **Speeds:** 2700 km/s (Springel & Farrar 2007), 4740 km/s and Mach 3.0 (Markevitch 2006).
- **Masses:** M200 1.5e15 (main) and the 2.3e14 sub fallback (Markevitch 2002), via `bullet_data_table.py`. K0d checks all 28
  transcribed strings against the record.
- **PROVISIONAL:** b = 150 kpc (reported only); the 15 % aperture-mass error in O3.
- **Wells:** the M200 pair has no Hernquist calibration (A1.1). With the fallback, a_main 450.3 kpc, a_sub 25.6 kpc; V_c(300 kpc)
  is 1854 / 1673 km/s.
- **Reported, the Bullet's own c_s** (σ 1500 km/s from 14.1 keV; ρ_b(<548 kpc) 1.0e-4 / 6.0e-5): 649–1004 km/s (main),
  571–878 km/s (sub).
- **Reported, at z = 0.296:** the c_s factors are 0.52 / 0.40 / 0.24 for p = 3 / 4 / 6.

## What this implies for the micro-nature (reported only)

1. **An extended, pressure-supported cold medium fails the Bullet.** It goes with the gas, as the law's phantom does. This is
   the COLD_SECTOR_SPEC §2.4 statement, now quantified: δ = 0, |Z| = 5.1, and a negative Δκ at the subcluster.
2. **Being collisionless is not enough at the sheet temperature.** With σ_1D = c_s ≈ 0.4–0.6 σ_well, the cold sector is a
   compact nucleus in each well. A head-on passage blows the main's nucleus away (b = 0; and at 2700 km/s even b = 150). A
   CDM-like dispersion survives.
   - What matters here is concentration relative to the well (c_s/σ_well), not fluid versus collisionless.
   - At these concentrations even a fluid nucleus passes through on momentum grounds (F-c).
3. **This bears directly on X30.** A cold sector at 556–761 km/s cannot be the extended dominant mass of a σ ≈ 1200–1300 km/s
   well as an equilibrium tracer: it collapses to a nucleus. Its self-consistent profile (it *is* most of the well) is outside
   this rigid-well toy, and it decides both the Bullet and the cluster-profile tests.
4. **R6 is therefore neither confirmed nor refuted.** The Bullet needs a component that rides with the galaxies. In this toy,
   the X26 sheet supplies one only if it is concentrated and the encounter is not head-on, or if its dispersion is near
   σ_well (CDM-like). Near σ_well conflicts with the sheet's c_s ≈ 1.1–1.5 σ_KT only through the σ_KT vs σ_well (lensing)
   difference in the Bullet, which is not resolved here.

## Is a collisionless, late-heated cold sector distinguishable from dark matter? (reported)

- **In the Bullet: yes in principle, by retention.** f_ret(main) is 0.003–0.59 for σ_1D = c_s, against 0.80–1.02 for the
  CDM-like comparator. But in this toy the difference is set by the well model and b.
- **In the record's other tests:**
  - R3 / SPARC: absent from isolated galaxies (X22, X26 C-SPARC);
  - the X22 forest and σ₈: the late c_s rise suppresses small-scale power after z ≈ 2;
  - X29: late-time S8 (peer lane);
  - X30: the cluster core profile.

  CDM predicts none of these departures. Being collisionless does not make it a particle: the cold sector stays field mass.

## What this does not show

- **The wells are rigid Hernquist spheres** calibrated to two aperture masses. The sub's a ≈ 26 kpc is forced by the record
  numbers, and the cold's own gravity does not respond. Galaxies are not simulated: their centroid is the well centre. The
  constant relative speed is an impulse-approximation stand-in for the real orbit.
- **The phantom** is QUMOND-type (h57's estimator), not an AQUAL solve.
- **The fluid placements are rules** (F-a, F-b pressure stripping; F-c inelastic columns), not hydrodynamics.
- **F takes its amount from C's normalisation.** Where C's main nucleus is destroyed, A runs away (up to 5.5e15), and F-c's
  O3 failures there are an artefact of that coupling.
- **Clowe's κ̄ normalisation** is not matched, so only Δκ signs are graded.

## Checks (10/11 PASS; K4 FAIL) and MUTATE

| check | result |
|---|---|
| K0a X26 sheet | 19 / 16 points, c_s reproduced (dev 1.2e-3) |
| K0b h57 reproduction | max dev 8.4e-5 |
| K0c Clowe offsets | 209.4 / 194.1 / 721.5 kpc |
| K0d transcribed strings | 28 / 28 found |
| K0e well calibration | fallback, a_main 450.3 / a_sub 25.6 kpc |
| K1 deep-MOND cylinder | −0.57 % |
| K2 control equilibrium | min 0.9972 |
| K3 map vs surface phantom | −3.0 % |
| **K4 normalisation** | **FAIL, residual 0.70** (c_s_min, v = 2700, both footings) |
| K5 RSS | 0.84 GB |
| K6 dt halving | Δf_ret 0.0000 |

**MUTATE** (`X32_MUTATE=1`): K0b FAILS (0.92), K0c FAILS, K2 FAILS (0.0000). The verdict is UNDECIDED (step 0), exit 1, as
required.

## Run

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X32_bullet_cold_sector/x32_bullet_cold_sector.py               # ~10 min, 0.84 GB
PYTHONHASHSEED=0 X32_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X32_bullet_cold_sector/x32_bullet_cold_sector.py # exit 1 by design
```
