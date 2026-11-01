#!/usr/bin/env python3
"""SL1: drive NF1's grader at NR1 PRIMARY's inputs, read only, with a tail. mode harvest: cache/sl1_cache.pkl. mode exact: regrade trees through dvecN.
    python3 sl1_harvest.py [tail.py]
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = '/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/FG1_final_grade'; RB = '/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22'; NF = os.path.join(RB, "NF1_no_floor_rule"); WD = '/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/FG1_final_grade/cache_fg1law_MUTATE'; os.makedirs(WD, exist_ok=True); NRD = os.path.join(RB, "NR1_native_n_ng80")
TAIL = '/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/FG1_final_grade/cache_fg1law_MUTATE/fg1law_MUTATE_tail.py'; sys.argv = [sys.argv[0]]
E = 21.53
os.environ.update(CN1_R="1.0", CN1_MODE="off", NF1_ON="1", NF1_TAB=json.dumps([math.log10(1.2414241604983889), math.log10(1.1474704316494144), 0.0]), X74_CF='/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/NR2_low_mass_ng80/NR2_MEDIAN_cf_table.json', X73_FSTAR="0.034", X73_SLOPE="2.7774425603108597", XH1_OUT=os.path.join(WD, "xh1_unused.json"), XH1_SMULT="1", PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
os.environ.setdefault("SL1_OUT", os.path.join(WD, "sl1_cache.pkl")); os.environ.pop("XH1_K0_REF", None)
t = open(os.path.join(RB, "XH1_xcop_native_rule", "xh1_tail.py")).read(); e = '_OUT["rss_gb"] = rss(); json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)\nsys.exit(0)'; assert t.count(e) == 1
i = t.index("_OUT = dict(fstar=FSTAR"); t = t[:i] + open(TAIL).read(); tf = os.path.join(WD, "tail_joined.py"); open(tf, "w").write(t)
N = open(os.path.join(NF, "nf1_x74.py")).read(); k = "T = T.replace(a, a + ADD);"; assert N.count(k) == 1
N = N.replace(k, "T = T.replace(a, a + ADD + SL1ADD);")
SL1ADD = 'sub(\'ETA_USE = {\\\'v\\\': ETA}\\n\', "ETA_USE = {\'v\': ETA}\\nSLDL = [0.0]\\nSLMAP = dict(m=\'EM1\', mut=1.0)\\ndef _SL3M(lMb, bg, rc):\\n    if SLMAP[\'m\'] == \'EM1\': M = 10 ** (bg[\'a\'] + bg[\'b\'] * (lMb - 10) + SLDL[0]); return M, (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)\\n    M = SLMAP[\'mut\'] * NAT_RRAT * 10 ** lMb\\n    if SLMAP[\'m\'] == \'FAIR200\': return M, (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)\\n    return M, NX[\'r_ta_com\'](10 ** lMb * MSUNE)\\n")\nsub(\'lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM; R200 = (3 * M200 * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)\', \'M200, R200 = _SL3M(q["lMb"], bg, rc)\')\n' + f"sub('sys.exit(0 if (n == len(checks) and x74ok) else 1)', open({tf!r}).read())\n"
os.chdir(WD); exec(compile(N, os.path.join(HERE, "nf1_x74_sl1"), "exec"), {"__file__": '/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/FG1_final_grade/nf1_x74_sl1.py', "__name__": "__main__", "SL1ADD": SL1ADD})
