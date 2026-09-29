# N1 -- joint coupling over-determination (pre-registration)

Written 2026-09-28 BEFORE any script in this directory was written or run. Amendments are appended at the bottom, never edited above.
Branch (from the red team's list, item 1): score (alpha_Y, alpha_2, alpha_3) TOGETHER. A map that fixes several couplings from few parameters is
over-determined: it can be killed by the RATIO test even though alpha alone could be fit by a free modulus.
Convention for every script in this lane: **the MUTATE control is triggered by the argv flag `--mutate`** (real run exits 0, `--mutate` must exit 1; both outputs saved,
the control as `*_MUTATE.out`). Scripts set `sys.dont_write_bytecode = True`; nothing is written outside this directory.

## What was read, and how (declared before any computation)

READ IN FULL: `ALPHA_CHAIN_STATUS.md`; `F_kk_stabilization/F0_PREREGISTRATION.md`; `f2_flux_freund_rubin.py` and its `.out` (the source of the S^2 relations);
`B_rg_asymptotic_safety/rg_common.py`; `D_calibration_bar/alpha_bar_checker.py`.
READ IN PART: `D_PREREGISTRATION.md` (first ~150 lines, i.e. definitions and the bar), `f3_light_charged.out` (last ~50 lines), `G0_PREREGISTRATION.md` (first 80 lines),
`g4_unification_running_and_handles.out` (first 60 lines), `M_red_team/m1_lane_a_running_check.out` (first 40 lines).
NOT READ: lane A's script, lane B's b1-b3 scripts, lane C, E, H, I, J, K scripts (only their summaries in the status file).
RECALLED (not re-checked from a source, and labelled RECALLED wherever used): the SM two-loop gauge coefficient matrix and top-Yukawa coefficients; the Dirac zero-mode counts
(S^2: |Q| zero modes forming spin (|Q|-1)/2; CP^2 spin^c: dim Sym^k(C^3) = (k+1)(k+2)/2 with flux m = k + 3/2); the Fubini-Study normalisations (checked by script where stated).

## Numbers known BEFORE this pre-registration (disclosed so nothing is presented as blind)

From lane M / lane G outputs: one-loop SM with measured couplings at m_Z gives alpha_Y^-1(m_P) = 55.48, alpha_2^-1(m_P) = 49.46, alpha_em^-1(m_P) = 104.94; the SM one-loop
alpha_1 = alpha_2 crossing is at ~1e13 GeV with alpha_3 off by -13%. By my own quick mental arithmetic (not a script) alpha_3^-1(m_P) ~ 52, so the three SM couplings
(with alpha_Y in the Q = T_3 + Y normalisation) are within ~12% of each other near the Planck scale. That near-equality is therefore KNOWN, and any map that predicts it
(e.g. all three couplings equal in Y-normalisation) would be POST-HOC; it is reported descriptively only and is NOT scored.

## Part I -- what lane F's S^2 relations are, exactly (n1_1_s2_rederive.py)

Setting (from f2 B3): 6D, action R/(2 kappa^2) - Lambda/kappa^2 - F^2/(4 g^2), M_4 x S^2 (radius R), integer flux oint F = 2 pi N for a unit-charge field, Minkowski point of the radion
(V = 0 and V' = 0, i.e. Lambda_6 = 1/(2R^2), R^2 = N^2 kappa^2/(4 g^2)). F derived the SU(2) coupling only for the U(1) Cartan fibration (d phi + A dy) and the U(1) for the 6D Maxwell zero mode.
Independent re-derivation (not a re-run of f2): for each of the THREE SU(2) generators use 1/g_a^2 = (1/(2 kappa^2)) Int |K_a|^2 + (1/g^2) Int mu_a^2, with K_a the Killing vector and mu_a the
(traceless, adjoint) moment map of the flux (i_K F = -d mu), which is the SU(2)-covariant statement of the flux term; U(1): 1/g_U1^2 = Vol/g^2.
* I1  |K_a|^2 average = 2R^2/3 and <mu_a^2> = N^2/12 for a = x, y, z (isotropy), no K-mu cross term, no SU(2)-U(1) kinetic mixing (Int mu_a = 0).
* I2  alpha_SU2 = 3 l_P^2/R^2 and alpha_U1(unit charge) = N^2 l_P^2/(2 R^2) at the Minkowski point (both agree with f2 B3d/B3e; f2 is also run and its PASS lines checked).
* I3  general geometric formula alpha_geo = 4 l_P^2/<|K|^2>: reproduces S^1: 4 l_P^2/R^2 (AH6/F) and the S^2 geometric half 6 l_P^2/R^2 (the flux piece doubles 1/g^2 at Minkowski).
* I4  the ratio alpha_U1/alpha_SU2 = N^2/6 does not contain chat = g^2/kappa (the ONE free real of the map); alpha_SU2 = 3 chat^2/(2 pi^2 N^4).
* I5  chirality/content lattice (spinor zero modes RECALLED, counting identities checked): a charge-q spinor sees monopole charge Q = qN and has |Q| zero modes with SU(2) spin (|Q|-1)/2,
      so dim_SU2 = |qN| and the U(1) charge of every doublet has |q| = 2/N, of every singlet |q| = 1/N.  Test: can ANY assignment of SM left-handed Weyl hypercharges
      (Q 1/6, L -1/2, u^c -2/3, d^c 1/3, e^c 1) satisfy |Y_doublet| = 2 |Y_singlet| with Y proportional to q?  Declared expectation: NO.
* I6  scope statement: tree level at the compactification scale mu_c = 1/R; radion (l = 0) direction only (hep-th/0205080: fluxed dS_p x S^q are generically unstable in other modes);
      needs Lambda_6 tuned to 2 (R/l_P)^2 x ~ 3e-119 of its value; chat free; 4D gauge group SU(2) x U(1) only (no SU(3)); the S^2 SU(2) is a KK isometry, not the electroweak one unless declared.
MUTATE (n1_1): drop the flux term of 1/g^2 (or flip the moment-map normalisation); the identity alpha_SU2 = 3 l_P^2/R^2 must then FAIL.

## Part II -- the maps that are scored (declared list; nothing else is scored)

Common: x = (l_P/R)^2, l_P^2 = G_4 (M_P = 1.220890e19 GeV, un-reduced, as in F/AH6). Scale of every coupling: mu_c = 1/R (lightest KK mass); for products mu_c = 1/R_max
(1/R_min reported as a sensitivity, not an extra trial). ONE real is fixed by data in each map: the overall scale, by requiring alpha_2^-1(mu_c) [measured, run from m_Z] = the map's alpha_2^-1 at that mu_c
(one equation, one unknown R; it is the map's free modulus). Everything else is a PREDICTION.

* MAP A (S^2 flux, lane F): predicts alpha_Y/alpha_2. Two identifications, both declared:
    A1 unit-charge identification Y = q: alpha_Y/alpha_2 = N^2/6 for N = 1..6 (6 trials);
    A2 doublet rule (hypercharge coupling read off a chiral SU(2) doublet with |Y_d|): alpha_Y = 2 x/Y_d^2, alpha_2 = 3x for Y_d = 1/2 (leptons) and 1/6 (quarks) (2 trials);
       equivalently sin^2 theta_W = 1/(1 + 3 Y_d^2/2).
  8 trials, one ratio each.
* MAP C (D = 10 product M_4 x CP^2 x S^2 with ONE 10D Maxwell field carrying flux N_1 on CP^2 (Fubini-Study scale R_1, holomorphic curvature 4/R_1^2) and N_2 on S^2, Lambda_10, integer/spin^c fluxes):
  isometry SU(3) x SU(2) x U(1). Minkowski conditions U = 0, dU/dR_1 = dU/dR_2 = 0 solved for (R_1, R_2, Lambda_10) (cross-checked against the 10D Einstein equations in the script).
  Predicts alpha_2/alpha_3 and alpha_Y/alpha_2 (Y = q identification). Family: N_2 in {1..6}, N_1 in {1/2, 1, 3/2, ..., 6} (half-odd values are the CP^2 spin^c shift, RECALLED)  = 6 x 12 = 72 pairs, 2 ratios each.
  Also computed and reported, NOT scored as a trial: the content lattice (colour triplet needs q N_1 = 5/2 and singlet 3/2 with q N_2 = SU(2) dimension) -- whether ONE (N_1, N_2) can host Q, L, u^c, d^c, e^c.
  Also reported: alpha_3 = alpha_2 requires (N_2/N_1)^2 = ?  (a derived value; not a trial).
* MAP D (SU(5)/SO(10)/E6 forced level structure, lane G): k_Y = 5/3 derived from traces (Y = diag(-1/3,-1/3,-1/3,1/2,1/2)); alpha_1 = alpha_2 = alpha_3 at ONE scale M_G with two fitted reals
  (alpha_G, M_G) and ONE prediction: the alpha_3 mismatch at the alpha_1 = alpha_2 crossing. SM desert (1 scored trial). The MSSM (M_S = 1 TeV) is run as a COMPARATOR only: its spectrum is an insertion the
  framework does not derive, so it is reported and not scored.
* MAP E (S^1 KK, alpha_n = 4 n^2 x): one U(1); charges n only rescale alpha, no independent second coupling => no over-determination. Structural statement only, 0 scored trials.
Total scored trials: 8 (A) + 72 (C) + 1 (D) = 81. Not tested and not scored: D = 11 M^{pqr} Freund-Rubin spaces with SU(3) x SU(2) x U(1) isometry (needs the C_3 mixing; a background with
|Lambda_4| ~ 1/R^2, i.e. ~120 decades from the observed value); Salam-Sezgin-type SUSY completions that might fix chat; string-derived Kac-Moody levels other than 5/3.

## Part III -- the joint scorer (n1_3_running_scorer.py, n1_lib.py) and the bar for ratios

Running: one-loop (rg_common inputs: 1/alpha(m_Z) = 127.930, sin^2 theta_W = 0.23122, alpha_s = 0.1180, m_Z = 91.1876; alpha_Y^-1 = alpha^-1 cos^2, alpha_2^-1 = alpha^-1 sin^2), coefficients
b = (41/6, -19/6, -7) for (Y, 2, 3) derived from field content and checked; two-loop with the top Yukawa (RECALLED coefficients; validated by reproducing lane B's 0.5-0.7% two-loop shift of alpha_em^-1(m_P)).
Running variants (5): 1L-A, 2L-A (central), 1L-B (lane G inputs 127.955, 0.1179), 2L-B, 1L-A with the top decoupled below m_t.
* delta_run,j = max_variant |r_j / r_j(2L-A) - 1|.  Threshold uncertainty from UNKNOWN new charged states is NOT bounded; it is quantified as a sensitivity (shift of each 1/alpha per extra multiplet and the
  number of extra unit-hypercharge Dirac fermions needed to bridge a claimed miss).
Bar for a joint ratio test (declared conventions):
* J1 accuracy: |r_pred/r_meas - 1| <= tol_j with tol_j = max(2 delta_run,j, 0.01) for EVERY ratio j of the member.
* J2 look-elsewhere: lambda = N_trials * prod_j (2 tol_j / ln 100) (log-uniform prior on each ratio over [0.1, 10]; ln 100 is a declared convention), P = 1 - exp(-lambda); need P < 1e-3.
* J3 forcedness: no fitted real beyond the ONE overall-scale equation above, and every ratio independent of chat.
* J4 scale stated (mu_c) and any threshold/two-loop error larger than tol_j is stated; a pass at a level the running cannot resolve is a LEAD, never evidence.
* Bar for the OVERALL alpha (lane D): miss <= 5e-10 or a stated predicted precision; the maps here fix ratios only, so the overall coupling stays the free modulus and cannot clear it (stated).
Verdicts per map: KILL = no member passes J1 (the ratio prediction is contradicted); LEAD = some member passes J1 but P >= 1e-3 or J3 fails; EVIDENCE = J1-J3 all pass (not expected).
Controls in n1_3: positive control (a synthetic map defined as the model's own 2L-A ratios, family size 1) is accepted; negative control (same ratios perturbed by 8%, family 72) rejected;
b_Y = 3/5 b_1 (the lane A bug) must FAIL the field-content and alpha_em^-1(m_P) = 104.94 checks (that is the `--mutate` mode).

## Hypotheses (declared, can be false)
* H1 (I1-I4): the S^2 relations re-derive exactly; ratio alpha_U1/alpha_SU2 = N^2/6.
* H2 (I5): no SM hypercharge assignment satisfies the doublet/singlet lattice of the S^2 map.
* H3 (A1, A2): alpha_Y/alpha_2 at mu_c ~ 1e18 GeV measured ~ 0.9 (one loop); none of N^2/6 (N=1..6) is within 10% (nearest N = 2 at 0.667 or N = 3 at 1.5); A2 gives 8/3 and 24, factors ~3 and ~27 off. All expected to FAIL J1 beyond any running uncertainty.
* H4 (C): the Minkowski conditions decouple, R_i^2 proportional to N_i^2, so alpha_2/alpha_3 = C0 (N_1/N_2)^2 with a derived constant C0; with 72 members some land within tol of the measured ratios by chance and the family cannot reach P < 1e-3 at tol >= 1%.
* H5 (C content): no single (N_1, N_2) hosts Q, L, u^c, d^c, e^c (four different N_1/N_2 ratios are required).
* H6 (D): the SM desert alpha_3 mismatch at the alpha_1 = alpha_2 crossing exceeds 5 delta_run (expected -13% one-loop); MSSM comparator passes at ~1% but is not scored.
* H7: two-loop shifts of the ratios at ~1e18 GeV are 0.3-3%; threshold uncertainty from O(1) extra multiplets is ~5-10% and unbounded in general, so ratio tests at 1e18 can kill but cannot confirm.
* H8 (bottom line, expected): NO branch of this lane yields a forced principle fixing a gauge coupling; the S^2 map is killed by content and ratio; map C is not scoreable or is killed by content; alpha_2 is fixed only by chat.

## Everything that will be run (declared list)
n1_1_s2_rederive.py (7 checks I1-I6 + f2 run); n1_2_product_maps.py (CP^2/CP^1 checks, Minkowski solution cross-checked vs Einstein equations, couplings, content lattice, family table);
n1_3_running_scorer.py (RG validation, variants, scorer controls, threshold sensitivity); n1_4_score_maps.py (maps A, C, D, E scored; verdicts). Support library n1_lib.py.
Count: 4 scripts + 1 library; 81 scored trials as listed above; every other number is a derivation or a reported sensitivity.
Amendments follow.

## Amendment 1 (appended after n1_1, n1_2, n1_3 were run; nothing above was edited)
* n1_2 (first run): my hand expectation of the moment-map coefficient (c = 1) was wrong; the solver returned c = 1/2 for i_V omega = -d mu0 with omega of holomorphic curvature 4 (so the adjoint moment map of F = 2 N omega is N <z|T3|z>/<z|z>).
  The first run therefore failed four checks (G4a, G4c, M1c) and gave alpha_3 = 32/5 l_P^2/R^2 and C0 = 5/4. The script was corrected to use the solved c (not tuned to a target: the independent S^2 result of n1_1 is what G4c/M1c reproduce).
  Corrected result: alpha_3 = 16 l_P^2/R_FS^2, alpha_2/alpha_3 = (1/2)(N_1/N_2)^2. The mutated normalisation (F = N omega) fails G3, G4c, M1b, M1c as required.
  Also removed two trivial `True` checks in n1_1 (now printed as NOTE lines) and made M4b test the actual claim (only (u^c, d^c) share a required N_1/N_2).
* n1_3 (first run): two of my own descriptive expectations were wrong and are amended, not hidden. R4a expected delta_run 0.1-5%; alpha_Y/alpha_2 has a running spread of only 0.08% at 1e18 GeV
  (alpha_2/alpha_3: 1.6%) so the lower bound is dropped. R5a expected that a factor-3.5 uncertainty in mu_c moves the ratios by < 2%; it moves alpha_Y/alpha_2 by 3.7% and alpha_2/alpha_3 by 1.5%, more than the running spread.
  Consequence for the bar: H7 ("two-loop shifts 0.3-3%") was wrong for alpha_Y/alpha_2. J1 is scored under BOTH tolerances: the pre-registered tol_j = max(2 delta_run,j, 1%) (primary) and an EXTENDED tol_j^ext = max(tol_j, scale ambiguity of
  the mu_c identification, factor 3.5) (robustness; it can only help a map pass, so a kill that survives it is stronger). P (J2) is reported for both.
* Trial counts are unchanged (81). No hit has been seen at this point; n1_4 has not been run.

## Amendment 2 (appended after n1_3 and BEFORE n1_4 was written or run; nothing above was edited)
Because n1_2 showed that alpha_Y/alpha_2 = N_2^2/6 does not depend on N_1 (so every Map-C member is judged by the same six numbers on that ratio), I add a fairness variant so that a kill is not an artefact of the hypercharge identification Y = q:
* C* (normalisation-free variant of Map C, REPORTED with its own P): the hypercharge normalisation s in Y = s q is left free, so alpha_Y/alpha_2 is NOT scored; only alpha_2/alpha_3 = (1/2)(N_1/N_2)^2 is scored, 72 trials of ONE ratio, primary and extended tolerance. It cannot be a derivation (s is a free real); it is scored to show whether the colour/weak ratio alone is informative.
* Descriptive rows (not trials): the inverse requirement (N, Y_d or N_1/N_2 that would be needed); the number of Y = 1 Dirac fermions at 1 TeV that would bridge each alpha_Y miss; the Planck-scale near-equality of (alpha_Y, alpha_2, alpha_3) is printed and flagged POST-HOC, not scored.
* Map D tolerance: tol_D = max(2 delta_run,D, 1%) with delta_run,D the largest deviation of the alpha_3 mismatch among the 5 running variants from the 2L-A value (absolute, in units of the fractional mismatch).
Total scored trials remain 81 (A 8, C 72, D 1); C* re-uses the 72 members and is reported alongside, not added.

## Amendment 3 (appended after n1_4 was run; nothing above was edited): hypotheses scored against the numbers
* H1 TRUE (n1_1: 20/20 real, 18/20 under --mutate; also agrees with f2's B3d/B3e). H2 TRUE (no two SM fields share |Y|/dim_SU2).
* H3 TRUE: alpha_Y/alpha_2 at mu_c = 1.02e18 GeV (R = 12.0 l_P, fixed by alpha_2) is 0.829; N^2/6 gives 0.167, 0.667 (-19.6%, nearest), 1.5 (+81%), ...; A2 gives 8/3 (+222%) and 24. Need N = 2.23 or Y_d = 0.897.
* H4 PARTLY FALSE: the decoupling and alpha_2/alpha_3 = (1/2)(N_1/N_2)^2 are as predicted (the constant C0 = 1/2, not known in advance), alpha_U1/alpha_2 = N_2^2/6 independent of N_1; but I expected some members to land within tolerance by chance
  and NONE did (joint 0/72 primary, 0/72 extended; C* 0/72). The chance-expected number for C* was lambda = 0.98, so 0 is not surprising.
* H5 TRUE (only (u^c, d^c) share a required N_1/N_2). H6 TRUE: the SM-desert alpha_3 mismatch is -11.6% (two loop; -13.2% one loop), 3.8 x tol_D; the MSSM comparator at one loop is -1.4 to -4% (not scored).
* H7 FALSE for alpha_Y/alpha_2 (running spread 0.09%), TRUE for alpha_2/alpha_3 (1.6%); the mu_c ambiguity (3.7%) and thresholds (one Y=1 Dirac fermion at 1 TeV: -12.7% on alpha_Y^-1) dominate. H8 TRUE.
* Post-hoc, NOT scored: (i) a larger Map-C* lattice (N_1 up to 14.5) contains members within 3% of the measured alpha_2/alpha_3 (e.g. (13, 9) at -0.3%); (ii) alpha_Y^-1, alpha_2^-1, alpha_3^-1 at m_P are 55.1, 49.1, 52.9 (max/min 1.12).
