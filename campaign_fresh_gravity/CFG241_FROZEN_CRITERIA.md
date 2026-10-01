# CFG241 -- Hostile post-publication referee of PAPER38 (a0(z) calibration wall, DOI 10.5281/zenodo.23073072, v1.1): FROZEN CRITERIA (phase 1)

Written 2026-09-30 by the referee agent, BEFORE any CFG241 script exists and before any substantive check. **kappa = 1/2 is FITTED, NOT DERIVED.** a0(z) FLAT is the programme's distinctive law (relative to LCDM and to the H(z) rival; standard MOND shares it); a0 proportional to H(z) is the rival. Nothing here says the data favour any law; a lean is not a detection; failed controls and wrong expectations are kept, never repaired. No favours language. The referee is **hostile but fair**: every finding must cite a source (file and line, or a numbered recomputation); no finding may rest on memory alone (memory-based concerns go in a separate "COULD NOT VERIFY" list, labelled "from memory, unverified").

Subject (read-only, never edited by this lane): `qwen_claude_field_theory/papers_2026/PAPER38_a0z_calibration_wall_2026.tex` (214 lines of text; git-clean at HEAD d73236046; sha256 5faf1b15e4ea2034598c6ae0d75410771c58ff0d94a32d60fa83ef9d1a0d5b41), the `.pdf`, the `.zenodo.json`, and `PAPER38_audit.py` (491 lines; sha256 cfcee5bd9f6d568ab688946f9b3aaa5fd4823b7ef45a6814915640bb35285340). Lane scripts will live in `campaign_fresh_gravity/CFG241_paper38_referee/` (the caller commits; this file is committed as `campaign_fresh_gravity/CFG241_FROZEN_CRITERIA.md` before phase 2).

## 0. What I read, and what I did not (blindness declaration)

- **Read in full (phase 1):** the tex (one pass, to enumerate structure). **So I know every sentence the paper makes; my hand estimates in section 11 are NOT blind to the text. They are blind to every source.**
- **Read partly:** `PAPER38_audit.py` docstring and the `SRC` file dictionary (lines 1 to 75 only; no regex rows); `git status`/`git log` for the paper (tex is unmodified at HEAD); the first 60 lines of `CFG238_FROZEN_CRITERIA.md` (format model only; they carry CFG224/CFG238 numbers, which I did not use); one `grep -n rc100` over `STANDING_2026-09-29.md`, which printed lines 126 to 148: **I therefore saw that the standing page says CFG216's "4.9-5.5 sigma" result is "not to be quoted as a ~5 sigma result", the -0.075 / -0.25 dex axis numbers, and the CFG217 input-correction note. The RC100 items are NOT blind.** One `grep -l "4,300|4300"` (hits: `CFG63_discrimination_forecast/README.md`, the STANDING page; contents not read).
- **Listings only (names, no contents):** the lane directories CFG216/217/218/223/233/234/236/237/238/240/255, `closure_map/`, `citations/`, `ChainCert/` (so I know `CalibrationWall.lean`, `CFG240_break_even_table.json`, `cfg223_lever.out` (real name: `CFG223_a0_over_cosmic_time/cfg223_lever.out`, plus `cfg223_lever.py`), `cfg255_stageA.out`/`stageB.out`, `CFG240_statements_phase1.lean.txt`, `verify_chain.sh` exist).
- **NOT read:** every README, `.out`, `.json`, `.lean`, `.bib` other than those named above; no physics script run; no kernel read.
- **Declared mental arithmetic while reading the tex (unscripted; not evidence; to be recomputed in P3, P2):** E(z) for a flat Omega_m = 0.3 reading gives about 2.20 (z = 1.4), 2.97 (z = 2), 3.39 (z = 2.3), 8.09 (z = 5), and about 1.08 between z = 0.2357 and 0.3723; and the algebraic relation between "0.05 dex in D" and the local slope (section 4, P2). I also noticed the items of section 11b while reading.
- **Throwaway enumerator (inline, not saved):** applying the section 3 rule gave **120 sentence units, of which 117 are claim sentences** (10 abstract + 110 body + 0 references) in 9 numbered sections plus abstract and reference list. Table cells and the 16 table rows are NOT yet separate units in that count (each table collapsed to one unit); the phase-2 `CFG241_extract.py` must reproduce 120/117 for prose and add the table rows as row-claims. Any difference is reported, not repaired.
- Literature facts not from the repo are marked "from memory, unverified".

## 1. Structure of the paper as seen (for coverage accounting)

| part | tex lines | prose sentence units (provisional) | audit tags (tex) |
|---|---|---|---|
| title block, conventions (comments) | 21-28 | 0 | - |
| abstract | 30-32 | 10 | B01 |
| 1 The prediction, the rival, the size of the signal (`sec:pred`; table 1, 6 rows) | 35-66 | 12 (+6 rows) | B02-B10 |
| 2 The lever (`sec:lever`; 2 bullet lists: 4 theorem items, 3 Fisher items) | 68-99 | 26 | B11-B14, B43, B12, B13, B15 |
| 3 What each sample gives (`sec:samples`; table 2, 10 rows) | 101-139 | 17 (+10 rows) | B16-B27 |
| 4 The gas calibration (`sec:gas`) | 141-150 | 10 | B28-B30 |
| 5 No dynamics-independent anchor (`sec:anchor`) | 152-161 | 11 | B31-B33 |
| 6 The differential route (`sec:diff`) | 163-174 | 13 | B35-B37 |
| 7 What would decide it (`sec:decide`) | 176-185 | 10 | B38-B40 |
| 8 Limitations and what is not claimed (`sec:lim`; 4 bullets) | 187-195 | 9 | B41 |
| 9 Reproducibility (`sec:rep`) | 197-199 | 2 | - |
| References (9 bibliographic entries behind 8 keys) | 201-212 | handled by section 7 below | B42 |

- Citation keys in the text: **ACE, B21, B23, C19, D22, DM14, HW20, NS23** (ACE = two papers: Solimano et al. arXiv:2609.21040 and Geesink et al. arXiv:2609.20926). Total 42 audit tags; **there is no tag B34** and B43 sits out of sequence (line 96). Cross-reference "section~2" at line 95 is hard-coded.
- 22 lane ids appear in the text: CFG213 to CFG224 (incl. 224b), CFG227 to CFG229, CFG233, CFG234, CFG237, CFG238, CFG240, CFG255; the text also cites CFG236 and the standing page.
- Files named in the tex as paths: `campaign_fresh_gravity/CFG240_calibration_wall/`, `data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md`, `real_research/reviews/lensing_rar/A0Z_LENSING_ZBIN_2026.md`, `PAPER38_audit.py`, `campaign_fresh_gravity/STANDING_2026-09-29.md`.

### Source files identified (candidate set; phase 2 maps each claim to a subset)

1. Audit `SRC` set (committed at HEAD): `campaign_fresh_gravity/STANDING_2026-09-29.md`, `STANDING_2026-09-28.md`, `LEDGER.md`; the READMEs of CFG213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224 (+ `README_B.md`), 227, 228, 229, 238, 240, 255; `CFG223_a0_over_cosmic_time/cfg223_lever.out`; `CFG228_alma_cubes/cfg228_preflight.out`; `CFG229_class_m_gold/cfg229_preflight.out`; `CFG255_lensing_rar_zsplit/cfg255_stageA.out`, `cfg255_stageB.out`; `data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md`; `real_research/reviews/lensing_rar/A0Z_LENSING_ZBIN_2026.md`.
2. Beyond the audit set (the referee must go to these): each lane's `FROZEN_CRITERIA.md` and `.out`/`.json`; `CFG223_a0_over_cosmic_time/cfg223_lever.py`, `cfg223_results.json`, `cfg223_points.csv`; the referee READMEs of CFG233, 234, 236, 237, 238 and `CFG238_FROZEN_CRITERIA.md`; CFG216 `INPUT_CORRECTION_2026-09-29.md`; CFG255 `PHASE1A_DATA_SCOPING`, `RERUN_BY_CALC_CHAT`, `PROPOSAL`, `FROZEN_CRITERIA`, `CFG255_1b_FROZEN_CRITERIA`; `fable_independent_2026/lean_2026/ChainCert/CalibrationWall.lean`, `CalibrationWallMutate.lean.txt`, `Certificates.lean`, `verify_chain.sh`, `campaign_fresh_gravity/closure_map/LEAN_CATALOGUE.md`; `CFG240_calibration_wall/{README.md, CFG240_break_even_table.json, .md, CFG240_fisher.py, .out, CFG240_statements_phase1.lean.txt}`, `CFG240_FROZEN_CRITERIA.md`.
3. Standing rules / withdrawals: `STANDING_2026-09-29.md`; `campaign_fresh_gravity/closure_map/*` (CLAIMS_AUDIT, OVERNIGHT_LESSONS, GATES*, VERIFICATION_REPORTED_ONLY etc.); lane correction notes (CFG216 INPUT_CORRECTION; CFG217/218 `*_corrected.out`); `LEDGER.md` rows for CFG216-218, 233, 234, 236, 237, 238; `citations/CORRECTIONS.md`, `citations/UNVERIFIED.md`, `citations/REFERENCES.bib`.
4. DR4 (READ ONLY, frozen files never edited): the Gaia DR4 preregistration and amendments (`deepseek_push/DR4_AMENDMENT_12.md` and the amendment files located in phase 2), `campaign_fresh_gravity/CFG200_dr4_merge_band_forecast/`, `CFG239_dr4_seed_noise_referee/`, `closure_map/DR4_DRESS_REHEARSAL_2026-09-29.md`, `CFG63_discrimination_forecast/README.md`, `data_assembly/AMENDMENT17_*`.
5. The deposited artefacts: the `.pdf` (text layer vs the tex), `.zenodo.json` (description vs abstract), `zenodo_publish_paper38.py` (metadata only).

## 2. Review protocol (per claim)

1. **Extract** all claims mechanically (section 3).
2. **Map** each claim to its source passages (section 3b): lane ids named in the sentence or its paragraph, the audit tag block (B-id) as a pointer (not as certification), numbers searched in the mapped files. Every claim gets a `source_map` row: files and line numbers, or `NONE`.
3. **Read** the mapped passage (README paragraph, `.out` block, Lean statement) and classify the claim with exactly one class (section 2a). I read the source sentence AROUND the number, not only the number.
4. **Recompute** where the claim is physics or arithmetic (section 4). A recomputation overrides a README only where the README is itself wrong; where a README and its `.out` differ the `.out` wins (the paper's own convention, line 28), and the discrepancy is itself reported.
5. **Severity** (section 2b) and a proposed replacement wording.
6. **Report** classification counts so coverage is visible: every claim ends in one class; `UNVERIFIABLE-OFFLINE` is a class, with a reason code.

### 2a. Classes (the peer's five, plus two)

- **FAITHFUL**: every number reproduces from the cited source/recomputation within the paper's displayed precision, the verb is no stronger than the source's, the scope (all/any/every) is no wider than the source's, and no source caveat that changes the reading is dropped.
- **OVERSTATED**: the claim's strength (verb, generality, certainty, scope, "decisive", "exactly", "any", "never") exceeds what the source supports.
- **UNSUPPORTED**: no source line, committed output, or recomputation supports the claim (the number or statement is not found in any mapped or searched file).
- **MISSING-CAVEAT**: the source attaches a qualifier (post hoc, not blind, hypothesis of a theorem, frozen only for X, bracket of prescriptions, not a detection) that changes how the sentence reads, and the paper drops it.
- **WITHDRAWN-CLAIM-CREPT-BACK**: the sentence quotes or implies something a committed correction, withdrawal, ledger row, or standing-page rule retires.
- **CONTRADICTED** (added): the source or my recomputation gives a different value or statement than the tex (beyond the tolerance of 2b).
- **UNVERIFIABLE-OFFLINE** (added): cannot be checked from files on disk; reason codes `NEEDS-NETWORK`, `SOURCE-NOT-ON-DISK`, `EXTERNAL-PAPER-NO-LOCAL-COPY`, `JUDGMENT-ONLY`. Reported, never silently counted as FAITHFUL.

### 2b. Severity scale (definitions frozen now)

- **CRITICAL**: (i) a false or contradicted numeric or physics claim (class CONTRADICTED or a failed re-derivation), where false means outside the displayed precision of the paper's own rounding (half a unit of the last shown digit; one unit when the source prints a further digit and the rounding is ambiguous); hedged claims ("about", "~") are false when off by more than 25%; (ii) a withdrawn claim quoted or implied as live; (iii) an overstatement a source explicitly refutes (a source line says the opposite, "NOT POSSIBLE", "withdrawn", "not to be quoted", and the paper says or implies the contrary); (iv) a bibliographic entry contradicted by the repo's own `.bib`/UNVERIFIED notes in volume, page, year, or first author. **A CRITICAL needs two independent supports: a source line plus a recomputation, or two source lines, or one explicit source statement of the contradiction.**
- **MAJOR**: a missing caveat or overstatement that changes the conclusion a reader would draw (a theorem stated without hypotheses that a reader would then apply outside them; a lever quoted for the wrong variable; an accusation about a named published table stated beyond what a parse can support; an unfair characterisation of a MOND or LCDM position that changes the reading); a hedged number off by 10-25%.
- **MINOR**: a dropped caveat that does not change the conclusion; ambiguous wording; hedged numbers off by <10% but not at the paper's displayed precision; undeclared choices (Omega_m, kernel, H0) that a careful reader can recover; incomplete bibliographic entry; internal inconsistency in notation.
- **NIT**: typography, hard-coded cross-reference, tag numbering, redundancy, grammar, `N>9` versus `N>=9` style items.
- **Tie rule:** when a finding sits between two severities, the lower is assigned; I do not inflate. A finding that depends on a source I judge ambiguous is MINOR at most and carries the quote.

## 3. Claim extraction (mechanical; script `CFG241_extract.py`)

**Units.** Take the tex between `\begin{abstract}` and `\section*{References}`; drop comment lines (starting `%`) but keep `% AUDIT: Bnn` tags as metadata attached to the unit immediately above them; break units at blank lines, `\begin`, `\end`, `\toprule`, `\midrule`, `\bottomrule`, `\item`, and section commands; each table row (a line ending `\\` inside a `tabular`) is its own **row-claim** (cells with a digit or a verdict word are sub-claims); each `\item` is its own unit.

**Sentences.** Split units at `[.?!]` followed by whitespace and an uppercase letter, backtick, backslash, `$` or `(`, after protecting `et al.\ `, `i.e.\ `, `e.g.\ `, `Eq.~`, `Table~`, `vs.\ `, `Sect.~` and decimal points.

**A claim is any sentence (or row, or item) that has at least one of:**
(a) a digit outside `\ref`, `\label`, and `\cite` arguments; (b) a trigger lexeme: *shows, show, implies, proves, theorem(s), finds, found, certif\*, predicts, exclud\*, disfavour\*, consistent, cannot, must, need(s), never, every, only, decisive, strongest, tightest, largest, no, none, not, ill-conditioned, walled, decides, determine\*, separate\*, lean, is, are*; (c) it lies in the abstract, Section 7 (`sec:decide`) or Section 8 (`sec:lim`) (all sentences there count). Everything else is logged as NON-CLAIM with the reason, so the denominator is auditable.

**Record per claim:** `id` (C001...), tex line of the unit start, section, text, number tokens, trigger lexemes, lane ids named, bibliographic keys named, universal-quantifier tokens (*any, every, all, whatever, always, never, however many, exactly, in every, at every*), caveat tokens present, the audit tag (B-id) of the unit, and a text hash (stable across line shifts, used by the plants).

**Reference entries** (9) and **code/path mentions** (`\fpath{...}`: each must exist at HEAD) are enumerated separately; they feed section 7 and the reproducibility checks.

### 3b. Source matching (mechanical first pass, human second pass)

1. **Index the sources.** Split each file in the section 1 set into paragraphs (blank-line blocks for `.md`; blocks for `.out`; theorem blocks for `.lean`), with line numbers.
2. **Candidate map.** For each claim, candidates are (i) the files of every lane id named in its sentence or its paragraph, (ii) the audit rows of its B tag (read from `PAPER38_audit.py`: the `SRC` key and regex give the pointer; I use them only to LOCATE the passage), (iii) any file in the full source set whose paragraphs contain at least two of the claim's number tokens, or one number plus two content words.
3. **Context extraction.** For each number token, return the source paragraph and +-2 lines. A number match is a pointer, not a verdict.
4. **Verdict is human**, written to `CFG241_classification.csv` (id, class, severity if any, source file:line, rationale <= 25 words), and the script **refuses to finish** (exit 2) if a claim has no row. The script flags mechanically (below), but flags never replace the reading.

### 3c. Mechanical flag families (the "claim-checker pipeline", script `CFG241_check.py`)

| family | rule | meaning |
|---|---|---|
| NUM | a number token in the claim is absent from every mapped source paragraph (tolerance: equal after rounding to the displayed precision; `-` and unicode minus unified; `x`/`times` unified) | numeric swap or unsupported number |
| VERB | strongest verb level in the claim > strongest verb level in the matched source sentence; levels: 0 descriptive (*lies inside, consistent with, reads, sits*), 1 (*suggests, leans, hints, gives*), 2 (*finds, indicates, implies*), 3 (*shows, demonstrates, certifies*), 4 (*proves, establishes, excludes, rules out, detects, confirms, rejects, decisive*) | stronger verb |
| CAVEAT | the matched source paragraph contains a caveat token (*post hoc, not blind, withdrawn, not to be quoted, NOT POSSIBLE, NON-DISCRIMINATING, fragile, calibration-bound, descriptive, not a detection, bracket, unverified, hypothesis, assumes*) that is absent from the claim's paragraph | dropped caveat |
| CITE | an author surname in the sentence is attached to a key whose first author differs (key-to-surname map from the reference list), or a citation of an author/year not in the reference list | wrong or phantom citation |
| WITHDRAWN | the claim matches a pattern of the withdrawn-lexicon (built in phase 2 from the files of section 1 item 3; frozen minimum seeds: RC100/CFG216 near 4.9, 5.5 or 5 sigma without a retraction word in the same sentence; "5.09 keV", "2.55-keV", "z*=2.4", "180 theorems", "BH*", "lambda_J = 2.7 Mpc", "74-89%", "6-8 sigma" (Ly-alpha), "AeST+mu10 survivor", "closed" as in "theory closed", "KiDS lead", and any lane-specific withdrawal found in LEDGER rows for CFG216-218, 233, 234, 236-238) | withdrawn claim |
| SCOPE | the claim contains a universal-quantifier token and the matched source paragraph carries a hypothesis marker (*if, provided, assume, hypothesis, requires, for the P2 kernel, 0 <= b_i <= 1/2*) or the same quantifier is absent from the source | scope inflation |
| ARITH | a derived quantity stated in the tex (a product, ratio, power of ten, N from a floor formula, rounding of a range) does not follow from the other quantities in the tex (a hand table of at least 20 internal relations, section 4 P10) | internal arithmetic |
| NOSRC | the claim has numbers or a "shows/finds"-type verb and the candidate map is empty | no source |

Flags are inputs to the human classification; a false-positive is logged, not hidden. The flagger's own recall is tested in section 7.

## 4. Physics re-derivations (frozen list; script `CFG241_physics.py`, numpy/scipy/sympy)

Kernel: read from `cfg223_lever.py` and `CalibrationWall.lean` ("P2" as the lane defines it) and implemented from that reading; a **second kernel** (the simple McGaugh form nu = 1/(1 - exp(-sqrt(y)))) is run as a sensitivity check, and the dependence on kernel is stated. Notation: y = g_bar/a0; nu(y) with D = g_obs/g_bar = nu; m(y) = -dlog10 nu / dlog10 y (positive; 1/2 in the deep limit, 0 in the Newtonian limit); delta_i(s) = log10[D_i / nu(y_i/s)]. Known-answer self-controls: m -> 1/2 for y << 1; nu -> 1 for y >> 1; E(0) = 1.

- **P1 -- delta/2 deep-regime mimicry.** With one calibration factor f on g_bar: g_obs = f g nu(f g/a0). Re-derive symbolically (sympy): d ln g_obs / d ln f = 1 - m(y); d ln g_obs / d ln a0 = m(y). Deep limit m = 1/2: both = 1/2, so a drift delta in log f and a drift delta in log a0 each move log g_obs by delta/2 and are indistinguishable; away from deep they are not (1 - m versus m). Then check against the tex: (i) lines 79, 169: "moves the amplitude by delta/2, exactly as an a0 drift does" (what the lane's "amplitude" is: dex of the lensing signal or of g_obs, per `CFG255` README/FROZEN_CRITERIA/code); (ii) "the rival's 0.018 dex needs the KiDS photometric M_* stable to better than 0.036 dex" (factor 2); (iii) whether the KiDS lens y-range supports "deep regime": the lane's own g_bar/a0 values, and the size of the difference between m and 1 - m there.
- **P2 -- the lever as a function of y.** Hand-algebra expectations (labelled hand expectations, to be confirmed or killed by sympy): (a) shift of log D by epsilon moves log s* by epsilon/m(y) (so 0.05 dex in D gives 10^(0.05/m)); (b) a shift x (dex) of all baryon masses at fixed g_obs moves log s* by -(1 - m)/m = 1 - 1/m per dex; (c) so the quoted pair "local slope 0.13 to 0.28" would give (a) a factor 1.5 to 2.4 and (b) -2.6 to -6.7, versus the paper's "factor 1.5 to 1.8" and "-2.5 to -4.8". Recompute from `cfg223_lever.out` (all eight points), from the kernel at each point's y, and report: the exact dependence on y and kernel, whether the abstract's "so a 0.05 dex error in the mass discrepancy is..." follows from the preceding clause (the two levers differ: one in D, one in baryon dex), whether "local slope" in line 73 is the m defined above, and the table of (y, m, L_D, L_b, factor) per point.
- **P3 -- rival-shift numbers.** E(z) = sqrt(Om (1+z)^3 + 1 - Om) at Om in {0.27, 0.30, 0.315, 0.32} (flat; and with a radiation term as a sensitivity), at z = 0.2, 0.2357, 0.23, 0.38, 0.3723, 0.40, 1.4, 2.0, 2.3, 5, and the CRISTAL redshifts quoted by CFG218/224/228 (8.69, 8.84). Compare: x2.2 at z ~ 1.4, x8 at z ~ 5, 3.4 at z = 2.3, 0.48 dex at z ~ 2, 1.083 (lens-lane predicted ratio), and the KiDS amplitude 0.018 dex (a0 ratio log E ratio over the lane's median redshifts, halved per P1). State whether the tex says which Omega_m is used (hand-note: it does not).
- **P4 -- KiDS power.** From `cfg255_stageA.out`, `stageB.out`, README, FROZEN_CRITERIA: reproduce Delta chi^2_pred = 0.14 (canonical) / 0.17 (alt) from the stated lever (+0.018 vs +0.001) and stated error(s): (0.017/sigma)^2 for sigma in {0.038 jackknife, stage-A error}; identify which error the pre-flight used and whether 0.038 (a stage-B quantity) and 0.14 (a stage-A pre-flight quantity) are mixed in one sentence (line 167); chi2.sf(19.8, 14), (19.2, 14), (15.1, 14) for the "all p > 0.1" statement; (0.060 - 0.018)/0.038 and (0.060 - 0.001)/0.038; the "p = 0.10" under injection; "9 required" = 3 sigma squared.
- **P5 -- the CFG240 statements as typed.** Read `CalibrationWall.lean` and the statements file; for T1, T2a, T2c, T4 (and the ones the paper omits, T2b/T3 if they exist) write the exact Lean statement, its hypotheses, its universe of quantification, and its conclusion; compare with the paper's lines 82-88: **T1** "g_obs depends on (f, a0) only through f a0" (hypothesis: exact deep law?); **T2a** "for the exact P2 kernel, two distinct g_bar values determine (f, a0) and one does not" (hypothesis: non-deep? injectivity domain? "determine" = locally or globally?); **T2c** "the Jacobian determinant tends to zero when both points are deep" (a limit statement; in which variable; relative or absolute); **T4** "with f free any sample obeys sigma(log a0) >= 3 sigma/sqrt N" (**the Lean hypothesis 0 <= b_i <= 1/2 on the local slope**: does the paper's "any sample" carry it? what is b_i? what is the 3: a derived constant or a bound from the slope range?; does the formal statement include the N and sigma consequences "N > 9" and "N > 36"; strict versus non-strict inequality). Count theorems in `CalibrationWall.lean` (paper: 50), the ChainCert total (paper: 281 to 331), "standard axioms only" (from the certificate/`#print axioms` output on disk), and `verify_chain.sh` (run only if a Lean toolchain is on disk and the run fits the time budget; otherwise report "NOT RUN, no network, toolchain not verified").
- **P6 -- the break-even table.** Re-implement the Fisher: log-uniform design in y in [y_min, y_max], N = 20 points, sigma = 0.1 dex per point on log g_obs, kernel P2, free (log f, log a0), no prior on f; Fisher matrix, covariance, sigma(log a0), correlation rho. Find the smallest y_max on the 0.02-dex grid (50 per decade) with sigma(log a0) <= 0.1 for y_min in {0.1, 1e-3, 1e-2}; independent bisection on a continuous y_max; compare with `CFG240_break_even_table.json` (headline cell read 7.94 on the grid vs about 7.61 bisection per the README, within one step) and with the tex ("y >~ 8", "y >~ 5.5", "never reaches 0.1: best 0.117", "rho ~ -0.8"). Then compute the same Fisher for the **discs the paper actually describes** (y in 1.1 to 4.4) as a direct number for line 95's closing sentence, and the dependence on the design (log-uniform vs the real sample).
- **P7 -- the floor T4 as a numerical bound.** For random designs with local slopes b_i in [0, 1/2], minimise sqrt(N) sigma(log a0)/sigma over designs under the Fisher model: is 3 attained, exceeded, or violated? (A violation would make T4 as typed false for the stated model; a large slack would make "3" a loose bound, not a floor that can be reached.) Then the table "N > 9 at sigma = 0.1 for 0.1 dex; N > 36 at 0.2": 3 sigma/sqrt N <= target.
- **P8 -- the DR4 paragraph.** From the DR4 prep files and the preregistration (read only): "B predicts gamma-hat = 1.000", "bare law's floor 1.161 (alt 1.192)", "sigma_sys = 0.02", "3 sigma needs about 4,300 pairs (alt 2,900) out of about 30,000 expected", "2 Dec 2026". Re-derive the pair counts from the frozen statistic model: N such that (floor - 1) / sqrt(sigma_sys^2 + (c/sqrt N)^2) >= 3 for the stated floors; check the ratio 2,900/4,300 (hand expectation: about 0.67) and the dependence on c; check that LCDM and Newton predict 1.000 in the SAME statistic under the preregistration's own definition (so that "B, LCDM and Newton all predict 1.000" is a statement about the preregistered statistic, not just a slogan); check the word "decisive" (abstract, section 7 heading) against the statement that DR4 cannot separate B from LCDM or Newton.
- **P9 -- number-by-number recomputation of derived tex statements** (the ARITH table, at least 20 rows): 0.175 -> +-0.06 (3 sigma separation, line 132); 0.036 = 2 x 0.018; 600 to 3,000 = 10^2.8 to 10^3.5; 0.18 to 0.33 = 0.1 x (1.8, 3.3); 3 to 7 x the 0.10 target from 0.35 to 0.7; "7 of 19 + 4 QSO + 3 GRB" rows of HW20 arithmetic (as stated); 0.64 to 0.55 rms after the shift; 1.309 +- 0.210 relative to 1.083 and 1.000 (sigmas); 0.465 dex between halves; 0.25 dex -> about 0.15 on baryons; "4 to 31 degrees" inclination; "1.3 to 8 times the stated radii"; 3.4 and 8.69 from E(z) at the lane redshifts; +0.33 dex = log10 2.16; F ratios; the 3 sigma needs (2.3 sigma, 1.3 sigma) statements of the standing page; counts "7 of 8", "flat 7/8/8, proxy 5/7/7, H(z) 4/5/7" against `cfg223_points_table.md`/`results.json`.
- **P10 -- audit-script anchoring review.** Parse the rows `R(block, value, file, regex, tex)` of `PAPER38_audit.py`; for each, classify the regex as ANCHORED (contains a context phrase of at least 12 characters around the capture group) or BARE (a bare number or a short generic neighbourhood); report the BARE count, and for each BARE row whether the same digits occur in more than one place of the source file (an unintended match is then possible). This measures how much of "293/293" can have passed on a number that sits in a different sentence than the tex's.
- **P11 -- PDF/tex drift.** If a PDF text extractor is present on disk, extract the PDF text and compare number tokens with the tex's (the deposited artefact is the PDF); report drift. Compare `.zenodo.json` description to the abstract.

Tolerances: tex versus recomputation by displayed precision (section 2b); recomputations that need a choice (Omega_m, kernel, design) are reported as a range and the claim is CONTRADICTED only if it is outside the whole range.

## 5. References: spot-check procedure and offline limits

**Done offline:** (1) parse the 9 entries; (2) compare title, first author, year, journal, volume, page/article number, doi and arXiv id with the matching entries of `citations/REFERENCES.bib` (and any in `citations/WORKS*.md`), and with the flags in `citations/UNVERIFIED.md` and `citations/CORRECTIONS.md`; (3) check that arXiv identifiers are of a plausible form for their stated month (2609.xxxxx = September 2026) and that "submitted to A&A" entries do not carry journal volumes; (4) look in the repo for local copies (HTML, PDF, tex) of the cited papers (`data_assembly/`, `_external_data/`-style folders, `multitracer_gas/raw_small/`) and compare the volume/page/year there; (5) completeness: **B23 (ApJ) and C19 (MNRAS, doi only) carry no volume or page: MINOR by the severity scale if the .bib has them**; "(Brouwer et al. 2021)" style redundant parentheticals: NIT.

**Pre-selected two journal volume/page spot-checks (chosen now, before reading the .bib):** **[D22] MNRAS 517, 962 (doi 10.1093/mnras/stac2098)** and **[HW20] ApJL 889, L7**; fall-backs, used only if the .bib/UNVERIFIED holds no entry for a chosen one: [NS23] ApJ 944, 78; [B21] A&A 650, A113; [DM14] MNRAS 441, 3359. HW20 is chosen because it carries the paper's sharpest claim about a named table.

**Cannot be done offline (stated in advance, reported as such):** whether the journal volume/pages match the publishers' records; whether arXiv numbers resolve; whether the ACE papers (arXiv 2609.xxxxx, dated after my knowledge cutoff) exist as stated and with the stated authors and titles; whether any local HTML copy is the final published version. For each, the report says "agrees with the repo's own record (.bib / local copy), NOT checked against the journal". My own recollection of any journal volume/page is recorded only in the "COULD NOT VERIFY (from memory, unverified)" list.

## 6. Fairness checklist (MOND and LCDM; each item scored FAIR / UNFAIR-TO-MOND / UNFAIR-TO-LCDM / UNFAIR-TO-NAMED-AUTHORS / UNDECLARED / NOT-APPLICABLE, with the tex line and, for any unfair score, a source line or the sentence itself)

F1 Is "flat a0" called "the programme's distinctive law" without saying that standard (Milgrom) MOND also has a constant a0, so that the distinction is against LCDM and the H(z) rival only?
F2 Is the H(z) rival attributed to a position held by someone, or is it a construct of the programme (and does the text say so)? Is it presented as a straw man (an upper-end alternative) while milder variants (a0 ~ c H0 / 2 pi fixed, or weak cosmological drifts) are not considered?
F3 Is the LCDM "effective-a0 proxy" described as the programme's own construct with the correct disclaimer in the places a reader sees first (abstract, table 1), not only in section 8? Are LCDM simulation predictions for the high-z RAR cited or only deferred to "CFG222"?
F4 Is the data-owner's (e.g., RC100's) own conclusion reported fairly where the paper reuses their sample for the programme's question?
F5 Tone toward named authors: HW20 re-reading ("cyclic shift", "do not follow from the paper's own Eq. 3", "scatters 0.64 dex against the 0.2 stated"): is each statement a transcription check carried with its limitation (the paper's own bullet 4 of section 8 says so), and is the abstract's phrasing as careful as the section's?
F6 Selective citation: no MOND-side, LCDM-side or high-z-RAR literature other than RC100, DM14, B21 is cited; is the absence declared (a reader would expect, e.g., the standard literature on high-z RAR)? Memory-based expectations go to COULD-NOT-VERIFY.
F7 Undeclared choices: Omega_m and H0 for E(z); the kernel and "P2"; the canonical vs alternative footing; 2 sigma vs 3 sigma conventions; "band" definitions (statistical / +-0.15 / +-0.30 dex); frozen vs post hoc quantities. Declared in the text or recoverable only from the lanes?
F8 Symmetry: is the calibration wall stated as limiting evidence FOR and AGAINST each of flat, rival and proxy (including when RC100's earlier result favoured flat)? Does the text correct the programme's own earlier stronger claims in the same breath (RC100, CFG218, CFG224)?
F9 "Decisive": is DR4 called decisive for a prediction (B = 1.000) that LCDM and Newton share?
F10 Is the paper's headline ("the limit is calibration, not N") equally true of a test that would favour the programme (a ceiling is a ceiling), and is the "if both errors <= 0.10 dex then flat vs H(z) separate" statement carried with its post hoc label?
F11 Characterisation of the other lanes' results ("fragile and calibration-bound", "lean toward the rival" for KURVS; "MUSE-DARK III's a0 rise is not recovered") against the standing page wording (the paper quotes the page; is the quote exact and complete?).
F12 AI-assisted authorship and "not peer reviewed" disclosure: present (title block). Check it is also in the `.zenodo.json` description.

## 7. MUTATE-style controls (planted false sentences in scratch COPIES; one plant per copy)

The pipeline of section 3c is run on (i) the unmodified tex (baseline flags F0), and (ii) each scratch copy (flags F1). A plant is **caught** iff F1 contains at least one flag of the **expected family** on the claim whose text hash is that of the planted sentence (or of the replaced sentence); flags of other families are recorded but do not count; a flag already in F0 for the same unmodified sentence does not count. A **faithful paraphrase** passes iff F1 for the paraphrased claim is a subset of F0 for the original claim (no new flag). Plants are replaced in a copy of the tex with the exact strings below (old -> new); if `old` is not found the control fails (exit 3). Plants are frozen now and cannot be tuned after seeing a miss.

| id | kind | tex line | old (exact) -> new (exact) | expected family |
|---|---|---|---|---|
| M1 | numeric swap | 167 | `$\Delta\chi^2_{\rm pred}=0.14$ (canonical)` -> `$\Delta\chi^2_{\rm pred}=0.41$ (canonical)` | NUM |
| M2 | stronger verb | 98 | `flat $a_0$ (ratio 1) lies inside the 95\% statistical interval of 7 of the 8 CFG223 points` -> `flat $a_0$ (ratio 1) is demonstrated by the 95\% statistical interval of 7 of the 8 CFG223 points` | VERB |
| M3 | dropped caveat | 110 | `not $a_0(z)$, and its frozen significance is not to be quoted` -> `not $a_0(z)$` | CAVEAT |
| M4 | wrong citation | 143 | `Dunne et al.\ [D22] the tracer masses agree by construction` -> `Dunne et al.\ [HW20] the tracer masses agree by construction` | CITE |
| M5 | withdrawn claim | 132 | `\emph{RC100} (Nestor Shachar et al.\ [NS23]) is the tightest sample statistically,` -> `\emph{RC100} (Nestor Shachar et al.\ [NS23]) rejects the rival at $z\approx2.2$ at $4.9$--$5.5\sigma$ and is the tightest sample statistically,` | WITHDRAWN |
| M6 | scope inflation | 87 | `With $f$ free, any sample obeys` -> `With $f$ free, any sample, for any kernel, obeys` | SCOPE |
| M7 | order-of-magnitude numeric | 73 | `a 0.05\,dex error in $D$ is a factor 1.5 to 1.8 in $a_0$` -> `a 0.05\,dex error in $D$ is a factor 15 to 18 in $a_0$` | NUM |
| M8 | invented supporting claim with phantom citation | 98 | append after `(one of them has no root in 10\% of resamples).` the text ` A Chandra stacking at $z\approx0.8$ independently confirms a flat $a_0$ to 3\% (Smith et al.\ 2025).` | NOSRC (or CITE) |
| M9 | internal arithmetic | 87 | `at 0.2\,dex it needs $N>36$` -> `at 0.2\,dex it needs $N>6$` | ARITH |
| M10 | direction swap on a derived number | 184 | `3$\sigma$ needs about 4,300 pairs (alt 2,900)` -> `3$\sigma$ needs about 4,300 pairs (alt 6,500)` | NUM or ARITH |

Faithful-paraphrase controls (must NOT be flagged beyond baseline):
- **P-a** (line 165): `A split by redshift inside one survey cancels any calibration that is common to both halves.` -> `Splitting a single survey in redshift removes any calibration shared by the two halves.`
- **P-b** (line 192): `The $\Lambda$CDM proxy is not $\Lambda$CDM.` -> `The $\Lambda$CDM proxy should not be mistaken for $\Lambda$CDM itself.`
- **P-c** (line 126): `NOT POSSIBLE (power 0.14 against 9) and NON-DISCRIMINATING by its MUTATE \\` -> `NOT POSSIBLE (power 0.14 against the 9 required) and NON-DISCRIMINATING in its MUTATE control \\`

Additional control: **self-disable test**: run M1 with `--disable NUM`; the plant run must then exit 1 (the control can fail). 10 plants + 3 paraphrases = 13 control runs; at least 5 plants (the peer's minimum) of different kinds are present (numeric, verb, caveat, citation, withdrawn, scope, unsupported, arithmetic).

**Exit-code convention (frozen):**
- `CFG241_check.py` main run: **0** if the pipeline completed on the real tex, wrote every output, and met the coverage target of section 9; **2** if the coverage target is missed, a claim has no classification row, or the script errored; **findings never change the exit code** (a referee that finds something is working).
- `CFG241_check.py --plant`: **0** only if all 10 plants were caught and no paraphrase was newly flagged; **1** if any plant was missed or any paraphrase flagged (misses are printed by id and kept in the committed `.out`); **3** if an `old` string is not found in the copy.
- `CFG241_physics.py`: **0** if it ran and its known-answer self-controls (m -> 1/2 deep, nu -> 1 Newtonian, E(0) = 1, break-even reproduction of the README's bisection value within 0.03 dex, a Fisher matrix positive definite) pass; **1** if a self-control fails; a recomputation that contradicts the paper prints `CONTRADICTS`, not an error exit. `--mutate` perturbs one input (kernel exponent) and must exit 1.
- `CFG241_refs.py`: 0 if the comparison completed; discrepancies are printed, not exit codes.
- If a plant is missed the miss and the run are kept; any new rule is added as a versioned rule (v2) with both outputs committed; the first result is not overwritten.

## 8. Script plan (all names `CFG241_*`, in `campaign_fresh_gravity/CFG241_paper38_referee/`)

| script | role | output |
|---|---|---|
| `CFG241_extract.py` | section 3 enumeration; sections, table rows, items, references, tags, citation keys, paths; counts | `CFG241_claims.csv`, `CFG241_extract.out` |
| `CFG241_sources.py` | build the source paragraph index and the withdrawn lexicon (from the section 1 item 3 files) | `CFG241_source_index.json`, `CFG241_withdrawn_lexicon.json` |
| `CFG241_check.py` | candidate map, six flag families, worksheet; `--plant`, `--disable RULE`; coverage report | `CFG241_worksheet.csv`, `CFG241_flags.out`, `CFG241_plant.out` |
| `CFG241_classification.csv` | hand classification of every claim (section 3b step 4) | committed table |
| `CFG241_physics.py` | P1 to P9, P11; `--mutate` | `CFG241_physics.out`, `CFG241_physics_results.json` |
| `CFG241_audit_anchor.py` | P10 | `CFG241_audit_anchor.out` |
| `CFG241_refs.py` | section 5 | `CFG241_refs.out` |
| `CFG241_run_all.sh` | everything in order | `CFG241_run_all.out` |
| `CFG241_README.md` | phase-2 report: findings ranked by severity, v1.2 statement, FAITHFUL list, COULD-NOT-VERIFY list | |

Conventions: no absolute home path printed anywhere: the repo root comes from `ZF_REPO` or by walking up from `__file__`, and is printed as `<repo>`; sources are read as committed at HEAD (`git show HEAD:<path>`) with the working tree read only where the file is untracked (reported), so that the deposited state is what is reviewed; stdlib + numpy/scipy/sympy only; **each script <= 15 min** (the whole run_all <= 15 min; the optional Lean check has a timeout and is reported NOT RUN if it cannot finish). No network. No file in `PAPER38_*` is written. Outputs go to the lane directory only. Plants run in a temp copy that is deleted after the run (the copy hashes are logged).

## 9. Coverage target

- Every mechanically enumerated claim (prose + table rows + items) gets exactly one class: **100% classified** (the script exits 2 otherwise).
- **At least 90%** of the claims with a number or a "shows/finds/predicts"-type verb are matched to a source line or recomputation (class FAITHFUL / OVERSTATED / CONTRADICTED / MISSING-CAVEAT / WITHDRAWN... / UNSUPPORTED), i.e. **at most 10% UNVERIFIABLE-OFFLINE**; **100% of the number tokens in the abstract, Section 2, Section 6 and Section 7** are individually checked (the sections the peer named). `UNVERIFIABLE-OFFLINE` claims are listed with their reason codes and are never counted as FAITHFUL. If a target is missed the report says MISSED and gives the achieved fraction.
- Also reported: the number of claims whose audit tag exists and whose B-row source is a different sentence from the tex's (from P10); the number of claims mapped to a source file outside the audit's `SRC` set.

## 10. Output format of phase 2 (the peer's request)

1. **Findings**, ranked CRITICAL / MAJOR / MINOR / NIT; each: id F-nn, tex line number(s), class, the source (file and line) that contradicts or fails to support it (or the recomputation id), and a proposed replacement wording.
2. **A v1.2 statement:** frozen rule: any CRITICAL, or two or more MAJOR findings on text the paper itself states (not on an undeclared choice), means "a v1.2 deposit is warranted"; otherwise "not warranted, list for a later revision". The owner decides.
3. **FAITHFUL list** (claim ids and tex lines) so coverage is visible; **UNVERIFIABLE-OFFLINE list**; **COULD NOT VERIFY (from memory, unverified)** list; **plant and paraphrase control results** including misses; **fairness checklist scores**.
4. The audit finding (P10): how much of 293/293 is anchored.

## 11. Hand ESTIMATES (mine, labelled; made AFTER reading the tex, BEFORE any source: not blind to the text)

**11a. Counts and probabilities.**

| quantity | estimate |
|---|---|
| CRITICAL findings (a false or contradicted number/physics claim, withdrawn claim quoted, source-refuted overstatement, contradicted reference) | P(0) = 0.55, P(1) = 0.30, P(>=2) = 0.15 |
| MAJOR findings | P(0) = 0.15, P(1-2) = 0.45, P(3-4) = 0.28, P(>=5) = 0.12 (median 2) |
| all findings (CRITICAL + MAJOR + MINOR + NIT) | median 16, 80% interval 9 to 26 |
| claims classified FAITHFUL (of those with a source) | about 85% (80% interval 72% to 93%) |
| a v1.2 deposit warranted by the rule of section 10 | 0.40 |
| planted controls: all 10 plants caught on the first run | 0.45; at least 8 of 10: 0.75 |
| paraphrase controls: none newly flagged on the first run | 0.55 |
| coverage target (section 9) met on the first run | 0.80 |
| a bibliographic contradiction (CRITICAL iv) | 0.08 |

I expect the audited numbers to be mostly right (293/293 plus several referee passes); I expect most trouble in the glosses (verb strength, scope, "decisive", "exactly", missing hypotheses of T4, the abstract's compression of two different levers), and in undeclared choices.

**11b. Pre-registered attention list (formed while reading the tex; NOT findings; each is tested in phase 2 and may be nothing; probability = P(it ends as a finding of at least MINOR)).**

- W1 (P2): "0.05 dex in D is a factor 1.5 to 1.8 in a0" and "-2.5 to -4.8 per baryon dex" versus the stated "local slope 0.13 to 0.28" (hand algebra gives 1.5 to 2.4 and -2.6 to -6.7 if m means the quantity defined in section 4): 0.45.
- W2: the abstract's "so" joins two different levers (baryon dex and the mass discrepancy D): 0.35.
- W3 (P5, P7): T4 as "any sample" while the Lean hypothesis is 0 <= b_i <= 1/2; `N>9` versus `N>=9`; T2b/T3 omitted: 0.50.
- W4 (P8): "decisive near-term test" while DR4 "cannot separate B from LCDM or Newton": 0.45.
- W5 (P3): Omega_m (and H0, flat?) is not stated where E(z) is used (line 40): 0.60 (MINOR).
- W6 (F1): "distinctive" without crediting standard MOND: 0.35.
- W7 (F5): the HW20 re-reading stated strongly (abstract: "scatters 0.64 dex about its own fit in its own table"): 0.35.
- W8: hard-coded "section~2" (line 95); tag B34 absent; B43 out of order: 0.50 (NIT).
- W9 (P4): the KiDS power 0.14 (a stage-A pre-flight number) and the jackknife error 0.038 (stage B) in one sentence: 0.30.
- W10 (section 5): B23, C19 lack volume/pages; "submitted to A&A" for ACE: 0.50 (MINOR).
- W11 (P1): "exactly as an a0 drift does" holds only at m = 1/2; at the KiDS lens y the sensitivities (1 - m) and m may differ: 0.40.
- W12 (P6): the break-even is for a log-uniform design with N = 20 and sigma = 0.1; the closing sentence of line 95 applies it to discs with y in 1.1 to 4.4: 0.40.
- W13 (P10): the audit matches numbers in place, not sentences; some rows are bare-number regexes: 0.60 (that at least some rows are weakly anchored).
- W14: the standing page's 2.3 sigma / 1.3 sigma statements (line 178) need their conditions: 0.25.

## 12. What this lane will not do

No edit of any repo file in phase 1; no edit of any PAPER38 file at any phase (the audit script, tex, pdf, zenodo json, deposit script included); no network; no new data; no deposit; no change to any frozen DR4 file; no claim that the paper is wrong or right in advance; no memory-only findings (those go to COULD-NOT-VERIFY); no repair of a failed control or a wrong estimate above (they are kept and graded).
