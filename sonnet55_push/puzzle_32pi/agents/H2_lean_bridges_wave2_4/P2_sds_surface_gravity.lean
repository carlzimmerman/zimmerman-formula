import Mathlib

open Real

/-!
# P2: Schwarzschild-de Sitter surface gravity (audit H2), in the f-normalisation and in the Bousso-Hawking normalisation

Conventions: G = c = 1.  f(r) = 1 - 2M/r - r^2/L^2 (M >= 0, L > 0), Lambda = 3/L^2, H = 1/L, x = r/L.
The "f-normalisation" of the Killing vector d/dt: surface gravity kappa = |f'(r_h)|/2 (the normalisation in which the pure de Sitter horizon has kappa = H).

CORRECTION OF THE BRIEF (proved here, `kappa_at_horizon`, `kappa_naive_off`): at a root of f the surface gravity is
    kappa_b = f'(r_b)/2 = (1 - Lambda r^2)/(2 r) = (1 - 3 r^2/L^2)/(2 r)          (black-hole horizon),
    kappa_c = -f'(r_c)/2 = (Lambda r^2 - 1)/(2 r) = (3 r^2/L^2 - 1)/(2 r)          (cosmological horizon),
NOT (1 - r^2/L^2)/(2 r): that is M/r^2 (the Newtonian term alone); the true kappa_b is smaller than it by exactly r/L^2.
Accordingly kappa_b = H/Z has the unique positive root  x = r/L = (sqrt(1 + 3 Z^2) - 1)/(3 Z)  (`kb_eq_iff`), not -1/Z + sqrt(1 + 1/Z^2)
(that would be the root of the naive formula (1 - x^2)/(2x) = 1/Z, `naive_root`); for Z^2 = 32 pi/3 it is x = 0.52263 (`xb_puzzle_bounds`),
the audit's r_b = 0.5226 L.  The cosmological root is x = (1 + sqrt(1 + 3 Z^2))/(3 Z) (`kc_eq_iff`).

CERTIFIED (premises => conclusions):
 (1) `f_deriv`, `kappa_at_horizon`, `kappa_Lambda_form`, `kappa_naive_off`.
 (2) `kb_eq_iff`, `kc_eq_iff`: unique positive roots; `xb_black_hole` (3 x_b^2 < 1 so f' > 0: the smaller root), `xc_cosmological`; `xc_lt_one_iff`: the
     cosmological root has positive mass iff Z > 1 (a0 < H).  `kb_strictAnti`, `kb_range`: kappa_b L runs strictly and continuously from +infinity (x -> 0) down to 0 at
     x = 1/sqrt 3 (Nariai): every kappa > 0 occurs exactly once.
 (3) `mass_le_nariai`, `mass_lt_nariai`: the mass M = L x (1 - x^2)/2 of the horizon at x is <= M_N = L/(3 sqrt 3) = L sqrt 3/9, with equality iff x = 1/sqrt 3; hence the horizon with kappa_b = a0 = H/Z exists
     at M* < M_N for EVERY Z > 0 (`a0_horizon_exists`), and for Z^2 = 32 pi/3 the ratio M*/M_N lies in (0.986, 0.988) (audit: 0.98695) (`puzzle_mass_ratio_bounds`).
 (4) `area_Lambda_at_a0_horizon`: at that horizon A_b Lambda = 12 pi x_b^2 < 4 pi < 32 pi^2 whatever Z is: the horizon carries the surface gravity a0 but does NOT satisfy the puzzle's
     area relation A Lambda = 32 pi^2 (audit a07 S3: 10.3); numerically 10.2 < A_b Lambda < 10.4 for the puzzle Z (`puzzle_area_Lambda_bounds`).
 (5) Bousso-Hawking normalisation (xi = d_t / sqrt(f(r*)), r* the radius where f' = 0, r*^3 = M L^2; f(r*) = 1 - 3 s^2, s = r*/L, s^3 = M/L; `rstar_props`):
     `bh_bound_b`: kappa_b^2 > 3 H^2 f(r*)  i.e. kappa_b^BH > sqrt 3 H (strict for every M < M_Nariai, the ratio tends to 3 at Nariai); `bh_bounds_c`: H^2 f(r*) < kappa_c^2 < 3 H^2 f(r*), i.e. H < kappa_c^BH < sqrt 3 H (strict; the two ends are M -> 0 and M -> M_Nariai).
     `bh_bound_b_dim`, `bh_bounds_c_dim`: the same two statements written directly on the metric function (M = s^3 L, f(r) = 0, kappa_b = f'(r)/2, kappa_c = -f'(r)/2, H = 1/L).
     Consequently no horizon of any SdS carries a0 = H/Z (Z > 1) in the BH normalisation (`no_a0_horizon_BH`), while one does in the f-normalisation (`a0_horizon_exists`).

NOT certified: that f(r) is the metric of SdS (input), that either normalisation is physical, that the a0-horizon has anything to do with MOND, kappa = 1/2.
-/

namespace SdS

noncomputable def f (M L r : ℝ) : ℝ := 1 - 2 * M / r - r ^ 2 / L ^ 2

theorem f_deriv {M L r : ℝ} (hr : r ≠ 0) : HasDerivAt (f M L) (2 * M / r ^ 2 - 2 * r / L ^ 2) r := by
  have h1 := (hasDerivAt_inv hr).const_mul (2 * M)
  have h2 := ((hasDerivAt_pow 2 r).div_const (L ^ 2))
  have h3 := (h1.const_sub 1).sub h2
  have hfun : f M L = fun x => 1 - 2 * M * x⁻¹ - x ^ 2 / L ^ 2 := by
    funext x; simp [f, div_eq_mul_inv]
  rw [hfun]
  refine h3.congr_deriv ?_
  field_simp
  ring

/-- (1) at a root of f: f'/2 = (1 - 3 r^2/L^2)/(2 r) (black hole) and -f'/2 = (3 r^2/L^2 - 1)/(2 r) (cosmological) -/
theorem kappa_at_horizon {M L r : ℝ} (hr : 0 < r) (hL : L ≠ 0) (hf : f M L r = 0) :
    (2 * M / r ^ 2 - 2 * r / L ^ 2) / 2 = (1 - 3 * r ^ 2 / L ^ 2) / (2 * r) ∧
    -((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2) = (3 * r ^ 2 / L ^ 2 - 1) / (2 * r) := by
  have hr0 : r ≠ 0 := hr.ne'
  unfold f at hf
  have hM : 2 * M = r * (1 - r ^ 2 / L ^ 2) := by
    field_simp at hf ⊢
    nlinarith [hf]
  have key : (2 * M / r ^ 2 - 2 * r / L ^ 2) / 2 = (1 - 3 * r ^ 2 / L ^ 2) / (2 * r) := by
    rw [hM]; field_simp; ring
  refine ⟨key, ?_⟩
  rw [key]; field_simp; ring

/-- Lambda = 3/L^2: kappa_b = (1 - Lambda r^2)/(2 r) -/
theorem kappa_Lambda_form {L r : ℝ} : (1 - (3 / L ^ 2) * r ^ 2) / (2 * r) = (1 - 3 * r ^ 2 / L ^ 2) / (2 * r) := by
  have : (3 / L ^ 2) * r ^ 2 = 3 * r ^ 2 / L ^ 2 := by ring
  rw [this]

/-- the naive formula (1 - r^2/L^2)/(2r) = M/r^2 exceeds the true kappa_b by exactly r/L^2 -/
theorem kappa_naive_off {L r : ℝ} (hr : r ≠ 0) :
    (1 - r ^ 2 / L ^ 2) / (2 * r) - (1 - 3 * r ^ 2 / L ^ 2) / (2 * r) = r / L ^ 2 := by
  field_simp; ring

/-! (2) roots.  Units L = 1: kb x = kappa_b L, kc x = kappa_c L at x = r/L. -/

noncomputable def kb (x : ℝ) : ℝ := (1 - 3 * x ^ 2) / (2 * x)
noncomputable def kc (x : ℝ) : ℝ := (3 * x ^ 2 - 1) / (2 * x)
noncomputable def xb (Z : ℝ) : ℝ := (Real.sqrt (1 + 3 * Z ^ 2) - 1) / (3 * Z)
noncomputable def xc (Z : ℝ) : ℝ := (1 + Real.sqrt (1 + 3 * Z ^ 2)) / (3 * Z)

/-- dimensionful: kappa_b = kb(x)/L at r = L x -/
theorem kb_dimensionful {L x : ℝ} (hL : 0 < L) (hx : 0 < x) :
    (1 - 3 * (L * x) ^ 2 / L ^ 2) / (2 * (L * x)) = kb x / L := by
  unfold kb; field_simp

theorem sqrt_facts {Z : ℝ} (hZ : 0 < Z) :
    0 < Real.sqrt (1 + 3 * Z ^ 2) ∧ Real.sqrt (1 + 3 * Z ^ 2) ^ 2 = 1 + 3 * Z ^ 2 ∧ 1 < Real.sqrt (1 + 3 * Z ^ 2) := by
  have h : 0 < 1 + 3 * Z ^ 2 := by positivity
  refine ⟨Real.sqrt_pos.mpr h, Real.sq_sqrt h.le, ?_⟩
  exact (Real.lt_sqrt (by norm_num)).mpr (by nlinarith [sq_pos_of_pos hZ])

/-- kappa_b = H/Z is the polynomial equation Z (1 - 3 x^2) = 2 x (x, Z > 0) -/
theorem kb_iff_poly {Z x : ℝ} (hZ : 0 < Z) (hx : 0 < x) : kb x = 1 / Z ↔ Z * (1 - 3 * x ^ 2) = 2 * x := by
  have hZ0 : Z ≠ 0 := hZ.ne'
  have hx0 : x ≠ 0 := hx.ne'
  unfold kb
  rw [div_eq_div_iff (by positivity) hZ0]
  constructor <;> intro h <;> linarith

theorem kc_iff_poly {Z x : ℝ} (hZ : 0 < Z) (hx : 0 < x) : kc x = 1 / Z ↔ Z * (3 * x ^ 2 - 1) = 2 * x := by
  have hZ0 : Z ≠ 0 := hZ.ne'
  have hx0 : x ≠ 0 := hx.ne'
  unfold kc
  rw [div_eq_div_iff (by positivity) hZ0]
  constructor <;> intro h <;> linarith

/-- kappa_b = H/Z  <=>  x = (sqrt(1 + 3 Z^2) - 1)/(3 Z): the unique positive root -/
theorem kb_eq_iff {Z x : ℝ} (hZ : 0 < Z) (hx : 0 < x) : kb x = 1 / Z ↔ x = xb Z := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  have hZ0 : Z ≠ 0 := hZ.ne'
  rw [kb_iff_poly hZ hx]
  unfold xb
  constructor
  · intro h1
    have h2 : (3 * Z * x + 1) ^ 2 = Real.sqrt (1 + 3 * Z ^ 2) ^ 2 := by rw [hs2]; nlinarith [h1]
    have h3 : 3 * Z * x + 1 = Real.sqrt (1 + 3 * Z ^ 2) := by
      have hpos : 0 < 3 * Z * x + 1 := by positivity
      nlinarith [sq_nonneg (3 * Z * x + 1 - Real.sqrt (1 + 3 * Z ^ 2)), sq_nonneg (3 * Z * x + 1 + Real.sqrt (1 + 3 * Z ^ 2))]
    field_simp; linarith
  · intro h
    have h3 : 3 * Z * x = Real.sqrt (1 + 3 * Z ^ 2) - 1 := by rw [h]; field_simp
    have h4 : 3 * Z * (Z * (1 - 3 * x ^ 2) - 2 * x) = 0 := by nlinarith [h3, hs2]
    rcases mul_eq_zero.mp h4 with h5 | h5
    · exfalso; have : 0 < 3 * Z := by positivity
      linarith
    · linarith

theorem kc_eq_iff {Z x : ℝ} (hZ : 0 < Z) (hx : 0 < x) : kc x = 1 / Z ↔ x = xc Z := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  have hZ0 : Z ≠ 0 := hZ.ne'
  rw [kc_iff_poly hZ hx]
  unfold xc
  constructor
  · intro h1
    have h2 : (3 * Z * x - 1) ^ 2 = Real.sqrt (1 + 3 * Z ^ 2) ^ 2 := by rw [hs2]; nlinarith [h1]
    have h3 : 3 * Z * x - 1 = Real.sqrt (1 + 3 * Z ^ 2) ∨ 3 * Z * x - 1 = -Real.sqrt (1 + 3 * Z ^ 2) :=
      sq_eq_sq_iff_eq_or_eq_neg.mp h2
    rcases h3 with h3 | h3
    · field_simp; linarith
    · exfalso
      have : 0 < 3 * Z * x := by positivity
      linarith
  · intro h
    have h3 : 3 * Z * x = 1 + Real.sqrt (1 + 3 * Z ^ 2) := by rw [h]; field_simp
    have h4 : 3 * Z * (Z * (3 * x ^ 2 - 1) - 2 * x) = 0 := by nlinarith [h3, hs2]
    rcases mul_eq_zero.mp h4 with h5 | h5
    · exfalso; have : 0 < 3 * Z := by positivity
      linarith
    · linarith

/-- the negative-root check of `kb_eq_iff`: 3 Z x^2 + 2 x - Z = 0 has the second root -(1 + s)/(3 Z) < 0 -/
theorem xb_black_hole {Z : ℝ} (hZ : 0 < Z) : 0 < xb Z ∧ 3 * xb Z ^ 2 < 1 := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  have hZ0 : Z ≠ 0 := hZ.ne'
  have hpos : 0 < xb Z := by unfold xb; apply div_pos <;> linarith
  refine ⟨hpos, ?_⟩
  have h := (kb_eq_iff hZ hpos).mpr rfl
  unfold kb at h
  have h1 : 0 < 1 / Z := by positivity
  rw [← h] at h1
  have : 0 < 1 - 3 * xb Z ^ 2 := by
    have h2 : 0 < 2 * xb Z := by positivity
    exact (div_pos_iff_of_pos_right h2).mp h1
  linarith

theorem xc_cosmological {Z : ℝ} (hZ : 0 < Z) : 0 < xc Z ∧ 1 < 3 * xc Z ^ 2 := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  have hpos : 0 < xc Z := by unfold xc; apply div_pos <;> linarith
  refine ⟨hpos, ?_⟩
  have h := (kc_eq_iff hZ hpos).mpr rfl
  unfold kc at h
  have h1 : 0 < 1 / Z := by positivity
  rw [← h] at h1
  have h2 : 0 < 2 * xc Z := by positivity
  have := (div_pos_iff_of_pos_right h2).mp h1
  linarith

/-- the cosmological root has x < 1 (positive mass) iff Z > 1 (a0 < H) -/
theorem xc_lt_one_iff {Z : ℝ} (hZ : 0 < Z) : xc Z < 1 ↔ 1 < Z := by
  obtain ⟨hs, hs2, hs1⟩ := sqrt_facts hZ
  have hZ0 : Z ≠ 0 := hZ.ne'
  unfold xc
  rw [div_lt_one (by positivity)]
  constructor
  · intro h
    have hlt : Real.sqrt (1 + 3 * Z ^ 2) < 3 * Z - 1 := by linarith
    have hsq : Real.sqrt (1 + 3 * Z ^ 2) ^ 2 < (3 * Z - 1) ^ 2 := by
      have h0 : 0 ≤ Real.sqrt (1 + 3 * Z ^ 2) := hs.le
      exact pow_lt_pow_left₀ hlt h0 (by norm_num)
    rw [hs2] at hsq
    nlinarith
  · intro h
    have : Real.sqrt (1 + 3 * Z ^ 2) < 3 * Z - 1 := by
      rw [Real.sqrt_lt' (by linarith)]
      nlinarith
    linarith


/-- the brief's root -1/Z + sqrt(1 + 1/Z^2) solves the NAIVE equation (1 - x^2)/(2x) = 1/Z ... -/
theorem naive_root_iff {Z x : ℝ} (hZ : 0 < Z) (hx : 0 < x) :
    (1 - x ^ 2) / (2 * x) = 1 / Z ↔ x = -1 / Z + Real.sqrt (1 + 1 / Z ^ 2) := by
  have hZ0 : Z ≠ 0 := hZ.ne'
  have hx0 : x ≠ 0 := hx.ne'
  have hq : 0 < 1 + 1 / Z ^ 2 := by positivity
  have hs2 := Real.sq_sqrt hq.le
  have hs0 := Real.sqrt_pos.mpr hq
  set t := Real.sqrt (1 + 1 / Z ^ 2)
  rw [div_eq_div_iff (by positivity) hZ0]
  constructor
  · intro h
    have h1 : x ^ 2 + 2 * x / Z - 1 = 0 := by
      field_simp; nlinarith [h]
    have h2 : (x + 1 / Z) ^ 2 = t ^ 2 := by rw [hs2]; field_simp; field_simp at h1; nlinarith [h1]
    have h3 : x + 1 / Z = t := by
      have hpos : 0 < x + 1 / Z := by positivity
      nlinarith [sq_nonneg (x + 1 / Z - t), sq_nonneg (x + 1 / Z + t)]
    have : x = t - 1 / Z := by linarith
    rw [this]; ring
  · intro h
    have h3 : x + 1 / Z = t := by rw [h]; ring
    have h2 : (x + 1 / Z) ^ 2 = 1 + 1 / Z ^ 2 := by rw [h3, hs2]
    field_simp at h2 ⊢
    nlinarith [h2]

/-- ... and at that root the TRUE kappa_b L = kb x equals 1/Z - x < 1/Z: the naive root does not carry the surface gravity H/Z -/
theorem kb_at_naive_root {x : ℝ} (hx : 0 < x) : kb x = (1 - x ^ 2) / (2 * x) - x := by
  unfold kb; field_simp; ring

/-- kb is strictly decreasing on (0, infinity): kappa_b runs from +infinity to 0 (at x = 1/sqrt 3, Nariai) and below -/
theorem kb_strictAnti : StrictAntiOn kb (Set.Ioi 0) := by
  intro x hx y hy hxy
  simp only [Set.mem_Ioi] at hx hy
  have h : kb x - kb y = (y - x) * (1 / (2 * x * y) + 3 / 2) := by
    unfold kb; field_simp; ring
  have : 0 < kb x - kb y := by rw [h]; have : 0 < y - x := by linarith
                               positivity
  linarith

theorem kb_blowup (K : ℝ) : ∃ x0 : ℝ, 0 < x0 ∧ ∀ x : ℝ, 0 < x → x < x0 → K < kb x := by
  refine ⟨min 1 (1 / (2 * |K| + 3)), by positivity, ?_⟩
  intro x hx hlt
  have h1 : x < 1 := lt_of_lt_of_le hlt (min_le_left _ _)
  have h2 : x < 1 / (2 * |K| + 3) := lt_of_lt_of_le hlt (min_le_right _ _)
  have hK : 0 ≤ |K| := abs_nonneg K
  have h3 : 2 * |K| + 3 < 1 / x := by
    rw [lt_div_iff₀ hx]
    rw [lt_div_iff₀ (by positivity)] at h2
    linarith
  have h4 : kb x = 1 / (2 * x) - 3 * x / 2 := by unfold kb; field_simp
  have h5 : 1 / (2 * x) = (1 / x) / 2 := by field_simp
  rw [h4, h5]
  have := le_abs_self K
  linarith

/-- every kappa > 0 is the black-hole surface gravity at exactly one r/L (f-normalisation) -/
theorem kb_range {κ : ℝ} (hκ : 0 < κ) : ∃! x : ℝ, 0 < x ∧ kb x = κ := by
  have hZ : 0 < 1 / κ := by positivity
  refine ⟨xb (1 / κ), ⟨(xb_black_hole hZ).1, ?_⟩, ?_⟩
  · have := (kb_eq_iff hZ (xb_black_hole hZ).1).mpr rfl
    rw [this]; field_simp
  · rintro y ⟨hy, hky⟩
    have : kb y = 1 / (1 / κ) := by rw [hky]; field_simp
    exact (kb_eq_iff hZ hy).mp this

/-! (3) the mass of the horizon -/

/-- mass in units of L of the SdS solution with a horizon at x = r/L:  M/L = x (1 - x^2)/2 -/
noncomputable def Mm (x : ℝ) : ℝ := x * (1 - x ^ 2) / 2
/-- the Nariai mass in units of L: 1/(3 sqrt 3) = sqrt 3/9 -/
noncomputable def MN : ℝ := Real.sqrt 3 / 9

theorem MN_eq : MN = 1 / (3 * Real.sqrt 3) := by
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h0 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  unfold MN; field_simp; nlinarith [h]

/-- the horizon condition: M = L Mm(x) makes f vanish at r = L x -/
theorem mass_makes_root {L x : ℝ} (hL : 0 < L) (hx : 0 < x) : f (L * Mm x) L (L * x) = 0 := by
  unfold f Mm; field_simp; ring

theorem mass_le_nariai {x : ℝ} (hx : 0 ≤ x) : Mm x ≤ MN := by
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h0 : 0 ≤ Real.sqrt 3 := Real.sqrt_nonneg 3
  unfold Mm MN
  have key : Real.sqrt 3 / 9 - x * (1 - x ^ 2) / 2 = (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by
    have : Real.sqrt 3 ^ 3 = 3 * Real.sqrt 3 := by nlinarith [h]
    nlinarith [h, this]
  have : 0 ≤ (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by positivity
  linarith

theorem mass_lt_nariai {x : ℝ} (hx : 0 < x) (hne : x ≠ Real.sqrt 3 / 3) : Mm x < MN := by
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h0 : 0 < Real.sqrt 3 := Real.sqrt_pos.mpr (by norm_num)
  unfold Mm MN
  have key : Real.sqrt 3 / 9 - x * (1 - x ^ 2) / 2 = (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by
    have : Real.sqrt 3 ^ 3 = 3 * Real.sqrt 3 := by nlinarith [h]
    nlinarith [h, this]
  have hne' : x - Real.sqrt 3 / 3 ≠ 0 := sub_ne_zero.mpr hne
  have : 0 < (x - Real.sqrt 3 / 3) ^ 2 * (x + 2 * (Real.sqrt 3 / 3)) / 2 := by positivity
  linarith

/-- kappa_b = 0 exactly at the Nariai radius x = 1/sqrt 3, and 3 x^2 < 1 <=> kappa_b > 0 -/
theorem kb_pos_iff {x : ℝ} (hx : 0 < x) : 0 < kb x ↔ 3 * x ^ 2 < 1 := by
  unfold kb
  rw [div_pos_iff_of_pos_right (by positivity)]
  constructor <;> intro h <;> linarith

theorem kb_nariai : kb (Real.sqrt 3 / 3) = 0 := by
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  unfold kb
  have : 3 * (Real.sqrt 3 / 3) ^ 2 = 1 := by nlinarith [h]
  rw [this]; simp

/-- for EVERY Z > 0 a black-hole horizon with kappa_b = H/Z exists (f-normalisation), at a mass 0 < M* < M_Nariai -/
theorem a0_horizon_exists {Z : ℝ} (hZ : 0 < Z) :
    ∃ x : ℝ, 0 < x ∧ 3 * x ^ 2 < 1 ∧ kb x = 1 / Z ∧ 0 < Mm x ∧ Mm x < MN := by
  obtain ⟨hx, hx3⟩ := xb_black_hole hZ
  refine ⟨xb Z, hx, hx3, (kb_eq_iff hZ hx).mpr rfl, ?_, ?_⟩
  · unfold Mm
    have : xb Z ^ 2 < 1 := by nlinarith
    have : 0 < 1 - xb Z ^ 2 := by linarith
    positivity
  · apply mass_lt_nariai hx
    intro h
    have h2 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
    have : 3 * xb Z ^ 2 = 1 := by rw [h]; nlinarith [h2]
    linarith

/-! (4) the area relation at the a0-horizon -/

theorem area_Lambda_at_a0_horizon {Z : ℝ} (hZ : 0 < Z) :
    (4 * π * xb Z ^ 2) * 3 = 12 * π * xb Z ^ 2 ∧ 12 * π * xb Z ^ 2 < 4 * π ∧ 4 * π < 32 * π ^ 2 ∧
    (4 * π * xb Z ^ 2) * 3 ≠ 32 * π ^ 2 := by
  have hp := Real.pi_pos
  obtain ⟨hx, hx3⟩ := xb_black_hole hZ
  have h1 : 12 * π * xb Z ^ 2 < 4 * π := by nlinarith
  have h2 : 4 * π < 32 * π ^ 2 := by nlinarith [Real.pi_gt_three]
  refine ⟨by ring, h1, h2, ?_⟩
  intro h; nlinarith

/-! numerics at the puzzle value Z^2 = 32 pi/3 -/

noncomputable def Zpuz : ℝ := Real.sqrt (32 * π / 3)

theorem Zpuz_bounds : 5.788 < Zpuz ∧ Zpuz < 5.789 := by
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  have hq : 0 ≤ 32 * π / 3 := by positivity
  unfold Zpuz
  constructor
  · rw [Real.lt_sqrt (by norm_num)]; nlinarith
  · rw [Real.sqrt_lt' (by norm_num)]; nlinarith

theorem Zpuz_sq : Zpuz ^ 2 = 32 * π / 3 := Real.sq_sqrt (by positivity)

theorem xb_puzzle_bounds : 0.5226 < xb Zpuz ∧ xb Zpuz < 0.5227 := by
  obtain ⟨hZl, hZu⟩ := Zpuz_bounds
  have hZ : 0 < Zpuz := by linarith
  obtain ⟨hx, hx3⟩ := xb_black_hole hZ
  have hpoly := (kb_iff_poly hZ hx).mp ((kb_eq_iff hZ hx).mpr rfl)
  set x := xb Zpuz with hxdef
  constructor
  · by_contra hcon
    have hcon := not_lt.mp hcon
    have h1 : 1 - 3 * (0.5226:ℝ) ^ 2 ≤ 1 - 3 * x ^ 2 := by nlinarith
    have h2 : Zpuz * (1 - 3 * (0.5226:ℝ) ^ 2) ≤ Zpuz * (1 - 3 * x ^ 2) := mul_le_mul_of_nonneg_left h1 hZ.le
    nlinarith
  · by_contra hcon
    have hcon := not_lt.mp hcon
    have h0 : 0 < 1 - 3 * x ^ 2 := by linarith
    have h1 : 1 - 3 * x ^ 2 ≤ 1 - 3 * (0.5227:ℝ) ^ 2 := by nlinarith
    have h2 : Zpuz * (1 - 3 * x ^ 2) ≤ 5.789 * (1 - 3 * (0.5227:ℝ) ^ 2) := by
      have : Zpuz * (1 - 3 * x ^ 2) ≤ Zpuz * (1 - 3 * (0.5227:ℝ) ^ 2) := mul_le_mul_of_nonneg_left h1 hZ.le
      have h3 : 0 < 1 - 3 * (0.5227:ℝ) ^ 2 := by norm_num
      nlinarith
    nlinarith

/-- audit a07/X3: the SdS mass at kappa_b = a0 is 0.98695 M_Nariai: certified 0.986 < M*/M_N < 0.988 -/
theorem puzzle_mass_ratio_bounds : 0.986 < Mm (xb Zpuz) / MN ∧ Mm (xb Zpuz) / MN < 0.988 := by
  obtain ⟨hxl, hxu⟩ := xb_puzzle_bounds
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h3l : 1.732 < Real.sqrt 3 := (Real.lt_sqrt (by norm_num)).mpr (by norm_num)
  have h3u : Real.sqrt 3 < 1.7321 := (Real.sqrt_lt' (by norm_num)).mpr (by norm_num)
  set x := xb Zpuz
  have hMN : 0 < MN := by unfold MN; positivity
  have hg1 : 0.3798 < x * (1 - x ^ 2) := by nlinarith [mul_pos (sub_pos.2 hxl) (sub_pos.2 hxu)]
  have hg2 : x * (1 - x ^ 2) < 0.3799 := by nlinarith [mul_pos (sub_pos.2 hxl) (sub_pos.2 hxu)]
  unfold Mm
  constructor
  · rw [lt_div_iff₀ hMN]; unfold MN; nlinarith
  · rw [div_lt_iff₀ hMN]; unfold MN; nlinarith

theorem puzzle_area_Lambda_bounds : 10.2 < 12 * π * xb Zpuz ^ 2 ∧ 12 * π * xb Zpuz ^ 2 < 10.4 := by
  obtain ⟨hxl, hxu⟩ := xb_puzzle_bounds
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  have hx2l : 0.27311 < xb Zpuz ^ 2 := by nlinarith
  have hx2u : xb Zpuz ^ 2 < 0.27322 := by nlinarith
  constructor <;> nlinarith

/-! (5) Bousso-Hawking normalisation.  Variables in units L = 1: x = r_h/L a root of f (x^3 - x + 2 s^3 = 0, s^3 = M/L, r* = s L). -/

/-- r* = s L with s^3 = M/L is the radius where f' = 0, and f(r*) = 1 - 3 s^2 -/
theorem rstar_props {M L s : ℝ} (hL : 0 < L) (hs : 0 < s) (hM : M = s ^ 3 * L) :
    (2 * M / (s * L) ^ 2 - 2 * (s * L) / L ^ 2 = 0) ∧ f M L (s * L) = 1 - 3 * s ^ 2 := by
  have hs0 : s ≠ 0 := hs.ne'
  have hL0 : L ≠ 0 := hL.ne'
  subst hM
  constructor
  · field_simp; ring
  · unfold f; field_simp; ring

/-- the horizon identity x (1 - 3 s^2) = (x - s)^2 (x + 2 s) on the root curve -/
theorem D_identity {x s : ℝ} (hc : x ^ 3 - x + 2 * s ^ 3 = 0) : x * (1 - 3 * s ^ 2) = (x - s) ^ 2 * (x + 2 * s) := by
  linear_combination (-1 : ℝ) * hc

/-- black-hole horizon: 3 x^2 < 1 forces x < s and f(r*) > 0 -/
theorem bh_x_lt_s {x s : ℝ} (hx : 0 < x) (hs : 0 < s) (hc : x ^ 3 - x + 2 * s ^ 3 = 0) (h3 : 3 * x ^ 2 < 1) :
    x < s ∧ 0 < 1 - 3 * s ^ 2 := by
  have h1 : x ^ 3 < s ^ 3 := by nlinarith [mul_pos hx (sub_pos.2 h3)]
  have hxs : x < s := lt_of_pow_lt_pow_left₀ 3 hs.le h1
  refine ⟨hxs, ?_⟩
  have hid := D_identity hc
  have : 0 < x * (1 - 3 * s ^ 2) := by
    rw [hid]; have : 0 < x - s ∨ x - s < 0 := by
      rcases lt_or_gt_of_ne (sub_ne_zero.mpr hxs.ne) with h | h
      · exact Or.inr h
      · exact Or.inl h
    have hsq : 0 < (x - s) ^ 2 := by nlinarith
    positivity
  exact (pos_iff_pos_of_mul_pos this).mp hx

/-- (5a) BH-normalised black-hole surface gravity: kappa_b^2 > 3 H^2 f(r*), i.e. (kb x)^2 > 3 (1 - 3 s^2) STRICTLY for every M < M_Nariai (the ratio tends to 3 at Nariai) -/
theorem bh_bound_b {x s : ℝ} (hx : 0 < x) (hs : 0 < s) (hc : x ^ 3 - x + 2 * s ^ 3 = 0) (h3 : 3 * x ^ 2 < 1) :
    3 * (1 - 3 * s ^ 2) < kb x ^ 2 := by
  obtain ⟨hxs, hD⟩ := bh_x_lt_s hx hs hc h3
  have hx0 : x ≠ 0 := hx.ne'
  have hsx : 0 < s - x := by linarith
  have hQ : 0 < (x ^ 2 + x * s + s ^ 2) ^ 2 - 3 * x ^ 3 * (x + 2 * s) := by
    have : (x ^ 2 + x * s + s ^ 2) ^ 2 - 3 * x ^ 3 * (x + 2 * s) = (s - x) * (s ^ 3 + 3 * s ^ 2 * x + 6 * s * x ^ 2 + 2 * x ^ 3) := by
      ring
    rw [this]
    positivity
  have hP : x ^ 2 * ((1 - 3 * x ^ 2) ^ 2 - 12 * x ^ 2 * (1 - 3 * s ^ 2))
      = 4 * (s - x) ^ 2 * ((x ^ 2 + x * s + s ^ 2) ^ 2 - 3 * x ^ 3 * (x + 2 * s)) := by
    linear_combination (-2 * s ^ 3 + 17 * x ^ 3 - x) * hc
  have hP0 : 0 < (1 - 3 * x ^ 2) ^ 2 - 12 * x ^ 2 * (1 - 3 * s ^ 2) := by
    have h4 : 0 < x ^ 2 * ((1 - 3 * x ^ 2) ^ 2 - 12 * x ^ 2 * (1 - 3 * s ^ 2)) := by rw [hP]; positivity
    exact (pos_iff_pos_of_mul_pos h4).mp (by positivity)
  unfold kb
  rw [div_pow, lt_div_iff₀ (by positivity)]
  nlinarith [hP0]

/-- (5b) BH-normalised cosmological surface gravity: H^2 f(r*) < kappa_c^2 < 3 H^2 f(r*) (strict; both ends are approached: M -> 0 and M -> M_Nariai) -/
theorem bh_bounds_c {y s : ℝ} (hy : 0 < y) (hs : 0 < s) (hc : y ^ 3 - y + 2 * s ^ 3 = 0) (h3 : 1 < 3 * y ^ 2) :
    (1 - 3 * s ^ 2) < kc y ^ 2 ∧ kc y ^ 2 < 3 * (1 - 3 * s ^ 2) ∧ 0 < 1 - 3 * s ^ 2 := by
  have hy0 : y ≠ 0 := hy.ne'
  have h1 : s ^ 3 < y ^ 3 := by nlinarith [mul_pos hy (sub_pos.2 h3)]
  have hsy : s < y := lt_of_pow_lt_pow_left₀ 3 hy.le h1
  have hid := D_identity hc
  have hD : 0 < 1 - 3 * s ^ 2 := by
    have hsq : 0 < (y - s) ^ 2 := by nlinarith
    have : 0 < y * (1 - 3 * s ^ 2) := by rw [hid]; positivity
    exact (pos_iff_pos_of_mul_pos this).mp hy
  refine ⟨?_, ?_, hD⟩
  · have hP : y ^ 2 * ((3 * y ^ 2 - 1) ^ 2 - 4 * y ^ 2 * (1 - 3 * s ^ 2))
        = 4 * (y - s) ^ 2 * (s ^ 2 * (s ^ 2 + 2 * s * y + 3 * y ^ 2)) := by
      linear_combination (-2 * s ^ 3 + 9 * y ^ 3 - y) * hc
    have hpos : 0 < (y - s) ^ 2 * (s ^ 2 * (s ^ 2 + 2 * s * y + 3 * y ^ 2)) := by
      have : 0 < y - s := by linarith
      positivity
    have h4 : 0 < y ^ 2 * ((3 * y ^ 2 - 1) ^ 2 - 4 * y ^ 2 * (1 - 3 * s ^ 2)) := by rw [hP]; nlinarith [hpos]
    have h5 : 0 < (3 * y ^ 2 - 1) ^ 2 - 4 * y ^ 2 * (1 - 3 * s ^ 2) := (pos_iff_pos_of_mul_pos h4).mp (by positivity)
    unfold kc
    rw [div_pow, lt_div_iff₀ (by positivity)]
    nlinarith [h5]
  · have hP : y ^ 2 * (12 * y ^ 2 * (1 - 3 * s ^ 2) - (3 * y ^ 2 - 1) ^ 2)
        = 4 * (y - s) ^ 2 * ((y - s) * (s ^ 3 + 3 * s ^ 2 * y + 6 * s * y ^ 2 + 2 * y ^ 3)) := by
      linear_combination (2 * s ^ 3 - 17 * y ^ 3 + y) * hc
    have hpos : 0 < (y - s) ^ 2 * ((y - s) * (s ^ 3 + 3 * s ^ 2 * y + 6 * s * y ^ 2 + 2 * y ^ 3)) := by
      have : 0 < y - s := by linarith
      positivity
    have h4 : 0 < y ^ 2 * (12 * y ^ 2 * (1 - 3 * s ^ 2) - (3 * y ^ 2 - 1) ^ 2) := by rw [hP]; nlinarith [hpos]
    have h5 : 0 < 12 * y ^ 2 * (1 - 3 * s ^ 2) - (3 * y ^ 2 - 1) ^ 2 := (pos_iff_pos_of_mul_pos h4).mp (by positivity)
    unfold kc
    rw [div_pow, div_lt_iff₀ (by positivity)]
    nlinarith [h5]

/-- (5c) In the BH normalisation kappa^2/f(r*) is >= 3 (black hole) or > 1 (cosmological), so it is never H^2/Z^2 for Z >= 1:
no SdS horizon carries a0 = H/Z (Z >= 1) there; in the f-normalisation one does (`a0_horizon_exists`). -/
theorem no_a0_horizon_BH {Z : ℝ} (hZ : 1 ≤ Z) :
    (∀ x s : ℝ, 0 < x → 0 < s → x ^ 3 - x + 2 * s ^ 3 = 0 → 3 * x ^ 2 < 1 → kb x ^ 2 / (1 - 3 * s ^ 2) ≠ 1 / Z ^ 2) ∧
    (∀ y s : ℝ, 0 < y → 0 < s → y ^ 3 - y + 2 * s ^ 3 = 0 → 1 < 3 * y ^ 2 → kc y ^ 2 / (1 - 3 * s ^ 2) ≠ 1 / Z ^ 2) := by
  have hZ0 : 0 < Z := by linarith
  have hZ2 : 1 / Z ^ 2 ≤ 1 := by
    rw [div_le_one (by positivity)]; nlinarith
  constructor
  · intro x s hx hs hc h3 h
    obtain ⟨_, hD⟩ := bh_x_lt_s hx hs hc h3
    have := bh_bound_b hx hs hc h3
    have h1 : 3 ≤ kb x ^ 2 / (1 - 3 * s ^ 2) := by rw [le_div_iff₀ hD]; linarith
    linarith
  · intro y s hy hs hc h3 h
    obtain ⟨h1, _, hD⟩ := bh_bounds_c hy hs hc h3
    have h2 : 1 < kc y ^ 2 / (1 - 3 * s ^ 2) := by rw [lt_div_iff₀ hD]; linarith
    linarith

/-- the sqrt form: kappa_b^BH = kappa_b/sqrt(f(r*)) > sqrt 3 (H = 1) -/
theorem bh_bound_b_sqrt {x s : ℝ} (hx : 0 < x) (hs : 0 < s) (hc : x ^ 3 - x + 2 * s ^ 3 = 0) (h3 : 3 * x ^ 2 < 1) :
    Real.sqrt 3 < kb x / Real.sqrt (1 - 3 * s ^ 2) := by
  obtain ⟨_, hD⟩ := bh_x_lt_s hx hs hc h3
  have hb := bh_bound_b hx hs hc h3
  have hkb : 0 < kb x := (kb_pos_iff hx).mpr h3
  have hsq : 0 < Real.sqrt (1 - 3 * s ^ 2) := Real.sqrt_pos.mpr hD
  rw [lt_div_iff₀ hsq, ← Real.sqrt_mul (by norm_num)]
  rw [Real.sqrt_lt' hkb]
  linarith

/-- (5d) the same bounds in DIMENSIONFUL form on the metric function itself: M = s^3 L (so r* = s L, f'(r*) = 0), r a black-hole root of f (f = 0, 3 r^2 < L^2):
    kappa_b^2 >= 3 H^2 f(r*) with kappa_b = f'(r)/2 and H = 1/L -/
theorem bh_bound_b_dim {M L r s : ℝ} (hL : 0 < L) (hr : 0 < r) (hs : 0 < s) (hM : M = s ^ 3 * L) (hf : f M L r = 0)
    (h3 : 3 * r ^ 2 < L ^ 2) :
    3 * (1 / L) ^ 2 * f M L (s * L) < ((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2) ^ 2 := by
  have hL0 : L ≠ 0 := hL.ne'
  have hr0 : r ≠ 0 := hr.ne'
  obtain ⟨_, hfs⟩ := rstar_props hL hs hM
  rw [hfs]
  have hk := (kappa_at_horizon hr hL0 hf).1
  rw [hk]
  set x := r / L with hx
  have hxpos : 0 < x := by positivity
  have hrx : r = L * x := by rw [hx]; field_simp
  have hx3 : 3 * x ^ 2 < 1 := by
    rw [hx, div_pow, ← mul_div_assoc, div_lt_one (by positivity)]; exact h3
  have hc : x ^ 3 - x + 2 * s ^ 3 = 0 := by
    unfold f at hf
    subst hM
    rw [hrx] at hf
    field_simp at hf
    have : L ^ 2 * (x ^ 3 - x + 2 * s ^ 3) = 0 := by nlinarith [hf]
    rcases mul_eq_zero.mp this with h | h
    · exact absurd h (pow_ne_zero 2 hL0)
    · exact h
  have hb := bh_bound_b hxpos hs hc hx3
  have hkb : (1 - 3 * r ^ 2 / L ^ 2) / (2 * r) = kb x / L := by
    rw [hrx]; exact kb_dimensionful hL hxpos
  rw [hkb]
  have hL2 : 0 < L ^ 2 := by positivity
  have e1 : 3 * (1 / L) ^ 2 * (1 - 3 * s ^ 2) = 3 * (1 - 3 * s ^ 2) / L ^ 2 := by field_simp
  have e3 : (kb x / L) ^ 2 = kb x ^ 2 / L ^ 2 := div_pow _ _ _
  rw [e1, e3]
  exact div_lt_div_of_pos_right hb hL2

/-- (5e) cosmological horizon, dimensionful: H^2 f(r*) < kappa_c^2 <= 3 H^2 f(r*), kappa_c = -f'(r)/2 (r a root of f with 3 r^2 > L^2) -/
theorem bh_bounds_c_dim {M L r s : ℝ} (hL : 0 < L) (hr : 0 < r) (hs : 0 < s) (hM : M = s ^ 3 * L) (hf : f M L r = 0)
    (h3 : L ^ 2 < 3 * r ^ 2) :
    (1 / L) ^ 2 * f M L (s * L) < (-((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2)) ^ 2 ∧
    (-((2 * M / r ^ 2 - 2 * r / L ^ 2) / 2)) ^ 2 < 3 * (1 / L) ^ 2 * f M L (s * L) := by
  have hL0 : L ≠ 0 := hL.ne'
  have hr0 : r ≠ 0 := hr.ne'
  obtain ⟨_, hfs⟩ := rstar_props hL hs hM
  rw [hfs]
  have hk := (kappa_at_horizon hr hL0 hf).2
  rw [hk]
  set x := r / L with hx
  have hxpos : 0 < x := by positivity
  have hrx : r = L * x := by rw [hx]; field_simp
  have hx3 : 1 < 3 * x ^ 2 := by
    rw [hx, div_pow, ← mul_div_assoc, one_lt_div (by positivity)]; exact h3
  have hc : x ^ 3 - x + 2 * s ^ 3 = 0 := by
    unfold f at hf
    subst hM
    rw [hrx] at hf
    field_simp at hf
    have : L ^ 2 * (x ^ 3 - x + 2 * s ^ 3) = 0 := by nlinarith [hf]
    rcases mul_eq_zero.mp this with h | h
    · exact absurd h (pow_ne_zero 2 hL0)
    · exact h
  obtain ⟨hb1, hb2, _⟩ := bh_bounds_c hxpos hs hc hx3
  have hkc : (3 * r ^ 2 / L ^ 2 - 1) / (2 * r) = kc x / L := by
    rw [hrx]; unfold kc; field_simp
  rw [hkc]
  have hL2 : 0 < L ^ 2 := by positivity
  have e1 : (1 / L) ^ 2 * (1 - 3 * s ^ 2) = (1 - 3 * s ^ 2) / L ^ 2 := by field_simp
  have e2 : 3 * (1 / L) ^ 2 * (1 - 3 * s ^ 2) = 3 * (1 - 3 * s ^ 2) / L ^ 2 := by field_simp
  have e3 : (kc x / L) ^ 2 = kc x ^ 2 / L ^ 2 := div_pow _ _ _
  rw [e1, e2, e3]
  exact ⟨div_lt_div_of_pos_right hb1 hL2, div_lt_div_of_pos_right hb2 hL2⟩

end SdS

#print axioms SdS.f_deriv
#print axioms SdS.kappa_at_horizon
#print axioms SdS.kappa_naive_off
#print axioms SdS.kb_eq_iff
#print axioms SdS.kc_eq_iff
#print axioms SdS.xc_lt_one_iff
#print axioms SdS.a0_horizon_exists
#print axioms SdS.area_Lambda_at_a0_horizon
#print axioms SdS.puzzle_mass_ratio_bounds
#print axioms SdS.bh_bound_b
#print axioms SdS.bh_bounds_c
#print axioms SdS.no_a0_horizon_BH
#print axioms SdS.bh_bound_b_dim
#print axioms SdS.bh_bounds_c_dim
