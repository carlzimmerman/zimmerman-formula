import Mathlib
import Mathlib.Tactic

/-!
# AS653 -- General flux power fixes acceleration homogeneity (Lean 4 certificate)

Formalized content (k04 four-form promotion cell; `q > 0` without loss of
generality since every physical quantity depends on `|q|` only; q != 0 is the
seed's declared domain):

    Pvac (lam n q)   := lam * q^n                       -- vacuum action density
    epsVac (lam n q) := q * P'_q - Pvac                 -- Legendre vacuum energy
    a0  (beta m q)   := beta * q^m                      -- flux-promoted scale
    kappa2(beta gN lam n m q) := a0^2 / (gN * epsVac)   -- a0^2/(G_N eps_vac)

  T1  derivative fact + LEGENDRE IDENTITY: for q > 0,
        d/dt (lam * t^n)|_q = n * lam * q^(n-1),  and
        epsVac = lam * (n-1) * q^n   (k04 F1 convention).

  T2  SIGN CONTROL: lam > 0, n > 1, q > 0  ==>  0 < epsVac
        (n = 1 gives epsVac = 0, n < 1 gives a negative vacuum energy --
         both excluded by the declared domain n > 1).

  T3  THE RATIO: kappa2 = beta^2 * q^(2m-n) / (gN * lam * (n-1))  (exact).

  T4  AMPLITUDE-FREE: n = 2m  ==>  kappa2 is the same constant for every
        pair of positive flux amplitudes q1, q2.

  T5  ANALYTIC LEMMA: (2 : ℝ)^a = 1  ==>  a = 0   [Real.log route].

  T6  NEGATIVE CONTROL (formal): 2m - n != 0  ==>  kappa2(1) != kappa2(2):
        the residual ratio is 2^(2m-n) != 1.  Amplitude cancellation for
        ARBITRARY (n,m) is FALSE -- the inference fails exactly when 2m-n != 0.

  T7  EQUIVALENCE: amplitude independence over all positive amplitudes
        <==>  n = 2m.

  T8  COEFFICIENT GATE: at n = 2m with the kappa = 1/2 constraint
        lam * (n-1) * gN = 4 * beta^2  (= lam*gN/beta^2 = 4/(n-1)),
        kappa2 = 1/4.  The amplitude problem is solved; the coefficient
        value remains a free combination (rank-1 identifiability, B2).

Certification discipline: no sorry. Axioms expected within
{propext, Classical.choice, Quot.sound}.
-/

noncomputable section
open Real
open scoped Topology

namespace AS653

def Pvac (lam n q : ℝ) : ℝ := lam * q ^ n

-- Legendre vacuum energy with the certified derivative value n*lam*q^(n-1):
def epsVac (lam n q : ℝ) : ℝ := q * (n * lam * q ^ (n - 1)) - Pvac lam n q

def a0 (beta m q : ℝ) : ℝ := beta * q ^ m

def kappa2 (beta gN lam n m q : ℝ) : ℝ := a0 beta m q ^ 2 / (gN * epsVac lam n q)

-- ------------------------------------------------------------------- T1
theorem T1_deriv (lam n q : ℝ) (hq : 0 < q) :
    HasDerivAt (fun t : ℝ => Pvac lam n t) (n * lam * q ^ (n - 1)) q := by
  have hd : HasDerivAt (fun t : ℝ => t ^ n) (n * q ^ (n - 1)) q :=
    Real.hasDerivAt_rpow_const (Or.inl (ne_of_gt hq))
  simpa [Pvac, mul_assoc, mul_left_comm, mul_comm] using hd.const_mul lam

theorem T1_legendre (lam n q : ℝ) (hq : 0 < q) :
    epsVac lam n q = lam * (n - 1) * q ^ n := by
  unfold epsVac Pvac
  have hqmul : q * q ^ (n - 1) = q ^ n := by
    have hq1 : (q : ℝ) ^ (1 : ℝ) = q := Real.rpow_one q
    have hqadd : q ^ n = q * q ^ (n - 1) := by
      calc
        q ^ n = q ^ (1 + (n - 1)) := by congr 1; ring
        _ = q ^ 1 * q ^ (n - 1) := Real.rpow_add hq 1 (n - 1)
        _ = q * q ^ (n - 1) := by rw [hq1]
    exact hqadd.symm
  calc
    q * (n * lam * q ^ (n - 1)) - lam * q ^ n
        = lam * n * (q * q ^ (n - 1)) - lam * q ^ n := by ring
    _ = lam * n * q ^ n - lam * q ^ n := by rw [hqmul]
    _ = lam * (n - 1) * q ^ n := by ring

-- ------------------------------------------------------------------- T2
theorem T2_eps_pos (lam n q : ℝ) (hlam : 0 < lam) (hn1 : 1 < n) (hq : 0 < q) :
    0 < epsVac lam n q := by
  rw [T1_legendre lam n q hq]
  exact mul_pos (mul_pos hlam (sub_pos.mpr hn1)) (Real.rpow_pos_of_pos hq n)

-- ------------------------------------------------------------------- T3
theorem T3_kappa2 (beta gN lam n m q : ℝ)
    (hq : 0 < q) (hgN : 0 < gN) (hlam : 0 < lam) (hn1 : 1 < n) :
    kappa2 beta gN lam n m q = beta ^ 2 * q ^ (2 * m - n) / (gN * lam * (n - 1)) := by
  unfold kappa2 a0
  rw [T1_legendre lam n q hq]
  have hpow : q ^ (2 * m) / q ^ n = q ^ (2 * m - n) := by
    rw [Real.rpow_sub hq (2 * m) n]
  have harg : m * 2 = 2 * m := by ring
  have hq2m : (q ^ m) ^ (2 : ℕ) = q ^ (2 * m : ℝ) := by
    rw [pow_two (q ^ m)]
    rw [← Real.rpow_add hq m m]
    congr 1
    ring
  calc
    (beta * q ^ m) ^ 2 / (gN * (lam * (n - 1) * q ^ n))
        = beta ^ 2 * (q ^ m) ^ 2 / (gN * lam * (n - 1) * q ^ n) := by ring
    _ = beta ^ 2 * q ^ (2 * m) / (gN * lam * (n - 1) * q ^ n) := by
      rw [hq2m]
    _ = (beta ^ 2 / (gN * lam * (n - 1))) * (q ^ (2 * m) / q ^ n) := by
      rw [← div_mul_div_comm]
    _ = (beta ^ 2 / (gN * lam * (n - 1))) * q ^ (2 * m - n) := by rw [hpow]
    _ = beta ^ 2 * q ^ (2 * m - n) / (gN * lam * (n - 1)) := by
      rw [div_mul_eq_mul_div]

-- ------------------------------------------------------------------- T4
theorem T4_amplitude_free (beta gN lam n m q1 q2 : ℝ)
    (hgN : 0 < gN) (hlam : 0 < lam) (hn1 : 1 < n)
    (hn : n = 2 * m) (hq1 : 0 < q1) (hq2 : 0 < q2) :
    kappa2 beta gN lam n m q1 = kappa2 beta gN lam n m q2 := by
  subst n
  have hq1pow : q1 ^ (2 * m - 2 * m) = 1 := by
    rw [sub_self (2 * m), Real.rpow_zero]
  have hq2pow : q2 ^ (2 * m - 2 * m) = 1 := by
    rw [sub_self (2 * m), Real.rpow_zero]
  rw [T3_kappa2 beta gN lam (2 * m) m q1 hq1 hgN hlam hn1,
      T3_kappa2 beta gN lam (2 * m) m q2 hq2 hgN hlam hn1]
  simp [hq1pow, hq2pow]

-- ------------------------------------------------------------------- T5
theorem T5_two_rpow_eq_one (a : ℝ) (h : (2 : ℝ) ^ a = 1) : a = 0 := by
  have hlog := congrArg Real.log h
  rw [Real.log_one] at hlog
  have hlr : Real.log ((2 : ℝ) ^ a) = a * Real.log 2 := Real.log_rpow (by norm_num) a
  rw [hlr] at hlog
  rcases mul_eq_zero.mp hlog with ha | hlog2
  · exact ha
  · exfalso
    have hz : (2 : ℝ) = 0 ∨ (2 : ℝ) = 1 ∨ (2 : ℝ) = -1 := Real.log_eq_zero.mp hlog2
    rcases hz with h0 | hone | hneg
    · norm_num at h0
    · norm_num at hone
    · norm_num at hneg

-- ------------------------------------------------------------------- T6
theorem T6_negative_control (beta gN lam n m : ℝ)
    (hbeta : 0 < beta) (hgN : 0 < gN) (hlam : 0 < lam) (hn1 : 1 < n)
    (ha : 2 * m - n ≠ 0) :
    kappa2 beta gN lam n m 1 ≠ kappa2 beta gN lam n m 2 := by
  intro heq
  have h1 : (1 : ℝ) ^ (2 * m - n) = 1 := Real.one_rpow (2 * m - n)
  have hq1 : (0 : ℝ) < 1 := by norm_num
  have hq2 : (0 : ℝ) < 2 := by norm_num
  rw [T3_kappa2 beta gN lam n m 1 hq1 hgN hlam hn1,
      T3_kappa2 beta gN lam n m 2 hq2 hgN hlam hn1] at heq
  rw [h1] at heq
  have hbeta2 : beta ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hbeta)
  have hden1 : (n - 1 : ℝ) ≠ 0 := ne_of_gt (sub_pos.mpr hn1)
  have hcancel : (2 : ℝ) ^ (2 * m - n) = 1 := by
    field_simp [hbeta2, hden1] at heq
    exact heq.symm
  exact ha (T5_two_rpow_eq_one (2 * m - n) hcancel)

-- ------------------------------------------------------------------- T7
theorem T7_iff (beta gN lam n m : ℝ)
    (hbeta : 0 < beta) (hgN : 0 < gN) (hlam : 0 < lam) (hn1 : 1 < n) :
    (∀ q1 q2 : ℝ, 0 < q1 → 0 < q2 →
       kappa2 beta gN lam n m q1 = kappa2 beta gN lam n m q2) ↔ n = 2 * m := by
  constructor
  · intro hκ
    by_contra hnz
    have hnz2 : 2 * m - n ≠ 0 := by
      intro hsub
      exact hnz (by linarith)
    exact T6_negative_control beta gN lam n m hbeta hgN hlam hn1 hnz2
      (hκ 1 2 (by norm_num) (by norm_num))
  · intro hn q1 q2 hq1 hq2
    exact T4_amplitude_free beta gN lam n m q1 q2 hgN hlam hn1 hn hq1 hq2

-- ------------------------------------------------------------------- T8
theorem T8_coefficient_gate (beta gN lam n m q : ℝ)
    (hbeta : 0 < beta) (hq : 0 < q) (hgN : 0 < gN) (hlam : 0 < lam) (hn1 : 1 < n)
    (hn : n = 2 * m) (hc : lam * (n - 1) * gN = 4 * beta ^ 2) :
    kappa2 beta gN lam n m q = 1 / 4 := by
  subst n
  have hqpow : q ^ (2 * m - 2 * m) = 1 := by
    rw [sub_self (2 * m), Real.rpow_zero]
  rw [T3_kappa2 beta gN lam (2 * m) m q hq hgN hlam hn1, hqpow]
  have hc' : gN * lam * (2 * m - 1) = 4 * beta ^ 2 := by
    calc
      gN * lam * (2 * m - 1) = lam * (2 * m - 1) * gN := by ring
      _ = 4 * beta ^ 2 := hc
  rw [hc']
  field_simp [pow_ne_zero 2 (ne_of_gt hbeta), (by norm_num : (4 : ℝ) ≠ 0)]

end AS653

#print axioms AS653.T1_deriv
#print axioms AS653.T1_legendre
#print axioms AS653.T2_eps_pos
#print axioms AS653.T3_kappa2
#print axioms AS653.T4_amplitude_free
#print axioms AS653.T5_two_rpow_eq_one
#print axioms AS653.T6_negative_control
#print axioms AS653.T7_iff
#print axioms AS653.T8_coefficient_gate
