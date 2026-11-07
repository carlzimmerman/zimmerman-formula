#!/usr/bin/env python3
"""HC1 (criteria c207d70254): the fixed thermal fermion (m = 93.14 eV x 0.11958 = 11.1377 eV, g_f 2, R 5.562) with the a0
law acting on baryons + fermion (rule TOT), graded on GB1's static battery G1-G8, read-only.
    python3 hc1.py            -> hc1.json / hc1.out            (KA1-KA4, then HC1, bound readings, rule BAR)
    python3 hc1.py --mutate   -> hc1_MUTATE.json / .out        (M1 cap x 1e4, M2 Newton + fermion; each must FAIL G1)
Read-only: gb1.py (exec'd up to its main block), hf1_fermion.solve, hf1_g23.xcop_rows (KA2; caches redirected here).
EXPERIMENT: adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, types
os.environ.setdefault("OMP_NUM_THREADS", "1"); sys.dont_write_bytecode = True
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); RB = os.path.join(REPO, "rebuild_2026_10_22")
HF1D = os.path.join(RB, "HF1_hybrid_fermion"); CRG = os.path.join(RB, "CRG1_clean_room_regrade")
MUT = "--mutate" in sys.argv; TAG = "hc1_MUTATE" if MUT else "hc1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------------ GB1 battery, read-only (everything above its main block)
GB1P = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); gsrc = open(GB1P).read()
gcut = gsrc.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GB1P, "__name__": "gb1_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(gsrc[:gcut], "gb1_lib", "exec"), NS); sys.argv = _a
G, MS, KPC, PC = NS["G"], NS["MS"], NS["KPC"], NS["PC"]; A0 = NS["A0"]; glaw = NS["glaw"]; Missing = NS["Missing"]; need = NS["need"]
GB1J = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))

sys.path.insert(0, HF1D)
import hf1_fermion as FM

# ------------------------------------------------------------------ the fermion, fixed (criteria section 1)
OMF = 0.11958060485606123; OMB = 0.0215; M_EV = 93.14 * OMF; R_FAIR = OMF / OMB; GF_ = 2.0
MPC = 3.0857e22; RHO_M0 = (OMB + OMF) * 2.775e11 * MS / MPC ** 3              # kg/m^3, h cancels
def rta_of(Mtot): return (3 * (1 + R_FAIR) * Mtot / (4 * math.pi * 5.55 * RHO_M0)) ** (1 / 3)
CAPF = 1e4 if MUT else 1.0
KA4 = dict(n=0, nonconv={}, cap_violations=0, fair_bad=0)

def solve_sys(cls, rg, Mb, Mtot, Rsys, a0, Rf=None, capf=None):
    """rg grid (m, log-spaced, ending at r_ta), Mb on it (kg). Returns (Mf on rg, info)."""
    Rf = R_FAIR if Rf is None else Rf; capf = CAPF if capf is None else capf; rta = rg[-1]
    if Rf == 0.0: return np.zeros_like(rg), dict(sigma=0.0, cap=0.0, conv=True)
    s = FM.solve(rg, Mb, rta, Rsys, Rf * Mtot, M_EV, a0, gf=GF_, capf=capf, iters=300, G_=G)
    KA4["n"] += 1
    if not s["conv"]: KA4["nonconv"][cls] = KA4["nonconv"].get(cls, 0) + 1
    if not np.all(s["rho"] <= s["cap"] * (1 + 1e-9)): KA4["cap_violations"] += 1
    binds = np.any(s["rho"] >= s["cap"] * (1 - 1e-6))
    if not binds and abs(s["Mf"][-1] / (Rf * Mtot) - 1) > 0.01: KA4["fair_bad"] += 1
    return s["Mf"], dict(sigma=float(s["sigma"]), cap=float(s["cap"]), conv=bool(s["conv"]), binds=bool(binds))

def grid(rmin, Mtot, rmax_min, n=360):
    rta = rta_of(Mtot); return np.geomspace(rmin, max(rta, 1.001 * rmax_min), n)
def at(rg, Mf, r): return float(np.exp(np.interp(math.log(r), np.log(rg), np.log(np.maximum(Mf, 1e-300))))) if Mf[-1] > 0 else 0.0
def hern(rg, Mtot, rh):
    a = rh / (1 + math.sqrt(2)); return Mtot * (rg / (rg + a)) ** 2

def attach(B, f, a0, Rf=None, capf=None):
    """Solve every system once and attach M_f(<r) (kg) to each graded point's features. Returns per-class info."""
    info = {k: [] for k in ("SPARC", "X-COP", "groups0", "groups1", "ellipticals", "UDGs", "dSphs", "KiDS")}
    # SPARC: GB1's S list is in SP order, one block of points per galaxy
    k = 0
    for g in NS["SP"]:
        r = g["R"]; n = len(r); Mp = np.maximum.accumulate(np.maximum(g["vb2"] * r / G, 1e-30 * MS)); Mt = float(Mp[-1])
        rg = grid(0.05 * r[0], Mt, 2 * r[-1]); Mb = np.where(rg < r[0], Mp[0] * (rg / r[0]) ** 2, np.where(rg > r[-1], Mt, np.exp(np.interp(np.log(rg), np.log(r), np.log(Mp)))))
        Mf, s = solve_sys("SPARC", rg, Mb, Mt, r[-1], a0, Rf, capf)
        for i in range(n):
            ft = B["S"][k + i]["feat"]; assert abs(ft["r"] / r[i] - 1) < 1e-12; ft["Mf"] = at(rg, Mf, r[i]); ft["Mb_"] = float(Mp[i])
        s.update(name=g["name"], Mf_over_Mb_Rlast=at(rg, Mf, r[-1]) / Mt); info["SPARC"].append(s); k += n
    assert k == len(B["S"])
    # X-COP: QX5 point list, grouped by cluster name
    by = {}
    for j, z in enumerate(NS["XC"]): by.setdefault(z["name"], []).append(j)
    for nm, js in by.items():
        z0 = NS["XC"][js[0]]; ML, RL = z0["Mb_last"][0] * MS, z0["Mb_last"][1] * KPC
        rr = np.array([NS["XC"][j]["r_kpc"] * KPC for j in js]); mm = np.array([NS["XC"][j]["M_b"] * MS for j in js]); o = np.argsort(rr); rr, mm = rr[o], mm[o]
        rk = np.concatenate([rr, [RL]]) if RL > rr[-1] * 1.0001 else rr; mk = np.maximum.accumulate(np.concatenate([mm, [ML]]) if RL > rr[-1] * 1.0001 else mm)
        sl = math.log(mk[1] / mk[0]) / math.log(rk[1] / rk[0]); Mt = float(max(ML, mk[-1]))
        rg = grid(0.02 * rk[0], Mt, 2 * rk[-1]); Mb = np.where(rg < rk[0], mk[0] * (rg / rk[0]) ** sl, np.where(rg > rk[-1], Mt, np.exp(np.interp(np.log(rg), np.log(rk), np.log(mk)))))
        Mf, s = solve_sys("X-COP", rg, Mb, Mt, rk[-1], a0, Rf, capf)
        for j in js:
            ft = B["X"][j]["feat"]; ft["Mf"] = at(rg, Mf, ft["r"]); ft["Mb_"] = ft["Mb"] * MS
        s.update(name=nm, Mf_over_Mb=[B["X"][j]["feat"]["Mf"] / B["X"][j]["feat"]["Mb_"] for j in js]); info["X-COP"].append(s)
    # groups, f* = 0 and 1
    for fst in (0, 1):
        for gp in B["GR"][fst]:
            p0, p1 = gp["pts"]; r0, r1 = p0["feat"]["r"], p1["feat"]["r"]; m0, m1 = p0["feat"]["Mb"] * MS, max(p1["feat"]["Mb"], p0["feat"]["Mb"]) * MS
            sl = math.log(m1 / m0) / math.log(r1 / r0); Mt = m1; rg = grid(0.02 * r0, Mt, 2 * r1)
            Mb = np.where(rg > r1, Mt, m0 * (rg / r0) ** sl); Mf, s = solve_sys(f"groups{fst}", rg, Mb, Mt, r1, a0, Rf, capf)
            for p in gp["pts"]: p["feat"]["Mf"] = at(rg, Mf, p["feat"]["r"]); p["feat"]["Mb_"] = p["feat"]["Mb"] * MS
            s.update(name=gp["name"], Mf_over_Mb=[p["feat"]["Mf"] / p["feat"]["Mb_"] for p in gp["pts"]]); info[f"groups{fst}"].append(s)
    # ellipticals (B["E"]: 3 points per galaxy, EL order)
    for ie, e in enumerate(NS["EL"]):
        Mt = e["Mbar"](1e9) * MS; rg = grid(0.01 * e["Re"] * KPC, Mt, 20 * e["Re"] * KPC)
        Mb = np.maximum.accumulate(np.array([e["Mbar"](x / KPC) for x in rg]) * MS); Mf, s = solve_sys("ellipticals", rg, Mb, Mt, 8 * e["Re"] * KPC, a0, Rf, capf)
        for q in range(3):
            ft = B["E"][3 * ie + q]["feat"]; assert B["E"][3 * ie + q]["name"] == e["name"]; ft["Mf"] = at(rg, Mf, ft["r"]); ft["Mb_"] = ft["Mb"] * MS
        s.update(name=e["name"], Mf_over_Mb=[B["E"][3 * ie + q]["feat"]["Mf"] / B["E"][3 * ie + q]["feat"]["Mb_"] for q in range(3)]); info["ellipticals"].append(s)
    # UDGs and dSphs: Hernquist with half-mass radius r_h
    def small(cls, ft):
        Mt = ft["Mb"] * MS; rh = ft["r"]; rg = grid(1e-3 * rh, Mt, 4 * rh); Mf, s = solve_sys(cls, rg, hern(rg, Mt, rh), Mt, rh, a0, Rf, capf)
        ft["Mf"] = at(rg, Mf, rh); ft["Mb_"] = Mt / 2; s.update(Mf_over_Mbhalf=ft["Mf"] / (Mt / 2)); return s
    for u in B["U"]: info["UDGs"].append(small("UDGs", u["feat"]))
    for c_, pts in B["D"].items():
        for p in pts:
            if p["feat"]["Mb"] is None: p["feat"]["Mf"] = None; continue
            s = small("dSphs", p["feat"]); s.update(name=p["name"], cls=c_); info["dSphs"].append(s)
    # KiDS bins: Hernquist a = R_med/20, normalised to g_bar R_med^2 / G inside R_med
    for ft in list(B["K"][0]) + list(B["K"][1]):
        R = ft["r"]; a = R / 20; Min = ft["x"] * a0 * R ** 2 / G; Mt = Min / (R / (R + a)) ** 2
        rg = grid(1e-3 * R, Mt, 4 * R); Mb = Mt * (rg / (rg + a)) ** 2; Mf, s = solve_sys("KiDS", rg, Mb, Mt, R, a0, Rf, capf)
        ft["Mf"] = at(rg, Mf, R); ft["Mb_"] = Min; s.update(Mf_over_Mb=ft["Mf"] / Min, R_Mpc=R / MPC, Mb_Msun=Min / MS); info["KiDS"].append(s)
    return info

# ------------------------------------------------------------------ Solar System: uniform local fermion density at the MW cap
RHO_SS = FM.rho_cap(M_EV, 220e3 / math.sqrt(2), GF_) * CAPF
def ss_feat_hc1(a0, r):
    ft = NS["F_"](NS["GM_SUN"] / r ** 2 / a0, 1.0, r, math.sqrt(NS["GM_SUN"] / r) / 1e3, None, 0.0, [])
    ft["Mf"] = 4 * math.pi / 3 * RHO_SS * r ** 3; return ft
NS["ss_feat"] = ss_feat_hc1      # g_ss resolves ss_feat through this namespace

# ------------------------------------------------------------------ candidates (direct Delta, criteria section 2)
def gf_of(ft):
    Mf = ft.get("Mf")
    if Mf is None: raise Missing("Mf")
    return G * Mf / ft["r"] ** 2
def TOT(f, a0):
    def c(ft):
        x = need(ft, "x"); gN = x * a0; return dict(delta=math.log10(glaw(gN + gf_of(ft), a0) / glaw(gN, a0)))
    return c
def BAR(f, a0):
    def c(ft):
        x = need(ft, "x"); gN = x * a0; return dict(delta=math.log10((glaw(gN, a0) + gf_of(ft)) / glaw(gN, a0)))
    return c
def NEWT_F(f, a0):
    def c(ft):
        x = need(ft, "x"); gN = x * a0; return dict(delta=math.log10((gN + gf_of(ft)) / glaw(gN, a0)))
    return c

def build_B(f, a0):
    S, E, X = NS["build"](f, a0); GRp = {0: NS["groups_pts"](a0, 0.0), 1: NS["groups_pts"](a0, 1.0)}
    U = NS["udgs"](f, a0); D = NS["dsphs"](f, a0); K = NS["kids"](a0)
    st = NS["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=D, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S]))); return B

def grade(cand, B, a0):
    row = {}
    for gname, fn, fills in NS["GATES"]:
        row[gname] = NS["run_gate"](fn, cand, B, a0, [])
    return row
def flat(o, pre=""):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items(): out.update(flat(v, f"{pre}.{k}" if pre else str(k)))
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o): out.update(flat(v, f"{pre}[{i}]"))
    elif isinstance(o, (bool, np.bool_)): out[pre] = bool(o)
    elif isinstance(o, (int, float, np.floating, np.integer)): out[pre] = float(o)
    return out
short = None
def sh(g, r):
    n = r["num"]
    if n is None: return f"NO VERDICT (needs {r['missing']})"
    if g.startswith("G1"): return f"Z {n['Z']:+.4f} rms {n['rms']:.4f} (line {n['rms_line']:.4f})"
    if g.startswith("G2"): return f"mean {n['mean']:+.4f} rms {n['rms']:.4f}"
    if g.startswith("G3"): return f"pass f*0 {n['fst0']['n_pass']}/20 f*1 {n['fst1']['n_pass']}/20 (median res {n['fst0']['median_res']:+.3f}/{n['fst1']['median_res']:+.3f})"
    if g.startswith("G4"): return f"mean {n['mean']:+.4f}"
    if g.startswith("G5"): return f"mean {n['mean']:+.4f} ({n['z']:+.2f} sigma_U)"
    if g.startswith("G6"): return "; ".join(f"{k} {v['median_minus_anchor']:+.3f} [{v['ci'][0]:+.3f},{v['ci'][1]:+.3f}]" for k, v in n.items() if v["graded"])
    if g.startswith("G7"): return f"D_cand {n['D_cand']:+.4f} R {n['R']:+.4f} ({n['z']:+.2f} sigma)"
    if g.startswith("G8"): return f"worst planet use {n['worst_planet_use']:.4g}, Cassini use {n['cassini_use']:.4g}, F_Cassini - 1 {n['cassini_F'] - 1:.3e}"

RES = dict(tag=TAG, criteria="c207d70254", note="EXPERIMENT; adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; not theory closed",
           m_eV=M_EV, omega_f=OMF, omega_b=OMB, R=R_FAIR, capf=CAPF, footings={}, KA={})
P(f"HC1 {'MUTATE' if MUT else 'MAIN'}: m {M_EV:.4f} eV, g_f 2, R {R_FAIR:.4f}, cap factor {CAPF:g}. EXPERIMENT; adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; not theory closed.")

if not MUT:
    # KA3: Tremaine-Gunn closed form (HF1's K_TG)
    sig, r0 = 1e6, 250 * 3.0857e19; rho0 = 9 * sig ** 2 / (4 * math.pi * FM.G * r0 ** 2); mm = FM.tg_mmin(sig, r0); q = FM.rho_cap(mm, sig) / rho0
    RES["KA"]["KA3"] = dict(m_min=mm, ratio=q, ok=bool(abs(q - 1) < 1e-10)); P(f"KA3 TG closed form: cap/rho0 {q:.12f} -> {'PASS' if abs(q - 1) < 1e-10 else 'FAIL'}")
    # KA2: HF1's own X-COP pipeline at m 11.8, caches redirected into this lane
    CC = os.path.join(HERE, "cache_crg")
    p = os.path.join(CRG, "v1", "crg1_core.py"); s = open(p).read(); a = 'INP = os.path.join(HERE, "inputs")'; assert s.count(a) == 1
    s = s.replace(a, f'INP = {os.path.join(CC, "inputs")!r}').replace('PART = os.path.join(HERE, os.environ.get("CRG1_PARTIALS", "partials"))', f'PART = {os.path.join(CC, "p")!r}').replace('CACHE = os.path.join(HERE, os.environ.get("CRG1_CACHE", "cache"))', f'CACHE = {os.path.join(CC, "c")!r}')
    mcore = types.ModuleType("crg1_core"); mcore.__file__ = p; sys.modules["crg1_core"] = mcore; exec(compile(s, p, "exec"), mcore.__dict__); sys.path.insert(0, os.path.join(CRG, "v1"))
    import hf1_g23 as H23
    g1r = json.load(open(os.path.join(HF1D, "hf1_g1_results.json")))["rows"]["FD"]["FD_m11.8"]; rec = json.load(open(os.path.join(HF1D, "hf1_g23_RUN_m11p8.json")))["R"]["X"]
    XCc = H23.C.xcop_load(); k2 = {}
    for f in ("canonical", "alt"):
        x = H23.xcop_rows(XCc, g1r["omega_f"] / g1r["omega_b"], 11.8, f)["all"]; d = max(abs(x["mean"] - rec[f]["all"]["mean"]), abs(x["rms"] - rec[f]["all"]["rms"]))
        k2[f] = dict(mean=x["mean"], rms=x["rms"], rec_mean=rec[f]["all"]["mean"], rec_rms=rec[f]["all"]["rms"], diff=d, ok=bool(d <= 1e-6))
        P(f"KA2 HF1 X-COP m 11.8 {f}: mean {x['mean']:+.6f} rms {x['rms']:.6f} vs HF1 {rec[f]['all']['mean']:+.6f} {rec[f]['all']['rms']:.6f}: |d| {d:.1e} -> {'PASS' if d <= 1e-6 else 'FAIL'}")
    # same HF1 pipeline at HC1's m and R (reported cross-check; HF1's CRG1 X-COP chain, not GB1's points)
    RES["HF1_pipeline_at_HC1"] = {}
    for f in ("canonical", "alt"):
        x = H23.xcop_rows(XCc, R_FAIR, M_EV, f); RES["HF1_pipeline_at_HC1"][f] = dict(all=x["all"], by_x=x["by_x"], mf_over_mb_by_x=x["mf_over_mb_by_x"])
        P(f"  reported: HF1's own X-COP pipeline at HC1's m {M_EV:.3f}, R {R_FAIR:.3f}, {f}: mean {x['all']['mean']:+.4f} rms {x['all']['rms']:.4f}; by x {[round(v, 3) for v in x['by_x'].values()]}; M_f/M_b {[round(v, 2) for v in x['mf_over_mb_by_x'].values()]}")
    RES["KA"]["KA2"] = k2

CANDS = {"M1_cap1e4": TOT, "M2_newton_fermion": NEWT_F} if MUT else {"HC1": TOT, "BAR_reported": BAR}
for f, a0 in A0.items():
    B = build_B(f, a0); RF = {}
    if not MUT:
        # KA1: fermion off reproduces GB1's L0 graded numbers
        info0 = attach(B, f, a0, Rf=0.0); r0 = grade(TOT(f, a0), B, a0)
        NS["ss_feat"] = lambda a0_, r: dict(ss_feat_hc1(a0_, r), Mf=0.0); r0 = grade(TOT(f, a0), B, a0); NS["ss_feat"] = ss_feat_hc1
        dmax = 0.0; nk = 0
        for gname, _, _ in NS["GATES"]:
            ref = GB1J["cands"]["L0"][f][gname]; assert ref["status"] == r0[gname]["status"], (gname, ref["status"], r0[gname]["status"])
            a_, b_ = flat(ref["num"]), flat(r0[gname]["num"])
            for kk in a_:
                if kk in b_: dmax = max(dmax, abs(a_[kk] - b_[kk])); nk += 1
        RES["KA"][f"KA1_{f}"] = dict(maxdiff=dmax, n_compared=nk, ok=bool(dmax <= 1e-9)); P(f"[{f}] KA1 fermion off vs GB1 L0, G1-G8 ({nk} numbers): max|d| {dmax:.1e} -> {'PASS' if dmax <= 1e-9 else 'FAIL'}")
    info = attach(B, f, a0); RF["info"] = info
    for cn, mk in CANDS.items():
        row = grade(mk(f, a0), B, a0); RF[cn] = row
        for gname, _, _ in NS["GATES"]: P(f"[{f}] {cn:18s} {gname:17s} {row[gname]['status']:10s} {sh(gname, row[gname])}")
    # where the fermion sits
    def med(v): v = [x for x in v if x is not None and np.isfinite(x)]; return float(np.median(v)) if v else None
    sit = dict(SPARC_Mf_over_Mb_Rlast=med([s["Mf_over_Mb_Rlast"] for s in info["SPARC"]]),
               SPARC_Mf_over_Mb_Rlast_max=float(max(s["Mf_over_Mb_Rlast"] for s in info["SPARC"])),
               SPARC_points_Mf_over_Mb=med([p["feat"]["Mf"] / p["feat"]["Mb_"] for p in B["S"]]),
               XCOP_Mf_over_Mb=med([v for s in info["X-COP"] for v in s["Mf_over_Mb"]]),
               groups_f0_Mf_over_Mb=med([v for s in info["groups0"] for v in s["Mf_over_Mb"]]), groups_f1_Mf_over_Mb=med([v for s in info["groups1"] for v in s["Mf_over_Mb"]]),
               ell_Mf_over_Mb=med([v for s in info["ellipticals"] for v in s["Mf_over_Mb"]]), UDG_Mf_over_Mbhalf=med([s["Mf_over_Mbhalf"] for s in info["UDGs"]]),
               dSph_Mf_over_Mbhalf=med([s["Mf_over_Mbhalf"] for s in info["dSphs"]]), KiDS_Mf_over_Mb=[round(s["Mf_over_Mb"], 4) for s in info["KiDS"]],
               sigma_kms={k: med([s["sigma"] / 1e3 for s in v]) for k, v in info.items() if v}, cap_binds_share={k: float(np.mean([s.get("binds", False) for s in v])) for k, v in info.items() if v})
    RF["where"] = sit; P(f"[{f}] where the fermion sits (median M_f/M_b at graded radii): {json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in sit.items()})}")
    if not MUT:
        # bound readings for the scarce side: UDGs and dSphs
        U = []
        for u, s in zip(B["U"], info["UDGs"]):
            ft = u["feat"]; rh = ft["r"]; sg = max(ft["sigma"] * 1e3, s["sigma"]); row_ = next(r for r in NS["UROWS"] if r["footing"] == f and abs(float(r["Mstar"]) - ft["Mb"]) < 1e-6 * ft["Mb"])
            ge = glaw(float(row_["x_e_dmean"]) * a0, a0); rho_amb = 3 * ge / (4 * math.pi * G * float(row_["d_mean_kpc"]) * KPC)
            Mmax = 4 * math.pi / 3 * rh ** 3 * (34 * FM.rho_cap(M_EV, sg, GF_) + rho_amb); gN = ft["x"] * a0
            U.append(dict(name=row_["name"], D=u["D"], Mmax_over_Mbhalf=Mmax / (ft["Mb"] * MS / 2), rho_amb_share=rho_amb / (34 * FM.rho_cap(M_EV, sg, GF_) + rho_amb), delta_max=math.log10(glaw(gN + G * Mmax / rh ** 2, a0) / glaw(gN, a0))))
        um = float(np.mean([q["D"] - q["delta_max"] for q in U])); RF["bound_UDG"] = dict(rows=U, mean_residual_at_max=um, z=um / B["sigU"], pass_at_max=bool(abs(um) <= 2 * B["sigU"]))
        P(f"[{f}] BOUND UDGs (MAX fermion, own 34 x cap + Coma's mean interior density): Delta_max {[round(q['delta_max'], 3) for q in U]}; mean residual {um:+.3f} ({um / B['sigU']:+.2f} sigma_U) -> {'PASS' if abs(um) <= 2 * B['sigU'] else 'FAIL'} at the maximum")
        HOST = {"MW classical": 220e3, "MW ultra-faint": 220e3, "bright M31": 250e3, "M31 others": 250e3, "LG field": None}
        dmx = {}
        for c_, pts in B["D"].items():
            vals = []
            for p in pts:
                ft = p["feat"]
                if ft["x"] is None or ft["Mb"] is None: continue
                rh = ft["r"]; amb = 34 * FM.rho_cap(M_EV, HOST[c_] / math.sqrt(2), GF_) if HOST[c_] else 0.0
                Mmax = 4 * math.pi / 3 * rh ** 3 * (34 * FM.rho_cap(M_EV, ft["sigma"] * 1e3, GF_) + amb); gN = ft["x"] * a0
                vals.append(math.log10(glaw(gN + G * Mmax / rh ** 2, a0) / glaw(gN, a0)))
            dmx[c_] = dict(max_delta_max=float(max(vals)) if vals else None, median_delta_max=float(np.median(vals)) if vals else None)
        RF["bound_dSph"] = dmx; P(f"[{f}] BOUND dSphs (MAX fermion): largest Delta_max per class {json.dumps({k: (None if v['max_delta_max'] is None else round(v['max_delta_max'], 5)) for k, v in dmx.items()})}")
        RF["solar_system"] = dict(rho_local_cap_Msun_pc3=RHO_SS / (MS / PC ** 3), g_f_Saturn=4 * math.pi / 3 * G * RHO_SS * NS["PLAN"]["Saturn"], g_f_Cassini=4 * math.pi / 3 * G * RHO_SS * NS["R_CASSINI"])
        P(f"[{f}] Solar System: local cap rho {RF['solar_system']['rho_local_cap_Msun_pc3']:.3e} Msun/pc^3; g_f at Saturn {RF['solar_system']['g_f_Saturn']:.3e} m/s^2, at 9.58 AU {RF['solar_system']['g_f_Cassini']:.3e} m/s^2")
    RES["footings"][f] = RF
RES["KA4"] = dict(KA4, ok=bool(KA4["cap_violations"] == 0 and KA4["fair_bad"] == 0))
P(f"KA4 solves {KA4['n']}: non-converged by class {KA4['nonconv']}; cap violations {KA4['cap_violations']}; fair-share misses (cap not binding) {KA4['fair_bad']} -> {'PASS' if RES['KA4']['ok'] else 'FAIL'}")

def label(cn):
    sts = {(f, g): RES["footings"][f][cn][g]["status"] for f in A0 for g, _, _ in NS["GATES"]}
    fails = sorted({g.split()[0] for (f, g), s in sts.items() if s == "FAIL"}); nvs = sorted({g.split()[0] for (f, g), s in sts.items() if s == "NO VERDICT"})
    return ("PASSES ALL STATIC GATES" if all(s == "PASS" for s in sts.values()) else (f"FAIL ({', '.join(fails)})" + (f"; NO VERDICT ({', '.join(nvs)})" if nvs else "")) if fails else f"NOT GRADABLE ({', '.join(nvs)})")
if MUT:
    bites = {cn: all(RES["footings"][f][cn]["G1 SPARC"]["status"] == "FAIL" for f in A0) for cn in CANDS}
    RES["MUTATE_bites"] = bites; RES["labels"] = {cn: label(cn) for cn in CANDS}
    for cn in CANDS: P(f"MUTATE {cn}: {RES['labels'][cn]}; G1 fails both footings -> {'BITES' if bites[cn] else 'NO POWER on G1'}")
else:
    kaok = RES["KA"]["KA3"]["ok"] and all(v["ok"] for v in RES["KA"]["KA2"].values()) and all(RES["KA"][f"KA1_{f}"]["ok"] for f in A0) and RES["KA4"]["ok"]
    RES["KA_all"] = bool(kaok); RES["labels"] = {cn: label(cn) for cn in CANDS}
    P(f"KA all: {'PASS' if kaok else 'FAIL (grades below are NOT valid)'}")
    for cn in CANDS: P(f"LABEL {cn} (static G1-G8): {RES['labels'][cn]}")
P("EXPERIMENT; adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; footings never pooled; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (MUT and all(RES["MUTATE_bites"].values())) or (not MUT and RES["KA_all"]) else 1)
