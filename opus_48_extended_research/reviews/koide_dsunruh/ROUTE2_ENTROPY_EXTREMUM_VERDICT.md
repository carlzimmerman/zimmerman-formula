# Route 2 — Entropy / Information Extremum attack on Koide — VERDICT: NULL (168th re-labeling)

**Date:** 2026-06-25
**Script:** `route2_entropy_extremum.py` (sympy 1.13.1 + mpmath dps=40)
**Task:** Is r=√2 / Q=2/3 / cos²=3/4 a CRITICAL point of a NATURAL information/entropy functional
defined WITHOUT mentioning 2/3? Distinct from the 4 prior attacks (dS-Unruh IR loop, EJA/Dirac
normalization, equipartition steelman, relational exhaustion) — a flavor-sector variational/info
extremum, not a thermal loop.

## VERDICT: NULL.
Q=2/3 is **not** the non-circular extremum of any natural entropy/information functional.

### The findings (all sympy/mpmath-exact)
- **Q(r)=1/3+r²/6 is a featureless monotone convex parabola** on r∈[0,∞). dQ/dr=r/3 (zero only at
  r=0), d²Q/dr²=1/3 constant. **2/3 is a GENERIC INTERIOR VALUE of Q** — no max/min/inflection. It
  carries no extremal meaning as a value of Q itself.
- **Unconstrained max-entropy** of the mass distribution → r=0 (uniform/perfectly democratic),
  NOT r=√2. H(p(r)) is monotone-decreasing in r (1.099 at r→0 → 0.150 at √2). Max-ent KILLS Koide.
- **Constrained max-ent** (fix any dispersion via a Lagrange multiplier) gives a Gibbs p_k∝exp(−λf_k)
  whose r is a FREE function of λ scanning all of [0,∞). The entropy principle does not prefer any λ;
  the constraint VALUE is an external input. NON-DIAGNOSTIC of √2.
- **Shannon H(p), H(q), Fisher information I_F, Renyi-2 IPR** — NONE has an interior stationary point
  at √2. Their extrema are at r=0 or nowhere on (0,∞).
- **The IPR smoking gun:** the inverse participation ratio Σq_k² of the sqrt-mass distribution
  q_k=√m_k/Σ√m is **IDENTICALLY Q** (sympy: Σq_k² = (Σm)/(Σ√m)² = 1/3+r²/6). So "information
  functional = 1/2 ⟹ Koide" is literally "Q=2/3" rewritten — the cleanest re-labeling.

### The one apparent hit — and why it is the 168th re-labeling
The democracy-deviation balance **F3 = D·(1−D)** with **D = cos²(v,(1,1,1)) = 1/(3Q) = 2/(r²+2)**
peaks at **r=√2 EXACTLY** (F3''(√2)=−1/4<0, a genuine MAX). But:
1. **The smuggle:** x(1−x) peaks at x=1/2 (target-free), and D=1/2 ⟺ 1/(3Q)=1/2 ⟺ **Q=2/3** ⟺ r=√2.
   The 2/3 enters through the *choice of the variable D whose half-value is Q=2/3*.
2. **Coordinate non-invariance (the killer):** the argmax of g·(1−g) moves off √2 for every other
   equally-natural [0,1] concentration measure — g=D^0.5→2.449, g=D^1.5→1.084, g=D²→2×10⁴,
   exp(−CV²)→1.177, Shannon-H/log3→1.522. Only the exact pre-privileged g=D=1/(3Q) (≡1/(1+CV²),
   sympy-verified identical) pulls back to √2. "Balance D at 1/2" is coordinate-equivalent to
   "impose Q=2/3." Not independent.
3. **Cross-fermion falsified:** D·(1−D) is flavor-blind, so maximizing it would drive quarks to
   D=1/2 (Q=2/3) too. They sit OFF the max (up D=0.393→0.238, down D=0.456→0.248, leptons D=0.500→0.250).
   No charged-lepton-specific ingredient in any functional.

### Both-ways discipline
- Not a manufactured win: the lone hit (D(1−D)) fails coordinate-invariance and cross-fermion, and
  its "1/2" is the Q=2/3 target wearing a coordinate disguise. IPR≡Q makes the circularity exact.
- Not a reflexive dismissal: the hit IS a real, exact maximum at √2 — examined, traced, and killed by
  the same rigor as a claimed win (the coordinate-covariance sweep is the decisive test, not a wave-off).

The last door (Route 2, entropy/information extremum) is **closed**. No maximal-re-verification flag.
SM mass sector stays WALLED. Quarantine held (2/3/√2/cos²=3/4 enter only as the target, never asserted derived).
