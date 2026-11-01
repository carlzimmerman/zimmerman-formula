#!/usr/bin/env python3
"""BOLTZ1_covariant_closure. Frozen: FROZEN_CRITERIA.md (e7bc4064fa).
Modes: algebra (Parts A, B, K4, K5, K6), checks (K1-K3), fit (Part C fit), channel (shear + forest), grade.
Imports RF5's rf5.py read-only with its module paths redirected; rf5's SIGTERM -> Preempted -> exit 75 path applies; rerun resumes.
Run: PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 boltz1.py <mode>
kappa = 1/2 FITTED, unused; cold dark energy = gravitating field component, never a particle; not theory closed.
"""
import json, math, os, shutil, sys
sys.dont_write_bytecode = True
import numpy as np
MUT = os.environ.get("BOLTZ1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
RF5D = os.path.join(LANE, "RF5_growth_native_yardstick")
OUT = os.path.join(HERE, f"boltz1_part{TAG}.json")


def jw(p, o):
    t = p + ".tmp"
    json.dump(o, open(t, "w"), indent=1, default=float)
    os.replace(t, p)


def algebra():
    import sympy as sp
    from scipy.integrate import cumulative_trapezoid  # noqa: F401
    R = {}
    # ---- S1
    X = sp.symbols("X", positive=True)
    Pf = sp.Function("P")(X)
    PX = Pf.diff(X)
    rho = 2 * X * PX - Pf
    n = sp.sqrt(2 * X) * PX
    cs2 = PX / (PX + 2 * X * PX.diff(X))
    r1 = sp.simplify(PX / rho.diff(X) - cs2)
    drho_dlna = rho.diff(X) * (-3 * n) / n.diff(X)     # n a^3 = const
    r1b = sp.simplify(drho_dlna + 3 * (rho + Pf))
    # ---- S2: any S(x), x = ln a
    x = sp.symbols("x", real=True)
    S = sp.Function("S")(x)
    res = sp.Function("I")(x)                          # rho_res, dI/dx = -exp(-3x) S'
    sgn = +1 if MUT else -1                            # m1 flips the reservoir pressure
    rho_c = sp.exp(-3 * x) * S
    Pu = sgn * res
    rho_u = rho_c + res
    dI = -sp.exp(-3 * x) * S.diff(x)
    dP = (sgn * dI)
    drho = (rho_c.diff(x) + dI)
    r2 = sp.simplify(dP / drho + S.diff(x) / S / 3)
    # ---- S3
    Q, mu, G, rh = sp.symbols("Q mu G rho", positive=True)
    e = sp.symbols("epsilon", positive=True)
    rq = mu**2 * (Q**2 - 1) / (8 * sp.pi * G)
    pq = mu**2 * (Q - 1) ** 2 / (8 * sp.pi * G)
    r3a = sp.simplify(pq.diff(Q) / rq.diff(Q) - (Q - 1) / Q)
    eps_lead = sp.limit((rq.subs(Q, 1 + e) * 4 * sp.pi * G / mu**2) / e, e, 0)   # rho 4 pi G / mu^2 = eps at leading order
    r3b = sp.simplify(eps_lead - 1)
    Kp = 2 * sp.pi * G / mu**2                         # P = K rho^2 at leading order
    r3c = sp.simplify(sp.limit(pq.subs(Q, 1 + e) / rq.subs(Q, 1 + e) ** 2 , e, 0) - Kp)
    R3 = sp.pi * sp.sqrt(Kp / (2 * sp.pi * G))
    r3d = sp.simplify(R3 - sp.pi / mu)
    res_s = {"S1_csq": str(r1), "S1_cont": str(r1b), "S2": str(r2), "S3_csq": str(r3a), "S3_eps": str(r3b), "S3_K": str(r3c), "S3_R": str(r3d)}
    R["sympy"] = res_s
    s_ok = all(v == "0" for v in res_s.values())
    R["S2_pass"] = res_s["S2"] == "0"
    R["K5_pass"] = s_ok
    # ---- N1, K6 on X34's own S
    GRID = [1e6, 3e5, 1e5, 5e4, 3e4, 2e4, 1.2e4, 7000.0, 4000.0, 2500.0, 1500.0, 1100.0, 300.0, 30.0]
    W = 0.05
    N1 = {}
    k6 = 0.0
    for z in GRID:
        xon = -math.log(1 + z)
        xs = np.linspace(xon - 40 * W, xon + 40 * W, 400001)
        dx = xs[1] - xs[0]
        u = (xs - xon)
        Sv = 1 / (1 + np.exp(-2 * u / W))
        Sp = 2 / W * Sv * (1 - Sv)
        f = np.exp(-3 * u) * Sp                       # rho in units of exp(-3 xon)
        Ic = np.concatenate(([0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * dx)))
        Iv = Ic[-1] - Ic                              # rho_res
        rc = np.exp(-3 * u) * Sv
        ru = rc + Iv
        Pu_n = (+1 if MUT else -1) * Iv
        m = (Sv > 1e-6) & (Sv < 1 - 1e-6)
        dPn = np.gradient(Pu_n, dx)
        drn = np.gradient(ru, dx)
        c2 = dPn[m] / drn[m]
        id_ = np.abs(drn[m] + 3 * (ru[m] - Iv[m]))    # rho_u + P_u = rho_c
        k6 = max(k6, float(np.max(id_ / ru[m])))
        N1[f"{z:g}"] = {"max_cs2": float(c2.max()), "min_cs2": float(c2.min()), "mean_dPdrho_step": float((Pu_n[m][-1] - Pu_n[m][0]) / (ru[m][-1] - ru[m][0])),
                        "formula_err": float(np.max(np.abs(c2 + (2 / W) * (1 - Sv[m]) / 3))) if not MUT else None}
    R["N1"] = N1
    R["N1_all_negative"] = all(v["max_cs2"] < 0 for v in N1.values())
    R["K6"] = {"max_rel": k6, "pass": k6 <= 1e-6}
    R["label_A"] = "NO TURN-ON IN P(X)" if (R["S2_pass"] and res_s["S1_csq"] == "0" and res_s["S1_cont"] == "0" and R["N1_all_negative"]) else "TURN-ON ALLOWED"
    # ---- K4, Q6's arithmetic, Q6's parameters
    from scipy.optimize import brentq
    q6 = json.load(open(os.path.join(LANE, "Q6_v3_class", "q6_native_results.json")))
    q6mu = q6["stepB"]["mu_K_BBN_per_Mpc"] if "stepB" in q6 else q6["mu_K_BBN_per_Mpc"]
    HREF, TC = 0.67552, 2.7255
    HUB = 1 / 2997.92458
    om_k = C7_OMEGA()
    H0 = HREF * HUB
    OMK = om_k / HREF**2
    OMG = 2.4728e-5 * (TC / 2.7255) ** 4 / HREF**2
    NUF = 3.044 * 7 / 8 * (4 / 11) ** (4 / 3)
    OMR = OMG * (1 + NUF)
    T0 = 8.617333e-11 * TC
    aT = T0 * (3.909 / 10.75) ** (1 / 3)
    fr = 10.75 / (2 + NUF * 2) * (3.909 / 10.75) ** (4 / 3)
    nrel = 10.75 / 1.75
    pw = 3 if MUT else 6                               # m2

    def rhoK(a, m2):
        I0 = 6 * H0**2 * OMK / (math.sqrt(1 + 3 * H0**2 * OMK / m2) + 1)
        return (I0 / a**3) * (1 + I0 / (4 * m2 * a ** (pw - 3)))

    def dn(lmu, om=None):
        m2 = (10**lmu) ** 2
        return rhoK(aT, m2) / (3 * H0**2 * OMR / aT**4 * fr) * nrel - 0.5
    try:
        mu_bbn = 10 ** brentq(dn, 0, 15, xtol=1e-9)
    except ValueError:
        mu_bbn = float("nan")
    d = abs(mu_bbn / q6mu - 1) if mu_bbn == mu_bbn else float("inf")
    R["K4"] = {"mu_BBN_per_Mpc": mu_bbn, "Q6": q6mu, "rel": d, "pass": d <= 1e-6}
    # ---- Part B: floors on mu, /Mpc. RF5's 1e6 best-fit omega_c for densities
    rec = json.load(open(os.path.join(RF5D, "cells", "R1_1000000.json")))
    omc = rec["params"]["omega_c"]
    H100 = 100.0                                       # km/s/Mpc
    pc_Mpc = 1e-6
    fourpiGrho = lambda z: 1.5 * omc * H100**2 * (1 + z) ** 3   # (km/s/Mpc)^2
    mu_for = math.sqrt(fourpiGrho(3.0)) / 6.0
    eps_1e8 = 714.0 * 10 ** ((8 - 10) / 3)             # pc
    mu_cross = math.pi / (eps_1e8 * pc_Mpc)
    floors = {"BBN_Q6": mu_bbn, "forest_X22_6kms_z3": mu_for, "crossing_R_le_eps_1e8": mu_cross}
    R["B_floors_on_mu_per_Mpc"] = floors
    R["B_eps_1e8_pc"] = eps_1e8
    bb = mu_bbn if mu_bbn == mu_bbn else q6mu
    R["B_R_at_muBBN_pc"] = math.pi / bb / pc_Mpc
    # G rho in (km/s)^2/pc^2: G = 4.30091e-3 pc (km/s)^2 / Msun
    GN = 4.30091e-3
    def cs(rho_Msun_pc3, mu_per_Mpc):
        return math.sqrt(4 * math.pi * GN * rho_Msun_pc3) / (mu_per_Mpc * pc_Mpc)
    rho200 = 200 * 3 * (100 * 0.675 / 1e6) ** 2 / (8 * math.pi * GN)   # Msun/pc^3
    tab = {}
    for lab, r_ in (("200 rho_crit", rho200), ("1 Msun/pc^3", 1.0), ("100 Msun/pc^3", 100.0)):
        tab[lab] = {"cs_kms_at_muBBN": cs(r_, bb), "cs_kms_at_mu_cross": cs(r_, mu_cross), "cosmic_z_same_density": (r_ / (omc * 2.775e-7)) ** (1 / 3) - 1}
    R["B_cs_table"] = tab
    win = {}
    for z in (3e4, 1e6):
        win[f"{z:g}"] = {"cs_over_c_at_muBBN": math.sqrt(fourpiGrho(z)) / bb / 299792.458, "cs_over_c_at_mu_cross": math.sqrt(fourpiGrho(z)) / mu_cross / 299792.458}
    R["B_window_map"] = win
    # z where eps = 1 (stiff onset) at each floor
    R["B_z_eps1"] = {k: (2 * (v * v) / (3 * (H100 / 299792.458) ** 2 * omc)) ** (1 / 3) - 1 for k, v in floors.items() if v == v}
    test = 100 * bb
    R["B_all_met_at_100muBBN"] = all(test >= v for v in floors.values() if v == v)
    R["label_B"] = "CEILINGS ONLY, NO PINCER" if R["B_all_met_at_100muBBN"] else "PINCER"
    R["label_B2"] = "PRESSURE CORE EXCLUDED IN THIS FAMILY" if R["B_R_at_muBBN_pc"] < eps_1e8 else "NOT EXCLUDED"
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    prev.update(R)
    jw(OUT, prev)
    print(json.dumps(R, indent=1, default=float))
    return R


def C7_OMEGA():
    # K4 is a tool check of Q6's arithmetic at Q6's own parameters; this number enters no grade.
    p = os.path.join(os.path.dirname(LANE), "covariant_push_2026_10_22", "C7_aest_class", "c7_native_results.json")
    return json.load(open(p))["fits"]["LCDM"]["params"]["omega_dm(FITTED)"]


def rf5mod():
    sys.path.insert(0, RF5D)
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    import rf5
    sys.path.pop(0)
    rf5.WORK = os.path.join(os.path.dirname(os.path.dirname(LANE)), "_external_data", f"boltz1_work{TAG}")
    rf5.CELLS = os.path.join(HERE, f"cells{TAG}")
    os.makedirs(rf5.WORK, exist_ok=True)
    os.makedirs(rf5.CELLS, exist_ok=True)
    dst = os.path.join(rf5.CELLS, "shear_scale_cut.json")
    if not os.path.exists(dst):
        shutil.copy(os.path.join(RF5D, "cells", "shear_scale_cut.json"), dst)
    return rf5


NAME = "R1_inf"


def install_off(rf5):
    orig = rf5.run
    def off(*a, **kw):
        kw["zon_off"] = True
        return orig(*a, **kw)
    rf5.run = off
    return orig


def checks():
    rf5 = rf5mod()
    R = {}
    rec = json.load(open(os.path.join(RF5D, "cells", "R1_1000000.json")))
    p = np.array([rec["params"][n] for n in rf5.NAMES])
    L = rf5.Lik()
    c = rf5.cell_obj(z=1e6)
    o = rf5.run("K1", c, p)
    if o is None:
        print("K1 CLASS fail"); sys.exit(1)
    ch = L.parts(o, rec["A"])
    dd = {k: abs(ch[k] - rec["chi2"][k]) for k in ("plik", "bao", "sn")}
    R["K1"] = {"d": dd, "chi2": {k: ch[k] for k in dd}, "max": max(dd.values()), "pass_1e-6": max(dd.values()) <= 1e-6, "pass": max(dd.values()) <= 1e-3}
    # K2
    D, F3 = rf5.forest_data()
    tab = np.load(os.path.join(os.path.dirname(rf5.WORK), "rf5_work", "forest", "R1_1000000", "z3.6.npz"))["tab"]
    fp = rf5.forest_profile(tab, D[3.6], 3.6)
    R["K2"] = {"chi2": fp["free"][0], "d": abs(fp["free"][0] - 87.35939598984058), "pass": abs(fp["free"][0] - 87.35939598984058) <= 1e-6}
    # K3
    cc = {"name": "K3", "kind": "R1", "zon": 1e4}
    a = rf5.run("off", cc, p, zon_off=not MUT)                         # m3 leaves the turn-on on at 1e4
    b = rf5.run("van", cc, p, vanilla=True)
    mx = 0.0
    for key in ("tt", "ee", "pp"):
        m = np.arange(2, 2501)
        mx = max(mx, float(np.max(np.abs(a[key][m] / b[key][m] - 1))))
    R["K3"] = {"max_dC_over_C": mx, "pass": mx <= 1e-4}
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    prev["checks"] = R
    jw(OUT, prev)
    print(json.dumps(R, indent=1, default=float))


def fit():
    rf5 = rf5mod()
    install_off(rf5)
    path = os.path.join(rf5.CELLS, NAME + ".json")
    if os.path.exists(path):
        print("done"); return
    rec = json.load(open(os.path.join(RF5D, "cells", "R1_1000000.json")))
    L = rf5.Lik()
    c = {"name": NAME, "kind": "R1", "zon": None}
    try:
        r = rf5.fit_cell(L, c, np.array([rec["params"][n] for n in rf5.NAMES]), rec["A"], maxit=10)
    except rf5.Preempted:
        sys.exit(75)
    if rf5.STOP["flag"]:
        sys.exit(75)
    r.update(cell=NAME, kind="R1", zon=None)
    rf5.jw(path, r)
    print(r["status"], r.get("chi2"), r.get("converged"), r.get("h"))


def channel():
    rf5 = rf5mod()
    install_off(rf5)
    rf5.mode_channel(NAME)
    print("channel done")


def grade():
    rf5 = rf5mod()
    r = json.load(open(os.path.join(rf5.CELLS, NAME + ".json")))
    ch = json.load(open(os.path.join(rf5.CELLS, NAME + "_channels.json")))
    r6 = json.load(open(os.path.join(RF5D, "cells", "R1_1000000.json")))
    c6 = json.load(open(os.path.join(RF5D, "cells", "R1_1000000_channels.json")))
    x = r["chi2"]
    G = {}
    G["G_CMB"] = {"chi2": x["plik"], "p": rf5.pval(x["plik"], 605)}
    G["G_BAO"] = {"chi2": x["bao"], "p": rf5.pval(x["bao"], 13)}
    G["G_SN"] = {"chi2": x["sn"], "p": rf5.pval(x["sn"], x["n_sn"] - 1)}
    sh = ch["shear"]
    G["G_SHEAR"] = {"chi2": sh["chi2"], "n": sh["n"], "p": rf5.pval(sh["chi2"], sh["n"] - 1), "A_shear": sh["A_shear"]}
    ga = all(rf5.BAND[z][0] <= r["sqrtX"][str(z)] <= rf5.BAND[z][1] for z in (1.0, 1.5, 2.33))
    G["G_A0"] = {"sqrtX": r["sqrtX"], "pass": ga}
    S = x["plik"] + x["Aprior"] + x["bao"] + x["sn"] + sh["chi2"]
    Smin = min(2324.0347150004386, S)
    S6 = r6["chi2"]["plik"] + r6["chi2"]["Aprior"] + r6["chi2"]["bao"] + r6["chi2"]["sn"] + c6["shear"]["chi2"]
    G["G_S"] = {"S": S, "S_min": Smin, "S_minus_Smin": S - Smin, "S_1e6": S6, "pass": S - Smin <= 25}
    gates_ok = all(G[k]["p"] >= 1e-3 for k in ("G_CMB", "G_BAO", "G_SN", "G_SHEAR")) and ga and G["G_S"]["pass"]
    fo = ch["forest"]
    fx = sum(v["free"][0] for v in fo.values())
    nb = sum(v["n"] for v in fo.values())
    dof = nb - 4 * len(fo)
    pj = rf5.pval(fx, dof)
    pz = {k: rf5.pval(v["free"][0], v["n"] - 4) for k, v in fo.items()}
    g0 = pj >= 0.01 and min(pz.values()) >= 1e-3
    fx6 = sum(v["free"][0] for v in c6["forest"].values())
    F = {"chi2": fx, "dof": dof, "p": pj, "p_z": pz, "G0": g0, "chi2_1e6": fx6, "per_z_free": {k: v["free"] for k, v in fo.items()},
         "vfbar": sum(v["vfbar"][0] for v in fo.values()), "vfbar_1e6": sum(v["vfbar"][0] for v in c6["forest"].values())}
    if not gates_ok:
        lab = "DUST LIMIT FAILS " + ",".join(k for k in G if not (G[k].get("pass", G[k].get("p", 0) >= 1e-3)))
    elif g0:
        lab = "DUST LIMIT PASSES GATES, FOREST G0 NOW PASSES"
    else:
        lab = "DUST LIMIT PASSES GATES, FOREST NOT DIAGNOSTIC"
    P = {"params": r["params"], "params_1e6": r6["params"], "h": r["h"], "Omega_m": r["Omega_m"], "sigma8": ch.get("sigma8"), "sigma8_1e6": c6.get("sigma8"), "lowTT": x["lowTT"], "lowEE": x["lowEE"], "converged": r["converged"], "gn": r["gn"]}
    prev = json.load(open(OUT))
    prev["part_C"] = {"gates": G, "forest": F, "label_C": lab, "summary": P}
    A = prev.get("label_A"); B = prev.get("label_B")
    prev["overall"] = "NEEDS A SELECTED LAGRANGIAN" if (A == "NO TURN-ON IN P(X)" and B == "CEILINGS ONLY, NO PINCER" and gates_ok and not g0) else "SEE PARTS"
    jw(OUT, prev)
    print(json.dumps(prev["part_C"], indent=1, default=float)); print(prev["overall"])


if __name__ == "__main__":
    {"algebra": algebra, "checks": checks, "fit": fit, "channel": channel, "grade": grade}[sys.argv[1]]()
