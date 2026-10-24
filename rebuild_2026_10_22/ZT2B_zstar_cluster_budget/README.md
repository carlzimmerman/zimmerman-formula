# ZT2B: Z★'s cluster core is a profile problem, not a budget problem. The free excess carries enough mass, but only if it sits ≥ 8× more concentrated than collapsed dust (and still short at 18π²ρ̄_m). The core stays red without a concentrating mechanism

Criteria **12df931233** (committed alone first). Script `zt2b_budget.py` execs Z-T2's committed script and patches only the
free-excess profile. Runtime about 9 min for 7 modes, 0.35 GB, one thread. κ = ½ FITTED. Footings never pooled. No dark-matter
particle. Not "theory closed". Nothing here says the data favour the framework.

**Why this lane.** Z-T2's free excess already sits on CFG930's native NFW (collapse-time concentration), so a "relaxed free dust"
variant would duplicate it. The question here is whether Z★'s dust budget could lift the core at all. A central mass maximises
ΔΣ at every radius for a fixed mass. Check KL: on the heaviest cluster a 1e14 M☉ central mass lifts the MID bins by 103 / 49 / 23
M☉ pc⁻², against 8 / 6 / 4 for the NFW debris of the same mass.

## T3 A_MID (C*_own, h 0.672, r_s cap; the other sub-cells agree to ±0.03)

| footing, R_own | Z-T2 (NFW debris) | PM: free excess central | ALLPM: all supply central | first passing c-multiplier on the debris NFW | class (PM) |
|---|---|---|---|---|---|
| canonical, 200ρ_c | 1.45 ± 0.14 ✗ | 0.89 ± 0.10 ✓ | 0.44 ✗ (overshoot) | ×8 | PROFILE-LIMITED |
| canonical, 18π²ρ̄_m | 1.68 ± 0.17 ✗ | 1.23 ± 0.14 ✓ | 0.27 ✗ | none up to ×16 (1.47) | PROFILE-LIMITED |
| alt, 200ρ_c | 1.41 ± 0.14 ✗ | 0.99 ± 0.11 ✓ | 0.44 ✗ | ×8 | PROFILE-LIMITED |
| alt, 18π²ρ̄_m | 1.62 ± 0.16 ✗ | 1.40 ± 0.14 ✗ | 0.27 ✗ | none up to ×16 (1.53) | **BUDGET NO-GO** |

T2 MID passes in most cells under every mode, because its s_tot is about 0.35. Checks: K-REP (the NFW mode reproduces Z-T2's committed
A and s_tot exactly, 0.0), KL, and Z-T2's own K0–K5 inside every mode: all PASS. `--mutate` (cross shear as data): K0 fails
(3.2) and the run exits 1 at its first mode.

## Reading

- **The budget is there.** At the cosmic share (f_s = 5.364), Z★'s total dust placed centrally overshoots the core 2–4×. In 3 of
  4 conventions even the free excess alone, the dust the law does not hold, could close T3's core if it sat at the centre.
- **The profile is the problem.** On the natural profile for free dust (CFG930's collapse-time NFW), the free excess must be about 8×
  more concentrated (200ρ_c) to pass. At 18π²ρ̄_m even 16× fails, because fewer T3 clusters are supply-rich there (36–58 %) and
  the excess is smaller. Ordinary dust dynamics give nothing near 8×; baryonic contraction around a BCG is typically ×1.5–2.
- **What a fix would need.** Something must put roughly 10¹³–10¹⁴ M☉ of free dust inside ~0.1–0.3 Mpc of rich-cluster centres
  without touching galaxies. The held dust must stay at the law (galaxies require it), and the free dust must not relax like dust.
  Nothing in Z★ or the record provides that. It is the same missing galaxy–cluster selector the v3s verdict names (§6), now
  stated as a concentration target.
- **Cluster row: stays red.** This lane does not change Z-T2's FAIL / PARTIAL classes. It shows the failure is not forced by Z★'s
  mass budget except in the alt / 18π²ρ̄_m convention.

Scope: spherical, the Z-T2 data and statistics unchanged, a Plummer core r_c = 10 kpc for the central bound, and the ladder scales
CFG930's c at fixed r_b (reported, not fitted). INNER and OUTER under PM / ALLPM are not models and are not graded.
