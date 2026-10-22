# VERDICT — A83

**The algebraic spine is certified, and it is not theatre.** Forty-seven new Lean 4 theorems in the
existing `lean_2026` project (`lake build A83` green from a cold start), zero `sorry`, zero `axiom`,
zero `native_decide`, every footprint exactly `[propext, Classical.choice, Quot.sound]`, and a
theorem delta of +47 names over A8_lean with 0 overlap, 0 deletions and — proved by byte-identical
source hashes — 0 weakening of the existing 40. The theorems formalize the A68 2×2 kinetic matrix and
its `β = −2/3` degeneracy, the `α = γ` single-stiffness condition, `Z, Q₀ > 0`, and the order-four
vanishing of `ω² = αp⁴/Z` with the punctured filter Lean requires; the A63/A54/A75 law `g_N = g²/(g+a₀)`
with both slopes (`dg/dg_N = 1 + a₀²/(g²+2a₀g) > 1`, by the inverse-function theorem), the
rectification obstruction `odd ⟹ f''(0) = 0` against `θ''(0) = −2`, and the mass cancellation
`a_sat = k_BTc/ħ`; the A72 coefficient **through** its Friedmann premise (`√(Gρ) = 2H/Z`,
`κ_DE = Z/4π = √(2/3π)`, `8π/κ² = 12π²`) with the unreduced branch isolated as `48π⁴`; and A78's
matter-inclusive `β = (2/3)Ω_L(r_Λ − 1)`, `β > 0 ⟺ r_Λ > 1`, the BBN window and its sharpness. Two
requested items are deliberately *not* certified as phrased: "second-class ⟺ α = γ" is false to A68
(its Dirac matrix carries no α or γ), and the gate's temperature-blindness is a definitional `rfl`
labelled as such and excluded from the substantive count; the task's `Q₀` formula and its
`48π⁴ = 4674.6` are transcription slips, corrected and documented rather than copied. What remains
outside Lean is exactly what A75 says remains outside the action — the thermal identification of
`a₀`, the PDE reduction, and the gates — and none of it is assumed in any of the 47 theorems.
