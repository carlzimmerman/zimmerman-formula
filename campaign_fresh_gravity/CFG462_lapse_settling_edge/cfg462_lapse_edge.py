#!/usr/bin/env python3
"""CFG462: does the khronon lapse (CFG373) make a settling cold fluid stop at the edge nu = Omega_m/Omega_b (5.85 r_M)?
Criteria: FROZEN_CRITERIA.md (committed alone first, 16518e951).

kappa = 1/2 is FITTED. Both footings scored separately, never pooled. No dark-matter particle is added: the cold fluid's
MASS is still required and its amount is an input. G9 stands. Offline theory + numerics; no data, no downloads.
This is not "theory closed".

Run:  python3 cfg462_lapse_edge.py                     (writes cfg462.out, cfg462_results.json; exit 0 iff K1-K5 pass)
      CFG462_MUTATE=1 python3 cfg462_lapse_edge.py     (a0 -> 2 a0 inside the lapse; writes *_MUTATE.*; exit 1 iff the
                                                        teeth are detected, as frozen)

Units inside the mechanisms: G = 1, M_b = 1, lengths in r_M(true a0) = sqrt(G M_b/a0_true), so a0_true = 1 and the
mechanisms see a0m = 1 (main) or 2 (MUTATE). Physical units only for the catchment radius and the energy budget.
"""
import os
import sys
import math
import json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.sparse import identity as sp_identity

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C  # noqa: E402  (record constants; nu_mono = FP1's committed kernel, exec'd read-only)

MUT = os.environ.get("CFG462_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg462{TAG}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")


# ======================================================================================================== constants
G, CL, MSUN, KPC = C.G_SI, C.C_SI, C.MSUN, C.KPC
A0 = C.A0                                         # canonical 9.3603e-11, alt 1.1312e-10 (kappa = 1/2 FITTED)
FOOTS = C.FOOTS
SHARE = 5.364                                     # Omega_c/Omega_b (input)
FB = 1.0 / (1.0 + SHARE)                          # 0.157134
S_EDGE = math.log(1.0 / (1.0 - FB))               # 0.170947
Y_E = S_EDGE ** 2                                 # 0.029223
X_EDGE = 1.0 / S_EDGE                             # r_edge / r_M = 5.8498
LOGMB = [9.0, 10.5, 11.5]
S_CAT = 22.6                                      # CFG118: M_ta = 23.6 M_b incl. the core -> cold inside r_ta
RTA_1E9_KPC = 236.0                               # CFG118 z = 0 turnaround radius at M_b = 1e9 (point core), ~ M^(1/3)
A_SCORED, A_REPORTED = 0.3, 1.0                   # Hernquist a / r_M
ALPHA_MIN, ALPHA_MAX = 9.62e-14, 3.2e-9           # L340 window
C2_MIN, C2_MAX = 7.29e-3, 0.0667
A0M = 2.0 if MUT else 1.0                         # a0 seen by the lapse (units of the true a0)
TOL_P1 = 0.05
PRED_SHIFT = math.log10(2 ** -0.5)                # -0.1505 dex
GYR = 3.15576e16
T_H = 13.8 * GYR
H0 = 67.4e3 / (1e3 * KPC)                         # s^-1
OM = 0.315
OL = 1.0 - OM
RHO_CRIT0 = 3 * H0 ** 2 / (8 * math.pi * G)
H_L = H0 * math.sqrt(OL)

R = {"lane": "CFG462", "mutate": MUT, "kappa": "1/2 FITTED", "a0_mech_over_true": A0M, "constants": {
    "f_b": FB, "y_e": Y_E, "x_edge": X_EDGE, "g_tot_edge_over_a0": Y_E / FB, "S_cat": S_CAT, "share": SHARE},
    "controls": {}, "flows": {}}

P("=" * 110)
P(f"CFG462 lapse settling edge   MUTATE={MUT} (a0 inside the lapse = {A0M:g} x true)")
P(f"f_b = {FB:.6f}; y_e = ln^2(1/(1-f_b)) = {Y_E:.6f}; r_edge = {X_EDGE:.4f} r_M; total field at edge {Y_E/FB:.5f} a0")
P(f"supplies: CAT (scored) = {S_CAT} M_b (CFG118 turnaround); SHARE (restatement control) = {SHARE} M_b")
P("=" * 110)


# ======================================================================================================== kernels
def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def nu_mono(y):
    return C.nu_mono(y)


# inverse of x = y nu(y) for nu_mono: monotone table + bracketed bisection refinement
_LY = np.linspace(-12.0, 12.0, 240001)
_LX = np.log10(10 ** _LY * nu_mono(10 ** _LY))
assert np.all(np.diff(_LX) > 0), "y nu_mono(y) must be strictly increasing"


def inv_mono(x):
    x = np.asarray(x, float)
    lx = np.log10(np.maximum(x, 1e-300))
    y0 = 10 ** np.interp(lx, _LX, _LY)
    lo, hi = y0 * (1 - 1e-5), y0 * (1 + 1e-5)
    bad = (lo * nu_mono(lo) > x) | (hi * nu_mono(hi) < x)
    lo = np.where(bad, 1e-12, lo)
    hi = np.where(bad, np.maximum(x, 1e-12) * 1.0000001, hi)
    for _ in range(36 if not np.any(bad) else 140):
        mid = np.sqrt(lo * hi)
        up = mid * nu_mono(mid) > x
        hi = np.where(up, mid, hi)
        lo = np.where(up, lo, mid)
    return np.sqrt(lo * hi)


def inv_p2(x):
    """CFG373's mass-shell inverse g_N = sqrt(g^2 + a_L^2) - a_L, a_L = a0/2, in a0 units (copied)."""
    x = np.asarray(x, float)
    return np.sqrt(x ** 2 + 0.25) - 0.5


KER = {"nu_mono": (nu_mono, inv_mono), "P2": (nu_p2, inv_p2)}


# ======================================================================================================== the lapse system (copied from CFG373, spherical)
def Mb_enc(r, a):
    r = np.asarray(r, float)
    return np.ones_like(r) if a == 0 else r ** 2 / (r + a) ** 2


def lapse_g(r, Mtot):
    """leaf-elliptic weak-field lapse: c^2 grad ln N = g, div g = -4 pi G_N rho  ->  g = G_N M(<r)/r^2 (G_N absorbed)."""
    return Mtot / r ** 2


def gN_of_g(g, a0m, ker):
    """CFG373's mass-shell inverse of the kernel."""
    return a0m * KER[ker][1](g / a0m)


def M_target(r, g, a0m, ker):
    """CFG373 G1: the lapse-local target, M_t[g](<r) = r^2 (g - g_N(g))/G."""
    return r ** 2 * (g - gN_of_g(g, a0m, ker))


def M_phantom(r, a, a0m, ker):
    Mb = Mb_enc(r, a)
    return (KER[ker][0](Mb / (r ** 2 * a0m)) - 1.0) * Mb


def rho_of_M(r, M):
    return np.gradient(M, r) / (4 * np.pi * r ** 2)


def x_edge_true(a, a0m=1.0, ker="nu_mono", S=SHARE):
    """the exhaustion radius M_ph(<r) = S (reference for the controls)."""
    return brentq(lambda x: float(M_phantom(np.array([x]), a, a0m, ker)[0]) - S, 1e-3, 1e5, xtol=1e-13)


def grid(xmax, n=12001, rmin=1e-3):
    return np.logspace(math.log10(rmin), math.log10(xmax), n)


# ======================================================================================================== controls K1, K5 (sympy)
P("\n[K1] CFG373's identities (sympy, copied) + nu_mono inverse round trip")
G_, M_, r_, A0_ = sp.symbols("G M r a0", positive=True)
gNs = G_ * M_ / r_ ** 2
gs = sp.sqrt(gNs ** 2 + gNs * A0_)
AL = A0_ / 2
ident = sp.expand(gs ** 2 + AL ** 2 - (gNs + AL) ** 2)
x_ = sp.symbols("x", positive=True)
rM_ = sp.sqrt(G_ * M_ / A0_)
cfg44 = M_ * (sp.sqrt(1 + x_ ** 2) - 1)
Mt_exact = r_ ** 2 * (gs + AL - (gNs + AL)) / G_
diff1 = sp.simplify(Mt_exact.subs(r_, x_ * rM_) - cfg44)
flux = sp.simplify(4 * sp.pi * r_ ** 2 * ((gNs + AL) - AL))
k1a = (ident == 0) and (diff1 == 0) and (sp.simplify(flux - 4 * sp.pi * G_ * M_) == 0)
yy = np.logspace(-5, 5, 4001)
rt = inv_mono(yy * nu_mono(yy))
k1b_err = float(np.max(np.abs(rt / yy - 1)))
rt2 = inv_p2(yy * nu_p2(yy))
k1c_err = float(np.max(np.abs(rt2 / yy - 1)))
K1 = bool(k1a and k1b_err <= 1e-9 and k1c_err <= 1e-9)
P(f"  perfect square identity = {ident}; local target - CFG44 = {diff1}; AQUAL flux identity holds: {k1a}")
P(f"  nu_mono inverse round trip max rel err on [1e-5, 1e5] = {k1b_err:.1e}; P2 closed form {k1c_err:.1e}  -> K1 {'PASS' if K1 else 'FAIL'}")
R["controls"]["K1"] = {"pass": K1, "nu_mono_roundtrip": k1b_err, "p2_roundtrip": k1c_err}

P("\n[K5] lapse field energy = -W for a bounded spherical mass (truncated SIS; sympy)")
Rs, Ms, rr = sp.symbols("R M r", positive=True)
Min = Ms * rr / Rs
W5 = -sp.integrate(G_ * Min * sp.diff(Min, rr) / rr, (rr, 0, Rs))
FE5 = sp.integrate((G_ * Min / rr ** 2) ** 2 / (8 * sp.pi * G_) * 4 * sp.pi * rr ** 2, (rr, 0, Rs)) + \
    sp.integrate((G_ * Ms / rr ** 2) ** 2 / (8 * sp.pi * G_) * 4 * sp.pi * rr ** 2, (rr, Rs, sp.oo))
K5 = sp.simplify(FE5 + W5) == 0
P(f"  W = {W5}; field energy = {sp.simplify(FE5)}; sum = {sp.simplify(FE5 + W5)}  -> K5 {'PASS' if K5 else 'FAIL'}")
P("  So the weak-field lapse's own energy IS the binding energy: contraction releases it (a source), it cannot absorb it.")
R["controls"]["K5"] = {"pass": bool(K5), "W": str(W5), "field_energy": str(sp.simplify(FE5))}


# ======================================================================================================== K2: the carrier on an extended host
P("\n[K2] unlimited supply: the lapse fixed point M_c = M_t[g] (iterated from M_c = 0) vs the law's M_ph, Hernquist host")


def fixed_point_unlimited(r, a, a0m, ker, n_iter=1000):
    Mc = np.zeros_like(r)
    Mb = Mb_enc(r, a)
    # plain iteration converges slowly in the deep regime (dM_t/dM_c -> 1); use the monotone bisection form instead and
    # report the plain-iteration residual after n_iter as a cross-check of the same fixed point
    lo, hi = np.zeros_like(r), np.full_like(r, 1e6)
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        h = M_target(r, lapse_g(r, Mb + mid), a0m, ker) - mid      # decreasing in M_c
        lo = np.where(h > 0, mid, lo)
        hi = np.where(h > 0, hi, mid)
    Mfp = 0.5 * (lo + hi)
    for _ in range(n_iter):
        Mc = M_target(r, lapse_g(r, Mb + Mc), a0m, ker)
    return Mfp, Mc


K2 = True
K2rows = {}
for ker in ("nu_mono", "P2"):
    for a in (A_SCORED, A_REPORTED):
        r = np.logspace(math.log10(0.05), math.log10(50), 801)
        Mfp, Mit = fixed_point_unlimited(r, a, A0M, ker)
        Mph = M_phantom(r, a, A0M, ker)
        e1 = float(np.max(np.abs(Mfp / Mph - 1)))
        e2 = float(np.max(np.abs(Mit / Mph - 1)))
        ok = e1 <= 1e-6
        K2 = K2 and ok
        K2rows[f"{ker}|a={a}"] = {"bisection_fixed_point_maxrel": e1, "plain_iteration_1000_maxrel": e2, "pass": ok}
        P(f"  {ker:7s} a = {a:.1f} r_M: max |M_fp/M_ph - 1| = {e1:.1e} (plain iteration x1000: {e2:.1e})  {'PASS' if ok else 'FAIL'}")
P(f"  K2 {'PASS' if K2 else 'FAIL'}: the lapse carries the law's phantom (the SIS in the deep regime) on an extended host, zero constants")
R["controls"]["K2"] = {"pass": K2, "rows": K2rows}


# ======================================================================================================== the flows' equilibria
def eq_FH(S, a, a0m, ker, xmax):
    """F-H (field energy of the mismatch): solve M_c = min(M_t[g(M_c)], S) pointwise by bisection on [0, S] using the
    lapse functions; the edge is where the solution first saturates at S."""
    r = grid(xmax)
    Mb = Mb_enc(r, a)
    lo, hi = np.zeros_like(r), np.full_like(r, S)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        h = np.minimum(M_target(r, lapse_g(r, Mb + mid), a0m, ker), S) - mid
        lo = np.where(h > 0, mid, lo)
        hi = np.where(h > 0, hi, mid)
    Mc = 0.5 * (lo + hi)
    sat = np.where(Mc >= S * (1 - 1e-9))[0]
    if len(sat) == 0:
        return dict(xe=float(xmax), domain=True, r=r, Mc=Mc, xe_brent=None)
    xe_grid = float(r[sat[0]])
    xe = x_edge_true(a, a0m, ker, S)                      # brentq refinement of the same free boundary
    # KKT outside: M_t[g] >= S beyond the edge (the cap binds consistently)
    out = r > xe * 1.001
    Mt_out = M_target(r[out], lapse_g(r[out], Mb[out] + S), a0m, ker)
    kkt = bool(np.all(Mt_out >= S * (1 - 1e-9)))
    return dict(xe=xe, xe_grid=xe_grid, domain=False, r=r, Mc=Mc, kkt=kkt)


def L2_profile(mu, r, a, a0m, ker):
    Mb = Mb_enc(r, a)
    Meff = Mb - (4 * np.pi / 3) * mu * r ** 3
    pos = Meff > 0
    yeff = np.where(pos, Meff, 1e-300) / (r ** 2 * a0m)
    g = np.where(pos, a0m * yeff * KER[ker][0](yeff), 0.0)
    Mc = r ** 2 * g - Mb
    rho = rho_of_M(r, Mc)
    i0 = np.searchsorted(r, 2e-3)
    bad = np.where((rho[i0:] <= 0) | (~pos[i0:]))[0]
    ie = i0 + bad[0] if len(bad) else len(r) - 1
    return Mc, rho, ie


def eq_F2(S, a, a0m, ker, xmax):
    """F-2 (L^2): rho_c = (rho_t[g] - mu)_+; on the support the lapse fixed point is the law applied to rho_b - mu."""
    r = grid(xmax)
    Mc0, _, _ = L2_profile(0.0, r, a, a0m, ker)                # mu = 0: the law on the whole domain
    if Mc0[-1] > S:
        # the supply cannot fill the domain's target: mu > 0, free boundary; bisect in log mu (mass decreasing in mu)
        def mass(lmu):
            Mc, _, ie = L2_profile(10 ** lmu, r, a, a0m, ker)
            return Mc[ie]
        lo, hi = -14.0, 3.0
        assert mass(lo) > S > mass(hi)
        for _ in range(90):
            mid = 0.5 * (lo + hi)
            if mass(mid) > S:
                lo = mid
            else:
                hi = mid
        mu = 10 ** (0.5 * (lo + hi))
    else:
        # supply exceeds the domain's target: support = domain, mu <= 0
        mu = brentq(lambda m: L2_profile(m, r, a, a0m, ker)[0][-1] - S, -1e3, 0.0, xtol=1e-16)
    Mc, rho, ie = L2_profile(mu, r, a, a0m, ker)
    domain = ie >= len(r) - 1
    xe = float(r[ie])
    # independent check: rebuild g by Poisson from the profile (cold zero beyond the edge), re-read the lapse target
    Mcf = np.where(np.arange(len(r)) <= ie, Mc, Mc[ie])
    g = lapse_g(r, Mb_enc(r, a) + Mcf)
    rho_t = rho_of_M(r, M_target(r, g, a0m, ker))
    rho_c = rho_of_M(r, Mcf)
    inner = (r > 0.05) & (r < 0.9 * xe)
    resid = float(np.max(np.abs(rho_c[inner] - (rho_t[inner] - mu)) / rho_t[inner])) if np.any(inner) else float("nan")
    outside = r > 1.02 * xe
    kkt_max = float(np.max(rho_t[outside] / mu)) if (np.any(outside) and mu > 0) else float("nan")
    return dict(xe=xe, domain=domain, mu=mu, r=r, Mc=Mcf, resid=resid, kkt_max_rhot_over_mu_outside=kkt_max,
                mass_check=float(Mcf[-1] / S))


def KL_yN(yb, lam, ker):
    nu = KER[ker][0]
    lo = np.full_like(yb, 1e-12)
    hi = np.array(yb, float)
    for _ in range(90):
        mid = np.sqrt(lo * hi)
        F = (1 - lam) * mid * nu(mid) + lam * mid
        up = F > yb
        hi = np.where(up, mid, hi)
        lo = np.where(up, lo, mid)
    return np.sqrt(lo * hi)


def KL_Mc(r, lam, a, a0m, ker):
    Mb = Mb_enc(r, a)
    yb = Mb / (r ** 2 * a0m)
    yN = KL_yN(yb, lam, ker)
    g = a0m * yN * KER[ker][0](yN)
    return r ** 2 * g - Mb


def eq_FKL(S, a, a0m, ker, xmax):
    """F-KL (relative entropy = T3/T10's JKO settling): rho_c = lambda rho_t[g] on the whole domain; pointwise the
    fixed point is (1 - lambda) g + lambda g_N(g) = g_b."""
    xm = np.array([xmax])
    lam = brentq(lambda L: float(KL_Mc(xm, L, a, a0m, ker)[0]) - S, 0.0, 1.0, xtol=1e-14)
    r = grid(xmax)
    Mc = KL_Mc(r, lam, a, a0m, ker)
    g = lapse_g(r, Mb_enc(r, a) + Mc)
    Mt = M_target(r, g, a0m, ker)
    inner = r > 0.01
    resid = float(np.max(np.abs(Mc[inner] / (lam * Mt[inner]) - 1)))
    rho_c = rho_of_M(r, Mc)
    return dict(xe=float(xmax), domain=True, lam=lam, r=r, Mc=Mc, resid=resid, min_rho=float(np.min(rho_c[inner])))


# ======================================================================================================== physical cells
def cell_numbers(lm, foot):
    Mb = 10 ** lm * MSUN
    a0 = A0[foot]
    rM = math.sqrt(G * Mb / a0)
    rta = RTA_1E9_KPC * KPC * (10 ** lm / 1e9) ** (1 / 3)
    Mtot = Mb / FB

    def R_ta(mtot, zc):                              # copied from CFG461 (EdS turnaround timing)
        rho_ta = (9 * math.pi ** 2 / 16) * OM * RHO_CRIT0 * (2 ** (2 / 3) * (1 + zc)) ** 3
        return (3 * mtot / (4 * math.pi * rho_ta)) ** (1 / 3)
    Rvir1 = 5 / 12 * R_ta(Mtot, 1.0)
    Rvir3 = 5 / 12 * R_ta(Mtot, 3.0)
    return dict(Mb=Mb, a0=a0, rM=rM, x_ta=rta / rM, rta_kpc=rta / KPC, rM_kpc=rM / KPC, x_vir1=Rvir1 / rM,
                x_vir3=Rvir3 / rM, Rvir1=Rvir1, Rvir3=Rvir3, Vf=(G * Mb * a0) ** 0.25)


CELLS = [(lm, f) for f in FOOTS for lm in LOGMB]
CN = {(lm, f): cell_numbers(lm, f) for (lm, f) in CELLS}
P("\n[cells] r_M, catchment and virial radii (physical; the mechanisms use x = r/r_M(true a0))")
for (lm, f) in CELLS:
    c = CN[(lm, f)]
    P(f"  {f:9s} M_b=10^{lm:<4}: r_M = {c['rM_kpc']:7.2f} kpc, r_edge = {X_EDGE*c['rM_kpc']:7.1f} kpc, r_ta = {c['rta_kpc']:7.1f} kpc"
      f" (x_ta = {c['x_ta']:6.1f}), R_vir(z_c=1) = {c['x_vir1']:5.2f} r_M (R_vir/r_edge = {c['x_vir1']/X_EDGE:.2f})")
R["cells"] = {f"{f}|{lm}": {k: v for k, v in CN[(lm, f)].items()} for (lm, f) in CELLS}


def edge_y(xe, a, a0m=1.0):
    """baryonic g_N/a0_true at the edge and the total law field (true a0) there."""
    Mb = float(Mb_enc(np.array([xe]), a)[0])
    y = Mb / xe ** 2
    return y, y * float(nu_mono(np.array([y]))[0])


def run_flow(flow, S, a, ker, xmax, xvir=None):
    if flow == "F-H":
        e = eq_FH(S, a, A0M, ker, xmax)
    elif flow == "F-2":
        e = eq_F2(S, a, A0M, ker, xmax)
    elif flow == "F-KL":
        e = eq_FKL(S, a, A0M, ker, xmax)
    elif flow == "F-0":
        e = dict(xe=float(xvir if xvir is not None else xmax), domain=xvir is None)
    yb, gt = edge_y(e["xe"], a)
    e["dex"] = math.log10(e["xe"] / X_EDGE)
    e["y_edge"] = yb
    e["gtot_edge_law"] = gt
    return e


FLOWS = ("F-H", "F-2", "F-KL", "F-0")
LOCAL = {"F-H": "NOT lapse-local: drive v = D[g_N(g) - g_b] needs the baryons' own field g_b (equivalently the fluid's own "
                "field g_c, a second elliptic solve keyed to one species): CFG60/CFG473 class, G9 tension",
         "F-2": "lapse-local (rho_c and rho_t[g] at the point)",
         "F-KL": "lapse-local (rho_c and rho_t[g] at the point); = T3/T10 JKO settling",
         "F-0": "the chassis as committed: no settling drive at all (CFG381)"}
tab = {}
P("\n[flows] equilibrium edges. nu_mono, Hernquist a = 0.3 r_M (scored). dex = log10(r_e/r_edge), r_edge = 5.8498 r_M")
for supply, S in (("CAT", S_CAT), ("SHARE", SHARE), ("2xSHARE", 2 * SHARE)):
    for flow in FLOWS:
        if supply == "2xSHARE" and flow != "F-H":
            continue
        rows = {}
        for (lm, f) in CELLS:
            c = CN[(lm, f)]
            xvir = None if supply == "CAT" else c["x_vir1"]
            e = run_flow(flow, S, A_SCORED, "nu_mono", c["x_ta"], xvir)
            rows[f"{f}|{lm}"] = {k: v for k, v in e.items() if k not in ("r", "Mc")}
        tab[(supply, flow)] = rows
        dx = [rows[f"{f}|{lm}"]["dex"] for (lm, f) in CELLS]
        xs = [rows[f"{f}|{lm}"]["xe"] for (lm, f) in CELLS]
        p1 = all(abs(d) <= TOL_P1 for d in dx)
        P(f"  {supply:7s} {flow:5s}: r_e/r_M = " + ", ".join(f"{x:7.2f}" for x in xs) + "  | dex = " +
          ", ".join(f"{d:+.3f}" for d in dx) + f"  | within 0.05 dex in 6/6: {p1}")
P("  (cell order: canonical 1e9, 10^10.5, 10^11.5; alt 1e9, 10^10.5, 10^11.5)")

# diagnostics printed per flow (first cell + checks)
P("\n[flow diagnostics]")
for (supply, flow), rows in tab.items():
    r0 = rows[f"canonical|10.5"]
    extra = []
    if flow == "F-H":
        extra.append(f"KKT cap binds outside: {all(v.get('kkt', True) for v in rows.values())}")
        extra.append(f"grid edge vs brentq: {max(abs(math.log10(v['xe_grid']/v['xe'])) for v in rows.values() if 'xe_grid' in v):.1e} dex")
    if flow == "F-2":
        extra.append(f"mu = {r0['mu']:.3e}; support fills domain: {r0['domain']}; self-consistency resid (indep. lapse re-read) max "
                     f"{max(v['resid'] for v in rows.values()):.1e}; mass check {r0['mass_check']:.6f}; max rho_t/mu outside {r0['kkt_max_rhot_over_mu_outside']:.3f}")
    if flow == "F-KL":
        extra.append(f"lambda = {r0['lam']:.4f} (middle canonical; range {min(v['lam'] for v in rows.values()):.4f}-"
                     f"{max(v['lam'] for v in rows.values()):.4f}); resid of rho_c = lambda rho_t[g] (indep. re-read) {max(v['resid'] for v in rows.values()):.1e}; min rho_c {min(v['min_rho'] for v in rows.values()):.2e}")
    P(f"  {supply:7s} {flow:5s}: y_edge (g_N/a0 at r_e) middle-canonical = {r0['y_edge']:.5f} (target {Y_E:.5f}); " + "; ".join(extra))
    P(f"           locality: {LOCAL[flow]}")


# ======================================================================================================== K3: restatement control
P("\n[K3] restatement control: F-H with exactly the cosmic share (the edge enters through the supply)")
xe_pt = x_edge_true(0.0, A0M, "nu_mono", SHARE)
k3a = abs(xe_pt / X_EDGE - 1) <= 1e-3
sh = tab[("SHARE", "F-H")]
k3b = all(abs(v["dex"]) <= TOL_P1 for v in sh.values())
K3 = bool(k3a and k3b) if not MUT else None
P(f"  point-mass host: x_e = {xe_pt:.5f} r_M vs {X_EDGE:.5f} ({'within' if k3a else 'OUTSIDE'} 1e-3)")
P(f"  Hernquist a = 0.3: dex = " + ", ".join(f"{v['dex']:+.4f}" for v in sh.values()) + f" -> within 0.05: {k3b}")
if not MUT:
    P(f"  K3 {'PASS' if K3 else 'FAIL'} (this shows the gate CAN pass; it is CFG423 / T10-S6 bookkeeping, not a mechanism)")
R["controls"]["K3"] = {"pass": K3, "point_mass_xe": xe_pt, "hernquist_dex": {k: v["dex"] for k, v in sh.items()}}


# ======================================================================================================== K4: time-dependent F-H (Lagrangian shells)
P("\n[K4] F-H as a time-dependent settling run (Lagrangian shells; middle galaxy, canonical, CAT supply, uniform-mu start)")
cK = CN[(10.5, "canonical")]
N_SH = 2000
mk = S_CAT / N_SH
Mk = (np.arange(N_SH) + 0.5) * mk
r_init = 0.01 + (cK["x_ta"] - 0.01) * Mk / S_CAT          # uniform mu over [0.01, x_ta]


def rhs_factory(D):
    def rhs(t, rk):
        rk = np.maximum(rk, 1e-6)
        Mb = Mb_enc(rk, A_SCORED)
        g = lapse_g(rk, Mb + Mk)
        # v = D G (M_c(<r) - M_t[g](<r))/r^2  (the mismatch field), identical to D [g_N(g) - g_b]
        return D * (Mk - M_target(rk, g, A0M, "nu_mono")) / rk ** 2
    return rhs


k4 = {}
for D in (1.0, 10.0):
    # DISCLOSED: the first run used a span of 4e5/D, too short for the outermost shells (they start at x_ta ~ 109 and
    # drift in at ~1e-4 D); the inner shells had converged (1.4e-5). Span lengthened to 2e7/D; criterion unchanged.
    sol = solve_ivp(rhs_factory(D), (0, 2e7 / D), r_init, method="BDF", jac_sparsity=sp_identity(N_SH, format="csr"),
                    rtol=1e-9, atol=1e-10, t_eval=[0, 1e3 / D, 1e5 / D, 2e7 / D])
    rfD = sol.y[:, -1]
    order_ok = bool(np.all(np.diff(rfD) > 0))
    # the outermost shell sits at M = S - m/2; extrapolate linearly to M = S (the free boundary)
    xe_dyn = float(rfD[-1] + (rfD[-1] - rfD[-2]) * 0.5)
    k4[D] = dict(xe=xe_dyn, ok=bool(sol.success), order_preserved=order_ok, rf=rfD,
                 r_mid=[float(np.median(sol.y[:, i])) for i in range(sol.y.shape[1])])
rf = k4[1.0]["rf"]
eqK = eq_FH(S_CAT, A_SCORED, A0M, "nu_mono", cK["x_ta"])
dexK4 = abs(math.log10(k4[1.0]["xe"] / eqK["xe"]))
Mph_at_shells = M_phantom(np.maximum(rf, 1e-6), A_SCORED, A0M, "nu_mono")
band = (rf > 0.1 * eqK["xe"]) & (rf < 0.9 * eqK["xe"])
prof_err = float(np.max(np.abs(Mk[band] / Mph_at_shells[band] - 1)))
dD = abs(math.log10(k4[10.0]["xe"] / k4[1.0]["xe"]))
K4 = bool(k4[1.0]["ok"] and k4[1.0]["order_preserved"] and dexK4 <= 0.01 and prof_err <= 0.01)
P(f"  dynamic edge = {k4[1.0]['xe']:.3f} r_M vs equilibrium {eqK['xe']:.3f} r_M ({dexK4:.1e} dex); M_c(<r) vs equilibrium on [0.1, 0.9] r_e: "
  f"max {prof_err:.1e}; median shell radius over time {', '.join(f'{x:.2f}' for x in k4[1.0]['r_mid'])}")
P(f"  mobility D x10 moves the settled edge by {dD:.1e} dex (D sets the clock only)  -> K4 {'PASS' if K4 else 'FAIL'}")
R["controls"]["K4"] = {"pass": K4, "xe_dynamic": k4[1.0]["xe"], "xe_equilibrium": eqK["xe"], "dex": dexK4, "profile_err": prof_err,
                       "D_x10_shift_dex": dD}
# the identity v/D = g_N(g) - g_b (F-H needs g_b)
rr_ = np.logspace(-1, 2, 50)
Mc_ = 0.5 * M_phantom(rr_, A_SCORED, A0M, "nu_mono")
g_ = lapse_g(rr_, Mb_enc(rr_, A_SCORED) + Mc_)
idres = float(np.max(np.abs((Mc_ - M_target(rr_, g_, A0M, "nu_mono")) / rr_ ** 2 - (gN_of_g(g_, A0M, "nu_mono") - Mb_enc(rr_, A_SCORED) / rr_ ** 2))))
P(f"  identity check: F-H velocity/D minus [g_N(g) - g_b] = {idres:.1e} (the drive needs the baryons' own field g_b)")
R["FH_drive_identity_residual"] = idres


# ======================================================================================================== gate scoring
P("\n" + "=" * 110)
P("GATES (scored supply CAT, a = 0.3 r_M, nu_mono)")
verd = {}
for flow in FLOWS:
    rows = tab[("CAT", flow)]
    p1 = all(abs(v["dex"]) <= TOL_P1 for v in rows.values())
    worst = max(abs(v["dex"]) for v in rows.values())
    verd[flow] = dict(P1=p1, worst_dex=worst, P2="PASS (no constant enters the equilibrium edge; mobility D is a coupling, reported)",
                      locality=LOCAL[flow], dex=[v["dex"] for v in rows.values()])
    P(f"  {flow:5s}: P1 {'PASS' if p1 else 'FAIL'} (worst |dex| = {worst:.3f}); P2 structurally clean; L: {LOCAL[flow][:60]}...")
R["gates"] = verd

# f_b-test
P("\n[f_b-test] d ln y_e / d ln f_b with f_b x1.2 wherever it enters the mechanism (target 2.181, nu_mono point mass)")
fbt = {}
c = CN[(10.5, "canonical")]
FB2 = 1.2 * FB
SH2 = 1 / FB2 - 1
for supply, S, S2 in (("CAT", S_CAT, S_CAT), ("SHARE", SHARE, SH2)):
    for flow in FLOWS:
        xvir = None if supply == "CAT" else c["x_vir1"]
        e1 = run_flow(flow, S, A_SCORED, "nu_mono", c["x_ta"], xvir)
        if supply == "SHARE" and flow == "F-0":
            xvir2 = xvir * (FB / FB2) ** (1 / 3)          # M_tot = M_b/f_b in the C4 toy
            e2 = run_flow(flow, S2, A_SCORED, "nu_mono", c["x_ta"], xvir2)
        else:
            e2 = run_flow(flow, S2, A_SCORED, "nu_mono", c["x_ta"], xvir)
        d = math.log(e2["y_edge"] / e1["y_edge"]) / math.log(1.2)
        fbt[f"{supply}|{flow}"] = d
        P(f"  {supply:5s} {flow:5s}: {d:+.3f}")
R["fb_test"] = fbt
# point-mass analytic target check
yA = math.log(1 / (1 - FB2)) ** 2
P(f"  (analytic exhaustion edge, point mass: {math.log(yA/Y_E)/math.log(1.2):+.3f} for a finite x1.2 step; derivative 2.181)")


# ======================================================================================================== edge-state flux diagnostic
P("\n[edge state] law-settled to r_edge + CAT remainder at uniform mu over [r_edge, r_ta]: does the flux vanish at r_edge?")
es = {}
for (lm, f) in [(10.5, "canonical"), (9.0, "alt"), (11.5, "alt")]:
    c = CN[(lm, f)]
    r = grid(c["x_ta"], 40001)
    Mph = M_phantom(r, A_SCORED, A0M, "nu_mono")
    rho_ph = rho_of_M(r, Mph)
    Me = float(M_phantom(np.array([X_EDGE]), A_SCORED, A0M, "nu_mono")[0])
    mu_rem = (S_CAT - Me) / (4 * np.pi * (c["x_ta"] - X_EDGE))
    w = 0.5 * (1 - np.tanh(np.log10(r / X_EDGE) / 0.02))
    rho_c = rho_ph * w + mu_rem / r ** 2 * (1 - w)
    Mc = np.concatenate([[0.0], np.cumsum(0.5 * (4 * np.pi * r[1:] ** 2 * rho_c[1:] + 4 * np.pi * r[:-1] ** 2 * rho_c[:-1]) * np.diff(r))])
    Mc += Mph[0]
    g = lapse_g(r, Mb_enc(r, A_SCORED) + Mc)
    Mt = M_target(r, g, A0M, "nu_mono")
    rho_t = rho_of_M(r, Mt)
    v = {"F-H": (Mc - Mt) / r ** 2, "F-2": -np.gradient(rho_c - rho_t, r), "F-KL": -np.gradient(np.log(rho_c / rho_t), r)}
    row = {}
    for fl, vv in v.items():
        fl_at = {}
        for q in (1.0, 1.1, 1.5):
            i = np.searchsorted(r, q * X_EDGE)
            flux = 4 * np.pi * r[i] ** 2 * rho_c[i] * vv[i]
            fl_at[q] = float(flux)
        row[fl] = fl_at
    i11 = np.searchsorted(r, 1.1 * X_EDGE)
    row["rho_t_over_rho_c_at_1.1"] = float(rho_t[i11] / rho_c[i11])
    row["mu_rem_over_mu_target"] = float(mu_rem / (rho_t[i11] * r[i11] ** 2))
    es[f"{f}|{lm}"] = row
    P(f"  {f:9s} 10^{lm}: rho_t[g]/rho_c at 1.1 r_edge = {row['rho_t_over_rho_c_at_1.1']:.2f} (the lapse asks for MORE fluid outside)")
    for fl in ("F-H", "F-2", "F-KL"):
        P(f"     {fl:5s} mass flux (D = 1; + outward) at 1.0 / 1.1 / 1.5 r_edge = " + " / ".join(f"{row[fl][q]:+.2e}" for q in (1.0, 1.1, 1.5)))
R["edge_state"] = es


# ======================================================================================================== reported variants
P("\n[reported variants, not scored]")
var = {}
for label, a, ker in (("a=1.0 nu_mono", A_REPORTED, "nu_mono"), ("a=0.3 P2 (CFG373 closed form)", A_SCORED, "P2"),
                      ("point mass nu_mono", 0.0, "nu_mono")):
    for supply, S in (("CAT", S_CAT), ("SHARE", SHARE)):
        for flow in ("F-H", "F-2", "F-KL"):
            dx = []
            for (lm, f) in CELLS:
                cc = CN[(lm, f)]
                e = run_flow(flow, S, a, ker, cc["x_ta"])
                dx.append(e["dex"])
            var[f"{label}|{supply}|{flow}"] = dx
            P(f"  {label:30s} {supply:5s} {flow:5s}: dex = " + ", ".join(f"{d:+.3f}" for d in dx))
R["variants"] = var


# ======================================================================================================== POST-RUN REPORT (added after the first run; not a verdict input)
P("\n[POST-RUN REPORT, not a verdict input] where each equilibrium's cold mass sits, and whether it realises the law")
P("  (middle galaxy, canonical, a = 0.3 r_M, nu_mono). r50/r90/r95 = radii enclosing 50/90/95% of the cold mass;")
P("  g/g_law = the equilibrium's total field over the law's field at 2, 5, 10, 20 r_M; Mc/Mb = M_c(<r)/M_b(<r) there.")
post_rep = {}
cpr = CN[(10.5, "canonical")]
for supply, S in (("CAT", S_CAT), ("SHARE", SHARE)):
    for flow in ("F-H", "F-2", "F-KL"):
        fn = {"F-H": eq_FH, "F-2": eq_F2, "F-KL": eq_FKL}[flow]
        e = fn(S, A_SCORED, A0M, "nu_mono", cpr["x_ta"])
        r, Mc = e["r"], e["Mc"]
        Mtot_c = Mc[-1]
        pct = {q: float(np.interp(q * Mtot_c, Mc, r)) for q in (0.5, 0.9, 0.95)}
        Mb = Mb_enc(r, A_SCORED)
        g = lapse_g(r, Mb + Mc)
        glaw = Mb / r ** 2 * nu_mono(Mb / r ** 2)
        at = {x: (float(np.interp(x, r, g / glaw)), float(np.interp(x, r, Mc / Mb))) for x in (2.0, 5.0, 10.0, 20.0)}
        post_rep[f"{supply}|{flow}"] = {"r50": pct[0.5], "r90": pct[0.9], "r95": pct[0.95],
                                        "g_over_glaw": {str(k): v[0] for k, v in at.items()}, "Mc_over_Mb": {str(k): v[1] for k, v in at.items()}}
        P(f"  {supply:5s} {flow:5s}: r50/r90/r95 = {pct[0.5]:6.2f} / {pct[0.9]:6.2f} / {pct[0.95]:6.2f} r_M | g/g_law at 2,5,10,20 = "
          + ", ".join(f"{at[x][0]:.3f}" for x in (2.0, 5.0, 10.0, 20.0)) + " | Mc/Mb = " + ", ".join(f"{at[x][1]:.2f}" for x in (2.0, 5.0, 10.0, 20.0)))
_kc, _ks = post_rep["CAT|F-KL"]["g_over_glaw"], post_rep["SHARE|F-KL"]["g_over_glaw"]
P(f"  Reading: F-KL with the lapse-carried target is a PARTIAL law whose g/g_law falls outward ({_kc['2.0']:.2f} -> {_kc['20.0']:.2f} over 2-20 r_M")
P(f"  on CAT, {_ks['2.0']:.2f} -> {_ks['20.0']:.2f} on SHARE), with its cold mass spread over the whole catchment; only where")
P("  g << [(1-lambda)/lambda] a0 does it approach M_c ~ [lambda/(1-lambda)] M_b (baryon-tracing). Its percentile radii are not an edge.")
P("  F-2 follows the law (of rho_b - mu) inside ~r_e/2 and bends below it toward its edge. F-H realises the law exactly inside its edge.")
R["post_run_report"] = post_rep


# ======================================================================================================== energy sink
P("\n[energy sink] what settling to r_edge must shed, and what the same field can absorb (z_c = 1 unless stated)")


def W_of(r, M):
    dM = np.gradient(M, r)
    return -np.trapezoid(M * dM / r, r) if hasattr(np, "trapezoid") else -np.trapz(M * dM / r, r)


sink = {}
for (lm, f) in CELLS:
    c = CN[(lm, f)]
    unitE = G * c["Mb"] ** 2 / c["rM"]
    Mtot = c["Mb"] / FB
    # (a) CFG461 toy
    dEa = G * Mtot ** 2 / 4 * (1 / (X_EDGE * c["rM"]) - 1 / c["Rvir1"])
    dEa3 = G * Mtot ** 2 / 4 * (1 / (X_EDGE * c["rM"]) - 1 / c["Rvir3"])
    contr = c["x_vir1"] / X_EDGE
    # (b) virial, Hernquist + cold
    r = np.logspace(-4, 5, 200001)
    Mb = Mb_enc(r, A_SCORED)
    Mc_i = SHARE * np.minimum(r / c["x_vir1"], 1.0)
    Mc_f = np.minimum(M_phantom(r, A_SCORED, 1.0, "nu_mono"), SHARE)
    Wi, Wf = W_of(r, Mb + Mc_i), W_of(r, Mb + Mc_f)
    Wh = W_of(r, Mb)
    dEb = (Wi - Wf) / 2 * unitE
    dW = abs(Wi - Wf) * unitE
    # channels
    cap_alpha = ALPHA_MAX / 2 * dW
    Vol = 4 * math.pi / 3 * c["Rvir1"] ** 3
    best_K = 0.0
    need_enh = []
    for Gam in (3.21 * H_L, 1 / T_H):
        for al in (ALPHA_MIN, ALPHA_MAX):
            for c2 in (C2_MIN, C2_MAX):
                K = 2 * (al / c2) * (c["Vf"] / CL) ** 2 * Gam / CL
                EK = c2 * CL ** 4 * K ** 2 / (16 * math.pi * G) * Vol * max(1.0, Gam * T_H)
                if dEb > 0:
                    best_K = max(best_K, EK / dEb)
                    Kneed = math.sqrt(16 * math.pi * G * dEb / (c2 * CL ** 4 * Vol * max(1.0, Gam * T_H)))
                    need_enh.append(Kneed / K)
    if dEb <= 0:
        best_K, need_enh = float("inf"), [0.0]
    sink[f"{f}|{lm}"] = dict(dE_toy_J=dEa, dE_toy_over_Evir=contr - 1, contraction_Rvir_over_redge=contr,
                             contraction_zc3=c["x_vir3"] / X_EDGE, dE_toy_zc3_J=dEa3, dE_virial_J=dEb,
                             W_hernquist_check=Wh * (6 * A_SCORED), ratio_lapse=0.0, ratio_alpha=cap_alpha / dEb,
                             ratio_K_best=best_K, K_enhancement_needed_min=min(need_enh), K_enhancement_needed_max=max(need_enh))
    s = sink[f"{f}|{lm}"]
    P(f"  {f:9s} 10^{lm:<4}: R_vir/r_edge = {contr:.2f} (z_c=3: {s['contraction_zc3']:.2f}); dE toy = {dEa:.2e} J "
      f"(= {contr-1:.2f} x E_vir), virial = {dEb:.2e} J; z_c=3 toy {dEa3:+.2e} J")
    P(f"             capacity/required: lapse 0 (K5) | alpha_c {s['ratio_alpha']:.1e} | K^2 (CFG381-induced K) {best_K:.1e}"
      f" | direct coupling must enhance K by {min(need_enh):.1e}-{max(need_enh):.1e}")
    P(f"             (Hernquist W check: W/(-G M^2/6a) = {-Wh*6*A_SCORED:.5f})")
sink_supplied = all(max(v["ratio_alpha"], v["ratio_K_best"], v["ratio_lapse"]) >= 1 for v in sink.values())
P(f"  SINK: {'SUPPLIED' if sink_supplied else 'NOT SUPPLIED'} by the same field (frozen line: some channel >= 1 in all 6 cells)")
R["sink"] = {"cells": sink, "supplied": sink_supplied,
             "contraction_cfg461_canonical_zc1": [sink[f"canonical|{lm}"]["contraction_Rvir_over_redge"] for lm in LOGMB]}


# ======================================================================================================== verdict
P("\n" + "=" * 110)
anyP1 = any(v["P1"] for v in verd.values())
if anyP1:
    lane = "LAPSE NO-FLUX EDGE FOUND (subject to P3 in the MUTATE run)"
elif (K3 if not MUT else all(abs(v["dex"]) <= TOL_P1 for v in tab[("SHARE", "F-H")].values())):
    lane = "EXHAUSTION ONLY (FAIL): no flow stops at r_edge with the catchment supply; the edge appears only as the exhaustion radius of exactly the cosmic share"
else:
    lane = "NO EDGE (FAIL)" if not MUT else "MUTATE: no flow and no control lands on the true r_edge"
P(f"LANE VERDICT: {lane}")
P(f"SINK: {'SUPPLIED' if sink_supplied else 'NOT SUPPLIED'}")
R["verdict"] = lane

rc = 0
if MUT:
    # teeth: the K3 control moves by -0.1505 +- 0.02 dex and fails P1 against the true r_edge; no flow passes P1
    sh_m = tab[("SHARE", "F-H")]
    xe_pt_shift = math.log10(xe_pt / X_EDGE)
    shifts_h = [v["dex"] - (math.log10(x_edge_true(A_SCORED, 1.0, "nu_mono", SHARE) / X_EDGE)) for v in sh_m.values()]
    teeth_pt = abs(xe_pt_shift - PRED_SHIFT) <= 0.02 and abs(xe_pt_shift) > TOL_P1
    teeth_h = all(abs(s - PRED_SHIFT) <= 0.02 for s in shifts_h) and all(abs(v["dex"]) > TOL_P1 for v in sh_m.values())
    P(f"\n[MUTATE teeth] K3 point mass shift {xe_pt_shift:+.4f} dex (pred {PRED_SHIFT:+.4f}); Hernquist shifts "
      + ", ".join(f"{s:+.4f}" for s in shifts_h) + f"; all fail P1 vs true r_edge: {teeth_h}; no flow passes P1: {not anyP1}")
    for flow in FLOWS:
        P(f"  {flow:5s} CAT dex vs TRUE r_edge under MUTATE: " + ", ".join(f"{d:+.3f}" for d in verd[flow]["dex"]))
    detected = bool(teeth_pt and teeth_h and not anyP1)
    R["mutate_teeth"] = {"point_shift": xe_pt_shift, "hernquist_shifts": shifts_h, "detected": detected}
    rc = 1 if detected else 0
    P(f"MUTATE: teeth {'DETECTED (exit 1, as designed)' if detected else 'NOT detected (exit 0: the control did not bite)'}")
else:
    ctl = {k: R["controls"][k]["pass"] for k in ("K1", "K2", "K3", "K4", "K5")}
    P(f"controls: {ctl}")
    rc = 0 if all(ctl.values()) else 1


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, (np.floating,)):
        o = float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None if math.isnan(o) else ("inf" if o > 0 else "-inf")
    return o


R["flows"] = {f"{s}|{fl}": rows for (s, fl), rows in tab.items()}
R["exit_code"] = rc
json.dump(jclean(R), open(os.path.join(HERE, f"cfg462_results{TAG}.json"), "w"), indent=1)
P(f"exit {rc}")
OUT.close()
sys.exit(rc)
