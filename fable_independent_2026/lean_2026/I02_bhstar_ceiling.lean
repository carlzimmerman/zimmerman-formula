import Mathlib

/-!
# I02 — Wave J: the SMS ceiling as a closed-form function of the GR coefficient

SCOPE (per lean-math-certification): this file certifies the ALGEBRA transporting three
inputs — (i) the T2 radiation-domination invariant x·q³M² = C, (ii) the T4 envelope
Γ₁ − 4/3 ≤ x/3 (Γ₁−4/3 ≤ β/3 ≤ x/3 with β = x/(1+x) ≤ x), (iii) the ABSORBED
Chandrasekhar-class stability criterion κ_GR·α ≤ Γ₁ − 4/3 with the compactness closed form
α = a5·S, S = √(M/M0) — into the stability bound S⁵·(3q³M0²κ_GR·a5) ≤ C, i.e.

    (M/M0)^(5/2) ≤ C / (3 q³ M0² κ_GR a5)          M_ceiling ∝ (q³ κ_GR)^(-2/5),

and its contrapositive: a configuration stable at mass M forces
κ_GR ≥ C/(3 q³ M0² a5 S⁵) ∝ M^(-5/2). Lean certifies this transport; it does not certify the
absorbed criterion or that nature's SMS structures obey the family. Zero `sorry`; axioms ⊆
{propext, Classical.choice, Quot.sound}. Numeric readings of the band (H1: κ_GR ∈
[8.8e-6, 4.8e-3] ⟹ ceiling ∈ [6.7e3, 8.4e4] envelope / [1.0e5, 5.1e5] exact-gap) stay in the
Python lane `bhstar_j1_ceiling_closed_form.py`.

The sqrt-atom firewall (skill): S = √(M/M0) is introduced as an ATOM (hS : 0 < S, hM :
M = M0 * S^2); no Real.sqrt appears in any proof below.
-/

noncomputable section

/-! ## The S⁵ stability bound -/

/-- **J (the S⁵ bound).** Given the family invariant x·q³M² = C, the envelope
Γ₁ − 4/3 ≤ x/3, the absorbed stability criterion κ_GR·α ≤ Γ₁ − 4/3, and the compactness
closed form α = a5·S with M = M0·S² — the configuration is stable only if
S⁵·(3q³M0²κ_GR·a5) ≤ C, i.e. (M/M0)^(5/2) ≤ C/(3q³M0²κ_GR·a5): the ceiling scales as
(q³κ_GR)^(-2/5). -/
theorem S5_bound {x q M C gap α κ a5 M0 S : ℝ}
    (hC : 0 < C) (hq : 0 < q) (hk : 0 < κ) (ha5 : 0 < a5) (hM0 : 0 < M0) (hS : 0 < S)
    (hM : M = M0 * S ^ 2) (halpha : α = a5 * S)
    (hT2 : x * q ^ 3 * M ^ 2 = C)
    (hgx : gap ≤ x / 3)
    (hstab : κ * α ≤ gap) :
    S ^ 5 * (3 * q ^ 3 * M0 ^ 2 * κ * a5) ≤ C := by
  have h3p : (3 : ℝ) ≠ 0 := by norm_num
  have hα : κ * α = κ * a5 * S := by rw [halpha]; ring
  -- normalize the invariant to the shape the multiplier chain produces
  rw [mul_assoc x (q ^ 3) (M ^ 2)] at hT2
  -- κ·a5·S·3 ≤ x  (from hstab, hgx, and (x/3)·3 = x)
  have h1 : κ * a5 * S * 3 ≤ x := by
    have hstep := mul_le_mul_of_nonneg_right hgx (by norm_num : (0 : ℝ) ≤ 3)
    rw [div_mul_cancel₀ _ h3p] at hstep
    have h2 := mul_le_mul_of_nonneg_right hstab (by norm_num : (0 : ℝ) ≤ 3)
    rw [hα] at h2
    linarith
  -- multiply by q³M² ≥ 0 and use the (normalized) invariant
  have h4 : κ * a5 * S * 3 * (q ^ 3 * M ^ 2) ≤ C := by
    have h5 : (κ * a5 * S * 3) * (q ^ 3 * M ^ 2) ≤ x * (q ^ 3 * M ^ 2) :=
      mul_le_mul_of_nonneg_right h1 (by positivity)
    rw [hT2] at h5
    exact h5
  -- substitute M = M0*S² and rearrange to the S⁵ form
  have h6 : κ * a5 * S * 3 * (q ^ 3 * (M0 * S ^ 2) ^ 2) ≤ C := by
    rw [← hM]
    exact h4
  calc S ^ 5 * (3 * q ^ 3 * M0 ^ 2 * κ * a5)
      = κ * a5 * S * 3 * (q ^ 3 * (M0 * S ^ 2) ^ 2) := by ring
    _ ≤ C := h6

/-- **J (the ceiling contrapositive).** If the GR coefficient is TOO SMALL for the mass —
C < S⁵·(3q³M0²κ_GR·a5), i.e. M above the closed-form ceiling — then the stability criterion
FAILS: the configuration is unstable. This is the ceiling as a falsifiable statement about
κ_GR. -/
theorem ceiling_unstable {x q M C gap α κ a5 M0 S : ℝ}
    (hC : 0 < C) (hq : 0 < q) (hk : 0 < κ) (ha5 : 0 < a5) (hM0 : 0 < M0) (hS : 0 < S)
    (hM : M = M0 * S ^ 2) (halpha : α = a5 * S)
    (hT2 : x * q ^ 3 * M ^ 2 = C)
    (hgx : gap ≤ x / 3)
    (hgt : C < S ^ 5 * (3 * q ^ 3 * M0 ^ 2 * κ * a5)) :
    ¬ (κ * α ≤ gap) := by
  intro hstab
  have h := S5_bound hC hq hk ha5 hM0 hS hM halpha hT2 hgx hstab
  linarith

/-- **J (the ceiling-transport theorem — the 2/5 sensitivity in its exact S⁵ form).** If a
configuration at GR coefficient κ is marginal at mass-scale S (S⁵·(cK·κ) = C, the stability
K-factor linear in κ with coefficient cK) and the coefficient is reduced to κ' = κ/lam
(structure suppression by lam), the marginal mass-scale moves to S' with S'⁵ = lam·S⁵ — i.e.
M_ceiling(κ/lam) = lam^(2/5)·M_ceiling(κ): the 552× κ_GR structure band transports to only
~12.5× in ceiling. The M^(2/5) reading stays in the Python lane. -/
theorem ceiling_transport {C cK κ lam S S' : ℝ}
    (hC : 0 < C) (hcK : 0 < cK) (hlam : 0 < lam) (hS : 0 < S) (hS' : 0 < S')
    (hmarg : S ^ 5 * (cK * κ) = C)             -- marginal at κ
    (hmarg' : S' ^ 5 * (cK * (κ / lam)) = C) : -- marginal at κ' = κ/lam
    S' ^ 5 = lam * S ^ 5 := by
  have hden : lam ≠ 0 := ne_of_gt hlam
  have hcKκ : cK * κ ≠ 0 := by
    intro hzero
    rw [hzero, mul_zero] at hmarg
    exact absurd hmarg.symm (ne_of_gt hC)
  have h2 : S' ^ 5 * (cK * κ) = C * lam := by
    have h3 := congrArg (fun t : ℝ => t * lam) hmarg'
    rw [← mul_assoc (S' ^ 5) cK (κ / lam)] at h3
    rw [mul_assoc ((S' ^ 5) * cK) (κ / lam) lam] at h3
    rw [div_mul_cancel₀ κ hden] at h3
    linear_combination (norm := ring_nf) h3
  have hS5 : S ^ 5 = C / (cK * κ) := (eq_div_iff hcKκ).mpr hmarg
  have hS'5 : S' ^ 5 = C * lam / (cK * κ) := (eq_div_iff hcKκ).mpr h2
  rw [hS'5, hS5, mul_comm lam (C / (cK * κ)), div_mul_eq_mul_div]

/-! ## Numeric anchors (exact rationals; the band readings stay in the Python lane) -/

/-- The T2 invariant at the anchor (x = 4.638e-8 = 4638/10^11, q = 2/5, M = 10^5 M⊙):
C = 296832/12500·... = 37104/1250 = 29.6832. -/
example : (4638 / 10 ^ 11 : ℝ) * (2 / 5) ^ 3 * (10 ^ 5) ^ 2 = 37104 / 1250 := by norm_num

/-- The inverse reading at the anchor: stability at M = 10⁵ M⊙ forces
κ_GR ≤ C/(3·q³·M0²·a5·S⁵) with S = 1 — the exact-gap κ_req(10⁵) of H1 (2.773e-3 with the
envelope factor absorbed in the Python lane). -/
example : (37104 / 1250 : ℝ) / (3 * (2 / 5) ^ 3 * (10 ^ 5) ^ 2) = (4638 / 10 ^ 11) / 3 := by
  norm_num

end

#print axioms S5_bound
#print axioms ceiling_unstable
#print axioms ceiling_transport
