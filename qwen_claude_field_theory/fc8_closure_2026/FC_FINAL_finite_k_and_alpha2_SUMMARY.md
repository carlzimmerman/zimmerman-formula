# FC-FINAL (AeST + sharp mu_10) — finite-k dispersion & alpha_2: the J_10 factorization

**Question:** does J_10 (the MOND kernel choice) affect the two open AeST gates — the finite-k FLRW scalar
dispersion and the PPN alpha_2? **Answer: NO. Both gates are J_10-independent; they live entirely in the
AeST aether sector (K_B, K_2, Q_0).** Grounded in the frozen action (fc8_closure_2026/FROZEN_CANDIDATE.md,
mu_10=y/(1+y^10)^{1/10}, a_0=const) and the AeST literature.

## 1. J_10 drops out of the quadratic FLRW action — PROVEN
FLRW background has Y=0. mu_10(y)=y+O(y^11) => J_10(x)=x^3/3+O(x^13) => a_0^2 J_10(sqrt Y/a_0)=O(Y^{3/2}).
For a perturbation of order delta, Y=O(delta^2) => F_{J_10}=O(delta^3) => delta^2 S_{J_10}=0.
=> **omega^2_{J_10}(k) = omega^2_{AeST}(k)** exactly. No J_10 rescue at quadratic cosmological order.
(Matches fc7 sharp-kernel sequestration F_MOND=O(delta^3), and flrw_fc8.py.)

## 2. AeST scalar dispersion — PROVEN (literature-anchored)
Two branches: omega^2=0 (nonpropagating) and omega^2 = c_s^2 k^2 + M^2, with (lambda_s=1, FC-FINAL)
  c_s^2 = (2-K_B)(1+K_B/2)/(K_2 K_B) = (4 - K_B^2)/(2 K_2 K_B).
Gradient-stable (c_s^2>0) iff **0 < K_B < 2, K_2 > 0** (sympy-verified).
Causality c_s^2 <= 1 is a JOINT condition **K_2 >= (2-K_B)(1+K_B/2)/K_B**, NOT simply K_B>=1 (refines the old
c_s^2~1/K_B estimate): e.g. K_B=0.5 needs K_2>=3.75; K_B=1 needs K_2>=1.5; K_B=1.5 needs K_2>=0.583.

## 3. The genuine open threat is INHERITED, not J_10 — the low-k mode
The omega^2=0 branch has an UNBOUNDED HAMILTONIAN for sufficiently small k (AeST linear stability,
PRD 106,104041 / arXiv:2109.13287), transition near the AeST mass scale mu. J_10 does NOT cure it (it is
O(delta^3) on FLRW). This, plus the oscillatory 3rd spherical regime (2304.05134), is the real decider.

## 4. alpha_2 is J_10-independent at 1PN — PROVEN NO; numeric NOT-COMPUTED
At solar-system y=g/a_0>>1: 1-mu_10 = O((a_0/g)^10), astronomically tiny => d alpha_2 / d J_10 = 0 at 1PN.
=> alpha_2 = alpha_2^AeST(K_B, K_2, Q_0) + O((a_0/g)^10). The NUMERIC value requires the FC-FINAL -> aether
PPN map (Foster-Jacobson Maxwell point c_1=-c_3=K_B, c_2=c_4=0, PLUS the scalar-sector correction, PLUS the
gamma_PPN=1 engineering). The repo has never computed it (ACTIVE_THEORY.md: "alpha_1/alpha_2 for this F OWED,
never computed"). DO NOT fabricate.

## Terminal status of S_{AeST+J_10}
| gate | status |
|---|---|
| J_10 affects quadratic FLRW | PROVEN NO |
| finite-k propagating scalar omega^2=c_s^2 k^2+M^2 | PROVEN (c_s^2 above) |
| gradient-stable window | PROVEN: 0<K_B<2, K_2 above the causality floor |
| low-k omega^2=0 unbounded-H mode | FAILED-inherited (J_10 does not cure) |
| J_10 tunes alpha_2 | PROVEN NO at 1PN |
| numeric alpha_2(K_B,K_2,Q_0) | NOT COMPUTED (needs the aether PPN map) |
| full FLRW stability / all speeds | NOT COMPUTED |

**Intersection = CONDITIONAL.** The propagating scalar has a healthy 2D (K_B,K_2) window, but the two
deciders — the low-k Hamiltonian sign and the numeric alpha_2 — are pure AeST-aether-sector problems in
(K_B,K_2,Q_0), NOT J_10 problems. No J_10 miracle; the Cassini lever (J_10) is orthogonal to the FLRW/PPN
kinetic sector. The remaining fried-chicken calc is alpha_2^AeST(K_B,K_2,Q_0) + the low-k mode sign.
