# KT28_tidal_filter_rule: the tidal filter rule SURVIVES on alt (MW 19 cells, Cassini 0.21x, dwarfs 15/24, SPARC +0.0005) and FAILS on canonical (MW, SPARC). Post hoc second attempt, corner cells only

Criteria: `FROZEN_CRITERIA.md` (c8b2586bb1), alone first, confirmed landed. `kt28.py` (KT27's code with the tidal rule: Cassini, dwarfs, SPARC), `kt28_mw.py` (KT26's code with ξ_tid(R0): Milky Way), their `.out`, `.json`, `.time`; `kt28_MUTATE.out/.json`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K840. 8 minutes each, 0.44 GB peak.

**Rule:** ξ_tid = (4/√3) τ³ / (|dτ/dr|² g*), τ = sqrt(g'² + 2(g/r)²) from the system's own field, g* = a0/κ. A uniform external field drops out (equivalence principle). The 4/√3 is fixed by the deep-MOND point mass (ξ = κ r_M), not fitted.

| test | canonical | alt |
|---|---|---|
| T0 MW: ξ_tid(R0), cells passing all four | 8.78 kpc, **0** (best D 2.19, Ou 131) | 7.26 kpc, **19** (14 at share 0.35, 5 at 0.26) |
| T1 Cassini Q2 / ceiling | 0.11, PASS | **0.21, PASS** |
| T2 dwarfs (line ≥ 15/24) | 15/24, PASS | **15/24, PASS** (Fornax kept: ξ_tid(a) 0.12 kpc vs r_M/2 0.11) |
| T3 SPARC d rms / median | +0.0079 / +0.072, FAIL | **+0.0005 / +0.043, PASS** |
| **Label** | **TIDAL RULE FAILS: MW, SPARC** | **TIDAL RULE SURVIVES** |

## Reading
- **On alt, a local, mass-free filter rule now passes all four tests.** It replaces "system mass" (KT17/KT25) with the tidal field, and it keeps the ½: deep in an isolated system it gives exactly r_M/2. It fixes both earlier problems: KT25's global form failed Cassini on alt, and KT27's local form failed the dwarfs. Blind to the uniform field, a Milky Way satellite gets about its isolated length, and Fornax comes back.
- **On canonical it fails.** The MW's outer curve misses at ξ 8.8 kpc, and SPARC loses too much inner phantom.

## As hard as a fail
- **Post hoc.** This is the second local rule, chosen after KT27's Fornax miss. The lines were frozen before running, but two tries were made.
- **The MW pass is corner cells only.** All 19 are BV2, R_d 2.6, Σ_b 53.9 (+2σ), M_bb 1.88-2.12e10 (top of the box), at thick-disc share 0.26-0.35. There are none at the star-count share 0.12. 0.26 matches Lian+22's APOGEE chemical share (provisional lookup). Strict h fails everywhere (3.21). The MW arm is one ξ value at R0, in-plane only: the vertical tidal component (local disc density) isn't in τ.
- **SPARC passes near the median line** (+0.043 vs 0.05); inner points lose phantom (inner median -0.006 → +0.050).
- **The dwarfs and Cassini add nothing beyond surviving.** The dwarfs are the same 15/24 as plain QUMOND and as r_M/2. Cassini passes by a factor of 5, not 100.
- **Approximations:** spherical, row-wise; the τ gradient is the radial derivative; the field isn't iterated; SPARC smooths ln τ over 0.1 in ln r (R3: changes ξ 0.4 %); row-wise smoothing doesn't conserve mass (SPARC total ratio 0.43-1.11). A full solve of the tidal-filtered field equation hasn't been done.

## Checks
R1 reproduces KT25 on all three (0.4806/1.057, 15/24, +0.0021/-0.0006). R2 1.00001. R3 0.004. MW: C1, C2 pass; KT17's C3 half-space factor fails again (known, the reason `kt28_mw.py` exits 1); Q5 doubled grid dK +0.06, dv +0.07. MUTATE (ν = 1): Cassini Q2 0, SPARC fails (0.573).
