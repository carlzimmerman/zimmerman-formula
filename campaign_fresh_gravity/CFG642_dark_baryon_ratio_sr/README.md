# CFG642 — non-numerology symbolic regression for Ω_c/Ω_b: CHANCE-LEVEL

Criteria: `FROZEN_CRITERIA.md` (commit a51c1ab0f, committed alone before any code). Script: `cfg642_sr.py`
(`cfg642.out`, `cfg642_results.json`); planted-target control: `MUTATE=1` → `cfg642_MUTATE.out` / `_results.json`.
One process, ~100 s, 0.66 GB peak.

**Target.** Planck 2018 ω_c/ω_b = 5.3643 ± 0.0646 (1.204%). BBN route (Cooke+18 D/H, CAMB PRIMAT 2024
inversion): ω_b = 0.02193 ± 0.00022 → 5.4715 ± 0.0770 (PArthENoPE bracket 0.02270 → 5.2866).

**Grammar.** Buckingham-π monomials P · (Gρ_b/H²)^n1 (Gρ_r/H²)^n2 (Gρ_DE/H²)^n3 (a₀/cH)^n4 κ^n5, all at one
named epoch (today, z* = 1089.92, z_eq, BBN T = 0.07 MeV); n_i ∈ {−2…2 step ½}; 11 geometric prefactors
(1, 2^±1, π^±1, (4π)^±1, (8π)^±1, (8π/3)^±1). 2,598,156 members per footing; the original law
a₀/(cH₀) = κ(Gρ_DE)^½/H₀ is expressible (checked). Footings searched separately.

| | canonical | alt |
|---|---|---|
| N_eff (distinct values) | 1,598,139 | 1,598,139 |
| distinct values in [1,10] | 37,196 | 37,227 |
| distinct values within 1σ | 375 | 399 |
| clean subspace N_eff (|ε_c| ≤ 0.05 + epoch rule) | 34,465 (2,055 in [1,10]; 14 within 1σ) | 57,401 (1,764; 17) |
| gate (a) full: p_rand / p_shuf | 0.68 / 0.56 | 0.57 / 0.47 |
| gate (a) clean: p_rand / p_shuf | 0.38 / 0.64 | 0.40 / 0.62 |

The real best MDL score sits at the median of the decoy distributions (canonical: real 10.16 bits vs decoy
median 9.44; alt 9.69 vs 9.46). Required: p < 0.0005. **Gate (a) fails everywhere.**

**Top candidates and what kills them** (`cfg642.out` lists 15 + 10 per footing with every gate):
- canonical best `2 (a₀/cH₀)^−½` today (z −1.18): today-epoch and time-dependent (epoch rule), ε_c +0.10
  (circular via ρ_DE), fails b1, d1, d2.
- alt best `(Gρ_b/H₀²)^−½ (a₀/cH₀)^½` today (z +0.86): epoch rule, fails d2 (h-dependent).
- clean best (both footings) `(1/π)(Gρ_r/H²)^−1` at equality = **16/3 = 5.333** (z −0.29): at equality the
  Friedmann equation forces Gρ_r/H² ≡ 3/(16π), so this is a pure number in disguise (a definitional identity,
  not physics); fails d1 (BBN route z −1.8).
- Of all 1σ members, exactly one passes (c)+epoch+(d1)+(d2) (canonical, BBN epoch, contains a₀ via
  (a₀/cH)²/(Gρ_DE/H²) ≡ κ²): it fails b1 (z = +38.6 in the alt footing). None passes (b): b3 needs a mechanism.

**Power / controls.**
- Injected true formulas (200 clean grammar members, C ≤ 6) are certified by gate (a) in 4/200 at the real
  1.2% precision, 2/200 at 1e-3, 29/200 at 1e-5, 189/200 at 1e-7. The grammar has only 1.6M distinct values
  and stays this dense: at 1.2% precision no search of this kind can certify even a TRUE relation.
- MUTATE (one member planted at 0.001%): found exactly (z = 0.000), but p_rand 0.015 / 0.0017 clean →
  NOT certified. The frozen expectation that MUTATE passes was wrong. That is a power limit (consistent with
  29/200 at 1e-5), not a bug.
- TRUE-VALUE control (F ≡ 5.364): b2 Ω_m = 0.315 vs DESI 0.2975 (z +1.77, inside 2σ), d1 z −1.39, d2 0.
- Naive space (16,384 two-term expressions with e, φ, √7): 49 within 1σ. e + √7 = 5.36403 (z −0.005) is the
  closest, and 10.2% of random decoys get a match at least that close (p ≈ 0.10). Every decoy (100%) has a
  1σ match. That makes it a chance hit.

**Verdict: CHANCE-LEVEL.** The non-numerology grammar matches 5.364 no better than it matches random numbers.
Ω_c/Ω_b at 1.2% carries ~6 bits, under atomos's 10-bit threshold, so value-matching alone cannot find it. A
real relation would have to come from a mechanism with a second, independent prediction (the interlock that
made a₀ = κc√(Gρ_DE) real), not from a search. κ = ½ FITTED; nothing here derives 5.364; not theory closed.
Disclosures: Planck ω_b–ω_c covariance not on disk (treated as uncorrelated). Planck h is itself fit with ω_c
(h held fixed in ε_c; checked separately by d2). Decoy range is log-uniform on [1,10].
