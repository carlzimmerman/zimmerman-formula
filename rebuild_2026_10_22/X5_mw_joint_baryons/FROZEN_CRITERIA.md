# X5_mw_joint_baryons FROZEN CRITERIA: can published Milky Way baryons pass K_z and v_c(R0) together under v3's AQUAL? Does S3's slope verdict survive CFG532's S2 errors?

Written 2026-10-23 and committed alone (with `ASSUMPTION_LEDGER.md`), before any script of this lane exists and before any
number of this lane is computed. Lane from `rebuild_2026_10_22/X0_explanation_map/MAP.md` §1.E items 1-2 and §3 ("P4's
'every baryon model fails' is robust to screening, EFE and footing, not to the baryon model"; "S3's ROBUST means robust to
v3's ingredients, not to rotation-curve systematics"). Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`.

κ = ½ is FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², computed and reported separately, never
pooled. No dark-matter particle. Never "theory closed"; never "the data favour the framework". Every run:
`OMP_NUM_THREADS=1 nice -n 15`, single thread, < 1 GB RSS per process, ≤ 30 min per run (the grid is split into several
runs if needed; a split never changes a cell). No downloads. Literature priors from web look-ups are PROVISIONAL and
labelled. Read only: every other lane, `compute_queue/`, LEDGER.md, the status board, THEORY_V3_DRAFT.md.

**v3 (the yardstick, as P4 and S3 used it).** Static weak-field limit on baryons only: AQUAL ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b with
μ(x) = x/(1+x); screening by the C4-literal stiffness (P4's solver); the external field as P4 (isolated primary, a declared
g_e = 0.03 a₀ along the disc axis reported). No settling, supply, round (RM) or dust rule. The BS24 μ_K²ψ term is not
included (batch R6 owns it).

## 0. Read before freezing (disclosed)

- P4 README, FROZEN_CRITERIA §T4 and §3, `p4_solver.py`, the T4 block of `p4_v3_galaxy_tiles.py`, and the T4 numbers of
  `p4_v3_galaxy_tiles_results.json`: F0 L★ 24 pc K_z,1.1(R₀)/2πG, χ²_Kz, v_c(R₀) (canonical / alt) = B1 92.282 / 96.860,
  178.371 / 250.710, 215.170 / 220.377; B2 90.12 / 94.71, 148.3 / 212.6, 209.1 / 214.3; B2b 104.5 / 109.5, 430.6 / 559.7,
  225.2 / 230.5; B3 (R_d 2.15, Σ(R₀) kept) 96.83 / 101.16, 332.9 / 435.1, 240.86 / 246.13; line χ²₀.₉₉(43) = 67.459; K8
  Newtonian K_z(R₀) 61.89 vs the column 55.05.
- U1 README and `u1_v3_dust_content_results.json` N6: the Eilers target v_c(R₀) = 229.053 ± 4.645 km/s (Eilers+19 Table 1
  interpolated at R₀ = 8.122, σ = stat ⊕ 2 %).
- S3 README, FROZEN_CRITERIA §1-2 and A1-A3, `s3_aqual.py`, `s3_mw.py`, `s3_partA_mw.py`, `s3_partA_mw.out`: the v3 cell is
  AQ_gamma0 (A3), primary Ou+Jiao ρ = 0 Z −4.37 / −4.62, robustness set {ρ = 0.5, e_N = 0, e_N = 2 × h81}, all SHAPE
  EXCLUDED; S3's cached solves live in its untracked `_cache_final/`.
- CFG532 README, FROZEN_CRITERIA §5 and code (`ou_err`, S2 rows); CFG532b FROZEN_CRITERIA_v2 §1 and code; the S2 rows of
  `cfg532_results.json` (Ou: data slope −0.3272 ± 0.1124 under S2, RM-v canonical per-curve CONSISTENT, Δ −1.50σ) and of
  `cfg532b_results.json` (Wang: −0.3734 ± 0.0865 under S2).
- CFG514 and CFG516 READMEs; `campaign_fresh_gravity/REFEREE_2608.10189_MW_rotation_curve.md`; V1 README (its screen lowers
  K_z(R₀) to 79.3 / 81.1); X0 MAP; `hunt_2026/g02_vertical_vs_planar_frequency_split.py/.out` (a QUMOND vertical/planar ratio
  test: a 2.5-3.1σ shared tension, shape-systematic dominated; it is a one-point ratio, not this joint χ² test).
- Web look-ups 2026-10-23 (PROVISIONAL; search-engine summaries, not the papers): Portail+17 (MNRAS 465, 1621) bar + bulge
  stellar mass 1.88 ± 0.12 × 10¹⁰ M☉, inner disc in the bar region 1.29 ± 0.12 × 10¹⁰; Bland-Hawthorn & Gerhard 2016 thin-disc
  R_d 2.6 ± 0.5 kpc (also in the record, `hunt_2026/g02…py`:54); Licquia & Newman 2015 total M★ 6.08 ± 1.14 × 10¹⁰ M☉;
  Licquia & Newman 2016 combined R_d 2.64 ± 0.13 kpc. McKee+15 Σ_b(R₀) = 47.1 ± 3.4 M☉ pc⁻² is in the record
  (`hunt_2026/g02…py`:53, 312).
- No number of this lane exists.

## 1. Step 0: reproductions (read-only use of the record's code; nothing written outside this lane)

- **P4.** P4's `p4_solver.py` imported, and P4's own T4 definitions (`R0_MW` … `load_tsv`, and the `mw_grid` / `mw_obs` /
  data block of `if want("T4")`) executed read-only from `p4_v3_galaxy_tiles.py` (P4's script itself is never run: it
  would overwrite P4's outputs). Reproduce B1 (McMillan17) F0 L★ 24 pc on both footings.
- **S3.** S3's `s3_aqual.py` / `s3_mw.py` imported and the data, C-table and scoring segments of `s3_partA_mw.py` executed
  read-only (`S3_CACHE_DIR` set to this lane's own untracked `_cache_s3/`; `PYTHONDONTWRITEBYTECODE=1` so nothing is written
  into S3's or P4's directory). The census cells (s = 1; e_N = 0, h81, 2 × h81; both footings) are SOLVED FRESH with S3's
  code. The off-census s-grid cells (used only by C-table interpolation and s* in reported per-curve labels) are byte copies
  of S3's cached solves (keys computed with S3's own key rule); S3's directory is never written. Reproduce S3 Part A's
  AQ_iso / AQ_gamma0 / AQ_gamma0_2x combined statistics with the primary errors.

## 2. Question (i): a joint light-column baryon test ("prior box", not a fit)

**Family (declared; all else McMillan17 as P4's `rho_mcm`).** ρ = thin + thick + bar/bulge + gas, with
- gas: McMillan17 HI + H₂ exactly as P4 (held);
- thin and thick stellar discs: McMillan17's vertical exponentials (z_d 0.3 / 0.9 kpc) and its thin share of the local
  stellar column at R₀ = 8.122 kpc (f_thin = Σ_thin/(Σ_thin + Σ_thick) of McMillan17 at R₀), both discs with ONE radial
  scale length R_d (P4's B3 convention), normalised so that Σ_thin(R₀) + Σ_thick(R₀) = Σ_b − Σ_gas(R₀), where Σ_gas(R₀)
  is McMillan17's HI + H₂ column at R₀ (all z) and Σ_b is the grid's local baryon column (discs + gas, all z; the bar's
  column at R₀ is < 1e-4 M☉ pc⁻² and not counted);
- bar/bulge: McMillan17's bulge profile (q = 0.5, r₀ = 0.075 kpc, α = 1.8, r_cut = 2.1 kpc) rescaled to total mass M_bb
  (a COMPACT, axisymmetric representation of the bar + bulge).

**Grid (frozen; 175 cells per footing; no refinement after any result).**
- Σ_b ∈ {40.3, 43.7, 47.1, 50.5, 53.9} M☉ pc⁻²: McKee+15 47.1 ± 3.4, ±2σ in 1σ steps.
- M_bb ∈ {1.64, 1.76, 1.88, 2.00, 2.12} × 10¹⁰ M☉: Portail+17 bar + bulge stellar mass 1.88 ± 0.12, ±2σ (PROVISIONAL).
- R_d ∈ {1.6, 1.9333, 2.2667, 2.6, 2.9333, 3.2667, 3.6} kpc: Bland-Hawthorn & Gerhard 2016 2.6 ± 0.5, ±2σ in ⅔σ steps.

**Solve (P4's code, P4's settings).** P4's `mw_grid(6.6e10/M_u)` (half grid, even symmetry), P4's `rho_axisym(nq = 4)`,
`Problem(…, ge = 0, Lam = 24 pc)`: the AQUAL solve (L★ = 0) is recorded first, then the stiffened L★ = 24 pc solve started
from it. Observables by P4's `mw_obs`: K_z,1.1(R)/2πG at the 43 Bovy & Rix MAPs (R_tab + 0.122 kpc), χ²_Kz with σ ⊕ 5 %,
K_z(R₀), its scale length h, v_c(R₀) at R₀ = 8.122 kpc, χ²_RC against Eilers (stat ⊕ 2 %). Per cell also: total stellar
mass M★ = M_thin + M_thick + M_bb, the model's Σ_b(R₀) and Σ(|z| < 1.1 kpc, R₀) by direct quadrature.

**Pass line (per cell, per footing; the scored cell is L★ = 24 pc, isolated).** The cell PASSES iff
χ²_Kz ≤ χ²₀.₉₉(43) = 67.459 AND |v_c(R₀) − 229.1| ≤ 9.2 km/s AND |v_c(R₀) − 229.053| ≤ 9.290 km/s
(the brief's rounded line and the unrounded 2σ of the Eilers target; a cell must pass both).
Closeness: D = max(χ²_Kz/67.459, |v_c(R₀) − 229.053|/9.290); D ≤ 1 for a passing cell. **Best cell** per footing = argmin D.

**Tags (declared now; reported for every passing cell and the best cell; not part of the pass line).**
- M★-IN iff 3.80e10 ≤ M★ ≤ 8.36e10 (Licquia & Newman 2015, 6.08 ± 1.14, ±2σ; PROVISIONAL).
- R_d-IN iff 2.38 ≤ R_d ≤ 2.90 kpc (Licquia & Newman 2016 combined 2.64 ± 0.13, ±2σ; PROVISIONAL).
- Robustness (reported): the best cell and every passing cell are re-solved at L★ = 90 pc (isolated) and at L★ = 0 with
  g_e = 0.03 a₀ along the disc axis on P4's full grid (P4's bracket). A pass that fails either is labelled FRAGILE.

**Verdict for (i), per footing (never pooled).**
- **FEASIBLE (cells listed):** at least one cell passes. Sub-label **FEASIBLE (tight priors)** if at least one passing cell
  is both M★-IN and R_d-IN; otherwise **FEASIBLE (wide priors only)**.
- **AQUAL-STRUCTURAL:** no cell passes. Meaning: inside this declared box of published baryon priors, v3's static AQUAL
  cannot give the measured vertical force and the measured local circular speed at once; K and V are a property of the
  field equation on the Milky Way's baryons, not of P4's choice of McMillan17.
- Reported with either: the best cell (parameters, χ²_Kz, v_c(R₀), K_z(R₀), h, D, tags); the minimum χ²_Kz over cells with
  |Δv_c| inside the line and the maximum v_c over cells with χ²_Kz inside the line (both may be empty).

**Hand expectation (before any number).** The light column lowers K_z(R₀) but also v_c(R₀); the compact heavy bar raises
v_c(R₀) and adds a direct vertical pull and a radial-term contribution to K_z at R₀; a short disc shortens the K_z scale
length (B1's h 3.84 against the data's 2.72) but raises the inner columns. Best cells expected at the lightest column,
the heaviest bar and R_d ≈ 1.9-2.3 kpc. Expectation: AQUAL-STRUCTURAL on both footings, with the best cell's D ≈ 1.3-2;
a FEASIBLE outcome, if any, only with wide priors (M★ high or R_d outside Licquia & Newman 2016).

## 3. Question (ii): S3 Part A under CFG532's S2 error budget

**S2, exactly as the record defined it.**
- Ou+24: stat ⊕ 5 % at R ≤ 22 kpc, stat ⊕ 15 % beyond (CFG532 §5, `ou_err(inner = 0.05)`).
- Eilers+19: stat ⊕ 5 % everywhere (CFG532 §5).
- Wang+23, Zhou+23, Feng+26: table errors ⊕ 5 % (CFG532b §1).
- Jiao+23 and SL23 DR3+: as published (CFG532b §1: "not applied to Jiao or SL23").
Everything else is S3 Part A unchanged: S3's loader and files, slope windows (15-27.5 kpc; Cepheids 10-R_max), weighted
slope estimator, the law's slope fitted at the same radii with the same (S2) weights, census s = 1, one curve per group
(APOGEE-RGB {Ou, Eilers, Zhou} × LIM {Jiao, Wang}), GLS at ρ = 0 and 0.5, labels SHAPE CONSISTENT |Z| ≤ 2 / TENSION
2 < |Z| ≤ 3 / EXCLUDED |Z| > 3 / NOT DIAGNOSTIC if σ̄ > |b_law + 0.5|/2.

**The v3 cell** is S3's (A3): AQ_gamma0 (AQUAL disc, h81 field along the axis, exact γ = 0 solve). **Primary:** Ou+Jiao,
ρ = 0. **S3's robustness set:** ρ = 0.5 (AQ_gamma0), e_N = 0 (AQ_iso), e_N = 2 × h81 (AQ_gamma0_2x), each under S2. The
3-D γ = 57° cells are not rerun (S3 A3: reported only).

**Verdict for (ii), per footing.**
- **SHAPE EXCLUDED ROBUST:** under S2 the primary label is SHAPE EXCLUDED and all three robustness members are SHAPE
  EXCLUDED.
- **ERROR-MODEL-DEPENDENT:** anything else. The README then names the primary S2 label and which members changed.
- Reported (no verdict weight): Z for every one-per-group pair under S2 (the range), the Cepheid Z, and the per-curve CFG532
  §4 labels (S3's `score`, s* from the s grid) for every curve at the v3 cell under S2 (CFG532's S2 flip was a per-curve Ou
  label).

**Hand expectation.** S2 widens Ou's slope error from 0.074 to ≈ 0.112 but leaves Jiao's 0.057; Jiao dominates the
combination. Expect Z ≈ −3.9 / −4.1 (ρ = 0) and ≈ −3.4 / −3.6 (ρ = 0.5): SHAPE EXCLUDED ROBUST; the per-curve Ou label at
the v3 cell likely CONSISTENT or NEEDS-HEAVY-DISC (as CFG532's RM-v flip).

## 4. Checks (the lane script prints one line per check `<ID> PASS|FAIL <value> <threshold>`; exit 0 iff all pass)

- **C0a** P4 reproduction: B1 F0 L★ 24 pc, both footings, against P4's JSON: |ΔK_z(R₀)| ≤ 0.05, |Δχ²_Kz| ≤ 0.1,
  |Δv_c(R₀)| ≤ 0.05 km/s.
- **C0b** B3 identity: the family at (Σ_b = McMillan17's local discs + gas column, M_bb = McMillan17's bulge mass,
  R_d = 2.15) equals P4's `rho_b3` to ≤ 1e-12 relative at 2,000 random points (R ∈ [0, 40], z ∈ [−5, 5] kpc), AND its solve
  reproduces P4's B3 F0 L★ 24 pc numbers to the C0a tolerances on both footings.
- **C0c** S3 reproduction (primary errors, census solved fresh): AQ_gamma0 primary Z, and AQ_iso and AQ_gamma0_2x primary Z,
  within 0.01 of S3's JSON on both footings; the per-curve law slopes of Ou and Jiao within 1e-4.
- **C0d** fresh census solves vs S3's cached census solves: max |Δg_R/g_R| on 5-27.5 kpc ≤ 1e-6 (all six cells).
- **C1** S2 data slopes and errors reproduce the record's S2 rows (CFG532: Ou `S2_5pct_inner`, Eilers `S2_5pct`; CFG532b:
  Wang, Zhou, Feng `S2_5pct`) to ≤ 1e-9.
- **C2** the Eilers target from P4's definitions equals U1's N6 value (229.053, 4.645) to ≤ 1e-6.
- **C3** grid complete: 175 cells × 2 footings present; every solve's scaled Newton residual ≤ 1e-8.
- **C4** mass bookkeeping: for every cell the grid's total mass equals the analytic sum (discs 2πΣ₀R_d², M_bb, gas by
  quadrature) to ≤ 1 %.
- **C5** resources: every run's peak RSS (parent and children) < 1 GB, every run ≤ 30 min (from the run JSONs).
- **MUTATE** (`--mutate`; outputs `*_MUTATE.out`, `*_results_MUTATE.json`): P4's solver with its mutate μ = x/√(1+x²)
  (L★ = 0, since P4's stiffened solve refuses the mutate) and S3's μ ≡ 1 (`S3_MUTATE`). C0a, the solved part of C0b and C0c
  must FAIL (exit 1). The mutate run does not run the grid; it solves the central cell once (reported) and C3-C5 are
  marked "not evaluated (mutate)".

## 5. Stop rule and amendments

No grid refinement, no new cell, no new constant and no new baryon component after any result of this lane. Any change of
a rule after a number exists is an append-only AMENDMENT labelled POST-RESULT, listing what had been seen; a change before
any number is PRE-RESULT. A failed check stops the part that depends on it (disclosed; its numbers are reported but carry no
verdict) unless an amendment diagnoses a mis-specified check, as the record's practice. The fail is checked as hard as a
pass: a FEASIBLE cell is re-solved for robustness and its tags are reported; an AQUAL-STRUCTURAL result is reported with the
best cell and the two one-sided extremes.

## 6. What the outcomes do not show (fixed now)

- AQUAL-STRUCTURAL is scoped to this family: axisymmetric, compact bar, McMillan17 vertical structure and gas, one R_d for
  both discs, isolated or a uniform axial field, static equilibrium, no μ_K² term, no dust (U1's multi-stream round dust is
  outside v3's literal statics). It does not test a long (≈ 5 kpc) bar, a flaring or warped disc, non-equilibrium (bending
  waves, the LMC), or the Bovy & Rix modelling assumptions.
- FEASIBLE says a published-prior baryon model exists; it does not say the Milky Way has it, and it is not a fit.
- (ii) is S3's statistic with the record's S2 errors; it is not a Jeans forward model (Koop+24), not a DR4 result, and it
  does not re-derive any paper's systematic budget.

## AMENDMENT A1 (2026-10-23, POST-RESULT: reported diagnostics only; no line, grid, class or check changes)

Seen before writing this: the frozen run (9/9 checks PASS). (i) FEASIBLE (wide priors only) on both footings: 7 / 4 passing
cells, all at Σ_b 40.3-43.7 and R_d 1.93-2.27 kpc (R_d-IN false, M★-IN true), best D 0.714 / 0.736, K_z(R₀) 76.7-80.9,
h 3.0-3.5, χ²_RC (Eilers) 96-194. (ii) SHAPE EXCLUDED ROBUST on both footings (S2 primary Z −3.88 / −4.09).

Because the pass rests on P4's χ² statistic (σ ⊕ 5 % per MAP) while the cells sit well above Bovy & Rix's own summary
K_z(R₀) = 66.4 ± 2.2, the win is checked as hard as a fail with these REPORTED diagnostics (no verdict weight), for every
passing cell and each footing's best cell:
- **D1** χ²_Kz with the table errors only (no 5 % term), against the same line.
- **D2** pulls against Bovy & Rix's summary numbers: (K_z(R₀) − 66.4)/2.2 and (h − 2.72)/0.15 (the model's h by P4's
  log-linear fit at the MAP radii).
- **D3** the same baryons' outer rotation shape: P4's solve (isolated, L★ 24 pc) evaluated in the plane at every curve's
  radii; S3's per-curve law slope (same weights) and the combined Ou+Jiao Z (ρ = 0 and 0.5, all pairs) under the primary and
  the S2 errors, with S3's labels. Validation before use (**D3-ref**, a reported control): the same evaluation on B1
  McMillan17 must give the Ou and Jiao law slopes of S3's AQ_iso within 0.005; if not, D3 is reported as unvalidated.
- **D4** χ²_RC against Eilers (stat ⊕ 2 %, P4's statistic) for the same cells, with χ²₀.₉₉(38) quoted beside it.

## AMENDMENT A2 (2026-10-23, POST-RESULT: one more reported diagnostic; nothing else changes)

Seen before writing this: the A1 diagnostics (every passing cell +4.7 to +6.6σ above K_z(R₀) = 66.4 ± 2.2). Added, reported
only: **D5** the smallest model K_z(R₀) over all 175 cells whose v_c(R₀) is inside the frozen v_c line, and over all cells,
per footing, with its pull against 66.4 ± 2.2. It answers whether ANY v_c-passing cell of the box reaches Bovy & Rix's
summary K_z(R₀); it carries no verdict weight (the frozen K line is the per-MAP χ²).
