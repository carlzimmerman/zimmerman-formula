import Mathlib

open MeasureTheory Set Real

/-! ### polarisation tensors (propagation along z), 3x3 -/

/-- e^+ = diag(1, -1, 0) -/
def ePlus : Fin 3 → Fin 3 → ℝ := ![![1, 0, 0], ![0, -1, 0], ![0, 0, 0]]
/-- e^x = offdiag(1) in the xy block -/
def eCross : Fin 3 → Fin 3 → ℝ := ![![0, 1, 0], ![1, 0, 0], ![0, 0, 0]]

theorem ePlus_sq : ∑ i, ∑ j, ePlus i j ^ 2 = 2 := by
  simp [Fin.sum_univ_three, ePlus]; norm_num

theorem eCross_sq : ∑ i, ∑ j, eCross i j ^ 2 = 2 := by
  simp [Fin.sum_univ_three, eCross]; norm_num

theorem ePlus_eCross_orth : ∑ i, ∑ j, ePlus i j * eCross i j = 0 := by
  simp [Fin.sum_univ_three, ePlus, eCross]

theorem ePlus_traceless : ∑ i, ePlus i i = 0 := by
  simp [Fin.sum_univ_three, ePlus]

theorem eCross_traceless : ∑ i, eCross i i = 0 := by
  simp [Fin.sum_univ_three, eCross]

/-- transverse to k = z: e_{z j} = 0 = e_{j z} -/
theorem ePlus_transverse : ∀ j : Fin 3, ePlus 2 j = 0 ∧ ePlus j 2 = 0 := by
  intro j; fin_cases j <;> simp [ePlus]

theorem eCross_transverse : ∀ j : Fin 3, eCross 2 j = 0 ∧ eCross j 2 = 0 := by
  intro j; fin_cases j <;> simp [eCross]

/-- h_ij h_ij = 2 (h_+^2 + h_x^2) for h_ij = h_+ e^+_ij + h_x e^x_ij -/
theorem hij_sq (hp hx : ℝ) :
    ∑ i, ∑ j, (hp * ePlus i j + hx * eCross i j) ^ 2 = 2 * (hp ^ 2 + hx ^ 2) := by
  simp [Fin.sum_univ_three, ePlus, eCross]; ring

/-- a single polarisation: h_ij h_ij = 2 h_+^2 -/
theorem hij_sq_plus (hp : ℝ) : ∑ i, ∑ j, (hp * ePlus i j) ^ 2 = 2 * hp ^ 2 := by
  simp [Fin.sum_univ_three, ePlus]; ring

/-! ### the coupling bridge  kappa_g^2 = 32 pi G  <->  TT quadratic coefficient 1/(64 pi G) canonical -/

/-- with h_ij = kappa_g * phi_ij the quadratic action (1/(64 pi G)) (hdot_ij hdot_ij - ...) has coefficient
kappa_g^2/(64 pi G) on (phidot_ij phidot_ij - ...); it is canonical (1/2) iff kappa_g^2 = 32 pi G. -/
theorem kappa_g_bridge {G κ : ℝ} (hG : 0 < G) : κ ^ 2 = 32 * π * G ↔ κ ^ 2 / (64 * π * G) = 1 / 2 := by
  have hp := Real.pi_pos
  have : 64 * π * G ≠ 0 := by positivity
  rw [div_eq_iff this]
  constructor <;> intro h <;> linarith

/-- the same with the polarisation counting: (1/(64 pi G)) (2 x^2) = (1/2) (x / sqrt(16 pi G))^2, for phi = h_+ / sqrt(16 pi G) -/
theorem canonical_plus {G : ℝ} (hG : 0 < G) (x : ℝ) :
    (1 / (64 * π * G)) * (2 * x ^ 2) = (1 / 2) * (x / Real.sqrt (16 * π * G)) ^ 2 := by
  have hp := Real.pi_pos
  have h0 : 0 ≤ 16 * π * G := by positivity
  rw [div_pow, Real.sq_sqrt h0]
  have : 16 * π * G ≠ 0 := by positivity
  field_simp
  ring

/-- Lagrangian (time and gradient parts together): (1/(64 pi G)) (hdot_ij^2 - grad h_ij^2) = (1/2)(phidot^2 - grad phi^2) for one polarisation -/
theorem canonical_lagrangian_plus {G : ℝ} (hG : 0 < G) (p g : ℝ) :
    (1 / (64 * π * G)) * (∑ i, ∑ j, (p * ePlus i j) ^ 2 - ∑ i, ∑ j, (g * ePlus i j) ^ 2)
      = (1 / 2) * (p / Real.sqrt (16 * π * G)) ^ 2 - (1 / 2) * (g / Real.sqrt (16 * π * G)) ^ 2 := by
  rw [hij_sq_plus, hij_sq_plus]
  have h1 := canonical_plus hG p
  have h2 := canonical_plus hG g
  linarith

/-- rescaling a field by a constant rescales its time derivative by the same constant -/
theorem phi_time_derivative {s : ℝ} (f : ℝ → ℝ) (f' t : ℝ) (hf : HasDerivAt f f' t) :
    HasDerivAt (fun u => f u / s) (f' / s) t := hf.div_const s

/-! ### time averages over one period -/

theorem int_sin_sq_period {ω φ : ℝ} (hω : 0 < ω) :
    ∫ t in (0:ℝ)..(2 * π / ω), Real.sin (ω * t + φ) ^ 2 = π / ω := by
  have h := intervalIntegral.integral_comp_mul_add (a := (0:ℝ)) (b := 2 * π / ω)
    (fun u : ℝ => Real.sin u ^ 2) hω.ne' φ
  rw [h, integral_sin_sq]
  have h2 : ω * (2 * π / ω) + φ = φ + 2 * π := by field_simp; ring
  rw [h2]
  simp [Real.sin_add_two_pi, Real.cos_add_two_pi]
  field_simp

/-- the average of sin^2 over one period is 1/2 (any phase) -/
theorem avg_sin_sq {ω φ : ℝ} (hω : 0 < ω) :
    (1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω), Real.sin (ω * t + φ) ^ 2 = 1 / 2 := by
  have hp := Real.pi_pos
  rw [int_sin_sq_period hω]
  field_simp

/-- h(t) = a cos(omega t + phi):  hdot = -a omega sin(omega t + phi) -/
noncomputable def wave (a ω φ t : ℝ) : ℝ := a * Real.cos (ω * t + φ)

theorem wave_hasDerivAt (a ω φ t : ℝ) : HasDerivAt (wave a ω φ) (-(a * ω * Real.sin (ω * t + φ))) t := by
  have h1 : HasDerivAt (fun t : ℝ => ω * t + φ) ω t := by
    simpa using ((hasDerivAt_id t).const_mul ω).add_const φ
  have h2 := (h1.cos).const_mul a
  unfold wave
  refine h2.congr_deriv ?_
  ring

/-- time average over one period of  hdot_ij hdot_ij  for a single plus-polarised wave h_+ = h0 cos(omega t) : = omega^2 h0^2 -/
theorem avg_hdot_ij_sq_plus {h0 ω : ℝ} (hω : 0 < ω) :
    (1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ∑ i, ∑ j, (deriv (wave h0 ω 0) t * ePlus i j) ^ 2 = ω ^ 2 * h0 ^ 2 := by
  have hp := Real.pi_pos
  have e : ∀ t, ∑ i, ∑ j, (deriv (wave h0 ω 0) t * ePlus i j) ^ 2 = 2 * (h0 * ω) ^ 2 * Real.sin (ω * t + 0) ^ 2 := by
    intro t
    rw [(wave_hasDerivAt h0 ω 0 t).deriv, hij_sq_plus]
    ring
  simp_rw [e]
  rw [intervalIntegral.integral_const_mul, int_sin_sq_period hω]
  field_simp

/-- Isaacson: rho_GW = <hdot_ij hdot_ij>/(32 pi G) = omega^2 h0^2/(32 pi G) for h_+ = h0 cos(omega t) -/
theorem isaacson_plus {G h0 ω : ℝ} (_hG : 0 < G) (hω : 0 < ω) :
    ((1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ∑ i, ∑ j, (deriv (wave h0 ω 0) t * ePlus i j) ^ 2) / (32 * π * G) = ω ^ 2 * h0 ^ 2 / (32 * π * G) := by
  rw [avg_hdot_ij_sq_plus hω]

/-- both polarisations, arbitrary phases: <hdot_ij hdot_ij> = omega^2 (a^2 + b^2), so
rho_GW = omega^2 (a^2+b^2)/(32 pi G) = (1/(16 pi G)) <hdot_+^2 + hdot_x^2> -/
theorem avg_hdot_ij_sq_both {a b ω φp φx : ℝ} (hω : 0 < ω) :
    (1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ∑ i, ∑ j, (deriv (wave a ω φp) t * ePlus i j + deriv (wave b ω φx) t * eCross i j) ^ 2
      = ω ^ 2 * (a ^ 2 + b ^ 2) := by
  have hp := Real.pi_pos
  have e : ∀ t, ∑ i, ∑ j, (deriv (wave a ω φp) t * ePlus i j + deriv (wave b ω φx) t * eCross i j) ^ 2
      = 2 * (a * ω) ^ 2 * Real.sin (ω * t + φp) ^ 2 + 2 * (b * ω) ^ 2 * Real.sin (ω * t + φx) ^ 2 := by
    intro t
    rw [(wave_hasDerivAt a ω φp t).deriv, (wave_hasDerivAt b ω φx t).deriv, hij_sq]
    ring
  simp_rw [e]
  have i1 : IntervalIntegrable (fun t : ℝ => 2 * (a * ω) ^ 2 * Real.sin (ω * t + φp) ^ 2) MeasureTheory.volume 0 (2 * π / ω) :=
    (by fun_prop : Continuous (fun t : ℝ => 2 * (a * ω) ^ 2 * Real.sin (ω * t + φp) ^ 2)).intervalIntegrable _ _
  have i2 : IntervalIntegrable (fun t : ℝ => 2 * (b * ω) ^ 2 * Real.sin (ω * t + φx) ^ 2) MeasureTheory.volume 0 (2 * π / ω) :=
    (by fun_prop : Continuous (fun t : ℝ => 2 * (b * ω) ^ 2 * Real.sin (ω * t + φx) ^ 2)).intervalIntegrable _ _
  rw [intervalIntegral.integral_add i1 i2, intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
    int_sin_sq_period hω, int_sin_sq_period hω]
  field_simp

theorem isaacson_both {G a b ω φp φx : ℝ} (_hG : 0 < G) (hω : 0 < ω) :
    ((1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ∑ i, ∑ j, (deriv (wave a ω φp) t * ePlus i j + deriv (wave b ω φx) t * eCross i j) ^ 2) / (32 * π * G)
      = ω ^ 2 * (a ^ 2 + b ^ 2) / (32 * π * G) := by
  rw [avg_hdot_ij_sq_both hω]

/-- canonical plane wave phi(t, x) = A cos(omega t - omega x) (unit speed) -/
noncomputable def cwave (A ω t x : ℝ) : ℝ := A * Real.cos (ω * t - ω * x)

theorem cwave_dt (A ω t x : ℝ) :
    HasDerivAt (fun s => cwave A ω s x) (-(A * ω * Real.sin (ω * t - ω * x))) t := by
  have h1 : HasDerivAt (fun s : ℝ => ω * s - ω * x) ω t := by
    simpa using ((hasDerivAt_id t).const_mul ω).sub_const (ω * x)
  have h2 := (h1.cos).const_mul A
  unfold cwave
  refine h2.congr_deriv ?_
  ring

theorem cwave_dx (A ω t x : ℝ) :
    HasDerivAt (fun y => cwave A ω t y) (A * ω * Real.sin (ω * t - ω * x)) x := by
  have h1 : HasDerivAt (fun y : ℝ => ω * t - ω * y) (-ω) x := by
    simpa using ((hasDerivAt_id x).const_mul ω).const_sub (ω * t)
  have h2 := (h1.cos).const_mul A
  unfold cwave
  refine h2.congr_deriv ?_
  ring

/-- the canonical energy density (1/2)(phidot^2 + phi'^2) of the wave, averaged over one period at fixed x, is (A omega)^2/2 -/
theorem canonical_energy_avg {A ω x : ℝ} (hω : 0 < ω) :
    (1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ((1 / 2) * (deriv (fun s => cwave A ω s x) t) ^ 2 + (1 / 2) * (deriv (fun y => cwave A ω t y) x) ^ 2)
      = (A * ω) ^ 2 / 2 := by
  have hp := Real.pi_pos
  have e : ∀ t : ℝ, ((1 / 2) * (deriv (fun s => cwave A ω s x) t) ^ 2 + (1 / 2) * (deriv (fun y => cwave A ω t y) x) ^ 2)
      = (A * ω) ^ 2 * Real.sin (ω * t + (-(ω * x))) ^ 2 := by
    intro t
    rw [(cwave_dt A ω t x).deriv, (cwave_dx A ω t x).deriv]
    have : ω * t + -(ω * x) = ω * t - ω * x := by ring
    rw [this]; ring
  simp_rw [e]
  rw [intervalIntegral.integral_const_mul, int_sin_sq_period hω]
  field_simp

/-- with A = h0/sqrt(16 pi G), i.e. phi = h_+/sqrt(16 pi G) canonical: the canonical energy density equals
the Isaacson value omega^2 h0^2/(32 pi G) -/
theorem canonical_energy_matches_isaacson {G h0 ω x : ℝ} (hG : 0 < G) (hω : 0 < ω) :
    (1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ((1 / 2) * (deriv (fun s => cwave (h0 / Real.sqrt (16 * π * G)) ω s x) t) ^ 2
          + (1 / 2) * (deriv (fun y => cwave (h0 / Real.sqrt (16 * π * G)) ω t y) x) ^ 2)
      = ω ^ 2 * h0 ^ 2 / (32 * π * G) := by
  have hp := Real.pi_pos
  rw [canonical_energy_avg hω, mul_pow, div_pow, Real.sq_sqrt (by positivity)]
  have : 16 * π * G ≠ 0 := by positivity
  field_simp
  ring

#print axioms ePlus_sq
#print axioms hij_sq
#print axioms kappa_g_bridge
#print axioms canonical_plus
#print axioms canonical_lagrangian_plus
#print axioms int_sin_sq_period
#print axioms avg_sin_sq
#print axioms wave_hasDerivAt
#print axioms avg_hdot_ij_sq_plus
#print axioms isaacson_plus
#print axioms avg_hdot_ij_sq_both
#print axioms isaacson_both
#print axioms cwave_dt
#print axioms cwave_dx
#print axioms canonical_energy_avg
#print axioms canonical_energy_matches_isaacson
