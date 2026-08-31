# v9 AeST preferred-frame PPN — terminal status: **KILL** (high confidence) — see V9_PPN_KILL_VERDICT.md

**RESOLVED 2026-08-31 (workflow wyzp0z5df, 7 agents, adversarially verified; alpha_1 re-derived by
hand). Terminal verdict = KILL on the healthy locus by TWO independent mechanisms:
(1) alpha_1 = -2(K_B+2) ~ -4.2, un-tunable, ~4.4e4x over Will |alpha_1|<1e-4 — the scalar J.grad(phi)
drag renormalizes eta_K=(K_B*J_Y+2)/(J_Y+1) to (K_B+2)/2>=1 at the physical deep field J_Y=1 (base
anchor -4K_B recovered as J_Y->oo). (2) alpha_2: the novel channel projects onto alpha_2 (not beta),
~1e4-1e5x over LLR, no K_B->0 decoupling. beta RETIRED (22+ orders safe). alpha_3==0 (DC-019 pass).
One residual: solar-profile background un-checked. Layer A untouched. FULL VERDICT: V9_PPN_KILL_VERDICT.md.**

---
*(Historical trail below — the calc as it developed from NOT-COMPUTED to the KILL above.)*

**Result of the boosted moving-source O(U)->O(wU)->O(w^2U) 1PN calc on the ACTUAL v9 F(Y,Q) action
(3 routes + consistency anchors + adversarial verify).**

## Confirmed (anchors met)
- Background reproduces v9 EXACTLY: K_Q(Q0)=0, K_QQ(Q0)=mu^2, a0Q(Q0)=0, a0QQ(Q0)=-kappa^2 G mu^2,
  bump'(Q0)=0, bump''(Q0)=2B(u); J_Y=1-e^{-u}=mu(u); w=-1; c_T=1.
- gamma_PPN=1 (Phi=Psi) met by all routes (no-slip identity lap(Psi-Phi)=0 at eps=0). Lensing sector OK.

## The decomposition  alpha_2^v9 = alpha_2^baseAeST + Dalpha2_K + Dalpha2_a0 + Dalpha2_B
- **Dalpha2_B (bump): PPN-SUPPRESSED ~1/u0 -> OUT of C0** (all routes agree; at Earth u0~6e7, bump~1.6e-8).
- **Dalpha2_K (K_QQ=mu^2): UNSUPPRESSED constant.**
- **Dalpha2_a0 (a0QQ): UNSUPPRESSED** — rides g(u)=dJ/d(a0^2)=(u^2+2u+2)e^{-u}-2 -> **-2** (nonzero constant,
  sympy-verified this session; g+2 exponentially small). So F_QQ(Q0) -> mu^2(1+kappa^2/4pi) survives u0>>1.

## KEY finding — the "novel terms are exponentially small at Solar-System u" ESCAPE IS DEAD
Route 2 claimed the a0-promotion/K_QQ deltas are charge-suppressed to exactly 0. Route 3 + independent
sympy REFUTED this: they ride g->-2, a nonzero CONSTANT, NOT 1/u0-suppressed. So the v9 novelty is NOT
PPN-shielded; v9_novelty_moves_alpha2 = TRUE.

## Why still NOT-COMPUTED (the owed calc)
- The geometric PROJECTION of the unsuppressed novel channel onto the w^2U (alpha_2) vs U^2 (beta) channel
  is uncomputed; requires the aether preferred-frame w-response delta A^i(w) from the FULL 5-EOM+A^2=-1 solve.
- base-AeST C0 = eta_K(eta_K-lam2)/(2 lam2), where eta_K = the owed E1 aether-anisotropy coefficient on the
  c123=0 GW-safe locus — NOT closed. C0_base=0 only on eta_K=0; no argument C0_novel vanishes there too.

## ⚠️ NEW LIABILITY (independent of alpha_2)
Naive counting (deltaQ ~ Qbar Phi) sends the leading UNSUPPRESSED novel piece to BETA's U^2 term, so v9 has a
distinct **|beta-1| exposure ~ Qbar^2 mu^2 (1+kappa^2/4pi)** that must be quantified. This is a real v9 PPN
liability surfaced by the calc, separate from the alpha_2 question.

## Decisive remaining calc
Solve the full {E_00,E_0i,E_ij,E_A^mu,E_phi}+A^2=-1 for rho=M delta^3(x-wt) to O(w^2U) with the INDEPENDENT
unit aether retained: get (a) eta_K on c123=0 (sets C0_base), (b) the projections Pi_K, Pi_a0 (alpha_2 vs
beta). Then test C0=0 jointly with alpha_1=-4 eta_K, gamma-1, beta-1 against Will bounds. Bump provably out.

## Standing
alpha_2^v9 remains the open certification gate; the easy screening/suppression escape is closed; a new
beta-1 exposure is now on the ledger. Layer A (R-2Lambda, a0=c^2 sqrt(Lambda/32pi)) unaffected.

## UPDATE (TARGET 2 computed): the projection Pi is now COMPUTED — it lands in ALPHA_2, not beta
Script: `aest_j10/wf2_target2_novel_projection_2026.py` (+ .out; all certificates pass).
Boosted anisotropic quadratic-action solve (two independent gauges + kx-scaling certificate +
Will-dictionary sympy certificate), Laurent split alpha_2 = c_-1/Q0^2 (contact, exterior-invisible)
+ c_0 (genuine, k-independent) + O(Q0^2) (Yukawa):
- **Pi_K -> alpha_2, UNSUPPRESSED and gauge-robust**: dc_0/dK2 |_(JY=1,Q0->0)
  = (4+4K_B-K_B^2)/(2-K_B)^3 (= 595/729 at K_B=1/5); exactly linear in K2; JY-form
  5(19JY+100)/(729 JY^2) at K_B=1/5 (dies ~1/JY only under JY->oo stiff-scalar screening;
  physical deep field is JY = mu(u0) = 1).
- **Pi_a0 (the novel increment)**: Delta alpha_2 = (kappa^2/4pi) K2 dc_0/dK2 ~ 1e-3..3e-2 for
  physical K2 ~ 0.1..1  =>  ~1e4-1e5 x over LLR |alpha_2| < 1e-7. The novel channel is an
  alpha_2 LIABILITY, not a beta one.
- **beta liability RETIRED**: (deltaQ)^2 has no gradient term; its U^2 exposure is
  (m_eff r)^2 (1+kappa^2/4pi) < 2e-27 inside 100 AU (m_eff^-1 = 4392 Mpc). The naive
  Qbar^2 mu2 (1+kappa^2/4pi) counting omitted that mu2 is dimensionful.
- Still NOT closed: the K2-free base offset of c_0 (= item (1), C0_base/eta_K): the two gauges
  disagree on it (-1771/405 vs -781/405 at K_B=1/5, JY=1) and the 11-field solve with E_h11
  retained is INCONSISTENT at O(wb^2) (rank 10, augmented 11) — a truncation-level broken
  constraint, exhibited in the script.
- Gauge-robust byproducts: alpha_3 == 0 exactly (DC-019 gate); alpha_1(Q0->0)
  = -4(K_B JY+2)/(JY+1) — base anchor (JY->oo after Q0->0) = -4K_B (FJ) PASSES, but at the
  physical deep-field point JY=1 this is alpha_1 = -2(K_B+2), i.e. eta_K renormalized to
  (K_B+2)/2 by the scalar drag — LIABILITY-IF-TRUE, needs the TARGET-1-grade independent
  verification before being quoted as a verdict.
