# CB1_leisher_count_baseline: the public code feeds the node count directly to the network; the paper says no global features. Baselines still need the trees

Criteria: `FROZEN_CRITERIA.md` (53735de87f, committed alone). **Independent audit of Leisher+ 2026 (ApJ 1005, 186; arXiv 2511.05367). Not a framework test;
no framework verdict follows either way.** Findings describe the public code at `ilemleisher/merger_tree_gnn` commit 6d01c315d1, which may differ from what produced the
paper's numbers. Part A numbers are from `cb1_part_a.out`; synthetic checks from `cb1_part_b_synthetic.out`. `authors_code/` holds a copy of the authors' parameter file, unmodified.

## Status

| Part | Status |
|---|---|
| A: code and parameter-file audit | **Done** |
| B: count-only baselines | **Pipeline validated on synthetic data only. Not run: needs DREAMS trees** (interest form and Globus sign-in, owner's step) |
| C: retrain with `u` set to zero | **Not run.** This is the real decider; needs the trees, torch_geometric and heavy CPU; owner's go |

**So the question "does a count reproduce the GNN?" is NOT answered yet.**

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
