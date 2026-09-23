import Mathlib

/-!
# I24 — The khronon's c₂ channel carries a moving phantom; the price lands on the aether's acceleration

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs are hypotheses: the linearised
khronometric system (β = 0, unitary gauge, k along the steady flow; its derivation from the action is the symbolic
check A1 of the companion lane), a source moving steadily through the preferred frame (ω = k·v), and a MOND-sector
phantom that enters the lapse equation with no momentum (L330 M1). Companion lane:
`real_research/g03_audit_2026/L333_c2_channel_carries_the_phantom.py`.

Variables: `n` lapse, `ψ` conformal factor, `b = i·B` (the longitudinal shift, made real), `P = 1/(16πG)`,
`α = c₁₄`, `ε = c₂`, sources ρ_m (baryons), ρ_ph (phantom), J = k·J (baryon momentum), Sij (stress).

* `moving_solution` — the explicit (n, ψ, b) solves the three linear equations exactly (Hamiltonian, trace-evolution,
  momentum), whenever the determinant Δ = αεk² + α(3ε+2)ω² − 2εk² is nonzero.
* `phantom_lapse_ratio`, `phantom_bardeen_ratio` — for the momentless phantom alone:
  n(ω)/n(0) − 1 = 2(3ε+2)x / (ε(2−α) − α(3ε+2)x) and Φ_B(ω)/n(0) − 1 = α(3ε+2)x / (ε(2−α) − α(3ε+2)x), x = ω²/k².
* `aether_vs_matter` — **the exact ratio: the aether-acceleration (MOND-input) distortion is 2/α times the
  distortion of the potential matter feels, at every speed.** With α = c₁₄ ≲ 1e-5 the input distortion is
  ≳ 2×10⁵ times the dynamical one.
* `yagi_alpha2_beta0` — Yagi–Blas–Barausse–Yunes 2014 eq. 49 at β = 0 equals α(α − λ + 2αλ)/(λ(2 − α)).
* `deep_mond_chi_*`, `deep_mond_isotropic` — for Φ_ph = ln r (deep MOND, V² = 1) the regular inverse Laplacian is
  χ = r²(ln r − 5/6)/6; its radial derivatives give an ISOTROPIC radial input distortion 1/(3r) and a tilt
  (χ'' − χ'/r)/r = 1/(3r): the "D/3" of the companion lane.
* `corner_distortion` — at c₁₄ = c₂ = 1e-5 and v = 620 km/s the body-frame coefficient C_ph v² / 3 exceeds 0.28.
* `branch_alpha2` — at c₁₄ = 8e-7, c₂ = 1e-3 the literature |α₂| is below 4e-7.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

/-- The three linear equations (k along the flow, b = i·B real). -/
def eqH (P k α n ψ ρm ρp : ℝ) : Prop := P * (2 * k ^ 2 * (α * n - 2 * ψ)) = ρm + ρp
def eqE (P k ω ε n ψ b Sij : ℝ) : Prop :=
  P * ((6 * ε + 4) * k ^ 2 * ω * b - 4 * k ^ 2 * n - (18 * ε + 12) * ω ^ 2 * ψ + 4 * k ^ 2 * ψ) = Sij
def eqM (P k ω ε ψ b J : ℝ) : Prop := P * (-2 * ε * k ^ 4 * b + (6 * ε + 4) * k ^ 2 * ω * ψ) = -J

def Δ (k ω α ε : ℝ) : ℝ := α * ε * k ^ 2 + 3 * α * ε * ω ^ 2 + 2 * α * ω ^ 2 - 2 * ε * k ^ 2

def nSol (P k ω α ε ρm ρp J Sij : ℝ) : ℝ :=
  (-3 * J * ε * ω - 2 * J * ω + Sij * ε * k ^ 2 + ε * k ^ 2 * ρm + ε * k ^ 2 * ρp + 3 * ε * ρm * ω ^ 2
    + 3 * ε * ρp * ω ^ 2 + 2 * ρm * ω ^ 2 + 2 * ρp * ω ^ 2) / (2 * P * k ^ 2 * Δ k ω α ε)
def ψSol (P k ω α ε ρm ρp J Sij : ℝ) : ℝ :=
  -(3 * J * α * ε * ω + 2 * J * α * ω - Sij * α * ε * k ^ 2 - 2 * ε * k ^ 2 * ρm - 2 * ε * k ^ 2 * ρp)
    / (4 * P * k ^ 2 * Δ k ω α ε)
def bSol (P k ω α ε ρm ρp J Sij : ℝ) : ℝ :=
  -(9 * J * α * ε * ω ^ 2 - 2 * J * α * k ^ 2 + 6 * J * α * ω ^ 2 + 4 * J * k ^ 2 - 3 * Sij * α * ε * k ^ 2 * ω
    - 2 * Sij * α * k ^ 2 * ω - 6 * ε * k ^ 2 * ρm * ω - 6 * ε * k ^ 2 * ρp * ω - 4 * k ^ 2 * ρm * ω
    - 4 * k ^ 2 * ρp * ω) / (4 * P * k ^ 4 * Δ k ω α ε)

theorem moving_solution {P k ω α ε ρm ρp J Sij : ℝ} (hP : P ≠ 0) (hk : k ≠ 0) (hΔ : Δ k ω α ε ≠ 0) :
    eqH P k α (nSol P k ω α ε ρm ρp J Sij) (ψSol P k ω α ε ρm ρp J Sij) ρm ρp ∧
    eqE P k ω ε (nSol P k ω α ε ρm ρp J Sij) (ψSol P k ω α ε ρm ρp J Sij) (bSol P k ω α ε ρm ρp J Sij) Sij ∧
    eqM P k ω ε (ψSol P k ω α ε ρm ρp J Sij) (bSol P k ω α ε ρm ρp J Sij) J := by
  unfold eqH eqE eqM nSol ψSol bSol
  refine ⟨?_, ?_, ?_⟩
  · field_simp; unfold Δ; ring
  · field_simp; unfold Δ; ring
  · field_simp; unfold Δ; ring

lemma Δ_zero {k α ε : ℝ} : Δ k 0 α ε = ε * k ^ 2 * (α - 2) := by unfold Δ; ring

lemma Δ_neg {k ω α ε : ℝ} : ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2 = -Δ k ω α ε := by unfold Δ; ring

/-- Momentless phantom alone: the lapse (the aether's acceleration potential) relative to its static value;
x = ω²/k² multiplied through. -/
theorem phantom_lapse_ratio {P k ω α ε ρp : ℝ} (hP : P ≠ 0) (hk : k ≠ 0) (hρ : ρp ≠ 0) (hε : ε ≠ 0)
    (hα : α ≠ 2) (hΔ : Δ k ω α ε ≠ 0) :
    nSol P k ω α ε 0 ρp 0 0 / nSol P k 0 α ε 0 ρp 0 0 - 1
      = 2 * (3 * ε + 2) * ω ^ 2 / (ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2) := by
  have ha2 : α - 2 ≠ 0 := sub_ne_zero.mpr hα
  have hΔ0 : Δ k 0 α ε ≠ 0 := by rw [Δ_zero]; exact mul_ne_zero (mul_ne_zero hε (pow_ne_zero 2 hk)) ha2
  have hden : ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2 ≠ 0 := by rw [Δ_neg]; exact neg_ne_zero.mpr hΔ
  unfold nSol
  rw [Δ_neg, Δ_zero]
  field_simp
  unfold Δ
  ring

/-- Momentless phantom alone: the Bardeen potential matter feels, Φ_B = n − ω b. -/
theorem phantom_bardeen_ratio {P k ω α ε ρp : ℝ} (hP : P ≠ 0) (hk : k ≠ 0) (hρ : ρp ≠ 0) (hε : ε ≠ 0)
    (hα : α ≠ 2) (hΔ : Δ k ω α ε ≠ 0) :
    (nSol P k ω α ε 0 ρp 0 0 - ω * bSol P k ω α ε 0 ρp 0 0) / nSol P k 0 α ε 0 ρp 0 0 - 1
      = α * (3 * ε + 2) * ω ^ 2 / (ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2) := by
  have ha2 : α - 2 ≠ 0 := sub_ne_zero.mpr hα
  have hden : ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2 ≠ 0 := by rw [Δ_neg]; exact neg_ne_zero.mpr hΔ
  unfold nSol bSol
  rw [Δ_neg, Δ_zero]
  field_simp
  unfold Δ
  ring

/-- THE EXACT RATIO: the aether-acceleration distortion is 2/α times the dynamical one, at every speed. -/
theorem aether_vs_matter {α ε ω k : ℝ} (hα : α ≠ 0)
    (hden : ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2 ≠ 0) :
    2 * (3 * ε + 2) * ω ^ 2 / (ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2)
      = (2 / α) * (α * (3 * ε + 2) * ω ^ 2 / (ε * (2 - α) * k ^ 2 - α * (3 * ε + 2) * ω ^ 2)) := by
  field_simp

/-- Yagi et al. 2014 eq. 49 at β = 0. -/
theorem yagi_alpha2_beta0 {α lam : ℝ} (hlam : lam ≠ 0) (hα : α ≠ 2) :
    (α - 2 * 0) * (-(0 : ℝ) ^ 2 + 0 * (α - 3) + α + lam * (-1 - 3 * 0 + 2 * α)) / ((0 - 1) * (lam + 0) * (α - 2))
      = α * (α - lam + 2 * α * lam) / (lam * (2 - α)) := by
  have h2 : (2 : ℝ) - α ≠ 0 := sub_ne_zero.mpr (Ne.symm hα)
  have h3 : α - 2 ≠ 0 := sub_ne_zero.mpr hα
  have hL : ((0 : ℝ) - 1) * (lam + 0) * (α - 2) ≠ 0 := by
    have : ((0 : ℝ) - 1) * (lam + 0) * (α - 2) = -(lam * (α - 2)) := by ring
    rw [this]; exact neg_ne_zero.mpr (mul_ne_zero hlam h3)
  rw [div_eq_div_iff hL (mul_ne_zero hlam h2)]
  ring

/-! ### The deep-MOND closed form (Φ_ph = ln r, V² = 1) -/

def χ (r : ℝ) : ℝ := r ^ 2 * (Real.log r - 5 / 6) / 6
def χ1 (r : ℝ) : ℝ := r / 3 * (Real.log r - 1 / 3)
def χ2 (r : ℝ) : ℝ := Real.log r / 3 + 2 / 9

theorem deep_mond_chi_d1 {r : ℝ} (hr : 0 < r) : HasDerivAt χ (χ1 r) r := by
  have hl : HasDerivAt Real.log r⁻¹ r := Real.hasDerivAt_log hr.ne'
  have h := ((hasDerivAt_pow 2 r).mul (hl.sub_const (5 / 6))).div_const 6
  show HasDerivAt (fun x => x ^ 2 * (Real.log x - 5 / 6) / 6) (χ1 r) r
  refine h.congr_deriv ?_
  unfold χ1; field_simp; ring

theorem deep_mond_chi_d2 {r : ℝ} (hr : 0 < r) : HasDerivAt χ1 (χ2 r) r := by
  have hl : HasDerivAt Real.log r⁻¹ r := Real.hasDerivAt_log hr.ne'
  have h := ((hasDerivAt_id r).div_const 3).mul (hl.sub_const (1 / 3))
  show HasDerivAt (fun x => id x / 3 * (Real.log x - 1 / 3)) (χ2 r) r
  refine h.congr_deriv ?_
  unfold χ2; simp only [id]; field_simp; ring

theorem deep_mond_chi_d3 {r : ℝ} (hr : 0 < r) : HasDerivAt χ2 (1 / (3 * r)) r := by
  have hl : HasDerivAt Real.log r⁻¹ r := Real.hasDerivAt_log hr.ne'
  have h := (hl.div_const 3).add_const (2 / 9)
  show HasDerivAt (fun x => Real.log x / 3 + 2 / 9) (1 / (3 * r)) r
  refine h.congr_deriv ?_
  field_simp

/-- The spherical Laplacian of χ is ln r (χ is the regular inverse Laplacian of the deep-MOND phantom potential). -/
theorem deep_mond_laplacian {r : ℝ} (hr : 0 < r) : χ2 r + 2 * χ1 r / r = Real.log r := by
  unfold χ1 χ2; field_simp; ring

/-- The radial and tangential input distortions of (v̂·∇)²χ are both 1/(3r): isotropic in the radial part. -/
theorem deep_mond_isotropic {r θ : ℝ} (hr : 0 < r) :
    Real.cos θ ^ 2 * (1 / (3 * r)) + Real.sin θ ^ 2 * (χ2 r / r - χ1 r / r ^ 2) = 1 / (3 * r) ∧
    (χ2 r - χ1 r / r) / r = 1 / (3 * r) := by
  have hr0 : r ≠ 0 := hr.ne'
  have key : χ2 r / r - χ1 r / r ^ 2 = 1 / (3 * r) := by unfold χ1 χ2; field_simp; ring
  refine ⟨?_, ?_⟩
  · rw [key, ← add_mul, Real.cos_sq_add_sin_sq, one_mul]
  · unfold χ1 χ2; field_simp; ring

/-! ### The branch numbers -/

/-- At c₁₄ = c₂ = 1e-5 and v = 620 km/s: C_ph v²/3 > 0.28 with C_ph = (4 + 4c₂ + c₁₄c₂)/(c₂(2 − c₁₄)). -/
theorem corner_distortion :
    (4 + 4 * (1e-5 : ℝ) + 1e-5 * 1e-5) / (1e-5 * (2 - 1e-5)) * (620 / 299792.458) ^ 2 / 3 > 0.28 := by
  norm_num

/-- At c₁₄ = 8e-7, c₂ = 1e-3 the literature α₂ satisfies |α₂| < 4e-7. -/
theorem branch_alpha2 :
    |(8e-7 : ℝ) * (8e-7 - 1e-3 + 2 * 8e-7 * 1e-3) / (1e-3 * (2 - 8e-7))| < 4e-7 := by
  rw [abs_lt]; constructor <;> norm_num

end

#print axioms moving_solution
#print axioms Δ_zero
#print axioms Δ_neg
#print axioms phantom_lapse_ratio
#print axioms phantom_bardeen_ratio
#print axioms aether_vs_matter
#print axioms yagi_alpha2_beta0
#print axioms deep_mond_chi_d1
#print axioms deep_mond_chi_d2
#print axioms deep_mond_chi_d3
#print axioms deep_mond_laplacian
#print axioms deep_mond_isotropic
#print axioms corner_distortion
#print axioms branch_alpha2
