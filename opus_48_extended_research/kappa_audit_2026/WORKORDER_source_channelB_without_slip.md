# WORK ORDER — source channel B without breaking Φ=Ψ (the joint that decides κ=1/2)

This is the single open task that would turn κ=1/2 from "empirically anchored" into "derived."
Basis: `K_AUDIT_two_channel_dust_obstruction.py` (the count fails for dust) +
`K_AUDIT_slope_is_degree2_independent.py` (κ needs only the slope = channel count).

## The exact obstruction (proved)

- Channel B is "engaged" (an independent Poisson operator in the response) ⟺ G_kk = 2∇²(Φ−Ψ) ≠ 0
  ⟺ **(Φ−Ψ) is a nonzero field** ⟺ **bare metric slip Φ ≠ Ψ**.
- Lensing=dynamics (L279, γ_PPN=1) ⟺ the **effective** potentials matter and light follow are equal:
  Φ_eff = Ψ_eff.
- Therefore channel-B-engaged AND lensing=dynamics can BOTH hold **only if bare ≠ effective**: a
  field (the scalar) must supply (Φ_eff−Φ_bare) and (Ψ_eff−Ψ_bare) so that a nonzero **bare** slip
  (which engages channel B → count 2 → slope 2 → κ=1/2) maps to **zero effective** slip (lensing=dynamics).
- If bare = effective (no scalar contribution to the metric matter/light follow), then
  channel-B-engaged ⇒ slip ⇒ NOT lensing=dynamics. **NO-GO in that case.**

## The escape shape (the only door left)

A single covariant scalar φ that:
1. **Engages channel B in the deep-MOND response** — its anisotropic stress T^φ_ij (∝ ∂_iφ ∂_jφ,
   which is anisotropic for a spherical source even for pressureless matter) sources ∇²(Φ_bare−Ψ_bare)
   ≠ 0, so the response has two independent channels → slope 2 → κ=1/2 for DUST.
2. **Leaves zero effective slip** — matter and light couple to ONE effective metric
   g_eff = g_Einstein + (φ terms) with Φ_eff = Ψ_eff, so lensing=dynamics holds on what is observed.

## The pincer it must thread (do NOT re-open dead routes)

- **Single metric / GW170817.** matter and light couple to the SAME effective metric; a second
  (disformal) metric is dead on the differential Shapiro delay (CK01; PAPER24/25 v2 errata). The
  φ-contribution must be conformal-type (or otherwise GW-safe), not a distinct null cone.
- **PPN α₁.** the AeST vector/scalar sector kills on α₁ = −2(K_B+2) when tuned for this response
  (relativistic-MOND closure notes). Any φ that engages channel B must keep |α₁|, α₂, α₃ within the
  Solar-System bounds. This is where the escape most likely dies — check it FIRST.
- **No ghost / stability** on the φ kinetic term in the two-channel configuration.

## Success criterion (falsifiable, Lean/PPN-checkable)

Exhibit the covariant action for which ALL hold:
- (a) deep-MOND response slope = 2 sourced by the scalar-engaged channel B, for a **pressureless**
  spherical source (the K_AUDIT dust obstruction must FLIP: G_kk ≠ 0 in the response);
- (b) effective γ_PPN = 1 (Φ_eff = Ψ_eff) — lensing=dynamics preserved;
- (c) single effective metric (GW170817-safe);
- (d) α₁, α₂, α₃ within Solar-System bounds; no ghost.

Regression check to keep: the current obstruction script must be extendable to show G_kk(response) ≠ 0
while γ_PPN stays 1. If any of (a)–(d) cannot co-hold, that is a **no-go** — and a no-go proof
(channel-B engagement necessarily forces slip, or α₁ violation, or a second metric) is EQUALLY
valuable: it settles κ=1/2 as empirically-anchored-only, honestly and permanently.

## Honest feasibility flag

This threads a needle three prior pincers have nearly closed (single-metric MOND, AeST α₁, disformal
GW170817). It may well be a no-go. Either outcome closes the κ=1/2 question: a working action makes
κ=1/2 derived; a no-go makes it measured-with-structure. Do not paper the gap — report which.
