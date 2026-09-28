import Mathlib
import Mathlib.Tactic

/-
  AS044 -- Deep point-source potential and boundary matching (Lean 4 certificate).

  Framework (FRAMEWORK_CONTRACT): a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ADOPTED
  as input. Deep point-source force g = sqrt(G Mb a0)/r = C / r with C = v_flat^2,
  matched at a finite radius to a Newtonian interior g_N = G Mb / r^2.

  Certified contents (all dimensionless, real analysis):
    T1  deep force equals a0 at the MOND radius:       C / rM = a0
    T2  Newtonian force equals a0 at rM:                G*Mb / rM^2 = a0
    T3  double continuity (Phi and g) forces r_t = rM:  r_t^2 = rM^2 follows from
        G*Mb/rt^2 = C/rt and the two defining squares
    T4  log-scale identity fixing the integration constant:
        log(rM / (e * rM)) = -1     (so Phi_deep(rM) = -C matches Phi_N(rM) = -C)
    T5  potential continuity: C * log(rM/(e rM)) = -C
    T6  derivative of the deep logarithmic potential is C / r:
        d/dr [C log(r / (e rM))] = C / r     (r > 0)
    T7  pointwise log-law (cleared algebra): log(t/(e rM)) = log t - log(e rM)

  Sign data (C > 0, rM > 0, a0 > 0, G*Mb > 0) is physical input: C = v_flat^2 > 0,
  rM = sqrt(G Mb / a0) > 0 for a0 > 0 and Mb > 0.

  Axiom bar: zero `sorry`; axioms subseteq {propext, Classical.choice, Quot.sound}.
-/

noncomputable section
open Real Filter

namespace AS044

-- T1: deep force at the transition radius equals a0, given the defining squares
--     C^2 = G*Mb*a0 and rM^2 = G*Mb/a0.
theorem deep_force_at_rM {C G Mb a0 rM : ℝ}
    (hC : C ^ 2 = G * Mb * a0) (hrM : rM ^ 2 = G * Mb / a0)
    (hCpos : 0 < C) (hrMpos : 0 < rM) (hposa0 : 0 < a0) : C / rM = a0 := by
  have ha0ne : a0 ≠ 0 := ne_of_gt hposa0
  have hrMne : rM ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hrMpos)
  have hrMmul : rM ^ 2 * a0 = G * Mb := by
    calc
      rM ^ 2 * a0 = (G * Mb / a0) * a0 := by rw [hrM]
      _ = G * Mb := by field_simp [ha0ne]
  have hC2 : C ^ 2 = a0 ^ 2 * rM ^ 2 := by
    nlinarith [hC, hrMmul]
  have hsq : (C / rM) ^ 2 = a0 ^ 2 := by
    rw [div_pow, hC2]
    field_simp [hrMne]
  have hposq : 0 < C / rM := div_pos hCpos hrMpos
  have hprod : (C / rM - a0) * (C / rM + a0) = (C / rM) ^ 2 - a0 ^ 2 := by ring
  have hfac : (C / rM - a0) * (C / rM + a0) = 0 := by
    rw [hprod, hsq]
    ring
  rcases mul_eq_zero.mp hfac with hz | hz
  · linarith [hz]
  · have hgt : 0 < C / rM + a0 := add_pos hposq hposa0
    linarith [hz, hgt]

-- T2: Newtonian force at the transition radius equals a0.
theorem newton_force_at_rM {G Mb a0 rM : ℝ}
    (hrM : rM ^ 2 = G * Mb / a0) (_hpos : 0 < G * Mb) (hposa0 : 0 < a0)
    (hposrM : 0 < rM) : G * Mb / rM ^ 2 = a0 := by
  have ha0ne : a0 ≠ 0 := ne_of_gt hposa0
  have hrMne : rM ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hposrM)
  have hmu : rM ^ 2 * a0 = G * Mb := by
    calc
      rM ^ 2 * a0 = (G * Mb / a0) * a0 := by rw [hrM]
      _ = G * Mb := by field_simp [ha0ne]
  calc
    G * Mb / rM ^ 2 = (rM ^ 2 * a0) / rM ^ 2 := by rw [hmu]
    _ = a0 := by field_simp [hrMne]

-- T3: double continuity of force at the transition radius forces r_t = rM:
--     G*Mb/rt^2 = C/rt together with C^2 = G*Mb*a0 and rM^2 = G*Mb/a0 imply
--     rt^2 = rM^2.
theorem double_continuity_forces_rM {C G Mb a0 rt rM : ℝ}
    (hC : C ^ 2 = G * Mb * a0) (hrM : rM ^ 2 = G * Mb / a0)
    (hforce : G * Mb / rt ^ 2 = C / rt)
    (hpos : 0 < G * Mb) (hposa0 : 0 < a0) (hrt : 0 < rt) : rt ^ 2 = rM ^ 2 := by
  have hrtne : rt ≠ 0 := ne_of_gt hrt
  have ha0ne : a0 ≠ 0 := ne_of_gt hposa0
  have hrtsq : rt ^ 2 ≠ 0 := pow_ne_zero 2 hrtne
  have hlin : G * Mb = C * rt := by
    have hh := congrArg (fun z : ℝ => z * rt ^ 2) hforce
    field_simp [hrtsq] at hh
    rw [mul_comm rt C] at hh
    exact hh
  have hsq2 : (G * Mb) ^ 2 = (G * Mb) * (a0 * rt ^ 2) := by
    calc
      (G * Mb) ^ 2 = (C * rt) ^ 2 := congrArg (fun z : ℝ => z ^ 2) hlin
      _ = C ^ 2 * rt ^ 2 := by ring
      _ = (G * Mb * a0) * rt ^ 2 := by rw [hC]
      _ = (G * Mb) * (a0 * rt ^ 2) := by ring
  have hsq2' : (G * Mb) * (G * Mb) = (G * Mb) * (a0 * rt ^ 2) := by
    rwa [pow_two] at hsq2
  have hcancel : G * Mb = a0 * rt ^ 2 := mul_left_cancel₀ hpos.ne' hsq2'
  have hrt2 : rt ^ 2 = G * Mb / a0 := by
    rw [eq_div_iff_mul_eq ha0ne, hcancel, mul_comm a0 (rt ^ 2)]
  calc
    rt ^ 2 = G * Mb / a0 := hrt2
    _ = rM ^ 2 := by rw [hrM]

-- T4: the logarithmic integration constant: log(rM/(e rM)) = -1.
theorem log_rM_over_exp_rM {rM : ℝ} (hrM : 0 < rM) :
    Real.log (rM / (Real.exp 1 * rM)) = -1 := by
  have hne : rM ≠ 0 := ne_of_gt hrM
  have hposE : 0 < Real.exp 1 := Real.exp_pos 1
  have hneE : Real.exp 1 ≠ 0 := ne_of_gt hposE
  have hdenpos : 0 < Real.exp 1 * rM := mul_pos hposE hrM
  have hdenne : Real.exp 1 * rM ≠ 0 := ne_of_gt hdenpos
  calc
    Real.log (rM / (Real.exp 1 * rM))
        = Real.log rM - Real.log (Real.exp 1 * rM) := Real.log_div hne hdenne
    _ = Real.log rM - (Real.log (Real.exp 1) + Real.log rM) := by
      rw [Real.log_mul hneE hne]
    _ = -(Real.log (Real.exp 1)) := by ring
    _ = -1 := by rw [Real.log_exp]

-- T5: potential continuity at rM: C * log(rM/(e rM)) = -C.
theorem potential_continuity {C rM : ℝ} (hrM : 0 < rM) :
    C * Real.log (rM / (Real.exp 1 * rM)) = -C := by
  rw [log_rM_over_exp_rM hrM]
  ring

-- T7 (cleared algebra): pointwise log identity on (0, oo).
theorem log_div_pointwise {rM t : ℝ} (ht : 0 < t) (hrM : 0 < rM) :
    Real.log (t / (Real.exp 1 * rM)) = Real.log t - Real.log (Real.exp 1 * rM) := by
  have htne : t ≠ 0 := ne_of_gt ht
  have hposE : 0 < Real.exp 1 := Real.exp_pos 1
  have hneE : Real.exp 1 ≠ 0 := ne_of_gt hposE
  have hdenpos : 0 < Real.exp 1 * rM := mul_pos hposE hrM
  have hdenne : Real.exp 1 * rM ≠ 0 := ne_of_gt hdenpos
  exact Real.log_div htne hdenne

-- T6: derivative of the deep logarithmic potential is C / r on (0, oo), certified
--     for the difference form  d/dt [C (log t - log(e rM))] = C / t, which is
--     pointwise equal to d/dt [C log(t / (e rM))] by the log law (T7).
theorem deep_potential_deriv {C rM r : ℝ} (hr : 0 < r) :
    HasDerivAt (fun t : ℝ => C * (Real.log t - Real.log (Real.exp 1 * rM))) (C / r) r := by
  have hlog : HasDerivAt Real.log (r⁻¹) r := Real.hasDerivAt_log (ne_of_gt hr)
  have hold : HasDerivAt (Real.log - fun _ : ℝ => Real.log (Real.exp 1 * rM)) (r⁻¹ - 0) r :=
    hlog.sub (hasDerivAt_const r (Real.log (Real.exp 1 * rM)))
  rw [sub_zero] at hold
  have hsub : HasDerivAt (fun t : ℝ => Real.log t - Real.log (Real.exp 1 * rM)) (r⁻¹) r := by
    exact hold
  have hsc := hsub.const_mul C
  have hc : C * r⁻¹ = C / r := by
    field_simp [ne_of_gt hr]
  simpa [hc] using hsc

end AS044