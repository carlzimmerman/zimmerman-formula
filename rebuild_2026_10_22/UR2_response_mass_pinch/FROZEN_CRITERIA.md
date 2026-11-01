# UR2_response_mass_pinch: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** UR1's best row, EM1 + adiabatic response, fails on Υ 0.35. EM1 was fitted with no response, so with response the halos should be lighter. How much lighter does Υ ask for, and does lensing, which weighs the halo outside the region the response moves, allow it?

This does not add a number to the theory: EM1's line is already fitted. The offset is an inversion, as in SL2. A value found here is a requirement, **FITTED**, never derived.

**Disclosed before the freeze. Not blind.**
- UR1, Blumenthal: EM1 Υ 0.35/0.35, rms 0.0671, tilt +0.16, groups Z +1.50, LITTLE THINGS +0.105. FAIR200 Υ 0.72/0.73, rms 0.0931, tilt +0.75, groups +3.79, LITTLE THINGS +0.423. X76 puts fair share 0.2–0.3 dex below EM1.
- BL1, A at EM1's masses, Δ log M200 for A = 1, canonical, 2σ: blue +0.03 (−0.10, +0.14); red +0.32 (+0.25, +0.38); all +0.26 (+0.21, +0.30).
- SL1 and SL2 are read; neither enters here.

**Expectation on record, mine.** Υ reaches 0.50 near δ −0.1, close to blue's lower edge, so the mass gate alone may not decide it. Tilt gets worse as δ falls, since UR1's two rows bracket it at +0.16 and +0.75, and I expect tilt or LITTLE THINGS to fail at δ_Υ. No pass expected.

## Runs
UR1's path and table unchanged: NR1 PRIMARY's η, f★ 0.034, canonical, both backgrounds.
lg M200 = 11.18 + 0.90 (lg M_b − 10) + δ, with the record's a, b per background. δ from −0.50 to +0.20, step 0.05, 15 values, one global offset, b unchanged.
Modes: Blumenthal (primary), Gnedin (LC1's measured response is close to it; alternate), off (comparator).

Clusters use fair share and don't read this map, so keys and X-COP stay at UR1's values for each mode, quoted, not rerun: Blumenthal 14/15, G-IN-Mall −2.05, X-COP −0.097, rms 0.146. **So no row can pass as a whole here, whatever SPARC does.** That's stated now.

## Read
1. **δ_Υ:** largest δ on the grid, by linear interpolation of median Υ, with Υ ≥ 0.50 on both backgrounds. Also by V_flat bin (six bins), Υ = 0.50 crossing per bin, reported.
2. **At δ_Υ, on the grid value at or below it:** rms ≤ 0.110, |tilt| ≤ 0.15, groups Z verdict CONSISTENT, |LITTLE THINGS median E| ≤ 0.10.
3. **Lensing line, not regraded:** blue's 2σ lower bound, δ = −0.10, since blue is the population SPARC samples. Red and all are quoted beside it. Lensing's A is read across from BL1, on FC1's core; the response moves inner mass and BL1's window is 6 outer points, so this is an approximation. Whether it holds isn't tested here.

## Labels (primary, Blumenthal)
- **PINCHED:** δ_Υ < −0.10, or no δ on the grid reaches Υ 0.50. SPARC + response asks for halos lighter than blue lensing allows.
- **MASS ROOM, GATES FAIL:** δ_Υ ≥ −0.10 and a gate in 2 fails; name it.
- **SPARC SIDE CLEARS, KEYS AND X-COP STILL FAIL:** δ_Υ ≥ −0.10 and all of 2 hold. This is not a pass; next would be KiDS's own grade, Local Group, MW and a cluster fix.

## Checks
K1 δ 0, off: NR1 PRIMARY's Υ, rms, |d| ≤ 10⁻⁶. K2 δ 0, Blumenthal: UR1's EM1 row, Υ, rms, tilt, groups, LITTLE THINGS, |d| ≤ 10⁻⁶. K3 Υ monotonic in δ on Blumenthal, else say so. MUTATE: M_b × 2 in the response only moves δ_Υ.

Inherits NR1's ANCHOR-DEPENDENT low masses; NR2 unread, so rerun when it lands. One thread, nice 15, under 1 GB, beside NR2. κ = ½ FITTED, unused; no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
