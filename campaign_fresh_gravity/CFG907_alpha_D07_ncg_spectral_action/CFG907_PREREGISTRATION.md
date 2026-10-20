# CFG907: alpha door D07, the noncommutative-geometry spectral action with a forced cutoff function (FROZEN pre-registration)

Written 2026-10-20, before any script of this lane was written or run. No number of this lane has been computed by any script when this file is committed. What I looked at before freezing is listed in section 11 (reading files, a tracked-file text search, and printing the summary block of Y1's committed `y1_4_results.json`). All numbers in sections 7 and 10 are hand estimates (one-loop arithmetic from committed Y1 / Z1 values).

This is **a post-ledger attempt of the alpha campaign** (rules: `campaign_fresh_gravity/CFG895_alpha_campaign_ledger/ALPHA_CAMPAIGN_RULES.md`; door: `ALPHA_DOORS.md`, section D07). Attempt #1 was CFG896 (door D02), #2 CFG901 (door D03); CFG906 (door D04) runs in parallel and is not committed as I write, so this is attempt **#3, or #4 if CFG906 is committed first** (the ledger orders by commit). Nothing here is expected to derive alpha. The door's own expectation is **KILLED by an order of magnitude (×18–26)**.

**Wall note.** The Standard-Model mass sector is WALLED. Measured masses (M_t, M_H, M_W) and alpha_s enter only as labelled inputs of Y1's validated running; none is derived or tuned. The minimal NCG model's Higgs-mass relation lies in the walled sector and is not used or computed. kappa and the record's Z play no part. Alpha stays an INPUT of the record.

## 1. Mechanism

In the spectral action principle (Chamseddine–Connes; Chamseddine–Connes–Marcolli, hep-th/0610241, **recalled**), the bosonic action of the almost-commutative geometry M × F of the Standard Model (+ nu_R) is Tr f(D_A/Λ). Its heat-kernel expansion, 2 f_4 Λ⁴ a_0 + 2 f_2 Λ² a_2 + f_0 a_4 + O(Λ⁻²), with f_0 = f(0), f_2 = ∫₀^∞ f(v) v dv, f_4 = ∫₀^∞ f(v) v³ dv, puts the Yang–Mills terms in f_0 a_4: (f_0/(2π²)) ∫ (g_3² G² + g_2² W² + (5/3) g_1² B²). Canonical normalisation then gives, at the cutoff scale Λ, **g_3² = g_2² = (5/3) g_1² (= g_U²) and g_U² f_0/(2π²) = 1/4** (g_1 = the SM hypercharge coupling g'; sin²θ_W = 3/8). Normally f is an arbitrary positive even cutoff function, so f_0 is a free number fitted to the measured couplings (class K0). Chamseddine–Connes–van Suijlekom, "Entropy and the spectral action" (arXiv:1809.02944, **recalled**), identify the spectral action with the von Neumann entropy of the second-quantised fermion system, which fixes f as the fermionic entropy function h(x) = ln(1 + e^(−x)) + x/(1 + e^x), the binary entropy of a Fermi occupation 1/(1 + e^x). Then **f_0 = h(0) = ln 2** is a forced, scale-free number: the entropy of a half-filled zero mode. That makes the absolute value of the unified coupling a prediction: 1/alpha_U = 4π/g_U² = **8 f_0/π = 8 ln 2/π = 1.7651**. Hypercharge then follows as alpha_Y(Λ) = (3/5) alpha_U.

## 2. Forced-kernel candidate and class (rules §2)

* **C(alpha) = 0** is the boundary condition at Λ: g_Y(Λ)² − (3/5) π²/(2 f_0) = 0 with f_0 = h(0), jointly with g_2(Λ)² = g_3(Λ)² = π²/(2 f_0). **Class K2**: the spectral action principle and the entropy identification are posited principles, not consistency conditions. The best grade it can reach is EVIDENCE, and only with a second, independent prediction that checks out (here the second coupling leg, section 6).
* **Why the solution set in alpha is discrete.** The boundary fixes one number alpha_Y(Λ); with Λ located by the E1 leg (the unique crossing of a_2 and a_3, section 3) and a strictly monotone running map a_Y(Λ) ↔ a_Y(M_t), the prediction of 1/alpha(0) is a single value. Uniqueness of the shooting root is checked (section 8).
* **What is forced and what is not.** f_0 is forced by the entropy identification (independent of the temperature/cutoff scale, because the a_4 term carries Λ⁰). f_2 is forced too (f_2 = 9ζ(3)/4, section 4), which with Newton's constant would fix Λ (variant Λ_G, reported). The placement of Λ at the g_2 = g_3 crossing is the standard NCG practice and the door's prescription; other placements are counted in K.

## 3. Which alpha, which scale, which scheme

* **Prediction (graded):** alpha(0), the Thomson limit. Target 1/alpha(0) = 137.035999177 (CODATA 2022), used only as the target.
* **UV quantities:** alpha_Y(Λ) = (3/5) π/(8 f_0) and alpha_2(Λ) = alpha_3(Λ) = π/(8 f_0), imposed at Λ = μ_23, the scale where a_2 = a_3 (a_i = 4π/g_i²) on the trajectory itself.
* **Running and map (Y1's validated machinery, imported read-only, as in CFG896):** `y1_lib` four-loop gauge betas, three-loop y_t and lambda, Buttazzo matching at μ = M_t, g_3 by Y1's QCD-only SMDR-calibrated route. The hypercharge coupling is NOT taken from the measured on-shell inputs: g_Y(M_t) is the unknown, solved by shooting so that the trajectory meets the boundary at its own μ_23 (self-consistent, so no measured g_Y enters at any loop order). The map to alpha(0) is CFG896's: 1/alpha(0) = a_Y(M_t) + a_2(M_t) + Δ_t with Δ_t = 137.035999177 − (a_Y + a_2)(M_t) at the Y1-central point (the 0 → M_t transport). Equivalently P = 137.036 + [a_Y^pred(M_t) − a_Y^Y1(M_t)]: the comparison is a_Y(M_t) predicted against Y1-central's, carried to the Thomson limit by the SM transport (disclosed, section 5).
* **Error carried for the running (rules §1.3):** Y1's σ(a_em)/137.036 = 8.8e-4 (0.1206 absolute, read from `y1_4_results.json` as CFG896 does) plus Y1's Thomson-link term, inside σ_Y (section 7).
* **UV cross-check (reported; the verdict must agree):** a_Y(μ_23) predicted (= (5/3) 8 f_0/π) against Y1-central's a_Y at μ_23.

## 4. The boundary condition, derived here as well as recalled

The recalled CCM relations are re-derived by the script from textbook heat-kernel coefficients (Gilkey; Vassilevich hep-th/0306138, **recalled**) and the SM + nu_R content, and the coefficients are checked numerically (gates K3–K6):

* For D_A = iγ^μ∇_μ on S ⊗ H_F (4D Euclidean), D_A² = −(∇² + E) with E = −R/4 − (1/2) γ^μγ^ν F_μν (Lichnerowicz). With a_4 = (4π)⁻² (1/360) ∫ tr(180 E² + 30 Ω_μνΩ_μν + ...), the spinor traces give tr_S(E_F²) = −2 tr_V(F_μνF_μν) and tr_S(Ω²) ⊃ 4 tr_V(F_μνF_μν), so the gauge part of a_4 is (4π)⁻²(−2/3) ∫ tr_V(F_μνF_μν). For F = −i g F^a T^a this is (g² C/(24π²)) ∫ F^aF^a with C = tr_{H_F}(T^aT^a) (no sum). Canonical (1/4) F^aF^a: **f_0 g² C/(24π²) = 1/4**.
* **Content traces over H_F (96 states = 3 generations × 16 with nu_R × particles + antiparticles):** C_3 = 12, C_2 = 12, C_Y = tr(Y²) = 20 (Q = T_3 + Y). Hence f_0 g_3²/(2π²) = f_0 g_2²/(2π²) = (5/3) f_0 g'²/(2π²) = 1/4: the recalled CCM relations and sin²θ_W = 3/8.
* **Einstein–Hilbert coefficient** (reported variant only): a_2 = (4π)⁻² (1/6) ∫ tr(6E + R) gives 2 f_2 Λ² a_2 = −(96 f_2 Λ²/(24π²)) ∫ R (recalled CCM form (96 f_2Λ² − f_0 c)/(24π²), with the Majorana term c neglected, flagged), so 1/(16πG) = 4 f_2 Λ²/π² and **Λ_G = M_P sqrt(π/(64 f_2))**, M_P = G^(−1/2) = 1.22089e19 GeV.
* **Cutoff functions and moments:** entropy h: f_0 = ln 2 = 0.693147, f_2 = (9/4) ζ(3) = 2.704628, f_4 = (225/8) ζ(5) (derived here: ∫x^(s−1) ln(1+e^(−x)) = Γ(s)η(s+1), ∫x^s/(1+e^x) = Γ(s+1)η(s+1)); characteristic χ_[0,1] (and every f with f(0) = 1): f_0 = 1, f_2 = 1/2, f_4 = 1/4.

Recalled and flagged (no download; whether to read the sources is the owner's call): the CCM printed relations g_3² = g_2² = (5/3) g_1², f_0 g²/(2π²) = 1/4, sin²θ_W = 3/8, the EH coefficient; the CCvS entropy function h and f_0 = h(0) = ln 2; the Gilkey a_2, a_4 coefficients. The derivation above makes the gauge relations independent of the recall, up to the trace convention of the spectral action (full 96-state H_F, as in CCM), which the MUTATE_NORM control varies.

## 5. Inputs

| Input | Value | Label |
|---|---|---|
| alpha_s(M_Z) | 0.1180 ± 0.0009 | measured (allowed), via Y1's g_3 route |
| M_W | 80.3692 ± 0.0133 GeV | measured (allowed), g_2(M_t) via Buttazzo's NNLO formula (Y1) |
| M_t | 172.57 ± 0.29 (exp) ± 0.30 (th) GeV | measured (allowed), y_t |
| M_H | 125.10 ± 0.09 GeV | measured (allowed), lambda |
| y_b, y_tau at M_t | SMDR reference values (Y1) | declared convention (tiny) |
| G_N | M_P = 1.22089e19 GeV | measured (allowed); variant Λ_G only |
| f_0, f_2 | ln 2, 9ζ(3)/4 (entropy); 1, 1/2 (characteristic) | derived |
| C_3, C_2, C_Y | 12, 12, 20 | derived from the SM + nu_R content |

**No measured alpha is an input** of the graded prediction. **Contamination list (rules §1.4), quantified by the substitution test:**
1. Δ_t is the target transport, built from 137.036 and Y1-central's a_em(M_t) (which came from the on-shell (G_F, M_W, M_Z) combination). Physically it is the 0 → M_t running, alpha-independent at one loop; its alpha-proportional part is bounded as in CFG896 (two-loop QED leptons × 4).
2. g_2(M_t): Buttazzo's NNLO matching from M_W contains alpha at loop level; slot = 1% of (g_2 − 2M_W/v).
3. g_3(M_t): the SMDR calibration factor of Y1's QCD-only route carries electroweak effects; slot = 1% of |calibration − 1| × g_3.
4. y_t and lambda matching (enter μ_23 only at two loops): slots as CFG896 (1% of NNLO − tree for lambda; 1% of a 2% electroweak share of y_t).
5. The measured g_Y (Buttazzo, on-shell, the alpha proxy) is NOT used by G1. It is used by the K-tests, by the target, and by the reported placements μ_12 and μ_13, which locate Λ on the measured trajectory and are therefore contaminated (their substitution test also scales g_Y).
6. G_N, f-moments, heat-kernel numbers, content: no alpha.

The substitution test scales every slot as if alpha were 1% larger and reports the shift of P as a fraction of the 1.357 an identity would show. Residual and shape tests do not apply (no closed form plus series).

## 6. Option space and the graded trial

| Axis | Options | Count |
|---|---|---|
| Cutoff function | **entropy h, f_0 = ln 2 (forced; graded)**; characteristic χ / any f(0) = 1, f_0 = 1 (K0, reported) | 2 |
| Placement of Λ | **μ_23 (a_2 = a_3, from alpha_s and g_2; graded)**; μ_12 (a_1 = a_2, contaminated); μ_13 (a_1 = a_3, contaminated); Λ_G (forced by f_2 and G_N) | 4 |

**K = 8.** Exactly **one graded trial: G1 = entropy function, Λ = μ_23 on the self-consistent trajectory, the joint boundary with two legs**:
* **leg A (second coupling, no alpha):** 1/alpha_U predicted = 8 f_0/π against a_23 = a_2(μ_23) = a_3(μ_23) on the G1 trajectory;
* **leg Y (alpha):** a_Y(μ_23) = (5/3)(8 f_0/π), shot to M_t, P = 1/alpha(0).

E1 (g_2 = g_3) is consumed to locate Λ, so it is not a leg of G1. The other 7 configurations are reported with the same rules. **N_mech: +1** (373 → 374 if CFG906 has not landed; otherwise CFG906's new count + 1). One joint trial counts once, as CFG896 counted its joint pairs.

**Reported, not counted in K (references and feasibility):**
* R1, the f_0-free ratio leg alone (E2: a_Y(Λ) = (5/3) a_2(Λ), the classic sin²θ_W = 3/8 run-down) at μ_23 (a real test) and at μ_12, μ_13 (identities by construction: there a_1 equals a_2 or a_3 by definition of the crossing, using the measured g_Y).
* R2, the full NCG run-down: all three couplings set to g_U at Λ = μ_23 (y_t, lambda, y_b, y_tau from the G1 trajectory) and run down with Y1's betas (1, 2 and 4 loops); the scale where alpha_3 or alpha_2 first exceeds 1 is printed. If it lies above M_t the full joint boundary has NO SOLUTION with a perturbative SM.
* R3, the upper end of the allowed range: P with Λ = M_P (entropy and characteristic); P(Λ) increases with Λ, so this is the largest value any Λ ≤ M_P gives.
* R4, tuned knobs (by construction, not predictions): f_0* = π a_23/8 (leg A), f_0,Y* = (3π/40) a_Y^Y1(μ_23) (leg Y), and the fermion-multiplicity equivalent 3 f_0*/f_0.

## 7. Leverage and precision pre-flight (rules §1.6), written now

* **Leverage.** The boundary acts on the coupling itself: dP/d a_Y(Λ) = 1 at one loop, so d ln a_Y(Λ)/d ln(1/alpha(0)) ≈ 137.04/61.85 ≈ 2.2 at the measured point (O(1), unlike the FSP equation's 5e-4). dP/d ln Λ = b_Y/(2π) = 41/(12π) = 1.088.
* **Input propagation (hand):** σ(a_3(μ_23)) from alpha_s ≈ 0.063 and d(a_3 − a_2)/d ln μ = 1.114 − 0.504 = 0.610 give σ(ln μ_23) ≈ 0.10, i.e. 0.11 in P; M_W adds ≈ 0.02. With Y1's map 0.1206: σ_in ≈ 0.17.
* **Route error, frozen formulas** (each component computed by the script; quadrature):
  * σ_Y (leg Y, in units of 1/alpha(0)) = sqrt(σ_map² + σ_Thomson² + σ_in² + σ_thr,Y² + σ_bnd,Y² + σ_loop²), where σ_in = input items (alpha_s, M_W, M_t, M_H, g_3 matching Y1 E5b, g_2 matching Y1 E5a) by central differences of re-solves at ±1σ; σ_thr,Y = half the spread of P with the boundary imposed at 2μ_23 and μ_23/2 (scheme/threshold at Λ; hand 0.754); σ_bnd,Y = half the spread of P with a_Y(Λ) scaled by (1 ± ε_bnd), ε_bnd = 3 alpha_U/(4π) (the strong-coupling matching of the cutoff coupling to MS-bar, largest Casimir; 0.135 for the entropy function; hand ≈ 0.40); σ_loop = |P(4-loop gauge, 3-loop y_t/lambda) − P(3-loop gauge, 2-loop y_t/lambda)|. Hand: σ_Y ≈ 0.9–1.0.
  * σ_A (leg A, in units of 1/alpha) = sqrt(σ_in,A² + σ_Y1,A² + σ_thr,A² + σ_bnd,A²), with σ_Y1,A = Z1's relative error of a_3 (0.0012) × a_23, σ_thr,A = half the spread of (a_2 + a_3)/2 at 2μ_23 and μ_23/2 (hand 0.56), σ_bnd,A = ε_bnd × 8 f_0/π (0.24). Hand: σ_A ≈ 0.65.
* **δ_route = σ_Y/137.036 ≈ 0.007 < 1**, so the route is diagnostic by rules §1.6. A joint two-coupling route can in principle reach EVIDENCE (K9); the K2 class caps it there.
* **Option-space bar (rules §4.3):** with K = 8, a single mechanism trial needs a relative miss of roughly 3e-4 for P < 1e-3, and campaign-wide (N_mech ≈ 374) roughly 8e-7. Any miss of order 10% or more is far outside both.

## 8. Gates, grades and kill criteria (frozen)

**Gates (all must pass, else NOT COMPLETED):**
* **K1, Y1 reproduced.** Y1-central at X_P: a_Y 55.2342, a_2 49.2026, a_3 52.9713, a_em 104.4368 (tolerance 1e-4); Buttazzo-input like-for-like at M_P: g_1 0.61537, g_2 0.50546, g_3 0.48731, y_t 0.38248, lambda −0.01437 (1e-5). (Exactly CFG896's K1.)
* **K2, the SM one-scale unification failure (Z1) reproduced** with Z1's own 4000-point grid: GUT-normalised minimum spread 7.62% at 1.737e14 GeV (1/alpha 40.47, 43.63, 40.47), Y-normalised 8.37% at 3.388e19; pairwise crossings Y 5.351e20 (+12.0%), 3.388e19 (−8.1%), 2.785e16 (+34.1%); GUT 1.112e13 (−11.5%), 1.718e14 (+7.8%), 2.785e16 (−19.6%). Tolerances: half a unit of the last printed digit. Plus the refined (brentq) crossings, which must lie within one grid step of Z1's.
* **K3, the boundary derived.** sympy with explicit 4×4 Euclidean gamma matrices: tr(γ^μγ^νγ^ργ^σ) F_μνF_ρσ = −8 F_μνF_μν for random antisymmetric F; Gilkey combination (1/360)(180 × (−2) + 30 × 4) = −2/3; content traces over the 96-state H_F: C_3 = C_2 = 12, C_Y = 20; hence C_Y/C_2 = 5/3 (= the recalled printed ratio), sin²θ_W = 3/8, and f_0 g² C/(24π²) = 1/4 ⇔ f_0 g²/(2π²) = 1/4 (= the recalled printed relation), exact rationals.
* **K4, Gilkey coefficients checked numerically** on exact spectra: (a) unit S² scalar Laplacian, Σ(2l+1)e^(−t l(l+1)): t K(t) = 1 + t/3 + t²/15 + ...; the extracted t and t² coefficients must equal 1/3 (the R/6 term) and 1/15 (the 5R² − 2Ric² + 2Riem² term) to 1e-6; (b) 2D Landau levels with field B: scalar (2n+1)B, degeneracy B/2π: t² coefficient of 4πt K/area = −B²/6 (the Ω² term, 30/360); spinor (σ_3 split): +2B²/3 (the E² + Ω² combination, 180/360 and 30/360), each to 1e-6 relative.
* **K5, cutoff moments.** sympy and mpmath quadrature: h is even; h equals the binary entropy of the occupation 1/(1+e^x); h(0) = ln 2; f_2 = 9ζ(3)/4 and f_4 = 225ζ(5)/8 (quadrature to 1e-10); χ: 1, 1/2, 1/4.
* **K6, EH coefficient.** 2 f_2 Λ² (4π)⁻² (1/6) tr_{S⊗H_F}(6E + R)|_R = −(96 f_2 Λ²/(24π²)) R exactly (sympy), and Λ_G = M_P sqrt(π/(64 f_2)).
* **K7, planted controls.** (a) boundary planted at a_Y(μ_23) = Y1-central's value: the shooting returns P = 137.035999177 within 1e-6; (b) f_0 planted at π a_23/8: z_A = 0 within 1e-9; (c) classifier cases: P = 137.036 → CONSISTENT; z = ±3.01 → KILLED; ±2.99 → CONSISTENT; leg A fails, leg Y passes → KILLED; no root → KILLED (reason: the boundary cannot be met by a perturbative SM trajectory); two roots → NOT DIAGNOSTIC; δ_route > 1 → NOT DIAGNOSTIC; a failed gate → NOT COMPLETED.
* **K8, solver.** Boundary residual |a_Y(μ_23) − target| < 1e-8 at the root; the root changes by < 1e-6 in P between ODE rtol 1e-11 and 1e-13; f is strictly monotone on the scan grid with exactly one sign change (else NOT DIAGNOSTIC for two or more, KILLED for none); acceptance is by residual, not by solver flag (the CFG896/CFG901 lesson).
* **K9, one-loop linearity.** With one-loop gauge and Yukawa betas (Opts(gauge_loops = 1, yuk_loops = 1)), the shift a_Y^pred(M_t) − a_Y^meas(M_t) equals a_Y^target(Λ) − a_Y^meas(Λ) to 1e-6 (one-loop a_Y is linear in ln μ and blind to the other couplings).

**Grade of G1 (frozen):**
1. Pre-flight: δ_route > 1 → NOT DIAGNOSTIC (not expected).
2. Leg Y root unique (K8) → value; none → KILLED; two or more → NOT DIAGNOSTIC.
3. z_Y = (P − 137.035999177)/σ_Y and z_A = (8 f_0/π − a_23)/σ_A. **|z_Y| > 3 or |z_A| > 3: KILLED** (the joint test fails if either leg fails). Both ≤ 3: CONSISTENT, reported with P_single (log-uniform 1/alpha on [10, 1000]) multiplied over the two legs and P_family over N_mech.
4. EVIDENCE would additionally need the rules §4 items (independent re-derivation, a second prediction outside the inputs, the look-elsewhere test); DERIVATION is impossible for a K2 kernel.

**Reported verdicts (not graded) use the same rules** for the other 7 configurations (for Λ_G, E1 is a third leg: z_E1 = (a_3 − a_2)/σ at Λ_G), and the R1–R4 items are printed.

## 9. MUTATE and positive controls (rules §1.9)

The load-bearing element is the boundary ratio g_1²(SM)/g_U² = C_2/C_Y = 3/5 (equivalently g_U² = (5/3) g'²).
* **MUTATE (the task's control): flip the boundary ratio** 5/3 → 3/5 (the boundary uses a_Y(Λ) = (3/5) a_U instead of (5/3) a_U, and the ratio leg uses (3/5) a_2). K3's check "ratio used = ratio derived from the content = recalled printed 5/3" must FAIL and the run must exit 1. The prediction must move: by hand, G1's P by ≈ −1.9 (a_Y(Λ) 2.94 → 1.06) and R1 at μ_23 from ≈ 152 to ≈ 103. The script checks the move is at least 0.5 in P and in the expected direction (move test, printed).
* **MUTATE_NORM (second control): drop the antiparticle half of H_F** (48 states, the doubling convention): C_3 = C_2 = 6, C_Y = 10, ratio unchanged, normalisation halved (1/alpha_U = 4 f_0/π). K3's normalisation check must FAIL, exit 1; leg A moves 1.765 → 0.883 and P by ≈ −1.5 (hand).
* MUTATE runs skip the input-error re-solves to save CPU while the 1024³ run is live (disclosed); exit 3 if a control does not bite.
* **Positive controls:** K7(a), K7(b) above.

## 10. Expected outcome (written before computing; hand, one loop from Y1 / Z1 numbers)

* μ_23 ≈ 2.8e16 GeV, a_23 ≈ 46.1. **Leg A: 1.765 vs ≈ 46.1, ×26, z_A ≈ −50 to −90.** Characteristic: 2.546, ×18.
* a_Y^Y1(μ_23) ≈ 61.85; boundary 2.94; shift −58.9 plus a two-loop correction of about +0.3. **Leg Y: P ≈ 78–79, z_Y ≈ −55 to −70. G1 KILLED.**
* Reported: characteristic at μ_23 P ≈ 79.5–80; μ_12 (1.1e13) P ≈ 70 (entropy) / 71 (characteristic); μ_13 (1.7e14) ≈ 73 / 74; Λ_G = 1.645e18 (entropy) / 3.825e18 (characteristic) GeV with P ≈ 83 / 85 and E1 failing at Λ_G (a_2 ≈ 48.2, a_3 ≈ 50.7). R3 (Λ = M_P): P ≈ 85 / 86, so no Λ ≤ M_P brings the entropy boundary near 137 (P = 137 would need a_Y^Y1(Λ) ≈ 3, i.e. Λ ~ 1e39 GeV by one-loop extrapolation, far past M_P).
* R1: ratio leg at μ_23 P ≈ 152 (+15; Z1's −19.6% in another form); identities 137.036 at μ_12 and μ_13. R2: alpha_3 reaches 1 within about one e-fold below Λ (one loop ≈ Λ/2): NO SOLUTION with a perturbative SM. R4: f_0* ≈ 18.1 (leg A) and f_0,Y* ≈ 14.6 (leg Y), different because the couplings do not unify.
* Substitution: G1 shift ≤ 0.1 (fraction < 0.1 of an identity); the μ_12/μ_13 placements partly contaminated (fraction of order 0.5); R1 at μ_12/μ_13 an identity (fraction ≈ 1).
* MUTATE and MUTATE_NORM exit 1 with the moves of section 9.
* A wrong expectation will be disclosed, not hidden.

## 11. Disclosures made before freezing

* Before freezing I read the campaign rules, D07, the ledger, CFG896's and CFG901's READMEs and pre-registrations, Y1's `y1_lib.py` interface, Z1's script and output, and printed the summary block of Y1's committed `y1_4_results.json` (the Y1 error items CFG896 also uses). I ran a tracked-file text search (`git grep`, md/py/tex) for earlier spectral-action work: the record has only legacy speculation in `ai_slop/` (no computation) and a kappa-side verdict (`opus_48_extended_research/reviews/KAPPA_CLASS6_SPECTRAL_ACTION_VERDICT_2026-06-26.md`, CFG894 K181: the f-moments are free cutoff data). The entropy identification is exactly what removes that freedom for f_0 here. No alpha attempt with NCG exists in the ledger.
* No script of this lane existed when this file was committed; no Y1 trajectory was run by me before the freeze.
* The derivation in section 4 was done by hand before freezing; the script re-does it (K3, K6) and checks the coefficients numerically (K4). A hand slip would show up as a gate failure and is disclosed if it happens.
* Stop rule (rules §6): this is the first result on D07. A second consecutive KILLED or NOT DIAGNOSTIC on D07 would close the door unless a new forced element appears.
* Compute: one core, `OMP_NUM_THREADS=1 nice -n 10`, expected under 10 minutes and under 300 MB; Y1 imported read-only with bytecode writing disabled; no file of Y1, Z1 or another lane is edited.
* Never say "theory closed". kappa = 1/2 stays FITTED; alpha stays an INPUT.

## 12. Files (planned)

`CFG907_PREREGISTRATION.md` (this file, committed alone first), `cfg907_d07.py` (gates, pre-flight, G1, reported configurations, R1–R4, substitution, MUTATE modes), `cfg907_d07.out` / `.json` (real run), `cfg907_d07_MUTATE.out` / `.json`, `cfg907_d07_MUTATE_NORM.out` / `.json`, `README.md`.

## Amendment A1 (appended 2026-10-20 after a crashed first execution; nothing above was edited)

**What happened.** The first execution of `cfg907_d07.py` (kept unchanged as `cfg907_d07_FIRSTRUN.py`, stdout `cfg907_d07_FIRSTRUN.out`, stderr with the traceback `cfg907_d07_FIRSTRUN.err`; local paths in the traceback replaced by `<repo>` and `<python>`) printed gates K3, K4, K5, K6, K1, K2 and K7(c) in that order, then **crashed at the first root solve of G1**: scipy's `brentq` refuses rtol = 4e-16 (its floor is 8.9e-16). **No graded value, no leg-A or leg-Y number and no reported configuration had been computed or printed** when it stopped (the scan's grid values are printed only after the solve returns). As frozen, that execution is NOT COMPLETED. Three gates had failed, all from code bugs, not from the physics:

* **K3b and K3c**: the spinor trace tr_S(E_F²) was built from complex gamma matrices and not expanded, so sympy printed an unreduced expression. Expanding the printed value by hand: −1636/225 + 2(−1/3 − 5i/3)(1/3 − 5i/3) + 2(−1/3 + i/3)(1/3 + i/3) = −1636/225 − 52/9 − 4/9 = −1012/75 = −2 × (506/75) = −2 F.F, the frozen value; T4 = −4048/75 = −8 F.F passed as printed. K3c failed only because it used the unreduced trace.
* **K3d**: the script added an anomaly sanity check that the frozen K3 does not list (sum Y = sum Y³ = 0 per generation) and summed left- and right-handed fields with the same sign. With the chirality sign (right-handed fields enter with −1) both sums vanish; without it the cubic sum is −4/9. The frozen K3d numbers printed correctly in the first execution: dim 96, C_3 = 12, C_2 = 12, C_Y = 20.

**Fixes (code only).** (1) `brentq` rtol 4e-16 → 2e-15 (xtol 1e-12 unchanged; the K8a residual gate is unchanged). (2) `sp.expand` before `nsimplify` for T4 and tr_S(E_F²). (3) Chirality signs in the extra anomaly check. No criterion, input, formula, option, threshold, kill rule or grade changes. The fixed script is run once as the real run; its gates must all pass.

## Amendment A2 (appended 2026-10-20 after the second execution; post hoc; nothing above was edited)

**Status of the second execution** (script = the A1-fixed `cfg907_d07.py` committed with this amendment; stdout `cfg907_d07_RUN2.out`, stderr `cfg907_d07_RUN2.err`, paths sanitized). Gates K1–K7 and K9 passed, K8a and K8b passed, **K8c failed**, and the run then **crashed** in a report-only step (the P-by-loop-order table). **As frozen (with A1) this execution is NOT COMPLETED.** I write this amendment **after seeing** G1's scan and root: a_Y(M_t) = 39.13349 (Y1-central 97.81582), self-consistent μ_23 = 2.8415e16 GeV, a_2 = a_3 = 46.141 there, hence P = 39.13349 + 29.95978 + 9.26040 = 78.354 by the frozen map; the route-error components had been computed but not printed.

* **Why K8c failed.** Scan points with a_Y(M_t) ≤ 36 returned a nearly constant f ≈ −2.52 (a_Y(Λ) ≈ 0.42) instead of an ODE blow-up, so f was not strictly monotone over the whole grid. Diagnosis (scratch script, not committed): those trajectories cross into strong coupling below Λ, and the truncated four-loop hypercharge beta function has a spurious zero at a_Y ≈ 0.418 (alpha_Y ≈ 2.4; d g_1²/d ln μ² changes sign between a_Y = 0.42 and 0.40 at fixed other couplings), where they stall; at one and two loops the same trajectories blow up (NoReach), as designed. These points are outside the perturbative domain and all lie on the negative side; the sign-change count over all points was exactly 1, as required.
* **Why the report crashed.** The mu_max of the μ_23 placement was set from the four-loop μ_23; the one-loop μ_23 lies outside 1.15 × that, so no crossing existed in range for the one-loop row.

**Amended rules.**
* **A2a (K8c on the perturbative domain).** A scan point is perturbative if alpha_Y, alpha_2 and alpha_3 (SM normalisation, alpha_Y = g'²/4π) stay ≤ 1 for all μ in [M_t, Λ] on its trajectory. K8c requires (i) exactly one sign change over all scan points (unchanged), (ii) strict monotonicity over the perturbative points, and (iii) a perturbative root trajectory. Non-perturbative points are listed. A configuration whose root is not perturbative is graded NOT DIAGNOSTIC (the running cannot be trusted there); this rule is new and is applied to every configuration.
* **A2b (loop-order rows).** For the μ_23 placement, mu_max = 1.15 × (factor) × the μ_23 of the measured trajectory at the same loop order. This affects only the integration range (the P-by-loop-order report and the σ_loop solve), not any definition.

Nothing else changes: inputs, boundary, map, error formulas, thresholds, kill rule and grades are as frozen. The amended script is run once as the real run.
