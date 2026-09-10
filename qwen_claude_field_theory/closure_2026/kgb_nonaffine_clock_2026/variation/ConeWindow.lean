import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Exact algebra for the already-derived local principal pencil. This is not
a proof that any particular action or background realizes the pencil, nor a
full physical Hamiltonian or nonlinear stability theorem. -/
namespace NonaffineConeWindow

def cone (K R T cross : ℝ) : Prop :=
  0 < K ∧ R < 0 ∧ T < 0 ∧ |cross| < K ∧
  ∀ t : ℝ, 0 ≤ t → t ≤ 1 →
    0 < K+T-2*|cross| *t+(R-T)*t^2

theorem feasible_K_iff (I R beta cross : ℝ) (hR : R < 0) (hb : 0 < beta) :
    (∃ K : ℝ, cone K R (beta*(K-I)) cross) ↔ 0 < I+R-2*|cross| := by
  constructor
  · rintro ⟨K,hK,hR',hT,hcross,hlight⟩
    have hKI : K < I := by
      by_contra h
      have hnon : 0 ≤ beta*(K-I) :=
        mul_nonneg (le_of_lt hb) (sub_nonneg.mpr (le_of_not_gt h))
      linarith
    have hrad := hlight 1 (by norm_num) (by norm_num)
    nlinarith
  · intro hgap
    let gap := I+R-2*|cross|
    let delta := min (gap/2) (-R/(2*beta))
    have hgap' : 0 < gap := hgap
    have hfracpos : 0 < -R/(2*beta) :=
      div_pos (neg_pos.mpr hR) (mul_pos (by norm_num) hb)
    have hd : 0 < delta := lt_min (by linarith) hfracpos
    have hdg : delta ≤ gap/2 := min_le_left _ _
    have hdf : delta ≤ -R/(2*beta) := min_le_right _ _
    have hfrac : beta*(-R/(2*beta)) = -R/2 := by
      field_simp
    have hbd : beta*delta ≤ -R/2 := by
      have h := mul_le_mul_of_nonneg_left hdf (le_of_lt hb)
      rwa [hfrac] at h
    have hI : 0 < I := by
      have hc := abs_nonneg cross
      dsimp [gap] at hgap'
      linarith
    have hq0 : 0 < I-delta-beta*delta := by
      dsimp [gap] at hdg
      linarith [abs_nonneg cross]
    have hq1 : 0 < I-delta+R-2*|cross| := by
      dsimp [gap] at hdg hgap'
      linarith
    have hconc : R+beta*delta ≤ 0 := by linarith
    refine ⟨I-delta, ?_, hR, ?_, ?_, ?_⟩
    · linarith [abs_nonneg cross]
    · have hpos := mul_pos hb hd
      nlinarith
    · linarith [abs_nonneg cross]
    · intro t ht ht1
      have hw : 0 ≤ 1-t := sub_nonneg.mpr ht1
      have hmix : 0 < (1-t)*(I-delta-beta*delta)
          +t*(I-delta+R-2*|cross|) := by
        by_cases htz : t = 0
        · simpa [htz] using hq0
        · have htpos : 0 < t := lt_of_le_of_ne ht (Ne.symm htz)
          exact add_pos_of_nonneg_of_pos
            (mul_nonneg hw (le_of_lt hq0)) (mul_pos htpos hq1)
      have hcorr : 0 ≤ -(R+beta*delta)*(t*(1-t)) :=
        mul_nonneg (neg_nonneg.mpr hconc) (mul_nonneg ht hw)
      nlinarith

theorem feasible_affine_control_iff
    (I R beta cross K0 slope : ℝ)
    (hR : R < 0) (hb : 0 < beta) (hs : slope ≠ 0) :
    (∃ j : ℝ, cone (K0+slope*j) R (beta*(K0+slope*j-I)) cross) ↔
    0 < I+R-2*|cross| := by
  constructor
  · rintro ⟨j,hj⟩
    exact (feasible_K_iff I R beta cross hR hb).1 ⟨K0+slope*j,hj⟩
  · intro hgap
    obtain ⟨K,hK⟩ := (feasible_K_iff I R beta cross hR hb).2 hgap
    refine ⟨(K-K0)/slope, ?_⟩
    have heq : K0+slope*((K-K0)/slope) = K := by
      field_simp
      ring
    simpa [heq] using hK

#print axioms feasible_K_iff
#print axioms feasible_affine_control_iff
end NonaffineConeWindow
