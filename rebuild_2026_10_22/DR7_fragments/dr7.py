#!/usr/bin/env python3
"""DR7 (FROZEN_CRITERIA.md): phase-space cap on UR1's response path, on NR2's eta. UR1, SL1, NF1, NR2, NR3 read only; own cache dirs. Checkpoints per row, so a kill resumes. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, signal, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); IN = dict(MEDIAN=(J["r10"], J["r11"], "MEDIAN"), LOW=(J["r10_68"][0], J["r11_68"][0], "LOW"), HIGH=(J["r10_68"][1], J["r11_68"][1], "HIGH"), MUTATE=(J["r10"], J["r11"], "MEDIAN"))
PRE = re.search(r'pre = (""".*?""")', open(os.path.join(UR1, "ur1.py")).read(), re.S).group(1); CUR = [None]
def term(*_):
    if CUR[0] is not None: CUR[0].terminate()
    sys.exit(143)
signal.signal(signal.SIGTERM, term)
def go(part):
    r10, r11, tag = IN[part]; O = os.path.join(HERE, f"dr7_{part}_results.json"); W = os.path.join(HERE, f"cache_{part}"); os.makedirs(W, exist_ok=True)
    t = open(os.path.join(UR1, "ur1_tail.py")).read(); i = t.index("import time as _tm"); tl = os.path.join(W, "dr7_tail.py"); open(tl, "w").write(t[:i] + open(os.path.join(HERE, "dr7_tail_add.py")).read())
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, f"NR2_{tag}_cf_table.json")))):
        assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "dr7_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1", DR7_PART=part, DR7_HERE=HERE)
    CUR[0] = subprocess.Popen(["nice", "-n", "15", sys.executable, "-W", "ignore", df], env=env, stdout=open(os.path.join(HERE, f"dr7_{part}_run.log"), "a"), stderr=subprocess.STDOUT); rc = CUR[0].wait(); print(part, "rc", rc, flush=True); return rc
for part in sys.argv[1:] or ("MEDIAN", "LOW", "HIGH", "MUTATE"):
    if go(part) != 0: raise SystemExit(f"NOT DECIDED: {part}, see dr7_{part}_run.log")
