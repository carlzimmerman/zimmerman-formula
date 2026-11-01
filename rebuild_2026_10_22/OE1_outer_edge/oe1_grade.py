#!/usr/bin/env python3
"""OE1 driver (FROZEN_CRITERIA.md): ZN4's grader text at gas +0.005 with the edge variants; per-cluster dump as M3A1. Serial, one thread, cached in cache_jobs, SIGTERM exits 75.
    python3 oe1_grade.py [job ...]
kappa = 1/2 FITTED; not theory closed."""
import json, os, signal, sys
HERE6 = os.path.dirname(os.path.abspath(__file__)); RB6 = os.path.dirname(HERE6); ZN1D = os.path.join(RB6, "ZN1_zooms_to_z0"); ZN4D = os.path.join(RB6, "ZN4_cluster_resolution"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(RB, 'ZN1_zooms_to_z0', 'zn1_def.py')!r}).read() + open({os.path.join(RB, 'ZN3_native_shape_at_1e15', 'zn3_def.py')!r}).read()""")
_s('open(os.path.join(HERE, "zn1_boot_tail.py")).read()', 'open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_boot_tail.py")).read()')
_s('open(xf, "w").write(GAS if gas else "")', 'open(xf, "w").write(gas)')
_s('{int(gas)}', '{abs(hash(gas)) % 10 ** 8}')
_s('["nice", "-n", "5", sys.executable', '["nice", "-n", "15", sys.executable')
K = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:')
exec(compile(T3[:K], os.path.abspath(__file__), "exec"))
G5 = GAS.replace("0.111", "0.005"); assert G5 != GAS; CJ = os.path.join(HERE6, "cache_jobs"); os.makedirs(CJ, exist_ok=True); INJT = open(os.path.join(HERE6, "oe1_inject.py")).read()
SHZ = os.path.join(ZN4D, "zn4_shapes.json")
def node(tag):
    p = os.path.join(CJ, f"shapes_{tag}.json")
    if tag == "MEAN" and not os.path.exists(p):   # reported, post-result: mean M(<r)/M200 over seeds in place of the median
        import numpy as _n; S = json.load(open(SHZ))
        for m_ in ("1e13", "1e14", "1e15"):
            for k_, q_ in S[m_].items(): q_["lnm"] = _n.log(_n.mean(_n.exp(_n.array([r_["lnm"] for r_ in q_["seeds"]])), axis=0)).tolist()
        json.dump(S, open(p, "w"))
    if not os.path.exists(p):
        S = json.load(open(SHZ)); V = json.load(open(os.path.join(RB6, "VB1_vacuum_boundary", f"vb1_shape_{tag}.json"))); S["1e14"] = V; json.dump(S, open(p, "w"))
    return p
def xfile(var, dump, rowf, dec):
    head = f"OE1_VAR = {var!r}\n"; x = G5 + f"sub('def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):', {(head + INJT)!r} + 'def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):')\n"
    hook = f"""
if SHAPE["s"] == "S" and ETA_USE["v"] == ETA and foot == "canonical":
            import numpy as _n; M3DUMP[hk] = V.copy(); M3DUMPC[hk] = bsum(DC_[(foot, hk)]).copy()
            _n.savez_compressed({dump!r}, **{{f"V_{{q}}": v_ for q, v_ in M3DUMP.items()}}, **{{f"d_{{q}}": NX["MEAS"][(foot, q)]["d"] for q in M3DUMP}}, **{{f"n_{{q}}": NX["MEAS"][(foot, q)]["n"] for q in M3DUMP}}, **{{f"vC_{{q}}": DC_[(foot, q)] for q in M3DUMP}}, T3M=NX["T3M"], TID=NX["TID"], I=NX["I"], PATCH=NX["PATCH"]); json.dump(dict(k2=OE1_K2["max"], rows=OE1_ROWS), open({rowf!r}, "w"), default=float)
"""
    x += "sub('cl = f\"{foot}|{hk}\"; o = M[cl]; vB = bsum(V);', " + repr(hook.strip("\n").replace("\n", "\n        ")) + " + '\\n        cl = f\"{foot}|{hk}\"; o = M[cl]; vB = bsum(V);')\n"
    x += "sub('def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):', 'M3DUMP = {}; M3DUMPC = {}\\ndef grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):')\n"
    if dec: x += """sub('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)\\n            if SHAPE["s"] == "S" and ETA_USE["v"] == ETA and foot == "canonical": oe1_dec(int(i), pp, Mh, foot, hk, NX["CL"][int(i)]["z"], pp["Mb"] + Mh)')\n"""
    return x
signal.signal(signal.SIGTERM, lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))
JOBS = dict(OFF=("OFF", SHZ), E1=("E1", SHZ), E2=("E2", SHZ), E3=("E3", SHZ), OFFA=("OFF", "A"), OFFB=("OFF", "B"), E1A=("E1", "A"), E1B=("E1", "B"), M10=("M10", SHZ), MZ=("MZ", SHZ), E1MEAN=("E1", "MEAN"))
def job(name, fs):
    f = os.path.join(CJ, f"{name}_{fs}.json"); dump = f[:-5] + "_dump.npz"; rowf = f[:-5] + "_rows.json"
    if os.path.exists(f): return json.load(open(f))
    v, sh = JOBS[name]; sh = sh if sh == SHZ else node(sh)
    try: R = run(fs, "fs", xfile(v, dump, rowf, name == "OFF" and fs == "0.034"), sh)
    except KeyboardInterrupt: sys.exit(75)
    O = dict(cells=cells(R), xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms")}, xcop_by=R["footings"]["canonical"]["by_x"], groupsZ=R["grader"]["canonical"]["groups"]["Z"], zn1=R["zn1"]); json.dump(O, open(f + ".tmp", "w"), default=float); os.replace(f + ".tmp", f); return O
if __name__ == "__main__":
    want = sys.argv[1:] or list(JOBS)
    for j in want:
        for fs in ("0.034", "0.0615"):
            if j in ("M10", "MZ") and fs != "0.034": continue
            O = job(j, fs); c = O["cells"]; print(j, fs, " ".join(f"{h} M3 {c[h]['G-OUT-M3']['Z']:+.3f}" for h in HH), f"X-COP {O['xcop']['mean']:+.3f} {O['xcop']['rms']:.3f}", flush=True)
