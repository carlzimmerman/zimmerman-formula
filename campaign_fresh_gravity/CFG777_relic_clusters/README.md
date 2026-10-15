# CFG777: frozen relic (tether set by the PEAK condensed mass) in groups and clusters. FAIL

**Hypothesis.** Systems that lost condensed baryons keep their cold energy tethered at the law of the peak condensed mass,
p × M_cond, with Tacconi p = 1.873 primary. Brackets: p = 1, 1.5, 2, 3.

**Result** (both kernels, both footings, Tacconi p). FAIL on 0 of 3 tests.

| test | result |
|---|---|
| eRASS1 318 | overshoot: A_MID 0.66–0.81 (Z −3 to −8) |
| ACCEPT 8 | strong overshoot: A_OUTER 0.33–0.35 (Z −7 to −8) |
| eFEDS 131 | χ² 22–23 on 8 dof (p ≈ 0.004) |

- Every bracket fails. Even p = 1, i.e. no relic and the plain condensed source, overshoots ACCEPT and misses eRASS1 high.
- A frozen relic adds mass where clusters do not want it. This agrees with CFG776: surplus tethered cold energy is
  expelled dynamically within 50–100 t₀.
- **The relic route to the cluster and early-type excess is closed.**

Controls: M1 (p = 1 reproduces CFG721 exactly) and M0 (the law reproduces CFG686) pass. M2 (shuffled p) bites. 4/4 checks
pass.

The first run crashed (NameError, P_TAC) and was fixed by moving CASES after P_TAC. The run was interrupted at
16:42 and resumed: the erass and accept stages had completed before the stop; efeds and score reran.

κ fitted; not theory closed.
