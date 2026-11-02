# Requirements v2: what any new framework has to do, 2026-11-02

Supersedes nothing on record: `REQUIREMENTS_2026-11-01/REQUIREMENTS_LIST.md` stays as written, and this extends it with what UX1-UX7, AF1, TG1, LW1 and the older frozen list (`campaign_fresh_gravity/closure_map/GATES.md`) add. The status board's tile list is folded in. Adopts no framework, grades nothing new. kappa = 1/2 FITTED. Footings never pooled: canonical 9.3603e-11 / alt 1.1312e-10 m/s^2. No dark matter particle. The cold sector stays retired. Not theory closed. Nothing here says the data favour the framework. Criteria: `FROZEN_CRITERIA.md` (42241594b2). **Not blind:** the law's numbers were known when these tolerances were set. Tolerances are in `tolerances.json`, committed with this file before any harness run.

**Columns.** *Measured, total error*: statistical and systematic in quadrature, from the named file. *New line*: |Z| <= 2 on that error, unless LINE ONLY (no measured value to set a Z, so the old line is carried). *Old line*: the frozen one, shown beside it, not moved. *Law*: record's reading, canonical / alt. Marks: **D** measured side disputed; **C:x** correlated within block x; **P** a term in the error is PROVISIONAL. Harness: **H** computed from g(Q), **Hf** only if the candidate supplies the named extra (vertical form, field equation), **N** NOT COMPUTABLE by this harness.

## A. Galaxies
| id | Must | Measured, total error | New line | Old line | Law can / alt | Marks | H | Source |
|---|---|---|---|---|---|---|---|---|
| A1 | Keep discs tight | no measured value; a scatter | LINE ONLY rms <= 0.110 | 0.110 (1.01) | 0.0541 / 0.0537 | C:sparc | H | FG1, CRG1 |
| A2 | Median Upsilon_3.6 | population line, not a measurement | LINE ONLY 0.50-0.80 | same; PAPER67 questions its lower edge | 0.52 / **0.44** | D, C:sparc | H | FG1 |
| A3 | No tilt with speed | 0; sigma median bootstrap, stat-only | \|Z\| <= 2 | \|tilt\| <= 0.15 | +0.02 / -0.02 | C:sparc | H | UR2, FG1 |
| A4 | Flat with surface brightness, V 60-120, Upsilon 0.50 | 0; bootstrap of slope, stat-only (n 47) | \|Z\| <= 2 | \|b\| <= 2 sigma | -0.016 +- 0.061 / -0.023 +- 0.063 | C:sparc | H | HS1 |
| A5 | Upsilon against measured stellar mass, 5 V bins, GSWLC | UL1's mu per bin; h = max(boot, 1.25 sig/sqrt n) + 0.04 in quadrature | \|Z\| <= 2 each | same (level) | 60-100 +3.4, 100-150 +5.6, then +1.6, +1.6, +1.9; alt in `ul1.out` | D (estimators), C:ups | H | UL1, UX5 |
| A6 | Same, Taylor | same | \|Z\| <= 2 each | same | NOT on level; needs +0.35 dex | D, C:ups | H | UL1, UX5 |
| A7 | Step in Upsilon, 100-150 to 150-200, no offset fixes it | UL1's step | \|Z\| <= 2 | same | fails, Z -2.1 to -3.7 across rows | C:ups | H | UL1, UX5 (rests on 23, 25 galaxies) |
| A8 | Little net contraction in spirals | f_Q 0.872 [0.54, 1.07], PZ1 0.946 [0.78, 1.08], f_B 0.753 [0.729, 0.777]; SPARC needs 0-0.2 | applies to any component that falls in | six of 75 RM2 cells | not needed: no component | | N, needs a live model | LC1, PZ1, DR8, RM2 |
| A9 | LITTLE THINGS, median E | 0; bootstrap with sE 0.075, stat-only | \|Z\| <= 2 | \|E\| <= 0.10 | -0.025 / -0.064 | | H | FG1, AF1 |
| A10 | IC 1613, i 48 | E 0; sigma 0.1503 = sE 0.075 + 15 % on V | \|Z\| <= 2 | \|Z\| < 2 on sE alone | -0.593 / -0.631; Z -3.94 on total, -7.9 on sE | D (inclination, HI holes) | H | UX4, RF2. Also printed at i 37.9, 34.4 |
| A11 | Dwarfs by class, with external field, solver E1 | E 0; sd + UX4's central-stack shift (bright M31 0.311, UFD 0.039, M31 others 0.020; classical and field stat-only). One-sided shift used two-sided, which is generous | \|Z\| <= 2 each, 5 classes | \|Z\| < 2 on sd | UFD +1.30, bright +0.55, others +0.97, classical +0.31, field +0.04; sd-only Z +6.76, +3.97, +2.71, +1.24, +0.53 | D (M31 orbit), C:dw | Hf (AQUAL form of the law only) | LW1, UX4 |
| A12 | Dwarfs, no field | same | same | same | +0.59, +0.23, +0.75, +0.24, +0.05 | C:dw | H | FG1, LW1 |
| A13 | Dwarfs, algebraic external field, any g | same | same | LW1's E2 | reported by LW1 | C:dw | H | LW1 |
| A14 | Dwarf flatness in host field | -0.05 +- 0.19 dex per dex; AQUAL says -0.76 | \|Z\| <= 2 | none | fails with its own field | C:dw | N | Z2, UX4 |
| A15 | Milky Way K_z(R0, 1.1 kpc), best in-prior cell | 66.4; sigma 3.98 = 2.2 + 5 % pad (X5's) | \|Z\| <= 2 | 66.4 +- 4.4 (2 sigma) | form A 83.5 in priors; form R 70.1 | D (Newtonian family inside the summary, PA1), C:mw | Hf vertical form | X5, LW1, UX5, PA1 |
| A16 | Milky Way gate: v_c, chi2_Kz, K(R0), Ou in priors | carried | LINE ONLY FEASIBLE IN PRIORS | same | form A, Q INFEASIBLE both; form R FEASIBLE, 1 / 6 cells | C:mw | Hf | LW1, UX5 |
| A17 | Milky Way K_z scale length | 2.72 +- 0.15 | \|Z\| <= 2 | not in the gate | form R 3.29-3.41, about +4 sigma | C:mw | N here | X5, UX5 |
| A18 | DiskMass r at 1.5 h_R | r target c, c 1.0-1.517: 1.2585, sigma from c half range / 2, 0.05 and bootstrap. **Wide on purpose: c is unsettled** | \|Z\| <= 2 | r 0.90-1.10, n >= 27 | form R 1.239 / 1.204 (old line FAIL); form A 1.477 | D (c, OD1 NOT SEPARATED; sources run 1.2-1.9) | Hf vertical form | LW1, OD1 |
| A19 | Upsilon at 3.6 from star counts, about ten discs | not measured | none | none | decides A5, A6 | open data | N | UX5 |
| A20 | a0 normalisation | g-dagger 1.20 +- 0.02 +- 0.24 e-10 | inside | same | 0.94, 1.13 | | N, declared a0 | GATES 1.03. Memory-free, older chain |
| A21 | BTFR, 124 clean V_flat | A_obs 52-59 | 0.053 dex | same | met, older chain | C:sparc | N, not wired | GATES 1.04 |
| A22 | Local a0, MeerKAT | +0.032 dex from SPARC | 0.15 line | same | pass | | N, not wired | PAPER60 |
| A23 | Tidal dwarfs; DF2, DF4 | Newtonian in host; contested DF | <= 2 sigma | same | grey: P4 -0.59, -1.66 ln with a screen | D | N | GATES 1.12, 1.14, status board |
| A24 | Coma UDGs (11) | +0.234 / +0.195 dex, 1.33 / 1.11 sigma | <= 2 sigma | same | older chain pass; S1 fails with field | | N | GATES 1.16, S1 |
| A25 | Outer globulars | M/L_V 1.0-2.5 | inside | same | not discriminating | | N | GATES 1.13, D10 |
| A26 | Early types: SLUGGS, X-ray ellipticals, SLACS | +0.097 (4.0 sigma) dynamical masses; +0.280 / +0.254; gap 0.15-0.17 | <= 2 sigma | same | SLUGGS fails, others marginal | D (IMF) | N | GATES 1.18-1.20 and its 09-28 note, CFG528 |
| A27 | Chae external-field signal; directional EFE | 4.08 / 4.29 sigma against e = 0; A-hat +2.95 (n 16) vs -1.70 +- 2.12 (n 25) | as lane | same | not decided, X36 NOT DIAGNOSTIC | D | N | GATES 1.15, 4.07, X36 |
| A28 | Binary galaxies | A in [0.80, 1.25]; 1.511 / 1.443 circular | undecided | same | undecided | D | N | GATES 1.17 |
| A29 | Environmental null | slopes +0.052 +- 0.043, -0.046 ... | no density fork | same | consistent | | N | GATES 1.24 |
| A30 | Isolated KiDS lensing, absolute chi^2 with 2-halo | 60 points, KiDS cov; dof 56. Z = (chi2 - dof)/sqrt(2 dof), cov only, no inventory term | \|Z\| <= 2 | CL2's rule compares with retired halos, so it can't serve a new framework; printed for the law | PASS on old rule; "no tested model fits in absolute terms" | C:lens | H | CRG1, KN1, BL1 |
| A31 | Lens amplitude by colour | law blue 1.016 +- 0.086 / 0.878; red 1.587 / 1.313; A = 1 | \|Z\| <= 2 | none | inventory-dependent | D (inventory), C:lens | N, no colour input wired | BL1, S2 |

## B. Groups, clusters, mergers
| id | Must | Measured, total error | New line | Old line | Law can / alt | Marks | H | Source |
|---|---|---|---|---|---|---|---|---|
| B1 | 63 groups, sigma against law | Z with 0.10 dex mass systematic | \|Z\| <= 2 | CONSISTENT | +0.31 / -0.31 | | H (no gas in table: gas-reading g is NOT COMPUTABLE) | FG1, LW1 |
| B2 | 20 X-ray groups | M_HSE/M_B within 2 sigma | same | same | R500 1.41 / 1.33; R2500 fails | D (HSE) | N | GATES 2.03 |
| B3 | Local Group zero-velocity radius | 0.93 +- 0.12 Mpc | R0 <= 1.17 | same | fails on halo-bearing B; law not graded | | N | GATES 2.04 |
| B4-B18 | **15 keys** G-IN-all, G-IN-Mall, G-MID-T1/T2/T3/b, G-OUT-all/T1/T2/T3/b/Mall/M1/M2/M3 | KiDS dDS on eRASS1 at measured gas +0.005 +- 0.017; Z stat-only (no budget on record) except M3 | \|Z\| <= 2, both h, both f* | same | 10 of 15; failing MID-T2, T3, b, OUT-M3, OUT-b | D (HSC, below), C:keys | H | LW1, NF1, BA1, GS4 |
| B19 | G-OUT-M3 on total error | Z_tot: s + gas + slope + m + n(z) + leak, M3A1 | \|Z_tot\| <= 2 | none | +3.80, +3.39 / +3.08, +2.71 | C:keys | H | LW1, M3A1 (terms built on canonical, carried to alt) |
| B20 | Joint chi^2 of the keys | BA1's R, recomputed per candidate | p >= 0.05 | JOINT PASS | 65.0, 3e-8 / 56.0, 1e-6 | C:keys | H | LW1, BA1 |
| B21 | Outer shear slope on gas mass | 0.90 +- 0.21; law 0.47 | \|Z\| <= 2 | none | -2.0 | C:keys | N, covered by B4-B18 | CFG687 |
| B22 | Temperature or gas | NOT SEPARABLE, F 0.52-0.60 | no line | none | open | open data | N | TG1, UX7 (gas against M500 NOT SEPARABLE too) |
| B23 | X-COP mean, x <= 0.75, log10(M_HSE / M_model) | 0; sigma = cluster scatter/sqrt 7 + 0.12 dex (LF1) used two-sided | \|Z\| <= 2 | \|mean\| <= 0.05 | +0.467 / +0.434 | D (HSE), C:xcop | H | LW1, LF1 |
| B24 | X-COP rms | no measured value | LINE ONLY rms <= 0.10 | same | 0.476 / 0.444 | C:xcop | H | LW1 |
| B25 | Deficit map on X-COP, dM/Mg, x 0.1-0.7 | 8.5, 8.0, 6.7, 5.2, 3.9; sigma = distance to LF1's bracket 5.7, 5.2, 4.3, 3.1, 2.1 (no other term on record) | \|Z\| <= 2 each | none, a measurement | law Q = 0 by definition, a miss in every x | D (HSE, HSC 1.7), C:xcop | H | LM1, GM1 |
| B26 | Deficit map on KiDS, Q by radius | 7.5 +- 2.0, 7.4 +- 1.6, 6.7 +- 1.3, 5.0 +- 1.1, 2.9 +- 1.1 at 0.26-1.18 Mpc | \|Z\| <= 2 | none | Q = 0 | D, C:keys | N, projected Q not wired; keys carry it | LM1 |
| B27 | HSC against KiDS | A 0.650 +- 0.075 frozen, biased low; 0.746 +- 0.091 unbiased, with 0.1 sys: 2.8, 1.9 sigma | **OPEN DATA: not a candidate test** | UNRESOLVED | factor 1.7-2 is an amplified 25 % mass gap (UX3) | D | N | UX3, GM1 |
| B28 | Bullet, map | peaks on galaxies, M300 3.5, 2.3e14, sign of dkappa | UX6's FAIL rule, plus M300 \|Z\| <= 2 at 15 % | UX6's | FAIL; M300 1.11, 0.73; dkappa -0.068, -0.111 | P (15 % and position sigma are X32's PROVISIONAL), C:bullet | H, static, baryons only | UX6, X32 |
| B29 | 72 collisions; cluster counts | not scored on record | none | none | NS | D | N | GATES 2.05 |

## C. Local and relativistic
| id | Must | Measured, total error | New line | Old line | Law | Marks | H | Source |
|---|---|---|---|---|---|---|---|---|
| C1 | Planets: radial anomaly at Earth, Mars, Saturn | M1's bounds, recovered as anomaly / ratio | anomaly / bound <= 1 | same | 1.0e4, 6.4e4, 1.3e4 / 1.2e4, 7.7e4, 1.5e4 x | C:solar | H | M1, UX1 |
| C2 | Cassini Q2 | (1.6 +- 1.8)e-27 s^-2; Hees line 9e-27 in UX1 | <= 5.2e-27 (GATES), 9e-27 (UX1), both shown | same | 2.44-4.59 / 2.85-5.19 x the line | C:solar | N: needs a field equation | E2, UX1, PAPER67 |
| C3 | PPN gamma, Cassini | gamma - 1 = (2.1 +- 2.3)e-5 | \|Z\| <= 2 | same | no graded number | | N | GATES 4.01, 4.03 |
| C4 | PPN beta, alpha1, alpha2 | pulsar and ephemeris limits | as limits | same | no action | | N | GATES 4.04, X15 |
| C5 | Tensor speed | c_T = c to 1e-15 | same | same | no graded number | | N | GATES 4.02 |
| C6 | Binary pulsars | double-pulsar precision | as P3 | same | no graded number | | N | v3s verdict P3, X16 |
| C7 | Wide binaries | Gaia DR3 contested, boost 1.0-1.4; DR4 2026-12-02 sealed | Arm by prereg | same | open | D | N | GATES 4.05, 4.06 |
| C8 | Preferred frame: a0 not tracking CMB-frame speed | | none | none | NS | | N | GATES 4.08 |
| C9 | Black holes, neutron stars | shifts small | as P3 | same | no graded number | | N | status board |

## D. Cosmology
| id | Must | Measured, total error | New line | Old line | Law | Marks | H | Source |
|---|---|---|---|---|---|---|---|---|
| D1 | **Matter term, UX2's requirement** | omega_x 0.1197 (cells 0.1196-0.1199: spread, not an error); 5.35 x baryons, an output; rho_x = 2.249e-27 (1+z)^3 kg/m^3; 2.92e-18 at z 1090, 2.62 x radiation | LINE ONLY inside the spread; on families run | RF5 window | **no term.** No-dust control plik 128270 / 605, BAO 30443 / 13 | | N; a declared value reads READ, never PASS | UX2, RF5 |
| D2 | Gravitates as dust by | z_on >= 3e4 (grid edge; line near 22 against 25) to 1e6 | LINE ONLY | same | none | | N, same | UX2, RF5 |
| D3 | How dust-like | VOIDED: K2 failed in UX2. Pointer only, w order 1e-3 or below, c_s^2 order 1e-6 or below | no line | none | none | | N | UX2 |
| D4 | Must stay out of galaxies or not contract: A8 against D1 | the central conflict | no line | none | carries no term | | N | list row 4, 11 |
| D5 | Rederive the ruler | a0 reads rho_total or rho_DE through this term; r_d 147.07 assumes it | stated derivation | none | circular, UX2 | | N | UX2, CFG689 |
| D6 | Raw plik-lite | /605, native background | p >= 0.05 | RF5 | no pass without dust | | N | RF5, BOLTZ1 |
| D7 | BAO, SN | /13, /1819, native | as RF5 | RF5 | law's band depends on the cold mass | | N | RF5, CFG689 |
| D8 | Growth: shear xi+ /101, sigma_8 | on RF5's window | as RF5 | S - S_min <= 25 | a0 absent in linear FRW | | N | RF5, v3s F3 |
| D9 | CMB lensing | Planck 1.011 +- 0.028, ACT 1.013 +- 0.023 | \|Z\| <= 2 | same | no graded number | | N | GATES 3.02 |
| D10 | BBN | G_cosmo/G > 0.9611; dN_eff; needs K_B < 0.078 in AeST's premise | LINE ONLY | C2, C7 | no term; v3s radiation era fails | | N | UX2, v3s Q6, Q7 |
| D11 | Forest | P1D raw. NOT DIAGNOSTIC for every model run: 424.0/327, 1864.2/690; no absolute line can be set | none, forward model required | older 0.10 (3.12), retired | no graded number | D | N | RF5, P1D4, BOLTZ1, FOREST_KILL_AUDIT |
| D12 | a0(z) | 0.91 [0.76, 1.03] z 1, 0.94 [0.71, 1.12] z 1.5, 0.91 [0.33, 1.21] z 2.33; a0 prop H is 1.76, 2.35, 3.49. 1.97 sigma | not decidable: needs 0.055 dex at z 1 | CFG689 | open | D (uses the cold mass) | N | CFG689, PAPER67 |
| D13 | High z, ALMA, CRISTAL | U4 2026-11-06, GS4 2026-11-28 sealed; one disc excludes nothing | sealed | same | open | | N | PAPER66, ledger |
| dropped | GATES 3.01's Omega_c h^2 = 0.1200 +- 0.0012, S8 >= 0.752, "LCDM background to 1 %" | **Not carried:** LCDM inputs and yardsticks, against the 10-25 rule. D1, D6-D8 replace them | | | | | | owner 10-25 |

## E. Theory
| id | Must | Line | Law | H | Source |
|---|---|---|---|---|---|
| E1 | One explicit action giving every row from one field content | stated, with g derived, not posited | none. UX1: 10 candidates, only K8 reaches CONDITIONAL LEAD, v3s + a separate dust | N, candidate must supply | UX1, GATES 5.01, v3s verdict |
| E2 | Exact law in isolated discs, or a stated, computed departure | recovers row A1-A4, A9 | by definition | H through A rows | UX1 G1 |
| E3 | Planets and law together | T-B: one convex field can't roll over; T-A: positive spectral weight can't weaken toward short range; both in stated class | fails | N | UX1, M1 |
| E4 | No ghost or gradient instability, all backgrounds in reach | stated calculation | none | N | UX1 G3, GATES 5.02, H1 |
| E5 | Well-posed; causality; global time if k^4 | stated | none | N | GATES 5.04, I1, UX1 T-C |
| E6 | Strong coupling above scale of use | stated | none | N | GATES 5.03 |
| E7 | Radiative stability | stated | none | N | status board (G12) |
| E8 | Matter conservation | Noether identity | NS | N | GATES 5.06 |
| E9 | Counted degrees of freedom; Newton and G recovered | stated | none | N | GATES 5.05, 5.09 |
| E10 | Zero-field limit | stated | isolated controlled | N | GATES 5.08 |
| E11 | Caustics, if a single-stream field | no folding, no new constant unstated | v3s STRUCTURAL GAP | N | v3s X14 |
| E12 | Selector, if any switch | not label-like: closed on inputs tested: potential, sigma, acceleration, environment, epoch, gas state, bars, surface brightness. Harness tags reads of labels [LABEL] | none needed | H (tag) | list, AF1, UX3 |
| E13 | Local in present gas can't work in mergers; a nonlocal carrier must be named | UX6 | law n/a | through B28 | UX6 |
| E14 | kappa, or a0, derived or declared fitted | declared | FITTED, 537 attempts | N | PAPER67 |

## Collisions a candidate has to get through (not rows; carried from the list and updated)
A8 and D1: dust in the CMB falls into galaxies. A2, A5: Upsilon line and measured masses disagree, and fixing one with an offset doesn't fix the step A7. A15 and A18: no one form clears both weighings. B19 and B4-B18: pushing M3 down raises OUT-all (UX3, UX7, 14 of 15 is cheap: UX7's MUTATE reached it). B4-B18 and B23: keys want k above X-COP's (UX7). Discs and clusters: any gas tie needs a switch, and none is separated from "not a cluster" (UX3); AF1: what ranks high across samples is sample identity. B28: a term on present gas fails the Bullet even when it gets the mass right (UX6).

## Correlation blocks
sparc A1-A4, A21; ups A5-A7; dw A11-A14; mw A15-A17; lens A30, A31; keys B4-B21, B26; xcop B23-B25; bullet B28; solar C1, C2. X-COP and keys are not independent of each other through GM1's result, and UX3's k was fitted on X-COP. Joint numbers treat blocks as independent and say so.

## Coverage
Older list and board folded row by row. Opened: the lanes named. A lane read only by title could add a row, as the 11-01 list said.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
