# CFG416: the switch confined to each host's supply edge, at 512³. QUEUED after CFG414

Criteria are in FROZEN_CRITERIA.md. Engine `cfg416_pm.py` is a CFG414 copy with x_h from `x_supply`. Launcher `cfg416_run_all.py` waits for CFG414.

**Controls (disclosed).**

**C2 FAILS at the frozen 1e-6 tolerance.**
- The engine's x_h matches the pre-check formula to 1.2e-4 relative.
- The difference comes from unit constants: G in SI with Msun and Mpc, against G = 4.30091e-9 in Mpc km² s⁻² Msun⁻¹.
- It is not a logic difference. The frozen tolerance was over-tight.
- x_h(r_ON) at z = 0 (canonical): 1.56 → 0.27, 4 → 0.31, 8 Mpc/h → 0.42.

**MUTATE FAILS, kept.** The frozen criteria were wrong in sign.
- r_edge = (5.364/f_ret)·r_M(f_ret M) scales as f_ret^(−1/2). So raising f_ret SHRINKS the edge; it does not enlarge it as frozen.
- f_ret × 10 changed the covered mass by −13%. The mask responds to f_ret, but in the opposite direction to the one declared, and below the 20% threshold.

**C1** is inherited from CFG414 (PASS).

## RESULT (512³): NOT CONFIRMED (canonical pass, alt misses by 0.0009)
`cfg416_analysis.py` (`cfg416_analysis.out`):
- **canonical:** σ₈ 1.0072, max|P−1| 0.0923, GROWTH OK.
- **alt:** σ₈ 1.0073, max|P−1| 0.1009, TENSION. It is over the 0.10 cut by 0.0009 and is kept as a miss.

**Reading.** The census supply edge, which uses measured baryon inputs and the declared inconsistency, sits at the cut on alt at 512³. That matches CFG414's knife-edge. The small-scale excess still rises with resolution. The zero-knob rule (CFG424, 256³: 0.027–0.029) is confirmed or not by CFG425 R3 at 512³.

CFG419 (DE branch, 512³) was paused so that CFG425 R3 could run first. It will be re-run afterwards; its launcher skips finished runs.
