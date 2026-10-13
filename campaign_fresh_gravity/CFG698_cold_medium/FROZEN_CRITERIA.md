# CFG698 — P as the displacement of a real cold medium: where the tether acts decides cosmology (frozen criteria)

Block CFG690–699. Written 2026-10-13, before any CFG698 script or number. Committed alone. κ = ½ fitted; both footings, never
pooled; the cold energy's mass is required; no particle species; not theory closed.

## The step (named in CFG697)
P = −ρ̄_c ξ: the displacement ξ of a cold medium with mean density ρ̄_c.
- The bound charge ∇·P = −ρ̄_c∇·ξ = δρ_c is the medium's own density perturbation.
- −(∇·P)Φ is its gravitational coupling.
- The kinetic term ½ρ̄_c|ξ̇|² fixes I = 1/ρ̄_c.
- The background density ρ̄_c enters Friedmann, restoring the cosmic mean that CFG697 found missing.
- The W(P) of CFG695 becomes a **tether**: the energy cost of displacing the medium relative to the cosmic frame.

## Tests (sympy; EdS-normalised linear growth with Ω_b = 0.049, Ω_c = 0.26 as in the record's cosmology inputs)
- **J1. Jeans neutrality.** With the critical tether W = 2πG P², the medium's longitudinal self-gravity term cancels exactly:
  ξ̈ = (4πGρ̄_c − W″ρ̄_c)ξ = 0 for k → 0. PASS iff the identity holds.
- **J2. Tether everywhere.** Coupled linear growth of (δ_b, δ_c), with the medium responding only to the baryons' field:
  δ̈_b = 4πG(ρ̄_bδ_b + ρ̄_cδ_c), δ̈_c = 4πGρ̄_bδ_b. Report the growing exponent p (δ ∝ a^p, matter era) against the free cold
  medium (p = 1).
  - **This version FAILS cosmology iff p ≤ 0.9:** growth too slow for the record's own D2/CMB requirements.
- **J3. Tether only inside bound basins (CFG693 reading).** Outside basins the medium is free and pressureless, so p = 1 exactly
  (verify). Inside basins the relaxed state is the law's profile. This version is identical to the record's **candidate B**
  (cold energy settling to the law inside bound regions; CFG541–554 / CFG624 identity) and inherits B's committed verdicts:
  - X-COP (CFG4/624 identity 0.946 ± 0.080);
  - Local Group (CFG624 M1);
  - D2 (CFG596 KiDS EXCLUDED, Δχ² +68.7);
  - C3 (CFG529).
  - Report them as inherited, not re-run.

## Verdict
- If J1 holds, J2 fails and J3 gives p = 1, the construction's only viable cosmological form is **candidate B with a mechanism**:
  - the cold energy is a real medium;
  - inside bound basins a critical, saturating tether holds it, and it relaxes by radiation to the law's profile;
  - outside, it is a free cold component.
- The mechanism then removes B's structural gaps (M1a, M2b, B3 well-posedness on fixed baryons). It does **not** change B's
  data failures (C3, D2), which belong to the law's profile itself (CFG678).

## MUTATE (`CFG698_MUTATE=1`, exit 1 iff both bite)
- **M1:** tether coefficient 1.1 × critical. J1 must fail (net restoring force).
- **M2:** no tether anywhere (free medium everywhere). J3's p = 1 must hold, but the static galaxy profile is lost: the
  equilibrium u(g) has no deep-law solution.
