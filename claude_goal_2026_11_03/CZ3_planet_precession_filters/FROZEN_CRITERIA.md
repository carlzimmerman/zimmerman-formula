# CZ3_planet_precession_filters — FROZEN CRITERIA (before any script; no new number computed)

Owner, 2026-11-03: "Run CZ3". CZ2 (b832956ac3) left two filter rules surviving MW, Cassini, dwarfs and SPARC on alt: TID
(KT28) and LOC (KT26/27). Neither has faced the planetary radial anomaly. astra's AZ11/AZ12 (astra_goal_2026_11_03/P2) built
that gate and failed its own kernel at Saturn (Z 6.98 / 11.33). This lane applies AZ12's gate, unchanged, to CZ2's rules.
astra's files are read, not edited; the method is re-implemented here.

κ = 1/2 FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the
data favour the framework. No download. Small job, one thread.

## The gate (AZ12's, copied)
- Radial monopole of the filtered anomalous source, by Gauss' law (AZ11):
  A(r) = ½ ∫_{-1}^{1} [ν(√(h² + e² + 2 h e μ)/a0) − 1] (h + e μ) dμ, simple ν.
- e = g_e² / (g_e + a0), g_e = 2.32e-10 (AZ11's Newtonian conversion; algebraically the same as CZ2's inversion of
  ν(y) y = η for the simple ν, checked as K4).
- Secular rate: ⟨ω̇⟩ = √(1−ε²)/(n a ε) · ∫₀^{2π} A(a(1−ε cos E)) (cos E − ε) dE/2π, n = √(GM☉/a³).
- Inputs exactly as AZ12: RQ3 `tolerances.json` PLANETS (a, EPM and INPOP 1σ in mas/yr), eccentricities Mercury .206, Venus
  .007, Earth .017, Mars .093, Jupiter .048, Saturn .054; GM☉ 1.32712440018e20, AU 149597870700 m, year 365.25 d.
- **Pass per footing if |rate| / max(EPM, INPOP) ≤ 2 for all six planets.** Both ephemerides printed separately.

## What changes: the filtered Sun field h(r)
Row-wise Gaussian point mass, as in KT16/KT27/KT28's Cassini rows: h = a0 · gh_pt(x, ξ(x)), x = r / r_M,
r_M = √(GM☉/a0). ξ from CZ2's Cassini code at η_N (the Newtonian Galactic field):
- **TID:** ξ_tid on the Sun's own field ν(√(x⁻⁴ + η_N²)) x⁻².
- **LOC:** ξ_loc on the total field ν(√(x⁻⁴ + η_N²)) √(x⁻⁴ + η_N²).
- **HALF:** ξ = 0.5 r_M (printed beside; already failed CZ2's Cassini).
ξ is computed on CZ2's grid (x 1e-7 to 1e5, 20000 log points) and interpolated in log x to each orbit radius.

**Labels per candidate and footing: <CAND> PASSES PLANETS / <CAND> FAILS PLANETS: <planets>.** Joined with CZ2:
**TID (or LOC) SURVIVES FIVE ON ALT** if it passes here and survived CZ2 on that footing.

## Expectation on record, not blind
KT26 and KT28 printed ξ at Saturn of about 190–210 r_M (LOC) and 240–260 r_M (TID), against astra's 0.5 r_M. In the core,
h ∝ r/ξ³, so A drops by roughly (0.5/200)³ ≈ 2e-8 against AZ12. **I expect both rules to pass by many orders of magnitude.**
HALF has a Gaussian core √(2/π)/3 against the resolvent's 1/6 at the same ξ, so I expect it to FAIL at about 1.6x AZ12's Z.
The gate is not blind for LOC and TID in direction, only in size.

## Checks
- K1: with AZ12's kernel (enclosed fraction gammainc(3, r/ξ), ξ = 0.5 r_M) the code reproduces AZ12's Saturn Z_generous
  6.983944 / 11.329246 and Mars 1.918578 / 3.112914 to relative 1e-5.
- K2: AZ12's oracles at a = n = 1 for each ε: constant A = 1 → −√(1−ε²); A = r → −1.5 √(1−ε²); A = 1/r² → 0; error ≤ 1e-10.
- K3: orbit/angular orders (128, 80) vs (256, 160) change Z by ≤ 1e-5 (absolute, in Z).
- K4: e from AZ11's formula equals η_N a0 from CZ2's root-find to relative 1e-8.
- K5: the ξ interpolation: doubling the ξ grid density changes Saturn's Z by ≤ 1 %.
- MUTATE: filter removed (h = GM☉/r²); the worst planet must exceed Z 10 on both footings; the run exits 1.

## Stated limits (carried)
Monopole only; quadrupole is Cassini's gate (CZ2), higher multipoles uncomputed; no ephemeris refit, no covariance (AZ12's
scope, a conditional necessary gate). Spherical row-wise filter, |g| not iterated, Newtonian Galactic field from the simple ν.
