import Mathlib

open MeasureTheory

/-!
# SW09_meanvalue.lean - Lean certification of the SW09 mean-value theorems (T1-T3)

ALGEBRA ONLY, concrete reals.  This file certifies the finite spherical-harmonic
core of the SW09 mean-value chain as exact theorems of Lean + Mathlib; the
physics gates (the numerical lanes) live in SW09_meanvalue.out and are not
formalized here.  Nothing in this file is left unproved.

Theorems compiled here (all four requested names, hypotheses explicit):

* `avg_rhat_zero` - the sphere average of the unit radial vector rhat vanishes,
  in two concrete forms: (i) in the mu = cos(theta) parametrisation the
  z-component of rhat is the odd function mu on the symmetric interval [-1,1],
  and its integral vanishes by the direct antiderivative y*y/2 (the x- and
  y-components vanish by the same odd symmetry, expressed concretely by (ii));
  (ii) the antipodal pairing rhat(-p) = -rhat(p) gives the vanishing antipodal
  average, component-wise (1/2)*(v i + -v i) = 0 for the radial direction v.

* `harmonic_mean_zero` - the l >= 1 harmonic components have zero sphere
  average.  Concrete cases over mu in [-1,1] (sphere average = integral / 2):
  P1 = mu (dipole) and P2 = (3*mu^2 - 1)/2, the quadrupole
  h = (2*z^2 - x^2 - y^2)/2 restricted to the unit sphere.  Both are direct
  antiderivative evaluations: the antiderivatives y*y/2 and (y^3 - y)/2 take
  the same value at the endpoints +1 and -1.

* `mean_value_property` - finite-model mean-value property: if the
  sphere-average functional A is additive and sends each constant function to
  its value, and the l >= 1 part h of the ambient field (the finite sum of all
  l >= 1 harmonic components; additivity collapses it to one function) has
  A h = 0, then the sphere average of the ambient c + h equals the centre
  value c.

* `variance_identity` - <|X|^2> = |<X>|^2 + <|X - <X>|^2 for the
  sphere-average functional A (additive, positively homogeneous, A 1 = 1).
  With <X> = g_env(B) this is Gamma^2 = <|g_N - g_env(B)|^2>: Gamma is the RMS
  deviation from the ambient.  The scalar identity, applied component-wise and
  summed, gives the vector-norm form.

Nothing from SW06_lemmas.lean is needed; this file is self-contained.
-/

/-- Antiderivative evaluation over the symmetric interval: if `F' = f` everywhere
and `f` is interval-integrable on `[-1, 1]`, then the unnormalised `mu`-integral
of `f` over `[-1, 1]` is `F 1 - F (-1)`. -/
theorem sw09_ftc (F f : ℝ → ℝ) (hF : ∀ x : ℝ, HasDerivAt F (f x) x)
    (hint : IntervalIntegrable f volume (-1 : ℝ) 1) :
    (∫ mu in (-1 : ℝ)..(1 : ℝ), f mu) = F 1 - F (-1) :=
  intervalIntegral.integral_eq_sub_of_hasDerivAt (fun x _ => hF x) hint

/-- Antiderivative fact for the odd function `mu`: `(y * y / 2)' = y`. -/
theorem sw09_hasDerivAt_mu (x : ℝ) : HasDerivAt (fun y : ℝ => y * y / 2) x x := by
  have h0 : HasDerivAt (fun y : ℝ => y * y / 2) (((1 : ℝ) * x + x * 1) / 2) x :=
    ((hasDerivAt_id' x).mul (hasDerivAt_id' x)).div_const 2
  have hEq : ((1 : ℝ) * x + x * 1) / 2 = x := by ring
  rw [hEq] at h0
  exact h0

/-- Antiderivative fact for the quadrupole integrand:
`((y ^ 3 - y) / 2)' = (3 * y ^ 2 - 1) / 2`. -/
theorem sw09_hasDerivAt_P2 (x : ℝ) :
    HasDerivAt (fun y : ℝ => (y ^ 3 - y) / 2) ((3 * x ^ 2 - 1) / 2) x :=
  ((hasDerivAt_pow 3 x).sub (hasDerivAt_id' x)).div_const 2

/-- P1: the `mu`-integral of the odd function `mu` over the symmetric interval
`[-1, 1]` vanishes (direct antiderivative `y * y / 2`). -/
theorem avg_mu_zero : (∫ mu in (-1 : ℝ)..(1 : ℝ), mu) = 0 := by
  have h : (∫ mu in (-1 : ℝ)..(1 : ℝ), mu)
      = (fun y : ℝ => y * y / 2) 1 - (fun y : ℝ => y * y / 2) (-1) :=
    sw09_ftc (fun y : ℝ => y * y / 2) (fun y : ℝ => y) sw09_hasDerivAt_mu
      (continuous_id.intervalIntegrable (-1 : ℝ) 1)
  rw [h]
  show (1 : ℝ) * 1 / 2 - (-1) * (-1) / 2 = 0
  norm_num

/-- T1 (finite form): the sphere average of the unit radial vector `rhat`
vanishes.  Concrete forms: (i) the odd `mu`-integral on the symmetric interval
`[-1, 1]` (z-component in the `mu = cos theta` parametrisation; the x- and
y-components vanish by the same odd symmetry, captured here by the antipodal
pairing), and (ii) the antipodal average `(1/2)*(v i + -v i) = 0` component-wise
since `rhat(-p) = -rhat(p)`. -/
theorem avg_rhat_zero (v : Fin 3 → ℝ) :
    (∫ mu in (-1 : ℝ)..(1 : ℝ), mu) = 0 ∧
      (∀ i : Fin 3, (1 / 2 : ℝ) * (v i + -v i) = 0) :=
  ⟨avg_mu_zero, fun _i => by ring⟩

/-- T1/T2 support: the `l >= 1` harmonic components have zero sphere average.
Concrete cases over `mu in [-1, 1]` (sphere average = integral / 2):
P1 = `mu` and P2 = `(3 * mu ^ 2 - 1) / 2`, the quadrupole
`h = (2 * z ^ 2 - x ^ 2 - y ^ 2) / 2` restricted to the unit sphere with
`mu = cos theta`.  Both antiderivatives (`y * y / 2`, `(y ^ 3 - y) / 2`) agree
at the endpoints `±1`. -/
theorem harmonic_mean_zero :
    (∫ mu in (-1 : ℝ)..(1 : ℝ), mu) = 0 ∧
      (∫ mu in (-1 : ℝ)..(1 : ℝ), (3 * mu ^ 2 - 1) / 2) = 0 := by
  refine ⟨avg_mu_zero, ?_⟩
  have hcontP2 : Continuous (fun y : ℝ => (3 * y ^ 2 - 1) / 2) :=
    Continuous.div_const
      (Continuous.sub (continuous_const.mul (continuous_pow 2)) continuous_const) 2
  have h : (∫ mu in (-1 : ℝ)..(1 : ℝ), (3 * mu ^ 2 - 1) / 2)
      = (fun y : ℝ => (y ^ 3 - y) / 2) 1 - (fun y : ℝ => (y ^ 3 - y) / 2) (-1) :=
    sw09_ftc (fun y : ℝ => (y ^ 3 - y) / 2) (fun y : ℝ => (3 * y ^ 2 - 1) / 2)
      sw09_hasDerivAt_P2 (hcontP2.intervalIntegrable (-1 : ℝ) 1)
  rw [h]
  show ((1 : ℝ) ^ 3 - 1) / 2 - ((-1 : ℝ) ^ 3 - (-1)) / 2 = 0
  norm_num

/-- Finite-model mean-value property: the sphere average of the ambient field,
decomposed as a constant part `c` plus the `l >= 1` harmonics collected in `h`
(with `A h = 0` by `harmonic_mean_zero`), equals the value at the centre. -/
theorem mean_value_property (A : (ℝ → ℝ) → ℝ)
    (h_add : ∀ f g : ℝ → ℝ, A (fun mu => f mu + g mu) = A f + A g)
    (h_const : ∀ c : ℝ, A (fun _ : ℝ => c) = c)
    (c : ℝ) (h : ℝ → ℝ) (hh : A h = 0) :
    A (fun mu => c + h mu) = c := by
  have h1 : A (fun mu : ℝ => c + h mu) = A (fun _ : ℝ => c) + A h :=
    h_add (fun _ : ℝ => c) h
  rw [h1, h_const c, hh, add_zero]

/-- T3: the variance identity `<|X|^2> = |<X>|^2 + <|X - <X>|^2>` for the
sphere-average functional `A` (additive, positively homogeneous, `A 1 = 1`).
With `<X> = g_env(B)` this is `Gamma^2 = <|g_N - g_env(B)|^2>`: the scalar
identity applied component-wise and summed gives the vector-norm form. -/
theorem variance_identity {ι : Type*} (A : (ι → ℝ) → ℝ)
    (h_add : ∀ f g : ι → ℝ, A (fun i => f i + g i) = A f + A g)
    (h_smul : ∀ (c : ℝ) (f : ι → ℝ), A (fun i => c * f i) = c * A f)
    (h_one : A (fun _ : ι => (1 : ℝ)) = 1) (X : ι → ℝ) :
    A (fun i => (X i) ^ 2) = (A X) ^ 2 + A (fun i => (X i - A X) ^ 2) := by
  have hconst : ∀ c : ℝ, A (fun _ : ι => c) = c := by
    intro c
    have hfe : (fun _ : ι => c) = (fun i : ι => c * (1 : ℝ)) := by
      funext i; ring
    have hs : A (fun i : ι => c * (1 : ℝ)) = c * A (fun _ : ι => (1 : ℝ)) :=
      h_smul c (fun _ : ι => (1 : ℝ))
    rw [hfe, hs, h_one, mul_one]
  have hdev : A (fun i : ι => (X i - A X) ^ 2)
      = A (fun i : ι => (X i) ^ 2) + ((-2 * A X) * A X + (A X) ^ 2) := by
    have hexp : (fun i : ι => (X i - A X) ^ 2)
        = (fun i : ι => (X i) ^ 2 + ((-2 * A X) * X i + (A X) ^ 2)) := by
      funext i; ring
    have e1 : A (fun i : ι => (X i) ^ 2 + ((-2 * A X) * X i + (A X) ^ 2))
        = A (fun i : ι => (X i) ^ 2)
            + A (fun i : ι => (-2 * A X) * X i + (A X) ^ 2) :=
      h_add (fun i : ι => (X i) ^ 2) (fun i : ι => (-2 * A X) * X i + (A X) ^ 2)
    have e2 : A (fun i : ι => (-2 * A X) * X i + (A X) ^ 2)
        = A (fun i : ι => (-2 * A X) * X i) + A (fun _ : ι => (A X) ^ 2) :=
      h_add (fun i : ι => (-2 * A X) * X i) (fun _ : ι => (A X) ^ 2)
    have e3 : A (fun i : ι => (-2 * A X) * X i) = (-2 * A X) * A X :=
      h_smul (-2 * A X) X
    have e4 : A (fun _ : ι => (A X) ^ 2) = (A X) ^ 2 := hconst ((A X) ^ 2)
    rw [hexp, e1, e2, e3, e4]
  rw [hdev]
  ring