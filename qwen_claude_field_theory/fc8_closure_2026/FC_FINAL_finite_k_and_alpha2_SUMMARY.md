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

---
## CORRECTIONS from the adversarial workflow (literature-anchored PRD 106,104041 + sympy, det U=0 re-solved)
1. **lambda_s = 0 for J10, NOT 1.** J10 has NO analytic linear-Y term (J=O(Y^{3/2})), so lambda_s=J_Y(0)=0
   exactly. Hence the SOLID sound speed is c_s^2(J10) = (2-K_B)/(K_2 K_B) = 2(2-K_B)/(K_B K''(Q0))
   -- WITHOUT the (1+K_B/2) factor. Normalization set by K_2=K''(Q0)/2 (dark-energy/dust curvature);
   for CMB-fit K_2~1e3-1e8, c_s^2~1e-4..1e-9 (deeply subluminal). M^2=(2-K_B)Q0^2/K_B.
2. **"K_B>=1 causality" was a RED HERRING.** The real subluminality floor is K_B >= 2/(K_2+1), which is
   ~2/K_2 << 1 for CMB-fit K_2 -- met throughout the BBN window K_B in [~2e-4, 0.25]. (K_B>=1 combined with
   BBN K_B<=0.25 would have spuriously EMPTIED the set.) And superluminal-in-aether-frame builds no CTCs, so
   subluminality is non-binding anyway. Causality gate = SATISFIED/NON-BINDING.
3. **alpha_2 Maxwell degeneracy CONFIRMED independently** (c123=c1+c2+c3=K_B-K_B=0 => alpha_2 simple pole,
   singular), PLUS alpha_1(aether)=-4K_B (finite, SOLID). KEY CONDITIONAL: if the scalar does NOT cancel the
   aether preferred-frame terms, |alpha_1|=4K_B<1e-4 forces K_B<2.5e-5 -- ~4 orders below BBN's 0.25 (near-kill);
   if it DOES cancel (as the same tuning gives gamma_PPN=1, Phi=Psi), alpha_1,alpha_2 small at larger K_B. Which = NOT-COMPUTED.
4. **Low-k mode:** lambda_s=0 pushes k_*->infinity, so SZ21's linear "unbounded only for k<k_* < mu" reassurance
   is LOST; boundedness for mu<k rests on the NONLINEAR |Y|^{3/2} MOND term (SZ Eqs.B31-B32). SOLID no-instability
   on Minkowski for the propagating branch; SUGGESTIVE on the FLRW/dS background (full constrained dS dispersion NOT-COMPUTED).

## Terminal verdict: S_{AeST+J10} = CONDITIONAL (neither empty nor non-empty)
Gradient stability + causality jointly SATISFIABLE on the BBN band K_B in [2e-4,0.25] (large K_2); the SOLE
undecided gate is |alpha_2|<~1e-7. THE ONE DECIDING CALCULATION: an AeST preferred-frame PPN expansion (aether
boosted vs matter rest frame, O(v) source) WITH the propagating scalar phi retained -- Foster-Jacobson redone
for AeST -- to regulate the c123=0 pole and return finite alpha_1(K_B), alpha_2(K_B). I.e. does the phi sector
cancel the aether preferred-frame parameters (the way it engineers gamma_PPN=1, Phi=Psi), or is K_B forced below
~1e-5? That single calc decides viable-vs-dead. NO number fabricated.
