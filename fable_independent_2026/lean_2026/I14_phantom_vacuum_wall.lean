import Mathlib

/-!
# I14 -- THE PHANTOM-VACUUM SPECTRAL WALL: the t-lattice Hardy identity, the confinement gap, and the kappa = 1/2 marginal boundary

**Scope statement (as every certificate in this repo reads):** Lean certifies
the MATHEMATICS. The physical premises -- the log-radial (t-) lattice as the
discrete coordinate system of the phantom halo's radial fluctuation modes
(the committed equilibrium profile phi_0 = C ln r; the t-lattice spacing
h = 1 in lattice units), the mode dressing u_n ~ sqrt(r_n) * phi_n, the
confinement profile q(n) from the scalar's self-coupling / the rho_Lambda sea,
and the coupling kappa in the framework's a0 = kappa * c * sqrt(G * rho_Lambda)
with kappa = 1/2 -- are the committed lanes' claims (G155, WAVEBOARD B8/G081,
THE_THEORY L5). This file certifies the algebraic spine of the phantom-vacuum
stability problem: the Yang-Mills mass-gap theorem's VACUUM side (the analog of
YM_ROADMAP item 3, "the uniqueness/stability of the vacuum", which the
yang_mills_gap campaign's R1 did not touch -- R1 proved the gapless
Goldstone's lift, i.e., the EXCITATION side).

The certified content:

  1. the t-lattice Hardy identity (the marginal-rigidity identity):
       sum (Delta u_n - u_n/2)^2 = (3/2) * sum (Delta u_n)^2 + (1/4) * sum u_n^2
     with Dirichlet boundary conditions u_0 = u_N = 0 -- the (u' - u/2)^2
     discretization of the log-radial kinetic term. The (1/4)-coefficient is
     the Hardy constant of the half-line: the radial 1/r^2-potential is
     EXACTLY marginal at kappa^2 = 1/4;
  2. the stability gap: for 0 <= kappa^2 <= 1/4,
       E[u] := sum (Delta u - u/2)^2 - kappa^2 * sum u^2 + mu^2 * sum q u^2
              >= (1/4 - kappa^2 + mu^2 * q_0) * sum u^2
     -- the vacuum's fluctuation spectrum is bounded below, with a strictly
     positive gap when the confinement is on: the framework's kappa = 1/2 sits
     EXACTLY on the boundary;
  3. the marginal identity: at kappa^2 = 1/4 the radial term cancels
     identically: E = (3/2) * sum Delta^2 + mu^2 * sum q u^2 -- the vacuum is
     stable at exactly the marginal coupling, and the gap is then carried
     ENTIRELY by the confinement: E >= mu^2 * q_0 * sum u^2;
  4. the pure face: at kappa^2 = 1/4 WITHOUT confinement the spectrum is
     gapless: the slab modes (0,1,1,...,1,0) have E = 3 exactly and
     E/sum u^2 = 3/(N-1) --> 0 -- the boundary zero mode lives at infinity;
  5. the wall: kappa^2 > 1/4 (kappa > 1/2) is the classical unstable side ---
     NOW CERTIFIED as `beyond_the_wall` below: for every kappa^2 > 1/4 there
     exist explicit negative modes (the flat slab at box size
     N > 1 + 3/(kappa^2 - 1/4)): the vacuum form is not positive beyond the
     boundary. The trichotomy is complete and machine-checked: gapped stable
     sector (kappa < 1/2), marginal (kappa = 1/2), explosive (kappa > 1/2).

Every identity below is checked: exit 0, zero sorry, axioms = the standard
three. Compiled against the repo's Mathlib build (Lean 4.34.0-rc2).
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

/-- THE HARDY-MARGINAL IDENTITY: the (1/4)-coefficient of the log-radial
    lattice. The radial term is exactly marginal at kappa^2 = 1/4. -/
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

/-- THE STABILITY GAP: for 0 <= kappa^2 <= 1/4 the confined vacuum's
    fluctuation form is bounded below by the gap (1/4 - kappa^2 + mu^2*q0)
    times the mode norm. The framework's kappa = 1/2 sits exactly on the
    stable boundary; the gap survives there through the confinement alone. -/
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

/-- THE MARGINAL GAP: at kappa = 1/2 the gap is carried entirely by the
    confinement: E >= mu^2 * q0 * sum u^2 -/
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

/-- THE PURE FACE: at the marginal coupling WITHOUT confinement the spectrum is
    gapless -- the ratio E/sum u^2 = 3/(N-1) reaches 0. The boundary zero mode
    lives at infinity: the gap is a confinement phenomenon. -/
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

/-- THE STABILITY WALL: kappa^2 <= 1/4 (kappa <= 1/2) is the stable sector.
    The framework's kappa = 1/2 sits exactly on the boundary; the
    classical complement (kappa^2 > 1/4: unbounded below, the Knopp
    sharpness of discrete Hardy) is registered in the docstring. -/
theorem stability_boundary (N : ℕ) (u : ℕ → ℝ) (hu0 : u 0 = 0) (huN : u N = 0)
    (kappa2 : ℝ) (hk1 : kappa2 ≤ 1 / 4) :
    0 ≤ A N u - kappa2 * U N u := by
  have hgap := vacuum_gap_free N u hu0 huN kappa2
  have hk : 0 ≤ 1 / 4 - kappa2 := by linarith
  have hU : 0 ≤ U N u := unorm_nonneg N u
  have hmul : 0 ≤ (1 / 4 - kappa2) * U N u := mul_nonneg hk hU
  nlinarith [hgap, hmul]

/-- BEYOND THE WALL: for every kappa^2 > 1/4 there EXIST explicit negative
    modes -- the flat slab u = 1 on [1, N-2] at box size N > 1 + 3/(kappa^2-1/4)
    has E = 3 - (kappa^2 - 1/4)*(N-1) < 0. At the committed kappa = 1/2 the
    vacuum is exactly marginal; any stronger coupling makes it explode. -/
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

/-! ## 7. the certificate record -/

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