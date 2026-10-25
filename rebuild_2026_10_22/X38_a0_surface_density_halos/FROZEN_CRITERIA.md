# X38_a0_surface_density_halos — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Hypothesis SD.** Cold dark energy (w ≈ 0, collisionless, not matter) clumps everywhere, as in route E: there is no law
force, gravity is Newtonian, and the RAR is emergent. Its halos are **cored, with central surface density pinned at the
framework's own scale**:

    ρ₀ r₀ = Σ_a₀ ≡ a₀ / (2πG),  a₀ = κ c √(G ρ_Λ)  →  107 (canonical) / 129 (alt) M☉ pc⁻²

The profile is Burkert, ρ = ρ₀ r₀³ / [(r + r₀)(r² + r₀²)]. This keeps a₀ = c²√(Λ/32π) as a constant of the cold sector,
not a coincidence: the halo's defining density. It adds zero new constants.

**Why test it.** It is the one route-E variant that ties the emergent scale to Λ. Cores address EM1's soft Υ failure,
where cusps forced Υ to 0.36. Route E already passes the red tiles by construction: growth/CMB, the forest, the Bullet
Cluster, TDGs, DF2/DF4. The open grades are SPARC and the cluster profile.

Standing rules:
- κ = ½ FITTED. Footings never pooled.
- No ΛCDM concentration–mass relation, halo model or HMcode. Σ_a₀ fixes the inner structure.
- Not "theory closed". Nothing here may say the data favour the framework. Cold dark energy is not matter.

## 1. SPARC (verdict-bearing)

- EM1's loader, mask, weights, Υ grid (0.30–1.20) and line, all copied: rms ≤ 0.110 AND median Υ ∈ [0.50, 0.80].
- **Halo mass:** EM1's committed global relation, lg M200 = a + b(lg M_b − 10), with (a, b) = (11.18, 0.90) on background A
  and (11.20, 0.90) on background B. It is borrowed from EM1's NFW fit and NOT refit here (disclosed: it was calibrated with
  NFW halos).
- R200 is taken at 200 ρ_c(z = 0) with each background's h (0.6758 / 0.6856).
- **r₀:** solve π Σ_a₀ r₀² B(R200/r₀) = M200, where B(x) = ln(1 + x²) + 2 ln(1 + x) − 2 arctan x.
- **Prediction:** g = g_bar(Υ) + G M_h(<r)/r², with M_h(<r) = π Σ_a₀ r₀² B(r/r₀). Υ is chosen per galaxy as in EM1.
- **Reported:** (a, b) refit in-sample for Burkert (EM1-style, 2 numbers, labelled IN-SAMPLE); EM1 NFW R1 and the law, for
  comparison.

## 2. Clusters (verdict-bearing): X30's machinery and keys, executed read-only

- **Halo:** Burkert at Σ_a₀, normalised so that M_h(<r_ta) = 5.364 M_b (fair share; clusters are closed boxes). Zero
  outside r_ta.
- **Gravity:** Newtonian on M_b + M_h, with no law. That is the route-E prediction, projected and lensed with X30's
  pipeline. A_pred = Σ d_N(M_b + M_h) / Σ d(C*), with C* the law on baryons, as measured.
- **Keys:** X30's G-MID-T1..T3, G-MID-b, G-OUT-all, G-OUT-T1..T3, G-OUT-b, G-IN-all (KT 106), and G-OUT-Mall,
  G-OUT-M1..M3, G-IN-Mall (all 326). |Z| ≤ 2 in both h cells.

## 3. Verdict (per footing; the class needs both footings to agree)

- **SD PASSES** — the SPARC line passes on both backgrounds AND every cluster key passes.
- **SD PASSES SPARC ONLY** / **SD PASSES CLUSTERS ONLY** — exactly one side passes.
- **SD FAILS** — neither side passes. The failing keys and SPARC legs are listed.

Reported: r₀ and ρ₀ for clusters (KT tercile medians); the SPARC rms and median Υ against EM1's NFW; Li+2020's measured
median 177 M☉ pc⁻² (SECOND_LAW_HUNT row 5), as context only. Not graded: dwarfs (the EM1 relation would be extrapolated
below 10⁸ M☉), growth, the forest and Bullet (route E inherits them), and lensing at galaxy scales.

## 4. Checks (all must pass; `--mutate` must fail K1)

- **K0:** EM1's law row is reproduced (rms 0.0541 / 0.0537 at Υ 0.52 / 0.44). X30's measured KT-all OUTER and MID are
  reproduced (0.716 / 1.668 canonical h 0.672).
- **K1:** Burkert B(x) closed form vs the quadrature of 4πr²ρ, to 1e-6. The solved r₀ returns M200 to 1e-8.
- **K2:** with the halo removed, SPARC returns EM1's Newtonian row (rms printed in EM1), and the clusters return d_N(M_b).
- **K3:** peak RSS < 2 GB; one thread; minutes.
- **MUTATE:** B(x) uses +2 arctan x instead of −2 arctan x; K1 must fail.
