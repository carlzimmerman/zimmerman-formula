# CFG656: the X-COP cold-energy supply from the framework's own turnaround catchment and the measured gas. No supply rule passes T3. The H-CB result is decided by gas BEYOND the X-ray data. Candidate B does not depend on the supply at all

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in c1236bf88 before any catchment, supply or gate number. Date 2026-10-12.
- **Settings:** κ = ½ is FITTED. Footings are canonical 9.3603e-11 / alt 1.1312e-10 and are never pooled. "Cold energy" throughout; its MASS is still required; no particle species. Not "theory closed". No ΛCDM halo shape or mass function and no standard-MOND yardstick enters any verdict.
- **Scripts.** Run them from the repository root with `OMP_NUM_THREADS=1 nice -n 10`, one process each.
  - `cfg656_derive.py`: about 81 min, under 200 MB. It computes the catchments and runs CFG637's Method A derivation (`cfg637_lib`, unchanged). It writes `cfg656_derive.out`, `cfg656_derive_results.json` and `cfg656_profiles.npz`. The npz is 5.4 MB, is not committed, and the script regenerates it.
  - `cfg656_gates.py`: about 1 s. It runs CFG634's T3/T2 code from CFG634's committed source, with CFG637's single RD patch plus one T2-CEN supply hook. It writes `cfg656_gates.out` and `cfg656_gates_results.json`.
- **Data:** read from disk only; nothing was downloaded. Every number below comes from the two JSONs.
- **Correction to the brief:** the T3 "headline" is NOT R200. It is CFG634's outermost audit row, 1000 kpc for all 12 clusters (about 0.45–0.57 R200). η at R200 is reported below only as a diagnostic.

## Catchment and supply (primary rule P, per cluster)

**How the catchment is set.**
- r_ta comes from CFG654's native Δ_ta(z) at each cluster's z. The catchment is solved as a fixed point.
- Census f_ret = 0.90 for all 12 clusters.
- The measured gas is extended beyond its last data point (1.6–2.7 Mpc) with the last-3-point log-slope. This is CFG634's own rule, carried here to r_ta.

**Result.** r_ta = 4.9–12.7 R200 (9.0–25.8 Mpc). Supply relative to the old convention:

| cluster | A1644 | A1795 | A2029 | A2142 | A2255 | A2319 | A3158 | A3266 | A644 | A85 | RXC1825 | ZW1215 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r_ta / R200 | 7.44 | 5.69 | 6.79 | 7.81 | 7.72 | 12.66 | 6.66 | 6.55 | 4.87 | 6.49 | 8.98 | 4.98 |
| supply P / OLD | 7.89 | 3.15 | 5.13 | 7.08 | 7.77 | 20.50 | 4.69 | 5.66 | 1.96 | 4.30 | 11.36 | 3.34 |

**Medians over the 12 clusters, supply relative to the old convention:**

| rule | median | range |
|---|---|---|
| P | ×5.4 | ×2.0–20.5 |
| HI | ×7.0 | ×3.0–29.4 |
| LO (steepening) | ×1.6 | ×0.95–4.7 |
| FLOOR (measured gas only) | ×1.04 | ×0.71–1.29 |
| RET (SHELL placement) | ×4.6 | — |
| NAT (5.481) | ×5.5 | — |

**Reading.** Measured gas alone (FLOOR) reproduces the old convention's supply to about 4%. Every larger supply comes from gas outside the X-ray data.
- Rule P implies M_gas ∝ r^0.3–1.2 out to about 10 R200.
- At r_ta the local baryon density is then about s·Δ_ta·f_ret/3 ≈ 1–4× the cosmic mean.
- This is an extrapolation, not a measurement.

## Gates

Values are canonical / alt. Method A is primary. Reservoirs are per host, under the condensed (H-CB) source and under candidate B.

| supply | H-CB T3 headline η (1000 kpc) | H-CB inner 200–420 | B T3 headline η | B inner |
|---|---|---|---|---|
| OLD (= CFG637) | 1.494 ± 0.061 / 1.661 ± 0.080 FAIL | 0.859 / 0.889 PASS | 1.820 ± 0.067 / 1.679 ± 0.062 FAIL | 3.163 / 2.927 FAIL |
| **P (primary)** | **0.452 ± 0.324 / 0.460 ± 0.308 TENSION (overshoot)** | 0.244 / 0.247 TENSION | **1.820 / 1.679 FAIL (identical)** | 3.163 / 2.927 FAIL |
| HI | 0.397 / 0.404 TENSION | 0.204 / 0.209 | identical | identical |
| LO | 2.064 / 3.449 TENSION | 0.990 / 4.902 | identical | identical |
| FLOOR | 1.491 ± 0.061 / 1.630 ± 0.071 FAIL | 0.890 / 0.904 PASS | identical | identical |
| RET | 0.504 / 0.506 TENSION | 0.279 / 0.280 | identical | identical |
| NAT (5.481) | 0.443 / 0.439 TENSION | 0.239 / 0.239 | identical | identical |
| P, ε 0.5 / q 0.05 / q 0.2 / uniform draw | 0.740 / 0.761; 0.435 / 0.435; 0.477 / 0.478; 1.229 / 1.388 (all TENSION) | | identical | |

**Per cluster, H-CB primary at 1000 kpc** (canonical): 0.35, 0.74, 0.50, 0.35, 0.33, 0.16, 0.55, 0.41, **4.30** (A644), 0.67, 0.32, 0.93.
- A644 has the shallowest outer gas slope (0.32), so its catchment stays small and its derived reservoir is empty.
- The other 11 clusters overshoot.
- The scatter (σ ≈ 0.31–0.32) is why the frozen label is TENSION rather than FAIL.

**Diagnostic η(R200)** (reported only; M_FORW at R200 is the published reconstruction):
- H-CB: OLD 1.88 / 2.07 → P 0.60 / 0.62, FLOOR 1.77 / 1.94, LO 2.21 / 2.80.
- B: 1.40 / 1.28 in every supply variant.

**T2 groups.**
- **Primary (group rule unchanged):** H-CB +0.066 (Z 1.85) / +0.050 (Z 1.38); B +0.060 (Z 1.65) / +0.043 (Z 1.20). All CLOSE, and they equal CFG637 exactly.
- **T2-CEN (the census f_ret, 0.109–0.595, applied to groups as to X-COP):** H-CB +0.124 (Z 3.09) / +0.111 (Z 2.75); B +0.118 (Z 2.97) / +0.105 (Z 2.58). **All ABOVE (fail).**
- So one census-consistent supply rule across scales breaks the group pass. The per-scale convention problem persists from the group side.

## MUTATE and controls (4/4 + 3/3 pass)

- **M-OLD PASS.** The old convention, re-derived by this lane, reproduces CFG637's T3 η, σ and inner η to **0.0e+00** for both sources and both footings. The profiles match cfg637_profiles.npz to 0.0e+00.
- **M-HALF PASS.** With the supply ×0.5, H-CB η rises from 0.452 / 0.460 to 0.782 / 0.814. For B it is unchanged at 1.820 / 1.679: the reservoir is empty, so that cell is not applicable.
- **T2 primary = CFG637** to 0.0e+00.
- **C1:** supply = drawn + reservoir to 1.2e-15. Turned-around mass is within 0.71% of M_ta.
- **C-FP:** all fixed points converged in ≤ 29 iterations. The derivation's own r_ta is 1.02–1.05 × the catchment r_ta.

## Verdict (frozen §3) and plain reading

**Frozen labels.**
- **H-CB:** "ROBUST TO THE SUPPLY CONVENTION (T3 TENSION; inner TENSION); BRACKET-DEPENDENT (ε 0.5 and the uniform draw give SHRINKS)."
- **Candidate B:** "ROBUST TO THE SUPPLY CONVENTION (T3 FAIL; inner FAIL)."

**Disclosure on the H-CB label.** The frozen class name misdescribes the H-CB outcome. The frozen rule measures |η − 1| against CFG637's shortfall. It labels the primary ROBUST because |0.45 − 1| is larger than 0.75 × |1.49 − 1|. But the shortfall did **not** survive: it turned into a ×2 overshoot.

**What the numbers say.**
- **Candidate B: the R200 fail is truly independent of the supply.** The derived reservoir is empty for every supply up to ×29, so η does not change in any digit.
  - Each larger catchment also enlarges the retained core and r_ta, and the law's phantom of all the baryons (∝ r out to r_ta) takes it all.
  - The fail sits in the second premise: settled phantom out to r_ta.
- **H-CB: the X-COP outcome is not fixed by the data.**
  - Measured gas only (FLOOR) gives back CFG637's fail (1.49 / 1.63) and inner-band pass.
  - The record's own extrapolation (P), and every bracket that keeps the outer slope, overshoot (η 0.40–0.50; inner band 0.20–0.28, broken).
  - The steepening bracket (LO) undershoots worse (2.06 / 3.45). The reason: a larger r_ta enlarges the settled phantom (∝ r_ta) faster than the supply (∝ r_ta^s, s < 1), which empties the reservoir.
  - **No supply variant passes T3**, and no variant passes the headline and the inner band together.
- **Answer to the question.** The H-CB R200 shortfall is a convention artefact only in the sense that it is undetermined. It neither closes nor holds once the supply is taken from the measured gas. The outcome is set by gas 5–13 R200 out, which no X-ray profile measures, and by the "phantom extends to r_ta" rule.
- Making the supply census-consistent across scales (T2-CEN) breaks the groups.

**What would decide it.** Either of these:
- a measurement of baryons in the infall region out to about 5–10 R200 (SZ or X-ray stacks; not on disk, so not downloaded);
- a derivation of where the settled phantom stops in clusters (the second premise of CFG637).
