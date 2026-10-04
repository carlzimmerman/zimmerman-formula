# CFG326 FROZEN CRITERIA: CFG323 extended with Alabi+16 GC density slopes

Written 2026-10-03, after the owner-approved download ("yeah download Alabi+16 too boss", orchestrator chat, 2026-10-03) and **before any Alabi+16 table value was read**. The not-blind statement (section 7) lists everything seen.

## 0. Starting point (fixed, not re-fitted)

- CFG323 (`campaign_fresh_gravity/CFG323_sluggs_measured_tracers/`, frozen b2e7ec16d, results 9ee283199) is the base. Its script is exec'd read-only (up to its MUTATE block, outputs redirected to this lane's directory). CFG323's files are never edited and its result is never retro-fixed.
- Same method, statistic, decision rule (e), footings (a₀ = 9.36e-11 canonical, 1.13e-10 alt), kernel ν_mono and κ = ½ as CFG323. Same 16 galaxies, outer bins, JAM-calibrated masses, measured gas, isotropic primary. No knob scans. Nothing fitted to the GC velocities.
- **The only change:** a per-galaxy GC density slope from Alabi+16 enters wherever CFG323 had no measured profile, under the "measured" test of section 1(b).
- Where both exist (NGC 1023, 2768, 3607, 4486), CFG323's source stays primary and Alabi+16 is a reported consistency check (control K2).

## 1. Alabi+16 input

### (a) Identity (checked before the source fetch)

- arXiv 1605.06101, Alabi, Forbes, Romanowsky & Brodie, "The SLUGGS Survey: The mass distribution in early-type galaxies within five effective radii and beyond" (MNRAS, accepted 2016). Read from the arXiv abstract page's citation metadata. Alabi + SLUGGS + GC-tracer mass: matches the approval.
- The quantity used is Table `tab:summary` column (12), γ, "the power-law slope of the de-projected globular cluster density profile", n(r) ∝ r^−γ. Columns (1) galaxy and (9) log M* (M/L_K = 1) are read with it. Nothing else from the table enters.
- VizieR has no Alabi+16 catalogue: J/MNRAS/460/3838 returns 404, and a J/MNRAS/460 listing shows no 3838 entry.

### (b) What counts as "measured"

The method text (read with its digits masked) says that Alabi+16 fits a linear γ–log M* relation (eq. `eq:fit_gamma`) to slopes compiled from the literature, "with this linear relation we estimate" γ for a galaxy, and that the table "contains a summary of γ for all the galaxies". So column (12) may be the relation's output, not a measurement of that galaxy's own GC system. A relation value is **not** a measured profile: it carries no information about the galaxy beyond its stellar mass. CFG111 has already scored that route.

**Test T0** (by script, after the freeze):
- Transcribe eq. `eq:fit_gamma` (slope a, intercept b, rms scatter) and the table's (galaxy, log M*, γ).
- For each galaxy, residual r_i = γ_tab − (a log M* + b).
- Rounding budget δ_i = ½u(a)·|log M*| + ½u(b) + ½u(γ) + |a|·½u(log M*). Here u(x) is one unit in the last printed digit of x.
- |r_i| ≤ δ_i → **RELATION** (not measured).
- |r_i| > δ_i → **candidate**. It is measured only if the paper's text attributes that galaxy's γ to its own GC surface-density data (galaxy name within the γ section or a table note). Otherwise it is **UNATTRIBUTED**: not measured in the primary, used only in the reported secondary S-A.
- A galaxy absent from Alabi+16's table (NGC 4459 is not in its 23-galaxy list in the Fig. 1 caption) keeps γ = 3.

### (c) How a measured Alabi slope enters

- Tracer ρ ∝ r^−γ_i (Alabi's γ is already deprojected and dimensionless, so no distance or R_e conversion is needed), with CFG323's general-profile Jeans code, isotropic, measured gas.
- Fit errors enter identically to CFG323. Δ_i = max |Δoffset| over γ_i ± σ_i (σ_i = the tabulated per-galaxy error); σ_meas = √(Σ_i Δ_i²)/N over all measured galaxies, including CFG323's four, independent across galaxies. A slope with no published error contributes 0 and is listed.
- The shared σ_γ (±0.5 coherent, half the difference of the means) applies only to the galaxies that are still unmeasured, at γ = 3, as in CFG323. σ_β is CFG323's ±0.5 bracket.

## 2. Statistic

Identical to CFG323: Z_stat = unweighted mean of per-galaxy mean outer log10(σ_obs/σ_pred) over the galaxy SEM (ddof 1); Z_sys adds σ_γ, σ_β and σ_meas in quadrature. Both footings.

**Pre-stated splits** (all printed with N and both Z):
- **ALL (16): the headline.**
- NO-CENTRALS (12): the 16 minus NGC 4486, 4365, 4374, 5846.
- CENTRALS (4).
- MEASURED / UNMEASURED, with coverage N = the number of the 16 with a measured profile (CFG323's 4 + Alabi measured).

## 3. Decision rule (e), unchanged

Applied to Z_sys of ALL on each footing; the headline is the weaker class of the two footings; both are printed.

| verdict | condition |
|---|---|
| FAIL CONFIRMED | mean > 0 and Z ≥ 3 |
| WEAKENED | mean > 0 and 2 ≤ Z < 3 |
| NOT SIGNIFICANT | \|Z\| < 2 |
| REVERSED | mean < 0 and \|Z\| ≥ 2 |

- The verdict text carries "measured-tracer coverage N/16".
- **If T0 classes no Alabi value as measured**, the primary is CFG323's primary by construction. The verdict line then reads "NO NEW MEASURED COVERAGE (Alabi+16 slopes are relation values)", and the class is CFG323's.

## 4. Reported rows (never decision rows)

- **R-A16:** Alabi's table γ (whatever T0 says) as a power-law tracer for every one of the 16 that lacks a CFG323 profile and is in Alabi's table. Z_sys has σ_γ = ±0.5 coherent around γ_i on those galaxies (CFG323's treatment, centred on γ_i instead of 3). A second line uses ±(the relation's rms scatter) instead of ±0.5.
- **R-A16-all:** as R-A16, but Alabi's γ also replaces CFG323's profiles for the overlap galaxies.
- **S-A:** UNATTRIBUTED candidates (if any) treated as measured, with σ_i = the relation's rms scatter.
- Splits are printed for every reported row.

## 5. Controls and checks

| ID | Kind | Test |
|---|---|---|
| K1 | CONTROL | Alabi switched off: the re-run CFG323 namespace reproduces the committed CFG323 `_results.json` stats (mean, Z_stat, Z_sys for every subset, both footings) within 1e-9, and the same verdict class. |
| K2 | CONTROL | Overlap agreement. For each overlap galaxy in Alabi's table, ⟨γ_323⟩ = the mean of CFG323's deprojected local slope at the outer-bin radii. σ_323 = the max \|Δ⟨γ⟩\| over CFG323's ±1σ fit-perturbation profiles. σ_A = Alabi's tabulated error, or the relation rms if T0 says RELATION or no error is given. Pass if \|γ_A − ⟨γ_323⟩\| ≤ 2√(σ_A² + σ_323²) for every overlap galaxy. A FAIL is kept. |
| K3 | CONTROL | Transcription by script from the LaTeX: tab:summary has 23 galaxy rows, whose set equals the 23 names in the Fig. 1 caption; eq. `eq:fit_gamma` gives two coefficients and an rms; one spot row is reprinted. |
| K4 | CONTROL | The inherited CFG323 check rows (C1–C6, P1) pass again in the re-run namespace. |
| T0 | REPORT | The relation test of 1(b), per galaxy, with r_i and δ_i printed. It classifies; it does not pass or fail. |
| M1 | MUTATE (`CFG326_MUTATE=1`, separate `_MUTATE` outputs) | The Alabi γ values are cyclically shifted by one across the 16 in CFG55 order (galaxies missing from Alabi's table are skipped). The test row is the primary if T0 makes any Alabi value measured, otherwise R-A16. Its mean over the Alabi-covered galaxies must change by ≥ 0.01 dex, or its class must change. Otherwise it prints "MUTATE INSENSITIVE" and M1 fails; that FAIL is kept. |

The script prints check() rows and an "N/M checks pass" line, and writes `.out` and `_results.json` files (`_MUTATE` for the control).

## 6. Not used

- Alabi+16's anisotropy values are assumptions (β = −0.5, 0, 0.5), not measurements: not used.
- Its α (potential slope), masses, dark-matter fractions, distances and R_e: not used.
- Its Fig. 4 data points (literature slopes) are a figure: not digitised.

## 7. Not-blind statement

**Known before freezing:** CFG323's numbers, per-galaxy offsets and verdict; CFG111's Alabi-relation result (3.64σ); the Alabi+17 relation span 2.49–3.43 quoted in CFG323.

**Seen during the header pass of Alabi+16:**
- The arXiv abstract page (title, authors, date, comments).
- Section headings, figure and table captions, the tab:summary column header and column notes.
- The γ section text, **with every digit masked**: the method (literature compilation, linear fit to log M*, the table summarises γ for all galaxies). No coefficient, rms or per-galaxy value was seen.
- The 23 galaxy names in the Fig. 1 caption (NGC 4459 is not among them).

**Not seen:** any table row, any γ value, the relation's coefficients or scatter.
