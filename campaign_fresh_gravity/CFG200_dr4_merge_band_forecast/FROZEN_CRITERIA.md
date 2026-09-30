# CFG200 — the DR4 separation forecast with the corrected P2 merge band. FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, at the orchestrator's request, before any CFG200 number. **κ = ½ FITTED, NOT DERIVED.** This is a forecast from frozen budgets and relayed predictions. It scores no data, changes nothing in the preregistration and adds no verdict language: row labels are quoted from the frozen text.

## Inputs

**The preregistration.** `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` is read only; its sha256 prefix at this writing is `97aa97c40fc1be25`. The script checks that each cited line still contains the cited text (C0).
- σ_sys = 0.02 (line 617); σ_tot = √(σ_fit² + 0.02²) (line 622).
- σ_fit ≈ 0.019 at N = 30,000, scaling as √(30000/N) (lines 629–631).
- The DR3-like scenario: σ_fit = 0.035 at N = 10,624 (line 674, the §1.6 value).
- The §1.5 decision table (lines 634–639), with Amendment 11(d)'s re-labelling: rows between 1.083 and 1.23 read "framework-band, arm NOT decided", and the guard edge is 1.23.
- Arm A's band: 1.1614–1.1814 canonical, 1.1917–1.2267 alt (lines 947–948).
- Arm C's rows (lines 1331–1336). Arm B = 1.0000 ± 0.0025, killed from above at 1.084 (Amendment 12, as restated in 14(f)).
- The chain's ceiling, 1.0725 / 1.0900 (line 1426), and its rows (lines 1471–1473).

**The corrected P2 merge band.** These values were relayed by the orchestrator on 2026-09-29 from CFG191 (the Opus chat's referee lane; its re-run is pending). They are the means of its 6-seed battery for the P2 kernel with the external field merged, under the frozen estimator.

| footing | g_ext 1.778 × 10⁻¹⁰ (primary): floor / top | g_ext 2.146 × 10⁻¹⁰: floor / top |
|---|---|---|
| canonical | 1.089 / 1.102 | 1.063 / 1.077 |
| alt | 1.111 / 1.127 | 1.079 / 1.099 |

- The relay adds that ν_RAR reproduces Arm A's anchors within 0.013.
- No battery spread was relayed, so the forecast carries no theory error on the merge band. That limitation is stated.
- The values are taken as given and are re-checked against CFG191's committed outputs when those land. CFG191's uncommitted outputs are not read.

## Algebra (CFG63's, reused; `CFG63_discrimination_forecast/forecast.py` is read only, not imported)

- σ_tot(N) = √(v₁/N + σ_sys²).
  - Frozen: v₁ = 0.019² × 30,000.
  - DR3-like: v₁ = 0.035² × 10,624.
- S = Δ/σ_tot(N).
- N_k = v₁ / ((Δ/k)² − σ_sys²), infinite when Δ/k ≤ σ_sys.
- cap = Δ/σ_sys, the separation at infinite N.
- **C1:** the script reproduces CFG63's committed rows for B vs the Arm A floor (S = 5.85 at N = 30,000; N₃σ = 4,342) and for the chain vs Newton (N₃σ = 58,850 canonical, 21,660 alt).

## Pairs, per footing and per g_ext case

Each pair is reported at N = 30,000 (frozen v₁) and at the DR3-like precision (v₁_DR3, at N = 10,624 as CFG63 did, and at N = 30,000). Each row gives S, N₂σ, N₃σ and the cap.

- (a) P2-merge floor, and top, vs ownership: Arm C = Arm B = Newton = 1.000.
- (b) P2-merge floor, and top, vs the chain ceiling (1.0725 canonical / 1.0900 alt).
- (c) The chain ceiling vs ownership. This is a CFG63 row, recomputed.
- (d) P2-merge floor, and top, vs Arm A's floor (1.1614 / 1.1917). This is reported: it shows how far the corrected band sits below the registered Arm A.

## Landing: where a true outcome at each value falls in the frozen rows

For each true value T (both P2-merge anchors in both g_ext cases, per footing; ownership 1.000; the chain ceiling):
- γ̂ is drawn as normal around T with σ_tot at N = 30,000 (frozen v₁). Contamination is NOT modelled; the frozen text says it only raises γ̂.
- Reported: the probability of landing in each row of the §1.5 table, of Arm C's rows, and of the chain's rows. The chain uses its canonical edges on the canonical footing and its bracketed alt edges on the alt footing.
- Also reported: the z-distances at T to 1.000, to the chain ceiling, to Arm A's floor, and to the §1.5 hypotheses 1.09 and 1.137.
- The row edges are the frozen text's illustrative values at σ_tot = 0.028. The frozen z-rule is operative, so the probabilities are also computed with the z-rule edges at σ_tot(30,000), and both are reported.
- The canonical footing decides; the alt footing is reported (§1.5).

## Controls

- **C0:** every cited line contains its cited text.
- **C1:** CFG63's rows are reproduced (above).
- **C2:** every landing distribution sums to 1 within 1e-12.
- **H (load-bearing):** P2-merge floor vs ownership, canonical primary case: S > 0 and N₃σ finite.
- **MUTATE=1:** every P2-merge value is set to 1.000.
  - H must FAIL: S = 0 and N₃σ = ∞ for (a).
  - (b) must equal (c).
  - The run must exit 1.
  - Outputs are written separately (`*_MUTATE`).
