# CFG523 — FROZEN CRITERIA: ALMA archive mining for z ≈ 2–3 discs that reach the deep regime

Frozen 2026-10-09, committed alone before any archive query made for this lane's analysis. Owner approval (in chat, 2026-10-09): mine the public ALMA Science Archive; download public pipeline / science-ready product FITS only (no raw ASDMs); budget ≈ 20 GB; proprietary or login-gated data are skipped, never worked around. Downloads live outside git (`../_external_data/cfg523_work/`); every fetch is logged (UID/URL, size, SHA-256, date) in `FETCH_LOG.md` with relative paths only.

**Framework statement.** a₀ = κ c √(G ρ_DE), κ = ½ FITTED; footings a₀ = 9.36e-11 and 1.13e-10 m s⁻², never pooled. Kernel ν(y) = 1/(1 − exp(−√y)), g = ν(g_N/a₀) g_N. FLAT a₀(z) is the distinctive law; the rival is a₀ ∝ H(z) (×3.7, +0.57 dex at z = 2.5). The cold energy mass is still required; no dark-matter species is added. No sentence will say the data favour a law.

**Primary product = an INVENTORY.** A full a₀ analysis is done only for a target that clears the measured reach gate (M3 below) and has a published measured gas tracer.

## Record check (before freezing)
Already done, NOT redone (overlap is reported, not re-scored): CFG213–229 (incl. ALESS, ALPAKA group), CFG270 KMOS3D cube fits, CFG271 HZ9, CFG272/283 ALPAKA, CFG273 Danhaive, CFG274 Amvrosiadis, CFG275 PKS 0529-549, CFG276 GN20, CFG277 Roman-Oliveira (BRI1335, SGP38326), CFG278 Lelli+23 (zC-400569, zC-488879), CFG280 SINS AO, CFG284/285 ADF22.5, CFG300–304 MIGHTEE, CFG307 ALESS 122.1, CFG308 CRISTAL, CFG385/386 self-calibration, CFG400–402 Genzel17, CFG403 (OSIRIS × deep × ALMA ≤ 0.6″ match: ABC = 0), CFG437/438 BX442, KURVS. Data front 09-30 priced SDP.81 (580 GB raw, no pipeline cube: out of scope) and fetched SPT0418 (z 4.2, out of range).

## Parents (all with an independent spectroscopic z and an SED stellar mass on disk)
P1 KMOS3D catalogue (`data_assembly/kmos3d_phibss/kmos3d_catalog.csv`: Z, RA, DEC, LMSTAR, RHALF [arcsec]); P2 SINS/zC-SINF AO (`sins_ao_table1`, sizes from `sins_ao_table5`); P3 ALPAKA I (`alpaka1_sample` + `alpaka1_properties`). Duplicates within 1.0″ merge. Window **2.0 ≤ z ≤ 3.0**.
A blind sweep (S) is also reported: all public `ivoa.obscore` rows with s_resolution ≤ 0.30″ in scientific category "Galaxy evolution" or "Active galaxies" whose science keywords include sub-mm galaxies / starbursts / lensing / galaxy structure; it has no redshifts, so it is counted (targets, projects) and name-matched to parents only; no target from S enters the shortlist without a literature z, which would be labelled PROVISIONAL.

## Lines (rest GHz)
CO(3–2) 345.796, CO(4–3) 461.041, CO(5–4) 576.268, CO(6–5) 691.473, CO(7–6) 806.652, [CI](1–0) 492.161, [CI](2–1) 809.342, [CII] 1900.537. A line is "covered" when a spectral window in the archive's own `frequency_support` string contains ν_rest/(1+z) with ±300 km/s margin inside the window edges.

## Pre-download gates (inventory → shortlist)
- **G1** parent in 2.0 ≤ z ≤ 3.0.
- **G2** ≥ 1 PUBLIC obscore row (data_rights = Public) whose footprint holds the parent (distance to pointing ≤ s_fov/2) with a covered line and **s_resolution ≤ 0.30″**. (Rows at 0.30–0.60″ are listed in an appendix table, not shortlisted.)
- **G3 reach (predicted).** Baryons: M_bar = M★ (1 + μ_gas), μ_gas from the Tacconi+2018 scaling at the main sequence (log μ = 0.12 − 3.62 (log(1+z) − 0.66)² − 0.35 (log M★ − 10.7)); a reach PREDICTOR only, never an analysis input. Geometry: one thin exponential disc with the stellar half-light radius R_e (R_d = R_e/1.678), Freeman acceleration in the plane. Predicted outermost resolved radius R_out,pred = 2 R_e. **y_pred = g_N(R_out,pred)/a₀ ≤ 2.0 at a₀ = 9.36e-11** (the stricter footing; y at 1.13e-10 is also reported). y at R_e/2 (the inner self-calibration anchor, ≥ 3 desired) is reported.
- **G4 resolution.** 2 R_e ≥ 1.5 × s_resolution (at least three beams across the line disc diameter).
- **Shortlist** = G1·G2·G3·G4, ranked by y_pred ascending; ties by archive sensitivity_10kms. Download in rank order within 20 GB (cube FITS for the spectral window holding the line, plus its pb / mask if small). If the shortlist needs more than 20 GB: stop and report the list with sizes.
- Every G-count also reported with G3 relaxed to y_pred ≤ 4 (labelled, not shortlisted).

## Measured gates (post-download, per cube)
- **M1 detection:** moment-0 over ±400 km/s around the line; peak S/N ≥ 5 (noise from line-free channels, same width).
- **M2 resolved rotation:** along the major axis (PA from the moment-1 extremes, slit one beam wide), at least three beam-spaced positions with S/N ≥ 3 and a monotonic velocity gradient; **R_out** = the largest radius with moment-0 S/N ≥ 3 along that axis; require R_out ≥ 1 beam FWHM.
- **M3 measured reach:** y_meas = g_N(R_out)/a₀ with the same G3 baryons. **REACHES-DEEP** if y_meas ≤ 2 at both footings; **NEAR-NEWTONIAN** if y_meas > 2; **NOT USEFUL** if M1 or M2 fails.

## Analysis (only for REACHES-DEEP targets with a published measured gas mass: CO, [CI] or dust)
- V_rot(R) from the beam-spaced major-axis centroids, deprojected by the literature inclination (or the H-band axis ratio, q₀ = 0.2); g_obs = V²/R (no pressure correction in the headline; σ-corrected reading reported).
- Baryons for the analysis: published SED M★ + published measured gas (stated conversion), same disc geometry. Implied a₀ solves g_obs = ν(g_bar/a₀) g_bar at the outermost point; s★ = a₀,implied / a₀,footing for each footing separately.
- Labels: **NO ROOT / FLOOR** (g_obs ≤ g_bar); **DISCRIMINATING** if the 68 % interval of log s★ (baryons ± 0.2 dex stars, ± 0.2 dex gas, inclination ± 10°) excludes exactly one of {0, +0.57}; **NOT DISCRIMINATING** if it contains both or neither is excluded while its width exceeds 0.67 dex; **UPPER BOUND** if the root exists only at the lower baryon corner.
- **MUTATE (must fail):** V_rot × 0.5 → every analysed row must become NO ROOT (rc 1). Inventory MUTATE: every parent shifted +60″ in Dec → G2 matches must fall to ≤ 10 % of the main run.

## Not claimed
Coverage is not a detection. A reach prediction is not a measurement. No a₀ is reported from a target that fails M3. Pre-registered departures will be disclosed as dated notes.
