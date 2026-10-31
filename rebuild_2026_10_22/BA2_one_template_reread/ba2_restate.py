#!/usr/bin/env python3
"""BA2_one_template_reread (criteria e30f1b461b): X71, GS1, X73, GX2, and FC1, MA1, NZ1 at ng 64, with G-OUT-Mall and G-OUT-M1..M3 on the run's own template, per key and by BA1's joint chi^2.
Each run executes that lane's own script text with asserted string replacements; writes go to a temporary directory.
    python3 ba2_restate.py --run      # every run: an idle driver and three workers, one thread each, nice 15; resumes from runs/
    python3 ba2_restate.py --grade    # checks, restatement, labels, story: ba2.out, ba2_results.json
    python3 ba2_restate.py --mutate   # the restate step reads the terciles reversed; K1 and K2 must fail: ba2_MUTATE.out, ba2_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, shutil, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); RUNS = os.path.join(HERE, "runs")
SM, S16, S84 = "2.7774425603108597", "2.675568930042712", "3.0711023902445302"; NM = {SM: "s2.7774", S16: "s2.6756", S84: "s3.0711"}
FS = ("0.034", "0.0615"); HH = ("h0672", "h0686"); FEET = ("canonical", "alt"); KEYS4 = ["G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3"]
HERE_LINE = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'
X71D, X73D, GS1D, GX2D, FC1D, MA1D, NZ1D, CE1D, BA1D = "X71_smooth_core_measured_fstar", "X73_smooth_core_all_measured", "GS1_measured_gas_outskirts", "GX2_infall_corrected_gas", "FC1_cold_share_native_eta", "MA1_cluster_mass_argument", "NZ1_zoom_core_radius", "CE1_converged_eta_grade", "BA1_joint_shear_statistic"
JOBS = {}
def job(tag, **kw): JOBS[tag] = kw
job("k1_fc1_0.034", lane="fc1", table="CE1_med_fs0.034_cf_table.json", fs="0.034", ref=[f"{FC1D}/FC1_med_fs0.034_x74_results_fs0.034_nat_s2.7774.json"])
job("k1_ma1_0.0615", lane="ma1", table="CE1_med_fs0.0615_cf_table.json", fs="0.0615", ref=[f"{MA1D}/ma1_results.json", "med_fs0.0615"])
job("k1_nz1_0.034", lane="nz1", table="CE1_med_fs0.034_cf_table.json", fs="0.034", ref=[f"{NZ1D}/nz1_results.json", "clusters_fs0.034"])
job("x71_S_0.2", lane="x71", fs="0.2", shape="S", ref=[f"{X71D}/x71_results_fs0.2_S.json"])
for fs in FS:
    for sh in ("S", "B"): job(f"x71_{sh}_{fs}", lane="x71", fs=fs, shape=sh, ref=[f"{X71D}/x71_results_fs{fs}_{sh}.json"])
    for sl in (SM, S16, S84): job(f"x73_S_nat_{NM[sl]}_{fs}", lane="x73", fs=fs, shape="S", native="1", slope=sl, ref=[f"{X73D}/x73_results_fs{fs}_S_nat_{NM[sl]}.json"])
    job(f"x73_S_nat_notail_{fs}", lane="x73", fs=fs, shape="S", native="1", slope="none", ref=[f"{X73D}/x73_results_fs{fs}_S_nat_notail.json"])
    job(f"x73_S_inh_s2.7774_{fs}", lane="x73", fs=fs, shape="S", native="0", slope=SM, ref=[f"{X73D}/x73_results_fs{fs}_S_inh_s2.7774.json"])
    job(f"x73_B_nat_s2.7774_{fs}", lane="x73", fs=fs, shape="B", native="1", slope=SM, ref=[f"{X73D}/x73_results_fs{fs}_B_nat_s2.7774.json"])
job("x73_S_nat_s2.7774_0.2", lane="x73", fs="0.2", shape="S", native="1", slope=SM, ref=[f"{X73D}/x73_results_fs0.2_S_nat_s2.7774.json"])
job("x73_B_nat_s2.7774_0.2", lane="x73", fs="0.2", shape="B", native="1", slope=SM, ref=[f"{X73D}/x73_results_fs0.2_B_nat_s2.7774.json"])
for r in ("R4", "R5", "RX48"):
    for lab, sl in (("meas", SM), ("s16", S16), ("s84", S84)): job(f"gs1_{r}_{lab}", lane="gs1", rule=r, slope=sl, ref=[f"{GS1D}/runs/x43copy_{r}_{lab}_results.json"])
for tg, edge, fac in (("rsp", 0.364, "c"), ("rta", 1.0, "c"), ("bur", None, "c"), ("rsp_m", 0.364, "m"), ("rsp_p", 0.364, "p")): job(f"gx2_{tg}", lane="gx2", tg=tg, edge=edge, fac=fac, ref=[f"{GX2D}/runs/x43copy_gx2_{tg}_results.json"])
for k in ("med", "p16", "p84"):
    for fs in FS: job(f"fc1_a4_{k}_{fs}", lane="fc1", table=f"CE1_A4_{k}_fs{fs}_cf_table.json", fs=fs, ref=[f"{FC1D}/FC1_A4_{k}_fs{fs}_x74_results_fs{fs}_nat_s2.7774.json"])
for fs in FS:
    job(f"ma1_a4_{fs}", lane="ma1", table=f"CE1_A4_med_fs{fs}_cf_table.json", fs=fs, ref=[f"{MA1D}/ma1_a4_results.json", f"med_fs{fs}"])
    job(f"nz1_a4_{fs}", lane="nz1", table=f"CE1_A4_med_fs{fs}_cf_table.json", fs=fs, ref=[f"{NZ1D}/nz1_a4_results.json", f"clusters_fs{fs}"])
# ------------------------------------------------------------------ worker: that lane's own text, asserted replacements only
def sub1(T, a, b):
    assert T.count(a) == 1, a[:80]
    return T.replace(a, b)
TAIL = 'exec(open(os.environ["BA2_COLLECT"]).read(), globals()); json.dump(ba2_collect(globals()), open(os.environ["BA2_O"], "w"), indent=1, default=float); sys.exit(0)'
EXTRA_OLD = '    extra = {"log": list(ns["NX"].get("GC2_LOG", []))[:N_LOG], "rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9}'
EXTRA_NEW = '    exec(open(os.environ["BA2_COLLECT"]).read(), ns); extra = {"BA2": ns["ba2_collect"](ns)}'
GS1CUT = "# ============================================================== A. measurement"
def worker():
    tag = os.environ["BA2_TAG"]; WD = os.environ["BA2_WD"]; sp = JOBS[tag]; lane = sp["lane"]; os.environ["BA2_COLLECT"] = os.path.join(HERE, "ba2_collect.py"); O = os.path.join(WD, "o.json"); os.environ["BA2_O"] = O; os.environ.pop("XH1_K0_REF", None); XC = None
    class Q:
        v = None
        def put(self, x): Q.v = x
    if lane == "x71":
        F = os.path.join(RB, X71D, "x71_fstar.py"); T = sub1(open(F).read(), HERE_LINE, f"HERE = {WD!r}; REB = {RB!r}"); T = sub1(T, "sys.exit(0 if n == len(checks) else 1)", TAIL); os.environ.update(X71_FSTAR=sp["fs"], X71_SHAPE=sp["shape"]); sys.argv = [F]
        try: exec(compile(T, F, "exec"), {"__file__": os.path.join(WD, "x71_fstar.py"), "__name__": "__main__"})
        except SystemExit: pass
    elif lane == "x73":
        F = os.path.join(RB, X73D, "x73_all_measured.py"); T = sub1(open(F).read(), HERE_LINE, f"HERE = {WD!r}; REB = {RB!r}"); T = sub1(T, "sys.exit(0 if n == len(checks) else 1)", TAIL); os.environ.update(X73_FSTAR=sp["fs"], X73_SHAPE=sp["shape"], X73_NATIVE=sp["native"], X73_SLOPE=sp["slope"]); sys.argv = [F]
        try: exec(compile(T, F, "exec"), {"__file__": os.path.join(WD, "x73_all_measured.py"), "__name__": "__main__"})
        except SystemExit: pass
    elif lane == "gs1":
        F = os.path.join(RB, GS1D, "gs1_gas_slope.py"); src = open(F).read(); src = src[:src.index(GS1CUT)]; src = sub1(src, HERE_LINE, f"HERE = {WD!r}; REB = {RB!r}"); src = sub1(src, EXTRA_OLD, EXTRA_NEW)
        G = {"__file__": os.path.join(WD, "gs1_ro.py"), "__name__": "gs1_ro"}; exec(compile(src, F, "exec"), G); G["_child"](sp["rule"], True, True, "R5", False, tag, Q(), float(sp["slope"])); json.dump(Q.v["BA2"], open(O, "w"), indent=1, default=float)
    elif lane == "gx2":
        F = os.path.join(RB, GX2D, "gx2_corrected_gas.py"); T = open(F).read(); SIGL = re.search(r"^SIG = float\(.*$", T, re.M).group(0); T = T[:T.index('RES = dict(criteria="c6783290b3"')]
        T = sub1(T, 'HB = os.path.dirname(os.path.abspath(__file__)); RB_ = os.path.dirname(HB); REPO_ = os.path.dirname(RB_)', f"HB = {WD!r}; RB_ = {RB!r}; REPO_ = os.path.dirname(RB_)")
        a = f'src = open(GSP).read(); src = src[:src.index("{GS1CUT}")]'; T = sub1(T, a, a + f"\nassert src.count({HERE_LINE!r}) == 1 and src.count({EXTRA_OLD!r}) == 1; src = src.replace({HERE_LINE!r}, {f'HERE = {WD!r}; REB = {RB!r}'!r}).replace({EXTRA_OLD!r}, {EXTRA_NEW!r})")
        T = sub1(T, '_, r = G1["run"]("R4", True, True, shape="R5", tag=tag, slope=S_MEAS)', 'G1["_child"]("R4", True, True, "R5", False, tag, BA2Q(), S_MEAS); r = json.load(open(os.path.join(G1["RUND"], f"x43copy_{tag}_results.json")))')
        ns = {"__file__": F, "__name__": "gx2_ro", "BA2Q": Q}; exec(compile(T + "\n" + SIGL + "\n", F, "exec"), ns); fac = {"c": ns["FAC0"], "m": 10 ** (0.111 - ns["SIG"]), "p": 10 ** (0.111 + ns["SIG"])}[sp["fac"]]
        ns["grade"](sp["tg"], sp["edge"], f"gx2_{sp['tg']}", fac); json.dump(Q.v["BA2"], open(O, "w"), indent=1, default=float)
    elif lane == "fc1":
        X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read(); INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(RB, FC1D, "fc1_x74.py")).read(), re.S).group(1); TX = sub1(TX, HERE_LINE, f"HERE = {WD!r}; REB = {RB!r}")
        MY = f"""
sub({HERE_LINE!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", {TAIL!r})
"""
        TX = sub1(TX, "sys.argv = [SRC]\n", INJ + MY + "sys.argv = [SRC]\n"); os.environ.update(FC1_MODE="cold", X74_CF=os.path.join(RB, CE1D, sp["table"]), X73_FSTAR=sp["fs"], X73_SLOPE=SM); sys.argv = [X74F]
        try: exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
        except SystemExit: pass
    else:   # ma1, nz1: their --worker block, one line added as nz1_common_gas.py adds it
        F = os.path.join(RB, MA1D, "ma1_grade.py") if lane == "ma1" else os.path.join(RB, NZ1D, "nz1_grade.py"); a = '    A = "sys.argv = [SRC]\\n"; assert TX.count(A) == 1'; T = sub1(open(F).read(), a, '    MY += open(os.environ["BA2_XFILE"]).read()\n' + a); XO = os.path.join(WD, "x.json")
        xf = os.path.join(WD, "x.py"); open(xf, "w").write("""sub('_OUT.update(ma1=_st,', 'exec(open(os.environ["BA2_COLLECT"]).read(), globals()); _OUT["BA2"] = ba2_collect(globals())\\n_OUT.update(ma1=_st,')\n""")
        os.environ.update(FC1_MODE="cold", X74_CF=os.path.join(RB, CE1D, sp["table"]), X73_FSTAR=sp["fs"], X73_SLOPE=SM, XH1_OUT=XO, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, BA2_XFILE=xf)
        if lane == "nz1": os.environ.update(NZ1_MODE="clusters", NZ1_R0X="1")
        sys.argv = [F, "--worker"]
        try: exec(compile(T, F, "exec"), {"__file__": F, "__name__": "__main__"})
        except SystemExit: pass
        R = json.load(open(XO)); XC = {k: R["footings"]["canonical"][k] for k in ("mean", "rms", "by_x")}; json.dump(R["BA2"], open(O, "w"), indent=1, default=float)
    R = json.load(open(O)); R.update(tag=tag, lane=lane, spec={k: v for k, v in sp.items() if k != "ref"}, xcop=XC); t = os.path.join(RUNS, f".{tag}.tmp"); json.dump(R, open(t, "w"), indent=1, default=float); os.replace(t, os.path.join(RUNS, f"{tag}.json"))
if "--worker" in sys.argv:
    worker(); sys.exit(0)
# ------------------------------------------------------------------ driver
READ_LANES = [X71D, X73D, GS1D, GX2D, FC1D, MA1D, NZ1D, CE1D, BA1D, "X74_all_measured_native_cf", "X43_collapse_core_floor", "X30_sheet_cluster_profile", "X2_cluster_outskirts", "X7_cluster_core_significance", "EM1_emergent_dust_law", "XH1_xcop_native_rule", "CS2_core_law_out_of_sample", "F2_outer_lensing", "P4_v3_galaxy_tiles", "X70_smooth_core_shape", "F3_growth_audit"]
def snapshot():
    """Tracked or untracked changes, and every file's mtime, in the lanes these runs read. *.md is left out: no run writes one, and other sessions annotate READMEs."""
    st = subprocess.run(["git", "status", "--porcelain", "--"] + [os.path.join(RB, d) for d in READ_LANES], cwd=REPO, capture_output=True, text=True).stdout.splitlines(); mt = {}
    for d in READ_LANES:
        for root, _, fn in os.walk(os.path.join(RB, d)):
            for f_ in fn:
                if not f_.endswith(".md"): p = os.path.join(root, f_); mt[os.path.relpath(p, RB)] = os.path.getmtime(p)
    return dict(status=sorted(x for x in st if not x.endswith(".md")), mtime=mt)
if "--run" in sys.argv:
    os.makedirs(RUNS, exist_ok=True); bl = os.path.join(RUNS, "_baseline.json")
    if not os.path.exists(bl): json.dump(snapshot(), open(bl, "w"))
    only = [a[7:] for a in sys.argv if a.startswith("--only=")]; TD = tempfile.mkdtemp()
    def launch(tag):
        out = os.path.join(RUNS, f"{tag}.json")
        if os.path.exists(out): return tag, "cached", 0.0
        WD = os.path.join(TD, tag); os.makedirs(WD); t0 = time.time(); env = dict(os.environ, BA2_TAG=tag, BA2_WD=WD, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1")
        p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
        if not os.path.exists(out): open(os.path.join(RUNS, f"{tag}.err"), "w").write(p.stdout[-3000:] + "\n" + p.stderr[-6000:]); return tag, f"FAILED exit {p.returncode}", time.time() - t0
        shutil.rmtree(WD, ignore_errors=True); return tag, "ok", time.time() - t0
    tags = [t for t in JOBS if not only or any(t.startswith(o) for o in only)]; bad = 0
    with ThreadPoolExecutor(3) as ex:
        for tag, st, dt in ex.map(launch, tags): print(f"{time.strftime('%H:%M:%S')} {tag}: {st} [{dt:.0f} s]", flush=True); bad += st.startswith("FAILED")
    shutil.rmtree(TD, ignore_errors=True); print(f"runs done: {len(tags) - bad} of {len(tags)}", flush=True); sys.exit(1 if bad else 0)
# ------------------------------------------------------------------ grade
import numpy as np
from scipy.stats import chi2
MUT = "--mutate" in sys.argv; TAG = "ba2_MUTATE" if MUT else "ba2"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def jl(rel): return json.load(open(os.path.join(RB, rel)))
_T = open(os.path.join(RB, BA1D, "ba1_grade.py")).read(); NSJ = {"np": np, "chi2": chi2}; exec(_T[_T.index("def joint(cells, RJ, h"):_T.index('P("BA1 joint chi^2')], NSJ); joint, jlabel = NSJ["joint"], NSJ["label"]
BA1 = jl(f"{BA1D}/ba1_results.json"); R_ORIG, R_GAS = BA1["R_orig"], BA1["R_gas"]; OT = jl(f"{NZ1D}/nz1_one_template_results.json")
RUN = {t: json.load(open(os.path.join(RUNS, f"{t}.json"))) for t in JOBS if os.path.exists(os.path.join(RUNS, f"{t}.json"))}; missing = [t for t in JOBS if t not in RUN]
if missing: raise SystemExit(f"NOT DECIDED: runs missing: {missing}")
def restate(cells, mo, foot, mut=False):
    """zn1_grade.py's cells(): the same predictions, the four measured values on the run's own template, s scaled by A/meas."""
    O = {}
    for h in HH:
        q = mo[f"{foot}|{h}"]; O[h] = {k: dict(v) for k, v in cells[h].items()}; terc = q["terc"][::-1] if mut else q["terc"]
        for k, A in zip(KEYS4, [q["all"]] + terc):
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
def over2(c): return sorted({k for h in HH for k, v in c[h].items() if abs(v["Z"]) > 2})
def fails_of(c):
    """X43's grade_clusters text."""
    bad = [k for k in c["h0672"] if not all(abs(c[h][k]["Z"]) <= 2 for h in HH)]
    return [f"{k} ({'OVER' if c['h0672'][k]['pred'] > c['h0672'][k]['meas'] else 'UNDER'})" for k in bad]
def worst(c): return max(((k, h, c[h][k]["Z"]) for h in HH for k in c[h]), key=lambda t: abs(t[2]))
def failing_of(ft, c): return [x for x in ft["failing"] if not x.startswith("G-")] + fails_of(c)
def lines_ok(ft): return all(v["line"] for v in ft["sparc"].values())
FRZ = {t: {f: RUN[t]["footings"][f]["cells"] for f in FEET} for t in RUN}; ONE = {t: {f: restate(FRZ[t][f], RUN[t]["M_outer"], f, MUT) for f in FEET} for t in RUN}
good = True; CHK = {}
def check(name, ok, msg):
    global good
    CHK[name] = dict(ok=bool(ok), msg=msg); good &= bool(ok); P(f"{name} {msg}: {'PASS' if ok else 'FAIL'}")
P(f"BA2 {TAG}: four shear keys on the run's own template, criteria e30f1b461b; kappa = 1/2 FITTED; footings never pooled; not theory closed" + ("; MUTATE: terciles reversed in the restate step, control output, not physics" if MUT else ""))
# K1
def cdiff(a, b, keys=("meas", "s", "pred", "Z")): return max(abs(a[h][k][q] - b[h][k][q]) for h in HH for k in b[h] for q in keys)
dk1 = {n: cdiff(ONE[t]["canonical"], OT["rules"][n]["cells"]) for t, n in (("k1_fc1_0.034", "FC1|0.034"), ("k1_ma1_0.0615", "MA1|0.0615"), ("k1_nz1_0.034", "NZ1|0.034"))}
k1 = max(dk1.values()) <= 1e-9; check("K1", k1, "restating FC1|0.034, MA1|0.0615, NZ1|0.034 at ng 48 reproduces nz1_one_template_results.json: " + ", ".join(f"{k} {v:.1e}" for k, v in dk1.items()))
# K2
r = RUN["x71_S_0.2"]; dA = max(max(abs(q["all"] - q["x7_all"]), *[abs(a - b) for a, b in zip(q["terc"], q["x7_terc"])]) for q in r["M_outer"].values()); dZ = max(abs(ONE["x71_S_0.2"][f][h][k]["Z"] - FRZ["x71_S_0.2"][f][h][k]["Z"]) for f in FEET for h in HH for k in KEYS4)
k2 = max(dA, dZ) <= 1e-9; check("K2", k2, f"f* 0.20, no tail: A against A_CAL {dA:.1e}, restated against frozen Z {dZ:.1e}")
# K3
def ref_foot(t, f):
    p = JOBS[t]["ref"]; J = jl(p[0])
    return J["runs"][p[1]]["grader"][f] if len(p) == 2 else J["footings"][f]
dk3 = {}; dfl = 0; dx = 0.0
for t in RUN:
    for f in FEET:
        G = ref_foot(t, f); dk3[f"{t}|{f}"] = cdiff(FRZ[t][f], G["clusters"]["cells"]); dfl += RUN[t]["footings"][f]["fails"] != G["clusters"]["fails"]; dfl += RUN[t]["footings"][f]["failing"] != G["failing"]
    if RUN[t]["xcop"]: p = JOBS[t]["ref"]; X = jl(p[0])["runs"][p[1]]["footings"]["canonical"]; dx = max(dx, abs(RUN[t]["xcop"]["mean"] - X["mean"]), abs(RUN[t]["xcop"]["rms"] - X["rms"]))
wk = max(dk3, key=dk3.get); k3 = dk3[wk] <= 1e-9 and dfl == 0 and dx <= 1e-9; check("K3", k3, f"{len(RUN)} re-runs reproduce the committed frozen read, 15 keys, both footings, both h: max |d| {dk3[wk]:.1e} ({wk}); fails/failing lists differing {dfl}; X-COP {dx:.1e}")
# K4
J0 = BA1["results"]["MA1 f* 0.034"]["cells"]; c = OT["rules"]["MA1|0.034"]["cells"]; d4 = max(abs(joint(c, R_ORIG, h)[0] - J0[h][0]) for h in HH); q = RUN["x73_S_nat_s2.7774_0.034"]["R_own"]; d4b = max(float(np.max(np.abs(np.array(q[h][k]) - np.array(R_ORIG[h][k])))) for h in HH for k in ("R_boot", "R_jack"))
k4 = d4 <= 1e-9 and d4b <= 1e-9; check("K4", k4, f"BA1's chi^2 for MA1 f* 0.034 from its committed cells {d4:.1e}; R from X73 PRIMARY f* 0.034 against BA1's R_orig {d4b:.1e}")
# K5
def mdiff(a, b):
    A, B = RUN[a]["M_outer"], RUN[b]["M_outer"]; return max(max(abs(A[c]["all"] - B[c]["all"]), *[abs(x - y) for x, y in zip(A[c]["terc"], B[c]["terc"])]) for c in A)
pairs = [(f"x71_S_{fs}", f"x71_B_{fs}") for fs in FS] + [(f"gs1_R4_{l}", f"gs1_{r}_{l}") for l in ("meas", "s16", "s84") for r in ("R5", "RX48")] + [("gx2_rsp", "gx2_rta"), ("gx2_rsp", "gx2_bur"), ("x73_S_nat_s2.7774_0.2", "gs1_R4_meas"), ("x73_S_nat_s2.7774_0.2", "x73_B_nat_s2.7774_0.2")]
for fs in FS: pairs += [(f"x73_S_nat_s2.7774_{fs}", f"fc1_a4_med_{fs}"), (f"x73_S_nat_s2.7774_{fs}", f"ma1_a4_{fs}"), (f"x73_S_nat_s2.7774_{fs}", f"nz1_a4_{fs}"), (f"x73_S_nat_s2.7774_{fs}", f"x73_B_nat_s2.7774_{fs}"), (f"fc1_a4_med_{fs}", f"fc1_a4_p16_{fs}"), (f"fc1_a4_med_{fs}", f"fc1_a4_p84_{fs}")]
pairs += [("x73_S_nat_s2.7774_0.034", "k1_fc1_0.034"), ("x73_S_nat_s2.7774_0.0615", "k1_ma1_0.0615")]
d5 = {f"{a} / {b}": mdiff(a, b) for a, b in pairs}; w5 = max(d5, key=d5.get); pv = OT["provenance"]; d5p = max(max(abs(RUN[f"fc1_a4_med_{fs}"]["M_outer"][c]["all"] - pv[f"{fs}|2.777"][c]["all"]), *[abs(x - y) for x, y in zip(RUN[f"fc1_a4_med_{fs}"]["M_outer"][c]["terc"], pv[f"{fs}|2.777"][c]["terc"])]) for fs in FS for c in pv[f"{fs}|2.777"])
k5 = d5[w5] <= 1e-12 and d5p <= 1e-12; check("K5", k5, f"template independent of the rule, {len(pairs)} pairs: max |d| {d5[w5]:.1e} ({w5}); against nz1's provenance {d5p:.1e}")
# ------------------------------------------------------------------ labels, each lane's own frozen rule
def x71_label(C):
    parts = [f"{x} at f* {fs}" for fs in FS for x in fails_of(C[fs])]; return dict(cls="SURVIVES" if not parts else "BREAKS", named=parts)
def gs1_label(C, f):
    fl = {f"{r}_{l}": ([] if lines_ok(RUN[f"gs1_{r}_{l}"]["footings"][f]) else ["SPARC line"]) + ([] if RUN[f"gs1_{r}_{l}"]["footings"][f]["groups"]["PASS"] else [f"groups Z {RUN[f'gs1_{r}_{l}']['footings'][f]['groups']['Z']:+.2f}"]) + fails_of(C[f"gs1_{r}_{l}"]) for r in ("R4", "R5", "RX48") for l in ("meas", "s16", "s84")}
    ps = [r for r in ("R4", "R5", "RX48") if not fl[f"{r}_meas"]]; rob = {r: (not fl[f"{r}_s16"], not fl[f"{r}_s84"]) for r in ps}
    v = ("MEASURED SLOPE PASSES (" + ", ".join(ps) + ")") if ps else "MEASURED SLOPE FAILS"
    if ps: v += " " + ("ROBUST" if all(all(x) for x in rob.values()) else "FRAGILE (bootstrap edges: " + "; ".join(f"{k} s16 {a} s84 {b}" for k, (a, b) in rob.items()) + ")")
    return dict(cls=v, named=fl)
_S = open(os.path.join(RB, X73D, "x73_summary.py")).read()
def x73_label(C, f):
    def J_(t):
        m = re.fullmatch(r"fs([\d.]+)_S_nat_(s[\d.]+)", t); r = RUN[f"x73_S_nat_{m.group(2)}_{m.group(1)}"]; return dict(footings={g: dict(clusters=dict(cells=C[f"x73_S_nat_{m.group(2)}_{m.group(1)}"][g]), sparc=r["footings"][g]["sparc"], groups=r["footings"][g]["groups"]) for g in FEET})
    ns = {"J": J_, "HK": HH}; exec(_S[_S.index("def grade(r, f):"):_S.index('OUT = {"criteria"')], ns)
    v, det = ns["cls"](FS, "s2.7774", f); edges = {s: ns["cls"](FS, s, f)[0] for s in ("s2.6756", "s3.0711")}
    same = all(e.split(":")[0] == v.split(":")[0] and (e == v or not v.startswith("ALL-MEASURED PASSES")) for e in edges.values())
    return dict(cls=v.split(":")[0] + ", " + ("ROBUST" if same else "FRAGILE"), named=dict(verdict=v, edges=edges), verdict=v, robust="ROBUST" if same else "FRAGILE")
def gx2_label(c):
    fl = fails_of(c); return dict(cls="INFALL HALO + CORRECTED GAS PASSES CLUSTERS" if not fl else "LENSING STILL FAILS", named=fl)
def fc1_label(C, f, pre="fc1_a4"):
    ok = lambda k, fs: not failing_of(RUN[f"{pre}_{k}_{fs}"]["footings"][f], C[f"{pre}_{k}_{fs}"]); med = [ok("med", fs) for fs in FS]; ends = [ok(k, fs) for fs in FS for k in ("p16", "p84")]
    return dict(cls="COLD-SHARE PASS" if all(med) and all(ends) else "KNIFE EDGE" if all(med) else "F*-DEPENDENT" if any(med) else "COLD-SHARE FAIL", named={fs: failing_of(RUN[f"{pre}_med_{fs}"]["footings"][f], C[f"{pre}_med_{fs}"]) for fs in FS}, ends=ends)
def ma1_verdict(C, f):
    ok = {fs: not failing_of(RUN[f"ma1_a4_{fs}"]["footings"][f], C[f"ma1_a4_{fs}"]) for fs in FS}; n = [fs for fs in FS if ok[fs]]
    v = "MASS ARGUMENT PASS" if len(n) == 2 else f"F*-DEPENDENT (passes at {n[0]})" if n else "MASS ARGUMENT FAIL: " + "; ".join(f"{fs} {over2(C[f'ma1_a4_{fs}']) or failing_of(RUN[f'ma1_a4_{fs}']['footings'][f], C[f'ma1_a4_{fs}'])}" for fs in FS)
    return dict(cls=v.split(":")[0], named=v)
NZA = jl(f"{NZ1D}/nz1_a4_results.json")
d_all = max(abs(NZA["runs"][f"all_fs{fs}"]["grader"][f]["clusters"]["cells"][h][k]["pred"] - NZA["runs"][f"clusters_fs{fs}"]["grader"][f]["clusters"]["cells"][h][k]["pred"]) for fs in FS for f in FEET for h in HH for k in NZA["runs"][f"all_fs{fs}"]["grader"][f]["clusters"]["cells"][h])
def nz1_verdict(C):
    """nz1_grade.py's V. ALL's cluster cells equal CLUSTERS's, |d| checked; SPARC, groups and X-COP as committed."""
    xok = lambda fs: abs(NZA["runs"][f"all_fs{fs}"]["footings"]["canonical"]["mean"]) <= 0.05 and NZA["runs"][f"all_fs{fs}"]["footings"]["canonical"]["rms"] <= 0.10
    def s(fs, m): g = NZA["runs"][f"{m}_fs{fs}"]["grader"]["canonical"]; fl = [x for x in g["failing"] if not x.startswith("G-")] + fails_of(C[f"nz1_a4_{fs}"]); return not fl, fl
    pa = [fs for fs in FS if s(fs, "all")[0] and xok(fs)]; pc = [fs for fs in FS if s(fs, "clusters")[0] and xok(fs)]; px = [fs for fs in FS if xok(fs)]
    V = "NATIVE CORE PASSES ALL" if len(pa) == 2 else f"F*-DEPENDENT (passes at {pa[0]})" if pa else "CLUSTERS PASS, GALAXIES BREAK (at " + ", ".join(pc) + ")" if pc else "X-COP PASSES, KEYS BREAK: " + "; ".join(f"{fs} {over2(C[f'nz1_a4_{fs}']) or s(fs, 'clusters')[1]}" for fs in px) if px else "NATIVE CORE FAILS: " + "; ".join(f"{fs} keys {over2(C[f'nz1_a4_{fs}']) or s(fs, 'all')[1]}, X-COP rms {NZA['runs'][f'all_fs{fs}']['footings']['canonical']['rms']:.3f}" for fs in FS)
    return dict(cls=V.split(":")[0], named=V)
def view(D, f): return {t: D[t][f] for t in D}
def labels(D):
    L = {"X71": {"canonical": x71_label({fs: D[f"x71_S_{fs}"]["canonical"] for fs in FS}), "alt": x71_label({fs: D[f"x71_S_{fs}"]["alt"] for fs in FS})}}
    L["GS1"] = {f: gs1_label(view(D, f), f) for f in FEET}; L["X73"] = {f: x73_label(D, f) for f in FEET}; L["GX2"] = {f: gx2_label(D["gx2_rsp"][f]) for f in FEET}; L["FC1 A4"] = {f: fc1_label(view(D, f), f) for f in FEET}; L["MA1 A4"] = {f: ma1_verdict(view(D, f), f) for f in FEET}; L["NZ1 A4"] = {"canonical": nz1_verdict(view(D, "canonical"))}
    return L
LF = labels(FRZ); LO = labels(ONE)
def change(a, b): return "HELD" if a["cls"] == b["cls"] and a["named"] == b["named"] else "NAMED LINES CHANGE" if a["cls"] == b["cls"] else "CLASS CHANGE"
# K6
x7s = jl(f"{X73D}/x73_summary.json"); gsv = jl(f"{GS1D}/gs1_gas_slope_results.json")["verdicts"]; gxv = jl(f"{GX2D}/gx2_corrected_gas_results.json")["verdict"]; fcv = jl(f"{FC1D}/fc1_a4_results.json")["labels"]; mav = jl(f"{MA1D}/ma1_a4_results.json")["verdict"]
k6 = {"X71": LF["X71"]["canonical"]["named"] == ["G-OUT-M3 (UNDER) at f* 0.034", "G-OUT-M3 (UNDER) at f* 0.0615"], "GS1": all(LF["GS1"][f]["cls"] == gsv[f]["class"] for f in FEET), "X73": all(LF["X73"][f]["verdict"] == x7s["verdict"][f] and LF["X73"][f]["robust"] == x7s["robustness"][f]["class"] and LF["X73"][f]["named"]["edges"] == x7s["robustness"][f]["edges"] for f in FEET), "GX2": all(("LENSING STILL FAILS: " + ", ".join(LF["GX2"][f]["named"])) == gxv[f] for f in FEET), "FC1": all(LF["FC1 A4"][f]["cls"] == fcv[f] for f in FEET), "MA1": all(LF["MA1 A4"][f]["named"] == mav[f] for f in FEET), "NZ1": LF["NZ1 A4"]["canonical"]["named"] == NZA["verdict"], "NZ1 ALL = CLUSTERS": d_all == 0.0}
check("K6", all(k6.values()), "each lane's rule on its frozen cells gives its committed label: " + ", ".join(f"{k} {'ok' if v else 'NO'}" for k, v in k6.items()))
# K7
if not MUT:
    B0 = json.load(open(os.path.join(RUNS, "_baseline.json"))); S1 = snapshot(); dst = sorted(set(S1["status"]) ^ set(B0["status"])); dmt = sorted(k for k in S1["mtime"] if S1["mtime"][k] != B0["mtime"].get(k)); k7 = not dst and not dmt
    check("K7", k7, f"files changed in the lanes the runs read, outside *.md: git status {dst}, mtime {dmt[:6]}")
# reported: does s scale with A?
gaps = []
for t in RUN:
    for c_, q in RUN[t]["M_outer"].items():
        for a, b, sa, sb, k in zip([q["all"]] + q["terc"], [q["x7_all"]] + q["x7_terc"], [q["s_all"]] + q["s_terc"], [q["x7_stat_all"]] + q["x7_stat_terc"], KEYS4): gaps.append(((sa / sb) / (a / b) - 1, t, c_, k))
gw = max(gaps, key=lambda x: abs(x[0]))
# ------------------------------------------------------------------ one line per run, with the joint read
GASR = {"gx2_rsp", "gx2_rta", "gx2_bur", "gx2_rsp_m", "gx2_rsp_p"}; JR = {}
def jline(t):
    c = ONE[t]["canonical"]; RJ = R_GAS if t in GASR else R_ORIG; v = {h: joint(c, RJ, h) for h in HH}; hw = min(HH, key=lambda q: v[q][2]); ni = joint(c, RJ, hw, keep=set(RJ[hw]["keys"]) - {"G-IN-all", "G-IN-Mall"}); ja = joint(c, RJ, hw, Rk="R_jack"); own = {h: joint(c, RUN[t]["R_own"], h) for h in HH}; hown = min(HH, key=lambda q: own[q][2]); g = {h: joint(FRZ[t]["canonical"], RJ, h) for h in HH}; hg = min(HH, key=lambda q: g[q][2])
    return dict(chi2=v[hw][0], dof=v[hw][1], p=v[hw][2], h=hw, label=jlabel(v[hw][2]), cells={h: v[h] for h in HH}, no_inner=ni, jack=ja, own=own[hown], own_label=jlabel(own[hown][2]), as_graded=g[hg])
for t in RUN: JR[t] = jline(t)
NAMES = {"x71_S": "X71 smooth, inherited, reread only", "x71_B": "X71 Burkert, inherited, reread only", "x73_S_nat_s2.7774": "X73 PRIMARY", "x73_S_nat_s2.6756": "X73 s16", "x73_S_nat_s3.0711": "X73 s84", "x73_S_nat_notail": "X73 native, no tail", "x73_S_inh_s2.7774": "X73 inherited, tail, reread only", "x73_B_nat_s2.7774": "X73 Burkert, native, tail", "fc1_a4_med": "FC1 ng 64 median", "fc1_a4_p16": "FC1 ng 64 p16", "fc1_a4_p84": "FC1 ng 64 p84", "ma1_a4": "MA1 ng 64", "nz1_a4": "NZ1 ng 64"}
def name(t):
    if t.startswith("gs1_"): return f"GS1 {t[4:]}, f* 0.20"
    if t.startswith("gx2_"): return {"gx2_rsp": "GX2 PRIMARY", "gx2_rta": "GX2 V1", "gx2_bur": "GX2 V2", "gx2_rsp_m": "GX2 PRIMARY -1 sigma", "gx2_rsp_p": "GX2 PRIMARY +1 sigma"}[t] + ", f* 0.20"
    a, b = t.rsplit("_", 1); return f"{NAMES.get(a, a)}, f* {b}"
def rline(t, f="canonical"):
    O, G = ONE[t][f], FRZ[t][f]; w, w0 = worst(O), worst(G); a, b = over2(O), over2(G); s = f"  {name(t)} [{f}]: {15 - len(a)} of 15, over 2 {a}, worst {w[0]} {w[1]} {w[2]:+.2f}; as graded {15 - len(b)} of 15, over 2 {b}, worst {w0[0]} {w0[2]:+.2f}. Four keys one template (as graded) h 0.672: " + ", ".join(f"{k[6:]} {O['h0672'][k]['Z']:+.2f} ({G['h0672'][k]['Z']:+.2f})" for k in KEYS4) + "; h 0.686: " + ", ".join(f"{k[6:]} {O['h0686'][k]['Z']:+.2f} ({G['h0686'][k]['Z']:+.2f})" for k in KEYS4)
    if f == "canonical": j = JR[t]; s += f". Joint chi^2 {j['chi2']:.1f} / {j['dof']}, p {j['p']:.2e}: {j['label']}; without INNER p {j['no_inner'][2]:.2e}; jackknife R p {j['jack'][2]:.2e}; own R {j['own'][0]:.1f}, p {j['own'][2]:.2e}; four keys as graded chi^2 {j['as_graded'][0]:.1f}"
    return s
P("Runs, canonical (K-only runs left out):")
ORDER = [f"x71_S_{fs}" for fs in FS] + [f"x71_B_{fs}" for fs in FS] + [f"gs1_{r}_{l}" for r in ("R4", "R5", "RX48") for l in ("meas", "s16", "s84")] + [f"x73_S_nat_s2.7774_{fs}" for fs in FS] + [f"x73_S_nat_s2.6756_{fs}" for fs in FS] + [f"x73_S_nat_s3.0711_{fs}" for fs in FS] + [f"x73_S_nat_notail_{fs}" for fs in FS] + [f"x73_S_inh_s2.7774_{fs}" for fs in FS] + ["x73_S_nat_s2.7774_0.2"] + [f"x73_B_nat_s2.7774_{fs}" for fs in FS + ("0.2",)] + ["gx2_rsp", "gx2_rta", "gx2_bur", "gx2_rsp_m", "gx2_rsp_p"] + [f"fc1_a4_{k}_{fs}" for k in ("med", "p16", "p84") for fs in FS] + [f"ma1_a4_{fs}" for fs in FS] + [f"nz1_a4_{fs}" for fs in FS]
for t in ORDER: P(rline(t))
P("Graded runs, alt, per key only (BA1's R is canonical):")
for t in [f"x71_S_{fs}" for fs in FS] + [f"x73_S_nat_{n}_{fs}" for n in ("s2.7774", "s2.6756", "s3.0711") for fs in FS] + ["gx2_rsp"] + [f"fc1_a4_med_{fs}" for fs in FS] + [f"ma1_a4_{fs}" for fs in FS] + [f"nz1_a4_{fs}" for fs in FS]: P(rline(t, "alt"))
P("GS1 alt, keys over 2 on one template (as graded): " + "; ".join(f"{t[4:]} {over2(ONE[t]['alt'])} ({over2(FRZ[t]['alt'])})" for t in ORDER if t.startswith("gs1_")))
# ------------------------------------------------------------------ the story
M3 = lambda D, t, h="h0672": D[t]["canonical"][h]["G-OUT-M3"]["Z"]
s1a = all(any(M3(ONE, f"x71_S_{fs}", h) > 2 for h in HH) for fs in FS); s1b = all(any(M3(ONE, f"x73_S_nat_notail_{fs}", h) > 2 for h in HH) for fs in FS); bad2 = {fs: fails_of(ONE[f"x73_S_nat_s2.7774_{fs}"]["canonical"]) for fs in FS}; s2 = not any(bad2.values())
STORY = "STORY SURVIVES" if s1a and s1b and s2 else "BREAK GONE" if not s1a and not s1b else "S1 SPLIT" if s1a != s1b else "TAIL DOES NOT FIX: " + "; ".join(f"f* {fs} {v}" for fs, v in bad2.items() if v)
MOVED = {}; rows = [("inherited, no tail (X71, X70), reread only", lambda fs: f"x71_S_{fs}"), ("native, no tail", lambda fs: f"x73_S_nat_notail_{fs}"), ("inherited, measured tail, reread only", lambda fs: f"x73_S_inh_s2.7774_{fs}"), ("native, measured tail (PRIMARY)", lambda fs: f"x73_S_nat_s2.7774_{fs}"), ("Burkert, native, measured tail", lambda fs: f"x73_B_nat_s2.7774_{fs}")]
P("What moved G-OUT-M3, canonical, h 0.672, one template (as graded):")
for lab, fn in rows:
    MOVED[lab] = {}
    for fs in FS + ("0.2",):
        t = fn(fs)
        if t in RUN: MOVED[lab][fs] = dict(one=M3(ONE, t), graded=M3(FRZ, t))
    P(f"  {lab}: " + "; ".join(f"f* {fs} {v['one']:+.2f} ({v['graded']:+.2f})" for fs, v in MOVED[lab].items()))
STEPS = {f"f* step, no tail, inherited, 0.20 to {fs}": (M3(ONE, f"x71_S_{fs}") - M3(ONE, "x71_S_0.2"), M3(FRZ, f"x71_S_{fs}") - M3(FRZ, "x71_S_0.2")) for fs in FS}
STEPS.update({f"tail step, native, f* {fs}": (M3(ONE, f"x73_S_nat_s2.7774_{fs}") - M3(ONE, f"x73_S_nat_notail_{fs}"), M3(FRZ, f"x73_S_nat_s2.7774_{fs}") - M3(FRZ, f"x73_S_nat_notail_{fs}")) for fs in FS})
STEPS.update({f"f* step, native, tail, 0.20 to {fs}": (M3(ONE, f"x73_S_nat_s2.7774_{fs}") - M3(ONE, "x73_S_nat_s2.7774_0.2"), M3(FRZ, f"x73_S_nat_s2.7774_{fs}") - M3(FRZ, "x73_S_nat_s2.7774_0.2")) for fs in FS})
P("Steps in G-OUT-M3's Z, canonical, h 0.672, one template (as graded): " + "; ".join(f"{k} {a:+.2f} ({b:+.2f})" for k, (a, b) in STEPS.items()))
ga = {t: (ONE[t]["canonical"]["h0672"]["G-OUT-all"]["Z"], FRZ[t]["canonical"]["h0672"]["G-OUT-all"]["Z"]) for t in ("x73_S_nat_s2.7774_0.2", "x73_S_nat_s2.7774_0.034", "x73_S_nat_s2.7774_0.0615")}
P("G-OUT-all, not one of the four keys, canonical, h 0.672: " + "; ".join(f"{name(t)} {a:+.2f} ({b:+.2f})" for t, (a, b) in ga.items()))
P(f"Reported: s scales with A? Largest gap between the run's own s_STAT ratio and A/A_CAL: {gw[0]:+.3f} ({name(gw[1])}, {gw[2]}, {gw[3]})")
# ------------------------------------------------------------------ verdict
RESL = {}
P("Labels by rule, each lane's own frozen rule (as graded -> one template):")
for lane, per in LO.items():
    RESL[lane] = {}
    for f, b in per.items():
        a = LF[lane][f]; ch = change(a, b); RESL[lane][f] = dict(as_graded=a, one_template=b, change=ch)
        if lane == "GS1":
            dl = {k: (a["named"][k], b["named"][k]) for k in a["named"] if a["named"][k] != b["named"][k]}; P(f"  GS1 [{f}]: {a['cls']} -> {b['cls']}: {ch}" + ("; lines that differ: " + "; ".join(f"{k} {x} -> {y}" for k, (x, y) in dl.items()) if dl else ""))
        else: P(f"  {lane} [{f}]: {a['cls']} {a['named']} -> {b['cls']} {b['named']}: {ch}" + (f"; ends p16, p84 at f* 0.034, then 0.0615, pass: {a['ends']} -> {b['ends']}" if lane == "FC1 A4" else ""))
RESL["GX2 V1, reported"] = {f: dict(as_graded=fails_of(FRZ["gx2_rta"][f]), one_template=fails_of(ONE["gx2_rta"][f])) for f in FEET}; RESL["GX2 V2, reported"] = {f: dict(as_graded=fails_of(FRZ["gx2_bur"][f]), one_template=fails_of(ONE["gx2_bur"][f])) for f in FEET}
for f in FEET: P(f"  GX2 V1 [{f}], reported: {RESL['GX2 V1, reported'][f]['as_graded']} -> {RESL['GX2 V1, reported'][f]['one_template']}; V2: {RESL['GX2 V2, reported'][f]['as_graded']} -> {RESL['GX2 V2, reported'][f]['one_template']}")
P(f"Story: S1 on X71's runs {s1a}, on X73's native no-tail runs {s1b}; S2 {s2}, X73 PRIMARY keys over 2: {bad2}")
res = dict(criteria="e30f1b461b", checks=CHK, labels=RESL, story=dict(verdict=STORY, s1_x71=s1a, s1_native=s1b, s2=s2, primary_over2=bad2, moved=MOVED, steps={k: dict(one=a, graded=b) for k, (a, b) in STEPS.items()}), s_gap=dict(gap=gw[0], run=gw[1], cell=gw[2], key=gw[3]), runs={t: dict(name=name(t), frozen=FRZ[t], one_template=ONE[t], joint=JR[t], m_outer={c: {k: q[k] for k in ("all", "terc", "x7_all", "x7_terc")} for c, q in RUN[t]["M_outer"].items()}, sparc={f: RUN[t]["footings"][f]["sparc"] for f in FEET}, groups={f: RUN[t]["footings"][f]["groups"] for f in FEET}, xcop=RUN[t]["xcop"], rss_gb=RUN[t]["rss_gb"]) for t in RUN})
if MUT:
    b0 = {fs: restate(FRZ[f"x73_S_nat_s2.7774_{fs}"]["canonical"], RUN[f"x73_S_nat_s2.7774_{fs}"]["M_outer"], "canonical")["h0672"]["G-OUT-M3"]["Z"] for fs in FS}; dm = max(abs(ONE[f"x73_S_nat_s2.7774_{fs}"]["canonical"]["h0672"]["G-OUT-M3"]["Z"] - b0[fs]) for fs in FS); c_ = ONE["x73_S_nat_s2.7774_0.034"]["canonical"]; a_ = joint(c_, R_ORIG, "h0672"); b_ = joint(c_, R_ORIG, "h0672", scale=2.0); x4 = abs(b_[0] / a_[0] - 4) < 1e-9
    bites = (not k1) and (not k2) and dm > 0.05 and x4; P(f"MUTATE: K1 {'failed' if not k1 else 'PASSED'}, K2 {'failed' if not k2 else 'PASSED'}, X73 PRIMARY G-OUT-M3 moved by {dm:.2f} in Z; d x 2: chi^2 x {b_[0] / a_[0]:.6f}: {'BITES' if bites else 'INSENSITIVE, lane UNDECIDED'}")
    json.dump(dict(k1_failed=not k1, k2_failed=not k2, dZ=dm, x4=x4, bites=bites), open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if bites else 1)
if good:
    ch = sorted(f"{l} [{f}]: {v['change']}" for l, d in RESL.items() if "change" in next(iter(d.values())) for f, v in d.items() if v["change"] != "HELD"); P("VERDICT, labels: " + ("no label changes" if not ch else "; ".join(ch))); P(f"VERDICT, story: {STORY}")
else: P("A CHECK FAILED: no verdict"); res.pop("story"); res["verdict"] = "NO VERDICT"
json.dump(res, open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if good else 1)
