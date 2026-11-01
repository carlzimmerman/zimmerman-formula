# ZN4_cluster_resolution: CONVERGED as frozen. At ng 80 the class on X-COP's gas scale holds, and c₂₀₀ moves under 10 %. Resolution doesn't rescue the measured gas scale, which stays X-COP ONLY

Criteria: `FROZEN_CRITERIA.md` (85c7c0652c), committed before any ng 80 run. `zn4_measure.py`, `zn4_grade.py`, `zn4_c200.py`; outputs `zn4.out`, `zn4_results.json`, `zn4_shapes.json`, `zn4_readouts.out`, `zn4_boot.out`, `zn4_MUTATE.out`, `zn4_c200.out`. κ = ½ FITTED; footings never pooled; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework.

Six seeds at each of 10¹⁴, 10¹⁵ (ng 64 had nine, and each grid draws its own field, so this mixes resolution with realisation), all 12 finished. 10¹³ stays ZN1's ng 64.

| Job | f★ 0.034 | f★ 0.0615 | class | ng 64 (ZN3) |
|---|---|---|---|---|
| **X-COP's gas, +0.111** | **15 of 15, G-OUT-M3 +1.53** | **15 of 15, G-OUT-M3 +1.18** | **PASSES BOTH** | PASSES BOTH |
| hydrostatic-free, +0.092 | 14 of 15, G-OUT-M3 +2.10 | 15 of 15, +1.76 | F★-DEPENDENT | not run in ZN3 |
| **GS4's measured gas, +0.005 (reported)** | **12 of 15, G-OUT-M3 +4.41** | **12 of 15, +4.13** | **X-COP ONLY** | X-COP ONLY, +4.35, +4.07 |
| eRASS1's own gas | 11 of 15, +4.53 | 12 of 15, +4.25 | X-COP ONLY | X-COP ONLY |
| MA1's budget M₂₀₀ | 10 of 15, G-OUT-all −3.19 | 6 of 15, −3.40 | FAILS BOTH | FAILS BOTH |

X-COP mean, rms: +0.013, 0.075 and +0.005, 0.074 (ng 64: −0.004, 0.076 and −0.011, 0.076). By x at f★ 0.034: −0.032, +0.011, +0.041, +0.038, +0.006.

**c₂₀₀** (NFW fit to m(x), x 0.05–1, ZN1's definition): 10¹⁴ 5.94 → 5.42 (0.913), 10¹⁵ 4.43 → 4.09 (0.922). Inside the 10 % line, but not by much, and both fall. Seed range at ng 80: 3.74–6.89 and 3.20–5.64.

**Bootstrap, 200 draws:** PASSES BOTH 184, KEYS ONLY 11, F★-DEPENDENT 5. The class holds in 92 %, not noise-limited. All 15 keys pass in 100 % of draws at both f★. X-COP passes in 94 % and 92 %.

## How this reads
- The pass was never limited by resolution. It's limited by the gas scale: `../GS4_pointed_gas_offset` measured +0.005 ± 0.017, not +0.111. The convergence applies to both readings, so X-COP ONLY on measured gas is converged too.
- At +0.092 the class changes by a hair, G-OUT-M3 +2.10 against the line 2. Frozen verdict uses +0.111 only.
- The ng 64 limits in ZN3 still stand, apart from resolution at this level: isolated spheres, thin closing shell near r_ta (median γ about −29; 94–180 of 1,318 cells outside −40 to 60), no gas or BCG response.
- ε keeps its fraction here, and ng 80 is the top. Nothing past it is tested.

## Checks
K1 ng 64 stacks through this path against ZN3, both f★: predictions and X-COP |d| 0, PASS. Bootstrap identity draw |d| 0, PASS. MUTATE r × 1.5: X-COP rms +0.166, G-IN-Mall +1.42, BITES.
