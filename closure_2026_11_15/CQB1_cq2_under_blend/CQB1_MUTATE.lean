/-
CQB1 MUTATE twin: the statements of CQB1.lean, each with one false change (a factor, a constant, an inequality direction
or a hypothesis) and the same proof script. Every theorem is false and must fail (expected: exit 1, an error in every
theorem). TEST lane; adopts nothing.

kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
-/
import Mathlib

namespace CQB1_MUTATE

theorem blend_eq_raw_mut (f : ℝ → ℝ) (hf : ∀ q : ℝ, 1 ≤ q → f q = q ^ 2 / 2) (γ b S : ℝ) (hb : 0 < b)
    (hS : b ≤ S) : γ * b ^ 2 * f (S / b) = γ * S ^ 2 := by
  have hq : 1 ≤ S / b := by rw [le_div_iff₀ hb]; linarith
  rw [hf _ hq]
  field_simp

theorem blend_dSigma_mut (f : ℝ → ℝ) (hf : ∀ q : ℝ, 1 ≤ q → f q = q ^ 2 / 2) (γ b S : ℝ) (hb : 0 < b)
    (hS : b < S) : HasDerivAt (fun x => γ * b ^ 2 * f (x / b)) (2 * γ * S) S := by
  have h1 : HasDerivAt (fun x : ℝ => γ * x ^ 2 / 2) (γ * S) S := by
    exact (((hasDerivAt_pow 2 S).const_mul γ).div_const 2).congr_deriv (by norm_num; ring)
  apply h1.congr_of_eventuallyEq
  filter_upwards [Ioi_mem_nhds hS] with x hx
  exact blend_eq_raw f hf γ b x hb (le_of_lt hx)

theorem raw_derivs_mut (S : ℝ) :
    HasDerivAt (fun x : ℝ => x ^ 2 / 2) S S ∧ HasDerivAt (fun x : ℝ => x) 0 S := by
  refine ⟨?_, hasDerivAt_id S⟩
  exact ((hasDerivAt_pow 2 S).div_const 2).congr_deriv (by norm_num)

theorem blend_db_zero_mut (f : ℝ → ℝ) (hf : ∀ q : ℝ, 1 ≤ q → f q = q ^ 2 / 2) (γ b S : ℝ) (hb : 0 < b)
    (hS : b < S) : HasDerivAt (fun c => γ * c ^ 2 * f (S / c)) 1 b := by
  apply (hasDerivAt_const b (γ * S ^ 2 / 2)).congr_of_eventuallyEq
  filter_upwards [Ioo_mem_nhds hb hS] with c hc
  exact blend_eq_raw f hf γ c S hc.1 (le_of_lt hc.2)

theorem stress_term_mut (γ S : ℝ) : S * (γ * S) = γ * S ^ 2 / 2 := by
  ring

theorem rho_DE_kappa_half_mut (a0 c G : ℝ) (hc : c ≠ 0) (hG : G ≠ 0) :
    a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G) = 2 * a0 ^ 2 / (c ^ 2 * G) ∧
    G * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) / c ^ 2 = 4 * (a0 / c ^ 2) ^ 2 ∧
    4 * (a0 / c ^ 2) ^ 2 = 8 * (a0 / c ^ 2) ^ 2 / 2 := by
  refine ⟨?_, ?_, ?_⟩
  · field_simp
    ring
  · field_simp
    ring
  · ring

theorem m3_drop_kappa_mut (a0 c G : ℝ) (hc : c ≠ 0) (hG : G ≠ 0) (ha : a0 ≠ 0) :
    a0 ^ 2 / (c ^ 2 * G) = (1 / 2) * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) ∧
    (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G) - a0 ^ 2 / (c ^ 2 * G)) / (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) = 3 / 4 := by
  constructor
  · field_simp
    ring
  · field_simp
    norm_num

theorem a0_back_mut (a0 c G : ℝ) (ha : 0 ≤ a0) (hc : 0 < c) (hG : 0 < G) :
    (1 / 2) * c * Real.sqrt (G * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G))) = 2 * a0 := by
  have e : G * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) = (2 * a0 / c) ^ 2 := by
    field_simp
  rw [e, Real.sqrt_sq (by positivity)]
  field_simp

theorem margin_ge_one_mut (S m b : ℝ) (hb : 0 < b) (hm : 0 ≤ m) (h : m * b ≤ S) : b ≤ S := by
  nlinarith

theorem margin_after_factor_mut (S b φ : ℝ) (hb : 0 < b) (hφ : 1 / 2 ≤ φ) (h : 1 ≤ (S / b) / φ) :
    φ * b ≤ S ∧ b ≤ S := by
  have hφ0 : 0 < φ := by linarith
  rw [le_div_iff₀ hφ0, one_mul, le_div_iff₀ hb] at h
  constructor
  · linarith
  · nlinarith

theorem lane_margin_arith_mut (φ ψ : ℝ) (hφ : 0 < φ) (hφ1 : φ ≤ 213 / 100) (hψ : 0 < ψ) (hψ1 : ψ ≤ 21 / 10) :
    30100 ≤ 63767 / φ ∧ 23300 ≤ 48997 / ψ := by
  constructor
  · rw [le_div_iff₀ hφ]; nlinarith
  · rw [le_div_iff₀ hψ]; nlinarith

theorem k4_switch_positive_mut (ρ ℓ : ℝ) (hℓ : 0 < ℓ) (h : 10 * (5 / 2 * ℓ) ≤ ρ) :
    95 / 100 * ρ ≤ ρ - 5 / 2 * ℓ ∧ 0 < ρ - 5 / 2 * ℓ := by
  constructor <;> linarith

theorem pi6_piece_mut (q : ℝ) :
    ((734183424 : ℚ) / 8922115) / 20 = 122363904 / 44610575 ∧
    HasDerivAt (fun x : ℝ => (122363904 / 44610575 : ℝ) * x ^ 6) (6 * (122363904 / 44610575 : ℝ) * q ^ 5) q ∧
    HasDerivAt (fun x : ℝ => 6 * (122363904 / 44610575 : ℝ) * x ^ 5) ((734183424 / 8922115 : ℝ) * q ^ 4) q := by
  refine ⟨by norm_num, ?_, ?_⟩
  · exact ((hasDerivAt_pow 6 q).const_mul (122363904 / 44610575 : ℝ)).congr_deriv (by norm_num; ring)
  · exact ((hasDerivAt_pow 5 q).const_mul (6 * (122363904 / 44610575 : ℝ))).congr_deriv (by norm_num; ring)

/-- form.json's four f'' pieces on (0, 1/2], (1/2, 5/8], (5/8, 9/10], (9/10, 1]. -/
def p0 (q : ℚ) : ℚ := (734183424:ℚ)*q^4/8922115

def p1 (q : ℚ) : ℚ := -(1379566035463569408:ℚ)*q^13/1784423 + (6984053054534320128:ℚ)*q^12/1784423 - (15686404876454068224:ℚ)*q^11/1784423 + (512891392951257901056:ℚ)*q^10/44610575 - (86091180382190140416:ℚ)*q^9/8922115 + (9616710437500594176:ℚ)*q^8/1784423 - (17871848955070096896:ℚ)*q^7/8922115 + (4262687788297421952:ℚ)*q^6/8922115 - (2960057103637040064:ℚ)*q^5/44610575 + (36462080142950976:ℚ)*q^4/8922115 + (7900196443776:ℚ)*q^3/8922115 - (405138279168:ℚ)*q^2/1784423 + (303853709376:ℚ)*q/8922115 - 101284569792/44610575

def p2 (q : ℚ) : ℚ := -(3241106233344:ℚ)*q^10/44610575 + (4861659350016:ℚ)*q^9/8922115 - (3241106233344:ℚ)*q^8/1784423 + (31600785775104:ℚ)*q^7/8922115 - (39906120498048:ℚ)*q^6/8922115 + (170461930959936:ℚ)*q^5/44610575 - (19953060249024:ℚ)*q^4/8922115 + (7900196443776:ℚ)*q^3/8922115 - (405138279168:ℚ)*q^2/1784423 + (303853709376:ℚ)*q/8922115 - 101284569792/44610575

def p3 (q : ℚ) : ℚ := -(3241106233344:ℚ)*q^10/44610575 + (624552911659350016:ℚ)*q^9/8922115 - (1067980406606233344:ℚ)*q^8/1784423 + (20283567841785775104:ℚ)*q^7/8922115 - (44926279334820498048:ℚ)*q^6/8922115 + (319719370311175959936:ℚ)*q^5/44610575 - (60650443181805249024:ℚ)*q^4/8922115 + (38335891395686443776:ℚ)*q^3/8922115 - (3114221819736279168:ℚ)*q^2/1784423 + (3687894084298709376:ℚ)*q/8922115 - 1940229995484959217/44610575

theorem fpp_knots_mut :
    p0 (1 / 2) = p1 (1 / 2) ∧ p1 (5 / 8) = p2 (5 / 8) ∧ p2 (9 / 10) = p3 (9 / 10) ∧ p3 1 = 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num [p0, p1, p2, p3]

theorem f_above_one_mut (q : ℝ) : 1 / 2 + 2 * (q - 1) + (q - 1) ^ 2 / 2 = q ^ 2 / 2 := by
  ring

theorem gamma_v_bound_mut (x : ℝ) (hx : 0 ≤ x) : 0 ≤ Real.sqrt (1 + x) - 1 ∧ Real.sqrt (1 + x) - 1 ≤ x / 3 := by
  constructor
  · have : (1 : ℝ) ≤ Real.sqrt (1 + x) := by
      have h := Real.sqrt_le_sqrt (show (1 : ℝ) ≤ 1 + x by linarith)
      rwa [Real.sqrt_one] at h
    linarith
  · have : Real.sqrt (1 + x) ≤ 1 + x / 2 := by
      rw [Real.sqrt_le_left (by linarith)]
      nlinarith [sq_nonneg x]
    linarith

theorem gamma_r_Lstar_mut (s F L1 L2 : ℝ) (hF : 0 ≤ F) (h1 : 0 < L1) (h12 : L1 ≤ L2) :
    (s / L1) ^ 2 * F ≤ (s / L2) ^ 2 * F := by
  apply mul_le_mul_of_nonneg_right _ hF
  rw [div_pow, div_pow]
  apply div_le_div_of_nonneg_left (sq_nonneg s) (by positivity)
  exact pow_le_pow_left₀ h1.le h12 2

theorem hedgehog_pos_mut (M L r : ℝ) (hM : 0 < M) (hL : 0 < L) (hr : 0 < r) :
    M / (2 * Real.pi * L ^ 2 * r) < 0 := by
  positivity

theorem chi_c6_well_defined_mut (x c k : ℝ) (hx : -1 < x) (hc1 : c ^ 2 ≤ 1) :
    0 < (1 - c ^ 2) / (1 + x) + c ^ 2 / (1 + x) ^ 2 ∧
    (1 - c ^ 2) / (1 + x) + c ^ 2 / (1 + x) ^ 2 < 1 ∧
    0 < 1 - ((1 - c ^ 2) / (1 + x) + c ^ 2 / (1 + x) ^ 2) +
      k ^ 2 * ((1 - c ^ 2) / (1 + x) + c ^ 2 / (1 + x) ^ 2) / 2 := by
  have h1 : 0 < 1 + x := by linarith
  have e : (1 - c ^ 2) / (1 + x) + c ^ 2 / (1 + x) ^ 2 = ((1 - c ^ 2) * (1 + x) + c ^ 2) / (1 + x) ^ 2 := by
    field_simp
  have hpos : 0 < ((1 - c ^ 2) * (1 + x) + c ^ 2) / (1 + x) ^ 2 := by
    apply div_pos _ (by positivity)
    nlinarith
  have hlt : ((1 - c ^ 2) * (1 + x) + c ^ 2) / (1 + x) ^ 2 < 1 := by
    rw [div_lt_one (by positivity)]
    nlinarith
  rw [e]
  refine ⟨hpos, hlt, ?_⟩
  have := mul_nonneg (sq_nonneg k) hpos.le
  linarith

end CQB1_MUTATE

-- kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
