# Lane P -- claim-level audit of ALPHA_CHAIN_STATUS.md

Pre-registration: `P_PREREGISTRATION.md` (written before any check ran; Amendment 1 lists the visible deviations). Scripts (each with a MUTATE control that exits 1, `.out` saved):
`p1_consistency.py` (hashes, names, quoted numbers, counts, verification note; 76 checks), `p2_rerun_all.py` (re-run of all 47 scripts of lanes A-M and AH1-AH6 in a scratch copy, compared with the committed `.out`),
`p3_independent_numbers.py` (40 checks that recompute numbers from stated inputs, no lane script imported), `p4_lean_rerun.py` (Lean AH3 and its MUTATE file).
Nothing outside this directory was written; no existing file was edited; lanes N1-N5 were not opened (one docstring line of an N4 script appeared in a grep, disclosed in the amendment).

## Bottom line

The document is sound in substance. Of 49 audited statements: **32 SUPPORTED AS WORDED, 15 OVERSTATED (wording only; none changes a verdict or reopens a branch), 2 UNSUPPORTED** (a factual sentence about control exit codes, and an unscripted plausibility rating). Every number in the document reproduces: all 47 scripts re-ran with exit 0 and output identical to the committed `.out` at 1e-9 (P2, including AH2 and AH4, which lane M did not re-run); 46 controls behaved as recorded; Lean AH3 compiles (ten axiom lines, standard axioms only) and its MUTATE file fails at the committed three lines; P3 recomputed the quoted numbers independently (40 checks) and P1 found no missing hash or file.

The wording problems that matter most:
1. **Verification note is false as written.** "Every control exits 1" fails for AH1, AH2, AH4, AH6 (they print "control works" and exit **0**); AH5 has no control; lanes K and M are missing from the invocation list.
2. **"Ten independent routes"** is nine routes plus the bar (lane D proposes nothing); they share inputs.
3. **AH6 row**: "derived by computer algebra" covers only the F^2 coefficient and mode operator on a one-component background (normalisation is a hand premise); "R = 23.41 l_P" omits the scale (lane F T5: with one-loop SM running to M_KK the same relation needs R = 20.7 l_P).
4. **Lane C**: the "1/alpha_em ~ 107 at the cutoff" residual mixes in SU(2), which cannot emerge; the emergence residual is 1/alpha_Y = 59.8.
5. **Lane E**: "Lambda and kappa never enter" is true by construction of the model class (check C1c is vacuous).
6. **Red-team bullets**: "the bar is right" (only counts were reproduced); the MacDowell-Mansouri bound is for SO(4,1) only.
7. **Lane K**: "no published claim clears the bar" covers 16 audited claims, three from summaries/abstracts, under a visibly relaxed K11 rule; six named claims were not audited.

## Re-run results (P2, P4)

* 47/47 real runs: exit 0, output equal to the committed `.out`. 46/46 controls: recorded exit code and matching `.out` (42 exit 1; AH1, AH2, AH4, AH6 exit 0 by design; K's extra `--mutate-s2` exits 0 and changes nothing). AH5: no control.
* Lean: `lake env lean AH3_alpha_nogo.lean` exit 0, ten `#print axioms` lines identical to `AH3_alpha_nogo.out`; MUTATE file exit 1 with errors at lines 18, 26, 39. The file declares **11** theorems (`obs_rescale` is not axiom-printed), the document says ten.

## Table of audited statements

Class: SUP / OVR / UNS. Flags: **R** = rests on a fact the lane labels recalled / abstract-only / snippet-only / from a transcribed PDF; **NT** = hypotheses a reader might assume tested were not (details in the consolidated list). "Evidence" is file:line of the deciding script/check.

| ID | Statement (short) | Evidence (file:line) | Regime actually tested | Class | Flags |
|---|---|---|---|---|---|
| S01 | (c,G,Lambda): no dimensionless number | `ah5_dimensional_obstruction.py:47` (D1) | Buckingham nullspace over (M,L,T): monomials only | **OVR** | NT |
| S02 | + hbar: exactly one, x = 2.85e-122 | ah5:57 (D2), :93 | same | SUP | |
| S03 | alpha independent second group once a charge exists | ah5:74 (D3) | rank{x, alpha} = 2, Gaussian e^2 | SUP | |
| S04 | a0 chain "cannot output alpha" | ah5 whole; D's bar | dimensional analysis only; pure numbers (Z, kappa, pi) not covered | **OVR** | NT |
| S05 | pair-production factor depends on e only via lambda; alpha free | `ah1_schwinger_ds2.py:176` (C5), C0-C4 | dS_2, minimal scalar, planar patch, k>0, external field, tree factor | SUP | NT |
| S06 | Lean: "ten theorems, standard axioms, controls fail" | `AH3_alpha_nogo.lean`, `p4` | implication under the premise + identities; premise not certified | **OVR** | |
| S07 | sigma/H = alpha G(m/H), no conductivity tie fixes alpha | `ah2_induced_current_ds2.py:192` (V5), `ah4_induced_current_ds4.py:217` (V4) | ties sigma/H = c, six c, mu in {0.3..5}/{0.5..5}, criterion: mass-independence | SUP | NT |
| S08 | dS_4 heavy fields fall as a power ~0.124/mu^2 | ah4:176-181 (V2) | closed form (transcribed), slope -2.008 on mu = 10..40; direct sum validates to mu <= 3 (ah4:147) | SUP | R, NT |
| S09 | ln(m/H) term = one-loop running, alpha enters as input | ah4:197 (V3) | coefficient identity; "so" is the prereg reading rule | SUP | R |
| S10 | alpha_n = 4 n^2 lP^2/R^2 "derived by computer algebra" | `ah6_kaluza_klein.py:58,72,79-86` | K1, K2 by sympy on A_y(x) background; K3 normalisation hand-set | **OVR** | NT |
| S11 | needs R = 23.41 lP, 5.2e17 GeV, electron 1e-21, alpha traded for R | ah6:103,133; `f3_light_charged.py:26,130` | untwisted S^1 (F3 adds twist, bulk mass); scale not stated | **OVR** | NT |
| S12 | "Ten independent routes" A-J | route table row D | nine routes + bar; shared inputs | **OVR** | |
| S13 | the bar: P<1e-3, miss<=5e-10, 0 fitted reals, scale | `D_PREREGISTRATION.md`, `alpha_bar_checker.py:1-20` | declared conventions; "predicted precision" clause omitted | SUP | |
| S14 | A: inequalities / alpha-free / re-expression / n ~ 3.5e61 | a1, `a2_dirac_extremal_and_handles.py:63-80,89`, `a3_...:70-85` | classical RN-dS, minimal magnetic extremal BH, WGC/FL as inequalities | SUP | R, NT |
| S15 | B: truncation-dependent bounds | `b1_reproduce_literature.py:114`, `b3_...:60` | EH-type published fixed points reproduced; truncation dependence quoted from 2508.03563 | SUP | R, NT |
| S16 | B: SM charged content gives alpha^-1 ~ 75-77 | `b3_forced_vs_required.py:39-40` (C3, C4) | HR NGFP2 toy, nine charged fermions only, no W/Higgs, two mass sets | **OVR** | NT |
| S17 | B: needs Planck-scale alpha^-1 ~ 105 | `b2_required_boundary.py:74,93` | SM one-loop from m_Z, no thresholds; content-dependent (em-only toy 61) | SUP | NT |
| S18 | C: inequalities or alpha traded for count N | `c1_...`, `c3_...:63` (C3d) | N in {28,118,126}, three conventions | SUP | R, NT |
| S19 | C: fermion-only toy misses ~1.9x | `c2_emergence_species.py:54-60` | 1.91-1.95 across N | SUP | |
| S20 | C: proper SM chain leaves ~107; 8.6 extra fermions; walled masses | `m4_lane_c_content_and_cutoff.py:32-37` | one loop, U(1)_Y only, unit-Y Dirac at 1 TeV | **OVR** | NT |
| S21 | D: no derivation, the standard to clear | D prereg | -- | SUP | |
| S22 | E: freedom moves into B_F(phi); Lambda, kappa never enter | `e1_coupling_function_freedom.py:35,87,99` | one scalar, B_F(phi), extremum; C1c vacuous | **OVR** | NT |
| S23 | E: fitted-exponent families need w ~ -1; B3 allows 1+w ~ 0.25 at zeta < 6.5e-8 | `e2_variation_bounds.py:89-94,B4` | x prop. rho_DE, constant w; clock bound only | SUP | NT |
| S24 | F: R ~ 1e30 lP from Casimir + Lambda; ~115 decades | `f1_radion_circle.py:83,106-107` | 5D circle, massless-field Casimir, dof list, radion only | **OVR** | NT |
| S25 | F: Freund-Rubin: free 6D ratio, tuned Lambda_6 | `f2_flux_freund_rubin.py:34,186,208` | S^2 (n=2), one flux integer; n=3 potential cross-check only | **OVR** | NT |
| S26 | G: integers, ratios; overall coupling free | g1-g5; G0 Amendment 1 | anomaly/Dirac/instanton/CS/GUT traces/S-duality; three checks are structural | SUP | NT |
| S27 | H: alpha traded for string scale/dilaton/thresholds; O(1) convention unresolved | h1 (rank 3), h3, `h4_...:50-52` | tree level + one-loop, three sources' conventions; D1c NOT MET (3.3x) | SUP | R, NT |
| S28 | I: bands 100s-1000s x 1e-3, HH extremum scheme choice | `i4_widths_and_verdict.py:48`, i3 V2f/V2g | six criteria; O(1) constants; two-loop QED vacuum energy | SUP | R, NT |
| S29 | J: alpha^-1 = (N_eff/3pi) ln + const; FL1 cannot supply | j1, j2, `j4_fl1_supply.py:8-9` | induced photon, hard cutoff, NJL/BCS, neutral FL1 | SUP | R, NT |
| S30 | Common finding (same non-derivable objects) | synthesis | nine routes | **OVR** | |
| S31 | "Nothing in the record does this" | synthesis | record excludes N1-N5 (pending) | SUP | |
| S32 | dS_2 toy caveat | AH1 Amendment 2 | -- | SUP | |
| S33 | untested list | AH/lane scope-outs | true but not exhaustive | SUP | NT |
| S34 | zeta<4e-9 unreconciled with 6.5e-8 | e2:93 ; p3 | recomputed 6.504e-8 | SUP | |
| S35 | post-hoc remark VOID; 104.94, k=5.12, Z 12-13% away | `m1_lane_a_running_check.py`, a3:77, p3 | 13.0% of k, 11.5% of Z | SUP | |
| S36 | several lanes abstract/recalled | each prereg reading log | -- | SUP | |
| S37 | disclosed slips list | amendments A, E, F, H, I | list incomplete, all named items confirmed | SUP | |
| S38 | verification note: every control exits 1 | p1, p2 | contradicted for AH1, AH2, AH4, AH6; AH5 none; K, M unnamed | **UNS** | |
| S39 | header: every line points to a script or source; K, M reported | p1 | Salam-Sezgin recalled; M's ratings; conventions | **OVR** | R |
| S40 | M re-ran all clean (AH2/AH4 not) | p2 | all 47 reproduce | SUP | |
| S41 | M lane B: universal f sign; 0.18% for 1e-3 | `m2_...`, p3 | 0.18% is for alpha_Y(173 GeV) | SUP | NT |
| S42 | M lane C: 0.6% self-consistency shift | m4; p3 (0.62%) | one loop, U(1)_Y | SUP | |
| S43 | M: MacDowell-Mansouri ~ (16/3) G Lambda ~ 1e-121 | `m3_ds_gauge_coupling.py:47-49` | SO(4,1) EH+Lambda action, normalisation factor 0.01-100 | **OVR** | NT |
| S44 | M lane D: independent counts; "the bar is right" | `m5_...:63+` | counts reproduced (E1(12) exact, E2(6) 7e-5) | **OVR** | |
| S45 | M Lean: no_alpha_from_obs adds no physics | AH3 lean; p4 | true; premise is external-field, tree-level | SUP | |
| S46 | M Salam-Sezgin recalled | doc's own label | untestable | SUP | R |
| S47 | five branches "all LOW plausibility" | -- | judgement, no script | **UNS** | |
| S48 | K: misses/sigmas; "no published claim clears the bar" | k1, `K_REPORT_TABLE.md`, p3 | 16 claims, 3 from summaries/abstracts, K11 rule relaxed, 6 unaudited | **OVR** | R |
| S49 | K structural scores; JBW 3/4 dead in QED; BSBM no value; mutate-s2 null | `k2_structural_scoring.py`, table | anthropic and Reinisch (2/4) unlisted in document | SUP | R |

(Count: OVR 15, UNS 2, SUP 32.)

## Proposed corrected wording (every OVR and UNS statement)

* **S01** "From (c, G, Lambda) no dimensionless monomial (product of powers) exists."
* **S04** "The a0 chain has neither hbar nor a charge, so by dimensional analysis alone it cannot produce alpha; a pure-number function of its dimensionless constants (Z, kappa, pi, integers) is not excluded by AH5 and is addressed statistically by lane D's bar."
* **S06** "Lean certifies the implication 'if an observable depends on e and E only through lambda = eE/H^2, no function of it recovers e or alpha' (11 theorems; ten axiom-printed, standard axioms only; MUTATE variants fail to compile) and identities for the published closed forms. That the dS_2 pair-production factor has that form is shown numerically by AH1 (C0-C5), not by Lean."
* **S10** "The coefficient -1/4 of F^2 in R_5 and the mode coupling kappa_g n/R were verified by computer algebra on a one-component background A_y(x) in flat 4D with constant radion; the canonical normalisation kappa_g^2 = 16 pi G_4 is a hand-set premise from which alpha_n = 4 n^2 l_P^2/R^2 follows algebraically."
* **S11** "If the tree-level relation held with the Thomson value, alpha = 1/137.036 needs R = 23.41 l_P (carrier mass 5.2e17 GeV); read at M_KK with one-loop SM running (1/alpha ~ 107) it needs R = 20.7 l_P. For a graviphoton-charged mode m >= e M_P/sqrt(16 pi) at any R, twist or bulk mass (lane F T1), so the electron (1e21 above it) cannot carry graviphoton charge on a flat circle. alpha is traded for R."
* **S12** "Nine routes (lanes A-C, E-J) plus the calibration bar (lane D); separately pre-registered, but they share inputs (x = Lambda l_P^2, the SM one-loop chain, one handle list) and are not statistically independent."
* **S16** "In the Harst-Reuter Einstein-Hilbert toy with the nine charged fermions only (no W, no Higgs; two light-quark mass sets), alpha_IR^-1 = 75.2-77.1."
* **S20** "The fermion-only toy misses by ~1.9x. With the proper SM one-loop chain at Lambda = M_red/sqrt(118), 1/alpha_Y = 59.8 and 1/alpha_2 = 47.4 (SU(2) cannot emerge, b_2 < 0), i.e. the emergence residual for hypercharge is 59.8 (1/alpha_em = 107 includes SU(2)); emergence of hypercharge would need ~8.6 extra unit-Y Dirac fermions at 1 TeV (8.2 at 200 GeV, 10 at 1e5 GeV, 17 at 1e10 GeV; one loop, U(1)_Y only); either way it needs the walled masses."
* **S22** "For one-scalar models with alpha = 1/(k B_F(phi_m)) at a Damour-Polyakov, runaway or de Sitter extremum, the value is the free B_F(phi_m); rho_Lambda and kappa do not enter because the potential and B_F are taken as functions of phi alone (E1 C1c is true by construction). Families in which alpha is an explicit function of x = Lambda l_P^2 were tested only against variation bounds."
* **S24** "For a 5D circle with only rho_5 and the Casimir energy of massless fields (net dof count in {+5,-4,-8,-16,-100}), matching the observed vacuum energy gives R ~ 1e30 l_P (alpha_grav ~ 1e-60); R = 23.4 l_P needs ~114.5 decades of cancellation. The effect of twists and massive 5D fields was argued by hand (F1 verdict), not scripted."
* **S25** "For Freund-Rubin M_4 x S^2 (D = 6, one 2-form flux integer N) the 4D couplings are geometric in (N, R/l_P), R is set by the free ratio chat = g_6^2/kappa_6, and holding V = x/(8 pi) tunes Lambda_6 to ~3e-119; S^3 was checked only at the potential level."
* **S30** "Each of the nine routes tested fixes integers, ratios or inequalities, or moves the freedom into a modulus, a dimensionful scale or cutoff ratio, the charged spectrum, or a gauge kinetic function; none of these was derived in the record (no lane proves them underivable)."
* **S38** "All 47 scripts re-run with exit 0 and reproduce their outputs. 42 controls exit 1 (positional MUTATE for A, B, D, E, G, H, I, J, M; --mutate for C, F, K; --selftest --mutate for the bar checker); AH1, AH2, AH4, AH6 with --mutate print 'control works' and exit 0 (exit 1 only if the control fails to fail); AH5 has no control; K's --mutate-s2 changes nothing (exit 0)."
* **S39** "Nearly every line points to a committed script or a cited source (exceptions: the recalled Salam-Sezgin item, lane M's plausibility ratings, and lane D's bar thresholds, which are declared conventions). Lanes K and M have both reported."
* **S43** "For the SO(4,1) MacDowell-Mansouri action that reproduces the Einstein-Hilbert and cosmological terms (c = -3/(64 pi G Lambda)), reading 1/g^2 = |c| x (normalisation factor 0.01-100) gives alpha_MM ~ (16/3) G Lambda/kN ~ 1e-121-1e-117; larger groups were argued in prose, not computed."
* **S44** "An independent enumerator reproduces lane D's E1(12) counts exactly and E2(6) to 7e-5, so the counts are right; the bar's thresholds are declared conventions, and it is one-sided by design."
* **S47** "(Lane M's judgement, not scripted; lanes N1-N5 test these branches.)"
* **S48** "No claim among the 16 audited (three 2024-26 claims read only as summaries or abstracts; the K11 selection rule was visibly relaxed; six 2025-26 claims named but not audited) clears the bar." Misses/sigma values are unchanged (recomputed by P3).

## Consolidated NOT-TESTED hypotheses, by route

* **AH5 (dimensional)**: pure numbers built into the chain (Z, kappa, pi); non-monomial functions; other cosmological dimensionless groups (Omega_b, eta, matter density) beyond (c, G, Lambda, hbar).
* **AH1-AH4 (de Sitter)**: charged fermions (dS_2 and dS_4), vector bosons, non-minimal coupling xi R phi^2, backreaction of E, nearly massless fields (AH4 excludes them), nonlinear response (only linear conductivity), sum over the physical charged species, non-Bunch-Davies states, higher loops, finite counterterm shifts of 1/e^2 (argued, not computed), ties other than the three (AH1) and six constants (AH2/4), a tie at a specified mass. dS_4 pair-production factor (only the current was computed). The heavy-field power law rests on a closed form validated only to m/H = 3.
* **AH6 / lane F (KK)**: warped compactifications; several extra dimensions and non-flat internal spaces beyond S^2; radion/dilaton mixing in the charge-to-mass ratio; loops; Casimir energy of massive or several twisted fields (hand-argued); flux stabilisation other than a single S^2 2-form; stability beyond the radion (Bousso-DeWolfe-Myers); SUSY completions (Salam-Sezgin, recalled); branes; explicit CY/F-theory models.
* **A (WGC/extremal)**: higher-derivative corrections to extremality; dilatonic and non-abelian charges; BPS/SUSY towers; sublattice/tower WGC; quantum corrections near Planck size; O(1) constants of the FL bound; WGC/FL read at abstract level only.
* **B (RG / AS)**: FRG beyond the Einstein-Hilbert-type truncations; higher-derivative gravity; other groups' full-SM FRG results; regulator/gauge dependence of f_g (taken from 2508.03563, not recomputed); the sign question of the gravity term; GUT groups with own fixed points; KK/GUT thresholds; two-loop in the fixed-point toy; W and Higgs in the HR toy.
* **C (holographic / species)**: towers (Dvali-Gomez break time, string towers: lane N2); scalars and vectors in the emergence sum; species scale with a derived coefficient; alternative holographic counting; emergence for SU(2), SU(3) (sign obstruction argued, not scanned).
* **D (bar)**: other grammars/atoms; other density models; Bayesian priors; correlated formulas; the flat-density assumption was tested only on decoys inside D.
* **E (attractors)**: multi-scalar or string-model B_F; axion couplings; non-abelian sectors; time-varying w; tie forms other than x prop. rho_DE power/log; quasar, Oklo, BBN and CMB variation bounds (only the clock and MICROSCOPE bounds used); attraction history F_t (B5 note); electron-mass dependence (walled).
* **G (topology)**: Green-Schwarz / 10D anomaly (recalled); discrete and global anomalies; 't Hooft anomaly matching; N=1/N=2 SCFT fixed couplings; anomaly inflow in higher dimensions; Witten effect (not numerically); T1b, T2c, T5b are structural statements, not tests (G0 Amendment 1).
* **H (string)**: non-SUSY strings; explicit orbifold models with computed thresholds; flux vacua (counting only); Horava-Witten nonlinear terms; F-theory / G_2; two-loop thresholds; the pre-registered size criterion D1c was NOT MET (required 35 vs reachable <= 10.5), so the T-duality exclusion is structural only.
* **I (selection)**: BBN and deuterium bottleneck; Hoyle carbon resonance (a percent-level window, K notes it); electroweak vacuum stability; weak-scale windows; habitability; landscape measures; other weights (tunnelling); alpha-dependence of QCD/EW vacuum energy; full stellar models (scaling only; hydrogen-stability and calibrated constants are recalled numbers).
* **J (emergent photon)**: non-perturbative emergence (string-net, lattice; beta_c recalled); emergent charged fermions from FL1; Sakharov-type G-Lambda relations; Fermi-point species counts (recalled); two-loop; scalar and vector contributions to N_eff.
* **K (literature)**: six 2025-26 claims (Primeon Theory, Holographic Bit-Mode Balance, tensor-field harmonic cascades, Maya lattice, Emergent C-Space, an unnamed 1.62-sigma preprint); Bleger, Blandino, Reinisch beyond summaries/abstract; Gilson's form from a search snippet.
* **M (red team)**: the five under-tested branches (N1-N5 running); the WebFetch source checks S1/S2 of M's pre-registration are not reported in the document (Salam-Sezgin stays recalled).

## Statements resting on recalled / abstract-only facts (flag R)

S08 (closed form transcribed from a PDF text layer, validated by direct sum to m/H <= 3), S09 (scheme argument), S14 (WGC/FL abstracts), S15 (2508.03563 regulator dependence), S18 (Dvali, HRR abstracts), S27 (Green-Schwarz, racetrack, Dine-Seiberg, hadronic Delta alpha from memory), S28 (n-p mass split D_EM, stellar constants, pole-mass relation, Euler-Heisenberg coefficient recalled; the pole relation is RG-checked), S29 (photon-mass bound, 3He ratios, beta_c recalled; none decides the verdict), S39 and S46 (Salam-Sezgin), S48 and S49 (snippet and summary sources per K's own table).

## Internal consistency (P1, P3)

* All nine hashes in the document resolve to commits that touch the cited files (a628e8a66: lanes A, B, C, E, F, G; 1d23899e6: D; 190cb6920: H, I, J); the void remark is in 1d23899e6's message; the status document was last touched by 087c41203 (lane K). Every quoted script, path and directory exists; lane directories A-K, M exist.
* 27 quoted numbers (some with several outputs) appear in their cited outputs; P3 recomputes the deciding ones from scratch (x = 2.8485e-122; R/l_P 23.4125; M_KK 5.215e17 GeV; N_max 3.468e61; 1/alpha_em(m_P) 104.937/104.917; k = 5.122; f_g precision 0.176%; toy 70.44; 107.25; 8.58; 6.504e-8; 114.5 decades; (16/3)x = 1.52e-121; Gilson 4.449e-9 = 27.8 sigma, a* = 28.695; Wyler, Rosen, Sherbon, Eddington, hierarchy, Bleger misses).
* Findings: row 5 "Ten independent routes" (S12); verification note (S38); "ten theorems" versus 11 in the Lean file (10 printed).

## Cosmetic list (no change of meaning)

* "Z 12-13% away": 13.0% relative to k, 11.5% relative to Z; lane A prints -12.0 as a two-significant-digit rounding of -11.5.
* 1/alpha(m_Z) input differs between lanes (127.930 in B, C, M4; 127.95 in A, F, M1; 127.955 in G, H), giving 104.92 versus 104.94.
* AH4 commit message writes "|f/lambda| ~ 0.124/mu^2"; 0.124 is |f/lambda|/pi = sigma/(alpha H) (|f/lambda| ~ 0.389/mu^2). The document's "(~0.124/mu^2)" is the sigma/(alpha H) form.
* Row 3 quotes sigma/H = alpha G(m/H): for the dS_2 toy read e^2/H^2 in place of alpha.
* "0.18% for 1e-3": for alpha_Y at 173 GeV, not alpha_em.
* Lane D's bar has a clause (route's own predicted precision) that the document's row 6 omits; lane K's structural summary omits the anthropic idea and Reinisch (both 2/4) and Blandino; the H lane's unmet criterion D1c is not mentioned; the Lean "ten" counts printed lines.
