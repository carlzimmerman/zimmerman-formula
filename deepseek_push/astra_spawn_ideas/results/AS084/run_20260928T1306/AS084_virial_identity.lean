import Mathlib
import Mathlib.Tactic

/-!
# AS084 -- Self-gravitational virial energy with a central mass (Lean 4 certificate)

Seed math (executed as on disk):
    W_vir,total = -∫_{r_in}^{R} G M(r)/r dM_shell(r),   M(r) = M_in + m_s (r - r_in),
    dM_shell(r) = m_s dr  (rho = A/r^2, A = C/(4 pi G), m_s = 4 pi A = C/G).

Certified statements (all on r_in > 0, R > r_in, i.e. the finite-shell domain):

  T1 `virial_integral_closed`   the defining integral equals the closed form
                                G m_s M_in ln(R/r_in) + G m_s^2 (R - r_in)
                                - G m_s^2 r_in ln(R/r_in)   (FTC + log algebra)
  T2 `separation_of_terms`      the closed form is exactly W_cent + W_self with
                                W_cent = -G m_s M_in ln(R/r_in)  (central mass)
                                W_self = -G m_s^2 (R - r_in - r_in ln(R/r_in))
                                (shell self-gravity); the pair self-energy and
                                the virial of the external central potential are
                                separate terms, never conflated.
  T3 `virial_value`             -(integral) = W_cent + W_self (the physical sign)
  T4 `naive_error_exact`        exact deviation of the naive replacement
                                -G M(R)^2/R from the true virial, for ANY M_in
  T5 `naive_overbinds`          NEGATIVE CONTROL (M_in = 0): on every finite
                                shell (r_in > 0) the naive -G M(R)^2/R is
                                strictly MORE negative than the true virial:
                                naive - exact < 0.  The control is capable of
                                failing; it fails (correctly rejects) everywhere.
  T6 `wself_singular_limit`     wself(r_in) -> -G m_s^2 R as r_in -> 0^+ (the
                                singular-sphere recovery -G M(R)^2/R with
                                M(R) = m_s R; terms that die with r_in -> 0^+
                                are the finite-shell corrections).

Deviations are exact: T1 is the full closed form, T4/T5 the full error structure.
No computational evidence is fabricated: the numeric residual checks live in the
run's compute script and residuals.json.

Framework inputs not re-derived here (adopted as declared): a0 = kappa c sqrt(G
rho_Lambda) with kappa = 1/2;  C = sqrt(G M_b a0);  A = C/(4 pi G).
-/

noncomputable section
open Real
open scoped Topology Interval
set_option linter.unnecessarySimpa false

/-- W_cent: the virial of the central mass M_in acting on the shell continuum
   (attraction term of the external point-mass potential). -/
def Wcent (G m_s M_in r_in R : ℝ) : ℝ :=
  -(G * m_s * M_in * Real.log (R / r_in))

/-- W_self: the shell-continuum self-gravity virial
   (-∫ G m_s (r - r_in)/r dM on [r_in, R], closed form). -/
def Wself (G m_s r_in R : ℝ) : ℝ :=
  -(G * m_s ^ 2 * (R - r_in - r_in * Real.log (R / r_in)))

/-- W_tot (closed form) = W_cent + W_self. -/
def Wtot (G m_s M_in r_in R : ℝ) : ℝ := Wcent G m_s M_in r_in R + Wself G m_s r_in R

/-- The naive 'all enclosed mass at R' replacement: -G M(R)^2 / R. -/
def Wnaive (G m_s M_in r_in R : ℝ) : ℝ := -G * (M_in + m_s * (R - r_in)) ^ 2 / R

/-- Positivity helper on the closed interval [r_in, R] (r_in < R). -/
lemma pos_of_mem_Icc {r_in R x : ℝ} (hr0 : 0 < r_in) (_hrR : r_in < R)
    (hx : x ∈ Set.Icc r_in R) : 0 < x := by
  exact lt_of_lt_of_le hr0 hx.1

/-- Positivity helper on the open interval (r_in, R). -/
lemma pos_of_mem_Ioo {r_in R x : ℝ} (hr0 : 0 < r_in) (_hrR : r_in < R)
    (hx : x ∈ Set.Ioo r_in R) : 0 < x := by
  exact lt_of_lt_of_le hr0 (le_of_lt hx.1)

/-- T1: the defining virial integral equals the closed form (FTC, exact). -/
theorem virial_integral_closed (G m_s M_in r_in R : ℝ) (hr0 : 0 < r_in) (hrR : r_in < R) :
    (∫ r in r_in..R, G * m_s * (M_in + m_s * (r - r_in)) / r)
      = G * m_s * M_in * Real.log (R / r_in)
        + G * m_s ^ 2 * (R - r_in)
        - G * m_s ^ 2 * r_in * Real.log (R / r_in) := by
  let F : ℝ → ℝ := fun r => G * m_s * (M_in * Real.log r + m_s * r - m_s * r_in * Real.log r)
  let fP : ℝ → ℝ := fun r => G * m_s * (M_in + m_s * (r - r_in)) / r
  have hRpos : 0 < R := lt_trans hr0 hrR
  -- continuity of the primitive on [r_in, R] (log is C^1 away from 0)
  have hcontF : ContinuousOn F (Set.Icc r_in R) := by
    intro x hx
    apply ContinuousAt.continuousWithinAt
    have hx0 : x ≠ 0 := ne_of_gt (pos_of_mem_Icc hr0 hrR hx)
    unfold F
    fun_prop
  -- HasDerivAt of the primitive at every interior point, value = fP x
  have hfd : ∀ x ∈ Set.Ioo r_in R, HasDerivAt F (fP x) x := by
    intro x hx
    have hx0 : x ≠ 0 := ne_of_gt (pos_of_mem_Ioo hr0 hrR hx)
    have hlogd : HasDerivAt Real.log x⁻¹ x := hasDerivAt_log hx0
    have hm : HasDerivAt (fun t : ℝ => M_in * Real.log t) (M_in * x⁻¹) x := hlogd.const_mul M_in
    have hmm : HasDerivAt (fun t : ℝ => m_s * t) m_s x := by
      simpa using (hasDerivAt_id x).const_mul m_s
    have hinner : HasDerivAt
        (fun t : ℝ => M_in * Real.log t + m_s * t - m_s * r_in * Real.log t)
        (M_in * x⁻¹ + m_s - m_s * r_in * x⁻¹) x := by
      exact (hm.add hmm).sub (hlogd.const_mul (m_s * r_in))
    have hFd : HasDerivAt F (G * m_s * (M_in * x⁻¹ + m_s - m_s * r_in * x⁻¹)) x := by
      simpa [F] using hinner.const_mul (G * m_s)
    have hval : G * m_s * (M_in * x⁻¹ + m_s - m_s * r_in * x⁻¹) = fP x := by
      unfold fP
      field_simp [hx0]
      ring
    simpa [hval] using hFd
  have hcontP : ContinuousOn fP (Set.Icc r_in R) := by
    intro x hx
    apply ContinuousAt.continuousWithinAt
    have hx0 : x ≠ 0 := ne_of_gt (pos_of_mem_Icc hr0 hrR hx)
    unfold fP
    fun_prop
  have hcontP_u : ContinuousOn fP (Set.uIcc r_in R) := by
    simpa [Set.uIcc_of_le (le_of_lt hrR)] using hcontP
  have hint : IntervalIntegrable fP MeasureTheory.volume r_in R := hcontP_u.intervalIntegrable
  have hftc : (∫ r in r_in..R, fP r) = F R - F r_in := by
    simpa [fP] using (intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le
      (le_of_lt hrR) hcontF hfd hint)
  rw [hftc]
  unfold F
  have hlog : Real.log (R / r_in) = Real.log R - Real.log r_in :=
    Real.log_div (ne_of_gt hRpos) (ne_of_gt hr0)
  rw [hlog]
  ring

/-- T2: the separation identity -- the total is exactly the central-mass term
   plus the shell self-gravity term; the two are distinct bookkeeping. -/
theorem separation_of_terms (G m_s M_in r_in R : ℝ) :
    Wtot G m_s M_in r_in R = Wcent G m_s M_in r_in R + Wself G m_s r_in R := by
  rfl

/-- T3: physical virial value, -(integral) = W_cent + W_self. -/
theorem virial_value (G m_s M_in r_in R : ℝ) (hr0 : 0 < r_in) (hrR : r_in < R) :
    -(∫ r in r_in..R, G * m_s * (M_in + m_s * (r - r_in)) / r)
      = Wtot G m_s M_in r_in R := by
  rw [virial_integral_closed G m_s M_in r_in R hr0 hrR]
  unfold Wtot Wcent Wself
  ring

/-- T4: exact deviation of the naive -G M(R)^2/R replacement from the true
   virial, for any M_in (negative control error structure). -/
theorem naive_error_exact (G m_s M_in r_in R : ℝ) (hR : R ≠ 0) :
    Wnaive G m_s M_in r_in R - Wtot G m_s M_in r_in R =
      -G * M_in ^ 2 / R
        + G * m_s * M_in * (Real.log (R / r_in) - 2 * (1 - r_in / R))
        - G * m_s ^ 2 * r_in * (Real.log (R / r_in) - (1 - r_in / R)) := by
  unfold Wnaive Wtot Wcent Wself
  field_simp [hR]
  nlinarith [mul_inv_cancel₀ hR]

/-- T5 NEGATIVE CONTROL: on every finite shell (r_in > 0) with no central mass
   the naive -G M(R)^2/R is strictly more negative than the true virial:
   naive - exact < 0.  (The naive form is exact only in the singular limit
   r_in -> 0, T6.) -/
theorem naive_overbinds (hG : 0 < G) (hm : 0 < m_s) (hr0 : 0 < r_in) (hrR : r_in < R) :
    Wnaive G m_s 0 r_in R - Wtot G m_s 0 r_in R < 0 := by
  have hRpos : 0 < R := lt_trans hr0 hrR
  have hR0 : R ≠ 0 := ne_of_gt hRpos
  have hdev : Wnaive G m_s 0 r_in R - Wtot G m_s 0 r_in R
      = -G * m_s ^ 2 * r_in * (Real.log (R / r_in) - (1 - r_in / R)) := by
    unfold Wnaive Wtot Wcent Wself
    field_simp [hR0]
    nlinarith [mul_inv_cancel₀ hR0]
  rw [hdev]
  have hbrack : 0 < Real.log (R / r_in) - (1 - r_in / R) := by
    have hu_lt : r_in / R < 1 := (div_lt_one hRpos).2 hrR
    have hlog_lt : Real.log (r_in / R) < r_in / R - 1 := by
      apply Real.log_lt_sub_one_of_pos
      · exact div_pos hr0 hRpos
      · intro hEqOne
        have hrin_eq : r_in = R := by
          have hRm : R ≠ 0 := ne_of_gt hRpos
          field_simp [hRm] at hEqOne
          linarith
        linarith
    have hswap : Real.log (R / r_in) = -Real.log (r_in / R) := by
      rw [← Real.log_inv]
      congr 1
      rw [inv_div]
    nlinarith
  have hprod : 0 < G * m_s ^ 2 * r_in * (Real.log (R / r_in) - (1 - r_in / R)) := by
    exact mul_pos (mul_pos (mul_pos hG (pow_pos hm 2)) hr0) hbrack
  linarith

/-- T6: singular-sphere recovery -- W_self(r_in) -> -G m_s^2 R as r_in -> 0^+,
   i.e. the naive form -G M(R)^2/R (with M(R) = m_s R) is exact only in the
   singular limit. -/
theorem wself_singular_limit (G m_s R : ℝ) (hR : 0 < R) :
    Filter.Tendsto (fun r_in : ℝ => Wself G m_s r_in R) (𝓝[>] (0 : ℝ))
      (𝓝 (-(G * m_s ^ 2 * R))) := by
  unfold Wself
  have ht_id : Filter.Tendsto id (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) :=
    tendsto_nhdsWithin_of_tendsto_nhds (@Filter.tendsto_id ℝ (𝓝 (0 : ℝ)))
  have ht_rlog : Filter.Tendsto (fun r : ℝ => r * Real.log r) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    have h := tendsto_log_mul_rpow_nhdsGT_zero (r := 1)
    simpa [pow_one, mul_comm] using h
  have ht_rlogR : Filter.Tendsto (fun r : ℝ => r * Real.log R) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    have hc : Filter.Tendsto (fun r : ℝ => Real.log R * id r) (𝓝[>] (0 : ℝ)) (𝓝 (Real.log R * 0)) :=
      Filter.Tendsto.const_mul (Real.log R) ht_id
    simpa [mul_zero] using
      (Filter.Tendsto.congr' (Filter.Eventually.of_forall (by intro r; simp [mul_comm])) hc)
  have hev' : ∀ᶠ r in 𝓝[>] (0 : ℝ), Real.log (R / r) = Real.log R - Real.log r := by
    filter_upwards [self_mem_nhdsWithin] with r hrpos
    exact Real.log_div (ne_of_gt hR) (ne_of_gt hrpos)
  have hcc : Filter.Tendsto (fun r : ℝ => r * (Real.log R - Real.log r)) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    simpa using Filter.Tendsto.congr'
      (Filter.Eventually.of_forall (by intro r; ring)) (ht_rlogR.sub ht_rlog)
  have ht_comb : Filter.Tendsto (fun r : ℝ => r * Real.log (R / r)) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    refine Filter.Tendsto.congr' ?_ hcc
    exact hev'.mono (by intro r hr; simpa [hr])
  have ht_brace : Filter.Tendsto (fun r : ℝ => R - r - r * Real.log (R / r)) (𝓝[>] (0 : ℝ)) (𝓝 R) := by
    have ht_sum : Filter.Tendsto (fun r : ℝ => r + r * Real.log (R / r)) (𝓝[>] (0 : ℝ)) (𝓝 (0 + 0)) :=
      ht_id.add ht_comb
    have ht_sub : Filter.Tendsto (fun r : ℝ => R - (r + r * Real.log (R / r))) (𝓝[>] (0 : ℝ)) (𝓝 (R - (0 + 0))) :=
      tendsto_const_nhds.sub ht_sum
    have hcong : Filter.Tendsto (fun r : ℝ => R - r - r * Real.log (R / r)) (𝓝[>] (0 : ℝ)) (𝓝 (R - (0 + 0))) := by
      refine Filter.Tendsto.congr' ?_ ht_sub
      exact Filter.Eventually.of_forall (by intro r; ring)
    simpa using hcong
  have houter : Filter.Tendsto
      (fun r_in : ℝ => -(G * m_s ^ 2 * (R - r_in - r_in * Real.log (R / r_in))))
      (𝓝[>] (0 : ℝ)) (𝓝 (-(G * m_s ^ 2 * R))) := by
    have hmul : Filter.Tendsto
        (fun r_in : ℝ => G * m_s ^ 2 * (R - r_in - r_in * Real.log (R / r_in)))
        (𝓝[>] (0 : ℝ)) (𝓝 (G * m_s ^ 2 * R)) :=
      tendsto_const_nhds.mul ht_brace
    simpa using hmul.neg
  simpa using houter

#print axioms virial_integral_closed
#print axioms separation_of_terms
#print axioms virial_value
#print axioms naive_error_exact
#print axioms naive_overbinds
#print axioms wself_singular_limit
