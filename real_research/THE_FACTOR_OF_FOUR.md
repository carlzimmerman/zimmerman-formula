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
  mildly prefers κ≈0.56 — which is *also* where the Jeans scale (1/√π = 0.564) and the thermal/Marongwe–Kauffman
  reading (a₀=cH₀/2π → κ≈0.56) land. These differ from ½ by <15%, below the interpolating-function systematic, so the
  data cannot separate them.

| reading of the prefactor κ | κ | Z = cH_Λ/a₀ | a₀ [m/s²] | verdict |
|---|---|---|---|---|
| **framework: free-fall / surface-gravity ½** | 0.500 | 5.79 (=√(32π/3)) | 9.36×10⁻¹¹ | in band (low edge) |
| no prefactor (κ=1) | 1.000 | 2.89 | 1.87×10⁻¹⁰ | **excluded** |
| Jeans scale 1/√π | 0.564 | 5.13 | 1.06×10⁻¹⁰ | in band (central) |
| thermal 2π (Marongwe–Kauffman) | 0.557 | 5.20 | 1.04×10⁻¹⁰ | in band (central) |
| data-allowed band | 0.48–0.69 | 4.2–6.0 | 9.0–13×10⁻¹¹ | — |

## Bottom line

The 4 = (½)² is a **legitimate, explainable free-fall / Bekenstein–Hawking prefactor**, data-selected to be ≈½ —
well-motivated and *not numerology*. What is *not* yet pinned is the last ~10–15% (exactly 4 vs ~3.3, i.e. ½ vs the
Jeans/thermal ~0.56): that requires committing to a specific covariant theory. AeST fixes it through the (currently
inserted) normalization of its free function C(𝒬); Marongwe–Kauffman's quantum gravity forces the thermal 2π
instead. **That normalization is the genuine open frontier** — and it cancels entirely in the coefficient-free bridge,
so it does not touch the evolution test.
