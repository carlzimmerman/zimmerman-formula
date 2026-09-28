import Mathlib

/-!
AS032 -- RAR phantom acceleration maximum (Lean 4 certificates).

Branch RAR (framework contract, criterion B):  nu_RAR(y) = 1/(1-exp(-sqrt(y))),
y = B/a0 > 0; the phantom (excess) acceleration is

    h_RAR(y) = y*(nu_RAR(y)-1) = y/(exp(sqrt(y))-1).

Work in t = sqrt(y) > 0:  R(t) := t^2/(e^t - 1).  Exact calculus:

    dR/dt = t*F(t)/(e^t-1)^2,   F(t) := (2-t)*e^t - 2,
    h'(y) = F(t)/(2 (e^t-1)^2),    so h' = 0  <=>  F(t) = 0  (t > 0)
    peak equation (exact form):    e^t (2-t) = 2,   t = sqrt(y).

Certified here (self-contained algebra on the declared RAR branch):
  A  derivative identity  d/dt [t^2/(e^t-1)] = t*F(t)/(e^t-1)^2   (e^t != 1)
  B  at a (positive) root of F the slope vanishes: h'(y_p) = 0
     (t != 0 is exactly the negative control: t = 0 also solves F t = 0
      but there e^t - 1 = 0 and the slope identity does not apply)
  C  exact peak-value law: whenever F(t)=0 and t≠0,  R(t) = t*(2-t)
     (so h_p = sqrt(y_p)*(2 - sqrt(y_p)) exactly as a function of the landmark)
  D  the peak equation in exact form: F t = 0 <-> (2-t)*e^t = 2
  E  Q branch (g^2 = B^2 + a0 B): h_Q/a0 = y(sqrt(1+1/y)-1) = 1/(1+sqrt(1+1/y))
     and the strict cap h_Q(y) < 1/2 for all y > 0 (supremum 1/2 at y -> oo only)
  F  MU2 branch (mu2(x) = 1-(1+x/2)^-2): h_MU2/a0 = x/(1+x/2)^2 <= 1/2 with
     equality exactly at x = 2 (g = 2 a0); exact deficit identity.

The root LOCATION (t_p in (1,2), y_p = 2.5396382821881..., h_p = 0.64761023789191...)
is analytic/numerical (IVT + strict monotonicity of F on (1,2), 50-digit mpmath);
this file certifies the algebraic identities those numbers plug into.
-/

noncomputable section
open Real

def RAR_t (t : ℝ) : ℝ := t ^ 2 / (Real.exp t - 1)
def F (t : ℝ) : ℝ := (2 - t) * Real.exp t - 2

/- A: exact first-derivative identity: d/dt [t^2/(e^t-1)] = t*F(t)/(e^t-1)^2,
   on the domain e^t != 1 (the peak t_p in (1,2) satisfies it; t = 0 does not). -/
theorem rar_deriv_identity (t : ℝ) (hne : Real.exp t ≠ 1) :
    HasDerivAt RAR_t (t * F t / (Real.exp t - 1) ^ 2) t := by
  unfold RAR_t F
  have hd_num : HasDerivAt (fun s : ℝ => s ^ 2) (2 * t) t := by
    change HasDerivAt (id ^ (2 : ℕ)) ((2 : ℝ) * t) t
    simpa using (hasDerivAt_id t).pow (2 : ℕ)
  have hd_den : HasDerivAt (fun s : ℝ => Real.exp s - 1) (Real.exp t) t :=
    (hasDerivAt_exp t).sub_const 1
  have hdq : HasDerivAt (fun s : ℝ => s ^ 2 / (Real.exp s - 1))
      ((2 * t * (Real.exp t - 1) - t ^ 2 * Real.exp t) / (Real.exp t - 1) ^ 2) t := by
    exact hd_num.div hd_den (sub_ne_zero.mpr hne)
  have hnum : 2 * t * (Real.exp t - 1) - t ^ 2 * Real.exp t =
      t * ((2 - t) * Real.exp t - 2) := by ring
  simpa [hnum] using hdq

/- B: at a root of F with t != 0 the slope vanishes (h'(y_p) = 0). -/
theorem rar_slope_zero_at_peak (t : ℝ) (ht0 : t ≠ 0) (hF : F t = 0) :
    HasDerivAt RAR_t 0 t := by
  have hne : Real.exp t ≠ 1 := by
    intro h
    have hmul : (2 - t) * Real.exp t = 2 := sub_eq_zero.mp hF
    rw [h] at hmul
    norm_num at hmul
    exact ht0 hmul
  have hd := rar_deriv_identity t hne
  rw [hF] at hd
  convert hd using 1
  ring

/- C: exact peak-value law h_p = t_p*(2 - t_p) given the peak equation and t != 0. -/
theorem rar_peak_value (t : ℝ) (ht0 : t ≠ 0) (hF : F t = 0) :
    RAR_t t = t * (2 - t) := by
  unfold RAR_t F at *
  have hmul : (2 - t) * Real.exp t = 2 := sub_eq_zero.mp hF
  have ht2 : 2 - t ≠ 0 := by
    intro hz
    rw [hz] at hF
    norm_num at hF
  have hexp : Real.exp t = 2 / (2 - t) := by
    rw [eq_div_iff ht2]
    simpa [mul_comm] using hmul
  have hexpm1 : Real.exp t - 1 = t / (2 - t) := by
    rw [hexp]
    field_simp [ht2]
    ring
  calc
    t ^ 2 / (Real.exp t - 1) = t ^ 2 / (t / (2 - t)) := by rw [hexpm1]
    _ = t * (2 - t) := by
      field_simp [ht0, ht2]

/- D: the peak equation in exact form: F t = 0 <-> e^t (2-t) = 2. -/
theorem peak_equation_iff (t : ℝ) : F t = 0 ↔ (2 - t) * Real.exp t = 2 := by
  unfold F
  constructor <;> intro h <;> linarith

/-! Q branch:  g^2 = B^2 + a0*B  =>  (g-B)/a0 = y*(sqrt(1+1/y)-1). -/

def Qh (y : ℝ) : ℝ := y * (Real.sqrt (1 + 1 / y) - 1)

/- E1: exact rationalized (stable) identity, valid on y > 0. -/
theorem q_identity (y : ℝ) (hy : 0 < y) : Qh y = 1 / (1 + Real.sqrt (1 + 1 / y)) := by
  unfold Qh
  have hyne : y ≠ 0 := ne_of_gt hy
  have harg_nonneg : 0 ≤ 1 + 1 / y := by nlinarith [one_div_pos.mpr hy]
  have hwsq : Real.sqrt (1 + 1 / y) ^ 2 = 1 + 1 / y := Real.sq_sqrt harg_nonneg
  have hwpos : 0 < Real.sqrt (1 + 1 / y) + 1 := by
    have hw0 : 0 ≤ Real.sqrt (1 + 1 / y) := Real.sqrt_nonneg (1 + 1 / y)
    nlinarith
  have hw1 : Real.sqrt (1 + 1 / y) + 1 ≠ 0 := ne_of_gt hwpos
  have hprod : (Real.sqrt (1 + 1 / y) - 1) * (Real.sqrt (1 + 1 / y) + 1) = 1 / y := by
    calc
      (Real.sqrt (1 + 1 / y) - 1) * (Real.sqrt (1 + 1 / y) + 1) = Real.sqrt (1 + 1 / y) ^ 2 - 1 := by ring
      _ = 1 / y := by
        rw [hwsq]
        ring
  have hwminus : Real.sqrt (1 + 1 / y) - 1 = (1 / y) / (Real.sqrt (1 + 1 / y) + 1) := by
    rw [eq_div_iff hw1]
    simpa [mul_comm] using hprod
  have hmain : y * (Real.sqrt (1 + 1 / y) - 1) = 1 / (Real.sqrt (1 + 1 / y) + 1) := by
    rw [hwminus]
    have hyi : y * (1 / y) = 1 := by
      rw [one_div]
      exact mul_inv_cancel₀ hyne
    calc
      y * ((1 / y) / (Real.sqrt (1 + 1 / y) + 1)) = (y * (1 / y)) / (Real.sqrt (1 + 1 / y) + 1) := by ring
      _ = 1 / (Real.sqrt (1 + 1 / y) + 1) := by rw [hyi]
  have hcomm : 1 / (Real.sqrt (1 + 1 / y) + 1) = 1 / (1 + Real.sqrt (1 + 1 / y)) := by
    congr 1
    rw [add_comm]
  rw [← hcomm]
  exact hmain

/- E2: strict cap: h_Q(y) < 1/2 for every y > 0 (supremum 1/2, attained only at infinity). -/
theorem q_strict_cap (y : ℝ) (hy : 0 < y) : Qh y < 1 / 2 := by
  rw [q_identity y hy]
  have hbg : 1 < Real.sqrt (1 + 1 / y) := by
    rw [← Real.sqrt_one]
    exact Real.sqrt_lt_sqrt (by norm_num) (by nlinarith [one_div_pos.mpr hy])
  have hden : 2 < 1 + Real.sqrt (1 + 1 / y) := by nlinarith [hbg]
  have hpos : 0 < 1 + Real.sqrt (1 + 1 / y) := by nlinarith [hbg]
  rw [div_lt_iff₀ hpos]
  nlinarith [hden]

/-! MU2 branch:  mu2(x) = 1-(1+x/2)^(-2),  mu2(x)*g = B,  x = g/a0.
   Phantom: (g-B)/a0 = x*(1-mu2(x)) = x/(1+x/2)^2. -/

def MU2h (x : ℝ) : ℝ := x / (1 + x / 2) ^ 2

/- F1: exact deficit identity 1/2 - h_MU2(x) = (1-x/2)^2 / (2 (1+x/2)^2). -/
theorem mu2_deficit (x : ℝ) (hx : 0 < x) :
    1 / 2 - MU2h x = (1 - x / 2) ^ 2 / (2 * (1 + x / 2) ^ 2) := by
  unfold MU2h
  have hden : 0 < 1 + x / 2 := by nlinarith
  have hdn : (1 + x / 2) ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hden)
  field_simp [hdn]
  ring

/- F2: cap: h_MU2(x) <= 1/2. -/
theorem mu2_capped (x : ℝ) (hx : 0 < x) : MU2h x ≤ 1 / 2 := by
  rw [← sub_nonneg]
  rw [mu2_deficit x hx]
  have hden : 0 < 2 * (1 + x / 2) ^ 2 := by
    have hp : 0 < (1 + x / 2) ^ 2 := sq_pos_of_pos (by nlinarith : (0 : ℝ) < 1 + x / 2)
    nlinarith
  exact div_nonneg (sq_nonneg (1 - x / 2)) (le_of_lt hden)

/- F3: attained exactly at x = 2 (g = 2 a0). -/
theorem mu2_max_iff (x : ℝ) (hx : 0 < x) : MU2h x = 1 / 2 ↔ x = 2 := by
  constructor
  · intro heq
    have hd := mu2_deficit x hx
    rw [heq] at hd
    have hd0 : 0 = (1 - x / 2) ^ 2 / (2 * (1 + x / 2) ^ 2) := by simpa using hd
    have hden : (2 * (1 + x / 2) ^ 2) ≠ 0 := by
      have hp : 0 < (1 + x / 2) ^ 2 := sq_pos_of_pos (by nlinarith : (0 : ℝ) < 1 + x / 2)
      nlinarith
    have hnum_or : (1 - x / 2) ^ 2 = 0 ∨ (2 * (1 + x / 2) ^ 2) = 0 := (div_eq_zero_iff).mp hd0.symm
    rcases hnum_or with hnum | hden0
    · have hlin : 1 - x / 2 = 0 := sq_eq_zero_iff.mp hnum
      linarith
    · exfalso
      exact hden hden0
  · intro hx2
    unfold MU2h
    rw [hx2]
    norm_num

#print axioms rar_deriv_identity
#print axioms rar_slope_zero_at_peak
#print axioms rar_peak_value
#print axioms peak_equation_iff
#print axioms q_identity
#print axioms q_strict_cap
#print axioms mu2_deficit
#print axioms mu2_capped
#print axioms mu2_max_iff
