#!/usr/bin/env python3
"""Recheck the named Lean kernels; numerical/literature claims are not certified.

Run from any directory. With --library-project, use already-built dependencies
from that project's .lake/packages, checking its toolchain and lake manifest.
Otherwise use this repository's lake env lean. No downloads are performed here.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROJECT = ROOT / "fable_independent_2026/lean_2026"
NAMES = ["QX1_closure_chain", "QX17B_field_equations", "FRW_correction",
         "SE1_shock_entropy", "SV1_shell_bound", "SV2_causality", "SV2_repair",
         "SV5_growth_nogo", "EW2_aest_window"]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--library-project", type=Path)
    args = ap.parse_args()
    env = os.environ.copy()
    command = ["lake", "env", "lean"]
    if args.library_project:
        lib = args.library_project.resolve()
        for name in ["lean-toolchain", "lake-manifest.json"]:
            if sha(lib / name) != sha(PROJECT / name):
                raise SystemExit(f"Dependency mismatch: {name}")
        paths = sorted((lib / ".lake/packages").glob("*/.lake/build/lib/lean"))
        if not any((p / "Mathlib.olean").is_file() for p in paths):
            raise SystemExit("No built Mathlib in --library-project")
        env["LEAN_PATH"] = os.pathsep.join(map(str, paths))
        command = ["lean"]
    outdir = HERE / "logs"
    outdir.mkdir(exist_ok=True)
    results = []
    sources = [(PROJECT / (n + ".lean"), False) for n in NAMES]
    sources += [(PROJECT / (n + "_MUTATE.lean"), True) for n in NAMES]
    sources += [(HERE / "ClosureLatest.lean", False)]
    for source, mutation in sources:
        text = source.read_text()
        # Comments are not trusted as evidence; inspect compiler-reported axioms.
        declarations = re.findall(r"^theorem\s+(\S+)", text, re.M)
        run = subprocess.run(command + [str(source)], cwd=PROJECT, env=env,
                             capture_output=True, text=True, timeout=300)
        log = run.stdout + run.stderr
        # Keep committed logs portable across checkouts.
        log = log.replace(str(ROOT) + "/", "")
        log = "\n".join(line.rstrip() for line in log.splitlines()) + "\n"
        logpath = outdir / (source.stem + ".out")
        logpath.write_text(log)
        reports = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log)
        empty = re.findall(r"'([^']+)' does not depend on any axioms", log)
        axioms = {n: [a.strip() for a in aa.split(",") if a.strip()] for n, aa in reports}
        axioms.update({n: [] for n in empty})
        if mutation:
            passed = run.returncode != 0 and bool(re.search(r":\d+:\d+: error:", log))
            label = "compiler_rejected"  # not a proof of the negated statement
        else:
            passed = (run.returncode == 0 and len(axioms) == len(declarations)
                      and all(set(aa) <= ALLOWED for aa in axioms.values())
                      and not re.search(r"\b(sorry|admit|axiom)\b", re.sub(r"/-.*?-/|--[^\n]*", "", text, flags=re.S)))
            label = "kernel_checked_standard_axioms"
        results.append({"source": str(source.relative_to(ROOT)), "sha256": sha(source),
                        "mutation": mutation, "exit_code": run.returncode,
                        "declared_theorems": len(declarations), "axioms": axioms,
                        "status": label if passed else "FAILED", "passed": passed,
                        "log": str(logpath.relative_to(ROOT)), "log_sha256": sha(logpath)})
        print(source.stem, results[-1]["status"], flush=True)
    version = subprocess.check_output(command + ["--version"], cwd=PROJECT, env=env, text=True).strip()
    payload = {"review": "self-review; conditional algebraic certification only",
               "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "lean_version": version, "toolchain": (PROJECT / "lean-toolchain").read_text().strip(),
               "lake_manifest_sha256": sha(PROJECT / "lake-manifest.json"),
               "certified_theorems": sum(r["declared_theorems"] for r in results if not r["mutation"] and r["passed"]),
               "all_passed": all(r["passed"] for r in results), "results": results}
    (HERE / "verification.json").write_text(json.dumps(payload, indent=2) + "\n")
    raise SystemExit(0 if payload["all_passed"] else 1)


if __name__ == "__main__":
    main()
