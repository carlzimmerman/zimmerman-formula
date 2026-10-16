# CFG811 FROZEN CRITERIA: H-EX prediction for the KiDS early − late lensing difference at matched baryonic mass (committed before any script)

**Observed target (record).** KiDS f30 early − late at matched M_b: +0.280 ± 0.083 dex (CFG669 T2). Record harness: CFG721 T-K
(`CFG721_supply_overflow/cfg721.py`, mode tk): prediction = CFG658 law value (−0.027) + Δ, where Δ is the log10 early/late ratio
of ΔΣ at R = 50, 70.71, 100 kpc, averaged over log M_b = 10.0, 10.5, 11.0, 11.5. PASS iff |prediction − 0.280| < 2 × 0.083,
i.e. prediction in (0.114, 0.446).

**Hook.** Under H-EX the expelled baryon share becomes free mass. Early types are held to have expelled/heated more of their
catchment baryons than late types at the same stellar mass, so at matched M_b,gal their free share is larger. The retained
tethered part (law truncated at 5.84 r_M, identical baryons) is the same for both types, so the law ratio in the harness is 1 and
the whole difference comes from the free share. This is the galaxy-scale model of CFG810 (same functions, imported).

**Declared contrast (set now, no tuning to +0.28).**
- Late: N_L = 1/f_ret from the CFG804 census fixed point (the record's own census).
- Early: retained fraction lower by a factor r_f: f_ret,E = f_ret,L / r_f, i.e. N_E = r_f N_L and M_ta,E = r_f M_ta,L.
- **Primary r_f = 1.5.** Source: a PROVISIONAL literature order-of-magnitude (detected baryon fractions of galaxy catchments, late
  types roughly 0.3 vs early types roughly 0.2 of the cosmic share; Bregman et al. 2018 and McGaugh et al. 2010 type estimates,
  quoted from memory and NOT verified against the papers). It is a declared input, not a derived number.
- Reported as sensitivity only (never as the pass): r_f = 1.0 (control), 2.0, 3.0, and the r_f that would give exactly +0.280
  (diagnostic). The pass is judged on r_f = 1.5 alone.
- Free-mass placement: isothermal to r_ta, as the CFG810 declared bracket (Method A at galaxy scale not run, see CFG810). MUTATE:
  uniform sphere. r_ta from `r_ta_single(M_ta, a_obs = 1)` (T-K is at z = 0, as in CFG721).

**Controls.**
- K1: r_f = 1.0 gives |prediction + 0.027| < 0.005 (equal retained fractions give no excess).
- K2: free share set to 0 for both types gives Δ = 0 exactly.
- MUTATE: uniform placement, separate outputs; the class is reported for both and flagged placement-conditional if they differ.

**Classes.** PASS (within 2σ), OVERSHOOT (> 0.446), SHORT (< 0.114). A PASS is conditional on the declared r_f and placement.

kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed.
