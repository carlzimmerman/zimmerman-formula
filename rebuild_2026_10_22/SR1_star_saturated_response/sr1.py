#!/usr/bin/env python3
"""SR1 (FROZEN_CRITERIA.md): three gates on UR1's path, read only. Writes sr1_results.json; sr1_read.py grades it. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); UR1 = os.path.join(RB, "UR1_one_response_rule"); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); W = os.path.join(HERE, "cache"); os.makedirs(W, exist_ok=True); O = os.path.join(HERE, "sr1_results.json")
d = subprocess.run(["git", "show", "770ed58e5a:rebuild_2026_10_22/UR1_one_response_rule/ur1_driver.py"], capture_output=True, text=True, cwd=RB, check=True).stdout
a = "(lMb - 10)); return M"; assert a in d; d = d.replace(a, "(lMb - 10) + SLDL[0]); return M"); b = "SLMAP = dict("; assert b in d; d = d.replace(b, "SLDL = [0.0]\\\\n" + b)
import re
d = re.sub(r"HERE = '[^']*'; RB = '[^']*';", f"HERE = {HERE!r}; RB = {RB!r};", d, 1); d = re.sub(r"WD = '[^']*'", f"WD = {W!r}", d, 1); d = re.sub(r"sys\.argv\[1\] if len\(sys\.argv\) > 1 else '[^']*'", repr(os.path.join(W, "sr1_tail.py")), d, 1); d = re.sub(r'"__file__": \'[^\']*\'', '"__file__": ' + repr(os.path.join(HERE, "nf1_x74_sl1.py")), d, 1)
t = open(os.path.join(UR1, "ur1_tail.py")).read(); i = t.index("import time as _tm"); open(os.path.join(W, "sr1_tail.py"), "w").write(t[:i] + open(os.path.join(HERE, "sr1_tail_add.py")).read())
df = os.path.join(W, "sr1_driver.py"); open(df, "w").write(d)
sys.exit(subprocess.run(["nice", "-n", "15", sys.executable, df], env=dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1"), stdout=open(os.path.join(HERE, "sr1_run.log"), "w"), stderr=subprocess.STDOUT).returncode)
