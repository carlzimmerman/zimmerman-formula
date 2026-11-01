#!/usr/bin/env python3
"""CP1 (FROZEN_CRITERIA.md): smooth per-object mix of the a0 law and N's halo; UR1's helpers, SL1's driver, NR2's eta, read only. V_crit 250, n 4 CHOSEN. Breaks the owner's 10-31 no-a0-in-cold-sector rule on purpose. kappa = 1/2 FITTED; not theory closed."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); IN = dict(MEDIAN=(J["r10"], J["r11"]), LOW=(J["r10_68"][0], J["r11_68"][0]), HIGH=(J["r10_68"][1], J["r11_68"][1]))
PRE = re.search(r'pre = (""".*?""")', open(os.path.join(UR1, "ur1.py")).read(), re.S).group(1)
def go(name, tag, mode):
    O = os.path.join(HERE, f"cp1_{name}_results.json")
    if os.path.exists(O): return
    r10, r11 = IN[tag]; W = os.path.join(HERE, f"cache_{name}"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); c = '_K = _run("EM1", "off")'; assert t.count(c) == 1; i = t.index("import time as _tm"); assert i < t.index(c)
    tl = os.path.join(W, "cp1_tail_joined.py"); open(tl, "w").write(t[:i] + "import time as _tm\n_T0 = _tm.time()\n" + open(os.path.join(HERE, "cp1_tail.py")).read())
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, f"NR2_{tag}_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "cp1_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1", CP1_MODE=mode)
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, f"cp1_{name}_run.log"), "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit(f"NOT DECIDED: {name} wrote no result, see its log")
for a in sys.argv[1:] or ["MEDIAN", "LOW", "HIGH", "MUTATE"]:
    go(a, dict(K4="MEDIAN", MUTATE="MEDIAN", R2MED="MEDIAN", R2LOW="LOW", R2HIGH="HIGH").get(a, a), dict(K4="k4", MEDIAN="full", LOW="band", HIGH="band", MUTATE="mutate", R2MED="r2full", R2LOW="r2band", R2HIGH="r2band")[a])
