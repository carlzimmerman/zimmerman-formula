# CFG842 FROZEN CRITERIA: can a satellite capture enough of its host's cold energy to explain its excess? (before any script)

**Why.** CFG827–839: the faint (satellite) dwarfs carry ~×2–3 extra inner mass; tides do not explain it; their own catchment
supply is tight/fails (CFG823); expelled-gas free cold energy lands too far out (CFG822); the framework's external field
lowers the boost (wrong sign). One framework channel is unchecked: satellites orbit INSIDE the host's settled cold-energy halo.
Cold energy is collisionless, so any capture conserves fine-grained phase-space density (Liouville).

## Inputs
- MW host: M_b = 6.0e10 M_⊙ (CFG821), canonical a0; settled cold profile M_c(<r) = ½ M_b (√(1 + 4r²/r_M²) − 1),
  ρ_c(r) = (dM_c/dr)/(4π r²), r_M = √(G M_b/a0). Host cold dispersion σ_h(D) = V_c(D)/√2 with V_c² = D g_law(D)
  (isothermal-like; declared). Same with the M_MW 8e10 bracket.
- Satellites: the 12 MW satellites of CFG839 (Δ from CFG828, r_1/2, D = present distance AND framework pericentre from CFG839).
- Needed extra inner density: ρ_need = 3 M_extra / (4π r_1/2³), M_extra = M_obs(<r_1/2) − M_law(<r_1/2), from g_obs = g_law 10^Δ
  at r_1/2 (M = g r²/G).
- **Liouville ceiling:** the densest a captured collisionless population can be inside a satellite of internal dispersion σ_s
  is ρ_max = ρ_c(D) (σ_s / σ_h(D))³ (maximum coarse-grained phase-space density cannot exceed the host's), σ_s = the observed σ.
  Evaluated at the present distance and at pericentre (higher ρ_c; take the larger ceiling).

## Classes
- **CAPTURE EXCLUDED** if, for every satellite, ρ_max / ρ_need < 0.1 at both distances and both MW masses.
- **CAPTURE POSSIBLE** if any satellite has ρ_max / ρ_need ≥ 1. **MARGINAL** otherwise.

## Controls
- K1: ρ_c(r) integrates back to M_c(<r) at r = 100 kpc to 1e-3.
- MUTATE (separate output): σ_h set equal to σ_s (no phase-space dilution) → the ratio must rise by (σ_h/σ_s)³.

κ = ½ fitted; cold energy mass required; not theory closed.
