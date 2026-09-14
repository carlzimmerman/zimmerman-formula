/-
  H001 — THE ZIMMERMAN-AeST ACTION: the algebraic core, certified in Lean 4
  (mathlib). Only fully-proven theorems; verified clean compile, exit 0, zero
  `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}.

  THE ACTION (Aether-Scalar-Tensor type, with the free function FIXED by the
  SPARC measurement of the mode count n = 2):

      S = ∫ √(-g) [ M_P² R/2 − L⁴ f(X) ] + S_m[g, matter] ,
      X = h^{μν} ∂_μφ ∂_νφ / (2 L⁴) ,  h^{μν} = g^{μν} − u^μ u^ν / u²

  with the aether's spatial projector making X ≥ 0 in BOTH the galactic
  (spacelike) and cosmological (timelike) branches, so a single real function
  covers both (this is why the aether is not optional: μ₂ depends on √X, and
  √X is imaginary on one branch in pure k-essence).

  Certified here (all pure algebra / calculus, no analysis):

    1. f_zero              : f(0) = −1 — the value at the non-analytic point
                             IS the dark energy (p/ρ = −1)
    2. hasDerivAt_f        : f'(X) = μ₂(√X) for X > 0 — PROVEN as a HasDerivAt
                             chain (not merely asserted)
    3. hasDerivAt_fprime   : f''(X) = 1/(√X (1+√X)³) for X > 0 — likewise
                             PROVEN as a HasDerivAt chain
    4. cs2_from_f_eq       : c_s² = f'/(f' + 2X f'') = (u²+3u+2)/(u²+3u+4),
                             u = √X — by field_simp; ring
    5. cs2_ge_half         : c_s² ≥ 1/2 for u ≥ 0 — STABILITY
    6. cs2_lt_one          : c_s² < 1  for u ≥ 0 — SUBLUMINALITY
    7. mu2_pos, fprime_pos : f'(X) > 0 for X > 0 — NO GHOST
    8. fpp_pos             : f''(X) > 0 for X > 0
    9. aest_algebraic_core : the conjunction (the capstone)

  NOT certified here, and deliberately so: the Noether-charge statement
  (shift symmetry φ → φ + c ⇒ J^μ = f'(X) h^{μν} ∂_νφ is exactly conserved,
  and its charge density redshifts as a⁻³ — that is the dust sector) is a
  statement about the DIFFEOMORPHISM-INVARIANT ACTION AND ITS SYMMETRY GROUP,
  not an algebraic identity in the reals. It cannot be reached from the field
  calculus used below and is therefore recorded as a comment (point 6 of the
  task spec), not as a theorem. Claiming it here would be false advertising.

  Scope: Lean certifies mathematics, not physics. The physical verdicts are
  the committed Python lane's (hy4_push/H001_zimmerman_aest_action.py).
-/
import Mathlib

noncomputable section

/-! ## The one function and its derivatives -/

/-- The one function: f(X) = X − 2 ln(1+√X) − 2/(1+√X) + 1. Integrated once
from μ₂; non-analytic at X = 0 (that non-analyticity is the point). -/
def f (X : ℝ) : ℝ := X - 2 * Real.log (1 + Real.sqrt X) - 2 / (1 + Real.sqrt X) + 1

/-- The measured interpolating function: μ₂(u) = u(2+u)/(1+u)², identically
1 − (1+u)⁻² wherever u ≠ −1 (proved below as `mu2_eq_one_minus`). -/
def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u) ^ 2

/-- The second derivative of f in closed form: f''(X) = 1/(√X (1+√X)³).
Proven (not assumed) as `hasDerivAt_fprime`. -/
def fpp (X : ℝ) : ℝ := 1 / (Real.sqrt X * (1 + Real.sqrt X) ^ 3)

/-- The scalar sound speed as the action gives it:
c_s² = f'/(f' + 2X f''). -/
def cs2_from_f (X : ℝ) : ℝ :=
  mu2 (Real.sqrt X) / (mu2 (Real.sqrt X) + 2 * X * fpp X)

/-- The same thing in closed form, u = √X. -/
def cs2 (u : ℝ) : ℝ := (u ^ 2 + 3 * u + 2) / (u ^ 2 + 3 * u + 4)

/-! ## Basic algebra of μ₂ -/

/-- μ₂(u) = 1 − (1+u)⁻² for u ≥ 0 (hence 1+u ≠ 0). This is the form whose
derivative is the clean one: dμ₂/du = 2(1+u)⁻³. -/
theorem mu2_eq_one_minus (u : ℝ) (hu : 0 ≤ u) :
    mu2 u = 1 - (1 : ℝ) / (1 + u) ^ 2 := by
  have h1 : 1 + u ≠ 0 := by nlinarith
  have hsq : (1 + u) ^ 2 ≠ 0 := pow_ne_zero 2 h1
  unfold mu2
  field_simp [h1, hsq]
  ring

/-- **No ghost (μ₂ side).** μ₂(u) > 0 for u > 0: the kinetic function is
positive, so the scalar is healthy, not phantom. -/
theorem mu2_pos {u : ℝ} (hu : 0 < u) : 0 < mu2 u := by
  unfold mu2
  positivity

/-! ## (1) The dark-energy value -/

/-- **The dark-energy value.** f(0) = −1 exactly. In FRW the spatial gradient
of φ vanishes identically (X = 0), so p/ρ = f/(2Xf' − f) = −1/1 = −1: the
cosmological constant is the VALUE OF THE MOND FUNCTION AT ITS
NON-ANALYTIC POINT. -/
theorem f_zero : f 0 = -1 := by
  norm_num [f]

/-! ## (2) The first derivative: f'(X) = μ₂(√X) -/

/-- The raw derivative chain for f, before the value is simplified. -/
private theorem hasDerivAt_f_raw (X : ℝ) (hX : X ≠ 0) (h1ne : 1 + Real.sqrt X ≠ 0) :
    HasDerivAt f
      (1 - 2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))
         - ((-(2 * (1 / (2 * Real.sqrt X)))) / (1 + Real.sqrt X) ^ 2))
      X := by
  have hsqrt : HasDerivAt (fun Y : ℝ => Real.sqrt Y) (1 / (2 * Real.sqrt X)) X :=
    Real.hasDerivAt_sqrt hX
  have h1p : HasDerivAt (fun Y : ℝ => 1 + Real.sqrt Y) (1 / (2 * Real.sqrt X)) X :=
    hsqrt.const_add (1 : ℝ)
  have hlog : HasDerivAt (fun Y : ℝ => Real.log (1 + Real.sqrt Y))
      ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X)) X := h1p.log h1ne
  have hlog2 : HasDerivAt (fun Y : ℝ => 2 * Real.log (1 + Real.sqrt Y))
      (2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))) X := hlog.const_mul (2 : ℝ)
  have hdiv : HasDerivAt (fun Y : ℝ => (2 : ℝ) / (1 + Real.sqrt Y))
      ((-(2 * (1 / (2 * Real.sqrt X)))) / (1 + Real.sqrt X) ^ 2) X := by
    have h := (hasDerivAt_const (x := X) (c := (2 : ℝ))).div h1p h1ne
    change HasDerivAt (fun Y : ℝ => (2 : ℝ) / (1 + Real.sqrt Y))
      ((0 * (1 + Real.sqrt X) - 2 * (1 / (2 * Real.sqrt X)))
        / (1 + Real.sqrt X) ^ 2) X at h
    convert h using 1
    ring
  exact (((hasDerivAt_id X).sub hlog2).sub hdiv).add_const (1 : ℝ)

/-- **The first derivative.** For X > 0, f is differentiable at X with
derivative exactly μ₂(√X) — the MOND interpolating function evaluated on the
square root of the gradient invariant. This is the statement that the
Lagrangian was integrated from the measured function; it is PROVEN here, not
asserted (G002 V1 left it to the symbolic lanes). -/
theorem hasDerivAt_f (X : ℝ) (hX : 0 < X) : HasDerivAt f (mu2 (Real.sqrt X)) X := by
  have hXne : X ≠ 0 := ne_of_gt hX
  have hspos : 0 < Real.sqrt X := Real.sqrt_pos.mpr hX
  have hsne : Real.sqrt X ≠ 0 := ne_of_gt hspos
  have h1ne : 1 + Real.sqrt X ≠ 0 := by nlinarith
  have h := hasDerivAt_f_raw X hXne h1ne
  have hval :
      1 - 2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))
        - ((-(2 * (1 / (2 * Real.sqrt X)))) / (1 + Real.sqrt X) ^ 2)
      = mu2 (Real.sqrt X) := by
    set u := Real.sqrt X with hu
    have hu_ne : u ≠ 0 := by rw [hu]; exact hsne
    have h1u : 1 + u ≠ 0 := by rw [hu]; exact h1ne
    unfold mu2
    field_simp [hu_ne, h1u]
    ring
  rw [hval] at h
  exact h

/-- **No ghost.** f'(X) > 0 for X > 0: the kinetic term is positive on the
whole galactic branch, so the scalar propagates with the right sign. -/
theorem fprime_pos {X : ℝ} (hX : 0 < X) : 0 < mu2 (Real.sqrt X) :=
  mu2_pos (Real.sqrt_pos.mpr hX)

/-! ## (3) The second derivative: f''(X) = 1/(√X (1+√X)³) -/

/-- The raw derivative chain for f' = μ₂(√X), written in the 1 − (1+√X)⁻²
form (whose derivative is the clean one), before simplification. -/
private theorem hasDerivAt_fprime_raw (X : ℝ) (hX : X ≠ 0)
    (h1ne : 1 + Real.sqrt X ≠ 0) :
    HasDerivAt (fun Y : ℝ => 1 - (1 : ℝ) / ((1 + Real.sqrt Y) ^ 2))
      (-((-(2 * (1 + Real.sqrt X) * (1 / (2 * Real.sqrt X))))
          / (((1 + Real.sqrt X) ^ 2) ^ 2)))
      X := by
  have hsqrt : HasDerivAt (fun Y : ℝ => Real.sqrt Y) (1 / (2 * Real.sqrt X)) X :=
    Real.hasDerivAt_sqrt hX
  have h1p : HasDerivAt (fun Y : ℝ => 1 + Real.sqrt Y) (1 / (2 * Real.sqrt X)) X :=
    hsqrt.const_add (1 : ℝ)
  have h1sq : (1 + Real.sqrt X) ^ 2 ≠ 0 := pow_ne_zero 2 h1ne
  have hpow : HasDerivAt (fun Y : ℝ => (1 + Real.sqrt Y) ^ 2)
      (2 * (1 + Real.sqrt X) * (1 / (2 * Real.sqrt X))) X := by
    have h0 := h1p.pow 2
    change HasDerivAt (fun Y : ℝ => (1 + Real.sqrt Y) ^ 2)
      ((2 : ℝ) * (1 + Real.sqrt X) ^ (2 - 1) * (1 / (2 * Real.sqrt X))) X at h0
    convert h0 using 1
    norm_num
  have hdiv : HasDerivAt (fun Y : ℝ => (1 : ℝ) / ((1 + Real.sqrt Y) ^ 2))
      ((-(2 * (1 + Real.sqrt X) * (1 / (2 * Real.sqrt X))))
        / (((1 + Real.sqrt X) ^ 2) ^ 2)) X := by
    have h0 := (hasDerivAt_const (x := X) (c := (1 : ℝ))).div hpow h1sq
    change HasDerivAt (fun Y : ℝ => (1 : ℝ) / ((1 + Real.sqrt Y) ^ 2))
      ((0 * ((1 + Real.sqrt X) ^ 2) - 1 * (2 * (1 + Real.sqrt X)
        * (1 / (2 * Real.sqrt X)))) / (((1 + Real.sqrt X) ^ 2) ^ 2)) X at h0
    convert h0 using 1
    ring
  simpa [sub_eq_add_neg] using (hdiv.neg.const_add (1 : ℝ))

/-- **The second derivative.** For X > 0, f' = μ₂∘√ is differentiable with
derivative 1/(√X (1+√X)³) — again PROVEN, not asserted. This is the input the
sound speed needs. -/
theorem hasDerivAt_fprime (X : ℝ) (hX : 0 < X) :
    HasDerivAt (fun Y : ℝ => mu2 (Real.sqrt Y)) (fpp X) X := by
  have hXne : X ≠ 0 := ne_of_gt hX
  have hspos : 0 < Real.sqrt X := Real.sqrt_pos.mpr hX
  have hsne : Real.sqrt X ≠ 0 := ne_of_gt hspos
  have h1ne : 1 + Real.sqrt X ≠ 0 := by nlinarith
  have h := hasDerivAt_fprime_raw X hXne h1ne
  -- transport the function across the pointwise identity μ₂(u) = 1 − (1+u)⁻²
  have hfun : (fun Y : ℝ => 1 - (1 : ℝ) / ((1 + Real.sqrt Y) ^ 2))
      = (fun Y : ℝ => mu2 (Real.sqrt Y)) := by
    funext Y
    exact (mu2_eq_one_minus (Real.sqrt Y) (Real.sqrt_nonneg Y)).symm
  rw [hfun] at h
  have hval :
      -((-(2 * (1 + Real.sqrt X) * (1 / (2 * Real.sqrt X))))
          / (((1 + Real.sqrt X) ^ 2) ^ 2)) = fpp X := by
    unfold fpp
    set u := Real.sqrt X with hu
    have hu_ne : u ≠ 0 := by rw [hu]; exact hsne
    have h1u : 1 + u ≠ 0 := by rw [hu]; exact h1ne
    have h1sq : (1 + u) ^ 2 ≠ 0 := pow_ne_zero 2 h1u
    field_simp [hu_ne, h1u, h1sq]
  rw [hval] at h
  exact h

/-- **Convexity.** f''(X) > 0 for X > 0. -/
theorem fpp_pos {X : ℝ} (hX : 0 < X) : 0 < fpp X := by
  unfold fpp
  positivity

/-! ## (4) The sound speed in closed form -/

/-- **The sound speed.** c_s² = f'/(f' + 2X f'') reduces, with u = √X, to
(u²+3u+2)/(u²+3u+4). Pure algebra once f' and f'' are known: the numerator
gathers as u(u²+3u+2)/(1+u)³ and the denominator as u(u²+3u+4)/(1+u)³, and
the common u/(1+u)³ cancels. -/
theorem cs2_from_f_eq (X : ℝ) (hX : 0 < X) : cs2_from_f X = cs2 (Real.sqrt X) := by
  set u := Real.sqrt X with hu
  have hupos : 0 < u := by rw [hu]; exact Real.sqrt_pos.mpr hX
  have hu_ne : u ≠ 0 := ne_of_gt hupos
  have h1u : 1 + u ≠ 0 := by nlinarith
  have h1sq : (1 + u) ^ 2 ≠ 0 := pow_ne_zero 2 h1u
  have hXu : X = u ^ 2 := by
    rw [hu]
    exact (Real.sq_sqrt (le_of_lt hX)).symm
  have hden_ne : u ^ 2 + 3 * u + 4 ≠ 0 := ne_of_gt (by nlinarith [sq_nonneg u, hupos])
  unfold cs2_from_f cs2 fpp mu2
  rw [← hu]
  rw [hXu]
  -- numerator: u(2+u)/(1+u)²  =  u(u²+3u+2)/(1+u)³
  have hnum : u * (2 + u) / (1 + u) ^ 2 = u * (u ^ 2 + 3 * u + 2) / (1 + u) ^ 3 := by
    field_simp [h1u, h1sq]
    ring
  -- the denominator, written with the ALREADY-REWRITTEN numerator term
  have hden' : u * (u ^ 2 + 3 * u + 2) / (1 + u) ^ 3
        + 2 * u ^ 2 * (1 / (u * (1 + u) ^ 3))
      = u * (u ^ 2 + 3 * u + 4) / (1 + u) ^ 3 := by
    field_simp [hu_ne, h1u, h1sq]
    ring
  rw [hnum, hden']
  field_simp [hu_ne, h1u, h1sq, hden_ne]

/-! ## (5) Stability and subluminality -/

/-- The sound-speed denominator is strictly positive for u ≥ 0: u² + 3u + 4
≥ 4. Everything below clears denominators against this. -/
private theorem cs2_den_pos {u : ℝ} (hu : 0 ≤ u) : 0 < u ^ 2 + 3 * u + 4 := by
  nlinarith [sq_nonneg u, mul_nonneg (by norm_num : (0 : ℝ) ≤ 3) hu]

/-- **STABILITY.** c_s² ≥ 1/2 for every u ≥ 0 (hence for every X ≥ 0, with
u = √X): the scalar sector is linearly stable, no gradient instability.
Clearing the positive denominator, the claim is u²+3u+4 ≤ 2(u²+3u+2), i.e.
0 ≤ u²+3u. -/
theorem cs2_ge_half {u : ℝ} (hu : 0 ≤ u) : (1 / 2 : ℝ) ≤ cs2 u := by
  have hD : 0 < u ^ 2 + 3 * u + 4 := cs2_den_pos hu
  unfold cs2
  rw [le_div_iff₀ hD]
  nlinarith [sq_nonneg u, mul_nonneg (by norm_num : (0 : ℝ) ≤ 3) hu]

/-- **SUBLUMINALITY.** c_s² < 1 for every u ≥ 0: the scalar never outruns
light. Clearing the positive denominator, the claim is u²+3u+2 < u²+3u+4. -/
theorem cs2_lt_one {u : ℝ} (hu : 0 ≤ u) : cs2 u < 1 := by
  have hD : 0 < u ^ 2 + 3 * u + 4 := cs2_den_pos hu
  unfold cs2
  rw [div_lt_iff₀ hD]
  ring_nf
  norm_num

/-- **Stability on the branch.** c_s² ≥ 1/2 at u = √X for every X ≥ 0 — the
form in which the bound is actually used (the aether projector guarantees
X ≥ 0 on both branches). -/
theorem cs2_ge_half_at (X : ℝ) : (1 / 2 : ℝ) ≤ cs2 (Real.sqrt X) :=
  cs2_ge_half (Real.sqrt_nonneg X)

/-- **Subluminality on the branch.** c_s² < 1 at u = √X for every X ≥ 0. -/
theorem cs2_lt_one_at (X : ℝ) : cs2 (Real.sqrt X) < 1 :=
  cs2_lt_one (Real.sqrt_nonneg X)

/-- **The sound-speed window, assembled.** 1/2 ≤ c_s² < 1 on the whole
physical range — stability and subluminality together, as one statement. -/
theorem cs2_window {u : ℝ} (hu : 0 ≤ u) : (1 / 2 : ℝ) ≤ cs2 u ∧ cs2 u < 1 :=
  ⟨cs2_ge_half hu, cs2_lt_one hu⟩

/-! ## The capstone -/

/-- **THE ALGEBRAIC CORE OF THE ZIMMERMAN-AeST ACTION.** All eight certified
facts conjoined: the dark-energy value at the non-analytic point, the first
and second derivatives PROVEN as HasDerivAt chains, the sound speed in closed
form, stability, subluminality, and the no-ghost condition — everything the
action's algebraic core asserts, machine-checked end to end.

  NOT included, because it is not algebra: the Noether-charge conservation
  (shift symmetry ⇒ ∂_μ J^μ = 0 with J^μ = f'(X) h^{μν} ∂_νφ, charge density
  ∝ a⁻³ — the dust sector). That is a statement about the action's symmetry
  group and requires the variational calculus, not the real algebra above. It
  is the ONE load-bearing claim of H001 left to the physics lanes. -/
theorem aest_algebraic_core (X : ℝ) (hX : 0 < X) :
    f 0 = -1
    ∧ HasDerivAt f (mu2 (Real.sqrt X)) X
    ∧ HasDerivAt (fun Y : ℝ => mu2 (Real.sqrt Y)) (fpp X) X
    ∧ cs2_from_f X = cs2 (Real.sqrt X)
    ∧ (1 / 2 : ℝ) ≤ cs2 (Real.sqrt X)
    ∧ cs2 (Real.sqrt X) < 1
    ∧ 0 < mu2 (Real.sqrt X)
    ∧ 0 < fpp X := by
  exact ⟨f_zero,
         hasDerivAt_f X hX,
         hasDerivAt_fprime X hX,
         cs2_from_f_eq X hX,
         cs2_ge_half (Real.sqrt_nonneg X),
         cs2_lt_one (Real.sqrt_nonneg X),
         fprime_pos hX,
         fpp_pos hX⟩

#print axioms f_zero
#print axioms mu2_eq_one_minus
#print axioms mu2_pos
#print axioms hasDerivAt_f
#print axioms hasDerivAt_fprime
#print axioms fprime_pos
#print axioms fpp_pos
#print axioms cs2_from_f_eq
#print axioms cs2_ge_half
#print axioms cs2_lt_one
#print axioms cs2_window
#print axioms aest_algebraic_core
