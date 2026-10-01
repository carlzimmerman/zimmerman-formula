# CFG265 -- Hostile, fair referee of the PAPER39 draft (closure map, NOT deposited): FROZEN CRITERIA (phase 1)

Written 2026-10-01 by the referee agent, BEFORE any CFG265 script exists and before any substantive check (no lane README, `.out`, `.json`, `.lean`, status page, closure-map file or DR4 file has been opened). **kappa = 1/2 is FITTED, NOT DERIVED.** Nothing here says the data favour any law; a lean is not a detection; failed controls and wrong expectations are kept, never repaired; nothing is called closed. The referee is **hostile but fair**: every finding cites a source (file and line, or a numbered recomputation); a memory-only concern goes to a separate "COULD NOT VERIFY (from memory, unverified)" list and never supports a finding.

**Subject (read-only, never edited by this lane):** `qwen_claude_field_theory/papers_2026/PAPER39_closure_map_2026.tex` (221 lines; committed in 53f374ae2; sha256 cfafe712560b95fb735c36c1bce6907d47d572ea6099f3e0ba1202444b5db58e), `PAPER39_audit.py` (317 lines; sha256 d95d057e462a4df0d1cbdd779e9019a4a50abf3ec50bbddda6bf8d0d7284a269), the `.pdf` and the `.zenodo.json`. Lane directory: `campaign_fresh_gravity/CFG265_paper39_referee/` (this lane writes nowhere else; it does not commit or push; no PAPER39 file and no other existing file is edited; the owner's personal name is written in no file).

**Model protocol:** CFG241 (the PAPER38 referee: `campaign_fresh_gravity/CFG241_FROZEN_CRITERIA.md`, its README, extractor, checker, findings). Lessons carried over: (L1) the trouble is in the glosses, not the audited numbers (CFG241's two MAJORs were an "in every lane" overstatement and a re-reading of named authors stated beyond its source); (L2) a lexical flagger misses key-only citation swaps and single-digit changes, so this lane adds a key-topic rule and a lane-attribution rule and plants both kinds; (L3) a paraphrase that the trigger rule does not extract is a vacuous pass, so all three paraphrases here are claim sentences; (L4) a rule changed after a miss is versioned, both outputs kept; (L5) sources are read at a pinned commit, not a moving HEAD.

## 0. Blindness declaration (what I read before freezing)

- **Read in full:** the PAPER39 tex (one pass, to enumerate structure and choose plants). **My hand estimates (section 11) are not blind to the text; they are blind to every source.**
- **Read partly:** `PAPER39_audit.py` lines 1-60 (docstring and the `SRC` dictionary: STAND, GAPS, TEN, TENG, D11, RD, VER, CFG0, R28, R230, R231, R232, R242-R245, R251, R259, LEANR, LEANV). I noticed that the `SRC` dictionary as printed in those lines has no entry for the READMEs of CFG29, CFG118, CFG131 or CFG253 or for any kappa note, which the tex's Reproducibility section lists as read (it may be defined further down; to be checked, W21).
- **Listings only (names, no contents):** `campaign_fresh_gravity/closure_map/`, the lane directories named in the tex, `fable_independent_2026/lean_2026/ChainCert/`, `gemini_pi_puzzle/`, `prep_2026/gaia_dr4_prep/` and its `dr4_ready_1/`.
- **Model files read:** CFG241 frozen criteria, README, `CFG241_common.py`, `CFG241_extract.py`, `CFG241_check.py`, the first entry of `CFG241_findings.json`, the first rows of `CFG241_classification.csv`. They carry PAPER38/DR4 facts (the DR4 per-pair constant c = 3.291 fixed by 4,342 pairs at floor 1.1614 and sigma_sys 0.02; the T4 premise 0 <= b_i <= 1/2; ChainCert 331). **Those items are NOT blind.**
- **Session memory index (in context at start; summaries, not sources):** it states, among other things, that the CFG259 re-score leaves B's UFD median within 0.005 dex at 3.5-3.9 sigma, Gate H moves H4 -> H2 with small margins, "pred >= 1.5 row 2.8 sigma under f = 0.7", the Boo I conflict moves nothing; that Milgrom's cH0/2pi fits SPARC as well as the framework (Delta chi2 5.3 vs 7.0) and "beats 1/2pi" holds only on the rho_Lambda footing; kappa 0.465 +- 0.076 / 0.55 +- 0.17; DR4 on 2 Dec 2026; the 32pi campaign leaves "the rational 4" underived; "no committed action produces B"; the Unruh/n = 2 route retired. **These items are NOT blind**; no finding may rest on them; each is re-read from a committed file.
- **Not read:** every lane README, `.out`, `.json`, `.lean`, the status page, the closure-map files, the DR4 preregistration and edge table, the kappa notes, the gemini note, the bib.
- **Throwaway enumerator (inline, not saved; section 3 rule):** 66 units (25 table-row units + 1 header row), **115 prose sentence units, all 115 claim sentences**, **25 table rows**, **140 claim units** in total. The committed `CFG265_extract.py` must reproduce 115 / 115 / 25 / 140; any difference is reported, not repaired.

## 1. Structure of the draft as seen (coverage accounting)

| part | tex lines | prose sentences (throwaway) | audit tags |
|---|---|---|---|
| title block, conventions (comments) | 22-30 | 0 | - |
| abstract (i)-(vii) | 32-34 | 12 | B01 |
| 1 The law, candidate B, the three gaps (`sec:law`) | 37-52 | 13 | B02-B06 |
| 2 What Lean certifies (`sec:lean`; 5 items) | 54-66 | 15 | B07-B08 |
| 3 The routes tried (`sec:doors`; longtable, 25 rows) | 68-136 | 13 (+25 rows) | B09-B32 |
| 4 The specification (`sec:spec`; S1-S6) | 138-155 | 17 | B33-B38 |
| 5 Satellites (`sec:sat`) | 157-168 | 13 | B39-B41 |
| 6 Gap 3: the coefficient (`sec:kappa`) | 170-176 | 8 | B42-B43 |
| 7 What would decide the rest (`sec:decide`) | 178-187 | 9 | B44-B46 |
| 8 Limitations (`sec:lim`; 6 items) | 189-198 | 9 | - |
| 9 Reproducibility (`sec:rep`) | 200-202 | 6 | - |
| References (12 entries) | 204-219 | section 5 below | - |

Reference keys: A20, AP26, D08, G26, HFB17, M09, M13, MC10, O26, P36, P38, V17. Lane ids in the text include CFG4, 28, 29, 43, 44, 48, 49, 50, 70, 72, 117-124, 130, 131, 151-159, 171, 172 (172D), 173, 188, 230, 231, 232, 240, 242-245, 251-254, 259. Named files: `campaign_fresh_gravity/STANDING_2026-09-29.md`, `closure_map/TEN_DOORS_GATES_2026-09-29.md`, `closure_map/RESEARCH_DIRECTION_2026-09-29.md`, `gemini_pi_puzzle/SOLVING_THE_PUZZLE.md`, `ChainCert/`, `PAPER39_audit.py`. Audit tags B01-B46 (B09 to B31 interleave the table rows; rows 4, 5, 11C-c and others carry no tag of their own).

## 2. Review protocol (per claim)

1. **Extract** all claims mechanically (section 3).
2. **Map** each claim to sources (section 3b).
3. **Read** the mapped passage (README paragraph, `.out` block, results JSON key, Lean statement) AROUND the number, and classify the claim with exactly one class (2a). Audited numbers are not assumed correct because the audit passes: the audit checks that a number exists in a file and in the tag block, not that the sentence around it says what the source says.
4. **Recompute** where the claim is physics or arithmetic (section 4). Where a README and its `.out`/results JSON differ, the output wins (the draft's own convention, line 30) and the discrepancy is itself reported.
5. **Severity** (2b) and proposed replacement wording.
6. **Report** class counts; `UNVERIFIABLE-OFFLINE` is a class with a reason code, never silently FAITHFUL.

### 2a. Classes

- **FAITHFUL**: every number reproduces from the cited source/recomputation within the displayed precision; the verb is no stronger than the source's; the scope is no wider; no source caveat that changes the reading is dropped.
- **OVERSTATED**: strength (verb, generality, certainty, scope, "every", "never", "exactly", "excluded", "preferred", "certifies") exceeds the source.
- **UNSUPPORTED**: no source line, committed output or recomputation supports the claim.
- **MISSING-CAVEAT**: the source attaches a qualifier (post hoc, not blind, a reading not a theorem, conditional, premise of a theorem, scoped to a frozen class, hand-check, toy-level, extrapolation, not independent, power) that changes how the sentence reads, and the draft drops it at that place.
- **WITHDRAWN-CLAIM-CREPT-BACK**: quotes or implies something a committed correction, withdrawal, ledger row or status-page rule retires.
- **CONTRADICTED**: the source or a recomputation gives a different value or statement (beyond 2b's tolerance). A table row whose class label is stronger than its lane's own verdict word (e.g. the row says "no-go" and the lane says UNDEFINED, NOT ADDRESSED, RESTATEMENT only, p* or "stop rule") is CONTRADICTED when the lane says the opposite and OVERSTATED otherwise.
- **UNVERIFIABLE-OFFLINE**: cannot be checked from files on disk; reason codes `NEEDS-NETWORK`, `SOURCE-NOT-ON-DISK`, `EXTERNAL-PAPER-NO-LOCAL-COPY`, `JUDGMENT-ONLY`.

### 2b. Severity (definitions frozen now)

- **CRITICAL**: (i) a false or contradicted numeric or physics claim, false meaning outside the displayed precision (half a unit of the last shown digit; one unit when the source prints a further digit and rounding is ambiguous); hedged claims ("about", "~", "nearly") false when off by > 25%; (ii) a withdrawn claim quoted or implied as live; (iii) an overstatement a source explicitly refutes (the source says NOT POSSIBLE, UNDEFINED, withdrawn, "not a theorem", "not to be quoted", and the draft says or implies the contrary); (iv) a bibliographic entry contradicted (first author, year, journal, volume, page, arXiv id) by the arXiv abstract page or the repo's own record; (v) a route-count or route-classification statement that a lane's own committed verdict contradicts. **A CRITICAL needs two independent supports**: a source line plus a recomputation, or two source lines, or one explicit source statement of the contradiction. Without the second support it is graded MAJOR at most.
- **MAJOR**: a missing caveat or overstatement that changes the conclusion a reader would draw (a theorem stated without premises a reader would then apply outside them; a requirement presented as established when its lane only fails one class; a "no-go" whose lane scopes it more narrowly in a way that matters; an unfair characterisation of a MOND, LCDM or named author's position that changes the reading; an internal contradiction between the abstract and the body on a headline); a hedged number off by 10-25%.
- **MINOR**: a dropped caveat that does not change the conclusion; ambiguous wording; hedged numbers off by < 10% but not at the displayed precision; undeclared choices a careful reader can recover; incomplete bibliographic entry; misattribution of a quotation or number to the wrong lane when the number itself is right.
- **NIT**: typography, cross-references, tag numbering, redundancy, grammar.
- **Tie rule:** between two severities the lower is assigned; a finding resting on an ambiguous source is MINOR at most and carries the quote.

## 3. Claim extraction (mechanical; script `CFG265_extract.py`)

**Text read:** the tex as committed at 53f374ae2 (`git show 53f374ae2:<path>`); sha256 printed and compared with the value above.

**Units.** Take the lines between `\begin{abstract}` and `\section*{References}`; drop comment lines (`%`), but attach `% AUDIT: Bnn` to the unit above; break units at blank lines, `\begin`, `\end`, `\toprule`, `\midrule`, `\bottomrule`, `\endhead`, `\setlength`, lone `{\small` / `}`, `\item`, and section commands. Inside `longtable`/`tabular` each line ending in `\\` is its own **row unit**; the first such row (`route & lane, commit & ...`) is the header and is not a claim.

**Sentences.** Split prose units at `[.?!]` followed by whitespace and an uppercase letter, backtick, backslash, `$` or `(`, after protecting `et al.\ `, `i.e.\ `, `e.g.\ `, `vs.\ `, `Eq.~`, `Table~`, `Section~` and decimal points. A `\textbf{Heading.}` whose period is followed by `}` stays attached to the next sentence.

**A claim** is a sentence or row with at least one of: (a) a digit outside `\ref`/`\label`/`\cite`/`\fpath`; (b) a trigger lexeme: *shows?, implies, proves?, theorems?, finds?, found, certif\*, predicts?, exclud\*, disfavour\*, consistent, cannot, must, needs?, never, every, only, decisive, strongest, tightest, largest, not, no, none, ill-conditioned, walled, decides?, determine\*, separate\*, lean, is, are, fail\*, no-go, kills?, forc\*, prefer\*, reproduc\*, gives?, requires?, at most, postulat\**; (c) it lies in the abstract, Section 7 or Section 8. Everything else is logged NON-CLAIM with the reason.

**Recorded per claim:** id (C001...), tex line, section, text, number tokens, trigger lexemes, lane ids, reference keys, universal-quantifier tokens (*any, every, all, whatever, always, never, however many, exactly, in every, at every, for any*), caveat tokens present, audit tag, text hash. Reference entries (12) and `\fpath{}` mentions (each must exist at 53f374ae2) are enumerated separately.

### 3b. Source matching (mechanical first pass, human verdict)

**Corpus (read at 53f374ae2; working tree only for untracked files, reported):**
1. every file of every lane named in the tex (directory `campaign_fresh_gravity/CFGnnn_*/` and top-level `CFGnnn_*` files, including `*_FROZEN_CRITERIA.md`), extensions `.md .out .txt .csv .json` (json <= 2 MB; read as text);
2. `campaign_fresh_gravity/STANDING_*.md`, `LEDGER.md`, `closure_map/*.md|*.out`;
3. `fable_independent_2026/lean_2026/ChainCert/`: `*.lean`, `README.md`, `verify_chain.out`, `Axioms.out`, `*Mutate.out`;
4. `gemini_pi_puzzle/*.md`; the 32pi campaign files and the two kappa notes (located in phase 2 by the audit's `SRC` entries and by grep for the quoted numbers 0.824, 1198, 5.34, 7.04);
5. DR4 (read only, frozen files never edited): `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`, `AMENDMENT*` texts, `dr4_ready_1/edge_table_dr4.json` and `dr4_ready_1/*.md`, `closure_map/DR4_DRESS_REHEARSAL_2026-09-29.md`, `CFG200_dr4_merge_band_forecast/` if it exists;
6. `citations/REFERENCES.bib`, `UNVERIFIED.md`, `CORRECTIONS.md`; the PAPER36 and PAPER38 `.zenodo.json` (for [P36], [P38]).
Excluded: CFG265 files.

**Map:** candidates are (i) the files of every lane named in the sentence or its unit; (ii) the audit row sources of its B tag (read from `PAPER39_audit.py` as text, never executed by the checker; used as pointers only); (iii) any corpus paragraph containing two of the claim's number tokens, or one number plus two content words. Paragraphs are blank-line blocks (long blocks split by line). Every claim gets a `source_map` row (files and lines, or NONE). The verdict is human, written to `CFG265_classification.csv` (id, class, severity, source file:line, rationale), and the checker **exits 2** if any claim has no row.

**Lane-level sources, not just audited numbers:** for every table row and every sentence naming a lane, the lane's README AND at least one committed `.out` or results JSON are opened, and the verdict word (FAIL / PASS / UNDEFINED / NOT ADDRESSED / RESTATEMENT / p* / stop rule / post hoc) is read from the lane's own verdict table.

### 3c. Mechanical flag families (`CFG265_check.py`; hints, not verdicts)

| family | rule |
|---|---|
| NUM | a number token is absent from the top-ranked mapped paragraph and from every mapped paragraph of a named lane (CFG241 v4 rule: integers match as integers; decimals by displayed precision; unicode minus unified); an "A to B" / "A--B" range must appear as a pair in a top paragraph |
| VERB | strongest claim verb level > the level of the best-matching source sentence; levels 0 descriptive, 1 (suggests, leans, gives, add), 2 (finds, indicates, implies), 3 (shows, demonstrates, certifies, reveals), 4 (proves, establishes, excludes, rules out, detects, confirms, rejects, decisive, refutes); negation-aware (CFG241 v2) |
| CAVEAT | a caveat token in the top source paragraphs is absent from the claim's unit: *post hoc, not blind, withdrawn, not to be quoted, not possible, non-diagnostic, non-discriminating, a reading, not a theorem, not a detection, conditional, hand-check, toy, not independent, unverified, hypothesis, assumes, premise, restatement, extrapolation, not a derivation, interpretation* |
| CITE | (a) a reference-list surname within 40 characters before `[KEY]` whose KEY's authors do not include it; (b) "Name et al.\ YEAR" or "(Name YEAR)" with Name not in the reference list (phantom); (c) **KEYTOPIC** (new, after CFG241's X5 miss): the claim's unit shares no 5-letter word prefix with the title of a key it cites (title words >= 4 letters, stopwords removed) |
| WITHDRAWN | a withdrawn-lexicon pattern without a retraction word in the same sentence. Frozen seeds: RC100 4.9/5.5/5 sigma; 5.09 keV; 2.55 keV; z* = 2.4; 180 theorems; BH*; lambda_J 2.7 Mpc; 74-89%; 6-8 sigma (forest); AeST+mu10 survivor; "theory (is) closed"; KiDS lead; L368; THE_EQUILIBRIUM_THEORY; "S8 neutral by theorem"; GP4 window; **kappa derived** (kappa ... derived / derives kappa / Unruh ... gives kappa = 1/2, exception words never, not, fitted, retired, underived); **"beats 1/2pi" without "only"**; **Omega_Lambda from a0** without "circular". Phase 2 adds patterns read from `STANDING_2026-09-29.md`, `closure_map/CLAIMS_AUDIT_2026-09-29.md` and `LEDGER.md` withdrawal rows (lexicon file committed) |
| SCOPE | a universal-quantifier token in the claim, and the top source paragraphs carry a hypothesis/scope marker (*if, provided, assum\*, hypothes\*, requires?, conditional, premise, for the P2 kernel, frozen class, spherical, monomial, pointwise, 0 <= b*) or lack the quantifier |
| ARITH | a hand-written table of >= 20 internal relations (section 4 P9) fails, and the claim contains the relation's anchor; plus **ARITH-COUNT**: the table's class counts (rows starting `no-go`, `no mechanism`, `realisable`) must equal the prose counts (25 / 22 / 2 / 1); on a mismatch every row of the over-counted class and the prose count sentence are flagged |
| LANE | (new) the claim names lanes L; a number token of the claim is found in no file of any lane in L but is found in another lane's files |
| CLASS | (new) for a table row: the class label's strength (no-go 3 > no mechanism (hand-check) 2 > realisable only 1) versus the lane's own verdict words in its README/`.out` and in the TEN_DOORS / DOOR11 result rows naming it; flag if the row says no-go and the lane's verdict lines carry UNDEFINED, NOT ADDRESSED, RESTATEMENT, p*, "stop rule", "hand-check", "phase 1", "realisable", or no FAIL/no-go/KILL/DEAD word |
| NOSRC | the claim has numbers or a shows/finds/confirms verb and no mapped paragraph supports it |

## 4. Physics re-derivations (frozen list; `CFG265_physics.py`, numpy/scipy/sympy; `CFG265_lean_read.py` reads only)

- **P1 Lean statements (read only; no build, nothing written into the repo).** For each certified statement of abstract (ii) and Section 2: print the exact Lean declaration (name, hypotheses, conclusion) from `Ownership.lean`, `Theory.lean`/wherever the EFE-linearity theorems live, `Dimension.lean`, `Action.lean`, `CalibrationWall.lean`, `Footing.lean`; compare each with the tex's paraphrase: (a) ownership non-local: the premise nu != 1, "same internal and external fields", what "function of the field data" means in Lean; (b) noEFE linearity: continuity, the additive functional equation, what "pointwise law with MOND's deep limit" and "scalar or vector" mean in the statements; (c) dimension: monomials only, the iff, the definition of "acceleration scale", hbar admissible; (d) AQUAL: x mu(x) increasing onto (0, inf), "reduced Euler-Lagrange" and "regularity" as premises, spherical; (e) calibration wall T1/T2a/T4 premises; (f) Footing: kappa = sqrt(2/(3 pi)) and which rho. Count theorem declarations per module and in total; compare 331, 47/219, 62/281, 50/331, "0 non-standard axioms", "0 sorry", "MUTATE=1 fails" with `verify_chain.out`, `Axioms.out`, the README.
- **P2 Dimension theorem (sympy).** Solve G^a M^b c^d [X^e] = length with b = 1/2 for X in {a0, hbar, Lambda, rho_Lambda, H0, a length, a mass}; confirm "no (G, M, c) monomial" and "exists iff (G, c, X) give an acceleration scale".
- **P3 AQUAL to kernel (sympy).** mu(x) = (sqrt(1 + 4x^2) - 1)/(2x): x mu(x) increasing onto (0, inf); invert to nu(y); compare with the P2 kernel as defined in the lanes/Lean (must be identical).
- **P4 Footing.** a0 = c H0/(2 pi) written as kappa c sqrt(G rho): rho = rho_crit gives kappa = sqrt(2/(3 pi)) = 0.4607; rho = rho_Lambda = Omega_Lambda rho_crit gives sqrt(2/(3 pi Omega_Lambda)) (about 0.557 at Omega_Lambda = 0.685). Read which rho `Footing.lean` uses and judge the tex's "kappa c sqrt(G rho) convention" (hand expectation: rho_crit; a reader of a paper whose law is written with rho_Lambda may misread).
- **P5 32pi algebra (sympy).** Lambda = 8 pi G rho_Lambda/c^2 implies R*^2 Lambda = 8 pi for R* = c/sqrt(G rho_Lambda); a0 = c^2/(2 R*) implies kappa = 1/2; C = Lambda c^4/a0^2 = 32 pi at kappa = 1/2 (state the units needed for "Lambda_geom/a0^2"); G rho_Lambda = 4 a0^2/c^2; the de Sitter horizon radius sqrt(3/Lambda) versus R* (ratio sqrt(8 pi/3)), to check "a radius that is not a horizon".
- **P6 kappa and BBN arithmetic.** (1.447 - 0.465)/0.076 = 12.9; 1/2 inside 0.465 +- 0.076 and 0.547 +- 0.175; R < 0.824 against G_BBN/G0 = 0.98 +- 0.06: the exclusion significance (hand: 2.6 sigma) and whether the lane and [A20] scope the BBN bound to a constant G during BBN; "Delta chi2 5.34 against 7.04 alt" against the kappa note (which footing each number belongs to).
- **P7 DR4.** From the preregistration and `edge_table_dr4.json` (read only): B = 1.000, floors 1.161/1.192, sigma_sys 0.02, the per-pair constant; re-derive the kill lines (1.084 for B, 1.077 for the bare law) at N = 30,000, the cap 8.1 sigma, 4,300 pairs for 3 sigma; compute the separation of 1.063 and 1.127 from 1.000 at N = 30,000 under the frozen error model (hand expectation from c = 3.291: about 2.3 and 4.6 sigma, so "2.3-3.7" may not follow), and of DOOR11_RESULT's 1.16-1.18; locate the committed source of "1.063-1.127" and of "2.3-3.7 sigma", and say which band is the record's.
- **P8 Satellites arithmetic.** 0.3245/sqrt(0.038^2 + 0.077^2) = 3.77; 0.068 and 0.104 as fractions of 0.3245 ("a fifth to a third"); +13.58/+11.32/+8.60, DV3 = 9 + 0.24, power 0.28, about -1.3 without UFDs, 33 of 40 clamped, H4 -> H2, "every 2026 variant"; the "weak-binary subsample ... 2.8 / 2.6 sigma" label against the CFG259 row it comes from; "capped near 2.5 sigma by systematic floors" (Section 7) against "3.5-3.9 sigma" (Section 5, abstract): locate the source of 2.5 sigma and decide whether the two statements are consistent.
- **P9 Internal arithmetic table (>= 20 relations, also the ARITH family):** 22 + 2 + 1 = 25 and the table's own class counts; 0 + 11 + 5 + 27 + 11 = 54; 219 + 62 = 281; 281 + 50 = 331; 219 - 47 = previous library size (README); sqrt(1000) = 31.6 for 1e9-1e12; 12.9 sigma; 3.77 sigma; cap (1.161 - 1)/0.02 = 8.05; kill lines; fifth/third; Gamma tau 0.79 x (5.17, 5.37) = 4.1-4.2; 0.79/(4.1-4.2); 1.7-1.9 H_Lambda against 5.17-5.37 ("nearly meet"); 2.8-38x and 1e-1376.8 (lane only); 0.16-0.21; 1.9e-4; R*^2 Lambda = 8 pi; kappa = sqrt(2/(3 pi)); route rows = 25; "ten doors" vs CFG151-159 (nine lanes, door 2 without referee).
- **P10 Audit anchoring.** Parse the rows of `PAPER39_audit.py`: count rows; BARE regexes (< 12 characters of context around the capture group) and whether their digits occur more than once in the source; the fraction of the tex's numeric tokens (outside `\ref`, lane ids and years) that sit in no audit literal of their own block; confirm the docstring's own statement that the route counts are not audited.
- **P11 PDF/tex drift.** If `pdftotext` exists, compare decimal tokens of the PDF with the tex; compare the `.zenodo.json` description with the abstract (numbers, the disclosure, "not deposited" status).
- **P12 Route recount (`CFG265_route_recount.py`, mechanical + hand).** For each of the 25 rows: the lane directory exists at 53f374ae2; the commit hash exists and touches that lane; the lane's frozen-criteria file exists and its first commit precedes (or equals, with the file order in that commit noted) the first commit of the lane's scripts (the tex claims "Each route below was given frozen criteria committed before its scripts"); the lane's own verdict words; the TEN_DOORS_RESULT / DOOR11_RESULT row for the door. Then recount the rows under the draft's own rule and under the lanes' own words; list any route that a source counts differently (merged, split, dropped, called restatement, UNDEFINED, NOT ADDRESSED, p*). Also check that the routes counted are the "routes to the missing object" and that excluded items (CFG44-72, CFG252, CFG254) are excluded consistently.
- **P13 Local phantom versus the CFG44 target (numeric).** For a point mass the QUMOND phantom density gives rho_ph r^3 g_tot = (a0/4 pi) M in the deep limit (and, for P2, also in the Newtonian limit: hand algebra); for extended spheres (Hernquist, Plummer, exponential-sphere; 1e9-1e12 Msun; P2 kernel) compute the maximum of C_ph/C_target and compare with "ratio up to 2.33 for P2". Sensitivity: profile and mass; the claim is CONTRADICTED only if outside the whole range and the lane's profile reproduces otherwise.

Tolerances: displayed precision (2b); a recomputation that needs a choice (Omega_m, kernel, profile, error model) is reported as a range; CONTRADICTED only if outside the whole range.

## 5. References: spot-check procedure and limits

**Offline:** parse the 12 entries; compare with `citations/REFERENCES.bib`, `UNVERIFIED.md`, `CORRECTIONS.md`, any local copies (HTML/PDF/tex) in the repo; check arXiv-id form against the stated year/month; "submitted"/"accepted" entries must not carry volumes; [P36]/[P38] DOIs against the repo's `.zenodo.json`/deposit records.

**Network (the only network use of this lane, read-only):** WebFetch of the arXiv abstract pages of **two pre-selected journal entries, chosen now: [HFB17] (Phys. Rev. D 95, 064019; arXiv:1702.04358) and [MC10] (ApJ 722, L209; arXiv:1009.4205)** (fall-backs, used only if a page fails: [D08], [M09]). Compared: title, authors, year, journal reference, and for HFB17 whether the abstract supports "Solar System misses by seven orders" as attributed in the row (or whether "seven orders" is the lane's own number). If budget allows, a labelled extra (not part of the frozen pair): [A20]'s abstract for the quoted G_BBN/G0 = 0.98 +- 0.06 and its scope.

**Cannot be done:** journal-side verification of volume/page beyond what the arXiv page shows; the content of the 2026 papers (AP26, G26, O26) beyond their abstract pages; whether any arXiv page is the final version. Each such item is reported "agrees with arXiv page / repo record, not checked against the journal".

## 6. Fairness checklist (scored FAIR / UNFAIR-TO-MOND / UNFAIR-TO-LCDM / UNFAIR-TO-NAMED-AUTHORS / UNDECLARED / N-A, with tex line)

F1 Is B's UFD failure attributed to B (ownership: satellites obey the isolated law) and not to MOND generally (standard MOND with an EFE predicts differently)? F2 Is the LCDM comparator at satellites (clamped SHMR [M13] + NFW [D08]) described as the record's construct, with its extrapolation stated where the lean is first stated (abstract)? F3 Are named theories (Verlinde, BIMOND, Mashhoon, Deser-Woodard, mimetic, superfluid, Hossenfelder) described as the lane's frozen version, not the authors' full theory, and is each named author cited? F4 Is "excluded" for the 32pi branch scoped (BBN, constant couplings, transfer assumptions)? F5 Is Milgrom's footing treated symmetrically ("fits as well"; "beats 1/2pi only on the rho_Lambda footing")? F6 Is the gemini note's claim characterised fairly (what it says vs what the status page says)? F7 DR4: is it called a survival test (not decisive for B) everywhere, and is the bare law's kill line given equal weight? F8 Is the menu's non-blindness and the referees' non-blindness stated where the route count is first stated (abstract)? F9 Are owner-directed lanes credited without implying they were blind or independent? F10 Selective literature: is the absence of a literature review declared? F11 Undeclared choices: kernel (nu_mono vs P2), footing, Omega_m, r_ta convention, error model. F12 AI-assisted / not peer reviewed disclosure in the title block and the `.zenodo.json`.

## 7. Planted-error controls (scratch copies only; one plant per copy; never the real tex)

The pipeline runs on (i) the unmodified tex (baseline flags F0) and (ii) each scratch copy (F1). A plant is **caught** iff F1 has at least one flag of an **expected family** on the planted claim that is not in F0 for the original claim. A **paraphrase passes** iff F1 for the paraphrased claim adds no flag to F0. If an `old` string is not found exactly once the control fails (exit 3). Plants are frozen now and are not tuned after a miss; any rule change is versioned and both outputs kept.

| id | kind | tex line | old (exact) -> new (exact) | expected family |
|---|---|---|---|---|
| M1 | numeric swap | 115 | `$n(t_{\rm ff})=0.791$, minimum 0.143` -> `$n(t_{\rm ff})=0.917$, minimum 0.143` | NUM |
| M2 | stronger verb | 136 | `The day's four swings (CFG242--245) add that ownership must remember boundness` -> `The day's four swings (CFG242--245) prove that ownership must remember boundness` | VERB |
| M3 | dropped caveat | 136 | `\textbf{A cross-door pattern, a reading and not a theorem.}` -> `\textbf{A cross-door pattern.}` | CAVEAT |
| M4 | wrong citation (surname) | 82 | `2 Verlinde [V17]` -> `2 Verlinde [M09]` | CITE |
| M5 | withdrawn claim | 33 | `with $\kappa=\tfrac12$ fitted, never derived` -> `with $\kappa=\tfrac12$ derived from the de Sitter Unruh temperature` | WITHDRAWN |
| M6 | scope inflation (dropped premise) | 64 | `with $f$ free, $\sigma(\log a_0)\ge3\sigma/\sqrt N$ (conditional on local slopes in $[0,\tfrac12]$)` -> `with $f$ free, every sample and every kernel obeys $\sigma(\log a_0)\ge3\sigma/\sqrt N$` | SCOPE or CAVEAT |
| M7 | order-of-magnitude range | 123 | `against $\approx4.1$--4.2 needed & no-go (Gate T)` -> `against $\approx41$--42 needed & no-go (Gate T)` | NUM |
| M8 | invented support + phantom citation | 136 | `and that the fluid must exist before structure.` -> `and that the fluid must exist before structure. A Bullet Cluster lensing reanalysis independently confirms the early-fluid requirement at 4$\sigma$ (Clowe et al.\ 2027).` | NOSRC or CITE |
| M9 | count arithmetic | 70 | `gives 25 routes: 22 scoped no-gos` -> `gives 25 routes: 23 scoped no-gos` | ARITH |
| M10 | cumulative arithmetic | 56 | `(62 theorems, 281)` -> `(62 theorems, 291)` | ARITH or NUM |
| M11 | inequality direction swap | 180 | `$\hat\gamma\ge1.084$ kills B; $\hat\gamma\le1.077$ kills the bare law` -> `$\hat\gamma\le1.084$ kills B; $\hat\gamma\ge1.077$ kills the bare law` | ARITH |
| M12 | wrong lane attribution | 142 | `(CFG243; the baryon-only $\sigma_b$ is 0.076 against the threshold 1.276)` -> `(CFG253; the baryon-only $\sigma_b$ is 0.076 against the threshold 1.276)` | LANE |
| M13 | key-only citation swap (CFG241's X5 kind) | 186 | `[O26, MC10]` -> `[O26, M09]` | CITE |
| M14 | route class upgrade | 87 | `encodes $C(r)$, not derives it & realisable only` -> `encodes $C(r)$, not derives it & no-go` | CLASS or ARITH |

Faithful paraphrases (must NOT be newly flagged; all three are claim sentences under the section 3 rule):
- **P-a** (140): `Each item is a necessary condition read off the failures of scored classes; none is shown sufficient, and the set is not shown jointly satisfiable.` -> `Each item is a necessary condition inferred from the failures of the scored classes; none has been shown sufficient, and the set has not been shown to be jointly satisfiable.`
- **P-b** (197): `A lean is not a detection.` -> `A lean should not be read as a detection.`
- **P-c** (96): `no stationary state; a ghost for $0<g t<2/3$` -> `there is no stationary state, and a ghost appears for $0<g t<2/3$`

**Self-disable:** M1 with `--disable NUM` must exit 1 (the control can fail). Total: 14 plants of 14 kinds (numeric, verb, caveat, citation-surname, withdrawn, scope, magnitude-range, invented+phantom, count arithmetic, cumulative arithmetic, direction, lane attribution, key-only citation, class) + 3 paraphrases + 1 self-disable = 18 control runs.

**Exit codes (frozen):** `CFG265_extract.py` 0 if 115/115/25/140 reproduced, 1 otherwise (kept); `CFG265_check.py` main 0 if the pipeline completed and the coverage target (section 9) is met, 2 otherwise (findings never change the exit code); `--plant` 0 only if all 14 plants are caught and no paraphrase is newly flagged, 1 otherwise (misses printed and kept), 3 if an `old` string is missing; `CFG265_physics.py` 0 if its known-answer self-controls pass (nu -> 1 Newtonian, nu -> y^-1/2 deep, P2 identity from the AQUAL mu, dimension solve recovers GM/c^2 for (G, M, c), the DR4 constant reproduces 4,342 pairs, R*^2 Lambda = 8 pi), 1 if one fails; a contradiction prints `CONTRADICTS`, not an error exit; `--mutate` perturbs one input and must exit 1; `CFG265_route_recount.py` 0 if it completed (discrepancies printed); `CFG265_refs.py` 0 if it completed.

## 8. Script plan (all in `campaign_fresh_gravity/CFG265_paper39_referee/`)

`CFG265_common.py` (repo discovery via `ZF_REPO` or walking up; reads at 53f374ae2; `<repo>` scrubbing; extraction), `CFG265_extract.py`, `CFG265_check.py`, `CFG265_route_recount.py`, `CFG265_lean_read.py`, `CFG265_physics.py`, `CFG265_refs.py`, `CFG265_run_all.sh`; hand tables `CFG265_classification.csv`, `CFG265_findings.json`, `CFG265_refs_webfetch.json` (the WebFetch transcriptions, typed by hand from the fetched pages); outputs `*.out`; `README.md` (phase-2 report). Stdlib + numpy/scipy/sympy; each script <= 15 min; no absolute home path printed; no network inside scripts (the WebFetch is done by the referee and transcribed); plants run in temporary copies deleted after the run.

## 9. Coverage target

- 100% of the 140 claim units classified (exit 2 otherwise).
- At most 10% UNVERIFIABLE-OFFLINE.
- 100% of the number tokens in the abstract, the Section 3 table, Section 4 (S1-S6) and Section 7 individually checked against a source or recomputation.
- All 25 table rows opened at the lane level (README + one `.out` or results JSON).
- If a target is missed the README says MISSED and gives the achieved fraction.

## 10. Output format and the revision rule (v1.1 rule)

Findings ranked CRITICAL / MAJOR / MINOR / NIT, each with id, tex line(s), class, source file:line (or recomputation id), evidence and proposed replacement wording, in `CFG265_findings.json` and the README. **Frozen rule: any CRITICAL, or two or more MAJOR findings on text the draft itself states, means a revision (v1.1 of the draft) is warranted before deposit; otherwise "not warranted, list for a later revision".** The owner decides. The README also gives: coverage counts; the route-count verdict; the controls' outcomes including misses; the FAITHFUL list; the UNVERIFIABLE-OFFLINE list; the COULD-NOT-VERIFY list; the fairness scores; the hand estimates graded.

## 11. Hand ESTIMATES (made after reading the tex, before any source)

**11a.**

| quantity | estimate |
|---|---|
| CRITICAL findings | P(0) = 0.50, P(1) = 0.30, P(>= 2) = 0.20 |
| MAJOR findings | P(0) = 0.15, P(1-2) = 0.45, P(3-4) = 0.28, P(>= 5) = 0.12 (median 2) |
| all findings | median 20, 80% interval 10 to 32 |
| FAITHFUL fraction of the 140 claim units | about 80% (80% interval 68% to 90%) |
| revision warranted by the section 10 rule | 0.55 |
| the 25 / 22 / 2 / 1 recount reproduces under the draft's own row rule | 0.60 |
| at least one row's class label is stronger than its lane's own verdict word | 0.55 |
| "1.063-1.127 ... 2.3-3.7 sigma" reproduces under the frozen DR4 error model | 0.35 |
| Footing's kappa = sqrt(2/(3 pi)) uses rho_crit (Omega_Lambda = 1), not rho_Lambda | 0.60 |
| every route lane has a frozen-criteria file committed before its scripts | 0.45 |
| all 14 plants caught on the first run | 0.30; at least 11 of 14: 0.70 |
| no paraphrase newly flagged on the first run | 0.50 |
| coverage target met on the first run | 0.75 |
| a bibliographic contradiction on the WebFetch pair | 0.10 |

**11b. Attention list (formed while reading the tex; NOT findings; P = probability it ends as a finding of at least MINOR).**

- W1 DR4 "1.063-1.127 ... 2.3-3.7 sigma at N = 30,000": the upper end looks like about 4.6 sigma under c = 3.291 and sigma_sys 0.02; and the band differs from DOOR11_RESULT's 1.16-1.18: 0.55.
- W2 Rows 11A and 11C-a are "no-go (restatement)": counting a restatement as a scoped no-go may be stronger than the lanes' word: 0.50.
- W3 "Each route below was given frozen criteria committed before its scripts": some route lanes (CFG130, CFG131, CFG171, CFG173) show no top-level frozen-criteria file in the listing: 0.40.
- W4 Lean (a)-(d) paraphrases versus the statements' premises ("certifies ... that ownership is not a function of local field data"; "a continuous law with no EFE is linear"): 0.40.
- W5 "no pointwise law with MOND's deep limit is EFE-free, in scalar or vector form": premises of `law_not_efeFreeRay` / `vecLaw_not_efeFree`: 0.35.
- W6 Footing: "In the kappa c sqrt(G rho) convention Milgrom's value is kappa = sqrt(2/(3 pi))": which rho: 0.45.
- W7 "Milgrom's cH0/2pi fits SPARC as well as the framework (Delta chi2 5.34 against 7.04 alt)": which number belongs to which model and footing; "as well" with a smaller Delta chi2 for Milgrom: 0.35.
- W8 32pi: "that branch is excluded" by BBN at about 2.6 sigma (R < 0.824 vs 0.98 +- 0.06), and whether BBN's bound is scoped to a constant G: 0.50.
- W9 Internal tension: Section 5 and the abstract say the bound-core reading "is preferred"; Section 7 says the lean "would need its power raised well above 0.28 before it could be called a preference": 0.60.
- W10 "The ultra-faint test is capped near 2.5 sigma by systematic floors" versus B's failure at 3.5-3.9 sigma: 0.45.
- W11 "CFG29's weak-binary subsample ... 2.8 sigma / 2.6 sigma" versus a "pred >= 1.5" row label in the record: 0.40.
- W12 "Under every 2026 variant both kernels cross the line": "every": 0.35.
- W13 HFB17 attribution of "seven orders" (lane number or the paper's?): 0.35.
- W14 "Hossenfelder's covariant Lagrangian" named without a reference: 0.40 (MINOR/NIT).
- W15 Reproducibility: the sources list (CFG29, CFG118, CFG131, CFG253, the kappa notes) versus the audit's `SRC` (lines 1-60): 0.40.
- W16 "the four swings CFG242-CFG245 of 2026-10-01": the date: 0.25.
- W17 S1-S6 stated as requirements ("must") when each lane fails one class: the section's opening sentence scopes them ("necessary condition read off the failures of scored classes"); individual items may still overreach (S3 "a rate no vacuum candidate provides"; S1 "is exactly what such classes cannot supply"): 0.50.
- W18 "CFG230 ... finds that only R01 and R02 are met by any scored row as a mechanism": 0.30.
- W19 [P38] "version 1.2, doi 10.5281/zenodo.23085582": whether a v1.2 deposit exists in the record: 0.30.
- W20 "a decisive test would need baryon masses calibrated to 0.10 dex" (line 39): PAPER38's range is wider (0.02-0.15 dex per CFG241): 0.30.
- W21 Table row 2 "Verlinde [V17]" while "door 2 has no referee": fine; but the Verlinde row's G5 entry rests on HFB17: 0.25.
- W22 Fairness: B's UFD failure must not read as a failure of MOND: 0.25.
- W23 The abstract's (iv) packs lane numbers (10^-1376.8, 0.791, 0.33-0.34, 0.79, 4.1-4.2) without "on its frozen class" at that place: 0.40.

## 12. What this lane will not do

No edit of any existing repo file at any phase; no edit of any PAPER39 file; no commit, no push, no deposit; no change to any frozen DR4 file; no Lean build (it would write into the repo tree); network only for the arXiv pages of section 5; no claim that the draft is right or wrong in advance; no memory-only findings; no repair of a failed control or a wrong estimate.
