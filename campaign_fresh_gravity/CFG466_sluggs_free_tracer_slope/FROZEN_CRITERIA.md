# CFG466 FROZEN CRITERIA: do the four SLUGGS centrals still fail with the GC tracer slope free?

**Lane:** CFG466. On-disk data only; no downloads. Written before any CFG466 code was run or any CFG466 number was computed.

## Question
The failure ledger (`LEDGER_failure_mechanisms_2026-10-08/README.md`, row 12) flags a HIGH artefact risk for the board tile "Massive ellipticals (SLUGGS)". The four group/cluster centrals' excess was computed at a FIXED globular-cluster (GC) density slope γ = 3. The four are M87 = NGC 4486, NGC 4365, NGC 4374 and NGC 5846.
- CFG330 K0: +0.224 canonical / +0.213 alt.
- CFG331 R-own: +0.198 / +0.187.

The test: let γ be free per galaxy. Is the law's prediction still excluded for each central?

## Fixed inputs (exactly as CFG330/CFG331)
CFG331's source (`CFG331_sluggs_centrals_environment/cfg331_environment.py`) is exec'd read-only up to its `# ---- run` block. That fixes:
- the raw Forbes+17 GC velocities, the |v − V_sys| < 1200 km/s cut and the global 3σ clip;
- equal-number bins, the ML dispersion, and the outer-bin rule R > max(R_e, 2 kpc);
- the ATLAS3D JAM calibration and the Hernquist scale a = R_e/1.8153;
- the kernel ν_mono and κ = ½ (FITTED), on both footings, 9.36e-11 and 1.13e-10;
- CFG331's host gas, members and g_e.

Only two things change: the tracer density and the error model. No knob scans, and no new constant.

## Tracer slope per central
- **M87 (measured).** The tracer is the Agnello+14 three-population Sérsic sum.
  - Values come from CFG323's script-parsed side file, `CFG323_sluggs_measured_tracers/cfg323_transcribed_values.tsv`: A14_n, A14_Re_as, A14_Sib, A14_Srb.
  - The sum is Abel-deprojected numerically with the Ciotti–Bertin b_n, as in CFG323.
  - Uncertainty comes from Monte Carlo: N_MC = 300 draws, seed 466. Each of the 8 parameters is drawn independently from a split normal with the published +/− errors.
    - No correlations are published, so independence is declared.
    - A draw is redrawn if n < 0.5, R_e < 5″, or a ratio ≤ 0.
- **NGC 4365, NGC 4374, NGC 5846 (declared prior).** No GC number-density profile for these three is on disk. The sources checked:
  - Pota+13 HTML: its Sérsic fits appear only in its Fig. 6.
  - Alabi+16 and Alabi+17: their γ values are relation outputs (CFG326 T0).
  - Kartha+14/16: they cover other galaxies.
  - The SLUGGS spectroscopic positions are not a density profile. CFG82 showed that slit and footprint selection biases a naive slope MLE by 0 to +0.8.
  - These three therefore get the declared prior **γ ~ U[2, 4]**, which is Alabi+16's stated range 2 ≤ γ ≤ 4. The tracer is a single power law ρ ∝ r^−γ. It is marginalised on a uniform 101-point grid.
- **Anisotropy (as in the record).** Isotropic, β = 0, in the primary. Constant β = ±0.5 is reported only.

## Per-galaxy error (new; the record has only galaxy-to-galaxy scatter)
- A non-parametric bootstrap over the GCs: N_B = 4000 resamples, seed 466.
- Each resample is drawn from the raw GC list and goes through the same 1200 km/s cut, global 3σ clip, equal-number binning, ML σ and outer-bin rule.
- For each resample, Δ*(γ) is evaluated with σ_pred interpolated in log R from a 60-point table per (reading, footing, γ).
- σ_Δ(γ) is the bootstrap standard deviation.
- For M87 the bootstrap uses the central Agnello profile, and each MC draw is shifted by its own Δ_obs.

## Statistic and per-central outcome (per reading, per footing)
Δ_obs(γ) = mean over the outer bins of log10(σ_obs/σ_pred(γ)). This is the committed statistic.
- **Gaussian p.** p(γ) = 1 − Φ(Δ_obs(γ)/σ_Δ(γ)), and p_G is its average over the prior (for M87, over the MC draws). Z_free = Φ⁻¹(1 − p_G).
- **Empirical p.** p_E(γ) is the fraction of resamples with Δ*(γ) ≤ 0, averaged over the prior. For M87 the condition is Δ*_c − Δ_obs,c + Δ_obs,draw ≤ 0, averaged over the MC draws.
- **Outcomes:**
  - **FAIL (persists):** p_G ≤ 0.02275 AND p_E ≤ 0.02275. The law's prediction is excluded at ≥ 2σ, one-sided, in the excess sense.
  - **CLEARED:** p_G > 0.02275 and p_E > 0.02275, and the central is not REVERSED.
  - **REVERSED:** p_G ≥ 0.97725. The law over-predicts at ≥ 2σ.
  - **FRAGILE:** the Gaussian and empirical tests disagree about the 2σ line.

## Readings
- **Decision readings:**
  - K0: CFG330 K0, stars only; this is the board's fail.
  - R-own: CFG331's PAPER35 ownership reading, the most favourable environment reading on record.
- **Reported only:** R-bar, R-barN, R-efe.

## Class per (reading, footing)
- **ROBUST FAIL:** at least 3 of the 4 centrals FAIL.
- **SLOPE ARTEFACT:** at least 3 of the 4 are CLEARED, and each CLEARED central is also cleared at a fixed slope (Gaussian Z < 2) at the slope the literature assigns, not only at the prior's shallow edge:
  - for M87, its measured profile;
  - for the others, the Alabi+16 relation slope γ_rel, taken from the γ column of `CFG326_sluggs_alabi16/cfg326_alabi16_transcribed.tsv`.
- **NOT DIAGNOSTIC:** otherwise.

**Headline.**
- ROBUST FAIL only if all four cells, (K0, R-own) × (canonical, alt), are ROBUST FAIL.
- SLOPE ARTEFACT only if all four cells are SLOPE ARTEFACT.
- Otherwise NOT DIAGNOSTIC, with the cell classes reported.

## Reported rows (not decision rows)
- Per central:
  - Δ at γ = 2, 2.5, 3, 3.5, 4;
  - γ_null, the slope where Δ = 0, searched over [1.0, 4.0];
  - Z at the prior's favourable edge, γ = 2 (profile-style).
- Alternative priors and inputs:
  - the Alabi relation prior N(γ_rel, 0.29), truncated to [2, 4];
  - a wide prior U[γ_min,M87, 4]. γ_min,M87 is the minimum local deprojected slope of the central Agnello profile at M87's outer bins, computed by script;
  - β = ±0.5;
  - M87 with U[2, 4] instead of its measured profile;
  - M87 with the Zhu+14/Peng+08 single Sérsic (PROVISIONAL text, as in CFG323).
- The centrals' mean, with independent γ draws.

## Controls (main run)
- **C1:** the power-law path at γ = 3, β = 0 reproduces, per central and on both footings, to 1e-9 dex:
  - the committed CFG330 K0 values (`cfg330_summary_K0.json`);
  - the committed CFG331 own/bar/barN/efe values (`cfg331_environment_results.json`).
- **C2:** the general-ρ Jeans code with ρ = r^−γ reproduces the power-law path at γ = 2, 3 and 4, per central, to 1e-5 dex.
- **C3:** Abel deprojection of a Plummer surface density recovers the log-slope of ρ ∝ (1 + r²)^(−5/2) within 0.01 over 0.1–30 a (CFG323's C3).
- **C4:** the central Agnello profile with the K0 field reproduces CFG323's "M87 no gas" offset to 0.005 dex: +0.21780 canonical / +0.20620 alt, from its results JSON.
- **C5:** bootstrap calibration on a synthetic galaxy.
  - The galaxy has NGC 5846's GC radii and velocity errors, Gaussian velocities, and a true σ that is constant at the observed outer-bin σ.
  - The bootstrap SD of Δ from one realisation must be within ±25% of the SD of Δ over 300 independent realisations.
- **C6:** the bootstrap binning code on the unresampled data reproduces CFG331's bins (R_b, σ_b) exactly.

## MUTATE (CFG466_MUTATE=1; separate outputs `_MUTATE`)
- **M1 (reproduction):** γ = 3 is forced for all four, with M87's measured profile replaced by r^−3, and β = 0.
  - The per-central offsets must reproduce the committed CFG330 K0 and CFG331 R-own/R-bar/R-barN/R-efe values to 1e-9 dex on both footings.
  - If they do not, M1 FAILS and is kept.
- **M2 (sensitivity):** γ = 1.5, which is unphysical, is forced for all four, with no marginalisation. For the class rule the forced slope counts as "measured".
  - The headline class must differ from the main run's headline class. If it does not, M2 FAILS and is kept.
  - Reported alongside: whether every central's Gaussian Z at γ = 1.5 is below its main-run Z_free.

## Scope and claims
- This is a per-central test of the statistical error plus the slope.
- The JAM M/L, distance and Hernquist-scale systematics are not propagated. They would widen the errors, which makes a FAIL harder, not easier.
- This is not an a0 measurement. κ = ½ is fitted.
- The verdict reads as stated: a FAIL is verified as hard as a CLEARED.

## Pre-freeze disclosure
Known before freezing (from committed lanes):
- the γ = 3 offsets (CFG330 K0, CFG331 per central);
- CFG111, post hoc: with the Alabi relation γ, the slope that nulls each central is 1.06 for NGC 4365 and 1.13 for NGC 4374, and none ≥ 1 for M87;
- CFG76: the law's zero for the mean of the 16 is at γ ≈ 1.83;
- CFG326 R-A16: the centrals' mean is +0.156 with the relation γ;
- CFG323 for M87 with the Agnello profile: no gas +0.218, measured outer slopes 1.87–2.34, urban_trunc gas +0.141.

No CFG466 number had been computed.

Process: at most 4 processes. One script, `cfg466_free_slope.py`. Outputs: `.out`, `_results.json`, `_MUTATE.out`, `_MUTATE_results.json`, and a README.
