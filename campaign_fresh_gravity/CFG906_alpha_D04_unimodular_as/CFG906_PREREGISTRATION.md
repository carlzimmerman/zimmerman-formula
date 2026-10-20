# CFG906: alpha door D04, unimodular asymptotic safety f_g (FROZEN pre-registration)

Written 2026-10-20, before any script of this lane was written or run. No script of this lane exists when this file is committed. I read the record's code and reports (AS1-AS3, lane B, CFG895, CFG896, CFG901) and did the hand derivations of section 10 with pencil arithmetic only.

This is **attempt #3 of the post-ledger alpha campaign** (rules: `campaign_fresh_gravity/CFG895_alpha_campaign_ledger/ALPHA_CAMPAIGN_RULES.md`; door: `ALPHA_DOORS.md`, section D04; attempt #1 was CFG896, door D02; attempt #2 was CFG901, door D03). Nothing here is expected to derive alpha. KILLED, NOT DIAGNOSTIC and CONSISTENT-at-best are normal outcomes. The door's ceiling is CONSISTENT (single coupling; rules §4.3, corollary K9).

**Wall note.** The Standard-Model mass sector is WALLED. No mass is used or derived: the gravitational fixed point depends only on field counts. kappa and the record's Z play no part. Alpha stays an INPUT of the record.

**Record rule restated (rules §0.3).** Asymptotic safety gave 1/alpha(0) = 91-96 (89-97 with systematics) in AS1-AS4, not 137; 137 needs f_g about 4x smaller than every computed value. AS4's frozen admissibility rule also rejects the published BMS pure-gravity fixed point (disclosed in AS4). This lane does not use AS4's rule or the BMS scheme.

## 1. Mechanism

In asymptotically safe gravity the graviton fluctuations add −f_g g_Y to the hypercharge beta function, beta_gY = −f_g g_Y + (41/6) g_Y^3/(16 pi^2). If f_g > 0 the interacting zero g_Y* = 4 pi sqrt(6 f_g/41) is IR-attractive, and on the predictive trajectory g_Y(M_P) = g_Y*. In **unimodular gravity** the metric determinant is fixed (sqrt g = sqrt g-bar), the gauge group is transverse diffeomorphisms (TDiff), and Lambda is an integration constant that is not a coupling of the action. So the flow has a single gravitational coupling g (no lambda), the graviton fluctuation is traceless, and f_g is evaluated at the unimodular fixed point g*. The door asks whether this removes the factor ~4 between the record's f_g and the f_g = 0.009805 that 137.036 needs.

## 2. Forced-kernel candidate and class (rules §2)

* **C(alpha) = 0** is beta_gY(g_Y; f_g) = 0 at its interacting zero, with f_g = f_g(g*) evaluated at the fixed point of the unimodular Einstein-Hilbert flow with SM matter. **Class K1** (UV completeness plus IR attractivity), conditional on the asymptotic-safety scenario and on unimodular gravity being the right gravitational theory.
* **Why discrete.** beta_gY = 0 has roots 0 and ±g_Y*; the IR-attractive interacting root is the predictive one. In the unimodular EH truncation the fixed-point condition for g is linear in 1/g (section 4.2), so the interacting fixed point is unique: no root selection is needed.
* No content, scale or count is chosen: the matter content is the SM (as in AS3, so that the K-tests reproduce AS3), and every scheme choice is enumerated in section 6.

## 3. Which alpha, which scale, which scheme

* **Prediction:** alpha(0), the Thomson limit. Target 1/alpha(0) = 137.035999177 (CODATA 2022), used only as the target.
* **UV quantity:** g_Y* imposed at M_P = 1.220890e19 GeV (lane B `rg_common.MPL`): 1/alpha_Y*(M_P) = 41/(24 pi f_g).
* **Downstream (graded map):** lane B C5's one-loop chain by import, unchanged, as in AS3 and CFG901: P = 41/(24 pi f_g) + (41/(12 pi)) ln(M_P/M_Z) + alpha_2^-1(M_Z) [measured] + Delta_0 [measured, 9.106]. dP/d ln f_g = −41/(24 pi f_g): −55.2 at the required f_g.
* **UV cross-check with no measured alpha (reported, must agree in verdict):** 41/(24 pi f_g) against Y1-central's 1/alpha_Y(M_P) = 55.234 (built from measured data, target only).
* **Running error (rules §1.3):** Y1's sigma(1/alpha_em)/137.036 = 8.8e-4, i.e. 0.1206, inside sigma_route (section 7).

## 4. The truncation and the f_g expression

### 4.1 Truncation (declared)

Gamma_k = −Z_N,k ∫ d^4x sqrt(g-bar) R(g) with det g = det g-bar, plus the Maxwell term (1/(4 e^2)) ∫ sqrt g g g F F for hypercharge, plus SM matter (type-I traces, Litim cutoff, exactly AS2/AS3's `X_matter`), plus the TDiff gauge fixing and its ghosts. No cosmological coupling: in unimodular gravity the vacuum term ∫ sqrt(g-bar) Lambda is field independent, so its flow does not enter any Hessian. Regulator: Litim, type I, the CPR procedure of AS2 (R_k = H(P_k) − H(Delta) for each Hessian H, with the d_t Z_N ("eta") terms kept, as in AS3). f_g is evaluated at the fixed point, where d_t f' = 2 f' (eta_N = −2), as in AS3.

### 4.2 The unimodular flow of g (not in the repository; derived here by this frozen procedure)

The published unimodular fixed points (Eichhorn arXiv:1301.0879 and 1501.05848, recalled, named by the door as its gate) are **not in the repository, and nothing is downloaded**. So the beta function is derived here from the record's AS2 machinery, and the door's external gate is replaced by internal gates (section 8). This is a weakness of the lane and is disclosed.

* **Background:** S^4 (AS2's heat kernels from the spectra). On S^4 the unimodular EH equations (R_mn − g R/4 = 0) hold for every radius, so S^4 is on-shell for unimodular gravity at any R-bar. For traceless fluctuations, the unimodular Hessian therefore equals the f(R) Hessian of AS2's `cpr_blocks` with f(R-bar) replaced by f'(R-bar) R-bar/2 (the f(R) on-shell condition), f'' = 0, restricted to traceless modes (TT, xi, sigma; no trace mode), and with CPR's gauge-fixing term removed. Derivation: with the linear constrained parametrisation g = g-bar + h-hat + g-bar tr(h-hat^2)/8 + ..., sqrt g is exact and ∫ R^(1)[g-bar phi] = −R-bar ∫ phi supplies the term that f(R-bar) sqrt(g)^(2) supplies in the unconstrained theory. Gates K4 test the result.
* **York decomposition** of the traceless fluctuation: h-hat = h^TT + (nabla xi + nabla xi) + (nabla nabla − g nabla^2/4) sigma, Jacobian det_VT(D − R/4)^(1/2) det_S(D(D − R/3))^(1/2) (D = −nabla^2), as in AS2.
* **Blocks** (D = −nabla^2; from AS2's blocks with F0 -> F1 R/2, F2 -> 0):
  * TT: H = −(F1/2)(D + R/6), i.e. −(F1/2)(Delta_L − 2 Lambda) with Lambda = R/4 (the massless spin-2 operator on S^4).
  * sigma: H = (3/16) F1 D^2 (D − R/3). sigma is **not** a gauge mode under TDiff, so it stays.
  * xi: gauge, frozen by the TDiff gauge fixing (1/(2 alpha_T)) ∫ F^T F^T, F^T = transverse part of nabla^n h-hat_nm = −(D − R/4) xi, alpha_T -> 0, not scaled by Z_N (CPR/AS2's convention "the gauge parameter does not run"); FP ghosts on transverse vectors with operator (D − R/4); Jacobian J_V. (At eta = 0 the net VT factor, det_VT(D − R/4)^(+1/2), is independent of the gauge-fixing form.)
* **Measure (axis A).** With the local measure D h-hat (TT, xi, sigma) the on-shell one-loop partition function equals GR's times det_S(D)^(−1/2) (derived by hand, section 10.1; GR's on-shell form is det_VT(D − R/4)^(1/2)/det_TT(D + R/6)^(1/2)). The recalled literature (de Leon Ardon-Ohta-Percacci 2018; Kugo-Nakayama-Ohta 2022; not read) states that unimodular gravity and GR agree at one loop on-shell.
  * **M-eq (graded):** the measure that restores one-loop on-shell equivalence: an extra real scalar factor det_S(D)^(+1/2), i.e. the trace term −(1/2) Tr_S[d_t R_k/(P_k)] with no eta term.
  * **M-naive (reported):** the local measure, no extra factor.
* **sigma regulator convention (axis B).** CPR (graded): sigma un-normalised, the regulator applied to the full sixth-order H(D), Jacobians as separate traces (AS2's convention). Normalised (reported): sigma rescaled by its Jacobian, H = (3/16) F1 D, regulator applied to that, no J_S.
* **Projection.** d_t f1 = [R^1] X/(16 pi^2), with X = (16 pi^2/V) Tr[...] from AS2's `trace_R2` (order 1), f1 = g~1 = −1/(16 pi g). At the fixed point d_t f1 = 2 f1, so **g* = −2 pi / X1(e = 2)**, where X1(e) is the R^1 coefficient and e = d_t f1/f1. The R^0 coefficient is the vacuum term and is not used.
* **Admissible:** 0 < g* < 50 (AS2's domain) and the eta denominator 16 pi^2 g~1 − A1 nonzero on (0, g*]; otherwise NOT DIAGNOSTIC.

### 4.3 f_g (flat background, constant F-bar; AS1/AS2 method)

The record's method (AS1 `as1_g1_fg_flat.py`, AS2 `fg_flat_cpr`, AS3 `as3_roots_report.py`) is used unchanged except for the field space: F-bar^2 coefficient of the graviton-photon part of the Wetterich trace, q = kappa e_4, q^2 -> P_k in the kinetic matrix, eta terms d_t f' (P − q^2) on the graviton block, angular average (tr C)/12 F F with the parity check, radial integral ∫ kappa^3 dkappa/(8 pi^2), f_g = 2 e^2 c_FF. AS1's `bilinear_action` supplies the EH kinetic form, the photon blocks and the vertices.

* **Field space:** traceless h-hat (9 components), photon a (4). The EH kinetic form is AS1's with lambda = 0 (no sqrt(g)^(2) term) and Z_N = −F1. On the flat background the EH first variation vanishes, so the EH Hessian is the same in every parametrisation.
* **TDiff gauge (axis C):** the gauge fixing acts only on the transverse part of q.h-hat, i.e. on h-hat_{4i} (i = 1..3), the xi^T modes. With alpha_T -> 0 the graviton field space is TT (5) + sigma (1) exactly (the limit is checked, K7d). sigma = diag(1, 1, 1, −3) for q-hat = e_4.
* **Maxwell vertices (axis D):** P-lin: the constrained linear parametrisation g = (delta + h-hat) det(delta + h-hat)^(−1/4) (det g = 1). By Weyl invariance of sqrt g g g F F in d = 4, its vertices equal AS1's linear-parametrisation vertices restricted to traceless h-hat (checked, K2). P-exp: g = exp(h-hat), sqrt g = 1, g^-1 = 1 − h-hat + h-hat^2/2.
* **The f_g expression.**
  * **TT part, from the repository.** AS3's committed CPR-gauge formula f_g = −5 (8 f + 4 f' − d_t f')/(1152 pi^2 (f + f')^2) comes from the TT modes only (AS3 report). On the flat unimodular background there is no sqrt(g)^(2) term, which is f -> 0 in that formula, and the TT kinetic term and vertices coincide with the standard ones at lambda = 0. So **f_g^TT = 5 (4 − e) g/(72 pi), = 5 g/(36 pi) at the fixed point** (e = 2). This is the door's "TT-only structure" and the K-test limit (K1).
  * **sigma part, derived here** by the same code restricted to the sigma mode: f_g^sigma = c_sigma g. Its closed form is not known before running; the hand expectation is c_sigma = −(2/5)(5/(36 pi)) (section 10.2).
  * **Graded f_g = f_g^TT + f_g^sigma** (TDiff gauge, alpha_T -> 0, P-lin). Hand expectation: g/(12 pi).
  * Reported: TT-only (sigma dropped; the door's hypothesis), TT + sigma + xi^T at alpha_T = 1 (gauge fixing (Z_N/2) |F^T|^2 scaled by Z_N, eta terms acting on it, AS1's convention), and P-exp.
* Ghosts: the TDiff FP operator and the M-eq scalar do not depend on A, and the abelian/TDiff ghost mixing is triangular, so they give no F-bar dependence (AS1's argument, unchanged).

## 5. Inputs

| Input | Value | Label |
|---|---|---|
| N_S, N_D, N_V | 4, 45/2, 12 | SM content (AS3's), declared |
| b_Y | 41/6 | derived (SM hypercharges) |
| Scheme pieces | Litim type I, CPR regulator procedure, eta terms, type-I matter | declared conventions inherited from AS2/AS3 |
| M_P, M_red | 1.220890e19, 2.435e18 GeV | declared (lane B) |
| M_Z | 91.1876 GeV | measured |
| alpha_2^-1(M_Z) | 127.930 x 0.23122 = 29.580 | measured input of the downstream (contamination below) |
| Delta_0 | 137.035999177 − 127.930 = 9.106 | measured input of the downstream (contamination below) |

* **No measured alpha enters g_Y*** (field counts, heat-kernel numbers, the cutoff).
* **Contamination (rules §1.4):** (1) lane B builds alpha_2^-1(M_Z) as alpha^-1(M_Z) sin^2 theta_W; (2) Delta_0 is measured running extracted with measured alpha; (3) the UV target 55.234 is built from data (target only); (4) M_P, M_Z, counts, heat kernels: no alpha. The substitution test scales (1) and (2) as if alpha were 1% larger and reports the shift of P against the 1.37 an identity would show. The gravitational piece 41/(24 pi f_g) cannot move.

## 6. Option space and the graded trial

| Axis | Options | Count |
|---|---|---|
| A. Measure | **M-eq (graded)**; M-naive | 2 |
| B. sigma regulator on S^4 | **CPR un-normalised (graded)**; normalised | 2 |
| C. Graviton modes in f_g / TDiff gauge | **TT + sigma, alpha_T -> 0 (graded)**; TT only (door's hypothesis); TT + sigma + xi^T, alpha_T = 1 | 3 |
| D. Maxwell-vertex parametrisation | **P-lin (graded)**; P-exp | 2 |
| E. Matching / running | **M_P one-loop (graded)**; M_P two-loop; M_red one-loop | 3 |

**K = 72.** Exactly **one graded trial: G1 = (M-eq, CPR, TT + sigma at alpha_T -> 0, P-lin, M_P one-loop).** The other 71 are reported, not graded. **N_mech: 373 -> 374.**

Why these graded choices: M-eq is the measure that keeps the recalled one-loop on-shell equivalence with GR and reduces at eta = 0 to the door's "TT plus transverse vector" content; CPR keeps AS2/AS3's convention (continuity with the K-tests); TT + sigma is the complete graviton content in the only gauge family TDiff allows (sigma is not gauge); P-lin is AS3's parametrisation; M_P one-loop is AS3's and CFG901's graded matching.

## 7. Leverage and precision pre-flight (rules §1.6), frozen now

* **sigma_route = 6.230**, frozen, inherited unchanged from CFG901 (the record's own AS spread, quadrature): two-loop 0.49735; matching at M_red 1.75338; Y1 running 0.1206; scheme |92.914 − 95.57847| = 2.66447; truncation |91.04527 − 96.37265| = 5.32738. Admissible-only variant 3.245 (reported). The script recomputes it from these numbers and must get 6.230 (check PF).
* **delta_route = 0.0455 < 1**: diagnostic in the rules' sense. 1% would need sigma <= 1.37, not reachable, so the ceiling is CONSISTENT.
* **Leverage:** dP/d ln f_g = −41/(24 pi f_g); dP/d ln g* is the same at fixed f_g/g. 137.036 needs f_g = 0.009805 (lane B's f_needed), i.e. g* = 0.009805/c for f_g = c g.
* UG-specific spread (measure, sigma convention, gauge, parametrisation) is not added to sigma_route; it is reported variant by variant and enters the door-level statement (section 8, rule D).

## 8. Gates, grades and kill criteria (frozen)

**Gates (all must pass, else G1 is NOT COMPLETED):**
* **K0, AS3 reproduced** with AS2's imported code: CPR-EH SM root (g, lambda) = (0.967159, −1.22293), f_g = 0.03883093, P = 95.57847; systematics two-loop 96.07582, M_red 93.82509; downstream G0 as CFG901's K4 (downstream_P(b3.fg) = b3.c5 to 1e-9; P(0.04795) = 92.914 and P(0.009805) = 137.036 to 1e-4 relative; P(b3.f_needed) = b3.c6 to 1e-9). Tolerance: half a unit of the last printed digit.
* **K1, the K-test (TT coincidence limit).** The lane's flat f_g code restricted to the 5 TT modes, with the cosmological sqrt(g)^(2) term restored (standard linear parametrisation, lambda -> −F0/(2 F1)), reproduces AS3's general formula −5 (8 F0 + 4 F1 − dF1)/(1152 pi^2 (F0 + F1)^2) identically (sympy), and at K0's root gives AS3's committed f_g = 0.03883093 and P = 95.57847. Without the term (unimodular), the TT-only result equals the same formula at F0 = 0, i.e. 5 (4 − e) g/(72 pi).
* **K2, vertices.** (a) The lane's re-implementation of AS1's vertex builder reproduces AS1's V1 and V2 exactly (all 10 components). (b) Weyl invariance: the P-lin unimodular vertices (g = (delta + h-hat) det^(−1/4), sqrt g = 1) equal AS1's vertices on traceless h-hat, to second order.
* **K3, flat unimodular kinetic form.** (a) With no gauge fixing it annihilates the TDiff pure-gauge modes h-hat = q-hat v + v q-hat (v ⊥ q-hat). (b) It does not annihilate sigma: per unit Frobenius norm, sigma = −Z_N s/8 and TT = +Z_N s/4 (hand values).
* **K4, S^4 blocks.** With F0 -> F1 R/2, F2 -> 0, CPR's gauge term removed: (a) the action part of AS2's xi block vanishes identically (on-shell gauge invariance); (b) TT = −(F1/2)(D + R/6), and D + R/6 = Delta_L − R/2 with Delta_L − D = 2R/3 on traceless symmetric tensors computed from the S^4 Riemann tensor (massless spin-2: (Delta_L − 2 Lambda) h = 0, Lambda = R/4; recalled textbook form); (c) the sigma block equals D^2 times the on-shell trace-mode block (3/16) F1 (D − R/3) (the pure-gauge equivalence h-hat_sigma = L_w g + g D sigma/4).
* **K5, one-loop on-shell equivalence (eta = 0, R^0, R^1, R^2 of the bulk trace, no excluded modes).** (a) GR on-shell from AS2's complete `gravity_W` (CPR gauge, beta -> infinity, ghosts, third ghosts, Jacobians) with F0 -> F1 R/2, F2 -> 0 equals the physical form (1/2) Tr_TT[2/(P + R/6)] − (1/2) Tr_VT[2/(P − R/4)], per field type; (b) unimodular M-eq equals the same; (c) M-naive minus the physical form equals exactly (1/2) Tr_S[2/P]. Reported (informational): 24 x the R^2 coefficient of the physical form (expected 59/45); recalled Christensen-Duff total −571/45 = 59/45 − 14, the integer being excluded modes (recalled, not gating).
* **K6, hand closed forms of the R^1 coefficients** (section 10.1), as functions of e: TT −5/4 − 5e/18; sigma + J_S (CPR) 1/6 + 17e/240; sigma normalised 1/6 + e/24; VT sector (xi + ghost + J_V) −5/8; M-eq scalar −1/6; matter (N_S − N_D − N_V)/6 = −61/12 for the SM.
* **K7, flat consistency:** (a) parity (self-dual = anti-self-dual weight) in every f_g computation; (b) photon-gauge (xi) independence; (c) additivity f(TT + sigma) = f(TT) + f(sigma) at alpha_T -> 0; (d) the alpha_T -> 0 limit of the 9-mode computation with the gauge parameter equals the restricted TT + sigma computation.
* **CC, classifier controls:** P = 137.035999177 -> CONSISTENT; P = 95.57847 -> KILLED; 137.036 ± 3.01 sigma_route -> KILLED; ± 2.99 sigma_route -> CONSISTENT; g* <= 0 -> NOT DIAGNOSTIC; f_g <= 0 -> NOT DIAGNOSTIC; a failed gate -> NOT COMPLETED.
* **PC, positive controls:** (i) f_g = lane B's f_needed gives P = 137.036 (lane B's c6), CONSISTENT, z = 0; (ii) planted gravity: a planted X1 with g* = f_needed/c_graded passes through the same pipeline to P = 137.036, CONSISTENT.

**Grade of G1:**
1. g* admissible (section 4.2), else **NOT DIAGNOSTIC**.
2. f_g* > 0, else **NOT DIAGNOSTIC** (no IR-attractive interacting g_Y*; alpha would stay free).
3. z = (P − 137.035999177)/sigma_route. **|z| > 3: KILLED.** |z| <= 3: **CONSISTENT**, reported with P_single (log-uniform 1/alpha on [10, 1000], window ±|P − 137.036|) and P_family over N_mech = 374.
4. EVIDENCE and DERIVATION are impossible here: a single coupling at Y1 running precision cannot pass the campaign-wide test (K9), there is no second prediction (theta_Y = −2 f_g is not measurable), and no blind re-derivation is planned.

**Rule D (door-level statement, reporting only, never changes G1).** All 71 reported variants are graded by the same rule. If G1 is KILLED and every variant is KILLED, the README says "KILLED across the declared option space". If G1 is KILLED but some variant has |z| <= 3, the README says "KILLED (graded); the option space is not uniform" and names the variants. If G1 is CONSISTENT and some variant is KILLED, the README says "CONSISTENT (graded), option-space dependent".

**Also reported:** g* and its critical exponent, f_g/f_g^TT, theta_Y, g_Y*, the g* that 137 would need for each f_g/g, the two systematics, the admissible-only z, the UV cross-check, the substitution test.

## 9. MUTATE and positive controls (rules §1.9)

Two load-bearing elements, two controls; each must exit 1.
* **MUTATE_SIGN:** every matter trace multiplied by −1, in the AS3 reproduction (K0) and in the unimodular flow. K0's root check and K6's matter coefficient must FAIL. The prediction must move as expected: X1 -> X1_grav − X1_matter, so g* -> −2 pi/(X1_grav + 61/12); with the hand numbers this is negative (g* ≈ −2.25), so G1 becomes NOT DIAGNOSTIC (no admissible fixed point). Check L-SIGN: the mutated g* equals −2 pi/(X1_grav,normal − X1_matter,normal) computed from the normal-mode pieces, to 1e-12 relative.
* **MUTATE_SPLIT (the TT/sigma split):** the sign of the sigma kinetic block flipped in the flat f_g computation (sigma treated as a positive-norm mode). K3(b) must FAIL. Check L-SPLIT: the mutated graded f_g equals f_g^TT − f_g^sigma of the normal run exactly (sympy), and P moves accordingly (hand: f_g -> (7/5) f_g^TT, P ≈ 91.9). The S^4 flow is untouched.
* Positive controls: section 8 PC (i) and (ii).

## 10. Hand derivations and the expected outcome (written before computing)

### 10.1 The flow (pencil, from AS2's heat-kernel table: TT (5, −5/6), VT (3, 1/4), S (1, 1/6); Q_1, Q_2 of the Litim profile)

* TT, weight 1/2, W = (2 + e(1 − z))/(1 + R/6): R^1 = −5/4 − 5e/18.
* sigma (CPR) + J_S: W_net = 1 + (e/2)[1 − z^2 (z − R/3)/(1 − R/3)]: R^1 = 1/6 + 17e/240. Normalised sigma: 1/6 + e/24.
* VT: xi (1/2)·4/(P − R/4), ghost −2/(P − R/4), J_V −1/(P − R/4): net −1/(P − R/4), R^1 = −5/8.
* M-eq scalar −(1/2)·2/P: R^1 = −1/6. Matter (SM): −61/12.
* At e = 2: **X1(M-eq, CPR) = −1327/180 = −7.3722, g* = 360 pi/1327 ≈ 0.8523**; M-naive −1297/180, g* ≈ 0.8720; normalised sigma: M-eq −2675/360 (g* ≈ 0.8456), M-naive −2615/360 (g* ≈ 0.8650). Matter dominates (−5.08 of −7.37); the gravity part is −2.29 (M-eq). Unique fixed point, eta_N = −2.
* At eta = 0 on-shell: M-eq's scalar sector cancels exactly and VT gives det_VT(D − R/4)^(1/2), the physical GR form; M-naive leaves det_S(D)^(−1/2) (gauge-invariant counting: the GR scalar sector cancels because the longitudinal diffeomorphisms remove one scalar, which TDiff does not).

### 10.2 f_g (pencil, mode sums at q-hat = e_4, P-lin)

* TT kinetic +Z_N s/4, sigma −Z_N s/8, xi^T at alpha_T = 1 +Z_N s/4 (per unit norm). Each mode contributes c_m^2/K_m to the loop and Q_m/K_m to the tadpole.
* Loop (photon-polarisation sums, F-bar electric part E along q-hat, magnetic part B): TT (20/3) E^2, sigma (4/3) E^2, xi^T 2 B^2. Tadpole sums: TT (5/4) B^2 + (5/6) E^2, sigma (2/3) E^2, xi^T (1/4) B^2 + (3/2) E^2. After the angular average (<B^2> = 2 <E^2>) both loop and tadpole give sigma/TT = −2/5 and xi^T(alpha_T = 1)/TT = +3/5, so the eta weighting cannot change the ratios.
* Hence **f_g(G1) = (3/5) f_g^TT = g/(12 pi)**; TT only 5 g/(36 pi); alpha_T = 1: (6/5) f_g^TT = g/(6 pi).
* **P-exp = P-lin exactly:** the parametrisation changes only the tadpole, by a term linear in T^mn(F-bar) contracted with mode sums of the form a delta + b q-hat q-hat; T is traceless and its angular average along q-hat vanishes.

### 10.3 Expected numbers (pencil; P = 0.54378/f_g + 81.5747; sigma_route 6.2303)

| Variant (M_P one-loop) | f_g | P | z |
|---|---|---|---|
| **G1: M-eq, CPR, TT + sigma, P-lin** | 30/1327 ≈ 0.02261 | ≈ 105.63 | ≈ −5.04 (KILLED) |
| TT only (door's hypothesis), M-eq | 50/1327 ≈ 0.03768 | ≈ 96.01 | ≈ −6.59 |
| alpha_T = 1, M-eq | 60/1327 ≈ 0.04521 | ≈ 93.60 | ≈ −6.97 |
| G1 with M-naive | 30/1297 ≈ 0.02313 | ≈ 105.09 | ≈ −5.13 |
| G1 with normalised sigma | 60/2675 ≈ 0.02243 | ≈ 105.82 | ≈ −5.01 |

* Expected: **G1 KILLED at |z| ≈ 5**, and KILLED across the declared option space (all |z| between about 4.8 and 7.3, including the two-loop (+0.5) and M_red (−1.75) shifts). The door's "137 needs g* ≈ 0.222 if TT-only carries over": the TT part does carry over (exact, K1), but sigma is physical in unimodular gravity, so 137 would need g* ≈ 0.370 with f_g = g/(12 pi); the flow gives ≈ 0.85. CONSISTENT would need sigma to cancel at least 61% of TT, or g* <= 0.555 at the hand ratio.
* A wrong expectation will be disclosed, not hidden.

## 11. Disclosures made before freezing

* No script of this lane was written or run before this commit. Everything in section 10 is pencil arithmetic on the record's printed numbers and AS2's heat-kernel table.
* The door's named gate (a published unimodular fixed point) cannot be run: the papers are not in the repository and downloads are not used. The unimodular gravity sector therefore has no external numerical anchor; K4 (Lichnerowicz/on-shell structure) and K5 (on-shell equivalence with GR computed by AS2's independent CPR blocks) are structural anchors only. The measure choice M-eq rests on a recalled literature statement (one-loop on-shell equivalence); M-naive is reported beside it.
* Recalled, not read: Eichhorn 1301.0879, 1501.05848; de Leon Ardon-Ohta-Percacci 2018; Kugo-Nakayama-Ohta 2022; Christensen-Duff's −571/45. None is used as a gate number.
* Stop rule (rules §6): this is the first result on D04. A second consecutive KILLED or NOT DIAGNOSTIC on D04 would close the door unless a new forced element appears.
* Compute: one core, `nice -n 10`, OMP_NUM_THREADS=1, a watchdog aborting above 900 MB RSS, expected well under 10 minutes. AS1-AS4 and lane B are imported read-only with bytecode writing disabled; none of their files is edited. A 1024^3 run is live, so nothing heavier runs.
* Never say "theory closed". kappa = 1/2 stays FITTED; alpha stays an INPUT.

## 12. Files (planned)

`CFG906_PREREGISTRATION.md` (this file, committed alone first), `cfg906_d04.py` (gates, flow, f_g, graded trial, reported variants, MUTATE modes), `cfg906_d04.out` / `.json` (real run), `cfg906_d04_MUTATE_SIGN.out` / `.json`, `cfg906_d04_MUTATE_SPLIT.out` / `.json`, `README.md`.
