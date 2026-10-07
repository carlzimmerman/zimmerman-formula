# CFG441: old tidal dwarf galaxies selected by tidal origin

## Verdict: NON-DISCRIMINATING. No old TDG with usable kinematics exists (N_A = 0)

| sample | footing | N | chi^2 Newton | chi^2 law+EFE (nu_mono, nominal host) | Delta | reading |
|---|---|---|---|---|---|---|
| **Tier A: old TDGs (the verdict)** | canonical 9.3603e-11 | **0** | — | — | — | **NON-DISCRIMINATING** (N < 3) |
| **Tier A** | alt 1.1312e-10 | **0** | — | — | — | **NON-DISCRIMINATING** (N < 3) |
| Tier B: tidal origin + kinematics, young (< 1 orbit), reported only | canonical | 7 | 1.10 | 34.02 | +32.9 | would read SETTLING; not a verdict |
| Tier B, reported only | alt | 7 | 1.10 | 40.29 | +39.2 | would read SETTLING; not a verdict |
| MUTATE (V_obs := V_Newton on Tier B) | canonical / alt | 7 | 0.00 | 40.73 / 47.66 | +40.7 / +47.7 | SETTLING SUPPORTED, as required (rc = 1) |

- **The answer to the question is a precise "not yet observed".** The literature search found no galaxy that has all
  three: independent evidence of tidal origin, a formation age of at least 1 Gyr, and kinematics good enough for a
  dynamical mass.
- The best old candidate is **NGC 5557-E1** (Duc et al. 2014).
  - Its tidal origin is secure: it sits in a 200-kpc stellar tidal tail and has near-solar O/H (12+log(O/H) = 8.6).
  - Its age is about 4 Gyr (SED fit), which passes the age rule.
  - It fails on kinematics. Its long-slit H-alpha gradients carry ±30 km/s errors, and the authors say their data
    cannot give a dynamical mass.
  - Its companion E2 has only an HI centroid velocity. E3 may not be bound.
- Every TDG that does have kinematics is young. Each has turned 0.2 to 0.6 of an orbit:
  - the CFG7 six (Lelli et al. 2015), with t_form 0.35 to 0.75 Gyr;
  - Arp 72c (Portilla-Narvaez et al. 2026), 0.32 Gyr old.
- The "older" ALFALFA candidates (Gray et al. 2023: AGC 229398, AGC 333576) fail the tidal-origin rule. Their tidal
  origin rests on being near a massive galaxy and on low dark-matter content, and dark-matter content is the quantity
  under test. Counting them would be circular.
- The full candidate list is in `data/candidates.csv`: 16 entries with the S0 to S3 outcome and the reason for each.

**What it says about the fork (CFG391).** The test leaves both branches open:
- Branch A: the satellite planes are not tidal debris.
- Branch B: old TDGs carry the full law boost.

The settling model's TDG prediction is confirmed only where it is weakest: young, non-equilibrium discs (< 1 orbit).
The reported Tier B numbers make that young-TDG result stronger, not new:
- Arp 72c joins the CFG7 six on the Newtonian side.
- At the nominal host mass (CFG7 quoted the host mass most favourable to the law), the law+EFE is worse by
  Delta chi^2 = +33 (canonical) and +39 (alt).
- It stays worse at host mass ×2 (+24 / +29) and with a 10% equilibrium systematic (+30 / +36).

None of this addresses an old TDG.

**What observation would decide it.** Forecast F1 (`cfg441_old_tdgs.out`) is a forecast, not a measurement:
- Setup: NGC 5557-E1 at 2 R_e = 4.6 kpc, in its host's field (M_host = 0.6 L_K = 1.09e11 Msun, D_p = 68.9 kpc).
  Its untabulated HI mass is bracketed between 1 and 3 × M_*.
- Predictions:
  - Newton: V_c = 16 to 24 km/s.
  - The law+EFE: 28 to 41 km/s.
  - The isolated law: 45 to 58 km/s.
- The smallest gap is 11.6 km/s. One object therefore needs a total V_c error of about 4 km/s or less to split the
  models at 3 sigma.
- What that takes: resolved HI (VLA/MeerKAT/uGMRT-class, about 5 km/s channels) or IFU H-alpha (MUSE/KCWI) kinematics
  of E1 and E2, a measured HI mass, and an inclination.
- The frozen rule needs N ≥ 3. That means at least one more old, tidally confirmed TDG with equal data, for example:
  - MATLAS / ATLAS3D shell-galaxy debris dwarfs with metallicity, followed up in deep HI;
  - WALLABY / MeerKAT detections in old-merger debris.

Standing: κ = ½ is FITTED. Both footings are run throughout. No dark-matter particle is added; the framework's
cold-fluid mass is still required wherever the law needs it. Nothing here says the data favour the framework over
ΛCDM.

## What was run

- `FROZEN_CRITERIA.md` was committed alone first (6f2023e4c), before any script, table reading or number.
- `cfg441_old_tdgs.py` is the single script. It uses the committed `nu_mono` and footings from `CFG4_common.py` and
  CFG7's 1-D EFE form.
  - Main run: `cfg441_old_tdgs.out` / `cfg441_old_tdgs_results.json` (rc 0).
  - MUTATE run: `cfg441_old_tdgs_MUTATE.out` / `_MUTATE_results.json` (rc 1, as required).
- Data:
  - `data/candidates.csv`: selection with reasons.
  - `data/tierB_arp72c.csv`: Arp 72c, transcribed from the arXiv LaTeX tables.
  - `data/PROVENANCE.md`.
  - The CFG7 six are read from `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`.
- Fetches: `FETCH_LOG.md`, with URL, bytes and sha256. The arXiv tarballs are git-ignored in
  `_external_data/cfg441/`.

## Controls (kept as they fell)

| control | result |
|---|---|
| C1: CFG7 young-TDG Newton chi^2 1.09 (6) within 0.01; nu_mono+EFE (most favourable host) 10.55 / 13.08 within 0.05 | PASS: 1.0950; 10.547 / 13.075 |
| C2: nu_mono import (deep limit) and the footings | PASS: 1.0050 |
| S3 audit (reported): every Tier B object < 1 orbit | PASS: 0.20 to 0.60 orbits |
| MUTATE: V_obs := V_N must read SETTLING SUPPORTED on both footings | detected (Delta +40.7 / +47.7), rc = 1 |

## Departures and disclosures

- **D1.** Arp 72c is scored with the isolated law, because no host mass or projected distance was compiled for it.
  This is Tier B, reported only. The isolated law is the less favourable reading for it.
- **D2.** Arp 72c's asymmetric V_c error (+9/−6) is symmetrised to 7.5 km/s.
- **D3.** Forecast F1 was not in the frozen criteria. It is reported only.
  - Duc et al. 2014 does not tabulate E1's HI mass; it says only that the "HI to visible mass" gas fraction is above
    50%. F1 therefore brackets M_HI between 1 and 3 × M_*.
  - The host NGC 5557 comes from ATLAS3D (M_K −24.87, D 38.8 Mpc) and Sesame.
- **D4.** Tier C (NGC 1052-DF2/DF4) is quoted from the committed CFG7 FG001 record, as frozen:
  - DF2: Newton 0.0 sigma, law+EFE 3.0 sigma.
  - DF4: Newton 0.8 sigma, law+EFE 1.5 sigma.

  arXiv 2606.30718 (2026) now proposes a merger-TDG (tidal) origin for them, as an alternative to the bullet-dwarf
  collision. The frozen rule keeps them in Tier C. Promoting them would still give N = 2 < 3, so the verdict cannot
  change. They lean Newtonian in the record, and their distances are contested.
- **D5.** Some exclusions rest on abstracts or search summaries, not tables: AGC 208457 (its authors call it young),
  the MATLAS candidates, HCG 16-LSB1 and the Kaviraj et al. 2012 photometric sample. None is reported to pass both the
  age rule and the orbit rule. The arXiv HTML/abstract summaries supplied no number to this lane.
