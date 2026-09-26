import Mathlib

/-!
# XC6 — the heat filter's metric variation: the soft-leg lemma

SCOPE. `real_research/extra_crispy_2026/XC6_filter_variation_soft_leg.py` checks that the first metric variation of
S = exp(b Δ_h) has matrix elements (δΔ)_(p,q) · [e^{−b q²} − e^{−b p²}]/(p² − q²) (Duhamel). Those elements escape the
per-leg Gaussian only into soft legs. Lean certifies the scalar inequalities behind that statement. The operator
identities and the numerical sup are computed in the lane.

* `dd_factor`: for P > Q (squared momenta) the divided difference factors as b e^{−bQ} · φ(b(P − Q)) with
  φ(x) = (1 − e^{−x})/x — the Gaussian of the SMALLER momentum times a bounded factor.
* `phi_bounds`: 0 ≤ φ(x) ≤ 1 and φ(x)·x ≤ 1 for x > 0.
* `soft_leg_conformal`: for momenta p, q > 0 and any φ with those bounds (applied at x = b|p² − q²|),
  p (3q² + pq) b φ ≤ 8 min(p,q) (1 + b min(p,q)²). With the common e^{−b m²} this is the lemma for the conformal
  leg: the output gradient is bounded by the softer momentum.
* `soft_leg_tt`: the same bound for a transverse-traceless leg, p q² b φ ≤ 8 min(p,q)(1 + b min(p,q)²).
-/

open Real

theorem dd_factor (b P Q : ℝ) (hb : 0 < b) (hPQ : Q < P) :
    (exp (-(b * Q)) - exp (-(b * P))) / (P - Q)
      = b * exp (-(b * Q)) * ((1 - exp (-(b * (P - Q)))) / (b * (P - Q))) := by
  have hd : 0 < P - Q := by linarith
  have hbd : 0 < b * (P - Q) := mul_pos hb hd
  have hsplit : exp (-(b * P)) = exp (-(b * Q)) * exp (-(b * (P - Q))) := by
    rw [← Real.exp_add]; ring_nf
  rw [hsplit]
  field_simp

theorem phi_bounds (x : ℝ) (hx : 0 < x) :
    0 ≤ (1 - exp (-x)) / x ∧ (1 - exp (-x)) / x ≤ 1 ∧ (1 - exp (-x)) / x * x ≤ 1 := by
  have h1 : exp (-x) ≤ 1 := by
    rw [Real.exp_le_one_iff]; linarith
  have h2 : 1 - x ≤ exp (-x) := by
    have := Real.add_one_le_exp (-x); linarith
  have hpos : 0 < exp (-x) := Real.exp_pos _
  refine ⟨?_, ?_, ?_⟩
  · apply div_nonneg <;> linarith
  · rw [div_le_one hx]; linarith
  · rw [div_mul_cancel₀ _ (ne_of_gt hx)]; linarith

theorem soft_leg_conformal (b p q φ : ℝ) (hb : 0 < b) (hp : 0 < p) (hq : 0 < q)
    (hφ0 : 0 ≤ φ) (hφ1 : φ ≤ 1) (hφx : φ * (b * |p ^ 2 - q ^ 2|) ≤ 1) :
    p * (3 * q ^ 2 + p * q) * b * φ ≤ 8 * min p q * (1 + b * (min p q) ^ 2) := by
  rcases le_total p q with hpq | hqp
  · -- m = p
    rw [min_eq_left hpq]
    have habs : |p ^ 2 - q ^ 2| = q ^ 2 - p ^ 2 := by
      rw [abs_of_nonpos (by nlinarith)]; ring
    rw [habs] at hφx
    by_cases hbig : 2 * p ^ 2 ≤ q ^ 2
    · -- b φ ≤ 2/q²
      have hq2 : 0 < q ^ 2 := by positivity
      have key : b * φ * q ^ 2 ≤ 2 := by nlinarith
      have hpq' : p * q ≤ q ^ 2 := by nlinarith
      -- p(3q² + pq) b φ ≤ p · 4q² · bφ ≤ 8p
      have h4 : p * (3 * q ^ 2 + p * q) * b * φ ≤ p * (4 * q ^ 2) * (b * φ) := by
        have hbφ : 0 ≤ b * φ := mul_nonneg hb.le hφ0
        have : 3 * q ^ 2 + p * q ≤ 4 * q ^ 2 := by linarith
        nlinarith [mul_le_mul_of_nonneg_left this (mul_nonneg hp.le hbφ)]
      have h5 : p * (4 * q ^ 2) * (b * φ) ≤ 8 * p := by nlinarith
      have h6 : 8 * p ≤ 8 * p * (1 + b * p ^ 2) := by
        have : 0 ≤ b * p ^ 2 := by positivity
        nlinarith
      linarith
    · -- q² < 2p², φ ≤ 1
      rw [not_le] at hbig
      have hpq' : p * q ≤ q ^ 2 := by nlinarith
      have h3 : 3 * q ^ 2 + p * q ≤ 8 * p ^ 2 := by nlinarith
      have hbφ : b * φ ≤ b := by nlinarith
      have h7 : p * (3 * q ^ 2 + p * q) * b * φ ≤ p * (8 * p ^ 2) * b := by
        have e1 : 0 ≤ p * (3 * q ^ 2 + p * q) := by positivity
        have e2 : p * (3 * q ^ 2 + p * q) * (b * φ) ≤ p * (3 * q ^ 2 + p * q) * b :=
          mul_le_mul_of_nonneg_left hbφ e1
        have e3 : p * (3 * q ^ 2 + p * q) * b ≤ p * (8 * p ^ 2) * b := by
          apply mul_le_mul_of_nonneg_right _ hb.le
          exact mul_le_mul_of_nonneg_left h3 hp.le
        nlinarith
      nlinarith
  · -- m = q
    rw [min_eq_right hqp]
    have habs : |p ^ 2 - q ^ 2| = p ^ 2 - q ^ 2 := by
      rw [abs_of_nonneg (by nlinarith)]
    rw [habs] at hφx
    by_cases hbig : 2 * q ^ 2 ≤ p ^ 2
    · have hp2 : 0 < p ^ 2 := by positivity
      have key : b * φ * p ^ 2 ≤ 2 := by nlinarith
      -- p(3q² + pq) bφ = (3q² + pq)(p bφ) and p bφ ≤ 2/p
      have hq_le : q ≤ p := hqp
      have hbφ : 0 ≤ b * φ := mul_nonneg hb.le hφ0
      have hA : p * (3 * q ^ 2 + p * q) * b * φ * p = (3 * q ^ 2 + p * q) * (b * φ * p ^ 2) := by ring
      have hB : (3 * q ^ 2 + p * q) * (b * φ * p ^ 2) ≤ (3 * q ^ 2 + p * q) * 2 := by
        apply mul_le_mul_of_nonneg_left key; positivity
      have hC : (3 * q ^ 2 + p * q) * 2 ≤ 8 * q * p := by nlinarith
      have hD : p * (3 * q ^ 2 + p * q) * b * φ * p ≤ 8 * q * p := by linarith
      have hE : p * (3 * q ^ 2 + p * q) * b * φ ≤ 8 * q := by
        have := hD
        nlinarith
      have h6 : 8 * q ≤ 8 * q * (1 + b * q ^ 2) := by
        have : 0 ≤ b * q ^ 2 := by positivity
        nlinarith
      linarith
    · rw [not_le] at hbig
      have hp2q : p ≤ 2 * q := by nlinarith
      have h3 : p * (3 * q ^ 2 + p * q) ≤ 8 * q ^ 3 := by nlinarith
      have hbφ : b * φ ≤ b := by nlinarith
      have h7 : p * (3 * q ^ 2 + p * q) * b * φ ≤ 8 * q ^ 3 * b := by
        have e1 : 0 ≤ p * (3 * q ^ 2 + p * q) := by positivity
        have e2 : p * (3 * q ^ 2 + p * q) * (b * φ) ≤ p * (3 * q ^ 2 + p * q) * b :=
          mul_le_mul_of_nonneg_left hbφ e1
        have e3 : p * (3 * q ^ 2 + p * q) * b ≤ 8 * q ^ 3 * b :=
          mul_le_mul_of_nonneg_right h3 hb.le
        nlinarith
      nlinarith

theorem soft_leg_tt (b p q φ : ℝ) (hb : 0 < b) (hp : 0 < p) (hq : 0 < q)
    (hφ0 : 0 ≤ φ) (hφ1 : φ ≤ 1) (hφx : φ * (b * |p ^ 2 - q ^ 2|) ≤ 1) :
    p * q ^ 2 * b * φ ≤ 8 * min p q * (1 + b * (min p q) ^ 2) := by
  have hc := soft_leg_conformal b p q φ hb hp hq hφ0 hφ1 hφx
  have hle : p * q ^ 2 * b * φ ≤ p * (3 * q ^ 2 + p * q) * b * φ := by
    have hbφ : 0 ≤ b * φ := mul_nonneg hb.le hφ0
    have : p * q ^ 2 ≤ p * (3 * q ^ 2 + p * q) := by nlinarith
    nlinarith [mul_le_mul_of_nonneg_right this hbφ]
  linarith

#print axioms dd_factor
#print axioms phi_bounds
#print axioms soft_leg_conformal
#print axioms soft_leg_tt
