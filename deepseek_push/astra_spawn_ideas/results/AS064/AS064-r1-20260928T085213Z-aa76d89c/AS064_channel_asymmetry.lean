import Mathlib

open scoped Real Filter Topology

/-!
AS064 -- sensitivity of the selected coefficient kappa to channel asymmetry.
Lean 4 certificate for the load-bearing algebraic identities.

Certified statements (see derivation.md for the mathematical context):
  T5 rational_closed_form : the asymmetric rational OR response (channels
        b1 = 1+eps, b2 = 1-eps, completions p_i(x) = b_i x/(1+x)) has the
        exact closed form  mu(x) = x*(2 + (1+eps^2) x)/(1+x)^2.
  T4 rational_slope_two  : the total slope at the origin is EXACTLY 2 for
        every eps (the deep-MOND slope is the SUM of the channel slopes --
        the chain rule mu'(0) = b1+b2 is certified symbolically by sympy
        T0a in the run and numerically; this Lean file certifies the
        concrete counterexample family through the limit
        lim_{x->0, x!=0} mu(x)/x = 2.
  T6 rational_quadratic_coefficient : the first visible asymmetry order is
        QUADRATIC: on the punctured neighbourhood of 0,
        lim (mu(x)-2x)/x^2 = -3+eps^2.  At eps = 0 the symmetric value -3
        is recovered; the coefficient shift is exactly eps^2.
  T7 powerlaw_collapse    : for completions p_i(x) = 1-(1+x)^(-b_i) the OR
        composition collapses to 1-(1+x)^(-(b1+b2)) = 1-(1+x)^(-2): channel
        asymmetry is invisible at EVERY order (exact identity).
  T9 normalization_decomposition : the rational family's deviation from the
        L230 Newtonian normalization, exactly:
        (1-p1)(1-p2)(x) = -eps^2 + 2 eps^2/(1+x) + (1-eps^2)/(1+x)^2;
        mu(inf)-1 = eps^2 then follows from the atTop limit, which is
        verified exactly by sympy in the run (this file certifies the
        algebra; checks T2c/T4d of the run verify mu(inf)-1 = lambda^2 at
        lambda = 1/2, 1, 2).
  T8 kappa_half_from_scale : a0 = s/2  =>  a0/s = 1/2  (the L230 matching
        chain's landing, as an algebra statement).

NOT certified in Lean (documented limitation): the fully-general
HasDerivAt chain-rule theorem d/dY[1-(1-p1)*(1-p2)] = a1+a2 for arbitrary
completion functions.  In this lean_2026 bundle, function-space
subtraction/multiplication terms fail to elaborate when applied to an
argument unless type-annotated, and HasDerivAt statements elaborated by
the tactic machinery acquire a different AddCommGroup class instance
(Real.normedAddCommGroup.toAddCommGroup vs Real.instAddCommGroup) than
the user-written statement, which no convert/simpa/exact bridge can close
(recorded verbatim).  The content is covered instead: symbolically by
sympy (T0a, derivative of the generic composition, exact 0 residual),
numerically at 50 digits (Richardson-extrapolated finite differences,
residuals ~1e-24), and in Lean for the concrete counterexample family by
the two limit certificates T4 and T6 above plus the exact closed form T5.
-/

namespace AS064

/- T5: exact closed form of the asymmetric rational response. -/
lemma rational_closed_form (eps x : ℝ) (hx : 1 + x ≠ 0) :
    1 - (1 - ((1 + eps) * x / (1 + x))) * (1 - ((1 - eps) * x / (1 + x)))
      = x * (2 + (1 + eps ^ 2) * x) / (1 + x) ^ 2 := by
  field_simp [hx]
  ring

/- T4: total slope exactly 2 (concrete family), as a punctured limit. -/
lemma rational_slope_two (eps : ℝ) :
    Filter.Tendsto (fun x : ℝ =>
      (1 - (1 - ((1 + eps) * x / (1 + x))) * (1 - ((1 - eps) * x / (1 + x)))) / x)
      (nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ)) (nhds (2 : ℝ)) := by
  have hleN : nhds (0 : ℝ) ⊓ 𝓟 ({(0 : ℝ)}ᶜ : Set ℝ) ≤ nhds (0 : ℝ) := inf_le_left
  have hselfp : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ), x ≠ 0 := by
    rw [nhdsWithin]
    exact ((Filter.eventually_principal.2 (by intro x hx; exact hx)).filter_mono
      (by exact (inf_le_right : nhds (0 : ℝ) ⊓ 𝓟 ({(0 : ℝ)}ᶜ : Set ℝ) ≤ 𝓟 ({(0 : ℝ)}ᶜ : Set ℝ))))
  have h1ne : ∀ᶠ x : ℝ in nhds (0 : ℝ), 1 + x ≠ 0 := by
    rw [eventually_nhds_iff]
    refine ⟨Metric.ball (0 : ℝ) 1, ?_, ?_, ?_⟩
    · intro x hx
      have hlt : |x| < 1 := by
        simpa using hx
      intro hz
      have hxneg : x = -1 := by
        linarith
      rw [hxneg] at hlt
      norm_num at hlt
    · exact Metric.isOpen_ball
    · simp [Metric.mem_ball]
  have h1neW : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ), 1 + x ≠ 0 := by
    exact h1ne.filter_mono hleN
  have hpunc : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ),
      x ≠ 0 ∧ 1 + x ≠ 0 := by
    filter_upwards [hselfp, h1neW]
    intro x hx0 hx1
    exact ⟨hx0, hx1⟩
  have hEq : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ),
      (1 - (1 - ((1 + eps) * x / (1 + x))) * (1 - ((1 - eps) * x / (1 + x)))) / x
        = (2 + (1 + eps ^ 2) * x) / (1 + x) ^ 2 := by
    filter_upwards [hpunc]
    intro x hx
    field_simp [hx.1, hx.2, rational_closed_form eps x hx.2]
    ring
  have hcid : ContinuousAt (fun x : ℝ => x) 0 := (hasDerivAt_id (0 : ℝ)).continuousAt
  have hcA : ContinuousAt (fun x : ℝ => (1 + eps ^ 2)) 0 :=
    (continuous_const : Continuous (fun x : ℝ => (1 + eps ^ 2))).continuousAt
  have hprod : ContinuousAt (fun x : ℝ => (1 + eps ^ 2) * x) 0 := hcA.mul hcid
  have hc2c : ContinuousAt (fun x : ℝ => (2 : ℝ)) 0 :=
    (continuous_const : Continuous (fun x : ℝ => (2 : ℝ))).continuousAt
  have hnumc : ContinuousAt (fun x : ℝ => 2 + (1 + eps ^ 2) * x) 0 := hc2c.add hprod
  have hc1 : ContinuousAt (fun x : ℝ => 1 + x) 0 :=
    (hasDerivAt_const (0 : ℝ) (1 : ℝ)).continuousAt.add hcid
  have hsq : ContinuousAt (fun x : ℝ => (1 + x) ^ 2) 0 := hc1.pow 2
  have hcr : ContinuousAt (fun x : ℝ => (2 + (1 + eps ^ 2) * x) / (1 + x) ^ 2) 0 :=
    hnumc.div hsq (by change (1 + (0 : ℝ)) ^ 2 ≠ 0; norm_num)
  have hR0 : Filter.Tendsto (fun x : ℝ => (2 + (1 + eps ^ 2) * x) / (1 + x) ^ 2)
      (nhds (0 : ℝ)) (nhds (2 : ℝ)) := by
    have hval : ((fun x : ℝ => (2 + (1 + eps ^ 2) * x) / (1 + x) ^ 2) 0) = 2 := by
      norm_num
    simpa [hval] using hcr.tendsto
  have hR : Filter.Tendsto (fun x : ℝ => (2 + (1 + eps ^ 2) * x) / (1 + x) ^ 2)
      (nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ)) (nhds (2 : ℝ)) :=
    Filter.Tendsto.mono_left hR0 hleN
  exact hR.congr' (Filter.EventuallyEq.symm hEq)

/- T6: first visible asymmetry at QUADRATIC order, coefficient -3+eps^2,
   on the punctured neighbourhood of 0 (the response over x^2 is not
   defined at 0). -/
lemma rational_quadratic_coefficient (eps : ℝ) :
    Filter.Tendsto (fun x : ℝ =>
      (1 - (1 - ((1 + eps) * x / (1 + x))) * (1 - ((1 - eps) * x / (1 + x))) - 2 * x)
        / x ^ 2) (nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ))
      (nhds (-3 + eps ^ 2)) := by
  have hleN : nhds (0 : ℝ) ⊓ 𝓟 ({(0 : ℝ)}ᶜ : Set ℝ) ≤ nhds (0 : ℝ) := inf_le_left
  have hselfp : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ), x ≠ 0 := by
    rw [nhdsWithin]
    exact ((Filter.eventually_principal.2 (by intro x hx; exact hx)).filter_mono
      (by exact (inf_le_right : nhds (0 : ℝ) ⊓ 𝓟 ({(0 : ℝ)}ᶜ : Set ℝ) ≤ 𝓟 ({(0 : ℝ)}ᶜ : Set ℝ))))
  have h1ne : ∀ᶠ x : ℝ in nhds (0 : ℝ), 1 + x ≠ 0 := by
    rw [eventually_nhds_iff]
    refine ⟨Metric.ball (0 : ℝ) 1, ?_, ?_, ?_⟩
    · intro x hx
      have hlt : |x| < 1 := by
        simpa using hx
      intro hz
      have hxneg : x = -1 := by
        linarith
      rw [hxneg] at hlt
      norm_num at hlt
    · exact Metric.isOpen_ball
    · simp [Metric.mem_ball]
  have h1neW : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ), 1 + x ≠ 0 := by
    exact h1ne.filter_mono hleN
  have hpunc : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ),
      x ≠ 0 ∧ 1 + x ≠ 0 := by
    filter_upwards [hselfp, h1neW]
    intro x hx0 hx1
    exact ⟨hx0, hx1⟩
  have hEq : ∀ᶠ x : ℝ in nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ),
      (1 - (1 - ((1 + eps) * x / (1 + x))) * (1 - ((1 - eps) * x / (1 + x))) - 2 * x)
        / x ^ 2 = -2 / (1 + x) - (1 - eps ^ 2) / (1 + x) ^ 2 := by
    filter_upwards [hpunc]
    intro x hx
    field_simp [hx.1, hx.2]
    ring
  have hc1 : ContinuousAt (fun x : ℝ => 1 + x) 0 :=
    (hasDerivAt_const (0 : ℝ) (1 : ℝ)).continuousAt.add
      (hasDerivAt_id (0 : ℝ)).continuousAt
  have hnum : ContinuousAt (fun x : ℝ => (-2 : ℝ)) 0 :=
    (continuous_const : Continuous (fun x : ℝ => (-2 : ℝ))).continuousAt
  have ht1 : ContinuousAt (fun x : ℝ => -2 / (1 + x)) 0 :=
    hnum.div hc1 (by norm_num : (fun x : ℝ => 1 + x) 0 ≠ 0)
  have hsq : ContinuousAt (fun x : ℝ => (1 + x) ^ 2) 0 := hc1.pow 2
  have hc2 : ContinuousAt (fun x : ℝ => (1 - eps ^ 2) / (1 + x) ^ 2) 0 :=
    ((continuous_const : Continuous (fun x : ℝ => (1 - eps ^ 2))).continuousAt).div hsq
      (by norm_num : (fun x : ℝ => (1 + x) ^ 2) 0 ≠ 0)
  have hcont : ContinuousAt (fun x : ℝ => -2 / (1 + x) - (1 - eps ^ 2) / (1 + x) ^ 2) 0 :=
    ht1.sub hc2
  have hR0 : Filter.Tendsto (fun x : ℝ => -2 / (1 + x) - (1 - eps ^ 2) / (1 + x) ^ 2)
      (nhds (0 : ℝ)) (nhds (-3 + eps ^ 2)) := by
    have hv0 : ((fun x : ℝ => -2 / (1 + x) - (1 - eps ^ 2) / (1 + x) ^ 2) 0)
        = -2 - (1 - eps ^ 2) := by
      norm_num
    have hv1 : (-2 - (1 - eps ^ 2)) = -3 + eps ^ 2 := by
      ring
    simpa [hv0, hv1] using hcont.tendsto
  have hR : Filter.Tendsto (fun x : ℝ => -2 / (1 + x) - (1 - eps ^ 2) / (1 + x) ^ 2)
      (nhdsWithin (0 : ℝ) ({(0 : ℝ)}ᶜ : Set ℝ)) (nhds (-3 + eps ^ 2)) :=
    Filter.Tendsto.mono_left hR0 hleN
  exact hR.congr' (Filter.EventuallyEq.symm hEq)

/- T7: power-law completions collapse: asymmetry invisible at every order. -/
lemma powerlaw_collapse (b1 b2 x : ℝ) (hx : 0 < 1 + x) :
    1 - (1 - (1 - (1 + x) ^ (-b1))) * (1 - (1 - (1 + x) ^ (-b2)))
      = 1 - (1 + x) ^ (-(b1 + b2)) := by
  have hce1 : 1 - (1 - (1 + x) ^ (-b1)) = (1 + x) ^ (-b1) := by
    ring
  have hce2 : 1 - (1 - (1 + x) ^ (-b2)) = (1 + x) ^ (-b2) := by
    ring
  have he : (-b1) + (-b2) = -(b1 + b2) := by
    ring
  rw [hce1, hce2, ← Real.rpow_add hx, he]

/- T8: the matching chain's landing: a0 = s/2 implies kappa = a0/s = 1/2. -/
lemma kappa_half_from_scale (s a0 : ℝ) (hs : s ≠ 0) (h : a0 = s / 2) :
    a0 / s = 1 / 2 := by
  rw [h]
  field_simp [hs]

/- T9: the rational family's deviation from the Newtonian normalization, exact. -/
lemma normalization_decomposition (eps x : ℝ) (hx : 1 + x ≠ 0) :
    (1 - ((1 + eps) * x / (1 + x))) * (1 - ((1 - eps) * x / (1 + x)))
      = -eps ^ 2 + 2 * eps ^ 2 / (1 + x) + (1 - eps ^ 2) / (1 + x) ^ 2 := by
  field_simp [hx]
  ring

end AS064
#check sorryAx
#print axioms AS064.rational_closed_form
#print axioms AS064.rational_slope_two
#print axioms AS064.rational_quadratic_coefficient
#print axioms AS064.powerlaw_collapse
#print axioms AS064.kappa_half_from_scale
#print axioms AS064.normalization_decomposition
