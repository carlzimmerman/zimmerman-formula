# SY1_free_constant_law_search: built and running; no result yet

Criteria `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md` (start now, beside BF1), `AMENDMENT_A2.md` (readings the criteria left open). **Not blind.** A hit is a description of data, not a theory. kappa = 1/2 FITTED. No cold component, no particle. Reinstates nothing. Not theory closed. Nothing here says the data favour the framework.

## Files
- `sy1_leaves.py`: leaves and wrappers, one formula for every system. `sy1_data.py`: BF1's loading and split, read from `bf1.py` unedited, its sha stored per search.
- `sy1.py MODE`: real, scrambled, planted, mutate; outputs in `runs/MODE/`. One seeded, serial, one-core search per worker. State saved every 20 iterations, so SIGTERM loses at most one slice.
- `sy1_read.py MODE [--stage3]`: gates. Real refuses until the three controls are read.
- `sy1_stage3.py`: RQ3's acceptance.py, unedited, with this lane as its working directory.
- `run_sy1.sh`: the whole run, ending in `sy1_search.done`.

## Run length, fixed before launch
**1500 iterations per search**, PySR's other settings at their defaults, maxsize 30.

| Mode | Searches |
|---|---|
| planted | 64: 8 tags x 8 seeds, planted wrapper only |
| real | 48: 2 arms x 3 wrappers x 8 seeds |
| scrambled | 48, same length |
| mutate | 6, one seed each |

From the smoke test: about 2.5 s per iteration, one core, machine load 25-40, flat over 400 iterations. So about 1 hour per search and, on 8 cores, about 21 hours of 166 searches, plus any yield. Iterations could slow as populations grow; that's untested past 400.

## Smoke test, planted and scrambled data and H = 1 only, no real-data search
- H = 1 in W3 through RQ3, without keys or Bullet: every computed row's label and Z match RQ3's law. A candidate reading every leaf ran the full card with keys and Bullet, no label reads. B1, A15 and B28 read NOT COMPUTABLE for it, as they should.
- At 40-260 iterations and one seed: P2 recovered noise-free and at real errors, P3 noise-free, P1 in arm Z at real errors. The other tags weren't tried long enough to say, so this isn't the planted result.
- Found and fixed: resume failed on a lost operator mapping; the yield check matched shell text; a worker quit when its launching shell ended. Resume and pool SIGTERM (exit 75) then tested.

## Environment
PySR 1.5.9 with its own Julia 1.11.9 from juliapkg, already installed, offline. Nothing was installed. `/opt/homebrew/bin/julia` isn't used.

## Limits on record
A2's list. Point-rule rows for s and D, Pareto front only, no refit at alt.

kappa = 1/2 FITTED; not theory closed.
