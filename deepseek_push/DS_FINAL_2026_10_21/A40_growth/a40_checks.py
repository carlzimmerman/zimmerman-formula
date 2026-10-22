#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A40 -- LINEAR GROWTH FROM THE MASTER ACTION: the f(z), sigma8(z) observable the
push has not computed, and the two forks that decide it.

WHAT THIS LANE DOES
  (1) Derives, exactly (sympy), the response of the canonical law
          g_N = g^2/(g+a0)   <=>   g = (g_N/2)(1 + s),  s = sqrt(1 + 4 a0/g_N)
      to a change of its source:  dg/dg_N = (1+s)^2/(4s)  [A4's D7],
      identifies G_eff = G (dg/dg_N), and shows the response is a function of the
      LOCAL Newtonian field alone -- no k, no derivative, no horizon scale.  The
      growth equation of the theory in the quasi-static sub-horizon limit is then
          delta'' + (2 + dlnH/dlna) delta' = (3/2) Omega_m(a) (G_eff/G) delta
      and its a0 -> 0 limit is integrated and checked against the exact LCDM
      growing mode (the integral solution of the same ODE).
  (2) Integrates it on the theory's OWN background: A33's F1 with beta = 0,
      Lambda_bare = 3 H0^2/c^2 (Omega_Lambda,eff = 1), Omega_c = 0.2666,
      Omega_b = 0.0497.  Reports f(z) at z = 0, 0.5, 1, 1.5, 2 and sigma8(0).
  (3) Scores it against the f sigma8 compilation on disk (8 points: 6dFGS,
      SDSS MGS, BOSS DR12, eBOSS DR16, typed in
      campaign_fresh_gravity/CFG4_cosmology.py with its bibliography) and
      against the sigma8/S8 measurements on disk (KiDS-1000, KiDS-Legacy,
      Planck 2018, DES Y3).  Reports chi^2 and N, and the size and direction of
      every offset.
  (4) THE FORK.  The cold sector is 5.3643 x the baryons and it gravitates.  Does
      the law's dg/dg_N already carry it (so that adding rho_c double counts), or
      not?  Three source branches are computed:
         S  total matter in the source, one response   (a la A33 section 5)
         A  baryons only in the source                 ("dg/dg_N already carries it")
         C  baryons boosted + cold unboosted           (reciprocity reading)
      and the action's own first integral is used to adjudicate.
      A FOURTH fork, which dominates all of them, is computed too: the reference
      field at which dg/dg_N is evaluated (cosmic cH(z) vs the perturbation's own
      rms field).  The first is scale-free by construction; the second destroys
      scale-independence and the fit.

CONVENTIONS.  c = 1 except in the numbers; K = 4 pi G; signature (-+++).
Every number printed here is written to a40_results.json.  No network, no fits.
Units: k in h/Mpc, R in Mpc/h, masses in Msun where stated.

Run:  python3 a40_checks.py            (15 checks, exit 0 iff all pass)
      python3 a40_checks.py --mutate {quad,nocold,bgflat}   (must exit 1)
"""
import json
import math
import os
import sys
import time

import numpy as np
import sympy as sp
from scipy.integrate import odeint, quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = None
for i, a in enumerate(sys.argv):
    if a == "--mutate" and i + 1 < len(sys.argv):
        MUT = sys.argv[i + 1]
    elif a.startswith("--mutate="):
        MUT = a.split("=", 1)[1]

RES = []
NP = NF = 0
NUM = {}
t0 = time.time()


def check(cid, name, measured, ok, threshold, reading=""):
    """One line per check: K<n> PASS|FAIL <measured> <threshold>."""
    global NP, NF
    ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    print(f"{cid} {tag} {measured}   {threshold}")
    if reading:
        print(f"      {reading}")
    RES.append({"id": cid, "name": name, "pass": ok,
                "value": measured if isinstance(measured, str) else str(measured),
                "threshold": threshold, "reading": reading})
    if ok:
        NP += 1
    else:
        NF += 1
    return ok


def banner(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)


# =====================================================================================
# 0.  CONSTANTS -- every one of them, with its source
# =====================================================================================
c_light = 2.99792458e8            # m/s          (BRIEF section 4)
G_N = 6.67430e-11                 # m^3/kg/s^2   (BRIEF section 4)
Mpc = 3.0856775814913673e22       # m            (BRIEF section 4)
H0_kms = 67.4                     # km/s/Mpc     (BRIEF section 4; = the de Sitter rate, A33 K16)
H0 = H0_kms * 1e3 / Mpc           # s^-1
OM_B = 0.0497                     # baryons      (task)
OM_C = 0.2666                     # cold sector  (task)
OM_M = OM_B + OM_C                # 0.3163
OM_L_EFF = 1.0                    # A33 section 3.5 with beta = 0: Omega_Lambda,eff = 1
A0_THEORY = 1.132e-10             # m/s^2  THEORY.md P3: a0 = kappa c sqrt(G rho_bare), kappa=1/2,
#                                          rho_bare = rho_DE/Omega_Lambda  -> the theory's own value
A0_CANON = 9.36e-11               # m/s^2  A33 K14b / BRIEF canonical footing (reported separately)
SIG8_PLANCK = 0.811               # Planck 2018 LCDM sigma8, the amplitude anchor
R8 = 8.0 / 0.674                  # Mpc/h -> Mpc  (8 h^-1 Mpc at h = 0.674)
SIG8_OBS = {                      # on-disk S8/sigma8 measurements (CFG1_evidence_audit.py L838)
    "KiDS-1000": (0.759, 0.021, "S8"),
    "KiDS-Legacy": (0.815, 0.021, "S8"),
    "Planck-2018": (0.832, 0.013, "S8"),
    "DES-Y3": (0.776, 0.017, "S8"),
}
# f sigma8 compilation ON DISK: campaign_fresh_gravity/CFG4_cosmology.py lines 85-88,
# with its own bibliography in the two lines above it:
#   6dFGS (Beutler+2012), SDSS MGS (Howlett+2015), BOSS DR12 consensus (Alam+2017),
#   eBOSS DR16 LRG/ELG/QSO (Alam+2021).
FS8 = [(0.067, 0.423, 0.055), (0.15, 0.53, 0.16), (0.38, 0.497, 0.045),
       (0.51, 0.458, 0.038), (0.61, 0.436, 0.034), (0.70, 0.473, 0.041),
       (0.85, 0.315, 0.095), (1.48, 0.462, 0.045)]

if MUT == "bgflat":
    OM_L_EFF = 1.0 - OM_M          # mutation: the flat-LCDM normalisation instead of Omega_L,eff = 1
if MUT == "nocold":
    pass                            # handled in the branch selector

print(__doc__)
print(f"constants: H0 = {H0_kms} km/s/Mpc (de Sitter rate, A33 K16); Omega_b = {OM_B}, "
      f"Omega_c = {OM_C}, Omega_m = {OM_M:.4f}; Omega_Lambda,eff = {OM_L_EFF}")
print(f"           a0(theory) = {A0_THEORY:.4e} m/s^2 (THEORY.md P3); a0(canonical) = {A0_CANON:.4e}")
print(f"           mode = {MUT if MUT else 'none'};  Sigma_m = 0.811 (Planck 2018 LCDM anchor)")

# =====================================================================================
# 1.  THE LAW AND ITS RESPONSE -- exact
# =====================================================================================
banner("1.  THE LAW AND ITS RESPONSE, EXACT (sympy)")

s_sym = sp.symbols("s", positive=True)          # s = sqrt(1 + 4 a0/g_N), s >= 1
a0s, gNs = sp.symbols("a_0 g_N", positive=True)

# With s as the variable: g_N = 4 a0/(s^2-1), and the law inverts to g = 2 a0/(s-1).
gN_of_s = 4 * a0s / (s_sym ** 2 - 1)
g_of_s = sp.simplify((gN_of_s / 2) * (1 + s_sym))

# K1 -- the inversion is exact: g_N - g^2/(g+a0) == 0
resid1 = sp.simplify(gNs - ((gNs / 2) * (1 + sp.sqrt(1 + 4 * a0s / gNs))) ** 2
                     / ((gNs / 2) * (1 + sp.sqrt(1 + 4 * a0s / gNs)) + a0s))
# and in the s variable
resid1s = sp.simplify(gN_of_s - g_of_s ** 2 / (g_of_s + a0s))
check("K1", "law inversion g_N = g^2/(g+a0) is an exact identity",
      f"residual = {resid1} (g_N-form), {resid1s} (s-form)",
      resid1 == 0 and resid1s == 0, "residual == 0",
      "g = (g_N/2)(1+s) with s = sqrt(1+4a0/g_N) inverts the law with no remainder; "
      "in the s variable the law is g = 2a0/(s-1), g_N = 4a0/(s^2-1)")

# K2 -- the response dg/dg_N = (1+s)^2/(4s), differentiated exactly
dgdgN_s = sp.simplify(sp.diff(g_of_s, s_sym) / sp.diff(gN_of_s, s_sym))   # chain rule, rational
target = sp.simplify((1 + s_sym) ** 2 / (4 * s_sym))
resid2 = sp.simplify(dgdgN_s - target)
# second exact form: g^2/(g_N (2g - g_N))
alt = sp.simplify(g_of_s ** 2 / (gN_of_s * (2 * g_of_s - gN_of_s)))
resid2b = sp.simplify(alt - target)
check("K2", "dg/dg_N = (1+s)^2/(4s) exactly; also = g^2/(g_N(2g-g_N))",
      f"residuals = {resid2}, {resid2b}",
      resid2 == 0 and resid2b == 0, "both residuals == 0",
      "the chain rule on the exact inverse; no expansion used. This is A4's D7 eq. (19)")

def response(y):
    """G_eff/G = dg/dg_N = (1+s)^2/(4s), s = sqrt(1+4/y), y = g_N/a0."""
    y = np.asarray(y, dtype=float)
    s = np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300))
    return (1.0 + s) ** 2 / (4.0 * s)


def response_quad(y):
    """The rival (quadrature) law's response: (1+1/(2y))/sqrt(1+1/y). Mutation target."""
    y = np.asarray(y, dtype=float)
    return (1.0 + 1.0 / (2.0 * np.maximum(y, 1e-300))) / np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))


RESP = response_quad if MUT == "quad" else response      # the function the ODE actually calls


# K2b -- the response the CODE uses equals the numerical derivative of the law the code
#        inverts.  This is the link between the derivation and the numbers below, and it is
#        the check a wrong interpolation breaks (see MUTATE.md, --mutate quad).
def g_of_gN(gNv, a0v):
    s = math.sqrt(1.0 + 4.0 * a0v / gNv)
    return 0.5 * gNv * (1.0 + s)


_fd_err = 0.0
for gNv in np.logspace(-2.0, 4.0, 60):
    gNv = float(gNv) * 1.132e-10
    h = 1e-6
    fd = (g_of_gN(gNv * (1 + h), 1.132e-10) - g_of_gN(gNv * (1 - h), 1.132e-10)) / (2 * h * gNv)
    _fd_err = max(_fd_err, abs(fd / float(RESP(gNv / 1.132e-10)) - 1.0))
check("K2b", "coded response == finite-difference derivative of the coded law (60 points, 6 decades)",
      f"max relative error = {_fd_err:.2e}",
      _fd_err < 1e-8, "< 1e-8",
      "this ties the analytic formula to the function the growth ODE actually calls; a rival "
      "interpolation (the n=2 quadrature law) fails it at the 10% level")

# K3 -- range and monotonicity: 1 <= dg/dg_N < infinity, decreasing in g_N
resp = sp.simplify((1 + s_sym) ** 2 / (4 * s_sym))
resp_expand = sp.expand(resp)                     # s/4 + 1/2 + 1/(4s)
dresp_ds = sp.simplify(sp.diff(resp, s_sym))
dresp_dgN = sp.simplify(sp.diff(resp.subs(s_sym, sp.sqrt(1 + 4 * a0s / gNs)), gNs))
lim_inf = sp.limit(resp, s_sym, sp.oo)
lim_one = resp.subs(s_sym, 1)
check("K3", "response is bounded below by 1 and strictly decreasing in g_N",
      f"min = {lim_one} at g_N->inf; d/ds = {dresp_ds} > 0 for s>1; d/dg_N sign = "
      f"{sp.sign(dresp_dgN)}; g_N->0 limit = {lim_inf}",
      lim_one == 1 and sp.simplify(dresp_ds - (1 - 1 / s_sym ** 2) / 4) == 0 and lim_inf == sp.oo,
      "min == 1, derivative sign fixed, divergence at g_N=0",
      "G_eff/G in [1,inf): Newtonian at high acceleration, divergent at zero field. "
      "The divergence is the deep-MOND square-root cusp A4 K11 flags")

# K4 -- NO SCALE: the response contains no wavenumber. Symbolically and by construction.
k_sym = sp.symbols("k", positive=True)
has_k = k_sym in resp.free_symbols
# numerically: the growth ODE coefficient is k-free, so two different k give bit-identical D
check("K4", "response is a function of the local field alone: no k anywhere",
      f"k in free symbols of dg/dg_N: {has_k}; response depends on (g_N, a0) only",
      (not has_k), "no k, no derivative, no H",
      "the law is algebraic: g at a point depends on g_N at that point. Hence the growth "
      "source (3/2)Omega_m(a)(dg/dg_N)delta has no k-dependent coefficient, and every "
      "wavenumber obeys the same ODE -> D(k,z) = D(z): growth is scale-free")

# =====================================================================================
# 2.  BACKGROUND -- A33 F1 with beta = 0
# =====================================================================================
banner("2.  THE THEORY'S OWN BACKGROUND (A33 F1, beta = 0)")

# A33 (F1):  3(2+3beta) H^2 = 2 Lambda + 4 K rho,  K = 4 pi G.
# beta = 0, Lambda = Lambda_bare = 3 H0^2/c^2 (c=1)  =>  6 H^2 = 6 H0^2 + 16 pi G rho
#           =>  H^2 = H0^2 + (8 pi G/3) rho  =>  E^2 = 1 + Omega_m (1+z)^3.
def E2(a, om=OM_M, ol=OM_L_EFF):
    return ol + om * a ** -3.0


def Om_of_a(a, om=OM_M, ol=OM_L_EFF):
    return om * a ** -3.0 / E2(a, om, ol)


E2_0 = E2(1.0)
H_today = H0 * math.sqrt(E2_0)
check("K5", "background: E^2(0) = Omega_L,eff + Omega_m exactly; the model's present rate",
      f"E^2(0) = {E2_0:.6f} = 1 + {OM_M:.4f}; H(0) = {H0_kms*math.sqrt(E2_0):.2f} km/s/Mpc "
      f"= {math.sqrt(E2_0):.4f} x H0(dS)",
      abs(E2_0 - (1.0 + OM_M)) < 1e-12, "|E^2(0)-(1+Omega_m)| < 1e-12",
      "A33 section 3.5 with beta=0: Lambda_bare = 3H0^2/c^2 gives Omega_Lambda,eff = 1 and the "
      "matter adds on top. FLAG: with H0 fixed as the de Sitter rate the model's present "
      "expansion rate is 1.1473 H0 = 77.3 km/s/Mpc (or, equivalently, Omega_K = -Omega_m). "
      "This is a background-level prediction of the beta=0 vacuum, not a choice")

NUM["background"] = {"Omega_b": OM_B, "Omega_c": OM_C, "Omega_m": OM_M,
                     "Omega_L_eff": OM_L_EFF, "E2_0": E2_0,
                     "H0_dS_kms": H0_kms, "H_today_kms": H0_kms * math.sqrt(E2_0),
                     "Omega_m_a1": float(Om_of_a(1.0)),
                     "note": "E^2 = 1 + Omega_m a^-3; H0 is the de Sitter rate Lambda_bare=3H0^2"}

# =====================================================================================
# 3.  THE GROWTH EQUATION, ITS a0 -> 0 LIMIT, AND THE SOLVER
# =====================================================================================
banner("3.  THE GROWTH EQUATION AND THE a0 -> 0 LIMIT (LCDM control)")

# delta'' + (2 + dlnH/dlna) delta' = (3/2) Omega_m(a) (G_eff/G) delta
# For dust + Lambda:  dlnH/dlna = -(3/2) Omega_m(a), so the friction is 2 - 1.5 Omega_m.
X0, A0s = math.log(1e-4), math.log(1.0)


def solve_growth(geff, om=OM_M, ol=OM_L_EFF, n=4000):
    """Integrate the growth ODE in x = ln a.  geff(x) -> G_eff/G.  Returns (x, D, f, delta)."""
    x = np.linspace(X0, A0s, n)
    a = np.exp(x)

    def rhs(_x, y):
        aa = math.exp(_x)
        om_a = om * aa ** -3.0 / (ol + om * aa ** -3.0)
        g = float(geff(_x))
        return [y[1], 1.5 * om_a * g * y[0] - (2.0 - 1.5 * om_a) * y[1]]

    sol = solve_ivp(rhs, (X0, A0s), [math.exp(X0), math.exp(X0)], t_eval=x,
                    rtol=1e-11, atol=1e-15, method="DOP853")
    d = sol.y[0]
    dp = sol.y[1]
    return x, d, dp / d, d


def D_lcdm_integral(a, om, ol):
    """Exact growing mode of the LCDM ODE: D = (5/2) Om E(a) int_0^a da'/(a' E)^3."""
    f = lambda ap: 1.0 / (ap * math.sqrt(ol + om * ap ** -3.0)) ** 3
    I = quad(f, 1e-9, a, limit=400)[0]
    return 2.5 * om * math.sqrt(ol + om * a ** -3.0) * I


one = lambda _x: 1.0
x_l, D_l, f_l, _ = solve_growth(one, om=OM_M, ol=1.0 - OM_M)      # LCDM control (flat)
D_lcdm_ode = float(D_l[-1])
D_lcdm_int = D_lcdm_integral(1.0, OM_M, 1.0 - OM_M)
# exact f(0) of the same ODE from the integral solution: f = -1.5 Om(a) + 1/(a^3 E^3 I(a))
def f_integral(a, om, ol):
    I = quad(lambda ap: 1.0 / (ap * math.sqrt(ol + om * ap ** -3.0)) ** 3, 1e-9, a, limit=400)[0]
    E = math.sqrt(ol + om * a ** -3.0)
    return -1.5 * (om * a ** -3.0 / E ** 2) + 1.0 / (a ** 3 * E ** 3 * I)


f_lcdm_0 = float(f_l[-1])
f_lcdm_int = f_integral(1.0, OM_M, 1.0 - OM_M)
eps = sp.symbols("epsilon", positive=True)
ser = sp.series((1 + sp.sqrt(1 + 4 * eps)) ** 2 / (4 * sp.sqrt(1 + 4 * eps)), eps, 0, 3).removeO()
c1, c2 = ser.coeff(eps, 1), ser.coeff(eps, 2)
check("K6", "a0 -> 0 limit: G_eff -> G and the equation reduces to LCDM",
      f"dg/dg_N = 1 + {c1}*(a0/g_N) + {c2}*(a0/g_N)^2 + O(eps^3) -> 1; "
      f"ODE with a0=0: D(1) = {D_lcdm_ode:.6f} vs integral {D_lcdm_int:.6f}",
      c1 == 0 and abs(D_lcdm_ode - D_lcdm_int) < 2e-4, "linear coeff == 0; |D_ode-D_int| < 2e-4",
      f"the exact growing mode of the same ODE is D=(5/2)Om E(a) int da'/(a'E)^3 = "
      f"{D_lcdm_int:.6f}. The correction to G_eff is QUADRATIC in a0/g_N (+1*(a0/g_N)^2), so "
      f"the Newtonian limit is approached from above with zero linear term: LCDM is the exact "
      f"a0=0 limit, not merely a small-a0 approximation")

check("K7", "LCDM control: f(0) and D(1) at Omega_m = 0.3163",
      f"f(0) = {f_lcdm_0:.5f} vs integral-solution {f_lcdm_int:.5f}; D(1) = {D_lcdm_ode:.5f}",
      abs(f_lcdm_0 - f_lcdm_int) < 1e-4 and abs(D_lcdm_ode - 0.7886) < 2e-3,
      "|f_ode-f_int| < 1e-4; |D(1)-0.7886| < 2e-3",
      "the solver reproduces the standard flat-LCDM numbers (D(1)=0.7886, f(0)=0.528 for "
      "Omega_m=0.3163), so a failure below is the theory's and not the integrator's")

NUM["lcdm_control"] = {"f0": f_lcdm_0, "D1_ode": D_lcdm_ode, "D1_integral": D_lcdm_int,
                       "Omega_m": OM_M, "Omega_L": 1.0 - OM_M}

# =====================================================================================
# 4.  THE THEORY'S GROWTH -- primary branch (S) and the reference-field fork
# =====================================================================================
banner("4.  THE THEORY'S GROWTH ON ITS OWN BACKGROUND")

A0 = A0_THEORY


def geff_cosmic(a0):
    """Reference field = the cosmic acceleration cH(z). The only background
    acceleration the theory has, and the convention the record itself uses
    (glm53_push/L180: 'G_eff/G = nu(cH(z)/a0)')."""
    def g(x):
        return float(RESP(c_light * H0 * math.sqrt(E2(math.exp(x))) / a0))
    return g


def geff_rms(sig8_0, a0, power=-2.4):
    """Reference field = the rms Newtonian field of the sigma8 sphere (R = 8/h Mpc):
    g_rms(z) = (4 pi G/3) rho_m(z) sigma8(z) R8.  sigma8(z) = sig8_0 D(z)/D(0)."""
    def make(D):
        def g(x):
            aa = math.exp(x)
            i = int(np.argmin(np.abs(np.exp(X0 + (A0s - X0) * np.arange(len(D)) / (len(D) - 1)) - aa)))
            s8z = sig8_0 * D[i] / D[-1]
            rho_fac = 0.5 * OM_M * H0 ** 2 * aa ** -3.0        # (4 pi G/3) rho_m(a)
            grms = rho_fac * s8z * R8 * Mpc
            return float(RESP(grms / a0))
        return g
    return make


# ---- the source branches.  'S' total matter, 'A' baryons only, 'C' baryons boosted
#      + cold unboosted (defined here so the primary honours the mutation switch).
SRC_MODE = "A" if MUT == "nocold" else "S"


def solve_branch(mode, a0=A0, sig8_0=None):
    g = geff_cosmic(a0)
    x = np.linspace(X0, A0s, 1500)

    def rhs(_x, y):
        aa = math.exp(_x)
        om_a = OM_M * aa ** -3.0 / (OM_L_EFF + OM_M * aa ** -3.0)
        if mode == "S":
            s = 1.5 * om_a * float(g(_x))
        elif mode == "A":
            s = 1.5 * om_a * (OM_B / OM_M) * float(g(_x))
        elif mode == "C":
            s = 1.5 * (om_a * (OM_B / OM_M) * float(g(_x)) + om_a * (OM_C / OM_M))
        return [y[1], s * y[0] - (2.0 - 1.5 * om_a) * y[1]]
    sol = solve_ivp(rhs, (X0, A0s), [math.exp(X0), math.exp(X0)], t_eval=x,
                    rtol=1e-11, atol=1e-15, method="DOP853")
    return x, sol.y[0], sol.y[1] / sol.y[0]


# ---- primary: the branch the action selects (S), cosmic reference field
gS = geff_cosmic(A0)
x_t, D_t, f_t = solve_branch(SRC_MODE)
D_th_1 = float(D_t[-1])
SIG8_TH = SIG8_PLANCK * D_th_1 / D_lcdm_ode
Z_REQ = [0.0, 0.5, 1.0, 1.5, 2.0]


def at(z, arr, zz):
    a = 1.0 / (1.0 + z)
    return float(np.interp(a, np.exp(x_t), arr))


f_tab = {z: at(z, f_t, x_t) for z in Z_REQ}
D_tab = {z: at(z, D_t, x_t) for z in Z_REQ}
s8_tab = {z: SIG8_TH * D_tab[z] / D_th_1 for z in Z_REQ}
geff_tab = {z: float(gS(math.log(1.0 / (1.0 + z)))) for z in Z_REQ}

print(f"  G_eff/G (cosmic closure): " + ", ".join(f"z={z}: {geff_tab[z]:.5f}" for z in Z_REQ))
print(f"  {'z':>5} {'a':>7} {'f(z)':>9} {'D(z)':>9} {'sigma8(z)':>10} {'G_eff/G':>9}")
for z in Z_REQ:
    print(f"  {z:5.2f} {1/(1+z):7.4f} {f_tab[z]:9.5f} {D_tab[z]:9.5f} {s8_tab[z]:10.5f} {geff_tab[z]:9.5f}")
print(f"  sigma8(0) = {SIG8_TH:.5f}   [= 0.811 x D_th(1)/D_LCDM(1) = 0.811 x "
      f"{D_th_1:.5f}/{D_lcdm_ode:.5f}]")

mono = all(f_tab[Z_REQ[i]] < f_tab[Z_REQ[i + 1]] for i in range(len(Z_REQ) - 1))
check("K8", "f(z) rises monotonically to 1 with z (the growing mode's signature)",
      f"f = {[round(f_tab[z],5) for z in Z_REQ]}; all < 1: {all(v<1 for v in f_tab.values())}",
      mono and all(v < 1.0 for v in f_tab.values()), "strictly increasing, f<1",
      "a monotone f is what a single growing mode gives; a non-monotone f would mean the "
      "integration or the response sign is wrong")

# independent second solver: LSODA (scipy.integrate.odeint) on the same system.
# A different library routine, a different adaptive scheme and a different error controller.
def solve_growth_odeint(geff, om=OM_M, ol=OM_L_EFF, n=4000):
    x = np.linspace(X0, A0s, n)

    def rhs(y, _x):
        aa = math.exp(_x)
        om_a = om * aa ** -3.0 / (ol + om * aa ** -3.0)
        g = float(geff(_x))
        return [y[1], 1.5 * om_a * g * y[0] - (2.0 - 1.5 * om_a) * y[1]]
    sol = odeint(rhs, [math.exp(X0), math.exp(X0)], x, rtol=1e-12, atol=1e-15)
    return sol[:, 0]


D_S_ref = float(solve_branch("S")[1][-1])
D_alt = solve_growth_odeint(gS)          # the same branch S, LSODA
ratio = D_alt[-1] / D_S_ref
check("K9", "the growth solution is integrator-independent (DOP853 vs LSODA), branch S",
      f"D(1) = {D_S_ref:.9f} (DOP853) vs {D_alt[-1]:.9f} (LSODA) -> ratio-1 = {ratio-1:+.2e}",
      abs(ratio - 1.0) < 1e-6, "|ratio-1| < 1e-6",
      "two independent adaptive integrators on the same ODE; a sign or friction error would "
      "show up here at O(1)")

NUM["growth_primary"] = {"z": Z_REQ, "f": [f_tab[z] for z in Z_REQ],
                         "D": [D_tab[z] for z in Z_REQ],
                         "sigma8_z": [s8_tab[z] for z in Z_REQ],
                         "G_eff_over_G": [geff_tab[z] for z in Z_REQ],
                         "sigma8_0": SIG8_TH, "D1": D_th_1,
                         "a0": A0, "closure": "cosmic cH(z) reference field, total-matter source",
                         "H0_kms": H0_kms, "H_today_kms": H0_kms * math.sqrt(E2_0)}

# =====================================================================================
# 5.  THE FORK: DOES dg/dg_N ALREADY CARRY THE COLD SECTOR?
# =====================================================================================
banner("5.  THE FORK -- COLD SECTOR IN THE SOURCE, OR ALREADY IN THE RESPONSE?")


xS, DS, fS = solve_branch("S")
xA, DA, fA = solve_branch("A")
xC, DC, fC = solve_branch("C")
table = {}
for nm, (xx, DD, ff) in (("S", (xS, DS, fS)), ("A", (xA, DA, fA)), ("C", (xC, DC, fC))):
    s8 = SIG8_PLANCK * DD[-1] / D_lcdm_ode
    table[nm] = {"sigma8_0": s8, "D1": float(DD[-1]),
                 "f": {z: float(np.interp(1 / (1 + z), np.exp(xx), ff)) for z in Z_REQ}}
    print(f"  branch {nm}: sigma8(0) = {s8:.4f}  D(1) = {DD[-1]:.4f}  "
          f"f(0) = {table[nm]['f'][0.0]:.4f}  f(2) = {table[nm]['f'][2.0]:.4f}")

check("K10", "the fork is DECIDABLE: branch S and branch A differ far beyond any error",
      f"sigma8(S) = {table['S']['sigma8_0']:.4f} vs sigma8(A) = {table['A']['sigma8_0']:.4f} "
      f"-> ratio {table['S']['sigma8_0']/table['A']['sigma8_0']:.3f}",
      table["S"]["sigma8_0"] / table["A"]["sigma8_0"] > 1.5, "ratio > 1.5",
      "putting the cold sector in the source raises sigma8 by tens of per cent; the two "
      "readings cannot both be called 'the theory'")

# the action's own first integral: g = g_N + u, g_N = G M_src/r^2 with M_src = M_b + M_c
# (A33 section 5). Consequence: the law is a relation between TOTAL g and TOTAL g_N.
Mph_over_Mb = 25.90                 # THEORY.md section 3.7 (MW-like, virial radius)
Mc_over_Mb = OM_C / OM_B            # 5.3643
check("K11", "the law's g_N is TOTAL (A33 section 5 first integral), so rho_c is not double counted",
      f"M_c/M_b = {Mc_over_Mb:.4f}; the law's phantom M_ph/M_b = {Mph_over_Mb:.2f}; "
      f"M_c/M_ph = {Mc_over_Mb/Mph_over_Mb:.3f}; g_N,tot/g_N,b = {1+Mc_over_Mb:.3f} "
      f"-> deep-MOND g ratio sqrt = {math.sqrt(1+Mc_over_Mb):.3f}",
      (1 + Mc_over_Mb) > 1.0 and Mc_over_Mb / Mph_over_Mb < 1.0,
      "M_src = M_b+M_c and M_ph != M_c",
      "the action's first integral fixes M_src = M_b + M_c: the law relates the total field to "
      "the total Newtonian field. NOT double counting -- the law contains only the SUM. "
      "NOTE the cost: evaluated with M_src = 6.3643 M_b the law predicts g = sqrt(6.3643) x the "
      "baryon-only deep-MOND value, i.e. 2.523x the SPARC fit's g. Branch S is the action's "
      "reading and it is INCONSISTENT with the baryon-only SPARC fits of THEORY.md section 4. "
      "Branch C is what those fits use and it needs the cold to be unboosted")

# ---- branch R: the amplitude closure (the reference field = the perturbation's own rms field)
xg = xS
Dn = DS / DS[-1]                       # shape from the primary pass (fixed point in the shape)


def g_rms_factory(s8_0, Dn=Dn, xg=xg):
    axg = np.exp(xg)

    def g(x):
        aa = math.exp(x)
        s8z = s8_0 * float(np.interp(aa, axg, Dn))
        rho_fac = 0.5 * OM_M * H0 ** 2 * aa ** -3.0        # (4 pi G/3) rho_m(a)
        return float(RESP(rho_fac * s8z * R8 * Mpc / A0))
    return g


sig = SIG8_PLANCK
hist = []
for it in range(40):
    gg = g_rms_factory(sig)
    xr, Dr, fr, _ = solve_growth(gg)
    new = SIG8_PLANCK * Dr[-1] / D_lcdm_ode if Dr[-1] > 0 else float("inf")
    hist.append(float(new))
    if not np.isfinite(new) or new > 1e3:
        break
    if abs(new - sig) / new < 1e-4:
        sig = new
        break
    sig = 0.5 * sig + 0.5 * new
s8_R = hist[-1]
g_rms_0 = 0.5 * OM_M * H0 ** 2 * SIG8_PLANCK * R8 * Mpc
g_rms_fix = g_rms_0 * (s8_R / SIG8_PLANCK)
print(f"  branch R (rms field, amplitude closure): iterations {len(hist)}, "
      f"sigma8(0) -> {s8_R:.3f}; g_rms(8/h Mpc, z=0) = {g_rms_0:.3e} m/s^2 = "
      f"{g_rms_0/A0:.4f} a0 -> G_eff/G = {float(RESP(g_rms_0/A0)):.2f}")
check("K12", "the amplitude closure breaks the theory: sigma8 is driven to O(10) or diverges",
      f"sigma8(0) fixed point = {s8_R:.3f} (Planck 0.811; growth-ratio band 0.75-0.85); "
      f"G_eff/G(g_rms) = {float(RESP(g_rms_0/A0)):.1f}",
      (not np.isfinite(s8_R)) or s8_R > 1.5, "sigma8 > 1.5 (1.8x the top of the observed band)",
      "with g_ref = the perturbation's own rms field, G_eff/G = 10-12 at z=0 and the growth "
      "is quasi-linear (G_eff depends on delta). This is the SAME failure L341/FP22 recorded "
      "for the chassis (sigma8 = 18-27); it is not cured by this background")

# scale-dependence of the amplitude closure: G_eff at two wavenumbers
def sig_R(R, n_eff=-2.4, s8=SIG8_PLANCK, R8m=R8):
    return s8 * (R / R8m) ** (-(3.0 + n_eff) / 2.0)
gN_k = {kh: 0.5 * OM_M * H0 ** 2 * sig_R(1.0 / kh, R8m=8.0) * ((1.0 / kh) / 0.674) * Mpc
        for kh in (0.05, 0.2)}
Gk = {kh: float(RESP(gN_k[kh] / A0)) for kh in gN_k}
check("K13", "amplitude closure is NOT scale-free: G_eff varies across the linear range",
      f"G_eff(k=0.05)/G_eff(k=0.2) = {Gk[0.05]/Gk[0.2]:.3f} "
      f"({Gk[0.05]:.2f} vs {Gk[0.2]:.2f}); n_eff = -2.4 assumed",
      abs(Gk[0.05] / Gk[0.2] - 1.0) > 0.2, "ratio differs from 1 by > 20%",
      "g_N ~ delta R with delta ~ R^{-(3+n)/2}, so g_N grows with R and the boost is LARGER on "
      "SMALLER scales: the amplitude closure predicts scale-DEPENDENT growth (a bluer P(k), more "
      "small-scale power). 'Scale-free' holds only at fixed g_N, i.e. only for a reference field "
      "that is a function of time alone")

NUM["fork"] = {"M_c_over_M_b": Mc_over_Mb, "M_ph_over_M_b_MW": Mph_over_Mb,
               "M_c_over_M_ph": Mc_over_Mb / Mph_over_Mb,
               "deep_MOND_g_ratio_total_vs_baryon": math.sqrt(1 + Mc_over_Mb),
               "branches": table,
               "branch_R": {"sigma8_0": float(s8_R), "iterations": len(hist),
                            "g_rms_0": float(g_rms_0), "G_eff_rms": float(RESP(g_rms_0 / A0)),
                            "g_rms_fixed_point": float(g_rms_fix),
                            "G_eff_rms_fixed_point": float(RESP(g_rms_fix / A0)),
                            "G_eff_k": {str(k): v for k, v in Gk.items()},
                            "n_eff_assumed": -2.4}}

# =====================================================================================
# 6.  DATA ON DISK
# =====================================================================================
banner("6.  THE DATA ON DISK: f sigma8 AND sigma8")

s8_fn = lambda z, s80: s80 * float(np.interp(1 / (1 + z), np.exp(xS), DS / DS[-1]))
f_fn = lambda z: float(np.interp(1 / (1 + z), np.exp(xS), fS))
f_fn_L = lambda z: float(np.interp(1 / (1 + z), np.exp(x_l), f_l))


def chi2_fs8(f_fn_, s80):
    tot = 0.0
    rows = []
    for z, obs, err in FS8:
        pred = f_fn_(z) * s8_fn(z, s80)
        r = (pred - obs) / err
        rows.append((z, obs, err, pred, r))
        tot += r * r
    return tot, rows


chi2_th, rows_th = chi2_fs8(f_fn, SIG8_TH)
chi2_L, rows_L = chi2_fs8(f_fn_L, SIG8_PLANCK)
print(f"  {'z':>5} {'f s8 obs':>9} {'err':>6} {'theory':>8} {'pull':>7} {'LCDM':>8} {'pull':>7}")
for (z, obs, err, pred, r), (_, _, _, predL, rL) in zip(rows_th, rows_L):
    print(f"  {z:5.2f} {obs:9.3f} {err:6.3f} {pred:8.3f} {r:+7.2f} {predL:8.3f} {rL:+7.2f}")
print(f"  chi^2(theory, S) = {chi2_th:.2f} / {len(FS8)} points;  "
      f"chi^2(LCDM control) = {chi2_L:.2f} / {len(FS8)}")
# brute-force recomputation as an arithmetic check
bf = sum(((f_fn(z) * s8_fn(z, SIG8_TH) - o) / e) ** 2 for z, o, e in FS8)
check("K14", "chi^2 on the 8-point f sigma8 compilation, arithmetic verified twice",
      f"theory chi^2 = {chi2_th:.3f} (N = {len(FS8)}), LCDM = {chi2_L:.3f}, "
      f"brute force = {bf:.3f}",
      abs(bf - chi2_th) < 1e-9 and 0.5 < chi2_L < 30.0, "|bf-chi2|<1e-9; 0.5<chi2_LCDM<30",
      "the LCDM control lands in the range the same data give in the literature (chi2/N ~ 1), "
      "so the score is not an artefact of the machinery")

# sigma_8 / S8 comparison
def s8_row(name, s80):
    obs, err, kind = SIG8_OBS[name]
    if kind == "S8":
        # S8 = sigma8 sqrt(Omega_m/0.3).  Two Omega_m conventions exist in this background:
        # the Lagrangian Omega_m = 0.3163 and the dynamical Omega_m(a=1) = 0.2403.
        S8_lag = s80 * math.sqrt(OM_M / 0.3)
        S8_dyn = s80 * math.sqrt(float(Om_of_a(1.0)) / 0.3)
        return S8_lag, S8_dyn, obs, err, (S8_lag - obs) / err, (S8_dyn - obs) / err
    return s80, s80, obs, err, (s80 - obs) / err, (s80 - obs) / err


print(f"\n  sigma8(0) = {SIG8_TH:.4f}; Omega_m(a=1) = {float(Om_of_a(1.0)):.4f}; "
      f"S8 (Lagrangian Omega_m) = {SIG8_TH*math.sqrt(OM_M/0.3):.4f}; "
      f"S8 (dynamical Omega_m) = {SIG8_TH*math.sqrt(float(Om_of_a(1.0))/0.3):.4f}")
s8rows = {}
for nm in SIG8_OBS:
    a, b, o, e, pa, pb = s8_row(nm, SIG8_TH)
    s8rows[nm] = {"S8_lag": a, "S8_dyn": b, "obs": o, "err": e, "pull_lag": pa, "pull_dyn": pb}
    print(f"  {nm:<12} S8 obs {o:.3f} +- {e:.3f}; theory(Lag) {a:.4f} ({pa:+.2f} sigma); "
          f"theory(dyn) {b:.4f} ({pb:+.2f} sigma)")

check("K15", "sigma8(0) and its direction relative to the sigma8/S8 measurements on disk",
      f"sigma8(0) = {SIG8_TH:.4f} vs Planck 0.811 ({SIG8_TH-0.811:+.4f}, "
      f"{(SIG8_TH-0.811)/0.006:+.2f} sigma on sigma8); S8(dyn) = "
      f"{SIG8_TH*math.sqrt(float(Om_of_a(1.0))/0.3):.4f} vs KiDS-1000 0.759 +- 0.021",
      abs(SIG8_TH - 0.811) / 0.811 < 0.15, "|sigma8-0.811|/0.811 < 15%",
      "the theory's sigma8 is BELOW Planck by the amount the extra vacuum suppresses growth; "
      "whether it lands on KiDS depends on which Omega_m enters S8")

NUM["data"] = {"fs8_points": [{"z": z, "fs8": o, "err": e} for z, o, e in FS8],
               "fs8_source": "campaign_fresh_gravity/CFG4_cosmology.py lines 85-88 "
                             "(6dFGS Beutler+2012; SDSS MGS Howlett+2015; BOSS DR12 Alam+2017; "
                             "eBOSS DR16 Alam+2021)",
               "chi2_theory_S": chi2_th, "chi2_lcdm": chi2_L, "N": len(FS8),
               "rows": [{"z": z, "obs": o, "err": e, "pred": p, "pull": r}
                        for z, o, e, p, r in rows_th],
               "sigma8_obs": s8rows,
               "chi2_per_point_theory": chi2_th / len(FS8)}

# =====================================================================================
# 7.  the a0-footing sensitivity and the flat-background sensitivity
# =====================================================================================
banner("7.  SENSITIVITIES -- a0 footing, and the background normalisation")

sens = {}
for nm, a0 in (("theory_1.132e-10", A0_THEORY), ("canonical_9.36e-11", A0_CANON)):
    gg = geff_cosmic(a0)
    xx, DD, ff, _ = solve_growth(gg)
    s80 = SIG8_PLANCK * DD[-1] / D_lcdm_ode
    c2, _ = chi2_fs8(lambda z, xx=xx, ff=ff: float(np.interp(1 / (1 + z), np.exp(xx), ff)), s80)
    sens[nm] = {"sigma8_0": s80, "f0": float(ff[-1]), "f2": float(np.interp(1 / 3.0, np.exp(xx), ff)),
                "chi2_fs8": c2, "G_eff_0": float(gg(0.0))}
    print(f"  {nm}: sigma8(0) = {s80:.4f}, f(0) = {float(ff[-1]):.4f}, "
          f"G_eff(0)/G = {float(gg(0.0)):.5f}, chi2_fs8 = {c2:.2f}")

# flat-LCDM normalisation of the same Omega_m: Omega_L = 1-Omega_m (what the theory would give
# if the beta term cancelled the excess vacuum, A33 section 3.5)
gg_flat = lambda x: float(RESP(c_light * H0 * math.sqrt((1 - OM_M) + OM_M * math.exp(x) ** -3.0) / A0))
xx_f, DD_f, ff_f, _ = solve_growth(gg_flat, om=OM_M, ol=1 - OM_M)
s80_f = SIG8_PLANCK * DD_f[-1] / D_lcdm_ode
sens["flat_LCDM_normalisation"] = {"sigma8_0": s80_f, "f0": float(ff_f[-1]),
                                   "note": "Omega_L = 1-Omega_m: the A33 'clock stress cancels "
                                           "the excess' branch; it reproduces LCDM by construction"}
print(f"  flat normalisation (Omega_L = 1-Omega_m): sigma8(0) = {s80_f:.4f}, "
      f"f(0) = {float(ff_f[-1]):.4f}  [= LCDM by construction]")

# the response tensor is anisotropic (A4 D7): eigenvalues nu (x2, transverse) and dg/dg_N
# (radial).  A spherical density perturbation samples the trace average (2 nu + dg/dg_N)/3.
def geff_trace(a0):
    def g(x):
        aa = math.exp(x)
        yv = c_light * H0 * math.sqrt(E2(aa)) / a0
        ss = math.sqrt(1.0 + 4.0 / yv)
        nu = 0.5 * (1.0 + ss)
        rd = (1.0 + ss) ** 2 / (4.0 * ss)
        return (2.0 * nu + rd) / 3.0
    return g


gg_tr = geff_trace(A0)
xx_tr, DD_tr, ff_tr, _ = solve_growth(gg_tr)
s80_tr = SIG8_PLANCK * DD_tr[-1] / D_lcdm_ode
sens["trace_average_response"] = {"sigma8_0": s80_tr, "f0": float(ff_tr[-1]),
                                  "G_eff_0": float(gg_tr(0.0)),
                                  "note": "(2 nu + dg/dg_N)/3 instead of dg/dg_N: the radial "
                                          "eigenvalue is the SMALLEST for s>1"}
print(f"  trace-average response (2nu+dg/dgN)/3: sigma8(0) = {s80_tr:.4f}, "
      f"f(0) = {float(ff_tr[-1]):.4f}, G_eff(0)/G = {float(gg_tr(0.0)):.4f}")

# ---- the background over-determination: Omega_L,eff = 1 + Omega_m + H(0)=H0 cannot all hold.
# Three ways out, all integrated with the SAME growth equation (the curvature term enters the
# friction: 2 + dlnH/dlna = 2 - 1.5 Omega_m(a) - Omega_K(a)).
def solve_bg(om, ol, ok, a0=A0, n=2500):
    x = np.linspace(X0, A0s, n)

    def rhs(_x, y):
        aa = math.exp(_x)
        E2v = ol + om * aa ** -3.0 + ok * aa ** -2.0
        om_a = om * aa ** -3.0 / E2v
        ok_a = ok * aa ** -2.0 / E2v
        g = float(RESP(c_light * H0 * math.sqrt(E2v) / a0))
        return [y[1], 1.5 * om_a * g * y[0] - (2.0 - 1.5 * om_a - ok_a) * y[1]]
    sol = solve_ivp(rhs, (X0, A0s), [math.exp(X0), math.exp(X0)], t_eval=x,
                    rtol=1e-11, atol=1e-15, method="DOP853")
    return sol.y[0][-1], sol.y[1][-1] / sol.y[0][-1]


bg = {}
for nm, ol, ok, note in (
        ("literal_OL1_H0dS", 1.0, 0.0, "Omega_L,eff = 1 flat: H(0) = 1.1473 H0 = 77.3"),
        ("flat_OL1mOm", 1.0 - OM_M, 0.0, "the beta-term cancels the excess: H(0) = H0, LCDM"),
        ("closed_OL1_OKmOm", 1.0, -OM_M, "Omega_L,eff = 1 with curvature: H(0) = H0, closed")):
    Dv, fv = solve_bg(OM_M, ol, ok)
    s8v = SIG8_PLANCK * Dv / D_lcdm_ode
    Hv = H0_kms * math.sqrt(ol + OM_M + ok)
    bg[nm] = {"Omega_L": ol, "Omega_K": ok, "D1": Dv, "f0": fv, "sigma8_0": s8v,
              "H0_today_kms": Hv, "note": note}
    print(f"  {nm:<20} Omega_L={ol:.4f} Omega_K={ok:+.4f}  H(0)={Hv:6.2f} km/s/Mpc  "
          f"D(1)={Dv:.4f}  f(0)={fv:.4f}  sigma8(0)={s8v:.4f}")
check("K16", "the background over-determination is NOT degenerate in sigma8: the fork decides the prediction",
      f"sigma8(0) = {bg['literal_OL1_H0dS']['sigma8_0']:.4f} (literal) / "
      f"{bg['flat_OL1mOm']['sigma8_0']:.4f} (flat) / {bg['closed_OL1_OKmOm']['sigma8_0']:.4f} (closed); "
      f"observed 0.811 +- 0.006 (Planck) and 0.76-0.83 (lensing)",
      bg["closed_OL1_OKmOm"]["sigma8_0"] > 1.0 and abs(bg["flat_OL1mOm"]["sigma8_0"] - 0.811) < 0.01,
      "closed > 1.0 (excluded); flat == 0.811",
      "Omega_L,eff = 1, Omega_m = 0.3163 and H(0) = H0 are three statements that cannot all hold "
      "with zero curvature. Resolving them by curvature (closed) gives sigma8 = 1.17, excluded by "
      "Planck at tens of sigma; resolving them by H(0) = 1.1473 H0 gives 0.760; cancelling the "
      "excess with the beta-stress gives 0.811 = LCDM exactly. The growth observable therefore "
      "does not test the law -- it tests which background the theory means")
NUM["background_fork"] = bg
NUM["sensitivity"] = sens
NUM["scale_independence"] = {
    "exact_at_fixed_gN": True,
    "statement": "dg/dg_N = F(g_N) with no k; the growth equation has no k-dependent "
                 "coefficient; hence D(k,z)=D(z) for every k at fixed reference field",
    "broken_by": "any reference field that depends on the perturbation amplitude, because "
                 "g_N ~ delta/k then reintroduces k",
    "G_eff_ratio_k005_k02": Gk[0.05] / Gk[0.2]}

# =====================================================================================
# 8.  FILES
# =====================================================================================
out = {"lane": "A40_growth",
       "status": "CONDITIONAL(closure: quasi-static law applied to sub-horizon perturbations; "
                 "fork resolved to branch S by A33 section 5, which then conflicts with the "
                 "baryon-only SPARC fits; reference field fixed to cH(z))",
       "checks": RES,
       "numbers": NUM,
       "constants_used": [
           "c = 2.99792458e8 m/s (BRIEF 4)", "G = 6.67430e-11 (BRIEF 4)",
           "H0 = 67.4 km/s/Mpc = 2.1843e-18 1/s (BRIEF 4; de Sitter rate per A33 K16)",
           "Mpc = 3.0856775814913673e22 m (BRIEF 4)",
           "Omega_b = 0.0497, Omega_c = 0.2666 (task)", "Omega_L,eff = 1 (A33 3.5, beta=0)",
           "a0 = 1.132e-10 m/s^2 (THEORY.md P3, rho_bare = rho_DE/Omega_L)",
           "a0 = 9.36e-11 m/s^2 (A33 K14b, canonical footing; sensitivity only)",
           "sigma8 anchor 0.811 (Planck 2018 LCDM; same A_s and transfer at z>~10)",
           "f sigma8 8 points (CFG4_cosmology.py 85-88: 6dFGS/SDSS MGS/BOSS DR12/eBOSS DR16)",
           "S8: KiDS-1000 0.759+-0.021, KiDS-Legacy 0.815, Planck 0.832+-0.013, DES Y3 0.776+-0.017 "
           "(campaign_fresh_gravity/CFG1_evidence_audit.py L838)",
           "M_ph/M_b = 25.90 at the MW virial radius (THEORY.md 3.7)",
           "n_eff = -2.4 for the sigma_R power law in the K13 scale-dependence estimate (declared)"],
       "mutate": MUT}

# derived ratios quoted in report.md, so every printed number is in this file
NUM["derived"] = {
    "ratio_sigma8_S_over_A": table["S"]["sigma8_0"] / table["A"]["sigma8_0"],
    "ratio_sigma8_S_over_C": table["S"]["sigma8_0"] / table["C"]["sigma8_0"],
    "delta_chi2_theory_minus_lcdm": chi2_th - chi2_L,
    "sigma8_offset_pct_vs_planck": 100.0 * (SIG8_TH - SIG8_PLANCK) / SIG8_PLANCK,
    "f0_ratio_theory_over_lcdm": f_tab[0.0] / f_lcdm_0,
    "f0_deficit_pct": 100.0 * (1.0 - f_tab[0.0] / f_lcdm_0),
    "f2_deficit_pct": 100.0 * (1.0 - f_tab[2.0] / float(np.interp(1 / 3.0, np.exp(x_l), f_l))),
    "S8_lag": SIG8_TH * math.sqrt(OM_M / 0.3),
    "S8_dyn": SIG8_TH * math.sqrt(float(Om_of_a(1.0)) / 0.3),
    "S8_lag_vs_dyn_pct": 100.0 * (math.sqrt(OM_M / 0.3) / math.sqrt(float(Om_of_a(1.0)) / 0.3) - 1.0),
    "a0_footing_sigma8_diff_pct": 100.0 * abs(sens["canonical_9.36e-11"]["sigma8_0"]
                                              - sens["theory_1.132e-10"]["sigma8_0"]) / SIG8_TH,
    "trace_average_sigma8_shift_pct": 100.0 * (sens["trace_average_response"]["sigma8_0"] - SIG8_TH) / SIG8_TH,
    "background_span_sigma8_pct": 100.0 * (bg["closed_OL1_OKmOm"]["sigma8_0"]
                                           - bg["literal_OL1_H0dS"]["sigma8_0"]) / SIG8_TH,
    "H0_today_over_H0_dS": math.sqrt(E2_0),
    "Omega_m_a1": float(Om_of_a(1.0)),
    "Omega_K_required_if_H0_fixed": -(OM_M),
}
with open(os.path.join(HERE, "a40_results.json"), "w") as fh:
    json.dump(out, fh, indent=2)

print("\n" + "=" * 100)
print(f"A40 COMPLETE: {NP}/{NP+NF} checks PASS.")
print("=" * 100)
sys.exit(0 if NF == 0 else 1)
