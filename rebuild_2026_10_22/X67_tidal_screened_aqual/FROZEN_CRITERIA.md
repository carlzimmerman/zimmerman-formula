# X67_tidal_screened_aqual: FROZEN CRITERIA (committed alone, before any script or number)

Source: the external model's fourth proposal, relayed by the owner in chat (10-29) after X66. The owner said "run X67".

Standing: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m s⁻², never pooled. Σ_a₀ ≡ a₀/(2πG).
Cold dark energy is not matter and not a particle. No ΛCDM input. Not "theory closed". Lane id X67.

**Pre-flight (computed in chat before freezing, on an exact Burkert profile):**
- g_N C² / (2πGρ₀r₀) = 0.31, 0.59, 1.00, 1.20, 0.94, 0.58, 0.23 at r/r₀ = 0.5, 1, 2, 5, 10, 20, 50.
- The proposal's table (2.88, 3.16, 1.72 at 5, 10, 50) is wrong.
- Expectation stated in advance: the screening reopens beyond about 20 r₀, so an X65-like failure is likely.
- a_crit = a₀/2 is chosen by the proposal, not derived.

## The law (as proposed)

This is X65's law with the μ argument multiplied by C². Here C = max(1, ρ̄(<r)/ρ_c(r)) and ρ̄(<r) = 3M(<r)/(4πr³), with
μ(u) = u/(1+u⁴)^(1/4) and u = g_φ C²/(a₀/2).

Field equation (first integral): μ(u) g_φ = g_NQ, where g_NQ = G M_Q(<r)/r² with X65's Q.
Exact solution:
- y = g_NQ C²/(a₀/2) and w = (y⁴ + √(y⁸ + 4y⁴))/2;
- u = w^(1/4) and g_φ = (a₀/2) u / C².

Force: a = −g_N − Q (g_φ − g_NQ) + L²/r³.

**Stated reductions:**
- The proposal's action, varied, gives an extra factor C⁴ multiplying μ and terms from C's dependence on Φ_N. Both are
  dropped; the test uses the field equation exactly as the proposal wrote it.
- ρ_c uses X66's chunk estimator (K = 32, 3-chunk smoothing), mapped to each shell's chunk.

## Runs (X65 / X66 numerics otherwise unchanged)

- **N runs:** j = 0.1 at all six masses (1e9–1e14 M☉); j = 0.05 and 0.2 at 1e9, 1e10, 1e11, 1e13.
- **G runs:**
  - canonical and alt, j = 0.1, all masses;
  - canonical, j = 0.05 and 0.2, at 1e9, 1e10, 1e11, 1e13;
  - canonical, N = 1000, at 1e9 and 1e10.
- **MUTATE** (a_crit = a₀ instead of a₀/2): canonical, j = 0.1, all masses. Separate outputs.

## Pre-checks, verdict, flags: identical to X66

- **Pre-checks:** E1 (Newtonian runs |ΔE/E| ≤ 2 %), S1 (Q = 0 whenever r is monotonic in q).
- **Floor:** per footing, FLOOR EMERGES / RAISES, NO FLOOR / NO EFFECT, using S = masses with R_N < 0.7 and window
  [0.67, 1.5] with spread ≤ 0.2 dex.
- **max() rule:** REPRODUCED if |Δ| ≤ 0.1 dex at every mass with R_N > 1.5; otherwise BROKEN.
- **j-robustness:** ROBUST / j-DEPENDENT, with the same cases as X66.
- **Resolution:** N = 1000 within 0.1 dex of N = 2000 at 1e9 and 1e10; otherwise UNRESOLVED.
- **Threshold sensitivity:** the median log₁₀ R over S must rise by ≥ 0.2 dex under MUTATE; otherwise
  THRESHOLD-INSENSITIVE.
- **OVERALL PASS** requires all of them.

Also reported: the final mass fraction where μ(u) < 0.9 (boost active), and the radius range of that zone in units of r₀.
