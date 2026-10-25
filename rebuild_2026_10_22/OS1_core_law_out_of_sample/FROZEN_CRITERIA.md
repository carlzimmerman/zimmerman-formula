# OS1_core_law_out_of_sample — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25 at the owner's request: "calibrate q once on SPARC alone (one constant), then grade X30's cluster cells and
CD1's dwarfs at that q, both footings." κ = ½ FITTED. Footings canonical / alt, calibrated and scored separately, never
pooled. Cold dark energy (not matter, never a particle). Nothing here says the data favour the framework or ΛCDM. Not
"theory closed".

## 0. Law (SC1, unchanged except q)

X38's route-E Burkert halos with Σ_i = Σ_a0 (σ_i/σ_ref)^q, where:
- Σ_a0 = a₀/(2πG);
- σ_ref = 70.50 km/s, the median SPARC V_last/√2 (SC1);
- the σ conventions are SC1's: SPARC V_last/√2; clusters √(kT/0.6 m_p) with the tercile fill.

**Dwarfs (fixed now).** σ_i is the binary-corrected dispersion implied by X1's Δ[Newton]: σ_i = √(g_obs r₁₂ / 3), with
g_obs = g_N · 10^Δ. Each dwarf's cap is g_cap,i = 0.254484 a₀ · (σ_i/σ_ref)^q (CD1's ceiling at that dwarf's Σ; LN1
certifies the ceiling ≤ 9/32 a₀ per unit Σ_a0). S_i = g_h,req,i / g_cap,i, and z_i is computed exactly as in CD1.

## 1. Calibration (SPARC only, once per footing)

- q_f = argmin over q of SPARC rms with EM1 background A (X38's `sparc` with Σ_i), on a grid 0.00–1.20 in steps of 0.02,
  then refined in steps of 0.002 within ±0.02 of the coarse minimum.
- If the line (rms ≤ 0.110, 0.50 ≤ median Υ ≤ 0.80) fails at q_f, the lane stops and reports it. q_f is not moved.
- Background B at q_f is reported. No cluster or dwarf number is computed before q_f is fixed and printed.

## 2. Out-of-sample grades at q_f

- **Clusters:** X38's 15 cells, both h; a cell passes if |Z| ≤ 2 at both.
  - PASS = every cell passes.
  - IMPROVE = no cell that passes in X38 fails, and the summed |Z| of X38's failing cells falls ≥ 50%.
  - FAIL = otherwise.
- **Dwarfs:** CD1's rule on X1's 89 dwarfs per footing.
  - EXCLUDE: ≥ 25% have z ≥ 2.
  - CONSISTENT: < 5% have z ≥ 2 and median S ≤ 1.
  - PARTIAL: otherwise.

| lane class (per footing; the verdict needs both footings to agree, else UNDECIDED) | rule |
|---|---|
| OS PASSES | clusters PASS and dwarfs CONSISTENT |
| OS CLUSTERS PASS, DWARFS FAIL | clusters PASS, dwarfs not CONSISTENT |
| OS DWARFS HOLD, CLUSTERS SHORT | dwarfs CONSISTENT, clusters IMPROVE or FAIL |
| OS FAILS OUT OF SAMPLE | clusters FAIL and dwarfs EXCLUDE |
| OS MIXED | anything else |

Reported only: the dwarf grades by X1 class; the q at which dwarfs would cross into EXCLUDE (from the same formula); and
cluster cells at q_f ± 0.05.

## 3. Checks

- **K0** At q = 0: SPARC equals X38 (to 1e-9), the clusters equal X38 (to 1e-6), and the dwarfs equal CD1 (fraction
  0.011, median S 0.53 / 0.44 to 0.005).
- **K1** At q = 1/3: SPARC equals SC1 (0.0686 / 0.0636 to 5e-5).
- **K2** Peak RSS < 2 GB, one thread.
- **MUTATE=1** (separate outputs): permute σ across the SPARC galaxies (seed 20261025), then calibrate. The rms gain over
  q = 0 must be under one third of the real gain. Exit 1 if so.

## 4. Disclosed before freezing

- **SPARC.** SC1's reported-only rows show SPARC rms falling from q = 0 to q = 1/2. The minimum may lie at q ≥ 1/2.
- **Hand estimate for dwarfs.** Their σ is about 5–10 km/s, so their S grows by about (σ_ref/σ)^q ≈ 10^q. CD1's median
  S was 0.53 at q = 0, so at q ≈ 1/2 the median becomes ≈ 1.7. Dwarfs are therefore expected to fall to PARTIAL or
  EXCLUDE if q_f ≥ 0.4.
- **Expected outcome.** The likely result is a tension (OS CLUSTERS PASS, DWARFS FAIL, or OS MIXED), written down now.
