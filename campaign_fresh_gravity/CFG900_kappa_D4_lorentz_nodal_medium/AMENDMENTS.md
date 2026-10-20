# CFG900 amendments to FROZEN_CRITERIA.md (32264ab5d)

Written after the freeze and BEFORE any script of this lane was written or run. Committed alone. FROZEN_CRITERIA.md is not
edited; the scorer prints both the frozen and the amended expectation for every item below.

## A1. M4 expected factor (hand-algebra slip in the frozen file)

- **Frozen text (§6 M4, §0):** "κ_H × 1/√2 (0.643 → 0.455)".
- **Correction:** κ_H × (1/2)^{3/2} = 0.3536 (0.643 → 0.227).
- **Why.** The horizon-locus posit gives a₀ = cH³/(12πGρ_DE), independent of Friedmann. With a footing Friedmann relation
  H² = e·8πGρ_DE/3, a₀ = (2e/9)cH and κ_H = (2e/9)·H/√(Gρ_DE) = (8πe/3)^{3/2}/(12π), so κ_H ∝ e^{3/2}. The frozen estimate kept
  only the √e from H/√(Gρ) and dropped the e in H³ = H·H².
- **What is unchanged.** The tooth's purpose: κ_H must move down under 8πG → 4πG, and κ_slot and the tube trade formula must
  not move. The scorer reports the frozen factor as FAILS AS FROZEN (slip) and grades the tooth on the amended factor.

## A2. Pauli–Villars: a second admissible regulator set (addition, no class change)

- **Frozen text (§3 V4):** the PV vacuum constant has "sign and size set by the regulator masses", with the explicit set
  (C₁, C₂, M₁², M₂²) = (−2, 1, M², 2M²).
- **Hand check before any script:** with two regulators the constant is (A/3)·M₁²M₂²/(M₁ + M₂), so it is always positive
  (0.828·(A/3)M³ for the frozen set). Its sign is free only with three or more regulators.
- **Addition:** a three-regulator admissible set, C = (−3, 3, −1) with M_i = (M, 2M, 3M). It satisfies Σ C_i = −1 (with the
  physical C₀ = 1, Σ = 0) and Σ C_i M_i² = 0, and gives the constant (A/3)(−6)M³ < 0. Both sets are printed. V4's class
  (CONDITION) is unchanged.

## A3. ħ powers under H1r (addition, report only)

- **Frozen text (§2):** at fixed (N, m*, v, h, Λ, q_b, C), a₀ ∝ ħ³ and κ² ∝ ħ⁹.
- **Addition:** under H1r (m* = ħk₀/c) and Λ = ε_Λħck₀/2, at fixed (N, k₀, h, ε_Λ, q_b, C), a₀ ∝ ħ² and κ² ∝ ħ³. Both are
  printed. Either way κ is not ħ-free at fixed microscopic parameters (a TRADE).
