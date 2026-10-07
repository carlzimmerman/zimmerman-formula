# CFG374: CFG372 with the measured baryon phase mix. TENSION (σ₈ fine, small scales +12–16%)

Criteria 396ed0c5a. Engine `cfg374_pm.py` (CFG372 copy plus a phase-weighted filter), launcher, controls (C1a–c and MUTATE pass), analysis `cfg374_analysis.py`. Census: Shull, Smith & Danforth 2012.

| mix (cool / hot / collapsed) | footing | σ₈ ratio | max \|P−1\|, k ≤ 1 | P at k = 0.1 / 0.3 / 1 | verdict |
|---|---|---|---|---|---|
| MIX-A, primary (0.28 / 0.54 / 0.18) | canonical | 1.015 | 0.124 | 1.012 / 1.043 / 1.124 | TENSION |
| MIX-A | alt | 1.019 | 0.156 | 1.015 / 1.054 / 1.156 | TENSION |
| MIX-B, conservative (0.57 / 0.25 / 0.18) | canonical | 1.023 | 0.191 | 1.021 / 1.065 / 1.191 | TENSION |
| MIX-B | alt | 1.029 | 0.240 | 1.026 / 1.080 / 1.240 | TENSION |

**Lane verdict: TENSION.**
- With the measured phase mix, σ₈ is within 1.5–2% (inside the 5% cut).
- But small-scale power at k = 1 is +12% / +16%, against a 10% cut.
- CFG372's GROWTH OK at a pure 1e6 K needs hotter phantom-sourcing baryons than the z ≈ 0 census gives: at k = 1 the census mix keeps 54% of the source, against 50% for pure WHIM.

**Sequence (σ₈; P(k = 1)).**
- CFG361 T5: +20.5% / +25.7%.
- CFG366 reservoir: +3.4% / +4.0%; +29% / +35%.
- CFG374 measured mix: +1.5% / +1.9%; +12% / +16%.
- CFG372 pure hot gas: +0.9% / +1.1%; +7% / +8%.

**Scope.**
- Linear phase filters with z ≈ 0 fractions at all z, on a collisionless run.
- The collapsed phase is unfiltered, though real halo gas is hot and pressured; that would push toward CFG372.
- The reservoir is bookkeeping, and the settling force is conditional (CFG373).
- The cold fluid is still required. κ = ½ is fitted.

**KNOWN BUG, CRITICAL (referee audit 5819dd616, 10-06): the gas-filter Jeans wavenumber has the wrong time dependence.**
- The engine uses comoving k_J = √(1.5 Ω_m a) · 100/c_s (∝ a^(+1/2)). The correct value is √(1.5 Ω_m / a) · 100/c_s (∝ a^(−1/2)), from Gnedin & Hui: k_J = (a/c_s)√(4πGρ̄), with ρ̄ ∝ a⁻³.
- It is correct only at z = 0. The phantom was over-filtered at earlier epochs, near k ≈ 1 by ×1.7 at z = 0.5, ×2.5 at z = 1 and ×4.3 at z = 2.
- The controls used the same formula and could not catch it. The error is the orchestrator's (frozen in the criteria).
- Consequences:
  - CFG372's "GROWTH OK at 1e6 K" is **WITHDRAWN**. The audit's estimate is max|P−1| of about 10–15%, likely TENSION.
  - The small-scale excesses reported here are lower limits.
- A corrected re-run (a criteria amendment committed first) is the fix.
- Also from the audit:
  - the runs are at an unconverged 256³, where the excess grows with resolution (CFG361 K4);
  - constant T and z ≈ 0 phase fractions are used at all z;
  - CFG372's overdraw was computed but read with the wrong key: 3.5% / 4.2% at 1e6 K, 18.8% / 21.3% at 1e4 K. CFG374 MIX-A is 9.8% / 11.9% and MIX-B 15.3% / 17.7%.
  - CFG374's "pure WHIM keeps 50% at k = 1" is wrong. It keeps W = 0.17; MIX-A keeps 3.2× more.
