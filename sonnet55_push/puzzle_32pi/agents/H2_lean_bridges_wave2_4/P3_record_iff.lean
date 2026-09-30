import Mathlib

open Real MeasureTheory intervalIntegral

/-!
# P3: the record's iff, the enthalpy family, the sharp-kernel moment, the Sciama integral, the N-count (lanes X3 and the record)

Conventions: a0 = kappa c sqrt(G rho) (kappa = a0/(c sqrt(G rho)); the framework's kappa = 1/2 is FITTED), R* = c/sqrt(G rho) = t_Lambda c (t_Lambda = 1/sqrt(G rho)),
M1 = (2/3) c/a0 (the first moment of the memory kernel required by the action, as transcribed from the record's `mi_N_count_and_kappa_iff_2026.py` Part C).

CERTIFIED (premises => conclusions):
 (1) `kappa_half_iff_M1`: kappa = 1/2  <=>  M1 = (4/3) t_Lambda (algebra; no kernel shape enters).  Control: `kappa_iff_M1_unit`: M1 = 1 t_Lambda <=> kappa = 2/3.
 (2) `enthalpy_family`: for w > -1, M1 = (1 + w) t_Lambda <=> kappa = 2/(3 (1 + w)); w = 1/3 gives 1/2 (`kappa_w_values`: w = 0 -> 2/3, w = 1 -> 1/3);
     `kappa_half_iff_w`: kappa(w) = 1/2 <=> w = 1/3; `kappa_dim`: w = 1/d gives kappa = (2/3) d/(d+1), which is 1/2 iff d = 3.  (This is the family of the record's premise
     "M1 = (rho + p)/rho t_Lambda" for an equation of state w; nothing here says the vacuum has w = 1/3.)
 (3) `kernel_norm`, `kernel_first_moment`: the sharp kernel K(tau) = 2 tau/T^2 on [0, T] is normalised and has first moment int tau K = 2T/3 (Mathlib interval integrals); the
     uniform kernel has T/2 (`uniform_first_moment`, the mutation control).  With T = R_c/c: M1 = (2/3) R_c/c, so M1 = (2/3) c/a0 <=> R_c = c^2/a0 (`Rc_iff`), and
     kappa = 1/2 <=> R_c = 2 R* (`Rc_eq_two_Rstar_iff`).  I.e. the record's requirement is EXACTLY "the cutoff is the Rindler distance of a0", which for kappa = 1/2 is twice R*.
 (4) Sciama: the potential of a uniform ball, Phi/(G rho) = int_0^R 4 pi r^2 (1/r) dr = 2 pi R^2 (`sciama_potential`); I(R) = 2 pi G rho R^2/c^2.  With H^2 = 8 pi G rho/3: I(c/H) = 3/4
     (pi cancels: `sciama_hubble`), I(R*) = 2 pi (`sciama_Rstar`), I(2R*) = 8 pi (`sciama_2Rstar`); closure I = 1 at R_S with R_S^2/R_H^2 = 4/3, R_S^2 = R*^2/(2 pi)
     (`sciama_closure`), (2R*)^2/R_S^2 = 8 pi.  The Rindler conversion a_c = c^2/R_c gives a_c^2/(G rho c^2) = 8 pi/3 (R_H), 2 pi (R_S), 1 (R*), 1/4 (2R*) (`rindler_conversion`);
     with a coupling factor g the closure at the Rindler cutoff gives a0^2/(G rho c^2) = 2 pi g, so the puzzle needs g = 1/(8 pi) (`coupling_factor`).
 (5) `mu_slope`: for mu(p) = 1 - (1 - p)^N and p = (g/s)/(1 + g/s): mu'(0) = N/s in g, so a0 = 1/mu'(0) = s/N; with s = c sqrt(G rho): N = 2 <=> kappa = 1/2 (`N_two_iff`).

NOT certified: that M1 = (4/3) t_Lambda, N = 2, w = 1/3 or that the cutoff is 2 R* hold in nature or follow from any action; kappa = 1/2 stays FITTED.  Lean certifies that these
statements are ONE statement, not that any is true.
-/

namespace RecordIff

/-- a0 = kappa c sqrt(G rho) -/
noncomputable def a0of (κ c G ρ : ℝ) : ℝ := κ * c * Real.sqrt (G * ρ)
/-- M1 = (2/3) c/a0 -/
noncomputable def M1of (c a0 : ℝ) : ℝ := (2 / 3) * c / a0
/-- t_Lambda = (G rho)^(-1/2) -/
noncomputable def tLam (G ρ : ℝ) : ℝ := 1 / Real.sqrt (G * ρ)

theorem sqrt_pos' {G ρ : ℝ} (hG : 0 < G) (hρ : 0 < ρ) : 0 < Real.sqrt (G * ρ) := Real.sqrt_pos.mpr (by positivity)

/-- (1) the record's iff -/
theorem kappa_half_iff_M1 {κ c G ρ : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    M1of c (a0of κ c G ρ) = (4 / 3) * tLam G ρ ↔ κ = 1 / 2 := by
  have hs := sqrt_pos' hG hρ
  unfold M1of a0of tLam
  rw [div_eq_iff (by positivity)]
  constructor
  · intro h
    field_simp at h
    nlinarith [h]
  · intro h; rw [h]; field_simp; ring

/-- control: M1 = 1 t_Lambda gives kappa = 2/3, not 1/2 -/
theorem kappa_iff_M1_unit {κ c G ρ : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    M1of c (a0of κ c G ρ) = 1 * tLam G ρ ↔ κ = 2 / 3 := by
  have hs := sqrt_pos' hG hρ
  unfold M1of a0of tLam
  rw [div_eq_iff (by positivity)]
  constructor
  · intro h
    field_simp at h
    nlinarith [h]
  · intro h; rw [h]; field_simp

/-- (2) the enthalpy family: M1 = (1 + w) t_Lambda <=> kappa = 2/(3 (1 + w)) -/
theorem enthalpy_family {κ c G ρ w : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) (hw : -1 < w) :
    M1of c (a0of κ c G ρ) = (1 + w) * tLam G ρ ↔ κ = 2 / (3 * (1 + w)) := by
  have hs := sqrt_pos' hG hρ
  have hw1 : 0 < 1 + w := by linarith
  unfold M1of a0of tLam
  rw [div_eq_iff (by positivity)]
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h; rw [h]; field_simp

theorem kappa_w_values : (2 : ℝ) / (3 * (1 + 1 / 3)) = 1 / 2 ∧ (2 : ℝ) / (3 * (1 + 0)) = 2 / 3 ∧ (2 : ℝ) / (3 * (1 + 1)) = 1 / 3 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- kappa(w) = 1/2 <=> w = 1/3 -/
theorem kappa_half_iff_w {w : ℝ} (hw : -1 < w) : 2 / (3 * (1 + w)) = 1 / 2 ↔ w = 1 / 3 := by
  have hw1 : 0 < 1 + w := by linarith
  rw [div_eq_div_iff (by positivity) (by norm_num)]
  constructor <;> intro h <;> linarith

/-- w = 1/d (radiation in d spatial dimensions): kappa = (2/3) d/(d + 1); equals 1/2 iff d = 3 -/
theorem kappa_dim {d : ℝ} (hd : 0 < d) :
    2 / (3 * (1 + 1 / d)) = (2 / 3) * (d / (d + 1)) ∧ (2 / (3 * (1 + 1 / d)) = 1 / 2 ↔ d = 3) := by
  have hd0 : d ≠ 0 := hd.ne'
  have h1 : 2 / (3 * (1 + 1 / d)) = (2 / 3) * (d / (d + 1)) := by
    field_simp
  refine ⟨h1, ?_⟩
  rw [h1]
  have hd1 : 0 < d + 1 := by linarith
  have hd10 : d + 1 ≠ 0 := hd1.ne'
  constructor
  · intro h
    field_simp at h
    linarith
  · intro h
    rw [h]; norm_num

/-- (3) the sharp kernel K(tau) = 2 tau/T^2 on [0, T] is normalised -/
theorem kernel_norm {T : ℝ} (hT : 0 < T) : ∫ τ in (0:ℝ)..T, 2 * τ / T ^ 2 = 1 := by
  have hT0 : T ≠ 0 := hT.ne'
  have : (fun τ : ℝ => 2 * τ / T ^ 2) = fun τ => (2 / T ^ 2) * τ := by funext τ; ring
  rw [this, intervalIntegral.integral_const_mul, integral_id]
  field_simp; ring

/-- ... and has first moment 2T/3 -/
theorem kernel_first_moment {T : ℝ} (hT : 0 < T) : ∫ τ in (0:ℝ)..T, τ * (2 * τ / T ^ 2) = 2 * T / 3 := by
  have hT0 : T ≠ 0 := hT.ne'
  have : (fun τ : ℝ => τ * (2 * τ / T ^ 2)) = fun τ => (2 / T ^ 2) * τ ^ 2 := by funext τ; ring
  rw [this, intervalIntegral.integral_const_mul, integral_pow]
  field_simp; ring

/-- control: the UNIFORM kernel 1/T has first moment T/2 -/
theorem uniform_first_moment {T : ℝ} (hT : 0 < T) : ∫ τ in (0:ℝ)..T, τ * (1 / T) = T / 2 := by
  have hT0 : T ≠ 0 := hT.ne'
  have : (fun τ : ℝ => τ * (1 / T)) = fun τ => (1 / T) * τ := by funext τ; ring
  rw [this, intervalIntegral.integral_const_mul, integral_id]
  field_simp; ring

/-- M1 = 2T/3 with T = R_c/c is (2/3) R_c/c; and (2/3) R_c/c = (2/3) c/a0 <=> R_c = c^2/a0 -/
theorem Rc_iff {c a0 Rc : ℝ} (hc : 0 < c) (ha : 0 < a0) : (2 / 3) * Rc / c = (2 / 3) * c / a0 ↔ Rc = c ^ 2 / a0 := by
  have hc0 : c ≠ 0 := hc.ne'
  have ha0 : a0 ≠ 0 := ha.ne'
  rw [div_eq_div_iff hc0 ha0]
  constructor
  · intro h
    field_simp
    nlinarith [h]
  · intro h; rw [h]; field_simp

/-- kappa = 1/2 <=> R_c = c^2/a0 equals 2 R*, R* = c/sqrt(G rho) -/
theorem Rc_eq_two_Rstar_iff {κ c G ρ : ℝ} (hκ : 0 < κ) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    c ^ 2 / a0of κ c G ρ = 2 * (c / Real.sqrt (G * ρ)) ↔ κ = 1 / 2 := by
  have hs := sqrt_pos' hG hρ
  unfold a0of
  rw [div_eq_iff (by positivity)]
  constructor
  · intro h
    field_simp at h
    nlinarith [h]
  · intro h; rw [h]; field_simp

/-- (4) the potential of a uniform ball at its centre: int_0^R 4 pi r^2 (1/r) dr = 2 pi R^2 -/
theorem sciama_potential (R : ℝ) : ∫ r in (0:ℝ)..R, 4 * π * r ^ 2 * (1 / r) = 2 * π * R ^ 2 := by
  have : (fun r : ℝ => 4 * π * r ^ 2 * (1 / r)) = fun r => (4 * π) * r := by
    funext r
    rcases eq_or_ne r 0 with h | h
    · simp [h]
    · field_simp
  rw [this, intervalIntegral.integral_const_mul, integral_id]
  ring

/-- Sciama's integral I(R) = 2 pi G rho R^2/c^2 -/
noncomputable def Isc (G ρ c R : ℝ) : ℝ := 2 * π * G * ρ * R ^ 2 / c ^ 2

/-- Hubble cutoff R_H = c/H with H^2 = 8 pi G rho/3: I = 3/4 (pi cancels) -/
theorem sciama_hubble {G ρ c H : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) (hH : 0 < H) (hF : H ^ 2 = 8 * π * G * ρ / 3) :
    Isc G ρ c (c / H) = 3 / 4 := by
  have hp := Real.pi_pos
  unfold Isc
  have hH0 : H ≠ 0 := hH.ne'
  have hc0 : c ≠ 0 := hc.ne'
  have : 2 * π * G * ρ * (c / H) ^ 2 / c ^ 2 = 2 * π * G * ρ / H ^ 2 := by field_simp
  rw [this, hF]
  field_simp; ring

theorem sciama_Rstar {G ρ c : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) :
    Isc G ρ c (c / Real.sqrt (G * ρ)) = 2 * π := by
  have hs := sqrt_pos' hG hρ
  have h2 := Real.sq_sqrt (show 0 ≤ G * ρ by positivity)
  unfold Isc
  have hc0 : c ≠ 0 := hc.ne'
  have : 2 * π * G * ρ * (c / Real.sqrt (G * ρ)) ^ 2 / c ^ 2 = 2 * π * (G * ρ) / Real.sqrt (G * ρ) ^ 2 := by
    field_simp
  rw [this, h2]; field_simp

theorem sciama_2Rstar {G ρ c : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) :
    Isc G ρ c (2 * (c / Real.sqrt (G * ρ))) = 8 * π := by
  have hs := sqrt_pos' hG hρ
  have h2 := Real.sq_sqrt (show 0 ≤ G * ρ by positivity)
  unfold Isc
  have hc0 : c ≠ 0 := hc.ne'
  have : 2 * π * G * ρ * (2 * (c / Real.sqrt (G * ρ))) ^ 2 / c ^ 2 = 8 * π * (G * ρ) / Real.sqrt (G * ρ) ^ 2 := by
    field_simp; ring
  rw [this, h2]; field_simp

/-- closure I = 1  <=>  R^2 = c^2/(2 pi G rho); then R_S^2/R_H^2 = 4/3, R_S^2 = R*^2/(2 pi), (2R*)^2/R_S^2 = 8 pi -/
theorem sciama_closure {G ρ c R : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) :
    Isc G ρ c R = 1 ↔ R ^ 2 = c ^ 2 / (2 * π * G * ρ) := by
  have hp := Real.pi_pos
  unfold Isc
  have hc0 : c ≠ 0 := hc.ne'
  rw [div_eq_one_iff_eq (by positivity), eq_div_iff (by positivity)]
  constructor <;> intro h <;> linarith

theorem closure_ratios {G ρ c H RS : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) (hH : 0 < H) (hF : H ^ 2 = 8 * π * G * ρ / 3)
    (hS : RS ^ 2 = c ^ 2 / (2 * π * G * ρ)) :
    RS ^ 2 / (c / H) ^ 2 = 4 / 3 ∧ RS ^ 2 / (c / Real.sqrt (G * ρ)) ^ 2 = 1 / (2 * π) ∧
    (2 * (c / Real.sqrt (G * ρ))) ^ 2 / RS ^ 2 = 8 * π := by
  have hp := Real.pi_pos
  have hs := sqrt_pos' hG hρ
  have h2 := Real.sq_sqrt (show 0 ≤ G * ρ by positivity)
  have hc0 : c ≠ 0 := hc.ne'
  have hH0 : H ≠ 0 := hH.ne'
  refine ⟨?_, ?_, ?_⟩
  · rw [hS]
    have : (c / H) ^ 2 = c ^ 2 / H ^ 2 := by rw [div_pow]
    rw [this, hF]; field_simp; ring
  · rw [hS, div_pow, h2]; field_simp
  · rw [hS, mul_pow, div_pow, h2]; field_simp; norm_num

/-- Rindler conversion a_c = c^2/R_c: a_c^2/(G rho c^2) = c^2/(R_c^2 G rho): R_H -> 8 pi/3, R_S -> 2 pi, R* -> 1, 2R* -> 1/4 -/
noncomputable def rindlerRatio (G ρ c R : ℝ) : ℝ := (c ^ 2 / R) ^ 2 / (G * ρ * c ^ 2)

theorem rindler_conversion {G ρ c H : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) (hH : 0 < H) (hF : H ^ 2 = 8 * π * G * ρ / 3) :
    rindlerRatio G ρ c (c / H) = 8 * π / 3 ∧
    (∀ RS : ℝ, 0 < RS → RS ^ 2 = c ^ 2 / (2 * π * G * ρ) → rindlerRatio G ρ c RS = 2 * π) ∧
    rindlerRatio G ρ c (c / Real.sqrt (G * ρ)) = 1 ∧
    rindlerRatio G ρ c (2 * (c / Real.sqrt (G * ρ))) = 1 / 4 := by
  have hp := Real.pi_pos
  have hs := sqrt_pos' hG hρ
  have h2 := Real.sq_sqrt (show 0 ≤ G * ρ by positivity)
  have hc0 : c ≠ 0 := hc.ne'
  have hH0 : H ≠ 0 := hH.ne'
  unfold rindlerRatio
  refine ⟨?_, ?_, ?_, ?_⟩
  · have : (c ^ 2 / (c / H)) ^ 2 / (G * ρ * c ^ 2) = c ^ 2 * H ^ 2 / (G * ρ * c ^ 2) := by field_simp
    rw [this, hF]; field_simp
  · intro RS hRS h
    have hRS0 : RS ≠ 0 := hRS.ne'
    have : (c ^ 2 / RS) ^ 2 / (G * ρ * c ^ 2) = c ^ 4 / (RS ^ 2 * (G * ρ * c ^ 2)) := by field_simp
    rw [this, h]; field_simp
  · have : (c ^ 2 / (c / Real.sqrt (G * ρ))) ^ 2 / (G * ρ * c ^ 2) = c ^ 2 * Real.sqrt (G * ρ) ^ 2 / (G * ρ * c ^ 2) := by
      field_simp
    rw [this, h2]; field_simp
  · have : (c ^ 2 / (2 * (c / Real.sqrt (G * ρ)))) ^ 2 / (G * ρ * c ^ 2) = c ^ 2 * Real.sqrt (G * ρ) ^ 2 / (4 * (G * ρ * c ^ 2)) := by
      field_simp; norm_num
    rw [this, h2]; field_simp

/-- with a coupling factor g (I -> g I) the closure at the Rindler cutoff R = c^2/a0 reads 2 pi g G rho c^2/a0^2 = 1, i.e. a0^2/(G rho c^2) = 2 pi g:
the puzzle value a0^2/(G rho c^2) = 1/4 needs g = 1/(8 pi) -/
theorem coupling_factor {g G ρ c a0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) (ha : 0 < a0) :
    g * Isc G ρ c (c ^ 2 / a0) = 1 ↔ a0 ^ 2 / (G * ρ * c ^ 2) = 2 * π * g := by
  have hp := Real.pi_pos
  have hc0 : c ≠ 0 := hc.ne'
  have ha0 : a0 ≠ 0 := ha.ne'
  unfold Isc
  have : g * (2 * π * G * ρ * (c ^ 2 / a0) ^ 2 / c ^ 2) = 2 * π * g * (G * ρ * c ^ 2) / a0 ^ 2 := by field_simp
  rw [this, div_eq_one_iff_eq (by positivity), div_eq_iff (by positivity)]
  constructor <;> intro h <;> nlinarith [h]

theorem coupling_puzzle {g : ℝ} : 2 * π * g = 1 / 4 ↔ g = 1 / (8 * π) := by
  have hp := Real.pi_pos
  rw [eq_div_iff (by norm_num : (4:ℝ) ≠ 0), eq_div_iff (by positivity : (8 * π) ≠ 0)]
  constructor <;> intro h <;> nlinarith [h]

/-- (5) the record's slope reading: mu(p) = 1 - (1 - p)^N has mu'(0) = N -/
theorem mu_p_deriv (N : ℝ) : HasDerivAt (fun p : ℝ => 1 - (1 - p) ^ N) N 0 := by
  have h1 : HasDerivAt (fun p : ℝ => 1 - p) (-1) 0 := by simpa using (hasDerivAt_id (0:ℝ)).const_sub 1
  have h2 := h1.rpow_const (p := N) (Or.inl (by norm_num))
  have h3 := h2.const_sub 1
  refine h3.congr_deriv ?_
  simp

/-- p(g) = (g/s)/(1 + g/s) has p'(0) = 1/s (unit response: p'(0) = 1 per channel in units of s) -/
theorem p_g_deriv {s : ℝ} (hs : 0 < s) : HasDerivAt (fun g : ℝ => (g / s) / (1 + g / s)) (1 / s) 0 := by
  have hs0 : s ≠ 0 := hs.ne'
  have h1 : HasDerivAt (fun g : ℝ => g / s) (1 / s) 0 := by simpa using (hasDerivAt_id (0:ℝ)).div_const s
  have h2 : HasDerivAt (fun g : ℝ => 1 + g / s) (1 / s) 0 := by simpa using h1.const_add 1
  have h3 := h1.div h2 (by simp)
  refine h3.congr_deriv ?_
  simp

/-- the composite mu(p(g)): slope N/s at g = 0.  The deep-Newtonian normalisation mu ~ g/a0 gives a0 = s/N -/
theorem mu_slope {s N : ℝ} (hs : 0 < s) : HasDerivAt (fun g : ℝ => 1 - (1 - (g / s) / (1 + g / s)) ^ N) (N / s) 0 := by
  have h1 := mu_p_deriv N
  have h2 := p_g_deriv hs
  have h3 : HasDerivAt ((fun p : ℝ => 1 - (1 - p) ^ N) ∘ (fun g : ℝ => (g / s) / (1 + g / s))) (N * (1 / s)) 0 := by
    have h1' : HasDerivAt (fun p : ℝ => 1 - (1 - p) ^ N) N ((fun g : ℝ => (g / s) / (1 + g / s)) 0) := by
      simpa using h1
    exact h1'.comp 0 h2
  refine h3.congr_deriv ?_
  ring

/-- a0 = 1/mu'(0) = s/N; with s = c sqrt(G rho): N = 2 <=> a0 = s/2 <=> kappa = 1/2 (for kappa := a0/s) -/
theorem N_two_iff {c G ρ N : ℝ} (hN : 0 < N) (hc : 0 < c) (hG : 0 < G) (hρ : 0 < ρ) :
    1 / (N / (c * Real.sqrt (G * ρ))) = a0of (1 / N) c G ρ ∧ (N = 2 ↔ 1 / N = 1 / 2) := by
  have hs := sqrt_pos' hG hρ
  constructor
  · unfold a0of; field_simp
  · constructor
    · intro h; rw [h]
    · intro h
      have := congrArg (fun t => 1 / t) h
      simpa using this

end RecordIff

#print axioms RecordIff.kappa_half_iff_M1
#print axioms RecordIff.kappa_iff_M1_unit
#print axioms RecordIff.enthalpy_family
#print axioms RecordIff.kappa_half_iff_w
#print axioms RecordIff.kappa_dim
#print axioms RecordIff.kernel_norm
#print axioms RecordIff.kernel_first_moment
#print axioms RecordIff.uniform_first_moment
#print axioms RecordIff.Rc_iff
#print axioms RecordIff.Rc_eq_two_Rstar_iff
#print axioms RecordIff.sciama_potential
#print axioms RecordIff.sciama_hubble
#print axioms RecordIff.sciama_Rstar
#print axioms RecordIff.sciama_2Rstar
#print axioms RecordIff.sciama_closure
#print axioms RecordIff.closure_ratios
#print axioms RecordIff.rindler_conversion
#print axioms RecordIff.coupling_factor
#print axioms RecordIff.mu_slope
#print axioms RecordIff.N_two_iff
