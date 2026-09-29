# CFG142 — does the dust continuum exclude the gas CFG141's P2 model needs? The KURVS-CDFS discs in GOODS-ALMA. FROZEN CRITERIA

Written 2026-09-29, before any catalogue cross-match. The data chat has committed the KURVS positions and their placement on the GOODS-ALMA footprint (e08195747). It has matched no source catalogue and read no map. This file and its pre-data table (`CFG142_requirement_fluxes.py`, `.out`) are committed before it does. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

- **What CFG141 found** (corrected a843be430): under the P2 dispersion model, both readings under-predict the outer accelerations of the ten rotation-supported KURVS discs unless these z ≈ 1.5 discs hold about 4 M* of cold gas.
  - The gas is unmeasured.
  - The requirement belongs to the P2 model, not to the framework, and it is nearly the same for either reading.
- **The data:** GOODS-ALMA 2.0 (1.1 mm; Gómez-Guijarro et al. 2022, arXiv:2106.13246) covers KURVS 9, 11 and 16 for any mosaic orientation, and seven more of the ten depending on the orientation.
- **The method:** dust continuum measures the dusty ISM mass (Scoville et al. 2016).
- **The question:** does the measured continuum exclude the flux that P2's gas requirement implies?

## The conversion (declared)

- **The formula:** M_ISM = 1.78 S_ν[mJy] (1+z)^−4.8 (ν_850/ν_obs)^3.8 (Γ_0/Γ_RJ) (d_L/Gpc)² × 10¹⁰ M☉.
  - Source: Scoville et al. 2016 (ApJ 820, 83): eq. A8 with α_850 = 6.7 × 10¹⁹ erg s⁻¹ Hz⁻¹ M☉⁻¹, and Γ_RJ = x/(eˣ − 1), x = hν_obs(1+z)/kT_d (eq. A4).
  - T_d = 25 K. Γ_0 = Γ_RJ(25 K, 850 μm, z = 0), computed the same way; it is 0.6994, and the paper quotes 0.71.
  - d_L is Planck18 at each galaxy's z_Hα.
  - ν_obs is the survey's stated frequency, or c/λ if only λ is stated. The pre-data table uses c/1.1 mm; the scoring recomputes with the same code.
- **The requirement flux, S_req:** the flux at μ_total = 4, CFG141's P2 requirement. It is scored at the **generous end**, which is the hardest to exclude:
  - the gas-to-dust ratio is doubled for sub-solar metallicity (×2), so only μ_dust = 2 is needed;
  - M* is set 0.2 dex below MAGPHYS.
  - Hence S_req,gen = S(μ_dust = 2) × 10^−0.2. The nominal end (×1, nominal M*, μ_dust = 4) is reported.
- **Pre-data values** at 272.5 GHz, generous / nominal:
  - KURVS 9: 0.157 / 0.498 mJy;
  - KURVS 11: 0.575 / 1.824 mJy;
  - KURVS 16: 0.172 / 0.546 mJy;
  - the other seven are in the `.out`.
  - The survey's average rms is 68.4 μJy/beam (data chat).

## The measurement per disc (declared)

- **Covered:** the disc lies inside the mosaic as the data chat places it. That means 9, 11 and 16, plus any orientation-dependent disc it places inside from the survey's own data or paper. A disc whose local rms exceeds twice the survey average (the mosaic edge) is reported but not scored.
- **Detected:** a catalogue source lies within 0.6″ of the KURVS position. Its catalogue flux and error are used; if a tapered-map flux is given, that one is used. A source 0.6–1.5″ away is reported and not used.
- **Not detected:** the limit is the catalogue's own detection threshold N_det (in σ, as the catalogue paper states it) times the rms at the position.
  - The rms is local if the data chat can report it. Otherwise it is the survey average, and the row is labelled APPROXIMATE.
  - A non-detection is not read as zero flux.
- **Powered:** a non-detected disc is powered only if S_req,gen > N_det × rms. Otherwise a non-detection there cannot exclude the requirement, and that disc is reported as unpowered. Detected discs are always scored.

## Checks

- **C-a / C-b (the conversion; already run in the pre-data script):**
  - Scoville's coefficient, 1.19 × 10²⁷ × 10⁻³ × 10⁶ / 6.7 × 10¹⁹ = 1.776 × 10¹⁰ against 1.78 × 10¹⁰ (1%): PASS.
  - Γ_0 = 0.6994 against the paper's 0.71 (2%): PASS.
  - The script's MUTATE (T_d × 2) fails C-b and exits 1.
- **C1 CONTROL:** CFG141's pipeline, exec'd read-only, reproduces CFG141's committed per-disc P2 Δ_flat and Δ_H at μ = 0.67 exactly. It supplies the R2 rows.
- **H1 [HEADLINE]:** the dust continuum does not exclude CFG141's P2 gas requirement in the scored covered discs. A disc excludes it if:
  - it is detected and S + 2σ_S < S_req,gen; or
  - it is not detected, powered, and S_req,gen > N_det × rms.
- **H1's verdict:**
  - H1 FAILS if at least two scored discs exclude the requirement and they are the majority of the scored discs.
  - H1 PASSES if none excludes it.
  - Anything else is MIXED. So is fewer than two scored discs: reported per disc, NON-DIAGNOSTIC for the sample.

## MUTATE (two pinned controls, since the direction of the result is unknown before the data)

- **MUTATE=1:** every scored disc's flux is set to S_req,gen with its measured error. H1 must PASS.
- **MUTATE=2:** every scored disc is set to a detection of zero flux with its error divided by 10. H1 must FAIL, provided at least two discs are scored.
- One of the two necessarily differs from the main run. Both must behave as stated, or the evaluator is broken. If fewer than two discs are scored, MUTATE=2 is reported as not applicable.

## Reported rows

- **R1:** per disc: placement, match (ID, separation), S ± σ or the limit, the rms (local or APPROXIMATE), powered or not, and μ_dust at ×1 and ×2 metallicity.
- **R2:** per scored disc: CFG141's P2 Δ_flat and Δ_H at μ_total = μ_dust × {1, 2}. With three discs these rows cannot separate the readings: the gap between them is about 0.15 dex, and the per-disc errors are about 0.2 dex.
- **R3:** the T_d = 35 K variant of R1.

## Readings (declared)

- **H1 PASS with detections at μ_dust ≥ 2:** the P2 requirement is met by dust-traced gas in those discs, and CFG141's P2 excess is explained by gas there. Flat against the rival stays NON-DIAGNOSTIC.
- **H1 PASS where only unpowered non-detections exist:** NON-DIAGNOSTIC.
- **H1 FAIL:** the dust-traced ISM falls short of the P2 requirement even at the generous end.
  - Under P2, both readings then under-predict these discs, unless the discs hold about 2 M* or more of dust-poor gas: HI beyond the dust, or gas at metallicity below the ×2 bracket.
  - That points at the P2 dispersion model before either law.
  - It is NOT evidence against either reading in particular.
- **Untested (declared):**
  - dust-poor atomic gas;
  - dust-to-gas below the ×2 bracket;
  - T_d other than 25 K and 35 K;
  - extended emission resolved out of the maps;
  - the P2 model itself.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
