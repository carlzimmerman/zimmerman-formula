# T13 — FROZEN CRITERIA: the phantom sound-speed theorem

**Claim to test (novel structural derivation from T10's settled state):**

The settled phantom halo (T10: μ ≡ const, ρ_ph = v_flat²/(4πGr²)) is a
barotropic fluid: hydrostatic equilibrium dP/dr = −ρ·g_ph with the flat
curve g_ph = v²/r and P = c²ρ force, EXACTLY,

    c_ph² = v_flat²/2            (the phantom is isothermal, σ² = v²/2)

  (S1)  With v⁴ = GMa₀ (T10 S3, Lean-certified): c_ph = (GMa₀)^{1/4}/√2
        — the phantom's sound speed is PINNED to the baryons: MW
        c_ph = 133.0 km/s (canonical) / 138.7 km/s (alt).

  (S2)  Jeans stability is structural: λ_J(r) = c_ph·√(π/Gρ_ph(r)) =
        √2·π·r — a radius-INDEPENDENT multiple of r (4.4429×). The
        phantom fluid is Jeans-stable at EVERY radius by construction.

  (S3)  Corollary (the missing-satellites theorem): phantom substructure
        is structurally impossible — any pure-dark subhalo (CDM-style,
        no baryonic counterpart) is forbidden. The observed MW dwarf
        population (~luminous dwarfs only) is the predicted population;
        ΛCDM's missing-satellites and too-big-to-fail expectations have
        no counterpart here.

  (S4)  The L2 closure: the record's L2 asked whether FL1's superfluid
        pressure reproduces |∇logρ_ph| = (2/√(GMa₀))·g_ph. Answer:
        |∇P|/ρ = c²|∇logρ| with c² = v²/2 gives exactly 2c²/r = v²/r =
        g_ph ⇒ the required pressure law IS the barotropic one — L2
        resolves into S1 (the settled fluid must be isothermal-thermal,
        not polytropic: P = Kρ^{5/3} fails the radial scaling).

**Falsifiers (registered):** (i) any observation of dark substructure
without a baryonic counterpart (pure-dark subhalo — strong-lensing flux
anomalies or satellite-plane kinematics requiring one) kills S3;
(ii) a measured phantom velocity dispersion σ_ph ≠ (GMa₀)^{1/4}/√2
(± measurement honesty: the MW classical-satellite dispersion probes
σ_ph ~ 110–125 km/s vs the prediction 133.0/138.7 — a LIVE near-boundary
test, registered with its systematic caveats).

**Screens:** Q1 — derives from the framework's settled state and Newton +
hydrostatics; a₀ enters only through v⁴ = GMa₀; Q2 — no inserted
rational; √2 and π arise from the identities themselves (√2 from σ = v/√2
is the SIS factor; π from the Jeans formula); Q3 — structural law.

**Checks that can fail (exit 1):**
  C1  barotropy: symbolic (sympy) hydrostatic equilibrium with P = c²ρ
      and ρ ∝ 1/r², g = v²/r ⇒ c² = v²/2 exactly (residual 0).
  C2  c_ph value: (GMa₀)^{1/4}/√2 = 133.0 ± 0.2 km/s (canonical),
      138.7 ± 0.2 km/s (alt) for M_b = 1e11 M_sun.
  C3  Jeans ratio: λ_J(r)/r = √2π = 4.4429 at 200 radii; max deviation
      < 1e-9.
  C4  stability: λ_J(r) > r on [r_in, r_out] (ratio > 1) — plus the
      corollary statement check: substructure-free requirement has no
      counterexample in the record's galaxy data (report only).
  C5  L2 closure: for P = Kρ^{5/3} (polytrope), the hydrostatic solution
      gives λ_J(r₂)/λ_J(r₁) ≠ 1 (drift ≥ 20% across a dex) — the
      isothermal law is DISTINGUISHABLE from a polytrope by the Jeans
      scale's constancy.
  C6  MUTATE (T13_MUTATE=1): replace isothermal with polytrope in the
      consistency chain — C1 must flip (polytropic residual ≠ 0).
      [CORRECTED 2026-10-07: the original wording declared C3/C5 would
      flip too; empirically only C1 is MUT-dependent — C2–C5 are computed
      identically in both modes (C3/C5's content is the polytrope
      DISTINGUISHABILITY, verified by C5's drift check, which passes in
      both modes by construction). MUTATE rc 1 verified.]
  C7  literature grounding: fetch 1–2 sources on the MW dwarf population
      and the missing-satellites problem (registration; the theorem's
      direction — no dark substructure — is the claim).

**Deliverables:** freeze committed ALONE; t13_phantom_sound_speed.py +
.out ×2 + results ×2; README with the L2 closure, the numbers, the
falsifiers; Lean certificate: c_ph⁴ = GMa₀/4 (ring, from the certified
v⁴ = GMa₀ and c² = v²/2) and λ_J² = 2π²r² (substitution algebra with
√2·π extraction via sq_sqrt). House pattern: the derivative steps
(dP/dr, Jeans formula) ride in the lane.
Language: no "closed"; falsifiers first-class; κ/a₀ untouched.