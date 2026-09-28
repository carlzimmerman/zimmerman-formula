import Mathlib

/-!
# AS151 — ADM momentum-map trace inversion (local fiber algebra)

Certificate for the algebraic content of AS151 step 2: on the symmetric-tensor
fiber with identity leaf metric (orthonormal frame), the map

    T_A(K) = A (K - tr(K) 1)

used for the canonical momentum π^{ij} = (M_P² √h / 2)(K^{ij} - K h^{ij})
(N.B. the source keeps K = K^{ij} h_{ij} as the trace; here h = 1 so h^{ij} = 1^{ij})
is inverted by

    S_A(π) = (1/A) (π - (1/2) tr(π) 1)

whenever A ≠ 0 and tr(1) = 3.  This is the exact algebraic reason the metric
sector contributes NO hidden primary constraint beyond π_N, π_i.
Statement: T_A ∘ S_A = id and S_A ∘ T_A = id.
-/

noncomputable section
open scoped BigOperators

namespace AS151

/-- Trace on 3×3 real matrices (diagonal sum). -/
def trm (M : Matrix (Fin 3) (Fin 3) ℝ) : ℝ := ∑ i : Fin 3, M i i

@[simp] lemma trm_smul (c : ℝ) (M : Matrix (Fin 3) (Fin 3) ℝ) :
    trm (c • M) = c • trm M := by
  simp [trm, Finset.mul_sum]

@[simp] lemma trm_sub (M N : Matrix (Fin 3) (Fin 3) ℝ) :
    trm (M - N) = trm M - trm N := by
  simp [trm, Finset.sum_sub_distrib]

@[simp] lemma trm_add (M N : Matrix (Fin 3) (Fin 3) ℝ) :
    trm (M + N) = trm M + trm N := by
  simp [trm, Finset.sum_add_distrib]

lemma trm_one : trm (1 : Matrix (Fin 3) (Fin 3) ℝ) = 3 := by
  simp [trm, Matrix.one_apply]

/-- p = A (K - tr(K) 1): the derived ADM momentum expression (trace sector, h=1). -/
def T (A : ℝ) (K : Matrix (Fin 3) (Fin 3) ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  A • (K - trm K • (1 : Matrix (Fin 3) (Fin 3) ℝ))

/-- K = (1/A) (p - (1/2) tr(p) 1): the inverse on the trace sector. -/
def S (A : ℝ) (p : Matrix (Fin 3) (Fin 3) ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  A⁻¹ • (p - (1/2 : ℝ) • (trm p • (1 : Matrix (Fin 3) (Fin 3) ℝ)))

/-- Trace projection of the ADM map: tr(T_A K) = -2A tr(K) (the -(2A) coefficient). -/
lemma trm_T (A : ℝ) (K : Matrix (Fin 3) (Fin 3) ℝ) : trm (T A K) = (-2 * A) * trm K := by
  unfold T
  rw [trm_smul, trm_sub, trm_smul, trm_one]
  ring

/-- T_1 is linear in the matrix argument. -/
lemma T_one_smul (c : ℝ) (K : Matrix (Fin 3) (Fin 3) ℝ) : T 1 (c • K) = c • T 1 K := by
  ext i j
  simp [T, trm_smul, smul_smul]
  ring

/-- Identity metric case, A = 1: T_1 ∘ S_1 = id (addition side of the inversion). -/
theorem T_one_S_one_identity (p : Matrix (Fin 3) (Fin 3) ℝ) : T 1 (S 1 p) = p := by
  ext i j
  simp [T, S, trm_sub, trm_smul, trm_one]
  ring

/-- Identity metric case, A = 1: S_1 ∘ T_1 = id (subtraction side of the inversion). -/
theorem S_one_T_one_identity (K : Matrix (Fin 3) (Fin 3) ℝ) : S 1 (T 1 K) = K := by
  ext i j
  simp [T, S, trm_sub, trm_smul, trm_one]
  ring

/-- General A ≠ 0: T_A ∘ S_A = id.  This is exactly "π given, recover K". -/
theorem T_S_identity (A : ℝ) (hA : A ≠ 0) (p : Matrix (Fin 3) (Fin 3) ℝ) : T A (S A p) = p := by
  have hS : S A p = A⁻¹ • S 1 p := by
    ext i j
    simp [S]
  have hT : T A (A⁻¹ • S 1 p) = A • T 1 (A⁻¹ • S 1 p) := by
    ext i j
    simp [T]
  rw [hS, hT]
  rw [T_one_smul]
  rw [smul_smul]
  have hAmul : A * A⁻¹ = 1 := mul_inv_cancel₀ hA
  rw [hAmul]
  simp
  exact T_one_S_one_identity p

/-- S_1 is linear in the matrix argument. -/
lemma S_one_smul (c : ℝ) (p : Matrix (Fin 3) (Fin 3) ℝ) : S 1 (c • p) = c • S 1 p := by
  ext i j
  simp [S, trm_smul, smul_smul]
  ring

/-- General A ≠ 0: S_A ∘ T_A = id.  This is exactly "K given, recover π". -/
theorem S_T_identity (A : ℝ) (hA : A ≠ 0) (K : Matrix (Fin 3) (Fin 3) ℝ) : S A (T A K) = K := by
  have hTsmul : T A K = A • T 1 K := by
    ext i j
    simp [T]
  have hSstep : S A (A • T 1 K) = A⁻¹ • S 1 (A • T 1 K) := by
    ext i j
    simp [S, trm_smul]
  calc
    S A (T A K) = S A (A • T 1 K) := by rw [hTsmul]
    _ = A⁻¹ • S 1 (A • T 1 K) := hSstep
    _ = A⁻¹ • (A • S 1 (T 1 K)) := by rw [S_one_smul]
    _ = (A⁻¹ * A) • S 1 (T 1 K) := by
          rw [smul_smul]
    _ = S 1 (T 1 K) := by
          rw [inv_mul_cancel₀ hA]
          simp
    _ = K := S_one_T_one_identity K

-- Axiom audits (hard bar: subseteq {propext, Classical.choice, Quot.sound})
#print axioms T_one_S_one_identity
#print axioms S_one_T_one_identity
#print axioms T_S_identity
#print axioms S_T_identity
#print axioms trm_T

end AS151
