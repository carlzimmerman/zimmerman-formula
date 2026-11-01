#!/usr/bin/env python3
"""OP2 POST-RESULT, no frozen verdict: are the near misses seed noise? 100 seed draws at all three tags, EM1's line, measured gas, both maps, both f*."""
import json, os, re
import numpy as np
from concurrent.futures import ThreadPoolExecutor
S = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "op2.py")).read(); S = S[:S.index("A = 11.18")]; exec(compile(S, "op2_head", "exec"))
NB = 100; NW = 2
def go(j):
    fs, rx, ch = j; lab = f"{fs}_{rx:.3f}_{ch.replace('/', 'of')}"; WD = os.path.join(TD, lab); os.makedirs(WD); o = os.path.join(WD, "o.json"); xf = os.path.join(WD, "x.py"); open(xf, "w").write(f"sub('def zn1_fn(foot, tag, pp, z):', {OPDEF!r} + 'def zn1_fn(foot, tag, pp, z):')\n")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"), X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, ZN1_MODE="fs", ZN1_RX=str(rx), ZN1_SNAP="nearest", ZN1_SHAPES=SH, ZN1_XFILE=xf, OP2_A="11.18", ZN1_BOOT=str(NB), ZN1_BOOT_CHUNK=ch, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, ZG, "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED {lab}: {p.stderr[-1200:]}")
    return fs, rx, json.load(open(o))
J = [(fs, rx, f"{i}/{NW}") for fs in ("0.034", "0.0615") for rx in (RXF, 1.0) for i in range(NW)]
with ThreadPoolExecutor(4) as ex: RR = list(ex.map(go, J))
D = {}
for fs, rx, R in RR:
    for b in R["boot"]:
        O = cells(dict(grader=dict(canonical=dict(clusters=dict(cells=b["cells"]))), M_outer=R["M_outer"])); bad = sorted({k for h in HH for k, v in O[h].items() if abs(v["Z"]) > 2}); D.setdefault((rx, b["draw"]), {})[fs] = dict(nbad=len(bad), bad=bad, x=bool(abs(b["mean"]) <= .05 and b["rms"] <= .10), mean=b["mean"], rms=b["rms"], M3=max(O[h]["G-OUT-M3"]["Z"] for h in HH), IN=min(O[h]["G-IN-Mall"]["Z"] for h in HH))
RES = {}
for rx in (RXF, 1.0):
    ds = [D[k] for k in D if k[0] == rx]; n = len(ds); pa = sum(all(d[f]["nbad"] == 0 and d[f]["x"] for f in d) for d in ds); ke = sum(all(d[f]["nbad"] == 0 for f in d) for d in ds); xp = sum(all(d[f]["x"] for f in d) for d in ds)
    L = f"map {'FC1' if rx != 1.0 else 'frozen'}: draws {n}; 15 keys + X-COP at both f* {pa}; 15 keys at both f* {ke}; X-COP at both f* {xp}"
    for f in ("0.034", "0.0615"):
        m3 = np.array([d[f]["M3"] for d in ds]); me = np.array([d[f]["mean"] for d in ds]); r = np.array([d[f]["rms"] for d in ds]); L += f"\n   f* {f}: M3 {np.median(m3):+.2f} [{np.percentile(m3,16):+.2f}, {np.percentile(m3,84):+.2f}]; X-COP mean {np.median(me):+.3f} [{np.percentile(me,16):+.3f}, {np.percentile(me,84):+.3f}] rms {np.median(r):.3f}"
    P(L); RES["FC1" if rx != 1.0 else "frozen"] = dict(n=n, pass_all=pa, keys=ke, xcop=xp)
P("K identity " + str(max(R["boot_k"] for _, _, R in RR))); json.dump(RES, open(os.path.join(HERE, "op2_boot_results.json"), "w"), indent=1); open(os.path.join(HERE, "op2_boot.out"), "w").write("\n".join(OUT) + "\n")
