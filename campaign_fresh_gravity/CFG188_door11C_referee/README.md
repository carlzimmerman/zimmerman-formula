# CFG188 — Independent referee re-derivation of the physics core of CFG172 (door 11C): phase 2 results

Frozen criteria: `CFG188_FROZEN_CRITERIA.md` (sha256 704386f14fe200e2673854d34eba893a75e06ccf9cbf2141feb7d0e7c3886460; committed as "CFG188: frozen criteria", 0bea830bf). Scripts, outputs and result JSONs are in this directory (`<scratch>` until the orchestrator commits it); nothing in the repository was edited (`CFG188_common.py` imports CFG44's `Bcommon.py` read-only for nu_mono). kappa = 1/2 is FITTED. Literature facts are from memory or as the record quotes them, none re-read. No new data.

**Nothing here says the theory is closed, that the timelike-flow reading is refuted outside the frozen class, or that any data favour the framework. A scoped no-go is not a closure.**

Order of work (as frozen): my scripts R1-R4, the verdict script and all ten MUTATE controls were written and run and saved FIRST; only afterwards did I open `CFG172_door11C/*.py` (A1, A2, A3, A6, A7, common; not the .out/.json). What I learned from them is used only in the "classification" column and in the one departure script R3b (section 6).

## 0. Bottom line (plain answers)

1. **The tail bound: theorem or artefact?** A theorem of the band and of the kernel, given one premise, and the premise is now supported in the full local theory. Closed form: the smallest tail any kernel with (yq)' >= 0 can have inside a +-b band of the target is (1 - sqrt(1 - eps^2))/2, eps = 1 - b (sympy): 0.2821 a0 at 10%, 0.2000 at 20%, 0.0670 at 50%; the band would have to be **98.2%** (g allowed to be ~2% of the target) before the tail bound alone stops violating the Q2 tolerance (8.0e-5 a0). Kernel-robust: P2 0.28206, simple kernel 0.46754, nu_mono 0.42405 (lane 0.282 / 0.4675 / 0.424). The premise (yq)' >= 0 was only a decoupling-limit statement in the lane (metric held fixed, no theta channel). My R2.b (STRETCH, **DONE**) derives the scalar-sector quadratic action with the **metric dynamical** (unitary gauge, uniform-acceleration background, high k) and finds omega^2 = c2/(2+3c2) k^2 (1-kappa)/kappa, kappa = q sin^2 + (yq)' cos^2: for c2 > 0 the radial mode is stable iff 0 < (yq)' < 1, and c2 only enters as a positive prefactor, so it cannot cure a negative (yq)' (same conclusion as the record's PASS_KILL c^2_par). Caveats: local (WKB) analysis about a background that is not itself a solution, scalar sector only, 11C-a's a-channel, tadpoles dropped. **Not an artefact of the 10% band or of P2. Conditional on the local-WKB full-theory result only.**
2. **Is the strict G4 count for 11C-b overstated?** Yes, under my reading (classification: framing/definition, not an error; D-5 not triggered). The overall size of (c2, c14, M^2) is a redefinition of F's argument (sympy: F -> F/s leaves L invariant), and the dressing F' cancels in the theta^2 : a^2 coefficient ratio (-c2/c14). The physical objects are R = c14/c2 (fixed by rule T: 301.6 or 440.5) and the function F (declared). So "1 (overall size of c2)" is not a physical constant; strict count 0 beyond the declared function. Caveat: the lane's picture keeps F' = 1 at the cosmic background while its Newtonian continuation has F' = 0 for u < 0; under the Newtonian continuation the effective c2 at the cosmic background is zero, so that picture is not internally one consistent reading of "bare c2".
3. **Does dressing flip G6(b)?** It changes the size and the character of the failure, and the verdict then depends on one input. Undressed (the lane's): alpha_2 at the rule-T tie with c2 = 2.7e-5 is 2.6 against 1.6e-9 (a failure by ~1.6e9); the G6 x G7 region needs t >= 3.7e6. Dressed (c2 and c14 both multiplied by F' at the test system's own acceleration; quoted alpha formulas): alpha_2 becomes a bound on R (R q_p <= 1.6e-9) instead of on c2. With my pulsar-row acceleration (own acceleration G M_c/a^2, y_p = 8.5e10) alpha_2 at the tie is 1.8e-9 (R = 301.6) / 2.6e-9 (R = 440.5): a marginal FAIL (1.1-1.6x); with the relative acceleration the lane's A3 used (73 m/s^2, y_p = 7.8e11) it is 1.9e-10 / 2.8e-10: PASS. **CONDITIONAL**: G6(b) is not a clean fail under dressing, and not a clean pass either. The ambient-background reading (Solar System governed by the galactic y = 1.5) gives alpha_1 = -2.2, a FAIL, under either dressing; the lane's own README flags this as unresolved.
4. **Does the Newtonian-continuation t = 1.2e-6 reproduce?** Yes, on the branch the lane's solver picks: **1.24e-6** with the smallest root (start at y = y_N and go up, i.e. the Newtonian branch). With the largest (MOND-like) root the Newtonian continuation gives 4.27e-4, identical to the mirrored and the linear continuation. So the "continuation" only matters through branch selection, which also explains why the lane's M6 did not bite under the Newtonian continuation (both offsets sit on the Newtonian branch: deviation saturates at 0.967). Classification: definition (branch selection), not an error; lane's mirrored 4e-4 reproduces (4.27e-4).

Verdict per the frozen labels: AGREE 21, CONDITIONAL 5, NOT DONE 1, **DISAGREE 0** (D-1..D-5 not triggered). Per-row table in section 2.

## 1. What was re-derived, and where independence stops

Re-derived by me (own sympy/numpy): R1 static reduction from the unitary-gauge ADM action in areal gauge, nonlinear (metric, R3, Euler-Lagrange, first integral, exact Schwarzschild control, G_N = G/(1-c14/2) control, covariant aether radial equation, zeta R3^2 counter-term); R2 kinetic coefficients (decoupling limit), the full-theory local dispersion (R2.b), the tail bound in closed form, three Q2 recipes, EFE first-order remark; R3 11C-b (own static law with anchor u = y^2 - t, three continuations and branch selections, undressed and dressed G6/G7, redundancy, momentum-constraint structure, anchors, D1); R4 11C-c (lattice elimination, effective pressure, c_s^2, saturating coupling, retarded toy).

Independence STOPS (quoted, not re-derived): the action class as written in the frozen file; the CFG44 target definitions (P2, nu_mono, exponential sphere) and both a0 footings; Q2 <= 5.2e-27 s^-2, Saturn's distance (9.58 AU from memory; 9.54 AU as sensitivity), the ephemeris delta A_R bounds (quoted); alpha_1 = -4 c14, the alpha_2 formula, the PPN limits, and **KM1's G7 threshold c2 >= 2.7e-5** (my R3-S moving-source solve was **NOT DONE**; every G7 number here is QUOTED); Flanagan's condition and the record's c^2_par (R2.b is a check against them); G2, G3, G4-as-count, S1/S2 (not addressed); CV4's theta = 3H (only its divergence structure re-derived: K (c2 F' - 2/3) = const, so K is uniform to ~1%, not exactly).

**R2.b: DONE** (frozen outcome "SUPPORTS"). **R3-S: NOT DONE.** Recipe B of R2.d (apsidal precession) computed in arcsec/century only; **ratio NOT SCORED** (no reliable ephemeris precession bound from memory). E23 (UV structure of the 11C-c instability): **NOT DONE**; the toy has no k^4 term.

## 2. Row-by-row against the lane (each verdict per the frozen labels; class of each difference)

| # | item | CFG172 README | CFG188 | verdict | class of difference |
|---|---|---|---|---|---|
| 1 | G1-law P2 max dev (7 masses x point/exp x both footings) | 5e-14 | 1.2e-12 | AGREE | numerical (root-finder tolerance; an identity for spherical baryons) |
| 2 | G1-law nu_mono | 5e-6 | 8.7e-8 | AGREE | numerical |
| 3 | static reduction mu = 1 - q, Psi' = Phi' | mu g = g_N, Psi = Phi | derived; residual 0; Q'(y)/y = 2q | AGREE | none |
| 4 | Psi/Phi - 1 (exact areal-gauge A-equation at the leading solution; 6 sampled cells) | 0 (weak field) | 6.2e-6 (aether part 5.9e-7) | AGREE | framing (O(Phi/c^2) terms the weak-field Lagrangian drops; not a disagreement) |
| 5 | aether radial equation, static aligned u | not stated | vanishes identically; nabla u = -u a exactly (sigma = theta = omega = 0) | AGREE | new check |
| 6 | (yq)' for P2 | 1 - 2y/sqrt(1+4y^2) > 0 | same (sympy) | AGREE | none |
| 7 | radial / tangential kinetic coefficients | K_x = N(yq)', K_perp = N q | 2(yq)', 2q (sympy, generic q) | AGREE | none |
| 8 | full-theory stability (metric dynamical) | UNDEFINED / record c^2_par | omega^2 = c2/(2+3c2) k^2 (1-kappa)/kappa (**DONE**) | AGREE (SUPPORTS) | scope: supports the premise of the tail theorem |
| 9 | minimal tail P2 / simple / nu_mono, +-10% | 0.282 / 0.4675 / 0.424 a0 | 0.28206 / 0.46754 / 0.42405 | AGREE | none |
| 10 | Q2 / bound, Sun's own P2 tail: canonical / alt | 6.3e3 / 7.6e3 | 6.28e3 (9.54 AU: 6.31e3) / 7.59e3 | AGREE | numerical (Saturn distance input, 0.4%) |
| 11 | Q2 / bound, minimal-tail kernel | 3.6e3 | 3.54e3 | AGREE | numerical (same input) |
| 12 | Q2 recipes B, C for the minimal tail | not done | B: 1.8 arcsec/cy at Saturn (ratio NOT SCORED); C: 7.2e2 (Earth), 7.1e2 (Mars) against the quoted delta A_R bounds | AGREE in direction (>= 100) | new check |
| 13 | tail bound vs band | +-10% | robust to a 98.2% band | AGREE | new check |
| 14 | 11C-b G1 t_max, mirrored continuation | 4e-4 | 4.27e-4 | AGREE | numerical |
| 15 | 11C-b G1 t_max, Newtonian continuation | 1.2e-6 | 4.27e-4 (largest root) / **1.24e-6 (smallest root)** | CONDITIONAL | definition: root/branch selection |
| 16 | 11C-b t_min on G6 x G7 (undressed) | 4.0e6 | 3.72e6 | AGREE | numerical (the lane scans a 400 x 400 grid; mine is analytic: c14_max = 3.20e-9 at c2 = 2.7e-5; 7.9% apart) |
| 17 | gap G1 vs G6/G7, undressed | 3e12 (N), 1e10 (Mi) | 3.0e12 (N, smallest root), 8.7e9 (Mi) | AGREE | numerical |
| 18 | 11C-b gap, dressed reading | not computed | 3.8e3 (Mi; own-acceleration pulsar), 4.1e2 (Mi; relative-acceleration pulsar); 1.3e6 / 1.4e5 (N, smallest root) | CONDITIONAL | framing: depends on which acceleration the pulsar row uses |
| 19 | 11C-b "overall size of c2 free" (G4 strict = 1) | 1 | redundant (F -> F/s invariance) | CONDITIONAL | framing/definition (D-5 not triggered) |
| 20 | 11C-b G6(b) FAIL at every c2 G7 allows | FAIL | undressed FAIL; dressed: marginal FAIL (1.1-1.6x) or PASS (6-8x margin) depending on the pulsar acceleration | CONDITIONAL | definition (dressing reading), see 0.3 |
| 21 | 11C-b anchor at K_bg(z=0) | not considered | G1(b) passes at z = 0 (2e-10); then t(z) = E^2 - 1 = 2.2, 13.2, 67.8 at z = 1, 2.5, 5: G1 fails at z > 0 | CONDITIONAL | scope: the pincer is anchor-conditional |
| 22 | 11C-b D1 a_*(z)/a_*(0) | 1.79, 3.77, 8.29 | 1.79, 3.77, 8.29 | AGREE | none |
| 23 | 11C-b (y q_eff)' near the branch | negative above the branch for any t > 0 | true, but the wrong-sign band is ~t/2 wide in y (5e-4 at t = 1e-3) | AGREE | framing: narrow at the G1-allowed t |
| 24 | 11C-b theta uniform (CV4) | K = 3H within 1e-2 | K (c2 F' - 2/3) = const: -0.98% / +1.0% (R = 301.6), -0.68% / +0.69% (R = 440.5) | AGREE | derivation refinement (not exactly uniform) |
| 25 | 11C-c K_c, P, c_s^2 | 8 pi G beta^2 c^4/(c2 theta_L^2), -K_c rho^2/2, -K_c rho | same (lattice sympy; c_s^2 = -K_c rho exactly, P = -K_c(rho^2 - rho_bar^2)/2) | AGREE | none |
| 26 | 11C-c saturating coupling | F | c_s^2 < 0 at all 60 sampled densities | AGREE | none |
| 27 | 11C-c UV-unbounded growth | Gamma ~ k | toy has Gamma ~ k; k^4 regularisation not tested | NOT DONE | neither agreement nor disagreement |

## 3. Attack results (frozen procedures)

- **(a) class and gauge.** The covariant aether radial equation vanishes identically for the static aligned u and a generic F(a^2) (only the multiplier direction survives); the aether and khronon forms have the same static reduction; shear, expansion and twist vanish on static slices. Adding a zeta R3^2 term leaves the N-equation unchanged at leading order but changes the A-equation at leading order (the class is a declared choice; not derived). Terms in div a were not tested. Verdict: PASS for the class as a *declared* one; no error found.
- **(b) tail bound.** Section 0.1. Theorem of the band and kernel, conditional on (yq)' >= 0, which holds in the local full theory (R2.b).
- **(c) Q2 recipe and continuation.** For 11C-a the bound is continuation-independent (s(y) = y q(y) is non-decreasing for y >= 0.929). Recipes A and C give >= 7e2 for the minimal tail; recipe B not scored. For 11C-b the continuation matters only through branch selection (section 0.4).
- **(d) declared kernel.** The G1-law is an identity requiring the declared kernel: the reduced action determines q(y) and nothing else; swapping the simple kernel against the P2 target fails the 10% line (0.155). Hidden objects in 11C-a: 1 free function (F_a), 2 constants (a_* tied by rule T with kappa = 1/2 FITTED; c2 inert in the static sector), structural choices (c13 = 0, baryons only as source, minimal coupling, q >= 0).

## 4. MUTATE outcomes (all 10 run; exit 1 = the control bit)

| control | script | claim that had to fail | outcome |
|---|---|---|---|
| M1 drop (yq)' >= 0 | R2 | tail >= 0.2 a0 | bites (forced tail at y = 1e6 is 0; lower edge peaks at 0.282) |
| M2 band 99% | R2 | bound exceeds the Q2 tolerance | bites (2.5e-5 < 8.0e-5) |
| M3 kernel -> GR | R1 | G1-law | bites (0.967) |
| M4 q -> -q | R1 | G1-law and K_perp = q > 0 | bites (0.983; K_perp flips sign by formula) |
| M5 anchor at K_bg | R3 | G1(b) fails at z = 0 | bites (3.02 -> 2e-10) |
| M6 F-dressing | R3 | G6 x G7 region needs t >= 1e6 | bites (3.7e6 -> 1.6) |
| M7 c2 -> -c2 | R4 | c_s^2 < 0 | bites (c_s^2 > 0; psi kinetic coefficient negative: ghost) |
| M8 beta -> 0 | R4 | compaction force non-zero | bites |
| M9 drop the aether term in the derivation | R1 | derived law equals mu = 1 - q for q != 0 | bites (not a tautology) |
| M10 band on mu instead of g | R2 | 0.282 is definition-robust | bites (0.3209, +13.8%) |

Weak or definitional controls: M4's no-ghost half is by formula (K_perp = q), not re-derived in that script (R2.a derives it); M7's "ghost" half uses the R2.b psi kinetic coefficient 2(2+3c2)/c2 evaluated at -c2; M6 flips the region cell, not the "dressed pulsar alpha_2 passes at the tie" cell (that cell does not flip with my pulsar acceleration).

## 5. Failed controls, wrong expectations, departures (kept)

- **First R3 run exited 1** (`CFG188_R3_b_operating_point_FIRSTRUN_two_expectations_misfiled_as_controls.out`): two hand estimates were coded as reproduction controls, E20 (with a second sample point that lies outside the narrow wrong-sign band) and E17 (dressed pulsar row passes at the tie). Both are expectations, not controls; I added `Checks.expect` (recorded, no effect on the exit code) and re-ran. E20's statement is true (negative just above the branch) but the band is ~t/2 wide. E17 is wrong as an expectation (marginal FAIL with my pulsar acceleration).
- **Wrong or partly wrong expectations:** E2 (predicted 1e-5..1e-4; got 6e-6, mostly GR nonlinearity); E14 (I predicted my Newtonian-continuation number would be ~2-4e-4 and could not explain the lane's 1.2e-6: true for the largest-root branch, but the lane's value is the smallest-root branch, 1.24e-6); E17 (predicted 0.55 that dressing flips G6(b) to PASS: marginal fail with my y_p); E18 (predicted a dressed pincer gap ~15 from G7 alone: the dressed pulsar-row alpha_2 turned out to be the binding line, t_min = 0.18-1.6, gap 4e2-4e3); E23 (not done). Held: E1, E3-E10, E12, E13, E15, E16, E19-E22.
- **Departures from the frozen list/scripts:** `cfg188_common.py` and `run_all.sh` renamed `CFG188_common.py`, `CFG188_run_all.sh` (coordinator's naming rule); R1's "exact nonlinear solve on the grid" for the slip was done as the residual of the exact A-equation at the leading-order solution on 6 sample cells (M = 1e9, 1e12; x = 0.1, 1, 30), point mass only; the EFE remark is first order only; R3-S not done; recipe B ratio not scored; `CFG188_R3b_pulsar_sensitivity.py` added (section 6).
- **New observation, not scored:** in the full local theory the spin-0 speed is c_S^2/c^2 = c2/(2+3c2) (1-kappa)/kappa; with P2 (yq)' -> 1/(8y^2), so c_S grows like y: superluminal above y ~ 1/(2 sqrt(c2)) (e.g. 4e3 c^2 at y = 1e3, c2 = 1e-3). The lane recorded hyperbolicity and criterion B as UNDEFINED; criterion A (no superluminal cone) fails; whether criterion B holds was not tested (the foliation leaves are a time function, but I did not check compatibility with every characteristic cone).

## 6. Departure script: pulsar-row acceleration (written after reading CFG172 A3)

`CFG188_R3b_pulsar_sensitivity.py` (not in the frozen list; run after my main and MUTATE outputs were saved): dressed alpha_2 at the rule-T tie, R_max and t_min for the two pulsar accelerations: own acceleration (y_p = 8.5e10): 1.8e-9 / 2.6e-9, R_max = 273, t_min = 1.6, gaps 3.8e3 (Mi), 1.3e6 (N smallest root); relative acceleration as in CFG172 A3 (y_p = 7.8e11): 1.9e-10 / 2.8e-10, R_max = 2.5e3, t_min = 0.18, gaps 4.1e2, 1.4e5. Pulsar masses and period are from memory (unverified).

## 7. Files and re-run

Scripts: `CFG188_common.py`, `CFG188_R1_static_reduction.py`, `CFG188_R2_stability_tail.py`, `CFG188_R3_b_operating_point.py`, `CFG188_R4_c_response.py`, `CFG188_verdict.py`, `CFG188_R3b_pulsar_sensitivity.py`, `CFG188_run_all.sh`. Outputs: `CFG188_R{1,2,3,4}_*.out` and `*_results.json` (main and `*_MUTATE_<M>_*`), `CFG188_verdict.out`, `CFG188_verdict_results.json`, `CFG188_R3b_pulsar_sensitivity.out/_results.json`, `CFG188_run_all.out`, `CFG188_R3_b_operating_point_FIRSTRUN_two_expectations_misfiled_as_controls.out`, this README. Frozen: `CFG188_FROZEN_CRITERIA.md`.

Re-run (about 65 s; numpy, scipy, sympy; from this directory): `ZF_REPO=<repo root> bash CFG188_run_all.sh`. Main runs exit 0 iff their reproduction controls pass (all four do); MUTATE runs exit 1 when the control bites (all ten do); the verdict script exits 0. No absolute home path is printed or stored (`<repo>`, `<scratch>`).

**Once more: a scoped agreement with a scoped no-go on a frozen class is not a closure of the time-flow reading, and kappa = 1/2 stays fitted.**

## In-place re-run (orchestrator)

`bash CFG188_run_all.sh` was re-run in this directory with `ZF_REPO` set: the four main runs exit 0, all ten MUTATE runs exit 1 (bite), the verdict script and the R3b sensitivity script exit 0. Every `.out` and `_results.json` is identical to the referee's apart from timing lines; `CFG188_run_all.out` and the FIRSTRUN file (the first R3 run, which exited 1 because two hand estimates had been misfiled as controls) are the referee's, kept as produced. The frozen criteria are `../CFG188_FROZEN_CRITERIA.md` (0bea830bf). Independence stops at the action class as written, the CFG44 targets, the Q2 bound and ephemeris inputs, Flanagan / the record's c_par formula, and the quoted alpha1/alpha2 formulas and limits.
