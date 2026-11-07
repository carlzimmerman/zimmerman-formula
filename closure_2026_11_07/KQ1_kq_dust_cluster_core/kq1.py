#!/usr/bin/env python3
"""KQ1 (criteria 07534f282b): can v3s's K(Q) dust (cold dark energy, n = 1 polytrope, Jeans wavenumber mu_K) in
hydrostatic equilibrium in the law's field of X-COP baryons + itself form NC4's cored cluster profile?
    python3 kq1.py            -> kq1.json / kq1.out
    python3 kq1.py --mutate   -> kq1_MUTATE.json / kq1_MUTATE.out   (M1 mu -> inf = KD1 cusp, M2 law alone, M3 planted)
Read-only: NA2's na2.py prefix (which executes QX7 iter_5's prelude incl. its host-hydrostatic `profile` solver),
NC4's cored shape (copied formula), KD1 kd1.json + its KD candidate (copied), GB1 gb1.py prefix (features, gates),
QX7 iter_5 qx7_iter5.json (recorded galaxy gates). One thread. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, signal, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07")
MUT = "--mutate" in sys.argv; TAG = "kq1_MUTATE" if MUT else "kq1"; OUT = []
RES = dict(lane="KQ1", criteria="07534f282b", tag=TAG, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
def P(s=""): print(s, flush=True); OUT.append(s)
def dump(tag=TAG):
    RES["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6      # macOS: bytes
    json.dump(RES, open(os.path.join(HERE, tag + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
def _term(sig, frm):
    RES["interrupted"] = "SIGTERM"; dump(TAG + "_partial"); sys.exit(3)
signal.signal(signal.SIGTERM, _term)

def load_prefix(path, marker, name, quiet=True):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}
    a = sys.argv; sys.argv = [path]; so = sys.stdout
    if quiet: sys.stdout = io.StringIO()
    try: exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a; sys.stdout = so
    return ns

# ------------------------------------------------------------------ NA2 prefix (-> iter_5 prelude + solver), read-only
NA = load_prefix(os.path.join(CL7, "NA2_compact_baryon_remnant", "na2.py"), "# ------------------------------------------------------------------ GB1 battery", "na2_prefix")
I5 = NA["NS"]
A0, XC, KPC, MS, G, glaw = (NA[k] for k in ("A0", "XC", "KPC", "MS", "G", "glaw"))
XINFO, SH, x_eval, BIN_EDGES = NA["XINFO"], NA["SH"], NA["x_eval"], NA["BIN_EDGES"]
profile, XPROF, r_ta0, FCAP, RR, dust = I5["profile"], I5["XPROF"], I5["r_ta0"], I5["FCAP"], I5["R"], I5["dust"]
MPC = 1e3 * KPC; XN = sorted(XINFO)
KDJ = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
I5J = json.load(open(os.path.join(CL6, "QX7_unified_cold_switch", "iter_5_host_hydrostatic", "qx7_iter5.json")))
FX = {f: KDJ["footings"][f]["uniform_f_diag"]["Xcop_f_need"] for f in A0}
CAPF = {f: KDJ["footings"][f]["uniform_f_diag"]["capture_f"] for f in A0}
SPCAP = {f: KDJ["footings"][f]["uniform_f_diag"]["SPARC_f_max"] for f in A0}
MU_BBN = {f: KDJ["footings"][f]["B1"]["mu_B1b"] for f in A0}
MU_GAL, MU_S4, MU_J_GL1 = 79.43282347242821, 0.1, 631.0
QK = {"canonical": 0.017, "alt": 0.016}   # X14 F5(d): q_K at mu_K 0.1, l 156 kpc
KA = {}; RES["KA"] = KA
P(f"KQ1 {'MUTATE' if MUT else 'MAIN'}: K(Q) dust host-hydrostatic in the law's field at X-COP. X-COP {XN}. kappa = 1/2 FITTED; not theory closed.")
P(f"F_X (KD1 need) {FX}; capture {CAPF}; SPARC cap {SPCAP}; mu_BBN {MU_BBN}")

# ------------------------------------------------------------------ GB1 prefix + KD1's KD candidate (copied from kd1.py)
GB = load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
GMSUN, PCm = 4.30091e-9, GB["PC"]
_ss = GB["ss_feat"]; GB["ss_feat"] = lambda a0, r: dict(_ss(a0, r), nodust=True)
def msys_rrM(ft, a0): return (ft["r"] / ft["rrM"]) ** 2 * a0 / GB["G"] / GB["MS"]
BATT = {}
for f, a0 in A0.items():
    S, E, X = GB["build"](f, a0)
    for p in S + E + X: p["feat"]["Msys"] = msys_rrM(p["feat"], a0); p["feat"]["Mb_enc"] = p["feat"]["Mb"]
    BATT[f] = dict(S=S, E=E, X=X, rms_L0=float(np.sqrt(np.mean([p["D"] ** 2 for p in S]))))
def enc(xi): return 1.0 if xi >= math.pi else (math.sin(xi) - xi * math.cos(xi)) / math.pi
def mj_of(ob, od, h, mu):
    rhoc0 = 3 * (100 * h) ** 2 / (8 * math.pi * GMSUN); rho_ta = 5.55 * (ob + od) / h ** 2 * rhoc0 * 27.0
    return 4 * math.pi / 3 * rho_ta * (math.pi / mu) ** 3
def KD(ob, od, h, mu, stats=None, frac=None):
    ratio = FCAP * od / ob if od > 1e-6 else 0.0; MJ = mj_of(ob, od, h, mu)
    def c(ft):
        if ft.get("nodust") or ratio == 0.0: return dict(b=1.0, F=1.0, T=0.0)
        Ms_, Me = GB["need"](ft, "Msys"), GB["need"](ft, "Mb_enc")
        cap = Ms_ * (ob + od) / ob > MJ
        if stats is not None: stats["n"] += 1; stats["captured"] += cap
        if not cap: return dict(b=1.0, F=1.0, T=0.0)
        e_ = enc(mu * ft["r"] / (1e6 * PCm)) if frac is None else frac
        return dict(b=1.0 + ratio * Ms_ * e_ / Me, F=1.0, T=0.0)
    return c
def setting(f): s = KDJ["footings"][f]["setting"]; return s["omega_b"], s["omega_d"], s["h"]
def galaxy_row(f, mu):
    ob, od, h = setting(f); st = dict(n=0, captured=0); ok, num = GB["g_sparc"](KD(ob, od, h, mu, st), BATT[f], A0[f])
    lam = 2 * math.pi / mu; keys = sorted(I5J["galaxy_gates_by_lambda0"], key=lambda k: abs(math.log(float(k) / lam)))
    k = keys[0]; g5, g6, g7 = I5J["galaxy_gates_by_lambda0"][k]
    return dict(M_J=mj_of(ob, od, h, mu), sparc_points_captured=st["captured"], sparc_points=st["n"], G1=("PASS" if ok else "FAIL"),
                G1_Z=num["Z"], G1_rms=num["rms"], G1_rms_line=num["rms_line"], capture_f=CAPF[f], sparc_cap=SPCAP[f],
                iter5_hostheld_lambda0=float(k), iter5_G5_G6_G7=[bool(g5), bool(g6), bool(g7)])

# ------------------------------------------------------------------ line calculators
def solve(n, f, mu, Mtot):
    fx, Ml = XPROF[n]; rs, r, M = profile(fx, Mtot, 2 * math.pi / mu, A0[f])
    dM = np.gradient(M, r); rho = dM / (4 * math.pi * r ** 2)
    # A1: the solver starts M = 0 at r_min, so np.gradient's one-sided ends spoil rho at the first two grid points;
    # the line calculators (rho(0), r_1/2, slope) use the grid from index 2 on.
    return dict(rs=rs, r=r, M=M, rho=rho, Mtot=Mtot, rl=r[2:], rhol=rho[2:])
def Md_of(S_, r_m): return np.where(np.asarray(r_m, float) >= S_["rs"], S_["Mtot"], np.interp(np.asarray(r_m, float), S_["r"], S_["M"]))
def r_half(r, rho):
    rho0 = rho[0]; i = np.where(rho <= 0.5 * rho0)[0]
    if not len(i): return None
    j = i[0]
    if j == 0: return float(r[0])
    t = (rho[j - 1] - 0.5 * rho0) / (rho[j - 1] - rho[j]); return float(r[j - 1] + t * (r[j] - r[j - 1]))
def max_slope_in(r, rho, rmax):
    m = (r <= rmax) & (rho > 0); lr, lp = np.log(r[m]), np.log(rho[m])
    if m.sum() < 3: return float("inf")
    s = np.gradient(lp, lr); return float(np.max(np.abs(s)))
def slope_at(r, rho, rr):
    lr, lp = np.log(r), np.log(np.maximum(rho, 1e-300)); s = np.gradient(lp, lr); return float(np.interp(math.log(rr), lr, s))
def xeval_md(f, mdfun):
    """L4 evaluator: NA2's x_eval statistic with an arbitrary M_d(<r) [Msun] per cluster (r in m)."""
    a0 = A0[f]; d = []; xr = []
    for z in XC:
        rm = z["r_kpc"] * KPC; md = float(mdfun[z["name"]](np.array([rm]))[0]) if mdfun else 0.0
        Mp = glaw(G * (z["M_b"] + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS
        d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / XINFO[z["name"]]["r500"])
    d = np.array(d); xr = np.array(xr); bins = []
    for lo, hi in zip(BIN_EDGES[:-1], BIN_EDGES[1:]):
        m = (xr >= lo) & (xr < hi); bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None))
    mean, rms = float(d.mean()), float(np.sqrt((d ** 2).mean()))
    gb = [b for b in bins if b["n"] >= 3]; maxbin = max(abs(b["mean"]) for b in gb)
    return dict(mean=mean, rms=rms, bins=bins, max_abs_bin=maxbin, inner_bin=bins[0]["mean"],
                L4=bool(rms <= 0.10 and maxbin <= 0.10), NA2_gate=bool(abs(mean) <= 0.05 and rms <= 0.10 and maxbin <= 0.10))
L1_LO, L1_HI, L2_MAX, L3P, L3S = 49.5, 100.5, 0.5, (0.2475, 0.2665), (0.21, 0.30)
def lines_from(f, per, xe, retained):
    rh = [per[n]["r_half_kpc"] for n in XN]; sl = [per[n]["max_slope_20kpc"] for n in XN]; cc = [per[n]["conc"] for n in XN]
    L1 = all(x is not None and L1_LO <= x <= L1_HI for x in rh); L2 = all(s <= L2_MAX for s in sl)
    L3 = all(L3P[0] <= c <= L3P[1] for c in cc); L3s = all(L3S[0] <= c <= L3S[1] for c in cc); L4 = xe["L4"]; L5 = all(retained.values())
    return dict(L1=bool(L1), L2=bool(L2), L3=bool(L3), L3_secondary=bool(L3s), L4=bool(L4), L5=bool(L5),
                n_fail=int(5 - sum([L1, L2, L3, L4, L5])), n_fail_secondary=int(5 - sum([L1, L2, L3s, L4, L5])),
                r_half_range=[min((x for x in rh if x is not None), default=None), max((x for x in rh if x is not None), default=None)],
                max_slope_20kpc=max(sl), conc_range=[min(cc), max(cc)], rms=xe["rms"], mean=xe["mean"], inner_bin=xe["inner_bin"],
                max_abs_bin=xe["max_abs_bin"], NA2_gate=xe["NA2_gate"],
                margins=dict(L1=[(min(x for x in rh if x is not None) - L1_LO) if any(x is not None for x in rh) else None,
                                 (L1_HI - max(x for x in rh if x is not None)) if any(x is not None for x in rh) else None],
                             L2=L2_MAX - max(sl), L3=[min(cc) - L3P[0], L3P[1] - max(cc)], L4_rms=0.10 - xe["rms"], L4_bin=0.10 - xe["max_abs_bin"]))
def cell(f, mu, F=None, norm="total"):
    per = {}; md = {}; ret = {}
    for n in XN:
        Ml = XINFO[n]["Mlast"]; Ft = FX[f] if F is None else F; T = Ft * Ml
        S_ = solve(n, f, mu, T)
        if norm == "tl":                                       # bracket: M_d(<tl) = F Mlast (3 fixed-point steps)
            for _ in range(3):
                inside = float(Md_of(S_, np.array([XINFO[n]["tl"] * KPC]))[0]); T = T * Ft * Ml / inside; S_ = solve(n, f, mu, T)
        r_k = S_["r"] / KPC; r5 = XINFO[n]["r500"]
        Mq = Md_of(S_, np.array([0.25 * r5, 0.7 * r5]) * KPC)
        ret[n] = bool(S_["rs"] / MPC < r_ta0(XPROF[n][1]))
        per[n] = dict(r_s_kpc=S_["rs"] / KPC, r_ta0_kpc=r_ta0(XPROF[n][1]) * 1e3, retained=ret[n], Mtot_over_Mlast=S_["Mtot"] / Ml,
                      r_half_kpc=r_half(S_["rl"] / KPC, S_["rhol"]), max_slope_20kpc=max_slope_in(S_["rl"] / KPC, S_["rhol"], 20.0),
                      conc=float(Mq[0] / Mq[1]), frac_in_tl=float(Md_of(S_, np.array([XINFO[n]["tl"] * KPC]))[0] / S_["Mtot"]))
        md[n] = (lambda r, S_=S_: Md_of(S_, r))
    xe = xeval_md(f, md); L = lines_from(f, per, xe, ret)
    return dict(mu=mu, lambda0_Mpc=2 * math.pi / mu, per_cluster=per, xeval=xe, lines=L), md

# ------------------------------------------------------------------ KA1, KA2, KA3, KA4 (both runs)
ok1 = True
for f in A0:
    xe0 = xeval_md(f, None); na = x_eval(f, "baryon", 0.0); ref = GB["KA20"][f]["X"]
    gx = GB["g_xcop"](lambda ft: dict(b=1.0, F=1.0, T=0.0), BATT[f], A0[f])[1]["mean"]
    o = dict(mine=xe0["mean"], na2=na["mean"], gb1_gxcop=gx, ref=ref, L4=xe0["L4"])
    o["ok"] = bool(abs(xe0["mean"] - ref) <= 1e-6 and abs(na["mean"] - xe0["mean"]) <= 1e-12 and abs(gx - ref) <= 1e-6); ok1 &= o["ok"]
    KA[f"KA1_{f}"] = o; P(f"[{f}] KA1 law alone: X-COP mean {xe0['mean']:.6f} (NA2 {na['mean']:.6f}, GB1 g_xcop {gx:.6f}) vs {ref} -> {'PASS' if o['ok'] else 'FAIL'}")
ref2 = {"canonical": dict(X=4.1786, cap=4.1110, m=-0.70286, r=0.80268), "alt": dict(X=3.7833, cap=4.1121, m=-0.71439, r=0.80949)}
for f in A0:
    ob, od, h = setting(f); mus = KDJ["footings"][f]["mu_star"]; ok_, num = GB["g_xcop"](KD(ob, od, h, mus), BATT[f], A0[f])
    rec = KDJ["footings"][f]["static"]["G2 X-COP"]["num"]
    o = dict(F_X=FX[f], capture=CAPF[f], G2_mean=num["mean"], G2_rms=num["rms"], rec_mean=rec["mean"], rec_rms=rec["rms"])
    o["ok"] = bool(abs(FX[f] - ref2[f]["X"]) <= 1e-4 and abs(CAPF[f] - ref2[f]["cap"]) <= 1e-4 and abs(num["mean"] - rec["mean"]) <= 1e-6
                   and abs(num["rms"] - rec["rms"]) <= 1e-6 and abs(num["mean"] - ref2[f]["m"]) <= 1e-5)
    KA[f"KA2_{f}"] = o; P(f"[{f}] KA2 KD1: F_X {FX[f]:.4f}, capture {CAPF[f]:.4f}; KD at mu* {mus:.4e}: G2 {num['mean']:.6f} / {num['rms']:.6f} vs kd1.json {rec['mean']:.6f} / {rec['rms']:.6f} -> {'PASS' if o['ok'] else 'FAIL'}")
# KA3: isolated Newtonian core, and iter_5's recorded lambda_0 3.162 X-COP row
mu_t = 5.0; rs_iso, _, _ = profile(lambda r: 0 * r, 1e12, 2 * math.pi / mu_t, A0["canonical"], host=False, law=False)
k3a = abs(rs_iso / MPC / (math.pi / mu_t) - 1)
lam = 10 ** 0.5; k3 = dict(iso_rel_err=k3a)
ok3 = k3a <= 1e-5
for f in A0:
    d = []
    for z in XC:
        fx, Mt = XPROF[z["name"]]; rm = z["r_kpc"] * KPC; md = float(dust(("X", z["name"]), fx, Mt, lam, A0[f])[0](rm))
        Mp = glaw(G * (z["M_b"] + md) * MS / rm ** 2, A0[f]) * rm ** 2 / G / MS; d.append(math.log10(z["M_obs"] / Mp))
    d = np.array(d); rec = I5J["reported_clusters_iter4_window"]["3.162"][f]
    k3[f] = dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), rec_mean=rec["X_mean"], rec_rms=rec["X_rms"])
    ok3 &= abs(d.mean() - rec["X_mean"]) <= 2e-3 and abs(np.sqrt((d ** 2).mean()) - rec["X_rms"]) <= 2e-3
k3["ok"] = bool(ok3); KA["KA3_solver"] = k3
P(f"KA3 solver: isolated Newtonian r_s/(pi/mu) - 1 = {k3a:.2e}; iter_5 lambda_0 3.162: canonical {k3['canonical']['mean']:+.4f}/{k3['canonical']['rms']:.4f} "
  f"(rec {k3['canonical']['rec_mean']:+.4f}/{k3['canonical']['rec_rms']:.4f}), alt {k3['alt']['mean']:+.4f}/{k3['alt']['rms']:.4f} "
  f"(rec {k3['alt']['rec_mean']:+.4f}/{k3['alt']['rec_rms']:.4f}) -> {'PASS' if ok3 else 'FAIL'}")
rg = np.geomspace(0.01, 5000, 20000); rho_iso = 1 / (1 + (rg / 100.0) ** 2)
k4 = dict(r_half=r_half(rg, rho_iso), slope20=slope_at(rg, rho_iso, 20.0), max_slope_20=max_slope_in(rg, rho_iso, 20.0))
k4["ok"] = bool(abs(k4["r_half"] - 100) <= 0.5 and abs(k4["slope20"] + 0.0769) <= 0.005); KA["KA4_calculators"] = k4
P(f"KA4 calculators on cored isothermal r_c 100: r_1/2 {k4['r_half']:.3f} kpc, slope at 20 kpc {k4['slope20']:+.4f} -> {'PASS' if k4['ok'] else 'FAIL'}")
# KA5 (A1): line calculators on the solver's own grid: isolated Newtonian core (sinc), r_1/2 = 1.895494/mu, slope at r -> 0 ~ 0
mu5 = 5.0; rs5, r5g, M5g = profile(lambda r: 0 * r, 1e12, 2 * math.pi / mu5, A0["canonical"], host=False, law=False)
rho5 = np.gradient(M5g, r5g) / (4 * math.pi * r5g ** 2); rh5 = r_half(r5g[2:] / KPC, rho5[2:]); ex5 = 1.895494267 / mu5 * 1e3
sl5 = max_slope_in(r5g[2:] / KPC, rho5[2:], 20.0); exs5 = (lambda x: abs(x / math.tan(x) - 1))(mu5 * 0.020)
KA["KA5_solver_grid"] = dict(r_half=rh5, expected=ex5, max_slope_20=sl5, expected_slope=exs5,
                             ok=bool(abs(rh5 / ex5 - 1) <= 1e-3 and abs(sl5 - exs5) <= 2e-3))
P(f"KA5 calculators on the solver grid (isolated sinc, mu 5): r_1/2 {rh5:.3f} vs {ex5:.3f} kpc; max slope <= 20 kpc {sl5:.5f} vs {exs5:.5f} -> {'PASS' if KA['KA5_solver_grid']['ok'] else 'FAIL'}")
KA_OK = all(v["ok"] for v in KA.values()); RES["KA_all"] = KA_OK
if not KA_OK:
    RES["label"] = "NO VERDICT (KA FAIL)"; P("KA FAIL -> NO VERDICT; nothing graded."); dump(); sys.exit(0)

def cored_shape(rc):                                    # NC4's gamma 2 cored shape, M(<r) up to a constant (r in kpc)
    return lambda rk: (lambda x: x - np.arctan(x))(np.asarray(rk, float) / rc)
def show(f, c, tag=""):
    L = c["lines"]
    P(f"[{f}] {tag}mu {c['mu']:9.4g} (lambda0 {c['lambda0_Mpc']:.3g} Mpc): r_1/2 {L['r_half_range'][0] if L['r_half_range'][0] is not None else float('nan'):7.1f}-"
      f"{L['r_half_range'][1] if L['r_half_range'][1] is not None else float('nan'):7.1f} kpc [{'P' if L['L1'] else 'F'}], slope<=20kpc {L['max_slope_20kpc']:6.3f} [{'P' if L['L2'] else 'F'}], "
      f"c {L['conc_range'][0]:.3f}-{L['conc_range'][1]:.3f} [{'P' if L['L3'] else 'F'}{'/p' if L['L3_secondary'] else '/f'}], rms {L['rms']:.3f} mean {L['mean']:+.3f} "
      f"bins {','.join('%+.2f' % b['mean'] for b in c['xeval']['bins'] if b['mean'] is not None)} [{'P' if L['L4'] else 'F'}], retained {'P' if L['L5'] else 'F'}; fails {L['n_fail']}")

# =================================================================== MUTATE
if MUT:
    MU = {}
    for f in A0:
        ob, od, h = setting(f); mus = KDJ["footings"][f]["mu_star"]
        for mu in (mus, 1e9):
            fr = []; rh = []
            for n in XN:
                Ml = XINFO[n]["Mlast"]; S_ = solve(n, f, mu, FX[f] * Ml)
                rr = np.array([z["r_kpc"] for z in XC if z["name"] == n]) * KPC; fr.append(float(np.min(Md_of(S_, rr) / S_["Mtot"])))
                rh.append(r_half(S_["rl"] / KPC, S_["rhol"]))
            fmin = min(fr); ok_, num = GB["g_xcop"](KD(ob, od, h, mus, frac=fmin), BATT[f], A0[f]); rec = KDJ["footings"][f]["static"]["G2 X-COP"]["num"]
            m1 = dict(mu=mu, min_enclosed_fraction=fmin, G2_mean=num["mean"], G2_rms=num["rms"], kd1_mean=rec["mean"], max_r_half_kpc=max(rh),
                      L1_fails=bool(max(rh) < 1.0))
            m1["bites"] = bool(abs(num["mean"] - rec["mean"]) <= 1e-6 and abs(num["rms"] - rec["rms"]) <= 1e-6 and m1["L1_fails"])
            MU[f"M1_{f}_mu{mu:.4g}"] = m1
            P(f"[{f}] M1 mu {mu:.4g}: min enclosed fraction at X-COP radii {fmin:.12f}; KD1 model P with it: G2 {num['mean']:.6f}/{num['rms']:.6f} vs KD1 {rec['mean']:.6f}; "
              f"max r_1/2 {max(rh):.3e} kpc -> L1 {'FAILS' if m1['L1_fails'] else 'passes'} -> {'BITES (KD1 cusp)' if m1['bites'] else 'NO BITE'}")
        xe0 = xeval_md(f, None); MU[f"M2_{f}"] = dict(mean=xe0["mean"], rms=xe0["rms"], L4=xe0["L4"], bites=bool(abs(xe0["mean"] - GB["KA20"][f]["X"]) <= 1e-6 and not xe0["L4"]))
        P(f"[{f}] M2 law alone: mean {xe0['mean']:.6f} rms {xe0['rms']:.4f}, L4 {'PASS' if xe0['L4'] else 'FAIL'} -> {'BITES' if MU[f'M2_{f}']['bites'] else 'NO BITE'}")
        # M3 planted: NC4's cored isothermal r_c 100 kpc at the need amount, NA2 install (M(<tl) = F_X Mlast, constant beyond)
        per = {}; md = {}
        for n in XN:
            m = cored_shape(100.0); tl = XINFO[n]["tl"]; t = float(m(np.array([tl]))[0]); Ml = XINFO[n]["Mlast"]; r5 = XINFO[n]["r500"]
            md[n] = (lambda r_m, m=m, t=t, tl=tl, Ml=Ml: FX[f] * Ml * np.where(np.asarray(r_m, float) / KPC > tl, 1.0, m(np.asarray(r_m, float) / KPC) / t))
            rho = 1 / (1 + (rg / 100.0) ** 2)
            per[n] = dict(r_half_kpc=r_half(rg, rho), max_slope_20kpc=max_slope_in(rg, rho, 20.0), conc=float(m(np.array([0.25 * r5]))[0] / m(np.array([0.7 * r5]))[0]))
        xe = xeval_md(f, md); L = lines_from(f, per, xe, {n: True for n in XN})
        MU[f"M3_{f}"] = dict(lines=L, xeval=xe, holds=bool(L["L1"] and L["L2"] and L["L3"] and L["L4"]))
        P(f"[{f}] M3 planted r_c 100 at need: r_1/2 {L['r_half_range'][0]:.1f}, slope {L['max_slope_20kpc']:.3f}, c {L['conc_range'][0]:.4f}-{L['conc_range'][1]:.4f}, "
          f"rms {xe['rms']:.4f} bins {','.join('%+.3f' % b['mean'] for b in xe['bins'] if b['mean'] is not None)} -> L1-L4 {'PASS: HOLDS' if MU[f'M3_{f}']['holds'] else 'FAIL'}")
    RES["MUTATE"] = MU
    RES["MUTATE_ok"] = bool(all(v.get("bites", v.get("holds")) for v in MU.values()))
    P(f"MUTATE all bite / hold: {RES['MUTATE_ok']}"); P("Adopts nothing. kappa = 1/2 FITTED; not theory closed."); dump(); sys.exit(0)

# =================================================================== MAIN grid
GRID = sorted(set(np.round(np.logspace(-1, 4, 26), 10).tolist()) | {MU_GAL, MU_J_GL1})
RES["grid"] = GRID; FO = {}
for f in A0:
    rows = []
    for mu in GRID:
        c, _ = cell(f, mu); c["galaxy"] = galaxy_row(f, mu); rows.append(c); show(f, c)
        g = c["galaxy"]
        P(f"[{f}]        galaxy cost: capture {g['capture_f']:.3f} vs SPARC cap {g['sparc_cap']:.4f}; KD1 model P at this mu: M_J {g['M_J']:.3e} Msun, "
          f"SPARC points captured {g['sparc_points_captured']}/{g['sparc_points']}, G1 {g['G1']} (Z {g['G1_Z']:+.3f}, rms {g['G1_rms']:.3f} line {g['G1_rms_line']:.3f}); "
          f"iter_5 host-held G5/G6/G7 at lambda0 {g['iter5_hostheld_lambda0']:.3g}: {g['iter5_G5_G6_G7']}")
        RES.setdefault("footings", {})[f] = dict(rows=rows)
    # pre-stated refinement around the best grid point
    best = min(rows, key=lambda c: (c["lines"]["n_fail"], c["lines"]["rms"])); i = GRID.index(best["mu"])
    lo, hi = GRID[max(i - 1, 0)], GRID[min(i + 1, len(GRID) - 1)]
    ref = []
    for mu in np.geomspace(lo, hi, 6)[1:-1]:
        c, _ = cell(f, float(mu)); c["galaxy"] = galaxy_row(f, float(mu)); ref.append(c); show(f, c, "refine ")
    allr = rows + ref
    best = min(allr, key=lambda c: (c["lines"]["n_fail"], c["lines"]["rms"]))
    near75 = min(allr, key=lambda c: abs(np.median([c["per_cluster"][n]["r_half_kpc"] or 1e9 for n in XN]) - 75.0))
    passing = [c["mu"] for c in allr if c["lines"]["n_fail"] == 0]
    passing_sec = [c["mu"] for c in allr if c["lines"]["n_fail_secondary"] == 0]
    # reported: best fitted amount at the closest mu (coarse F grid), and the M_d(<tl) normalisation bracket
    fit = []
    for Fm in (1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0):
        c, _ = cell(f, best["mu"], F=Fm); fit.append(dict(F=Fm, rms=c["xeval"]["rms"], mean=c["xeval"]["mean"], bins=[b["mean"] for b in c["xeval"]["bins"]], lines=c["lines"]))
    fbest = min(fit, key=lambda x: x["rms"])
    br, _ = cell(f, best["mu"], norm="tl")
    FO[f] = dict(rows=rows, refine=ref, closest=best, nearest_r_half_75=near75, passing_mu=passing, passing_mu_secondary=passing_sec,
                 fitted_amount_at_closest=dict(grid=fit, best=fbest), bracket_Mtl_at_closest=br)
    RES["footings"][f] = FO[f]
    show(f, best, "CLOSEST ")
    show(f, near75, "r_1/2~75 ")
    P(f"[{f}] closest mu, amount free (F grid 1-12): best F {fbest['F']} rms {fbest['rms']:.3f} mean {fbest['mean']:+.3f} bins {','.join('%+.2f' % b for b in fbest['bins'] if b is not None)}")
    show(f, br, "closest, M_d(<tl) = F_X Mlast bracket: ")
    P(f"[{f}] passing mu (primary): {passing}; (secondary c band): {passing_sec}")
    dump(TAG + "_partial")

# ------------------------------------------------------------------ label
pc, pa = set(FO["canonical"]["passing_mu"]), set(FO["alt"]["passing_mu"]); both = sorted(pc & pa)
if both:
    inside = [m for m in both if m <= MU_GAL]
    lab = (f"FORMS CORE (scoped), mu_K {inside}" if inside else f"FORMS CORE, mu_K EXCLUDED, mu_K {both}")
else:
    lab = "CANNOT FORM CORE"
ps = sorted(set(FO["canonical"]["passing_mu_secondary"]) & set(FO["alt"]["passing_mu_secondary"]))
RES["label"] = lab; RES["secondary_label_reading"] = ("passes with the secondary band at mu_K " + str(ps)) if ps else "CANNOT FORM CORE (secondary band too)"
for f in A0:
    c = FO[f]["closest"]; L = c["lines"]
    P(f"[{f}] closest profile: mu_K {c['mu']:.4g} Mpc^-1 (lambda0 {c['lambda0_Mpc']:.3g} Mpc), failed lines {[k for k in ('L1','L2','L3','L4','L5') if not L[k]]}; "
      f"vs BBN {MU_BBN[f]:.3e} (x{MU_BBN[f]/c['mu']:.2e} below), vs galaxy 79.43 (x{c['mu']/MU_GAL:.3g}); q_K at l 156 kpc (X14 scaling {QK[f]} x mu/0.1) {QK[f]*c['mu']/0.1:.3g}")
P(f"LABEL: {lab}"); P(f"secondary reading: {RES['secondary_label_reading']}")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
dump()
