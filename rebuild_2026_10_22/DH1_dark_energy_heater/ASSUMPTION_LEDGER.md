# DH1_dark_energy_heater: assumption ledger (committed with the frozen criteria, before any script or number)

## 1. Physical assumptions

| id | assumption | why / direction |
|---|---|---|
| A1 | The cold sector is collisionless (R6). Its fine-grained state at z ≳ 2 is single-stream (cold, R2). | the spec; a fluid fails the Bullet (X23, X32) |
| A2 | Dark-energy quantities are spatially homogeneous: Λ exactly; a dynamical DE φ(t) up to perturbations sourced by matter, which act like a rescaled gravity (∝ ∇Φ). | standard; any matter-sourced δφ is a gravitational-type force and is counted with Φ |
| A3 | Peculiar velocities of a free collisionless medium redshift as 1/a (σ² ∝ a⁻² with no source). | Liouville in comoving momentum; MUTATE m1 changes it |
| A4 | Background matter dilutes as a⁻³; f = ρ_DE/ρ_m = (Ω_Λ/Ω_m) a³ for Λ. | MUTATE m2 changes it |
| A5 | "No fitted knob": a coefficient, exponent, threshold, length or velocity not fixed by the action counts as a knob. κ = ½ is the record's one fitted constant and is not a new knob. | owner rule |
| A6 | The heater acts after z ≈ 2; R1 (CMB) is untouched by any candidate that is off before z = 3. | spec |
| A7 | Wave medium (H5): dispersion ω = D k² (D plays ħ/2m; classical constant). Its forest sound speed at k is D k. Driving at rate Γ excites modes with D k² ≲ Γ; faster modes are adiabatic (exponentially suppressed). | standard adiabatic theorem; taken generously (comoving k, Γ = 3H₀ = max of d ln f/dt) |
| A8 | G4 uses medians (SPARC σ 70.5, KT σ 517.1 km/s) as X26 does for its energy table. | per-system grading is X26's machinery, cited not rerun |
| A9 | H6's quadrature model σ² = σ_well² + v_k² is graded only through G1/G3 and its window (D7); X29's C₀ bound is X26-family-based and is used as an approximate cosmic line, disclosed. | approximation, reported |

## 2. Inputs (read-only; SHA-256 recorded by the script)

| input | used for |
|---|---|
| `X22_cosmic_dust_window/x22_cosmic_dust_window_results.json` | c_s,need; p = 2 / 3 rows (cs_z3, cs_z2, forest class); α_NF k_hm |
| `X26_cold_sector_map/x26_cold_sector_map_results.json` + `.out` lines for σ medians | KT and SPARC c_s ranges, σ medians, virial r = 1 line |
| `X29_late_power_shear/x29_late_power_shear_results.json` | survivor C₀ maximum |
| `X35_a0_tracks_ede/x35_results.json` | CFG689 sqrtX(z* = 2.33) read-back |
| `X30_sheet_cluster_profile`, `X32_bullet_cold_sector` READMEs | inherited classes (quoted, not rerun) |

PROVISIONAL constants (from memory, used only for reported trigger epochs D6, not for any gate): Ω_m = 0.315, Ω_Λ = 0.685.
H₀ cancels in D5 (k in h/Mpc, H₀ = 100 h km/s/Mpc).

## 3. Record check (grep of the repo and `campaign_fresh_gravity/LEDGER.md`, 2026-10-25)

- "anti-friction": only CFG958 A1 (an exchange-rate tooth for a vacuum deposit; not a heating law).
- "Amendola / coupled quintessence": literature mentions only; no lane grades a DE-keyed velocity drive.
- "Liouville": CFG842 (capture ceiling), G2, PH1 (D5: normal → condensed impossible), sol61 kinetic_support (support does
  not choose a mass). None states that a homogeneous drive cannot heat a cold sheet.
- "parametric resonance": sol61 stochastic source (inflationary seeding), real_research pump hunt; none at DE rates.
- "deceleration / acceleration onset" and "phase change": no heating-trigger lane; PH1 is a two-phase condensate
  (no-go on its own grounds).
- "ρ_DE/ρ_m" as a key: no hits.
- Heating lanes in LEDGER: CFG643, CFG741, CFG742, CFG958; X22–X35 in rebuild_2026_10_22. Closed forms listed in the
  criteria §1.

## 4. What is not assumed

- No new data, no download, no fit, no scan. No N-body. Nothing about the dwarf floor c₀ (separate lane).
- The obstruction, if found, is for DE-keyed, knob-free, collisionless heating. It says nothing about a heater with a new
  constant or a collisional channel.
