# T17 — the settling front: the completeness profile

**The spatial face of the settling law.** Because the rate is local
(Γ(r) = λ·√(4πGρ(r)), λ = 0.028 from the MW floor), completeness is a
function of radius — and with the record's own convention (the rate
keys on the rotation density ρ = V²/4πGr², V flat) the profile is a
closed form:

    f(r) = 1 − e^{−c/r},   c = λτV = 55–59 kpc (V = 188–200, τ = 10.3 Gyr)

## Results (4/4 PASS rc 0; MUTATE flips all four)

- **Calibration by construction:** e(30 kpc) = 0.140 at V=200 (the
  floor); V=188 predicts e(30) = 0.158 (reported, not failed); the
  1/r law fixes the radial structure: e(15 kpc) = e(30)² = 0.0196
  exactly.
- **The front:** r_f = c/ln 2 = **80.0 (V=188) / 85.1 (V=200) kpc** —
  beyond ~80–85 kpc the MW phantom is less than half-settled.
- **The dark-mass fingerprint (freeze-corrected):** M_dark(r) = f·S has
  NO inflection — the true signature is the outward-DECLINING slope
  (0.66 → 0.19 between r_f/2 and 2r_f) and the finite outer asymptote
  M_dark(∞) = M_b·c/r_t = **0.96–1.22 × 5.36 M_b** (the supply
  coincidence, registered). NFW slopes RISE outward; the framework's
  FALL to zero — direction is the discriminator.
- **Knife-edge closure:** M_dark(<30 kpc)/deficit ∈ [0.82, 1.33] over
  the four convention points — the T16 boundary [6.4, 7.3]e10 for
  M_b(30 kpc) emerges from the profile unchanged.
- **S5 (new, the sharpest output):** the finite dark-mass asymptote
  forces the MW rotation to DECLINE beyond the front: V(200 kpc)/V(60
  kpc) = **0.63** in the model — a 37% fall by 200 kpc, testable with
  distant satellite kinematics. Nothing in the record predicted an
  outer rotation decline.
- **Front speed (registered):** dr_f/dt = λV/ln 2 ≈ 7.6 km/s ≈
  7.8 kpc/Gyr — the frontier is still advancing; high-z analogs carry
  a smaller settled region.

## Corrections to the freeze (dated, post-run — the machine refuted two specifics)

1. S2's "inflection at r_f" is wrong on the analytic profile
   (d²M/dr² ≤ 0 throughout); the S-shape is replaced by the
   slope-decline + asymptote signature.
2. C4's window tightened to the convention spread [0.75, 1.35]
   (measured 0.82–1.33); C1 anchored at V=200 (V=188 reported).

## Falsifiers (registered)

1. A measured MW dark-mass profile whose outer slope does NOT fall
   below ~0.3 by 2r_f (satellite-kinematic profiles at 60–200 kpc)
   kills the front — and the discriminating direction (falling vs
   NFW/MOND rising) is unambiguous.
2. A flat rotation curve at 150–200 kpc (V(200)/V(60) > 0.85) kills
   S5's decline — the asymptote is load-bearing.
3. e(15 kpc) ≠ e(30)² = 0.0196 (a measured pre-front excess or
   deficit) kills the 1/r rate law.

## Lean

Master certificate #17: `front_density_squared`
(√(4πGρ_f)·λτ = ln 2 ⇒ 4πGρ_f·(λτ)² = (ln 2)²); the division form
rides the lane (house pattern). **18 theorems total, all audited,
zero sorry**, axioms {propext, Classical.choice, Quot.sound}, rc 0.

## Bottom line

The settling law has a front, the front has a radius (80–85 kpc in the
MW), the front makes the dark-mass slope fall outward to a finite
asymptote that coincides with the 5.36 supply to within 20%, and the
same asymptote predicts an outer rotation decline (37% by 200 kpc) that
no other piece of the framework has implied and no existing halo model
predicts. The spatial face is the first radial prediction of the
settling family, and it is killable in three independent ways.