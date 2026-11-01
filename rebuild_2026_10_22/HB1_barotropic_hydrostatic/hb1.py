#!/usr/bin/env python3
"""HB1 (FROZEN_CRITERIA.md, AMENDMENTS.md): the hydrostatic solve in place of the shell map on NR3 MEDIAN's path. UR1, SL1, NF1, NR2, NR3, DR3 read only. python3 hb1.py PART [TAG]. Resumable between rows. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); DR3 = os.path.join(RB, "DR3_thin_disc_monopole")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); IN = dict(MEDIAN=(J["r10"], J["r11"]), LOW=(J["r10_68"][0], J["r11_68"][0]), HIGH=(J["r10_68"][1], J["r11_68"][1]))
PRE = re.search(r'pre = (""".*?""")', open(os.path.join(UR1, "ur1.py")).read(), re.S).group(1)
A_ = 'Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0));'; B_ = 'Mbk = DR3_MBK(q, iu, U, R_);'
GAS = """_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\' % (10 ** 0.005))\\n'
sub('NX = {"__file__": X30SRC,', _x + 'NX = {"__file__": X30SRC,')
"""
def go(part, tag="MEDIAN", extra=None, nsub=None, grid=None):
    r10, r11 = IN[tag]; O = os.path.join(HERE, f"hb1_{part}_results.json")
    if os.path.exists(O): return json.load(open(O))
    W = os.path.join(HERE, f"cache_{part}"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); h3 = open(os.path.join(DR3, "dr3_tail_add.py")).read(); t = t[:t.index("import time as _tm")] + "import time as _tm0\n" + h3[:h3.index("def _eff(")].replace("_T0 = _tm.time(); ", "") + "\nos.environ.setdefault('X', '')\n" + open(os.path.join(HERE, "hb1_tail_add.py")).read(); tl = os.path.join(W, "hb1_tail.py"); open(tl, "w").write(t)
    pre = eval(PRE) + (GAS if part == "G5" else ""); d = open(os.path.join(SL1, "sl1_harvest.py")).read(); rep = 'T = T.replace(A_, B_);'
    if grid: rep += f" T = T.replace('rg = np.geomspace(R_[0] * 0.05, R200, 300)', 'rg = np.geomspace(R_[0] * 0.05, R200, {grid})');"
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(pre) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, f"NR2_{tag}_cf_table.json"))), ('"T = T.replace(a, a + ADD + SL1ADD);"', '"T = T.replace(a, a + ADD + SL1ADD); assert T.count(A_) == 1; ' + rep + '"'), ('"SL1ADD": SL1ADD}', f'"SL1ADD": SL1ADD, "A_": {A_!r}, "B_": {B_!r}}}')): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "hb1_driver.py"); open(df, "w").write(d); log = os.path.join(HERE, f"hb1_{part}_run.log")
    env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1", DR3_PART="HB1", DR3_HERE=DR3, HB_PART=part, HB_HERE=HERE, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=DR3)
    if nsub: env["HB_NSUB"] = str(nsub)
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(log, "a"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit(f"NOT DECIDED: {part} wrote no result, see {log}")
    return json.load(open(O))
if __name__ == "__main__":
    p = sys.argv[1]
    go(p, "LOW" if p == "LOW" else "HIGH" if p == "HIGH" else "MEDIAN", nsub=4 if p == "K3" else None, grid=1200 if p == "GRID4" else None)
