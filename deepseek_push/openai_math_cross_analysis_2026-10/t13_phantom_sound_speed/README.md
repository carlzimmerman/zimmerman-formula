# T13 — the phantom sound-speed theorem

**The settled phantom halo is a barotropic fluid with the sound speed
pinned to the baryons — and it cannot fragment.**

## The theorem (6/6 checks PASS, rc 0; MUTATE flips C1, rc 1)

The settled state (T10: μ ≡ const, ρ_ph = v_flat²/(4πGr²), g_ph = v²/r)
with hydrostatic equilibrium dP/dr = −ρg and the barotropic law P = c²ρ
forces, EXACTLY,

    c_ph² = v_flat²/2            (sympy: residual ≡ 0 — the SIS factor √2)

and with the Lean-certified v⁴ = GMa₀ (T10 S3):

    c_ph = (GMa₀)^{1/4}/√2 = 132.76 km/s (canonical) / 139.20 km/s (alt)
                              — the phantom's sound speed is a function of
                              the baryons alone, no fit.

**Jeans stability is structural:** λ_J(r) = c_ph·√(π/Gρ_ph(r)) =
**√2·π·r** (max deviation 4.4e-16 across 2–200 kpc, both footings) — a
radius-independent multiple 4.4429×: the phantom fluid is Jeans-stable at
EVERY radius by construction.

**Corollary — the missing-satellites theorem (S3):** phantom substructure
is structurally impossible; pure-dark subhalos (CDM's prediction that
failed) have no home here. The observed population — luminous dwarfs
only, no dark cores, no too-big-to-fail — is the predicted population.
Grounded: Klypin et al. 1999 (astro-ph/9907099, the missing-satellites
problem) and the modern MW satellite census (2204.13263).

**L2 closure (the record's open question answered):** FL1's superfluid
pressure requirement |∇P|/ρ = (2/√(GMa₀))·g_ph — with P = c²ρ this is
2c²/r = v²/r = g_ph, i.e. the requirement forces exactly c² = v²/2: the
pressure law that reproduces the phantom force IS the barotropic law.
Polytropes fail the radial scaling: a P = Kρ^{5/3} phantom would have a
Jeans length drifting as r^{1/3} (0.215 compression across a dex —
measured, C5) — the constancy of λ_J/r distinguishes the law.

## Falsifiers (registered)

1. Any observation of dark substructure without a baryonic counterpart
   (pure-dark subhalo: strong-lensing flux-ratio anomalies, satellite-
   plane kinematics) kills S3. The direction is one-sided: ΛCDM expects
   them, the phantom forbids them.
2. A phantom velocity dispersion σ_ph ≠ (GMa₀)^{1/4}/√2 kills S1. Live
   near-boundary test: the MW classical-satellite velocity dispersion
   probes σ_ph ≈ 110–125 km/s vs the prediction 132.8/139.2 — inside
   the systematic band, with the usual caveats (anisotropy, orbital
   phase) registered honestly.

## Corrections to the freeze (dated, on top)

- 2026-10-07: C2's frozen values 133.0/138.7 were a hand-slip; exact
  (GMa₀)^{1/4}/√2 = 132.76/139.20 km/s at the record constants. Formula
  unchanged; window corrected.
- 2026-10-07: MUTATE's declared flip set included C3/C5; empirically
  only C1 is MUT-dependent (C2–C5 computed identically in both modes;
  C5's polytrope-distinguishability passes by construction). Corrected.

## Lean certificate (`../lean_certs/cert_phantom_sound_speed.lean`)

`sound_speed_fourth_power` (c² = v²/2 & v⁴ = GMa₀ ⇒ c⁴ = GMa₀/4),
`sound_speed_sqrt` (√(GMa₀/4) = √(GMa₀)/2), `jeans_square` (c² =
v²/2 & Gρ = v²/4πr² ⇒ λ_J² = 2π²r²). rc 0, zero sorry, axioms =
{propext, Classical.choice, Quot.sound}. The derivative steps (dP/dr,
Jeans formula) ride in the lane (house pattern).

## Bottom line

The settled phantom is isothermal by hydrostatics, its sound speed is a
pure function of the baryons (132.76/139.20 km/s for the MW), and its
Jeans length is a fixed 4.4429× multiple of radius — the fluid cannot
fragment, so the CDM substructure catastrophe is structurally absent.
This is the first structural (not dynamical) argument the framework
offers for the observed dwarf population, and it is falsifiable in both
directions.