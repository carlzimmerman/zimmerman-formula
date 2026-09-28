-- AS037 - Constitutive Hessian eigenvalues of an AQUAL branch
-- Algebraic part of the audited-cell certificate: MU2 branch (u = x/2, x = g/a0 >= 0)
-- and Q-branch comparison. EXP/RAR/MONO carry transcendental content (exp, sqrt-composed
-- splines) and are carried numerically in the Python lane (80 dps).
--
-- Constitutive matrix eigenvalues (AQUAL form, flux A(v) = mu(|v|/a0) v):
--   lambda_T = mu               (transverse)
--   lambda_L = mu + x*mu' = d(x*mu)/dx   (longitudinal, x = |v|/a0)
-- MU2: mu(u) = 1 - (1+u)^(-2), u = x/2
-- Q:   mu(x) = (sqrt(1+4x^2)-1)/(2x),  x*mu = yQ(x) = (sqrt(1+4x^2)-1)/2
-- Certified: eigenvalue identities, strict positivity on the declared domains x>0 / u>0,
-- degeneracy at 0, exact upper bounds and Newtonian-side forms.
import Mathlib

noncomputable section
open Real

/- ------------------------- MU2 branch (u = x/2 > 0) ------------------------- -/

def mu2 (u : ℝ) : ℝ := 1 - ((1 + u) ^ (2:ℕ))⁻¹
def mu2p (u : ℝ) : ℝ := 2 / ((1 + u) ^ (3:ℕ))
def lamT (u : ℝ) : ℝ := u * (2 + u) / ((1 + u) ^ (2:ℕ))
def lamL (u : ℝ) : ℝ := u * (4 + 3 * u + u ^ 2) / ((1 + u) ^ (3:ℕ))

theorem mu2_eq_lamT {u : ℝ} (hu : (1:ℝ) + u ≠ 0) : mu2 u = lamT u := by
  unfold mu2 lamT
  have hne2 : (1 + u) ^ (2:ℕ) ≠ 0 := pow_ne_zero 2 hu
  field_simp [hne2]
  ring

theorem lamL_eq_mu_plus {u : ℝ} (hu : (1:ℝ) + u ≠ 0) :
    lamL u = mu2 u + u * mu2p u := by
  unfold lamL mu2 mu2p
  have hne2 : (1 + u) ^ (2:ℕ) ≠ 0 := pow_ne_zero 2 hu
  have hne3 : (1 + u) ^ (3:ℕ) ≠ 0 := pow_ne_zero 3 hu
  field_simp [hne2, hne3]
  ring

theorem lamL_eq_one_plus {u : ℝ} (hu : (1:ℝ) + u ≠ 0) :
    lamL u = 1 + (u - 1) / ((1 + u) ^ (3:ℕ)) := by
  unfold lamL
  have hne3 : (1 + u) ^ (3:ℕ) ≠ 0 := pow_ne_zero 3 hu
  field_simp [hne3]
  ring

/- positivity on the physical domain u > 0 -/

theorem lamT_pos {u : ℝ} (hu : 0 < u) : 0 < lamT u := by
  unfold lamT
  exact div_pos (mul_pos hu (by nlinarith : (0:ℝ) < 2 + u))
    (pow_pos (by nlinarith : (0:ℝ) < 1 + u) 2)

theorem lamL_pos {u : ℝ} (hu : 0 < u) : 0 < lamL u := by
  unfold lamL
  exact div_pos (mul_pos hu (by nlinarith [sq_nonneg u] : (0:ℝ) < 4 + 3 * u + u ^ 2))
    (pow_pos (by nlinarith : (0:ℝ) < 1 + u) 3)

theorem mu2_pos {u : ℝ} (hu : 0 < u) : 0 < mu2 u := by
  rw [mu2_eq_lamT (by nlinarith : (1:ℝ) + u ≠ 0)]
  exact lamT_pos hu

/- degeneracy at the origin: both eigenvalues vanish at u = 0 -/

theorem mu2_zero : mu2 0 = 0 := by
  unfold mu2
  norm_num

theorem lamT_zero : lamT 0 = 0 := by norm_num [lamT]

theorem lamL_zero : lamL 0 = 0 := by norm_num [lamL]

/- exact upper bound and its attainment at u = 2 -/

theorem lamL_le_28_27 {u : ℝ} (hu : 0 ≤ u) : lamL u ≤ (28:ℝ) / 27 := by
  have hu1 : (1:ℝ) + u ≠ 0 := by nlinarith
  rw [lamL_eq_one_plus hu1]
  have hpos : (0:ℝ) < (1 + u) ^ 3 := pow_pos (by nlinarith : (0:ℝ) < 1 + u) 3
  have hmain : 27 * (u - 1) ≤ (1 + u) ^ 3 := by
    have hfac : (1 + u) ^ 3 - 27 * (u - 1) = (u - 2) ^ 2 * (u + 7) := by ring
    nlinarith [mul_nonneg (sq_nonneg (u - 2)) (by nlinarith : (0:ℝ) ≤ u + 7), hfac]
  have hdiv : (u - 1) / ((1 + u) ^ (3:ℕ)) ≤ (1:ℝ) / 27 := by
    rw [div_le_iff₀ hpos]
    nlinarith [hmain]
  linarith

theorem lamL_max_at_two : lamL 2 = (28:ℝ) / 27 := by
  norm_num [lamL]

/- derivative facts:  mu2' = 2/(1+u)^3  and  d(u*mu2)/du = lamL (i.e. lamL = d(x*mu)/dx) -/

theorem mu2p_deriv {u : ℝ} (hu : (1:ℝ) + u ≠ 0) : HasDerivAt mu2 (mu2p u) u := by
  have hlin : HasDerivAt (fun v : ℝ => 1 + v) 1 u := (hasDerivAt_id u).const_add 1
  have hpow2 : HasDerivAt (((fun v : ℝ => 1 + v) ^ (2:ℕ))) (2 * (1 + u)) u := by
    simpa using hlin.pow 2
  have hne2 : (1 + u) ^ (2:ℕ) ≠ 0 := pow_ne_zero 2 hu
  have hinv : HasDerivAt ((((fun v : ℝ => 1 + v) ^ (2:ℕ))⁻¹))
      (-(2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2) u := hpow2.inv hne2
  have hnegv : HasDerivAt (-(((fun v : ℝ => 1 + v) ^ (2:ℕ))⁻¹))
      (-(-(2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2)) u := hinv.neg
  have hc : HasDerivAt (1 + -(((fun v : ℝ => 1 + v) ^ (2:ℕ))⁻¹))
      (-(-(2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2)) u := hnegv.const_add 1
  have hnorm : -(-(2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2) =
      (2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2 := by ring
  have hgoalc : HasDerivAt (1 + -(((fun v : ℝ => 1 + v) ^ (2:ℕ))⁻¹))
      ((2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2) u := by
    rw [hnorm] at hc
    exact hc
  have hfneq : (fun v : ℝ => 1 - (((1 + v) ^ (2:ℕ))⁻¹)) =ᶠ[nhds u]
      (1 + -(((fun v : ℝ => 1 + v) ^ (2:ℕ))⁻¹)) := by
    refine Filter.Eventually.of_forall ?_
    intro v
    simp [sub_eq_add_neg]
  have hgoal : HasDerivAt (fun v : ℝ => 1 - (((1 + v) ^ (2:ℕ))⁻¹))
      ((2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2) u :=
    hgoalc.congr_of_eventuallyEq hfneq
  have hrate : (2 * (1 + u)) / ((1 + u) ^ (2:ℕ)) ^ 2 = 2 / ((1 + u) ^ (3:ℕ)) := by
    have hne3 : (1 + u) ^ (3:ℕ) ≠ 0 := pow_ne_zero 3 hu
    have hne4 : (1 + u) ^ (4:ℕ) ≠ 0 := pow_ne_zero 4 hu
    field_simp [hu, hne3, hne4]
  have hgoal2 : HasDerivAt (fun v : ℝ => 1 - (((1 + v) ^ (2:ℕ))⁻¹))
      (2 / ((1 + u) ^ (3:ℕ))) u := by
    rw [hrate] at hgoal
    exact hgoal
  rw [show mu2 = (fun v : ℝ => 1 - (((1 + v) ^ (2:ℕ))⁻¹)) by rfl]
  rw [show mu2p u = 2 / ((1 + u) ^ (3:ℕ)) by rfl]
  exact hgoal2

theorem xmu2_deriv {u : ℝ} (hu : (1:ℝ) + u ≠ 0) :
    HasDerivAt (fun v : ℝ => v * mu2 v) (lamL u) u := by
  have htmp : HasDerivAt (id * mu2) (1 * mu2 u + id u * mu2p u) u :=
    (hasDerivAt_id u).mul (mu2p_deriv hu)
  have hfneq : (fun v : ℝ => v * mu2 v) =ᶠ[nhds u] (id * mu2) := by
    refine Filter.Eventually.of_forall ?_
    intro v
    simp
  have htmp2 : HasDerivAt (fun v : ℝ => v * mu2 v) (1 * mu2 u + id u * mu2p u) u :=
    htmp.congr_of_eventuallyEq hfneq
  have heq : 1 * mu2 u + id u * mu2p u = lamL u := by
    simp [one_mul]
    exact (lamL_eq_mu_plus hu).symm
  rw [heq] at htmp2
  exact htmp2

/- ------------------------- Q branch (x > 0) ------------------------- -/

def muQ (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / (2 * x)
def yQ (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
def lamLQ (x : ℝ) : ℝ := 2 * x / Real.sqrt (1 + 4 * x ^ 2)

theorem yQ_eq_x_muQ {x : ℝ} (hx : x ≠ 0) : x * muQ x = yQ x := by
  unfold muQ yQ
  field_simp [hx]

theorem yQ_pos {x : ℝ} (hx : 0 < x) : 0 < yQ x := by
  unfold yQ
  have h1 : (1:ℝ) < Real.sqrt (1 + 4 * x ^ 2) := by
    rw [Real.lt_sqrt (by norm_num : (0:ℝ) ≤ 1)]
    nlinarith [pow_pos hx 2]
  exact div_pos (sub_pos.mpr h1) (by norm_num)

theorem muQ_pos {x : ℝ} (hx : 0 < x) : 0 < muQ x := by
  unfold muQ
  have h1 : (1:ℝ) < Real.sqrt (1 + 4 * x ^ 2) := by
    rw [Real.lt_sqrt (by norm_num : (0:ℝ) ≤ 1)]
    nlinarith [pow_pos hx 2]
  exact div_pos (sub_pos.mpr h1) (mul_pos zero_lt_two hx)

/- deep bracket: 0 < muQ < x  (muQ ~ x as x -> 0, i.e. B ~ g^2/a0) -/

theorem muQ_lt_x {x : ℝ} (hx : 0 < x) : muQ x < x := by
  unfold muQ
  have hs : Real.sqrt (1 + 4 * x ^ 2) < 1 + 2 * x ^ 2 := by
    rw [Real.sqrt_lt' (by nlinarith : (0:ℝ) < 1 + 2 * x ^ 2)]
    nlinarith [pow_pos hx 2]
  exact (div_lt_iff₀ (by positivity : (0:ℝ) < 2 * x)).mpr (by nlinarith [hs])

theorem muQ_lt_one {x : ℝ} (hx : 0 < x) : muQ x < 1 := by
  unfold muQ
  have hs : Real.sqrt (1 + 4 * x ^ 2) < 1 + 2 * x := by
    rw [Real.sqrt_lt' (by nlinarith : (0:ℝ) < 1 + 2 * x)]
    nlinarith [pow_pos hx 2]
  exact (div_lt_iff₀ (by positivity : (0:ℝ) < 2 * x)).mpr (by nlinarith [hs])

theorem lamLQ_pos {x : ℝ} (hx : 0 < x) : 0 < lamLQ x := by
  unfold lamLQ
  exact div_pos (mul_pos zero_lt_two hx) (Real.sqrt_pos.2 (by nlinarith [pow_pos hx 2]))

theorem lamLQ_lt_one {x : ℝ} (hx : 0 < x) : lamLQ x < 1 := by
  unfold lamLQ
  have h2x : 2 * x < Real.sqrt (1 + 4 * x ^ 2) := by
    rw [Real.lt_sqrt (by positivity : (0:ℝ) ≤ 2 * x)]
    nlinarith [sq_nonneg x]
  exact (div_lt_one (Real.sqrt_pos.2 (by nlinarith [sq_nonneg x]))).mpr h2x

/- lambda_L = d(x*mu)/dx for Q:  d/dx [(sqrt(1+4x^2)-1)/2] = 2x/sqrt(1+4x^2) -/

theorem yQ_deriv {x : ℝ} (hx : 0 < x) : HasDerivAt yQ (lamLQ x) x := by
  have harg : 0 < 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
  have hd : HasDerivAt (fun z : ℝ => 1 + 4 * z ^ 2) (4 * (2 * x)) x := by
    simpa using (((hasDerivAt_id x).pow (2 : ℕ)).const_mul (4 : ℝ)).const_add (1 : ℝ)
  have hds : HasDerivAt (fun z : ℝ => Real.sqrt (1 + 4 * z ^ 2))
      ((4 * (2 * x)) / (2 * Real.sqrt (1 + 4 * x ^ 2))) x :=
    hd.sqrt (ne_of_gt harg)
  have hdy : HasDerivAt (fun z : ℝ => (Real.sqrt (1 + 4 * z ^ 2) - 1) / 2)
      (((4 * (2 * x)) / (2 * Real.sqrt (1 + 4 * x ^ 2))) / 2) x :=
    (hds.sub_const 1).div_const 2
  have hslope : ((4 * (2 * x)) / (2 * Real.sqrt (1 + 4 * x ^ 2))) / 2 =
      2 * x / Real.sqrt (1 + 4 * x ^ 2) := by
    field_simp [ne_of_gt (Real.sqrt_pos.2 harg)]
    ring
  rw [hslope] at hdy
  exact hdy

/- transferring to the flux form: d(x*muQ)/dx = lamLQ (x > 0) -/

theorem xmuQ_deriv {x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun t : ℝ => t * muQ t) (lamLQ x) x := by
  have hy : HasDerivAt yQ (lamLQ x) x := yQ_deriv hx
  have hfneq : (fun t : ℝ => t * muQ t) =ᶠ[nhds x] yQ := by
    refine Filter.Eventually.of_forall ?_
    intro t
    by_cases ht : t = 0
    · subst t
      simp [yQ, muQ, Real.sqrt_one]
    · exact yQ_eq_x_muQ ht
  exact hy.congr_of_eventuallyEq hfneq

#check mu2_eq_lamT
#check lamL_eq_mu_plus
#check lamL_pos
#check mu2_pos
#check lamT_pos
#check lamL_le_28_27
#check lamL_max_at_two
#check mu2p_deriv
#check xmu2_deriv
#check muQ_pos
#check muQ_lt_one
#check muQ_lt_x
#check lamLQ_pos
#check lamLQ_lt_one
#check yQ_deriv
#check xmuQ_deriv

#print axioms mu2_eq_lamT
#print axioms lamL_eq_mu_plus
#print axioms lamL_eq_one_plus
#print axioms lamT_pos
#print axioms lamL_pos
#print axioms mu2_pos
#print axioms mu2_zero
#print axioms lamT_zero
#print axioms lamL_zero
#print axioms lamL_le_28_27
#print axioms lamL_max_at_two
#print axioms mu2p_deriv
#print axioms xmu2_deriv
#print axioms yQ_eq_x_muQ
#print axioms yQ_pos
#print axioms muQ_pos
#print axioms muQ_lt_x
#print axioms muQ_lt_one
#print axioms lamLQ_pos
#print axioms lamLQ_lt_one
#print axioms yQ_deriv
#print axioms xmuQ_deriv

end
