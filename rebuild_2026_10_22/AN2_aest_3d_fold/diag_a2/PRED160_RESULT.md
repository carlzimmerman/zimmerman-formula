# AN2 diagnostic P160, result: PREDICTED. All four 160^3 shape rows land within 0.7 % of the frozen predictions. Diagnostic only; AN2 stays NO VERDICT, no label changes.

Note `PRED160_NOTE.md`, predictions frozen and pushed before any run. Data `pred160.jsonl`. Rows as AN2 S1 (hold on, baryon stop, eta 0.05, L = 8 q_t, canonical, TSC), N 160. Not blind to 64/128, blind to 160.

| Row | t(128) | Predicted t(160) | Ran t(160) | Off | Move 128 to 160 | Fold |
|---|---|---|---|---|---|---|
| 1e12 A | 5.401 | 5.232 | 5.262 | +0.58 % | −2.57 % | filament |
| 1e12 B | 5.039 | 4.868 | 4.901 | +0.68 % | −2.73 % | sheet (canonical filament at 128) |
| 1e15 A | 5.028 | 4.870 | 4.879 | +0.18 % | −2.97 % | point (filament at 128) |
| 1e15 B | 4.765 | 4.616 | 4.626 | +0.22 % | −2.91 % | filament |

## Read
- **PREDICTED** by the frozen rule: every row within 1 %. The grid error scales as N^-p with SG's pure-dust orders, and multiplies with hold, to under 0.7 %. All four misses are on the late side, like the spheres' retro check (+0.25, +0.7 %), so the rule slightly over-corrects, more at 1e12 where hold is large.
- Two fold labels changed class at 160 (1e12 B filament to sheet, 1e15 A filament to point). Reported as is; by the note this isn't a timing miss. The label of a fold this close to the sphere's is grid-sensitive, and the time isn't.
- So SG's grid-corrected shifts and its read that every shape folds 5-16 % before AN1's sphere stand as the output of a correction that has now predicted fresh runs. Still a read, not an AN2 label: AN2's frozen section 9 compares the 128^3 rows as they are.
- Every row still moves about 3 % from 128 to 160, so none is settled at 160 by SL's 3 % line.

## Compute
4 runs, nice 15, one thread, two at a time, 2026-11-04 16:09-17:15 UTC. 1809-1930 CPU s, 2.67-2.86 GB, over the 1 GB target, under the 67.5 min cap.

kappa = 1/2 FITTED. Canonical only, footings not pooled. A gravitating field, never a particle. The cold sector stays retired. No LCDM input. Not theory closed. Nothing here says the data favour the framework.
