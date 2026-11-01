#!/usr/bin/env python3
"""M3A1 driver (FROZEN_CRITERIA.md): ZN4's grader text at gas +0.005 with a per-cluster dump of the model vectors and measured sums. No output lands in other lanes. Serial, one thread; each job cached in cache_jobs; SIGTERM exits 75.
    python3 m3a1_grade.py [job ...]
kappa = 1/2 FITTED; not theory closed."""
import json, os, re, signal, sys
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
SH = os.path.join(ZN4D, "zn4_shapes.json"); G5 = GAS.replace("0.111", "0.005"); assert G5 != GAS
CJ = os.path.join(HERE6, "cache_jobs"); os.makedirs(CJ, exist_ok=True)
def xfile(job, dump):
    ff = {"BASE": None, "C1a": "C1a", "C1a_MUTATE": "C1a_MUTATE", "C1a_M3": "C1a_M3", "C1a_cap": "C1a_cap", "C2a": "C2a", "C2a_plus": "C2a_plus", "SHUF": None}.get(job)
    mc = {"MC0": 0.0, "MC2": 2.0}.get(job, 1.0); x = ""
    if ff:
        p = os.path.join(HERE6, f"m3a1_factor_{ff}.json")
        x += f"""_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5*\\' + repr(10 ** 0.005) + \\';\\'\\nassert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*\\' + repr(10 ** 0.005) + \\'*M3F[cl["name"]];\\'); codeX = codeX.replace("PREP = {{}}\\\\n", "PREP = {{}}\\\\nimport json as _jj; M3F = _jj.load(open(%r))\\\\n", 1)\\n' % {p!r}
sub('NX = {{"__file__": X30SRC,', _x + 'NX = {{"__file__": X30SRC,')
"""
    if mc != 1.0:
        x += f"""_x = '_g = \\'dmpc=np.radians(cl["off_deg"])\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'dmpc=np.radians(cl["off_deg"]*{mc})\\')\\n'
sub('NX = {{"__file__": X30SRC,', _x + 'NX = {{"__file__": X30SRC,')
"""
    hook = f"""
if SHAPE["s"] == "S" and ETA_USE["v"] == ETA and foot == "canonical":
            import numpy as _n; M3DUMP[hk] = V.copy(); M3DUMPC[hk] = bsum(DC_[(foot, hk)]).copy()
            _mm = NX["MEAS"][(foot, hk)]; _n.savez_compressed({dump!r}, **{{f"V_{{q}}": v_ for q, v_ in M3DUMP.items()}}, **{{f"d_{{q}}": NX["MEAS"][(foot, q)]["d"] for q in M3DUMP}}, **{{f"n_{{q}}": NX["MEAS"][(foot, q)]["n"] for q in M3DUMP}}, **{{f"nraw_{{q}}": NX["MEAS"][(foot, q)]["nraw"] for q in M3DUMP}}, **{{f"nx_{{q}}": NX["MEAS"][(foot, q)]["nx"] for q in M3DUMP}}, **{{f"nrr_{{q}}": NX["MEAS"][(foot, q)]["nrr"] for q in M3DUMP}}, **{{f"vC_{{q}}": DC_[(foot, q)] for q in M3DUMP}}, T3M=NX["T3M"], TID=NX["TID"], I=NX["I"], PATCH=NX["PATCH"])
"""
    x += "sub('cl = f\"{foot}|{hk}\"; o = M[cl]; vB = bsum(V);', " + repr(hook.strip("\n").replace("\n", "\n        ") ) + " + '\\n        cl = f\"{foot}|{hk}\"; o = M[cl]; vB = bsum(V);')\n"
    x += "sub('def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):', 'M3DUMP = {}; M3DUMPC = {}\\ndef grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):')\n"
    return G5 + x
signal.signal(signal.SIGTERM, lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))
def job(name, fs):
    f = os.path.join(CJ, f"{name}_{fs}.json"); dump = f[:-5] + "_dump.npz"
    if os.path.exists(f): return json.load(open(f))
    try: R = run(fs, "fs", xfile(name, dump), SH)
    except KeyboardInterrupt: sys.exit(75)
    O = dict(cells=cells(R), xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms")}, groupsZ=R["grader"]["canonical"]["groups"]["Z"]); json.dump(O, open(f + ".tmp", "w"), default=float); os.replace(f + ".tmp", f); return O
if __name__ == "__main__":
    FS = ("0.034", "0.0615"); ALL = [(j, fs) for j in ("BASE", "C1a", "C2a", "MC0", "MC2") for fs in FS] + [("C2a_plus", "0.034"), ("C1a_MUTATE", "0.034"), ("C1a_M3", "0.034"), ("C1a_cap", "0.034")]; want = sys.argv[1:]
    for j, fs in ALL:
        if want and j not in want: continue
        O = job(j, fs); c = O["cells"]; print(j, fs, " ".join(f"{h} M3 {c[h]['G-OUT-M3']['Z']:+.3f} Mall {c[h]['G-OUT-Mall']['Z']:+.3f} T3 {c[h]['G-MID-T3']['Z']:+.3f}" for h in HH), f"X-COP {O['xcop']['mean']:+.3f} {O['xcop']['rms']:.3f}", flush=True)
