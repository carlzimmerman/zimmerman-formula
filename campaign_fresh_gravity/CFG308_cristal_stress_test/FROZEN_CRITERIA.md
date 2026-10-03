# CFG308 — FROZEN CRITERIA: the CRISTAL a₀ point at z ≈ 5 stress-tested on framework-native inputs

**Owner request (2026-10-02):** "stress test cristal too".

**Frozen before any new number is computed.** Nothing in this lane has been run. At the time of writing, the following had been read:
- CFG303's README, its CRISTAL code path (`cfg303_rc100_cristal_LCDMFREE.py`), its results JSON and its per-galaxy CSV (so the committed per-galaxy g_bar, g_obs and D values, and the committed s★ and intervals, are known);
- the loaders and READMEs of CFG213, CFG220 and CFG223 (the estimator), CFG219's criteria (its σ★ = 0.15 dex), CFG228's README and stage-1 CSV (the [CII] luminosity of DC494057 = CRISTAL-20), and the CFG234 referee README;
- the three CRISTAL tables, their raw TeX (including the dynamics-table footnotes), `cristal_vector/README.md`, `cristal_outer_summary.csv` and `cristal_points.csv`;
- `data_assembly/MULTI_TRACER_GAS_2026-09-30.md` and the CRISTAL lines of `STANDING_2026-09-29.md`;
- Jones+21's ALPINE Table 1 on disk (`data_assembly/highz_literature_tables/jones2021_alpine/`).

**Arithmetic done on inputs while designing (no estimator run):**
- the median quoted inclination errors in Jones+21 Table 1 (30 rows): 9.5° (3DBarolo) and 19° (moment map);
- the sign of V_tot² − 3.36 (R/R_e) σ₀² at the outermost data marker, from `cristal_outer_summary.csv` and the dynamics table. It is negative for CRISTAL-02 and CRISTAL-11 and positive for the other four. That is, in the authors' model there is no rotation left at those two markers once the pressure term is removed.

**Framework.** a₀ = κ c √(G ρ_Λ) with **κ = ½ FITTED** (never derived), and the ν_mono law. The cold mass is still required; no dark-matter particle is added. No halo-fit quantity enters any cell: no f_DM, no log M_tot, and no model curve beyond the last data marker. **No sentence of this lane will say the data favour a law.** A lean is not a detection.

## 1. What is being stress-tested
CFG303 (commit 2d9bdc1b9) gives the following for the six dust-detected CRISTAL discs (02, 03, 07a, 11, 19, 20; z 4.44–5.69), with framework-native baryons (SED M★/(1 − f_molgas) in CFG216's thin exponential disc) and CFG223's estimator:
- **R_e:** s★ = 2.01, 68% [0.24, 7.27], 95% [0.001, 14.9];
- **R_out (outermost data marker, the authors' V_tot there):** s★ = 1.95, 68% [0.42, 5.05], 95% [0.001, 8.78].

FLAT predicts s★ = 1.00. The expected s★ for a₀ ∝ H(z) is 8.84 (CFG223's placement through g_obs at each galaxy's z). At R_out, H(z) sits just outside the 95% upper edge. **The question:** does that exclusion, or the R_e non-exclusion, survive every declared variant of the inputs?

## 2. The estimator (unchanged, executed from committed source)
- **Machinery.** `cfg223_a0_over_time.py` is exec'd up to its marker `P("\nCONTROLS")`, as CFG303 does. This yields `analyse`, `implied`, `place`, `Farr`, `NU` = ν_mono, `A0L` = 9.3603e-11 m s⁻² (canonical footing), and the bootstrap index `IDX(n, 10000)` with seed 223·1000 + n. `cfg216_rc100.py` is exec'd up to its `data` marker for `disc_v2` (the thin exponential disc, R_e = 1.678 R_d).
- **s★** is the root of median_i log₁₀[D_i / ν(g_bar,i / (a₀ s))] = 0 on log₁₀ s ∈ [−3, 3]. The 68% and 95% intervals are percentiles of the 10,000-resample galaxy bootstrap. A row-set with no root returns the bracket edge (0.001 floor or 1000 ceiling) and is flagged.
- **The expected s★ of each law** comes from CFG223's `place` + `implied`: each galaxy is placed on the law through its g_obs at its own z. FLAT gives 1.00 exactly. E(z_med) is printed beside it.
- **Galaxy order** is the one CFG303 uses (six: 02, 03, 07a, 11, 19, 20; nine: 02, 03, 07a, 08, 11, 12, 19, 20, 23b). Leave-one-out subsets keep that order. The same n therefore draws the same bootstrap index matrix.
- **g_bar** = M_b × disc_v2(1, R_e, R)/R (SI), with R = R_e or the outermost data marker's radius.

## 3. The grid axes (declared levels only; no scan, no fit)
Each axis lists its levels and its source. Shifts are applied coherently to all galaxies in the same direction (corner variants).

### (a) Gas route, 7 levels
- **G0 (committed):** dust gas, M_gas = M★ f/(1 − f), with f = the paper's f_molgas (Appendix dust2gas).
- **G+ / G−:** the same with f + errhi and f − errlo, the paper's quoted 1σ (f − errlo is floored at 0).
- **C0:** **[CII] gas where it exists on disk.** Only CRISTAL-20 (= DEIMOS_COSMOS_494057) has an L_[CII] on disk: CFG228's own cube extraction, L = 7.9255 × 10⁸ L☉, read from `cfg228_stage1_alpine_measurements.csv`. Its gas is M_gas = α_[CII] L with α = 30 M☉/L☉, Zanella+18's mean as quoted in the record (CFG228; taken to include helium). The other five keep their dust gas: the CRISTAL tables carry no L_[CII], and there are no downloads.
- **C+ / C−:** α_[CII] = 30 × 10^{±0.3}, Zanella+18's quoted 0.3 dex scatter. This applies to CRISTAL-20 only.
- **S (stars only):** M_gas = 0 for every disc. This is the lower bound on the baryons, so it gives an **upper bound** on s★ (§4).

### (b) Stellar mass, 3 levels
log M★ + {−0.15, 0, +0.15} dex. The CRISTAL tables carry no M★ error; 0.15 dex is the record's declared σ★ for these six discs (CFG219, labelled an assumption there). Each disc's gas is held at its measured mass, M★,committed f/(1 − f), because the dust gas does not scale with M★.

### (c) Pressure support
The table's V_rot(R_e) is the authors' rotation velocity after their pressure-support term; CFG213 adds 3.36 σ₀² back to obtain V_circ. At the marker, the authors' V_tot is the mass model's circular velocity. Its pressure term is taken as the DysmalPy / Burkert+10 form α_c(R) = 3.36 (R/R_e), which equals the record-measured k = 3.37 at R_e (CFG234). The model rotation at the marker is defined as V_r² = max(V_tot² − α_c σ₀², 0).

**At R_e, 3 levels:** g_obs = (V_rot² s_i + α σ₀²)/R_e.
- **P_auth:** α = 3.36, the committed level. It coincides with CFG228's 2R/R_d = 3.356 at R_e, so that level is not counted twice.
- **P168:** α = 1.68 (CFG213/CFG229 variant).
- **P0:** α = 0 (none).

**At R_out, 5 levels:**
- **P_auth (committed):** g_obs = [V_tot² + V_r² (s_i − 1)]/R, which is exactly the authors' V_tot at the committed inclination.
- **P_B10:** g_obs = [V_r² s_i + 3.356 (R/R_e) σ₀²]/R. This is CFG228's constant-σ exponential-disc form 2R/R_d applied to the clipped rotation. It differs from P_auth only where V_r² was clipped (02 and 11).
- **P336, P168, P0:** g_obs = [V_r² s_i + α σ₀²]/R with α = 3.36, 1.68 and 0. These are the record's {3.36, 1.68, 0} pressure variants (CFG213, CFG229).

**No rotation left.** A disc with g_obs = 0 (V_r = 0 and α = 0) has nothing left to rotate. It is carried as g_obs = 10⁻²⁰ m s⁻²: below every law at every s, which is equivalent to D → 0 for the median.

### (d) Inclination, 3 levels
committed, −σ_i, +σ_i (coherent), with i′ clipped to [5°, 90°] and s_i = (sin i / sin i′)². The rotation term scales by s_i; σ₀ and the pressure term do not.

The CRISTAL inclinations are fixed in the fits and the table gives no error. The footnote says they come from JWST/F444W images, except CRISTAL-10a, 20 and 23, which come from the [CII] flux map. The declared σ_i is a record value:
- **19°** for the [CII]-map inclinations (20, 23b): the median Jones+21 moment-map error, for the same tracer at the same z;
- **9.5°** for the JWST-image inclinations: the median Jones+21 3DBarolo error, the smaller record value, used for the higher-resolution images.

### (e) Radius, 2 levels
- **R_e:** the table's R_e,disk, V_rot(R_e) and σ₀.
- **R_out:** the outermost data marker (`cristal_outer_summary.csv`, `outermost_data_marker`), with the authors' V_tot there, which is MODEL-OTHER inside the data with `halo_in_fit = yes`.

**Beam smearing.** Neither the record nor the papers on disk provide a stand-alone beam-smearing correction for the CRISTAL markers. The committed velocities are the authors' forward-model intrinsic values, so they are already beam-deconvolved. No beam-corrected level is therefore declared. The uncorrected raw marker is scored as diagnostic D1 (§7), outside the decision.

### (f) Sample, 2 levels in the decision grid
- **six:** the dust detections.
- **nine with the upper limits as bounds:** the six plus 08, 12 and 23b, whose dust gas is an upper limit (CFG219, CFG220). Each upper-limit disc's gas is bracketed in [0, M★ f_table/(1 − f_table)]. Two builds are scored: "at the limit" (the most baryons, the lower s★ end) and "at zero" (the upper end). The detections take the cell's gas level. In level S both builds coincide (all gas 0).

**Leave-one-out** is control (iii) (§6): the full (a)–(e) grid on each of the six five-disc subsets of the six. It is not pooled into the decision fractions; its fractions are reported beside them.

**Grid size.**
- Decision grid: R_e 7 × 3 × 3 × 3 × 2 = 378 cells; R_out 7 × 3 × 5 × 3 × 2 = 630 cells; **1,008 decision cells**.
- Leave-one-out: 6 × 504 = 3,024 cells.

## 4. Per-cell outputs and the inside/outside rule
**Outputs per cell:**
- s★, its root status (root / no root at the floor / no root at the ceiling), the no-root bootstrap fraction, and the 68% and 95% intervals;
- the expected s★ of FLAT and H(z), and E(z_med);
- whether FLAT and H(z) lie inside the 95% interval.

**The rule.** A law is **inside** if lo95 ≤ s_law ≤ hi95, using the bootstrap percentiles exactly as CFG223/CFG303 do, whatever the point estimate's root status. A law is **excluded** if it is outside.
- **Bound cells, upper limits (nine, gas levels other than S).** The 95% envelope is [min lo95, max hi95] over the two builds. A law is excluded only if it lies outside the envelope, i.e. whatever the true upper-limit gas.
- **Stars-only cells (S).** The cell is one-sided: s★ ≤ hi95(S). A law is excluded only if s_law > hi95(S). Adding any gas can only lower s★, so this cell cannot exclude a law from below. This is proved by monotonicity and checked in C3.

## 5. Decision rule (frozen)
Over the 1,008 decision cells:
- frac_H_excl = the fraction of cells in which H(z) is excluded;
- frac_F_in = the fraction in which FLAT is inside;
- frac_F_excl = 1 − frac_F_in; frac_H_in = 1 − frac_H_excl.

The verdicts:
- **"RIVAL ROBUSTLY DISFAVOURED"** if frac_H_excl ≥ 0.80 **and** frac_F_in ≥ 0.80.
- **"FLAT ROBUSTLY DISFAVOURED"** if frac_F_excl ≥ 0.80 **and** frac_H_in ≥ 0.80.
- **"NOT DISCRIMINATING"** otherwise.

Both fractions excluding each law are reported.

**Secondary readings (reported; they cannot change the headline):**
1. the same fractions over the cells whose point estimate has a root (bound cells count if either build has one);
2. the H(z) target set to E(z_med) instead of the placement value;
3. each radius separately, and the six-disc sample alone.

**Dominant axis.** Within each radius sub-grid, for each axis (gas, M★, pressure, inclination, sample), compute the marginal frac_H_excl at each level. The axis swing is max − min over the levels. The radius axis's swing is |frac_H_excl(R_e) − frac_H_excl(R_out)|. The **dominant axis** is the one with the largest swing (the larger of its two radius values). The same is printed for frac_F_excl, together with the median |Δ log₁₀ s★| between each axis's extreme levels over matched root-bearing cells (non-bound cells only).

## 6. Controls (each can fail)
- **(i) Identity: reproduce CFG303.**
  - The builder at the committed settings (G0, ΔM★ = 0, P_auth, committed i, six) reproduces CFG303's per-galaxy g_bar and g_obs from `cfg303_cristal_pergalaxy_LCDMFREE.csv` to a relative 2e-6 (the CSV has 7 significant figures), at R_e and at R_out.
  - Run through CFG223's `analyse` + `expectations`, it reproduces CFG303's JSON exactly (|Δ| ≤ 1e-9 in log₁₀ and in pull units): s★, lo68, hi68, lo95, hi95, and the FLAT and H(z) expected s★ and pulls. That is 2.01 [0.24, 7.27] / [0.001, 14.9] and 1.95 [0.42, 5.05] / [0.001, 8.78].
  - The grid's own committed cells (R_e and R_out, six) equal the same numbers.
  - The nine-disc "at the limit" build at R_e equals CFG303's nine-disc set with the upper limits used as values (0.674), also exactly.
- **(ii) MUTATE (separate run, `MUTATE=1`, outputs suffixed `_MUTATE`).** Every velocity (V_rot, σ₀, V_tot, the observed markers) is multiplied by 1.5.
  - **M1:** every non-floored log D moves by +log₁₀ 2.25 = +0.35218 exactly, in every build.
  - **M2:** in every cell whose main-run point has a root, s★ rises by at least 2.25² = 5.0625, or reaches the 1000 ceiling. This follows because |d log ν_mono / d log y| ≤ ½ (checked numerically as a precondition), so the median δ falls by at most 0.5 per dex of s.
  - **M3:** the two committed cells' mutated s★ equal an independent scalar `brentq` re-solve to 1e-6.
  - The MUTATE run reads the main run's outputs; if they are missing, its checks FAIL.
- **(iii) Leave-one-out stability.** The decision recomputed on each of the six leave-one-out subgrids equals the full-grid decision. The LOO fractions and the committed cells' LOO s★ are printed. A FAIL here is a finding, kept.
- **Structural (code) checks** over matched cells, all from monotonicity of the median-root in each baryon mass and each g_obs:
  - **C1:** s★(G+) ≤ s★(G0) ≤ s★(G−) and s★(M★ +0.15) ≤ s★(0) ≤ s★(−0.15).
  - **C2:** s★ is non-decreasing in the pressure term at fixed everything else (P0 ≤ P168 ≤ P336 ≤ P_B10 at R_out; P0 ≤ P168 ≤ P_auth at R_e).
  - **C3:** s★(S) ≥ s★ of every gas level, and the "at zero" build ≥ the "at the limit" build in every upper-limit cell.
  - **C4:** inclination −σ_i ≥ committed ≥ +σ_i.

  Ties at the bracket floor or ceiling count as satisfied.

## 7. Diagnostics (declared; outside the decision grid)
- **D1, the raw outermost observed marker** (`cristal_points.csv`, kind `data`, the largest R per disc). This velocity is projected and beam-smeared, with no correction. g_obs = [(V_obs / sin i)² + α σ₀²]/R with α ∈ {0, 1.68, 3.36, 3.36 R/R_e}, at G0, ΔM★ = 0, committed i, six discs. It shows what the uncorrected markers alone say.
- **D2, CFG303's table-R_out variant** (the model curve at the table's R_out) is reproduced (1.90) as a second identity. It is not graded.

## 8. Hand estimates (written before any run; scored in the README, misses kept)
- **H1.** Control (i) reproduces exactly (0.97).
- **H2.** frac_H_excl over the decision grid lies in [0.45, 0.80] (0.6). Pressure P0 and P168 at R_out, and P0 at R_e, mostly give no root, so H(z) is excluded there by the literal rule.
- **H3.** frac_F_in lies in [0.45, 0.75] (0.6). The no-root cells exclude FLAT too.
- **H4.** **Decision: NOT DISCRIMINATING** (0.85).
- **H5.** Root-only reading: H(z) is excluded in 40–75% of the root-bearing cells (0.55), and FLAT is inside in ≥ 90% of them (0.75).
- **H6.** The dominant axis is the pressure term (0.7); the gas route is second (0.5).
- **H7.** At R_out, P0 gives no root in every six-disc cell (0.8).
- **H8.** H(z) is not excluded in ≥ 80% of the stars-only cells (0.7).
- **H9.** The decision is LOO-stable (0.75). The committed R_out cell's H(z) exclusion flips under at least one LOO (0.8).
- **H10.** MUTATE: every root-bearing cell rises by ≥ 5.06 (0.97), with a median factor between 6 and 20 (0.6).
- **H11.** D1 (raw markers) at α = 0 has no root (0.8).
- **H12.** frac_F_excl < 0.5 (0.85), so "FLAT ROBUSTLY DISFAVOURED" is not reached.

## 9. Outputs (this lane only)
- `cfg308_cristal_stress.py`, with check() rows and a final "N/M checks pass" line;
- `cfg308_cristal_stress.out` and `cfg308_cristal_stress_results.json`;
- `cfg308_grid.csv`, one row per cell, decision and LOO;
- `cfg308_cristal_stress_MUTATE.out`, `cfg308_cristal_stress_MUTATE_results.json` and `cfg308_grid_MUTATE.csv`;
- `README.md`.

No other lane's file is written. CFG307's directory is not touched.

## 10. Known limits (stated now)
- Every velocity is the authors' DysmalPy value (MODEL-OTHER, with a halo in the fit) inside the data. The markers rest on 1.6–5.5 beam elements.
- The pressure form at the marker (α_c = 3.36 R/R_e) is inferred from the paper's convention at R_e, not read from the paper's equation, which is not on disk. It affects every level except P_auth at the committed inclination.
- [CII] gas exists for one disc only. The dust gas uses the paper's single conversion, whose temperature and κ choices are not on disk. The upper-limit values are treated as limits (the table's errors on them are not used).
- σ★ (0.15) and σ_i (9.5° / 19°) are record values carried over from other samples, not errors measured for these discs.
- With six discs the bootstrap lower edge often sits at the floor (resamples with no root). FLAT can then be excluded only from above, and the intervals are wide.
- No variant here measures a₀(z). At best the grid shows whether the CFG303 exclusion at R_out is robust to the record's own declared input variants.
