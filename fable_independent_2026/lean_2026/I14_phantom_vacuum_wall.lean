import Mathlib

/-!
# I14: exact statements for a specified Dirichlet difference form

The model is defined below, with lattice spacing one and real parameters
`kappa2`, `mu2` (their names do not impose nonnegativity). Under u 0 = u N = 0,
A = (3/2) D + (1/4) U. The factor 3/2 belongs to this forward-difference
prescription; it is not the continuum coefficient of the derivative term.

For constant q = q0 put b = 1/4 - kappa2 + mu2*q0. The energy is exactly
(3/2)D + b U. The new certificates prove that b is the best lower bound
uniformly over all finite boxes and nonzero Dirichlet modes. Thus positivity
on every box is equivalent to b >= 0. Negative b supplies negative modes in
sufficiently large boxes; b = 0 gives no positive uniform gap. Every fixed
finite box still has a strictly positive kinetic eigenvalue.

The elementary full diagonalization, with eigenvalues
6 sin^2(j*pi/(2N)) + b, 1 <= j < N, and its proof are recorded in
real_research/reviews/spectral_spine_closure_2026_09_22/i14/DERIVATION.md.
The Lean claims are exactly the declarations below; prose diagonalization
is not silently promoted to a full Lean spectral theorem.

With variable confinement q >= q0 and mu2 >= 0 the same b is a lower bound,
but need not be sharp for that fixed profile. In the unconfined case the
uniform threshold is kappa2 = 1/4. Positive confinement can move the threshold:
`confined_counterexample_to_universal_wall` certifies stability at
kappa2 = mu2 = q0 = 1. Stability alone never selects a unique coupling.

These are certificates for the defined quadratic form. Identifying this form
with a physical action's Hessian, identifying its parameter with the kappa in
a0 = kappa*c*sqrt(G*rho_Lambda), and supplying a confinement potential require
separate derivations. G155/G081/WAVEBOARD B8/THE_THEORY L5 do not supply those
identifications; the source-level obstruction is documented with the proof.
No Yang--Mills vacuum or quantum mass-gap assertion follows from this file.
-/
noncomputable section
open scoped Real
open scoped BigOperators

/-! ## 1. the sums of the t-lattice -/

/-- the kinetic-plus-radial term of the mode u on the box [0, N] -/
noncomputable def A (N : ℕ) (u : ℕ → ℝ) : ℝ :=
  ∑ n ∈ Finset.range N, (u (n + 1) - u n - u n / 2)^2

/-- the squared first differences -/
noncomputable def D (N : ℕ) (u : ℕ → ℝ) : ℝ :=
  ∑ n ∈ Finset.range N, (u (n + 1) - u n)^2

/-- the cross term -/
noncomputable def C (N : ℕ) (u : ℕ → ℝ) : ℝ :=
  ∑ n ∈ Finset.range N, (u (n + 1) - u n) * u n

/-- the mode norm -/
noncomputable def U (N : ℕ) (u : ℕ → ℝ) : ℝ :=
  ∑ n ∈ Finset.range N, (u n)^2

/-- the confined quadratic form: kinetic + radial, minus the kappa^2 term,
    plus the mu^2-weighted confinement -/
noncomputable def E (N : ℕ) (u : ℕ → ℝ) (kappa2 mu2 : ℝ) (q : ℕ → ℝ) : ℝ :=
  A N u - kappa2 * U N u + mu2 * (∑ n ∈ Finset.range N, q n * (u n)^2)

/-! ## 2. the Hardy-marginal identity -/

/-- the cross term is minus half the kinetic term (the telescoping identity) -/
theorem delta_dot_u (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0) :
    C N u = -(D N u) / 2 := by
  have htel : (∑ n ∈ Finset.range N, ((u (n + 1))^2 - (u n)^2)) = 0 := by
    have htel_raw := Finset.sum_range_sub (fun m : ℕ => (u m)^2) N
    change (∑ n ∈ Finset.range N,
      ((fun m : ℕ => (u m)^2) (n + 1) - (fun m : ℕ => (u m)^2) n)) = 0
    rw [htel_raw]
    simp [hu0, huN]
  have hpt : ∀ n ∈ Finset.range N,
      (u (n + 1) - u n)^2 = (u (n + 1))^2 - (u n)^2 - 2 * (u (n + 1) - u n) * u n := by
    intro n hn
    ring
  have hmain : D N u = -(2 * C N u) := by
    calc
      D N u = ∑ n ∈ Finset.range N, (u (n + 1) - u n)^2 := rfl
      _ = ∑ n ∈ Finset.range N, ((u (n + 1))^2 - (u n)^2 - 2 * (u (n + 1) - u n) * u n) :=
        Finset.sum_congr rfl hpt
      _ = -2 * (∑ n ∈ Finset.range N, (u (n + 1) - u n) * u n) := by
        rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib]
        rw [← Finset.sum_sub_distrib]
        rw [htel]
        have hpt2 : ∀ n ∈ Finset.range N,
            2 * (u (n + 1) - u n) * u n = 2 * ((u (n + 1) - u n) * u n) := by
          intro n hn
          ring
        rw [Finset.sum_congr rfl hpt2, ← Finset.mul_sum]
        ring
      _ = -(2 * C N u) := by
        unfold C
        ring
  have h2 : 2 * C N u = -(D N u) := by linarith [hmain]
  exact (eq_div_iff (by norm_num : (2 : ℝ) ≠ 0)).2 (by nlinarith)

/-- Exact square expansion for this forward-difference prescription.
    Its scalar shift cancels at kappa2 = 1/4. -/
theorem hardy_identity (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0) :
    A N u = (3 / 2) * D N u + (1 / 4) * U N u := by
  have hpt : ∀ n ∈ Finset.range N,
      (u (n + 1) - u n - u n / 2)^2 = (u (n + 1) - u n)^2 - (u (n + 1) - u n) * u n + (1 / 4) * (u n)^2 := by
    intro n hn
    ring
  have hC : C N u = -(D N u) / 2 := delta_dot_u N u hu0 huN
  calc
    A N u = ∑ n ∈ Finset.range N, (u (n + 1) - u n - u n / 2)^2 := rfl
    _ = ∑ n ∈ Finset.range N, ((u (n + 1) - u n)^2 - (u (n + 1) - u n) * u n + (1 / 4) * (u n)^2) :=
      Finset.sum_congr rfl hpt
    _ = D N u - C N u + (1 / 4) * U N u := by
      rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
      rw [← Finset.mul_sum]
      unfold D C U
      ring
    _ = (3 / 2) * D N u + (1 / 4) * U N u := by
      rw [hC]
      ring

/-- the kinetic term is nonnegative -/
theorem kinetic_nonneg (N : ℕ) (u : ℕ → ℝ) : 0 ≤ D N u := by
  unfold D
  exact Finset.sum_nonneg (by intro n hn; exact sq_nonneg _)

/-- the mode norm is nonnegative -/
theorem unorm_nonneg (N : ℕ) (u : ℕ → ℝ) : 0 ≤ U N u := by
  unfold U
  exact Finset.sum_nonneg (by intro n hn; exact sq_nonneg _)

/-! ## 3. the stability gap -/

/-- the confinement profile is bounded below pointwise -/
theorem qsum_lower (N : ℕ) (u : ℕ → ℝ) (q : ℕ → ℝ) (q0 : ℝ)
    (hq : ∀ n ∈ Finset.range N, q0 ≤ q n) :
    q0 * U N u ≤ ∑ n ∈ Finset.range N, (q n * (u n)^2) := by
  have hpt : ∀ n ∈ Finset.range N, q0 * (u n)^2 ≤ q n * (u n)^2 := by
    intro n hn
    exact mul_le_mul_of_nonneg_right (hq n hn) (sq_nonneg (u n))
  have hsum : (∑ n ∈ Finset.range N, q0 * (u n)^2) ≤ ∑ n ∈ Finset.range N, (q n * (u n)^2) :=
    Finset.sum_le_sum hpt
  simpa [U, Finset.mul_sum] using hsum

/-- Uniform lower bound for every real kappa2. It is a positive gap only
    when the displayed coefficient is positive. -/
theorem vacuum_gap (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0)
    (kappa2 mu2 q0 : ℝ) (hm2 : 0 ≤ mu2)
    (q : ℕ → ℝ) (hq : ∀ n ∈ Finset.range N, q0 ≤ q n) :
    E N u kappa2 mu2 q ≥ (1 / 4 - kappa2 + mu2 * q0) * U N u := by
  have hA : A N u ≥ (1 / 4) * U N u := by
    rw [hardy_identity N u hu0 huN]
    nlinarith [kinetic_nonneg N u]
  have hq' : q0 * U N u ≤ ∑ n ∈ Finset.range N, (q n * (u n)^2) :=
    qsum_lower N u q q0 hq
  have hmul : mu2 * q0 * U N u ≤ mu2 * (∑ n ∈ Finset.range N, (q n * (u n)^2)) := by
    calc
      mu2 * q0 * U N u = mu2 * (q0 * U N u) := by ring
      _ ≤ mu2 * ∑ n ∈ Finset.range N, (q n * (u n)^2) := mul_le_mul_of_nonneg_left hq' hm2
  unfold E
  nlinarith [hA, hmul]

/-- the unconfined vacuum: bounded below by the (1/4 - kappa^2) gap -/
theorem vacuum_gap_free (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0)
    (kappa2 : ℝ) :
    A N u - kappa2 * U N u ≥ (1 / 4 - kappa2) * U N u := by
  have hA : A N u ≥ (1 / 4) * U N u := by
    rw [hardy_identity N u hu0 huN]
    nlinarith [kinetic_nonneg N u]
  nlinarith

/-! ## 4. the marginal face: kappa^2 = 1/4 EXACTLY -/

/-- at the marginal coupling the radial term cancels IDENTICALLY: the form is
    kinetic plus confinement, nothing else -/
theorem marginal_identity (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0)
    (mu2 : ℝ) (q : ℕ → ℝ) :
    E N u (1 / 4) mu2 q = (3 / 2) * D N u + mu2 * (∑ n ∈ Finset.range N, q n * (u n)^2) := by
  unfold E
  rw [hardy_identity N u hu0 huN]
  ring

/-- At kappa2 = 1/4 the confinement supplies this uniform lower bound;
    the finite-box kinetic term also contributes positive energy. -/
theorem marginal_gap (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0)
    (mu2 q0 : ℝ) (hm2 : 0 ≤ mu2)
    (q : ℕ → ℝ) (hq : ∀ n ∈ Finset.range N, q0 ≤ q n) :
    E N u (1 / 4) mu2 q ≥ (mu2 * q0) * U N u := by
  rw [marginal_identity N u hu0 huN mu2 q]
  have hq' : q0 * U N u ≤ ∑ n ∈ Finset.range N, (q n * (u n)^2) :=
    qsum_lower N u q q0 hq
  have hmul : mu2 * q0 * U N u ≤ mu2 * (∑ n ∈ Finset.range N, (q n * (u n)^2)) := by
    calc
      mu2 * q0 * U N u = mu2 * (q0 * U N u) := by ring
      _ ≤ mu2 * ∑ n ∈ Finset.range N, (q n * (u n)^2) := mul_le_mul_of_nonneg_left hq' hm2
  nlinarith [kinetic_nonneg N u, hmul]

/-! ## 5. the pure face: no confinement, no gap -/

/-- the slab mode: 0 on the boundary, 1 inside -/
noncomputable def slab (N : ℕ) (n : ℕ) : ℝ := if n = 0 ∨ n = N then 0 else 1

/-- the slab satisfies the left Dirichlet boundary condition -/
theorem slab_bc0 : slab N 0 = 0 := by
  simp [slab]

/-- the slab satisfies the right Dirichlet boundary condition -/
theorem slab_bcN : slab N N = 0 := by
  simp [slab]

/-- the slab mode's norm: sum u^2 = N - 1 -/
theorem slab_norm (N : ℕ) (hN : 1 ≤ N) : U N (slab N) = (N : ℝ) - 1 := by
  have hpt : ∀ n ∈ Finset.range N, (slab N n)^2 = 1 - ite (n = 0) 1 0 := by
    intro n hn
    have hnN : n ≠ N := ne_of_lt (Finset.mem_range.mp hn)
    unfold slab
    by_cases hn0 : n = 0
    · subst n
      simp
    · simp [hn0, hnN]
  calc
    U N (slab N) = ∑ x ∈ Finset.range N, (slab N x)^2 := rfl
    _ = ∑ n ∈ Finset.range N, (1 - ite (n = 0) 1 0) := Finset.sum_congr rfl hpt
    _ = (∑ n ∈ Finset.range N, 1) - ∑ n ∈ Finset.range N, ite (n = 0) 1 0 := by
      rw [Finset.sum_sub_distrib]
    _ = (N : ℝ) - 1 := by
      have h0r : (0 : ℕ) ∈ Finset.range N := by
        exact Finset.mem_range.mpr (by omega)
      have hone : (∑ n ∈ Finset.range N, ite (n = 0) 1 0) = 1 := by
        rw [Finset.sum_eq_single 0]
        · simp
        · intro b hb hb0
          simp [hb0]
        · intro hmem
          exact False.elim (hmem h0r)
      rw [Finset.sum_const]
      have hN0 : N ≠ 0 := by omega
      simp [Finset.card_range, hN0]

/-- the slab mode's kinetic: sum (Delta u)^2 = 2 -- exactly the two boundary
    jumps, independent of the box size -/
theorem slab_diff (N : ℕ) (hN : 2 ≤ N) : D N (slab N) = 2 := by
  have hpt : ∀ n ∈ Finset.range N,
      (slab N (n + 1) - slab N n)^2 = ite (n = 0 ∨ n = N - 1) 1 0 := by
    intro n hn
    have hnN : n < N := Finset.mem_range.mp hn
    by_cases hn0 : n = 0
    · subst n
      have h1N : 1 ≠ N := by omega
      have h0N : 0 ≠ N := by omega
      have h01 : 0 ≠ N - 1 := by omega
      norm_num [slab, h1N, h0N, h01]
    · by_cases hnlast : n = N - 1
      · subst n
        have hsub : N - 1 + 1 = N := by omega
        have hN1 : N - 1 ≠ 0 := by omega
        have hNn : N - 1 ≠ N := by omega
        norm_num [slab, hsub, hN1, hNn]
      · have hnN' : n ≠ N := ne_of_lt hnN
        have hnpN : n + 1 ≠ N := by omega
        have hnp0 : n + 1 ≠ 0 := by omega
        have hnn1 : n ≠ N - 1 := hnlast
        norm_num [slab, hn0, hnN', hnpN, hnp0, hnn1]
  calc
    D N (slab N) = ∑ x ∈ Finset.range N, (slab N (x + 1) - slab N x)^2 := rfl
    _ = ∑ n ∈ Finset.range N, ite (n = 0 ∨ n = N - 1) 1 0 := Finset.sum_congr rfl hpt
    _ = ∑ n ∈ Finset.range N, (ite (n = 0) 1 0 + ite (n = N - 1) 1 0) := by
      apply Finset.sum_congr rfl
      intro n hn
      by_cases hn0 : n = 0
      · subst n
        have h01 : 0 ≠ N - 1 := by omega
        simp [h01]
      · by_cases hnN1 : n = N - 1
        · subst n
          have h10 : N - 1 ≠ 0 := by omega
          simp [h10]
        · simp [hn0, hnN1]
    _ = 2 := by
      have h0r : (0 : ℕ) ∈ Finset.range N := by
        exact Finset.mem_range.mpr (by omega)
      have hNr : N - 1 ∈ Finset.range N := by
        exact Finset.mem_range.mpr (by omega)
      have hone : (∑ n ∈ Finset.range N, ite (n = 0) 1 0) = 1 := by
        rw [Finset.sum_eq_single 0]
        · simp
        · intro b hb hb0
          simp [hb0]
        · intro hmem
          exact False.elim (hmem h0r)
      have hlast : (∑ n ∈ Finset.range N, ite (n = N - 1) 1 0) = 1 := by
        rw [Finset.sum_eq_single (N - 1)]
        · simp
        · intro b hb hb0
          simp [hb0]
        · intro hmem
          exact False.elim (hmem hNr)
      rw [Finset.sum_add_distrib]
      have h0N : 0 < N := by omega
      simp [h0N]
      norm_num

/-- the free marginal slab: E = 3 exactly, whatever the box size -/
theorem free_marginal_energy (N : ℕ) (hN : 2 ≤ N) :
    E N (slab N) (1 / 4) 0 (fun _ => 0) = 3 := by
  have hmi := marginal_identity N (slab N) (slab_bc0) (slab_bcN) 0 (fun _ => 0)
  have hd := slab_diff N hN
  rw [hd] at hmi
  simpa [one_div] using hmi

/-- At the unconfined critical coupling slab Rayleigh quotients approach
    zero as box size grows. This does not exhibit a zero mode on a fixed box. -/
theorem free_gap_closes (eps : ℝ) (heps : 0 < eps) :
    ∃ N : ℕ, ∃ u : ℕ → ℝ, u 0 = 0 ∧ u N = 0 ∧
      E N u (1 / 4) 0 (fun _ => 0) = 3 ∧ 3 / (((N : ℝ)) - 1) < eps := by
  rcases exists_nat_gt (3 / eps + 1) with ⟨N, hN⟩
  refine ⟨N, slab N, slab_bc0, slab_bcN, ?_, ?_⟩
  · exact free_marginal_energy N (by
      have he3 : 0 < 3 / eps := by positivity
      have h1 : (1 : ℝ) < (N : ℝ) := by nlinarith [hN, he3]
      have h1n : 1 < N := by exact_mod_cast h1
      omega)
  · have hNgt : 3 / eps < (N : ℝ) - 1 := by nlinarith [hN]
    have hnn : 0 < (N : ℝ) - 1 := by
      have he3 : 0 < 3 / eps := by positivity
      nlinarith [hN, he3]
    have hnz : (N : ℝ) - 1 ≠ 0 := ne_of_gt hnn
    have hm : 3 < eps * ((N : ℝ) - 1) := by
      have h := mul_lt_mul_of_pos_left hNgt heps
      have hcancel : eps * (3 / eps) = 3 := by
        field_simp [ne_of_gt heps]
      rwa [hcancel] at h
    have hm' : (3 / ((N : ℝ) - 1)) * ((N : ℝ) - 1) < eps * ((N : ℝ) - 1) := by
      rwa [← div_mul_cancel₀ 3 hnz] at hm
    exact lt_of_mul_lt_mul_right hm' (le_of_lt hnn)

/-! ## 6. the wall -/

/-- Nonnegativity for the unconfined form on every finite Dirichlet box. -/
theorem stability_boundary (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0)
    (kappa2 : ℝ) (hk1 : kappa2 ≤ 1 / 4) :
    0 ≤ A N u - kappa2 * U N u := by
  have hgap := vacuum_gap_free N u hu0 huN kappa2
  have hk : 0 ≤ 1 / 4 - kappa2 := by linarith
  have hU : 0 ≤ U N u := unorm_nonneg N u
  have hmul : 0 ≤ (1 / 4 - kappa2) * U N u := mul_nonneg hk hU
  nlinarith [hgap, hmul]

/-- For the unconfined form and every kappa2 > 1/4 there exists a negative
    mode in a sufficiently large box. The slab is one at indices 1,...,N-1.
    This is an existential box statement, not instability of every finite
    box or of a positively confined form. -/
theorem beyond_the_wall (kappa2 : ℝ) (hk : 1 / 4 < kappa2) :
    ∃ N : ℕ, ∃ u : ℕ → ℝ, u 0 = 0 ∧ u N = 0 ∧ A N u - kappa2 * U N u < 0 := by
  let eps : ℝ := kappa2 - 1 / 4
  have heps : 0 < eps := by
    dsimp [eps]
    linarith
  rcases exists_nat_gt (1 + 3 / eps) with ⟨N, hN⟩
  refine ⟨N, slab N, slab_bc0, slab_bcN, ?_⟩
  have hk2 : 1 / 4 + eps = kappa2 := by
    dsimp [eps]
    ring
  have hE : A N (slab N) - (1 / 4 + eps) * U N (slab N) = 3 - eps * ((N : ℝ) - 1) := by
    rw [hardy_identity N (slab N) slab_bc0 slab_bcN]
    have hd : D N (slab N) = 2 := slab_diff N (by
      have he3 : 0 < 3 / eps := by positivity
      have h1 : (1 : ℝ) < (N : ℝ) := by nlinarith [hN, he3]
      have h1n : 1 < N := by exact_mod_cast h1
      omega)
    have hu : U N (slab N) = (N : ℝ) - 1 := slab_norm N (by
      have he3 : 0 < 3 / eps := by positivity
      have h1 : (1 : ℝ) < (N : ℝ) := by nlinarith [hN, he3]
      have h1n : 1 < N := by exact_mod_cast h1
      exact le_of_lt h1n)
    rw [hd, hu]
    ring
  have hlt : 3 - eps * ((N : ℝ) - 1) < 0 := by
    have hN1 : 3 / eps < (N : ℝ) - 1 := by nlinarith [hN]
    have hm : 3 < eps * ((N : ℝ) - 1) := by
      have h := mul_lt_mul_of_pos_left hN1 heps
      have hcancel : eps * (3 / eps) = 3 := by field_simp [ne_of_gt heps]
      rwa [hcancel] at h
    linarith
  rw [← hk2, hE]
  exact hlt

/-! ## 7. Sharp uniform threshold with constant confinement -/

/-- Exact constant-confinement reduction, with no sign restrictions. -/
theorem constant_confinement_identity (N : ℕ) (u : ℕ → ℝ)
    (hu0 : u 0 = 0) (huN : u N = 0) (kappa2 mu2 q0 : ℝ) :
    E N u kappa2 mu2 (fun _ => q0) =
      (3 / 2) * D N u + (1 / 4 - kappa2 + mu2 * q0) * U N u := by
  unfold E
  rw [hardy_identity N u hu0 huN, ← Finset.mul_sum]
  unfold U
  ring

/-- The constant-confinement floor holds for arbitrary real parameters. -/
theorem constant_confinement_floor (N : ℕ) (u : ℕ → ℝ)
    (hu0 : u 0 = 0) (huN : u N = 0) (kappa2 mu2 q0 : ℝ) :
    (1 / 4 - kappa2 + mu2 * q0) * U N u ≤
      E N u kappa2 mu2 (fun _ => q0) := by
  rw [constant_confinement_identity N u hu0 huN]
  nlinarith [kinetic_nonneg N u]

/-- The slab's exact confined energy. -/
theorem constant_slab_energy (N : ℕ) (hN : 2 ≤ N) (kappa2 mu2 q0 : ℝ) :
    E N (slab N) kappa2 mu2 (fun _ => q0) =
      3 + (1 / 4 - kappa2 + mu2 * q0) * ((N : ℝ) - 1) := by
  rw [constant_confinement_identity N (slab N) slab_bc0 slab_bcN,
    slab_diff N hN, slab_norm N (by omega)]
  ring

/-- Sharpness of the uniform floor: nonzero Dirichlet slabs approach it
    within any positive epsilon, expressed without a quotient. -/
theorem constant_floor_sharp (kappa2 mu2 q0 eps : ℝ) (heps : 0 < eps) :
    ∃ N : ℕ, ∃ u : ℕ → ℝ, u 0 = 0 ∧ u N = 0 ∧ 0 < U N u ∧
      E N u kappa2 mu2 (fun _ => q0) <
        (1 / 4 - kappa2 + mu2 * q0 + eps) * U N u := by
  rcases exists_nat_gt (1 + 3 / eps) with ⟨N, hN⟩
  have he3 : 0 < 3 / eps := by positivity
  have hreal : (1 : ℝ) < N := by linarith
  have hnat : 2 ≤ N := by exact_mod_cast hreal
  have hnorm : U N (slab N) = (N : ℝ) - 1 := slab_norm N (by omega)
  refine ⟨N, slab N, slab_bc0, slab_bcN, ?_, ?_⟩
  · rw [hnorm]
    linarith
  · rw [constant_slab_energy N hnat, hnorm]
    have hlarge : 3 / eps < (N : ℝ) - 1 := by linarith
    have hmul := (div_lt_iff₀ heps).mp hlarge
    nlinarith

/-- Exact best uniform lower bound over all finite Dirichlet boxes.
    This pins every quantifier needed for the infinite-box threshold. -/
theorem constant_uniform_floor_iff (kappa2 mu2 q0 gamma : ℝ) :
    (∀ (N : ℕ) (u : ℕ → ℝ), u 0 = 0 → u N = 0 →
      gamma * U N u ≤ E N u kappa2 mu2 (fun _ => q0)) ↔
        gamma ≤ 1 / 4 - kappa2 + mu2 * q0 := by
  constructor
  · intro h
    by_contra hnot
    have hgt : 0 < gamma - (1 / 4 - kappa2 + mu2 * q0) := by linarith
    obtain ⟨N, u, hu0, huN, _, hlt⟩ :=
      constant_floor_sharp kappa2 mu2 q0 _ hgt
    have hlo := h N u hu0 huN
    nlinarith
  · intro h N u hu0 huN
    exact le_trans (mul_le_mul_of_nonneg_right h (unorm_nonneg N u))
      (constant_confinement_floor N u hu0 huN kappa2 mu2 q0)

/-- Positivity on every box is equivalent to the shifted wall. -/
theorem constant_all_boxes_nonneg_iff (kappa2 mu2 q0 : ℝ) :
    (∀ (N : ℕ) (u : ℕ → ℝ), u 0 = 0 → u N = 0 →
      0 ≤ E N u kappa2 mu2 (fun _ => q0)) ↔
        kappa2 ≤ 1 / 4 + mu2 * q0 := by
  have h := constant_uniform_floor_iff kappa2 mu2 q0 0
  simp only [zero_mul] at h
  constructor
  · intro hn
    have hb := h.mp hn
    linarith
  · intro hk
    apply h.mpr
    linarith

/-- Explicit existential instability beyond the confined wall. -/
theorem confined_beyond_wall (kappa2 mu2 q0 : ℝ)
    (hk : 1 / 4 + mu2 * q0 < kappa2) :
    ∃ N : ℕ, ∃ u : ℕ → ℝ, u 0 = 0 ∧ u N = 0 ∧ 0 < U N u ∧
      E N u kappa2 mu2 (fun _ => q0) < 0 := by
  have heps : 0 < kappa2 - (1 / 4 + mu2 * q0) := by linarith
  obtain ⟨N, u, hu0, huN, hnorm, hlt⟩ :=
    constant_floor_sharp kappa2 mu2 q0 _ heps
  refine ⟨N, u, hu0, huN, hnorm, ?_⟩
  nlinarith

/-- At the shifted critical coupling there is no positive gap uniform
    in box size, including when confinement is nonzero. -/
theorem confined_critical_gap_closes (mu2 q0 eps : ℝ) (heps : 0 < eps) :
    ∃ N : ℕ, ∃ u : ℕ → ℝ, u 0 = 0 ∧ u N = 0 ∧ 0 < U N u ∧
      0 ≤ E N u (1 / 4 + mu2 * q0) mu2 (fun _ => q0) ∧
      E N u (1 / 4 + mu2 * q0) mu2 (fun _ => q0) < eps * U N u := by
  obtain ⟨N, u, hu0, huN, hnorm, hlt⟩ :=
    constant_floor_sharp (1 / 4 + mu2 * q0) mu2 q0 eps heps
  have hlo := constant_confinement_floor N u hu0 huN (1 / 4 + mu2 * q0) mu2 q0
  refine ⟨N, u, hu0, huN, hnorm, ?_, ?_⟩ <;> nlinarith

/-- A uniform positive gap at kappa2 = 1 > 1/4 refutes any universal
    claim that confinement cannot stabilize couplings beyond 1/2. -/
theorem confined_counterexample_to_universal_wall (N : ℕ) (u : ℕ → ℝ)
    (hu0 : u 0 = 0) (huN : u N = 0) :
    (1 / 4) * U N u ≤ E N u 1 1 (fun _ => 1) := by
  have h := constant_confinement_floor N u hu0 huN 1 1 1
  norm_num at h ⊢
  exact h

/-! ## 8. Finite-box strictness and the sine eigenmode equation -/

/-- A nonzero mode with a zero left endpoint has positive kinetic energy
    on its finite box. Thus a vanishing uniform gap is not a finite-box
    zero eigenvalue. -/
theorem kinetic_pos_of_norm_pos (N : ℕ) (u : ℕ → ℝ)
    (hu0 : u 0 = 0) (hnorm : 0 < U N u) : 0 < D N u := by
  by_contra hnot
  have hzero : D N u = 0 := le_antisymm (le_of_not_gt hnot) (kinetic_nonneg N u)
  have hdiff : ∀ n ∈ Finset.range N, (u (n + 1) - u n)^2 = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg (fun n _ => sq_nonneg (u (n + 1) - u n))).mp hzero
  have hvanish : ∀ n, n ≤ N → u n = 0 := by
    intro n
    induction n with
    | zero => intro _; exact hu0
    | succ n ih =>
      intro hn
      have heq := hdiff n (Finset.mem_range.mpr (by omega))
      have hi := ih (by omega)
      nlinarith [sq_nonneg (u (n + 1) - u n)]
  have hnzero : U N u = 0 := by
    unfold U
    apply Finset.sum_eq_zero
    intro n hn
    rw [hvanish n (by have := Finset.mem_range.mp hn; omega)]
    norm_num
  linarith

/-- At the shifted critical coupling every nonzero finite-box mode has
    strictly positive energy, despite the lack of a uniform box-size gap. -/
theorem confined_critical_finite_pos (N : ℕ) (u : ℕ → ℝ)
    (hu0 : u 0 = 0) (huN : u N = 0) (hnorm : 0 < U N u) (mu2 q0 : ℝ) :
    0 < E N u (1 / 4 + mu2 * q0) mu2 (fun _ => q0) := by
  rw [constant_confinement_identity N u hu0 huN]
  nlinarith [kinetic_pos_of_norm_pos N u hu0 hnorm]

/-- Sine eigenmode on the box, extended by the same formula outside it. -/
noncomputable def sine_mode (N j n : ℕ) : ℝ :=
  Real.sin ((n : ℝ) * ((j : ℝ) * Real.pi / N))

theorem sine_mode_left (N j : ℕ) : sine_mode N j 0 = 0 := by
  simp [sine_mode]

theorem sine_mode_right (N j : ℕ) (hN : 0 < N) : sine_mode N j N = 0 := by
  have hN0 : (N : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hN)
  unfold sine_mode
  have ha : (N : ℝ) * ((j : ℝ) * Real.pi / N) = (j : ℝ) * Real.pi := by
    field_simp
  rw [ha, Real.sin_nat_mul_pi]

/-- Exact local eigenmode recurrence of the Dirichlet second difference. -/
theorem sine_mode_recurrence (N j n : ℕ) :
    2 * sine_mode N j (n + 1) - sine_mode N j n - sine_mode N j (n + 2) =
      4 * Real.sin (((j : ℝ) * Real.pi / N) / 2)^2 * sine_mode N j (n + 1) := by
  let t : ℝ := (j : ℝ) * Real.pi / N
  have hm : (n : ℝ) * t = ((n : ℝ) + 1) * t - t := by ring
  have hp : ((n : ℝ) + 2) * t = ((n : ℝ) + 1) * t + t := by ring
  change 2 * Real.sin (((n + 1 : ℕ) : ℝ) * t) - Real.sin ((n : ℝ) * t) -
    Real.sin (((n + 2 : ℕ) : ℝ) * t) =
      4 * Real.sin (t / 2)^2 * Real.sin (((n + 1 : ℕ) : ℝ) * t)
  push_cast
  rw [hm, hp, Real.sin_sub, Real.sin_add]
  have hs := Real.sin_sq_eq_half_sub (t / 2)
  have ht : 2 * (t / 2) = t := by ring
  rw [ht] at hs
  rw [hs]
  ring

/-- Discrete summation by parts with both boundary contributions zero. -/
theorem dirichlet_green_identity (N : ℕ) (u : ℕ → ℝ)
    (hu0 : u 0 = 0) (huN : u N = 0) :
    D N u = ∑ n ∈ Finset.range N, u n * (2 * u n - u (n - 1) - u (n + 1)) := by
  let f : ℕ → ℝ := fun n => u n * (u n - u (n - 1))
  have hs := Finset.sum_range_succ' f N
  rw [Finset.sum_range_succ] at hs
  have hshift : (∑ n ∈ Finset.range N, u (n + 1) * (u (n + 1) - u n)) =
      ∑ n ∈ Finset.range N, u n * (u n - u (n - 1)) := by
    simpa [f, hu0, huN] using hs.symm
  calc
    D N u = ∑ n ∈ Finset.range N,
        (u (n + 1) * (u (n + 1) - u n) - u n * (u (n + 1) - u n)) := by
      unfold D
      apply Finset.sum_congr rfl
      intro n _
      ring
    _ = (∑ n ∈ Finset.range N, u n * (u n - u (n - 1))) -
        ∑ n ∈ Finset.range N, u n * (u (n + 1) - u n) := by
      rw [Finset.sum_sub_distrib, hshift]
    _ = _ := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro n _
      ring

/-- The sine mode has the exact quadratic-form eigenvalue. Completeness
    of these modes is proved separately in the accompanying derivation. -/
theorem sine_mode_energy (N j : ℕ) (hN : 0 < N) (kappa2 mu2 q0 : ℝ) :
    E N (sine_mode N j) kappa2 mu2 (fun _ => q0) =
      (6 * Real.sin (((j : ℝ) * Real.pi / N) / 2)^2 +
        1 / 4 - kappa2 + mu2 * q0) * U N (sine_mode N j) := by
  have hD : D N (sine_mode N j) =
      (4 * Real.sin (((j : ℝ) * Real.pi / N) / 2)^2) * U N (sine_mode N j) := by
    rw [dirichlet_green_identity N (sine_mode N j) (sine_mode_left N j)
      (sine_mode_right N j hN)]
    unfold U
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro n _
    by_cases hn : n = 0
    · subst n
      simp [sine_mode_left]
    · obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero hn
      have hr := sine_mode_recurrence N j k
      simp only [Nat.succ_eq_add_one, Nat.add_sub_cancel] at *
      rw [show k + 1 + 1 = k + 2 by omega]
      rw [hr]
      ring
  rw [constant_confinement_identity N (sine_mode N j) (sine_mode_left N j)
    (sine_mode_right N j hN), hD]
  ring

/-- Exactly the indices 1 <= j < N are needed for these nonzero modes. -/
theorem sine_mode_norm_pos (N j : ℕ) (hj0 : 0 < j) (hjN : j < N) :
    0 < U N (sine_mode N j) := by
  have hN : 0 < (N : ℝ) := by exact_mod_cast (lt_trans hj0 hjN)
  have hj : 0 < (j : ℝ) := by exact_mod_cast hj0
  have hjlt : (j : ℝ) < N := by exact_mod_cast hjN
  have ht0 : 0 < (j : ℝ) * Real.pi / N := by positivity
  have htpi : (j : ℝ) * Real.pi / N < Real.pi := by
    apply (div_lt_iff₀ hN).mpr
    nlinarith [Real.pi_pos]
  unfold U
  apply Finset.sum_pos' (fun n _ => sq_nonneg _)
  refine ⟨1, Finset.mem_range.mpr (by omega), ?_⟩
  have hsin := Real.sin_pos_of_pos_of_lt_pi ht0 htpi
  simpa [sine_mode] using sq_pos_of_pos hsin

/-! ## 9. the certificate record -/

#print axioms delta_dot_u
#print axioms beyond_the_wall
#print axioms hardy_identity
#print axioms vacuum_gap
#print axioms vacuum_gap_free
#print axioms marginal_identity
#print axioms marginal_gap
#print axioms slab_norm
#print axioms slab_diff
#print axioms free_marginal_energy
#print axioms free_gap_closes
#print axioms stability_boundary
#print axioms constant_confinement_identity
#print axioms constant_confinement_floor
#print axioms constant_slab_energy
#print axioms constant_floor_sharp
#print axioms constant_uniform_floor_iff
#print axioms constant_all_boxes_nonneg_iff
#print axioms confined_beyond_wall
#print axioms confined_critical_gap_closes
#print axioms confined_counterexample_to_universal_wall
#print axioms kinetic_pos_of_norm_pos
#print axioms confined_critical_finite_pos
#print axioms sine_mode_left
#print axioms sine_mode_right
#print axioms sine_mode_recurrence
#print axioms dirichlet_green_identity
#print axioms sine_mode_energy
#print axioms sine_mode_norm_pos
