# CFG372: CFG366's reservoir rule with the phantom sourced by pressure-filtered baryons. GROWTH OK at T = 1e6 K (primary); TENSION at 1e4 K

Criteria 733d27623. Engine `cfg372_pm.py` (CFG366 copy plus a one-line filter), launcher `cfg372_run_all.py`, controls `cfg372_checks.py`, analysis `cfg372_analysis.py`. Work data in ../_external_data/cfg372_work/. S0 is CFG359's 256³ run, read-only.

**Frozen decision (CFG361's cuts, ratios to S0 at z = 0)**

| T | footing | σ₈ ratio | max \|P−1\|, k ≤ 1 | P at k = 0.1 / 0.3 / 1 | verdict |
|---|---|---|---|---|---|
| 1e6 K (primary, WHIM) | canonical | 1.0089 | 0.076 | 1.004 / 1.027 / 1.068 | GROWTH OK |
| 1e6 K | alt | 1.0105 | 0.089 | 1.005 / 1.031 / 1.080 | GROWTH OK |
| 1e4 K (secondary, photoionised) | canonical | 1.0289 | 0.244 | 1.027 / 1.081 / 1.244 | TENSION |
| 1e4 K | alt | 1.0350 | 0.301 | 1.033 / 1.098 / 1.301 | TENSION |

**Lane verdict: GROWTH OK** (T = 1e6 K, both footings).

**Sequence.**
- CFG359 additive: ×1.58.
- CFG361 T5: ×1.205 / ×1.257 (FAIL).
- CFG366 reservoir at R_c = 3: ×1.034 / ×1.040, but P(k = 1) ×1.29 / ×1.35 (TENSION).
- CFG372 with 1e6 K gas pressure: ×1.009 / ×1.011, P within 7.6% / 8.9% (GROWTH OK).

**The pass depends on the gas temperature.** At the 1e4 K photoionised floor the small-scale excess stays at +24 / +30%.
- The real diffuse baryons are a mixture: WHIM at 1e5–1e7 K holds roughly 40–50% of baryons at z < 1, and cooler IGM and halo gas the rest. A mass-weighted mixture is not run.
- So "GROWTH OK" holds if the gas that sources the phantom is mostly WHIM-hot.

**Controls.**
- C1 (filter algebra) and C2 pass. On CFG361's z = 0 field, 1e6 K halves the rms phantom source (0.477) and 1e4 K cuts it to 0.954.
- MUTATE: T = 1e10 K cuts it to 0.014, as required.

**POST-FREEZE combined scorecard (reported, not scored; T = 1e6 K).**
- (i) CMB-lensing proxy: the mean P ratio at k = 0.05–0.2 is 1.001 / 1.002 at z = 1 / 0.5. That gives A_lens − 1 ≲ +0.3%. This is an upper bound from snapshots, not a full calculation.
- (ii) KiDS isolated lenses: the reservoir compensation changes the enclosed lensing mass by −0.02% at 0.3 Mpc, −0.3% at 1 Mpc and −6.5% at 3 Mpc, for M_b = 1e10.5–1e11, on both footings.
  - This is safe against KiDS-1000.
  - It is a sharp prediction for KiDS-Legacy / Euclid stacks: a dip of a few percent at about 3 Mpc relative to the bare law.
- (iii) SPARC: the change inside 0.1 Mpc is below 0.01%.

**Scope.**
- The gas filter is linear, at constant temperature, on a collisionless run. There is no hydrodynamics.
- The reservoir is bookkeeping: the cold fluid is not moved as particles. The overdraw, reported in CFG366, is not recomputed here.
- The settling force is CONDITIONAL (CFG373).
- The cold fluid is still required. κ = ½ is fitted.

**FORWARD FIX (10-06, from CFG377, a8360bf1b): the KiDS "sharp prediction" was overstated.**
- In the lensing observable ΔΣ, the −6.5% enclosed-mass change at 3 Mpc is only about −2%. It is −0.4% at 2 Mpc and −0.03% at 1 Mpc, because a 4.45 Mpc Gaussian deficit acts almost like a uniform sheet.
- KiDS-1000 reaches about 2.2 Mpc and has no power (Δχ² +0.33 / +0.37, power 0.046).
- An expected 2σ detection needs about 1e4 times KiDS-1000's pairs, plus a two-halo model good to about 0.2%.
- So it is NOT a near-term KiDS-Legacy / Euclid test.
