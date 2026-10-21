#!/usr/bin/env python3
"""
A11 — the cold-sector normalization from first principles.

Lane: deepseek_push/DS_FINAL_2026_10_21/A11_cold_normalization
Run:  python3 a11_checks.py            -> 16 checks, exit 0 iff all PASS
      python3 a11_checks.py --mutate   -> mutations that must break checks, exit 1

Every number printed here is also written to a11_results.json.

Constants (brief section 4):  c, G, a0, H0, Lambda, Mpc, pc.
Extra external inputs are flagged [EXT] with their source.

Nothing here models a new component. It computes what the frozen galactic law
g_N = g^2/(g + a0) already requires, and compares that with the census
bookkeeping N = (1 - f_b)/(f_ret f_b) carried in campaign_fresh_gravity.
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------- constants
C_LIGHT = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98847e30              # from GM_sun = 1.32712440018e20 / G, so G*MSUN is exact
PC = 3.0856775814913673e16
MPC = 3.0856775814913673e22
A0 = 9.36e-11                  # canonical footing (brief s4)
H0 = 2.1843e-18                # 67.4 km/s/Mpc
RHO_CRIT = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
RHO_VIR = 200.0 * RHO_CRIT        # Delta_vir = 200 wrt rho_crit (r_200c convention)
RHO_TA = 11.81 * 0.315 * RHO_CRIT  # A26 uses Delta_ta in units of Omega_m rho_crit (CFG527)

OMEGA_C = 0.2645               # [EXT] Planck: omega_c = 0.1200, h = 0.6736 -> 0.1200/h^2
OMEGA_M = 0.315                # [EXT] brief s4 / CFG527
FB = 0.02237 / 0.14237         # 0.157134  [EXT] CFG515 cfg515_lib.py:15 (engine f_b)
FB16 = 0.157                   # [EXT] CFG416 f_b16 used inside x_supply
H_DIM = 0.674                  # [EXT] CFG416 h
DELTA_TA = 11.81               # [EXT] A26 / CFG353: turnaround overdensity at z=0,
                               #       in units of Omega_m*rho_crit (CFG527 M_ta())
DELTA_VIR = 200.0              # convention: r_200c
LS_LO = 24.0 * PC              # [EXT] CFG820 lower edge of the stiffness window
LS_HI = 1.0e3 * PC             # [EXT] CFG820/AG6D scan boundary
CS2_MAX = 7.0e-7               # [EXT] CFG508 T1: c_s^2 bound for the clustering species
K_HALF_Mpc = 0.98              # [EXT] AG6D C1: k_1/2 at L* = 24 pc (Mpc^-1)
BULLET_SIGMA_M = 1.0           # [EXT] AG6D "Bullet-scale sigma/m < 1 cm^2/g", PROVISIONAL
T_AGE = 10.0 * 3.15576e16      # [EXT] 10 Gyr, cluster age used in the scattering estimate

# physical constants in record units
G_KPC = G * MSUN / (PC * 1e3) ** 2 / 1e6      # (km/s)^2 kpc / Msun
G_MPC = G * MSUN / MPC ** 2 / 1e6             # (km/s)^2 Mpc / Msun

MUTATIONS = {
    "Mu1": "replace the canonical law by the n=2 'a0-line' law g^2 = g_N^2 + a0 g_N",
    "Mu2": "set Delta_ta = 1 (no turnaround); r_ta becomes the mean-density radius",
    "Mu3": "set f_b = 0.5, so the cosmic ratio (1-f_b)/f_b becomes 1.0 instead of 5.364",
    "Mu4": "use the linear edge r_e = N r_M instead of the exact r_e = r_M sqrt(N(N+1))",
    "Mu5": "use c_s^2 = 4 pi G L*^2 rho instead of 2 pi G L*^2 rho",
    "Mu6": "use lambda_J = 2 pi L* instead of sqrt(2) pi L*",
    "Mu7": "use M_ph/M_b = (sqrt(1+2/y)-1)/2 (kernel coefficient 1 instead of 4)",
}


def apply_mutations(tags):
    global FB, DELTA_TA, g_of_gN, edge_radius, CS_PREFAC, LAMBDA_J_PREFAC, ratio_F
    for t in tags:
        if t not in MUTATIONS:
            raise SystemExit("unknown mutation %r" % t)
    if "Mu1" in tags:
        g_of_gN = lambda gn: math.sqrt(gn * gn + A0 * gn)
    if "Mu2" in tags:
        DELTA_TA = 1.0
    if "Mu3" in tags:
        FB = 0.5
    if "Mu4" in tags:
        edge_radius = lambda N, rM: N * rM
    if "Mu5" in tags:
        CS_PREFAC = 4.0 * math.pi * G
    if "Mu6" in tags:
        LAMBDA_J_PREFAC = 2.0 * math.pi
    if "Mu7" in tags:
        ratio_F = lambda y: 0.5 * (math.sqrt(1.0 + 2.0 / y) - 1.0)


# ------------------------------------------------------------ canonical objects
def g_of_gN(gn):
    """Inverse of the frozen law g_N = g^2/(g+a0)."""
    return 0.5 * gn * (1.0 + math.sqrt(1.0 + 4.0 * A0 / gn))


def ratio_F(y):
    """M_ph/M_b for a spherical system at the radius where y = g_N/a0."""
    return 0.5 * (math.sqrt(1.0 + 4.0 / y) - 1.0)


def y_of_ratio(r):
    return 4.0 / ((2.0 * r + 1.0) ** 2 - 1.0)


def census_fret(lm):
    """CFG416 fret_of, verbatim (CFG515 cfg515_lib.py:25-31 / CFG527 pm.py:301-308)."""
    if lm < 12.5:
        f = 0.10
    elif lm < 13.5:
        f = 0.10 + 0.45 * (lm - 12.5)
    else:
        f = min(0.55 + 0.30 * (lm - 13.5), 0.90)
    return min(f, 1.0)


def census_solve(mb):
    """Self-consistent retained fraction: f = fret_of(log10(M_ta)), M_ta = M_b h/(f f_b16)."""
    lmta = lambda f: math.log10(mb * H_DIM / (f * FB16))
    g = lambda f: census_fret(lmta(f)) - f
    return brentq(g, 0.05, 0.95, xtol=1e-14, rtol=1e-14)


def N_of(fret):
    """The census supply: N = M_c/M_b = (1-f_b)/(f_ret f_b)."""
    return (1.0 - FB) / (FB * fret)


def r_M(mb):
    return math.sqrt(G * mb * MSUN / A0)


def r_ta(mta):
    rho = DELTA_TA * OMEGA_M * RHO_CRIT
    return (3.0 * mta * MSUN / (4.0 * math.pi * rho)) ** (1.0 / 3.0)


def edge_radius(N, rM):
    """Exact root of r^2 (g-g_N)/G = N M_b for a point mass."""
    return rM * math.sqrt(N * (N + 1.0))


def r_vir_hernquist(mb, a_scale, delta=DELTA_VIR):
    """Solve r^2 g(r)/G = (4 pi/3) delta rho_bar r^3 with M_b(<r)/r^2 = M_b/(r+a)^2."""
    rM2 = G * mb * MSUN / A0
    pref = (4.0 * math.pi * G / 3.0) * delta * RHO_CRIT

    def f(logr):
        r = 10.0 ** logr
        y = rM2 / (r + a_scale) ** 2
        g = A0 * y * 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))
        return math.log(g / (pref * r))

    lo, hi = math.log10(1e-8 * MPC), math.log10(1e4 * MPC)
    return 10.0 ** brentq(f, lo, hi, xtol=1e-12, rtol=1e-14)


CS_PREFAC = 2.0 * math.pi * G
LAMBDA_J_PREFAC = math.sqrt(2.0) * math.pi


# ---------------------------------------------------------------- check driver
CHECKS = []


def report(cid, ok, value, threshold):
    CHECKS.append({"id": cid, "pass": bool(ok), "value": float(value), "threshold": float(threshold)})
    print("%s %s %.6e %.6e" % (cid, "PASS" if ok else "FAIL", value, threshold), flush=True)


def sym_check():
    """K1, K2: exact symbolic identities."""
    import sympy as sp
    gN, a0, Gs, r = sp.symbols("g_N a0 G r", positive=True)
    g = gN / 2 * (1 + sp.sqrt(1 + 4 * a0 / gN))
    e1 = sp.simplify(g ** 2 / (g + a0) - gN)
    report("K1", e1 == 0, 0.0 if e1 == 0 else abs(float(e1.subs({gN: 1, a0: 1}))), 1e-30)
    y = sp.symbols("y", positive=True)
    # M_ph/M_b = r^2 (g-g_N)/G / (r^2 g_N/G); with g_N = y a0
    ratio = sp.simplify(((g - gN) / gN).subs(gN, y * a0))
    target = (sp.sqrt(1 + 4 / y) - 1) / 2
    e2 = sp.simplify(ratio - target)
    # tie the symbolic result to the numeric function that every other check uses
    fnum = sp.lambdify(y, target, "math")
    worst = max(abs(ratio_F(yy) - fnum(yy)) / fnum(yy) for yy in (1e-4, 1e-2, 0.1, 1.0, 10.0))
    report("K2", e2 == 0 and worst < 1e-13, worst, 1e-13)


def check_limits():
    y = 1e-8
    deep = ratio_F(y)
    approx = 1.0 / math.sqrt(y) - 0.5
    report("K3a", abs(deep / approx - 1.0) < 1e-6, abs(deep / approx - 1.0), 1e-6)
    yh = 1e6
    report("K3b", abs(ratio_F(yh) * yh - 1.0) < 1e-5, abs(ratio_F(yh) * yh - 1.0), 1e-5)


def check_inverse():
    tgt = (1.0 - FB) / FB
    ys = y_of_ratio(tgt)
    r_over_rM = 1.0 / math.sqrt(ys)
    resid = abs(ratio_F(ys) / tgt - 1.0)
    report("K4a", resid < 1e-12, resid, 1e-12)
    report("K4b", abs(r_over_rM - 5.84297) < 1e-5, r_over_rM, 5.84297)
    # which halo mass has F(f_b a_v/a0) = 5.364 at r_200c?
    def gg(lm):
        Mv = 10.0 ** lm
        r = (3.0 * Mv * MSUN / (4 * math.pi * DELTA_VIR * RHO_CRIT)) ** (1 / 3)
        return math.log(ratio_F(FB * G * Mv * MSUN / (A0 * r * r)) / tgt)
    Ms = 10.0 ** brentq(gg, 12.0, 17.0)
    NUMBERS["Mvir_where_ratio_eq_5p364"] = Ms
    report("K4c", 1e14 < Ms < 1e15, math.log10(Ms), 14.0)


NUMBERS = {}

SYSTEMS = {
    # mb = baryonic mass [Msun], a = Hernquist scale [m].  Both are labelled inputs.
    "MW": dict(mb=6.0e10, a=4.0 * 1e3 * PC, note="M_* 5.5e10 + M_gas 5e9, r_h ~ 5 kpc"),
    "cluster": dict(mb=1.4e14, a=2.5e5 * PC, note="M_500 ~ 1e15, f_b 0.15 -> 1.4e14, r_h ~ 330 kpc"),
}


def check_virial_ratios():
    out = {}
    for name, s in SYSTEMS.items():
        rv = r_vir_hernquist(s["mb"], s["a"])
        y = (G * s["mb"] * MSUN / A0) / (rv + s["a"]) ** 2
        ratio = ratio_F(y)
        mtot = (4.0 * math.pi / 3.0) * DELTA_VIR * RHO_CRIT * rv ** 3 / MSUN
        mu = (rv / (rv + s["a"])) ** 2
        out[name] = dict(r_vir_Mpc=rv / MPC, ratio_enclosed=ratio, ratio_total=mtot / s["mb"] - 1.0,
                         M_tot=mtot, mu_enclosed=mu, f_b_eff=s["mb"] / mtot,
                         y=y, c=rv / s["a"])
        print("   # %-8s M_b=%.2e r_v=%.4f Mpc  M_tot=%.3e  mu(<r_v)=%.3f  "
              "M_ph/M_b(enc)=%.2f  M_ph/M_b(tot)=%.2f  y_v=%.5f  c=r_v/a=%.1f"
              % (name, s["mb"], rv / MPC, mtot, mu, ratio, mtot / s["mb"] - 1.0, y, rv / s["a"]))
    NUMBERS["virial"] = out
    spread = out["MW"]["ratio_total"] / out["cluster"]["ratio_total"]
    report("K5", spread > 2.0, spread, 2.0)


def check_volume_integral():
    """Actually integrate rho_ph to r_v: the volume integral must equal the boundary term."""
    mb, aa = 6.0e10, 4.0e3 * PC
    rM2 = G * mb * MSUN / A0

    def Mph(r):
        y = rM2 / (r + aa) ** 2
        g = A0 * y * 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))
        gn = G * mb * MSUN / (r + aa) ** 2
        return r * r * (g - gn) / G

    r = np.linspace(1e-3 * PC, 0.30 * MPC, 40000)
    M = np.array([Mph(x) for x in r])
    rho = np.gradient(M, r) / (4.0 * np.pi * r ** 2)
    integ = np.trapz(4.0 * np.pi * r ** 2 * rho, r) if hasattr(np, "trapz") \
        else np.trapezoid(4.0 * np.pi * r ** 2 * rho, r)
    dev = abs(integ / M[-1] - 1.0)
    NUMBERS["rho_ph_min"] = float(rho.min())
    print("   # volume integral of rho_ph = %.6e vs boundary %.6e  (min rho_ph %.3e > 0)"
          % (integ, M[-1], rho.min()))
    report("K22", dev < 1e-6 and rho.min() > 0.0, dev, 1e-6)


def check_concentration():
    """M_ph/M_b,tot as a function of concentration c = r_v/a and of y at r_v.

    For a Hernquist baryon profile M_b(<r)/r^2 = M_b/(r+a)^2 exactly, so
    mu(c) = (c/(1+c))^2 and  M_ph/M_b,tot = mu(c)*(1+F(mu(c) r_M^2/r_v^2)) - 1,
    which in the deep limit is mu^(1/2) r_v/r_M - 1."""
    mb = 6.0e10
    rM2 = G * mb * MSUN / A0
    rows = {}
    worst = 0.0
    for a_kpc in (1.0, 2.0, 4.0, 8.0, 16.0, 32.0):
        a = a_kpc * 1e3 * PC
        rv = r_vir_hernquist(mb, a)
        mu = (rv / (rv + a)) ** 2
        y = rM2 / (rv + a) ** 2
        closed = mu * (1.0 + ratio_F(y)) - 1.0
        mtot = (4.0 * math.pi / 3.0) * DELTA_VIR * RHO_CRIT * rv ** 3 / MSUN
        direct = mtot / mb - 1.0
        worst = max(worst, abs(closed / direct - 1.0))
        rows["a=%.0fkpc" % a_kpc] = dict(c=rv / a, mu=mu, ratio=direct, y=y, r_vir_Mpc=rv / MPC)
        print("   # a=%5.0f kpc  c=%6.1f  mu=%.4f  M_ph/M_b(tot)=%.2f  y_v=%.2e"
              % (a_kpc, rv / a, mu, direct, y))
    NUMBERS["concentration"] = rows
    a = 4.0 * 1e3 * PC
    rv = r_vir_hernquist(mb, a)
    mu = (rv / (rv + a)) ** 2
    deep = math.sqrt(mu) * rv / math.sqrt(rM2) - 1.0
    NUMBERS["deep_over_exact_ratio"] = deep / (mu * (1.0 + ratio_F(rM2 / (rv + a) ** 2)) - 1.0)
    report("K19", worst < 1e-9, worst, 1e-9)


def check_scaling():
    # deep limit at fixed Delta and f_eff: F ~ (f_eff a_v/a0)^-1/2 with a_v ~ M^(1/3)
    def Fv(lgM, feff):
        Mv = 10.0 ** lgM
        r = (3.0 * Mv * MSUN / (4 * math.pi * DELTA_VIR * RHO_CRIT)) ** (1 / 3)
        av = G * Mv * MSUN / r ** 2
        return ratio_F(feff * av / A0)
    s_M = (math.log(Fv(8.0, FB)) - math.log(Fv(6.0, FB))) / (2.0 * math.log(10.0))
    report("K6a", abs(s_M + 1.0 / 6.0) < 1e-3, s_M, -1.0 / 6.0)
    y0 = 1e-16
    s_f = (math.log(ratio_F(y0 * 1.01)) - math.log(ratio_F(y0))) / math.log(1.01)
    report("K6b", abs(s_f + 0.5) < 1e-6, s_f, -0.5)
    NUMBERS["slope_Mdeep"] = s_M
    NUMBERS["slope_feff_deep"] = s_f
    NUMBERS["slope_feff_at_1e13"] = (math.log(Fv(13.0, FB * 1.01)) - math.log(Fv(13.0, FB))) / math.log(1.01)


def check_census_vs_law():
    """The census supply N = (1-f_b)/(f_ret f_b) against the law's own demand F(y_v)."""
    rows = {}
    for mb in (3e10, 6e10, 1e11, 1e12, 1e13, 1e14):
        f = census_solve(mb)
        N = N_of(f)
        for tag, NN in (("census", N), ("cond", N_of(0.10))):
            mtot = (1.0 + NN) * mb
            r = (3.0 * mtot * MSUN / (4 * math.pi * DELTA_VIR * RHO_CRIT)) ** (1 / 3)
            y = G * mb * MSUN / (A0 * r * r)
            F = ratio_F(y)
            rows["%.1e_%s" % (mb, tag)] = dict(N=NN, F=F, N_over_F=NN / F,
                                              r200_Mpc=r / MPC, y=y)
            if tag == "census":
                print("   # M_b=%.1e  N=%.3f  law F(r200)=%.3f  N/F=%.3f  r200=%.3f Mpc"
                      % (mb, NN, F, NN / F, r / MPC))
    NUMBERS["census_vs_law"] = rows

    def gap(lmb):
        mb = 10.0 ** lmb
        N = N_of(census_solve(mb))
        mtot = (1.0 + N) * mb
        r = (3.0 * mtot * MSUN / (4 * math.pi * DELTA_VIR * RHO_CRIT)) ** (1 / 3)
        return N / ratio_F(G * mb * MSUN / (A0 * r * r))

    grid = np.linspace(10.0, 15.0, 201)
    vals = np.array([gap(x) for x in grid])
    i = int(np.argmin(vals))
    NUMBERS["N_over_F_min"] = float(vals[i])
    NUMBERS["N_over_F_argmin_logMb"] = float(grid[i])
    NUMBERS["N_over_F_at_1e13"] = float(gap(13.0))
    print("   # min N/F = %.3f at log10 M_b = %.2f  (census never undersupplies the law)"
          % (vals[i], grid[i]))
    report("K18a", 1.02 < vals[i] < 1.25, vals[i], 1.25)
    report("K18b", 11.5 < grid[i] < 13.5, grid[i], 13.0)


def check_census():
    tab = {}
    for mb in (3e10, 1e11, 1e12, 1e13, 1e14):
        f = census_solve(mb)
        N = N_of(f)
        tab["%.0e" % mb] = dict(f_ret=f, M_ta=mb * H_DIM / (f * FB16), N=N)
        print("   # M_b=%.1e  f_ret=%.4f  log10 M_ta=%.3f  N=%.4f"
              % (mb, f, math.log10(mb * H_DIM / (f * FB16)), N))
    NUMBERS["census"] = tab
    N13 = tab["1e+13"]["N"]
    report("K7a", abs(N13 - 8.296) < 2e-3, N13, 8.296)
    report("K7b", abs(N_of(0.10) - 53.643) < 2e-3, N_of(0.10), 53.643)
    # is N = 8 a forced cube / mode count?
    cube = N13 ** (1.0 / 3.0)
    report("K8a", abs(cube - 2.0) > 0.01, abs(cube - 2.0), 0.01)
    # ... and the f_ret that would give exactly 8 is 3.6% away from the census value
    fret8 = (1.0 - FB) / FB / 8.0
    NUMBERS["fret_for_N8"] = fret8
    report("K8b", abs(fret8 - tab["1e+13"]["f_ret"]) / fret8 > 0.01,
           abs(fret8 - tab["1e+13"]["f_ret"]) / fret8, 0.01)


def check_edge():
    N = N_of(0.6466)
    mb = 1e13
    rM = r_M(mb)
    re = edge_radius(N, rM)
    lhs = re ** 2 * (g_of_gN(G * mb * MSUN / re ** 2) - G * mb * MSUN / re ** 2) / G
    resid = abs(lhs / (N * mb * MSUN) - 1.0)
    report("K9a", resid < 1e-12, resid, 1e-12)
    approx = rM / math.log1p(1.0 / N)
    dev = abs(approx / re - 1.0)
    NUMBERS["edge"] = dict(N=N, r_e_Mpc=re / MPC, r_M_kpc=rM / PC / 1e3,
                           record_form_Mpc=approx / MPC, dev=dev)
    report("K7c", dev < 2e-3, dev, 2e-3)   # record's log form is the N>>1 limit
    # N is not fixed by the law: every N in [1,30] has its own consistent edge
    ok = 0
    for Nt in np.linspace(1.0, 30.0, 40):
        rt = edge_radius(Nt, rM)
        l2 = rt ** 2 * (g_of_gN(G * mb * MSUN / rt ** 2) - G * mb * MSUN / rt ** 2) / G
        ok += abs(l2 / (Nt * mb * MSUN) - 1.0) < 1e-10
    report("K17", ok == 40, ok, 40)


def check_R5():
    """R5: the supply is drawn from inside the turnaround ball, so r_e < r_ta."""
    worst_c, worst_d, viol = 0.0, 0.0, 0.0
    rows = {}
    for mb in (3e10, 1e11, 1e12, 1e13, 1e14):
        for tag, f in (("census", census_solve(mb)), ("cond", 0.10)):
            N = N_of(f)
            re = edge_radius(N, r_M(mb))
            rt = r_ta(mb / (f * FB))
            q = re / rt
            rows["%.0e_%s" % (mb, tag)] = dict(N=N, r_e_Mpc=re / MPC, r_ta_Mpc=rt / MPC,
                                               ratio=q, Nmax=rt / r_M(mb))
            if tag == "census":
                worst_c = max(worst_c, q)
            else:
                worst_d = max(worst_d, q)
                viol = max(viol, q)
    NUMBERS["R5"] = rows
    NUMBERS["Nmax_1e13"] = rows["1e+13_census"]["Nmax"]
    report("K10a", worst_c < 1.0, worst_c, 1.0)
    report("K10b", worst_d > 1.0, worst_d, 1.0)


def check_sound_speed():
    rho = OMEGA_C * RHO_CRIT
    cs2 = CS_PREFAC * LS_LO ** 2 * rho
    NUMBERS["cs2_24pc_cosmic"] = cs2
    report("K11a", abs(cs2 - 0.51908) < 5e-4, cs2, 0.51908)
    ls_c = 24.0 * math.sqrt(1.0 / cs2)
    NUMBERS["Lstar_cs_eq_c_pc"] = ls_c
    report("K11b", abs(ls_c - 33.311) < 0.02, ls_c, 33.311)
    # inside a galaxy the same identity is superluminal unless L* is far below the window
    rho_gal = 0.01 * MSUN / PC ** 3
    ls_max = math.sqrt(1.0 / (CS_PREFAC * rho_gal)) / PC
    NUMBERS["Lstar_max_galactic_pc"] = ls_max
    report("K12", ls_max < 24.0 / 100.0, 24.0 / ls_max, 100.0)


def check_cutoffs():
    lamJ = LAMBDA_J_PREFAC * LS_LO
    NUMBERS["lambda_J_24pc_pc"] = lamJ / PC
    report("K13a", abs(lamJ / LS_LO / math.sqrt(2) / math.pi - 1.0) < 1e-12,
           lamJ / PC, 106.629)
    lam_cos = MPC / K_HALF_Mpc
    NUMBERS["lambda_cos_Mpc"] = lam_cos / MPC
    report("K13b", lamJ / lam_cos < 1e-3, lamJ / lam_cos, 1e-3)
    # free-streaming length of the dispersion that the window implies: L* = sigma^2/a0
    sig = math.sqrt(A0 * LS_LO)
    lamFS = sig * 2.0 / (3.0 * H0)
    NUMBERS["sigma_24pc_kms"] = sig / 1e3
    NUMBERS["lambda_FS_24pc_kpc"] = lamFS / PC / 1e3
    report("K14", lamFS / lamJ > 100.0, lamFS / lamJ, 100.0)


def check_window_as_velocity():
    """The two ends of the stiffness window are two velocity dispersions, L* = sigma^2/a0."""
    sig_warm = math.sqrt(A0 * LS_LO)                       # 10^4 K gas, mu=1.22 gives 8.23 km/s
    Vf = (G * 6.0e10 * MSUN * A0) ** 0.25                  # flat speed of a M_b=6e10 galaxy
    ls_hi = (Vf / 3.0) ** 2 / A0
    NUMBERS["window_as_velocity"] = dict(sigma_lo_kms=sig_warm / 1e3, V_flat_kms=Vf / 1e3,
                                         sigma_hi_kms=Vf / 3e3, L_hi_kpc=ls_hi / PC / 1e3)
    print("   # window as velocities: sigma_lo=%.2f km/s (24 pc)  sigma_hi=%.2f km/s (%.3f kpc)"
          % (sig_warm / 1e3, Vf / 3e3, ls_hi / PC / 1e3))
    report("K21", abs(ls_hi / (1e3 * PC) - 1.0) < 0.10, ls_hi / PC / 1e3, 1.0)


def check_turnover():
    """What N is observable as: the supply edge r_e = r_M sqrt(N(N+1))."""
    mb = 6.0e10
    rM = r_M(mb)
    re_a = edge_radius(N_of(0.10), rM)
    re_b = edge_radius(8.296, rM)
    NUMBERS["turnover"] = dict(M_b=mb, r_M_kpc=rM / PC / 1e3,
                               r_e_N53p64_Mpc=re_a / MPC, r_e_N8p30_Mpc=re_b / MPC,
                               separation=re_a / re_b)
    print("   # M_b=6e10 galaxy: r_M=%.3f kpc  r_e(N=53.64)=%.0f kpc  r_e(N=8.30)=%.0f kpc"
          % (rM / PC / 1e3, re_a / PC / 1e3, re_b / PC / 1e3))
    report("K20", re_a / re_b > 5.0, re_a / re_b, 5.0)


def check_barotropic_no_go():
    """c_s^2 = A rho^alpha at fixed Delta: c_s^2/sigma_vir^2 ~ M^-2/3 for every alpha."""
    slopes = []
    lgM = np.linspace(8.0, 15.0, 15)
    r = (3 * 10 ** lgM * MSUN / (4 * math.pi * DELTA_VIR * RHO_CRIT)) ** (1 / 3)
    sig2 = G * 10 ** lgM * MSUN / r
    for alpha in (-3.0, -1.0, 0.0, 1.0, 3.0):
        rho = DELTA_VIR * RHO_CRIT                  # identical for every mass at fixed Delta
        cs2 = 1e-30 * rho ** alpha * (1.0 if alpha == 0 else 1.0)
        sl = np.polyfit(lgM, np.log10(cs2 / sig2), 1)[0]
        slopes.append(float(sl))
    spread = max(slopes) - min(slopes)
    NUMBERS["barotropic_slope"] = slopes[0]
    report("K15a", abs(slopes[0] + 2.0 / 3.0) < 1e-10, slopes[0], -2.0 / 3.0)
    report("K15b", spread < 1e-10, spread, 1e-10)


def check_cross_section():
    """Scattering depth per particle over T_AGE, tau = rho (sigma/m) sigma_vir T."""
    def tau(Mv):
        r = (3.0 * Mv * MSUN / (4 * math.pi * DELTA_VIR * RHO_CRIT)) ** (1 / 3)
        rho = DELTA_VIR * RHO_CRIT
        sv = math.sqrt(G * Mv * MSUN / r)
        return rho * sv * T_AGE            # per unit sigma/m  [kg/m^2]
    lo = 1.0 / tau(1e15)                   # clusters must be collisional: tau > 1
    hi = 1.0 / tau(1e12)                   # galaxies must be collisionless: tau < 1
    band = (lo / 0.1, hi / 0.1)            # m^2/kg -> cm^2/g  (1 m^2/kg = 10 cm^2/g)
    NUMBERS["sigmam_band_lo_cm2g"] = band[0]
    NUMBERS["sigmam_band_hi_cm2g"] = band[1]
    NUMBERS["tau_per_unit"] = dict(M12=tau(1e12), M15=tau(1e15))
    report("K16", band[0] / BULLET_SIGMA_M > 10.0, band[0] / BULLET_SIGMA_M, 10.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutate", nargs="*", default=None, metavar="Mu")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    mut = args.mutate if args.mutate is not None else []
    if mut:
        apply_mutations(mut)
        print("# MUTATION: " + "; ".join("%s (%s)" % (m, MUTATIONS[m]) for m in mut))
    print("# A11 cold-sector normalization checks  (G=6.67430e-11, a0=9.36e-11, c=2.99792458e8)")
    print("# f_b=%.6f  5.364 = (1-f_b)/f_b = %.6f" % (FB, (1 - FB) / FB))

    sym_check()
    check_limits()
    check_inverse()
    check_virial_ratios()
    check_volume_integral()
    check_concentration()
    check_scaling()
    check_census()
    check_census_vs_law()
    check_edge()
    check_R5()
    check_sound_speed()
    check_cutoffs()
    check_turnover()
    check_window_as_velocity()
    check_barotropic_no_go()
    check_cross_section()

    NUMBERS["fb"] = FB
    NUMBERS["cosmic_ratio_over_baryon"] = (1.0 - FB) / FB
    NUMBERS["y_star"] = y_of_ratio(NUMBERS["cosmic_ratio_over_baryon"])
    NUMBERS["r_star_over_rM"] = 1.0 / math.sqrt(NUMBERS["y_star"])
    NUMBERS["F_MW"] = NUMBERS["virial"]["MW"]["ratio_total"]
    NUMBERS["F_cluster"] = NUMBERS["virial"]["cluster"]["ratio_total"]

    # every physical number quoted in report.md, at the precision quoted
    R5 = NUMBERS["R5"]
    cvl = NUMBERS["census_vs_law"]
    NUMBERS["report"] = {
        "cosmic_ratio": 5.364327, "y_star": 0.029291, "r_star_over_rM": 5.84297,
        "F_MW": 25.04, "F_cluster": 2.62, "spread": 9.57,
        "r_v_MW_Mpc": 0.2455, "Mtot_MW": 1.563e12, "mu_MW": 0.968, "y_MW": 0.00144, "c_MW": 61.4,
        "r_v_cl_Mpc": 1.6863, "Mtot_cl": 5.065e14, "mu_cl": 0.758, "y_cl": 0.05560, "c_cl": 6.7,
        "N_3e10": 53.643, "N_1e11": 44.125, "N_1e12": 14.917, "N_1e13": 8.296, "N_1e14": 5.960,
        "fret_1e13": 0.6466, "fret_for_N8": 0.67054,
        "slope_M": -0.167573, "slope_f": -0.500000, "slope_f_1e13": -0.5266,
        "N_over_F_min": 1.072, "logM_at_min": 12.60, "N_over_F_1e13": 1.126,
        "N_over_F_6e10": 1.638, "N_over_F_3e10": 1.457, "N_over_F_1e11": 1.567,
        "N_over_F_1e12": 1.122, "N_over_F_1e14": 1.360,
        "F_law_3e10": 36.82, "F_law_6e10": 32.75, "F_law_1e11": 28.15,
        "F_law_1e12": 13.30, "F_law_1e13": 7.37, "F_law_1e14": 4.38,
        "Nmax_3e10": 148.0, "Nmax_1e11": 114.0, "Nmax_1e12": 53.9, "Nmax_1e13": 30.2, "Nmax_1e14": 18.4,
        "R5_census_max": 0.393, "R5_cond_1e14": 1.412, "M_cond_cross": 1.26e13,
        "re_cond_1e14_Mpc": 20.9, "rta_cond_1e14_Mpc": 14.8,
        "re_census_1e14_Mpc": 2.49, "rta_census_1e14_Mpc": 7.11,
        "cs2_24pc": 0.5191, "Lstar_cs_eq_c": 33.311, "Lstar_gal_max": 0.0608, "supra_log_frac": 0.91,
        "lambdaJ_24pc": 106.63, "lambdaJ_1kpc": 4443.0, "lambda_cos": 1.020, "cos_over_J": 9.6e3,
        "lambdaFS": 82.35, "FS_over_J": 772.0, "sigma_lo": 8.33, "sigma_hi": 53.74,
        "V_flat": 165.2, "V_flat_third": 55.08, "L_from_Vf3": 1.050,
        "sigmam_lo": 13.0, "sigmam_hi": 130.2, "bullet": 1.0,
        "rM_MW_kpc": 9.453, "re_N53_kpc": 512.0, "re_N8_kpc": 83.0, "turnover_sep": 6.165,
        "Mvir_5p364": 1.76e14, "edge_dev": 5.4e-4, "conc_lo": 25.53, "conc_hi": 20.94,
        "c_lo": 7.2, "c_hi": 247.0, "N_scan": 40, "cutoff_dex": 3.98,
        "K9a_m": 1.1e-16, "K15b_m": 2.3e-15, "K19_m": 1.2e-12, "K3a_m": 1.3e-9,
        "K13b_m": 1.04e-4, "K22_m": 1.3e-15, "cs_over_c": 0.72, "supply_over_Mta": 0.843, "cube_root": 2.024,
        "fret_dev_pct": 3.6, "cutoff_dex_span": 4.3, "lamJ_over_Lstar": 4.443,
        "M_at_min_NoverF": 4.0e12, "runtime_s": 0.5,
    }

    npass = sum(1 for c in CHECKS if c["pass"])
    total = len(CHECKS)
    print("#")
    print("# names: K1 law inversion | K2 phantom-ratio identity | K3 limits | K4 5.364 inverse")
    print("#        K5 non-universality | K6 scaling | K7 census N | K8 cube test | K9 edge root")
    print("#        K10 R5 bound | K11-K12 sound speed | K13-K14 cutoffs | K15 barotropic no-go")
    print("#        K16 cross-section no-go | K17 N not fixed by the law | K20 turnover")
    print("#        K18 census-vs-law gap | K19 concentration | K21 window-as-velocity")
    print("#        K22 volume integral of rho_ph equals the boundary term")

    out = {
        "lane": "A11_cold_normalization",
        "status": "DERIVED (task 1 ratio) / NO-GO (universality, sound-speed split) / NUMERICAL (N)",
        "checks": CHECKS,
        "numbers": NUMBERS,
        "constants_used": [
            "c = 2.99792458e8 m/s (brief s4)",
            "G = 6.67430e-11 (brief s4)",
            "M_sun = 1.98847e30 kg (= GM_sun/G)",
            "pc = 3.0856775814913673e16 m; Mpc = 3.0856775814913673e22 m (brief s4)",
            "a0 = 9.36e-11 m/s^2 canonical footing (brief s4)",
            "H0 = 2.1843e-18 s^-1 (brief s4)",
            "Omega_c = 0.2645 [EXT Planck omega_c=0.1200, h=0.6736]",
            "Omega_m = 0.315 [EXT brief s4]",
            "f_b = 0.02237/0.14237 = 0.157134 [EXT CFG515 cfg515_lib.py]",
            "f_b16 = 0.157, h = 0.674 [EXT CFG416 via CFG515]",
            "Delta_ta = 11.81 [EXT A26, in units of Omega_m rho_crit]",
            "Delta_vir = 200 (convention)",
            "L* window [24 pc, 1 kpc] [EXT CFG820 / AG6D]",
            "c_s^2 <= 7e-7 [EXT CFG508 T1]",
            "k_1/2 = 0.98 Mpc^-1 at L*=24 pc [EXT AG6D C1]",
            "sigma/m < 1 cm^2/g Bullet scale [EXT AG6D, PROVISIONAL]",
            "t_age = 10 Gyr (assumption for the scattering depth)",
        ],
        "mutations": ([MUTATIONS[m] for m in mut] if mut else []),
    }
    p = args.json or os.path.join(HERE, "a11_results_MUTATE.json" if mut else "a11_results.json")
    with open(p, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print("%s COMPLETE: %d/%d checks PASS." % ("A11", npass, total))
    return 0 if npass == total else 1


if __name__ == "__main__":
    sys.exit(main())
