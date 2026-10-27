import Mathlib

/-! Own-framework leading NR coefficient and finite-coordinate energy audit.
Source: COLD_ENERGY_EQUATIONS.tex section2, natural units. No new fields,
profile target, MOND/LambdaCDM physical premises, quantum width or operator axiom.
The scalar/summed results are not noncommuting normal-ordered operator proofs.
Regulated operator interpretation and validity of NR reduction remain external.
-/
noncomputable section
namespace FrameworkNREnergy

def delta (m M : ℝ) : ℝ := M - 2 * m
def c3 (m M g : ℝ) : ℝ := g / (2 * m * Real.sqrt (2 * M))
def quartic (m M g rep : ℝ) : ℝ := (g ^ 2 / (M ^ 2 - 4 * m ^ 2) + rep) / (4 * m ^ 2)
def remainder (m M g rep : ℝ) : ℝ := quartic m M g rep - c3 m M g ^ 2 / delta m M

theorem c3_squared (m M g : ℝ) (hM : 0 ≤ M) :
    c3 m M g ^ 2 = g ^ 2 / (8 * m ^ 2 * M) := by
  unfold c3
  rw [div_pow, mul_pow, mul_pow, Real.sq_sqrt (by positivity : 0 ≤ 2 * M)]
  congr 1
  ring

theorem coefficient_identity (m M g rep : ℝ) (hm : 0 < m) (hM : 2 * m < M) :
    remainder m M g rep = rep / (4 * m ^ 2) + g ^ 2 / (8 * m ^ 2 * M * (M + 2 * m)) := by
  have hMp : 0 < M := by linarith
  have hd : 0 < M - 2 * m := by linarith
  have hp : 0 < M + 2 * m := by linarith
  have hgap : 0 < M ^ 2 - 4 * m ^ 2 := by
    have := mul_pos hd hp
    nlinarith
  unfold remainder
  rw [c3_squared m M g hMp.le]
  unfold quartic delta
  have hd' : M - m * 2 ≠ 0 := by nlinarith
  field_simp [hm.ne', hMp.ne', hd.ne', hd', hp.ne', hgap.ne']
  ring

theorem remainder_nonnegative (m M g rep : ℝ) (hm : 0 < m) (hM : 2 * m < M)
    (hrep : 0 ≤ rep) : 0 ≤ remainder m M g rep := by
  rw [coefficient_identity m M g rep hm hM]
  have hMp : 0 < M := by linarith
  positivity

theorem remainder_strict (m M g rep : ℝ) (hm : 0 < m) (hM : 2 * m < M)
    (hrep : 0 < rep) : 0 < remainder m M g rep := by
  rw [coefficient_identity m M g rep hm hM]
  have hMp : 0 < M := by linarith
  positivity

/-- psi=x+i*y, b=u+i*v; real/imag psi²=(x²-y²,2xy). -/
def density (m M g rep x y u v : ℝ) : ℝ :=
  delta m M * (u ^ 2 + v ^ 2) +
    2 * c3 m M g * (u * (x ^ 2 - y ^ 2) + v * (2 * x * y)) +
      quartic m M g rep * (x ^ 2 + y ^ 2) ^ 2

def completedDensity (m M g rep x y u v : ℝ) : ℝ :=
  delta m M * ((u + c3 m M g / delta m M * (x ^ 2 - y ^ 2)) ^ 2 +
    (v + c3 m M g / delta m M * (2 * x * y)) ^ 2) +
      remainder m M g rep * (x ^ 2 + y ^ 2) ^ 2

theorem exact_square_completion (m M g rep x y u v : ℝ) (hd : delta m M ≠ 0) :
    density m M g rep x y u v = completedDensity m M g rep x y u v := by
  unfold density completedDensity remainder
  field_simp [hd]
  ring

theorem density_nonnegative (m M g rep x y u v : ℝ) (hm : 0 < m)
    (hM : 2 * m < M) (hrep : 0 ≤ rep) : 0 ≤ density m M g rep x y u v := by
  have hd : 0 < delta m M := by unfold delta; linarith
  rw [exact_square_completion m M g rep x y u v hd.ne']
  have hr := remainder_nonnegative m M g rep hm hM hrep
  unfold completedDensity
  positivity

/-- Finite weighted coordinate energy; all regulator weights are explicitly nonnegative. -/
theorem finite_energy_bounds {ι : Type*} (s : Finset ι) (m M g rep T : ℝ)
    (x y u v weights : ι → ℝ) (hm : 0 < m) (hM : 2 * m < M) (hrep : 0 ≤ rep)
    (hT : 0 ≤ T) (hw : ∀ i ∈ s, 0 ≤ weights i) :
    0 ≤ T ∧ T ≤ T + ∑ i ∈ s, weights i * density m M g rep (x i) (y i) (u i) (v i) := by
  refine ⟨hT, ?_⟩
  have hsum : 0 ≤ ∑ i ∈ s, weights i * density m M g rep (x i) (y i) (u i) (v i) := by
    apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hw i hi) (density_nonnegative m M g rep (x i) (y i) (u i) (v i) hm hM hrep)
  linarith

/-- One real component of the source gradient energy; arbitrary finite components
 can represent real/imaginary gradients along each spatial direction. -/
def gradientTerm (m M a b : ℝ) : ℝ := a ^ 2 / (2 * m) + b ^ 2 / (2 * M)

theorem gradient_nonnegative (m M a b : ℝ) (hm : 0 < m) (hM : 0 < M) :
    0 ≤ gradientTerm m M a b := by unfold gradientTerm; positivity

theorem finite_gradient_energy_nonnegative {ι : Type*} (s : Finset ι) (m M : ℝ)
    (a b weights : ι → ℝ) (hm : 0 < m) (hM : 0 < M)
    (hw : ∀ i ∈ s, 0 ≤ weights i) :
    0 ≤ ∑ i ∈ s, weights i * gradientTerm m M (a i) (b i) := by
  apply Finset.sum_nonneg
  intro i hi
  exact mul_nonneg (hw i hi) (gradient_nonnegative m M (a i) (b i) hm hM)

end FrameworkNREnergy
#print axioms FrameworkNREnergy.c3_squared
#print axioms FrameworkNREnergy.coefficient_identity
#print axioms FrameworkNREnergy.remainder_nonnegative
#print axioms FrameworkNREnergy.remainder_strict
#print axioms FrameworkNREnergy.exact_square_completion
#print axioms FrameworkNREnergy.density_nonnegative
#print axioms FrameworkNREnergy.finite_energy_bounds

#print axioms FrameworkNREnergy.gradient_nonnegative
#print axioms FrameworkNREnergy.finite_gradient_energy_nonnegative

/- EXPECTED FAILURE: deleting the interaction cross term changes actual NR energy. -/
example : FrameworkNREnergy.density 1 8 8 0 1 0 1 0 =
    FrameworkNREnergy.delta 1 8 + FrameworkNREnergy.quartic 1 8 8 0 := by
  norm_num [FrameworkNREnergy.density, FrameworkNREnergy.quartic,
    FrameworkNREnergy.c3, FrameworkNREnergy.delta]
