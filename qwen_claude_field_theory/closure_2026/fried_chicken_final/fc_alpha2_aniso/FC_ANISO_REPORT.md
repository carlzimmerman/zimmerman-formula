# FC-AeST + c_2* Preferred-Frame alpha_2 — Full Report (PHASE 3)

**Candidate:** AeST action with c1=K_B, c3=-K_B, c4=0, c2* = K_B/(1-2K_B) (Maxwell
corner), K(Q) = -2Lambda + K2(Q-Q0)^2, K_B < 2.5e-5, c_T = 1 exact.
**Task:** compute alpha_2 via the full anisotropic O(w^2) boosted-source 1PN solve.
**Result:** alpha_2 DERIVED; **PPN-KILL-alpha2-too-large**.

---

## 1. GR-VALIDATION GATE — PASSED

`fc_aniso_grgate.py` builds the full anisotropic O(w^2) 1PN machinery (generic
10-component metric, no ansatz; boosted perfect-fluid source with rigid retardation
omega = k.w; harmonic-gauge trace-reversed propagator; gauge-invariant PPN extraction).
16/16 sympy certificates, exit 0:
- [C1] full linearized Einstein G1[h]=8πG T for all 10 components.
- [D2] gamma_PPN = 1. Order-counting resolution of the isotropic-ansatz failure: with
  U~eps^2, w~eps, the anisotropic w^2 U spatial terms are O(eps^4) = 2PN, beyond the
  O(eps^2) g_ij truncation — the machinery KEEPS them (so all 10 components close) but
  gamma is read at O(eps^2) => 1.
- [E1] alpha_1 = 0, [E2] alpha_2 = 0; [F1/F2] an independent boosted-Schwarzschild
  oracle reproduces (a,b,d) and alpha=0.
- [I1] reading alpha_2 from g_00 ALONE gives spurious, self-inconsistent nonzero values
  even for exact GR (the true cause of the old [D2] disagreement). The gauge-invariant
  2b+d fixes it. **This is the key lesson carried into PHASE 2.**

## 2. THE SOLVE — two independent routes

### Route A — Setup-M direct coupled {E_mn, E_Ai, E_phi} solve
`fc_solveA_setupM.py`, all gates pass, exit 0, ~107s. Aether at rest A=(1,0,0,0),
matter moving at w with rigid retardation, phi_bg = Q0 t so Q=Q0, Y=0. Full generic
10-component h_mn + covariant dark sector. Unit constraint A.A=-1 solved ALGEBRAICALLY
including the O(eps^2) temporal piece b_0 (REQUIRED — without it the O(w) scalar EOM is
diffeo-inconsistent by one equation; this was the actual blocker of prior attempts).
Gauge-invariant extraction alpha_1=-2(a+b)-(4gamma+4), alpha_2=-(2b+d)-1.
- GR limit reproduced: (a,b,d)=(-4,0,-1), alpha=0.
- EA Maxwell corner reproduced: alpha_1=-4K_B, alpha_2=0 exactly, all K_B.
- Static renorm Ghat/Gt = 2/(2-K_B) matches typeII.
- Full AeST, large-lam_s asymptotic: **alpha_2 = 1/lam_s + 2/(K_B lam_s^2) + O(lam_s^-3)**,
  alpha_1 = -4K_B + O(1/lam_s). Anisotropic consistency (rot/av/aw/cd across 3 w-samples)
  all True — the test the isotropic ansatz failed.

### Route B — Foster-Jacobson c-tensor map + independent Setup-M solve
`fc_solveB_partA_fj.py` (6/6) + `fc_solveB_final.py` (7 blocks, exit 0, ~33s).
- [C1] GR: alpha=0. [C2] VECTOR sector reproduces Foster-Jacobson EXACTLY (both c2 signs,
  K_B=1/4,1/10,1/100) — the published EA preferred-frame cross-check.
- [C3] cone speeds: ACTION -c2*(divA)^2 is luminal & alpha_2^EA=0 (HEALTHY corner);
  ACTION +c2* (the brief's literal sign) has s0^2=-1.003<0 = spin-0 GHOST. **The brief's
  '+c2*' is a sign typo; the healthy Maxwell corner is -c2*(divA)^2.**
- [C4] static Ghat: H00(on)/H00(off) = 1 + 1/J_Y.
- [C5] the J^mu grad_mu phi acceleration coupling IS the whole preferred-frame effect:
  OFF => alpha_1=-4K_B, alpha_2~0; ON => alpha_1=-2.70, alpha_2=+67.4 (huge).
- [C6/C7] **alpha_2 = 4/(J_Y(1+J_Y)) * 1/K_B** (genuine simple pole, residue certified
  to <3% over J_Y=1/2..20), alpha_1 = -8/(1+J_Y). Q0- and K2-independent.

## 3. RECONCILIATION — the routes agree

At beta_0~0.5 (lam_s=J_Y~2), K_B<2.5e-5:
- Route A: alpha_2 = 1/2 + 2/(4 K_B) = 0.5 + 0.5/K_B ~ 2.0e4.
- Route B: alpha_2 = 4/(2·3 K_B) = 0.667/K_B ~ 2.7e4.
- Agree to a factor 1.33 (pole-residue precision). Both give alpha_2 ~ 1e4 >> 1e-7.
- alpha_1 ~ -2.7 both routes (independent kill vs bound 1e-4).

Route A's headline "PASS" (alpha_2 = 1/lam_s ~ 8e-9) requires lam_s = J_Y = 1.3e8, i.e.
beta_0 = 7.7e-9 — the small-beta_0 SCREENING escape. Route A's own subleading term
2/(K_B lam_s^2) is the same 1/K_B pole Route B isolates; it is negligible ONLY under
that deep screening. Screening is CLOSED by the committed `fc_beta0_cassini_nogo_2026.py`
(Cassini-safe kernels need p>=4 => beta0_min>=0.27; the brief freezes beta_0~0.5).

## 4. VERDICT LOGIC

- PASS requires a point with |alpha_2|<1e-7 at (K_B<2.5e-5, beta_0~0.5, K2>0, lam_s>0,
  0<c_s^2<=1, c_T=1). With beta_0~0.5 frozen, lam_s~2 is fixed; the only free knobs are
  K_B (worsens the pole as K_B->0) and K2 (alpha_2 is K2-independent at leading order).
  alpha_2 is minimized at the largest allowed K_B=2.5e-5, giving ~2e4. **No such point
  exists.** Even the non-pole leading term 1/lam_s = 0.5 >> 1e-7.
- alpha_2 is DERIVED (GR + EA/FJ cross-validated), > 1e-7 throughout => **PPN-KILL**.
- Not INCONCLUSIVE: GR gate passed, solve closed (both routes, exit 0), gauge-invariant
  channels agree on sign/pole/scale.

## 5. MECHANISM

c2* at the Maxwell corner liberates the spin-0 aether mode with a soft kinetic term
~ c2* ~ K_B. The O(1) acceleration coupling 2(2-K_B) J^mu grad_mu phi sources it,
producing a 1/K_B strong-coupling response into the preferred-frame sector. The same
coupling drags alpha_1 to O(1) (-8/(1+J_Y)) when the scalar is unscreened. FC-AeST + c2*
therefore fails BOTH preferred-frame parameters at the Cassini-forced unscreened
beta_0~0.5, independently of J_10 (irrelevant at 1PN) and of K2.
