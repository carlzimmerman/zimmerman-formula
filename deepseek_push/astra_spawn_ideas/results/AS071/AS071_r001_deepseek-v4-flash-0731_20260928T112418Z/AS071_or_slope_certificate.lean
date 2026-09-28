/-
AS071 -- Physical response versus probability interpretation (audit).
Run: AS071_r001_deepseek-v4-flash-0731_20260928T112418Z

Certified algebraic identities (MU_n statistical-response branch, the task's
declared branch; nothing here transfers to the MONO operative target):

  (1) or_slope_chain_rule
      For ANY differentiable completion p with HasDerivAt p p' 0,
          d/dY [ 1 - (1 - p Y)^n ] |_{Y=0}  =  n * (1 - p 0)^(n-1) * p'.
      This is the exact chain-rule value behind the OR composition
      mu_n(Y) = 1 - (1 - p(Y))^n (PD01 A1 / PD08 STEP 4).

  (2) or_slope_eq_count
      If additionally p(0) = 0 and p'(0) = 1 (the fraction identity),
          d/dY [ 1 - (1 - p Y)^n ] |_{Y=0}  =  n.
      The deep-MOND slope equals the channel count for EVERY completion:
      the count, not the CDF, carries the slope.

  (3) corpus_mu_n_slope
      The corpus family mu_n(Y) = 1 - (1/(1+Y))^n has slope n at 0, and
      corpus_slope_one / corpus_slope_two show n = 1 and n = 2 both occur:
      CDF-shaped response functions with slopes 1 and 2 exist in the same
      family, so CDF-ness alone does not fix the slope (the audit point:
      the kappa = a0/s = 1/n content lives in the physical premises
      'OR composition', 'p'(0) = 1', 'channel count n' -- NOT in the
      probability/CDF reading of mu).

  (4) corpus_is_or_member
      The corpus family IS a member of the OR class: with p(Y) = Y/(1+Y),
          (1 - p Y) = 1/(1+Y)   on a neighbourhood of Y = 0,
      so  1 - (1 - p Y)^n  =  1 - (1/(1+Y))^n  eventually at 0.

Style notes: function-level `sub`/`add`/`div` types are bridged to their
lambda forms through HasDerivAt.congr_of_eventuallyEq with pointwise rfl;
the field identity in corpus_is_or_member is closed by field_simp with no
trailing tactic.
-/
import Mathlib

noncomputable section
open scoped Real Topology
open Filter

namespace AS071

/-- Chain-rule value of the OR-composition slope at the origin:
    (1 - (1 - p ·)^n)' (0) = n * (1 - p 0)^(n-1) * p'. -/
theorem or_slope_chain_rule {p : ℝ → ℝ} {p' : ℝ} (n : ℕ)
    (hp : HasDerivAt p p' 0) :
    HasDerivAt (fun Y : ℝ => 1 - (1 - p Y) ^ n)
      ((n : ℝ) * (1 - p 0) ^ (n - 1) * p') 0 := by
  have hf_raw : HasDerivAt ((fun _ : ℝ => (1 : ℝ)) - p) (-p') 0 := by
    simpa using (hasDerivAt_const 0 (1 : ℝ)).sub hp
  have hf : HasDerivAt (fun Y : ℝ => 1 - p Y) (-p') 0 := by
    refine hf_raw.congr_of_eventuallyEq ?_
    filter_upwards with Y
    rfl
  have hfn : HasDerivAt (fun Y : ℝ => (1 - p Y) ^ n)
      ((n : ℝ) * ((1 - p 0) ^ (n - 1)) * (-p')) 0 := hf.pow n
  have hres : HasDerivAt (fun Y : ℝ => 1 - (1 - p Y) ^ n)
      ((0 : ℝ) - (((n : ℝ) * (1 - p 0) ^ (n - 1)) * (-p'))) 0 := by
    refine ((hasDerivAt_const 0 (1 : ℝ)).sub hfn).congr_of_eventuallyEq ?_
    filter_upwards with Y
    rfl
  have hval : (0 : ℝ) - (((n : ℝ) * (1 - p 0) ^ (n - 1)) * (-p')) =
      (n : ℝ) * (1 - p 0) ^ (n - 1) * p' := by
    ring
  simpa [hval] using hres

/-- With p(0) = 0 and p'(0) = 1, the OR-composition deep-MOND slope is the
    channel count n, for EVERY completion p. -/
theorem or_slope_eq_count {p : ℝ → ℝ} (n : ℕ) (hp0 : p 0 = 0)
    (hp1 : HasDerivAt p 1 0) :
    HasDerivAt (fun Y : ℝ => 1 - (1 - p Y) ^ n) (n : ℝ) 0 := by
  have hc := or_slope_chain_rule (p := p) (p' := 1) n hp1
  have hval : (n : ℝ) * (1 - p 0) ^ (n - 1) * 1 = (n : ℝ) := by
    rw [hp0]
    simp
  simpa [hval] using hc

/-- The corpus family mu_n(Y) = 1 - (1/(1+Y))^n has deep slope n at 0. -/
theorem corpus_mu_n_slope (n : ℕ) :
    HasDerivAt (fun Y : ℝ => 1 - (1 / (1 + Y)) ^ n) (n : ℝ) 0 := by
  have hc : HasDerivAt (fun _ : ℝ => (1 : ℝ)) 0 0 := hasDerivAt_const 0 (1 : ℝ)
  have hg_raw : HasDerivAt ((fun _ : ℝ => (1 : ℝ)) + id) (1 : ℝ) 0 := by
    simpa using (hasDerivAt_const 0 (1 : ℝ)).add (hasDerivAt_id 0)
  have hg : HasDerivAt (fun Y : ℝ => (1 : ℝ) + Y) 1 0 := by
    refine hg_raw.congr_of_eventuallyEq ?_
    filter_upwards with Y
    rfl
  have hg0 : (1 : ℝ) + 0 ≠ 0 := by norm_num
  have hinv_raw : HasDerivAt ((fun _ : ℝ => (1 : ℝ)) / (fun Y : ℝ => (1 : ℝ) + Y))
      (-1) 0 := by
    simpa using hc.div hg hg0
  have hinv : HasDerivAt (fun Y : ℝ => 1 / (1 + Y)) (-1) 0 := by
    refine hinv_raw.congr_of_eventuallyEq ?_
    filter_upwards with Y
    rfl
  have hpow : HasDerivAt (fun Y : ℝ => (1 / (1 + Y)) ^ n)
      ((n : ℝ) * ((1 / (1 + 0)) ^ (n - 1)) * (-1)) 0 := hinv.pow n
  have hval1 : (1 / (1 + 0)) ^ (n - 1) = 1 := by
    simp
  have hpow1 : HasDerivAt (fun Y : ℝ => (1 / (1 + Y)) ^ n) (-(n : ℝ)) 0 := by
    simpa [hval1] using hpow
  have hres : HasDerivAt (fun Y : ℝ => 1 - (1 / (1 + Y)) ^ n)
      ((0 : ℝ) - (-(n : ℝ))) 0 := by
    refine ((hasDerivAt_const 0 (1 : ℝ)).sub hpow1).congr_of_eventuallyEq ?_
    filter_upwards with Y
    rfl
  simpa using hres

/-- Slope 1 and slope 2 both occur in the CDF-shaped corpus family:
    CDF-ness does not fix the deep slope. -/
theorem corpus_slope_one :
    HasDerivAt (fun Y : ℝ => 1 - 1 / (1 + Y)) 1 0 := by
  simpa using corpus_mu_n_slope 1

theorem corpus_slope_two :
    HasDerivAt (fun Y : ℝ => 1 - (1 / (1 + Y)) ^ 2) 2 0 := by
  simpa using corpus_mu_n_slope 2

/-- The corpus family is a member of the OR class: with the engagement
    p(Y) = Y/(1+Y),  (1 - p Y) = 1/(1+Y) eventually at 0. -/
theorem corpus_is_or_member (n : ℕ) :
    EventuallyEq (𝓝 (0 : ℝ)) (fun Y : ℝ => 1 - (1 - Y / (1 + Y)) ^ n)
      (fun Y : ℝ => 1 - (1 / (1 + Y)) ^ n) := by
  have hEq : Set.EqOn (fun Y : ℝ => 1 - (1 - Y / (1 + Y)) ^ n)
      (fun Y : ℝ => 1 - (1 / (1 + Y)) ^ n) {Y : ℝ | Y ≠ -1} := by
    intro Y hY
    have hY1 : (1 : ℝ) + Y ≠ 0 := by
      intro h
      apply hY
      linarith
    have hb : 1 - Y / (1 + Y) = 1 / (1 + Y) := by
      field_simp [hY1]
      ring
    change 1 - (1 - Y / (1 + Y)) ^ n = 1 - (1 / (1 + Y)) ^ n
    rw [hb]
  have hmem : {Y : ℝ | Y ≠ -1} ∈ 𝓝 (0 : ℝ) := by
    exact (isOpen_compl_singleton (x := (-1 : ℝ))).mem_nhds (by norm_num : (0 : ℝ) ≠ -1)
  exact hEq.eventuallyEq_of_mem hmem

#print axioms AS071.or_slope_chain_rule
#print axioms AS071.or_slope_eq_count
#print axioms AS071.corpus_mu_n_slope
#print axioms AS071.corpus_slope_one
#print axioms AS071.corpus_slope_two
#print axioms AS071.corpus_is_or_member

end AS071
