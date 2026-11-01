#!/usr/bin/env python3
"""DR3 (FROZEN_CRITERIA.md ca7006d189): true thin-disc monopole in SPARC's contraction, GB kept as force, on NR3 MEDIAN's path. UR1, SL1, NF1, NR2, NR3, CN1, LC1 read only. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); TG = ("A_c2b_refit", "B_cfg886_bg")
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); r10, r11 = J["r10"], J["r11"]
U1 = open(os.path.join(UR1, "ur1.py")).read(); PRE = re.search(r'pre = (""".*?""")', U1, re.S).group(1); tag = "MEDIAN"
DR3_A = 'Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0));'; DR3_B = 'Mbk = DR3_MBK(q, iu, U, R_);'
def go(part):
    O = os.path.join(HERE, f"dr3_{part}_results.json")
    if os.path.exists(O): return json.load(open(O))
    W = os.path.join(HERE, f"cache_{part}"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); t = t[:t.index("import time as _tm")] + open(os.path.join(HERE, "dr3_tail_add.py")).read(); tl = os.path.join(W, "dr3_tail.py"); open(tl, "w").write(t)
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, f"NR2_{tag}_cf_table.json"))), ('"T = T.replace(a, a + ADD + SL1ADD);"', '"T = T.replace(a, a + ADD + SL1ADD); assert T.count(DR3_A) == 1; T = T.replace(DR3_A, DR3_B);"'), ('"SL1ADD": SL1ADD}', f'"SL1ADD": SL1ADD, "DR3_A": {DR3_A!r}, "DR3_B": {DR3_B!r}}}')): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "dr3_driver.py"); open(df, "w").write(d); log = os.path.join(HERE, f"dr3_{part}_run.log"); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1", DR3_PART=part, DR3_HERE=HERE)
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(log, "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit(f"NOT DECIDED: {part} wrote no result, see {log}")
    return json.load(open(O))
if __name__ == "__main__": go(sys.argv[1] if len(sys.argv) > 1 else "PRIMARY")
