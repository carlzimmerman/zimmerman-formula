# PAPER46 deposit record

- Title: A Dated, Graded Ledger of the Testable Predictions of a Vacuum-Tied MOND Framework, with Its Confronted Record and Retracted Claims (Working Note)
- Version 1.0, deposited 2026-10-11. DOI 10.5281/zenodo.23303805 (record https://zenodo.org/record/23303805).
- File: PAPER46_prediction_ledger_2026.pdf (232,953 bytes, 22 pages). Built by PAPER46_build.py from explainers/kepler_grade_prediction_chart.html; audited by PAPER46_audit.py (10/10 before the deposit).
- Repository state at deposit: commit e9c6dd51d (paper, builder, audit, metadata); the publish script was then corrected (the metadata file wraps its fields in a top-level `metadata` key, which the first run double-wrapped, so Zenodo rejected the first publish attempt with a 400 and nothing went live; the same draft, id 23303805, was resumed and published).
- The web chart is maintained and updated after this record; this record is the 2026-10-11 version and is not updated in place. A new version needs a new Zenodo version under the same concept DOI.
- kappa = 1/2 is fitted; the cold energy's mass is required; the theory is not closed.

## After the deposit (2026-10-11)
- The chart now lists this deposit (16 deposit rows against the paper's 15) and carries a "Frozen version" line with the DOI. The deposited PDF and `.tex` are untouched.
- `PAPER46_audit.py` is bound to the chart at the deposit commit (e9c6dd51d): its A1 check (PDF newer than the chart) and the count checks will report the paper as stale after later chart edits. That is by design. A new paper version means rebuilding with `PAPER46_build.py`, re-auditing, and depositing a new Zenodo version under concept DOI 10.5281/zenodo.23303804.
- The public web copy is regenerated from the chart by `explainers/build_public_chart.py`.
