# BR1_bars_sparc: BARS DON'T SEPARATE. At 150–250 km/s, RC3's barred discs read the same Υ under the response as unbarred ones. Not an exclusion: small n, optical classes, half the bin at the Υ floor

Criteria: `FROZEN_CRITERIA.md` (b4176c98a3), committed alone before any class was fetched. `br1.py`, `br1_inc.py`, `br1.out`, `br1_inc.out`, `br1_matched.json`. RC3 family, VizieR VII/155 via the CfA mirror, `_external_data/br1_bars/rc3.tsv`, sha256 starts 847c5aa486ba9413, untracked; classes as matched are committed. TP1's per-galaxy Υ. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

**Primary, 150–250 km/s, SB vs SA, Υ_Blum:** SB n 7, median 0.33; SA n 15, median 0.32. Gap +0.010 [−0.080, +0.060], one-sided rank p 0.61. **Frozen label: BARS DON'T SEPARATE**, as expected on record.

| Reported | Barred | Other | Gap [95 %] | p |
|---|---|---|---|---|
| SB + SAB vs SA, Υ_Blum | 18, 0.30 | 15, 0.32 | −0.015 [−0.080, +0.045] | 0.79 |
| SB vs SA + SAB, Υ_Blum | 7, 0.33 | 26, 0.30 | +0.030 [−0.060, +0.060] | 0.44 |
| SB vs SA, Υ_off | 7, 0.63 | 15, 0.59 | +0.040 [−0.190, +0.160] | 0.48 |
| 150–200 | 4, 0.30 | 8, 0.35 | −0.045 | 0.86 |
| 200–250 | 3, 0.36 | 7, 0.30 | +0.060 | 0.29 |
| 100–400 at fixed lg V_flat | n 41 | | rank +0.08 | 0.50 |

The need is about +0.20 (0.30 to 0.50). Medians at the floor can't exclude a shift hidden below 0.30: 29 % of SB against 47 % of SA sit there, which leans the right way and isn't significant.

## Limits
- **Optical classes, and edge-on discs.** Bars are hard to see at high inclination, so some SA flags are wrong: NGC 891 is SA here. A mix like that would hide an effect. `br1_inc.out` repeats at i < 75°, reported after the result.
- Coverage: 33 of 43 at 150–250 km/s have a family; the 10 without are dropped.
- **S4G's mid-IR classes were not obtained:** the mirror's transfer failed. This is the better catalogue and could be tried again.
- A flag isn't bar strength, and adiabatic Υ here is not a dynamical torque calculation.

## Checks
K1 TP1's values read directly. **K2 as frozen FAILED, and the fault was mine:** I wrote that NGC 3198 and NGC 2403 aren't SB in RC3 from memory. RC3 reads NGC 3198 .SBT5.. and NGC 2403 .SXS6.. (SAB). The parser is right, spot checks NGC 1300 SB, NGC 7331 SA. No class or line was changed. MUTATE shuffled flags: p quartiles 0.22, 0.52, 0.77, about uniform.
