import Mathlib

/-!
AS147 -- diagonal U(1) Noether current of the five-field carrier.
Algebraic certificates (pure ring identities over ℝ).  Each theorem certifies one
factor/sign identity of the derivation:

  J^μ = J_φ^μ + J_χ^μ,   J_ψ^μ = ε_ab ψ_a C^μν ∂_ν ψ_b,
  div J_φ = +E,  div J_χ = -E,  div J_total = 0,
  E = B γ m_L² s (φ1 χ2 - φ2 χ1),   V = ½m_H²|φ|² + ½m_L²|χ+γsφ|² + ½μ²s²,
  C^{μν} symmetric (h^{μν} - n^μ n^ν at t = 1),  B := t^{-1}.
-/
noncomputable section

-- E (exchange source) at B = 1
def exch (γ s mL2 φ1 φ2 χ1 χ2 : ℝ) : ℝ := γ * mL2 * s * (φ1 * χ2 - φ2 * χ1)

-- 1. phi-side source equals +E  (div J_φ = +E on shell)
theorem exchange_phi
    (φ1 φ2 χ1 χ2 s γ mH2 mL2 : ℝ) :
    φ1 * (mH2 * φ2 + γ * mL2 * s * (χ2 + γ * s * φ2))
      - φ2 * (mH2 * φ1 + γ * mL2 * s * (χ1 + γ * s * φ1))
    = exch γ s mL2 φ1 φ2 χ1 χ2 := by
  unfold exch
  ring

-- 2. chi-side source equals -E  (div J_χ = -E on shell)
theorem exchange_chi
    (φ1 φ2 χ1 χ2 s γ mL2 : ℝ) :
    χ1 * (mL2 * (χ2 + γ * s * φ2)) - χ2 * (mL2 * (χ1 + γ * s * φ1))
    = -exch γ s mL2 φ1 φ2 χ1 χ2 := by
  unfold exch
  ring

-- 3. total source pair cancels: div J_total = 0
theorem exchange_pair_cancels
    (φ1 φ2 χ1 χ2 s γ mH2 mL2 : ℝ) :
    (φ1 * (mH2 * φ2 + γ * mL2 * s * (χ2 + γ * s * φ2))
       - φ2 * (mH2 * φ1 + γ * mL2 * s * (χ1 + γ * s * φ1)))
    + (χ1 * (mL2 * (χ2 + γ * s * φ2)) - χ2 * (mL2 * (χ1 + γ * s * φ1)))
    = 0 := by
  ring

-- 4. diagonal (mass) terms are antisymmetric: no self-source
theorem diag_mass_antisym (mH2 φ1 φ2 : ℝ) : φ1 * (mH2 * φ2) - φ2 * (mH2 * φ1) = 0 := by
  ring

-- 5. collinear chi = λ φ  =>  E = 0 identically
theorem collinear_zero (lam φ1 φ2 χ1 χ2 γ s mL2 : ℝ)
    (h1 : χ1 = lam * φ1) (h2 : χ2 = lam * φ2) :
    exch γ s mL2 φ1 φ2 χ1 χ2 = 0 := by
  unfold exch
  rw [h1, h2]
  ring

-- 6. gamma = 0  =>  E = 0  (decoupled sector, separate currents)
theorem gamma0_zero (φ1 φ2 χ1 χ2 s mL2 : ℝ) : exch 0 s mL2 φ1 φ2 χ1 χ2 = 0 := by
  unfold exch
  ring

-- 7. U(1) potential matrix determinant: det V = m_H² m_L² > 0
--    (static sector: -Δ + V positive definite on the compact leaf, kernel {0})
theorem potmat_det (mH2 mL2 γ s : ℝ) :
    (mH2 + γ^2 * mL2 * s^2) * mL2 - (γ * mL2 * s)^2 = mH2 * mL2 := by
  ring

-- 8. current first-derivative (∂ψ ∂ψ) term vanishes by symmetry of C^{μν}:
--    ε_ab A_a B_b + ε_ab B_a A_b = 0
theorem curl_term_antisym (p1 p2 q1 q2 : ℝ) :
    (p1 * q2 - p2 * q1) + (q1 * p2 - q2 * p1) = 0 := by
  ring

-- 9. on-shell mode coefficient: with ratio r = (P - y - a)/(γ m_L² s),
--    a = m_H² + γ²m_L²s², the mode potential coefficient collapses to P - y:
--    m_H² + γ m_L² s r + γ² m_L² s² = P - y.
theorem onshell_coefficient (mH2 mL2 γ P y a s : ℝ)
    (ha : a = mH2 + γ^2 * mL2 * s^2) (hden : γ * mL2 * s ≠ 0) :
    mH2 + γ * mL2 * s * ((P - y - a) / (γ * mL2 * s)) + γ^2 * mL2 * s^2 = P - y := by
  have hcancel : γ * mL2 * s * ((P - y - (mH2 + γ ^ 2 * mL2 * s ^ 2)) / (γ * mL2 * s))
      = P - y - (mH2 + γ ^ 2 * mL2 * s ^ 2) := by
    rw [mul_comm (γ * mL2 * s) ((P - y - (mH2 + γ ^ 2 * mL2 * s ^ 2)) / (γ * mL2 * s))]
    exact div_mul_cancel₀ (P - y - (mH2 + γ ^ 2 * mL2 * s ^ 2)) hden
  have hmain : γ * mL2 * s * (mH2 + γ * mL2 * s *
      ((P - y - (mH2 + γ ^ 2 * mL2 * s ^ 2)) / (γ * mL2 * s)) + γ^2 * mL2 * s^2)
      = γ * mL2 * s * (P - y) := by
    rw [hcancel]
    ring
  have hnum : (P - y - a) / (γ * mL2 * s)
      = (P - y - (mH2 + γ ^ 2 * mL2 * s ^ 2)) / (γ * mL2 * s) := by
    rw [ha]
  rw [hnum]
  exact mul_left_cancel₀ hden hmain

-- 10. mode-ratio consistency across the two coupled equations:
--     (P - y - a)/(γ m_L² s) = γ m_L² s / (P - y - b)   given the dispersion
--     (P - y - a)(P - y - b) = γ² m_L⁴ s².
theorem mode_ratio_consistency (P y a b c mL2 γ s : ℝ)
    (hdisp : (P - y - a) * (P - y - b) = c)
    (hcgt : c = γ^2 * mL2^2 * s^2)
    (hden1 : γ * mL2 * s ≠ 0) (hden2 : P - y - b ≠ 0) :
    (P - y - a) / (γ * mL2 * s) = γ * mL2 * s / (P - y - b) := by
  have hmul : (P - y - a) * (P - y - b) = (γ * mL2 * s) * (γ * mL2 * s) := by
    rw [hcgt] at hdisp
    nlinarith [hdisp]
  have hrew : ((P - y - a) / (γ * mL2 * s)) * (P - y - b)
      = ((P - y - a) * (P - y - b)) / (γ * mL2 * s) := by
    ring
  rw [eq_div_iff hden2]
  rw [hrew, hmul]
  field_simp [hden1]

-- 11. cell construction: P = (y1 + y2 + a + b)/2  =>  y1 + y2 = 2P - (a + b)
theorem cell_sum (y1 y2 a b P : ℝ) (hP : P = (y1 + y2 + a + b) / 2) :
    y1 + y2 = 2 * P - (a + b) := by
  rw [hP]
  ring

-- 12. s-EOM amplitude: a² = -μ² / (γ m_L² (r + γ s))  from the homogeneous
--     rotating-mode solution of μ²s + γ m_L² s |φ|²(r + γ s) = 0 (s ≠ 0).
theorem sEOM_amplitude (μ2 s γ mL2 r a : ℝ)
    (hs : s ≠ 0) (hden : γ * mL2 * (r + γ * s) ≠ 0)
    (heom : μ2 * s + γ * mL2 * s * (a * (r * a) + γ * s * (a * a)) = 0) :
    a^2 = -μ2 / (γ * mL2 * (r + γ * s)) := by
  have hf : s * (μ2 + γ * mL2 * a^2 * (r + γ * s)) = 0 := by
    nlinarith [heom]
  have h2 : μ2 + γ * mL2 * a^2 * (r + γ * s) = 0 := by
    exact (mul_eq_zero.mp hf).resolve_left hs
  rw [eq_div_iff hden]
  nlinarith [h2]

-- ==== AXIOM AUDIT (unfiltered #print axioms; hard bar: subseteq of
--     {propext, Classical.choice, Quot.sound}, zero sorry) ====
#print axioms exch
#print axioms exchange_phi
#print axioms exchange_chi
#print axioms exchange_pair_cancels
#print axioms diag_mass_antisym
#print axioms collinear_zero
#print axioms gamma0_zero
#print axioms potmat_det
#print axioms curl_term_antisym
#print axioms onshell_coefficient
#print axioms mode_ratio_consistency
#print axioms cell_sum
#print axioms sEOM_amplitude

end
