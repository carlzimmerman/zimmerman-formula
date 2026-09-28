# CFG18 — FG001's satellites with their infall baryons

Script: `CFG18_satellite_infall_gas.py`, about 1 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. With no infall gas, FG001's H4 comes back, and H1 fails (rc = 1).

**This is a robustness test of FG001's exploratory H8, not a blind test.** H8's outcome was known before this lane was written, and it is reproduced below as a control.

## The question

FG001's class A says an accreted satellite keeps the cold component it carried at infall. FG001's committed H4 nonetheless scored satellites with their *current* baryons: stars only, because ram pressure has since removed their gas. The M31 LVD dwarfs then sat at +0.116 / +0.096 dex (2.6 / 2.2σ), FG001's one failed satellite gate.

FG001's H8 estimated the infall gas from Local Volume field dwarfs, but:
- it used HI detections only, which biases the estimate gas-rich;
- it extrapolated to every mass.

## The method (declared before the first run)

- **Calibration set:** 42 LVD field dwarfs with M_V and HI information, 32 detections and 10 upper limits, log M_* 4.98–9.65. M_* = 2.0 L_V (FG001's Υ_V); gas = 1.33 M_HI.
- **Draws:** each satellite inside that range draws its infall gas-to-star ratio from its 5 nearest calibration dwarfs in log M_*.
- **Non-detections:** counted as zero gas (conservative for FG001; the headline) or at their upper limit (reported).
- **Below the calibrated range:** no infall gas (reionisation fossils). The nearest-neighbour draw is reported as an alternative.
- **Infall baryons:** M_* + max(current gas, drawn gas).
- **Realizations:** 2000.
- FG001's committed machinery is exec'd read-only.

## Results

| check | result |
|---|---|
| C1: FG001's committed H4 isolated medians and H8 offsets | reproduced exactly |
| **H1:** MW classical and M31 LVD within 2σ, both footings (non-detections as zero) | **pass** |

The median offset log(σ_obs/σ_isolated), with the 68% range over realizations:

| sample | stars only (FG001 H4) | infall gas, non-detections = 0 | infall gas, non-detections at limit |
|---|---|---|---|
| MW classical dSphs (14/14 in range) | +0.067 / +0.047 | **+0.025 (0.4σ) / +0.005 (0.1σ)** | +0.009 / −0.010 |
| M31 LVD (29/34 in range) | +0.116 (2.6σ) / +0.096 (2.2σ) | **+0.078 (1.6σ) / +0.060 (1.2σ)** | +0.059 (1.2σ) / +0.040 (0.8σ) |
| M31 Collins+13 (12/14 in range) | +0.226 (2.5σ) / +0.207 (2.3σ) | +0.125 (1.4σ) / +0.105 (1.2σ) | +0.102 / +0.082 |
| MW ultra-faints (1/31 in range) | +0.355 (8.0σ) / +0.334 | +0.339 (7.4σ) / +0.319 | nearest-neighbour draw below range: +0.224 (3.6σ) |

Each cell gives canonical / alt.

## Standing

**FG001's own infall logic removes its M31 tension.**
- With infall gas drawn from real field dwarfs of the same stellar mass, taking the conservative bracket and propagating the spread, the M31 LVD dwarfs move to 1.6σ / 1.2σ and Collins to 1.4σ / 1.2σ.
- H4's failure came from scoring accreted satellites with their stripped present-day baryons, which contradicts FG001's own class-A statement.

**What stays:**
- **The MW ultra-faints still fail at 7–8σ.** The infall-gas account cannot help them: they sit below the calibrated mass range and were quenched before they could hold gas. Known systematics for ultra-faints, binaries and tides, are not modelled here. The external-field rival fails them harder, at 13σ.
- **The harness** (FG097) still reads FG001's committed H4. With this lane, FG001's M31 gates (G5, G6) would pass on both footings. The harness re-score is not done here.

Nothing here says the theory is closed.
