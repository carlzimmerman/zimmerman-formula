# CR1_carrier_requirements: what could the cold fluid be?

**Read with CR2_core_scale_origin, which corrects the S(M) reading below.**

**Verdict: no candidate SURVIVES. No listed class meets both R5 (stream crossing) and R6 (core scaling).** Desk grade of classes: no action written, no grader
or zoom run, no v3s lane opened. Most rows read existing verdicts (disclosed in `FROZEN_CRITERIA.md`). κ = ½ FITTED. Not "theory closed". Clusters and the CMB
still need the mass; what is dropped is the particle. Literature values PROVISIONAL. Numbers: `cr1_grade.py`, `cr1_results.json`.

| candidate | R1 isocurv. | R2 stable | R3 abundance | R4 spread | R5 crossing | R6 S(M) | R7 no species | fails |
|---|---|---|---|---|---|---|---|---|
| A X1 spectator | FAIL 2e8–6e8 | absorbed unless inert | FREE | pass | not tested | none | pass | R1 R2 R3 R6 |
| B QC1 condensate | pass | FAIL Γ/H 1e19 | FAIL (B-even) | FAIL 1e-8 | not tested | none | pass | R2 R3 R4 R6 |
| C shift charge, free I₀ | FAIL: not locked; pre-inflation charge × 7e-79 | pass | FREE (F49) | pass | FAIL L374 | none | pass | R1 R3 R5 R6 |
| **D C, locked to baryons** | pass* | pass | LOCKED | pass | FAIL L374 | none | pass | **R5 R6** |
| E wave field, free | FAIL: not locked | pass | FREE | pass | pass | FAIL exponent 1 | FAIL | R1 R3 R6 R7 |
| **F wave, locked** | pass* | pass | LOCKED | pass | pass | FAIL exponent 1 | FAIL | **R6 R7** |
| **G repulsive wave, locked** | pass* | pass | LOCKED | pass | pass (L374's GP) | FAIL exponent 2/3 | FAIL | **R6 R7** |
| H particles (control) | depends | depends | depends | pass | pass | FAIL cusps (X81) | FAIL | R6 R7 |
| I D plus C1 | pass* | pass | LOCKED | pass | CONDITIONAL: C1 cures health, needs a new constant, makes small-scale growth overshoot (X14, X17) | FAIL: C1's static lensing effect is exactly 0 | pass | **R6**, R5 open |

*Conditional: a sharing era is assumed, with no action written.

## What the numbers say
1. **Target for core scaling (new).** ET1's table fits S ∝ M^(0.238 ± 0.034), χ² 5.3 for 4 dof. Wave: exponent 1, χ² 509, z +22. Thermal-core: 2/3, χ² 165, z +12.6. Flat floor: 0, χ² 54.5, z −7.0.
   Reported only: 1/3, χ² 13.1, z +2.8. **Corrected by CR2: 1/3 is not Σ_coll's scaling; Σ_coll runs M^0.24, so this slope is collapse scaling.** Errors cover sample scatter only, and M200 comes from the fitted EM1 relation.
2. **Wave field.** Matching S 150 at lg M 11.76 needs m = 5.6e-24 eV, 3.6e4–8.9e4 × below the record's floor of 2–5e-19 eV (F50, L383). That match gives S 2.4 against the 68.6 needed at lg M 9.97. At the floor, S ≈ 9e6 M☉/pc² with r_c 0.08 pc at 1e12: a tiny soliton, not this core.
3. **Thermal core.** Fixed R_TF, while r₀ ~ M/(R₂₀₀S) varies × 8.5 across ET1's masses.
4. **Baryon locking (rows D, F, G: the one gain).** If shift charge shares with baryon number at a B-violating era, then n_c = q n_b. That removes isocurvature, fixes the sign and is exact afterwards. A pure-gradient coupling to a conserved current is removable, so it adds no force once B is conserved.
   The dust branch holds below T = 3.1 TeV (0.72–13 TeV for M × ⅓–3), above sphaleron freeze-out near 130 GeV, so a window exists. Today ρ_c/M⁴ = 1.6e-50.
   **The price:** m_eff = R m_p/q = 4.95 GeV/q (4.74–5.15 at q = 1, R's 1σ). That swaps free I₀ for free m_eff/q. Why Ω_c/Ω_b ≈ 5 is relabelled, not explained. For wave rows, q ≈ 1e28 per baryon at the floor.
5. **A consequence for route E.** Native η comes from collisionless zooms, which assume multi-stream flow. A carrier without multi-stream (C, D, I) is not what those zooms simulate, so route E's collapse rule would not be native to it. The carriers that do cross streams (E–H) are the ones with quanta.

## Where it lands
X1's isocurvature failure has a class-level way out (LOCKED), conditional on an unwritten action, and it is not a derivation. The hard wall is R5 with R7, plus core form: nothing listed crosses streams without new quanta and also makes a core. **Corrected by CR2:** the exponent is what collapse gives, so it does not filter carriers that collapse like dust. Ask new proposals for core form and for crossing streams without quanta. CR1 also omitted self-coupling; CR2 grades it.
