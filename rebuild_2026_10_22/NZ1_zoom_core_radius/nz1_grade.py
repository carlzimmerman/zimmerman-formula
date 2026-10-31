#!/usr/bin/env python3
"""NZ1_zoom_core_radius: r0 from the zooms, r0 = r_f/a with eta = (4/3) a^2/B(a); fair share only beyond r_f. FC1's full grader with MA1's mass argument and nz1_def.py injected.
    python3 nz1_grade.py            # checks, graded runs, reported runs (two single-thread workers)
    python3 nz1_grade.py --mutate   # r0 x 1.5, separate outputs
    python3 nz1_grade.py --A4       # same grade on CE1's A4 tables, separate outputs
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"
CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); MA1 = os.path.join(RB, "MA1_cluster_mass_argument")
if "--worker" in sys.argv:
    WD = os.environ["MA1_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
    INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    tail = open(os.path.join(MA1, "ma1_tail.py")).read(); e = 'exec(compile(_T1, "xh1_tail_ma1", "exec"), globals())'; assert tail.count(e) == 1
    PATCH = r'''
_a = 'Mh = math.pi * s * r0 ** 2 * float(B(min(rm, rta) / r0)); dd.append('; assert _T1.count(_a) == 1; _T1 = _T1.replace(_a, 'Mh = float(_nzf(np.array([min(rm, rta)]))[0]); dd.append(')
_a = 'k2.append(0.0 if sat else'; assert _T1.count(_a) == 1; _T1 = _T1.replace(_a, '_nzf = nz1_fn(_TBG, Mtot, s, act, Mfair, rta); _nzl = dict(NZ1_LAST); k2.append(0.0 if sat else')
_a = 'saturated=bool(sat))'; assert _T1.count(_a) == 1; _T1 = _T1.replace(_a, 'saturated=bool(sat), nz1=_nzl)')
'''
    tail = tail.replace(e, PATCH + e)
    tail = tail.replace('_OUT.update(ma1=_st,', '_g = NZ1_STAT["gam"]; _OUT["nz1"] = dict({k_: NZ1_STAT[k_] for k_ in ("cells", "no_tail", "k1a", "k1b", "k2a", "k2b")}, gam_med=float(np.median(_g)) if _g else None, gam_p16=float(np.percentile(_g, 16)) if _g else None, gam_p84=float(np.percentile(_g, 84)) if _g else None, gam_min=float(np.min(_g)) if _g else None, gam_max=float(np.max(_g)) if _g else None, mode=NZ1_MODE, r0x=NZ1_R0X)\n_OUT.update(ma1=_st,', 1)
    open(os.path.join(WD, "tail.py"), "w").write(tail)
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'nz1_def.py')!r}).read()
sub('def grade_clusters(foot, rule=True, tag="A_c2b_refit"):', _d + 'def grade_clusters(foot, rule=True, tag="A_c2b_refit"):')
sub('pp = prep(int(i), foot, hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE', 'pp = prep(int(i), foot, hk); Mtot = ma1_arg(foot, tag, pp)')
sub('r0 = solve_r0(pp["Mfair"], pp["rta"], s); Mh = math.pi * s * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)', 'Mh = nz1_fn(tag, Mtot, s, a_, pp["Mfair"], pp["rta"])(RM)')
sub('r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)', 'r0 = nz1_r0(tag, M200 / (FC1_MC if ETA_USE["v"] == ETA else 1.0), a_, lambda: solve_r0(M200 * MSUNE, R200, s)); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)')
sub('r0 = solve_r0(M200, R200, sc); rr = XG * a', 'r0 = nz1_r0("A_c2b_refit", M200 / MSUNE / (FC1_MC if ETA_USE["v"] == ETA else 1.0), act, lambda: solve_r0(M200, R200, sc)); rr = XG * a')
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", open({os.path.join(WD, 'tail.py')!r}).read())
"""
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
MUT = "--mutate" in sys.argv; A4 = "--A4" in sys.argv; PRE = "CE1_A4" if A4 else "CE1"; TAG = "nz1_MUTATE" if MUT else "nz1_a4" if A4 else "nz1"; OUT = []; TD = tempfile.mkdtemp(); FS = ("0.034", "0.0615")
def P(s): print(s, flush=True); OUT.append(s)
P(f"NZ1 {TAG}: r0 from the zooms; fair share only beyond r_f; FC1's grader, MA1's M; kappa = 1/2 FITTED; footings never pooled; not theory closed" + ("" if A4 else " [cluster masses ng 48]"))
def run(fs, mode="all", g=1.0, r0x=1.0):
    tag = f"{mode}_{fs}_{g:g}_{r0x:g}"; WD = os.path.join(TD, tag); os.makedirs(WD); T = json.load(open(os.path.join(CE1, f"{PRE}_med_fs{fs}_cf_table.json")))
    for m in ("1e+13", "1e+14"): T["cf_by_mass"][m] *= g ** 0.8
    t = os.path.join(WD, "t.json"); json.dump(T, open(t, "w")); o = os.path.join(WD, "o.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, NZ1_MODE=mode, NZ1_R0X=str(r0x), PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {tag} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-900:]}")
    r = json.load(open(o)); shutil.rmtree(WD, ignore_errors=True); return r
def summ(R, f="canonical"):
    F = R["grader"][f]; s = F["sparc"]; c = F["clusters"]["cells"]; zs = [(k, h, c[h][k]["Z"]) for h in c for k in c[h]]; w = max(zs, key=lambda t: abs(t[2]))
    return dict(keys_ok=bool(all(v["line"] for v in s.values()) and not F["failing"]), line=all(v["line"] for v in s.values()), failing=F["failing"], U=[s["A_c2b_refit"]["U_median"], s["B_cfg886_bg"]["U_median"]], rms=s["A_c2b_refit"]["rms"], groupsZ=F["groups"]["Z"], worst=w, over2=sorted({k for k, _, z in zs if abs(z) > 2}), cl_ok=not [k for k, _, z in zs if abs(z) > 2])
xok = lambda x: abs(x["mean"]) <= 0.05 and x["rms"] <= 0.10
def line(tag, R, f="canonical"):
    s = summ(R, f); x = R["footings"][f]; n = R["nz1"]
    P(f"  {tag} [{f}]: keys {'PASS' if s['keys_ok'] else 'FAIL'}; SPARC U {s['U'][0]:.3f}/{s['U'][1]:.3f} rms {s['rms']:.4f} line {s['line']}; groups Z {s['groupsZ']:+.2f}; worst {s['worst'][0]} {s['worst'][1]} {s['worst'][2]:+.2f}; over 2: {s['over2']}; failing {s['failing']}")
    P(f"     X-COP {'PASS' if xok(x) else 'FAIL'}: mean {x['mean']:+.3f} rms {x['rms']:.3f} by x " + " ".join(f"{k} {v:+.3f}" for k, v in x["by_x"].items()) + f"; band model/data {x['band']['R_X']:.3f}; gamma med {n['gam_med'] if n['gam_med'] is None else round(n['gam_med'], 3)} [{n['gam_p16'] if n['gam_p16'] is None else round(n['gam_p16'], 3)}, {n['gam_p84'] if n['gam_p84'] is None else round(n['gam_p84'], 3)}], no tail {n['no_tail']} of {n['cells']}")
def save(RES): json.dump(RES, open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    b = run("0.034"); m = run("0.034", r0x=1.5); line("base", b); line("r0 x 1.5", m); d = m["footings"]["canonical"]["rms"] - b["footings"]["canonical"]["rms"]; bites = abs(d) > 0.01
    P(f"MUTATE moves X-COP rms by {d:+.3f}: {'BITES' if bites else 'INSENSITIVE, lane UNDECIDED'}"); json.dump(dict(d=d, bites=bites), open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if bites else 1)
RES = dict(runs={}, checks={}); good = True
def fc1j(fs): return json.load(open(os.path.join(FC1, f"FC1_med_fs{fs}_x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")))["footings"]
if not A4:
    K = run("0.034", mode="off"); J = json.load(open(os.path.join(MA1, "ma1_results.json")))["runs"]["med_fs0.034"]["grader"]; f_ = ("canonical", "alt")
    dc = max(abs(K["grader"][f]["clusters"]["cells"][h][k]["pred"] - J[f]["clusters"]["cells"][h][k]["pred"]) for f in f_ for h in J[f]["clusters"]["cells"] for k in J[f]["clusters"]["cells"][h])
    ds = max(abs(K["grader"][f]["sparc"][t]["rms"] - J[f]["sparc"][t]["rms"]) for f in f_ for t in J[f]["sparc"]); dg = max(abs(K["grader"][f]["groups"]["Z"] - J[f]["groups"]["Z"]) for f in f_)
    RES["checks"]["K0"] = bool(max(dc, ds, dg) <= 1e-9); good &= RES["checks"]["K0"]; P(f"K0 rule off reproduces MA1: clusters {dc:.1e}, SPARC rms {ds:.1e}, groups Z {dg:.1e}: {'PASS' if RES['checks']['K0'] else 'FAIL'}")
with ThreadPoolExecutor(2) as ex:
    fa = {fs: ex.submit(run, fs, "all") for fs in FS}; fc = {fs: ex.submit(run, fs, "clusters") for fs in FS}; ALL = {fs: fa[fs].result() for fs in FS}; CL = {fs: fc[fs].result() for fs in FS}
for fs in FS:
    RES["runs"][f"all_fs{fs}"] = ALL[fs]; RES["runs"][f"clusters_fs{fs}"] = CL[fs]
    for lab, R in (("ALL", ALL[fs]), ("CLUSTERS", CL[fs])):
        n = R["nz1"]; ok = n["k1a"] <= 1e-9 and n["k1b"] <= 1e-9 and n["k2a"] <= 1e-6 and n["k2b"] <= 1e-9; RES["checks"][f"K1K2_{lab}_{fs}"] = bool(ok); good &= ok
        P(f"K1 K2 {lab} f* {fs}: a(eta) {n['k1a']:.1e}, M_c(r_f) {n['k1b']:.1e}, M_c(r_ta) {n['k2a']:.1e}, rho(r_f) {n['k2b']:.1e}: {'PASS' if ok else 'FAIL'}; RSS {R['rss_gb']:.2f} GB")
    if not A4:
        J = fc1j(fs); f_ = ("canonical", "alt"); d = max(max(abs(CL[fs]["grader"][f]["sparc"][t]["rms"] - J[f]["sparc"][t]["rms"]) for t in J[f]["sparc"]) for f in f_); d2 = max(abs(CL[fs]["grader"][f]["groups"]["Z"] - J[f]["groups"]["Z"]) for f in f_)
        RES["checks"][f"K3_{fs}"] = bool(max(d, d2) <= 1e-9); good &= RES["checks"][f"K3_{fs}"]; P(f"K3 f* {fs}: CLUSTERS leaves SPARC rms {d:.1e}, groups Z {d2:.1e}: {'PASS' if RES['checks'][f'K3_{fs}'] else 'FAIL'}")
if not good: P("A CHECK FAILED: no verdict"); save(RES); sys.exit(1)
for fs in FS:
    line(f"ALL f* {fs}", ALL[fs]); line(f"CLUSTERS f* {fs}", CL[fs]); line(f"ALL f* {fs}", ALL[fs], "alt")
pa = [fs for fs in FS if summ(ALL[fs])["keys_ok"] and xok(ALL[fs]["footings"]["canonical"])]; pc = [fs for fs in FS if summ(CL[fs])["keys_ok"] and xok(CL[fs]["footings"]["canonical"])]; px = [fs for fs in FS if xok(ALL[fs]["footings"]["canonical"])]
V = "NATIVE CORE PASSES ALL" if len(pa) == 2 else f"F*-DEPENDENT (passes at {pa[0]})" if pa else "CLUSTERS PASS, GALAXIES BREAK (at " + ", ".join(pc) + ")" if pc else "X-COP PASSES, KEYS BREAK: " + "; ".join(f"{fs} {summ(CL[fs])['over2'] or summ(CL[fs])['failing']}" for fs in px) if px else "NATIVE CORE FAILS: " + "; ".join(f"{fs} keys {summ(ALL[fs])['over2'] or summ(ALL[fs])['failing']}, X-COP rms {ALL[fs]['footings']['canonical']['rms']:.3f}" for fs in FS)
RES["verdict"] = V; P(("A4 READ: " if A4 else "VERDICT: ") + V)
for lab, R in (("ALL", ALL["0.034"]), ("CLUSTERS", CL["0.034"])):
    for h in ("h0672", "h0686"): P(f"all keys {lab} {h}, f* 0.034: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in R["grader"]["canonical"]["clusters"]["cells"][h].items()))
P("X-COP per cluster, ALL, f* 0.034: " + "; ".join(f"{k} mean {v:+.3f} M {ALL['0.034']['footings']['canonical']['info'][k]['logM']:.2f} r_f {ALL['0.034']['footings']['canonical']['info'][k]['nz1'].get('rf_kpc', 0):.0f} r0 {ALL['0.034']['footings']['canonical']['info'][k]['nz1'].get('r0_kpc', 0):.0f} gamma {(ALL['0.034']['footings']['canonical']['info'][k]['nz1'].get('gamma') or 0):.2f}" for k, v in ALL["0.034"]["footings"]["canonical"]["per_cluster"].items()))
save(RES)
if A4: sys.exit(0)
with ThreadPoolExecutor(2) as ex:
    fut = [(f"{m} g 1.1144 f* {fs}", ex.submit(run, fs, m, 1.1144)) for m in ("all", "clusters") for fs in FS]
    for lab, q in fut: r = q.result(); RES["runs"][lab] = r; line(lab, r); save(RES)
