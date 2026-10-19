# CFG847 FROZEN CRITERIA: how far can lensing differ from dynamics in the framework? (gravitational-slip bound; before any script)

**Source.** Path 2 of the 2026-10-19 review of Codex's work. Canonical v2 lists "predict lensing from a relativistic completion"
as not done. This lane does not build the completion; it bounds the lensing–dynamics mismatch for the CLASS of parents the record
uses (GR + a cold, dust-like gravitating component + the stiffened P-field, CFG43-type), and compares it with test precision.

**Disclosed up front (by-construction check):** if the extra gravity is real, pressureless (dust-like) cold energy, lensing tracing
dynamics follows largely from that premise. The content here is the SIZE of the residual slip from the components that are not
dust: the cold energy's own velocity dispersion, the P-field's potential energy W and its stiffness (gradient) energy.

## Bound (weak field, static, spherical, order of magnitude; declared)
- In GR, the slip Φ − Ψ is sourced only by anisotropic stress: |Φ − Ψ| ≤ 8πG r² Π_max / c², with Π_max ≤ the largest non-dust
  stress present inside r. Ratio to the dynamical potential: s = |Φ − Ψ| / v_c².
- Stresses considered (each bounded by its energy density):
  1. cold-energy dispersion: Π₁ = ρ_c σ², σ² = v_c²/2 (isothermal-like) → s₁ = 8πG r² ρ_c σ² / (c² v_c²);
  2. P-field potential energy: Π₂ = |W(u)| with K W′(u) = u²/(a0 − u), K = 4πG (canonical v2 stiffened action), evaluated at the
     field value u at radius r, taken as u = a0 g_N/(g_N + a0) ... declared as the law's u ≤ a0 with a cap u ≤ 0.999 a0 (the
     logarithmic wall), and the bracket W ≤ (a0²/4πG)·|ln(1 − u/a0)|;
  3. stiffness energy: Π₃ = (γ/2)|∇P|² with γ = K L*²/2 and |∇P| ~ ρ_c (the source scale), L* ∈ [24 pc, 1 kpc] (CFG820 window).
- Systems (both footings): dwarf (M_b 1e7 M_⊙, r 0.3 kpc), Milky-Way-like disc (6e10; r 10 and 100 kpc), group (1e12; 300 kpc),
  cluster (1.5e14; 1 Mpc). ρ_c from the settled law profile at r.

## Classes
- **LENSING = DYNAMICS AT TEST PRECISION** if the summed s ≤ 1e-2 for every system and footing (lensing tests reach ~5–10%).
- **SLIP POSSIBLY TESTABLE** if any s lies in (1e-2, 1). **SLIP LARGE** if any s ≥ 1.
- The class is conditional on a well-posed covariant parent of this type existing (not shown here; stated).

## Controls
- K1: for a pure dust component the slip term from (1) vanishes as σ → 0 (scales ∝ σ²).
- MUTATE (separate output): replace the field-stress cap by a TeVeS-like O(1) anisotropic stress Π = ρ_c c² × 1e-3 → must
  class SLIP LARGE or POSSIBLY TESTABLE (the bound is sensitive to the parent class, as it should be).

κ = ½ fitted; cold energy mass required; not theory closed.
