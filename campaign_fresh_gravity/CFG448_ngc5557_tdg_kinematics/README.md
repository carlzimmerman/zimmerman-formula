# CFG448: archival resolved kinematics of the NGC 5557 tidal dwarfs

## Verdict: DATA NOT AVAILABLE. No archival product can score E1, E2 or E3; the fork stays open

- **The only resolved HI data are the ATLAS3D WSRT cube (Serra et al. 2012).** The lane extracted it from the public
  23 GB release by HTTP range reads.
  - Beam: 39.2" × 35.9", which is 7.4 × 6.8 kpc. Channels: 8.25 km/s. Noise: 0.48 mJy/beam.
  - E1's HI is **unresolved**. Its intensity FWHM along the velocity gradient is 36.6", smaller than the 39.0" beam, so
    the beam-deconvolved size is 0. Its detected mask edge spans only 2.07 beams.
  - The 3-channel detection rule finds emission at ±0.5 beam only, never at ±1 to ±2 beams (U3 FAIL).
  - No inclination exists (U4 FAIL).
  - E2 fails U1, U3 and U4. E3 fails U3 and U4, and its authors doubt it is bound.
- **Nothing else exists.**

  | archive | what was found |
  |---|---|
  | NRAO VLA/EVLA (TAP) | 67 rows within 0.3 deg. None is HI spectral-line data. The 4 rows that cover 1405 MHz are 30 s and 170 s continuum snapshots. |
  | Apertif DR1/DR2 | Field not covered (nearest beam 1.94 deg away) |
  | ESO (MUSE, any instrument; raw and products) | 0 rows |
  | Keck KCWI | 0 rows |
  | FASHI (FAST) | Detects E1, E2 and E3, but the beam is 2.9' (33 kpc), so they are unresolved |
  | Literature 2014-2026 (arXiv API, 77 citing papers, web search) | No new kinematics |
  | Gemini, CADC/CFHT-SITELLE | **Not searched**: Gemini requires a login, and the CADC TAP was unreachable. Both are owner items. |

- **Indicative only (not a verdict).** E1's WSRT velocity gradient is 16.8 km/s across the detected extent, a
  half-amplitude of 8.4 km/s. It is beam-smeared and possibly tail streaming. The FASHI W50/2 is 14.4 km/s.
  - Without an inclination, every model is allowed. To match V_rot sin i = 8.4 km/s you need:
    - Newton: sin i = 0.49;
    - law+EFE: sin i = 0.29 (canonical) or 0.28 (alt);
    - isolated law: sin i = 0.18 (canonical) or 0.17 (alt).
  - The data favour neither branch.

**What it adds to F1 (reported; U5 measured).** E1's HI flux is now measured instead of bracketed:
- WSRT: 0.403 Jy km/s, so M_HI = 1.43e8 Msun (1.19 × M_*).
- FASHI: 0.765 Jy km/s, so M_HI = 2.71e8 (2.26 × M_*). This is an upper value, because the FAST beam also contains
  tail gas.

At R = 2 R_e = 4.6 kpc, in the host's field:

| | M_HI source | Newton (km/s) | law+EFE (km/s, canonical / alt) | isolated law (km/s, canonical / alt) |
|---|---|---|---|---|
| WSRT | measured | 17.3 ± 2.1 | 29.4 / 30.6 | 46.3 / 48.4 |
| FASHI | upper value | 21.6 ± 2.0 | 35.9 / 37.3 | 52.3 / 54.6 |

- The smallest Newton-to-law+EFE gap is 12.1 km/s. A 3σ split therefore still needs a total V_c error of about 4 km/s
  or less.
- The prediction errors are dominated by E1's stellar mass (Duc et al. 2014: 1.2 ± 0.7 × 10^8 Msun). Even a perfect
  4 km/s V_c equal to Newton reads NON-DISCRIMINATING with today's M_* error (Δχ² +5.5 / +6.4 at the WSRT mass). A
  better M_* (SED with near-IR photometry) is part of the requirement.

**Observation needed.** These are planning numbers; the instrument constants come from general knowledge and must be
checked with the official exposure calculators:
- Resolution: HI at a beam of about 12" (so R_out = 24.5" spans 2 beams) and channels of 5 km/s or less.
- Sensitivity: rms ≈ 0.18 mJy/beam per 5 km/s channel. This assumes E1's WSRT flux fills R_out uniformly, with half
  the mean column at the outer points (1.3e20 cm^-2) and a peak S/N of 5.
- Time on source: **VLA C-config about 90 h, or uGMRT about 80 h.**
- Also needed: an inclination from the deep MegaCam / Legacy Surveys images, and a better M_*.
- MUSE and MeerKAT see Dec +36.5 only at elevations of about 29° and 23°.
- IFU H-alpha (SITELLE, or KCWI's red arm) is secondary: E1's H-alpha is weak and patchy.
- E1 alone is a single-object reading. CFG441's frozen verdict still needs N_A ≥ 3 old tidal TDGs.

Standing: κ = ½ is FITTED. Both footings are run. No dark-matter particle is added; the framework's cold-fluid mass is
still required wherever the law needs it. Nothing here says the data favour the framework over ΛCDM.

## What was run

- `FROZEN_CRITERIA.md` was committed alone first (bc9b42594).
- `cfg448_fetch_wsrt_cube.py` walks the tar headers of the public ATLAS3D `allcubes.tar` by range requests and fetches
  only `NGC5557_cube.fits.gz` (215 MB, git-ignored in `_external_data/cfg448/`). It needs only network access, about
  4 min.
- `cfg448_ngc5557_tdg.py` runs the controls, the archive census from the committed query files, U1-U5 on the cube, the
  F1 update, the indicative numbers, the decision, the observation spec and the rule test. It takes about 20 s.
  - Main run: `.out` / `_results.json`, rc 0.
  - MUTATE run: `_MUTATE.out` / `_MUTATE_results.json`, rc 0 (see controls).
- Fetches: `FETCH_LOG.md` (URL, bytes, sha256). Query results, including the empty ones, are in `fetched/`.

## Controls (kept as they fell)

| control | result |
|---|---|
| C1: reproduce CFG441 F1 (10 numbers) within 0.1 km/s | PASS, max dev 0.048 km/s |
| C2: nu_mono import, footings | PASS (deep-limit ratio 1.0050) |
| Flux cross-check: WSRT mom0 vs cube within the mask (E1) | PASS: 0.403 vs 0.405 Jy km/s |
| WSRT vs FASHI flux for E1 | FASHI is 1.90 × WSRT, consistent with tail gas in the 33-kpc FAST beam and/or flux the interferometer resolves out |
| **MUTATE: synthetic V_c := V_N with a 4 km/s error must read SETTLING at every mass, on both footings** | **FAILED at one point, kept** (rc 0). Detected at the 3 × M_* end and at both measured masses. Not detected at the 1 × M_* end, where canonical Δχ² = +8.4 < 9 (alt +10.1). 4 km/s sits just above the 3.9 km/s that end needs. |
| Reported variant: the same rule with a 3 km/s error | SETTLING at every mass (Δχ² +15.0 to +31.8). The rule works when the error is small enough. |
| Rule reach (reported): V_c = V_law+EFE → LAW at every mass with 4 km/s | FAIL at the 1 × M_* end (−8.4 / −8.3), for the same reason |

## Departures and disclosures

- **D1. U1 reading.** "Extent" is taken as the detected mask-edge extent along the velocity-gradient axis, which is the
  generous reading. E1 passes it at 2.07 beams, but its intensity FWHM is below the beam, so it is unresolved. The
  verdict does not depend on U1: U3 and U4 fail for every object.
- **D2. U2.** U2 uses the header channel width (8.25 km/s). The effective resolution after any Hanning smoothing was
  not verified. The verdict is unaffected.
- **D3. U3 positions.** Positions are set along the gradient axis at 0.5-beam steps. "Independent" means at least 1 beam
  apart. Both choices were made in the script, not frozen.
- **D4. FASHI.** FASHI was not in the frozen archive list. It is added as a measured upper M_HI and as an unresolved
  width; it never enters a score.
- **D5. Prediction errors.** The F1 update uses Duc et al. 2014's M_* error (±0.7e8), not the generic 0.15 dex, because
  the published error is larger and real.
- **D6. Observation spec.** The SEFDs (VLA 420 Jy, uGMRT 400 Jy), weighting factors (1.3 / 1.4), efficiencies, the
  uniform-column assumption and the peak S/N of 5 are planning assumptions. Treat the hour estimates as ±50%.
- **D7. Gemini and CADC not searched.** These two archives could not be searched (login required / endpoint
  unreachable). Duc et al. 2014's GMOS data are known to be long-slit with ±30 km/s errors.
