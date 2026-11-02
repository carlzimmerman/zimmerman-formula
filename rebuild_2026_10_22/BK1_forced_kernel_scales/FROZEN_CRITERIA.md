# BK1_forced_kernel_scales: FROZEN CRITERIA, committed alone before any script, target budget run or search number of this lane

**Question.** a0 came from a dimension-pruned, depth-limited, deduplicated tree enumeration over forced constants, then a human step finding forced GR coefficients in the winner, then an interlock. Does the same procedure, gated, find anything on the scales the programme has since measured? Owner's go, 2026-11-02. The cold sector stays retired; no result here reinstates it. kappa = 1/2 FITTED. Numerology wall stands, SM targets stay out (SM values appear only as calibration negatives, inside project_atomos's own suite). Nobody here says breakthrough: each formula gets the list of gates it passed.

**Not blind.** Before freezing I read the target values below, `hali_flow/bruteflow/constrained_search.py`, project_atomos's gate and calibration code, and the READMEs of UX3, LM1, GM1, UX2, TD1, AF1, BF1, SL2, LC1, PZ1, plus `CU1/cu1_stress.out`. I know k is 10-14 fitted and that BF1's pi^2 family broke discs. No search of this lane has run.

**Read before freezing, and it shapes gate 5.** I ran project_atomos's Gate A on its a0 candidate. `candidate_a0` sets `target_value = KERNEL = 2.894` but its structural null returns accelerations near 1e-10, and the gate tests |out - target_value| < 6e-12. So P = 0 and bits = inf **by a unit mismatch**. Compared to a0 itself the same null gives P 0.022, **5.5 bits, under its own 10-bit line**. So "calibrate.py 8/8" holds, but a0's Gate A pass in it is an artefact. Project_atomos isn't edited here; this is reported. Gate 5 below therefore doesn't lean on that pass.

## Expected structure, stated before any number
- With a0 tied to rho by a0 = c sqrt(G rho)/2 on each footing, c, G, rho, a0 make one dimensionless group, and its value is the fitted 1/2. So **for dimensionless targets the dimensional filter removes nothing physical**, the search reduces to geometry numbers, f_b and (with H0) Omega_DE. This is ENGINE_REVERSE_ENGINEERING section 4's warning, and I expect gate 2 to kill them.
- T needs about 10.7 dex from the Hubble mass (TD1), and this alphabet holds no small number, so I expect no T hit, or none at low depth. Expected, not a result.
- I expect zero survivors at gate 4. Same bar if it's otherwise.

## Targets, chosen before search. 2 sigma acceptance throughout
Total error = statistical and systematic in quadrature. Reported per footing, never pooled. Numbers marked (A1) get fixed by `bk1_budget.py` in AMENDMENT_A1, by the procedure stated here, before any search.

| id | Target | Value canonical / alt | Statistical | Systematic | Independence class |
|---|---|---|---|---|---|
| K | gas-term k, X-COP train, A = 1 (UX3, CU1) | 13.287 / 14.251 | CU1 boot4 sd 2.10 / 2.28 (only 35 distinct resamples) | HSE bias: half of k(HSE) - k(HSE - 0.12 dex, LF1) (A1) | I (X-COP gas) |
| D8 | Q, dM/M_gas, x 0.2-0.5 (GM1) | 7.56 / 7.18 | 1.03 (GM1), alt taken the same | LM1 X-COP HSE bracket half-shift at x 0.2: (8.0 - 5.2)/2 = 1.4 | I |
| D5 | Q, x 0.5-1 (GM1) | 5.37 / 4.93 | 0.79 | at x 0.5: (5.2 - 3.1)/2 = 1.05 | I |
| XR | omega_x/omega_b, RF5 R1_3e5: same as the "cold-to-baryon requirement" of UX2, one target | 5.350, both | **no chain exists; statistical NOT MEASURED** | UX2 w grid at abs w <= 1e-3: omega_x 0.1173-0.1237, half-range 2.7 %; cell spread adds 0.2 % | II (CMB) |
| RHO | rho_x(0), same fit, dimension-bearing | 2.249e-27 kg/m^3, both | as XR | as XR | II, not independent of XR |
| FQ | f_Q, PZ1 (LC1 0.872) | 0.946, one sim set | half [0.78, 1.08] = 0.15, 8 seeds | half PZ1 - LC1 = 0.037 | III (sim) |
| T | switch threshold, lg M_sun (COOL1/TD1) | 12.29, canonical only | window [12.19, 12.39] taken as 2 sigma, so 0.05 dex, combined | included; "upper edge is one object's margin" | IV |

Second readings, reported beside the first, never replacing it: K and D8, D5 with GM1/UX3's HSC factor 1.7 added as half-difference in quadrature; XR, RHO with a 1 % statistical size added, tagged PROVISIONAL since it's a size-only recollection of CMB fits.

**Not targets.** The 0.0541 scatter (owner). SL2's A_req: a range across scales, no single number. Anything LCDM. Planck 5.364 isn't used.

**Flags.** BLUNT = dimensionless with sigma/value above 10 %. By this rule K, D8, D5, FQ will be BLUNT; they are searched and hits reported, labelled BLUNT. D8 and D5 are band values of a function falling with radius, so a "match" has less meaning. K, D8, D5 share class I and can't interlock with each other. XR, RHO share II. FQ contains 1, Blumenthal's own value, as a depth-1 number.

**Tautology.** f_b leaf is omega_b/(omega_b + omega_x) from the same cell (0.15747), so 1/f_b - 1 = XR by definition. f_b is **removed from the alphabet for XR and RHO**.

## The machine
Port of `constrained_search.py`. Value and (L, M, T) tracked together. Unary sqrt, cbrt, inverse, power from {2, 3, .5, -1, -2, 1.5, -.5, 1/3, 2/3}; binary mul, div; decoration by {pi, 2, 3, 4, 6, 2pi, 4pi} ×, ÷. Depth layers as in `_generate_at_depth`: leaf 1, depth d from unary and decoration on depth d-1 and binary on all pairs of depth < d. Full to depth 4; depth 5 is only decoration of depth 4 in the target's dimension (bruteflow's default 4-5, reduced for compute, stated). G1 has no addition, as the search that found a0. G2 adds a + b, a - b of equal dimension, at depth <= 3 operands, with its own control, because the record's FDR library has them.

**Counting.** Trees tried = every formal combination, including those pruned by dimension. Reported at each depth: tried, dimension-correct, distinct value after dedupe at 1e-9 relative (the numeric form of canonical-hash dedupe).

**Alphabets.** A: c, G, rho, a0, f_b. B: A + H0, footing stated: RF5 R1_3e5, h 0.675, Omega_DE 1 - Omega_m. rho = rho_DE canonical, rho_total alt, a0 9.3603e-11 / 1.1312e-10, rho set by a0 = c sqrt(G rho)/2, which ties them exactly. Lambda is rho with 8 pi G/c^2 and isn't a separate leaf. Calibration alphabet CAL: bruteflow's G, c, H0, Lambda, rho_c, l_P, t_P, m_P at its own values.

## Gates, in order, all required
**Gate 1, dimension.** Hard filter. Dimensionless targets: filter counted, recorded as vacuous per the structure above.

**Gate 2, FDR.** Window = value +- 2 sigma. Every hit has its Z = (value - target)/sigma reported. Controls: 1000 scrambled targets, seed 20261102, log-uniform within +- 1 dex of the target (the record's "same range", `koide_fdr_sqrt2`, `false_discovery_rate`), same fractional half-window, same machine. For dimension-bearing targets also SPAN: log-uniform over the whole occupied range of dimension-correct values.
- Statistic: d* = lowest depth with a hit. P(d*) = control fraction with a hit at depth <= d*. Look-elsewhere: bits = -log2(min(1, P(d*) x 15)), 15 = number of target-footing rows here, at 2 sigma. Trees tried enter through P, measured at that same size and tolerance. Also reported: hits vs mean control hits at each depth, candidate-level FDR = mean control hits / real hits, and the bit ceiling log2(2 dex / window width in dex), which limits any target before search.
- **Reading A: PASS at bits >= 10**, GATE_SPEC's line.
- **Reading B: PASS at bits >= B_ref**, B_ref = a0's bits on the same machine and same null in gate 5, used only if a0 fails reading A and all negatives fail at B_ref. A target can't be promoted by B alone without that being said. Both readings are always reported. A tolerance never widens after a result; if a budget changes, both readings are reported.
Fail = **COINCIDENCE** at gate 2, no further gate needed; gates 3 and 4 are still computed for the lowest-depth hit of each target, marked as near-miss information.

**Gate 3, forced kernel.** Registry, frozen here, each with its law: 8 pi Einstein; 3 Friedmann; 4 pi Poisson; 2 pi Gauss on a thin sheet; 4 pi/3 sphere volume; 18 pi^2 EdS virial overdensity. Substitute the record's identities (Friedmann rho_c = 3H^2/8 pi G; Einstein rho_L = Lambda c^2/8 pi G) into the winner. The numeric coefficient must equal a product of at most two registry factors from distinct laws at powers +-{1/2, 1, 2}, times at most one free number from {1/2, 2}. Run through project_atomos `forced_kernel_detector` with `Factor`s from its registry extended with this list in a local copy. **Known departure:** that code requires exactly one free number; I also pass zero free and label it. Mechanical decomposition is cheap (GATE_SPEC: provenance, not factorization), so a pass also needs a written line saying why that law acts in that observable, and I'll report the control's mechanical pass rate. No line, label FORCED FACTORS, NO LINK, a fail.

**Gate 4, interlock.** The same skeleton (same monomial, up to the at-most-one free number) hits at least 2 targets of **different independence classes**, or ties at least 3 constants with at most 1 parameter, on the same footing. Class I targets among themselves don't count. Scored over all hits, with the control rate of two scrambled targets from distinct classes sharing a skeleton.

**Gate 5, calibration, run and committed before any target search.**
- C1: `calibrate.py` runs unmodified, 8/8 reproduced as a code test, with the unit mismatch above noted.
- C2: the port on CAL re-finds c sqrt(G rho_c)/2 and its depth <= 4 form within 10 % of 1.2e-10, as `constrained_search` did.
- C3: after substituting Friedmann, its coefficient passes gate 3 (einstein, friedmann, free 1/2), gate 4 mode C1 as declared in calibrate.py (Einstein, Friedmann, dS-Unruh form).
- C4: corrected gate 2 on a0, with sigma 1.20 +- 0.02 +- 0.24 e-10 (McGaugh, Lelli, Schombert 2016, recalled, PROVISIONAL), and a second reading at calibrate.py's 5 %. Both LOCAL and SPAN. Sets B_ref on LOCAL at sigma's window.
- C5: negatives fail: atomos's 4Z^2+3, 64 pi+Z, Z+11, 6 pi^5, 3/13, dS-Unruh sqrt 2 (atomos's own path), and the same five at tolerance 1e-3 through this gate 2 at their dimensionless alphabet; plus k = pi^2 on the K row.
- Labels: **CERTIFIES** if C1-C5 hold at reading A. **CERTIFIES AT B ONLY** if a0 fails A, passes C2, C3, and all negatives sit below B_ref. **DOES NOT CERTIFY** otherwise, including if B_ref is so low a negative matches it. On DOES NOT CERTIFY, the search still runs for its counts, but **gate 2 PASS cannot be issued** on any target; I report raw hits, Z, control rates only.

**Gate 6, empirical.** Survivors of 2-4 only, both footings. K-type: UX3's path (`ux3_grade.py` reused by import, no edits): 15 keys, X-COP, discs; Bullet through the record's path if one applies; else stated not applicable. Prior note: UX3 and CU1 already record that no k clears every key (G-OUT-all needs about 7.2 or lower, MID-T3 about 12.9 or higher), so any bare k formula is expected to fail this gate as a k. Not a substitute for running a survivor.

## Labels per formula
COINCIDENCE (fails any of 2-4) with a gate list, NEAR MISS (top lowest-depth hit per target, with bits and margin to the line), PASSED GATES <list>. Lane verdict line: trees tried, hits, control rate, survivors at each gate.

## Checks and twins
K1 enumerator's a0 winner matches arithmetic. K2 depth-3 tree count against a brute python enumeration of the same grammar. K3 hist and exact window hit counts agree on depth <= 3. K4 Z sign and bits arithmetic on a hand case. K5 peak RSS < 4 GB, one thread, nice 19.
**PLANT:** target sqrt(8 pi/3)/2 dimensionless at sigma 1e-4, and rho_x-like dimensioned tree at sigma 1e-3, must be recovered; they report what bits the machine gives a true tree; a plant recovered at under B_ref tells me gate 2 lacks power there, and I say so.
**MUTATE:** G's dimension set to L^2 M^-1 T^-2: C2 must fail. Rerun byte-identical on the JSON.
Every failed check is published. Hit listings: all hits at depth <= 3, per target; depth 4-5 hits by histogram with Z distribution, plus up to 200000 rows lowest-Z first per target, the cap stated when it binds.

Compute: one thread, nice 19, preemptible by restart at per-target checkpoints. No downloads. No deposit. No edits to project_atomos, hali_flow, PAPER67 or the ledger. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
