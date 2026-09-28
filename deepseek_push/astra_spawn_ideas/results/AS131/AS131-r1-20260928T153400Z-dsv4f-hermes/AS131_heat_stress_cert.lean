import Mathlib
/-!
# AS131 — heat-field metric stress: algebraic core certificate

Scope. In the heat-constraint block of action (4) (FINAL_ACTION.md, CA4-GNC;
inherited by CA5-GNC-R),

    S_heat = (M_P² c_N / 2) ∫dτ ∫_Σ N√h ∫_0^b dr L (∂_r W − Δ_h W),   b = ξ²/2,

the spatial integration by parts on a closed leaf with lapse N = e^σ is

    ∫ N√h L Δ_h W  =  −∫ N√h [ <DL,DW> + L <D ln N, DW> ].

On a flat 1D leaf (periodic coordinate, period 2π, √h = 1) with ∂_r W = μ W
this is the identity certified below in `heat_ibp_correct`:

    ∫₀^{2π} e^σ [ μLW + L′W′ + Lσ′W′ ]  =  ∫₀^{2π} e^σ L ( μW − W″ )

for ANY C¹-periodic σ,L,W with periodic W′ (lapse, multiplier and heat field).
The proof is one line of analysis: the difference of the two integrands is the
derivative of e^σ·L·W′, whose integral over a period vanishes (FTC +
periodicity) — this is exactly the IBP content, including the lapse-gradient
term Lσ′W′ that the NEGATIVE CONTROL discards.

`heat_onshell_measure`: imposing the heat equation ∂_r W = Δ_h W (1D:
μW = W″) makes the leaf integral vanish: ∫ N√h B₀ = 0 on the closed leaf.

`wrong_residual_eq`: the wrong (lapse-derivative-discarded) side fails exactly
by the lapse-gradient moment ∫e^σ L σ′ W′, which is nonzero for nonconstant
lapse (numerically verified with the Fourier witness, run_stdout.txt).

The pure mode-bracket theorems (`ibp_bracket_zero`, `wrong_ibp_bracket`,
witness example) certify the mode algebra for W = e^{ikx}, L = e^{iqx}: the
correct bracket equals the direct bracket, and the wrong bracket misses
−k(q+k)·Φ ≠ 0 at (k,q) = (1,2).

Lean certifies the displayed algebraic statements, not the whole gravity model.
-/

open scoped intervalIntegral Real
open Set intervalIntegral

noncomputable section
namespace AS131

/-- Periodic integration by parts zero lemma: ∫₀^{2π} f′ = 0 for C¹ periodic f. -/
theorem periodic_integral_deriv_zero (f : ℝ → ℝ) (d : ℝ → ℝ)
    (hf : ∀ x, HasDerivAt f (d x) x) (hd : Continuous d)
    (hper : f (2 * Real.pi) = f 0) :
    ∫ x in (0 : ℝ)..2 * Real.pi, d x = 0 := by
  have hftc : ∫ x in (0 : ℝ)..2 * Real.pi, d x = f (2 * Real.pi) - f 0 := by
    refine intervalIntegral.integral_deriv_eq_sub' f ?hderiv ?hdiff ?hcont
    · funext x
      exact (hf x).deriv
    · intro x hx
      exact (hf x).differentiableAt
    · exact hd.continuousOn
  rw [hftc, hper]
  ring

/-- The IBP identity for the heat block on a flat 1D periodic leaf with lapse
    N = e^σ, multiplier L and heat field W, ∂_r W = μ W:
    the CORRECT (lapse-gradient-retained) integral equals the DIRECT one. -/
theorem heat_ibp_correct {σ L W : ℝ → ℝ} {dσ dL dW dW' : ℝ → ℝ} (μ : ℝ)
    (hσ : ∀ x, HasDerivAt σ (dσ x) x) (hL : ∀ x, HasDerivAt L (dL x) x)
    (hW : ∀ x, HasDerivAt W (dW x) x) (hW' : ∀ x, HasDerivAt dW (dW' x) x)
    (hσc : Continuous dσ) (hLc : Continuous dL) (hWc : Continuous dW) (hW'c : Continuous dW')
    (hσp : σ (2 * Real.pi) = σ 0) (hLp : L (2 * Real.pi) = L 0)
    (hW'p : dW (2 * Real.pi) = dW 0) :
    ∫ x in (0 : ℝ)..2 * Real.pi,
        Real.exp (σ x) * (μ * L x * W x + dL x * dW x + L x * dσ x * dW x)
      = ∫ x in (0 : ℝ)..2 * Real.pi, Real.exp (σ x) * (L x * (μ * W x - dW' x)) := by
  -- the derivative form: (e^σ L dW)' = e^σ (σ' L dW + dL dW + L dW')
  let g : ℝ → ℝ := fun x =>
      Real.exp (σ x) * dσ x * (L x * dW x) + Real.exp (σ x) * (dL x * dW x + L x * dW' x)
  -- the product whose derivative is the integrand difference
  let f : ℝ → ℝ := fun x => Real.exp (σ x) * (L x * dW x)
  have hf : ∀ x, HasDerivAt f (g x) x := by
    intro x
    unfold f g
    exact (hσ x).exp.mul ((hL x).mul (hW' x))
  have hfper : f (2 * Real.pi) = f 0 := by
    unfold f
    rw [← hσp, ← hLp, ← hW'p]
  have hfcont : Continuous g := by
    have hσct : Continuous σ := continuous_iff_continuousAt.mpr
      (fun x => (hσ x).differentiableAt.continuousAt)
    have hLct : Continuous L := continuous_iff_continuousAt.mpr
      (fun x => (hL x).differentiableAt.continuousAt)
    have hdWct : Continuous dW := continuous_iff_continuousAt.mpr
      (fun x => (hW' x).differentiableAt.continuousAt)
    unfold g
    fun_prop
  have hzero : ∫ x in (0 : ℝ)..2 * Real.pi, g x = 0 :=
    periodic_integral_deriv_zero f g hf hfcont hfper
  -- direct vs correct integrand difference equals g pointwise
  have hEq : Set.EqOn (fun x =>
        Real.exp (σ x) * (μ * L x * W x + dL x * dW x + L x * dσ x * dW x)
        - Real.exp (σ x) * (L x * (μ * W x - dW' x)))
      g (Set.uIcc 0 (2 * Real.pi)) := by
    intro x hx
    unfold g
    ring
  have hdiff0 : ∫ x in (0 : ℝ)..2 * Real.pi,
        (Real.exp (σ x) * (μ * L x * W x + dL x * dW x + L x * dσ x * dW x)
          - Real.exp (σ x) * (L x * (μ * W x - dW' x))) = 0 := by
    rw [intervalIntegral.integral_congr hEq, hzero]
  -- linearity: (∫A) − (∫B) = ∫(A − B)
  let A : ℝ → ℝ := fun x =>
      Real.exp (σ x) * (μ * L x * W x + dL x * dW x + L x * dσ x * dW x)
  let B : ℝ → ℝ := fun x => Real.exp (σ x) * (L x * (μ * W x - dW' x))
  have hA : Continuous A := by
    have hσct : Continuous σ := continuous_iff_continuousAt.mpr
      (fun x => (hσ x).differentiableAt.continuousAt)
    have hLct : Continuous L := continuous_iff_continuousAt.mpr
      (fun x => (hL x).differentiableAt.continuousAt)
    have hWct : Continuous W := continuous_iff_continuousAt.mpr
      (fun x => (hW x).differentiableAt.continuousAt)
    have hdWct : Continuous dW := continuous_iff_continuousAt.mpr
      (fun x => (hW' x).differentiableAt.continuousAt)
    unfold A
    fun_prop
  have hB : Continuous B := by
    have hσct : Continuous σ := continuous_iff_continuousAt.mpr
      (fun x => (hσ x).differentiableAt.continuousAt)
    have hLct : Continuous L := continuous_iff_continuousAt.mpr
      (fun x => (hL x).differentiableAt.continuousAt)
    have hWct : Continuous W := continuous_iff_continuousAt.mpr
      (fun x => (hW x).differentiableAt.continuousAt)
    unfold B
    fun_prop
  have hsub : (∫ x in (0 : ℝ)..2 * Real.pi, A x) - (∫ x in (0 : ℝ)..2 * Real.pi, B x)
      = ∫ x in (0 : ℝ)..2 * Real.pi, (A x - B x) := by
    exact (intervalIntegral.integral_sub (f := A) (g := B)
      (Continuous.intervalIntegrable (by exact hA) _ _)
      (Continuous.intervalIntegrable (by exact hB) _ _)).symm
  -- assemble: (∫A) − (∫B) = ∫(A−B) = 0
  have hlin : (∫ x in (0 : ℝ)..2 * Real.pi, A x) - (∫ x in (0 : ℝ)..2 * Real.pi, B x) = 0 := by
    rw [hsub, hdiff0]
  simpa [A, B, sub_eq_zero] using hlin

/-- On the heat equation (1D: μ W = W″) the leaf integral of the constraint
    density vanishes: ∫ N√h B₀ = 0 on the closed leaf. -/
theorem heat_onshell_measure {σ L W : ℝ → ℝ} {dσ dL dW dW' : ℝ → ℝ} (μ : ℝ)
    (hσ : ∀ x, HasDerivAt σ (dσ x) x) (hL : ∀ x, HasDerivAt L (dL x) x)
    (hW : ∀ x, HasDerivAt W (dW x) x) (hW' : ∀ x, HasDerivAt dW (dW' x) x)
    (hσc : Continuous dσ) (hLc : Continuous dL) (hWc : Continuous dW) (hW'c : Continuous dW')
    (hσp : σ (2 * Real.pi) = σ 0) (hLp : L (2 * Real.pi) = L 0)
    (hW'p : dW (2 * Real.pi) = dW 0) (honshell : ∀ x, μ * W x = dW' x) :
    ∫ x in (0 : ℝ)..2 * Real.pi,
        Real.exp (σ x) * (μ * L x * W x + dL x * dW x + L x * dσ x * dW x) = 0 := by
  rw [heat_ibp_correct μ hσ hL hW hW' hσc hLc hWc hW'c hσp hLp hW'p]
  calc
    ∫ x in (0 : ℝ)..2 * Real.pi, Real.exp (σ x) * (L x * (μ * W x - dW' x))
        = ∫ x in (0 : ℝ)..2 * Real.pi, (0 : ℝ) := by
          apply intervalIntegral.integral_congr
          intro x hx
          change Real.exp (σ x) * (L x * (μ * W x - dW' x)) = 0
          rw [honshell x]
          ring
    _ = 0 := by simp

/-- Wrong (lapse-derivative-discarded) side: its defect against the direct
    side is exactly the lapse-gradient moment ∫e^σ L σ′ W′. -/
theorem wrong_residual_eq {σ L W : ℝ → ℝ} {dσ dL dW dW' : ℝ → ℝ} (μ : ℝ)
    (hσ : ∀ x, HasDerivAt σ (dσ x) x) (hL : ∀ x, HasDerivAt L (dL x) x)
    (hW : ∀ x, HasDerivAt W (dW x) x) (hW' : ∀ x, HasDerivAt dW (dW' x) x)
    (hσc : Continuous dσ) (hLc : Continuous dL) (hWc : Continuous dW) (hW'c : Continuous dW')
    (hσp : σ (2 * Real.pi) = σ 0) (hLp : L (2 * Real.pi) = L 0)
    (hW'p : dW (2 * Real.pi) = dW 0) :
    (∫ x in (0 : ℝ)..2 * Real.pi, Real.exp (σ x) * (L x * (μ * W x - dW' x)))
      - (∫ x in (0 : ℝ)..2 * Real.pi,
            Real.exp (σ x) * (μ * L x * W x + dL x * dW x))
      = ∫ x in (0 : ℝ)..2 * Real.pi, Real.exp (σ x) * (L x * dσ x * dW x) := by
  have h := heat_ibp_correct μ hσ hL hW hW' hσc hLc hWc hW'c hσp hLp hW'p
  rw [← h]
  let Wr : ℝ → ℝ := fun x =>
      Real.exp (σ x) * (μ * L x * W x + dL x * dW x)
  let Lap : ℝ → ℝ := fun x => Real.exp (σ x) * (L x * dσ x * dW x)
  have hWr : Continuous Wr := by
    have hσct : Continuous σ := continuous_iff_continuousAt.mpr
      (fun x => (hσ x).differentiableAt.continuousAt)
    have hLct : Continuous L := continuous_iff_continuousAt.mpr
      (fun x => (hL x).differentiableAt.continuousAt)
    have hWct : Continuous W := continuous_iff_continuousAt.mpr
      (fun x => (hW x).differentiableAt.continuousAt)
    have hdWct : Continuous dW := continuous_iff_continuousAt.mpr
      (fun x => (hW' x).differentiableAt.continuousAt)
    unfold Wr
    fun_prop
  have hLap : Continuous Lap := by
    have hσct : Continuous σ := continuous_iff_continuousAt.mpr
      (fun x => (hσ x).differentiableAt.continuousAt)
    have hLct : Continuous L := continuous_iff_continuousAt.mpr
      (fun x => (hL x).differentiableAt.continuousAt)
    have hdWct : Continuous dW := continuous_iff_continuousAt.mpr
      (fun x => (hW' x).differentiableAt.continuousAt)
    unfold Lap
    fun_prop
  have hsplit : (∫ x in (0 : ℝ)..2 * Real.pi,
        Real.exp (σ x) * (μ * L x * W x + dL x * dW x + L x * dσ x * dW x))
      = (∫ x in (0 : ℝ)..2 * Real.pi, Wr x)
        + (∫ x in (0 : ℝ)..2 * Real.pi, Lap x) := by
    rw [← intervalIntegral.integral_add (f := Wr) (g := Lap)
      (Continuous.intervalIntegrable (by exact hWr) _ _)
      (Continuous.intervalIntegrable (by exact hLap) _ _)]
    apply intervalIntegral.integral_congr
    intro x hx
    unfold Wr Lap
    ring
  rw [hsplit]
  ring

/-- Mode algebra: the CORRECT IBP bracket equals the direct bracket identically
    (W = e^{ikx}, L = e^{iqx}, ∂_r W = μW, Δ = −k² on the mode). -/
theorem ibp_bracket_zero (k q : ℂ) : -(q * k) + k * (q + k) - k * k = 0 := by
  ring

/-- Mode algebra: the WRONG (lapse-derivative-discarded) bracket differs from
    the direct one by exactly −k(q+k): the negative-control residual. -/
theorem wrong_ibp_bracket (k q : ℂ) : -(q * k) - k * k = -(k * (q + k)) := by
  ring

/-- Negative-control instance: for the witness (k,q) = (1,2) the residual
    coefficient −k(q+k) = −3 ≠ 0, so the discarded-lapse IBP fails there
    whenever the Fourier moment Φ(q+k) is nonzero (verified numerically,
    run_stdout.txt: residual 1.25e-01 ≫ tolerance). -/
example : -(1 : ℂ) * (2 : ℂ) - (1 : ℂ) * (1 : ℂ) ≠ 0 := by
  norm_num

#print axioms periodic_integral_deriv_zero
#print axioms heat_ibp_correct
#print axioms heat_onshell_measure
#print axioms wrong_residual_eq
#print axioms ibp_bracket_zero
#print axioms wrong_ibp_bracket

end AS131
