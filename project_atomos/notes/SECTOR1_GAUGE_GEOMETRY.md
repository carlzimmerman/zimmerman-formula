# SECTOR 1 — GAUGE GEOMETRY: the forced-geometric web of the SM gauge sector + GUT embeddings

*Built per the geometric-web charter: catalog ONLY forced-geometric primitives (rep dims, |G|, Weyl orders, Dynkin
indices, Casimirs, measure factors, anomaly-closure conditions). All numeric claims sympy-verified exact, 2026-06-25.
No a₀/Z/κ injected. Same bar both ways: forced is labeled forced, free is labeled free.*

## Verified forced primitives (all exact)

**Anomaly + Yukawa closure pins ALL hypercharges to ONE scale.** Solving the linear anomaly conditions
([SU(3)]²U(1): 2y_Q+y_u+y_d=0 · [SU(2)]²U(1): 3y_Q+y_L=0 · grav²U(1): 6y_Q+3y_u+3y_d+2y_L+y_e=0) **together with**
Yukawa gauge-invariance (y_Q+y_d+y_H=0, y_L+y_e+y_H=0, y_Q+y_u−y_H=0) gives, in terms of y_Q alone:
`y_H=−3y_Q, y_L=−3y_Q, y_d=2y_Q, y_e=6y_Q, y_u=−4y_Q`. Setting y_Q=1/6 → the **entire observed pattern**
(y_L=−1/2, y_e=−1, y_d=+1/3, y_u=−2/3) and electric charges Q=+2/3, −1/3, −1, 0. **The cubic [U(1)]³ anomaly is then
AUTOMATICALLY zero** (`sympy.simplify = 0`) — it adds no new constraint, it is *implied*. This is the self-constraint:
the hypercharges are not 5 free numbers, they are 1 scale × a forced integer pattern, and the quantization of electric
charge (why Q_proton = −Q_electron exactly) is a *consequence*, not an input.

**sin²θ_W = 3/8 (tree, GUT) is forced two equivalent ways.** Over a complete SU(5) multiplet (5̄ = d^c×3, e, ν):
`sin²θ_W = Tr(T₃²)/Tr(Q²) = (1/2)/(4/3) = 3/8` (exact). Equivalently the GUT normalization `g₁²_GUT = (5/3) g_Y²` with
g₁_GUT=g₂ at unification gives `(3/5)/((3/5)+1) = 3/8`. The 3/8 and the 5/3 are the *same* forced fact.

**GUT group invariants (forced):** dim SU(5)=24, SO(10)=45, E₆=78. One generation: SU(5) 5̄+10=**15**, SO(10) **16**
spinor (= 15 + ν_R), E₆ **27** = 16+10+1. Weyl orders |W(A₄)|=5!=120, |W(D₅)|=2⁴·5!=1920, |W(E₆)|=51840. Coxeter h:
SU(5)→5, SO(10)→8, E₆→12. Casimirs C₂(adj)=N, C₂(fund)=(N²−1)/2N, T(fund)=½ for every SU(N).

**β-coefficients are rep-dim-forced:** SM one-loop (GUT-norm U(1)) `(b₁,b₂,b₃)=(41/10, −19/6, −7)`; the 4/3·n_gen
generation piece + the forced 11, 22/3 gauge/ghost pieces. Forced difference ratio (b₁−b₂)/(b₂−b₃)=218/115. MSSM
`(33/5, 1, −3)`.

## Honest both-ways anchor to real data
- Measured sin²θ_W(M_Z)=0.23122±0.00003; tree GUT 3/8=0.375 must RUN down. GQW one-loop SU(5) → ~0.20; **plain-SM
  running misses 0.231 by a few %** (the known near-miss); MSSM tightens it. So the gauge interlock is real in FORM,
  fails the precision second-observable test in the *minimal* SM — that is the honest status, not a win.
- The 3 coupling *values* (α_em, α_s, sin²θ_W as inputs) are FREE. What is forced is the *embedding structure* that, IF a
  GUT holds, collapses them to one α_GUT — a near-interlock, not a closed one in the minimal SM.
