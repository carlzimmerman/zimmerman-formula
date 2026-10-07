# CFG397: M/L-free a₀ rung (SPARC gas-dominated points). RUNG NOT ESTABLISHED (anchor σ 0.071 > 0.05); the anchor sits on the alt footing

Criteria fe7a17fc5 (committed before the script). Script `cfg397_gas_rung.py` (~1 s). κ = ½ fitted; both footings. No DM particle; the cold mass is still required.

| sample | N gal (points) | a₀ | log a₀ |
|---|---|---|---|
| A all distance methods | 30 (223) | 7.59e-11 | −10.120 ± 0.071 |
| **B ladder anchor (TRGB/Cepheid/SNe)** | **10 (108)** | **1.11e-10** | **−9.953 ± 0.071** |
| C Hubble flow | 19 (112) | 6.61e-11 | −10.180 ± 0.085 |

- **K1 (Υ-insensitivity) PASS:** Υ_disk 0.5 → 0.7 moves a₀ by −0.037 dex (all points: 0.24, CFG390). The gas-dominated selection removes the M/L degeneracy as intended.
- **Anchor vs the footings:** canonical +0.075 dex (+1.1σ), **alt −0.007 dex (−0.1σ)**, PAPER43's gas-point 8.3e-11 +0.127 (+1.8σ); all consistent within 2σ.
- **CFG301 MeerKAT gas-dominated BTFR** (N 37, 1.19e-10): anchor minus it −0.028 dex. Two independent M/L-free routes (resolved SPARC rotation curves on ladder distances; MeerKAT catalogue widths) agree to 0.03 dex.
- **Flow − ladder (gas-only) = −0.226 ± 0.111 dex (2.0σ).** This is the opposite sign to CFG390's all-points split (+0.15). Gas-dominated flow galaxies are nearby dwarfs, whose Hubble-flow distances carry large peculiar-velocity errors. Hubble-flow a₀ from gas dwarfs should not be trusted, and the all-points "flow higher" was likely an M/L effect.
- **Verdict:** NOT ESTABLISHED as frozen (σ 0.071 with 10 anchor galaxies). The anchor needs ~20 more ladder-distance gas-dominated discs (σ ∝ N^−½ → ~0.05 at N ≈ 20).
- **MUTATE** (gas dropped): empty selection detected, exit 1.

Caveats: 10 anchor galaxies; Q ≤ 2; the CFG301 comparison is a BTFR median from catalogue widths, not a rotation-curve fit.
