# T18 — FROZEN CRITERIA: the cold-fluid reconstruction (from the front)

**Claim to test (new door — the cold fluid is measured, not assumed).**
T17's front law pins the present-day phantom at every radius:
    M_ph(r) = f(r)·S(<r),  f(r) = 1 − e^{−λτV/r} (c = 55–59 kpc),
    S(<r) = M_b/(e^{r_t/r} − 1)  (certified closed forms).
The observed MW halo mass profile (published anchors, declared below)
then LEAVES the cold fluid:
    M_cold(r) = M_tot,obs(r) − M_b — M_ph(r)     (master cert #15,
    radial application — the same budget identity at every radius).

**S1 — the reconstructed cold profile and fraction curve.** Outputs:
M_cold(r) and ρ_cold(r) at 30–250 kpc, the cold/dark fraction
x_cold(r), under two anchor sets (A: Callingham-ish, B: Gaia DR3-era,
both declared). Declared expectations: M_cold(30 kpc) ≈ 0 (the T15
knife-edge, closed with M_b(30) = 7e10), turning positive outward —
the knife-edge is the INNER boundary of the cold component; the
measured shape of ρ_cold(r) discriminates reservoir-flat vs cusped
(shape reported, not assumed).

**S2 — the rotation-decline masking (S5 quantified).** The observed
rotation includes the cold fluid: the reconstructed total
M_tot(r) = M_b + f·S + M_cold must reproduce the anchor masses at the
anchors (by construction) AND give V(200)/V(60) including the cold: the
front's decline (0.63 with phantom alone) is diluted by the cold —
the honestly reported content: how much decline survives in the total,
and at what radius the total curve must bend.

**S3 — the outer-halo knife-edge.** At the outermost anchors (200 or
217 kpc) M_cold must stay ≥ 0: a negative cold at ANY anchor kills the
front law at that radius — the outer boundary of the framework's
consistency, with the anchor-set spread as the window.

**Screens:** Q1 — the phantom part is closed-form certified (T9/T10/
T17); the only inputs are the record's λ, τ, V and published MW masses;
Q2 — no rationals; Q3 — a reconstruction (measurement of the cold
component's spatial law).

**Checks (exit 1 on failure):**
  C1  phantom profile: M_ph(r) at the five radii (30/50/100/200/217
      kpc) from the closed forms, both conventions (c = 55.4/59.0),
      residuals < 1e-12 (identity check).
  C2  cold nonnegativity: M_cold(r) ≥ −1e-9·M_b at every anchor, both
      anchor sets (with M_b(30) = 7e10 at 30 kpc; baryon interior
      masses declared at each anchor).
  C3  knife-edge inner: |M_cold(30 kpc)/M_b| ≤ 0.3 (the T15 closure).
  C4  cold fraction rises outward: x_cold(100 kpc) < x_cold(217 kpc)
      − 0.1 (the cold emerges outside the front).
  C5  reconstruction closure: V_recon(r) at the anchors within ±15% of
      the flat-level bracket (188–200 km/s) for both anchor sets.
  C6  MUTATE (T18_MUTATE=1: fully-settled branch f ≡ 1 — the deepest
      wrong branch): C2 must fail at ≥ 2 anchors (the kernel alone
      overdraws: negative cold at 30 and 100 kpc); C4 must fail.
  C7  report: the S5 decline after cold-masking: V(200)/V(60) with the
      cold fluid — the surviving decline and the bend radius.

**Anchors (declared, published):** M_tot(30 kpc) = 2.47e11 (V=188) /
2.80e11 (V=200) [rotation, framework-consistent]; M(50) = 4.0±0.6e11
[Huang+16, blue-HB]; M(100) = 6.4±0.8e11 [Huang+16/Posti+19];
set A: M(200) = 8.2±1.5e11 [Callingham+19]; set B: M(217) =
1.00±0.10e12 [Gaia DR3 era]. Baryon interiors: M_b(30) = 7.0e10,
M_b(50) = 8.5e10, M_b(100) = 9.5e10, M_b(200/217) = 1.0e11 [the
record's disk+bulge+gas model]. All anchors run with their ± windows
for C2/C4 (a row passes if the window-consistent ≥ 0 exists).

**Deliverables:** freeze committed ALONE; t18_cold_reconstruction.py +
.out ×2 + results ×2; README (the reconstructed profile table, the
fraction curve, the S5-masking verdict, the falsifiers); no new Lean
theorem (the radial application of certified #14–16 rides the lane);
campaign row. Language: the cold fluid is reconstructed from data +
the law, its shape reported as a measurement, its sign-checked at
every anchor; nothing "closed".