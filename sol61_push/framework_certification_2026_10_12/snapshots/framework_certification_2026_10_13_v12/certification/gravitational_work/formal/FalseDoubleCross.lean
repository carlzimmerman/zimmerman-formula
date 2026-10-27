import Mathlib

/-! Existing live reciprocal Newtonian A7 pair scope. Positions/velocities lie
in any real inner-product space (3D Euclidean space included). Fixed mass and
noncollision hypotheses are explicit. Actual potential/kinetic derivatives are
proved; no energy-balance axiom, DE receiver, metric or PDE existence assumed. -/
noncomputable section
namespace FrameworkGravitationalWork
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

def pairPotential (γ : ℝ) (x y : E) : ℝ := -γ / ‖x - y‖
def pairForce (γ : ℝ) (x y : E) : E := (-γ / ‖x - y‖ ^ 3) • (x - y)
def kinetic (m : ℝ) (v : E) : ℝ := m / 2 * ‖v‖ ^ 2

theorem reciprocal_force (γ : ℝ) (x y : E) : pairForce γ y x = -pairForce γ x y := by
  unfold pairForce
  rw [norm_sub_rev y x]
  have hsep : y - x = -(x - y) := by abel
  rw [hsep, smul_neg]

omit [InnerProductSpace ℝ E] in
theorem potential_symmetric (γ : ℝ) (x y : E) : pairPotential γ y x = pairPotential γ x y := by
  unfold pairPotential
  rw [norm_sub_rev y x]

/-- Derivative of the ACTUAL Newtonian separation potential along moving paths. -/
theorem pair_potential_derivative (γ t : ℝ) (x y : ℝ → E) (vx vy : E)
    (hx : HasDerivAt x vx t) (hy : HasDerivAt y vy t) (hne : x t ≠ y t) :
    HasDerivAt (fun s => pairPotential γ (x s) (y s))
      (-inner ℝ (pairForce γ (x t) (y t)) (vx - vy)) t := by
  have hR : ‖x t - y t‖ ≠ 0 := norm_ne_zero_iff.mpr (sub_ne_zero.mpr hne)
  have hn := ((hx.sub hy).norm_sq).sqrt (pow_ne_zero 2 hR)
  have hf : (fun s : ℝ => Real.sqrt (‖x s - y s‖ ^ 2)) =
      (fun s => ‖x s - y s‖) := by
    funext s
    exact Real.sqrt_sq (norm_nonneg _)
  simp only [Pi.sub_apply] at hn
  rw [hf] at hn
  have hnorm : HasDerivAt (fun s => ‖x s - y s‖)
      (inner ℝ (x t - y t) (vx - vy) / ‖x t - y t‖) t := by
    apply hn.congr_deriv
    rw [Real.sqrt_sq (norm_nonneg _)]
    field_simp
  have hp := (hasDerivAt_const t (-γ)).div hnorm hR
  apply hp.congr_deriv
  unfold pairForce
  rw [real_inner_smul_left]
  field_simp
  ring

/-- Potential force is identified by its actual directional derivatives, not set by energy balance. -/
theorem force_directional_action (γ : ℝ) (x y vx vy : E) (hne : x ≠ y) :
    HasDerivAt (fun s : ℝ => -pairPotential γ (x + s • vx) (y + s • vy))
      (inner ℝ (pairForce γ x y) vx + inner ℝ (pairForce γ y x) vy) 0 := by
  have hx : HasDerivAt (fun s : ℝ => x + s • vx) vx 0 := by
    simpa using ((hasDerivAt_id (0 : ℝ)).smul_const vx).const_add x
  have hy : HasDerivAt (fun s : ℝ => y + s • vy) vy 0 := by
    simpa using ((hasDerivAt_id (0 : ℝ)).smul_const vy).const_add y
  have h := (pair_potential_derivative γ 0 _ _ vx vy hx hy (by simpa using hne)).neg
  apply h.congr_deriv
  simp only [zero_smul, add_zero, inner_sub_right]
  rw [reciprocal_force γ x y, inner_neg_left]
  ring

/-- Actual kinetic derivative under fixed mass and its supplied Newton force equation. -/
theorem kinetic_force_power (m t : ℝ) (v : ℝ → E) (acc force : E)
    (hv : HasDerivAt v acc t) (hNewton : m • acc = force) :
    HasDerivAt (fun s => kinetic m (v s)) (inner ℝ force (v t)) t := by
  have hk := (hv.norm_sq).const_mul (m / 2)
  apply hk.congr_deriv
  rw [← hNewton, real_inner_smul_left, real_inner_comm acc (v t)]
  ring

/-- Live two-body energy derivative vanishes by derived force/kinetic/potential work. -/
theorem live_pair_energy (γ mc mb t : ℝ) (x y vx vy : ℝ → E) (ac ab : E)
    (hx : HasDerivAt x (vx t) t) (hy : HasDerivAt y (vy t) t)
    (hvc : HasDerivAt vx ac t) (hvb : HasDerivAt vy ab t) (hne : x t ≠ y t)
    (hc : mc • ac = pairForce γ (x t) (y t))
    (hb : mb • ab = pairForce γ (y t) (x t)) :
    HasDerivAt (fun s => kinetic mc (vx s) + kinetic mb (vy s) + pairPotential γ (x s) (y s)) 0 t := by
  have hkc := kinetic_force_power mc t vx ac _ hvc hc
  have hkb := kinetic_force_power mb t vy ab _ hvb hb
  have hw := pair_potential_derivative γ t x y (vx t) (vy t) hx hy hne
  apply ((hkc.add hkb).add hw).congr_deriv
  rw [reciprocal_force γ (x t) (y t), inner_neg_left, inner_sub_right]
  ring

/-- Allocate the single cross interaction wholly to cold: its live baryon work remains explicit. -/
theorem cold_cross_ledger (γ mc t : ℝ) (x y vx : ℝ → E) (vy ac : E)
    (hx : HasDerivAt x (vx t) t) (hy : HasDerivAt y vy t)
    (hvc : HasDerivAt vx ac t) (hne : x t ≠ y t)
    (hc : mc • ac = pairForce γ (x t) (y t)) :
    HasDerivAt (fun s => kinetic mc (vx s) + pairPotential γ (x s) (y s))
      (inner ℝ (pairForce γ (x t) (y t)) vy) t := by
  have hkc := kinetic_force_power mc t vx ac _ hvc hc
  have hw := pair_potential_derivative γ t x y (vx t) vy hx hy hne
  apply (hkc.add hw).congr_deriv
  rw [inner_sub_right]
  ring

omit [InnerProductSpace ℝ E] in
/-- The double ordered cross expression with 1/2 equals the once-counted rectangular cross sum. -/
theorem finite_cross_counted_once {ι κ : Type*} (cold : Finset ι) (baryon : Finset κ)
    (γ : ι → κ → ℝ) (x : ι → E) (y : κ → E) :
    ((∑ i ∈ cold, ∑ j ∈ baryon, pairPotential (γ i j) (x i) (y j)) +
      (∑ j ∈ baryon, ∑ i ∈ cold, pairPotential (γ i j) (y j) (x i))) / 2 =
        ∑ i ∈ cold, ∑ j ∈ baryon, pairPotential (γ i j) (x i) (y j) := by
  simp_rw [potential_symmetric]
  have hswap : (∑ j ∈ baryon, ∑ i ∈ cold, pairPotential (γ i j) (x i) (y j)) =
      ∑ i ∈ cold, ∑ j ∈ baryon, pairPotential (γ i j) (x i) (y j) := Finset.sum_comm
  rw [hswap]
  ring

/-- Actual derivative of any finite cross energy, with all pair noncollisions explicit. -/
theorem finite_cross_derivative {ι κ : Type*} (cold : Finset ι) (baryon : Finset κ)
    (γ : ι → κ → ℝ) (x : ι → ℝ → E) (y : κ → ℝ → E) (vx : ι → E) (vy : κ → E)
    (t : ℝ) (hx : ∀ i ∈ cold, HasDerivAt (x i) (vx i) t)
    (hy : ∀ j ∈ baryon, HasDerivAt (y j) (vy j) t)
    (hne : ∀ i ∈ cold, ∀ j ∈ baryon, x i t ≠ y j t) :
    HasDerivAt (fun s => ∑ i ∈ cold, ∑ j ∈ baryon, pairPotential (γ i j) (x i s) (y j s))
      (∑ i ∈ cold, ∑ j ∈ baryon, -inner ℝ (pairForce (γ i j) (x i t) (y j t)) (vx i - vy j)) t := by
  apply HasDerivAt.fun_sum
  intro i hi
  apply HasDerivAt.fun_sum
  intro j hj
  exact pair_potential_derivative (γ i j) t (x i) (y j) (vx i) (vy j) (hx i hi) (hy j hj) (hne i hi j hj)

end FrameworkGravitationalWork
#print axioms FrameworkGravitationalWork.reciprocal_force
#print axioms FrameworkGravitationalWork.potential_symmetric
#print axioms FrameworkGravitationalWork.pair_potential_derivative
#print axioms FrameworkGravitationalWork.force_directional_action
#print axioms FrameworkGravitationalWork.kinetic_force_power
#print axioms FrameworkGravitationalWork.live_pair_energy
#print axioms FrameworkGravitationalWork.cold_cross_ledger
#print axioms FrameworkGravitationalWork.finite_cross_counted_once
#print axioms FrameworkGravitationalWork.finite_cross_derivative

/- EXPECTED FAILURE: twice-counted W contributes a nonzero residual in actual force power. -/
example : inner ℝ (FrameworkGravitationalWork.pairForce 1 (1 : ℝ) 0) 1 +
    inner ℝ (FrameworkGravitationalWork.pairForce 1 (0 : ℝ) 1) 0 -
      2 * inner ℝ (FrameworkGravitationalWork.pairForce 1 (1 : ℝ) 0) (1 - 0) = 0 := by
  norm_num [FrameworkGravitationalWork.pairForce, inner, smul_eq_mul, Real.norm_eq_abs]
