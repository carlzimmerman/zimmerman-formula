#!/usr/bin/env python3
"""X3_switched_stiffness: does -(gamma_L/2)[max(D.P, 0)]^2 (zero new constants) make v3 well-posed where rho_tau < 0,
with every screened static result unchanged (C6 Solar System, D10 outer globulars, P3 strong field)?

v3 (THEORY_V3_DRAFT section 1; C5 at beta = eta = gamma_F = 0, xi = 1) with ONE change:
  L/sqrt(-g) = R/(4K) + P^mu A_mu - W(K|P|) - (gamma_L/2)[max(D.P, 0)]^2 + mu_K^2 (Q-1)^2/(2K),  gamma_L = K L*^2/2.
Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (8aeba82a87, committed alone before any script or number).

Runs (each: OMP_NUM_THREADS=1 nice -n 15, < 1 GB RSS, <= 30 min):
  python3 x3_switched_stiffness.py --d10 E_mid|E_lo|E_hi   D4 production (switched D10 re-solve), resumable
  python3 x3_switched_stiffness.py                         main: Parts A-E + D4 aggregation + verdict
  X3_MUTATE=1 python3 x3_switched_stiffness.py             mutation: Theta = 1 everywhere (the switch removed)
kappa = 1/2 FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
"""
import ast
import json
import math
import os
import resource
import sys
import textwrap
import time

if os.environ.get("PYTHONHASHSEED") != "0":      # determinism of sympy's simplification paths (as H4, P3)
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED="0"))

import numpy as np
import scipy.linalg as sla
import scipy.sparse as sps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
H4DIR = os.path.join(REPO, "rebuild_2026_10_22", "H4_v3_saddle_stability")
H4PY = os.path.join(H4DIR, "h4_v3_saddle_stability.py")
H4JSON = os.path.join(H4DIR, "h4_v3_saddle_stability_results.json")
D10DIR = os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar")
D10JSON = os.path.join(D10DIR, "d10_native_lstar_results.json")
CFG332JSON = os.path.join(REPO, "campaign_fresh_gravity", "CFG332_globulars_three_routes", "cfg332_globulars_results.json")
P3JSON = os.path.join(REPO, "rebuild_2026_10_22", "P3_v3_strong_field", "p3_v3_strong_field_results.json")
sys.path.insert(0, D10DIR)
import d10_solver as S  # noqa: E402  (record code, imported read-only)

MUTATE = os.environ.get("X3_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""

# ------------------------------------------------------------------ constants
c_SI = 2.99792458e8
G_SI = 6.67430e-11
GMSUN = 1.32712440018e20
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
YR = 3.15576e7
GYR = 1e9 * YR
MSUN_PC3 = MSUN / PC ** 3
LPLANCK = 1.616255e-35                                   # P3's value
SQK = math.sqrt(4 * math.pi) * LPLANCK                   # P3's K^(1/2) in m
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}       # record footing values (D10)
A0_H4 = {"canonical": 9.36e-11, "alt": 1.13e-10}        # values inside H4's reused code
LFLOOR = {"canonical": 21.7, "alt": 22.9}               # pc (D10 floors, as H4)
D10_CENTRAL = {"canonical": 21.680757539917785, "alt": 22.847696106846282}
# D10 driver constants (verbatim, for exact reuse of its production)
G10, Msun10, kpc10, PC10 = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
A_H = 3.0 * kpc10
GE2_8KPC = 2.0592e-10
UPS_V, WID = 1.6, 0.15
PRIMARY = ["NGC 2419", "Pal 3", "Pal 4", "Pal 14"]
PRIM3 = ["NGC 2419", "Pal 4", "Pal 14"]
BRACKETS = ("E_lo", "E_mid", "E_hi")

lines, checks = [], []
res = {"lane": "X3_switched_stiffness", "mutate": MUTATE, "frozen": "8aeba82a87"}


def log(s=""):
    print(s, flush=True)
    lines.append(str(s))


def check(cid, ok, value, thr):
    ok = bool(ok)
    checks.append({"id": cid, "pass": ok, "value": str(value), "threshold": thr})
    log(f"{cid} {'PASS' if ok else 'FAIL'} {value} {thr}")
    return ok


def rss_gb(who=resource.RUSAGE_SELF):
    return resource.getrusage(who).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(o) if np.isfinite(o) else str(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    return o


# ====================================================================================================== D10 machinery
def g_mw(R_kpc, Mb, a0):
    gN = G10 * Mb * Msun10 / (R_kpc * kpc10 + A_H) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))


def Mb_hi(a0):
    gN = GE2_8KPC ** 2 / (GE2_8KPC + a0)
    return gN * (8 * kpc10 + A_H) ** 2 / G10 / Msun10


EBR = {foot: {"E_lo": 4.0e10, "E_mid": 6.0e10, "E_hi": Mb_hi(a0)} for foot, a0 in A0.items()}


def s_gal(R_kpc, Mb, a0, a_m):
    """Galactic phantom at R_GC in D10 units: K rho_ph * a / a0, K rho_ph = R^-2 d/dR [R^2 (g - g_N)] (spherical AQUAL
    phantom of D10's Hernquist MW with D10's law; FRAMEWORK-NATIVE formula on SURVEY-CALIBRATION input)."""
    def F(Rm):
        gN = G10 * Mb * Msun10 / (Rm + A_H) ** 2
        g = 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
        return Rm * Rm * (g - gN)
    R = R_kpc * kpc10
    dR = 1e-4 * R
    Krho = (F(R + dR) - F(R - dR)) / (2 * dR) / R ** 2
    return Krho * a_m / a0, Krho / (4 * math.pi * G10)          # (dimensionless s_g, rho_ph in kg/m^3)


class SW(S.Solver2D):
    """D10's Solver2D with the switched stiffness: lam2 * [(D + s_g)_+ - (s_g)_+] (constant shift -lam2 (s_g)_+ so the
    far field, D -> 0, is unshifted); Jacobian I - lam2 diag(Theta(D + s_g)) J (semi-smooth Newton, D10's line search).
    switched=False is D10's operator exactly. MUTATE: Theta = 1 everywhere (the switch removed)."""

    def __init__(self, g, y, xe, Lam, sg=0.0, switched=True, isolated=False):
        super().__init__(g, y, xe, Lam, isolated=isolated)
        self.sg = float(sg)
        self.switched = bool(switched) and not MUTATE

    def resid(self, U):
        n = self.g.n
        chi, psi = U[:n], U[n:]
        D, J, Fo = self.divp(chi)
        Lp, Lop = self.lap_psi(psi, Fo)
        R1 = Lp - D
        if self.switched:
            on = (D + self.sg) > 0
            if self.sg >= 0:
                sw = np.where(on, D, -self.sg)
            else:
                sw = np.where(on, D + self.sg, 0.0)
            Js = sps.diags(on.astype(float)) @ J
        else:
            sw, Js = D, J
        R2 = chi - self.phiN - psi - self.lam2 * sw
        I = sps.identity(n, format="csr")
        Jac = sps.bmat([[-J, Lop], [I - self.lam2 * Js, -I]], format="lil")
        if self.iso:
            kk = self.g.k(self.g.Nr - 1, 0)
            R1[kk] = psi[kk]
            Jac[kk, :] = 0
            Jac[kk, n + kk] = 1.0
        return np.concatenate([R1, R2]), Jac.tocsc()

    def divfield(self, U=None):
        U = self.U if U is None else U
        return self.divp(U[:self.g.n])[0]


def d10_inputs():
    d10 = json.load(open(D10JSON))
    cl = d10["clusters"]
    umf = json.load(open(CFG332JSON))["route2"]["ups_mf"]
    return d10, cl, umf


def sigma_chain(GR, cl, foot, Mb, name, UPSG, LG, sg, switched, maxit=200):
    """one cluster's (3, nUps, nL + 2) sigma table, D10's chain: AQUAL solve, then L* ascending warm-started."""
    a0 = A0[foot]
    g = cl[name]
    a = g["rhl"] * PC10
    xe = g_mw(g["RGC"], Mb, a0) / a0
    unit = math.sqrt(a0 * a) / 1e3
    tab = np.zeros((3, len(UPSG), len(LG) + 2))
    worst, nbad, ns, itmax = 0.0, 0, 0, 0
    for iu, ups in enumerate(UPSG):
        y = G10 * ups * g["LV"] * Msun10 / (a * a * a0)
        sv = SW(GR, y, xe, 0.0, sg=sg, switched=False)
        U, r_, it_ = sv.solve()
        worst, ns, itmax = max(worst, r_), ns + 1, max(itmax, it_)
        nbad += r_ > 1e-8
        rf, gr = sv.field_monopole()
        s2, vir, wo = S.jeans(rf, gr, [g["Rbin"]])
        tab[:, iu, 0] = [s2[0], vir, wo]
        for il, Lst in enumerate(LG):
            sv = SW(GR, y, xe, Lst * PC10 / a, sg=sg, switched=switched)
            U, r_, it_ = sv.solve(U0=U, maxit=maxit)
            worst, ns, itmax = max(worst, r_), ns + 1, max(itmax, it_)
            nbad += r_ > 1e-8
            rf, gr = sv.field_monopole()
            s2, vir, wo = S.jeans(rf, gr, [g["Rbin"]])
            tab[:, iu, il + 1] = [s2[0], vir, wo]
        s2, vir, wo = S.jeans(rf, S.plummer_gN(rf, y), [g["Rbin"]])
        tab[:, iu, -1] = [s2[0], vir, wo]
    return np.sqrt(tab) * unit, {"worst_residual": worst, "n_unconverged": int(nbad), "n_solves": ns, "max_iters": itmax,
                                 "x_e": xe, "s_g": sg}


# ---- D10's statistic (verbatim logic, tables passed in)
def make_stat(d10, umf):
    UPSG = np.array(d10["Ups_grid"])
    LG = np.array(d10["L_grid"])
    SIGI = np.array(d10["sigma_int_grid"])
    LIK = {k: np.array(v) for k, v in d10["lik_tables"].items()}
    LU = np.linspace(math.log(UPSG[0]), math.log(UPSG[-1]), 600)

    def prior_of(pk, name):
        if pk == "P1":
            return UPS_V, WID
        br = "K" if pk == "P2" else "S"
        return umf[br][name][0], umf[br][name][1]

    def lnL(sigtab, name, pk, f, est, il):
        sig = sigtab[est, :, il]
        lsig = np.interp(LU, np.log(UPSG), np.log(sig))
        lp = np.interp(lsig, np.log(SIGI), LIK[f"{name}|{f}"], left=-690.0, right=-690.0)
        c, w = prior_of(pk, name)
        zz = (LU / math.log(10) - math.log10(c)) / w
        pr = np.exp(-0.5 * zz * zz)
        pr /= np.trapz(pr, LU)
        mx = lp.max()
        return mx + math.log(max(np.trapz(pr * np.exp(lp - mx), LU), 1e-300))

    def chi2(tables, pk, f, est, names):
        nL = len(LG) + 2
        return np.array([-2 * sum(lnL(tables[n], n, pk, f, est, il) for n in names) for il in range(nL)])

    def L95(c):
        cmin = c.min()
        d = c - cmin
        if d[0] <= 3.84:
            return 0.0, d
        inner = d[1:-1]
        ok = np.where(inner <= 3.84)[0]
        if len(ok) == 0:
            return (float("inf") if d[-1] <= 3.84 else float("nan")), d
        i = ok[0]
        if i == 0:
            return float(LG[0]), d
        x1, x2 = math.log(LG[i - 1]), math.log(LG[i])
        y1, y2 = inner[i - 1] - 3.84, inner[i] - 3.84
        return float(math.exp(x1 + (x2 - x1) * y1 / (y1 - y2))), d

    return UPSG, LG, chi2, L95


# ====================================================================================================== D4 production
def production(bracket):
    T0 = time.time()
    out = os.path.join(HERE, f"x3_d10_tables_{bracket}.json")
    logf = os.path.join(HERE, f"x3_d10_{bracket}.out")
    st = json.load(open(out)) if os.path.exists(out) else {"bracket": bracket, "blocks": {}, "blocks_sg0": {}}
    d10, cl, umf = d10_inputs()
    UPSG, LG = np.array(d10["Ups_grid"]), np.array(d10["L_grid"])
    GR = S.Grid2D(nper=24, Nt=16)
    plog = []

    def P(s):
        print(s, flush=True)
        plog.append(s)

    P(f"X3 D4 production, bracket {bracket}: switched D10 re-solve (s_g = Galactic phantom at R_GC); "
      f"{'resuming' if st['blocks'] else 'fresh'}")
    todo = [(foot, n, "blocks") for foot in A0 for n in PRIMARY]
    if bracket == "E_mid":
        todo += [(foot, n, "blocks_sg0") for foot in A0 for n in PRIM3]
    for foot, name, kind in todo:
        key = f"{foot}|{name}"
        if key in st[kind]:
            continue
        if time.time() - T0 > 27 * 60:
            P("time guard (27 min): saved; rerun to resume")
            json.dump(clean(st), open(out, "w"))
            open(logf, "a").write("\n".join(plog) + "\n")
            sys.exit(75)
        Mb = EBR[foot][bracket]
        a_m = cl[name]["rhl"] * PC10
        sg, rho_ph = s_gal(cl[name]["RGC"], Mb, A0[foot], a_m)
        if kind == "blocks_sg0":
            sg = 0.0
        t1 = time.time()
        tab, info = sigma_chain(GR, cl, foot, Mb, name, UPSG, LG, sg, True)
        info.update({"time_s": time.time() - t1, "rho_ph_gal_Msun_pc3": rho_ph / (Msun10 / PC10 ** 3)})
        st[kind][key] = {"sig": tab, "info": info}
        json.dump(clean(st), open(out, "w"))
        P(f"  {kind:10s} {key:22s} s_g {sg:.3e} (rho_gal {info['rho_ph_gal_Msun_pc3']:.2e} Msun/pc^3) solves "
          f"{info['n_solves']} worst residual {info['worst_residual']:.1e} unconverged {info['n_unconverged']} "
          f"max iters {info['max_iters']} ({info['time_s']:.0f} s; RSS {rss_gb():.2f} GB)")
    P(f"bracket {bracket} complete ({time.time() - T0:.0f} s, peak RSS {rss_gb():.2f} GB)")
    st["complete"] = True
    json.dump(clean(st), open(out, "w"))
    open(logf, "a").write("\n".join(plog) + "\n")


# ====================================================================================================== workers
def h4_disc_worker(foot):
    """own process: H4's AQUAL solver (imported read-only), S5a MW-like disc, isolated, fine level."""
    os.environ["OMP_NUM_THREADS"] = "1"
    sys.path.insert(0, H4DIR)
    import h4_v3_saddle_stability as H4
    L = 2.6 * KPC
    Md = 5e10
    a0h = A0_H4[foot] * L ** 2 / (G_SI * Md * MSUN)
    spec = {"name": f"S5a|{foot}", "kind": "disc", "deep": False, "hz": 0.3 / 2.6, "bulge": (1e10 / Md, 0.6 / 2.6),
            "Mtot": 1.2, "zc": 0.0, "a0h": a0h, "eh": 0.0, "box": 200.0}
    lv = H4.run_level(spec, "fine", None)
    rho = lv["rho"] * Md * MSUN / L ** 3 / MSUN_PC3
    RR, ZZ = lv["RR"] * 2.6, lv["ZZ"] * 2.6
    box = (RR >= 7.2) & (RR <= 9.2) & (np.abs(ZZ) <= 1.0) & np.isfinite(rho)
    jz = np.argmin(np.abs(lv["z"] * 2.6 - 0.02))
    at_sun = float(np.interp(8.2 / 2.6, lv["R"], lv["rho"][:, jz])) * Md * MSUN / L ** 3 / MSUN_PC3
    im = np.unravel_index(np.argmin(np.where(box, rho, np.inf)), rho.shape)
    return {"min_box": float(rho[box].min()), "at_min_Rz_kpc": [float(RR[im]), float(ZZ[im])], "at_sun": at_sun,
            "n_box": int(box.sum()), "residual": lv["info"]["residual_rel"], "rss_GB": lv["rss_GB"],
            "time_s": lv["time_s"], "grid": [lv["nr"], lv["nz"]]}


# ====================================================================================================== slab (Part C)
def slab(N, gL, rho_d=0.0, grid="unaligned", theta0=0.0, switched=True, K=1.0, M=2.0):
    """staggered FV: nodes z_i = i/N carry s and gamma_i; faces z_{i+1/2} carry dP, q = d sigma/dz, rho_tau.
    Gamma^2 = max eig of (-rho) q = G^2 L^{-1} q on zero-mean q, L = K(M-1) + K Pi0 + D^T diag(gamma) D."""
    i = np.arange(N)
    zf = (i + 0.5) / N
    rho = -0.5 + np.cos(2 * np.pi * zf) + rho_d
    if not switched or MUTATE:
        on = np.ones(N)
    elif grid == "aligned":
        m = np.minimum(i, N - i)
        on = (6 * m < N).astype(float)
        on[6 * m == N] = theta0
    else:
        on = ((-0.5 + np.cos(2 * np.pi * i / N)) > 0).astype(float)
    gam = gL * on
    h = 1.0 / N
    E = np.eye(N)
    Dm = (E - np.roll(E, 1, axis=0)) / h
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        L = K * (M - 1) * E + (K / N) * np.ones((N, N)) + Dm.T @ (gam[:, None] * Dm)
    viol = int(np.sum((on > 0) & ((rho < 0) | (np.roll(rho, 1) < 0))))
    Q = sla.null_space(np.ones((1, N)))
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):   # spurious Accelerate matmul FP flags
        A = Q.T @ (-rho[:, None] * Q)
        X = sla.solve(L, Q, assume_a="pos")
        B = Q.T @ X
    if not (np.isfinite(A).all() and np.isfinite(B).all()):
        raise FloatingPointError("non-finite slab matrices")
    B = 0.5 * (B + B.T)
    A = 0.5 * (A + A.T)
    w = sla.eigh(A, B, eigvals_only=True, subset_by_index=[N - 2, N - 2])
    G = math.sqrt(max(float(w[0]), 0.0))
    neg = rho < 0
    fm = neg.mean()
    bound = math.sqrt(K * (M - 1 + fm) * (np.max(-rho[neg]) if neg.any() else 0.0))
    return G, viol, bound


def _slab_task(N, kw):
    return slab(N, **kw), rss_gb()


def ladder(Ns, **kw):
    """each level in its own spawned process (dense N x N algebra; keeps every process well under 1 GB)."""
    import concurrent.futures as cf
    import multiprocessing as mp
    out = []
    for N in Ns:
        with cf.ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn"), max_tasks_per_child=1) as ex:
            (G, v, b), r = ex.submit(_slab_task, N, kw).result()
        out.append({"N": N, "Gamma": G, "violations": v, "bound": b, "child_rss_GB": r})
    return out


# ====================================================================================================== main
# ====================================================================================================== child tasks
# (each runs in its own spawned process so every process stays well under 1 GB RSS)
def task_C():
    lines.clear()
    checks.clear()
    res.clear()
    log("")
    log("C: slab (1D periodic, no WKB): K = 1, M = 2, s0 = -0.5 + cos(2 pi z); staggered FV, Theta on nodes")
    C = {}
    C["C0_unswitched_1e-3"] = ladder((64, 128, 256, 512), gL=1e-3, switched=False)
    C["C0_gL0"] = ladder((64, 128, 256, 512), gL=0.0, switched=False)
    g1 = [r_["Gamma"] for r_ in C["C0_unswitched_1e-3"]]
    g0 = [r_["Gamma"] for r_ in C["C0_gL0"]]
    log(f"  C0 unswitched gamma_L 1e-3: {[round(v, 4) for v in g1]}; gamma_L 0: {[round(v, 6) for v in g0]}")
    c0_ok = (1.8 <= g1[3] / g1[2] <= 2.2) and g0[3] / g0[2] <= 1.01 and abs(g0[3] / 1.224744871391589 - 1) <= 0.01
    check("C0", c0_ok, f"ratio {g1[3] / g1[2]:.4f}; gamma_L=0: ratio {g0[3] / g0[2]:.6f}, {g0[3]:.6f} vs 1.224745",
          "[1.8, 2.2]; <= 1.01 and within 1 %")
    verdict_C = {}
    for cid, kw, Ns, target in (("C1", {"rho_d": 0.0, "grid": "aligned", "theta0": 0.0}, (96, 192, 384, 768, 1536),
                                 math.sqrt(1.5)),
                                ("C2", {"rho_d": 0.1, "grid": "unaligned"}, (64, 128, 256, 512, 1024), math.sqrt(1.4))):
        oks = []
        for gv in (1e-3, 1e-2):
            lad_ = ladder(Ns, gL=gv, **kw)
            C[f"{cid}_{gv}"] = lad_
            G_ = [r_["Gamma"] for r_ in lad_]
            ra = G_[-1] / G_[-2]
            okb = all(r_["Gamma"] <= r_["bound"] * (1 + 1e-9) for r_ in lad_)
            okc = all(r_["violations"] == 0 for r_ in lad_)
            oka = abs(ra - 1) <= 0.10
            oks.append((oka, okb, okc, ra))
            log(f"  {cid} gamma_L {gv:g}: Gamma {[round(v, 5) for v in G_]} (N {list(Ns)}); finest ratio {ra:.4f}; "
                f"bound {lad_[-1]['bound']:.5f}; violations {[r_['violations'] for r_ in lad_]}; "
                f"localised-mode value {target:.6f} (finest/target {G_[-1] / target:.4f})")
        ok_ = all(o[0] and o[1] and o[2] for o in oks)
        verdict_C[cid] = {"pass": ok_, "a": all(o[0] for o in oks), "b": all(o[1] for o in oks),
                          "c": all(o[2] for o in oks), "max_ratio": max(o[3] for o in oks)}
        check(cid, ok_, f"finest ratios {[round(o[3], 4) for o in oks]}; bound held {[o[1] for o in oks]}; "
              f"sign-consistent {[o[2] for o in oks]}", "(a) |ratio - 1| <= 0.10, (b) Gamma <= bound, (c) 0 violations")
    for gv in (1e-3, 1e-2):
        lad_ = ladder((64, 128, 256, 512, 1024, 2048), gL=gv, rho_d=0.0, grid="unaligned")
        C[f"C3a_{gv}"] = lad_
        G_ = [r_["Gamma"] for r_ in lad_]
        log(f"  C3a (diagnostic) zero dust, unaligned, gamma_L {gv:g}: Gamma {[round(x_, 4) for x_ in G_]}; ratios "
            f"{[round(G_[j + 1] / G_[j], 3) for j in range(len(G_) - 1)]}; slope {math.log(G_[-1] / G_[-2]) / math.log(2):.3f}; "
            f"violations {[r_['violations'] for r_ in lad_]}")
        lad_ = ladder((96, 192, 384, 768, 1536), gL=gv, rho_d=0.0, grid="aligned", theta0=1.0)
        C[f"C3b_{gv}"] = lad_
        G_ = [r_["Gamma"] for r_ in lad_]
        log(f"  C3b (diagnostic) aligned, Theta(0) := 1, gamma_L {gv:g}: Gamma {[round(x_, 4) for x_ in G_]}; ratios "
            f"{[round(G_[j + 1] / G_[j], 3) for j in range(len(G_) - 1)]}; slope {math.log(G_[-1] / G_[-2]) / math.log(2):.3f}; "
            f"violations {[r_['violations'] for r_ in lad_]}")
    res["C"] = C
    res["C_verdict"] = verdict_C
    return {"lines": list(lines), "checks": list(checks), "res": clean(dict(res)), "rss_GB": rss_gb()}


def task_D1():
    lines.clear()
    checks.clear()
    res.clear()
    d10, cl, umf = d10_inputs()
    UPSG, LG, chi2, L95 = make_stat(d10, umf)
    GR = S.Grid2D(nper=24, Nt=16)
    D1 = {}
    # (a) isolated: lemma
    da = []
    for y in (0.04, 3.0):
        for Lam in (0.5, 2.0, 8.0):
            su = SW(GR, y, 0.0, Lam, switched=False, isolated=True)
            su.solve()
            Du = su.divfield()
            ss_ = SW(GR, y, 0.0, Lam, sg=0.0, switched=True, isolated=True)
            ss_.solve(maxit=200)
            rfu, gru = su.field_monopole()
            rfs, grs = ss_.field_monopole()
            s2u = S.jeans(rfu, gru, [0.83, 1.0])[0]
            s2s = S.jeans(rfs, grs, [0.83, 1.0])[0]
            i_ = np.argmin(abs(np.log(rfu)))
            dd = max(float(np.max(abs(np.sqrt(s2s / s2u) - 1))), abs(grs[i_] / gru[i_] - 1))
            da.append({"y": y, "Lam": Lam, "minD": float(Du.min()), "maxD": float(Du.max()), "dev": dd,
                       "res_s": ss_.res})
    ok_a = all(r_["minD"] >= 0 for r_ in da) and max(r_["dev"] for r_ in da) <= 1e-8
    log(f"  D1(a) isolated (lemma): min D over cases {min(r_['minD'] for r_ in da):.3e}; max switched/unswitched dev "
        f"{max(r_['dev'] for r_ in da):.2e}")
    D1["a"] = da
    # (b), (c)
    y_, xe_, Lam_ = 0.04, 0.14, 1.0

    def sig_of(sv):
        rf, gr = sv.field_monopole()
        return math.sqrt(S.jeans(rf, gr, [1.0])[0][0]), float(np.interp(0.0, np.log(rf), gr))

    su = SW(GR, y_, xe_, Lam_, switched=False)
    su.solve()
    sp_hi = SW(GR, y_, xe_, Lam_, sg=1e6, switched=True)
    sp_hi.solve(maxit=200)
    sq0 = SW(GR, y_, xe_, 0.0, switched=False)
    sq0.solve()
    sp_lo = SW(GR, y_, xe_, Lam_, sg=-1e6, switched=True)
    sp_lo.solve(maxit=200)
    (su_s, su_g), (hi_s, hi_g), (q0_s, q0_g), (lo_s, lo_g) = sig_of(su), sig_of(sp_hi), sig_of(sq0), sig_of(sp_lo)
    dev_b = max(abs(hi_s / su_s - 1), abs(hi_g / su_g - 1))
    dev_c = max(abs(lo_s / q0_s - 1), abs(lo_g / q0_g - 1))
    log(f"  D1(b) s_g = +1e6 vs unswitched EFE: dev {dev_b:.2e}; D1(c) s_g = -1e6 vs AQUAL (Lam 0): dev {dev_c:.2e} "
        f"(unswitched vs AQUAL differ by {abs(su_s / q0_s - 1):.3e})")
    D1["b"], D1["c"] = dev_b, dev_c
    # (d) reproduce D10 tables and the central floor
    sigt = {k_: np.array(v_) for k_, v_ in d10["sigma_tables"].items()}
    cells = [("canonical", "E_mid", "Pal 4", 9), ("alt", "E_mid", "Pal 14", 9), ("canonical", "E_hi", "NGC 2419", 5)]
    devd = 0.0
    for foot, ek, name, iu in cells:
        g = cl[name]
        a = g["rhl"] * PC10
        xe = g_mw(g["RGC"], EBR[foot][ek], A0[foot]) / A0[foot]
        unit = math.sqrt(A0[foot] * a) / 1e3
        y = G10 * UPSG[iu] * g["LV"] * Msun10 / (a * a * A0[foot])
        sv = SW(GR, y, xe, 0.0, switched=False)
        U, _, _ = sv.solve()
        for il, Lst in enumerate(LG):
            sv = SW(GR, y, xe, Lst * PC10 / a, switched=False)
            U, _, _ = sv.solve(U0=U)
            if il in (8, 23):
                rf, gr = sv.field_monopole()
                sg_ = math.sqrt(S.jeans(rf, gr, [g["Rbin"]])[0][0]) * unit
                devd = max(devd, abs(sg_ / sigt[f"{foot}|{ek}|{name}"][0, iu, il + 1] - 1))
    tabs_u = {f: {n: sigt[f"{f}|E_mid|{n}"] for n in PRIMARY} for f in A0}
    l95u = {f: L95(chi2(tabs_u[f], "P1", 0.3, 0, PRIM3))[0] for f in A0}
    devL = max(abs(l95u[f] - D10_CENTRAL[f]) for f in A0)
    log(f"  D1(d) six D10 cells reproduced: max rel dev {devd:.2e}; central L*95 from D10's tables {l95u} "
        f"(max |dev| {devL:.1e} pc)")
    D1["d"] = {"sigma_dev": devd, "L95_reproduced": l95u}
    # (e) switched grid convergence
    de = []
    foot = "canonical"
    for name in PRIM3:
        g = cl[name]
        a = g["rhl"] * PC10
        Mb = EBR[foot]["E_mid"]
        xe = g_mw(g["RGC"], Mb, A0[foot]) / A0[foot]
        y = G10 * UPS_V * g["LV"] * Msun10 / (a * a * A0[foot])
        sg_, _ = s_gal(g["RGC"], Mb, A0[foot], a)
        Lam = LFLOOR[foot] * PC10 / a
        vals = []
        for grd in (GR, S.Grid2D(nper=48, Nt=32), S.Grid2D(nper=24, Nt=16, rout=1e5)):
            sv = SW(grd, y, xe, Lam, sg=sg_, switched=True)
            sv.solve(maxit=200)
            rf, gr = sv.field_monopole()
            vals.append((math.sqrt(S.jeans(rf, gr, [g["Rbin"]])[0][0]), sv.res))
        dd = max(abs(vals[1][0] / vals[0][0] - 1), abs(vals[2][0] / vals[0][0] - 1))
        de.append({"cluster": name, "sigma": [v_[0] for v_ in vals], "res": [v_[1] for v_ in vals], "dev": dd})
        log(f"  D1(e) {name}: switched sigma base/fine/far {[round(v_[0], 6) for v_ in vals]} residuals "
            f"{[f'{v_[1]:.0e}' for v_ in vals]} -> change {dd:.2e}")
    D1["e"] = de
    ok_d1 = (ok_a and dev_b <= 1e-8 and dev_c <= 1e-8 and devd <= 1e-8 and devL <= 1e-6
             and max(r_["dev"] for r_ in de) <= 5e-3)
    check("D1", ok_d1, f"(a) minD {min(r_['minD'] for r_ in da):.2e}, dev {max(r_['dev'] for r_ in da):.1e}; (b) {dev_b:.1e}; "
          f"(c) {dev_c:.1e}; (d) {devd:.1e}, {devL:.1e} pc; (e) {max(r_['dev'] for r_ in de):.1e}",
          "(a) minD >= 0 & <= 1e-8; (b), (c), (d) <= 1e-8 / 1e-6 pc; (e) <= 5e-3")
    res["D1"] = D1
    return {"lines": list(lines), "checks": list(checks), "res": clean(dict(res)), "rss_GB": rss_gb()}


def task_D2(gal):
    lines.clear()
    checks.clear()
    res.clear()
    h4j = json.load(open(H4JSON))
    GRs = S.Grid2D(nper=24, Nt=32)
    a_s = 0.1 * PC
    d2rows = []
    for foot in A0:
        Ls = [LFLOOR[foot], 24.0, 90.0]
        for xe in (1.15, 2.6):
            for Lp in Ls:
                y = GMSUN / (a_s ** 2 * A0[foot])
                sv = SW(GRs, y, xe, Lp * PC / a_s, switched=False)
                sv.solve()
                Dsun = sv.divfield() * A0[foot] / a_s / (4 * math.pi * G_SI) / MSUN_PC3
                negmax = float(max(0.0, -Dsun.min()))
                ik = int(np.argmin(Dsun))
                r_at = GRs.r2d[ik] * 0.1
                t_at = math.degrees(GRs.t2d[ik])
                rneg = GRs.r2d[Dsun < 0] * 0.1
                margin = gal[foot]["min_box"] / negmax if negmax > 0 else float("inf")
                tot = gal[foot]["min_box"] - negmax
                d2rows.append({"foot": foot, "x_e": xe, "Lstar_pc": Lp, "max_neg_lobe_Msun_pc3": negmax,
                               "at_r_pc": r_at, "at_theta_deg": t_at,
                               "neg_r_range_pc": [float(rneg.min()), float(rneg.max())] if len(rneg) else None,
                               "max_pos_Msun_pc3": float(Dsun.max()), "rho_gal_min": gal[foot]["min_box"],
                               "min_total": tot, "margin": margin, "residual": sv.res})
                log(f"    D2 {foot:9s} x_e {xe:4.2f} L* {Lp:5.1f} pc: Sun's deepest lobe {-negmax:.3e} Msun/pc^3 at "
                    f"r {r_at:.1f} pc, theta {t_at:.0f} deg (negative for r in "
                    f"{[round(v_, 1) for v_ in d2rows[-1]['neg_r_range_pc']] if len(rneg) else 'none'} pc); total min "
                    f"{tot:.4f}; margin {margin:.3g}")
    ok_d2 = all(r_["min_total"] > 0 and r_["margin"] >= 10 for r_ in d2rows) and all(r_["residual"] < 1e-8 for r_ in d2rows)
    h4c3min = min(r_["DP_Msun_pc3"] for r_ in h4j["C3"])
    e01 = [k_ for k_ in h4j["regions"] if k_.startswith("S5a_MW_disc") and k_.endswith("e0.01")]
    lobe_R = {k_: h4j["regions"][k_]["f0"]["fine"]["box"].get("R_range_m") for k_ in e01}
    lobe_in = min(v_[0] for v_ in lobe_R.values() if v_) / KPC if any(lobe_R.values()) else float("nan")
    far = (min(LFLOOR.values()) * PC / (max(lobe_in, 40.0) * KPC)) ** 2
    log(f"  D2 reported: H4 C3 near-zone minimum {h4c3min:.4f} Msun/pc^3; nearest MW external-field lobe (H4 S5a e0.01) "
        f"inner R {lobe_in:.1f} kpc -> far-region stiffness effect ~ (L*/R)^2 = {far:.1e} (estimate)")
    check("D2", ok_d2, f"min total D.P {min(r_['min_total'] for r_ in d2rows):.4f} Msun/pc^3; min margin "
          f"{min(r_['margin'] for r_ in d2rows):.3g} over {len(d2rows)} cells", "> 0 and margin >= 10 (all cells)")
    res["D2"] = {"galactic": gal, "rows": d2rows, "H4_C3_min": h4c3min, "far_effect_estimate": far, "lobe_inner_kpc": lobe_in}
    return {"lines": list(lines), "checks": list(checks), "res": clean(dict(res)), "rss_GB": rss_gb()}


def task_D3():
    lines.clear()
    checks.clear()
    res.clear()
    p3 = json.load(open(P3JSON))
    gh = [r_.get("G_hat") for r_ in p3["E4"].values()]
    ok_p3 = all(g_ is not None and g_ > 0 for g_ in gh) and len(p3["E4_G_nonpositive"]) == 0
    sph = []
    for y in (1e-3, 0.04, 3.0, 300.0):
        for Lam in (0.1, 1.0, 10.0):
            rs, gt, stt = S.iso_1d(y, Lam)
            p_ = gt - S.plummer_gN(rs, y)
            s_ = np.gradient(rs ** 2 * p_, rs) / rs ** 2
            sph.append({"y": y, "Lam": Lam, "min_over_max": float(s_.min() / s_.max()), "bvp_status": int(stt)})
    ok_sph = all(r_["min_over_max"] >= -1e-6 and r_["bvp_status"] == 0 for r_ in sph)
    log(f"  D3: P3 E4 rows with G_hat > 0: {sum(1 for g_ in gh if g_ and g_ > 0)}/{len(gh)}; E4_G_nonpositive "
        f"{p3['E4_G_nonpositive']}; isolated spherical screened min s / max s over 12 cases "
        f"{min(r_['min_over_max'] for r_ in sph):.2e} (bvp status {sorted(set(r_['bvp_status'] for r_ in sph))})")
    check("D3", ok_p3 and ok_sph, f"P3 rows positive {ok_p3}; spherical min/max {min(r_['min_over_max'] for r_ in sph):.2e}",
          "all G_hat > 0; s >= -1e-6 max s, BVPs converged")
    res["D3"] = {"p3_rows": len(gh), "spherical": sph}
    return {"lines": list(lines), "checks": list(checks), "res": clean(dict(res)), "rss_GB": rss_gb()}


def task_D4maps(foot_):
    lines.clear()
    checks.clear()
    res.clear()
    d10, cl, umf = d10_inputs()
    GR = S.Grid2D(nper=24, Nt=16)
    maps = []
    for foot in (foot_,):
        Mb = EBR[foot]["E_mid"]
        for name in PRIMARY:
            g = cl[name]
            a = g["rhl"] * PC10
            xe = g_mw(g["RGC"], Mb, A0[foot]) / A0[foot]
            y = G10 * UPS_V * g["LV"] * Msun10 / (a * a * A0[foot])
            sg_, rph = s_gal(g["RGC"], Mb, A0[foot], a)
            for Lp in (D10_CENTRAL[foot], 24.0, 90.0):
                su = SW(GR, y, xe, Lp * PC10 / a, switched=False)
                su.solve()
                Dt = su.divfield() + sg_
                ss_ = SW(GR, y, xe, Lp * PC10 / a, sg=sg_, switched=True)
                ss_.solve(U0=su.U, maxit=200)
                rf, gr = su.field_monopole()
                s_u = math.sqrt(S.jeans(rf, gr, [g["Rbin"]])[0][0])
                rf, gr = ss_.field_monopole()
                s_s = math.sqrt(S.jeans(rf, gr, [g["Rbin"]])[0][0])
                neg = Dt < 0
                ik = int(np.argmin(Dt))
                rr = GR.r2d * g["rhl"]
                inner = rr <= Lp
                conv = 1.0 / (a * 4 * math.pi * G10) * A0[foot] / (Msun10 / PC10 ** 3)
                maps.append({"foot": foot, "cluster": name, "Lstar_pc": Lp, "x_e": xe, "s_g": sg_,
                             "rho_gal_Msun_pc3": rph / (Msun10 / PC10 ** 3),
                             "min_total_Msun_pc3": float(Dt.min()) * conv, "at_r_pc": float(rr[ik]),
                             "at_theta_deg": math.degrees(GR.t2d[ik]),
                             "neg_r_range_pc": [float(rr[neg].min()), float(rr[neg].max())] if neg.any() else None,
                             "neg_cell_fraction_r<10a": float((neg & (GR.r2d < 10)).sum() / max(1, (GR.r2d < 10).sum())),
                             "min_total_inside_Lstar": float(Dt[inner].min()) * conv if inner.any() else None,
                             "sigma_unswitched": s_u, "sigma_switched": s_s, "dsigma_rel": s_s / s_u - 1,
                             "res_switched": ss_.res})
                m_ = maps[-1]
                log(f"    D4 map {foot:9s} {name:8s} L* {Lp:5.1f} pc (x_e {xe:.3f}, rho_gal {m_['rho_gal_Msun_pc3']:.1e}): "
                    f"min D.P {m_['min_total_Msun_pc3']:.2e} Msun/pc^3 at r {m_['at_r_pc']:.0f} pc, "
                    f"theta {m_['at_theta_deg']:.0f} deg; D.P < 0 for r in "
                    f"{[round(v_) for v_ in m_['neg_r_range_pc']] if m_['neg_r_range_pc'] else 'none'} pc; min inside L* "
                    f"{m_['min_total_inside_Lstar']:.2e}; sigma_p switched/unswitched - 1 = {m_['dsigma_rel']:+.2e}")
    res["D4_maps"] = maps
    return {"lines": list(lines), "checks": list(checks), "res": clean(dict(res)), "rss_GB": rss_gb()}


def run_child(fn, *args):
    import concurrent.futures as cf
    import multiprocessing as mp
    with cf.ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn"), max_tasks_per_child=1) as ex:
        out = ex.submit(fn, *args).result()
    lines.extend(out["lines"])
    checks.extend(out["checks"])
    return out


def main():
    import sympy as sp
    from sympy.calculus.euler import euler_equations
    import concurrent.futures as cf
    import multiprocessing as mp
    T0 = time.time()
    log("X3_switched_stiffness: -(gamma_L/2)[max(D.P,0)]^2 in v3 -- well-posed where rho_tau < 0? statics unchanged?")
    log(f"mutate = {MUTATE} (Theta = 1 everywhere: the switch removed); kappa = 1/2 FITTED; footings never pooled")
    h4j = json.load(open(H4JSON))

    # ============================================================================================ PART A (H4, read-only)
    log("")
    log("A: reproduction of H4 with H4's own code (source executed verbatim, nothing edited)")
    src = open(H4PY).read()
    tree = ast.parse(src)
    main_fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    msrc = ast.get_source_segment(src, main_fn)
    ml = msrc.splitlines()
    sym_line = next(l_ for l_ in ml if l_.strip().startswith("K, gL, muK, a0s = sp.symbols("))
    i0 = next(i for i, l_ in enumerate(ml) if l_.strip().startswith("# A4: PN linear system"))
    i1 = next(i for i, l_ in enumerate(ml) if l_.strip().startswith("# A5: J_x masses"))
    b1l = [l_ for l_ in ml if l_.strip().startswith(("w2 = sol[0]", "lim_uv = sp.simplify(", "lim_b = sp.simplify("))]
    block = textwrap.dedent("\n".join([sym_line] + ml[i0:i1] + b1l))
    h4chk = {}
    ns = {"sp": sp, "SGN": 1, "log": lambda *a_, **k_: None, "res": {},
          "check": lambda cid, ok, v, t: h4chk.__setitem__(cid, bool(ok))}
    exec(compile(block, H4PY, "exec"), ns)
    smap = {"K": ns["K"], "gamma_L": ns["gL"], "mu_K": ns["muK"], "rho_0": ns["r0"], "M_L": ns["ML"], "M_T": ns["MT"],
            "theta": ns["th"]}
    uv_json = sp.sympify(h4j["B1"]["uv_coefficient"], locals=smap)
    b_json = sp.sympify(h4j["B1"]["bounded_limit_gammaL0"], locals=smap)
    r_uv = sp.simplify(ns["lim_uv"] - uv_json)
    r_b = sp.simplify(ns["lim_b"] - b_json)
    r_w2 = sp.simplify(ns["sol"][0] - ns["w2_expected"])
    log(f"  A0a: H4 A4 block: H4's own A4 check = {h4chk.get('A4')}; omega^2 - rho_tau(k^2/chi - K) = {r_w2}; "
        f"UV coefficient = {ns['lim_uv']} (json residual {r_uv}); gamma_L = 0 limit = {ns['lim_b']} (json residual {r_b})")
    check("A0a", h4chk.get("A4") and r_w2 == 0 and r_uv == 0 and r_b == 0,
          f"H4 A4 {h4chk.get('A4')}; dispersion residual {r_w2}; B1 json residuals {r_uv}, {r_b}",
          "H4's block reproduces its own A4 and B1 json strings (residuals 0)")
    res["A0a"] = {"omega2": str(ns["sol"][0]), "uv": str(ns["lim_uv"]), "bounded": str(ns["lim_b"])}
    gfn = next(n for n in ast.walk(main_fn) if isinstance(n, ast.FunctionDef) and n.name == "gmax")
    gns = {"np": np, "math": math, "SGN": 1}
    exec(compile(textwrap.dedent(ast.get_source_segment(src, gfn, padded=True)), H4PY, "exec"), gns)
    lad = {str(gv): [gns["gmax"](N, gv) for N in (64, 128, 256, 512)] for gv in (1e-3, 0.0)}
    dev = max(abs(a_ / b_ - 1) for k_ in ("0.001", "0.0") for a_, b_ in zip(lad[k_], h4j["B2"]["ladder"][k_]))
    r_grow = lad["0.001"][3] / lad["0.001"][2]
    pred = h4j["B2"]["prediction_bounded"]
    log(f"  A0b: H4 gmax ladder gamma_L = 1e-3: {[round(v, 4) for v in lad['0.001']]}; gamma_L = 0: "
        f"{[round(v, 6) for v in lad['0.0']]}; max rel. dev. from H4 json {dev:.1e}; ratio {r_grow:.4f}")
    check("A0b", dev <= 1e-12 and 1.8 <= r_grow <= 2.2 and abs(lad["0.0"][3] / pred - 1) <= 0.01,
          f"dev {dev:.1e}; Gamma(512)/Gamma(256) = {r_grow:.4f}; gamma_L=0: {lad['0.0'][3]:.6f} vs {pred:.6f}",
          "<= 1e-12; [1.8, 2.2]; within 1 %")
    res["A0b"] = {"ladder": lad, "max_rel_dev": dev}

    # ============================================================================================ PART B (sympy)
    log("")
    log("B: the switched operator (sympy)")
    k, om, r0, th, ML, MT = ns["k"], ns["om"], ns["r0"], ns["th"], ns["ML"], ns["MT"]
    K, gL, muK = ns["K"], ns["gL"], ns["muK"]
    dphi, dsig, dXi, drho = sp.symbols("dphi dsigma dXi drho")
    dP = sp.symbols("dP0:3")
    kh = sp.Matrix([0, 0, 1])
    Ph = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hm = K * (MT * sp.eye(3) + (ML - MT) * Ph * Ph.T)
    dPv = sp.Matrix(dP)
    W2 = sp.Symbol("W2")

    def disp_switched(theta_val):
        """own linear system (Poisson, rho_tau = div P - mu^2 Xi/K, continuity, Bernoulli, P equation with stiffness
        Theta gamma_L); returns omega^2."""
        Peq = sp.I * k * kh * dXi - theta_val * gL * k ** 2 * kh * (kh.dot(dPv)) - Hm * dPv
        eqs_ = [-k ** 2 * dphi - K * drho, drho - (sp.I * k * kh.dot(dPv) - muK ** 2 * dXi / K),
                -sp.I * om * drho + r0 * k ** 2 * dsig, dXi - (dphi + sp.I * om * dsig)] + list(Peq)
        Msys = sp.linear_eq_to_matrix(eqs_, [dphi, dsig, dXi, drho] + list(dP))[0]
        det = sp.factor(sp.simplify(Msys.det()))
        sol_ = sp.solve(sp.Eq(det.subs(om, sp.sqrt(W2)), 0), W2)
        return sp.simplify(sol_[0]) if len(sol_) == 1 else None

    wP = disp_switched(1)
    wN = disp_switched(1 if MUTATE else 0)
    Mth = 1 / (sp.cos(th) ** 2 / ML + sp.sin(th) ** 2 / MT)
    rP = sp.simplify(wP - ns["w2_expected"]) if wP is not None else "no root"
    limN_k2 = sp.simplify(sp.limit(wN / k ** 2, k, sp.oo))
    limN = sp.simplify(sp.limit(wN, k, sp.oo))
    rN = sp.simplify(limN - K * r0 * (Mth - 1))
    wP0 = sp.simplify(wP.subs(muK, 0) - K * r0 * (Mth - 1 + gL * k ** 2 / K))
    f_M = sp.lambdify((ML, MT, th), Mth - 1, "numpy")
    rng = np.random.default_rng(7)
    xs_ = 10 ** rng.uniform(-4, 4, 20000)
    Mmin = float(np.min(f_M((1 + xs_) ** 2, 1 + xs_, rng.uniform(0, math.pi, 20000))))
    log(f"  B1-S: D.P0 > 0 side: omega^2 - H4's = {rP}; D.P0 < 0 side: omega^2 = {wN}")
    log(f"        D.P0 < 0: lim omega^2/k^2 = {limN_k2}; lim omega^2 = {limN} (minus K rho (M_theta - 1): {rN}); "
        f"mu_K = 0, D.P0 > 0: omega^2 - K rho (M_theta - 1 + gL k^2/K) = {wP0}; min(M_theta - 1) over 2e4 J_x samples "
        f"{Mmin:.3e}")
    ok_b1 = rP == 0 and limN_k2 == 0 and rN == 0 and wP0 == 0 and Mmin >= 0
    check("B1-S", ok_b1, f"P side residual {rP}; N side UV omega^2/k^2 -> {limN_k2}, omega^2 -> K rho (M-1) "
          f"(residual {rN}); mu=0 P side residual {wP0}, M_theta - 1 >= {Mmin:.2e}",
          "P side = H4; N side finite UV limit K rho_tau (M_theta - 1); P side omega^2 >= 0 for rho_tau >= 0")
    res["B1S"] = {"omega2_P": str(wP), "omega2_N": str(wN), "N_uv_over_k2": str(limN_k2), "N_uv": str(limN)}

    # B2-S nonlinear principal part, 1D
    t, z = sp.symbols("t z", real=True)
    mu1, rd = sp.symbols("mu rho_d", nonnegative=True)
    phi = sp.Function("phi")(t, z)
    sig = sp.Function("sigma")(t, z)
    Pz = sp.Function("P")(t, z)
    rhom = sp.Function("rho_m")(z)
    Ff = sp.Function("F")
    Wf = sp.Function("W")
    Xi = phi - sp.diff(sig, t) + sp.diff(sig, z) ** 2 / 2
    s_ = sp.diff(Pz, z)
    L1 = (-sp.diff(phi, z) ** 2 / (2 * K) - rhom * phi + Pz * sp.diff(Xi, z) - Wf(K * Pz) - gL / 2 * Ff(s_)
          + mu1 ** 2 * Xi ** 2 / (2 * K))
    eqs = euler_equations(L1, [phi, sig, Pz], [t, z])
    rt = s_ - mu1 ** 2 * Xi / K
    v = -sp.diff(sig, z)
    cont = sp.diff(rt, t) + sp.diff(rt * v, z)
    r_cont = sp.simplify(sp.expand(eqs[1].lhs + cont))
    xs = sp.Symbol("xs")
    hP = sp.diff(Xi, z) - K * sp.Subs(sp.diff(Wf(xs), xs), xs, K * Pz).doit() + sp.diff(
        gL / 2 * sp.Subs(sp.diff(Ff(xs), xs), xs, s_).doit(), z)
    r_P = min((sp.simplify(sp.expand((eqs[2].lhs - sg_ * hP).doit())) for sg_ in (1, -1)), key=lambda e: len(str(e)))
    r_eu = sp.simplify(sp.expand(sp.diff(v, t) + v * sp.diff(v, z) - (sp.diff(Xi, z) - sp.diff(phi, z))))
    s0, kk_, oo, h1 = sp.symbols("s_0 k omega h_1")
    Msym = sp.Matrix([[-sp.I * oo, sp.I * kk_ * (s0 + rd)], [sp.I * kk_ * h1, -sp.I * oo]])
    w2s = sp.solve(sp.Eq(Msym.det(), 0), oo)
    c2gen = sp.simplify(w2s[0] ** 2 / kk_ ** 2)
    ss = sp.Symbol("s", real=True)
    sp_, sn_, eps = sp.symbols("s_p s_n epsilon", positive=True)
    F_sw = (ss ** 2) if MUTATE else sp.Piecewise((ss ** 2, ss > 0), (0, True))

    def c2_of(Fexpr, s0val, rdval):
        return sp.simplify(c2gen.subs(h1, gL / 2 * sp.diff(Fexpr, ss, 2)).subs(ss, s0val).subs(s0, s0val).subs(rd, rdval))

    c2_sw_pos = c2_of(F_sw, sp_, rd)
    c2_sw_neg = c2_of(F_sw, -sn_, rd)
    c2_v3 = c2_of(ss ** 2, -(rd + sn_), rd)
    Feps = ((ss + sp.sqrt(ss ** 2 + eps ** 2)) / 2) ** 2
    c2_eps = c2_of(Feps, -eps, 0)
    eps_vals = [float(c2_eps.subs({eps: e_, gL: 1})) for e_ in (1e-6, 1e-3, 1.0, 1e3)]
    sw_ok = bool(sp.ask(sp.Q.nonnegative(c2_sw_pos), sp.Q.nonnegative(rd))) if c2_sw_pos.is_nonnegative is None \
        else bool(c2_sw_pos.is_nonnegative)
    sw_ok_neg = (c2_sw_neg == 0) or bool(c2_sw_neg.is_nonnegative)
    v3_neg = bool(c2_v3.is_negative)
    eps_neg = all(e_ < 0 for e_ in eps_vals)
    log(f"  B2-S: sigma-EL + continuity(rho_tau = s - mu^2 Xi/K) = {r_cont}; P-EL - [Xi_z - K W'(KP) + d_z((gL/2)F'(s))] "
        f"= {r_P}; D_t v - (Xi_z - phi_z) = {r_eu}; principal symbol omega^2/k^2 = {c2gen}")
    log(f"        c^2 switch: s0 > 0 -> {c2_sw_pos}; s0 < 0 -> {c2_sw_neg}; v3 (F = s^2) at s0 = -(rho_d + s_n): {c2_v3}; "
        f"eps-smoothed max at s0 = -eps, rho_d = 0: {sp.simplify(c2_eps)} (values at eps = 1e-6..1e3, gL = 1: "
        f"{[f'{e_:.3e}' for e_ in eps_vals]})")
    check("B2-S", r_cont == 0 and r_P == 0 and r_eu == 0 and sw_ok and sw_ok_neg and v3_neg and eps_neg,
          f"identities {r_cont}/{r_P}/{r_eu}; switch c^2 >= 0 both branches: {sw_ok and sw_ok_neg}; v3 c^2 < 0: {v3_neg}; "
          f"eps-smoothing c^2 < 0: {eps_neg}",
          "switch: c^2 = gL (s0 + rho_d) Theta(s0) >= 0; v3 and every smoothing: c^2 < 0 somewhere")
    res["B2S"] = {"c2_general": str(c2gen), "c2_switch_pos": str(c2_sw_pos), "c2_switch_neg": str(c2_sw_neg),
                  "c2_v3": str(c2_v3), "c2_eps": str(sp.simplify(c2_eps)), "c2_eps_values": eps_vals}

    # B3-S interface / convexity / scalar reduction
    f_ = F_sw
    f1 = sp.diff(f_, ss)
    lim_p, lim_m = sp.limit(f1, ss, 0, "+"), sp.limit(f1, ss, 0, "-")
    f2p, f2m = sp.diff(f_, ss, 2).subs(ss, sp_), sp.diff(f_, ss, 2).subs(ss, -sn_)
    gap = ss ** 2 - f_
    gap_pos, gap_neg = sp.simplify(gap.subs(ss, sp_)), sp.simplify(gap.subs(ss, -sn_))
    v1_, v2_, v3_ = sp.symbols("v1 v2 v3", positive=True)
    vv = sp.Matrix([v1_, v2_, v3_])
    vm = sp.sqrt(v1_ ** 2 + v2_ ** 2 + v3_ ** 2)
    pp = vv / (1 + vm)
    pm = sp.sqrt(sum(c_ ** 2 for c_ in pp))
    r_h = max(abs(float(sp.N(c_.subs({v1_: 0.3, v2_: 1.7, v3_: 0.05})))) for c_ in (pp / (1 - pm) - vv))
    ok_b3 = (lim_p == 0 and lim_m == 0 and f2p >= 0 and f2m >= 0 and gap_pos == 0 and bool(gap_neg.is_positive)
             and r_h < 1e-14)
    log(f"  B3-S: f'(0+) = {lim_p}, f'(0-) = {lim_m} (C^1); f'' = {f2p} / {f2m} (convex); s^2 - f = {gap_pos} (s > 0), "
        f"{gap_neg} (s < 0); h(p(grad chi)) - grad chi = {r_h:.1e} with chi = Phi + (L*^2/2)(div p)_+")
    check("B3-S", ok_b3, f"C1 {lim_p}/{lim_m}; f'' {f2p}/{f2m}; E_s - E_u = 0 iff s >= 0: {gap_pos}, {gap_neg}; "
          f"reduction {r_h:.1e}", "C^1, convex, E_switched <= E_v3 with equality iff D.P >= 0; scalar reduction exact")
    log(f"A, B done ({time.time() - T0:.0f} s)")

    # ============================================================================================ PART C (slab, child)
    oc = run_child(task_C)
    res.update({k_: v_ for k_, v_ in oc["res"].items()})
    verdict_C = oc["res"]["C_verdict"]
    log(f"C done ({time.time() - T0:.0f} s; C child RSS {oc['rss_GB']:.2f} GB, worst slab-level child RSS "
        f"{max(r_['child_rss_GB'] for lad_ in oc['res']['C'].values() for r_ in lad_):.2f} GB)")

    # ============================================================================================ PART D (statics)
    log("")
    log("D: statics")
    o1 = run_child(task_D1)
    res.update(o1["res"])
    log(f"  (D1 child RSS {o1['rss_GB']:.2f} GB)")
    h4j = json.load(open(H4JSON))
    # ---- D2 Solar System (C6)
    ctx = mp.get_context("spawn")
    gal = {}
    with cf.ProcessPoolExecutor(max_workers=1, mp_context=ctx, max_tasks_per_child=1) as ex:
        for foot in A0:
            gal[foot] = ex.submit(h4_disc_worker, foot).result()
            log(f"  D2 Galactic phantom (H4 S5a solver, {foot}): at the Sun {gal[foot]['at_sun']:.4f} (H4 json "
                f"{[r_['rho_gal_phantom'] for r_ in h4j['C3'] if r_['foot'] == foot][0]:.4f}); min over R 7.2-9.2 kpc, |z| <= 1 kpc: "
                f"{gal[foot]['min_box']:.4f} Msun/pc^3 at (R, z) = {[round(v_, 3) for v_ in gal[foot]['at_min_Rz_kpc']]} kpc "
                f"({gal[foot]['n_box']} nodes; residual {gal[foot]['residual']:.1e}; child RSS {gal[foot]['rss_GB']:.2f} GB, "
                f"{gal[foot]['time_s']:.0f} s)")
    o2 = run_child(task_D2, gal)
    res.update(o2["res"])
    log(f"  (D2 child RSS {o2['rss_GB']:.2f} GB)")
    o3 = run_child(task_D3)
    res.update(o3["res"])
    p3 = json.load(open(P3JSON))
    maps = []
    for foot in A0:
        o4 = run_child(task_D4maps, foot)
        maps += o4["res"]["D4_maps"]
        log(f"  (D4 maps {foot} child RSS {o4['rss_GB']:.2f} GB)")
    res["D4_maps"] = maps
    d10, cl, umf = d10_inputs()
    UPSG, LG, chi2, L95 = make_stat(d10, umf)
    sigt = {k_: np.array(v_) for k_, v_ in d10["sigma_tables"].items()}

    # ---- D4 aggregation of the production tables
    D4 = {"maps": "see D4_maps"}
    ok_d4 = False
    d4_status = "UNDECIDED"
    if MUTATE:
        log("  D4 production aggregation skipped in MUTATE (the mutated switch is v3 itself; production not rerun)")
        d4_status = "SKIPPED (MUTATE)"
    else:
        tabs = {}
        missing = [b_ for b_ in BRACKETS if not os.path.exists(os.path.join(HERE, f"x3_d10_tables_{b_}.json"))]
        prod = {}
        for b_ in BRACKETS:
            fn = os.path.join(HERE, f"x3_d10_tables_{b_}.json")
            if os.path.exists(fn):
                prod[b_] = json.load(open(fn))
        complete = (not missing) and all(prod[b_].get("complete") for b_ in BRACKETS)
        if not complete:
            log(f"  D4 production incomplete (missing/incomplete brackets: {missing or [b_ for b_ in prod if not prod[b_].get('complete')]})")
        else:
            nsol = sum(v_["info"]["n_solves"] for b_ in BRACKETS for v_ in prod[b_]["blocks"].values())
            nbad = sum(v_["info"]["n_unconverged"] for b_ in BRACKETS for v_ in prod[b_]["blocks"].values())
            worst = max(v_["info"]["worst_residual"] for b_ in BRACKETS for v_ in prod[b_]["blocks"].values())
            for b_ in BRACKETS:
                for key, v_ in prod[b_]["blocks"].items():
                    foot, name = key.split("|")
                    tabs[(foot, b_, name)] = np.array(v_["sig"])
            cells_out = {}
            band_ok = True
            for foot in A0:
                for pk in ("P1", "P2", "P3"):
                    for ek in BRACKETS:
                        ts = {n: tabs[(foot, ek, n)] for n in PRIMARY}
                        tu = {n: sigt[f"{foot}|{ek}|{n}"] for n in PRIMARY}
                        cs = chi2(ts, pk, 0.3, 0, PRIM3)
                        cu = chi2(tu, pk, 0.3, 0, PRIM3)
                        ls, ds = L95(cs)
                        lu, du = L95(cu)
                        ref = d10["band_cells"][f"{foot}|{pk}|{ek}"]["L95"]
                        rel = ls / lu - 1 if lu > 0 else float("nan")
                        okc = abs(ls - lu) <= max(0.02 * lu, 0.2)
                        band_ok &= okc
                        cells_out[f"{foot}|{pk}|{ek}"] = {"L95_switched": ls, "L95_D10": lu, "D10_json": ref, "rel": rel,
                                                         "dchi2_AQUAL_switched": float(ds[0]), "dchi2_Newton_switched": float(ds[-1]),
                                                         "ok": okc}
                        log(f"    D4 [{foot:9s} {pk} {ek:5s}] L*95 switched {ls:7.3f} pc vs D10 {lu:7.3f} (json {ref:7.3f}): "
                            f"{rel * 100:+.3f} %; dchi2 AQUAL {ds[0]:.2f}, Newton {ds[-1]:.2f}")
            cen = {f: cells_out[f"{f}|P1|E_mid"] for f in A0}
            ok_cen = all(abs(cen[f]["rel"]) <= 0.02 for f in A0)
            sigd = []
            il_ok = [il for il, Lst in enumerate(LG) if 20.0 <= Lst <= 90.0]
            for foot in A0:
                for name in PRIM3:
                    ts = tabs[(foot, "E_mid", name)][0, 9]
                    tu = sigt[f"{foot}|E_mid|{name}"][0, 9]
                    for il in il_ok:
                        sigd.append(abs(ts[il + 1] / tu[il + 1] - 1))
            ok_sig = max(sigd) <= 0.01
            conv_ok = nbad <= 0.01 * nsol
            # s_g = 0 variant (central, E_mid, primary three)
            sg0 = {}
            for foot in A0:
                t0_ = {n: np.array(prod["E_mid"]["blocks_sg0"][f"{foot}|{n}"]["sig"]) for n in PRIM3}
                sg0[foot] = L95(chi2(t0_, "P1", 0.3, 0, PRIM3))[0]
            # D10 verdict lines re-read
            vre = {}
            for foot in A0:
                cs_ = [cells_out[f"{foot}|{pk}|{ek}"]["L95_switched"] for pk in ("P1", "P2", "P3") for ek in BRACKETS]
                lo, hi = min(cs_), max(cs_)
                if lo > 90:
                    win = "ABOVE"
                elif lo >= 20 and hi <= 90:
                    win = "INSIDE"
                elif hi < 20:
                    win = "BELOW"
                else:
                    win = "STRADDLES " + ("the 90 pc edge" if hi > 90 and lo >= 20 else
                                          ("the 20 pc edge" if lo < 20 and hi <= 90 else "both edges"))
                refc = {"canonical": 23.96, "alt": 24.72}[foot]
                mv = "FLOOR MOVES" if abs(cen[foot]["L95_switched"] / refc - 1) > 0.10 else "FLOOR HOLDS"
                aq = all(cells_out[f"{foot}|{pk}|{ek}"]["dchi2_AQUAL_switched"] > 3.84 for pk in ("P1", "P2", "P3") for ek in BRACKETS)
                vre[foot] = {"central": cen[foot]["L95_switched"], "band": [lo, hi], "window": win, "move": mv,
                             "AQUAL_excluded_all_cells": aq}
                log(f"  D4 [{foot}] switched: central {cen[foot]['L95_switched']:.3f} pc (D10 {cen[foot]['L95_D10']:.3f}, "
                    f"{cen[foot]['rel'] * 100:+.3f} %); band {lo:.2f}-{hi:.2f}; {win}; {mv}; AQUAL excluded all cells {aq}; "
                    f"s_g = 0 variant central {sg0[foot]:.3f} pc")
            log(f"  D4 production: {nsol} switched-chain solves, unconverged {nbad}, worst residual {worst:.1e}; "
                f"max |dsigma/sigma| at Ups 1.67, E_mid, L* 20-90 pc, three primary clusters {max(sigd):.2e}")
            ok_d4 = ok_cen and band_ok and ok_sig and conv_ok
            d4_status = "PASS" if ok_d4 else ("UNDECIDED" if not conv_ok else "CHANGE")
            D4.update({"cells": cells_out, "central_ok": ok_cen, "band_ok": band_ok, "max_dsigma": max(sigd),
                       "sigma_ok": ok_sig, "n_solves": nsol, "n_unconverged": nbad, "worst_residual": worst,
                       "converged_ok": conv_ok, "sg0_central": sg0, "D10_lines_switched": vre})
        check("D4", ok_d4, f"status {d4_status}" + (f"; central {[round(D4['cells'][f'{f}|P1|E_mid']['rel'] * 100, 3) for f in A0]} %; "
                                                     f"band ok {D4['band_ok']}; max dsigma {D4['max_dsigma']:.2e}; "
                                                     f"unconverged {D4['n_unconverged']}/{D4['n_solves']}" if "cells" in D4 else ""),
              "central <= 2 %, band <= max(2 %, 0.2 pc), sigma <= 1 %, >= 99 % converged")
    res["D4"] = D4
    res["D4_status"] = d4_status
    log(f"D done ({time.time() - T0:.0f} s)")

    # ============================================================================================ PART E (secondary)
    log("")
    log("E: secondary (report only)")
    row = p3["E4"]["planets (1 AU)|canonical|24pc"]
    rowg = p3["E4"]["galaxy (1 kpc; phantom 0.01 Msun/pc^3, ILLUSTRATIVE)|canonical|24pc"]

    def lam_V1_V4(zh, zPh, gh_):
        c_ = math.sqrt(gh_ / zh)
        L1_ = math.sqrt(zh ** 1.5 * c_ ** 3.5 / (zPh * 0.5 * SQK))
        l4 = zPh * 0.25 / 2
        L4_ = (zh ** 2 * c_ ** 7 / (l4 * SQK ** 2)) ** 0.25
        return c_, L1_, L4_

    e0dev = 0.0
    for rr_ in (row, rowg):
        c_, L1_, L4_ = lam_V1_V4(rr_["Z_hat"], rr_["ZP_hat"], rr_["G_hat"])
        e0dev = max(e0dev, abs(c_ / rr_["c_pi"] - 1), abs(L1_ / rr_["vertices"]["V1 pidot (grad pi)^2 [clock]"]["Lambda_m-1"] - 1),
                    abs(L4_ / rr_["vertices"]["V4 (grad pi)^4 [clock, quartic]"]["Lambda_m-1"] - 1))
    check("E0", e0dev <= 1e-9, f"max rel dev {e0dev:.1e}", "<= 1e-9 (P3's A69 estimate reproduced)")
    E1 = []
    regs = h4j["efolds"]
    for key in [k_ for k_ in regs if f"L*{LFLOOR['canonical']}" in k_ or f"L*{LFLOOR['alt']}" in k_]:
        nm, foot = key.split("|")[0], key.split("|")[1]
        ekey = "|".join(key.split("|")[:3])
        z0 = h4j["regions"][ekey]["f0"]["fine"]["near"]
        if z0.get("empty"):
            z0 = h4j["regions"][ekey]["f0"]["fine"]["box"]
        rho_abs = z0["median_abs_rho"]
        x_ = z0["x_median"]
        L = LFLOOR[foot] * PC
        kk = 1 / L
        ML_ = (1 + x_) ** 2
        rows_ = {}
        for fct in (1.0, 1e-3, 1e-6, 1e-9):
            dPh = 4 * math.pi * G_SI * rho_abs * fct / c_SI ** 2
            gh_ = dPh * (1 + dPh * L ** 2 / 2)
            zPh = kk ** 2 / (ML_ + L ** 2 * kk ** 2 / 2)
            c_, L1_, L4_ = lam_V1_V4(zPh, zPh, gh_)
            eps1 = (c_ * kk / L1_) ** 4
            rows_[f"{fct:g}"] = {"c_pi": c_, "c_pi_m_s": c_ * c_SI, "Lambda_V1": L1_, "k_sc_m-1": L1_ / c_,
                                 "lambda_sc_m": 2 * math.pi * c_ / L1_, "eps_at_1/L*": eps1}
        E1.append({"region": key, "median_abs_rho_kg_m3": rho_abs, "x": x_, "P_side": rows_,
                   "N_side": "c_pi = 0 (no gradient term): P3's estimate gives Lambda = 0, strongly coupled at every k "
                             "(as BS's gamma_L = 0 theory; C5 H8)"})
    for r_ in E1[:4]:
        log(f"  E1 {r_['region']}: P side c_pi {r_['P_side']['1']['c_pi_m_s']:.2f} m/s, strong-coupling length "
            f"{r_['P_side']['1']['lambda_sc_m']:.2e} m; at rho/1e9: c_pi {r_['P_side']['1e-09']['c_pi_m_s']:.2e} m/s, "
            f"length {r_['P_side']['1e-09']['lambda_sc_m']:.2e} m, eps(1/L*) {r_['P_side']['1e-09']['eps_at_1/L*']:.1e}; "
            f"N side: c_pi = 0")
    res["E1"] = E1
    E2 = []
    K4 = 4 * math.pi * G_SI

    def gmax_beta(rho_abs, x_, Lm, beta):
        A_ = K4 * rho_abs
        B_ = c_SI ** 2 * beta / (2 + 3 * beta)
        C_ = (1 + x_) ** 2 - 1
        D_ = Lm ** 2 / 2
        X_ = (D_ * A_ - B_ * C_) / (2 * B_ * D_)
        if X_ <= 0:
            return math.sqrt(A_ * C_)
        return math.sqrt((A_ - B_ * X_) * (C_ + D_ * X_))

    worst_reg = None
    for key in [k_ for k_ in regs if f"L*{LFLOOR['canonical']}" in k_ or f"L*{LFLOOR['alt']}" in k_]:
        foot = key.split("|")[1]
        e_ = regs[key]
        rho_abs = None
        ekey = "|".join(key.split("|")[:3])
        z0 = h4j["regions"][ekey]["f0"]["fine"]["near"]
        if z0.get("empty"):
            z0 = h4j["regions"][ekey]["f0"]["fine"]["box"]
        rho_abs, x_ = z0["median_abs_rho"], z0["x_median"]
        T = e_["T_Gyr"] * GYR
        Lm = LFLOOR[foot] * PC
        ef = {f"{b_:g}": gmax_beta(rho_abs, x_, Lm, b_) * T for b_ in (1e-9, 1e-12, 1e-15, 1e-18)}
        E2.append({"region": key, "efolds": ef, "N_bounded_H4": e_["median"]["N_bounded"]})
        if worst_reg is None or ef["1e-18"] > worst_reg[1]["efolds"]["1e-18"]:
            worst_reg = (key, E2[-1], rho_abs, x_, Lm, T)
    key_w, _, ra_, xw_, Lw_, Tw_ = worst_reg
    lo_, hi_ = -40.0, 0.0
    for _ in range(200):
        mid = 0.5 * (lo_ + hi_)
        if gmax_beta(ra_, xw_, Lw_, 10 ** mid) * Tw_ > 1.0:
            lo_ = mid
        else:
            hi_ = mid
    beta1 = 10 ** hi_
    for r_ in E2:
        log(f"  E2 {r_['region']}: e-folds at beta 1e-9/1e-12/1e-15/1e-18: "
            f"{[f'{v_:.2e}' for v_ in r_['efolds'].values()]} (H4 bounded branch {r_['N_bounded_H4']:.3f})")
    log(f"  E2: worst median region {key_w} reaches 1 e-fold at beta = {beta1:.2e} (C5 window upper edge ~1e-9, estimate); "
        f"beta is a new constant in v3 (not adopted)")
    res["E2"] = {"rows": E2, "beta_1efold": beta1, "worst_region": key_w}

    # ============================================================================================ VERDICT
    log("")
    ck = {c_["id"]: c_["pass"] for c_ in checks}
    a_ok = ck.get("A0a") and ck.get("A0b") and ck.get("C0")
    if not a_ok:
        wp = "UNDECIDED"
        why = "reproduction or discretisation validation failed (A0/C0)"
    elif ck.get("B1-S") and ck.get("B2-S") and ck.get("C1") and ck.get("C2"):
        wp = "WELL-POSED"
        why = "finite UV limit where D.P < 0; nonlinear c^2 = gamma_L (D.P + rho_d) Theta(D.P) >= 0; slab rates converge"
    else:
        grow = any((not verdict_C[c_]["a"]) and verdict_C[c_]["max_ratio"] > 1.10 for c_ in ("C1", "C2"))
        if (not ck.get("B1-S")) or (not ck.get("B2-S")) or grow:
            wp = "STILL ILL-POSED"
            why = ("the stiffness acts where rho_tau < 0 (non-zero UV coefficient / c^2 < 0 / resolution-growing rate)")
        else:
            wp = "UNDECIDED"
            why = "slab bound or sign-consistency defect"
    if not ck.get("D1"):
        stat = "UNDECIDED"
    elif ck.get("D2") and ck.get("D3") and ck.get("D4"):
        stat = "UNCHANGED"
    elif d4_status == "UNDECIDED" and ck.get("D2") and ck.get("D3"):
        stat = "UNDECIDED"
    else:
        where = [c_ for c_ in ("D2", "D3", "D4") if not ck.get(c_)]
        stat = "CHANGE (" + ", ".join({"D2": "C6 Solar System", "D3": "P3 strong field", "D4": "D10 globular floor"}[w_]
                                      for w_ in where) + ")"
    if wp == "WELL-POSED" and stat == "UNCHANGED":
        overall = "WELL-POSED + STATICS UNCHANGED"
    elif wp == "WELL-POSED" and stat.startswith("CHANGE"):
        overall = "WELL-POSED BUT STATICS CHANGE: " + stat[len("CHANGE "):]
    elif wp == "STILL ILL-POSED":
        overall = "STILL ILL-POSED (" + why + ")"
    else:
        overall = "UNDECIDED (" + (why if wp == "UNDECIDED" else "statics " + stat) + ")"
    qual = ["conditional on rho_d >= -D.P wherever D.P > 0 (non-negative dust; v3's mu_K -> 0 regime)",
            "requires sign-consistent numerics (C3 diagnostic)",
            "the bounded instability where rho_tau < 0 remains (H4's gamma_L = 0 branch: 0.006-0.20 e-folds median, "
            "<= 4.2 at the deepest cells)",
            "strong coupling: c_pi = 0 on the D.P < 0 side (E1)"]
    log(f"WELL-POSEDNESS: {wp} -- {why}")
    log(f"STATICS: {stat}")
    log(f"OVERALL: {overall}")
    for q_ in qual:
        log(f"  qualifier: {q_}")
    res["verdict"] = {"well_posedness": wp, "why": why, "statics": stat, "overall": overall, "qualifiers": qual}
    npass = sum(c_["pass"] for c_ in checks)
    log(f"run: {time.time() - T0:.1f} s, peak RSS parent {rss_gb():.2f} GB, children {rss_gb(resource.RUSAGE_CHILDREN):.2f} GB, "
        f"single thread")
    log(f"X3_SWITCHED_STIFFNESS COMPLETE: {npass}/{len(checks)} checks PASS.")
    res["checks"] = checks
    res["runtime_s"] = time.time() - T0
    res["peak_rss_GB"] = {"parent": rss_gb(), "children": rss_gb(resource.RUSAGE_CHILDREN)}
    json.dump(clean(res), open(os.path.join(HERE, f"x3_switched_stiffness_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"x3_switched_stiffness{TAG}.out"), "w").write("\n".join(lines) + "\n")
    sys.exit(0 if npass == len(checks) else 1)


if __name__ == "__main__":
    if "--d10" in sys.argv:
        production(sys.argv[sys.argv.index("--d10") + 1])
    else:
        main()
