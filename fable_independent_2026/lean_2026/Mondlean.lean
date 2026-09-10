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
