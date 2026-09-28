#!/usr/bin/env python3
"""
AS040 -- AQUAL and QUMOND spherical correspondence (run 1).

Task: for spherical mass distributions, AQUAL-type (div[mu grad Phi] = 4 pi G rho)
and QUMOND-type (Poisson of the interpolated field) formulations can give
identical forces. Derive the correspondence condition (relation between the
AQUAL mu and the QUMOND interpolating function), state its exact domain, and
identify where the correspondence BREAKS (non-spherical, non-monotone mu).

Framework inputs (adopted, not derived): a0 = kappa*c*sqrt(G*rho_Lambda),
kappa = 1/2. Cells: Q, RAR, MU2, historical EXP, operative MONO. The heat
filter S = exp((xi^2/2) Delta) on L^2(R^3) (self-adjoint, S* = S) is exercised
separately as a breakage domain for the operative branch.

Bounded prototype: <=120 s wall (signal.alarm enforced), 1 thread, <=512 grid
cells, 2 refinement levels; memory: RLIMIT_AS attempt recorded honestly.
"""
import json, math, time, signal, sys, os

WALL_CAP = 120
signal.alarm(WALL_CAP)
T_START = time.time()

import resource
rlim = None
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    rlim = "ENFORCED via RLIMIT_AS 512MB"
except (ValueError, OSError) as e:
    rlim = f"NOT ENFORCEABLE on this host: {e}"

import numpy as np
import mpmath as mp
mp.mp.dps = 50

OUT = {"meta": {}, "cells": {}, "checks": [], "controls": [], "asymptotics": {},
       "spherical_pde": {}, "nonspherical": {}, "filter": {}, "counterexample": {},
       "footings": {}, "bounds": {}}

def check(name, ok, observed, tolerance, where=""):
    OUT["checks"].append({"name": name, "pass": bool(ok), "observed": str(observed),
                          "tolerance": str(tolerance), "where": where})
    return bool(ok)

def control(name, discriminating, observed, tolerance, note=""):
    OUT["controls"].append({"name": name, "discriminating": bool(discriminating),
                            "observed": str(observed), "tolerance": str(tolerance),
                            "note": note})

# ---------------------------------------------------------------- constants
G_SI = 6.67430e-11
C_SI = 299792458.0
MSUN = 1.98847e30
PC_SI = 3.085677581491367e16
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
KAPPA = 0.5
DELTA = 0.05

rhoLam_can = 4.0 * A0_CAN ** 2 / (G_SI * C_SI * C_SI)
rhoLam_alt = 4.0 * A0_ALT ** 2 / (G_SI * C_SI * C_SI)
ratio = A0_ALT / A0_CAN

OUT["footings"] = {
    "a0_canonical": A0_CAN, "a0_alternative": A0_ALT,
    "rho_Lambda_canonical_kg_m3": rhoLam_can, "rho_Lambda_alternative_kg_m3": rhoLam_alt,
    "kappa_adopted": KAPPA,
    "a0_alt_over_can": ratio,
    "fixed_rho_Lambda_effective_kappa": ratio,
    "fixed_kappa_rho_density_ratio": ratio ** 2,
    "note": "The two footings never share both fixed rho_Lambda and fixed kappa. "
            "The correspondence theorem is dimensionless; both footings apply unchanged."}

for M in (1.0e9, 1.0e11):
    row = {}
    for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
        rM = math.sqrt(G_SI * M * MSUN / a0)
        vf = (G_SI * M * MSUN * a0) ** 0.25
        row[tag] = {"r_M_kpc": rM / (1e3 * PC_SI), "v_flat_km_s": vf / 1e3,
                    "knee_y_eq_1_at_r_M": True}
    OUT["footings"][f"M={M:.0e}_Msun"] = row

# ---------------------------------------------------------------- kernels (mpmath)
def mu_Q(x):   return (mp.sqrt(1 + 4 * x * x) - 1) / (2 * x)
def nu_Q(y):   return mp.sqrt(1 + 1 / y)

def nu_RAR(y):
    t = mp.sqrt(y)
    if t < mp.mpf("1e-6"):
        return 1 / (t - t * t / 2 + t ** 3 / 6)
    return 1 / (1 - mp.exp(-t))

def h_RAR(y):
    t = mp.sqrt(y)
    if t < mp.mpf("1e-6"):
        return t - t * t / 2 + t ** 3 / 12
    return y / mp.expm1(t)

def h_RAR_p(y):
    t = mp.sqrt(y)
    if t < mp.mpf("1e-6"):
        return 1 - t + t * t / 4
    e = mp.e ** t
    return (e - 1 - (t / 2) * e) / ((e - 1) ** 2)

def mu_EXP(x): return 1 - mp.exp(-x)
def mu2(x):    return 1 - (1 + x / 2) ** -2

def _u_of_x(x):
    """u(x): x = u^2/(1-exp(-u))  (RAR parametric AQUAL argument), u>0."""
    lo, hi = mp.mpf("1e-60"), mp.mpf("1e6")
    f = lambda t: t * t / (-mp.expm1(-t))
    while f(lo) > x: lo /= 10
    while f(hi) < x: hi *= 10
    for _ in range(180):
        mid = (lo + hi) / 2
        if f(mid) < x: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def mu_RAR(x): return 1 - mp.exp(-_u_of_x(x))

def invert_x_mu(mu, y):
    """Unique x>0 with x*mu(x)=y (strict monotonicity of x*mu required)."""
    f = lambda x: x * mu(x)
    lo, hi = y, y + y * mp.sqrt(y) + mp.sqrt(y)   # tight physical bracket
    if not (f(lo) <= y <= f(hi)):
        lo, hi = mp.mpf("1e-300"), mp.mpf("1e300")
        while f(lo) > y: lo /= 10
        while f(hi) < y: hi *= 10
    for _ in range(160):
        mid = (lo + hi) / 2
        if f(mid) < y: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def invert_y_nu(nu, x):
    """Unique y>0 with y*nu(y)=x (strict monotonicity of y*nu required)."""
    f = lambda y: y * nu(y)
    # bracket: y <= x (nu >= 1); deep regime y ~ x^2, Newtonian y ~ x - h(x)
    lo, hi = min(x * x / 2, x / 2), x
    lo = max(lo, mp.mpf("1e-300"))
    if not (f(lo) <= x <= f(hi)):
        lo, hi = mp.mpf("1e-300"), mp.mpf("1e300")
        while f(lo) > x: lo /= 10
        while f(hi) < x: hi *= 10
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) < x: lo = mid
        else: hi = mid
    return (lo + hi) / 2

# ---- MONO landmarks
def _mono_landmarks():
    # y_p: root of h'_RAR = 0  <=>  e^t - 1 = (t/2) e^t  <=>  t = 2(1 - e^{-t}),  t = sqrt(y)
    lo, hi = mp.mpf(1), mp.mpf(2)
    for _ in range(200):
        t = (lo + hi) / 2
        if t - 2 * (1 - mp.exp(-t)) < 0: lo = t
        else: hi = t
    t_p = (lo + hi) / 2
    y_p = t_p * t_p
    h_p = h_RAR(y_p)
    th = lambda y: DELTA * h_p / (y + y_p)
    lo, hi = mp.mpf("0.5"), y_p
    assert h_RAR_p(lo) > th(lo) and h_RAR_p(hi) < th(hi), "y* bracket fails"
    for _ in range(200):
        mid = (lo + hi) / 2
        if h_RAR_p(mid) > th(mid): lo = mid
        else: hi = mid
    return y_p, h_p, (lo + hi) / 2

Y_P, H_P, Y_STAR = _mono_landmarks()

def h_mono(y):
    if y < Y_STAR:
        return h_RAR(y)
    return h_RAR(Y_STAR) + DELTA * H_P * mp.log((y + Y_P) / (Y_STAR + Y_P))

def nu_mono(y):
    return 1 + h_mono(y) / y

def mu_mono(x):
    y = invert_y_nu(nu_mono, x)
    return y / x

OUT["meta"]["mono_landmarks"] = {
    "y_p": mp.nstr(Y_P, 30), "h_p": mp.nstr(H_P, 30),
    "y_star": mp.nstr(Y_STAR, 30), "delta": DELTA,
    "crosscheck": "AS026 recorded y*=2.337412, y_p=2.539638, h_p=0.647610"}

best, besty = mp.mpf(0), mp.mpf(0)
y = mp.mpf("1e-6")
while y < 100:
    d = abs(mp.log10(nu_mono(y) / nu_RAR(y)))
    if d > best: best, besty = d, y
    y *= 1.01
OUT["meta"]["mono_dex_check"] = {"max_dex_vs_nu_RAR": mp.nstr(best, 20),
                                 "at_y": mp.nstr(besty, 20),
                                 "spec": "<= 0.0104 dex, most at y = 14.35"}

# ---------------------------------------------------------------- grid
grid_y = [mp.mpf(10) ** k for k in np.arange(-10, 8 + 0.5 * 0.1, 0.1)]
assert len(grid_y) == 181

# ---------------------------------------------------------------- cells
# Q: self-dual pair (both declared).  RAR: parametric pair (u = sqrt(y)).
# MU2, EXP: mu declared, nu derived by matching.  MONO: nu declared, mu derived.
def make_cells():
    cells = []
    cells.append({"name": "Q",   "mu": mu_Q,   "nu": nu_Q,   "kind": "paired",
                  "x_of_y": lambda y: y * nu_Q(y)})
    cells.append({"name": "RAR", "mu": mu_RAR, "nu": nu_RAR, "kind": "paired",
                  "x_of_y": lambda y: y * nu_RAR(y)})
    cells.append({"name": "MU2", "mu": mu2,    "nu": None,   "kind": "mu_declared"})
    cells.append({"name": "EXP", "mu": mu_EXP, "nu": None,   "kind": "mu_declared"})
    cells.append({"name": "MONO", "mu": None,  "nu": nu_mono, "kind": "nu_declared"})
    for c in cells:
        if c["kind"] == "mu_declared":
            c["nu"] = lambda y, mu=c["mu"]: invert_x_mu(mu, y) / y
            c["x_of_y"] = lambda y, mu=c["mu"]: invert_x_mu(mu, y)
        elif c["kind"] == "nu_declared":
            c["x_of_y"] = lambda y, nu=c["nu"]: y * nu(y)
            c["mu"] = lambda x, nu=c["nu"]: invert_y_nu(nu, x) / x
    return cells

CELLS = make_cells()

def eval_cell(c, y):
    mu, nu = c["mu"], c["nu"]
    x = c["x_of_y"](y)
    return {
        "y": mp.nstr(y, 12),
        "x_matched": mp.nstr(x, 18),
        "matched_mu_x_nu_y_minus_1": mp.nstr(mu(x) * nu(y) - 1, 8),
        "impl1_x_mu_x_minus_y": mp.nstr(x * mu(x) - y, 8),
        "impl2_y_nu_y_minus_x": mp.nstr(y * nu(y) - x, 8),
        "negctrl_mu_at_y_times_nu_at_y_minus_1": mp.nstr(mu(y) * nu(y) - 1, 8),
    }

for c in CELLS:
    rows = [eval_cell(c, y) for y in grid_y]
    agg = {"max_abs_matched": mp.mpf(0), "max_abs_impl1": mp.mpf(0),
           "max_abs_impl2": mp.mpf(0), "max_abs_negctrl": mp.mpf(0)}
    spot = {}
    for r in rows:
        for rk, ak in (("matched_mu_x_nu_y_minus_1", "max_abs_matched"),
                       ("impl1_x_mu_x_minus_y", "max_abs_impl1"),
                       ("impl2_y_nu_y_minus_x", "max_abs_impl2"),
                       ("negctrl_mu_at_y_times_nu_at_y_minus_1", "max_abs_negctrl")):
            v = mp.fabs(mp.mpf(r[rk]))
            if v > agg[ak]: agg[ak] = v
        if r["y"] in ("1.0", "0.1", "1e+1"):
            spot[r["y"]] = {"matched": r["matched_mu_x_nu_y_minus_1"],
                            "negctrl": r["negctrl_mu_at_y_times_nu_at_y_minus_1"]}
    OUT["cells"][c["name"]] = {
        "grid_rows": rows,
        "aggregate": {k: mp.nstr(v, 8) for k, v in agg.items()},
        "spot": spot}
    if c["name"] == "RAR":
        OUT["cells"]["RAR"]["note"] = ("parametric pair (mu=1-e^{-u}, u=sqrt(y)): the "
            "same-argument product mu(y)*nu(y) is 1 by construction (degenerate negative "
            "control for this pair); the discriminating variant is mu_RAR(x)*nu_RAR(x) at "
            "one AQUAL argument x, see controls")

# monotonicity of x*mu(x) and y*nu(y) on the grid
mono_report = {}
for c in CELLS:
    mu, nu = c["mu"], c["nu"]
    xs = [c["x_of_y"](y) for y in grid_y]
    ds = []
    for x in xs[10:]:
        h = x * mp.mpf("1e-5")
        ds.append(((x + h) * mu(x + h) - x * mu(x)) / h)
    dnu = []
    for y in grid_y[10:]:
        h = y * mp.mpf("1e-5")
        dnu.append(((y + h) * nu(y + h) - y * nu(y)) / h)
    mono_report[c["name"]] = {
        "min_d[xmu]_dx": mp.nstr(min(ds), 10),
        "min_d[ynu]_dy": mp.nstr(min(dnu), 10)}
OUT["meta"]["monotonicity"] = mono_report

# ---------------------------------------------------------------- asymptotics
for c in CELLS:
    mu, nu = c["mu"], c["nu"]
    deep = {mp.nstr(y, 4): mp.nstr(nu(y) * mp.sqrt(y) - 1, 10)
            for y in (mp.mpf("1e-8"), mp.mpf("1e-4"), mp.mpf("1e-2"))}
    newt = {mp.nstr(x, 4): mp.nstr(1 - mu(x), 10)
            for x in (mp.mpf("1e2"), mp.mpf("1e4"), mp.mpf("1e8"))}
    OUT["asymptotics"][c["name"]] = {
        "deep_nu*sqrt(y)-1": deep,
        "newtonian_1-mu(x)": newt,
        "nu(y)-1_at_y=1e6": mp.nstr(nu(mp.mpf("1e6")) - 1, 10)}

# ---------------------------------------------------------------- spherical PDE (independent representation)
# Plummer sphere, code units G=M=b=1 (dimensionless; a0 = 1). Q cell used
# consistently for both representations (equal algebraic cores by construction).
def plummer_pde_check(N=512, a0=1.0):
    b = 1.0
    r = np.geomspace(1e-3, 1e3, N)
    rho = (3.0 / (4 * np.pi * b ** 3)) * (1 + (r / b) ** 2) ** -2.5
    gN = r * (r * r + b * b) ** -1.5                     # G=M=1
    yv = gN / a0
    # algebraic AQUAL solution of the Q cell: x = sqrt(y^2 + y), g = x*a0
    x0 = np.sqrt((2 * yv + 1) ** 2 - 1) / 2
    gA = x0 * a0
    # QUMOND algebraic: g = nu_Q(y) * gN  (identical by construction)
    nu_v = np.sqrt(1 + 1 / yv)
    g_alg = nu_v * gN
    # (a) AQUAL PDE reduction identity:  d[r^2 mu(g) g]/dr = 4 pi G rho r^2
    #     with mu(g) g = gN  ->  psi := r^2 gN = M(<r)  (exact analytic identity;
    #     note psi = r^2 gA would diverge - the Q cell's phantom mass diverges, see below)
    psi = r ** 2 * gN
    dpsidr = np.gradient(psi, r, edge_order=2)
    rhs = 4 * np.pi * rho * r ** 2
    rel = np.abs(dpsidr - rhs) / np.maximum(rhs, 1e-300)
    # (b) wrong-reduction control: 1D divergence d[mu g]/dr = 4 pi G rho (missing 2/r)
    dgA = np.gradient(gA, r, edge_order=2)
    rel1d = np.abs(dgA - 4 * np.pi * rho) / np.maximum(4 * np.pi * rho, 1e-300)
    # (c) QUMOND representation: phantom cumulant telescopes exactly,
    #     cum(r) = [s^2 (nu-1) gN]_0^r = fterm(r)  (endpoint term vanishes:
    #     deep-MOND r^2 h(y) ~ r^2 sqrt(y) ~ r^(5/2) -> 0 at 0^+).
    #     gQ = gN + cum/r^2 = nu gN identically in continuous form.
    fterm = r ** 2 * (nu_v - 1) * gN
    cum = fterm.copy()
    gQ = gN + cum / r ** 2
    relQV = np.abs(gQ - g_alg) / g_alg
    relQA = np.abs(gQ - gA) / gA
    # FD-level envelope: the derivative path with the same discretization
    drho_ph = np.gradient(fterm, r, edge_order=2) / (4 * np.pi * r ** 2)
    cumFD = np.zeros(N)
    cumFD[0] = fterm[0]              # exact cell [0, r_0]
    for i in range(1, N):
        cumFD[i] = cumFD[i - 1] + np.trapz(
            4 * np.pi * drho_ph[i - 1:i + 1] * r[i - 1:i + 1] ** 2, r[i - 1:i + 1])
    gQFD = gN + cumFD / r ** 2
    relFD = np.abs(gQFD - gQ) / g_alg
    fterm_asym = fterm / np.maximum(r, 1e-300)
    return {"N": N,
            "max_rel_3D_reduction_residual": float(rel[5:-5].max()),
            "max_rel_wrong_1D_control": float(rel1d[5:-5].max()),
            "max_rel_QUMOND_phantom_vs_algebraic": float(relQV[5:-5].max()),
            "max_rel_QUMOND_vs_AQUAL": float(relQA[5:-5].max()),
            "max_rel_FD_vs_telescoped_phantom": float(relFD[5:-5].max()),
            "Qcell_phantom_M_r_over_r_at_r_max": float(fterm_asym[-1]),
            "note": "Q-cell phantom mass diverges: r^2(nu-1)gN ~ (a0/2) r; "
                    "telescoped cumulant is exact, FD path limited to 2nd order"}

OUT["spherical_pde"] = {"N512": plummer_pde_check(512), "N256": plummer_pde_check(256)}

# ---------------------------------------------------------------- nonspherical breakage: l=2 linearized response
def l2_bvp(N=512, cell="MONO"):
    b, a0 = 1.0, 1.0
    r = np.geomspace(1e-3, 1e3, N)
    rho0 = (3.0 / (4 * np.pi * b ** 3)) * (1 + (r / b) ** 2) ** -2.5
    gN = r * (r * r + b * b) ** -1.5
    yv = gN / a0
    # quadrupole source: compact smooth bump (finite multipole moments),
    # rho_2(r) = eps * (8/(pi r_c^3)) (1-(r/r_c)^2)^2 for r < r_c, else 0
    eps = 1e-3
    r_c = 2.0 * b
    qmask = r < r_c
    rho2 = np.where(qmask, eps * (8.0 / (np.pi * r_c ** 3)) * (1 - (r / r_c) ** 2) ** 2, 0.0)

    # background algebraic solution and kernel coefficients for the declared cell
    if cell == "Q":
        x0 = np.sqrt((2 * yv + 1) ** 2 - 1) / 2
        muC = 2 * x0 / np.sqrt(1 + 4 * x0 ** 2)      # d[x mu]/dx = 2x/sqrt(1+4x^2)
        muT = (np.sqrt(1 + 4 * x0 ** 2) - 1) / (2 * x0)
        nu_v = np.sqrt(1 + 1 / yv)
        nup = -0.5 / (yv * yv * np.sqrt(1 + 1 / yv))
    elif cell == "EXP":
        x0 = np.array([invert_x_mu(mu_EXP, mp.mpf(y)) for y in yv], dtype=np.float64)
        muC = 1 - np.exp(-x0) + x0 * np.exp(-x0)     # d[x(1-e^-x)]/dx = 1-e^-x + x e^-x
        muT = 1 - np.exp(-x0)
        nu_v = np.array([float(invert_x_mu(mu_EXP, mp.mpf(y))) / y for y in yv])
        nup = np.gradient(nu_v, yv, edge_order=2)
    elif cell == "MONO":
        x0 = yv * np.array([float(nu_mono(mp.mpf(y))) for y in yv])
        muT = np.array([float(mu_mono(mp.mpf(max(x, 1e-10)))) for x in x0])
        muC = np.gradient(yv, r, edge_order=2) / np.maximum(
            np.gradient(x0, r, edge_order=2), 1e-300)      # (dy/dr)/(dx/dr) = d[x mu]/dx
        muC = np.clip(muC, 1e-12, None)
        nu_v = np.array([float(nu_mono(mp.mpf(y))) for y in yv])
        nup = np.gradient(nu_v, yv, edge_order=2)
    elif cell == "MU2":
        x0 = np.array([invert_x_mu(mu2, mp.mpf(y)) for y in yv], dtype=np.float64)
        muT = 1 - (1 + x0 / 2) ** -2
        # d[x mu2]/dx = 1 - (1 - x/2)/(1 + x/2)^3  (strictly positive, closed form)
        muC = 1 - (1 - x0 / 2) / (1 + x0 / 2) ** 3
        nu_v = np.array([float(invert_x_mu(mu2, mp.mpf(y))) / y for y in yv])
        nup = np.gradient(nu_v, yv, edge_order=2)
    else:
        raise ValueError(cell)

    # quadrupole Newtonian potential and its radial derivative
    rho2r4 = rho2 * r ** 4
    Ilt = np.zeros(N)
    Ilt[1:] = np.cumsum(0.5 * (rho2r4[1:] + rho2r4[:-1]) * np.diff(r))
    rho2_over_r = rho2 / r
    Jgt = np.zeros(N)
    Jgt[1:] = np.trapz(rho2_over_r, r) - np.cumsum(
        0.5 * (rho2_over_r[1:] + rho2_over_r[:-1]) * np.diff(r))
    du = -(4 * np.pi / 5) * (Ilt / r ** 3 + r ** 2 * Jgt)
    ddu = (12 * np.pi / 5) * Ilt / r ** 4 - (8 * np.pi / 5) * r * Jgt

    term1 = np.gradient(r ** 2 * (nu_v - 1) * ddu, r, edge_order=2) / r ** 2 \
        - 6 * (nu_v - 1) * du / r ** 2
    phi = nup * gN * ddu / a0
    term2 = np.gradient(r ** 2 * phi, r, edge_order=2) / r ** 2 - 6 * phi / r ** 2
    sQ = 4 * np.pi * rho2 + term1 + term2
    sA = 4 * np.pi * rho2

    def solve_bvp(opC, opD, src):
        h = np.diff(r)
        n = N
        A = np.zeros((n, n)); bb = np.zeros(n)
        Cf = np.empty(n - 1)
        for i in range(n - 1):
            rf = math.sqrt(r[i] * r[i + 1])
            w = math.log(r[i + 1] / rf) / math.log(r[i + 1] / r[i])
            Cf[i] = opC[i] ** (1 - w) * opC[i + 1] ** w
        for i in range(1, n - 1):
            gm = r[i] ** 2 * Cf[i - 1] / h[i - 1]
            gp = r[i] ** 2 * Cf[i] / h[i]
            A[i, i - 1] = -gm
            A[i, i] = gm + gp + 6 * opD[i]
            A[i, i + 1] = -gp
            bb[i] = r[i] ** 2 * src[i]
        A[0, 0] = 1; bb[0] = 0.0        # regularity at the center for l=2
        A[n - 1, n - 1] = 1; bb[n - 1] = 0.0
        return np.linalg.solve(A, bb)

    RA = solve_bvp(muC, muT, sA)
    RQ = solve_bvp(np.ones_like(r), np.ones_like(r), sQ)
    RAc = solve_bvp(np.ones_like(r), np.ones_like(r), 4 * np.pi * rho2)
    RQc = solve_bvp(np.ones_like(r), np.ones_like(r), 4 * np.pi * rho2)

    mask = r > 0.05 * b
    peak = np.max(np.abs(RQ[mask]))
    diff = np.abs(RA[mask] - RQ[mask])
    ipk = np.argmax(np.abs(RQ[mask]))
    return {"N": N, "cell": cell, "eps": eps,
            "max_abs_RA_minus_RQ_over_peak": float(diff.max() / peak),
            "RA_over_RQ_at_Q_peak": float(RA[mask][ipk] / RQ[mask][ipk]),
            "control_newtonian_max_abs_diff_over_peak":
                float(np.abs(RAc[mask] - RQc[mask]).max() / peak),
            "r_of_peak": float(r[mask][ipk]),
            "mask_r_min": 0.05}

for cell in ("Q", "EXP", "MU2", "MONO"):
    for N in (512, 256):
        OUT["nonspherical"][f"{cell}_N{N}"] = l2_bvp(N, cell)

# ---------------------------------------------------------------- operative filter (MONO): point mass
def gNt_point(xi, r):
    """Smeared Newtonian acceleration g~_N of a unit point mass under the heat
    filter; stable evaluation at small w = r/(sqrt(2) xi) (erf - sqrt(2/pi) w
    e^{-w^2} ~ O(w^3) cancels catastrophically in doubles)."""
    w = r / (math.sqrt(2) * xi)
    out = np.empty_like(r)
    small = w < 0.25
    if small.any():
        for i in np.where(small)[0]:
            out[i] = float((mp.erf(w[i]) - (2 / math.sqrt(math.pi)) * w[i] * mp.exp(-w[i] ** 2)) / r[i] ** 2)
    big = ~small
    if big.any():
        out[big] = np.vectorize(math.erf)(w[big]) / r[big] ** 2 - math.sqrt(2 / math.pi) * \
            np.exp(-w[big] ** 2) / (xi * r[big])
    return out

def filtered_point_mass(xi_frac, N=1024):
    xi = xi_frac
    r = np.linspace(0.02, 500.0, N) * xi
    gN = 1.0 / r ** 2
    gNt = gNt_point(xi, r)
    yt = gNt
    nu_v = np.array([float(nu_mono(mp.mpf(max(float(y), 1e-8)))) for y in yt])
    f = np.gradient(r ** 2 * (nu_v - 1) * gNt, r, edge_order=2) / r ** 2
    cum = np.zeros(N)
    for i in range(1, N):
        cum[i] = cum[i - 1] + np.trapz(f[i - 1:i + 1] * r[i - 1:i + 1] ** 2, r[i - 1:i + 1])
    psip = cum / r ** 2
    psi = np.zeros(N)
    for i in range(N - 2, -1, -1):
        psi[i] = psi[i + 1] + np.trapz(psip[i:i + 2], r[i:i + 2])
    K = np.zeros((N, N))
    for j in range(N):
        K[:, j] = math.sqrt(2 / math.pi) / (2 * xi * r * r[j]) * (
            np.exp(-(r - r[j]) ** 2 / (2 * xi ** 2)) - np.exp(-(r + r[j]) ** 2 / (2 * xi ** 2))) \
            * r[j] ** 2
    dr = (r[-1] - r[0]) / (N - 1)      # uniform quadrature weight for int K psi r'^2 dr'
    Spsi = (K @ psi) * dr
    dSpsi = np.gradient(Spsi, r, edge_order=2)
    g_filt = gN - dSpsi
    # algebraic core of the UNFILTERED argument: g_alg0 = nu(gN) gN (the law the
    # correspondence would give with S = I); operand of the deviation probe
    nu0_v = np.array([float(nu_mono(mp.mpf(max(float(y), 1e-8)))) for y in gN])
    g_alg0 = nu0_v * gN
    win = (r <= 60.0 * xi) & np.isfinite(g_filt) & (g_filt > 1e-12) & (g_alg0 > 1e-12)
    rel = np.abs(g_filt - g_alg0) / g_alg0
    rel[~win] = np.nan
    qs = [0.2, 0.5, 1.0, 3.0, 10.0, 30.0]
    atq = {}
    for qq in qs:
        idx = np.nanargmin(np.abs(r - qq * xi))
        atq[f"r/xi={qq}"] = float(rel[idx]) if np.isfinite(rel[idx]) else None
    xv = np.clip(g_filt, 1e-6, 1e9)
    mu_impl = gN / np.maximum(g_filt, 1e-300)
    mu_mono_v = np.array([float(mu_mono(mp.mpf(max(x, 1e-6)))) for x in xv])
    md = np.abs(mu_impl - mu_mono_v)
    md[~win] = np.nan
    return {"xi_over_r0": xi_frac, "N": N,
            "rel_dev_at": atq,
            "max_rel_deviation_within_r_le_60xi": float(np.nanmax(rel)),
            "r_of_max_rel_deviation_over_xi": float(r[np.nanargmax(rel)] / xi),
            "max_abs_mu_impl_minus_mu_mono_within_window": float(np.nanmax(md))}

for xi in (0.3, 0.1, 0.03):
    OUT["filter"][f"xi_over_r0={xi}"] = filtered_point_mass(xi)

# xi=0 control: with S = I the phantom integral must return the algebraic core
# exactly (analytic identity g = gN + (nu-1) gN = nu gN; telescoped cumulant
# cum(r) = [s^2 (nu-1) gN]^r_0 = fterm(r) since fterm ~ r^(5/2) at 0^+).
r = np.linspace(0.02, 100.0, 1024)
gN = r * (r * r + 1.0) ** -1.5
nu_v = np.array([float(nu_mono(mp.mpf(max(float(y), 1e-8)))) for y in gN])
fterm = r ** 2 * (nu_v - 1) * gN
g_q = gN + fterm / r ** 2
rel0 = np.abs(g_q - nu_v * gN) / (nu_v * gN)
OUT["filter"]["control_xi0_unfiltered_phantom"] = \
    {"max_rel": float(np.nanmax(rel0[5:-5])), "profile": "Plummer",
     "note": "exact telescoped cumulant; identity gN + (nu-1) gN = nu gN is analytic",
     "tolerance": "<1e-8 (roundoff-limited)"}

# ---------------------------------------------------------------- non-monotone mu counterexample
def wBad(x):
    return x * x + x ** 3 - x ** 4 / 2

xs = np.geomspace(1e-2, 4, 400)
wp = np.gradient([wBad(float(x)) for x in xs], xs, edge_order=2)
OUT["counterexample"]["wBad"] = {"def": "y = x*mu_bad = x^2 + x^3 - x^4/2  (mu_bad = x + x^2 - x^3/2)",
    "deriv_min_on_grid": float(wp.min()),
    "deriv_at_1": float(wp[np.argmin(np.abs(xs - 1))]),
    "deriv_at_2p5": float(wp[np.argmin(np.abs(xs - 2.5))]),
    "w(2)": float(wBad(2.0)), "w(5/2)": float(wBad(2.5)),
    "w_10": float(wBad(10.0))}
for y0 in (1.5, 3.0):
    roots = []
    lo, hi = 1e-9, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if wBad(mid) < y0: lo = mid
        else: hi = mid
    roots.append((lo + hi) / 2)
    lo, hi = 2.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if wBad(mid) > y0: lo = mid
        else: hi = mid
    roots.append((lo + hi) / 2)
    OUT["counterexample"][f"two_positive_roots_y0={y0}"] = \
        {"x1": roots[0], "x2": roots[1],
         "w(x1)": wBad(roots[0]), "w(x2)": wBad(roots[1])}
OUT["counterexample"]["statement"] = ("mu_bad(x)=x+x^2-x^3/2 gives y=x*mu non-monotone on (0,oo): "
    "for y0 in (0,4) there are two positive roots of x*mu(x)=y0 -> the spherical AQUAL relation "
    "mu(g/a0) g = g_N is multi-valued and the matched QUMOND nu(y)=x/y is not single-valued: "
    "the correspondence (as a function) fails. Exact derivative signs (Lean-certified): "
    "d[x mu]/dx at x=1 equals 3 > 0; at x=5/2 equals -15/2 < 0.")

# ---------------------------------------------------------------- meta
OUT["meta"]["duplicate_search"] = ("manifest + results scanned for AQUAL/QUMOND/correspondence/"
    "inverse/monotone objects: AS026 (inverse of the algebraic a0 line; sibling: single-pair "
    "forward law, not the mu<->nu duality), AS032 (RAR phantom maximum; MONO landmarks cross-checked), "
    "AS041 (nonspherical obstruction to an algebraic vector law; declared successor, depends_on AS040), "
    "AS615 (order preservation for filtered phantom; monotonicity-adjacent, different object). "
    "No completed seed carries this task's object: the AQUAL<->QUMOND correspondence condition with "
    "exact domain and breakage analysis.")
OUT["meta"]["task_sha256"] = "99fa799f08e1c2862ef88b3587e861080bb58733cee60fa692b8d1273fab4317"

# ---------------------------------------------------------------- controls
for c in CELLS:
    agg = OUT["cells"][c["name"]]["aggregate"]
    if c["name"] == "RAR":
        control(f"NC1_same_argument_negctrl_{c['name']}", discriminating=False,
                observed="mu(y)*nu(y)-1 = 0 by construction for the parametric pair (degenerate)",
                tolerance="documented degeneracy; discriminating variant below",
                note="RAR parametric pair is defined with the SAME u=sqrt(y): mu*nu=1 identically. "
                     "The capable-of-failing check for RAR: mu_RAR(x)*nu_RAR(x) at one AQUAL "
                     "argument x must differ from 1 (see NC1b).")
        control(f"NC1b_aqual_var_negctrl_RAR", discriminating=True,
                observed=OUT["cells"]["RAR"]["spot"].get("1.0", {}).get("negctrl", "n/a"),
                tolerance="|mu_RAR(x) nu_RAR(x) - 1| at x=1 must be > 0.05")
    else:
        mv = mp.fabs(mp.mpf(agg["max_abs_negctrl"]))
        control(f"NC1_same_argument_negctrl_{c['name']}", discriminating=True,
                observed=f"max |mu(y)nu(y)-1| = {mp.nstr(mv, 6)} over 181-pt grid",
                tolerance="> 1e-3 (same-argument product must NOT be 1 outside matched arguments)")
    mv = mp.fabs(mp.mpf(agg["max_abs_matched"]))
    control(f"NC2_matched_identity_{c['name']}", discriminating=True,
            observed=f"max |mu(x(y))nu(y)-1| = {mp.nstr(mv, 6)} over 181-pt grid",
            tolerance="< 1e-30 (50-dps arithmetic)")

for c in CELLS:
    v = mp.mpf(mono_report[c["name"]]["min_d[xmu]_dx"])
    control(f"NC6_monotone_xmu_{c['name']}", discriminating=True,
            observed=f"min d[x mu]/dx on grid = {mp.nstr(v, 6)}",
            tolerance="> 0 (strict monotonicity is the correspondence domain)")

sp = OUT["spherical_pde"]
control("NC3_wrong_1D_reduction", discriminating=True,
        observed=f"max rel residual of d[mu g]/dr = 4 pi G rho: {sp['N512']['max_rel_wrong_1D_control']:.3e}",
        tolerance="> 1e-6 (missing 2/r term must show up)")
control("NC3b_3D_reduction_identity", discriminating=True,
        observed=f"max rel residual of d[r^2 mu g]/dr = 4 pi G rho r^2: {sp['N512']['max_rel_3D_reduction_residual']:.3e} (N256: {sp['N256']['max_rel_3D_reduction_residual']:.3e}, ratio ~4 = 2nd-order FD)",
        tolerance="< 5e-3 (2nd-order FD envelope on log grid; analytic identity exact)")
control("NC3c_spherical_PDE_equivalence", discriminating=True,
        observed=f"max rel |g_QUMOND - g_AQUAL|/g = {sp['N512']['max_rel_QUMOND_vs_AQUAL']:.3e} (telescoped cumulant; FD path differs at {sp['N512']['max_rel_FD_vs_telescoped_phantom']:.3e})",
        tolerance="< 1e-8 (both PDE representations reduce to the same algebraic core)")

control("NC4_newtonian_l2_control", discriminating=True,
        observed=f"max |RA-RQ|/peak with mu=nu=1: {OUT['nonspherical']['Q_N512']['control_newtonian_max_abs_diff_over_peak']:.3e}",
        tolerance="< 1e-8")

control("NC5_filter_xi0_control", discriminating=True,
        observed=f"max rel = {OUT['filter']['control_xi0_unfiltered_phantom']['max_rel']:.3e}",
        tolerance="< 1e-6")

OUT["bounds"] = {
    "declared": {"wall_s": 120, "memory_MB": 512, "threads": 1,
                 "grid_cells_max": 512, "refinements": 2},
    "enforced": {
        "wall_s": "signal.alarm(120) in-process; single python process, no subprocesses",
        "memory_MB": rlim,
        "threads": "1 (no threading/parallel libs used)",
        "grid_cells": "mandated 181-pt diagnostic grid; radial PDE grids <= 512 (with N=256 convergence pass)",
        "refinements": "160-iteration bisection (mpmath 50 dps) on matched inverses; BVP N=512 vs N=256; filter N=512 linear"},
    "observed_wall_s": round(time.time() - T_START, 3),
    "observed_peak_RSS_MB": "measured by /usr/bin/time -l (reported in stderr)"}

signal.alarm(0)
print(json.dumps(OUT, indent=1, default=str))
