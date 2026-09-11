#!/usr/bin/env python3
"""Run reproducible new checks and relevant existing controls, in parallel.

An exit code certifies execution/check status, not completion of a theory.
Outputs and hashes are retained for completed jobs, including nonzero exits.
An externally interrupted or timed-out runner may not produce a manifest.
No dependency installs. Inputs must remain unchanged across the entire run.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/".git").exists())
RUN = HERE/"run_001"
LEAN_ENV = HERE.parent.parent/"clock_constitutive_construction_2026/lean_formalization_2026"


def run_all():
    RUN.mkdir(exist_ok=True)
    python_jobs = [
        ("background",HERE/"background.py"),
        ("background_tests",HERE/"test_background.py"),
        ("initial",HERE/"initial.py"),
        ("initial_tests",HERE/"test_initial.py"),
        ("slice_derivation",HERE/"slice_action/derive.py"),
        ("slice_tests",HERE/"slice_action/test_slice.py"),
        ("potentials",HERE/"potentials.py"),
        ("potential_tests",HERE/"test_potentials.py"),
        ("experiment",HERE/"run_experiment.py"),
        ("existing_action",HERE.parent/"spherical_baryon_bridge/action/derive.py"),
        ("existing_matter",HERE.parent/"spherical_baryon_bridge/action/matter.py"),
        ("existing_background",HERE.parent/"cubic_background_completion/derive.py"),
    ]
    jobs = [(name,[sys.executable,"-B",str(path.relative_to(ROOT))],ROOT)
            for name,path in python_jobs]
    lake = shutil.which("lake")
    if lake is None:
        raise RuntimeError("existing lake executable is required; not installing it")
    jobs.append(("lean",[lake,"env","lean",str(HERE/"lean/SmallSourceObstruction.lean")],LEAN_ENV))
    inputs = list(HERE.rglob("*.py"))+list(HERE.rglob("*.lean"))+list(HERE.rglob("*.md"))
    inputs += [path for _,path in python_jobs if not path.is_relative_to(HERE)]
    inputs += [HERE.parent/"nonlinear_transport/stationary.py"]

    def hash_inputs():
        return {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(set(inputs))}
    hashes_before = hash_inputs()

    def execute(job):
        name,command,cwd = job
        started = time.monotonic()
        result = subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=180)
        (RUN/(name+".stdout.txt")).write_text(result.stdout)
        (RUN/(name+".stderr.txt")).write_text(result.stderr)
        row = dict(name=name,command=command,cwd=str(cwd.relative_to(ROOT)),
                   exit_status=result.returncode,seconds=round(time.monotonic()-started,3))
        print(json.dumps(row),flush=True)
        return row

    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(execute,jobs))
    hashes = hash_inputs()
    inputs_stable = hashes_before == hashes
    head = subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    manifest = dict(status="checks_passed" if inputs_stable and all(row["exit_status"]==0 for row in rows) else "failed",
                    python=platform.python_version(),platform=platform.platform(),head_at_run=head,
                    jobs=rows,sha256=hashes,sha256_before=hashes_before,inputs_stable=inputs_stable,
                    scope="initial slice and conditional algebra only; full theory remains OPEN")
    (RUN/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return 0 if manifest["status"]=="checks_passed" else 1


if __name__ == "__main__":
    sys.exit(run_all())
