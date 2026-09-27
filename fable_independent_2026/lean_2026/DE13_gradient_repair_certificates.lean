/-
DE13 -- can a gradient stiffness repair DE12's obstruction?  Certificates for the structural steps.

real_research/dark_energy_2026/DE13_gate_gradient_repair.py computes the numbers (exact inertia counts on real
transition layers).  These theorems certify the steps its verdict rests on:
  * the second variation of (1/2) h(t) t'^2 in a direction eps has density h eps'^2 + 2 h' t' eps eps' +
    (1/2) h'' t'^2 eps^2.  This equals h eps'^2 - ((1/2) h'' t'^2 + h' t'') eps^2 plus the derivative of h' t' eps^2
    (chain and product rules).  After integrating by parts the k^0 term is K0 = (1/2) h'' t'^2 + h' t'';
  * for the gate's own gradient energy h = W'^2: h' = 2 W' W'' and h'' = 2 (W''^2 + W' W'''), so
    K0 = (W''^2 + W' W''') t'^2 + 2 W' W'' t'' (form ii);
  * a coefficient that switches on from zero with zero slope (h(0) = 0, h'(0) = 0, h(a) > 0) is strictly convex
    somewhere on (0, a), by the mean value theorem twice.  So a stiffness localised to the layer brings its own
    negative k^0 term, -(1/2) h'' t'^2 < 0 there;
  * a direction with G < 0 (gate and gas) and R <= 0 (the repair's own form) has G + mu R < 0 for every mu >= 0 (E3);
  * a direction with R < 0 is destabilised by every large enough mu.
Standard axioms only, no sorry.
-/
import Mathlib

open Set

namespace DE13

/-- the pointwise second-variation identity: stiffness, the k^0 term K0, and a total derivative. -/
theorem second_variation_density (h0 h1 h2 t1 t2 e e1 : ℝ) :
    h0 * e1 ^ 2 + 2 * h1 * t1 * e * e1 + (1 / 2) * h2 * t1 ^ 2 * e ^ 2
      = h0 * e1 ^ 2 - ((1 / 2) * h2 * t1 ^ 2 + h1 * t2) * e ^ 2
        + ((h2 * t1 ^ 2 + h1 * t2) * e ^ 2 + 2 * h1 * t1 * e * e1) := by
  ring

/-- the total derivative in `second_variation_density` is the derivative of h'(t) t' eps^2. -/
theorem boundary_term_deriv (hp hpp t tp tpp e ep : ℝ → ℝ) (x : ℝ)
    (Ht : HasDerivAt t (tp x) x) (Htp : HasDerivAt tp (tpp x) x) (He : HasDerivAt e (ep x) x)
    (Hh : HasDerivAt hp (hpp (t x)) (t x)) :
    HasDerivAt (fun y => hp (t y) * tp y * e y ^ 2)
      ((hpp (t x) * tp x ^ 2 + hp (t x) * tpp x) * e x ^ 2 + 2 * hp (t x) * tp x * e x * ep x) x := by
  have h1 : HasDerivAt (fun y => hp (t y)) (hpp (t x) * tp x) x := Hh.comp x Ht
  have h3 : HasDerivAt (fun y => e y ^ 2) (2 * e x * ep x) x := by
    have h : HasDerivAt (fun y => e y * e y) (ep x * e x + e x * ep x) x := He.mul He
    have hf : (fun y => e y ^ 2) = (fun y => e y * e y) := by funext y; ring
    rw [hf]
    exact h.congr_deriv (by ring)
  exact ((h1.mul Htp).mul h3).congr_deriv (by simp only [Pi.mul_apply]; ring)

/-- the second variation at a point: stiffness minus K0 eps^2 plus the derivative of the boundary term. -/
theorem second_variation_ibp (h hp hpp t tp tpp e ep : ℝ → ℝ) (x : ℝ)
    (Ht : HasDerivAt t (tp x) x) (Htp : HasDerivAt tp (tpp x) x) (He : HasDerivAt e (ep x) x)
    (Hh : HasDerivAt hp (hpp (t x)) (t x)) :
    ∃ D, HasDerivAt (fun y => hp (t y) * tp y * e y ^ 2) D x ∧
      h (t x) * ep x ^ 2 + 2 * hp (t x) * tp x * e x * ep x + (1 / 2) * hpp (t x) * tp x ^ 2 * e x ^ 2
        = h (t x) * ep x ^ 2 - ((1 / 2) * hpp (t x) * tp x ^ 2 + hp (t x) * tpp x) * e x ^ 2 + D :=
  ⟨_, boundary_term_deriv hp hpp t tp tpp e ep x Ht Htp He Hh, by ring⟩

/-- form (ii), h = W'^2: h' = 2 W' W'' and h'' = 2 (W''^2 + W' W'''). -/
theorem form_ii_coefficients (W1 W2 W3 : ℝ → ℝ) (t : ℝ)
    (H1 : HasDerivAt W1 (W2 t) t) (H2 : HasDerivAt W2 (W3 t) t) :
    HasDerivAt (fun s => W1 s ^ 2) (2 * W1 t * W2 t) t ∧
      HasDerivAt (fun s => 2 * W1 s * W2 s) (2 * (W2 t ^ 2 + W1 t * W3 t)) t := by
  constructor
  · have h : HasDerivAt (fun s => W1 s * W1 s) (W2 t * W1 t + W1 t * W2 t) t := H1.mul H1
    have hf : (fun s => W1 s ^ 2) = (fun s => W1 s * W1 s) := by funext s; ring
    rw [hf]
    exact h.congr_deriv (by ring)
  · exact ((H1.const_mul 2).mul H2).congr_deriv (by ring)

/-- form (ii)'s K0 is (1/2) h'' t'^2 + h' t'' with h = W'^2. -/
theorem form_ii_K0 (W1 W2 W3 t1 t2 : ℝ) :
    (1 / 2) * (2 * (W2 ^ 2 + W1 * W3)) * t1 ^ 2 + (2 * W1 * W2) * t2
      = (W2 ^ 2 + W1 * W3) * t1 ^ 2 + 2 * W1 * W2 * t2 := by
  ring

/-- a coefficient switching on from zero with zero slope is strictly convex somewhere: its own k^0 term,
-(1/2) h'' t'^2, is negative there. -/
theorem switch_on_convex (h : ℝ → ℝ) (hd : Differentiable ℝ h) (hd' : Differentiable ℝ (deriv h))
    (a : ℝ) (ha : 0 < a) (h0 : h 0 = 0) (hd0 : deriv h 0 = 0) (hpos : 0 < h a) :
    ∃ η ∈ Ioo (0 : ℝ) a, 0 < deriv (deriv h) η := by
  obtain ⟨c, hc, hfc⟩ := exists_deriv_eq_slope h ha hd.continuous.continuousOn hd.differentiableOn
  rw [h0] at hfc
  norm_num at hfc
  obtain ⟨η, hη, hfη⟩ := exists_deriv_eq_slope (deriv h) hc.1 hd'.continuous.continuousOn hd'.differentiableOn
  refine ⟨η, ⟨hη.1, lt_trans hη.2 hc.2⟩, ?_⟩
  rw [hfη, hfc, hd0]
  have hc0 : 0 < c := hc.1
  apply div_pos
  · simpa using div_pos hpos ha
  · linarith

/-- E3: one direction destabilised by the gate and gas (G < 0) and not stabilised by the repair (R <= 0) stays
unstable for every repair strength mu >= 0. -/
theorem no_mu_stabilises (G R : ℝ) (hG : G < 0) (hR : R ≤ 0) : ∀ μ : ℝ, 0 ≤ μ → G + μ * R < 0 := by
  intro μ hμ
  have : μ * R ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hμ hR
  linarith

/-- a direction the repair alone destabilises (R < 0) is unstable for every large enough mu. -/
theorem large_mu_destabilises (G R : ℝ) (hR : R < 0) : ∃ μ₀ : ℝ, ∀ μ, μ₀ < μ → G + μ * R < 0 := by
  have hR' : 0 < -R := by linarith
  refine ⟨|G| / (-R), fun μ hμ => ?_⟩
  rw [div_lt_iff₀ hR'] at hμ
  have hG : G ≤ |G| := le_abs_self G
  nlinarith

end DE13

#print axioms DE13.second_variation_density
#print axioms DE13.boundary_term_deriv
#print axioms DE13.second_variation_ibp
#print axioms DE13.form_ii_coefficients
#print axioms DE13.form_ii_K0
#print axioms DE13.switch_on_convex
#print axioms DE13.no_mu_stabilises
#print axioms DE13.large_mu_destabilises
