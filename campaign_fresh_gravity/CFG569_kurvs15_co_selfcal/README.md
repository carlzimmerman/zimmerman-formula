# CFG569: KURVS-15 archival ALMA CO -> measured gas shape -> self-calibrated a0. NOT POSSIBLE: CO NOT DETECTED (and the rotation curve does not span the needed range)

**Ledger line:** CFG569 KURVS-15 (z 1.613) archival ALMA CO(2-1)/(5-4): not detected in any cube (Ibar B3 S/N +0.74, Molina -0.76, B6 -0.20); 3-sigma mu_mol < 4.0 (alpha_CO 4.36) / < 0.93 (1.0); no gas shape -> no a0 number; Halpha curve outside the PSF spans g_obs only x2.0 (need x6.4). One galaxy; not an a0(z) test.

Criteria: `FROZEN_CRITERIA.md`, committed alone first (83f1d4ba0), before any cube was downloaded or read. Script `cfg569_kurvs15.py` (~16 s). Data: the owner-approved minimum set (6.6 GB), `FETCH_LOG.md`.

## Result
- **CO(2-1), Ibar Band 3 (primary total flux; 2.65" x 1.73" beam):** peak at KURVS-15 +0.059 Jy km/s in +-300 km/s, sigma 0.080 (MAD of 200 off-source positions) -> **S/N +0.74, not detected.** +-200 km/s: S/N +1.21. 2"-aperture variant +0.033.
- **CO(2-1), Molina Band 3 (0.16" x 0.13"):** 1.2"-aperture sum -0.147, sigma 0.194 -> S/N -0.76, not detected. So no resolved gas shape exists.
- **CO(5-4), Ibar Band 6 (1.50" x 0.89"):** S/N -0.20 (reported only).
- **Limits (3 sigma, S < 0.239 Jy km/s, r21 0.77, He included):** M_mol < 4.7e10 Msun, **mu_mol < 4.04** at alpha_CO 4.36; < 1.1e10, mu_mol < 0.93 at alpha_CO 1.0. As CFG163's power row predicted (mu_mol >~ 5.5 needed for a detection), this is non-diagnostic for the gas prior; the dust limit (CFG163, mu < 1.90 nominal) stays the tighter one.
- **No a0 number.** Per the frozen ladder (and the CFG400/CFG475 lesson) the self-calibrated fit needs a MEASURED gas shape; none exists, so the fit was not run. Nothing is said about a0(z = 1.6) vs the framework (~0.95-1.0), flat, LCDM-feedback (~1.7-1.9) or H(z) (~2.4).
- **The span would also have failed (a data property, no a0 involved):** outside the KURVS PSF half-width (R >= 2.5 kpc; 16 points to 9.2 kpc) g_obs varies only x2.01 (P0) / x1.20 (B10 pressure), against the required x6.4. Including the beam-smeared inner points (R >= 0.5 kpc): x4.40 / x1.35. Stars-only y = g_bar/a0 runs 0.91 -> 0.25 (canonical; alt 0.75 -> 0.20), never reaching y >= 3. **KURVS-15 does not reach the Newtonian regime with seeing-limited Halpha; even a CO detection would have given a SPAN-LIMITED demonstration only.** One galaxy cannot decide a0(z) in any case.

## Controls (all kept)
- R1: the authors' model curve at R_max / sin 38 deg = 113.2 vs 112.2 km/s (0.9%); table row unchanged. PASS.
- H1-H4 (spectral coverage, beam class, pb = 1.000 at the source, Jy/beam) PASS for all three cubes.
- N1 line-free windows at the source position: Ibar B3 median z -0.36, std 0.58 (n 7); B6 -0.52 / 0.71 (n 2); Molina +0.66 / 0.81 (n 6). PASS.
- **C_disc FAILED (kept):** the thin-disc ring-sum solver gives 0.968 / 0.982 / 0.993 of the Freeman exponential at 2/4/8 kpc (3% tolerance missed at 2 kpc). Cause diagnosed after the run: the declared z0 = 0.05 kpc softening (z0 = 0.01 gives 0.987); not changed. The solver is used only by the gas-shape fit, which did not run, so no reported number depends on it. Main and MUTATE_A therefore exit 1.
- MUTATE_B (0.5 Jy km/s line injected into the Ibar B3 mom0): reads DETECTED at S/N 6.90, recovered 1.000 (exact by linearity: it tests the pipeline, not the noise). PASS.
- MUTATE_A (measured gas -> exponential): **could not run, no measured gas shape exists** (disclosed per the plan). The CFG400 shape lesson therefore remains untested here.

## Disclosures
- Run 1 had a sign error in the disc solver (C_disc read -0.968...); fixed to the inward magnitude. Run 1's span line was printed as a check; changed to a RESULT line (it is a result, not a control). No CO number changed between runs.
- Cube frames are LSRK; z_Halpha's frame differs by < 30 km/s, small against the +-300 km/s window.
- The Ibar B3 statistic is the peak pixel; for a ~1" source in a 2.1" (geometric mean) beam it underestimates by <~10%.
- The record has no KURVS-15 PA; the frozen PA-from-CO rule never ran.

## Owner items
- None needed for this lane. What would make KURVS-15 (or any z ~ 1.6 disc) usable: deeper CO (mu_mol ~ 1 needs ~4x deeper than the archive) AND AO/JWST inner kinematics reaching y >~ 3. Both are new observations, not archive.
- The 6.6 GB of cubes sit in campaign_fresh_gravity/_external_data/cfg569/ (git-ignored; plus ~6 GB of gunzipped pb files); deleting them is the owner's call.

kappa = 1/2 fitted; both footings carried; the cold mass is still required; nothing here favours the framework over LCDM.
