#!/usr/bin/env python3
"""Reproduce the bounded study with execution failures and provenance preserved.

Only this study's results, figure, log and manifest are published. Research data
are read-only; legacy commands and newly generated artifacts use a temporary
working directory. A zero runner exit is not acceptance of a physical theory.
The job-record/hash design extends algebraic_connection_no_mond_2026/run_audit.py;
that source is included in the input hashes as code provenance.
"""

from datetime import datetime, timezone
import hashlib
from importlib import metadata
import json
import math
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENVIRONMENT = {
    "PYTHONDONTWRITEBYTECODE": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
}
REQUIRED_LOCAL = (
    "response_math.py", "test_response_math.py", "empirical.py",
    "test_empirical.py", "render_results.py", "test_render_results.py",
    "run_study.py", "test_run_study.py", "CONTRACT.md", "DERIVATION.md",
    "LITERATURE.md", "REPORT.md",
)
REQUIRED_LEGACY = (
    "orbit_shape.py", "test_orbit_shape.py", "kernel_comparison.py",
    "test_kernel_comparison.py",
)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def record_job(argv, cwd, timeout=180, environment=None):
    """Capture success, nonzero exit, missing executable and bounded timeout."""
    if not math.isfinite(timeout) or not 0 < timeout <= 180:
        raise ValueError("job timeout must be finite and in (0, 180] seconds")
    started_at, started = utc_now(), time.perf_counter()
    override = dict(environment or {})
    override.update(ENVIRONMENT)  # A caller cannot undo the resource caps.
    env = dict(os.environ)
    env.update(override)
    argv = [str(value) for value in argv]
    try:
        completed = subprocess.run(argv, cwd=cwd, env=env, text=True,
                                   encoding="utf-8", errors="replace",
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   timeout=timeout, check=False)
        output, status, timed_out = completed.stdout, completed.returncode, False
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        status, timed_out = 124, True
    except OSError as error:
        output = f"{type(error).__name__}: {error}\n"
        status, timed_out = 127, False
    return {"argv": argv, "command": shlex.join(argv), "cwd": str(cwd),
            "environment_override": override, "timeout_seconds": timeout,
            "exit_status": status, "timed_out": timed_out,
            "started_at": started_at, "ended_at": utc_now(),
            "runtime_seconds": time.perf_counter()-started, "output": output}


def fingerprint(path, root=ROOT):
    path, root = Path(path), Path(root)
    try:
        label = str(path.relative_to(root))
    except ValueError:
        label = str(path)
    record = {"path": label, "sha256": None}
    try:
        record["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        record["error"] = f"{type(error).__name__}: {error}"
    return record


def source_inventory(here=HERE, root=ROOT):
    """Include missing mandatory paths and detect added/deleted source files."""
    here, root = Path(here), Path(root)
    legacy = here.parent/"two_kernel_orbit_shape_2026"
    paths = {here/name for name in REQUIRED_LOCAL}
    paths.update(path for path in here.rglob("*")
                 if path.is_file() and path.suffix in (".py", ".md"))
    paths.update(legacy/name for name in REQUIRED_LEGACY)
    paths.update(legacy.glob("*.py"))
    paths.add(here.parent/"algebraic_connection_no_mond_2026/run_audit.py")
    paths.update((root/"hunt_2026/hunt_lib.py",
                  root/"real_research/data/SPARC_Lelli2016c.mrt"))
    catalog = sorted((root/"real_research/data/sparc_data").glob("*_rotmod.dat"))
    paths.update(catalog)
    errors = ([] if len(catalog) == 175 else
              [f"Expected 175 SPARC rotmod inputs; found {len(catalog)}"])
    errors.extend(f"Missing required input: {path}" for path in sorted(paths)
                  if not path.is_file())
    return sorted(paths), errors


def git_state(root=ROOT):
    revision = record_job(["git", "rev-parse", "HEAD"], root, timeout=30)
    status = record_job(["git", "status", "--porcelain"], root, timeout=30)
    if revision["exit_status"] or status["exit_status"]:
        return {"commit": None, "dirty": None,
                "error": revision["output"]+status["output"]}
    entries = status["output"].splitlines()
    return {"commit": revision["output"].strip(), "dirty": bool(entries),
            "status_porcelain": entries}


def job_plan(here, root, scratch):
    here, root, scratch = Path(here), Path(root), Path(scratch)
    legacy = here.parent/"two_kernel_orbit_shape_2026"
    cache = {"MPLCONFIGDIR": str(scratch/"matplotlib"),
             "XDG_CACHE_HOME": str(scratch/"xdg-cache"), "MPLBACKEND": "Agg"}
    return [
        {"name": "study_unittests", "argv": [sys.executable, "-m", "unittest", "discover", "-s", str(here), "-v"], "cwd": scratch, "environment": cache},
        {"name": "response_math", "argv": [sys.executable, str(here/"response_math.py")], "cwd": scratch, "environment": {}},
        {"name": "empirical", "argv": [sys.executable, str(here/"empirical.py"), "--output", str(scratch/"results.json")], "cwd": scratch, "environment": {}},
        {"name": "render_results", "argv": [sys.executable, str(here/"render_results.py"), "--input", str(scratch/"results.json"), "--output", str(scratch/"finite_interval_results.png")], "cwd": scratch, "environment": cache},
        {"name": "orbit_shape_unittests", "argv": [sys.executable, "-m", "unittest", "discover", "-s", str(legacy), "-v"], "cwd": scratch, "environment": {}},
        {"name": "orbit_shape", "argv": [sys.executable, str(legacy/"orbit_shape.py")], "cwd": scratch, "environment": {}},
    ]


def failure_reasons(jobs, inputs_start, inputs_end, commit_start, commit_end, errors):
    reasons = list(errors)
    if any(job["exit_status"] != 0 or job["timed_out"] for job in jobs):
        reasons.append("At least one command failed or timed out")
    if inputs_start != inputs_end:
        reasons.append("Source/data inventory or content changed during execution")
    if any(item["sha256"] is None for item in inputs_start+inputs_end):
        reasons.append("At least one required input is unreadable")
    if commit_start is None or commit_end is None or commit_start != commit_end:
        reasons.append("Git revision unavailable or changed during execution")
    return reasons


def software_versions():
    result = [f"Python {platform.python_version()}"]
    for package in ("numpy", "scipy", "sympy", "mpmath", "matplotlib"):
        try:
            result.append(f"{package} {metadata.version(package)}")
        except metadata.PackageNotFoundError:
            result.append(f"{package}: unavailable")
    return result


def main():
    started_at, started = utc_now(), time.perf_counter()
    repository_start = git_state()
    paths_start, preflight_errors = source_inventory()
    inputs_start = [fingerprint(path) for path in paths_start]
    errors = list(preflight_errors)
    if any(item["sha256"] is None for item in inputs_start):
        errors.append("Input preflight found an unreadable source or data file")
    records, publications, empirical_metadata = [], [], {}
    with tempfile.TemporaryDirectory(prefix="finite-interval-study-") as scratch_name:
        scratch = Path(scratch_name)
        (scratch/"matplotlib").mkdir()
        (scratch/"xdg-cache").mkdir()
        if not errors:
            for job in job_plan(HERE, ROOT, scratch):
                print("RUN", job["name"], shlex.join(str(v) for v in job["argv"]), flush=True)
                record = record_job(job["argv"], job["cwd"], environment=job["environment"])
                record["name"] = job["name"]
                records.append(record)
                print(f"exit={record['exit_status']} elapsed={record['runtime_seconds']:.3f}s", flush=True)
            for filename, producing_job in (("results.json", "empirical"),
                                             ("finite_interval_results.png", "render_results")):
                path = scratch/filename
                producer = next(record for record in records if record["name"] == producing_job)
                if producer["exit_status"] != 0 or not path.is_file():
                    errors.append(f"Fresh output not available from successful producer: {filename}")
                    continue
                try:
                    payload = path.read_bytes()
                    if filename.endswith(".json"):
                        content = json.loads(payload)
                        empirical_metadata = {key: content[key] for key in ("seed", "replicates")}
                    elif not payload.startswith(b"\x89PNG\r\n\x1a\n"):
                        raise ValueError("Generated figure is not a PNG")
                    (HERE/filename).write_bytes(payload)
                    publications.append({"staged_path": str(path), "published_path": str(HERE/filename)})
                except (OSError, ValueError, KeyError) as error:
                    errors.append(f"Cannot validate/publish {filename}: {type(error).__name__}: {error}")
    paths_end, end_errors = source_inventory()
    inputs_end = [fingerprint(path) for path in paths_end]
    repository_end = git_state()
    errors.extend(end_errors)
    if len(records) != 6:
        errors.append(f"Expected six fresh jobs; executed {len(records)}")
    reasons = failure_reasons(records, inputs_start, inputs_end,
                              repository_start["commit"], repository_end["commit"], errors)
    log = [f"START: {started_at}\nPREFLIGHT ERRORS: {json.dumps(preflight_errors)}\n"]
    for record in records:
        log.append(f"JOB: {record['name']}\nCOMMAND: {record['command']}\nCWD: {record['cwd']}\n"
                   f"ENVIRONMENT: {json.dumps(record['environment_override'], sort_keys=True)}\n"
                   f"EXIT: {record['exit_status']} TIMEOUT: {record['timed_out']}\n"
                   f"SECONDS: {record['runtime_seconds']:.6f}\n{record['output']}\n")
    log.append("EXECUTION FAILURE REASONS: "+json.dumps(reasons))
    (HERE/"audit_output.txt").write_text("\n".join(log)+"\n", encoding="utf-8")
    output_paths = sorted(path for path in HERE.iterdir() if path.is_file()
                          and path.name != "computation_manifest.json"
                          and path.suffix in (".py", ".md", ".json", ".png", ".txt"))
    manifest = {
        "schema_version": 1,
        "claim_id": "finite-interval-exponential-mond-sparc-2026-09-04",
        "repository": {"commit": repository_start["commit"], "dirty": repository_start["dirty"],
                       "start": repository_start, "end": repository_end},
        "command": shlex.join([sys.executable, str(HERE.relative_to(ROOT)/"run_study.py")]),
        "environment": {"software": software_versions(),
                        "hardware": f"{platform.machine()}; {platform.platform()}",
                        "subprocess_environment_override": ENVIRONMENT},
        "mathematics": {
            "assertion_tested": "Finite-interval slope/convexity corollaries and frozen one-triple-per-galaxy SPARC response-shape comparisons; see CONTRACT.md and REPORT.md.",
            "coefficient_domain": "Exact symbolic expressions plus finite-precision positive real accelerations and galaxy bootstrap samples",
            "conventions": "b is baryonic acceleration; g observed/model acceleration; contrasts in log10; mu_exp and nu_rar are distinct kernels",
            "inputs": inputs_start,
            "inputs_end": inputs_end,
            "bounds": {"SPARC_rotmod_files": 175, "jobs": 6, "per_job_timeout_seconds": 180,
                       "empirical_randomness": empirical_metadata},
            "non_claims": ["Execution success does not imply scientific acceptance or a full relativistic theory.",
                           "Finite data and symbolic identities do not certify global literature novelty.",
                           "The algebraic response approximation does not solve disk-field or external-field equations.",
                           "Conditional rotation-curve errors omit unavailable full baryonic/inter-ring covariance."]},
        "randomness": {"used": True, "generator": "NumPy default_rng (PCG64); galaxy bootstrap and seeded synthetic tests",
                       "seed": {"empirical": empirical_metadata.get("seed"),
                                "empirical_synthetic": (empirical_metadata["seed"]+1) if "seed" in empirical_metadata else None,
                                "legacy_profile_tests": [7, 11],
                                "test_details": "Additional synthetic seeds are fixed in the hashed test sources."}},
        "run": {"started_at": started_at, "ended_at": utc_now(),
                "runtime_seconds": time.perf_counter()-started, "exit_status": 1 if reasons else 0,
                "source_inputs_unchanged": inputs_start == inputs_end,
                "all_inputs_readable": all(item["sha256"] is not None for item in inputs_start+inputs_end),
                "failure_reasons": reasons, "publications": publications},
        "outputs": [fingerprint(path) for path in output_paths],
        "checks": [{key: value for key, value in record.items() if key != "output"} for record in records],
        "result": ("Execution/provenance failure: inspect audit_output.txt before scientific interpretation."
                   if reasons else "All six bounded jobs reproduced with unchanged inputs. Scientific results, including null or negative findings, are in results.json and REPORT.md."),
        "residual_risks": ["Shared worktree is dirty; start/end SHA256 inventories define the actual sources.",
                           "The checks cover the recorded catalog, selection and kernels, not all MOND theories.",
                           "Temporary absolute job paths identify this run; rerun this runner to recreate fresh staging paths."]}
    (HERE/"computation_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"jobs": len(records), "execution_exit_status": 1 if reasons else 0,
                      "failure_reasons": reasons, "scientific_acceptance_inferred": False}, indent=2))
    return 1 if reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
