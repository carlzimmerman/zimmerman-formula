# X37_orbit_conversion — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Hypothesis OC (owner session 10-25).** Cold dark energy (w ≈ 0, gravitating, clumps) converts into smooth dark energy
(w = −1) wherever it has completed many orbits. The fraction left is f = exp(−N_orb / N★). The converted part no longer
clusters, so it leaves bound systems. Since a₀ = κc√(Gρ_DE), a₀ rises slightly as conversion proceeds. One constant, N★.

This lane grades OC on the two constraints that killed the late-heating sheet:
- SPARC, which sets N★;
- the cluster INNER / MID / OUTER bands (X30's machinery and grading, executed read-only).

Standing rules: κ = ½ FITTED. Footings canonical / alt, never pooled. Raw shear bands against a framework-native
prediction. No ΛCDM concentration–mass relation, halo model or HMcode. N★ is set once, from SPARC only, and never fitted to
clusters. Cold dark energy is not matter and not a particle. Not "theory closed". Nothing here may say the data favour the
framework.

## 1. N★ from SPARC (verdict-bearing, no cluster input)

- N_orb convention is X19's: N_orb = t_age / t_orb, with t_orb = 2πr/V at the measurement radius and t_age = 13.8 Gyr. That
  is an upper bound, and the same convention is used for clusters.
- X22's numbers at the forest-allowed cut α_NF: gravity alone captures a median **cap = 0.760** of the fair share inside
  R_last. SPARC tolerates f_max = 0.1965 (canonical) / 0.0269 (alt) of the fair share.
- The binding SPARC galaxies are the least-orbited ones. N₁₆ = 9.301, the lower 16th percentile of X19's two SPARC classes
  (SPARC large).
- **N★ = N₁₆ / ln(cap / f_max).** This is the largest N★ for which the least-orbited sixth of SPARC is cleared, and so the
  value most favourable to retention in clusters.

## 2. The cluster profile under OC (per cluster, per footing, per h cell; X30's grid, gas, C* potential and lensing)

- **Unconverted cold dark energy:** collisionless secondary infall, ρ₀ ∝ r^(−9/4) inside r_ta (Bertschinger's self-similar
  slope; first-principles, not ΛCDM-calibrated), normalised to M₀(<r_ta) = 5.364 M_b (X30's `Mfair`), and zero outside r_ta.
  Reported variant: ρ₀ ∝ r^−2.
- **Orbits:** V(r) = √(g r), with g = X30's `gfun(M_b + M₀)` (the law on baryons + unconverted cold). Then
  N_orb(r) = t_age V/(2πr).
- **Retained:** ρ(r) = ρ₀(r) exp(−N_orb(r)/N★), and M_c(<r) = ∫ 4πr² ρ dr.
- **Prediction:** `dvec(i, foot, hk, M_c)`, giving A_pred = Σ d(C* + cold) / Σ d(C*) per band and per stack, exactly as X30.

## 3. Grades (X30's keys, measured values and σ read from X30's machinery; |Z| ≤ 2 in both h cells)

- KT sample (106): G-MID-T1..T3, G-MID-b, G-OUT-all, G-OUT-T1..T3, G-OUT-b, G-IN-all.
- All 326 clusters (OC is not KT-keyed, so these are graded as X30 graded its r = 0 points): G-OUT-Mall, G-OUT-M1..M3,
  G-IN-Mall.

## 4. Verdict (per footing; the class needs both footings to agree)

- **OC PASSES CLUSTERS** — every graded key |Z| ≤ 2.
- **OC INNER-ONLY** — only G-IN-all / G-IN-Mall fail.
- **OC FAILS CLUSTERS: <keys>** — otherwise. The failing keys are listed with their sign: pred > meas is OVER.

Reported, no verdict weight:
- profile fractions: retained / fair share, M_c(<0.15) / M_c and M_c(<0.5) / M_c, per KT tercile;
- the r^−2 variant;
- N★ × ½ and × 2 (sensitivity only; a class change there is reported, never adopted);
- the cosmic budget: the converted fraction is not computed (it needs a halo population the record does not own). Its
  sign is stated: ρ_DE rises, a₀ rises.

Not graded here: the forest and the CMB (no orbits before collapse, so OC is inert there by construction, stated not
tested), shear (X29-type), and the dwarfs (separate floor, X24).

## 5. Checks (all must pass; `--mutate` must fail K2)

- **K0:** X30's measured KT-all OUTER and MID values are reproduced to 1e-9 from the executed machinery (0.72 / 1.67
  canonical h 0.672, as printed in X30's README to 0.01). X30's C* vector for one cluster is reproduced exactly.
- **K1:** at N★ → ∞, M_c(<r_ta) = 5.364 M_b to 1e-6. At N★ → 0, the prediction equals C* exactly.
- **K2:** the r^(−9/4) profile's closed-form M₀(<r) equals the quadrature to 1e-6.
- **K3:** peak RSS < 2 GB; one thread; minutes.
- **MUTATE:** the exponent sign is flipped, so that f = exp(+N_orb/N★) is capped at 1, which keeps everything. K2's
  quadrature is run on the mutated profile, so K2 must fail.
