#!/usr/bin/env python3
"""POST-RESULT, reported only: the shear keys with eRASS1's gas on X-COP's scale (+0.111 dex, SM1), with the four keys that read fixed X7 values put on the same template as the rest.
The other 11 keys recompute measured A against the current template. G-OUT-Mall and G-OUT-M1..M3 read X7's A_CAL, computed with the original gas, so a gas change leaves them on the old template while their predictions use the new one. Here: A from this run's M_all|OUTER and M_terc|OUTER, s_CAL scaled by the same ratio. At the original gas this is the identity (K).
Rules: MA1 (S from M200, budget r0) and NZ1 (zoom r0), CLUSTERS mode. X-COP keeps its own gas. Optional z_obs as MA1's stress test.
    python3 nz1_common_gas.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade")
T = open(os.path.join(HERE, "nz1_grade.py")).read()
a = '    A = "sys.argv = [SRC]\\n"; assert TX.count(A) == 1'; assert T.count(a) == 1
T = T.replace(a, '    MY += open(os.environ["NZ1_XFILE"]).read()\n' + a)
TD = tempfile.mkdtemp(); W = os.path.join(HERE, "_nz1_cg_worker.py"); open(W, "w").write(T)
GAS = """_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\' % (10 ** 0.111))\\n'
sub('NX = {"__file__": X30SRC,', _x + 'NX = {"__file__": X30SRC,')
"""
ZOB = r'''
_z = """ZOBS = dict(D=1.0, E2=1.0)
def zobs_set(tag, z):
    e = EPS[tag]; ZOBS["D"] = float(np.interp(z, e["zg"], e["Dg"])); ZOBS["E2"] = NAT_OM * (1 + z) ** 3 + 1 - NAT_OM
def zobs_reset(): ZOBS["D"] = 1.0; ZOBS["E2"] = 1.0
"""
sub('def zform(tag, M):', _z + 'def zform(tag, M):')
sub('S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0)); Df = DC / (DC + OMEGA * S)', 'S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0)); Df = DC / (DC / ZOBS["D"] + OMEGA * S)')
sub('thr = 200 * rc if MA1_MODE == "m200" else 18 * math.pi ** 2 * NAT_OM * rc', 'thr = (200 * rc if MA1_MODE == "m200" else 18 * math.pi ** 2 * NAT_OM * rc) * ZOBS["E2"]')
sub('pp = prep(int(i), foot, hk); Mtot = ma1_arg(foot, tag, pp)', 'pp = prep(int(i), foot, hk); zobs_set(tag, NX["CL"][int(i)]["z"]); Mtot = ma1_arg(foot, tag, pp)')
sub('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'zobs_reset(); V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)')
'''
DUMP = """sub('_OUT.update(ma1=_st,', '_OUT["M_outer"] = {f"{f_}|{h_}": dict(all=M[f"{f_}|{h_}"]["M_all|OUTER"]["A"], terc=[x_["A"] for x_ in M[f"{f_}|{h_}"]["M_terc|OUTER"]]) for f_ in FEET for h_ in HK}\\n_OUT.update(ma1=_st,')
"""
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("Shear keys on one template, POST-RESULT, reported only; CLUSTERS mode; X-COP keeps its own gas; kappa = 1/2 FITTED; footings never pooled; not theory closed [cluster masses ng 48]")
def run(tag, mode, txt, fs):
    WD = os.path.join(TD, tag + fs); os.makedirs(WD); t = os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"); o = os.path.join(WD, "o.json"); xf = os.path.join(WD, "x.py"); open(xf, "w").write(txt + DUMP)
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, NZ1_MODE=mode, NZ1_R0X="1", NZ1_XFILE=xf, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, W, "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {tag} {fs} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-900:]}")
    return json.load(open(o))
def fixed(R):
    """Z for every key with the four X7 keys on this run's template."""
    c = R["grader"]["canonical"]["clusters"]["cells"]; O = {}
    for h in c:
        m = R["M_outer"][f"canonical|{h}"]; O[h] = {k: dict(v) for k, v in c[h].items()}
        for k, A in [("G-OUT-Mall", m["all"])] + [(f"G-OUT-M{t + 1}", m["terc"][t]) for t in range(3)]:
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
JOBS = [("NZ1, original gas", "clusters", ""), ("NZ1, gas on X-COP's scale", "clusters", GAS), ("NZ1, X-COP's scale, z_obs", "clusters", GAS + ZOB), ("MA1, gas on X-COP's scale", "off", GAS), ("MA1, X-COP's scale, z_obs", "off", GAS + ZOB)]
RES = {}
try:
    with ThreadPoolExecutor(2) as ex:
        fu = [(lab, fs, ex.submit(run, lab.replace(" ", "_").replace(",", "").replace("'", ""), mode, txt, fs)) for lab, mode, txt in JOBS for fs in ("0.034", "0.0615")]
        for lab, fs, q in fu:
            R = q.result(); O = fixed(R); RES[f"{lab}|{fs}"] = dict(cells=O, xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms", "by_x")}, nz1=R["nz1"], ma1={k: v for k, v in R["ma1"].items()}, groupsZ=R["grader"]["canonical"]["groups"]["Z"], U=[R["grader"]["canonical"]["sparc"][t]["U_median"] for t in ("A_c2b_refit", "B_cfg886_bg")])
            bad = sorted({k for h in O for k, v in O[h].items() if abs(v["Z"]) > 2}); x = R["footings"]["canonical"]; ok = 15 - len(bad)
            P(f"  {lab}, f* {fs}: {ok} of 15 keys pass; over 2: {bad}; X-COP mean {x['mean']:+.3f} rms {x['rms']:.3f}; SPARC U {RES[f'{lab}|{fs}']['U'][0]:.2f}/{RES[f'{lab}|{fs}']['U'][1]:.2f}; groups Z {RES[f'{lab}|{fs}']['groupsZ']:+.2f}")
            for h in ("h0672", "h0686"): P(f"     {h}: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in O[h].items()))
finally:
    os.remove(W)
J = json.load(open(os.path.join(HERE, "nz1_results.json")))["runs"]; d = max(abs(RES[f"NZ1, original gas|{fs}"]["cells"][h][k]["Z"] - J[f"clusters_fs{fs}"]["grader"]["canonical"]["clusters"]["cells"][h][k]["Z"]) for fs in ("0.034", "0.0615") for h in ("h0672", "h0686") for k in ("G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3"))
P(f"K at the original gas, this template step leaves the four keys where NZ1 had them: max |dZ| {d:.1e} (X7 A_CAL vs this run's A, tolerance 0.01): {'PASS' if d <= 0.01 else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "nz1_common_gas_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nz1_common_gas.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if d <= 0.01 else 1)
