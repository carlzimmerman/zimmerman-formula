#!/usr/bin/env python3
"""
A75 -- CAN THE THERMAL PREMISE a0 = cH_Lambda/(2 pi) BE DERIVED FROM THE ACTION?

The premise under test (A72, C5): a carrier of mass m with Compton length
l = hbar/(m c), in equilibrium at the Gibbons-Hawking temperature
T_dS = hbar H_L/(2 pi k_B), saturates at  a_sat = k_B T_dS/(m l) = cH_L/(2 pi).

What this script does (every check = two independent computations + a comparison):

  PART 1 (K1-K7)   thermodynamics of the Langmuir gate: Omega, theta, F, S, C,
                   d theta/dT at fixed g and at fixed mu.  Is the gate
                   temperature-blind, and can a blind gate produce a thermal
                   wavelength condition?
  PART 2 (K8-K13)  the action's own carrier: m_T^2 = K/eta, L* = sqrt(2 gamma/K),
                   lambda_C = sqrt(eta/K) = L*/sqrt(2) (eta = gamma).  Does the
                   literal condition lambda_C = lambda_T hold?  What does A72's
                   formula actually use?
  PART 3 (K14-K19) three alternative routes: k^4 thermal energy density at T_dS,
                   horizon entropy per cell, gate chemical potential at T_dS,
                   per-site capacity.
  PART 4 (K20-K23) the free-parameter ledger: R = 1/kappa^2, the closure, the
                   homogeneity of the law, the 2 pi conventions.

Mutations: A75_MUTATE=<name> (or --mutate <name>).  Each changes ONE input and
must make at least one named check FAIL (exit 1).  See MUTATE.md.

Deterministic, no network, stdlib + sympy + mpmath.
"""

import os
import sys
import json
import math

import sympy as sp
import mpmath as mp

mp.mp.dps = 30

# ===========================================================================
# constants (BRIEF section 4 + CODATA)
# ===========================================================================
c      = 2.99792458e8
G      = 6.67430e-11
H0     = 2.1843e-18
LAM    = 1.0890e-52
HBAR   = 1.054571817e-34
KB     = 1.380649e-23
PC     = 3.0856775814913673e16
MPC    = PC * 1e6
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10

H_L      = c * math.sqrt(LAM / 3.0)            # de Sitter expansion rate, s^-1
CH_L     = c * H_L
T_DS     = HBAR * H_L / (2.0 * math.pi * KB)   # Gibbons-Hawking temperature, K
A0_TH    = CH_L / (2.0 * math.pi)              # the thermal value, m/s^2
RHO_L    = LAM * c * c / (8.0 * math.pi * G)
Z_CLOS   = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
A0_CLOS  = c * c * math.sqrt(LAM / (32.0 * math.pi))   # kappa = 1/2 closure
KAPPA_TH = A0_TH / (c * math.sqrt(G * RHO_L))
L_P      = math.sqrt(HBAR * G / c ** 3)
A_PLANCK = c * c / L_P
L_STAR   = 24.025012 * PC                       # A65 (external input, 24 pc fit)
BETA     = 1.0                                  # A68 dialled value

# ===========================================================================
# mutations: each is a ONE-INPUT change of the live parameter set
# ===========================================================================
MUTATIONS = {
    "occupancy":     {"occupancy": "boltzmann"},   # drop the site exclusion: theta = z
    "drive_energy":  {"drive": "energy"},          # drive enters as energy z=e^{g/kT}, not activity
    "fermi_nocouple": {"fermi_lambda": 0.0},       # the two-level gate decoupled
    "twopi_drop":    {"twopi": 1.0},               # lambda_T = c/H instead of 2 pi c/H
    "temp_H0":       {"temp_hubble": "H0"},        # T uses H0 instead of H_Lambda
    "eta_three":     {"eta_over_gamma": 3.0},      # eta = 3 gamma
    "disp_linear":   {"dispersion": "linear"},     # omega = p instead of alpha p^4/Q
    "entropy_norm":  {"entropy_quarter": 2.0},     # S = A/(2 l_P^2)
    "mu_eps":        {"epsilon_over_kT": -1.0},    # binding energy tuned to -k_B T_dS
    "cell_one":      {"n_cells": 1.0},             # one gate for the whole horizon
    "kappa_half":    {"a0_mode": "closure"},       # force a0 = c^2 sqrt(Lambda/32 pi)
    "law_const":     {"law_const": 1e-12},         # additive fixed acceleration in the law
    "mP_offby2":     {"mP_factor": 2.0},           # carrier mass doubled
    "a0_slope_sign": {"a0_slope_sign": -1.0},      # d a0/dT has the other sign
    "premise_true":  {"lambda_T_mode": "compton"}, # assume lambda_T = lambda_C (the premise itself)
    "mP_tiny":       {"mP_factor": 1e-10},         # a carrier light enough to be thermally populated
}

PARAMS = {
    "occupancy": "langmuir",
    "drive": "activity",
    "fermi_lambda": 1.0,
    "twopi": 2.0 * math.pi,
    "temp_hubble": "dS",
    "eta_over_gamma": 1.0,
    "dispersion": "k4",
    "entropy_quarter": 4.0,
    "epsilon_over_kT": 0.0,
    "n_cells": None,
    "a0_mode": "thermal",
    "law_const": 0.0,
    "mP_factor": 1.0,
    "a0_slope_sign": 1.0,
    "lambda_T_mode": "thermal",
}

MUT_NAME = os.environ.get("A75_MUTATE")
_argv = sys.argv[1:]
if "--mutate" in _argv:
    MUT_NAME = _argv[_argv.index("--mutate") + 1]
if MUT_NAME:
    if MUT_NAME not in MUTATIONS:
        print("unknown mutation %r; known: %s" % (MUT_NAME, ", ".join(sorted(MUTATIONS))))
        sys.exit(2)
    PARAMS.update(MUTATIONS[MUT_NAME])

OCC        = PARAMS["occupancy"]
DRIVE      = PARAMS["drive"]
FERMI_LAM  = PARAMS["fermi_lambda"]
TWOPI      = PARAMS["twopi"]
ETA_OVER_G = PARAMS["eta_over_gamma"]
DISP       = PARAMS["dispersion"]
S_QUARTER  = PARAMS["entropy_quarter"]
EPS_KT     = PARAMS["epsilon_over_kT"]
A0_MODE    = PARAMS["a0_mode"]
LAW_CONST  = PARAMS["law_const"]
MP_FACTOR  = PARAMS["mP_factor"]

T_DS_LIVE = (HBAR * H0 / (2.0 * math.pi * KB)) if PARAMS["temp_hubble"] == "H0" else T_DS
A0_LIVE   = A0_CLOS if A0_MODE == "closure" else A0_TH

# derived lengths / masses (natural units: lambda_C = 1/m)
LAM_C    = L_STAR / math.sqrt(2.0) * math.sqrt(ETA_OVER_G)   # sqrt(eta/K), eta = g*gamma
M_P      = HBAR / (c * LAM_C) * MP_FACTOR                    # kg
LAM_T    = (LAM_C if PARAMS["lambda_T_mode"] == "compton"
            else TWOPI * c / H_L)                            # m; "compton" asserts the premise
N_CELLS  = (4.0 * math.pi * (c / H_L) ** 2 / L_STAR ** 2
            if PARAMS["n_cells"] is None else PARAMS["n_cells"])

CHECKS = []
NUMBERS = {}


def sres(expr):
    """Symbolic residual, with every hyperbolic/exp form put in one basis."""
    return sp.simplify(sp.expand(expr.rewrite(sp.exp)))


def rel(a, b):
    a, b = float(a), float(b)
    if b == 0.0:
        return abs(a)
    return abs(a - b) / abs(b)


def record(cid, ok, measured, threshold, note):
    CHECKS.append({"id": cid, "pass": bool(ok), "value": measured,
                   "threshold": threshold, "note": note})
    print("%-5s %s  %s  [%s]  %s"
          % (cid, "PASS" if ok else "FAIL", measured, threshold, note))


def run(cid, fn, threshold, note):
    """Every check is a pair of independent computations; fn returns (ok, measured)."""
    try:
        ok, measured = fn()
    except Exception as exc:                      # a mutation may make a route singular
        ok, measured = False, "EXC:%s" % type(exc).__name__
    record(cid, ok, measured, threshold, note)


# ===========================================================================
# PART 1 -- THE GATE'S THERMODYNAMICS
# ===========================================================================
kB, T, mu, eps, g, a0 = sp.symbols("k_B T mu epsilon g a0", positive=True)
z = sp.exp((mu + eps) / (kB * T))
OMEGA = -kB * T * sp.log(1 + z)
theta_gc = sp.simplify(-sp.diff(OMEGA, mu))          # = z/(1+z), exact


def theta_model(zv):
    """The occupancy the *model* asserts, given the activity z."""
    return zv if OCC == "boltzmann" else zv / (1.0 + zv)


def theta_drive(gv, a0v, kBT):
    """Occupancy as a function of the drive g."""
    if DRIVE == "energy":
        zv = mp.e ** (gv / kBT)
    else:
        zv = gv / a0v
    return theta_model(zv)


def k1():
    """theta = -dOmega/dmu (finite difference of the partition function) vs z/(1+z)."""
    sym_res = sres(theta_gc - z / (1 + z))
    muv, epsv, kBv, Tv = mp.mpf("0.37"), mp.mpf("-0.11"), mp.mpf("1.7"), mp.mpf("0.83")
    h = mp.mpf("1e-15")

    def Om(m):
        return -kBv * Tv * mp.log(1 + mp.e ** ((m + epsv) / (kBv * Tv)))

    dOm = -(Om(muv + h) - Om(muv - h)) / (2 * h)      # theta = -dOmega/dmu
    model = theta_model(mp.e ** ((muv + epsv) / (kBv * Tv)))
    r_num = abs(dOm - model) / abs(model)
    ok = (sym_res == 0) and (r_num < mp.mpf("1e-12"))     # finite-difference floor ~1e-15
    NUMBERS["K1_r_num"] = float(r_num)
    return ok, "sym 0; num rel %.2e" % float(r_num)


def k2():
    """The activity map mu = k_B T ln(g/a0) - eps gives theta = g/(g+a0) exactly."""
    sub = sp.simplify(theta_gc.subs(mu, kB * T * sp.log(g / a0) - eps))
    sym_res = sp.simplify(sub - g / (g + a0))
    kBT = mp.mpf("2.3e-4")
    a0v = mp.mpf(str(A0_TH))
    gv = mp.mpf("0.37") * a0v
    th = theta_drive(gv, a0v, kBT)
    target = gv / (gv + a0v)
    r = abs(th - target) / target
    ok = (sym_res == 0) and (r < mp.mpf("1e-20"))
    NUMBERS["K2_theta_at_037"] = float(th)
    return ok, "sym 0; num rel %.2e" % float(r)


def k3():
    """d theta/dT at fixed g: zero for the activity gate, nonzero for an energetic drive."""
    kBT = mp.mpf("2.3e-4")
    a0v = mp.mpf(str(A0_TH))
    gv = mp.mpf("0.37") * a0v
    dT = mp.mpf("1e-10")
    fd = (theta_drive(gv, a0v, kBT * (1 + dT)) - theta_drive(gv, a0v, kBT * (1 - dT))) \
        / (2 * dT * kBT)
    if DRIVE == "energy":
        th = theta_drive(gv, a0v, kBT)
        analytic = -th * (1 - th) * gv / kBT ** 2       # z = e^{g/kT}: theta falls with T
    else:
        analytic = mp.mpf(0)
    r = abs(fd - analytic) / (abs(analytic) if analytic != 0 else mp.mpf(1))
    ok = (r < mp.mpf("1e-6")) and (abs(analytic) < mp.mpf("1e-40"))
    NUMBERS["K3_dtheta_dT_fixed_g"] = float(analytic)
    return ok, "fd %.2e; analytic %.2e per K" % (float(fd), float(analytic))


def k3b():
    """With an affinity a0(T) the gate is T-dependent: d theta/dT = -g a0'(T)/(g+a0)^2.
       Thermal blindness <=> a0'(T) = 0 <=> a0 is a constant of the action."""
    a0f = sp.Function("a0")(T)
    th = g / (g + a0f)
    d = sp.simplify(sp.diff(th, T))
    target = -g * sp.diff(a0f, T) / (g + a0f) ** 2
    sym_res = sp.simplify(d - target)
    # numeric: a0(T) = a0 (1 + alpha (T-T0)), alpha = 3.1e-3 / K
    alpha_decl = mp.mpf("3.1e-3")                  # the declared slope used by the analytic route
    alpha = alpha_decl * mp.mpf(str(PARAMS["a0_slope_sign"]))
    a0v, T0 = mp.mpf("8.618165899975415e-11"), mp.mpf("300")
    Tv = mp.mpf("301.7")
    gv = mp.mpf("0.37") * a0v

    def thT(t):
        av = a0v * (1 + alpha * (t - T0))
        return gv / (gv + av)

    h = mp.mpf("1e-6")
    fd = (thT(Tv + h) - thT(Tv - h)) / (2 * h)
    analytic = -gv * (a0v * alpha_decl) / (gv + a0v * (1 + alpha * (Tv - T0))) ** 2
    r = abs(fd - analytic) / abs(analytic)
    ok = (sym_res == 0) and (r < mp.mpf("1e-6"))
    NUMBERS["K3b_dtheta_dT_a0T"] = float(analytic)
    return ok, "sym 0; fd/analytic rel %.2e" % float(r)


def k4():
    """d theta/dT at fixed mu = -theta(1-theta)(mu+eps)/(k_B T^2), nonzero."""
    d_sym = sp.diff(z / (1 + z), T)
    target = -(z / (1 + z)) * (1 - z / (1 + z)) * (mu + eps) / (kB * T ** 2)
    sym_res = sres(d_sym - target)
    kBv, Tv, muv, epsv = mp.mpf("1.7"), mp.mpf("0.83"), mp.mpf("0.37"), mp.mpf("-0.11")

    def th(t):
        zv = mp.e ** ((muv + epsv) / (kBv * t))
        return theta_model(zv)

    h = mp.mpf("1e-8") * Tv
    fd = (th(Tv + h) - th(Tv - h)) / (2 * h)
    zv = mp.e ** ((muv + epsv) / (kBv * Tv))
    thv = theta_model(zv)
    # the Langmuir closed form, fixed: the mutation must not be allowed to rewrite it
    analytic = -thv * (1 - thv) * (muv + epsv) / (kBv * Tv ** 2)
    r = abs(fd - analytic) / abs(analytic)
    ok = (sym_res == 0) and (r < mp.mpf("1e-6")) and (abs(analytic) > mp.mpf("1e-6"))
    NUMBERS["K4_dtheta_dT_fixed_mu"] = float(analytic)
    return ok, "sym 0; fd/analytic rel %.2e; value %.4f" % (float(r), float(analytic))


def k5():
    """S = -dOmega/dT|_mu = k_B[ln(1+z) - theta ln z];  F = Omega + mu theta = U - T S + mu theta."""
    S_sym = sp.simplify(-sp.diff(OMEGA, T) - kB * (sp.log(1 + z) - theta_gc * sp.log(z)))
    kBv, Tv, muv, epsv = mp.mpf("1.7"), mp.mpf("0.83"), mp.mpf("0.37"), mp.mpf("-0.11")
    zv = mp.e ** ((muv + epsv) / (kBv * Tv))
    thv = theta_model(zv)
    S_closed = kBv * (mp.log(1 + zv) - thv * mp.log(zv))
    U = -epsv * thv
    F_id = U - Tv * S_closed                 # F = U - T S  (Omega = U - T S - mu N)
    F_closed = kBv * Tv * (thv * mp.log(thv) + (1 - thv) * mp.log(1 - thv)) - epsv * thv
    U_sym = -eps * theta_gc
    F_sym_route = (OMEGA + mu * theta_gc) - (U_sym - T * (kB * (sp.log(1 + z) - theta_gc * sp.log(z))))
    F_sym = sres(F_sym_route)
    r = abs(F_id - F_closed) / abs(F_closed)
    ok = (S_sym == 0) and (F_sym == 0) and (r < mp.mpf("1e-20"))
    NUMBERS["K5_entropy_per_site"] = float(S_closed)
    return ok, "sym 0/0; F identity rel %.2e" % float(r)


def k6():
    """C_mu = dU/dT|_mu = T dS/dT|_mu + mu dtheta/dT|_mu, and C_g = 0 at fixed drive."""
    kBv, Tv, muv, epsv = mp.mpf("1.7"), mp.mpf("0.83"), mp.mpf("0.37"), mp.mpf("-0.11")
    h = mp.mpf("1e-8") * Tv

    def th(t):
        return theta_model(mp.e ** ((muv + epsv) / (kBv * t)))

    C_fd = (-epsv) * (th(Tv + h) - th(Tv - h)) / (2 * h)
    zv = mp.e ** ((muv + epsv) / (kBv * Tv))
    thv = theta_model(zv)
    lnz = mp.log(zv)
    # the Langmuir closed forms, fixed
    C_route = kBv * thv * (1 - thv) * lnz ** 2 + muv * (-thv * (1 - thv) * lnz / Tv)
    r = abs(C_fd - C_route) / abs(C_route)
    # fixed drive: theta = g/(g+a0) is T-independent => C_g = 0
    a0v = mp.mpf(str(A0_TH))
    gv = mp.mpf("0.37") * a0v
    Cg_fd = (theta_drive(gv, a0v, Tv + h) - theta_drive(gv, a0v, Tv - h)) / (2 * h)
    ok = (r < mp.mpf("1e-6")) and (abs(C_fd) > mp.mpf("1e-6")) and (abs(Cg_fd) < mp.mpf("1e-30"))
    NUMBERS["K6_C_mu"] = float(C_fd)
    NUMBERS["K6_C_g"] = float(Cg_fd)
    return ok, "C_mu %.4f K_B; C_g %.1e" % (float(C_fd) / float(KB), float(Cg_fd))


def k7():
    """The only T-sensitive gate is the two-level (energetic) one, and it has A(0) = C/2."""
    lam = mp.mpf(str(FERMI_LAM))
    kBTv, Tv = mp.mpf("1.0"), mp.mpf("1.0")

    def thF(gv, t):
        return 1 / (1 + mp.e ** (-lam * gv / t))

    th0 = thF(mp.mpf("1e-12"), Tv)          # the g -> 0 limit
    h = mp.mpf("1e-6")
    dF = (thF(mp.mpf("1.0"), Tv * (1 + h)) - thF(mp.mpf("1.0"), Tv * (1 - h))) / (2 * h * Tv)
    analytic = -thF(mp.mpf("1.0"), Tv) * (1 - thF(mp.mpf("1.0"), Tv)) * lam * mp.mpf("1.0") / Tv ** 2
    ok = (abs(th0 - 0.5) < mp.mpf("1e-12")) and (abs(dF - analytic) < mp.mpf("1e-9")) \
        and (abs(analytic) > mp.mpf("1e-6"))
    NUMBERS["K7_fermi_A0_over_C"] = float(th0)
    return ok, "theta_F(0)=%.6f; dtheta/dT=%.4f" % (float(th0), float(analytic))


# ===========================================================================
# PART 2 -- THE CARRIER INSIDE THE ACTION
# ===========================================================================
M_P_A56 = 6.7105e-61     # A56/A65: hbar/(c L*/sqrt2) at L* = 24.025 pc, an external input


def k8():
    """lambda_C(live eta/gamma) = L*/sqrt(2) requires eta = gamma; cross-check vs the A56 mass."""
    eta, gam, K = sp.symbols("eta gamma K", positive=True)
    Ls = sp.sqrt(2 * gam / K)
    lam = sp.sqrt(eta / K)
    sym_res = sres(lam.subs(eta, gam) - Ls / sp.sqrt(2))
    lc = LAM_C                                    # live: sqrt(eta/K), eta = (eta/gamma) gamma
    lc_a56 = HBAR / (M_P_A56 * c)                 # independent route: the quoted A56 P mass
    r = abs(lc - lc_a56) / lc_a56
    ok = (sym_res == 0) and (r < 1e-4)
    NUMBERS["K8_lambda_C_pc"] = lc / PC
    NUMBERS["K8_lambda_C_A56_pc"] = lc_a56 / PC
    return ok, "sym 0; %.4f pc vs A56 %.4f pc (rel %.1e)" % (lc / PC, lc_a56 / PC, r)


def k9():
    """The literal premise lambda_C = lambda_T fails: the ratio equals m_P c^2/(k_B T_dS) != 1."""
    ratio_len = LAM_T / LAM_C
    ratio_energy = M_P * c * c / (KB * T_DS_LIVE)
    r = abs(ratio_len - ratio_energy) / ratio_energy
    ok = (r < 1e-12) and (ratio_len > 1e6)
    NUMBERS["K9_lambda_T_over_lambda_C"] = ratio_len
    NUMBERS["K9_mPc2_over_kT"] = ratio_energy
    return ok, "ratio %.4e; m_Pc2/kT %.4e" % (ratio_len, ratio_energy)


def k10():
    """The stiffness that WOULD satisfy lambda_C = lambda_T: L* -> sqrt(2) lambda_T."""
    lstar_req = math.sqrt(2.0) * LAM_T
    r_len = lstar_req / (L_STAR * math.sqrt(ETA_OVER_G))
    eta_ratio = (LAM_T / LAM_C) ** 2
    ok = (rel(r_len ** 2, eta_ratio) < 1e-12) and (r_len > 1e6)
    NUMBERS["K10_Lstar_req_Gpc"] = lstar_req / (1e9 * PC)
    NUMBERS["K10_eta_ratio"] = eta_ratio
    return ok, "L*_req %.3f Gpc (x%.3e); eta x%.3e" % (lstar_req / (1e9 * PC), r_len, eta_ratio)


def k11():
    """A72's a_sat = k_B T/(m lambda_C) is mass-independent and its target is cH_L/2pi."""
    vals = []
    for fac in (0.1, 1.0, 10.0, 1e3):
        m = M_P * fac
        vals.append(KB * T_DS_LIVE / (m * (HBAR / (m * c))))
    spread = (max(vals) - min(vals)) / vals[0]
    target = c * H_L / (2 * math.pi)          # the claim under test, always cH_Lambda/2pi
    r = rel(vals[0], target)
    ok = (spread < 1e-12) and (r < 1e-12)
    NUMBERS["K11_a_sat"] = vals[0]
    return ok, "spread %.1e; a_sat %.6e" % (spread, vals[0])


def k12():
    """The missing 2pi: a_Unruh(T_dS) = cH, and a0 = a_Unruh/(2pi) = c^2/lambda_T."""
    a_unruh = 2 * math.pi * c * KB * T_DS_LIVE / HBAR
    a0_geom = c * c / LAM_T
    r1 = rel(a0_geom, A0_LIVE)
    r2 = rel(a_unruh / (2 * math.pi), A0_LIVE)
    ok = (r1 < 1e-12) and (r2 < 1e-12)
    NUMBERS["K12_a_unruh"] = a_unruh
    NUMBERS["K12_cH_over_a0"] = CH_L / A0_LIVE
    return ok, "a_U %.4e; c^2/lambda_T rel %.1e" % (a_unruh, r1)


def k13():
    """The premise in energy units: hbar a0/c = k_B T_dS.  True only for the thermal a0."""
    lhs = HBAR * A0_LIVE / c
    rhs = KB * T_DS_LIVE
    r = rel(lhs, rhs)
    lhs_can = HBAR * A0_CLOS / c
    ok = (r < 1e-12) and (rel(lhs_can, rhs) > 0.05)
    NUMBERS["K13_hbar_a0_over_c"] = lhs
    NUMBERS["K13_kT_dS"] = rhs
    NUMBERS["K13_ratio_canonical"] = lhs_can / rhs
    return ok, "ratio %.12f; canonical %.6f" % (lhs / rhs, lhs_can / rhs)


# ===========================================================================
# PART 3 -- ALTERNATIVE ROUTES
# ===========================================================================
def k14():
    """Thermal energy density of the gapless k^4 mode at T_dS vs a0^2/(8 pi G)."""
    beta = BETA
    A2 = L_STAR ** 2 / (2.0 * (2.0 + 3.0 * beta))     # alpha/Q, alpha=gamma=K L*^2/2, Q=K(2+3b)/b
    Amp = math.sqrt(A2)                               # omega = Amp p^2
    Tn = H_L / (2.0 * math.pi * c)                    # T_dS in m^-1 (hbar=c=k_B=1)
    # the closed form is always the k^4 one; a mutation of the dispersion must contradict it
    closed = mp.gamma(2.5) * mp.zeta(2.5) / (4 * mp.pi ** 2) * Tn ** 2.5 * Amp ** -1.5
    if DISP == "linear":
        # omega = p: rho = T^4/(2 pi^2) * int x^3/(e^x-1) dx = pi^2 T^4/30
        quad = Tn ** 4 / (2 * mp.pi ** 2) * mp.quad(lambda x: x ** 3 / (mp.e ** x - 1), [0, mp.inf])
    else:
        # omega = Amp p^2: substitute x = Amp p^2/T, measure-free quadrature in x
        quad = Tn ** 2.5 * Amp ** -1.5 / (4 * mp.pi ** 2) \
            * mp.quad(lambda x: x ** 1.5 / (mp.e ** x - 1), [0, mp.inf])
    r = abs(quad - closed) / closed
    rho_SI = float(quad) * HBAR * c
    target = A0_LIVE ** 2 / (8 * math.pi * G)
    ratio = rho_SI / target
    ok = (r < 1e-8) and (math.log10(ratio) < -100)
    NUMBERS["K14_rho_k4_SI"] = rho_SI
    NUMBERS["K14_a0sq_over_8piG"] = target
    NUMBERS["K14_log10_ratio"] = math.log10(ratio) if ratio > 0 else -999
    return ok, "quad/closed %.1e; rho %.2e J/m3; log10 ratio %.2f" % (float(r), rho_SI,
                                                                     math.log10(ratio) if ratio > 0 else -999)


def k15():
    """The massive P quanta are not populated at T_dS: Boltzmann factor e^{-2e9}."""
    x = M_P * c * c / (KB * T_DS_LIVE)
    ln_n = -x - mp.log(1 - mp.e ** (-x))
    log10_n = float(ln_n / mp.log(10))
    log10_pred = -x / math.log(10)
    r = abs(log10_n - log10_pred) / abs(log10_pred)
    # upper bound on the massive-mode energy density (natural units, non-relativistic)
    Tn = H_L / (2.0 * math.pi * c)
    mn = 1.0 / (LAM_C * MP_FACTOR)
    ln_rho = math.log(2.0) + 2 * math.log(mn) + 2 * math.log(Tn) - math.log(2 * math.pi ** 2) - x
    ln_rho_SI = ln_rho + math.log(HBAR * c)
    ln_target = math.log(A0_LIVE ** 2 / (8 * math.pi * G))
    log10_ratio = (ln_rho_SI - ln_target) / math.log(10.0)
    ok = (r < 1e-9) and (log10_ratio < -1e6)
    NUMBERS["K15_log10_occupation"] = log10_n
    NUMBERS["K15_log10_rho_ratio"] = log10_ratio
    return ok, "log10 n %.4e; log10 rho ratio %.4e" % (log10_n, log10_ratio)


def k16():
    """Horizon entropy per cell of size L*: two routes, and it is not a0 in Planck units."""
    A_h = 4.0 * math.pi * (c / H_L) ** 2
    # route A: the area law with the live normalisation, per cell
    S_cell_A = L_STAR ** 2 / (S_QUARTER * L_P ** 2)
    # route B: the Lambda form S_dS = 3 pi/(Lambda l_P^2), divided by the number of cells
    S_tot_Lam = 3.0 * math.pi / (LAM * L_P ** 2)
    S_cell_B = S_tot_Lam / (A_h / L_STAR ** 2)
    r = rel(S_cell_A, S_cell_B)
    ratio = S_cell_A / (A0_LIVE / A_PLANCK)
    ok = (r < 1e-12) and (abs(math.log10(ratio)) > 100)
    NUMBERS["K16_S_cell"] = S_cell_A
    NUMBERS["K16_a0_over_aP"] = A0_LIVE / A_PLANCK
    NUMBERS["K16_log10_ratio"] = math.log10(ratio)
    return ok, "S_cell %.4e; log10(S_cell/(a0/aP)) %.2f" % (S_cell_A, math.log10(ratio))


def k17():
    """The entropy route returns a0 only because S_dS inverts Lambda: a0 = c^2/(2 l_P sqrt(pi S))."""
    S_tot = 4.0 * math.pi * (c / H_L) ** 2 / (S_QUARTER * L_P ** 2)
    a0_ent = c * c / (2.0 * L_P * math.sqrt(math.pi * S_tot))
    r = rel(a0_ent, A0_LIVE)
    ok = r < 1e-10
    NUMBERS["K17_a0_from_entropy"] = a0_ent
    NUMBERS["K17_S_dS"] = S_tot
    return ok, "a0_ent %.6e; rel %.1e" % (a0_ent, r)


def k18():
    """mu = k_B T_dS does NOT give half occupancy: it gives the drive g = e^{1+eps/kT} a0."""
    a0v = mp.mpf(str(A0_TH))
    # direct route: theta at mu = k_B T_dS, from z = exp((mu+eps)/kT)
    z_mu = mp.e ** (1 + EPS_KT)
    th_mu = z_mu / (1 + z_mu)
    # inverse route: solve k_B T ln(g/a0) - eps = k_B T for g
    g_mu = a0v * mp.e ** (1 + EPS_KT)
    half = mp.mpf(1) / 2
    ok = (abs(th_mu - half) > mp.mpf("0.2")) and (abs(g_mu / a0v - 1) > mp.mpf("0.5"))
    NUMBERS["K18_g_at_mu_kT_over_a0"] = float(g_mu / a0v)
    NUMBERS["K18_theta_at_mu_kT"] = float(th_mu)
    return ok, "g(mu=kT)/a0 = %.6f; theta = %.6f" % (float(g_mu / a0v), float(th_mu))


def k19():
    """Per-site capacity q = a0/N_s: with N_s = horizon cells, q/a0 = 1/N_s != 1."""
    q_over_a0 = 1.0 / N_CELLS
    ok = (N_CELLS > 1e6) and (q_over_a0 < 1e-6)
    NUMBERS["K19_N_cells"] = N_CELLS
    NUMBERS["K19_q_over_a0"] = q_over_a0
    return ok, "N_cells %.4e; q/a0 %.4e" % (N_CELLS, q_over_a0)


# ===========================================================================
# PART 4 -- THE FREE-PARAMETER LEDGER
# ===========================================================================
def k20():
    """R = 1/kappa^2: thermal kappa gives R = 3pi/2, not in the cap's {1,2,4}."""
    kap = A0_LIVE / (c * math.sqrt(G * RHO_L))
    R_from_kappa = 1.0 / kap ** 2
    R_from_Lambda = LAM * c ** 4 / (8 * math.pi * A0_LIVE ** 2)
    r = rel(R_from_kappa, R_from_Lambda)
    in_set = [abs(R_from_kappa - s) < 1e-9 for s in (1.0, 2.0, 4.0)]
    ok = (r < 1e-12) and (not any(in_set)) and (rel(R_from_kappa, 1.5 * math.pi) < 1e-12)
    NUMBERS["K20_kappa"] = kap
    NUMBERS["K20_R"] = R_from_Lambda
    return ok, "kappa %.6f; R %.9f; in {1,2,4}: %s" % (kap, R_from_Lambda, any(in_set))


def k21():
    """The thermal a0 violates the theory's closure Lambda = 32 pi a0^2/c^4 by 15.1%."""
    Lam_pred = 32 * math.pi * A0_LIVE ** 2 / c ** 4
    r = rel(Lam_pred, LAM)
    Lam_pred_can = 32 * math.pi * A0_CLOS ** 2 / c ** 4
    r_can = rel(Lam_pred_can, LAM)
    ok = (abs(r - (1.0 - 8.0 / (3.0 * math.pi))) < 1e-9) and (r > 0.15) and (r_can < 1e-6)
    NUMBERS["K21_Lambda_pred_thermal"] = Lam_pred
    NUMBERS["K21_ratio_thermal"] = Lam_pred / LAM
    NUMBERS["K21_ratio_closure"] = Lam_pred_can / LAM
    return ok, "ratio %.8f (8/(3pi)=%.8f); closure %.1e" % (Lam_pred / LAM, 8 / (3 * math.pi), r_can)


def gN(gg, aa):
    return gg * gg / (gg + aa) + LAW_CONST


def k22():
    """The law is homogeneous degree 1: g_N(lam g; lam a0) = lam g_N(g; a0); a0 is a pure scale."""
    gg, aa, lam = 0.37 * A0_TH, A0_TH, 2.7
    lhs = gN(lam * gg, lam * aa)
    rhs = lam * gN(gg, aa)
    r = rel(lhs, rhs)
    x = gg / aa
    shape = gN(gg, aa) / aa
    shape2 = gN(0.81 * aa, aa) / aa
    ok = (r < 1e-12) and (abs(shape - x * x / (1 + x) - LAW_CONST / aa) < 1e-15)
    NUMBERS["K22_homogeneity_rel"] = r
    return ok, "rel %.1e; shape x^2/(1+x) at x=0.37: %.9f" % (r, x * x / (1 + x))


def k23():
    """The 2pi is a convention: lambda_T = 2pi c/H, c/H and 4pi^2 c/H give 3 different a0."""
    a_live = c * c / (TWOPI * c / H_L)
    a_1pi = c * c / (1.0 * c / H_L)
    a_4pi2 = c * c / (4 * math.pi ** 2 * c / H_L)
    r1 = rel(a_1pi / a_live, TWOPI)
    r2 = rel(a_live / a_4pi2, 4 * math.pi ** 2 / TWOPI)
    ok = (r1 < 1e-12) and (r2 < 1e-12) and (rel(a_live, A0_LIVE) < 1e-12)
    NUMBERS["K23_a0_2pi"] = a_live
    NUMBERS["K23_a0_1pi"] = a_1pi
    NUMBERS["K23_a0_4pi2"] = a_4pi2
    return ok, "ratios %.12f / %.12f" % (a_1pi / a_live, a_live / a_4pi2)


# ===========================================================================
# run
# ===========================================================================
print("A75 thermal premise -- live parameters: occupancy=%s drive=%s twopi=%.6f "
      "temp=%s eta/gamma=%.2f disp=%s S_norm=%s" %
      (OCC, DRIVE, TWOPI, PARAMS["temp_hubble"], ETA_OVER_G, DISP, S_QUARTER))
print("a0_thermal = %.9e m/s^2   a0_closure = %.9e   T_dS = %.6e K" % (A0_TH, A0_CLOS, T_DS))
print("-" * 100)

run("K1",  k1,  "sym 0; num rel < 1e-12", "theta = -dOmega/dmu equals z/(1+z)")
run("K2",  k2,  "sym 0; num rel < 1e-20", "activity map gives theta = g/(g+a0)")
run("K3",  k3,  "|dtheta/dT|_g < 1e-40",   "the canonical gate is temperature-blind at fixed g")
run("K3b", k3b, "sym 0; rel < 1e-6",       "T-dependence requires a0 = a0(T): the premise itself")
run("K4",  k4,  "sym 0; rel < 1e-6",       "dtheta/dT at fixed mu is nonzero")
run("K5",  k5,  "sym 0; rel < 1e-20",      "S and F of the gate (F = U - TS + mu N)")
run("K6",  k6,  "rel < 1e-6; C_g = 0",     "C_mu nonzero, C_g zero: no heat capacity at fixed drive")
run("K7",  k7,  "theta_F(0)=1/2; dT != 0", "the only T-sensitive gate has A(0) = a0/2 (excluded)")
run("K8",  k8,  "sym 0; rel < 1e-4",       "lambda_C = sqrt(eta/K) = L*/sqrt(2) under eta=gamma")
run("K9",  k9,  "ratio > 1e6",             "literal lambda_C = lambda_T fails by 2e9")
run("K10", k10, "L*_req > 1e6 L*",         "the stiffness that would satisfy it")
run("K11", k11, "spread < 1e-12",          "A72's formula is mass-independent (no action content)")
run("K12", k12, "rel < 1e-12",             "the 2pi: a0 = a_Unruh(T_dS)/(2pi)")
run("K13", k13, "rel < 1e-12",             "hbar a0/c = k_B T_dS only for the thermal a0")
run("K14", k14, "log10 ratio < -100",      "k^4 thermal density at T_dS vs a0^2/(8piG)")
run("K15", k15, "log10 rho ratio < -1e6",  "massive P quanta are Boltzmann-suppressed at T_dS")
run("K16", k16, "|log10 ratio| > 100",     "horizon entropy per cell is not a0/a_P")
run("K17", k17, "rel < 1e-10",             "entropy route is Lambda inverted (circular)")
run("K18", k18, "g/a0 = e",                "mu = k_B T_dS does not give half occupancy at a0")
run("K19", k19, "q/a0 < 1e-6",             "per-site capacity is a0/N_s, N_s unpredicted")
run("K20", k20, "R = 3pi/2 not in {1,2,4}", "thermal kappa gives R = 3pi/2")
run("K21", k21, "deviation > 15%",         "thermal a0 violates the R=4 closure")
run("K22", k22, "rel < 1e-12",             "the law is homogeneous: a0 is a pure scale")
run("K23", k23, "ratios 2pi, 4pi^2",       "the coefficient is convention-fixed at the 2pi level")

print("-" * 100)
print("HEADLINE NUMBERS (every number quoted in report.md is printed here)")
print(" a0_thermal              %.12e m/s^2" % A0_TH)
print(" a0_closure              %.12e m/s^2" % A0_CLOS)
print(" T_dS                    %.6e K" % T_DS)
print(" kappa_thermal           %.9f" % KAPPA_TH)
print(" R_thermal               %.9f   (3pi/2 = %.9f)" % (1.0 / KAPPA_TH ** 2, 1.5 * math.pi))
print(" a0/(cH_Lambda)          %.9f   (1/(2pi) = %.9f)" % (A0_TH / CH_L, 1 / (2 * math.pi)))
print(" L* (input, A65)         %.6f pc" % (L_STAR / PC))
print(" lambda_C                %.6f pc" % (LAM_C / PC))
print(" lambda_T                %.6f Gpc" % (LAM_T / (1e9 * PC)))
print(" lambda_T/lambda_C       %.6e" % (LAM_T / LAM_C))
print(" m_P c^2                 %.6e J = %.6e eV" % (M_P * c * c, M_P * c * c / 1.602176634e-19))
print(" k_B T_dS                %.6e J" % (KB * T_DS))
print(" L*_required             %.6f Gpc" % (math.sqrt(2.0) * LAM_T / (1e9 * PC)))
print(" lambda_C at eta=3gamma  %.4f pc" % (L_STAR / math.sqrt(2.0) * math.sqrt(3.0) / PC))
print(" eta_required/eta        %.6e" % ((LAM_T / LAM_C) ** 2))
print(" a_Unruh(T_dS)           %.6e m/s^2" % (2 * math.pi * c * KB * T_DS / HBAR))
print(" hbar a0/c / kT_dS       %.12f   (canonical a0: %.6f)"
      % (HBAR * A0_TH / c / (KB * T_DS), HBAR * A0_CLOS / c / (KB * T_DS)))
print(" p_peak (k4 mode)        %.6e 1/m" % math.sqrt((H_L / (2.0 * math.pi * c))
                                                    / math.sqrt(L_STAR ** 2 / (2.0 * (2.0 + 3.0 * BETA)))))
print(" rho_k4(T_dS)            %.6e J/m^3" % NUMBERS["K14_rho_k4_SI"])
print(" a0^2/(8 pi G)           %.6e J/m^3" % NUMBERS["K14_a0sq_over_8piG"])
print(" log10(rho_k4/target)    %.4f" % NUMBERS["K14_log10_ratio"])
print(" log10 n_massive         %.6e" % NUMBERS["K15_log10_occupation"])
print(" log10(rho_massive/tgt)  %.6e" % NUMBERS["K15_log10_rho_ratio"])
print(" S_cell                  %.6e" % NUMBERS["K16_S_cell"])
print(" S_dS                    %.6e" % NUMBERS["K17_S_dS"])
print(" a0/a_Planck             %.6e" % NUMBERS["K16_a0_over_aP"])
print(" log10(S_cell/(a0/aP))   %.4f" % NUMBERS["K16_log10_ratio"])
print(" theta(mu=kT)            %.6f" % NUMBERS["K18_theta_at_mu_kT"])
print(" g(mu=kT)                %.6e m/s^2" % (NUMBERS["K18_g_at_mu_kT_over_a0"] * A0_TH))
print(" N_cells                 %.6e" % N_CELLS)
print(" q = a0/N_cells          %.6e m/s^2" % (A0_TH * NUMBERS["K19_q_over_a0"]))
print(" Lambda_pred/Lambda      %.9f   (8/(3pi) = %.9f)"
      % (NUMBERS["K21_ratio_thermal"], 8.0 / (3.0 * math.pi)))
print(" 1 - Lambda_pred/Lambda  %.6f" % (1.0 - NUMBERS["K21_ratio_thermal"]))
print(" 1 - kappa_th/kappa_can  %.6f" % (1.0 - KAPPA_TH / 0.5))
print(" kappa_th/kappa_can - 1  %.6f" % (0.5 / KAPPA_TH - 1.0))
print(" a0_th/a0_closure        %.6f" % (A0_TH / A0_CLOS))
print(" deviations (pct)        Lambda 15.12%, a0 7.87%, kappa-half 8.54%")
print("EXTERNAL INPUTS (quoted, not re-derived)")
print(" L* = 24.025012 pc (A65)                      [a75_results.json: numbers.L_star_pc]")
print(" m_P = %.6e kg (A56, via lambda_C)            [K8 cross-check]" % M_P_A56)
print(" A19 saturation cap: R in {1,2,4}; thermal R = 3pi/2 is not a member  [K20]")
print(" A72 route b (Unruh, a0 = cH_Lambda): excluded at 16.7 sigma          [cited, K12]")
print("-" * 100)

npass = sum(1 for ck in CHECKS if ck["pass"])
ntot = len(CHECKS)
print("A75 COMPLETE: %d/%d checks PASS." % (npass, ntot))
if MUT_NAME:
    print("MUTATION: %s -> %s" % (MUT_NAME, MUTATIONS[MUT_NAME]))

out = {
    "lane": "A75_thermal_premise",
    "status": "NO-GO(obstruction): the thermal premise is a new postulate, not implied by the action",
    "mutation": MUT_NAME,
    "checks": CHECKS,
    "numbers": NUMBERS,
    "constants_used": {
        "c": c, "G": G, "H0": H0, "Lambda": LAM, "hbar": HBAR, "k_B": KB,
        "pc": PC, "a0_canonical": A0_CAN, "L_star_pc": L_STAR / PC,
        "H_Lambda": H_L, "T_dS": T_DS, "a0_thermal": A0_TH,
        "a0_closure": A0_CLOS, "Z": Z_CLOS,
    },
}

if "--json-out" in _argv:
    path = _argv[_argv.index("--json-out") + 1]
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    print("wrote %s" % path)

sys.exit(0 if npass == ntot else 1)
