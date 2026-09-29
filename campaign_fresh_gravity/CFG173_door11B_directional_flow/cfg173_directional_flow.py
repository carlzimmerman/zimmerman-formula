#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG173 -- door 11, variant 11B': a compressible directional flow of a massless Lambda-medium.  ONE script for the lane.

Frozen criteria: FROZEN_CRITERIA.md in this directory (written before any script or number).  The governing file is
closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md (gates, addenda 1-2, erratum 1).  Nothing in the record is edited;
CFG4_common (constants, P2) and CFG7_common (Report, Omega_m) are imported READ-ONLY.

Target (erratum 1): P2 is primary, g_tot^2 = g_N^2 + a0 g_N; the phantom a_ph = g_tot - g_N.  Point mass: s(x) = a_ph/a0 =
(sqrt(1 + x^2) - 1)/x^2, x = r/r_M, r_M = sqrt(G M/a0).  The simple kernel nu = 1/2 + sqrt(1/4 + 1/y) is reported.
a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED; both footings and rho_Lambda are read from CFG4_common (canonical primary,
alt reported; rho_Lambda is the same number on both footings -- only a0 changes).  Exponential sphere: rho = M/(8 pi h^3)
exp(-r/h), h = 2 kpc at every mass.  G1 grid: x = 25 log points on [0.1, 30]; M = 1e9..1e12 Msun; theta = 0, 45, 90, 135, 180
deg from the upstream axis; the flow moves along -z ("from the top"), so upstream is +z (theta < 90).

  S1  (H-A, V1; sympy) a w = -1 medium has no flow: eta is boost-invariant, T^{01} = (1 + w) rho gamma^2 c v = 0 for every v,
      and the Euler coefficient (energy density + p) = (1 + w) rho c^2 = 0.
  S2  (H-B, reading T1) the gravity of the flow's own energy, g_ach, against a_ph on the grid (R = g_ach/a_ph):
      V1' (near-vacuum field, eps = 0.1, c_s^2 = 1e-4 c^2, hydrostatic), V2 (a null flux lensed by a point mass; point mass
      only), V3 (a radiation fluid, hydrostatic); u in {rho_Lambda c^2, P_cap = kappa^2/(8 pi) rho_Lambda c^2}.
  S3  (H-C, reading T2: push) V2's directional shadow push on the exponential sphere (thin absorber, relative to the galaxy's
      CM), normalised once at M = 1e11, x = 1; V3's isotropic Le Sage bath; energy (G3), optical depths (G5c), drag (G6), G2.
  S4  (H-D, reading T3: V4, the granted flux law, a declared RESTATEMENT) the stream's first-order l = 1 dipole (G8b), the
      second-order monopole (G7), the l = 2 BVP plus the l = 0 spread (G8a), the sink's energy and momentum (G3), the sound
      speed (G5a), the inherited Sun tail (G5b, CFG185) and the preferred-frame acceleration at 1 AU (G6).
  Gate matrix: V1, V1'(T1), V2(T1), V2(T2), V3(T1), V3(T2), V4(T3) x G1..G8.

Controls (load-bearing): C1 F(s(x)) x^2 = 1 (sympy for P2; numeric 1e-12 for P2 and simple); C2 the deep l = 1 ODE has
exactly the solutions x and 1/x; C3 the point-lens magnification (lens equation, 1 + 2/u^4, and the lensing integral);
C4 S3's normalisation reproduces its target to 1e-6; C5 the second-order flux expansion (and C5b its angular projections);
C6 the deep l = 2 particular solution (2/3) x^2.
MUTATE (environment variable MUTATE, popped before CFG4_common is imported; unset or "0" is the main run):
  A  w = -0.9 in S1            -> S1b and S1c must FAIL
  B  every g_ach x 1e12 in S2  -> S2's "short everywhere" checks must FAIL
  C  V2's field made isotropic (a_in = G_LS M(<r)/r^2, same normalisation) -> S3a (sign change) must FAIL
  D  V4's law F = s^2 everywhere (s = 1/x, no stiff core; the l = 1 ODE starts at f = x0, f' = 1) -> S4-D must FAIL
Outputs (in this directory): cfg173_directional_flow[_MUTATE_X].out and ..._results.json.  Exit 1 if a load-bearing check
fails.  Runs in about half a minute.
"""
import os
import sys
import math
import time

sys.dont_write_bytecode = True                                   # never write a __pycache__ into the record
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.environ.get("CFG173_CFGDIR") or os.path.dirname(LANE)
sys.path.insert(0, CFG)

# this script's own mode: MUTATE is popped BEFORE CFG4_common is imported (CFG4_common reads MUTATE at import time for its own
# harness) and restored afterwards.
_MUT = os.environ.pop("MUTATE", None)
MODE = "" if _MUT in (None, "", "0") else _MUT.strip()
if MODE not in ("", "A", "B", "C", "D"):
    raise SystemExit(f"CFG173: unknown MUTATE mode {_MUT!r}; allowed: A, B, C, D (or unset)")
try:
    import CFG4_common as C4                                     # noqa: E402  (read-only: constants, P2, footings)
    import CFG7_common as C7                                     # noqa: E402  (read-only: Report, OM_PL, H_PL)
finally:
    if _MUT is not None:
        os.environ["MUTATE"] = _MUT

import numpy as np                                               # noqa: E402
import sympy as sp                                               # noqa: E402
from scipy.integrate import quad, solve_ivp, solve_bvp, cumulative_trapezoid, simpson   # noqa: E402
from scipy.special import gammainc, k1e                          # noqa: E402

R = C7.Report("cfg173_directional_flow" + (f"_MUTATE_{MODE}" if MODE else ""), False)
P, banner, check = R.P, R.banner, R.check
T0 = time.time()

# ================================================================================================================ constants
KAPPA = 0.5                                                      # FITTED (never derived)
assert KAPPA == C4.KAPPA
G, C, MSUN = C4.G_SI, C4.C_SI, C4.MSUN
KPC, MPC = C4.KPC, C4.MPC
FOOTS = tuple(C4.FOOTS)                                          # ("canonical", "alt"); canonical is primary
A0 = {f: float(C4.A0[f]) for f in FOOTS}
RHO_L = float(C4.RHO_LAMBDA)
U_L = RHO_L * C ** 2                                             # rho_Lambda c^2 (the Lambda tie)
P_CAP = KAPPA ** 2 / (8.0 * math.pi) * U_L                       # P_cap = kappa^2/(8 pi) rho_Lambda c^2
UVALS = (("rhoLc2", U_L), ("Pcap", P_CAP))
SQ_GRHO = math.sqrt(G * RHO_L)                                   # sqrt(G rho_Lambda)
H0 = 67.36e3 / MPC                                               # s^-1
T_H = 1.0 / H0
OM = C7.OM_PL                                                    # 0.3153
OL = 1.0 - OM
AU, R_SUN, M_EARTH, R_EARTH = 1.495978707e11, 6.957e8, 5.972e24, 6.371e6
V_EARTH, W_SUN, A_RAD = 29.78e3, 370e3, 7.5657e-16
H_EXP = 2.0 * KPC                                                # the exponential sphere's h at every mass
EPS_V1P, CS2_V1P = 0.1, 1e-4 * C ** 2                            # V1' at its most compressible corner
ALPHA2, ALPHA1 = 1.6e-9, 3.5e-5                                  # declared citations (Shao et al. 2013; Shao & Wex 2012)
DAR_EARTH, DAR_MARS = 3.66e-14, 3.72e-14                         # planetary delta A_R bounds, as cited by CFG185 (STANDING)
MB_FAC = 1e12 if MODE == "B" else 1.0                            # MUTATE B: every achieved g multiplied by 1e12
XG = np.logspace(np.log10(0.1), np.log10(30.0), 25)              # the G1 x grid
MASSES = (1e9, 1e10, 1e11, 1e12)                                 # Msun
THETAS = (0.0, 45.0, 90.0, 135.0, 180.0)                         # deg from the upstream axis (+z)
KERNS = ("P2", "simple")
XF = np.geomspace(0.1, 30.0, 2001)                               # fine x grid for S4 maxima
GM_SUN = G * MSUN
G_SUN_AU = GM_SUN / AU ** 2
SC_A2 = 0.5 * ALPHA2 * (W_SUN / C) ** 2 * G_SUN_AU                # alpha2-type scale at 1 AU
SC_A1 = 0.5 * ALPHA1 * (W_SUN * V_EARTH / C ** 2) * G_SUN_AU      # alpha1-type scale at 1 AU

P(f"CFG173 -- door 11B': a compressible directional flow of a massless Lambda-medium   (mode: {'MAIN' if not MODE else 'MUTATE_' + MODE})")
P(f"  CFG dir: {os.path.basename(CFG)} (read-only imports: CFG4_common, CFG7_common)")
P(f"  a0: canonical {A0['canonical']:.5e}, alt {A0['alt']:.5e} m/s^2;  rho_Lambda = {RHO_L:.5e} kg/m^3;  kappa = 1/2 FITTED")
P(f"  rho_L c^2 = {U_L:.5e} J/m^3;  P_cap = kappa^2/(8 pi) rho_L c^2 = {P_CAP:.5e} J/m^3;  sqrt(G rho_L) = {SQ_GRHO:.5e} 1/s")
P(f"  kappa c sqrt(G rho_L) = {KAPPA * C * SQ_GRHO:.5e} (canonical a0 check);  t_H = 1/H0 (67.36) = {T_H:.4e} s;  Omega_m = {OM}")
R.num("constants", dict(a0=A0, rho_L=RHO_L, u_L=U_L, P_cap=P_CAP, t_H=T_H, Omega_m=OM, h_exp_kpc=2.0, eps_V1p=EPS_V1P,
                        cs2_over_c2_V1p=1e-4, alpha2=ALPHA2, alpha1=ALPHA1, mode=MODE))


# ================================================================================================================ kernels, profiles
def nu_simple(y):
    """the simple kernel nu = 1/2 + sqrt(1/4 + 1/y) (reported; not the primary)."""
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


NU = {"P2": C4.nu_p2, "simple": nu_simple}                        # P2 is CFG4_common's own nu = sqrt(1 + 1/y)


def g_tot(gN, a0, kern):
    return NU[kern](gN / a0) * gN


def a_ph(gN, a0, kern):
    return (NU[kern](gN / a0) - 1.0) * gN


def s_point(x, kern="P2"):
    """point-mass phantom / a0, in the cancellation-free form: P2 1/(sqrt(1+x^2)+1); simple 1/(sqrt(1/4+x^2)+1/2)."""
    x = np.asarray(x, float)
    return 1.0 / (np.sqrt(1.0 + x * x) + 1.0) if kern == "P2" else 1.0 / (np.sqrt(0.25 + x * x) + 0.5)


def r_M(Msun, foot="canonical"):
    return math.sqrt(G * Msun * MSUN / A0[foot])


def M_enc_exp(r, Mkg, h=H_EXP):
    """M(<r) = M [1 - e^{-r/h}(1 + r/h + r^2/(2h^2))] = M P(3, r/h) (the regularised incomplete gamma: no cancellation)."""
    return Mkg * gammainc(3.0, np.asarray(r, float) / h)


def Phi_exp(r, Mkg, h=H_EXP):
    """|Phi_N| of the exponential sphere: G M(<r)/r + G M (r + h) e^{-r/h}/(2 h^2)."""
    r = np.asarray(r, float)
    return G * M_enc_exp(r, Mkg, h) / r + G * Mkg * (r + h) * np.exp(-r / h) / (2.0 * h * h)


def rho_exp(r, Mkg, h=H_EXP):
    return Mkg / (8.0 * math.pi * h ** 3) * np.exp(-np.asarray(r, float) / h)


def gN_prof(prof, Msun, r):
    Mkg = Msun * MSUN
    return G * Mkg / np.asarray(r, float) ** 2 if prof == "point" else G * M_enc_exp(r, Mkg) / np.asarray(r, float) ** 2


def lab_g6(a):
    """G6: PASS below the alpha2 scale; FAIL above the alpha1 scale; UNDECIDED between."""
    return "PASS" if a < SC_A2 else ("FAIL" if a > SC_A1 else "UNDECIDED")


def lab_g8b(d):
    return "PASS" if d <= 0.02 else ("FAIL" if d > 0.10 else "UNDECIDED")


# a few reported sanity checks on the building blocks
_q = np.array([0.05, 0.5, 2.0, 7.0, 30.0])
_d = np.max(np.abs(gammainc(3.0, _q) - (1 - np.exp(-_q) * (1 + _q + _q ** 2 / 2))))
check("aux: M(<r) as gammainc(3, r/h) equals the frozen closed form M[1 - e^{-q}(1 + q + q^2/2)]",
      f"max |difference| over q in {list(_q)} = {_d:.2e}", _d < 1e-13, load_bearing=False)
_y = np.geomspace(1e-3, 1e3, 7)
_d = float(np.max(np.abs(C4.nu_p2(_y) - np.sqrt(1 + 1 / _y))))
check("aux: CFG4_common.nu_p2 is P2 (nu = sqrt(1 + 1/y), erratum 1)", f"max |nu_p2 - sqrt(1+1/y)| = {_d:.1e}", _d < 1e-14,
      load_bearing=False)

# ================================================================================================================ S1
banner("S1 (H-A, variant V1: w = -1) -- does a vacuum-like medium flow at all?  (sympy)")
W_S1 = sp.Rational(-9, 10) if MODE == "A" else sp.Integer(-1)
P(f"  variant w = {W_S1}" + ("   [MUTATE A: w = -0.9]" if MODE == "A" else ""))
phi, vv, cc, rho = sp.symbols("phi v c rho", positive=True)
wsym = sp.symbols("w", real=True)
Lam = sp.Matrix([[sp.cosh(phi), sp.sinh(phi), 0, 0], [sp.sinh(phi), sp.cosh(phi), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
eta = sp.diag(-1, 1, 1, 1)
dS1a = sp.simplify(Lam * eta * Lam.T - eta)
ok_s1a = dS1a == sp.zeros(4, 4)
check("S1a: a boost Lambda along x (rapidity phi) leaves eta = diag(-1,1,1,1) invariant, so T = -rho c^2 eta is the same in every frame",
      f"Lambda eta Lambda^T - eta simplifies to {'the zero matrix' if ok_s1a else dS1a}", ok_s1a)
gam = 1 / sp.sqrt(1 - vv ** 2 / cc ** 2)
uvec = gam * sp.Matrix([cc, vv, 0, 0])


def T_fluid(w):
    """perfect fluid T^{mu nu} = (rho + p/c^2) u^mu u^nu + p eta^{mu nu}, p = w rho c^2, u = gamma (c, v, 0, 0)."""
    p_ = w * rho * cc ** 2
    return (rho + p_ / cc ** 2) * uvec * uvec.T + p_ * eta


T01_gen = sp.simplify(T_fluid(wsym)[0, 1] - (1 + wsym) * rho * gam ** 2 * cc * vv)
check("S1b' (control): for general w, T^{01} = (1 + w) rho gamma^2 c v",
      f"T^01 - (1 + w) rho gamma^2 c v simplifies to {T01_gen}", T01_gen == 0)
T01 = sp.simplify(T_fluid(W_S1)[0, 1])
check(f"S1b: at the variant's w = {W_S1}, T^{{01}} = 0 for every v (no momentum or energy flux in any frame)",
      f"T^01(w = {W_S1}) = {T01}", T01 == 0)
euler_coef = sp.simplify(rho * cc ** 2 + W_S1 * rho * cc ** 2)
check(f"S1c: at w = {W_S1} the relativistic Euler coefficient (energy density + p) = (1 + w) rho c^2 vanishes",
      f"(rho c^2 + p) = {euler_coef};  so (eps + p) u^nu d_nu u^mu = -h^{{mu nu}} d_nu p reduces to h^{{mu nu}} d_nu p = 0",
      euler_coef == 0)
S1_NOFLOW = bool(ok_s1a and T01 == 0 and euler_coef == 0)
P(f"  S1 reading: {'no rest frame, no energy or momentum flux, no compression -- a w = -1 medium cannot flow (H-A holds)' if S1_NOFLOW else 'at this w a flow EXISTS (T^01 != 0): H-A does not apply'}")
R.num("S1", dict(w=str(W_S1), T01=str(T01), euler_coef=str(euler_coef), no_flow=S1_NOFLOW))

# ================================================================================================================ S2
banner("S2 (H-B, reading T1): the gravity of the flow's own energy, g_ach, against the phantom a_ph on the G1 grid")
P(f"  V3  radiation fluid, hydrostatic: du/u = 4|Phi_N|/c^2, active density 2 du/c^2; point mass g = 16 pi G^2 M u/c^4")
P(f"  V1' near-vacuum field (eps = {EPS_V1P}, c_s^2 = 1e-4 c^2): d rho = eps rho_L |Phi_N|/c_s^2, active factor (1 + 3 c_s^2/c^2)")
P(f"  V2  null flux lensed by a point mass: excess u_F (A(u) - 1) downstream, zero upstream (point mass only, as declared)")
P(f"  both profiles for V1', V3 (point mass, exp sphere h = 2 kpc); u in {{rho_L c^2, P_cap}} for V2, V3")
if MODE == "B":
    P("  [MUTATE B: every g_ach multiplied by 1e12]")


def lens_I(U):
    """int_0^U (A(u) - 1) u du = (U/2)(sqrt(U^2 + 4) - U), written cancellation-free as 2U/(sqrt(U^2 + 4) + U)."""
    return 2.0 * U / (math.sqrt(U * U + 4.0) + U)


def lens_J(Q):
    """J(Q) = int_0^1 t I(U(t)) dt, U = sqrt(Q (1 - t^2)/t), Q = r c^2/(4 G M): M_act(<r) = (16 pi G M u_F/c^4) r^2 J.  -> 1/2."""
    def f(t):
        return t * lens_I(math.sqrt(Q * (1.0 - t * t) / t))
    pts = sorted({p for p in (1e-6, 1e-3, 0.5, 1 - 1e-3, 1 - 100.0 / Q, 1 - 10.0 / Q, 1 - 1.0 / Q) if 0.0 < p < 1.0})
    return quad(f, 0.0, 1.0, points=pts, limit=1000, epsabs=1e-15, epsrel=1e-12)[0]


def I_phi_num(r, Mkg, h=H_EXP):
    """int_0^r |Phi_N(r')| 4 pi r'^2 dr' for the exponential sphere, NUMERICALLY (q = r'/h)."""
    Q = r / h
    f = lambda q: float(gammainc(3.0, q)) * q + 0.5 * (q + 1.0) * q * q * math.exp(-q)
    pts = [p for p in (1.0, 5.0, 20.0, 60.0) if p < Q]
    return 4 * math.pi * h * h * G * Mkg * quad(f, 0.0, Q, points=pts or None, limit=500, epsabs=0.0, epsrel=1e-12)[0]


def I_phi_closed(r, Mkg, h=H_EXP):
    """the same integral in closed form (a check only): 4 pi h^2 G M [Q^2/2 - 2 + e^{-Q}(2 + 2Q + Q^2/2)]."""
    Q = r / h
    return 4 * math.pi * h * h * G * Mkg * (Q * Q / 2 - 2 + math.exp(-Q) * (2 + 2 * Q + Q * Q / 2))


FAC_V1P = (1.0 + 3.0 * CS2_V1P / C ** 2) * EPS_V1P * RHO_L / CS2_V1P   # active density per unit |Phi| (kg/m^3 per m^2/s^2)


def g_ach(mech, prof, Msun, r, u=None):
    """the flow's own extra radial gravity (monopole) at radius r.  MUTATE B multiplies it by 1e12."""
    Mkg = Msun * MSUN
    if mech == "V3":
        g = 16 * math.pi * G ** 2 * Mkg * u / C ** 4 if prof == "point" else G * (8 * u / C ** 4) * I_phi_num(r, Mkg) / r ** 2
    elif mech == "V1p":
        g = 2 * math.pi * G * FAC_V1P * G * Mkg if prof == "point" else G * FAC_V1P * I_phi_num(r, Mkg) / r ** 2
    elif mech == "V2":
        assert prof == "point"
        g = 16 * math.pi * G ** 2 * Mkg * u * lens_J(r * C ** 2 / (4 * G * Mkg)) / C ** 4
    else:
        raise ValueError(mech)
    return g * MB_FAC


# the mechanisms, their u values and profiles
S2_CASES = [("V1p", "-", None, ("point", "exp")), ("V2", "rhoLc2", U_L, ("point",)), ("V2", "Pcap", P_CAP, ("point",)),
            ("V3", "rhoLc2", U_L, ("point", "exp")), ("V3", "Pcap", P_CAP, ("point", "exp"))]
GACH = {}                                   # (mech, ukey, prof, foot) -> array (len(MASSES), len(XG))
for (mech, uk, u, profs) in S2_CASES:
    for prof in profs:
        for foot in FOOTS:
            GACH[(mech, uk, prof, foot)] = np.array([[g_ach(mech, prof, M, x * r_M(M, foot), u) for x in XG] for M in MASSES])

# checks on the building blocks: the closed-form enclosure, and the exp sphere tending to the point mass at r >> h
_rel = max(abs(I_phi_num(x * r_M(M, f), M * MSUN) / I_phi_closed(x * r_M(M, f), M * MSUN) - 1)
           for M in MASSES for x in XG for f in FOOTS)
check("aux: the numerical enclosure int |Phi_N| 4 pi r^2 dr (exp sphere) equals its closed form",
      f"max relative difference over the G1 grid (both footings) = {_rel:.2e}", _rel < 1e-8, load_bearing=False)
_rat = GACH[("V3", "rhoLc2", "exp", "canonical")][-1, -1] / GACH[("V3", "rhoLc2", "point", "canonical")][-1, -1]
check("aux: V3's exp-sphere g_ach tends to the point-mass value far outside h (M = 1e12, x = 30: r/h = "
      f"{30 * r_M(1e12) / H_EXP:.0f}; expected 1 - 4 (h/r)^2)",
      f"ratio = {_rat:.8f}; 1 - 4(h/r)^2 = {1 - 4 * (H_EXP / (30 * r_M(1e12))) ** 2:.8f}",
      abs(_rat - (1 - 4 * (H_EXP / (30 * r_M(1e12))) ** 2)) < 1e-7, load_bearing=False)
_J = [lens_J(x * r_M(M) * C ** 2 / (4 * G * M * MSUN)) for M in (1e9, 1e12) for x in (0.1, 30.0)]
P(f"  V2 lensing: J(Q) = int t I dt (-> 1/2) at (1e9, x=0.1), (1e9, 30), (1e12, 0.1), (1e12, 30): "
  + ", ".join(f"{j:.9f}" for j in _J))

# R = g_ach / a_ph per mechanism, u, kernel, footing, profile; and the G1 (T1) law metric
S2_SUM, S2_MAXR = {}, {}
P(f"\n  {'mech':5s} {'u':7s} {'kern':7s} {'foot':10s} {'profile':6s}  {'max R':>10s} {'at (M, x)':>16s}  {'min R':>10s}  {'max |gN+g_ach-g_tot|/g_tot':>27s}")
for (mech, uk, u, profs) in S2_CASES:
    for kern in KERNS:
        for foot in FOOTS:
            for prof in profs:
                ga = GACH[(mech, uk, prof, foot)]
                aph = np.array([[a_ph(gN_prof(prof, M, x * r_M(M, foot)), A0[foot], kern) for x in XG] for M in MASSES])
                gt = np.array([[g_tot(gN_prof(prof, M, x * r_M(M, foot)), A0[foot], kern) for x in XG] for M in MASSES])
                gn = np.array([[gN_prof(prof, M, x * r_M(M, foot)) for x in XG] for M in MASSES])
                Rr = ga / aph
                i, j = np.unravel_index(np.argmax(Rr), Rr.shape)
                g1 = np.abs(gn + ga - gt) / gt
                key = f"{mech}|{uk}|{kern}|{foot}|{prof}"
                S2_SUM[key] = dict(maxR=float(Rr.max()), minR=float(Rr.min()), argmax=f"M = {MASSES[i]:.0e}, x = {XG[j]:.3g}",
                                   g1_max_err=float(g1.max()), g1_frac_within_10pct=float(np.mean(g1 <= 0.10)),
                                   max_gach_over_gtot=float((ga / gt).max()))
                P(f"  {mech:5s} {uk:7s} {kern:7s} {foot:10s} {prof:6s}  {Rr.max():10.3e} {f'({MASSES[i]:.0e}, {XG[j]:.3g})':>16s}  {Rr.min():10.3e}  {g1.max():27.4f}")

for mech in ("V1p", "V2", "V3"):
    keys = [k for k in S2_SUM if k.startswith(mech + "|") and (mech == "V1p" or "|rhoLc2|" in k)]
    mx = max(S2_SUM[k]["maxR"] for k in keys)
    kx = max(keys, key=lambda k: S2_SUM[k]["maxR"])
    S2_MAXR[mech] = mx
    mname = "V1'" if mech == "V1p" else mech
    check(f"S2 ({mname}, Lambda tie u = rho_L c^2): the flow's own gravity is short everywhere on the G1 grid (max R < 1)",
          f"max R = g_ach/a_ph = {mx:.3e} at {kx} ({S2_SUM[kx]['argmax']});  min over the grid of C_req/C_ach = 1/max R = {1 / mx:.3e}",
          mx < 1.0)
# the required compaction C_req - 1 = a_ph / ((4 pi/3) G rho_act r), rho_act = 2 rho_L (V2, V3) and 2 eps rho_L (V1')
creq = []
for kern in KERNS:
    for foot in FOOTS:
        for prof in ("point", "exp"):
            for M in MASSES:
                for x in XG:
                    r = x * r_M(M, foot)
                    creq.append(a_ph(gN_prof(prof, M, r), A0[foot], kern) / (4 * math.pi / 3 * G * 2 * RHO_L * r))
creq = np.array(creq)
P(f"\n  required compaction C_req - 1 = a_ph/((4 pi/3) G (2 rho_L) r) over the grid (both kernels, footings, profiles): "
  f"min {creq.min():.3e}, max {creq.max():.3e}")
P(f"    (V1', rho_act = 2 eps rho_L: min {creq.min() / EPS_V1P:.3e}, max {creq.max() / EPS_V1P:.3e})")
P(f"  reading: to supply a_ph the medium would need a density excess of {creq.min():.1e} to {creq.max():.1e} times rho_L;"
  f" the mechanisms achieve R <= {max(S2_MAXR.values()):.1e} of it")
R.num("S2", dict(summary=S2_SUM, max_R_at_tie=S2_MAXR, Creq_minus1_min=float(creq.min()), Creq_minus1_max=float(creq.max()),
                 Creq_minus1_V1p_min=float(creq.min() / EPS_V1P), Creq_minus1_V1p_max=float(creq.max() / EPS_V1P)))

# ================================================================================================================ S3
banner("S3 (H-C, reading T2: push) -- V2's directional shadow push, V3's isotropic Le Sage bath")
if MODE == "C":
    P("  [MUTATE C: V2's field replaced by the isotropic mutual-shadowing field a_in = G_LS M(<r)/r^2, same normalisation]")

# ---- the galaxy's mass-weighted mean upstream column, a 2D numerical integral over the sphere's own mass.  In units of
#      Sigma_0 = M/(8 pi h^2): Sigma_up(b, z) = Sigma_0 S(beta, zeta), beta = b/h, zeta = z/h, S = int_zeta^inf e^{-sqrt(beta^2+t^2)} dt,
#      and <S> = (1/4) int_0^inf beta dbeta int dzeta e^{-sqrt(beta^2+zeta^2)} S(beta, zeta).
_Lb, _nb = 40.0, 1601
_b = np.linspace(0.0, _Lb, _nb)
_z = np.linspace(-_Lb, _Lb, 2 * _nb - 1)
_B, _Z = np.meshgrid(_b, _z, indexing="ij")
_f = np.exp(-np.sqrt(_B * _B + _Z * _Z))
_S = cumulative_trapezoid(_f[:, ::-1], -_z[::-1], axis=1, initial=0.0)[:, ::-1]     # int_zeta^L f dt  (tail e^-40 dropped)
S_MEAN = 0.25 * simpson(_b * simpson(_f * _S, x=_z, axis=1), x=_b)
del _B, _Z, _f, _S
check("aux: the 2D numerical <Sigma_up> equals the analytic M/(24 pi h^2) (identity int rho Sigma_up dz = Sigma_tot^2/2 and "
      "int beta^3 K1^2 = 2/3), i.e. <S> = 1/3", f"<S> numeric = {S_MEAN:.10f}; 1/3 = {1 / 3:.10f}; rel. diff {S_MEAN * 3 - 1:.2e}",
      abs(S_MEAN * 3 - 1) < 1e-6, load_bearing=False)


def S_up(beta, zeta):
    """S(beta, zeta) = int_zeta^inf exp(-sqrt(beta^2 + t^2)) dt (quad); for zeta < 0 through the full column 2 beta K1(beta)."""
    if zeta >= 0.0:
        return quad(lambda t: math.exp(-math.sqrt(beta * beta + t * t)), zeta, np.inf, epsabs=1e-15, epsrel=1e-12, limit=400)[0]
    full = 2.0 if beta == 0.0 else 2.0 * beta * float(k1e(beta)) * math.exp(-beta)
    return full - S_up(beta, -zeta)


def trig(th_deg):
    """sin, cos with the grid's exact zeros (90 and 180 deg)."""
    s_, c_ = math.sin(math.radians(th_deg)), math.cos(math.radians(th_deg))
    return (0.0 if abs(s_) < 1e-12 else s_), (0.0 if abs(c_) < 1e-12 else c_)


def strength_V2(Msun, x, th, foot):
    """V2's inward push per unit K = k^2 u_F: Sigma_0 [<S> - S(test)] cos(theta) (kg/m^2).  MUTATE C: M(<r)/r^2 instead."""
    r = x * r_M(Msun, foot)
    if MODE == "C":
        return float(M_enc_exp(r, Msun * MSUN)) / r ** 2
    sn, cs = trig(th)
    Sig0 = Msun * MSUN / (8 * math.pi * H_EXP ** 2)
    return Sig0 * (S_MEAN - S_up(r * sn / H_EXP, r * cs / H_EXP)) * cs


def gtot_exp(Msun, x, foot, kern):
    r = x * r_M(Msun, foot)
    return float(g_tot(gN_prof("exp", Msun, r), A0[foot], kern))


# ---- normalisation (C4) and the G1 grid, per footing and kernel (canonical P2 primary)
V2 = {}
for (foot, kern) in (("canonical", "P2"), ("alt", "P2"), ("canonical", "simple")):
    st = [strength_V2(1e11, 1.0, th, foot) for th in THETAS]
    i_star = int(np.argmax(st))
    th_star = THETAS[i_star]
    Kn = gtot_exp(1e11, 1.0, foot, kern) / st[i_star]              # K (normal) or G_LS (MUTATE C)
    grid = np.array([[[Kn * strength_V2(M, x, th, foot) for th in THETAS] for x in XG] for M in MASSES])   # (M, x, theta)
    tgt = np.array([[gtot_exp(M, x, foot, kern) for x in XG] for M in MASSES])
    rel = grid / tgt[:, :, None] - 1.0
    V2[(foot, kern)] = dict(K=Kn, th_star=th_star, grid=grid, tgt=tgt, frac=float(np.mean(np.abs(rel) <= 0.10)),
                            per_theta=[float(s_ / st[i_star]) for s_ in st])
V2P = V2[("canonical", "P2")]
K_V2 = V2P["K"] * (4 * math.pi if MODE == "C" else 1.0)            # K = k^2 u_F  (MUTATE C: k^2 u_F = 4 pi G_LS, flagged)
# x = 1 is not on the 25-point grid: C4 evaluates the grid's own function at x = 1, and an independent SI quadrature
def a_in_indep(Msun, x, th, foot, Kn):
    """the push at one point evaluated independently in SI units: quad over the physical column rho(sqrt(b^2 + z'^2)) (or, under
    MUTATE C, over the enclosed mass), instead of the dimensionless S(beta, zeta) used on the grid."""
    Mkg = Msun * MSUN
    r = x * r_M(Msun, foot)
    sn, cs = trig(th)
    if MODE == "C":
        return Kn * quad(lambda rr: 4 * math.pi * rr * rr * float(rho_exp(rr, Mkg)), 0.0, r, epsabs=0.0, epsrel=1e-12, limit=400)[0] / r ** 2
    b, z = r * sn, r * cs
    col_f = lambda zz: float(rho_exp(math.hypot(b, zz), Mkg))
    top = max(z, 0.0) + 80.0 * H_EXP                                 # finite range in metres (e^-80 tail dropped)
    col = quad(col_f, max(z, 0.0), top, epsabs=0.0, epsrel=1e-12, limit=400)[0]
    if z < 0:
        col += quad(col_f, z, 0.0, epsabs=0.0, epsrel=1e-12, limit=400)[0]
    return Kn * (S_MEAN * Mkg / (8 * math.pi * H_EXP ** 2) - col) * cs


g_norm = gtot_exp(1e11, 1.0, "canonical", "P2")
c4 = abs(V2P["K"] * strength_V2(1e11, 1.0, V2P["th_star"], "canonical") / g_norm - 1)
c4i = abs(a_in_indep(1e11, 1.0, V2P["th_star"], "canonical", V2P["K"]) / g_norm - 1)
check(f"C4 (control): S3's normalisation reproduces the target g_tot at M = 1e11, x = 1, theta* = {V2P['th_star']:.0f} deg to 1e-6",
      f"a_in/g_tot - 1 = {c4:.2e} (grid path), {c4i:.2e} (independent SI quadrature of the column);  K = k^2 u_F = {V2P['K']:.5e} "
      f"m^3 kg^-1 s^-2 ({V2P['K'] / G:.4f} G)" + ("  [MUTATE C: this is G_LS]" if MODE == "C" else ""), c4 <= 1e-6 and c4i <= 1e-6)
P(f"  theta* = {V2P['th_star']:.0f} deg (a_in per unit K at theta = {THETAS}: "
  + ", ".join(f"{v_:.3f}" for v_ in V2P["per_theta"]) + " of the maximum)")
for (foot, kern), d in V2.items():
    P(f"  G1 ({foot}, {kern}): fraction of the {d['grid'].size} grid points (4 M x 25 x x 5 theta) within 10% of the exp sphere's g_tot = {d['frac']:.3f}")
# mass scaling at theta*
jt = THETAS.index(V2P["th_star"])
ms_push = V2P["grid"][MASSES.index(1e12), :, jt] / V2P["grid"][MASSES.index(1e9), :, jt]
ms_tgt = V2P["tgt"][MASSES.index(1e12), :] / V2P["tgt"][MASSES.index(1e9), :]
for xx in (0.1, 1.0, 10.0, 30.0):
    j = int(np.argmin(np.abs(XG - xx)))
    P(f"    mass scaling at theta*, x = {XG[j]:.3g}: a_in(1e12)/a_in(1e9) = {ms_push[j]:.4g}   (target: point mass 1; exp sphere's own g_tot ratio {ms_tgt[j]:.4g})")
# the shadow geometry: upstream sees no shadow (Sigma_up(test) ~ 0), so its relative push is the galaxy's self-shadow deficit
if MODE != "C":
    r1 = r_M(1e11)
    S_up0 = S_up(0.0, r1 / H_EXP)
    P(f"  shadow geometry (M = 1e11, x = 1, r = {r1 / H_EXP:.2f} h): upstream on axis Sigma_up(test)/<Sigma_up> = {S_up0 / S_MEAN:.2e} (no shadow);"
      f" downstream on axis {S_up(0.0, -r1 / H_EXP) / S_MEAN:.3f}")
# S3a: the sign of the radial push over theta at fixed r (M = 1e11, x = 1), fine theta grid
THF = np.linspace(0.0, 180.0, 721)
ain_f = np.array([V2P["K"] * strength_V2(1e11, 1.0, th, "canonical") for th in THF])
g_n = gtot_exp(1e11, 1.0, "canonical", "P2")
up, dn = ain_f[THF < 90.0], ain_f[THF > 90.0]
neg = THF[(THF > 90.0) & (ain_f < 0)]
ok_s3a = bool(up.min() > 0.0 and dn.min() < 0.0)
check("S3a: at fixed r (M = 1e11, x = 1) the radial component of V2's relative push changes sign over theta "
      "(inward upstream, outward downstream outside the shadow)",
      f"a_in/g_tot: upstream (theta < 90) min {up.min() / g_n:+.4f}, max {up.max() / g_n:+.4f};  downstream min {dn.min() / g_n:+.4f}, "
      f"max {dn.max() / g_n:+.4f};  outward for theta in "
      + (f"[{neg.min():.2f}, {neg.max():.2f}] deg" if len(neg) else "(none)"), ok_s3a)
V2_ANISO = float((ain_f.max() - ain_f.min()) / abs(ain_f).max())

# ---- V2 energy (G3), opacity, optical depths (G5c), drag estimate (G6), Doppler estimate (G7)
SIG_SUN = MSUN / (math.pi * R_SUN ** 2)
SIG_EARTH = M_EARTH / (math.pi * R_EARTH ** 2)
V2_E = {}
for uk, u in UVALS:
    k = math.sqrt(K_V2 / u)
    Eo = {M: k * u * C * T_H / (0.5 * math.sqrt(G * M * MSUN * A0["canonical"])) for M in MASSES}
    V2_E[uk] = dict(k=k, E_over_Eorb=Eo, tau_sun=k * SIG_SUN, tau_earth=k * SIG_EARTH, drag=2 * k * u * V_EARTH / C,
                    power_per_kg=k * u * C)
    P(f"  V2 u_F = {uk:6s}: k = sqrt(K/u_F) = {k:.4e} m^2/kg; absorbed power ~ k u_F c = {k * u * C:.3e} W/kg; "
      f"E/E_orb over t_H = " + ", ".join(f"{Eo[M]:.2e} (1e{int(math.log10(M))})" for M in MASSES))
    P(f"      G5c optical depths: k Sigma_sun = {k * SIG_SUN:.3e}, k Sigma_earth = {k * SIG_EARTH:.3e}"
      f"  ({'saturated' if min(k * SIG_SUN, k * SIG_EARTH) >= 1 else 'thin'});  G6 drag estimate 2 k u_F v_E/c = {2 * k * u * V_EARTH / C:.3e} m/s^2")
DOPPLER_V2 = (1 + 600e3 / C) ** 2 - 1                              # the monopole's change for U = 600 km/s (G7 estimate)
P(f"  V2 G7 estimate: a galaxy moving at U = 600 km/s sees the beam Doppler-scaled, (1 + U/c)^2 - 1 = {DOPPLER_V2:.3e}")

# ---- V3: isotropic Le Sage bath, a_LS = G_LS M/r^2, fitted to a_ph at x = 1 (point mass)
P("")
V3 = {}
for kern in KERNS:
    gls = float(s_point(1.0, kern))                                # (G_LS/G)/x^2 = s(x) at x = 1
    err = np.abs(gls / XG ** 2 / s_point(XG, kern) - 1.0)
    V3[kern] = dict(GLS_over_G=gls, g1_max_err=float(err.max()), g1_err_x01=float(err[0]), g1_err_x30=float(err[-1]))
    P(f"  V3 ({kern}): G_LS/G = s(1) = {gls:.6f}; G1 max |a_LS/a_ph - 1| over x in [0.1, 30] = {err.max():.4g} "
      f"(x = 0.1: {err[0]:.4g}; x = 30: {err[-1]:.4g})")
G_LS = V3["P2"]["GLS_over_G"] * G
ms_v3 = [(G_LS * 1e12 * MSUN / (x * r_M(1e12)) ** 2) / (G_LS * 1e9 * MSUN / (x * r_M(1e9)) ** 2) for x in XG]
P(f"  V3 mass scaling a_LS(x; 1e12)/a_LS(x; 1e9) over the x grid: min {min(ms_v3):.12f}, max {max(ms_v3):.12f} "
  f"-- universal (a_LS = (G_LS/G) a0/x^2 at every mass)")
V3_E = {}
for uk, u in UVALS:
    k = math.sqrt(4 * math.pi * G_LS / u)
    Eo = {M: k * u * C * T_H / (0.5 * math.sqrt(G * M * MSUN * A0["canonical"])) for M in MASSES}
    drag = (4.0 / 3.0) * k * u * V_EARTH / C
    V3_E[uk] = dict(k=k, E_over_Eorb=Eo, tau_sun=k * SIG_SUN, tau_earth=k * SIG_EARTH, drag=drag, T_bath=(u / A_RAD) ** 0.25,
                    power_per_kg=k * u * C)
    P(f"  V3 u_R = {uk:6s}: k = sqrt(4 pi G_LS/u_R) = {k:.4e} m^2/kg; E/E_orb over t_H = "
      + ", ".join(f"{Eo[M]:.2e} (1e{int(math.log10(M))})" for M in MASSES))
    P(f"      G5c: k Sigma_sun = {k * SIG_SUN:.3e}, k Sigma_earth = {k * SIG_EARTH:.3e};  G6 drag (4/3) k u_R v_E/c = {drag:.3e} m/s^2 "
      f"-> {lab_g6(drag)};  bath temperature if EM (u_R/a_rad)^(1/4) = {(u / A_RAD) ** 0.25:.2f} K (reported only)")
P(f"  G6 scales at 1 AU: alpha2-type (alpha2/2)(w/c)^2 GM_sun/AU^2 = {SC_A2:.4e}; alpha1-type (alpha1/2)(w v_E/c^2) GM_sun/AU^2 = {SC_A1:.4e} m/s^2")
DOPPLER_V3 = (4.0 / 3.0) * (600e3 / C) ** 2
DIPOLE_V3 = 4 * 600e3 / C
P(f"  V3 G7/G8 estimates at U = 600 km/s: monopole change (4/3)(U/c)^2 = {DOPPLER_V3:.2e}; the bath's intensity dipole 4U/c = {DIPOLE_V3:.2e}")

# ---- G2 for V2 and V3 (both carry u proportional to (1+z)^4)
RHO_M0 = RHO_L * OM / OL
G2 = {uk: u / (RHO_M0 * C ** 2) * 1101.0 for uk, u in UVALS}
P(f"  G2: Omega_flow/Omega_m at z = 1100 = (u/(rho_m0 c^2)) 1101: rho_L c^2 -> {G2['rhoLc2']:.4g}; P_cap -> {G2['Pcap']:.4g}  (FAIL line 0.01)")
# V1' (frozen G2 rule): its energy density at z = 1100 scales as (1+z)^(3 eps); growth effect ~ eps Omega_L/Omega_m
G2_V1P_CMB = (RHO_L / RHO_M0) * 1101.0 ** (3 * EPS_V1P) / 1101.0 ** 3
G2_V1P_GROWTH = EPS_V1P * OL / OM
P(f"  G2 (V1', eps = {EPS_V1P}): rho_V1'/rho_m at z = 1100 = {G2_V1P_CMB:.3e}; growth estimate eps Omega_L/Omega_m = {G2_V1P_GROWTH:.4f} "
  f"(PASS line 0.05; eps <= {0.05 * OM / OL:.4f} would pass)")
R.num("S3", dict(S_mean=S_MEAN, V2=dict(K=V2P["K"], K_over_G=V2P["K"] / G, theta_star=V2P["th_star"],
                                        frac_within_10pct={f"{f}|{k}": d["frac"] for (f, k), d in V2.items()},
                                        mass_ratio_push=ms_push.tolist(), mass_ratio_target=ms_tgt.tolist(),
                                        S3a_ok=ok_s3a, up_min=float(up.min() / g_n), down_min=float(dn.min() / g_n),
                                        outward_theta=[float(neg.min()), float(neg.max())] if len(neg) else None,
                                        energy=V2_E, doppler=DOPPLER_V2),
                 V3=dict(fit=V3, mass_ratio=[min(ms_v3), max(ms_v3)], energy=V3_E, doppler=DOPPLER_V3, dipole=DIPOLE_V3),
                 G2=G2, G2_V1p_cmb=G2_V1P_CMB, G2_V1p_growth=G2_V1P_GROWTH, alpha2_scale=SC_A2, alpha1_scale=SC_A1))

# ================================================================================================================ S4
banner("S4 (H-D, reading T3: V4, the granted flux law -- a declared RESTATEMENT) -- what a stream does to the best flow law")
if MODE == "D":
    P("  [MUTATE D: F = s^2 everywhere (s = 1/x), no stiff core; the l = 1 ODE starts at f = x0, f' = 1]")

# ---- C1: F(s(x)) x^2 = 1
xs_, s2 = sp.symbols("x s", positive=True)
Fp2 = s2 ** 2 / (1 - 2 * s2)
Fsi = s2 ** 2 / (1 - s2)
sp2x = (sp.sqrt(1 + xs_ ** 2) - 1) / xs_ ** 2
ssix = (sp.sqrt(sp.Rational(1, 4) + xs_ ** 2) - sp.Rational(1, 2)) / xs_ ** 2
c1_p2 = sp.simplify(Fp2.subs(s2, sp2x) * xs_ ** 2 - 1)
c1_si = sp.simplify(Fsi.subs(s2, ssix) * xs_ ** 2 - 1)
XC1 = np.geomspace(0.1, 30.0, 401)
num_c1 = {k_: float(np.max(np.abs((s_point(XC1, k_) ** 2 / (1 - (2 if k_ == "P2" else 1) * s_point(XC1, k_))) * XC1 ** 2 - 1)))
          for k_ in KERNS}
_sn = (np.sqrt(1 + XC1 ** 2) - 1) / XC1 ** 2                         # the naive (cancelling) form, reported only
naive_c1 = float(np.max(np.abs(_sn ** 2 / (1 - 2 * _sn) * XC1 ** 2 - 1)))
check("C1 (control): F(s(x)) x^2 = 1 -- P2 F = s^2/(1-2s) with s = (sqrt(1+x^2)-1)/x^2 (sympy), and numerically for P2 and simple "
      "(F = s^2/(1-s)) to 1e-12 on x in [0.1, 30]",
      f"sympy: P2 residual {c1_p2}, simple residual {c1_si};  numeric max |F x^2 - 1|: P2 {num_c1['P2']:.1e}, simple {num_c1['simple']:.1e} "
      f"(s in the cancellation-free form 1/(sqrt(1+x^2)+1); the naive form gives {naive_c1:.1e})",
      c1_p2 == 0 and num_c1["P2"] <= 1e-12 and num_c1["simple"] <= 1e-12)


# ---- closed-form coefficient functions of x (algebraically identical to F_s(s(x)), F/s, F_ss; cancellation-free)
def coef(x, law):
    """(s, F, F_s, F_ss, F/s) as functions of x.  P2: w = sqrt(1+x^2), s = 1/(w+1); simple: v = sqrt(1/4+x^2), p = v+1/2, s = 1/p;
    deep (MUTATE D): F = s^2, s = 1/x.  F = 1/x^2 in every case (the static flux constraint)."""
    x = np.asarray(x, float)
    if law == "P2":
        w = np.sqrt(1.0 + x * x)
        return 1.0 / (w + 1), 1.0 / x ** 2, 2 * w * (w + 1) ** 2 / x ** 4, 2 * (w + 1) ** 6 / x ** 6, (w + 1) / x ** 2
    if law == "simple":
        v = np.sqrt(0.25 + x * x)
        p = v + 0.5
        return 1.0 / p, 1.0 / x ** 2, 2 * v * p ** 2 / x ** 4, 2 * p ** 6 / x ** 6, p / x ** 2
    return 1.0 / x, 1.0 / x ** 2, 2.0 / x, 2.0 + 0.0 * x, 1.0 / x


# reported: the closed forms equal sympy's derivatives of F at s(x)
_errc = 0.0
for law, Fl, sx in (("P2", Fp2, sp2x), ("simple", Fsi, ssix)):
    fs_ = sp.lambdify(s2, sp.diff(Fl, s2))
    fss_ = sp.lambdify(s2, sp.diff(Fl, s2, 2))
    for xv in (0.3, 1.0, 3.0, 10.0):
        sv = float(sx.subs(xs_, xv).evalf(30))
        cf = coef(xv, law)
        _errc = max(_errc, abs(cf[2] / fs_(sv) - 1), abs(cf[3] / fss_(sv) - 1), abs(cf[4] / (float(Fl.subs(s2, sv)) / sv) - 1))
check("aux: the closed-form F_s, F_ss, F/s (functions of x) equal sympy's derivatives of F at s(x)",
      f"max relative difference at x = 0.3, 1, 3, 10 (P2 and simple) = {_errc:.1e}", _errc < 1e-9, load_bearing=False)

# ---- C2: deep regime (F = s^2, s = 1/x): the l = 1 ODE (x^2 F_s f')' - 2 (F/s) f = 0 has exactly the solutions x and 1/x
fS = sp.Function("f")
Fgen = sp.Function("F")
ode_l1 = lambda Fexpr, sexpr, f_: sp.diff(xs_ ** 2 * sp.diff(Fexpr, s2).subs(s2, sexpr) * sp.diff(f_, xs_), xs_) \
    - 2 * (Fexpr / s2).subs(s2, sexpr) * f_
res_x = sp.simplify(ode_l1(s2 ** 2, 1 / xs_, xs_))
res_1x = sp.simplify(ode_l1(s2 ** 2, 1 / xs_, 1 / xs_))
gen = sp.dsolve(ode_l1(s2 ** 2, 1 / xs_, fS(xs_)), fS(xs_))
gen_rhs = sp.expand(gen.rhs)
terms = sorted(str(sp.simplify(t_ / t_.free_symbols.difference({xs_}).pop())) for t_ in gen_rhs.as_ordered_terms())
check("C2 (control): in the deep regime (F = s^2, s = 1/x) the l = 1 ODE has exactly the solutions x and 1/x (sympy)",
      f"residual(f = x) = {res_x}, residual(f = 1/x) = {res_1x}; dsolve: f = {gen.rhs}",
      res_x == 0 and res_1x == 0 and sorted(terms) == sorted(["x", "1/x"]))

# ---- C5 (+C5b): the second-order expansion of J = F(|S|) S/|S|, S = (s + d_r, d_th)
eps_, dr_, dt_ = sp.symbols("epsilon d_r d_theta", real=True)
F0, F1, F2 = sp.symbols("F F_s F_ss", real=True)
mag = sp.sqrt((s2 + eps_ * dr_) ** 2 + (eps_ * dt_) ** 2)
Dl = sp.series(mag - s2, eps_, 0, 3).removeO()
Fx = F0 + F1 * Dl + F2 * Dl ** 2 / 2                               # F(s + Delta) to second order (Delta = O(eps))
Jr = sp.series(Fx * (s2 + eps_ * dr_) / (s2 + Dl), eps_, 0, 3).removeO()
Jt = sp.series(Fx * (eps_ * dt_) / (s2 + Dl), eps_, 0, 3).removeO()
Qr_spec = F1 * dt_ ** 2 / (2 * s2) + F2 * dr_ ** 2 / 2 - F0 * dt_ ** 2 / (2 * s2 ** 2)
Qt_spec = (F1 / s2 - F0 / s2 ** 2) * dr_ * dt_
c5 = [sp.simplify(Jr.coeff(eps_, 0) - F0), sp.simplify(Jr.coeff(eps_, 1) - F1 * dr_), sp.simplify(Jr.coeff(eps_, 2) - Qr_spec),
      sp.simplify(Jt.coeff(eps_, 0)), sp.simplify(Jt.coeff(eps_, 1) - F0 / s2 * dt_), sp.simplify(Jt.coeff(eps_, 2) - Qt_spec)]
check("C5 (control): J = F(|S|) S/|S|, S = (s + d_r, d_th), to second order: J_r = F + F_s d_r + Q_r, J_th = (F/s) d_th + Q_th with "
      "Q_r = F_s d_th^2/(2s) + F_ss d_r^2/2 - F d_th^2/(2s^2), Q_th = (F_s/s - F/s^2) d_r d_th (sympy)",
      f"residuals (J_r at orders 0, 1, 2; J_th at 0, 1, 2) = {c5}", all(e == 0 for e in c5))
th_, lam_, fh_, fhp_, xx_ = sp.symbols("theta lambda fh fhp x", positive=True)
sub = {dr_: lam_ * fhp_ * sp.cos(th_), dt_: -lam_ * fh_ / xx_ * sp.sin(th_)}
Qr_t = Qr_spec.subs(sub)
Qt_t = Qt_spec.subs(sub)
avg = sp.simplify(sp.integrate(Qr_t * sp.sin(th_), (th_, 0, sp.pi)) / 2)
avg_spec = lam_ ** 2 * ((F1 / (3 * s2) - F0 / (3 * s2 ** 2)) * (fh_ / xx_) ** 2 + F2 * fhp_ ** 2 / 6)
P2c = (3 * sp.cos(th_) ** 2 - 1) / 2
l2c = sp.simplify(sp.Rational(5, 2) * sp.integrate(Qr_t * P2c * sp.sin(th_), (th_, 0, sp.pi)))
qr2_spec = lam_ ** 2 * sp.Rational(2, 3) * (-(F1 / (2 * s2) - F0 / (2 * s2 ** 2)) * (fh_ / xx_) ** 2 + F2 * fhp_ ** 2 / 2)
divQt = sp.simplify(sp.diff(sp.sin(th_) * Qt_t, th_) / sp.sin(th_) / xx_)
divQt_spec = -2 * lam_ ** 2 * (F1 / s2 - F0 / s2 ** 2) * fhp_ * (fh_ / xx_) / xx_ * P2c
c5b = [sp.simplify(avg - avg_spec), sp.simplify(l2c - qr2_spec), sp.simplify(divQt - divQt_spec)]
check("C5b (control): with d_r = lam fh' cos(th), d_th = -lam (fh/x) sin(th): <Q_r> = lam^2[(F_s/3s - F/3s^2)(fh/x)^2 + F_ss fh'^2/6] "
      "(so F_s <eps_r> = -<Q_r>: G7), the P2 projection of Q_r = lam^2 q_r2, and (1/(x sin))d_th(sin Q_th) = "
      "-2 lam^2 (F_s/s - F/s^2) fh' (fh/x)/x P2(cos) (the l = 2 source)",
      f"residuals = {c5b}", all(e == 0 for e in c5b))

# ---- C6: the deep l = 2 particular solution
gS = sp.Function("g")


def ode_l2(Fexpr, sexpr, fh_expr, g_):
    """the l = 2 equation (x^2 F_s g' + x^2 q_r2)' - 6 (F/s) g - 2x (F_s/s - F/s^2) fh' (fh/x) as a sympy expression."""
    Fs_ = sp.diff(Fexpr, s2)
    Fss_ = sp.diff(Fexpr, s2, 2)
    sub_ = lambda e: e.subs(s2, sexpr)
    fhp_x = sp.diff(fh_expr, xs_)
    qr2 = sp.Rational(2, 3) * (-(sub_(Fs_ / (2 * s2) - Fexpr / (2 * s2 ** 2))) * (fh_expr / xs_) ** 2 + sub_(Fss_) * fhp_x ** 2 / 2)
    Y = xs_ ** 2 * sub_(Fs_) * sp.diff(g_, xs_) + xs_ ** 2 * qr2
    return sp.diff(Y, xs_) - 6 * sub_(Fexpr / s2) * g_ - 2 * xs_ * sub_(Fs_ / s2 - Fexpr / s2 ** 2) * fhp_x * (fh_expr / xs_)


res6 = sp.simplify(ode_l2(s2 ** 2, 1 / xs_, xs_, sp.Rational(2, 3) * xs_ ** 2))
pp = sp.symbols("p")
hom = sp.simplify(ode_l2(s2 ** 2, 1 / xs_, 0 * xs_, xs_ ** pp) / xs_ ** (pp - 1))
roots6 = sp.solve(sp.Eq(hom, 0), pp)
check("C6 (control): deep regime (F = s^2, s = 1/x, fh = x): the l = 2 particular solution is g = (2/3) x^2 (sympy)",
      f"residual = {res6}; homogeneous exponents {roots6} (x^(+-sqrt 3), excluded by the BC at x_b)",
      res6 == 0 and set(roots6) == {sp.sqrt(3), -sp.sqrt(3)})

# ---- the first-order l = 1 stream solution: (x^2 F_s f')' - 2 (F/s) f = 0 in t = ln x, state (f, Pi = x^2 F_s f')
X0, X1 = 1e-3, 1e4
LAWS = ("deep",) if MODE == "D" else ("P2", "simple")


def solve_l1(law):
    m = 1 if law == "deep" else 3                                  # the regular core exponent (P2, simple: 0 and 3; take 3)
    _, _, Fs0, _, _ = coef(X0, law)
    y0 = [X0 ** m, X0 ** 2 * Fs0 * m * X0 ** (m - 1)]

    def rhs(t, y):
        x = math.exp(t)
        _, _, Fs, _, Fos = coef(x, law)
        return [y[1] / (x * Fs), x * 2 * Fos * y[0]]

    def jac(t, y):
        x = math.exp(t)
        _, _, Fs, _, Fos = coef(x, law)
        return np.array([[0.0, 1 / (x * Fs)], [2 * x * Fos, 0.0]])

    out = {}
    for meth in ("Radau", "DOP853"):                               # Radau (stiff-capable) is used; DOP853 is a cross-check
        sol = solve_ivp(rhs, (math.log(X0), math.log(X1)), y0, method=meth, rtol=1e-12, atol=1e-30, dense_output=True,
                        **({"jac": jac} if meth == "Radau" else {}))
        if sol.status != 0:
            raise RuntimeError(f"l = 1 ODE ({law}, {meth}) did not finish: {sol.message}")
        out[meth] = sol
    sol = out["Radau"]

    def AB(x):
        f, Pi = sol.sol(math.log(x))
        fp = Pi / (x * x * coef(x, law)[2])
        return (f + x * fp) / (2 * x), x * (f - x * fp) / 2

    A, B = AB(X1)
    A3, B3 = AB(1e3)
    c3 = float(sol.sol(math.log(X0))[0] / A / X0 ** m)              # core asymptotic fh = c3 x^m below x0

    def fh(x):
        x = np.atleast_1d(np.asarray(x, float))
        lo = x < X0
        xc = np.where(lo, X0, x)
        y = sol.sol(np.log(xc))
        h = y[0] / A
        hp = y[1] / (xc * xc * coef(xc, law)[2]) / A
        return np.where(lo, c3 * x ** m, h), np.where(lo, m * c3 * x ** (m - 1), hp)

    def fh_dop(x):
        y = out["DOP853"].sol(np.log(x))
        return y[1] / (x * x * coef(x, law)[2]) / A

    return dict(law=law, m=m, A=float(A), B=float(B), BA=float(B / A), A3=float(A3), BA3=float(B3 / A3), c3=c3, fh=fh,
                fhp_core=float(fh(X0)[1][0]), nfev=sol.nfev, dop_diff=float(np.max(np.abs(fh_dop(XF) / fh(XF)[1] - 1))))


L1 = {}
for law in LAWS:
    L1[law] = S = solve_l1(law)
    P(f"  l = 1 ({law}): A = {S['A']:.8f}, B/A = {S['BA']:.5g} at x1 = 1e4 (B/A = {S['BA3']:.5g} at 1e3; 2B/(A x1) = {2 * S['BA'] / X1:.5f} -- "
      f"see note); c3 = fh(x0)/x0^{S['m']} = {S['c3']:.8f}; fh'_core = fh'(x0) = {S['fhp_core']:.3e}; Radau nfev {S['nfev']}")
    P(f"      fh'(x) at x = 0.1, 1, 3, 10, 30: " + ", ".join(f"{float(S['fh'](xv)[1][0]):.6f}" for xv in (0.1, 1, 3, 10, 30))
      + f";  fh(x) - x at x = 30, 1e3: {float(S['fh'](30.0)[0][0]) - 30:.5f}, {float(S['fh'](1e3)[0][0]) - 1e3:.5f}")
    check(f"aux: l = 1 ({law}) Radau and DOP853 agree on fh' over x in [0.1, 30]", f"max relative difference {S['dop_diff']:.1e}",
          S["dop_diff"] < 1e-7, load_bearing=False)
if LAWS[0] != "deep":
    P("  note: B = x1(f - x1 f')/2 grows with x1 (B/A ~ -x1/2 for P2): at large x fh -> x + c0 with a constant c0 (2B/(A x1) -> c0),"
  " which the two-term form x + (B/A)/x cannot represent; B is reported as the frozen formula gives it and is not used by any gate.")

LAW0 = LAWS[0]                                                     # the primary law (P2; 'deep' under MUTATE D)
lam = lambda U, b=1.0: b * U / (KAPPA * C)                         # lambda = b U/(kappa c)
US = (150e3, 300e3, 370e3, 600e3)


def s4_fields(law, x):
    s, F, Fs, Fss, Fos = coef(x, law)
    h, hp = L1[law]["fh"](x)
    return s, F, Fs, Fss, Fos, h, hp


def D_l1(law, x, U, b=1.0):
    """the side-to-side rotation-velocity asymmetry lam (fh' - fh'_core)/(s + 1/x^2); and the frozen variant .../s."""
    s, F, Fs, Fss, Fos, h, hp = s4_fields(law, x)
    num = lam(U, b) * (hp - L1[law]["fhp_core"])
    return num / (s + 1 / x ** 2), num / s


def eps_r(law, x, U, b=1.0):
    """<eps_r> = -(lam^2/F_s)[(F_s/(3s) - F/(3s^2))(fh/x)^2 + F_ss fh'^2/6] (the sink flux through every sphere is fixed)."""
    s, F, Fs, Fss, Fos, h, hp = s4_fields(law, x)
    return -(lam(U, b) ** 2 / Fs) * ((Fs / (3 * s) - F / (3 * s * s)) * (h / x) ** 2 + Fss * hp ** 2 / 6)


# ---- the l = 2 BVP (solve_bvp in t = ln x), and a shooting cross-check
def q_r2(law, x):
    s, F, Fs, Fss, Fos, h, hp = s4_fields(law, x)
    return (2.0 / 3.0) * (-(Fs / (2 * s) - F / (2 * s * s)) * (h / x) ** 2 + 0.5 * Fss * hp ** 2)


def l2_rhs(law, x, g, Y, source=True):
    s, F, Fs, Fss, Fos, h, hp = s4_fields(law, x)
    q = q_r2(law, x) if source else 0.0 * x
    dg = x * (Y - x * x * q) / (x * x * Fs)
    dY = x * (6 * Fos * g + (2 * x * (Fs / s - F / (s * s)) * hp * (h / x) if source else 0.0))
    return dg, dY


def solve_l2(law, xb, xa=1e-2):
    def fun(t, y):
        dg, dY = l2_rhs(law, np.exp(t), y[0], y[1])
        return np.vstack([dg, dY])

    def bc(ya, yb):
        dg_a, _ = l2_rhs(law, np.array([xa]), np.array([ya[0]]), np.array([ya[1]]))
        return np.array([dg_a[0] - 3 * ya[0], yb[0] - (2.0 / 3.0) * xb ** 2])     # x g' = 3 g at x_a; g = (2/3) x_b^2

    t = np.linspace(math.log(xa), math.log(xb), 600)
    x = np.exp(t)
    g0 = (2.0 / 3.0) * x ** 2 * x / (1 + x)                          # guess: x^3 core, (2/3) x^2 outside
    _, _, Fs, _, _ = coef(x, law)
    Y0 = x * x * Fs * np.gradient(g0, x) + x * x * q_r2(law, x)
    sol = solve_bvp(fun, bc, t, np.vstack([g0, Y0]), tol=1e-8, max_nodes=300000)

    def gp(xv):
        xv = np.asarray(xv, float)
        g, Y = sol.sol(np.log(xv))
        return l2_rhs(law, xv, g, Y)[0] / xv                        # g' = (dg/dt)/x
    return sol, gp


def shoot_l2(law, xb, xa=1e-2):
    """g = g_part + c g_hom: g_part from g = g' = 0 at x_a (satisfies x g' = 3 g), g_hom from g = 1, g' = 3/x_a; c from g(x_b)."""
    res = {}
    for kind in ("part", "hom"):
        _, _, Fs_a, _, _ = coef(xa, law)
        y0 = [0.0, xa * xa * q_r2(law, np.array([xa]))[0]] if kind == "part" else [1.0, xa * xa * Fs_a * 3 / xa]
        def f_(t, y, k_=kind):
            dg, dY = l2_rhs(law, np.array([math.exp(t)]), y[0], y[1], source=(k_ == "part"))
            return [dg[0], dY[0]]
        # LSODA (automatic stiff/non-stiff switching) is ~20x cheaper here than DOP853 or Radau, whose step control reacts to the
        # piecewise dense output of the l = 1 solution that feeds the source terms
        res[kind] = solve_ivp(f_, (math.log(xa), math.log(xb)), y0, method="LSODA", rtol=1e-10, atol=1e-30, dense_output=True)
    cc_ = ((2.0 / 3.0) * xb ** 2 - res["part"].y[0, -1]) / res["hom"].y[0, -1]

    def gp(xv):
        xv = np.asarray(xv, float)
        yp, yh = res["part"].sol(np.log(xv)), res["hom"].sol(np.log(xv))
        return (l2_rhs(law, xv, yp[0], yp[1])[0] + cc_ * l2_rhs(law, xv, yh[0], yh[1], source=False)[0]) / xv
    return gp


S4 = {}
for law in LAWS:
    s_f, F_f, Fs_f, Fss_f, Fos_f, h_f, hp_f = s4_fields(law, XF)
    gl = s_f + 1 / XF ** 2                                          # g_law/a0
    rows = {}
    for U in US:
        D, Dfz = D_l1(law, XF, U)
        e0 = eps_r(law, XF, U)
        rows[U] = dict(Dmax=float(np.max(np.abs(D))), x_Dmax=float(XF[np.argmax(np.abs(D))]), Dfrozen_max=float(np.max(np.abs(Dfz))),
                       G7max=float(np.max(np.abs(e0) / gl)), x_G7max=float(XF[np.argmax(np.abs(e0) / gl)]))
    # G8a at U = 600 (l = 2 part at U = 600, RMS over isotropic disc orientations) + the l = 0 spread over U in [0, 600]
    bvp = {}
    for xb in (1e3, 1e4):
        sol, gp = solve_l2(law, xb)
        if sol.status != 0:
            P(f"  l = 2 BVP ({law}, x_b = {xb:.0e}) did NOT converge: {sol.message}")
        bvp[xb] = dict(status=int(sol.status), message=sol.message, nodes=len(sol.x), gp=gp(XF))
    shoot = shoot_l2(law, 1e4)(XF)
    gscale = float(np.max(np.abs(bvp[1e4]["gp"])))                  # g' crosses zero inside [0.1, 1]: differences are scaled
    shoot_diff = float(np.max(np.abs(shoot - bvp[1e4]["gp"]))) / gscale
    xb_sens = float(np.max(np.abs(bvp[1e3]["gp"] - bvp[1e4]["gp"]))) / gscale
    big = XF >= 1.0
    xb_sens_rel1 = float(np.max(np.abs(bvp[1e3]["gp"][big] / bvp[1e4]["gp"][big] - 1)))
    Ug = np.linspace(0.0, 600e3, 2001)
    l0 = np.array([np.std(np.log10(1 + eps_r(law, xv, Ug) / (s_ + 1 / xv ** 2))) for xv, s_ in zip(XF, s_f)])
    g8a = {}
    for xb in (1e3, 1e4):
        l2 = 0.5 / math.sqrt(5.0) * lam(600e3) ** 2 * np.abs(bvp[xb]["gp"]) / gl
        tot = np.sqrt(np.log10(1 + l2) ** 2 + l0 ** 2)
        g8a[xb] = dict(max=float(tot.max()), x_at=float(XF[np.argmax(tot)]), l2_dex_max=float(np.log10(1 + l2).max()),
                       l0_dex_max=float(l0.max()))
    l2_Uavg = 0.5 / math.sqrt(5.0) * lam(600e3) ** 2 / math.sqrt(5.0) * np.abs(bvp[1e4]["gp"]) / gl   # RMS of U^2 over [0, 600]
    g8a_Uavg = float(np.max(np.sqrt(np.log10(1 + l2_Uavg) ** 2 + l0 ** 2)))
    # deep-regime check of G7: <eps_r>/s -> -lam^2 x^2/3
    dchk = {xv: float(eps_r(law, np.array([xv]), 600e3)[0] / coef(xv, law)[0] / (-(lam(600e3) ** 2) * xv ** 2 / 3)) for xv in (1e3, 1e4)}
    S4[law] = dict(rows=rows, g8a=g8a, g8a_Uavg=g8a_Uavg, bvp={xb: dict(status=d["status"], nodes=d["nodes"]) for xb, d in bvp.items()},
                   shoot_diff=shoot_diff, xb_sens=xb_sens, xb_sens_rel1=xb_sens_rel1, deep_ratio=dchk)
    P(f"\n  V4 [{law}] per U (b = 1), maxima over x in [0.1, 30]:")
    P(f"    {'U km/s':>7s} {'lambda':>10s} {'G8b max D':>10s} {'at x':>6s} {'D (frozen /s)':>14s} {'G7 max':>10s} {'at x':>6s}")
    for U in US:
        r_ = rows[U]
        P(f"    {U / 1e3:7.0f} {lam(U):10.4e} {r_['Dmax']:10.4f} {r_['x_Dmax']:6.2f} {r_['Dfrozen_max']:14.4f} {r_['G7max']:10.3e} {r_['x_G7max']:6.2f}")
    for xb in (1e3, 1e4):
        P(f"    l = 2 BVP x_b = {xb:.0e}: status {bvp[xb]['status']} ({bvp[xb]['message']}), {bvp[xb]['nodes']} nodes;"
          f" G8a max = {g8a[xb]['max']:.3e} dex at x = {g8a[xb]['x_at']:.2f} (l=2 part max {g8a[xb]['l2_dex_max']:.2e}, l=0 spread max {g8a[xb]['l0_dex_max']:.2e})")
    P(f"    x_b sensitivity: max |g'(x_b=1e3) - g'(x_b=1e4)| / max|g'| over x in [0.1, 30] = {xb_sens:.2e} (relative, x in [1, 30]: "
      f"{xb_sens_rel1:.2e}); G8a max changes by {abs(g8a[1e3]['max'] - g8a[1e4]['max']):.1e} dex;  BVP vs shooting (x_b = 1e4): {shoot_diff:.2e}")
    P(f"    if the l = 2 part is also RMS'd over U uniform in [0, 600] (a reading, not scored): G8a max = {g8a_Uavg:.3e} dex")
    check(f"aux: l = 2 ({law}) solve_bvp agrees with a superposition shooting solution (x_b = 1e4) on g' over x in [0.1, 30]",
          f"max |difference| / max|g'| = {shoot_diff:.1e}", shoot_diff < 1e-4 and all(d["status"] == 0 for d in bvp.values()), load_bearing=False)
    check(f"aux: G7 deep-regime check ({law}): <eps_r>/s -> -lambda^2 x^2/3",
          f"ratio to -lambda^2 x^2/3 at x = 1e3: {dchk[1e3]:.6f}; at x = 1e4: {dchk[1e4]:.6f}", abs(dchk[1e4] - 1) < 1e-2, load_bearing=False)

S4P = S4[LAW0]
U600 = 600e3
D600 = S4P["rows"][U600]["Dmax"]
check("S4-D: the first-order l = 1 dipole is nonzero (max |D| at U = 600 km/s over x in [0.1, 30] > 1e-6)",
      f"max |D| = {D600:.4e} ({LAW0})" + ("  [MUTATE D: a uniform stream is an exact solution of F = s^2]" if MODE == "D" else ""),
      D600 > 1e-6)
G8B_LAB = lab_g8b(D600)
G7_MAX = S4P["rows"][U600]["G7max"]
G8A_MAX = S4P["g8a"][1e4]["max"]
P(f"\n  G8b ({LAW0}, U = 600): max D = {D600:.4f} at x = {S4P['rows'][U600]['x_Dmax']:.2f} -> {G8B_LAB}"
  f"  (frozen variant lambda(fh'-fh'_core)/s: {S4P['rows'][U600]['Dfrozen_max']:.4f} -> {lab_g8b(S4P['rows'][U600]['Dfrozen_max'])})")
P(f"  G7  ({LAW0}, U = 600): max |<eps_r>|/(s + 1/x^2) = {G7_MAX:.3e} -> {'PASS' if G7_MAX <= 0.10 else 'FAIL'} (line 0.10)")
P(f"  G8a ({LAW0}, x_b = 1e4): max over x in [0.1, 30] = {G8A_MAX:.3e} dex -> {'PASS' if G8A_MAX <= 0.048 else 'FAIL'} (line 0.048);"
  f" x_b = 1e3: {S4P['g8a'][1e3]['max']:.3e}")
if "simple" in S4:
    P(f"  simple kernel (reported): G8b max D = {S4['simple']['rows'][U600]['Dmax']:.4f}, G7 max = {S4['simple']['rows'][U600]['G7max']:.3e},"
      f" G8a max = {S4['simple']['g8a'][1e4]['max']:.3e} dex")

# ---- G3b: the sink's energy; G3a: the momentum it absorbs from the stream
SIG_E = {"rhoLc2": 4 * math.pi * C ** 2 * SQ_GRHO, "Pcap": 4 * math.pi * C ** 2 * SQ_GRHO * KAPPA ** 2 / (8 * math.pi)}   # b = 1
VF = {M: (G * M * MSUN * A0["canonical"]) ** 0.25 for M in MASSES}
BMIN = {uk: {M: SIG_E[uk] * T_H / (0.5 * VF[M] ** 2) for M in MASSES} for uk in SIG_E}
bmax_8b = 0.10 / D600 if D600 > 0 else float("inf")
bmax_7 = math.sqrt(0.10 / G7_MAX) if G7_MAX > 0 else float("inf")
P(f"\n  G3b: sigma_E = 4 pi c^2 sqrt(G rho_L)/b = {SIG_E['rhoLc2']:.4e} W/kg (n1 = rho_L c^2), {SIG_E['Pcap']:.4e} W/kg (P_cap), at b = 1")
WINDOW = {}
for uk in SIG_E:
    bm = BMIN[uk]
    WINDOW[uk] = dict(spec_empty=bool(max(bmax_8b, bmax_7) < min(bm.values())), strict_empty=bool(min(bmax_8b, bmax_7) < max(bm.values())))
    P(f"    n1 = {uk:6s}: E/E_orb over t_H at b = 1 (= b_min) = " + ", ".join(f"{bm[M]:.3e} (1e{int(math.log10(M))})" for M in MASSES))
    P(f"      window: b_max_8b = 0.10/max D = {bmax_8b:.4g}, b_max_7 = sqrt(0.10/G7) = {bmax_7:.4g};  min b_min = {min(bm.values()):.3e};"
      f" empty (max b_max < min b_min): {WINDOW[uk]['spec_empty']}  (and min b_max < max b_min: {WINDOW[uk]['strict_empty']})")
XR = np.geomspace(0.3, 30.0, 4001)
glaw_r = A0["canonical"] * (coef(XR, LAW0)[0] + 1 / XR ** 2)
G3A = {}
for uk in SIG_E:
    ar = SIG_E[uk] * U600 / C ** 2
    over = ar > 0.10 * glaw_r
    G3A[uk] = dict(a_react=ar, frac_exceeds=float(np.mean(over)), x_from=float(XR[over].min()) if over.any() else None,
                   b_min_3a=float(ar / (0.10 * glaw_r.min())))
    P(f"  G3a (n1 = {uk}): a_react = sigma_E U/c^2 (U = 600, b = 1) = {ar:.3e} m/s^2; exceeds 0.1 g_law over a fraction {np.mean(over):.3f}"
      f" of x in [0.3, 30] (log-uniform)" + (f", for x >= {XR[over].min():.3f}" if over.any() else "")
      + f"  (G3a alone would need b >= {ar / (0.10 * glaw_r.min()):.3g})")

# ---- G5a: the medium's sound speed from its Bernoulli relation, c_s^2/q^2 = -1/L, L = d ln(F/s)/d ln s
Lsym = {}
for law, Fl in (("P2", Fp2), ("simple", Fsi), ("deep", s2 ** 2)):
    Lsym[law] = sp.simplify(s2 * sp.diff(sp.log(Fl / s2), s2))
L_fun = sp.lambdify(s2, Lsym[LAW0])
cs2q2 = -1.0 / np.asarray(L_fun(coef(XF, LAW0)[0]), float) * np.ones_like(XF)
G5A_NEG = bool(np.any(cs2q2 < 0))
P(f"\n  G5a: L = d ln(F/s)/d ln s = {Lsym[LAW0]} ({LAW0}; P2 {Lsym['P2']}, simple {Lsym['simple']});"
  f" c_s^2/q^2 = -1/L over x in [0.1, 30]: min {cs2q2.min():.4f}, max {cs2q2.max():.4f} -> "
  f"{'imaginary sound speed everywhere' if np.all(cs2q2 < 0) else ('negative somewhere' if G5A_NEG else 'real')}")
G5B = {f: dict(earth=A0[f] / 2 / DAR_EARTH, mars=A0[f] / 2 / DAR_MARS) for f in FOOTS}
P(f"  G5b (inherited, CFG185{'; the main law -- not recomputed under MUTATE D' if MODE == 'D' else ''}): V4 reproduces P2, so the Sun carries a0/2 = {A0['canonical'] / 2:.3e} m/s^2: "
  f"{G5B['canonical']['mars']:.0f}-{G5B['alt']['earth']:.0f}x the planetary delta A_R bound (canonical Earth {G5B['canonical']['earth']:.0f}x, "
  f"Mars {G5B['canonical']['mars']:.0f}x; alt Earth {G5B['alt']['earth']:.0f}x, Mars {G5B['alt']['mars']:.0f}x)")

# ---- G6: the preferred-frame acceleration at 1 AU from the l = 1 solution in the Sun's field
G6 = {}
for foot in FOOTS:
    xs_sun = AU / math.sqrt(GM_SUN / A0[foot])
    lw = W_SUN / (KAPPA * C)
    S_ = L1[LAW0]
    hp_sun = float(S_["fh"](xs_sun)[1][0])                          # core asymptotic below x0: m c3 x^(m-1)
    hp_zero = S_["m"] * S_["c3"] * 0.0 ** (S_["m"] - 1) if S_["m"] > 1 else S_["c3"]   # the core value fh'(0)
    d_phys = lw * A0[foot] * abs(hp_sun - hp_zero)
    d_lit = lw * A0[foot] * abs(hp_sun - S_["fhp_core"])
    G6[foot] = dict(x_sun=xs_sun, fhp_sun=hp_sun, delta_a=d_phys, delta_a_literal=d_lit, label=lab_g6(d_phys), label_literal=lab_g6(d_lit))
    P(f"  G6 ({foot}): x_sun(1 AU) = {xs_sun:.4e} (< x0: core asymptotic fh = c3 x^{S_['m']}); lambda_w = w/(kappa c) = {lw:.4e};"
      f" delta_a = lambda_w a0 |fh'(x_sun) - fh'(0)| = {d_phys:.3e} m/s^2 -> {lab_g6(d_phys)}"
      f"  [with fh'_core = fh'(x0): {d_lit:.3e} -> {lab_g6(d_lit)}]")
R.num("S4", dict(law=LAW0, l1={k_: {kk: v_ for kk, v_ in d.items() if kk != "fh"} for k_, d in L1.items()},
                 per_law={k_: dict(rows={f"{U / 1e3:.0f}": r_ for U, r_ in d["rows"].items()},
                                   g8a={f"{xb:.0e}": v_ for xb, v_ in d["g8a"].items()}, g8a_Uavg=d["g8a_Uavg"],
                                   bvp={f"{xb:.0e}": v_ for xb, v_ in d["bvp"].items()}, shoot_diff=d["shoot_diff"],
                                   xb_sens=d["xb_sens"], xb_sens_rel1=d["xb_sens_rel1"], deep_ratio={f"{xv:.0e}": v_ for xv, v_ in d["deep_ratio"].items()})
                          for k_, d in S4.items()},
                 G8b=dict(Dmax=D600, label=G8B_LAB), G7max=G7_MAX, G8a_max=G8A_MAX, sigma_E=SIG_E, b_min=BMIN,
                 b_max_8b=bmax_8b, b_max_7=bmax_7, window=WINDOW, G3a=G3A, G5a=dict(L=str(Lsym[LAW0]), cs2q2_min=float(cs2q2.min()),
                                                                                     cs2q2_max=float(cs2q2.max())),
                 G5b=G5B, G6=G6))

# ================================================================================================================ gate matrix
banner("GATE MATRIX -- variant x G1..G8 (primary: canonical footing, P2, u = rho_L c^2; reasons carry the alternatives)")
ROWS = ("V1", "V1'(T1)", "V2(T1)", "V2(T2)", "V3(T1)", "V3(T2)", "V4(T3)")
M_ = {r_: {} for r_ in ROWS}


def put(row, gate, lab, why):
    M_[row][gate] = (lab, why)


# V1
if S1_NOFLOW:
    put("V1", "G1", "FAIL", "no flow exists: T = -rho c^2 eta is boost-invariant, T^0i = 0 for every v, (eps + p) = 0 (S1a-c)")
    for g_, why in (("G2", "no flow (G1 structural); V1 is Lambda itself"), ("G3", "no flow: no reaction, no energy flux (T^0i = 0)"),
                    ("G4", "no mechanism whose constants could be counted"), ("G5", "no flow")):
        put("V1", g_, "NOT REACHED", why)
    for g_, why in (("G6", "no rest frame: nothing to prefer"), ("G7", "no frame for a0 to depend on"), ("G8", "no flow direction")):
        put("V1", g_, "UNDEFINED", why)
else:
    put("V1", "G1", "UNDECIDED", f"S1 finds a flow at w = {W_S1} (T^01 = {T01}): V1 is then V1'-like, scored in the V1' row")
    for g_ in ("G2", "G3", "G4", "G5", "G6", "G7", "G8"):
        put("V1", g_, "NOT REACHED", f"w = {W_S1}: not V1")

# T1 rows: the gravity of the flow's own energy
T1 = {"V1'(T1)": ("V1p", "-"), "V2(T1)": ("V2", "rhoLc2"), "V3(T1)": ("V3", "rhoLc2")}
for row, (mech, uk) in T1.items():
    keys = [k for k in S2_SUM if k.startswith(mech + "|") and (mech == "V1p" or f"|{uk}|" in k)]
    maxR = max(S2_SUM[k]["maxR"] for k in keys)
    g1e = max(S2_SUM[k]["g1_max_err"] for k in keys if "|P2|canonical|" in k)
    mgt = max(S2_SUM[k]["max_gach_over_gtot"] for k in keys)
    lab1 = "PASS" if g1e <= 0.10 else "FAIL"
    alt = "" if mech == "V1p" else f"; P_cap max R {max(S2_SUM[k]['maxR'] for k in S2_SUM if k.startswith(mech + '|') and '|Pcap|' in k):.1e}"
    put(row, "G1", lab1, f"max R = g_ach/a_ph = {maxR:.1e} (all kernels, footings, profiles{alt}); max |g_N + g_ach - g_tot|/g_tot = {g1e:.3f}")
    if mech == "V1p":
        lab2 = "FAIL" if G2_V1P_CMB > 0.01 else ("PASS" if G2_V1P_GROWTH <= 0.05 else "UNDECIDED")
        put(row, "G2", lab2, f"CMB: rho/rho_m(1100) = {G2_V1P_CMB:.1e} (< 0.01); growth eps Omega_L/Omega_m = {G2_V1P_GROWTH:.3f} > 0.05, no Boltzmann code")
        put(row, "G4", "FAIL", f"eps = {EPS_V1P} and c_s^2 = 1e-4 c^2 are new constants (not Lambda-tied)")
    else:
        put(row, "G2", "FAIL" if G2["rhoLc2"] > 0.01 else "PASS",
            f"Omega_flow/Omega_m(1100) = {G2['rhoLc2']:.0f} (rho_L c^2), {G2['Pcap']:.1f} (P_cap) > 0.01")
        put(row, "G4", "PASS", "only u (Lambda-tied: rho_L c^2 or P_cap), G and c; no opacity k in the T1 reading")
    put(row, "G3", "NOT REACHED", f"G1 fails structurally (max R = {maxR:.0e}); a static compression/focusing absorbs no power")
    put(row, "G5", "NOT REACHED", f"G1 fails structurally (max R = {maxR:.0e})")
    gsun = g_ach(mech, "point", MSUN / MSUN, AU, U_L if mech != "V1p" else None)
    put(row, "G6", lab_g6(gsun), f"trivial bound: the Sun's whole T1 extra gravity at 1 AU = {gsun:.1e} m/s^2 vs alpha2 scale {SC_A2:.1e}")
    put(row, "G7", "PASS" if mgt <= 0.10 else "FAIL", f"trivial bound: the whole T1 force <= {mgt:.1e} g_tot over the grid (line 0.10)")
    ok8 = math.log10(1 + mgt) <= 0.048 and mgt <= 0.02
    put(row, "G8", "PASS" if ok8 else "FAIL", f"trivial bound: any anisotropy <= the whole T1 force, {mgt:.1e} g_tot ({math.log10(1 + mgt):.1e} dex)")

# V2(T2): directional push
f10 = V2P["frac"]
j1 = int(np.argmin(np.abs(XG - 1.0)))
put("V2(T2)", "G1", "PASS" if f10 == 1.0 else "FAIL", f"{f10:.3f} of the 500 grid points within 10% (alt {V2[('alt', 'P2')]['frac']:.3f}, simple {V2[('canonical', 'simple')]['frac']:.3f}); "
    f"mass scaling a_in(1e12)/a_in(1e9) at theta* = {ms_push[j1]:.0f} at x ~ 1 (target 1; exp sphere {ms_tgt[j1]:.1f}); "
    f"{'sign change' if ok_s3a else 'no sign change'} (S3a)")
put("V2(T2)", "G2", "FAIL" if G2["rhoLc2"] > 0.01 else "PASS", f"Omega_flow/Omega_m(1100) = {G2['rhoLc2']:.0f} (rho_L c^2), {G2['Pcap']:.1f} (P_cap)")
eo2 = V2_E["rhoLc2"]["E_over_Eorb"]
eo2p = V2_E["Pcap"]["E_over_Eorb"]
put("V2(T2)", "G3", "FAIL" if max(eo2.values()) > 1 else "PASS",
    f"absorbed energy over t_H / orbital energy = {min(eo2.values()):.1e}-{max(eo2.values()):.1e} (rho_L c^2), {min(eo2p.values()):.1e}-{max(eo2p.values()):.1e} (P_cap)")
put("V2(T2)", "G4", "FAIL", f"the opacity k = {V2_E['rhoLc2']['k']:.3g} m^2/kg (rho_L c^2), {V2_E['Pcap']['k']:.3g} (P_cap) is a new constant")
put("V2(T2)", "G5", "FAIL" if min(V2_E["rhoLc2"]["tau_sun"], V2_E["rhoLc2"]["tau_earth"]) >= 1 else "PASS", f"G5c: k Sigma_sun = {V2_E['rhoLc2']['tau_sun']:.1e}, k Sigma_earth = {V2_E['rhoLc2']['tau_earth']:.1e} "
    f"(P_cap {V2_E['Pcap']['tau_earth']:.1e}): saturated, push not proportional to mass (EP broken)")
d2 = V2_E["rhoLc2"]["drag"]
put("V2(T2)", "G6", lab_g6(d2), f"ESTIMATE (not in the frozen S3): Doppler drag 2 k u_F v_E/c = {d2:.1e} m/s^2 (P_cap {V2_E['Pcap']['drag']:.1e} -> "
    f"{lab_g6(V2_E['Pcap']['drag'])}); scales alpha2 {SC_A2:.1e}, alpha1 {SC_A1:.1e}; thin-absorber k (the Earth is saturated)")
put("V2(T2)", "G7", "PASS" if DOPPLER_V2 <= 0.10 else "FAIL", f"ESTIMATE: the beam's Doppler factor changes the monopole by (1 + U/c)^2 - 1 = {DOPPLER_V2:.1e} at 600 km/s")
put("V2(T2)", "G8", "FAIL" if ok_s3a else lab_g8b(V2_ANISO),
    f"the radial push changes sign over theta at fixed r (S3a: outward for theta in {neg.min():.0f}-{neg.max():.0f} deg); O(1) anisotropy "
    f"(range/max = {V2_ANISO:.2f})" if ok_s3a else f"S3a finds no sign change (a_in > 0 everywhere; range/max = {V2_ANISO:.2f})")

# V3(T2): isotropic Le Sage bath
put("V3(T2)", "G1", "PASS" if V3["P2"]["g1_max_err"] <= 0.10 else "FAIL", f"shape: max |a_LS/a_ph - 1| = {V3['P2']['g1_max_err']:.1f} over x in [0.1, 30] (x = 30: {V3['P2']['g1_err_x30']:.3f}); "
    f"G_LS/G = {V3['P2']['GLS_over_G']:.4f}; mass scaling universal (ratio {min(ms_v3):.6f})")
put("V3(T2)", "G2", "FAIL" if G2["rhoLc2"] > 0.01 else "PASS", f"Omega_flow/Omega_m(1100) = {G2['rhoLc2']:.0f} (rho_L c^2), {G2['Pcap']:.1f} (P_cap)")
eo3 = V3_E["rhoLc2"]["E_over_Eorb"]
eo3p = V3_E["Pcap"]["E_over_Eorb"]
put("V3(T2)", "G3", "FAIL" if max(eo3.values()) > 1 else "PASS",
    f"absorbed energy over t_H / orbital energy = {min(eo3.values()):.1e}-{max(eo3.values()):.1e} (rho_L c^2), {min(eo3p.values()):.1e}-{max(eo3p.values()):.1e} (P_cap)")
put("V3(T2)", "G4", "FAIL", f"the opacity k = {V3_E['rhoLc2']['k']:.3g} m^2/kg (rho_L c^2), {V3_E['Pcap']['k']:.3g} (P_cap) is a new constant")
put("V3(T2)", "G5", "FAIL" if min(V3_E["rhoLc2"]["tau_sun"], V3_E["rhoLc2"]["tau_earth"]) >= 1 else "PASS", f"G5c: k Sigma_sun = {V3_E['rhoLc2']['tau_sun']:.1e}, k Sigma_earth = {V3_E['rhoLc2']['tau_earth']:.1e} "
    f"(P_cap {V3_E['Pcap']['tau_earth']:.1e}): saturated (EP broken)")
d3 = V3_E["rhoLc2"]["drag"]
put("V3(T2)", "G6", lab_g6(d3), f"drag (4/3) k u_R v_E/c = {d3:.1e} m/s^2 (P_cap {V3_E['Pcap']['drag']:.1e} -> {lab_g6(V3_E['Pcap']['drag'])}); "
    f"scales alpha2 {SC_A2:.1e}, alpha1 {SC_A1:.1e}; thin-absorber k (the Earth is saturated)")
put("V3(T2)", "G7", "PASS" if DOPPLER_V3 <= 0.10 else "FAIL", f"ESTIMATE: an isotropic bath seen at U = 600 km/s changes the monopole by (4/3)(U/c)^2 = {DOPPLER_V3:.1e}")
put("V3(T2)", "G8", lab_g8b(DIPOLE_V3), f"ESTIMATE: the bath's dipole 4U/c = {DIPOLE_V3:.1e} bounds the l = 1 asymmetry (b: <= 0.02); l = 2 and l = 0 are O((U/c)^2)")

# V4(T3): the granted flux law
put("V4(T3)", "G1", "FAIL", f"by rule: a restatement (n(q) reverse-engineered from P2); G1-with-stream at U = 600: max D = {D600:.3f} "
    f"({'>' if D600 > 0.10 else '<='} 0.10) at x = {S4P['rows'][U600]['x_Dmax']:.1f}")
put("V4(T3)", "G2", "UNDEFINED", "no cosmological perturbation equations for the flux law (background-only)")
g3fail = G3A["rhoLc2"]["frac_exceeds"] > 0 or min(BMIN["rhoLc2"].values()) > 1
put("V4(T3)", "G3", "FAIL" if g3fail else "PASS",
    f"G3a: sigma_E U/c^2 > 0.1 g_law over {G3A['rhoLc2']['frac_exceeds']:.2f} of x in [0.3, 30] (P_cap {G3A['Pcap']['frac_exceeds']:.2f}); "
    f"G3b: E/E_orb = {min(BMIN['rhoLc2'].values()):.1e}-{max(BMIN['rhoLc2'].values()):.1e} at b = 1 (P_cap {min(BMIN['Pcap'].values()):.1e}-"
    f"{max(BMIN['Pcap'].values()):.1e}); b-window empty: {WINDOW['rhoLc2']['spec_empty']} (P_cap {WINDOW['Pcap']['spec_empty']})")
put("V4(T3)", "G4", "FAIL", f"n(q) ~ s^2/(1-2s) is a reverse-engineered function; b = 1 fails G3b and any b != 1 is a new constant (b-window "
    f"empty: {WINDOW['rhoLc2']['spec_empty']} by max b_max < min b_min, {WINDOW['rhoLc2']['strict_empty']} by min b_max < max b_min)")
put("V4(T3)", "G5", "FAIL" if G5A_NEG else "PASS",
    f"G5a: c_s^2/q^2 = -1/L = {cs2q2.min():.3f}..{cs2q2.max():.3f} < 0 (imaginary sound speed); G5b inherited (CFG185): the Sun carries a0/2, "
    f"{G5B['canonical']['mars']:.0f}-{G5B['alt']['earth']:.0f}x the planetary bound")
put("V4(T3)", "G6", G6["canonical"]["label"], f"delta_a(1 AU) = lambda_w a0 |fh'(x_sun) - fh'(0)| = {G6['canonical']['delta_a']:.1e} m/s^2 "
    f"(alt {G6['alt']['delta_a']:.1e}; with fh'_core = fh'(x0): {G6['canonical']['delta_a_literal']:.1e} -> {G6['canonical']['label_literal']}) "
    f"vs alpha2 scale {SC_A2:.1e}")
put("V4(T3)", "G7", "PASS" if G7_MAX <= 0.10 else "FAIL", f"max |<eps_r>|/(s + 1/x^2) at U = 600 = {G7_MAX:.2e} (line 0.10)")
g8a_lab = "PASS" if G8A_MAX <= 0.048 else "FAIL"
g8_lab = "FAIL" if "FAIL" in (g8a_lab, G8B_LAB) else ("UNDECIDED" if "UNDECIDED" in (g8a_lab, G8B_LAB) else "PASS")
put("V4(T3)", "G8", g8_lab, f"G8a {g8a_lab}: {G8A_MAX:.1e} dex (line 0.048); G8b {G8B_LAB}: max D = {D600:.3f} at U = 600 "
    f"(PASS <= 0.02, FAIL > 0.10; frozen /s variant {S4P['rows'][U600]['Dfrozen_max']:.3f})")

GATES = ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8")
short = {"PASS": "PASS", "FAIL": "FAIL", "UNDECIDED": "UNDEC", "UNDEFINED": "UNDEF", "NOT REACHED": "N/R"}
P(f"  {'':9s}" + "".join(f"{g_:>7s}" for g_ in GATES))
for row in ROWS:
    P(f"  {row:9s}" + "".join(f"{short[M_[row][g_][0]]:>7s}" for g_ in GATES))
P("  (UNDEC = UNDECIDED, UNDEF = UNDEFINED, N/R = NOT REACHED)")
for row in ROWS:
    P(f"\n  {row}")
    for g_ in GATES:
        lab_, why_ = M_[row][g_]
        P(f"    {g_} {lab_:11s} {why_}")
R.num("matrix", {row: {g_: dict(verdict=M_[row][g_][0], reason=M_[row][g_][1]) for g_ in GATES} for row in ROWS})

P("\n  Reading: a scoped statement for V1-V4 under T1-T3 as frozen. kappa = 1/2 and Omega_c h^2 stay FITTED; nothing here touches"
  " candidate B, says the theory is closed, or says the data favour any model.")
P(f"  run time {time.time() - T0:.1f} s")
nf = R.write(LANE)
sys.exit(1 if nf else 0)
