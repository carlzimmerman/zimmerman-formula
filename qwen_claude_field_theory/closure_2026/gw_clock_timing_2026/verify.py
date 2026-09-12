#!/usr/bin/env python3
"""Run the bounded research checks and Lean leaves; never certify a theory.

Each compiler exit status and printed axiom set is checked. Prior logs are
preserved. No imports are built/downloaded and no existing result is rewritten.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    here = Path(__file__).resolve().parent
    front = root/"qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026"
    repair = front.parent
    lean_cwd = root/"qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026"
    output = args.output.resolve()
    if root not in output.parents:
        raise ValueError("result directory must be below repo root")
    output.mkdir(exist_ok=False)
    scripts = [here/"timing_audit.py",front/"boosted/derive_boosted.py",front/"boosted/test_boosted.py",
               front/"boosted/check_archived_jets.py",front/"boosted/tensor_cone.py",front/"boosted/clock_lapse.py",
               front/"health/audit_health.py",front/"health/pressure/audit_pressure.py",
               repair/"mond_braiding_completion/derive.py"]
    lean_files = [here/"TimingIdentities.lean",here/"ReviewedClaudeTime.lean",front/"boosted/ClockGeometry.lean",
                  front/"health/HealthSign.lean",front/"health/pressure/PressureIdentity.lean"]
    jobs = [(p.stem,[sys.executable,"-B",str(p)],root,p,False) for p in scripts]
    jobs += [(p.stem,["/opt/homebrew/bin/lake","env","lean",str(p)],lean_cwd,p,True) for p in lean_files]
    # Unique names even if another module is named derive.
    jobs = [(str(i)+"_"+name,argv,cwd,p,islean) for i,(name,argv,cwd,p,islean) in enumerate(jobs)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONOPTIMIZE="0",
               OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
    guards = []
    for label,source,expected_success in (
        ("assertions_enabled", "import sys; print(sys.flags.optimize); assert sys.flags.optimize == 0", True),
        ("false_assertion_rejected", "assert False, 'intentional verifier negative control'", False)):
        argv = [sys.executable,"-B","-c",source]
        guard = subprocess.run(argv,cwd=root,env=env,capture_output=True,text=True,timeout=10)
        ok = (guard.returncode==0) if expected_success else (guard.returncode!=0 and "AssertionError" in guard.stderr)
        guards.append(dict(name=label,argv=argv,exit_status=guard.returncode,
                           stdout=guard.stdout,stderr=guard.stderr,checked_ok=ok))
        if not ok:
            raise RuntimeError("assertion preflight failed: "+label)

    def run(job):
        name,argv,cwd,path,islean = job
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        start = time.monotonic()
        try:
            proc = subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True,timeout=90)
            code,stdout,stderr = proc.returncode,proc.stdout,proc.stderr
        except subprocess.TimeoutExpired as exc:
            code,stdout,stderr = 124,str(exc.stdout or ""),str(exc.stderr or "")
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        (output/(name+".stdout.txt")).write_text(stdout)
        (output/(name+".stderr.txt")).write_text(stderr)
        axioms = re.findall(r"depends on axioms: \[([^]]*)\]",stdout) if islean else []
        axiom_sets = [sorted(x.strip() for x in match.split(",") if x.strip()) for match in axioms]
        allowed = {"propext","Classical.choice","Quot.sound"}
        axiom_ok = (bool(axiom_sets) and all(set(x)<=allowed for x in axiom_sets)) if islean else None
        ok = code==0 and before==after and (not islean or axiom_ok)
        result = dict(name=name,argv=argv,cwd=str(cwd),exit_status=code,seconds=time.monotonic()-start,
                      source_sha256_before=before,source_sha256_after=after,checked_ok=ok,
                      axiom_sets=axiom_sets,axiom_check=axiom_ok)
        print(name,"exit",code,"verified",ok,flush=True)
        return result

    # Two workers bound resource use; compiler jobs do not rebuild dependencies.
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run,jobs))
    revision = subprocess.run(["git","rev-parse","HEAD"],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
    summary = {"scope":"bounded checks only, not whole-theory certification","head_at_completion":revision,
               "assertion_guards":guards,"child_PYTHONOPTIMIZE":"0",
               "worker_cap":2,"per_command_timeout_seconds":90,"results":results,
               "all_checks_passed":all(r["checked_ok"] for r in results)}
    (output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
