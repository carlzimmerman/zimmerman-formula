# CFG376: CFG374 MIX-A with the collapsed phase split into hot halo gas + stars/cold gas. TENSION (σ₈ fine; P(k = 1) +10.0% / +12.5% under the frozen filter, which has a KNOWN BUG, so these are LOWER LIMITS)

Criteria 2f4c18600 (committed alone, before any script). Engine `cfg376_pm.py` (a CFG374 copy; only the MIXES weights and one extra phase term changed), launcher `cfg376_run_all.py`, controls `cfg376_checks.py` (C1a–c and MUTATE pass), analysis `cfg376_analysis.py` → `cfg376_analysis.out`, `cfg376_results.json`. RES rule, R_c = 3 Mpc/h, A0-FLAT, 256³, seed 359, 150 steps; S0 = CFG359 256³ (read-only).

**Weights (fractions of all baryons).** Cool 1e4 K 0.28, WHIM 1e6 K 0.54 (both as CFG374 MIX-A), hot halo gas 0.10 at T_halo, and stars + cold gas 0.08 unfiltered. The 18% collapsed total comes from Shull, Smith & Danforth 2012, and I checked it in the arXiv abstract. The 0.08 / 0.10 split is **not verified from a source read this session**. It is recalled from Shull+2012 and Fukugita & Peebles 2004, with a declared bracket f_sc ∈ [0.07, 0.09]. Across that bracket W(k = 1, z = 0) moves only 0.436–0.454 (central 0.445), worked out analytically, not run.

| variant | footing | σ₈ ratio | max \|P−1\|, k ≤ 1 | P at k = 0.1 / 0.3 / 1 | verdict |
|---|---|---|---|---|---|
| HALO-A, primary (T_halo = 10^6.5 K) | canonical | 1.012 | 0.1005 | 1.008 / 1.035 / 1.099 | TENSION (misses the 10% cut by 0.0005) |
| HALO-A | alt | 1.015 | 0.125 | 1.011 / 1.044 / 1.124 | TENSION |
| HALO-B, conservative (10^6 K) | canonical | 1.013 | 0.105 | 1.009 / 1.037 / 1.103 | TENSION |
| HALO-B | alt | 1.016 | 0.130 | 1.011 / 1.046 / 1.129 | TENSION |

**Lane verdict (frozen filter): TENSION.**
- σ₈ is within 1.2–1.6%, well inside the 5% cut.
- Small-scale power at k = 1 is +10.0% (canonical, exactly at the cut) and +12.5% (alt) for HALO-A.
- Filtering the halo gas moves CFG374 MIX-A (+12.4% / +15.6%) about a fifth of the way toward CFG372's pure-1e6 K pass (+7.6% / +8.9%).
- The alt footing fails the P cut clearly in both variants.

**CMB-lensing proxy (not scored).** The mean P ratio over k = 0.05–0.2 at z = 0.5 is 1.005 / 1.006, so A_lens − 1 ≲ +0.5% (z = 1: 1.002).

**Controls.**
- C1a: the weights sum to 1. C1b: W(0) = 1 at all a.
- C1c: T_halo → 0 reproduces CFG374 MIX-A's W to 1e-16.
- MUTATE (CFG376_MUTATE=1, `cfg376_checks_MUTATE.out`): f_sc = 1 gives W ≡ 1, differing from HALO-A by 0.555 at k = 1.
- All checks are at the algebra level. No field-level re-run.

## KNOWN BUG (audit 5819dd616)
The Jeans wavenumber inherited from CFG372 (and CFG374) is coded as k_J = √(1.5 Ω_m **a**) · 100/c_s.
- The correct comoving value is k_J = a·√(4πGρ̄)/c_s = √(1.5 Ω_m **/ a**) · 100/c_s, which goes as a^(−1/2). I re-derived this independently.
- The two agree only at z = 0. At earlier epochs the frozen filter OVER-filters the phantom source.
- For this lane's HALO-A mix at k = 1 h/Mpc, W is 0.389 (coded) against 0.522 (correct) at z = 1, i.e. ×1.34. At z = 3 it is 0.342 against 0.621, ×1.8.
- For a pure 1e6 K phase at z = 1 the factor is ×3.1 (0.093 against 0.291).
- So the phantom source in these runs is too weak at z > 0. **The small-scale excess (and the σ₈ shift) reported above are LOWER LIMITS.** The corrected filter will give larger P(k = 1) excesses, so the TENSION verdict cannot turn into a pass by fixing the bug.
- The same bug affects CFG372's GROWTH OK and CFG374's numbers.
- These runs were finished unchanged under the frozen criteria. Corrected runs are the orchestrator's amendment, not run here. Nothing committed was rewritten.

**Scope.**
- Linear, constant-temperature phase filters, with z ≈ 0 fractions applied at all z, on a collisionless run.
- Treating all 10% halo gas as hot is optimistic, because part of the CGM is cool.
- The reservoir is bookkeeping, and the settling force is conditional (CFG373).
- κ = ½ is fitted. No dark-matter particle: the cold fluid is still required.
