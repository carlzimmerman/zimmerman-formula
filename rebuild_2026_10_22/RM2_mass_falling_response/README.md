# RM2_mass_falling_response: CELLS CLEAR [NOISE-LIMITED]. Six of 75 cells clear the five gates, all at f_hi 0 or 0.2, so the map asks for almost no response above lg M_b about 10. A requirement, not a rule, and it contradicts LC1's measured response unless a process removes it

Criteria: `FROZEN_CRITERIA.md` (75364f3b50), `AMENDMENTS.md` A1, both committed before any graded cell. `rm2.py`, `rm2_tail_add.py`, `rm2_read.py`, `rm2.out`, `rm2_RUN_results.json`. RM1's path, NR2 MEDIAN, EM1. lg M_c, f_hi, δ are FITTED. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

| lg M_c, f_hi, δ | Υ A/B | rms | tilt A/B | Groups Z | LT A/B | Υ by V_flat |
|---|---|---|---|---|---|---|
| 9.5, 0, +0.05 | 0.59/0.60 | 0.0693 | +0.02/+0.02 | +1.00 | +0.090/+0.084 | 0.46 0.72 0.89 0.57 0.59 0.77 |
| 9.5, 0, +0.10 | 0.58/0.58 | 0.0731 | −0.06/−0.05 | +0.53 | +0.065/+0.059 | 0.43 0.64 0.85 0.57 0.59 0.76 |
| 9.5, 0.2, +0.05 | 0.52/0.53 | 0.0670 | +0.07/+0.08 | +1.01 | +0.090/+0.084 | 0.46 0.64 0.75 0.49 0.55 0.69 |
| 9.5, 0.2, +0.10 | 0.51/0.52 | 0.0712 | +0.03/+0.03 | +0.53 | +0.065/+0.059 | 0.43 0.59 0.73 0.49 0.54 0.69 |
| 10.0, 0, +0.05 | 0.52/0.53 | 0.0693 | −0.11/−0.12 | +1.00 | +0.090/+0.084 | 0.46 0.52 0.68 0.57 0.59 0.77 |
| 10.0, 0, +0.10 | 0.51/0.51 | 0.0734 | −0.13/−0.13 | +0.53 | +0.065/+0.059 | 0.43 0.47 0.65 0.57 0.59 0.76 |

No cell at f_hi 0.4 or above clears, and none at lg M_c 10.5.

## The three costs the criteria required
- **Clusters:** at f_hi 0 or 0.2, 12 of 15, bad G-IN-Mall, G-IN-all, G-MID-T3; X-COP −0.160, −0.148. Worse than full response's 14 and −0.097. Clusters sit at f_hi by this rule. A separate rule keeping them at f 1 would be another posit.
- **Bins:** 250–400 km/s at 0.69–0.77; 150–200 at 0.49–0.57; 100–150 km/s runs high at 0.65–0.89 in place of the old trough.
- **LC1:** every clearing f_hi is below 0.54, the low end of LC1's 0.872 [0.54, 1.07], for a live smooth disc, gravity only, no bars, no feedback. So gravity alone doesn't supply this. ER1, PG1 and DR9 find one coupling won't deliver it. Hydro is out of this machine's scope, so this stays an unclosed requirement.

## Limits
Three fitted numbers on a 75-cell grid, with six cells clearing is a fit, not a test. Lensing, the Milky Way and DiskMass aren't graded. UR3's reading stands: those weigh inner cold mass. Nothing here touches G-OUT-M3 on measured gas or T. Band runs on NR2 not done: [NOISE-LIMITED] per NR2's band.

My expectation on record: cells clear at a cost in keys, below LC1's range. Held. I put them near lg M_c 10, f_hi 0.2–0.4: they came lower, and at 9.5 too.

Checks: K1 f_hi 1 equals NR3's `EM1|blum`. K2 M_b range lg 6.30 to 14.92 including clusters; the criteria's 10⁶–10¹³ was for SPARC, the read's limit is 16 for that reason. K3 true. Read rerun byte-identical. MUTATE f → 1 − f (A1): K1 FAIL, exit 1.

κ = ½ FITTED. Not theory closed.
