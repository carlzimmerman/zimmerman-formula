#!/usr/bin/env python3
"""UR3: S(M200) from NF1's grader at NR1 PRIMARY, through UR1's driver, read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); UR1 = os.path.join(RB, "UR1_one_response_rule"); W = os.path.join(HERE, "cache"); os.makedirs(W, exist_ok=True)
d = subprocess.run(["git", "show", "770ed58e5a:rebuild_2026_10_22/UR1_one_response_rule/ur1_driver.py"], capture_output=True, text=True, cwd=RB, check=True).stdout
d = re.sub(r"HERE = '[^']*'; RB = '[^']*';", f"HERE = {HERE!r}; RB = {RB!r};", d, count=1); d = re.sub(r"WD = '[^']*'", f"WD = {W!r}", d, count=1); d = re.sub(r"sys\.argv\[1\] if len\(sys\.argv\) > 1 else '[^']*'", repr(os.path.join(W, "t.py")), d, count=1); d = re.sub(r'"__file__": \'[^\']*\'', '"__file__": ' + repr(os.path.join(HERE, "nf1_x74_sl1.py")), d, count=1)
t = open(os.path.join(UR1, "ur1_tail.py")).read(); i = t.index("import time as _tm"); open(os.path.join(W, "t.py"), "w").write(t[:i] + open(os.path.join(HERE, "ur3_table_tail.py")).read())
df = os.path.join(W, "d.py"); open(df, "w").write(d)
sys.exit(subprocess.run(["nice", "-n", "15", sys.executable, df], env=dict(os.environ, UR1_SL1=os.path.join(RB, "SL1_symbolic_law_search"), SL1_OUT=os.path.join(HERE, "ur3_S_table.json"), CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1"), stdout=open(os.path.join(HERE, "ur3_table.log"), "w"), stderr=subprocess.STDOUT).returncode)
