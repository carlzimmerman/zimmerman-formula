#!/usr/bin/env python3
"""CE2 (FROZEN_CRITERIA.md 8e89ef6740): QX7 iter_4's late-heated window at QX10's four cells, on the sector's host-bound
n = 1 end state (QX10 iter_2 static A), graded on X-COP shape, groups (strict + kT trend), Bullet (ram-pressure split),
CMB lensing chi^2, DESI DR1 fsigma8 at z < 1, forest at z 2-4.
    python3 ce2.py            -> ce2.json / ce2.out
    python3 ce2.py --mutate   -> ce2_MUTATE.json / ce2_MUTATE.out
QX10 iter_2, QX7 iter_4, QX5, QX3 and DB1 are exec'd read-only from their sources. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, subprocess, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
CL6 = os.path.join(REPO, "closure_2026_11_06")
MUT = "--mutate" in sys.argv; TAG = "ce2_MUTATE" if MUT else "ce2"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

CELLS = {"C1": (2.6102, 4.25), "C2": (1.4678, 3.5), "C3": (8.254, 5.625), "C4": (2.1544, 3.75)}
V_BULLET = (2700.0, 4700.0)          # km/s, primary / reported
R_QX15 = 0.12094000633665247 / 0.022358   # KD1 / QX15 omega_d / omega_b (M1)


def load_qx10():
    f = os.path.join(CL6, "QX10_window_hardening", "iter_2_capture_dynamics", "qx10_i2.py")
    src = open(f).read(); cut = src.index('if __name__ == "__main__":')
    NS = {"__file__": f, "__name__": "qx10_i2_reused"}; argv0 = sys.argv; sys.argv = [f]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], f, "exec"), NS)
    sys.argv = argv0; return NS


# ======================================================================== Bullet child (separate process)
def bullet_child(spec):
    Q = load_qx10()
    DB1 = os.path.join(REPO, "rebuild_2026_10_22", "DB1_cluster_dark_baryons"); src = open(os.path.join(DB1, "db1_fast.py")).read()
    pre = src[:src.index("# ---------- X-COP, own replica")]
    a_ = 'OUT = open(f"db1_{MODE}{TG2}{TAG}.out", "w")'; assert pre.count(a_) == 1; pre = pre.replace(a_, "OUT = io.StringIO()")
    sys.path.insert(0, DB1); os.chdir(DB1); sys.argv = [os.path.join(DB1, "db1_fast.py"), "ce2"]
    B = {"__file__": os.path.join(DB1, "db1_fast.py"), "__name__": "db1_fast_ce2"}; so = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(pre, "db1_fast_prefix", "exec"), B)
    finally: sys.stdout = so
    GRP, GAL, MST, MGJ, MGAS, OWN, fld, SYS, BU, C, TOL, ZL, law0 = (B[k] for k in ("GRP", "GAL", "MST", "MGJ", "MGAS", "OWN", "fld", "SYS", "BU", "C", "TOL", "ZL", "law0"))
    A0B = B["A0"]

    def row(f, Rgal, Mgas_extra):
        def extra(sp, Cc, reg=True):
            a0 = sp["a0"]; gv = tuple(sum(q[i] for q in Cc["gas"]) for i in range(3)); gb = [gv[i] + Cc["st"][i] for i in range(3)]
            if reg: gb[1] = gb[1] + a0 / 1000.0
            s = Mgas_extra / MGAS; cb = [s * gv[i] for i in range(3)]
            for i, c in enumerate(GAL):
                w = Rgal[OWN.get(i, 0)]
                if w:
                    fq = fld(Cc["X"], Cc["Y"], Cc["Z"], c); cb = [cb[q] + w * fq[q] for q in range(3)]
            tot = [gb[i] + cb[i] for i in range(3)]; g = np.sqrt(tot[0] ** 2 + tot[1] ** 2 + tot[2] ** 2); m = C.law(g, a0) / np.maximum(g, 1e-300)
            return tuple(tot[i] * m - gb[i] for i in range(3))
        SYS.extra = extra
        try:
            sp = {f: dict(form="CAND", k=0.0, a0=A0B[f])}; R = BU["run"](sp); o = BU["observe"](*R[f])
        finally: SYS.extra = law0
        T = TOL["BULLET"]; zs = [(o["M300"][i] / T["obs_M300"][i] - 1) / T["sig_frac_PROVISIONAL"] for i in (0, 1)]
        ok = o["cls"] != "FAIL" and all(abs(z) <= ZL for z in zs)
        return dict(label="PASS" if ok else "FAIL", cls=o["cls"], M300=[float(x) for x in o["M300"]], ZM=zs,
                    dkappa=[o["main"]["dkappa"], o["sub"]["dkappa"]], d_gal=[o["main"]["d_bcg"], o["sub"]["d_bcg"]], d_gas=[o["main"]["d_gas"], o["sub"]["d_gas"]])

    out = dict(KA5=row("canonical", [0.0, 0.0], 0.0))
    ctr = [np.asarray(g[0], float).ravel() for g in GRP]; dsep = float(np.hypot(*(ctr[0][:2] - ctr[1][:2])))
    out["d_sep_kpc"] = dsep; out["M_star"] = [float(x) for x in MST]; out["M_gas"] = [float(x) for x in MGJ]
    for f, a0k in Q["A0K"].items():
        for cell, (l0, p) in spec["cells"].items():
            K = Q["K_of"](l0 * 1e3) * spec.get("kmul", 1.0); sols = []
            for j in range(len(GRP)):
                r, mg, ms = B["sub_profiles"](j); r = np.asarray(r, float); mb = np.asarray(mg, float) + np.asarray(ms, float)
                Mt = float(mb[-1]); host = (lambda rr, mb=mb, r=r: float(np.interp(rr, r, mb)) if rr <= r[-1] else float(mb[-1]))
                s = Q["solve_static"](host, spec["fcap"] * Q["R"] * Mt, K, Q["r_ta"](Mt), a0k); sols.append((s, Mt))
            smain = sols[0][0]; rho_main = float(np.interp(math.log(dsep), np.log(smain["r"]), smain["rho"])) if dsep < smain["r"][-1] else 0.0
            rows = {}
            for v in V_BULLET:
                Pram = rho_main * v ** 2; Rgal = []; Mstrip = 0.0; info = []
                for j, (s, Mt) in enumerate(sols):
                    Mdt = float(s["Md"][-1])
                    if j == 0 or Pram <= 0: kept = Mdt; rs = None
                    else:
                        pr = K * np.asarray(s["rho"]) ** 2; idx = np.where(pr < Pram)[0]
                        if len(idx) == 0: kept = Mdt; rs = float(s["r"][-1])
                        else: k0 = int(idx[0]); rs = float(s["r"][k0]); kept = float(s["Md"][k0 - 1]) if k0 > 0 else 0.0
                    Mstrip += Mdt - kept; Rgal.append(kept / MST[j])
                    cs2 = 2 * K * float(s["rho"][0])
                    info.append(dict(M_d=Mdt, kept=kept, r_strip_kpc=rs, Rs_kpc=s["Rs"], Mach=v / math.sqrt(cs2) if cs2 > 0 else None, P_core=K * float(s["rho"][0]) ** 2))
                b = row(f, Rgal, Mstrip) if (v == V_BULLET[0] or spec.get("all_v")) else None
                rows[f"v{int(v)}"] = dict(P_ram=Pram, rho_main_at_dsep=rho_main, subs=info, R_gal=Rgal, M_stripped=Mstrip, bullet=b)
            out[f"{f}|{cell}"] = rows
    out["child_peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("CE2CHILD " + json.dumps(out, default=float)); sys.exit(0)


if "--bullet-child" in sys.argv: bullet_child(json.loads(sys.argv[sys.argv.index("--bullet-child") + 1]))

# ======================================================================== main
P(f"CE2 {'MUTATE' if MUT else 'MAIN'}: QX7 iter_4 late-heated window at QX10 cells C1-C4, host-bound n = 1 end state. kappa = 1/2 FITTED; not theory closed.")
Q = load_qx10()
A0K, XC, GR, glaw, GK, solve_static, Mdust_at, profile_from, r_ta, K_of = (Q[k] for k in ("A0K", "XC", "GR", "glaw", "GK", "solve_static", "Mdust_at", "profile_from", "r_ta", "K_of"))
q10 = json.load(open(os.path.join(CL6, "QX10_window_hardening", "iter_2_capture_dynamics", "qx10_i2.json")))
q4 = json.load(open(os.path.join(CL6, "QX7_unified_cold_switch", "iter_4_late_evaporation", "qx7_iter4.json")))
RES = dict(lane="CE2", criteria="8e89ef6740", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed")

# R500 per X-COP cluster (header of the same file QX5 reads)
from astropy.io import fits
R500 = {}
for z in XC:
    if z["name"] not in R500:
        with fits.open(os.path.join(REPO, "real_research", "data", "xcop", z["name"], f"{z['name']}_hydro_mass.fits")) as hh: R500[z["name"]] = float(hh[1].header["R500"])
clusters = {}
for z in XC: clusters.setdefault(z["name"], []).append(z)


def xcop_grade(lam_kpc, a0k, fcap):
    K = K_of(lam_kpc); d = []; xr = []; prof = []
    for nm, pts in clusters.items():
        Ml, rl = pts[0]["Mb_last"]; host = profile_from([p_["r_kpc"] for p_ in pts], [p_["M_b"] for p_ in pts], Ml, rl)
        s = solve_static(host, fcap * Q["R"] * Ml, K, r_ta(Ml), a0k)
        mdR = Mdust_at(s, R500[nm])
        for p_ in pts:
            x = p_["r_kpc"]; md = Mdust_at(s, x); Mp = glaw(GK * (p_["M_b"] + md) / x ** 2, a0k) * x ** 2 / GK
            d.append(math.log10(p_["M_obs"] / Mp)); xr.append(x / R500[nm])
            prof.append(dict(name=nm, x=x / R500[nm], dust=md / mdR if mdR > 0 else 0.0, gas=p_["M_gas"], star=p_["M_b"] - p_["M_gas"]))
    d = np.array(d); xr = np.array(xr); bins = []
    edges = (0, 0.25, 0.5, 0.75, 1.0, 2.0)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (xr > lo) & (xr <= hi)
        if m.sum() >= 3: bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean())))
    mean, rms = float(d.mean()), float(np.sqrt((d ** 2).mean()))
    ok = abs(mean) <= 0.05 and rms <= 0.10 and all(abs(b["mean"]) <= 0.10 for b in bins)
    return dict(mean=mean, rms=rms, bins=bins, pass_=bool(ok)), prof


def needed_f(gp, fst, a0k):
    def mean_d(f):
        v = []
        for q in gp["pts"]:
            x = q["r_kpc"]; Mb = q["M_gas"] * (1 + fst); Mp = glaw(GK * (1 + f) * Mb / x ** 2, a0k) * x ** 2 / GK; v.append(math.log10(q["M_obs"] / Mp))
        return float(np.mean(v))
    if mean_d(0.0) <= 0: return 0.0
    if mean_d(30.0) > 0: return 30.0
    lo, hi = 0.0, 30.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if mean_d(mid) > 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


def groups_grade(lam_kpc, a0k, fcap):
    K = K_of(lam_kpc); res = {}
    for fst in (0.0, 1.0):
        npass = 0; rows = []
        for gp in GR:
            Mbt = gp["g5"] * (1 + fst)
            host = profile_from([q["r_kpc"] for q in gp["pts"]], [q["M_gas"] * (1 + fst) for q in gp["pts"]], Mbt, gp["R5"])
            s = solve_static(host, fcap * Q["R"] * Mbt, K, r_ta(Mbt), a0k); ok = True; dl = []
            for q in gp["pts"]:
                x = q["r_kpc"]; Mb = q["M_gas"] * (1 + fst); md = Mdust_at(s, x)
                Mp = glaw(GK * (Mb + md) / x ** 2, a0k) * x ** 2 / GK; dd = math.log10(q["M_obs"] / Mp); dl.append(dd)
                ok &= abs(dd) <= 2 * q["eM"] / (q["M_obs"] * math.log(10))
            npass += ok
            rows.append(dict(name=gp["name"], kT=gp["kT"], mean_delta=float(np.mean(dl)), pass_=bool(ok),
                             f_pred=Mdust_at(s, gp["R5"]) / host(gp["R5"]), f_need=needed_f(gp, fst, a0k)))
        lk = np.log10([r_["kT"] for r_ in rows]); md = np.array([r_["mean_delta"] for r_ in rows])
        slope = float(np.polyfit(lk, md, 1)[0]); rng = np.random.default_rng(7); bs = []
        for _ in range(2000):
            ii = rng.integers(0, len(rows), len(rows))
            if np.ptp(lk[ii]) > 0: bs.append(np.polyfit(lk[ii], md[ii], 1)[0])
        se = float(np.std(bs))
        from scipy.stats import spearmanr
        fp = np.array([r_["f_pred"] for r_ in rows]); fn = np.array([r_["f_need"] for r_ in rows])
        res[f"fst{fst:g}"] = dict(n_pass=int(npass), slope=slope, slope_se=se, trend_ok=bool(abs(slope) <= 2 * se),
                                  rho_fpred_kT=float(spearmanr(fp, lk)[0]), rho_fneed_kT=float(spearmanr(fn, lk)[0]),
                                  f_pred_median=float(np.median(fp)), f_need_median=float(np.median(fn)), rows=rows)
    res["pass_"] = bool(all(res[k]["n_pass"] >= 16 and res[k]["trend_ok"] for k in ("fst0", "fst1")))
    return res


# ---------------------------------------------------------------- KA2 (QX10 iter_2 reproduction) and KA3 (law alone)
KA = {}
ka2 = []
for c, (l0, p) in CELLS.items():
    for f, a0k in A0K.items():
        o = Q["grade_cell"](l0 * 1e3, a0k); r10 = q10["cells"][c][f]
        dX = max(abs(o["clusters"]["X_mean"] - r10["clusters"]["X_mean"]), abs(o["clusters"]["X_rms"] - r10["clusters"]["X_rms"]))
        dG = max(abs(o["clusters"]["groups_npass"][k] - r10["clusters"]["groups_npass"][k]) for k in ("fst0", "fst1"))
        d6 = abs(o["G6_mean"] - r10["G6_mean"]); ka2.append(dict(cell=c, footing=f, dX=dX, dG=dG, dG6=d6, G5=o["G5"]["pass_"], G6_mean=o["G6_mean"]))
        if MUT: break
    if MUT: break
KA["KA2"] = dict(rows=ka2, pass_=bool(all(r_["dX"] <= 1e-9 and r_["dG"] == 0 and r_["dG6"] <= 1e-9 for r_ in ka2)))
P(f"KA2 QX10 iter_2 static A reproduced: max |dX| {max(r_['dX'] for r_ in ka2):.1e}, max |dgroups| {max(r_['dG'] for r_ in ka2)}, max |dG6| {max(r_['dG6'] for r_ in ka2):.1e} -> {'PASS' if KA['KA2']['pass_'] else 'FAIL'}")
gb1 = json.load(open(os.path.join(CL6, "GB1_all_gates_battery", "gb1.json")))
ka3 = {}
for f, a0k in A0K.items():
    x0, _ = xcop_grade(2610.2, a0k, 0.0); ref = {"canonical": 0.4675, "alt": 0.4345}[f]; g = gb1["cands"]["L0"][f]["G2 X-COP"]["num"]["mean"]
    ka3[f] = dict(mean=x0["mean"], qx2=ref, gb1=g, ok=bool(abs(x0["mean"] - ref) <= 1e-3), gb1_diff=abs(x0["mean"] - g), pass_law=x0["pass_"])
KA["KA3"] = dict(rows=ka3, pass_=bool(all(v["ok"] for v in ka3.values())))
P("KA3 law alone (f_cap 0): " + "; ".join(f"{f} X-COP {v['mean']:+.4f} vs QX2 {v['qx2']:+.4f}, GB1 L0 {v['gb1']:+.4f} (|d| {v['gb1_diff']:.1e})" for f, v in ka3.items()) + f" -> {'PASS' if KA['KA3']['pass_'] else 'FAIL'}")

# ---------------------------------------------------------------- growth machinery (QX7 iter_4 prefix, read-only)
I4 = os.path.join(CL6, "QX7_unified_cold_switch", "iter_4_late_evaporation", "qx7_iter4.py")
s4 = open(I4).read(); c4 = s4.index("RES = dict(tag=TAG")
argv0 = sys.argv; sys.argv = [I4]; N4 = {"__file__": I4, "__name__": "qx7_iter4_reused"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(s4[:c4], I4, "exec"), N4)
sys.argv = argv0
N3, I2, g2gen, kJ_of, ode, OD0, h4, K1 = (N4[k] for k in ("N3", "I2", "g2gen", "kJ_of", "ode", "OD0", "h", "K1"))
solve_gen = None
for k_, v_ in N4.items():
    pass
# solve_gen lives in g2gen's globals
solve_gen = g2gen.__globals__["solve_gen"]
c0 = float(N3["c0"]); MC = N3["M"]; kgrid = N3["kgrid"]; zgrid = N3["zgrid"]; ref = N3["ref"]
KA["K1_iter4"] = dict(iter3=K1["iter3"], generalised=K1["generalised"], pass_=bool(K1["pass_"] and abs(K1["iter3"] - 55.640290726118906) <= 1e-6))
members = {}
for c, (l0, p) in CELLS.items():
    e = min((e for e in q4["evaluated"] if abs(e["p"] - p) < 1e-9), key=lambda e: abs(math.log(e["lambda_0"] / l0)))
    members[c] = e

# fsigma8
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]
hh = MC.h(); R8 = 8.0 / hh
Pref = np.array([[MC.pk_lin(k, z) for z in zgrid] for k in kgrid])
def W(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
lk = np.log(kgrid); w2k3 = W(kgrid * R8) ** 2 * kgrid ** 3 / (2 * np.pi ** 2)
def sig8(Rr):
    v = Pref * Rr ** 2 * w2k3[:, None]
    return np.sqrt((getattr(np, "trapezoid", None) or np.trapz)(v, lk, axis=0))
lna_z = np.log(1 / (1 + zgrid))
def fs8_ratio(Rr):
    from scipy.interpolate import CubicSpline
    o = np.argsort(lna_z); s_sw = sig8(Rr); s_rf = sig8(np.ones_like(Rr))
    d_sw = CubicSpline(lna_z[o], s_sw[o]).derivative()(lna_z); d_rf = CubicSpline(lna_z[o], s_rf[o]).derivative()(lna_z)
    rr = d_sw / d_rf; return {b[0]: float(np.interp(b[1], zgrid, rr)) for b in DESI}, {b[0]: float(np.interp(b[1], zgrid, s_sw / s_rf)) for b in DESI}
ka4 = fs8_ratio(np.ones_like(ref))[0]
KA["KA4"] = dict(rows=ka4, pass_=bool(all(abs(v - 1) <= 1e-6 for v in ka4.values())))
P(f"KA4 fsigma8 machinery at R = 1: max |Rf - 1| {max(abs(v - 1) for v in ka4.values()):.1e} -> {'PASS' if KA['KA4']['pass_'] else 'FAIL'}")
def fs8_gate(rf):
    rows = []
    for (t, z, r1, p1, m1, r2, p2, m2) in DESI:
        e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = rf[t]
        rows.append(dict(bin=t, z=z, Rf=x, sf=r1, sf_err=e1, sfb=r2, sfb_err=e2, s8dir=bool(x <= 1.001), in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2)))
    return dict(rows=rows, pass_=bool(all(r_["s8dir"] and r_["in_sf"] and r_["in_sfb"] for r_ in rows)))
FOREST_LINE = (0.42 / h4) / 4
def forest(lst, p): return {z: float(lst * ode(float(z)) ** p) for z in (2, 3, 4)}


def cmb_side(lst, p):
    dm = solve_gen(kJ_of(lst, p)); Rr = dm / ref
    S = I2.limber_ratio(MC, N4["H0"], kgrid, zgrid, Rr); c, _ = I2.best_amp_chi2(N3["X0"] * S); dchi = float(c - c0)
    rf, s8r = fs8_ratio(Rr); gl = dict(chi2=float(c), dchi2=dchi, pass_=bool(c <= 18.48 and dchi <= 4.0))
    fo = forest(lst, p); gfo = dict(lambda_J=fo, line=FOREST_LINE, pass_=bool(all(v <= FOREST_LINE for v in fo.values())))
    return gl, dict(fs8_gate(rf), sigma8_ratio=s8r), gfo


# ======================================================================== MAIN or MUTATE
def run_bullet(spec):
    cp = subprocess.run([sys.executable, os.path.abspath(__file__), "--bullet-child", json.dumps(spec)], capture_output=True, text=True)
    line = [l for l in cp.stdout.splitlines() if l.startswith("CE2CHILD ")]
    if cp.returncode != 0 or not line: P("bullet child failed: " + cp.stderr[-800:]); return None
    return json.loads(line[0][9:])

def dump():
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")

if not MUT:
    ka1 = {c: dict(lambda_0=e["lambda_0"], p=e["p"], record=e["dchi2"], now=g2gen(kJ_of(e["lambda_star"], e["p"]))) for c, e in members.items()}
    for v in ka1.values(): v["d"] = abs(v["now"] - v["record"])
    KA["KA1"] = dict(rows=ka1, pass_=bool(all(v["d"] <= 1e-9 for v in ka1.values()) and KA["K1_iter4"]["pass_"]))
    P(f"KA1 iter_4 G2' at C1-C4: " + ", ".join(f"{c} {v['now']:.4f} vs {v['record']:.4f}" for c, v in ka1.items()) + f"; K1 {K1['iter3']:.4f} -> {'PASS' if KA['KA1']['pass_'] else 'FAIL'}")
    spec = dict(cells={c: v for c, v in CELLS.items()}, fcap=Q["FCAP"])
    BC = run_bullet(spec)
    if BC is None: RES["label"] = "NO VERDICT (bullet child failed)"; RES["KA"] = KA; dump(); sys.exit(2)
    k0 = BC["KA5"]; KA["KA5_bullet"] = dict(M300=k0["M300"], dkappa=k0["dkappa"], pass_=bool(abs(k0["M300"][0] / 1.112e14 - 1) < 0.01 and abs(k0["M300"][1] / 7.337e13 - 1) < 0.01 and abs(k0["dkappa"][0] + 0.068) < 0.002 and abs(k0["dkappa"][1] + 0.111) < 0.002))
    P(f"KA5 Bullet, law alone: M300 {k0['M300'][0]:.4g}, {k0['M300'][1]:.4g}; dkappa {k0['dkappa'][0]:+.4f}, {k0['dkappa'][1]:+.4f} -> {'PASS' if KA['KA5_bullet']['pass_'] else 'FAIL'} (child peak RSS {BC['child_peak_rss_MB']:.0f} MB; d_sep {BC['d_sep_kpc']:.0f} kpc)")
    RES["KA"] = KA; RES["bullet_child_peak_rss_MB"] = BC["child_peak_rss_MB"]
    kaok = all(v["pass_"] for v in KA.values())
    if not kaok: P("KNOWN ANSWER FAILED: the gates it covers are NO VERDICT.")
    G = {}
    for c, (l0, p) in CELLS.items():
        e = members[c]; gl, gf, gfo = cmb_side(e["lambda_star"], e["p"]); G[c] = dict(GL=gl, GF=gf, GFo=gfo)
        P(f"[{c}] lambda_0 {e['lambda_0']:.4f} p {e['p']}: GL chi2 {gl['chi2']:.2f} dchi2 {gl['dchi2']:.2f} -> {'PASS' if gl['pass_'] else 'FAIL'}; "
          f"GF Rf " + " ".join(f"{r_['bin']} {r_['Rf']:.3f}" for r_ in gf["rows"]) + f" -> {'PASS' if gf['pass_'] else 'FAIL'}; "
          f"GFo lambda_J(z2,3,4) " + " ".join(f"{v:.3g}" for v in gfo["lambda_J"].values()) + f" Mpc (line {FOREST_LINE:.3g}) -> {'PASS' if gfo['pass_'] else 'FAIL'}")
        for f, a0k in A0K.items():
            gx, prof = xcop_grade(l0 * 1e3, a0k, Q["FCAP"]); gg = groups_grade(l0 * 1e3, a0k, Q["FCAP"])
            bb = BC[f"{f}|{c}"]; b0 = bb["v2700"]["bullet"]; gb = dict(label=b0["label"], detail=bb, pass_=b0["label"] == "PASS")
            # band reading: median normalised dust vs gas/star normalised profiles per bin
            band = []
            for lo, hi in ((0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0), (1.0, 2.0)):
                rr = [x for x in prof if lo < x["x"] <= hi]
                if len(rr) >= 3:
                    nm_g = {};
                    band.append(dict(lo=lo, hi=hi, dust=float(np.median([x["dust"] for x in rr]))))
            G[c][f] = dict(GX=gx, GG={k: (v if k == "pass_" else {kk: vv for kk, vv in v.items() if kk != "rows"}) for k, v in gg.items()}, GG_rows=gg, GB=gb, band=band)
            s1 = bb["v2700"]["subs"][1]; s47 = bb["v4700"]["subs"][1]
            P(f"   [{f}] GX mean {gx['mean']:+.3f} rms {gx['rms']:.3f} bins " + " ".join(f"{b['mean']:+.2f}" for b in gx["bins"]) + f" -> {'PASS' if gx['pass_'] else 'FAIL'}")
            P(f"   [{f}] GG fst0 {gg['fst0']['n_pass']}/20 slope {gg['fst0']['slope']:+.3f}+-{gg['fst0']['slope_se']:.3f}; fst1 {gg['fst1']['n_pass']}/20 slope {gg['fst1']['slope']:+.3f}+-{gg['fst1']['slope_se']:.3f}; "
              f"f_pred med {gg['fst0']['f_pred_median']:.2f} (rho_kT {gg['fst0']['rho_fpred_kT']:+.2f}) vs f_need med {gg['fst0']['f_need_median']:.2f} (rho_kT {gg['fst0']['rho_fneed_kT']:+.2f}) -> {'PASS' if gg['pass_'] else 'FAIL'}")
            P(f"   [{f}] GB v 2700: sub sector kept {s1['kept']/max(s1['M_d'],1e-30):.2f} (Mach {s1['Mach'] if s1['Mach'] is None else round(s1['Mach'],2)}), M_stripped {bb['v2700']['M_stripped']:.3g}; bullet {b0['label']} ({b0['cls']}, ZM {b0['ZM'][0]:+.2f}/{b0['ZM'][1]:+.2f}, d_gal {b0['d_gal'][1]:.0f} d_gas {b0['d_gas'][1]:.0f}); v 4700 kept {s47['kept']/max(s47['M_d'],1e-30):.2f}")
    RES["gates"] = G
    lab = {}
    for c in CELLS:
        fails = []
        for gname in ("GL", "GF", "GFo"):
            if not G[c][gname]["pass_"]: fails.append(gname)
        for f in A0K:
            for gname in ("GX", "GG", "GB"):
                if not G[c][f][gname]["pass_"]: fails.append(f"{gname}[{f}]")
        lab[c] = dict(pass_=not fails, blocking=fails)
    RES["cells_label"] = lab
    anyp = any(v["pass_"] for v in lab.values())
    L = ("NO VERDICT (known answer failed)" if not kaok else "PASSES CE2, CANDIDATE PENDING KX1" if anyp else "FAIL")
    RES["label"] = L
    for c, v in lab.items(): P(f"  {c}: {'PASS' if v['pass_'] else 'FAIL: ' + ', '.join(v['blocking'])}")
    P(f"LABEL: {L}")
else:
    MU = {}
    # M1 no heating, KD1's background ratio
    Q["R"] = R_QX15; fc = Q["FCAP"] * Q["R"]
    o = Q["grade_cell"](1.0, A0K["canonical"]); gx, _ = xcop_grade(1.0, A0K["canonical"], Q["FCAP"])
    bite = abs(fc - 4.1110) <= 1e-3 and ((not o["G5"]["pass_"]) or abs(o["G6_mean"] - Q["baselines"](A0K["canonical"])[0]) > 0.05) and gx["mean"] < -0.3
    MU["M1"] = dict(f_capture=fc, G5_pass=o["G5"]["pass_"], G6_mean=o["G6_mean"], X_mean=gx["mean"], bites=bool(bite))
    P(f"M1 no heating (lambda_0 1 kpc, R {Q['R']:.4f}): captured ratio {fc:.4f} vs KD1 4.1110; G5 {'PASS' if o['G5']['pass_'] else 'FAIL'}, G6 mean {o['G6_mean']:+.3f}; X-COP mean {gx['mean']:+.3f} -> {'BITES' if bite else 'NO BITE'}")
    Q["R"] = 0.11958060485606123 / 0.0215
    gx0, _ = xcop_grade(2610.2, A0K["canonical"], 0.0); MU["M2"] = dict(X_mean=gx0["mean"], GX_pass=gx0["pass_"], bites=bool(not gx0["pass_"]))
    P(f"M2 f_cap 0: X-COP {gx0['mean']:+.4f} -> GX {'PASS' if gx0['pass_'] else 'FAIL'} -> {'BITES' if not gx0['pass_'] else 'NO BITE'}")
    e = members["C1"]; gl, gf, gfo = cmb_side(10 * e["lambda_star"], e["p"]); b3 = not (gl["pass_"] and gf["pass_"])
    MU["M3"] = dict(GL=gl, GF_rows=gf["rows"], GF_pass=gf["pass_"], bites=bool(b3))
    P(f"M3 lambda_* x10 at C1: GL chi2 {gl['chi2']:.2f} dchi2 {gl['dchi2']:.2f}; GF Rf " + " ".join(f"{r_['bin']} {r_['Rf']:.3f}" for r_ in gf["rows"]) + f" -> {'BITES' if b3 else 'NO BITE'}")
    RES["MUTATE"] = MU; RES["KA"] = KA
    P("MUTATE: " + ("ALL BITE" if all(v["bites"] for v in MU.values()) else "NOT ALL BITE"))
P("kappa = 1/2 FITTED; not theory closed.")
dump()
