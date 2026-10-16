# CFG818 FROZEN CRITERIA: freed cold energy is NOT yet phase-mixed. Place it by its simulated positions, not the relaxed reservoir (committed before any script)

**Motivation (post-hoc, disclosed).** Under H-EX, the eRASS1 inner band is over-predicted (A_INNER ≈ 0.5) while the middle
band and the middle tercile are short (≈ 1.6). The free mass is placed too centrally. CFG637's Method A places free cold
energy in its fully phase-mixed final profile, but cold energy freed by gas expulsion was freed recently and should still
trace its infall orbits.

**Change (one line of physics, derived, no new constant).** Free cold energy is placed by the Infall run's own time-averaged
positions of the residual elements over the last 1 Gyr (cfg637_lib Infall.M_res_avg on rgrid_avg). This replaces the
phase-mixed M_res_g. It is renormalised to the same total M_res_tot, so ONLY the placement changes, not the amount.
Everything else is CFG815 primary profile P:
- the eROSITA-outskirt retention;
- the M_cond relation;
- the split H-EX;
- all 318 eRASS1 clusters + 8 ACCEPT.

## Pass rules (as CFG815; ν_s primary; both footings)
1. **eRASS1:** MID and OUTER within 2σ, AND every tercile |Z_MID| < 3.
2. **ACCEPT:** OUTER within 2σ.

**Classes:** PASS (both on ≥ 1 footing) / PARTIAL / FAIL. Also report the change against CFG815 P in INNER, MID and the middle
tercile.

## Controls
- K1: with the placement switched back to M_res_g, the run reproduces CFG815 P's stored eRASS1 rows (5 clusters, < 1e-6).
- K2: the total free mass equals CFG815's per system (< 1e-6).

κ = ½ fitted; cold energy mass required; not theory closed.
