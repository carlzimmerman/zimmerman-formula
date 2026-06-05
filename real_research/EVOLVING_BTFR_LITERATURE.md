# The evolving BTFR in the literature — Marongwe & Kauffman (2025) vs the a₀↔Λ framework

**C. Zimmerman, June 2026.** While grounding the high-z BTFR prediction (Door 3) in real data, I found a
directly-competing paper and I'm reporting it straight, because it changes the novelty picture and sharpens the
tests. No spin.

## The find

**Marongwe & Kauffman, *"The Evolving Baryonic Tully–Fisher Relation: A Universal Law from Galaxies to Clusters,"*
arXiv:2511.20188 (Nov 2025)** independently propose that **the BTFR normalization evolves with cosmic time** while
the slope stays fixed at ~4. Because the BTFR is `V⁴ = G·M_b·a₀`, the normalization *is* a₀ — so this paper is
literally proposing **"the MOND acceleration scale evolves with cosmic time."** That is the core idea of this
framework, now in the literature from another group.

**What that means honestly:** the "a₀ evolves" idea is live, publishable, and not crazy — but the *bare concept* of
an evolving BTFR normalization is no longer uniquely ours. What remains distinct is the *mechanism*, the *functional
form*, and the *coefficient*. Those differ sharply, and that's where the real content (and the discriminating tests)
live.

## Side-by-side (verified numerically, `coefficient_landscape.py` + inline checks)

| | **This framework (Zimmerman)** | **Marongwe–Kauffman 2025** |
|---|---|---|
| Origin of a₀ | `a₀ = c²√(Λ/32π)` — the cosmological constant / dark-energy density | "Nexus Paradigm" quantum gravity: spacetime as Bloch wave-packets; DM = Ricci solitons; their Eq. 9 |
| Static coefficient | `a₀ = cH₀/6.99 = 9.36×10⁻¹¹` (i.e. `cH_Λ/√(32π/3)`) | `a₀ = cH₀/2π = 1.04×10⁻¹⁰` (their Eq. 7–9) |
| → numerical a₀ | 9.4×10⁻¹¹ m/s² | 1.04×10⁻¹⁰ m/s² (**11% higher**; both inside the data band [9, 13]×10⁻¹¹) |
| Evolution law | `a₀(z) ∝ √ρ_DE(z)` — **mild, non-monotonic** (peaks z~0.4, then declines) | `M_b ∝ e^(−4H₀t)·V⁴`, t = time since formation — **steep, exponential** |
| Predicted BTFR offset by z=3 | **+0.13 dex** in M_b at fixed V (computed) | much steeper (calibrated to the 0.6–0.8 dex cluster offset) |
| Cluster offset (0.6–0.8 dex) | **NOT** from a₀ evolution (predicts only −0.02 dex to z~0.3); inherited MOND cluster residual | **explained** as a formation-epoch effect (galaxies form z~2–3, clusters z<1) |

## The two sharp, honest takeaways

**1. The coefficient question I flagged is real — and now it's an inter-theory dispute.** My coefficient landscape
identified the one genuinely-open ~8% as "√(32π/3)=5.79 vs thermal 2π=6.28." Marongwe–Kauffman independently derive
**exactly the 2π value** (`a₀ = cH₀/2π`) from their quantum gravity. So the "2π vs 32π/3" fork is not academic —
two different theories land on the two sides of it. They differ by ~11% in a₀, which is *inside* today's
interpolating-function systematic, so current rotation-curve data **cannot yet decide between them.** Pinning a₀ to
better than ~10% (with a first-principles interpolating function) becomes a real discriminator between two published
frameworks — not just a check on one.

**2. The cluster offset cleanly separates the two evolution laws — and is honestly awkward for the steep reading.**
The observed galaxy–cluster BTFR offset is 0.6–0.8 dex. Marongwe–Kauffman *attribute* it to BTFR evolution, which
forces a steep exponential law. **This framework cannot do that** — `√ρ_DE` gives only ~0.02 dex of a₀-evolution out
to the cluster epoch (z~0.3), 30× too small. So:
   - In *this* framework, the cluster offset is **not** evolution; it is the long-known MOND cluster residual (the
     same red-team #2 limitation — clusters need a separate component). The mild `√ρ_DE` law is *consistent with*
     clusters being a separate problem.
   - In the M–K reading, the same offset *is* the evolution, which then predicts **large** high-z disc offsets.
   - **These are distinguishable by data:** the high-z disc BTFR offset should be **small and √ρ_DE-shaped** (this
     framework: ~0.06 dex at z=2, ~0.13 at z=3) vs **large** (M–K's steep law). The existing high-z disc samples
     (Übler+2017 etc.) showing only *modest* offsets actually favor the **mild** law over the steep one.

## The real-data check: the sign is confirmed, but it's not yet a discriminator

[Übler et al. 2017, KMOS³D (arXiv:1703.04321)](https://arxiv.org/abs/1703.04321) measured the baryonic TFR at z~0.9
and z~2.3 and found **"higher baryonic masses at fixed circular velocity at z~2.3"** and a **positive evolution of
the baryonic TFR zero-point from z~0.9 to z~2.3.** That is exactly the framework's *sign* (smaller a₀ at high z →
discs below the z=0 BTFR → more baryonic mass at fixed V). **But** this sign is *shared* with ΛCDM (lower DM fraction
at high z) and with M–K, so it is a **consistency check, not a discriminator.** The magnitude reported is modest —
consistent with the mild `√ρ_DE` law, and (so far) with the framework's "existing samples can't yet decide" forecast.

## What is genuinely still distinct to this framework (the honest novelty residue)

The concept "a₀ evolves" is now shared. What is **not** in Marongwe–Kauffman, and remains specific here:
1. **The mechanism is the cosmological constant itself**: `a₀ = c²√(Λ/32π)`, i.e. a₀ *is* √ρ_Λ — not a quantum-gravity
   soliton spectrum. This ties a₀ to a *measured* quantity (Λ), not a new paradigm.
2. **The specific `√ρ_DE(z)` form tied to DESI dark energy** — including its **non-monotonic** shape (peak at z~0.4).
   M–K's `e^(−4H₀t)` is monotonic and steep. The shapes are different and testable against each other.
3. **The coefficient-free bridge** `a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE0)` — a parameter-free cross-check against the
   dark-energy history, with the 32π (or 2π) cancelling. M–K have no analog.

## Bottom line

Someone published the evolving-a₀ idea first *as a concept* — that's the honest news, and it validates that the idea
is taken seriously. But the two frameworks are **physically distinct and observationally distinguishable**: by the
coefficient (√(32π/3) vs 2π, an ~11% a₀ question), by the evolution steepness (mild √ρ_DE vs steep exponential, the
high-z disc offset magnitude), and by the unique `√ρ_DE`-vs-DESI correlation that only this framework predicts. The
right next move is to keep sharpening exactly those three discriminators.

**Sources:**
- [Marongwe & Kauffman 2025, "The Evolving Baryonic Tully–Fisher Relation" (arXiv:2511.20188)](https://arxiv.org/abs/2511.20188)
- [Übler et al. 2017, "The Evolution of the Tully–Fisher Relation between z~2.3 and z~0.9 with KMOS³D" (arXiv:1703.04321)](https://arxiv.org/abs/1703.04321)
- Galaxy–cluster BTFR offset 0.6–0.8 dex: Gonzalez et al. 2013; Chiu et al. 2018 (as compiled in arXiv:2511.20188)
