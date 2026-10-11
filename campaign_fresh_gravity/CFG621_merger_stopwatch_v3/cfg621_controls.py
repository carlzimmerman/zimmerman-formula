#!/usr/bin/env python3
"""CFG621 controls C1-C3, C4(a), C5, C6 (FROZEN_CRITERIA_B.md): CFG599's control script (../CFG599_merger_stopwatch_v2/
cfg599_controls.py) executed read-only in memory with its simulator swapped for cfg621_sim (the stage-A estimator E-1) and its
own file writers removed.  Only C4(a) depends on the estimator; C1-C3, C5, C6 re-run unchanged code.
Run: nice -n 10 python3 cfg621_controls.py  -> cfg621_controls.out, cfg621_controls_results.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg621_sim  # noqa: F401,E402
F599 = os.path.join(HERE, "..", "CFG599_merger_stopwatch_v2", "cfg599_controls.py")
src = open(F599).read()
a = "import cfg599_sim as S"
assert src.count(a) == 1
src = src.replace(a, "import cfg621_sim as S")
cut = src.index('open(os.path.join(HERE, "cfg599_controls.out")')
src = src[:cut]
ns = {"__name__": "cfg599_controls_in_cfg621", "__file__": F599}
exec(compile(src, "cfg599_controls.py[cfg621 estimator]", "exec"), ns)
RES, OUT = ns["RES"], ns["OUT"]
OUT.insert(0, "CFG621 controls: CFG599's control code (read-only) with the stage-A estimator E-1 (R_min 75 kpc).")
open(os.path.join(HERE, "cfg621_controls.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg621_controls_results.json"), "w"), indent=1)
sys.exit(0 if RES["all_pass"] else 1)
