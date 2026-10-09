# TORUS, ONE-PARAMETER CONTINUOUS WILSON-LINE FAMILIES — FROZEN CRITERIA (committed before any script)

Setup as TORUS_WILSON (M_L = M_R = 3, M_H = 6, ψ_ζ(z) = ψ(z + ζ), ζ_H = (ζ_L + ζ_R)/2, single-valuedness gate).
Why one parameter: three masses have two ratios; a model with two free knobs fitted to both ratios fixes Q by
construction (no test). With ONE knob fitted to m_μ/m_e, Q (i.e. m_τ) is a prediction.

PRE-DECLARED families (x ∈ [0, 1), Higgs single mode k ∈ {0..5}):
 F1 ζ_L = x, ζ_R = 0     F2 ζ_L = ζ_R = x     F3 ζ_L = x, ζ_R = -x     F4 ζ_L = x τ, ζ_R = 0
 each for τ ∈ {i, e^{2πi/3}}  → 8 families × 6 Higgs modes.
Procedure: scan x on 400 points, find every x with m_μ/m_e = 206.768283 (non-degenerate spectrum), refine,
read Q.  PASS only if some solution has |Q - 0.666661| < 3e-5 AND the number of such solutions exceeds the
chance expectation (number of fitted solutions × 6e-5 / spread of their Q values).  KILL otherwise.
Report every fitted solution's Q and m_τ/m_μ.
