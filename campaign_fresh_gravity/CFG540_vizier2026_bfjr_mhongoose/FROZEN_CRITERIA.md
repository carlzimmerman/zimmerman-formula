# CFG540 FROZEN CRITERIA (2026-10-09): the baryonic Faber–Jackson relation (Tian+2026) under the law, and what MHONGOOSE adds

Committed alone, before any σ residual is computed. κ = ½ is FITTED. Footings a0 = 9.36e-11 and 1.13e-10 m s⁻², reported
separately, never pooled. Kernel ν(y) = 1/(1 − e^(−√y)) (ν_mono). No external-field effect (R7). Round enclosed-mass rule (R6).
Cold energy settles into the law's phantom, supply-capped at the census edge (R2/R4). The cold energy's mass is still required.
No dark-matter particle. Not "theory closed".

## 0. Data (owner-approved VizieR ASU-TSV fetch; `FETCH_LOG.md` copied here; stored outside git)

- **J/A+A/710/L39** (Tian+2026, "Baryonic Faber-Jackson relation"), table `catalog`, 1400 data rows. Units from the TSV unit
  row: logSigma [km/s], logMbar [Msun], loggbarRe [m/s²] ("log10(<gbar> within Re)"), Re [kpc] ("Effective radius/mean
  radius"), logFPmass [Msun] = log10(5 Re σ_e²/G). So σ is σ_e, the dispersion inside Re (checked pre-freeze: logFPmass
  reproduces 5 Re σ²/G from the listed logSigma and Re). Samples: MaNGA elliptical 1218, ATLAS elliptical 26, Galaxy group 63,
  Fornax dwarf 31, Virgo dwarf 34, Local Group dwarf 28.
- **J/A+A/712/A74** (Veronese+2026, MHONGOOSE): table1 (16 galaxies: D, log M_HI, i, log M*, log SFR) and HI column-density
  profiles (units 1e19 cm⁻²). **No rotation curves are in this catalogue.**
- **J/A+A/705/A13** (TDCOSMO XXI, SL2S): a list of spectrum files only, no tabulated σ. **Not usable**; nothing more is fetched.

**Pre-freeze disclosures (dated 2026-10-09).** Before writing this file I looked at the column header/units, the per-class
ranges of logSigma, logMbar, loggbarRe, Re and the errors, and I compared loggbarRe with log(G M_bar/Re²): the offset is
+0.17 (ATLAS), +0.21 (MaNGA), +0.17 ± 0.38 (groups), −0.36 (Fornax), −0.28 (Virgo) and exactly −0.465 (LG) dex. So the
catalogue's g_bar is profile-dependent and not reproducible from M_bar and Re alone with the ReadMe on disk. I computed the
census f_ret ranges for group masses (CFG515 `fret_census`). **No σ prediction and no residual has been computed.** The paper
text is not on disk: what enters "Mbar" for groups (members' stars + cold gas, or also hot gas) and for dwarfs is not
known to me. The groups verdict is conditional on that and says so.

## 1. Estimator (derived, declared; no knobs)

Each system is a spherical, non-rotating, self-consistent baryonic body: tracer density = baryon density (mass follows light).
The law's field is g(r) = ν(g_N(r)/a0) g_N(r), g_N = G M_b(<r)/r² (round rule), plus the census edge (below).

- **Profiles (declared):** ellipticals (MaNGA, ATLAS) and groups: **Hernquist**, R_e = 1.8153 a (projected half-mass).
  Dwarfs (Fornax, Virgo, LG): **Plummer**, R_e = a. The catalogue Re is taken as the projected half-mass radius.
- **Jeans:** constant anisotropy β; ρσ_r²(r) = r^(−2β) ∫_r^∞ r'^(2β) ρ g dr'; projected Σσ_p²(R) = 2∫_R^∞ (1 − βR²/r²) ρσ_r² r dr
  /√(r² − R²).
- **Aperture (declared):** ellipticals and dwarfs: σ_law² = light-weighted ⟨σ_p²⟩ inside R < Re (σ_e). Groups: the whole-system
  line-of-sight dispersion (aperture ∞, the members' global σ), which equals ⟨r g⟩/3 for any β (virial). In the deep-MOND limit
  this is Milgrom's exact σ⁴ = (4/81) G M a0, which is the check K1 below.
- **β:** primary β = 0; sensitivity β = −0.3 and +0.3. A class verdict is called only if it is the same at all three β; otherwise
  it is labelled β-DEPENDENT (reported with all three).
- **Census edge (part of the framework, primary):** r_edge = r_M / ln(1 + f_ret f_b/(1 − f_b)), r_M = √(G M_b/a0), f_ret =
  CFG515 `fret_census(M_b)` (imported read-only). Beyond r_edge the phantom (settled cold energy) mass is frozen at its value at
  r_edge: g = G[M_b(<r) + M_ph(r_edge)]/r². The law without the edge is also reported; for each class the shift edge-vs-no-edge
  is reported, and the edge is called irrelevant inside Re if |shift| < 0.005 dex for every object in the class.
- **Mass-error propagation:** s_i = d log σ_law / d log M_b (numerical, per object); σ_Δ,i² = e_logSigma² + (s_i e_logMbar)².

## 2. Statistics

Δ_i = log σ_obs − log σ_law, per object, per footing.

- **Classes (primary verdicts):** GROUPS (63); ELLIPTICALS = MaNGA + ATLAS (1244); DWARFS = Fornax + Virgo + LG (93).
  Each sub-sample is reported descriptively.
- Class mean Δ̄ (unweighted) with SE = sd/√N (empirical; includes intrinsic scatter). Weighted mean and median reported.
- Class systematic floor (declared): σ_sys = s̄ × 0.10 dex (a class-common 0.10 dex baryonic-mass-scale systematic: M/L, IMF,
  distance). σ_tot = √(SE² + σ_sys²); Z = Δ̄/σ_tot (Z_stat = Δ̄/SE also reported).
- **Verdict per class (per footing):** NOT DIAGNOSTIC if σ_tot > 0.045 dex (the record's +0.09 dex would be < 2σ). Else
  CONSISTENT if |Z| < 2; ABOVE LAW if Z ≥ +2; BELOW LAW if Z ≤ −2 (Z ≥ 3 in size noted as strong).
- **Trend with g_bar:** x = log(g_bar/a0) with the catalogue's loggbarRe; OLS slope of Δ on x over all 1400 (bootstrap SE,
  2000 resamples, seed 540), and binned means in 0.5-dex bins (N ≥ 10). **TRACKS** if every bin mean with N ≥ 10 lies within
  ±0.10 dex; **DOES NOT TRACK** otherwise (bins out of range named). Same with x' = log(G M_b/(2 Re²)/a0) reported.
- **Massive-system tension (record: SLUGGS centrals +0.07/+0.06 dex in σ; KiDS early-type ε ≈ +0.5 → about +0.04 (deep) to
  +0.09 (Newtonian) dex in σ).** For ELLIPTICALS and for GROUPS separately: **REPLICATES** if Δ̄ ≥ +0.035 dex and Z ≥ 2 at
  every β; **DOES NOT REPLICATE** if Δ̄ + 2σ_tot < +0.07 dex at every β; otherwise NOT DIAGNOSTIC / β-DEPENDENT. Also reported:
  the MaNGA massive end (log M_b ≥ 11.3) and Δ vs log M_b slope inside ELLIPTICALS.
- **No-EFE readout (descriptive, named in advance):** Fornax and Virgo dwarfs sit in cluster fields; the framework has no EFE,
  so its σ is the isolated one. A Fornax/Virgo mean significantly BELOW the law while LG dwarfs are on it would read as an
  EFE-like signature (against R7); the reverse or no difference reads with R7. Reported, no verdict weight (tides,
  non-equilibrium and the unknown dwarf M_b composition are not modelled).

## 3. Checks (must pass before any verdict is read)
- K1: groups' deep-MOND limit — for an object with y = G M/(Re² a0) < 1e-3, σ_law reproduces (4/81 G M a0)^(1/4) to < 0.01 dex
  (no edge).
- K2: Newtonian limit (ν = 1) Hernquist isotropic aperture-∞ σ² = GM/(6a) (exact for Hernquist) to < 0.5%.
- K3: logFPmass reproduces 5 Re σ²/G from the listed columns to < 0.01 dex for every row.

## 4. MUTATE (`CFG540_MUTATE=1`, separate outputs `_MUTATE.*`); each must FAIL as stated
- M1 Newtonian (ν = 1): GROUPS and DWARFS must not be CONSISTENT (expected ABOVE LAW).
- M2 a0 × 4: GROUPS and DWARFS must not be CONSISTENT (expected BELOW LAW, about −0.15 dex in deep MOND).
- M3 σ shuffled across systems within each sub-sample (200 shuffles, seed 540): the within-class rms of Δ must exceed the
  true rms in ≥ 95% of shuffles for ELLIPTICALS and DWARFS (per-object tracking, not just the class mean).
- MUTATE passes if M1, M2, M3 all behave as stated on both footings.

## 5. PART B — MHONGOOSE (descriptive; no verdict)
- Integrate the global stacked profile (ProfStack; face-on N_HI) to M_HI(<R) = ∫ 2πR N_HI m_H dR; compare with table1 log M_HI.
- For thresholds N_HI = 1e20 and 1e19 cm⁻² (typical older and SPARC-era HI depths), report the radius where the profile first
  drops below the threshold, the HI mass fraction beyond it (what a curve-and-model stopping there would miss), and the
  gas-only g_bar there (1.33 M_HI, spherical enclosed) in units of a0 (both footings).
- State plainly: no rotation curves, so no RAR or outer-slope test is possible from this catalogue.

## 6. Outputs and rules
`cfg540_bfjr.py` → `cfg540_bfjr.out`, `cfg540_bfjr_results.json` (MUTATE → `_MUTATE.*`); `cfg540_mhongoose.py` →
`.out` / `_results.json`; README with numbers read from the JSON. `nice -n 10`, ≤ 2 threads. Nothing more is fetched. This
file is never edited after commit; any later change is a dated addendum.
