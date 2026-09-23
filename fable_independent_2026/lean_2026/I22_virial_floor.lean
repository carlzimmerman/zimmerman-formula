import Mathlib

/-!
# I22 — The virial floor: every isolated spherical system obeys ⟨v²⟩ ≥ (2/3)√(G M a0)

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs, stated as hypotheses:
(i) spherical shells with enclosed masses M_i = m_1 + … + m_i and the framework's acceleration floor
g_i ≥ √(G M_i a0)/r_i (i.e. g ≥ √(g_N a0), which holds for the RAR kernel and any μ(x) ≤ x: Lean I20);
(ii) the scalar virial theorem of an isolated equilibrium system, 2K = Σ m_i r_i g_i.
Companion lane: `real_research/virial_floor_2026/L328_virial_floor_highz.py`.

* `step_32` — for 0 ≤ a ≤ b: b√b − a√a ≤ (3/2)(b − a)√b  (the difference is ½(√b − √a)²(√b + 2√a)).
* `shell_sum_floor` — Σ_{i<n} m_i √(M_{i+1}) ≥ (2/3) M_n √M_n for any nonnegative shell masses.
* `virial_floor` — Σ m_i r_i g_i ≥ (2/3) √(G a0) M √M: the kinetic energy of ANY isolated spherical system in the
  framework is at least that of the deep-MOND virial relation — Milgrom's equality ⟨v²⟩² = (4/9) G M a0 is the
  deep-MOND EQUALITY case; here it is a LOWER BOUND at every acceleration.
* `sigma_floor` — with σ² = ⟨v²⟩/3 (the orientation-averaged line-of-sight dispersion): σ⁴ ≥ (4/81) G M a0.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

open Finset

theorem step_32 {a b : ℝ} (ha : 0 ≤ a) (hab : a ≤ b) :
    b * Real.sqrt b - a * Real.sqrt a ≤ 3 / 2 * (b - a) * Real.sqrt b := by
  set s := Real.sqrt a with hs
  set t := Real.sqrt b with ht
  have hs0 : 0 ≤ s := Real.sqrt_nonneg a
  have ht0 : 0 ≤ t := Real.sqrt_nonneg b
  have hsa : s ^ 2 = a := Real.sq_sqrt ha
  have htb : t ^ 2 = b := Real.sq_sqrt (le_trans ha hab)
  rw [← hsa, ← htb]
  nlinarith [mul_nonneg (sq_nonneg (t - s)) (by linarith : (0 : ℝ) ≤ t + 2 * s)]

/-- Enclosed mass after the first k shells. -/
noncomputable def Mc (m : ℕ → ℝ) (k : ℕ) : ℝ := ∑ i ∈ range k, m i

theorem shell_sum_floor (m : ℕ → ℝ) (hm : ∀ i, 0 ≤ m i) (n : ℕ) :
    2 / 3 * (Mc m n * Real.sqrt (Mc m n)) ≤ ∑ i ∈ range n, m i * Real.sqrt (Mc m (i + 1)) := by
  induction n with
  | zero => simp [Mc]
  | succ n ih =>
    rw [sum_range_succ]
    have ha : 0 ≤ Mc m n := sum_nonneg (fun i _ => hm i)
    have hb : Mc m (n + 1) = Mc m n + m n := by unfold Mc; rw [sum_range_succ]
    have hab : Mc m n ≤ Mc m (n + 1) := by rw [hb]; linarith [hm n]
    have hstep := step_32 ha hab
    have : m n = Mc m (n + 1) - Mc m n := by rw [hb]; ring
    rw [this] at *
    nlinarith [hstep, ih]

/-- The virial floor: Σ m_i r_i g_i ≥ (2/3)√(G a0) M √M, given g_i ≥ √(G a0 M_{i+1})/r_i. -/
theorem virial_floor (m r g : ℕ → ℝ) (G a0 : ℝ) (hG : 0 < G) (ha0 : 0 < a0) (hm : ∀ i, 0 ≤ m i)
    (hr : ∀ i, 0 < r i) (hfloor : ∀ i, Real.sqrt (G * a0 * Mc m (i + 1)) / r i ≤ g i) (n : ℕ) :
    2 / 3 * Real.sqrt (G * a0) * (Mc m n * Real.sqrt (Mc m n)) ≤ ∑ i ∈ range n, m i * r i * g i := by
  have hGa : 0 ≤ G * a0 := by positivity
  have hterm : ∀ i ∈ range n, Real.sqrt (G * a0) * (m i * Real.sqrt (Mc m (i + 1))) ≤ m i * r i * g i := by
    intro i _
    have hM : 0 ≤ Mc m (i + 1) := sum_nonneg (fun k _ => hm k)
    have h1 : Real.sqrt (G * a0 * Mc m (i + 1)) = Real.sqrt (G * a0) * Real.sqrt (Mc m (i + 1)) :=
      Real.sqrt_mul hGa _
    have h2 : Real.sqrt (G * a0 * Mc m (i + 1)) ≤ r i * g i :=
      calc Real.sqrt (G * a0 * Mc m (i + 1)) ≤ g i * r i := (div_le_iff₀ (hr i)).mp (hfloor i)
        _ = r i * g i := mul_comm _ _
    calc Real.sqrt (G * a0) * (m i * Real.sqrt (Mc m (i + 1)))
        = m i * Real.sqrt (G * a0 * Mc m (i + 1)) := by rw [h1]; ring
      _ ≤ m i * (r i * g i) := mul_le_mul_of_nonneg_left h2 (hm i)
      _ = m i * r i * g i := by ring
  calc 2 / 3 * Real.sqrt (G * a0) * (Mc m n * Real.sqrt (Mc m n))
      = Real.sqrt (G * a0) * (2 / 3 * (Mc m n * Real.sqrt (Mc m n))) := by ring
    _ ≤ Real.sqrt (G * a0) * ∑ i ∈ range n, m i * Real.sqrt (Mc m (i + 1)) :=
        mul_le_mul_of_nonneg_left (shell_sum_floor m hm n) (Real.sqrt_nonneg _)
    _ = ∑ i ∈ range n, Real.sqrt (G * a0) * (m i * Real.sqrt (Mc m (i + 1))) := by rw [mul_sum]
    _ ≤ ∑ i ∈ range n, m i * r i * g i := sum_le_sum hterm

/-- σ⁴ ≥ (4/81) G M a0, from ⟨v²⟩ ≥ (2/3)√(G M a0) and σ² = ⟨v²⟩/3. -/
theorem sigma_floor {G M a0 v2 σ : ℝ} (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0)
    (hv : 2 / 3 * Real.sqrt (G * M * a0) ≤ v2) (hσ : σ ^ 2 = v2 / 3) :
    4 / 81 * (G * M * a0) ≤ σ ^ 4 := by
  have hs : 0 ≤ Real.sqrt (G * M * a0) := Real.sqrt_nonneg _
  have hsq : Real.sqrt (G * M * a0) ^ 2 = G * M * a0 := Real.sq_sqrt (by positivity)
  have hσ2 : 2 / 9 * Real.sqrt (G * M * a0) ≤ σ ^ 2 := by rw [hσ]; linarith
  have h4 : σ ^ 4 = (σ ^ 2) ^ 2 := by ring
  rw [h4]
  have : (2 / 9 * Real.sqrt (G * M * a0)) ^ 2 ≤ (σ ^ 2) ^ 2 :=
    pow_le_pow_left₀ (by positivity) hσ2 2
  nlinarith [this, hsq]

#print axioms step_32
#print axioms shell_sum_floor
#print axioms virial_floor
#print axioms sigma_floor
