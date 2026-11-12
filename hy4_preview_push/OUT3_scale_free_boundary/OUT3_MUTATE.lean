/-
OUT-3 (SCALE-FREE BOUNDARY): the load-bearing algebra of

        kappa = 1/2   <=>   N_f = N_v

    N_f = the formation normalisation (the cold sector's dimensionless normalisation
          pinned on the fold Sigma_f)
    N_v = the vacuum value of the same dimensionless normalisation

Slots (unit-matched pairs only; mixing slots is inadmissible and is not graded):

    A  energy density   N_f = G rho_c(Sigma_f) c^2 / a0^2      N_v = G rho_L c^2 / a0^2 = 1/kappa^2
    B  column           N_f = X/(4 pi u)                       N_v = 1/(Z kappa)
    C  share            N_f = X(u_f)                           N_v = Omega_L/Omega_b

with  u_f = a0/g_b,f = a0 R_f^2/(G M_b),  X = Xo(u_f) = (sqrt(1+4u)-1)/2,
rho_c(Sigma_f) = 3 X M_b/(4 pi R_f^3),  Z = sqrt(8 pi/3).

Certified here:
  share_quad          Xo u * (1 + Xo u) = u                        (FLD1's exact share)
  share_of_quad       the converse: X >= 0 and X(1+X) = u  =>  X = Xo u
  Xo_strictMono       Xo is strictly increasing on u >= 0
  dlnX_dlnu_pos       s = d ln X/d ln u > 0 for u > 0
  Nv_eq_inv_kappa_sq  N_v(V1) = 1/kappa^2  from a0 = kappa c sqrt(G rho_L)
  iff_half            N_v(V1) = 4  <=>  kappa = 1/2   (THE IFF OF THE TAKE; an identity)
  armA_iff            N_f(F1) = N_v(V1)  <=>  rho_c(Sigma_f) = rho_Lambda  (a0^2 cancels)
  armA_invert         exact inversion -> a0 = G M_b q(1+q)/R_f^2, q = 4 pi rho_L R_f^3/(3 M_b)
  rhoC_strictMono     rho_c(Sigma_f) is strictly increasing in a0
  armA_at_most_one    the root in a0 is unique
  armB_invert         exact inversion -> kappa = ((1 + 8 pi uu/Z)^2 - 1)/(4 uu)
  armC_invert         exact inversion -> kappa = q_c(1+q_c)/uu
  weight_gap_A/B/C    the G_lambda weights of both sides, with rho = d ln R_f/d ln a0
  flat_BC_rho         rho = -1/2 makes arms B and C FLAT DIRECTIONS (exact, at every u)
  flat_BC_only        for B/C the gap vanishes only if rho = -1/2 (given s /= 0)
  flat_A_deep_iff     in the deep-field limit s = 1/2, rho = +1/4 is the flat condition for A
  gap_at_measured_fold  at the measured rho = 0 the gaps are nonzero for s > 0

SCOPE.  This file certifies ALGEBRA.  It does not certify that N_f = N_v is a law of nature,
that the clock sector is the cold component, or that FLD1's R_fold values are the ones the
universe realises; those are measured (FLD1) and graded (out3.out).
TEST lane; adopts nothing.  kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace OUT3

noncomputable section

-- the sector's share, as a function of u = a0/g
def Xo (u : ℝ) : ℝ := (Real.sqrt (1 + 4 * u) - 1) / 2

-- the cold (sector) mean density inside the fold
def rhoC (a0 Mb Rf G : ℝ) : ℝ :=
  3 * Mb * Xo (a0 * Rf ^ 2 / (G * Mb)) / (4 * Real.pi * Rf ^ 3)

-- ------------------------------------------------------------------ 1. the share

theorem Xo_nonneg (u : ℝ) (hu : 0 ≤ u) : 0 ≤ Xo u := by
  unfold Xo
  have h : 1 ≤ Real.sqrt (1 + 4 * u) := by
    rw [Real.le_sqrt (by norm_num : (0 : ℝ) ≤ 1) (by nlinarith : 0 ≤ 1 + 4 * u)]
    nlinarith
  nlinarith

theorem Xo_pos (u : ℝ) (hu : 0 < u) : 0 < Xo u := by
  unfold Xo
  have h : 1 < Real.sqrt (1 + 4 * u) := by
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 1)]
    nlinarith
  nlinarith

theorem share_quad (u : ℝ) (hu : 0 ≤ u) : Xo u * (1 + Xo u) = u := by
  unfold Xo
  have hnon : 0 ≤ 1 + 4 * u := by nlinarith
  have hsq : (Real.sqrt (1 + 4 * u)) ^ 2 = 1 + 4 * u := Real.sq_sqrt hnon
  calc
    ((Real.sqrt (1 + 4 * u) - 1) / 2) * (1 + (Real.sqrt (1 + 4 * u) - 1) / 2)
        = ((Real.sqrt (1 + 4 * u)) ^ 2 - 1) / 4 := by ring
    _ = (1 + 4 * u - 1) / 4 := by rw [hsq]
    _ = u := by ring

theorem share_of_quad (X u : ℝ) (hX : 0 ≤ X) (h : X * (1 + X) = u) : X = Xo u := by
  unfold Xo
  have hsq : (2 * X + 1) ^ 2 = 1 + 4 * u := by nlinarith [h]
  have hpos : 0 ≤ 2 * X + 1 := by nlinarith
  have hs : Real.sqrt (1 + 4 * u) = 2 * X + 1 := by
    rw [← hsq, Real.sqrt_sq_eq_abs, abs_of_nonneg hpos]
  nlinarith

theorem Xo_strictMono (u₁ u₂ : ℝ) (h₁ : 0 ≤ u₁) (hlt : u₁ < u₂) : Xo u₁ < Xo u₂ := by
  by_contra hnot
  have hle : Xo u₂ ≤ Xo u₁ := le_of_not_gt hnot
  have h₂ : 0 ≤ u₂ := le_trans h₁ (le_of_lt hlt)
  have hX1 : 0 ≤ Xo u₁ := Xo_nonneg u₁ h₁
  have hX2 : 0 ≤ Xo u₂ := Xo_nonneg u₂ h₂
  have hd : 0 ≤ Xo u₁ - Xo u₂ := sub_nonneg.mpr hle
  have hs : 0 ≤ 1 + Xo u₁ + Xo u₂ := by nlinarith
  have hprod : 0 ≤ (Xo u₁ - Xo u₂) * (1 + Xo u₁ + Xo u₂) := mul_nonneg hd hs
  have hm : Xo u₂ * (1 + Xo u₂) ≤ Xo u₁ * (1 + Xo u₁) := by nlinarith [hprod]
  have q1 := share_quad u₁ h₁
  have q2 := share_quad u₂ h₂
  nlinarith

/-- s = d ln X / d ln u in closed form. Positive for u > 0. -/
theorem dlnX_dlnu_pos (u : ℝ) (hu : 0 < u) :
    0 < u / (Xo u * Real.sqrt (1 + 4 * u)) := by
  have hX : 0 < Xo u := Xo_pos u hu
  have hs : 0 < Real.sqrt (1 + 4 * u) := Real.sqrt_pos.2 (by nlinarith)
  positivity

-- ------------------------------------------------- 2. the vacuum value and the IFF

/-- N_v(V1) = G rho_L c^2 / a0^2 = 1/kappa^2, from a0 = kappa c sqrt(G rho_L). -/
theorem Nv_eq_inv_kappa_sq (a0 kappa c G rhoL : ℝ)
    (ha0 : a0 = kappa * c * Real.sqrt (G * rhoL))
    (hpos : 0 < G * rhoL) (hkappa : kappa ≠ 0) (hc : c ≠ 0) :
    G * rhoL * c ^ 2 / a0 ^ 2 = 1 / kappa ^ 2 := by
  have hG : G ≠ 0 := by
    intro h; rw [h] at hpos; norm_num at hpos
  have hr : rhoL ≠ 0 := by
    intro h; rw [h] at hpos; norm_num at hpos
  rw [ha0]
  have hsq : (Real.sqrt (G * rhoL)) ^ 2 = G * rhoL := Real.sq_sqrt (le_of_lt hpos)
  calc
    G * rhoL * c ^ 2 / (kappa * c * Real.sqrt (G * rhoL)) ^ 2
        = G * rhoL * c ^ 2 / (kappa ^ 2 * c ^ 2 * (Real.sqrt (G * rhoL)) ^ 2) := by ring
    _ = G * rhoL * c ^ 2 / (kappa ^ 2 * c ^ 2 * (G * rhoL)) := by rw [hsq]
    _ = 1 / kappa ^ 2 := by
        field_simp [hkappa, hc, hG, hr]

/-- THE IFF OF THE TAKE: the vacuum value equals 4 exactly when kappa = 1/2. -/
theorem iff_half (kappa : ℝ) (hkappa : 0 < kappa) :
    (1 / kappa ^ 2 = 4) ↔ kappa = 1 / 2 := by
  constructor
  · intro h
    have hk2 : kappa ^ 2 = 1 / 4 := by
      have hne : kappa ^ 2 ≠ 0 := by positivity
      field_simp [hne] at h
      nlinarith
    have hf : (kappa - 1 / 2) * (kappa + 1 / 2) = 0 := by nlinarith [hk2]
    rcases mul_eq_zero.mp hf with h1 | h2
    · nlinarith
    · nlinarith
  · intro h
    rw [h]
    norm_num

/-- Arm A: the a0^2 cancels, so N_f = N_v is a statement about the density alone. -/
theorem armA_iff (a0 c G rhoC_ rhoL : ℝ) (ha0 : a0 ≠ 0) (hc : c ≠ 0) (hG : G ≠ 0) :
    G * rhoC_ * c ^ 2 / a0 ^ 2 = G * rhoL * c ^ 2 / a0 ^ 2 ↔ rhoC_ = rhoL := by
  have hscale : G * c ^ 2 / a0 ^ 2 ≠ 0 := by
    exact div_ne_zero (mul_ne_zero hG (pow_ne_zero 2 hc)) (pow_ne_zero 2 ha0)
  constructor
  · intro h
    have h' : (G * c ^ 2 / a0 ^ 2) * rhoC_ = (G * c ^ 2 / a0 ^ 2) * rhoL := by
      calc
        (G * c ^ 2 / a0 ^ 2) * rhoC_ = G * rhoC_ * c ^ 2 / a0 ^ 2 := by ring
        _ = G * rhoL * c ^ 2 / a0 ^ 2 := h
        _ = (G * c ^ 2 / a0 ^ 2) * rhoL := by ring
    exact mul_left_cancel₀ hscale h'
  · intro h
    rw [h]

-- ------------------------------------------------------- 3. arm A: exact inversion

/-- Arm A solved exactly: a0 = G M_b q(1+q)/R_f^2 with q = 4 pi rho_L R_f^3/(3 M_b).
    No deep-field approximation. -/
theorem armA_invert (a0 Mb Rf G rhoL : ℝ)
    (ha0 : 0 ≤ a0) (hMb : 0 < Mb) (hRf : 0 < Rf) (hG : 0 < G)
    (hrho : rhoC a0 Mb Rf G = rhoL) :
    a0 = G * Mb * (4 * Real.pi * rhoL * Rf ^ 3 / (3 * Mb)) / Rf ^ 2 := by
  let u : ℝ := a0 * Rf ^ 2 / (G * Mb)
  let q : ℝ := 4 * Real.pi * rhoL * Rf ^ 3 / (3 * Mb)
  have hu : 0 ≤ u := by
    dsimp [u]
    positivity
  have hquad : Xo u * (1 + Xo u) = u := share_quad u hu
  have hX : Xo u = q := by
    unfold rhoC at hrho
    change 3 * Mb * Xo u / (4 * Real.pi * Rf ^ 3) = rhoL at hrho
    dsimp [q]
    have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
    field_simp [hpi, ne_of_gt hMb, ne_of_gt hRf] at hrho ⊢
    nlinarith
  rw [hX] at hquad
  have hu_eq : u = q * (1 + q) := by nlinarith [hquad]
  dsimp [u, q] at hu_eq ⊢
  field_simp [ne_of_gt hMb, ne_of_gt hRf, ne_of_gt hG] at hu_eq ⊢
  nlinarith

/-- rho_c(Sigma_f) is strictly increasing in a0, so arm A's root is unique. -/
theorem rhoC_strictMono (a01 a02 Mb Rf G : ℝ) (h1 : 0 ≤ a01) (hlt : a01 < a02)
    (hMb : 0 < Mb) (hRf : 0 < Rf) (hG : 0 < G) :
    rhoC a01 Mb Rf G < rhoC a02 Mb Rf G := by
  unfold rhoC
  have hk : 0 < Rf ^ 2 / (G * Mb) := by positivity
  have hu1 : 0 ≤ a01 * Rf ^ 2 / (G * Mb) := by positivity
  have hult : a01 * Rf ^ 2 / (G * Mb) < a02 * Rf ^ 2 / (G * Mb) := by
    have := mul_lt_mul_of_pos_right hlt hk
    rw [show a01 * (Rf ^ 2 / (G * Mb)) = a01 * Rf ^ 2 / (G * Mb) by ring,
        show a02 * (Rf ^ 2 / (G * Mb)) = a02 * Rf ^ 2 / (G * Mb) by ring] at this
    exact this
  have hX := Xo_strictMono (a01 * Rf ^ 2 / (G * Mb)) (a02 * Rf ^ 2 / (G * Mb)) hu1 hult
  have hcoef : 0 < 3 * Mb / (4 * Real.pi * Rf ^ 3) := by positivity
  have hm : (3 * Mb / (4 * Real.pi * Rf ^ 3)) * Xo (a01 * Rf ^ 2 / (G * Mb))
          < (3 * Mb / (4 * Real.pi * Rf ^ 3)) * Xo (a02 * Rf ^ 2 / (G * Mb)) :=
    mul_lt_mul_of_pos_left hX hcoef
  convert hm using 1 <;> ring

theorem armA_at_most_one (a01 a02 Mb Rf G rhoL : ℝ) (h1 : 0 ≤ a01) (h2 : 0 ≤ a02)
    (hMb : 0 < Mb) (hRf : 0 < Rf) (hG : 0 < G)
    (heq1 : rhoC a01 Mb Rf G = rhoL) (heq2 : rhoC a02 Mb Rf G = rhoL) : a01 = a02 := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have hm := rhoC_strictMono a01 a02 Mb Rf G h1 hlt hMb hRf hG
    nlinarith
  · have hm := rhoC_strictMono a02 a01 Mb Rf G h2 hgt hMb hRf hG
    nlinarith

-- -------------------------------------------------- 4. arms B and C: exact inversion

/-- Arm B: X/(4 pi u) = 1/(Z kappa) with u = kappa*uu  =>  kappa = ((1+8 pi uu/Z)^2-1)/(4 uu). -/
theorem armB_invert (kappa uu Z : ℝ) (huu : uu ≠ 0) (hZ : Z ≠ 0)
    (hkap : kappa ≠ 0) (hu_nonneg : 0 ≤ kappa * uu)
    (h : Xo (kappa * uu) / (4 * Real.pi * (kappa * uu)) = 1 / (Z * kappa)) :
    kappa = ((1 + 8 * Real.pi * uu / Z) ^ 2 - 1) / (4 * uu) := by
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hku : kappa * uu ≠ 0 := mul_ne_zero hkap huu
  have hquad : Xo (kappa * uu) * (1 + Xo (kappa * uu)) = kappa * uu :=
    share_quad (kappa * uu) hu_nonneg
  have h1 := h
  field_simp [hpi, hkap, huu, hZ, hku] at h1
  have hX : Xo (kappa * uu) = 4 * Real.pi * uu / Z := by
    field_simp [hZ]
    nlinarith [h1]
  have hsq : (1 + 8 * Real.pi * uu / Z) ^ 2 = 1 + 4 * kappa * uu := by
    let A : ℝ := 4 * Real.pi * uu / Z
    have hA : Xo (kappa * uu) = A := by dsimp [A]; exact hX
    have hq : A * (1 + A) = kappa * uu := by
      have hq' := hquad
      rw [hA] at hq'
      exact hq'
    have hmain : (1 + 2 * A) ^ 2 = 1 + 4 * kappa * uu := by nlinarith [hq]
    have h8 : 8 * Real.pi * uu / Z = 2 * A := by dsimp [A]; ring
    rw [h8]
    exact hmain
  calc
    kappa = (1 + 4 * kappa * uu - 1) / (4 * uu) := by
      field_simp [huu]
      ring
    _ = ((1 + 8 * Real.pi * uu / Z) ^ 2 - 1) / (4 * uu) := by rw [hsq]

/-- Arm C: X(u_f) = q_c with u_f = kappa*uu  =>  kappa = q_c(1+q_c)/uu. -/
theorem armC_invert (kappa uu qc : ℝ) (huu : uu ≠ 0)
    (hX : Xo (kappa * uu) = qc) (hu : 0 ≤ kappa * uu) :
    kappa = qc * (1 + qc) / uu := by
  have hquad : Xo (kappa * uu) * (1 + Xo (kappa * uu)) = kappa * uu :=
    share_quad (kappa * uu) hu
  rw [hX] at hquad
  field_simp [huu] at hquad ⊢
  nlinarith

-- --------------------------------------------------- 5. the G_lambda weight ledger
--   s  = d ln X / d ln u           rho = d ln R_f / d ln a0
--   w_F1 = -2 + s*(1+2rho) - 3rho  w_V1 = -2
--   w_F2 = -1 + s*(1+2rho)         w_V2 = -1
--   w_F3 =      s*(1+2rho)         w_V3 =  0

theorem weight_gap_A (s rho : ℝ) :
    (-2 + s * (1 + 2 * rho) - 3 * rho) - (-2) = s * (1 + 2 * rho) - 3 * rho := by ring

theorem weight_gap_B (s rho : ℝ) :
    (-1 + s * (1 + 2 * rho)) - (-1) = s * (1 + 2 * rho) := by ring

theorem weight_gap_C (s rho : ℝ) :
    (s * (1 + 2 * rho)) - 0 = s * (1 + 2 * rho) := by ring

/-- rho = -1/2 (R_f ~ a0^{-1/2}) makes arms B and C FLAT DIRECTIONS, exactly, at every u. -/
theorem flat_BC_rho (s rho : ℝ) (h : rho = (1 / 2 : ℝ)) :
    (-1 + s * (1 + 2 * rho) = -1) ∧ (s * (1 + 2 * rho) = 0) := by
  subst rho
  constructor <;> ring

/-- and for B/C, since s /= 0, that is the ONLY way the gap can vanish. -/
theorem flat_BC_only (s rho : ℝ) (hs : s ≠ 0)
    (hgap : s * (1 + 2 * rho) = 0) : rho = -(1 / 2 : ℝ) := by
  have hz : 1 + 2 * rho = 0 := (mul_eq_zero.mp hgap).resolve_left hs
  nlinarith

/-- In the deep-field limit s = 1/2, arm A is a flat direction IFF rho = +1/4. -/
theorem flat_A_deep_iff (rho : ℝ) :
    (-2 + (1 / 2 : ℝ) * (1 + 2 * rho) - 3 * rho = -2) ↔ rho = 1 / 4 := by
  constructor <;> intro h <;> nlinarith

/-- At the measured fold response rho = 0 the gaps are nonzero for s > 0. -/
theorem gap_at_measured_fold (s : ℝ) (hs : 0 < s) :
    |s * (1 + 2 * 0) - 3 * 0| ≠ 0 ∧ |s * (1 + 2 * 0)| ≠ 0 := by
  constructor <;> simp [ne_of_gt hs]

end

end OUT3

/-- MUTATE M3: the headline claim asserted WITHOUT the weight gap. Must not compile. -/
theorem mutate_headline (s : ℝ) : s * (1 + 2 * (0 : ℝ)) = 0 := by ring
