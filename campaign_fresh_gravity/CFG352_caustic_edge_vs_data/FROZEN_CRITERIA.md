# CFG352 FROZEN CRITERIA: does CFG351's switch edge (the second caustic, 0.232 r_ta) pass KiDS lensing, SPARC and growth?

**Lane:** orchestrator. The owner said "run the lensing check".

**The model.** CFG351's full-rank cold switch is a sharp step: f = 1 inside the radius where all three axes have crossed, and 0 outside. In spherical infall that radius is the second caustic, r_edge = 0.232 r_ta (CFG351, via Bertschinger; its first caustic sits at 0.359).

**Harness.** CFG346's committed harness, copied, using its sharp-edge code path (ℓ = 0, f_in = 1). The only change is that every turnaround radius is multiplied by EDGE_FRAC. Everything else is unchanged:
- the KiDS isolated-lens χ² scorer and its baseline (law χ² 162.6 / 154.8);
- SPARC A3 and Δrms with their limits (A3 ≥ 0.90; |Δrms| < 0.005);
- the growth-leak check.

## Rows
- **EDGE_FRAC = 0.232:** primary.
- **EDGE_FRAC = 0.359:** reported (the first caustic).
- **EDGE_FRAC = 1.0:** the control; it must reproduce CFG346's sharp turnaround row.

## Decision (primary row, both footings)
- **PASS:** KiDS Δχ² ≤ +9 AND SPARC passes AND growth passes.
- **PARTIAL:** two of the three pass.
- **FAIL:** otherwise.

## Controls
- **C1:** EDGE_FRAC = 1.0 reproduces CFG346's sharp-turnaround KiDS Δχ² and SPARC result.
- **MUTATE** (CFG352_MUTATE=1): EDGE_FRAC = 0.05, an edge far too small, which must fail KiDS or SPARC.
