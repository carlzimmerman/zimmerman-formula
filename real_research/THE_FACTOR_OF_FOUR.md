# Where the 4 comes from: dissecting 32π = 4 × 8π

**C. Zimmerman, June 2026.** "Make sure it's legit and logical and explainable." Here is the honest answer, computed
(`predictions/factor_of_four.py`), not asserted.

## The decomposition collapses the question to a single ½

Substituting `ρ_Λ = Λc²/(8πG)` (Einstein) into `a₀ = c²√(Λ/32π)` gives the clean form
```
a₀ = (c/2)·√(G ρ_Λ) = c²/(2 L_Λ),   L_Λ = c/√(G ρ_Λ)  (the "vacuum gravitational length", ≈ 51 Gly)
```
So:
- **The 8π is forced** — it is Einstein's coupling turning the geometric Λ into the gravitating density ρ_Λ.
- **`√(Gρ_Λ)` is the physical skeleton** — the vacuum's own gravitational frequency `ω_Λ` (dark energy treated as a
  gravitating fluid). The 8π/3 that separates `ω_Λ` from the expansion rate `H_Λ` lives in H, not in a₀.
- **The entire "4" is `(½)²`** — the prefactor in `a₀ = (c/2)√(Gρ_Λ)`. Nothing else is free.

## The ½ has three exactly-equivalent, physical readings

1. **`a₀·τ_Λ = c/2`** — a₀ brings a particle from rest to *half the speed of light* in one vacuum gravitational
   free-fall time `τ_Λ = 1/√(Gρ_Λ)`.
2. **`a₀ = c²/(2L_Λ)`** — a₀ is the **surface gravity** of the vacuum gravitational length L_Λ — the same universal ½
   that appears in every horizon surface gravity (e.g. Schwarzschild κ = c²/2R_s).
3. **Holographic reading** — if a₀ emerges from de Sitter horizon entropy (`S = A/4`), the "4" is the
   **Bekenstein–Hawking ¼**. Same number, deeper origin.

## Is it legit, logical, forced? (the honest verdict)

- **LEGIT — yes.** The 4 is not arbitrary. The data *requires* a prefactor near ½: with no prefactor (κ=1) the
  formula gives a₀ = 1.9×10⁻¹⁰, ~2× too large, which is **excluded**. So a factor of order 4 *must* be there — it is
  data-confirmed, not invented.
- **LOGICAL/EXPLAINABLE — yes.** It is the universal free-fall / surface-gravity (or Bekenstein–Hawking) prefactor,
  with the three equivalent statements above.
- **FORCED to exactly 4 — no, at the ~10–15% level.** Writing `a₀ = κ·c√(Gρ_Λ)`, the measured a₀ pins `κ ∈ [0.48,
  0.69]`. The framework's κ=½=0.50 sits at the **low edge** (matching the simple-μ fit 9.1×10⁻¹¹); the central value
  mildly prefers κ≈0.56, where the Jeans scale (1/√π = 0.564) lands. The thermal/Marongwe–Kauffman reading, taken
  *consistently* with the same pure-Λ rate (`a₀=cH_Λ/2π`), instead gives the clean κ = √6/(3√π) ≈ 0.46 (Z = 2π) —
  just below the band, on the *other* side of ½. These well-motivated readings fan out within ~±15% of ½, below the
  interpolating-function systematic, so the data cannot separate them.

| reading of the prefactor κ | κ | Z = cH_Λ/a₀ | a₀ [m/s²] | verdict |
|---|---|---|---|---|
| **framework: free-fall / surface-gravity ½** | 0.500 | 5.79 (=√(32π/3)) | 9.36×10⁻¹¹ | in band (low edge) |
| no prefactor (κ=1) | 1.000 | 2.89 | 1.87×10⁻¹⁰ | **excluded** |
| Jeans scale 1/√π | 0.564 | 5.13 | 1.06×10⁻¹⁰ | in band (central) |
| thermal 2π (Marongwe–Kauffman, cH_Λ/2π) | 0.461 (=√6/(3√π)) | 6.28 (=2π) | 8.63×10⁻¹¹ | just below band |
| data-allowed band | 0.48–0.69 | 4.2–6.0 | 9.0–13×10⁻¹¹ | — |

> **Note — the thermal row uses the pure-Λ rate, for consistency.** Every κ in this table is defined against
> `√(Gρ_Λ)`, i.e. the *pure-Λ* de Sitter rate `H_Λ = √(8π/3)·√(Gρ_Λ)` (what ρ_Λ alone would drive). For the thermal
> reading `a₀ = cH/2π` that fixes `H = H_Λ`, giving the closed forms `κ = √6/(3√π) = 0.461` and `Z = 2π` *exactly*.
> Marongwe–Kauffman instead quote the *measured* `H₀` (full ΛCDM, Ω_Λ ≈ 0.685): `a₀ = cH₀/2π = 1.04×10⁻¹⁰`, an
> effective `κ ≈ 0.557` (larger by `1/√Ω_Λ`). That mixes matter back in through `H₀`, so it sits on a different
> footing; it is the number MK actually cite, recorded here only for reference. Using the consistent value does not
> change the verdict — and at κ = 0.461, *below* ½ and just under the band while the Jeans reading (0.564) sits
> *above*, the motivated readings now fan out across ½ rather than clustering, which only sharpens the "not forced"
> conclusion.

## Bottom line

The 4 = (½)² is a **legitimate, explainable free-fall / Bekenstein–Hawking prefactor**, data-selected to be ≈½ —
well-motivated and *not numerology*. What is *not* yet pinned is the last ~10–15% (exactly 4 vs ~3.3, i.e. ½ vs the
Jeans/thermal ~0.56): that requires committing to a specific covariant theory. AeST fixes it through the (currently
inserted) normalization of its free function C(𝒬); Marongwe–Kauffman's quantum gravity forces the thermal 2π
instead. **That normalization is the genuine open frontier** — and it cancels entirely in the coefficient-free bridge,
so it does not touch the evolution test.

## Independent corroboration: symmetry fixes the *form*, not the coefficient

Singh 2026 (arXiv:2601.04290, "A Relativistic MOND," T. P. Singh) reaches the same verdict from a different
direction. He shows the deep-MOND action is conformally invariant under a 10-parameter group isomorphic to the
de Sitter group `SO(4,1)`, and that this symmetry **forces** the free-function *form* `F(y) ∼ (2/3) y^{3/2}` as
`y→0` — but **explicitly not** its coefficient. He writes the scale as `a₀ = c²/(ξ ℓ_dS)` with `ξ = O(1)` "fixed
by matching to the static (AQUAL) limit," i.e. *set by matching, not derived from the symmetry*. Singh's ξ plays
exactly the role of this framework's `Z/κ`: the same undetermined O(1) prefactor relating `a₀` to a de
Sitter/cosmological length. The conclusion is independent and identical — **conformal/de Sitter symmetry forces
the shape; only AQUAL-limit matching sets the number** — which is precisely why the prefactor, not the form, is
the genuine open frontier.
