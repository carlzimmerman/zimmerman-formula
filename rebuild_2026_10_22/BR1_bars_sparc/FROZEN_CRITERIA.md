# BR1_bars_sparc: FROZEN CRITERIA (committed alone, before any classification is fetched or any number)

**Question.** Bars are the one named mechanism TP1 couldn't test. A bar torques the inner cold fluid, so barred galaxies should need less contraction. At the same V_flat, is Υ under the response higher in barred discs? A measured flag, no formula.

**Disclosed. Not blind to Υ.** TP1's per-galaxy Υ_Blum, Υ_off are on file; I haven't looked at any against a bar flag and have no flags yet. Bar fraction in discs is high and optical classes are partly subjective.

**Expectation on record, mine.** No detection. The within-bin spread is partly distance and inclination noise, n is small, and half the bin pins at Υ 0.30. If bars do anything it's a small positive shift. I expect BARS DON'T SEPARATE, which doesn't exclude them.

## Data
- **Primary:** RC3 family from VizieR VII/155: SA, SAB, SB, read from its morphological string. Uniform and independent of any halo or rotation curve. Raw file under `_external_data/`, untracked; matched table committed.
- **Alternate, if it can be fetched:** S4G's mid-IR classes (Buta+15, J/ApJS/217/32), closer to 3.6 µm. Reported beside; it doesn't change the label.
- Match by exact catalogue name after normalising spaces. No by-hand fixes of classes. Report the match rate by V_flat bin. Unmatched or no family: dropped.

**NOT** Hubble type, and nothing derived from V_obs.

## Test
TP1's per-galaxy values: UR1's path, NR1's η, EM1, δ 0, background A, Q ≤ 2, i ≥ 30°.
**Primary:** 150–250 km/s, SB against SA (SAB left out). One-sided: barred Υ_Blum higher. Rank test by permutation, 20,000 draws, seeded, since Υ is censored at 0.30. Also the fraction at the floor in each class.
**Reported:** SB + SAB against SA; Υ_off, same; fixed lg V_flat across 100–400 km/s; each of 150–200, 200–250; medians and n.

## Labels
- **BARS SEPARATE:** p < 0.05 one-sided, barred higher, and the median gap ≥ 0.05 in Υ.
- **BARS DON'T SEPARATE:** otherwise, with the interval on the median gap. If either class has n < 5 at 150–250: **UNDERPOWERED**, stated, whatever p says.
- A separation would be a correlation, not a mechanism, and barred and unbarred differ in other ways.
- **Wrong sign is reported too.**

## Checks
K1 values reproduce TP1's bin medians. K2 spot-check: NGC 3198 and NGC 2403 are not SB in RC3's family; NGC 1300-class SB strings parse as SB, on the parser. MUTATE: shuffled flags give p near uniform.

κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
