# X15_c1_preferred_frame: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½, L★), ILLUSTRATIVE (round model values, not data), ADOPTED (a posed choice, not derived) and METHOD.

## A. What the question rests on (the record)

| ingredient | class | where | used here as |
|---|---|---|---|
| v3s action: gravity [R3 + K_ijK^ij − K²]/(4K), clock term P^iD_i ln N, W(u), switched stiffness, K(Q) | FRAMEWORK-NATIVE (J_x, stiffness POSTULATED; K(Q) from BS24, LITERATURE-INPUT) | THEORY_V3_DRAFT §0–1; V3_FULL_PICTURE §1; A22 D1 (ADM form) | the theory under test |
| C1 operator −βK²/(4K) (Hořava λ = 1 + β), PN coefficient B = βc²/(2 + 3β), window β ∈ [2.0e-6 / 2.2e-6, 1.0e-5] (μ_K 0.1), ≤ 1.1e-4 (μ_K 0.03) | FRAMEWORK-NATIVE record (X14 SYMPY/NUM; the window's upper edge rests on C5's IR-band estimate) | X14 README, JSON `classes.C1.FT_window` | the completion under test; S0-2 |
| A22: α₁ = α₂ = 0 at PPN order; hedgehog Φ = Ψ = −GM/r + (GM/L★²)r; u/a₀ = 2.6e-6 in the Solar System; ψ = D·P = M/(2πL★²r) > 0 | FRAMEWORK-NATIVE record (SYMPY, `a22_checks.py` 13/13) | `deepseek_push/DS_FINAL_2026_10_21/A22_ppn_frames/` | S0-1, S0-5; screened-branch premises (M = 1, Θ = 1) |
| C8 K8: P-sector leaf-tilt anisotropy (r/L★)², α₂-equivalent 4.1e-14 at 1 AU | FRAMEWORK-NATIVE record (NUM) | `covariant_push_2026_10_22/C8_instantaneous/README.md` | comparison of residual sizes (reported) |
| X3/X14 linear khronon system and its dispersion (ρ_τ + Bk²/K)(k²/χ − K) | FRAMEWORK-NATIVE (SYMPY record) | X14 `disp`, X3 B1-S | S0-3 target |
| X3's PN Lagrangian L1 (Ξ = φ − σ̇ + \|∇σ\|²/2, hold law, continuity of ρ_τ) | FRAMEWORK-NATIVE (SYMPY record) | X3 / X14 R1 | 3b steady equation (3D form) |
| X14's `aqual_point` (spherical AQUAL field and phantom of a point mass), MW-mass 6e10 M☉, fold radii, c_A at β_max | FRAMEWORK-NATIVE (spherical AQUAL is algebraic) + ILLUSTRATIVE masses (as X8/X10) | X14 script L431–435, JSON | S0-2, step 3 |
| μ_K ≤ 0.1 Mpc⁻¹ (S4 guard), 0.03 Mpc⁻¹ (galaxies-survive edge) | FRAMEWORK-NATIVE record (S4) | S4 README via X14 | window edges |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| a₀ = 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | doors BRIEF |
| L★ = 21.682 / 22.849 pc (switched D10 floor); γ_L = K L★²/2 | FITTED | X3 D4 via X14 |
| native H₀ = 67.2 km/s/Mpc (conservative lower end) | FRAMEWORK-NATIVE | BRIEF (C2, A78), as X14 |
| linearisation about Minkowski + khronon at rest + P = 0, quadratic action of §1 | METHOD (ADOPTED): valid while u ≪ a₀ (M = 1), D·P > 0 (Θ = 1) and C1 dominates the khronon's charge transport (P-LIN) | FROZEN §1 |
| √h N R3 to quadratic order for h = (1 − 2ψ)δ: 2\|∇ψ\|² − 4∇n·∇ψ; K_ij = −ψ̇δ_ij − ∂_(iN_j) | METHOD (standard ADM algebra, re-derived in the script where checked by S0-4/S0-5) | — |
| point-particle matter action −M∫dτ expanded to linear order in the fields | METHOD | — |
| PPN metric form in the preferred frame with ζ_i = ξ = α₃ = 0 (g_0i = −½(7+α₁−α₂)V_i − ½(1+α₂)W_i; no 𝒜 term in g_00) | LITERATURE-INPUT [mem], validated by the GR control S0-4 | LITERATURE_MAP L2 |
| BPS 2011 Eq. 91 khronometric α₁, α₂ (leading order) | LITERATURE-INPUT, PROVISIONAL (summarising web fetch) | LITERATURE_MAP L1 |
| Einstein-aether c₁₃ = 0 α₂ formula (Oost, Mukohyama & Wang 2018) | LITERATURE-INPUT (record transcription [FT]) | DOOR11 §1 |
| bounds \|α₁\| < 1e-4, \|α₂\| < 2.4e-7, \|α̂₁\| < 2.1e-5, \|α̂₂\| < 1.6e-9 (CMB frame, w ≈ 369 km/s) | LITERATURE-INPUT (record transcription; Nordtvedt 1987 secondary) | DOOR11 §1 |
| test radii: 1 AU, 30 AU, Earth–Moon 3.844e8 m, NS radius 1.2e4 m, J1738+0333 separation 1.73e9 m | RAW constants / ILLUSTRATIVE (C8 table for the binary, C8 for the NS radius) | C8 README |
| Galactic phantom density near the Sun ≤ 1e-21 kg/m³ (only for P-LIN's margin) | ILLUSTRATIVE upper value | — |
| step-3 speeds 70, 220, 369, 600, 1000 km/s; held-halo radius R_h ∈ {1, 10} Mpc; cluster 1e14 M☉ at 300 kpc; lnΛ = ln 100 | ILLUSTRATIVE | FROZEN §6 |
| supersonic dynamical-friction drag 4π(GM)²ρ lnΛ/w² | LITERATURE-INPUT [mem], ESTIMATE | LITERATURE_MAP L4 |
| ρ_crit = 3H₀²/(8πG) at H₀ = 67.2 as an upper bound on the cosmic khronon dust density | FRAMEWORK-NATIVE H₀; bound ADOPTED (the dust abundance is FITTED and ≤ ρ_crit) | — |
| G, c, M☉, M⊕, AU, pc | RAW constants | CODATA / IAU values in the script |

## C. Not used

- No survey data, no SURVEY-CALIBRATION, no LCDM-PROCESSED input. No data comparison other than the published PPN bounds.
- No STANDARD-MOND-MACHINERY: no QUMOND, no EFE formula. The a₀-line law and the AQUAL phantom are the theory's own static
  limit.
- No new fitted constant, no knob scan (β is scanned only across X14's frozen window to test the bounds), no simulation, no
  downloads; `compute_queue/` and other lanes untouched (A22's script is executed read-only with its output redirected into
  this lane).
