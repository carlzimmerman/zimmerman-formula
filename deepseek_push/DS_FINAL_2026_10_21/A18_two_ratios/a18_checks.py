#!/usr/bin/env python3
"""A18 -- reconciling the TWO 5.364s: the cosmic cold/baryon ratio and the law's own
phantom-to-baryon ratio at the virial radius.

Framework (canonical, do not re-derive): g_N = g^2/(g+a0)  <=>  g = (g_N/2)(1+sqrt(1+4 a0/g_N)).
Spherical symmetry.  Hernquist baryons.  Virial at Delta_v = 200 wrt rho_crit(H0 = 67.4).

The lane's three objects, kept apart everywhere below:
  R_cosmic  = (1-f_b)/f_b = 5.364327          -- cold / *catchment* baryons  (budget, global)
  F(y)      = (1/2)(sqrt(1+4/y)-1)            -- phantom / *enclosed* baryons at r  (force, local)
  N         = R_cosmic/f_ret                  -- supply in units of the system's *total* baryons
  u         = R_tot/N                         -- sourcing fraction: how much of the supply the
                                                 law's phantom actually carries

Usage:  python3 a18_checks.py [--mutate] [--mutate2]
        writes a18.out (stdout) and a18_results.json
Exit 0 iff every declared check passes.  Deterministic, stdlib + numpy/scipy/sympy, no network.
"""
import argparse, json, math, os, sys, time

T0 = time.time()          # wall clock, includes the imports below
import numpy as np                     # noqa: E402
import sympy as sp                     # noqa: E402
from scipy.optimize import brentq      # noqa: E402

LANE = "A18"
HERE = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", action="store_true",
                help="M1: bookkeeping slip -- the catchment is identified with the system (f_ret=1)")
ap.add_argument("--mutate2", action="store_true",
                help="M2: inversion slip -- the Delta-Sigma amplitude A is read as the phantom rescaling lambda")
A = ap.parse_args()
MUT = "M1" if A.mutate else ("M2" if A.mutate2 else "")
TAG = ("_MUTATE" if MUT == "M1" else ("_MUTATE2" if MUT == "M2" else ""))
OUTF = open(os.path.join(HERE, "a18" + TAG + ".out"), "w")


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
A0 = 9.36e-11                      # canonical footing only; never pooled (BRIEF s1)
H0 = 67.4 * 1e3 / MPC              # 2.1843e-18 s^-1
RHO_C = 3.0 * H0 ** 2 / (8.0 * np.pi * G)
DELTA_V = 200.0
OM_B, OM_C = 0.02237, 0.14237      # CFG515 cfg515_lib.py:15 [EXT]
FB = OM_B / OM_C                   # 0.1571258
R_COSMIC = (1.0 - FB) / FB         # 5.3643272
MSUN_KG = MSUN

CONSTANTS = [
    dict(name="G", value=G, unit="m^3 kg^-1 s^-2", source="BRIEF s4"),
    dict(name="c", value=C_LIGHT, unit="m/s", source="BRIEF s4"),
    dict(name="a0_canonical", value=A0, unit="m/s^2", source="BRIEF s4"),
    dict(name="H0", value=H0, unit="s^-1", source="BRIEF s4 (67.4 km/s/Mpc)"),
    dict(name="rho_crit", value=RHO_C, unit="kg/m^3", source="3H0^2/(8 pi G)"),
    dict(name="Delta_v", value=DELTA_V, unit="1", source="BRIEF s4 / A11 K5 convention"),
    dict(name="M_sun", value=MSUN, unit="kg", source="GM_sun/G, BRIEF s4"),
    dict(name="Mpc", value=MPC, unit="m", source="BRIEF s4"),
    dict(name="f_b", value=FB, unit="1", source="CFG515 cfg515_lib.py:15 [EXT]: 0.02237/0.14237"),
    dict(name="R_cosmic", value=R_COSMIC, unit="1", source="(1-f_b)/f_b == Omega_c/Omega_b"),
]

# record inputs (all labelled external)
A_LAW = (1.9102, 0.1186)          # CFG687 MID amplitude, law nu_mono, canonical, 318 eRASS1
A_NEW = (10.17, 0.65)             # CFG687 MID amplitude, Newtonian baryons only, canonical
A_OUT_LAW = (1.0118, 0.0888)      # CFG687 OUTER amplitude, law  (CFG949 K2/K3 restate)
A_OUT_NEW = (7.262, None)         # CFG949 README: Newtonian baryons only, OUTER
A_HUT = (1.0109, 0.0632)          # CFG949 B0 primary corner, supply = 5.364 x catchment
A_HUT_OUT = (1.0469, 0.0888)
F_RET_SEG = "0.10 below 1e12.5; +0.45/decade to 1e13.5; +0.30/decade, cap 0.90"  # CFG416 [EXT]
RECORD = [
    dict(name="A_MID_law", value=A_LAW[0], err=A_LAW[1], source="CFG687 (318 eRASS1 x KiDS), MID band, canonical"),
    dict(name="A_MID_newton", value=A_NEW[0], err=A_NEW[1], source="CFG687, baryons only (law_dsigma with a0=0)"),
    dict(name="A_OUTER_law", value=A_OUT_LAW[0], err=A_OUT_LAW[1], source="CFG687 (restated in CFG949 K2/K3)"),
    dict(name="A_OUTER_newton", value=A_OUT_NEW[0], err=None, source="CFG949 README table"),
    dict(name="A_MID_HUT", value=A_HUT[0], err=A_HUT[1], source="CFG949 B0 primary corner (5.364 supply, untethered NFW)"),
    dict(name="A_OUTER_HUT", value=A_HUT_OUT[0], err=A_HUT_OUT[1], source="CFG949 B0 primary corner"),
    dict(name="f_ret_table", value=None, err=None, source="CFG416 [EXT] via CFG515: " + F_RET_SEG),
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
    """retained fraction, solved implicitly: M_ta = M_b h/(f_ret f_b16)  (A11 s10, CFG416)."""
    K = 0.674 / 0.157                      # h / f_b16
    def g(f):
        return f_ret_tab(math.log10(max(K * Mb_msun / f, 1e-30))) - f
    return brentq(g, 0.10, 0.90, xtol=1e-14, rtol=1e-14)


def n_supply(Mb_msun):
    """N = R_cosmic / f_ret: the supply in units of the system's total baryonic mass."""
    if MUT == "M1":                       # M1: catchment == system
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


def solve_Mb_fixed_Mv(Mv, c, delta=DELTA_V):
    """given (M_v, c): r_v is fixed by M_v, mu by c; solve the enclosed baryon mass."""
    rv = (3.0 * Mv / (4 * math.pi * delta * RHO_C)) ** (1.0 / 3.0)
    mu = (c / (1.0 + c)) ** 2

    def g(lme):
        Me = math.exp(lme)
        return Me * (1.0 + float(F(G * Me / (A0 * rv * rv)))) - Mv
    Me = math.exp(brentq(g, math.log(1e-9 * Mv), math.log(Mv), xtol=1e-15, rtol=1e-15))
    return dict(rv=rv, mu=mu, Me=Me, Mb=Me / mu, Fv=float(F(G * Me / (A0 * rv * rv))), Mv=Mv, c=c)


# ===================================================================================== K1-K4 identities
head("K1-K4  the two identities, exactly (sympy)")

gN, g, a0, y = sp.symbols("g_N g a0 y", positive=True)
g_sol = (gN / 2) * (1 + sp.sqrt(1 + 4 * a0 / gN))
res = sp.simplify(g_sol ** 2 / (g_sol + a0) - gN)
K1 = abs(complex(sp.N(res))) if res.is_number else 0.0
K1 = 0.0 if sp.simplify(res) == 0 else float(abs(sp.N(res)))
check("K1", K1 < 1e-30, f"{K1:.1e}", "<1e-30", "g=(g_N/2)(1+sqrt(1+4a0/g_N)) is an exact root of g_N=g^2/(g+a0)")

# M_ph/M_b = g/g_N - 1 with y = g_N/a0
Fexpr = sp.simplify(sp.radsimp((g_sol / gN - 1).subs(gN, y * a0)))
Ftarget = sp.Rational(1, 2) * (sp.sqrt(1 + 4 / y) - 1)
K2 = float(abs(sp.N(sp.simplify(Fexpr - Ftarget))))
check("K2", K2 < 1e-25, f"{K2:.1e}", "<1e-25", "M_ph/M_b = g/g_N-1 = (1/2)(sqrt(1+4/y)-1) exactly")

# closed-form inverse: F(4/((2R+1)^2-1)) == R exactly
Rsym = sp.Symbol("R", positive=True)
yinv = 4 / ((2 * Rsym + 1) ** 2 - 1)
K3a = float(abs(sp.N(sp.simplify(Ftarget.subs(y, yinv) - Rsym))))
YSTAR = float(yinv.subs(Rsym, R_COSMIC))
K3b = abs(float(F(YSTAR)) - R_COSMIC)
check("K3", (K3a < 1e-25 and K3b < 1e-12), f"{K3b:.1e}", "<1e-12",
      f"F(y*)=R_cosmic exactly at y*={YSTAR:.9f}; closed-form inverse verified")

RM_OVER_R = 1.0 / math.sqrt(YSTAR)
check("K4", abs(RM_OVER_R - 5.8429730266) < 1e-9, f"{RM_OVER_R:.9f}", "5.842973027+-1e-9",
      "5.364327 is the law's ratio at r = 5.84297 r_M (A11 K4b)")

# ===================================================================================== K5 A11 anchors
head("K5-K6  reproduce the two published ratios (A11 K5 table)")

anchors = {}
for nm, Mb, a in [("MW", 6.0e10 * MSUN, 4.0 * KPC), ("cluster", 1.4e14 * MSUN, 250.0 * KPC)]:
    rv = solve_rv_fixed_a(Mb, a)
    Me = mb_enc(Mb, a, rv)
    Fv = float(F(G * Me / (A0 * rv * rv)))
    c = rv / a
    mu = (c / (1 + c)) ** 2
    anchors[nm] = dict(Mb=Mb / MSUN, a_kpc=a / KPC, rv_Mpc=rv / MPC, Mv=(Me * (1 + Fv)) / MSUN,
                       mu=mu, F_enc=Fv, R_tot=mu * (1 + Fv) - 1, y=G * Me / (A0 * rv * rv), c=c)

mw, cl = anchors["MW"], anchors["cluster"]
K5 = max(abs(mw["R_tot"] - 25.04) / 25.04, abs(cl["R_tot"] - 2.62) / 2.62,
         abs(mw["rv_Mpc"] - 0.2455) / 0.2455, abs(cl["rv_Mpc"] - 1.6863) / 1.6863)
check("K5", K5 < 2e-3, f"{K5:.2e}", "<2e-3",
      "MW r_v=0.2455 Mpc R_tot=25.04 ; cluster r_v=1.6863 Mpc R_tot=2.62 (A11 K5)")

SPREAD = mw["R_tot"] / cl["R_tot"]
check("K6", SPREAD > 2.0, f"{SPREAD:.4f}", ">2",
      "the law's ratio is not universal: MW/cluster = 9.57 (A11: 9.566)")

P("")
for nm in ("MW", "cluster"):
    d = anchors[nm]
    P(f"  {nm:8s} Mb={d['Mb']:.4e} Msun  a={d['a_kpc']:.1f} kpc  r_v={d['rv_Mpc']:.5f} Mpc  "
      f"M_v={d['Mv']:.4e} Msun  c={d['c']:.2f}  y_v={d['y']:.6f}")
    P(f"           mu={d['mu']:.5f}  F(y_v)={d['F_enc']:.4f}  R_tot=mu(1+F)-1={d['R_tot']:.4f}")

# ===================================================================================== K7-K10 the grid
head("K7-K9  the (M_v, c) grid: where the law's ratio equals 5.364, and which side is which")

CGRID = [4.0, 7.0, 10.0, 20.0, 40.0, 100.0]
MV_GRID = [10.0 ** k * MSUN for k in np.arange(8.0, 15.01, 0.5)]

# crossing mass for R_enc (ratio to enclosed baryons) -- claimed c-independent
def cross_Mv(c):
    def h(lmv):
        Mv = math.exp(lmv)
        s = solve_Mb_fixed_Mv(Mv, c)
        return float(F(G * s["Me"] / (A0 * s["rv"] ** 2))) - R_COSMIC
    return math.exp(brentq(h, math.log(1e10 * MSUN), math.log(1e19 * MSUN), xtol=1e-14, rtol=1e-14))


cross = {c: cross_Mv(c) for c in CGRID}
vals = np.array([cross[c] / MSUN for c in CGRID])
K7 = float(np.max(np.abs(vals / vals.mean() - 1.0)))
check("K7", K7 < 1e-9, f"{vals.mean():.6e}", "spread<1e-9",
      "R_enc = 5.364 exactly at M_v = 1.7584e14 Msun, INDEPENDENT of concentration")

# crossing mass for R_tot (ratio to the system's total baryons) -- c-dependent
def cross_Mv_tot(c):
    def h(lmv):
        s = solve_Mb_fixed_Mv(math.exp(lmv), c)
        return s["mu"] * (1 + s["Fv"]) - 1.0 - R_COSMIC
    return math.exp(brentq(h, math.log(1e12 * MSUN), math.log(1e18 * MSUN), xtol=1e-14, rtol=1e-14))


cross_tot = {c: cross_Mv_tot(c) / MSUN for c in CGRID}
K8 = (cross_tot[4.0] < cross_tot[100.0] < vals.mean())
check("K8", K8, f"{cross_tot[4.0]:.3e} -> {cross_tot[100.0]:.3e}", f"both < {vals.mean():.3e}",
      "R_tot = 5.364 needs LESS mass at low c (mu<1): crossing runs 3.8e13 (c=4) to 1.6e14 (c=100)")

# grid table
grid = []
for c in CGRID:
    for Mv in MV_GRID:
        s = solve_Mb_fixed_Mv(Mv, c)
        Nn = n_supply(s["Mb"] / MSUN)
        grid.append(dict(c=c, Mv_Msun=s["Mv"] / MSUN, Mb_Msun=s["Mb"] / MSUN, rv_Mpc=s["rv"] / MPC,
                         F_enc=s["Fv"], R_tot=s["mu"] * (1 + s["Fv"]) - 1, f_ret=f_ret_of(s["Mb"] / MSUN),
                         N=Nn, u=(s["mu"] * (1 + s["Fv"]) - 1) / Nn,
                         sign_enc="+" if s["Fv"] > R_COSMIC else "-",
                         sign_tot="+" if (s["mu"] * (1 + s["Fv"]) - 1) > R_COSMIC else "-"))

# monotonicity + sign structure
mono = True
for c in CGRID:
    sub = [r for r in grid if r["c"] == c]
    d = np.diff([r["F_enc"] for r in sub])
    mono = mono and bool(np.all(d < 0))
lo = [r for r in grid if abs(r["c"] - 7.0) < 1e-12 and abs(math.log10(r["Mv_Msun"]) - 8.0) < 1e-9][0]
hi = [r for r in grid if abs(r["c"] - 7.0) < 1e-12 and abs(math.log10(r["Mv_Msun"]) - 15.0) < 1e-9][0]
K9 = mono and (lo["F_enc"] > R_COSMIC) and (hi["F_enc"] < R_COSMIC)
check("K9", K9, f"{lo['F_enc']:.3e} -> {hi['F_enc']:.3f}", "monotone, sign + at 1e8, - at 1e15",
      "F_enc falls monotonically: OVER-supplies below 1.758e14, UNDER-supplies above")

P("")
P("  grid of R_enc = M_ph(<r_v)/M_b(<r_v) and R_tot = M_ph(<r_v)/M_b,total   [R_cosmic = 5.364327]")
P(f"  {'log10 M_v':>10} | " + " | ".join(f"c={c:<5g}".rjust(20) for c in CGRID))
for k in np.arange(8.0, 15.01, 1.0):
    row = []
    for c in CGRID:
        r = [q for q in grid if abs(q["c"] - c) < 1e-12 and abs(math.log10(q["Mv_Msun"]) - k) < 1e-9][0]
        row.append(f"{r['F_enc']:8.3f}/{r['R_tot']:7.3f}")
    P(f"  {k:10.1f} | " + " | ".join(v.rjust(20) for v in row))

P("")
P("  crossing masses (Msun):")
P("    R_enc = 5.364 : " + ", ".join(f"c={c:g}: {cross[c]/MSUN:.4e}" for c in CGRID))
P("    R_tot = 5.364 : " + ", ".join(f"c={c:g}: {cross_tot[c]:.4e}" for c in CGRID))

# ===================================================================================== K10-K12 sourcing fraction
head("K10-K12  the sourcing fraction u = R_tot / N")

def solve_rv_fixed_c(Mb, c, delta=DELTA_V):
    """self-consistent virial radius at fixed concentration c = r_v/a."""
    def g(lr):
        r = math.exp(lr)
        a = r / c
        Me = mb_enc(Mb, a, r)
        return Me * (1.0 + float(F(G * Me / (A0 * r * r)))) - (4 * math.pi / 3) * delta * RHO_C * r ** 3
    return math.exp(brentq(g, math.log(1e-8 * MPC), math.log(1e3 * MPC), xtol=1e-15, rtol=1e-15))


def R_tot_at(Mb, c=7.0):
    rv = solve_rv_fixed_c(Mb, c)
    a = rv / c
    Me = mb_enc(Mb, a, rv)
    Fv = float(F(G * Me / (A0 * rv * rv)))
    mu = (c / (1 + c)) ** 2
    return dict(rv=rv, Mv=Me * (1 + Fv), Fv=Fv, mu=mu, R_tot=mu * (1 + Fv) - 1)


u_mw = mw["R_tot"] / n_supply(mw["Mb"])
u_cl = cl["R_tot"] / n_supply(cl["Mb"])
K10 = (abs(u_mw - 0.467) < 0.01) and (abs(u_cl - 0.439) < 0.01) and (u_mw < 1) and (u_cl < 1)
check("K10", K10, f"MW {u_mw:.4f} / cl {u_cl:.4f}", "0.467 / 0.440 +-0.01",
      "u = R_tot/N: MW 0.467, cluster 0.440 -- the law's phantom is ~45% of the supply, not 100%")

# scan in M_b at c = 7 (representative) -- where the supply stops covering the phantom
MB_SCAN = [10.0 ** k * MSUN for k in np.arange(8.0, 15.01, 0.25)]
scan = []
for Mb in MB_SCAN:
    s = R_tot_at(Mb, 7.0)
    Nn = n_supply(Mb / MSUN)
    scan.append(dict(Mb_Msun=Mb / MSUN, Mv_Msun=s["Mv"] / MSUN, R_tot=s["R_tot"], f_ret=f_ret_of(Mb / MSUN),
                     N=Nn, u=s["R_tot"] / Nn, rv_Mpc=s["rv"] / MPC))
u_scan = np.array([r["u"] for r in scan])
win = [r for r in scan if 1e10 <= r["Mb_Msun"] <= 1e14]
u_win = np.array([r["u"] for r in win])
K11 = bool(np.all(u_win > 0.35) and np.all(u_win < 0.75) and (u_win.max() / u_win.min() < 2.0))
check("K11", K11, f"u in [{u_win.min():.3f},{u_win.max():.3f}]", "[0.35,0.75], max/min<2.0",
      "over M_b=1e10..1e14 (c=7): u stays in 0.39-0.72 -- the law carries ~half the supply, never all of it")


def u_one(lmb):
    Mb = math.exp(lmb) * MSUN
    return R_tot_at(Mb, 7.0)["R_tot"] / n_supply(Mb / MSUN) - 1.0


try:
    MB_CRIT = math.exp(brentq(u_one, math.log(1e8), math.log(1e12), xtol=1e-12))  # Msun
    u_crit_Mv = R_tot_at(MB_CRIT * MSUN, 7.0)["Mv"] / MSUN
    K12 = (u_one(math.log(1e8)) > 0) and (u_one(math.log(1e12)) < 0) and (1e9 < MB_CRIT < 3e9)
except ValueError:                      # no crossing: u never reaches 1 (the M1 mutation)
    MB_CRIT, u_crit_Mv, K12 = float("nan"), float("nan"), False
check("K12", K12, f"M_b={MB_CRIT:.3e}", "1e9..3e9",
      f"u=1 at M_b={MB_CRIT:.2e} (M_v={u_crit_Mv:.2e}): below it the law demands more cold energy than the whole catchment holds")

P("")
P(f"  u = R_tot/N at the two anchors: MW {u_mw:.4f}, cluster {u_cl:.4f}   (u<1: supply covers the phantom)")
P(f"  c=7 scan, M_b = 1e10..1e14: u in [{u_win.min():.3f},{u_win.max():.3f}]")
P(f"  u = 1 (law's phantom exhausts the entire catchment) at M_b = {MB_CRIT:.3e} Msun, M_v = {u_crit_Mv:.3e} Msun")
P("")
P(f"  {'log10 M_b':>9} {'log10 M_v':>9} {'R_tot':>9} {'f_ret':>6} {'N':>8} {'u':>7}")
for r in scan[::2]:
    P(f"  {math.log10(r['Mb_Msun']):9.2f} {math.log10(r['Mv_Msun']):9.2f} {r['R_tot']:9.3f} "
      f"{r['f_ret']:6.3f} {r['N']:8.3f} {r['u']:7.4f}")

# ===================================================================================== K13-K16 cluster
head("K13-K16  the cluster: shortfall in dex, and the record's own amplitude algebra")

SHORT_COSMIC = math.log10(R_COSMIC / cl["R_tot"])
check("K13", abs(SHORT_COSMIC - 0.3113) < 1e-3, f"{SHORT_COSMIC:.4f}", "0.3113+-1e-3",
      "cosmic share / law at cluster = 2.047x = 0.311 dex short")

# exact algebra on the record's three amplitudes (same weights, same bands)
f_band = 1.0 - A_LAW[0] / A_NEW[0]
lam_req = A_LAW[0] * (A_NEW[0] - 1.0) / (A_NEW[0] - A_LAW[0])
# error propagation
if MUT == "M2":
    lam_req = A_LAW[0]                       # M2: read A as lambda
dlam_dA = (A_NEW[0] - 1.0) * A_NEW[0] / (A_NEW[0] - A_LAW[0]) ** 2
dlam_dN = A_LAW[0] * (1.0 - A_LAW[0]) / (A_NEW[0] - A_LAW[0]) ** 2
sig_lam = math.hypot(dlam_dA * A_LAW[1], dlam_dN * A_NEW[1])
K14 = (lam_req / A_LAW[0] > 1.05) and (lam_req / A_LAW[0] < 1.20)
check("K14", K14, f"lambda/A={lam_req/A_LAW[0]:.4f}", "1.05<.<1.20",
      "lambda_req = A(A_n-1)/(A_n-A) = 2.120, NOT A itself: the amplitude is on the TOTAL signal")

R_REQ = lam_req * cl["R_tot"]
sig_R = sig_lam * cl["R_tot"]
dev_cos = abs(R_REQ - R_COSMIC) / sig_R
dev_law = abs(R_REQ - cl["R_tot"]) / sig_R
K15 = (dev_cos < 1.0) and (dev_law > 3.0)
check("K15", K15, f"{R_REQ:.3f}+-{sig_R:.3f}", "<1 sigma from 5.364, >3 sigma from 2.62",
      f"required M_ph/M_b = {R_REQ:.3f}: {dev_cos:.2f} sigma from 5.364, {dev_law:.1f} sigma from 2.62")

f_band_err = math.hypot(A_LAW[1] / A_NEW[0], A_LAW[0] * A_NEW[1] / A_NEW[0] ** 2)

# the same share in 3D mass at the MID band centre (R = 0.8 Mpc) -- for comparison with the
# Delta-Sigma-weighted 0.812; not used in any check
R_MID = 0.8 * MPC
_Mm = mb_enc(1.4e14 * MSUN, 250.0 * KPC, R_MID)
_Fm = float(F(G * _Mm / (A0 * R_MID * R_MID)))
f_MID_3D = _Fm / (1.0 + _Fm)
K16 = abs(f_band - 0.8122) < 0.01
check("K16", K16, f"{f_band:.4f}", "0.8122+-0.01",
      "phantom's share of the law's total Delta-Sigma in MID, from A_law/A_newton (no model)")

P("")
P(f"  f_band = 1 - A_law/A_newton = {f_band:.4f} +- {f_band_err:.4f}   (law total/baryons = {A_NEW[0]/A_LAW[0]:.3f})")
P(f"  lambda_req = {lam_req:.4f} +- {sig_lam:.4f}   vs lambda_cosmic = {R_COSMIC/cl['R_tot']:.4f}   vs lambda_law = 1")
P(f"  R_req = {R_REQ:.4f} +- {sig_R:.4f}   (law 2.620, cosmic 5.364)")
P(f"  measured shortfall log10(lambda_req) = {math.log10(lam_req):.4f} dex ; "
  f"cosmic shortfall = {SHORT_COSMIC:.4f} dex ; difference {abs(math.log10(lam_req)-SHORT_COSMIC):.4f} dex")

# ===================================================================================== K17-K18 discriminator
head("K17-K18  the discriminator")

A_law_pred = 1.0
A_cos_pred = 1.0 + (R_COSMIC / cl["R_tot"] - 1.0) * f_band
Z_law = (A_LAW[0] - A_law_pred) / A_LAW[1]
Z_cos = (A_LAW[0] - A_cos_pred) / A_LAW[1]
SEP = (A_cos_pred - A_law_pred) / A_LAW[1]
K17 = (Z_law > 5.0) and (abs(Z_cos) < 1.0) and (SEP > 5.0)
check("K17", K17, f"A_pred {A_law_pred:.3f} vs {A_cos_pred:.3f}", f"sep {SEP:.2f} sigma",
      f"measured A_MID={A_LAW[0]:.4f}+-{A_LAW[1]:.4f}: law {Z_law:.2f} sigma, cosmic {Z_cos:.2f} sigma out")

# shape discriminator: MID/OUTER
mo_law = A_LAW[0] / A_OUT_LAW[0]
mo_law_e = mo_law * math.hypot(A_LAW[1] / A_LAW[0], A_OUT_LAW[1] / A_OUT_LAW[0])
mo_hut = A_HUT[0] / A_HUT_OUT[0]
mo_hut_e = mo_hut * math.hypot(A_HUT[1] / A_HUT[0], A_HUT_OUT[1] / A_HUT_OUT[0])
K18 = (abs(mo_law - 1.887) < 0.01) and (abs(mo_hut - 0.966) < 0.01) and (mo_hut < 1.0 < mo_law)
check("K18", K18, f"{mo_hut:.3f}+-{mo_hut_e:.3f} vs {mo_law:.3f}+-{mo_law_e:.3f}", "measured<1<law",
      "shape discriminator: MID/OUTER = 0.97 (native) vs 1.89 (law's phantom); 1 is the fence")

P("")
P(f"  A_MID predictions: cold=phantom {A_law_pred:.3f} ; cold=cosmic share {A_cos_pred:.3f} ; measured {A_LAW[0]:.4f}+-{A_LAW[1]:.4f}")
P(f"  separation {SEP:.2f} sigma ; Delta chi^2 (law - cosmic) = {Z_law**2 - Z_cos**2:.1f}")

# ===================================================================================== K19-K20 postulate
head("K19-K20  the missing rule and its falsifier")

fret_need_mw = R_COSMIC / mw["R_tot"]
fret_need_cl = R_COSMIC / cl["R_tot"]
K19 = (abs(fret_need_mw - 0.2142) < 0.005) and (fret_need_cl > 1.0)
check("K19", K19, f"MW {fret_need_mw:.4f} vs table 0.10 ; cluster {fret_need_cl:.4f}", "cluster >1",
      "u=1 would need f_ret=0.214 (MW, 2.1x the table) and f_ret=2.05 (cluster) -> impossible")

resid_lo, resid_hi = A_HUT[0], 1.21
r_lo = R_COSMIC * (1.0 + (resid_lo - 1.0) / f_band)
r_hi = R_COSMIC * (1.0 + (resid_hi - 1.0) / f_band)
sig_lo = (A_HUT[1] / f_band) * R_COSMIC
K20 = (abs(r_lo - R_COSMIC) / sig_lo < 0.5) and (r_hi / R_COSMIC < 1.30)
check("K20", K20, f"{r_lo:.3f}+-{sig_lo:.3f} .. {r_hi:.3f}", f"|d|<0.5 sigma, hi<1.30x",
      "record's post-5.364 residual A_MID 1.011-1.21 maps to 5.44+-0.42 .. 6.75: no further cold energy needed")

# ===================================================================================== results
N_PASS = sum(1 for c in CHECKS if c["pass_"])
N_TOT = len(CHECKS)
numbers = dict(
    R_cosmic=R_COSMIC, f_b=FB, y_star=YSTAR, r_over_rM=RM_OVER_R,
    MW=dict(rv_Mpc=mw["rv_Mpc"], Mv_Msun=mw["Mv"], mu=mw["mu"], F_enc=mw["F_enc"],
            R_tot=mw["R_tot"], c=mw["c"], y_v=mw["y"], u=u_mw, Mb_Msun=mw["Mb"], a_kpc=mw["a_kpc"]),
    cluster=dict(rv_Mpc=cl["rv_Mpc"], Mv_Msun=cl["Mv"], mu=cl["mu"], F_enc=cl["F_enc"],
                 R_tot=cl["R_tot"], c=cl["c"], y_v=cl["y"], u=u_cl, Mb_Msun=cl["Mb"], a_kpc=cl["a_kpc"]),
    u_postulate=0.45, u_postulate_err=0.03, A_MID_sample=318, A_MID_residual_hi=1.21,
    H0_kms_Mpc=67.4, omega_b=0.02237, omega_m=0.14237,
    lambda_over_A=lam_req / A_LAW[0], K5_rel=K5, falsifier_threshold=1.3,
    f_MID_3D=f_MID_3D, group_factor=None,
    ratio_spread=SPREAD,
    cross_Mv_enc_Msun=float(vals.mean()), cross_Mv_enc_spread=K7,
    cross_Mv_tot_by_c={str(k): v for k, v in cross_tot.items()},
    u_MW=u_mw, u_cluster=u_cl,
    u_window_min=float(u_win.min()), u_window_max=float(u_win.max()),
    Mb_crit_u1_Msun=MB_CRIT, Mv_crit_u1_Msun=u_crit_Mv,
    scan=scan,
    shortfall_cosmic_dex=SHORT_COSMIC,
    f_band=f_band, f_band_err=f_band_err,
    lambda_req=lam_req, lambda_req_err=sig_lam,
    lambda_cosmic=R_COSMIC / cl["R_tot"],
    R_req=R_REQ, R_req_err=sig_R,
    dev_cosmic_sigma=dev_cos, dev_law_sigma=dev_law,
    measured_shortfall_dex=math.log10(lam_req),
    A_pred_law=A_law_pred, A_pred_cosmic=A_cos_pred,
    Z_law=Z_law, Z_cos=Z_cos, separation_sigma=SEP, delta_chi2=Z_law ** 2 - Z_cos ** 2,
    MID_OUTER_law=mo_law, MID_OUTER_law_err=mo_law_e, MID_OUTER_hut=mo_hut, MID_OUTER_hut_err=mo_hut_e,
    fret_need_MW=fret_need_mw, fret_need_cluster=fret_need_cl,
    residual_ratio_lo=r_lo, residual_ratio_hi=r_hi,
    n_grid_points=len(grid),
    R_enc_at_1e8=next(r["F_enc"] for r in grid if abs(r["c"] - 7.0) < 1e-9 and abs(math.log10(r["Mv_Msun"]) - 8.0) < 1e-9),
    R_enc_frac_1e15=next(r["F_enc"] for r in grid if abs(r["c"] - 7.0) < 1e-9 and abs(math.log10(r["Mv_Msun"]) - 15.0) < 1e-9) / R_COSMIC,
    N_anchors=[n_supply(m) for m in (3e10, 1e11, 1e12, 1e13, 1e14)],
    shortfall_diff_dex=abs(math.log10(lam_req) - SHORT_COSMIC),
    MID_OUTER_ratio=mo_law / mo_hut,
    falsifier_sigma=(1.3 - mo_hut) / mo_hut_e,
    group_forecast=dict(Mv_Msun=1e13,
                        R_tot=next(r["R_tot"] for r in grid if abs(r["c"] - 7.0) < 1e-9 and abs(math.log10(r["Mv_Msun"]) - 13.0) < 1e-9),
                        N=next(r["N"] for r in grid if abs(r["c"] - 7.0) < 1e-9 and abs(math.log10(r["Mv_Msun"]) - 13.0) < 1e-9)),
)

numbers["group_factor"] = numbers["group_forecast"]["N"] / numbers["group_forecast"]["R_tot"]
res = dict(lane=LANE, status="NO-GO(obstruction) + DECIDABLE", checks=[
    dict(id=c["id"], **{"pass": c["pass_"]}, value=c["value"], threshold=c["threshold"], label=c["label"])
    for c in CHECKS], numbers=numbers,
    constants_used=CONSTANTS, record_inputs=RECORD,
    grid=grid, mutation=MUT or None,
    runtime_s=round(time.time() - T0, 2))

with open(os.path.join(HERE, "a18_results" + TAG + ".json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)

head("SUMMARY")
P(f"  R_cosmic = (1-f_b)/f_b = {R_COSMIC:.6f}   y* = {YSTAR:.9f}   r*/r_M = {RM_OVER_R:.6f}")
P(f"  law at r_v: MW R_tot={mw['R_tot']:.3f}  cluster R_tot={cl['R_tot']:.3f}  (spread {SPREAD:.3f}x)")
P(f"  crossing (enclosed-baryon denominator): M_v = {vals.mean():.4e} Msun, c-independent to {K7:.1e}")
P(f"  u = R_tot/N: MW {u_mw:.3f}, cluster {u_cl:.3f}; window 1e10-1e14 [{u_win.min():.3f},{u_win.max():.3f}]; u=1 at M_b={MB_CRIT:.2e}")
P(f"  cluster shortfall: cosmic/law = {R_COSMIC/cl['R_tot']:.3f}x = {SHORT_COSMIC:.3f} dex")
P(f"  record inversion: lambda_req = {lam_req:.3f}+-{sig_lam:.3f} -> R_req = {R_REQ:.3f}+-{sig_R:.3f}")
P(f"  discriminator: A_MID {A_law_pred:.3f} vs {A_cos_pred:.3f} (measured {A_LAW[0]:.3f}+-{A_LAW[1]:.3f}), {SEP:.1f} sigma")
P("")
P(f"{LANE} COMPLETE: {N_PASS}/{N_TOT} checks PASS.")
OUTF.close()
sys.exit(0 if N_PASS == N_TOT else 1)
