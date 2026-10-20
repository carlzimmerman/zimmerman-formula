# CFG910: alpha door D01, f_g from the fluctuation photon–graviton vertex (FROZEN pre-registration, scoped version)

Written 2026-10-20, before any script of this lane was written or run. No number of this lane has been computed by any script when this file is committed. Nothing was run before freezing (not even the existing AS code); the record values quoted below are copied from committed outputs (`AS3_REPORT.md`, `as1_g1_fg_flat.out`, CFG901/CFG906 READMEs).

This is **post-ledger alpha attempt #5** if it outputs a graded value (rules: `campaign_fresh_gravity/CFG895_alpha_campaign_ledger/ALPHA_CAMPAIGN_RULES.md`; door: `ALPHA_DOORS.md`, section D01; #1 CFG896, #2 CFG901, #3 CFG906, #4 CFG907; CFG899 was a structural closure). N_mech before this lane: 375. Nothing here is expected to derive alpha. KILLED, NOT DIAGNOSTIC, NOT COMPLETED and CONSISTENT-at-best are normal outcomes. The door's ceiling is CONSISTENT (single coupling; rules §4.3, corollary K9). The door's own honest expectation: "another 90–110".

**Wall note.** The Standard-Model mass sector is WALLED. No mass enters or is derived: the gravitational fixed point depends only on field counts. kappa and the record's Z play no part. Alpha stays an INPUT of the record. Nothing is downloaded; every literature statement below is labelled "recalled" and is not used as a gate.

**Record rule restated (rules §0.3).** Asymptotic safety gave 1/alpha(0) = 91–96 (89–97 with systematics) in AS1–AS4, not 137; 137 needs f_g about 4x smaller than every computed value. This lane does not reuse AS4's admissibility rule (which also rejects the published BMS pure-gravity fixed point; disclosed in AS4). It reuses AS2/AS3's CPR admissibility (g > 0, 1 − 2 lambda > 0, 1 − 4 lambda/3 > 0 at EH order) only to reproduce AS3's fixed point.

## 0. Scope (why this is a SCOPED D01)

The door asks for f_g from the fluctuation photon–graviton vertex beyond the background-field approximation, at a fluctuation fixed point, and estimates 2–5 agent-days. This lane has one session. It therefore freezes the **simplest closed fluctuation truncation that can be carried through exactly in sympy tonight**, and states precisely what it leaves out (section 12). In one sentence: **the photon sector is treated in the fluctuation approach (its own photon–graviton coupling g_3, read off the zero-graviton-momentum aah vertex, with its own flow and fixed point), while the pure-gravity sector (graviton mass parameter mu_h, graviton anomalous dimension eta_h, graviton three-point coupling g_h3, its cosmological part lambda_3) is held at the record's background-field fixed point mapped into fluctuation variables.** This is a "semi-fluctuation" closure (named F1 below). It is not the full fluctuation fixed point of the door; the README must say so.

## 1. Mechanism

In asymptotically safe gravity the graviton fluctuations add −f_g g_Y to the hypercharge beta function, beta_gY = −f_g g_Y + (41/6) g_Y^3/(16 pi^2). If f_g > 0 the interacting zero g_Y* = 4 pi sqrt(6 f_g/41) is IR-attractive and the hypercharge coupling at the Planck scale is fixed. For an abelian field the charge runs only through the photon wave-function renormalisation (Ward identity): beta_e = (eta_A/2) e with eta_A = −d_t ln Z_A, so **f_g = −eta_A^grav/2**, the gravitational part of the photon anomalous dimension. In AS1–AS4 every graviton–photon vertex carried the background Newton coupling g and the graviton propagator carried the background lambda (the background-field approximation). In the fluctuation approach the aah, aahh, aahhh vertices carry their own couplings (g_3, g_4, g_5), the graviton propagator carries a mass parameter mu_h, and the regulator is built from the background metric only, so it does not see the graviton fluctuation. The photon–graviton coupling g_3 then runs by its own flow, and its fixed-point value replaces g in f_g.

## 2. Forced-kernel candidate and class (rules §2)

* **C(alpha) = 0** is beta_gY(g_Y; f_g) = 0 at the interacting zero, with f_g = f_g(g_3*, g_4*, mu_h, eta_h) evaluated at the unique admissible zero g_3* of beta_g3 (section 5.5) in closure F1. **Class K1** (UV completeness and IR attractivity), conditional on the asymptotic-safety scenario and on closure F1.
* **Discreteness.** beta_gY = 0 has the roots 0 and ±g_Y*; the IR-attractive interacting root is the predictive one. beta_g3 = 0 is (after multiplying by a power of sqrt(g_3)) a polynomial equation of degree ≤ 3 in x = sqrt(g_3) with coefficients fixed by the computation; its admissible roots are finite. Uniqueness among admissible roots is required (section 8).

## 3. Which alpha, which scale

* **Prediction:** alpha(0), Thomson limit. Target 1/alpha(0) = 137.035999177 (CODATA 2022), used only as the target.
* **UV quantity:** g_Y* imposed at M_P = 1.220890e19 GeV (lane B `rg_common.MPL`), 1/alpha_Y*(M_P) = 41/(24 pi f_g).
* **Downstream (graded map):** lane B C5's one-loop chain by import, unchanged, exactly as AS1–AS4, CFG901 and CFG906 used it (`AS1_fg_r2_truncation/as1_common.py::downstream_P`): P = alpha_Y^-1(M_Z)[from g_Y*] + alpha_2^-1(M_Z) [measured] + Delta_0 [measured offset]. Closed form P = 41/(24 pi f_g) + const; dP/d ln f_g = −41/(24 pi f_g).
* **Contamination-free cross-check (reported; must agree in verdict):** 1/alpha_Y*(M_P) = 41/(24 pi f_g) against Y1-central 55.234 (target only), z_UV = (value − 55.234)/sigma_tot.
* **Running error** (rules §1.3): Y1's 8.8e-4 x 137.036 = 0.1206, inside sigma_route.

## 4. Inputs

| Input | Value | Label |
|---|---|---|
| Field content | SM: N_S 4, N_D 45/2, N_V 12 (type-I matter) | declared; enters only through AS3's background fixed point |
| Background fixed point (g*, lambda*) | AS3 CPR-EH + SM: (0.967159, −1.22293) | derived by the record's code (AS2/AS3, imported read-only; reproduced as gate G-REC) |
| eta_N at that point | −2 (exact at any background fixed point, beta_g = (2 + eta_N) g) | derived |
| Scheme, regulator | Litim type I: every q^2 of the (fluctuation-free) kinetic matrix replaced by P_k(q^2); background metric delta in the regulator and gauge fixing | declared convention (AS1/AS2) |
| M_P, M_red, M_Z | 1.220890e19, 2.435e18, 91.1876 GeV | declared / measured (lane B) |
| alpha_2^-1(M_Z), Delta_0 | lane B values | measured inputs of the downstream; they contain measured alpha (substitution test, section 9) |
| Forbidden | alpha at any scale or any proxy as an input to the gravitational part; kappa; Z; fitted reals | none used |

**Contamination list.** (i) The gravitational part (fixed point, g_3*, f_g) uses field counts only: no alpha. (ii) The downstream uses alpha_2^-1(M_Z) = alpha^-1(M_Z) sin^2 theta_W and Delta_0, both containing measured alpha, as in every AS lane; the substitution test (rules §4.2) and the UV cross-check expose this. (iii) No lattice scale, no electromagnetic mass shift, no CODATA-derived constant enters.

## 5. The truncation, the vertex and the flows (all definitions frozen)

### 5.1 Fields, action, gauges

Euclidean flat background, metric g = delta + h_c + h, where h_c is a **constant** symmetric matrix (the zero-momentum graviton, the external leg of the projected vertex) and h is the graviton fluctuation; photon A = A-bar + a with constant background field strength F-bar (the external photon legs at zero momentum, AS1's method). Units k = 1, e = 1 (e cancels in f_g; Z_A = 1 at the evaluation point). Truncation (AS1 normalisation, field h dimensionless):

* graviton two-point: Z_N [ −(sqrt g R)^(2) + 2 lambda_2 (sqrt g)^(2) ] + gauge fixing, Z_N = 1/(16 pi g_h); **mu_h ≡ −2 lambda_2** is the graviton mass parameter (it multiplies the kinetic tensor structure exactly in both de Donder gauges and in the CPR gauge on the TT modes);
* the h_c-dependence of the graviton Hessian (the hhh vertex with one zero-momentum leg): tag sqrt(g_h3/g_h) times Z_N [ −(sqrt g R)^(2) + 2 lambda_3 (sqrt g)^(2) ] differentiated once in h_c, with the kinetic part evaluated at the actual loop momentum q^2 (it is fluctuation-dependent and is not regulated);
* Maxwell (1/4) sqrt g g^{ma} g^{nb} F_mn F_ab expanded in X = h_c + h; each term of order n in graviton legs (h_c and h together) carries the photon-sector tag (g_n'/g_h)^{n/2} with g_n' = g_3 for n = 1 (aah: the F-bar h a vertex V1, the h_c a a photon-block correction W_A, the tree F-bar F-bar h_c), g_4 for n = 2 (aahh: F-bar F-bar h h = V2, F-bar h a h_c = U1), g_5 for n = 3 (aahhh: F-bar F-bar h h h_c = U2);
* photon gauge fixing (1/(2 xi)) (d.a)^2 with the flat background metric; xi symbolic or at two values; every result must be xi-independent (gate G-XI);
* graviton gauge fixing built from the flat background metric (fluctuation approach) and therefore independent of h_c:
  * **CPR** (graded): rho = 0 (chi_nu = d^mu h_mu nu − (1/4) d_nu h), Landau limit (gauge-fixing strength → infinity). Implemented by restricting the graviton to the kernel of chi (5 TT modes + the pure trace mode h_mn = phi delta_mn for q = kappa e_4), which is exact in that limit for every insertion (the gauge-fixing term and its regulator vanish on the kernel; the O(1/strength) parts of the propagator are suppressed). Lambda enters the TT modes as (1 − 2 lambda_2) and the trace mode as (1 − 4 lambda_2/3).
  * **LdD** (reported): beta = 1 (F_mu = d^nu h_nu mu − (1/2) d_mu h), Landau limit, kernel restriction (5 TT + the scalar h = diag(1,1,1,3) for q = kappa e_4).
  * **FdD** (reported; also the gauge of gate G-COV): beta = 1, alpha = 1, full 10-component graviton, (Z_N/2) F_mu F_mu.
* Ghosts give no F-bar dependence (the photon-ghost/diffeomorphism-ghost matrix is triangular and the regulator is ghost-diagonal; AS1's argument, unchanged by a constant h_c), so they are omitted.

### 5.2 Regulator and d_t R_k

Fluctuation approach: R_k is built from the flat background only, R_k = (P_k(q^2) − q^2) x [the h_c = 0 kinetic matrix at unit q-hat], Litim P_k = max(q^2, 1). On its support (q^2 = kappa^2 < 1): Gamma^(2) + R_k = M^0(s = 1) + [h_c-dependent terms with s = kappa^2]. d_t R_k = 2 d_s M^0 − eta_h (1 − kappa^2) d_s M^0_hh (graviton block, including its gauge-fixing part in FdD), and 2 d_s M^0_aa on the photon block with **no eta_A term**: at the hypercharge fixed point the total photon anomalous dimension vanishes exactly (beta_gY = (eta_A/2) g_Y = 0 with g_Y* ≠ 0), and f_g enters the prediction only at that point. This also matches AS1–AS4.

### 5.3 Expansion (exact bookkeeping)

With X = f V1 + f^2 V2 + eps W + f eps U1 + f^2 eps U2 (W = W_h + W_A) and G = (M^0)^-1 (block diagonal):
* two-point, order f^2: (1/2) Tr[(−G V2 G + G V1 G V1 G) d_t R_k];
* vertex, order f^2 eps: (1/2) Tr[(−G U2 G + G V2 G W G + G W G V2 G + G U1 G V1 G + G V1 G U1 G − G V1 G V1 G W G − G V1 G W G V1 G − G W G V1 G V1 G) d_t R_k].
Each term is a polynomial in kappa on the support; radial measure int_0^1 kappa^3 dkappa/(8 pi^2). Diagram classes and the coupling monomial each carries (relative to the tree aah vertex, the propagator coupling g_h cancels identically): two-point [V1V1] g_3, [V2] g_4; vertex [U2] g_5^{3/2} g_3^{-1/2}, [V2 W_h] g_4 sqrt(g_h3/g_3), [U1 V1] g_4, [V1 V1 W_h] sqrt(g_3 g_h3), [V1 V1 W_A] g_3. The lambda_3 part of W_h is kept as a separate symbol.

### 5.4 Angular average and the vertex projection

q = kappa e_4 is fixed and the integrand is averaged over the joint rotation orbit of (F-bar, h_c) (AS1's method extended). The integrand at q-hat = e_4 is fitted exactly to the 7 parity-even invariants linear in h_c and quadratic in F-bar built with a unit vector n: A1 = tr(h) F:F, A2 = h_ab F_ac F_bc, B1 = tr(h)(nFFn), B2 = (nhn) F:F, B3 = (nh FF^T n), B4 = (nF) h (nF)^T, C1 = (nhn)(nFFn); the S^3 average gives c_A A1 + c_B A2 with c_A = c_A1 + (c_B1 + c_B2)/4 + c_C1/24, c_B = c_A2 + (c_B3 + c_B4)/4 + c_C1/12. Two-point: d1 F:F + d2 (nFFn) → c_0 = d1 + d2/4. The fit uses 7 configurations of rational (F-bar, h_c); at least 2 further configurations must give residual exactly 0 (G-FIT) and a reflected configuration (diag(−1,1,1,1) applied to both) must give the identical value (G-PAR, no parity-odd terms).

* **Tree vertex:** the order-h_c term of (1/4) sqrt g g g F-bar F-bar is (1/4)(A1/2 − 2 A2). Its trace part is zero (constant Weyl rescaling; Maxwell is Weyl invariant in d = 4), so the tree vertex is purely the traceless A2 structure. **g_3 is defined by the A2 (traceless) coefficient.** A generated trace part 4 c_A + c_B ≠ 0 is an operator outside the truncation (regulator-induced Weyl breaking); it is reported as a truncation diagnostic, not used.
* **Flows (e = Z_A = 1 at the point):** d_t Z_A = 4 c_0, eta_A^grav = −4 c_0, **f_g = 2 c_0** (AS1's normalisation). d_t(Z_A tau_3) = −2 c_B, so with tau_3 = sqrt(g_3/g_h) and d_t ln g_h = 2 + eta_h:

  **beta_g3 = g_3 [2 + eta_h + 2 Delta], Delta = eta_A^grav + V^grav = −2 f_g − 2 c_B/tau_3,**

  where charged-matter loops are assumed to renormalise Z_A and the aah vertex identically (covariant Ward identity) and therefore cancel in Delta. Their non-covariant remainder is not computed; it is bracketed by the matter probes of section 7.
* **Covariance identity (basis of gate G-COV):** if the regulator and the gauge fixings are built with g_c = delta + h_c instead of delta (the background-field treatment of the constant mode), the flow on (g_c, F-bar) is c_0 sqrt(g_c) g_c g_c F-bar F-bar, so c_A = c_0/2 and c_B = −2 c_0, i.e. Delta ≡ 0 when every coupling is identified. Implemented by q-hat → g_c^{1/2} e_4, all forms (including both gauge fixings) with g_c, d_t R_k from the g_c forms, measure sqrt(g_c). With the delta regulator (the fluctuation approach) Delta ≠ 0, and this regulator-induced remainder is what decides g_3*.

### 5.5 Closure F1 and the fixed point

* **Graded closure F1:** (g_h3, lambda_3, mu_h, eta_h) = (g*, lambda*, −2 lambda*, −2) from G-REC; photon-sector identification **U: g_4 = g_5 = g_3**; g_3* = the admissible zero of beta_g3. With eta_h = −2 and U, Delta = a g_3 + b sqrt(g_3 g*), so the nontrivial zero is **g_3*/g* = r = (b/a)^2**, admissible iff −b/a > 0; then f_g = r x f_g^BF(gauge) exactly.
* **Admissible root:** g_3* real and > 0, f_g(g_3*) > 0, all propagator denominators of section 5.1 positive. If f_g ≤ 0 at the unique admissible g_3*, the route predicts g_Y(M_P) = 0 (no interacting zero): graded KILLED.
* In the covariant mode (G-COV) the same closure gives r = 1 exactly (positive control PC2: the background-field identification g_3 = g is the fixed point when the regulator respects the constant-mode covariance).

## 6. Option space K and the graded trial

| Axis | Values | Count |
|---|---|---|
| graviton gauge | CPR (graded), LdD, FdD | 3 |
| eta_h | −2 (graded), 0 | 2 |
| lambda_3 | lambda_2 (graded; one cosmological coupling in the graviton n-point functions), 0 | 2 |
| photon-sector identification | U: g_4 = g_5 = g_3 (graded); U': g_4 = g_5 = g_h3 (only the aah coupling resolved) | 2 |
| matching / running | one-loop at M_P (graded), two-loop, start at M_red | 3 |

**K = 72; one graded trial G1 = (CPR, eta_h = −2, lambda_3 = lambda_2, U, one-loop at M_P).** The other 71 are reported, not graded. LdD and FdD use the CPR fixed-point inputs (the record has no SM fixed point in those gauges): flagged gauge-inconsistent, reported only, not in sigma_fl. N_mech: 375 → 376 if G1 yields a value.

## 7. Leverage pre-flight and error budget (rules §1.6)

* Leverage: dP/d ln r = dP/d ln f_g = −41/(24 pi f_g): −14.0 at r = 1 (f_g^BF = 0.0388309), −55.2 at the required f_g = 0.009805, i.e. r_needed = 0.2525. 1% in alpha needs f_g to 2.5%: not reachable; ceiling CONSISTENT.
* **sigma_route = 6.230** (frozen, inherited from CFG901: scheme 2.664, truncation 5.327, matching 1.753, two-loop 0.497, Y1 0.121, in quadrature); admissible-only variant 3.245 reported.
* **sigma_fl (fluctuation-closure systematic, recipe frozen here, value computed):** half of (max − min) of the one-loop-at-M_P P over the 10 CPR-gauge closure probes: the 8 combinations of eta_h x lambda_3 x {U, U'} plus the two matter probes Delta → Delta ± eta_A^matter on G1's closure, with eta_A^matter = +2 f_g(g_3) (its exact value at the hypercharge fixed point, where eta_A^grav + eta_A^matter = 0). Probes without an admissible root are excluded from the range and counted.
* **sigma_tot = sqrt(sigma_route^2 + sigma_fl^2); z = (P_G1 − 137.036)/sigma_tot; delta_route = sigma_tot/P_G1.**
* With sigma_fl = 0, CONSISTENT would need P ≥ 118.35, i.e. f_g ≤ 0.01479, r ≤ 0.381.

## 8. Grades for G1 (rules §5 wording)

1. Any required gate fails (section 9) → **NOT COMPLETED** (no graded value). Exception declared in advance: if only G-BF-LdD fails, the LdD variants are dropped (disclosed) and the lane continues.
2. G1 closure has no admissible root, or two or more → **NOT DIAGNOSTIC** (no value; all roots reported).
3. delta_route > 1 → **NOT DIAGNOSTIC**.
4. f_g ≤ 0 at the unique admissible root → **KILLED** (no interacting hypercharge zero).
5. |z| > 3 → **KILLED**; |z| ≤ 3 → **CONSISTENT** ("allowed, not predicted"; never a derivation). EVIDENCE is impossible here (single coupling, no second prediction; theta_Y = −2 f_g is not measurable).
* The door's kill clause ("the gate fails twice") is applied on the record: a second failing execution of a required gate after a disclosed fix is NOT COMPLETED for the door.

## 9. Gates and checks (all required unless stated)

* **PF:** sigma_route and the admissible-only value equal 6.230 and 3.245.
* **G-REC:** AS3 reproduced with AS2/AS3 code (read-only): unique admissible CPR-EH SM root (0.967159, −1.22293), f_g = 0.03883093, P = 95.57847, two-loop 96.07582, M_red 93.82509 (printed digits, half-unit tolerance).
* **G-DS:** lane B downstream G0 checks (as CFG901/CFG906).
* **G-VTX:** this lane's vertex builder reproduces AS1's V1 and V2 exactly at h_c = 0 (all 10 h components), and its EH quadratic form at h_c = 0 equals AS1's bilinear action's graviton block.
* **G-BF (the door's gate, background-field limit g_3 = g_4 = g, mu_h = −2 lambda, eta_h = eta_N, two-point):** exact symbolic identities in (g, lambda, eta_N): CPR: 5 g (eta_N − 16 lambda + 4)/(72 pi (1 − 2 lambda)^2) (AS1's TT formula; equals AS3's 5 g (1 − 8 lambda)/(36 pi (1 − 2 lambda)^2) at eta_N = −2, also checked); LdD: g (eta_N − 16 lambda + 4)/(16 pi (1 − 2 lambda)^2); FdD: g (eta_N − 16 lambda + 4)/(8 pi (1 − 2 lambda)^2) (AS1's printed (0,1) and (1,1) results).
* **G-XI:** two-point symbolic in xi: d/dxi = 0; every vertex class identical at xi = 1 and xi = 2.
* **G-FIT / G-PAR:** section 5.4 (exact).
* **G-EXP:** the perturbative bookkeeping of section 5.3 checked independently: for one configuration at a rational point (lambda_2, lambda_3, eta_h, xi, kappa), the full matrix (M^0 + X) is inverted numerically at 50 digits (mpmath) and d_eps d_f^2 of (1/2) Tr[(M^0 + X)^-1 d_t R_k] is extracted by finite differences; it must equal the expansion's integrand to relative 1e-12 (FdD and CPR).
* **G-COV (FdD):** covariant mode gives c_A = c_0/2 and c_B = −2 c_0 as exact identities in (lambda, eta) at xi = 1 and 2 (declared fallback if sympy cannot finish within the run budget: exact equality at 4 rational (lambda, eta) points; disclosed if used).
* **PC1:** planted f_g = f_needed gives P = 137.035999177 and grades CONSISTENT.
* **PC2:** covariant-mode closure F1 (FdD) has the unique admissible root r = 1.
* **MUTATE_VERTEX** (load-bearing element: the zero-graviton-momentum photon–graviton vertex W_A, sign flipped in both modes): G-COV must FAIL and the run must exit 1, while G-BF (two-point, no W_A) must still PASS; the moved G1 root is reported.
* **MUTATE_GRAV** (the graviton-block h_c dependence W_h set to zero in both modes): G-COV must FAIL, exit 1; G-BF must still PASS; the moved G1 root is reported.
* **Substitution test (rules §4.2):** scale the downstream's measured alpha_2^-1(M_Z) and Delta_0 as if alpha were 1% larger; report the fraction of an identity's shift (expected 0.28, all from the downstream). **UV cross-check:** section 3.

## 10. Expected outcome (hand expectations, written before computing)

* The two-point gates must reproduce the record formulas exactly (they are the same diagrams as AS1's constant-F-bar computation: each aah vertex is O(p), so the photon line's momentum dependence enters only beyond O(p^2)).
* The covariant mode must give Delta ≡ 0 (identity) and r = 1.
* In the fluctuation mode I expect a regulator-induced remainder of tens of percent, so **r between 0.5 and 2**, f_g^G1 between 0.019 and 0.078, **P between about 88 and 105, z ≈ −5 to −8: KILLED**, in line with the door's recalled "effective universality" expectation (vertex and background couplings agree to tens of percent; recalled, not checked). CONSISTENT would need r ≤ 0.38. I have no hand value for the sign of a or b; a NOT DIAGNOSTIC (no admissible root) outcome is possible.
* Weyl-breaking diagnostic 4 c_A + c_B: nonzero, size unknown.

## 11. Compute and hygiene

One core (OMP_NUM_THREADS=1, nice 10), an RSS watchdog at 900 MB, < 20 min per run, sympy exact rational arithmetic for the flows (floats only after the fixed point is inserted). Outputs: `cfg910_d01.out/.json` (real), `cfg910_d01_MUTATE_VERTEX.out/.json`, `cfg910_d01_MUTATE_GRAV.out/.json`; first executions kept if anything is changed after them (disclosed). AS1–AS3 and lane B are imported read-only with bytecode writing disabled. Only this lane's paths are committed. No push.

## 12. What this scoped lane does NOT do (remains for a full D01)

* The pure-gravity fluctuation couplings are not resolved: mu_h from the zero-momentum graviton two-point flow, eta_h from its momentum dependence, g_h3 and lambda_3 from the graviton three-point flow, with matter. They are held at the background fixed point (closure F1). The eta_h = 0 and lambda_3 = 0 probes are the only handle on this.
* The aah vertex is projected at zero graviton momentum only (no symmetric-point projection).
* The charged-matter non-covariant remainder in beta_g3 is bracketed, not computed.
* The R^2 and C^2 truncations are not repeated in the fluctuation approach.
* No published fluctuation computation (recalled: Christiansen–Eichhorn arXiv:1702.07724; Eichhorn–Held–Wetterich arXiv:1711.02949; Eichhorn–Labus–Pawlowski–Reichert arXiv:1804.00012) is reproduced: none is in the repository and nothing is downloaded. The external gate the door names is therefore NOT run; the internal gates G-BF and G-COV replace it, and this is disclosed as a limitation.
