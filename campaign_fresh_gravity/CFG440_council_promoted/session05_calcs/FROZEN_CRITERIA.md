# Session 5 calcs, FROZEN before any script exists — clusters at 0.6

κ = ½ fitted; both footings. No DM particle; the cold mass is still required. On-disk data only.

## K. What shape is the clusters' missing mass?
The working model has ONE attractor, the law's target ρ_ph[ρ_b]. Clusters hold more cold mass than the target (the 0.6 level). If the excess is the same settling fluid, it has nowhere else to settle, so it should take the **target's shape**: M_c(r) ∝ M_ph(r). If the excess instead follows the baryons (CFG371's "excess tracks depleted gas"; a baryon-tied component), M_c(r) ∝ M_b(r).
- Data: the 12 X-COP clusters via `qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/cluster_audit.py`'s own `load_cluster` and `profiles` (M_FORW hydrostatic, gas, stars with its median-ratio import for the 5 without a stellar file). Radii are the audit's grid; the shape fit uses 100–1000 kpc (valid points only).
- Law: g_law = ν_mono(g_b/a₀) g_b with g_b = G M_b(<r)/r² (spherical). M_law = g_law r²/G, M_ph = M_law − M_b, M_c = M_HSE − M_law.
- Statistic: per cluster, the OLS slope of log(M_c/M_ph) and of log(M_c/M_b) against log r over 100–1000 kpc. Median over clusters, bootstrap over clusters (2000, seed 31).
- **TARGET-SHAPED** if the M_c/M_ph slope is within 2σ of 0 **and** the M_c/M_b slope is > 3σ from 0. **BARYON-SHAPED** in the mirror case. **NEITHER** if both are > 3σ from 0. **NON-DISCRIMINATING** otherwise (including both within 2σ).
- Primary: hydrostatic bias b = 0, canonical and alt. Reported: b = 0.2 (M_true = M_HSE/0.8), the 3 relaxed clusters alone, and the 7 with stellar files alone.
- MUTATE (`--mutate`): M_c replaced by 2 M_b (baryon-shaped by construction). The script must return BARYON-SHAPED on the canonical primary; it exits 1 when it does.
