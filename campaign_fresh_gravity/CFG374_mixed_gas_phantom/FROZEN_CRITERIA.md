# CFG374 FROZEN CRITERIA: CFG372 with the measured baryon phase mix. Does growth pass when the phantom's baryons are the real hot + cool + collapsed mixture?
(owner 2026-10-06: "ook sir", to the mixed-gas run; committed before any script)

**Why.** CFG372 passes at T = 1e6 K (GROWTH OK) and is TENSION at 1e4 K. Real diffuse baryons are a mixture.

**The filter.** The baryon field that sources the phantom is the matter field times a phase-weighted response:
- W(k) = f_cool / (1 + k²/k_J(1e4 K)²) + f_hot / (1 + k²/k_J(1e6 K)²) + f_coll × 1.
- k_J(T) is as in CFG372. The collapsed phase (stars, cold gas and CGM in halos) is unfiltered.
- Everything else is CFG372's engine exactly: the RES rule, R_c = 3 Mpc/h, A0-FLAT, 256³, seed 359.

**Census (Shull, Smith & Danforth 2012, z ≈ 0, fractions of all baryons).**
- Photoionised Lyα forest: 28%.
- WHIM: 25%.
- Collapsed (galaxies, CGM, clusters): 18%.
- Unaccounted ("missing"): 29%.

**Two declared assignments. No scan.**
- **MIX-A (PRIMARY):** the missing 29% are WHIM, the standard reading, supported by later FRB / tSZ / X-ray detections. f_cool = 0.28, f_hot = 0.54, f_coll = 0.18.
- **MIX-B (conservative):** the missing 29% are cool. f_cool = 0.57, f_hot = 0.25, f_coll = 0.18.

**Runs.** 2 mixtures × 2 footings = 4 runs. Work data go to ../_external_data/cfg374_work/. S0 is CFG359's 256³ run, read-only.

**Decision.** CFG361's cuts verbatim, per footing, never pooled. GROWTH OK means |σ₈ ratio − 1| ≤ 5% AND max over k ≤ 1 of |P ratio − 1| ≤ 10%, on both footings. TENSION and FAIL are as in CFG361. The lane verdict is set by MIX-A; MIX-B gets its own verdict.

**Also reported.** The CFG372-style combined scorecard (CMB-lensing proxy; KiDS enclosed-mass change, unchanged by the filter; SPARC).

**Controls.**
- C1: the weights sum to 1. W(0) = 1. MIX with f_hot = 1 reproduces CFG372's 1e6 K filter exactly (field level).
- **MUTATE** (field level, CFG374_MUTATE=1): f_coll = 1 (no filtering) must give the same rms phantom source as T = 0, to 1e-6 relative. MUTATE writes separate outputs.

**Scope.**
- Linear, constant-temperature phase filters on a collisionless run. The phase fractions are z ≈ 0 values applied at all z, which is an approximation; WHIM grows at late times.
- The reservoir is bookkeeping, and the settling force is conditional (CFG373).
- The cold fluid is still required. κ = ½ is fitted.
