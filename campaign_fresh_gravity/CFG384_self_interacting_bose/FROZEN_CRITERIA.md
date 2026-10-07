# CFG384 FROZEN CRITERIA: can a self-interaction relax the ~eV cold-fluid field to CFG383's condensate split, within the limits?
(owner 2026-10-06: "yeah keep going"; follow-up of CFG383; committed before any script)

**Setup.** The cold fluid is the record's complex scalar of mass m (CFG383: m_half = 0.81 eV, range 0.62–1.04 eV). It gets one self-coupling, V ⊃ (λ/4)|Φ|⁴. That adds one dark-sector constant; baryons stay untouched (G9).
- Natural units. 2→2 cross-section σ = λ²/(128π m²), converted with ħc.
- Bose-enhanced relaxation rate Γ = D σ v n, with D the degeneracy n λ_T³ from CFG383, v = σ_v (dispersion) and n = ρ_c/m. Inputs are CFG383's frozen systems.

**Gates (each evaluated over the m range and both species counts, g = 1 and 2).**
- **G1, relaxation.** Γ × 13.8 Gyr ≥ 1 in clusters (at R500) AND in the Milky Way, so the equilibrium fractions can be reached. This gives λ ≥ λ_min.
- **G2, Bullet Cluster.** σ/m < 1 cm²/g on the bare cross-section (declared; Randall et al. 2008). This gives λ ≤ λ_max.
- **G3, dust and structure.** The self-interaction pressure gives c_s² = λ ρ/(4 m⁴). Require:
  - c_s(z = 1100, cosmic mean cold density) < 1e-3 c (dust before recombination, as in CFG288 G-DUST);
  - today, the Jeans length in the Milky Way halo (c_s/√(Gρ)) below 1 kpc, so the fluid can still settle into kpc-scale phantom profiles. The condensate is also allowed to support itself.
  - Each condition gives an upper bound on λ.

**Verdict.**
- **OPEN WINDOW:** at some m in [0.62, 1.04] eV, λ_min ≤ min(λ_max, λ_G3) for g = 1. Report the window width in decades.
- **MARGINAL:** closed by less than a factor 3 in λ.
- **CLOSED:** closed by more than that.

**Also reported.**
- The window as a function of m.
- What the Bullet bound would have to relax to, as a factor.
- Whether the cross-section implied in galaxies is consistent with the record's settling-rate window (CFG245 / CFG382 report Γ ~ 3 H_L in the Milky Way and 0.6 H_L in clusters).

**MUTATE** (CFG384_MUTATE=1): the Bose enhancement is removed (D := 1). The window must shrink by more than 1 decade. MUTATE writes separate outputs.

**Scope.**
- Order-of-magnitude rates. Ideal-gas degeneracy. Classical Bullet bound, with no velocity dependence.
- κ = ½ is fitted. The cold fluid's amount is still not derived.
