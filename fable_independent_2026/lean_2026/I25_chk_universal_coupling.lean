import Mathlib

/-!
# I25 — C-H/K boosts every minimally coupled source alike: no "additive" dark carrier

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs are hypotheses: L340's unitary
scalar block of C-H/K at ω = 0 (rows: slip, Hamiltonian, momentum, U-equation; C the kernel's constitutive
coefficient, α = α_c the khronon a²-coefficient, c₂ the K²-coefficient), with the matter source split into baryons
R_b and a dark carrier R_c. `gU` is a hypothetical direct coupling of the carrier to C-H's auxiliary U — a term
C-H/K does NOT contain; it is the control. Companion lane:
`real_research/dark_sector_2026/L345_chk_universal_carrier_pincer.py` (U0).

* `static_solution` — (ψ, φ, U, β) below solves the four static rows exactly.
* `carrier_boost_iff` — the carrier's coefficient in ψ equals the baryons' (the same MOND boost (1+C)) **iff gU = 0**:
  a minimally coupled carrier is boosted exactly like baryons ("universal"); L321's "additive" coupling is not
  realisable in C-H/K.
* `U_coupling_cancels_boost` — the only internal escape: gU = C removes the carrier's boost entirely (its response
  is then Newtonian up to the α_c renormalisation) — a coupling that would have to track the field-dependent kernel.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- The four static rows of L340's block (ω = 0). -/
def rowSlip (k ψ φ : ℝ) : Prop := 4 * k ^ 2 * ψ - 4 * k ^ 2 * φ = 0
def rowHam (k α ψ φ U Rb Rc : ℝ) : Prop := -4 * k ^ 2 * ψ - 4 * k ^ 2 * (U - φ) + 2 * α * k ^ 2 * φ - (Rb + Rc) = 0
def rowMom (k c2 β : ℝ) : Prop := -2 * c2 * k ^ 4 * β = 0
def rowU (k C gU φ U Rc : ℝ) : Prop := 4 * k ^ 2 * (U - φ) + 4 * k ^ 2 * C * U + gU * Rc = 0

def ψS (k C α gU Rb Rc : ℝ) : ℝ := ((1 + C) * (Rb + Rc) - gU * Rc) / (2 * k ^ 2 * (α * (1 + C) - 2))
def US (k C α gU Rb Rc : ℝ) : ℝ := (2 * α * k ^ 2 * ψS k C α gU Rb Rc - (Rb + Rc)) / (4 * k ^ 2)

theorem static_solution {k C α c2 gU Rb Rc : ℝ} (hk : k ≠ 0) (hD : α * (1 + C) - 2 ≠ 0) :
    rowSlip k (ψS k C α gU Rb Rc) (ψS k C α gU Rb Rc) ∧
    rowHam k α (ψS k C α gU Rb Rc) (ψS k C α gU Rb Rc) (US k C α gU Rb Rc) Rb Rc ∧
    rowMom k c2 0 ∧
    rowU k C gU (ψS k C α gU Rb Rc) (US k C α gU Rb Rc) Rc := by
  unfold rowSlip rowHam rowMom rowU US ψS
  refine ⟨by ring, ?_, by ring, ?_⟩
  · field_simp; ring
  · field_simp; ring

/-- Coefficients of R_b and R_c in ψ. -/
def coefB (k C α : ℝ) : ℝ := (1 + C) / (2 * k ^ 2 * (α * (1 + C) - 2))
def coefC (k C α gU : ℝ) : ℝ := (1 + C - gU) / (2 * k ^ 2 * (α * (1 + C) - 2))

theorem psi_decomposes {k C α gU Rb Rc : ℝ} :
    ψS k C α gU Rb Rc = coefB k C α * Rb + coefC k C α gU * Rc := by
  unfold ψS coefB coefC; ring

theorem carrier_boost_iff {k C α gU : ℝ} (hk : k ≠ 0) (hD : α * (1 + C) - 2 ≠ 0) :
    coefC k C α gU = coefB k C α ↔ gU = 0 := by
  unfold coefC coefB
  have hden : 2 * k ^ 2 * (α * (1 + C) - 2) ≠ 0 := mul_ne_zero (mul_ne_zero two_ne_zero (pow_ne_zero 2 hk)) hD
  rw [div_eq_div_iff hden hden]
  constructor
  · intro h
    have : gU * (2 * k ^ 2 * (α * (1 + C) - 2)) = 0 := by linarith
    rcases mul_eq_zero.mp this with h1 | h1
    · exact h1
    · exact absurd h1 hden
  · intro h; rw [h]; ring

theorem U_coupling_cancels_boost {k C α : ℝ} :
    coefC k C α C = 1 / (2 * k ^ 2 * (α * (1 + C) - 2)) := by
  unfold coefC; ring

end

#print axioms static_solution
#print axioms psi_decomposes
#print axioms carrier_boost_iff
#print axioms U_coupling_cancels_boost
