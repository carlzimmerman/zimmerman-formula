# Lane P -- claim-level red-team audit of ALPHA_CHAIN_STATUS.md (pre-registration)

Written 2026-09-28 BEFORE any check script of this lane was written or run. Amendments are appended at the bottom, never edited in place.

## Disclosure of what was done before this file
I READ ALPHA_CHAIN_STATUS.md (74 lines), the AH5 script and .out, the Lean file AH3_alpha_nogo.lean, `ls` of every lane directory, and the
`git log` messages of the alpha commits (to know which files exist). I have NOT read any lane script other than AH5, have NOT run any script,
and have NOT looked at lanes N1-N5 (not opened, out of scope). Reading AH5 and the Lean file by eye before pre-registering produced two
suspicions that are tested below rather than assumed: (i) "no dimensionless number exists from (c, G, Lambda)" is a statement about
Buckingham-pi MONOMIALS only (pure numbers such as Z or 4 pi trivially exist), so "the a0 chain cannot output alpha" may be dimensional-only;
(ii) chain row 5 says "Ten independent routes" although lane D "proposes no derivation".

## Scope
Every statement in ALPHA_CHAIN_STATUS.md that says a route "fails", "ends at", "cannot", "does not fix", "is excluded", "is sound", "is void",
or "was re-run clean", plus the document's inventory claims (hashes, script names, numbers, untested-list, verification note).
Not in scope: lanes N1-N5; re-deriving alpha; any physics beyond what is needed to judge whether a claim's wording exceeds its evidence.

## Categories (exactly these three, plus two flags)
* SUPPORTED AS WORDED (SUP): every quantifier, regime, field content, dimension and number in the sentence is covered by a tested case that I can
  cite (file:line), and the printed number matches the .out and my re-run.
* OVERSTATED (OVR): the committed evidence exists and is correct, but the sentence quantifies wider than the tested class (all truncations, all
  fields, all dimensions, "cannot", "never", "no X"), or glosses a number as more than the script shows. I give the narrower wording.
* UNSUPPORTED (UNS): no committed script or read source supports the sentence, or the number does not reproduce, or the script tests something
  different from what the sentence says.
* Flag R: the sentence rests on a fact the lane itself labels recalled / abstract-only / snippet-only (docstring, prereg, or report text), not
  read and not derived. Flag NT: the sentence has a non-empty list of natural hypotheses a reader might assume tested but that were not.
* A wording nit that changes no meaning goes in a separate "cosmetic" list, not in OVR.

## Protocol (fixed, applied to every statement)
1. Locate the script(s) and the exact tested hypotheses: field content (scalar/fermion), dimension (2/4/5/6/10), couplings (minimal/non-minimal),
   loop order / truncation, parameter ranges / grids, regime (heavy/light, m/H), stabilization mechanism, tower spectrum. Cite file:line.
2. Compare with the wording; classify by the rules above. A default of SUP is NOT assumed; a default of OVR is NOT assumed. "Sound" is a valid outcome.
3. List NOT-TESTED hypotheses per route.
4. Recalled-fact flag by grep of each lane's files for recall/abstract/memory/snippet wording and by reading the docstrings.
5. Re-run: p2_rerun_all.py copies the two directories into a scratch temp dir (no existing file is touched), runs every real script and its
   documented MUTATE invocation, and compares stdout with the committed .out (numeric tolerance 1e-9 relative on all floats, text otherwise; lines
   containing wall-clock or path text are ignored). Expected: real exit 0 and identical output; control exit 1. Scripts that need long runtimes are
   given a 600 s cap; a timeout is reported as NOT RE-RUN, never as pass.
6. p1_consistency.py checks: every commit hash in the document resolves in `git log`; every script name mentioned exists; the numbers quoted in
   the document appear in the cited .out / json (list fixed below); counts (lanes, routes). MUTATE argv: `python3 p1_consistency.py MUTATE`
   replaces one hash and one number by wrong values and must exit 1.
7. Where a document number is cheaply derivable from stated inputs (list fixed below) p3_independent_numbers.py recomputes it from scratch
   (MUTATE argv: `python3 p3_independent_numbers.py MUTATE`, flips one input, must exit 1).

## Statements to be audited (fixed list; IDs S01..S49; additions only by visible amendment)
Chain table: S01 (c,G,Lambda) has no dimensionless number; S02 with hbar exactly one, x = 2.85e-122; S03 alpha is an independent second group;
S04 a0 chain "cannot output alpha"; S05 AH1 rate depends on e only through lambda, alpha a free direction; S06 AH3 Lean "ten theorems, standard
axioms, controls fail"; S07 AH2 sigma/H = alpha*G(m/H), no conductivity tie fixes alpha; S08 AH4 heavy-field power law ~0.124/mu^2; S09 AH4
ln(m/H) is one-loop running so alpha enters as measured input; S10 AH6 alpha_n = 4 n^2 lP^2/R^2 by computer algebra; S11 AH6 R = 23.41 lP,
5.2e17 GeV, electron 1e-21, "alpha is traded for R"; S12 "ten independent routes" (row 5) and the lane/commit attribution; S13 the bar (row 6).
Routes: S14 A ends at inequalities/alpha-free/re-expression/automatic integer fit n~3.5e61; S15 B truncation-dependent bounds; S16 B SM content
gives alpha^-1 ~ 75-77; S17 B needs Planck-scale alpha^-1 ~ 105; S18 C inequalities or alpha traded for a count; S19 C fermion-only toy misses
~1.9x; S20 C proper SM chain leaves ~107 and ~8.6 extra unit-Y Dirac fermions near 1 TeV, walled masses; S21 D no derivation, standard; S22 E
freedom moves into B_F(phi), Lambda and kappa never enter; S23 E dark-energy-tied alpha needs w ~ -1 for fitted-exponent families, B3 allows 1+w
up to ~0.25 at zeta < 6.5e-8; S24 F R ~ 1e30 lP from Casimir + Lambda, ~115 decades; S25 F Freund-Rubin free 6D ratio, tuned Lambda_6; S26 G
integers/ratios, overall coupling free; S27 H alpha traded for string scale/dilaton, O(1) convention unresolved; S28 I bands hundreds to
thousands wider than 1e-3, HH extremum is a scheme choice; S29 J alpha^-1 = (N_eff/3pi) ln + const, N_eff and Lambda/mu not derived, dark-fluid
cannot supply; S30 common finding.
Framing and caveats: S31 "what a derivation would have to supply ... Nothing in the record does this"; S32 dS_2 toy caveat; S33 untested list;
S34 zeta bound unreconciled; S35 post-hoc observation VOID with corrected numbers (104.94, k = 5.12, Z 12-13% away); S36 "several lanes read only
abstracts or recalled"; S37 agents' disclosed slips list; S38 verification note (positional MUTATE vs --mutate; every real exit 0, control exit 1);
S39 header "every line points to a committed script or cited source" and "Lanes K and M have both reported".
Red team: S40 M re-ran all clean, AH2/AH4 not; S41 M lane B universal-f sign result and "0.18% for 1e-3"; S42 M lane C 0.6% self-consistency
shift; S43 M dS gauge MacDowell-Mansouri ~ (16/3) G Lambda ~ 1e-121; S44 M lane D independent enumeration and "one-sided by design"; S45 M Lean
no_alpha_from_obs adds no physics; S46 M Salam-Sezgin recalled; S47 five under-tested branches "all LOW plausibility".
Lane K: S48 misses and sigma values for the named claims (Eddington, Gilson, Wyler, Rosen, Sherbon, hierarchy, Bleger, Atiyah); S49 K structural
scores, JBW 3/4 "dead in QED", BSBM predicts no value, mutate-s2 control changes nothing.

## Document numbers checked by p1_consistency.py (fixed)
2.85e-122; 0.124; 23.41; 5.2e17; 1e-21 (9.8e-22); 3.5e61; 75-77; 104.9/104.94; 1.9; 107; 8.6; 6.5e-8; 1e30; 115 decades; 5.12; 12-13%; 0.18%;
4.9x; 0.6%; 16/3; 1e-121; 27.8 sigma; 28.695; 0.61; 3800 sigma; 3.3e-11; P=0.90; hashes 4dc1a546a, 5db88bfc2, 86f3c7a9a, 5823f6bfe, 0c72bfdec,
e39f0bfcc, a628e8a66, 1d23899e6, 190cb6920, 442b3253e(M), 087c41203(K).

## Numbers recomputed independently by p3 (fixed, only those cheap from stated inputs)
x = Lambda lP^2; R/lP for alpha = 4 lP^2/R^2 (n=1); m_e R c/hbar; number of decades of tuning (log10(1e30/23.41)); alpha^-1 at m_P from SM
one-loop with b_Y = 41/6 (corrected number 104.94, from the standard one-loop coefficients and m_Z inputs stated in the script); k_req = 1/(2 sqrt(alpha));
Z/k_req; Lean eps* = (1/2)/sqrt(4 pi alpha); Gilson-type digit/rounding numbers are NOT recomputed (need K's text).

## Outputs
P_REPORT.md (table of all 49 statements: script+lines, tested hypotheses, class, R/NT flags; corrected wording for every OVR/UNS; consolidated
NOT-TESTED list by route; internal-consistency list; cosmetic list), p1/p2/p3 scripts with .out and _MUTATE.out. Nothing outside this
directory is written; no ledger, no commit, no edit of any existing file.

## Stated expectation
The document is largely sound; expected findings are a handful of OVR wordings (universal quantifiers such as "cannot", "no conductivity tie",
"ten independent routes", "sound"), not a re-opened branch. This expectation does not decide any classification.

## Amendments

### Amendment 1 (2026-09-28, written after all four scripts had been run once; nothing above edited)
* Deviations from the plan above, all visible: (i) a fourth script p4_lean_rerun.py (Lean re-run of AH3 and its MUTATE file) was added; the plan named only p1-p3. (ii) p3 additionally recomputes the misses of the closed forms named in lane K (Gilson, Wyler, Eddington, Rosen, Sherbon, hierarchy, Bleger) from their printed formulas; the plan said the Gilson-type digits would NOT be recomputed: they are recomputed from the formula only, K's text is still not read. (iii) '4.9x' was on the planned number list but occurs only in a commit message, not in the document; it is not checked. (iv) p1 first version matched the digits of 137.035999177 as a hash and treated MUTATE and no_alpha_from_obs as file names: script bugs, fixed before the recorded run; no criterion changed. (v) p2 first version used an absolute tolerance of 1e-14 that hid a corrupted 2.8485e-122; fixed to a pure relative 1e-9 before the recorded run (the MUTATE control found it). (vi) p2 first full run reported 4 mismatches: two were wall-clock text ('build 2.2s', '(33 s on 7 processes)', now normalised) and two were the exit code of AH1/AH2 controls; the controls of AH1, AH2, AH4, AH6 exit 0 by design when the control fails as required (not 1 as the document says): this became finding S38. The first-run output is not kept; the numbers are in the report.
* The statement list is unchanged (49). Classification counts were not fixed in advance.
* Disclosure: a repository-wide `grep argv` over */*.py printed ONE docstring line of an N4 script (its own control invocation); nothing else of lanes N1-N5 was opened or read, and p2 excludes N* directories from the copy.
* Not done: no attempt to derive alpha; lanes N1-N5 not opened (beyond that line); no WebFetch of any source (every source claim is judged from the lanes' own prereg reading logs).
