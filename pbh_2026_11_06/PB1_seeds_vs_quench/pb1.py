#!/usr/bin/env python3
"""PB1_seeds_vs_quench (FROZEN_CRITERIA.md, 3b174fddd7): do primordial black holes (mass M_p, f = Omega_PBH / Omega_b)
break EB1b's web-EFE quench under WG2's R1 rule? (a) point-seed secondary infall with Compton-drag release,
(b) Poisson isocurvature (white noise, two-species linear stage) + EB1b's shell. R0 (Newton) control.
Imports EB1 / EB1b functions read-only. A PBH population is a MASS component (added to B2 here) that must be paid for.
Usage: python3 pb1.py ; PB1_MUTATE=1 python3 pb1.py (P_iso x 0: KA3 must FAIL, exit 1).
kappa = 1/2 FITTED; not theory closed. Conditional on R1, which fails the CMB-lensing shape (WG2-WG6)."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy.integrate import solve_ivp, quad, simpson

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
EBD = os.path.join(REPO, "early_bh_2026_11_06")
sys.path.insert(0, os.path.join(EBD, "EB1_seed_epoch")); sys.path.insert(0, os.path.join(EBD, "EB1b_web_efe"))
import eb1, eb1b                                                     # read only
MUTATE = os.environ.get("PB1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUTATE else ""
PISO_FAC = 0.0 if MUTATE else 1.0
EB1RES = json.load(open(os.path.join(EBD, "EB1_seed_epoch", "eb1_results.json")))
EB1BRES = json.load(open(os.path.join(EBD, "EB1b_web_efe", "eb1b_results.json")))
T0 = time.time()

G = eb1.GSH; C = eb1.C; MPC = eb1.MPC; MSUN = eb1.MSUN; MYR = eb1.MYR; H0 = eb1.H0; RHOC = eb1.RHOC
OMB, OFLD, OMR = eb1.OMB, eb1.OFLD, eb1.OMR
RHOB0 = RHOC * OMB                                                   # kg/m^3
RHOB0_MSUN_MPC3 = RHOB0 * MPC ** 3 / MSUN
A0 = eb1.A0; FOOTS = ("canonical", "alt")
SIGT = 6.6524587e-29; MP = 1.67262192e-27; YHE = 0.2453
OMG = 2.4728e-5 / eb1.H ** 2                                         # photons only (T_cmb 2.7255)
Z_ON = 50.0; Z_REL = 1000.0; Z_S = 3000.0; Z_QSO = eb1.QSO1_Z
ETA = 0.003

def OL(f): return 1.0 - OMB * (1 + f) - OFLD - OMR
def E(a, f): return np.sqrt(OMR / a ** 4 + (OMB * (1 + f) + OFLD) / a ** 3 + OL(f))
_AGE = {}
def age(a, f):
    key = (float(a), float(f))
    if key not in _AGE:
        _AGE[key] = quad(lambda x: 1.0 / (x * H0 * float(E(x, f))), 0.0, a, epsabs=0, epsrel=1e-11, limit=400)[0]
    return _AGE[key]

# ---------------------------------------------------------------- CLASS thermodynamics (WG2 settings, B2)
def class_thermo():
    from classy import Class
    c = Class(); c.set({"h": eb1.H, "omega_b": eb1.OMB_H2, "omega_cdm": 1e-7, "n_s": eb1.NS, "A_s": 2.1e-9,
                        "Omega_fld": OFLD, "w0_fld": -0.001, "wa_fld": 0.0, "cs2_fld": 1.0, "use_ppf": "no"})
    c.compute(); th = c.get_thermodynamics(); zd = c.get_current_derived_parameters(["z_d"])["z_d"]; c.struct_cleanup()
    z = np.array(th["z"]); o = np.argsort(z)
    return np.log1p(z[o]), np.array(th["x_e"])[o], np.array(th["Tb [K]"])[o], np.array(th["c_b^2"])[o], zd
LX, XE, TB, CB2, ZDRAG = class_thermo()
def xe(z): return np.interp(np.log1p(z), LX, XE)
def cb2(z): return np.interp(np.log1p(z), LX, CB2) * C ** 2     # m^2/s^2
def gamma_d(a):
    z = 1 / a - 1; rg = RHOC * OMG / a ** 4; rb = RHOB0 / a ** 3
    return (4 / 3) * (rg / rb) * xe(z) * (1 - YHE) * rb / MP * SIGT * C

# ---------------------------------------------------------------- external field tables
ZG = np.linspace(0.0, math.log1p(3500.0), 4000)                     # x = ln(1+z) grid
def e_table(foot, which, extrap):
    efun, snaps = eb1b.e_of_z(foot, which)
    zz = np.expm1(ZG); tab = np.array([efun(z) for z in zz])
    if extrap:                                                       # ZON_REL: power law of WG2's z 30-50 segment
        e30, e50 = snaps["30"], snaps["50"]; s = math.log(e50 / e30) / math.log(51 / 31)
        hi = zz > 50; tab[hi] = e50 * ((1 + zz[hi]) / 51) ** s
    return tab

# ---------------------------------------------------------------- vectorised shell integrator
def run_shells(S, a_end):
    """S: dict of arrays (n): a, r, v, Menc, f, a0, egrp (index into S['etabs']), eH0, zon, r1 (bool), drag (bool).
    Returns dict of arrays: z_ta, r_ta, nu_ta, z_coll, t_coll, r_end."""
    n = len(S["a"]); etabs = S["etabs"]
    a = S["a"].copy(); r = S["r"].copy(); v = S["v"].copy(); t = S["t"].copy()
    Menc = S["Menc"]; f = S["f"]; a0 = S["a0"]; eg = S["egrp"]; eH0 = S["eH0"]; zon = S["zon"]; r1 = S["r1"]; drag = S["drag"]
    rmax = r.copy(); turned = np.zeros(n, bool); active = np.ones(n, bool)
    out = {k: np.full(n, np.nan) for k in ("z_ta", "r_ta", "nu_ta", "z_coll", "t_coll", "r_end")}
    dx = ZG[1] - ZG[0]
    def rhs(idx, a_, r_, v_):
        f_ = f[idx]; Ea = E(a_, f_)
        rb = RHOB0 / a_ ** 3; rr = RHOC * OMR / a_ ** 4; rf = RHOC * OFLD / a_ ** 3; rl = RHOC * OL(f_)
        acc = -(4 * math.pi * G / 3) * (rb * (1 + f_) + rf + 2 * rr - 2 * rl) * r_
        gN = G * (Menc[idx] - (4 * math.pi / 3) * (1 + f_) * rb * r_ ** 3) / r_ ** 2
        z = 1 / a_ - 1; x = np.log1p(np.maximum(z, 0.0)); j = np.minimum((x / dx).astype(int), len(ZG) - 2); w = x / dx - j
        ew = etabs[eg[idx], j] * (1 - w) + etabs[eg[idx], j + 1] * w
        e = np.sqrt(ew ** 2 + (eH0[idx] * (1 + z) ** 2) ** 2)
        on = r1[idx] & (z <= zon[idx])
        yy = (np.abs(gN) + e * a0[idx]) / a0[idx]
        nu = np.where(on, 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(yy, 1e-300)), 1.0)
        return a_ * H0 * Ea, v_, acc - nu * gN, nu, gN
    while active.any():
        idx = np.nonzero(active)[0]
        a_, r_, v_, t_ = a[idx], r[idx], v[idx], t[idx]
        da, dr, dv, nu, gN = rhs(idx, a_, r_, v_)
        tdyn = 1.0 / np.sqrt(np.abs(nu * G * Menc[idx] / r_ ** 3) + 1e-300)
        dt = ETA * np.minimum(np.minimum(t_, r_ / (np.abs(v_) + 1e-300)), tdyn)
        # drag half step (exact exponential on the peculiar velocity)
        gd = np.where(drag[idx], gamma_d(a_), 0.0)
        Hh = H0 * E(a_, f[idx]); u = (v_ - Hh * r_) * np.exp(-gd * dt / 2); v_ = Hh * r_ + u
        k1 = rhs(idx, a_, r_, v_)
        k2 = rhs(idx, a_ + 0.5 * dt * k1[0], r_ + 0.5 * dt * k1[1], v_ + 0.5 * dt * k1[2])
        k3 = rhs(idx, a_ + 0.5 * dt * k2[0], r_ + 0.5 * dt * k2[1], v_ + 0.5 * dt * k2[2])
        k4 = rhs(idx, a_ + dt * k3[0], r_ + dt * k3[1], v_ + dt * k3[2])
        an = a_ + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        rn = r_ + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        vn = v_ + dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        gd2 = np.where(drag[idx], gamma_d(an), 0.0)
        Hn = H0 * E(an, f[idx]); u = (vn - Hn * rn) * np.exp(-gd2 * dt / 2); vn = Hn * rn + u
        tn = t_ + dt
        # turnaround
        newta = (~turned[idx]) & (vn < 0)
        if newta.any():
            ii = idx[newta]; out["z_ta"][ii] = 1 / an[newta] - 1; out["r_ta"][ii] = rn[newta]
            out["nu_ta"][ii] = rhs(ii, an[newta], rn[newta], vn[newta])[3]; turned[ii] = True
        rmax[idx] = np.maximum(rmax[idx], rn)
        coll = turned[idx] & (rn <= 1e-3 * rmax[idx])
        end = an >= a_end
        if coll.any():
            ii = idx[coll]; out["z_coll"][ii] = 1 / an[coll] - 1; out["t_coll"][ii] = tn[coll]; active[ii] = False
        endm = end & ~coll
        if endm.any():
            ii = idx[endm]; out["r_end"][ii] = rn[endm]; active[ii] = False
        a[idx], r[idx], v[idx], t[idx] = an, rn, vn, tn
    return out

def mk(n):
    return {"a": np.zeros(n), "r": np.zeros(n), "v": np.zeros(n), "t": np.zeros(n), "Menc": np.zeros(n), "f": np.zeros(n),
            "a0": np.zeros(n), "egrp": np.zeros(n, int), "eH0": np.zeros(n), "zon": np.zeros(n), "r1": np.zeros(n, bool),
            "drag": np.ones(n, bool)}

def RL_m(Mb_msun):                                                   # comoving Lagrangian radius, m
    return (3 * Mb_msun * MSUN / (4 * math.pi * RHOB0)) ** (1 / 3)

# ---------------------------------------------------------------- (b) linear stage
def lin_rhs(x, y, k, f, bgt):
    a = math.exp(x); dp, dp1, db, db1 = y
    if bgt is not None:                                              # KA2 test background (radiation + matter, all clustering)
        yy = a / bgt["a_eq"]; om = yy / (1 + yy); dlnH = -(4 + 3 * yy) / (2 * (1 + yy))
        Op = bgt["fp"] * om; Ob = (1 - bgt["fp"]) * om; gH = 0.0; ckH = 0.0
    else:
        E2 = OMR / a ** 4 + (OMB * (1 + f) + OFLD) / a ** 3 + OL(f)
        dlnH = (-4 * OMR / a ** 4 - 3 * (OMB * (1 + f) + OFLD) / a ** 3) / (2 * E2)
        Op = OMB * f / a ** 3 / E2; Ob = OMB / a ** 3 / E2
        Hh = H0 * math.sqrt(E2); gH = float(gamma_d(a)) / Hh
        ckH = float(cb2(1 / a - 1)) * (k / MPC) ** 2 / (a ** 2 * Hh ** 2)
    src = 1.5 * (Op * dp + Ob * db)
    return [dp1, -(2 + dlnH) * dp1 + src, db1, -(2 + dlnH + gH) * db1 + src - ckH * db]

def a_eq(f): return OMR / (OMB * (1 + f) + OFLD)

def lin_transfer(f, ks, z_outs):
    """T_p, T_b and d/dlna at each z_out, per unit initial delta_p, on a k grid (1/Mpc)."""
    aeq = a_eq(f); y0 = 1e-2; x0 = math.log(y0 * aeq)
    gam = OMB * f / (OMB * (1 + f) + OFLD)                           # clustering fraction while baryons are tied
    xo = sorted([math.log(1 / (1 + z)) for z in z_outs])
    res = {z: np.zeros((len(ks), 4)) for z in z_outs}
    for i, k in enumerate(ks):
        sol = solve_ivp(lin_rhs, (x0, xo[-1]), [1.0, 1.5 * gam * y0, 0.0, 0.0], args=(k, f, None), method="Radau",
                        rtol=1e-7, atol=[1e-12, 1e-12, 1e-14 * max(f, 1e-12), 1e-14 * max(f, 1e-12)], t_eval=xo)
        for j, z in enumerate(sorted(z_outs, reverse=True)):
            res[z][i] = sol.y[:, j]
    return res

def W(x):
    x = np.asarray(x, float); out = np.ones_like(x); s = x > 1e-3
    out[s] = 3 * (np.sin(x[s]) - x[s] * np.cos(x[s])) / x[s] ** 3; out[~s] = 1 - x[~s] ** 2 / 10; return out

def sigma_iso(Mb, Mp, f, ks, tr, cut=True, Tunit=False):
    """sigma of the clustering-mass contrast and its growth rate, white noise P_p = 1/n_p (Mpc^3)."""
    if f <= 0: return 0.0, 0.0
    n_p = f * RHOB0_MSUN_MPC3 / Mp; P = PISO_FAC / n_p
    R = (3 * Mb / (4 * math.pi * RHOB0_MSUN_MPC3)) ** (1 / 3)
    kk = np.logspace(math.log10(1e-3 / R), math.log10(3e3 / R), 6000)
    if cut: kk = kk[kk <= (6 * math.pi ** 2 * n_p) ** (1 / 3)]
    if len(kk) < 10: return 0.0, 0.0
    if Tunit: T = np.ones_like(kk); dT = np.zeros_like(kk)
    else:
        lk = np.log(ks); lkk = np.clip(np.log(kk), lk[0], lk[-1])
        Tp = np.interp(lkk, lk, tr[:, 0]); Tb = np.interp(lkk, lk, tr[:, 2])
        dTp = np.interp(lkk, lk, tr[:, 1]); dTb = np.interp(lkk, lk, tr[:, 3])
        T = (Tb + f * Tp) / (1 + f); dT = (dTb + f * dTp) / (1 + f)
    pre = kk ** 3 / (2 * math.pi ** 2) * P * W(kk * R) ** 2
    s2 = simpson(pre * T ** 2, x=np.log(kk)); sv = simpson(pre * T * dT, x=np.log(kk))
    if s2 <= 0: return 0.0, 0.0
    return math.sqrt(s2), sv / s2

# ---------------------------------------------------------------- checks
def ka2():
    bgt = {"a_eq": 1.0, "fp": 0.01}; y0 = 1e-4; x0 = math.log(y0); fp = bgt["fp"]
    dm0 = fp * (1 + 1.5 * y0); ddm0 = fp * 1.5 * y0
    y_init = [dm0 + (1 - fp), ddm0, dm0 - fp, ddm0]                  # delta_p, delta_c (species 2 = CDM-like)
    ys = [1.0, 10.0, 100.0]
    sol = solve_ivp(lin_rhs, (x0, math.log(100.0)), y_init, args=(0.0, 0.0, bgt), method="DOP853", rtol=1e-11,
                    atol=1e-14, t_eval=[math.log(v) for v in ys])
    dm = fp * sol.y[0] + (1 - fp) * sol.y[2]; target = fp * (1 + 1.5 * np.array(ys))
    rel = np.abs(dm / target - 1)
    return {"y": ys, "delta_m": dm.tolist(), "target_f(1+3y/2)": target.tolist(), "max_rel": float(rel.max()),
            "pass": bool(rel.max() < 1e-3)}

def ka3():
    rows = []
    for (Mb, Mp, f) in [(1e10, 1e3, 1e-3), (1e8, 1e2, 1.0), (1e12, 1e6, 1e-2)]:
        s, _ = sigma_iso(Mb, Mp, f, None, None, cut=False, Tunit=True); N = f * Mb / Mp
        rows.append({"Mb": Mb, "Mp": Mp, "f": f, "sigma2_N": s ** 2 * N})
    dev = max(abs(r["sigma2_N"] - 1) for r in rows)
    return {"rows": rows, "max_dev": dev, "pass": bool(dev < 0.01)}

def ka4():
    """EdS, R0, no drag: point excess d, unperturbed Hubble flow at a_i; delta_lin = (3/5) d a/a_i."""
    # emulate EdS with the run_shells machinery is not possible (B2 hard-wired); integrate the same RK4 form directly
    d = 1e-3; a_i = 1e-3; Hi = 1.0
    # dimensionless EdS: r'' = -GM_bg/r^2 - G dM / r^2 with GM_bg = (1/2) H_i^2 r_i^3, dM = d M_bg
    ri = 1.0; GM = 0.5 * Hi ** 2 * ri ** 3
    r, v, t = ri, Hi * ri, 2 / (3 * Hi); rmax = r; turned = False; t_ta = None; t_c = None
    while True:
        def acc(r_): return -GM * (1 + d) / r_ ** 2
        dt = ETA * min(t, r / abs(v), 1 / math.sqrt(GM * (1 + d) / r ** 3))
        k1r, k1v = v, acc(r); k2r, k2v = v + .5 * dt * k1v, acc(r + .5 * dt * k1r)
        k3r, k3v = v + .5 * dt * k2v, acc(r + .5 * dt * k2r); k4r, k4v = v + dt * k3v, acc(r + dt * k3r)
        r += dt / 6 * (k1r + 2 * k2r + 2 * k3r + k4r); v += dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v); t += dt
        rmax = max(rmax, r)
        if not turned and v < 0: turned = True; t_ta = t
        if turned and r <= 1e-3 * rmax: t_c = t; break
    a_ta = a_i * (t_ta / (2 / (3 * Hi))) ** (2 / 3); a_c = a_i * (t_c / (2 / (3 * Hi))) ** (2 / 3)
    dl_ta = 0.6 * d * a_ta / a_i; dl_c = 0.6 * d * a_c / a_i
    # the 3/5 growing-mode fraction is exact only for a_i -> 0 (decaying mode 2/5 a^-3/2 is negligible here)
    return {"delta_lin_ta": dl_ta, "target_ta": 1.0624, "delta_lin_coll": dl_c, "target_coll": 1.6865,
            "pass": bool(abs(dl_ta / 1.0624 - 1) < 0.01 and abs(dl_c / 1.6865 - 1) < 0.01)}

# ---------------------------------------------------------------- grids
MPS = [10.0 ** p for p in range(1, 10)]
FS = [10.0 ** p for p in range(-10, 1)]
MSH = [10.0 ** (p / 4) for p in range(-4, 33)]                      # m = M_b / M_p, 1e-1 .. 1e8
MBS = [10.0 ** p for p in range(5, 13)]
ZREP = [100, 50, 30, 20, 15, 10, Z_QSO, 5, 3, 2]
A_END_MAP = 1 / 3.0                                                  # z 2

def egroups(spec):
    """spec: list of (foot, which, extrap) -> (etabs array, index dict)."""
    keys = list(dict.fromkeys(spec)); tabs = np.array([e_table(*k) if k[1] not in ("zero", "huge") else
                                                       np.full(len(ZG), 0.0 if k[1] == "zero" else 1e3) for k in keys])
    return tabs, {k: i for i, k in enumerate(keys)}

def point_seed_set(rule, foot, which, zon, extrap=False, holts=False, drag=True):
    """all (M_p, f, m) shells for one setting; returns list of per-cell dicts."""
    etabs, gi = egroups([(foot, which, extrap)])
    rows = []
    for Mp in MPS:
        for f in FS:
            for m in MSH:
                Mb = m * Mp
                if f * m >= 1 or Mb > 1e13: continue
                rows.append((Mp, f, m, Mb))
    n = len(rows); S = mk(n); S["etabs"] = etabs
    a_s = 1 / (1 + Z_S)
    for i, (Mp, f, m, Mb) in enumerate(rows):
        RL = RL_m(Mb); S["a"][i] = a_s; S["r"][i] = a_s * RL; S["v"][i] = H0 * float(E(a_s, f)) * a_s * RL
        S["t"][i] = age(a_s, f); S["Menc"][i] = (Mp + Mb) * MSUN; S["f"][i] = f; S["a0"][i] = A0[foot]
        S["egrp"][i] = gi[(foot, which, extrap)]; S["zon"][i] = zon; S["r1"][i] = (rule == "R1"); S["drag"][i] = drag
        if holts:
            n_phys0 = f * RHOB0 / (Mp * MSUN)                       # per m^3 comoving
            S["eH0"][i] = 2.603 * G * Mp * MSUN * n_phys0 ** (2 / 3) / A0[foot]
    o = run_shells(S, A_END_MAP)
    cells = {}
    for i, (Mp, f, m, Mb) in enumerate(rows):
        c = cells.setdefault((Mp, f), [])
        zc = o["z_coll"][i]
        if np.isnan(zc): continue
        zta = o["z_ta"][i]; pot = o["nu_ta"][i] * G * (Mp + Mb) * MSUN / o["r_ta"][i]
        c.append({"m": m, "Mb": Mb, "z_coll": float(zc), "t_coll": float(o["t_coll"][i]), "z_ta": float(zta),
                  "press_ok": bool(pot >= float(cb2(zta))), "pot_over_cs2": float(pot / float(cb2(zta)))})
    return cells

def m_bound(shells, z, xi=1):
    ok = [s["Mb"] for s in shells if s["z_coll"] >= z and (xi == 0 or s["press_ok"])]
    return max(ok) if ok else 0.0

def clump_set(rule, foot, which, zstart, extrap, cellspec, TR, SAD):
    """(b): shells for M_b in MBS, nu 3,5 (and KA tables), started at zstart. cellspec: list of (Mp, f, Mb, nu) or
    ('KA', M, nu) entries; returns dict key -> z_coll (None / '>=zstart')."""
    etabs, gi = egroups([(foot, which, extrap)])
    a_on = 1 / (1 + zstart); rows = []; pre = {}
    for key in cellspec:
        Mp, f, Mb, nu = key
        sad, fad = SAD[(Mb, zstart)]
        if f > 0:
            si, fi = sigma_iso(Mb, Mp, f, TR["ks"], TR[(f, zstart)])
        else: si, fi = 0.0, 0.0
        sad_c = sad / (1 + f); s2 = sad_c ** 2 + si ** 2; s = math.sqrt(s2)
        fM = (sad_c ** 2 * fad + si ** 2 * fi) / s2
        d0 = nu * s
        if d0 >= 1.0: pre[key] = f">={zstart:g}"; continue
        rows.append((key, Mb, f, d0, fM))
    n = len(rows); S = mk(n); S["etabs"] = etabs
    for i, (key, Mb, f, d0, fM) in enumerate(rows):
        RL = RL_m(Mb); r0 = a_on * RL * (1 - d0 / 3); v0 = H0 * float(E(a_on, f)) * r0 * (1 - fM * d0 / 3)
        S["a"][i] = a_on; S["r"][i] = r0; S["v"][i] = v0; S["t"][i] = age(a_on, f); S["Menc"][i] = (1 + f) * Mb * MSUN
        S["f"][i] = f; S["a0"][i] = A0[foot]; S["egrp"][i] = gi[(foot, which, extrap)]; S["zon"][i] = zstart
        S["r1"][i] = (rule == "R1")
    out = dict(pre)
    if n:
        o = run_shells(S, A_END_MAP if cellspec and cellspec[0][0] != "KA" else 1.0)
        for i, (key, *_r) in enumerate(rows):
            out[key] = None if np.isnan(o["z_coll"][i]) else (float(o["z_coll"][i]), float(o["t_coll"][i]))
    return out

def ka_tables(foot, which, a_end=1.0):
    """f = 0 (b) pipeline on EB1b's grid; returns {M: {nu: z_coll}}."""
    etabs, gi = egroups([(foot, which, False)])
    a_on = 1 / (1 + Z_ON); rows = []
    for M in eb1.MASSES:
        s, fM = eb1.sigma_f(M, 2.1e-9, "B2", Z_ON, eb1.KMAX)
        for nu in eb1.NUS: rows.append((M, nu, nu * s, fM))
    n = len(rows); S = mk(n); S["etabs"] = etabs
    for i, (M, nu, d0, fM) in enumerate(rows):
        RL = RL_m(M); r0 = a_on * RL * (1 - d0 / 3)
        S["a"][i] = a_on; S["r"][i] = r0; S["v"][i] = H0 * float(E(a_on, 0.0)) * r0 * (1 - fM * d0 / 3)
        S["t"][i] = age(a_on, 0.0); S["Menc"][i] = M * MSUN; S["a0"][i] = A0[foot]; S["egrp"][i] = 0; S["zon"][i] = Z_ON
        S["r1"][i] = True
    o = run_shells(S, a_end)
    tab = {}
    for i, (M, nu, *_r) in enumerate(rows):
        tab.setdefault(f"{M:.0e}", {})[str(nu)] = None if np.isnan(o["z_coll"][i]) else float(o["z_coll"][i])
    return tab

def compare(tab, ref):
    pat = True; dev = 0.0
    for M in ref:
        for n in ref[M]:
            a, b = tab[M][n], ref[M][n]["z_coll"] if isinstance(ref[M][n], dict) else ref[M][n]
            if (a is None) != (b is None): pat = False
            elif a is not None: dev = max(dev, abs(math.log((1 + a) / (1 + b))))
    return pat, dev

# ---------------------------------------------------------------- QSO1 growth
def qso_growth(Mp, res_events, f, eta_f=1.0, eps=0.1):
    """res_events: list of (t_coll, M_res); Eddington from t(z 1000) with supply ceiling M_p + eta_f M_res(t)."""
    tE = eb1.T_SAL * eps / (1 - eps) * MYR
    t0 = age(1 / (1 + Z_REL), f); t1 = age(1 / (1 + Z_QSO), f)
    ev = sorted(res_events); ts = np.linspace(t0, t1, 4000); M = Mp; j = 0; cur = 0.0
    for k in range(1, len(ts)):
        while j < len(ev) and ev[j][0] <= ts[k]: cur = max(cur, ev[j][1]); j += 1
        cap = Mp + eta_f * cur
        M = min(M * math.exp((ts[k] - ts[k - 1]) / tE), max(cap, M))
    return M

# ---------------------------------------------------------------- main
def main():
    out = {"mutate": MUTATE, "definitions": "f = Omega_PBH / Omega_b; Omega_PBH added to B2 (mass paid for)",
           "z_drag_CLASS": ZDRAG, "checks": {}, "mutate_controls": {}, "diagnostics": {}}
    gz = {z: float(gamma_d(1 / (1 + z)) / (H0 * E(1 / (1 + z), 0.0))) for z in (3000, 1500, 1100, 1000, 800, 500, 200, 100, 50)}
    out["diagnostics"]["Gamma_d_over_H"] = gz
    z_rel = None
    for z in np.linspace(3000, 50, 5000):
        if gamma_d(1 / (1 + z)) / (H0 * E(1 / (1 + z), 0.0)) < 1: z_rel = float(z); break
    out["diagnostics"]["z_release_Gamma_eq_H"] = z_rel
    print(f"[{time.time()-T0:.0f}s] drag Gamma/H {gz}; release z {z_rel}")
    out["checks"]["KA2"] = ka2(); out["checks"]["KA3"] = ka3(); out["checks"]["KA4"] = ka4()
    print(f"[{time.time()-T0:.0f}s] KA2 {out['checks']['KA2']['pass']} KA3 {out['checks']['KA3']['pass']} KA4 {out['checks']['KA4']}")
    if MUTATE:
        json.dump(out, open(os.path.join(HERE, f"pb1_results{SUF}.json"), "w"), indent=1)
        print("PB1_MUTATE: checks " + ", ".join(f"{k} {'PASS' if v['pass'] else 'FAIL'}" for k, v in out["checks"].items()))
        sys.exit(0 if all(v["pass"] for v in out["checks"].values()) else 1)
    # KA1: f = 0 (b) pipeline vs EB1b stored tables
    ka1 = {}
    for foot in FOOTS:
        for which in ("p05", "med"):
            tab = ka_tables(foot, which); pat, dev = compare(tab, EB1BRES["tables"][f"{foot}|{which}"])
            ka1[f"{foot}|{which}"] = {"pattern_same": pat, "max_dln1pz": dev}
    out["checks"]["KA1"] = {"tables": ka1, "pass": all(v["pattern_same"] and v["max_dln1pz"] <= 1e-3 for v in ka1.values())}
    print(f"[{time.time()-T0:.0f}s] KA1 {ka1}")
    # MU1 (b) part: e = 0 vs EB1 isolated sphere
    mu1b = {}
    for foot in FOOTS:
        tab = ka_tables(foot, "zero"); pat, dev = compare(tab, EB1RES["collapse"][f"primary|R1|{foot}"])
        mu1b[foot] = {"pattern_same": pat, "max_dln1pz": dev}
    print(f"[{time.time()-T0:.0f}s] MU1b {mu1b}")
    # ---- (b) linear transfers
    ks = np.logspace(-1, 4, 26)
    TR = {"ks": ks}
    for f in FS:
        res = lin_transfer(f, ks, [Z_ON, Z_REL])
        TR[(f, Z_ON)] = res[Z_ON]; TR[(f, Z_REL)] = res[Z_REL]
    out["diagnostics"]["transfer_k0.1"] = {f"{f:g}": {"z50": TR[(f, Z_ON)][0].tolist(), "z1000": TR[(f, Z_REL)][0].tolist()} for f in FS}
    out["diagnostics"]["db_over_dp_z50_k0.1"] = {f"{f:g}": float(TR[(f, Z_ON)][0][2] / TR[(f, Z_ON)][0][0]) for f in FS}
    print(f"[{time.time()-T0:.0f}s] transfers done")
    SAD = {}
    for Mb in MBS:
        for zs in (Z_ON, Z_REL): SAD[(Mb, zs)] = eb1.sigma_f(Mb, 2.1e-9, "B2", zs, eb1.KMAX)
    # sigma table (diagnostic) and validity
    sig = {}
    for Mp in MPS:
        for f in FS:
            for Mb in MBS:
                si, fi = sigma_iso(Mb, Mp, f, ks, TR[(f, Z_ON)])
                sig[f"{Mp:.0e}|{f:.0e}|{Mb:.0e}"] = {"sigma_iso_z50": si, "fM_iso": fi, "N": f * Mb / Mp,
                                                     "sigma_ad_z50": SAD[(Mb, Z_ON)][0] / (1 + f)}
    out["sigma_z50"] = sig
    # iso field diagnostic at 8 x 1e10 vs e(z_on)
    diag = {}
    for Mp in MPS:
        for f in FS:
            si8, _ = sigma_iso(8e10, Mp, f, ks, TR[(f, Z_ON)])
            R8 = RL_m(8e10) / (1 + Z_ON); g = G * (1 + f) * 8e10 * MSUN * si8 / R8 ** 2
            diag[f"{Mp:.0e}|{f:.0e}"] = g / A0["canonical"] / EB1BRES["e_snaps"]["canonical|med"]["50"]
    out["diagnostics"]["iso_field_8e10_over_e_web_z50_canonical"] = diag
    efun, _ = eb1b.e_of_z("canonical", "med"); rediag = {}
    for Mp in MPS:
        row = {}
        for z in (50.0, 10.0):
            re_ = math.sqrt(G * Mp * MSUN / (efun(z) * A0["canonical"])); rsh = RL_m(10 * Mp) / (1 + z)
            row[f"z{z:g}"] = {"r_e_kpc": re_ / (MPC / 1e3), "r_shell_10Mp_kpc": rsh / (MPC / 1e3)}
        rediag[f"{Mp:.0e}"] = row
    out["diagnostics"]["r_e_vs_shell_canonical_med"] = rediag
    # ---- (b) clump runs
    spec = [(Mp, f, Mb, nu) for Mp in MPS for f in FS for Mb in MBS for nu in (3, 5) if f * Mb / Mp >= 10]
    print(f"[{time.time()-T0:.0f}s] (b) {len(spec)} clumps per setting")
    BSET = {}
    settings_b = [("R0", "canonical", "med", Z_ON, False)] + \
                 [("R1", ft, w, Z_ON, False) for ft in FOOTS for w in ("med", "p05", "p95", "zero", "huge")] + \
                 [("R1", ft, "med", Z_REL, True) for ft in FOOTS] + [("R0", "canonical", "med", Z_REL, False)]
    for (rule, ft, w, zs, ex) in settings_b:
        BSET[(rule, ft, w, zs)] = clump_set(rule, ft, w, zs, ex, spec, TR, SAD)
        print(f"[{time.time()-T0:.0f}s] (b) {rule} {ft} {w} zstart {zs:g} done")
    # ---- (a) point-seed runs
    ASET = {}
    settings_a = [("R0", "canonical", "med", Z_ON, False, False, True)] + \
                 [("R1", ft, w, Z_ON, False, False, True) for ft in FOOTS for w in ("med", "p05", "p95", "zero", "huge")] + \
                 [("R1", ft, "med", Z_REL, True, False, True) for ft in FOOTS] + \
                 [("R1", ft, "med", Z_ON, False, True, True) for ft in FOOTS] + \
                 [("R0", "canonical", "med", Z_ON, False, False, False)]
    for st in settings_a:
        rule, ft, w, zs, ex, hz, dr = st
        ASET[st] = point_seed_set(rule, ft, w, zs, ex, hz, dr)
        print(f"[{time.time()-T0:.0f}s] (a) {st} done")
    # ---- gates per setting
    def zc_of(B, key):
        v = B.get(key)
        if v is None: return None
        if isinstance(v, str): return float(v[2:])
        return v[0]
    def tc_of(B, key, f):
        v = B.get(key)
        if v is None: return None
        if isinstance(v, str): return age(1 / (1 + float(v[2:])), f)
        return v[1]
    def gates(A, B, xi=1, eta_f=1.0, eps=0.1, nu_host=5):
        cells = {}
        for Mp in MPS:
            for f in FS:
                sh = A.get((Mp, f), [])
                Mbz = {f"{z:g}": m_bound(sh, z, xi) for z in ZREP}
                ev = [(s["t_coll"], s["Mb"]) for s in sh if xi == 0 or s["press_ok"]]
                for Mb in MBS:
                    tc = tc_of(B, (Mp, f, Mb, nu_host), f)
                    if tc is not None and f * Mb / Mp >= 1: ev.append((tc, Mb))
                Mbh = qso_growth(Mp, ev, f, eta_f, eps)
                gal = {}
                for Mb in (1e9, 1e10, 1e11):
                    z3 = zc_of(B, (Mp, f, Mb, 3)); z5 = zc_of(B, (Mp, f, Mb, 5))
                    gal[f"{Mb:.0e}"] = {"z_coll_3sig": z3, "z_coll_5sig": z5}
                zb = gal["1e+10"]["z_coll_3sig"]
                via_b = zb is not None and zb >= 3
                via_a = m_bound(sh, 3, xi) >= 1e10 and f * 1e10 / Mp >= 1e-3
                Gi = Mbh >= 10 ** 7.7
                cells[f"{Mp:.0e}|{f:.0e}"] = {
                    "Mp": Mp, "f": f, "n_p_cMpc3": f * RHOB0_MSUN_MPC3 / Mp, "M_bound_a": Mbz,
                    "M_BH_z7": Mbh, "G_i": Gi, "G_i_6.9": Mbh >= 10 ** 6.9,
                    "trivial": Mp >= 10 ** 7.7, "galaxy": gal, "G_ii": bool(via_b or via_a),
                    "G_ii_via": ("b" if via_b else "") + ("a" if via_a else ""),
                    "G_ii_early": bool((zb is not None and zb >= 6) or (m_bound(sh, 6, xi) >= 1e10 and f * 1e10 / Mp >= 1e-3))}
        return cells
    G_ = {}
    G_["R0|canonical"] = gates(ASET[("R0", "canonical", "med", Z_ON, False, False, True)], BSET[("R0", "canonical", "med", Z_ON)])
    G_["R0|ZON_REL"] = gates(ASET[("R0", "canonical", "med", Z_ON, False, False, True)], BSET[("R0", "canonical", "med", Z_REL)])
    for ft in FOOTS:
        for w in ("med", "p05", "p95", "zero", "huge"):
            G_[f"R1|{ft}|{w}"] = gates(ASET[("R1", ft, w, Z_ON, False, False, True)], BSET[("R1", ft, w, Z_ON)])
        A = ASET[("R1", ft, "med", Z_ON, False, False, True)]; B = BSET[("R1", ft, "med", Z_ON)]
        G_[f"R1|{ft}|med|NOPRESS"] = gates(A, B, xi=0)
        G_[f"R1|{ft}|med|eta0.1"] = gates(A, B, eta_f=0.1)
        G_[f"R1|{ft}|med|eps0.2"] = gates(A, B, eps=0.2)
        G_[f"R1|{ft}|med|host3sig"] = gates(A, B, nu_host=3)
        G_[f"R1|{ft}|ZON_REL"] = gates(ASET[("R1", ft, "med", Z_REL, True, False, True)], BSET[("R1", ft, "med", Z_REL)])
        G_[f"R1|{ft}|PBH-EFE"] = gates(ASET[("R1", ft, "med", Z_ON, False, True, True)], B)
    out["gates"] = G_
    # ---- MUTATE controls
    mu = {}
    m1a = {}
    for ft in FOOTS:
        A0e = ASET[("R1", ft, "zero", Z_ON, False, False, True)]; Am = ASET[("R1", ft, "med", Z_ON, False, False, True)]
        ge = all(m_bound(A0e.get(c, []), Z_QSO) >= m_bound(Am.get(c, []), Z_QSO) for c in A0e.keys() | Am.keys())
        gt = any(m_bound(A0e.get(c, []), Z_QSO) > m_bound(Am.get(c, []), Z_QSO) for c in A0e.keys() | Am.keys())
        m1a[ft] = {"ge_all": ge, "gt_some": gt}
    mu["MU1"] = {"b_vs_EB1_isolated": mu1b, "a_bound_z7": m1a,
                 "pass": all(v["pattern_same"] and v["max_dln1pz"] <= 1e-3 for v in mu1b.values()) and all(v["ge_all"] and v["gt_some"] for v in m1a.values())}
    m2 = {}
    R0A = ASET[("R0", "canonical", "med", Z_ON, False, False, True)]; R0B = BSET[("R0", "canonical", "med", Z_ON)]
    for ft in FOOTS:
        Ah = ASET[("R1", ft, "huge", Z_ON, False, False, True)]; Bh = BSET[("R1", ft, "huge", Z_ON)]
        da = 0.0; pata = True; dmb = 0.0
        for c in R0A.keys() | Ah.keys():
            x = {s["m"]: s["z_coll"] for s in R0A.get(c, [])}; y = {s["m"]: s["z_coll"] for s in Ah.get(c, [])}
            if set(x) != set(y): pata = False
            for m in set(x) & set(y): da = max(da, abs((1 + y[m]) / (1 + x[m]) - 1))
            for z in ZREP:
                p_, q_ = m_bound(R0A.get(c, []), z), m_bound(Ah.get(c, []), z)
                if p_ > 0 and q_ > 0: dmb = max(dmb, abs(math.log(q_ / p_)))
        db = 0.0; patb = True
        for k in spec:
            x, y = zc_of(R0B, k), zc_of(Bh, k)
            if (x is None) != (y is None): patb = False
            elif x is not None: db = max(db, abs((1 + y) / (1 + x) - 1))
        same_map = all(G_[f"R1|{ft}|huge"][c]["G_ii"] == G_["R0|canonical"][c]["G_ii"] for c in G_["R0|canonical"])
        m2[ft] = {"a_shell_pattern_same": pata, "a_shell_max_rel_1pz": da, "a_max_dln_Mbound_grid_reported": dmb, "b_pattern_same": patb, "b_max_rel_1pz": db, "G_ii_map_same": same_map}
    mu["MU2"] = {"by_foot": m2, "pass": all(v["a_shell_pattern_same"] and v["a_shell_max_rel_1pz"] <= 0.01 and v["b_pattern_same"] and v["b_max_rel_1pz"] <= 0.01 and v["G_ii_map_same"] for v in m2.values())}
    And = ASET[("R0", "canonical", "med", Z_ON, False, False, False)]
    ge = all(m_bound(And.get(c, []), 100) >= m_bound(R0A.get(c, []), 100) for c in And.keys() | R0A.keys())
    gt = any(m_bound(And.get(c, []), 100) > m_bound(R0A.get(c, []), 100) for c in And.keys() | R0A.keys())
    mb_nd = {f"{Mp:.0e}": [m_bound(And.get((Mp, 1e-10), []), 100) / Mp, m_bound(R0A.get((Mp, 1e-10), []), 100) / Mp] for Mp in MPS}
    mu["MU3"] = {"ge_all": ge, "gt_some": gt, "Mbound_z100_over_Mp_nodrag_vs_drag_f1e-10": mb_nd, "pass": bool(ge and gt)}
    out["mutate_controls"] = mu
    # ---- labels
    def region(key, gate):
        cells = G_[key]; return [c for c, v in cells.items() if v[gate] and not (gate == "G_i" and v["trivial"])]
    def summary(key):
        cells = G_[key]; s = {}
        for gate in ("G_i", "G_ii"):
            pas = [cells[c] for c in region(key, gate)]
            minf = {}
            for Mp in MPS:
                fs = [v["f"] for v in pas if v["Mp"] == Mp]; minf[f"{Mp:.0e}"] = min(fs) if fs else None
            s[gate] = {"n_cells": len(pas), "min_f_per_Mp": minf,
                       "min_Mp": min([v["Mp"] for v in pas]) if pas else None,
                       "min_fMp": min([v["f"] * v["Mp"] for v in pas]) if pas else None,
                       "via": sorted(set(v.get("G_ii_via", "") for v in pas)) if gate == "G_ii" else None}
        both = [c for c in region(key, "G_i") if cells[c]["G_ii"]]
        s["both"] = {"n_cells": len(both), "cells": both}
        return s
    out["summary"] = {k: summary(k) for k in G_}
    prim = [f"R1|{ft}|med" for ft in FOOTS]
    both_prim = all(out["summary"][k]["both"]["n_cells"] > 0 for k in prim)
    gi_prim = all(out["summary"][k]["G_i"]["n_cells"] > 0 for k in prim)
    gii_prim = all(out["summary"][k]["G_ii"]["n_cells"] > 0 for k in prim)
    variants = [k for k in G_ if k.startswith("R1|") and k.endswith(("|p05", "ZON_REL", "PBH-EFE", "NOPRESS"))]
    any_var = any(out["summary"][k]["G_i"]["n_cells"] or out["summary"][k]["G_ii"]["n_cells"] for k in variants)
    if both_prim:
        # both gates in one cell, both footings, same cell
        common = set(out["summary"][prim[0]]["both"]["cells"]) & set(out["summary"][prim[1]]["both"]["cells"])
        label = "QUENCH BROKEN" if common else "PARTIAL"
    elif gi_prim or gii_prim: label = "PARTIAL"
    elif any_var: label = "CONDITIONAL"
    else: label = "NOT BROKEN"
    checks_ok = all(v["pass"] for v in out["checks"].values()); mu_ok = all(v["pass"] for v in mu.values())
    out["label"] = label if (checks_ok and mu_ok) else f"NO LABEL (checks {checks_ok}, mutate controls {mu_ok}); would read {label}"
    out["runtime_s"] = time.time() - T0
    json.dump(out, open(os.path.join(HERE, f"pb1_results{SUF}.json"), "w"), indent=1, default=lambda o: None)
    # ---- print
    print(f"PB1: checks " + ", ".join(f"{k} {'PASS' if v['pass'] else 'FAIL'}" for k, v in out["checks"].items()) +
          "; controls " + ", ".join(f"{k} {'PASS' if v['pass'] else 'FAIL'}" for k, v in mu.items()))
    print(f"LABEL: {out['label']}")
    for k in ["R0|canonical", "R0|ZON_REL"] + [f"R1|{ft}|{w}" for ft in FOOTS for w in ("med", "p05", "p95", "med|NOPRESS", "med|eta0.1", "med|eps0.2", "med|host3sig", "ZON_REL", "PBH-EFE", "zero")]:
        s = out["summary"][k]
        print(f"-- {k}: G_i cells {s['G_i']['n_cells']} min_Mp {s['G_i']['min_Mp']} min_fMp {s['G_i']['min_fMp']}; "
              f"G_ii cells {s['G_ii']['n_cells']} min_Mp {s['G_ii']['min_Mp']} min_fMp {s['G_ii']['min_fMp']} via {s['G_ii']['via']}; both {s['both']['n_cells']}")
        print("   min f per M_p  G_i: " + " ".join(f"{m}:{v if v is None else f'{v:.0e}'}" for m, v in s["G_i"]["min_f_per_Mp"].items()))
        print("   min f per M_p G_ii: " + " ".join(f"{m}:{v if v is None else f'{v:.0e}'}" for m, v in s["G_ii"]["min_f_per_Mp"].items()))
    for ft in FOOTS:
        print(f"-- (a) M_bound(z) / M_p, R1 {ft} med, f 1e-10 (rows M_p; cols z {ZREP})")
        for Mp in MPS:
            c = G_[f"R1|{ft}|med"][f"{Mp:.0e}|1e-10"]
            print(f"   {Mp:.0e}: " + " ".join(f"{c['M_bound_a'][f'{z:g}'] / Mp:8.2g}" for z in ZREP) + f"   M_BH(z7) {c['M_BH_z7']:.3g}")
    c = G_["R0|canonical"]
    print(f"-- (a) M_bound(z) / M_p, R0, f 1e-10")
    for Mp in MPS:
        cc = c[f"{Mp:.0e}|1e-10"]; print(f"   {Mp:.0e}: " + " ".join(f"{cc['M_bound_a'][f'{z:g}'] / Mp:8.2g}" for z in ZREP) + f"   M_BH(z7) {cc['M_BH_z7']:.3g}")
    for k in ("R0|canonical", "R1|canonical|med", "R1|alt|med"):
        print(f"-- (b) z_coll 3-sigma of M_b 1e10 under {k} (rows M_p, cols f 1e-10..1; '-' = N < 10 or none by z 2)")
        for Mp in MPS:
            row = []
            for f in FS:
                z = G_[k][f"{Mp:.0e}|{f:.0e}"]["galaxy"]["1e+10"]["z_coll_3sig"]; row.append(f"{z:6.2f}" if z is not None else "     -")
            print(f"   {Mp:.0e}: " + " ".join(row))
    print(f"runtime {out['runtime_s']:.0f} s")
    sys.exit(0 if (checks_ok and mu_ok) else 1)

if __name__ == "__main__":
    main()
