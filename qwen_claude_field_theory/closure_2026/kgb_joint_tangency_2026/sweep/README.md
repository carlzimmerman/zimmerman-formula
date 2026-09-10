# Local parallel search

From `kgb_joint_tangency_2026`, a bounded M4 Max run:

```sh
python3 sweep/parallel_sweep.py --output sweep/m4_run.jsonl --starts 256 --max-nfev 300
```

Resume with exactly the same semantic options and `--resume`:

```sh
python3 sweep/parallel_sweep.py --output sweep/m4_run.jsonl --starts 256 --max-nfev 300 --resume
```

Defaults: `min(8, max(1, cpu_count()-2))` spawned workers, one numerical thread
per worker, seed `20260910`. Override `--workers` if needed; it may change on
resume. Seed, start count, evaluation budget, source hashes, and package/Python
versions must match. Source pinning includes the launcher, both solvers,
parametric/fast kernels, health/refinement, and a conservative snapshot of their
six older local dependency directories. Existing output is never overwritten.
Only one writer may hold a checkpoint; completed rows are flushed and synced.
An incomplete final JSON line is rejected for explicit inspection, not silently
discarded. A changed source requires a new output file.

Even indices vary `[dw1,y2,u2,y1]` with fixed `u1`; odd indices vary
`[dw1,y2,u2,u1]` with fixed `y1`. Index 0 repeats the known joint point as a
control: it is deliberately expected to fail local angular-gradient health.
Other starts are independently seed/index-determined log-uniform points inside
the solver bounds. This samples only the solvers' negative-w, GR-connected
pressure-root chart. No excluded chart, zero-control branch, or continuous
parameter domain is ruled out by failed attempts.

Each JSONL result records optimizer success separately from numerical joint
acceptance, local health-screen rejection, and the independent-verification
queue. Health-screen errors are failures, not rejections or queued candidates.
Solver/chart errors retain their messages and job inputs. Crashed worker pools
stop the run; unfinished jobs remain available on resume. `max-nfev` is SciPy's
function-evaluation budget (numerical-Jacobian work is additional), **not a wall
clock limit**. There is no hard timeout; interruption may wait for running workers.

For a queued index, export a flat candidate and explicitly run the independent
verifier (the launcher never launches an unbounded verification automatically):

```sh
python3 sweep/parallel_sweep.py --output sweep/m4_run.jsonl --export-index 12 --candidate-out sweep/candidate12.json
python3 refine_joint.py --candidate-json sweep/candidate12.json --dps 60 80
```

No result is a full-theory PASS: further preservation, nonlinear closure,
source calibration, and empirical/cosmological tests remain separate. The
launcher makes **zero model or network API calls** and uses existing local
Python, NumPy, SciPy, SymPy, and mpmath only.

Small regression suite: `python3 -m unittest discover -s sweep -p 'test_sweep.py'`.
The final `smoke_002.jsonl` is only four jobs, two workers, and one solver
evaluation per job; it is a launcher check, not a parameter survey.
`smoke_001.jsonl` retains the preliminary run before two transitive source
dependencies were added to the pin set; use run 002 as the final evidence.
