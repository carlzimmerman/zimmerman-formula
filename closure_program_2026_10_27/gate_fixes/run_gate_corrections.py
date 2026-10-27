"""Bounded correction run. All writes are confined to a NEW requested output directory.

The mathbox runner creates that directory; this script refuses existing result files.
An audit hook rejects writes elsewhere and hashes project/catalogue inputs actually read.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", required=True)
args = parser.parse_args()
outdir = Path(args.output_dir).resolve()
allowed_parent = ROOT/"closure_program_2026_10_27/gate_fixes"
if not outdir.is_relative_to(allowed_parent) or outdir == allowed_parent:
    raise ValueError("Output must be a run subdirectory of gate_fixes")
if not outdir.is_dir():
    raise ValueError("Create output via the bounded provenance runner")
results = [outdir/n for n in ("x57_r4b_corrected.json", "x64_c6r_corrected.json", "provenance.json")]
if any(p.exists() for p in results):
    raise FileExistsError("Refusing to replace correction results")

observed = {}; hashing = False
external = ROOT.parent/"_external_data"


def digest(path):
    hh = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            hh.update(chunk)
    return hh.hexdigest()


def audit(event, args):
    global hashing
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        p = Path(os.fsdecode(args[0])).resolve()
        flags = args[2]
        writing = flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
        if writing and not p.is_relative_to(outdir):
            raise PermissionError(f"Correction run attempted a write outside output: {p}")
        if not writing and not hashing and not p.is_relative_to(outdir) and (
            p.is_relative_to(ROOT) or p.is_relative_to(external)) and "site-packages" not in p.parts and p.is_file():
            key = str(p)
            if key not in observed:
                hashing = True
                try: observed[key] = dict(sha256_before=digest(p), size_bytes=p.stat().st_size)
                finally: hashing = False
    if event in ("os.remove", "os.rmdir", "os.mkdir", "os.rename"):
        paths = args[:2] if event == "os.rename" else args[:1]
        for value in paths:
            if isinstance(value, (str, bytes, os.PathLike)) and not Path(os.fsdecode(value)).resolve().is_relative_to(outdir):
                raise PermissionError(f"Correction run attempted mutation outside output: {event} {value}")


sys.addaudithook(audit)
t0 = time.monotonic()


def load(rel, name):
    path = ROOT/rel
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


r4 = load("rebuild_2026_10_22/X57_exclusion_mechanism/x57_r4b_correction.py", "r4_correction")
c6 = load("rebuild_2026_10_22/X64_oblique_object_keys/x64_c6_correction.py", "c6_correction")
r = r4.calculate(ROOT/"rebuild_2026_10_22/X57_exclusion_mechanism/x57_exclusion_results.json")
with results[0].open("x") as fh: json.dump(r, fh, indent=2, allow_nan=False)
print("X57:", {f: v["verdicts"]["M6"]["verdict"] for f,v in r["footings"].items()}, flush=True)
c = c6.calculate(ROOT)
with results[1].open("x") as fh: json.dump(c, fh, indent=2, allow_nan=False)
print("X64:", c["verdict"], flush=True)
hashing = True
for p, record in observed.items():
    record["sha256_after"] = digest(p)
    record["unchanged"] = record["sha256_before"] == record["sha256_after"]
if not all(v["unchanged"] for v in observed.values()):
    raise RuntimeError("Observed input changed during calculation")
import numpy, scipy, astropy
provenance = dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__, astropy=astropy.__version__,
                  wall_seconds=time.monotonic()-t0, observed_inputs=observed,
                  peak_rss_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6),
                  filesystem_guard="All mutations outside this fresh output directory rejected by Python audit hook",
                  inputs_unchanged=True, execution_scope="X57 saved-result R4b regrade; X64 member rebuild before CLASS, C6R and frozen eight-key regrade")
with results[2].open("x") as fh: json.dump(provenance, fh, indent=2)
print("Observed unchanged inputs:", len(observed), "; seconds:", round(provenance["wall_seconds"], 2), "; RSS GB:", round(provenance["peak_rss_GB"], 3))
