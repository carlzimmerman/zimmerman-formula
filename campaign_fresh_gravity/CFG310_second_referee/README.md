# CFG310: second-round hostile referee of MNRAS v3.2 and PAPER40 v1.1 (2026-10-03)

**Scope.** Read-only on both papers. Nothing is committed by this lane. Post hoc referee diagnostics: they are not frozen and they are not a₀ measurements. κ = ½ is FITTED. The cold mass is still required. Nothing here says the data favour any law.

## Verdicts

| paper | recommendation | CRIT / MAJOR / MINOR / NIT | ready? |
|---|---|---|---|
| MNRAS v3.2 (tag `mnras-v3.2` = d96f177fe) | MINOR REVISION, conditional | 0 / 5 / 8 / 4 | **not yet** for submission: 5 text, citation or disclosure fixes, plus the owner's TODO-RUN |
| PAPER40 v1.1 (24fcc8250) | MINOR REVISION | 0 / 2 / 7 / 3 | **not yet** for Zenodo: 2 text fixes, using numbers already committed |

The reports are `REFEREE_REPORT_MNRAS_v3.2.md` and `REFEREE_REPORT_PAPER40_v1.1.md`.

## What was run

1. **Clean mirror.** `git archive 24fcc8250` was extracted into a fresh scratch directory. That commit carries the MNRAS directory byte-unchanged since d96f177fe; `git diff --stat` shows only PAPER40 files between the two commits. A pre-existing `mirror/` in the shared scratchpad held symlinks into the live repo, so it was not used.
2. **MNRAS.** `bash reproduce_all.sh` in the mirror reports ALL STEPS PASSED in 2 min 16 s.
   - `paper_numbers.py`: 100 checks, 0 FAIL.
   - `paper_numbers.out` and `.json` are byte-identical to the committed files.
   - The six figures are identical once rendered (pdftoppm hashes); only their creation dates differ.
   - The PDF text is identical.
3. **PAPER40.** `make_paper40_figures.py` in the mirror passes 31/31 gates. The JSON and both figure PDFs are byte-identical.
   - `PAPER40_audit.py` was run on the mirror's tex, PDF and JSON with `PAPER40_REPO` set to the live repo. It reads committed sources through `git show HEAD:`, read-only.
   - Results: 375/375, 19/19 LIT, 236/236 PDF-text. `--mutate` and `--mutate-tex` both exit 1, as required.
   - The full log is in `cfg310_mirror_reproduction.out`.
4. **`cfg310_referee_checks.py`** (writes `.out` and `_results.json`):
   - MNRAS compliance: abstract counted three ways plus the paste text, keywords, AI disclosure, tag, alt text, PDF.
   - MNRAS bibliography: the ALESS sources are absent; Lee2025 is checked against `cfg310_lee2025_crossref.json`, a Crossref record saved here.
   - The RC100 native-route floor fraction against z, and a censoring-aware rank test.
   - The MUSE-DARK native rows, the KURVS native P2 cell and the ALESS fractions.
   - The columns of the PUBLISHED RC100 table.
   - PAPER40: abstract count, flux readings, the H₀ like-for-like verdict, the statistical error (the paper's chain is exec'd from `make_paper40_figures.py` and reproduces the committed pooled s*; five bootstrap seeds), the joint fit and selection rows, and the Zenodo and PDF metadata.
5. **`cfg310_shared_calibration_N.py`** (writes `.out`) re-implements the KL design computation of MNRAS Table 12. It reproduces 20.8:1, 6.2:1 and 2.4:1, then gives the N needed for 20:1 against the shared calibration error δ_c.
6. **`cfg310_number_trace.py`** traces 28 numbers per paper to committed sources and to the tex, and writes `number_trace.csv` and `cfg310_number_trace.out`. All 56 match; 14 carry a referee note.

## Network reads

These were read-only metadata look-ups. Nothing was downloaded beyond the JSON record kept here.
- Crossref: 10.1051/0004-6361/202555362 (Lee2025).
- arXiv API: 2507.11600, 2609.20926 and 1107.2934 (McGaugh 2012's abstract, which confirms PAPER40's "1.3 ± 0.3").
- `git ls-remote --tags origin`: confirms that `mnras-v3.1` and `mnras-v3.2` are pushed.

## Top findings

**MNRAS v3.2**
1. The abstract's "the MUSE-DARK rise … disappears" and Conclusion (vi) regress CFG290 #16. With molecular gas, the native route also excludes constancy (2 of 3 thirds).
2. The primary RC100 native route is censored: 41 of 100 discs sit at the floor, and the fraction rises from 27% to 51% with z (p = 0.013). Kept as censored values, the implied a₀ falls with z (p = 0.006). "Show no rise" misdescribes a baryon-calibration failure.
3. ALESS 122.1 is used without citing any of its sources: Dunne+22, Calistro Rivera+18 and Amvrosiadis+. The last of these was not on the known-open list.
4. "Checked cell by cell against the journal" does not cover the SED M* column, which the primary route uses.
5. "Eight discs … and a 0.06 dex calibration" are not jointly sufficient. At δ_c = 0.06, eight discs give 4.8:1, and 20:1 needs about 36.

**PAPER40 v1.1**
1. The single-dish range 0.97–1.13 drops CFG304's frozen primary (0.90). STANDING records 0.90–1.06.
2. On the H₀ = 67.4 value the paper calls like-for-like (1.208), the canonical footing is inside the recipe width and the alternative footing is inside the 95% statistical interval. The abstract's "just outside" holds only on H₀ = 70.
3. The bootstrap SD (0.034) sits about 30% below the median's asymptotic error from the paper's own per-galaxy spread (0.048). The alternative-footing "outside the 95% interval" statement depends on that choice.
