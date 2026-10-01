# CFG243 -- a conserved dust created once, at turnaround, by a local causal source: phase 2 (a scoped no-go at the first gate, COSMIC)

Criteria frozen and committed before any script: `campaign_fresh_gravity/CFG243_FROZEN_CRITERIA.md` (commit 7cc93bdef, sha256 ee6df5b2...265a8ea2, identical to the file I wrote). Run as frozen; every departure and every ambiguity is listed in section 9. **Nothing here is closure. kappa = 1/2 stays FITTED. There is no dark-matter particle and no new species: the class is a pressureless fluid created from the vacuum, and the cold MASS is still required (the gates count it, and the class does not supply it).** A scoped no-go is not a theorem. Nothing in the repository was edited.

**Lineage (credit).** This lane descends from CFG251, the owner-directed "one-time pass" door 11D lane (reading iii-a: a compaction set once at a system's first turnaround, then frozen). It combines CFG251's turnaround-then-freeze reading with the PAPER36 / CFG35 conservation rule (the cold component keeps its collapse mass) and with CFG242 route A's persistence requirement (ownership must remember boundness; a decaying latch forgets at theta_b = 0). CFG251 found that the freeze reproduces the ownership CLASSES but not the AMOUNT; CFG243 attacked that gate and put the cosmic amount first.

**Disclosure about PAPER36.** The frozen file said that no PAPER36 file was found and read the conservation rule from `CFG35_README.md`. That statement was wrong: the paper exists at `qwen_claude_field_theory/papers_2026/PAPER36_cold_mass_conservation_2026.tex` (deposited as DOI 10.5281/zenodo.23025372; audit script `PAPER36_audit.py` in the same directory). The rule is cited here to both CFG35 (the source lane) and PAPER36. I read only the paper's statement of the rule and its stated status. The paper states it as derived from T4's premise that the cold fluid is pressureless and its amount conserved: "a bound system keeps the cold mass it collapsed with, M_c = (1 - f_b) M_coll", the leftover beyond the law's phantom keeping its collapse (NFW) profile. It changes nothing in how the rule is used here: the AMOUNT gate uses only the conservation of the dust AFTER creation (geodesic, conserved apart from the source), and no frozen line was edited. The paper's amount, (1 - f_b) M_coll, is the cosmic cold share that already exists at collapse. This class does not have that early fluid (COSMIC), so the rule's premise is exactly what the class cannot supply.

**Re-run (about 8.5 min).** From this directory: `ZF_REPO=<repo root> bash CFG243_run_all.sh` (inside the repository the root is found by walking up, so `bash CFG243_run_all.sh` suffices). It runs the controls, COSMIC, the post-hoc extras, every MUTATE and ROBUST check with the frozen expected exit code beside the observed one (`unexpected outcomes: 0`), then `CFG243_verdict.py`. It needs python3 with numpy, scipy, sympy and `classy` (CLASS 3.3.4.0 was importable here, so no own Press-Schechter or growth code was substituted for CLASS). Nothing is downloaded or installed. No output prints an absolute home path (`<repo>` and `<lane>` are substituted; checked by grep).

## 1. Bottom line

**COSMIC is the binding FAIL, as frozen.** Nothing has turned around at z = 1100, so a turnaround-triggered source supplies no dust at recombination. Under the most generous reading (amount tuned so that Omega_dust(z = 0) = Omega_c, collapse fractions taken from LCDM sigma(M) as if the cold matter already existed), with sigma(M, z) from CLASS:

| M_min (Msun) | z = 1100 | z = 10 | z = 2.5 | z = 0 (the normalisation) |
|---|---|---|---|---|
| 1e5 (most favourable; the verdict cell) | Omega_dust h^2 = 0.1200 x 10^-1376.8 | 0.0436 | 0.1007 | 0.1200 |
| 1e8 | 0.1200 x 10^-3451.1 | 0.0177 | 0.0888 | 0.1200 |
| 1e10 | 0.1200 x 10^-7892.3 | 0.0032 | 0.0719 | 0.1200 |

- **Against the frozen pass line 0.060 (0.5 x 0.1200) at z = 1100: the class supplies 10^-1377.7 and falls short by a factor 10^1376.5** (10^1376.8 against the full 0.1200). The order-of-magnitude line (0.006) is missed by the same margin, so this is the binding FAIL and the frozen stop rule halted the lane. It is not a scatter of the estimator: the CLASS sigma(M = 1e5 Msun, z = 1100) is 0.0134 against a threshold of 1.0624, so the erfc argument is 56 (an 80-sigma Gaussian tail) (hand estimate before the run: at most 1e-18 for any sigma(M, 0) <= 100; kept as an inequality that holds).
- **z = 10:** 0.0177 (M_min 1e8) is 14.7% of the 0.1200 that linear cold behaviour at z >~ 10 needs (shortfall 6.8x); 0.0436 (1e5) is 36% (2.8x); 0.0032 (1e10) is 2.6% (38x). Reported, not binding.
- **z = 0** is the normalisation, not a result. The class's own z = 0 amount is not computed here: CFG4's cold budget (restated, not recomputed) says the target's phantoms hold Omega_ph = 0.47-0.55 if every galaxy's phantom ran to its turnaround radius, against Omega_c = 0.265, and the budget edge x <= 0.46 uses all of Omega_c.
- **What would be needed for a pass:** sigma(M, 1100) = 1.575 for F_ta = 0.5, which is x118 (M_min 1e5) to x283 (1e10) the CLASS value, equivalent to a z = 0 sigma of about 1.1e3 against CLASS's 9.2 at 1e5 Msun.
- **The self-consistent reading is worse.** With no cold matter at all (omega_cdm -> 1e-7, flat) the maximum linear baryon-only sigma_b(R, z = 0) over R = 1e-3 to 100 Mpc is 0.076 against the threshold 1.276 (16.8x short): the trigger never fires in a baryon-only universe. And the acoustic baryon velocity divergence at z = 1100 reaches |delta theta_b|/(3H) = 2.4e-4 at most (k = 0.14/Mpc; rms 2.3e-4), so the trigger cannot fire in the plasma either.

The post-hoc extras (section 4) all fail as well, and the failures are of different kinds (a mislocated trigger, over-counting, a source that needs the enclosed mass, no knowledge of the host, a vacuum ledger short by 1.7x to 25x). They are not a verdict.

## 2. Gate table (P = PASS, F = FAIL, U = UNDEFINED, N = NOT ADDRESSED; each cell cites its script; FROZEN = the stop-rule verdict, PH = post-hoc extra, labelled, never part of the verdict)

| gate | cell | script |
|---|---|---|
| controls K1-K7 | **P** (9 of 9) | `CFG243_controls.py` |
| **COSMIC** | **F, BINDING, STOP (FROZEN)**: 10^-1377.7 against the line 0.060 | `CFG243_cosmic.py` (rows C1, C1b) |
| COSMIC C2-C6 (reported) | z = 10: 0.0032-0.0436; baryon-only sigma_b 0.076 (F, 16.8x); acoustic theta_b/(3H) 2.4e-4 (F); budget restated | `CFG243_cosmic.py` |
| G0 legality | **N in the frozen verdict**; PH: **F** | `CFG243_g0_legality_posthoc.py` |
| &nbsp;&nbsp;G0-a locus | PH **F**: theta_b = 0 comes 0.60 of t_ta later than the shell turnaround; 0.000 of shells within 25% | same |
| &nbsp;&nbsp;G0-b multiplicity | PH **F** (a counting rule is required): median 21-24 downward crossings per inner shell | same |
| &nbsp;&nbsp;G0-c causality | PH **P**: c_adv = 0.0 (N = 200, 400); the centred-difference detector fires (1.0) | same |
| &nbsp;&nbsp;G0-d bound-only | PH **F**: 1.0000 of the firing elements are not 3D-turned-around (sum of the axis terms = 3) | same |
| &nbsp;&nbsp;G0-e vacuum compensation | PH **F**: grad theta is misaligned with u_mu (residual/gradient = 1.0; the gradient is 9.3e7 x the aligned value) | same |
| &nbsp;&nbsp;G0-f inertness | PH **P**: no source in the Hubble flow and none in shells that never turn around | same |
| AMOUNT | **N in the frozen verdict**; PH: **F** | `CFG243_amount_posthoc.py` |
| &nbsp;&nbsp;AMT-1 dimension | PH **P as P-declared** (variable a0/g_loc, function declared) | same |
| &nbsp;&nbsp;AMT-2 construction | PH **P** (point mass exact, 4e-12; uniform sphere local, 4e-16) | same |
| &nbsp;&nbsp;AMT-3 locality of the amount | PH **F**: 14 of 16 cells exceed 10%; only the uniform sphere passes; counterexample pair differs by 3.000 | same |
| &nbsp;&nbsp;AMT-4 retention | PH **F**: f_ret spread 128 (1e9-1e12), 2.98 (1e9-1e11); amplitude error 10.3 / 0.73 against 0.10 | same |
| &nbsp;&nbsp;AMT-5 survival (G1) | PH **F**: largest deviation 0.74-0.99 over the cases run; no creation scale passes | same |
| &nbsp;&nbsp;AMT-6 later turnarounds (reported) | zero-velocity radius 678 kpc with the source against 243 kpc without | same |
| HIERARCHY | **N in the frozen verdict**; PH: **F** | `CFG243_hierarchy_posthoc.py` |
| &nbsp;&nbsp;H1 embedded | PH **F** (unflagged): amplitude ratio 0.047 / 0.445 / 0.996, firing-particle count ratio 1.000 | same |
| &nbsp;&nbsp;H2 accreted | PH **F** unflagged (21 times the first-crossing dust is created again); flagged **P only as a prescribed label** (CFG48 G3: PARTIAL) | same (multiplicity from the G0 script) |
| &nbsp;&nbsp;H3 top-level ownership | PH **F**: 0.16-0.21 of the baryons first turn around in a system of >= 0.1 of the final mass | same |
| G3/G4 | **N in the frozen verdict**; PH: **F** | `CFG243_g3g4_ledger_posthoc.py` |
| &nbsp;&nbsp;L1 reaction | PH **P** (0, trivially; the momentum accounting is G0-e) | same |
| &nbsp;&nbsp;L2 energy | PH **F**: M_c c^2 is 6.7e5 to 1.5e9 times the orbital energy | same |
| &nbsp;&nbsp;L3 vacuum ledger | PH **F**: f(x = 30) = 24.8 (CFG48 r_ta), 0.30 / 0.53 / 0.93 / 1.65 (B's r_ta), 1.71 (CFG131 Lagrangian); a0 shift f/2 against 1e-2 | same |
| &nbsp;&nbsp;L4 constants | PH **F (strict)**: the generous normalisation N enters COSMIC | same |
| G5, G2 (perturbation-level growth) | **N** (outside the frozen order) | not run |

## 3. The frozen gate COSMIC in detail (`CFG243_cosmic.py`, about 66 s)

- **Estimator (as frozen, with the memory-level inputs replaced):** Press-Schechter turned-around fraction F_ta = erfc(delta_ta / (sqrt2 sigma(M_min, z))), the frozen thresholds delta_ta = 1.0624 (z >= 10), 1.076 (z = 2.5), 1.276 (z = 0). sigma(M, z) comes from CLASS 3.3.4.0 matter transfer functions d_m(k, z) at the Planck 2018 inputs of `CFG4_cosmology.py` (matter_source_in_current_gauge needed for z above z_rec), P_R(k) = A_s (k/0.05)^(n_s - 1), a top-hat window at the mean matter density Omega_m rho_crit,0 with Omega_m = 0.3157. Controls reproduce the committed numbers: sigma_8 = 0.81165 (CFG4_cosmology.out 0.8116), Omega_m = 0.31573 (0.3157), the growth sigma_8(z = 10)/sigma_8(0) to 0.7% of CFG7_common's committed D(a), the committed top-hat contrasts 11.76 / 8.87 / 7.08 / 5.71 (CFG4: 11.81 / 8.89 / 7.09 / 5.72) and delta_lin 1.274 / 1.073 (1.276 / 1.076), and the CLASS velocity-divergence normalisation theta_tot/(calH delta_tot) = -0.9936 against -f = -0.9991.
- **sigma(M, z) table (CLASS):** z = 0: 9.17 (1e5), 5.92 (1e8), 3.92 (1e10), 2.25 (1e12); z = 10: 1.07, 0.69, 0.46, 0.26; z = 1100: 0.0134, 0.0084, 0.0056, 0.0032. M* (sigma = 1.686) = 6.7e12 Msun.
- **The dust-to-baryon ratio of the target (stated, not used in the verdict):** M_c/M_b = sqrt(1 + x^2) - 1 (P2 point mass): 0.414 at x = 1 and 29.0 at x = 30, independent of mass at fixed x; at fixed physical radius it goes as M_b^(-1/2) in the deep regime; at B's density edge it is 37-211 (x_e = 38 to 212 over 1e12 to 1e9, x_e going as M^(-0.25), from CFG251 via CFG70).
- **What the CMB needs, second hand:** a clustering a^-3 density with Omega_c h^2 = 0.1200 +- 0.0012 at z ~ 1100; smooth dust gives peak3/peak2 = 0.5545 against 0.9906, and z_eq = 3423 with it against 532 without (L121/L129 as quoted by CFG251; not re-read). CFG253's tolerance for continuous transfer is stricter (at least 97% of today's cold mass at z = 1090); this lane's line is the frozen 0.5.
- **Robustness:** R1 (requirement lowered from 0.1200 to 0.01, line 0.005): does not bite, as frozen (10^-1377.7 against 0.005). R2 (delta_ta(1100) = 0.5): does not bite (10^-307.1 against 0.060). The verdict is not a feature of the pass line or of the threshold.

## 4. The post-hoc extras (run after the stop; labelled; the frozen estimates compared in section 5)

Common toy (`CFG243_shells.py`, a fresh numpy leapfrog modelled on CFG118 / CFG7_common's shell code): 1-D spherical, baryon shells collisionless, a static core (M_pert plus the baryons inside the radius where the initial linear overdensity reaches 0.25), the REST of the matter smooth and not clustering, radiation neglected (a_i = 0.005). Its controls: the unperturbed flow stays on the Hubble flow to 1.5e-6; no theta_b zero occurs in it; the all-matter variant of the same code puts the zero-velocity shell at 11.79 against the committed GR top-hat 11.76 (0.3%). theta_b of a shell is d ln J/dt with J = r^2 |r_(i+1) - r_(i-1)|; the source fires at its first downward zero and creates dust Q m with Q = a0/(3 g_loc), g_loc the peculiar field at that moment (the AMT-2 closure).

- **G0.** theta_b = 0 is NOT the turnaround: in the toy it comes a median 0.60 of t_ta after the shell's zero velocity (p10-p90 +0.59 to +0.64), at r_theta0/r_ta = 0.856. The results at 1e9, 1e10 and 1e12 are identical because the baryon-shell infall without dust is self-similar in mass (turnaround scale M^(1/3), as CFG118/CFG158). Each inner shell crosses theta_b = 0 downward 21-24 times over 13.8 Gyr (hysteresis 0.01 / 0.05 / 0.2 give 19-24), so the unflagged source needs a counting rule; the first-crossing flag n is a prescribed label (CFG48 G3: PARTIAL; inside an action a history variable: FAIL). The Zel'dovich identity sum_i T_i = 3 at theta_b = 0 (T_i the contraction rate of axis i over H) means every non-spherical element still expands along some axis when the source fires (T_min < 1: 1.0000; T_min < 0.5: 0.998; an axis that never collapses: 0.88-0.90); sheets and filaments fire. The localised source also cannot be compensated by a pure Lorentz-invariant vacuum (CFG131 D1: d_mu rho_L = S c^2 u_mu needs grad theta parallel to u_mu; here the ratio of the actual gradient to the aligned value is 9.3e7). Causality and inertness pass.
- **AMOUNT.** For baryons uniform at turnaround the local closure rho_c/rho_b = a0/(3 g_loc) is exact (4e-16); for any other profile it is not (the closure is 2/3 of the target for rho ~ r^-1, 1/3 for r^-2, 0 for a point mass, and decays for the exponential spheres), and two systems with identical (rho_b, g_loc) differ in target by a factor 3.000 (the nonlocality of `ChainCert.Ownership`: `ownership_distinguishes`, `ownership_not_field_local`). The target keyed to the galaxy's present baryons needs the retained fraction (committed SHMR from h48: f_ret = 0.104 / 0.258 / 0.086 / 0.002 at 1e9 / 1e10 / 1e11 / 1e12). Survival in the shell toy (point cores; 1e9 and 1e12 at q_j = 0.1, 1e10 at q_j = 0.05 / 0.1 / 0.2 and on the alt footing): C_final/C_target is 0.11-0.31 at x = 0.11, 0.20-0.65 at x = 1.1 and 0.013-1.19 at x = 28; the median over x in [1, 30] is 0.94 (1e9), 0.87 (1e10), 0.37 (1e12), so the scale does not follow r_M (it follows turnaround). Scaling the creation by 0.25-2 never brings the largest deviation below 0.93. The dust itself moves the later turnarounds: the zero-velocity radius at a = 1 is 678 kpc with the source and 243 kpc without it.
- **HIERARCHY.** A satellite cloud of test particles with theta_b integrated exactly along trajectories (tangent dynamics): every particle fires in every row, so the count ratio with host / isolated is 1.000. The amplitude (through g_loc) falls to 0.047 at d = 30 kpc and 0.445 at d = 100 kpc from a 1e12 Msun point host and is 0.996 inside an extended host: an external-field-like suppression, not ownership. The first-crossing flag gives 0 by construction. For baryons that end in a 1e12 Msun system turning around at z = 0, an excursion-set walk puts the first turned-around system at a median 2.7e7 Msun (M_min 1e5; z about 6.9): only 0.16-0.21 first turn around in a system of >= 0.1 of the final mass. The first-crossing rule gives ownership to the smallest progenitors, the opposite of CFG251's top-level rule.
- **G3/G4.** The baryon equation has no source term (reaction 0). The rest-mass ledger is the obstruction: the vacuum energy in the turnaround ball is 1.17 M_b in CFG48's r_ta convention (mass independent), against 29.0 M_b of dust at x = 30 (f = 24.8); in B's committed r_ta it is 98 / 55 / 31 / 18 M_b (f = 0.30 / 0.53 / 0.93 / 1.65); CFG131's Lagrangian-volume ledger gives f = 1.71 at x = 30 and crosses 1 at x* = 20.2 (all reproduced). The implied local a0 shift f/2 must be <= 1e-2, i.e. f <= 0.02. CFG242 route A's ledger (at most 1.9e-4 of the ball's vacuum energy) is for the dust's HEAT; the rest mass is a different, larger number.

## 5. How the frozen hand estimates fared (kept, wrong ones included)

| estimate | frozen | result | |
|---|---|---|---|
| E1 supplied at z = 1100 | <= 9e-19 x 0.12 for sigma(M, 0) <= 100 | 10^-1377.7 (CLASS) | holds (far below) |
| E2 sigma needed | z = 0 equivalent 1.3e3, "40-45x" a ceiling of 30 | 1.08-1.11e3; x118-x283 the CLASS sigma(1100); CLASS sigma(1e5, 0) = 9.2, not 30 | right order; the "ceiling 30" was a memory number and not a CLASS value |
| E3 z = 10 | 0.011 (M > 1e8), 0.0022 (1e10); shortfall 9-55x | 0.0177, 0.0032; 6.8x, 38x; 0.0436 (2.8x) at 1e5 | wrong by 1.4-1.6x in abundance (the class supplies more than estimated; the 1e5 row was outside the quoted range) |
| E3 z = 2.5 | 0.085 / 0.071 | 0.0888 / 0.0719 | right |
| E4 acoustic theta_b/(3H) | <= 1e-3 | 2.4e-4 (rms 2.3e-4) | right |
| E5 baryon-only sigma_b(z = 0) | ~1e-2, ~100x short | 0.076, 16.8x short | wrong by 7.6x in sigma (still a FAIL) |
| memory M* | ~3e12 | 6.7e12 (CLASS) | wrong |
| P(COSMIC pass) | 0.003 | FAIL | as expected |
| E7 crossings per inner shell | >= 10 | 21-24 | right |
| E8 theta_b = 0 locus | r_theta0/r_ta 0.5-0.9; P(pass) 0.5 | r_theta0/r_ta = 0.856, but the TIME lag is +0.60 t_ta: 0.000 within 25% | the radius was in the range, the pass line (a time criterion) missed: kept as a wrong P |
| E9 non-3D-bound dust | >= 0.3 | 1.0000 (an identity within ZA) | direction right, magnitude stronger |
| E10 vacuum compensation | FAIL (P 0.05) | FAIL | right |
| E11 causality, inertness | PASS | PASS | right |
| E12 uniform exact; s = 2 off by a factor 3 | | exact; closure/target = 1/3 | right |
| E13 survival ratio | ~2.5, too heavy in the deep regime | 0.14-0.94 (median in [1, 30]), too LIGHT, mass dependent | **wrong in direction**, kept |
| E14 retention spread | >= 3, error >= 0.73 | 128 over 1e9-1e12 (10.3), 2.98 over 1e9-1e11 (0.73) | right (the 1e12 end dominates) |
| E15 unflagged host / isolated | 0.8-1.5 | count ratio 1.000; amplitude 0.047 / 0.445 / 0.996 | right for the count; **wrong for the amplitude at d = 30 and 100 kpc** (the closure's g_loc suppresses the amplitude in a strong host field) |
| E16 flagged | 0 / 1 by construction | 0 | right |
| E17 first-crossing mass | median <= 1e8, P(H3) 0.05 | median 2.7e7 (M_min 1e5), 1e8 (1e6), 5.6e8 (1e7); fraction 0.16-0.21 | right for M_min <= 1e6; wrong for 1e7 |
| E18 reaction | PASS | PASS | right |
| E19 energy | 1e6-1e8 x orbital | 6.7e5-1.5e9 (gross) | right order |
| E20 vacuum ledger | f_ta >= 6.7 (turnaround ball, CFG118 convention), CFG131 1.70 | 24.8 (CFG48 r_ta); **0.30-1.65 at x = 30 in B's committed r_ta** (5.4 out to r_ta); 1.706 (CFG131) | **wrong for B's convention** (three of four masses pass f <= 1 at x <= 30 there); the FAIL stands through CFG48's convention, the Lagrangian ledger and the a0-shift line |
| a0 shift needs f <= 0.02 | fails by >= 100x | fails by 15x (B, 1e9) to 1240x (CFG48) | partly wrong (15x in B's convention) |
| E21 constants | at least one enters | N enters COSMIC (strict) | right |
| joint P | 7.5e-9 | the first gate failed | |

## 6. MUTATE controls and robustness checks (frozen expected exit codes; observed)

| control | expected | observed | what bites |
|---|---|---|---|
| M1 z-independent creation (`CFG243_cosmic.py`) | 1 | **1** | C1 FAIL -> PASS (the whole 0.1200 at z = 1100, initial data = CDM with a vacuum origin story) |
| M2 evaluation at z = 0 | 1 | **1** | C1 FAIL -> PASS (0.1200 by the normalisation) |
| M3 non-local source (`CFG243_amount_posthoc.py`) | 1 | **1** | AMT-3 FAIL -> PASS for all 16 cells; the locality test PASS -> FAIL |
| M4 host-aware source (`CFG243_hierarchy_posthoc.py`) | 1 | **1** | H1 FAIL -> PASS (a prescribed label, not a mechanism) |
| M5 counting rule (`CFG243_g0_legality_posthoc.py`) | 1 | **1** | G0-b FAIL -> PASS (median crossings 22 -> 1) |
| M6 vacuum ball 1e3 times larger (`CFG243_g3g4_ledger_posthoc.py`) | 1 | **1** | L3 FAIL -> PASS (f(30) 24.8 -> 0.02), by non-locality |
| R1 requirement 0.01 | 0 (not to bite) | **0** | does not bite |
| R2 delta_ta(1100) = 0.5 | 0 (not to bite) | **0** | does not bite |

M3-M6 apply to the post-hoc scripts, because the frozen stop rule halted the lane before those gates; each still bites as frozen.

## 7. Failed controls, errors and wrong expectations (kept)

- **Harness bug in the MUTATE comparison.** The first M1 and M2 runs exited 0 (the control did not bite) because `Run.main_cells()` looked for `<slug>.json` instead of `<slug>_results.json`. I fixed the path and re-ran: both bite. The COSMIC main run was complete and unchanged before the fix.
- **A failed control, kept as reported.** The shell-toy control "the zero-velocity shell reproduces the committed GR top-hat contrast 11.76" FAILED on the class toy (9.69, -18%) because in the toy the rest of the matter is smooth and does not fall in. The same code with the shells carrying all the matter gives 11.79 (0.3%); that variant is the control that passes, and the failing class-toy row is printed beside it as a reported FAIL (`C2-toy`).
- **Code errors found and fixed before the final run (none changed a COSMIC number):** a softening of 0.02 kpc left the no-core Hubble flow at 5.3e-5 (the value 0.002 gives 1.5e-6); the shell code missed turnarounds that occurred in the second half-kick (events moved to the full-step velocities); the first G0-c detector control did not fire (an off-by-one in the cut-point slice); a numpy matmul warning on this machine led to explicit arithmetic in the Zel'dovich sampler; the first AMT-3 profiles were truncated inside x = 30 (re-truncated at 300 kpc); the h48 import needed `hunt_2026` on the path. Every one of these was found by a failing control or a printed anomaly, not by a result I preferred.
- **Wrong frozen estimates:** section 5 (E3 magnitude, E5, E8's pass line, E13's direction, E15's amplitude, E17 at M_min 1e7, E20 in B's convention, the a0-shift factor, M* from memory).

## 8. A source creating dust after recombination cannot supply the CMB-epoch cold matter

This is the plain content of the binding failure. The acoustic peaks need a clustering, pressureless component with Omega_c h^2 = 0.1200 present at z ~ 1100. A source that creates dust only when the baryon flow turns around creates it after the first halos form, which is long after recombination (the earliest turnarounds are at z of order 10 in the table above). If the dust were created after recombination as a second cold component beside a separate early one, the observables it would touch are: (i) the acoustic peaks, in particular the third peak (the clustering a^-3 density sets z_eq = 3423 against 532 without it) and the CMB lensing; (ii) linear growth at z >~ 10 to k = 30/Mpc (R05 / G2: the cold-early requirement, c_s^2 <= 4.6e-12), where the class supplies 3-36% of the cold mass at z = 10 in the generous reading and none before; (iii) BAO and RSD through the background; (iv) the high-redshift galaxy epochs (CFG197). In that reading the class is not a replacement for the cold mass: it adds a late galaxy-scale component beside the required cosmic one and reduces to candidate B's T4 (CFG251's own reduction); CFG253's reading (B) (early transfer completed before recombination) is the alternative, and it is CDM with a vacuum origin story.

## 9. Departures, ambiguities (labelled post hoc) and what is not covered

- **Verdict cell for COSMIC.** The frozen text lists M_min in {1e5, 1e8, 1e10} and a verdict cell; I used the most favourable of the three (1e5) for the verdict and report all three. The FAIL holds for each.
- **AMT-5 run set (a departure from the frozen full coverage; a FAIL needs one failing case).** Point cores only (the exponential-sphere core was not run); 1e9 and 1e12 at q_j = 0.1, 1e10 at q_j = 0.05 / 0.1 / 0.2 and on the alt footing; N = 1000 baryon shells. The creation-scale scan is a labelled extra (a scale is a constant). The closure Q = a0/(3 g_loc) with the peculiar field and the first-crossing flag is my reading of "AMT-2's closure"; a different amplitude rule is not covered.
- **G0-d operationalisation.** The frozen text gave no definition of "3D-bound" for the Zel'dovich toy. I chose: not 3D-turned-around if some axis still expands at the theta_b = 0 event (T_min < 1). With sum_i T_i = 3 that holds for every non-spherical element, so the number is 1.0000 by an identity, not by a statistic; the 0.88-0.90 fraction with an axis that never collapses (lambda_3 <= 0) is the sample-based statement. The ZA uses the Gaussian (Doroshkevich) eigenvalue sample at sigma_lin(M, z = 0) from CLASS; no N-body halo census was run.
- **H1 "created dust".** I scored both the amplitude-weighted amount and the number of firing particles; the pass line is missed in each. H2 takes the multiplicity from the G0-b shell toy because the single-stream tangent integration stops at the first caustic.
- **H3** uses uncorrelated (sharp-k) increments with sigma^2(M) from the top-hat window (the usual excursion-set approximation) and M_min in {1e5, 1e6, 1e7}.
- **L3 reading.** "f <= 1 for all x <= 30 in both conventions" is read as the dust within x r_M against the vacuum in the creation ball (the turnaround ball, in each r_ta convention) plus CFG131's Lagrangian ledger; it fails on CFG48's convention and on the Lagrangian ledger, and passes at x <= 30 for three masses on B's. L4 is scored strictly (N enters COSMIC, in the class's favour).
- **Not covered:** other source classes (a trigger other than theta_b, a non-Lorentz-invariant or dynamical vacuum funder, an action realising S, collisional dust); G5 (well-posedness, Solar System) and the perturbation-level G2 (growth to k = 30/Mpc, perturbation equations); non-spherical baryons (CFG44: a thin disc differs by 3-15x); gas physics and feedback in the toy; a relativistic completion; a Boltzmann (CMB) run of the source; the PAPER36 text beyond the rule's statement; L121/L129 and CFG7, CFG50, CFG60, CFG72, CFG158 (cited second hand through CFG251, CFG131 and CFG4). From memory and unverified: only the standard methods themselves (Press-Schechter, the Zel'dovich approximation, the Doroshkevich eigenvalue distribution), the Planck 2018 requirement value (in `CFG4_cosmology.py`), and the literature numbers quoted second hand above.

## 10. Files

Scripts (all exit as stated in `CFG243_run_all.sh`): `CFG243_common.py`, `CFG243_controls.py`, `CFG243_cosmic.py`, `CFG243_shells.py`, `CFG243_g0_legality_posthoc.py`, `CFG243_amount_posthoc.py`, `CFG243_hierarchy_posthoc.py`, `CFG243_g3g4_ledger_posthoc.py`, `CFG243_verdict.py`, `CFG243_run_all.sh`.
Outputs (each as `.out` and `_results.json`): `CFG243_controls`, `CFG243_cosmic` (and `_MUTATE_1`, `_MUTATE_2`, `_ROBUST_1`, `_ROBUST_2`), `CFG243_g0_legality_posthoc` (`_MUTATE_5`), `CFG243_amount_posthoc` (`_MUTATE_3`), `CFG243_hierarchy_posthoc` (`_MUTATE_4`), `CFG243_g3g4_ledger_posthoc` (`_MUTATE_6`), `CFG243_verdict`; `run_all.log` is the transcript of the last full run. The frozen file `CFG243_FROZEN_CRITERIA.md` is committed separately and is not part of this directory's install.

## In-place re-run (orchestrator)

`bash CFG243_run_all.sh` was re-run in this directory with `ZF_REPO` set (about 9 minutes; `run_all.out`; `classy` 3.3.4.0 as importable in the Python used; nothing downloaded or installed): `unexpected outcomes: 0`; the controls pass; COSMIC fails as the binding gate (frozen stop rule); the four later gates run as labelled post-hoc extras and fail; M1-M6 bite; R1 and R2 do not bite (as frozen). Every `_results.json` is identical to the author's apart from the `runtime_s` fields, and every `.out` apart from timing seconds. The frozen criteria are `../CFG243_FROZEN_CRITERIA.md` (7cc93bdef). The frozen file's note that no PAPER36 file was found is superseded by the disclosure above (the paper exists, DOI 10.5281/zenodo.23025372); the frozen file itself is not edited. Nothing here is closure, the cold mass is still required, kappa = 1/2 stays fitted, and there is no dark-matter particle.
