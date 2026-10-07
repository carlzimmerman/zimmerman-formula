# CFG472: can a pressure-supported cold fluid in plain Newtonian equilibrium BE the law's target? (lead L2 from the openai-math cross-analysis) FROZEN before any script exists

Owner chat 10-07 ("have the council run some computational analysis"). κ = ½ fitted; both footings (in these units, a footing only rescales r_M). No DM particle; the cold mass is still required.

**The question (L2, deepseek_push/openai_math_cross_analysis_2026-10/README.md).** A gravity-only settling force must hold the cold fluid at ρ_ph. In FL1 (40c6ae144) the fluid's pressure channels are:
- the Thomas–Fermi polytrope P = K ρ² (n = 1);
- a kinetic / multistream effective temperature (isothermal, P = σ² ρ).

So ask: is ρ_ph[ρ_b] a **hydrostatic equilibrium of the fluid in the Newtonian potential of baryons + fluid**, for a physically fixed EOS?

**Analytic part (sympy, checked).**
- In the deep regime, ρ_ph = √(G M a₀) / (4π G r²) = V_f² / (4π G r²) with V_f⁴ = G M a₀. That is exactly the singular isothermal sphere (SIS) of velocity V_f.
- An isothermal fluid in a flat-curve potential has ρ ∝ r^(−V_f²/σ²), which equals the target's r⁻² iff σ² = V_f²/2.
- K-A: verify both identities symbolically.

**Numerical part (units G = a₀ = M_b = 1, so r_M = 1, V_f = 1).**
- Baryons: Hernquist spheres with scale a = 0.1, 0.3, 1, 3 r_M (compact HSB to diffuse LSB; declared, not fitted).
- Target: M_ph(<r) = (ν_mono(g_N/a₀) − 1) M_b(<r) (CFG4_common.nu_mono), spherical.
- **Model I (isothermal):** σ² = V_f²/2 FIXED by the BTFR (no freedom). ρ_c = ρ₀ exp(−(Φ − Φ(r_min))/σ²), with Poisson for baryons + fluid integrated outward from r_min = 1e-3. ONE free number per galaxy: ρ₀ (scan, log-spaced 1e-8 to 1e4, 600 values).
- **Model P (Thomas–Fermi polytrope):** ρ_c = max(ρ₀ − (Φ − Φ(r_min))/(2K), 0). TWO free numbers per galaxy, ρ₀ and K (scan 120 × 120, log-spaced; K in 1e-4 to 1e4).
- Statistic: D = max over r ∈ [0.5, 30] r_M of |log10(M_c(<r) / M_ph(<r))|, minimised over the free numbers. Also reported over [0.2, 100].

**Verdicts per model.**
- **SHAPE REPRODUCED** if D ≤ 0.04 dex (≈ 10%) at all four compactnesses.
- **SHAPE FAILS** if D > 0.1 dex at any compactness.
- PARTIAL otherwise.
- Model I passing would mean the law's target = an isothermal fluid at σ² = V_f²/2 in plain gravity, and the law's whole content reduces to the BTFR normalisation selecting σ.
- Model P failing would mean FL1's Thomas–Fermi channel cannot be the settling force.

**Controls.**
- K-A: the symbolic identities above.
- K-B: with baryons removed (a → ∞ limit, M_b → 0), Model I's far field gives M_c(<r)/r → 2σ²/G = 1 within 5% over r ∈ [10, 100] (the SIS slope).

**MUTATE (`--mutate`).** The target is replaced by M_ph × (r/r_M)^0.3 (a non-isothermal shape). Model I must give D > 0.1 at a = 0.3; exit 1 when detected.
