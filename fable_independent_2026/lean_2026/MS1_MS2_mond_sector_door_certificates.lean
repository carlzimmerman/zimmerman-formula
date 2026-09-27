import Mathlib

/-!
# MS1–MS2 — the MOND-sector door: which switch variable keeps the carrier kernel-invisible once the gate is varied

SCOPE. `real_research/mond_sector_gate_2026/MS1_gate_variation_reciprocity.py` varies CV1's gate f = W(U) on four
readings of the switch variable U and derives the Euler–Lagrange equations with sympy. Integrated, they fix the
potentials in closed form in terms of the Newtonian potential u_N of all matter and the gate's edge term
c = C·W′(U)·B (B = 8πG ∂L/∂f):

* curvature door (U = C∇²Φ) and MOND-sector door (U = C∇²(Φ − v)): u = u_N − c/2;
* matter door (U = C(ρ_b + ρ_d)) and baryons door (U = Cρ_b): u = u_N;
* every door: Φ = u + f·P (P = Ψ/2, CV1's gated phantom);
* λ = −2 f P on the curvature, matter and baryons doors, λ = −2 f P + c on the MOND-sector door;
* the dark component's potential is Φ + λ/2, less c/(8πG) on the matter door (U reads ρ_d there).

Lean certifies the algebra that decides the doors (the derivations themselves are sympy's, in the lane), and the
two MS2 identities the door's phenomenology rests on.

* `mond_sector_door_carrier_newtonian`: on the MOND-sector door the dark component's potential is exactly u_N.
* `baryons_door_carrier_newtonian`: on the baryons door the dark component's potential is exactly u_N.
* `curvature_door_leak`: on the curvature door it is u_N − c/2.
* `matter_door_leak`: on the matter door it is u_N − c/(8πG).
* `curvature_door_newtonian_iff`: the curvature door keeps the dark component Newtonian iff c = 0, i.e. only off the
  gate's transition (W′ = 0) or where the MOND sector carries no energy (B = 0).
* `matter_door_newtonian_iff`: the same for the matter door (G > 0).
* `door_contrast_in_web`: in the unbound web (gas tracing matter, ρ_b = f_b ρ_m, no phantom) the MOND-sector door's
  contrast is f_b times the matter door's.
* `door_activation_ratio`: so the matter overdensity needed to switch the door on is 1/f_b times the matter door's.
-/

/-- MOND-sector door: u = u_N − c/2, Φ = u + fP, λ = −2fP + c ⇒ Φ + λ/2 = u_N. -/
theorem mond_sector_door_carrier_newtonian (uN f P c : ℝ) :
    ((uN - c / 2) + f * P) + (-2 * f * P + c) / 2 = uN := by
  ring

/-- Baryons door: u = u_N, Φ = u + fP, λ = −2fP ⇒ Φ + λ/2 = u_N. -/
theorem baryons_door_carrier_newtonian (uN f P : ℝ) :
    (uN + f * P) + (-2 * f * P) / 2 = uN := by
  ring

/-- Curvature door: u = u_N − c/2, Φ = u + fP, λ = −2fP ⇒ Φ + λ/2 = u_N − c/2. -/
theorem curvature_door_leak (uN f P c : ℝ) :
    ((uN - c / 2) + f * P) + (-2 * f * P) / 2 = uN - c / 2 := by
  ring

/-- Matter door: u = u_N, Φ = u + fP, λ = −2fP, and U reads ρ_d ⇒ the potential is u_N − c/(8πG). -/
theorem matter_door_leak (uN f P c G : ℝ) :
    (uN + f * P) + (-2 * f * P) / 2 - c / (8 * Real.pi * G) = uN - c / (8 * Real.pi * G) := by
  ring

/-- The curvature door is Newtonian for the dark component iff the gate's edge term vanishes. -/
theorem curvature_door_newtonian_iff (uN f P c : ℝ) :
    ((uN - c / 2) + f * P) + (-2 * f * P) / 2 = uN ↔ c = 0 := by
  constructor
  · intro h
    have : uN - c / 2 = uN := by linarith
    linarith
  · intro h
    subst h
    ring

/-- The matter door is Newtonian for the dark component iff the gate's edge term vanishes (G > 0). -/
theorem matter_door_newtonian_iff (uN f P c G : ℝ) (hG : 0 < G) :
    (uN + f * P) + (-2 * f * P) / 2 - c / (8 * Real.pi * G) = uN ↔ c = 0 := by
  have hk : (8 * Real.pi * G) ≠ 0 := by positivity
  constructor
  · intro h
    have h1 : c / (8 * Real.pi * G) = 0 := by linarith
    rcases div_eq_zero_iff.mp h1 with h2 | h2
    · exact h2
    · exact absurd h2 hk
  · intro h
    subst h
    ring

/-- In the unbound web (ρ_b = f_b ρ_m, background ρ̄_b = f_b ρ̄_m, no phantom) the door's contrast is f_b times the
matter door's: 1.5 Ω (ρ_b/ρ̄_m − f_b) = f_b · 1.5 Ω (ρ_m/ρ̄_m − 1). -/
theorem door_contrast_in_web (Om fb rhom rhobar : ℝ) (hr : rhobar ≠ 0) :
    1.5 * Om * ((fb * rhom) / rhobar - fb) = fb * (1.5 * Om * (rhom / rhobar - 1)) := by
  field_simp

/-- Hence, with 0 < f_b, the door switches on at overdensity x/(1.5 Ω f_b): 1/f_b times the matter door's x/(1.5 Ω). -/
theorem door_activation_ratio (Om fb x : ℝ) (hO : 0 < Om) (hf : 0 < fb) :
    x / (1.5 * Om * fb) = (1 / fb) * (x / (1.5 * Om)) := by
  field_simp

#print axioms mond_sector_door_carrier_newtonian
#print axioms baryons_door_carrier_newtonian
#print axioms curvature_door_leak
#print axioms matter_door_leak
#print axioms curvature_door_newtonian_iff
#print axioms matter_door_newtonian_iff
#print axioms door_contrast_in_web
#print axioms door_activation_ratio
