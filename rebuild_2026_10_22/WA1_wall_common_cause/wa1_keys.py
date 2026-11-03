#!/usr/bin/env python3
"""WA1 keys: LW1's real path via RQ3's patches, extra nodes for tilt and carry; BK2's row gets RQ3's three cells too. Resumes. One thread, nice 19. python3 wa1_keys.py [cid ...]. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
from wa1_common import *
A = load_acc(); L, T = A.keys_tail()
WD = os.path.join(HERE, "cache_k2"); os.makedirs(WD, exist_ok=True)
SLOPE0 = 'X73_SLOPE="2.7774425603108597"'
def gas_block(dex, tl):
    ex = f'10**({dex!r}+({tl!r})*(__import__("wa1_m500").lg(cl["name"])-14.3))'
    return "_x = '_g = \\'Mg500 = cl[\"Mgas500\"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl[\"Mgas500\"]*qd**2.5*" + ex + ";\\')\\n'\nsub('NX = {\"__file__\": X30SRC,', _x + 'NX = {\"__file__\": X30SRC,')\n"
TAGS = dict(tiltm1=(.005, "0.034", -0.20, None), tilt0=(.005, "0.034", -0.10, None), carrylo=(.005, "0.034", 0.0, NUIS["carry"][0] - NUIS["carry"][1]), carryhi=(.005, "0.034", 0.0, NUIS["carry"][0] + NUIS["carry"][1]), checkbase=(.005, "0.034", 0.0, None))
BK = dict(g005_f034=(.005, "0.034", None, None), g005_f0615=(.005, "0.0615", None, None), g0_f034=(0.0, "0.034", None, None))
def run(cid, tag, dex, fs, tl, slope):
    W = os.path.join(WD, f"{cid}_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(W, "keys.json")
    if os.path.exists(O) and json.load(open(O)).get("done"): return True
    TL = os.path.join(W, "tail.py"); open(TL, "w").write(T); d = open(os.path.join(L.SL1, "sl1_harvest.py")).read()
    add = gas_block(dex, tl) if tl is not None else (L.GAS % dex if dex else "")
    pairs = [('SL1ADD = f"sub(', 'SL1ADD = ' + repr(add) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')]
    if slope is not None: pairs.append((SLOPE0, f'X73_SLOPE="{slope!r}"'))
    for a, b in pairs:
        assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "driver.py"); open(df, "w").write(d); env = dict(os.environ, PYTHONPATH=HERE, UR1_SL1=L.SL1, SL1_OUT=O, CN1_FORCE="1", LW1_A0X="1.0", RQ2_CAND=os.path.abspath(CANDS[cid]), DR1_RUN=json.dumps(dict(rows=L.ROWS, k2=False)))
    p = subprocess.run(["nice", "-n", "19", sys.executable, df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT); ok = os.path.exists(O) and json.load(open(O)).get("done"); print(cid, tag, p.returncode, ok, flush=True); return ok
for cid in (sys.argv[1:] or REAL):
    if cid == "BK2":
        for t, v in BK.items(): run(cid, t, *v)
    for t, v in TAGS.items():
        if t == "checkbase" and cid != "LAW": continue
        run(cid, t, *v)
print("done", flush=True)
