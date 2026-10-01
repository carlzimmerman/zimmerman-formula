#!/usr/bin/env python3
"""CFG241_mkreadme.py: assembles README.md from the hand tables (classification CSV, findings JSON) and the committed outputs."""
import csv, json, collections, os
H = os.path.dirname(os.path.abspath(__file__))
cl = list(csv.DictReader(open(os.path.join(H, 'CFG241_classification.csv'))))
F = json.load(open(os.path.join(H, 'CFG241_findings.json')))
cnt = collections.Counter(r['class'] for r in cl)
faith = [r for r in cl if r['class'] == 'FAITHFUL']
unv = [r for r in cl if r['class'] == 'UNVERIFIABLE-OFFLINE']
byid = {f['id']: f for f in F}
def fl(ids): return ', '.join(ids)
fa = ', '.join('%s(L%s)' % (r['id'], r['tex_line']) for r in faith)
sev = collections.Counter(f['severity'] for f in F)
def block(f):
    return ('### %s  %s  (%s)  tex line(s) %s  claims %s\n- **Sources:** %s\n- **Evidence:** %s\n- **Independent support:** %s\n- **Proposed fix:** %s\n' %
            (f['id'], f['severity'], f['class'], ', '.join(map(str, f['tex_lines'])), ', '.join(f['claims']) or '-', '; '.join('`%s`' % s for s in f['source']), f['evidence'], f['independent_support'] or 'see sources', f['proposed_fix']))
maj = ''.join(block(f) for f in F if f['severity'] == 'MAJOR')
mino = ''.join(block(f) for f in F if f['severity'] == 'MINOR')
nit = '\n'.join('- **%s** (tex %s; %s): %s Fix: %s' % (f['id'], ', '.join(map(str, f['tex_lines'])), '; '.join('`%s`' % s for s in f['source']), f['evidence'], f['proposed_fix']) for f in F if f['severity'] == 'NIT')
R = '''# CFG241 -- hostile post-publication referee of PAPER38 (DOI 10.5281/zenodo.23073072, v1.1): phase 2 report

**kappa = 1/2 is FITTED, NOT DERIVED.** Nothing here says the data favour any law. Frozen criteria: `campaign_fresh_gravity/CFG241_FROZEN_CRITERIA.md` (ae00eda43, sha256 a1766656...). Paper read at git HEAD 96a00a65a (tex unchanged since the deposit; tex sha256 5faf1b15...). Failed controls and wrong expectations are kept below. A single reader classified every claim by hand; the flagger is a hint generator, not the verdict.

## 1. Bottom line

- **0 CRITICAL, 2 MAJOR, 13 MINOR, 8 NIT** (23 findings; claim-level classes in section 3). Every number the paper quotes that I traced reproduces from its source (exceptions: F-14, a mislabelled threshold, and F-12, RC100 values taken from the uncorrected input table, effect < 0.003); the trouble is in the glosses: one abstract sentence that is true only asymptotically (F-01) and the treatment of the Heintz and Watson table (F-02). No withdrawn claim crept back (RC100 4.9/5.5 sigma is not quoted; the paper says "not to be quoted"); no bibliographic entry is contradicted; the DR4 pair numbers, E(z) values, KiDS power, chi2 p-values, break-even table and Lean theorem count all reproduce.
- **v1.2:** by the rule frozen in section 10 of the criteria (any CRITICAL, or two or more MAJOR findings on text the paper itself states) a v1.2 deposit **is warranted**; both MAJOR findings and every MINOR finding are wording fixes (no number changes), so a v1.2 would be an editorial revision. The owner decides. One borderline item (F-14, "2 SD = 0.084") is graded MINOR by the tie rule; read literally it is a CRITICAL-class numeric slip with no effect on the conclusion.

## 2. Commands and files

Re-run (about 1 minute, no network): `ZF_REPO=<repo root> bash campaign_fresh_gravity/CFG241_paper38_referee/CFG241_run_all.sh` (from anywhere; the scripts also find the repo by walking up from the lane directory). Exit codes expected: extract 0; plant (frozen set, rule v4) 0; plant --fresh 1; plant --fresh2 1; self-disable 1; check 0; physics 0; physics --mutate 1; refs 0; report 0.
Files: `CFG241_common.py`, `CFG241_extract.py`, `CFG241_check.py` (+ `CFG241_check_v1/v2/v3/v31_snapshot.py`, the earlier rule versions that produced the kept outputs), `CFG241_physics.py`, `CFG241_refs.py`, `CFG241_report.py`, `CFG241_mkreadme.py`, `CFG241_run_all.sh`; tables `CFG241_claims.csv`, `CFG241_worksheet.csv/json`, `CFG241_classification.csv`, `CFG241_findings.json`, `CFG241_sections.json`; outputs `CFG241_extract.out`, `CFG241_flags.out`, `CFG241_flag_vs_hand.out`, `CFG241_physics.out`, `CFG241_physics_results.json`, `CFG241_physics_MUTATE.out`, `CFG241_refs.out`, `CFG241_plant_*.out` (all rule versions kept).

## 3. Coverage

- Extraction reproduces the frozen throwaway count: **120 sentence units, 117 claim sentences** (tables collapsed), 9 numbered sections plus abstract. Split properly: 116 prose sentences (114 claim sentences) plus **15 table rows** (the frozen file says 16: table 1 has 6 rows and table 2 has 9, not 10; the 120/117 count is unaffected) = **129 claim units, all 129 classified (100%)**.
- Classes: FAITHFUL @@FA, MISSING-CAVEAT @@MC, OVERSTATED @@OS, CONTRADICTED @@CD, UNVERIFIABLE-OFFLINE @@UV (@@UVP%, target <= 10%). Of 129, 2 are signposts (C020, C031). The 6 UNVERIFIABLE-OFFLINE claims (@@UVL) state content of external papers (Heintz and Watson; Dunne et al.; Coogan; Birkin) and agree only with the repo's own scoping note (the cached PDF text is outside the repo): reason code EXTERNAL-PAPER-NO-LOCAL-COPY. All number tokens in the abstract and sections 2, 6 and 7 were individually matched (the NUM flag family plus hand reading).
- Flagger versus hand (`CFG241_flag_vs_hand.out`): of 19 hand-found non-faithful claims, 16 carry some flag and 12 a non-CAVEAT flag; precision is low (NUM 2 of 21 flagged claims, SCOPE 8 of 21, VERB 3 of 16, CAVEAT 13 of 90). Missed by every flag: C007 (causal "because"), C055 (misattributed quotation), C092 (a dropped clause).

## 4. Control outcomes (kept, in order)

- **Frozen plants M1-M10 and paraphrases P-a to P-c, rule v1 (as frozen): 8 of 10 caught; M2 (stronger verb) and M7 (15 to 18) MISSED** (`CFG241_plant_firstrun.out`, exit 1). P-a was scored FALSE POSITIVE by a harness bug: the paraphrase is not extracted as a claim by the frozen trigger rule, so it has no flags (vacuous pass); P-b and P-c passed. M3 is caught by the CAVEAT family but through the token "post hoc", not through the planted token "not to be quoted" (kept).
- Rule v2 (negation-aware per-verb VERB rule; integer tokens must match as integers): M2 caught, M7 still missed (9/10). v3 (range-pair rule) 9/10; v3.1 (word-boundary fix) 9/10: M7's digits "15" and "18" occur in unrelated paragraphs (ALPAKA 15, 18). v4 (a number counts as supported only from the top-ranked paragraph or from a lane the claim names): **10/10 caught, 3/3 paraphrases not flagged, exit 0**. v4 was written after seeing the M7 miss, so the frozen-set result is partly tuned; the X plants were written with v3 (after the v1/v2 results) and the Y plants with v4, and none was used to tune a rule.
- Fresh plants (X1-X5, X6 paraphrase; Y1-Y4): X1 (range edit) caught, X2 (verb) caught, X3 (dropped caveat) caught, X4 (5.09 keV) caught, **X5 (wrong citation key with no surname) MISSED**, X6 paraphrase not flagged; Y1, Y2, Y4 caught, **Y3 (5 sigma replacing 3 sigma, a single-digit change) MISSED**. Known limits of the lexical pipeline: key-only citation swaps and single-digit changes.
- Self-disable (M1 with NUM disabled) exits 1 as required; `CFG241_physics.py --mutate` exits 1 (3 of 7 self-controls fail), as required.
- Hand estimates graded (made after reading the tex, before any source): CRITICAL P(0)=0.55 -> 0 observed (but one borderline, F-14); MAJOR P(1-2)=0.45 -> 2; all findings median 16 (80%% 9-26) -> 23; FAITHFUL fraction about 85%% -> 104 of 129 (81%%) or 104 of 121 claims with an on-disk source (86%%); v1.2 warranted 0.40 -> yes by the frozen rule; all 10 plants first run 0.45 -> **no (8/10), wrong**; paraphrases unflagged 0.55 -> harness false positive on P-a (wrong, harness bug); coverage met first run 0.80 -> yes; bib contradiction 0.08 -> none.
- Attention list: W1 (lever vs 1/m) -> the quoted numbers reproduce; my hand 1/m expectation (1.5-2.4) was **wrong** as a prediction of the table (1.46-1.83), but the baryon lever is step-dependent (F-03); W2 -> F-03; W3 -> F-05, N-04; W4 -> F-09; W5 -> F-10; W6 -> N-01; W7 -> F-02; W8 -> N-05; W9 (stage mixing) -> **not a finding** (0.0383 is both the pre-flight and the measured error; the 0.14 differs from (0.0179/0.0383)^2 = 0.22 because it is a 14-bin quantity); W10 -> F-13; W11 -> N-03 (6%%); W12 -> F-04; W13 -> F-11; W14 -> not a finding (closure_map/GATES_STATUS:219-221 supports the sentence).

## 5. MAJOR findings

@@MAJ
## 6. MINOR findings

@@MIN
## 7. NITs

@@NIT

## 8. Physics re-derivations (`CFG241_physics.out`; known-answer self-controls 7/7 pass)

- **P1 (delta/2):** sympy: d ln g_obs/d ln f = 1 - m, d ln g_obs/d ln a0 = m, m = -dln nu/dln y; both 1/2 in the deep limit, so a drift delta in either moves log g_obs by delta/2. KiDS K1 bins (CFG61 edges 1e-15..5e-12, bins 8-14) have y = 0.0006-0.03 (canonical a0): the two responses differ by at most 6%% (N-03). The rival's half-log E ratio gives +0.0237 (late) and +0.0178 (early) dex, consistent with the lane (+0.0179 combined, late +0.024).
- **P2 (lever):** reproduces `cfg223_lever.out` (slopes 0.126-0.283; x1.46-1.83 per 0.05 dex in D; -2.48..-4.83 per baryon dex at +-0.03 dex). At +-0.01 dex the baryon lever runs -2.46..-6.42 (F-03). Dependence: single-galaxy shift eps of log D moves log s by eps/m(y/s*); baryon shift x moves it by -(1-m)/m; for the median over N galaxies neither is an equality; kernel dependence: at y = 1.1/2/3/4.4 the P2 kernel has m = 0.24/0.17/0.13/0.09 and the McGaugh kernel 0.28/0.23/0.19/0.15.
- **P3 (E(z)):** Om 0.27-0.32: E(1.4) = 2.11-2.26, E(2) = 2.83-3.05 (0.45-0.49 dex), E(2.3) = 3.23-3.49, E(5) = 7.68-8.36; all paper values fall inside; Omega_m is never stated (F-10).
- **P4 (KiDS):** chi2.sf(19.81/19.80/19.21/15.05, 14) = 0.136/0.137/0.157/0.375 (paper: all p > 0.1, ok); 1.06 and 1.53 sigma reproduce; 9 = 3^2.
- **P5 (CFG240):** CalibrationWall.lean has 50 theorems; ChainCert declarations counted: 331. T1_deep_iff, T2a_P2_injective, T2a_one_point_fails, T2c_det_bounds, T4 statements printed with hypotheses (F-05, N-04). A Lean toolchain exists on the machine (lake, lean) but `lake build` / `verify_chain.sh` were NOT run (a build would write into the repo tree; no network); proofs not re-checked here.
- **P6/P7 (Fisher):** y_min 0.01: 7.94 on the 0.02-dex grid (bisection 7.60), y_min 1e-3: 5.50, y_min 0.1: never (min 0.1169 at y_max = 47.9); rho = -0.79 and cond = 13.3 at break-even; matches `CFG240_break_even_table.json` (7.943). Paper discs (log-uniform 1.1-4.4, N = 20): 0.42 dex; real per-galaxy y: 0.15-0.22 per RC100 quartile, 0.089 pooled (F-04). T4 floor: minimum 3.0000 over 16,000 random designs, equality at 2/3 deep, 1/3 Newtonian: not violated.
- **P8 (DR4):** the file's 4,342 pairs (floor 1.1614, sigma_sys 0.02) fix c = 3.291; floor 1.1917 then needs 2,941 (file 2,940); cap 8.07 (file 8.1); 5.85 sigma at 30,000 (file 5.8): the paper's 4,300/2,900/30,000/1.000/1.161/1.192 are faithful. Statistic: B, LCDM, Newton -> 1.000 per closure_map/WHAT_WOULD_DECIDE:10 and the preregistration table.
- **P9:** 22 internal arithmetic relations all hold (A1-A21).
- **P10 (audit):** 293 rows; 33 bare-context rows; 85 of 371 numeric tokens (23%%) outside any audit literal; the tex side is checked at block level (F-11).
- **P11:** PDF text layer and tex agree on every decimal token (the only tex-only tokens are table-column widths); `.zenodo.json` carries the AI-assisted / not-peer-reviewed disclosure.

## 9. References (`CFG241_refs.out`; offline limits)

Frozen spot-checks: **D22 MNRAS 517, 962** and **HW20 ApJL 889, L7**. Neither has a REFERENCES.bib entry; both agree with later papers' reference lists held as local HTML (arxiv_2411.04290 line 1222 prints "MNRAS, 517, 962"; arxiv_2306.03153 line 2197 prints "ApJ, 889, L7"; the HW20 doi 10.3847/2041-8213/ab6733 appears in two local HTML copies) and with the repo's scoping note: consistent, **not checked against the journals**. B21, DM14, NS23 agree with the bib. ACE titles and first authors agree with the local HTML copies; "submitted to A&A" and the existence of arXiv:2609.xxxxx outside the repo's fetched copies cannot be checked offline. Nothing contradicted; see F-13.

## 10. Fairness checklist (F1-F12 of the criteria)

F1 flat as "distinctive": UNDECLARED (N-01). F2 rival unattributed: UNDECLARED (F-15). F3 LCDM proxy: FAIR (disclaimed in the abstract and section 8; no LCDM-simulation predictions cited, deferred to CFG222). F4 RC100's own interpretation: NOT-APPLICABLE (neutral use). F5 tone toward Heintz and Watson: UNFAIR-TO-NAMED-AUTHORS in part (F-02). F6 literature scope: UNDECLARED (F-15). F7 undeclared choices (Omega_m, kernel, bands): UNDECLARED (F-10). F8 symmetry: FAIR (the RC100 "5 sigma" retraction and the calibration ceiling are stated for every law). F9 "decisive": OVERSTATED (F-09). F10 ceiling applies to a result favouring the programme equally: FAIR (the 0.10-dex requirement is labelled post hoc in section 8). F11 quotations of the standing page: FAIR (exact; one misattribution, N-02). F12 AI-assisted / not peer reviewed: FAIR (title block, `.zenodo.json`).

## 11. Claims found FAITHFUL (@@NF of 129; tex line in parentheses)

@@FALIST

## 12. Could not verify (from memory, unverified; none of these supports a finding)

- Whether the omission of the high-redshift RAR literature (MOND-side and LCDM-side, including LCDM simulation predictions) is material to a reader; I have not read that literature here.
- The journal volume, page and year of every reference (including D22 and HW20) against the publishers' records; whether arXiv:2609.20926 and arXiv:2609.21040 exist as stated (after my training data) and are "submitted to A&A".
- Whether Heintz and Watson 2020 has an erratum, how the authors define their 0.2 dex scatter, and whether the apparent shift in the alpha column is a property of the published table or of the repo's text extraction (the cached PDF text is not in the repo; the extraction is line-based, which makes a column misalignment less likely but not impossible).
- Who holds a0 proportional to H(z): from memory Verlinde-type and a0 ~ cH readings; the repo's lensing note names Verlinde.
- That the Lean proofs compile (toolchain present, build not run).
- Standard (Milgrom) MOND's treatment of a0 at high redshift beyond "a0 is constant".
- Whether the single reader's classification would be reproduced by a second reader.

## 13. v1.2 statement

By the frozen rule a v1.2 deposit is warranted (two MAJOR findings on text the paper states). Minimal v1.2 content: the F-01 abstract sentence, the F-02 rewording of the Heintz and Watson passages (abstract, line 157, line 193), and, if the owner wishes, the MINOR wording fixes (F-03 to F-15). Reasoning: no number is wrong, no withdrawn claim returns, and the physics holds; the two MAJORs are about what the sentences claim relative to their sources (a headline generalisation and the tone toward a named published table), which a MOND or LCDM expert would raise first. Cost of not revising: the abstract overstates one lane family and says more about HW20 than the scoping note supports. The owner decides.
'''
R = R.replace('%%', '%')
for k, v in {'@@FA': str(cnt['FAITHFUL']), '@@MC': str(cnt['MISSING-CAVEAT']), '@@OS': str(cnt['OVERSTATED']), '@@CD': str(cnt['CONTRADICTED']), '@@UVP': '%.1f' % (100.0 * cnt['UNVERIFIABLE-OFFLINE'] / 129), '@@UVL': ', '.join(r['id'] for r in unv), '@@UV': str(cnt['UNVERIFIABLE-OFFLINE']), '@@MAJ': maj, '@@MIN': mino, '@@NIT': nit, '@@NF': str(len(faith)), '@@FALIST': fa}.items():
    R = R.replace(k, v)
open(os.path.join(H, 'README.md'), 'w').write(R)
print('README written', len(R), 'chars')
