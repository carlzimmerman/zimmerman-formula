# CFG858 FROZEN CRITERIA: can the stiffened action produce the dwarfs' extra speed V_x² ≈ a0 × 31 pc? (derivation; before any script)

**Why.** CFG856/857: faint dwarfs carry an extra isothermal speed V_x ≈ 9–11 km/s that passes SPARC. Noted coincidence: V_x² ≈ a0 × 31 pc,
near the bottom of the stiffness window (L* ≥ 24 pc, CFG820). **Identity, stated first:** V² = a0 L is the same as L = r_M(M) with
M = V⁴/(G a0), so "31 pc" restates V_x as the deep-law speed of M ≈ 6e5 M_⊙; the only physics question is whether the stiffened action
generates such a term.

## The equation (canonical v2 stiffened action, as written: L = −|∇Φ − KP|²/2K − ρΦ − W(u) − (γ/2)|∇P|², K = 4πG, γ = K L*²/2)
Varying Φ gives ∇Φ = g_N + KP; varying P gives, with u = K|P| radial and outward-positive meaning added inward pull:
  u²/(a0 − u) − (L*²/2) [u'' + 2u'/r − 2u/r²] = g_N(r),   u(0) = 0, u → law solution for r ≫ L*.
(The bracket is the radial component of the vector Laplacian.) Total g = g_N + u.

## Systems and grid
- Plummer stellar profiles (M★ = Υ_SFH L_V, a = r_h) for Draco, Ursa Minor, Sextans, CVn I, Leo II, Fornax (CFG827/828 inputs), canonical a0
  (alt reported); L* ∈ {1, 3, 10, 24, 31, 100, 300, 1000} pc. Solved as a BVP on [1e-3 a, 300 a] (log grid; scipy solve_bvp; tolerance 1e-6;
  convergence checked by doubling nodes).
## Statistic and classes
- G_ratio(L*) = g(r_1/2) / g_law(r_1/2) (stiffened over unstiffened); also max over r of g/g_law (any overshoot anywhere).
- **STIFFNESS CAN SUPPLY V_x** if for some L* in [24 pc, 1 kpc] G_ratio ≥ 10^{+0.3} (the +0.3 to +0.6 dex the dwarfs need) for most dwarfs.
- **STIFFNESS ONLY SCREENS** if G_ratio ≤ 1 + 1e-3 for every dwarf and L* (and no overshoot > 1% anywhere).
- **SMALL OVERSHOOT** otherwise (report the maximum).
- Report the coincidence's base rate: the probability that a random log-uniform L in the window [24 pc, 1 kpc] lies within ×1.3 of 24 pc.

## Controls
- K1: L* → 0 (1 pc) reproduces the algebraic law to 1e-3 at r_1/2. MUTATE (separate output): flip the sign of the stiffness term
  (anti-stiffness) → must change G_ratio (shows the solver responds to the term).

κ = ½ fitted; cold energy mass required; not theory closed.
