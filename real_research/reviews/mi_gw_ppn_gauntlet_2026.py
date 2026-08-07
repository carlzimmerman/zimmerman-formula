#!/usr/bin/env python3
r"""
LANE F -- THE CONSISTENCY GAUNTLET for the de Sitter-Unruh MODIFIED-INERTIA framework
=====================================================================================
Five field-theory constraints that have killed most modified-gravity theories of the last decade,
run against the framework's OWN realizations, on BOTH a_0 footings, with the margin reported for
each and the failures stated bluntly.

  1. GW170817 / GRB170817A tensor speed  |c_T/c - 1| < ~5e-16
  2. PPN gamma (Cassini) and beta (LLR Nordtvedt)
  3. The Cassini Q2 quadrupole -- does PURE MI inherit the MG realization's wall?
  4. Gdot/G from a rolling / gated condensate vs LLR, and the committed omega_c window
  5. Pass/fail table with margins

FRAMEWORK (judged on its own terms, never through the standard-MOND or McGaugh lens):
  a_0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 (FITTED, NOT DERIVED)
        -> 9.3614e-11 m/s^2 canonical (rho_DE, cH_Lambda/Z);  ALT 1.130e-10 (rho_total, cH0)
  exact law   g_obs^2 = g_bar^2 + a_0 g_bar      (Milgrom's balance with floor k = a_0/2)
  kernel      nu(y) = sqrt(1 + 1/y),  y = g_bar/a_0;  mu_fw(x) = (sqrt(1+4x^2)-1)/(2x)
  c H_Lambda = 5.4194e-10 m/s^2 ;  Z = 2 sqrt(8 pi/3) = 5.7888100366

MANDATORY CREDIT.  nu = sqrt(1+1/y) and the dS-Unruh balance are MILGROM 1999 PLA 253:273 eqs 6-9
(he fixes a_0_hat = 2 c H_Lambda; his eqs 10-11 give a second coefficient); MILGROM 2008
arXiv:0801.3133 sec 7.3.1 notes the coefficient mismatch "isn't necessarily meaningful".  The
temperature sqrt(a^2 + Lambda/3)/2pi is NARNHOFER, PETER & THIRRING 1996 IJMPB 10:1507; the
five-acceleration reading DESER & LEVIN 1997 CQG 14:L163; a_lambda = c^2 sqrt(Lambda/3) MILGROM 1994
Ann.Phys. 229:384; the exponential kernel MCGAUGH 2008 ApJ 683:137 eq 11a; AQUAL BEKENSTEIN &
MILGROM 1984; TeVeS BEKENSTEIN 2004; AeST SKORDIS & ZLOSNIK 2021.  The framework's distinctive
content is the cH_Lambda/Z COEFFICIENT plus the modified-inertia completion -- not the kernel.

EXTERNAL ANCHORS used (each cited where used):
  GW170817/GRB170817A  |c_T/c - 1| < ~5e-16          Abbott+ 2017 ApJL 848:L13 (dt <= +1.74 s, 40 Mpc)
  Cassini Shapiro      gamma - 1 = (2.1 +/- 2.3)e-5  Bertotti, Iess & Tortora 2003 Nature 425:374
  LLR Nordtvedt        eta_N = (-0.2 +/- 1.1)e-4     Hofmann & Mueller 2018 CQG 35:035015
  LLR Gdot/G           (-5.0 +/- 9.6)e-15 /yr        Biskupek, Mueller & Torre 2021 Universe 7:34
  Cassini Q2           (1.6 +/- 1.8)e-27 s^-2        Park+ 2026 arXiv:2602.17884
  Cassini Q2 (2024)    (3 +/- 3)e-27 s^-2, RAR IF ruled out at 8.7 sigma
                                                     Desmond, Hees & Famaey 2024 MNRAS 530:1781
  MOND SS quadrupole formula (eq 12 of Desmond+24)   Milgrom 2009 MNRAS 399:474
  const-radial delta A_R  Earth 3.66e-14, Mars 3.72e-14 m/s^2 (2 sigma)
                                                     Sereno & Jetzer 2006 astro-ph/0606197 Tab.1+Eq.9
                                                     (Pitjeva EPM2004), as inverted in the corpus
  Horndeski tensor sector  G_T, F_T                  Kobayashi, Yamaguchi & Yokoyama 2011 PTP 126:511
  Einstein-aether tensor speed c_T^2 = 1/(1-c1-c3)   Jacobson & Mattingly 2004 PRD 70:024003

CORPUS ANCHORS reproduced independently here (not read-and-agreed):
  prep_2026/gw170817_check/RESULT.md          B_max ~ 4.5e-6, Delta_t ~ 3.5e7 s  -> EXCLUDED
  prep_2026/mi_field_theory/UNIFICATION.md    c_T = 1 exact; |Delta gamma| ~ 7.2e-7 / 8.7e-7 at Saturn
  reviews/cassini_mi_evasion_2026/            MI l=1 1.5e-28, l=2 7.4e-34 s^-2 -> EVADES
  prep_2026/mi_planetary_falsification/       omega_c window, drift d ln r/dt = a_0 omega_c/g_N
  STANDING.md sec 5 item 0                    ephemeris liability 1279x canon / 1544x alt (post-EFE
                                              = bare; the EFE relief is WITHDRAWN)

CALIBRATION.  Manufacture neither a win nor a deficit.  Every dimensional number on both footings.
Every claim of a FAILURE is checked as hard as every claim of a PASS -- and section 2 below
WITHDRAWS one corpus liability that turns out to be a c^2 units slip.  No "theory closed" language.

Run:  python3 real_research/reviews/mi_gw_ppn_gauntlet_2026.py     (exit 0 iff every check holds)
"""
import sys
import numpy as np
import sympy as sp
from scipy import integrate
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

np.seterr(all="ignore")

# ---------------------------------------------------------------------------------- check harness
_N = 0
_OK = 0
_FAILED = []


def chk(name, cond, extra=""):
    global _N, _OK
    _N += 1
    ok = bool(cond)
    if ok:
        _OK += 1
    else:
        _FAILED.append(name)
    print(f"  [{'OK' if ok else 'FAIL'}] {name}" + (f"   {extra}" if extra else ""))
    return ok


RULE = "=" * 104


def head(s):
    print("\n" + RULE + "\n" + s + "\n" + RULE)


# ------------------------------------------------------------------------------ constants/footings
c = 2.99792458e8
G = 6.674e-11
GM_SUN = 1.32712440018e20
GM_EARTH = 3.986004418e14
M_SUN = 1.989e30
AU = 1.495978707e11
R_SUN = 6.957e8
R_MOON = 3.844e8
KPC = 3.0857e19
MPC = 1000.0 * KPC
YR = 3.15576e7

A0 = {"canon": 9.3614e-11, "alt": 1.1300e-10}
CH_LAMBDA = 5.4194e-10
Z_CONST = 2.0 * np.sqrt(8.0 * np.pi / 3.0)

# planets: semi-major axis, eccentricity, period [yr]
PLANETS = {
    "Mercury": (0.387098 * AU, 0.20563, 0.240846),
    "Venus":   (0.723332 * AU, 0.006772, 0.615198),
    "Earth":   (1.000000 * AU, 0.016710, 1.000017),
    "Mars":    (1.523680 * AU, 0.093400, 1.880848),
    "Jupiter": (5.204400 * AU, 0.048900, 11.86200),
    "Saturn":  (9.582600 * AU, 0.056500, 29.45700),
}
R_SAT = PLANETS["Saturn"][0]

# Galactic external field at the Sun (the TRUE/observed centripetal acceleration)
V_LSR, R_GC = 233.0e3, 8.2 * KPC
A_EXT = V_LSR ** 2 / R_GC

# external bounds
CT_BOUND = 5.0e-16                       # Abbott+ 2017
GAM_C, GAM_S = 2.1e-5, 2.3e-5            # Bertotti+ 2003
GAM_CEIL = abs(GAM_C) + 2 * GAM_S        # 2 sigma ceiling on |gamma-1|
ETA_N_C, ETA_N_S = -0.2e-4, 1.1e-4       # Hofmann & Mueller 2018
Q2_C, Q2_S = 1.6e-27, 1.8e-27            # Park+ 2026
Q2_CEIL = Q2_C + 2 * Q2_S                # 5.2e-27 s^-2
Q2_2024_C, Q2_2024_S = 3.0e-27, 3.0e-27  # Desmond+24 anchor
LLR_C, LLR_S = -5.0e-15, 9.6e-15         # Biskupek+ 2021, /yr
DAR_EARTH, DAR_MARS = 3.66e-14, 3.72e-14 # Sereno & Jetzer 2006 inverted, 2 sigma, m/s^2

# committed omega_c window (task-stated, in force)
WC_LO = 1.7824e-14
WC_HI = {"canon": 2.2113e-14, "alt": 1.8306e-14}
OMEGA_GAL_BIND = 5.94e-15                # UGC05721 innermost deep-MOND orbit (committed)
GATE_KEEP = 0.90


# ------------------------------------------------------------------------------- framework kernels
def nu_a1(y):
    """alpha = 1: the EXACT law.  g_obs = nu g_bar with g_obs^2 = g_bar^2 + a0 g_bar."""
    return np.sqrt(1.0 + 1.0 / np.asarray(y, float))


def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


# ---- FLOAT64 HAZARD, and it bit this script on the first run ------------------------------------
# Both excess functions are differences of two nearly-equal numbers at planetary y = g_bar/a_0.  In
# section 2a the ray grazes the Sun, g_bar ~ 100 m/s^2 => y ~ 1e12, and the naive
# sqrt(1+x^2) - 1 forms lose ALL significance: the first run of this file returned a NEGATIVE
# alpha=2 gamma-1 on the ALT footing (a sign flip out of pure cancellation).  Both are rewritten in
# expm1/log1p form below, and a convergence/consistency check against the analytic asymptote is run.
def excess_a1(gbar, a0):
    """(nu-1) g_bar for alpha = 1, cancellation-safe.  -> a0/2 exactly as y -> inf.
    sqrt(1+1/y) - 1 = expm1(log1p(1/y)/2)."""
    y = np.asarray(gbar, float) / a0
    return np.expm1(0.5 * np.log1p(1.0 / y)) * gbar


def excess_a2(gbar, a0):
    """(nu-1) g_bar for the alpha = 2 kernel K = sqrt(z/(1+z)), i.e. mu = x/sqrt(1+x^2).
    a0 x^2/sqrt(1+x^2) = g_bar has the CLOSED form x = y sqrt((1+sqrt(1+4/y^2))/2), so
        excess = a0 y [sqrt((1+sqrt(1+4/y^2))/2) - 1]
    evaluated with expm1/log1p throughout.  -> a0^2/(2 g_bar) as y -> inf."""
    y = np.asarray(gbar, float) / a0
    s = 4.0 / (y * y)
    r1 = np.expm1(0.5 * np.log1p(s))          # sqrt(1+s) - 1, exact for tiny s
    w = 0.5 * r1                              # (1+sqrt(1+s))/2 - 1
    return a0 * y * np.expm1(0.5 * np.log1p(w))


print(RULE)
print("LANE F -- THE CONSISTENCY GAUNTLET:  GW170817 c_T, PPN gamma/beta, Cassini Q2, LLR Gdot/G")
print(RULE)
print(f"""
  a_0 canonical = {A0['canon']:.4e} m/s^2   (kappa=1/2, rho_DE, cH_Lambda/Z;  kappa is FITTED)
  a_0 ALT       = {A0['alt']:.4e} m/s^2   (rho_total, cH0)   ratio = {A0['alt']/A0['canon']:.4f}
  c H_Lambda    = {CH_LAMBDA:.4e} m/s^2 ;  Z = {Z_CONST:.10f} ;  cH_Lambda/Z = {CH_LAMBDA/Z_CONST:.4e}
  Galactic external field at the Sun  a_ext = V^2/R = {A_EXT:.4e} m/s^2  (a_ext/a_0 =
      {A_EXT/A0['canon']:.4f} canon / {A_EXT/A0['alt']:.4f} alt)
  Kernel credit: nu = sqrt(1+1/y) is Milgrom 1999 PLA 253:273 eq 9.  The framework's own content is
  the cH_Lambda/Z coefficient (his was 2 cH_Lambda) plus the MI completion.
""")
chk("footing bookkeeping: a_0(canon) = cH_Lambda/Z to 0.1%",
    abs(A0["canon"] / (CH_LAMBDA / Z_CONST) - 1.0) < 1e-3,
    f"ratio = {A0['canon']/(CH_LAMBDA/Z_CONST):.6f}")
chk("footing bookkeeping: ALT/canon = 1/sqrt(Omega_Lambda) = 1.2082 to 0.3%",
    abs(A0["alt"] / A0["canon"] / 1.2082 - 1.0) < 3e-3,
    f"ratio = {A0['alt']/A0['canon']:.4f}")
chk("alpha=1 kernel: (nu-1) g_bar -> a_0/2 in the deep-Newton limit (the ephemeris landmine)",
    abs(excess_a1(1e8 * A0["canon"], A0["canon"]) / (A0["canon"] / 2) - 1.0) < 1e-7,
    f"ratio = {excess_a1(1e8*A0['canon'],A0['canon'])/(A0['canon']/2):.9f}")
chk("alpha=2 kernel: (nu-1) g_bar -> a_0^2/(2 g_bar), i.e. DECAYS (the relief axis)",
    abs(excess_a2(1e6 * A0["canon"], A0["canon"]) / (A0["canon"] ** 2 / (2 * 1e6 * A0["canon"])) - 1.0) < 1e-5,
    f"ratio = {excess_a2(1e6*A0['canon'],A0['canon'])/(A0['canon']**2/(2*1e6*A0['canon'])):.8f}")
# cancellation-safety: at the y ~ 1e12 the near-Sun ray actually reaches, both kernels must still
# track their analytic asymptotes.  The NAIVE forms fail here -- that is the point of the check.
print("\n  FLOAT64 CANCELLATION CHECK at the y the section-2a ray actually reaches (y ~ 1e12):")
naive_a1 = lambda gb, a0: (np.sqrt(1.0 + a0 / gb) - 1.0) * gb
naive_a2 = lambda gb, a0: a0 * (gb / a0) * (np.sqrt((1 + np.sqrt(1 + 4 * (a0 / gb) ** 2)) / 2) - 1)
print(f"  {'y':>10s}{'stable a1/(a0/2)':>20s}{'naive a1/(a0/2)':>20s}"
      f"{'stable a2/asym':>18s}{'naive a2/asym':>18s}")
naive_broke = False
for yy in (1e6, 1e9, 1e12):
    a0 = A0["canon"]
    gb = yy * a0
    s1, n1 = excess_a1(gb, a0) / (a0 / 2), naive_a1(gb, a0) / (a0 / 2)
    asym2 = a0 ** 2 / (2 * gb)
    s2, n2 = excess_a2(gb, a0) / asym2, naive_a2(gb, a0) / asym2
    naive_broke |= abs(n2 - 1) > 0.5
    print(f"  {yy:>10.0e}{s1:>20.9f}{n1:>20.9f}{s2:>18.9f}{n2:>18.9f}")
chk("float64: the expm1/log1p forms track BOTH analytic asymptotes to 1e-6 at y = 1e12, while the "
    "naive sqrt(...)-1 form for alpha=2 has lost all significance there (this is the bug that flipped "
    "a sign on the first run of this file)",
    abs(excess_a1(1e12 * A0["canon"], A0["canon"]) / (A0["canon"] / 2) - 1) < 1e-6
    and abs(excess_a2(1e12 * A0["canon"], A0["canon"]) / (A0["canon"] ** 2 / (2 * 1e12 * A0["canon"])) - 1) < 1e-6
    and naive_broke,
    "naive alpha=2 form breaks by >50% at y=1e12")


# =================================================================================================
head("SECTION 1 -- GW170817 / GRB170817A:  the tensor-mode speed c_T")
# =================================================================================================
print(f"""
  The bound.  GRB170817A arrived within [-0.01, +1.74] s of GW170817 after ~40 Mpc (Abbott+ 2017
  ApJL 848:L13) => |c_T/c - 1| <~ {CT_BOUND:.0e}.  This one constraint annihilated most of Horndeski
  (G4X, G5): Creminelli & Vernizzi 2017, Ezquiaga & Zumalacarregui 2017, Baker+ 2017.

  The framework's MI completion (published action, UNIFICATION.md sec 3):
      S = S_EH[g]  -  INT lambda/2 (u.u + 1)  -  1/2 INT rho_m [ s u^mu K(box_u/a_0^2) u_mu ]
          -  1/4 INT sqrt(-gtilde) F^2  with  gtilde = g + B u u
  plus the dark sector identified as a GHOST CONDENSATE, L = M^4 P(X), shift-symmetric, attractor
  P'(X) = 0, u_mu = grad_mu phi / sqrt(-(grad phi)^2) so u.u = -1 identically.

  FOUR independent places a c_T shift could enter.  Each is checked, each with a control that shows
  the check is not vacuous.
""")

# --- 1a Horndeski tensor sector -------------------------------------------------------------------
print("  1a. Horndeski tensor sector (Kobayashi, Yamaguchi & Yokoyama 2011 PTP 126:511):")
X, H, phid, phidd, Mpl, cc = sp.symbols("X H phidot phiddot M_pl c4", positive=True)
G4 = sp.Function("G4")
G5 = sp.Function("G5")
G4s, G4X, G5s, G5X, G5p = sp.symbols("G4 G4X G5 G5X G5phi", real=True)
G_T = 2 * (G4s - 2 * X * G4X - X * (H * phid * G5X - G5p))
F_T = 2 * (G4s - X * (G5p + phidd * G5X))
cT2 = sp.simplify(F_T / G_T)
print(f"       c_T^2 = F_T/G_T = {cT2}")
cT2_fw = sp.simplify(cT2.subs({G4X: 0, G5X: 0, G5p: 0}))
print(f"       framework:  G4 = M_pl^2/2 (constant)  =>  G4X = 0, G5 == 0  =>  c_T^2 = {cT2_fw}")
chk("1a  Horndeski c_T^2 = 1 EXACTLY when G4X = G5 = 0 (the framework's minimal coupling)",
    sp.simplify(cT2_fw - 1) == 0)
# control: a nonzero G4X must break it, else the check above is vacuous
kk = sp.Symbol("k", positive=True)
cT2_ctrl = sp.simplify(cT2.subs({G4s: Mpl ** 2 / 2 + kk * X, G4X: kk, G5X: 0, G5p: 0}))
ctrl_val = float(cT2_ctrl.subs({Mpl: 1.0, kk: 0.01, X: 1.0}))
print(f"       CONTROL  G4 = M_pl^2/2 + k X (G4X = k):  c_T^2 = {sp.simplify(cT2_ctrl)}"
      f"  -> at k=0.01, X=M_pl^2=1: {ctrl_val:.6f}")
chk("1a  CONTROL: G4X != 0 gives c_T^2 != 1, so the 1a check discriminates",
    sp.simplify(cT2_ctrl - 1) != 0 and abs(ctrl_val - 1.0) > 1e-3,
    f"|c_T^2-1| = {abs(ctrl_val-1):.4f}")

# --- 1b passive frame vs Einstein-aether ---------------------------------------------------------
print("\n  1b. The preferred timelike frame u_mu -- aether kinetic terms (Jacobson & Mattingly 2004):")
c1, c3 = sp.symbols("c1 c3", real=True)
cT2_ae = 1 / (1 - c1 - c3)
print(f"       Einstein-aether / generalised khronon:  c_T^2 = {cT2_ae}")
print("       The framework's u enters ONLY through the Lagrange constraint -lambda/2 (u.u+1) and")
print("       through rho_m u K(box_u) u.  There is NO (grad u)^2 term => c1 = c3 = 0 identically,")
print("       and the frame carries ZERO propagating dof (corpus: constraint_structure.py /")
print("       A10_dirac_block.py).  This is WHY c_T = 1 is structural and not a tuning.")
chk("1b  passive frame (c1 = c3 = 0, zero propagating dof) => c_T^2 = 1 exactly",
    sp.simplify(cT2_ae.subs({c1: 0, c3: 0}) - 1) == 0)
ae_ctrl = float(np.sqrt(1.0 / (1.0 - 0.1)) - 1.0)
chk("1b  CONTROL: an aether kinetic term with c1+c3 = 0.1 gives |c_T-1| = 5.4e-2, i.e. 1e14x over "
    "the bound -- so 'zero' must be EXACT, not merely small",
    ae_ctrl / CT_BOUND > 1e13, f"|c_T-1| = {ae_ctrl:.4e} = {ae_ctrl/CT_BOUND:.2e} x bound")
print("       NOTE, against interest: the framework's CMB-safe covariant limb is AeST (Skordis &")
print("       Zlosnik 2021), which DOES carry vector kinetic terms and gets c_T = c only by an")
print("       explicit design choice.  The MG limb passes by construction; the MI limb passes by")
print("       structure.  Neither is evidence FOR the framework -- GR passes exactly too.")

# --- 1c ghost condensate cannot touch the TT sector ----------------------------------------------
print("\n  1c. Does the ghost condensate contribute to the tensor kinetic term?  Exact symbolic test:")
a_s = sp.Symbol("a", positive=True)
h11, h12, h13, h22, h23 = sp.symbols("h11 h12 h13 h22 h23", real=True)
hTT = sp.Matrix([[h11, h12, h13], [h12, h22, h23], [h13, h23, -h11 - h22]])  # traceless
g4 = sp.zeros(4, 4)
g4[0, 0] = -1
g4[1:, 1:] = a_s ** 2 * (sp.eye(3) + hTT)
ginv = g4.inv()
phi_t = sp.Function("phi")(sp.Symbol("t"))
dphi = sp.Matrix([sp.diff(phi_t, sp.Symbol("t")), 0, 0, 0])
Xval = sp.simplify(-(dphi.T * ginv * dphi)[0, 0])
print(f"       g^00 for block-diagonal g with ARBITRARY traceless spatial block: {sp.simplify(ginv[0,0])}")
print(f"       X = -g^munu d_mu phi d_nu phi  with phi = phi(t):  X = {Xval}")
chk("1c  X is EXACTLY independent of h^TT (to all orders): g^00 = -1 for any spatial block",
    sp.simplify(ginv[0, 0] + 1) == 0 and sp.simplify(Xval - sp.diff(phi_t, sp.Symbol("t")) ** 2) == 0)
# control: give phi a spatial gradient -> X must then feel h
dphi_ctrl = sp.Matrix([sp.diff(phi_t, sp.Symbol("t")), sp.Symbol("px"), 0, 0])
X_ctrl = sp.simplify(-(dphi_ctrl.T * ginv * dphi_ctrl)[0, 0])
chk("1c  CONTROL: with a spatial gradient d_x phi != 0, X DOES depend on h^TT -> 1c is not vacuous",
    sp.simplify(sp.diff(X_ctrl, h11)) != 0)
print("       => L = M^4 P(X) is a pure background object in the TT sector.  It changes H(t), never")
print("          the graviton kinetic term.  Contribution to c_T: EXACTLY ZERO, all orders in h^TT.")

# --- 1d the MI operator is proportional to rho_m -------------------------------------------------
print("\n  1d. The MI term -1/2 INT rho_m [s u K(box_u/a_0^2) u] is proportional to rho_m.  Its")
print("      second-order-in-h piece competes with (c^4/16 pi G)(omega/c)^2 h^2.  Upper bound on the")
print("      fractional tensor-speed shift:  delta(c_T^2) <~ 16 pi G rho / omega^2.")
f_gw = 100.0
om_gw = 2 * np.pi * f_gw
rhos = [("IGM along the NGC4993 sightline", 1e-27, om_gw, True),
        ("mean cosmic matter rho_m0", 2.7e-27, om_gw, True),
        ("Milky Way ISM", 1e-21, om_gw, True),
        ("[not GW170817] PTA band, rho_m0 @ 3 nHz", 2.7e-27, 2 * np.pi * 3e-9, False)]
print(f"      {'medium':42s}{'rho [kg/m^3]':>15s}{'omega [rad/s]':>15s}{'d(c_T^2) bound':>17s}{'x bound':>12s}")
worst, worst_pta = 0.0, 0.0
for lab, rho, om, in_ligo in rhos:
    d = 16 * np.pi * G * rho / om ** 2
    if in_ligo:
        worst = max(worst, 0.5 * d / CT_BOUND)
    else:
        worst_pta = max(worst_pta, 0.5 * d / CT_BOUND)
    print(f"      {lab:42s}{rho:>15.2e}{om:>15.3e}{d:>17.3e}{0.5*d/CT_BOUND:>12.2e}")
chk("1d  in the LIGO band (the band GW170817 actually constrains) the rho_m-weighted MI contribution "
    "to c_T is <= 1e-18 of the bound in every propagation medium checked",
    worst < 1e-18, f"worst |c_T-1|/bound = {worst:.3e}")
chk("1d  the same bound degrades as 1/omega^2, so it is 1e6 x weaker in the nHz PTA band -- reported "
    "against interest, though GW170817 does not constrain that band and it is still <1e-4 of the limit",
    worst_pta / worst > 1e5 and worst_pta < 1e-4,
    f"PTA-band |c_T-1|/bound = {worst_pta:.3e} = {worst_pta/worst:.1e} x the LIGO-band value")
print("      NOTE: this quantity is a_0-BLIND at leading order (the ratio has no a_0 in it), so it")
print("      does not discriminate the footings -- stated rather than dressed up as a both-footings")
print("      result.")

# --- 1e the channel that actually FAILS: the disformal photon --------------------------------------
print("\n  1e. What GW170817 actually measures is the GRAVITON-PHOTON ARRIVAL DIFFERENCE.  The")
print("      framework's own lensing sector puts photons on gtilde = g + B u u, so c_gamma =")
print("      sqrt(1-B) < c_T = c.  Independent re-derivation of the line integral (corpus:")
print("      prep_2026/gw170817_check/RESULT.md, reproduced here, not read-and-agreed):")


def B_deep_mond_shell(a0, Mgal, r_in, r_out, n=200001):
    """Dimensionless B from grad B = 4(nu-1)g_bar/c^2, boundary B->0 at r_out (void BC, the choice
    most favourable to the framework).  B(r) = (4/c^2) INT_r^{r_out} (nu-1) g_bar dr'."""
    r = np.linspace(r_in, r_out, n)
    gbar = G * Mgal / r ** 2
    integ = (4.0 / c ** 2) * (nu_a1(gbar / a0) - 1.0) * gbar
    Bcum = np.concatenate(([0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(r))))
    B = Bcum[-1] - Bcum                    # B(r), zero at r_out
    dt = np.trapz(1.0 / np.sqrt(1.0 - np.clip(B, 0, 0.9)) - 1.0, r) / c
    return B.max(), dt


D_GW = 40.0 * MPC
t_travel = D_GW / c
print(f"      {'footing':8s}{'B_max host':>13s}{'B_max MW':>11s}{'Dt host+MW [s]':>17s}"
      f"{'|dc|/c':>12s}{'vs 1.74 s':>13s}{'vs 1e-15':>12s}")
gwres = {}
for f_ in ("canon", "alt"):
    a0 = A0[f_]
    Bh, dth = B_deep_mond_shell(a0, 1e11 * M_SUN, 2.0 * KPC, 300.0 * KPC)
    Bm, dtm = B_deep_mond_shell(a0, 6e10 * M_SUN, 8.0 * KPC, 300.0 * KPC)
    dt = dth + dtm
    dc = dt / t_travel
    gwres[f_] = (Bh, Bm, dt, dc)
    print(f"      {f_:8s}{Bh:>13.3e}{Bm:>11.3e}{dt:>17.3e}{dc:>12.3e}"
          f"{dt/1.74:>13.2e}{dc/1e-15:>12.2e}")
chk("1e  B_max in the host MOND shell reproduces the corpus 4.5e-6 within a factor 3, both footings",
    all(0.33 < gwres[f_][0] / (4.5e-6 if f_ == "canon" else 5.1e-6) < 3.0 for f_ in ("canon", "alt")),
    f"canon {gwres['canon'][0]:.2e} vs 4.5e-6 ; alt {gwres['alt'][0]:.2e} vs 5.1e-6")
chk("1e  Delta_t (host + MW crossings only, IGM = 0) reproduces the corpus 3.5e7 s within a factor "
    "6, both footings",
    all(1 / 6 < gwres[f_][2] / (3.5e7 if f_ == "canon" else 3.9e7) < 6.0 for f_ in ("canon", "alt")),
    f"canon {gwres['canon'][2]:.2e} s ; alt {gwres['alt'][2]:.2e} s")
chk("1e  FAILURE, both footings: the photon-graviton arrival difference exceeds the 1.74 s bound by "
    ">1e6",
    all(gwres[f_][2] / 1.74 > 1e6 for f_ in ("canon", "alt")),
    f"canon x{gwres['canon'][2]/1.74:.2e} ; alt x{gwres['alt'][2]/1.74:.2e}")
print(f"""
      VERDICT for section 1, stated without softening:
        * TENSOR SPEED, narrowly construed: c_T = c EXACTLY, by structure, for three independent
          reasons (G4X = G5 = 0; c1 = c3 = 0 with zero frame dof; P(X) blind to h^TT).  The only
          non-structural piece is the rho_m-weighted MI operator, bounded above at {worst:.1e} of the
          GW170817 limit.  PASS, and the margin is ~{1/max(worst,1e-99):.1e}.
        * THE MULTI-MESSENGER CONSTRAINT: FAIL by ~7 orders, both footings, through the framework's
          OWN disformal photon sector.  The graviton rides the clean metric g; the photon rides the
          tilted cone gtilde, and the two mandatory galaxy-shell crossings alone give Dt ~ 1e7-1e8 s.
        * So "c_T = 1 exactly" is TRUE and is NOT a GW170817 pass.  Quoting the first without the
          second would be a manufactured win.  What is excluded is the disformal photon-metric route
          to dark-matter-free lensing -- the RAR, BTFR, a_0-line and spherical dynamics are untouched.
""")


# =================================================================================================
head("SECTION 2 -- PPN gamma and beta in the solar-system limit")
# =================================================================================================
print(f"""
  In modified INERTIA host gravity is UNMODIFIED: S_EH[g] alone, linear Poisson, no phantom source.
  The exterior metric of the Sun is therefore EXACTLY Schwarzschild, so at the metric level
  gamma = beta = 1 identically -- there is no O(Phi^2) nonlinearity to shift beta and no anisotropic
  stress to shift gamma.  The observable deviations do NOT live in the metric; they live in (i) the
  disformal photon cone (gamma channel) and (ii) the non-geodesic worldline (the beta channel's
  physical stand-in).  Both are computed here.

  Bounds:  Cassini gamma - 1 = ({GAM_C:.1e} +/- {GAM_S:.1e})  ->  2 sigma ceiling |gamma-1| <= {GAM_CEIL:.2e}
           LLR Nordtvedt eta_N = 4 beta - gamma - 3 = ({ETA_N_C:.1e} +/- {ETA_N_S:.1e})
             -> with gamma = 1: |beta - 1| <= {(abs(ETA_N_C)+2*ETA_N_S)/4:.2e} at 2 sigma
""")

# --- 2a gamma at the REAL Cassini ray geometry ----------------------------------------------------
print("  2a. gamma from the disformal photon metric, at the ACTUAL Cassini ray geometry.")
print("      Lensing potential = Phi - B/4 with grad(c^2 B) = 4 (nu-1) g_bar (UNIFICATION.md sec 2),")
print("      so the anomalous transverse gradient on light is exactly (nu-1) g_bar -- the SAME")
print("      anomalous acceleration matter feels, which is the point of the construction.")
print("      alpha_defl = (2/c^2) INT grad_perp Phi_eff dl ;  gamma - 1 = 2 Delta alpha / alpha_GR.")
b_ray = 1.6 * R_SUN          # 2002 superior-conjunction impact parameter, ~1.6 R_sun
L_earth, L_sat = 1.0 * AU, 8.5 * AU
alpha_GR = 4 * GM_SUN / (c ** 2 * b_ray)


def gamma_ray(a0, excess, npts=400001):
    """LOS integral, split at the impact point and done on a log-spaced grid on each side (the
    integrand is peaked over ~b within a 1e3 b range -- plain quad on the full range warns and
    under-resolves).  Grid refinement is reported, not assumed."""
    def f(l):
        r = np.sqrt(b_ray ** 2 + l ** 2)
        return excess(GM_SUN / r ** 2, a0) * (b_ray / r)

    tot = 0.0
    for L in (L_earth, L_sat):
        u = np.concatenate(([0.0], np.logspace(np.log10(b_ray * 1e-4), np.log10(L), npts - 1)))
        tot += np.trapz(f(u), u)
    return 2.0 * (2.0 * tot / c ** 2) / alpha_GR


# grid-refinement audit (float64 hazard: a coarse grid reporting an unsampled value)
g_lo = gamma_ray(A0["canon"], excess_a1, 100001)
g_hi = gamma_ray(A0["canon"], excess_a1, 400001)
print(f"      grid refinement 1e5 -> 4e5 points: gamma-1 = {g_lo:.8e} -> {g_hi:.8e}  "
      f"(shift {abs(g_hi/g_lo-1):.2e})")
chk("2a  the LOS quadrature is converged: a 4x grid refinement shifts gamma-1 by < 1e-4",
    abs(g_hi / g_lo - 1) < 1e-4, f"shift = {abs(g_hi/g_lo-1):.3e}")
# analytic cross-check: for alpha=1 the excess is exactly a0/2, so the integral is closed-form
ana_a1 = (2.0 * (2.0 * (A0["canon"] / 2) * b_ray
                 * (np.arcsinh(L_earth / b_ray) + np.arcsinh(L_sat / b_ray)) / c ** 2) / alpha_GR)
chk("2a  CROSS-CHECK: for alpha=1 the excess is the constant a_0/2, so Delta alpha = (a_0 b/c^2)"
    "[asinh(L1/b)+asinh(L2/b)] in closed form -- the quadrature matches it to 0.1%",
    abs(g_hi / ana_a1 - 1) < 1e-3, f"quad/closed-form = {g_hi/ana_a1:.6f}")

gam = {}
print(f"      {'footing':8s}{'alpha=1 gamma-1':>18s}{'x Cassini ceil':>16s}"
      f"{'alpha=2 gamma-1':>18s}{'x Cassini ceil':>16s}")
for f_ in ("canon", "alt"):
    g1 = gamma_ray(A0[f_], excess_a1)
    g2 = gamma_ray(A0[f_], excess_a2)
    gam[f_] = (g1, g2)
    print(f"      {f_:8s}{g1:>18.4e}{g1/GAM_CEIL:>16.2e}{g2:>18.4e}{g2/GAM_CEIL:>16.2e}")
chk("2a  gamma-1 at the Cassini ray geometry PASSES on alpha=1, both footings, by > 1e6",
    all(gam[f_][0] / GAM_CEIL < 1e-6 for f_ in ("canon", "alt")),
    f"canon {gam['canon'][0]/GAM_CEIL:.2e} ; alt {gam['alt'][0]/GAM_CEIL:.2e} of the ceiling")
chk("2a  alpha=2 is tighter still (its excess decays as 1/g_bar): gamma-1(alpha=2) < gamma-1(alpha=1)"
    " by > 1e6",
    all(gam[f_][1] / gam[f_][0] < 1e-6 for f_ in ("canon", "alt")),
    f"canon ratio {gam['canon'][1]/gam['canon'][0]:.2e}")

# --- 2b reproduce the corpus's Saturn-local number and show it is CONSERVATIVE ---------------------
gN_sat = GM_SUN / R_SAT ** 2
loc = {f_: A0[f_] / (2 * gN_sat) for f_ in A0}
print(f"\n  2b. The corpus (UNIFICATION.md sec 4) quotes |Delta gamma| ~ 7.2e-7 (canon) / 8.7e-7 (alt)")
print(f"      'at Saturn'.  That is the LOCAL deep-Newton boost nu-1 = a_0/(2 g_N) at r = 9.58 AU:")
print(f"      canon {loc['canon']:.3e}, alt {loc['alt']:.3e}.  Reproduced.")
chk("2b  reproduce the corpus's Saturn-local |Delta gamma| = 7.2e-7 / 8.7e-7 to 1%",
    abs(loc["canon"] / 7.2e-7 - 1) < 0.02 and abs(loc["alt"] / 8.7e-7 - 1) < 0.02,
    f"canon {loc['canon']:.3e}, alt {loc['alt']:.3e}")
chk("2b  the Saturn-local evaluation is CONSERVATIVE by >1e4 vs the real Cassini ray geometry (the "
    "ray grazes the Sun at 1.6 R_sun where g_N is 1e6 x larger)",
    loc["canon"] / gam["canon"][0] > 1e4,
    f"ratio = {loc['canon']/gam['canon'][0]:.2e}")

# --- 2c beta, and why the beta pass is vacuous -----------------------------------------------------
print("\n  2c. beta.  The metric is Schwarzschild => beta - 1 = 0 EXACTLY.  But PPN presumes GEODESIC")
print("      test-body motion, and modified inertia breaks exactly that hypothesis.  So beta = 1 does")
print("      NOT mean the perihelion motion is GR's.  The physically meaningful number in the beta")
print("      channel is the secular apsidal drift driven by the constant sunward a_0/2 anomaly.")
print("      Closed form for a constant inward perturbation k:  d(varpi)/orbit = -2 pi k a^2 sqrt(1-e^2)/GM")
print("      -- derived here and VALIDATED against my own orbit integration with a k=0 noise control.")


def prec_numeric(a, e, k, N=60):
    n = np.sqrt(GM_SUN / a ** 3)
    T = 2 * np.pi / n

    def rhs(t, y):
        x, yy, vx, vy = y
        r = np.hypot(x, yy)
        return [vx, vy, -GM_SUN * x / r ** 3 - k * x / r, -GM_SUN * yy / r ** 3 - k * yy / r]

    rp, vp = a * (1 - e), np.sqrt(GM_SUN * (1 + e) / (a * (1 - e)))
    s = solve_ivp(rhs, [0, N * T], [rp, 0.0, 0.0, vp], rtol=3e-13, atol=1e-6, dense_output=True)
    ts = np.linspace(0, N * T, 20001)
    x, y, vx, vy = s.sol(ts)
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    ex = (v2 / GM_SUN - 1.0 / r) * x - rv * vx / GM_SUN
    ey = (v2 / GM_SUN - 1.0 / r) * y - rv * vy / GM_SUN
    return np.polyfit(ts, np.unwrap(np.arctan2(ey, ex)), 1)[0] * T


def prec_closed(a, e, k):
    return -2 * np.pi * k * a ** 2 * np.sqrt(1 - e ** 2) / GM_SUN


k_can = A0["canon"] / 2
print(f"      {'planet':9s}{'numeric [rad/orbit]':>22s}{'closed form':>16s}{'ratio':>9s}{'k=0 noise':>13s}")
prec_ok = True
for nm in ("Mercury", "Mars"):
    a, e, P = PLANETS[nm]
    num = prec_numeric(a, e, k_can)
    ana = prec_closed(a, e, k_can)
    noise = prec_numeric(a, e, 0.0)
    prec_ok &= abs(num / ana - 1) < 0.02 and abs(noise) < abs(num) / 1000
    print(f"      {nm:9s}{num:>22.5e}{ana:>16.5e}{num/ana:>9.4f}{noise:>13.2e}")
chk("2c  the constant-radial precession closed form is validated by my own orbit integration to 2%, "
    "with the k=0 noise floor >1000x below the signal",
    prec_ok)

print("\n      The anomaly in both currencies, both footings, alpha=1 (the EXACT law):")
print(f"      {'planet':9s}{'a_0/2 [m/s^2]':>16s}{'delta A_R 2sig':>16s}{'x over':>9s}"
      f"{'|dvarpi| [as/cy]':>18s}{'bound [as/cy]':>15s}")
eph = {}
for f_ in ("canon", "alt"):
    k = A0[f_] / 2
    for nm, bd in (("Earth", DAR_EARTH), ("Mars", DAR_MARS)):
        a, e, P = PLANETS[nm]
        norb = 100.0 / P
        dvp = abs(prec_closed(a, e, k)) * norb * 206264.806
        dvp_b = abs(prec_closed(a, e, bd)) * norb * 206264.806
        eph[(f_, nm)] = k / bd
        print(f"      {nm+'/'+f_:9s}{k:>16.4e}{bd:>16.3e}{k/bd:>9.1f}{dvp:>18.4e}{dvp_b:>15.3e}")
chk("2c  reproduce the corpus ephemeris liability 1279x (canon) / 1544x (alt) on the Earth bound, "
    "to 1%",
    abs(eph[("canon", "Earth")] / 1279 - 1) < 0.01 and abs(eph[("alt", "Earth")] / 1544 - 1) < 0.01,
    f"canon {eph[('canon','Earth')]:.1f}x, alt {eph[('alt','Earth')]:.1f}x")
chk("2c  the two currencies agree by construction (both linear in k) -- recorded as a coherence "
    "check on the Sereno & Jetzer inversion, NOT as independent evidence",
    abs((abs(prec_closed(PLANETS["Mars"][0], PLANETS["Mars"][1], k_can))
         / abs(prec_closed(PLANETS["Mars"][0], PLANETS["Mars"][1], DAR_MARS))) / (k_can / DAR_MARS) - 1) < 1e-12)
print("      alpha = 2 relief, for contrast -- and the trap the corpus already corrected:")
for f_ in ("canon", "alt"):
    a0 = A0[f_]
    pl = excess_a2(GM_SUN / AU ** 2, a0)
    print(f"        {f_}: PLANET-carried alpha=2 anomaly at Earth = {pl:.3e} m/s^2 = {pl/DAR_EARTH:.2e} x "
          f"the bound -- but this evaluation is the one the corpus CORRECTED 2026-08-02: the binding")
    print(f"           body is the SUN's reflex (g ~ 2.1e-7 m/s^2), giving 6.2-8.5x over (canon) / "
          f"9.0-12.4x (alt) per mi_alpha2_sun_reflex_2026.py.  NOT re-derived here; NOT a pass.")
chk("2c  the planet-carried alpha=2 number is <1e-4 of the bound, i.e. it would LOOK like a pass -- "
    "flagged as the corrected-and-retired evaluation so it is not re-used as one",
    excess_a2(GM_SUN / AU ** 2, A0["canon"]) / DAR_EARTH < 1e-4)

# --- 2d the gamma pass is MOND-SHARED -------------------------------------------------------------
print("\n  2d. IS THE gamma PASS EVIDENCE FOR THE FRAMEWORK?  No -- it is MOND-SHARED.  gamma-1 scales")
print("      linearly in a_0, so every a_0 in the literature gives the same answer to within a factor")
print("      of ~1.3, while the bound is ~1e7 away.  Discriminating power is nil:")
a0_menu = [("framework canon 9.36e-11", A0["canon"]), ("framework ALT 1.13e-10", A0["alt"]),
           ("McGaugh RAR 1.20e-10", 1.20e-10), ("Milgrom 2 cH_Lambda 1.08e-9", 2 * CH_LAMBDA)]
gvals = []
for lab, a0 in a0_menu:
    gv = gamma_ray(a0, excess_a1)
    gvals.append(gv)
    print(f"      {lab:28s}gamma-1 = {gv:.4e}   ({gv/GAM_CEIL:.2e} of the Cassini ceiling)")
spread = (max(gvals) - min(gvals)) / GAM_CEIL
chk("2d  the FULL spread of gamma-1 across every a_0 on the menu is < 1e-5 of the Cassini ceiling => "
    "gamma cannot separate the framework from any MOND variant, nor from GR",
    spread < 1e-5, f"spread/ceiling = {spread:.3e}")

# --- 2e a corpus liability that does NOT survive checking -----------------------------------------
print("\n  2e. CHECKING A CORPUS *LIABILITY* AS HARD AS A CORPUS WIN.  STANDING.md sec 5 item 0 states")
print("      that the disformal construction 'sends a SECOND BILL': that B varies by 257 (canon) /")
print("      311 (alt) across Mercury->Saturn, '~2 orders over its own premise' B < 1.  But the")
print("      framework's own line-integral script uses grad B = 4(nu-1) g_bar / c^2 (gw170817_")
print("      lineintegral.py:10,52), i.e. B is DIMENSIONLESS.  257 is the c^2-less m^2/s^2 value.")
dB_dimful, dB_dimless = {}, {}
for f_ in ("canon", "alt"):
    a0 = A0[f_]
    r1, r2 = PLANETS["Mercury"][0], R_SAT
    fint = lambda r: excess_a1(GM_SUN / r ** 2, a0)
    dB_dimful[f_] = 4.0 * quad(fint, r1, r2, limit=400)[0]
    dB_dimless[f_] = dB_dimful[f_] / c ** 2
    print(f"      {f_}: Delta(c^2 B) Mercury->Saturn = {dB_dimful[f_]:.1f} m^2/s^2   ->  "
          f"Delta B = {dB_dimless[f_]:.3e}  (dimensionless)")
chk("2e  reproduce the corpus's 257 (canon) / 311 (alt) as the DIMENSIONFUL c^2 B, to 2%",
    abs(dB_dimful["canon"] / 257 - 1) < 0.02 and abs(dB_dimful["alt"] / 311 - 1) < 0.02,
    f"canon {dB_dimful['canon']:.1f}, alt {dB_dimful['alt']:.1f}")
chk("2e  WITHDRAWAL: the dimensionless B across the solar system is ~3e-15 << 1, so the 'B > 1, "
    "2 orders over its own premise' second bill is a c^2 units slip and does NOT stand",
    max(dB_dimless.values()) < 1e-10,
    f"max Delta B = {max(dB_dimless.values()):.3e}")
# what DOES stand: dB/dr is 4x the ephemeris anomaly.  Tested by DIFFERENTIATING the B integral
# numerically and comparing to an independently-evaluated 4(nu-1)g_bar -- not by re-dividing 4x by x.
h_step = R_SAT * 1e-6
Bint = lambda rr: 4.0 * quad(lambda r: excess_a1(GM_SUN / r ** 2, A0["canon"]),
                             PLANETS["Mercury"][0], rr, limit=400)[0]
dBdr_num = (Bint(R_SAT + h_step) - Bint(R_SAT - h_step)) / (2 * h_step)
dBdr_pred = 4.0 * excess_a1(gN_sat, A0["canon"])
print(f"      numerical d(c^2 B)/dr at Saturn = {dBdr_num:.9e} ;  4(nu-1)g_bar = {dBdr_pred:.9e} ;  "
      f"ratio to the ephemeris anomaly (nu-1)g_bar = {dBdr_num/excess_a1(gN_sat, A0['canon']):.6f}")
chk("2e  what DOES stand: differentiating the B line integral gives d(c^2 B)/dr = 4 x the ephemeris "
    "anomaly (nu-1) g_bar to 1e-5, so the disformal sector is NOT independent evidence about alpha",
    abs(dBdr_num / dBdr_pred - 1) < 1e-5
    and abs(dBdr_num / excess_a1(gN_sat, A0["canon"]) - 4.0) < 1e-4,
    f"d(c^2 B)/dr / (nu-1)g_bar = {dBdr_num/excess_a1(gN_sat, A0['canon']):.6f} (predicted 4)")
print("      Net: one liability line in STANDING.md needs correcting (the B<1 'second bill'), and")
print("      the correction does NOT rescue alpha=1 -- the 1279x/1544x ephemeris wall is untouched.")


# =================================================================================================
head("SECTION 3 -- The Cassini Q2 quadrupole:  does PURE MI inherit the MG realization's wall?")
# =================================================================================================
print(f"""
  The wall.  Desmond, Hees & Famaey 2024 (MNRAS 530:1781) rule out the RAR interpolating function at
  8.7 sigma by confronting the SPARC RAR with the Cassini solar-system quadrupole; Park+ 2026
  (arXiv:2602.17884) tighten it to Q2 = ({Q2_C:.1e} +/- {Q2_S:.1e}) s^-2, 2 sigma ceiling {Q2_CEIL:.2e}.
  The corpus records the tension as 3-15 sigma and records that the framework's AeST (= modified
  GRAVITY) realization INHERITS it.  Question: does the pure MI realization inherit it too?

  Mechanism, and it is the whole answer.  In modified GRAVITY the anisotropic galactic external
  field feeds a PHANTOM density rho_ph = (1/4 pi G) div[(nu-1) g], sourced by a NONLINEAR Poisson
  operator, which produces an r-INDEPENDENT quadrupole near the Sun.  In modified INERTIA the Sun's
  field is EXACTLY Newtonian -- there is no phantom density at all -- and the external field enters
  only through the argument of the test body's own inertia.  Two different objects, same nu, same a_0.
""")

# --- 3a MG side: Milgrom 2009 / Desmond+24 eq (12), with an external anchor ------------------------
print("  3a. MG (AQUAL/QUMOND) side -- Milgrom 2009 MNRAS 399:474, as written in Desmond+24 eq (12):")
print("      q = 3/2 INT_0^inf dv INT_-1^1 dxi  delta(Y) [ e_N(3xi - 5xi^3) + v^2(1 - 3xi^2) ],")
print("      Y = sqrt(e_N^2 + v^4 + 2 e_N v^2 xi),  delta = nu - 1,  Q2 = -(3 a_0^3/2 / 2 sqrt(GM)) q")


def q_milgrom(delta, eN, vmax=80.0):
    def ig(xi, v):
        D = eN * eN + v ** 4 + 2.0 * eN * v * v * xi
        if D <= 0.0:
            return 0.0
        return float(delta(np.sqrt(D))) * (eN * (3 * xi - 5 * xi ** 3) + v * v * (1 - 3 * xi * xi))
    val, _ = integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0,
                               epsabs=1e-11, epsrel=1e-7)
    return 1.5 * val


def Q2_from_q(q, a0):
    return -(3.0 * a0 ** 1.5) / (2.0 * np.sqrt(GM_SUN)) * q


def solve_eN(delta, etilde):
    """External field in a_0 units: the NEWTONIAN e_N that reproduces the observed etilde."""
    return brentq(lambda e: e * (1.0 + float(delta(e))) - etilde, 1e-8, etilde, xtol=1e-14)


d_frame = lambda y: nu_a1(y) - 1.0
d_rar = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.asarray(y, float)))) - 1.0   # McGaugh 2008 eq 11a
# ANCHOR: RAR IF at a0 = 1.2e-10 must reproduce Desmond+24's 8.7-sigma class vs the 2024 datum
eN_a = solve_eN(d_rar, A_EXT / 1.20e-10)
Q2_a = Q2_from_q(q_milgrom(d_rar, eN_a), 1.20e-10)
sig_a = (Q2_a - Q2_2024_C) / Q2_2024_S
print(f"      ANCHOR (Desmond+24): RAR IF, a_0 = 1.20e-10, e_tilde = {A_EXT/1.20e-10:.4f} -> e_N = "
      f"{eN_a:.4f}, Q2 = {Q2_a:.3e} s^-2 = {sig_a:+.1f} sigma vs the 2024 (3+/-3)e-27")
chk("3a  ANCHOR: my eq(12) implementation reproduces Desmond+24's published 8.7-sigma exclusion of "
    "the RAR IF in order and sigma-class (6-14 sigma) -- this validates the solver",
    1e-26 < Q2_a < 6e-26 and 6.0 < sig_a < 14.0, f"Q2 = {Q2_a:.3e}, {sig_a:+.1f} sigma")
print(f"\n      NOW THE FRAMEWORK'S OWN nu (never McGaugh's), both footings:")
print(f"      {'footing':8s}{'e_tilde':>9s}{'e_N':>9s}{'q':>10s}{'Q2 [s^-2]':>14s}"
      f"{'x 2sig ceil':>13s}{'sigma':>8s}")
Q2_MG = {}
for f_ in ("canon", "alt"):
    a0 = A0[f_]
    et = A_EXT / a0
    eN = solve_eN(d_frame, et)
    q = q_milgrom(d_frame, eN)
    Q2 = Q2_from_q(q, a0)
    Q2_MG[f_] = Q2
    print(f"      {f_:8s}{et:>9.4f}{eN:>9.4f}{q:>10.5f}{Q2:>14.4e}{Q2/Q2_CEIL:>13.2f}"
          f"{(Q2-Q2_C)/Q2_S:>8.1f}")
chk("3a  MG realization with the framework's OWN nu FAILS Cassini Q2 on both footings (> 2 sigma "
    "ceiling), at 11-13 sigma -- the corpus's 'AeST limb inherits the wall' reproduced",
    all(Q2_MG[f_] > Q2_CEIL for f_ in ("canon", "alt"))
    and all((Q2_MG[f_] - Q2_C) / Q2_S > 6.0 for f_ in ("canon", "alt")),
    f"canon {Q2_MG['canon']:.3e} = {(Q2_MG['canon']-Q2_C)/Q2_S:.1f} sigma ; "
    f"alt {Q2_MG['alt']:.3e} = {(Q2_MG['alt']-Q2_C)/Q2_S:.1f} sigma")
print("      AGAINST INTEREST: my numbers (2.2-2.5e-26) sit slightly ABOVE the corpus's own D4 band")
print("      (1.2-2.0e-26, '+6 to +14 sigma').  Same class, same verdict; I report the higher number")
print("      rather than the corpus's, because it is the one my own solver produces.")

# --- 3b MI side: derived here from the framework's own EOM ------------------------------------------
print("\n  3b. MI side -- derived from scratch, NOT the phantom formula.  EOM: mu_fw(|A|/a_0) A = g_tot")
print("      with g_tot EXACTLY Newtonian.  Write A = delta + A_sun, eps = a_ext/|delta|, xi = cos angle.")
print("      |A| = |delta|[1 + eps xi + (eps^2/2)(1-xi^2) + ...], and for alpha = 1")
print("        nu(|A|/a_0) = 1 + a_0/(2|A|) = 1 + (a_0/2|delta|)[ 1 - eps xi + eps^2 P2(xi) + ... ]")
print("      so the anomalous radial acceleration grades as")
print("        l=0: a_0/2            (the constant sunward term -- the ephemeris landmine)")
print("        l=1: -(a_0/2) eps xi  (first order in a_ext)")
print("        l=2: +(a_0/2) eps^2 P2(xi)  (SECOND order in a_ext -- what Cassini constrains)")
print("      Symbolic verification of the eps^2 coefficient (that it is exactly P2), then the numbers.")
eps_s, xi_s = sp.symbols("epsilon xi", real=True)
mag = sp.sqrt(1 + 2 * eps_s * xi_s + eps_s ** 2)
ser = sp.series(1 / mag, eps_s, 0, 3).removeO().expand()
c0 = ser.coeff(eps_s, 0)
c1_ = sp.simplify(ser.coeff(eps_s, 1))
c2_ = sp.simplify(ser.coeff(eps_s, 2))
P2 = (3 * xi_s ** 2 - 1) / 2
print(f"      1/|A|-expansion: O(1) = {c0}, O(eps) = {c1_}, O(eps^2) = {sp.factor(c2_)}  ;  P2 = {P2}")
chk("3b  symbolic: the O(eps^2) coefficient of the inertia boost is EXACTLY the Legendre P2(xi)",
    sp.simplify(c2_ - P2) == 0 and sp.simplify(c1_ + xi_s) == 0)
chk("3b  CONTROL: the O(eps) coefficient is -xi (pure l=1), NOT P2 -- so the l=1/l=2 grading is real "
    "and not an artefact of the expansion",
    sp.simplify(c1_ - P2) != 0)


def Q2_MI_l2(a0, r, a_ext=A_EXT):
    """MI l=2: radial anomaly (a0/2) eps^2 P2, eps = a_ext/g_N, matched to
    delta_Phi = -(Q2/2)[(x.e)^2 - x^2/3] whose radial accel is (2 Q2 r/3) P2."""
    gN = GM_SUN / r ** 2
    eps = a_ext / gN
    return 1.5 * (a0 / 2.0) * eps ** 2 / r


def A_MI_l1(a0, r, a_ext=A_EXT):
    gN = GM_SUN / r ** 2
    return (a0 / 2.0) * (a_ext / gN)


Q2_MI, A1_MI = {}, {}
print(f"\n      {'footing':8s}{'l=1 accel [m/s^2]':>20s}{'l=1 /r [s^-2]':>16s}"
      f"{'l=2 Q2 [s^-2]':>16s}{'x 2sig ceil':>13s}")
for f_ in ("canon", "alt"):
    a0 = A0[f_]
    A1 = A_MI_l1(a0, R_SAT)
    Q2 = Q2_MI_l2(a0, R_SAT)
    A1_MI[f_], Q2_MI[f_] = A1, Q2
    print(f"      {f_:8s}{A1:>20.4e}{A1/R_SAT:>16.4e}{Q2:>16.4e}{Q2/Q2_CEIL:>13.3e}")
chk("3b  reproduce the corpus MI l=1 dipole scale 1.5e-28 s^-2 (canon) within a factor 3",
    1 / 3 < (A1_MI["canon"] / R_SAT) / 1.5e-28 < 3.0,
    f"mine {A1_MI['canon']/R_SAT:.3e} vs corpus 1.5e-28")
chk("3b  reproduce the corpus MI l=2 quadrupole 7.4e-34 s^-2 (canon) within a factor 3",
    1 / 3 < Q2_MI["canon"] / 7.4e-34 < 3.0,
    f"mine {Q2_MI['canon']:.3e} vs corpus 7.4e-34")
chk("3b  MI PASSES Cassini Q2 on both footings by > 1e6",
    all(Q2_MI[f_] / Q2_CEIL < 1e-6 for f_ in ("canon", "alt")),
    f"canon {Q2_MI['canon']/Q2_CEIL:.2e} ; alt {Q2_MI['alt']/Q2_CEIL:.2e} of the ceiling")
# structure: the MI anisotropy is NOT of Cassini's r-independent form
r_test = np.array([PLANETS["Mercury"][0], R_SAT])
ratio_r3 = Q2_MI_l2(A0["canon"], r_test[0]) / Q2_MI_l2(A0["canon"], r_test[1])
chk("3b  STRUCTURAL CAVEAT, stated because it is generous to the test: Q2_MI scales as r^3, so it is "
    "not the r-independent object Cassini fits -- verified (r_Merc/r_Sat)^3 to 1e-12",
    abs(ratio_r3 / (r_test[0] / r_test[1]) ** 3 - 1) < 1e-12,
    f"Q2(Merc)/Q2(Sat) = {ratio_r3:.4e} = (r ratio)^3")

# --- 3c the internal discriminator ----------------------------------------------------------------
print("\n  3c. THE INTERNAL DISCRIMINATOR between the framework's own two realizations:")
print(f"      {'footing':8s}{'Q2_MG [s^-2]':>15s}{'Q2_MI [s^-2]':>15s}{'MG/MI':>12s}{'verdict':>34s}")
for f_ in ("canon", "alt"):
    rr = Q2_MG[f_] / Q2_MI[f_]
    print(f"      {f_:8s}{Q2_MG[f_]:>15.4e}{Q2_MI[f_]:>15.4e}{rr:>12.3e}"
          f"{'MG FAILS / MI PASSES':>34s}")
chk("3c  Q2_MG / Q2_MI > 1e6 on both footings: pure MI does NOT inherit the wall.  This IS a real "
    "internal discriminator -- same a_0, same nu, opposite verdict",
    all(Q2_MG[f_] / Q2_MI[f_] > 1e6 for f_ in ("canon", "alt")),
    f"canon {Q2_MG['canon']/Q2_MI['canon']:.2e} ; alt {Q2_MG['alt']/Q2_MI['alt']:.2e}")

# --- 3d the price MI pays -------------------------------------------------------------------------
print("\n  3d. WHAT MI PAYS FOR THE EVASION.  The same expansion that kills the l=2 term at eps^2")
print("      leaves the l=0 term at FULL STRENGTH: a_0/2, constant, sunward, r-independent.  That is")
print("      the ephemeris liability of section 2c.  The wall MOVES from l=2 to l=0; it does not go.")
print(f"      {'realization':14s}{'failing multipole':>20s}{'excess factor (canon/alt)':>30s}")
print(f"      {'MG (AeST)':14s}{'l=2 (Cassini Q2)':>20s}"
      f"{f'{Q2_MG[chr(99)+chr(97)+chr(110)+chr(111)+chr(110)]/Q2_CEIL:.1f}x / {Q2_MG[chr(97)+chr(108)+chr(116)]/Q2_CEIL:.1f}x':>30s}")
print(f"      {'MI (pure)':14s}{'l=0 (Earth ranging)':>20s}"
      f"{f'{eph[(chr(99)+chr(97)+chr(110)+chr(111)+chr(110), chr(69)+chr(97)+chr(114)+chr(116)+chr(104))]:.0f}x / {eph[(chr(97)+chr(108)+chr(116), chr(69)+chr(97)+chr(114)+chr(116)+chr(104))]:.0f}x':>30s}")
chk("3d  BOTH realizations fail SOMEWHERE in the solar system: MG at l=2 (>1x the Q2 ceiling) and "
    "pure MI at l=0 (>1x the ranging bound).  No realization clears both",
    Q2_MG["canon"] / Q2_CEIL > 1.0 and eph[("canon", "Earth")] > 1.0
    and Q2_MG["alt"] / Q2_CEIL > 1.0 and eph[("alt", "Earth")] > 1.0)
print("\n      And the l=1 EFE residual, for completeness -- with one small correction to STANDING.md.")
print("      In MI the Sun's own inertia is set by its")
print("      near-deep-MOND galactic acceleration, so subtracting the Sun's motion leaves a UNIFORM")
print("      anomalous vector -(nu_ext - 1) g_ext in a fixed Galactic direction:")
unif = {}
for f_ in ("canon", "alt"):
    a0 = A0[f_]
    xx = A_EXT / a0
    mu_e = float(mu_fw(xx))
    nu_e = 1.0 / mu_e
    g_ext = mu_e * A_EXT
    unif[f_] = (nu_e - 1.0) * g_ext
    print(f"        {f_}: mu_fw(a_ext/a_0 = {xx:.4f}) = {mu_e:.4f}, nu_ext = {nu_e:.4f}, "
          f"g_ext = {g_ext:.4e} -> uniform residual = {unif[f_]:.4e} m/s^2 = {unif[f_]/a0:.4f} a_0")
# a uniform force averages to zero radially on a circular orbit -> absorbed as forced eccentricity
th = np.linspace(0, 2 * np.pi, 2000001)
avg_circ = np.trapz(np.cos(th), th) / (2 * np.pi)


def avg_cos_sin_f(e, n=4000001):
    """Orbit-TIME averages of cos f and sin f (dt propto (1 - e cos E) dE)."""
    E = np.linspace(0, 2 * np.pi, n)
    w = 1 - e * np.cos(E)
    cosf = (np.cos(E) - e) / w
    sinf = np.sqrt(1 - e * e) * np.sin(E) / w
    W = np.trapz(w, E)
    return np.trapz(cosf * w, E) / W, np.trapz(sinf * w, E) / W


e_sat = PLANETS["Saturn"][1]
print(f"        orbit-time-average of the radial projection of a FIXED vector:  circular "
      f"{avg_circ:.3e}")
print(f"        {'e':>8s}{'<cos f>_t':>14s}{'-e':>14s}{'ratio':>9s}{'<sin f>_t':>14s}")
ecc_ok = True
for ee in (e_sat, 0.2, 0.5):
    ac, as_ = avg_cos_sin_f(ee)
    ecc_ok &= abs(ac / (-ee) - 1) < 1e-5 and abs(as_) < 1e-9
    print(f"        {ee:>8.4f}{ac:>14.6e}{-ee:>14.6e}{ac/(-ee):>9.5f}{as_:>14.3e}")
chk("3d  the uniform residual is ~0.44 a_0 on both footings, and its orbit-averaged radial projection "
    "is 0 for e = 0 and exactly <cos f>_t = -e otherwise (verified at three eccentricities) -- so it "
    "cannot cancel the sunward a_0/2, exactly as mi_efe_escape_and_ch23_withdrawn_2026.py E1b found",
    abs(avg_circ) < 1e-9 and ecc_ok
    and 0.40 < unif["canon"] / A0["canon"] < 0.50 and 0.40 < unif["alt"] / A0["alt"] < 0.50,
    f"circ {avg_circ:.2e}; <cos f>_t/(-e) = 1.00000 at e = {e_sat}, 0.2, 0.5; "
    f"residual/a_0 = {unif['canon']/A0['canon']:.4f} canon / {unif['alt']/A0['alt']:.4f} alt")

print("\n      BUT THE CORPUS NEVER SIZED THE 'FORCED ECCENTRICITY' IT HANDS THE TERM OFF TO.")
print("      STANDING.md sec 5 item 0 and mi_efe_escape...py E1b both say the fixed-direction term")
print("      'produces a FORCED ECCENTRICITY instead -- which is exactly the piece an ephemeris fit")
print("      absorbs'.  That is asserted, not computed.  Computing it (my own integration, with the")
print("      first-order amplitude 3 pi A a^2 / GM per orbit derived and cross-checked):")


def uniform_secular(a, e, A, ang, N=300):
    """Secular rates from a CONSTANT force A in a FIXED inertial direction (angle ang from the
    initial perihelion).  Returns (d ln a, de, d varpi) per orbit."""
    n = np.sqrt(GM_SUN / a ** 3)
    T = 2 * np.pi / n
    fx, fy = A * np.cos(ang), A * np.sin(ang)

    def rhs(t, y):
        x, yy, vx, vy = y
        r = np.hypot(x, yy)
        return [vx, vy, -GM_SUN * x / r ** 3 + fx, -GM_SUN * yy / r ** 3 + fy]

    rp, vp = a * (1 - e), np.sqrt(GM_SUN * (1 + e) / (a * (1 - e)))
    s = solve_ivp(rhs, [0, N * T], [rp, 0.0, 0.0, vp], rtol=3e-13, atol=1e-6, dense_output=True)
    ts = np.linspace(0, N * T, 60001)
    x, y, vx, vy = s.sol(ts)
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    aa = 1.0 / (2.0 / r - v2 / GM_SUN)
    ex = (v2 / GM_SUN - 1.0 / r) * x - rv * vx / GM_SUN
    ey = (v2 / GM_SUN - 1.0 / r) * y - rv * vy / GM_SUN
    return (np.polyfit(ts, np.log(aa), 1)[0] * T,
            np.polyfit(ts, np.hypot(ex, ey), 1)[0] * T,
            np.polyfit(ts, np.unwrap(np.arctan2(ey, ex)), 1)[0] * T)


print(f"      {'planet':9s}{'amp=3piAa^2/GM':>17s}{'de/orbit num':>15s}{'ratio':>8s}"
      f"{'dvarpi num':>14s}{'ratio':>8s}{'|dvarpi| as/cy':>16s}{'d ln a/orbit':>15s}")
uni_ok = True
uni_cy = {}
A_un = unif["canon"]
for nm in ("Mercury", "Mars", "Saturn"):
    a, e, P = PLANETS[nm]
    amp = 3 * np.pi * A_un * a * a / GM_SUN
    _, de_n, _ = uniform_secular(a, e, A_un, np.pi / 2)
    dlna_n, _, dw_n = uniform_secular(a, e, A_un, 0.0)
    cy = abs(dw_n) * 206264.806 * 100.0 / P
    uni_cy[nm] = cy
    uni_ok &= abs(de_n / amp - 1) < 0.03 and abs(dw_n / (-amp / e) - 1) < 0.03 and abs(dlna_n) < 1e-10
    print(f"      {nm:9s}{amp:>17.4e}{de_n:>15.4e}{de_n/amp:>8.4f}{dw_n:>14.4e}"
          f"{dw_n/(-amp/e):>8.4f}{cy:>16.2f}{dlna_n:>15.2e}")
chk("3d  the forced-eccentricity amplitudes match the first-order closed form 3 pi A a^2/GM (de) and "
    "3 pi A a^2/(GM e) (dvarpi) to 3% at three planets, with NO secular d ln a/dt (< 1e-10/orbit) -- "
    "so this does not touch section 4's Gdot/G channel",
    uni_ok)
chk("3d  FLAGGED, AGAINST INTEREST, AND NEW: the 'absorbed' forced eccentricity is NOT small -- the "
    "apsidal circulation is 4-75 arcsec/century (canonical), i.e. 3-4 orders above any plausible "
    "anomalous-precession budget (~1e-3 as/cy).  The corpus's hand-off was never sized",
    uni_cy["Saturn"] > 10.0 and uni_cy["Mercury"] > 1.0,
    f"Mercury {uni_cy['Mercury']:.2f} / Mars {uni_cy['Mars']:.2f} / Saturn {uni_cy['Saturn']:.2f} as/cy"
    f" ; ALT footing scales by {unif['alt']/unif['canon']:.3f} -> Saturn {uni_cy['Saturn']*unif['alt']/unif['canon']:.1f}")
print(f"""
        *** AND NOW THE BRAKE, because this must NOT be inflated into an exclusion. ***
        Three reasons the {uni_cy['Saturn']:.0f} as/cy is NOT a kill, and I am not treating it as one:
         (i) the prescription I used -- mu_fw(|a_int + a_ext|/a_0) with a naive VECTOR sum -- is NOT
             the framework's committed one.  The committed kernel is A_eff = a_int + theta(y) a_ext
             with theta(y) = theta_0/(1+(theta_0-1)y^2), theta_0 = sqrt(2), theta(1) = 1
             (MI_NONLOCAL_ECCENTRICITY_2026.md sec 1, from DSUNRUH_MI_THEORY_2026.md sec 4).  That
             reweights the static component by an O(1) factor (theta(0) = 1.414 would make this
             LARGER, theta(2) = 0.53 smaller) -- it changes the number, not the order.
        (ii) the covariant MI completion that would FIX the external-field prescription is, by the
             corpus's own standing, UNWRITTEN.  A residual computed from a placeholder EOM is a
             placeholder residual.
       (iii) the perturbation is a COMMON fixed direction for every planet (the bracket
             [1 + a_0/2g_N - nu_ext] varies by < 1e-6 across Mercury->Saturn), so it is partially
             degenerate with the fitted Galactic-field direction and with each planet's own varpi.
             I have not run an ephemeris covariance, and without one no sigma is defensible.
        DISPOSITION: an OPEN, newly-quantified item -- "STANDING.md's forced-eccentricity hand-off is
        unsized, and the first honest estimate is large" -- not a new wall.  It points the same way as
        the l=0 liability: the MI limb's solar-system exposure lives at l=0/l=1, not at l=2.
""")


# =================================================================================================
head("SECTION 4 -- Gdot/G:  the gated condensate's secular drift vs LLR, and the omega_c window")
# =================================================================================================
print(f"""
  The mechanism (corpus, MI_FIELD_THEORY_RESULTS_2026.md sec on the gate).  The exact law's constant
  a_0/2 tail must be suppressed at planetary frequencies.  The unique minimal CAUSAL one-corner object
  is a single-pole Debye relaxator G(omega) = 1/(1 + i omega/omega_c).  Kramers-Kronig then FORCES a
  dissipative partner: the same gate that suppresses the reactive tail (Re G) produces a tangential
  force (|Im G|), hence a secular orbital drift
        d ln r/dt = a_0 omega_c / g_N,
  which an ephemeris/LLR fit reads as an apparent Gdot/G = -d ln a/dt.  omega_c is a FREE FIFTH
  CONSTANT (the action's own corner is a_0/2c ~ 1.6e-19 rad/s, five orders below the window and
  RAR-dead).  Committed window: [{WC_LO:.4e}, {WC_HI['canon']:.4e}] canon / [{WC_LO:.4e}, {WC_HI['alt']:.4e}] alt rad/s.

  The task asks me to VERIFY the consistency rather than assume it, because the window's upper edge
  was FIXED BY this very bound.  That is exactly what makes it worth checking -- and it is also why
  a "pass" here carries no evidential weight.  Both facts are established below.
""")

# --- 4a the varying-G mapping ---------------------------------------------------------------------
print("  4a. The mapping an LLR fit uses: for a slowly varying G with L conserved, L^2 = G M a for a")
print("      circular orbit, so d ln a/dt = -Gdot/G.  Verified by my own integration:")


def dlna_dt_varyingG(gdot_over_G, a0_orb=R_MOON, N=400):
    GM0 = GM_EARTH
    n = np.sqrt(GM0 / a0_orb ** 3)
    T = 2 * np.pi / n

    def rhs(t, y):
        x, yy, vx, vy = y
        r = np.hypot(x, yy)
        gm = GM0 * (1.0 + gdot_over_G * t)
        return [vx, vy, -gm * x / r ** 3, -gm * yy / r ** 3]

    v0 = np.sqrt(GM0 / a0_orb)
    s = solve_ivp(rhs, [0, N * T], [a0_orb, 0.0, 0.0, v0], rtol=3e-13, atol=1e-6, dense_output=True)
    ts = np.linspace(0, N * T, 40001)
    x, y, vx, vy = s.sol(ts)
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    gm = GM0 * (1.0 + gdot_over_G * ts)
    aa = 1.0 / (2.0 / r - v2 / gm)          # osculating semi-major axis
    return np.polyfit(ts, np.log(aa), 1)[0]


gd = 1e-13   # /s: small enough that Gdot*t_span ~ 1e-4, so the LINEAR mapping is what is tested
meas = dlna_dt_varyingG(gd)
print(f"      Gdot/G = {gd:.1e} /s  ->  measured d ln a/dt = {meas:.5e} /s ;  -Gdot/G = {-gd:.5e}")
chk("4a  d ln a/dt = -Gdot/G verified by orbit integration to 0.5%",
    abs(meas / (-gd) - 1) < 5e-3, f"ratio = {meas/(-gd):.6f}")
big = dlna_dt_varyingG(1e-9)
chk("4a  CONTROL (a trap I fell into first): at Gdot/G = 1e-9 /s, G nearly DOUBLES over the span and "
    "the linear fit reads 0.69 instead of 1.00 -- the mapping is linear only in the small-Gdot limit",
    abs(big / (-1e-9) - 1) > 0.2, f"large-Gdot ratio = {big/(-1e-9):.4f}")
chk("4a  CONTROL: with Gdot = 0 the measured drift is < 1e-3 of the signal (integrator noise floor)",
    abs(dlna_dt_varyingG(0.0)) < abs(meas) / 1e3,
    f"noise = {dlna_dt_varyingG(0.0):.3e} /s")

# --- 4b the drift closed form and the LLR calibration ---------------------------------------------
print("\n  4b. The drift at the Moon, at the committed upper edge -- does it reproduce the LLR ceiling?")
gN_moon = GM_EARTH / R_MOON ** 2
ceil_same = abs(LLR_C) + 2 * LLR_S      # expansion has the SAME sign as the LLR central
ceil_opp = LLR_C + 2 * LLR_S            # the opposite-sign ceiling
print(f"      g_N(Moon) = GM_E/R^2 = {gN_moon:.5e} m/s^2 ;  LLR = ({LLR_C:.1e} +/- {LLR_S:.1e})/yr")
print(f"      2 sigma ceilings:  SAME sign as the central |cen|+2sig = {ceil_same:.4e}/yr ;")
print(f"                         OPPOSITE sign      cen+2sig = {ceil_opp:.4e}/yr")
print(f"      {'footing':8s}{'omega_hi [rad/s]':>18s}{'predicted |Gdot/G| /yr':>25s}{'/ ceiling':>12s}")
drift = {}
for f_ in ("canon", "alt"):
    d = A0[f_] * WC_HI[f_] / gN_moon * YR
    drift[f_] = d
    print(f"      {f_:8s}{WC_HI[f_]:>18.4e}{d:>25.5e}{d/ceil_same:>12.5f}")
chk("4b  the committed upper edges reproduce the LLR 2-sigma ceiling 2.420e-14/yr at the Moon to "
    "better than 0.3%, both footings -- the closed form and the edges are mutually consistent",
    all(abs(drift[f_] / ceil_same - 1) < 3e-3 for f_ in ("canon", "alt")),
    f"canon {drift['canon']/ceil_same:.5f}, alt {drift['alt']/ceil_same:.5f}")
chk("4b  CONTROL: moving omega_c by 10% breaks that agreement (so 4b is a real numerical test, not "
    "an identity)",
    abs((A0["canon"] * 1.10 * WC_HI["canon"] / gN_moon * YR) / ceil_same - 1) > 0.05)

# --- 4c the lower edge ----------------------------------------------------------------------------
print("\n  4c. The lower edge, from galactic RAR preservation: Re G(omega_gal) = 1/(1+(om/om_c)^2) >=")
print(f"      {GATE_KEEP:.2f} at the deepest confirmed MOND orbit omega_gal = {OMEGA_GAL_BIND:.3e} rad/s")
print("      (UGC05721 innermost, committed) => om_c >= om_gal sqrt(keep/(1-keep)) = 3 om_gal.")
wc_lo_derived = OMEGA_GAL_BIND * np.sqrt(GATE_KEEP / (1.0 - GATE_KEEP))
ReG = lambda om, wc: 1.0 / (1.0 + (om / wc) ** 2)
print(f"      derived om_lo = {wc_lo_derived:.5e} rad/s ;  committed {WC_LO:.5e} ;  "
      f"Re G at that corner = {ReG(OMEGA_GAL_BIND, wc_lo_derived):.6f}")
chk("4c  the committed lower edge 1.7824e-14 is exactly 3 x omega_gal, i.e. Re G = 0.900 -- "
    "reproduced to 0.1%",
    abs(wc_lo_derived / WC_LO - 1) < 1e-3 and abs(ReG(OMEGA_GAL_BIND, wc_lo_derived) - 0.90) < 1e-9,
    f"derived/committed = {wc_lo_derived/WC_LO:.6f}")
print("\n      FOOTING FORK on the lower edge -- run both ways, per the standing rule.  The in-force")
print("      edge uses a KINEMATIC omega_gal = V/r (UGC05721 innermost: V = 16.5 km/s, r = 0.09 kpc),")
print("      which carries no a_0.  WINDOW.md instead used omega_gal = y a_0/v (y = 0.8, v = 25 km/s),")
print("      which DOES carry a_0.  The two give different edges and different window widths:")
om_kin = 16.5e3 / (0.09 * KPC)
print(f"      {'lower-edge definition':34s}{'om_lo canon':>15s}{'om_lo alt':>13s}"
      f"{'width canon':>13s}{'width alt':>11s}")
lo_kin = om_kin * np.sqrt(GATE_KEEP / (1 - GATE_KEEP))
print(f"      {'kinematic V/r (in force)':34s}{lo_kin:>15.4e}{lo_kin:>13.4e}"
      f"{WC_HI['canon']/lo_kin:>13.4f}{WC_HI['alt']/lo_kin:>11.4f}")
lo_yv = {f_: 0.8 * A0[f_] / 25e3 * np.sqrt(GATE_KEEP / (1 - GATE_KEEP)) for f_ in ("canon", "alt")}
print(f"      {'WINDOW.md y a_0/v (a_0-dependent)':34s}{lo_yv['canon']:>15.4e}{lo_yv['alt']:>13.4e}"
      f"{WC_HI['canon']/lo_yv['canon']:>13.4f}{WC_HI['alt']/lo_yv['alt']:>11.4f}")
chk("4c  the kinematic lower edge reproduces omega_gal = 5.94e-15 from V/r to 0.1%, so the in-force "
    "edge is genuinely footing-independent -- computed, not asserted",
    abs(om_kin / OMEGA_GAL_BIND - 1) < 1e-3, f"V/r = {om_kin:.4e} vs committed {OMEGA_GAL_BIND:.4e}")
chk("4c  FORK: WINDOW.md's a_0-dependent lower edge reproduces its published widths x2.46 (canon) / "
    "x1.69 (alt) to 1%, and is 2.0x / 1.6x LOOSER than the in-force edge -- the window width is a "
    "footing-and-definition choice, spread x1.03 to x2.46",
    abs(WC_HI["canon"] / lo_yv["canon"] / 2.46 - 1) < 0.01
    and abs(WC_HI["alt"] / lo_yv["alt"] / 1.69 - 1) < 0.01
    and lo_kin / lo_yv["canon"] > 1.5,
    f"widths {WC_HI['canon']/lo_yv['canon']:.3f} / {WC_HI['alt']/lo_yv['alt']:.3f}; "
    f"edge ratio {lo_kin/lo_yv['canon']:.3f} canon, {lo_kin/lo_yv['alt']:.3f} alt")

# --- 4d window widths -----------------------------------------------------------------------------
print("\n  4d. Window widths on the committed edges:")
wid = {f_: WC_HI[f_] / WC_LO for f_ in ("canon", "alt")}
for f_ in ("canon", "alt"):
    print(f"      {f_}: [{WC_LO:.4e}, {WC_HI[f_]:.4e}] rad/s  ->  width x{wid[f_]:.4f}  "
          f"(tau = {1/WC_HI[f_]/YR/1e6:.2f}-{1/WC_LO/YR/1e6:.2f} Myr)")
chk("4d  BLUNT: the ALT footing's window is only x1.03 wide -- a 2.7% sliver, i.e. effectively a "
    "single tuned point, not an interval",
    wid["alt"] < 1.05, f"alt width = x{wid['alt']:.4f}")
chk("4d  the canonical window is wider but still narrow (x1.24)",
    1.10 < wid["canon"] < 1.40, f"canon width = x{wid['canon']:.4f}")

# --- 4e the sign the window is hostage to ---------------------------------------------------------
print("\n  4e. The window's EXISTENCE is hostage to a sign.  The retarded filter makes the anomalous")
print("      attraction LAG; on a circulating orbit a lagged attraction has a PROGRADE tangential")
print("      component, so on the framework's own branch (sigma = +1 = extra pull = the sign MEASURED")
print("      in galaxies = the s = -1 posit) the orbit EXPANDS -> apparent Gdot/G NEGATIVE -> SAME")
print("      sign as the LLR central.  If sigma = -1 the correct ceiling is cen + 2 sigma:")
wc_hi_opp = {f_: ceil_opp / YR * gN_moon / A0[f_] for f_ in ("canon", "alt")}
for f_ in ("canon", "alt"):
    print(f"      {f_}: opposite-sign om_hi = {wc_hi_opp[f_]:.4e} rad/s  vs om_lo = {WC_LO:.4e}  ->  "
          f"{'EMPTY' if wc_hi_opp[f_] < WC_LO else 'non-empty'}")
chk("4e  under the opposite drift sign the window is EMPTY on BOTH footings -- so a non-empty window "
    "is conditional on a sign that galaxies fix but causality does not",
    all(wc_hi_opp[f_] < WC_LO for f_ in ("canon", "alt")),
    f"canon {wc_hi_opp['canon']:.3e} < {WC_LO:.3e} ; alt {wc_hi_opp['alt']:.3e}")

# --- 4f is LLR really the binding bound? ----------------------------------------------------------
print("\n  4f. Is LLR really the binding bound?  The drift scales as 1/g_N, so OUTER bodies drift")
print("      fractionally FASTER.  Absolute drift dr/dt = a_0 omega_c r^3/GM grows as r^3:")
print(f"      {'body':10s}{'g_N [m/s^2]':>14s}{'d ln r/dt /yr':>16s}{'dr/dt [m/yr]':>15s}"
      f"{'om_c ceiling':>15s}")
wc_ceil = {}
for nm, (a, e, P) in list(PLANETS.items()) + [("Moon", (R_MOON, 0.0549, 27.32 / 365.25))]:
    gm = GM_EARTH if nm == "Moon" else GM_SUN
    gN = gm / a ** 2
    dl = A0["canon"] * WC_HI["canon"] / gN * YR
    print(f"      {nm:10s}{gN:>14.4e}{dl:>16.4e}{dl*a:>15.4e}", end="")
    if nm == "Moon":
        wc_ceil[nm] = ceil_same / YR * gN / A0["canon"]
        print(f"{wc_ceil[nm]:>15.4e}   <- LLR Gdot/G")
    elif nm == "Saturn":
        # corpus 'Saturn proxy' ceiling 3.5e-14 rad/s <-> a fractional-a allowance of:
        allow = 3.5e-14 * A0["canon"] / gN * YR
        wc_ceil[nm] = 3.5e-14
        print(f"{wc_ceil[nm]:>15.4e}   <- corpus proxy (= {allow*a:.2f} m/yr allowance)")
    else:
        print("")
chk("4f  LLR does bind, but only by x1.6 over the corpus's own Saturn proxy -- the upper edge is not "
    "comfortable, and the SAME corner puts ~1.5 m/yr of secular drift into Saturn's orbit",
    1.0 < wc_ceil["Saturn"] / wc_ceil["Moon"] < 2.0,
    f"Saturn/Moon ceiling ratio = {wc_ceil['Saturn']/wc_ceil['Moon']:.3f}; Saturn drift = "
    f"{A0['canon']*WC_HI['canon']/(GM_SUN/R_SAT**2)*YR*R_SAT:.2f} m/yr")

# --- 4g calibration, not prediction ---------------------------------------------------------------
print("\n  4g. THE EVIDENTIAL WEIGHT OF THIS PASS.  The upper edge was DEFINED as the omega_c at which")
print("      the predicted drift equals the LLR 2-sigma ceiling.  So at the edge the prediction equals")
print("      the bound to machine precision by construction -- there is no residual to be surprised by:")
for f_ in ("canon", "alt"):
    print(f"      {f_}: predicted/ceiling = {drift[f_]/ceil_same:.6f}")
chk("4g  the prediction/bound ratio at the upper edge is 1.000 +/- 0.003 by CONSTRUCTION on both "
    "footings => 'the framework passes Gdot/G' is CALIBRATION, not a prediction, and carries zero "
    "evidential weight for the framework over GR",
    all(abs(drift[f_] / ceil_same - 1) < 3e-3 for f_ in ("canon", "alt")))
print("      Also: at planetary and lunar accelerations GR predicts zero drift and healthy")
print("      MOND-family theories predict ~zero.  Nothing in section 4 discriminates the framework")
print("      against LambdaCDM.  What section 4 DOES do is price the fifth constant.")


# =================================================================================================
head("SECTION 5 -- PASS / FAIL TABLE WITH MARGINS")
# =================================================================================================
rows = [
    ("1. GW170817 tensor speed c_T (graviton only)", "PASS (exact)",
     f"|c_T-1| <= {worst*CT_BOUND:.1e} vs {CT_BOUND:.0e}  ->  margin ~{1/max(worst,1e-99):.0e}x",
     "structural: G4X=G5=0, c1=c3=0, P(X) blind to h^TT; only the rho_m-weighted MI term is nonzero"),
    ("1e. GW170817 MULTI-MESSENGER timing (photon)", "*** FAIL ***",
     f"Dt = {gwres['canon'][2]:.1e} s (canon) / {gwres['alt'][2]:.1e} s (alt) vs 1.74 s  ->  "
     f"over by {gwres['canon'][2]/1.74:.1e}x",
     "the disformal photon cone; kills the disformal route to DM-free lensing, not the RAR/BTFR"),
    ("2. PPN gamma (Cassini, real ray geometry)", "PASS",
     f"gamma-1 = {gam['canon'][0]:.1e} / {gam['alt'][0]:.1e} vs ceiling {GAM_CEIL:.1e}  ->  "
     f"margin {GAM_CEIL/gam['canon'][0]:.0e}x",
     "MOND-SHARED: full spread over every a_0 on the menu is 1e-5 of the ceiling -> zero evidence"),
    ("2. PPN beta (LLR Nordtvedt)", "PASS (vacuously)",
     f"beta-1 = 0 exactly vs |beta-1| <= {(abs(ETA_N_C)+2*ETA_N_S)/4:.1e}",
     "metric is Schwarzschild; but PPN assumes GEODESIC motion, which MI breaks -> the pass is empty"),
    ("2c. Ephemeris l=0 anomaly (beta channel's real content)", "*** FAIL ***",
     f"a_0/2 = {A0['canon']/2:.2e} m/s^2 vs Earth 2sig {DAR_EARTH:.2e}  ->  over by "
     f"{eph[('canon','Earth')]:.0f}x (canon) / {eph[('alt','Earth')]:.0f}x (alt)",
     "alpha=1 only; alpha=2 relieves 3.35 orders to 6.2-8.5x / 9.0-12.4x -- still a FAIL"),
    ("3. Cassini Q2 -- MG (AeST) realization", "*** FAIL ***",
     f"Q2 = {Q2_MG['canon']:.2e} / {Q2_MG['alt']:.2e} s^-2 vs ceiling {Q2_CEIL:.1e}  ->  "
     f"{(Q2_MG['canon']-Q2_C)/Q2_S:.0f}-{(Q2_MG['alt']-Q2_C)/Q2_S:.0f} sigma",
     "phantom density from the nonlinear Poisson operator; corpus D4 band 1.2-2.0e-26 reproduced-and-exceeded"),
    ("3. Cassini Q2 -- pure MI realization", "PASS (evades)",
     f"Q2 = {Q2_MI['canon']:.2e} / {Q2_MI['alt']:.2e} s^-2  ->  margin "
     f"{Q2_CEIL/Q2_MI['canon']:.0e}x ; MG/MI = {Q2_MG['canon']/Q2_MI['canon']:.1e}",
     "no phantom density; the EFE enters only at eps^2 = (a_ext/g_N)^2.  A REAL internal discriminator"),
    ("3d. MI l=1 uniform EFE residual (forced eccentr.)", "OPEN -- newly sized",
     f"apsidal circulation {uni_cy['Mercury']:.0f}-{uni_cy['Saturn']:.0f} as/cy (canon), x"
     f"{unif['alt']/unif['canon']:.2f} alt, vs a ~1e-3 as/cy budget; NO secular d ln a/dt",
     "the corpus asserts 'an ephemeris fit absorbs it' and never sized it; my number is large but "
     "rests on a NAIVE vector EOM, not the committed theta(y) kernel -> flagged, NOT an exclusion"),
    ("4. Gdot/G (LLR) at the committed omega_c upper edge", "PASS (by calibration)",
     f"|Gdot/G| = {drift['canon']:.3e} / {drift['alt']:.3e} /yr vs ceiling {ceil_same:.3e}  ->  "
     f"ratio 1.000",
     f"window x{wid['canon']:.2f} canon / x{wid['alt']:.2f} alt on the in-force (kinematic) lower "
     f"edge, x{WC_HI['canon']/lo_yv['canon']:.2f}/x{WC_HI['alt']/lo_yv['alt']:.2f} on WINDOW.md's; "
     f"EMPTY under the opposite drift sign; omega_c is a FREE 5th constant"),
]
print(f"\n  {'constraint':52s}{'verdict':18s}{'margin':>1s}")
print("  " + "-" * 100)
for name, verdict, margin, note in rows:
    print(f"  {name:52s}{verdict:18s}")
    print(f"      margin : {margin}")
    print(f"      note   : {note}")
print(f"""
  {'-'*100}
  HOW MANY FAILURES.  Three, and they are not cosmetic:
    (i)   GW170817 multi-messenger timing, ~7 orders, both footings -- the framework's OWN disformal
          photon sector.  "c_T = 1 exactly" is true and is not a pass.
    (ii)  the inner-planet ephemerides, {eph[('canon','Earth')]:.0f}x / {eph[('alt','Earth')]:.0f}x on alpha=1 (the EXACT law);
          the alpha=2 mutation buys 3.35 orders and still fails at 6-12x on the Sun's reflex.
    (iii) the Cassini Q2 quadrupole, 11-13 sigma, for the MG/AeST realization -- which is the
          framework's only WRITTEN CMB-safe covariant limb.
  Plus ONE new OPEN item, reported because a gauntlet that only re-runs known items is not a gauntlet:
    (iv)  the l=1 uniform EFE residual's "forced eccentricity" was asserted-absorbed and never sized.
          Sized here at {uni_cy['Mercury']:.0f}-{uni_cy['Saturn']:.0f} as/cy of apsidal circulation.  It rests on a NAIVE vector EOM,
          not the committed theta(y) kernel, so it is FLAGGED, not an exclusion.
  And ONE corpus liability WITHDRAWN, checked as hard as any win:
    (v)   the disformal "second bill" (B varies by 257, "~2 orders over its own premise B < 1") is a
          c^2 units slip -- the dimensionless B across the solar system is {max(dB_dimless.values()):.1e}.  This does NOT
          rescue alpha = 1; the {eph[('canon','Earth')]:.0f}x ephemeris wall is untouched.

  WHAT SURVIVES, stated no more strongly than it deserves.  The tensor sector is clean by structure
  and not by tuning.  PPN gamma and beta pass but are worthless as evidence: gamma is MOND-shared to
  1e-5 of the ceiling and beta is vacuous because MI is not a metric theory of geodesic motion.  The
  ONE genuinely informative result is section 3: at fixed a_0 and fixed nu, the MG realization is
  11-13 sigma over the Cassini quadrupole while the pure-MI realization evades it by 1e7 -- a real,
  computed, internal discriminator, and it points at MI.  But MI buys that evasion with the l=0
  constant a_0/2, so the solar-system wall MOVES from l=2 to l=0 rather than disappearing.  No
  realization on the table clears both.  Nothing here bears on the RAR, the BTFR, the a_0-line, the
  a_0 = kappa c sqrt(G rho_Lambda) reframing (kappa = 1/2 FITTED), or the spherical dynamics.  Doors
  remain open: the alpha=2 Sun-reflex margin, a non-disformal lensing sector, and the still-unwritten
  covariant MI completion that would have to reproduce section 3b's suppression.
""")

print(RULE)
print(f"{_OK}/{_N} checks held.")
if _FAILED:
    print("FAILED:")
    for nm in _FAILED:
        print(f"  - {nm}")
print(RULE)
sys.exit(0 if not _FAILED else 1)
