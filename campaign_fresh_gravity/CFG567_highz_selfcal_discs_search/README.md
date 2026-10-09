# CFG567: no z ~ 1.5-3 disc qualifies for a self-calibrated a0(z) test (0 of 15 primary-band candidates; 0 of 60 census rows). CENSUS ONLY: NONE

**Ledger line:** CFG567 census: 0 of 60 rows (15 in z 1.5-3) pass CFG385 span + resolved gas + resolved stars; every gas-mapped disc stops at g_obs >= 1.9 a0 (massive discs need R_out 25-57 kpc to go deep); Q1 binds, not Q3; no score. kappa fitted; not theory closed.

Criteria `FROZEN_CRITERIA.md`, committed alone first (46a2029f7). Script `cfg567_census.py` (seconds), census table `cfg567_census.csv`, RC41 parse check `cfg567_parse_rc41.py`, fetches `FETCH_LOG.md`. No a0 is scored, so nothing here bears on the framework vs LCDM.

## Verdict
**CENSUS ONLY: NONE.** Qualifying discs (Q1-Q6, z 1.5-3.0): **0**. Report band z 3-4.5: **0**. Qualified-but-not-obtainable: 0. No disc anywhere passes Q1 (the CFG385 span).

**Why (structural, one line):** every disc with a resolved gas map (CO / [CI] / [CII]) at these redshifts is massive (V 240-530 km/s). For flat V, reaching the deep point g_obs <= 0.55 a0 needs R_out >= 25 kpc at 200 km/s, 39 kpc at 250, 57 kpc at 300 (19-44 kpc if the threshold is set at y = 0.3 exactly). Gas tracers stop at 4-17 kpc. The discs that DO go deep (KURVS, KDS, RC41's low-V Halpha discs) have no gas map and usually no inner Newtonian point. This repeats CFG386 (z 1.5-2.7, on disk) and CFG268 (z 2.5-4) with the 2022-2026 literature added.

## Census (closest rows; full table in the CSV)
| row | disc | z | tracer | outer g_obs / a0 (low footing) | lacks |
|---|---|---|---|---|---|
| G10 / G5 | RC41 COS3_22796 / GS4_13143 | in 0.67-2.45 | Halpha | 0.48 / 0.52 (provisional: vc(Re) at R_out) | no gas map (scaling relations); inner point unknown, likely fails (V >= 156 km/s needed at the ~2 kpc PSF HWHM) |
| A6 / A7 / A5 | NOEMA3D G4_17555 / G4_37375 / GN4_32842 | 1.54 / 1.63 / 1.52 | CO NOEMA, resolved | ~1.9 / ~2.2 / ~3.3 (R_out ASSUMED 3 Re, generous) | never deep; cubes and profiles not public |
| A4 | SDSS J0901 (lensed) | 2.26 | CO ~600 pc + Halpha | ~4.7 (curve stops at ~1 Re) | outer curve; image-plane model only |
| A2 | zC-400569 | 2.24 | Halpha AO + CO | ~3.0 (R 0.68-7.43 kpc, V 254) | never deep |
| A1 | ALPAKA-13 COSMOS 3182 | 2.10 | [CI] + JWST | y 13.7 at R_ext (CFG272) | never deep; ~2 beams per side |
| R1 / R2 | ADF22.1 / Big Wheel | 3.09 / ~3 | [CII]/CO + JWST | ~6.9 / ~2.1 | massive giant discs |
| M* | MSA-3D six discs at z 1.51-1.68 | | NIRSpec Halpha | not tabulated | no gas map (t_depl x SFR); curves figure-only |
| S1-S3 | KMOS3D 192, KURVS 22, SINS AO 38 | | Halpha | | CFG386 / CFG280: no span, no gas |

Near-misses (>= 3 of Q1-Q5): A1-A8, R1, R2, S4. All fail Q1. Nine of them (A1, A4-A8, R1, R2, S4) fail ONLY Q1 among Q1/Q3/Q4/Q5: they have resolved gas and resolved stars but never reach the deep regime. A2 and A3 (Lelli+23) also lack a tabulated gas profile.

## Controls
- **C1 PASS:** a KURVS-type synthetic row (deep outer, inner at 2.2 a0) fails Q1, matching CFG386.
- **C2 FAILED, kept:** the frozen 0.55 a0 outer threshold is 13.5% (P2) / 29% (nu_mono, exp-RAR) stricter than y = 0.3 (0.62 / 0.71 a0); 0.55 a0 is y ~ 0.2. The inner threshold agrees (1-4%). The labelled sensitivity run at 0.711 a0 also gives **0** qualifying.
- **MUTATE (Q3 relaxed): NOT DETECTED, exit 0.** The qualifying count stays 0 (and the no-FAIL count stays 0), because Q1 binds for every gas-mapped disc and the Halpha-only discs fail Q1, Q5 or Q6 as well. As in CFG475, this shows the verdict does not rest on the gas rule. Disclosed, not repaired.
- RC41 rows were re-parsed from the PDF text: `cfg567_parse_rc41.py` gives 37 of 41 rows (rows 38-41 lost to a page break, not in the census) and 0 mismatches.

## Reading
- The CFG385 test cannot run on existing published z ~ 1.5-3 data. The binding gap is **kinematic reach at low mass**, not the gas maps: gas-mapped discs are too massive to go deep inside their gas extent.
- Nothing here measures a0. CFG565's sign test (LCDM-feedback rises x2-5, the framework ~0.8-0.87) stays untested at these redshifts.

## Cheapest path to 10 discs (observing / fetch specification)
1. **Targets:** z ~ 1.5-2.5 rotation-dominated discs with V_flat ~ 120-180 km/s (log M* ~ 9.8-10.4). Deep needs R_out ~ 10-19 kpc (frozen) or 8-15 kpc (y = 0.3); inner needs V >= 110 km/s at 1 kpc (>= 78 at 0.5 kpc), so the PSF HWHM must be <= 1 kpc (0.12"; JWST/NIRSpec IFU or ERIS/MAVIS AO).
2. **Kinematics:** NIRSpec IFU Halpha for the inner 0.5-3 kpc, plus ultra-deep KMOS/ERIS outer curves to 3-5 R_e (KURVS depth). The cheapest starting list is the KURVS rotation-dominated discs and the RC41 low-V discs (COS3_22796, GS4_13143, zC_405501, U3_05138, GS4_03228): their outer points already reach about 0.5-0.7 a0, so they need an inner JWST/AO anchor plus a gas map.
3. **Gas:** ALMA CO(3-2) or CO(4-3) (or dust continuum at a declared conversion) at <= 0.25" to R_out. At these masses (L'_CO ~ 10^9.3-9.8) this is several hours per disc at z ~ 1.5; it is the expensive step.
4. **Stars:** JWST/NIRCam pixel-SED mass maps (already public in COSMOS/GOODS/EGS for most such fields).
5. **Before any proposal:** check the ALMA archive for CO in the 5 RC41 low-V discs and the KURVS rotators (a metadata query, no download), and check whether the MSA-3D authors will release per-radius curves for its six z >= 1.5 discs. Both need the owner's go.

kappa = 1/2 FITTED. Footings 9.3603e-11 / 1.1312e-10. No dark-matter particle; the cold mass is required and its amount is free. Not theory closed.
