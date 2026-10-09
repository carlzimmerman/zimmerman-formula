import Mathlib

/-!
# KOIDE_FLUX_SOURCE -- what can set the generation-ring flux?

KOIDE_HOLONOMY: Koide's Z3 invariant 3δ is the gauge-invariant flux Φ through the three-generation ring.
Two live targets (KOIDE_PHASE showed they cannot both be exact):
  Koide branch   (r = √2 exact):  Φ ∈ [0.6666661401, 0.6666661425]  (from m_μ/m_e, scratch door4.py);
  Brannen branch (Φ = 2/3 exact): then r = √2 (1 - 2.13e-7), Q = 2/3 - 1.42e-7, m_τ = 1776.9665 MeV (scratch).
The topological class of mechanisms gives Φ = 2π n / N: a Dirac-quantised flux 2πn shared equally by N
plaquettes (a polyhedron's faces, a lattice's cells, a Z_N holonomy).

CERTIFIED:
(A) `farey_bound`: if a/b < n/N < c/d with bc - ad = 1 then N ≥ b + d (the Farey-neighbour lemma).
(B) `koide_branch_needs_huge_N`: if Φ ∈ [0.6666661401, 0.6666661425] and Φ = 2πn/N (N > 0), then
    N ≥ 113088.  Uses Farey neighbours 9320/87839 and 2679/25249 and Mathlib's 20-digit π bounds.
    No polyhedron or lattice with fewer than 113088 plaquettes per flux quantum gives the Koide-branch flux.
(C) `brannen_branch_not_quantised`: there are NO integers n, N (N ≠ 0) with 2/3 = 2πn/N (π is irrational).
    The Brannen-branch flux cannot come from ANY topological (quantised) mechanism.
CONCLUSION (stated, follows from B, C): the flux must be a continuous, radian-valued phase: a charge times a
holonomy in natural units (Φ = q ∮A), a dynamical phase (ΔE T/ħ), or a logarithm from running.  In that class
the Brannen value 2/3 rad would read as q = 2/3 times one unit of holonomy, or as Φ = Q.  These are READINGS,
not derivations: nothing in the record supplies a unit holonomy or ties Φ to Q.
NOT CERTIFIED: the Φ interval and the Brannen-branch numbers (scratch, mpmath; masses quoted from PDG).
-/

namespace KoideFluxSource
open Real

theorem farey_bound (a b c d n N : ℤ) (hb : 0 < b) (hd : 0 < d) (_hN : 0 < N)
    (hdet : b * c - a * d = 1) (h1 : a * N < n * b) (h2 : n * d < c * N) : b + d ≤ N := by
  have e : N = b * (c * N - d * n) + d * (n * b - a * N) := by linear_combination (-N) * hdet
  have i1 : 1 ≤ c * N - d * n := by linarith
  have i2 : 1 ≤ n * b - a * N := by linarith
  nlinarith

theorem koide_branch_needs_huge_N (Φ : ℝ) (n N : ℤ) (hN : 0 < N)
    (hl : (0.6666661401 : ℝ) ≤ Φ) (hu : Φ ≤ 0.6666661425) (h : Φ = 2 * π * n / N) : 113088 ≤ N := by
  have pl := pi_gt_d20
  have pu := pi_lt_d20
  have hNr : (0 : ℝ) < N := by exact_mod_cast hN
  have hpi : 0 < π := pi_pos
  have key : (n : ℝ) * (2 * π) = Φ * N := by rw [h]; field_simp
  -- lower: 9320 * N < 87839 * n
  have low : (9320 : ℝ) * N < 87839 * n := by
    have : (9320 : ℝ) * (2 * π) < 87839 * Φ := by nlinarith
    nlinarith
  have up : (n : ℝ) * 25249 < 2679 * N := by
    have : 25249 * Φ < (2679 : ℝ) * (2 * π) := by nlinarith
    nlinarith
  have low' : (9320 : ℤ) * N < n * 87839 := by
    have : (9320 : ℝ) * N < n * 87839 := by linarith
    exact_mod_cast this
  have up' : n * 25249 < (2679 : ℤ) * N := by exact_mod_cast up
  have := farey_bound 9320 87839 2679 25249 n N (by norm_num) (by norm_num) hN (by norm_num) low' up'
  linarith

theorem brannen_branch_not_quantised : ¬ ∃ n N : ℤ, N ≠ 0 ∧ (2 / 3 : ℝ) = 2 * π * n / N := by
  rintro ⟨n, N, hN, h⟩
  have hNr : (N : ℝ) ≠ 0 := by exact_mod_cast hN
  have hn : (n : ℝ) ≠ 0 := by
    rintro hn; rw [hn] at h; simp at h
  have hpi : π = ((N / (3 * n) : ℚ) : ℝ) := by
    push_cast
    field_simp at h ⊢
    linarith
  exact irrational_pi.ne_rat _ hpi

end KoideFluxSource

#print axioms KoideFluxSource.farey_bound
#print axioms KoideFluxSource.koide_branch_needs_huge_N
#print axioms KoideFluxSource.brannen_branch_not_quantised
