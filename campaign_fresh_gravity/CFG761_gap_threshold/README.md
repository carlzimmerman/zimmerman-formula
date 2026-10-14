# CFG761: the P-radiation threshold sharpens toward the gap; the pincer is OPEN as frozen by a 3% sliver in one dwarf case

**Label: T1 PASS (sharpening), T2 OPEN as frozen ⇒ overall OPEN.** Exactly one case of 16 opens (alt footing, M_b = 10⁹ M☉,
y = 0.1: margin 0.97), and only under the deliberately generous threshold the criteria fixed in advance. K1, K2 PASS. MUTATE bites
(exit 1).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (364fc9c73), after CFG760's numbers and before any CFG761 number.
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg761.py` (~20 min, < 100 MB; CFG760's equations, code copied) →
  `cfg761.out`, `cfg761_results.json`. `CFG761_MUTATE=1` (no vacuum curvature) exits 1: x_e = 0.30 everywhere, T1 fails, T2 opens.
- **Settings:** κ = ½ FITTED; L* = 5.754 pc; cubic W; the cold energy's mass is required; no particle species; not "theory closed".

## Results
x_e = the smallest ω/ω_g at which the exact suppression S reaches e^{−1}:

| s₀ | 20 | 50 | 200 | 1000 | 5000 |
|---|---|---|---|---|---|
| x_e | 0.71 | 0.77 | 0.86 | 0.94 | 0.96 |
| S at ω/ω_g = 0.9 | 0.21 | 0.13 | 0.070 | 2.0e-3 | 5.2e-6 |

- **T1 PASS:** the switch-on moves up to the gap itself as s₀ grows, and the edge gets steeper (S at 0.9ω_g falls ×4×10⁴ from
  s₀ = 20 to 5000). Physical halos sit at s₀ ≈ 10⁵–10⁹.
- **T2 OPEN as frozen.** The rule used x_e,min = 0.71 (the s₀ = 20 value) at every physical case:
  - canonical: all 8 closed (margins 1.23, 6.9, 6.9, 39, 39, 219, 219, 1233);
  - alt: 7 closed (5.5–973) and **10⁹ M☉, y = 0.1 OPEN** (c_P,max 256 m/s vs c_P,min 249 m/s, margin 0.97).
- K1: CFG760's G1 values reproduced exactly. K2: flux invariant beyond the turning point holds to 3e-9 (CFG760's K2 failure was
  the in-barrier evaluation, as disclosed there).

## Reading
1. **As frozen, the door is open**, by a 3% sliver: alt footing, the outskirts (3.5 kpc) of a 10⁹ M☉ dwarf, c_P ≈ 249–256 m/s,
   under a threshold taken from s₀ = 20 although the case sits at s₀ = 2.4×10⁵.
2. **Post-hoc (no verdict weight).**
   - With the largest measured s₀ (x_e = 0.96, s₀ = 5000) the same case would close (margin ≈ 1.3).
   - **c_P is one constant for every system.** The c_P that opens the dwarf case (≈ 250 m/s) leaves every system ≥ 10¹⁰ M☉
     closed by ×30–1000, because their halos would need c_P ≥ 2.5–27 km/s just to be crossed in a Hubble time. No single c_P lets
     P radiation export infall energy across the galaxy population.
3. **Together with CFG760:** P radiation is not a working export channel for cold-energy infall in L* ≥ 5.75 pc theories, except
   possibly a narrow dwarf-outskirts sliver with c_P ≈ 250 m/s. A follow-up must freeze the "one c_P for all systems" test before
   that can be called closed.
