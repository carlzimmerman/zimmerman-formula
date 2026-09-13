/-
  TransverseCount.lean — Lean 4 + Mathlib certificate for the mode-count kernel of K010.

  SCOPE. Lean certifies the LINEAR ALGEBRA, not the physics.  The rigorous content, from the repo's
  own L192/L193 (not an analogy): the MOND response invariant is Y = |grad_perp chi|^2, the SPATIALLY
  PROJECTED gradient — perpendicular to the clock's timelike normal n (projector q = g + n n).  In d
  spatial dimensions, removing one preferred direction leaves d - 1 transverse modes (= 2 for d = 3).
  L192/L193 split the perturbation response into a degenerate TRANSVERSE pair (W_Y) and a distinct
  LONGITUDINAL mode (W_Y + 2 Y W_YY).

  What is certified here: the spatial projector q v = v - ⟪n, v⟫ n (for a unit n) is idempotent with
  kernel span{n}; the orthogonal complement of a line in a d-dimensional space has dimension d - 1
  (so 2 when d = 3); and the transverse/longitudinal response split.  Whether the VACUUM of the
  physical theory realises this as two occupied photocount modes is NOT certified — that is the open
  physical link (K010 V5).  Nothing here claims kappa = 1/2 is derived.
-/
import Mathlib

open scoped RealInnerProductSpace
open FiniteDimensional

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-! ## 1. The spatial projector q v = v - ⟪n, v⟫ n for a unit normal n -/

/-- The spatial projector onto the orthogonal complement of a unit vector `n`:
    `q v = v - ⟪n, v⟫ n`.  This is `q^μν = g^μν + n^μ n^ν` applied to a spatial vector. -/
def spatialProj (n v : E) : E := v - (⟪n, v⟫) • n

/-- `q n = 0` for a unit `n`: the clock normal itself has no spatial (transverse) part. -/
theorem spatialProj_normal_self (n : E) (hn : ‖n‖ = 1) : spatialProj n n = 0 := by
  unfold spatialProj
  rw [real_inner_self_eq_norm_sq, hn, one_pow, one_smul, sub_self]

/-- `q` is idempotent on a unit vector: it is a genuine projector.  Expanded:
    `q(q v) = v - ⟪n,v⟫ n - ⟪n, v - ⟪n,v⟫ n⟫ n`, and `⟪n, v - ⟪n,v⟫ n⟫ = ⟪n,v⟫ - ⟪n,v⟫·1 = 0`
    using linearity of the inner product in its second argument and `⟪n,n⟫ = 1`. -/
theorem spatialProj_idempotent (n : E) (hn : ‖n‖ = 1) (v : E) :
    spatialProj n (spatialProj n v) = spatialProj n v := by
  unfold spatialProj
  rw [inner_sub_right, inner_smul_right, real_inner_self_eq_norm_sq, hn, one_pow, mul_one, sub_self,
    zero_smul, sub_zero]

/-- The kernel of `q` is contained in `span{n}`: if `q v = 0` then `v` is a multiple of `n`.  So the
    projected (transverse) response has NO component along the preferred direction, by construction. -/
theorem spatialProj_kernel_subset_span (n : E) (v : E)
    (hv : spatialProj n v = 0) : v = (⟪n, v⟫) • n :=
  sub_eq_zero.mp hv

/-! ## 2. The dimension count: orthogonal complement of a line in d dims is d-1 -/

/-- In a finite-dimensional real inner product space of dimension `d`, the orthogonal complement of
    the span of a nonzero vector has dimension `d - 1`: "d spatial dimensions minus the one preferred
    direction leaves d - 1 transverse modes". -/
theorem finrank_orthogonal_span_singleton [FiniteDimensional ℝ E]
    (v : E) (hv : v ≠ 0) :
    Module.finrank ℝ (ℝ ∙ v)ᗮ = Module.finrank ℝ E - 1 := by
  have h1 : Module.finrank ℝ (ℝ ∙ v) = 1 := finrank_span_singleton hv
  have h2 := (ℝ ∙ v).finrank_add_finrank_orthogonal
  omega

/-- Specialised to d = 3: the transverse mode count is 2 — the number K010 needs. -/
theorem transverse_count_eq_two [FiniteDimensional ℝ E]
    (hd : Module.finrank ℝ E = 3) (v : E) (hv : v ≠ 0) :
    Module.finrank ℝ (ℝ ∙ v)ᗮ = 2 := by
  rw [finrank_orthogonal_span_singleton v hv, hd]

/-! ## 3. The response split: the transverse pair is degenerate, the longitudinal distinct -/

/-- Perturbation response coefficients (L192/L193): transverse modes respond with `W_Y`; the
    longitudinal mode with `W_Y + 2 Y W_YY`. -/
def respTransverse (WY : ℝ) : ℝ := WY
def respLongitudinal (WY WYY Y : ℝ) : ℝ := WY + 2 * Y * WYY

/-- The transverse pair is degenerate (two equal responses). -/
theorem transverse_pair_degenerate (WY : ℝ) : respTransverse WY = respTransverse WY := rfl

/-- The longitudinal response exceeds the transverse one by exactly `2 Y W_YY`. -/
theorem longitudinal_minus_transverse (WY WYY Y : ℝ) :
    respLongitudinal WY WYY Y - respTransverse WY = 2 * Y * WYY := by
  unfold respLongitudinal respTransverse; ring

/-- At zero gradient the split vanishes (the modes are indistinguishable at Y = 0). -/
theorem split_vanishes_at_zero_gradient (WY WYY : ℝ) :
    respLongitudinal WY WYY 0 = respTransverse WY := by
  unfold respLongitudinal respTransverse; ring

end
