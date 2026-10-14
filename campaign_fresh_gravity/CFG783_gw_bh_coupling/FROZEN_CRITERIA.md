# CFG783 FROZEN CRITERIA: are black holes cosmologically coupled (k = 3)? A volume-limited test on raw GWTC source masses

Committed alone, before any script or number. 2026-10-14. Block CFG780–789.
- Owner: "yeah dude do all of it.. you dont need to ask me". This approves the GWTC download.
- Data: GWOSC event API (`https://gwosc.org/eventapi/json/GWTC/`), fetched 2026-10-14 15:43, 738,435 bytes, sha256
  `9802865cc8b41508f4073769758f7dbaf5498b22a907849d567083635e7e862a`. Stored outside the repo in
  `_external_data/gwtc_eventapi/`; not committed. No number had been read from it when this file was written; only its first
  600 bytes were displayed.

## Question
- If black-hole masses grow as M ∝ a^k with k = 3 (Farrah et al. 2023; Croker et al. 2021/2024), then BHs observed merging at
  higher redshift have had less time to grow.
- At fixed formation history, the mean log source mass of a volume-limited sample should fall with z:
  Δ log10 M = −k log10[(1 + z_hi)/(1 + z_lo)] between bins (exact if formation precedes both bins; an upper bound on the
  shift otherwise).
- No coupling (k = 0) predicts no shift.
- This tests the black-hole half of CFG775/779's dark-energy link, independently of the framework.

## Declared statistic
- **Sample.** Every event with non-null `mass_1_source`, `redshift`, `luminosity_distance` and `network_matched_filter_snr`,
  with `p_astro` ≥ 0.5 where given, and both source masses ≥ 3 M☉ (BBH).
- **Per-event horizon.** d_h,i = d_L,i × SNR_i / 8. This is an empirical, orientation-included horizon from the event's own
  SNR (inspiral scaling SNR ∝ 1/d_L at fixed detector-frame signal).
- **Volume-limited cut.** Keep events with d_h,i ≥ D_cut, where D_cut = the d_L of the median-redshift event of the sample.
  Restrict to d_L,i ≤ D_cut. Within that sphere every kept event's analogue would have been detectable throughout, so the
  kept set is volume-limited in mass.
- **Bins.** Split the kept events at their median z: low and high.
- **Measure.** Δ = mean log10 m1,src(high) − mean log10 m1,src(low), with a bootstrap 68% interval (10⁴ resamples,
  seed 783).
- **Predictions:** k = 0 gives Δ = 0; k = 3 gives Δ_k3 = −3 log10[(1 + z̄_hi)/(1 + z̄_lo)] using the bins' mean redshifts.

## Classes
- **k = 3 EXCLUDED** if Δ − Δ_k3 ≥ 3σ (σ = bootstrap half-width).
- **k = 0 EXCLUDED** if |Δ| ≥ 3σ.
- Otherwise NOT DIAGNOSTIC.
- Also report the k favoured, k̂ = −Δ / log10[(1 + z̄_hi)/(1 + z̄_lo)], with its interval.

## Controls
- K1 (selection tooth): without the volume-limited cut (all events), Δ_raw is reported. Selection should push it positive
  (heavier at high z). If the cut leaves Δ unchanged from Δ_raw, the cut is not doing anything; this is flagged.
- K2 (power): N_kept ≥ 20, and σ < |Δ_k3|/2. Otherwise NOT DIAGNOSTIC.
- MUTATE (CFG783_MUTATE=1): inject k = 3 by scaling each kept event's mass by [(1 + z̄)/(1 + z_i)]³. The statistic must
  then recover k̂ ≈ 3 within its interval.

## Hand estimate
- Expect N_kept ~ 30–60, z̄ ~ 0.15 vs 0.35.
- Δ_k3 ≈ −3 log10(1.35/1.15) ≈ −0.21 dex; σ ≈ 0.05–0.08.
- Likely outcome: k = 3 tested at about 3σ, uncertain direction.

## Disclosures
- The empirical horizon ignores the frequency-dependence of SNR for heavy BBHs (merger/ringdown). That bias is reported as
  a limitation.
- Formation-time spread: the k = 3 prediction is an upper bound on the shift if many BHs form between the bins.
- This is not framework-native gravity. It tests a dark-energy-source hypothesis.
- κ fitted; not theory closed.

## Machine
- Run after the relaunched T1x has finished. It is a seconds-long script.
