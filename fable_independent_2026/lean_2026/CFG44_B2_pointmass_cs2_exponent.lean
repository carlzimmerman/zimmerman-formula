import Mathlib

/-!
# MineM1-E: the required sound speed of the point-mass target and its mass exponent at fixed density (CFG44 B2, check E1)

Source lane: campaign_fresh_gravity/CFG44_fluid_target/B2_barotropic_nogo.py, docstring result "E1  point mass:  c_s^2 = sqrt(G M a0) (1 + x^2)^(3/2) / (x (1 + 2 x^2)) ...
  At FIXED rho it scales as M^e with e(x) = 1/2 - (1/2)[(1+x^2)/(1+2x^2)] dlnS/dlnx in [1/2, 1] ... a universal EOS needs e = 0" and the sympy block at lines 60-74
  (cs2_x, S_x, dlnS, dlnx_dlnM, e_x).  Ledger row 8 ("no barotropic EOS ... produces the target").  Overlap with the corpus: ChainCert/PointMass.lean certifies the sibling result E2
  (effective index Gamma = 2(1+x^2)/(1+2x^2)); a grep for cs2 / sound-speed / mass exponent in ChainCert finds nothing for E1.

CERTIFIED (premises => conclusions; mathematics of the stated target only):
* `sx_deriv`, `rhoc_deriv`: rho_c = a0/(4 pi G r sqrt(1+x^2)) has d rho_c/dr = -rho_c (2 s^2 - 1)/(r s^2), s = sqrt(1+x^2).
* `cs2_eq`, `cs2_scalefree`, `cs2_eq_Sfun`: c_s^2 := rho_c g_tot/|d rho_c/dr| = G M s^3/(r (2 s^2 - 1)) = sqrt(G M a0) (1+x^2)^(3/2)/(x (1+2 x^2)), x = r/sqrt(G M/a0)  (g_tot = G M s/r^2).
* `Sfun_deriv`: d ln S/d ln x = -(4x^2+1)/((1+x^2)(1+2x^2)).
* `rhoc_scalefree`: rho_c(x r_M) x sqrt(1+x^2) sqrt(M) = a0 sqrt(a0/G)/(4 pi G), so fixed density is the curve x sqrt(1+x^2) sqrt(M) = K.
* `fixed_rho_exponent`: along ANY differentiable curve X(M) of that form, d ln c_s^2/d ln M = e(X) = (2 X^4 + 4 X^2 + 1)/(2 X^2 + 1)^2  (implicit differentiation proved, not assumed).
* `eFun_bounds`, `eFun_zero`, `eFun_eq_one_iff`, `eFun_tendsto`, `no_universal_eos_exponent`, and the theorem `no_universal_eos` (if c_s^2 were the same function of rho for every M, i.e. constant along the fixed-density curve, contradiction): 1/2 < e(x) <= 1, e(0) = 1 (equality only at x = 0), e -> 1/2 as x -> infinity, so e never vanishes:
  no universal barotropic Pi(rho) reproduces the point-mass target (E1 for the point-mass family; the exclusion's hypotheses are those of the B2 docstring: static, spherical, weak-field, P = Pi(rho_c), g_felt = g_tot).

NOT certified: the EXISTENCE of a differentiable fixed-density curve X(M) (it follows from x sqrt(1+x^2) being an increasing bijection, but is not proved here: `fixed_rho_exponent` and
`no_universal_eos` are conditional on such a curve); that the target rho_c g_tot = a0 M_b/(4 pi r^3) is the right law (CFG44's declared target), extended baryon profiles, E3/E4 (extra-force families, sympy series), E5 (shape dependence), the numerical
M = 1e8..1e14 scans, or any relativistic statement.  Nothing here says a fluid closure exists or does not exist beyond the scoped B2 hypotheses.  kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open Filter Topology Real

namespace MineM1

/-- the target's cold density and total field for a point mass (CFG44 B1): x^2 = a0 r^2/(G M), s = sqrt(1+x^2) -/
noncomputable def sx (G a0 M r : ℝ) : ℝ := Real.sqrt (1 + a0 / (G * M) * r ^ 2)
noncomputable def rhoc (G a0 M r : ℝ) : ℝ := a0 / (4 * Real.pi * G * r * sx G a0 M r)
noncomputable def gtot (G a0 M r : ℝ) : ℝ := G * M * sx G a0 M r / r ^ 2

lemma sx_sq {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) (r : ℝ) :
    sx G a0 M r ^ 2 = 1 + a0 / (G * M) * r ^ 2 := by
  unfold sx; rw [Real.sq_sqrt]; positivity

lemma sx_pos {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) (r : ℝ) : 0 < sx G a0 M r := by
  unfold sx; apply Real.sqrt_pos.2; positivity

lemma sx_deriv {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) (r : ℝ) :
    HasDerivAt (sx G a0 M) (a0 / (G * M) * r / sx G a0 M r) r := by
  have h1 : HasDerivAt (fun r : ℝ => 1 + a0 / (G * M) * r ^ 2) (a0 / (G * M) * (2 * r)) r := by
    have := ((hasDerivAt_pow 2 r).const_mul (a0 / (G * M))).const_add 1
    simpa using this
  have h2 := h1.sqrt (by positivity)
  refine h2.congr_deriv ?_
  unfold sx
  field_simp

/-- d rho_c/dr = - rho_c (1 + 2x^2)/(r (1 + x^2)), written with s = sx: -rho_c (2 s^2 - 1)/(r s^2) -/
theorem rhoc_deriv {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    HasDerivAt (rhoc G a0 M) (-(rhoc G a0 M r) * (2 * sx G a0 M r ^ 2 - 1) / (r * sx G a0 M r ^ 2)) r := by
  have hs := sx_pos hG ha hM r
  have hsq := sx_sq hG ha hM r
  have hp := Real.pi_pos
  have hne : (4 * Real.pi * G * r) * sx G a0 M r ≠ 0 := mul_ne_zero (by positivity) hs.ne'
  have hd := (hasDerivAt_const r a0).div (((hasDerivAt_id r).const_mul (4 * Real.pi * G)).mul (sx_deriv hG ha hM r))
    (by simpa using hne)
  refine hd.congr_deriv ?_
  simp only [Pi.mul_apply, id]
  unfold rhoc
  have e : a0 / (G * M) * r ^ 2 = sx G a0 M r ^ 2 - 1 := by linarith
  have e2 : a0 * r ^ 2 = (sx G a0 M r ^ 2 - 1) * (G * M) := by
    field_simp at e; linarith
  field_simp
  nlinarith [e2]


/-- the required sound speed squared c_s^2 = rho g/|rho'| (the barotropic identity Pi'(rho) = c_s^2 of CFG44 B2) -/
noncomputable def cs2 (G a0 M r : ℝ) : ℝ := rhoc G a0 M r * gtot G a0 M r / (-(deriv (rhoc G a0 M) r))

theorem cs2_eq {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    cs2 G a0 M r = G * M * sx G a0 M r ^ 3 / (r * (2 * sx G a0 M r ^ 2 - 1)) := by
  have hs := sx_pos hG ha hM r
  have hsq := sx_sq hG ha hM r
  have h1 : 1 ≤ sx G a0 M r ^ 2 := by
    rw [hsq]; have : 0 ≤ a0 / (G * M) * r ^ 2 := by positivity
    linarith
  have hpos : 0 < 2 * sx G a0 M r ^ 2 - 1 := by linarith
  have hp := Real.pi_pos
  unfold cs2
  rw [(rhoc_deriv hG ha hM hr).deriv]
  unfold gtot rhoc
  field_simp

/-- in the scale-free variable x = r/r_M, r_M = sqrt(G M/a0): c_s^2 = sqrt(G M a0) (1+x^2)^(3/2)/(x (1+2x^2)) -/
theorem cs2_scalefree {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    cs2 G a0 M r = Real.sqrt (G * M * a0) *
      ((1 + (r / Real.sqrt (G * M / a0)) ^ 2) * Real.sqrt (1 + (r / Real.sqrt (G * M / a0)) ^ 2)
        / ((r / Real.sqrt (G * M / a0)) * (1 + 2 * (r / Real.sqrt (G * M / a0)) ^ 2))) := by
  rw [cs2_eq hG ha hM hr]
  set rM := Real.sqrt (G * M / a0) with hrM
  have hrMpos : 0 < rM := Real.sqrt_pos.2 (by positivity)
  have hrM2 : rM ^ 2 = G * M / a0 := Real.sq_sqrt (by positivity)
  have hx2 : (r / rM) ^ 2 = a0 / (G * M) * r ^ 2 := by
    rw [div_pow, hrM2]; field_simp
  have hsxx : sx G a0 M r = Real.sqrt (1 + (r / rM) ^ 2) := by
    unfold sx; rw [hx2]
  have hq : Real.sqrt (G * M * a0) = G * M / rM := by
    rw [hrM]
    have : G * M * a0 = (G * M) ^ 2 / (G * M / a0) := by field_simp
    rw [this, Real.sqrt_div (by positivity), Real.sqrt_sq (by positivity)]
  rw [hq, hsxx]
  have hw := Real.sq_sqrt (show (0:ℝ) ≤ 1 + (r / rM) ^ 2 by positivity)
  have hw3 : Real.sqrt (1 + (r / rM) ^ 2) ^ 3 = (1 + (r / rM) ^ 2) * Real.sqrt (1 + (r / rM) ^ 2) := by
    rw [pow_succ, hw]
  rw [hw3, hw]
  have hx : r / rM ≠ 0 := by positivity
  have h12 : 1 + 2 * (r / rM) ^ 2 ≠ 0 := by positivity
  have h13 : rM ^ 2 + 2 * r ^ 2 ≠ 0 := by positivity
  field_simp
  ring_nf
  field_simp


/-- rho_c in the scale-free variable: rho_c(x r_M) * (x sqrt(1+x^2) sqrt(M)) = a0 sqrt(a0/G)/(4 pi G): fixed density <=> x sqrt(1+x^2) sqrt(M) = const -/
theorem rhoc_scalefree {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {x : ℝ} (hx : 0 < x) :
    rhoc G a0 M (x * Real.sqrt (G * M / a0)) * (x * Real.sqrt (1 + x ^ 2) * Real.sqrt M)
      = a0 * Real.sqrt (a0 / G) / (4 * Real.pi * G) := by
  have hp := Real.pi_pos
  set rM := Real.sqrt (G * M / a0) with hrM
  have hrMpos : 0 < rM := Real.sqrt_pos.2 (by positivity)
  have hrM2 : rM ^ 2 = G * M / a0 := Real.sq_sqrt (by positivity)
  have hsx : sx G a0 M (x * rM) = Real.sqrt (1 + x ^ 2) := by
    unfold sx; congr 1
    rw [mul_pow, hrM2]; field_simp
  have hs : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.2 (by positivity)
  have hq : Real.sqrt M / rM = Real.sqrt (a0 / G) := by
    rw [hrM, ← Real.sqrt_div hM.le]
    congr 1; field_simp
  unfold rhoc
  rw [hsx]
  have : a0 / (4 * Real.pi * G * (x * rM) * Real.sqrt (1 + x ^ 2)) * (x * Real.sqrt (1 + x ^ 2) * Real.sqrt M)
      = a0 / (4 * Real.pi * G) * (Real.sqrt M / rM) := by
    field_simp
  rw [this, hq]; ring


/-- S(x) = (1+x^2)^(3/2)/(x (1+2x^2)), c_s^2 = sqrt(G M a0) S(x) -/
noncomputable def Sfun (x : ℝ) : ℝ := (1 + x ^ 2) * Real.sqrt (1 + x ^ 2) / (x * (1 + 2 * x ^ 2))

/-- exponent of c_s^2 in M at fixed density -/
noncomputable def eFun (x : ℝ) : ℝ := (2 * x ^ 4 + 4 * x ^ 2 + 1) / (2 * x ^ 2 + 1) ^ 2

lemma sqrt1_deriv (x : ℝ) : HasDerivAt (fun y : ℝ => Real.sqrt (1 + y ^ 2)) (x / Real.sqrt (1 + x ^ 2)) x := by
  have h1 : HasDerivAt (fun y : ℝ => 1 + y ^ 2) (2 * x) x := by
    simpa using ((hasDerivAt_pow 2 x).const_add 1)
  have := h1.sqrt (by positivity)
  refine this.congr_deriv ?_
  have hs : Real.sqrt (1 + x ^ 2) ≠ 0 := (Real.sqrt_pos.2 (by positivity)).ne'
  field_simp

theorem Sfun_deriv {x : ℝ} (hx : 0 < x) :
    HasDerivAt Sfun (Sfun x * (-(4 * x ^ 2 + 1) / (x * (1 + x ^ 2) * (1 + 2 * x ^ 2)))) x := by
  have hw := sqrt1_deriv x
  have hs : Real.sqrt (1 + x ^ 2) ≠ 0 := (Real.sqrt_pos.2 (by positivity)).ne'
  have hw2 := Real.sq_sqrt (show (0:ℝ) ≤ 1 + x ^ 2 by positivity)
  have hn : HasDerivAt (fun y : ℝ => (1 + y ^ 2) * Real.sqrt (1 + y ^ 2))
      (2 * x * Real.sqrt (1 + x ^ 2) + (1 + x ^ 2) * (x / Real.sqrt (1 + x ^ 2))) x := by
    have h1 : HasDerivAt (fun y : ℝ => 1 + y ^ 2) (2 * x) x := by
      simpa using ((hasDerivAt_pow 2 x).const_add 1)
    exact h1.mul hw
  have hd : HasDerivAt (fun y : ℝ => y * (1 + 2 * y ^ 2)) (1 * (1 + 2 * x ^ 2) + x * (2 * (2 * x))) x := by
    have h1 : HasDerivAt (fun y : ℝ => 1 + 2 * y ^ 2) (2 * (2 * x)) x := by
      simpa using (((hasDerivAt_pow 2 x).const_mul 2).const_add 1)
    exact (hasDerivAt_id x).mul h1
  have := hn.div hd (by positivity)
  refine this.congr_deriv ?_
  unfold Sfun
  have hx0 : x ≠ 0 := hx.ne'
  field_simp
  set w := Real.sqrt (1 + x ^ 2)
  have hw' : w ^ 2 = 1 + x ^ 2 := hw2
  ring_nf
  simp only [hw']
  ring


/-- e(x) = 1 - 2 x^4/(2x^2+1)^2 = 1/2 + (4x^2+1)/(2 (2x^2+1)^2): e(0) = 1, e > 1/2, e <= 1 with equality iff x = 0, e -> 1/2 -/
theorem eFun_zero : eFun 0 = 1 := by unfold eFun; norm_num

theorem eFun_bounds (x : ℝ) : 1 / 2 < eFun x ∧ eFun x ≤ 1 := by
  unfold eFun
  have hd : 0 < (2 * x ^ 2 + 1) ^ 2 := by positivity
  constructor
  · rw [lt_div_iff₀ hd]; nlinarith [sq_nonneg x, sq_nonneg (x ^ 2)]
  · rw [div_le_one hd]; nlinarith [sq_nonneg x, sq_nonneg (x ^ 2)]

theorem eFun_eq_one_iff (x : ℝ) : eFun x = 1 ↔ x = 0 := by
  unfold eFun
  have hd : 0 < (2 * x ^ 2 + 1) ^ 2 := by positivity
  rw [div_eq_one_iff_eq hd.ne']
  constructor
  · intro h
    have : x ^ 4 = 0 := by nlinarith
    exact pow_eq_zero_iff (by norm_num) |>.1 this
  · rintro rfl; norm_num

theorem eFun_tendsto : Tendsto eFun atTop (𝓝 (1 / 2)) := by
  have h1 : Tendsto (fun x : ℝ => 2 / (2 * x ^ 2 + 1)) atTop (𝓝 0) := by
    have : Tendsto (fun x : ℝ => 2 * x ^ 2 + 1) atTop atTop :=
      tendsto_atTop_add_const_right _ _ ((tendsto_pow_atTop (by norm_num : (2:ℕ) ≠ 0)).const_mul_atTop (by norm_num))
    exact this.const_div_atTop 2 |> fun h => by simpa using h
  have hlow : ∀ x : ℝ, 1 / 2 ≤ eFun x := fun x => (eFun_bounds x).1.le
  have hup : ∀ x : ℝ, eFun x ≤ 1 / 2 + 2 / (2 * x ^ 2 + 1) := by
    intro x
    unfold eFun
    have hd : 0 < (2 * x ^ 2 + 1) := by positivity
    rw [div_add_div _ _ (by norm_num) hd.ne', div_le_div_iff₀ (by positivity) (by positivity)]
    nlinarith [sq_nonneg x, sq_nonneg (x ^ 2), pow_pos hd 3, mul_pos hd hd]
  have h2 : Tendsto (fun x : ℝ => 1 / 2 + 2 / (2 * x ^ 2 + 1)) atTop (𝓝 (1 / 2)) := by
    have := h1.const_add (1 / 2)
    rwa [add_zero] at this
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds h2 hlow hup


lemma alg2 {X' r s w : ℝ} (hs : 0 < s) (hw : 0 < w) (hw2 : w ^ 2 = 1 + r ^ 2)
    (E : (X' * w + r * ((r / w) * X')) * s + r * w * (1 / (2 * s)) = 0) :
    s * s * X' = -(r * (1 + r ^ 2)) / (2 * (1 + 2 * r ^ 2)) := by
  have hd : 0 < 1 + 2 * r ^ 2 := by positivity
  field_simp at E ⊢
  rw [hw2] at E
  linear_combination E

lemma alg3 {A S0 r s X' : ℝ} (hs : 0 < s) (hr : 0 < r)
    (hMX : s * s * X' = -(r * (1 + r ^ 2)) / (2 * (1 + 2 * r ^ 2))) :
    s * s * (A * (1 / (2 * s)) * S0 + A * s * (S0 * (-(4 * r ^ 2 + 1) / (r * (1 + r ^ 2) * (1 + 2 * r ^ 2))) * X'))
      = eFun r * (A * s * S0) := by
  have hss : s * s ≠ 0 := by positivity
  have hX' : X' = -(r * (1 + r ^ 2)) / (2 * (1 + 2 * r ^ 2)) / (s * s) := by
    field_simp at hMX ⊢; linarith
  subst hX'
  unfold eFun
  have hr1 : 1 + r ^ 2 ≠ 0 := by positivity
  have hr2 : 1 + 2 * r ^ 2 ≠ 0 := by positivity
  have hr3 : 2 * r ^ 2 + 1 ≠ 0 := by positivity
  field_simp
  ring

/-- FIXED-DENSITY EXPONENT (CFG44 B2, E1): along the curve X(M) of constant rho_c (x sqrt(1+x^2) sqrt(M) = K),
    d ln c_s^2 / d ln M = e(x) = (2x^4 + 4x^2 + 1)/(2x^2 + 1)^2  (c_s^2 = sqrt(G a0) sqrt(M) S(x)). -/
theorem fixed_rho_exponent {G a0 K : ℝ} {X : ℝ → ℝ} {X' M0 : ℝ}
    (hM0 : 0 < M0) (hX : HasDerivAt X X' M0) (hpos : ∀ M, 0 < M → 0 < X M)
    (hK : ∀ M, 0 < M → X M * Real.sqrt (1 + X M ^ 2) * Real.sqrt M = K) :
    ∃ c' : ℝ, HasDerivAt (fun M => Real.sqrt (G * a0) * Real.sqrt M * Sfun (X M)) c' M0 ∧
      M0 * c' = eFun (X M0) * (Real.sqrt (G * a0) * Real.sqrt M0 * Sfun (X M0)) := by
  set s := Real.sqrt M0 with hsdef
  have hs : 0 < s := Real.sqrt_pos.2 hM0
  have hss : s * s = M0 := Real.mul_self_sqrt hM0.le
  set r := X M0 with hrdef
  have hr : 0 < r := hpos M0 hM0
  set w := Real.sqrt (1 + r ^ 2) with hwdef
  have hw : 0 < w := Real.sqrt_pos.2 (by positivity)
  have hw2 : w ^ 2 = 1 + r ^ 2 := Real.sq_sqrt (by positivity)
  -- derivatives of the pieces
  have dW : HasDerivAt (fun M => Real.sqrt (1 + X M ^ 2)) (r / w * X') M0 :=
    (sqrt1_deriv r).comp M0 hX
  have dS : HasDerivAt (fun M => Real.sqrt M) (1 / (2 * s)) M0 := by
    have := Real.hasDerivAt_sqrt hM0.ne'
    simpa [hsdef] using this
  have dq : HasDerivAt (fun M => X M * Real.sqrt (1 + X M ^ 2) * Real.sqrt M)
      ((X' * w + r * (r / w * X')) * s + r * w * (1 / (2 * s))) M0 :=
    (hX.mul dW).mul dS
  have dq0 : HasDerivAt (fun M => X M * Real.sqrt (1 + X M ^ 2) * Real.sqrt M) 0 M0 := by
    refine (hasDerivAt_const M0 K).congr_of_eventuallyEq ?_
    filter_upwards [lt_mem_nhds hM0] with M hM using hK M hM
  have E := dq.unique dq0
  have hMX := alg2 hs hw hw2 E
  -- c_s^2 derivative
  have dSf : HasDerivAt (fun M => Sfun (X M)) (Sfun r * (-(4 * r ^ 2 + 1) / (r * (1 + r ^ 2) * (1 + 2 * r ^ 2))) * X') M0 :=
    (Sfun_deriv hr).comp M0 hX
  have dc : HasDerivAt (fun M => Real.sqrt (G * a0) * Real.sqrt M * Sfun (X M))
      (Real.sqrt (G * a0) * (1 / (2 * s)) * Sfun r + Real.sqrt (G * a0) * s *
        (Sfun r * (-(4 * r ^ 2 + 1) / (r * (1 + r ^ 2) * (1 + 2 * r ^ 2))) * X')) M0 := by
    have := ((hasDerivAt_const M0 (Real.sqrt (G * a0))).mul dS).mul dSf
    refine this.congr_deriv ?_
    simp only [Pi.mul_apply, zero_mul, zero_add]
    rfl
  refine ⟨_, dc, ?_⟩
  rw [← hss]
  exact alg3 hs hr hMX


/-- c_s^2 of the target = sqrt(G M a0) S(x) with x = r/r_M -/
theorem cs2_eq_Sfun {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    cs2 G a0 M r = Real.sqrt (G * M * a0) * Sfun (r / Real.sqrt (G * M / a0)) := by
  rw [cs2_scalefree hG ha hM hr]; rfl

/-- a UNIVERSAL barotropic EOS Pi(rho) would need c_s^2 independent of M at fixed rho, i.e. exponent 0; the target has exponent e(x) in (1/2, 1] -/
theorem no_universal_eos_exponent (x : ℝ) : eFun x ≠ 0 := by
  have := (eFun_bounds x).1
  intro h; rw [h] at this; norm_num at this

lemma Sfun_pos {x : ℝ} (hx : 0 < x) : 0 < Sfun x := by
  unfold Sfun
  have : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.2 (by positivity)
  positivity

/-- NO UNIVERSAL BAROTROPIC EOS for the point-mass family: if a single function Pi'(rho) supplied c_s^2 for every M, then along the constant-density curve
    c_s^2(M, X(M)) would be constant; but its log-derivative is e(X) > 1/2 > 0. -/
theorem no_universal_eos {G a0 K C0 : ℝ} (hG : 0 < G) (ha : 0 < a0) {X : ℝ → ℝ} {X' M0 : ℝ}
    (hM0 : 0 < M0) (hX : HasDerivAt X X' M0) (hpos : ∀ M, 0 < M → 0 < X M)
    (hK : ∀ M, 0 < M → X M * Real.sqrt (1 + X M ^ 2) * Real.sqrt M = K)
    (hc : ∀ M, 0 < M → Real.sqrt (G * a0) * Real.sqrt M * Sfun (X M) = C0) : False := by
  obtain ⟨c', hd, hc'⟩ := fixed_rho_exponent (G := G) (a0 := a0) hM0 hX hpos hK
  have hd0 : HasDerivAt (fun M => Real.sqrt (G * a0) * Real.sqrt M * Sfun (X M)) 0 M0 := by
    refine (hasDerivAt_const M0 C0).congr_of_eventuallyEq ?_
    filter_upwards [lt_mem_nhds hM0] with M hM using hc M hM
  have h0 : c' = 0 := hd.unique hd0
  rw [h0, mul_zero] at hc'
  have h1 : 0 < Real.sqrt (G * a0) := Real.sqrt_pos.2 (by positivity)
  have h2 : 0 < Real.sqrt M0 := Real.sqrt_pos.2 hM0
  have h3 : 0 < Sfun (X M0) := Sfun_pos (hpos M0 hM0)
  have h4 : 1 / 2 < eFun (X M0) := (eFun_bounds _).1
  have : 0 < eFun (X M0) * (Real.sqrt (G * a0) * Real.sqrt M0 * Sfun (X M0)) := by
    apply mul_pos (by linarith) (by positivity)
  linarith

end MineM1

open MineM1 in
#print axioms rhoc_deriv
open MineM1 in
#print axioms cs2_eq
open MineM1 in
#print axioms cs2_eq_Sfun
open MineM1 in
#print axioms Sfun_deriv
open MineM1 in
#print axioms rhoc_scalefree
open MineM1 in
#print axioms fixed_rho_exponent
open MineM1 in
#print axioms eFun_bounds
open MineM1 in
#print axioms eFun_tendsto
open MineM1 in
#print axioms no_universal_eos_exponent
open MineM1 in
#print axioms no_universal_eos
