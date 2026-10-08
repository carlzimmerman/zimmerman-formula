# T17 — FROZEN CRITERIA: the settling front (the completeness profile)

**Claim to test (new door — the spatial face of the settling law).**
The settling rate is local, Γ(r) = λ·√(4πG·ρ(r)) with λ = 0.028
(CFG382 floor calibration), so completeness is a FUNCTION OF RADIUS:
the fixed-point profile

    f(r) = 1 − exp[−λ τ √(4πG·(ρ_b(r) + f(r)·ρ_k(r) + ρ_cold(r)))]

with the kernel phantom ρ_k(r) = √(GM_b a₀)/(4πG·r²) (T9/T10 closed
form), τ = 10.3 Gyr (z=2 primary), ρ_cold = (1−f)·ρ_supply
(reservoir complement, T15).

**S1 — the front.** The e = 1/2 contour is r_f where
ρ(r_f) = (ln 2)²/(4πG(λτ)²) = 6.9e-24 kg/m³; on the MW density field
(slope −2 in the phantom-dominated regime) this lands at r_f ≈ 85 kpc
(window [60, 120] kpc over the baryon/rotation conventions). Inside,
the phantom is ≥ 50% settled; outside, mostly unsettled. The Leancertified front-density closed form: √(4πGρ_f)·λτ = ln 2 ⇒ ρ_f =
(ln 2)²/(4πG(λτ)²) (master cert #18).

**S2 — the S-shaped dark-mass profile (the new prediction).**
M_dark(r) = f(r)·S(<r) is NOT a power law: it has an inflection at
r_f (inner slope ≈ 2, the kernel; outer slope → steeper/falling as
f → 0). This S-shape is the settling's fingerprint, distinguishable
from NFW-cusped and from MOND-effective profiles by the INFLECTION:
   d²M_dark/dr² changes sign at r_f; the slope contrast (inner vs
   outer, evaluated at r_f/2 and 2r_f) is reported and checked.

**S3 — self-consistency with the knife-edge (T16).** The profile's
mass within 30 kpc, M_dark(<30 kpc) = f(30)·S(30)·M_b, must equal the
rotation-implied deficit at the measured flat level (188–200 km/s):
closure iff M_b(30 kpc) ∈ [6.4, 7.3]e10 — the T16 boundary is
re-derived from the profile (a genuine cross-lane consistency check).

**S4 — front motion (registered).** r_f grows with τ: the front is
slow-moving today (dr_f/dt ≈ r_f/(2τ) ≈ 4 kpc/Gyr); high-z analogs
show a smaller settled region (completeness out to smaller r). The
X-COP z-slope (T16) and the front's growth are the two time-domain
tests; the front speed is registered with the z-evolution formula.

**Falsifier (registered):** a measured MW dark-mass profile whose
inner/outer slope contrast (or lack of inflection) excludes the
S-shape at > 2σ kills S2 — with satellite-kinematic mass profiles at
30–150 kpc as the live test; the T16 boundary window [6.4, 7.3]e10 for
M_b(30 kpc) is the second knife-edge.

**Screens:** Q1 — derives from the record's own calibration (CFG382)
and the kernel (T9/T10); Q2 — no inserted rationals; λ, τ, a₀ all
record values; Q3 — a differential (radial) prediction, new family:
no prior lane derived f(r).

**Checks (exit 1 on failure):**
  C1  fixed-point profile solved: |residual| < 1e-9 at 200 radii
      (2–300 kpc), both M_b conventions; f(30 kpc) = 0.86 reproduced
      (calibration anchor; noted as by-construction).
  C2  the front: r_f ∈ [60, 120] kpc (both conventions); the
      front-density identity √(4πGρ_f)·λτ = ln 2 to 1e-9.
  C3  the S-shape: d²M_dark/dr² changes sign at r_f (numeric, robust
      stencil); slope contrast inner/outer ≥ 1.5 (both conventions).
  C4  knife-edge closure: M_dark(<30 kpc)/deficit(30 kpc) ∈
      [0.95, 1.30] at V = 188 AND the boundary M_b(30 kpc) window is
      re-derived ∩ [6.4, 7.3]e10 ≠ ∅.
  C5  front speed: dr_f/dt ≈ r_f/(2τ) reported with the z-evolution
      formula registered.
  C6  MUTATE (T17_MUTATE=1: uniform, density-independent Γ — the
      global-rate branch): C1–C4 must fail (flat f, no front, no
      inflection, knife-edge broken).
  C7  report: floor-30-kpc semantics (the floor IS the local settled
      fraction at the anchor radius — by construction consistent) and
      the profile-vs-NFW discrimination statement.

**Deliverables:** freeze committed ALONE; t17_settling_front.py + .out
×2 + results ×2; README (the profile, the front, the S-shape, the
falsifier); ONE new master-cert theorem
(`front_density_from_condition`, #18) compiled + audited; campaign row.
Language: the first radial prediction of the settling family; falsifier
first-class; nothing "closed".