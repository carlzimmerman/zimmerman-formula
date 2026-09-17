# RH06 -- THE LOG-MOMENT SEQUENCE (second-order falsification, 2026-09-17)

1. **VERDICT [branch C, MIXED]**: the framework's member-pinned spine
   n!·0.6746^n is NOT realized: κ₂=0.910/κ₃=1.842/κ₄=4.970 vs measured
   0.49191/0.38104/0.31042 → z = 62/192/569σ (FAIL ×3).
2. Measured on 1500 TRUE zeros (zetazero dps=15, 151 s; rho(t)=(1/2π)ln(t/2π)
   unfolded, unit-mean): κ₁=0.67504±0.00492, κ₂=0.49191±0.00676,
   κ₃=0.38104±0.00763, κ₄=0.31042±0.00818 (naive se; bootstrap CIs in JSON).
3. κ₁ reproduces the RH01 pin (0.6746±0.0035, 1σ) and GUE (0.6706, 0.9σ) —
   lane pipeline validated.
4. Exact-GUE MC (24×500, same recipe as RH01b): κ₂=0.49492, κ₃=0.39243,
   κ₄=0.32946 → sides with the zeros on κ₂ (z=0.45) and κ₃ (z=1.49) [PASS].
5. κ₄: GUE off at 2.05σ (naive, both errors folded) → FAIL under the
   pre-registered strict 2σ rule; framework off at 569σ. "Neither."
6. C1 identity κ_n = n!/(λ-1)^n = n!·κ₁^n EXACT n=1..4 (sympy residual 0 on
   λ-1>0 + numeric at λ=2,5/2,3) [PASS]; K1/K3/K4 kills not fired [PASS].
7. Rigidity note (post-hoc): lag-1 autocorr −0.31..−0.41 → std/√N is
   conservative; block-bootstrap se shrinks ~4-8×, pushing κ₃/κ₄ to ~3.5/4.8σ
   from GUE — consistent with slow early-zero convergence, never framework.
8. **Conclusion**: zeros' log-moment sequence is GUE's (κ₂,κ₃); single-moment
   pin (κ₁=0.6746) was a coincidence of one number; the ladder's full spine is
   dead at 62-569σ. No RH claim.
9. Files: RH06_moment_sequence.py/.out, RH06_results.json,
   RH06_zeros_spacings_cache.npz, this summary. Nothing committed.
10. Checks: 3/3 PASS (C1 identity, K3 unfolding sanity, K4 GUE sample size).