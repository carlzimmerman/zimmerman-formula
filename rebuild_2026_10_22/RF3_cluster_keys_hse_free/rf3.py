#!/usr/bin/env python3
"""RF3_cluster_keys_hse_free (FROZEN_CRITERIA.md, e17dcb4e62): 15 keys and comparison masses for ZN3, native X77 c_f, external c_f 4.
    python3 rf3.py --inputs     # data only: XF, match table, KiDS coverage
    python3 rf3.py --run        # 26 grader runs, three workers, one thread, nice 15; resumes from runs/
    python3 rf3.py --grade      # checks and tables: rf3.out, rf3_results.json
    RF3_MUTATE=1 python3 rf3.py --run; RF3_MUTATE=1 python3 rf3.py --grade   # separate outputs
ZN3's, NZ1's and X73's files are read only. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); DATA = os.path.join(REPO, "real_research", "data"); RUNS = os.path.join(HERE, "runs")
SLOPE = "2.7774425603108597"; FS = ("0.024", "0.034", "0.0615", "0.136"); HH = ("h0672", "h0686"); FEET = ("canonical", "alt"); KEYS4 = ["G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3"]
MUT = os.environ.get("RF3_MUTATE") == "1"; TAG = "rf3_MUTATE" if MUT else "rf3"; ZN3D = os.path.join(RB, "ZN3_native_shape_at_1e15"); X77D = os.path.join(RB, "X77_direct_core_surface_density"); X73D = os.path.join(RB, "X73_smooth_core_all_measured"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); CE1 = os.path.join(RB, "CE1_converged_eta_grade")
INP = os.path.join(HERE, "rf3_inputs.json"); PLANCK = 5.364
GAS = """_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\' % (10 ** {dex!r}))\\n'
sub('NX = {{"__file__": X30SRC,', _x + 'NX = {{"__file__": X30SRC,')
"""
RFTAIL = r'''
assert abs(NAT_RRAT - 5.364) > 1e-3
_rf = dict(NAT_RRAT=NAT_RRAT, planck_lines=[l_.strip()[:120] for l_ in codeX.split("\n") if "5.364" in l_] if "codeX" in globals() else None)
_mt = json.load(open(os.environ["RF3_INP"])); _dex = float(os.environ["RF3_DEX"]); _flav = os.environ["RF3_FLAV"]
def _rf_fn(foot, Mg, r5, z):
    Mbx, Mbt = _gc2(Mg, r5 / 1e3, z, 3.0 * 1.2 * Mg * _MSX); rta = _rta_com(Mbt) / (1 + z); Mf = NAT_RRAT * Mbt
    if _flav == "zn3": f_ = zn1_fn(foot, _TBG, dict(Mb=Mbx, Mfair=Mf, rta=rta), z)
    else:
        s_ = sig_core(foot, _TBG, (Mf + Mbt) / MSUNE, True)[0]; r0_ = solve_r0(Mf, rta, s_); f_ = lambda r: math.pi * s_ * r0_ ** 2 * B(np.minimum(r, rta) / r0_)
    return Mbx, f_, rta
_rf["xcop"] = {}; _rf["match"] = {}; _rf["k4"] = 0.0; _rf["k5"] = {}
for f_ in FEET:
    _o = {}; _k5 = []
    for nm, m_ in _XM.items():
        Mbx_, fn_, rta_ = _rf_fn(f_, m_["Mg500"], m_["r500"], m_["z"]); _o[nm] = {}
        for rw in _mt["xcop_rows"].get(nm, []):
            rm = rw["r_kpc"] * 1e3 * _PCm; _o[nm][str(rw["i"])] = [float(np.interp(rm, RM, Mbx_)) / MSUNE, float(fn_(np.array([rm]))[0]) / MSUNE]
        for v in _OUT["footings"][f_]["rows"]:
            if v["cluster"] == nm:
                rm = v["r_kpc"] * 1e3 * _PCm; _rf["k4"] = max(_rf["k4"], abs(math.log10(float(fn_(np.array([rm]))[0]) / MSUNE / v["Mh_Msun"]))); _k5.append((v["x"], math.log10(float(np.interp(rm, RM, Mbx_)) / MSUNE / v["Mb_Msun"])))
    _rf["xcop"][f_] = _o; _rf["k5"][f_] = {f"{x:g}": float(np.median([d for a, d in _k5 if a == x])) for x in sorted({a for a, _ in _k5})}
    _o = {}
    for rw in _mt["match_rows"]:
        Mg_ = rw["Mg500"] * 10 ** _dex; Mbx_, fn_, rta_ = _rf_fn(f_, Mg_, rw["r500_kpc"], rw["z"]); rm = rw["r_kpc"] * 1e3 * _PCm; _o[str(rw["i"])] = [float(np.interp(rm, RM, Mbx_)) / MSUNE, float(fn_(np.array([rm]))[0]) / MSUNE]
    _rf["match"][f_] = _o
_num = lambda d: {k: float(v) for k, v in d.items() if isinstance(v, (int, float, np.floating))}
_rf["amps"] = {f"{f_}|{h_}": {b_: _num(M[f"{f_}|{h_}"][b_]) for b_ in ("KT_all|MID", "M_all|INNER", "KT_all|OUTER")} for f_ in FEET for h_ in HK}
_OUT["M_outer"] = {f"{f_}|{h_}": dict(all=M[f"{f_}|{h_}"]["M_all|OUTER"]["A"], terc=[x_["A"] for x_ in M[f"{f_}|{h_}"]["M_terc|OUTER"]]) for f_ in FEET for h_ in HK}
_OUT["grader"] = {f_: {k_: RES["footings"][f_][k_] for k_ in ("verdict", "failing", "sparc", "groups", "clusters")} for f_ in FEET}
for f_ in FEET: _OUT["footings"][f_].pop("rows", None); _OUT["footings"][f_].pop("info", None)
_OUT["rf"] = _rf
'''
def jobs():
    J = {}
    for r in ("ZN3", "NAT", "C4"):
        for g in ("E", "X"):
            for fs in FS: J[f"{r}_{g}_{fs}"] = dict(rule=r, gas=g, fs=fs)
    for fs in ("0.034", "0.0615"): J[f"ZN3_XF_{fs}"] = dict(rule="ZN3", gas="XF", fs=fs)
    return J
def dex_of(g):
    return dict(E=0.0, X=0.111, XF=json.load(open(INP))["XF"]["median_dex"])[g]
def worker():
    WD = os.environ["RF3_WD"]; rule = os.environ["RF3_RULE"]; dex = float(os.environ["RF3_DEX"]); xp = (GAS.format(dex=dex) if dex != 0.0 else "") + f"RFT_ = {RFTAIL!r}\n"
    if rule == "ZN3":
        xp += '_e = \'json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)\\nsys.exit(0)\'; sub(_e, RFT_ + _e)\n'
        xf = os.path.join(WD, "x.py"); open(xf, "w").write(xp); os.environ["ZN1_XFILE"] = xf; G = os.path.join(ZN3D, "zn3_grade.py"); sys.argv = [G, "--worker"]; exec(compile(open(G).read(), G, "exec"), {"__file__": G, "__name__": "__main__"})
    X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read(); INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    t = open(os.path.join(RB, "XH1_xcop_native_rule", "xh1_tail.py")).read(); e = '_OUT["rss_gb"] = rss(); json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)\nsys.exit(0)'; assert t.count(e) == 1; t = t.replace(e, RFTAIL + e); tf = os.path.join(WD, "tail.py"); open(tf, "w").write(t)
    MY = f"sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})\nsub('if CFSRC == \"const4\" and CFMULT == 1 and SLOPE is not None:', 'if CFSRC == \"const4\" and CFMULT == 1 and SLOPE is not None and FSTAR in (0.034, 0.0615, 0.2):')\n" + f"sub('sys.exit(0 if (n == len(checks) and x74ok) else 1)', open({tf!r}).read())\n" + (GAS.format(dex=dex) if dex != 0.0 else "")
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
def run1(a):
    tag, sp = a; o = os.path.join(RUNS, f"{tag}.json")
    if os.path.exists(o): return tag, True, 0
    WD = tempfile.mkdtemp(); out = os.path.join(WD, "o.json"); rule = sp["rule"]
    tab = {"ZN3": os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), "NAT": os.path.join(X77D, "A4_x77_native_table.json"), "C4": "const4"}[rule]
    env = dict(os.environ, FC1_MODE="cold" if rule == "ZN3" else "none", X74_CF=tab, X73_FSTAR=sp["fs"], X73_SLOPE=SLOPE, XH1_OUT=out, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, RF3_WD=WD, RF3_RULE=rule, RF3_FLAV="zn3" if rule == "ZN3" else "cf", RF3_DEX=str(dex_of(sp["gas"])), RF3_INP=INP, ZN1_MODE="fs", ZN1_RX=str(sp.get("rx", 1.0)), ZN1_SNAP="nearest", ZN1_SHAPES=os.path.join(ZN3D, "zn3_shapes.json"), PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, "-I", os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(out): print(f"{tag} NO RESULT exit {p.returncode}: {p.stdout[-400:]} {p.stderr[-1500:]}", flush=True); return tag, False, p.returncode
    r = json.load(open(out)); keep = {k: r[k] for k in ("fstar", "footings", "grader", "M_outer", "rf", "rss_gb") if k in r}; keep["zn1"] = {k: v for k, v in r.get("zn1", {}).items()}; os.makedirs(RUNS, exist_ok=True); json.dump(keep, open(o, "w"), default=float); shutil.rmtree(WD, ignore_errors=True); print(f"{tag} done, rss {r.get('rss_gb')}", flush=True); return tag, True, 0
def fix_cells(R, f):
    c = R["grader"][f]["clusters"]["cells"]; O = {}
    for h in HH:
        m = R["M_outer"][f"{f}|{h}"]; O[h] = {k: dict(v) for k, v in c[h].items()}
        for k, A in zip(KEYS4, [m["all"]] + m["terc"]):
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
# ------------------------------------------------------------------ data-only inputs
def hms(a):
    x = [float(t) for t in a.split()]; return 15 * (x[0] + x[1] / 60 + x[2] / 3600)
def dms(a):
    a = a.strip(); sg = -1 if a.startswith("-") else 1; x = [abs(float(t)) for t in a.replace("+", "").replace("-", "").split()]; return sg * (x[0] + x[1] / 60 + x[2] / 3600)
def rho_c(z, Om, h): return 2.775e11 * h * h * (Om * (1 + z) ** 3 + 1 - Om)
def r200_kpc(M, z, Om, h): return 1e3 * (3 * M / (4 * math.pi * 200 * rho_c(z, Om, h))) ** (1 / 3)
def inputs():
    from astropy.io import fits
    def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
    E = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data; EN = {str(n).strip(): k for k, n in enumerate(E["NAME"])}; SM = json.load(open(os.path.join(RB, "SM1_cluster_sample_match", "sm1_cluster_sample_match_results.json")))["matched"]; XT = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json"))); xf = []
    for q in SM:
        n = q["xcop"]; j = EN[q["erass"]]; 
        with fits.open(os.path.join(DATA, "xcop", n, f"{n}_fgas_profile.fits")) as h: g = h[1].data.copy(); rg = float(h[1].header["R500"])
        Re = float(E["R500"][j]); Me = float(E["MGAS500"][j]) * 1e11; d = math.log10(li(g["RADIUS"] * rg, g["MGAS"], Re) / Me); d0 = math.log10(li(g["RADIUS"] * rg, g["MGAS"], XT[n]["R500"] * 1e3) / Me); xf.append(dict(xcop=n, dex_at_eRASS_R500=d, dex_at_XCOP_R500=d0, R500_eRASS_kpc=Re, R500_XCOP_kpc=XT[n]["R500"] * 1e3))
    XF = dict(rows=xf, median_dex=float(np.median([r["dex_at_eRASS_R500"] for r in xf])), median_at_xcop_r500=float(np.median([r["dex_at_XCOP_R500"] for r in xf])))
    L = [l.rstrip("\n") for l in open(os.path.join(DATA, "groener2016_cluster_concentrations.tsv")) if not l.startswith("#") and l.strip()]; H = L[0].split("\t"); ix = {h: i for i, h in enumerate(H)}; ROWS = []; drop = 0
    for l in L[3:]:
        c = [t.strip() for t in l.split("\t")]
        try: M = float(c[ix["M200"]]) * 1e14
        except ValueError: drop += 1; continue
        def fl(k, d=None):
            try: return float(c[ix[k]])
            except ValueError: return d
        ROWS.append(dict(src="G16", cluster=c[ix["Cluster"]], z=fl("z"), ra=hms(c[ix["RAJ2000"]]), dec=dms(c[ix["DEJ2000"]]), method=c[ix["Method"]], M=M, ep=(fl("E_M200", 0) or 0) * 1e14, em=(fl("e_M200", 0) or 0) * 1e14, Om=fl("Omegam", 0.3), h=fl("h"), ref=c[ix["Ref"]]))
    T1 = {}
    for l in open(os.path.join(REPO, "deepseek_push", "G203_data", "table1.dat")):
        p = [t.strip() for t in l.split("|")]; T1[p[0]] = p
    hecs = [dict(zip(("cluster", "r500", "r200", "r56", "rmax", "M200", "M200e"), l.split("\t")[:7])) for l in list(open(os.path.join(REPO, "deepseek_push", "G203_data", "hecs2013_table4.tsv")))[1:]]
    for q in hecs:
        l = T1[q["cluster"]]; ra, dec = float(l[1]), float(l[2]); ROWS.append(dict(src="HeCS", cluster=q["cluster"], z=float(l[3]), ra=ra, dec=dec, method="CM", M=float(q["M200"]) * 1e14, ep=float(q["M200e"]) * 1e14, em=float(q["M200e"]) * 1e14, Om=0.3, h=1.0, ref="Rines+13"))
    NM = {"A85": r"^Abell 0*85$", "A644": r"^Abell 0*644$", "A1644": r"^Abell 1644$", "A1795": r"^Abell 1795$", "A2029": r"^Abell 2029$", "A2142": r"^Abell 2142$", "A2319": r"^Abell 2319$", "ZW1215": r"^ZwCl 1215"}
    i = 0; xrows = {}; mrows = []; ra_e, de_e, z_e = np.array(E["RA"], float), np.array(E["DEC"], float), np.array(E["BEST_Z"], float); MG = np.array(E["MGAS500"], float); R5 = np.array(E["R500"], float); blank = 0
    def conv(r, h):
        hs = r["h"] if r["h"] else h; M = r["M"] * hs / 0.7; rk = r200_kpc(r["M"], r["z"], r["Om"], hs) * hs / 0.7; return M, rk
    for r in ROWS:
        blank += 0 if r["h"] else 1
        for hv in ([None] if r["h"] else [0.7, 1.0]):
            h = r["h"] or hv; M, rk = conv(r, h); base = dict(i=i, cluster=r["cluster"], src=r["src"], method=r["method"], ref=r["ref"], M=M, ep=r["ep"] * h / 0.7, em=r["em"] * h / 0.7, r_kpc=rk, h_used=h, h_blank=not r["h"], z=r["z"]); i += 1
            for n, pat in NM.items():
                if re.search(pat, r["cluster"]): xrows.setdefault(n, []).append(dict(base))
            if r["z"] is None or r["z"] > 0.6: continue
            d = np.hypot((ra_e - r["ra"]) * math.cos(math.radians(r["dec"])), de_e - r["dec"]); j = int(np.nanargmin(d))
            if d[j] * 60 < 3.0 and abs(z_e[j] - r["z"]) < 0.01 and np.isfinite(MG[j]) and MG[j] > 0 and np.isfinite(R5[j]) and R5[j] > 0:
                b = dict(base); b.update(erass=str(E["NAME"][j]).strip(), Mg500=float(MG[j]) * 1e11, r500_kpc=float(R5[j]), z=float(z_e[j])); mrows.append(b)
    # KiDS coverage near every X-COP cluster, sparse scan
    f = fits.open(os.path.join(DATA, "lensing_rar", "KiDS_DR4.1_SOM_gold_WL_cat.fits"), memmap=True); d = f[1].data; n = len(d); A = []; D = []
    for k in range(0, n, n // 1000): A.append(np.array(d["RAJ2000"][k:k + 300], float)); D.append(np.array(d["DECJ2000"][k:k + 300], float))
    A = np.concatenate(A); D = np.concatenate(D); cov = {}; c_ = 2.998e5
    for nm in sorted(os.listdir(os.path.join(DATA, "xcop"))):
        p = os.path.join(DATA, "xcop", nm, f"{nm}_fgas_profile.fits")
        if not os.path.exists(p): continue
        with fits.open(p) as h: ra = float(h[1].header["RA"]); dec = float(h[1].header["DEC"])
        z = XT[nm]["z"]; zz = np.linspace(0, z, 400); chi = float(np.sum(0.5 * np.diff(zz) * (lambda y: y[1:] + y[:-1])(c_ / (70 * np.sqrt(0.2976 * (1 + zz) ** 3 + 0.7024))))); DA = chi / (1 + z); sep = np.degrees(np.arccos(np.clip(np.sin(np.radians(D)) * math.sin(math.radians(dec)) + np.cos(np.radians(D)) * math.cos(math.radians(dec)) * np.cos(np.radians(A - ra)), -1, 1))); dmin = float(sep.min()); cov[nm] = dict(ra=ra, dec=dec, sep_deg=dmin, sep_Mpc=math.radians(dmin) * DA, R200_Mpc=XT[nm]["R200"], sep_over_R200=math.radians(dmin) * DA / XT[nm]["R200"])
    json.dump(dict(XF=XF, xcop_rows=xrows, match_rows=mrows, coverage=cov, n_scan=len(A), dropped_no_M200=drop, n_rows=len(ROWS), blank_h=blank), open(INP, "w"), indent=1, default=float)
    print("XF rows"); [print(" ", r) for r in xf]; print("XF median", XF["median_dex"], "at X-COP R500", XF["median_at_xcop_r500"]); print("scan", len(A), "coverage"); [print(" ", k, {a: round(b, 3) for a, b in v.items()}) for k, v in cov.items()]
    from collections import Counter; print("xcop rows", {k: len(v) for k, v in xrows.items()}, "methods", Counter(r["method"] for v in xrows.values() for r in v)); print("match rows", len(mrows), Counter(r["method"] for r in mrows), "clusters", len({r["erass"] for r in mrows}))
if __name__ == "__main__" and "--worker" in sys.argv: worker(); sys.exit(0)
if __name__ == "__main__" and "--inputs" in sys.argv: inputs(); sys.exit(0)
if __name__ == "__main__" and "--run" in sys.argv:
    J = {"ZN3_X_0.034_RX1.5": dict(rule="ZN3", gas="X", fs="0.034", rx=1.5)} if MUT else jobs()
    if os.environ.get("RF3_ONLY"): J = {k: v for k, v in J.items() if k in os.environ["RF3_ONLY"].split(",")}
    with ThreadPoolExecutor(3) as ex: S = list(ex.map(run1, J.items()))
    bad = [t for t, ok, _ in S if not ok]; print("failed:", bad, flush=True); sys.exit(1 if bad else 0)
# ------------------------------------------------------------------ grade
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def load(t): return json.load(open(os.path.join(RUNS, f"{t}.json")))
def key_summary(R, f):
    O = fix_cells(R, f); bad = sorted({k for h in HH for k, v in O[h].items() if abs(v["Z"]) > 2}); w = max(((k, h, v["Z"], v["pred"] > v["meas"]) for h in HH for k, v in O[h].items()), key=lambda t: abs(t[2])); return dict(n=15 - len(bad), bad=bad, worst=w[0], worst_h=w[1], Z=w[2], over=bool(w[3]))
def zex(R, f, h):
    a = R["rf"]["amps"][f"{f}|{h}"]; m = a["KT_all|MID"]; i = a["M_all|INNER"]; return dict(A_MID=m["A"], s_MID=m["s"], Z_MID=(m["A"] - 1) / m["s"], A_IN=i["A"], s_IN=i["s_IN"], Z_IN=(i["A"] - 1) / i["s_IN"])
def reduce_rows(rows, vals, fac):
    """rows: comparison rows; vals: i -> [Mb, Mh]. Median per (cluster, h variant), then across clusters."""
    C = {}
    for r in rows:
        v = vals[str(r["i"])]; d = math.log10(fac * r["M"] / (v[0] + v[1])); e = (r["ep"] + r["em"]) / 2 / r["M"] / math.log(10) if r["M"] and (r["ep"] or r["em"]) else None; C.setdefault(r["erass"] if "erass" in r else r["cluster"], []).append((d, e))
    D = np.array([float(np.median([x[0] for x in q])) for q in C.values()]); N = len(D)
    if N >= 3: se = float(np.std(D, ddof=1) / math.sqrt(N))
    else:
        es = [x[1] for q in C.values() for x in q]; se = None if any(e is None for e in es) or not es else float(math.sqrt(sum(e * e for e in es)) / len(es))
    return dict(N=N, n_rows=len(rows), median=float(np.median(D)) if N else None, mean=float(np.mean(D)) if N else None, rms=float(np.std(D, ddof=1)) if N >= 2 else None, SE=se)
def reading(s):
    if s["N"] == 0: return "NO ROWS"
    if s["SE"] is None: return "NOT RESOLVED (no error)"
    if abs(s["median"]) <= 0.05 and s["SE"] <= 0.05: return "AT THE LINE"
    if abs(s["median"]) - 2 * s["SE"] > 0.05: return "OFF THE LINE, " + ("model too light" if s["median"] > 0 else "model too heavy")
    return "NOT RESOLVED"
def grade():
    I = json.load(open(INP)); fac = 2.0 if MUT else 1.0; RES = {"inputs": dict(XF=I["XF"], coverage=I["coverage"], n_rows=I["n_rows"], dropped=I["dropped_no_M200"], blank_h=I["blank_h"])}; ok = True
    P(f"RF3 {TAG}: ZN3, NAT (X77 ng 64), C4 EXTERNAL; f* band; one template; comparison masses as labelled brackets; kappa = 1/2 FITTED; footings never pooled; not theory closed")
    P(f"XF: HSE-free gas scale, median log10[M_gas,X-COP(<R500,eRASS)/Mgas500,eRASS] = {I['XF']['median_dex']:+.3f} (at X-COP's R500 {I['XF']['median_at_xcop_r500']:+.3f}; SM1 +0.111); rows " + ", ".join(f"{r['xcop']} {r['dex_at_eRASS_R500']:+.3f}" for r in I["XF"]["rows"]))
    cv = I["coverage"]; ins = [k for k, v in cv.items() if v["sep_over_R200"] < 1.0]; P("RAW: KiDS DR4 nearest sparse-scan source, in R200: " + ", ".join(f"{k} {v['sep_over_R200']:.1f}" for k, v in sorted(cv.items(), key=lambda t: t[1]["sep_over_R200"])[:4]) + f"; inside 1 R200: {ins or 'none'} (scan {I['n_scan']})"); RES["raw_inside"] = ins
    J = {"ZN3_X_0.034_RX1.5": dict(rule="ZN3", gas="X", fs="0.034", rx=1.5)} if MUT else jobs()
    # checks
    ZJ = json.load(open(os.path.join(ZN3D, "zn3_results.json")))["runs"]
    def d_pred(R, ref): return max(abs(R["grader"]["canonical"]["clusters"]["cells"][h][k]["pred"] - ref[h][k]["pred"]) for h in HH for k in ref[h])
    if MUT:
        R = load("ZN3_X_0.034_RX1.5"); B_ = load("ZN3_X_0.034"); d = d_pred(R, ZJ["f* 0.034, X-COP's gas"]["cells"]); x = R["footings"]["canonical"]; x0 = B_["footings"]["canonical"]; P(f"MUTATE r x 1.5: K1 |d| {d:.3f} (must fail), X-COP rms {x0['rms']:.3f} -> {x['rms']:.3f}")
        dG = fix_cells(R, "canonical")["h0672"]["G-IN-Mall"]["Z"] - fix_cells(B_, "canonical")["h0672"]["G-IN-Mall"]["Z"]; S0 = reduce_rows(I["match_rows"], B_["rf"]["match"]["canonical"], 1.0); S1 = reduce_rows(I["match_rows"], B_["rf"]["match"]["canonical"], 2.0); dd = S1["median"] - S0["median"]; bites = d > 1e-9 and abs(dG) > 0.05 and dd > 0.25
        P(f"MUTATE G-IN-Mall moved {dG:+.2f}; every M_pub x 2 moves Delta by {dd:+.3f}: {'BITES' if bites else 'INSENSITIVE, lane UNDECIDED'}"); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(dict(bites=bites, K1d=d, dG=dG, dd=dd), open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1); sys.exit(0 if bites else 1)
    ZF = {"ZN3_X_0.034": "f* 0.034, X-COP's gas", "ZN3_X_0.0615": "f* 0.0615, X-COP's gas", "ZN3_E_0.034": "f* 0.034, eRASS1's own gas"}; k1 = 0.0
    for t, l in ZF.items():
        R = load(t); k1 = max(k1, d_pred(R, ZJ[l]["cells"]))
        if "X_" in t:
            k1 = max(k1, abs(R["footings"]["canonical"]["mean"] - ZJ[l]["xcop"]["mean"]), abs(R["footings"]["canonical"]["rms"] - ZJ[l]["xcop"]["rms"]))
    k2 = 0.0; k2z = []; BA = json.load(open(os.path.join(RB, "BA2_one_template_reread", "ba2_results.json")))
    for fs in ("0.034", "0.0615"):
        R = load(f"C4_E_{fs}"); XJ = json.load(open(os.path.join(X73D, f"x73_results_fs{fs}_S_nat_s2.7774.json")))["footings"]; k2 = max(k2, *[abs(R["grader"][f]["clusters"]["cells"][h][k]["pred"] - XJ[f]["clusters"]["cells"][h][k]["pred"]) for f in FEET for h in HH for k in XJ[f]["clusters"]["cells"][h]]); k2z.append(fix_cells(R, "canonical")["h0672"]["G-OUT-M3"]["Z"])
    k2b = abs(k2z[0] - 1.04) <= 0.005 and abs(k2z[1] - 0.73) <= 0.005; k3 = 0.0
    for fs in ("0.034", "0.0615"):
        R = load(f"NAT_E_{fs}"); XJ = json.load(open(os.path.join(X77D, f"A4grade_x74_results_fs{fs}_nat_s2.7774.json")))["footings"]; k3 = max(k3, *[abs(R["grader"][f]["clusters"]["cells"][h][k]["pred"] - XJ[f]["clusters"]["cells"][h][k]["pred"]) for f in FEET for h in HH for k in XJ[f]["clusters"]["cells"][h]])
    ALL = {t: load(t) for t in J}; k4 = max(R["rf"]["k4"] for R in ALL.values()); k6 = all(abs(R["rf"]["NAT_RRAT"] - PLANCK) > 1e-3 for R in ALL.values())
    gr = [l for l in open(os.path.abspath(__file__)) if "5.364" in l and "assert" not in l and "PLANCK =" not in l and "planck_lines" not in l and 'if "5.364"' not in l and "5.364 in" not in l and "gr = [l" not in l]; pl = sorted({x for R in ALL.values() for x in (R["rf"].get("planck_lines") or [])})
    K = dict(K1=k1 <= 1e-9, K2=k2 <= 1e-9 and k2b, K3=k3 <= 1e-9, K4=k4 <= 1e-6, K6=k6 and not gr)
    P(f"K1 ZN3 preds, X-COP vs zn3_results: {k1:.1e} {'PASS' if K['K1'] else 'FAIL'}; K2 C4 vs X73 {k2:.1e}, G-OUT-M3 one template {k2z[0]:+.3f} {k2z[1]:+.3f} vs BA2 +1.04 +0.73 {'PASS' if K['K2'] else 'FAIL'}; K3 NAT vs X77 A4 grade {k3:.1e} {'PASS' if K['K3'] else 'FAIL'}; K4 M_h vs grader rows {k4:.1e} {'PASS' if K['K4'] else 'FAIL'}")
    P(f"K6 no 5.364: NAT_RRAT {ALL['C4_E_0.034']['rf']['NAT_RRAT']:.4f} every run, {'PASS' if k6 else 'FAIL'}; script grep hits {len(gr)}; lines still holding 5.364 in the patched X30 text (inactive unless listed as used): {pl[:6]}")
    k5 = ALL["ZN3_X_0.034"]["rf"]["k5"]["canonical"]; P("K5 grader-model M_b / measured gas + stars at X-COP rows, median dex by x: " + ", ".join(f"{a} {b:+.3f}" for a, b in k5.items())); use_meas = abs(k5.get("0.7", 0.0)) > 0.05; RES["k5"] = k5
    ok = all(K.values()); RES["checks"] = K
    # keys
    P("\nKEYS: passing of 15, worst key and Z (OVER = pred above meas), both h; X-COP HSE line beside it (bracket)")
    KT = {}
    for t in J:
        R = ALL[t]; r, g, fs = t.split("_"); 
        for f in FEET:
            s = key_summary(R, f); x = R["footings"][f]; xp = abs(x["mean"]) <= 0.05 and x["rms"] <= 0.10; sp = R["grader"][f]; KT[f"{t}|{f}"] = dict(s, xcop_mean=x["mean"], xcop_rms=x["rms"], xcop_pass=xp, groups_Z=sp["groups"]["Z"], sparc=sp["sparc"], grader_failing=sp["failing"], verdict=sp["verdict"])
    for r in ("ZN3", "NAT", "C4"):
        for g in ("E", "X", "XF"):
            for f in FEET:
                for fs in FS:
                    q = KT.get(f"{r}_{g}_{fs}|{f}")
                    if q: P(f"  {r} {g} f* {fs} {f}: {q['n']}/15 worst {q['worst']} {q['Z']:+.2f} ({'OVER' if q['over'] else 'UNDER'}) over 2 {q['bad']}; X-COP {q['xcop_mean']:+.3f}, {q['xcop_rms']:.3f} {'PASS' if q['xcop_pass'] else 'FAIL'}; groups Z {q['groups_Z']:+.2f}")
    RES["keys"] = KT
    # excess
    P("\nEXCESS (A-1)/s, law's template, no rule; MID = KT_all|MID, IN = M_all|INNER; band over f* (0.024-0.136) per footing, gas, h")
    ZB = {}
    for g in ("E", "X"):
        for f in FEET:
            for h in HH:
                z = [zex(ALL[f"C4_{g}_{fs}"], f, h) for fs in FS]; ZB[f"{g}|{f}|{h}"] = dict(Z_MID=[q["Z_MID"] for q in z], A_MID=[q["A_MID"] for q in z], s_MID=z[0]["s_MID"], Z_IN=[q["Z_IN"] for q in z], A_IN=[q["A_IN"] for q in z]); P(f"  gas {g} {f} {h}: Z_MID {min(ZB[f'{g}|{f}|{h}']['Z_MID']):+.2f} to {max(ZB[f'{g}|{f}|{h}']['Z_MID']):+.2f} (A {min(q['A_MID'] for q in z):.3f}-{max(q['A_MID'] for q in z):.3f}); Z_IN {min(q['Z_IN'] for q in z):+.2f} to {max(q['Z_IN'] for q in z):+.2f}")
    RES["excess"] = ZB; d_rule = max(abs(zex(ALL[f"{r}_E_0.034"], "canonical", "h0672")["A_MID"] - zex(ALL["C4_E_0.034"], "canonical", "h0672")["A_MID"]) for r in ("ZN3", "NAT")); P(f"  template independent of rule: max |d A_MID| {d_rule:.1e}")
    # c_f question
    P("\nDOES IT NEED EXTERNAL c_f? 15 keys alone, then keys + SPARC line + groups (X74's own failing list)")
    CF = {}
    for f in FEET:
        for g in ("E", "X"):
            for fs in FS:
                n, c = KT[f"NAT_{g}_{fs}|{f}"], KT[f"C4_{g}_{fs}|{f}"]; a = "NAT passes" if n["n"] == 15 else "only C4 passes" if c["n"] == 15 else "neither"; CF[f"{f}|{g}|{fs}"] = a; P(f"  {f} gas {g} f* {fs}: {a} (NAT {n['n']}, C4 {c['n']}, ZN3 {KT[f'ZN3_{g}_{fs}|{f}']['n']}); NAT failing lines {n['grader_failing']}; C4 failing lines {c['grader_failing']}")
    RES["cf"] = CF
    # comparison masses
    P("\nCOMPARISON MASSES, labelled brackets (LCDM-PROCESSED or HSE), Delta = log10(M_pub/M_model), > 0 model too light. Median per cluster, then across clusters. Line |median| <= 0.05, SE <= 0.05")
    METH = ("CM", "WL", "WL+SL", "LOSVD", "X-ray"); CM = {}
    def table(lab, rows, vals, extra=""):
        for m in METH:
            for hv, sel in (("", lambda r: not r["h_blank"] or r["h_used"] == 0.7), (" [blank h = 1]", lambda r: not r["h_blank"] or r["h_used"] == 1.0)):
                q = [r for r in rows if r["method"] == m and sel(r) and str(r["i"]) in vals]
                if hv and not any(r["h_blank"] for r in q): continue
                s = reduce_rows(q, vals, 1.0); s["reading"] = reading(s); CM[f"{lab}|{m}{hv}"] = s
                if s["N"]: P(f"  {lab} {m}{hv}: clusters {s['N']} rows {s['n_rows']} median {s['median']:+.3f} mean {s['mean']:+.3f} SE {s['SE'] if s['SE'] is None else round(s['SE'], 3)}: {s['reading']}")
    xr = [r for v in I["xcop_rows"].values() for r in v]
    for rule in ("ZN3", "NAT", "C4"):
        for fs in ("0.034", "0.0615"):
            for f in (FEET if rule != "ZN3" else ("canonical",)):
                vals = {k: v for nm in ALL[f"{rule}_X_{fs}"]["rf"]["xcop"][f].values() for k, v in nm.items()}; table(f"X-COP-7 {rule} f* {fs} {f}", xr, vals)
    for rule in ("ZN3", "NAT", "C4"):
        for g in ("X", "E") + (("XF",) if rule == "ZN3" else ()):
            for fs in ("0.034", "0.0615"):
                for f in (FEET if rule != "ZN3" else ("canonical",)):
                    table(f"eRASS1 match {rule} gas {g} f* {fs} {f}", I["match_rows"], ALL[f"{rule}_{g}_{fs}"]["rf"]["match"][f])
    RES["comparison"] = CM
    # model-free: published vs HSE on X-COP-7
    from astropy.io import fits
    P("\nMODEL-FREE: log10(M_pub / M_FORW) at the published r200, X-COP-7"); MF = []
    for nm, rows in I["xcop_rows"].items():
        with fits.open(os.path.join(DATA, "xcop", nm, f"{nm}_hydro_mass.fits")) as h: hm = h[1].data.copy()
        for r in rows:
            if r["r_kpc"] <= hm["RADIUS"].max() and r["r_kpc"] >= hm["RADIUS"].min(): 
                m = float(10 ** np.interp(np.log10(r["r_kpc"]), np.log10(hm["RADIUS"]), np.log10(hm["M_FORW"]))); MF.append(dict(cluster=nm, method=r["method"], ref=r["ref"], h_used=r["h_used"], r_kpc=r["r_kpc"], M_pub=r["M"], M_FORW=m, d=math.log10(r["M"] / m)))
    for q in MF:
        if q["method"] != "X-ray": P(f"  {q['cluster']} {q['method']} {q['ref']} h {q['h_used']}: r {q['r_kpc']:.0f} kpc, M_pub {q['M_pub']:.2e}, M_FORW {q['M_FORW']:.2e}, {q['d']:+.3f}")
    RES["model_free"] = MF
    P("\nX-COP-7 rows, one by one (ZN3, f* 0.034, canonical): cluster method ref h: Delta")
    V = {k: v for nm in ALL["ZN3_X_0.034"]["rf"]["xcop"]["canonical"].values() for k, v in nm.items()}
    for nm, rows in I["xcop_rows"].items():
        for r in rows:
            if r["method"] != "X-ray" and str(r["i"]) in V: P(f"  {nm} {r['method']} {r['ref']} h {r['h_used']}: r {r['r_kpc']:.0f}, M_pub {r['M']:.2e}, model {sum(V[str(r['i'])]):.2e}: {math.log10(r['M'] / sum(V[str(r['i'])])):+.3f}")
    # verdicts
    xf = [KT[f"ZN3_XF_{fs}|canonical"] for fs in ("0.034", "0.0615")]; XFV = "ZN3 KEYS SURVIVE ON THE HSE-FREE GAS SCALE" if all(q["n"] == 15 for q in xf) else "FAILS ON THE HSE-FREE GAS SCALE: " + ", ".join(sorted({k for q in xf for k in q["bad"]}))
    cl = lambda fs: (KT[f"ZN3_X_{fs}|canonical"]["n"] == 15, KT[f"ZN3_X_{fs}|canonical"]["xcop_pass"]); base = cl("0.034"); dep = any(cl(fs) != base for fs in FS)
    GATE = "UNDETERMINED: no clean HSE-free X-COP mass on disk" if not ins else "NOT DECIDED: raw shear exists inside R200, amendment needed"
    P(f"\nVERDICT ZN3 keys: {XFV}. X-COP gate without HSE: {GATE}.{' [F*-BAND-DEPENDENT]' if dep else ''}")
    RES["verdict"] = dict(keys_XF=XFV, gate=GATE, fstar_dep=dep, checks_ok=ok); json.dump(RES, open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    if not ok: P("K FAILURE: no verdict"); sys.exit(1)
if __name__ == "__main__" and "--grade" in sys.argv: grade()
