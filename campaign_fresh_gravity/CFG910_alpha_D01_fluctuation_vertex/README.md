# CFG910: alpha door D01, f_g from the fluctuation photon–graviton vertex (scoped version, semi-fluctuation closure F1)

**Result: NOT DIAGNOSTIC.** In the graded closure the photon–graviton coupling g_3 has **no admissible fixed point**, so there is no graded value of 1/alpha(0). All gates pass. The frozen error recipe would have made the route non-diagnostic anyway: sigma_fl = 4260, so sigma_tot/P is far above 1. The fixed-point condition comes down to a small, regulator-induced remainder. Its sign depends on the gauge, and it is 6.3 times smaller than the charged-matter term that this scoped truncation does not compute. Nothing here derives alpha. Alpha stays an INPUT; kappa = 1/2 stays FITTED. **No graded value, so this is not counted as post-ledger attempt #5, and N_mech stays 375.** It still gets a ledger row. Rules and door: `../CFG895_alpha_campaign_ledger/` (door D01). Pre-registration: `CFG910_PREREGISTRATION.md` (frozen c849b27e4, committed alone before any script; no amendments).

**Wall note.** The SM mass sector is WALLED. No mass enters or is derived: the background fixed point depends only on field counts. kappa and the record's Z play no part. Nothing was downloaded. Literature is cited from memory, marked "recalled", and none of it serves as a gate.

## Scope: what was and was not done

The door asks for f_g from the fluctuation photon–graviton vertex at a fluctuation fixed point, and estimates 2–5 agent-days for it. This lane had one session. It therefore froze the simplest closed fluctuation truncation that sympy could carry through exactly, which is closure F1:

* **Fluctuation approach for the photon sector.**
  * The aah, aahh and aahhh vertices carry their own couplings g_3, g_4 and g_5.
  * The graviton propagator carries a mass parameter mu_h = −2 lambda_2 and an anomalous dimension eta_h.
  * The regulator and the gauge fixing are built from the flat background only.
  * g_3 is read off the zero-graviton-momentum aah vertex. The external graviton is a constant h_c and the external photons are a constant F-bar (AS1's method, extended). The vertex is projected onto the traceless A2 = h_ab F_ac F_bc structure, which is the only structure the tree vertex has, because Maxwell is Weyl invariant.
  * The flows are beta_g3 = g_3 [2 + eta_h + 2 Delta], with Delta = eta_A^grav − 2 c_B/tau_3, and f_g = −eta_A^grav/2.
* **Pure-gravity sector held at the record's background fixed point.** AS3 CPR-EH + SM gives (g*, lambda*) = (0.967159, −1.22293). This maps to mu_h = −2 lambda*, eta_h = −2, g_h3 = g* and lambda_3 = lambda*.
* **Not done (this is what remains for a full D01):**
  * mu_h, eta_h, g_h3 and lambda_3 from their own flows. That needs momentum-dependent graviton two- and three-point functions, with matter.
  * The charged-matter non-covariant remainder in beta_g3. It is only bracketed here, and it turns out to decide the result (see the results).
  * A symmetric-point projection of the vertex.
  * SM background fixed points in the LdD and FdD gauges.
  * The external gate the door names, a published fluctuation computation (recalled: Christiansen–Eichhorn arXiv:1702.07724; Eichhorn–Held–Wetterich arXiv:1711.02949; Eichhorn–Labus–Pawlowski–Reichert arXiv:1804.00012). None of these is in the repository and nothing was downloaded. The internal gates G-BF and G-COV stand in for it.

**Graded trial G1:** CPR gauge (rho = 0, Landau limit, kernel restriction), eta_h = −2, lambda_3 = lambda_2, g_4 = g_5 = g_3, one loop at M_P. The option space is gauge 3 × eta_h 2 × lambda_3 2 × photon identification 2 × matching 3, so **K = 72**. The route error is sigma_tot = sqrt(6.230² + sigma_fl²): 6.230 is CFG901's frozen sigma_route, and sigma_fl is the half-range of P over the 10 frozen CPR closure probes.

## Results (`cfg910_d01.out`, `cfg910_d01.json`; real run, exit 0, every required gate PASS)

**G1: NOT DIAGNOSTIC (no admissible root).**

* Per unit coupling at G1's point: Delta = a g_3 + b sqrt(g_3 g*), with **a = −0.01270318** and **b = −0.00274051**.
* With eta_h = −2 the canonical term cancels exactly, because 2 + eta_h = 0 at any background fixed point. The fixed-point condition is then just Delta = 0, so g_3* = g* (b/a)². That root needs −b/a > 0.
* Here a and b have the same sign, so Delta < 0 for every g_3 > 0 and there is no root.
* In this closure beta_g3 < 0 everywhere, so g_3 shrinks toward the UV (no interacting zero). Because of the matter bracket below, this is not a statement about the full theory.

Decomposition of Delta per unit coupling at G1's point (CPR; from `cfg910_landau_check.out`):

| Term | Coefficient |
|---|---|
| eta_A^grav = −4 c_0 | −0.08030 |
| [U2] aahhh tadpole | −0.08877 |
| [U1 V1] aahh × aah | +0.18649 |
| [V1 V1 W_A] h_c on the photon line | −0.03013 |
| [V2 W_h] h_c on the graviton line, tadpole | +0.04902 |
| [V1 V1 W_h] h_c on the graviton line, loop | −0.05176 |
| **a** (first four rows) | **−0.01270** |
| **b** (last two rows) | **−0.00274** |

* **Regulator-induced remainder.** On the background line g_3 = g*, Delta/g* = a + b = −0.01544. That is **19.2% of eta_A^grav per unit coupling**, against exactly 0 for a covariant regulator (G-COV). So with the fluctuation regulator, the background-field identification g_3 = g fails by tens of percent. This matches the door's recalled expectation of "effective universality to tens of percent".
* **Why the closure cannot decide.**
  * Both a and b are small residuals of terms ten times larger. b is a near-cancellation of +0.049 against −0.052.
  * The pre-registered bracket for the uncomputed charged-matter remainder is ±eta_A^matter = ±2 f_g. That is ±0.0803 per unit g_3, which is **6.3 × |a|**, so it can flip the sign of a.
  * With the +bracket the root appears at r = 0.0016 (P = 8601). With the −bracket there is no root.
  * The root's existence and location are therefore set by a term outside the scoped truncation.

**The frozen error recipe (reported).** sigma_fl = 4259.78. It is the half-range over the 7 of 10 probes that have an admissible root; 3 probes have none and are excluded and counted. That gives sigma_tot = 4259.79. Even if G1 had a root, delta_route = sigma_tot/P would be far above 1, which is NOT DIAGNOSTIC under rule 3.

CPR closure probes (one loop at M_P; two-loop and M_red in the .out):

| eta_h | lambda_3 | identification | matter | r = g_3*/g* | f_g | P |
|---|---|---|---|---|---|---|
| −2 | lambda* | U (graded G1) | 0 | none | – | – |
| −2 | lambda* | U' (g_4 = g_5 = g_h3) | 0 | 0.912 | 0.03287 | 98.12 |
| −2 | 0 | U | 0 | none | – | – |
| −2 | 0 | U' | 0 | 0.867 | 0.02980 | 99.82 |
| 0 | lambda* | U | 0 | 128.4 | 5.448 | 81.67 |
| 0 | lambda* | U' | 0 | 6.91 | 0.4211 | 82.87 |
| 0 | 0 | U | 0 | 134.2 | 5.694 | 81.67 |
| 0 | 0 | U' | 0 | 7.36 | 0.4499 | 82.78 |
| −2 | lambda* | U | +1 | 0.00164 | 6.4e-5 | 8601.23 |
| −2 | lambda* | U | −1 | none | – | – |

**Gauge variants** (reported, not graded, not in sigma_fl; they use the CPR fixed-point inputs, so they are gauge-inconsistent):

* **FdD:**
  * G1-type closure: r = 2.278, P = 84.99.
  * U': 88.19 (lambda_3 = lambda*) and 98.99 (lambda_3 = 0).
  * U with lambda_3 = 0: no root.
* **LdD:**
  * G1-type closure: no root (a = −0.0359, b = −0.0107).
  * U': 110.55 (lambda_3 = lambda*) and 144.08 (lambda_3 = 0).
* **eta_h = 0 rows:** 81.7–82.9 in both gauges.
* Across all reported variants with a root, P runs from 81.67 to 144.08, plus 8601 for the matter probe. This route in this truncation does not localise 1/alpha. Whether a root exists at all, and where, changes with the gauge and with the uncomputed couplings.

The class coefficients at lambda*, as exact polynomials in (lambda_3, eta_h), are printed per gauge in `cfg910_d01.out` and stored in `cfg910_d01.json` (`fl_classes`).

## Gates and controls (all PASS in the real run)

* **PF.** sigma_route = 6.2303 and the admissible-only value 3.2452 equal the frozen numbers.
* **G-REC.** AS3 is reproduced with AS2/AS3 code: (0.9671594, −1.222930), f_g 0.038830931, P 95.578469, two-loop 96.075819, M_red 93.825087. **G-DS:** lane B's downstream G0 checks pass.
* **G-VTX.** This lane's builder (EH + Lambda + FdD gauge fixing + photon, V1, V2) equals AS1's bilinear action exactly, with s, lambda, xi and F-bar all symbolic.
* **G-BF, the door's gate.** In the background-field limit g_3 = g_4 = g, mu_h = −2 lambda, eta_h = eta_N, the fluctuation two-point function reproduces the record's background f_g as **exact symbolic identities**:
  * CPR: 5 g (eta − 16 lambda + 4)/(72 pi (1 − 2 lambda)²), which is AS3's 5 g (1 − 8 lambda)/(36 pi (1 − 2 lambda)²) at eta = −2.
  * LdD: g (eta − 16 lambda + 4)/(16 pi (1 − 2 lambda)²).
  * FdD: g (eta − 16 lambda + 4)/(8 pi (1 − 2 lambda)²).
  * All three are xi-free.
  * New split of the CPR result: the loop [V1V1] gives 5 (16 − 16 lambda − eta)/(72 pi (1 − 2 lambda)²) per unit g_3, and the tadpole [V2] gives −5 (6 − eta)/(36 pi (1 − 2 lambda)²) per unit g_4. At G1's point these are +0.0699 and −0.0298.
* **G-EXP.** The f²·eps and f² coefficients of (1/2) Tr[(M0 + X)^-1 d_t R_k] from 60-digit finite differences agree with the expansion to 1e-22 (FdD and CPR).
* **G-COV.** With the regulator, both gauge fixings and the measure built on g_c = delta + h_c, the vertex flow gives **c_A = c_0/2 and c_B = −2 c_0 exactly**, as identities in (lambda, eta) at xi = 1 and xi = 2. So Delta ≡ 0 when every coupling is identified. This validates every h_c-dependent piece: the EH form on g_c, the photon block, U1, U2 and the invariant fit. The pre-registered fallback to rational points was not needed.
* **PC2.** The covariant-mode closure has the unique admissible root r = 1. One bookkeeping choice was made at scripting time and is not in the frozen text. In covariant mode, the h_c dependence of each block's regulator, gauge fixing and momentum normalisation carries that block's 3-point coupling, and the measure factor carries g_3 (the external-leg normalisation, like the tree vertex). Under this assignment the propagator coupling cancels, exactly as in fluctuation mode. PC2 is then equivalent to G-COV with a ≠ 0.
* **PC1.** Planting f_g = f_needed gives P = 137.035999177, graded CONSISTENT.
* **G-XI, G-FIT, G-PAR.** In all three gauges:
  * every class (c_0, c_A, c_B) is identical at xi = 1 and xi = 2;
  * the 7-invariant fit leaves zero residual on 2 extra configurations;
  * the reflected configuration gives an identical value;
  * all values are real.
* **MUTATE_VERTEX** (sign of W_A, the zero-graviton-momentum aah vertex, flipped; `cfg910_d01_MUTATE_VERTEX.out` / `.json`): **exit 1.**
  * G-COV FAILS at xi = 1 and 2, with c_B + 2 c_0 = (eta + 16 lambda − 16)/(24 pi (1 − 2 lambda)²), and PC2 fails.
  * All four G-BF checks PASS.
  * G1 moves to a = +0.04755, root r = 0.0033, P = 4297.7 (reported only).
* **MUTATE_GRAV** (W_h, the graviton-block h_c dependence, set to 0; `cfg910_d01_MUTATE_GRAV.out` / `.json`): **exit 1.**
  * G-COV FAILS, with c_B + 2 c_0 = −(eta − 6)/(6 pi (1 − 2 lambda)²), and PC2 fails.
  * All four G-BF checks PASS.
  * G1 gives b = 0 and no root.

## Post hoc verification (not pre-registered; `cfg910_landau_check.py`, `.out`, `.json`)

The verdict rests on the vertex classes in the Landau gauges, which use the kernel restriction. The pre-registered gates test the restriction only on the two-point function. So, after seeing the result, I recomputed the vertex classes with the full 10-component graviton and a finite gauge-fixing weight beta = 1e4, 1e5, 1e6, in exact arithmetic, and Richardson-extrapolated them to beta → infinity.

* For both CPR and LdD, every class reproduces the restricted value to ≤ 8.7e-10 relative to the class scale. The deviation at 1e4 is O(1e-5), consistent with a 1/beta approach.
* G1's (a, b) are reproduced to 8 digits.
* So the "no root" outcome is not an artefact of the restriction.

The script runs sections (0)–(2) of `cfg910_d01.py` verbatim (via exec of its source) and leaves that file unchanged. **First execution, kept as `cfg910_landau_check_FIRSTRUN.out` / `.json`:** it flagged LdD only because my deviation metric divided by each component, and the LdD [U1 V1] class has c_A = 0 exactly (extrapolated 2.3e-12). I changed that one metric line to divide by the class scale and reran. Every number line is identical between the two runs.

## Hand expectations against results

* **Correct:** the two-point gates (exact) and covariance (exact). The remainder came out at the level of tens of percent: 19% on the background line.
* **Wrong:** I expected a root with r between 0.5 and 2, P of about 88–105, and KILLED. Instead the graded closure has no root. I had flagged in advance that I had no hand value for the signs of a and b and that a NOT DIAGNOSTIC outcome was possible.
* **Not foreseen:** that eta_h = −2 makes the fixed-point condition purely a ratio of non-covariant residuals, and that the uncomputed charged-matter bracket would be 6.3 times the decisive coefficient.

## Run history and disclosures

* **Development runs** (in a scratch directory, not committed) executed sections (0)–(4) and then (0)–(6): PF, G-REC, G-VTX, G-BF, G-EXP, G-COV and PC2. All passed on their first execution. Those sections compute no fluctuation-mode quantity at the graded point. Sections (7)–(9), which hold the graded computation, ran for the first time in the committed real run, unchanged.
* **Code edits before the real run:** an mpmath conversion helper, the order of PC1 relative to the gate tally, reporting G1's root in every mode, and bool serialisation in the JSON. None changes a criterion, gate, tolerance, option or grade. No amendments were made to the frozen file.
* **PC2's coupling bookkeeping** in covariant mode was chosen at scripting time (see above). It is a control, not graded.
* **The downstream uses measured alpha** (alpha_2^-1(M_Z) and Delta_0), as in AS1–AS4, CFG901 and CFG906. With no graded value, the substitution test and the UV cross-check were not evaluated.
* **The external gate was not run** (no downloads). The gravity-sector fluctuation couplings are not resolved (closure F1).
* **Stop rule (rules §6).** This is the **first** NOT DIAGNOSTIC result on D01. A second consecutive KILLED or NOT DIAGNOSTIC on D01 closes the door unless a new forced element appears.
* **Compute.** One core at nice 10 (OMP_NUM_THREADS = 1), with a watchdog at 900 MB.

  | Run | Time | Peak memory |
  |---|---|---|
  | Real run | 253 s | 190 MB |
  | MUTATE_VERTEX / MUTATE_GRAV | 247 s / 188 s | 190 MB / 187 MB |
  | Landau check | 204 s | 172 MB |

  No bytecode was written into the imported lanes, and none of their files was edited.
* Never say "theory closed".

## Attempt count and ledger rows

There is **no graded value**, so N_mech stays **375**. This is not counted as post-ledger attempt #5; that number stays free for the next value-producing attempt. Ledger rows (reported to their owners; this lane edits no other lane's files):

`ALPHA_ATTEMPTS_LEDGER.md`:

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| CFG910 | FP | campaign_fresh_gravity/CFG910_alpha_D01_fluctuation_vertex | Door D01 (scoped): AS f_g with the photon sector in the fluctuation approach (own aah coupling g_3 from the zero-graviton-momentum vertex, delta regulator; f_g = −η_A^grav/2 with g_3, g_4, μ_h, η_h), gravity sector held at AS3's CPR-EH + SM background point (closure F1); CPR gauge graded | none graded (G1 has no root); reported variants 81.67–144.08 (+8601 for the matter probe) | NOT DIAGNOSTIC: G1 has no admissible g_3 fixed point (Δ = a g_3 + b√(g_3 g*), a −0.0127, b −0.0027, same sign); the remainder is 19% of η_A^grav and its sign depends on the gauge (FdD root r 2.28); the uncomputed charged-matter bracket is 6.3 × \|a\|; frozen σ_fl = 4260. G-BF (AS1/AS3 background f_g as g_3 → g, 3 gauges) and G-COV (Δ ≡ 0 for a covariant regulator) are exact; MUTATE_VERTEX/GRAV exit 1 | 0 (N_mech stays 375) | c849b27e4 / (run commit of this lane) |

`campaign_fresh_gravity/LEDGER.md`:

| CFG910 | (block 910–919; criteria c849b27e4, no amendments; agent lane; α door D01, scoped; no graded value, so not post-ledger attempt #5) f_g from the fluctuation photon–graviton vertex in a semi-fluctuation closure F1. The photon sector is in the fluctuation approach: own aah coupling g_3 read off the zero-graviton-momentum vertex (constant h_c + constant F-bar, traceless A2 projection), delta regulator and gauge fixing, β_g3 = g_3[2 + η_h + 2Δ]. The gravity sector is held at AS3's CPR-EH + SM point (μ_h = −2λ*, η_h = −2). **NOT DIAGNOSTIC**: graded G1 (CPR, η_h = −2, λ_3 = λ*, g_4 = g_5 = g_3) has no admissible root, because Δ = a g_3 + b√(g_3 g*) with a −0.0127 and b −0.0027 of the same sign (at η_h = −2 the canonical term cancels, so the fixed point is a ratio of non-covariant residuals). The remainder on the background line is 19% of η_A^grav. The uncomputed charged-matter bracket ±2f_g is 6.3 × \|a\| (+ gives r 0.0016, P 8601); frozen σ_fl = 4260. Gauge-inconsistent variants: FdD root r 2.28 (P 85.0), LdD none; U' 88–144; η_h = 0 81.7–82.9. Gates exact: G-BF (door's gate: AS1/AS3 background f_g reproduced as g_3 → g in CPR/LdD/FdD; CPR split loop 5(16−16λ−η)/(72π(1−2λ)²), tadpole −5(6−η)/(36π(1−2λ)²)), G-COV (covariant regulator gives c_B = −2c_0, Δ ≡ 0), G-EXP 1e-22, G-XI/FIT/PAR; the post-hoc Landau check (finite β → ∞) reproduces the kernel restriction to 9e-10. MUTATE_VERTEX/GRAV exit 1 (G-BF still passes). Remaining for a full D01: μ_h, η_h, g_h3 from their own flows, the charged-matter remainder, a symmetric-point projection, and the external gate (no downloads). First NOT DIAGNOSTIC on D01. N_mech stays 375. α stays an input. | (run commit) |

## Files

| File | Contents |
|---|---|
| `CFG910_PREREGISTRATION.md` | Frozen criteria (c849b27e4, committed alone before any script). |
| `cfg910_d01.py` | Gates, the fluctuation-mode and covariant-mode vertex machinery, closures, grading and the MUTATE modes. |
| `cfg910_d01.out`, `cfg910_d01.json` | Real run (exit 0). |
| `cfg910_d01_MUTATE_VERTEX.out` / `.json`, `cfg910_d01_MUTATE_GRAV.out` / `.json` | The controls (exit 1 each). |
| `cfg910_landau_check.py`, `.out`, `.json` | Post hoc Landau-limit verification (exit 0). |
| `cfg910_landau_check_FIRSTRUN.out` / `.json` | Its first execution (metric artefact; identical numbers). |

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg910_d01.py [MUTATE_VERTEX | MUTATE_GRAV]`; `OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg910_landau_check.py`.
