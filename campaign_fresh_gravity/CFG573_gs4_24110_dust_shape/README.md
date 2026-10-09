# CFG573: where GS4_24110's gas sits (public 0.13″ dust image)

Criteria eaee201fe (committed alone, before the download). Data: public 2015.1.00664.S continuum image of KMOS3DGS4-24110 (one 7.8 MB file plus its pb map; owner yes 10-09; deleted after the run).

## Frozen run: NOT DETECTED at 0.13″
- Peak S/N is 2.6 within 0.5″ (rms 39.8 μJy/beam). The frozen ≥ 5σ detection gate fails, so there is no size fit and no frozen Δ_v update.
- MUTATE (2″-shifted position): not detected → exit 1. This is **non-diagnostic**, because the true position isn't detected either.
- C1/C2 did not run (the script stops at the detection gate).

## Post-freeze (`cfg573_postfreeze.py`; reported only, never a verdict)
- **The non-detection is informative.** A point source with the expected total flux (Boogaard+20's 342 μJy at 1.2 mm, scaled to 265 GHz: 478 μJy) would sit at 12σ. So the dust is extended: **R_e,dust ≥ 0.6 kpc**.
- **Smoothing the image:**
  - the peak rises from 104 (0.14″) to 153 (0.3″), 200 (0.5″) and 269 μJy/beam (0.8″), each at only ~3σ;
  - read as one Gaussian of the expected total, that gives a dust FWHM of ~0.45–0.7″, **R_e,dust ≈ 1.8–2.9 kpc**;
  - so the dust is more compact than the stars and the Hα (7.39 kpc), and it is crude.
- **Effect on CFG572's Δ_v** (dust gas, M★ 10.89, canon footing): putting the gas at R_e 2–3 kpc instead of 7.4 kpc raises Δ_v by ~+0.10 for every model:

| gas R_e | a0 ∝ √ρ_DE | a0 ∝ H(z) | Newton |
|---|---|---|---|
| 7.4 kpc (CFG572 assumption) | +0.12 | +0.37 | −0.03 |
| 2.9 kpc | +0.22 | +0.47 | +0.08 |
| 2.0 kpc | +0.21 | +0.47 | +0.07 |

## What it means
- If the gas is as compact as the dust hints, **even plain Newton has slightly too many baryons** inside R_e. That points to the inputs (M★ too high, V_c too low, or the gas conversion) and not to any one model.
- The **gap between models doesn't move.** a0 ∝ H(z) stays ~0.25 dex worse than the framework under every shape.
- **The absolute level is the weak link.** One galaxy; dust shape = gas shape is assumed. The 2026-11-28 [CI](2-1) 0.09″ data (deeper, line-based) are the real gas-shape measurement.

κ = ½ fitted; the cold mass is still required.
