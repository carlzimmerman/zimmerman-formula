#!/usr/bin/env python3
"""SE1 (FROZEN_CRITERIA.md bf53473414): the shock-entropy sector at action level, L_x = F(Q, s) + zeta n.ds.
Arm (a) F = (mu_K^2/2K) g(s)(Q-1)^2; arm (b) gamma 5/3 ideal fluid. Readings H / O, closures strict / generous.
Graded on GB1 G1-G8 (read-only) + G9a/G9b (QX3 iter2 machinery as KD1 runs it).
    python3 se1.py            -> se1.json / se1.out      (checkpoints in parts/)
    python3 se1.py --mutate   -> se1_MUTATE.json / .out  (i host temperature, ii Sigma flipped, iii g const)
kappa = 1/2 FITTED; footings never pooled; not theory closed.  1 thread, < 1 GB."""
import os, sys, json, math, runpy, io, contextlib, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, "..")); REPO = os.path.dirname(CL)
MUT = "--mutate" in sys.argv; TAG = "se1_MUTATE" if MUT else "se1"; OUT = []; T0 = time.time()
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
def P(s=""): print(s, flush=True); OUT.append(str(s))
def load_prefix(path, marker, name, file_as=None):
    src = open(path).read(); ns = {"__file__": file_as or path, "__name__": name}
    a = sys.argv; sys.argv = [path]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
RES = dict(tag=TAG, criteria="bf53473414", note="kappa = 1/2 FITTED; not theory closed", KA={}, inputs={}, arms={})
P(f"SE1 {'MUTATE' if MUT else 'MAIN'}: shock-entropy sector at action level. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ record machinery (read-only)
EN = load_prefix(os.path.join(CL, "EN1_shock_entropy_field", "en1.py"), "TABLE = {}", "en1_lib", file_as=os.path.join(HERE, "en1_as_lib.py"))
GB, BATT = EN["GB"], EN["BATT"]
A0, G, MS, PC, KPC = GB["A0"], GB["G"], GB["MS"], GB["PC"], GB["KPC"]
GBJ = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
KDJ = json.load(open(os.path.join(CL, "KD1_unpinned_kq_dust", "kd1.json")))
ENJ = json.load(open(os.path.join(CL, "EN1_shock_entropy_field", "en1.json")))
Q13J0 = json.load(open(os.path.join(CL, "QX13_virial_floor", "qx13.json")))            # original (pre-QX16 elliptical fix)
Q13FX = os.path.join(CL, "QX16_elliptical_binding_fix", "fixed_outputs", "QX13_virial_floor")   # the current record (QX16 rerun)
Q13J = json.load(open(os.path.join(Q13FX, "qx13_FIXED.json"))); Q13M = json.load(open(os.path.join(Q13FX, "qx13_MUTATE_FIXED.json")))
Q3 = load_prefix(os.path.join(CL, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
kds = open(os.path.join(CL, "KD1_unpinned_kq_dust", "kd1.py")).read()
KDNS = dict(GB=GB, math=math, np=np, FCAP=Q3["FCAP"], GMSUN=Q3["GMSUN"], PC=PC)
exec(compile(kds[kds.index("def enc(xi):"):kds.index("def flat(x, p=\"\"):")], "kd1_KD", "exec"), KDNS)   # KD1's enc, mj_of, KD verbatim
_gs = open(os.path.join(CL, "GB1_all_gates_battery", "gb1.py")).read()
exec(compile(_gs[_gs.index("def short(g, r):"):_gs.index("for cn, mk in CANDS.items():")], "gb1_short", "exec"), GB)
_ssp = GB["ss_feat"]; GB["ss_feat"] = lambda a0, r: dict(_ssp(a0, r), nodust=True)          # KD1 P4 (as kd1.py)
GK = 4.30091e-6; ACC = 1e6 / KPC; C_KMS = 299792.458
def glaw(gN, a0k): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0k * np.maximum(gN, 0.0))
GATES = GB["GATES"]
def flat(x, p=""):
    if isinstance(x, dict):
        o = {}
        for k, v in x.items(): o.update(flat(v, p + "/" + k))
        return o
    if isinstance(x, (list, tuple)):
        o = {}
        for i, v in enumerate(x): o.update(flat(v, p + f"[{i}]"))
        return o
    return {p: x}
def grade(cand, f): return {g: GB["run_gate"](fn, cand, BATT[f], A0[f], fills) for g, fn, fills in GATES}
def rowdiff(row, ref):
    dmax, ok = 0.0, True
    for g in row:
        a, b = flat(row[g]["num"]), flat(ref[g]["num"]); ok &= (a.keys() == b.keys()) and row[g]["status"] == ref[g]["status"]
        for k in a:
            if isinstance(a[k], (int, float)) and not isinstance(a[k], bool) and k in b and isinstance(b[k], (int, float)): dmax = max(dmax, abs(a[k] - b[k]))
    return dmax, ok
def statuses(row): return {g: r["status"] for g, r in row.items()}

# ------------------------------------------------------------------ settings per footing (KD1's QX15 setting)
SET = {}
for f in A0:
    s = KDJ["footings"][f]["setting"]; ob, od, h = s["omega_b"], s["omega_d"], s["h"]
    rho_c1 = 3 * 100.0 ** 2 / (8 * math.pi * 4.30091e-9) / 1e9                       # Msun/kpc^3 per h^2
    SET[f] = dict(ob=ob, od=od, h=h, ns=s["n_s"], tau=s["tau"], R=od / ob, fcap=Q3["FCAP"], rho_sea=od * rho_c1, rho_m0=(ob + od) * rho_c1,
                  a0k=A0[f] / ACC, mu_star=KDJ["footings"][f]["mu_star"])
def r_ta(M, st): return (M * (1 + st["R"]) / (4 * math.pi / 3 * 5.55 * st["rho_m0"])) ** (1 / 3)   # QX10's rule, kpc
RES["inputs"] = {f: dict(R=SET[f]["R"], fcap=SET[f]["fcap"], capture_share=SET[f]["fcap"] * SET[f]["R"], rho_sea_Msun_kpc3=SET[f]["rho_sea"],
                         alpha_bracket=[0.0, 2 / 3, 5 / 3], r_sh="r_ta/2 (variant r_ta/3 reported)", source="kd1.json setting (QX15 main theta), X22 f_cap") for f in A0}
P("built inputs (frozen rules): " + "; ".join(f"[{f}] R {SET[f]['R']:.4f}, f_cap R {SET[f]['fcap']*SET[f]['R']:.4f}, rho_sea {SET[f]['rho_sea']:.4g} Msun/kpc^3" for f in A0))

# ------------------------------------------------------------------ KA1: b = 1 is GB1 L0; KA4: EN1 reproduced
for f in A0:
    d, ok = rowdiff(grade(lambda ft: dict(b=1.0, F=1.0, T=0.0), f), GBJ["cands"]["L0"][f])
    RES["KA"][f"KA1_{f}"] = dict(maxdiff=d, ok=bool(ok and d <= 1e-12) and EN["RES"]["KA"][f"KA1_means_{f}"]["ok"])
    P(f"[{f}] KA1 b = 1 vs gb1.json L0: max|d| {d:.1e}, statuses equal {ok}; QX20 means {EN['RES']['KA'][f'KA1_means_{f}']['maxdiff']:.1e} -> {'PASS' if RES['KA'][f'KA1_{f}']['ok'] else 'FAIL'}")
    a = EN["RES"]["within_host_need_vs_proxy"][f]; b = ENJ["within_host_need_vs_proxy"][f]
    dd = max(max(abs(x["f_need_med"] - y["f_need_med"]), abs(x["proxy_med"] - y["proxy_med"])) for x, y in zip(a, b))
    c, _ = EN["fix_const"](f, "V-frac-L"); dc = abs(c / ENJ["V-frac-L"][f]["const"] - 1)
    RES["KA"][f"KA4_EN1_{f}"] = dict(table_maxdiff=float(dd), const_rel=float(dc), ok=bool(dd <= 1e-9 and dc <= 1e-9))
    P(f"[{f}] KA4 EN1 within-host table max|d| {dd:.1e}, V-frac-L constant rel {dc:.1e} -> {'PASS' if RES['KA'][f'KA4_EN1_{f}']['ok'] else 'FAIL'}")

# ------------------------------------------------------------------ hosts (one rule for every class)
def table_fn(rr, mm):
    rr = np.asarray(rr, float); mm = np.maximum.accumulate(np.maximum(np.asarray(mm, float), 1e-30))
    o = np.argsort(rr); rr, mm = rr[o], mm[o]; u, iu = np.unique(rr, return_index=True); rr, mm = u, mm[iu]
    lr, lm = np.log(rr), np.log(mm)
    def f(r):
        r = np.asarray(r, float); x = np.log(np.maximum(r, 1e-300))
        out = np.exp(np.interp(x, lr, lm)); out = np.where(r < rr[0], mm[0] * (r / rr[0]) ** 3, out); out = np.where(r > rr[-1], mm[-1], out)
        return out
    return f
def tab_analytic(fun, rlo, rhi): rr = np.geomspace(rlo, rhi, 600); return table_fn(rr, fun(rr))
L13 = None
def qx13_lib():
    global L13
    if L13 is None:
        a = sys.argv; sys.argv = [os.path.join(CL, "QX13_virial_floor", "qx13.py")]
        with contextlib.redirect_stdout(io.StringIO()): L13 = runpy.run_path(sys.argv[0], run_name="qx13_lib")
        sys.argv = a
    return L13
_x, _y = [], []
for ln in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):        # QX12 iter_3 A1's r_d fit, same rule
    t = ln.split()
    if len(t) < 18: continue
    try: Lk = float(t[7]); Rd = float(t[11]); MHI = float(t[13]); q = int(t[17]); inc = float(t[5])
    except ValueError: continue
    if q <= 2 and inc >= 30 and Rd > 0: _x.append(math.log10((0.5 * Lk + 1.33 * MHI) * 1e9)); _y.append(math.log10(Rd))
RD_B, RD_A = np.polyfit(_x, _y, 1)
def rd_of(Mb): return 10 ** (RD_A + RD_B * math.log10(Mb))
def expdisc_v(Mb, rd): return lambda r: Mb * (1 - (1 + r / rd) * np.exp(-r / rd))
UROWS = GB["UROWS"]
def build_hosts(f):
    """list of hosts: dict(cls, name, Mb (vector fn of r kpc), Msys, pts=[ft dicts], shocked_H (reading H))"""
    B = BATT[f]; H = []; nid = [0]
    def tag(ft):
        ft["SE1id"] = nid[0]; nid[0] += 1; return ft["SE1id"]
    k = 0
    for g in GB["SP"]:
        n = len(g["R"]); pts = B["S"][k:k + n]; k += n
        r = g["R"] / KPC; M = g["vb2"] * g["R"] / G / MS; Ms = g["vb2"][-1] * g["R"][-1] / G / MS
        for p in pts: tag(p["feat"])
        H.append(dict(cls="SPARC", name=g["name"], Mb=table_fn(r[M > 0], M[M > 0]), Msys=Ms, pts=[p["feat"] for p in pts], shockH=False))
    assert k == len(B["S"])
    for i, e in enumerate(GB["EL"]):
        pts = B["E"][3 * i:3 * i + 3]; Ms = e["Mbar"](1e9)
        for p in pts: tag(p["feat"]); assert p["name"] == e["name"]
        H.append(dict(cls="ellipticals", name=e["name"], Mb=tab_analytic(lambda r: np.array([e["Mbar"](x) for x in r]), 1e-3 * e["Re"], 1e4), Msys=Ms,
                      pts=[p["feat"] for p in pts], shockH=True, kT=EN["FUK"].get(e["name"], {}).get("kTo")))
    names = []
    for z in GB["XC"]:
        if z["name"] not in names: names.append(z["name"])
    for nm in names:
        idx = [i for i, z in enumerate(GB["XC"]) if z["name"] == nm]; zz = [GB["XC"][i] for i in idx]
        Ml, rl = zz[0]["Mb_last"]; pts = [B["X"][i]["feat"] for i in idx]
        for p in pts: tag(p)
        q = EN["xprof"](nm)
        H.append(dict(cls="X-COP", name=nm, Mb=table_fn([z["r_kpc"] for z in zz] + [rl], [z["M_b"] for z in zz] + [Ml]), Msys=Ml, pts=pts, shockH=True,
                      kT=float(np.mean(q["kT"]))))
    for fst in (0, 1):
        for gp, graw in zip(B["GR"][fst], GB["GR"]):
            pts = [p["feat"] for p in gp["pts"]]
            for p in pts: tag(p)
            Ms = graw["g5"] * (1 + fst)
            H.append(dict(cls=f"groups_fst{fst}", name=graw["name"], Mb=table_fn([q["r_kpc"] for q in graw["pts"]] + [graw["R5"]], [q["M_gas"] * (1 + fst) for q in graw["pts"]] + [Ms]),
                          Msys=Ms, pts=pts, shockH=True, kT=graw["kT"]))
    for u, row in zip(B["U"], [r for r in UROWS if r["footing"] == f]):
        ft = u["feat"]; tag(ft); Ms = ft["Mb"]; rh = ft["r"] / KPC
        H.append(dict(cls="UDG", name=row["name"], Mb=tab_analytic(lambda r, Ms=Ms, rh=rh: Ms * r ** 3 / (r ** 3 + rh ** 3), 1e-3 * rh, 1e5), Msys=Ms, pts=[ft], shockH=True,
                      d_mean=float(row["d_mean_kpc"]), kT=8.6))
    for cls_, lst in B["D"].items():
        for p in lst:
            ft = p["feat"]; tag(ft)
            if ft["Mb"] is None or ft["r"] is None: continue
            Ms = ft["Mb"]; rh = ft["r"] / KPC
            H.append(dict(cls="dSph", sub=cls_, name=p["name"], Mb=tab_analytic(lambda r, Ms=Ms, rh=rh: Ms * r ** 3 / (r ** 3 + rh ** 3), 1e-3 * rh, 1e5), Msys=Ms, pts=[ft], shockH=False))
    for j, lst in enumerate(B["K"]):
        for ft in lst:
            tag(ft); R_ = ft["r"] / KPC; Ms = ft["x"] * A0[f] * ft["r"] ** 2 / G / MS
            H.append(dict(cls="KiDS", sub=("early", "late")[j], name=f"KiDS{j}", Mb=tab_analytic(expdisc_v(Ms, rd_of(Ms)), 1e-3, 1e5), Msys=Ms, pts=[ft], shockH=(j == 0), Mpt=Ms))
    return H

# ------------------------------------------------------------------ solvers
def solve_gen(Mbf, Mcap, rsh, rta, a0k, alpha, rho_sea, nstep=300, rounds=7, width=16, v2_override=None):
    """mass-conserving stratified gamma 5/3 sector: K(m) = K_sh (m/Mcap)^alpha, shock jump at r_sh, shoot rho_sh."""
    Msea = lambda r: 4 / 3 * math.pi * rho_sea * r ** 3
    ro = np.geomspace(rsh, rta, 400); gout = glaw(GK * (Mbf(ro) + Mcap - Msea(rsh)) / ro ** 2, a0k); Hsh = float(np.trapz(gout, ro)); v2 = 2 * Hsh if v2_override is None else v2_override
    u = np.linspace(math.log(Mcap), math.log(Mcap * 1e-7), nstep + 1); du = u[1] - u[0]
    def run(lrho, keep=False):
        rho_sh = np.exp(lrho); r = np.full_like(rho_sh, rsh); Pp = (3 / 16) * v2 * rho_sh; Ksh = Pp / rho_sh ** (5 / 3)
        alive = np.ones_like(rho_sh, bool); traj = [r.copy()] if keep else None
        def d(uu, r, Pp):
            m = math.exp(uu); K = Ksh * (m / Mcap) ** alpha; rho = (np.maximum(Pp, 1e-300) / K) ** 0.6
            rs = np.maximum(r, 1e-12); g = glaw(GK * (Mbf(rs) + m - Msea(rs)) / rs ** 2, a0k)
            return m / (4 * math.pi * rs ** 2 * rho), -m * g / (4 * math.pi * rs ** 2)
        for i in range(nstep):
            k1 = d(u[i], r, Pp); k2 = d(u[i] + du / 2, r + du / 2 * k1[0], Pp + du / 2 * k1[1])
            k3 = d(u[i] + du / 2, r + du / 2 * k2[0], Pp + du / 2 * k2[1]); k4 = d(u[i] + du, r + du * k3[0], Pp + du * k3[1])
            rn = r + du / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); Pn = Pp + du / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            bad = ~(np.isfinite(rn) & (rn > 0) & np.isfinite(Pn) & (Pn > 0)); alive &= ~bad
            r = np.where(alive, rn, r); Pp = np.where(alive, Pn, Pp)
            if keep: traj.append(r.copy())
        return alive, r, (np.array(traj) if keep else None), Ksh
    rbar = Mcap / (4 / 3 * math.pi * rsh ** 3); lo, hi = math.log(rbar * 1e-8), math.log(rbar * 1e12)
    for _ in range(rounds):                       # inward: too low rho_sh -> r hits 0 before m -> 0 (dead); too high -> hole (alive)
        grid = np.linspace(lo, hi, width); al, _, _, _ = run(grid)
        if al.all(): lo, hi = lo - 15, grid[0]; continue
        if not al.any(): lo, hi = grid[-1], hi + 15; continue
        i = int(np.argmax(al)); lo, hi = grid[i - 1], grid[i]
    lo = hi
    al, rend, traj, Ksh = run(np.array([lo]), keep=True)
    rr = traj[:, 0]; mm = np.exp(u)
    return dict(r=rr[::-1], m=mm[::-1], rend_over_rsh=float(rend[0] / rsh), Ksh=float(Ksh[0]), v2=v2, rho_sh=math.exp(lo), Hsh=Hsh)
def Mx_gen(sol, r, rsh, Mcap, rho_sea):
    r = np.asarray(r, float); rr, mm = sol["r"], sol["m"]
    inside = np.interp(np.log(np.maximum(r, 1e-300)), np.log(np.maximum(rr, 1e-300)), mm)
    inside = np.where(r < rr[0], mm[0] * (r / max(rr[0], 1e-300)) ** 3, inside)
    return np.where(r > rsh, Mcap + 4 / 3 * math.pi * rho_sea * (r ** 3 - rsh ** 3), inside)
def solve_strict(Mb_arr, r, Mcap, rta, a0k, rho_sea, Kfix=None, mode="open", tol=1e-7, itmax=4000):
    """isentropic per host (Theorem K). mode 'open': rho = (rho_sea^(2/3) + 2H/(5K))^(3/2), H = int_r^{r_ta} g, K = K_sh (or Kfix);
    mode 'qx13shock': QX13 iter_1's shock-case profile (rho(r_sh) = 4 rho_sea), floor off; capped at Mcap; Picard as QX13."""
    lr = np.log(r); dr = np.diff(r); shell = 4 * math.pi * r ** 2; Msea = 4 / 3 * math.pi * rho_sea * r ** 3
    Md = Msea.copy(); rsh = 0.5 * rta; Ksh = 0.0; capped = False; err = 1.0
    for it in range(itmax):
        g = glaw(GK * (Mb_arr + Md - Msea) / r ** 2, a0k)
        Hc = np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]])
        Hsh = float(np.interp(math.log(rsh), lr, Hc)); Ksh = (0.75 * rho_sea * 2 * Hsh) / (4 * rho_sea) ** (5 / 3)
        K = Kfix if Kfix is not None else Ksh
        if mode == "qx13shock":
            rho = ((4 * rho_sea) ** (2 / 3) + 2 * np.maximum(Hc - Hsh, 0.0) / (5 * K)) ** 1.5; rho = np.where(r <= rsh, rho, rho_sea)
        else:
            rho = (rho_sea ** (2 / 3) + 2 * Hc / (5 * K)) ** 1.5
        seg = 0.5 * (shell[1:] * rho[1:] + shell[:-1] * rho[:-1]) * dr
        mc = np.cumsum(np.concatenate([[4 / 3 * math.pi * r[0] ** 3 * rho[0]], seg]))
        if Mcap is not None and mc[-1] > Mcap: new = mc / mc[-1] * Mcap; capped = True
        else: new = mc; capped = False
        err = float(np.max(np.abs(new - Md)) / max(np.max(new), 1e-300)); Md = 0.5 * Md + 0.5 * new
        if err < tol and it > 5: break
    return dict(r=r, Md=new - Msea, capped=capped, its=it, err=err, conv=bool(err < tol), Ksh=Ksh, ka2=abs(2.5 * Ksh * (4 * rho_sea) ** (2 / 3) / (15 / 16 * Hsh) - 1) if Hsh > 0 else 0.0)

# ------------------------------------------------------------------ KA5 (KNOWN): Lane-Emden n = 1 and n = 3/2 (law off, no host, no sea)
def lane_emden_check():
    # (i) reference: outward Newtonian integration of the n = 3/2 polytrope P = K rho^(5/3) against the Lane-Emden constants
    K, rc = 1.0, 1.0; a = math.sqrt((2.5 * K * rc ** (-1 / 3)) / (4 * math.pi * GK)); dr = 10 * a / 200000
    hh = 2.5 * K * rc ** (2 / 3); m = 0.0; x = 1e-9; R = None; prof = []
    while True:
        rho = (max(hh, 0) / (2.5 * K)) ** 1.5
        if hh <= 0: R = x; break
        prof.append((x, m, rho)); m += 4 * math.pi * x ** 2 * rho * dr; hh -= GK * m / x ** 2 * dr; x += dr
    e15 = abs(R / (3.65375 * a) - 1); em = abs(m / (2.71406 * 4 * math.pi * a ** 3 * rc) - 1)
    # (ii) SE1's Lagrangian shooting solver (solve_gen, alpha 0, law off, no host, no sea) on the same star truncated at 0.6 R:
    # given M(<x_s), x_s and the boundary P/rho, it must find rho(x_s) and the interior mass profile
    pr = np.array(prof); i = int(np.searchsorted(pr[:, 0], 0.6 * R)); xs, Ms_, rs_ = pr[i]
    sol = solve_gen(lambda r: np.zeros_like(np.asarray(r, float)), Ms_, xs, 2 * xs, 0.0, 0.0, 0.0, nstep=600, rounds=9, v2_override=(16 / 3) * K * rs_ ** (2 / 3))
    erho = abs(sol["rho_sh"] / rs_ - 1); j = int(np.searchsorted(pr[:, 0], 0.5 * xs))
    em2 = abs(float(np.interp(math.log(pr[j, 0]), np.log(np.maximum(sol["r"], 1e-300)), sol["m"])) / pr[j, 1] - 1)
    # (iii) n = 1: P = Kp rho^2 has radius pi a, a = sqrt(Kp / (2 pi G)) = 1/k_J (KD1's core rule R_c = pi / mu_K)
    Kp = 1.0; a1 = math.sqrt(Kp / (2 * math.pi * GK)); hh = 2 * Kp * rc; m = 0.0; x = 1e-9; dr = 5 * a1 / 200000
    while hh > 0:
        m += 4 * math.pi * x ** 2 * (hh / (2 * Kp)) * dr; hh -= GK * m / x ** 2 * dr; x += dr
    e1 = abs(x / (math.pi * a1) - 1)
    return dict(n15_R_rel=e15, n15_M_rel=em, solver_rho_s_rel=erho, solver_M_half_rel=em2, n1_R_rel=e1,
                ok=bool(max(e15, em, erho, em2, e1) <= 1e-3))
ka5 = lane_emden_check(); RES["KA"]["KA5_known"] = ka5
P(f"KA5 KNOWN Lane-Emden: n=3/2 R rel {ka5['n15_R_rel']:.1e}, M rel {ka5['n15_M_rel']:.1e}; SE1 shooting solver on the truncated n=3/2 star: rho_s rel {ka5['solver_rho_s_rel']:.1e}, M(<x_s/2) rel {ka5['solver_M_half_rel']:.1e}; n=1 R = pi/k_J rel {ka5['n1_R_rel']:.1e} -> {'PASS' if ka5['ok'] else 'FAIL'}")
# the shooting solver on a KNOWN self-similar case: no host, law off, isentropic sector of mass M bounded by a shock: compare the
# solved boundary pressure with an independent outward Lane-Emden-type integration (reported in the convergence check below)

# ------------------------------------------------------------------ KA3: QX13 to 0 (record code) and SE1's strict solver in QX13's mode
L = qx13_lib(); GR3 = L["grade"]; KA3 = {}
for f in A0:
    cm = Q13J["foot"][f]["c_min"]; L["MODE"].update(dict(heat=True, floor=True, kfac=1.0)); o = GR3(cm["c"], L["A0K"][f], L["BASE"][f])
    keys = ("X_mean", "X_rms", "G_fst0", "G_fst1", "G5_max", "G6_shift", "G7_shift"); d = max(abs(o[k] - cm[k]) for k in keys)
    m1 = Q13M["M"][f]["M1"]
    def my_iso(Mb_fn, M_cap, c2, rta, a0k, law=True, host=True, rho_sea=L["RHO_D0"], n=900, rmin=1e-3):
        rr = np.geomspace(rmin, rta, n); Mb = np.array([Mb_fn(x) for x in rr]) if host else np.zeros(n)
        return solve_strict(Mb, rr, M_cap, rta, a0k, rho_sea, mode="qx13shock")
    old = GR3.__globals__["solve_iso"]; GR3.__globals__["solve_iso"] = my_iso
    try: o2 = GR3(0.0, L["A0K"][f], L["BASE"][f])
    finally: GR3.__globals__["solve_iso"] = old
    d2 = max(abs(o2[k] - m1[k]) for k in keys); c0r = Q13J0["foot"][f]["c_min"]; dorig = {k: float(o[k] - c0r[k]) for k in keys}
    KA3[f] = dict(qx13_record_maxdiff=float(d), se1_strict_vs_qx13_M1_maxdiff=float(d2), ok=bool(d <= 1e-12 and d2 <= 1e-9),
                  per_key_vs_original_prefix16=dorig, reference="QX16 fixed_outputs qx13_FIXED.json / qx13_MUTATE_FIXED.json")
    P(f"[{f}] KA3 QX13 c_min row by its own solver vs qx13_FIXED.json (QX16 rerun): max|d| {d:.1e}; SE1 strict solver (QX13 shock mode, floor off) vs QX13 M1 FIXED: max|d| {d2:.1e} -> {'PASS' if KA3[f]['ok'] else 'FAIL'}")
    P(f"[{f}] KA3 reported: vs the original qx13.json (pre-QX16): " + ", ".join(f"{k} {v:+.1e}" for k, v in dorig.items()))
RES["KA"]["KA3_QX13"] = KA3

# ------------------------------------------------------------------ per-footing solves (checkpointed)
def Msea_f(r, st): return 4 / 3 * math.pi * st["rho_sea"] * r ** 3
def host_solutions(f, closure, alpha=None, fcap=None, rsh_frac=0.5, Kmode=None):
    key = f"{f}|{closure}|{alpha}|{fcap}|{rsh_frac}|{Kmode}"; fn = os.path.join(PARTS, key.replace("|", "__").replace("/", "-") + ".json")
    if os.path.exists(fn): return json.load(open(fn))
    st = SET[f]; out = {}
    for hst in HOSTS[f]:
        Ms = hst["Msys"]; rta = r_ta(Ms, st); Mcap = (fcap or st["fcap"]) * st["R"] * Ms
        rpts = [ft["r"] / KPC for ft in hst["pts"]]; rec = dict(cls=hst["cls"], name=hst["name"])
        if closure == "generous":
            rsh = rsh_frac * rta; sol = solve_gen(hst["Mb"], Mcap, rsh, rta, st["a0k"], alpha, st["rho_sea"])
            if sol is None: rec["fail"] = True
            else:
                Mx = Mx_gen(sol, rpts, rsh, Mcap, st["rho_sea"]) - Msea_f(np.array(rpts), st)
                rec.update(Mx=[float(v) for v in Mx], rend=sol["rend_over_rsh"], Ksh=sol["Ksh"], v2=sol["v2"], rho_sh=sol["rho_sh"])
                if hst["cls"] == "X-COP":
                    rr = sol["r"]; mm = sol["m"]; Kprof = sol["Ksh"] * (mm / Mcap) ** alpha
                    rec["Kx_at_pts"] = [float(np.interp(math.log(x), np.log(np.maximum(rr, 1e-300)), Kprof)) for x in rpts]
        else:
            rr = np.geomspace(1e-3, rta, 900); Mb = hst["Mb"](rr); Kfix = None
            if Kmode == "hostT":
                kT = 8.617333e-8 * 1e4 if hst["cls"] == "SPARC" else hst.get("kT")          # SPARC: cold ISM 1e4 K (frozen section 4)
                if kT is None or not np.isfinite(kT): rec["missing"] = True; out[str(hst["pts"][0]["SE1id"])] = rec; continue
                Kfix = kT * 1.597e5 * (4 * st["rho_sea"]) ** (-2 / 3)
            sol = solve_strict(Mb, rr, Mcap, rta, st["a0k"], st["rho_sea"], Kfix=Kfix)
            Mx = np.interp(np.log(rpts), np.log(rr), sol["Md"]); rec.update(Mx=[float(v) for v in Mx], conv=sol["conv"], capped=sol["capped"], Ksh=sol["Ksh"], ka2=sol["ka2"])
        out[str(hst["pts"][0]["SE1id"])] = rec
    json.dump(out, open(fn, "w"), default=float); return out
def cand_from(sols, f, coldH=None):
    """GB1 candidate: b = 1 + M_x(<r)/M_b(<r) from host solutions; coldH: KD captured-cold candidate for reading-H s_0 hosts."""
    bmap = {}; miss = set()
    for hst in HOSTS[f]:
        rec = sols.get(str(hst["pts"][0]["SE1id"]))
        for j, ft in enumerate(hst["pts"]):
            if coldH is not None and not hst["shockH"]: bmap[ft["SE1id"]] = ("cold", None); continue
            if rec is None or rec.get("missing") or rec.get("fail"): miss.add(ft["SE1id"]); continue
            Me = hst.get("Mpt") or (ft["Mb"] / 2 if hst["cls"] in ("UDG", "dSph") else ft["Mb"])
            bmap[ft["SE1id"]] = ("b", 1.0 + rec["Mx"][j] / Me)
    def c(ft):
        i = ft.get("SE1id")
        if i is None: return dict(b=1.0, F=1.0, T=0.0)                          # the Sun: no host collapse (KD1 P4)
        if i in miss: raise GB["Missing"]("sector_state")
        if i not in bmap:
            if ft.get("Mb") is None or ft.get("x") is None: raise GB["Missing"]("Mb")
            raise RuntimeError("point without a host")
        kind, b = bmap[i]
        return coldH(ft) if kind == "cold" else dict(b=b, F=1.0, T=0.0)
    return c
def KDc(f, mult=1.0):
    st = SET[f]; return KDNS["KD"](st["ob"], st["od"], st["h"], mult * st["mu_star"])
for f in A0:                                                        # KD1's features for its candidate (as kd1.py builds them)
    B = BATT[f]; a0 = A0[f]
    for p in B["S"] + B["E"] + B["X"] + [p for g in B["GR"][0] + B["GR"][1] for p in g["pts"]]:
        p["feat"]["Msys"] = (p["feat"]["r"] / p["feat"]["rrM"]) ** 2 * a0 / G / MS; p["feat"]["Mb_enc"] = p["feat"]["Mb"]
    for p in B["U"] + [p for c_ in B["D"].values() for p in c_]:
        Mb = p["feat"]["Mb"]; p["feat"]["Msys"] = Mb; p["feat"]["Mb_enc"] = None if Mb is None else Mb / 2
    for ft in B["K"][0] + B["K"][1]: ft["Msys"] = 1e10; ft["Mb_enc"] = 1e10
HOSTS = {f: build_hosts(f) for f in A0}
P("hosts per footing: " + ", ".join(f"{c} {sum(1 for h in HOSTS['canonical'] if h['cls'] == c)}" for c in ("SPARC", "ellipticals", "X-COP", "groups_fst0", "groups_fst1", "UDG", "dSph", "KiDS")))

# ------------------------------------------------------------------ KA2 / MUTATE iii: arm (a) with g constant = KD1
ARM_A = {}
for f in A0:
    row = grade(KDc(f), f); d, ok = rowdiff(row, KDJ["footings"][f]["static"]); ARM_A[f] = dict(row=row)
    RES["KA"][f"KA2_static_{f}"] = dict(maxdiff=d, ok=bool(ok and d <= 1e-12))
    P(f"[{f}] KA2 / MUTATE iii arm (a) g const = KD1 static rows: max|d| {d:.1e}, statuses equal {ok} -> {'PASS' if RES['KA'][f'KA2_static_{f}']['ok'] else 'FAIL'}")
    for mlt in (10.0, 100.0, 1e4):                                 # Sigma >= 0, g monotone: mu_eff = mu* sqrt(g(s)/g(s0)) >= mu*
        ARM_A[f][f"status_mu_x{mlt:g}"] = statuses(grade(KDc(f, mlt), f))
    P(f"[{f}] arm (a) statuses at mu_eff = 10, 100, 1e4 x mu* equal mu*'s: {all(ARM_A[f][f'status_mu_x{m:g}'] == statuses(row) for m in (10.0, 100.0, 1e4))}")
if MUT:
    MR = {}
    for f in A0:
        sols = host_solutions(f, "strict", Kmode="hostT"); r1 = grade(cand_from(sols, f), f)
        r2 = grade(KDc(f), f)                                       # (ii) Sigma flipped: shocked hosts sit at or below s_0 -> cold, captured (KD1)
        MR[f] = dict(i_hostT=dict(statuses=statuses(r1), rows=r1, bites=bool(any(v == "FAIL" for v in statuses(r1).values()))),
                     ii_sigma_flipped=dict(statuses=statuses(r2), G1=r2["G1 SPARC"]["status"], bites=bool(r2["G1 SPARC"]["status"] == "FAIL")),
                     iii_g_const=dict(equals_KD1=RES["KA"][f"KA2_static_{f}"]["ok"], G1=ARM_A[f]["row"]["G1 SPARC"]["status"],
                                      bites=bool(RES["KA"][f"KA2_static_{f}"]["ok"] and ARM_A[f]["row"]["G1 SPARC"]["status"] == "FAIL")))
        for g, r in r1.items(): P(f"[{f}] MUTATE (i) host temperature {g:17s} {r['status']:10s} {GB['short'](g, r) if r['num'] is not None else r['missing']}")
        P(f"[{f}] MUTATE (i) bites: {MR[f]['i_hostT']['bites']}; (ii) Sigma flipped G1 {MR[f]['ii_sigma_flipped']['G1']} -> {'BITES' if MR[f]['ii_sigma_flipped']['bites'] else 'NO BITE'}; "
          f"(iii) g const = KD1 {MR[f]['iii_g_const']['equals_KD1']}, G1 {MR[f]['iii_g_const']['G1']} -> {'BITES' if MR[f]['iii_g_const']['bites'] else 'NO BITE'}")
    RES["MUTATE"] = MR; RES["MUTATE_all_bite"] = bool(all(MR[f][k]["bites"] for f in A0 for k in MR[f]))
    P(f"MUTATE all bite: {RES['MUTATE_all_bite']}"); P("kappa = 1/2 FITTED; not theory closed.")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)
P(f"elapsed {time.time() - T0:.0f} s")

# ------------------------------------------------------------------ G9a / G9b: CLASS + Jeans growth (arm a: KD1; arm b: s = s_0, c_s ~ 1/a)
LIB, D3 = Q3["LIB"], Q3["D"]
gsrc = open(os.path.join(CL, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py")).read()
gsrc = gsrc[gsrc.index("def growth_ratio("):gsrc.index("def limber_ratio(")]
assert "jeans = 0.0 if mu is None else (kv / (a * mu)) ** 2" in gsrc
GNS = dict(Q3); exec(compile(gsrc.replace("jeans = 0.0 if mu is None else (kv / (a * mu)) ** 2", "jeans = 0.0 if mu is None else (kv / (a * mu)) ** 2 * a ** JPOW"), "growth_pw", "exec"), GNS)
KG = np.logspace(-4, 1, 70); ZG = np.linspace(0.02, Q3["ZPK"], 120)
def run_class(ob, od, h, ns, tau):
    M = Q3["Class"]()
    M.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': Q3["LMAX"] + 100, 'h': h, 'omega_b': ob, 'omega_cdm': max(od, 1e-7), 'A_s': Q3["AS0"], 'n_s': ns,
           'tau_reio': tau, 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': Q3["ZPK"]}); M.compute(); return M
def jeans_rows(M, ob, od, H0, mus, jpow):
    GNS["JPOW"] = jpow; X0 = Q3["X_of"](M); c0, _ = Q3["best_amp_chi2"](X0); Rs = GNS["growth_ratio"](M, ob, od, H0, list(mus), KG, ZG); rows = []
    for mu in mus:
        S = Q3["limber_ratio"](M, H0, KG, ZG, Rs[mu]); c, _ = Q3["best_amp_chi2"](X0 * S)
        rows.append(dict(mu=float(mu), dchi2=float(c - c0), S_L100=float(S[100]), S_L400=float(S[400])))
    return c0, rows
def mu_min_of(rows):
    for i in range(len(rows)):
        if all(x["dchi2"] <= Q3["DCHI2_LINE"] for x in rows[i:]): return rows[i]["mu"]
    return None
G9 = {}
for f in A0:
    st = SET[f]; ob, od, h = st["ob"], st["od"], st["h"]; M = run_class(ob, od, h, st["ns"], st["tau"])
    # KA2b: n = 1 Jeans term reproduces KD1's rows
    kdr = KDJ["footings"][f]["G9a_jeans"]["rows"]; c0, r0 = jeans_rows(M, ob, od, 100 * h, [r["mu"] for r in kdr], 0.0)
    dj = max(abs(a["dchi2"] - b["dchi2"]) for a, b in zip(r0, kdr)); dc = abs(c0 - KDJ["footings"][f]["G9a_shape"]["chi2_mu_inf"])
    RES["KA"][f"KA2_G9_{f}"] = dict(jeans_maxdiff=float(dj), chi2_diff=float(dc), ok=bool(dj <= 1e-6 and dc <= 1e-6))
    P(f"[{f}] KA2 G9a n=1 Jeans rows vs kd1.json: max|d| {dj:.1e}; chi2 cold limit {c0:.6f} (|d| {dc:.1e}) -> {'PASS' if RES['KA'][f'KA2_G9_{f}']['ok'] else 'FAIL'}")
    # arm (b): k^2/(a mu0^2)
    Om_x = od / h ** 2; H0 = 100 * h
    # converse: c0 that keeps the smallest SPARC host out of capture under reading H (Jeans mass at turnaround, z = 2, KD1's rule)
    Mmin = min(hh["Msys"] for hh in HOSTS[f] if hh["cls"] == "SPARC"); rho_ta = 5.55 * st["rho_m0"] * 27.0 * 1e9      # Msun/Mpc^3
    cs_per_c0 = (5.55 * 27.0) ** (1 / 3)                                                                                 # adiabatic c_s(ta)/c0
    GM = 4.30091e-9
    def MJ_of_c0(c0_):
        kJ = math.sqrt(4 * math.pi * GM * rho_ta) / (c0_ * cs_per_c0); return 4 * math.pi / 3 * rho_ta * (math.pi / kJ) ** 3
    c0_gal = (Mmin * (st["ob"] / (st["ob"] + st["od"])) ** 0 / MJ_of_c0(1.0)) ** (1 / 3)        # M_J ~ c0^3; KD1 compares M_b,sys (1+R) with M_J
    c0_gal = (Mmin * (1 + st["R"]) / MJ_of_c0(1.0)) ** (1 / 3)
    mu_gal = math.sqrt(1.5 * Om_x) * H0 / c0_gal
    mus = sorted(set(np.logspace(0, 8, 41).tolist()) | {mu_gal})
    cb, rb = jeans_rows(M, ob, od, H0, mus, 1.0); M.struct_cleanup()
    mu0J = mu_min_of(rb); c0J = math.sqrt(1.5 * Om_x) * H0 / mu0J
    a34 = 1 / 3401.0; wz = 0.6 * (c0J / a34 / C_KMS) ** 2; Om_r = 2.47e-5 * (1 + 0.2271 * 3.046) / h ** 2; aB = KDJ["footings"][f]["B1"]["a_BBN"]
    a_nr = c0J / C_KMS; bbn = (Om_x / Om_r) * min(a_nr, aB) if a_nr > 0 else 0.0
    rg = min(rb, key=lambda r: abs(math.log(r["mu"] / mu_gal)))
    G9[f] = dict(chi2_cold=cb, rows=rb, mu0_J=mu0J, c0_J_kms=c0J, w_z3400=wz, B1a=bool(wz <= 0.01), bbn_extra_over_rad=bbn, B1b=bool(bbn <= 0.067),
                 G9a=bool(cb <= Q3["CHI2_LINE"]), converse=dict(c0_gal_kms=c0_gal, mu0_gal=mu_gal, dchi2=rg["dchi2"], G9a=bool(rg["dchi2"] <= Q3["DCHI2_LINE"]), M_min_SPARC=Mmin),
                 MJ_ta_at_c0J=MJ_of_c0(c0J), mach_at_100kms=100.0 / (c0J * cs_per_c0))
    P(f"[{f}] arm (b) G9a: chi2 cold {cb:.3f}; mu0_J {mu0J:.4g} Mpc^-1 -> c0_J {c0J:.3e} km/s; w(3400) {wz:.2e}; BBN extra/rad {bbn:.2e}; "
      f"M_J(ta) at c0_J {MJ_of_c0(c0J):.2e} Msun; Mach of a 100 km/s infall {100.0/(c0J*cs_per_c0):.2e}")
    P(f"[{f}] arm (b) converse: c0 keeping the smallest SPARC host (M_sys {Mmin:.3e}) uncaptured = {c0_gal:.3g} km/s (mu0 {mu_gal:.3g}): Delta chi2 {rg['dchi2']:.1f} -> {'PASS' if rg['dchi2'] <= 4 else 'FAIL'}")
RES["G9_arm_b"] = G9
P(f"elapsed {time.time() - T0:.0f} s")

# ------------------------------------------------------------------ arm (b) statics: readings H / O x closures strict / generous
ALPHAS = (0.0, 2 / 3, 5 / 3); KEYS = ("G1 SPARC", "G2 X-COP", "G3 groups", "G4 ellipticals", "G5 Coma UDGs", "G6 dSph classes", "G7 KiDS split", "G8 Solar System")
def coma_ambient(f):
    """upper bound on an ambient sector inside each UDG: Newtonian hydrostatic total density of Coma's beta model at d_mean."""
    c2 = 8.6 * 1.597e5; beta, rc = 0.71, 276.0; out = {}
    for hst in HOSTS[f]:
        if hst["cls"] != "UDG": continue
        d = hst["d_mean"]; rho = 3 * beta * c2 * (d ** 2 + 3 * rc ** 2) / (4 * math.pi * GK * (d ** 2 + rc ** 2) ** 2)
        ft = hst["pts"][0]; rh = ft["r"] / KPC; out[ft["SE1id"]] = rho * 4 / 3 * math.pi * rh ** 3 / (ft["Mb"] / 2)
    return out
def with_ambient(c, amb):
    def cc(ft):
        o = dict(c(ft)); i = ft.get("SE1id")
        if i in amb: o["b"] = o["b"] + amb[i]
        return o
    return cc
def class_f(cand, f):
    """mean extra-mass fraction b - 1 per class (reported f table)"""
    B = BATT[f]; out = {}
    def mf(pts):
        v = []
        for ft in pts:
            try: v.append(cand(ft)["b"] - 1.0)
            except Exception: pass
        return float(np.mean(v)) if v else None
    out["SPARC"] = mf([p["feat"] for p in B["S"]]); out["X-COP"] = mf([p["feat"] for p in B["X"]]); out["ellipticals"] = mf([p["feat"] for p in B["E"]])
    out["groups_fst0"] = mf([p["feat"] for g in B["GR"][0] for p in g["pts"]]); out["groups_fst1"] = mf([p["feat"] for g in B["GR"][1] for p in g["pts"]])
    out["UDG"] = mf([p["feat"] for p in B["U"]]); out["dSph bright M31"] = mf([p["feat"] for p in B["D"]["bright M31"]]); out["dSph LG field"] = mf([p["feat"] for p in B["D"]["LG field"]])
    out["KiDS early"] = mf(B["K"][0]); out["KiDS late"] = mf(B["K"][1]); return out
KEV_CM2 = 0.6 * 1.6726e-24 * (1.155 * 1.6726e-24) ** (2 / 3) * 1e10 * (1.989e33 / 3.0857e21 ** 3) ** (-2 / 3) / 1.602176634e-9   # sector K -> keV cm^2
CONV = []
for cls in ("SPARC", "ellipticals", "X-COP", "groups_fst0", "UDG", "dSph", "KiDS"):
    f = "canonical"; st = SET[f]; h = [x for x in HOSTS[f] if x["cls"] == cls][0]; Ms = h["Msys"]; rta = r_ta(Ms, st); Mcap = st["fcap"] * st["R"] * Ms
    rp = [ft["r"] / KPC for ft in h["pts"]]; Me = np.array([h.get("Mpt") or (ft["Mb"] / 2 if cls in ("UDG", "dSph") else ft["Mb"]) for ft in h["pts"]])
    for al in ALPHAS:
        s1 = solve_gen(h["Mb"], Mcap, 0.5 * rta, rta, st["a0k"], al, st["rho_sea"]); s2 = solve_gen(h["Mb"], Mcap, 0.5 * rta, rta, st["a0k"], al, st["rho_sea"], nstep=600, rounds=9)
        b1 = 1 + Mx_gen(s1, rp, 0.5 * rta, Mcap, st["rho_sea"]) / Me; b2 = 1 + Mx_gen(s2, rp, 0.5 * rta, Mcap, st["rho_sea"]) / Me
        CONV.append(dict(cls=cls, alpha=al, max_rel_b=float(np.max(np.abs(b2 / b1 - 1)))))
RES["solver_convergence"] = dict(rows=CONV, worst=max(c["max_rel_b"] for c in CONV), line=1e-3, ok=bool(max(c["max_rel_b"] for c in CONV) <= 1e-3))
P(f"solver convergence (step count x2, one host per class, every alpha): worst rel change in b {RES['solver_convergence']['worst']:.1e} (line 1e-3) -> {'PASS' if RES['solver_convergence']['ok'] else 'FAIL'}")
ARMB = {}
for f in A0:
    AR = {}; amb = coma_ambient(f); cold = KDc(f)
    sols = {"strict": host_solutions(f, "strict")}
    for al in ALPHAS: sols[f"gen{al:.4f}"] = host_solutions(f, "generous", alpha=al)
    sols["rep_fcap1"] = host_solutions(f, "generous", alpha=2 / 3, fcap=1.0); sols["rep_rsh3"] = host_solutions(f, "generous", alpha=2 / 3, rsh_frac=1 / 3)
    for key, so in sols.items():
        for rd in ("O", "H"):
            c = cand_from(so, f, coldH=cold if rd == "H" else None); row = grade(c, f); rowa = grade(with_ambient(c, amb), f)
            AR[f"{rd}|{key}"] = dict(statuses=statuses(row), rows=row, G5_with_Coma_ambient=dict(status=rowa["G5 Coma UDGs"]["status"], num=rowa["G5 Coma UDGs"]["num"]),
                                     f_table=class_f(c, f))
            if key in ("strict",) or key.startswith("gen"):
                P(f"[{f}] arm (b) reading {rd} {key:10s}: " + "; ".join(f"{g.split()[0]} {row[g]['status'][:4]}" for g in KEYS) +
                  f" | G5 with Coma ambient {rowa['G5 Coma UDGs']['status']} ({GB['short']('G5 Coma UDGs', rowa['G5 Coma UDGs'])})")
    for key in ("strict", "gen0.0000", "gen0.6667", "gen1.6667"):
        for g in KEYS: P(f"[{f}]    O|{key} {g:17s} {AR['O|'+key]['rows'][g]['status']:10s} {GB['short'](g, AR['O|'+key]['rows'][g]) if AR['O|'+key]['rows'][g]['num'] is not None else AR['O|'+key]['rows'][g]['missing']}")
        P(f"[{f}]    O|{key} f table (mean b-1): " + ", ".join(f"{k} {v:.3g}" for k, v in AR['O|' + key]['f_table'].items() if v is not None))
    # solver health
    hl = {}
    for key, so in sols.items():
        v = list(so.values()); hl[key] = dict(n=len(v), failed=sum(1 for r in v if r.get("fail")), missing=sum(1 for r in v if r.get("missing")),
                                             max_rend=max([r.get("rend", 0.0) for r in v if "rend" in r] or [0.0]), nonconv=sum(1 for r in v if r.get("conv") is False),
                                             max_ka2=max([r.get("ka2", 0.0) for r in v if "ka2" in r] or [0.0]))
    AR["solver_health"] = hl; P(f"[{f}] solver health: " + "; ".join(f"{k} fail {h['failed']} nonconv {h['nonconv']} max hole/r_sh {h['max_rend']:.1e}" for k, h in hl.items()))
    # EN1 comparison: X-COP per radius, f predicted vs needed, sector entropy shape vs gas K
    B = BATT[f]; xs = (0.1, 0.2, 0.3, 0.5, 0.7); need = {r["x"]: r["f_need_med"] for r in EN["RES"]["within_host_need_vs_proxy"][f] if r["cls"] == "X-COP"}
    cmp = {}
    for key in ("strict", "gen0.0000", "gen0.6667", "gen1.6667"):
        c = cand_from(sols[key], f); rows = []
        for x in xs:
            pts = [p for p in B["X"] if abs(p["r_kpc"] / EN["xprof"](p["name"])["R5"] - x) < 1e-6]
            fp = float(np.median([c(p["feat"])["b"] - 1 for p in pts])); Kg = float(np.median([p["Kval"] for p in pts]))
            Kx = None
            if key.startswith("gen"):
                vals = []
                for p in pts:
                    h_ = [hh for hh in HOSTS[f] if hh["cls"] == "X-COP" and hh["name"] == p["name"]][0]; rec = sols[key][str(h_["pts"][0]["SE1id"])]
                    j = [q["SE1id"] for q in h_["pts"]].index(p["feat"]["SE1id"]); vals.append(rec["Kx_at_pts"][j] * KEV_CM2)
                Kx = float(np.median(vals))
            rows.append(dict(x=x, f_pred_med=fp, f_need_med=need[x], K_gas_med=Kg, K_sector_med_keVcm2=Kx))
        cmp[key] = rows
        P(f"[{f}] EN1 shape check {key}: " + "; ".join(f"x {r['x']}: f {r['f_pred_med']:.2f} vs need {r['f_need_med']:.2f}" + (f", K_x {r['K_sector_med_keVcm2']:.3g} vs K_gas {r['K_gas_med']:.3g}" if r['K_sector_med_keVcm2'] else "") for r in rows))
    AR["EN1_shape"] = cmp
    # no-tuning check (reading O, generous): which alpha passes each class gate
    pa = {g: [al for al in ALPHAS if AR[f"O|gen{al:.4f}"]["statuses"][g] == "PASS"] for g in KEYS}
    AR["alpha_passing_per_gate"] = pa; inter = set(ALPHAS)
    for g in KEYS: inter &= set(pa[g])
    AR["alpha_common"] = sorted(inter); P(f"[{f}] no-tuning: alphas passing per gate (reading O, generous): " + "; ".join(f"{g.split()[0]} {[round(a, 3) for a in v]}" for g, v in pa.items()) + f" -> common {sorted(inter)}")
    # shock / KA6 / Mach
    AR["KA6_max"] = max(hl["strict"]["max_ka2"], 0.0); ARMB[f] = AR
    P(f"elapsed {time.time() - T0:.0f} s")
RES["KA"]["KA6_shock_identity"] = dict(max=max(ARMB[f]["KA6_max"] for f in A0), ok=bool(max(ARMB[f]["KA6_max"] for f in A0) <= 1e-10))
P(f"KA6 strong-shock identity on every strict host: max rel {RES['KA']['KA6_shock_identity']['max']:.1e} -> {'PASS' if RES['KA']['KA6_shock_identity']['ok'] else 'FAIL'}")

# ------------------------------------------------------------------ tables and labels
def lab_rows(st):
    fails = sorted({g.split()[0] for g, v in st.items() if v == "FAIL"}); nvs = sorted({g.split()[0] for g, v in st.items() if v == "NO VERDICT"})
    return fails, nvs
TABLE = {}
for f in A0:
    t = {}
    ka = {g.split()[0]: v for g, v in statuses(ARM_A[f]["row"]).items()}; kt = KDJ["footings"][f]["at_mu_star"]
    ka.update(G9a="PASS" if kt["G9a"] else "FAIL", G9b="PASS" if kt["G9a"] else "FAIL", B1a="PASS" if kt["B1"]["B1a"] else "FAIL", B1b="PASS" if kt["B1"]["B1b"] else "FAIL")
    t["a|any reading"] = ka
    g9 = G9[f]
    for rd in ("O", "H"):
        for key in ("strict", "gen"):
            if key == "strict": st = {g.split()[0]: v for g, v in ARMB[f][f"{rd}|strict"]["statuses"].items()}
            else:
                st = {}
                for g in KEYS:
                    vv = {ARMB[f][f"{rd}|gen{al:.4f}"]["statuses"][g] for al in ALPHAS}
                    st[g.split()[0]] = vv.pop() if len(vv) == 1 else "NO VERDICT (alpha bracket)"
            st.update(G9a="PASS" if (g9["G9a"]) else "FAIL", G9b="PASS" if g9["G9a"] else "FAIL", B1a="PASS" if g9["B1a"] else "FAIL", B1b="PASS" if g9["B1b"] else "FAIL")
            t[f"b|{rd}|{key}"] = st
    TABLE[f] = t
RES["TABLE"] = TABLE; RES["arm_a"] = {f: dict(statuses=statuses(ARM_A[f]["row"]), mono=ARM_A[f], converse=KDJ["footings"][f]["converse"]) for f in A0}
RES["arm_b"] = {f: {k: v for k, v in ARMB[f].items() if k not in ()} for f in A0}
for f in A0:
    for k, st in TABLE[f].items(): P(f"[{f}] TABLE {k:16s}: " + ", ".join(f"{g} {v}" for g, v in st.items()))
labels = {}
for k in TABLE["canonical"]:
    st = {f"{f}|{g}": v for f in A0 for g, v in TABLE[f][k].items()}
    fails = sorted({g.split("|")[1] for g, v in st.items() if v == "FAIL"}); nvs = sorted({g.split("|")[1] for g, v in st.items() if v.startswith("NO VERDICT")})
    labels[k] = "PASS" if not fails and not nvs else (f"FAIL ({', '.join(fails)})" + (f"; NO VERDICT ({', '.join(nvs)})" if nvs else "") if fails else f"NO VERDICT ({', '.join(nvs)})")
    P(f"LABEL {k}: {labels[k]}")
RES["labels"] = labels
ka_ok = all(v["ok"] for k, v in RES["KA"].items() if isinstance(v, dict) and "ok" in v); RES["KA_all"] = bool(ka_ok)
P(f"KA all: {ka_ok} ({', '.join(k for k, v in RES['KA'].items() if isinstance(v, dict) and not v.get('ok', True))} failed)" if not ka_ok else "KA all: PASS")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
