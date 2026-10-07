# CFG396: the "two-regime" rule IS CFG361's T5. Stopped at the identity gate, no PM rerun. Inherited verdict: FAIL on both footings (σ₈ ×1.205 / ×1.257)

Criteria e66c7ca1d (committed alone first). Script `cfg396_two_regime.py` → `cfg396_two_regime.out` / `_results.json`; MUTATE → `*_MUTATE.*` (rc 1, as required). Runtime 7 s. No new PM runs, no new constants, no downloads.

**Verdict (CFG361's cuts, ratios to CFG359's S0 at z = 0, 256³; inherited because the rule is identical to T5)**

| rule | footing | σ₈ ratio | max \|P−1\|, k ≤ 1 | P at k = 0.1 / 0.3 / 1 | verdict |
|---|---|---|---|---|---|
| two-regime (= T5) | canonical | 1.2049 | 0.750 | 1.359 / 1.549 / 1.602 | FAIL |
| two-regime (= T5) | alt | 1.2573 | 0.972 | 1.460 / 1.707 / 1.782 | FAIL |
| regime gate open (= ADD, C2) | canonical / alt | 1.5815 / 1.6452 | 2.57 / 2.85 | | FAIL |
| spatial gate open (= S1T5) | canonical / alt | 1.3165 / 1.3973 | 1.10 / 1.39 | | FAIL |

**Answer to the question asked.** No. The two-regime rule does not close large-scale growth, with or without gas temperature. It is the T = 0, R_c → ∞ limit of CFG372 (equivalently, CFG366's RES without the catchment). Everything that brought σ₈ down in CFG366 and CFG372 came from the catchment compensation and the gas filter, not from a cold-versus-phantom gate.

**Why it is identical (G0, algebra).**
- The rule says: extra source = 0 where ρ_cold ≥ ρ_ph, and ρ_ph − ρ_cold where ρ_cold < ρ_ph, inside bound cells.
- That is f · max(0, s_ph − s_c), with the same s_c (the engine's CIC cell density × (1 − f_b)), the same baryon-only phantom s_ph and the same T1 switch f.
- CFG361's T5 is literally `extra = fsw * max(s_ph - s_c, 0)`. CFG366's "literal local min rule" (dark ≤ cold present, on top of the Newtonian cold) adds 0 = S0; it is a different rule and is not this one.

**G1 (field level, CFG361's evolved z = 0 field at 128³).** An independent implementation with explicit regime masks matches the engine's T5 force to 5.8e-7 (canonical) / 4.8e-7 (alt) relative. Both PASS (threshold 1e-5).

**The physical reason the gate does nothing.** On that field, 98.4% (canonical) / 99.6% (alt) of the bound (ON) mass sits in the phantom regime (ρ_cold < ρ_ph). The cold regime holds only 0.7% / 0.2%. The engine's cold density is the cosmic share of the local matter, (1 − f_b)/f_b ≈ 5.4 × baryons, and the deep-MOND phantom exceeds that in almost every bound cell. CFG361 already reported this (94–97% phantom-dominated, so max(phantom, cold) ≈ phantom).

**Controls.**
- C1 PASS: the six ratios used here, re-derived from CFG361's run JSONs and CFG359's S0 JSON, match CFG361's committed results to 0.
- C2 PASS: with the regime gate open, the over-build is larger (ADD 1.58 / 1.65 against 1.205 / 1.257).
- MUTATE (gate disabled in the independent implementation): G1 FAILS (rel 3.2 / 2.9), rc 1, as required.

**Departures (disclosed).**
- No PM run was made: Step 0 said identical, as frozen. So the like-for-like CFG372 rerun at a lower resolution was not needed. The "reproduce one CFG372 number" control became C1, which reproduces CFG361's numbers that the verdict actually uses.
- The task framed "gate forced open" as reproducing the T5-like over-build. In fact the gated rule IS T5. Opening the gate gives ADD (CFG359), which is worse.
- CFG361's K4 (resolution) failure carries over: T5 is not converged at 256³, and the excess grows with resolution. That makes the FAIL worse, not lenient.

**What would make the X-COP idea bite (owner item, not run).** The gate matters only if the cold fluid is MORE concentrated than the cosmic share. That is the NFW-like X-COP picture, with ρ_cold above ρ_ph in cores. In this engine the cold is pinned to (1 − f_b)(1 + δ), so that regime is almost empty by construction. Testing it needs a cold fluid that moves as its own collisionless component, i.e. a two-species PM in which the phantom is a settling target and not an added source. That is a new model with a new mechanism, not this minimal change. The cold fluid is still required, its amount is free, and κ = ½ is fitted.
