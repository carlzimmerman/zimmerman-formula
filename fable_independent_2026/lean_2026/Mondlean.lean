/-
  Mondlean — Lean 4 / mathlib formalization of the load-bearing MATHEMATICS behind the de Sitter–MOND
  F(Q)Θ completion (fable_independent_2026 lanes L77–L90; astra's F(Q)Θ construction).

  IMPORTANT SCOPE. Lean certifies *mathematical theorems*, not physical laws. What is machine-checked here
  is the internal mathematics the physics rests on — kernel identities, the health-sign dichotomy, the
  affine cuscuton degeneracy, the pressureless-dust / stiff-term density structure, and the MOND limits.
  Whether the theory is "a law of nature" is decided by the falsifiable predictions (dwarf σ–R_gc EFE,
  flat a₀(z), subdominant scalar GW) confronting DATA — not by Lean, and not while the intrinsic BBN
  fine-tuning (L84/L87) and astra's open ADM/khronon gates stand.

  Theorems (all: exit 0, zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}):
    hasDerivAt_G, hasDerivAt_Gp   — Gp = dG/dy and Gpp = d²G/dy² proven (not merely asserted).
    kernel_identity               — MOND kernel G'(y)/(2y) = 1 − e^{-y}.
    Gpp_zero, Gpp_pos             — health dichotomy: G''(0)=0, G''(y)>0 ∀ y>0 (no ghost off zero field).
    cubic_leading                 — G(0)=G'(0)=G''(0)=0 ⇒ MOND term is cubic (drops from the linear action).
    affine_degeneracy             — cuscuton/det-W degeneracy K_QQ = 3F_Q²/(2M²) ⟺ 2M²K_QQ − 3F_Q² = 0.
    density_affine                — the FLRW density is B + 3M²H² − (M²/3f²)(A+C/a³)²: a Λ-const, an a⁻³
                                    DUST cross term, and an a⁻⁶ STIFF term (the L84/L87 structure).
    stiff_coeff_ne_zero           — the a⁻⁶ stiff coefficient −M²/(3f²) ≠ 0 for M,f ≠ 0 (fine-tuning intrinsic).
    sound_speed_zero              — c_s² = 0 (pressureless dust; the L82 clustering key).
    mu_deep_slope                 — deep-MOND: μ(η)=1−e^{-η} has slope 1 at η=0 (μ ≈ η).
    mu_newton_limit               — EFE/strong-field: μ(η) → 1 as η → ∞ (Newtonisation).
-/
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

open Real Filter Topology

noncomputable def G (y : ℝ) : ℝ := y ^ 2 + 2 * (1 + y) * Real.exp (-y) - 2
noncomputable def Gp (y : ℝ) : ℝ := 2 * y * (1 - Real.exp (-y))
noncomputable def Gpp (y : ℝ) : ℝ := 2 * (1 + (y - 1) * Real.exp (-y))

/-- exp(-x) derivative, via the dedicated `HasDerivAt.exp` builder (clean function form). -/
private theorem hasDerivAt_expNeg (y : ℝ) :
    HasDerivAt (fun x : ℝ => Real.exp (-x)) (Real.exp (-y) * (-1)) y :=
  ((hasDerivAt_id y).neg).exp

/-- G'(y) = 2y(1 − e^{-y}): the MOND kernel, proven as the derivative. -/
theorem hasDerivAt_G (y : ℝ) : HasDerivAt G (Gp y) y := by
  have hpow : HasDerivAt (fun x : ℝ => x ^ 2) (2 * y) y := by simpa using hasDerivAt_pow 2 y
  have hlin2 : HasDerivAt (fun x : ℝ => 2 * (1 + x)) (2 * 1) y :=
    ((hasDerivAt_id y).const_add (1 : ℝ)).const_mul 2
  have hmul : HasDerivAt (fun x : ℝ => 2 * (1 + x) * Real.exp (-x))
      ((2 * 1) * Real.exp (-y) + 2 * (1 + y) * (Real.exp (-y) * (-1))) y :=
    hlin2.mul (hasDerivAt_expNeg y)
  have h : HasDerivAt G
      ((2 * y) + ((2 * 1) * Real.exp (-y) + 2 * (1 + y) * (Real.exp (-y) * (-1)))) y :=
    (hpow.add hmul).sub_const (2 : ℝ)
  have hv : (2 * y) + ((2 * 1) * Real.exp (-y) + 2 * (1 + y) * (Real.exp (-y) * (-1))) = Gp y := by
    simp only [Gp]; ring
  rwa [hv] at h

/-- G''(y) = 2(1 + (y−1)e^{-y}): proven as the derivative of Gp. -/
theorem hasDerivAt_Gp (y : ℝ) : HasDerivAt Gp (Gpp y) y := by
  have h2y : HasDerivAt (fun x : ℝ => 2 * x) (2 : ℝ) y := by simpa using (hasDerivAt_id y).const_mul 2
  have h1me : HasDerivAt (fun x : ℝ => 1 - Real.exp (-x)) (0 - Real.exp (-y) * (-1)) y :=
    (hasDerivAt_const y (1 : ℝ)).sub (hasDerivAt_expNeg y)
  have h : HasDerivAt Gp
      (2 * (1 - Real.exp (-y)) + (2 * y) * (0 - Real.exp (-y) * (-1))) y := h2y.mul h1me
  have hv : 2 * (1 - Real.exp (-y)) + (2 * y) * (0 - Real.exp (-y) * (-1)) = Gpp y := by
    simp only [Gpp]; ring
  rwa [hv] at h

/-- The MOND kernel identity: G'(y)/(2y) = 1 − e^{-y} for y ≠ 0. -/
theorem kernel_identity (y : ℝ) (hy : y ≠ 0) : Gp y / (2 * y) = 1 - Real.exp (-y) := by
  simp only [Gp]; field_simp

/-- Zero-field point: G''(0) = 0 (loss of ellipticity / astra's strong-coupling obstruction). -/
theorem Gpp_zero : Gpp 0 = 0 := by simp only [Gpp, neg_zero, Real.exp_zero]; ring

/-- Away from zero field the scalar is a stable massive mode: G''(y) > 0 for all y > 0. -/
theorem Gpp_pos {y : ℝ} (hy : 0 < y) : 0 < Gpp y := by
  have he : 0 < Real.exp (-y) := Real.exp_pos _
  have hexp_ge : y + 1 ≤ Real.exp y := Real.add_one_le_exp y
  have hfac : 0 < Real.exp y + y - 1 := by nlinarith
  have hinv : Real.exp (-y) * Real.exp y = 1 := by rw [← Real.exp_add]; simp
  have hkey : 1 + (y - 1) * Real.exp (-y) = Real.exp (-y) * (Real.exp y + y - 1) := by
    linear_combination -hinv
  have hpos : 0 < 1 + (y - 1) * Real.exp (-y) := by rw [hkey]; exact mul_pos he hfac
  simp only [Gpp]; linarith

theorem G_zero : G 0 = 0 := by simp only [G, neg_zero, Real.exp_zero]; ring
theorem Gp_zero : Gp 0 = 0 := by simp [Gp]

/-- G's expansion begins at the CUBE (G(0)=G'(0)=G''(0)=0): why the MOND term is cubic in the perturbation
    and drops from the quadratic cosmological action (L82). -/
theorem cubic_leading : G 0 = 0 ∧ Gp 0 = 0 ∧ Gpp 0 = 0 := ⟨G_zero, Gp_zero, Gpp_zero⟩

/-- The affine cuscuton degeneracy: K_QQ = 3F_Q²/(2M²) ⟺ 2M²K_QQ − 3F_Q² = 0 (M ≠ 0). -/
theorem affine_degeneracy (M FQ KQQ : ℝ) (hM : M ≠ 0) :
    KQQ = 3 * FQ ^ 2 / (2 * M ^ 2) ↔ 2 * M ^ 2 * KQQ - 3 * FQ ^ 2 = 0 := by
  have hM2 : (2 : ℝ) * M ^ 2 ≠ 0 := mul_ne_zero two_ne_zero (pow_ne_zero 2 hM)
  rw [eq_div_iff hM2]; constructor
  · intro h; linear_combination h
  · intro h; linear_combination h

/-- The FLRW density on the affine locus is a Λ-constant plus a back-reaction plus an a⁻³ DUST cross term
    and an a⁻⁶ STIFF term, exactly: expanding (A + C/a³)² = A² + 2A(C/a³) + (C/a³)². -/
theorem density_affine (M f A B C H a : ℝ) :
    B + 3 * M ^ 2 * H ^ 2 - (M ^ 2 / (3 * f ^ 2)) * (A + C / a ^ 3) ^ 2
    = (B + 3 * M ^ 2 * H ^ 2 - (M ^ 2 / (3 * f ^ 2)) * A ^ 2)      -- Λ-const + back-reaction
      + (-(2 * M ^ 2 * A) / (3 * f ^ 2)) * (C / a ^ 3)            -- a⁻³ DUST cross term
      + (-(M ^ 2) / (3 * f ^ 2)) * (C / a ^ 3) ^ 2 := by          -- a⁻⁶ STIFF term
  ring

/-- The a⁻⁶ stiff coefficient −M²/(3f²) is nonzero for any M ≠ 0, f ≠ 0: the stiff term is unavoidable
    once the clock sources a dust (L84/L87 — the intrinsic BBN fine-tuning). -/
theorem stiff_coeff_ne_zero (M f : ℝ) (hM : M ≠ 0) (hf : f ≠ 0) :
    -(M ^ 2) / (3 * f ^ 2) ≠ 0 := by
  have : (3 : ℝ) * f ^ 2 ≠ 0 := mul_ne_zero three_ne_zero (pow_ne_zero 2 hf)
  simp [div_ne_zero_iff, pow_ne_zero, hM, this, neg_ne_zero]

/-- Pressureless dust: gradient coefficient 0 and positive kinetic coefficient ⟹ sound speed² = 0. -/
theorem sound_speed_zero (grad kin : ℝ) (hgrad : grad = 0) (hkin : 0 < kin) : grad / kin = 0 := by
  simp [hgrad]

/-- Deep-MOND limit: the interpolating function μ(η)=1−e^{-η} has slope 1 at η=0, i.e. μ(η) ≈ η
    (the deep-MOND regime, matching G'(y)/(2y) at small argument). -/
theorem mu_deep_slope : HasDerivAt (fun η : ℝ => 1 - Real.exp (-η)) 1 0 := by
  have h : HasDerivAt (fun η : ℝ => 1 - Real.exp (-η)) (0 - Real.exp (-0) * (-1)) 0 :=
    (hasDerivAt_const (0 : ℝ) (1 : ℝ)).sub (hasDerivAt_expNeg 0)
  have hv : (0 - Real.exp (-0) * (-1)) = 1 := by simp
  rwa [hv] at h

/-- EFE / strong-field limit: μ(η)=1−e^{-η} → 1 as η → ∞ (full Newtonisation under a strong external
    field — the External Field Effect saturating to the GR/DM baseline, L89). -/
theorem mu_newton_limit : Tendsto (fun η : ℝ => 1 - Real.exp (-η)) atTop (𝓝 1) := by
  have h0 : Tendsto (fun η : ℝ => Real.exp (-η)) atTop (𝓝 0) :=
    Real.tendsto_exp_neg_atTop_nhds_zero
  have h := (tendsto_const_nhds (x := (1 : ℝ))).sub h0
  simpa using h

/-! ### Cuscuton-closure theorem (L95): a p²-kinetic MOND scalar cannot close the constraint algebra. -/

/-- The MOND interpolating kernel μ(y)=1−e^{-y} has derivative μ'(y)=e^{-y} (strictly positive: monotone). -/
theorem mu_kernel_deriv (y : ℝ) : HasDerivAt (fun t : ℝ => 1 - Real.exp (-t)) (Real.exp (-y)) y := by
  have h := (hasDerivAt_const y (1 : ℝ)).sub (hasDerivAt_expNeg y)
  have hv : (0 : ℝ) - Real.exp (-y) * (-1) = Real.exp (-y) := by ring
  rwa [hv] at h

/-- μ'(y) = e^{-y} > 0 for all y: the kernel is strictly monotone (the fact that drives the obstruction). -/
theorem mu_kernel_deriv_pos (y : ℝ) : 0 < Real.exp (-y) := Real.exp_pos _

/-- The p³ closure obstruction: matching the diffeomorphism generator forces A = 1/μ, and the cubic bracket
    coefficient (1/2) A A' equals −μ'/(2 μ³). -/
theorem closure_obstruction (mu mup : ℝ) (hmu : mu ≠ 0) :
    (1 / mu) * (-(mup) / mu ^ 2) / 2 = -mup / (2 * mu ^ 3) := by
  field_simp

/-- Closure requires the obstruction to vanish; with μ ≠ 0 that happens iff μ' = 0 — a flat (non-MOND) kernel. -/
theorem closure_needs_flat_kernel (mu mup : ℝ) (hmu : mu ≠ 0) :
    (-mup / (2 * mu ^ 3) = 0) ↔ mup = 0 := by
  have hb : (2 : ℝ) * mu ^ 3 ≠ 0 := mul_ne_zero two_ne_zero (pow_ne_zero 3 hmu)
  rw [div_eq_zero_iff]; simp [hb]

/-- CUSCUTON FORCED: for the exponential MOND kernel μ=1−e^{-y}, μ'=e^{-y} ≠ 0, so the closure obstruction
    −μ'/(2 μ³) is nonzero wherever μ ≠ 0. A p²-kinetic MOND scalar cannot close the constraint algebra; the
    non-propagating (cuscuton) branch is forced. -/
theorem cuscuton_forced (y : ℝ) (hmu : 1 - Real.exp (-y) ≠ 0) :
    -(Real.exp (-y)) / (2 * (1 - Real.exp (-y)) ^ 3) ≠ 0 := by
  intro hcontra
  rw [closure_needs_flat_kernel (1 - Real.exp (-y)) (Real.exp (-y)) hmu] at hcontra
  exact (Real.exp_pos (-y)).ne' hcontra
