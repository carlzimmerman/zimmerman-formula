# Rules for new attempts on the fine-structure constant (CFG895)

These rules apply to every new attempt to derive alpha (1/alpha(0) = 137.035999177(21), CODATA 2022). Alpha is the constant most prone to numerology in physics. The record already holds at least 359 graded trials at the level of mechanisms and 78.6 million rule-search trials, and none of them produced alpha (see `ALPHA_ATTEMPTS_LEDGER.md`). The rules have one aim: if a new attempt ever does produce 137.036, it should be believable. They extend the record's existing bar (`real_research/alpha_principle_2026/D_calibration_bar/alpha_bar_checker.py`) and the exactness harness (`V1_exactness_harness/v1_exactness_harness.py`); they do not replace either. The numbers quoted below come from `cfg895_check.py` (output in `cfg895_check.out`, values in `cfg895_check.json`).

## 0. Record rules (restated; they bind every lane)

1. **The Standard-Model bridge is WALLED.** Do not reopen it without a NEW FORCED KERNEL: a mechanism in which a consistency condition forces alpha, so that nobody chooses it (definition in section 2). The SM mass sector is also walled. Measured masses and couplings other than alpha may be used as labelled inputs; they may not be derived or tuned.
2. **Schwinger/Unruh is a NO-GO.** The route through horizon pair production and induced current (AH1–AH4, with N5, Q1, Q2, S1, S2) is a no-go in dS₂ and dS₄. Every horizon response so far has the form alpha × G(m/H), and the mass function is free (Lean AH3; AH7 covers the dimensional obstruction).
3. **Asymptotic safety gives 1/alpha of 91–96, not 137.** Lanes AS1–AS4 found 1/alpha(0) = 91–96 (89–97 with systematics); 137 needs f_g about 4× smaller than every computed value. Disclosed: the frozen admissibility rule in AS4 also rejects the published pure-gravity fixed point (BMS 0902.4630). Any lane that reuses that rule must restate this.
4. **kappa and Z play no part in alpha.** A rule, formula or kernel that contains kappa, Z, 32π/3, or another framework-fitted number is rejected outright (A1/A2 searched 36.0M such rules and project_atomos 42.5M values; zero hits).
5. **The Koide doors are closed** (Lean, 10-08). Do not re-run them.
6. **Never manufacture a derivation.** A fail is verified as hard as a win.
7. **Check identities by construction.** Before claiming that two quantities agree, check whether one of them was built from the other (section 4).
8. **Hygiene.** Claims are committed scripts. Margins come from JSON. Each lane commits only its own paths and never rewrites history. While a 1024³ run is live, nothing heavy runs: light single-core scripts only, and no repo-wide greps over data files.

## 1. Before computing: the pre-registration, committed and hashed

Commit a `*_PREREGISTRATION.md` before any graded computation, and quote its commit hash in the run commit. It must state everything below.

1. **The mechanism**, in one paragraph: what physical process fixes the coupling.
2. **The forced-kernel candidate.** This is the equation C(alpha, data) = 0 that forces the value. Name its class (section 2) and say why its solution set in alpha is discrete.
3. **Which alpha.** Give the scale and the scheme, from:
   * alpha(0), the Thomson limit, 1/137.035999177;
   * alpha(M_Z), either MS-bar (1/alpha ≈ 127.95) or on-shell including Δalpha_lep+had (≈ 128.9). Both are recalled approximations and must be cited if used;
   * alpha_Y and alpha_2 at a declared UV scale. Y1's central values at M_P (1.22089e19 GeV) are 1/alpha_Y = 55.234, 1/alpha_2 = 49.203 and 1/alpha_em = 104.437.

   A route that predicts a UV value must run it down to alpha(0) with the record's validated machinery (`Y1_running_precision/`) and carry Y1's error budget, which is σ(1/alpha_em)/137.036 = 8.8e-4 from the running alone. Comparing a UV value with 137.036 without running it down is a category error, and the comparison is void.
4. **The inputs.** Label each input as measured, derived or a declared convention.
   * **Forbidden inputs:**
     * alpha measured at any scale;
     * any proxy for alpha: R_K, Z_0, μ_0 (in the 2019 SI, μ_0 = 2 alpha h/(c e²)), R∞ together with m_e, the Bohr radius, the Thomson cross-section, the classical electron radius, an alpha extracted from g−2, an on-shell sin²θ_W built together with G_F and M_W, or any quantity whose definition contains alpha at O(1);
     * real numbers fitted to alpha;
     * kappa and Z.
   * **Allowed inputs:** measured masses, alpha_s, G_F, M_W, m_H and m_t, labelled, with their uncertainties carried through.
   * **Contamination test:** list every place where a measured alpha could hide (lattice scale setting, Δalpha_had, electromagnetic shifts in masses, CODATA-derived constants). Section 4.3 is the test.
5. **The option space**, which sets the trials factor. Enumerate every discrete choice the route could have made: truncations, gauges, regulators, schemes, scales, normalisations, matter-content sets, identification rules, and which conditions get combined. The count is K. Where it is cheap, list the values the route would give for each choice. Choose the graded trial or trials before computing; one graded trial per lane is preferred, as in AS1–AS4. Any other choice is reported but not graded.
6. **A leverage and precision pre-flight**, written before the hard computation.
   * Compute the leverage L = d ln(selection observable)/d ln alpha and propagate every input uncertainty into σ(1/alpha). This gives δ_route, the best precision the route could reach even if all of its physics is correct.
   * If δ_route > 1 (the route cannot fix alpha to within a factor of e), the route is NON-DIAGNOSTIC by construction. Record it and stop.
   * Worked example (`cfg895_check.py` B2): the FSP selection equation R(alpha) = c_H/C_p³ = H̄/(K G m_p³). Alpha enters only through first-order electromagnetic corrections, p_alpha ≈ (4.9–5.8)e-4. Even with a generous |S| ≤ 10 p_alpha, the H0 bracket gives σ(ln alpha) ≥ 11, and knowing the cosmological side to 1% still gives 1.7. Inferring alpha to 1% needs the cosmological side and the QCD ratio to 5.8e-5.
   * Worked example (B1): on the asymptotic-safety route d(1/alpha(0))/d ln f_g = −55.2 at the required f_g, so 1% in alpha needs f_g to 2.5%. The spread across the published schemes is about 25%.
7. **Gates.** Reproduce a published or independent result with the same machinery before the graded run. The gate must be anchored on numbers that are consistent with each other. This is the AS1 lesson: that lane's design error was gating on equations that cannot be rebuilt from a published scheme.
8. **Kill criteria and the expected outcome**, both written down beforehand. A wrong expectation is disclosed, not hidden.
9. **Mutation and positive controls.** Name the load-bearing element that the MUTATE control alters: a sign, a group factor, a factor of 2, or a coupling identification. Say how the control must fail (exit 1). Plant a known answer as the positive control.

## 2. What a forced kernel is (kernel classes)

| Class | Meaning | Examples | Best grade it can reach |
|---|---|---|---|
| **K1. Forced by consistency** | Alpha solves a condition imposed by UV completeness, IR attractivity, anomaly freedom or unitarity. The other data are measured or derived. | Hypercharge at an IR-attractive interacting fixed point of quantum gravity (lane B, AS1–AS4); a coupling forced by anomaly inflow | DERIVATION |
| **K2. A postulated selection principle** | Alpha follows from a principle that is posited, not forced: criticality or the multiple point principle, naturalness (the Veltman condition), entropy maximisation, the Coleman big fix | B1–B4 (gauge MPP); I3 (Hartle–Hawking extremum) | EVIDENCE for the principle, and only if it also makes a second, independent prediction that checks out. Never DERIVATION on its own. |
| **K3. A saturated bound** | An inequality (WGC, positivity, Festina Lente, unitarity) taken at equality | Lanes A, C, Q5 | Admissible only if something forces the saturation; otherwise it is a choice (K0) |
| **K0. A chosen boundary condition** | Any value, scale, count or coefficient picked by hand | Lanes N4 and U3 | Not a kernel. Grade NUMEROLOGY or NOT DIAGNOSTIC. |

A route that moves the freedom into a modulus, a dimensionful scale or cutoff ratio, the charged spectrum or a gauge kinetic function has not forced anything. That is the record's common finding across about 40 lanes.

## 3. The running attempt count and look-elsewhere

* **Every attempt gets a ledger row**, including NOT COMPLETED and KILLED. A lane appends its row to `ALPHA_ATTEMPTS_LEDGER.md` through its own lane commit, or reports it to the owner of this ledger.
* **N_mech** is the number of graded value trials at the level of mechanisms: numerical outputs for a coupling compared against a target. From the record it is at least 359 (`cfg895_check.py` A, itemised in the ledger's Trials column). **N_rule** counts rule-search trials: 78,586,900 (A1 5,488,000 + A2 30,530,688 + project_atomos 42,534,139 distinct values + the legacy 34,073-formula space). The numerical-search budget is spent: A1+A2 reach a cumulative P_chance of about 1.5%, and A2 alone is not powered. **No further formula or rule search can be significant.** Only a mechanism can.
* **Each new graded trial adds 1 to N_mech.** A lane with K pre-declared graded variants adds K.
* **Campaign-wide look-elsewhere.** A claim of EVIDENCE requires P_family = 1 − (1 − P_single)^(N_mech) < 1e-3, which is approximately N_mech × P_single < 1e-3. The counts include the record's trials.

## 4. What counts as a hit (all of these are required)

1. **It survives the mutation control.** The hit must disappear when the load-bearing element is altered, and the positive control must pass. A control that cannot fail is a broken lane. In the record, T1 and V1 signal a broken control with exit 3, and A1's first control was broken (A1 pre-registration, Amendment 1).
2. **It is not an identity by construction.** Three checks:
   * *Substitution test:* scale every place a measured alpha could enter by 1.01. If the "prediction" moves by the same 1%, it is an identity or contaminated.
   * *Residual test (the AH8 lesson):* a closed form plus correction terms is not a prediction when the corrections are the leftover rewritten as a series in alpha. Report the bare form's own precision. For 4Z²+3 that precision is 3.9e-5, not 1.8e-8.
   * *Shape test (T2):* a claimed "loop correction" must have coefficients in the class that real QED produces. The first order is rational/π; the second order lies in the Q-span of {1, ζ(3), π², π² ln 2} over π².
3. **Its precision is what the option space demands.**
   * Grade formula families with the lane D checker (`alpha_bar_checker.py --size K --predicted-precision δ`). The bar is P < 1e-3, a miss ≤ 5e-10 or the route's own a-priori precision, zero fitted reals, and the scale stated.
   * Grade mechanism outputs, which are continuous numbers, with a declared prior: log-uniform 1/alpha in [10, 1000] by default (density 0.217 per unit relative deviation). A narrower declared range is stricter and is allowed. **The stricter of the two grades applies.**
   * The relative miss δ each grade allows for P < 1e-3 (`cfg895_check.py` B3):

| Option space K | Formula grammar (lane D) | Mechanism, one trial | Campaign-wide, × N_mech = 359 |
|---|---|---|---|
| 1 | 2.0e-2 | 2.3e-3 | 6.4e-6 |
| 10 | 2.0e-3 | 2.3e-4 | 6.4e-7 |
| 100 | 2.0e-4 | 2.3e-5 | 6.4e-8 |
| 1e3 | 2.0e-5 | 2.3e-6 | 6.4e-9 |
| 1e6 | 2.0e-8 | 2.3e-9 | 6.4e-12 |
| 3.6e7 | 5.6e-10 | 6.4e-11 | 1.8e-13 |

   * **Corollary (B3, K9).** A route that predicts a single UV coupling cannot reach campaign-wide P < 1e-3 at today's running precision, because P_single ≥ 3.8e-4 and N_mech × P = 0.14. Such a route can at most be CONSISTENT. A route that predicts **two or more couplings, or a coupling and a mass, jointly** multiplies its P values. At Y1 precision a joint alpha_Y and alpha_2 hit has P_single ≈ 9e-8, which survives N_mech = 359 (N_mech × P = 3.3e-5). **Prefer routes with joint predictions.**
4. **It runs and states its scale** (section 1.3), with zero fitted reals.
5. **It matches the measurements, not their centre.** The independent measurements agree only to about 9 digits: the Cs and Rb recoil values are 5.5σ apart (V1). Grade a candidate against all five V1 values with `v1_exactness_harness.py --candidate`. Landing on the CODATA centre is not evidence.
6. **It survives an independent re-derivation.** A second agent, working blind, derives the critical step before seeing the author's verdict and reproduces the number. This is the FSP practice and the AS3/AS4 re-runs.
7. **It makes a second prediction.** The mechanism predicts at least one other measurable quantity that was not used as an input. This is the EXT-screen rule (3).
8. **It survives the campaign-wide look-elsewhere test** (section 3).

## 5. Grades (use exactly these words)

| Grade | Meaning |
|---|---|
| KILLED | Outside the route's own stated error, or it fails its joint test. |
| NOT COMPLETED | A gate failed, so no graded value exists (AS1, AS2). |
| NOT DIAGNOSTIC | Several admissible roots, an option space too large for the achieved precision, or leverage below the bar (AS3; the FSP selection equation by B2). |
| CONSISTENT | Inside the route's own error, but P_family ≥ 1e-3. "Allowed, not predicted." **Never call this a derivation.** B1's weak pass (138.35 ± 8.28) was of this kind and was later withdrawn as a three-coupling result (B4). |
| EVIDENCE | Every item in section 4 holds except a precision at the level of the measurements. A K1 or K2 kernel with a second prediction. |
| DERIVATION | EVIDENCE, plus a K1 kernel, plus precision at the level of the measurements (a miss ≤ 5e-10 against all of V1's values) or a declared a-priori theory error ≤ 1e-6 with a hit inside it, plus independent re-derivation, plus a second prediction that checks out. **Nothing in the record reaches it.** |

Use none of the following phrases unless the grade is DERIVATION: "derives alpha", "explains 137", "theory closed". "Within X% of 137" may not be written without the P value beside it. No public statement goes out without the owner's sign-off.

## 6. Running the campaign

* **One graded trial per lane** whenever possible. The frozen pre-registration is committed first, then the run, then an independent re-run.
* **IDs.** Take an ID only from a block reserved in `campaign_fresh_gravity/LEDGER.md` (grep LEDGER and `ls campaign_fresh_gravity` first). The fine-structure puzzle programme keeps its own FSP-xxx numbering and its own review rules (`fine_structure_puzzle/TARGET.md`). Its results are cross-listed in this ledger, not renumbered.
* **Parallel lanes share the ledger but not lane directories.** Nobody edits another lane's files. Frozen files are never edited (`*_PREREGISTRATION.md` gets amendments appended; hash files never change).
* **Downloads.** Primary sources are read before any number from them is used. A recalled formula is labelled "recalled" and checked numerically against a printed decimal. Whether downloads are allowed is the owner's decision for each lane.
* **Compute.** Light single-core scripts only while a 1024³ run is live. Lattice production jobs (for example FSP-011's N0) are owner decisions.
* **Stop rule.** Two consecutive KILLED or NOT DIAGNOSTIC results on the same door close it, unless a new forced element appears. This applies to that door and its variants.
