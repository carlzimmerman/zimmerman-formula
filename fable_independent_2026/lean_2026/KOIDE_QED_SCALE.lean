import Mathlib

/-!
# KOIDE_QED_SCALE -- can QED running make Koide AND δ = 2/9 exact at one common scale?

Brannen (MASSES2.pdf, eqs 17-19) already found exact Koide ⇒ δ = 0.22222204715(312) and δ = 2/9 ⇒ η² =
0.49999978688(380): the two are slightly incompatible at pole masses (KOIDE_PHASE re-derived this
independently; it is NOT new).  His suggested way out is a second-order correction.  Test: one-loop MS-bar QED
running, m_i(μ) = M_i [1 - (α/π)(1 + (3/4) ln(μ²/M_i²))], one free parameter μ, two conditions.

CERTIFIED (`log_shift_scale_free`): to first order, ln m_i(μ) - ln m_j(μ) shifts by (3/2)(α/π) ln(M_i/M_j),
independent of μ and of the universal constant.  So a one-loop scale cannot select a point: every μ gives
the same flavour-dependent distortion.
NUMERIC (KOIDE_QED_SCALE.py / _py.out, mpmath): the running masses sit at Q - 2/3 ≈ +1.1e-3 and δ - 2/9 ≈
-1.1e-3 for every μ from 0.5 MeV to 1 TeV (both tau inputs, 1776.93 and Belle II 1777.09).  The pole-mass
tension (~2e-7) is ~5000× smaller than the running distortion: it is not a QED-running effect, and Koide and
the 2/9 phase are pole-mass relations only.
-/

theorem log_shift_scale_free (k c L a b : ℝ) :
    (-c - k * (L - 2 * a)) - (-c - k * (L - 2 * b)) = 2 * k * (a - b) := by ring

#print axioms log_shift_scale_free
