import Mathlib

/-!
# X03 — the first-flight ladder: corrected r4, first r10 certificate, new r12

Companion to deepseek_push/X03_ladder_lean.py (kills pre-registered in
X-WAVE_BRIEF.md) and X01/X02.  The X-wave CLOSES the even ladder in one exact
rational formula, M_n = (3/(2(n+1)(n+2))) * sum_k (k+1)/(2k+1), and CORRECTS
the m=4 rung: the landed 1/4 came from a hand-written antiderivative whose s^2
and s^3 coefficients are halved (M05_geometric_anchors I2 / P01 I2 / Q01
g_m(4); m=4 was absent from every K0 replication gate).  The correct value is
17/60.  The Q01 theorem q01CoreR4 (int P~_4 = 1/4) is a formally-correct proof
about the polynomial OF THE BUGGY DERIVATION — Q01_r6_core.lean stays
bit-identical (append-only house rule); THIS theorem supersedes its semantic
content.

The cores below come from the CLEAN route (sympy sp.integrate of the full
power (R^2+2R mu s+s^2)^k in s, then the exact mu->t change of variables, the
log/atanh parts integrated by parts with V(1)=0 — divisibility CHECKED, not
assumed; cf. S01_r10_moment.py derive()).  Each I_m = int_0^1 P~_m dR is the
exact 1D polynomial core whose value is certified here (FTC idiom of
N03/Q01/S01).  The 2D->1D reduction is sympy-exact and cross-checked by
40-dps original-variable quadrature and 1e7 MC in X01_ladder_closure.py —
it is NOT a 2D Lean certification (K3 scope).
-/

namespace X01

noncomputable section

open scoped intervalIntegral

/-- Antiderivative of the degree-14 polynomial (function-level sum). -/
def coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 : ℝ) : ℝ → ℝ :=
  (fun y : ℝ => c0 * y) +
    (fun y : ℝ => (c1 / 2) * y ^ 2) +
    (fun y : ℝ => (c2 / 3) * y ^ 3) +
    (fun y : ℝ => (c3 / 4) * y ^ 4) +
    (fun y : ℝ => (c4 / 5) * y ^ 5) +
    (fun y : ℝ => (c5 / 6) * y ^ 6) +
    (fun y : ℝ => (c6 / 7) * y ^ 7) +
    (fun y : ℝ => (c7 / 8) * y ^ 8) +
    (fun y : ℝ => (c8 / 9) * y ^ 9) +
    (fun y : ℝ => (c9 / 10) * y ^ 10) +
    (fun y : ℝ => (c10 / 11) * y ^ 11) +
    (fun y : ℝ => (c11 / 12) * y ^ 12) +
    (fun y : ℝ => (c12 / 13) * y ^ 13) +
    (fun y : ℝ => (c13 / 14) * y ^ 14) +
    (fun y : ℝ => (c14 / 15) * y ^ 15)

/-- The polynomial itself. -/
def corePoly (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 : ℝ) : ℝ → ℝ :=
  fun x : ℝ => c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8 + c9 * x ^ 9 + c10 * x ^ 10 + c11 * x ^ 11 + c12 * x ^ 12 + c13 * x ^ 13 + c14 * x ^ 14

/-- deriv (coreAnti) = corePoly, termwise. -/
lemma x01_deriv_coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 : ℝ) : deriv (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14) = corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 := by
  funext x
  unfold coreAnti corePoly
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9) + (fun y : ℝ => (c9 / 10) * y ^ 10) + (fun y : ℝ => (c10 / 11) * y ^ 11) + (fun y : ℝ => (c11 / 12) * y ^ 12) + (fun y : ℝ => (c12 / 13) * y ^ 13) + (fun y : ℝ => (c13 / 14) * y ^ 14)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c14 / 15) * y ^ 15) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9) + (fun y : ℝ => (c9 / 10) * y ^ 10) + (fun y : ℝ => (c10 / 11) * y ^ 11) + (fun y : ℝ => (c11 / 12) * y ^ 12) + (fun y : ℝ => (c12 / 13) * y ^ 13)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c13 / 14) * y ^ 14) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9) + (fun y : ℝ => (c9 / 10) * y ^ 10) + (fun y : ℝ => (c10 / 11) * y ^ 11) + (fun y : ℝ => (c11 / 12) * y ^ 12)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c12 / 13) * y ^ 13) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9) + (fun y : ℝ => (c9 / 10) * y ^ 10) + (fun y : ℝ => (c10 / 11) * y ^ 11)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c11 / 12) * y ^ 12) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9) + (fun y : ℝ => (c9 / 10) * y ^ 10)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c10 / 11) * y ^ 11) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c9 / 10) * y ^ 10) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c8 / 9) * y ^ 9) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c7 / 8) * y ^ 8) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c6 / 7) * y ^ 7) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c5 / 6) * y ^ 6) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c4 / 5) * y ^ 5) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c3 / 4) * y ^ 4) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c2 / 3) * y ^ 3) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => c0 * y) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c1 / 2) * y ^ 2) x)]
  change deriv (fun y : ℝ => c0 * id y) x + deriv (fun y : ℝ => (c1 / 2) * y ^ 2) x + deriv (fun y : ℝ => (c2 / 3) * y ^ 3) x + deriv (fun y : ℝ => (c3 / 4) * y ^ 4) x + deriv (fun y : ℝ => (c4 / 5) * y ^ 5) x + deriv (fun y : ℝ => (c5 / 6) * y ^ 6) x + deriv (fun y : ℝ => (c6 / 7) * y ^ 7) x + deriv (fun y : ℝ => (c7 / 8) * y ^ 8) x + deriv (fun y : ℝ => (c8 / 9) * y ^ 9) x + deriv (fun y : ℝ => (c9 / 10) * y ^ 10) x + deriv (fun y : ℝ => (c10 / 11) * y ^ 11) x + deriv (fun y : ℝ => (c11 / 12) * y ^ 12) x + deriv (fun y : ℝ => (c12 / 13) * y ^ 13) x + deriv (fun y : ℝ => (c13 / 14) * y ^ 14) x + deriv (fun y : ℝ => (c14 / 15) * y ^ 15) x
      = c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8 + c9 * x ^ 9 + c10 * x ^ 10 + c11 * x ^ 11 + c12 * x ^ 12 + c13 * x ^ 13 + c14 * x ^ 14
  simp_rw [deriv_const_mul_field, deriv_pow_field, deriv_id]
  simp
  ring_nf

/-- Differentiability of the antiderivative everywhere. -/
lemma x01_diff_coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 x : ℝ) : DifferentiableAt ℝ (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14) x := by
  unfold coreAnti
  fun_prop

/-- Continuity of the polynomial on [0,1]. -/
lemma x01_cont_corePoly (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 : ℝ) :
    ContinuousOn (corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14) (Set.uIcc 0 1) := by
  unfold corePoly
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : ℝ => c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8 + c9 * x ^ 9 + c10 * x ^ 10 + c11 * x ^ 11 + c12 * x ^ 12 + c13 * x ^ 13 + c14 * x ^ 14) Set.univ)
  intro x hx
  simp

/-- Exact polynomial integral on [0,1]. -/
lemma x01_int_core_01 (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 : ℝ) :
    (∫ x in (0 : ℝ)..1, corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 x) = c0 + c1 / 2 + c2 / 3 + c3 / 4 + c4 / 5 + c5 / 6 + c6 / 7 + c7 / 8 + c8 / 9 + c9 / 10 + c10 / 11 + c11 / 12 + c12 / 13 + c13 / 14 + c14 / 15 := by
  rw [intervalIntegral.integral_deriv_eq_sub' (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14)]
  · dsimp [coreAnti]
    norm_num <;> ring_nf
  · exact x01_deriv_coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14
  · intro x hx
    exact x01_diff_coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 x
  · exact x01_cont_corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14

/-- E[int r^4 ds] = 17/60 (CORRECTED; supersedes Q01's q01CoreR4 = 1/4) — int_0^1 P~_{R2} dR = 17/60 (clean sympy route B; see deepseek_push/X03_ladder_lean.py). -/
theorem x01CoreR4 : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 16 * R ^ 0 + (0 : ℝ) * R ^ 1 + (3 : ℝ) / 80 * R ^ 2 + (0 : ℝ) * R ^ 3 + (5 : ℝ) / 48 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 16 * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8 + (0 : ℝ) * R ^ 9 + (0 : ℝ) * R ^ 10 + (0 : ℝ) * R ^ 11 + (0 : ℝ) * R ^ 12 + (0 : ℝ) * R ^ 13 + (0 : ℝ) * R ^ 14) = (17 : ℝ) / 60 := by
  have hp : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 16 * R ^ 0 + (0 : ℝ) * R ^ 1 + (3 : ℝ) / 80 * R ^ 2 + (0 : ℝ) * R ^ 3 + (5 : ℝ) / 48 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 16 * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8 + (0 : ℝ) * R ^ 9 + (0 : ℝ) * R ^ 10 + (0 : ℝ) * R ^ 11 + (0 : ℝ) * R ^ 12 + (0 : ℝ) * R ^ 13 + (0 : ℝ) * R ^ 14)
      = (∫ R in (0 : ℝ)..1, corePoly ((3 : ℝ) / 16) ((0 : ℝ)) ((3 : ℝ) / 80) ((0 : ℝ)) ((5 : ℝ) / 48) ((0 : ℝ)) ((7 : ℝ) / 16) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [x01_int_core_01 ((3 : ℝ) / 16) ((0 : ℝ)) ((3 : ℝ) / 80) ((0 : ℝ)) ((5 : ℝ) / 48) ((0 : ℝ)) ((7 : ℝ) / 16) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ))]
  norm_num

/-- E[int r^10 ds] = 13649/97020 (T01 rung — FIRST certificate) — int_0^1 P~_{R5} dR = 13649/97020 (clean sympy route B; see deepseek_push/X03_ladder_lean.py). -/
theorem x01CoreR10 : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 28 * R ^ 0 + (0 : ℝ) * R ^ 1 + (3 : ℝ) / 616 * R ^ 2 + (0 : ℝ) * R ^ 3 + (5 : ℝ) / 504 * R ^ 4 + (0 : ℝ) * R ^ 5 + (1 : ℝ) / 56 * R ^ 6 + (0 : ℝ) * R ^ 7 + (9 : ℝ) / 280 * R ^ 8 + (0 : ℝ) * R ^ 9 + (11 : ℝ) / 168 * R ^ 10 + (0 : ℝ) * R ^ 11 + (13 : ℝ) / 56 * R ^ 12 + (0 : ℝ) * R ^ 13 + (0 : ℝ) * R ^ 14) = (13649 : ℝ) / 97020 := by
  have hp : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 28 * R ^ 0 + (0 : ℝ) * R ^ 1 + (3 : ℝ) / 616 * R ^ 2 + (0 : ℝ) * R ^ 3 + (5 : ℝ) / 504 * R ^ 4 + (0 : ℝ) * R ^ 5 + (1 : ℝ) / 56 * R ^ 6 + (0 : ℝ) * R ^ 7 + (9 : ℝ) / 280 * R ^ 8 + (0 : ℝ) * R ^ 9 + (11 : ℝ) / 168 * R ^ 10 + (0 : ℝ) * R ^ 11 + (13 : ℝ) / 56 * R ^ 12 + (0 : ℝ) * R ^ 13 + (0 : ℝ) * R ^ 14)
      = (∫ R in (0 : ℝ)..1, corePoly ((3 : ℝ) / 28) ((0 : ℝ)) ((3 : ℝ) / 616) ((0 : ℝ)) ((5 : ℝ) / 504) ((0 : ℝ)) ((1 : ℝ) / 56) ((0 : ℝ)) ((9 : ℝ) / 280) ((0 : ℝ)) ((11 : ℝ) / 168) ((0 : ℝ)) ((13 : ℝ) / 56) ((0 : ℝ)) ((0 : ℝ)) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [x01_int_core_01 ((3 : ℝ) / 28) ((0 : ℝ)) ((3 : ℝ) / 616) ((0 : ℝ)) ((5 : ℝ) / 504) ((0 : ℝ)) ((1 : ℝ) / 56) ((0 : ℝ)) ((9 : ℝ) / 280) ((0 : ℝ)) ((11 : ℝ) / 168) ((0 : ℝ)) ((13 : ℝ) / 56) ((0 : ℝ)) ((0 : ℝ))]
  norm_num

/-- E[int r^12 ds] = 50423/420420 (NEW rung from the closed-form ladder) — int_0^1 P~_{R6} dR = 50423/420420 (clean sympy route B; see deepseek_push/X03_ladder_lean.py). -/
theorem x01CoreR12 : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 32 * R ^ 0 + (0 : ℝ) * R ^ 1 + (9 : ℝ) / 2912 * R ^ 2 + (0 : ℝ) * R ^ 3 + (15 : ℝ) / 2464 * R ^ 4 + (0 : ℝ) * R ^ 5 + (1 : ℝ) / 96 * R ^ 6 + (0 : ℝ) * R ^ 7 + (27 : ℝ) / 1568 * R ^ 8 + (0 : ℝ) * R ^ 9 + (33 : ℝ) / 1120 * R ^ 10 + (0 : ℝ) * R ^ 11 + (13 : ℝ) / 224 * R ^ 12 + (0 : ℝ) * R ^ 13 + (45 : ℝ) / 224 * R ^ 14) = (50423 : ℝ) / 420420 := by
  have hp : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 32 * R ^ 0 + (0 : ℝ) * R ^ 1 + (9 : ℝ) / 2912 * R ^ 2 + (0 : ℝ) * R ^ 3 + (15 : ℝ) / 2464 * R ^ 4 + (0 : ℝ) * R ^ 5 + (1 : ℝ) / 96 * R ^ 6 + (0 : ℝ) * R ^ 7 + (27 : ℝ) / 1568 * R ^ 8 + (0 : ℝ) * R ^ 9 + (33 : ℝ) / 1120 * R ^ 10 + (0 : ℝ) * R ^ 11 + (13 : ℝ) / 224 * R ^ 12 + (0 : ℝ) * R ^ 13 + (45 : ℝ) / 224 * R ^ 14)
      = (∫ R in (0 : ℝ)..1, corePoly ((3 : ℝ) / 32) ((0 : ℝ)) ((9 : ℝ) / 2912) ((0 : ℝ)) ((15 : ℝ) / 2464) ((0 : ℝ)) ((1 : ℝ) / 96) ((0 : ℝ)) ((27 : ℝ) / 1568) ((0 : ℝ)) ((33 : ℝ) / 1120) ((0 : ℝ)) ((13 : ℝ) / 224) ((0 : ℝ)) ((45 : ℝ) / 224) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [x01_int_core_01 ((3 : ℝ) / 32) ((0 : ℝ)) ((9 : ℝ) / 2912) ((0 : ℝ)) ((15 : ℝ) / 2464) ((0 : ℝ)) ((1 : ℝ) / 96) ((0 : ℝ)) ((27 : ℝ) / 1568) ((0 : ℝ)) ((33 : ℝ) / 1120) ((0 : ℝ)) ((13 : ℝ) / 224) ((0 : ℝ)) ((45 : ℝ) / 224)]
  norm_num

#print axioms x01CoreR4
#print axioms x01CoreR10
#print axioms x01CoreR12
