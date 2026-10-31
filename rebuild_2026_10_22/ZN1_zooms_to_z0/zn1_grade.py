#!/usr/bin/env python3
"""ZN1 grade (criteria 22d690ccf2, AMENDMENT A1, A2): the native z = 0 profile on X-COP and the 15 shear keys, one template, X-COP's gas scale primary.
    python3 zn1_grade.py --k3             # K3: the harness reproduces MA1's predictions; reads no ZN1 snapshot
    python3 zn1_grade.py --shapes FILE    # a shape table to grade, default zn1_shapes.json
    python3 zn1_grade.py --mutate         # shape's r x 1.5, separate outputs
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); MA1 = os.path.join(RB, "MA1_cluster_mass_argument"); HH = ("h0672", "h0686")
GAS = """_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\' % (10 ** 0.111))\\n'
sub('NX = {"__file__": X30SRC,', _x + 'NX = {"__file__": X30SRC,')
"""
if "--worker" in sys.argv:
    WD = os.environ["MA1_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
    INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    tail = open(os.path.join(MA1, "ma1_tail.py")).read(); e = 'exec(compile(_T1, "xh1_tail_ma1", "exec"), globals())'; assert tail.count(e) == 1
    PATCH = r'''
_a = 'Mh = math.pi * s * r0 ** 2 * float(B(min(rm, rta) / r0)); dd.append('; assert _T1.count(_a) == 1; _T1 = _T1.replace(_a, 'Mh = float(_znf(np.array([min(rm, rta)]))[0]); dd.append(')
_a = 'k2.append(0.0 if sat else'; assert _T1.count(_a) == 1; _T1 = _T1.replace(_a, '_znf = zn1_fn(foot, _TBG, dict(Mb=_mbx, Mfair=Mfair, rta=rta), _XM[nm]["z"]); k2.append(0.0 if sat else')
'''
    tail = tail.replace(e, PATCH + e)
    tail = tail.replace('_OUT.update(ma1=_st,', '_g = ZN1_STAT["gam"]; _OUT["zn1"] = dict(cells=ZN1_STAT["cells"], no_tail=ZN1_STAT["no_tail"], no_fs=ZN1_STAT["no_fs"], k4=ZN1_STAT["k4"], gam_med=float(np.median(_g)) if _g else None, gam_p16=float(np.percentile(_g, 16)) if _g else None, gam_p84=float(np.percentile(_g, 84)) if _g else None, m2_over_mta=float(np.median(ZN1_STAT["ratio"])) if ZN1_STAT["ratio"] else None)\n_OUT["M_outer"] = {f"{f_}|{h_}": dict(all=M[f"{f_}|{h_}"]["M_all|OUTER"]["A"], terc=[x_["A"] for x_ in M[f"{f_}|{h_}"]["M_terc|OUTER"]]) for f_ in FEET for h_ in HK}\n_OUT.update(ma1=_st,', 1)
    open(os.path.join(WD, "tail.py"), "w").write(tail)
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()
sub('def grade_clusters(foot, rule=True, tag="A_c2b_refit"):', _d + 'def grade_clusters(foot, rule=True, tag="A_c2b_refit"):')
sub('r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)', '''if SHAPE["s"] == "S" and ETA_USE["v"] == ETA: Mh = zn1_fn(foot, tag, pp, NX["CL"][int(i)]["z"])(RM)
            else: r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)''')
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", open({os.path.join(WD, 'tail.py')!r}).read())
"""
    MY += open(os.environ["ZN1_XFILE"]).read()
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
TD = tempfile.mkdtemp(); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def run(fs, mode, gas, shapes, rx=1.0, snap="nearest"):
    tag = f"{fs}_{mode}_{int(gas)}_{rx:g}_{snap}"; WD = os.path.join(TD, tag); os.makedirs(WD); t = os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"); o = os.path.join(WD, "o.json"); xf = os.path.join(WD, "x.py"); open(xf, "w").write(GAS if gas else "")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, ZN1_MODE=mode, ZN1_RX=str(rx), ZN1_SNAP=snap, ZN1_SHAPES=shapes, ZN1_XFILE=xf, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "5", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {tag} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-1200:]}")
    r = json.load(open(o)); shutil.rmtree(WD, ignore_errors=True); return r
def cells(R):
    c = R["grader"]["canonical"]["clusters"]["cells"]; O = {}
    for h in HH:
        m = R["M_outer"][f"canonical|{h}"]; O[h] = {k: dict(v) for k, v in c[h].items()}
        for k, A in [("G-OUT-Mall", m["all"])] + [(f"G-OUT-M{t + 1}", m["terc"][t]) for t in range(3)]:
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
xok = lambda x: abs(x["mean"]) <= 0.05 and x["rms"] <= 0.10
def line(lab, R):
    O = cells(R); bad = sorted({k for h in HH for k, v in O[h].items() if abs(v["Z"]) > 2}); x = R["footings"]["canonical"]; z = R["zn1"]; w = max(((k, h, v["Z"]) for h in HH for k, v in O[h].items()), key=lambda t: abs(t[2]))
    P(f"  {lab}: {15 - len(bad)} of 15 keys, over 2 {bad}, worst {w[0]} {w[1]} {w[2]:+.2f}; X-COP {'PASS' if xok(x) else 'FAIL'} mean {x['mean']:+.3f} rms {x['rms']:.3f} by x " + " ".join(f"{k} {v:+.3f}" for k, v in x["by_x"].items()) + f"; gamma med {z['gam_med']}, no tail {z['no_tail']}, no fair-share R200 {z['no_fs']} of {z['cells']}, M200/M_ta {z['m2_over_mta']}")
    P("     h 0.672: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in O["h0672"].items())); P("     h 0.686: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in O["h0686"].items())); return bad, xok(x)
if __name__ == "__main__":
    if "--k3" in sys.argv:
        sh = os.path.join(TD, "syn.json"); import numpy as np; X_ = np.geomspace(1e-3, 40.0, 500); mu = lambda y: np.log1p(y) - y / (1 + y); lnm = (np.log(mu(5.0 * X_) / mu(5.0))).tolist(); B_ = dict(lgM=14.0, x_edge=2.0, lnm=lnm); A_ = dict(lgM=13.0, x_edge=2.0, lnm=lnm); json.dump({"x": X_.tolist(), "1e13": {k: A_ for k in ("0.00", "0.25", "0.50")}, "1e14": {k: B_ for k in ("0.00", "0.25", "0.50")}}, open(sh, "w"))
        R = run("0.034", "ma1", False, sh); O = cells(R); J = json.load(open(os.path.join(RB, "NZ1_zoom_core_radius", "nz1_one_template_results.json")))["rules"]["MA1|0.034"]["cells"]; d = max(abs(O[h][k]["pred"] - J[h][k]["pred"]) for h in HH for k in J[h]); e = max(abs(O[h][k]["Z"] - J[h][k]["Z"]) for h in HH for k in J[h]); ok = d <= 1e-9 and e <= 1e-9
        P(f"K3 the harness in MA1's mode reproduces MA1 on one template: preds {d:.1e}, Z {e:.1e}: {'PASS' if ok else 'FAIL'}"); R2 = run("0.034", "fs", True, sh); line("synthetic NFW c 5 at every mass, harness test, not a result", R2); open(os.path.join(HERE, "zn1_k3.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
    SH = sys.argv[sys.argv.index("--shapes") + 1] if "--shapes" in sys.argv else os.path.join(HERE, "zn1_shapes.json"); MUT = "--mutate" in sys.argv; TAG = "zn1_MUTATE" if MUT else "zn1"
    P(f"ZN1 grade {TAG}: native z = 0 profile, one template, X-COP's gas scale primary; kappa = 1/2 FITTED; footings never pooled; not theory closed")
    if MUT:
        b = run("0.034", "fs", True, SH); m = run("0.034", "fs", True, SH, rx=1.5); line("base", b); line("shape's r x 1.5", m); dr = m["footings"]["canonical"]["rms"] - b["footings"]["canonical"]["rms"]; dg = cells(m)["h0672"]["G-IN-Mall"]["Z"] - cells(b)["h0672"]["G-IN-Mall"]["Z"]; bites = abs(dr) > 0.01 and abs(dg) > 0.05
        P(f"MUTATE moves X-COP rms by {dr:+.3f}, G-IN-Mall by {dg:+.2f}: {'BITES' if bites else 'INSENSITIVE, lane UNDECIDED'}"); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if bites else 1)
    JOBS = [(f"f* {fs}, X-COP's gas", dict(fs=fs, mode="fs", gas=True, shapes=SH)) for fs in ("0.034", "0.0615")] + [(f"f* {fs}, eRASS1's own gas", dict(fs=fs, mode="fs", gas=False, shapes=SH)) for fs in ("0.034", "0.0615")] + [(f"f* {fs}, X-COP's gas, MA1's budget M200", dict(fs=fs, mode="budget", gas=True, shapes=SH)) for fs in ("0.034", "0.0615")] + [(f"f* {fs}, X-COP's gas, z = 0 shape for all", dict(fs=fs, mode="fs", gas=True, shapes=SH, snap="0.00")) for fs in ("0.034", "0.0615")]
    with ThreadPoolExecutor(4) as ex: RR = list(ex.map(lambda j: (j[0], run(**j[1])), JOBS))
    RES = {}; res = {}
    for lab, R in RR: res[lab] = line(lab, R); RES[lab] = dict(cells=cells(R), xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms", "by_x", "per_cluster", "band")}, zn1=R["zn1"], groupsZ=R["grader"]["canonical"]["groups"]["Z"])
    def cls(a, b):
        pa = not a[0] and a[1]; pb = not b[0] and b[1]; xa, xb = a[1] and b[1], a[1] or b[1]; ka, kb = (not a[0]) and (not b[0]), (not a[0]) or (not b[0])
        return "Z0 PROFILE PASSES BOTH" if pa and pb else "F*-DEPENDENT" if pa or pb else "X-COP ONLY" if xb and not kb else "KEYS ONLY" if kb and not xb else "FAILS BOTH" if not xb and not kb else "NEITHER AT ONE f*: keys and X-COP pass at different f*"
    V = cls(res["f* 0.034, X-COP's gas"], res["f* 0.0615, X-COP's gas"]); V2 = cls(res["f* 0.034, eRASS1's own gas"], res["f* 0.0615, eRASS1's own gas"]); V3 = cls(res["f* 0.034, X-COP's gas, MA1's budget M200"], res["f* 0.0615, X-COP's gas, MA1's budget M200"])
    tags = ("" if V2 == V else " [GAS-SCALE-DEPENDENT]") + ("" if V3 == V else " [MASS-DEFINITION-DEPENDENT]"); P(f"VERDICT: {V}{tags}. eRASS1's own gas: {V2}. MA1's budget M200: {V3}. [NOISE-LIMITED] is read separately by --bootstrap")
    json.dump(dict(verdict=V, tags=tags, runs=RES), open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
