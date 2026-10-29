#!/usr/bin/env python3
"""X74_all_measured_native_cf: X73_smooth_core_all_measured's script, run unchanged except that the collapse branch uses
eta(M) = (4/(3 B_S(1))) c_f(M)^(5/4) with the native c_f(M) from X48 A4 (criteria c3e69578c5).
Run (from this directory):
    X74_CF=const4|<path to x48_analyze_results_ng64_A4.json> X74_CFMULT=1 X73_FSTAR=0.034 X73_SLOPE=2.7774425603108597 \
        PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x74_native_cf.py
X73_SHAPE stays S and X73_NATIVE stays 1 (frozen). MUTATE = X74_CFMULT=2. Exit 0 only if every inherited check and,
at c_f = 4, the K1 identity against X73's committed JSON pass. X73's inherited K0 / K0x38 fail off f* 0.20 by
construction (as in X73 and X71), so the exit code is 1 there; the frozen K3 reads "same check pattern as X73"."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
SRC = os.path.join(REB, "X73_smooth_core_all_measured", "x73_all_measured.py"); T = open(SRC).read()
os.environ["X73_SHAPE"] = "S"; os.environ["X73_NATIVE"] = "1"
def sub(a, b):
    global T
    assert T.count(a) == 1, a
    T = T.replace(a, b)
CFBLOCK = '''
CFSRC = os.environ.get("X74_CF", "const4"); CFMULT = float(os.environ.get("X74_CFMULT", "1"))
if CFSRC == "const4":
    CFLM, CFV = np.array([12.0, 14.0]), np.array([4.0, 4.0])
else:
    _t = {float(k): v for k, v in json.load(open(CFSRC))["cf_by_mass"].items() if v is not None}
    if not all(any(abs(math.log10(m) - l) < 1e-6 for m in _t) for l in (12, 13, 14)): raise SystemExit("UNDECIDED: A4 table lacks 1e12/1e13/1e14")
    CFLM = np.array(sorted(math.log10(m) for m in _t)); CFV = np.array([_t[min(_t, key=lambda m: abs(math.log10(m) - l))] for l in CFLM])
CFV = CFV * CFMULT
def cf_of(M): return float(np.interp(math.log10(M), CFLM, CFV))
'''
sub("NAT_OB = NAT_wb / NAT_h ** 2; NAT_RRAT = (NAT_OM - NAT_OB) / NAT_OB\n", "NAT_OB = NAT_wb / NAT_h ** 2; NAT_RRAT = (NAT_OM - NAT_OB) / NAT_OB\n" + CFBLOCK)
sub('    sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2',
    '    sc = (eta_of(cf_of(M)) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2')
sub('"x73_x30_machinery"', '"x74_x30_machinery"')
X74TAIL = '''
P("c_f table: " + ", ".join(f"1e{l:.0f}: {c:.3f}" for l, c in zip(CFLM, CFV)) + "; eta(M) at 1e12/13/14/15: "
  + ", ".join(f"{eta_of(cf_of(10 ** l)):.3f}" for l in (12, 13, 14, 15)))
k2x = all(abs(eta_of(cf_of(10 ** l)) - 4.0 / (3.0 * float(B(1.0))) * cf_of(10 ** l) ** 1.25) < 1e-12 for l in (12, 13, 14, 15))
P(f"X74 K2 eta(M) formula: {'PASS' if k2x else 'FAIL'}")
RES["x74"] = dict(cf_src=CFSRC, cf_mult=CFMULT, cf_lgM=CFLM.tolist(), cf=CFV.tolist(), eta={f"1e{l}": eta_of(cf_of(10 ** l)) for l in (12, 13, 14, 15)}, k2=k2x)
x74ok = k2x
if CFSRC == "const4" and CFMULT == 1 and SLOPE is not None:
    XJ = json.load(open(os.path.join(REB, "X73_smooth_core_all_measured", f"x73_results_fs{FSTAR:g}_S_nat_s{SLOPE:.4f}.json")))
    did = max(abs(RES["footings"][f_]["clusters"]["cells"][hk_][k_]["pred"] - XJ["footings"][f_]["clusters"]["cells"][hk_][k_]["pred"])
              for f_ in FEET for hk_ in HK for k_ in XJ["footings"][f_]["clusters"]["cells"][hk_])
    dsp = max(abs(RES["footings"][f_]["sparc"][t_]["rms"] - XJ["footings"][f_]["sparc"][t_]["rms"]) for f_ in FEET for t_ in XJ["footings"][f_]["sparc"])
    dgz = max(abs(RES["footings"][f_]["groups"]["Z"] - XJ["footings"][f_]["groups"]["Z"]) for f_ in FEET)
    k1x = max(did, dsp, dgz) <= 1e-9
    P(f"X74 K1 identity vs X73 (c_f 4): clusters {did:.1e}, SPARC rms {dsp:.1e}, groups Z {dgz:.1e}: {'PASS' if k1x else 'FAIL'}")
    RES["x74"]["k1"] = dict(clusters=did, sparc=dsp, groups=dgz, ok=k1x); x74ok = x74ok and k1x
cft = "c4" if CFSRC == "const4" else "nat"
tagf = f"_fs{FSTAR:g}_{cft}{'' if CFMULT == 1 else 'x%g' % CFMULT}_{'s%.4f' % SLOPE if SLOPE is not None else 'notail'}"
'''
sub("tagf = f\"_fs{FSTAR:g}_{SHAPE['s']}_{'nat' if NATIVE else 'inh'}_{'s%.4f' % SLOPE if SLOPE is not None else 'notail'}\"\n", X74TAIL)
sub('f"x73{tagf}.out"', 'f"x74{tagf}.out"'); sub('f"x73_results{tagf}.json"', 'f"x74_results{tagf}.json"')
sub("sys.exit(0 if n == len(checks) else 1)", "sys.exit(0 if (n == len(checks) and x74ok) else 1)")
if os.environ.get("X74_CF", "const4") != "const4": T = T.replace("[c_f EXTERNAL]", "[c_f NATIVE, X48 A4]")
sys.argv = [SRC]
exec(compile(T, os.path.join(HERE, "x74_native_cf.py[x73]"), "exec"), {"__file__": os.path.join(HERE, "x74_native_cf.py"), "__name__": "__main__"})
