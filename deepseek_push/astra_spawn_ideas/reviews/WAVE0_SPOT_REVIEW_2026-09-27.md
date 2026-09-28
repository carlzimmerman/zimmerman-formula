# Orchestrator independent review — wave 0A/0B headline claims (spot check)

**Date:** 2026-09-27 · **Reviewer:** hermes-orchestrator (independent of workers) · **Status:** spot-pass

Scope: independent numerical re-derivation of the load-bearing empirical/algebraic
claims from the landed waves, before downstream gates reuse them. This is a review
role attached to existing results (per ORCHESTRATOR.md §7), not a duplicate task.

## AS009 — Σ/phantom-cap failure on RAR and MONO (reviewed: PASS)

Claim: h_RAR peak 0.6476·a0 at y_p = 2.53964; h_mono(y*) = 0.647 > 1/2 at splice
y* = 2.337412; h grows logarithmically on the continuation; hence the slab ceiling
premise g_φ < a0/2 (used for Σ_φ,tot < a0/(4πG)) fails on RAR and on operative MONO.

Recomputed independently:
- h_RAR(y*) = 0.646960 (claim 0.647) ✓
- h_p = h_RAR(2.53964) = 0.647610 (claim 0.647610) ✓ exact
- h_mono(10) = 0.677539, h_mono(100) = 0.745582, h_mono(10⁴) = 0.893896 (claim 0.8939 ✓)
- Q-branch cap (sqrt(y²+y) − y) < 1/2 for y ∈ {0.1, 1, 5, 100}: 0.232/0.414/0.477/0.499 ✓
  (consistent with the worker's Lean-certified Q strict cap)

Verdict: the cap-failure finding is real and quantitatively reproduced; it properly
restricts the ZD07 slab-ceiling transfer to the Q branch (or a future filtered-MONO
bound). No correction needed.

## AS010 — P(r_M) = a0²/(8πG) (reviewed: PASS)

Recomputed: canonical 5.224953e-12 Pa (claim 5.22495e-12 ✓); alternative 7.583953e-12 Pa
(claim 7.58395e-12 ✓). Exact coefficient 1/(8π) confirmed; no footing mixing.

## AS003 — Ω_L identity and closure exclusion (reviewed: PASS)

Ω_L(can) = (32π/3)(a0/(H0c))² = 0.68493 (claim 0.68493 ✓, vs Planck 0.6847 — ratio
0.9999, i.e. the alternative footing at H0 = 67.203 km/s/Mpc realizes closure by
construction). Exclusion of "closure value 1" at 43.2σ: |1 − 0.68493| = 0.31507;
with Planck 2018 σ(Ω_Λ) = 0.0073 → 43.2σ ✓ (43.16). Worker's z-score uses the correct
reference sigma; verified consistent.

## Scope note

Full independent reproduction of every Lean certificate remains outstanding (per
contract, certificates are verified at review time — 21 .lean files on record).
The spot check above covers the claims most likely to be reused downstream.
Remaining review queue: systematic recompile audit of all 21 certificates
(recommended as a dedicated bounded review task before closure synthesis).
