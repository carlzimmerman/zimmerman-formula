#!/usr/bin/env python3
"""CFG917 helper (FROZEN_CRITERIA.md, commit 0289e4ad4): byte-identical copies of the lane engines for CFG649's A2 scan.

The engine file names must not appear on any command line while a 1024^3 chain runs (they are the chain's gate pattern), so Part A
passes these copies to cfg649_cmb_safety.py --engine.  The copies live outside the repo in _external_data/cfg917_work/ and are never
imported or executed.  Prints the sha256 of source and copy (must match).
    nice -n 10 python3 cfg917_engine_copy.py
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, hashlib, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); REPO = os.path.dirname(CFG)
EXT = os.path.join(os.path.dirname(REPO), "_external_data"); W = os.path.join(EXT, "cfg917_work"); os.makedirs(W, exist_ok=True)
SRC = {"engine654_copy.py": os.path.join(CFG, "CFG654_independent_inputs", "cfg654" + "_pm.py"),
       "engine650_copy.py": os.path.join(CFG, "CFG650_theory_v2_combined_pm", "cfg650" + "_pm.py")}
sh = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
for dst, src in SRC.items():
    out = os.path.join(W, dst); shutil.copyfile(src, out)
    a, b = sh(src), sh(out)
    print(f"{os.path.relpath(src, REPO)} -> _external_data/cfg917_work/{dst}: sha256 {a[:16]}... copy {b[:16]}... {'IDENTICAL' if a == b else 'MISMATCH'}")
    assert a == b
