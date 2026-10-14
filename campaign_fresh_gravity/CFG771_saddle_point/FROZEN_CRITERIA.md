# CFG771 FROZEN CRITERIA: the Sun–Earth saddle point (the proposed LISA Pathfinder test) under the framework's own action

Committed alone, before any script or number. 2026-10-14. Block CFG770–779.

## Question
Bekenstein & Magueijo (2006) and Trenkel et al. (2010) proposed flying LISA Pathfinder (LPF) through the Sun–Earth saddle
point, where the Newtonian field cancels. That mission ended without making the pass. What does the framework's action predict
there, and could such a pass ever test it?

## Declared calculation
**S1 geometry.**
- Locate the saddle point of the Sun + Earth + Moon Newtonian field on the Sun–Earth line, with the Moon at its mean distance
  in two placements (on the line, and at quadrature).
- Compute the Newtonian tidal tensor T there by finite differences.
- Gate: K1, the saddle's distance from Earth agrees with d ≈ D√(M_E/M_S)/(1 + √(M_E/M_S)) to 1e-3 when the Moon is removed.

**S2, action without stiffness (γ = 0): the local, algebraic (curl-free) part only, disclosed.**
- Use g = ν_s(|g_N,tot|/a0) g_N,tot, where g_N,tot = g_e + T·x includes the Galaxy's field (the action has no basin rule).
- Report:
  - the region where |g_N,tot| < 3 g_e (beyond it the response is within ~10% of the far value);
  - the maximum anomalous stress |∂(g − g_N)| inside the region;
  - the crossing time at 1.5 km/s.
- Also report the basin-rule variant (Galaxy removed, CFG693): the "bubble" where |T·x| < a0, of radius r_b = a0/|T|.

**S3, the stiffened action (the framework as committed, L* = 5.75 pc to 1 kpc).**
- The anomalous tidal tensor at the saddle, from CFG770's exact linear response, summed over the Sun, Earth and Moon.
- For r ≪ λ_e each body gives a constant-magnitude pull GM_i/L*² toward itself, so its anomalous stress is
  (GM_i/L*²)(δ_ij − r̂_i r̂_j)/r_i.
- The Galaxy's field is uniform there and carries no tide.

**S4 sensitivity.** LPF's measured differential acceleration noise (Armano et al. 2018: about 1.74e-15 m s⁻²/√Hz above
1 mHz; quoted from memory and flagged as provisional), divided by its 0.376 m test-mass separation, gives a gradient noise.
Compute the signal-to-noise ratio for S2 and S3 over the crossing.

## Classes
- **NULL PREDICTED** if S3's SNR < 1 for every L* in the window: the framework predicts LPF would see nothing.
- **TESTABLE** if SNR ≥ 1.
- Also state whether the γ = 0 action would have been testable (its S2 SNR), as context only.

## MUTATE (CFG771_MUTATE=1, separate outputs)
- M1: L* → 1e-4 pc in S3. The stress must rise by (5.75/1e-4)² ≈ 3.3e9.
- M2: T → 0 (no tide). S2's region must become unbounded (flagged).

## Hand estimate (before any script)
- d ≈ 2.59e8 m and |T| ~ 4.6e-11 s⁻², so the basin-rule bubble r_b = a0/|T| ≈ 2 m. This is not Bekenstein–Magueijo's
  383 km, which came from TeVeS's κ scaling.
- With the Galaxy's field included the region is of order g_e/|T| ≈ 5 m.
- S3 stress ≈ 4.2e-15/AU ≈ 3e-26 s⁻². LPF gradient noise is about 5e-15 s⁻²/√Hz. **NULL PREDICTED**, by about 11 orders of
  magnitude.

## Disclosures fixed now
- S2 neglects the curl part of the field (the action is AQUAL-type), so its numbers are order-of-magnitude context, not a
  verdict.
- The LPF noise figure is quoted from memory (provisional).
- κ fitted; cold energy mass required; not theory closed.
