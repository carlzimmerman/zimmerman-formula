#!/usr/bin/env python3
"""Copy and validate completed native seed outputs; compute no concentration grade."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
REB = HERE.parent
ROOT = REB.parent
RUNS = REB / "X48_native_cf_zoom/runs"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inputs = [Path(__file__), REB / "X48_native_cf_zoom/x48_zoom.py",
              REB / "X48_native_cf_zoom/x48_analyze.py",
              REB / "NL1_native_level_L/nl1_native_level.py"]
    records = {}
    for seed in range(1, 10):
        src = RUNS / f"M1e12_s{seed}_ng64"
        snap, done, log = (src / n for n in ("snap_zf.npz", "done.json", "run.log"))
        if not (snap.exists() and done.exists()):
            continue
        files = [snap, done, log]
        before = {p: sha(p) for p in files}
        completion = json.loads(done.read_text())
        with np.load(snap, allow_pickle=False) as z:
            meta = json.loads(str(z["meta"]))
            checks = dict(seed=meta["seed"] == seed, grid=meta["ng"] == 64,
                mass=meta["M"] == 1e12, positions=z["x"].shape == (meta["N"], 3),
                velocities=z["v"].shape == (meta["N"], 3),
                finite=bool(np.isfinite(z["x"]).all() and np.isfinite(z["v"]).all()),
                particle_mass=bool(np.isfinite(z["m"]) and float(z["m"]) > 0
                                   and float(z["m"]) == meta["mpart"]),
                done_matches=all(completion[k] == meta[k] for k in ("steps", "t_end", "N")),
                final_log=log.read_text().splitlines()[-1] == f"done: {meta['steps']} steps")
        assert all(checks.values()), (seed, checks)
        dest = HERE / "completed" / src.name
        dest.mkdir(parents=True, exist_ok=True)
        for p in files:
            target = dest / p.name
            if target.exists():
                assert sha(target) == before[p], f"Completed output changed: {target}"
            else:
                shutil.copyfile(p, target)
            assert sha(target) == before[p]
        assert all(sha(p) == h for p, h in before.items()), "Inputs changed during publication"
        inputs.extend(files)
        records[src.name] = dict(meta=meta, completion=completion, checks=checks,
            files={str((dest / p.name).relative_to(ROOT)): before[p] for p in files})
    result = dict(observed_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        completed=len(records), expected=9, runs=records,
        assertion_tested="Final snapshot/done/log agreement, identity, array shapes and finiteness; byte-identical stable copies",
        non_claims=["No aggregate concentration or L estimate", "No NL1 grade", "No convergence or observational pass claim",
                    "Snapshot meta.L is simulation box length, not L_nat"],
        software=dict(python=sys.version, numpy=np.__version__),
        input_sha256={str(p.relative_to(ROOT)): sha(p) for p in inputs})
    (HERE / "completed_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(completed=len(records), expected=9,
        checks=sum(len(r["checks"]) for r in records.values()), seeds=list(records))))


if __name__ == "__main__":
    main()
