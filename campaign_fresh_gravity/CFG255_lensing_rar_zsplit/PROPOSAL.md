# CFG255 — does the weak-lensing RAR evolve with lens redshift? A differential test that cancels the common-mode baryon calibration (PROPOSAL; the orchestrator's lane, 2026-09-30)

**Status: a proposal only. Nothing is fetched and no z-split lensing number has been looked at.** Each phase freezes its own criteria before it runs. κ = ½ is FITTED. ΛCDM has no a₀; its line is an effective-a₀ PROXY.

## Why this lane
Every high-z a₀ lane on the record is limited by the ABSOLUTE baryon calibration: CFG223/224/228/229, CFG238 and the gas-anchor scoping 7d8d3b350 (no dynamics-independent anchor reaches 0.1 dex at z ≥ 1.6). A split BY LENS REDSHIFT within one lensing survey, with one stellar-mass method, cancels any calibration offset common to both bins. It leaves only the calibration DRIFT with z, which at z < 1 with consistent photometry is plausibly smaller than the drift at z > 1.6. That plausibility is exactly what phase 1 must quantify, not assume.

## The signal (deep-MOND regime, where galaxy–galaxy lensing at large radius sits)
g_obs ∝ √(g_bar a₀), so the shift at fixed g_bar is Δlog g_obs = ½ Δlog a₀.
- **FLAT (the framework's distinctive law):** 0.
- **The rival a₀ ∝ H(z)** (flat ΛCDM background, Ω_m = 0.3):

| lens bins (z) | a₀ ratio | Δlog g_obs (dex) |
|---|---|---|
| 0.15 vs 0.35 | 1.115 | 0.024 |
| 0.2 vs 0.5 | 1.186 | 0.037 |
| 0.2 vs 0.7 | 1.336 | 0.063 |
| 0.3 vs 1.0 | 1.51 | 0.090 |

- **The ΛCDM PROXY** comes from the evolution of the stellar-to-halo relation. It is to be computed in phase 1c and is not assumed to be zero.

## Phases (each with frozen criteria and a MUTATE control)
1. **Phase 1a, data scoping (data chat; no downloads):** which public products give the lensing ESD or RAR in lens-redshift bins with one consistent stellar-mass method and covariance? Candidates to check: Brouwer+2021's KiDS-1000 released products; the KiDS-bright lens catalogue with the KiDS-1000 shear catalogue; DES Y3; HSC Y3; KiDS-Legacy; Mistele+2024. For each: the lens-z range, N, the isolation criterion, whether it has a z-split, and its size.
2. **Phase 1b, blind pre-flight (a calculation session):**
   - using mocks only and no z-split data, forecast the precision on Δlog g_obs between bins for each candidate survey;
   - include a declared stellar-mass drift budget with z (bands, SED templates, IMF, photo-z scatter);
   - include the isolation-criterion change with depth and the two-halo term;
   - decide POSSIBLE or NOT POSSIBLE for FLAT against H(z), and FLAT against the ΛCDM proxy, BEFORE any z-split number is read;
   - the forecast statistic must see shared systematics (the CFG219 lesson): total scatter plus a control that can fail.
3. **Phase 1c, the ΛCDM proxy (independent session):** what a ΛCDM stellar-to-halo relation (published, not tuned here) predicts for the lensing RAR at fixed g_bar across the same bins.
4. **Phase 2:** the measurement, only if 1b says POSSIBLE and only after the owner's go for any download.

## What would count
- A measured shift consistent with 0 at a precision that excludes the rival's value is FLAT-consistent. It is not a detection of the framework, and ΛCDM must be scored by the same rule.
- A robust shift at the rival's value is a KILL of the flat law in this regime.
- NOT POSSIBLE at phase 1b is a valid and likely outcome, and it is recorded as such.
