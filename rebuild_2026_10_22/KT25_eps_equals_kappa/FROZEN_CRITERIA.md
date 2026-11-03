# KT25_eps_equals_kappa — FROZEN CRITERIA (before any script or number)

Hypothesis: the filter's smoothing fraction ε (KT17: ξ = ε sqrt(G M_b / a0), ε = 0.55 passes, window about 0.5 to below 1,
not derived) is **the same number as κ**: ε ≡ κ = 1/2, so ξ = r_M / 2. Two unexplained numbers would become one. This is a
reduction, not a derivation: it doesn't explain why 1/2.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
No download.

**Not blind, expectation on record:** KT16's Cassini threshold is ξ/r_M >= 0.450 (canonical) and 0.504 (alt), so I expect
canonical to pass Cassini and **alt to fail it narrowly** at 0.5. KT17 passed MW at ε 0.55 (canonical 5 cells, alt 62) and
failed at 1.0 (v_c too low), so ε 0.5 should keep v_c; whether K_z still passes is open. KT18 and KT22 showed the share
dependence at 0.55.

## Method
- `kt25.py`: KT17's `kt17.py` with EPS = [0.5] (MUTATE keeps KT17's own [1.0]); Cassini (KT16 integral), 24 dwarfs (KT15
  model) and the 1375 in-prior MW cells per footing, unchanged otherwise. Passing MW cells reported by thick share.
- `kt25_sparc.py`: KT19's `kt19.py` with EPS = 0.5, unchanged otherwise.

## Labels, per footing
**ε = κ SURVIVES** if all four hold: Cassini Q2 <= 5.2e-27 s^-2; dwarfs >= 15/24 with the MW external field; at least one
in-prior MW cell passes L1, L2a, L2b and L3; SPARC d rms <= 0.005 and |median| <= 0.05. Otherwise **ε = κ FAILS: <tests>**.
Beside: MW passes at the star-count share 0.12 (expected none); strict h.

## Checks
KT17's and KT19's checks as they are (KT17's C3 half-space factor and KT19's C3 envelope are known failures; disclosed again if
they recur, not fixed here). MUTATE for both: KT17's and KT19's own MUTATE paths.
