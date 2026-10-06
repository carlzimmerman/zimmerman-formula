# CFG352: the CFG351 switch edge (second caustic) against the data

**Verdict (frozen): PARTIAL.**

The sharp switch edge was placed at 0.232 r_ta, using CFG346 harness with every turnaround radius scaled.

| edge | KiDS d chi2 (canonical / alt) | SPARC | growth |
|---|---|---|---|
| 1.0 r_ta (control) | -9.18 / -9.30, pass | pass | pass |
| 0.359 r_ta (first caustic) | +68.8 / +65.3, FAIL | pass | pass |
| **0.232 r_ta (CFG351)** | **+169 / +163, FAIL** | pass | pass |

The control reproduces CFG346 sharp-turnaround row exactly. MUTATE (edge 0.05 r_ta) fails KiDS, as required.

**Reading:**
- Rotation curves do not care where the edge is, as long as it lies beyond the disc.
- Weak lensing does. The isolated-lens signal needs the law out to about the turnaround radius. A switch that turns ON only where all three axes have crossed (inside about 0.23 r_ta) misses the lensing signal from 0.25 to 1 r_ta.
- So the full-rank cold switch is too conservative: it must also cover infalling, turned-around matter.

Run: `python3 campaign_fresh_gravity/CFG352_caustic_edge_vs_data/cfg352_caustic_edge.py` (CFG352_MUTATE=1 for the control).
