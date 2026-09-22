/-
  K004 — the roundabout to kappa = 1/2, certified empty.

  Scope. Lean certifies the algebra below. It does not certify that kappa = 1/2
  is a law of nature. The header states which step is an identity and which
  step would have been the derivation.

  The tempting roundabout: the horizon ball sourced by rho_Lambda has Newtonian
  acceleration exactly (1/2) c H (the volume factor 4 pi/3 against the Einstein
  factor 3/(8 pi)). Move that half off c H onto the local scale s = c sqrt(G rho)
  and the product is s/2, i.e. kappa = 1/2. The move is an identity, and it is
  empty: c and H cancel, and the conclusion is the posit. The three compositions
  that keep the horizon miss 1/4 by the exact squares 2 pi/3, 8 pi/3, 32 pi/3.

  Separately, a pure cuscuton's energy density is its potential, for any
  coefficient. A tau-dependent coefficient (the L236 loophole) does not source
  expansion. This does not speak to the repo's extended clock, whose density is
  U/m_rel; that case is G001.

  What survives, and is not a derivation of the integer: deep matching with
  slope n forces kappa = 1/n. n = 2 is not selected by any theorem in this file.
-/
import Mathlib

/-! ## The horizon-ball half multiplies c H, not s -/

/-- The volume factor against the Einstein factor is exactly one half. -/
theorem ball_half : (4 / 3 : ℝ) * Real.pi * (3 / (8 * Real.pi)) = 1 / 2 := by
  field_simp
  ring

/-- Relocating the half from c H onto s cancels c and H. -/
theorem relocation_cancels (c H s : ℝ) (hc : c ≠ 0) (hH : H ≠ 0) :
    ((1 / 2 : ℝ) * c * H) * (s / (c * H)) = s / 2 := by
  field_simp

/-- The conclusion of the relocation is the definition of kappa = 1/2. No
gravitational symbol remains. This is the anti-tautology: the roundabout
outputs the posit. -/
theorem relocation_is_the_posit (s : ℝ) : s / 2 = (1 / 2 : ℝ) * s := by
  ring

/-! ## Compositions that keep the horizon miss 1/4 -/

theorem ball_kappa_sq (h : 0 ≤ (8 * Real.pi / 3 : ℝ)) :
    (Real.sqrt (8 * Real.pi / 3) / 2) ^ 2 = 2 * Real.pi / 3 := by
  have hs : (Real.sqrt (8 * Real.pi / 3)) ^ 2 = 8 * Real.pi / 3 := Real.sq_sqrt h
  have hdiv : (Real.sqrt (8 * Real.pi / 3) / 2) ^ 2 =
      (Real.sqrt (8 * Real.pi / 3)) ^ 2 / 4 := by ring
  rw [hdiv, hs]
  ring

theorem ball_kappa_miss :
    (Real.sqrt (8 * Real.pi / 3) / 2) ^ 2 ≠ (1 / 4 : ℝ) := by
  have hnonneg : 0 ≤ (8 * Real.pi / 3 : ℝ) := by positivity
  rw [ball_kappa_sq hnonneg]
  intro h
  have h8 : (8 : ℝ) * Real.pi = 3 := by
    have h1 : (2 : ℝ) * Real.pi / 3 = 1 / 4 := h
    field_simp at h1
    linarith
  have hpi : (3 : ℝ) < Real.pi := Real.pi_gt_three
  have hbig : (8 : ℝ) * Real.pi > 24 := by nlinarith
  linarith

theorem doubled_ball_kappa_sq :
    (Real.sqrt (8 * Real.pi / 3)) ^ 2 = 8 * Real.pi / 3 := by
  exact Real.sq_sqrt (by positivity)

theorem doubled_ball_miss :
    (Real.sqrt (8 * Real.pi / 3)) ^ 2 ≠ (1 / 4 : ℝ) := by
  rw [doubled_ball_kappa_sq]
  intro h
  have h8 : (8 : ℝ) * Real.pi = 3 / 4 := by
    have h1 : (8 : ℝ) * Real.pi / 3 = 1 / 4 := h
    field_simp at h1
    linarith
  have hpi : (3 : ℝ) < Real.pi := Real.pi_gt_three
  nlinarith

theorem milgrom_kappa_sq :
    (2 * Real.sqrt (8 * Real.pi / 3)) ^ 2 = 32 * Real.pi / 3 := by
  have hs : (Real.sqrt (8 * Real.pi / 3)) ^ 2 = 8 * Real.pi / 3 :=
    Real.sq_sqrt (by positivity)
  calc (2 * Real.sqrt (8 * Real.pi / 3)) ^ 2
      = 4 * (Real.sqrt (8 * Real.pi / 3)) ^ 2 := by ring
    _ = 4 * (8 * Real.pi / 3) := by rw [hs]
    _ = 32 * Real.pi / 3 := by ring

theorem milgrom_miss :
    (2 * Real.sqrt (8 * Real.pi / 3)) ^ 2 ≠ (1 / 4 : ℝ) := by
  rw [milgrom_kappa_sq]
  intro h
  have hpi : (3 : ℝ) < Real.pi := Real.pi_gt_three
  have h1 : (32 : ℝ) * Real.pi / 3 = 1 / 4 := h
  field_simp at h1
  nlinarith

/-! ## Pure cuscuton: the coefficient does not source the energy -/

/-- rho = 2X P_X - P with P = U s - V and s = sqrt(2X), s ≠ 0, is V.
The coefficient U cancels. A running U does not replace the potential
in the energy density. -/
theorem cuscuton_energy_is_the_potential (U V s : ℝ) (_hs : s ≠ 0) :
    (s * s) * (U / s) - (U * s - V) = V := by
  field_simp
  ring

/-- Friedmann at vanishing potential gives H = 0. The field equation
U' + 3 H U = 0 then forces U' = 0. No running branch expands. -/
theorem running_dies_when_expansion_dies (Up U : ℝ) :
    Up + 3 * (0 : ℝ) * U = Up := by
  ring

theorem no_potential_forces_no_expansion (H V : ℝ) (hF : H ^ 2 = V) (hV : V = 0) :
    H = 0 := by
  rw [hV, sq_eq_zero_iff] at hF
  exact hF

/-! ## What survives: kappa = 1/n, and n is not selected here -/

/-- Deep matching n (g/s) g = g_bar forces g^2 = s g_bar / n, so the
acceleration scale extracted as a0 = s/n has kappa = a0/s = 1/n.
Selecting n = 2 is not a theorem of this file. -/
theorem kappa_is_reciprocal_of_slope (n s g gbar : ℝ) (hn : n ≠ 0) (hs : s ≠ 0)
    (hdeep : n * (g / s) * g = gbar) : g ^ 2 = s * gbar / n := by
  field_simp at hdeep ⊢
  linarith

theorem reciprocal_at_two (n s : ℝ) (hn : n ≠ 0) (_hs : s ≠ 0) (h : n = 2) :
    (s / n) / s = 1 / 2 := by
  subst h
  field_simp

#print axioms ball_half
#print axioms relocation_cancels
#print axioms relocation_is_the_posit
#print axioms ball_kappa_miss
#print axioms doubled_ball_miss
#print axioms milgrom_miss
#print axioms cuscuton_energy_is_the_potential
#print axioms no_potential_forces_no_expansion
#print axioms kappa_is_reciprocal_of_slope
#print axioms reciprocal_at_two
