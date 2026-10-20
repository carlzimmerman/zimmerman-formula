# CFG901: alpha door D03, f_g with the record's own matter content

**Result: KILLED.** With the record's own content, SM + 3 right-handed neutrinos (N_S 4, N_D 24, N_V 12), the asymptotic-safety route gives 1/alpha(0) = **96.504** in the graded scheme (CPR, Einstein–Hilbert truncation). That is 40.5 below 137.036, **z = −6.51** in units of the route's own frozen error (6.230), so the grade is KILLED. The three neutrinos move the prediction by only **+0.93** from the SM value 95.578; the other schemes move by +0.90 and +0.38. The content loophole is closed at every computed truncation. The canonical theory's dark sector posits no elementary relativistic field, so the second content set the door allowed does not exist and was not a trial. Nothing here derives alpha. Alpha stays an INPUT; kappa = 1/2 stays FITTED. This is attempt #2 of the post-ledger alpha campaign (rules and door: `../CFG895_alpha_campaign_ledger/`; attempt #1 is CFG896).

**Wall note.** The SM mass sector is WALLED. No mass enters this lane: the gravitational fixed point depends only on field counts. kappa and the record's Z play no part.

## What was tested

Asymptotic safety adds −f_g g_Y to the hypercharge beta function. If f_g > 0, the hypercharge coupling at the Planck scale is fixed at the IR-attractive zero g_Y* = 4π sqrt(6 f_g/41) (kernel class K1, conditional on the AS scenario). f_g is set by the gravitational fixed point (g*, λ*), and that fixed point depends on the matter content. AS1–AS4 used SM content only. Door D03 re-evaluates the route with the content the record itself fixes:

* **Content A (graded): SM + 3 ν_R.** The three ν_R come from FS11, the conditional door "SM on a circle + the non-SUSY AdS swampland conjecture", under which neutrinos must be Dirac. A Weyl fermion's trace is half a Dirac fermion's, so N_D = 45/2 + 3/2 = 24. ν_R has hypercharge 0, so b_Y = 41/6 and the running below M_P are unchanged. The content therefore enters only through f_g.
* **Content B (the canonical dark fields): not defined by the record, so not a trial.** The canonical S2 action (`THEORY_CANONICAL_2026-10-14.md`, unchanged in field content through v3) is non-relativistic. Φ in it is the Newtonian potential and P is the displacement of a collisionless medium. The relativistic completion is listed as not done, and the record has a rule of no DM particle. So there is no elementary field with a spin and a kinetic term to count. A bracket B1–B4 is reported as sensitivity only.

**Machinery.** All of it is imported read-only:

* AS3's CPR f(R) code (EH and EH + R²) and AS4's BMS code (EH and EH + C² + R²), with type-I matter and the Litim cutoff;
* lane B's EV betas, flagged as not rebuildable (AS1);
* lane B's one-loop downstream P = 41/(24π f_g) + (41/12π) ln(M_P/M_Z) + α_2⁻¹(M_Z) + 9.106.

f_g comes from the closed forms in the AS3/AS4 reports. Those formulas contain no matter terms, so content enters only through the fixed point. In the EH truncation the matter traces are N_S(1/2 + R/6) + N_D(−2 − R/6) + N_V(1 − R/6) in both schemes; K6 checks this against a hand derivation.

**Graded trial G1** (one trial): content A, CPR-EH, g_Y* imposed at M_P, the one-loop downstream. The option space is 5 schemes/truncations × 3 matching/running choices = **K = 15**, with one trial graded. **N_mech: 372 → 373.**

**Route error.** σ_route = 6.230 was frozen before computing, from the record's own SM-content numbers, added in quadrature:

| Component | Value | Source |
|---|---|---|
| scheme | 2.664 | EV vs CPR |
| truncation | 5.327 | BMS HD in-domain root vs BMS EH; the root is inadmissible, so this is conservative |
| matching at M_red | 1.753 | |
| two-loop | 0.497 | |
| Y1 running | 0.121 | |

* Kill rule: |z| > 3 means KILLED.
* δ_route = 0.0455 < 1, so the route is diagnostic by rules §1.6. It cannot reach 1%, so its ceiling is CONSISTENT.

## Results (`cfg901_d03.out`, `cfg901_d03.json`; amended run, exit 0, all gates PASS)

**G1, graded: KILLED.**

* Fixed point: one unique admissible CPR-EH root, (g*, λ*) = (0.934943, −1.295585), with critical exponents 1.9008 and 3.9072.
* f_g* = 0.03642403, which is 3.715 times the 0.009805 needed for 137.
* Hypercharge fixed point: g_Y* = 0.917461, IR-attractive (θ_Y = −0.0728).
* **P = 96.50384**, so the miss is −40.53 (−29.6%).
* **z = −6.506.** With the admissible-only error (3.245) it is −12.49.
* Systematics: two-loop 96.995; matching at M_red 94.750.
* **The cross-check that uses no α agrees.** 1/α_Y*(M_P) = 41/(24π f_g) = 14.93, against Y1's target 55.234, gives z_UV = −6.47, the same verdict.
* **Substitution test.** Scaling the downstream's measured α_2⁻¹(M_Z) and Δ_0 as if α were 1% larger moves P by −0.383. An identity would move it by −1.357, so the fraction is 0.28. That shift comes entirely from the measured downstream terms; the gravitational piece cannot move.

**Content shift and the diagnostic map** (door's first computation, not graded). Derivatives of P at SM content, from the implicit-function theorem:

| Scheme | dP/dN_S | dP/dN_D | dP/dN_V |
|---|---|---|---|
| CPR-EH | −0.291 | +0.614 | −0.032 |
| BMS-EH | −0.294 | +0.596 | −0.008 |
| EV-EH | −0.279 | +0.251 | +0.307 |

Fermions push λ* more negative and g* down. That lowers f_g and raises P; the sign was expected, but the size is about 0.6 per Dirac fermion. The content shift P_A − P_SM:

| Scheme | Direct | Linear map |
|---|---|---|
| CPR-EH | +0.925 | +0.922 |
| BMS-EH | +0.900 | +0.893 |
| EV-EH | +0.382 | +0.377 |

Every shift is far below σ_route, so **the content loophole is closed at the computed truncations.**

**Reported, not graded** (content A):

| Scheme / truncation | Roots | Selection | P |
|---|---|---|---|
| CPR-R² | 4 real, 2 admissible | NOT DIAGNOSTIC | 96.243 and 96.655 (each would be KILLED, z ≈ −6.5) |
| BMS-EH | unique | value | 97.272 (z −6.38) |
| BMS-EH + C² + R² | 3 real, none admissible | NOT DIAGNOSTIC (no admissible root) | in-domain root 91.711; its spin-0 denominator is −0.076 |
| EV-EH | | value | 93.296 (z −7.02) |

**Bracket for content B** (not defined; sensitivity only). Shifts relative to content A, CPR-EH:

| Variant | Shift |
|---|---|
| +1 real scalar | −0.29 |
| +2 real scalars | −0.58 |
| +1 gauge vector | −0.04 |
| +1 vector + 1 scalar (Proca) | −0.33 |

BMS behaves the same way. Scalars move P away from 137, and no dark-field reading moves it by more than 0.6.

**Tuned content.** These are counts at which CPR-EH would reach 137 if content were a free knob. They are by construction, not predictions, and not admissible under X1's zero-knob rule.

* **N_D\* = 87.76**, i.e. +65.3 Dirac or +130.5 Weyl fermions.
* **N_V\* = 45.05**, i.e. +33 vectors. It gets there only because λ* climbs to +0.0745, toward the zero of f_g at λ = 1/8. This is CFG895's "λ* = 0.107" branch.
* **N_S: never.** g* runs away and leaves the AS2 domain (g < 50) near N_S ≈ 39.6, while f_g rises from 0.039 to 0.14, away from the target.

## Gates and controls (amended run: all PASS)

* **K1. AS3 reproduced with its own content.**
  * CPR-EH: (0.9671594, −1.222930), f_g 0.038830931, P 95.578469.
  * Systematics: two-loop 96.075819, M_red 93.825087.
  * CPR-R²: 4 roots, 2 admissible, both matching AS3's printed roots, f_g and P.
* **K2. AS4 reproduced with its own content.**
  * BMS-EH: (0.8647728, −1.090055), f_g 0.036746945, P 96.372649.
  * Systematics: 96.864957 and 94.619266.
  * BMS-HD: 3 roots, 0 admissible; the in-domain root gives P 91.045266, and root 3 gives 83.505781.
* **K3.** Lane B's EV result: f_g 0.0479549692 and c5 92.914075, identical to lane B.
* **K4.** The downstream G0 checks pass.
* **K5.** sympy confirms the f_g closed forms: CPR general = 5g(1 − 8λ)/(36π(1 − 2λ)²), and BMS at u3 = 0 equals CPR.
* **K6.** The per-field matter traces equal the hand values in both schemes, and the SM totals equal AS3's and AS4's printed totals exactly.
* **K7. Published anchors of the content dependence.**
  * CPR pure gravity: g~0* = 0.0052261, θ = 2.3824 ± 2.1682 i.
  * BMS pure gravity: (0.90160, 0.10926).
  * **BMS with one scalar (published n_s = 1 row): (0.86006, 0.13077), θ = 2.5808 ± 1.9544 i.**
* **K8.**
  * The implicit-function derivatives agree with Richardson finite differences to ≤ 2e-8; the raw error ratio is 4.00, the O(h²) signature.
  * Continuation from SM to content A lands on the grid root.
* **Classifier and planted controls.** All 10 classifier cases come out as frozen. The planted f_g = f_needed gives P = 137.035999177 and is graded CONSISTENT.
* **L1/L2: the prediction moves as expected.**
  * L1: the SM + 3 Dirac shift divided by the content-A shift is +1.857/+0.925 = 2.007.
  * L2: the SM − 3 Weyl shift divided by the content-A shift is −0.917/+0.925 = −0.991.
* **MUTATE_SIGN** (all matter traces × −1; `cfg901_d03_MUTATE_SIGN.out`): exit 1.
  * K1a, K1c, K2a, K3, K6 and K7c (the n_s = 1 anchor) FAIL, and K8/L1/L2 fail as a consequence.
  * The pure-gravity anchors K7a and K7b still PASS, so the control is targeted.
  * The graded root moves to λ* = +0.367 with f_g = −0.243. There is no IR-attractive g_Y*, so no value.
* **MUTATE_COUNT** (the 3 Weyl ν_R counted as Dirac; `cfg901_d03_MUTATE_COUNT.out`): exit 1.
  * C-DEF FAILS.
  * The prediction moves to 97.435. That is a shift of +1.857, 2.007 times the correct shift, as expected. L1/L2 PASS.
* **MUTATE runs skip the BMS-HD grid,** as pre-registered.

## The first run and the amendments

The first run (`cfg901_d03_FIRSTRUN.out` / `.json`, committed unchanged with the first-run script in ced3bd06b) failed K8a, K8b and L1/L2. **As frozen, its verdict is NOT COMPLETED.** Amendments A1–A4 were written after I had seen every first-run number, including the would-be graded value (disclosed in the amendment text). They are post hoc:

* **A1.** My continuation helper demanded fsolve's flag 1. Flag 3 ("xtol too small") at a residual of 1e-17 is converged, so the helper now accepts by residual. The imported AS2/AS4 grid searches that produce the graded root are unchanged.
* **A2.** K8a's 1e-3 relative tolerance failed only for the near-zero derivatives dP/dN_V, a genuine O(h²) finite-difference error (FD → IFT, falling 4× per halving). It is replaced by a Richardson check.
* **A3.** A step guard was added to the tuned-content scan.
* **A4.** Bookkeeping.

No content, scheme, root search, f_g formula, downstream, σ_route, threshold or grade changed. The amended run reproduces the first run's graded numbers digit for digit.

## Disclosures

* **Hand estimates against results.** Before computing I wrote:
  * ΔP ≈ +1 (range 0 to +2, same sign in every scheme). Result: +0.93, +0.90, +0.38. Correct.
  * P_A ≈ 96–97.5 and |z| ≈ 6–7. Result: 96.50 and 6.51. Correct.
  * Bracket shifts < 2. Result: at most 0.59. Correct.
  * Tuned content of "tens to about a hundred" Dirac fermions. Result: +65. Correct.
  * I had not foreseen the N_V route via λ* → 1/8, or the N_S runaway.
* **Feasibility timing before freezing.** I ran the AS3/AS4 code on SM content only, reproducing committed numbers, and it printed the general symbolic matter traces. No content-A number was computed before the freeze.
* **The downstream contains measured α.** It uses α_2⁻¹(M_Z) = α⁻¹(M_Z) sin²θ_W and the measured offset Δ_0, as in AS1–AS4. The prediction of g_Y* uses no α. The substitution fraction is 0.28, all from the downstream. The UV cross-check, which has no α at all, gives the same verdict.
* **Conditional content.** FS11, and hence the 3 ν_R, rests on an unproven conjecture. FS11's scripts are not tracked in this repository. The result is conditional, but it hardly matters: SM-only gives 95.58 and SM + 3 ν_R gives 96.50.
* **AS4's admissibility rule** used for BMS-HD also rejects the published BMS pure-gravity fixed point (rules §0.3, restated).
* **Scope of KILLED.** It holds at the computed truncations, with the record's own spread as the error. Convergence of the truncation is untested in the record, as for AS3/AS4. Even the conservative σ_route, which includes the inadmissible BMS root, leaves |z| = 6.5.
* **Precision ceiling.** A single coupling with no second prediction (θ_Y is not measurable) cannot exceed CONSISTENT (rules K9). No blind second-agent re-derivation was done; it is only needed for EVIDENCE.
* **Stop rule (rules §6).** This is the first KILLED result on D03. A second consecutive KILLED or NOT DIAGNOSTIC on D03 closes the door unless a new forced element appears. The door's two content sets are exhausted: A is graded and B is undefined.
* **Compute.** One core at nice 10, peak 208 MB, a watchdog at 900 MB. Run times: real run 137 s, MUTATE_SIGN 41 s, MUTATE_COUNT 38 s. No bytecode was written into the imported lanes, and none of their files was edited. Never say "theory closed".

## Attempt count and ledger rows

This is post-ledger alpha attempt **#2**, with one graded trial, so **N_mech goes from 372 to 373.** The campaign now has 103 ledger rows and 0 derivations.

Row for `ALPHA_ATTEMPTS_LEDGER.md` (reported to its owner; this lane edits no other lane's files):

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| CFG901 | FP | campaign_fresh_gravity/CFG901_alpha_D03_own_content_fg | Door D03: AS f_g (background field) with the record's own content SM + 3 ν_R (FS11; N_D 24), CPR-EH graded (AS3 code), CPR-R², BMS-EH/HD, EV reported; canonical dark fields not elementary, so set B undefined | 96.504 (CPR-EH graded); reported 96.24/96.65 (CPR-R², two roots), 97.27 (BMS-EH), 93.30 (EV); ν_R shift +0.93/+0.90/+0.38 | KILLED: z = −6.51 against the frozen σ_route 6.230 (scheme + truncation + matching + two-loop + Y1); f_g = 3.7× the required; content loophole closed (shift ≪ σ); tuned content needs +65 Dirac or +33 vectors (knobs). As frozen, the first run was NOT COMPLETED (K8a FD tolerance, solver flag; amendments A1–A4 post hoc, graded numbers identical) | 1 | f1e4cb90d / ced3bd06b / the run commit of this lane |

## Files

| File | Contents |
|---|---|
| `CFG901_PREREGISTRATION.md` | The frozen criteria (f1e4cb90d, committed alone before any script), plus post-hoc amendments A1–A4 (ced3bd06b). |
| `cfg901_d03.py` | Gates, pre-flight map, graded trial, reported trials, bracket, tuned content, and the MUTATE modes. |
| `cfg901_d03.out`, `cfg901_d03.json` | The amended real run (exit 0). |
| `cfg901_d03_MUTATE_SIGN.out` / `.json`, `cfg901_d03_MUTATE_COUNT.out` / `.json` | The controls (exit 1 each). |
| `cfg901_d03_FIRSTRUN.out` / `.json` | The first run under the frozen gates (exit 1), kept unchanged. |

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg901_d03.py [MUTATE_SIGN | MUTATE_COUNT]`.
