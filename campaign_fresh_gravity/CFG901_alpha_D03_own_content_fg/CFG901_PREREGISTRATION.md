# CFG901: alpha door D03, f_g evaluated with the record's own matter content (FROZEN pre-registration)

Written 2026-10-20, before any script of this lane was written or run. No number for the record's own matter content (SM + 3 nu_R) has been computed by any script when this file is committed. What I did run before freezing is disclosed in section 11 (timing of the existing AS3/AS4 code on the Standard-Model content only, reproducing committed numbers).

This is **attempt #2 of the post-ledger alpha campaign** (rules: `campaign_fresh_gravity/CFG895_alpha_campaign_ledger/ALPHA_CAMPAIGN_RULES.md`; door: `ALPHA_DOORS.md`, section D03; attempt #1 was CFG896, door D02). Nothing here is expected to derive alpha. KILLED, NOT DIAGNOSTIC and CONSISTENT-at-best are normal outcomes. The door's own ceiling is CONSISTENT (single coupling; rules §4.3, corollary K9).

**Wall note.** The Standard-Model mass sector is WALLED. This lane derives no mass and uses none: the gravitational fixed point depends only on field counts. kappa and the record's Z play no part. Alpha stays an INPUT of the record.

**Record rule restated (rules §0.3).** Asymptotic safety gave 1/alpha(0) = 91–96 (89–97 with systematics) in AS1–AS4, not 137; 137 needs f_g about 4x smaller than every computed value. This lane reuses AS4's frozen admissibility rule for the BMS scheme, and that rule **also rejects the published BMS pure-gravity fixed point** (BMS arXiv:0902.4630; disclosed in AS4). It is restated here as the rules require.

## 1. Mechanism

In asymptotically safe gravity the graviton fluctuations add −f_g g_Y to the hypercharge beta function, beta_gY = −f_g g_Y + (b_Y/(16 pi^2)) g_Y^3 with b_Y = 41/6. If f_g > 0 the interacting zero g_Y* = 4 pi sqrt(6 f_g/41) is IR-attractive, and on the predictive trajectory the hypercharge coupling at the Planck scale equals g_Y*. f_g is computed by the gravity sector; in the background-field approximation of AS3/AS4 it is a function of the dimensionless gravitational couplings at the Reuter fixed point only. That fixed point depends on the matter content through the matter traces in the flow of (g, lambda). Door D03 asks: what does the route give with the record's OWN content instead of the bare SM? The record fixes content beyond the SM in exactly one place that a field count can use (section 4): three right-handed neutrinos from the conditional FS11 door (Dirac neutrinos).

## 2. Forced-kernel candidate and class (rules §2)

* **C(alpha) = 0** is beta_gY(g_Y; f_g) = 0 at the interacting zero, with f_g = f_g(g*, lambda*) evaluated at the unique admissible gravitational fixed point of the flow with the declared content. **Class K1** (UV completeness and IR attractivity), conditional on the asymptotic-safety scenario, exactly as in AS1–AS4 and door D01/D03.
* **Why the solution set is discrete.** beta_gY = 0 has the roots g_Y = 0 and g_Y = ±g_Y*; the IR-attractive interacting root is the predictive one. The gravitational fixed point is a root of two polynomial-rational equations (EH) or four (BMS higher-derivative); uniqueness among admissible roots is required, otherwise NOT DIAGNOSTIC (section 8).
* The content enters as integers fixed by the record before computing. Content is not a free knob here: under X1's zero-knob rule, free content would be a knob, so no content other than the record's is graded (section 4, set B and the bracket).

## 3. Which alpha, which scale, which scheme

* **Prediction:** alpha(0), the Thomson limit. Target 1/alpha(0) = 137.035999177 (CODATA 2022), used only as the target.
* **UV quantity:** g_Y* imposed at M_P = 1.220890e19 GeV (lane B `rg_common.MPL`), i.e. 1/alpha_Y*(M_P) = 41/(24 pi f_g).
* **Downstream (graded map):** lane B C5's one-loop chain, by import, unchanged, exactly as AS3 and AS4 used it (so that the K-tests can reproduce their committed values exactly):
  P = alpha_Y^-1(M_Z)[from g_Y*, b_Y = 41/6] + alpha_2^-1(M_Z) [measured] + Delta_0 [measured 0 -> M_Z offset, 9.106].
  In closed form P = 41/(24 pi f_g) + (41/(12 pi)) ln(M_P/M_Z) + alpha_2^-1(M_Z) + 9.106. The slope is dP/d ln f_g = −41/(24 pi f_g) (−55.2 at the required f_g, about −14 at the computed f_g).
* **Content and the downstream.** nu_R has hypercharge 0, so b_Y = 41/6 and the SM running of g_Y and g_2 below M_P are unchanged; Dirac neutrino Yukawas are below 1e-12 and are neglected. So the content changes P only through f_g.
* **Cross-check, contamination-free (reported, must agree in verdict):** 1/alpha_Y*(M_P) = 41/(24 pi f_g), which uses no measured alpha at all, compared with Y1-central's 1/alpha_Y(M_P) = 55.234 (built from measured data, used only as a target). In the one-loop chain the two comparisons differ by a constant, so their misses agree to the downstream's precision; any disagreement in verdict is disclosed.
* **Error carried for the running (rules §1.3):** Y1's sigma(1/alpha_em)/137.036 = 8.8e-4, i.e. 0.1206, included in sigma_route (section 7).

## 4. The matter content and how it enters f_g (sources in the repository)

**Graded content set A = SM + 3 nu_R:** N_S = 4 real scalars (Higgs doublet), N_D = 45/2 + 3/2 = **24** Dirac-equivalents (45 SM Weyl fermions + 3 right-handed Weyl neutrinos; a Weyl fermion's trace is half a Dirac fermion's), N_V = 12 gauge vectors.

* **Source of the 3 nu_R:** project_atomos FS11 (2026-10-08), the conditional door "SM on a circle + the non-SUSY AdS swampland conjecture": Majorana neutrinos are forbidden, Dirac neutrinos are allowed with m_lightest < 7.35 meV (later refined to 7.66 meV, FS18). Dirac neutrinos need three nu_R. FS11 rests on an unproven conjecture (stated in `fable_independent_2026/lean_2026/LEPTON_CHAIN_CRITERIA.md`). FS11's scripts are not tracked in this repository; the door statement is cited from `ALPHA_DOORS.md` D03 and the LEPTON_CHAIN criteria files. Conditional content, conditional result.
* **Reference set (SM, AS3/AS4's content):** N_S = 4, N_D = 45/2, N_V = 12. Used for the K-tests and the shift Delta P = P_A − P_SM.

**Content set B = A + the canonical theory's elementary dark fields: NOT DEFINED by the record, so NOT a trial.** I read the canonical statement before freezing: `THEORY_CANONICAL_2026-10-14.md` S2 writes a non-relativistic action L = −|∇Phi − K P|²/(2K) − rho_b Phi − W_rem(u) − (gamma/2)|∇P|², where Phi is the Newtonian potential (part of the metric, not new matter) and P is the displacement (polarization) of the cold-energy medium; S3 calls cold energy "a collisionless rest-mass medium"; §3 lists "predict lensing from a relativistic completion" as not done; v2 (2026-10-16) and v3 (2026-10-18) leave S2's field content unchanged (v2 adds only that its rest state is the law exactly). The record also has a standing rule of no dark-matter particle. So the canonical theory posits no elementary relativistic field with a spin and a kinetic term that a heat-kernel count can take. Set B is therefore not graded and adds nothing to N_mech. **Bracket (reported, not graded, a sensitivity only):** if a future version promoted the dark sector to elementary fields, the natural readings are B1 = A + 1 real scalar, B2 = A + 2 real scalars (a complex order parameter, cf. FL1), B3 = A + 1 gauge vector, B4 = A + 1 vector + 1 scalar (a Proca field in Stückelberg form). Context: atomos FS12 (conditional) allows at most 2 extra light bosonic degrees of freedom.

**How content enters (formulas used; all in the repository; type-I matter, Litim cutoff, the AS1/AS2 rule):**
* Matter contributions to (16 pi^2/V) d_t Gamma_k (AS2 pre-registration, "Exception (a)"; code `real_research/alpha_principle_2026/AS2_fg_cpr_scheme/as2_common.py::X_matter` and `AS4_fg_weyl2/as4_common.py::matter_type_I`): scalars (1/2) Tr_S[d_t R_k/P_k]; Dirac −(1/2) Tr_spinor[d_t R_k/(P_k + R/4)]; vectors in Feynman gauge (1/2) Tr_V[d_t R_k/(P_k + R/4)] − Tr_S[d_t R_k/P_k] (ghost).
* With the Litim Q-functionals (Q_2[1] = 1/2, Q_1[1] = 1) and the S^4 / Einstein-space heat-kernel coefficients, the EH-relevant (R^0, R^1) coefficients are, per field: scalar (1/2, 1/6), Dirac (−2, −1/6), vector with ghosts (1, −1/6). So in the EH truncation X_matter = N_S (1/2 + R/6) + N_D (−2 − R/6) + N_V (1 − R/6), identical in the CPR and BMS schemes; the R^2 and Riem^2 parts differ by scheme and enter only the R^2 / C^2 truncations. For SM: −31 − 61 R/12 (AS3 prints −31 − 61R/12 − 1751R²/4320; AS4 prints {1: −31, R: −61/12, R²: −27/80, W: −293/720}). Set A shifts N_D by +3/2: X_matter(A) = −34 − 16R/3 at EH order. Check K6 re-derives these by hand.
* f_g (matter-independent formula; content enters only through the fixed point):
  * CPR gauge (AS3 report): f_g = −5 (8 f + 4 f' − d_t f') / (1152 pi² (f + f')²); at a fixed point (d_t f' = 2 g~1, R^2 coupling drops out) f_g = 5 g (1 − 8 lambda) / (36 pi (1 − 2 lambda)²).
  * BMS gauge (AS4 report): f_g = −(40 u0 + 20 u1 − 5 d_t u1 + 14 d_t u3) / (1152 pi² (u0 + u1 − 2 u3)²), with d_t u1 = 2 u1, d_t u3 = 0 at a fixed point; at u3 = 0 it equals the CPR formula (check K5).
  * EV (lane B `b3_forced_vs_required.py`, Eichhorn–Versteegen as typed there): f_g = G (1 − 4 L)/(4 pi (1 − 2 L)²), with matter entering the EV betas as (2 N_D + N_S − 4 N_V) and (N_S − 4 N_D + 2 N_V). Reported only, flagged: AS1 showed that these equations cannot be rebuilt from a published scheme.
* Gravity flows: AS3's CPR f(R) machinery (n = 1 EH, n = 2 EH + R^2) and AS4's BMS machinery (EH, EH + C^2 + R^2), imported read-only and unchanged. The fixed-point search uses each lane's frozen grid, domain, merge and admissibility rules (AS2 pre-registration "Trials and fixed-point selection"; AS4 pre-registration).
* No published coefficient outside the repository is needed. Nothing is downloaded.

## 5. Inputs

| Input | Value | Label |
|---|---|---|
| N_S, N_D, N_V (set A) | 4, 24, 12 | declared from the record (SM + FS11's 3 nu_R) |
| b_Y | 41/6 | derived (SM hypercharges; nu_R has Y = 0) |
| Scheme, gauge, cutoff, matter rule | CPR f(R) type Ib (AS2/AS3); BMS (AS4); type-I matter; Litim | declared conventions inherited from AS2–AS4 |
| M_P, M_red | 1.220890e19, 2.435e18 GeV | declared (lane B) |
| M_Z | 91.1876 GeV | measured |
| alpha_2^-1(M_Z) | lane B: 127.930 x 0.23122 = 29.580 | measured input of the downstream (see contamination) |
| Delta_0 | lane B: 137.035999177 − 127.930 = 9.106 | measured input of the downstream (see contamination) |

* **No measured alpha enters the prediction of g_Y*** (counts, heat-kernel numbers and the cutoff only). 
* **Contamination list (rules §1.4), quantified in the script by the substitution test:**
  1. lane B builds alpha_2^-1(M_Z) as alpha^-1(M_Z) x sin²theta_W(MS-bar). Numerically this is the SU(2) coupling, which can also be had from the allowed inputs (G_F, M_W) up to scheme (tree level: 1/alpha_2 = pi/(sqrt2 G_F M_W²) = 29.49); the construction still passes through a measured alpha.
  2. Delta_0 = alpha^-1(0) − alpha^-1(M_Z) is the measured running (leptons + Delta alpha_had); at one loop the running in inverse-coupling units is alpha-independent, but the number is extracted with measured alpha.
  3. Y1-central's 1/alpha_Y(M_P) = 55.234 (the UV cross-check target) is built from measured data; target only.
  4. M_P, M_Z, heat-kernel coefficients, counts: no alpha.
  The substitution test scales items 1 and 2 as if alpha were 1% larger and reports the shift of P as a fraction of the 1.37 that an identity would show. The gravitational piece 41/(24 pi f_g) cannot move. Residual and shape tests do not apply (no closed form, no series).

## 6. Option space and the graded trial

| Axis | Options | Count |
|---|---|---|
| Content | A (graded); B undefined (not a trial) | 1 |
| Scheme/truncation | **CPR-EH (graded)**; CPR-R^2; BMS-EH; BMS-EH+C^2+R^2; EV-EH | 5 |
| Matching / running | **M_P one-loop (graded)**; M_P two-loop; M_red one-loop | 3 |

**K = 15.** Exactly **one graded trial: G1 = content A, CPR scheme, EH truncation, g_Y* imposed at M_P, lane B one-loop downstream** (the door's reference point: AS3's EH root (0.967159, −1.22293) is the point from which CFG895 computed "137 needs lambda* = 0.107 or −7.83"). The other 14 are reported, not graded. **N_mech: 372 -> 373.**

Values the route would give for each choice are all printed (the two systematics for every scheme root with a value).

## 7. Leverage and precision pre-flight (rules §1.6), written now

* **Route error, frozen from the record's committed numbers (SM content), quadrature of:**
  * two-loop running: 0.49735 (AS3 EH; AS4 EH 0.49231);
  * matching at M_red instead of M_P: 1.75338 (AS3 and AS4);
  * Y1 running: 8.8e-4 x 137.036 = 0.1206;
  * scheme: |P_EH(EV) − P_EH(CPR)| = |92.914 − 95.57847| = 2.66447 (largest of the three schemes; BMS differs by 0.79418);
  * truncation: |P(BMS HD in-domain root) − P_EH(BMS)| = |91.04527 − 96.37265| = 5.32738 (largest record truncation shift; that root is inadmissible under AS4's rule, so this is conservative; the admissible-only largest shift is AS3's 0.30886).
  * **sigma_route = 6.230** (6.2303). Admissible-only variant, reported for information: 3.245.
* **delta_route = 6.230/137.036 = 0.0455 < 1**, so the route is diagnostic in the rules' sense (§1.6 threshold). It cannot reach 1% (sigma_route > 1.37), so its best grade is CONSISTENT.
* **Content leverage (diagnostic map, not graded; the door's first computation):** at SM content, d(g*, lambda*, f_g, P)/d(N_S, N_D, N_V) in CPR-EH, BMS-EH and EV-EH, by the implicit-function theorem on the content-symbolic flow and cross-checked by finite differences (N_S ±1, N_D ±1/2, N_V ±1). The script prints the map's linear prediction of P_A − P_SM before the graded solve. If |P_A − P_SM| < sigma_route in every scheme with a value, the content loophole is closed at the computed truncations.
* **Tuned content (by construction, like lane B's C6; not a prediction, a knob):** the N_D (and separately N_S, N_V) at which P(CPR-EH) would reach 137.036 along the continuation of the admissible root, if such a value exists below 1000.

## 8. Gates, grades and kill criteria (frozen)

**Gates (all must pass, else NOT COMPLETED):**
* **K1, AS3 reproduced with its own content (SM).** CPR-EH root (g, lambda) = (0.967159, −1.22293), f_g = 0.03883093, P = 95.57847; CPR-R^2: 4 real roots, 2 admissible, (1.006220, −1.264456, −0.0037661) with f_g 0.03970669, P 95.26961 and (0.988607, −1.297727, 0.0055494) with f_g 0.03848093, P 95.70584; EH systematics two-loop 96.07582, M_red 93.82509. Tolerance: half a unit of the last printed digit.
* **K2, AS4 reproduced with its own content (SM).** BMS-EH root (0.864773, −1.09006), f_g 0.03674694, P 96.37265; BMS-HD: 3 real roots, 0 admissible; in-domain root (0.863182, −1.07628, 0.0210528, −0.0072056) with f_g 0.05741784, P 91.04527; root 3 P 83.50578; EH systematics two-loop 96.86496, M_red 94.61927. Same tolerance.
* **K3, lane B's EV value reproduced.** With N_D = 22.5, lane B's module values fg and c5 to 1e-12, and the printed 92.914 to 5e-4.
* **K4, downstream (AS3's G0).** downstream_P(b3.fg) = b3.c5 (1e-9); downstream_P(0.04795) = 92.914 (1e-4 relative); downstream_P(0.009805) = 137.036 (1e-4 relative); downstream_P(b3.f_needed) = b3.c6 (1e-9).
* **K5, f_g closed forms.** sympy: AS3's printed general CPR formula with d_t f' = 2 f' equals 5 g (1 − 8 lambda)/(36 pi (1 − 2 lambda)²); AS4's BMS formula at u3 = d_t u3 = 0 equals the CPR one.
* **K6, matter traces.** The code's per-field (R^0, R^1) coefficients in both schemes equal the hand values (1/2, 1/6), (−2, −1/6), (1, −1/6); the SM totals equal AS3's and AS4's printed totals exactly.
* **K7, published anchors of the content dependence.** Content (0,0,0) in CPR-EH: g~0* = 0.005226 and theta = 2.382 ± 2.168 i (CPR Tables 1–2, 0.1% each). Content (0,0,0) in BMS-EH: (0.902, 0.109), theta 2.52 ± 1.78 i; content (1,0,0) in BMS-EH: (0.860, 0.131), theta 2.58 ± 1.95 i (BMS's printed n_s = 1 row), each to half the last printed digit.
* **K8, map consistency.** The implicit-function derivatives agree with the finite differences to 1e-3 relative; the content-A root found by the frozen grid equals the root reached by continuation from the SM root in steps of Delta N_D = 0.25.
* **CC, classifier controls with planted inputs:** P = 137.035999177 -> CONSISTENT; P = 95.57847 -> KILLED; P = 137.036 ± 3.01 sigma_route -> KILLED; ± 2.99 sigma_route -> CONSISTENT; two admissible roots -> NOT DIAGNOSTIC; none -> NOT DIAGNOSTIC; f_g <= 0 -> NOT DIAGNOSTIC; a failed gate -> NOT COMPLETED.
* **Positive control (planted answer):** f_g = lane B's f_needed gives P = 137.036 (lane B's c6) and the classifier returns CONSISTENT with z = 0.

**Grade of G1:**
1. CPR-EH with content A has exactly one admissible root (AS2 rules: g > 0, 1 − 2 lambda > 0, in-domain), else **NOT DIAGNOSTIC** (two or more roots, or none; the CFG895 grade set has no "NOT PREDICTED", so "no admissible root" maps to NOT DIAGNOSTIC with that reason stated).
2. f_g* > 0, else **NOT DIAGNOSTIC** (no IR-attractive interacting g_Y*).
3. z = (P_A − 137.035999177)/sigma_route. **|z| > 3: KILLED.** |z| <= 3: **CONSISTENT**, reported with P_single (log-uniform 1/alpha on [10, 1000], window ±|P_A − 137.036|) and P_family over N_mech = 373.
4. EVIDENCE and DERIVATION are impossible in this lane: a single coupling with Y1-precision running cannot pass the campaign-wide test (K9), there is no second prediction (theta_Y = −2 f_g is not measurable), and no blind second-agent re-derivation is planned.

**Reported verdicts (not graded) use the same rules** for CPR-R^2, BMS-EH, BMS-HD and EV-EH with content A, for the B bracket, and for the systematics.

## 9. MUTATE and positive controls (rules §1.9)

The load-bearing element is the matter content entering the gravitational flow.
* **MUTATE_SIGN:** every matter trace multiplied by −1 (CPR, BMS, EV). K1, K2, K3, K6 and K7's n_s = 1 row must FAIL, and the run must exit 1. The pure-gravity K7 rows must still PASS (the control is targeted). The mutated graded P is printed to show how far it moves.
* **MUTATE_COUNT:** the graded content uses Delta N_D = +3 (the 3 Weyl neutrinos counted as Dirac). The content-definition check C-DEF (Delta N_D = 3/2 for 3 Weyl singlets) must FAIL and the run exit 1. The prediction must move as expected: (P(SM + 3 Dirac) − P_SM)/(P_A − P_SM) = 2 within 10%, and (P(SM − 3 Weyl) − P_SM)/(P_A − P_SM) = −1 within 10%. These two linearity checks (L1, L2) also run, and must pass, in NORMAL mode, where they are diagnostics. MUTATE runs skip the BMS-HD grid (51 s per content) to save CPU while the 1024³ run is live; this is disclosed.

## 10. Expected outcome (written before computing)

* By hand (matter-dominated estimate, g* ~ 1/|X_R|, lambda* ~ −X_0/(4 X_R)): adding 3/2 Dirac makes g* about 5% smaller and lambda* about 4% more negative; f_g drops by about 7%, so **P_A − P_SM ≈ +1** in CPR-EH (expected range 0 to +2, same sign in every scheme). In the EV form, more fermions also lower f_g.
* **P_A(CPR-EH) ≈ 96–97.5; G1 KILLED at |z| ≈ 6–7** (39–41 units below 137.036).
* Content loophole closed: |P_A − P_SM| < sigma_route in every scheme. Bracket B1–B4 shifts each below 2 units.
* Tuned content: tens to about a hundred extra Dirac fermions would be needed to reach 137 in CPR-EH (rough), if the root survives that far.
* A wrong expectation will be disclosed, not hidden.

## 11. Disclosures made before freezing

* **Feasibility timing before freezing** (scratch scripts outside the repository, not committed): I ran the existing AS3 and AS4 code on the **SM content only**: CPR-EH (5 s, 160 MB), CPR-R^2 (19 s, 176 MB), BMS-EH (2 s, 134 MB) and BMS-HD (51 s, 138 MB). They reproduced the committed AS3/AS4 roots. That run also printed the code's symbolic matter traces for general (N_S, N_D, N_V), which matched the hand formula of section 4 that I had written down first. No fixed point, f_g or P for content A (or any other non-SM content) was computed. AS3's own 1120 s / 1.35 GB came from its symbolic f_g derivation; this lane uses the closed forms instead, verified by K1/K2/K5.
* The hand estimate in section 10 was made from the matter traces alone (no gravity part), before any computation for content A.
* Stop rule (rules §6): this is the first result on D03. A second consecutive KILLED or NOT DIAGNOSTIC on D03 would close the door unless a new forced element appears.
* Compute: one core, `nice -n 10`, a watchdog that aborts above 900 MB RSS, expected total about 3 minutes. Lanes AS1–AS4 and lane B are imported read-only, with bytecode writing disabled; none of their files is edited.
* Never say "theory closed". kappa = 1/2 stays FITTED; alpha stays an INPUT.

## 12. Files (planned)

`CFG901_PREREGISTRATION.md` (this file, committed alone first), `cfg901_d03.py` (gates, pre-flight map, graded trial, reported trials, bracket, MUTATE modes), `cfg901_d03.out` / `.json` (real run), `cfg901_d03_MUTATE_SIGN.out`, `cfg901_d03_MUTATE_COUNT.out`, `README.md`.
