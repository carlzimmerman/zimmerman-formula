import Mathlib
import Mathlib.Tactic

/-!
# AS063 -- Identifiability of n and a per-channel slope (Lean 4 certificate)

Formalized content (all in the declared CORE coefficient / MU_n response cell;
`Y = g/s` with `s = c*sqrt(G*rho_Lambda) > 0` the vacuum's own acceleration scale,
`lambda > 0` the dimensionless per-channel slope, `n : Nat, n >= 1` the channel
count; `kappa = 1/2` stays an ADOPTED framework input -- not derived here):

    mu  (n lambda Y) := 1 - (1 + lambda*Y)^(-(n:Z))     -- the response family
    pLam(lambda Y)    := 1 - (1 + lambda*Y)^(-1)        -- per-channel engagement
    slope     (n lambda) := (n : R) * lambda             -- the deep slope
    kappaCoef (n lambda) := n*(n+1) * lambda^2 / 2       -- 2nd-order |coefficient|

  T1  OR-composition identity (PD01 A2 lambda-generalised): with per-channel
        engagement p_lam (p_lam(0)=0, p_lam(inf)=1), the OR composition
        1 - (1 - p_lam(Y))^n equals the family mu(n,lambda,Y) for every Y.
        [zpow algebra: (x^(-1))^n = x^(-n)]

  T2  THE DEEP SLOPE:  HasDerivAt (fun Y => mu n lambda Y) ((n : R) * lambda) 0
        -- the deep slope of the composed response is the PRODUCT n*lambda
        (channel count x per-channel slope).  [chain rule + zpow derivative]
        At n = 1 this also certifies the per-channel property p_lam'(0) = lambda.

  T3  Spherical deep matching (scale factors explicit): with a0 := s/(n*lambda)
        from the a0-line g^2 = a0 * g_N, the coefficient kappa := a0/s equals
        1/(n*lambda): a function of the PRODUCT only.  [field algebra]

  T4  Curvature lambda-freeness: 2 * n * kappaCoef = (n+1) * slope^2, i.e. the
        normalized transition curvature  kappaCoef / slope^2 = (n+1)/(2n)
        contains NO lambda: a curvature measurement would fix n once the
        product (deep data) is known.  [pure ring algebra]

  T5 + T6  IDENTIFIABILITY THEOREM: the normalized curvature ratio is an
        injective function of the channel count n (T5), and two configurations
        with EQUAL PRODUCT (deep-equivalent) and EQUAL curvature must have
        equal channel counts (T6).  Thus deep data (product only, T2+T3)
        cannot separate n from lambda; the transition-shape observable
        (T4-T6) could -- stated as an identifiability criterion, not a claim
        that current observations already deliver it.

  T7  NEWTONIAN RECOVERY:  mu(n,lambda,Y) -> 1 as Y -> +infinity (the exact
        high-field limit of the family; the n-dependent tail follows from the
        zpow structure, exercised numerically in compute_as063.py).  [atTop]

Certification discipline: no sorry.  Axioms expected within
{propext, Classical.choice, Quot.sound}.
-/

noncomputable section
open Real
open Filter
open scoped Topology

namespace AS063

def slope (n : ℕ) (lam : ℝ) : ℝ := (n : ℝ) * lam

def kappaCoef (n : ℕ) (lam : ℝ) : ℝ := (n : ℝ) * ((n : ℝ) + 1) * lam ^ 2 / 2

def mu (n : ℕ) (lam : ℝ) (Y : ℝ) : ℝ := 1 - (1 + lam * Y) ^ (-(n : ℤ))

def pLam (lam : ℝ) (Y : ℝ) : ℝ := 1 - (1 + lam * Y) ^ (-(1 : ℤ))

-- =====================================================================
-- T1: the OR composition over n channels with per-channel engagement
--     p_lam(Y) = 1 - (1 + lambda*Y)^(-1) IS the family mu(n,lambda,Y)
-- =====================================================================
theorem as063_or_composition (n : ℕ) (lam : ℝ) (Y : ℝ) :
    (1 - pLam lam Y) ^ n = (1 + lam * Y) ^ (-(n : ℤ)) := by
  unfold pLam
  simp

-- =====================================================================
-- T2: the deep slope of the response family is the product n * lambda
-- =====================================================================
theorem as063_deep_slope (n : ℕ) (lam : ℝ) :
    HasDerivAt (fun Y : ℝ => mu n lam Y) (slope n lam) 0 := by
  unfold mu slope
  have hu : HasDerivAt (fun Y : ℝ => 1 + lam * Y) lam (0 : ℝ) := by
    simpa [mul_one, add_zero] using
      (HasDerivAt.const_add (1 : ℝ) (HasDerivAt.const_mul lam (hasDerivAt_id (0 : ℝ))))
  have hpow : HasDerivAt (fun Y : ℝ => (1 + lam * Y) ^ n)
      ((n : ℝ) * (1 + lam * (0 : ℝ)) ^ (n - 1) * lam) (0 : ℝ) :=
    hu.pow n
  have hzpow : HasDerivAt (fun Y : ℝ => ((1 + lam * Y) ^ n)⁻¹) (-(lam * (n : ℝ))) (0 : ℝ) := by
    simpa [Pi.inv_def, one_pow, inv_one, div_one, neg_mul, neg_neg, mul_one, mul_zero,
      add_zero, mul_comm, mul_left_comm] using hpow.inv (by simp)
  have hb : HasDerivAt (fun Y : ℝ => 1 - ((1 + lam * Y) ^ n)⁻¹) (lam * (n : ℝ)) (0 : ℝ) := by
    simpa [Pi.neg_def, Pi.inv_def, neg_neg, sub_eq_add_neg, add_comm] using
      (hzpow.neg).const_add (1 : ℝ)
  have hs : HasDerivAt (fun Y : ℝ => 1 - (1 + lam * Y) ^ (-(n : ℤ))) (lam * (n : ℝ)) (0 : ℝ) :=
    hb.congr_of_eventuallyEq (Eventually.of_forall (fun Y => by simp [zpow_neg, zpow_natCast]))
  simpa only [mul_comm] using hs

-- =====================================================================
-- T3: kappa := a0/s with a0 := s/(n*lambda) is 1/(n*lambda): a function
--     of the product only (scale-free: any footing once s is fixed).
-- =====================================================================
theorem as063_kappa_of_product (n : ℕ) (lam s : ℝ) (hs : s ≠ 0) (hl : slope n lam ≠ 0) :
    s / slope n lam / s = 1 / slope n lam := by
  field_simp [hs, hl]

-- =====================================================================
-- T4: the normalized transition curvature is lambda-free
--     2 n * kappaCoef(n, lambda) = (n+1) * slope(n, lambda)^2
-- =====================================================================
theorem as063_curvature_lambda_free (n : ℕ) (lam : ℝ) :
    2 * (n : ℝ) * kappaCoef n lam = ((n : ℝ) + 1) * (slope n lam) ^ 2 := by
  unfold slope kappaCoef
  ring

-- =====================================================================
-- T5: the ratio map n -> (n+1)/n is injective (on natural n >= 1)
-- =====================================================================
theorem as063_shape_ratio_injective (n n' : ℕ) (hn : (n : ℝ) ≠ 0) (hn' : (n' : ℝ) ≠ 0)
    (h : ((n : ℝ) + 1) / (n : ℝ) = ((n' : ℝ) + 1) / (n' : ℝ)) : n = n' := by
  have hR : (n : ℝ) = (n' : ℝ) := by
    field_simp [hn, hn'] at h
    nlinarith
  exact_mod_cast hR

-- =====================================================================
-- T6: equal PRODUCT (deep-equivalent) and equal curvature force n = n'
-- =====================================================================
theorem as063_curvature_separates (n n' : ℕ) (lam lam' : ℝ)
    (hn : 0 < n) (hn' : 0 < n') (hlam : 0 < lam) (hlam' : 0 < lam')
    (hprod : slope n lam = slope n' lam') (hk : kappaCoef n lam = kappaCoef n' lam') :
    n = n' := by
  let s := slope n lam
  have hs2 : s ^ 2 ≠ 0 := by
    have hs_pos : 0 < s := by
      dsimp [s]
      unfold slope
      exact mul_pos (by exact_mod_cast hn) hlam
    exact pow_ne_zero 2 (ne_of_gt hs_pos)
  have hL : 2 * (n : ℝ) * kappaCoef n lam = ((n : ℝ) + 1) * s ^ 2 := by
    dsimp [s]
    exact as063_curvature_lambda_free n lam
  have hLs : 2 * (n' : ℝ) * kappaCoef n' lam' = ((n' : ℝ) + 1) * s ^ 2 := by
    dsimp [s]
    rw [hprod]
    exact as063_curvature_lambda_free n' lam'
  have hA : ((n : ℝ) + 1) * (2 * (n' : ℝ)) * s ^ 2 =
      ((n' : ℝ) + 1) * (2 * (n : ℝ)) * s ^ 2 := by
    calc
      ((n : ℝ) + 1) * (2 * (n' : ℝ)) * s ^ 2
          = 2 * (n' : ℝ) * (((n : ℝ) + 1) * s ^ 2) := by ring
      _ = 2 * (n' : ℝ) * (2 * (n : ℝ) * kappaCoef n lam) := by rw [hL]
      _ = 2 * (n : ℝ) * (2 * (n' : ℝ) * kappaCoef n' lam') := by rw [hk]; ring
      _ = 2 * (n : ℝ) * (((n' : ℝ) + 1) * s ^ 2) := by rw [hLs]
      _ = ((n' : ℝ) + 1) * (2 * (n : ℝ)) * s ^ 2 := by ring
  have hB : ((n : ℝ) + 1) * (2 * (n' : ℝ)) = ((n' : ℝ) + 1) * (2 * (n : ℝ)) :=
    mul_right_cancel₀ hs2 hA
  have hC : (n : ℝ) = (n' : ℝ) := by
    nlinarith [hB]
  exact_mod_cast hC

-- =====================================================================
-- T7: Newtonian recovery: mu(n,lambda,Y) -> 1 as Y -> +infinity
-- =====================================================================
theorem as063_newtonian_recovery (n : ℕ) (lam : ℝ) (hn : n ≠ 0) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => mu n lam Y) atTop (𝓝 1) := by
  unfold mu
  have hu0 : Tendsto (fun Y : ℝ => lam * Y) atTop atTop := by
    exact (tendsto_const_mul_atTop_of_pos hlam).mpr tendsto_id
  have hu : Tendsto (fun Y : ℝ => 1 + lam * Y) atTop atTop := by
    simpa only [add_comm] using
      (tendsto_atTop_add_const_right (atTop : Filter ℝ) (1 : ℝ) hu0)
  have hpow : Tendsto (fun Y : ℝ => (1 + lam * Y) ^ n) atTop atTop :=
    (tendsto_pow_atTop hn).comp hu
  have hinv : Tendsto (fun Y : ℝ => ((1 + lam * Y) ^ n)⁻¹) atTop (𝓝 0) :=
    tendsto_inv_atTop_zero.comp hpow
  have hz : Tendsto (fun Y : ℝ => (1 + lam * Y) ^ (-(n : ℤ))) atTop (𝓝 0) :=
    hinv.congr' (Eventually.of_forall (fun Y => by simp [zpow_neg, zpow_natCast]))
  have hmu : Tendsto (fun Y : ℝ => 1 - (1 + lam * Y) ^ (-(n : ℤ))) atTop (𝓝 (1 - 0)) :=
    Tendsto.sub tendsto_const_nhds hz
  simpa only [sub_zero] using hmu

/-- The per-channel engagement saturates: p_lam(Y) -> 1 as Y -> +infinity.
    Together with p_lam(0) = 0 (simp) and p_lam'(0) = lam (T2 at n = 1). -/
theorem as063_per_channel_saturates (lam : ℝ) (hlam : 0 < lam) :
    Tendsto (fun Y : ℝ => pLam lam Y) atTop (𝓝 1) := by
  have h := as063_newtonian_recovery 1 lam (by norm_num) hlam
  simpa using h.congr' (Eventually.of_forall (fun Y => by rfl))

end AS063
#print axioms AS063.as063_or_composition
#print axioms AS063.as063_deep_slope
#print axioms AS063.as063_kappa_of_product
#print axioms AS063.as063_curvature_lambda_free
#print axioms AS063.as063_shape_ratio_injective
#print axioms AS063.as063_curvature_separates
#print axioms AS063.as063_newtonian_recovery
#print axioms AS063.as063_per_channel_saturates
