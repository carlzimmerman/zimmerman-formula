# CFG760: the law's own vacuum gives P perturbations a mass gap, so galaxy-scale cold-energy motions barely radiate

**Label: G2 CLOSED (pincer), G3 hatch CLOSED; G1 FAIL as frozen (WKB misses near the gap edge); K2 and K3 FAIL as frozen
(disclosed below); K1, K4, K5 PASS. MUTATE bites (exit 1).** The closest G2 case closes by less than ×2, so CFG761 measures the
threshold directly.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (6f2ee620b), 2026-10-13. Block CFG760–769.
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg760.py` (a few minutes, < 100 MB) → `cfg760.out`, `cfg760_results.json`.
  `CFG760_MUTATE=1` (vacuum curvature removed) exits 1: G1 fails (S ≡ 1) and G2 opens. `CFG691_copy.py` is CFG691's SPARC
  statistic, checked by K5.
- **Settings:** κ = ½ FITTED; L* = 5.754 pc; cubic W; the cold energy's mass is required; no particle species; not "theory closed".

## The idea
Linearise CFG696's P-field equation about the law's own static profile v₀. The cubic W, which *is* the deep law, gives small
perturbations a position-dependent mass term 2|v₀|/s. A motion at code frequency ω radiates P waves only above the local gap
ω_g = √(2|v₀|/s + 2/s²); below it the response is confined and leaks out only by tunnelling. A galaxy-scale motion at radius r
has ω = (V/c_P)/s₀ with s₀ = r/ℓ_γ ~ 10⁵–10⁹, so radiation needs c_P ≲ V/√(2s₀), while P's own relaxation needs c_P ≥ r/t.

## Results
**G1/K4: the gap is real.** Point source, exact Green's function, suppression S = P_full/P_ref (reference = no vacuum curvature):

| s₀ | ω/ω_g = 0.5 | 0.7 | 2 (above) |
|---|---|---|---|
| 20 | 2.4e-8 (WKB e^−15.6; ratio 1.13) | 0.23 (WKB e^−5.3; **ratio 0.27**) | 1.06 |
| 50 | 1.3e-11 (ratio 1.02) | 1.1e-4 (ratio 1.08) | **6.7** |
| 200 | 1.1e-22 (ratio 1.03) | 2.5e-6 (**ratio 0.76**) | **0.15** |

Deep below the gap, S follows e^{−ΔE} to 2–13%. K4: CFG696's full nonlinear equation in the time domain gives below/above-gap
flux 2.6e-8 and S_td/S_fd = 1.02 above the gap (PASS).

**G2: the pincer (L* = 5.754 pc, V = 2V_f, lenient one-crossing c_P,min = r/13.8 Gyr).** CLOSED in all 16 cases, both footings:

| case | c_P,max (export) | c_P,min (relax) | margin, can / alt |
|---|---|---|---|
| 10⁹ M☉, y = 0.1 (3.5–3.9 kpc) | 158 / 182 m/s | 273 / 249 m/s | **1.73 / 1.36** |
| 10⁹, y = 0.01 and 10¹⁰, y = 0.1 | 89–102 m/s | 0.79–0.86 km/s | 7.7–9.7 |
| 10¹⁰, y = 0.01 and 10¹¹, y = 0.1 | 50–57 m/s | 2.5–2.7 km/s | 43–55 |
| 10¹¹, y = 0.01 and 10¹², y = 0.1 | 28–32 m/s | 7.9–8.6 km/s | 244–309 |
| 10¹², y = 0.01 (350–390 kpc) | 16–18 m/s | 25–27 km/s | 1370–1740 |

CFG744's frozen relaxation law would need c_P ≥ 10⁶–10⁹ m/s instead of the one-crossing bound; with it, every margin is ≥ 10⁴.

**G3: a larger L* weakens the gap**, but it opens every case only at L* ≈ 9.5 kpc (canonical) / 7.6 kpc (alt), where SPARC's rms
is 0.172 / 0.161 (bar 0.110; K5 reproduces CFG691 to < 1e-4). CLOSED.

## Disclosures (2026-10-13)
- **G1 FAILS as frozen.** At the edge of the gap (s₀ = 20 and 200, ω/ω_g = 0.7) WKB overstates the suppression (ratios 0.27,
  0.76). The [0.8, 1.25] band was set for the deep regime. G2 uses the WKB ΔE ≤ 1 threshold, so its c_P,max can be too small near
  threshold. That matters only for the 10⁹ M☉, y = 0.1 case (margin < 2), so **CFG761 measures the threshold exactly** (criteria
  committed before any number).
- **K3 FAILS as frozen.** Above the gap S is not near 1. It oscillates (0.15–6.7) because the curvature changes the standing-wave
  factor between the regular origin and the source. Radiation is not suppressed there, but the frozen [0.3, 3] window was naive.
- **K2 FAILS as frozen** at s₀ = 50 and 200, ω/ω_g = 0.5 (spread 7e-7 and 3e4). The invariant was evaluated inside the barrier,
  where Im(u*u′) is a difference of numbers of order e^{ΔE} (e^{49} at s₀ = 200). Outside barriers it holds to 1e-10. CFG761
  evaluates it beyond the turning point only.
- The threshold criterion ΔE ≤ 1 is favourable: it assumes the free problem would radiate all the infall energy every orbit.

## Reading
1. **The law's vacuum stiffens against slow motions.** Around any galaxy, small P disturbances behave like a field with a local
   Compton length √(rℓ_γ/2), only ~0.1–20 pc at L* = 5.75 pc. Motions slower than c_P over that length can't radiate.
2. **So P radiation can't be the export channel** for cold energy arriving at infall speeds: the c_P it would need is ≤ 16–180 m/s,
   and at that speed the P field could not even cross the halo in a Hubble time. This closes the last dissipation route inside
   the action (CFG744's damping) on CFG760's frozen criteria. **CFG761 (exact threshold) reopens one dwarf-outskirts case by 3% as
   frozen**; see its README.
3. **Side benefit, reported.** The same gap means stellar bars, satellites and binaries don't lose orbital energy to P waves.
4. **Where it points.** Other export routes are astra's (receiver, selective cooling, photon bath) and CFG750's sink. If they
   close too, cold energy can't be assembled by infall and must be **formed at rest** in each system's frame (in-situ production,
   F1/F5).

## Not tested
Non-spherical modes (they add stronger ℓ(ℓ + 1)/s² barriers), large-amplitude nonlinear effects, the saturating W inside r_M, other
export channels.
