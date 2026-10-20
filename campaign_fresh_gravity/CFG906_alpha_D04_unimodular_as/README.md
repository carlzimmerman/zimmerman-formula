# CFG906: alpha door D04, unimodular asymptotic-safety f_g

**Result: KILLED.** In unimodular gravity (metric determinant fixed, transverse diffeomorphisms only, Lambda an integration constant, so the flow has one gravitational coupling g and no lambda), the asymptotic-safety route gives 1/alpha(0) = **105.628** in the graded scheme. That is 31.4 below 137.036, **z = −5.04** in units of the route's frozen error (6.230), so the grade is KILLED. Every one of the 72 pre-declared variants is KILLED as well (P from 91.58 to 106.27, z from −7.30 to −4.94). Nothing here derives alpha. Alpha stays an INPUT; kappa = 1/2 stays FITTED. This is attempt #3 of the post-ledger alpha campaign (rules and door: `../CFG895_alpha_campaign_ledger/`; attempt #1 is CFG896, #2 is CFG901).

**Wall note.** The SM mass sector is WALLED. No mass enters this lane: the gravitational fixed point depends only on field counts. kappa and the record's Z play no part.

## What was tested

Asymptotic safety adds −f_g g_Y to the hypercharge beta function. If f_g > 0, the hypercharge coupling at the Planck scale is fixed at the IR-attractive zero g_Y* = 4 pi sqrt(6 f_g/41) (kernel class K1, conditional on the AS scenario and, here, on unimodular gravity). AS1–AS4 and CFG901 gave f_g ≈ 0.037–0.048 at the standard (g, lambda) fixed point, about 4 times the 0.009805 that 137.036 needs. The door asked whether the unimodular theory, where lambda drops out, closes that gap. Its stated hope: "137 needs g* ≈ 0.222 if the TT-only structure carries over".

**Two findings decide it.**

1. **The TT part carries over exactly, but sigma does not vanish.** On the flat unimodular background there is no sqrt(g)^(2) term, so the TT contribution is AS3's committed formula with f = 0: f_g^TT = 5(4 − e)g/(72 pi), i.e. 5g/(36 pi) at the fixed point (K1 reproduces AS3's formula and its committed numbers). Under transverse diffeomorphisms, however, the traceless scalar sigma is not a gauge mode. It couples to the photon, with the conformal-mode sign, and contributes **f_g^sigma = −(2/5) f_g^TT** exactly. So the graded f_g = **(3/5) f_g^TT = g/(12 pi)**, and 137 would need g* = **0.3696** (TT only: 0.2218, the door's 0.222).
2. **The unimodular fixed point is g* = 360 pi/1327 = 0.8523,** which is unique and admissible, with critical exponent 2.119 and eta_N = −2. Matter dominates it: the R^1 coefficient is −7.372, of which the SM gives −61/12 = −5.083 and gravity −2.289. Reaching g* = 0.37 would need a coefficient of −17.0.

So f_g* = 0.022607, which is 2.31 times the required value, and P = 105.628.

## Machinery (all record code imported read-only; nothing downloaded)

* **Flow of g on S^4.** On S^4 the unimodular EH equations hold for every radius, so the unimodular Hessian equals AS2's CPR f(R) Hessian with f -> f'R/2 and f'' -> 0, restricted to the traceless York modes TT and sigma, and with CPR's gauge term removed. xi is frozen by the TDiff gauge fixing (alpha_T -> 0, with transverse FP ghosts and Jacobians). Traces use AS2's `trace_R2` (Litim type I, the CPR regulator procedure, eta terms), plus AS2's type-I matter for the SM. The fixed point is g* = −2 pi/X1(e = 2).
* **Measure (axis A).** M-eq is graded: an extra det_S(D)^(+1/2), so that one-loop on-shell equivalence with GR holds (K5). M-naive (the local measure) is reported.
* **f_g on flat space.** AS1's `bilinear_action` and AS2/AS3's trace method, on traceless h (9 components) plus the photon: F-bar^2 coefficient, q^2 -> P_k, eta terms, angular average with a parity check. For alpha_T -> 0 the graviton space is TT + sigma (K7d confirms the limit).
* **Downstream.** Lane B's one-loop C5 chain, as in AS3 and CFG901.

**Graded trial G1** (one trial): M-eq, CPR sigma regulator, TT + sigma at alpha_T -> 0, P-lin vertices, g_Y* at M_P, one-loop downstream. The option space is measure 2 × sigma regulator 2 × modes/gauge 3 × parametrisation 2 × matching 3 = **K = 72**. **N_mech: 373 -> 374.** The route error **sigma_route = 6.230** is frozen and inherited from CFG901 (the record's scheme, truncation, matching, two-loop and Y1 spread). Kill rule: |z| > 3.

## Results (`cfg906_d04.out`, `cfg906_d04.json`; exit 0, all gates PASS)

**G1, graded: KILLED.**

* Fixed point: g* = 360 pi/1327 = 0.852278 (unique, admissible). X1(e) = −149e/720 − 167/24, so X1(2) = −1327/180. Critical exponent theta_g = 2.119. The eta pole sits at g = 15.2, outside (0, g*].
* f_g closed forms in f' = F1 and d_t f' = dF1, with the photon gauge xi symbolic and all of them xi-free:

| Field content | f_g |
|---|---|
| TT | −5(4F1 − dF1)/(1152 pi^2 F1^2) |
| sigma | +(4F1 − dF1)/(576 pi^2 F1^2) |
| TT + sigma (graded) | −(4F1 − dF1)/(384 pi^2 F1^2), = g/(12 pi) at the fixed point |
| alpha_T = 1 (TT + sigma + xi^T) | −(4F1 − dF1)/(192 pi^2 F1^2), = g/(6 pi) |

* **f_g* = 0.02260739,** which is 0.600 times the TT-only value and 2.306 times the required one. g_Y* = 0.722801 and theta_Y = −0.045215 (IR-attractive).
* **P = 105.62788,** a miss of −31.41 (−22.9%). **z = −5.041;** with the admissible-only error (3.245), z = −9.68.
* Systematics: two-loop 106.07890; M_red 103.87449.
* **The cross-check that uses no alpha agrees.** 41/(24 pi f_g) = 24.053 against Y1's 55.234 gives z_UV = −5.005, the same verdict.
* **Substitution test.** Scaling the downstream's measured alpha_2^-1(M_Z) and Delta_0 as if alpha were 1% larger shifts P by −0.383, against the −1.357 an identity would show: a fraction of 0.282, all of it from the measured downstream. The gravitational piece cannot move.

**The declared option space (rule D): KILLED across all 72 variants.** One-loop at M_P; the P-exp column is identical to P-lin in every row (expectation E3):

| Measure, sigma regulator | g* | TT + sigma (alpha_T -> 0) | TT only | alpha_T = 1 |
|---|---|---|---|---|
| **M-eq, CPR** | 0.852278 | **105.628 (z −5.04)** | 96.007 (−6.59) | 93.601 (−6.97) |
| M-eq, normalised | 0.845588 | 105.818 (−5.01) | 96.121 (−6.57) | 93.696 (−6.96) |
| M-naive, CPR | 0.871992 | 105.084 (−5.13) | 95.680 (−6.64) | 93.329 (−7.02) |
| M-naive, normalised | 0.864989 | 105.274 (−5.10) | 95.795 (−6.62) | 93.425 (−7.00) |

Shifts across all 72 variants: two-loop +0.45 to +0.51; M_red −1.75. The closest variant to 137 is M-eq/normalised/two-loop at 106.269 (z −4.94); the farthest is M-naive/CPR/alpha_T = 1/M_red at 91.576 (z −7.30). CONSISTENT would need f_g <= 0.01482, i.e. g* <= 0.559 with f_g = g/(12 pi).

## Gates and controls (all PASS in the real run)

* **PF.** sigma_route = 6.2303 and the admissible-only value 3.2452 equal the frozen numbers.
* **K0. AS3 reproduced** with AS2's code: (0.9671594, −1.222930), f_g 0.038830931, P 95.578469. Systematics: two-loop 96.075819, M_red 93.825087. The downstream G0 checks pass.
* **K1. The K-test (TT coincidence limit).**
  * The lane's TT-only code with the cosmological sqrt(g)^(2) term restored reproduces AS3's general formula −5(8F0 + 4F1 − dF1)/(1152 pi^2 (F0 + F1)^2) identically.
  * At K0's root it gives AS3's committed f_g = 0.038830931 and P = 95.578469.
  * Without the term (unimodular), the result is the same formula at F0 = 0, which is 5g/(36 pi) at the fixed point.
* **K2. Vertices.**
  * The re-implemented vertex builder reproduces AS1's V1 and V2 exactly.
  * Weyl invariance: g = (1 + h) det(1 + h)^(−1/4), with sqrt g = 1 and the determinant from sympy, gives AS1's vertices on traceless h to second order.
* **K3. The flat kinetic form.**
  * It annihilates the three TDiff pure-gauge modes and does not annihilate sigma.
  * Per unit norm: sigma = −Z_N s/8 and TT = +Z_N s/4, as the hand values say.
* **K4. The S^4 blocks.**
  * The on-shell xi action block is 0.
  * TT = −(f'/2)(D + R/6) = −(f'/2)(Delta_L − 2 Lambda), with Delta_L − D = 2R/3 computed from the S^4 Riemann tensor.
  * The sigma block = D^2 × (3/16) f'(D − R/3).
* **K5. One-loop on-shell equivalence** (eta = 0; bulk R^0, R^1, R^2).
  * AS2's complete GR CPR blocks (beta -> infinity, ghosts, third ghosts, Jacobians), taken on-shell, equal the physical form TT(D + R/6), VT(D − R/4) per field type; the scalar sector is 0.
  * Unimodular M-eq equals the same.
  * M-naive minus the physical form = (1/2) Tr_S[2/P] exactly.
  * Informational: 24 × the R^2 coefficient = 59/45, and the recalled Christensen–Duff −571/45 = 59/45 − 14 (the integer is the excluded modes; recalled, not gating).
* **K6. Hand closed forms of the R^1 coefficients**, all equal to the code's:
  * TT: −5/4 − 5e/18
  * sigma + J_S: 1/6 + 17e/240
  * normalised sigma: 1/6 + e/24
  * VT: −5/8
  * M-eq scalar: −1/6
  * matter: −61/12
* **FP-X.** AS2's own `beta_system` gives the same unique g*.
* **K7. Flat-space checks.** Parity holds; every f_g is independent of xi; f(TT + sigma) = f(TT) + f(sigma); and the alpha_T -> infinity limit of the 9-mode computation equals the TT + sigma restriction.
* **Classifier and positive controls.**
  * All 8 classifier cases come out as frozen.
  * **PC(i):** f_g = f_needed gives P = 137.035999177, graded CONSISTENT.
  * **PC(ii):** a planted X1 = −16.9987 gives g* = 0.3696, f_g = 0.009805 and P = 137.035999177, graded CONSISTENT.
* **MUTATE_SIGN** (matter traces × −1; `cfg906_d04_MUTATE_SIGN.out`): exit 1.
  * K0a and K6 (matter) FAIL as required. K0b and K1b fail as consequences: the mutated K0 root (0.2148, 0.3623) has f_g = −0.238.
  * L-SIGN PASSES: the mutated g* = −2.248456 = −2 pi/(X1_grav − X1_matter), as predicted (hand −2.25). There is no admissible fixed point, so there is no value.
* **MUTATE_SPLIT** (sigma kinetic sign flipped; `cfg906_d04_MUTATE_SPLIT.out`): exit 1.
  * K3b FAILS.
  * L-SPLIT PASSES: the mutated graded f_g equals f_TT − f_sigma exactly (7/5 f_TT), and P moves to 91.883 (hand 91.9).

## Hand expectations against results

Before computing, the pre-registration (section 10) wrote down:

* the R^1 forms and g* = 360 pi/1327;
* f_g^sigma/f_g^TT = −2/5 and f_g^xi(alpha_T = 1)/f_g^TT = +3/5, from mode sums in which both the loop and the tadpole give the same ratio;
* P-exp = P-lin, because the parametrisation term is linear in a traceless T^mn(F-bar), whose angular average vanishes;
* G1 ≈ 105.63 (z ≈ −5.04), TT-only ≈ 96.01, alpha_T = 1 ≈ 93.60, M-naive G1 ≈ 105.09 and normalised-sigma G1 ≈ 105.82;
* KILLED across the option space.

**Every one of these came out exactly as written** (E1–E3 and the variant table). The agreement is a consistency check between my pencil derivation and my code, not an independent re-derivation: both are mine.

## Run history and disclosures

* **Run 1** (`cfg906_d04_CRASH1.out`) crashed with a sympy immutable-matrix assignment in my f_g function. That happened after gates PF, K0, K2 and K3 had passed and before any unimodular f_g, g* or P had been computed. Fix: one `sp.Matrix(...)` copy, plus the same for the restricted kinetic matrix used by MUTATE_SPLIT. The home path in its traceback was replaced by `./` and `<site-packages>`; nothing else in that file was changed.
* **Run 2** (`cfg906_d04_RUN2.out` / `.json`, kept) completed with all gates passing and the graded verdict above. One display label, the exact form of one non-graded g* (M-eq, normalised sigma), printed a garbled `nsimplify` expression; its float was correct (144 pi/535 = 0.845588). The label was fixed (`simplify`).
* **MUTATE_SIGN, first attempt.** A print crashed on a None (the mutated root has f_g < 0) before L-SIGN ran. I guarded the print and reran MUTATE_SIGN.
* **The committed outputs all come from the final script.** The final normal run differs from run 2 only in that label line (diff checked), and MUTATE_SPLIT was rerun with identical output.
* **No criterion, gate, tolerance, option, sigma_route or grade was changed,** so there are no amendments to the frozen file.
* **The door's named gate could not be run.** A published unimodular fixed point (Eichhorn arXiv:1301.0879 / 1501.05848, recalled) is not in the repository, and nothing was downloaded. The unimodular gravity sector therefore has no external numerical anchor. K4 (S^4 on-shell structure, Lichnerowicz) and K5 (on-shell equivalence with AS2's independent GR blocks) are structural anchors only.
* **The graded measure M-eq rests on a recalled literature statement** (one-loop on-shell equivalence of unimodular gravity and GR: de León Ardón–Ohta–Percacci 2018; Kugo–Nakayama–Ohta 2022; not read). M-naive changes P by only −0.54.
* **f_g is off-shell.** The flat background with F-bar is not a solution, so f_g depends on the TDiff gauge. alpha_T -> 0 gives (3/5) f_g^TT and alpha_T = 1 gives (6/5) f_g^TT. Both are in the declared space, and both are KILLED.
* **Truncation convergence** (beyond unimodular EH) is untested, as for AS1–AS4.
* **The downstream contains measured alpha** (alpha_2^-1(M_Z) and Delta_0), as in AS1–AS4 and CFG901. The prediction of g_Y* uses none. The substitution fraction is 0.28, and the UV cross-check, which uses no alpha, gives the same verdict.
* **Precision ceiling.** A single coupling with no second prediction (theta_Y is not measurable) cannot exceed CONSISTENT (rules K9). No blind re-derivation was done.
* **Stop rule (rules §6).** This is the first KILLED result on D04. A second consecutive KILLED or NOT DIAGNOSTIC result on D04 closes the door unless a new forced element appears.
* **Compute.** One core at nice 10 (OMP_NUM_THREADS = 1) with a watchdog at 900 MB. Each run took about 18 s with a peak of 175 MB. No bytecode was written into the imported lanes, and none of their files was edited. Never say "theory closed".

## Attempt count and ledger rows

This is post-ledger alpha attempt **#3**, with one graded trial, so **N_mech goes from 373 to 374.** With this row the campaign ledger has 104 rows (CFG901's 103 plus this one; a parallel CFG907 row would add another) and 0 derivations.

Row for `ALPHA_ATTEMPTS_LEDGER.md` (reported to its owner; this lane edits no other lane's files):

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| CFG906 | FP | campaign_fresh_gravity/CFG906_alpha_D04_unimodular_as | Door D04: unimodular AS f_g (det g fixed, TDiff, no λ): S^4 flow from AS2 CPR blocks on-shell (f → f′R/2), TT + σ, M-eq measure; flat f_g with traceless h (AS1/AS3 method) | 105.628 graded (g* = 360π/1327 = 0.852, f_g = g/(12π) = 0.0226); variants 91.58–106.27 (TT-only 96.01, α_T = 1 93.60) | KILLED: z = −5.04 vs σ_route 6.230; TT part = AS3 at f = 0 (5g/36π) but σ is physical under TDiff and gives −2/5 of TT; 137 needs g* = 0.370 (TT-only 0.222), flow gives 0.852 (matter −5.08 of X1 = −7.37); all 72 declared variants KILLED | 1 | 29fb5fdc0 / (run commit of this lane) |

## Files

| File | Contents |
|---|---|
| `CFG906_PREREGISTRATION.md` | The frozen criteria (29fb5fdc0, committed alone before any script). |
| `cfg906_d04.py` | Gates, flow, f_g, the graded trial, the 72-variant table and the MUTATE modes. |
| `cfg906_d04.out`, `cfg906_d04.json` | The real run (exit 0). |
| `cfg906_d04_MUTATE_SIGN.out` / `.json`, `cfg906_d04_MUTATE_SPLIT.out` / `.json` | The controls (exit 1 each). |
| `cfg906_d04_RUN2.out` / `.json` | Run 2, identical except one display label. |
| `cfg906_d04_CRASH1.out` | Run 1, crashed before any unimodular number. |

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg906_d04.py [MUTATE_SIGN | MUTATE_SPLIT]`.
