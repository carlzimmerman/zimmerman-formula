#!/usr/bin/env python3
"""EB1b_web_efe (FROZEN_CRITERIA.md, 0ff17cf4ce): EB1's collapse + QSO1 timing gate with the external field e(z) read from
WG2's own law-on box (rebuild_2026_10_22/WG2_bare_law_web_lensing/runs, read only). Imports EB1's functions unchanged.
Usage: python3 eb1b.py ; EB1b_MUTATE=1 python3 eb1b.py (e(z) x 0; K7 must FAIL).
kappa = 1/2 FITTED; not theory closed. Conditional on R1, which fails the CMB-lensing shape (WG2-WG6)."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "EB1_seed_epoch")); import eb1     # read only
MUTATE = os.environ.get("EB1b_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUTATE else ""
WG2 = os.path.join(REPO, "rebuild_2026_10_22", "WG2_bare_law_web_lensing", "runs")
EB1RES = json.load(open(os.path.join(os.path.dirname(HERE), "EB1_seed_epoch", "eb1_results.json")))

def e_of_z(foot, which):
    d = json.load(open(os.path.join(WG2, f"R1_TIE_B2_As2.1e-09_N128_s200_zon50_{foot}.json")))
    zs = np.array([s["z"] for s in d["snaps"]]); ys = np.array([s[f"y_{which}"] for s in d["snaps"]])
    o = np.argsort(zs); x = np.log1p(zs[o]); y = ys[o]
    fac = 0.0 if MUTATE else 1.0
    return (lambda z: fac * float(np.interp(math.log1p(z), x, y))), {f"{z:g}": v for z, v in zip(zs[o], y)}

def collapse(M, delta0, fM, foot, efun):
    """EB1.collapse (B2, z_on 50, R1, TIE) with e = efun(z)."""
    bgname = "B2"; z_on = 50.0
    ob, of, orr, ol = eb1.bg(bgname); a_on = 1 / (1 + z_on)
    Mkg = M * eb1.MSUN; rho_b0 = eb1.RHOC * ob
    RL = (3 * Mkg / (4 * math.pi * rho_b0)) ** (1 / 3)
    r0 = a_on * RL * (1 - delta0 / 3); v0 = eb1.H0 * eb1.E(a_on, bgname) * r0 * (1 - fM * delta0 / 3)
    a0 = eb1.A0[foot]; G = eb1.GSH
    def rhs(t, y):
        a, r, v = y; Ea = eb1.E(a, bgname)
        rb = rho_b0 / a ** 3; rf = eb1.RHOC * of / a ** 3; rr = eb1.RHOC * orr / a ** 4; rl = eb1.RHOC * ol
        acc = -(4 * math.pi * G / 3) * (rb + rf + 2 * rr - 2 * rl) * r
        gN = G * (Mkg - (4 * math.pi / 3) * rb * r ** 3) / r ** 2
        yy = (abs(gN) + efun(1 / a - 1) * a0) / a0
        nu = 0.5 + math.sqrt(0.25 + 1.0 / max(yy, 1e-300))
        return [a * eb1.H0 * Ea, v, acc - nu * gN]
    st = {"rmax": r0, "turned": False}
    def ev_coll(t, y):
        if y[2] < 0: st["turned"] = True
        if y[1] > st["rmax"]: st["rmax"] = y[1]
        return y[1] - 1e-3 * st["rmax"] if st["turned"] else 1.0
    ev_coll.terminal = True; ev_coll.direction = -1
    def ev_end(t, y): return y[0] - 1.0
    ev_end.terminal = True
    t0 = eb1.age(a_on, bgname)
    sol = solve_ivp(rhs, (t0, t0 + 50 / eb1.H0), [a_on, r0, v0], method="DOP853", rtol=1e-10,
                    atol=[1e-14, 1e-6 * r0, 1e-14], events=[ev_coll, ev_end])
    if len(sol.t_events[0]):
        ac = sol.y_events[0][0][0]; return {"z_coll": 1 / ac - 1, "t_coll_Myr": sol.t_events[0][0] / eb1.MYR}
    return {"z_coll": None, "t_coll_Myr": None}

def table(foot, efun):
    rows = {}
    for M in eb1.MASSES:
        s, f = eb1.sigma_f(M, 2.1e-9, "B2", 50.0, eb1.KMAX)
        rows[f"{M:.0e}"] = {str(n): collapse(M, n * s, f, foot, efun) for n in eb1.NUS}
    return rows

def main():
    out = {"mutate": MUTATE, "checks": {}, "tables": {}, "gate": {}, "e_snaps": {}}
    zero = lambda z: 0.0; const = lambda z: 0.03
    # K5 / K6
    t0 = table("canonical", zero); ref = EB1RES["collapse"]["primary|R1|canonical"]
    dev = max(abs((1 + t0[M][n]["z_coll"]) / (1 + ref[M][n]["z_coll"]) - 1) for M in t0 for n in t0[M])
    out["checks"]["K5"] = {"max_rel": dev, "pass": bool(dev < 1e-6)}
    t6 = table("canonical", const)
    out["checks"]["K6"] = {"any_collapse": any(t6[M][n]["z_coll"] for M in t6 for n in t6[M]),
                           "pass": not any(t6[M][n]["z_coll"] for M in t6 for n in t6[M])}
    for foot in ("canonical", "alt"):
        for which in ("p05", "med", "p95"):
            efun, snaps = e_of_z(foot, which); out["e_snaps"][f"{foot}|{which}"] = snaps
            tab = table(foot, efun); out["tables"][f"{foot}|{which}"] = tab
            for eps in (0.1, 0.2):
                tE = eb1.T_SAL * eps / (1 - eps); t_obs = eb1.age(1 / (1 + eb1.QSO1_Z), "B2") / eb1.MYR
                for lm in eb1.QSO1_LOGM:
                    for Ms in eb1.SEEDS:
                        t_seed = t_obs - tE * math.log(10 ** lm / Ms); Mc = 10 * Ms
                        s, f = eb1.sigma_f(Mc, 2.1e-9, "B2", 50.0, eb1.KMAX)
                        nu_req = None; zc = None
                        if t_seed > 0:
                            for n in eb1.NUS:
                                o = collapse(Mc, n * s, f, foot, efun)
                                if o["t_coll_Myr"] is not None and o["t_coll_Myr"] <= t_seed:
                                    nu_req = n; zc = o["z_coll"]; break
                        out["gate"][f"{foot}|{which}|eps{eps}|logM{lm}|seed{Ms:.0e}"] = {
                            "t_seed_Myr": t_seed, "M_clump": Mc, "nu_req": nu_req, "z_coll": zc,
                            "label": eb1.label(nu_req, t_seed)}
    med = out["tables"]["canonical|med"]
    differs = any((med[M][n]["z_coll"] is None) != (t0[M][n]["z_coll"] is None) or
                  (med[M][n]["z_coll"] is not None and abs(med[M][n]["z_coll"] - t0[M][n]["z_coll"]) > 1e-6)
                  for M in med for n in med[M])
    out["checks"]["K7"] = {"median_differs_from_zero": differs, "pass": bool(differs)}
    json.dump(out, open(os.path.join(HERE, f"eb1b_results{SUF}.json"), "w"), indent=1)
    print(f"EB1b{SUF}: checks " + ", ".join(f"{k} {'PASS' if v['pass'] else 'FAIL'}" for k, v in out["checks"].items()))
    for key, tab in out["tables"].items():
        print(f"-- z_coll {key} (rows M, cols nu 1..5)")
        for M, row in tab.items():
            print(f"   {M}: " + "  ".join(f"{(row[str(n)]['z_coll'] if row[str(n)]['z_coll'] is not None else float('nan')):7.2f}" for n in eb1.NUS))
    print("-- G1 primary (median e, eps 0.1, seed 1e5)")
    for foot in ("canonical", "alt"):
        for lm in (7.7, 6.9):
            g = out["gate"][f"{foot}|med|eps0.1|logM{lm}|seed1e+05"]
            print(f"   {foot} logM {lm}: t_seed {g['t_seed_Myr']:.1f} Myr, nu_req {g['nu_req']}, z_coll {g['z_coll']}, {g['label']}")
    sys.exit(0 if all(v["pass"] for v in out["checks"].values()) else 1)

if __name__ == "__main__":
    main()
