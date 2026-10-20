# CFG899: alpha door D08, the charged vector boson in dS_4 with a covariant completion (closes S1) (FROZEN pre-registration)

Written 2026-10-20, before any script of this lane was written or run. No script of this lane exists when this file is committed. I read the campaign rules and doors (`../CFG895_alpha_campaign_ledger/`), the S1 lane (`real_research/alpha_principle_2026/S1_vector_bosons/`: pre-registration with Amendments 1-5, lane notes, the four outputs), AH4 (`real_research/alpha_schwinger_2026/ah4_induced_current_ds4.py`), the AH3 Lean statement, Q1's `q1_lib.py`, S2's heavy-mass script and output (`S2_fermion_independent/s2_4_heavy_mass_current.py/.out`), and the READMEs/pre-registrations of CFG896, CFG901 and CFG906. Every number in section 3 is pencil arithmetic on those committed results.

**Status declared in advance: STRUCTURAL CLOSURE, not a value trial.** This lane cannot output a value of alpha: alpha (that is, e) stays a free symbol throughout, and no number is compared with 137.036 at any point. So it is **not counted as a post-ledger attempt; N_mech stays 374.** It gets a ledger row as a structural item (like AH4, Q1, S1: Trials "-").

**Record rules restated.** The Schwinger/Unruh route (AH1-AH4, N5, Q1, Q2, S1, S2) is a NO-GO in dS_2 and dS_4: every horizon response is alpha x G(m/H) with a free mass function (AH3 Lean certifies the premise-to-conclusion step). The SM mass sector is WALLED: no mass is used or derived; m is a free symbol (mu = m/H). kappa and the record's Z play no part. Alpha stays an INPUT; kappa = 1/2 stays FITTED. Never "theory closed".

## 1. The S1 question (precise)

S1 (commit 61f3895cf) computed the induced current of ONE complex Proca field (unitary gauge, gyromagnetic ratio g = 2 via the Corben-Schwinger term; g = 1 reported) in the dS_4 planar patch with the "constant" electric field F_{tau z} = E a^2 (lambda = eE/H^2, mu = m/H). It found: sigma/H = alpha G_v(mu) structurally; a finite G only for the decoupled W_y polarization; the coupled {W_x, W_z} block has no finite renormalised current: after the AH4/Q1 second-order adiabatic subtraction its remainder is log-divergent, with a mass-dependent log coefficient c_{-1}/lambda = c_inf + a/mu^2 (fit c_inf = 6.837, a = 5.12 at g = 2; c_inf = 1.032, a = −1.57 at g = 1) and a mass-dependent quadratic term c1/lambda = −(8/3 + 4/(3 mu^2)) at g = 2: non-renormalisable H^2/m^2 divergences. Its "next step": a covariant regularisation plus a Higgs/Goldstone completion.

**The question CFG899 answers.** With the Higgs/Goldstone completion of the charged W in the background-covariant R_xi gauge and a covariant regulator (Pauli-Villars or point-splitting):
* (Q-a) Is the induced current renormalisable: is its only divergence a charge renormalisation, with the one-loop W running coefficient (b = −7 for g = 2, i.e. "7" in S1's c_{-1}/lambda units) and no mass-dependent (H^2/m^2) divergence?
* (Q-b) Is the finite part sigma/H = alpha G_v(mu) well defined: regulator independent after a stated renormalisation condition, and gauge-parameter independent?
* (Q-c) Does any condition of the covariant system select alpha (a forced kernel), or is it closure only?

## 2. Setup (field content, gauge, background, regulators)

* **Units, background.** H = 1, planar patch, conformal time tau < 0, a = −1/tau, metric a^2 eta (signature −+++, MTW curvature: R = 12, R_mn = 3 g_mn). Background A_z = f(tau) with f = −E/tau for the dS field (F_{tau z} = E a^2), as in AH4/S1/S2. D = nabla − i e A on charge-e fields; Omega_mn := [D_m, D_n] on a charge-e scalar = −i e F_mn.
* **Fields (the charged sector of the electroweak theory in a photon background).** W (complex vector, charge e, mass m, gyromagnetic ratio g; g = 2 is the Yang-Mills value, g = 1 is reported), the charged Goldstone phi (complex), and the FP ghosts of the complex gauge parameter (c, cbar: two complex Grassmann scalars). The neutral fields (h, the neutral Goldstone, Z, photon fluctuations) do not couple to the background at one loop and do not contribute to the current. A curvature coupling zeta R |H|^2 of the Higgs does not enter: it is a function of |H|^2, so by the Goldstone theorem the Goldstone mass from the potential is zero at the minimum (it only shifts m).
* **Action.** sqrt(−g) [ −(1/2) Wbar_mn W^mn − m^2 Wbar W + p Wbar^m Omega_mn W^n − |D phi − m W|^2 − (1/xi) |D.W − xi m phi|^2 ] + ghosts, with p = g − 1 (Pauli term) and the background-covariant R_xi gauge-fixing function G = D.W − xi m phi. Ghost operator from delta W = D theta, delta phi = m theta: −box + xi m^2.
* **Regulators (the door's two options).** R-PV: one Pauli-Villars partner per field (mass M, weight −1, Sum c = 0). R-PS: covariant point-splitting with the Hadamard/DeWitt-Schwinger subtraction at scale mu_PS. Both are represented through the DeWitt-Schwinger (heat-kernel) expansion of the one-loop effective action; the current is J^m = delta Gamma/delta A_m.
* **Renormalisation condition (graded).** On-shell (decoupling) charge: the flat-space vacuum polarisation of every massive field vanishes at q^2 = 0 (S2's scheme; equivalent at O(1/m^2) to the AH4/Q1 adiabatic scheme, as S2 verified). An MS-bar-like condition at a fixed scale is reported (it shifts G_v by a mu-independent constant).

## 3. Hand derivations (pencil; the script must CHECK them, not assume them)

* **H1 (mixing).** The W-phi cross terms of −|D phi − m W|^2 and of the gauge-fixing term cancel up to a total derivative for every xi and every background (integration by parts with D; no commutator needed). After it: W sector −(1/2)|W_mn|^2 − m^2|W|^2 + Pauli − (1/xi)|D.W|^2; Goldstone −|D phi|^2 − xi m^2 |phi|^2.
* **H2 (operators).** With [D_n, D_m] W^n = R_sm W^s + Omega_nm W^n: Delta_xi W = −box W + Ric W + m^2 W − g Omega.W + (1 − 1/xi) D (D.W), where (Omega.W)_m = Omega_m^n W_n. At xi = 1 it is Laplace type, Delta_1 = −(box + E_V) + m^2 with **E_V = −Ric + g Omega** (matrix on the vector index) and bundle curvature Omega_ij(bundle) = Riem_ij + Omega_ij 1. Goldstone and ghosts: −box + xi m^2 (minimal). One-loop: Gamma = Tr ln Delta_xi + Tr ln(−box + xi m^2) − 2 Tr ln(−box + xi m^2) = Tr ln Delta_xi − Tr ln(−box + xi m^2). Count 4 + 1 − 2 = 3 = the Proca count.
* **H3 (intertwining).** Delta_g (D theta) = D (Delta_0 theta) + (2 − g) Omega.D theta − (nabla^n Omega_nm) theta, Delta_0 = −box + m^2 (Ric cancels). So the longitudinal (pure-gauge) modes decouple iff **g = 2 and nabla^n F_nm = 0**. In the dS background nabla_n F^{nz} = −2EH/a ≠ 0 (AH4 V3, S2 D0c): the constant-E background is not a vacuum Maxwell solution, so the BRST/longitudinal decoupling is broken by a defect K_m = −(nabla^n Omega_nm), proportional to the background's Maxwell equation. This is the same object as S1's constraint source "(d_n F^{nm}) W_m". For the vacuum-Maxwell background F_{tau z} = const (conformal frame) the defect vanishes.
* **H4 (exact gauge-parameter dependence, g = 2).** With D theta =: Dop theta, Dop^dag W = −D.W, Delta_xi = Delta_1 + (1/xi − 1) Dop Dop^dag, the Sylvester identity and H3 give, exactly,
  Gamma(xi) − Gamma(1) = Tr ln[ 1 − (1 − xi) (Delta_0^(xi))^{-1} Dop^dag Delta_1^{-1} K ],  Delta_0^(xi) = −box + xi m^2.
  Consequences: (i) it vanishes identically on vacuum-Maxwell backgrounds (K = 0); (ii) the F^2 coefficient (charge renormalisation, and the whole constant-F Euler-Heisenberg Lagrangian) is xi-independent; (iii) at O(F^2, 1/m^2) the xi-dependence is c(xi) Int K^2/m^2 = c(xi) Int (nabla^j F_ij)^2/m^2 (S2's structure S2), with no curvature correction at this order (curvature x K^2 is dimension 8). Whether c(xi) ≠ 0 is **computed, no hand value**. Recalled (not opened): background-field-method gauge-boson self-energies depend on the quantum gauge parameter off-shell (Denner-Weiglein-Dittmaier 1994-95); expectation: c(xi) ≠ 0.
* **H5 (decomposition at xi = 1, all mu).** Goldstone − 2 ghosts = −1 minimally coupled complex scalar of mass m: with chi = a phi its mode equation is AH4's (Whittaker index mu_w^2 = 9/4 − lambda^2 − mu^2), so **J_scalar part = −J_AH4(lambda, mu) exactly, at every mu**. In Delta_1 (k_y = 0) W_y decouples with S1's equation (W_y'' + (P^2 + mu^2/tau^2) W_y = 0, index 1/4 − lambda^2 − mu^2). The remaining {W_tau, W_x, W_z} block is a 3-component coupled system with an indefinite metric (W_tau has the wrong-sign kinetic term in Feynman gauge) and is **not solved in this lane** (no closed form; a mode sum is out of budget).
* **H6 (UV, heat kernel a_2).** F^2 part of tr a_2 = (1/360)(30 tr Omega_ij Omega^ij + 180 tr E^2). Ratio to one complex scalar: Delta_1(g): 4 − 6 g^2; Goldstone − 2 ghosts: −1; **R_xi total 3 − 6 g^2, b = 1 − 2 g^2 = −7 (g = 2), −1 (g = 1)**; massless Yang-Mills part (vector − 2 ghosts) 2 − 6g^2 → −22/3 at g = 2, Goldstone +1/3 (S1 B3's split); Dirac 4 (b = 4/3, Q1). No mass, no xi in these coefficients, so the current's divergence is b ln(Lambda^2/m^2) times the charge-renormalisation current nabla_n F^{nm} only: **no H^2/m^2 divergence**. tr E_F = g Omega^a_a = 0, so a_1 has no F: **no Lambda^2 term** in the current. Flat proper-time factor of the R_xi system (x/sinh x)(1 + 2 cosh g x) [x^2 ratio 3 − 6g^2]; electric continuation (x/sin x)(1 + 2 cos g x): leading Schwinger-pole weight 1 + 2 cos(g pi) = **3 (g = 2)** (S1 B4/B5's ratio 3), −1 (g = 1). In D dimensions: (D − 3 + 2 cosh 2x): ratio D − 25 (−21 at D = 4), pole weight D − 1.
* **H7 (regulators).** Proper time: R-PV gives Int ds s^{n−3}(e^{−s m^2} − e^{−s M^2}): n = 2 → ln(M^2/m^2), n = 3 → 1/m^2 − 1/M^2. R-PS gives Int ds s^{n−3} e^{−s m^2 − sigma/(4s)}: n = 2 → 2 K_0(m sqrt(sigma)) = −ln(m^2 sigma/4) − 2 gamma_E + O(sigma), Hadamard-subtracted → −ln(m^2/mu_PS^2) + const; n = 3 → (2 sqrt(sigma)/m) K_1 → 1/m^2. a_0, a_1 carry no F. Hence J_PV − J_PS = J_a2 [ln(M^2/mu_PS^2) + const], m-independent, proportional to b nabla_n F^{nm}: a mu-independent constant in G_v. The only local conserved current of dimension 3 linear in F is nabla_n F^{nm}. **The door's K = 2 regulators collapse to one after the renormalisation condition.**
* **H8 (heavy mass, a_3, xi = 1).** Reduction of the recalled a_3 (the coefficient set validated in S2: 8, 2, 12, −12, −6, −4, 5, 6, 60, 30, 60, 30, 10, 4, 12, 30, 12, 5, −2, 2; R^V = −R^MTW) to S2's structures S1..S6 (coefficients x q^2/360):
  * scalar (E = −xi_R R): (−8, −2, −12, 6, 4, −5 + 30 xi_R) [S2];
  * Delta_1(g) (tr 1 = 4, E_R = −Ric = −(R/4)1, E_F = g Omega): **(−32 + 30 g^2, −8, −48 + 60 g^2, 24 − 60 g, 16, 10 − 15 g^2)**; the term linear in g is the cross term 2 tr(E_F Riem_ij) Omega^ij of 30 tr(E Omega Omega) (same structure as the Dirac's −2 S4 in S2 at g = 1).
  * Per-structure dS currents (sigma_HFY M^2 per unit coefficient, bosonic prefactor −1/(16 pi^2 m^2 360)), inferred from S2's committed scalar and Dirac results with S1 = −S3 (integration by parts): u = (1/360, −1/720, −1/360, 1/360, −1/240, −1/60)/pi^2, with u_{F^2} = −1/(720 pi^2); consistent with the Bianchi identity Int S1 = 2 Int S2 − 4 Int F^2 in dS.
  * **sigma_HFY M^2: Delta_1(g) = (3g^2 − 3g − 2)/(18 pi^2); R_xi total = (4g^2 − 4g − 5)/(24 pi^2) = 1/(8 pi^2) (g = 2), −5/(24 pi^2) (g = 1).** With G = 4 pi sigma_HFY: **G_v mu^2 → (4g^2 − 4g − 5)/(6 pi) = 1/(2 pi) = 0.159155 (g = 2)**; scalar 7/(18 pi) = 0.123787 (AH4), Dirac −1/(9 pi) (Q1).
* **H9 (flat q^4 coefficient, xi = 1).** Delta_1 = 4 scalars + the spin bubble −(1/2)Tr(G V_s G V_s), V_s = −g Omega; in units of (e^2/16 pi^2) Int F^2: scalar (1/4)[(1/3) L − (1/30) q^2/m^2], spin −(g^2/2)[L − (1/6) q^2/m^2], L = ln(Lambda^2/m^2). Ratio of the R_xi (xi = 1) q^4 coefficient to the scalar's: **3 − 10 g^2 = −37 (g = 2), −7 (g = 1)**; the a_3 flat combination (c1 − c3 + c2/2) gives the same: (9 − 30 g^2)/3.
* **H10 (gauge shift in dS).** r(xi) := [c4(xi) − c4(1)]/c4_scalar (flat q^4 coefficients, same machinery). The shift Lagrangian is 6 r(xi) S2 (in the scalar's normalisation), so delta(sigma_HFY M^2) = 6 r u2 = −r(xi)/(120 pi^2), **delta(G_v mu^2) = −r(xi)/(30 pi)**. Expected: r ≢ 0; r ~ ln xi as xi → infinity (the unitary limit diverges: S1's non-renormalisable divergence reappears as ln xi); r singular as xi → 0 (massless unphysical scalars; the heavy expansion needs xi m^2 >> H^2). Informational only: identifying ln xi with ln(Lambda^2/m^2), S1's a would correspond to (coefficient of ln xi in r)/30; this identification is heuristic, no gate.

## 4. What counts as "alpha selected" versus "closure"

* **Selected (a forced kernel, class K1):** a consistency condition of the covariant system (finiteness, regulator independence, gauge independence, unitarity) that holds only for particular e; or a covariant observable G_v(mu, xi) that is independent of mu and xi, so that a tie sigma/H = c would fix alpha = c/G_v (and even then c itself must be forced, else the kernel is K0).
* **Closure:** the covariant current is computed to the stated order, every condition holds for all e, and G_v depends on mu (and/or xi), so alpha = c/G_v(mu, xi) is a function, not a number (AH3 `no_alpha_from_obs`, `tie_coupling_differs`).
* **Classifier E1** on G_v(mu) over mu in {3, 5, 10, 20} (heavy regime): SELECTED iff max|G|/min|G| <= 1 + 1e-6 with one sign; else NOT SELECTED. If the O(1/mu^2) coefficient were exactly 0 the classifier is NOT DIAGNOSTIC at this order.

## 5. Inputs and contamination

No measured input of any kind. e, E, m, H, xi, g, M, mu_PS are symbols; the numbers used are group and heat-kernel numbers, the recalled a_3 coefficients (as validated in S2), and the record's committed closed forms (AH4 (2.58) via Q1's `scalar_closed_f`, Q1's `hfy_weak`) evaluated at symbolic-free test points. No alpha, no alpha proxy, no fitted real, no kappa, no Z. Contamination test: not applicable (nothing measured); the substitution test is replaced by check A7 (e enters only through e A).

## 6. Option space

| Axis | Options | Status |
|---|---|---|
| Regulator (the door's K = 2) | **R-PV**, R-PS | shown to differ only by a mu-independent constant (H7) |
| Gyromagnetic ratio | **g = 2** (Yang-Mills), g = 1 (minimal; not a gauge theory) | g = 1 reported |
| Gauge parameter | **xi = 1** (Feynman-'t Hooft), continuous family xi > 0 | family reported (Part D) |
| Renormalisation condition | **on-shell charge**, fixed-scale (MS-bar-like) | constant shift reported |

No graded value trial exists (no alpha is output). **N_mech unchanged (374).**

## 7. Leverage pre-flight (rules §1.6)

At fixed (mu, xi) sigma/H = alpha G_v, so d ln(sigma/H)/d ln alpha = 1. But the only candidate selection equation, a tie sigma/H = c, has a chosen constant c (K0) and G_v carries the free mu (and xi): **NON-DIAGNOSTIC for alpha by construction** unless G_v turns out mu- and xi-independent (E1). The lane's value is structural: it settles S1's open item.

## 8. Checks (script `cfg899_d08.py`; sympy/mpmath, one process)

Exact means a sympy identity (residual 0); tolerances otherwise as stated.

**A. Structure (dS_4, Lorentzian, exact).**
* A1 geometry: R = 12, R_mn = 3 g_mn, R_mnrs = g g − g g (MTW), nabla Riem = 0, |nabla_n F^{nz}| = 2E at tau = −1 (AH4 V3, S2 D0c).
* A2 operator identity: the Euler-Lagrange operator of the xi = 1 action (generic complex W_m(tau, x, y, z), Pauli p = g − 1) equals −box + Ric + m^2 − g Omega (overall sign fixed by the m^2 term), g in {1, 2}.
* A3 mixing: the W-phi cross terms have identically vanishing Euler-Lagrange derivatives (total derivative) for symbolic xi.
* A4 intertwining: Delta_g(D theta) − D(Delta_0 theta) − (2 − g) Omega.D theta + (nabla^n Omega_nm) theta = 0 (generic theta), g in {1, 2}. A4b: at the graded g, the defect on the vacuum-Maxwell background F_{tau z} = const vanishes identically; on the dS background it equals −(nabla^n Omega_nm) theta ≠ 0.
* A5 Goldstone/ghost mode equation → AH4's (index 9/4 − lambda^2 − mu^2).
* A6 W_y (k_y = 0) decouples in Feynman gauge, equation = S1's (index 1/4 − lambda^2 − mu^2).
* A7 AH3 premise: every operator is invariant under (e, A) → (s e, A/s).

**B. UV structure.**
* B1 a_2 ratios computed from explicit traces (vector bundle with E_V and Omega(bundle); Dirac with explicit gamma matrices; scalar): Dirac 4; Delta_1(g) 4 − 6 g^2; R_xi 3 − 6 g^2; **gate: b(graded g) = −7 exactly** and the split −22/3 + 1/3; g = 1 → −1 (reported).
* B1b K-tests on committed numbers: b_s = 1/3 = AH4 V3's coefficient; b_D = 4 b_s (Q1); ratio −21 (S1 B3); S1 E4's exact-mode c_inf (parsed from S1's committed `s1_4_vector_uv_and_current.out`): 6.837 and 1.032 within 5% of −b = 7 and 1.
* B2 no mass dependence of the F^2 part of a_2 and tr E_F = 0 (no Lambda^2), exact; the dS current of the a_2 F^2 term has a mu-independent coefficient.
* B3 regulators: the proper-time integrals and Bessel expansions of H7 (sympy); J_PV − J_PS is m-independent and proportional to the a_2 current.
* B4 proper-time factors: x^2 ratio 3 − 6g^2; electric pole weight at x = pi equals 3 at the graded g (S1's 3); D-dimensional count gives ratio −21 at D = 4.

**C. Heavy mass (a_3) in dS.** My own trace code: E and Omega(bundle) as explicit matrices in the dS chart, covariant derivatives with the bundle connection, every term of the 1/360 group of the recalled a_3, the F^2 part extracted with a scaling parameter (the linear part must vanish); then S2's `current_from_L` (imported read-only).
* C0 K-tests (positive controls, known answers of the record): scalar (7/18 − 2 xi_R)/(4 pi^2) for xi_R in {0, 1/6, 1/12} exactly with MY trace code; Dirac −1/(36 pi^2) with S2's committed reduction; **AH4's closed form**: Richardson of mu^2 G_s(mu) (lambda = 1e-6; mu = 10, 20, 40) → 7/(18 pi) within 1e-5 relative; **Q1's closed form**: mu^2 G_f → −1/(9 pi) within 1e-6 (mu = 20, 40, 80).
* C1 vector bundle: sigma_HFY M^2 of Delta_1(g) equals the hand reduction (3g^2 − 3g − 2)/(18 pi^2) for g in {0, 1, 2}, and each single-structure current equals the hand u_i (code-consistency gate; a mismatch is diagnosed and disclosed).
* C2 R_xi total at xi = 1: sigma_HFY M^2 and G_v mu^2 (expected 1/(8 pi^2), 1/(2 pi) at g = 2); the physical current is tau-independent (dS invariance).
* C3 flat a_3 combination on a Euclidean plane wave (same trace code): ratio of the R_xi (xi = 1) q^4 term to the scalar's (expected 3 − 10 g^2); feeds D-G3.

**D. Gauge dependence (flat Euclidean momentum space, general xi; "route D").** Gamma^(2) at O(a abar) for the background a e^{iqx} + c.c., vector propagator P_T/(k^2 + m^2) + xi P_L/(k^2 + xi m^2), vertices from −D^2, (1 − 1/xi) D D. and −g Omega, minus one scalar of mass xi m^2; Taylor in q (q^2: log coefficient; q^4: convergent), 4D angular average, exact radial integrals. The K-formula route computes −(1 − xi) Tr X − (1/2)(1 − xi)^2 Tr X^2 at O(a abar) from H4 with the same machinery.
* D-G1 Ward identity: for the longitudinal polarisation the q^4 integral and the q^2 log coefficient vanish (xi in {1/2, 1, 2}, g in {1, 2}).
* D-G2 scalar positive control: c4/cL = −1/10.
* D-G3 xi = 1: route D's q^4 ratio = C3's a_3 flat ratio (exact).
* D-G4 log ratio cL(xi)/cL_scalar = B1's 3 − 6 g^2 for xi in {1/2, 1, 2, 3}, both g (charge renormalisation xi-independent).
* D-G5 (g = 2): route D's c4(xi) − c4(1) = the K-formula's, exactly (symbolic xi, or at xi in {1/2, 2, 3} if the symbolic integral stalls); the K-formula has no q^2 log term.
* Reported: r(xi) in closed form; values at xi = 0.1, 1/2, 2, 3, 10, 100; the ln xi asymptotics; g = 1's xi dependence (no gauge symmetry, reported only); the dS shift delta(G_v mu^2) = −r/(30 pi) with u2 from S2's pipeline; the finite q^2 part's xi difference is NOT graded (4D-cutoff routing ambiguity of the quadratically divergent parent).
* **Part-D verdict:** GAUGE DEPENDENT at O(1/mu^2) if r ≢ 0 and D-G1..G5 pass; GAUGE INDEPENDENT at O(1/mu^2) if r ≡ 0 and the gates pass; NOT ESTABLISHED if a D gate fails.

**E. Selection.**
* E1 classifier (section 4) on G_v(mu) from C2; positive controls: planted constant G → SELECTED; planted 1/(2 pi mu^2) → NOT SELECTED.
* E2 no condition constrains e: finiteness (B), on-shell gauge independence (A4/H4) and g = 2 hold for symbolic e; every computed coefficient is e-free after the overall e^2.

## 9. Verdict rules (frozen)

* **CLOSED, NO SELECTION** iff every check in A, B (incl. B1b), C0, C1, C2 and E passes and E1 says NOT SELECTED. The README states the Part-D verdict beside it.
* **NOT COMPLETED** if any A, B, C or E gate fails: the closure is not established, and the failing part is named.
* If E1 says SELECTED, that is reported as found, with every caveat; it is not expected.
* Real-run exit 0 iff CLOSED; exit 2 otherwise.

## 10. MUTATE and positive controls (rules §1.9)

* **MUTATE_SPIN** (load-bearing element: the gyromagnetic coupling, g = 2 → 1 in every graded computation). Must FAIL: B1 (b = −1, not −7), A4b (the on-shell defect (2 − g) Omega.D theta ≠ 0), B4 (pole weight −1, not 3), D-G5 (H4 holds only at g = 2). L-SPIN (must pass): the mutated b, pole weight, R_xi sigma_HFY M^2 and flat q^4 ratio equal the real run's g = 1 values exactly (−1, −1, −5/(24 pi^2), −7).
* **MUTATE_DIM** (load-bearing element: the dimension in the multiplicity count, D = 4 → 6, i.e. tr 1 of the vector bundle in a_2 and the proper-time spin factor). Must FAIL: B1 (ratio −19, b = −19/3) and B4 (weight 5). L-DIM (must pass): ratio = D − 25 = −19, weight = D − 1 = 5. The 4D-only parts (A, C, D) run unchanged.
* Exit: 1 iff every targeted check fails and every L-check passes (the control works); 3 otherwise.
* Positive controls: C0 (AH4, Q1 known answers), D-G2 (scalar), E1's planted G.

## 11. Expected outcome (written before computing)

**CLOSED, NO SELECTION.** In R_xi the current is renormalisable: the divergence is a pure charge renormalisation with b = −7 (g = 2), xi- and mass-independent; S1's mass-dependent log (a/mu^2) and quadratic (4/(3 mu^2)) terms are absent (they are unitary-gauge artefacts); the regulators differ by a constant. The finite part exists in every R_xi gauge; in Feynman gauge G_v mu^2 → 1/(2 pi) at large mu (g = 2). Part D: expected GAUGE DEPENDENT at O(1/mu^2), because the dS constant-E background is off-shell (H3, H4): G_v is then not a gauge-invariant observable beyond its log coefficient. sigma/H = alpha G_v(mu, xi) with a free mass and gauge parameter: no tie fixes alpha. A wrong expectation will be disclosed, not hidden.

## 12. Disclosures made before freezing

* No script of this lane was written or run before this commit; section 3 is pencil arithmetic on committed record results.
* Recalled, not read in this lane: Vassilevich's a_3 (the coefficient set is the one S2 recalled and validated on the Dirac and scalar heavy-mass limits; its individual coefficients are not each validated); the DeWitt-Schwinger/Hadamard facts of H7; the BFM gauge-parameter literature of H4 (expectation only); Nielsen identities (named only); the Goldstone theorem in a constant-curvature background. No download.
* The cross term (linear in g) of H8 is validated only through its Dirac analogue in S2 and the code-consistency gate C1; the flat terms are validated by D-G3.
* Not done here: the finite-mu current of the 3-component Feynman block (G_v at mu of order 1), O(1/mu^4), non-linear response in lambda, the dS pair-production factor of the vector, backreaction, other charged species, S1's g = 2 dynamical instability at large lambda/mu^2 (not re-examined; this lane is linear response).
* Compute: one core, `OMP_NUM_THREADS=1 nice -n 10 python3 -B`, PYTHONDONTWRITEBYTECODE=1, a watchdog aborting above 900 MB peak RSS, target under 10 minutes per run. S2's and Q1's modules are imported read-only with bytecode writing disabled; no file of another lane is written. A 1024^3 run is live: nothing heavier runs.
* Stop rule (rules §6): first result on D08.

## 13. Files (planned)

`CFG899_PREREGISTRATION.md` (this file, committed alone first), `cfg899_d08.py`, `cfg899_d08.out` / `.json` (real run), `cfg899_d08_MUTATE_SPIN.out` / `.json`, `cfg899_d08_MUTATE_DIM.out` / `.json`, `README.md`.
