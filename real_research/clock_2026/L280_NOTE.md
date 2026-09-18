# L280 — the α₂ reconciliation of the standing candidate (2026-09-18)

**The problem.** The candidate's scorecard (FINAL_THEORY_CANDIDATE_2026-09-05, row 4) reads "PPN derived: PASS … α₂(clock) =
−6×10⁻⁶" while the solar-spin bound is |α₂| < 4×10⁻⁷ (Nordtvedt 1987; BPS 2011 quote ≲ 10⁻⁷). Nothing reconciled the two.

**The identities (Lean: `lean_2026/L280_alpha_ppn.lean`).** With the pipeline's map of the clock sector onto Einstein-æther,
c₁ = K_B, c₃ = −K_B, c₄ = c₁₄ − K_B (c₁₃ = 0), the Foster–Jacobson parameters reduce exactly to

    α₁ = −4 c₁₄,        α₂ = c₁₄ [c₁₄(1 + 2c₂) − c₂] / [c₂ (2 − c₁₄)],        α₂ = 0 ⟺ c₂ = c₁₄/(1 − 2c₁₄).

The khronometric formulas of Blas, Pujolàs & Sibiryakov (2011, eq. 5.34), which are the appropriate ones for a hypersurface-
orthogonal clock (they warn the æther α₁,₂ cannot be used in general because transverse æther modes contaminate them), give at
β = c₁₃ = 0, α = c₁₄, λ′ = c₂: α₁ = −4c₁₄ and α₂ = (c₁₄/2)(c₁₄/c₂ − 1); the difference from the æther closed form is
c₁₄²(c₁₄ + 3c₂)/[2c₂(2 − c₁₄)], below 10⁻⁹ everywhere in the candidate's range. So the record's method was right for c₁₃ = 0,
and both treatments vanish on the same equal-speed locus (every mode at c), the c₂* the pipeline found in g03v.

**The two corners that pass everything** (|α₁| < 10⁻⁴, |α₂| < 4×10⁻⁷, Cherenkov c₂ ≥ c₁₄, the dark-sector locus
|K₂| = (2 − K_B)²/c₂ inside [5×10⁴, 3.24×10⁵]):

| corner | condition | α₁ | α₂ | G_N/G − 1 | √c₁₄ M_P |
|---|---|---|---|---|---|
| rigid (c₂ ≫ c₁₄) | c₁₄ ≤ 8.0×10⁻⁷ (2.0×10⁻⁷ at the 10⁻⁷ limit); c₂ free in the locus window | −3.2×10⁻⁶ | −4×10⁻⁷ | 4×10⁻⁷ | 1.1×10¹⁶ GeV |
| equal-speed | c₂ = c₁₄/(1 − 2c₁₄), c₁₄ ∈ [1.0×10⁻⁵, 2.5×10⁻⁵] (|K₂| ∈ [1.3, 3.24]×10⁵) | −4×10⁻⁵ to −10⁻⁴ | 0 | 5×10⁻⁶ | 3.9×10¹⁶ GeV |

**The finding.** The corner the record used (c₁₄ = 10⁻⁵, c₂ = 1) has α₂ = −5.0×10⁻⁶, 12× over the bound: row 4 was not a pass on
α₂. It becomes one at c₁₄ ≤ 8×10⁻⁷ or on the equal-speed locus; nothing else on the record moves (α₁ tighter, G_N closer to G, the
strong-coupling scale at 10¹⁶ GeV as BPS estimate for their own model). CK10 is settled. Nothing here derives κ.
