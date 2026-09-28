# CFG19 — the harness re-scored with CFG18

Script: `CFG19_harness_rescore.py`, under a second.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Without the substitution B stays at 38/48, and H1 fails (rc = 1).

FG097's committed harness scored candidate B (CFG4's target plus FG001) at 38/48. Two of B's population gates, both M31 dwarf samples, were computed from the satellites' stripped present-day stars, on each footing.

CFG18 re-scored them with the infall baryons FG001's class A calls for, using the conservative bracket. This lane swaps exactly those four rows and recounts.

| check | result |
|---|---|
| C1: every candidate's committed score recounted from its committed rows | exact (A 32, B 38, C 34, D 32, F 36 out of 48) |
| **H1: B with CFG18's four M31 rows** | **42/48**. M31 LVD 1.63σ / 1.24σ and Collins 1.44σ / 1.21σ: FAIL → PASS on both footings |

**B still fails:**
- the MW ultra-faints, on both footings; CFG18 leaves them at 7–8σ;
- Chae's D1 / D2 external-field gates, on both footings.

The Chae gates are FG001's committed values, from Chae's own fits. CFG8's refit under the framework's own law (1.7–2.2σ canonical) is a different statistic and is **not** substituted here.

The external-field rival (D) stays at 32/48.
