#!/usr/bin/env python3
"""MA1_cluster_mass_argument (criteria b22583d196): the same collapsed mass as S's argument on the cluster path as on SPARC and groups. FC1's full grader, ma1_def.py and ma1_tail.py injected.
    python3 ma1_grade.py            # checks, graded runs, then reported runs (two single-thread workers)
    python3 ma1_grade.py --mutate   # mass argument x 2, separate outputs
    python3 ma1_grade.py --A4       # same grade on CE1's A4 tables, separate outputs
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"
CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); XH1 = os.path.join(RB, "XH1_xcop_native_rule")
if "--worker" in sys.argv:
    WD = os.environ["MA1_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
    INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
_d = open({os.path.join(HERE, 'ma1_def.py')!r}).read()
sub('def grade_clusters(foot, rule=True, tag="A_c2b_refit"):', _d + 'def grade_clusters(foot, rule=True, tag="A_c2b_refit"):')
sub('pp = prep(int(i), foot, hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE', 'pp = prep(int(i), foot, hk); Mtot = ma1_arg(foot, tag, pp)')
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", open({os.path.join(HERE, 'ma1_tail.py')!r}).read())
"""
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
MUT = "--mutate" in sys.argv; A4 = "--A4" in sys.argv; PRE = "CE1_A4" if A4 else "CE1"; TAG = "ma1_MUTATE" if MUT else "ma1_a4" if A4 else "ma1"; OUT = []; TD = tempfile.mkdtemp(); FEET = ("canonical", "alt"); FS = ("0.034", "0.0615")
def P(s): print(s, flush=True); OUT.append(s)
P(f"MA1 {TAG}: S's argument on the cluster path = M200 (model's own, fixed point); FC1's grader; kappa = 1/2 FITTED; footings never pooled; not theory closed" + ("" if A4 else " [cluster masses ng 48]"))
def run(fs, k="med", g=1.0, mode="m200", mult=1.0):
    tag = f"{k}_{fs}_{g:g}_{mode}_{mult:g}"; WD = os.path.join(TD, tag); os.makedirs(WD); T = json.load(open(os.path.join(CE1, f"{PRE}_{k}_fs{fs}_cf_table.json")))
    for m in ("1e+13", "1e+14"): T["cf_by_mass"][m] *= g ** 0.8   # eta ~ c^(5/4)
    t = os.path.join(WD, "t.json"); json.dump(T, open(t, "w")); o = os.path.join(WD, "o.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE=mode, MA1_MULT=str(mult), MA1_WD=WD, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {tag} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-800:]}")
    r = json.load(open(o)); shutil.rmtree(WD, ignore_errors=True); return r
def summ(R, f):
    F = R["grader"][f]; s = F["sparc"]; c = F["clusters"]["cells"]; zs = [(k, h, c[h][k]["Z"]) for h in c for k in c[h]]; w = max(zs, key=lambda t: abs(t[2]))
    return dict(ok=bool(all(v["line"] for v in s.values()) and not F["failing"]), line=all(v["line"] for v in s.values()), failing=F["failing"], U=[s["A_c2b_refit"]["U_median"], s["B_cfg886_bg"]["U_median"]], rms=s["A_c2b_refit"]["rms"], groupsZ=F["groups"]["Z"], worst=w,
                inmall=[c["h0672"]["G-IN-Mall"]["Z"], c["h0686"]["G-IN-Mall"]["Z"]], t3=[c["h0672"]["G-MID-T3"]["Z"], c["h0686"]["G-MID-T3"]["Z"]], over2=sorted({k for k, _, z in zs if abs(z) > 2}))
def line(tag, R, f="canonical"):
    s = summ(R, f); x = R["footings"][f]
    P(f"  {tag} [{f}]: {'PASS' if s['ok'] else 'FAIL'}; SPARC U {s['U'][0]:.3f}/{s['U'][1]:.3f} rms {s['rms']:.4f}; groups Z {s['groupsZ']:+.2f}; worst {s['worst'][0]} {s['worst'][1]} {s['worst'][2]:+.2f}; G-IN-Mall {s['inmall'][0]:+.2f}/{s['inmall'][1]:+.2f}; G-MID-T3 {s['t3'][0]:+.2f}/{s['t3'][1]:+.2f}; over 2: {s['over2']}; failing {s['failing']}")
    P(f"     X-COP mean {x['mean']:+.3f} rms {x['rms']:.3f} by x " + " ".join(f"{k} {v:+.3f}" for k, v in x["by_x"].items()) + f"; band model/data {x['band']['R_X']:.3f}; {'PASS' if abs(x['mean']) <= 0.05 and x['rms'] <= 0.10 else 'FAIL'}" + (f"; M200/M_ta {R['ma1']['ratio_med']:.3f} [{R['ma1']['ratio_min']:.3f}, {R['ma1']['ratio_max']:.3f}], S/S_FC1 {R['ma1']['sratio_med']:.3f} [{R['ma1']['sratio_min']:.3f}, {R['ma1']['sratio_max']:.3f}]" if R["ma1"].get("ratio_med") else ""))
if MUT:
    b = run("0.034"); m = run("0.034", mult=2.0); line("base", b); line("argument x 2", m); d = summ(m, "canonical")["inmall"][0] - summ(b, "canonical")["inmall"][0]; bites = abs(d) > 0.05
    P(f"MUTATE moves G-IN-Mall by {d:+.3f}: {'BITES' if bites else 'INSENSITIVE, lane UNDECIDED'}"); json.dump(dict(d=d, bites=bites), open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if bites else 1)
RES = dict(runs={}, checks={})
def fc1j(fs): return json.load(open(os.path.join(FC1, f"FC1_med_fs{fs}_x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")))["footings"]
good = True
if not A4:
    K = run("0.034", mode="off"); J = fc1j("0.034"); dc = max(abs(K["grader"][f]["clusters"]["cells"][h][k]["pred"] - J[f]["clusters"]["cells"][h][k]["pred"]) for f in FEET for h in J[f]["clusters"]["cells"] for k in J[f]["clusters"]["cells"][h])
    ds = max(abs(K["grader"][f]["sparc"][t]["rms"] - J[f]["sparc"][t]["rms"]) for f in FEET for t in J[f]["sparc"]); dg = max(abs(K["grader"][f]["groups"]["Z"] - J[f]["groups"]["Z"]) for f in FEET)
    XJ = json.load(open(os.path.join(XH1, "xh1_results.json")))["runs"]["g1_fs0.034"]["footings"]["canonical"]; dx = max(abs(K["footings"]["canonical"][q] - XJ[q]) for q in ("mean", "rms"))
    RES["checks"]["K0"] = bool(max(dc, ds, dg) <= 1e-9 and dx <= 1e-9); good &= RES["checks"]["K0"]; P(f"K0 switch off reproduces FC1: clusters {dc:.1e}, SPARC rms {ds:.1e}, groups Z {dg:.1e}; XH1's X-COP {dx:.1e}: {'PASS' if RES['checks']['K0'] else 'FAIL'}")
G = {fs: run(fs) for fs in FS}
for fs in FS:
    RES["runs"][f"med_fs{fs}"] = G[fs]; st = G[fs]["ma1"]; J = fc1j(fs)
    if not A4:
        d1 = max(max(abs(G[fs]["grader"][f]["sparc"][t]["rms"] - J[f]["sparc"][t]["rms"]) for t in J[f]["sparc"]) for f in FEET); d2 = max(abs(G[fs]["grader"][f]["groups"]["Z"] - J[f]["groups"]["Z"]) for f in FEET)
        RES["checks"][f"K1_{fs}"] = bool(max(d1, d2) <= 1e-9); good &= RES["checks"][f"K1_{fs}"]; P(f"K1 f* {fs}: SPARC rms {d1:.1e}, groups Z {d2:.1e}: {'PASS' if RES['checks'][f'K1_{fs}'] else 'FAIL'}")
    k2 = st["nonconv"] == 0 and st["k2"] <= 1e-6; k3 = st["over"] == 0; RES["checks"][f"K2_{fs}"] = bool(k2); RES["checks"][f"K3_{fs}"] = bool(k3); good &= k2 and k3
    P(f"K2 f* {fs}: {st['cells']} cells, {st['nonconv']} not converged, most iterations {st['maxit']}, R200 equation {st['k2']:.1e}: {'PASS' if k2 else 'FAIL'}; K3 M200 >= M_ta in {st['over']}: {'PASS' if k3 else 'FAIL'}; RSS {G[fs]['rss_gb']:.2f} GB")
def save(): json.dump(RES, open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if not good: P("A CHECK FAILED: no verdict"); save(); sys.exit(1)
for fs in FS:
    for f in FEET: line(f"f* {fs}", G[fs], f)
def verdict(f):
    n = [fs for fs in FS if summ(G[fs], f)["ok"]]
    return "MASS ARGUMENT PASS" if len(n) == 2 else f"F*-DEPENDENT (passes at {n[0]})" if n else "MASS ARGUMENT FAIL: " + "; ".join(f"{fs} {summ(G[fs], f)['over2'] or summ(G[fs], f)['failing']}" for fs in FS)
RES["verdict"] = {f: verdict(f) for f in FEET}; P(("A4 READ canonical: " if A4 else "VERDICT canonical: ") + RES["verdict"]["canonical"]); P("alt, reported: " + RES["verdict"]["alt"])
P("all keys h 0.672, f* 0.034, this rule vs FC1: " + "; ".join(f"{k} {v['Z']:+.2f} ({fc1j('0.034')['canonical']['clusters']['cells']['h0672'][k]['Z']:+.2f})" for k, v in G["0.034"]["grader"]["canonical"]["clusters"]["cells"]["h0672"].items()))
P("all keys h 0.686, f* 0.034, this rule vs FC1: " + "; ".join(f"{k} {v['Z']:+.2f} ({fc1j('0.034')['canonical']['clusters']['cells']['h0686'][k]['Z']:+.2f})" for k, v in G["0.034"]["grader"]["canonical"]["clusters"]["cells"]["h0686"].items()))
save()
if A4: sys.exit(0)
JOBS = [(f"{k} f* {fs}", dict(fs=fs, k=k)) for k in ("p16", "p84") for fs in FS] + [(f"g {g:g} f* {fs}", dict(fs=fs, g=g)) for g in (1.1144, 1.206) for fs in FS] + [(f"M at 18 pi^2 rho_m f* {fs}", dict(fs=fs, mode="m178m")) for fs in FS]
with ThreadPoolExecutor(2) as ex:
    fut = [(lab, ex.submit(run, **kw)) for lab, kw in JOBS]
    for lab, q in fut: r = q.result(); RES["runs"][lab] = r; line(lab, r); save()
n = [fs for fs in FS if summ(RES["runs"][f"M at 18 pi^2 rho_m f* {fs}"], "canonical")["ok"]]; m = [fs for fs in FS if summ(G[fs], "canonical")["ok"]]
RES["definition_dependent"] = n != m; P(f"definition sensitivity: M200 passes at {m}, 18 pi^2 rho_m passes at {n}: {'DEFINITION-DEPENDENT' if n != m else 'label unchanged'}"); save()
