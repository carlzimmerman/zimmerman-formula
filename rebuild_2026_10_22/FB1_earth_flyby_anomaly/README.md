# FB1_earth_flyby_anomaly — RESULT (frozen b7871a1296, no amendment)

**Verdict: FB SILENT (= GR) on both footings.** The framework predicts no Earth flyby anomaly, so it does not explain
the anomaly.

| reading | largest extra field near Earth | Δv∞ bound (T = 2e6 s) | class |
|---|---|---|---|
| R-S screened theory, L★ = 24 / 28.9 / 90 pc (primary) | Earth hedgehog 7.3e-22 m/s²; Sun-hedgehog tide 3.2e-18 | ≤ 6.5e-9 mm/s (exact value 0: a static central field conserves energy) | SILENT, both footings |
| R-M ν_mono, unscreened | log10(ν−1) = −3457 (canonical) / −3145 (alt) | 10^−3450 / 10^−3137 mm/s | SILENT |
| R-1 ν1, unscreened AQUAL (reported only; already Cassini-dead, E2) | ≈ a₀, near-uniform | ≤ 0.19 / 0.23 mm/s | — |

- NEAR needs 13.46 mm/s. The screened framework supplies at most 6.5e-9 mm/s, about 2e9 times too little.
- Anderson's empirical K = 2ω_E R_E/c = 3.10e-6 needs a coupling to Earth's **spin**. Every framework reading is static
  and spherically symmetric about each body, so it has no such term. The anomaly's ω_E R/c scaling points away from an
  a₀-type law.
- Reported: Rosetta II (2007), Rosetta III (2009) and Juno (2013) showed no anomaly where Anderson's formula predicted
  one. A framework that is silent is consistent with those nulls. Flybys cannot hurt the framework, and cannot help it.

## Checks
- **K0 PASS** 6/6: Anderson's formula reproduces the transcribed Table I (NEAR 13.29 vs 13.46, Galileo I 4.13 vs 3.92, …).
- **K1 PASS** Earth hedgehog = GM_E/L★² exactly.
- **K2** one thread, under a second.
- **MUTATE: FAILED as frozen (exit 0).** With Anderson's formula injected, the grader returns FB CONFLICTS instead of
  FB EXPLAINS. The reason is that the frozen EXPLAINS rule (2σ on every flyby) is stricter than the formula itself:
  NEAR ±0.01 mm/s (13.29 vs 13.46), Rosetta ±0.03, MESSENGER ±0.01 all miss. So **the EXPLAINS branch is not reachable
  even by the target formula**. This does not touch the SILENT verdict, which depends only on the bound
  (8 to 3000+ decades below threshold), but it means the grader could not have certified an explanation. Not amended
  after the fact; disclosed here.

## Prior record
`ai_slop/research/unsolved_problems/pioneer_flyby_anomalies.py` (2026-06-01) reached "cannot explain" by inspection.
FB1 is the computed version on the current (screened) theory, and agrees with it.

Table I transcribed from Anderson et al. 2008, PRL 100, 091102 (K0 cross-checks it). κ = ½ FITTED; footings never
pooled; cold dark energy, not matter; not theory closed.
