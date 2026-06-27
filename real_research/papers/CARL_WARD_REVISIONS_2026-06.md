# Carl Ward review — the 5 revisions, applied

Reviewer (Carl Ward) recommended **accept with minor revisions**, all in the direction of claiming *less*. The independent tests held (algebra correct; the central no-go survived an adversarial non-stationary/evolving-DE stress-test). The five scoping revisions are now applied to `DESITTER_UNRUH_A0_NOGO_2026.md` (GitHub working copy; Zenodo republish pending Carl's go).

| # | Section | What changed | Backed by |
|---|---|---|---|
| 1 | §5 | Replaced the bare "a₀(z=3) ≈ 0.74" with the **combo-dependent band (median 0.61–0.78)** + **~2.4–2.7σ significance, explicitly inherited from (and weaker than) DESI's 2.8–4.2σ** w₀wₐ preference. Not a clean detection. | Real DESI posterior, `reviews/a0z_desi_chains_propagation.py` (exit 0) |
| 2 | §5 | Corrected the near-field direction: a₀(z) is **non-monotonic** — **+3 to +8% *above* local at z≈0.3–0.7**, through unity ~z≈1.3, decline only z≳2. The old "high-z BTFR sits slightly *below* local" is wrong in the accessible (z≲1) regime. | same script (real chains, all 3 SN combos) |
| 3 | §4.2 | Replaced the asserted "operates at super-horizon frequencies" with the **computed** result: ω_MOND ≈ 0.17 H is *near* the horizon; the O(ε) gradient expansion with the IBP boundary term retained finds no sign-flipping loophole and **corroborates** (not cutoff-independently proves, since IR-sensitive) the stationary passivity result. | matches the reviewer's own stress-test |
| 4 | §2 | Added the caveat that the surface-gravity gloss R⋆ = √(8π/Λ) is a **constant-Λ** statement; the density reading a₀=(c/2)√(Gρ_DE) is the primitive one and generalizes to ρ_DE(z) (basis of §5). The geometric picture is the w=−1 special case. | — |
| 5 | Abstract | Reframed: of the three items, (1) is algebra, (2) is borrowed; **(3) the no-go set is the load-bearing contribution.** Dropped the bare 0.74 from the conclusion, replaced with the marginal/non-monotonic band framing. | — |

**Net:** every revision tightens a claim toward what is actually established — exactly the reviewer's recommendation and the author's standing position. The a₀(z) prediction is now honestly a *marginal, non-monotonic, DESI-hostage band*, reproducible from the committed chain-propagation script.

**Outstanding (optional, the reviewer's note):** swap the **DR2** chains for the DR1 ones used here once the DR2 portal is public (currently DESI-auth-walled); identical code, only strengthens the significance.
