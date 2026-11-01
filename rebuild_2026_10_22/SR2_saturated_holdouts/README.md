# SR2_saturated_holdouts: HOLDOUTS FAIL. SR1's saturated rule doesn't reach DiskMass (r 1.212) and the Milky Way stays V+K ONLY; clusters don't move. On SPARC it reaches the line only at δ −0.10, where groups and LITTLE THINGS fail

Criteria: `FROZEN_CRITERIA.md` (ffd99d8451), committed alone first. `sr2_common.py`, `sr2_diskmass.py`, `sr2_mw.py`, `sr2.py`, `sr2_tail_add.py`, `sr2*.out`, `sr2*.json`. Rule unchanged from SR1. κ = ½ FITTED, unused. No a₀. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

| Holdout, δ 0 | Off (UR3) | Blumenthal (UR3) | **Saturated** | Line |
|---|---|---|---|---|
| DiskMass r at 1.5 h_R | 1.365 | 1.071 | **1.212 [1.170, 1.320], n 29: NOT REACHED** | 0.90–1.10 |
| Υ_K, halo share of g | 0.618, 0.20 | 0.287, 0.61 | 0.433, 0.41 | |
| Milky Way box | wide priors | V+K ONLY, D 1.01 | **V+K ONLY, 0 cells, D 1.43** | in priors |
| McMillan V_c, K_z | 197.5, 66.6 | 251.2, 81.2 | 225.1, 73.8 | 229.1, 66.4 |

Best Milky Way cell: V_c 224, K_z 67.1, both fine; the Oort/outer curve fails, χ² about 79–116 at McMillan against 59.9. δ −0.05 improves it, D 1.22, 1.29 in prior, and still no cell. At 2.2 h_R DiskMass reads 1.109, also outside. Effects of ±0.1 dex on lg M_b and of background are under 0.01.

**Frozen label: HOLDOUTS FAIL.** My expectation was right on DiskMass and wrong on the Milky Way's class.

**Clusters, BCG in χ★: 14/15, G-IN-Mall −2.05, unchanged.** Z moves by 2 × 10⁻⁵. My expectation that it gets worse was wrong: the BCG is small against the cold mass at the keys' radii. Groups change by 3 × 10⁻⁶ in the mean: the Hernquist baryons' radii barely respond. So the rule neither helps nor hurts there, and clusters still fail.

| SPARC, reported | Υ A/B | rms | tilt | Υ by V_flat | groups Z | LITTLE THINGS |
|---|---|---|---|---|---|---|
| δ 0 | 0.47/0.46 | 0.0752 | +0.10 | 0.48 0.58 0.56 0.44 0.51 0.68 | +1.50 | +0.105 |
| δ −0.05 | 0.48/0.49 | 0.0698 | +0.11 | 0.55 0.60 0.59 0.45 0.53 0.71 | +1.96 | +0.128 |
| δ −0.10 | **0.52/0.52** | 0.0658 | +0.10 | 0.58 0.61 0.62 0.46 0.55 0.72 | +2.43 ABOVE | +0.148 |

δ −0.10 clears line and tilt, at blue lensing's 2σ edge. Groups and LITTLE THINGS then fail, and 150–200 km/s is 0.46.

## Reading
The rule is better on SPARC than anything else without a₀, and data it wasn't shaped on don't back it. Halfway between off and Blumenthal, it loses DiskMass's agreement and doesn't gain the Milky Way. As the rule's form was chosen after seeing SPARC, that is the result that counts. KiDS's own grade and Local Group weren't run.

## Checks
K0 no halo: 1.494, 0.821. K1 denominator off: r 1.071, Υ_K 0.287, n 28; McMillan 251.2, 81.2, as UR3. K2 UR1's keys. MUTATE M★ × 0.1: r 1.072; V_c 251.0; Υ 0.35.
