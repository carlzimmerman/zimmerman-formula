/-
  LN1_lean_cold_sector_certs — Lean 4 + Mathlib certificates for the mathematics used in the 2026-10-25 lanes
  CD1 (a₀-cored dwarf ceiling), NM1 (member halos), DH1 (dark-energy heater) and HG1/HG2 (hot gas).

  What this certifies: ALGEBRA AND ANALYSIS ONLY, from the stated premises. It does not certify any empirical fact:
  not that halos are Burkert, not that Σ = a₀/(2πG), not any measured dwarf or cluster number. κ = ½ is FITTED.
  Numeric inputs quoted from lane outputs are labelled as premises.

  Compile: cd fable_independent_2026/lean_2026 && lake env lean <path>/ColdSectorCerts.lean
-/
import Mathlib

open Real

namespace ColdSectorCerts

/-! ## 1. The Burkert mass shape function -/

/-- `Bk x = ln(1+x²) + 2 ln(1+x) − 2 arctan x`. For a Burkert profile ρ = ρ₀ r₀³ / ((r+r₀)(r²+r₀²)) the enclosed mass
is M(r) = π ρ₀ r₀³ · Bk(r/r₀) (X38 / CD1 `B`). -/
noncomputable def Bk (x : ℝ) : ℝ := Real.log (1 + x ^ 2) + 2 * Real.log (1 + x) - 2 * Real.arctan x

theorem Bk_zero : Bk 0 = 0 := by simp [Bk]

/-- **T1.** dBk/dx = 4x² / ((1+x)(1+x²)). Hence d/dr [π ρ₀ r₀³ Bk(r/r₀)] = 4π r² ρ(r): the closed form is the Burkert
mass (with `Bk_zero`, M(0) = 0). -/
theorem Bk_hasDerivAt (x : ℝ) (hx : 0 ≤ x) :
    HasDerivAt Bk (4 * x ^ 2 / ((1 + x) * (1 + x ^ 2))) x := by
  have h1 : (0 : ℝ) < 1 + x ^ 2 := by positivity
  have h2 : (0 : ℝ) < 1 + x := by linarith
  have dsq : HasDerivAt (fun y : ℝ => 1 + y ^ 2) (2 * x) x := by
    simpa using ((hasDerivAt_pow 2 x).const_add 1)
  have dlin : HasDerivAt (fun y : ℝ => 1 + y) 1 x := by
    simpa using ((hasDerivAt_id x).const_add 1)
  have d1 : HasDerivAt (fun y : ℝ => Real.log (1 + y ^ 2)) (2 * x / (1 + x ^ 2)) x :=
    dsq.log (ne_of_gt h1)
  have d2 : HasDerivAt (fun y : ℝ => Real.log (1 + y)) (1 / (1 + x)) x :=
    dlin.log (ne_of_gt h2)
  have d3 : HasDerivAt Real.arctan (1 / (1 + x ^ 2)) x := Real.hasDerivAt_arctan x
  have hsum := (d1.add (d2.const_mul 2)).sub (d3.const_mul 2)
  have h1' : (1 + x ^ 2) ≠ 0 := ne_of_gt h1
  have h2' : (1 + x) ≠ 0 := ne_of_gt h2
  have key : 2 * x / (1 + x ^ 2) + 2 * (1 / (1 + x)) - 2 * (1 / (1 + x ^ 2))
      = 4 * x ^ 2 / ((1 + x) * (1 + x ^ 2)) := by
    field_simp
    ring
  rw [← key]
  exact hsum

/-! ## 2. A fixed-Σ halo's pull depends on r and r₀ only through x = r/r₀ -/

/-- **T2.** With Σ = ρ₀ r₀ and M(r) = π Σ r₀² Bk(r/r₀), the acceleration G M / r² equals π G Σ · Bk(x)/x², x = r/r₀.
So the maximum over every core radius r₀ is π G Σ · sup_x Bk(x)/x², the same at every radius (CD1's ceiling). -/
theorem accel_shape (G Sig r r0 : ℝ) (hr : 0 < r) (hr0 : 0 < r0) :
    G * (π * Sig * r0 ^ 2 * Bk (r / r0)) / r ^ 2 = π * G * Sig * (Bk (r / r0) / (r / r0) ^ 2) := by
  field_simp

/-! ## 3. Certified bounds on the ceiling: 1/2 < sup Bk(x)/x² ≤ 9/16 -/

/-- Polynomial lemma behind the upper bound: 4x ≤ (9/8)(1+x)(1+x²) for x ≥ 0. -/
theorem poly_bound (x : ℝ) (hx : 0 ≤ x) : 4 * x ≤ (9 / 8) * (1 + x) * (1 + x ^ 2) := by
  nlinarith [sq_nonneg (x - 13 / 20), mul_nonneg hx (sq_nonneg (x - 13 / 20)), sq_nonneg (x - 1),
    mul_nonneg hx (sq_nonneg (x - 1 / 2))]

theorem deriv_kernel_le (x : ℝ) (hx : 0 ≤ x) : 4 * x ^ 2 / ((1 + x) * (1 + x ^ 2)) ≤ (9 / 8) * x := by
  have hpos : (0 : ℝ) < (1 + x) * (1 + x ^ 2) := by positivity
  rw [div_le_iff₀ hpos]
  have := poly_bound x hx
  nlinarith [mul_le_mul_of_nonneg_left this hx]

/-- **T3 (upper).** Bk(x) ≤ (9/16) x² for every x ≥ 0. -/
theorem Bk_le (x : ℝ) (hx : 0 ≤ x) : Bk x ≤ 9 / 16 * x ^ 2 := by
  set f : ℝ → ℝ := fun y => 9 / 16 * y ^ 2 - Bk y with hf
  have hd : ∀ y, 0 ≤ y → HasDerivAt f (9 / 8 * y - 4 * y ^ 2 / ((1 + y) * (1 + y ^ 2))) y := by
    intro y hy
    have hp : HasDerivAt (fun z : ℝ => z ^ 2) (2 * y) y := by simpa using hasDerivAt_pow 2 y
    have h := (hp.const_mul (9 / 16 : ℝ)).sub (Bk_hasDerivAt y hy)
    have e : 9 / 8 * y - 4 * y ^ 2 / ((1 + y) * (1 + y ^ 2))
        = 9 / 16 * (2 * y) - 4 * y ^ 2 / ((1 + y) * (1 + y ^ 2)) := by ring
    rw [e]
    exact h
  have hmono : MonotoneOn f (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
    · intro y hy
      exact (hd y hy).continuousAt.continuousWithinAt
    · intro y hy
      rw [interior_Ici] at hy
      exact (hd y (le_of_lt hy)).differentiableAt.differentiableWithinAt
    · intro y hy
      rw [interior_Ici] at hy
      rw [(hd y (le_of_lt hy)).deriv]
      linarith [deriv_kernel_le y (le_of_lt hy)]
  have h0 : f 0 ≤ f x := hmono (Set.mem_Ici.mpr (le_refl (0 : ℝ))) hx hx
  simp only [hf, Bk_zero] at h0
  norm_num at h0
  linarith

/-- **T3 (lower).** Bk(1) = 3 ln 2 − π/2 > 1/2, so sup Bk(x)/x² > 1/2 (attained at x = 1 or better). -/
theorem Bk_one_gt : 1 / 2 < Bk 1 := by
  have hl : Bk 1 = 3 * Real.log 2 - π / 2 := by
    simp only [Bk, Real.arctan_one]
    norm_num
    ring
  rw [hl]
  have h2 := Real.log_two_gt_d9
  have hp := Real.pi_lt_d2
  linarith

/-- **CD1 ceiling, certified.** With Σ = a₀/(2πG), every fixed-Σ Burkert halo, for every r and r₀, has
G M(r)/r² ≤ (9/32) a₀ = 0.28125 a₀. CD1's numerical value 0.2545 a₀ lies inside [1/4, 9/32] a₀ (T3 lower × π G Σ = a₀/4). -/
theorem ceiling (G a0 r r0 : ℝ) (hG : 0 < G) (ha : 0 < a0) (hr : 0 < r) (hr0 : 0 < r0) :
    G * (π * (a0 / (2 * π * G)) * r0 ^ 2 * Bk (r / r0)) / r ^ 2 ≤ 9 / 32 * a0 := by
  rw [accel_shape G _ r r0 hr hr0]
  have hx : 0 < r / r0 := div_pos hr hr0
  have hb := Bk_le (r / r0) hx.le
  have hx2 : 0 < (r / r0) ^ 2 := by positivity
  have hq : Bk (r / r0) / (r / r0) ^ 2 ≤ 9 / 16 := by
    rw [div_le_iff₀ hx2]; linarith
  have hpi : 0 < π := Real.pi_pos
  have hcoef : π * G * (a0 / (2 * π * G)) = a0 / 2 := by field_simp
  calc π * G * (a0 / (2 * π * G)) * (Bk (r / r0) / (r / r0) ^ 2)
      = a0 / 2 * (Bk (r / r0) / (r / r0) ^ 2) := by rw [hcoef]
    _ ≤ a0 / 2 * (9 / 16) := by apply mul_le_mul_of_nonneg_left hq; linarith
    _ = 9 / 32 * a0 := by ring

/-! ## 4. DH1: a spatially uniform drive cannot be a fold source -/

/-- **T4.** For H(x) = A p²/2 + B x p + C x + Φ(x) at fixed (p, t), the drive coefficients A, B, C (anything uniform in
space, e.g. dark-energy quantities) drop out of ∂²H/∂x², which is Φ''(x). A single-stream sheet folds only through Φ''. -/
theorem fold_source (A Bc C p : ℝ) (Φ : ℝ → ℝ) (hΦ : Differentiable ℝ Φ) (x : ℝ) :
    deriv (deriv (fun y => A * p ^ 2 / 2 + Bc * y * p + C * y + Φ y)) x = deriv (deriv Φ) x := by
  have e : (fun y => A * p ^ 2 / 2 + Bc * y * p + C * y + Φ y)
      = fun y => A * p ^ 2 / 2 + (Bc * p + C) * y + Φ y := by
    funext y; ring
  have hl : ∀ y, HasDerivAt (fun y => A * p ^ 2 / 2 + (Bc * p + C) * y + Φ y) ((Bc * p + C) + deriv Φ y) y := by
    intro y
    have h1 : HasDerivAt (fun y : ℝ => (Bc * p + C) * y) (Bc * p + C) y := by
      simpa using (hasDerivAt_id y).const_mul (Bc * p + C)
    exact (h1.const_add (A * p ^ 2 / 2)).add (hΦ y).hasDerivAt
  have hD : deriv (fun y => A * p ^ 2 / 2 + (Bc * p + C) * y + Φ y) = fun y => (Bc * p + C) + deriv Φ y := by
    funext y; exact (hl y).deriv
  rw [e, hD]
  exact deriv_const_add (Bc * p + C)

/-- **T5 (DH1 statement 2, from the lane's numbers as premises).** If heating per unit mass ∝ σ² then c_s = A σ with one
A for every system. SPARC needs A ≥ 2.695 (canonical) / 2.856 (alt); KT clusters allow A ≤ 1.424 / 1.472. No A does both. -/
theorem windows_disjoint :
    (¬ ∃ A : ℝ, 2695 / 1000 ≤ A ∧ A ≤ 1424 / 1000) ∧ (¬ ∃ A : ℝ, 2856 / 1000 ≤ A ∧ A ≤ 1472 / 1000) := by
  constructor <;> rintro ⟨A, h1, h2⟩ <;> linarith

/-! ## 5. HG1/HG2: the baryonic acceleration of a group does not depend on its distance -/

/-- **T6.** With M = Υ F (4π) d² (flux F) and r = θ d (angle θ), g_bar = G M / r² is the same at distance k d. -/
theorem gbar_distance_free (G Υ F θ d k : ℝ) (hd : d ≠ 0) (hθ : θ ≠ 0) (hk : k ≠ 0) :
    G * (Υ * F * (4 * π) * (k * d) ^ 2) / (θ * (k * d)) ^ 2 = G * (Υ * F * (4 * π) * d ^ 2) / (θ * d) ^ 2 := by
  field_simp


/-! ## 6. The open question: can a self-coupled cold dark energy give a₀ cores in galaxies and denser cluster cores?

Premises (stated, not certified as physics):
* (P1) isothermal (King) core: ρ₀ r₀² = 9σ²/(4πG);
* (P2) the core is where the self-interaction rate times the age is one, with a power-law velocity dependence:
  ρ₀ = 1 / (K σ^(1−n) t), K > 0 (cross-section per mass ∝ v^(−n), velocity ∝ σ, constants absorbed in K).
Then the core surface density is Σ₀ = ρ₀ r₀ with Σ₀² = 9 σ^(1+n) / (4πG K t), i.e. Σ₀ ∝ σ^q t^(−1/2), q = (1+n)/2. -/

/-- **T7.** Σ₀² = 9 σ^(1+n) / (4πG K t) from (P1) and (P2). -/
theorem sidm_core_surface (G K t σ n ρ0 r0 : ℝ) (hG : 0 < G) (hK : 0 < K) (ht : 0 < t) (hσ : 0 < σ)
    (hP1 : ρ0 * r0 ^ 2 = 9 * σ ^ 2 / (4 * π * G))
    (hP2 : ρ0 = 1 / (K * σ ^ (1 - n) * t)) :
    (ρ0 * r0) ^ 2 = 9 * σ ^ (1 + n) / (4 * π * G * K * t) := by
  have hsplit : σ ^ (2 : ℝ) = σ ^ (1 + n) * σ ^ (1 - n) := by
    rw [← Real.rpow_add hσ]; ring_nf
  have hs2 : σ ^ 2 = σ ^ (1 + n) * σ ^ (1 - n) := by
    rw [← hsplit]; norm_cast
  have hpos : 0 < σ ^ (1 - n) := Real.rpow_pos_of_pos hσ _
  have hpi : 0 < π := Real.pi_pos
  calc (ρ0 * r0) ^ 2 = ρ0 * (ρ0 * r0 ^ 2) := by ring
    _ = 1 / (K * σ ^ (1 - n) * t) * (9 * (σ ^ (1 + n) * σ ^ (1 - n)) / (4 * π * G)) := by rw [hP1, hP2, hs2]
    _ = 9 * σ ^ (1 + n) / (4 * π * G * K * t) := by field_simp

/-- Σ₀ written as a function of the halo dispersion and the age: Σ(σ, t) = C σ^q t^(−1/2) (C > 0, q = (1+n)/2). -/
noncomputable def SigmaCore (C q σ t : ℝ) : ℝ := C * σ ^ q * t ^ (-(1 / 2 : ℝ))

theorem log_SigmaCore (C q σ t : ℝ) (hC : 0 < C) (hσ : 0 < σ) (ht : 0 < t) :
    Real.log (SigmaCore C q σ t) = Real.log C + q * Real.log σ - (1 / 2) * Real.log t := by
  unfold SigmaCore
  rw [Real.log_mul (by positivity) (by positivity), Real.log_mul (by positivity) (by positivity),
    Real.log_rpow hσ, Real.log_rpow ht]
  ring

/-- **T8 (the window).** Suppose
* galaxies of the same age with dispersions σ₁ < σ₂ have Σ within a factor F: Σ(σ₂)/Σ(σ₁) ≤ F;
* clusters need Σ_cl/Σ_gal ≥ Q, with σ_cl/σ_gal ≤ R_c and t_cl/t_gal ≥ τ (clusters younger: τ ≤ 1).
Then the exponent q must satisfy  log Q + ½ log τ ≤ q · log R_c  and  q · log(σ₂/σ₁) ≤ log F.
So the window is empty whenever (log Q + ½ log τ)/log R_c > log F / log(σ₂/σ₁). -/
theorem sidm_window (C q σ1 σ2 σg σc t tg tc F Q Rc τ : ℝ)
    (hC : 0 < C) (hq : 0 ≤ q) (h1 : 0 < σ1) (h2 : 0 < σ2) (hg : 0 < σg) (hc : 0 < σc)
    (ht : 0 < t) (htg : 0 < tg) (htc : 0 < tc) (hQ : 0 < Q) (hτ : 0 < τ)
    (hflat : SigmaCore C q σ2 t / SigmaCore C q σ1 t ≤ F)
    (hcl : Q ≤ SigmaCore C q σc tc / SigmaCore C q σg tg)
    (hRc : σc / σg ≤ Rc) (hage : τ ≤ tc / tg) :
    Real.log Q + (1 / 2) * Real.log τ ≤ q * Real.log Rc ∧ q * Real.log (σ2 / σ1) ≤ Real.log F := by
  have pos : ∀ σ' t', 0 < σ' → 0 < t' → 0 < SigmaCore C q σ' t' := by
    intro σ' t' hs ht'; unfold SigmaCore; positivity
  constructor
  · have hr : 0 < SigmaCore C q σc tc / SigmaCore C q σg tg := div_pos (pos _ _ hc htc) (pos _ _ hg htg)
    have hl := Real.log_le_log hQ hcl
    rw [Real.log_div (ne_of_gt (pos _ _ hc htc)) (ne_of_gt (pos _ _ hg htg)),
      log_SigmaCore C q σc tc hC hc htc, log_SigmaCore C q σg tg hC hg htg] at hl
    have hR : Real.log (σc / σg) ≤ Real.log Rc := Real.log_le_log (div_pos hc hg) hRc
    have hT : Real.log τ ≤ Real.log (tc / tg) := Real.log_le_log hτ hage
    rw [Real.log_div (ne_of_gt hc) (ne_of_gt hg)] at hR
    rw [Real.log_div (ne_of_gt htc) (ne_of_gt htg)] at hT
    nlinarith [mul_le_mul_of_nonneg_left hR hq]
  · have hF : 0 < F := lt_of_lt_of_le (div_pos (pos _ _ h2 ht) (pos _ _ h1 ht)) hflat
    have hl := Real.log_le_log (div_pos (pos _ _ h2 ht) (pos _ _ h1 ht)) hflat
    rw [Real.log_div (ne_of_gt (pos _ _ h2 ht)) (ne_of_gt (pos _ _ h1 ht)),
      log_SigmaCore C q σ2 t hC h2 ht, log_SigmaCore C q σ1 t hC h1 ht] at hl
    rw [Real.log_div (ne_of_gt h2) (ne_of_gt h1)]
    linarith

end ColdSectorCerts

/-! ## Axiom audit (must list only propext, Classical.choice, Quot.sound) -/
#print axioms ColdSectorCerts.Bk_hasDerivAt
#print axioms ColdSectorCerts.Bk_le
#print axioms ColdSectorCerts.Bk_one_gt
#print axioms ColdSectorCerts.ceiling
#print axioms ColdSectorCerts.fold_source
#print axioms ColdSectorCerts.windows_disjoint
#print axioms ColdSectorCerts.gbar_distance_free
#print axioms ColdSectorCerts.sidm_core_surface
#print axioms ColdSectorCerts.sidm_window
