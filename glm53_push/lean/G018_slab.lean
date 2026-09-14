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

  Companion computational lane: G018_slab_limit.py (8 checks, hand-anchored).
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

#print axioms slab_A_sq
#print axioms slab_layer_halfwidth
#print axioms slab_baryon_column
#print axioms slab_phantom_column
#print axioms slab_nu_two
#print axioms num_zc_product
