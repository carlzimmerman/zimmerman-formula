#!/usr/bin/env python3
"""OP2 (FROZEN_CRITERIA.md): ZN3's grader with EM1's line as the cold mass in clusters. Drives zn3_grade.py --worker; ZN3's files are read only. python3 op2.py"""
import ast, json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); Z3 = os.path.join(RB, "ZN3_native_shape_at_1e15"); ZG = os.path.join(Z3, "zn3_grade.py"); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SH = os.path.join(Z3, "zn3_shapes.json"); SLOPE = "2.7774425603108597"
ZT = open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_grade.py")).read(); GAS = ast.literal_eval(re.search(r'GAS = ("""(?:.*?)""")', ZT, re.S).group(1)); FC = 0.8405; RXF = FC ** (1 / 3); HH = ("h0672", "h0686")
OPDEF = '''
_OP2A = float(os.environ["OP2_A"])
def zn1_m200_fs(Mb, z):
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); thr = 200 * rc * (NAT_OM * (1 + z) ** 3 + 1 - NAT_OM); fc_ = NAT_RRAT / (1 + NAT_RRAT)
    d = 10 ** (_OP2A + 0.90 * (np.log10(np.maximum(Mb, 1e-200) / MSUNE) - 10)) * MSUNE / fc_ / (4 / 3 * math.pi * RM ** 3); i = np.where(d >= thr)[0]
    if len(i) == 0: return None, None, thr
    i = int(i.max()); lr = math.log(RM[i]) + (math.log(thr) - math.log(d[i])) / (math.log(d[i + 1]) - math.log(d[i])) * (math.log(RM[i + 1]) - math.log(RM[i])); R = math.exp(lr)
    return thr * 4 / 3 * math.pi * R ** 3, R, thr
'''
TD = tempfile.mkdtemp(); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def run(lab, fs, gas, rx, a):
    WD = os.path.join(TD, re.sub(r"\W", "_", lab)); os.makedirs(WD); o = os.path.join(WD, "o.json"); xf = os.path.join(WD, "x.py"); s = GAS if gas else ""
    if a is not None: s += f"sub('def zn1_fn(foot, tag, pp, z):', {OPDEF!r} + 'def zn1_fn(foot, tag, pp, z):')\n"
    open(xf, "w").write(s); env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"), X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, ZN1_MODE="fs", ZN1_RX=str(rx), ZN1_SNAP="nearest", ZN1_SHAPES=SH, ZN1_XFILE=xf, OP2_A=str(a or 0), PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, ZG, "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED {lab} exit {p.returncode}: {p.stdout[-300:]} {p.stderr[-1500:]}")
    return lab, json.load(open(o))
def cells(R):
    c = R["grader"]["canonical"]["clusters"]["cells"]; O = {}
    for h in HH:
        m = R["M_outer"][f"canonical|{h}"]; O[h] = {k: dict(v) for k, v in c[h].items()}
        for k, A in [("G-OUT-Mall", m["all"])] + [(f"G-OUT-M{t + 1}", m["terc"][t]) for t in range(3)]:
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
A = 11.18
J = [("K1 fair share, rx 1, f* 0.034, eRASS1 gas", "0.034", False, 1.0, None), ("MUTATE a+0.2, FC1 map, f* 0.034, eRASS1 gas", "0.034", False, RXF, A + .2)]
for fs in ("0.034", "0.0615"):
    J += [(f"PRIMARY EM1, FC1 map, f* {fs}, eRASS1 gas", fs, False, RXF, A), (f"EM1, frozen map, f* {fs}, eRASS1 gas", fs, False, 1.0, A), (f"EM1, FC1 map, f* {fs}, X-COP gas", fs, True, RXF, A), (f"fair share, FC1 map, f* {fs}, eRASS1 gas", fs, False, RXF, None)]
with ThreadPoolExecutor(3) as ex: RR = list(ex.map(lambda j: run(*j), J))
RES = {}; ok = {}
for lab, R in RR:
    O = cells(R); bad = sorted({k for h in HH for k, v in O[h].items() if abs(v["Z"]) > 2}); x = R["footings"]["canonical"]; w = max(((k, h, v["Z"]) for h in HH for k, v in O[h].items()), key=lambda t: abs(t[2])); xp = abs(x["mean"]) <= .05 and x["rms"] <= .10; ok[lab] = (not bad, xp)
    P(f"{lab}: {15 - len(bad)} of 15, over 2 {bad}, worst {w[0]} {w[1]} {w[2]:+.2f}; X-COP {'PASS' if xp else 'FAIL'} mean {x['mean']:+.3f} rms {x['rms']:.3f} by x " + " ".join(f"{k} {v:+.3f}" for k, v in x["by_x"].items()) + f"; groups {R['grader']['canonical']['groups']['Z']:+.2f}; no_fs {R['zn1'].get('no_fs')}")
    P("   h 0.672: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in O["h0672"].items())); RES[lab] = dict(bad=bad, cells=O, xcop={k: x[k] for k in ("mean", "rms", "by_x")})
a, b = [ok[f"PRIMARY EM1, FC1 map, f* {f}, eRASS1 gas"] for f in ("0.034", "0.0615")]
V = "ONE RULE PASSES" if all(a + b) else "KEYS PASS, X-COP FAILS" if a[0] and b[0] else "X-COP PASSES, KEYS FAIL" if a[1] and b[1] else "BOTH FAIL" if not (a[0] or b[0] or a[1] or b[1]) else "MIXED"
tag = " [F*-DEPENDENT]" if a != b else ""; P(f"VERDICT: {V}{tag}"); json.dump(dict(verdict=V + tag, runs=RES), open(os.path.join(HERE, "op2_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "op2.out"), "w").write("\n".join(OUT) + "\n"); shutil.rmtree(TD, ignore_errors=True)
