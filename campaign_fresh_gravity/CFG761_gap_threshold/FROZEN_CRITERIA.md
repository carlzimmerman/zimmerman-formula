# CFG761 FROZEN CRITERIA: where exactly does P radiation switch on? (hardening CFG760's pincer)

Date: 2026-10-13. Block CFG760–769. Written and committed ALONE, after CFG760's run (its G2 margins are known: closest case
M_b = 10⁹ M☉, y = 0.1, c_P,min/c_P,max = 1.73 canonical / 1.36 alt) and BEFORE any CFG761 script or number. κ = ½ FITTED; both
footings, never pooled; the cold energy's mass is required; no particle species; not "theory closed".

## Why
CFG760's G2 used the WKB exponent ΔE ≤ 1 to set the radiation threshold. CFG760 G1 showed that WKB misses near the gap edge
(s₀ = 20, ω/ω_g = 0.7: S = 0.23 vs e^{−5.35}). The closest G2 case closes by less than a factor 2, so the threshold position decides
it. This lane measures the threshold directly from the exact Green's function, with no WKB.

## Method (CFG760's equations, frequency domain, code copied)
- x = ω/ω_g(s₀) on the grid 0.30, 0.31, …, 1.50; s₀ ∈ {20, 50, 200, 1000, 5000}. S(x, s₀) = P_full/P_ref exactly as in CFG760.
- **x_e(s₀)** = the smallest grid x with S ≥ e^{−1} (favourable: radiation counts from the first frequency at which it reaches e^{−1}
  of the uncurved reference, however narrow the window).

## Controls
- **K1.** Reproduces CFG760's G1 values of S at (s₀, x) ∈ {(20, 0.5), (50, 0.5), (50, 0.7), (200, 0.7)} to ≤ 1e-6 relative.
- **K2.** The flux invariant Im(u₂*u₂′), evaluated only where k² > 0 beyond the outer turning point, is constant to ≤ 1e-6. (CFG760's
  K2 also evaluated it inside the barrier, where it is a difference of numbers of order e^{ΔE}; that failure is disclosed there.)

## Tests
- **T1 (sharpening).** x_e(s₀) is non-decreasing across the five s₀, and x_e(5000) > x_e(20).
- **T2 (re-scored pincer).** c_P,max = V/(x_e,min · ω_g(s₀) · s₀) at each physical case, with x_e,min the minimum of x_e over the five
  s₀ (the most generous measured value; conservative at physical s₀ ~ 10⁵–10⁹ only if T1 holds). Same cases, V = 2V_f, L* = 5.754 pc
  and lenient c_P,min = r/13.8 Gyr as CFG760 G2. **CLOSED iff c_P,max < c_P,min for every case, both footings.**
- If T1 FAILS, T2 is reported but the verdict is **NOT ESTABLISHED** (the threshold at physical s₀ is then not bounded by the
  measured range).

**MUTATE** (`CFG761_MUTATE=1`): no vacuum curvature. Then S ≡ 1, x_e = 0.30 (the grid floor) at every s₀, T1 must FAIL and T2
must not be CLOSED. Exit 1 iff both bite.

## Not tested
Same as CFG760: non-spherical modes, large-amplitude effects, the saturating W inside r_M, other export channels.
