# Reproduction and interpretation notes

Every experiment has its source, prior finite contract, fresh output
directory and v2 bounded-runner manifest. The exact numerical argv and full
input hashes are recorded in each manifest. Reproduction uses the installed
mathbox `scripts/run_experiment.py`, the corresponding `contract*.json`,
every execution artifact as `--input`, the recorded command after `--`,
and a fresh output/result directory. Existing records must not be overwritten.
`launch_segment.py` shows the full bounded continuation construction;
`benchmark.py` consolidates the pinned fresh ancestries without a solve.

Limits are at most 240 wall/235 CPU seconds and one numerical thread.
Completed numerical results retain measured macOS peak RSS in bytes.
An interrupted/failed record can retain only a partial observation or no
result RSS; that is not silently replaced by an estimate. The initial
resource-limited midpoint record's RSS is a lower-bound partial observation,
not its terminal process peak. Python3.9.6, NumPy1.26.2, SciPy1.11.4 and
mpmath1.3.0 are pinned where used. No installation, Git mutation or prior
review edit was performed by this package.

Run statuses retain their original meaning. A failed assertion is not a
completed finite claim; a CPU/time cap is resource inconclusiveness.
`run_midpoint002` is a failed assertion because not all refinement cases
complete, despite useful positive partial results. Its JSON claim_id
retains the general midpoint label; its manifest's reduced-control claim,
explicit total_dN=1e-6 and recorded command identify the tested case.

Some early fresh contracts retained an obsolete inherited `bounds.dN`
inventory [5e-5,2.5e-5] from a one-step template. Their explicit `stepmax`,
argv and actual accepted-step histories define the fresh coarse 1e-4 and
fine 5e-5 runs. The obsolete field is an inventory erratum, not an alternative
execution. Original contracts and manifests remain unchanged. Preflight
duplicate-input rejections produced no numerical run directory; the
corrected versioned contracts are retained alongside their predecessors.

The collision endpoint energy equation is part of the method. It is not
offered as an independent physical-energy proof. The FRW stress-energy
work integral is independent and starts at the fresh initial state.
Gross-flux roundoff allowances are numerical solver budgets; raw physical
number residuals are reported separately and are not physical energy
conservation evidence. Time refinement of actual action and yields remains
necessary even when the global work defect is tiny.

`python3 reviews/weak_completion_2026_11_04/energy/finalize_records.py`
checks all terminal manifests with the installed validator and writes the
source/contract/status inventory. It refuses unfinished run directories.
`PROVENANCE.json` records current-input validation; the per-run manifests
remain the authoritative before/after input and output records.
