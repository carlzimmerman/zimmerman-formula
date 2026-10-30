# CB1 Part C: FROZEN CRITERIA (committed alone, before any GNN is trained)

Extends `FROZEN_CRITERIA.md` §2 (53735de87f), which named the `u`-ablated retrain and left its details open. Not a framework test; no framework verdict follows. Findings describe the public code at commit 6d01c315d1, which may differ from what produced the paper's numbers.

## 0. Seen before freezing (disclosed)
- Part B's baselines (`cb1_part_b.out`).
- **New reading of `graph_script.py` `get_edges`:** `desid_to_idx[did] = j` overwrites, so each descendant keeps one progenitor edge. Measured on real boxes 0, 3, 1000: 5550 of 6046, 4027 of 4293, 3655 of 3933 true edges kept (91.8 %, 93.8 %, 92.9 %), giving 497, 267, 279 connected components, where the true tree has 1. Paper §2.2.1: edges pair "each subhalo with its unique descendant". Reported as "public code does X; paper says Y", not as a bug in published results.
- **New reasoning:** `global_add_pool` scales with node count, so zeroing `u` alone may not remove the count. That is why arm C exists.
- Table 1 gives hyperparameters only for the best M_WDM model: lr 1.889e-5, wd 5.139e-7, nl 4, hc 128.

## 1. Design
Inputs: `x = 1` (placeholder; paper 0.509 / 0.107) and `x = SnapNum` raw, as in the public graph script (snapshot only; paper 0.708 / 0.082).

| Arm | `u` | Add pool | Edges |
|---|---|---|---|
| A control | log10 N, as public code | yes | authors' `get_edges` |
| B | 0 | yes | authors' |
| C | 0 | zeroed | authors' |
| D | 0 | yes | true tree: every subhalo linked to its descendant, same direction |

Two inputs × four arms × seeds 1, 2, 3 = 24 runs.

Fixed for all: authors' architecture, `edge_attr` ones, loss, Adam, CyclicLR (max 1e-3, step_up 500), batch 32, 1000 epochs, Table 1 hyperparameters, best-validation weights, call 0's split from `cb1_part_a_results.json`. **Hyperparameters are not re-tuned:** the paper ran 50 trials per model, which is out of reach here. Metric: R² and RMSE in 1/M on call 0's test set; arm value = mean of three seeds.

## 2. Verdicts, per input
`T = max(0.05, 2 × pooled seed sd)`.
- **Control:** REPRODUCED if arm A's mean is within 0.10 of the paper. Otherwise NOT REPRODUCED: the comparisons below still stand among themselves but say nothing about the published values.
- **A vs B:** U MATTERS if A − B > T, else U NOT NEEDED.
- **B vs C:** ADD POOL CARRIES IT if B − C > T, else ADD POOL NOT NEEDED.
- **D vs B:** BRANCHING MATTERS if |D − B| > T, stating the sign; else NO BRANCHING EFFECT.
- **Structure beyond count, input `x = 1` only:** STRUCTURE ADDS if C − 0.499 (Part B's log N isotonic) > T, else NO STRUCTURE GAIN SHOWN. C has no direct route to N but can still sense it through max and mean pools, so this is a lower-confidence reading.

Declared now: U NOT NEEDED would mean the §2.2.2 wording difference did not drive the result, and would weaken the hook sent to the authors. That is to be said plainly.

## 3. Checks
- K6: our graph network equals an explicit-loop calculation of the authors' equations on a small graph, to 1e-5, for each arm's switches. Scatter max on a node with no incoming edge gives 0, stated as our assumption for `torch_scatter`.
- K7: authors' `get_edges` copied verbatim gives the same edge count as our derivation from stored descendants on boxes 0, 3, 1000 (values in §0).
- K8: resume equivalence: a short run uninterrupted vs SIGTERM + `--resume` gives identical weights, per the job contract.
- K9: **smoke:** on a planted target of log N, a 60-epoch arm A reaches test R² > 0.8, or the trainer is treated as broken.
- MUTATE (`--mutate`): targets permuted, arm A `x = 1`, one seed, 200 epochs, separate outputs: test R² < 0.1, or exit 1.

## 4. Limits named now
Untuned hyperparameters may hurt some arms more than others. One split, three seeds. torch_scatter and PyTorch Geometric are replaced by plain torch with K6 as the guard. CPU, not GPU, so seeds do not match any run of the authors. Preemptible through `compute_queue`; no result is read before all 24 finish.
