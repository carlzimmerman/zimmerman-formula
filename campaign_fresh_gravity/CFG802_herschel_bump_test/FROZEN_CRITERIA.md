# CFG802 FROZEN CRITERIA: is CFG799's 3.2σ hint at 541.700 GHz real? (committed before any script)

**The hint.** CFG799 (cb5ec89cb) finds a = +20.5 ± 6.5 mK at 541.700 GHz:
- z = +3.17, with errors already inflated by √χ²_ν;
- Level-1 z = +0.03;
- scan maximum |z| = 4.45 at +38 MHz from 541.664.

The framework predicts no line. A real mirror line must:
- stay at fixed spacecraft-frame RF;
- be about the instrument width (≈1.1 MHz FWHM);
- appear in every independent subset of the data;
- not depend on any one target.

**Data.** CFG799's reduced data and pipeline, imported read-only. No new data. Target ν_h = 541.700 GHz, plus ν_s, the
scan peak 541.702 GHz, reported alongside.

## Tests at ν_h
- **T1, splits.** Split the stack into halves and test each:
  - H vs V polarisation;
  - early vs late (obsid median);
  - USB vs LSB;
  - line-rich targets (Orion, Sgr B2, IRC+10216, G34.26, W49, W51, NGC 6334, DR21, any 'hot core') vs the rest.

  **PERSISTS** if both halves have z ≥ 1.5 and agree, |Δa|/σ_Δ < 2, in every split.
- **T2, width.** Fit the stack with the Gaussian FWHM set to 1.14, 2, 4, 8 and 16 MHz. **NARROW** if z is largest at
  FWHM ≤ 2 MHz. BROAD otherwise, which points to a baseline or source feature, not a mirror line.
- **T3, leave-one-observation-out.** **NOT DRIVEN** if no single removal drops z below 2.
- **T4, look-elsewhere.** The fraction of 0.5 MHz scan steps within ±40 MHz that have |z| ≥ 3.17 (from CFG799's
  scan), and the trials-corrected p-value, using 161 steps with a declared effective-trials factor of 161/3 for
  correlated neighbours.

## Classes
- **HINT SURVIVES** if T1 PERSISTS, T2 NARROW and T3 NOT DRIVEN. Next step: obtain the 35 undownloaded scans.
- **HINT FADES** otherwise. Name which test kills it.

## Controls
- K1: re-running CFG799's stack at ν_h reproduces a = +20.5 ± 6.5 mK within 0.1 mK.
- MUTATE (separate output): inject a 1.14 MHz line of 3× the hint's amplitude at ν_h. It must give HINT SURVIVES.

κ fitted; not theory closed.
