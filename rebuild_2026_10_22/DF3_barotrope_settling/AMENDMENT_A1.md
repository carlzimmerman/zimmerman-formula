# DF3 AMENDMENT A1: post-result, disclosed as such

Written after the cells and map were read. κ = ½ FITTED. Not theory closed.

**An artefact in the NO EQUILIBRIUM count.** Γ ≤ 1 rows at low σ read NO EQUILIBRIUM 0.00 in clusters, as at Γ 1, σ 30 (X-COP −1.284, the same as Γ 5/3). That's wrong. Newtonian M_max = 2.52 σ² r_ta / G at σ 30 is about 3e12 M☉, far under a cluster's fair share. The solver starts from a uniform sphere at the first grid radius, and there the fair share fits inside that one cell before any peak appears, so it reports a root that isn't an isothermal solution. **Those rows are read here as NO EQUILIBRIUM.** Their numbers in `df3_cell_G1.000_s30.out` and the map's Γ 1 σ ≤ 30 and Γ 2/3 σ ≤ 3 rows carry no meaning as equilibria. Solver and outputs aren't changed; no label depends on this, since those rows fail either way.

**Γ 5/3 is different.** It has real equilibria, and the same first-cell behaviour is a real core below the grid: Newtonian R scales as σ² M^(−1/3), and K_lane_emden and K_K16 check this. So its X-COP numbers stand, but its core values and Bullet columns are bounds set by the grid, not measurements.

**MUTATE.** K x 16 was run as a control in every pass rather than as a separate mode, so `df3_controls.json` carries it. The separate-output run adds nothing, and it wasn't done on the graded cells.
