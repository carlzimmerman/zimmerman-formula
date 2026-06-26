# Route 3 (Horava non-projectable IR) — the preferred-FOLIATION Cassini-safe lensing partner: OBSTRUCTED. c_T=c PASS, ghost-window PASS, but delta-Phi=0 + position-dependent slip FAIL together (2026-06-17)

*The post-no-go open box, foliation side. Computed (sympy, not asserted) from the EXPLICIT non-projectable
Horava-Lifshitz IR action S = (1/16piG_H) int dt d3x N sqrt(g)[K_ijK^ij - lambda K^2 + (3)R + alpha a_i a^i],
a_i = d_i ln N. Primaries: Blas-Pujolas-Sibiryakov 0909.3525 + 1007.3503 (the healthy non-projectable
alpha a^2 term + scalar window), Jacobson 1001.4823 (IR = khronometric, the dictionary), Foster-Jacobson
gr-qc/0509083 (gamma=1). Script: route3_horava_nonprojectable_IR.py. Both ways.*

---

## Verdict: OBSTRUCTED — the smaller symmetry MOVED the obstruction (off the Bianchi leg) but did NOT lift it

| Demand | Horava-IR result (computed) | Pass? |
|---|---|---|
| (1) delta-Phi = 0 | The **spatial g_ij variation** gives `4 nabla^2 Psi - 4 nabla^2 Phi = 0` -> **Psi=Phi (gamma=1)**, with alpha PROVABLY ABSENT (`d/d alpha = 0`). delta-Phi=0 only with delta-Psi=0 (no lensing). | **FAIL where lensing needed** |
| (2) grad(dPsi)=2(g_obs-g_N) | The `alpha a_i a^i` (non-projectable) term lands ENTIRELY in the lapse/Phi channel; the lapse eq with Psi=Phi gives `(2 alpha - 4) nabla^2 Phi = kappa rho`, i.e. a **constant G_N renormalization** `G_N = G_H/(2-alpha)` (= Foster-Jacobson `G/(1-c14/2)`, alpha<->c14). No static position-dependent Psi-only slip exists. | **FAIL** |
| (3) c_T = c | **AUTOMATIC**: TT graviton has K=0, a_i=0 so lambda,alpha drop out; `c_T^2 = (3)R-coeff / K_ijK^ij-coeff = 1`. | **PASS (auto)** |
| (4) ghost-free | Open healthy khronon window EXISTS: `c_s^2 = ((2-alpha)/alpha)((lambda-1)/(3lambda-1)) > 0` for `0<alpha<2, lambda>1` (witness alpha=1/2,lambda=3/2 -> c_s^2=0.4286). | **PASS** |

**All four together: NO.** (3) and (4) are EASY and PASS in an open corner; (1) and (2) are MUTUALLY
EXCLUSIVE. delta-Psi=2(g_obs-g_N) is NOT derived — it can only be put in BY HAND as a free function
F(a^2), which (i) STILL lives in the lapse/Phi channel (moves Phi -> AeST/Cassini failure) and (ii) STILL
leaves the spatial eq Psi=Phi. Phenomenology in the wrong potential, not a derived Psi-only Lagrangian.

## The one genuinely-new result vs Route 4 (the task's core question, answered honestly)
The task asked: does the SMALLER foliation-preserving symmetry weaken the Bianchi obstruction enough to
allow the slip? **Partially yes, but it does not help.** Computed in Section 8:
- The covariant Bianchi leg forced a conservation-completing pressure `3 delta-p = -2 nabla^2 f != 0` that
  sources delta-Phi. In Horava the analogue is the **momentum constraint** (vary the shift N^i):
  `D_j(K^ij - lambda g^ij K) = 8piG_H T^0i/N`. Statically `K_ij=0`, so it is **trivially 0=0** — there is
  **NO forced delta-p**. The smaller symmetry genuinely DID remove the covariant Bianchi pressure-completion.
- BUT the slip is re-killed by a **DIFFERENT** equation — the **spatial g_ij variation** — which gives
  `nabla^2(Psi-Phi)=0` independent of alpha. The non-projectable `alpha a^2` term only touches the lapse
  (Phi) channel and cannot reach the g_ij equation. **The obstruction MOVED (Bianchi -> spatial-metric eq)
  but did NOT lift.** By the Jacobson dictionary (alpha<->c14, beta<->c13, lambda-1<->c2) this IS the same
  Foster-Jacobson gamma=1 no-go as Route 4, now derived from the foliation action.

## Both-ways honesty
- **Credited (genuine positives):** c_T=c is AUTOMATIC (c_T^2=1, no tuning); a ghost-free gradient-stable
  khronon window provably exists (0<alpha<2, lambda>1). Conditions (3),(4) are NOT the obstruction. The
  preferred foliation = the dS-Unruh cosmic rest frame the framework already needs. The smaller symmetry
  REALLY does kill the covariant Bianchi leg (trivial static momentum constraint) — a real, correct point.
- **Conceded (the obstruction, full weight):** the IR Horava action cannot make a pure (delta-Phi=0)
  static position-dependent MOND slip — the spatial g_ij equation locks Psi=Phi (gamma=1), and alpha a^2
  only renormalizes G_N (provably absent from the Psi-Phi equation, `d/d alpha = 0`). The slip needs a
  hand-put free function F(a^2) that moves Phi (AeST structure -> Cassini fails) and STILL leaves Psi=Phi.
- **Strong-coupling caveat (BPS):** the healthy scalar window needs alpha=O(1); the alpha->0 (projectable)
  limit decouples the khronon and sends the strong-coupling scale to 0. So there is no "small-alpha free
  pass" — the healthy corner has an O(1) G_N rescale, still no slip.

## What Carl CAN / MUST NOT say
- **CAN:** Route 3 (non-projectable Horava IR) is OBSTRUCTED, computed from the explicit action. c_T=c is
  automatic and a ghost-free khronon window exists (the EASY conditions), but delta-Phi=0 + a
  position-dependent slip FAIL together: the spatial-metric equation forces Psi=Phi (gamma=1) and the
  alpha a^2 term only renormalizes G_N. The smaller foliation symmetry genuinely weakened the *covariant
  Bianchi* leg (trivial static momentum constraint) — but the obstruction MOVED to the spatial-metric
  equation rather than lifting. Same wall as Route 4 / the covariant no-go, foliation side.
- **MUST NOT:** "Horava's smaller symmetry lets the slip through" (FALSE — re-killed by g_ij eq);
  "Route 3 passes all four" (2 of 4; slip + delta-Phi=0 fail together); "grad dPsi=2(g_obs-g_N) is derived
  in Horava" (hand-put F(a^2), and it moves Phi); "the alpha a^2 term sources a slip" (provably absent from
  Psi-Phi, d/d alpha=0). Quarantine held (a0/Z/kappa never asserted derived).

## One line
Route 3 (non-projectable Horava-Lifshitz IR) **OBSTRUCTED**: from the explicit action
`N sqrt(g)[K_ijK^ij - lambda K^2 + (3)R + alpha a_i a^i]` the weak-field spatial-metric (g_ij) equation
forces **Psi=Phi (gamma=1)** with the non-projectable alpha a^2 term PROVABLY ABSENT (sympy: d/d alpha=0),
so alpha only renormalizes `G_N=G_H/(2-alpha)` and there is NO static position-dependent Psi-only slip;
**c_T=c is automatic (c_T^2=1)** and a **ghost-free khronon window exists (0<alpha<2, lambda>1)** — the EASY
conditions — but delta-Phi=0 and the MOND slip are mutually exclusive, the slip only via a hand-put F(a^2)
that moves Phi (AeST/Cassini). The smaller foliation symmetry DID kill the covariant Bianchi leg (trivial
static momentum constraint) but the lock MOVED to the spatial-metric equation — **same wall, foliation
side** (Jacobson dictionary -> Foster-Jacobson gamma=1). A real result, not a manufactured Lagrangian.
