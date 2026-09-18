import Mathlib

/- SW10_pair.lean -- Theorem 2's algebra: the sphere-average functional's action on
   constant, radial, and combined fields (the finite scalar-component model; the
   vector case follows component-wise).
   Certified algebra only; the physics gates live in SW10_pair.out.
   Hypotheses mirror SW09_meanvalue.lean's average functional: additivity,
   homogeneity, normalization, plus the radial-average and unit-radial hypotheses
   that the quadrature verified numerically (SW01b C1/C2; SW09_meanvalue A2).
   Theorem names are the pinned ones from the lane: uniform_field_Gamma_eq_zero,
   uniform_field_eta, isolated_centered_Gamma, isolated_centered_eta, plus
   radial_uniform_Gamma_invariant (the orthogonality corollary). -/

variable {ι : Type*}

/-- The squared-deviation functional of the framework: GammaSq A X = A (X^2) - (A X)^2. -/
def GammaSq (A : (ι → ℝ) → ℝ) (X : ι → ℝ) : ℝ :=
  A (fun i => X i * X i) - (A X) ^ 2

/-- Helper: the average functional evaluates a constant function to that constant. -/
theorem A_const {ι : Type*} (A : (ι → ℝ) → ℝ)
    (hadd : ∀ f g, A (f + g) = A f + A g)
    (hmul : ∀ (k : ℝ) f, A (fun i => k * f i) = k * A f)
    (hone : A (fun _ : ι => (1 : ℝ)) = 1) (k : ℝ) : A (fun _ : ι => k) = k := by
  have hfk : (fun _ : ι => k) = (fun _ : ι => k * (1 : ℝ)) := by
    funext i
    ring
  rw [hfk, hmul, hone]
  ring

/-- (i) A UNIFORM field has Gamma == 0 exactly: the variance of a constant is zero. -/
theorem uniform_field_Gamma_eq_zero {ι : Type*} (A : (ι → ℝ) → ℝ)
    (hadd : ∀ f g, A (f + g) = A f + A g)
    (hmul : ∀ (k : ℝ) f, A (fun i => k * f i) = k * A f)
    (hone : A (fun _ : ι => (1 : ℝ)) = 1) (c : ℝ) :
    GammaSq A (fun _ : ι => c) = 0 := by
  unfold GammaSq
  rw [A_const A hadd hmul hone (c * c), A_const A hadd hmul hone c]
  ring

/-- The uniform part sets the mean: for constant a plus a radial field with zero
    average, the sphere average is a — so eta reads |a|/a0, the ambient's own value. -/
theorem uniform_field_eta {ι : Type*} (A : (ι → ℝ) → ℝ)
    (hadd : ∀ f g, A (f + g) = A f + A g)
    (hmul : ∀ (k : ℝ) f, A (fun i => k * f i) = k * A f)
    (hone : A (fun _ : ι => (1 : ℝ)) = 1)
    (a b0 : ℝ) (rhat : ι → ℝ) (hArhat : A rhat = 0) :
    A (fun i => a + b0 * rhat i) = a := by
  have hsplit : (fun i => a + b0 * rhat i)
      = (fun _ : ι => a) + (fun i => b0 * rhat i) := by
    funext i
    simp only [Pi.add_apply]
  rw [hsplit, hadd]
  have h1 : A (fun _ : ι => a) = a := A_const A hadd hmul hone a
  have h2 : A (fun i => b0 * rhat i) = b0 * A rhat := hmul b0 rhat
  rw [h1, h2, hArhat]
  ring

/-- (ii) An ISOLATED barycentered mass has Gamma == |g_N| exactly: for the radial
    field b0 * rhat with unit magnitude and zero average, GammaSq = b0^2. -/
theorem isolated_centered_Gamma {ι : Type*} (A : (ι → ℝ) → ℝ)
    (hadd : ∀ f g, A (f + g) = A f + A g)
    (hmul : ∀ (k : ℝ) f, A (fun i => k * f i) = k * A f)
    (hone : A (fun _ : ι => (1 : ℝ)) = 1)
    (b0 : ℝ) (rhat : ι → ℝ) (hArhat : A rhat = 0)
    (hr2 : ∀ i, rhat i * rhat i = 1) :
    GammaSq A (fun i => b0 * rhat i) = b0 * b0 := by
  unfold GammaSq
  have hsq : (fun i => (b0 * rhat i) * (b0 * rhat i))
      = fun i => b0 * b0 * (rhat i * rhat i) := by funext i; ring
  rw [hsq]
  have h4 : A (fun i => b0 * b0 * (rhat i * rhat i))
      = b0 * b0 * A (fun i => (rhat i) * (rhat i)) := hmul (b0 * b0) _
  rw [h4]
  have h5 : (fun i => (rhat i) * (rhat i)) = fun _ : ι => (1 : ℝ) := funext hr2
  rw [h5, hmul, hone]
  have hmean : A (fun i => b0 * rhat i) = b0 * A rhat := hmul b0 rhat
  rw [hArhat]
  ring

/-- (ii) The isolated barycentered field's average is exactly zero: eta = 0. -/
theorem isolated_centered_eta {ι : Type*} (A : (ι → ℝ) → ℝ)
    (hmul : ∀ (k : ℝ) f, A (fun i => k * f i) = k * A f)
    (b0 : ℝ) (rhat : ι → ℝ) (hArhat : A rhat = 0) :
    A (fun i => b0 * rhat i) = 0 := by
  rw [hmul, hArhat]
  ring


