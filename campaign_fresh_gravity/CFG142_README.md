# CFG142 — does the dust continuum exclude the gas CFG141's P2 model needs? The KURVS-CDFS discs in GOODS-ALMA 1.1 mm

- **Criteria:** frozen in `CFG142_FROZEN_CRITERIA.md` (ae867cd1d), with its pre-data table (`CFG142_requirement_fluxes.py`, `.out`), before any catalogue was matched.
- **Data:** the data chat's cross-match (b25d5c902, README fix fef5d64ed; positions e08195747). It gives the placement on the mosaic, the catalogue matches, the survey's stated frequency (265.0 GHz) and the catalogue paper's thresholds. It is read-only here.
- **Script:** `CFG142_goodsalma_gas_test.py`; seconds per run.
- **Runs:**
  - The main run passes both load-bearing controls (C-0, C1) and exits 0. The headline verdict is reported.
  - MUTATE=1 sets the scored disc's flux to the requirement. The disc no longer excludes it, as required; exit 0.
  - MUTATE=2 makes the scored disc a zero-flux detection. It excludes the requirement, as required; exit 0. The sample-level FAIL is not applicable with one scored disc, as frozen.
  - The two controls move the scored disc's verdict in opposite directions, so the evaluator can go both ways.

## Bottom line

**As frozen: NON-DIAGNOSTIC for the sample. Only one of the ten discs lies within the survey's reach.**

- **No detections.** None of the ten rotation-supported discs is detected: no catalogue source lies within 1.5″ of any of them.
- **Coverage.**
  - Six discs are inside the mosaic under both orientation readings: 9, 11, 13, 15, 16 and 17. Of these, 13 and 17 are within 0.5′ of the edge.
  - Discs 3, 7 and 21 depend on the reading, and disc 8 is outside.
- **Only KURVS-11 is powered.**
  - Its generous-end requirement is 0.528 mJy at 265 GHz. The limit, 4.4σ at the survey-average rms, is 0.301 mJy, so the requirement is above it.
  - The other covered discs need 0.04–0.16 mJy, below the limit, so their non-detections say nothing.
- **KURVS-11 excludes the P2 requirement, as an approximate point-source limit.**
  - Its dust-traced ISM is below 0.72 M* at the nominal calibration (Scoville, 25 K), and below 1.44 M* with the ×2 gas-to-dust factor. P2 needs about 4 M*.
  - **This holds only if its dust is compact against the 0.45″ beam.** The catalogue is built on peak S/N.
    - If the beam's peak holds half the total flux or less, the effective total-flux limit (≥ 0.60 mJy) is above the requirement. The disc is then unpowered at every threshold except the prior-based 3.5σ at exactly one half.
    - The dust size is not measured.
  - The rms is the survey average: no noise map at the position was available.
- **CFG141's P2 residuals for KURVS-11 at its gas bound** (anchor-corrected, one galaxy, so the errors are large):
  - Δ′_flat = +0.26 at μ = 0.72 and +0.18 at μ = 1.44;
  - Δ′_H = +0.13 and +0.06;
  - at the P2 requirement, μ = 4, they would be −0.01 and −0.11.
- **Context, not scored.** Two KURVS galaxies outside the ten, KURVS-12 (log M* 11.52) and KURVS-22 (11.12), are detected, at 0.74 and 1.36 mJy.
  - Their dust-traced μ is 0.26 and 1.19 at the nominal calibration, or 0.82 and 3.8 at the generous end.
  - So dust-traced gas fractions from well below to near the P2 level occur in this survey's KURVS galaxies.

## Reading

- **As frozen:** NON-DIAGNOSTIC. At this depth the dust continuum can test the P2 requirement in one of the ten discs, and only for compact dust.
- **What the one powered disc indicates.** KURVS-11 has dust-traced gas well below what P2 needs, as a point-source approximation.
  - Taken at face value, that points at the P2 dispersion model over-correcting, as CFG141's correction flagged. It does not point at either reading of a₀.
  - It is an indication, not a measurement: the rms is approximate and the dust size is unknown.
- **What would settle it:**
  - the GOODS-ALMA noise maps at the KURVS positions (local rms and a size-matched limit);
  - CO or deeper dust continuum for KURVS-11;
  - HI, which dust does not trace.

## Controls

- **C-0:** the conversion reproduces the committed pre-data table at 272.5 GHz, to 7e-4 (3-digit print).
- **C1:** CFG141's pipeline, exec'd read-only, reproduces its committed per-disc P2 Δ_flat and Δ_H at μ = 0.67 for all ten discs (2-decimal print).
- **C-a / C-b:** Scoville's coefficient and Γ₀. These were run in the pre-data script, whose MUTATE fails C-b.

## Disclosures

- **N_det = 4.4.** This is the catalogue paper's stated blind threshold (σ_p for 100% purity in the combined map). The frozen text says "as the catalogue paper states it", and the paper states several thresholds. The others (5.2 high-res, 3.5 prior-based, and the faintest blind-table flux of 0.49 mJy) are reported as variants. KURVS-11 is powered under all four as a point source.
- **Placement:** "covered" means inside the mosaic under both of the data chat's orientation readings. The frozen text named 9, 11 and 16 plus any disc placed inside.
- **ν_obs = 265.0 GHz,** the survey's stated tuning, as frozen. The pre-data table used c/1.1 mm (272.5 GHz), which lowers S_req by about 9%.
- **MUTATE, operationalised per disc.** The frozen text gives the sample-level expectations. With one scored disc, each pinned control is checked on that disc. Each MUTATE run exits 0 when it behaves as required.
- **The first MUTATE=1 run is kept** (`CFG142_goodsalma_gas_test_MUTATE1_firstrun.out` / `.json`).
  - It failed C1 because the exec'd CFG141/CFG140 pipeline reads the same MUTATE variable, so it doubled the KURVS velocities.
  - The variable is now cleared around the exec in every mode. The main run was unaffected; MUTATE=2 does not collide.

## Untested (declared)

- the local rms at each position;
- the dust sizes;
- dust-poor atomic gas;
- gas-to-dust below the ×2 bracket;
- T_d other than 25 K (35 K is reported);
- the P2 model itself.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Provenance correction: the KURVS outer velocity is a model value (appended 2026-09-29; the text above is unchanged)

- **The KURVS outer velocity this lane uses is the authors' fitted exponential-disc MODEL evaluated at R_max, not the last measured data point.** It is Table B1 col 3, read as `v_at_last_point_kms` through CFG140's loader.
- **How this was established.** The data chat's digitisation of the paper's figures (5e8617c81, `data_assembly/arxiv_tables/kurvs_rc_profiles/`) includes a control file (`kurvs_rc_control_vs_table.csv`). In it, the authors' model curve at R_max divided by sin i_SFR equals the tabulated velocity to about 1% for all ten discs (for example KURVS-3: 208.6 against 209.8 km/s; KURVS-15: 113.2 against 112.2). I checked this from the control file alone.
- **Where the record says otherwise.** Where this lane or CFG140 calls the velocity "measured" or "the velocity at the last observed point", read "the fitted model at R_max". The authors deprojected it with i_SFR; CFG140 uses i* only in its inclination-error term.
- **The a₀(z) numbers here are therefore model-velocity numbers.** The measured outer markers can differ from the model: an indicative, unreconciled probe found −15% to +10% for seven discs.
- **A re-run with the measured outer markers** is planned as a new frozen lane (proposed CFG189), after CFG184. The measured markers have not been read in the meantime.
