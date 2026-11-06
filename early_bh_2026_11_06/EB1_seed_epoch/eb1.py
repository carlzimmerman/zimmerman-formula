#!/usr/bin/env python3
"""EB1_seed_epoch (FROZEN_CRITERIA.md, 7ac6bbb3f9): can a baryon clump big enough for A2744-QSO1's black hole collapse in time,
under WG2's web rule R1 (QUMOND on the peculiar field, simple nu) vs R0 (Newton, baryons only)?
Inputs reuse WG2's CLASS settings (rebuild_2026_10_22/WG2_bare_law_web_lensing/wg2_pm.py, read only, values copied here).
Usage: python3 eb1.py          (writes eb1_results.json, prints table)
       EB1_MUTATE=1 python3 eb1.py   (G halved in the shell equation; K1 must FAIL; writes eb1_results_MUTATE.json)
kappa = 1/2 FITTED; not theory closed. Conditional on R1, which fails the CMB-lensing shape (WG2-WG6)."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math
import numpy as np
from scipy.integrate import solve_ivp, quad, simpson

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "a0kit")); import a0kit                     # read only
MUTATE = os.environ.get("EB1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUTATE else ""

# ---- WG2's settings (copied, unchanged)
H = 0.6736; OMB_H2 = 0.02237; OMB = OMB_H2 / H ** 2; OMR = 4.18e-5 / H ** 2; NS = 0.9649; KP = 0.05   # KP in 1/Mpc
OFLD = 0.2504
A0 = a0kit.footings()
# ---- constants (SI)
G0 = 6.67430e-11; GSH = G0 * (0.5 if MUTATE else 1.0)    # G used in the shell equation
C = 299792458.0; MPC = 3.0856775814913673e22; MSUN = 1.98847e30; MYR = 3.15576e13
H0 = 100e3 * H / MPC                                       # 1/s
RHOC = 3 * H0 ** 2 / (8 * math.pi * G0)                    # kg/m^3
T_SAL = 6.6524587e-29 * C / (4 * math.pi * G0 * 1.67262192e-27) / MYR   # Myr, sigma_T c / (4 pi G m_p)

def bg(name):
    """Omegas (b, fld, r, L) and whether the fluid clusters (never)."""
    if name == "B2": return OMB, OFLD, OMR, 1 - OMB - OFLD - OMR
    if name == "B1": return OMB, 0.0, OMR, 1 - OMB - OMR
    if name == "EDS": return 1.0, 0.0, 0.0, 0.0
    raise ValueError(name)

def E(a, name):
    ob, of, orr, ol = bg(name); return math.sqrt(orr / a ** 4 + (ob + of) / a ** 3 + ol)

def age(a, name):
    """t(a) in s."""
    return quad(lambda x: 1.0 / (x * H0 * E(x, name)), 0.0, a, epsabs=0, epsrel=1e-11, limit=400)[0]

# ---------------------------------------------------------------- sigma_b(M) from CLASS (baryons only)
_CL = {}
def class_tf(bgname, z_on, kmax):
    key = (bgname, z_on, kmax)
    if key in _CL: return _CL[key]
    from classy import Class
    a_on = 1 / (1 + z_on); zp = 1 / (a_on * 1.02) - 1; zm = 1 / (a_on * 0.98) - 1
    p = {"h": H, "omega_b": OMB_H2, "omega_cdm": 1e-7, "n_s": NS, "A_s": 2.1e-9, "output": "mTk", "z_max_pk": zm + 1.0,
         "P_k_max_1/Mpc": kmax}
    if bgname == "B2":
        p.update({"Omega_fld": OFLD, "w0_fld": -0.001, "wa_fld": 0.0, "cs2_fld": 1.0, "use_ppf": "no"})
    c = Class(); c.set(p); c.compute()
    t0 = c.get_transfer(z=z_on); tp = c.get_transfer(z=zp); tm = c.get_transfer(z=zm)
    k = t0["k (h/Mpc)"] * H                                   # 1/Mpc
    db = t0["d_b"]; ddb = (tp["d_b"] - tm["d_b"]) / (math.log(a_on * 1.02) - math.log(a_on * 0.98))
    c.struct_cleanup()
    _CL[key] = (k, db, ddb); return _CL[key]

def R_L(M):
    """comoving Lagrangian radius (Mpc) of baryon mass M (Msun)."""
    rho_b0 = RHOC * OMB * MPC ** 3 / MSUN                     # Msun / Mpc^3
    return (3 * M / (4 * math.pi * rho_b0)) ** (1 / 3)

def W(x):
    x = np.asarray(x, float); out = np.ones_like(x); s = x > 1e-3
    out[s] = 3 * (np.sin(x[s]) - x[s] * np.cos(x[s])) / x[s] ** 3; out[~s] = 1 - x[~s] ** 2 / 10; return out

def sigma_f(M, As, bgname, z_on, kmax):
    k, db, ddb = class_tf(bgname, z_on, kmax)
    PR = 2 * math.pi ** 2 * As * (k / KP) ** (NS - 1) / k ** 3
    w2 = W(k * R_L(M)) ** 2; lk = np.log(k); pre = k ** 3 / (2 * math.pi ** 2) * PR * w2
    s2 = simpson(pre * db ** 2, x=lk); sv = simpson(pre * db * ddb, x=lk)
    return math.sqrt(s2), sv / s2                              # sigma, f_M

# ---------------------------------------------------------------- spherical collapse
def collapse(M, delta0, fM, z_on, bgname, rule, foot="canonical", a0rule="TIE", e=0.0, a0_override=None):
    """returns dict(z_ta, z_coll, t_coll_Myr, a_coll); None fields if no collapse by a = 1 (EDS: by a = 1e4)."""
    ob, of, orr, ol = bg(bgname)
    a_on = 1 / (1 + z_on)
    Mkg = M * MSUN
    rho_b0 = RHOC * ob
    RL = (3 * Mkg / (4 * math.pi * rho_b0)) ** (1 / 3)        # comoving, m
    r0 = a_on * RL * (1 - delta0 / 3)
    v0 = H0 * E(a_on, bgname) * r0 * (1 - fM * delta0 / 3)
    a0base = a0_override if a0_override is not None else A0[foot]
    a_end = 1e4 if bgname == "EDS" else 1.0
    def rhs(t, y):
        a, r, v = y
        Ea = E(a, bgname)
        rb = rho_b0 / a ** 3; rf = RHOC * of / a ** 3; rr = RHOC * orr / a ** 4; rl = RHOC * ol
        acc = -(4 * math.pi * GSH / 3) * (rb + rf + 2 * rr - 2 * rl) * r
        dM = Mkg - (4 * math.pi / 3) * rb * r ** 3
        gN = GSH * dM / r ** 2
        nu = 1.0
        if rule == "R1":
            a0 = a0base * (Ea if a0rule == "RIVAL" else 1.0)
            y_ = (abs(gN) + e * a0) / a0
            nu = 0.5 + math.sqrt(0.25 + 1.0 / max(y_, 1e-300))
        return [a * H0 * Ea, v, acc - nu * gN]
    state = {"rmax": r0, "turned": False, "a_ta": None}
    def ev_coll(t, y):
        if y[2] < 0 and not state["turned"]:
            state["turned"] = True
        if y[1] > state["rmax"]: state["rmax"] = y[1]
        return y[1] - 1e-3 * state["rmax"] if state["turned"] else 1.0
    ev_coll.terminal = True; ev_coll.direction = -1
    def ev_end(t, y): return y[0] - a_end
    ev_end.terminal = True
    def ev_ta(t, y): return y[2]
    ev_ta.terminal = False; ev_ta.direction = -1
    t0 = age(a_on, bgname)
    sol = solve_ivp(rhs, (t0, t0 + 50 / H0), [a_on, r0, v0], method="DOP853", rtol=1e-10, atol=[1e-14, 1e-6 * r0, 1e-14],
                    events=[ev_coll, ev_end, ev_ta], dense_output=False, max_step=np.inf)
    out = {"z_ta": None, "z_coll": None, "t_coll_Myr": None, "a_coll": None}
    if len(sol.t_events[2]): out["z_ta"] = 1 / sol.y_events[2][0][0] - 1
    if len(sol.t_events[0]):
        ac = sol.y_events[0][0][0]; out.update(a_coll=ac, z_coll=1 / ac - 1, t_coll_Myr=sol.t_events[0][0] / MYR)
    return out

# ---------------------------------------------------------------- checks
def checks():
    res = {}
    # K1: EdS, R0, tiny delta: linear extrapolation to collapse = 1.686
    z_on = 1000.0; d0 = 1e-4
    o = collapse(1e12, d0, 1.0, z_on, "EDS", "R0")
    dlin = d0 * o["a_coll"] * (1 + z_on) if o["a_coll"] else float("nan")
    res["K1"] = {"delta_lin_at_collapse": dlin, "target": 1.6865, "pass": abs(dlin / 1.6865 - 1) < 0.01}
    # K4: EdS age
    a = 0.3; t = age(a, "EDS"); ta = (2 / 3) * a ** 1.5 / H0
    res["K4"] = {"rel": abs(t / ta - 1), "pass": abs(t / ta - 1) < 1e-6}
    # K3: sigma convergence at 1e6
    s1 = sigma_f(1e6, 2.1e-9, "B2", 50.0, 300.0)[0]; s2 = sigma_f(1e6, 2.1e-9, "B2", 50.0, 600.0)[0]
    res["K3"] = {"sigma_300": s1, "sigma_600": s2, "rel": abs(s2 / s1 - 1), "pass": abs(s2 / s1 - 1) < 0.02}
    # K2: R1 with a0 -> 0 equals R0
    s, f = sigma_f(1e9, 2.1e-9, "B2", 50.0, 300.0)
    r0 = collapse(1e9, 3 * s, f, 50.0, "B2", "R0"); r1 = collapse(1e9, 3 * s, f, 50.0, "B2", "R1", a0_override=1e-30)
    if r0["z_coll"] is None and r1["z_coll"] is None:
        res["K2"] = {"note": "neither collapses by z 0", "pass": True}
    elif r0["z_coll"] is None or r1["z_coll"] is None:
        res["K2"] = {"r0": r0, "r1": r1, "pass": False}
    else:
        rel = abs((1 + r1["z_coll"]) / (1 + r0["z_coll"]) - 1)
        res["K2"] = {"z0": r0["z_coll"], "z1": r1["z_coll"], "rel": rel, "pass": rel < 1e-3}
    return res

# ---------------------------------------------------------------- main
MASSES = [10.0 ** p for p in range(6, 14)]
NUS = [1, 2, 3, 4, 5]
QSO1_Z = 7.0451; QSO1_LOGM = [6.9, 7.6, 7.7]; SEEDS = [1e2, 1e4, 1e5, 1e6]
KMAX = 300.0

def label(nu_req, t_seed):
    if t_seed <= 0: return "NO (age)"
    if nu_req is None: return "NO"
    return "EASY" if nu_req <= 2 else ("RARE" if nu_req <= 4 else "EXTREME")

def main():
    K = checks()
    out = {"checks": K, "mutate": MUTATE, "T_sal_Myr": T_SAL, "a0": A0}
    # sigma table
    sig = {}
    for bgname in ("B2", "B1"):
        for z_on in (50.0, 200.0):
            for As in (1e-9, 2.1e-9, 4e-9):
                sig[f"{bgname}|{z_on:g}|{As:g}"] = {f"{M:.0e}": sigma_f(M, As, bgname, z_on, KMAX) for M in MASSES}
    out["sigma"] = sig
    # collapse table: primary + brackets
    cells = []
    def cell(bgname, z_on, As, rule, foot, a0rule, e):
        rows = {}
        for M in MASSES:
            s, f = sigma_f(M, As, bgname, z_on, KMAX)
            rows[f"{M:.0e}"] = {str(n): collapse(M, n * s, f, z_on, bgname, rule, foot, a0rule, e) for n in NUS}
        return rows
    prim = dict(bgname="B2", z_on=50.0, As=2.1e-9, a0rule="TIE", e=0.0)
    variants = [("primary", prim)]
    for As in (1e-9, 4e-9): variants.append((f"As{As:g}", dict(prim, As=As)))
    variants += [("zon200", dict(prim, z_on=200.0)), ("B1", dict(prim, bgname="B1")),
                 ("e0.03", dict(prim, e=0.03)), ("e0.1", dict(prim, e=0.1)), ("RIVAL", dict(prim, a0rule="RIVAL"))]
    coll = {}
    for name, v in variants:
        coll[f"{name}|R0"] = cell(v["bgname"], v["z_on"], v["As"], "R0", "canonical", "TIE", 0.0) if name in ("primary", "As1e-09", "As4e-09", "zon200", "B1") else None
        for foot in (("canonical", "alt") if name == "primary" else ("canonical",)):
            coll[f"{name}|R1|{foot}"] = cell(v["bgname"], v["z_on"], v["As"], "R1", foot, v["a0rule"], v["e"])
    out["collapse"] = {k: v for k, v in coll.items() if v is not None}
    # seed time and gate
    gate = {}
    for name, v in variants:
        for key in [k for k in out["collapse"] if k.startswith(name + "|")]:
            rule = key.split("|")[1]; foot = key.split("|")[2] if rule == "R1" else "canonical"
            for eps in (0.1, 0.2):
                tE = T_SAL * eps / (1 - eps)
                t_obs = age(1 / (1 + QSO1_Z), v["bgname"]) / MYR
                for lm in QSO1_LOGM:
                    for Ms in SEEDS:
                        t_seed = t_obs - tE * math.log(10 ** lm / Ms)
                        Mc = 10 * Ms
                        s, f = sigma_f(Mc, v["As"], v["bgname"], v["z_on"], KMAX)
                        nu_req = None; z_c = None
                        if t_seed > 0:
                            for n in NUS:
                                o = collapse(Mc, n * s, f, v["z_on"], v["bgname"], rule, foot, v["a0rule"], v["e"])
                                if o["t_coll_Myr"] is not None and o["t_coll_Myr"] <= t_seed:
                                    nu_req = n; z_c = o["z_coll"]; break
                        gate[f"{key}|eps{eps}|logM{lm}|seed{Ms:.0e}"] = {
                            "t_obs_Myr": t_obs, "t_seed_Myr": t_seed, "M_clump": Mc, "sigma_clump": s,
                            "nu_req": nu_req, "z_coll": z_c, "label": label(nu_req, t_seed),
                            "below_jeans": Mc < 1e5}
    out["gate"] = gate
    with open(os.path.join(HERE, f"eb1_results{SUF}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=lambda o: None)
    # print
    print(f"EB1{SUF}: checks " + ", ".join(f"{k} {'PASS' if v['pass'] else 'FAIL'}" for k, v in K.items()))
    print(f"T_sal = {T_SAL:.2f} Myr; a0 canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e}")
    print("sigma_b(M) at z_on 50, B2, A_s 2.1e-9:", {k: round(v[0], 5) for k, v in sig["B2|50|2.1e-09"].items()})
    for key in ("primary|R0", "primary|R1|canonical", "primary|R1|alt"):
        print(f"-- z_coll {key} (rows M, cols nu 1..5)")
        for M, row in out["collapse"][key].items():
            print(f"   {M}: " + "  ".join(f"{(row[str(n)]['z_coll'] if row[str(n)]['z_coll'] is not None else float('nan')):7.2f}" for n in NUS))
    print("-- G1 primary cells (eps 0.1, seed 1e5)")
    for key in ("primary|R0", "primary|R1|canonical", "primary|R1|alt"):
        for lm in (7.7, 6.9):
            g = gate[f"{key}|eps0.1|logM{lm}|seed1e+05"]
            print(f"   {key} logM {lm}: t_obs {g['t_obs_Myr']:.1f} Myr, t_seed {g['t_seed_Myr']:.1f} Myr, nu_req {g['nu_req']}, z_coll {g['z_coll']}, {g['label']}")
    allpass = all(v["pass"] for v in K.values())
    sys.exit(0 if allpass else 1)

if __name__ == "__main__":
    main()
