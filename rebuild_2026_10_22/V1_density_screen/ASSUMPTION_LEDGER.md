# V1_density_screen — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNAL / ILLUSTRATIVE /
POSTULATED (new in this lane).

## A. The theory and the screen

| ingredient | class | source | used as |
|---|---|---|---|
| v3 action (Khronon τ, covector P, J_x so the static limit is AQUAL μ = x/(1+x), β = η = γ_F = 0, BS K(Q) dust) | FRAMEWORK-NATIVE | THEORY_V3_DRAFT §1; C4, C5 | the base theory, γ_L removed |
| BS24 PN system (Ξ = φ − σ̇ + ∣∇σ∣²/2, khronon continuity) | EXTERNAL (transcribed, re-derived in H4 A1) | H4 A1, BSK1 | the PN Lagrangian of Part A |
| s(ψ) = ψ² multiplying the P sector | POSTULATED (this lane's choice) | FROZEN_CRITERIA §1 | the one insertion point |
| symmetron potential (μ_ψ²/2)(ψ²−1)², conformal matter coupling A = 1 + v²ψ²/(2M²) | POSTULATED (standard symmetron form, Hinterbichler–Khoury 2010) | — | the screening dynamics |
| ρ_* = μ_ψ²M² | FITTED (the one allowed constant, swapped for L★) | Part C | — |
| λ_C = 1/μ_ψ, v²/M² | extra constants: must decouple or be tied (Part I) | — | regime boundary; fifth force / back-reaction |
| coupling to the matter trace only (not to the BS dust, not to ρ_τ) | POSTULATED | §1 | keying on "density"; coupling to ρ_τ would key the screen on the MOND sector itself (circular, and anti-screens where ρ_τ < 0) |
| alternative insertion a₀ → s·a₀ | not tested numerically | — | Part B results are insertion-independent (they concern ψ only); Parts C–H numbers would shift |

## B. Data and record inputs (all read-only)

| input | class | source |
|---|---|---|
| globular σ_obs, e_c, N, L_V, r_h,l, R_GC; likelihood tables (binaries f_b 0.3); Υ_V priors P1/P2/P3 | RAW + SURVEY-CALIBRATION (as D10's ledger) | `doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar_results.json`; CFG332 json |
| MW field at the clusters: Hernquist M_b 4e10 / 6e10 / E_hi, a = 3 kpc, with the law (F-D10) or with μ_S (F-S) | SURVEY-CALIBRATION (D10) + FRAMEWORK-NATIVE | D10 |
| D10 solver (Solver2D, Jeans, Plummer) | FRAMEWORK-NATIVE record code | `d10_solver.py` (imported, not edited) |
| Cassini Q₂ machinery (Route N), fields E0–E3, Hees/Park bands, planet bounds, BN11 anchor | FRAMEWORK-NATIVE code + SURVEY-CALIBRATION (fields) + RAW (ephemeris bounds as published) | D7d solver + D7b json; D7d inputs |
| E2 AQUAL Q₂ (R1) and γ_v at 20 kAU (R2) | FRAMEWORK-NATIVE record | E2 json |
| DR4 registered readings (Arm A floor 1.1614 / 1.1917; medium-first 1.000; PREREG g_ext) | FRAMEWORK-NATIVE record (frozen, read only) | `prep_2026/gaia_dr4_prep/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md` |
| satellites: per-system log(g_obs/g_bar), y, x_e (E_mid), d_host, v3 Δ | RAW (LVD kinematics) + SURVEY-CALIBRATION (Υ_V = 2, distances, host masses) | S1 `s1_per_system.csv` |
| SPARC rotmod files + Lelli 2016 table | RAW + SURVEY-CALIBRATION (SPS Υ grid, distances, inclinations) | `real_research/data/sparc_data/`, `SPARC_Lelli2016c.mrt` (P4's loader, re-implemented) |
| P4 axisymmetric AQUAL solver; McMillan17 MW baryons; Bovy & Rix K_z; Eilers v_c | FRAMEWORK-NATIVE code + SURVEY-CALIBRATION | P4 solver (imported), P4 T4 constants; `real_research/data/mw_*.tsv` |
| H4 region medians (|ρ_τ|, x, T) | FRAMEWORK-NATIVE record (ILLUSTRATIVE inputs per H4) | H4 json |
| F1 Newtonian-baryon cluster A_MID 9.82 ± 0.63 | RAW (KiDS × eRASS1) + SURVEY-CALIBRATION | F1 json (read only, only if the ICM is screened) |
| Sun: GM☉, R☉ = 6.957e8 m (surface potential, reference star for the Regime A/B boundary) | EXTERNAL (IAU nominal) | constants |

## C. Premises the verdict may rest on (stated so they can be attacked)

- **P-mono:** in the regime where stars are thin-shell screened (Regime B), the only matter ψ sees in a galaxy's halo is
  diffuse gas; its density does not rise outward between the satellites (20–104 kpc) and the outer globulars
  (68.6–104 kpc), and the Sun's local ISM is denser than the halo gas at 100 kpc. EXTERNAL physical premise (no
  circumgalactic density is on disk); the lane reports which results depend on it.
- **P-lin:** the Regime A potential inequality uses linear theory with the Yukawa factor dropped — both choices
  over-estimate screening, so a FAIL under them is robust; a PASS would need the nonlinear solve.
- **P-star:** the Sun's surface potential GM☉/R☉ represents the stars that carry a cluster's or a disc's mass (main-sequence
  stars have GM/R within a factor ~1.5 of the Sun's; giants are a small mass fraction).
- **P-uniform:** in Parts C–G a system sits in a uniform screening level s over its own extent (the screened region is
  larger than the system), except R-G3 (thin slab).

No ΛCDM-processed input and no standard-MOND machinery carries a verdict: the field equation is v3's AQUAL (or μ_S), no
QUMOND, no EFE recipe (fields solved as boundary conditions as in D10/S1/P4), no halo model.
