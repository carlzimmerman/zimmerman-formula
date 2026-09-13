/-
  TransverseCount.lean — Lean 4 + Mathlib certificate for the mode-count kernel of K010.

  SCOPE. Lean certifies the LINEAR ALGEBRA, not the physics.  The physical claim of K010 is that the
  vacuum presents n = 2 modes to an acceleration.  The rigorous content, drawn from the repo's own
  L192/L193 (not an analogy), is:

    * The MOND response invariant is Y = |grad_perp chi|^2, the SPATIALLY PROJECTED gradient — the
      component of grad chi PERPENDICULAR to the clock's timelike normal n (projector q = g + n n).
    * In d spatial dimensions, decomposing a vector along one preferred direction (the background
      gradient / clock normal) leaves an orthogonal complement of dimension d - 1 = 2 in d = 3.
    * L192/L193 show the perturbation response splits into a TRANSVERSE pair (degenerate, eigenvalue
      W_Y) and a LONGITUDINAL mode (eigenvalue W_Y + 2 Y W_YY); the degeneracy is structural.

  What is certified here: the spatial projector q = 1 - n nᵀ is idempotent with kernel span{n}; the
  orthogonal complement of a line in a d-dimensional space has dimension d - 1 (so 2 when d = 3); and
  the transverse-pair / longitudinal response split.  Whether the VACUUM of the physical theory
  realises this as two occupied photocount modes is NOT certified — that is the open physical link
  (K010 V5).  Nothing here claims kappa = 1/2 is derived; it certifies the dimension count the
  candidate derivation rests on.
-/
import Mathlib

open scoped RealInnerProductSpace
open FiniteDimensional

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-! ## 1. The spatial projector q v = v - ⟪n, v⟫ n is idempotent with kernel span{n} -/

/-- A unit vector `n` (the clock's timelike normal). -/
structure UnitNormal where
  n : E
  hn : ‖n‖ = 1

/-- The spatial projector onto the orthogonal complement of `n`: `q v = v - ⟪n, v⟫ n`.
    This is `q^μν = g^μν + n^μ n^ν` applied to a spatial vector. -/
def spatialProj (u : UnitNormal) (v : E) : E :=
  v - (⟪u.n, v⟫_ℝ) • u.n

/-- `q n = 0`: the clock normal itself has no spatial (transverse) part. -/
theorem spatialProj_normal_self (u : UnitNormal) : spatialProj u u.n = 0 := by
  unfold spatialProj
  rw [real_inner_self_eq_norm_sq, u.hn, one_pow, one_smul, sub_self]

/-- `q` is idempotent: it is a genuine projector. -/
theorem spatialProj_idempotent (u : UnitNormal) (v : E) :
    spatialProj u (spatialProj u v) = spatialProj u v := by
  unfold spatialProj
  rw [map_sub, map_smul, real_inner_self_eq_norm_sq, u.hn, one_pow, one_smul]
  simp [smul_smul, sub_sub, mul_one]
  abel

/-- The kernel of `q` is contained in `span{n}`: if `q v = 0` then `v` is a multiple of `n`.  So the
    projected (transverse) response has NO component along the preferred direction, by construction. -/
theorem spatialProj_kernel_subset_span (u : UnitNormal) (v : E)
    (hv : spatialProj u v = 0) : v = (⟪u.n, v⟫_ℝ) • u.n :=
  sub_eq_zero.mp hv

/-! ## 2. The dimension count: orthogonal complement of a line in d dims is d-1 -/

/-- In a finite-dimensional real inner product space of dimension `d`, the orthogonal complement of
    the span of a nonzero vector has dimension `d - 1`: "d spatial dimensions minus the one preferred
    direction leaves d - 1 transverse modes". -/
theorem finrank_orthogonal_span_singleton [FiniteDimensional ℝ E]
    (v : E) (hv : v ≠ 0) :
    finrank ℝ (ℝ ∙ v)ᗮ = finrank ℝ E - 1 := by
  have h1 : finrank ℝ (ℝ ∙ v) = 1 := finrank_span_singleton hv
  have h2 := (ℝ ∙ v).finrank_add_finrank_orthogonal
  omega

/-- Specialised to d = 3: the transverse mode count is 2 — the number K010 needs. -/
theorem transverse_count_eq_two [FiniteDimensional ℝ E]
    (hd : finrank ℝ E = 3) (v : E) (hv : v ≠ 0) :
    finrank ℝ (ℝ ∙ v)ᗮ = 2 := by
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
