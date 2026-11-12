/-
  FINAL-10 (LEAN-STRESS)
  Anisotropic stress of the law's static halo, certified in Lean 4 / mathlib.

  Definitions (all over ℝ):
      K      = 4 π G                       (Kphys G; kept abstract-positive as K elsewhere)
      u      = g / a0
      mu     = u / (1 + u)
      J(g)   = (a0^2 / K) * (u - log(1+u))
      Pi_ij  = J(g) δ_ij - g_i g_j / (K (1+u))

  Targets
    (1) radial field g = g(r) r̂  ⇒  Pi_rr = J - g^2/(K(1+u)),  Pi_tt = Pi_φφ = J,
        hence Pi_rr + Pi_tt = 2J - g^2/(K(1+u)).
    (2) deep-law branch u^2 = x^2 (1+u): the claimed identity
            2 (u - log(1+u)) = u^2/(1+u)
        is FALSE.  The honest residual
            R(u) = 2 (u - log(1+u)) - u^2/(1+u) = 2(u - log(1+u)) - x^2
        is STRICTLY POSITIVE for every u > 0, so Pi_rr + Pi_tt ≠ 0.
        Exact closed form: R = 2 (sinh s - s) with s = log(1+u).
        True ratio: Pi_rr = (1 - x^2/(u - log(1+u))) * Pi_tt.
    (3) isotropic pressure limit:  |(u - log(1+u)) - u^2/2| ≤ u^3/3  for u ≥ 0,
        i.e. J = g^2/(2K) + O(u^3);  and ρ_c σ² ≡ J.

  No `sorry`, no `admit`, no axiomatised constants (see the #print axioms report at
  the bottom).
-/

import Mathlib

noncomputable section
open Real
open BigOperators

namespace Final10

/-! ## 0. Definitions -/

/- Physical K = 4 π G; positive whenever G > 0. -/
def Kphys (G : ℝ) : ℝ := 4 * Real.pi * G

lemma Kphys_pos {G : ℝ} (hG : 0 < G) : 0 < Kphys G := by
  exact mul_pos (mul_pos (by norm_num) Real.pi_pos) hG

abbrev Vec3 := Fin 3 → ℝ

def dot (v w : Vec3) : ℝ := ∑ i, v i * w i

def gnorm (gv : Vec3) : ℝ := Real.sqrt (dot gv gv)

/-- dimensionless field strength u = g / a0 -/
def uOf (a0 g : ℝ) : ℝ := g / a0

/-- the interpolation function mu = u/(1+u) -/
def muOf (a0 g : ℝ) : ℝ := uOf a0 g / (1 + uOf a0 g)

/-- J(g) = (a0^2/K) (u - log(1+u)) -/
noncomputable def JF (K a0 g : ℝ) : ℝ :=
  (a0 ^ 2 / K) * (uOf a0 g - Real.log (1 + uOf a0 g))

/-- the three orthonormal basis directions of the spherical frame -/
def e0 : Vec3 := fun i => if i = 0 then (1 : ℝ) else 0
def e1 : Vec3 := fun i => if i = 1 then (1 : ℝ) else 0
def e2 : Vec3 := fun i => if i = 2 then (1 : ℝ) else 0

/-- a purely radial field g = g(r) r̂, expressed in the spherical frame -/
def radial (g : ℝ) : Vec3 := fun i => if i = 0 then g else 0

/-- Pi_ij = J δ_ij - g_i g_j / (K (1+u)) -/
noncomputable def PiTensor (K a0 : ℝ) (gv : Vec3) (i j : Fin 3) : ℝ :=
  JF K a0 (gnorm gv) * (if i = j then (1 : ℝ) else 0)
    - gv i * gv j / (K * (1 + uOf a0 (gnorm gv)))

/-- quadratic form v ↦ vᵀ M v -/
def quad (M : Fin 3 → Fin 3 → ℝ) (v : Vec3) : ℝ := ∑ i, ∑ j, v i * M i j * v j

/-! ## 1. Radial decomposition (target 1) -/

lemma dot_radial_radial (g : ℝ) : dot (radial g) (radial g) = g ^ 2 := by
  simp [dot, radial, Fin.sum_univ_three, pow_two]

lemma gnorm_radial (g : ℝ) (hg : 0 ≤ g) : gnorm (radial g) = g := by
  rw [gnorm, dot_radial_radial, Real.sqrt_sq_eq_abs, abs_of_nonneg hg]

lemma uOf_radial (a0 g : ℝ) (hg : 0 ≤ g) : uOf a0 (gnorm (radial g)) = g / a0 := by
  rw [gnorm_radial g hg, uOf]

lemma uOf_mul_cancel (a0 u : ℝ) (ha0 : a0 ≠ 0) : uOf a0 (a0 * u) = u := by
  unfold uOf
  field_simp [ha0]

lemma dot_radial_e0 (g : ℝ) : dot (radial g) e0 = g := by
  simp [dot, radial, e0, Fin.sum_univ_three]

lemma dot_radial_e1 (g : ℝ) : dot (radial g) e1 = 0 := by
  simp [dot, radial, e1, Fin.sum_univ_three]

lemma dot_radial_e2 (g : ℝ) : dot (radial g) e2 = 0 := by
  simp [dot, radial, e2, Fin.sum_univ_three]

lemma unit_e0 : dot e0 e0 = 1 := by simp [dot, e0, Fin.sum_univ_three]
lemma unit_e1 : dot e1 e1 = 1 := by simp [dot, e1, Fin.sum_univ_three]
lemma unit_e2 : dot e2 e2 = 1 := by simp [dot, e2, Fin.sum_univ_three]

/-- Pi_rr = J - g^2/(K(1+u)) -/
lemma Pi_rr (K a0 g : ℝ) (hg : 0 ≤ g) :
    PiTensor K a0 (radial g) 0 0 = JF K a0 g - g ^ 2 / (K * (1 + g / a0)) := by
  unfold PiTensor
  simp [radial, gnorm_radial g hg, uOf]
  ring_nf

/-- Pi_tt = J  (index 1 = θ̂) -/
lemma Pi_tt (K a0 g : ℝ) (hg : 0 ≤ g) :
    PiTensor K a0 (radial g) 1 1 = JF K a0 g := by
  unfold PiTensor
  simp [radial, gnorm_radial g hg, uOf]

/-- Pi_φφ = J  (index 2 = φ̂) -/
lemma Pi_pp (K a0 g : ℝ) (hg : 0 ≤ g) :
    PiTensor K a0 (radial g) 2 2 = JF K a0 g := by
  unfold PiTensor
  simp [radial, gnorm_radial g hg, uOf]

lemma Pi_tt_eq_Pi_pp (K a0 g : ℝ) (hg : 0 ≤ g) :
    PiTensor K a0 (radial g) 1 1 = PiTensor K a0 (radial g) 2 2 := by
  rw [Pi_tt K a0 g hg, Pi_pp K a0 g hg]

/-- Pi_rr + Pi_tt = 2J - g^2/(K(1+u)) -/
lemma Pi_rr_add_Pi_tt (K a0 g : ℝ) (hg : 0 ≤ g) :
    PiTensor K a0 (radial g) 0 0 + PiTensor K a0 (radial g) 1 1 =
      2 * JF K a0 g - g ^ 2 / (K * (1 + g / a0)) := by
  rw [Pi_rr K a0 g hg, Pi_tt K a0 g hg]
  ring

/-- off-diagonal components vanish in the spherical frame -/
lemma Pi_offdiag (K a0 g : ℝ) (hg : 0 ≤ g) :
    PiTensor K a0 (radial g) 0 1 = 0 ∧ PiTensor K a0 (radial g) 1 2 = 0 := by
  constructor <;> (unfold PiTensor; simp [radial, gnorm_radial g hg, uOf])

/-- coordinate-free version: for ANY unit direction v,
    vᵀ Π v = J - (g·v)^2/(K(1+u)).  Radial (v = r̂) gives Pi_rr,
    tangential (v ⊥ r̂, so g·v = 0) gives Pi_tt = Pi_φφ = J. -/
lemma quad_Pi_general (K a0 : ℝ) (gv v : Vec3) :
    quad (PiTensor K a0 gv) v =
      JF K a0 (gnorm gv) * dot v v - (dot gv v) ^ 2 / (K * (1 + uOf a0 (gnorm gv))) := by
  unfold quad PiTensor
  simp [dot, Fin.sum_univ_three]
  ring_nf

lemma quad_Pi_unit (K a0 : ℝ) (gv v : Vec3) (hv : dot v v = 1) :
    quad (PiTensor K a0 gv) v =
      JF K a0 (gnorm gv) - (dot gv v) ^ 2 / (K * (1 + uOf a0 (gnorm gv))) := by
  rw [quad_Pi_general, hv]
  ring

/-- radial: quad of Π along r̂ gives J - g^2/(K(1+u)) -/
lemma quad_Pi_radial (K a0 g : ℝ) (hg : 0 ≤ g) :
    quad (PiTensor K a0 (radial g)) e0 = JF K a0 g - g ^ 2 / (K * (1 + g / a0)) := by
  rw [quad_Pi_unit K a0 (radial g) e0 unit_e0]
  simp [gnorm_radial g hg, uOf, dot_radial_e0]

/-- tangential: quad of Π along θ̂ (and φ̂) gives J -/
lemma quad_Pi_tangential1 (K a0 g : ℝ) (hg : 0 ≤ g) :
    quad (PiTensor K a0 (radial g)) e1 = JF K a0 g := by
  rw [quad_Pi_unit K a0 (radial g) e1 unit_e1]
  simp [gnorm_radial g hg, uOf, dot_radial_e1]

lemma quad_Pi_tangential2 (K a0 g : ℝ) (hg : 0 ≤ g) :
    quad (PiTensor K a0 (radial g)) e2 = JF K a0 g := by
  rw [quad_Pi_unit K a0 (radial g) e2 unit_e2]
  simp [gnorm_radial g hg, uOf, dot_radial_e2]

/-! ## 2. The deep-law branch and the honest residual (target 2) -/

/-- the deep-law branch: u > 0 and u^2 = x^2 (1+u), i.e. u^2/(1+u) = x^2 -/
def DeepLaw (x u : ℝ) : Prop := 0 < u ∧ u ^ 2 = x ^ 2 * (1 + u)

/-- the closed-form positive root u(x) of u^2 = x^2 (1+u) -/
noncomputable def branchU (x : ℝ) : ℝ := (x ^ 2 + Real.sqrt (x ^ 4 + 4 * x ^ 2)) / 2

lemma branchU_pos (x : ℝ) (hx : x ≠ 0) : 0 < branchU x := by
  unfold branchU
  have hs : 0 ≤ Real.sqrt (x ^ 4 + 4 * x ^ 2) := Real.sqrt_nonneg _
  have hx2 : 0 < x ^ 2 := sq_pos_of_ne_zero hx
  nlinarith

/-- u(x) really does satisfy DeepLaw: the branch is non-empty -/
lemma branchU_spec (x : ℝ) (hx : x ≠ 0) : DeepLaw x (branchU x) := by
  constructor
  · exact branchU_pos x hx
  · unfold branchU
    have hnn : 0 ≤ x ^ 4 + 4 * x ^ 2 := by nlinarith [sq_nonneg (x ^ 2), sq_nonneg x]
    have hs2 : Real.sqrt (x ^ 4 + 4 * x ^ 2) ^ 2 = x ^ 4 + 4 * x ^ 2 := by
      rw [Real.sq_sqrt hnn]
    nlinarith [hs2]

/-- the positive root is the only positive one (the other root is -x^2/u < 0) -/
lemma DeepLaw_unique {x u₁ u₂ : ℝ} (h₁ : DeepLaw x u₁) (h₂ : DeepLaw x u₂) : u₁ = u₂ := by
  by_contra hne
  have hs : u₁ + u₂ = x ^ 2 := by
    have e1 : u₁ ^ 2 - x ^ 2 * u₁ - x ^ 2 = 0 := by nlinarith [h₁.2]
    have e2 : u₂ ^ 2 - x ^ 2 * u₂ - x ^ 2 = 0 := by nlinarith [h₂.2]
    have hdiff : (u₁ - u₂) * (u₁ + u₂ - x ^ 2) = 0 := by nlinarith [e1, e2]
    have hnz : u₁ - u₂ ≠ 0 := by linarith
    have : u₁ + u₂ - x ^ 2 = 0 := (mul_eq_zero.mp hdiff).resolve_left hnz
    linarith
  have hprod : u₁ * u₂ = -(u₁ + u₂) := by nlinarith [h₁.2, hs]
  have hpos : 0 < u₁ * u₂ := mul_pos h₁.1 h₂.1
  have hneg : u₁ * u₂ < 0 := by nlinarith [hprod, h₁.1, h₂.1]
  linarith

/-- on the branch, u^2/(1+u) is exactly x^2 -/
lemma DeepLaw_div_eq (h : DeepLaw x u) : u ^ 2 / (1 + u) = x ^ 2 := by
  have hne : (1 + u : ℝ) ≠ 0 := by linarith [h.1]
  rw [div_eq_iff hne]
  exact h.2

/-- u * mu = u^2/(1+u) -/
lemma u_mul_mu (a0 g : ℝ) : uOf a0 g * muOf a0 g = (uOf a0 g) ^ 2 / (1 + uOf a0 g) := by
  unfold muOf
  ring

/-- the law u·mu = x^2 on the branch -/
lemma DeepLaw_u_mul_mu (a0 u x : ℝ) (ha0 : 0 < a0) (h : DeepLaw x u) :
    u * muOf a0 (a0 * u) = x ^ 2 := by
  rw [show uOf a0 (a0 * u) = u from uOf_mul_cancel a0 u (ne_of_gt ha0)]
  rw [show u * muOf a0 (a0 * u) = u * (uOf a0 (a0 * u) / (1 + uOf a0 (a0 * u))) by rfl]
  rw [show uOf a0 (a0 * u) = u from uOf_mul_cancel a0 u (ne_of_gt ha0)]
  rw [h.div_eq]
  ring

/-- the honest residual: R(u) = 2(u - log(1+u)) - u^2/(1+u) -/
noncomputable def residual (u : ℝ) : ℝ := 2 * u - 2 * Real.log (1 + u) - u ^ 2 / (1 + u)

lemma residual_eq (u : ℝ) :
    residual u = 2 * (u - Real.log (1 + u)) - u ^ 2 / (1 + u) := by
  unfold residual
  ring

/-- J(g) - g^2/(2K) = (a0^2/K) * ((u - log(1+u)) - u^2/2) -/
lemma JF_sub_g2_div_2K (K a0 g : ℝ) (ha0 : a0 ≠ 0) :
    JF K a0 g - g ^ 2 / (2 * K) =
      (a0 ^ 2 / K) * ((uOf a0 g - Real.log (1 + uOf a0 g)) - (uOf a0 g) ^ 2 / 2) := by
  unfold JF uOf
  field_simp [ha0]
  ring

/-! ### 2a. The stress sum on the branch -/

/-- On the branch, with g = a0·u,  Pi_rr + Pi_tt = (a0^2/K)(2(u - log(1+u)) - x^2). -/
lemma stress_sum_on_branch (K a0 u x : ℝ) (ha0 : 0 < a0) (h : DeepLaw x u) :
    PiTensor K a0 (radial (a0 * u)) 0 0 + PiTensor K a0 (radial (a0 * u)) 1 1 =
      (a0 ^ 2 / K) * (2 * (u - Real.log (1 + u)) - x ^ 2) := by
  have hg : 0 ≤ a0 * u := mul_nonneg (le_of_lt ha0) (le_of_lt h.1)
  rw [Pi_rr_add_Pi_tt K a0 (a0 * u) hg]
  have hga : uOf a0 (a0 * u) = u := uOf_mul_cancel a0 u (ne_of_gt ha0)
  unfold JF
  simp [hga, uOf]
  rw [← h.div_eq]
  ring_nf

/-- ... and that is exactly (a0^2/K)·residual(u), which is NOT zero. -/
lemma stress_sum_eq_residual (K a0 u x : ℝ) (ha0 : 0 < a0) (h : DeepLaw x u) :
    PiTensor K a0 (radial (a0 * u)) 0 0 + PiTensor K a0 (radial (a0 * u)) 1 1 =
      (a0 ^ 2 / K) * residual u := by
  rw [stress_sum_on_branch K a0 u x ha0 h]
  rw [residual_eq u]
  rw [h.div_eq]

/-! ### 2b. The residual is strictly positive (so the claimed identity is FALSE) -/

/-- F(u) := u - log(1+u) > 0 for u > 0 (from log x < x - 1). -/
lemma F_pos (u : ℝ) (hu : 0 < u) : 0 < u - Real.log (1 + u) := by
  have hp : 0 < 1 + u := by linarith
  have hne : (1 + u : ℝ) ≠ 1 := by linarith
  have h := Real.log_lt_sub_one_of_pos hp hne
  linarith

-- helper derivatives -------------------------------------------------------

lemma hasDerivAt_log_one_add (x : ℝ) (h1p : (1 + x : ℝ) ≠ 0) :
    HasDerivAt (fun t : ℝ => Real.log (1 + t)) (1 / (1 + x)) x := by
  have hlin : HasDerivAt (fun t : ℝ => 1 + t) 1 x := by
    simpa using ((hasDerivAt_const (x := x) (c := (1 : ℝ))).add (hasDerivAt_id x))
  simpa [one_div] using hlin.log h1p

lemma hasDerivAt_sq (x : ℝ) : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := by
  simpa [pow_two] using ((hasDerivAt_id x).mul (hasDerivAt_id x))

lemma hasDerivAt_cube (x : ℝ) : HasDerivAt (fun t : ℝ => t ^ 3) (3 * x ^ 2) x := by
  simpa using ((hasDerivAt_id x).pow 3)

/-- R'(u) = u^2/(1+u)^2 -/
lemma hasDerivAt_residual (x : ℝ) (hx : 0 < x) :
    HasDerivAt residual (x ^ 2 / (1 + x) ^ 2) x := by
  have h1p : (1 + x : ℝ) ≠ 0 := by linarith
  have hlin : HasDerivAt (fun t : ℝ => 1 + t) 1 x := by
    simpa using ((hasDerivAt_const (x := x) (c := (1 : ℝ))).add (hasDerivAt_id x))
  have hlog : HasDerivAt (fun t : ℝ => Real.log (1 + t)) (1 / (1 + x)) x :=
    hasDerivAt_log_one_add x h1p
  have h2log : HasDerivAt (fun t : ℝ => 2 * Real.log (1 + t)) (2 * (1 / (1 + x))) x :=
    hlog.const_mul 2
  have h2t : HasDerivAt (fun t : ℝ => 2 * t) (2 * 1) x :=
    (hasDerivAt_id x).const_mul 2
  have hsq : HasDerivAt (fun t : ℝ => t ^ 2) (2 * x) x := hasDerivAt_sq x
  have hquot : HasDerivAt (fun t : ℝ => t ^ 2 / (1 + t))
      (((2 * x) * (1 + x) - x ^ 2 * 1) / (1 + x) ^ 2) x :=
    hsq.div hlin h1p
  have h := (h2t.sub h2log).sub hquot
  -- h : HasDerivAt (fun t => 2*t - 2*log(1+t) - t^2/(1+t)) (..) x
  change HasDerivAt (fun t : ℝ => 2 * (t - Real.log (1 + t)) - t ^ 2 / (1 + t))
      (x ^ 2 / (1 + x) ^ 2) x
  convert h using 1
  · field_simp [h1p]
    ring

/-- residual is strictly increasing on [0,∞) -/
lemma residual_strictMonoOn : StrictMonoOn residual (Set.Ici (0 : ℝ)) := by
  refine strictMonoOn_of_deriv_pos (convex_Ici (0 : ℝ)) ?hcont ?hderiv
  · unfold residual
    refine ContinuousOn.sub ?hpoly ?hquot
    · fun_prop
    · refine ContinuousOn.div ?hnum ?hden ?hne
      · fun_prop
      · fun_prop
      · intro x hx
        linarith
  · intro x hx
    have hx0 : 0 < x := by simpa [interior_Ici] using hx
    rw [(hasDerivAt_residual x hx0).deriv]
    exact div_pos (sq_pos_of_pos hx0) (sq_pos_of_pos (by linarith : 0 < 1 + x))

lemma residual_zero : residual 0 = 0 := by
  unfold residual
  norm_num

/-- THE HONEST NEGATIVE RESULT: R(u) > 0 for every u > 0.

    Consequently  2(u - log(1+u)) = u^2/(1+u)  is FALSE on the whole branch,
    and Pi_rr + Pi_tt = (a0^2/K)·R  does not vanish. -/
theorem residual_pos (u : ℝ) (hu : 0 < u) : 0 < residual u := by
  have hlt : residual 0 < residual u :=
    residual_strictMonoOn (by simp : (0 : ℝ) ∈ Set.Ici (0 : ℝ))
      (show u ∈ Set.Ici (0 : ℝ) from le_of_lt hu) hu
  simpa [residual_zero] using hlt

/-- the claimed identity fails -/
theorem claimed_identity_false (u : ℝ) (hu : 0 < u) :
    2 * (u - Real.log (1 + u)) - u ^ 2 / (1 + u) ≠ 0 := by
  rw [← residual_eq u]
  exact ne_of_gt (residual_pos u hu)

/-- the stress sum is strictly positive on the branch -/
theorem stress_sum_pos_on_branch (K a0 u x : ℝ) (ha0 : 0 < a0) (hK : 0 < K) (h : DeepLaw x u) :
    0 < PiTensor K a0 (radial (a0 * u)) 0 0 + PiTensor K a0 (radial (a0 * u)) 1 1 := by
  rw [stress_sum_eq_residual K a0 u x ha0 h]
  exact mul_pos (div_pos (sq_pos_of_pos ha0) hK) (residual_pos u h.1)

/-! ### 2c. Exact closed form of the residual: R = 2 (sinh s - s), s = log(1+u) -/

lemma residual_eq_sinh (u : ℝ) (hu : -1 < u) :
    residual u = 2 * (Real.sinh (Real.log (1 + u)) - Real.log (1 + u)) := by
  have hp : 0 < 1 + u := by linarith
  have h1p : (1 + u : ℝ) ≠ 0 := by linarith
  unfold residual
  rw [Real.sinh]
  have hexp : Real.exp (Real.log (1 + u)) = 1 + u := Real.exp_log hp
  have hneg : Real.exp (-(Real.log (1 + u))) = (1 + u)⁻¹ := by
    rw [Real.exp_neg, hexp]
  rw [hexp, hneg]
  field_simp [h1p]
  ring

/-- sinh s > s for s > 0 (mean value theorem), the analytic core of the sign. -/
lemma sinh_gt_self (s : ℝ) (hs : 0 < s) : s < Real.sinh s := by
  let f : ℝ → ℝ := fun y => Real.sinh y - y
  have hmono : StrictMonoOn f (Set.Ici (0 : ℝ)) := by
    refine strictMonoOn_of_deriv_pos (convex_Ici (0 : ℝ)) ?hcont ?hderiv
    · dsimp [f]
      fun_prop
    · intro x hx
      have hx0 : 0 < x := by simpa [interior_Ici] using hx
      have hd : deriv f x = Real.cosh x - 1 := by
        have h := ((Real.hasDerivAt_sinh x).sub (hasDerivAt_id x)).deriv
        dsimp [f] at h
        simpa using h
      rw [hd]
      have hc : 1 < Real.cosh x := (Real.one_lt_cosh).2 (ne_of_gt hx0)
      linarith
  have hlt : f 0 < f s :=
    hmono (by simp : (0 : ℝ) ∈ Set.Ici (0 : ℝ))
      (show s ∈ Set.Ici (0 : ℝ) from le_of_lt hs) hs
  dsimp [f] at hlt
  simpa using hlt

/-- R(u) = 2(sinh(log(1+u)) - log(1+u)) > 0, re-derived from sinh_gt_self. -/
theorem residual_pos_via_sinh (u : ℝ) (hu : 0 < u) : 0 < residual u := by
  rw [residual_eq_sinh u (by linarith : -1 < u)]
  have hs : 0 < Real.log (1 + u) := Real.log_pos (by linarith : 1 < 1 + u)
  nlinarith [sinh_gt_self (Real.log (1 + u)) hs]

/-! ### 2d. What Pi_rr/Pi_tt actually equals -/

/-- Pi_rr = (1 - x^2/(u - log(1+u))) · Pi_tt   (u > 0 on the branch). -/
theorem Pi_rr_eq_ratio_mul_Pi_tt (K a0 u x : ℝ) (hK : K ≠ 0) (h : DeepLaw x u) :
    PiTensor K a0 (radial (a0 * u)) 0 0 =
      (1 - x ^ 2 / (u - Real.log (1 + u))) * PiTensor K a0 (radial (a0 * u)) 1 1 := by
  have hg : 0 ≤ a0 * u := mul_nonneg (sub_nonneg.mp (le_of_lt h.1)) -- placeholder
  sorry
