# D7d_screened_q2 — Cassini Q₂ of the stiffened action, in the Galaxy's field

## Verdict: CRISP FINDING — with the record's stiffness, Q₂ passes Cassini by 10⁷–10⁹ at L* = 24–90 pc

- The stiffened DSF-21 action passes Cassini for **L* ≥ L*_C**, with L*_C ≤ **0.069 pc** (canonical) and
  L*_C ≤ **0.111 pc** (alt). This holds for all four Galactic fields.
- That is about 220–350× below the globular bound (23.96 / 24.72 pc, CFG820 json). So the screened picture is
  **consistent**: Cassini does not set the lower end of the L* window.
- The binding lower gate is still CFG691's Saturn monopole (5.75 pc).
- At the physical window, Q₂ is **1.0–2.3e-34 s⁻² at 24 pc**, **1.1–2.5e-35 at 50 pc** and **2–4e-36 at 90 pc**.
  That is 2.5e-8 to 4e-10 of the Hees 2σ line. It also passes Park 2026.
- The mechanism: inside L* the Sun's P field is a constant hedgehog GM/L*² r̂ (A22/A30), which has no quadrupole.
  Q₂ comes only from the anisotropic Galactic "mass" term acting at r ~ L*. So **Q₂ ∝ GM/L*³**, not a₀^{3/2}/√(GM).

Script: `d7d_screened_q2.py` (solvers in `d7d_solver.py`). **10/10 checks PASS**, exit 0, 28 min, single thread.
`--mutate` (scalar Laplacian in Route N) gives K5 and K6 FAIL, exit 1. Criteria were frozen first (a13e418498).
Amendment 1 (e1ba64cf92) is pre-result. Every number below is in `d7d_screened_q2_results.json`.
κ = ½ is FITTED. Not theory closed.

## The equations (from the action, not assumed)

From A33 (L) and (P), static, at O(ε), with p = KP and Φ = ln N:
- **(L)** ∇²Φ = Kρ + ∇·p;
- **(P)** ∇Φ + (L*²/2)∇²p = a₀p/(a₀ − |p|).

Because γ_F = γ_L, the stiffness is the plain vector Laplacian. At L* = 0 this is **AQUAL with μ = x/(1+x)**, not QUMOND.
So L* → 0 reproduces BN11's AQUAL μ₁ number: **3.818e-26 vs 3.8e-26 (K4, ratio 1.005)**. D7b's QUMOND number is the
other formulation, and it sits a factor 0.737 below.

The stiffness is **not** a multiplicative screening S(s) here. In the Galactic field the Sun's perturbation obeys
[(k²L*²/2)I + J − k̂k̂] δp̂ = δĝ_N, with J = diag(1+x_e, 1+x_e, (1+x_e)²). The isolated S(s) applies only with no external field.

## Checks (all PASS)

- **K1:** sympy confirms the law at L* = 0, and that the isolated reduction is exactly CFG691's ODE with ℓ = L*²/2r_M.
- **K2:** Route F at L* = 0 equals the linear AQUAL EFE response, to 2e-15.
- **K3:** the grid machinery in QUMOND mode reproduces D7b at all 8 points, to 5.6e-4.
- **K4:** the BN11 AQUAL anchor, above.
- **K5:** the isolated profile reproduces CFG691/CFG820's S(s) to 1.2e-4.
- **K6:** the nonlinear grid (Route N) and the Fourier formula (Route F) agree to 6e-4 at L* = 30 and 100 r_M.
- **K7:** the limits. L* = 0.01 r_M gives the AQUAL value to 5e-5. Q₂(L* = 10 kpc) is 7e-17 of it.
- **K8:** the Richardson correction is 0.8 % / 1.1 %, and halving r_in changes Q₂ by about 1e-4.
- **K9:** linear validity at 24 pc, with GM/L*²/u_e ≤ 4.6e-6.
- **K10:** Route F reproduces CFG770's six values to 7e-6.

## The Cassini bound on L* (Route N, nonlinear)

L*_C is bracketed on the frozen grid. The passing endpoint is **L* = 1.78 r_M** (0.069 pc canonical, 0.062 pc alt).
At that point Q₂ (Richardson) is 4.7–8.3e-27 canonical and 5.6–8.5e-27 alt, against the Hees line of 9.0e-27.

One exception: **alt E3 fails at 1.78 r_M and passes at 3.16 r_M** (0.111 pc).

**Non-converged band.** Between L* = 0.03 and 1.0 r_M neither sweep converged to the frozen residual, so those points
are not scored. The prototype shows why: below L* = r_M the near-Sun hedgehog saturates the cap, since the radial
balance is (1 − L*²/r_M²)/r². In this band the linear core would also exceed the cap on one side (L* < r_M√(1+x_e)).
The bracket's lower end is therefore L* = 0, which fails, and the bound is an upper bound on L*_C, not a measurement.

## Consequences (reported only): one screened picture vs law-first

| | screened, L* = 24 / 50 / 90 pc | unscreened law-first |
|---|---|---|
| Cassini Q₂ (s⁻²) | ≤ 2.3e-34 / 2.5e-35 / 4.3e-36: PASS | 1.5–3.6e-26 (D7b), FAIL 1.7–4.0× |
| wide binary 1.5 M☉, 20 kAU, γ_v − 1 | 8.1e-6 / 1.9e-6 / 5.8e-7 (CFG740 isolated ½(s/L*)² = 8.16e-6 / 1.88e-6 / 5.80e-7; EFE changes it < 1 %) | 0.175 / 0.210 (D2) |
| inner-planet sunward anomaly | GM/L*² = 2.42e-16 / 5.6e-17 / 1.7e-17 m/s²; Mars 0.17 / 0.040 / 0.012 of its bound | a₀ tail without P5: 1.1e4–8.1e4 × the bounds; with P5: 1e-22–2e-18 (invisible) |

So the screened theory is Solar-System-clean and predicts **no** wide-binary boost visible to DR4. The law-first reading
predicts 1.18–1.21 and fails Cassini. **The two readings cannot both hold.**

## Found in the record

- **CFG770's sign.** CFG770 prints Q₂ = −1.1 to −1.8e-32 and calls it the Park/Hees convention. Its integral is the
  Φ-convention quadrupole: K10 matches it exactly in that convention. In the BN11/Hees convention, fixed here by the
  QUMOND match to D7b (K3), the screened Q₂ is **positive**. No verdict changes.
- **CFG832's "Cassini gate 0.087 pc"** was an L*⁻³ extrapolation into the band where the linear core violates the
  cap. The nonlinear bracket (≤ 0.069 / ≤ 0.111 pc) is the same order, so it was right to order of magnitude.
- **The globular bound.** The brief's 23.64 / 24.48 pc was not found in the record. `cfg820_results.json` gives
  23.96 / 24.72 pc, and those are the values used here.

## What this does not show

- It assumes a uniform, static Galactic field over about L*, and stays at O(ε).
- It does not refit the ephemeris and does not include the planets' own fields.
- The band 0.03–1 r_M is unsolved, so L*_C is an upper bound only.
- **Compute disclosure.** The main run peaked at **3.0 GB RSS**, over the brief's 2 GB. The cause was one
  (60 pts/decade, N_θ = 96) solve on an 11-decade domain, while CFG960 was live. Nothing was killed. The MUTATE run
  (1.6 GB) runs only K1, K2, K5 and K6 at L* = 30 r_M, for the same budget reason.
