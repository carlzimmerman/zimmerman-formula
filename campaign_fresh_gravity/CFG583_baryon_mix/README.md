# CFG583: does the law's residual track the baryon mix (gas, bulge) at fixed baryonic mass? NO RELATION, but UNDERPOWERED (MUTATE not detected)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (ba12dc107). (owner chat 10-09)
- **Script:** `cfg583_mix.py` → `cfg583_mix.out`, `cfg583_results.json`; MUTATE `CFG583_MUTATE=1` (inject −0.20 f_gas) → `_MUTATE`.
- **Data:** SPARC on disk (`SPARC_Lelli2016c.mrt` via CFG516's parser, `sparc_data/*_rotmod.dat`); Q ≤ 2, Inc ≥ 30° → 153 galaxies, 139/141 with ≥ 3 outer points.
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Result (outer residual, g_bar < a0/3; Υ_d 0.5)
| footing | n | median Δ | b (log M_b) | c (f_gas), p | d (f_bul), p |
|---|---|---|---|---|---|
| canonical | 139 | +0.008 | +0.067 | +0.105, 0.34 | +0.065, 0.55 |
| alt | 141 | −0.020 | +0.062 | +0.089, 0.45 | +0.079, 0.50 |

Υ_d 0.4 / 0.6 and the all-points residual give the same picture (p 0.18–0.88). Only 13–20 galaxies have a bulge > 5%.

## Verdict as frozen: NO RELATION for f_gas and f_bul — but the test is UNDERPOWERED
- **MUTATE FAILS (not detected):** an injected −0.20 dex per unit f_gas moves c by exactly −0.20 (to −0.095 / −0.111)
  but p = 0.29 / 0.23. SPARC's outer residuals cannot detect a gas-fraction dependence of that size, so "no relation"
  only excludes effects larger than ≈ 0.3 dex per unit fraction.
- **C3 FAILS mildly:** the within-mass permutation gives p < 0.05 in 9.0% of null datasets (expected 5 ± 3.5%), i.e.
  slightly anti-conservative — which makes the null more, not less, secure.
- C1, C2 pass (the law fits SPARC's outer points with median residual +0.008 / −0.020 dex).

## Reading (not a verdict)
- SPARC cannot see the KiDS pattern either way: it is gas-rich discs with few bulges, and its per-galaxy outer residuals
  are too noisy for a ≈0.1–0.2 dex composition effect.
- Not tested, reported only (post hoc, no significance claimed): the mass coefficient b ≈ +0.06–0.07 dex per dex of
  M_b is positive in every cell — the same direction as KiDS's deficit growing with M*. A frozen test of a mass trend
  would be a separate lane.
- The time question is out of scope here (SPARC is z ≈ 0).

## Dated correction (2026-10-09, after CFG584)
The reading above said SPARC "cannot see the KiDS pattern". That was too strong: the orchestrator's CFG534 found a SPARC
early-type outer excess of +0.071 dex sorted by Hubble type (surviving a free M/L in CFG537 Part B; not replicated in
WALLABY, CFG537 Part A). CFG583's gas-fraction and bulge-fraction predictors did not detect a composition effect, but the
type split does show one in SPARC. The post-hoc mass slope noted above did not replicate in WALLABY (CFG584: −0.07,
Z ≈ −2). No verdict changes.
