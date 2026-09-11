/-
  Mondlean — Lean 4 / mathlib formalization of the load-bearing MATHEMATICS behind the de Sitter–MOND
  F(Q)Θ completion (fable_independent_2026 lanes L77–L90; astra's F(Q)Θ construction).

  IMPORTANT SCOPE. Lean certifies *mathematical theorems*, not physical laws. What is machine-checked here
  is the internal mathematics the physics rests on — kernel identities, the health-sign dichotomy, the
  affine cuscuton degeneracy, the pressureless-dust / stiff-term density structure, and the MOND limits.
  Whether the theory is "a law of nature" is decided by the falsifiable predictions (dwarf σ–R_gc EFE,
  flat a₀(z), subdominant scalar GW) confronting DATA — not by Lean, and not while the intrinsic BBN
  fine-tuning (L84/L87) and astra's open ADM/khronon gates stand.

  Theorems (99 as of 2026-09-10; all: exit 0, zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}):
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
    mu_kernel_deriv(_pos)         — μ'(y)=e^{-y}>0 (kernel strictly monotone, the fact driving the obstruction).
    closure_obstruction           — L95: matching the generator forces A=1/μ ⇒ obstruction (1/2)AA' = −μ'/(2μ³).
    closure_needs_flat_kernel     — L95: obstruction = 0 ⟺ μ' = 0 (a flat, non-MOND kernel).
    cuscuton_forced               — L95 (necessity): exp kernel ⇒ μ'≠0 ⇒ obstruction ≠ 0 ⇒ p²-scalar can't
                                    close ⇒ the non-propagating (cuscuton) branch is forced.
    obstruction_coeff             — L105: the obstruction coefficient is (1/2)·A·A' in the p²-kinetic coeff A.
    cuscuton_obstruction_vanishes — L105 (sufficiency): a cuscuton has A ≡ 0 ⇒ obstruction (1/2)AA' = 0
                                    IDENTICALLY, for ANY kernel slope.
    cuscuton_closes_monotone      — L105: on the cuscuton branch obstruction = 0 AND μ' = e^{-y} > 0 coexist
                                    (impossible in the canonical case) — closure compatible with a monotone kernel.
    csSq_canonical, csSq_aqual    — L106: c_s²(n)=1/(2n−1); n=1 luminal (c_s²=1), n=3/2 AQUAL (c_s²=1/2, a
                                    competing cone that corrupts the structure function).
    cuscuton_denom_zero           — L106: n=1/2 makes 2n−1 = 0 ⇒ c_s² diverges (infinite, causal sound speed).
    cuscuton_unique_infinite      — L106: 2n−1 = 0 ⟺ n = 1/2 — the cuscuton is the UNIQUE power with no finite
                                    competing cone ⇒ the metric-sector structure function stays h^{ij}.
    canonical_scalar_dof          — Dirac count: a canonical scalar (phase dim 2, no constraints) has 1
                                    propagating dof (a wave).
    cuscuton_scalar_dof           — L108: a cuscuton scalar (phase dim 2, second-class pair) has 0 dof — the
                                    machine-checked DOF face of L104/L105/L106.
    cam_auxiliary_zero_dof        — L108: astra's CAM finite-k count (P=6, F=0, S=6) ⇒ (6−0−6)/2 = 0 dof
                                    (no propagating MOND scalar; the scalar-sector closure count).
    fully_constrained_zero_dof    — general: a fully second-class-constrained sector (S=P, F=0) has 0 dof.
    (… L117–L128 theorems: clock_structure_function, cam_conformal_ghost, cam_strong_coupling,
        reduction_master_certificate, kfs_strictly_increasing, hybrid_pincer_no_interior [arithmetic only],
        yukawa_transmission_increasing, yukawa_no_window, twometric_*, ppn_alpha1_vanishes_iff_local_source,
        cuscuton_stiff_denominator_zero, cuscuton_sound_speed_denominator_zero, cuscuton_rho_eq_potential,
        cuscuton_pressureless_iff, cuscuton_dust_reproduces_friedmann — documented in README.md.)
    kessence_dust_stiff_decomposition — L137: quadratic K ⇒ 8πG̃ρ̄ = 2Λ + Q₀I₀a⁻³ + [I₀²/(4K₂)]a⁻⁶ (dust LINEAR,
                                    stiff QUADRATIC in the shift charge I₀) — exact identity.
    stiff_dust_coefficient_ratio,   — L137: stiff/dust coefficient ratio = I₀/(4K₂Q₀) (= published w₀ = the
    stiff_dust_term_ratio             L84 BBN ratio); the TERM ratio scales as a⁻³.
    stiff_dust_ratio_vanishes_iff   — L137: for quadratic K, ratio = 0 ⟺ I₀ = 0 (no dust without stiff).
    lv_kessence_sound_speed_scaling — L138: c_s² = 2c_Y/K_QQ with K_QQ = K_QQ⁰a⁻³ ⇒ c_s² = (2c_Y/K_QQ⁰)a³.
    lv_kessence_sound_speed_increasing — L138: that c_s² is strictly increasing in a (colder in the past).
    particle_sound_speed_decreasing — L138 control: a particle's c_s² = v₀²/a² is strictly DECREASING —
                                    the L125 velocity lemma is particle-specific.
    cuscuton_time_kinetic_affine    — L139: √((1−2εΨ)(τ̄̇+εδτ̇)²) = √(1−2εΨ)(τ̄̇+εδτ̇), affine in δτ̇ ⇒ the
                                    (δτ̇)² coefficient vanishes identically (0-DOF from the action).
    cuscuton_slaved_mode_identity   — L139: the elliptic solution δτ = −(a²τ̄̇S/μ²)/(k² + V″a²τ̄̇/μ²), 1/k².
    cuscuton_elliptic_slaving       — L139/L129: (aH/k)⁴ < 1e-4 whenever k/(aH) > 10.
    leaf_normal_no_frame_drag_source, — L139: the Route-2 momentum source −K_Q∂ᵢχ/N vanishes when ∂ᵢχ = 0,
    leaf_normal_frame_drag_source_iff   and (K_Q ≠ 0) ONLY then — gradient-driven, no F² frame-drag term.
    lapse_measured_charge_helmholtz — L139: K₂(Q₀(1−Ψ) − Q₀)² = K₂Q₀²Ψ² (the inherited Helmholtz mass).
    helmholtz_mass_cannot_be_switched_off — L139: that term is > 0 for K₂ > 0, Q₀, Ψ ≠ 0.
    fourth_power_error_budget       — L143: Var(4X − Y) with Cov = 0 equals 16 Var X + Var Y.
    fourth_power_velocity_binds,    — L143: σ_logv > 0.0335 ⇒ 16σ_logv² > 0.134²; 16·0.0335² = 0.134² exactly.
    fourth_power_velocity_threshold
-/
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.SpecialFunctions.Log.Basic
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

/-! ### Positive closure theorem (L105): the cuscuton branch escapes the obstruction.

    The general p³ closure obstruction coefficient is (1/2)·A·A', where A is the p²-kinetic coefficient.
    Canonical case: closure forces A = 1/μ, giving −μ'/(2μ³) ≠ 0 (cuscuton_forced above). CUSCUTON case:
    there is NO p² kinetic term (A ≡ 0, the momentum is constrained), so the obstruction vanishes
    identically — for ANY kernel slope — while the kernel stays strictly monotone. Lean certifies the
    algebraic identity and the coexistence; the full HDA closure invokes Afshordi–Chung–Geshnizjani and is
    physics, not Lean. -/

/-- The closure obstruction coefficient is (1/2)·A·A' in the p²-kinetic coefficient A. -/
theorem obstruction_coeff (A Aprime : ℝ) : A * Aprime / 2 = (1 / 2) * A * Aprime := by ring

/-- POSITIVE CLOSURE (cuscuton branch): a cuscuton has NO p² kinetic term, i.e. A = 0, so the closure
    obstruction (1/2)·A·A' vanishes IDENTICALLY — for ANY kernel slope A', monotone or not. -/
theorem cuscuton_obstruction_vanishes (Aprime : ℝ) : (0 : ℝ) * Aprime / 2 = 0 := by ring

/-- DECOUPLING / coexistence (the L105 sufficiency): on the cuscuton branch (A = 0) the obstruction is zero
    WHILE the MOND kernel stays strictly monotone (μ' = e^{-y} > 0). Closure and a genuine interpolating
    kernel coexist — impossible in the canonical case, where closure_needs_flat_kernel forces μ' = 0. -/
theorem cuscuton_closes_monotone (y : ℝ) :
    (0 : ℝ) * Real.exp (-y) / 2 = 0 ∧ 0 < Real.exp (-y) :=
  ⟨by ring, Real.exp_pos _⟩

/-! ### Sound-speed / structure-function theorem (L106): c_s²(n)=1/(2n−1); the cuscuton n=1/2 is the unique
    infinite-sound-speed power (no competing characteristic cone ⇒ the HDA structure function stays h^{ij}).
    Lean certifies the rational-function algebra of c_s²(n) and the uniqueness of the pole; the derivation
    c_s² = P_X/(P_X+2X P_XX) = 1/(2n−1) is in L106.py, and the structure-function principle is physics. -/

/-- The k-essence sound speed for a power-law kinetic term P ~ X^n is c_s² = 1/(2n−1) (derived in L106). -/
noncomputable def csSq (n : ℝ) : ℝ := 1 / (2 * n - 1)

/-- Canonical scalar (n=1) is luminal: c_s² = 1 = c_light (preserves h^{ij}, but P=X is not MOND). -/
theorem csSq_canonical : csSq 1 = 1 := by unfold csSq; norm_num

/-- Deep-MOND AQUAL (n=3/2, MOND placed in the KINETIC term) has c_s² = 1/2: a competing subluminal cone
    that corrupts the structure function (the covariant root of L95 and the AeST/aether pathologies). -/
theorem csSq_aqual : csSq (3 / 2) = 1 / 2 := by unfold csSq; norm_num

/-- CUSCUTON (n=1/2): the denominator 2n−1 vanishes, so c_s² diverges — the infinite (but causal) sound
    speed. An infinite cone is no finite competing cone, so the structure function reverts to h^{ij}. -/
theorem cuscuton_denom_zero : 2 * (1 / 2 : ℝ) - 1 = 0 := by norm_num

/-- UNIQUENESS: 2n−1 = 0 (infinite sound speed) iff n = 1/2 — the cuscuton is the UNIQUE kinetic power with
    no finite competing characteristic cone. Any other MOND-generating nonlinearity has a finite c_s². -/
theorem cuscuton_unique_infinite (n : ℝ) : 2 * n - 1 = 0 ↔ n = 1 / 2 := by
  constructor <;> intro h <;> linarith

/-! ### Dirac degree-of-freedom counting (L108: closure at the DOF level, astra's CAM finite-k count).

    The physical configuration DOF of a constrained system is  dof = (P − 2·F − S)/2, where P is the phase-
    space dimension (2 × #fields), F the number of first-class and S the number of second-class constraints.
    Lean certifies the COUNTING; the constraint structure itself (that the CAM auxiliary sector has 6
    second-class constraints at finite k, PB rank 6) is astra's Dirac computation (cuscuton_acceleration_
    mond_2026), and the full covariant τ-clock algebra + PPN remain open. The cuscuton's zero-DOF result
    here is the same fact as cuscuton_obstruction_vanishes (L105) and cuscuton_denom_zero (L106, c_s=∞). -/

/-- Dirac physical-configuration DOF: dof = (P − 2F − S)/2 (phase dim P, F first-class, S second-class). -/
def diracDOF (P F S : ℤ) : ℤ := (P - 2 * F - S) / 2

/-- A CANONICAL scalar (phase dim 2, no constraints) carries ONE propagating DOF: it is a wave. -/
theorem canonical_scalar_dof : diracDOF 2 0 0 = 1 := by decide

/-- A CUSCUTON scalar (phase dim 2, a second-class primary+secondary pair) carries ZERO propagating DOF:
    the momentum is constrained, not evolved — the machine-checked DOF face of L104/L105/L106. -/
theorem cuscuton_scalar_dof : diracDOF 2 0 2 = 0 := by decide

/-- The CAM AUXILIARY sub-sector (fields u, ℓ, Φ) at finite k: phase dim 6, 0 first-class, 6 second-class
    ⇒ (6 − 0 − 6)/2 = 0 physical DOF. SCOPE (corrected per astra's physical audit, commit 5943d5325, and
    L115): this counts ONLY the (u,ℓ,Φ) auxiliary toy sector; the FULL ADM additionally RETAINS a metric-
    scalar canonical pair (ζ, p) with a nonzero cubic Hamiltonian, so this does NOT certify the full CAM
    scalar DOF. It remains a correct count for the stated sub-sector. -/
theorem cam_auxiliary_zero_dof : diracDOF 6 0 6 = 0 := by decide

/-- General: a fully second-class-constrained sector (S = P, no first-class) has ZERO physical DOF — the
    structural reason a cuscuton/constrained sector cannot propagate, for any phase dimension P. -/
theorem fully_constrained_zero_dof (P : ℤ) : diracDOF P 0 P = 0 := by
  unfold diracDOF; simp

/-- Arithmetic identity 2 + diracDOF 6 0 6 = 2. SCOPE (corrected per astra 5943d5325 + L115): this was
    ORIGINALLY read as "CAM full linearized DOF = 2 = GR", but that interpretation is RETRACTED — it omitted
    the retained metric-scalar pair (ζ, p) that the full ADM keeps (with a nonzero cubic Hamiltonian, health
    undetermined). Lean certifies only the arithmetic (2 + 0 = 2); it does NOT certify that CAM's full
    linearized DOF equals GR's. Kept as an honest arithmetic fact, not a closure certificate. -/
theorem cam_total_linear_dof : (2 : ℤ) + diracDOF 6 0 6 = 2 := by decide

/-! ### Fleet synthesis (L117): the cuscuton CLOCK is healthy, but the MOND acceleration operator liberates
    a conformal GHOST. Lean certifies BOTH the healthy identity and the fatal one -- the honest verdict that
    the minimal CAM does NOT close into a ghost-free theory. (Three independent subagents + astra's audit.) -/

/-- HEALTHY CLOCK (agent 1): for the cuscuton clock's H_perp-density with F^2 = (p^2 - m g) g s^2, the crux
    identity (∂_p F^2)(∂_s F^2)/(4 F^2) = g p s holds -- {H_perp,H_perp} closes with the GR structure
    function γ^{xx}=g. The degree-1 clock kinetic term is healthy (ACDG). -/
theorem clock_structure_function (p s g m : ℝ) (h : (p^2 - m*g) * g * s^2 ≠ 0) :
    (2*p*g*s^2) * ((p^2 - m*g) * g * (2*s)) / (4 * ((p^2 - m*g) * g * s^2)) = g * p * s := by
  have h4 : (4 : ℝ) * ((p^2 - m*g) * g * s^2) ≠ 0 := mul_ne_zero (by norm_num) h
  rw [div_eq_iff h4]; ring

/-- FATAL GHOST (agent 3): the MOND acceleration term makes H_perp second-class (L116), so the GR conformal
    mode ζ survives with kinetic term -3M²ζ̇²; its homogeneous (k→0) Hamiltonian is H_0 = -p²/(12M²) < 0 --
    unbounded below, a ghost in the cosmological sector. The minimal CAM is NOT ghost-free. -/
theorem cam_conformal_ghost (M2 p : ℝ) (hM : 0 < M2) (hp : p ≠ 0) : -p^2 / (12 * M2) < 0 := by
  have h : 0 < p^2 / (12 * M2) := by positivity
  have e : -p^2 / (12 * M2) = -(p^2 / (12 * M2)) := by ring
  rw [e]; linarith

/-- STRONG COUPLING (agent 3): the surviving mode's reduced quadratic Hamiltonian H_red = M²k²ζ²(1-η)/η
    VANISHES at the physical MOND value η=1 -- zero quadratic action ⇒ no perturbative propagator ⇒ infinite
    strong coupling around Minkowski. -/
theorem cam_strong_coupling (M2 k zeta : ℝ) : M2 * k^2 * zeta^2 * (1 - 1) / 1 = 0 := by ring

/-! ### Health-branch transition-health certificate (L119/L121 Phase A): the AQUAL operator is elliptic for
    ALL accelerations -- a POSITIVE certificate, in contrast to CAM's nonelliptic lapse. When the MOND kernel
    is carried by a separate field's projected gradient, the AQUAL Hessian eigenvalues are μ=1-e^{-y}
    (transverse) and 1+(y-1)e^{-y}=Gpp(y)/2 (longitudinal), BOTH strictly positive for y>0. -/

/-- Transverse AQUAL-Hessian eigenvalue μ(y)=1-e^{-y} > 0 for y>0. -/
theorem mu_positive (y : ℝ) (hy : 0 < y) : 0 < 1 - Real.exp (-y) := by
  have h : Real.exp (-y) < 1 := by rw [Real.exp_lt_one_iff]; linarith
  linarith

/-- HEALTH-BRANCH TRANSITION HEALTH: both AQUAL-Hessian eigenvalues are strictly positive for all y>0 --
    transverse μ=1-e^{-y} and longitudinal 1+(y-1)e^{-y} (=Gpp/2, via Gpp_pos). So the AQUAL operator is
    ELLIPTIC across ALL accelerations, unlike CAM's lapse (nonelliptic for y>1). The transition pathology is
    removed, not relocated. -/
theorem aqual_hessian_transition_healthy (y : ℝ) (hy : 0 < y) :
    0 < 1 - Real.exp (-y) ∧ 0 < 1 + (y - 1) * Real.exp (-y) := by
  refine ⟨mu_positive y hy, ?_⟩
  have h := Gpp_pos hy
  simp only [Gpp] at h
  linarith

/-! ### Kernel-blind transition health (L122 reduction map): the ∇φ AQUAL operator is elliptic for ALL y and
    for EVERY standard kernel -- transition health comes from the SOURCING (separate field), not the kernel.
    Certified here for the 'simple' and 'standard' kernels via their closed-form longitudinal eigenvalues. -/

/-- SIMPLE kernel μ(y)=y/(1+y): transverse μ>0 and longitudinal (yμ)'=y(2+y)/(1+y)² > 0 for all y>0. -/
theorem mu_simple_transition_healthy (y : ℝ) (hy : 0 < y) :
    0 < y / (1 + y) ∧ 0 < y * (2 + y) / (1 + y) ^ 2 := by
  constructor <;> positivity

/-- STANDARD kernel μ(y)=y/√(1+y²): transverse μ>0 and longitudinal (yμ)'=y(2+y²)/(1+y²)^{3/2} > 0 ∀ y>0. -/
theorem mu_standard_transition_healthy (y : ℝ) (hy : 0 < y) :
    0 < y / Real.sqrt (1 + y ^ 2) ∧ 0 < y * (2 + y ^ 2) / Real.sqrt (1 + y ^ 2) ^ 3 := by
  have hs : 0 < Real.sqrt (1 + y ^ 2) := Real.sqrt_pos.mpr (by positivity)
  constructor <;> positivity

/-- Ghost SEPARABILITY (L123): the conformal-ghost bracket {p_n,S_n} = −2M²k²η vanishes iff η=0 (η = the
    coefficient of MOND sourced from the LAPSE). So a dark sector that does NOT source MOND from the lapse
    (η_dust=0) is ghost-free: the conformal ghost was a lapse-sourcing artifact, not a property of an a⁻³
    density. A CMB-safe theory is not blocked by the ghost. -/
theorem dust_ghost_separable (M2 k η : ℝ) (hM : M2 ≠ 0) (hk : k ≠ 0) :
    -2 * M2 * k ^ 2 * η = 0 ↔ η = 0 := by
  constructor
  · intro h
    have h2 : (-2 * M2 * k ^ 2) ≠ 0 := by
      have : k ^ 2 ≠ 0 := pow_ne_zero 2 hk
      simp [mul_ne_zero, hM, this]
    rcases mul_eq_zero.mp h with h3 | h3
    · exact absurd h3 h2
    · exact h3
  · intro h; rw [h]; ring

/-! ### MASTER CERTIFICATE (L124): the machine-checked mathematical spine of the parameter-space reduction.

    SCOPE (read carefully). Lean certifies the algebraic/analytic FACTS below; it does NOT certify a complete
    physical theory of gravity. The physics that remains outside Lean -- full nonlinear constraint closure,
    PPN β/α_i, the cosmological Boltzmann third-peak fit, and the a₀ coefficient -- is unproven, and the
    honest verdict of the reduction (L123) is that the viable all-gates theory is HEALTHY MOND + a minimal
    DECOUPLED dark sector, NOT pure MOND. This theorem merely CONJOINS the load-bearing lemmas of the
    reduction into one statement, so "the certificate for all of it" is a single object. Each conjunct is one
    of the established theorems above. -/
theorem reduction_master_certificate
    (y M f p k η mu mup Aprime : ℝ)
    (hy : 0 < y) (hM : 0 < M) (hf : f ≠ 0) (hp : p ≠ 0) (hk : k ≠ 0) (hmu : mu ≠ 0) :
    -- (1) health dichotomy: G''(y) > 0 for y>0 (stable massive mode off the zero-field point)
    (0 < Gpp y)
    -- (2) the MOND term is cubic: G(0)=G'(0)=G''(0)=0
    ∧ (G 0 = 0 ∧ Gp 0 = 0 ∧ Gpp 0 = 0)
    -- (3) ELIMINATION (L95): a propagating p²-MOND scalar closes only for a FLAT (non-MOND) kernel
    ∧ ((-mup / (2 * mu ^ 3) = 0) ↔ mup = 0)
    -- (4) SURVIVAL (L105): the cuscuton branch's closure obstruction vanishes identically (A≡0)
    ∧ ((0 : ℝ) * Aprime / 2 = 0)
    -- (5) the cuscuton is the unique infinite-sound-speed kinetic power (n=1/2)
    ∧ (2 * (1 / 2 : ℝ) - 1 = 0)
    -- (6) TRANSITION HEALTH (health branch): the AQUAL operator is elliptic for all y (both eigenvalues > 0)
    ∧ (0 < 1 - Real.exp (-y) ∧ 0 < 1 + (y - 1) * Real.exp (-y))
    -- (7) BBN horn of the pincer: the intrinsic a⁻⁶ stiff coefficient is nonzero
    ∧ (-(M ^ 2) / (3 * f ^ 2) ≠ 0)
    -- (8) the lapse-sourced conformal mode is a GHOST (H₀ < 0) -- why MOND must not be lapse-sourced
    ∧ (-p ^ 2 / (12 * M) < 0)
    -- (9) SEPARABILITY (L123): a decoupled dark sector (η=0) does NOT re-liberate the ghost
    ∧ (-2 * M * k ^ 2 * η = 0 ↔ η = 0) :=
  ⟨Gpp_pos hy,
   cubic_leading,
   closure_needs_flat_kernel mu mup hmu,
   cuscuton_obstruction_vanishes Aprime,
   cuscuton_denom_zero,
   aqual_hessian_transition_healthy y hy,
   stiff_coeff_ne_zero M f (ne_of_gt hM) hf,
   cam_conformal_ghost M p hM hp,
   dust_ghost_separable M k η (ne_of_gt hM) hk⟩

/-! ### The cosmology DOUBLE no-go (L123 + L125): pure MOND fails the CMB, and the minimal decoupled-dark-
    sector hybrid ALSO fails via a mechanism-independent VELOCITY-ORDERING lemma. -/

/-- Velocity-ordering: a decoupled collisionless species has v_rms ∝ 1/a, so its free-streaming clustering
    cutoff k_fs(a) = a/v0 is strictly INCREASING in a (v0>0). -/
theorem kfs_strictly_increasing (v0 a1 a2 : ℝ) (hv : 0 < v0) (h : a1 < a2) :
    a1 / v0 < a2 / v0 := by gcongr

/-- ⚠️ PHYSICAL INTERPRETATION RETRACTED 2026-09-10 (see L136). The ARITHMETIC below is true and stands:
    from k < a_rec/v0 and a_rec < a_now it follows that k < a_now/v0. What is RETRACTED is the physical
    reading that this implies "cold-enough-for-the-CMB ⟹ clusters-in-galaxies". That was a category error:
    a/v0 is an INSTANTANEOUS ratio, whereas the transfer-function cutoff is set by the CUMULATIVE COMOVING
    free-streaming distance, which CONVERGES and is therefore FROZEN — it does not migrate downward. A single
    species can be cold at CMB scales and suppressed at galaxy scales simultaneously. Do NOT cite this
    theorem as a physical no-go; it is arithmetic about a/v0 only. -/
theorem hybrid_pincer_no_interior (v0 k a_rec a_now : ℝ) (hv : 0 < v0)
    (h_order : a_rec < a_now) (h_cmb : k < a_rec / v0) : k < a_now / v0 :=
  lt_trans h_cmb (kfs_strictly_increasing v0 a_rec a_now hv h_order)

/-! ### The TWO-METRIC (bimetric) branch dies on BOTH decisive gates (L126), and the health branch clears
    the PPN α₁ preferred-frame gate that killed AeST (α₁-agent). -/

/-- GATE 7 (CMB): the Fourier transmission of a massive graviton η(k)=k²/(k²+m²) is STRICTLY INCREASING in
    k — for 0 ≤ k₁ < k₂ and m ≠ 0, η(k₁) < η(k₂). A graviton mass is a HIGH-PASS force filter (passes short
    range, suppresses long range) — the WRONG sign for a CMB-driving + galaxy-smoothing (low-pass) window. -/
theorem yukawa_transmission_increasing (k1 k2 m : ℝ)
    (hk1 : 0 ≤ k1) (h : k1 < k2) (hm : m ≠ 0) :
    k1 ^ 2 / (k1 ^ 2 + m ^ 2) < k2 ^ 2 / (k2 ^ 2 + m ^ 2) := by
  have hm2 : 0 < m ^ 2 := by positivity
  have d1 : 0 < k1 ^ 2 + m ^ 2 := by positivity
  have d2 : 0 < k2 ^ 2 + m ^ 2 := by positivity
  have hk12 : k1 ^ 2 < k2 ^ 2 := by nlinarith [h, hk1]
  have d1' : (k1 ^ 2 + m ^ 2) ≠ 0 := ne_of_gt d1
  have d2' : (k2 ^ 2 + m ^ 2) ≠ 0 := ne_of_gt d2
  have expand : k2 ^ 2 / (k2 ^ 2 + m ^ 2) - k1 ^ 2 / (k1 ^ 2 + m ^ 2)
      = (m ^ 2 * (k2 ^ 2 - k1 ^ 2)) / ((k2 ^ 2 + m ^ 2) * (k1 ^ 2 + m ^ 2)) := by
    field_simp; ring
  have hnum : 0 < m ^ 2 * (k2 ^ 2 - k1 ^ 2) := mul_pos hm2 (by linarith)
  have hden : 0 < (k2 ^ 2 + m ^ 2) * (k1 ^ 2 + m ^ 2) := mul_pos d2 d1
  have key : 0 < k2 ^ 2 / (k2 ^ 2 + m ^ 2) - k1 ^ 2 / (k1 ^ 2 + m ^ 2) := by
    rw [expand]; exact div_pos hnum hden
  linarith

/-- GATE 7 (CMB), F3 — the mass-independent kill: no graviton mass gives BOTH CMB-driving and
    galaxy-smoothness. Since η is increasing, k_CMB < k_gal, and the required thresholds satisfy c₂ < c₁,
    one cannot have η(k_CMB,m) ≥ c₁ AND η(k_gal,m) ≤ c₂ — the window has the wrong ordering for EVERY m. -/
theorem yukawa_no_window (kC kG m c1 c2 : ℝ)
    (hkC : 0 ≤ kC) (hk : kC < kG) (hm : m ≠ 0) (hc : c2 < c1)
    (hcmb : c1 ≤ kC ^ 2 / (kC ^ 2 + m ^ 2))
    (hgal : kG ^ 2 / (kG ^ 2 + m ^ 2) ≤ c2) : False := by
  have hmono := yukawa_transmission_increasing kC kG m hkC hk hm
  linarith

/-- GATE 5 (mode health): the MOND acceleration a = −2(2u₀+u₁) and the transverse-vector Box² Ostrogradsky
    ghost coefficient −(λ/2)(2u₀+u₁) share the SAME factor (2u₀+u₁). So with λ ≠ 0 they vanish together:
    MOND-alive (a≠0) ⟺ ghost-on. The only ghost-free point 2u₀+u₁=0 kills MOND. -/
theorem twometric_mond_ghost_linked (u0 u1 lam : ℝ) (hlam : lam ≠ 0) :
    (-2 * (2 * u0 + u1) = 0) ↔ (-(lam / 2) * (2 * u0 + u1) = 0) := by
  constructor
  · intro h
    have hs : 2 * u0 + u1 = 0 := by linarith
    rw [hs, mul_zero]
  · intro h
    rcases mul_eq_zero.mp h with h1 | h1
    · exact absurd (by linarith [neg_eq_zero.mp h1] : lam = 0) hlam
    · rw [h1, mul_zero]

/-- GATE 5: the transverse-vector time-kinetic matrix has NEGATIVE determinant (a negative-norm ghost mode).
    Minkowski: det W = (−2)(9/2) = −9 < 0. -/
theorem twometric_detW_negative : (-2 : ℝ) * (9 / 2) < 0 := by norm_num

/-- GATE 5: on a nonzero MOND background det W = −8 M₁² ≤ 0 (=0 only at M₁=0, i.e. M′(T̄)=0 = no MOND) — the
    ghost is robust, not a Minkowski artifact (closes the exact-function escape). -/
theorem twometric_detW_bg_nonpos (M1 : ℝ) : -8 * M1 ^ 2 ≤ 0 := by nlinarith [sq_nonneg M1]

/-- PPN α₁ of the single-metric HEALTH branch: the preferred-frame parameter is α₁ = −8·c_pf, where c_pf is
    the coefficient of a LOCAL frame-drag source ρ w_i in the g₀ᵢ momentum sector. The cuscuton clock is
    exactly shift-independent (∂S/∂Nⁱ = 0 to all orders) and leaf-projection kills φ's frame-drag ⇒ c_pf = 0
    ⇒ α₁ = 0, clearing the |α₁|<1e-4 gate that killed AeST (whose aether VECTOR gave an O(1) c_pf,
    α₁ = −2(K_B+2)). α₁ ≠ 0 ⟺ c_pf ≠ 0 (validated positive control). -/
theorem ppn_alpha1_vanishes_iff_local_source (c_pf : ℝ) :
    (-8 * c_pf = 0) ↔ (c_pf = 0) := by
  constructor
  · intro h; linarith
  · intro h; rw [h]; ring

/-! ### L128: the CUSCUTON is the degeneracy point of the stiff-genericity no-go, and with a forced
    quadratic potential it is EXACTLY pressureless a⁻³ field-dust — at the price of c_s² = ∞.
    Parametrisation: s = √X > 0 (so X = s², |φ̇| = s), P = μ²s − V, P_X = μ²/(2s), P_XX = −μ²/(4s³). -/

/-- STIFF-ESCAPE: the L87 stiff-genericity obstruction coefficient 2X·P_XX + P_X vanishes IDENTICALLY for
    the cuscuton. So the theorem "no a⁻⁶ stiff ⟺ no a⁻³ dust" (whose statement divides by this coefficient)
    is degenerate at the cuscuton and does NOT obstruct it. -/
theorem cuscuton_stiff_denominator_zero (mu2 s : ℝ) (hs : 0 < s) :
    mu2 / (2 * s) + 2 * s ^ 2 * (-(mu2 / (4 * s ^ 3))) = 0 := by
  have : s ≠ 0 := ne_of_gt hs
  field_simp
  ring

/-- The SAME vanishing denominator is the cuscuton's infinite sound speed: c_s² = P_X/(P_X + 2X·P_XX) has a
    zero denominator, so c_s² = ∞ and the Jeans length is infinite (smooth at every sub-horizon scale).
    The stiff-escape and the non-clustering are ONE algebraic fact, and V does not enter it. -/
theorem cuscuton_sound_speed_denominator_zero (mu2 s : ℝ) (hs : 0 < s) :
    mu2 / (2 * s) + 2 * s ^ 2 * (-(mu2 / (4 * s ^ 3))) = 0 :=
  cuscuton_stiff_denominator_zero mu2 s hs

/-- The cuscuton energy density is PURELY the potential: ρ = 2X·P_X − P = V exactly (the sqrt-kinetic
    contribution cancels identically). -/
theorem cuscuton_rho_eq_potential (mu2 s V : ℝ) (hs : 0 < s) :
    2 * s ^ 2 * (mu2 / (2 * s)) - (mu2 * s - V) = V := by
  have : s ≠ 0 := ne_of_gt hs
  field_simp
  ring

/-- The cuscuton is PRESSURELESS exactly when μ²|φ̇| = V — a condition on the potential, not on initial
    data (p = P = μ²s − V). -/
theorem cuscuton_pressureless_iff (mu2 s V : ℝ) : mu2 * s - V = 0 ↔ mu2 * s = V := by
  constructor <;> intro h <;> linarith

/-- FIELD-DUST: imposing w=0 with the cuscuton FRW equation V′ = −3μ²H forces V″ = 12πGμ⁴ (constant), i.e.
    a QUADRATIC potential V = 6πGμ⁴φ², whose implied H(φ) = −4πGμ²φ reproduces the Friedmann equation
    ρ = 3H²/(8πG) EXACTLY. A field with ZERO propagating DOF and no ghost supplies exact a⁻³ dust. -/
theorem cuscuton_dust_reproduces_friedmann (G mu2 phi pi : ℝ) (hG : 0 < G) (hpi : 0 < pi) :
    3 * (-(4 * pi * G * mu2 * phi)) ^ 2 / (8 * pi * G)
      = 6 * pi * G * mu2 ^ 2 * phi ^ 2 := by
  have h1 : pi ≠ 0 := ne_of_gt hpi
  have h2 : G ≠ 0 := ne_of_gt hG
  field_simp
  ring

/-! ### L137–L139 (the surviving corner) + L143: the quadratic-K dust/stiff structure and its non-quadratic
    escape (L137), the Lorentz-violating k-essence sound speed (L138), the cuscuton transplant — Route 1's
    elliptic slaving, Route 2's leaf-normal momentum source and inherited Helmholtz mass (L139) — and the
    fourth-power error budget of the decisive a₀(z) measurement (L143). Every statement below is algebra
    or a real-number inequality; none certifies a Boltzmann run, a PPN solve or a collapse computation. -/

/-- L137 (A1): for a QUADRATIC shift-symmetric k-essence K(Q) = −2Λ + K₂(Q−Q₀)² whose conserved shift charge
    obeys dK/dQ = 2K₂(Q−Q₀) = I₀/a³, the FLRW energy density 8πG̃ρ̄ = Q·K_Q − K decomposes EXACTLY as
    2Λ + Q₀I₀·a⁻³ + [I₀²/(4K₂)]·a⁻⁶ — a Λ-constant, an a⁻³ DUST term LINEAR in I₀, and an a⁻⁶ STIFF term
    QUADRATIC in I₀. This is the published AeST Higgs-phase background and it is the SAME structure as the
    repo's L84/L87 density (dust ∝ A·C, stiff ∝ C²). SCOPE: an identity for quadratic K only (K₂, a > 0); it
    says nothing about cosh/exp K, for which L137 shows numerically that the a⁻⁶ partner is ABSENT — so
    "no stiff-free dust" (L87/L123c) is refuted as a general claim while standing for quadratic K. -/
theorem kessence_dust_stiff_decomposition (K2 Q0 I0 Lam a Q : ℝ) (hK : 0 < K2) (ha : 0 < a)
    (hcharge : 2 * K2 * (Q - Q0) = I0 / a ^ 3) :
    Q * (I0 / a ^ 3) - (-2 * Lam + K2 * (Q - Q0) ^ 2)
      = 2 * Lam + Q0 * I0 / a ^ 3 + I0 ^ 2 / (4 * K2) / a ^ 6 := by
  have hK' : K2 ≠ 0 := ne_of_gt hK
  have ha' : a ≠ 0 := ne_of_gt ha
  have hQ : Q = Q0 + I0 / (2 * K2 * a ^ 3) := by
    have h3 : (a ^ 3) ≠ 0 := pow_ne_zero 3 ha'
    have h := (eq_div_iff h3).mp hcharge
    have h' : I0 / (2 * K2 * a ^ 3) = Q - Q0 := by
      rw [div_eq_iff (by positivity)]
      linear_combination (-1 : ℝ) * h
    linarith
  subst hQ
  field_simp
  ring

/-- L137 (A2/A3): the ratio of the stiff to the dust COEFFICIENT is I₀/(4K₂Q₀) — a number that carries no a.
    Evaluated today (a = 1) it is the published w₀ = P_stiff(1)/ρ_dust(1) AND the repo's L84 BBN fine-tuning
    ratio Ω_stiff,0/Ω_dust,0: the two are ONE object. Holds for I₀ = 0 too (both sides 0). -/
theorem stiff_dust_coefficient_ratio (K2 Q0 I0 : ℝ) (hK : K2 ≠ 0) (hQ : Q0 ≠ 0) :
    (I0 ^ 2 / (4 * K2)) / (Q0 * I0) = I0 / (4 * K2 * Q0) := by
  by_cases hI : I0 = 0
  · simp [hI]
  · field_simp

/-- L137, the honest a-dependence: the ratio of the stiff TERM to the dust TERM at scale factor a is
    [I₀/(4K₂Q₀)]·a⁻³ — the stiff piece overtakes the dust going back in time, which is exactly why the
    coefficient ratio must be tuned to ≲1e-8 to survive BBN (the L87 horn, for quadratic K). -/
theorem stiff_dust_term_ratio (K2 Q0 I0 a : ℝ) (hK : K2 ≠ 0) (hQ : Q0 ≠ 0) (ha : a ≠ 0) :
    (I0 ^ 2 / (4 * K2) / a ^ 6) / (Q0 * I0 / a ^ 3) = (I0 / (4 * K2 * Q0)) / a ^ 3 := by
  by_cases hI : I0 = 0
  · simp [hI]
  · field_simp

/-- L137: for quadratic K the stiff/dust ratio I₀/(4K₂Q₀) vanishes IFF the shift charge I₀ vanishes — i.e.
    quadratic K cannot carry dust (∝ Q₀I₀) without its a⁻⁶ stiff partner (∝ I₀²). This is the precise
    content of L87 that survives; its converse for NON-quadratic K is false (L137). -/
theorem stiff_dust_ratio_vanishes_iff (K2 Q0 I0 : ℝ) (hK : K2 ≠ 0) (hQ : Q0 ≠ 0) :
    I0 / (4 * K2 * Q0) = 0 ↔ I0 = 0 := by
  have hd : (4 * K2 * Q0) ≠ 0 := by positivity
  rw [div_eq_zero_iff]
  exact or_iff_left hd

/-- L138 (B3): for a Lorentz-violating k-essence with leaf-projected gradient term c_Y|Dχ|², the sound speed
    is c_s² = 2c_Y/K_QQ(a). If K_QQ = K_QQ⁰·a⁻³ (the cosh/exp kinetic functions on the charge trajectory)
    then c_s² = (2c_Y/K_QQ⁰)·a³ EXACTLY. SCOPE: the identity only; that K_QQ ∝ a⁻³ for cosh/exp K is the
    L138 numerical result, not certified here. -/
theorem lv_kessence_sound_speed_scaling (cY KQQ0 a : ℝ) (hK : 0 < KQQ0) (ha : 0 < a) :
    2 * cY / (KQQ0 / a ^ 3) = (2 * cY / KQQ0) * a ^ 3 := by
  have hK' : KQQ0 ≠ 0 := ne_of_gt hK
  have ha' : a ≠ 0 := ne_of_gt ha
  field_simp

/-- L138: the running sound speed c_s² = (2c_Y/K_QQ⁰)·a³ is STRICTLY INCREASING in a for c_Y, K_QQ⁰ > 0 —
    such a dust is COLDER at recombination than today, the opposite ordering to a particle. -/
theorem lv_kessence_sound_speed_increasing (cY KQQ0 a1 a2 : ℝ) (hc : 0 < cY) (hK : 0 < KQQ0)
    (h1 : 0 < a1) (h : a1 < a2) :
    (2 * cY / KQQ0) * a1 ^ 3 < (2 * cY / KQQ0) * a2 ^ 3 := by
  have hpos : 0 < 2 * cY / KQQ0 := by positivity
  have hpow : a1 ^ 3 < a2 ^ 3 := by gcongr
  exact mul_lt_mul_of_pos_left hpow hpos

/-- L138 (B1, the control): a decoupled free-streaming PARTICLE has v_rms = v₀/a, so c_s² = v₀²/a² is
    STRICTLY DECREASING in a. Together with `lv_kessence_sound_speed_increasing` this is why the L125
    velocity lemma is particle-specific, NOT mechanism-independent: the two mechanisms order c_s²(a) in
    OPPOSITE directions, and the lemma's hypothesis is the particle one. -/
theorem particle_sound_speed_decreasing (v0 a1 a2 : ℝ) (hv : 0 < v0) (h1 : 0 < a1) (h : a1 < a2) :
    v0 ^ 2 / a2 ^ 2 < v0 ^ 2 / a1 ^ 2 := by
  have hv2 : 0 < v0 ^ 2 := by positivity
  have hpow : a1 ^ 2 < a2 ^ 2 := by gcongr
  exact div_lt_div_of_pos_left hv2 (by positivity) hpow

/-- L139 (C2-1), Route 1's obstruction at its root: at zero spatial gradient the cuscuton kinetic term
    √(−(∂τ)²) = √((1−2εΨ)(τ̄̇+εδτ̇)²) equals √(1−2εΨ)·(τ̄̇+εδτ̇) EXACTLY, which is AFFINE in δτ̇ — so the
    (δτ̇)² coefficient vanishes identically (to ALL orders, not just second). The perturbation has no
    time-kinetic term; this is the 0-DOF property seen from the action. Companion to the derivative form
    `cuscuton_stiff_denominator_zero` (P_X + 2X·P_XX = 0). Hypotheses: the usual positivity of the lapse
    factor and of the background clock rate. -/
theorem cuscuton_time_kinetic_affine (eps Psi tb d : ℝ) (h1 : 0 ≤ 1 - 2 * eps * Psi)
    (h2 : 0 ≤ tb + eps * d) :
    Real.sqrt ((1 - 2 * eps * Psi) * (tb + eps * d) ^ 2)
      = Real.sqrt (1 - 2 * eps * Psi) * (tb + eps * d) := by
  rw [Real.sqrt_mul h1, Real.sqrt_sq h2]

/-- L139 (C2-3): the elliptic constraint (μ_c²k²/(a²τ̄̇) + V″)δτ = −S is solved ALGEBRAICALLY and the solution
    can be written δτ = −(a²τ̄̇S/μ_c²)/(k² + V″a²τ̄̇/μ_c²) — the 1/k² sub-horizon fall-off is manifest, with
    k²δτ → −a²τ̄̇S/μ_c². A slaved, 1/k²-suppressed δτ carries no independent growing mode: background a⁻³
    dust ≠ clustering dust (Route 1 obstructed). Exact identity (a, τ̄̇, μ_c² ≠ 0; Lean's x/0 = 0 covers a
    vanishing denominator on both sides). -/
theorem cuscuton_slaved_mode_identity (S mu2 k a tb Vpp : ℝ) (hmu : mu2 ≠ 0)
    (ha : a ≠ 0) (htb : tb ≠ 0) :
    -S / (mu2 * k ^ 2 / (a ^ 2 * tb) + Vpp)
      = -(a ^ 2 * tb * S / mu2) / (k ^ 2 + Vpp * a ^ 2 * tb / mu2) := by
  have hc : a ^ 2 * tb / mu2 ≠ 0 := by positivity
  have e1 : -(a ^ 2 * tb * S / mu2) = (a ^ 2 * tb / mu2) * (-S) := by ring
  have e2 : k ^ 2 + Vpp * a ^ 2 * tb / mu2
      = (a ^ 2 * tb / mu2) * (mu2 * k ^ 2 / (a ^ 2 * tb) + Vpp) := by
    field_simp
  rw [e1, e2, mul_div_mul_left _ _ hc]

/-- L139 (C2-4) / L129: the sub-horizon suppression factor of a slaved elliptic mode relative to clustering
    dust, (aH/k)⁴, is below 1e-4 whenever k/(aH) > 10 — at third-peak scales (k/aH ~ 10²) it is ~1e-8, the
    order of the 4e-5 δ_τ/δ_CDM found numerically. A real-number inequality; the identification of the
    ratio with (aH/k)⁴ is the L129/L139 scaling argument, not certified here. -/
theorem cuscuton_elliptic_slaving (k a H : ℝ) (hk : 0 < k) (ha : 0 < a) (hH : 0 < H)
    (hsub : 10 < k / (a * H)) :
    (a * H / k) ^ 4 < 1e-4 := by
  have haH : 0 < a * H := mul_pos ha hH
  have hx : 0 ≤ a * H / k := le_of_lt (div_pos haH hk)
  have hx' : a * H / k < 1 / 10 := by
    have := one_div_lt_one_div_of_lt (by norm_num : (0:ℝ) < 10) hsub
    rwa [one_div_div] at this
  calc (a * H / k) ^ 4 < (1 / 10) ^ 4 := by gcongr
    _ = 1e-4 := by norm_num

/-- L139 (C3-4), Route 2's decisive α₁ point: with Q = (χ̇ − Nⁱ∂ᵢχ)/N measured along the clock's leaf normal,
    the dark sector's momentum-constraint source is ∂L/∂Nⁱ = −K_Q·∂ᵢχ/N, proportional to the LOCAL spatial
    gradient of χ; it vanishes wherever ∂ᵢχ = 0 (the FLRW background, any locally homogeneous dark field).
    No F² vector kinetic term is present, so AeST's O(1) frame-drag source (and its α₁) is simply absent.
    SCOPE: the O(w) PPN solve with χ is NOT done; this certifies only the local source. -/
theorem leaf_normal_no_frame_drag_source (KQ dchi N : ℝ) (_hN : N ≠ 0) (h : dchi = 0) :
    -(KQ * dchi) / N = 0 := by
  rw [h, mul_zero, neg_zero, zero_div]

/-- L139 (C3-4), positive control: for a nonzero charge density K_Q the source −K_Q·∂ᵢχ/N vanishes IFF the
    local gradient ∂ᵢχ vanishes — the source is exactly gradient-driven, never a velocity (frame-drag) term. -/
theorem leaf_normal_frame_drag_source_iff (KQ dchi N : ℝ) (hN : N ≠ 0) (hK : KQ ≠ 0) :
    -(KQ * dchi) / N = 0 ↔ dchi = 0 := by
  rw [div_eq_zero_iff, neg_eq_zero, mul_eq_zero]
  constructor
  · rintro ((h | h) | h)
    · exact absurd h hK
    · exact h
    · exact absurd h hN
  · intro h; exact Or.inl (Or.inr h)

/-- L139 (C3-8), the COST inherited by the transplant: because Q is measured with the LOCAL lapse,
    Q → Q₀(1−Ψ) in the weak field, and expanding the quadratic K about its minimum gives
    K(Q₀(1−Ψ)) = K₂Q₀²Ψ² EXACTLY — the same "mass term for the potential" μ²Φ² that AeST has, hence the
    Helmholtz (oscillatory quasistatic) regime and the published weak-lensing tension. -/
theorem lapse_measured_charge_helmholtz (K2 Q0 Psi : ℝ) :
    K2 * (Q0 * (1 - Psi) - Q0) ^ 2 = K2 * Q0 ^ 2 * Psi ^ 2 := by ring

/-- L139 (C3-8): the induced Helmholtz mass term is STRICTLY POSITIVE for K₂ > 0 (required for dust AND
    health), Q₀ ≠ 0 and Ψ ≠ 0 — it cannot be switched off, only pushed out of range by small Q₀. -/
theorem helmholtz_mass_cannot_be_switched_off (K2 Q0 Psi : ℝ) (hK : 0 < K2) (hQ : Q0 ≠ 0)
    (hP : Psi ≠ 0) : 0 < K2 * Q0 ^ 2 * Psi ^ 2 := by positivity

/-- L143, the decisive-measurement error budget: with log a₀ = 4·log v − log M_b and INDEPENDENT errors
    (covariance 0), the bilinear variance propagation Var(4X−Y) = 4²Var X + 2·4·(−1)Cov + (−1)²Var Y
    collapses to σ²(log a₀) = 16σ²(log v) + σ²(log M_b): the FOURTH POWER binds. Algebra only; the
    independence and Gaussian-propagation assumptions are the physics inputs. -/
theorem fourth_power_error_budget (vx vy cov : ℝ) (hind : cov = 0) :
    4 ^ 2 * vx + 2 * 4 * (-1) * cov + (-1) ^ 2 * vy = 16 * vx + vy := by
  rw [hind]; ring

/-- L143: the velocity term ALONE exceeds the registered σ(log a₀) ≤ 0.134 dex budget as soon as
    σ(log v) > 0.0335 dex (= 0.134/4) — i.e. ~8% on v_flat blows the budget regardless of M_b. -/
theorem fourth_power_velocity_binds (sv : ℝ) (h : 0.0335 < sv) :
    0.134 ^ 2 < 16 * sv ^ 2 := by
  nlinarith [mul_pos (sub_pos.mpr h) (by linarith : (0:ℝ) < sv + 0.0335)]

/-- L143: the threshold is exact — 16·(0.0335)² = (0.134)², so 0.0335 dex on log v spends the ENTIRE budget
    with nothing left for the baryonic mass. -/
theorem fourth_power_velocity_threshold : (16 : ℝ) * 0.0335 ^ 2 = 0.134 ^ 2 := by norm_num

/-! ### L156–L158: the GDM sound-speed loophole and the BAROTROPIC bounds (growth ceiling, density–time
    duality, Jeans ordering). Parametrisation: c_s² ∝ a^p. -/

/-- JEANS ORDERING: with c_s² ∝ a^p the comoving Jeans wavenumber goes as a^{−(1+p)/2}, so the clustering set
    GROWS with a (exponent positive) iff p < −1. A decoupled particle species sits at p = −2 (v_rms ∝ 1/a) —
    the ENTIRE content of the L125 velocity lemma is this one corner of a one-parameter family. -/
theorem jeans_exponent_positive_iff (p : ℝ) : 0 < -(1 + p) / 2 ↔ p < -1 := by
  constructor <;> intro h <;> linarith

/-- The particle case p = −2 lies in the growing-clustering corner; p = 0 (constant c_s) and p = 3
    (the L139 running sector) do NOT. -/
theorem particle_corner_and_escapes : (-2 : ℝ) < -1 ∧ ¬ ((0 : ℝ) < -1) ∧ ¬ ((3 : ℝ) < -1) := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- BAROTROPIC EQUATION OF STATE from a power-law sound speed: for P = P(ρ) with c_s² = c·(ρ/ρ₀)^{−p/3}
    (i.e. c_s² ∝ a^p on an a⁻³ background) and p < 3, integrating dP = c_s² dρ gives w = P/ρ = 3c_s²/(3−p).
    Certified here as the algebraic content: the ratio w/c_s² = 3/(3−p), and for growing sound speed
    (p ≥ 0) one has c_s² ≤ w — THEOREM A's inequality. -/
theorem barotropic_w_ratio (c p : ℝ) (hc : 0 < c) (hp : p < 3) :
    (3 * c / (3 - p)) / c = 3 / (3 - p) ∧ (0 ≤ p → c ≤ 3 * c / (3 - p)) := by
  have h3 : 0 < 3 - p := by linarith
  have hne : (3 - p) ≠ 0 := ne_of_gt h3
  have hcne : c ≠ 0 := ne_of_gt hc
  refine ⟨by field_simp, ?_⟩
  intro hp0
  rw [le_div_iff₀ h3]
  nlinarith

/-- THE GROWTH CEILING'S COST: the background cost ratio w/c_s² = 3/(3−p) is strictly increasing in p on
    p < 3, and is UNBOUNDED as p → 3⁻ (for every M ≥ 1 the value M is attained at p = 3 − 3/M). So p = 3 is a
    genuine ceiling for a barotropic fluid: growing faster buys less galaxy protection at diverging cost. -/
theorem barotropic_cost_increasing (p1 p2 : ℝ) (h12 : p1 < p2) (h2 : p2 < 3) :
    3 / (3 - p1) < 3 / (3 - p2) := by
  have a1 : 0 < 3 - p1 := by linarith
  have a2 : 0 < 3 - p2 := by linarith
  have n1 : (3 - p1) ≠ 0 := ne_of_gt a1
  have n2 : (3 - p2) ≠ 0 := ne_of_gt a2
  have expand : 3 / (3 - p2) - 3 / (3 - p1) = 3 * (p2 - p1) / ((3 - p1) * (3 - p2)) := by
    field_simp; ring
  have key : 0 < 3 / (3 - p2) - 3 / (3 - p1) := by
    rw [expand]; exact div_pos (by nlinarith) (mul_pos a1 a2)
  linarith

theorem barotropic_cost_unbounded (M : ℝ) (hM : 1 ≤ M) :
    3 / (3 - (3 - 3 / M)) = M := by
  have hMne : M ≠ 0 := by linarith
  have h : 3 - (3 - 3 / M) = 3 / M := by ring
  rw [h, div_div_eq_mul_div]
  field_simp

/-- DENSITY–TIME DUALITY (the reason Theorem A holds): on an a⁻³ background ρ̄(x) = ρ₀/x³, a region of
    overdensity Δ = s³ − 1 at scale factor a carries exactly the density the universe had at a/s:
    ρ̄(a)·(1+Δ) = ρ̄(a/s). For a BAROTROPIC fluid the sound speed is a function of density alone, so the fluid
    inside a galaxy carries the sound speed of an EARLIER epoch — "grows with a" IS "falls with ρ". A fluid
    whose c_s² depends on an internal clock rather than on ρ breaks this by construction (the surviving door). -/
theorem density_time_duality (rho0 a s : ℝ) (ha : 0 < a) (hs : 0 < s) :
    rho0 / a ^ 3 * s ^ 3 = rho0 / (a / s) ^ 3 := by
  have hane : a ≠ 0 := ne_of_gt ha
  have hsne : s ≠ 0 := ne_of_gt hs
  field_simp

/-! ### L166: CONDITIONAL-COMPLETENESS CERTIFICATE — NECESSITY ONLY.
    What any theory built on the framework's equations (a₀ = κc√(Gρ_DE), ν-kernel, a⁻³ dust) MUST have in
    order to pass the galaxy, CMB, Lyα and PPN gates simultaneously. Each clause is the algebraic content of a
    computed pincer (L145–L151 dark fraction; L152–L158 barotropic ceiling; L134 PPN α₁). This is NOT a complete
    theory and NOT a sufficiency proof: sufficiency is the content of three uncomputed simulations (two-species
    Lyα hydro; baryon+MOND growth in the c_ad 300–537 km/s sliver; N-body mass-dependent kick) and cannot be
    Lean-certified because those gates are empirical. -/

/-- DARK-FRACTION PINCER forces a MASS-DEPENDENT dark fraction: if some galaxy host m_g needs f(m_g) ≤ f_gal_max,
    the population sourcing the third peak needs f(m_c) ≥ f_cmb_min, and f_gal_max < f_cmb_min (0.105 < 0.988),
    then f is strictly larger at m_c and cannot be constant. -/
theorem dark_fraction_forces_mass_dependence (f : ℝ → ℝ) (m_g m_c f_gal_max f_cmb_min : ℝ)
    (hg : f m_g ≤ f_gal_max) (hc : f_cmb_min ≤ f m_c) (hlt : f_gal_max < f_cmb_min) :
    f m_g < f m_c ∧ ¬ (∀ m₁ m₂, f m₁ = f m₂) := by
  have h : f m_g < f m_c := by linarith
  refine ⟨h, ?_⟩
  intro hconst
  have := hconst m_g m_c
  linarith

theorem dark_fraction_pincer_numeric : (0.105 : ℝ) < 0.988 := by norm_num

/-- Lyα: the required clustering exponent p_req ∈ [3.53, 4.09] lies strictly above the barotropic ceiling p < 3
    (barotropic_w_ratio needs 3 − p > 0), so a single barotropic fluid cannot pass Lyα; the surviving door is
    non-barotropic (two species / internal clock, cf. density_time_duality). -/
theorem lya_excludes_barotropic (p p_req : ℝ) (hbar : p < 3) (hreq : 3.53 ≤ p_req) : p < p_req := by
  linarith

theorem lya_window_above_ceiling : ¬ ∃ p : ℝ, p < 3 ∧ 3.53 ≤ p ∧ p ≤ 4.09 := by
  rintro ⟨p, h1, h2, _⟩; linarith

/-- FOOTINGS (L140–L144): the framework's a₀² = κ²c²G·(Ω_Λ ρ_crit) versus the ΛCDM-native g†² = κ²c²G ρ_crit:
    the squared ratio alt/canonical is exactly 1/Ω_Λ (= 1.2048² for Ω_Λ = 0.689). Certified on squares. -/
theorem footing_ratio_sq (κ c G ρ_crit Ω : ℝ) (hκ : κ ≠ 0) (hc : c ≠ 0) (hG : G ≠ 0) (hρ : ρ_crit ≠ 0)
    (hΩ : Ω ≠ 0) :
    (κ ^ 2 * c ^ 2 * (G * ρ_crit)) / (κ ^ 2 * c ^ 2 * (G * (Ω * ρ_crit))) = 1 / Ω := by
  field_simp

/-- FLAT vs RISING: with ρ_crit(H) = 3H²/(8πG) (π passed as a nonzero constant) the ΛCDM-native scale squared scales as (H/H₀)², whereas the
    framework's w = −1 law a₀² = κ²c²G ρ_DE is H-independent. This is the fork ΛCDM cannot mimic. -/
theorem lcdm_native_scale_rises (c G H H0 pi : ℝ) (hc : c ≠ 0) (hG : G ≠ 0) (hH0 : H0 ≠ 0)
    (hpi : pi ≠ 0) :
    (c ^ 2 * (G * (3 * H ^ 2 / (8 * pi * G)))) / (c ^ 2 * (G * (3 * H0 ^ 2 / (8 * pi * G))))
      = (H / H0) ^ 2 := by
  field_simp

/-- CONDITIONAL-COMPLETENESS CERTIFICATE (necessity). Any theory passing the galaxy gate (f ≤ 0.105 at some
    host), the CMB gate (f ≥ 0.988 for the third-peak population), the Lyα gate (p_eff ≥ 3.53) and the PPN α₁
    gate (α₁ = −8 c_pf = 0) must have: (i) a mass-dependent dark fraction, (ii) a non-barotropic effective
    fluid, (iii) a local (screened) α₁ source. Sufficiency is NOT proven here and is not Lean-provable. -/
theorem necessary_conditions_for_all_gates (f : ℝ → ℝ) (m_g m_c p_eff c_pf : ℝ)
    (gate_galaxy : f m_g ≤ 0.105) (gate_cmb : 0.988 ≤ f m_c)
    (gate_lya : 3.53 ≤ p_eff) (gate_ppn : -8 * c_pf = 0) :
    (¬ ∀ m₁ m₂, f m₁ = f m₂) ∧ (¬ p_eff < 3) ∧ c_pf = 0 := by
  refine ⟨(dark_fraction_forces_mass_dependence f m_g m_c 0.105 0.988 gate_galaxy gate_cmb
    (by norm_num)).2, ?_, (ppn_alpha1_vanishes_iff_local_source c_pf).1 gate_ppn⟩
  intro h
  linarith

/-! ### L168: the TWO-BODY DECAY LIFETIME PINCER (forest vs galaxies).
    Exact linear response (L168) shows that for any kick v_k ≳ 200 km/s every daughter born more than ~0.1 Gyr
    before z = 3 carries no power at k ≥ 5 h/Mpc, so the small-scale transfer function has a floor
    T² = (1 − f_d)² = exp(−t₃/τ)² = exp(−2t₃/τ), with f_d the decayed fraction at z = 3 and t₃ = t(z=3) = 2.14 Gyr.
    The forest tolerates at most a factor T_min there; the L167 galaxy gate needs τ ≤ τ_gal = 20 Gyr.
    Numbers: T_min = 0.90 (loose) ⇒ τ ≥ 41 Gyr; T_min = 0.994 (5.3 keV-calibrated) ⇒ τ ≥ 744 Gyr. Both exceed 20. -/

/-- (e^{-t/τ})² = e^{-2t/τ}: the plateau identity. -/
theorem two_body_plateau_identity (t τ : ℝ) : Real.exp (-t / τ) ^ 2 = Real.exp (-2 * t / τ) := by
  rw [sq, ← Real.exp_add]; ring_nf

/-- Forest floor ⇒ lifetime bound: T_min ≤ e^{-2t₃/τ} with τ > 0 forces 2t₃ ≤ τ·(−log T_min). -/
theorem two_body_forest_lifetime_bound (t3 τ Tmin : ℝ) (hτ : 0 < τ) (hT : 0 < Tmin)
    (hforest : Tmin ≤ Real.exp (-2 * t3 / τ)) : 2 * t3 ≤ τ * (-Real.log Tmin) := by
  have h2 : Real.log Tmin ≤ -2 * t3 / τ := by
    have := Real.log_le_log hT hforest
    rwa [Real.log_exp] at this
  have h3 : τ * Real.log Tmin ≤ τ * (-2 * t3 / τ) := mul_le_mul_of_nonneg_left h2 hτ.le
  have h4 : τ * (-2 * t3 / τ) = -2 * t3 := by field_simp
  have h5 : τ * (-Real.log Tmin) = -(τ * Real.log Tmin) := by ring
  linarith

/-- THE PINCER: forest floor (T_min < 1) plus galaxy gate (τ ≤ τ_gal) ⇒ τ_gal ≥ 2t₃/(−log T_min). -/
theorem two_body_tau_pincer (t3 τ τ_gal Tmin : ℝ) (hτ : 0 < τ) (hT0 : 0 < Tmin) (hT1 : Tmin < 1)
    (hforest : Tmin ≤ Real.exp (-2 * t3 / τ)) (hgal : τ ≤ τ_gal) :
    2 * t3 / (-Real.log Tmin) ≤ τ_gal := by
  have hlog : 0 < -Real.log Tmin := by have := Real.log_neg hT0 hT1; linarith
  have hb := two_body_forest_lifetime_bound t3 τ Tmin hτ hT0 hforest
  rw [div_le_iff₀ hlog]
  calc 2 * t3 ≤ τ * (-Real.log Tmin) := hb
    _ ≤ τ_gal * (-Real.log Tmin) := mul_le_mul_of_nonneg_right hgal hlog.le

/-- Numeric instance (loose tolerance): with t₃ = 2.14 Gyr and T_min = 0.9 the forest needs τ > 20 Gyr,
    i.e. more than the galaxy gate allows. Uses only 1 + x ≤ eˣ. -/
theorem two_body_pincer_numeric : (20 : ℝ) < 2 * 2.14 / (-Real.log 0.9) := by
  have h1 : (0.214 : ℝ) + 1 ≤ Real.exp 0.214 := Real.add_one_le_exp 0.214
  have hlog : -0.214 < Real.log 0.9 := by
    rw [Real.lt_log_iff_exp_lt (by norm_num)]
    rw [Real.exp_neg, inv_lt_comm₀ (Real.exp_pos _) (by norm_num)]
    linarith
  have hpos : 0 < -Real.log 0.9 := by
    have := Real.log_neg (by norm_num : (0:ℝ) < 0.9) (by norm_num); linarith
  rw [lt_div_iff₀ hpos]
  linarith

/-! ### L169: the SINGLE-METRIC KINETIC-MIXING ACTION — static/PPN algebra certified, cosmology certified to FAIL.
    See SINGLE_METRIC_ACTION.md. -/

/-- Double-filter kernel: 1/(k²(1+u)²) = 1/k² − ξ²/(1+u) − ξ²/(1+u)² with u = ξ²k² (inverse transform ⇒ T(x)). -/
theorem double_filter_kernel (k ξ : ℝ) (hk : k ≠ 0) :
    1 / (k ^ 2 * (1 + ξ ^ 2 * k ^ 2) ^ 2)
      = 1 / k ^ 2 - ξ ^ 2 / (1 + ξ ^ 2 * k ^ 2) - ξ ^ 2 / (1 + ξ ^ 2 * k ^ 2) ^ 2 := by
  have h : (1 + ξ ^ 2 * k ^ 2) ≠ 0 := by positivity
  field_simp
  ring

/-- UV suppression of the scalar channel: (1+u)⁻² ≤ u⁻² — the k⁴ coherent stiffening. -/
theorem double_filter_uv_suppression (u : ℝ) (hu : 0 < u) : 1 / (1 + u) ^ 2 ≤ 1 / u ^ 2 := by
  apply one_div_le_one_div_of_le (by positivity)
  nlinarith

/-- Smoothing sector (χ_i, λ_i): 6 configuration variables, phase dimension 12, 12 second-class constraints ⇒ 0 DOF. -/
theorem smoothing_sector_zero_dof : diracDOF 12 0 12 = 0 := fully_constrained_zero_dof 12

/-- Transmission bound: T(x) = 1 − e^{−x}(1 + x + x²/2) satisfies 0 ≤ T(x) ≤ x³ on [0,1]
    (mathlib Taylor bound |exp y − Σ_{i<4} yⁱ/i!| ≤ |y|⁴·5/96 for |y| ≤ 1, at y = −x). -/
theorem double_filter_transmission_cubic (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    0 ≤ 1 - Real.exp (-x) * (1 + x + x ^ 2 / 2) ∧ 1 - Real.exp (-x) * (1 + x + x ^ 2 / 2) ≤ x ^ 3 := by
  have hb := Real.exp_bound (x := -x) (by rw [abs_neg, abs_of_nonneg h0]; exact h1) (n := 4) (by norm_num)
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial, pow_zero, pow_one] at hb
  norm_num at hb
  have hneg : (-x) ^ 3 = -x ^ 3 := by ring
  rw [hneg, abs_of_nonneg h0] at hb
  have hlo := (abs_le.mp hb).1
  have hhi := (abs_le.mp hb).2
  have hx2 : x ^ 2 ≤ x := by nlinarith
  have hx3 : x ^ 3 ≤ x ^ 2 := by nlinarith
  have hx4 : x ^ 4 ≤ x ^ 3 := by nlinarith
  have hx5 : x ^ 5 ≤ x ^ 4 := by nlinarith
  have hx6 : x ^ 6 ≤ x ^ 5 := by nlinarith
  constructor <;> nlinarith [hlo, hhi, hx2, hx3, hx4, hx5, hx6, sq_nonneg x, Real.exp_pos (-x)]

/-- Cassini: |γ−1| = 2 f_eff with f_eff ≤ T(r/ξ) ≤ (r/ξ)³; at r/ξ ≤ 1/100 this is ≤ 2×10⁻⁶ < 2.3×10⁻⁵. -/
theorem screened_gamma_cassini (x feff : ℝ) (h0 : 0 ≤ x) (hx : x ≤ 1 / 100) (hf0 : 0 ≤ feff) (hf : feff ≤ x ^ 3) :
    2 * feff < 2.3e-5 := by
  have hx2 : x ^ 2 ≤ (1 / 100) ^ 2 := by nlinarith
  have hx3 : x ^ 3 ≤ (1 / 100) ^ 3 := by nlinarith
  norm_num at hx3
  linarith

/-- THE CERTIFIED FAILURE: a theory whose dark fraction is host-independent cannot pass galaxies (≤ 0.105) and the
    CMB (≥ 0.988) together. The single-metric action has only such components (cuscuton dust, stiff φ background). -/
theorem single_metric_uniform_dark_fraction_fails (f : ℝ → ℝ) (m_g m_c : ℝ)
    (huniform : ∀ m₁ m₂, f m₁ = f m₂) (hgal : f m_g ≤ 0.105) (hcmb : 0.988 ≤ f m_c) : False :=
  (dark_fraction_forces_mass_dependence f m_g m_c 0.105 0.988 hgal hcmb (by norm_num)).2 huniform

/-! ### L170: BOOSTED-FRAME PPN of the single-metric action — the clock-drag channel.
    For a source moving at w relative to the cuscuton clock, the smoothing constraint's λ^μA_μ term drives the clock tilt T
    through μ_c²k²T = (w·k)(k·λ), and the resulting O(w²) potential is Φ⁽²⁾/Φ⁽⁰⁾ = (c²/μ_∞)²(w·k)²/(4πGμ_c²(1+u)⁴) (π passed as a positive constant).
    Certified: the drag amplitude, and that the ratio exceeds any bound once the clock is soft enough. Numbers (L170):
    3×10⁻² Φ_N at Saturn, > Φ_N beyond 30 AU, PPN-safe μ_c² ≥ 10¹⁵ × the dark-energy value. -/

/-- Clock-drag amplitude: μ²k²T = (w·k)(k·λ) with μ, k ≠ 0 ⇒ T = (w·k)(k·λ)/(μ²k²). -/
theorem clock_drag_amplitude (mu2 k2 wk klam T : ℝ) (hmu : mu2 ≠ 0) (hk : k2 ≠ 0)
    (h : mu2 * k2 * T = wk * klam) : T = wk * klam / (mu2 * k2) := by
  field_simp
  linarith

/-- The drag ratio C·wk²/(4πG μ² (1+u)⁴) exceeds any bound B once μ² < C·wk²/(4πG B (1+u)⁴): no finite PPN tolerance survives
    a soft clock. -/
theorem drag_ratio_exceeds_bound (C wk G pi mu2 u B : ℝ) (hC : 0 < C) (hwk : 0 < wk) (hG : 0 < G) (hpi : 0 < pi)
    (hmu : 0 < mu2) (hu : 0 ≤ u) (hB : 0 < B)
    (hsoft : mu2 < C * wk ^ 2 / (4 * pi * G * B * (1 + u) ^ 4)) :
    B < C * wk ^ 2 / (4 * pi * G * mu2 * (1 + u) ^ 4) := by
  have hpos : 0 < 4 * pi * G * B * (1 + u) ^ 4 := by positivity
  have h1 : mu2 * (4 * pi * G * B * (1 + u) ^ 4) < C * wk ^ 2 := by
    rwa [lt_div_iff₀ hpos] at hsoft
  have hden : 0 < 4 * pi * G * mu2 * (1 + u) ^ 4 := by positivity
  rw [lt_div_iff₀ hden]
  nlinarith

/-! ### L171: the STIFF-CLOCK version (khronometric K² clock, c₁₃ = c₁₄ = 0). -/

/-- Stiff clock: the drag ratio 2C²(w·k)²/(c₂k²(1+u)⁴) is bounded by 2C²w²/c₂ (Cauchy–Schwarz (w·k)² ≤ w²k², (1+u)⁻⁴ ≤ 1). -/
theorem stiff_clock_drag_bounded (C w k wk c2 u : ℝ) (hc2 : 0 < c2) (hk : 0 < k) (hu : 0 ≤ u)
    (hcs : wk ^ 2 ≤ w ^ 2 * k ^ 2) :
    2 * C ^ 2 * wk ^ 2 / (c2 * k ^ 2 * (1 + u) ^ 4) ≤ 2 * C ^ 2 * w ^ 2 / c2 := by
  have h1 : 1 ≤ (1 + u) ^ 4 := one_le_pow₀ (by linarith)
  have hden : 0 < c2 * k ^ 2 * (1 + u) ^ 4 := by positivity
  rw [div_le_div_iff₀ hden hc2]
  have hC : 0 ≤ 2 * C ^ 2 := by positivity
  have h2 : 2 * C ^ 2 * wk ^ 2 ≤ 2 * C ^ 2 * (w ^ 2 * k ^ 2) := mul_le_mul_of_nonneg_left hcs hC
  have h3 : 2 * C ^ 2 * (w ^ 2 * k ^ 2) * c2 ≤ 2 * C ^ 2 * w ^ 2 * (c2 * k ^ 2 * (1 + u) ^ 4) := by
    have : 0 ≤ 2 * C ^ 2 * w ^ 2 * c2 * k ^ 2 := by positivity
    nlinarith
  nlinarith

/-- α₁ from the gauge-invariant O(w) combination: A + B = −4 (the scalar does not enter g₀ᵢ) and
    A + B = −2γ − 2 − α₁ (PPN dictionary) ⇒ α₁ = 2(1 − γ). -/
theorem alpha1_from_invariant (A B γ α₁ : ℝ) (hGR : A + B = -4) (hdict : A + B = -2 * γ - 2 - α₁) :
    α₁ = 2 * (1 - γ) := by linarith

/-- BBN: G_cosmo/G_N = 1/(1 + 3c₂/2) ≥ 0.94 with c₂ ≥ 0 ⇒ c₂ ≤ 0.0426. -/
theorem bbn_c2_bound (c2 : ℝ) (h0 : 0 ≤ c2) (h : (0.94 : ℝ) ≤ 1 / (1 + 3 * c2 / 2)) : c2 ≤ 0.0426 := by
  have hp : 0 < 1 + 3 * c2 / 2 := by linarith
  rw [le_div_iff₀ hp] at h
  linarith

/-- The K² clock has no time derivatives at quadratic order: phase dimension 2, fully constrained ⇒ 0 DOF. -/
theorem stiff_clock_zero_dof : diracDOF 2 0 2 = 0 := fully_constrained_zero_dof 2
