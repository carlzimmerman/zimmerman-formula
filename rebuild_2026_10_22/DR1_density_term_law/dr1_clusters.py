#!/usr/bin/env python3
"""DR1 clusters (FROZEN_CRITERIA.md): law rows through NF1's grader via SL1's driver, read only; own cache. Resumes row by row after SIGTERM: rerun. kappa = 1/2 FITTED; not theory closed."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); TL = os.path.join(HERE, "dr1_tail.py")
ALL = [["R1", 0, "canonical", None], ["R1", 1, "canonical", None], ["R1", 3, "canonical", None], ["R2", 0, "canonical", None], ["R2", 1, "canonical", None], ["R3", 0, "canonical", None], ["R3", 1, "canonical", None], ["R3", 3, "canonical", None], ["R1", 0, "alt", None], ["R1", 1, "alt", None]]
PR = [["R1", 0, "canonical", None], ["R1", 1, "canonical", None]]
MU = [["R1", 1, "canonical", "zero"], ["R1", 1, "canonical", "three"]]
RUNS = {"g0_f034": (0.0, "0.034", PR, True), "g005_f034": (0.005, "0.034", ALL + MU, False), "g005_f0615": (0.005, "0.0615", ALL[:3] + ALL[5:8], False), "g111_f034": (0.111, "0.034", PR, False)}
GAS = "_x = '_g = \\'Mg500 = cl[\"Mgas500\"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl[\"Mgas500\"]*qd**2.5*%%r;\\' %% (10 ** %r))\\n'\nsub('NX = {\"__file__\": X30SRC,', _x + 'NX = {\"__file__\": X30SRC,')\n"
for tag in (sys.argv[1:] or RUNS):
    dex, fs, rows, k2 = RUNS[tag]; W = os.path.join(HERE, f"cache_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(HERE, f"dr1_{tag}.json")
    if os.path.exists(O) and json.load(open(O)).get("done"): continue
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(GAS % dex if dex else "") + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')):
        assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "dr1_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", DR1_RUN=json.dumps(dict(rows=rows, k2=k2)))
    p = subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, f"dr1_{tag}.log"), "w"), stderr=subprocess.STDOUT)
    print(tag, p.returncode, flush=True)
