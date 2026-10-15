# CFG794 FROZEN CRITERIA: can any known enhancement speed up cold-energy → light conversion enough? (theory only, committed before any script)

This is a theoretical calculation. It follows on from CFG789 (spontaneous lifetime τ ≥ 4.4 × 10¹⁵ yr from the cosmic optical
background) and CFG792 (a sail-thickness converter needs S = 6.4 × 10³⁴ over that rate). Photon energy ħω = 2.5 eV (the CFG790
line). Ambient u_c = ρc² = 6.1 × 10⁻⁵ J/m³ with velocity dispersion σ = 230 km/s. External numbers are quoted from memory
(provisional).

## The four standard enhancement classes
- **(a) Resonant (Q).** Enhancement = min(Q_cavity, Q_field), with Q_field = (c/σ)² and Q_cavity ≤ 10¹¹ (optical, extreme).
- **(b) Stimulated (Bose).** The rate into a photon mode is multiplied by (1 + n). Laser-threshold test: the spontaneous rate
  into one mode is r = u_c/(τ ħω ρ_m), where ρ_m = ω²Δω/(π²c³) and Δω = ω/Q_field. Net energy gain requires r > ω/Q_cavity.
  Report the shortfall factor.
- **(c) Coherent volume (N²).** Gain ≤ (ℓ_c/d)², with ℓ_c = ħc/(mc²·σ/c), m = 2.5 eV (conditional on the CFG790 portal
  scale) and d = 0.5 μm.
- **(d) Parametric.** Shown analytically to reduce to (b): the pump supplies the photons, and the cold-energy draw is still
  the stimulated term.

## Verdict classes
- **GAP CLOSABLE:** the best passive product (a)·(c) is ≥ S, OR (b) is above threshold.
- **NOT CLOSABLE:** otherwise. Report the shortfall in orders of magnitude.

## Controls
- **K1:** the mode-density formula, integrated with Planck occupation, reproduces aT⁴ within 1% at 5800 K.
- **K2:** recompute S = 6.4 × 10³⁴ (CFG792).
- **MUTATE** (separate outputs): with τ = 1 μs, (b) must cross threshold.

κ fitted; not theory closed.
