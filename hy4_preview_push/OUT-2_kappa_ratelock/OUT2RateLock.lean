import Mathlib

/-!
# OUT-2 (KAPPA_RATELOCK): Lean certificates for the clock-rate lock

Criteria: `hy4_preview_push/OUT-2_kappa_ratelock/PREREGISTER.md`, committed **alone** before
`out2.py` or any number existed.

Scope, stated up front: **Lean certifies algebra, not physics and not data.** The lock equation
`a0 = c H_Lam / (2 pi)` is a *postulate* of this lane; what is certified is everything that follows
from it, and — the load-bearing part — that what follows is **not** the record's fitted
`kappa = 1/2`, and that the lock **breaks** the `G_lam` flat direction.

Chain:

```
(2)  H_Lam^2 = Lam c^2 / 3 ,  Lam = 8 pi G rho / c^2   ==>  H_Lam^2 = (8 pi / 3) G rho
(3)  1:1 lock:  a0^2 = c^2 H_Lam^2 / (4 pi^2)
(4)  kappa^2 := a0^2 / (c^2 G rho) = 2 / (3 pi)
(5)  kappa = sqrt(2/(3 pi)) = 0.460659 ,  and 2/5 < kappa < 1/2  (so kappa != 1/2)
```

Also certified: the winding family `kappa^2 = n^2 * 2/(3 pi)`; the circularity twin (the record
identity `a0^2/(8 pi G) = rho c^2/(32 pi)` is *equivalent to* `kappa^2 = 1/4`, so it may not be
used as an input); and the capacity fix (the lock equation is charged under `G_lam`).

`kappa = 1/2 FITTED; not theory closed.` Nothing here relabels it. Adopts nothing.
-/

namespace Out2RateLock

section RateLock

open Real

lemma pi_ne_zero : Real.pi ≠ 0 := ne_of_gt Real.pi_pos

/-- T1: the vacuum's own rate, from Einstein's equation `Lam = 8 pi G rho / c^2` alone.
    (This is the only place `8 pi` enters the chain, and it is Einstein's `8 pi`, not the
    record identity `a0^2/(8 pi G) = rho c^2/(32 pi)`.) -/
theorem vacuum_rate_sq {H Lam G rho c : ℝ} (hc : c ≠ 0)
    (hLam : Lam = 8 * Real.pi * G * rho / c ^ 2)
    (hH : H ^ 2 = Lam * c ^ 2 / 3) :
    H ^ 2 = (8 * Real.pi / 3) * G * rho := by
  rw [hLam] at hH
  rw [hH]
  field_simp [hc]

/-- T2 (the lane's output): the 1:1 lock gives `kappa^2 = 2/(3 pi)` exactly.
    No measured number enters; `kappa` is not fitted. -/
theorem kappaSq_from_lock {a0 H G rho c : ℝ} (hc : c ≠ 0) (hG : G ≠ 0) (hrho : rho ≠ 0)
    (hH : H ^ 2 = (8 * Real.pi / 3) * G * rho)
    (hlock : a0 ^ 2 = c ^ 2 * H ^ 2 / (4 * Real.pi ^ 2)) :
    a0 ^ 2 / (c ^ 2 * G * rho) = 2 / (3 * Real.pi) := by
  rw [hlock, hH]
  field_simp [hc, hG, hrho, pi_ne_zero]
  ring

/-- T3: the lock value is positive, so its square root is a real number. -/
theorem lock_kappaSq_pos : 0 < 2 / (3 * Real.pi) := by positivity

/-- T4 (G1, INDEPENDENCE): the lock does **not** restate `kappa = 1/2`.
    `2/(3 pi) != 1/4` because `3 pi > 9 > 8`. -/
theorem lock_kappaSq_ne_quarter : 2 / (3 * Real.pi) ≠ (1 : ℝ) / 4 := by
  intro h
  field_simp [pi_ne_zero] at h
  nlinarith [h, Real.pi_gt_three]

/-- T5: `kappa_lock < 1/2` (a strict inequality, stronger than T4). -/
theorem lock_kappa_lt_half : Real.sqrt (2 / (3 * Real.pi)) < (1 : ℝ) / 2 := by
  have hsq : 2 / (3 * Real.pi) < ((1 : ℝ) / 2) ^ 2 := by
    rw [show ((1 : ℝ) / 2) ^ 2 = 1 / 4 by norm_num]
    field_simp [pi_ne_zero]
    nlinarith [Real.pi_gt_three]
  have h := Real.sqrt_lt_sqrt (show 0 ≤ 2 / (3 * Real.pi) by positivity) hsq
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2)] at h
  exact h

/-- T6: `kappa_lock > 2/5`, so the output is bracketed by `0.4 < kappa < 0.5`. -/
theorem lock_kappa_gt_two_fifths : (2 : ℝ) / 5 < Real.sqrt (2 / (3 * Real.pi)) := by
  have hsq : ((2 : ℝ) / 5) ^ 2 < 2 / (3 * Real.pi) := by
    rw [show ((2 : ℝ) / 5) ^ 2 = 4 / 25 by norm_num]
    field_simp [pi_ne_zero]
    nlinarith [Real.pi_lt_four]
  have h := Real.sqrt_lt_sqrt (show 0 ≤ ((2 : ℝ) / 5) ^ 2 by positivity) hsq
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2 / 5)] at h
  exact h

/-- T7 (G2, THE CAPACITY FIX): the lock equation is **charged** under
    `G_lam : (a0, g) -> (lam*a0, lam*g)`. If both `a0` and `lam*a0` satisfy the lock, then
    `lam^2 = 1`. So the flat direction is removed: this is why the lane is a capacity fix and
    not "just another flat direction" (mutation arm MU6). -/
theorem lock_charged_under_Glambda {a0 c H lam : ℝ} (ha0 : a0 ≠ 0)
    (h1 : a0 ^ 2 = (c * H / (2 * Real.pi)) ^ 2)
    (h2 : (lam * a0) ^ 2 = (c * H / (2 * Real.pi)) ^ 2) :
    lam ^ 2 = 1 := by
  have hm : lam ^ 2 * a0 ^ 2 = 1 * a0 ^ 2 := by
    calc
      lam ^ 2 * a0 ^ 2 = (lam * a0) ^ 2 := by ring
      _ = (c * H / (2 * Real.pi)) ^ 2 := h2
      _ = a0 ^ 2 := h1.symm
      _ = 1 * a0 ^ 2 := by ring
  exact mul_right_cancel₀ (pow_ne_zero 2 ha0) hm

/-- T8: the winding family. An `n:1` lock gives `kappa^2 = n^2 * 2/(3 pi)`; the lane uses `n = 1`
    and mutation arms MU3 (`n = 2`) and MU7 (`n = 1/2`) are graded against it. -/
theorem kappaSq_from_lock_winding {a0 H G rho c n : ℝ} (hc : c ≠ 0) (hG : G ≠ 0) (hrho : rho ≠ 0)
    (hH : H ^ 2 = (8 * Real.pi / 3) * G * rho)
    (hlock : a0 ^ 2 = n ^ 2 * c ^ 2 * H ^ 2 / (4 * Real.pi ^ 2)) :
    a0 ^ 2 / (c ^ 2 * G * rho) = n ^ 2 * (2 / (3 * Real.pi)) := by
  rw [hlock, hH]
  field_simp [hc, hG, hrho, pi_ne_zero]
  ring

/-- T9 (MU5, CIRCULARITY TWIN): the record identity `a0^2/(8 pi G) = rho c^2/(32 pi)` is
    **equivalent to** `kappa^2 = 1/4`, i.e. to `kappa = 1/2`. Taking it as an input is taking
    the conclusion as an input; this lane does not use it (see T10/T11). -/
theorem identity_iff_kappaSq_quarter {a0 c G rho : ℝ} (hc : c ≠ 0) (hG : G ≠ 0) (hrho : rho ≠ 0) :
    a0 ^ 2 / (8 * Real.pi * G) = rho * c ^ 2 / (32 * Real.pi) ↔
    a0 ^ 2 / (c ^ 2 * G * rho) = (1 : ℝ) / 4 := by
  constructor
  · intro h
    field_simp [hc, hG, hrho, pi_ne_zero] at h ⊢
    nlinarith
  · intro h
    field_simp [hc, hG, hrho, pi_ne_zero] at h ⊢
    nlinarith

/-- T10 (G7): under the lock the `a0`-pressure is `rho c^2/(12 pi^2)`, **not** the record's
    `rho c^2/(32 pi)`. The chain uses `Lam = 8 pi G rho/c^2` only. -/
theorem lock_pressure {a0 c G rho : ℝ} (hG : G ≠ 0)
    (hlock : a0 ^ 2 = (2 / (3 * Real.pi)) * (c ^ 2 * G * rho)) :
    a0 ^ 2 / (8 * Real.pi * G) = rho * c ^ 2 / (12 * Real.pi ^ 2) := by
  rw [hlock]
  field_simp [hG, pi_ne_zero]
  ring

/-- T11: and `12 pi^2` is not `32 pi` (equivalently `3 pi != 8`), so T10 is genuinely a
    different statement from the record identity. -/
theorem twelve_pi_sq_ne_thirty_two_pi : (12 * Real.pi ^ 2 : ℝ) ≠ 32 * Real.pi := by
  intro h
  have h' : (3 * Real.pi : ℝ) = 8 := by
    have hm := congrArg (fun x : ℝ => x / (4 * Real.pi)) h
    field_simp [pi_ne_zero] at hm
    linarith
  nlinarith [h', Real.pi_gt_three]

/-- T12: the lock written as the rate ratio it is: `a0/c = H_Lam/(2 pi)`. -/
theorem lock_rate_ratio {a0 c H : ℝ} (hc : 0 < c) (ha0 : 0 < a0) (hH : 0 < H)
    (hlock : a0 ^ 2 = c ^ 2 * H ^ 2 / (4 * Real.pi ^ 2)) :
    a0 / c = H / (2 * Real.pi) := by
  have hsq : (a0 / c) ^ 2 = (H / (2 * Real.pi)) ^ 2 := by
    calc
      (a0 / c) ^ 2 = a0 ^ 2 / c ^ 2 := by ring
      _ = (c ^ 2 * H ^ 2 / (4 * Real.pi ^ 2)) / c ^ 2 := by rw [hlock]
      _ = H ^ 2 / (4 * Real.pi ^ 2) := by
        field_simp [ne_of_gt hc]
      _ = (H / (2 * Real.pi)) ^ 2 := by ring
  rcases sq_eq_sq_iff_eq_or_eq_neg.mp hsq with h | h
  · exact h
  · have hL : 0 ≤ a0 / c := by positivity
    have hRpos : 0 < H / (2 * Real.pi) := by positivity
    linarith

end RateLock

end Out2RateLock

-- Axiom exposure (the audit convention: the axiom set must be evidenced, not assumed).
#print axioms Out2RateLock.vacuum_rate_sq
#print axioms Out2RateLock.kappaSq_from_lock
#print axioms Out2RateLock.lock_kappaSq_pos
#print axioms Out2RateLock.lock_kappaSq_ne_quarter
#print axioms Out2RateLock.lock_kappa_lt_half
#print axioms Out2RateLock.lock_kappa_gt_two_fifths
#print axioms Out2RateLock.lock_charged_under_Glambda
#print axioms Out2RateLock.kappaSq_from_lock_winding
#print axioms Out2RateLock.identity_iff_kappaSq_quarter
#print axioms Out2RateLock.lock_pressure
#print axioms Out2RateLock.twelve_pi_sq_ne_thirty_two_pi
#print axioms Out2RateLock.lock_rate_ratio
