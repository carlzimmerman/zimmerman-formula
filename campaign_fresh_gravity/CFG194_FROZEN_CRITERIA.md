# CFG194 — Referee re-derivation of CFG189 (the KURVS a0(z) test re-run with the MEASURED outer rotation markers, three laws, plus variant BS). FROZEN CRITERIA (phase 1)

(Numbered CFG194 on the coordinator's message; the scratch dir keeps its earlier name `cfg191`. Every "CFG191" in older notes means this lane.)

Written 2026-09-29 by the referee agent, BEFORE any script exists, before any marker value was read, and before CFG189's `.py`, `.out` and `.json` were opened.

## 0. What I read and did not read (order of work)

- **Read (phase 1):** CFG189 `FROZEN_CRITERIA.md` (39846c92e) and `README.md`; CFG175 README (with its two appended notes); my referee READMEs CFG165, CFG166, CFG167, CFG168, CFG180, CFG183; the data chat's digitisation README, the head of `checks.txt` and the column headers of `kurvs_rc_points.csv`, `kurvs_rc_control_vs_table.csv`, `kurvs_rc_reference_lines.csv`, `kurvs_rc_model_curves.csv`; the sigma-profile README; `KURVS_DEFINITIONS_NOTE.md` and `KURVS_SIGMA_METHODS_NOTE.md`; the column headers and row counts of the `kurvs2023_*` tables; and the function list, loader, `per_object`, `pool`, `anchor_pool`, `cell` and `classify` of my own `CFG165_referee_kurvs_p4.py` (to plan the imports). **No marker value, no model-curve value and no control-file value was read.**
- **Not read, and not to be read until my own main and MUTATE runs and attacks are saved:** CFG189's `cfg189_measured_markers.py`, `.out`, `_results.json`, `_MUTATE1*`; CFG184's script and README; every value in `kurvs_rc_points.csv`.
- **Order:** phase 1 = this file. Phase 2 = my scripts written from this text alone -> main run, MUTATE runs, attacks, mocks all run and saved -> ONLY THEN CFG189's `.py`, `.out`, `.json` opened -> `CFG194_diag_post.py` written after that (labelled post-comparison; not part of any frozen result).
- **Not a blind re-derivation.** Every CFG189 README number below is a TARGET I read, not a prediction. My hand estimates (section 3) were made after reading the README, and are labelled as such.
- Repo untouched; no network; no new data. No absolute home path in any output (`<repo>` is printed; `ZF_REPO` or a walk up from `__file__`). Every run under 15 minutes (expected under 2 minutes for the set, mocks vectorised).
- Standing rules kept: kappa = 1/2 is FITTED; a0(z) FLAT is the framework's distinctive law, a0 proportional to H(z) the rival, T (a0 proportional to t(z)/t0) the owner's third reading; nothing here says the data favour any law; a lean is not a detection; failed controls and wrong expectations are kept, never repaired.

## 1. What is re-derived, and where independence STOPS

**Re-derived from the frozen CFG189 text, in my own code:**
- the marker reader (from `kurvs_rc_points.csv`), the unclipped filter, the per-side outermost-marker rule, the variants V-a, V-b, V-c, V-d;
- V_out = |v_obs| / sin i_SFR and its error (mean of the up and down bars, over sin i);
- sigma at R_out (my own interpolation on the unclipped sigma profile, same side; error interpolated with it; beyond the side's points the outermost sigma point);
- the T law t(z)/t0 (closed form, flat LCDM, Omega_m = 0.315, my own code; patched into the imported pipeline's `E_of_z` in-process, with two controls: E := 1 reproduces flat exactly and the original E replays the rival exactly);
- the break-even root-finder and 1-sigma edges (roots of Delta'(mu) = 0 and +-sigma(mu), sigma at the trial mu), the gas-status rule (excluded iff the lower 1-sigma edge of the KURVS break-even exceeds 3.47; "over" iff no root; else allowed), the fit points s0 at mu = 0.67 (root in s of Delta' = 0), the headline label;
- every attack and mock.

**Imported read-only from `CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` as `M` (SHARED, not independent):** `load_kurvs` (non-velocity columns: R_eff, log M*, z, sigma0, table col 3 for the control only), `load_sparc_anchor`, `per_object`, `pool` (chi2/dof inflation), `anchor_pool`, `cell`, `spec`/`SP`, `alpha_K` (Kretschmer's alpha(x) as quoted, unverified literature), `classify`, `E_of_z`, and through it `CFG4_common.nu_mono` and the a0 constants. **`load_kurvs` reads the model-value column; I use it only for the control C1 and for the non-velocity fields, and I overwrite S.R, S.V, S.eV, S.sig, S.esig, S.grad2 and S.inc from my own marker reader. `MUTATE` is forced to "0" during the import.** CFG165, CFG167, CFG168, CFG180, CFG183 showed this pipeline reproduces CFG160/161/162/170/175 numbers.

**Shared and NOT re-checked:** (i) the data chat's digitisation itself (`kurvs_rc_points.csv`, `kurvs_sigma_profiles.csv`, the model curves): I read its tables, I do not re-extract them from the PDFs; the only check I make on it is the control against Table B1 (section 5, C4) and the marker-radius agreement (C2'); (ii) CFG140's set-up (thin exponential discs, spherical surrogate, g_obs = V^2/R, gas bracket mu, mass error 0.15 dex, inclination error 5 deg, the ten f_DM discs, the z = 0 SPARC anchor); (iii) CFG175's declared gas ceiling 3.47 and placed s values; (iv) **variant BS's forward model: CFG184's functions, imported/exec'd read-only in phase 2 (allowed by the task), so BS is NOT independent, and CFG184's own script and README stay unread until my runs are saved.** Agreement therefore shows that the frozen text plus the data plus this shared pipeline determine the numbers. It does not test nu_mono, alpha(x), the pressure prescriptions, the digitisation, or the physics of any law.

**Forks not fixed by the CFG189 text, declared here before any value is read (each also a row in the attack grid):**
1. Signs: "the plot convention is that the velocity gradient is always positive", so I use |v_obs| and |R| and keep the side label sign(R). If the negative side's v is signed I take the absolute value; the sign structure is printed, not assumed.
2. Ties: if the two sides' outermost unclipped |R| differ by less than 0.005 kpc, take the positive side.
3. Inclination column for the primary: i_SFR both for the deprojection and in the +-5 deg error term (as CFG189's text says). CFG160's model-value cell used i_star in the error term (CFG165 found the column moves Delta' by 0.002-0.005 dex). So C1 (model-value reproduction) uses i_star, the primary uses i_SFR, and the diagnostic `V-d'` (primary with i_star in the error term only) isolates the column.
4. Interval convention for break-evens: sigma at the trial mu (the convention CFG175 and CFG183 show).
5. s axis: alpha_K x s applied to the KURVS discs AND the anchor, s in {0, 1, 1.42, 1.62, 1.69, 3.00}; s = 0 is P0.

## 2. The headline, pinned (CFG189 README numbers = TARGETS I read)

Decision cell: mu = 0.67, s = 1 (P4, Kretschmer), delta = 0, canonical footing. Classes per the frozen map (`classify`: lean rival = flat > +2 sigma and rival within 2 sigma; lean flat = rival < -2 sigma and flat within 2 sigma; else non-diagnostic).

| input | flat Delta' (z) | a0 proportional to H (z) | T (z) | class |
|---|---|---|---|---|
| model V, Table B1 col 3 (CFG160/175) | +0.144 ± 0.044 (+3.3) | −0.006 (−0.1) | +0.323 ± 0.047 (+6.9) | lean rival |
| **measured primary** | **+0.125 ± 0.051 (+2.4)** | **−0.021 (−0.4)** | **+0.295 (+5.5)** | **lean rival** |
| V-a outer three | (+2.4) | (−1.0) | (+5.9) | lean rival |
| V-b both sides, shorter radius | (+0.1) | (−3.2) | (+3.4) | **lean flat** |
| V-c clipped included | (+2.8) | (+0.1) | (+5.7) | lean rival |
| V-d i_star deprojection | (+2.2) | (−0.7) | (+5.3) | lean rival |
| BS (sigma_int from CFG184) | (+2.2) | (−0.6) | (+5.2) | lean rival |

- Shifts, measured primary minus model: flat −0.019 dex (z −0.84), rival −0.015 (−0.29), T −0.027 (−1.46).
- Headline by the frozen form: T's z shift 1.46 > 1, so **CHANGED** (the class at the decision cell is unchanged, lean rival; 1 of the 5 variants, V-b, flips the class to lean flat).
- Per-disc, measured V_out against the model V: KURVS-3 +10.5% (at 10.06 kpc, not 11.70), -7 −15.2%, -8 −6.6%, -9 +0.4%, -11 −3.3%, -13 +9.7%, -15 −6.5%, -16 −5.8% (at 10.05, not 10.90), -17 −22.3% (at 7.34 kpc, not 9.90; its two outer markers are clipped), -21 −6.0%. Marker errors exceed the model errors (KURVS-3: ±32.9 against ±14.1 km/s).
- Break-evens at s = 1, flat / rival / T: model 2.11 / 0.62 / 4.34; measured 1.86 / 0.50 / 3.80. T's lower 1-sigma edge at s = 1 falls below 3.47 (T gas-allowed at s = 1 by CFG175's rule; still 5.5 sigma under-predicting at the decision cell); at s = 1.42–3.00 T central break-evens 4.97–9.11 stay excluded; T at P0 fits (+0.9 sigma).
- Fit points at mu = 0.67: flat 0.42, rival 1.12, T < 0 (model V: 0.39 / 1.03 / < 0).
- C2 (frozen by CFG189, kept failing there): 22 of 231 markers exceed 0.02 kpc: two are KURVS-3's extra velocity markers (−9.41 and −8.57 kpc, no sigma counterpart), twenty are all of KURVS-17's panel at a constant 0.065 kpc offset.

## 3. Hand estimates (made AFTER reading the CFG189 README; labelled; reproduction probabilities)

| item | my estimate | P(reproduces within the pass line) |
|---|---|---|
| primary flat / rival / T Delta' | +0.12 / −0.02 / +0.29 (± 0.015 each) | each within 0.008 dex: 0.55 |
| primary sigma_flat | 0.051 ± 0.004 | within 8%: 0.65 |
| primary class at decision cell | lean rival | 0.9 |
| variant classes (V-a, V-b, V-c, V-d, BS) | rival, **flat**, rival, rival, rival | all five: 0.45 (V-b is the coin flip, 0.65; BS 0.75 because it rests on the shared CFG184 functions) |
| shifts (flat, rival, T) in z | −0.8, −0.3, −1.4 | each within 0.3: 0.6 |
| headline label | CHANGED (T's shift 1.46 vs the line at 1 is a 0.46 margin) | 0.75 |
| per-disc measured/model, all ten within 1 pp of the README | | 0.6 (edge rules; KURVS-3, -16, -17 radii within 0.02 kpc: 0.8) |
| break-evens s = 1: 1.86 / 0.50 / 3.80 | | each within 6%: 0.5 |
| C2': 22 of 231, 2 in KURVS-3, 20 in KURVS-17 | | 0.75 |
| C1 (my loader on col 3 with i_star reproduces +0.1441 / −0.0060 / T +0.3227 within 5e-4) | | 0.9 |

**Hand estimates for the attacks (mine, unseen by any run):**
- (a) Radius-only decomposition: the model curve read at R_out (instead of R_max) moves flat Delta' by < 0.01 dex (P 0.6); the marker-minus-model step at fixed R_out carries most of the −0.019. The `V-b` flip: the farther side alone read at the SHORTER radius also flips to lean flat, P 0.35 (I lean toward "two-side averaging cancels a centring/asymmetry offset" as the driver, not radius). The fraction of the pre-declared grid (a2–a6) that keeps lean rival: 0.5 ± 0.2 (line 0.8: expected FAIL).
- (a) The V scale that ends the lean (flat +2 sigma) is only about −3% to −5% in V (flat sits 0.4 sigma above the edge): P 0.7.
- (a) The pressure ambiguity is NOT reintroduced by the marker choice: s_mid moves by <= 0.2 across the grid and the published placements stay above it, P 0.6.
- (b) Leave-one-out: lean rival persists in 4–8 of 10 (median 6; P(>= 8) = 0.25), because flat's +2.4 sigma is 0.4 sigma above the edge. Dropping KURVS-13, -17, -21 (large positive residuals in the model-value analysis) is the likeliest way out.
- (c) Marker chi-square about the model curve at R_out: 6–16 for 10 dof (P 0.6), p > 0.05 (P 0.7): the measured markers are consistent with the model within their errors, so the shift is mostly noise. The paired sign-flip p-value of the flat shift is > 0.2 (P 0.65). About half of flat's z drop (0.5 ± 0.15 of 0.84) comes from the larger sigma, half from the value.
- (c) Mocks (ideal, known gas): P(lean rival | flat truth) 0.10–0.25, P(lean rival | rival truth) 0.6–0.85, P(lean rival | T truth) < 0.05. With nuisance N1 (CFG165's): 0.3 / 0.55 / < 0.05. The frozen informativeness rule is expected to FAIL under N1 (P 0.8).
- (d) C2 immaterial (a passing C2 would change no class and no z by more than 0.1): P 0.85.
- (e) Direction agrees with the model-value verdicts (same class, same signs of Delta' for all three laws, ordering flat > rival and T > flat in break-evens): P 0.9. Disagreements: V-b's class and T's s = 1 gas label (both known to be fragile).

## 4. The pass lines (main run; rows are REPRODUCES / DIFFERS, never "repaired")

- **P1 (C1)** with the table's col 3 (i_star error term) and my sigma_out at R_max: flat and rival cell within 5e-4 of +0.1441 / −0.0060; T within 5e-4 of +0.3227 (CFG175, via my own t(z)/t0).
- **P2 per-disc table:** R_out within 0.02 kpc of the README radii where quoted (KURVS-3 10.06, -16 10.05, -17 7.34); measured/model −1 within 1.0 pp of each README entry.
- **P3 primary decision cell:** for each law |Delta' − target| <= 0.008 dex, sigma within 8%, z within 0.25. T's target +0.295 (z 5.5).
- **P4 class labels:** primary = lean rival; the five variants = rival / flat / rival / rival / rival in the order V-a, V-b, V-c, V-d, BS; z of each variant law within 0.35 of the README's one-decimal values.
- **P5 headline:** the shifts −0.019 / −0.015 / −0.027 dex within 0.006, the z shifts −0.84 / −0.29 / −1.46 within 0.3, the label CHANGED, and "1 of 5 variants flips".
- **P6 break-evens and status:** measured mu_be at s = 1 (1.86 / 0.50 / 3.80) within 6%; model (2.11 / 0.62 / 4.34) within 4%; T's lower 1-sigma edge at s = 1 below 3.47 and its s = 1.42–3.00 centrals in 4.97–9.11 within 6%; the T-at-P0 z +0.9 within 0.3; fit points s0 0.42 / 1.12 / < 0 within 0.05.
- **P7 C2':** the count of markers with |R_v − R_sigma| > 0.02 kpc equals 22 of 231 (+-2), and the split 2 (KURVS-3) / 20 (KURVS-17, constant offset 0.065 ± 0.01 kpc).
- **P8 determinism:** a second full main run byte-identical.
- Overall main verdict per row; "REPRODUCES" overall only if P1–P8 all pass. **Exit convention: main exits 0 iff my own controls (C1, C3, C4 below, and the two E-patch controls) pass; the reproduction rows and the attack outcomes are reported and do not set the exit code. MUTATE exits 1 when the control bites; a MUTATE that does not bite exits 0 and is kept.**

## 5. Controls and MUTATE

**My controls (main run):**
- **C1** (= P1).
- **C2'** the marker-vs-sigma radius agreement is REPORTED (as CFG189 froze it: within 0.02 kpc wherever both exist). It is scored as a row (P7), and its value is what it is; a fail is kept, as in CFG189. Attack (d) asks what it means.
- **C3** the T-law patch: E := 1 makes the H rows equal flat to 0.0; the original E replays the rival rows to 0.0; t/t0 = 1 at z = 0 (CFG183 showed the anchor control is vacuous, so I also require t/t0 at z = 0.85 / 1.5 to equal −0.3264 / −0.5099 dex to 0.002).
- **C4** the digitisation control against Table B1: the data chat's model curve at R_Hα,max divided by sin i_SFR reproduces col 3 to within 1.5% for the ten discs. (Computed in my own code from `kurvs_rc_model_curves.csv` and the table; KURVS-10 is not in the ten; KURVS-4 is not either.) This checks the digitisation, not the physics.
- **C5** structure: 511 markers, 18 clipped, ten discs present, every side has an unclipped marker.

**MUTATE (each flips a load-bearing cell; exit 1 = the control bites):**

| MUTATE | what it does | bite condition (frozen) | my expectation |
|---|---|---|---|
| M1 | measured V x 10^0.3 (V and its error) | class at the decision cell differs from the main run's | bites: both flat and rival above +2 sigma, "non-diagnostic (both outside)" (P 0.95) |
| M2 | the law labels swapped in `classify` | class != lean rival | bites; NOT lean flat (CFG165's M3 lesson: the map is not label-symmetric); P 0.9 that it reads non-diagnostic |
| M3 | no inclination deprojection (V_out = |v_obs|, error likewise) | class != lean rival | bites: V lower by 1/sin i, flat Delta' falls below +2 sigma (P 0.9) |
| M4 | T := flat (t/t0 replaced by 1) | T's rows equal flat's to 1e-9 and the headline T-shift z equals the flat shift | bites (identity); P 0.99 |
| M5 | the innermost unclipped marker with |R| >= 0.25 R_max instead of the outermost | flat Delta' differs from the main run's by more than 0.05 dex | bites: P 0.85 |
| M6 (informational, exit 0 is allowed) | sigma at R_out permuted across discs (seed 194) | class != main class | CFG165's M6 did not bite for the lean class; P(bites) 0.3; kept either way |

## 6. The attacks (pre-declared procedures; the headline stays the primary at the decision cell)

**All bootstrap/mock seeds: 194 (main) and 195 (repeat, agreement within 0.02 in every class fraction, else "seed-unstable" is reported). Mock N = 10,000 per world and family. Bootstrap N = 2,000 disc resamples.**

### (a) The digitisation: which marker is "the outer point"
Grid (each row: Delta' and z for the three laws at s = 1, mu = 0.67, and the class):
- **A1** primary (P3 reproduction).
- **A2** each side alone: the + side's outermost unclipped marker; the − side's; and the nearer-to-R_max side.
- **A3** annulus median: the error-weighted mean and the plain median of |v|/sin i over the unclipped markers with |R| in [0.8, 1.0], [0.7, 1.0], [0.6, 1.0] x R_far, both sides pooled, at the mean radius; error = max(propagated, standard error of the scatter).
- **A4** outer k = 2, 3 (V-a), 5 markers on the farther side, error-weighted.
- **A5** both sides averaged (V-b): interpolated on each side at the SHORTER side's outermost unclipped radius; AND the discriminating pair: **A5x** the farther side alone read at that same shorter radius; and **A5y** both sides at a fixed fraction of the table R_max (f = 0.8) interpolated on each side (only discs where both sides reach). A5 against A5x decides whether the V-b flip is radius or the two-side average.
- **A6 radius scan:** for f in {0.5, 0.6, 0.7, 0.8, 0.9, 1.0} x R_max(table), the farther side's V interpolated at f R_max (discs where it reaches); Delta' and z of flat and rival against f.
- **A7 inclination:** sin i_SFR (primary); sin i_star (V-d); the error term i_star (V-d'); i_SFR ± 5 deg as a scale row (V scales by sin(i)/sin(i ± 5), all discs coherently).
- **A8 V scale tolerance:** the coherent V scale v_s in [0.90, 1.10] step 0.01: the class against v_s and the two crossing scales (flat = +2 sigma; rival = −2 sigma). This bounds the untested beam-smearing bias of V, the centring, and non-circular motion as a single number: how large a coherent V error ends the lean.
- **A9 the model curve at R_out** (from `kurvs_rc_model_curves.csv`, divided by sin i_SFR, my own interpolation): the decomposition chain **model at R_max -> model at R_out (radius effect) -> measured at R_out (marker-minus-model)**, for each law: Delta' and z at each step, and the fraction of the total shift each step carries. Also the sigma step: sigma at R_out versus at R_max.
- **A10 the pressure axis (the P0-versus-P4 question):** for the primary and for every A1–A7 row that changed the class: Delta'(s) for s in {0, 1, 1.42, 1.62, 1.69, 3.00}, the crossing s_mid (Delta'_flat = Delta'_H at mu = 0.67; model-value target 0.669), s_f2 and s_h2, and CFG175's status labels (flat / rival / T).
- **Pass/fail meaning:** (i) the class is choice-robust iff >= 80% of the grid rows A2–A7 (not the A6 scan, not A8) keep lean rival and none flips the rival to > +2 sigma; expected FAIL. (ii) The verdict is radius-driven (as CFG189's reading says) iff A5x also flips to lean flat AND A6's class changes monotonically with f; centring-driven iff A5 flips and A5x does not. (iii) The pressure ambiguity is NOT reintroduced iff the range of s_mid over the grid is <= 0.20, and K21 (s = 1) plus the four other placements stay above s_mid in every row; it IS reintroduced if any row moves s_mid above 1.0 (the class then depends on the calibration) or above 1.42.

### (b) The disc set
- **B1 leave-one-out** (10 runs): the class, z and mu_be for the three laws. Pass line: lean rival persists in >= 8 of 10 (expected FAIL).
- **B2 bootstrap** of the ten discs (N = 2,000, seed 194): class fractions for the three laws at the decision cell; P(flat z > 2) and P(T gas-allowed at s = 1).
- **B3 named subsets (reported):** drop KURVS-17 (its two outer markers clipped; outer radius 7.34); drop discs whose outer markers are clipped; drop |measured/model − 1| > 15%; keep only discs whose farther side reaches >= 0.9 R_max (table); drop KURVS-21 (flagged asymmetric).
- **B4 extension (labelled, NOT part of the headline; needs no new data):** the discs of the 22 with a measured outer point and an integrated-table row and V/sigma0 >= 1.0 (`kurvs2023_kinematics`), run through the same pipeline with the same declared gas (mu = 0.67). Reported as a robustness row: does the lean survive a wider sample where measured markers are usable? A B4 class that differs from the ten-disc one is stated as "sample-specific", not repaired.
- **Meaning:** the ten discs are CFG140's selection (the f_DM rows); a class that lives on 4–8 of them is a small-sample lean.

### (c) The error model and null worlds
- **C-a marker consistency:** chi-square of (measured V_out − model V at R_out) with the marker errors (dof 10; correlated neighbours make this a lower bound on the dispersion), and the per-disc pulls. The pooled chi2/dof and the inflation factor inside `pool` for measured and model runs.
- **C-b paired sign-flip test:** 10,000 random sign flips of the per-disc (log V_meas − log V_model) shifts, seed 194: the distribution of the pooled flat, rival and T shifts; the observed shifts' two-sided p-values. Meaning: is "the markers move all three laws toward the data" more than noise.
- **C-c the z decomposition:** flat's z drop split into value-only (new Delta', old sigma) and sigma-only (old Delta', new sigma) parts.
- **C-d error variants (grid):** E1 mean bar (primary); E2 the larger bar; E3 the smaller bar; E4 all marker errors x 1.5 (declared for correlated adaptively-binned neighbours); E5 a 5 km/s systematic floor added in quadrature; E6 a coherent common V scale error ln s ~ N(0, 0.03) propagated as a covariance term (declared, standing for beam smearing, centring, non-circular motion). Reported: Delta', sigma, class, T z.
- **C-e mock null worlds, three truths x two families, same errors:** truth = the real KURVS baryons, sigma_out (measured), R_out, and marker errors; the law (flat / rival / T at its own z) generates g; mock V_c from g, mock V_obs^2 = V_c^2 − alpha_K(x) sigma^2 (s = 1, the analysis pipeline's own pressure model), mock marker = V_obs + N(0, err_meas), the analysis is the primary pipeline exactly.
  - Families: ideal (mu_true = 0.67, alpha exact, s = 1); N1 (CFG165's: mu_true lognormal median 1.0, 0.3 dex; alpha x lognormal(0, 0.4) per disc x coherent lognormal(0, 0.2)); and, for the extra-scatter reading, **N1x** (N1 plus per-marker extra scatter equal to sqrt(max(0, observed rms pull^2 − 1)) x err, only if C-a finds pulls above 1).
  - Statistics per world: mean and sd of Delta' (three laws), P(z_flat >= 2.4), class fractions, the T status at s = 1 (fraction with lower edge above 3.47), and the likelihood ratios at the observed primary (rival-truth over flat-truth; T-truth over flat-truth; Gaussian and KDE).
  - **Frozen informativeness rule (CFG165's):** the lean is "justified as stated" only if P(lean rival | flat truth) < 0.05 and P(lean rival | rival truth) > 0.3. Reported for ideal and N1 (and N1x). Expected: passes ideal at most marginally, FAILS N1.
  - Measured-versus-model power: the same mocks run with the model-value errors (CFG165's power) as a row, to state whether swapping to markers changed the discriminating power.

### (d) The kept failure C2'
- **D1** what the failure is: the exact list of markers over 0.02 kpc, per disc (P7).
- **D2 repair variants (post hoc labelled):** (i) KURVS-17's sigma profile shifted by its constant offset, sigma re-interpolated; (ii) sigma taken from the nearest sigma marker in |R| on the same side; (iii) KURVS-17 dropped; (iv) KURVS-3's two extra markers dropped from the velocity list (they only matter if they are its outer point; the count of discs where any of them is used).
- **Pass/fail meaning:** C2' is IMMATERIAL iff, over D2 (i–iv), no class changes and the largest change in any law's z is <= 0.10. If it is material the CFG189 headline is conditional on an unrepaired radius mismatch.

### (e) Agreement with the model-value verdicts (CFG165/175)
Rows: same class at the decision cell; sign of Delta' for each law; ordering of break-evens (rival < flat < T at every s); T's s = 1 gas label against the ceiling and against CFG183's 2.2% margin note; the s-axis ordering of the placements against s_mid. **Disagreement** = a class change, a sign change, an ordering change, or |z shift| > 1 for any law; each disagreement is explained by the A9 decomposition (radius / marker / sigma / error size) or reported as unexplained.

## 7. Script plan (names CFG194_*; exit convention as in section 4; outputs `<name>.out` and `<name>_results.json`; no absolute home path printed)

- `CFG194_lib.py` — marker reader, outer-point rules (primary, V-a..V-d, A2–A6), sigma-at-R_out, t(z)/t0, root-finder and status rule, headline label; imports `M` from CFG165 (shared).
- `CFG194_referee_main.py` — P1–P8, C1–C5, the section 2 table for the primary and the five variants (BS via CFG184's functions, read-only, in phase 2; skipped with a stated flag if that import fails, never substituted). `MUTATE=1..6` selects the mutations; MUTATE runs write `CFG194_MUTATE_<k>.out/_results.json`.
- `CFG194_attacks_a.py` — A1–A10 and B1–B4 (deterministic).
- `CFG194_attacks_c.py` — C-a to C-e and D1–D2, seeds 194 and 195 (file names carry the seed).
- `CFG194_diag_post.py` — written ONLY after CFG189's outputs are opened; labelled post-comparison.
- `run_all.sh`, `CFG194_manifest.txt` (sha256 of inputs, scripts, outputs). Whole set expected < 3 minutes.

## 8. What would count as DISAGREEMENT with CFG189

- Any pass line P1–P8 missed (in particular: my primary class is not lean rival; V-b does not flip; the headline is not CHANGED; the break-even or status labels differ; C2's count differs).
- An attack showing a CFG189 sentence is not supported, which is then a valid referee finding even if all numbers reproduce. The ones I expect and will state if they occur: "the lean is 0.4 sigma above the class edge and does not survive leave-one-out or the V scale grid"; "the shift is inside the noise (paired p)"; "the V-b flip is radius / centring"; "the mock rule does not justify the class"; "C2 is / is not material".
- A finding that the digitised marker table itself is inconsistent with its README (C4, C5).
- Wrong hand estimates are kept and scored in the README's scorecard.

κ = 1/2 and Ω_c h² stay fitted. a0(z) FLAT is the framework's distinctive law, a0 proportional to H(z) the rival, T the owner's third reading. Nothing here says the data favour any law, or that the theory is closed; a lean is not a detection.
