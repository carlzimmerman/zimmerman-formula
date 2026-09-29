# CFG50 — the tidal-closure fluid action: an auxiliary baryon-sourced potential, and reciprocity

Scripts: `D1_action_reciprocity.py` (6 checks; MUTATE=a fails C4) and `D2_wellposed_nogo.py` (6 checks; MUTATE=b fails W3b and W3c); shared `Dcommon.py`, which imports CFG44's `Bcommon` read-only. Each runs in about two seconds; outputs `_MUTATE_<mode>.out` (mode 0 is the main run). Written by a delegated agent and re-run here (both main runs pass, both controls fail).

## What was tested

CFG44 found that for spherical baryons the target ρ_c g_tot = a₀ M_b(<r)/(4πr³) equals a **local tidal closure**, ρ_c g = (a₀/4πG) T_⊥. CFG44's exclusions did not cover a fluid whose stress is a functional of the tidal tensor T_ij = (δ_ij ∇² − ∂_i∂_j)Φ_b of an **auxiliary potential sourced by baryons only**, with a multiplier making Φ_b baryon-sourced so the baryons do not couple to it directly. This lane writes that action in the Newtonian weak-field reduction (S = S_b + S_c − ∫|∇Φ_tot|²/8πG + ∫λ(∇²Φ_b − 4πGρ_b)/4πG + ½χ∫T_ij Π^ij, Π^ij the fluid's second moment) and asks for the reaction on the baryons.

## Result: it fails, under CFG44's obstructions plus one new bound

| statement | label |
|---|---|
| T_ij is identically divergence-free, so used as a stress it exerts no force; a cold fluid has S_int = 0; isotropic Π gives a contact term 4πGχ ∫ρ_b P | DERIVED |
| the requested coefficient a₀/8πG is not an energy density for Π = ρσ²; it must be a time², χ | DERIVED |
| **reciprocity**: a_react = −∇λ; for S_int = ∫F^ij T_ij, a_react = 8πG[F_⊥' + (F_⊥ − F_rr)/r]; renormalising Φ_b's normalisation does not remove it | DERIVED |
| a prescribed stress is ill-posed (ω² = −iF·k/ρ₀); the same stress derived from an action gives exactly zero force | DERIVED |
| no equation of state built from local Φ_b fields has the target as a static equilibrium (the ρ_b terms force μ_ρ = μ_T = 0, then μ_r is inconsistent) | DERIVED |
| the closure itself (which coupling picks ρ_T), the value of χ, and Φ_b built on the overdensity in FRW | POSTULATED |
| the relativistic completion ((Φ_b, λ) has kinetic matrix [[0, D], [D, 0]], a dipole-ghost structure) | OPEN |

Key numbers (exponential spheres, canonical a₀):
- **The reaction on the baryons is O(g_law), not zero or small,** and opposite in sign to the fluid-side force inside r < 1.7h. At the ghost-limited strength, reaction/g_law at r = 0.3h and 1h is 7.3 and 1.3 (M_b = 10⁹), 3.1 and 0.54 (10¹⁰), 0.23 and 0.03 (10¹²). It shrinks with the fluid-to-baryon mass ratio in the Newtonian regime, so it is a strong exclusion in dwarfs and LSBs and a weaker one in massive spirals. The virtual-work check agrees with the adjoint formula to 0.24%.
- **A second, independent ceiling.** The largest ghost-free outward force on the fluid is **0.505 g_tot** (at r ≈ h, mass-independent; 0.34 at 0.3h, 0.14 at 3h), never the full closure. a₀ drops out.
- **Universality:** the χ needed differs by ×64 across M_b = 10⁹–10¹².
- **FRW:** uniform ρ_b gives T_ij = Ω_b H² δ_ij, which renormalises the fluid inertia by 1 + χΩ_bH²: 4 × 10⁻⁸ to 3 × 10⁻⁶ today, but 50 to 3400 at z = 1100. Incompatible with GR + CDM at the CMB unless Φ_b is built on the overdensity (postulated).
- Point mass: Π is isotropic and the force on the fluid is exactly zero.

**Controls (both fail as required).** MUTATE=a (Φ_b sourced by the fluid): the closure becomes seed-dependent, 0.60–0.68 dex from P2 (the baryon-sourced version matches P2 to 3 × 10⁻¹² dex). MUTATE=b (reversed χ): the force turns inward and the ghost boundary moves ×91 outward.

**Caveat:** the analysis assumes the coupling must carry the closure force (f = 1 per unit fluid mass).

## Standing

**The tidal-tensor coupling does not rescue the fluid.** It falls under CFG44's reciprocity and state-independent-stress obstructions and adds a ceiling of 0.5 on the force it can supply. What CFG44 found survives: a temperature-slaved or locally virialised fluid, as restatements. The remaining object is still the non-adiabatic, nonlocal enclosed-mass exchange, which is Gap 1's ownership object.

Nothing here says the theory is closed.
