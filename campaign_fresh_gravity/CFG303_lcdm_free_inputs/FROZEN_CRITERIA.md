# CFG303 — FROZEN CRITERIA: every a₀ input on the record, tagged; the ΛCDM-halo-derived inputs replaced by framework-native ones and re-run

**Frozen before any re-run of any lane and before any replacement value is computed.** At the time of writing, the following had been read: the status record `STANDING_2026-09-29.md`; the two chart READMEs and `chart_a0z_points.csv`; the READMEs and loaders of CFG210, CFG213, CFG216, CFG217, CFG223; the head and section index of CFG189's README and the key layout of its results JSON; `data_assembly/rc100_provenance/README.md`; `data_assembly/price2021_rc41/README.md` and the column headers of its two CSVs; the column headers of the three CRISTAL tables in `data_assembly/arxiv_tables/`; and the S5 section of the MNRAS v3.1 `paper_numbers.py` (read only, never edited). No replacement input has been evaluated, and no committed estimator has been run with a replaced input.

**Owner direction (2026-10-02, verbatim):** "we need to use all the data using our framework not ACDM assumptions!" and "we must use empirical evidence raw and unfiltered".

**The framework here** is a₀ = κ c √(G ρ_Λ), with **κ = ½ FITTED** (never derived), and the ν_mono law. Candidate B adds hierarchical ownership and a cold component whose **mass is still required**. No dark-matter particle is added anywhere in this lane. Both footings are carried where a lane carries them: a₀ = 9.36 × 10⁻¹¹ m s⁻² (ρ_Λ) and 1.13 × 10⁻¹⁰ m s⁻² (ρ_crit).

## 1. The tags (applied to every input quantity)

- **LCDM-MODEL.** Any of the following:
  - an output of an NFW, DC14, Einasto or Burkert dark-matter-halo fit: f_DM, V_DM, a halo mass or concentration, Σ_DM;
  - a baryon mass that is the posterior of a joint baryon + halo fit (for example RC100's log M_baryon, CRISTAL's log M_tot, NOEMA3D's dynamical baryon mass);
  - a disc + halo model curve evaluated **beyond the radial range of the data** (where its value is set by the halo shape);
  - a c(M) relation, an abundance-matching, SMHM or halo-prior stellar or halo mass;
  - any prior or calibration drawn from a ΛCDM simulation. This includes the DC14 profile itself and the Kretschmer et al. (2021) pressure-support factor α(x), which is calibrated on the VELA ΛCDM zoom simulations, together with any correction that uses α(x)'s shape with a rescaled normalisation.
- **MODEL-OTHER.** An authors' model value that is not one of the above. Examples: a dynamical-model total circular velocity at a radius **inside** the data range; a pressure-support or asymmetric-drift model (Burkert et al. 2010's 3.36 σ₀²; an isothermal self-gravitating layer; a fixed scale height); a gas scaling relation (Tacconi et al. 2018/2020); a virial M_dyn; a JAM model; a published fit level (for example an a₀ fitted with the authors' M/L); a structural fit parameter (R_e, B/T) from a kinematic fit. **A disc + halo model's total velocity inside the data range is tagged MODEL-OTHER with the flag `halo_in_fit = yes`.** There, the data pin the value whatever halo family is fitted. Its halo dependence is disclosed in every row, and where a measured velocity exists on disk the measured one is preferred.
- **RAW.** A measured quantity: rotation velocities, dispersions and line widths; HI, CO and dust fluxes and the gas masses converted from them with a stated α_CO or dust calibration; photometry and SED stellar masses with a stated M/L and IMF; sizes, inclinations, positions and redshifts; distances from the Hubble law with H₀ stated. Angular-diameter distances computed in a stated FLRW background (H₀, Ω_m) count as **geometry (RAW)**. They are not a halo output, and the framework's own background has the same form, with Ω_c h² fitted.
- **COMPARATOR.** A ΛCDM-side quantity used only to build the ΛCDM comparator, such as the effective-a₀ proxy or halo-mass-matched rises. It is never an input to the framework's a₀ measurement. It is inventoried but not replaced.

## 2. The inventory (`INVENTORY.csv`)

Scope:
- every section of `STANDING_2026-09-29.md` that carries an a₀-law statement: §1 SPARC and the law's checks; §3 populations (KiDS, SLUGGS, super spirals, Local Group, ultra-faints and satellites, X-ray ellipticals, SLACS, X-ray groups, clusters, Chae); §4 and the appended a₀(z) lines (RC100, CRISTAL, MUSE-DARK, KURVS, KROSS, MIGHTEE, KiDS, the z ≥ 2 samples, BUDHIES, KMOS3D, SINS);
- the chart inputs (`CHART_a0z_rar_z0_5_2026-10-01/`, `CHART_a0z_combined_2026-09-30/chart_a0z_points.csv`);
- the lanes CFG213–CFG302.

One row per input quantity, with the fields `lane, dataset_or_object, quantity, source_paper, how_authors_derived, tag, halo_in_fit, feeds, native_replacement_on_disk, evidence_file`. The provenance comes from the lane READMEs, the loaders and the `data_assembly` provenance files. Where these are unclear, the source paper's arXiv abstract or HTML may be read as a page read; there are no downloads. A pure-theory or referee lane gets one row saying so.

## 3. The re-run rule

- **Where.** In a scratch mirror built by `git archive HEAD`, outside the repository. Outputs are copied back into this lane only, with the suffix `_LCDMFREE`. No committed output of any lane is overwritten, and no other lane's file is edited.
- **What estimator.** The lane's own committed estimator. Its functions are taken from the committed source text (exec of the committed file up to a fixed marker, as CFG223 itself does for CFG213/CFG220), not rewritten. Only the replaced input differs.
- **No knob scans.** Each replacement and each variant is declared in §4 before its run. A replacement discovered during the inventory is declared in a dated addendum (`FROZEN_CRITERIA_ADDENDUM_n.md`) written before that replacement is evaluated. The addendum says what had been seen when it was written.
- **Verify both ways.** A shift that helps the framework is checked as hard as one that hurts it, with the same controls and the same tolerances.

## 4. Declared replacements (before any run)

### R1 — RC100 (Nestor Shachar et al. 2023)
Committed uses:
- CFG223's four z-quartile implied-a₀ points (the chart);
- CFG216's within-sample Theil–Sen slopes of δ_flat and δ_rival;
- the MNRAS v3.1 S5 closed-form inversion a₀ = (1 − f_DM) g_obs / [ln(1/f_DM)]².

All three form g_bar = (1 − f_DM) g_obs, which is LCDM-MODEL (NFW decomposition). RC100's log M_baryon is the posterior of the joint fit, also LCDM-MODEL.

- **g_obs (kept):** V_c(R_e)²/R_e from the corrected transcription. This is MODEL-OTHER with `halo_in_fit = yes`, inside the data range (RC100's curves reach 1.3–4 R_e), and it includes the paper's 3.36 σ₀² term.
- **g_bar, native:** g_bar = M_bar,nat × `disc_v2(1, R_e, R_e)` / R_e. Here `disc_v2` is CFG216's committed thin exponential (Freeman) disc, R_e = 1.678 R_d, evaluated at R = R_e; all baryons are in the disc. This is primary geometry **G1**. CFG216 already used this geometry in its sensitivity (d), with the table's posterior mass.
- **M_bar,nat, sample A (primary, on disk):** the RC41 galaxies found in RC100 by name (CFG216/217's name join), with M_bar,nat = 10^logMstar_SED + 10^logMgas from Price et al. 2021 Table 1 (`data_assembly/price2021_rc41/price2021_rc41.csv`). These are the SED M★ and the measured or Tacconi+18-scaling gas; the per-galaxy gas source is not flagged in the table.
- **M_bar,nat, sample B (conditional):** all 100 galaxies, with M★,SED from RC100 Table 3 column 6. It is transcribed from the local PDF copy (sha256 a04738e4…, named in `data_assembly/rc100_provenance/README.md`; no download). The gas is M_gas = μ M★ with CFG217's committed function `mu_t18(z, log M★)`, as written (δMS is not used; disclosed). Sample B runs only if the transcription passes all three gates:
  - **T1:** the transcribed column 7 (log M_baryon) equals the corrected CSV in all 100 rows;
  - **T2:** the transcribed column 8 (log M_bulge) equals the value carried in the committed (uncorrected) CSV for the 7 rows that carried M_bulge by mistake (rows 58, 62, 63, 65, 77, 93, 95);
  - **T3 (reported, not gating):** the median |column 6 − Price SED log M★| over the RC41 overlap.
- **Declared variant G2 (sample A only):** the bulge fraction B/T from Price Table 1 is placed as a point mass inside R_e, and (1 − B/T) goes into the G1 disc.
- **Outputs:**
  - CFG223's s* per committed quartile (the committed `EDGES`; the functions `implied`, `analyse`, `expectations`, `bands`; seeds as committed), plus one pooled point per sample;
  - CFG216's slopes, CIs, z-scores against flat-true and rival-true, and outcome label (its functions `delta`, `slope_ci`, `med_ci`, `outcome`, and the expected-slope block);
  - the S5 statistics of `rc100_run` (slope, bootstrap error, median a₀, distances from constant and H(z)), fed through a temporary table with f_DM,nat ≡ 1 − g_bar,nat/g_obs, so that the paper's committed function is unchanged.
- Galaxies with g_bar,nat ≥ g_obs (D ≤ 1, the Newtonian floor) stay in the median estimators and are counted; S5's own (0.02, 0.98) window excludes them, and they are counted there too.

### R2 — CRISTAL (ALMA-CRISTAL, arXiv:2507.11600)
Committed uses: CFG223's four CRISTAL points (fit route R_e/R_out; independent route R_e/R_out) and CFG213's Z5 bin. The fit route forms g_bar from (1 − f_DM). The committed "independent" route forms g_bar = (1 − f_DM) V_c²/R_e × M_ind/M_fit. That still carries the fit's f_DM and M_fit (both LCDM-MODEL) as the baryon geometry.

- **g_obs (kept):** (V_rot(R_e)² + 3.36 σ₀²)/R_e, as committed (MODEL-OTHER, `halo_in_fit = yes`). At R_out: V_tot(R_out)²/R_out from the committed vector extraction (MODEL-OTHER, `halo_in_fit = yes`, at the outermost data radius).
- **g_bar, native:** M_ind × `disc_v2(1, R_e, R)` / R, with R_d = R_e/1.678, at R = R_e and at R = R_out. M_ind = M★,SED/(1 − f_molgas) is exactly the committed independent route's baryon mass: SED stars plus CRISTAL's tabulated gas fraction.
- **ID sets:** (a) the committed independent-route six; (b) the committed fit-route twelve, restricted to rows with finite log M★ and f_molgas. Outputs: CFG223's s*, intervals, expectations and bands for each point.

### R3 — MUSE-DARK II/III
Route (i) (DC14-fitted masses) is **LCDM-MODEL**. Routes (iii) (SED stars) and (ii) (SED + H₂), as committed in CFG262, are the framework-native baryon routes. If CFG262's velocity in routes (ii)/(iii) is itself read from the DC14 model curve:
- inside the data range it is MODEL-OTHER (`halo_in_fit = yes`), and the committed route (ii)/(iii) numbers are the LCDM-free headline (no re-run);
- extrapolated beyond the data it is LCDM-MODEL. A re-run is then required with a measured velocity where one exists on disk; otherwise the row is listed as not replaceable.

### R4 — KURVS (and KROSS through the same pipeline)
- **P4 (Kretschmer et al. 2021)** is LCDM-MODEL (VELA-calibrated), and so is every s-scaled K21-shape row.
- The LCDM-free pressure models are the committed analytic ones: P0 (none), P1 (Burkert constant-σ), P2 (the isothermal self-gravitating layer with the measured outer σ; CFG141's headline) and P3 (fixed scale height).
- The model velocity (Table B1 column 3) is MODEL-OTHER; the measured outer markers (CFG189's primary marker set) are RAW.
- **LCDM-free primary cell:** the measured markers through CFG141's committed P2, at the decision cell μ = 0.67, canonical. P0, P1 and P3 are reported beside it.
- If no committed lane holds those numbers, CFG189's own driver is re-run with CFG141's P-prescriptions in place of P4 (the pipeline and the marker loader as committed).
- The gas prior (PHIBSS measured CO, CFG164) is RAW with a stated α_CO.

### R5 — anything else
Every other LCDM-MODEL input found by the inventory that feeds a committed number is either re-run under a dated addendum (§3) or listed in the README as **not replaceable on disk**, saying what data would be needed. Any such data would need the owner's yes to fetch; nothing is fetched by this lane.

## 5. Controls that can fail (each lane re-run carries all three)

- **C-i (identity replacement).** The LCDM-free driver, fed the original input through the replacement path (for RC100 and CRISTAL, g_bar,nat := the committed g_bar), reproduces the lane's committed output. Tolerance: |Δ log₁₀ s*| ≤ 1e-9; slopes, CIs and medians ≤ 1e-9; labels identical.
- **C-ii (swap-back).** After the native run, the LCDM-MODEL input is swapped back into the same data structure (full sample, mask = all), and the committed output is reproduced to the same tolerance. For a lane whose committed script is run unmodified in the scratch mirror, that run must also reproduce its committed JSON numbers (timing lines excepted).
- **C-iii (MUTATE).** M_bar,nat × 10^0.2 for every galaxy:
  - every log₁₀ D must move by −0.2000 ± 1e-12, and every log₁₀ g_bar by +0.2000 ± 1e-12;
  - the median δ at s = 1 must move by exactly the amount an independent recomputation gives (≤ 1e-9);
  - each s* must move down, unless both runs have no root, which is reported;
  - the mutated s* must equal an independent scalar `brentq` re-solve of the median condition to ≤ 1e-6 in log₁₀ s*.
  - For KURVS, MUTATE is the committed lane's MUTATE path. If the committed script exposes none for the swapped prescription, the measured V is multiplied by 10^0.1 (0.2 dex in V²), and every disc's Δ′ must move by the independently computed amount.
- **Transcription gates** T1–T3 (R1-B), as above.
- A failed control is kept, reported and never re-tuned. Each script ends with a final line "N/M checks pass".

## 6. When a recorded statement "changes"

A recorded statement or headline counts as **changed** by its LCDM-free counterpart if any of these hold:
- (a) its class or verdict word changes (for example W-flat → W-mixed, lean rival → non-diagnostic, root → no root);
- (b) its central value moves outside the committed 68% interval;
- (c) a sign flips.

Otherwise it is **unchanged** (the shift is still printed). A statement whose inputs were all RAW or MODEL-OTHER is **not affected**. One whose LCDM-MODEL input has no native replacement on disk is **not replaceable**, and what is missing is said. The report gives old → new for every re-derived headline.

## 7. Wording rules

- No sentence says the data favour a law, the framework or ΛCDM.
- κ = ½ is FITTED.
- The cold mass is still required, and no dark-matter particle is introduced.
- No personal names and no absolute home paths in any file.
- No downloads.
- No edits to other lanes' files, and never to `paper_numbers.py`.
- An LCDM-free result that lands nearer the flat law is checked as hard as one that lands farther from it.
