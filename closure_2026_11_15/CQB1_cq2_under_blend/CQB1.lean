/-
CQB1: Lean statements for the algebra of lane CQB1_cq2_under_blend (closure_2026_11_15/CQB1_cq2_under_blend: cqb1.py,
FROZEN_CRITERIA.md, RESULT.md) and of the CQ2 seal it relies on (cq_lanes_2026_11_04/CQ2_v3s_dr4_seal: cq2.py,
SEALED_PREDICTION.md; that folder is not touched). They certify the algebra, not the physics, and no number or label of
either lane. The two arithmetic statements on the lane's printed margins only check the division the label gate does.
TEST lane; adopts nothing.

  blend_eq_raw          : with f(q) = q^2/2 for q >= 1 (S1) and b > 0, the blend gamma b^2 f(Sigma/b) equals the raw
                          stiffness gamma Sigma^2/2 wherever Sigma >= b.
  blend_dSigma          : on the open set Sigma > b the blend's Sigma-derivative is gamma Sigma (F' = Sigma).
  raw_derivs            : F = Sigma^2/2 has F' = Sigma and F'' = 1.
  blend_db_zero         : on Sigma > b > 0 the blend does not depend on b there (dF/db = 0).
  stress_term           : Sigma F' = 2 F for F = gamma Sigma^2/2, F' = gamma Sigma (QX17D's R2 stress term equals 2F).
  rho_DE_kappa_half     : rho_DE = a0^2 / (kappa^2 c^2 G) at kappa = 1/2 is 4 a0^2 / (c^2 G); G rho_DE / c^2 =
                          4 (a0/c^2)^2 = (8 (a0/c^2)^2) / 2, QX19's b = s2v/2 with s2v = 8 ag^2 (U1, U2).
  m3_drop_kappa         : without the 1/kappa^2 (mutation M3) b is one quarter of rho_DE's, relative difference 3/4.
  a0_back               : a0 = kappa c sqrt(G rho_DE) recovers a0 from rho_DE (a0 >= 0, c > 0, G > 0).
  margin_ge_one         : Sigma >= m b with m >= 1, b > 0 gives Sigma >= b.
  margin_after_factor   : (Sigma/b)/phi >= 1 with phi >= 1, b > 0 gives Sigma >= phi b >= b (the U4 label gate).
  lane_margin_arith     : the division the gate does on the printed minima: 63767/phi >= 29900 for 0 < phi <= 213/100,
                          48997/phi >= 23300 for 0 < phi <= 21/10.
  k4_switch_positive    : a positive lobe and rho_gal >= 10 x (5/2) lobe give rho_gal - (5/2) lobe >= (9/10) rho_gal > 0
                          (CQ2's K4 line 10; R1's Sigma = rho_gal,min - 2.5 lobe).
  pi6_piece             : on (0, 1/2] f = A6 q^6 with A6 = A/30 = 122363904/44610575 (A = 734183424/8922115 from
                          form.json): f' = 6 A6 q^5, f'' = 30 A6 q^4 = A q^4.
  fpp_knots             : form.json's f'' pieces agree at the knots 1/2, 5/8, 9/10, and the last piece is 1 at q = 1.
  f_above_one           : f(1) = 1/2, f'(1) = 1, f'' = 1 above 1 give f = q^2/2 for q >= 1 (Taylor identity).
  gamma_v_bound         : gamma_v = sqrt(gamma_r): 0 <= sqrt(1 + x) - 1 <= x/2 for x >= 0.
  gamma_r_Lstar         : gamma_r - 1 = (s/L*)^2 F with F >= 0 does not increase when L* increases.
  hedgehog_pos          : the hedgehog divergence M / (2 pi L*^2 r) is positive (S3).
  chi_c6_well_defined   : CQ2's Route F kernel: m = (1 - c^2)/(1 + x) + c^2/(1 + x)^2 lies in (0, 1) for x > 0,
                          0 <= c^2 <= 1, so 1 - m + k^2 m / 2 > 0.

kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
-/
import Mathlib

namespace CQB1

theorem blend_eq_raw (f : ℝ → ℝ) (hf : ∀ q : ℝ, 1 ≤ q → f q = q ^ 2 / 2) (γ b S : ℝ) (hb : 0 < b)
    (hS : b ≤ S) : γ * b ^ 2 * f (S / b) = γ * S ^ 2 / 2 := by
  have hq : 1 ≤ S / b := by rw [le_div_iff₀ hb]; linarith
  rw [hf _ hq]
  field_simp

theorem blend_dSigma (f : ℝ → ℝ) (hf : ∀ q : ℝ, 1 ≤ q → f q = q ^ 2 / 2) (γ b S : ℝ) (hb : 0 < b)
    (hS : b < S) : HasDerivAt (fun x => γ * b ^ 2 * f (x / b)) (γ * S) S := by
  have h1 : HasDerivAt (fun x : ℝ => γ * x ^ 2 / 2) (γ * S) S := by
    exact (((hasDerivAt_pow 2 S).const_mul γ).div_const 2).congr_deriv (by norm_num; ring)
  apply h1.congr_of_eventuallyEq
  filter_upwards [Ioi_mem_nhds hS] with x hx
  exact blend_eq_raw f hf γ b x hb (le_of_lt hx)

theorem raw_derivs (S : ℝ) :
    HasDerivAt (fun x : ℝ => x ^ 2 / 2) S S ∧ HasDerivAt (fun x : ℝ => x) 1 S := by
  refine ⟨?_, hasDerivAt_id S⟩
  exact ((hasDerivAt_pow 2 S).div_const 2).congr_deriv (by norm_num)

theorem blend_db_zero (f : ℝ → ℝ) (hf : ∀ q : ℝ, 1 ≤ q → f q = q ^ 2 / 2) (γ b S : ℝ) (hb : 0 < b)
    (hS : b < S) : HasDerivAt (fun c => γ * c ^ 2 * f (S / c)) 0 b := by
  apply (hasDerivAt_const b (γ * S ^ 2 / 2)).congr_of_eventuallyEq
  filter_upwards [Ioo_mem_nhds hb hS] with c hc
  exact blend_eq_raw f hf γ c S hc.1 (le_of_lt hc.2)

theorem stress_term (γ S : ℝ) : S * (γ * S) = 2 * (γ * S ^ 2 / 2) := by
  ring

theorem rho_DE_kappa_half (a0 c G : ℝ) (hc : c ≠ 0) (hG : G ≠ 0) :
    a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G) = 4 * a0 ^ 2 / (c ^ 2 * G) ∧
    G * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) / c ^ 2 = 4 * (a0 / c ^ 2) ^ 2 ∧
    4 * (a0 / c ^ 2) ^ 2 = 8 * (a0 / c ^ 2) ^ 2 / 2 := by
  refine ⟨?_, ?_, ?_⟩
  · field_simp
    ring
  · field_simp
    ring
  · ring

theorem m3_drop_kappa (a0 c G : ℝ) (hc : c ≠ 0) (hG : G ≠ 0) (ha : a0 ≠ 0) :
    a0 ^ 2 / (c ^ 2 * G) = (1 / 4) * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) ∧
    (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G) - a0 ^ 2 / (c ^ 2 * G)) / (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) = 3 / 4 := by
  constructor
  · field_simp
    ring
  · field_simp
    norm_num

theorem a0_back (a0 c G : ℝ) (ha : 0 ≤ a0) (hc : 0 < c) (hG : 0 < G) :
    (1 / 2) * c * Real.sqrt (G * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G))) = a0 := by
  have e : G * (a0 ^ 2 / ((1 / 2) ^ 2 * c ^ 2 * G)) = (2 * a0 / c) ^ 2 := by
    field_simp
  rw [e, Real.sqrt_sq (by positivity)]
  field_simp

theorem margin_ge_one (S m b : ℝ) (hb : 0 < b) (hm : 1 ≤ m) (h : m * b ≤ S) : b ≤ S := by
  nlinarith

theorem margin_after_factor (S b φ : ℝ) (hb : 0 < b) (hφ : 1 ≤ φ) (h : 1 ≤ (S / b) / φ) :
    φ * b ≤ S ∧ b ≤ S := by
  have hφ0 : 0 < φ := by linarith
  rw [le_div_iff₀ hφ0, one_mul, le_div_iff₀ hb] at h
  constructor
  · linarith
  · nlinarith

theorem lane_margin_arith (φ ψ : ℝ) (hφ : 0 < φ) (hφ1 : φ ≤ 213 / 100) (hψ : 0 < ψ) (hψ1 : ψ ≤ 21 / 10) :
    29900 ≤ 63767 / φ ∧ 23300 ≤ 48997 / ψ := by
  constructor
  · rw [le_div_iff₀ hφ]; nlinarith
  · rw [le_div_iff₀ hψ]; nlinarith

theorem k4_switch_positive (ρ ℓ : ℝ) (hℓ : 0 < ℓ) (h : 10 * (5 / 2 * ℓ) ≤ ρ) :
    9 / 10 * ρ ≤ ρ - 5 / 2 * ℓ ∧ 0 < ρ - 5 / 2 * ℓ := by
  constructor <;> linarith

theorem pi6_piece (q : ℝ) :
    ((734183424 : ℚ) / 8922115) / 30 = 122363904 / 44610575 ∧
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

theorem fpp_knots :
    p0 (1 / 2) = p1 (1 / 2) ∧ p1 (5 / 8) = p2 (5 / 8) ∧ p2 (9 / 10) = p3 (9 / 10) ∧ p3 1 = 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num [p0, p1, p2, p3]

theorem f_above_one (q : ℝ) : 1 / 2 + 1 * (q - 1) + (q - 1) ^ 2 / 2 = q ^ 2 / 2 := by
  ring

theorem gamma_v_bound (x : ℝ) (hx : 0 ≤ x) : 0 ≤ Real.sqrt (1 + x) - 1 ∧ Real.sqrt (1 + x) - 1 ≤ x / 2 := by
  constructor
  · have : (1 : ℝ) ≤ Real.sqrt (1 + x) := by
      have h := Real.sqrt_le_sqrt (show (1 : ℝ) ≤ 1 + x by linarith)
      rwa [Real.sqrt_one] at h
    linarith
  · have : Real.sqrt (1 + x) ≤ 1 + x / 2 := by
      rw [Real.sqrt_le_left (by linarith)]
      nlinarith [sq_nonneg x]
    linarith

theorem gamma_r_Lstar (s F L1 L2 : ℝ) (hF : 0 ≤ F) (h1 : 0 < L1) (h12 : L1 ≤ L2) :
    (s / L2) ^ 2 * F ≤ (s / L1) ^ 2 * F := by
  apply mul_le_mul_of_nonneg_right _ hF
  rw [div_pow, div_pow]
  apply div_le_div_of_nonneg_left (sq_nonneg s) (by positivity)
  exact pow_le_pow_left₀ h1.le h12 2

theorem hedgehog_pos (M L r : ℝ) (hM : 0 < M) (hL : 0 < L) (hr : 0 < r) :
    0 < M / (2 * Real.pi * L ^ 2 * r) := by
  positivity

theorem chi_c6_well_defined (x c k : ℝ) (hx : 0 < x) (hc1 : c ^ 2 ≤ 1) :
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

end CQB1

-- kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing.
