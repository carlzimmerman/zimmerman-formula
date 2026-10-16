# CFG812 FROZEN CRITERIA: impulsive gas expulsion unbinds part of the freed cold energy (H-UB) (committed before any script)

**Motivation (seen, disclosed).** CFG809 (split H-EX) overshoots eRASS1 (MID 0.76, OUTER 0.64) and ACCEPT (×2), while eFEDS
passes. The data sit between no free cold energy and the full expelled share.

**Mechanism (no new constant).** When the expelled baryons leave the catchment, the potential becomes shallower. The freed
(collisionless) cold energy keeps its velocities at that moment, so its energy becomes E′ = ½v² + ½j²/r² + Φ′(r), where Φ′ is
the potential WITHOUT the expelled baryons. Elements with no outer turning point inside the Method A grid (4 r_ta) under Φ′
are unbound and leave. Only the bound remainder stays, placed by Method A orbits in Φ′.
- **Implementation:** CFG809's InfallEX, with final_profile overridden. Φ′ removes the turned shells' diffuse-baryon mass
  m_bdiff = dm f_b (1 − f_ret). The unbound residual elements are dropped from M_res.
- **Everything else is identical to CFG809:** census catchment, split cap, all-retained source, placement, data, statistics.

**Honest prior (stated before running).** The expelled baryons are ≲ 8% of the total mass, so the impulsive change is small.
Unbinding may be confined to marginally bound outer orbits, and the overall effect may be too small to remove the ×1.3
overshoot.

## Pass rules (as in CFG808/809; ν_s primary; both footings)
1. **eRASS1:** MID and OUTER within 2σ, AND every tercile |Z_MID| < 3.
2. **ACCEPT:** OUTER within 2σ.
3. **eFEDS:** p ≥ 0.01.

**Verdict:** PASS (3 of 3 on ≥ 1 footing) / PARTIAL (2) / FAIL.

## Controls
- K1: the ALL control reproduces CFG727's ALL rows.
- K2: with the unbinding disabled (Φ′ = Φ), the EX case reproduces CFG809's eRASS1 MID 0.76 within 0.01 (run on 30
  clusters as a spot check).
- Report the median bound fraction of the freed cold energy per tercile.

κ = ½ fitted; cold energy mass required; not theory closed.
