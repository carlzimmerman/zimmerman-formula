# CFG399: is the retention step keyed to virial temperature? FAILS (out of sample, the 22 super spirals above 2.3e6 K)

Criteria cca28095f (committed before the script). Script `cfg399_step_key.py`. κ = ½ fitted; both footings.

cm08–cm10 placed the retained-cold-fraction step (0.13 → 0.60) at host T_vir 0.5–2.3e6 K. A temperature-keyed (phase-change) step predicts any system hotter than 2.3e6 K sits at the upper level. The 23 Ogle+2019 super spirals are isolated discs that were not used to place the step (CFG440 session02 per-object f, enclosed baryons).

| footing | sample | N | measured median f | predicted | difference | verdict |
|---|---|---|---|---|---|---|
| canonical | T_vir > 2.3e6 K | 22 | 0.166 | 0.588 | +0.422 ± 0.062 (6.8σ) | **FAILS** |
| canonical | nine fastest | 9 | 0.485 | 0.598 | +0.113 ± 0.262 | survives |
| alt | T_vir > 2.3e6 K | 22 | 0.148 | 0.588 | +0.440 ± 0.062 (7.1σ) | **FAILS** |
| alt | nine fastest | 9 | 0.460 | 0.598 | +0.138 ± 0.259 | survives |

- **Reading.** Isolated discs with virial temperatures of 2–12 million K hold the galaxy-level fraction, not the group level. The step is not a temperature (phase) transition of the host. That agrees with cm09's finding that the step follows host *status* (group/cluster membership), not the galaxy's own σ. The nine fastest lean upward, but that is weak and partly built in, since V enters f.
- **K1 FAILED as frozen** and is kept: the frozen logistic gives f(3e5 K) = 0.142, against the required 0.13 ± 0.01, because the tails are not fully asymptotic. It moves predictions by ~0.01 against a 0.42 gap, so the verdict is unaffected. The main run exits 1 because of K1.
- **MUTATE** (measured f set to the prediction): SURVIVES, detected, exit 1.
