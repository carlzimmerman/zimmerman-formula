# FN5_ship_record: PAPER67 v1.1 is ready except the BK2 L2 line. This file is the fold-in for the session holding BK2

Item 5 of the five-item push (`../README.md`). Nothing here was deposited or sent. Never run `PAPER67_zenodo_publish.py` from a drafting session; the owner runs it. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## Lane status, 2026-11-04
**Label: READY EXCEPT BK2 L2.** The owed fixes and the lanes of 2026-11-02 to 11-04 are folded into the draft, and the `% PENDING: BK2 L2` marker stays, so the publish guard still refuses.

| Step | Commit | Result |
|---|---|---|
| TeX: owed fixes (i)-(iv) and the new lanes, Table 5 of lanes with labels and commits | 43914ec08b | UX2 line corrected (AN1 v3, AN2, SG, P160); HF1 and VW1 in "one family left outside"; BK2's canonical L1 control; BF1 L4; rows 5, 7, 8, 12, the κ paragraph and AT1 |
| `PAPER67_audit.py` extended, PDF rebuilt offline (`tectonic -C`) | cf6ac7eb40 | 616 of 617 pass; the one failure is the PENDING marker. MUTATE: 556 of 557 literals not found (the old TD1 survivor), 37 of 37 recomputations and commits fail |
| `.zenodo.json` description draft | 6f6b0a7d0f | dated 2026-11-04, one paragraph on the new lanes; not published |
| `rebuild_2026_10_22/EXTERNAL_SUMMARY_2026-11-04_DRAFT.md` and its audit | 93b4235c4b | DRAFT for the owner to read; not sent. 220 of 220 pass; MUTATE 196 of 196 |

**Failed checks and departures.**
- The PAPER67 audit fails one check by design: the PENDING marker.
- Commit 93b4235c4b also carries eight FN3 files that another session had staged in the shared index (`FN3_musedark_law_refit/AMENDMENT_A2.md`, `fn3_k2*`). Their content is theirs and unchanged. The lead records this forward; nothing was rewritten.
- Not in the owed list, done because the record moved: PAPER66 is cited at v1.4 (DOI 10.5281/zenodo.23958256) instead of v1.2, and "537 attempts" became 550 from the κ register.
- Table 5 has one row for the ΛCDM recipe experiment (DOI 10.5281/zenodo.23958263), worded "kept apart; nothing in it feeds this paper". That deposit's README says nothing in it feeds PAPER67, so the owner may prefer the row gone. Deleting it needs the matching three tuples and one COMMITS entry removed from the audit.

**Needs the owner.** The go for `--newversion 23883741` (given, and it stands once BK2 L2 is folded); whether the ΛCDM-recipe row stays; whether the outside summary is sent, and to whom.

## Before folding: BK2's preconditions
1. BK2's L2 controls have finished on both footings, BK2's README states the L2 label, and the L2 files are committed. Check: `git ls-files rebuild_2026_10_22/BK2_dimensional_law_search | grep L2` lists `bk2_train_L2_{canonical,alt}_{real,control}.json`, `bk2_read_L2_*.out` and `bk2_stage2_L2_*`.
2. The slots below assume the L2 label is **NO HIT** on both footings. If BK2 reads anything else (a SURVIVOR flag, WITHIN ERRORS, OUTSIDE A LINE, FAILS ONLY CASSINI), stop. Its README then needs the dear gates and a separate recheck, and the paper's sentence is written from that label, not from these slots.

**As read on 2026-11-04 from the uncommitted real runs only. Provisional; recheck after BK2 commits them.**
- `bk2_train_L2_canonical_real.json` `"enum": 737794339680`; `bk2_train_L2_alt_real.json` `"enum": 737788750704`. That is 7.4e11 per footing.
- Both `bk2_read_L2_*_real.out` FINAL lines read `'train_line': 0, 'train_err': 0`. Both `bk2_stage2_L2_*_real.out` read `50 formulas; train pass 0`.
- Closest by line: canonical `Zl 1.01 cass True X -0.012,0.100`, alt `Zl 1.01 cass False X +0.033,0.101`.
- Controls were still running (`bk2_status.out`: canonical control L2 at T1|I3, alt at T1|I4).

## Text slots in `qwen_claude_field_theory/papers_2026/PAPER67_galaxy_law_and_what_it_leaves_2026.tex`
Braces mark values to fill from the committed L2 files. Each old string occurs once.

| Slot | Old | New |
|---|---|---|
| A, line 1 | `% PENDING: BK2 L2` | delete the line |
| B, title note | `version 1.1, 2026-11-04.` | `version 1.1, {deposit date}.` |
| C, abstract | `Formula searches that have finished found no hit, and one level keeps running with no result claimed.` | `Formula searches found no hit.` |
| D, Section 7 opening | ` BK2's level L2 is still running, and nothing here claims a result from it.` | delete, with its leading space |
| E, BK2 paragraph | `Level L2 is unfinished, temperature and dispersion aren't in the grammar, and check K3 failed on the IC~1613 row.` | `Level L2, $7.4\times10^{11}$ expressions per footing, also reads NO HIT: 0 through G1--G3 on the line or within errors, on both footings. Its closest rows read {Zl_can_real} and {Zl_alt_real}, and the scrambled control's {Zl_can_ctrl} and {Zl_alt_ctrl}. Temperature and dispersion aren't in the grammar, and check K3 failed on the IC~1613 row.` |
| F, Table 5, after the `BK2 L1` row | (none) | `BK2 L2 & dimensioned expressions, level L2 & {L2 label as BK2's README writes it} & {L2 result commit}\\` |
| G, Data and code | `BK2 is still running, and its README is the record of what has landed.` | `BK2's README is the record of both levels.` |

If the control comes closer than the real data, slot E's second sentence says so in those words; if it doesn't, say "the control doesn't come as close" and quote both.

## Audit edits in `PAPER67_audit.py`
Remove this tuple from the BK2 block (the TeX loses its fragment):
```python
("Level L2 is unfinished", B + "README.md", "## Unfinished, running"),
```
Add these to the FN5 block (before `F = 0; n = 0`), with the braces filled from the committed files:
```python
 ("Level L2, $7.4\\times10^{11}$ expressions per footing", B + "bk2_train_L2_canonical_real.json", "\"enum\": 737794339680"),
 ("Level L2, $7.4\\times10^{11}$ expressions per footing", B + "bk2_train_L2_alt_real.json", "\"enum\": 737788750704"),
 ("also reads NO HIT: 0 through G1--G3", B + "bk2_read_L2_canonical_real.out", "'train_line': 0, 'train_err': 0"),
 ("also reads NO HIT: 0 through G1--G3", B + "bk2_read_L2_alt_real.out", "'train_line': 0, 'train_err': 0"),
 ("Its closest rows read {Zl_can_real} and {Zl_alt_real}", B + "bk2_read_L2_canonical_real.out", "by LINE\nZl {Zl_can_real} cass"),
 ("Its closest rows read {Zl_can_real} and {Zl_alt_real}", B + "bk2_read_L2_alt_real.out", "by LINE\nZl {Zl_alt_real} cass"),
 ("the scrambled control's {Zl_can_ctrl} and {Zl_alt_ctrl}", B + "bk2_read_L2_canonical_control.out", "by LINE\nZl {Zl_can_ctrl} cass"),
 ("the scrambled control's {Zl_can_ctrl} and {Zl_alt_ctrl}", B + "bk2_read_L2_alt_control.out", "by LINE\nZl {Zl_alt_ctrl} cass"),
 ("{L2 label} & {L2 commit}", B + "README.md", "{the README's L2 label line, verbatim}"),
```
Append to `COMMITS`:
```python
("{L2 commit}", Q + "BK2_dimensional_law_search"),
```
After the fold-in the PENDING check passes, so every check should pass: 652 of 652 if exactly the nine tuples and one commit above go in (643 checks today after the 2026-11-04 TX1, MB1, BF3, DB1 rows and the FN1b, FN3, FN4b, FN4c and owner-decision checks, minus 1 removed, plus 9 and 1). MUTATE should still show only the old TD1 survivor, with every recomputation and commit failing when perturbed.

## `.zenodo.json` description
Append to the last paragraph, before `</p>`:
` A dimensioned search's level L2, 7.4e11 expressions per footing, also reads NO HIT, and its scrambled control {comes as close / doesn't come as close}.`
Change `version 1.1 (2026-11-04)` to the deposit date if it differs. Nothing else in the metadata changes.

## Outside summary (optional, it isn't deposited)
In `rebuild_2026_10_22/EXTERNAL_SUMMARY_2026-11-04_DRAFT.md`: `it waits on one running search` becomes `it waits on the owner's go`, and `its level L2 is still running` becomes `its level L2 also reads NO HIT`. In its audit, replace the two tuples that point those fragments at `"## Unfinished, running"` with the L2 literals above.

## Finish, in order
1. Make slots A-G and the audit edits.
2. `cd qwen_claude_field_theory/papers_2026 && tectonic -C PAPER67_galaxy_law_and_what_it_leaves_2026.tex` (offline; it worked on 2026-11-04). Don't keep the log; it isn't committed.
3. `python3 PAPER67_audit.py > PAPER67_audit.out` must exit 0 with every check passing. `python3 PAPER67_audit.py --mutate > PAPER67_audit_MUTATE.out` must exit 0.
4. Commit with explicit paths only, because other sessions stage files in the same index: `git add` nothing new, then `git commit -m "..." -- <tex> <pdf> <audit.py> <audit.out> <audit_MUTATE.out> <zenodo.json>`.
5. The owner runs `python3 PAPER67_zenodo_publish.py --newversion 23883741`. Its guard reads the marker and the audit first.
