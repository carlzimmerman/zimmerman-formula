import Mathlib

/-!
# L357–L361 — the vacuum gate and the bound-region kernel: algebraic certificates

SCOPE. Lean certifies the algebra behind `real_research/g03_audit_2026/L359_vacuum_gated_switch.py` (the gated MOND
switch), `real_research/dark_sector_2026/L357_virialization_triggered_carrier.py` (the gated carrier) and
`real_research/g03_audit_2026/L360_assembled_construction_kids.py`.  The forest, KiDS, growth, S_8, X-COP and galaxy
numbers are computed in those lanes, not here.

* `omegaL_khronon`: on flat FRW with K = 3H (c = 1), Omega_Lambda = Lambda/(3H^2) equals 3 Lambda/K^2 — the gate
  [Omega_Lambda/Omega_Lambda,0]^p is a function of the khronon's mean curvature K alone.
* `tt_mode_trace_free`: the TT metric diag(e^h, e^-h, 1) has unit determinant, so K = d/dt ln sqrt(det) vanishes for a
  tensor mode and the gate is tensor-blind (L351's c_T = 1 carries over).
* `constant_threshold_pincer`: if KiDS needs x_c <= X_K and the forest needs x_c >= X_F with X_K < X_F, no constant
  threshold satisfies both (the L352/L358 pincer).
* `gated_threshold_window`: a threshold x_c(z) = x_c0 g(z) with g(z_K), X_K > 0 satisfies both whenever the gate ratio
  g(z_F)/g(z_K) is at least X_F/X_K (take x_c0 = X_K/g(z_K)).
* `gate_increasing`: for p > 0 and 1 <= E1 <= E2 the gate E^(2p) is monotone, so the threshold rises into the matter era.
* `triggered_fraction_monotone`: the NFW enclosed-mass shape m(y) = log(1+y) - y/(1+y) is monotone on y >= 0, so the
  triggered fraction m(y_v)/m(c) falls as the threshold rises (y_v falls).
* `bound_region_phantom_equation` (L361): for any linear operator L (the Laplacian) and screening M^2, if
  (L - M^2) psi = L w + D and chi solves the same screened equation as w, then the phantom P = psi - chi obeys
  (L - M^2) P = D + M^2 w — the region-local phantom plus the thin screened edge layer M^2 w.
-/

theorem omegaL_khronon (H Λ : ℝ) (hH : H ≠ 0) : Λ / (3 * H ^ 2) = 3 * Λ / (3 * H) ^ 2 := by
  field_simp

theorem tt_mode_trace_free (h : ℝ) : Real.exp h * Real.exp (-h) * 1 = 1 := by
  rw [mul_one, ← Real.exp_add, add_neg_cancel, Real.exp_zero]

theorem constant_threshold_pincer (XK XF : ℝ) (h : XK < XF) : ¬ ∃ x : ℝ, x ≤ XK ∧ XF ≤ x := by
  rintro ⟨x, hx1, hx2⟩
  linarith

theorem gated_threshold_window (XK XF gK gF : ℝ) (hXK : 0 < XK) (hgK : 0 < gK)
    (hratio : XF / XK ≤ gF / gK) : ∃ x0 : ℝ, x0 * gK ≤ XK ∧ XF ≤ x0 * gF := by
  refine ⟨XK / gK, ?_, ?_⟩
  · rw [div_mul_cancel₀ XK (ne_of_gt hgK)]
  · have h1 : XF ≤ gF / gK * XK := by
      have := mul_le_mul_of_nonneg_right hratio (le_of_lt hXK)
      rwa [div_mul_cancel₀ XF (ne_of_gt hXK)] at this
    calc XF ≤ gF / gK * XK := h1
      _ = XK / gK * gF := by ring

theorem gate_increasing (p E1 E2 : ℝ) (hp : 0 < p) (h1 : 1 ≤ E1) (h12 : E1 ≤ E2) :
    E1 ^ (2 * p) ≤ E2 ^ (2 * p) := by
  apply Real.rpow_le_rpow (by linarith) h12 (by linarith)

theorem triggered_fraction_monotone (y1 y2 : ℝ) (h0 : 0 ≤ y1) (h12 : y1 ≤ y2) :
    Real.log (1 + y1) - y1 / (1 + y1) ≤ Real.log (1 + y2) - y2 / (1 + y2) := by
  -- d/dy [log(1+y) - y/(1+y)] = y/(1+y)^2 >= 0 on y >= 0
  have hmono : MonotoneOn (fun y : ℝ => Real.log (1 + y) - y / (1 + y)) (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
    · apply ContinuousOn.sub
      · apply ContinuousOn.log (by fun_prop)
        intro y hy; simp only [Set.mem_Ici] at hy; linarith
      · apply ContinuousOn.div (by fun_prop) (by fun_prop)
        intro y hy; simp only [Set.mem_Ici] at hy; linarith
    · apply DifferentiableOn.sub
      · apply DifferentiableOn.log (by fun_prop)
        intro y hy; simp only [interior_Ici, Set.mem_Ioi] at hy; linarith
      · apply DifferentiableOn.div (by fun_prop) (by fun_prop)
        intro y hy; simp only [interior_Ici, Set.mem_Ioi] at hy; linarith
    · intro y hy
      simp only [interior_Ici, Set.mem_Ioi] at hy
      have hy1 : (1 + y) ≠ 0 := by linarith
      have hd : deriv (fun y : ℝ => Real.log (1 + y) - y / (1 + y)) y = y / (1 + y) ^ 2 := by
        have h1 : HasDerivAt (fun y : ℝ => Real.log (1 + y)) (1 / (1 + y)) y := by
          have := ((hasDerivAt_id y).const_add 1).log hy1
          simpa using this
        have h2 : HasDerivAt (fun y : ℝ => y / (1 + y)) ((1 * (1 + y) - y * 1) / (1 + y) ^ 2) y := by
          exact (hasDerivAt_id y).div ((hasDerivAt_id y).const_add 1) hy1
        have h3 : HasDerivAt (fun y : ℝ => Real.log (1 + y) - y / (1 + y))
            (1 / (1 + y) - (1 * (1 + y) - y * 1) / (1 + y) ^ 2) y := h1.sub h2
        rw [h3.deriv]
        field_simp
        ring
      rw [hd]
      positivity
  exact hmono (Set.mem_Ici.mpr h0) (Set.mem_Ici.mpr (le_trans h0 h12)) h12

theorem bound_region_phantom_equation {V : Type*} [AddCommGroup V] [Module ℝ V] (L : V →ₗ[ℝ] V) (M2 : ℝ)
    (w ψ χ D : V) (hψ : L ψ - M2 • ψ = L w + D) (hχ : L χ - M2 • χ = L w - M2 • w) :
    L (ψ - χ) - M2 • (ψ - χ) = D + M2 • w := by
  rw [map_sub, smul_sub]
  have : L ψ - L χ - (M2 • ψ - M2 • χ) = (L ψ - M2 • ψ) - (L χ - M2 • χ) := by abel
  rw [this, hψ, hχ]
  abel
