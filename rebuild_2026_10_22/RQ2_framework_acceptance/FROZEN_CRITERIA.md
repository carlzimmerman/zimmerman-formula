# RQ2_framework_acceptance: FROZEN CRITERIA, committed alone, before any script or number of this lane

The owner's go, 2026-11-02: the updated requirements list as one runnable acceptance test for any new framework. **This grades nothing new and adopts no framework.** Directory named `<id>_framework_acceptance` as the brief asks; RQ2 was free by `ls` and `git log`. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, reported separately, never pooled. No dark matter particle. The cold sector stays retired; nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** Read before this freeze: REQUIREMENTS_LIST, FOREST_KILL_AUDIT, closing ledger draft, FG1 criteria, LW1 criteria, README and scripts, READMEs of UX1-UX7, AF1, TG1, CRG1, CRG1's SPARC, groups, dwarfs code, NQ1's ranking, PAPER67, the v3s verdict, the status board's tile list. So every law number the harness will reproduce is known to me, and tolerances are set knowing them. That can't be undone; what's fixed here is the rule, so that it can't be tuned to a later candidate.

## Deliverables
`REQUIREMENTS_V2.md` (rows with measured value, total error, frozen line, law on both footings, source lane, disputed and correlated marks, tolerance). `acceptance.py` (harness). `README.md`. V2's tolerance table is committed **before any candidate, the law included, is run through the harness**.

## Tolerance rule, fixed
1. Each computable row has Z = (candidate - measured) / sigma_total, sign stated per row, sigma_total = quadrature of statistical and systematic terms, each from a committed file named in the row. **Row line: |Z| <= 2.**
2. A number from memory or a web page is PROVISIONAL and can't set sigma_total alone; such a row is marked.
3. If a row has no measured value (a scatter, a label on a gate), the old frozen line is carried, tagged LINE ONLY, with no Z, and it doesn't enter joint statistics.
4. Old frozen lines are printed beside every row. Where the error-derived line and the frozen line disagree on the law, that's listed in the README. Neither is moved afterwards. A later change goes in a dated amendment and any row it moves is named.
5. Only cases with a total systematic on record get one. If I can't source a term, the row says stat-only and is not widened by judgment.

## Row labels
PASS, FAIL, NOT COMPUTABLE, READ (a value carried from the record for a named candidate, not computed from what the candidate supplied; **never counted as a pass**), OPEN DATA (a dispute between measurements, not a test of a candidate). DISPUTED marks a row whose measured side is itself contested. NaN, inf, a crash or a missing input from a candidate reads NOT COMPUTABLE, never PASS.

## Candidate interface
A Python module with `g(Q)`, Q a dict-like of baryon and local quantities in SI, or a stated profile `M_extra`. Declarations: name, `a0` per footing or none, vertical form, optional `field_eq`, `cosmo`, `action`. The harness never passes an observed dynamical quantity. It records which keys a candidate reads. Reading a sample label, or a size that works as a label (R500, a host name), gets the tag **[LABEL]** beside its rows.

## Joint statistics
Correlated rows sit in named blocks. 15 keys: BA1's chi^2 definition (eigenmode cut 1e-3 max, chi2 sf), R recomputed on the candidate's run as LW1 did, or a stated reuse. Across blocks: one number per block, block chi^2 over the blocks that were computable, with N computable and N not. It is labelled as a summary with blocks treated as independent, which they aren't exactly. **A candidate's overall line: ACCEPTED only if every row on the list is PASS; with any NOT COMPUTABLE or READ row the most it can read is NOT REJECTED ON n OF N.** Nothing is a verdict on a theory by counting rows.

## Known answers, a failed one means no scorecard is trusted
- KA1: the law through the harness reproduces LW1's scorecard labels and numbers on both footings: keys Z to 1e-6 against `lw1_keys_*.json` if the same path runs; X-COP, dwarfs, DiskMass, Milky Way against LW1's JSON to their printed tolerances; S, Tl, LT, G against CRG1 or FG1 to 1e-3. I state any line where this can't be met; it isn't hidden by loosening the check.
- KA2: Bullet row for the law reproduces UX6's k = 0 row, if that path runs.
- KA3: mocks are flagged: a planted mock whose miss sits in named rows must fail those rows, and pass nothing it shouldn't; a NaN mock must read NOT COMPUTABLE, with zero PASS; a mock with a sample-label switch must carry [LABEL].
- MUTATE twin: the harness with a0 x 1.5 labelled as the law must fail KA1 and exit 1, with separate outputs. Rerun byte-identical.

## Scope limits, fixed
Other lanes' files are read, never edited. BK2 and AS2 aren't touched. No downloads. REQUIREMENTS_LIST.md, the ledger, PAPER67 aren't edited. One thread, nice 19, under 4 GB; if a row's path is too heavy to run per candidate, it's NOT COMPUTABLE with the reason, or read from a cache with that stated. Local commits only: own directory, no push.

**Expectation on record:** the law reproduces LW1's FAIL lines; some Z shrink on total error (IC 1613, X-COP, one or two dwarf classes), so a few lines may flip when frozen lines are replaced by error lines, and I'd report that as a statement about the tolerance and not as relief. About half the rows NOT COMPUTABLE from g alone, since action, health, CMB, PPN and tensor speed can't be read off a static g. kappa = 1/2 FITTED; not theory closed.
