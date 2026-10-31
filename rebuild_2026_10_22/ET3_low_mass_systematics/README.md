# ET3_low_mass_systematics: the low-mass rise is ROBUST to the systematics tested and they cannot fake its size; the floor stays MIXED

Criteria: `FROZEN_CRITERIA.md` (8d55654b06, committed alone). Numbers: `et3.out`, `et3_results.json`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## Frozen verdicts
- **Rise: ROBUST.** ρ > 0 at p < 0.01 under all six single changes and 20 of 20 inclination and distance draws. WORST (30″ cut, σ 12, Inc ≥ 45°, Q 1; 38 galaxies) still reads RISE, but only just: ρ +0.415, p 0.0099.
- **Floor: canonical STABLE MIXED; alt VARIATION-DEPENDENT** (some MC draws REJECTED). No variation gives FLOOR HOLDS.
- **Forward from a flat floor: PARTIAL**, the worst case over footings. One case of eight, alt with 30″ and σ 12, is significant (ρ +0.321, p 0.0075). None is FAKED.

| Case | 20–60 | 60–100 | 100–150 | ρ |
|---|---|---|---|---|
| Real, base | 70.2 | 107.7 | 157.5 | +0.556 |
| Real, P12 | 87.0 [77, 129] | 118.4 | 165.2 [143, 190] | +0.462 |
| Real, WORST | 94.3 [75, 147] | 112.9 | 165.2 [143, 190] | +0.415 |
| Flat canonical, 30″ + σ 12 | 82.9 | 93.4 | 93.4 | +0.275 |
| Flat alt, 30″ + σ 12 | 102.7 | 112.9 | 118.4 | +0.321 |

## How this reads
1. Systematics can tilt a flat floor in the observed direction, but by about ×1.13–1.15 across the bins, against ×2.2 in the real curves.
2. **The two ends behave differently.** The 20–60 deficit is the soft part: the upper-bound pressure correction lifts its interval to [77, 129], which contains both floors. The 100–150 excess is the harder part: it stays above canonical's floor in every case, and moves the wrong way for pressure to explain it. Under B30 its interval [124, 182] contains alt's 129.
3. This does not reject the floor: no case reaches two bins on one side on the real curves except some alt MC draws. It does not identify a mechanism. Baryon error remains: one Υ for all galaxies. V_flat and baryon mass correlate, so an Υ trend with mass was not tested here and is the next open door, as is core shape.

## Limits
Beams bracketed, not per galaxy. 1D smoothing, not a 3D beam, so NOT FAKED is conditional. No warps or non-circular motions. P cases can overcorrect curves already corrected. K4 rests on 5 inner points of one galaxy. K3b: 95.9 % of galaxies refit within a grid step.

## Checks
K1 equals ET2 per galaxy, K2 on-grid plants exact, K3 1.8e-15, K3b, K4: all pass. MUTATE planted S ∝ V_flat reads ρ +0.993. Two crashes before any output was read (a NumPy name, JSON types) were fixed; neither touched a number.
