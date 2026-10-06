import Mathlib

/-!
# CFG349 -- certificates for the khronon-timed memory switch (ratchet along the baryon flow)

Exact step solution of u.dm = Gamma H(-theta) (1 - m) over a step dt with chi = H(-theta) in {0,1}:
m' = 1 - (1 - m) exp(-(Gamma dt chi)).

* R1 ratchet monotonicity: m <= m' (a compression can only raise m: no flicker).
* R2 [0,1] invariance.
* R3 FRW-off invariance: if never triggered (chi = 0 at every step) and m0 = 0, then m = 0 at every step.
* R4 strong hyperbolicity: for c_s > 0, k != 0 the characteristic roots 0, c k, -c k are pairwise distinct;
  R4b the acoustic block's characteristic polynomial factors as (w - c k)(w + c k).
* R5 kinetic positivity of the baryons in the physical limit (inertia rho > 0).
* R6 L-ord partner identity: lambda' = a lambda + s, m' = a (1 - m)  =>  (lambda (1 - m))' = s (1 - m);
  R6b unsourced, lambda (1 - m) = C != 0 forces |lambda| >= |C|/eps once 1 - m <= eps (lambda diverges as m -> 1).
* R7 fidelity bound: 0 <= df <= 1 - m and X/A >= 0 give df X/A <= (1 - m) X/A.
* R8 reversible (MUTATE) memory with duty d has fixed point m = d (flicker around the duty, not ON).
-/

noncomputable def step (m G dt χ : ℝ) : ℝ := 1 - (1 - m) * Real.exp (-(G * dt * χ))

theorem R1_ratchet_monotone (m G dt χ : ℝ) (hm : m ≤ 1) (hx : 0 ≤ G * dt * χ) :
    m ≤ step m G dt χ := by
  unfold step
  have he : Real.exp (-(G * dt * χ)) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
  have h1 : 0 ≤ 1 - m := by linarith
  nlinarith [mul_le_mul_of_nonneg_left he h1]

theorem R2_unit_interval (m G dt χ : ℝ) (h0 : 0 ≤ m) (hm : m ≤ 1) (hx : 0 ≤ G * dt * χ) :
    0 ≤ step m G dt χ ∧ step m G dt χ ≤ 1 := by
  unfold step
  have he : Real.exp (-(G * dt * χ)) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
  have hp : 0 < Real.exp (-(G * dt * χ)) := Real.exp_pos _
  have h1 : 0 ≤ 1 - m := by linarith
  constructor
  · nlinarith [mul_le_mul_of_nonneg_left he h1]
  · nlinarith [mul_nonneg h1 hp.le]

theorem R3_frw_off (mseq : ℕ → ℝ) (G dt : ℝ) (χ : ℕ → ℝ)
    (hstep : ∀ n, mseq (n + 1) = step (mseq n) G dt (χ n)) (hχ : ∀ n, χ n = 0) (h0 : mseq 0 = 0) :
    ∀ n, mseq n = 0 := by
  intro n
  induction n with
  | zero => exact h0
  | succ n ih => rw [hstep, ih, hχ]; unfold step; simp

theorem R4_distinct_roots (c k : ℝ) (hc : 0 < c) (hk : k ≠ 0) :
    (0:ℝ) ≠ c * k ∧ (0:ℝ) ≠ -(c * k) ∧ c * k ≠ -(c * k) := by
  have h : c * k ≠ 0 := mul_ne_zero (ne_of_gt hc) hk
  refine ⟨fun e => h e.symm, fun e => h (by linarith), fun e => h (by linarith)⟩

theorem R4b_acoustic_charpoly (w c k ρ : ℝ) (hρ : ρ ≠ 0) :
    w * w - (ρ * k) * (c ^ 2 * k / ρ) = (w - c * k) * (w + c * k) := by
  field_simp; ring

theorem R5_kinetic_positive (ρ v : ℝ) (hρ : 0 < ρ) (hv : v ≠ 0) : 0 < ρ * v ^ 2 / 2 := by
  have : 0 < v ^ 2 := by positivity
  positivity

theorem R6_partner (L M : ℝ → ℝ) (a s : ℝ → ℝ) (t : ℝ)
    (hL : HasDerivAt L (a t * L t + s t) t) (hM : HasDerivAt M (a t * (1 - M t)) t) :
    HasDerivAt (fun u => L u * (1 - M u)) (s t * (1 - M t)) t := by
  exact (hL.mul ((hasDerivAt_const t (1:ℝ)).sub hM)).congr_deriv (by simp only [Pi.sub_apply]; ring)

theorem R6b_partner_diverges (L oneMinusM C ε : ℝ) (_hC : C ≠ 0) (hprod : L * oneMinusM = C)
    (hpos : 0 < oneMinusM) (hε : oneMinusM ≤ ε) : |C| / ε ≤ |L| := by
  have hεp : 0 < ε := lt_of_lt_of_le hpos hε
  rw [div_le_iff₀ hεp, ← hprod, abs_mul, abs_of_pos hpos]
  exact mul_le_mul_of_nonneg_left hε (abs_nonneg L)

theorem R7_fidelity (df m XA : ℝ) (_hdf : 0 ≤ df) (hle : df ≤ 1 - m) (hXA : 0 ≤ XA) :
    df * XA ≤ (1 - m) * XA := mul_le_mul_of_nonneg_right hle hXA

theorem R8_reversible_fixed_point (d m : ℝ) : d * (1 - m) - (1 - d) * m = 0 ↔ m = d := by
  constructor
  · intro h; linarith
  · intro h; subst h; ring

#print axioms R1_ratchet_monotone
#print axioms R2_unit_interval
#print axioms R3_frw_off
#print axioms R4_distinct_roots
#print axioms R4b_acoustic_charpoly
#print axioms R5_kinetic_positive
#print axioms R6_partner
#print axioms R6b_partner_diverges
#print axioms R7_fidelity
#print axioms R8_reversible_fixed_point
