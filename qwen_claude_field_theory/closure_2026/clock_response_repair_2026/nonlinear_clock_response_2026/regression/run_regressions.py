#!/usr/bin/env python3
"""Run the named existing regressions, with at most four concurrent jobs.

The parent computation-audit runner supplies wall/CPU/log/thread limits and
immutable input provenance. Child Python audits additionally inventory actual
project reads and reject project writes outside this new run directory.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import time
import unittest

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
ROOT=BASE.parents[2]
LEAN=BASE.parent/"clock_constitutive_construction_2026/lean_formalization_2026"
SUITES=[
    ("cosmological_bridge", "cosmological_bridge_2026", 35),
    ("variance_geometry", "variance_closure_2026/geometry", 8),
    ("charge_constraints", "inhomogeneous_charge_2026/constraints", 5),
    ("metric_cubic", "finite_gradient_metric_2026/cubic", 6),
    ("variance_evolution", "variance_closure_2026/evolution", 4),
    ("variance_vertices", "variance_closure_2026/vertices", 5),
    ("charge_exterior", "inhomogeneous_charge_2026/exterior", 5),
    ("charge_current", "inhomogeneous_charge_2026/current", 9),
    ("charge_tracking", "inhomogeneous_charge_2026/tracking", 5),
    ("metric_root_only", "finite_gradient_metric_2026", 4),
    ("finite_gradient_background", "finite_gradient_background_2026", 6),
]
SCRIPT_CHECKS=[
    ("mond_derivation", "mond_braiding_completion/derive.py", "mond_derivation.json"),
    ("prior_ellipticity", "dirac_operator/ellipticity.py", "prior_ellipticity.json"),
    ("prior_lapse", "dirac_operator/lapse_source.py", "prior_lapse.json"),
]


def relative(path):
    return str(Path(path).resolve().relative_to(ROOT))


def child(args):
    output=args.output.resolve()
    output_root=output.parent
    contract=json.loads((HERE/"contract.json").read_text())
    allowed=set(contract["execution_artifacts"])
    observed=set()
    unpinned=set()
    root_prefix=str(ROOT)+os.sep
    output_prefix=str(output_root)+os.sep
    def audit(event, values):
        if event!="open" or not isinstance(values[0],(str,bytes,os.PathLike)):
            return
        raw=os.fsdecode(values[0])
        absolute=os.path.abspath(raw)
        if not absolute.startswith(root_prefix):
            return
        mode,flags=values[1],values[2]
        writing=(isinstance(mode,str) and any(c in mode for c in "wax+")) or (
            isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)))
        if writing:
            if not absolute.startswith(output_prefix):
                raise PermissionError("Regression may not write old project files: "+absolute)
            return
        if absolute.startswith(output_prefix):
            return
        # Python may read existing bytecode even with -B; pin its source.
        if absolute.endswith(".pyc"):
            try:
                absolute=importlib.util.source_from_cache(absolute)
            except ValueError:
                absolute=absolute[:-1]
        rel=os.path.relpath(absolute,str(ROOT))
        observed.add(rel)
        if rel not in allowed:
            unpinned.add(rel)
    sys.addaudithook(audit)
    started=time.perf_counter()
    status=0
    details={}
    if args.suite:
        directory=BASE/args.suite
        sys.path.insert(0,str(directory))
        tests=unittest.TestSuite()
        names=[p.stem for p in sorted(directory.glob("test*.py"))]
        for name in names:
            tests.addTests(unittest.defaultTestLoader.loadTestsFromName(name))
        result=unittest.TextTestRunner(verbosity=2).run(tests)
        status=int(not result.wasSuccessful())
        details=dict(tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),
                     skipped=len(result.skipped),test_modules=names,
                     failure_details=[dict(test=str(t),traceback=s) for t,s in result.failures+result.errors])
    else:
        source=BASE/args.script
        sys.path.insert(0,str(source.parent))
        sys.argv=[str(source),"--result-file",str(output_root/args.script_result)]
        try:
            runpy.run_path(str(source),run_name="__main__")
        except SystemExit as exc:
            status=int(exc.code or 0)
    if unpinned:
        status=2 if status==0 else status
    payload=dict(command_argv=[sys.executable,*args.original_argv],cwd=str(ROOT),
        exit_status=status,runtime_seconds=time.perf_counter()-started,
        observed_project_inputs=sorted(observed),unpinned_project_inputs=sorted(unpinned),
        all_observed_project_inputs_pinned=not unpinned,**details)
    output.write_text(json.dumps(payload,indent=2)+"\n")
    return status


def parent(args):
    out=args.output.resolve().parent
    out.mkdir(parents=True,exist_ok=True)
    common=[sys.executable,"-B",str(HERE/"run_regressions.py"),"--child"]
    jobs=[]
    for name,directory,count in SUITES:
        jobs.append(dict(name=name,kind="unit_tests",expected_tests=count,cwd=ROOT,
            argv=common+["--suite",directory,"--output",str(out/(name+".json"))]))
    for name,script,result_file in SCRIPT_CHECKS:
        jobs.append(dict(name=name,kind="existing_script",cwd=ROOT,
            argv=common+["--script",script,"--script-result",result_file,
                         "--output",str(out/(name+"_execution.json"))]))
    jobs.append(dict(name="mond_lean",kind="existing_lean",cwd=LEAN,
        argv=["/opt/homebrew/bin/lake","env","lean","-j1",str(BASE/"mond_braiding_completion/CubicRelations.lean")]))
    def execute(job):
        started=time.perf_counter()
        try:
            run=subprocess.run(job["argv"],cwd=job["cwd"],capture_output=True,text=True,timeout=150)
            record=dict(name=job["name"],kind=job["kind"],argv=job["argv"],cwd=str(job["cwd"]),
                exit_status=run.returncode,timeout=False,runtime_seconds=time.perf_counter()-started,
                stdout=run.stdout,stderr=run.stderr)
        except subprocess.TimeoutExpired as exc:
            record=dict(name=job["name"],kind=job["kind"],argv=job["argv"],cwd=str(job["cwd"]),
                exit_status=None,timeout=True,runtime_seconds=time.perf_counter()-started,
                stdout=exc.stdout.decode() if isinstance(exc.stdout,bytes) else exc.stdout or "",
                stderr=exc.stderr.decode() if isinstance(exc.stderr,bytes) else exc.stderr or "")
        if job["kind"]=="unit_tests":
            p=out/(job["name"]+".json")
            if p.exists():
                record["test_result"]=json.loads(p.read_text())
                record["expected_test_count"]=job["expected_tests"]
                record["test_count_matches"]=record["test_result"]["tests_run"]==job["expected_tests"]
        return record
    rows=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures=[pool.submit(execute,job) for job in jobs]
        for future in as_completed(futures):
            row=future.result();rows.append(row)
            print(json.dumps(dict(name=row["name"],exit_status=row["exit_status"],
                timeout=row["timeout"],runtime_seconds=row["runtime_seconds"])),flush=True)
    order={job["name"]:i for i,job in enumerate(jobs)}
    rows.sort(key=lambda row:order[row["name"]])
    tests=[row for row in rows if row["kind"]=="unit_tests"]
    total=sum(row.get("test_result",{}).get("tests_run",0) for row in tests)
    success=all(row["exit_status"]==0 and not row["timeout"] for row in rows)
    success=success and total==92 and all(row.get("test_count_matches",False) for row in tests)
    result=dict(scope="Existing regression tests and four existing MOND completion checks only; not new physical evidence or full theory closure.",
        expected_unit_tests=92,actual_unit_tests=total,unit_test_suites=len(tests),
        other_checks=4,max_concurrent_jobs=4,cooperative_numerical_threads_per_job=1,
        per_job_timeout_seconds=150,all_successful=success,cases=rows)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    return int(not success)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--child",action="store_true")
    p.add_argument("--suite")
    p.add_argument("--script")
    p.add_argument("--script-result")
    a=p.parse_args();a.original_argv=sys.argv.copy()
    raise SystemExit(child(a) if a.child else parent(a))
