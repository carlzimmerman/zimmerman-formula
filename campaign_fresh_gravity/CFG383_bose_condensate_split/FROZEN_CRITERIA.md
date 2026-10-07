# CFG383 FROZEN CRITERIA: the cold fluid as a Bose field. Is the "unsettled" cluster fraction the non-condensed (normal) fraction?
(owner 2026-10-06: "yeah go"; idea from OpenAI math result 267, positive-temperature Bose–Einstein condensation; committed before any script)

**Idea.** The record's cold fluid is a free complex scalar (CFG288 road W, mass window 2e-20 to 2.78 eV).
- Treated as a Bose gas of mass m, virialised at velocity dispersion σ, it has effective temperature k T = m σ² and is condensed below T_c.
- Reading: the condensate settles into the phantom shape (the law), while the normal fraction stays unsettled.
- This would explain why galaxies obey the law (cold, dense, condensed) while clusters carry unsettled cold fluid (CFG379: about half beyond the phantom target).

**Formulas (ideal uniform Bose gas, one species; the complex field's antiparticles are reported as a factor-2 variant).**
- λ_T = h/(m σ √(2π)); degeneracy D = n λ_T³ with n = ρ_c/m.
- Condensate fraction f_c = 1 − ζ(3/2)/D for D > ζ(3/2) = 2.612, else 0. Unsettled fraction u = 1 − f_c.

**Systems (declared inputs; cold-fluid density ρ_c and σ).**
- Clusters: σ = 1000 km/s (bracket 800–1200). ρ_c = 0.85 × (500 ρ_crit)/3, the local density at R500 for ρ ∝ r⁻².
- Groups: σ = 400 km/s (300–500), the same ρ_c at their R500.
- Milky Way: σ = V/√2 with V = 200 km/s. ρ_c = the settled phantom density V²/(4πG r²) at r = 30 kpc.
- UFDs: σ = 5 km/s. ρ_c = 1e6 Msun/((4/3)π (100 pc)³).
- ρ_crit uses H₀ = 67.4.

**Step 1 (fix m from clusters).** m_half is the mass at which clusters have u = 0.5. Because the levels are bias-dominated (audit, f982f4a34), also take the bracket u ∈ [0.3, 0.7] → [m_lo, m_hi], using the σ bracket.

**Step 2 (predict, no freedom).**
- u for groups, the Milky Way and UFDs at m_half.
- Is m_half inside the record's fluid window, [2e-20, 2.78] eV?
- Is it in a CFG367 surviving piece (≥ 8.8e-12 eV is unconstrained by black-hole spins)?

**Verdict.**
- VIABLE: m_half lies in the window AND u(Milky Way) < 0.05 AND u(UFD) < 0.05 AND u(groups) < u(clusters).
- PARTIAL: some of these hold.
- FAILS: m_half lies outside the window, or the Milky Way or UFDs are non-condensed.

**Reported caveat (timescale, not scored).** A free field relaxes toward equilibrium only through gravity. Report the gravitational condensation time τ_gr ≈ (b√2/(12π³)) m v⁶/(G² n² ħ³ ln Λ) (Levkov et al. 2018, b ≈ 0.7, ln Λ ≈ ln(m v R/ħ)) for each system, against the age 13.8 Gyr. If τ_gr exceeds the age in galaxies, the equilibrium fractions do not apply there.

**MUTATE** (CFG383_MUTATE=1): σ_cluster := σ_MW. Clusters must then be fully condensed (u < 0.05) at m_half. MUTATE writes separate outputs.

**Scope.** An ideal-gas estimate, not a derivation.
- A ~eV boson field is the record's cold fluid within its fluid window, not a new species. Its mass is still required, and its amount is not derived.
- κ = ½ is fitted.
