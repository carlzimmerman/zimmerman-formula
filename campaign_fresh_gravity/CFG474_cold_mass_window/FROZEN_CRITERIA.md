# CFG474: what can the cold mass be? Combine the UFD cold-dominance (CFG440 s03), the failed soliton reading (CFG440 s02), the UFD heating bound (Dalal & Kravtsov 2022) and the superradiance windows (CFG367/394/444). FROZEN before any script exists

Owner chat 10-07 ("see if the council can figure out the cold mass"). κ = ½ fitted; both footings. No DM particle *species is added by hand*: the cold fluid is the record's wave field (FL1). This lane only bounds its mass. The amount (Ω_c/Ω_b = 5.36) stays required and underived.

**Step 1 (computed): is the UFDs' dynamics dominated by the cold fluid?**
- Per resolved MW UFD (the AUDIT_UFD sample, 31): f_cold = (M_dyn − M_law)/M_dyn inside r_½ = (4/3) R_e. M_dyn = 3σ²r_½/G; M_law is the isolated law on the stars (the AUDIT_UFD estimator, Υ_V = 2).
- Report the median and the fraction with f_cold ≥ 0.5, and Segue 1 explicitly (the bound's anchor; Segue 2 has only an upper-limit σ in the LVD and is reported as such).
- **COLD-DOMINATED** if the median f_cold ≥ 0.6 and Segue 1's f_cold ≥ 0.8, on both footings.

**Step 2 (logic, conditional).** Dalal & Kravtsov 2022 (arXiv 2203.05750, abstract read 10-06): a wave field that dominates a UFD as a *virialized, granular* halo heats its stars; m > 3e-19 eV at 99% (Segue 1/2). The record's ground-state escape is closed by CFG440 s02 (soliton scaling rejected, 6.23). So if Step 1 passes, the bound applies to the cold fluid, conditional on:
- (c1) the fluid in UFDs is the same field that is the cosmological cold component;
- (c2) the UFD fluid is virialized/granular, not a coherent ground state (supported by CFG440 s02);
- (c3) the published bound itself (not re-derived here).

**Step 3 (interval arithmetic, computed).** Intersect m > 3e-19 eV with CFG367's committed surviving intervals (read from its results JSON, not retyped) and note CFG394's indicative re-measurement caveat. Output: the surviving mass windows, each with its de Broglie length at σ = 10 km/s and 200 km/s.

**Step 4 (reported).** For each surviving window, does the field behave as CDM on the scales the record tests (λ_dB at 200 km/s ≪ 1 kpc)? Relate this to CFG440 s05 / CFG443 (cluster excess NFW-like; collisionless-like halos).

**Controls.**
- K1: Step 1 reproduces CFG440 s03's per-object M_dyn and M_law for Segue 1 (2.86e5 / 1.15e4 M☉ canonical) to 1%.
- K2: the CFG367 interval file is read and its light end equals 2.0–4.4e-20 eV.

**MUTATE.** M_law ×20 (as if the law alone carried the UFD mass). Step 1 must then return NOT COLD-DOMINATED (exit 1 when detected).
