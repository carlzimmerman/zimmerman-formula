# CFG907: alpha door D07, the noncommutative-geometry spectral action with a forced cutoff function

**Result: KILLED.** The spectral action fixes the three gauge couplings at its cutoff Λ through f_0 = f(0). The entropy reading of the spectral action forces f_0 = ln 2, so the unified coupling is predicted as 1/alpha_U = 8 ln 2/π = **1.765**. At the scale where g_2 = g_3 (2.84e16 GeV), the measured couplings run up to **46.14**, a miss of **×26.1** (z = −72). Imposing the boundary on hypercharge and running it down with Y1's validated machinery gives **1/alpha(0) = 78.354** against 137.036 (−42.8%, z = −67.7). All 8 configurations in the option space are KILLED, as the door expected (×18–26). Nothing here derives alpha. Alpha stays an INPUT; kappa = 1/2 stays FITTED. This is **post-ledger alpha attempt #4** (rules and door: `../CFG895_alpha_campaign_ledger/`; #1 CFG896, #2 CFG901, #3 CFG906). **N_mech: 374 → 375.**

**Wall note.** The Standard-Model mass sector is WALLED. M_t, M_H and M_W enter only as labelled inputs of Y1's running, and alpha_s enters the same way. None of them is derived. The minimal NCG model's Higgs-mass relation lies in the walled sector, so it was neither used nor computed. kappa and the record's Z play no part.

## What was tested

* **The boundary condition.** In the spectral action Tr f(D_A/Λ) the Yang–Mills terms sit in f_0 a_4. Canonical normalisation then gives g_3² = g_2² = (5/3) g'² = g_U² and g_U² f_0/(2π²) = 1/4 at Λ (Chamseddine–Connes–Marcolli, hep-th/0610241, **recalled**). The script also re-derives this rather than relying on the recall:
  * the Gilkey a_4 coefficient with the Lichnerowicz E = −R/4 − ½γγF gives −(2/3)(4π)⁻² tr_V F² (sympy, explicit Euclidean gamma matrices);
  * the 96-state H_F of SM + ν_R (both particles and antiparticles) gives C_3 = C_2 = 12 and C_Y = 20;
  * so the relation is f_0 g² C/(24π²) = 1/4, the ratio is C_Y/C_2 = 5/3, and sin²θ_W = 3/8 at Λ.
  * The Gilkey coefficients themselves are checked numerically against exact spectra:
    * the unit S² gives 1/3 and 1/15;
    * 2D Landau levels give −1/6 for the scalar and +2/3 for the spinor.
    * Every check agrees to 3e-10 relative or better.
* **The forced cutoff function.** Chamseddine–Connes–van Suijlekom (arXiv:1809.02944, **recalled**) identify the spectral action with the entropy of the second-quantised fermions. That fixes f = h with h(x) = ln(1+e⁻ˣ) + x/(1+eˣ), which is the binary entropy of a Fermi occupation (checked at 30 digits; agreement and evenness to 3e-30). It gives:
  * f_0 = h(0) = ln 2, independent of the cutoff or temperature scale;
  * f_2 = 9ζ(3)/4 = 2.704628 and f_4 = 225ζ(5)/8 = 29.16359 (derived here and checked by quadrature).
* **Kernel class:** K2 (posited principles). The door is a joint prediction: the second coupling leg (leg A) and the alpha leg (leg Y).
* **Running:** Y1 (four-loop gauge, three-loop y_t and λ, Buttazzo matching at M_t), imported read-only.
  * g_Y(M_t) is the unknown. It is solved by shooting so that the trajectory meets the boundary at its own μ_23. No measured g_Y or alpha is an input.
  * The map is CFG896's: 1/alpha(0) = a_Y(M_t) + a_2(M_t) + Δ_t, with Δ_t = 9.2604. This is equivalent to P = 137.036 + [a_Y^pred(M_t) − a_Y^Y1(M_t)].
* **Allowed inputs:** alpha_s(M_Z) = 0.1180 ± 0.0009, M_W = 80.3692 ± 0.0133 (for g_2), M_t = 172.57 ± 0.42, M_H = 125.10 ± 0.09, and G_N (only for the Λ_G variant).

## G1, the graded trial (entropy function, Λ = μ_23; `cfg907_d07.out`, `cfg907_d07.json`, exit 0, all 42 gate checks PASS)

| Quantity | Value |
|---|---|
| self-consistent μ_23 (a_2 = a_3) | 2.8415e16 GeV (measured trajectory 2.8055e16) |
| root a_Y(M_t) | 39.13349 (Y1-central 97.81582); unique; maximum alpha on [M_t, Λ] 0.340 (perturbative) |
| **leg A** | 1/alpha_U = **1.76508** vs a_23 = **46.1409**: ×26.14, σ_A 0.613, **z_A = −72.3** |
| **leg Y** | **1/alpha(0) = 78.3537**, miss −58.682 (−42.82%), σ_Y 0.867, **z_Y = −67.7** |
| UV cross-check | a_Y(μ_23): boundary 2.9418 vs Y1-central 61.8839, z_UV = −68.0 (same verdict) |
| joint | χ² (2 dof) = 9815; the input correlation of the legs is +0.994 (both are driven by alpha_s) |
| pre-flight | δ_route = σ_Y/137.036 = 0.0063 < 1 (diagnostic); leverage dP/d a_Y(Λ) = 1 at one loop |
| substitution test | total shift 0.0137 = **0.010** of an identity's 1.357 (the g_2 slot dominates); not an identity |
| P_single | 0.199 (log-uniform prior, the leg-Y window), not significant |
| **grade** | **KILLED** (both legs \|z\| > 3) |

**Route error, from the frozen formulas** (units of 1/alpha):

* **σ_Y = 0.867**, from these components:
  * map: 0.1206;
  * Thomson link: 0.0080;
  * inputs: 0.1144 in total. The items are alpha_s +0.1107, M_W −0.0267, M_t −0.0099, g_2 matching −0.0030 and g_3 matching +0.0014, with the rest below 1e-4;
  * threshold, from a ×2 change of Λ: 0.758 (P = 79.112 at 2μ_23 and 77.595 at μ_23/2);
  * strong-coupling boundary, with ε = 3α_U/4π = 0.135: 0.386;
  * loop order: 0.0052.
* **σ_A = 0.613**, from these components:
  * inputs: 0.052;
  * Y1: 0.055;
  * threshold: 0.560;
  * boundary: 0.239.
* **P by loop order:** 79.019 (1 loop), 78.391 (2), 78.359 (3) and 78.354 (4).

Leg A uses no alpha and no running below the crossing. Its ×26 miss is 72 times its combined error.

## The option space (K = 8): every configuration, the same rules

| Cutoff function | Λ | Λ (GeV) | 1/alpha(0) | z_Y | 1/alpha_U vs (a_2+a_3)/2 | z_A | E1: a_3 − a_2 (z) | Grade |
|---|---|---|---|---|---|---|---|---|
| **entropy, f_0 = ln 2** | **μ_23** | 2.84e16 | **78.354** | −67.7 | 1.765 vs 46.141 (×26.1) | −72.3 | (0 by construction) | **KILLED (graded)** |
| entropy | μ_12 (contaminated) | 1.12e13 | 69.759 | −77.8 | 1.765 vs 39.799 (×22.5) | −61.9 | −4.88 (−11.0) | KILLED |
| entropy | μ_13 (contaminated) | 1.73e14 | 72.763 | −74.5 | 1.765 vs 42.014 (×23.8) | −65.7 | −3.17 (−7.2) | KILLED |
| entropy | Λ_G = M_P √(π/64f_2) | 1.64e18 | 82.800 | −63.0 | 1.765 vs 49.425 (×28.0) | −77.7 | +2.52 (+5.7) | KILLED |
| characteristic, f_0 = 1 | μ_23 | 2.84e16 | 79.621 | −66.1 | 2.546 vs 46.145 (×18.1) | −71.0 | (0) | KILLED |
| characteristic | μ_12 | 1.12e13 | 71.030 | −76.3 | 2.546 vs 39.804 (×15.6) | −60.7 | −4.87 (−11.0) | KILLED |
| characteristic | μ_13 | 1.73e14 | 74.033 | −72.9 | 2.546 vs 42.020 (×16.5) | −64.5 | −3.17 (−7.2) | KILLED |
| characteristic | Λ_G | 3.83e18 | 84.993 | −60.4 | 2.546 vs 50.113 (×19.7) | −77.6 | +3.04 (+6.9) | KILLED |

* **The placements μ_12 and μ_13 locate Λ with the measured g_Y**, which is an alpha proxy. The measured-g_Y substitution slot moves their predictions by 0.57 (μ_12) and 0.37 (μ_13) of the shift in a_Y^meas(M_t). They are therefore partly contaminated; this was disclosed before computing.
* **Λ_G is the fully forced variant.** f_2 from the entropy function, together with Newton's constant, fixes Λ, so no scale is chosen. All three legs fail there.
* **σ_E1** = sqrt(inputs² + Y1² + threshold²). This formula is defined in the script; the frozen text left the E1 error unspecified.

## Reported items R1–R4

* **R1, the ratio leg alone** (f_0-free; a_Y(Λ) = (5/3) a_2(Λ), i.e. sin²θ_W = 3/8 run down):
  * **μ_23:** 152.094 (+15.06, z +10.7). This is Z1's and N1's −19.6% non-unification expressed as an alpha(0) number.
  * **μ_12:** 137.0360. It is an identity by construction: the measured-g_Y slot moves it by 1.000 of the a_Y^meas shift.
  * **μ_13:** 142.304 (+5.27, z +3.8; g_Y slot 0.65). It is **not** an identity, contrary to my pre-registered expectation. The ratio leg ties g' to g_2, but at μ_13 it is a_1 that equals a_3.
* **R2, the full NCG run-down.** All three couplings are set to g_U (alpha_U = 0.567) at Λ = μ_23 and run down. alpha_3 reaches 1 at:
  * 1.43e16 GeV at one loop (Λ/1.99);
  * 1.59e16 at two loops (Λ/1.79);
  * 1.62e16 at four loops (Λ/1.76).

  The full joint boundary therefore has **NO SOLUTION** with a perturbative Standard Model below Λ.
* **R3, Λ = M_P.** P = 84.995 (entropy) and 86.264 (characteristic). P rises with Λ, so no Λ ≤ M_P brings the boundary within 50 of 137.
* **R4, tuned knobs** (by construction, not predictions):
  * leg A needs f_0 = 18.12, which is 26.1 × ln 2 (the fermion-multiplicity equivalent of about 78 generations);
  * leg Y needs f_0 = 14.58 (21.0 × ln 2). The two differ because the couplings do not unify;
  * the one-loop Λ at which the entropy boundary would meet Y1's a_Y is 9e39 GeV, far past M_P, in the U(1) Landau region.

## Gates and controls

* **K1.** Y1 reproduced exactly:
  * a_Y, a_2, a_3 and a_em at X_P = 55.23423, 49.20258, 52.97131 and 104.43681;
  * the Buttazzo-input couplings at M_P = 0.615371, 0.505457, 0.487311, 0.382475 and −0.014367.
* **K2.** Z1's SM non-unification reproduced with Z1's grid:
  * the minimum GUT spread is 7.619% at 1.7370e14 GeV, and the minimum Y spread is 8.367% at 3.3883e19;
  * all six pairwise crossings and third-coupling misses match: a_2 = a_3 at 2.785e16, where a_1 misses by −19.56%;
  * the refined crossings lie inside Z1's grid steps.
* **K3.** The boundary derived (8 checks, exact rationals): tr(γγγγ)FF = −8 F.F; tr_S E_F² = −2 F.F; −2/3; C = 12, 12, 20; ratio 5/3; sin²θ_W = 3/8; normalisation 1/4; C_3 = C_2.
* **K4.** Gilkey numerics:
  * S²: 0.3333333333 and 0.0666666666;
  * Landau: −0.1666666666 (scalar) and +0.6666666666 (spinor).
* **K5.** h is the binary entropy, h is even, h(0) = ln 2; f_2 and f_4 by quadrature agree with the closed forms within the 1e-10 gate (12 printed digits identical).
* **K6.** The EH coefficient is −96 f_2 Λ²/(24π²), giving Λ_G = 1.64478e18 GeV (entropy) and 3.82540e18 GeV (characteristic).
* **K7.** Planted controls:
  * a planted boundary returns P = 137.0359991769;
  * a planted f_0 gives a leg-A residual of 0;
  * the classifier returns the frozen grade in all 10 cases, plus A2a's new case.
* **K8.** The solver:
  * the residual is 4e-15;
  * P changes by 3e-11 between ODE rtol 1e-11 and 1e-13;
  * there is one sign change, f is monotone on the perturbative points, and the root is perturbative.
* **K9.** One-loop linearity: −59.286750062 on both sides.
* **MUTATE** (boundary ratio 5/3 → 3/5; `cfg907_d07_MUTATE.out`): exit 1.
  * Exactly K3e and K3f fail.
  * G1's P moves 78.354 → 76.530 (−1.82; hand estimate −1.9).
  * R1 at μ_23 moves 152.09 → 102.90 (−49.2).
* **MUTATE_NORM** (H_F without the antiparticle half, 48 states; `cfg907_d07_MUTATE_NORM.out`): exit 1.
  * Exactly K3d, K3g and K6 fail.
  * Leg A halves (1.765 → 0.883, ratio exactly 0.5), so the doubling convention moves the prediction away from 137.
  * G1's P moves −1.42 (hand estimate −1.5).
  * Cosmetic: that output still labels 1/alpha_U as "8 ln2/pi" although the value printed is the mutated 4 ln2/π.
* As frozen, the MUTATE runs skip the input re-solves (σ_in = 0 there, so their z values are indicative only).

## Execution history (amendments are appended to `CFG907_PREREGISTRATION.md`)

1. **Frozen criteria** were committed alone before any script (088b4e0b2).
2. **First execution: crashed.** It stopped at G1's first root solve, because scipy's brentq rejected rtol = 4e-16, before any graded or reported value existed. Three gates had failed from code bugs:
   * K3b and K3c: an unexpanded complex sympy trace, whose hand-expanded value is the frozen −2 F.F;
   * K3d: an extra anomaly check, not in the frozen criteria, that lacked chirality signs.

   As frozen, this execution is NOT COMPLETED. **Amendment A1** made code fixes only and changed no criterion. It was committed with the first-run script and outputs (2bac4efb6).
3. **Second execution.** All gates passed except K8c, and the run then crashed in the report-only loop-order table. **As frozen + A1, it is NOT COMPLETED.**
   * K8c failed because scan points below a_Y(M_t) ≈ 36 stalled at a_Y(Λ) ≈ 0.42 instead of blowing up. The truncated four-loop hypercharge beta function has a spurious zero at alpha_Y ≈ 2.4, deep in the non-perturbative region; at one and two loops the same trajectories blow up as designed.
   * The crash came from the one-loop μ_23 lying outside the four-loop-based integration range.
   * **Amendment A2 is post hoc.** I wrote it after seeing G1's root (a_Y(M_t) = 39.13349, P = 78.354). It makes two changes:
     * K8c's monotonicity is required only on perturbative scan points (alpha ≤ 1 on [M_t, Λ]), together with a perturbative root. This adds a NOT DIAGNOSTIC rule for non-perturbative roots, which no configuration triggers.
     * The integration range is set per loop order.

     It was committed with the executed script and outputs (4b8b675f9).
4. **Amended real run:** exit 0, all gates pass. The graded numbers are identical to the second execution (root 39.13348911).

## Disclosures

* **Sources recalled, not read.** No download was made, and whether to read the sources is the owner's call. The recalled items are:
  * CCM's printed relations and the EH coefficient;
  * CCvS's entropy function and f_0 = ln 2;
  * Gilkey's a_2 and a_4.

  The script re-derives the gauge relations and the EH coefficient and checks the Gilkey numbers on exact spectra. What remains convention is the trace over the full 96-state H_F, as in CCM; MUTATE_NORM shows that halving it moves the prediction away from 137.
* **The comparison target is built from an alpha proxy.** It is Y1-central's a_Y(M_t), from (G_F, M_W, M_Z) on shell. It is used only as the target, together with Δ_t, the SM 0 → M_t transport. Δ_t's alpha-proportional part (two-loop QED, bounded at 4 × the leptons) moves P by at most 3.7e-4 under the 1% substitution. This is the same convention as CFG896.
* **The boundary is at strong coupling** (alpha_U = 0.567). Matching the cutoff coupling to MS-bar carries a declared 13.5% boundary error (ε = 3α_U/4π). The verdict would survive an error many times larger.
* **Hand expectations against results:**
  * every central value fell inside the pre-registered ranges;
  * σ_Y came out at 0.867, against the expected 0.9–1.0;
  * R1 at μ_13 is not an identity (142.30), as noted above.
* **Prior record.** The record has no NCG alpha attempt. A kappa-side verdict (CFG894 K181) found the f-moments free; the entropy identification removes that freedom for f_0, and the forced value misses by ×26. N1 and Z1 already had the −19.6% ratio miss at μ_23, which R1 restates.
* **Stop rule (rules §6).** This is the first result on D07. A second consecutive KILLED or NOT DIAGNOSTIC result closes the door unless a new forced element appears. A non-minimal spectral triple (for example Pati–Salam) changes the content and the running, so it would be a different door.
* **Compute.** One core at nice 10. Real run 136 s and 128 MB; MUTATE 121 s; MUTATE_NORM 106 s. Y1, Z1 and lane B were imported read-only with bytecode writing disabled; no file of another lane was edited.
* Never say "theory closed". kappa = 1/2 is FITTED; alpha is an INPUT.

## Ledger rows (proposed; this lane edits neither ledger)

`campaign_fresh_gravity/LEDGER.md`:

| CFG907 | (block 900–909; criteria 088b4e0b2; amendments A1 2bac4efb6 (code only, after a crashed first execution) and A2 4b8b675f9 (post hoc, after seeing G1's root); agent lane; α door D07, post-ledger attempt #4) NCG spectral action with the entropy cutoff (CCvS, recalled): f_0 = h(0) = ln 2 forced, boundary g_3² = g_2² = (5/3)g'², g_U² f_0/2π² = 1/4 (CCM, recalled; re-derived from Gilkey a_4 + the 96-state SM + ν_R traces, Gilkey numbers checked on S² and Landau spectra): **KILLED** — G1 (Λ = μ_23 = 2.84e16, self-consistent shooting with Y1, no measured α as input): leg A 1/α_U = 8 ln2/π = 1.765 vs a_23 46.14 (×26.1, z −72.3); leg Y 1/α(0) = 78.354 (−42.8%, z −67.7, σ 0.87). All 8 configurations KILLED (characteristic f_0 = 1 ×18.1, P 79.6; μ_12/μ_13 placements contaminated, P 69.8–74.0; forced Λ_G = M_P√(π/64f_2) P 82.8/85.0 with E1 also failing); no Λ ≤ M_P gives P > 86.3; full run-down non-perturbative (α_3 = 1 at Λ/1.8: NO SOLUTION); f_0-free ratio leg 152.1 at μ_23. K1 Y1 and K2 Z1 non-unification reproduced; MUTATE (ratio 5/3 → 3/5) and MUTATE_NORM (48 states) exit 1, P moves −1.82 / −1.42. N_mech 374→375. α stays an input. | (run commit) |

`ALPHA_ATTEMPTS_LEDGER.md`:

| CFG907 | GEO/FP | campaign_fresh_gravity/CFG907_alpha_D07_ncg_spectral_action | Door D07: NCG spectral action with the entropy cutoff f_0 = ln 2 (CCvS); boundary g_3² = g_2² = (5/3)g'², g² f_0/2π² = 1/4 at Λ = μ_23; Y1 running, joint legs | 78.354 graded (1/α_U = 1.765 vs a_23 = 46.14, ×26); configurations 69.8–85.0; ratio leg alone 152.1 | KILLED: z_Y = −67.7, z_A = −72.3 (σ 0.87 / 0.61); all 8 configurations KILLED; full run-down non-perturbative | 1 | 088b4e0b2 / 2bac4efb6 / 4b8b675f9 / (run commit) |

## Files

| File | Contents |
|---|---|
| `CFG907_PREREGISTRATION.md` | The frozen criteria (088b4e0b2) with amendments A1 (2bac4efb6) and A2 (4b8b675f9) appended. |
| `cfg907_d07.py` | Gates K1–K9, G1, the 8 configurations, R1–R4, the substitution test, and the MUTATE modes. |
| `cfg907_d07.out`, `.json`, `.err` | The amended real run (exit 0). |
| `cfg907_d07_MUTATE.out`, `.json`, `.err` | The ratio-flip control (exit 1). |
| `cfg907_d07_MUTATE_NORM.out`, `.json`, `.err` | The 48-state control (exit 1). |
| `cfg907_d07_FIRSTRUN.py`, `.out`, `.err` | The first execution (crashed, NOT COMPLETED), unchanged except for sanitised paths in the traceback. |
| `cfg907_d07_RUN2.out`, `.err` | The second execution (K8c failed, crashed in the report table, NOT COMPLETED); its script is the version of `cfg907_d07.py` in 4b8b675f9. |

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 cfg907_d07.py` for the real run (about 2.3 minutes, 128 MB), and `... cfg907_d07.py MUTATE` or `... cfg907_d07.py MUTATE_NORM` for the controls (about 2 minutes each).
