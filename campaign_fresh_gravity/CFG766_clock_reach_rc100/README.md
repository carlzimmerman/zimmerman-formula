# CFG766: pre-flight — RC100 can reach the clock-diagnostic regime (REACHABLE), but its outer curves are not in the record

**Label: R1 REACHABLE (both footings). MUTATE bites (exit 1).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (c1d71c3be), 2026-10-13. Block CFG760–769.
- **Script:** `python3 cfg766.py` (instant) → `cfg766.out`, `cfg766_results.json`. Input: the record's CORRECTED RC100 table (read
  only).
- κ = ½ FITTED; not "theory closed". A pre-flight: no clock verdict.

## Result
Radius at which y = g_bar/a₀ falls to 0.17 (the CFG765 requirement), in units of R_e:

| footing | min | 16th pct | median | ≤ 3 R_e | ≤ 5 R_e |
|---|---|---|---|---|---|
| canonical | 1.29 | 2.68 | 4.51 | **21** | 61 |
| alt | 1.17 | 2.44 | 4.10 | **28** | 70 |

## Reading
1. **A decisive high-z clock test is possible in principle.** About 20–30 RC100 discs (z 0.6–2.5) reach the regime where the orbital
   clock (full law) and the universal clock (25–75% at 1-Gyr baryons) differ by ≥ 0.30 dex, within ~3 R_e.
2. **What it needs that the record lacks.**
   - The per-galaxy outer rotation curves at 2–3 R_e. The record has only Table 3 values at R_e (data_assembly/rc100_provenance).
   - Baryon masses, gas included, good to ≲ 0.15 dex. This is the known limit of the high-z fronts (CFG213–229).
   - A baryon-age estimate per galaxy.
3. Point-mass baryons are used for R_need. Beyond ~3 R_e the enclosed disc mass is close to the total, so this is a fair
   approximation, and it is favourable at smaller radii.

## Data availability check (2026-10-14; web look-ups are PROVISIONAL summaries, not tables read by a script)
- RC100 per-galaxy curves: no machine-readable release was found. The RotCurves package (arXiv:2601.08348;
  github.com/nestoramit/RotCurves) holds code only.
- MSA-3D (JWST/NIRSpec, arXiv:2606.27853): 30 galaxies at z 0.5–1.7, 19 reach ≳ 2 R_e. The tables give V_rot only at R_e; gas is
  given only as a sample range M_mol/M★ ≈ 0.2–4.5 (≫ 0.15 dex); per-galaxy figures are in an MPE supplementary PDF.
- **Standing:** no public sample decides the formation clocks today. Per-galaxy outer curves plus gas masses would be needed.
