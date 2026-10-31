# CR2_core_scale_origin: FROZEN CRITERIA

Written before the script. **Disclosed first, including an error of mine.** CR1 called 1/3 "the scaling of Σ_coll" and offered the exponent as a filter on carriers. Reading the brief's table,
Σ_coll runs about M^0.24 by hand, the same as ET1's 0.238, so that label looks wrong and the filter may be empty. The brief already says the collapse branch gives the × 2 rise at about two-thirds of the amplitude.
CR1's closed list also omitted self-coupling (CA1), which is a real omission. Rough hand values seen: Σ_coll slope 0.239; b₁M near 1 at m_χ 556 GeV. Not blind.

**Inputs, read only.** ET1 S_need table. Σ_coll at 1e11…1e15 and f_cη at 1e12…1e14, brief §3. CA1: p = 5, 7, n 0.800, 0.571, s★(σ_ref) 0.1545, 0.1058 cm²/g, m_χ if M = E_Λ 1.3e13, 5.7e6 GeV, G6 floor 556, 685 GeV, E_Λ 2.24, 2.46 meV. OS1: q_f 0.892, 0.748; dwarf caps q ≤ 0.13, 0.22. Each footing keeps its own values.

## Tests
- **T1 slope.** Σ_coll's own log slope against ET1's fit. Below 1e11 the table is extrapolated (linear and quadratic in lg M, both reported). S_need uses M200, the rule uses M_t, so also shift lg M by +0.1. ORIGIN IS COLLAPSE if the slope is within 2σ in all variants.
- **T2 constant ratio.** Fit S_need = A Σ_coll, one free A; report χ² against S_need flat and each CR1 exponent. A against f_cη at 1e12, and at 1e13, 1e14: if A differs from them by > 1.25, amplitude is the open gap.
- **T3 self-coupling slope.** Convert ET1's exponent to q and n, using σ ∝ M^(1/3). Compare OS1's q_f and the dwarf caps. Add row J to CR1's grid.
- **T4 lock on heavy field.** Row J with baryon locking set at sphaleron freeze-out: solve R = (m/m_p) c 𝓕(m/T*) with the fermion function 𝓕 for T* 130–200 GeV, c 0.1–10. Is m ≥ CA1's G6 floor? R7 is stated plainly: a field quantum at this mass is a heavy particle by any test.
- **T5 EFT validity.** Pair exchange is valid only for r > 1/M. Using s ∝ M^(−8/5) m^(−7/5) (p = 5), M^(−8/7) m^(−13/7) (p = 7), anchored on CA1's row, solve M at each m. Grade b₁M with b₁ = √(σ_T/π) at 20 and 1000 km/s. VALID needs b₁M ≥ 1 at both for some m ≥ G6 floor.

## Word rule
CR1's README gets corrected forward whatever T1 says. "Derived" is not used: collapse scaling is a fact about P(k) and formation time, and core form and amplitude stay separate. κ = ½ FITTED. Not "theory closed".
