# Q3 -- Salam-Sezgin (6D N=(1,0) gauged supergravity) as a possible fixer of chat = g_6^2/kappa_6 and Lambda_6

Written 2026-09-28 BEFORE any script in this directory was written or run. Amendments are appended at the bottom, never edited above.
Convention for every script here: **the MUTATE control is triggered by the argv flag `--mutate`** (real run exits 0, `--mutate` must exit 1; outputs saved as `*.out` and `*_MUTATE.out`).
Scripts set `sys.dont_write_bytecode = True`; nothing is written outside this directory; no PDFs are kept here.

## What was read, and how (declared before any computation)

Primary sources were fetched as PDFs by the web-fetch tool (saved by the harness outside the repo) and READ AS PAGE IMAGES:
* Gibbons-Guven-Pope, hep-th/0307238 ("3-Branes and Uniqueness of the Salam-Sezgin Vacuum"), READ IN FULL through section 5's opening (paper pp. 1-8: the bosonic Lagrangian (2.1), field equations (2.2), the CC-vanishing argument (2.5)-(2.9), the local solutions (2.19)-(2.21), Dirac condition (3.3)-(3.11), additional gauge fields (4.1)-(4.4)). NOT read: appendix A (k != 0 solutions), the rest of section 5, section 6.
* Gibbons-Pope, hep-th/0307052 ("Consistent S^2 Pauli reduction of six-dimensional chiral gauged Einstein-Maxwell supergravity"), READ IN FULL for paper pp. 1-14 (bosonic Pauli ansatz (2.3)-(2.6), the 4D action (2.17)/(2.20), fermion ansatz and 4D SUSY rules (3.1)-(3.20), black-hole uplift (4.1)-(4.5), and section 5 up to (5.11): radius (5.1), rescaled couplings (5.2)-(5.4), extra 6D YM fields (5.5)-(5.7), KK masses (5.8)-(5.10), g_YM ~ M_K/M_Planck (5.11)). NOT read: the rest of section 5 (the cosmological-constant paragraph and the 3-brane/S^1/Z_2 discussion), section 6, the appendix.
* Aghababaie-Burgess-Parameswaran-Quevedo, hep-th/0304256 ("Towards a naturally small cosmological constant from branes in 6D supergravity"), READ pp. 1-11 (introduction; model (2.1) with kappa^2 = 1 and Weinberg conventions; S^2 compactification (2.2)-(2.3) with the conditions R_mu nu = 0, F_mn F^mn = 8 g_1^2 e^{2 phi}, f = n/(2 g_1 r^2), e^phi r^2 = 1/(4 g_1^2), n = +-1; the statement that N = 1 SUSY protects the flat 4D vacuum; brane coupling and SUSY breaking (2.4)-(2.10)). NOT read: sections 3-5 (4D vacuum energy, quantum corrections, explicit brane model, topological constraint).
* Aghababaie et al., hep-th/0308064 ("Warped brane worlds in six dimensional supergravity"): ABSTRACT AND TABLE OF CONTENTS ONLY.
* Salam-Sezgin 1984 (Phys. Lett. 147B, 47) and Randjbar-Daemi-Salam-Sezgin-Strathdee: NOT obtained. Everything attributed to them (N=1 4D SUSY of the S^2 vacuum, the 6D field content, the anomaly-cancellation condition n_H = dim G + 244) is taken from the three papers above, at the level those papers state it.
* Repo: ALPHA_CHAIN_STATUS.md, P_REPORT.md, F2 (script and .out), N1 (preregistration and n1_1 .out), D's `alpha_bar_checker.py` READ IN FULL / in the parts shown; F3 report and N1's other scripts NOT read.
* Not consulted at all: any modern review; the 6D SUSY transformation rules beyond those printed in hep-th/0307052 (3.1)-(3.2); the 6D anomaly polynomial and Green-Schwarz couplings (only the n_H = dim G + 244 sentence in ABPQ p. 6 is used).

RECALLED and to be labelled as such where used: nothing is used as a load-bearing input from memory except (a) the meaning of "unit-normalised su(2)" (T_3 = +-1/2 on doublets), (b) sympy/conventions of the reduction (checked by script where stated).

## Numbers and expectations known BEFORE this pre-registration (disclosed so nothing is presented as blind)

By hand (not a script), while reading the papers, I found: (1) at the vacuum the three 6D field equations (mu nu, ab, dilaton) are consistent for every constant dilaton value, giving R^2 = e^{p/2}/(8 g^2) (p = dilaton vev in the hatted 6D convention), f^2 = 16 g^2 e^{-p}, and the flux number g oint F / 2 pi = 1; (2) the SU(2) kinetic coefficient of the Pauli reduction splits as three equal thirds (metric, F_(2) flux term, H_(3) term), so the SU(2) coupling should be alpha_SU2 = 2 l_P^2/R^2 rather than lane F's 3 l_P^2/R^2 (which has no H_(3) term); (3) the 6D photon zero mode should be massive (Stueckelberg with B_{45}); (4) the vacuum energy is zero exactly; (5) the dictionary to lane F is chat = g_F^2/kappa_6 = 2 kappa_6 g^2 e^{-p/2} with lane F's Minkowski condition Lambda_6 = 2 g_F^2/(N^2 kappa_6^2) holding automatically at N = 1. These are EXPECTATIONS, not blind predictions; each script tests them and a miss will be reported as a miss.

## Hypotheses and exact pass/fail criteria

**H1 (Lambda_6 is tied).** In the Salam-Sezgin model the "cosmological" term is the potential 8 g^2 e^{-phi/2}, tied to the fermion charge g. PASS if a script shows (a) the 6D field equations on M_4 x S^2 with constant dilaton are consistent for all values of the dilaton vev, with V = 0 exactly, (b) the flux number is forced to 1 (no free flux integer) and it is the potential-charge relation (coefficient 8 g^2 with charge g) that forces it (MUTATE: coefficient 7 g^2 must break N = 1). FAIL otherwise. (Script q1.)
**H2 (chat is fixed).** PASS only if the vacuum conditions fix the dilaton vev p (equivalently the dimensionless chat = 2 kappa_6 g^2 e^{-p/2}). Expected FAIL: the critical set of the reduced potential is a curve. (Script q1: the critical set, its dimension, Hessian rank and the sign of the non-zero eigenvalue.)
**H3 (lane F/N1 S^2 relations are reproduced).** PASS if the SU(2) coupling extracted from the 6D action on the Pauli ansatz equals alpha_SU2 = 3 l_P^2/R^2. Expected FAIL (2 l_P^2/R^2). Sub-checks: the ansatz satisfies its own Bianchi identity dH = (1/2) F^F; the total kinetic coefficient equals the 4D coefficient of the source (2.17), e^{-phi} in units of the source's normalisation; the split into metric/F/H parts. (Script q2.)
**H4 (there is a massless U(1) with alpha_U1 = N^2 l_P^2/(2 R^2)).** PASS only if the l = 0 6D photon stays massless. Expected FAIL: Stueckelberg mass from H = dB + (1/2) F ^ A with B_{45}. Sub-check: compare the mass with the value the source states in (5.9); a mismatch is reported, not tuned. (Script q2.)
**H5 (flat direction).** PASS if the tree-level potential vanishes along the whole critical curve, its Hessian there has rank exactly 1 (one flat, one positive direction), and along the curve R/l_P is free (chat free) so alpha_SU2 = chat^2/pi^2 is free. (Scripts q1, q3.)
**H6 (natural integers give alpha).** Scored against lane D's bar (P < 1e-3 after look-elsewhere, miss <= 5e-10 or the route's own predicted precision, zero fitted reals, scale stated). Declared scored family, fixed now (16 trials in all; N = 1 is forced so it is NOT a trial; the dilaton vev is a free real):
  * T1, 7 trials: R set by the observed vacuum energy, M_KK^4 = rho_Lambda with R = c / rho_Lambda^{1/4}, c in {1/(2 pi), 1/2, 1/sqrt 2, 1, sqrt 2, 2, 2 pi}; prediction alpha_SU2 = 2 l_P^2/R^2 (Thomson value is the only target; the scale is mu = 1/R at tree level).
  * T2, 9 trials: chat set to a "natural" handle h in {1/(4 pi), 1/(2 pi), 1/pi, 1/2, 1, 2, pi, 2 pi, 4 pi}; prediction alpha_SU2 = (h/pi)^2 (N = 1).
  Also reported, NOT scored: the values of chat and R/l_P that alpha_SU2 = alpha_Thomson would REQUIRE (a requirement, not a prediction); the consistency of T1 with the source's statement (hep-th/0307052 abstract) that a KK scale of 1e-3 eV needs bulk couplings of order 1e-31.
  A planted match (alpha times (1 + 1e-3)) must be rejected by the bar (MUTATE loosens the bar and must then accept it).
  Verdict rule: a trial "hits" only if its miss <= 5e-10; anything else is a miss. The route as a whole is a LEAD only if a hit survives the bar; otherwise NEGATIVE. The identification of the SU(2) isometry coupling with the photon coupling is itself a declared assumption (N1 already found the SU(2) is a KK isometry, not the electroweak group); it is not scored as a trial.

## Scripts (declared list; nothing else is scored)

* `q1_ss_vacuum_and_flat_direction.py` -- H1, H2, H5 (checks A1-A8).
* `q2_pauli_su2_coupling_and_u1.py` -- H3, H4 (checks B1-B7).
* `q3_dictionary_and_scoring.py` -- dictionary to lane F, free-parameter table, H5 (alpha along the flat direction), H6 (checks C1-C8). It runs q2 as a subprocess (real mode) to read its coefficient, so it has no run-order dependence on saved files.
Controls: q1 `--mutate` sets the potential coefficient 8 g^2 -> 7 g^2 (SUSY tie broken); q2 `--mutate` drops the H_(3) term; q3 `--mutate` loosens the bar so the planted match is accepted. Each must fail at least one check and exit 1.

## Not tested and not scored (declared)

Fermion sector and anomaly cancellation beyond the n_H = dim G + 244 arithmetic; the Green-Schwarz mixing; brane/conical solutions and their tension constraints (ABPQ sections 3-5, hep-th/0308064); warped SLED solutions; quantum corrections and the mechanism that lifts the flat direction; the Salam-Sezgin theory's 7D or string origin (Cvetic-Gibbons-Pope, not read); non-abelian gauge couplings of extra 6D vector multiplets (their 6D couplings g' are free in the source and are not scanned); how the SM would be embedded.

## Amendment 1 (appended after the runs; nothing above was edited)

Disclosed deviations and slips:
1. Check numbering: q1 has A1, A3, A4, A5a-f, A7, A8 (A2 was merged into A1b/A1c and A6 into A5; no check was dropped). q2 has B1-B7 as listed plus B3a-c, B4a-c, B5a-b, B6b, B7a-b sub-checks.
2. q2 check B4c (the total kinetic density is independent of theta, i.e. the three pieces cancel the S^2 dependence) was NOT pre-registered; I added it after the first successful run printed a theta-independent total. It is post hoc, reported as a consistency check with the source's remark on the Pauli reduction, not as a test of a hypothesis.
3. q2's first attempt crashed (a tuple-unpack bug `kap2, = ...` and a missing `import sympy.combinatorics`); no physics was changed. q1 was edited once before its outputs were saved (a cosmetic rewrite of the R^2 solve line and of the sign expression for g A_phi in A4; the printed results are identical before and after).
4. q2 B7: I first expected a single Stueckelberg mass. The script computes it for both normalisations of the Chern-Simons coefficient (1/2 and 1) because the source's (5.9) mass (m^2 R^2 = 2) is 4x my naive value (1/2). The discrepancy is NOT resolved (see the note printed by q2); H4 does not depend on it (massive either way).
5. q3's cross-check against the source's abstract (KK scale 1e-3 eV -> bulk coupling ~1e-31) was registered as "reported, not scored"; it is implemented as a check (C3d) that only asserts agreement within a factor 10 of the order of magnitude.
6. The disclosed expectations (alpha_SU2 = 2, U(1) massive, chat free) all came out as expected; the only quantity that differed from what I would have guessed before reading was the size of the mismatch of the massive-photon coefficient (item 4).
7. Prereg said the bar would be applied with family size = trial count; q3 passes size = 16 to lane D's checker with 0 fitted reals (T1 and T2 have no fitted real: chat is set to a handle, not fitted).
