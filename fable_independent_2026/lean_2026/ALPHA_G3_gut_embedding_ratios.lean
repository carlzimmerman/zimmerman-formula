import Mathlib

/-!
# M2_02 -- Lean certificate for the GUT-embedding ratio algebra of lane G3
Source lane: real_research/alpha_principle_2026/G_topological_anomaly/g3_gut_embedding_ratios.py
(checks E1a-E1e, E2c-E2e, E3a-E3b, E4a-E4b).  Repo Lean corpus: `git grep -n -i -e hypercharge -e "3/8" -e sin2
-- '*.lean'` finds nothing on this (the only "3/8" hits are unrelated: ChainCert/Exchange.lean sigmaReact,
AS007, AS245).  So this is new.

CERTIFIED (exact rational arithmetic on stated field content; Q = T3 + Y; left-handed Weyl multiplets given as
(colour dim, SU(2) dim, Y), trace over T3 eigenvalues (d-1)/2 - i):
* SU(5) generation 5bar + 10 (d^c, L, Q, u^c, e^c): Tr T3^2 = 2, Tr Y^2 = 10/3, Tr Q^2 = 16/3,
  Tr T3 Y = 0, Tr Q^2 = Tr T3^2 + Tr Y^2, Tr Y^2 / Tr T3^2 = 5/3, sin^2 theta_W := Tr T3^2 / Tr Q^2 = 3/8.
* the same 3/8 for the SO(10) 16 (adds nu^c) and the E6 27 (adds vector-like 5 + 5bar and a singlet).
* mutation control: dropping u^c (an incomplete SU(5) multiplet) gives sin^2 /= 3/8.
* one coupling g in the simple group: g_Y^2 Tr Y^2 = g_2^2 Tr T3^2  =>  g_Y^2 = (3/5) g_2^2.
* Pati-Salam with independent couplings: sin^2 theta_W = 3 g4^2 gR^2 / (3 g4^2 gR^2 + gL^2 (3 g4^2 + 2 gR^2)),
  equal to 3/8 at g4 = gL = gR, homogeneous of degree 0, and equal to 6/13 and 9/16 at (2,1,1) and (1,1,3):
  the ratio is NOT fixed without imposing equal couplings.
* one-loop coefficients from the standard field-content formulas: SM (41/10, -19/6, -7), MSSM (33/5, 1, -3)
  (this certifies the arithmetic of the formulas as written in the script, not that they are the right formulas).
* at unification alpha_em^-1 = (5/3) alpha_1^-1 + alpha_2^-1 -> (8/3) alpha_G^-1.
NOT CERTIFIED: that nature has a GUT, the scale M_G, any running to the Thomson limit, any value of alpha.
The lane's own conclusion (which this file supports algebraically): the traces fix the RATIO g_Y/g_2 and the
b_i fix slopes; the common coupling and every additive constant stay free.  kappa = 1/2 is not involved.
-/

namespace M2Gut

/-- a left-handed Weyl multiplet: colour dim, SU(2) dim, hypercharge -/
structure Fld where
  c : ℕ
  d : ℕ
  y : ℚ

/-- T3 eigenvalue of the i-th component of a d-plet -/
def t3 (d : ℕ) (i : ℕ) : ℚ := ((d : ℚ) - 1) / 2 - i

def trT3sq (f : Fld) : ℚ := f.c * ∑ i ∈ Finset.range f.d, (t3 f.d i) ^ 2
def trYsq (f : Fld) : ℚ := f.c * f.d * f.y ^ 2
def trQsq (f : Fld) : ℚ := f.c * ∑ i ∈ Finset.range f.d, (t3 f.d i + f.y) ^ 2
def trT3Y (f : Fld) : ℚ := f.c * ∑ i ∈ Finset.range f.d, (t3 f.d i * f.y)

def sumT3sq (l : List Fld) : ℚ := (l.map trT3sq).sum
def sumYsq (l : List Fld) : ℚ := (l.map trYsq).sum
def sumQsq (l : List Fld) : ℚ := (l.map trQsq).sum
def sumT3Y (l : List Fld) : ℚ := (l.map trT3Y).sum

def dc : Fld := ⟨3, 1, 1 / 3⟩
def Lf : Fld := ⟨1, 2, -1 / 2⟩
def Qf : Fld := ⟨3, 2, 1 / 6⟩
def uc : Fld := ⟨3, 1, -2 / 3⟩
def ec : Fld := ⟨1, 1, 1⟩
def nuc : Fld := ⟨1, 1, 0⟩
def d5 : Fld := ⟨3, 1, -1 / 3⟩
def l5 : Fld := ⟨1, 2, 1 / 2⟩

def genSU5 : List Fld := [dc, Lf, Qf, uc, ec]
def genSO10 : List Fld := genSU5 ++ [nuc]
def genE6 : List Fld := genSO10 ++ [d5, l5, dc, Lf] ++ [nuc]
def genIncomplete : List Fld := [dc, Lf, Qf, ec]

theorem su5_traces :
    sumT3sq genSU5 = 2 ∧ sumYsq genSU5 = 10 / 3 ∧ sumQsq genSU5 = 16 / 3 ∧ sumT3Y genSU5 = 0 := by
  simp [genSU5, sumT3sq, sumYsq, sumQsq, sumT3Y, trT3sq, trYsq, trQsq, trT3Y, t3, dc, Lf, Qf, uc, ec,
    Finset.sum_range_succ]
  norm_num

theorem su5_Q_decomposition :
    sumQsq genSU5 = sumT3sq genSU5 + sumYsq genSU5 := by
  obtain ⟨h1, h2, h3, _⟩ := su5_traces
  rw [h1, h2, h3]; norm_num

theorem su5_Y_over_T3 : sumYsq genSU5 / sumT3sq genSU5 = 5 / 3 := by
  obtain ⟨h1, h2, _, _⟩ := su5_traces
  rw [h1, h2]; norm_num

theorem su5_sin2 : sumT3sq genSU5 / sumQsq genSU5 = 3 / 8 := by
  obtain ⟨h1, _, h3, _⟩ := su5_traces
  rw [h1, h3]; norm_num

theorem so10_sin2 : sumT3sq genSO10 / sumQsq genSO10 = 3 / 8 := by
  simp [genSO10, genSU5, sumT3sq, sumQsq, trT3sq, trQsq, t3, dc, Lf, Qf, uc, ec, nuc, Finset.sum_range_succ]
  norm_num

theorem e6_sin2 : sumT3sq genE6 / sumQsq genE6 = 3 / 8 := by
  simp [genE6, genSO10, genSU5, sumT3sq, sumQsq, trT3sq, trQsq, t3, dc, Lf, Qf, uc, ec, nuc, d5, l5,
    Finset.sum_range_succ]
  norm_num

/-- mutation control: an incomplete SU(5) multiplet (u^c dropped) does not give 3/8 -/
theorem incomplete_multiplet_breaks : sumT3sq genIncomplete / sumQsq genIncomplete ≠ 3 / 8 := by
  simp [genIncomplete, sumT3sq, sumQsq, trT3sq, trQsq, t3, dc, Lf, Qf, ec, Finset.sum_range_succ]
  norm_num

/-- generic step: with Tr T3 Y = 0, Q^2 splits, and sin^2 = 3/8 iff Tr Y^2 = (5/3) Tr T3^2 -/
theorem sin2_iff_five_thirds (t y : ℝ) (ht : 0 < t) (hy : 0 < y) :
    t / (t + y) = 3 / 8 ↔ y = 5 / 3 * t := by
  have hty : t + y ≠ 0 := by positivity
  rw [div_eq_iff hty]
  constructor <;> intro h <;> linarith

/-- single coupling g_gut: g_Y^2 Tr Y^2 = g_2^2 Tr T3^2 gives g_Y^2 = (3/5) g_2^2 -/
theorem gY_sq (g2s gYs : ℝ) (h : gYs * (10 / 3) = g2s * 2) : gYs = 3 / 5 * g2s := by
  linarith

/-- Pati-Salam: g_Y^2 = 1/(1/gR^2 + (2/3)/g4^2), sin^2 = g_Y^2/(gL^2 + g_Y^2) -/
noncomputable def gY2 (g4 gR : ℝ) : ℝ := 1 / (1 / gR ^ 2 + (2 / 3) / g4 ^ 2)
noncomputable def sin2PS (g4 gL gR : ℝ) : ℝ := gY2 g4 gR / (gL ^ 2 + gY2 g4 gR)

theorem sin2PS_formula (g4 gL gR : ℝ) (h4 : 0 < g4) (hL : 0 < gL) (hR : 0 < gR) :
    sin2PS g4 gL gR = 3 * g4 ^ 2 * gR ^ 2 / (3 * g4 ^ 2 * gR ^ 2 + gL ^ 2 * (3 * g4 ^ 2 + 2 * gR ^ 2)) := by
  unfold sin2PS gY2
  have h4' : g4 ^ 2 ≠ 0 := by positivity
  have hR' : gR ^ 2 ≠ 0 := by positivity
  have hd : 3 * g4 ^ 2 + 2 * gR ^ 2 ≠ 0 := by positivity
  have hden : 3 * g4 ^ 2 * gR ^ 2 + gL ^ 2 * (3 * g4 ^ 2 + 2 * gR ^ 2) ≠ 0 := by positivity
  field_simp
  ring

theorem sin2PS_equal_couplings (g : ℝ) (hg : 0 < g) : sin2PS g g g = 3 / 8 := by
  rw [sin2PS_formula g g g hg hg hg]
  have : g ^ 2 ≠ 0 := by positivity
  field_simp
  ring

theorem sin2PS_homogeneous (l g4 gL gR : ℝ) (hl : 0 < l) (h4 : 0 < g4) (hL : 0 < gL) (hR : 0 < gR) :
    sin2PS (l * g4) (l * gL) (l * gR) = sin2PS g4 gL gR := by
  rw [sin2PS_formula _ _ _ (by positivity) (by positivity) (by positivity),
    sin2PS_formula _ _ _ h4 hL hR]
  have : l ^ 2 ≠ 0 := by positivity
  have hden : 3 * g4 ^ 2 * gR ^ 2 + gL ^ 2 * (3 * g4 ^ 2 + 2 * gR ^ 2) ≠ 0 := by positivity
  field_simp

theorem sin2PS_not_fixed :
    sin2PS 2 1 1 = 6 / 13 ∧ sin2PS 1 1 3 = 9 / 16 ∧ sin2PS 1 1 1 = 3 / 8 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [sin2PS_formula _ _ _ (by norm_num) (by norm_num) (by norm_num)]; norm_num
  · rw [sin2PS_formula _ _ _ (by norm_num) (by norm_num) (by norm_num)]; norm_num
  · exact sin2PS_equal_couplings 1 (by norm_num)

/-- one-loop coefficients from the script's field-content formulas (3 generations) -/
def bSM : ℚ × ℚ × ℚ :=
  (3 / 5 * (2 / 3 * 3 * (10 / 3) + 1 / 3 * 2 * (1 / 4)),
   -22 / 3 + 2 / 3 * 3 * (3 * (1 / 2) + 1 / 2) + 1 / 3 * (1 / 2),
   -11 + 2 / 3 * 3 * (2 * (1 / 2) + 1 / 2 + 1 / 2))
def bMSSM : ℚ × ℚ × ℚ :=
  (3 / 5 * (3 * (10 / 3) + 2 * 2 * (1 / 4)),
   -6 + 3 * (3 * (1 / 2) + 1 / 2) + 2 * (1 / 2),
   -9 + 3 * (2 * (1 / 2) + 1 / 2 + 1 / 2))

theorem bSM_values : bSM = (41 / 10, -19 / 6, -7) := by
  simp only [bSM]; norm_num
theorem bMSSM_values : bMSSM = (33 / 5, 1, -3) := by
  simp only [bMSSM]; norm_num

/-- alpha_em^-1 = (5/3) alpha_1^-1 + alpha_2^-1, at unification -> (8/3) alpha_G^-1 and sin^2 = 3/8 -/
theorem unification_alpha_em (aG : ℝ) (haG : 0 < aG) :
    (5 / 3 * aG + aG = 8 / 3 * aG) ∧ (1 / (5 / 3 * aG + aG)) / (1 / aG) = 3 / 8 := by
  constructor
  · ring
  · have : aG ≠ 0 := haG.ne'
    field_simp
    ring

end M2Gut

#print axioms M2Gut.su5_traces
#print axioms M2Gut.su5_Q_decomposition
#print axioms M2Gut.su5_Y_over_T3
#print axioms M2Gut.su5_sin2
#print axioms M2Gut.so10_sin2
#print axioms M2Gut.e6_sin2
#print axioms M2Gut.incomplete_multiplet_breaks
#print axioms M2Gut.sin2_iff_five_thirds
#print axioms M2Gut.gY_sq
#print axioms M2Gut.sin2PS_formula
#print axioms M2Gut.sin2PS_equal_couplings
#print axioms M2Gut.sin2PS_homogeneous
#print axioms M2Gut.sin2PS_not_fixed
#print axioms M2Gut.bSM_values
#print axioms M2Gut.bMSSM_values
#print axioms M2Gut.unification_alpha_em
