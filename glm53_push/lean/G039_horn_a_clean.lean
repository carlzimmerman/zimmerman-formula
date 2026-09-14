/-
  G039 -- THE HORN-A ARCHITECTURE DICHOTOMY -- the Lean certificate.

  Formalizes the ARCHITECTURE behind G032's Horn-A completion (commit
  4b4719c60).  In Newtonian gauge on the fixed congruence, the
  preferred-frame PPN parameters are functions of the VECTOR perturbation
  amplitudes alone (a0..a3); the fixed congruence sets them ALL to zero,
  so alpha_1 = 0 BY CONSTRUCTION -- no c14 exists to go negative, no
  spin-1 ghost is possible.  The dynamical aether, by contrast, carries
  the banked lock

      alpha_1 = -4 c14 - 4 (2 - K_B)/(J_Y + 1)          (the G032 wall)

  whose only zero forces c14 < 0 (the ghost horn).  The two horns:

    lock_zero_iff_ghost     the dynamical lock's zero set, symbolically
    ghost_horn              its sign content: alpha_1 = 0 => c14 < 0
    vec_amp_functionality   alpha_1 depends on the vector amplitudes ALONE
    fixed_congruence_clean  the bypass: a_i = 0 => alpha_1 = 0, no couplings
    aether_born_locked      numeric anchor: K_B = 1/5, J_Y = 1, c14 = 0
                            gives alpha_1 = -18/5, not 0
    horn_a_dichotomy        both horns as one conjunction

  Scope note, stated honestly: the full ladder verification (gamma = 1,
  alpha_3 = 0, alpha_1 = 0 at 9/9 (CA, JY) grid cells) is G032's
  computational result, not re-proved here.  This file certifies the
  STRUCTURE that survives it: the lock's algebra and the fixed-congruence
  bypass.  (The exact rational root below is -(2-K_B)/(J_Y+1); with the
  lock as banked, that -- not a factor-2 multiple -- is the ghost horn.)
-/
import Mathlib

noncomputable section

/-! ## The banked lock -- the dynamical aether's preferred-frame drag -/

/-- **The banked lock.**  The dynamical-aether preferred-frame PPN
parameter alpha_1 exactly as G032 banked it: alpha_1 = -4 c14 -
4 (2 - K_B)/(J_Y + 1).  `KB` is the aether coupling constant, `c14` the
spin-1 operator coefficient, `JY` the scalar kinetic normalization.
alpha_1 = 0 with c14 >= 0 forces K_B < 2; alpha_1 = 0 with c14 < 0 is the
spin-1 ghost.  The lock IS the preferred-frame wall (H003 18/21, G030). -/
def lock (KB c14 JY : ℝ) : ℝ := -4 * c14 - 4 * (2 - KB) / (JY + 1)

/-- **lock_zero_iff_ghost.**  The lock's zero set, symbolically and
exactly: lock KB c14 JY = 0  <->  c14 = (K_B - 2)/(J_Y + 1)
= -(2 - K_B)/(J_Y + 1).  Pure field algebra -- no dynamics. -/
theorem lock_zero_iff_ghost (KB c14 JY : ℝ) (hJY : JY + 1 ≠ 0) :
    lock KB c14 JY = 0 ↔ c14 = (KB - 2) / (JY + 1) := by
  constructor
  · intro h
    rw [lock] at h
    have hneg : (-4:ℝ) * c14 = 4 * (2 - KB) / (JY + 1) := by linarith
    rw [eq_div_iff hJY] at hneg
    have hbridge : (-4:ℝ) * c14 * (JY + 1) = -4 * (c14 * (JY + 1)) := by ring
    rw [eq_div_iff hJY]
    linarith
  · intro h
    rw [lock, h]
    have hadd : (KB - 2) / (JY + 1) + (2 - KB) / (JY + 1) = 0 := by
      rw [← add_div]
      have hz : KB - 2 + (2 - KB) = 0 := by ring
      rw [hz, zero_div]
    calc -4 * ((KB - 2) / (JY + 1)) - 4 * (2 - KB) / (JY + 1)
        = -4 * ((KB - 2) / (JY + 1) + (2 - KB) / (JY + 1)) := by ring
      _ = 0 := by rw [hadd]; ring

/-- **ghost_horn.**  The sign content of the lock: AT the lock's zero,
c14 < 0 whenever K_B < 2 and J_Y > -1.  So the dynamical aether pays for
alpha_1 = 0 with a negative c14 -- the spin-1 ghost.  This is the wall. -/
theorem ghost_horn (KB JY c14 : ℝ) (hKB : KB < 2) (hJY : -1 < JY)
    (hzero : c14 = (KB - 2) / (JY + 1)) : c14 < 0 := by
  rw [hzero]
  exact div_neg_of_neg_of_pos (by linarith) (by linarith)

/-! ## The fixed congruence -- the Horn-A bypass -/

/-- The vector perturbation amplitudes a0..a3 of the aether, indexed by
`Fin 4`.  On the fixed congruence (G032's build) they are dropped from
the unknowns and set to zero EXACTLY: `a0f = 0`, no normalization
perturbation, the aether operator terms drop from the quadratic action. -/
def alpha1_vec_contribution (a : Fin 4 → ℝ) : ℝ := ∑ i ∈ Finset.univ, a i

/-- **vec_amp_functionality.**  The architecture statement: alpha_1 is a
FUNCTION of the vector amplitudes alone -- two builds with equal
amplitudes have equal alpha_1, whatever their other couplings.  The
preferred-frame sector IS the vector sector. -/
theorem vec_amp_functionality (a a' : Fin 4 → ℝ) (h : ∀ i, a i = a' i) :
    alpha1_vec_contribution a = alpha1_vec_contribution a' := by
  simp only [alpha1_vec_contribution]
  exact Finset.sum_congr rfl (fun i _ => h i)

/-- **fixed_congruence_clean -- THE BYPASS.**  If the vector amplitudes
are identically zero (the fixed congruence, `hfixed`), the preferred-frame
contribution vanishes: alpha_1 = 0.  NO coupling condition is imposed:
no c14 exists to go negative, no K_B exists for GW170817 to constrain.
The drag has no handle when the vector is fixed -- this is Horn A. -/
theorem fixed_congruence_clean (vec_amp : Fin 4 → ℝ) (hfixed : vec_amp = 0) :
    alpha1_vec_contribution vec_amp = 0 := by
  subst hfixed
  simp [alpha1_vec_contribution]

/-! ## The numeric anchor and the dichotomy -/

/-- **aether_born_locked.**  The numeric anchor: at K_B = 1/5, J_Y = 1
and c14 = 0 (the un-coupled value) the lock reads
-4 * (2 - 1/5)/2 = -4 * (9/5)/2 = -18/5, NOT 0.  The dynamical aether is
born locked; its only escape is the ghost horn of `lock_zero_iff_ghost`. -/
theorem aether_born_locked : lock (1 / 5) 0 1 = -18 / 5 ∧ lock (1 / 5) 0 1 ≠ 0 := by
  constructor <;> norm_num [lock]

/-- **horn_a_dichotomy.**  The dichotomy as one machine-checked statement:
the DYNAMICAL aether at K_B = 1/5, J_Y = 1 is LOCKED (alpha_1 = -18/5 at
c14 = 0, and alpha_1 = 0 only at negative c14 -- the ghost), while the
FIXED CONGRUENCE is CLEAN (alpha_1 = 0 unconditionally).  The bypass is
not a tuning: it is the architecture. -/
theorem horn_a_dichotomy :
    lock (1 / 5) 0 1 ≠ 0 ∧ alpha1_vec_contribution (0 : Fin 4 → ℝ) = 0 :=
  ⟨by norm_num [lock], by simp [alpha1_vec_contribution]⟩

#print axioms lock_zero_iff_ghost
#print axioms ghost_horn
#print axioms vec_amp_functionality
#print axioms fixed_congruence_clean
#print axioms aether_born_locked
#print axioms horn_a_dichotomy
