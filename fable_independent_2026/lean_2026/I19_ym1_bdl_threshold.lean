import Mathlib

/-!
# I19 — D-YM1: the explicit strong-coupling threshold (BDL extension to Kogut–Susskind SU(N))

SCOPE (per lean-math-certification): Lean certifies the NUMERIC CHAIN of the finite-volume gap theorem
in `real_research/ym1_bdl_extension_2026/DERIVATION.md`, from its formulas (E3)–(E11) to the thresholds.
The ANALYTIC lemmas (sector norm, Lemmas 1′–4′, Claim 3′, the Kirkwood–Thomas majorant, the
truncation/min–max limit) are proved in prose there and refereed adversarially (no error found), but
are NOT formalized here. Source adapted: Bravyi, DiVincenzo, Loss, "Polynomial-time algorithm for
simulation of weakly interacting quantum spin systems", CMP 284 (2008) 481, arXiv:0707.1894.

* `gamma0_sq_s4`, `gammaS_sq_s4` (and s = 3) — the sector sums (E3), (E4) as exact rationals.
* `q4_mono`, `q4d_mono` — the majorant polynomial q(μ) = β₀ + Σ_{k=1}^{8} β_k μ^k/k! with
  β_k = 2^k(γ₀ 4^k + k γ_S 4^{k−1}) (E5–E6) and its derivative are monotone in (γ₀, γ_S) for μ ≥ 0.
* `threshold_s4`, `threshold_s3` — THE CERTIFICATE (E7–E9) at the true γ's (√ of the exact sums):
  μ_c − λ_c q(μ_c) ≥ 0 (so ‖C‖₁ ≤ μ_c) and 2 λ_c q′(μ_c) < 1 (gap ≥ Δ/2), with
  λ_c(4) = 2977072941/250000000000 ≈ 0.0119083 and λ_c(3) = 17904018857/10^12 ≈ 0.0179040.
* `eps_uniform` — ε = 2b_N/(x²C_F) ≤ 32/(3x²) for all N ≥ 2, 0 ≤ b_N ≤ 2N (C_F = (N²−1)/(2N)).
* `Xd_link_d2`, `Xd_link_d3`, `Xd_link_d4` — for x ≥ 42.34 / 59.87 / 73.32 the normalized coupling
  λ = ε·D ≤ λ_c(4) (link grouping, D = 2(d−1)): the thresholds X₂ ≈ 42.3, X₃ ≈ 59.9, X₄ ≈ 73.3.
* `bdl_erratum_constant` — BDL App. A's constant survives their erratum (|M_j| ≤ 3|M|, not 2|M|):
  max_{k≤4} (3k·2^{2k+1} + 2^{2k+2}) = 7168 ≤ 2^13.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- β_k for s = 4 sites per plaquette. -/
def b4 (g0 gS : ℝ) (k : ℕ) : ℝ := 2 ^ k * (g0 * 4 ^ k + k * gS * 4 ^ (k - 1))

/-- The majorant polynomial (E6), s = 4, depth 2s = 8. -/
def q4 (g0 gS μ : ℝ) : ℝ :=
  g0 + b4 g0 gS 1 * μ + b4 g0 gS 2 * μ ^ 2 / 2 + b4 g0 gS 3 * μ ^ 3 / 6 + b4 g0 gS 4 * μ ^ 4 / 24 +
    b4 g0 gS 5 * μ ^ 5 / 120 + b4 g0 gS 6 * μ ^ 6 / 720 + b4 g0 gS 7 * μ ^ 7 / 5040 +
    b4 g0 gS 8 * μ ^ 8 / 40320

/-- Its derivative in μ. -/
def q4d (g0 gS μ : ℝ) : ℝ :=
  b4 g0 gS 1 + b4 g0 gS 2 * μ + b4 g0 gS 3 * μ ^ 2 / 2 + b4 g0 gS 4 * μ ^ 3 / 6 +
    b4 g0 gS 5 * μ ^ 4 / 24 + b4 g0 gS 6 * μ ^ 5 / 120 + b4 g0 gS 7 * μ ^ 6 / 720 +
    b4 g0 gS 8 * μ ^ 7 / 5040

/-- β_k for s = 3 (vertex grouping), depth 6. -/
def b3 (g0 gS : ℝ) (k : ℕ) : ℝ := 2 ^ k * (g0 * 3 ^ k + k * gS * 3 ^ (k - 1))

def q3 (g0 gS μ : ℝ) : ℝ :=
  g0 + b3 g0 gS 1 * μ + b3 g0 gS 2 * μ ^ 2 / 2 + b3 g0 gS 3 * μ ^ 3 / 6 + b3 g0 gS 4 * μ ^ 4 / 24 +
    b3 g0 gS 5 * μ ^ 5 / 120 + b3 g0 gS 6 * μ ^ 6 / 720

def q3d (g0 gS μ : ℝ) : ℝ :=
  b3 g0 gS 1 + b3 g0 gS 2 * μ + b3 g0 gS 3 * μ ^ 2 / 2 + b3 g0 gS 4 * μ ^ 3 / 6 +
    b3 g0 gS 5 * μ ^ 4 / 24 + b3 g0 gS 6 * μ ^ 5 / 120

/-- (E3), s = 4: Σ_{t=1}^{4} C(3,t−1)/t² = 103/48. -/
theorem gamma0_sq_s4 : ((1 : ℚ) + 3 / 2 ^ 2 + 3 / 3 ^ 2 + 1 / 4 ^ 2) = 103 / 48 := by norm_num
/-- (E4), s = 4: 5² Σ_{t=0}^{4} C(4,t)/(t+1)² = 887/12. -/
theorem gammaS_sq_s4 : ((5 : ℚ) ^ 2 * (1 + 4 / 2 ^ 2 + 6 / 3 ^ 2 + 4 / 4 ^ 2 + 1 / 5 ^ 2)) = 887 / 12 := by
  norm_num
/-- (E3), s = 3: Σ_{t=1}^{3} C(2,t−1)/t² = 29/18. -/
theorem gamma0_sq_s3 : ((1 : ℚ) + 2 / 2 ^ 2 + 1 / 3 ^ 2) = 29 / 18 := by norm_num
/-- (E4), s = 3: 4² Σ_{t=0}^{3} C(3,t)/(t+1)² = 103/3. -/
theorem gammaS_sq_s3 : ((4 : ℚ) ^ 2 * (1 + 3 / 2 ^ 2 + 3 / 3 ^ 2 + 1 / 4 ^ 2)) = 103 / 3 := by norm_num

lemma b4_mono {g0 gS g0' gS' : ℝ} (h0 : g0 ≤ g0') (hS : gS ≤ gS') (k : ℕ) :
    b4 g0 gS k ≤ b4 g0' gS' k := by
  unfold b4
  gcongr

lemma b3_mono {g0 gS g0' gS' : ℝ} (h0 : g0 ≤ g0') (hS : gS ≤ gS') (k : ℕ) :
    b3 g0 gS k ≤ b3 g0' gS' k := by
  unfold b3
  gcongr

theorem q4_mono {g0 gS g0' gS' μ : ℝ} (h0 : g0 ≤ g0') (hS : gS ≤ gS') (hμ : 0 ≤ μ) :
    q4 g0 gS μ ≤ q4 g0' gS' μ := by
  have hb := fun k => b4_mono h0 hS k
  unfold q4
  gcongr <;> exact hb _

theorem q4d_mono {g0 gS g0' gS' μ : ℝ} (h0 : g0 ≤ g0') (hS : gS ≤ gS') (hμ : 0 ≤ μ) :
    q4d g0 gS μ ≤ q4d g0' gS' μ := by
  have hb := fun k => b4_mono h0 hS k
  unfold q4d
  gcongr <;> exact hb _

theorem q3_mono {g0 gS g0' gS' μ : ℝ} (h0 : g0 ≤ g0') (hS : gS ≤ gS') (hμ : 0 ≤ μ) :
    q3 g0 gS μ ≤ q3 g0' gS' μ := by
  have hb := fun k => b3_mono h0 hS k
  unfold q3
  gcongr <;> exact hb _

theorem q3d_mono {g0 gS g0' gS' μ : ℝ} (h0 : g0 ≤ g0') (hS : gS ≤ gS') (hμ : 0 ≤ μ) :
    q3d g0 gS μ ≤ q3d g0' gS' μ := by
  have hb := fun k => b3_mono h0 hS k
  unfold q3d
  gcongr <;> exact hb _

lemma sqrt_le_of_sq {x u : ℝ} (hu : 0 ≤ u) (h : x ≤ u ^ 2) : Real.sqrt x ≤ u := by
  calc Real.sqrt x ≤ Real.sqrt (u ^ 2) := Real.sqrt_le_sqrt h
    _ = u := Real.sqrt_sq hu

/-- The certified rationals. -/
def LAM4 : ℝ := 2977072941 / 250000000000
def MU4 : ℝ := 7714031583367 / 257393552939521
def LAM3 : ℝ := 17904018857 / 1000000000000
def MU3 : ℝ := 14377156102957 / 367568212348887

/-- THE CERTIFICATE, s = 4 (link sites): at the true γ's, μ_c ≥ λ_c q(μ_c) and 2 λ_c q′(μ_c) < 1. -/
theorem threshold_s4 :
    0 ≤ MU4 - LAM4 * q4 (Real.sqrt (103 / 48)) (Real.sqrt (887 / 12)) MU4 ∧
      2 * LAM4 * q4d (Real.sqrt (103 / 48)) (Real.sqrt (887 / 12)) MU4 < 1 := by
  have hg0 : Real.sqrt (103 / 48) ≤ 1464866319270579 / 1000000000000000 :=
    sqrt_le_of_sq (by norm_num) (by norm_num)
  have hgS : Real.sqrt (887 / 12) ≤ 1074685031377411 / 125000000000000 :=
    sqrt_le_of_sq (by norm_num) (by norm_num)
  have hmu : (0 : ℝ) ≤ MU4 := by unfold MU4; norm_num
  have hlam : (0 : ℝ) ≤ LAM4 := by unfold LAM4; norm_num
  have h1 := mul_le_mul_of_nonneg_left (q4_mono hg0 hgS hmu) hlam
  have h2 := mul_le_mul_of_nonneg_left (q4d_mono hg0 hgS hmu) hlam
  have c1 : 0 ≤ MU4 - LAM4 * q4 (1464866319270579 / 1000000000000000)
      (1074685031377411 / 125000000000000) MU4 := by
    unfold MU4 LAM4 q4 b4; norm_num
  have c2 : 2 * LAM4 * q4d (1464866319270579 / 1000000000000000)
      (1074685031377411 / 125000000000000) MU4 < 1 := by
    unfold MU4 LAM4 q4d b4; norm_num
  constructor
  · linarith
  · linarith

/-- THE CERTIFICATE, s = 3 (vertex sites). -/
theorem threshold_s3 :
    0 ≤ MU3 - LAM3 * q3 (Real.sqrt (29 / 18)) (Real.sqrt (103 / 3)) MU3 ∧
      2 * LAM3 * q3d (Real.sqrt (29 / 18)) (Real.sqrt (103 / 3)) MU3 < 1 := by
  have hg0 : Real.sqrt (29 / 18) ≤ 253859103528797 / 200000000000000 :=
    sqrt_le_of_sq (by norm_num) (by norm_num)
  have hgS : Real.sqrt (103 / 3) ≤ 1464866319270579 / 250000000000000 :=
    sqrt_le_of_sq (by norm_num) (by norm_num)
  have hmu : (0 : ℝ) ≤ MU3 := by unfold MU3; norm_num
  have hlam : (0 : ℝ) ≤ LAM3 := by unfold LAM3; norm_num
  have h1 := mul_le_mul_of_nonneg_left (q3_mono hg0 hgS hmu) hlam
  have h2 := mul_le_mul_of_nonneg_left (q3d_mono hg0 hgS hmu) hlam
  have c1 : 0 ≤ MU3 - LAM3 * q3 (253859103528797 / 200000000000000)
      (1464866319270579 / 250000000000000) MU3 := by
    unfold MU3 LAM3 q3 b3; norm_num
  have c2 : 2 * LAM3 * q3d (253859103528797 / 200000000000000)
      (1464866319270579 / 250000000000000) MU3 < 1 := by
    unfold MU3 LAM3 q3d b3; norm_num
  constructor
  · linarith
  · linarith

/-- ε = 2 b_N /(x² C_F) ≤ 32/(3x²) for all N ≥ 2 and 0 ≤ b_N ≤ 2N (C_F = (N²−1)/(2N)). -/
theorem eps_uniform {N b x : ℝ} (hN : 2 ≤ N) (hb0 : 0 ≤ b) (hb : b ≤ 2 * N) (hx : 0 < x) :
    2 * b / (x ^ 2 * ((N ^ 2 - 1) / (2 * N))) ≤ 32 / (3 * x ^ 2) := by
  have hN0 : 0 < N := by linarith
  have hN2 : 0 < N ^ 2 - 1 := by nlinarith
  have hx2 : 0 < x ^ 2 := by positivity
  have e : 2 * b / (x ^ 2 * ((N ^ 2 - 1) / (2 * N))) = 4 * b * N / (x ^ 2 * (N ^ 2 - 1)) := by
    field_simp
    ring
  rw [e, div_le_div_iff₀ (by positivity) (by positivity)]
  have h1 : b * N ≤ 2 * N * N := by nlinarith
  have h2 : 12 * b * N ≤ 32 * N ^ 2 - 32 := by nlinarith
  have h3 := mul_le_mul_of_nonneg_left h2 hx2.le
  nlinarith [h3]

/-- d = 2, link grouping (D = 2): x ≥ 42.34 ⟹ (32/3)·2/x² ≤ λ_c(4). -/
theorem Xd_link_d2 {x : ℝ} (hx : 42.34 ≤ x) :
    32 / (3 * x ^ 2) * 2 ≤ (2977072941 / 250000000000 : ℝ) := by
  have hx2 : (42.34 : ℝ) ^ 2 ≤ x ^ 2 := by gcongr
  rw [div_mul_eq_mul_div, div_le_iff₀ (by positivity)]
  nlinarith

/-- d = 3, link grouping (D = 4): x ≥ 59.87. -/
theorem Xd_link_d3 {x : ℝ} (hx : 59.87 ≤ x) :
    32 / (3 * x ^ 2) * 4 ≤ (2977072941 / 250000000000 : ℝ) := by
  have hx2 : (59.87 : ℝ) ^ 2 ≤ x ^ 2 := by gcongr
  rw [div_mul_eq_mul_div, div_le_iff₀ (by positivity)]
  nlinarith

/-- d = 4, link grouping (D = 6): x ≥ 73.32. -/
theorem Xd_link_d4 {x : ℝ} (hx : 73.32 ≤ x) :
    32 / (3 * x ^ 2) * 6 ≤ (2977072941 / 250000000000 : ℝ) := by
  have hx2 : (73.32 : ℝ) ^ 2 ≤ x ^ 2 := by gcongr
  rw [div_mul_eq_mul_div, div_le_iff₀ (by positivity)]
  nlinarith

/-- BDL App. A erratum: with |M_j| ≤ 3|M| the per-order constant max_{k≤4}(3k·2^{2k+1}+2^{2k+2})
is 7168, still ≤ 2^13 = 8192 — their Theorem 1 constant survives. -/
theorem bdl_erratum_constant :
    (∀ k ∈ Finset.Icc 1 4, 3 * k * 2 ^ (2 * k + 1) + 2 ^ (2 * k + 2) ≤ 7168) ∧
      3 * 4 * 2 ^ (2 * 4 + 1) + 2 ^ (2 * 4 + 2) = 7168 ∧ (7168 : ℕ) ≤ 2 ^ 13 := by
  refine ⟨?_, by norm_num, by norm_num⟩
  decide

end

#print axioms threshold_s4
#print axioms threshold_s3
#print axioms q4_mono
#print axioms eps_uniform
#print axioms Xd_link_d2
#print axioms Xd_link_d3
#print axioms Xd_link_d4
#print axioms bdl_erratum_constant
#print axioms gamma0_sq_s4
#print axioms gammaS_sq_s4
