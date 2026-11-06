#!/usr/bin/env python3
"""QX10 iter_2 (FROZEN_CRITERIA.md c1f0cadb7a + AMENDMENT_A1.md 168db297bd): the sector's end state in each host's own
potential (a0 law on), n = 1 barotropic p = K rho^2, K = G lambda_J^2/(2 pi). Static method A (graded) and B (reported);
the time-dependent heating run is in qx10_i2_hydro.py.
  python3 qx10_i2.py            -> qx10_i2.json/.out
  python3 qx10_i2.py --mutate   -> qx10_i2_MUTATE.json/.out  (M1 lambda_0 = 1e-3 Mpc; M2 K x 1e4)
kappa = 1/2 FITTED; not theory closed. Footings never pooled. Units: kpc, Msun, km/s."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx10_i2_MUTATE" if MUT else "qx10_i2"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# --- QX5's data and law, executed from its source up to its grading section (read-only reuse, as QX7 iter_4 does)
Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); cut = src.index("DIR = dict(")
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], Q5, "exec"), NS)
sys.argv = argv0
G_SI, MS, KPC_M, A0, glaw_SI, XC, GR, LE, EL = (NS[k] for k in ("G", "MS", "KPC", "A0", "glaw", "XC", "GR", "LE", "EL"))

GK = 4.30091e-6                       # kpc (km/s)^2 / Msun
ACC = 1e6 / KPC_M                     # 1 (km/s)^2/kpc in m/s^2
A0K = {f: a / ACC for f, a in A0.items()}
def glaw(gN, a0k): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0k * np.maximum(gN, 0.0))

# --- QX7 iter_4's constants and corner background (QX3 iter2 worst corner)
OB, OD, H0 = 0.0215, 0.11958060485606123, 65.0
R = OD / OB; FCAP = 0.76
RHO_M0 = (OB + OD) * 3 * 100.0 ** 2 / (8 * math.pi * 4.30091e-9) / 1e9      # Msun/kpc^3 (h cancels)
RHO_D0 = OD * 3 * 100.0 ** 2 / (8 * math.pi * 4.30091e-9) / 1e9
CELLS = {"C1": (2.6102, 4.25), "C2": (1.4678, 3.5), "C3": (8.254, 5.625), "C4": (2.1544, 3.75)}
def r_ta(Mb_tot): return (Mb_tot * (1 + R) / (4 * math.pi / 3 * 5.55 * RHO_M0)) ** (1 / 3)   # kpc, z = 0 (iter_4's rule)
def K_of(lam_kpc): return GK * lam_kpc ** 2 / (2 * math.pi)


def solve_static(Mb_fn, M_t, K, rta, a0k, law=True, host=True, open_rho=None, n=1600, rmin=1e-4):
    """n = 1 hydrostatics d rho/dr = -g/(2K), g = glaw(G(M_b + M_d)/r^2). Closed (open_rho None): retained mass M_t if a
    profile with rho >= 0 ends inside r_ta, else the rho(r_ta) = 0 profile. Open: rho(r_ta) = open_rho. Picard, damped."""
    r = np.geomspace(rmin, rta, n)
    Mb = np.array([Mb_fn(x) for x in r]) if host else np.zeros(n)
    R0 = min(0.25 * math.sqrt(2 * math.pi * K / GK), rta)   # lambda/4 start
    Md = M_t * np.minimum(1.0, (r / max(R0, 1e-3)) ** 3) if open_rho is None else np.zeros(n)
    dr = np.diff(r); shell = 4 * math.pi * r ** 2
    for it in range(4000):
        gN = GK * (Mb + Md) / r ** 2
        g = glaw(gN, a0k) if law else gN
        Hc = np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]])   # int_r^{r_ta} g
        if open_rho is None:
            lr = np.log(r)
            def mass_for(lRs):   # continuous edge at r = exp(lRs)
                Hs = float(np.interp(lRs, lr, Hc)); rho = np.clip((Hc - Hs) / (2 * K), 0, None); rho[lr > lRs] = 0.0
                seg = 0.5 * (shell[1:] * rho[1:] + shell[:-1] * rho[:-1]) * dr
                m = np.concatenate([[4 / 3 * math.pi * r[0] ** 3 * rho[0]], seg])
                j = int(np.searchsorted(lr, lRs))           # partial segment r[j-1] .. Rs (rho -> 0 linearly)
                if 0 < j < n:
                    Rs_ = math.exp(lRs); m[j] = 0.5 * shell[j - 1] * rho[j - 1] * (Rs_ - r[j - 1])
                return rho, np.cumsum(m)
            rho_full, mc_full = mass_for(lr[-1])
            if mc_full[-1] <= M_t:
                rho, mc = rho_full, mc_full; Rs = rta; retained = mc[-1]; bound = False
            else:
                lo, hi = lr[1], lr[-1]
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    if mass_for(mid)[1][-1] >= M_t: hi = mid
                    else: lo = mid
                rho, mc = mass_for(hi); Rs = math.exp(hi); f = M_t / mc[-1]; rho *= f; mc *= f; retained = M_t; bound = True
        else:
            rho = open_rho + Hc / (2 * K)
            m = np.concatenate([[4 / 3 * math.pi * r[0] ** 3 * rho[0]], 0.5 * (shell[1:] * rho[1:] + shell[:-1] * rho[:-1]) * dr])
            mc = np.cumsum(m); Rs = rta; retained = mc[-1]; bound = None
        new = mc
        err = float(np.max(np.abs(new - Md)) / max(np.max(new), 1e-300))
        Md = 0.5 * Md + 0.5 * new
        if err < 1e-7 and it > 5: break
    return dict(r=r, rho=rho, Md=new, Rs=float(Rs), retained=float(retained), bound=bound, its=it, err=err)


def Mdust_at(sol, x):
    if x <= sol["r"][0]: return float(sol["Md"][0] * (x / sol["r"][0]) ** 3)
    if x >= sol["r"][-1]: return float(sol["Md"][-1])
    return float(np.interp(math.log(x), np.log(sol["r"]), sol["Md"]))


# --- hosts
def expdisc(Mb, Ropt):
    rd = Ropt / 3.2
    return lambda x: Mb * (1 - (1 + x / rd) * math.exp(-x / rd))
def pointmass(Mb): return lambda x: Mb
def profile_from(rk, Mk, Mlast, rlast):
    rr = np.concatenate([np.asarray(rk, float), [rlast]]); mm = np.concatenate([np.asarray(Mk, float), [Mlast]])
    o = np.argsort(rr); rr, mm = rr[o], np.maximum.accumulate(mm[o])
    s0 = math.log(mm[1] / mm[0]) / math.log(rr[1] / rr[0]) if len(rr) > 1 and mm[1] > mm[0] else 1.5
    def f(x):
        if x <= rr[0]: return float(mm[0] * (x / rr[0]) ** max(s0, 0.5))
        if x >= rr[-1]: return float(mm[-1])
        return float(math.exp(np.interp(math.log(x), np.log(rr), np.log(mm))))
    return f

sp = []
for ln in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    t = ln.split()
    if len(t) < 18: continue
    try: nm = t[0]; L = float(t[7]); MHI = float(t[13]); q = int(t[17]); inc = float(t[5])
    except ValueError: continue
    if q <= 2 and inc >= 30: sp.append((nm, (0.5 * L + 1.33 * MHI) * 1e9))
sp = sorted(sp, key=lambda x: -x[1])[:5]
G5SYS = [("reference", 1e10, 10.0)] + [(n_, m_, 20.0) for n_, m_ in sp]

clusters = {}
for z in XC: clusters.setdefault(z["name"], []).append(z)


def baselines(a0k):
    Lb = []
    for p in LE:
        Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]) / KPC_M
        Lb.append(math.log10(p["gobs"] / glaw_SI(p["gbar"], a0k * ACC)))
    Eb = []
    for e in EL:
        for m in (2, 4, 8):
            x = m * e["Re"]; Mp = glaw(GK * e["Mbar"](x) / x ** 2, a0k) * x ** 2 / GK; Eb.append(math.log10(e["Mtot"](x) / Mp))
    return float(np.mean(Lb)), float(np.mean(Eb))


def grade_cell(lam0_kpc, a0k, kmul=1.0, cache=None):
    K = K_of(lam0_kpc) * kmul; out = {}
    # G5
    g5 = []
    for nm, Mb, Ro in G5SYS:
        s = solve_static(expdisc(Mb, Ro), FCAP * R * Mb, K, r_ta(Mb), a0k)
        f = Mdust_at(s, Ro) / Mb; g5.append(dict(name=nm, Mb=Mb, Ropt=Ro, ratio=f, Rs_kpc=s["Rs"], rta_kpc=r_ta(Mb), bound=s["bound"],
                                                  retained_frac=s["retained"] / (FCAP * R * Mb), its=s["its"], err=s["err"]))
    out["G5"] = dict(rows=g5, pass_=bool(all(x["ratio"] <= 0.3 for x in g5)))
    # G6 (point-mass hosts; distinct masses cached)
    d = []; sols = {}
    for p in LE:
        Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]) / KPC_M
        key = round(math.log10(Mb), 6)
        if key not in sols: sols[key] = solve_static(pointmass(Mb), FCAP * R * Mb, K, r_ta(Mb), a0k)
        md = Mdust_at(sols[key], r); gN = p["gbar"] + G_SI * md * MS / (r * KPC_M) ** 2
        d.append(math.log10(p["gobs"] / glaw_SI(gN, a0k * ACC)))
    out["G6_mean"] = float(np.mean(d))
    # G7
    d = []
    for e in EL:
        Mt = e["Mbar"](1e9); s = solve_static(e["Mbar"], FCAP * R * Mt, K, r_ta(Mt), a0k)
        for m in (2, 4, 8):
            x = m * e["Re"]; md = Mdust_at(s, x); Mp = glaw(GK * (e["Mbar"](x) + md) / x ** 2, a0k) * x ** 2 / GK
            d.append(math.log10(e["Mtot"](x) / Mp))
    out["G7_mean"] = float(np.mean(d))
    # clusters (reported)
    xd = []
    for nm, pts in clusters.items():
        Ml, rl = pts[0]["Mb_last"]
        host = profile_from([p_["r_kpc"] for p_ in pts], [p_["M_b"] for p_ in pts], Ml, rl)
        s = solve_static(host, FCAP * R * Ml, K, r_ta(Ml), a0k)
        for p_ in pts:
            x = p_["r_kpc"]; md = Mdust_at(s, x); Mp = glaw(GK * (p_["M_b"] + md) / x ** 2, a0k) * x ** 2 / GK
            xd.append(math.log10(p_["M_obs"] / Mp))
    xd = np.array(xd)
    grp = {}
    for fst in (0.0, 1.0):
        npass = 0
        for gp in GR:
            Mbt = gp["g5"] * (1 + fst)
            host = profile_from([q_["r_kpc"] for q_ in gp["pts"]], [q_["M_gas"] * (1 + fst) for q_ in gp["pts"]], Mbt, gp["R5"])
            s = solve_static(host, FCAP * R * Mbt, K, r_ta(Mbt), a0k); ok = True
            for q_ in gp["pts"]:
                x = q_["r_kpc"]; Mb = q_["M_gas"] * (1 + fst); md = Mdust_at(s, x)
                Mp = glaw(GK * (Mb + md) / x ** 2, a0k) * x ** 2 / GK; dl = math.log10(q_["M_obs"] / Mp)
                ok &= abs(dl) <= 2 * q_["eM"] / (q_["M_obs"] * math.log(10))
            npass += ok
        grp[f"fst{fst:g}"] = int(npass)
    out["clusters"] = dict(X_mean=float(xd.mean()), X_rms=float(np.sqrt((xd ** 2).mean())),
                           X_pass=bool(abs(xd.mean()) <= 0.05 and np.sqrt((xd ** 2).mean()) <= 0.10), groups_npass=grp,
                           groups_strict=bool(all(v >= 16 for v in grp.values())))
    return out


def ka():
    res = {}
    # KA1: Newtonian, no host: Lane-Emden n = 1, R_s = lambda/2, any mass
    rows = []
    for lam in (100.0, 2610.2):
        for M in (1e9, 1e12):
            s = solve_static(pointmass(0.0), M, K_of(lam), 50 * lam, 1.0, law=False, host=False)
            rows.append(dict(lam=lam, M=M, Rs_over_half_lam=s["Rs"] / (lam / 2), its=s["its"]))
    res["KA1"] = dict(rows=rows, pass_=bool(all(abs(x["Rs_over_half_lam"] - 1) <= 1e-3 for x in rows)))
    # KA2: host pull and law off = iter_4's idealisation for the reference galaxy
    kar = []
    for c, l0 in list(((k, v[0]) for k, v in CELLS.items())) + [("lam100kpc", 0.1), ("lam300kpc", 0.3)]:
        lam = l0 * 1e3; Rc = lam / 2; xi = math.pi * 10.0 / Rc
        f4 = FCAP * R * ((math.sin(xi) - xi * math.cos(xi)) / math.pi if 10.0 < Rc else 1.0) if Rc < r_ta(1e10) else 0.0
        s = solve_static(pointmass(0.0), FCAP * R * 1e10, K_of(lam), max(r_ta(1e10), 1.01 * Rc), 1.0, law=False, host=False)
        mine = Mdust_at(s, 10.0) / 1e10 if Rc < r_ta(1e10) else 0.0
        kar.append(dict(cell=c, iter4=f4, solver=mine))
    res["KA2"] = dict(rows=kar, pass_=bool(all(abs(x["solver"] - x["iter4"]) <= 1e-2 * max(abs(x["iter4"]), 1e-12) or abs(x["solver"] - x["iter4"]) <= 1e-6 for x in kar)))
    return res


if __name__ == "__main__":
    P(f"QX10 iter_2 static ({'MUTATE' if MUT else 'main'}): the sector's n = 1 end state in each host's own potential, a0 law on.")
    P(f"kappa = 1/2 FITTED; not theory closed. R {R:.3f}, f_cap {FCAP}; rho_m0 {RHO_M0:.4g} Msun/kpc^3. Criteria c1f0cadb7a, A1 168db297bd.")
    RES = dict(lane="QX10 iter_2 static", criteria="c1f0cadb7a", amendment="168db297bd", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed")
    BASE = {f: baselines(a) for f, a in A0K.items()}; RES["baselines"] = BASE
    if not MUT:
        KA = ka(); RES["KA"] = KA
        P(f"KA1 Lane-Emden n=1 (Newton, no host): R_s/(lambda/2) " + ", ".join(f"{x['Rs_over_half_lam']:.5f}" for x in KA["KA1"]["rows"]) + f" -> {'PASS' if KA['KA1']['pass_'] else 'FAIL'}")
        P(f"KA2 iter_4 idealisation, reference galaxy: " + ", ".join(f"{x['cell']} {x['iter4']:.4f}/{x['solver']:.4f}" for x in KA["KA2"]["rows"]) + f" -> {'PASS' if KA['KA2']['pass_'] else 'FAIL'}")
        RES["cells"] = {}
        for c, (l0, pp) in CELLS.items():
            RES["cells"][c] = {}
            for f, a0k in A0K.items():
                o = grade_cell(l0 * 1e3, a0k); bL, bE = BASE[f]
                o["G6_shift"] = o["G6_mean"] - bL; o["G7_shift"] = o["G7_mean"] - bE
                o["G6_pass"] = bool(abs(o["G6_shift"]) <= 0.05); o["G7_pass"] = bool(abs(o["G7_shift"]) <= 0.15)
                o["pass_"] = bool(o["G5"]["pass_"] and o["G6_pass"] and o["G7_pass"])
                # open reading B for the reference galaxy (reported)
                sB = solve_static(expdisc(1e10, 10.0), 0.0, K_of(l0 * 1e3), r_ta(1e10), a0k, open_rho=RHO_D0)
                o["B_reference_Md_Ropt_over_Mb"] = Mdust_at(sB, 10.0) / 1e10
                RES["cells"][c][f] = o
                g5 = o["G5"]["rows"][0]
                P(f"{c} (lambda_0 {l0} Mpc, p {pp}) {f}: G5 ref M_d(<R_opt)/M_b {g5['ratio']:.3f} (R_s {g5['Rs_kpc']:.0f} kpc vs r_ta {g5['rta_kpc']:.0f}, "
                  f"{'bound' if g5['bound'] else 'evaporating'}, kept {g5['retained_frac']:.2f}); max over G5 {max(x['ratio'] for x in o['G5']['rows']):.3f} -> {'PASS' if o['G5']['pass_'] else 'FAIL'}; "
                  f"G6 shift {o['G6_shift']:+.3f} -> {'PASS' if o['G6_pass'] else 'FAIL'}; G7 shift {o['G7_shift']:+.3f} -> {'PASS' if o['G7_pass'] else 'FAIL'}; "
                  f"X-COP {o['clusters']['X_mean']:+.3f}/{o['clusters']['X_rms']:.3f}, groups {o['clusters']['groups_npass']}; B ref {o['B_reference_Md_Ropt_over_Mb']:.3g}")
            RES["cells"][c]["static_pass"] = bool(all(RES["cells"][c][f]["pass_"] for f in A0K))
        P("Static A labels: " + "; ".join(f"{c} {'PASS' if RES['cells'][c]['static_pass'] else 'FAIL'}" for c in CELLS))
    else:
        RES["M"] = {}
        for f, a0k in A0K.items():
            bL, bE = BASE[f]
            o1 = grade_cell(1.0, a0k)       # lambda_0 = 1e-3 Mpc = 1 kpc
            m1 = not o1["G5"]["pass_"]
            o2 = grade_cell(CELLS["C2"][0] * 1e3, a0k, kmul=1e4)
            base_ok = abs(o2["G6_mean"] - bL) <= 1e-3 and abs(o2["G7_mean"] - bE) <= 1e-3 and all(x["ratio"] <= 1e-3 for x in o2["G5"]["rows"])
            RES["M"][f] = dict(M1=dict(G5_max=max(x["ratio"] for x in o1["G5"]["rows"]), bites=bool(m1)),
                               M2=dict(G5_max=max(x["ratio"] for x in o2["G5"]["rows"]), G6_shift=o2["G6_mean"] - bL, G7_shift=o2["G7_mean"] - bE, bites=bool(base_ok)))
            P(f"{f}: M1 (lambda_0 1e-3 Mpc) G5 max {RES['M'][f]['M1']['G5_max']:.3f} -> {'BITES' if m1 else 'DOES NOT BITE'}; "
              f"M2 (K x 1e4, C2) G5 max {RES['M'][f]['M2']['G5_max']:.2e}, G6 {RES['M'][f]['M2']['G6_shift']:+.1e}, G7 {RES['M'][f]['M2']['G7_shift']:+.1e} -> {'BITES' if base_ok else 'DOES NOT BITE'}")
        RES["all_bite"] = bool(all(v["M1"]["bites"] and v["M2"]["bites"] for v in RES["M"].values()))
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
