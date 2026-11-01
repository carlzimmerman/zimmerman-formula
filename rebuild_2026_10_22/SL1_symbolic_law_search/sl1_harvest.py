#!/usr/bin/env python3
"""SL1: drive NF1's grader at NR1 PRIMARY's inputs, read only, with a tail. mode harvest: cache/sl1_cache.pkl. mode exact: regrade trees through dvecN.
    python3 sl1_harvest.py [tail.py]
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); NF = os.path.join(RB, "NF1_no_floor_rule"); WD = os.path.join(HERE, "cache"); os.makedirs(WD, exist_ok=True); NRD = os.path.join(RB, "NR1_native_n_ng80")
TAIL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sl1_tail_harvest.py"); sys.argv = [sys.argv[0]]
E = 21.53
os.environ.update(CN1_R="1.0", CN1_MODE="off", NF1_ON="1", NF1_TAB=json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0]), X74_CF=os.path.join(NRD, "NR1_PRIMARY_cf_table.json"), X73_FSTAR="0.034", X73_SLOPE="2.7774425603108597", XH1_OUT=os.path.join(WD, "xh1_unused.json"), XH1_SMULT="1", PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
os.environ.setdefault("SL1_OUT", os.path.join(WD, "sl1_cache.pkl")); os.environ.pop("XH1_K0_REF", None)
t = open(os.path.join(RB, "XH1_xcop_native_rule", "xh1_tail.py")).read(); e = '_OUT["rss_gb"] = rss(); json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)\nsys.exit(0)'; assert t.count(e) == 1
i = t.index("_OUT = dict(fstar=FSTAR"); t = t[:i] + open(TAIL).read(); tf = os.path.join(WD, "tail_joined.py"); open(tf, "w").write(t)
N = open(os.path.join(NF, "nf1_x74.py")).read(); k = "T = T.replace(a, a + ADD);"; assert N.count(k) == 1
N = N.replace(k, "T = T.replace(a, a + ADD + SL1ADD);")
SL1ADD = f"sub('sys.exit(0 if (n == len(checks) and x74ok) else 1)', open({tf!r}).read())\n"
os.chdir(WD); exec(compile(N, os.path.join(HERE, "nf1_x74_sl1"), "exec"), {"__file__": os.path.join(HERE, "nf1_x74_sl1.py"), "__name__": "__main__", "SL1ADD": SL1ADD})
