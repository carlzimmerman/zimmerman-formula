# X3_switched_stiffness: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT,
plus FITTED (κ = ½, L★), ILLUSTRATIVE (round model values, not data) and METHOD (own numerics).

## A. What the record's failure rests on (H4 "ILL-POSED")

| ingredient | class | where | used here as |
|---|---|---|---|
| v3 PN Lagrangian; dispersion ω² = ρ_τ[k²/χ − K], χ = k²/(KM_θ + γ_Lk²) + μ_K²/K | FRAMEWORK-NATIVE (H4 A1–A4, BS24 PN transcription PROVISIONAL via C4/BSK1) | `H4_v3_saddle_stability/h4_v3_saddle_stability.py` A4 block | re-executed verbatim (A0a); switched version derived (B1-S) |
| B2 slab model K = 1, M = 2, ρ̄ = −0.5, Δ = 1, γ_L = 1e-3 | METHOD / ILLUSTRATIVE (dimensionless) | H4 script `gmax` | reproduced with H4's code (A0b); same model for C0–C3 |
| region depths, x, lifetimes; bounded-branch e-folds 0.006–0.20 (median), ≤ 4.2 (deepest cells) | FRAMEWORK-NATIVE on ILLUSTRATIVE systems | H4 json `efolds`, `regions` | E1, E2 inputs; qualifier in the verdict |
| Galactic phantom at the Sun +0.045 / +0.051 M☉/pc³; screened near-zone D·P ≥ 0.045 | FRAMEWORK-NATIVE (own AQUAL solver) on an ILLUSTRATIVE MW-like disc | H4 json `C3` | reported; the region minimum is recomputed with H4's solver (D2) |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| the switched stiffness −(γ_L/2)[max(D·P, 0)]² | lane hypothesis; zero new constants (X0 MAP §1.C1) | X0_explanation_map/MAP.md |
| v3 action otherwise (β = η = γ_F = 0, ξ = 1, capped W, K(Q) dust) | FRAMEWORK-NATIVE | THEORY_V3_DRAFT §1, C4, C5, C8 |
| AQUAL μ = x/(1+x); J_x masses M_T = 1+x, M_L = (1+x)² | FRAMEWORK-NATIVE | C4 K2, C5, H4 A5 |
| C4-literal static equations (L), (P_L); scalar reduction χ = Φ + (L★²/2)∇·p | FRAMEWORK-NATIVE | C6 C1, D10 K1 |
| D10 axisymmetric solver, Jeans, statistic (`d10_solver.py`, D10 json likelihood tables) | METHOD (record code, imported read-only) | doors_push_2026_10_22/D10_native_Lstar |
| H4 AQUAL solver (`run_level`, S5a MW-like disc: 5e10 disc, R_d 2.6 kpc, h_z 0.3 kpc, 1e10 bulge) | METHOD (record code) on ILLUSTRATIVE masses | H4 script |
| a₀ footings 9.3603e-11 / 1.1312e-10 m/s² (9.36e-11 / 1.13e-10 inside reused H4 code) | FITTED (κ = ½) | doors BRIEF, D10 |
| L★ ∈ {21.7 / 22.9 (D10 floors), 24, 90} pc; D10 grid 2–500 pc | FITTED | D10, H4, P3 |
| x_e = 1.15–2.6 at the Sun | FRAMEWORK-NATIVE / SURVEY-CALIBRATION (MW field model) | C5 inputs (D7d `R2_scan`) |
| globular σ_obs, N, RV-bin radii | RAW | Baumgardt tables via D10 / CFG332 |
| L_V, r_h,l, R_GC, distances | RAW + SURVEY-CALIBRATION | D10 / CFG332 |
| Υ_V priors P1 (SPS) and P2/P3 (MF-slope) | SURVEY-CALIBRATION | D10 / CFG332 |
| binaries (f_b 0.3, DM91), per-star e_c | SURVEY-CALIBRATION | D10 / CFG334 (stored likelihood tables reused) |
| MW Hernquist M_b bracket 4e10 / 6e10 / E_hi, a_H = 3 kpc, D10's law at R_GC | SURVEY-CALIBRATION (E_lo a round bracket) | D10 / A60 / D7b |
| Galactic phantom at R_GC: spherical AQUAL phantom of that MW model | FRAMEWORK-NATIVE formula on SURVEY-CALIBRATION input | this lane (D4) |
| Sun: GM☉, Plummer a = 0.1 pc (point-like at r ≫ 0.1 pc) | RAW constant / METHOD | this lane (D2) |
| P3 E4 rows (G_hat, Z_hat), A69 strong-coupling estimate | FRAMEWORK-NATIVE record / ADOPTED method | P3 json, P3 `scales()` |
| C5 β dispersion ω² = γ_Lβk⁴/(K(2+3β)) and the window β ≲ 1e-9 (estimate) | FRAMEWORK-NATIVE record (estimate) | C5 README |
| dust offset ρ_d ≥ 0 (C2 uses 0.1, dimensionless) | ILLUSTRATIVE; v3's BS dust abundance is positive (μ_K → 0 regime, S4) | S4, H4 |
| WKB / frozen-coefficient principal-symbol analysis (B2-S); 1D slab without WKB (C) | METHOD (as H4) | — |

## C. Not used

- **LCDM-PROCESSED:** none. **STANDARD-MOND-MACHINERY:** none. QUMOND is not used, and D10's E4 bridge (ν_RAR, recipe) is
  not used.
- **LITERATURE-INPUT:** none in any check or verdict. Any analogy in the README (for example degenerate hyperbolic fluids)
  is marked as unverified reading, from memory, with no web lookup.
- No downloads, no PM simulations, no raw survey re-reduction (this is a theory-consistency lane).
