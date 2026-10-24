#!/usr/bin/env python3
"""H5_v3s_lobe_growth: do v3s's D.P < 0 lobes produce harmful growth?

v3s = v3 with the switched stiffness -(gamma_L/2)[max(D.P, 0)]^2 (X3). Where D.P < 0 the khronon/dust pair follows H4's
bounded gamma_L = 0 branch, Gamma = sqrt(K |rho_tau| (M - 1)). The open question (V3_FULL_PICTURE 4.7): how long does the
khronon fluid sit in a moving system's lobe?

Part A (sympy): the PN system's Euler-Lagrange equations, the Galilean frame of the static branch, the steady linear
response in a moving system's frame, sign invariance of the khronon charge, and the Danby-Camm flow-through density.
Part B: lobe maps (X3's switched D10 operator) for the outer globulars and the MW satellites, with H4's rates().

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (2cde8548ed, committed alone before any number).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 h5_v3s_lobe_growth.py          (H5_MUTATE=1: A2, A3, A5 mutated)
kappa = 1/2 FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
"""
import csv
import json
import math
import os
import resource
import sys
import time

if os.environ.get("PYTHONHASHSEED") != "0":      # determinism of sympy's simplification paths (as H4, X3)
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED="0"))

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator
import scipy.sparse as sps

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
H4JSON = os.path.join(REPO, "rebuild_2026_10_22", "H4_v3_saddle_stability", "h4_v3_saddle_stability_results.json")
X3JSON = os.path.join(REPO, "rebuild_2026_10_22", "X3_switched_stiffness", "x3_switched_stiffness_results.json")
S1CSV = os.path.join(REPO, "rebuild_2026_10_22", "S1_v3_hosted_small", "s1_per_system.csv")
U1CSV = os.path.join(REPO, "rebuild_2026_10_22", "U1_v3_dust_content", "u1_satellites_per_system.csv")
D10DIR = os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar")
D10JSON = os.path.join(D10DIR, "d10_native_lstar_results.json")
sys.path.insert(0, D10DIR)
import d10_solver as S  # noqa: E402  (record code, imported read-only)

MUTATE = os.environ.get("H5_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"h5_v3s_lobe_growth{TAG}.out")
JSON = os.path.join(HERE, f"h5_v3s_lobe_growth_results{TAG}.json")
CSVOUT = os.path.join(HERE, "h5_per_system.csv")

# ------------------------------------------------------------------ constants
# H4's (rates(), B0a)
G_SI = 6.67430e-11
MSUN = 1.98847e30
PC = 3.0856775814913673e16
KPC = 1e3 * PC
AU = 1.495978707e11
YR = 3.15576e7
GYR = 1e9 * YR
T_H = 13.8 * GYR
MSUN_PC3 = MSUN / PC ** 3
K4 = 4 * math.pi * G_SI
# record footings
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
D10_CENTRAL = {"canonical": 21.680757539917785, "alt": 22.847696106846282}
# D10 driver constants (verbatim, as X3)
G10, Msun10, kpc10, PC10 = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
A_H = 3.0 * kpc10
GE2_8KPC = 2.0592e-10
UPS_V = 1.6
PRIMARY = ["NGC 2419", "Pal 3", "Pal 4", "Pal 14"]
MB_MID = 6.0e10
# S1's constants (B0c, satellites)
G_S1, MSUN_S1, PC_S1 = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC_S1 = 1e3 * PC_S1
A_H_S1 = 3.0 * KPC_S1

lines, checks = [], []
res = {"lane": "H5_v3s_lobe_growth", "mutate": MUTATE, "frozen": "2cde8548ed"}


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


# ====================================================================================== record code (copied read-only)
def rates(rho_abs, x_, Lp, T):
    """H4 Part D rates(), verbatim (h4_v3_saddle_stability.py L803-815)."""
    mL1 = (1 + x_) ** 2 - 1
    Gb = math.sqrt(K4 * rho_abs * mL1)
    out = {"Gamma_bounded_s-1": Gb, "N_bounded": Gb * T}
    for lam_name, lam in (("L*", Lp * PC), ("1pc", PC), ("1AU", AU)):
        kL = 2 * math.pi / lam * Lp * PC
        Gm = math.sqrt(K4 * rho_abs * (mL1 + kL ** 2 / 2))
        out[f"Gamma_{lam_name}_s-1"] = Gm
        out[f"N_{lam_name}"] = Gm * T
    rhs = 1 / (K4 * rho_abs * T ** 2) - mL1
    out["lambda1_pc"] = float("inf") if rhs <= 0 else 2 * math.pi * Lp / math.sqrt(2 * rhs)
    return out


def g_mw(R_kpc, Mb, a0):
    """X3 (D10 driver) host field: Hernquist M_b, a_H = 3 kpc, the law."""
    gN = G10 * Mb * Msun10 / (R_kpc * kpc10 + A_H) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))


def s_gal(R_kpc, Mb, a0, a_m):
    """X3: Galactic phantom at R_GC in D10 units (dimensionless s_g, and rho_ph in kg/m^3)."""
    def F(Rm):
        gN = G10 * Mb * Msun10 / (Rm + A_H) ** 2
        g = 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
        return Rm * Rm * (g - gN)
    R = R_kpc * kpc10
    dR = 1e-4 * R
    Krho = (F(R + dR) - F(R - dR)) / (2 * dR) / R ** 2
    return Krho * a_m / a0, Krho / (4 * math.pi * G10)


def g_host_s1(R_m, Mb, a0):
    """S1's g_host (S1 constants)."""
    gN = G_S1 * Mb * MSUN_S1 / (R_m + A_H_S1) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))


class SW(S.Solver2D):
    """X3's switched operator (copied): lam2 * [(D + s_g)_+ - (s_g)_+]; switched=False is D10's operator exactly."""

    def __init__(self, g, y, xe, Lam, sg=0.0, switched=True, isolated=False):
        super().__init__(g, y, xe, Lam, isolated=isolated)
        self.sg = float(sg)
        self.switched = bool(switched)

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


# ============================================================================================= PART A (sympy)
def part_A():
    import sympy as sp
    from sympy.calculus.euler import euler_equations
    out = {}
    log("")
    log("A: the khronon velocity relative to a moving system's lobe (sympy)")
    # ---- A1: Euler-Lagrange equations of the PN Lagrangian (H4 A1 form, switched stiffness as a generic F)
    t, x, z = sp.symbols("t x z", real=True)
    K, gL, muK = sp.symbols("K gamma_L mu_K", positive=True)
    phi = sp.Function("phi")(t, x, z)
    sig = sp.Function("sigma")(t, x, z)
    P1 = sp.Function("P1")(t, x, z)
    P2 = sp.Function("P2")(t, x, z)
    rhom = sp.Function("rho_m")(t, x, z)
    W, F = sp.Function("W"), sp.Function("F")
    Xi = phi - sig.diff(t) + (sig.diff(x) ** 2 + sig.diff(z) ** 2) / 2
    divP = P1.diff(x) + P2.diff(z)
    L = (-(phi.diff(x) ** 2 + phi.diff(z) ** 2) / (2 * K) - rhom * phi + P1 * Xi.diff(x) + P2 * Xi.diff(z)
         - W(K * sp.sqrt(P1 ** 2 + P2 ** 2)) - gL / 2 * F(divP) + muK ** 2 * Xi ** 2 / (2 * K))
    eqs = euler_equations(L, [phi, sig, P1, P2], [t, x, z])
    rho_tau = divP - muK ** 2 * Xi / K
    v1, v2 = -sig.diff(x), -sig.diff(z)
    cont = rho_tau.diff(t) + (rho_tau * v1).diff(x) + (rho_tau * v2).diff(z)
    r_sig = sp.simplify(sp.expand(eqs[1].lhs + cont))          # EL_sigma = -(continuity)
    pois = (phi.diff(x, 2) + phi.diff(z, 2) - K * (rhom + rho_tau)) / K
    r_phi = sp.simplify(sp.expand(eqs[0].lhs - pois))
    psi = phi - Xi
    E1 = v1.diff(t) + v1 * v1.diff(x) + v2 * v1.diff(z) + psi.diff(x)
    E2 = v2.diff(t) + v1 * v2.diff(x) + v2 * v2.diff(z) + psi.diff(z)
    r_eu = [sp.simplify(sp.expand(E1)), sp.simplify(sp.expand(E2))]
    log(f"  A1: EL_sigma + [d_t rho_tau + div(rho_tau v_tau)] = {r_sig}; EL_phi - [lap phi - K(rho_m + rho_tau)]/K = "
        f"{r_phi}; D_t v_tau + grad(phi - Xi) = {r_eu} (rho_tau = div P - mu_K^2 Xi/K, v_tau = -grad sigma)")
    check("A1", r_sig == 0 and r_phi == 0 and r_eu == [0, 0], f"residuals {r_sig}, {r_phi}, {r_eu}", "all identically 0")
    out["A1"] = {"sigma": str(r_sig), "phi": str(r_phi), "euler": [str(e) for e in r_eu]}

    # ---- A2: Galilean frame
    xp, zp = sp.symbols("xp zp", real=True)
    Vx, Vz = sp.symbols("V_x V_z", real=True)
    s_, f_ = sp.Function("s"), sp.Function("f")
    a_, b_, tt = sp.symbols("a b tt")
    Xs, Zs = xp + Vx * t, zp + Vz * t
    sigp = s_(Xs, Zs, t) + Vx * xp + Vz * zp + (0 if MUTATE else 1) * (Vx ** 2 + Vz ** 2) * t / 2
    Xip = f_(Xs, Zs, t) - sp.diff(sigp, t) + (sp.diff(sigp, xp) ** 2 + sp.diff(sigp, zp) ** 2) / 2
    Xih = (f_(a_, b_, tt) - sp.diff(s_(a_, b_, tt), tt)
           + (sp.diff(s_(a_, b_, tt), a_) ** 2 + sp.diff(s_(a_, b_, tt), b_) ** 2) / 2).subs({a_: Xs, b_: Zs, tt: t})
    dXi = sp.simplify((Xip - Xih).doit())
    vh = [-sp.diff(s_(a_, b_, tt), a_).subs({a_: Xs, b_: Zs, tt: t}), -sp.diff(s_(a_, b_, tt), b_).subs({a_: Xs, b_: Zs, tt: t})]
    vp = [-sp.diff(sigp, xp), -sp.diff(sigp, zp)]
    dv = [sp.simplify((vp[0] - (vh[0] - Vx)).doit()), sp.simplify((vp[1] - (vh[1] - Vz)).doit())]
    log(f"  A2: x = x' + V t, sigma' = sigma + V.x' + {'0' if MUTATE else 'V^2 t/2'}: Xi' - Xi = {dXi}; "
        f"v' - (v - V) = {dv}. The static branch (v_tau = 0) holds only in the khronon rest frame; in a frame moving at "
        f"V the same fluid has v' = -V")
    check("A2", dXi == 0 and dv == [0, 0], f"Xi' - Xi = {dXi}; v' - (v - V) = {dv}", "identically 0")
    out["A2"] = {"dXi": str(dXi), "dv": [str(d) for d in dv]}

    # ---- A3: steady linear response in the system frame
    k, rb, ML, MT, Ls = sp.symbols("k rhobar M_L M_T Lstar", positive=True)
    c, s, Dk = sp.symbols("c s D", real=True)               # cos/sin of k's angle to the host field n; D = k.V
    Th = sp.symbols("Theta", nonnegative=True)
    drm = sp.symbols("drho_m")
    I = sp.I
    kx, kz = k * s, k * c
    gam = K * Ls ** 2 / 2                                     # gamma_L = K L*^2 / 2
    if not MUTATE:
        unk = sp.symbols("dr dvx dvz dphi dXi dPx dPz")
        dr, dvx, dvz, dphi, dXI, dPx, dPz = unk
        ku = -Dk                                              # fluid moves at -V in the system frame
        eqs3 = [I * ku * dr + I * rb * (kx * dvx + kz * dvz),         # continuity about (rhobar, -V)
                I * ku * dvx + I * kx * (dphi - dXI), I * ku * dvz + I * kz * (dphi - dXI)]   # Euler, kick -grad(phi - Xi)
    else:                                                     # MUTATE: Doppler dropped -> fluid in equilibrium (psi = 0)
        unk = sp.symbols("dr dphi dXi dPx dPz")
        dr, dphi, dXI, dPx, dPz = unk
        eqs3 = [dphi - dXI]
    eqs3 += [-k ** 2 * dphi - K * (drm + dr),                                          # Poisson, all mass
             I * kx * dXI - K * MT * dPx - gam * Th * kx * (kx * dPx + kz * dPz),       # P equation, Hessian K M
             I * kz * dXI - K * ML * dPz - gam * Th * kz * (kx * dPx + kz * dPz),       # (n = z: M_L along n)
             dr - I * (kx * dPx + kz * dPz)]                                           # rho_tau = div P (mu_K = 0)
    Am, bv = sp.linear_eq_to_matrix(eqs3, unk)
    sol = dict(zip(unk, Am.LUsolve(bv)))
    sub1 = {s: sp.sqrt(1 - c ** 2)}
    Mk = 1 / (c ** 2 / ML + (1 - c ** 2) / MT)
    target = drm / (Mk - 1 + Th * Ls ** 2 * k ** 2 / 2 - Dk ** 2 / (K * rb))
    r_i = sp.simplify(sp.together(sol[dr].subs(sub1) - target))
    m_ = 1 / Mk
    kap = k * Ls
    s0 = sp.limit(sol[dr].subs(sub1).subs(Th, 1), Dk, 0)
    r_ii = sp.simplify(sp.together(s0 / drm - m_ / (1 - m_ + kap ** 2 * m_ / 2)))
    lim_r = sp.limit(sol[dr].subs(sub1) * Dk ** 2, Dk, sp.oo)
    r_iii_r = sp.simplify(lim_r + K * rb * drm)
    dpsi = (sol[dphi] - sol[dXI]).subs(sub1)
    r_iii_p = sp.simplify(sp.limit(dpsi, Dk, sp.oo) + K * drm / k ** 2)
    if not MUTATE:
        r_iii_v = sp.simplify(sp.together(sol[unk[1]] - kx * (sol[dphi] - sol[dXI]) / Dk))
    else:
        r_iii_v = "n/a (no velocity in the mutated system)"
    log("  A3: steady linear response, system frame, host background (rhobar > 0, field n), stiffness gamma_L Theta:")
    log(f"      (i)  d rho_tau - d rho_m / [M(k) - 1 + Theta L*^2 k^2/2 - (k.V)^2/(K rhobar)] = {r_i}")
    log(f"      (ii) V = 0, Theta = 1: d rho_tau / d rho_m - m/(1 - m + kappa^2 m/2) [D10 Route F kernel] = {r_ii}")
    log(f"      (iii) V -> inf: (k.V)^2 d rho_tau + K rhobar d rho_m = {r_iii_r}; d psi + K d rho_m/k^2 = {r_iii_p}; "
        f"d v - k d psi/(k.V) = {r_iii_v}")
    log("      => static limit = the screened phantom (lobes from the anisotropic M); flow-through limit = the cold wake of the")
    log("         baryons' Newtonian potential, amplitude proportional to rhobar; crossover V_* = sqrt(K rhobar (M-1) + gamma_L rhobar k^2)/k")
    ok3 = (r_i == 0 and r_ii == 0 and r_iii_r == 0 and r_iii_p == 0 and r_iii_v == 0)
    check("A3", ok3, f"(i) {'0' if r_i == 0 else 'NONZERO'}, (ii) {r_ii}, (iii) {r_iii_r}, {r_iii_p}, "
          f"{'0' if r_iii_v == 0 else r_iii_v}", "all identically 0")
    out["A3"] = {"i": str(r_i)[:300], "ii": str(r_ii), "iii_rho": str(r_iii_r), "iii_psi": str(r_iii_p),
                 "iii_v": str(r_iii_v)}

    # ---- A4: sign invariance (Jacobi's formula)
    Xl, Zl = sp.symbols("X Z", real=True)
    x1 = sp.Function("x1")(Xl, Zl, t)
    x2 = sp.Function("x2")(Xl, Zl, t)
    Fm = sp.Matrix([[x1.diff(Xl), x1.diff(Zl)], [x2.diff(Xl), x2.diff(Zl)]])
    Jd = Fm.det()
    divv = (Fm.diff(t) * Fm.inv()).trace()
    rho0 = sp.Function("rho0")(Xl, Zl)
    r_a4 = sp.simplify((rho0 / Jd).diff(t) + (rho0 / Jd) * divv)
    log(f"  A4: rho = rho0(X)/det(dx/dX) in Lagrangian continuity D_t rho + rho div v: residual {r_a4} -> the sign of "
        f"rho_tau is carried along v_tau (before caustics); rho_tau > 0 in, rho_tau > 0 out")
    check("A4", r_a4 == 0, f"residual {r_a4}", "identically 0")
    out["A4"] = str(r_a4)

    # ---- A5: Danby-Camm flow through the lobe (point mass, psi = phi_N of the baryons)
    r, th, GM, V = sp.symbols("r theta GM V", positive=True)
    R = r * sp.sin(th)
    b = (R + sp.sqrt(R ** 2 + 4 * r * GM / V ** 2 * (1 + sp.cos(th)))) / 2
    vr = -GM / (b * V) * sp.sin(th) + V * sp.cos(th)
    vth = -b * V / r
    rho = b ** 2 / (R * (2 * b - R))
    div = (1 / r ** 2) * sp.diff(r ** 2 * rho * vr, r) + 1 / (r * sp.sin(th)) * sp.diff(sp.sin(th) * rho * vth, th)
    fdiv = sp.lambdify((r, th, GM, V), div * r / V, "numpy")
    fen = sp.lambdify((r, th, GM, V), (vr ** 2 + vth ** 2 - V ** 2 - 2 * GM / r) / V ** 2, "numpy")
    rng = np.random.default_rng(5)
    rr = 10 ** rng.uniform(-1, 2, 200)
    tq = rng.uniform(0.05, math.pi - 0.05, 200)
    cmax = max(float(np.max(np.abs(fdiv(rr, tq, gm, vv)))) for gm, vv in ((1.0, 1.0), (0.3, 2.0)))
    emax = max(float(np.max(np.abs(fen(rr, tq, gm, vv)))) for gm, vv in ((1.0, 1.0), (0.3, 2.0)))
    bb, RR = sp.symbols("b R", positive=True)
    ident = sp.simplify(bb ** 2 / (RR * (2 * bb - RR)) - 1 - (bb - RR) ** 2 / (RR * (2 * bb - RR)))
    frho = sp.lambdify((r, th, GM, V), rho, "numpy")
    lag = lagrangian_density(+1 if not MUTATE else -1, frho)
    dev = float(np.max(np.abs(lag[:, 2] / lag[:, 3] - 1)))
    mind = float(lag[:, 2].min())
    log(f"  A5: Danby-Camm steady continuity max |div(rho v)| r/(rho_inf V) = {cmax:.2e} (200 points, 2 parameter sets); "
        f"energy |v|^2 = V^2 + 2GM/r to {emax:.1e}; rho/rho_inf - 1 - (b-R)^2/[R(2b-R)] = {ident}")
    log(f"      numerical Lagrangian ({'REPULSIVE (mutate)' if MUTATE else 'attractive'} point mass, DOP853 rtol 1e-12, "
        f"{len(lag)} points): max |rho_num/rho_DC - 1| = {dev:.2e}, min rho_num/rho_inf = {mind:.6f}")
    ok5 = cmax <= 1e-9 and ident == 0 and len(lag) >= 20 and dev <= 1e-3 and mind >= 1.0
    check("A5", ok5, f"continuity {cmax:.1e}; identity {ident}; Lagrangian dev {dev:.1e}, min {mind:.6f}, n {len(lag)}",
          "<= 1e-9; 0; <= 1e-3 with min >= 1 at >= 20 points")
    out["A5"] = {"continuity_max": cmax, "energy_max": emax, "identity": str(ident), "lagrangian_maxdev": dev,
                 "lagrangian_min": mind, "n_points": len(lag)}
    # reported (not gated, frozen 1 A5): the same integration in NGC 2419's Plummer potential at lobe radii, units a = V = 1,
    # GM/(V^2 a) at the PROXY speed (canonical, D10 inputs), against the point-mass Danby-Camm density
    d10 = json.load(open(D10JSON))
    g = d10["clusters"]["NGC 2419"]
    a0c = A0["canonical"]
    Vc = math.sqrt(g_mw(g["RGC"], MB_MID, a0c) * g["RGC"] * kpc10)
    gmv = G10 * UPS_V * g["LV"] * Msun10 / (Vc ** 2 * g["rhl"] * PC10)
    lp = lagrangian_density(+1 if not MUTATE else -1, frho, pot="plummer", aP=1.0, GM=gmv,
                            bvals=(5.0, 10.0, 20.0, 40.0, 80.0), zq=np.linspace(-80, 80, 17))
    sel = lp[:, 0] >= 9.0
    log(f"      reported: NGC 2419 Plummer (GM/(V^2 a) = {gmv:.2e} at V = {Vc / 1e3:.0f} km/s), {int(sel.sum())} points at "
        f"r >= 9 a: rho/rho_inf in [{lp[sel, 2].min():.8f}, {lp[sel, 2].max():.8f}], max |rho_Plummer/rho_DC,point - 1| = "
        f"{np.max(np.abs(lp[sel, 2] / lp[sel, 3] - 1)):.1e}")
    out["A5_plummer_NGC2419"] = {"GM_over_V2a": gmv, "n": int(sel.sum()), "min": float(lp[sel, 2].min()),
                                 "max": float(lp[sel, 2].max()),
                                 "maxdev_vs_point": float(np.max(np.abs(lp[sel, 2] / lp[sel, 3] - 1)))}
    return out, frho


def lagrangian_density(sgn, frho, pot="point", aP=1.0, GM=1.0, Vv=1.0, bvals=(0.5, 1.0, 2.0, 5.0, 10.0, 20.0),
                       zq=None, Z0=1e6):
    """cold test particles from z = -Z0 (x = b, v = (0, V)) in a point-mass or Plummer potential; density from the
    Jacobian of (b, t) -> (x, z): rho/rho_inf = V b / (x |det|). Returns rows (r, theta_from_downstream, rho_num, rho_DC)."""
    def rhs(_t, u):
        xx, zz, vx, vz = u
        d = (xx * xx + zz * zz) ** 1.5 if pot == "point" else (xx * xx + zz * zz + aP * aP) ** 1.5
        return [vx, vz, -sgn * GM * xx / d, -sgn * GM * zz / d]
    zq = np.linspace(-30, 50, 9) if zq is None else zq
    out = []
    for b0 in bvals:
        sols = {}
        for bb_ in (b0 * (1 - 1e-5), b0, b0 * (1 + 1e-5)):
            sols[bb_] = solve_ivp(rhs, (0, (Z0 + zq.max() + 10) / Vv), [bb_, -Z0, 0.0, Vv], method="DOP853", rtol=1e-12,
                                  atol=1e-12, dense_output=True)
        s0 = sols[b0]
        for zt in zq:
            tq = (Z0 + zt) / Vv
            u = s0.sol(tq)
            um = sols[b0 * (1 - 1e-5)].sol(tq)
            up = sols[b0 * (1 + 1e-5)].sol(tq)
            if u[0] <= 0:
                continue
            dxb = (up[0] - um[0]) / (2e-5 * b0)
            dzb = (up[1] - um[1]) / (2e-5 * b0)
            det = dxb * u[3] - dzb * u[2]
            dens = Vv * b0 / (u[0] * abs(det))
            rq = math.hypot(u[0], u[1])
            thq = math.atan2(u[0], u[1])
            out.append((rq, thq, dens, float(frho(rq, thq, GM, Vv))))
    return np.array(out)


# ============================================================================================ PART B helpers
GR = S.Grid2D(nper=24, Nt=16)
CELLV = np.outer((GR.re[1:] ** 3 - GR.re[:-1] ** 3) / 3.0, np.cos(GR.te[:-1]) - np.cos(GR.te[1:])) * 2 * math.pi


def solve_map(y, xe, Lam, sg):
    """unswitched (D10) solve, then the switched (v3s) solve warm-started from it (as X3 D4)."""
    su = SW(GR, y, xe, Lam, switched=False)
    su.solve()
    Du = su.divfield() + sg
    ss = SW(GR, y, xe, Lam, sg=sg, switched=True)
    ss.solve(U0=su.U, maxit=200)
    Ds = ss.divfield() + sg
    chi = ss.U[:GR.n]
    vr = GR.Crr @ chi + xe * np.cos(GR.t2d)
    vt = GR.Cth @ chi - xe * np.sin(GR.t2d)
    xloc = np.hypot(vr, vt)
    return {"Du": Du, "Ds": Ds, "x": xloc, "res_u": su.res, "res_s": ss.res, "it_s": ss.it}


def lobe_stats(Dtot, xloc, a_m, a0, Gc):
    """lobe = cells with total rho_tau < 0; returns stats (SI) and the Gamma grid (1/s)."""
    rho = Dtot * a0 / (4 * math.pi * Gc * a_m)                  # kg/m^3
    neg = rho < 0
    Gam = np.zeros(GR.n)
    if not neg.any():
        return {"empty": True}, Gam.reshape(GR.Nr, GR.Nt)
    Gam[neg] = np.sqrt(K4 * np.abs(rho[neg]) * ((1 + xloc[neg]) ** 2 - 1))
    vol = CELLV.ravel() * a_m ** 3
    w = vol[neg]
    a_ = np.abs(rho[neg])
    o_ = np.argsort(a_)
    cw = np.cumsum(w[o_]) / w.sum()
    med = float(a_[o_][np.searchsorted(cw, 0.5)])
    xo = xloc[neg]
    ox = np.argsort(xo)
    cwx = np.cumsum(w[ox]) / w.sum()
    xmed = float(xo[ox][np.searchsorted(cwx, 0.5)])
    ik = int(np.argmin(rho))
    ii = np.where(neg)[0] // GR.Nt
    st = {"empty": False, "V_m3": float(w.sum()), "ell_m": float(w.sum()) ** (1 / 3), "median_abs_rho": med,
          "x_median": xmed, "deep_abs_rho": float(-rho[ik]), "x_deep": float(xloc[ik]), "r_deep_a": float(GR.r2d[ik]),
          "theta_deep_deg": math.degrees(GR.t2d[ik]), "r_in_a": float(GR.re[ii.min()]), "r_out_a": float(GR.re[ii.max() + 1]),
          "touches_box": bool(ii.max() >= GR.Nr - 1), "Gamma_deep": float(Gam[ik]), "n_cells": int(neg.sum())}
    return st, Gam.reshape(GR.Nr, GR.Nt)


def make_interp(Gam):
    th = np.concatenate([[0.0], GR.tc, [math.pi]])
    G2 = np.concatenate([Gam[:, :1], Gam, Gam[:, -1:]], axis=1)
    return RegularGridInterpolator((np.log(GR.rc), th), G2, method="linear", bounds_error=False, fill_value=0.0)


def gam_at(itp, X, Y, Z):
    r = np.sqrt(X * X + Y * Y + Z * Z)
    r = np.maximum(r, 1e-30)
    th = np.arccos(np.clip(Z / r, -1, 1))
    return itp(np.stack([np.log(r), th], axis=-1))


def path_max(itp, rmax, angles_deg=(0, 30, 60, 90), noff=61, ns=4000):
    """max over straight paths of int Gamma ds (grid units of a); returns (max, per-angle max)."""
    S_ = 1.05 * rmax
    offs = np.linspace(-S_, S_, noff)
    sgrid = np.linspace(-S_, S_, ns)
    ds = sgrid[1] - sgrid[0]
    best = {}
    for al in angles_deg:
        a = math.radians(al)
        d = np.array([math.sin(a), 0.0, math.cos(a)])
        e1 = np.array([math.cos(a), 0.0, -math.sin(a)])
        e2 = np.array([0.0, 1.0, 0.0])
        mx = 0.0
        for p in offs:
            P_ = p * e1[None, None, :] + offs[:, None, None] * e2[None, None, :] + sgrid[None, :, None] * d[None, None, :]
            g = gam_at(itp, P_[..., 0], P_[..., 1], P_[..., 2])
            I_ = (g.sum(axis=1) - 0.5 * (g[:, 0] + g[:, -1])) * ds
            mx = max(mx, float(I_.max()))
        best[al] = mx
    return max(best.values()), best


def apo_max(itp, rmax, ge_units, noff=61, nz=4000):
    """radial orbit at apocentre: N = (4/sqrt(2 g)) max over lines parallel to n and turning points of
    int_0^inf Gamma(z0 +- u^2) du (grid units; returns the bare max of sqrt(h) * correlation, to be scaled)."""
    S_ = 1.05 * rmax
    zg = np.linspace(-S_, S_, nz)
    h = zg[1] - zg[0]
    m = np.arange(1, nz)
    wts = np.sqrt(m) - np.sqrt(m - 1)
    best = 0.0
    for R0 in np.linspace(0, S_, noff):
        g = gam_at(itp, np.full(nz, R0), np.zeros(nz), zg)
        for gg in (g, g[::-1]):
            Gt = 0.5 * (gg[:-1] + gg[1:])                     # segment means, k = 0..nz-2
            # A_i = sum_{m>=1} w_m Gt_{i+m-1}
            A = np.convolve(Gt[::-1], wts)[:nz - 1][::-1]
            best = max(best, float(A.max()) * math.sqrt(h))
    return best * 4.0 / math.sqrt(2.0 * ge_units)


def flow_state(st, a_m, Mb_kg, V, Gc, Dtot_grid_neg):
    """Danby-Camm density over the lobe cells (x 16 azimuths) for V parallel and perpendicular to n (point mass M_b)."""
    GMv2 = Gc * Mb_kg / V ** 2 / a_m                          # GM/V^2 in grid units
    ii, jj = np.where(Dtot_grid_neg)
    r = GR.rc[ii]
    t = GR.tc[jj]
    phis = (np.arange(16) + 0.5) * 2 * math.pi / 16
    X = (r[:, None] * np.sin(t)[:, None] * np.cos(phis)[None, :]).ravel()
    Y = (r[:, None] * np.sin(t)[:, None] * np.sin(phis)[None, :]).ravel()
    Z = (np.repeat(r * np.cos(t), 16))
    out = {}
    for lab, vdir in (("par", np.array([0.0, 0.0, 1.0])), ("perp", np.array([1.0, 0.0, 0.0]))):
        down = -vdir                                          # fluid moves at -V in the system frame
        rr = np.sqrt(X * X + Y * Y + Z * Z)
        cth = (X * down[0] + Y * down[1] + Z * down[2]) / rr
        th = np.arccos(np.clip(cth, -1, 1))
        R = rr * np.sin(th)
        b = 0.5 * (R + np.sqrt(R * R + 4 * rr * GMv2 * (1 + np.cos(th))))
        dens = b * b / (R * (2 * b - R))
        out[lab] = {"min": float(dens.min()), "max": float(dens.max()), "median": float(np.median(dens))}
    r_in = st["r_in_a"] * a_m
    out["dv_max_kms"] = (math.sqrt(V ** 2 + 2 * Gc * Mb_kg / r_in) - V) / 1e3
    out["r_cap_pc"] = 2 * Gc * Mb_kg / V ** 2 / PC
    out["r_in_pc"] = r_in / PC
    out["v_esc_rin_kms"] = math.sqrt(2 * Gc * Mb_kg / r_in) / 1e3
    out["GM_over_rinV2"] = Gc * Mb_kg / (r_in * V ** 2)
    return out


def system_block(name, foot, a_m, y, xe, Lp, sg, rho_gal_SI, Mb_kg, V, d_host_m, a0, Gc, V_apo10=None):
    Lam = Lp * PC10 / a_m
    mp = solve_map(y, xe, Lam, sg)
    st, Gam = lobe_stats(mp["Ds"], mp["x"], a_m, a0, Gc)
    stu, _ = lobe_stats(mp["Du"], mp["x"], a_m, a0, Gc)
    row = {"name": name, "foot": foot, "Lstar_pc": Lp, "a_pc": a_m / PC, "y": y, "x_e": xe, "V_kms": V / 1e3,
           "res_u": mp["res_u"], "res_s": mp["res_s"], "rho_host_Msun_pc3": rho_gal_SI / MSUN_PC3,
           "Mb_Msun": Mb_kg / MSUN, "unswitched_deep_Msun_pc3": (stu.get("deep_abs_rho", 0.0) / MSUN_PC3) if not stu["empty"] else 0.0,
           "unswitched_empty": stu["empty"]}
    if st["empty"]:
        row.update({"empty": True, "N_TH": 0.0, "N_path": 0.0, "N_cum": 0.0, "N_apo": 0.0, "V_crit_kms": 0.0,
                    "N_ell_med": 0.0, "N_ell_deep": 0.0})
        return row
    itp = make_interp(Gam)
    rmax = st["r_out_a"]
    pm, per_angle = path_max(itp, rmax)
    Vcrit = pm * a_m                                          # m/s
    ge_units = xe * a0 / a_m                                  # g_e in (grid length)/s^2 -> int Gamma du has sqrt(grid)
    N_apo = apo_max(itp, rmax, ge_units)
    T_orb = 2 * math.pi * d_host_m / V
    n_enc = 2 * T_H / T_orb
    Tl = min(T_H, st["ell_m"] / V)
    rm = rates(st["median_abs_rho"], st["x_median"], Lp, Tl)
    rd = rates(st["deep_abs_rho"], st["x_deep"], Lp, Tl)
    rTH = rates(st["deep_abs_rho"], st["x_deep"], Lp, T_H)
    rTHe = rates(st["deep_abs_rho"], xe, Lp, T_H)              # the preliminary's convention (x_e)
    ML1 = (1 + st["x_median"]) ** 2 - 1
    Vstar = st["ell_m"] * math.sqrt(K4 * rho_gal_SI * ML1) / (2 * math.pi) if rho_gal_SI > 0 else float("nan")
    fs = flow_state(st, a_m, Mb_kg, V, Gc, (mp["Ds"] < 0).reshape(GR.Nr, GR.Nt))
    row.update({"empty": False, "ell_pc": st["ell_m"] / PC, "r_in_pc": st["r_in_a"] * a_m / PC,
                "r_out_pc": rmax * a_m / PC, "touches_box": st["touches_box"], "theta_deep_deg": st["theta_deep_deg"],
                "r_deep_pc": st["r_deep_a"] * a_m / PC,
                "median_Msun_pc3": st["median_abs_rho"] / MSUN_PC3, "deep_Msun_pc3": st["deep_abs_rho"] / MSUN_PC3,
                "x_median": st["x_median"], "x_deep": st["x_deep"], "Gamma_deep": st["Gamma_deep"],
                "N_TH": rTH["N_bounded"], "N_TH_xe": rTHe["N_bounded"],
                "T_ell_Myr": Tl / GYR * 1e3, "N_ell_med": rm["N_bounded"], "N_ell_deep": rd["N_bounded"],
                "N_path": Vcrit / V, "path_per_angle_kms": {str(k_): v * a_m / 1e3 for k_, v in per_angle.items()},
                "V_crit_kms": Vcrit / 1e3, "N_apo": N_apo, "T_orb_Gyr": T_orb / GYR, "n_enc": n_enc,
                "N_cum": Vcrit / V * n_enc, "V_star_kms": Vstar / 1e3, "flow": fs})
    if V_apo10 is not None:
        row["V_apo10_kms"] = V_apo10 / 1e3
        row["N_path_at_Vapo10"] = Vcrit / V_apo10
    return row


# ================================================================================================= main
def main():
    T0 = time.time()
    log("H5_v3s_lobe_growth: v3s's D.P < 0 lobes -- the khronon velocity relative to the lobe, and the e-folds")
    log(f"mutate = {MUTATE}; kappa = 1/2 FITTED; footings never pooled; one thread, nice 15")
    resA, frho = part_A()
    res["A"] = resA

    log("")
    log("B0: reproduce the record first")
    h4 = json.load(open(H4JSON))
    key = "S1_MW-M31|canonical|e0|L*21.7"
    nm = key.split("|L*")[0]
    zone = h4["regions"][nm]["f0"]["fine"]["near"]
    if zone.get("empty"):
        zone = h4["regions"][nm]["f0"]["fine"]["box"]
    Tq = min(T_H, zone["ell_m"] / h4["meta"][nm]["v"])
    mine = {"median": rates(zone["median_abs_rho"], zone["x_median"], 21.7, Tq),
            "max": rates(zone["max_abs_rho_excl_null"], zone["x_at_max"], 21.7, Tq)}
    dev = max(abs(mine[b][f] / h4["efolds"][key][b][f] - 1) for b in mine for f in mine[b])
    check("B0a", dev <= 1e-12, f"H4 row {key}: max rel dev {dev:.1e} over {sum(len(v) for v in mine.values())} fields "
          f"(N_bounded median {mine['median']['N_bounded']:.4f}, max {mine['max']['N_bounded']:.4f})", "<= 1e-12")
    x3 = json.load(open(X3JSON))
    d10 = json.load(open(D10JSON))
    cl = d10["clusters"]
    devs = []
    for row in x3["D4_maps"]:
        if abs(row["Lstar_pc"] - D10_CENTRAL[row["foot"]]) > 1e-9:
            continue
        g = cl[row["cluster"]]
        a0 = A0[row["foot"]]
        a = g["rhl"] * PC10
        xe = g_mw(g["RGC"], MB_MID, a0) / a0
        y = G10 * UPS_V * g["LV"] * Msun10 / (a * a * a0)
        sg_, _ = s_gal(g["RGC"], MB_MID, a0, a)
        su = SW(GR, y, xe, row["Lstar_pc"] * PC10 / a, switched=False)
        su.solve()
        Dt = su.divfield() + sg_
        conv = 1.0 / (a * 4 * math.pi * G10) * a0 / (Msun10 / PC10 ** 3)
        mn = float(Dt.min()) * conv
        devs.append((row["foot"], row["cluster"], mn, row["min_total_Msun_pc3"], abs(mn / row["min_total_Msun_pc3"] - 1)))
    mdev = max(d_[4] for d_ in devs)
    for d_ in devs:
        log(f"  B0b {d_[0]:9s} {d_[1]:8s}: min D.P {d_[2]:.6e} vs X3 {d_[3]:.6e} (rel {d_[4]:.1e})")
    check("B0b", len(devs) == 8 and mdev <= 1e-6, f"8 X3 D4 map minima, max rel dev {mdev:.1e}", "<= 1e-6")
    s1 = [r for r in csv.DictReader(open(S1CSV)) if r["host"] == "MW"]
    u1 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(U1CSV))}
    dx = []
    dx3 = []
    for r in s1:
        a0 = A0[r["footing"]]
        xe_ = g_host_s1(float(r["d_host_kpc"]) * KPC_S1, MB_MID, a0) / a0
        dx.append(abs(xe_ / float(r["x_e_mid"]) - 1))
        dx3.append(abs(g_mw(float(r["d_host_kpc"]), MB_MID, a0) / a0 / float(r["x_e_mid"]) - 1))
    check("B0c", len(dx) == 64 and max(dx) <= 1e-9, f"{len(dx)} rows, max rel dev {max(dx):.1e} (X3 g_mw: {max(dx3):.1e})",
          "<= 1e-9")
    res["B0"] = {"h4_row": key, "h4_dev": dev, "x3_maps": devs, "s1_xe_dev": max(dx), "x3_gmw_vs_s1": max(dx3)}

    # ---- method validations B2, B3 (synthetic uniform-Gamma lobes on the same grid)
    kR = 120
    Rv = GR.re[kR]
    Gu = np.where(GR.rc[:, None] < Rv, 1.0, 0.0) * np.ones((1, GR.Nt))
    pmv, _ = path_max(make_interp(Gu), Rv)
    eb2 = abs(pmv / (2 * Rv) - 1)
    check("B2", eb2 <= 0.01, f"uniform sphere R = {Rv:.4g}: max path integral / 2R = {pmv / (2 * Rv):.5f}", "within 1 %")
    # B3: slab z in [0, L] at R0 < r-range: build Gamma = 1 inside a thin cylinder? use a direct line test
    Lsl, gtest = 50.0, 1.0
    nz = 4000
    zg = np.linspace(-60, 60, nz)
    h = zg[1] - zg[0]
    gline = np.where((zg >= 0) & (zg <= Lsl), 1.0, 0.0)
    m = np.arange(1, nz)
    wts = np.sqrt(m) - np.sqrt(m - 1)
    Gt = 0.5 * (gline[:-1] + gline[1:])
    A = np.convolve(Gt[::-1], wts)[:nz - 1][::-1]
    i0 = int(np.argmin(np.abs(zg - 0.0)))
    num = A[i0] * math.sqrt(h) * 4 / math.sqrt(2 * gtest)
    ana = 2 * 1.0 * math.sqrt(2 * Lsl / gtest)
    eb3 = abs(num / ana - 1)
    check("B3", eb3 <= 0.01, f"uniform slab L = {Lsl}, turning point at the edge: numeric {num:.5f} vs 2 Gamma sqrt(2L/g) "
          f"{ana:.5f}", "within 1 %")

    rows = []
    if not MUTATE:
        # ---- (a) outer globulars
        log("")
        log("B1(a): outer globulars -- v3s switched maps (D10 solver, X3 operator), E_mid MW, Upsilon_V 1.6")
        for foot in ("canonical", "alt"):
            a0 = A0[foot]
            for name in PRIMARY:
                g = cl[name]
                a = g["rhl"] * PC10
                xe = g_mw(g["RGC"], MB_MID, a0) / a0
                y = G10 * UPS_V * g["LV"] * Msun10 / (a * a * a0)
                sg_, rph = s_gal(g["RGC"], MB_MID, a0, a)
                Vc = math.sqrt(g_mw(g["RGC"], MB_MID, a0) * g["RGC"] * kpc10)
                Vapo10 = Vc * math.sqrt(2 * math.log(10) / 99)
                Mb = UPS_V * g["LV"] * Msun10
                for Lp in (D10_CENTRAL[foot], 24.0, 90.0):
                    row = system_block(name, foot, a, y, xe, Lp, sg_, rph, Mb, Vc, g["RGC"] * kpc10, a0, G10, Vapo10)
                    row["class"] = "a_globular"
                    row["V_src"] = "PROXY v_c(R_GC), D10 MW E_mid"
                    rows.append(row)
                    log_row(row)
        # ---- (b) MW satellites
        log("")
        log("B1(b): MW satellites (S1 inputs, U1 LVD-3D speeds) -- v3s switched maps, E_mid MW")
        for r in s1:
            foot = r["footing"]
            a0 = A0[foot]
            u = u1[(foot, r["name"])]
            if u["V_src"] != "LVD-3D":
                continue
            a = float(r["rh_pc"]) * PC_S1
            y = float(r["y_plummer"])
            xe = float(r["x_e_mid"])
            d = float(r["d_host_kpc"])
            sg_, rph = s_gal(d, MB_MID, a0, a)
            Mb = y * a * a * a0 / G_S1
            V = float(u["V_kms"]) * 1e3
            for Lp in (D10_CENTRAL[foot], 90.0):
                row = system_block(r["name"], foot, a, y, xe, Lp, sg_, rph, Mb, V, d * KPC_S1, a0, G_S1)
                row["class"] = "b_satellite"
                row["V_src"] = "LVD-3D (U1)"
                rows.append(row)
                log_row(row)
        res["rows"] = rows
        verdicts(rows)
    else:
        log("")
        log("MUTATE: maps and statistics are not rerun (as frozen)")

    npass = sum(c_["pass"] for c_ in checks)
    log("")
    log(f"run: {time.time() - T0:.1f} s, peak RSS {rss_gb():.2f} GB, single thread")
    log(f"H5_V3S_LOBE_GROWTH COMPLETE: {npass}/{len(checks)} checks PASS.")
    res["checks"] = checks
    res["runtime_s"] = time.time() - T0
    res["peak_rss_GB"] = rss_gb()
    with open(JSON, "w") as fh:
        json.dump(clean(res), fh, indent=1)
    with open(OUT, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    if not MUTATE and rows:
        keys = ["class", "foot", "name", "Lstar_pc", "V_kms", "V_src", "x_e", "y", "a_pc", "Mb_Msun", "rho_host_Msun_pc3",
                "empty", "r_in_pc", "r_out_pc", "ell_pc", "median_Msun_pc3", "deep_Msun_pc3", "x_deep", "N_TH", "N_TH_xe",
                "T_ell_Myr", "N_ell_med", "N_ell_deep", "N_path", "V_crit_kms", "N_apo", "n_enc", "N_cum", "V_star_kms",
                "V_apo10_kms", "N_path_at_Vapo10", "res_s"]
        with open(CSVOUT, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(keys + ["flow_min_par", "flow_min_perp", "flow_max_perp", "r_cap_pc", "dv_max_kms"])
            for r_ in rows:
                fl = r_.get("flow", {})
                wr.writerow([r_.get(k_, "") for k_ in keys] + [fl.get("par", {}).get("min", ""), fl.get("perp", {}).get("min", ""),
                             fl.get("perp", {}).get("max", ""), fl.get("r_cap_pc", ""), fl.get("dv_max_kms", "")])
    sys.exit(0 if npass == len(checks) else 1)


def log_row(r):
    if r["empty"]:
        log(f"  {r['class'][0]} {r['foot']:9s} {r['name']:18s} L* {r['Lstar_pc']:5.1f}: no rho_tau < 0 cell (v3s); "
            f"unswitched {'none' if r['unswitched_empty'] else format(-r['unswitched_deep_Msun_pc3'], '.1e')}; res {r['res_s']:.0e}")
        return
    fl = r["flow"]
    log(f"  {r['class'][0]} {r['foot']:9s} {r['name']:18s} L* {r['Lstar_pc']:5.1f}: lobe r {r['r_in_pc']:.0f}-{r['r_out_pc']:.0f} pc"
        f"{' (BOX)' if r['touches_box'] else ''}, deep -{r['deep_Msun_pc3']:.2e} (x {r['x_deep']:.3f}), med -{r['median_Msun_pc3']:.1e},"
        f" ell {r['ell_pc']:.0f} pc | V {r['V_kms']:.0f} km/s: N_TH {r['N_TH']:.1f} (x_e conv. {r['N_TH_xe']:.1f}), "
        f"N_ell deep {r['N_ell_deep']:.3f}, N_path {r['N_path']:.3f}, V_crit {r['V_crit_kms']:.2f} km/s, N_apo {r['N_apo']:.2f}, "
        f"N_cum {r['N_cum']:.3f} (n_enc {r['n_enc']:.1f}) | flow: rho/rho_host min {min(fl['par']['min'], fl['perp']['min']):.6f}, "
        f"r_cap {fl['r_cap_pc']:.2g} pc vs r_in {fl['r_in_pc']:.0f} pc, |dv| <= {fl['dv_max_kms']:.3f} km/s, V_* {r['V_star_kms']:.2f} km/s;"
        f" res {r['res_s']:.0e}")


def verdicts(rows):
    log("")
    log("B1 / verdicts")
    okB1 = all(r_["res_u"] <= 1e-8 and r_["res_s"] <= 1e-8 for r_ in rows)
    fin = all(np.isfinite([r_.get(k_, 0.0) for k_ in ("N_TH", "N_path", "N_apo", "N_cum")]).all() for r_ in rows)
    check("B1", okB1 and fin, f"{len(rows)} maps x 2 solves, worst residual "
          f"{max(max(r_['res_u'], r_['res_s']) for r_ in rows):.1e}; statistics finite {fin}", "<= 1e-8; finite")
    V = {}
    for cls in ("a_globular", "b_satellite"):
        V[cls] = {}
        for foot in ("canonical", "alt"):
            rs = [r_ for r_ in rows if r_["class"] == cls and r_["foot"] == foot]
            fl = [r_ for r_ in rs if abs(r_["Lstar_pc"] - D10_CENTRAL[foot]) < 1e-9]
            ne = [r_ for r_ in fl if not r_["empty"]]
            mNp = max([r_["N_path"] for r_ in ne], default=0.0)
            mNc = max([r_["N_cum"] for r_ in ne], default=0.0)
            if cls == "a_globular":
                vc_ok = all(r_["V_crit_kms"] < r_["V_apo10_kms"] for r_ in ne)
            else:
                vc_ok = True
            if mNp >= 1 or mNc >= 1:
                vP = "BOUNDED-BUT-LARGE"
            elif not vc_ok:
                vP = "UNDETERMINED"
            else:
                vP = "BENIGN"
            Aok = all(c_["pass"] for c_ in checks if c_["id"].startswith("A"))
            dok = Aok and all(r_["flow"]["r_cap_pc"] < r_["flow"]["r_in_pc"] and
                              min(r_["flow"]["par"]["min"], r_["flow"]["perp"]["min"]) >= 1 - 1e-12 for r_ in ne)
            vD = "NO NEGATIVE LOBE IN THE FLOW STATE" if dok else "layer D not established"
            allr = [r_ for r_ in rs if not r_["empty"]]
            V[cls][foot] = {"P": vP, "D": vD, "n_systems": len(fl), "n_with_lobe": len(ne),
                            "max_N_path_floor": mNp, "max_N_cum_floor": mNc, "Vcrit_below_Vapo10": vc_ok,
                            "max_N_path_any_Lstar": max([r_["N_path"] for r_ in allr], default=0.0),
                            "max_N_TH_floor": max([r_["N_TH"] for r_ in ne], default=0.0),
                            "max_N_apo_floor": max([r_["N_apo"] for r_ in ne], default=0.0),
                            "max_N_apo_any_Lstar": max([r_["N_apo"] for r_ in allr], default=0.0),
                            "max_Vcrit_kms": max([r_["V_crit_kms"] for r_ in ne], default=0.0)}
            log(f"  {cls:12s} {foot:9s}: layer P {vP:18s} (max N_path {mNp:.3f}, max N_cum {mNc:.3f}, "
                f"V_crit < V_apo,10: {vc_ok}; {len(ne)}/{len(fl)} with a lobe at the floor); layer D: {vD}")
        order = ["BOUNDED-BUT-LARGE", "UNDETERMINED", "BENIGN"]
        V[cls]["class_P"] = min((V[cls][f]["P"] for f in ("canonical", "alt")), key=order.index)
        V[cls]["class_D"] = ("NO NEGATIVE LOBE IN THE FLOW STATE" if all(V[cls][f]["D"].startswith("NO") for f in ("canonical", "alt"))
                             else "layer D not established")
        log(f"  => class {cls}: {V[cls]['class_P']} (pattern granted); {V[cls]['class_D']} (flow state)")
    # (c) worst case
    ne_all = [r_ for r_ in rows if not r_["empty"]]
    fl_all = [r_ for r_ in ne_all if abs(r_["Lstar_pc"] - D10_CENTRAL[r_["foot"]]) < 1e-9]
    mapo = max([r_["N_apo"] for r_ in fl_all], default=0.0)
    wapo = max(fl_all, key=lambda r_: r_["N_apo"]) if fl_all else None
    comove = [r_["name"] for r_ in ne_all if r_["flow"]["r_cap_pc"] >= r_["flow"]["r_in_pc"]]
    mTH = max(fl_all, key=lambda r_: r_["N_TH"]) if fl_all else None
    vC = "BENIGN" if (mapo < 1 and not comove) else "BOUNDED-BUT-LARGE"
    log(f"  (c) worst case: radial-orbit apocentre max N_apo {mapo:.2f} ({wapo['name'] if wapo else '-'}, {wapo['foot'] if wapo else ''});"
        f" co-moving lobe allowed by the capture law (r_cap >= r_in) for: {comove if comove else 'none'}; "
        f"posited co-moving T_H: max N_TH {mTH['N_TH'] if mTH else 0:.1f} ({mTH['name'] if mTH else '-'}) -> {vC} "
        f"(pattern granted); reachability: A4 (negative charge cannot be produced from rho_tau > 0)")
    V["c_worst"] = {"P": vC, "max_N_apo_floor": mapo, "worst_apo": wapo["name"] if wapo else None,
                    "comoving_allowed": comove, "max_N_TH_floor": mTH["N_TH"] if mTH else 0.0,
                    "worst_TH": mTH["name"] if mTH else None}
    res["verdicts"] = V


if __name__ == "__main__":
    main()
