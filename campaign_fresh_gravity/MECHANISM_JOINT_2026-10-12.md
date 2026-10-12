# Cold energy: the mechanism as far as both threads reach (joint synthesis, 2026-10-12)

For the owner and for astra. Combines this chat's CFG638–CFG661 with astra's `sol61_push/cold_production_2026_10_11/` and
`sol61_push/phase_source_closure_2026_10_12/` (read only; astra's files were not edited). κ = ½ fitted; footings never pooled;
the cold energy's mass is required; no claim that any field here is an identified particle; not "theory closed"; nothing here
says the data favour the framework.

## 1. The chain, link by link

| # | link | equation | status | source |
|---|---|---|---|---|
| 1 | the scale comes from the vacuum | a₀ = κ c √(G ρ_DE) | **INPUT**, κ fitted. No route derives it. A vacuum offset drops out of every response equation tried | CFG635; astra POLARIZATION_SELECTOR (G W₀/a₀² = 4 is not enforced) |
| 2 | cold matter exists, amount fixed | Ω_c/Ω_b = 5.364 | **INPUT**. A conditional production route: cold daughters of a two-field carrier (φ charge 1, χ charge 2) by near-threshold decay, E ≥ m\|Q\|, cold by construction | astra COLD_ENERGY_EQUATIONS.tex |
| 3 | cold matter is needed as matter | — | **ESTABLISHED on the record**: removing it fails clusters, the Bullet, LG timing and shear | CFG624 |
| 4 | the galaxy law is a static equilibrium of a stress | Π = P⊥I + (P∥ − P⊥)ĝĝ, dP∥/dg = (g/4πG)(1/F′ − 1), P⊥ − P∥ = g(g − F⁻¹(g))/4πG | **DERIVED, exact** for any spherical baryon profile; SPARC rms = the law's to 1e-8. Deep limit = minus the gravitational Maxwell stress | CFG660 S1, D1 |
| 5 | that stress is not the cold particles' pressure | P∥ < 0, β = 2–11 | **DERIVED**: no particle gas can carry it. Any isotropic pressure is excluded by raw SPARC (0.177 vs 0.100 dex) | CFG660 S4, D1 |
| 6 | the stress cannot belong to a simple medium | — | **DERIVED NO-GO** (local, first-order, spherical, {G, a₀}): field-only stress is ill-posed (growth ∝ √k); adding density dependence keeps exactness only through u = ρ_c − (F′−1)ρ_b with a free function that dimensions force to be constant. Independently, the dipolar (polarization) fluid has a growing mode Π̈ ≈ 4πGρΠ that no friction removes | CFG660 S5, CFG661; astra POLARIZATION_REPAIR_GATE (Stahl+22) |
| 7 | a stable response sector exists | L = Zφ̇²/2 + I\|Ṗ\|²/2 − [a/2 \|∇φ − P/a\|² + β/3 \|P\|³ + γ/2 \|∇P\|²] − α ρ_b φ; static ∇·D = αρ_b, ∇φ = P/a + β\|P\|P − γ∇²P | **CONSTRUCTION**, stable for fixed sources (convex energy). Deep tail V⁴ = G_s a_s M. Coefficients phenomenological: critical square, non-analytic \|P\|³, G_s a_s = G a₀ imposed. It escapes link 6 through the gradient term γ, exactly the escape CFG661 names | astra STABLE_SOURCED_RESPONSE, POSITIVE_POLARIZATION |
| 8 | prediction of link 7 | onset length ℓ_γ = γ/(βB) ∝ M^(−1/2): the law turns on later in low-mass systems, with one universal γ | **UNTESTED** | astra; CFG662 proposed |
| 9 | energy for any settling | signed exchange (import for IC-C, export for IC-B); a constant vacuum cannot supply; feedback-driven gravitational work transfers energy (+0.3% of binding) but **does not select the profile** | **OPEN** | astra SETTLED_HALO_RESULT, GRAVITATIONAL_POWER_SOURCE, receiver work; CFG542/544 |
| 10 | heating-law route (FKPS Q_c = C a₀ v ρ_b) | needs σ ∝ 1/(n v²) | **BLOCKED in the Born-Yukawa class** (slope identity A = −pq, B = −4 + 2q); supply-limited bath is an open type | astra STABLE_SCREENING_AND_SUPPLY |

## 2. What this means, stated plainly

1. **If links 4–7 are right, galaxies need no settling.** The law is the static response of a separate stiff field sector to the
   baryons; the cold matter can stay collisionless. That is consistent with the merger result (CFG623: only α = 0 allowed; CFG639
   and CFG641 are queued) and removes the merger–galaxy α tension instead of tuning α.
2. **The price is two sectors**: collisionless cold matter (link 2) plus a response field (link 7). The record already showed
   that "one field doing both" is two components under one label (CFG288, CFG635), so this is not a new defeat, but it must be
   said.
3. **Three things are still missing, and each is now a sharp question:**
   - **(a) Coefficients.** Derive the critical square, the |P|³ term and G_s a_s = G a₀ from actual degrees of freedom, and the
     vacuum link of row 1. Without that, link 7 is phenomenology.
   - **(b) Lensing.** Link 7's φ is a separate scalar. A conformally coupled scalar does not bend light, so as written the response
     sector would not lens, and galaxy–galaxy lensing would see only baryons plus cold matter. Coupling it to the metric
     (disformal, AeST-like) is required if lensing follows the law; the dipolar (metric) version is the unstable one (row 6). This
     **lensing ⇄ stability fork** is the most important open structural question.
   - **(c) Cold matter inside galaxies.** If cold matter is collisionless and also present in galaxies (the record's census:
     about 0.13 of the cosmic share retained), it adds mass on top of the response sector's law. Whether SPARC tolerates that is
     untested.

## 3. Proposed division of work (for astra and the owner to adjust)

- **astra (field-theory side):** (a) derive or protect link 7's coefficients; (b) specify a metric coupling for the response
  sector and test its stability with the gravitating sector included; the abundance of link 2.
- **this chat (framework and data side, block CFG660–669):**
  - CFG662: score link 7 on raw SPARC with one universal stiffness (its interpolation ν = 1 + y^(−1/2) at γ = 0, the
    ℓ_γ ∝ M^(−1/2) onset), frozen criteria first.
  - CFG663: the lensing fork on raw data: compare the record's raw KiDS ESD (CFG700's data path) with "response does not lens"
    (baryons + collisionless cold matter only) and "response lenses".
  - CFG664: link 3(c), collisionless cold matter added to the law on SPARC at the record's retention.
  - The queued merger grids (CFG639, CFG641) continue unchanged.

## 4. Not claimed

No complete mechanism. No derivation of a₀, κ or Ω_c/Ω_b. Link 4 is spherical only. Link 7 is a construction with imposed
coefficients. Links 9–10 are open. Nothing here is evidence for the carrier's existence.
