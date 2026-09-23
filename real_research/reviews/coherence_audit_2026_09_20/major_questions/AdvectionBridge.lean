import Mathlib

/-!
The exact finite-dimensional bridge which the NS lane implementation missed.
D i j means partial_j u_i, i.e. rows are velocity components. The chain rule
identifying grad (|u|^2/2) with D.transpose*u is stated in the adjacent report,
not formalized here. This is algebra, not a Navier--Stokes regularity theorem.
-/
namespace CoherenceMajorQuestions
noncomputable section

def advect (u : Fin 3 → ℝ) (D : Fin 3 → Fin 3 → ℝ) (i : Fin 3) : ℝ :=
  ∑ j, u j * D i j

def transposed (u : Fin 3 → ℝ) (D : Fin 3 → Fin 3 → ℝ) (i : Fin 3) : ℝ :=
  ∑ j, u j * D j i

/-- The finite chain-rule polynomial for the implemented contraction. -/
theorem implemented_is_half_square_derivative
    (u : Fin 3 → ℝ) (D : Fin 3 → Fin 3 → ℝ) (i : Fin 3) :
    transposed u D i = (∑ j, 2 * u j * D j i) / 2 := by
  simp [transposed, Fin.sum_univ_succ]
  ring

/-- Both contractions have the same pointwise energy contraction. An energy
test cannot distinguish this index error, even before space integration. -/
theorem energy_contraction_blind
    (u : Fin 3 → ℝ) (D : Fin 3 → Fin 3 → ℝ) :
    (∑ i, u i * advect u D i) = ∑ i, u i * transposed u D i := by
  simp [advect, transposed, Fin.sum_univ_succ]
  ring

def waveProject (k v : Fin 3 → ℝ) (i : Fin 3) : ℝ :=
  v i - (∑ j, k j * v j) / (∑ j, k j * k j) * k i

/-- Every gradient Fourier polarization lies in the projection kernel.
Zero wavevector is excluded here; the implemented code separately zeros it. -/
theorem projector_kills_gradient (k : Fin 3 → ℝ) (a : ℝ)
    (hk : (∑ j, k j * k j) ≠ 0) (i : Fin 3) :
    waveProject k (fun j => a * k j) i = 0 := by
  unfold waveProject
  have hs : (∑ j, k j * (a * k j)) = a * (∑ j, k j * k j) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [hs]
  rw [mul_div_cancel_right₀ a hk]
  ring

/-- At (x,y)=(0,pi/2), u=(sin y,0,sin x) has these exact values and
Jacobian. The actual advection is nonzero while the code's contraction is zero. -/
def witnessU : Fin 3 → ℝ := ![1,0,0]
def witnessD : Fin 3 → Fin 3 → ℝ := ![![0,0,0],![0,0,0],![1,0,0]]

theorem witness_correct : advect witnessU witnessD 2 = 1 := by
  norm_num [advect, witnessU, witnessD, Fin.sum_univ_three, Matrix.cons_val_two]

theorem witness_implemented : ∀ i, transposed witnessU witnessD i = 0 := by
  intro i
  fin_cases i <;> norm_num [transposed, witnessU, witnessD, Fin.sum_univ_three, Matrix.cons_val_two]

/-- The true witness advection has wavevectors (1,±1,0) polarized in z;
it survives the Leray projector. -/
theorem witness_survives_projection (s : ℝ) :
    waveProject ![1,s,0] ![0,0,1] 2 = 1 := by
  norm_num [waveProject, Fin.sum_univ_three, Matrix.cons_val_two]

#print axioms implemented_is_half_square_derivative
#print axioms energy_contraction_blind
#print axioms projector_kills_gradient
#print axioms witness_correct
#print axioms witness_implemented
#print axioms witness_survives_projection
end
end CoherenceMajorQuestions
