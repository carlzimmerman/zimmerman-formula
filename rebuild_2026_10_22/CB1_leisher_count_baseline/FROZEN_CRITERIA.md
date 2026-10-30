# CB1_leisher_count_baseline — FROZEN CRITERIA (committed alone, before any split, baseline or R2 is computed)

**Question.** Leisher+ 2026 (ApJ 1005, 186; arXiv 2511.05367) infer WDM mass from DREAMS merger trees with a GNN. How much of the result is the
subhalo count? Part A audits the authors' public code and parameter file and needs no simulation data. Part B runs count-only baselines and
needs the trees.

This is an independent audit of a CDM/WDM simulation paper. **It is not a framework test**, no framework verdict follows either way, and it uses
no framework input. Nothing here says the data favour any model. Findings concern the public code at `ilemleisher/merger_tree_gnn`, which
**may differ from the code that produced the paper's numbers**; no claim is made about what was actually run beyond what is measured here.

## 0. Seen before freezing (disclosed)

Read from source, no number computed: `graph_script.py` builds `u = log10(ngal)`; `gnn_script.py` concatenates `u[batch]` in `NodeModel` and `u` before
`outlayer`; `objective` returns `test_loss`; `split_dataset` calls `random.seed(5); random.shuffle(dataset)` in place. Paper §2.2.2: "we do not input any
global features"; §2.2.5: tuning minimizes "the validation loss", and the seeded shuffle gives "identical dataset division". Expectation: repeated in-place
shuffles change the split. My earlier chat estimates of R2 above 6 and 9.7 keV (0.35, -1.35, assuming constant RMSE) are known.

## 1. Part A (parameter file only; runs now)

Input: `WDM_TNG_MW_SB4_parameters.txt` (1007 rows; authors' repo). Target as in `norm_params`: y = 1/M in keV^-1 (`sample[:,0]` x fiducial 1, inverted twice).

- **A1 Split replay.** Exactly reproduce `split_dataset` on list indices with Python's `random`: call 0 (main's first split) and calls 1..50 (one per Optuna trial, in
  place, cumulative). Report the size of each test set and the pairwise overlap of call 0's test set with each later one.
  - **SPLIT CHANGES** if any later call's test set differs from call 0's. **SPLIT FIXED** otherwise. Repeat with a copy passed each call (the paper's stated behaviour), as control: it must be SPLIT FIXED.
- **A2 Test-set spread.** For each call: var(y_test), the number of test sims above 6.0 and 9.7 keV, and the R2 implied by fixed RMSE 0.031 (R2 = 1 - RMSE^2 / var). Report min, median, max
  across calls. This measures how much R2 moves through split choice alone.
- **A3 Reported pairs.** For each (R2, RMSE) pair in the paper (0.708/0.082, 0.509/0.107, 0.936/?, 0.957/0.031, 0.073/0.147, 0.873/0.054, 0.454/0.117), using rounding intervals (±0.0005 both), the
  implied var(y_test); report which calls admit it, and whether the implied var fits a single fixed split. **UNITS CONFIRMED** if all pairs with RMSE give a var within the range seen across calls (1/M in keV^-1).
  Pairs with unknown RMSE are skipped. Also full-sample var as control.
- **A4 Prior fractions.** Share of the 1007 sims above 6.0 and 9.7 keV. Conditional R2 at fixed RMSE 0.031, on the actual test set of call 0 and of the sample, flagged as ASSUMPTION (constant error, which the paper's own figures contradict at high mass, in the favourable direction for the paper's reader only if error were lower).
- **A5 Code facts** cited by file and line: u's definition; each place u enters the network; the objective's return; which loss the best trial is chosen on. Also whether u remains in the placeholder, main-branch, flattened and pruned cases (it is built for every graph in `create_dataset`).

**Part A reporting rule.** State each as "public code does X; paper says Y". Do not call it a bug in the published results; the authors can say what ran.

## 2. Part B (needs trees; frozen now, not run until data access exists)

Data: each box's `tree_extended.hdf5`, MW tree found per `merger_tree_script.py` (`get_MW_idx`), walked with the authors' logic, keeping only `SnapNum`, `SubhaloID`, `DescendantID`, `FirstProgenitorID`, `NextProgenitorID`, and `SubhaloMassType`.
Split: call 0's test set, untouched until the final evaluation. Models fit on train + valid only, with 5-fold CV for any hyperparameter.

- **B0**: y from log10(N_nodes) alone. Isotonic regression, and a cubic polynomial; report both, primary cubic.
- **B1**: y from N per snapshot in the 91 snapshots, log1p counts. Ridge (alpha by CV) is primary; gradient boosting reported.
- **B2 (reported)**: B1 + log10 of summed M_DM per snapshot.
- **B3 (reported)**: main-branch length alone (expected near zero).

Uncertainty: bootstrap of the test set (10000, seed 20261030) and a repeated-split distribution (200 random 80/20 splits of all 1007), with R2 and RMSE in 1/M and R2 restricted to M above 6.0 and 9.7 keV.

**Grades** versus the paper's values (no features 0.509; snapshot only 0.708; flattened 0.873; main branch 0.073):
- **COUNT SUFFICES** for a row: baseline 95% interval (repeated-split) reaches or exceeds the paper's R2.
- **GRAPH ADDS**: baseline's 95% upper limit is below the paper's R2.
- Row pairs: no features vs B0; snapshot only and flattened vs B1; best (0.957) vs B2.
- **Key decider, if the trees allow it:** retrain with `u` set to zero everywhere (`u`-ablated placeholder and snapshot-only), keeping the authors' architecture and fixed hyperparameters from Table 1 where given. Needs torch_geometric and heavy CPU, so it is **Part C**, not run without the owner's go, preemptible, per the compute rules.

## 3. Checks

- K1: parameter file has 1007 rows and 1/M inside [1/30, 1/1.8] up to rounding of the suite's stated bounds.
- K2: `split_dataset` copied verbatim from the authors' file, sizes 806/100/101 or as the code gives.
- K3: on synthetic data with a planted count law, Part B's pipeline recovers R2 within 0.03 of the truth, and for a null target gives R2 near 0.
- MUTATE (`--mutate`): targets permuted: conditional and pair checks must fail UNITS CONFIRMED or move var outside the range; separate outputs; exit 1 if it does not bite.

## 4. Limits named now

The paper's trials may have been launched separately, resumed through Optuna's database, or run from a different code revision, so the replay's call numbering is a model of the public script. The bootstrap script `gnn_bootstrap.py` is separate and not audited in Part A except as noted. No GNN is retrained in Parts A or B. The R2 conditional in A4 is an assumption, not a measurement.
