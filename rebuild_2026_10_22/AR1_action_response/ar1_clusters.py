#!/usr/bin/env python3
"""AR1 clusters, groups, X-COP, LT (FROZEN_CRITERIA.md): NF1's grader on NR3 MEDIAN's path, S-core rule N, contract replaced by the action solver. UR1, SL1, NF1, NR2, NR3 read only.
    ar1_clusters.py erass | gs5   (gs5 = gas +0.005, the ZN1 patch on Mgas500). kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); r10, r11 = J["r10"], J["r11"]
U1 = open(os.path.join(UR1, "ur1.py")).read(); PRE = re.search(r'pre = (""".*?""")', U1, re.S).group(1)
GAS = open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_grade.py")).read(); GAS = eval(re.search(r'^GAS = (""".*?""")', GAS, re.S | re.M).group(1)).replace("0.111", "0.005")
def go(part):
    O = os.path.join(HERE, f"ar1_clusters_{part}.json")
    if os.path.exists(O): return
    W = os.path.join(HERE, f"cache_cl_{part}"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); t = t[:t.index("import time as _tm")] + open(os.path.join(HERE, "ar1_tail_add.py")).read(); tl = os.path.join(W, "ar1_tail.py"); open(tl, "w").write(t)
    d = open(os.path.join(SL1, "sl1_harvest.py")).read(); pre = eval(PRE) + (GAS if part == "gs5" else "")
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(pre) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, "NR2_MEDIAN_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "ar1_driver.py"); open(df, "w").write(d); log = os.path.join(HERE, f"ar1_clusters_{part}_run.log"); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1", AR1_PART=part, AR1_HERE=HERE, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.Popen(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(log, "a"), stderr=subprocess.STDOUT)
    import signal; signal.signal(signal.SIGTERM, lambda *a: (p.terminate(), sys.exit(75))); p.wait()
    if not os.path.exists(O): raise SystemExit(f"NOT DECIDED: {part} wrote no result, see {log}")
if __name__ == "__main__": go(sys.argv[1])
