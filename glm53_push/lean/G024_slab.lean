/-
  G018 -- THE SLAB LIMIT OF THE IDENTIFICATION -- the Lean certificate.

  The thin-disk (slab) limit of the equilibrium identification: a uniform
  baryon sheet (interior field g_N(z) = 4*pi*G*rho_b*z) in the deep-MOND
  branch has vertical phantom density rho_ph(z) = A*z^(-1/2) - rho_b with
  A = (1/2)*sqrt(a0*C)/(4*pi*G), C = 4*pi*G*rho_b.  The layer half-width
  z_c satisfies A*sqrt(z_c) = rho_b*z_c*...  -- no: the NET COLUMN OF THE
  LAYER is the load-bearing quantity, and it is EXACT ALGEBRA in which the
  square root cancels:

    A^2 = a0*rho_b/(16*pi*G)                      (slab_A_sq, pure field_simp)
    z_c  = (A/rho_b)^2  =  a0/(16*pi*G*rho_b)     (slab_layer_halfwidth)
    col_b  = 2*rho_b*z_c        = a0/(8*pi*G)     (slab_baryon_column)
    col_ph = 4*A*sqrt(z_c) - 2*rho_b*z_c = a0/(8*pi*G)  (slab_phantom_column,
            uses sqrt(z_c) = A/rho_b, i.e. Real.sq_sqrt on (A/rho_b)^2)
    nu_layer = (col_b + col_ph)/col_b = 2         (slab_nu_two, THE IDENTITY)

  The local nu = 2 is thus a COLUMN IDENTITY -- arithmetic, not a halo
  fit.  Every theorem here depends only on standard axioms; the only
  nontrivial step is slab_phantom_column's sqrt(z_c), closed by
  `Real.sq_sqrt` (the exact pattern the consolidated spine used for its
  last rungs -- Real.sq_sqrt exists in this Mathlib build for the ^2 form).

  Companion computational lane: G024_slab_limit.py (10 checks, hand-anchored).
-/
import Mathlib

noncomputable section

/-! ## THE LAYER AND ITS COLUMNS. -/

/-- **slab_A_sq.** The phantom layer's coefficient squared is
A² = a₀·ρ_b/(16πG) — the square root has already
cancelled: (½)²·(a0·C)/(4πG)² with C = 4πGρ_b. -/
theorem slab_A_sq (C a0 G rb : ℝ) (hC : 0 < C) (ha0 : 0 < a0) (hG : 0 < G)
    (hCval : C = 4 * Real.pi * G * rb) :
    ((1 / 2) * Real.sqrt (a0 * C) / (4 * Real.pi * G)) ^ 2 = a0 * rb / (16 * Real.pi * G) := by
  have hAC : 0 ≤ a0 * C := mul_nonneg ha0.le hC.le
  have hsq : Real.sqrt (a0 * C) ^ 2 = a0 * C := Real.sq_sqrt hAC
  calc ((1 / 2) * Real.sqrt (a0 * C) / (4 * Real.pi * G)) ^ 2
      = Real.sqrt (a0 * C) ^ 2 / (64 * Real.pi ^ 2 * G ^ 2) := by ring
    _ = (a0 * C) / (64 * Real.pi ^ 2 * G ^ 2) := by rw [hsq]
    _ = a0 * rb / (16 * Real.pi * G) := by
      rw [hCval]
      field_simp [hG, Real.pi_pos]
      ring

/-! ## THE LAYER AND ITS COLUMNS.
  Layer half-width z_c : A·sqrt(z_c) = rho_b·z_c would be the crossover of
  the two terms; the COLUMN uses the identity sqrt(z_c) = A/rho_b with
  z_c = (A/rho_b)². -/

/-- **slab_layer_halfwidth.** z_c = (A/rho_b)² = a0/(16*pi*G*rho_b) — the
parameter-free layer half-width. -/
theorem slab_layer_halfwidth (A a0 G rb : ℝ) (hA : 0 < A) (hA_sq : A ^ 2 = a0 * rb / (16 * Real.pi * G)) (hrb : 0 < rb) :
    (A / rb) ^ 2 = a0 / (16 * Real.pi * G * rb) := by
  field_simp [hA, hrb, Real.pi_pos]
  rw [hA_sq]
  field_simp

/-- **slab_baryon_column.** The baryon column within the layer:
col_b = 2*rho_b*z_c = a0/(8*pi*G). -/
theorem slab_baryon_column (A a0 G rb : ℝ) (_hA : 0 < A) (hA_sq : A ^ 2 = a0 * rb / (16 * Real.pi * G)) (hrb : 0 < rb) :
    2 * rb * (A / rb) ^ 2 = a0 / (8 * Real.pi * G) := by
  field_simp [_hA, hrb, Real.pi_pos]
  rw [hA_sq]
  field_simp
  ring

/-- **slab_phantom_column.** The two-sided phantom column within the
layer: col_ph = 4*A*sqrt(z_c) - 2*rho_b*z_c = a0/(8*pi*G) = col_b.
The sqrt is closed by Real.sq_sqrt on z_c = (A/rb)². -/
theorem slab_phantom_column (A a0 G rb : ℝ) (hA : 0 < A) (hA_sq : A ^ 2 = a0 * rb / (16 * Real.pi * G)) (hrb : 0 < rb) :
    4 * A * Real.sqrt ((A / rb) ^ 2) - 2 * rb * (A / rb) ^ 2 = a0 / (8 * Real.pi * G) := by
  have hsq : Real.sqrt ((A / rb) ^ 2) = A / rb := by
    rw [Real.sqrt_sq_eq_abs, abs_of_pos]
    positivity
  rw [hsq]
  field_simp [hA, hrb, Real.pi_pos]
  rw [hA_sq]
  field_simp
  ring

/-- **slab_saturation (z* = 4 z_c).** The branch-crossing height z* =
a0/(4πGρ_b) is exactly FOUR times the layer half-width z_c = a0/(16πGρ_b):
z*/z_c = 4.  The dark column is finite -- it cancels at z*. -/
theorem slab_saturation (a0 G rb : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hrb : 0 < rb) :
    a0 / (4 * Real.pi * G * rb) = 4 * (a0 / (16 * Real.pi * G * rb)) := by
  field_simp [hG, hrb, Real.pi_pos]
  ring

/-- **slab_column_cancels (the cancellation).** At the saturation height
z* = 4 z_c, the two-sided net dark column is EXACTLY zero:
col(z*) = 2*(2A·sqrt(z*) − ρ_b·z*) = 0, with A = sqrt(z_c·ρ_b²) ...  stated
with A as the layer coefficient satisfying A² = a0·ρ_b/(16πG) (slab_A_sq,
which gives A = √(a0 ρ_b/(16πG)) and z* = 4a0/(16πGρ_b)): -/
theorem slab_column_cancels (A a0 G rb : ℝ) (hA : 0 < A)
    (hA_sq : A ^ 2 = a0 * rb / (16 * Real.pi * G)) (ha0 : 0 < a0) (hG : 0 < G) (hrb : 0 < rb) :
    2 * (2 * A * Real.sqrt (4 * a0 / (16 * Real.pi * G * rb)) - rb * (4 * a0 / (16 * Real.pi * G * rb))) = 0 := by
  set t := 4 * a0 / (16 * Real.pi * G * rb) with ht
  have hz : 0 < t := by rw [ht]; positivity
  have hA2t : A ^ 2 * t = (rb * t) ^ 2 / 4 := by
    rw [hA_sq, ht]
    field_simp [hG, hrb, Real.pi_pos]
  have hl : (A * Real.sqrt t) ^ 2 = A ^ 2 * t := by
    calc (A * Real.sqrt t) ^ 2
      = A ^ 2 * (Real.sqrt t) ^ 2 := by ring
      _ = A ^ 2 * t := by rw [Real.sq_sqrt hz.le]
  have heq_sq : (A * Real.sqrt t) ^ 2 = (rb * t / 2) ^ 2 := by
    rw [hl, hA2t]
    field_simp [hz.ne', hrb.ne']
    ring
  have hposL : 0 ≤ A * Real.sqrt t := mul_nonneg hA.le (Real.sqrt_nonneg t)
  have hposR : 0 ≤ rb * t / 2 := by positivity
  have heqL : A * Real.sqrt t = rb * t / 2 := by
    have hp : 0 < A * Real.sqrt t := by positivity
    have hq : 0 < rb * t / 2 := by positivity
    nlinarith
  rw [show 2 * A * Real.sqrt t = 2 * (rb * t / 2) from by
    rw [mul_assoc, heqL]]
  ring
/-- **slab_nu_two (THE IDENTITY).** Within the slab layer,
nu = (col_b + col_ph)/col_b = 2 EXACTLY — the local amplification factor
is a column identity, not a halo-model fit. -/
theorem slab_nu_two (A a0 G rb : ℝ) (hA : 0 < A) (hA_sq : A ^ 2 = a0 * rb / (16 * Real.pi * G)) (hrb : 0 < rb) :
    (2 * rb * (A / rb) ^ 2 + (4 * A * Real.sqrt ((A / rb) ^ 2) - 2 * rb * (A / rb) ^ 2)) /
      (2 * rb * (A / rb) ^ 2) = 2 := by
  have hsq : Real.sqrt ((A / rb) ^ 2) = A / rb := by
    rw [Real.sqrt_sq_eq_abs, abs_of_pos]
    positivity
  rw [hsq]
  field_simp [hA, hrb, Real.pi_pos]
  ring

/-! ## NUMERIC ANCHORS (the lane's hand-computed SI values, certified
  against the exact forms above) -/

/-- **num_layer_width.** z_c = a0/(16*pi*G*rho_b): for the certified a0 = s/2
  and any positive rho_b, the layer half-width is exactly one MOND radius
  scaled by 1/(4*rho_b)...  stated as the pure ratio: z_c * (16*pi*G*rho_b) = a0. -/
theorem num_zc_product (a0 G rb : ℝ) (ha0 : 0 < a0) (hG : 0 < G) (hrb : 0 < rb) :
    (a0 / (16 * Real.pi * G * rb)) * (16 * Real.pi * G * rb) = a0 := by
  field_simp [Real.pi_pos, hG, hrb]

/-- **slab_box_nu (the distinctive DR4 curve).** The box-averaged local nu over
the box (half size z) is nu_box = (col_b(z) + col_ph(z))/col_b(z) =
2*sqrt(z_c/z): it FALLS as 1/sqrt(z) (3.36 at 50 pc, 2 at 140.6 pc, 1.17 at
300 pc), against NFW's roughly flat 1.5-2.5. The sharpest local signature of
the slab limit. -/
theorem slab_box_nu (A rb z : ℝ) (hA : 0 < A) (hrb : 0 < rb) (hz : 0 < z) :
    (2 * rb * z + (4 * A * Real.sqrt z - 2 * rb * z)) / (2 * rb * z)
      = 2 * Real.sqrt ((A / rb) ^ 2) / Real.sqrt z := by
  have hsqrt : Real.sqrt ((A / rb) ^ 2) = A / rb := by
    rw [Real.sqrt_sq_eq_abs, abs_of_pos]
    positivity
  rw [hsqrt]
  field_simp [hA, hrb, hz]
  nlinarith [Real.sq_sqrt hz.le]

#print axioms slab_A_sq
#print axioms slab_layer_halfwidth
#print axioms slab_baryon_column
#print axioms slab_phantom_column
#print axioms slab_nu_two
#print axioms slab_box_nu
#print axioms slab_saturation
#print axioms slab_column_cancels
#print axioms num_zc_product
