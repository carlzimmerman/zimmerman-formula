#!/usr/bin/env python3
"""Grader defect, POST-RESULT: four shear keys (G-OUT-Mall, G-OUT-M1..M3) read X7's fixed A_CAL and s_CAL, computed on the C* template at f* 0.20. Their predictions, and the other 11 keys' measured values, use the current template. This lane (1) finds which input moves the template, (2) restates FC1, MA1, NZ1 with the four keys on the run's own template, s_CAL scaled by the same ratio. Frozen labels stand as frozen.
    python3 nz1_one_template.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); MA1 = os.path.join(RB, "MA1_cluster_mass_argument")
if "--worker" in sys.argv:
    WD = os.environ["MA1_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
    INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    tail = '''_o = {f"{f_}|{h_}": dict(all=M[f"{f_}|{h_}"]["M_all|OUTER"]["A"], terc=[x_["A"] for x_ in M[f"{f_}|{h_}"]["M_terc|OUTER"]], x7_all=X7J["all"][f"C*|boost|{f_}|{h_}"]["OUTER"]["A_CAL"], x7_terc=[r_["OUTER"]["A_CAL"] for r_ in X7J["bins"][f"terciles|{f_}|{h_}"]], kt_out=M[f"{f_}|{h_}"]["KT_all|OUTER"]["A"]) for f_ in FEET for h_ in HK}
json.dump(_o, open(os.environ["XH1_OUT"], "w"), indent=1, default=float); sys.exit(0)
'''
    open(os.path.join(WD, "tail.py"), "w").write(tail)
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", open({os.path.join(WD, 'tail.py')!r}).read())
"""
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
OUT = []; TD = tempfile.mkdtemp()
def P(s): print(s, flush=True); OUT.append(s)
P("Grader defect: four shear keys on an old template, POST-RESULT; kappa = 1/2 FITTED; footings never pooled; not theory closed")
def prov(fs, sl):
    WD = os.path.join(TD, f"{fs}_{sl[:5]}"); os.makedirs(WD); o = os.path.join(WD, "o.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), X73_FSTAR=fs, X73_SLOPE=sl, XH1_OUT=o, MA1_WD=WD, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {fs} {sl} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-900:]}")
    return json.load(open(o))
J = [("0.20", "none"), ("0.20", SLOPE), ("0.034", "none"), ("0.034", SLOPE), ("0.0615", SLOPE)]
with ThreadPoolExecutor(2) as ex: RP = dict(zip(J, ex.map(lambda a: prov(*a), J)))
P("1. This run's A (OUTER) against X7's fixed A_CAL, canonical, h 0.672. Which input moves the template:")
for (fs, sl), r in RP.items():
    c = r["canonical|h0672"]; P(f"  f* {fs}, tail {'none' if sl == 'none' else 'to r_ta'}: M_all {c['all']:.4f} (X7 {c['x7_all']:.4f}), M1 {c['terc'][0]:.4f} ({c['x7_terc'][0]:.4f}), M2 {c['terc'][1]:.4f} ({c['x7_terc'][1]:.4f}), M3 {c['terc'][2]:.4f} ({c['x7_terc'][2]:.4f}); KT_all {c['kt_out']:.4f}")
c = RP[("0.20", "none")]; d = max(max(abs(c[k]["all"] - c[k]["x7_all"]), *[abs(a - b) for a, b in zip(c[k]["terc"], c[k]["x7_terc"])]) for k in c)
P(f"K at f* 0.20 with no tail this run's A equals X7's A_CAL, every cell: max |d| {d:.1e}: {'PASS' if d <= 1e-3 else 'FAIL'}")
KEYS = ["G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3"]; HH = ("h0672", "h0686")
def fix(cells, fs):
    """Same rule, same predictions; four measured values on the run's template."""
    m = RP[(fs, SLOPE)]; O = {}
    for h in HH:
        q = m[f"canonical|{h}"]; O[h] = {k: dict(v) for k, v in cells[h].items()}
        for k, A in zip(KEYS, [q["all"]] + q["terc"]):
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
def rep(lab, cells, fs, RES):
    O = fix(cells, fs); zs = [(k, h, v["Z"]) for h in HH for k, v in O[h].items()]; w = max(zs, key=lambda t: abs(t[2])); bad = sorted({k for k, _, z in zs if abs(z) > 2})
    w0 = max(((k, h, v["Z"]) for h in HH for k, v in cells[h].items()), key=lambda t: abs(t[2])); bad0 = sorted({k for h in HH for k, v in cells[h].items() if abs(v["Z"]) > 2})
    RES[f"{lab}|{fs}"] = dict(cells=O, over2=bad, worst=w, over2_frozen=bad0)
    P(f"  {lab}, f* {fs}: {15 - len(bad)} of 15 pass, worst {w[0]} {w[1]} {w[2]:+.2f}, over 2 {bad}; as the grader read it: {15 - len(bad0)} of 15, worst {w0[0]} {w0[2]:+.2f}, over 2 {bad0}. Four keys h 0.672: " + ", ".join(f"{k[6:]} {O['h0672'][k]['Z']:+.2f} ({cells['h0672'][k]['Z']:+.2f})" for k in KEYS))
RES = {}; P("2. Rules at the original gas, four keys on the run's template (as frozen in brackets):")
F = lambda fs: json.load(open(os.path.join(FC1, f"FC1_med_fs{fs}_x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")))["footings"]["canonical"]["clusters"]["cells"]
MJ = json.load(open(os.path.join(MA1, "ma1_results.json")))["runs"]; ZJ = json.load(open(os.path.join(MA1, "ma1_zobs_results.json"))); NJ = json.load(open(os.path.join(HERE, "nz1_results.json")))["runs"]; NZ = json.load(open(os.path.join(HERE, "nz1_zobs_results.json")))
for fs in ("0.034", "0.0615"):
    g = lambda R: R["grader"]["canonical"]["clusters"]["cells"]
    rep("FC1", F(fs), fs, RES); rep("MA1", g(MJ[f"med_fs{fs}"]), fs, RES); rep("MA1, eta x 1.1144", g(MJ[f"g 1.1144 f* {fs}"]), fs, RES); rep("MA1, eta x 1.206", g(MJ[f"g 1.206 f* {fs}"]), fs, RES); rep("MA1, z_obs", g(ZJ[f"g1_fs{fs}"]), fs, RES); rep("MA1, z_obs, eta x 1.1144", g(ZJ[f"g1.1144_fs{fs}"]), fs, RES)
    rep("NZ1", g(NJ[f"clusters_fs{fs}"]), fs, RES); rep("NZ1, z_obs", g(NZ[f"z_obs, eRASS1's own gas|{fs}"]), fs, RES)
json.dump(dict(provenance={f"{a}|{b[:5]}": v for (a, b), v in RP.items()}, rules=RES), open(os.path.join(HERE, "nz1_one_template_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nz1_one_template.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if d <= 1e-3 else 1)
