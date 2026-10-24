# X26_cold_sector_map: FROZEN CRITERIA (committed alone, before any script or number of this lane)

κ = ½ FITTED. Footings canonical a₀ 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. The cold sector ("cold energy",
Ω_c/Ω_b = 5.364) is gravitating field mass, never a particle. Theory frozen as v3s
(`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §7–8). The map is exhaustive, not a fit: no "best-fit" point is
ever reported as a result, only the allowed region and its boundaries. Never "theory closed". Never "the data favour the
framework".

**Seen before freezing.** V3S verdict §7–8; READMEs/criteria and model sections of X19, X20 (both lanes), X21, X22, X23 (both
lanes), X24, X24b (README head and verdict key only), X25; X22 / X23 / X24 scripts; the μ-pincer verdict (Part F). Committed
numbers read: X22 c_s,need 190.0 / 201.3, f_max 0.196 / 0.0269, its p-scan; X23 A1 one-c_s scan; X24 c₀ 4.59 / 4.05, H χ²
217 / 195 (floor) vs 637 / 559 (law), field χ² 70.0 / 82.9; X21 KT terciles 1.10 / 1.65 / 2.13 and b +2.24 ± 0.74 (canonical
h 0.672); X24b NO ε WINDOW (3492bcbeb4). No number of this lane's model exists.

## 1. The family (stated before any number)

Inside a bound system the cold sector has an effective isothermal sound speed (c_s² ≡ P/ρ_c, one value per system):

    c_s²(system, z) = c_*² · (σ/σ_*)^{2r} · (ρ/ρ_*)^{q} · h(z),   h(z) = a^{2p−1}  (X22's p-family: c_s ∝ a^{p−½})

- σ_* = 100 km/s and ρ_* = 1e-3 M☉ pc⁻³ (baryon density) are units, never fitted.
- **σ** = the system's own 1D velocity scale; **ρ** = its mean enclosed baryon density at the measurement radius, both in X19's
  conventions:
  - SPARC galaxy i: σ = V_last/√2; ρ = M_b(<R_last)/(4π R_last³/3) with M_b from the law's own best Υ (X22's `LAW` index).
  - KT clusters (X21's 106): σ = σ_KT = (kT/μ m_p)^½, μ = 0.6; ρ = M_b(<0.548 Mpc)/(4π 0.548³/3) from X2's model baryons
    (X19's RMID).
  - Groups, MW disc and other X19 classes: X19's class-median σ and ρ_b (`intervals["<f>|p16_84"]`).
  - Dwarfs (per system, X24's rows: 61 hosted H + 13 LG field): σ = X24's binary-corrected σ (`sc`); ρ = (M★/2)/(4π r₁₂³/3).
  - The cosmic medium (forest, σ₈, CMB): the forest half-mode perturbation of X22 (M_hm = 4.89e9 M☉, Lagrangian R_hm = 208
    kpc/h comoving, read from X22's JSON): σ_cos(a) = [G M_hm/(2 a R_hm)]^½, ρ_cos(a) = Ω_b ρ_crit a⁻³ (δ_b = 0; δ_b = 10
    reported). Hence c_s,cos(a) = C₀ a^{p_eff−½} with **p_eff = p − r/2 − 3q/2** (derived in §5's sympy script).
- Free parameters (c_*, r, q, p). z_h is not a separate axis: h(z) is X22's p-family.
- **Grid (exhaustive):** log₁₀ c_* ∈ [0, 4] step 0.125 (33 values, km/s); r ∈ [−1, 3] step 0.125 (33); q ∈ [−1, 1] step
  0.125 (17); p ∈ {3, 4, 6}. 55 539 points per footing. If a step is too slow, the grid is coarsened by an amendment
  committed before that step runs.
- **Special cases marked on the map:** universal late heating (r = q = 0; X23); virial heating (r = 1, q = 0, c_* ≈ the
  system's own σ, i.e. c_* ≈ σ_* = 100 km/s); density-keyed (q ≠ 0; the μ-pincer region); X24b's VHC (vacuum heating per unit
  volume ⇒ per unit mass ∝ 1/ρ: the line r = 0, q = −1 at p = 2; excluded by its own lane, `X24b_vacuum_heated_cold`
  JSON `verdict` "NO EPS WINDOW", 3492bcbeb4; marked, not regraded; its non-barotropic perturbations make forest Jeans
  suppression 3.6× weaker than X22's barotropic form, a stated caveat on the forest cut for q ≠ 0); dwarf floor (below).

## 2. Retention model (no new physics; copied from the record)

- **Galaxies, groups, MW disc, dwarfs:** X22's flat-well hydrostatic content, M_c(<r) = 5.364 M_b (1/δ_ta) 3/(3−β)
  min(r/r_ta,1)^{3−β}, β = 2σ²/c_s², capped at 2.9 (X22 BCAP; CAPTURED flag), δ_ta 5.55, X22's r_ta. SPARC: X22's
  `sparc_stats_g` with per-galaxy c_s,i (vector form; reduces to X22's `gd_hydro` at r = q = 0). Classes and dwarfs: the
  peer lane `X23_late_heating_graded`'s `e_pred` (g_pred = law(g_N + g_c), E = log₁₀ g_pred/g_iso).
- **Clusters:** X23_late_heated_cold's machinery verbatim (X2's functions exec'd read-only, X7's npz, C* potential with noclu
  EFE, isothermal hydrostatic ρ_c ∝ exp[∫_r^{r_ta} g dr/c_s²], A1 normalisation = min(cosmic mean at r_ta, fair share 5.364 M_b),
  the cold mass sources AQUAL and lenses). Per cluster and cell, d_i(c_s) is tabulated on a log grid of c_s (5 to 3e4 km/s,
  ≥ 60 nodes, including X23's A1 nodes c_s,need × {1 … 16} exactly) and interpolated linearly in log c_s; outside the table
  the end value is held (stated, checked by K1).
- **Cosmic medium:** X22's linear two-fluid ODE and `grade` (forest class and R_σ₈), with c_s(a) = C₀ a^{p_eff−½}.
  Monotone in C₀ at fixed p_eff (X22's C3); thresholds are found by bisection in log C₀ on a p_eff grid (step 0.125 or finer,
  covering every p_eff the grid produces) and the class is read from the thresholds.

## 3. Constraints (each a cut; graded per footing; a point passes a constraint only if it passes in both h cells where h enters)

| id | rule | source |
|---|---|---|
| C-forest | X22 forest class ≠ FAIL for c_s,cos(a) (X22's window rule) | X22 step 3B, `forest_class` |
| C-σ₈ | R_σ₈ ≥ 0.95 (X22's window rule) | X22 step 3B |
| C-CMB | k_J(z = 1100) = aH/c_s,cos ≥ 1 h/Mpc (beyond the damping tail) | X23 CMB line, made a cut |
| C-SPARC | X22's d2 line (rms ≤ 0.110 and U_edge ≤ median Υ ≤ 0.80) with per-galaxy c_s,i | X22 step 2 (f_max 0.196 / 0.0269 is the same line) |
| C-groups | \|E_obs − E_pred\| < 2 s, X19 group median row | X23 A1 C-GRP / peer lane |
| C-T1, C-T2, C-T3 | X21 KT-tercile A_MID: \|A_meas − A_pred\| ≤ 2 s per tercile | X21 `binned.V1.terciles`, X23 machinery |
| C-KTb | X21 KT slope: \|b_meas − b_pred\| ≤ 2 s_b | X21 `tests.V1.cells` |
| C-dwarfs | the 74 dwarfs (61 H + 13 LG field) per system: χ²_fam ≤ χ²_floor (X24's floor at its field-calibrated c₀, same 74) **and** Spearman(E_pred, log M★) < 0 | X24 test B |
| C-MW | E_pred(MW disc) ≤ log₁₀(1 + 2·2.2/66.4) = K_z may rise by at most 2σ of 66.4 ± 2.2 | S3/X5 K_z, peer e_pred |

- **Scenario A (family alone):** all constraints graded.
- **Scenario B (separate c₀):** the dwarf extra is assigned to X24's c₀; C-dwarfs is replaced by C-dwarfs-c₀: χ² of
  (floor + family retention, E = E_floor + E_fam) on the 74 ≤ χ²_floor + 4. Every other constraint unchanged.
- **Reported only:** X7 MGAS500 terciles (σ needs KT, so only KT clusters are graded); the other X19 classes (Crater II,
  TDGs, DF2/DF4, UMa, Antlia II, Coma UDGs: their residuals are the law's own, peer A1); δ_b = 10 forest; c_s,cos at z = 3.
- **C-energy (reported):** heating energy per unit mass (3/2) c_s² at the median SPARC galaxy and the median KT cluster over the
  allowed set (range), as a fraction of ρ_Λ c² (for the global cold density, (3/2) Ω_c c_s²/(Ω_Λ c²)) and in keV per baryon
  (5.364 × (3/2) m_p c_s²).

## 4. Rule and verdict classes

A grid point is **allowed** iff every graded constraint of the scenario passes in both h cells, per footing. Footings never
pooled.

- **ALLOWED REGION EXISTS** (Scenario A non-empty on both footings): state its extent (ranges of c_*, r, q, p, the boundary
  table) and the tightest constraints (those that bound it).
- **ALLOWED ONLY WITH SEPARATE c₀**: A empty, B non-empty on both footings.
- **EMPTY**: A and B empty on both footings. Name the closing pair(s): every pair of graded constraints whose joint allowed
  set is already empty; if no pair, the smallest closing triple.
- **UNDECIDED**: footings disagree in class, or step 0 fails.

**Boundary table (required):** for each (r, q) the allowed c_* interval per constraint and their intersection; per
constraint, the (r, q) extent; the first-principles cuts overlaid.

## 5. First-principles cuts (sympy, `PYTHONHASHSEED=0`, separate script `x26_derive.py`; each an inequality on (r, q))

- **FP1 thermodynamic stability:** c_s² > 0 (automatic) and, reading q locally (barotropic P ∝ ρ^{1+q}), dP/dρ > 0 ⇔ q > −1.
  Schwarzschild/convective stability of the hydrostatic profile: per-system isothermal profile stable for any adiabatic
  index γ > 1; barotropic reading stable iff 1 + q < γ (γ = 5/3 ⇒ q < 2/3; reported with γ = 4/3). FP1 hard cut: q > −1;
  the γ cut is conditional and reported.
- **FP2 causality:** c_s < c in every graded system and in the cosmic medium for z ≤ 1100 (computed); asymptotic statement
  derived: c_s < c for all σ → 0 needs r ≥ 0, for all ρ → ∞ needs q ≤ 0, for all ρ → 0 needs q ≥ 0 (so q = 0 unless a
  cutoff). The computed cut is graded; the asymptotic one is reported.
- **FP3 virial bound:** a cold fluid bound by its system with no external confinement obeys 3 c_s² ≤ ⟨r·∇Φ⟩ (= 2σ² in a flat
  well): retention needs c_s/σ ≤ √(2/3)·k (k from the derivation). Since log(c_s/σ) = log c_* + (r−1) log(σ/σ_*) +
  (q/2) log(ρ/ρ_*) is linear in (log σ, log ρ), "retained" vs "expelled" classes must be linearly separable in that plane;
  with q = 0 the ratio is monotone in σ, so no q = 0 member can retain at both ends (dwarfs, clusters) and expel in the middle
  (SPARC). Derived symbolically; applied as a cut on (r, q) using the class medians.
- **FP4 μ-pincer Part F:** for a purely density-keyed c_s (r = 0), the background passes through each well's state at
  (1+z_match)³ = δ_well; derived: with c_s,cos ∝ a^{p_eff−½}, p_eff = p − r/2 − 3q/2, the forest (X22: needs p_eff ≳ 3 at
  c_s,need) cuts q ≤ (2/3)(p − r/2 − 3); stated as an inequality and checked against the graded forest cut.

## 6. Step 0 (stop rule: all must pass, else UNDECIDED with no graded number)

- **K0a:** X21 KT terciles and slope b reproduced via X23's n/d sums ≤ 1e-9 (4 cells).
- **K0b:** X23 A1 KT-tercile A_pred at c_s,need × {1 … 16} reproduced from this lane's table nodes ≤ 1e-9.
- **K0c:** X22 c_s,need reproduced by this lane's SPARC machinery at r = q = 0 (bisection) ≤ 0.1 % relative.
- **K0d:** X22 R_σ₈ at p = 3, 4, 6 and c_s,need reproduced ≤ 1e-6; forest classes identical.
- **K0e:** peer lane groups and MW disc E_pred at c_s,need reproduced ≤ 1e-10; X24 c₀ and χ²_floor (H, field) reproduced
  ≤ 1e-6 relative.
- **K0f:** X24b verdict read ("NO EPS WINDOW").

## 7. Checks and MUTATE

- K1: cluster-table interpolation: A_pred at off-node c_s vs direct ≤ 1 % relative (sample of 6 values × 4 cells).
- K2: SPARC monotonicity in c_* on ≥ 8 full (r, q) columns (used to justify bisection on c_*).
- K3: the sympy script's checks all pass.
- K4: peak RSS < 1 GB.
- **MUTATE (`X26_MUTATE=1`, outputs `*_MUTATE.*`, exit 1):** m1 X21's measured KT terciles swapped T1 ↔ T3; m2 retention
  β = σ²/c_s² (factor 2 dropped). **K0a and K0c must FAIL.**

## 8. Compute

One thread, `nice -n 15`, `PYTHONHASHSEED=0`, < 1 GB, minutes per step; no download; never `compute_queue/`. Commit by pathspec
only; no push. README numbers only from the committed `.out` / `_results.json`.
