# CFG323 FROZEN CRITERIA: the SLUGGS law-only offset re-scored with measured tracers

Written 2026-10-03, after the owner-approved downloads ("yeah download the elliptical tables boss", orchestrator chat, 2026-10-03) and **before any table VALUE was read**. Only ReadMes, section headings, table captions and column headers were read. The not-blind statement below lists everything seen.

## 0. Starting point (fixed, not re-fitted)

- Baseline is the independent recompute `AUDIT_SLUGGS_2026-10-03/audit_sluggs_recompute.py`: ν_mono, κ = ½ fixed, γ = 3, β = 0, CFG55's 16 galaxies, outer bins R > max(R_e, 2 kpc), JAM-calibrated stellar mass (IMF-free).
- Its headline: +0.0977 ± 0.0243 dex, 4.02σ canonical (a₀ = 9.36e-11) / 3.67σ alt (a₀ = 1.13e-10).
- The audit's machinery is reused read-only. Its source runs up to the "1. HEADLINE" block in a private namespace, with no file writes.
- Its bins, clipping, ML dispersions, JAM masses and kernel are inherited unchanged. CFG55, CFG57, CFG111, CFG313 and the audit are never edited.
- Both footings, kernel ν_mono, κ = ½. No knob scans. Nothing is fitted to the GC velocities.

## 1. Tracer inputs

### (a) GC density: measured where published

**Sources, in priority order.** Galaxy names are those of CFG55's 16.
1. A fitted **total-GC-system** surface-density profile (Sérsic R_e, n, background; or a power law) with numerical parameters in a table of a downloaded paper:
   - Kartha+14 (arXiv 1310.1979): NGC 1023, 2768 (720 is not in the 16).
   - Kartha+16 (1602.01838): NGC 3607.
   - Agnello+14 (1401.4461) population tables: NGC 4486.
   - Zhu+14 (1407.2263): NGC 4486 fallback, only if Agnello+14 lacks numerical density parameters.
2. Per-galaxy power-law slopes stated in the **text** of Pota+13 (arXiv HTML 1209.4351, §3.5/§7.1). These are transcribed by position and marked **PROVISIONAL**.
3. Rules for which fit is used:
   - Total-system fits take precedence over subpopulation fits. The velocities are of all GCs, with no colour split.
   - A galaxy with only subpopulation fits is used only if both the normalisations and the fractions are tabulated. The total is then their sum.
   - For M87, if Agnello+14 tabulates per-population density parameters and number fractions, the tracer is the exact mixture (see (b)).
4. Galaxies with no measured profile keep **γ = 3** and are **reported separately** (the "unmeasured" subset).

**Deprojection.**
- The fitted Σ(R), background removed, is Abel-deprojected numerically to ρ(r).
- Angular parameters are converted at SLUGGS's distance.
- The **primary** Jeans model uses the full deprojected ρ(r) in σ_r²(r) = [ρ r^{2β}]⁻¹ ∫_r^∞ ρ r'^{2β} g dr'. It is projected with ρ, so at every bin radius the tracer slope is exactly the deprojected local slope γ_i(r) = −dlnρ/dlnr.
- **Secondary (reported):**
  - S1: the audit's power-law machinery with γ = γ_i(R_bin), evaluated per bin.
  - S2: ρ truncated at the published GC-system extent, where one is tabulated.
- If S1's verdict class differs from the primary's, the output flags "PRIMARY/S1 DISAGREE". The primary still decides.

### (b) Anisotropy

- Measured β only where a downloaded paper **tabulates** it for a galaxy in the 16:
  - M87: Agnello+14's anisotropy table.
  - If β is per population, M87 uses the exact mixture: σ²_los(R) = Σ_k Σ_k(R) σ²_los,k(R) / Σ_k Σ_k(R), each population with its own ρ_k and β_k.
  - If only a single β (constant or β(r) in a table) is given, it is used directly.
- β(r) shown only in figures (e.g. Zhu+14) is **not digitised**. It is recorded as not machine-readable.
- Pota+15 (NGC 1407) is not in the scored 16, since NGC 1407 has no ATLAS3D JAM. Its β is recorded as unscorable.
- Everywhere else: isotropic, with a reported **±0.5 bracket**: β = +0.5 and −0.5 applied to the non-measured-β galaxies.

### (c) Hot gas

- Added to the baryons as mass only. No hydrostatic equilibrium is assumed.
- The JAM calibration includes M_gas(< r½), as in CFG57's convention.
- **Measured gas = CFG57's committed sources**, already on disk under `real_research/data/cfg57_gas_sources/`:
  - Lakhchaura+18 n_e(r): NGC 4486, 5846, 4374, 4649.
  - Fukazawa+06 β-model: NGC 4365, 4494, 3607, 4697, where tabulated.
  - CFG57's D1 conventions are used: μ_e = 1.155, outer extrapolation = power law of the last three points, distance scaling r ∝ D, n_e ∝ D^-½.
- **M87 beyond the Lakhchaura field:**
  - If Churazov+08 or Urban+11 give a *numerical* deprojected n_e(r), either tabulated or as a formula with its normalisation in the text, it replaces the extrapolation from the first radius where it exists.
  - If not, CFG57's extrapolation is kept and M87's outer gas is flagged EXTRAPOLATED.
- Babyk+18 (arXiv 1802.02589) is used only if it tabulates per-galaxy gas masses or n_e profiles for a galaxy in the 16. Its captions show only sample and entropy-fit tables, so the expectation is none.

## 2. Statistic (d)

- **Z_stat:** the audit's statistic. It is the unweighted mean over galaxies of each galaxy's mean outer log10(σ_obs/σ_pred), divided by the galaxy-to-galaxy SEM (ddof 1).
- **Z_sys:** the same mean, with error σ_tot² = σ_stat² + σ_γ² + σ_β² + σ_meas², where:
  - σ_γ: the shared tracer-slope systematic on the **unmeasured** galaxies. It is half the difference of the means with γ = 3.5 and γ = 2.5 applied to all of them coherently. The ±0.5 matches the Alabi+17 relation's span (2.49–3.43).
  - σ_β: the same with β = +0.5 and −0.5 on all non-measured-β galaxies.
  - σ_meas: the published fit errors of the measured profiles. Per galaxy, Δ_i = max |Δoffset| over the four ±1σ perturbations of (R_e, n), one at a time. Then σ_meas = √(Σ Δ_i²)/N, independent across galaxies. A fit with no published error contributes 0 and is listed.
- Both statistics are computed on both footings for:
  - ALL: the 16, measured where available. **This is the headline.**
  - MEASURED: the galaxies with a measured profile.
  - UNMEASURED: the rest, at γ = 3.
  - NO-CENTRALS: the 16 minus the four group/cluster centrals.

### Pre-stated centrals split

- The four centrals are NGC 4486 (M87), NGC 4365, NGC 4374 and NGC 5846.
- They are reported as their own subset, and the 12 non-centrals separately. **Neither split is the headline.**

## 3. Decision rule (e)

Applied to **Z_sys of ALL** on each footing. The headline verdict is the class reached on **both** footings, i.e. the weaker of the two; both classes are printed.

| verdict | condition |
|---|---|
| **FAIL CONFIRMED** | mean > 0 and Z ≥ 3 |
| **WEAKENED** | mean > 0 and 2 ≤ Z < 3 |
| **NOT SIGNIFICANT** | \|Z\| < 2 |
| **REVERSED** | mean < 0 and \|Z\| ≥ 2 |

- Spec text "REVERSED if negative" is read as negative at ≥ 2σ. A negative mean below 2σ is NOT SIGNIFICANT, and the sign is printed.
- The same classes are printed, not as verdicts, for Z_stat and for every subset.
- If fewer than 3 of the 16 receive a measured profile, the verdict text carries "MEASURED-TRACER COVERAGE x/16". The unmeasured galaxies still enter at γ = 3 under the shared systematic.

## 4. Controls and checks

| ID | Kind | Test |
|---|---|---|
| C1 | CONTROL | Audit baseline reproduced: the audit machinery gives the canonical ν_mono 16-galaxy mean at γ = 3, β = 0 within **0.001 dex** of +0.0977, alt within 0.001 dex of +0.0885. |
| C2 | CONTROL | The general-profile Jeans code with ρ ∝ r⁻³, β = 0 and no gas reproduces the audit's per-galaxy offsets within 0.001 dex (max over the 16). |
| C3 | CONTROL | Abel deprojection vs closed form. A Plummer Σ ∝ (1+R²/a²)⁻² must give ρ ∝ (1+r²/a²)^-5/2, with log-slope within 0.01 over 0.1–30 a. |
| C4 | CONTROL | Internal consistency of the measured slopes with the published power-law fits. If a paper also gives a power-law index α for the same profile, the projected Sérsic log-slope averaged in log R over the fitted range must match α within max(0.3, 2σ_α). If no power-law fit is published, the check uses the Prugniel–Simien asymptotic deprojected slope (p_n = 1 − 0.6097/n + 0.05463/n²) against the numerical γ_i at 3 R_e,GC, within 0.15. |
| C5 | CONTROL | Transcription. Rows per transcribed table equal the table's row count, and one spot value is reprinted. Any hand transcription is marked PROVISIONAL and read by position. |
| C6 | CONTROL | Gas-zero with γ = 3 reproduces C2's numbers exactly (≤ 1e-9 dex). |
| M1 | MUTATE (`CFG323_MUTATE=1`, separate `_MUTATE` outputs) | The measured tracer profiles, tabulated on x = r/R_e,gal, are cyclically shuffled across the measured galaxies. M87 receives another galaxy's single total ρ with its number-weighted mean β. The mean offset over the MEASURED subset must change by ≥ 0.01 dex, or a verdict class must change. Otherwise the run prints "MUTATE INSENSITIVE" and M1 fails. That FAIL is kept as it falls. |

Scripts print check() rows and an "N/M checks pass" line, and write `.out` and `_results.json` files (`_MUTATE` for the control).

## 5. Row gap (provenance)

- The Forbes+17 source (arXiv 1701.04835) and the J/AJ/153/114 ReadMe are read to explain why 3,575 velocity rows sit against a galaxy-table N summing to 4,492. Candidate causes to test: UCDs and contaminants tabulated separately, or N counting GCs with velocities from other sources not in Table 5.
- It is reported as an explanation, not a correction. The GC velocity input is unchanged.

## 6. Not-blind statement

**Known before freezing:**
- The audit's numbers and per-galaxy offsets.
- CFG57's gas results (gas moves the mean by 0.010 dex).
- CFG111's Alabi-relation result (3.64σ).

**Seen during the header pass:**
- Table captions and column headers of every downloaded source.
- The Urban+11 figure caption states a power-law fit n_e ∝ r^-1.2 to the deprojected density, with no normalisation seen.
- In Babyk+18, the sample-table header row and the entropy broken-power-law fit table: global entropy slopes, not per-galaxy gas masses.
- No GC density parameter, anisotropy value or gas normalisation from the downloads was read.

**Not available:**
- Pota+13's source tarball (11.8 MB) exceeded the 10 MB per-file cap and was skipped; its arXiv HTML was fetched instead.
- VizieR has no density-profile or anisotropy tables for these papers. Their VizieR entries are velocity or photometry catalogues, or are absent: J/AJ/154/80, J/MNRAS/437/273, J/ApJ/792/59, J/ApJ/857/32 and J/MNRAS/442/3299 return 404.
