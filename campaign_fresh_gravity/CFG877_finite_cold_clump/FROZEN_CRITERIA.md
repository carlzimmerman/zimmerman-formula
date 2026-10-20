# CFG877 — FROZEN CRITERIA: does a FINITE cold clump (no new parameter) fit every dwarf sample at once?

Frozen before any script (owner block 870–879). κ = ½ fitted; not theory closed.

## Why, and the post-hoc label
CFG876: the extended cored component (mass ∝ r) is BROKEN by large out-of-sample dwarfs, while compact ones fit. The record
already holds the finite form: CFG871's self-gravitating deep-regime cold clump of total mass M_cl = 81σ⁴/(4 G a0).
**Post-hoc:** this test is chosen because CFG876 failed, and CFG876's 33 out-of-sample dwarfs are now seen. Every number in the
model is fixed by earlier lanes, so nothing is tuned here. It also must not break the samples CFG870 passed.

## Model (all numbers fixed beforehand)
- σ = V_x/√2 with V_x from cfg870_results.json (10.6547 canonical / 10.5870 alt); r_c = 104 pc (CFG870).
- M_cl = 81 σ⁴ / (4 G a0) (CFG871's relation, per footing).
- Clump mass inside r: M_x(<r) = min[ V_x² r³ / (G (r² + r_c²)), M_cl ] (CFG870's shape, capped at the clump's total mass).
- σ_pred² = σ_law² + G M_x(<r12) / (3 r12) (Wolf), with σ_law exactly as in the lane whose sample is scored.

## Samples and inputs (each scored exactly as in its source lane)
1. **MW classical (CFG870's calibration set):** CFG828 rows, host MW, Δ > 0.05; CFG824 σ, CFG827 Υ_SFH, no gas.
2. **M31 + field (CFG870 T2):** same inputs.
3. **Literature-σ UFDs (CFG870 T3):** CFG859's list, LVD σ, Υ = 2.20.
4. **Large out-of-sample (CFG876 B, 18):** LVD σ, Υ_V = 2, gas counted. Individual failures z ≤ −3 at Υ_V = 1 as in CFG876.
5. **Small out-of-sample (CFG876, 15):** same inputs.
6. **SPARC small rotating dwarfs (CFG870 T1):** D = median per galaxy of log10(g_obs/g_law) − log10((g_law + g_x)/g_law), g_x from M_x.

E = mean ln(σ_obs/σ_pred) per dwarf group, se_E = bootstrap (4000, seed 877).

## Classes (canonical primary; the alternative footing must agree, else the weaker class)
- **FINITE CLUMP HOLDS:** every dwarf group |E|/se_E < 2; large group N_fail < 2; SPARC |D| < 0.05 and |D| ≤ 2 se_D.
- **FAILS-UNDER:** any dwarf group E/se_E ≥ +3 (the clump is too small somewhere).
- **FAILS-OVER:** any dwarf group E/se_E ≤ −3, or large-group N_fail ≥ 2, or SPARC D ≤ −0.05.
- **PARTIAL:** anything else (tensions between 2 and 3 se), with the tense groups named.

## Controls
- **K1:** with M_cl → ∞ the script reproduces CFG870's T2 E and CFG876's primary E (canonical) to < 1e-9.
- **MUTATE** (`CFG877_MUTATE=inf|tenth`): M_cl → ∞ must give FAILS-OVER (CFG876's result); M_cl × 0.1 must not give
  FINITE CLUMP HOLDS.

## Disclosed limits
No EFE or tides (Crater II and Cassiopeia III already exceed the law alone, so they may fail regardless). CFG872 found that
a self-consistent clump cannot supply 6/25 extreme compact dwarfs; this model fixes one clump for all, so per-dwarf scatter
(0.52 dex in CFG872) is not modelled.
