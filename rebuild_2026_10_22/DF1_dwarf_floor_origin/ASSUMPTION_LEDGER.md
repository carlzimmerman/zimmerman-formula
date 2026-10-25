# DF1_dwarf_floor_origin — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script)

Categories follow the record: RAW, SURVEY-CALIBRATION, RECORD-VALUE, PHYSICS-INPUT (fixed constants and named results),
MODELLING-CHOICE (declared here, not tuned), POST-HOC.

| id | assumption | category | source | used in |
|---|---|---|---|---|
| A1 | E, s, σ, r_h, M_V, logM★ per system and footing | RECORD-VALUE (built on RAW kinematics) | `X1_hosted_recount/x1_per_system.csv` | all |
| A2 | binary factor b (free-f ratio; median for unmatched M_V > −7.7; else 1) | SURVEY-CALIBRATION | `CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv` via X28's `load()` | g_iso |
| A3 | M★ = LVD mass at Υ_V = 2; gas not added to the M★ term of SI (field dwarfs Leo T, Phoenix etc. carry HI) | SURVEY-CALIBRATION; MODELLING-CHOICE | X1 B4 | SI's m term, T4 |
| A4 | E_pred = log₁₀(1 + g_x/g_iso): the extra adds linearly in g at r₁₂ on top of the isolated law | MODELLING-CHOICE (X24/X28's convention) | X28 | all power-law candidates |
| A5 | **cross-system self-similarity**: each dwarf's extra component has its characteristic radius ∝ r₁₂, so the in-system scaling (polytrope, cascade, infall) maps onto the cross-system exponent | MODELLING-CHOICE (the load-bearing one; disclosed) | — | S1, S2, S3 |
| A6 | polytrope mapping c_s² ≈ g r/3, ρ_x = g(2 − n)/(4πG r) ⇒ n = Γ/(2 − Γ) | PHYSICS-INPUT (hydrostatic + Poisson for a power law) | §1 | S1, T3 |
| A7 | Kolmogorov σ² ∝ (εr)^(2/3); Burgers σ² ∝ r (same form as Γ = 0) | PHYSICS-INPUT | Kolmogorov 1941; Burgers | S2 |
| A8 | secondary infall ρ ∝ r^(−9/4), M(<r) ∝ M_seed^(3/4) r^(3/4); the seed is M★ | PHYSICS-INPUT (Bertschinger 1985; Fillmore & Goldreich 1984) + MODELLING-CHOICE (seed) | — | S3 |
| A9 | IMF bound F ≤ 2 (Υ_V 4 against the adopted 2) | RECORD-VALUE | X1 B4 (range 1–4) | S4 T3 |
| A10 | local slope s from the simple ν, inverted at the system's own boost ν_i (the record's law is ν_e / AQUAL; only s is taken from ν_simple) | MODELLING-CHOICE (approximation, disclosed) | — | S4 |
| A11 | forest gate c_s ≤ 6–13 km/s at z = 2–3; the most lenient corner (13 km/s, z = 3, overdensity 10) is used | RECORD-VALUE | X22 | T3 P0 |
| A12 | Ω_m 0.3085, Ω_c/Ω_b 5.364, h 0.6856 | RECORD-VALUE | CFG682, CFG886 | T3 P0 |
| A13 | SPARC test points (30 km/s at 2 kpc; 100 km/s at 10 kpc), M = V⁴/(G a₀) | MODELLING-CHOICE | X24/X28 used similar points | T4 |
| A14 | Deep-law virial theorem (σ² = (2/9)√(G M a₀) mass-weighted, isolated, deep regime) used to drop S5/S6 | PHYSICS-INPUT (standard MOND result) | §1 | screening only |
| A15 | target numbers (X24 c₀, X28 n) known before freezing | POST-HOC | FROZEN_CRITERIA §7 | all |
| A16 | not blind: the same 82 systems that defined the description are used to grade the origins | POST-HOC | — | all; a survivor is a lead only |
