# CZ4_solar_neighbourhood_filter — FROZEN CRITERIA (before any script; no new number computed)

Owner, 2026-11-04: "Run CZ4". CZ3 (0d21eeff4e) found TID and LOC pass the planets by ~7 orders, but the filter length at
the planets is 7–9 pc at Saturn and grows inward (ξ ∝ 1/r in the Newtonian regime), so the Gaussian that smooths the
Sun's field also takes in the Galactic disc and the nearby stars. CZ2/CZ3 smoothed the Sun alone. This lane puts the
neighbourhood inside the filter and re-grades the planet (AZ12) and Cassini (KT16 Q2) rows.

κ = 1/2 FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the
data favour the framework. No download. Small job, one thread.

## The physics being added
With ξ ≫ r the Sun's own strong field no longer screens ν near the planets, so the Galaxy's local phantom density
(≈ (ν_e − 1) times the local baryon tide plus the ν' term) acts inside the planetary orbits. The filtered Newtonian field is
g̃(r) = h̃_☉(r) r̂ + e x̂ + T·r, x̂ toward the Galactic centre, ẑ the north Galactic pole, e = g_e²/(g_e + a0) (CZ3).
- **Disc tide T (Newtonian, baryons only):** T_xx = β e/R0, T_yy = −e/R0, T_zz = −4πGρ_b − (β − 1) e/R0, off-diagonal 0
  (∇·g = −4πGρ_b). R0 = 8.122 kpc. ρ_b(R0, 0) from the committed S3 Milky Way models (`s3_mw.py`: McMillan, B2, B2b,
  B3), **the largest of the four is graded**; β ∈ {0, 1, 2}, **the worst is graded**. Midplane, **unsmoothed** (smoothing a
  slab only lowers ρ̃; the vertically smoothed ρ̃ at each ξ is printed beside, not graded).
- **Nearby stars (discreteness about the smooth ρ_b):** Campbell's theorem on the Gaussian-smoothed tide of a Poisson
  field of stellar systems, density ρ_* (S3 stars at R0) / M_w, mass-weighted system mass M_w = 2 M☉ (1 M☉ beside),
  excluding s < 1.3 pc (no system nearer than α Cen); bound 3σ, in the worst orientation. Plus α Cen explicitly: 2.1 M☉ at
  1.34 pc, smoothed at ξ(r), worst orientation. Both enter as a linear bound added in absolute value.

## Planet gate (AZ12's, unchanged)
A(r) = spherical average of r̂·[ν(|g̃|/a0) − 1] g̃ (Gauss' law, exact for QUMOND's phantom flux), simple ν, 2D angular
quadrature (μ = r̂·x̂ Gauss–Legendre, φ uniform), then CZ3's orbit-averaged secular rate. Stars bound per radius:
ΔA_* = (r/3)[(ν_e − 1)|tr T_*| + |ν'_e| (e/a0)|T_*,xx|]. **Planet pass per footing if Z_cons = Z(Sun + disc) + Z(stars
bound) ≤ 2 for all six planets**, Z = |rate| / max(EPM, INPOP). ξ(r) as CZ3 (TID, LOC; HALF beside).

## Cassini row (KT16's Q2, ceiling 5.2e-27 s⁻², CZ2's code)
Q2_total = Q2_☉(ξ with neighbourhood) + Q2_env.
- ξ with neighbourhood: TID τ → √(τ_☉² + |T|_F²), LOC |d|g|/dr| → |d|g|/dr| + |T|_F (x units, |T|_F · r_M / a0).
- Q2_env bound: the Frobenius norm of the traceless symmetric part of M = (ν_e − 1)(T + T_*) + ν'_e (e/a0) x̂ x̂ᵀ(T + T_*),
  and, as a bound that does not lean on locality, the whole local tide 4πG ρ_tot with ρ_tot = S3's Oort-limit prediction
  (0.166 canonical / 0.174 alt); **graded on the larger**.
- **Cassini pass if Q2_total ≤ ceiling** (orientation not used: Hees' ceiling is for the Galactic-centre axis; all
  orientations compared to it is conservative).

**Labels per rule and footing: <RULE> PASSES WITH NEIGHBOURS / <RULE> FAILS WITH NEIGHBOURS: <rows>.** Joined with CZ2
(MW, dwarfs, SPARC carried, unchanged by this lane): **<RULE> SURVIVES FIVE ON ALT WITH NEIGHBOURS**.

## Expectation on record, not blind
Estimate before the script: alt ν_e − 1 ≈ 0.49, 4πGρ_b ≈ 5–9e-30 s⁻², so ΔA/r ≈ 1e-30 s⁻², about 5e-6 of HALF's core at
Saturn; **Saturn Z_env ≈ 1e-4 on both rules, a pass by ~4 orders** (equivalently a uniform phantom of ~0.05 M☉/pc³ inside
the solar system). Q2_env ≈ 1e-30 to 1e-29 against 5.2e-27, **pass by ≳ 500x**; ξ with neighbourhood changes only r ≳ 1 pc
(tidal radius), so Q2_☉ should move little. The direction is not blind; only the size is.

## Checks
- K1: with T = 0 and no stars the code reproduces CZ3's Z (cz3.json) for TID, LOC, HALF at Saturn and Mars to relative 1e-4.
- K2: the numeric disc ΔA agrees with the linear formula (r/3)[(ν_e − 1) tr T + ν'_e (e/a0) T_xx] to 1 % at every planet.
- K3: doubling the angular orders changes every Z_cons by ≤ 1 % (relative).
- K4: with the neighbourhood in ξ, ξ at every planet radius changes by ≤ 1e-6 (relative).
- K5: the Gaussian-blob Hessian: ∫ (tr T_blob)² d³s = (4πG)² / (8 π^{3/2} ξ³) to 1e-3 (no cut).
- K6: with the neighbourhood ξ off, Q2_☉ reproduces CZ2's Newtonian-field Cassini (TID 0.208 / 0.442, LOC 0.0039 / 0.0215).
- MUTATE: ρ_b × 1e5 (a dense cluster-core neighbourhood); Saturn Z_cons must exceed 10 for TID and LOC on both footings,
  so the environment term is shown to reach the rate; the run exits 1.

## Stated limits
Slab tide at the midplane (the Sun's 20 pc height, spiral arms, the Local Bubble ignored; the Bubble lowers ρ, so ignoring
it is conservative). Linear bound for the stars, not a realisation. Row-wise spherical filter, |g| not iterated, Newtonian
Galactic field from the simple ν (CZ2/CZ3). Monopole precession + one quadrupole number; no ephemeris refit.
