# project_atomos — source and results records (artifacts excluded)

This directory is the **source-only** copy of project_atomos: the search machinery, the
gate/verification scripts, the null-result records, and the write-up.

**What is deliberately NOT here.** The working repo generates ~5.3 GB of regenerable
artifacts — the depth-10 value arrays (`values_*.f64`), the value-key files
(`keys_*.txt`, ~156 MB each), `records.sqlite`, and the skeleton-layer caches. They are
excluded on purpose: git never forgets a blob, so committing them would tax every future
clone forever, and every one of them can be rebuilt from the scripts here. Rebuild with
`parallel_skeleton_layer.py` (the layers, ~5 h across 10 cores) then `sharded_build.py`
(the depth-10 value set, ~15 min with layers cached) then `sweep_depth.py` (the sweep).

**Start here.**

| file | what it is |
|---|---|
| `PAPER_ATOMOS_NULL.md` | the write-up: exhaustive null to depth 10 + the depth-ceiling argument |
| `NULL_RESULT_DEPTH10_EXHAUSTIVE.md` | the depth-10 result record, with the bugs the guards caught |
| `NULL_RESULT_D3_D18.md` | the earlier depths 3–18 record |
| `GATE_POWER_ANALYSIS.py` | why single-target matching is uninformative past depth ~10–13 |
| `BITS_RULE.py` | why Gate C must sum bits rather than count targets |
| `sweep_depth.py` | the target sweep on a prebuilt value set |
| `sharded_build.py` | the parallel exhaustive build (validated against the serial path) |
| `parallel_skeleton_layer.py` | the skeleton-layer cache: 8.019e9 sequences -> 22,708 skeletons |

**Reading the result honestly.** It is a NULL: 42,534,139 distinct values, 82,613
in-window hits, zero surviving the gate. It concerns one germ vocabulary at one depth
under one gate, and it neither supports nor damages the gravity framework whose germs it
uses — `a0`'s value, `Z`, the response sign and `omega_c` all remain postulated. See §8
of the paper for the scope statement.
