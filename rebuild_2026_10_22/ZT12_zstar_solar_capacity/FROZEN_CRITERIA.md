# ZT12_zstar_solar_capacity — FROZEN CRITERIA (committed with the ledger, before any script or number)

New Z★ test (Z-T12; flagged by ZT11, e977f1a22f): **does R1's upper obstacle 0 ≤ D·P ≤ ρ_d, which caps the Sun's screened
hedgehog inside r_nl = M☉/(2πL★²ρ_d) (60–970 AU), break Solar-System screening?** κ = ½ FITTED. Footings 9.3603e-11 /
1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.
One thread, < 1 GB, seconds.

## 1. Mechanism to derive (sympy, in the script)

Static Lagrangian of C6 (`covariant_push_2026_10_22/C6_literal_cassini/README.md`): −|∇Φ|²/2K + p·∇Φ − W(K|p|) −
(γ_L/2)(∇·p)² − ρΦ, with the screened (|p| ≪ a₀) limit of W, in spherical symmetry with K absorbed as in C6's (L), (P_L).

- **M1 (reduction).** Substitute the Φ equation (Φ′ = g_N + p) back into the Lagrangian density. Claim: all p-dependence
  cancels except through D = ∇·p, so the reduced functional is local in D: F[D] = −∫ r² [(γ_L/2) D² + Φ_N D] dr (Green
  reciprocity for ∫ρΦ_D = ∫Φ_N D). Residual must be 0.
- **M2 (free solution).** Stationarity of F gives (L★²/2) D′ = −g_N: D_v3s = 2GM/(L★² r) + const (C6's hedgehog,
  M/(2πL★²r) of density). Residual 0.
- **M3 (obstacle).** Because F is local and strictly convex in D, minimising it under the pointwise constraint
  0 ≤ D ≤ Kρ_cap gives D_Z★ = min(max(D_v3s, 0), Kρ_cap) pointwise. Check numerically: a projected-gradient minimisation of the
  discretised F on a radial grid with the cap agrees with the clamp to 1e-6 (relative, max over the grid), and the exterior
  r > r_nl is unchanged to 1e-6.
- **M4 (monotonicity).** p(r) = r⁻² ∫₀^r D r′² dr′ with D_Z★ ≤ D_v3s pointwise ⇒ p_Z★(r) ≤ p_v3s(r) at every r. Closed forms:
  p = (4π/3)Gρ_cap r for r ≤ r_nl; p = (GM/L★²)(1 − r_nl²/(3r²)) for r > r_nl.

## 2. Brackets for ρ_cap (the cap the Sun's hedgehog sees)

- **B0**: ρ_cap = 0. Stars own no dust (Z★ rule R2: they move through the medium faster than their own escape speed), or the
  local dust is fully committed to the Milky Way's smooth phantom. The Sun has no hedgehog.
- **B1**: ρ_cap = ρ_ph(R₀), the local held density from ZT11's MW table (0.0588 / 0.0676 M☉ pc⁻³; ZT11's reading).
- **B2**: ρ_cap = 10 ρ_ph(R₀) (free dust present).
- **B∞**: no cap = v3s = C6's numbers (reproduced, check KC6).

L★ ∈ {24, 50, 90} pc (C6's set); both footings (they enter through ρ_ph).

## 3. Scored rows

- **Planets.** Anomalous radial acceleration from the Sun's held dust at Earth (1.000 AU), Mars (1.524 AU) and Saturn (9.537 AU)
  against C6's bounds (8.7e-15, 1.4e-15, 7.0e-15 m/s²).
- **Cassini quadrupole.** Conservative bound Q₂,Z★ ≤ Q₂,C6(max over E0–E3) + 4πGρ_cap (the largest traceless tidal tensor a
  uniform saturated ball of any shape can add), against Hees 2014 (9.0e-27 s⁻²) and Park 2026 (5.2e-27 s⁻²) as used by C6.
- **Wake (reported).** Gravitational focusing of the medium streaming past at 230 km/s raises the local dust by at most
  2GM/(r v²); its uniform-ball acceleration at each planet is reported against the same bounds.
- **Ambient (reported, common to v3s and Z★).** The Milky Way's own held density ρ_ph as a uniform ball about the Sun,
  (4π/3)Gρ_ph r, against the planetary bounds.

**Verdict.** PASS iff every planetary ratio and both quadrupole ratios are ≤ 1 in B0, B1 and B2, at every L★ and footing.
FAIL iff any ratio exceeds 1 in B0 or B1 (the design's own readings). Otherwise CONDITIONAL (fails only at B2).

## 4. Checks and `--mutate`

`zt12_solar_capacity.py`: KM1, KM2 (sympy residuals 0), KM3 (projected minimiser = clamp, exterior unchanged, 1e-6), KM4 (closed
forms vs numeric integral, 1e-6; p_Z★ ≤ p_v3s on the grid), KC6 (v3s planetary ratios reproduce C6's R2 rows to 1e-3), KZ11
(r_nl at B1, 24 pc, canonical = ZT11's 970 AU within 2 %), KR (RSS < 1 GB). Exit 0 iff all pass. `--mutate`: the obstacle is
applied to p instead of D (a non-local cap) → KM3 fails (exit 1). Outputs `zt12_solar_capacity{,_MUTATE}.out`,
`_results{,_MUTATE}.json`. Post-result changes go in a dated AMENDMENT.
