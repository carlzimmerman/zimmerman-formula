# AR1_action_response: FROZEN CRITERIA, committed alone before any script or number of this lane

**Question.** DR8 measured, at one mass (1e12), that Blumenthal over-predicts contraction of an isotropic smooth core inside r0, and that exact adiabatic invariants (J_r, L, disc monopole) track the live halo, f 1.019 [0.965, 1.134], with no fitted number. DR8 carried only a table in r/r0 (Upsilon 0.42/0.43). Here Blumenthal is replaced by the exact action calculation at each object's own halo and baryons. Does that clear the record's lines?

**Record check.** No lane computes per-galaxy action response. DR8 part B is one mass; DR3 is Blumenthal and Gnedin on the monopole; UL1 and HM1 use Blumenthal, Gnedin or f_Q. HM1 is running native + Blumenthal clusters: not duplicated here. **Not blind:** DR8, DR3, NR3, UL1, UR1, UR3, LC1, HM1's criteria and their numbers were read. No outside AI input. kappa = 1/2 FITTED, unused. No a0 in the cold sector. Cold dark energy, never a particle. No LCDM input in a grade. Not theory closed. Nothing here says the data favour the framework.

## Rule. No new fitted number
- **Start.** Spherical, isotropic, in equilibrium: total density (1 + F) rho_0(r), baryons mixed with the cold share, f(E) by Eddington inversion. rho_0 is M0 from the record's path. F as the record's path passes it to `contract`.
- **Invariants.** Each orbit keeps J_r and L. Cold mass per orbit conserved. **End** potential: M_cold,f(r) + M_b(r), M_b spherical (monopole), held constant beyond the edge. Iterated to self-consistency (Young's scheme). This is DR8's `dr8_action.py` in orbit-quadrature form: a deterministic grid in (E, L/L_c) in place of sampled particles, weights 8 pi^2 L T_r f(E) dE dL, Newton on J_r(E) with dJ_r/dE = T_r/(2 pi), orbit-averaged mass deposit.
- **Hand choices that are numerics or are inherited, disclosed:**
  - Truncation at the record's edge (R200, r_ta) has no isotropic DF, so **DR8's taper** is used: rho continues beyond the edge with matched value and slope times exp(-(r - edge)/(0.1 edge)), to 2 edge. M_out = min(M_act, M0(edge)), Blumenthal's same cap, so no row gains cold mass over the record's budget. Negative f(E) is clipped to 0 and counted; reported.
  - Discretisation correction: M_out = M0 x [deposit in end state / deposit in start state], so zero baryons is an exact identity on the grid. Size of the correction reported.
  - A spherical isotropic start is itself an assumption: real halos are radially biased outside; the core shape is by hand (owner's rule N, no known origin, X81). This tests the response of the assumed core, not its existence.

## Runs. PRIMARY: hand core, EM1 map, NR2 medians, both backgrounds, f* 0.034, canonical
| Row | M_b |
|---|---|
| **ACT MONO-INV, PRIMARY** | true monopole: DR3's stars from SPARC's SB, bulge 1.4 U Vbul^2 r/G, gas from DR3's nonnegative V_gas inversion, pinned to 1.33 M_HI. Chosen because it is measured with no assumed gas shape; DR3 showed the exponential-gas row's low bins are a hand artefact |
| ACT MONO-EXP, reported | DR3's own primary: exponential gas |
| ACT v2r, reported | grader's v^2 r/G, same input as NR3, direct comparator |
| BLUM on each M_b | comparators; DR3's and NR3's records reproduced |

- SPARC: per-galaxy best U on UL1's engine (`ul1_core.py`, K1 there 0 against the grader), record grid 0.30-1.20 for the lines and wide grid for UL1's gate. The action response is computed on 17 log-spaced U nodes from 0.06 to 2.40 and interpolated in U in ln(M_f/M0) at each radius (check K6).
- LITTLE THINGS (uniform baryon sphere, as the record), groups (Hernquist, as the record), clusters (BCG in source and response, CN1's, S-core path of N through NF1's grader), X-COP (no BCG on disk, as the record). These have no disc, so no monopole correction exists.
- **Keys:** 15 keys, f* 0.034, both h, gas **+0.005** (GS4), by the same patch ZN1's grader uses on Mgas500 inside the X30 machinery, on N's S-core path. Also eRASS1's own gas, reported, the path NR3's and DR8's rows used, so they can be compared. +0.111 not run for this door.
- **Native shape:** SP3/UL1's `tot` map on EM1, ZN2's z = 0 table. Its Eddington f(E) is checked for positivity. If definable: SPARC, tilt, LITTLE THINGS, UL1's gate, by the same solver, compared with UL1's native Blumenthal row. Native groups, keys, X-COP NOT GRADED: HM1's cluster lane is native + Blumenthal and is read only.
- **UL1's measured-Upsilon gate**, as reported by `ul1_grade.py`'s `gate`: Taylor and GSWLC, ACT rows, reported beside the lines and not part of the label. 0.50-0.80 not moved.
- **UR3 weighing as corrected by UL1:** DiskMass r and MW class by SP3's/UL1's `w`, action response, c200 8.0 NFW and hand core, reported only, if the cost stays modest (else stated not run). An NFW start here is an isotropic NFW.
- **Effective response:** f_eff = (Q_act - 1)/(Q_blum - 1), same M_b, U 0.5, by V_flat bin, at 2.2 R_d and r/r0 0.25, 0.5, 1, 2, 4; both on MONO-INV. **Mass trend:** Spearman of f_eff(2.2 R_d) with V_flat, and the dwarfs (V < 100) vs L* (150-250) medians. Stated, whichever way it goes; it is no number added.

## Live validation at other masses (before graded rows are read)
DR8's kernel, DR8's setup and growth time (7.7 Gyr, isolated, linear), one seed each, disc and no disc, **arg mass 1e10 and 1e13**, same smooth core, EM1's inverse for M_d (background A), Kuzmin disc with a = median SPARC R_d of galaxies with M200 within 0.25 dex, softening 0.7 kpc x (R200 / 199.3 kpc), N 30,000. Modest means no more than about 3 CPU-h a run by a timing test; if it costs more, stated UNVALIDATED and only 1e12 stands.
- Line: f_A = (Q_live - 1)/(Q_act - 1), median over 2, 3, 4 R_d, inside **0.85-1.15** at each mass. Fail is stated as ACTION SOLVER NOT VALIDATED AT THAT MASS: any row depending on it can't be read as a win, and the label is otherwise unchanged. Blumenthal's f at the same radii reported. Poisson counts stated.
- Graded rows may compute alongside, but aren't read until this is written to `ar1_live.out`.

## Pass lines, the record's
SPARC rms <= 0.110 and Upsilon 0.50-0.80 both backgrounds; tilt <= 0.15 both; 15 keys |Z| <= 2 on +0.005; X-COP |mean| <= 0.05, rms <= 0.10; groups |Z| <= 2; LITTLE THINGS |median E| <= 0.10 both.

## Labels on the primary row
- **ACTIONS CLEAR**: all lines pass. Then verify as hard: rerun with taper 0.2 edge and doubled grid, LOW and HIGH NR2 inputs, DR3's EXP row, and state live validation.
- **MOVES AND FAILS [lines]**: Upsilon median differs from BLUM on the same M_b by >= 0.02 on a background, some line fails.
- **NO MOVE (<0.02)**: below that on both.
Any failed check: no verdict.

## Checks
- K1 baseline: harness EM1|blum, eRASS1 gas: keys preds, groups, X-COP, LT vs NR3 MEDIAN, |d| <= 1e-6. UL1 engine `hand_blum` vs UL1's rows, |d| <= 1e-6 on Upsilon, bins, tilt, rms. +0.005 Blumenthal vs HM1's S|blum|bcg preds at +0.005 if that file exists by then, else stated.
- K2 solver vs `dr8_action.py` at 1e12, same analytic start, same disc: |Q_new/Q_dr8 - 1| <= 0.01 at r/R_d 2, 3, 4 (<= 0.03 at 1, 6, 8, 10).
- K3 zero baryons, F 0: M_out = M0, |d| <= 1e-6, on core, native, clusters' M0.
- K4 point mass: DR8's K12 (M_p 0.1 M(<r0), harmonic core): inner slope within 0.05 of DR8's exact -1.41. And a Kepler check of J_r to 1e-3.
- K5 mass conservation and monotonic M_out on every graded call: counted; convergence last-pass change reported, line 1e-2 at r >= 0.1 r0.
- K6 U-node interpolation: on Blumenthal, nodes vs the full U grid, |d| Upsilon <= 0.005, bins <= 0.01. On action, 15 galaxies, full record grid: |d U| <= 0.01 for >= 90 %.
- K7 grid convergence: doubled (E, L, nodes) on 12 galaxies and 4 clusters: Q within 0.5 % at r >= 0.1 r0.
- MUTATE baryons x 2, separate output: Upsilon must move by >= 0.02.

## Expectation on record, mine
MOVES AND FAILS about 95 %. Upsilon about 0.40-0.46 on MONO-INV, below the line; 150-250 km/s about 0.36-0.45; tilt fails, about +0.1 to +0.3; LITTLE THINGS fails at about +0.12; keys 11-14 of 15 on +0.005, X-COP fails. Groups pass. Mass trend: f_eff at 2.2 R_d about 0.7-0.9 with no strong trend. Live at 1e10, 1e13: 70 % inside the line on both. ACTIONS CLEAR under 2 %.

One thread per process, nice 15; SIGTERM checkpoint and resume. Outputs small, caches and runs gitignored. kappa = 1/2 FITTED. Not theory closed.
