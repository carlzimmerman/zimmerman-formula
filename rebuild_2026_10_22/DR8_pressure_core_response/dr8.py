#!/usr/bin/env python3
"""DR8 part A (FROZEN_CRITERIA.md): the outside text's pressure-term contraction rule on NR3 MEDIAN's path, through UR1's tail. UR1, SL1, NF1, NR2, NR3 read only. The rule is posited, not derived. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); IN = dict(MEDIAN=(J["r10"], J["r11"]), LOW=(J["r10_68"][0], J["r11_68"][0]), HIGH=(J["r10_68"][1], J["r11_68"][1]))
U1 = open(os.path.join(UR1, "ur1.py")).read(); PRE = re.search(r'pre = (""".*?""")', U1, re.S).group(1)
def go(part, tag="MEDIAN", extra=None):
    r10, r11 = IN[tag]; O = os.path.join(HERE, f"dr8_{part}_results.json")
    if os.path.exists(O): return json.load(open(O))
    W = os.path.join(HERE, f"cache_{part}"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); t = t[:t.index("import time as _tm")] + open(os.path.join(HERE, "dr8_tail_add.py")).read(); tl = os.path.join(W, "dr8_tail.py"); open(tl, "w").write(t)
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, f"NR2_{tag}_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "dr8_driver.py"); open(df, "w").write(d); log = os.path.join(HERE, f"dr8_{part}_run.log"); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", UR1_DRIVER="1", DR8_PART=part, DR8_HERE=HERE, PYTHONDONTWRITEBYTECODE="1", **(extra or {}))
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(log, "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit(f"NOT DECIDED: {part} wrote no result, see {log}")
    return json.load(open(O))
if __name__ == "__main__": go(sys.argv[1] if len(sys.argv) > 1 else "PRIMARY", sys.argv[2] if len(sys.argv) > 2 else "MEDIAN")
