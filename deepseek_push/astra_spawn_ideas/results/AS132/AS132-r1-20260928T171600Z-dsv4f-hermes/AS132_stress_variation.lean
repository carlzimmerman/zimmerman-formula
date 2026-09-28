import Mathlib

/-!
AS132 (Tier-0): fixed-compensator stress via leaf-metric variation — algebraic core.

Pinned action: CA4-GNC host (real_research/common_action_2026_09_26/action/
FINAL_ACTION.md, eq. (4)), branch CA5-GNC-R (reciprocal dark sector).

Target (task math):  S_comp = (M_P^2 c_N ell / 2) * int dtau
int_Sigma N sqrt(h) a^i D_i W_b,   a = D ln N,
varied over the leaf metric h at FIXED (N, W_b) on a compact closed spacelike
leaf; the first variation is claimed to be

    delta_h S_comp = (M_P^2 c_N ell / 2) int N sqrt(h) Theta_comp^ij delta_h_ij,
    Theta_comp^ij = (1/2) h^ij (a . DW_b) - a^{(i} D^{j)} W_b  .

Certified algebra over R (flat-leaf 2D prototype of the pointwise identity;
the semantic mapping is documented in derivation.md):
  d/deps |_0  sqrt(det(h + eps s)) * (a(h + eps s) . DW)
      =  (s11 + s22)/2 * (a1 w1 + a2 w2)
         - (s11 a1 w1 + s12 (a1 w2 + a2 w1) + s22 a2 w2)
with  h = delta_ij,  a(h) = h^{-1} a  (raised),  DW fixed (lowered covector),
g(eps) := (1+eps s11)(1+eps s22) - (eps s12)^2,
A(eps)  := (I + eps S)^{-1} a  via the 2x2 adjugate:
A1(eps) := ((1+eps s22) a1 - eps s12 a2) / g(eps),
A2(eps) := ((-eps s12) a1 + (1+eps s11) a2) / g(eps).
This is the S2 claim in the flat limit: the measure channel contributes
det'(0)/(2 sqrt(det 0)) (a . DW) with det 0 = 1, and the contraction channel
contributes -s_ij a^i w^j via the inverse-metric derivative
d/deps (I + eps S)^{-1} |_0 = -S.

Theorems:
  1. `g_value_at_zero`, `g_deriv_at_zero`  — g(0) = 1, g'(0) = s11 + s22.
  2. `raise_deriv_1` / `raise_deriv_2`     — d/deps A_i |_0 = -(S a)_i.
  3. `contraction_variation`               — the -s_ij a^i w^j block.
  4. `sqrtg_deriv_at_zero`                 — d/deps sqrt(g) |_0 = (s11+s22)/2.
  5. `stress_variation_flat`               — the full S2 flat identity.
-/

noncomputable section
namespace AS132

/-- perturbed determinant: g(eps) = det(I + eps S), S symmetric [[s11,s12],[s12,s22]]. -/
def g (s11 s12 s22 : ℝ) : ℝ → ℝ :=
  fun ε => (1 + ε * s11) * (1 + ε * s22) - (ε * s12) * (ε * s12)

/-- first component of the raised acceleration a(h(eps)) = (I + eps S)^{-1} a
    (adjugate formula, 2 x 2). -/
def A1 (s11 s12 s22 a1 a2 : ℝ) : ℝ → ℝ :=
  fun ε => ((1 + ε * s22) * a1 - ε * s12 * a2) / g s11 s12 s22 ε

/-- second component of the raised acceleration. -/
def A2 (s11 s12 s22 a1 a2 : ℝ) : ℝ → ℝ :=
  fun ε => ((-ε * s12) * a1 + (1 + ε * s11) * a2) / g s11 s12 s22 ε

/-- g(0) = det I = 1. -/
lemma g_value_at_zero (s11 s12 s22 : ℝ) : g s11 s12 s22 0 = 1 := by
  unfold g
  ring

/-- g'(0) = tr S = s11 + s22. -/
lemma g_deriv_at_zero (s11 s12 s22 : ℝ) :
    HasDerivAt (g s11 s12 s22) (s11 + s22) 0 := by
  unfold g
  have h1 : HasDerivAt (fun ε : ℝ => 1 + ε * s11) (0 + 1 * s11) 0 := by
    exact (hasDerivAt_const (0 : ℝ) 1).add ((hasDerivAt_id (0 : ℝ)).mul_const s11)
  have h2 : HasDerivAt (fun ε : ℝ => 1 + ε * s22) (0 + 1 * s22) 0 := by
    exact (hasDerivAt_const (0 : ℝ) 1).add ((hasDerivAt_id (0 : ℝ)).mul_const s22)
  have h3 : HasDerivAt (fun ε : ℝ => (ε * s12) * (ε * s12))
      ((1 * s12) * (0 * s12) + (0 * s12) * (1 * s12)) 0 := by
    exact (((hasDerivAt_id (0 : ℝ)).mul_const s12).mul
      ((hasDerivAt_id (0 : ℝ)).mul_const s12))
  have hraw : HasDerivAt (fun ε : ℝ => (1 + ε * s11) * (1 + ε * s22) - (ε * s12) * (ε * s12))
      (((0 + 1 * s11) * (1 + 0 * s22) + (1 + 0 * s11) * (0 + 1 * s22))
        - ((1 * s12) * (0 * s12) + (0 * s12) * (1 * s12))) 0 := by
    exact (h1.mul h2).sub h3
  have hEq : (((0 + 1 * s11) * (1 + 0 * s22) + (1 + 0 * s11) * (0 + 1 * s22))
        - ((1 * s12) * (0 * s12) + (0 * s12) * (1 * s12))) = s11 + s22 := by
    ring
  rw [hEq] at hraw
  exact hraw

/-- A1(0) = a1 (raised = lowered at the flat base). -/
lemma A1_value_at_zero (s11 s12 s22 a1 a2 : ℝ) :
    A1 s11 s12 s22 a1 a2 0 = a1 := by
  unfold A1 g
  ring

/-- A2(0) = a2. -/
lemma A2_value_at_zero (s11 s12 s22 a1 a2 : ℝ) :
    A2 s11 s12 s22 a1 a2 0 = a2 := by
  unfold A2 g
  ring

/-- d/deps A1 |_0 = -(s11 a1 + s12 a2)  (first row of -S applied to a). -/
lemma raise_deriv_1 (s11 s12 s22 a1 a2 : ℝ) :
    HasDerivAt (A1 s11 s12 s22 a1 a2) (-(s11 * a1 + s12 * a2)) 0 := by
  unfold A1
  have hn : HasDerivAt (fun ε : ℝ => (1 + ε * s22) * a1 - ε * s12 * a2)
      ((0 + 1 * s22) * a1 - 1 * s12 * a2) 0 := by
    have hn1 : HasDerivAt (fun ε : ℝ => (1 + ε * s22) * a1)
        ((0 + 1 * s22) * a1) 0 := by
      exact ((hasDerivAt_const (0 : ℝ) 1).add
        ((hasDerivAt_id (0 : ℝ)).mul_const s22)).mul_const a1
    have hn2 : HasDerivAt (fun ε : ℝ => ε * s12 * a2) (1 * s12 * a2) 0 := by
      exact ((hasDerivAt_id (0 : ℝ)).mul_const s12).mul_const a2
    exact hn1.sub hn2
  have hg := g_deriv_at_zero s11 s12 s22
  have hdiv := hn.div hg (by simp [g_value_at_zero])
  have hEq : ((((0 + 1 * s22) * a1 - 1 * s12 * a2) * g s11 s12 s22 0
        - ((1 + 0 * s22) * a1 - 0 * s12 * a2) * (s11 + s22)) / g s11 s12 s22 0 ^ 2)
      = -(s11 * a1 + s12 * a2) := by
    rw [g_value_at_zero]
    ring
  rw [hEq] at hdiv
  exact hdiv

/-- d/deps A2 |_0 = -(s12 a1 + s22 a2)  (second row of -S applied to a). -/
lemma raise_deriv_2 (s11 s12 s22 a1 a2 : ℝ) :
    HasDerivAt (A2 s11 s12 s22 a1 a2) (-(s12 * a1 + s22 * a2)) 0 := by
  unfold A2
  have hn : HasDerivAt (fun ε : ℝ => -ε * s12 * a1 + (1 + ε * s11) * a2)
      ((-1 * s12) * a1 + (0 + 1 * s11) * a2) 0 := by
    have hn1 : HasDerivAt (fun ε : ℝ => -ε * s12 * a1) ((-1 * s12) * a1) 0 := by
      exact ((hasDerivAt_id (0 : ℝ)).neg.mul_const s12).mul_const a1
    have hn2 : HasDerivAt (fun ε : ℝ => (1 + ε * s11) * a2)
        ((0 + 1 * s11) * a2) 0 := by
      exact ((hasDerivAt_const (0 : ℝ) 1).add
        ((hasDerivAt_id (0 : ℝ)).mul_const s11)).mul_const a2
    exact hn1.add hn2
  have hg := g_deriv_at_zero s11 s12 s22
  have hdiv := hn.div hg (by simp [g_value_at_zero])
  have hEq : ((((-1 * s12) * a1 + (0 + 1 * s11) * a2) * g s11 s12 s22 0
        - (-0 * s12 * a1 + (1 + 0 * s11) * a2) * (s11 + s22)) / g s11 s12 s22 0 ^ 2)
      = -(s12 * a1 + s22 * a2) := by
    rw [g_value_at_zero]
    ring
  rw [hEq] at hdiv
  exact hdiv

/-- the contraction channel: d/deps (A(eps) . w)_0 = -s_ij a^i w^j. -/
lemma contraction_variation (s11 s12 s22 a1 a2 w1 w2 : ℝ) :
    HasDerivAt (fun ε : ℝ =>
        A1 s11 s12 s22 a1 a2 ε * w1 + A2 s11 s12 s22 a1 a2 ε * w2)
      (-(s11 * a1 * w1 + s12 * a1 * w2 + s12 * a2 * w1 + s22 * a2 * w2)) 0 := by
  have hw := (raise_deriv_1 s11 s12 s22 a1 a2).mul_const w1
  have hv := (raise_deriv_2 s11 s12 s22 a1 a2).mul_const w2
  have hsum := hw.add hv
  have hEq : (-(s11 * a1 + s12 * a2)) * w1 + (-(s12 * a1 + s22 * a2)) * w2
      = -(s11 * a1 * w1 + s12 * a1 * w2 + s12 * a2 * w1 + s22 * a2 * w2) := by
    ring
  rw [hEq] at hsum
  exact hsum

/-- the measure channel derivative: d/deps sqrt(g) |_0 = (s11 + s22)/2. -/
lemma sqrtg_deriv_at_zero (s11 s12 s22 : ℝ) :
    HasDerivAt (fun ε : ℝ => Real.sqrt (g s11 s12 s22 ε))
      ((s11 + s22) / 2) 0 := by
  have hg := g_deriv_at_zero s11 s12 s22
  have hg0nz : g s11 s12 s22 0 ≠ 0 := by
    rw [g_value_at_zero]
    norm_num
  have hsq := (Real.hasDerivAt_sqrt hg0nz).comp (0 : ℝ) hg
  have hEq : (1 / (2 * Real.sqrt (g s11 s12 s22 0))) * (s11 + s22)
      = (s11 + s22) / 2 := by
    rw [g_value_at_zero, Real.sqrt_one]
    ring
  rw [hEq] at hsq
  exact hsq

/-- THE S2 FLAT IDENTITY: full first variation of the compensator density
    sqrt(det(h+eps s)) (a(h+eps s) . DW) at eps = 0 equals
    (s11+s22)/2 (a1 w1 + a2 w2) - (s11 a1 w1 + s12 (a1 w2 + a2 w1) + s22 a2 w2). -/
theorem stress_variation_flat (s11 s12 s22 a1 a2 w1 w2 : ℝ) :
    HasDerivAt (fun ε : ℝ =>
        Real.sqrt (g s11 s12 s22 ε) *
          (A1 s11 s12 s22 a1 a2 ε * w1 + A2 s11 s12 s22 a1 a2 ε * w2))
      ((s11 + s22) / 2 * (a1 * w1 + a2 * w2)
        - (s11 * a1 * w1 + s12 * a1 * w2 + s12 * a2 * w1 + s22 * a2 * w2)) 0 := by
  have hsq := sqrtg_deriv_at_zero s11 s12 s22
  have hb := contraction_variation s11 s12 s22 a1 a2 w1 w2
  have hf := hsq.mul hb
  have hb0 : A1 s11 s12 s22 a1 a2 0 * w1 + A2 s11 s12 s22 a1 a2 0 * w2 =
      a1 * w1 + a2 * w2 := by
    rw [A1_value_at_zero, A2_value_at_zero]
  have hEq : ((s11 + s22) / 2 * (A1 s11 s12 s22 a1 a2 0 * w1
          + A2 s11 s12 s22 a1 a2 0 * w2)
        + Real.sqrt (g s11 s12 s22 0) * (-(s11 * a1 * w1 + s12 * a1 * w2
          + s12 * a2 * w1 + s22 * a2 * w2)))
      = ((s11 + s22) / 2 * (a1 * w1 + a2 * w2)
        - (s11 * a1 * w1 + s12 * a1 * w2 + s12 * a2 * w1 + s22 * a2 * w2)) := by
    rw [hb0, g_value_at_zero, Real.sqrt_one]
    ring
  rw [hEq] at hf
  exact hf

end AS132

#print axioms AS132.g_deriv_at_zero
#print axioms AS132.stress_variation_flat