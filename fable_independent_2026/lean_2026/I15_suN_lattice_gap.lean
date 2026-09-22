import Mathlib

/-!
# I15 -- THE SU(N) STRONG-COUPLING GAP, UNIFORM IN N

Scope: the declarations in this file certify scalar inequalities, not an
operator construction. For the single-plaquette Hamiltonian, the separate
min-max proof in real_research/reviews/spectral_spine_closure_2026_09_22/
i15/PROOF.md supplies the actual comparison with the spectral gap. It uses
the full character Hilbert space, a positive magnetic operator, and a trial
upper bound on the INTERACTING ground energy. It does not assume that the
electric vacuum remains an eigenvector. The comparison gives the bound

    gap_N(x) = x (N^2-1)/N - 2N/x,   x = g^2 (lattice units),

with gap_N(2) = (N^2-2)/N and gap_N(x) >= 1 for x >= 2, N >= 2.
These are lower bounds, not exact interacting gaps.

For the MANY-PLAQUETTE lattice, PROOF.md instead applies Yarotsky's
weak-interaction theorem (math-ph/0411042v1, Theorems 1-3). This gives a
gap uniform in N and volume for x >= X_d, where X_d is a finite but not
numerically evaluated range-dependent constant. It does NOT certify x=2
for arbitrary volume or transfer the one-plaquette formula to that case.
The source theorem and its operator application are not Lean formalized;
the normalization and rescaling arithmetic below is. No continuum or Clay
claim is made.

Compiled against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real

/-- the electric Casimir of SU(N), dimensionless -/
def Cc (N : ℝ) : ℝ := (N^2 - 1) / (2 * N)

/-- the strong-coupling lattice gap bound (lattice units) -/
def gapN (N x : ℝ) : ℝ := x * (N^2 - 1) / N - 2 * N / x

/-- the loop energy is twice the Casimir times x: E_loop = 2 x C_F -/
theorem loop_energy (N x : ℝ) (hN : N ≠ 0) : x * (N^2 - 1) / N = 2 * x * Cc N := by
  unfold Cc
  field_simp [hN]

/-- the certified corner values: gap_N(2) = (N^2 - 2)/N -- SU(2) gives 1,
    SU(3) gives 7/3, reproducing the certified table -/
theorem gap_at_two (N : ℝ) (hN : N ≠ 0) : gapN N 2 = (N^2 - 2) / N := by
  unfold gapN
  field_simp [hN, (by norm_num : (2 : ℝ) ≠ 0)]
  ring

/-- the Casimir is positive -/
theorem casimir_pos (N : ℝ) (hN2 : 2 ≤ N) : 0 < Cc N := by
  have hN : 0 < N := by linarith
  unfold Cc
  exact div_pos (by nlinarith [hN2]) (by linarith)

/-- THE GAP, UNIFORM IN N: for every SU(N), N >= 2, at every strong coupling
    x >= 2 the spectral gap bound is strictly positive -/
theorem gap_at_strong (N x : ℝ) (hN2 : 2 ≤ N) (hx2 : 2 ≤ x) : 0 < gapN N x := by
  have hN : 0 < N := by linarith
  have hNn : N ≠ 0 := ne_of_gt hN
  have hq : 0 ≤ (N^2 - 1) / N := by
    exact le_of_lt (div_pos (by nlinarith [hN2]) hN)
  have h1 : (2 : ℝ) * (N^2 - 1) / N ≤ x * (N^2 - 1) / N := by
    calc
      (2 : ℝ) * (N^2 - 1) / N = 2 * ((N^2 - 1) / N) := by ring
      _ ≤ x * ((N^2 - 1) / N) := mul_le_mul_of_nonneg_right hx2 hq
      _ = x * (N^2 - 1) / N := by ring
  have hx1 : 1 / x ≤ 1 / 2 := by
    exact one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 2) hx2
  have h2 : 2 * N / x ≤ N := by
    calc
      2 * N / x = (2 * N) * (1 / x) := by ring
      _ ≤ (2 * N) * (1 / 2) := mul_le_mul_of_nonneg_left hx1 (by linarith : 0 ≤ 2 * N)
      _ = N := by
        field_simp [(by norm_num : (2 : ℝ) ≠ 0)]
  have hmain : (N^2 - 2) / N ≤ gapN N x := by
    unfold gapN
    calc
      (N^2 - 2) / N = (2 : ℝ) * (N^2 - 1) / N - N := by
        field_simp [hNn]
        ring
      _ ≤ x * (N^2 - 1) / N - 2 * N / x := by
        nlinarith [h1, h2]
  have hpos : 0 < (N^2 - 2) / N := by
    exact div_pos (by nlinarith [hN2]) hN
  exact lt_of_lt_of_le hpos hmain

/-! ## the certificate record -/

#print axioms loop_energy
#print axioms gap_at_two
#print axioms casimir_pos
#print axioms gap_at_strong

/-! ## Explicit uniform constants and honest comparison interfaces -/

/-- A numerical lower bound on the fundamental Casimir, independent of N. -/
theorem casimir_uniform_floor (N : ℝ) (hN : 2 ≤ N) : (3 / 4 : ℝ) ≤ Cc N := by
  have hNp : 0 < N := by linarith
  unfold Cc
  apply (le_div_iff₀ (by positivity : 0 < 2 * N)).2
  have hprod : 0 ≤ (N - 2) * (N + 1 / 2) :=
    mul_nonneg (by linarith) (by linarith)
  nlinarith [hprod]

/-- The original scalar lower bound is at least ONE uniformly in N and x. -/
theorem gap_uniform_one (N x : ℝ) (hN : 2 ≤ N) (hx : 2 ≤ x) : 1 ≤ gapN N x := by
  have hNp : 0 < N := by linarith
  have hxp : 0 < x := by linarith
  have hp : 0 ≤ (N - 2) * (N + 1) := mul_nonneg (by linarith) (by linarith)
  have he : N + 1 ≤ 2 * (N^2 - 1) / N := by
    apply (le_div_iff₀ hNp).2
    nlinarith [hp]
  have hem : 2 * (N^2 - 1) / N ≤ x * (N^2 - 1) / N := by
    apply div_le_div_of_nonneg_right _ (le_of_lt hNp)
    exact mul_le_mul_of_nonneg_right hx (by nlinarith)
  have hb : 2 * N / x ≤ N := by
    apply (div_le_iff₀ hxp).2
    nlinarith [mul_nonneg (by linarith : 0 ≤ x - 2) (le_of_lt hNp)]
  unfold gapN
  linarith

/-- Conditional arithmetic after the operator min-max bounds have been proved.
    E0 is the actual interacting ground energy; b is the magnetic coefficient. -/
theorem single_plaquette_comparison (N x b E0 E1 : ℝ)
    (hN : 2 ≤ N) (hx : 0 < x) (hb : b ≤ 2 * N)
    (hground : E0 ≤ b / x) (hexcited : 2 * x * Cc N ≤ E1) :
    gapN N x ≤ E1 - E0 := by
  have hNn : N ≠ 0 := by linarith
  have hmag : b / x ≤ 2 * N / x := div_le_div_of_nonneg_right hb (le_of_lt hx)
  have hel := loop_energy N x hNn
  unfold gapN
  linarith

/-- Uniform control of b/C_F for all magnetic normalizations 0 <= b <= 2N. -/
theorem magnetic_casimir_ratio (N b : ℝ) (hN : 2 ≤ N) (hb : b ≤ 2 * N) :
    b / Cc N ≤ 16 / 3 := by
  have hCp := casimir_pos N hN
  apply (div_le_iff₀ hCp).2
  have hNp : 0 < N := by linarith
  have hbound : 2 * N ≤ (16 / 3 : ℝ) * Cc N := by
    unfold Cc
    have hcancel : (16 / 3 : ℝ) * ((N^2 - 1) / (2 * N)) =
        ((8 / 3 : ℝ) * (N^2 - 1)) / N := by ring
    rw [hcancel]
    apply (le_div_iff₀ hNp).2
    nlinarith [sq_nonneg (N - 2)]
  exact le_trans hb hbound

/-- m is the number of plaquette orientations per anchor (d choose 2).
    The local perturbation after removing its scalar constant has this bound. -/
theorem normalized_magnetic_bound (N x b m : ℝ) (hN : 2 ≤ N)
    (hx : 0 < x) (hb : b ≤ 2 * N) (hm : 0 ≤ m) :
    2 * b * m / (x^2 * Cc N) ≤ (32 / 3 : ℝ) * m / x^2 := by
  have hr := magnetic_casimir_ratio N b hN hb
  have hc : 0 ≤ 2 * m / x^2 := by positivity
  have ht := mul_le_mul_of_nonneg_left hr hc
  calc
    2 * b * m / (x^2 * Cc N) = (2 * m / x^2) * (b / Cc N) := by
      simp only [div_eq_mul_inv, mul_inv_rev]
      ring
    _ ≤ (2 * m / x^2) * (16 / 3) := ht
    _ = (32 / 3 : ℝ) * m / x^2 := by ring

/-- Rescaling a normalized spectral bound from Yarotsky's theorem. The source
    theorem supplies hgap; it is an explicit hypothesis, not an axiom here. -/
theorem lattice_gap_rescale (N x delta eta c2 : ℝ)
    (hN : 2 ≤ N) (hx : 0 < x) (hsmall : c2 * eta ≤ 1 / 2)
    (hgap : (x * Cc N / 2) * (1 - c2 * eta) ≤ delta) :
    3 * x / 16 ≤ delta := by
  have hC := casimir_uniform_floor N hN
  have hCp := casimir_pos N hN
  have hmul : (x * Cc N / 2) * (1 / 2) ≤
      (x * Cc N / 2) * (1 - c2 * eta) := by
    apply mul_le_mul_of_nonneg_left (by linarith)
    positivity
  have hxc := mul_le_mul_of_nonneg_left hC (le_of_lt hx)
  nlinarith [hgap, hmul, hxc]

#print axioms casimir_uniform_floor
#print axioms gap_uniform_one
#print axioms single_plaquette_comparison
#print axioms magnetic_casimir_ratio
#print axioms normalized_magnetic_bound
#print axioms lattice_gap_rescale
