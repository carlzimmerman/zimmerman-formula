# PG1_sloshing_coupling: WRONG SHAPE. The sloshing factor doesn't fix ER1's ordering: when 150–200 km/s reaches Υ 0.50, tilt is about +0.6, and no ε passes the line and the tilt gate

Criteria: `FROZEN_CRITERIA.md` (ffe29d775b), committed alone first. `pg1.py`, `pg1_x.py`, `pg1_read.py`, `pg1.out`, `pg1_results.json`. ER1's path, native shape, ng 64-era shapes, not on NR2. ε FITTED. κ = ½ FITTED, unused; no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

| ε | Υ A/B | rms | tilt | line | Υ by V_flat |
|---|---|---|---|---|---|
| 0.1 | 0.46/0.43 | 0.0732 | +0.31 | no | 0.55 0.71 0.59 0.34 0.41 0.53 |
| 0.285, the text's | 0.48/0.46 | 0.0746 | +0.33 | no | 0.38 0.77 0.78 **0.40** 0.42 0.53 |
| 0.46 | 0.53/0.51 | 0.0762 | **+0.56** | yes | 0.80 1.18 0.84 0.43 0.43 0.54 |
| 0.7 | 0.60/0.55 | 0.0778 | +0.53 | yes | 0.85 1.05 0.93 0.45 0.45 0.55 |
| 1.0 | 0.68/0.59 | 0.0789 | +0.64 | yes | 0.68 1.19 0.97 **0.52** 0.46 0.56 |

The text's claim, 150–200 km/s at Υ 0.50 by ε 0.285, misses: 0.40 there, and 0.52 needs ε 1, all of E_SN. Dwarfs still move first: 60–100 km/s is at 1.18 by ε 0.46.

**Why.** The factor's medians by bin are 0.006, 0.014, 0.026, 0.035, 0.023, 0.024. It does favour 150–200, by about 2.5–6 ×, but that's on the native shape, and less than the text's 5.4 × between 20–60 and 150–200 only at one end. It doesn't offset the 4–8 × lower cost of undoing a dwarf. Non-monotonic bin 20–60 at low ε comes from per-galaxy thresholds on 12 systems.

**Delivery.** Every ε reaching the line is at least 0.46, about 150 × CM1's gravity-only channel of about 0.3 % of E_SN. Citation of Pontzen & Governato 2012 unverified here.

My expectation on record held. Groups read ABOVE LAW on this path at every ε, as on ER1's.

Checks: K1 ε 10⁻¹² equals ER1 f 0.872, 0. K2 ε 10³ equals ER1 f 0, 0. K3 factor 0.0004 to 0.10. Read rerun byte-identical. MUTATE factor × 0.01 at 0.285: Υ falls to 0.44, f 0.872's value.

κ = ½ FITTED. Not theory closed.
