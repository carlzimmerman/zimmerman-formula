# K -- literature audit of published claims to derive or explain alpha (pre-registration)

Written 2026-09-28 BEFORE any computation in this lane was run and before any source was read for this lane. Only lane D's bar (alpha_bar_checker.py, its selftest 11/11,
D_PREREGISTRATION.md, d2_audit_known_formulas.out) was read. Everything I say about a claim BEFORE fetching its source is RECALLED and is labelled so; each per-claim
table row will say whether the source was read in FULL TEXT, ABSTRACT ONLY, or via a SEARCH SNIPPET / secondary page.

Target: 1/alpha = 137.035999177 (Thomson limit, CODATA 2022), delta_CODATA = 1.6e-10. Bar = lane D's: P_lookelsewhere < 1e-3, miss <= 5e-10 (or the route's own a-priori predicted
precision), zero fitted reals, scale of alpha stated. Checker used unmodified: ../D_calibration_bar/alpha_bar_checker.py (imported as a module; nothing in D is edited).

## Claims to audit (declared list, 12 items; count fixed now, any addition is an Amendment)
K1  Eddington: 1/alpha = 136, later 137 (16*17/2 [+1]).                                    [recalled]
K2  Gilson (and other small-integer geometric formulas, e.g. 4 pi^3 + pi^2 + pi).            [recalled]
K3  Atiyah 2018 (Todd function claim).                                                       [recalled]
K4  Nambu 1952 (masses as multiples of 137/2 m_e) -- ONLY its alpha content; Koide-type relations are audited only to record whether they contain alpha (expected: no; then out of scope, SM mass sector is walled).  [recalled]
K5  Wyler 1969/71 (already scored by D; here only its structure, criticism and the 2015-2026 status).
K6  Adler 1972 (eigenvalue condition for alpha in finite/massless QED; and his Wyler comments)                              [recalled, poorly]
K7  Bekenstein 1982 varying-alpha theory.                                                    [recalled]
K8  Sandvik-Barrow-Magueijo 2002 (BSBM) varying-alpha cosmology.                             [recalled]
K9  Combinatorial hierarchy (Parker-Rhodes / Bastin-Kilmister / Noyes): 137 and the refinement 137.03596...  [recalled]
K10 Anthropic / environmental explanations of alpha's value (Barrow-Tipler, Carr-Rees, Barr-Khan).   [recalled]
K11 Recent (2015-2026) derivation claims: to be found by search; declared quota: audit the 3 most cited or most prominent that state a closed formula or a mechanism; the selection rule is
    'peer-reviewed or arXiv with >= 1 independent published critique, stated numerical prediction', chosen from the first two search result pages, not after computing anything.
K12 Johnson-Baker-Willey / Gell-Mann-Low eigenvalue condition (structural ancestor of K6) and Sommerfeld/Bohr/Feynman-type 'mystery' remarks: no formula, so only the structural verdict.

## Per-claim protocol (fixed now; identical for every claim)
(a) precise statement with the source; (b) free choices, listed as an integer count F of independent discrete choices (integers, exponents, constants, operations) and a count of fitted reals;
(c) run through the D checker in THREE ways, all reported: P_MDL (checker default, expression shape, intmax = max(12, largest integer in the formula), P as the checker prints it);
    P_forced (N = 1: every choice assumed forced by the author's derivation -- the steelman); P_decl (size declared in Amendment 1 from the free choices actually documented in the source, BEFORE running);
    also miss, miss in sigma_CODATA, fitted reals, scale-of-alpha-stated; (d) strongest published criticism, with source and whether read; (e) STRUCTURAL verdict.
A formula is a NUMERICAL WIN only if all four bar criteria hold under P_decl AND under P_MDL with intmax as above. Failing P_MDL but passing P_forced is reported as 'passes only if every choice is forced'.

## Structural-survival rule (fixed now)
An idea S is a SURVIVING STRUCTURAL IDEA iff ALL of:
 S1 it is a mechanism/principle (a condition that would determine a coupling), not merely a numerical expression;
 S2 as stated it has zero fitted reals and its inputs are dimensionless numbers with independent definitions;
 S3 it makes at least one testable statement beyond reproducing alpha (a second observable, a bound, a running or a variation law);
 S4 it is NOT already closed by lanes A,B,C,E,F,G (their published verdicts, read as summarised in their .out files) and not refuted by CODATA on its own terms.
Score S1..S4 each 0/1. Survives iff 4/4; 'partly survives' 3/4 (say which fails). Ranking of the table: (1) bar cleared (none expected), (2) structural score, (3) log10(P_decl) ascending, (4) miss.
Hypotheses (declared so they can be false):
 H1 no published closed formula clears the bar (P_decl < 1e-3 and miss <= 5e-10 and 0 fitted reals): expected TRUE. It is FALSE if any does; then it is verified twice with a fresh implementation.
 H2 every small-integer formula with miss > 1e-6 has P_MDL > 0.5: expected TRUE.
 H3 at least one structural idea reaches 3/4: expected TRUE (eigenvalue condition, dynamical attractor); none reaches 4/4: expected TRUE.
 H4 the Atiyah claim as published has no closed numeric statement of an alpha value reproducible from a stated formula: unknown; only what is in the source will be scored.
Outputs: k1_numeric_audit.py (+ .out, MUTATE control), k2_structural_scoring.py (+ .out, MUTATE control), K_REPORT_TABLE.md (the ranked table), source notes in sources/. MUTATE controls declared:
 k1 MUTATE (argv `--mutate`): feeds every formula the precision it does not have (miss set to 1e-11); the audit must then report at least one false clear, proving the checker step is live (exit 1 when so).
 k2 MUTATE (argv `--mutate`): sets S2 of every idea to 1 regardless of content; the scorer must then report a spurious survivor (exit 1).
 Real runs must exit 0.

## Not done / limits
No derivation proposed. Web sources only via WebSearch/WebFetch (summaries produced by a small model over fetched pages) and pdftotext where a PDF is fetched to disk; a WebFetch summary is not full text and will be marked as such.
SM mass sector walled; kappa = 1/2 FITTED; no dark-matter particle.

## Amendments
(none yet)

### Amendment 1 (2026-09-28; written after the LITERATURE READING and BEFORE any computation of this lane; nothing below was computed yet)
Reading log (what was actually read, so the per-claim 'source status' is auditable). FULL TEXT = fetched as PDF and read with pdftotext in this session; SUMMARY = a WebFetch model summary of a page (NOT full text);
SNIPPET = WebSearch result snippet only.
* Jentschura and Nandori, arXiv:1411.4673 (EPJ H 2014): FULL TEXT (Wyler, Rosen, Eddington-number, Dirac/Weyl, KK, RG sections).
* Atiyah, 'The Fine Structure Constant' (the manuscript hosted by a university web page, 17 pp.): FULL TEXT. Cook's blog and a news report on the Riemann-hypothesis claim: SUMMARY (critics quoted there: Litt, Buckley).
* Kragh, arXiv:1510.04046 (Eddington's theory of everything): FULL TEXT (136 = 16 + 16*15/2; the move to 137; Pauli's 1929 verdict).
* Dattoli, arXiv:1009.1711 (ENEA report, 'numerical alchemy'): FULL TEXT of pp.1-14 (Gilson's formula and its stated value; the author's own remark that the formula has no physical motivation). Anastassov, arXiv:physics/9712044 (3 pp.): FULL TEXT.
* Adler: his own commentary on his 1972 paper (book commentaries, arXiv:hep-ph/0505177, chapter on QED): FULL TEXT of that chapter's relevant pages. The 1972 paper itself (PRD 5, 3021) and PRD 10, 1894: SNIPPET/abstract via search only (publisher page returned 403).
* Noyes, arXiv:hep-th/9707020 (combinatorial hierarchy, 42 pp.): FULL TEXT of the alpha derivation section. Critique of the hierarchy: SNIPPET only (search summaries).
* Sandvik-Barrow-Magueijo, arXiv:astro-ph/0107512 (4 pp.): FULL TEXT. Bekenstein 2002 (gr-qc/0208081): FULL TEXT of abstract/introduction; Bekenstein 1982 (PRD 25, 1527): SNIPPET (abstract) only.
* Nambu 1952 (Prog. Theor. Phys. 7, 595): SNIPPET only. Rosen (PRD 13, 830, 1976): SNIPPET plus the description in 1411.4673 (FULL TEXT of that description). Anthropic bounds: SNIPPET only.
* 2024-2026 claims: Bleger (Zenodo, 2026-04-23), Blandino (Zenodo, 2026-04-28): SUMMARY of the record page only. Reinisch (APL Quantum 1, 016111, 2024): abstract via SNIPPET only (publisher 403).
* Sherbon (4 pi^3 + pi^2 + pi): SNIPPET only; the formula also appears inside the Blandino summary.

K11 outcome (declared before computing): the selection rule as pre-registered ('peer-reviewed or arXiv with >= 1 independent published critique, stated numerical prediction') was applied to the first two search result pages.
 EXCLUDED, no stated 1/alpha prediction (abstract read via SUMMARY): Sticker arXiv:2512.07027; Lipovka arXiv:1608.04596.
 NO ITEM on those pages satisfies the rule in full (none had a published independent critique that I could find). To avoid returning an empty K11, the rule is RELAXED, visibly, to: 'states a closed formula or model value for 1/alpha, dated 2015-2026',
 quota still 3: K11a Bleger 2026 (Zenodo, self-published, not peer reviewed, no critique found), K11b Blandino 2026 (same status), K11c Reinisch 2024 (peer reviewed, abstract only).
 Named in search results but NOT audited (not read; count = 6): 'Primeon Theory', 'Holographic Bit-Mode Balance', 'Lorentz-covariant tensor field harmonic cascades', 'Maya discrete lattice', 'Emergent C-Space', 'Purely Mathematical Derivation within 1.62 sigma' (Preprints.org). Listed so nothing is hidden; no verdict on them.
Added claims (count now 14, not 12): K13 Rosen (4 pi/(N(N-1)), N = 42); K14 Sherbon (4 pi^3 + pi^2 + pi) as a separate row from K2's Gilson; K2 is also extended with the small formulas quoted in the full-text sources (Anastassov's list, Dattoli's own).

Formulas fixed now (values NOT yet computed; T = 137.035999177; every 1/alpha; alpha-form claims are inverted):
 K1a 1/alpha = 16 + 16*15/2 (= 136). K1b 1/alpha = 137 (= 136 + 1).
 K2a Gilson: 1/alpha = pi / (29 cos(pi/137) tan(pi/(29*137)))   [as quoted by the search snippet and Dattoli's text; the exact typeset form in Dattoli is garbled by pdftotext, so I use the search-snippet form and ALSO check that it reproduces the value 137.035999786699 printed in Dattoli; if it does not, the row is marked UNVERIFIED and no verdict is given].
 K2b Anastassov's listed formulas from Eagles 1976 (values as printed in the source, recomputed): 108 pi (8/1843)^(1/6); 4 pi^5/9 + 37/36; sqrt(137^2 + pi^2). Dattoli's own Pythagorean formula is the last one. Anastassov's own alpha_rho: only the stated value 137.035989392 is used (formula garbled in the text; NOT reconstructed).
 K3 Atiyah: as stated (value '137.035999...', no evaluable procedure expected); two internal checks declared: (i) the recursion printed as (8.1)-(8.3) is self-consistent or not (k(1) from 'log k(j+1) = k(j)' versus 'k(j+1) = 2k(j)' with k(0)=0); (ii) whether a product of unit-modulus roots of unity can equal 137.036 (|product| = 1).
 K5 Wyler: 1/alpha = 8 pi^4/9 * (2^4 5!/pi^5)^(1/4), by the checker in three ways; D's W1/W2 templates are cited, not rerun.
 K9 combinatorial hierarchy: 1/alpha = 137 / (1 - 1/(30*127)).
 K13 Rosen: 1/alpha = 42*41/(4 pi).   K14 Sherbon: 1/alpha = 4 pi^3 + pi^2 + pi.
 K11a Bleger: 1/alpha = 19596/143 + 5R/(6370 - 2R), R = ln(2 + sqrt 3) [from the record summary; a summarizer could have garbled it: the script prints the value and, if it is not 137.035999181 to 1e-9 as the record says, the row is marked UNVERIFIED].
 K11b Blandino: 1/alpha = A - 1/(24 A) - 1/(A^2 pi^2 K), A = 4 pi^3 + pi^2 + pi, K = 9.9327912864 with K stated by the source as derived from CODATA 2022 => ONE FITTED REAL (declared now; c3 fails by the source's own account).
 K11c Reinisch: 1/alpha = 1/(7.364e-3) (stated model value; author's own stated error 'about 1%', mean-field): SCORED ONLY AS A STATED NUMBER, no P_decl (abstract only, no formula).
 K4 Nambu, K6 Adler, K7 Bekenstein, K8 BSBM, K10 anthropic, K12 JBW: no closed value for alpha; numeric column = 'none stated'; structural scoring only. For K6/K7/K8/K10 the 'number of fitted reals' column uses what the sources themselves say.

Declared families for P_decl (slot ranges, fixed now, product = N_decl; distinct-ness ignored, which OVER-counts and is therefore generous to the checker's sceptical side and conservative against the claim):
 K1a/K1b: n + n(n-1)/2 + c, n in 1..32, c in {0,1}: N = 64.
 K2a Gilson: pi/(a cos(pi/b) tan(pi/(a b))), a, b in 1..200: N = 40000. Supplementary declared computations for K2a: (s1) empirical scan of that family (all 40000 members): count of members within 1e-9, 1e-8, 1e-7, 1e-6 of T, against the checker's predicted lambda; (s2) with b = 137 fixed as in the source, the REAL a* that would hit T exactly, and the distance of the source's a = 29 from a*; the chance that some integer lies within that distance of a real target is 2|a - a*| per unit spacing (declared as the rounding test); (s3) the small-1/b expansion 1/alpha = b + pi^2/(2b) - pi^2/(3 a^2 b) + ...: what part of the match is carried by each term.
 K2b list: P_decl := P_MDL (no slot template declared; these are single fixed-shape formulas).
 K9: A/(1 - 1/(B C)), A in 1..200, B in 1..60, C in 1..255: N = 3.06e6.
 K13: 4 pi/(N(N-1)), N in 1..200: N = 200 (the shape is fixed by the source; alternatives in shape are counted by P_MDL).
 K14: c1 pi^3 + c2 pi^2 + c3 pi, c_i in 1..12: N = 1728.
 K11a: a/b + c R/(d - e R), a in 1..20000, b in 1..200, c in 1..10, d in 1..7000, e in 1..5: N = 1.4e12 (R fixed as the single constant).
 K5: P_MDL (checker default) and P_forced (N = 1) only; D's W1/W2 numbers are cited from d2_audit_known_formulas.out.
 K3, K11b, K11c: no P_decl (K3 no evaluable formula; K11b has a fitted real so c3 fails regardless; K11c abstract only).
Scale of alpha stated (c4) is scored from what the source says; where a source is silent it is scored 'not stated' (fails c4).
Structural rubric (k2_structural_scoring.py) content is fixed by the S1-S4 definitions above; per-idea evidence lines are written into the script with source labels, and are not changed after the MUTATE run.
Ranking (unchanged): (1) bar cleared, (2) structural score, (3) log10 P_decl ascending where defined, (4) miss.
Count of computations declared: k1 (numeric audit incl. supplementary s1-s3 and Atiyah checks i-ii) and k2 (structural scoring), each with a MUTATE control = 4 script runs plus reruns for exit codes.

### Amendment 2 (2026-09-28, still before any computation of this lane)
* K3 extra check (iii), declared now: implement the recursion in Atiyah's (8.1)-(8.4) literally under two readings (A: k(j+1) = 2 k(j) with k(0) = 0 so k = 0; B: k(j+1) = 2^k(j) [log2 k(j+1) = k(j)] with k(0) = 0 replaced by k(1) = 1 as the only consistent start) and record whether the product of v(j) or the last v(j) approaches 137.036 in 40 steps. This is a guess at an ambiguous text: a failure to reach 137.036 is NOT a refutation of what the author intended; it only shows the printed text does not define a computation that yields the number.
* Exit-code convention for k1: exit 1 iff ANY row passes all four bar criteria under P_MDL or under P_decl (the loosest reading); exit 0 otherwise. H1 is therefore tested in its strongest form. Rows are also flagged 'would pass if all choices forced (N=1) and the scale were granted', reported for information and not used for H1.
* The MDL size for K11b uses A and K as named leaves; for K11a R is a named leaf. The checker's evaluator cannot evaluate cos/tan, so for K2a the value is computed here with mpmath and the size is taken from the checker's own mdl_size on the shape (cos, tan count as unary decorations); for expressions the checker CAN evaluate (Wyler, Sherbon, Rosen, Noyes, small formulas) the script asserts that assess(expr=...) and the script's route agree.

### Amendment 3 (2026-09-28; after k1 was run and BEFORE k2 was written or run; the k1 results are in k1_numeric_audit.out)
Recorded honestly, changes to plan:
* k1 result that changes how P_decl is read: for K2a (Gilson) the flat-density P_decl (N = 40000, 8.9e-6) UNDERSTATES the chance, because with b = 137 fixed by the data the family collapses onto a one-parameter grid (relative spacing 1.4e-8 near a = 29); the rounding test s2 (declared in Amendment 1) gives the appropriate look-elsewhere number, 0.61. The table uses the LARGER of P_decl and, where declared, the rounding chance (P_used). No other row has such a data-selected sub-line by construction.
* k2 MUTATE control redesigned BEFORE running: the declared control (S2 forced to 1 for every idea) is expected NOT to create a spurious survivor, because in my rubric every idea with S1 = S3 = 1 already fails S4 (and the ideas that pass S4 fail S1), i.e. S2 is never the binding criterion. That would make it a control that cannot fail. So k2 has two mutation modes: `--mutate-s2` (as declared; the script reports whether it changes the survivor set, expected: no) and `--mutate` (S2 and S4 forced to 1; must produce a spurious survivor and exit 1). The real run must exit 0 (no 4/4 idea). Scoring policy fixed now: no credit for content I did not read (SNIPPET/SUMMARY/abstract-only content scores 0 on a criterion that needs it; the row says so).
* The scoring below is a judgement, not a measurement; each S is 0/1 with a one-line evidence citation in the script so it can be disputed line by line.

## Outcome (appended after all runs; nothing above was edited)
* H1 TRUE: no row passes all four criteria under P_MDL or P_decl (k1 exit 0; k1 --mutate exits 1 via a spurious clear of K9). Closest in miss: Bleger 2026 (3.3e-11, 0.2 sigma) and Blandino 2026 (fitted K); Bleger's family gives P = 0.90 (not evidence) and the scale is not stated; the only rows that pass c1+c2+c3 under N = 1 are Bleger and the fitted/1% rows, all failing c4 or c3.
* H2 TRUE (Eddington 137, small-integer families, Rosen, Sherbon: P_MDL = 1).
* H3 first half TRUE by one idea only (E5, the eigenvalue condition, 3/4, fails S4); the expected dynamical-attractor idea scored 2/4 (S2 and S4 fail), so that expectation was too generous. Second half TRUE (no 4/4; k2 exit 0). k2 --mutate (S2 and S4 forced) gives 6 spurious survivors and exits 1; k2 --mutate-s2 changes nothing, as predicted in Amendment 3.
* H4 TRUE: Atiyah's manuscript gives no evaluable procedure; the printed recursion is self-inconsistent; the leading digits are input.
* Not done / weaknesses: Gilson's formula form comes from a search snippet and was verified only by reproducing the value printed in a full-text source (137.035999786699 to 1e-11); Bleger, Blandino and Reinisch were not read beyond summaries/abstract; six 2025-2026 claims were named but not audited; the S scores are judgements.
