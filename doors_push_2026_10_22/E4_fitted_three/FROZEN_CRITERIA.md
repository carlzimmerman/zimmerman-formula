# E4_fitted_three — FROZEN CRITERIA (written before any script or number of this lane)

Item (wave E, open item 3): in the screened theory κ, L★ and u are fitted, not derived.
Rules: `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md` (owner's raw-data rule, binding).
κ = ½ is FITTED; Z/4π = 0.460659 is a POSTULATE (Milgrom's relation). Two footings, never pooled:
canonical a₀ = 9.3603e-11, alt a₀ = 1.1312e-10 m/s² (the record's FP0 values; "alt" is a₀ = ½c√(Gρ_crit)).
No dark-matter particle (cold energy). Never "theory closed". No knob scans: every bracket below is declared here,
two-sided, and is a propagation of a named calibration, never a fit.

Not redone (cited only): D5 (κ class no-go), D6 (u mechanism, u_gal), D7 (y_t ≡ κ relabelled), D8/D8b (σ_c, L★ = σ_c²/a₀
premise), A81 (ledger rank: γ, L★, σ_c are one scale; η free), D7d (screened Cassini, running).

## Inputs (read-only)

- κ: `campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined_results.json` (routes P1/P2/P3: log a₀,
  unique and shared error terms, levers incl. S_HF = d log a₀ / d log H₀ for Hubble-flow distances).
  Clean background: `campaign_fresh_gravity/CFG886_ratio_fret_without_planck/cfg886_results.json` T2a
  (DESI BAO + BBN D/H, flat, w = −1; h, Ω_m means and SDs; treated as uncorrelated — declared).
- L★: CFG820 cluster table (`CFG332_globulars_three_routes/cfg332_globulars_results.json`) and CFG820's estimator,
  copied (not imported) into this lane; CFG691 screening table S(s); CFG821 dSph table (`real_research/data/dsph/lvd_dwarf_mw.csv`).
- u: `campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_percluster.npz` and D6's inversion
  u_MID = (P_law − P_N)/(D − P_N) over the MID bins, copied (not imported).
- Kernel of the screened theory: the law g_N = g²/(g + a₀), i.e. ν_L(y) = (1 + √(1 + 4/y))/2.

## Part 1 — input ledger (deliverable, no pass/fail)

Every empirical input of the κ, L★ and u verdicts is classified RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION /
ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY with its source file, in the README and the results JSON.

## Part 2 — clean recomputations (classifications, frozen lines)

**κ (galaxy gas routes; the cluster channel is excluded as circular, A81 §9.4).**
- Replace Planck ρ_Λ (h 0.674, Ω_Λ 0.685) and the Hubble-flow distance scale (H₀ = 67.4) by CFG886 T2a (h, Ω_m):
  shift each route by lever_HF × log10(h′/0.674), redo CFG493's GLS with CFG493's own covariance, then
  κ_Λ = a₀/(c√(Gρ_Λ′)), ρ_Λ′ = 3H₀′²(1−Ω_m′)/(8πG); κ_crit = a₀/(c√(Gρ_crit′)). Background errors added in quadrature.
- Kernel: ratio a₀(ν_L)/a₀(ν_mono) needed to reproduce the same g_obs/g_bar at y = 0.03, 0.072 (P3 median), 0.3. Reported as a
  bound on the kernel term (CFG493 routes use ν_mono; the per-point data are not re-reduced here).
- Line: **κ ROBUST** if |κ_clean − κ_CFG493| < 0.5 σ_CFG493 on the footing in question, else **κ SHIFTS**.
- The **raw-data fitted constant is a₀ itself** (m/s², at the stated distance convention); κ is a₀ divided by a background input.
  Both are reported.

**L★ (CFG820 globulars, primary = no Pal 3).**
- R0: CFG820 as written (ν_RAR kernel + additive EFE recipe y + g_ext/a₀), fine-grid Δχ² = 3.84 root.
- N1 (native, primary): kernel ν_L, **no** EFE recipe (the action's own external-field response is not the additive recipe;
  D7 K3), everything else as CFG820. N2 (reported only): ν_L **with** the recipe (labelled STANDARD-MOND MACHINERY).
- Υ_V propagation on N1: a coherent Υ_V × 10^(±0.15) (CFG820's own 1σ width, applied coherently). Two values, no scan.
- a₀ derivative on N1: d ln L★_95 / d ln a₀ by central difference at a₀ × 1.05^(±1).
- Line: **L★ FLOOR STABLE** if |ln(L★_95,N1 / L★_95,R0)| ≤ 0.05 on both footings, else **L★ FLOOR MOVES**. Also report
  Δχ²_N1 at the thermal L★ (23.43 / 19.38 pc) and whether it is > 3.84.
- CFG821 (dSph upper bound) re-run with ν_L, isolated: reported only (CFG821 is CONDITIONAL — unscreened fit p ≈ 0 and no
  bound cold mass, which the screened theory requires for dwarfs).

**u (eRASS1 × KiDS stack, MID band).**
- Reproduce D6's u_MID (canonical 0.47157, alt 0.5234).
- Sensitivities (each a declared bracket, both footings): a₀ × 1.05^(±1) (gives d ln u / d ln a₀); eRASS1 M_gas × 1.10
  (survey calibration, gives d ln u / d ln M_gas); R500 × 10^(±0.033) at fixed M_gas (= ±0.1 dex in the ΛCDM/WL-calibrated
  M500); stellar fraction f_s ∈ {0.10, 0.30} (record 0.20, externally calibrated); background swap Planck → CFG886 T2a at
  first order (ΔΣ ∝ h, R and R500 ∝ 1/h, M_gas ∝ h^(−5/2)).
- Line: **u CLEAN** if every ΛCDM-PROCESSED bracket (R500, background) moves u_MID by < 1σ (σ = 0.0325 canonical,
  0.0360 alt); else **u CONTAMINATION-SENSITIVE**. The survey and external brackets are reported with the same yardstick.
- Report the MID band's physical radii (Mpc), and whether any r_sp / r200 / NFW quantity enters u_MID.

## Part 3 — dependency structure

- Jacobian J of three observable classes w.r.t. (ln a₀, ln L★, ln u), numerically: galaxy rotation (M_b = 1e10 M☉, r = 10 kpc,
  through CFG691's S(s)); globular σ (NGC 2419 and Pal 14, N1 model, L★ = 30 pc); cluster MID ΔΣ prediction
  D_pred = P_N + (P_law − P_N)/u. Report J, its singular values and rank (rank tolerance 1e-3 × largest).
- Measurement coupling: d ln u / d ln a₀ and d ln L★_95 / d ln a₀ from Part 2.
- The count of independent fitted constants of the screened theory, with every other input listed (Ω_c/Ω_b, η, β, Λ/ρ_Λ, H₀,
  y_t, kernel form, Υ's, MW mass).

## Part 4 — forced relations

A relation counts only if it follows from the action (THEORY P1–P3 terms) with no number inserted. For each candidate
(L★ = σ_c²/a₀; I(y_t) = 8π/κ²; u vs a₀ or L★; η = γ; the screening variable) state FORCED / POSIT / NONE and the source.
If a forced relation exists: its look-elsewhere probability and a second prediction. If none: say so.

## Checks (script `e4_fitted_three.py`, one line each, exit 0 iff all pass)

- **K1** CFG493 GLS reproduced from its JSON: |log a₀ − (−10.10732)| < 1e-4 and |σ − 0.098475| < 1e-4.
- **K2** CFG493 variant V6 (HF at H₀ 73.04) reproduced by lever arithmetic: |log a₀ − (−10.0621)| < 0.002.
- **K3** CFG820 R0 fine-grid root reproduced: 23.641 ± 0.02 pc (canonical), 24.476 ± 0.02 pc (alt) (D8 values).
- **K4** D6 u_MID reproduced: |u − 0.47157| < 1e-3 (canonical), |u − 0.5234| < 2e-3 (alt).
- **K5** the native kernel satisfies g_N = g²/(g + a₀): max relative residual < 1e-12 on y ∈ [1e-4, 1e4].
- **K6** Jacobian structural zeros: |∂/∂ln u| for galaxy and globular rows = 0 exactly; |∂/∂ln L★| for the cluster row < 1e-3.
- **MUTATE** (`--mutate`): the native kernel is replaced by ν_RAR. K5 must fail. Outputs `*_MUTATE.out`,
  `*_results_MUTATE.json`.

## Overall verdict (frozen mapping)

- **CRISP FINDING** if any of: κ SHIFTS, L★ FLOOR MOVES, u CONTAMINATION-SENSITIVE, a forced relation found, or an error in
  the record (file:line).
- **SCOPED NO-GO** if none of those and Part 4 finds no forced relation (the three stay independent fitted inputs).
- Compute: `OMP_NUM_THREADS=1 nice -n 10`, single thread, < 2 GB, minutes. No network, no downloads.
