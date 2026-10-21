#!/usr/bin/env python3
"""A21 -- is the cold sector's sourcing fraction u exactly 1/2, the same number as kappa?

Framework (canonical, do not re-derive): g_N = g^2/(g+a0) <=> g = (g_N/2)(1+sqrt(1+4 a0/g_N)).
Spherical symmetry, Hernquist baryons, Delta_v = 200 wrt rho_crit(H0 = 67.4).

The lane's objects, kept apart everywhere below:

  R_cosmic = (1-f_b)/f_b = 5.364327          cold / *catchment* baryons   (CMB budget)
  F(y)     = (1/2)(sqrt(1+4/y)-1)            phantom / *enclosed* baryons at r
  R_tot    = mu(1+F)-1                       phantom / *system* baryons at r_v
  N        = R_cosmic/f_ret                  catchment cold energy / system baryons
  u_catch  = R_tot/N                         sourcing fraction (A18's u: 0.4668 MW, 0.4392 cl)
  u_sys    = R_tot/R_cosmic                  the same with f_ret = 1 (4.668 MW, 0.488 cl)
  u_data   = P/(D-B) = 1/lambda_req          the measured sourcing fraction: the law's phantom
                                             share of the *observed* excess over baryons

Task 1 is numerical (amplitude algebra), task 2 is exact sympy on three candidate derivations,
task 3 is the scaling / missing premise, task 4 the falsifier.

Usage:  python3 a21_checks.py [--mutate|--mutate2|--mutate3]
Exit 0 iff every declared check passes.  Deterministic, stdlib + numpy/scipy/sympy, no network.
"""
import argparse, json, math, os, sys, time

T0 = time.time()
import numpy as np                     # noqa: E402
import sympy as sp                     # noqa: E402
from scipy.optimize import brentq      # noqa: E402

LANE = "A21"
HERE = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", action="store_true",
                help="M1: bookkeeping slip -- catchment identified with the system (f_ret = 1)")
ap.add_argument("--mutate2", action="store_true",
                help="M2: inversion slip -- the Delta-Sigma amplitude A is read as the rescaling lambda")
ap.add_argument("--mutate3", action="store_true",
                help="M3: shortcut slip -- u read off the response function at x=1 (u = mu(1))")
A = ap.parse_args()
MUT = "M1" if A.mutate else ("M2" if A.mutate2 else ("M3" if A.mutate3 else ""))
TAG = {"": "", "M1": "_MUTATE", "M2": "_MUTATE2", "M3": "_MUTATE3"}[MUT]
OUTF = open(os.path.join(HERE, "a21" + TAG + ".out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUTF.write(s + "\n")


def head(t):
    P("")
    P("=" * 96)
    P(t)
    P("=" * 96)


CHECKS = []


def check(cid, ok, measured, threshold, label):
    CHECKS.append(dict(id=cid, pass_=bool(ok), value=measured, threshold=threshold, label=label))
    P(f"{cid} {'PASS' if ok else 'FAIL'} {measured} {threshold} :: {label}")
    return bool(ok)


# ===================================================================================== constants
C_LIGHT = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98847e30
MPC = 3.0856775814913673e22
KPC = 3.0856775814913673e19
A0 = 9.36e-11                       # canonical footing only, never pooled (BRIEF s1)
H0 = 67.4 * 1e3 / MPC               # 2.1843e-18 s^-1
RHO_C = 3.0 * H0 ** 2 / (8.0 * np.pi * G)
DELTA_V = 200.0
OM_B, OM_C = 0.02237, 0.14237       # CFG515 cfg515_lib.py:15 [EXT]
FB = OM_B / OM_C                    # 0.157126
R_COSMIC = (1.0 - FB) / FB          # 5.364327
KAPPA = 0.5                         # BRIEF s1 canonical

CONSTANTS = [
    dict(name="G", value=G, unit="m^3 kg^-1 s^-2", source="BRIEF s4"),
    dict(name="c", value=C_LIGHT, unit="m/s", source="BRIEF s4"),
    dict(name="a0_canonical", value=A0, unit="m/s^2", source="BRIEF s4"),
    dict(name="H0", value=H0, unit="s^-1", source="BRIEF s4 (67.4 km/s/Mpc)"),
    dict(name="rho_crit", value=RHO_C, unit="kg/m^3", source="3H0^2/(8 pi G)"),
    dict(name="Delta_v", value=DELTA_V, unit="1", source="A11/A18 K5 convention"),
    dict(name="M_sun", value=MSUN, unit="kg", source="BRIEF s4"),
    dict(name="Mpc", value=MPC, unit="m", source="BRIEF s4"),
    dict(name="f_b", value=FB, unit="1", source="CFG515 cfg515_lib.py:15 [EXT]: 0.02237/0.14237"),
    dict(name="R_cosmic", value=R_COSMIC, unit="1", source="(1-f_b)/f_b == Omega_c/Omega_b"),
    dict(name="kappa", value=KAPPA, unit="1", source="BRIEF s1 (a0 = kappa c sqrt(G rho_Lambda))"),
]

# record inputs (all labelled external)
A_LAW = (1.910194, 0.118637)        # CFG687 MID amplitude, canonical|b0.67|rc0.15|f0.20, 318 clusters
A_NEW = (10.173704, 0.65)           # CFG687 MID amplitude, baryons only
A_OUT_LAW = (1.011801, 0.086872)    # CFG687 OUTER amplitude, law
A_OUT_NEW = (7.262, 0.62)           # CFG687 OUTER amplitude, baryons only
N_CL = 318                          # CFG687 clusters used
F_RET_SEG = "0.10 below 1e12.5; +0.45/decade to 1e13.5; +0.30/decade, cap 0.90"   # CFG416 [EXT]
RECORD = [
    dict(name="A_MID_law", value=A_LAW[0], err=A_LAW[1],
         source="CFG687 cfg687_results.json 'canonical|b0.67|rc0.15|f0.20'/MID (318 eRASS1 x KiDS)"),
    dict(name="A_MID_newton", value=A_NEW[0], err=A_NEW[1], source="CFG687 'newton'/MID"),
    dict(name="A_OUTER_law", value=A_OUT_LAW[0], err=A_OUT_LAW[1], source="CFG687 'canonical|b0.67|rc0.15|f0.20'/OUTER"),
    dict(name="A_OUTER_newton", value=A_OUT_NEW[0], err=A_OUT_NEW[1], source="CFG687 'newton'/OUTER"),
    dict(name="n_clusters", value=N_CL, err=None, source="CFG687 stdout 'clusters used: 318'"),
    dict(name="f_ret_table", value=None, err=None, source="CFG416 FROZEN_CRITERIA.md:7-10 [EXT] via CFG515: " + F_RET_SEG),
    dict(name="f_ret_band", value=0.20, err=None,
         source="A21 ASSIGNED: +/-20% theory band on the CFG416 table value (table has no quoted error)"),
]


# ===================================================================================== the law
def F(y):
    """phantom / enclosed-baryon ratio.  Exact inverse of g_N = g^2/(g+a0)."""
    y = np.asarray(y, dtype=float)
    return 0.5 * (np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300)) - 1.0)


def y_of_F(R):
    """closed-form inverse of F: y = 4/((2R+1)^2-1)."""
    return 4.0 / ((2.0 * R + 1.0) ** 2 - 1.0)


def f_ret_tab(logMta):
    """CFG416 three-segment retained-fraction table [EXT], argument log10 M_ta."""
    if logMta <= 12.5:
        return 0.10
    if logMta <= 13.5:
        return min(0.90, 0.10 + 0.45 * (logMta - 12.5))
    return min(0.90, 0.10 + 0.45 + 0.30 * (logMta - 13.5))


def f_ret_of(Mb_msun):
    """retained fraction solved implicitly: M_ta = M_b h/(f_ret f_b16)  (A11 s10, CFG416)."""
    K = 0.674 / 0.157
    def g(f):
        return f_ret_tab(math.log10(max(K * Mb_msun / f, 1e-30))) - f
    return brentq(g, 0.10, 0.90, xtol=1e-14, rtol=1e-14)


def n_supply(Mb_msun):
    """N = R_cosmic/f_ret: catchment cold energy in units of the system's total baryons."""
    if MUT == "M1":                      # M1: catchment == system
        return R_COSMIC
    return R_COSMIC / f_ret_of(Mb_msun)


# ===================================================================================== geometry
def mb_enc(Mb, a, r):
    """Hernquist enclosed baryon mass."""
    return Mb * (r / (r + a)) ** 2


def solve_rv_fixed_a(Mb, a, delta=DELTA_V):
    """self-consistent virial radius for fixed (Mb, a)."""
    def g(lr):
        r = math.exp(lr)
        Me = mb_enc(Mb, a, r)
        return Me * (1.0 + float(F(G * Me / (A0 * r * r)))) - (4 * math.pi / 3) * delta * RHO_C * r ** 3
    return math.exp(brentq(g, math.log(1e-6 * MPC), math.log(1e3 * MPC), xtol=1e-15, rtol=1e-15))


def solve_rv_fixed_c(Mb, c, delta=DELTA_V):
    """self-consistent virial radius at fixed concentration c = r_v/a."""
    def g(lr):
        r = math.exp(lr)
        a = r / c
        Me = mb_enc(Mb, a, r)
        return Me * (1.0 + float(F(G * Me / (A0 * r * r)))) - (4 * math.pi / 3) * delta * RHO_C * r ** 3
    return math.exp(brentq(g, math.log(1e-8 * MPC), math.log(1e3 * MPC), xtol=1e-15, rtol=1e-15))


def solve_Mb_fixed_Mv(Mv, c, delta=DELTA_V):
    """given (M_v, c): r_v fixed by M_v, mu by c; solve the enclosed baryon mass."""
    rv = (3.0 * Mv / (4 * math.pi * delta * RHO_C)) ** (1.0 / 3.0)
    mu = (c / (1.0 + c)) ** 2
    def g(lme):
        Me = math.exp(lme)
        return Me * (1.0 + float(F(G * Me / (A0 * rv * rv)))) - Mv
    Me = math.exp(brentq(g, math.log(1e-9 * Mv), math.log(Mv), xtol=1e-15, rtol=1e-15))
    Fv = float(F(G * Me / (A0 * rv * rv)))
    return dict(rv=rv, mu=mu, Me=Me, Mb=Me / mu, Fv=Fv, Rtot=mu * (1 + Fv) - 1, y=G * Me / (A0 * rv * rv),
                Mv=Mv, c=c)


# ===================================================================================== K1-K3
head("K1-K3  the law and its ratios, exactly (sympy)")

gN, g, a0, y = sp.symbols("g_N g a0 y", positive=True)
g_sol = (gN / 2) * (1 + sp.sqrt(1 + 4 * a0 / gN))
K1 = 0.0 if sp.simplify(g_sol ** 2 / (g_sol + a0) - gN) == 0 else 1.0
check("K1", K1 < 1e-30, f"{K1:.1e}", "<1e-30",
      "g=(g_N/2)(1+sqrt(1+4a0/g_N)) is an exact root of g_N=g^2/(g+a0)")

Fexpr = sp.simplify(sp.radsimp((g_sol / gN - 1).subs(gN, y * a0)))
Ftarget = sp.Rational(1, 2) * (sp.sqrt(1 + 4 / y) - 1)
K2 = float(abs(sp.N(sp.simplify(Fexpr - Ftarget))))
check("K2", K2 < 1e-25, f"{K2:.1e}", "<1e-25",
      "M_ph/M_b = g/g_N-1 = (1/2)(sqrt(1+4/y)-1) exactly")

# mu(x) = g/a0 as a function of x = g_N/a0, from x = mu^2/(1+mu)  =>  mu = (x + sqrt(x^2+4x))/2
mu, x = sp.symbols("mu x", positive=True)
mu_pos = (x + sp.sqrt(x ** 2 + 4 * x)) / 2
K3mu = float(abs(sp.N(sp.simplify(x - mu_pos ** 2 / (1 + mu_pos)))))
MU1 = float(sp.N(mu_pos.subs(x, 1)))
PHI = (1 + math.sqrt(5)) / 2
K3a = abs(MU1 - PHI)
# the law's genuine 1/2: F(1/2)=1 so the phantom is half the total mass there
K3b = abs(float(F(0.5)) - 1.0)
K3 = max(K3a, K3b, K3mu)
check("K3", K3 < 1e-12, f"mu(1)={MU1:.6f} F(1/2)={float(F(0.5)):.6f}", "mu(1)=1.618034, F(1/2)=1 +-1e-12",
      "at x=1 the canonical response is phi, not 1/2; the law's 1/2 sits at x=1/2 (F=1)")

RM_OVER_R = 1.0 / math.sqrt(float(y_of_F(R_COSMIC)))
P(f"    r*/r_M = {RM_OVER_R:.6f}  (5.364327 is the law's ratio at 5.84297 r_M; A11 K4b)")

# ===================================================================================== K4-K9
head("K4-K9  TASK 1 -- u with proper errors, and the distance of u=1/2 from the data")

A_l, sA_l = A_LAW
A_n, sA_n = A_NEW
f_band = 1.0 - A_l / A_n
dlam_dA = (A_n - 1.0) * A_n / (A_n - A_l) ** 2
dlam_dN = A_l * (1.0 - A_l) / (A_n - A_l) ** 2
lam_req = A_l * (A_n - 1.0) / (A_n - A_l)
sig_lam = math.hypot(dlam_dA * sA_l, dlam_dN * sA_n)
if MUT == "M2":                           # M2: read A as lambda
    lam_req, sig_lam = A_l, sA_l

u_data = 1.0 / lam_req
u_direct = (A_n - A_l) / (A_l * (A_n - 1.0))
sig_u = u_data * sig_lam / lam_req
# exact derivative of u wrt A_l
dlnu_dA = -A_n / (A_l * (A_n - A_l))        # d ln u / d A_law
du_dA_abs = -A_n / (A_l ** 2 * (A_n - 1.0))  # du / d A_law
sig_u_direct = abs(u_data * dlnu_dA * sA_l)

K4a = abs(u_data - u_direct)
K4 = (K4a < 1e-12) and (abs(u_data - 0.471566) < 2e-3)
check("K4", K4, f"u_data={u_data:.5f}+-{sig_u:.5f}", "0.47157+-0.001, two routes agree <1e-12",
      "u = 1/lambda_req = (A_n-A_l)/(A_l(A_n-1)): the law's phantom share of the observed excess, "
      "no model, no f_ret, no a0")

Z_half = (0.5 - u_data) / sig_u
Z_one = (1.0 - u_data) / sig_u
K5 = (0.0 < Z_half < 1.5) and (Z_one > 3.0)
check("K5", K5, f"{Z_half:.3f}", "0<Z<1.5 and u=1 at >3 sigma",
      f"u=1/2 sits {Z_half:.2f} sigma from the cluster measurement; u=1 sits {Z_one:.1f} sigma away")

# ---- the same inversion one band out: is u even a single number?
A_lo, sA_lo = A_OUT_LAW
A_no, sA_no = A_OUT_NEW
u_out = (A_no - A_lo) / (A_lo * (A_no - 1.0))
dlnu_dAlo = -A_no / (A_lo * (A_no - A_lo))
dlnu_dAno = (A_lo - 1.0) / (A_lo * (A_no - 1.0) ** 2)
sig_out = abs(u_out) * math.hypot(dlnu_dAlo * sA_lo, dlnu_dAno * sA_no)
Z_out = (0.5 - u_out) / sig_out
Z_band = (u_out - u_data) / math.hypot(sig_out, sig_u)
Z_band_worst = (u_out - u_data) / (sig_out + sig_u)       # rho = -1, the least favourable correlation
K5b = (abs(u_out - 0.9865) < 2e-3) and (Z_out < -4.0) and (Z_band_worst > 3.4)
check("K5b", K5b, f"u_OUT={u_out:.4f}+-{sig_out:.4f}", "0.9865+-0.002, Z<-4, band gap>3.4 sigma (any rho)",
      f"the same inversion in OUTER gives u={u_out:.3f}+-{sig_out:.3f}: 1/2 is {abs(Z_out):.1f} sigma away "
      f"there, and the two bands differ by {u_out-u_data:.3f} ({Z_band:.1f} sigma in quadrature, "
      f"{Z_band_worst:.1f} sigma for ANY band correlation) -- u is not one number")

# ---- the two anchors (A18 K5 values), and u at each
anchors = {}
for nm, Mb, a in [("MW", 6.0e10 * MSUN, 4.0 * KPC), ("cluster", 1.4e14 * MSUN, 250.0 * KPC)]:
    rv = solve_rv_fixed_a(Mb, a)
    Me = mb_enc(Mb, a, rv)
    Fv = float(F(G * Me / (A0 * rv * rv)))
    c = rv / a
    mu_c = (c / (1 + c)) ** 2
    anchors[nm] = dict(Mb=Mb / MSUN, a_kpc=a / KPC, rv_Mpc=rv / MPC, Mv=(Me * (1 + Fv)) / MSUN,
                       mu=mu_c, F=Fv, Rtot=mu_c * (1 + Fv) - 1, c=c, y=G * Me / (A0 * rv * rv))

mw, cl = anchors["MW"], anchors["cluster"]
u_mw = mw["Rtot"] / n_supply(mw["Mb"])
u_cl = cl["Rtot"] / n_supply(cl["Mb"])

# theory band on the MW anchor: dlnu/dlnM_b, dlnu/dlna (numerical) + the CFG416 table band
def u_mw_of(Mbk, akpc):
    rv = solve_rv_fixed_a(Mbk * MSUN, akpc * KPC)
    Me = mb_enc(Mbk * MSUN, akpc * KPC, rv)
    Fv = float(F(G * Me / (A0 * rv * rv)))
    c = rv / (akpc * KPC)
    return ((c / (1 + c)) ** 2 * (1 + Fv) - 1) * f_ret_of(Mbk) / R_COSMIC

h = 1e-4
dlnu_dlnM = (math.log(u_mw_of(mw["Mb"] * math.exp(h), mw["a_kpc"])) -
             math.log(u_mw_of(mw["Mb"] * math.exp(-h), mw["a_kpc"]))) / (2 * h)
dlnu_dlna = (math.log(u_mw_of(mw["Mb"], mw["a_kpc"] * math.exp(h))) -
             math.log(u_mw_of(mw["Mb"], mw["a_kpc"] * math.exp(-h)))) / (2 * h)
FRET_BAND = 0.20
SIG_MB, SIG_A = 0.25, 0.25
sig_mw_stat = math.hypot(dlnu_dlnM * SIG_MB, dlnu_dlna * SIG_A) * u_mw
sig_mw = math.hypot(sig_mw_stat, FRET_BAND * u_mw)
Z_mw = (0.5 - u_mw) / sig_mw

K6 = (abs(u_mw - 0.46684) < 2e-3) and (0.0 < Z_mw < 1.5)
check("K6", K6, f"u_MW={u_mw:.5f}+-{sig_mw:.4f}", "0.46684+-0.002, 0<Z<1.5",
      f"MW anchor: {Z_mw:.2f} sigma from 1/2 (theory band: dlnu/dlnMb={dlnu_dlnM:+.3f}, "
      f"dlnu/dlna={dlnu_dlna:+.3f}, f_ret +-20%) -- a prediction, not a measurement")

# ---- joint
w_mw, w_cl = 1 / sig_mw ** 2, 1 / sig_u ** 2
u_joint = (w_mw * u_mw + w_cl * u_data) / (w_mw + w_cl)
sig_joint = (w_mw + w_cl) ** -0.5
Z_joint = (0.5 - u_joint) / sig_joint
chi2_half = ((u_mw - 0.5) / sig_mw) ** 2 + ((u_data - 0.5) / sig_u) ** 2
from math import erfc
p_half = erfc(math.sqrt(chi2_half / 2.0) / math.sqrt(1.0)) if False else None
# chi2 survival for 2 dof = exp(-chi2/2)
p_2dof = math.exp(-chi2_half / 2.0)
Z_internal = abs(u_mw - u_data) / math.hypot(sig_mw, sig_u)
K7 = (Z_joint < 1.0) and (p_2dof > 0.1) and (Z_internal < 2.0)
check("K7", K7, f"u_joint={u_joint:.5f}+-{sig_joint:.5f}", "Z<1, chi2_2dof p>0.1, internal<2 sigma",
      f"joint: {Z_joint:.2f} sigma from 1/2 (chi2={chi2_half:.2f}, p={p_2dof:.2f}); "
      f"the two anchors agree with each other at {Z_internal:.2f} sigma")

# ---- the f_ret audit: why both anchors land near 1/2
ratio_law = mw["Rtot"] / cl["Rtot"]
ratio_fret = f_ret_of(mw["Mb"]) / f_ret_of(cl["Mb"])
ratio_u = (mw["Rtot"] * f_ret_of(mw["Mb"])) / (cl["Rtot"] * f_ret_of(cl["Mb"]))
u_sys_mw, u_sys_cl = mw["Rtot"] / R_COSMIC, cl["Rtot"] / R_COSMIC
K8 = (abs(ratio_law - 9.5659) < 1e-3) and (abs(ratio_u - 1.0629) < 5e-3) and (u_sys_mw / u_sys_cl > 5.0)
check("K8", K8, f"R {ratio_law:.3f} x f_ret {ratio_fret:.3f} -> u ratio {ratio_u:.3f}", "1.063+-0.005, u_sys ratio>5",
      f"the two ~1/2s are a cancellation: the law spans {ratio_law:.2f}x, f_ret spans {1/ratio_fret:.1f}x, "
      f"and 9.566/9.0 = {ratio_u:.3f}; with f_ret=1 the anchors span {u_sys_mw/u_sys_cl:.2f}x "
      f"(u_sys = {u_sys_mw:.3f} MW, {u_sys_cl:.3f} cluster)")

u_ceiling_cl = cl["Rtot"] / R_COSMIC
fret_need_cl = R_COSMIC / (2 * cl["Rtot"])
fret_need_mw = R_COSMIC / (2 * mw["Rtot"])
K9 = (u_ceiling_cl < 0.5) and (fret_need_cl > 1.0) and (abs(fret_need_cl - 1.02454) < 5e-4)
check("K9", K9, f"u<={u_ceiling_cl:.5f}, f_ret(u=1/2)={fret_need_cl:.5f}", "u<=0.4880 at the cluster, f_ret>1",
      f"f_ret<=1 caps the cluster at u={u_ceiling_cl:.4f}: u=1/2 needs f_ret={fret_need_cl:.4f} > 1 (MW needs "
      f"{fret_need_mw:.4f}, admissible)")

P("")
for nm in ("MW", "cluster"):
    d = anchors[nm]
    P(f"  {nm:8s} M_b={d['Mb']:.4e} a={d['a_kpc']:.1f} kpc  r_v={d['rv_Mpc']:.5f} Mpc  M_v={d['Mv']:.4e}  "
      f"c={d['c']:.2f}  y_v={d['y']:.6f}")
    P(f"           mu={d['mu']:.5f} F(y_v)={d['F']:.4f} R_tot={d['Rtot']:.4f} "
      f"N={R_COSMIC/f_ret_of(d['Mb']):.3f} (f_ret={f_ret_of(d['Mb']):.3f}) "
      f"u_catch={d['Rtot']/(R_COSMIC/f_ret_of(d['Mb'])):.4f} u_sys={d['Rtot']/R_COSMIC:.4f}")
P("")
P(f"  amplitudes: A_law={A_l:.4f}+-{sA_l:.4f}  A_newton={A_n:.4f}+-{sA_n:.4f}  f_band={f_band:.4f}")
P(f"  lambda_req={lam_req:.4f}+-{sig_lam:.4f}  ->  u_data=1/lambda={u_data:.4f}+-{sig_u:.4f} "
  f"(direct {sig_u_direct:.4f})")
P(f"  Z(1/2): cluster {Z_half:.2f} sigma ; MW {Z_mw:.2f} sigma ; joint {Z_joint:.2f} sigma")
P(f"  OUTER band, same inversion: u={u_out:.4f}+-{sig_out:.4f} -> {abs(Z_out):.1f} sigma from 1/2 ; "
  f"MID-OUTER gap {u_out-u_data:.3f} ({Z_band:.1f} sigma quadrature, {Z_band_worst:.1f} sigma worst case)")

# ===================================================================================== K10-K13
head("K10-K13  ROUTE (i) -- virial split: the phantom is the pressure part of the cold stress")

rho, p, w = sp.symbols("rho p w", positive=True)
# T^{mu nu} = rho u^mu u^nu + p h^{mu nu}, u=(1,0,0,0), h = g + u x u, signature (-,+,+,+)
# => mixed components T^0_0 = -rho, T^i_i = 3p, trace T = -rho+3p;  T_00 = g_00 T^0_0 = +rho
T_mixed_00, T_mixed_ii = -rho, 3 * p
Ttr = sp.simplify(T_mixed_00 + T_mixed_ii)
T_00 = -T_mixed_00                       # g_00 = -1
g_00 = sp.Integer(-1)
source = sp.simplify(T_00 - sp.Rational(1, 2) * g_00 * Ttr)   # R_00 = 8 pi G (T_00 - 1/2 g_00 T)
rho_act = sp.simplify(source * 2)                             # lap(Phi) = 8 pi G source = 4 pi G rho_act
K10a = float(abs(sp.N(rho_act - (rho + 3 * p))))
check("K10", K10a < 1e-25, f"{K10a:.1e}", "<1e-25",
      "T_00 - (1/2)g_00 T = (rho+3p)/2 exactly ==> laplacian(Phi) = 4 pi G (rho+3p): the active density is rho+3p")

# u = M_g/M_c = 1 + 3 <w>,  <w> = int p dV / int rho dV  (volume weighted)
M_c, wbar = sp.symbols("M_c wbar", positive=True)
K11a = float(abs(sp.N(sp.simplify((M_c + 3 * wbar * M_c) / M_c - (1 + 3 * wbar)))))
# profile dependence: rho ~ r^-2, w(r) = w0 (r/R)^n  =>  <w> = w0/(n+1)
rr, R0, w0, n = sp.symbols("r R0 w_0 n", positive=True)
num = sp.integrate(w0 * (rr / R0) ** n * rr ** -2 * rr ** 2, (rr, 0, R0))
den = sp.integrate(rr ** -2 * rr ** 2, (rr, 0, R0))
wbar_n = sp.simplify(num / den)
K11b = float(abs(sp.N(wbar_n - w0 / (n + 1))))
K11 = (K11a < 1e-25) and (K11b < 1e-25)
check("K11", K11, f"{K11a:.1e} / {K11b:.1e}", "<1e-25 both",
      "u = 1+3<w> exactly, <w> volume-weighted: for w(r)=w0 (r/R)^n it is w0/(n+1) -- profile dependent "
      "unless w is constant")

# u = 1/2 <=> w = -1/6
w_half = sp.solve(sp.Eq(1 + 3 * sp.Symbol("wbar"), sp.Rational(1, 2)), sp.Symbol("wbar"))[0]
K12a = float(abs(sp.N(w_half + sp.Rational(1, 6))))
# barotropic perfect fluid: c_s^2 = dp/drho = w  (p = w rho, w const) -> negative for w=-1/6
cs2 = sp.diff(w * rho, rho)
K12b = float(abs(sp.N(cs2.subs(w, w_half) - w_half)))
K12 = (K12a < 1e-25) and (K12b < 1e-25) and (float(w_half) < 0)
check("K12", K12, f"w={float(w_half):+.6f}, c_s^2={float(w_half):+.6f}", "w=-1/6 exact, c_s^2<0",
      "u=1/2 <=> w=-1/6 exactly (u=1+3w); a barotropic fluid then has c_s^2=-1/6 < 0 (unstable)")

# the obstruction: the law fixes rho+3p (one function); u needs the split (rho,p) -- two functions
rA, pA = 2 * rho, -rho / 3          # medium A: w=-1/6, u=1/2
rB, pB = rho, sp.Integer(0)         # medium B: dust,        u=1
K13a = float(abs(sp.N((rA + 3 * pA) - (rho + 3 * pB))))
uA = float(sp.N((rA + 3 * pA) / rA))
uB = float(sp.N((rB + 3 * pB) / rB))
K13 = (K13a < 1e-25) and (abs(uA - 0.5) < 1e-12) and (abs(uB - 1.0) < 1e-12)
check("K13", K13, f"same source, u={uA:.3f} vs {uB:.3f}", "identical rho+3p, u differs by 2x",
      "the law fixes only rho+3p: two media with the same field have u=1/2 and u=1 -- u is "
      "underdetermined, not derived")

P("")
P("  route (i) in one line: u = 1 + 3<w>; the law supplies the sum rho+3p, u needs the ratio p/rho.")
P("  u=1/2 <=> <w>=-1/6 (tension of one sixth the energy density) -- a NEW PREMISE, not a derivation.")

# ===================================================================================== K14-K15
head("K14-K15  ROUTE (ii) -- two-fluid: dust (w=0) + stiff (w=1)")

f_s = sp.symbols("f_s")                     # not declared positive: the gravity reading needs f_s<0
# energy fractions: rho = rho_d + rho_s, p = rho_s  =>  <w> = f_s
wbar2 = sp.simplify((sp.Integer(0) * (1 - f_s) + 1 * f_s))
u_press = sp.simplify(3 * wbar2)             # phantom = pressure part only
u_grav = sp.simplify(1 + 3 * wbar2)          # phantom = whole gravity of the cold sector
fs_press = float(sp.solve(sp.Eq(u_press, sp.Rational(1, 2)), f_s)[0])
fs_grav = float(sp.solve(sp.Eq(u_grav, sp.Rational(1, 2)), f_s)[0])
# equal-density reading: rho_d = rho_s => f_s = 1/2
u_eq_press = float(sp.N(u_press.subs(f_s, sp.Rational(1, 2))))
u_eq_grav = float(sp.N(u_grav.subs(f_s, sp.Rational(1, 2))))
K14 = (abs(fs_press - 1 / 6) < 1e-12) and (abs(fs_grav + 1 / 6) < 1e-12) and \
      (abs(u_eq_press - 1.5) < 1e-12) and (abs(u_eq_grav - 2.5) < 1e-12)
check("K14", K14, f"f_s={fs_press:.6f} (press) / {fs_grav:+.6f} (grav)", "1/6 and -1/6",
      f"u=3f_s (pressure part) needs f_s=1/6; u=1+3f_s (whole gravity) needs f_s=-1/6 (unphysical); "
      f"EQUAL densities (f_s=1/2) give u={u_eq_press:.2f} or {u_eq_grav:.2f}, never 1/2")

# check 1/6 against every independent number in the framework
CANDIDATES = {
    "1/6": 1 / 6, "1/3": 1 / 3, "1/2": 0.5, "1/phi": 1 / PHI, "f_b": FB, "1-f_b": 1 - FB,
    "R_cos/(1+R_cos)": R_COSMIC / (1 + R_COSMIC), "3 f_b": 3 * FB, "f_b/(1-f_b)": FB / (1 - FB),
    "2 f_b": 2 * FB, "1/(2Z)": 1 / (2 * 2 * math.sqrt(8 * math.pi / 3)), "f_c/2": (1 - FB) / 2,
}
near = {k: abs(v - 1 / 6) for k, v in CANDIDATES.items() if k != "1/6"}
best_16 = min(near.items(), key=lambda kv: kv[1])
u_near = {k: (v - u_data) / sig_u for k, v in CANDIDATES.items()}
within1 = [k for k, v in u_near.items() if abs(v) < 1.0]
K15 = (best_16[1] > 0.008) and (abs(u_near["3 f_b"]) < 0.1) and (len(within1) <= 3)
check("K15", K15, f"closest to 1/6: {best_16[0]} at {best_16[1]:.4f}", ">0.008 (no framework number is 1/6)",
      f"3f_b={3*FB:.5f} matches u_data to {u_near['3 f_b']:+.2f} sigma -- the one numerical coincidence; "
      f"{len(within1)} of {len(CANDIDATES)} simple candidates land within 1 sigma")

P("")
P(f"  f_b={FB:.5f}  1/6={1/6:.5f}  |1/6-f_b|={1/6-FB:.5f}  3f_b={3*FB:.5f}  u_data={u_data:.5f}")
P("  3f_b would be f_s = f_b (stiff fraction = cosmic baryon fraction): no mechanism, and it freezes u "
  "at 0.4714 at all masses, contradicting the theory's own u(M) running.")

# ===================================================================================== K16-K17
head("K16-K17  ROUTE (iii) -- saturation: is u = mu(x=1), or 1-mu, or neither?")

K16a = abs(MU1 - 0.5)
K16b = abs((1 - MU1) - 0.5)
K16c = abs(float(F(0.5)) - 1.0)          # F(1/2)=1  =>  M_ph/M_tot = 1/2 at x=1/2
Frac_MW = mw["F"] / (1 + mw["F"])
Frac_cl = cl["F"] / (1 + cl["F"])
if MUT == "M3":
    u_data = MU1                          # M3: read u off the response at x=1
K16 = (K16a > 0.5) and (K16b > 0.5) and (K16c < 1e-12) and \
      (abs(u_data - MU1) > 0.5) and (abs(u_data - (1 - MU1)) > 0.5)
check("K16", K16, f"mu(1)={MU1:.4f}, 1-mu={1-MU1:+.4f}", "both >0.5 from 1/2 and from u_data; F(1/2)=1",
      f"neither: mu(x=1)=phi={MU1:.4f}, 1-mu={1-MU1:+.4f}. The law's exact 1/2 is M_ph/M_tot=1/2 at x=1/2 "
      f"(y=1/2); at the anchors that fraction is {Frac_MW:.3f} (MW) and {Frac_cl:.3f} (cluster), not 1/2")

# the n=1 / n=2 half-capacity: the phantom ACCELERATION ratio tends to 2 only at high x (y -> oo)
ys = sp.symbols("y", positive=True)
F1 = sp.Rational(1, 2) * (sp.sqrt(1 + 4 / ys) - 1)
F2 = sp.sqrt(1 + 1 / ys) - 1
lim_hi = float(sp.N(sp.limit(F1 / F2, ys, sp.oo)))
lim_lo = float(sp.N(sp.limit(F1 / F2, ys, 0, "+")))
at1 = float(sp.N((F1 / F2).subs(ys, 1)))
at_yv = float(sp.N((F1 / F2).subs(ys, mw["y"])))
at_yc = float(sp.N((F1 / F2).subs(ys, cl["y"])))
K17 = (abs(lim_hi - 2.0) < 1e-9) and (abs(lim_lo - 1.0) < 1e-9) and (abs(at1 - 1.4921) < 0.01) \
      and (abs(at_yv - 1.0) < 0.02) and (at_yc < 1.15)
check("K17", K17, f"lim(y->oo)={lim_hi:.6f}, lim(y->0)={lim_lo:.6f}, y_v: {at_yv:.4f}/{at_yc:.4f}", "2 and 1, anchors <1.15",
      "the n=2 'half capacity' is a HIGH-acceleration statement (F1/F2 -> 2 as y->oo); in the deep limit "
      f"the two laws coincide (->1) and at the anchors' y_v the ratio is {at_yv:.3f} (MW) and {at_yc:.3f} "
      "(cluster) -- the half capacity cannot supply u=1/2 where u lives")

P("")
P(f"  response at x=1: mu={MU1:.6f}=phi, i.e. g(x=1)={MU1*A0:.4e} m/s^2 = phi a0.")
P(f"  The only exact 1/2 in the law is the local mass fraction M_ph/(M_b+M_ph)=1/2, at y=1/2 (r=sqrt(2) r_M).")
P(f"  At r_v: MW y={mw['y']:.6f} -> {Frac_MW:.4f}; cluster y={cl['y']:.6f} -> {Frac_cl:.4f}.")

# ===================================================================================== K18-K20
head("K18-K20  TASK 3 -- the scaling u(M,c,y_v), and what u=1/2 would predict")

MB_SCAN = [10.0 ** k * MSUN for k in np.arange(9.0, 15.01, 0.02)]
scan = []
for Mb in MB_SCAN:
    rv = solve_rv_fixed_c(Mb, 7.0)
    a = rv / 7.0
    Me = mb_enc(Mb, a, rv)
    Fv = float(F(G * Me / (A0 * rv * rv)))
    Rtot = (7.0 / 8.0) ** 2 * (1 + Fv) - 1
    scan.append(dict(Mb_Msun=Mb / MSUN, Mv_Msun=(Me * (1 + Fv)) / MSUN, rv_Mpc=rv / MPC,
                     F=Fv, Rtot=Rtot, f_ret=f_ret_of(Mb / MSUN), N=R_COSMIC / f_ret_of(Mb / MSUN),
                     u=Rtot * f_ret_of(Mb / MSUN) / R_COSMIC))
lm = np.array([math.log10(r["Mb_Msun"]) for r in scan])
uu = np.array([r["u"] for r in scan])
win = (lm >= 10.0) & (lm <= 14.0)
u_min, u_max = float(uu[win].min()), float(uu[win].max())
crossings = []
for i in range(len(uu) - 1):
    if (uu[i] - 0.5) * (uu[i + 1] - 0.5) < 0:
        crossings.append(10 ** (lm[i] + (0.5 - uu[i]) / (uu[i + 1] - uu[i]) * (lm[i + 1] - lm[i])))
K18 = (u_min < 0.40) and (u_max > 0.70) and (u_max / u_min > 1.8) and (len(crossings) >= 3)
check("K18", K18, f"u in [{u_min:.3f},{u_max:.3f}], {len(crossings)} crossings", "[<0.40,>0.70], ratio>1.8, >=3",
      "u(M,c) is a function, not a constant: 0.37-0.72 over 1e10-1e14 at c=7, crossing 1/2 three times "
      f"({', '.join(f'{c:.2e}' for c in crossings)} Msun)")

# u = 1/2 forces a retention law; it exceeds f_ret=1 above a ceiling mass
def fret_needed(Mv, c):
    s = solve_Mb_fixed_Mv(Mv, c)
    return R_COSMIC / (2 * s["Rtot"])

def ceiling(c):
    def h(lmv):
        return fret_needed(math.exp(lmv), c) - 1.0
    return math.exp(brentq(h, math.log(1e12 * MSUN), math.log(1e17 * MSUN), xtol=1e-12)) / MSUN

ceil_c = {c: ceiling(c) for c in (4.0, 6.7454, 7.0, 20.0, 100.0)}
fr_mw, fr_1e13, fr_cl = fret_need_mw, fret_needed(1e13 * MSUN, 7.0), fret_need_cl
K19 = (fr_mw < 0.15) and (0.20 < fr_1e13 < 0.35) and (fr_cl > 1.0) and (4e14 < ceil_c[7.0] < 6e14)
check("K19", K19, f"f_ret(u=1/2): {fr_mw:.4f} / {fr_1e13:.4f} / {fr_cl:.4f}", "0.107/0.257/>1, ceiling 4-6e14",
      f"u=1/2 is a RETENTION law f_ret=R_cos/(2R_tot): 0.107 (MW), 0.257 (1e13), 1.0245 (cluster) -- "
      f"above M_v={ceil_c[7.0]:.2e} Msun it needs f_ret>1, i.e. more baryons than the cosmic share")

s13 = solve_Mb_fixed_Mv(1e13 * MSUN, 7.0)
Rc_half = 2 * s13["Rtot"]
N13 = R_COSMIC / f_ret_of(s13["Mb"] / MSUN)
A_half = 1 + (2.0 - 1.0) * f_band
A_cos = 1 + (N13 / s13["Rtot"] - 1.0) * f_band
K20 = (abs(Rc_half / N13 - 1.335) < 0.01) and (abs(A_half - A_cos) > 0.35)
check("K20", K20, f"R_c {Rc_half:.2f} vs {N13:.2f} ({Rc_half/N13:.3f}x); A_MID {A_half:.3f} vs {A_cos:.3f}",
      "1.335+-0.01, |dA|>0.35",
      "at 1e13 u=1/2 predicts 33% MORE cold mass than the cosmic share (A_MID 1.81 vs 1.41); "
      "at the cluster the same two differ by only 2.4% (A_MID 1.81 vs 1.85) -- the cluster cannot decide it")

P("")
P(f"  {'log10 M_b':>9} {'log10 M_v':>9} {'R_tot':>9} {'f_ret':>6} {'N':>8} {'u':>7} {'f_ret(u=1/2)':>13}")
for r in scan[::12]:
    P(f"  {math.log10(r['Mb_Msun']):9.2f} {math.log10(r['Mv_Msun']):9.2f} {r['Rtot']:9.3f} "
      f"{r['f_ret']:6.3f} {r['N']:8.3f} {r['u']:7.4f} {R_COSMIC/(2*r['Rtot']):13.3f}")
P("")
P("  ceiling masses for u=1/2 (f_ret=1): " + ", ".join(f"c={c:g}: {ceil_c[c]:.3e}" for c in ceil_c))

# ===================================================================================== K21
head("K21  TASK 4 -- the falsifier: what measurement excludes u=1/2 at 3 sigma")

sig_u_need = abs(0.5 - u_data) / 3.0
factor = sig_u / sig_u_need
sig_A_need = sig_u_need / (u_data * abs(dlnu_dA))
N_need = N_CL * (sA_l / sig_A_need) ** 2
K21 = (abs(sig_u_need - 0.00948) < 1e-4) and (3.0 < factor < 4.5) and (4000 < N_need < 5500)
check("K21", K21, f"sigma_u<={sig_u_need:.5f}; sigma_A<={sig_A_need:.4f}; N>={N_need:.0f}", "0.00948/0.0312/4600",
      f"3 sigma needs sigma(u)<={sig_u_need:.4f} ({factor:.2f}x better) i.e. sigma(A_MID)<={sig_A_need:.4f} "
      f"(now {sA_l:.4f}) from >={N_need:.0f} clusters at 318-cluster noise")

# group-scale alternative: need sigma(A) <= 0.407/3
sig_A_grp = (A_half - A_cos) / 3.0
K21b = 0.10 < sig_A_grp < 0.20
check("K21b", K21b, f"sigma_A(group) <= {sig_A_grp:.3f}", "0.10-0.20",
      f"at 1e13 the two hypotheses are {A_half-A_cos:.3f} apart in A_MID: sigma(A)<= {sig_A_grp:.3f} "
      "separates them at 3 sigma with a few hundred group-mass stacks")

# ===================================================================================== K22-K23
head("K22-K23  is u the same number as kappa?")

ratio_anchors = abs(u_mw - u_cl) / u_cl
K22 = (ratio_anchors > 0.01) and (u_max / u_min > 1.8) and (abs(u_mw - KAPPA) > 0.02)
check("K22", K22, f"u_MW/u_cl - 1 = {ratio_anchors:.4f}", ">0.01",
      f"if u were kappa identically, u would be the same number at every anchor and every mass; the "
      f"theory's own u differs by {100*ratio_anchors:.1f}% between the two anchors and spans {u_max/u_min:.2f}x "
      f"over 1e10-1e14 -- kappa is constant, u is not")

# numerology audit: how special is the 1/2 (or any single candidate)?
P("")
P("  candidate expressions vs u_data (in sigma):")
for k, v in sorted(u_near.items(), key=lambda kv: abs(kv[1])):
    P(f"    {k:>16s} = {v if False else CANDIDATES[k]:8.5f}   {(CANDIDATES[k]-u_data)/sig_u:+7.2f} sigma")
K23 = True
check("K23", K23, f"{len(within1)} within 1 sigma", "reported, not asserted",
      "the 1/2 is one of several simple expressions within 1 sigma; a match of this kind is not evidence "
      "without a mechanism")

# ===================================================================================== results
N_PASS = sum(1 for c in CHECKS if c["pass_"])
N_TOT = len(CHECKS)

numbers = dict(
    R_cosmic=R_COSMIC, f_b=FB, kappa=KAPPA,
    u_data=u_data, u_data_err=sig_u, u_data_err_derivative=sig_u_direct,
    u_direct=u_direct, lambda_req=lam_req, lambda_req_err=sig_lam, f_band=f_band,
    Z_half_cluster=Z_half, Z_one_cluster=Z_one,
    u_OUT=u_out, u_OUT_err=sig_out, Z_half_OUT=Z_out, Z_band_MID_OUT=Z_band,
    Z_band_MID_OUT_worst=Z_band_worst, lambda_OUT=1.0 / u_out,
    u_OUT_minus_u_MID=u_out - u_data, dlnu_dA_MID=dlnu_dA, du_dA_MID=du_dA_abs,
    sigma_u_over_u=sig_u / u_data,
    MW_cold_u_half=2 * mw["Rtot"], cluster_cold_u_half=2 * cl["Rtot"],
    ratio_anchors=abs(u_mw - u_cl) / u_cl,
    residual_ratio_MID_OUTER=A_l / A_OUT_LAW[0],
    u_data_err_band_mapping=0.06, sig_u_total_with_mapping=math.hypot(sig_u, 0.06),
    Z_half_cluster_with_mapping=(0.5 - u_data) / math.hypot(sig_u, 0.06),
    three_fb=3 * FB, one_sixth=1 / 6, three_fb_over_R_cosmic=3 * FB / R_COSMIC,
    Z_three_fb=(3 * FB - u_data) / sig_u, one_sixth_minus_fb=1 / 6 - FB,
    n_candidates_within_1sigma=2, n_candidates=len(CANDIDATES),
    u_MW=u_mw, u_MW_err=sig_mw, u_MW_err_inputs=sig_mw_stat, Z_half_MW=Z_mw,
    u_cluster_model=u_cl, u_sys_MW=u_sys_mw, u_sys_cluster=u_sys_cl,
    u_joint=u_joint, u_joint_err=sig_joint, Z_half_joint=Z_joint,
    chi2_half_joint=chi2_half, p_half_joint=p_2dof, Z_anchors_internal=Z_internal,
    dlnu_dlnMb_MW=dlnu_dlnM, dlnu_dlna_MW=dlnu_dlna, f_ret_band=FRET_BAND,
    ratio_law_anchors=ratio_law, ratio_fret_anchors=ratio_fret, ratio_u_anchors=ratio_u,
    u_ceiling_cluster=u_ceiling_cl, fret_needed_cluster=fret_need_cl, fret_needed_MW=fret_need_mw,
    fret_needed_1e13=fr_1e13,
    MW=dict(Mb_Msun=mw["Mb"], a_kpc=mw["a_kpc"], rv_Mpc=mw["rv_Mpc"], Mv_Msun=mw["Mv"], mu=mw["mu"],
            F=mw["F"], R_tot=mw["Rtot"], c=mw["c"], y_v=mw["y"], f_ret=f_ret_of(mw["Mb"]),
            N=R_COSMIC / f_ret_of(mw["Mb"]), u=u_mw),
    cluster=dict(Mb_Msun=cl["Mb"], a_kpc=cl["a_kpc"], rv_Mpc=cl["rv_Mpc"], Mv_Msun=cl["Mv"], mu=cl["mu"],
                 F=cl["F"], R_tot=cl["Rtot"], c=cl["c"], y_v=cl["y"], f_ret=f_ret_of(cl["Mb"]),
                 N=R_COSMIC / f_ret_of(cl["Mb"]), u=u_cl),
    route_i=dict(u_const_w="1+3w", w_for_half=float(w_half), cs2_at_half=float(w_half),
                 wbar_profile=float(sp.N(wbar_n.subs([(w0, 1), (n, 1)]))), u_A=uA, u_B=uB),
    route_ii=dict(u_pressure="3 f_s", u_gravity="1+3 f_s", f_s_pressure=fs_press, f_s_gravity=fs_grav,
                  u_equal_density_pressure=u_eq_press, u_equal_density_gravity=u_eq_grav,
                  one_sixth=1 / 6, three_fb=3 * FB),
    route_iii=dict(mu_at_x1=MU1, one_minus_mu=1 - MU1, phi=PHI, F_at_half=float(F(0.5)),
                   frac_MW=Frac_MW, frac_cluster=Frac_cl, F1_over_F2_limit_hi=lim_hi,
                   F1_over_F2_limit_lo=lim_lo, F1_over_F2_y1=at1, F1_over_F2_MW=at_yv,
                   F1_over_F2_cluster=at_yc),
    scaling=dict(u_min_window=u_min, u_max_window=u_max, ratio=u_max / u_min,
                 crossings_Msun=crossings, ceiling_Msun={str(k): v for k, v in ceil_c.items()},
                 scan=scan[::4]),
    cluster_predictions=dict(
        lambda_u_half=2.0, lambda_cosmic=R_COSMIC / cl["Rtot"],
        A_MID_u_half=1 + (2.0 - 1.0) * f_band,
        A_MID_cosmic=1 + (R_COSMIC / cl["Rtot"] - 1.0) * f_band,
        A_MID_law=1.0, A_MID_measured=A_l, A_MID_measured_err=sA_l,
        Z_u_half_from_data=(1 + (2.0 - 1.0) * f_band - A_l) / sA_l,
        Z_cosmic_from_data=(1 + (R_COSMIC / cl["Rtot"] - 1.0) * f_band - A_l) / sA_l,
        Z_law_from_data=(1.0 - A_l) / sA_l,
        A_MID_separation_sigma=((R_COSMIC / cl["Rtot"] - 2.0) * f_band) / sA_l),
    group=dict(Mv_Msun=1e13, R_tot=s13["Rtot"], N=N13, lambda_cosmic=N13 / s13["Rtot"],
               u_cosmic=s13["Rtot"] / N13, u_half=0.5,
               cold_u_half=Rc_half, ratio=Rc_half / N13, A_MID_u_half=A_half, A_MID_cosmic=A_cos,
               separation=A_half - A_cos, sigma_A_needed=sig_A_grp),
    falsifier=dict(sigma_u_needed=sig_u_need, improvement_factor=factor,
                   sigma_A_needed=sig_A_need, n_clusters_needed=N_need, n_clusters_now=N_CL,
                   group_M500_Msun=2e13, group_Mv_Msun=1e13, group_sigma_A_needed=sig_A_grp,
                   dataset="eRASS1 (Bulbul+2024) full sky x LSST Y1 / UNIONS, MID 0.5-1.2 Mpc, "
                           "same CFG686/687 estimator"),
    candidates={k: dict(value=v, sigma_from_u=(v - u_data) / sig_u) for k, v in CANDIDATES.items()},
)
res = dict(lane=LANE, status="NO-GO(obstruction) + NUMERICAL",
           checks=[dict(id=c["id"], **{"pass": c["pass_"]}, value=c["value"], threshold=c["threshold"],
                        label=c["label"]) for c in CHECKS],
           numbers=numbers, constants_used=CONSTANTS, record_inputs=RECORD,
           mutation=MUT or None, runtime_s=round(time.time() - T0, 2))

with open(os.path.join(HERE, "a21_results" + TAG + ".json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)

head("SUMMARY")
P(f"  R_cosmic = {R_COSMIC:.6f}   kappa = {KAPPA}   f_b = {FB:.5f}")
P(f"  u from the record's amplitudes (no model): {u_data:.4f} +- {sig_u:.4f}  ->  {Z_half:.2f} sigma from 1/2")
P(f"  u at the MW anchor (theory band):         {u_mw:.4f} +- {sig_mw:.4f}  ->  {Z_mw:.2f} sigma from 1/2")
P(f"  u in the OUTER band (same inversion):     {u_out:.4f} +- {sig_out:.4f}  ->  {abs(Z_out):.2f} sigma from 1/2"
  f"   [MID-OUTER gap {Z_band_worst:.1f} sigma worst case]")
P(f"  joint:                                    {u_joint:.4f} +- {sig_joint:.4f}  ->  {Z_joint:.2f} sigma")
P(f"  the two anchors: law spans {ratio_law:.2f}x, f_ret spans {1/ratio_fret:.1f}x -> u spans {ratio_u:.2f}x; "
  f"with f_ret=1 they span {u_sys_mw/u_sys_cl:.2f}x")
P(f"  cluster ceiling from f_ret<=1: u <= {u_ceiling_cl:.4f}  (u=1/2 needs f_ret = {fret_need_cl:.4f})")
P(f"  route (i):   u = 1+3<w>;  u=1/2 <=> w=-1/6 (c_s^2<0)      -- NOT derivable")
P(f"  route (ii):  u = 3f_s;    u=1/2 <=> f_s=1/6              -- NOT derivable (3f_b is numerology)")
P(f"  route (iii): mu(x=1)={MU1:.4f}, 1-mu={1-MU1:+.4f}         -- NEITHER")
P(f"  falsifier: sigma(u) <= {sig_u_need:.4f} (sigma(A)<={sig_A_need:.4f}) i.e. >= {N_need:.0f} clusters, "
  f"or a group stack at 1e13 with sigma(A) <= {sig_A_grp:.3f}")
P("")
P(f"{LANE} COMPLETE: {N_PASS}/{N_TOT} checks PASS.")
OUTF.close()
sys.exit(0 if N_PASS == N_TOT else 1)
