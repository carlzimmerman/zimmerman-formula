# ET1_core_strength_needed: the L★ tension is not a measured feature; the failures are below the mass where it was thought to live

Criteria: `FROZEN_CRITERIA.md` (fb266e6788, committed alone). Numbers: `et1.out`, `et1_results.json`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## What was measured
The S = ρ₀r₀ each SPARC galaxy asks for at fixed Υ, with M200 from the EM1 relation. 123 galaxies pass the cuts, none censored at Υ 0.50. S_need is footing-free; footings enter only through the predictions.

| V_flat | n | lg M200 | S_need, M☉/pc² [95 %] | Floor can / alt | Converged rule P2 can / alt |
|---|---|---|---|---|---|
| 20–60 | 12 | 9.97 | 68.6 [51.6, 85.0] | 107 / 129 | 107 / 129 |
| 60–100 | 35 | 10.59 | 102.7 [81.0, 124.2] | 107 / 129 | 107 / 129 |
| 100–150 | 23 | 11.13 | 143.2 [118.4, 199.8] | 107 / 129 | 107 / 129 |
| 150–200 | 25 | 11.76 | 150.2 [97.9, 190.5] | 107 / 129 | 155 / 155 |
| 200–250 | 18 | 12.11 | 215.1 [136.6, 272.1] | 107 / 129 | 182 / 182 |
| 250–400 | 10 | 12.27 | 411.7 [181.6, 596.0] | 107 / 129 | 189 / 189 |

## Frozen verdicts (Υ 0.50)
- **L★ tension: SAMPLE-LEVEL**, both footings and at Υ 0.40 and 0.60. The 150–200 and 200–250 intervals overlap. The step LS1 showed between those bins is not resolved at this sample size.
- **Bulge: NO BULGE SIGNAL** at all three Υ. Bulged galaxies sit higher (195 vs 158) but the intervals overlap.
- **Mass trend, V_flat ≥ 150: NO TREND** (ρ −0.009, p 0.95).
- **External c_f 4 rule (P1): FAILS** on both footings: too little S at 200–400 km/s, and too much at the lowest masses.
- **Converged rule (P2): FAILS**, but only below 150 km/s. Canonical: 20–60 needs less, 100–150 needs more. Alt: 20–60 and 60–100 need less. **All three bins above 150 km/s contain P2 at Υ 0.50.**
- **Plateau:** canonical MIXED (below, inside, above), alt REJECTED.

## How this reads
1. Q1's "the sample needs η ≤ 21.2, the analogs want 26" compares a free-Υ sample median with a fixed-Υ subset. At one fixed Υ, the data above 150 km/s accept the converged rule, with wide intervals. This does **not** rescue the converged rule: the frozen SPARC line (median free-Υ ≥ 0.50, Υ 0.48) and the cluster keys still fail, and ET1 grades neither. It says the tension is not a resolved mass step.
2. The new information is at low mass. Below 150 km/s S_need is not flat: 68.6 → 102.7 → 143.2. The floor is the part of the rule that this measurement disputes. **Post-result, reported only:** Spearman of lg S_need on lg M200 is +0.60 (p 0.003) below lg M 10.5, and flat at +0.05 and −0.03 above that.

## What would undo this
**M200 is the weak link, and the mutation shows it.** With M200 × 0.5, the 20–60 interval becomes [60.9, 118.3], which contains canonical's 107 but not alt's 129. The canonical low-mass miss therefore depends on the M200 relation. 100–150 rises further at that mass, to 230. Since that run moved all galaxies by one factor, it is a stress test and does not measure a relation. Do not cite the sub-floor dwarf value as a floor failure until M200 at lg M < 10.5 has its own check.

Other limits: one Υ for all galaxies; a chosen core shape; distance and inclination errors ignored; 52 galaxies cut (Q, Inc, or no V_flat); intervals cover sample scatter only. Rotation curves ending near r₀ constrain S weakly.

## Checks
K1 (own S vs LS1 halo) 0.0, K2 (planted S 50/200/800 recovered within a step), K3 (mse direct) 8.7e-19: all pass. MUTATE M200 × 0.5: 200–250 median 215.1 → 286.0, bites.
