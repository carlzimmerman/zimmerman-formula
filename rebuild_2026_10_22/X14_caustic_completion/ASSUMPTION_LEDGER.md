# X14_caustic_completion: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or derivation result)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / LCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT, plus
FITTED (κ = ½, L★), ILLUSTRATIVE (round model values, not data), ADOPTED (a posed choice, not derived) and METHOD.

## A. What the question rests on (the record)

| ingredient | class | where | used here as |
|---|---|---|---|
| v3s action; switched stiffness; J_x (μ = x/(1+x)); K(Q) = μ_K²(Q − 1)² | FRAMEWORK-NATIVE (J_x and the stiffness POSTULATED; K(Q) form from BS24, LITERATURE-INPUT) | V3_FULL_PICTURE §1; X3 | the theory under test |
| PN khronon system: Ξ = φ − σ̇ + \|∇σ\|²/2, hold law, Poisson, D_t v = −∇φ + ∇Ξ | FRAMEWORK-NATIVE (BS24 PN transcription PROVISIONAL, re-derived in C4 K1) | V3_FULL_PICTURE §2 | F1–F4 |
| X3's 1D PN Lagrangian `L1` and its B2-S identities (continuity, P-equation, Bernoulli) | FRAMEWORK-NATIVE (SYMPY record) | `X3_switched_stiffness/x3_switched_stiffness.py` lines ~795–835 | F1, R1 |
| X3's linear system `disp_switched` (H4's A4 system with Θγ_L) and its B1-S result | FRAMEWORK-NATIVE (SYMPY record) | same file, lines ~747–778 | R0; P3 base, copied with provenance |
| khronon at Q = 1 is mimetic (geodesic) dust; coupling α ≡ 1 | FRAMEWORK-NATIVE (SYMPY, X6 X-D1, X-D2) | `X6_dust_coupling/README.md` | the zero-charge limit of F2 |
| v3's constraint algebra: 3 DOF | FRAMEWORK-NATIVE (review, SYMPY) | `reviews/v3_constraint_algebra_2026_10_23/` | P4 target |
| C5's DOF table (β > 0, η = 0: 3) and IR band ω² = −βk²/(2 + 3β) for aH ≪ k ≪ μ_K; c_s² = (Q̄ − 1)/Q̄ | FRAMEWORK-NATIVE (SYMPY record) | `covariant_push_2026_10_22/C5_health/README.md` | P4, P6(c) for C1; C3 |
| X3 E2's β-dispersion form B = βc²/(2 + 3β) (C5 × H4 superposition, an ESTIMATE in X3) | FRAMEWORK-NATIVE record (estimate) | X3 README §4 E2; `gmax_beta` | C1's PN coefficient |
| X8/X10 fold facts: relative speeds, fold locations 11–33 kpc (X8 h 5) and 73–156 kpc, 76–91 kpc behind MW (X10) | FRAMEWORK-NATIVE record (NUM) | X8, X10 READMEs | the regime points of FT and F5 |
| μ_K ≤ 0.1 Mpc⁻¹ (isolated-galaxy guard, both footings); 0.03 Mpc⁻¹ galaxies-survive edge | FRAMEWORK-NATIVE record (S4, from lensing data through S4's pipeline) | `S4_v3_muK_clusters/README.md` | F5(d), P6(c) |
| BS cap μ_K ≤ 10 Mpc⁻¹ (14.8 h/Mpc) | LITERATURE-INPUT (BS24 Eq. 39, via S4) | S4 README | F5(d) |
| BS25 DBI K = (2μ²/λ_D)[1 − √(1 − λ_D(Q − 1)²)], published sets P1, P2 | LITERATURE-INPUT (via Q7, WebFetch PROVISIONAL) | `Q7_bs25_cosmology/README.md` | C4 |
| O1's candidates c and e (K6 no merging, K11 caustic) | FRAMEWORK-NATIVE record | `O1_ownership_action/README.md` | C8 |
| AeST + γ_L (v4) health (C5) | FRAMEWORK-NATIVE record | C5 README | C7 |

## B. This lane's ingredients

| ingredient | class | source |
|---|---|---|
| a₀ = 9.3603e-11 / 1.1312e-10 m/s² | FITTED (κ = ½) | doors BRIEF |
| L★ = 21.682 / 22.849 pc (switched D10 floor), γ_L = K L★²/2 | FITTED | X3 D4 |
| native H₀ = 67.2–68.6 km/s/Mpc (67.2 used, conservative) | FRAMEWORK-NATIVE | BRIEF (C2, A78) |
| MW-mass 6e10 M☉ as a point mass | LITERATURE-INPUT, ILLUSTRATIVE (as X8, X10) | X8 ledger |
| w ∈ {68.75, 74.8} km/s | ILLUSTRATIVE (X10's O2 and O1 t_i 3 MW speeds) | X10 FROZEN |
| fold locations r ∈ {11, 33, 73, 91, 156} kpc | record values (X8 h 5 events 11–33 kpc; X10 events 73–156 kpc, wake 76–91 kpc) | X8, X10 READMEs |
| spherical AQUAL field of a point mass, g μ(g/a₀) = GM/r², and its phantom ρ_ph | FRAMEWORK-NATIVE (v3s's static limit; spherical AQUAL is algebraic) | V3_FULL_PICTURE §2 |
| M_θ bracket [1 + x, (1 + x)²] | FRAMEWORK-NATIVE (H4) | V3_FULL_PICTURE §2 |
| completion classes C1–C9, their mechanisms and costs | LITERATURE-INPUT (PROVISIONAL web look-ups) | `LITERATURE_MAP.md` |
| C1's PN representative −(B/(2K))(∇²σ)² (from −βK², K ≈ ∇²σ/c) | ADOPTED (PN reduction; checked against the record form X3 E2) | FROZEN §2 |
| C2's representative ∇²φ − sℓ_*²∇⁴φ = Kρ | ADOPTED (minimal PN image of a z ≥ 2 curvature potential) | FROZEN §2 |
| C5's quantum potential Q_ν = −(ν²/2)∇²√ρ/√ρ | LITERATURE-INPUT (Madelung form; BR17, Widrow & Kaiser 1993) | LITERATURE_MAP |
| Lax's blow-up theorem for genuinely nonlinear fields (shock after a fold is caught by pressure) | LITERATURE-INPUT (PROVISIONAL, secondary sources) | LITERATURE_MAP A11 |
| G, c, M☉, kpc, Mpc | RAW constants | CODATA / IAU values in the script |

## C. Not used

- **RAW survey data, SURVEY-CALIBRATION:** none. No data comparison is made.
- **LCDM-PROCESSED:** none.
- **STANDARD-MOND-MACHINERY:** none. No QUMOND and no EFE formula. The spherical point-mass field is AQUAL's own algebraic
  solution (in spherical symmetry AQUAL and QUMOND coincide, but QUMOND is not used).
- No new fitted constant, no knob scan, no simulation, no downloads; the heavy queue and other lanes are not touched.
