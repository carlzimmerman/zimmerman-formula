# CFG416 FROZEN CRITERIA: the switch confined to each host's SUPPLY EDGE (no fitted radius), 512³
(owner 2026-10-07: "keep going"; the 10-07 supply-edge hypothesis in STANDING; committed before any script)

**Rule.** As CFG414 (corrected k_J, RES with R_c = 3, MIX-A, A0-FLAT, seed 359, NSEED = 512, 150 steps), but the confinement radius is per host instead of a fixed x.
- x_h·r_ON = r_edge = (5.364/f_ret) · r_M(M_b,now).
- M_b,now = f_ret · f_b · M_ta, with M_ta = (4π/3) r_ON³ Δ_ta(a) ρ̄_m (comoving) and r_M = √(G M_b,now / a₀(a)).
- **Declared f_ret(M_ta) (gas + stars fraction relative to cosmic):**
  - 0.10 below 10^12.5 Msun/h;
  - log-linear to 0.55 at 10^13.5 and 0.85 at 10^14.5;
  - capped at 0.90.
  - This is not fitted to growth. It comes from the census and group/cluster baryon fractions, stated in advance, and is the same relation as the pre-check.
- IN(x_h) is the union of balls of radius min(x_h, 1)·r_ON, using CFG414's cover machinery. The cover is recomputed every 10 steps.

**Known inconsistency (declared).** The PM does not model baryon depletion, so the phantom is still sourced by the undepleted PM baryons. Only the confinement radius uses f_ret.

**Pre-check (post-hoc, labelled).** On CFG410 z0 the resolved hosts give x_h ≈ 0.24–0.33.

**Runs.** 512³ canonical, then alt, queued after CFG414; 8 threads. S0 512³ canonical is CFG411's.

**Decision.** CFG361's cuts (GROWTH OK / TENSION / FAIL) per footing.
- CONFIRMED if both footings are GROWTH OK. If only canonical has run, the verdict is provisional.

**Controls.**
- C1: field-level, x_h → ∞ reproduces BASE coverage (inherits CFG414 C1).
- C2: the x_h(M_ta) function is monotone in r_ON and equals the pre-check values on the CFG410 snapshot to 1e-6.

**MUTATE.** f_ret × 10 (capped at 1), which enlarges the edge (x_h ≈ 1 everywhere). The field-level switch-ON mass must rise by more than 20% relative to the primary.

**Scope.** As CFG414. The KiDS side rests on CFG413's free two-halo amplitude. κ = ½ is fitted.
