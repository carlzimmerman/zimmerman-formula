#!/usr/bin/env python3
"""SP3 hand core (FROZEN_CRITERIA.md): RET1's driving of UR1's tail on SL1's driver, NR2 medians, read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); RES = os.path.join(HERE, "sp3_hand_results.json")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); r10, r11 = J["r10"], J["r11"]
W = os.path.join(HERE, "cache_hand"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); t = t[:t.index("import time as _tm")] + open(os.path.join(HERE, "sp3_hand_tail.py")).read(); tl = os.path.join(W, "sp3_tail.py"); open(tl, "w").write(t)
U1 = open(os.path.join(UR1, "ur1.py")).read(); PRE = eval(re.search(r'pre = (""".*?""")', U1, re.S).group(1)); a = "\\n    M = SLMAP['mut']"; assert PRE.count(a) == 1
PRE = PRE.replace(a, "\\n    if SLMAP['m'] == 'RET': M = SLMAP['f'](lMb, bg, rc); return M, (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)" + a)
d = open(os.path.join(SL1, "sl1_harvest.py")).read()
for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(PRE) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, "NR2_MEDIAN_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
df = os.path.join(W, "sp3_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=RES, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1", SP3_TABLES=os.path.join(HERE, "sp3_tables.json"))
sys.exit(subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, "sp3_hand_run.log"), "w"), stderr=subprocess.STDOUT).returncode)
