# KT27_local_rule_alt_grade: KT26's local filter rule FAILS ON ALT at the dwarfs (14/24, Fornax lost); Cassini passes by 470x, SPARC passes narrowly (d rms +0.0031, median +0.044). Canonical fails dwarfs and SPARC too, on top of KT26's MW fail

Criteria: `FROZEN_CRITERIA.md` (19603e63ef), alone first, confirmed landed. `kt27.py`, `kt27.out`, `kt27.json`, `kt27.time`; `kt27_MUTATE.out`, `kt27_MUTATE.json` (logs are gitignored; the .out files hold the same lines). No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K839. 7 minutes, 0.20 GB.

The rule ξ_loc = |g|² / (|d|g|/dr| g*), g* = a0/κ, applied row-wise (width taken at the radius evaluated), |g| the unfiltered board-law field.

| test | canonical | alt |
|---|---|---|
| T1 Cassini Q2 / ceiling | 0.0005, PASS | **0.0021, PASS** |
| T2 dwarfs (line ≥ 15/24; plain 15, r_M/2 15) | 14/24, FAIL | **14/24, FAIL** |
| T3 SPARC d rms / median | +0.0129 / +0.073, FAIL | **+0.0031 / +0.044, PASS** |
| **Label** | **already FAILS (MW, KT26); also dwarfs, SPARC** | **LOCAL RULE FAILS ON ALT: dwarfs** |

## Reading
- **The dwarf fail is Fornax, and it has a mechanism.** In the MW's external field |g| is nearly constant across a satellite, so d|g|/dr is small and ξ_loc gets large: 2.6 kpc for Fornax (24x r_M/2), 10²-10⁴ x for Draco, Sextans, Carina, Ursa Minor, Canes Venatici. The satellite's own mass is smoothed away and its phantom goes with it, so Fornax predicts 5.1 km/s against 11.7 observed. Isolated and M31 dwarfs (no external field in KT15's model) get ξ_loc ≈ 2.4 x r_M/2 and keep passing. All seven MW satellites fail; r_M/2 keeps Fornax.
- **It's a one-galaxy miss on a frozen line, not a margin call.** The line was 15/24 and it's 14/24. I'm not moving it. And the direction is structural, not noise: the local rule makes the external-field effect much stronger than plain QUMOND for every MW satellite.
- **Cassini passes easily on both** (ξ_loc ≥ 0.92 r_M everywhere, minimum near 0.4 r_M), which fixes KT25's alt Cassini fail. **SPARC on alt passes narrowly**: the median +0.044 is close to the 0.05 line, and inner points lose phantom (inner median -0.006 → +0.050). Canonical fails SPARC (+0.0129).
- **So no footing survives the local rule.** Canonical fails the MW, dwarfs and SPARC; alt fails the dwarfs. KT25's global ξ = r_M/2 on canonical is still the only filter form that survives all four, and it isn't local.

## As hard as a fail
- |g| is the unfiltered field, not iterated, and the external field is added in quadrature; a vector treatment could change ξ_loc inside satellites, though the constant-field cause would remain.
- Row-wise smoothing doesn't conserve mass (SPARC total ratio 0.36-1.13, median 0.81); printed, not graded, as frozen.
- KT26's MW was a one-value screen, not re-run row-wise here.

## Checks
R1: constant r_M/2 reproduces KT25 (Cassini 0.4806 / 1.057, dwarfs 15/24, SPARC +0.0021 / -0.0006). R2: point-mass deep limit 1.00001. MUTATE (ν = 1): Cassini Q2 0, SPARC fails (rms 0.573), as expected. 0 failed checks.
