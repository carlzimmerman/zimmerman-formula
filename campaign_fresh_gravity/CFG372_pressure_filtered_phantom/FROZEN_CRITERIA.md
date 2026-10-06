# CFG372 FROZEN CRITERIA: does gas pressure close the growth gap? CFG366's reservoir rule, with the phantom sourced by a pressure-smoothed baryon field
(owner 2026-10-06: "get me across the final mile"; committed before any script)

**Why.**
- CFG361 (T5) fails: σ₈ ×1.205 / ×1.257.
- CFG366's reservoir rule at the host-scale catchment R_c = 3 Mpc/h fixes σ₈ (×1.034 / ×1.040) but leaves P(k = 1) ×1.29 / ×1.35.
- Both runs source the phantom from baryons that trace collisionless matter exactly (g_b = f_b g_N). Real diffuse baryons are hot gas, with photoionised IGM at ~1e4 K and WHIM at ~1e5–1e7 K. Gas pressure smooths them below the gas Jeans scale. That is the missing physics at k ~ 0.5–5 h/Mpc, where the residual excess sits.

**The change (one line in the engine).** The baryon field that sources the phantom is the matter field filtered by the linear gas response at constant temperature (Gnedin & Hui 1998):
- W(k) = 1/(1 + k²/k_J²), with comoving k_J(a) = √(1.5 Ω_m a) × (100 km/s)/c_s in h/Mpc;
- c_s = √(5 k T/(3 μ m_p)), μ = 0.6.
- Everything else is CFG366's engine (copied, not imported) exactly. That covers the RES rule and the catchment R_c = 3 Mpc/h; the T1 switch, tidal tensor and cold share s_c all read the unfiltered total field.
- The filter applies only to g_b inside the phantom.
- No knob scan: T is a declared two-value bracket from measured gas phases.

**Runs.** RES, R_c = 3, A0-FLAT, 256³, seed 359, both footings, T ∈ {1e6 K (PRIMARY: WHIM median), 1e4 K (secondary: photoionised floor)}. That is 4 runs.
- S0 256³ is read read-only from CFG359's work JSON.
- Work data go to ../_external_data/cfg372_work/.

**Decision.** CFG361's cuts verbatim, per footing, never pooled:
- GROWTH OK: |σ₈ ratio − 1| ≤ 5% on BOTH footings AND max over k ≤ 1 h/Mpc of |P ratio − 1| ≤ 10% on both.
- TENSION: the σ₈ shift is in (5%, 20%], or the P shift is > 10% with σ₈ within 20%.
- FAIL: the σ₈ shift is > 20% on either footing.
- The lane verdict is set by T = 1e6 K. T = 1e4 K gets its own verdict.

**Also reported.**
- k_J at z = 0 for each T.
- The P ratio at k = 0.1, 0.3 and 1.
- Overdraw (as CFG366).
- The comparison with CFG366 R_c = 3.

**Controls.**
- C1: W(k_J) = 0.5, W ≤ 1, monotone. T → 0 gives W ≡ 1 (CFG366's code path).
- C2: field-level, on CFG361's T5 canonical z = 0 snapshot (read-only, deposited 128³). The rms phantom source with T = 1e6 is below that with T = 0, and above 0.
- **MUTATE** (field-level, CFG372_MUTATE=1): T = 1e10 K must cut the rms phantom source by > 90% relative to T = 0. MUTATE writes separate outputs.

**Scope.**
- A linear, constant-temperature gas filter on a collisionless run. Hydrodynamics, cooling and shock heating are not simulated.
- Inside collapsed hosts the gas cools and condenses, which this mesh does not resolve.
- The cold fluid is not moved as particles; the reservoir is bookkeeping, as in CFG366.
- The cold fluid is still required. κ = ½ is fitted.
