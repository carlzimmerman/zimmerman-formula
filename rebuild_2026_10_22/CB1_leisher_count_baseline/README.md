# CB1_leisher_count_baseline: the public code feeds the node count directly to the network; the paper says no global features. Baselines still need the trees

Criteria: `FROZEN_CRITERIA.md` (53735de87f, committed alone). **Independent audit of Leisher+ 2026 (ApJ 1005, 186; arXiv 2511.05367). Not a framework test;
no framework verdict follows either way.** Findings describe the public code at `ilemleisher/merger_tree_gnn` commit 6d01c315d1, which may differ from what produced the
paper's numbers. Part A numbers are from `cb1_part_a.out`; synthetic checks from `cb1_part_b_synthetic.out`. `authors_code/` holds a copy of the authors' parameter file, unmodified.

## Status

| Part | Status |
|---|---|
| A: code and parameter-file audit | **Done** |
| B: count-only baselines | **Done on all 1007 real trees** (`cb1_part_b.out`, `cb1_counts.npz`) |
| C: retrain with `u` set to zero | **Not run.** This is the real decider; needs edges re-fetched, torch_geometric and heavy CPU, and waits on the live zooms |

**So: counts reach the no-feature and snapshot-only rows, and do not reach the best model. Whether the published networks used the count or found the same information in the structure is NOT answered.**

## Part B results

| Paper's row (R² / RMSE) | Baseline | Same test set R² / RMSE | Repeated-split 95 % | Frozen grade |
|---|---|---|---|---|
| No features 0.509 / 0.107 | B0 cubic (primary), log N only | 0.426 / 0.116 | 0.438–0.651 | COUNT SUFFICES |
| | B0 isotonic, log N only | **0.499 / 0.108** | 0.468–0.657 | |
| Snapshot only 0.708 / 0.082 | B1 ridge (primary), N per snapshot | 0.644 / 0.091 | 0.658–0.809 | COUNT SUFFICES |
| | B1 gradient boosting | **0.703 / 0.083** | 0.696–0.812 | |
| Flattened 0.683 / 0.086 | B1 ridge | 0.644 / 0.091 | 0.658–0.809 | COUNT SUFFICES |
| Best 0.957 / 0.031 | B2 ridge, N and summed M_DM per snapshot | 0.721 / 0.081 | −2.755–0.848 | GRAPH ADDS |

**Read the frozen grade with care.** It uses the repeated-split upper limit, and call 0's test set is harder than average, so it is generous. On the paper's own test set the primary models fall short (0.426, 0.644), and the two non-primary models land within 0.01 (0.499, 0.703). Those two were chosen by the criteria as reported variants, not picked after the fact, but with two tries per row the closeness is suggestive only.

- **The best model is untouched.** R² 0.957 is well above every baseline: its node features carry information that per-snapshot totals do not.
- **All baselines fail in the cold regime:** R² −6 to −14 above 6 keV and −18 to −48 above 9.7 keV on the test set. The paper's constant-error estimate is not directly comparable.
- **B3 main branch:** test R² −2.675, not a usable comparison with the paper's 0.073. A cubic on a nearly constant quantity with a few outliers is unstable.
- N spans 149–8717, median 2697; Spearman with 1/M −0.762.
- **What this does and does not show:** a single number nearly matches the no-feature model, which fits finding 1. A network can also recover the same information from graph structure, so this does not show `u` produced the 0.509.

## Data step (`cb1_fetch.py`)

Trees read over Globus HTTPS one box at a time and deleted. **K5:** on boxes 0, 3 and 1000 our walk equals the authors' recursion in N and per snapshot. **Mapping:** every box's feedback parameters in its catalog match the table row under the authors' mapping (max difference 5.0e-05, the storage rounding).
**The DREAMS README's statement that row i is box_i is wrong for `WDM_TNG_MW_SB4.txt`:** the table has the 17 corrupted boxes removed, so rows shift (box 3 is row 1). The authors' code handles this; following the README would mispair trees and parameters.
MUTATE with permuted targets: `cb1_part_b_MUTATE.out`. `np.polyfit` reproduces the B0 cubic (R² 0.4257, the numpy warnings are harmless).

## Part A findings

**1. Node count as a direct input (the main finding).** `graph_script.py:131` sets `u = np.log10(ngal)` for every graph. `gnn_script.py:122` concatenates `u[batch]` in every
node update, and `gnn_script.py:188` concatenates `u` directly before the output layer. The paper's §2.2.2 says "we do not input any global features". If the published runs
used this code, then the "no node features" model (R² 0.509) was given the node count directly, and it also explains why the main branch fails: its node count is nearly fixed. This is a reading of
the code. No retraining was done, and the authors can say what ran.

**2. Split.** The public script shuffles one list in place, so the split changes per trial (SPLIT CHANGES; control with a copy, SPLIT FIXED). Call 0's test set shares a median 10 of 100 sims with later calls' test sets, and a median 80
with later train sets.

**But the reported numbers do not behave that way.** Six published R²/RMSE pairs fit one test-set variance, [0.02314, 0.02335], which is admitted by calls 0, 16 and 40 only:
snapshot only, no features, best, main branch, flattened (ApJ), and pruned (caption). Six independent splits would each fit their own pair with probability 3.0e-6. **So this supports the paper's
statement that networks share one division, for the reported metrics.** I expected the opposite, and this finding goes against the suspicion. No claim of leakage is made. How a best trial's hyperparameters became a final metric is not in
the public script; a fresh retrain on call 0's split would be clean, and it fits this result.

**3. Selection.** `objective` returns `test_loss` (`gnn_script.py:365`), and best trial is chosen on it (`:429`); the paper's §2.2.5 says validation loss. Given finding 2, the effect on the final numbers is unknown and may be small.

**4. Units confirmed.** RMSE is in 1/M keV⁻¹ (`denormalize`, and all pairs fit the data's variance); the wrong-unit MUTATE fails it. So R² is dominated by warm models:
25.8% of the sims are above 6.0 keV and 13.6% above 9.7 keV. Call 0's test set has 23 and 12. Fixed RMSE 0.031 implies R² +0.29 and −1.27 there. **That is an ASSUMPTION, not a measurement** (constant error).

**5. R² from split choice alone.** With fixed RMSE 0.031, R² runs 0.947–0.965 across the 51 test sets. Differences such as 0.936 / 0.945 / 0.957 are comparable with this.

**6. A likely resolution of the paper's pruning mismatch.** The caption's 0.477 / 0.110 fits the shared test set. The text's 0.454 / 0.117 does not (implied variance [0.02483, 0.02531]), so the caption is probably the
right value. The published main-branch and flattened χ² are both printed as 1.704, which is worth a check.

## Correction: arXiv v1 and the published text differ

The chat drafts quoted a flattened R² of 0.873 from arXiv v1. **The published value is 0.683 (RMSE 0.086),** and the published text adds a bootstrap (original 0.696 ± 0.113, flattened 0.702 ± 0.150) and concludes that tree structure is not necessarily sensitive to WDM and that node counts
hold the predictive power. The published paper has therefore already moved most of the way to the "count" reading. The new question is finding 1, which is not addressed there.

## Amendments and deviations (after the first run)

1. A3 was frozen with arXiv pairs. The published pairs and a chance level were added as `A3-ApJ` after the first run. The original lines are unchanged. This also added the pruned caption pair.
2. MUTATE: permuting targets cannot bite a variance statistic, as the output says, so the wrong-unit target carries the tooth. Disclosed; the frozen wording did not foresee this.
3. Part B's first synthetic run crashed on an indexing error in the check, fixed, and an unused line and a loose K3 condition were removed. No real data was involved.
4. Numpy emits "divide by zero in matmul" in these fits, including on a clean toy fit, so it looks environmental. Fits stay finite and K3 / K4 pass. **Re-check against `np.polyfit` before grading real data.** B2 ridge has a wide repeated-split range on synthetic data; treat it with care.

## Checks

K1 and K2 (807 / 100 / 100) pass. K3 planted law: truth 0.935, B0 0.945. Null target near zero. K4: the iterative walk equals the authors' recursion on 20 random trees. These validate the pipeline, not any real number. `extract` has never touched a real tree file.

## Limits

Trial numbering assumes the public script's order; Optuna runs may have been resumed or split across jobs. Published values were read through a fetch tool, so check them against the PDF before citing them publicly. Nothing here says the paper's conclusion is wrong, or that WDM can't be inferred from these trees.
