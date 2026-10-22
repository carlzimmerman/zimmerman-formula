#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A45 -- WHAT IS g_N IN COSMOLOGY?  The reference-field fork, decided at the level of the
P equation.

WHAT THIS LANE DOES
  (1) Goes back to the P equation of the master action (A33 eq. P) and linearises it
      about FRW + a scalar perturbation.  A22 proved P = 0 is the unique homogeneous
      solution on FRW, so the law cannot act on a background field; the question is what
      it does at first order in a perturbation.
        * K1-K4   the exact algebra of W(u):  the law is  g_N = u^2/(a0 (1-u/a0)),
                  i.e. the Newtonian field is QUADRATIC in the P field; nu = a0/u; the
                  inverse is a square root (branch point at g_N = 0).  There is no
                  regime in which the response is 1 + O(field).
        * K5-K9   the linearised P equation.  For a pure-gradient mode the
                  gamma (D.P)^2 and (gamma/4) F^2 terms combine exactly into
                  gamma lap^2(dP_i), so the P sector is an ELLIPTIC CONSTRAINT, not a
                  propagating field, at cosmological k.  The coefficient multiplying
                  grad(delta Phi) is 1/K * 1/(1+(k lambda_P)^2) -- reported, with its
                  numerical value at k = 0.1 h/Mpc.
        * K6-K8   the charge it carries, delta d = lap^2(delta Phi)/K, is a COPY of the
                  Poisson source.  Eliminating it between the P equation and the lapse
                  equation (A22's exact linearised system, eqs 4-6) gives
                  G_eff/G = 1 + 1/(k lambda_P)^2 = 7.6e11 at 0.1 h/Mpc -- a k^-4 runaway:
                  the linear order has NO finite solution. Equivalently u = g to 1e-12,
                  i.e. g_N/g = (k lambda_P)^2, i.e. the linearised P sector sits exactly at
                  the deep-MOND endpoint (g -> 0). The modification is inert at linear order
                  in the only operational sense: it admits no linear field.
        * K9      the linear solution is not the delta -> 0 limit of the exact solution:
                  u_exact/u_linear = sqrt(a0/g_N) = 22 at the 8 h^-1 Mpc field.
  (2) The bound-system reading, made quantitative.  The law is a static-spherical first
      integral; its hypotheses (static, spherical, isolated, u ~ a0) hold in a bound
      system and nowhere else.  Implement G_eff = 1 below a density contrast delta_c and
      the full pointwise response above it, solve the (now nonlinear) growth ODE, and
      find the delta_c that gives sigma8 = 0.832.
  (3) The filtered reading.  Implement the law with g_N smoothed on the scale R(a0)
      where the smoothed field equals a0: g_R = (1/2) Omega_m H^2 delta_R R.  Solve
      for R(a0) in the linear field (it does not exist: max g_R = 0.0021 a0) and in the
      nonlinear field (R(a0) ~ 15 kpc).  Report sigma8 and f sigma8.
  (4) Verdict, with the discriminating observable.

CONVENTIONS.  c = 1 in the algebra (SI restored in the numbers); K = 4 pi G (A33
section 1.1); signature (-+++); ' = d/dlna.  Growth is computed on the theory's own
beta = 0 background (A33 F1): Omega_Lambda,eff = 1, Omega_b = 0.0497, Omega_c = 0.2666,
H0 = 67.4 km/s/Mpc the de Sitter rate => H(0) = 77.33 km/s/Mpc (A40 K5).  sigma8 is
anchored to Planck's A_s through a LCDM transfer at z >> 10 (A40's convention), so the
LCDM control has sigma8(0) = 0.811 by construction; every sigma8 here is
0.811 * D_branch(1) / D_LCDM(1).

Run:  python3 a45_checks.py                 (exit 0 iff all checks pass)
      python3 a45_checks.py --mutate {pointwise,cH,quad,nocut,gamma_pc}   (must exit 1)
"""
import json
import math
import os
import sys
import time

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

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
    global NP, NF
    ok = bool(ok)
    print(f"{cid} {'PASS' if ok else 'FAIL'} {measured}   {threshold}")
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
# 0.  CONSTANTS, each with its source
# =====================================================================================
c_light = 2.99792458e8            # m/s
G_N = 6.67430e-11                 # m^3/kg/s^2
Mpc = 3.0856775814913673e22       # m
pc = 3.0856775814913673e16        # m
H0_kms = 67.4                     # km/s/Mpc  -- the de Sitter rate (A33 K16)
H0 = H0_kms * 1e3 / Mpc           # s^-1
H0_m = H0 / c_light               # m^-1   (c = 1 units)
OM_B = 0.0497
OM_C = 0.2666
OM_M = OM_B + OM_C                # 0.3163
OM_L_EFF = 1.0                    # A33 3.5 with beta = 0  =>  E^2 = 1 + Om a^-3
A0 = 1.132e-10                    # m/s^2  THEORY.md P3
A0_CANON = 9.36e-11               # m/s^2  A33 K14b
L_STAR = 24.0 * pc                # m      A20 surviving value (worst case for a_P)
if MUT == "gamma_pc":
    L_STAR = 24.0 * Mpc           # MUTATION: the 17 pc stiffness read as 17 Mpc (a unit slip)
LAMBDA_P = L_STAR / math.sqrt(2.0)  # m    lambda_P = sqrt(gamma/K) = L*/sqrt(2) = 17 pc
R8 = 8.0 / 0.674                  # Mpc   8 h^-1 Mpc at h = 0.674
SIG8_PLANCK = 0.811               # Planck 2018 LCDM sigma8 (the amplitude anchor)
SIG8_PLANCK_ERR = 0.006
S8_PLANCK = 0.832                 # Planck 2018 S8, the number the task names
TARGET = 0.832
# f sigma8 compilation ON DISK: campaign_fresh_gravity/CFG4_cosmology.py L85-88
FS8 = [(0.067, 0.423, 0.055), (0.15, 0.53, 0.16), (0.38, 0.497, 0.045),
       (0.51, 0.458, 0.038), (0.61, 0.436, 0.034), (0.70, 0.473, 0.041),
       (0.85, 0.315, 0.095), (1.48, 0.462, 0.045)]
Z_REQ = [0.0, 0.5, 1.0, 1.5, 2.0]

print(__doc__)
print(f"constants: H0(dS) = {H0_kms} km/s/Mpc -> H(0) = {H0_kms*math.sqrt(1+OM_M):.2f} km/s/Mpc; "
      f"Omega_b = {OM_B}, Omega_c = {OM_C}, Omega_m = {OM_M:.4f}; Omega_L,eff = {OM_L_EFF}")
print(f"           a0 = {A0:.4e} m/s^2; L* = {L_STAR/pc:.1f} pc -> lambda_P = {LAMBDA_P/pc:.2f} pc; "
      f"mutation = {MUT if MUT else 'none'}")

# =====================================================================================
# 1.  THE LAW, EXACTLY: g_N IS QUADRATIC IN THE P FIELD
# =====================================================================================
banner("1.  THE EXACT ALGEBRA OF W(u): g_N = u^2/(a0 (1-u/a0))  [the law is quadratic]")

u, a0s, gNs, gs = sp.symbols("u a_0 g_N g", positive=True)
g_of_u = u / (1 - u / a0s)                     # g = K W'(u) with W the saturating log
gN_of_u = sp.simplify(g_of_u - u)              # the first integral  g_N = g - u
law = sp.simplify(g_of_u ** 2 / (g_of_u + a0s))

res_law = sp.simplify(gN_of_u - law)
res_quad = sp.simplify(gN_of_u - u ** 2 / (a0s * (1 - u / a0s)))
check("K1", "the law is the elimination of u: g_N = g^2/(g+a0) = u^2/(a0(1-u/a0))",
      f"residuals = {res_law}, {res_quad}",
      res_law == 0 and res_quad == 0, "both residuals == 0",
      "g = K W'(u) = u/(1-u/a0) is the saturating-log force; g_N = g-u is A33 section 5's "
      "first integral. The two combine to the law (A33 K3). Rewritten in u = K|P| -- the "
      "P sector's OWN field -- the law says something the record has not used: g_N is "
      "QUADRATIC in the P field")

nu = sp.simplify(g_of_u / gN_of_u)
check("K2", "the response in closed form: nu = g/g_N = a0/u exactly",
      f"nu - a0/u = {sp.simplify(nu - a0s/u)}",
      sp.simplify(nu - a0s / u) == 0, "residual == 0",
      "the whole content of the law is that the boost is the ratio a0/u. Nothing else -- no k, "
      "no H, no delta. u is the P field. So 'which field is g_N' is the same question as "
      "'what sets u', and at the level of the algebra the only available answer is: the "
      "source's own field")

d1 = sp.simplify(sp.diff(gN_of_u, u).subs(u, 0))
d2 = sp.simplify(sp.diff(gN_of_u, u, 2).subs(u, 0))
d3 = sp.simplify(sp.diff(gN_of_u, u, 3).subs(u, 0))
ser = sp.series(gN_of_u, u, 0, 4).removeO()
check("K3", "g_N has NO linear term in u: dg_N/du|_0 = 0, d2g_N/du2|_0 = 2/a0",
      f"dg_N/du|0 = {d1}, d2/du2|0 = {d2}, d3/du3|0 = {d3}; series = {sp.simplify(ser)}",
      d1 == 0 and sp.simplify(d2 - 2 / a0s) == 0, "first derivative == 0, second == 2/a0",
      "*** The Newtonian field is QUADRATIC in the P field. ***  A first-order perturbation "
      "of P produces a SECOND-order g_N, so the modification cannot appear at first order in "
      "the density contrast. It is not that the effect is small; it is that it is absent at "
      "the order where linear growth is defined")

u_of_gN = sp.solve(sp.Eq(gNs * (a0s - u) - u ** 2, 0), u)          # the quadratic, exactly
lead = sp.simplify(u_of_gN[0])
print(f"      u(g_N) exactly = {u_of_gN}")
try:
    sp.series(a0s / sp.sqrt(a0s * gNs), gNs, 0, 2)
    puiseux = "g_N^(-1/2) (a Puiseux series: no Taylor series exists)"
except Exception:                                        # pragma: no cover
    puiseux = "g_N^(-1/2) (a Puiseux series: no Taylor series exists)"
dnu = sp.simplify(sp.diff(a0s / sp.sqrt(a0s * gNs), gNs))
lead_ratio = sp.limit(lead ** 2 / (a0s * gNs), gNs, 0)
check("K4", "the inverse is a SQUARE ROOT: u = sqrt(a0 g_N); nu = sqrt(a0/g_N) is non-analytic at g_N = 0",
      f"u(g_N) = {u_of_gN}; u^2/(a0 g_N) -> {lead_ratio}; d nu/d g_N = {dnu}",
      lead_ratio == 1 and dnu.has(gNs), f"u^2/(a0 g_N) -> 1; nu' ~ {puiseux}",
      "the law has a branch point at zero field: nu -> infinity as g_N -> 0 and nu has no "
      "Taylor series there. Hence there is NO regime in which the response is 1 + O(field): "
      "at high field it is 1 + (a0/g_N)^2 (A40 K6, quadratic), at low field it is "
      "sqrt(a0/g_N) (a square root). The two ends do not meet in a linear term")

eps = sp.symbols("epsilon", positive=True)
ser_hi = sp.series((1 + sp.sqrt(1 + 4 * eps)) ** 2 / (4 * sp.sqrt(1 + 4 * eps)), eps, 0, 3).removeO()
print(f"      high field (eps = a0/g_N):  dg/dg_N = {sp.expand(ser_hi)}")
print(f"      low  field (u/a0 -> 0)   :  nu = a0/u, g = sqrt(a0 g_N) + O(g_N)")
NUM["algebra"] = {"law": "g_N = g^2/(g+a0) = u^2/(a0(1-u/a0))", "nu": "a0/u",
                  "dgN_du_at_0": str(d1), "d2gN_du2_at_0": str(d2),
                  "u_of_gN": [str(s) for s in u_of_gN], "nu_series_at_0": puiseux}

# =====================================================================================
# 2.  LINEARISING THE P EQUATION ABOUT FRW + delta
# =====================================================================================
banner("2.  THE P EQUATION AT LINEAR ORDER: the coefficient on grad(delta Phi)")

x_, y_, z_ = sp.symbols("x y z", real=True)
chi = sp.Function("chi")(x_, y_, z_)
lap = lambda f: sp.diff(f, x_, 2) + sp.diff(f, y_, 2) + sp.diff(f, z_, 2)

# delta P_i = d_i chi is the only scalar mode of a covector at linear order.
# The two gradient operators in (P) are gamma D_i(D.P) and gamma D_j F^j_i.
res = []
for xi in (x_, y_, z_):
    dP = [sp.diff(chi, x_), sp.diff(chi, y_), sp.diff(chi, z_)]
    div = sp.diff(dP[0], x_) + sp.diff(dP[1], y_) + sp.diff(dP[2], z_)
    term_a = sp.diff(div, xi)                                    # D_i (D.P)
    term_b = lap(dP[i2 := (x_, y_, z_).index(xi)]) - sp.diff(div, xi)   # D_j F^j_i
    res.append(sp.simplify(term_a + term_b - lap(dP[i2])))
check("K5", "for a gradient mode the (D.P)^2 and F^2 terms combine exactly into lap^2(dP_i)",
      f"residuals = {res}", all(r == 0 for r in res), "all three components == 0",
      "the longitudinal piece of the F^2 operator cancels the (D.P)^2 operator identically. "
      "So the P sector's spatial operator is gamma lap^2: an ELLIPTIC CONSTRAINT with "
      "stiffness gamma = K L*^2/2, not a propagating scalar. That is why P is a slave at "
      "cosmological scales -- and it is the term A33 section 7.4 records as mis-transcribed "
      "in A3")

k_s, om_s, H_s, K_s, gam_s, eta_s = sp.symbols("k omega H K gamma eta", positive=True)
coef_qs = sp.simplify(K_s / (K_s + gam_s * k_s ** 2))
print(f"      linearised (P), quasi-static:  delta P_i = d_i(delta Phi) * [{coef_qs}]")
k_01 = 0.1 * 0.674 / Mpc                     # 0.1 h/Mpc in 1/m
kl = k_01 * LAMBDA_P
gamk2_over_K = (k_01 * LAMBDA_P) ** 2        # = (gamma/K) k^2
etaH2_over_K = (L_STAR ** 2 / 2.0) * H0_m ** 2   # = (eta/K) H^2 with eta = gamma
print(f"      k = 0.1 h/Mpc:  k*lambda_P = {kl:.3e};  (gamma/K)k^2 = {gamk2_over_K:.3e};"
      f"  (eta/K)H^2 = {etaH2_over_K:.3e}")
check("K6", "the coefficient multiplying grad(delta Phi) is 1/K to 1e-12 at cosmological k",
      f"1/(1+(k lambda_P)^2) - 1 = {-gamk2_over_K/(1+gamk2_over_K):.3e} at k = 0.1 h/Mpc "
      f"(k lambda_P = {kl:.2e}); kinetic term (eta/K)H^2 = {etaH2_over_K:.1e}",
      gamk2_over_K < 1e-10 and etaH2_over_K < 1e-15, "(gamma/K)k^2 < 1e-10 and (eta/K)H^2 < 1e-15",
      "*** THE COEFFICIENT IS 1. ***  delta P_i = d_i(delta Phi)/K exactly, in the "
      "quasi-static sub-horizon limit. The P field is not an independent degree of freedom: "
      "it is the gradient of the potential, with unit coefficient. A 17 pc stiffness is "
      "1e-12 of the cosmological scales and the Compton term is 1e-17, so no k or omega "
      "dependence survives")

# the charge is a copy of the Poisson source; A22 D4's exact linearised static system
Psi_s, rho_s, psi_s = sp.symbols("Psi rho psi")
eq4 = sp.Eq(-k_s ** 2 * Psi_s, K_s * (psi_s + rho_s))                    # lapse       A22 (4)
eq6 = sp.Eq(-gam_s * k_s ** 2 * psi_s, K_s * psi_s + k_s ** 2 * Psi_s)   # P equation  A22 (6)
psi_sol = sp.solve(eq6, psi_s)[0]
Phi_sol = sp.simplify(sp.solve(eq4.subs(psi_s, psi_sol), Psi_s)[0])
Geff_sym = sp.simplify((-k_s ** 2 * Phi_sol) / (K_s * rho_s))
Geff_lim = sp.simplify(sp.limit(Geff_sym, gam_s, 0))
print(f"      psi = {sp.simplify(psi_sol)}")
print(f"      eliminating psi between A22 (4) and (6):  Phi = {Phi_sol}")
print(f"      =>  G_eff/G = (-k^2 Phi)/(K rho) = {Geff_sym}  ->  {Geff_lim} as gamma k^2 -> 0")
Geff_num = 1.0 + 1.0 / gamk2_over_K
check("K7", "eliminating psi gives G_eff/G = 1 + 1/(k lambda_P)^2 -> DIVERGENT: no linear Newtonian limit",
      f"Phi = {Phi_sol}; G_eff/G = {Geff_sym} = {Geff_num:.2e} at k = 0.1 h/Mpc",
      Geff_lim == sp.oo or Geff_num > 1e10, "G_eff -> infinity (k^-4 runaway)",
      "*** THE LINEAR ORDER OF THE ACTION HAS NO FINITE SOLUTION. ***  The charge "
      "delta d = lap^2(delta Phi)/K is a copy of the Poisson source with coefficient 1, so "
      "A22's (4)+(6) give lap^2(Phi) = K rho (1 + K/(gamma k^2)): an anti-screened G_eff of "
      "1/(k lambda_P)^2 = 7.6e11 at 0.1 h/Mpc. The potential runs away as k^-4, so the "
      "linearised system is not a truncation of any solution -- exactly the 'zero-field k^2 "
      "runaway' A40 cites (FP22 B0-B4), now with its coefficient. There is no linear growth "
      "equation: not 'LCDM', not 'modified'")

# the law then admits only the zero-field point
g_star = A0 * gamk2_over_K
print(f"      the law + the linear P equation admit only g = a0 (k lambda_P)^2 = {g_star:.2e} m/s^2")
check("K8", "the linear branch is the deep-MOND endpoint: g_N/g = (k lambda_P)^2 -> 0, g -> a0 (k lambda_P)^2",
      f"g_N/g = {gamk2_over_K:.2e};  u/g = {1-gamk2_over_K:.12f};  g_consistent = {g_star:.1e} m/s^2",
      gamk2_over_K < 1e-10, "g_N/g < 1e-10",
      "at linear order u = g to 1e-12 and g_N/g = (k lambda_P)^2: the P field carries "
      "essentially the whole field and the Newtonian field vanishes. Combined with the law "
      "(g_N = u^2/a0) the only field the linear system admits is g = a0 (k lambda_P)^2 ~ "
      "1.5e-22 m/s^2 -- i.e. zero. Linearising about P = 0 is an expansion about the "
      "deep-MOND endpoint, not about GR")

g_rms_0 = 0.5 * OM_M * H0 ** 2 * SIG8_PLANCK * R8 * Mpc      # (4 pi G/3) rho_m sigma8 R8
ratio = math.sqrt(A0 / g_rms_0)
print(f"      g_rms(8/h Mpc, z=0) = {g_rms_0:.3e} m/s^2 = {g_rms_0/A0:.4f} a0;"
      f"  u_exact/u_linear = sqrt(a0/g_N) = {ratio:.1f}")
check("K9", "the linear solution is NOT the delta->0 limit: u_exact/u_linear = sqrt(a0/g_N) = 22",
      f"ratio at the 8 h^-1 Mpc field = {ratio:.2f}; at 0.1 a0 = {math.sqrt(10):.2f}; "
      f"at 1 a0 = 1.00", ratio > 10, "ratio > 10 (the linear solution is the wrong branch)",
      "the exact small-source solution has u = sqrt(a0 g_N), which is LARGER than g_N and "
      "scales as delta^(1/2), not delta. The linearised system (u = g) and the exact solution "
      "(u = sqrt(a0 g_N)) are different branches; the map between them is singular at "
      "delta = 0. So 'the modification is a small perturbation of GR' is not a statement this "
      "action can make")

# the first NONZERO order: g_N is quadratic, so the correction is O(g_N/a0) relative
g100 = 0.5 * OM_M * H0 ** 2 * 0.0885 * 100.0 * Mpc
print(f"      second order: g_N^(2) = (grad dPhi)^2/a0, so the correction to the potential is "
      f"O(g_N/a0) = {g_rms_0/A0:.4f} at 8/h Mpc, {g100/A0:.2e} at 100 Mpc")
check("K9b", "the first nonzero correction is O(g_N/a0) = 0.2%: the a0 effect enters at SECOND order",
      f"g_N/a0 = {g_rms_0/A0:.4f} (8/h Mpc), {g100/A0:.2e} (100 Mpc)",
      (g_rms_0 / A0) < 5e-3, "g_N/a0 < 5e-3",
      "because g_N = u^2/a0 + u^3/a0^2, the P sector's contribution to the potential at second "
      "order is (grad dPhi)^2/a0, i.e. a fraction g_N/a0 = 0.21% of the first-order Newtonian "
      "field at the 8 h^-1 Mpc peak and 0.18% at 100 Mpc (the smoothed field is nearly flat "
      "past its peak). That is the entire a0 imprint on "
      "linear growth: below every quoted error bar (sigma8 would move by < 0.2%)")

NUM["linear_order"] = {"coefficient": "1/K * 1/(1+(k lambda_P)^2)",
                       "k_lambdaP_at_0.1h": kl, "gamma_over_K_k2": gamk2_over_K,
                       "eta_over_K_H2": etaH2_over_K,
                       "psi_solution": str(sp.simplify(psi_sol)),
                       "Phi_solution": str(Phi_sol), "G_eff_symbolic": str(Geff_sym),
                       "G_eff_limit_gamma0": str(Geff_lim), "G_eff_at_0.1h": Geff_num,
                       "g_consistent_ms2": g_star,
                       "u_over_g_linear": 1.0, "gN_over_g_linear": 0.0,
                       "u_exact_over_u_linear_at_8Mpc": ratio,
                       "g_rms_8Mpc_ms2": g_rms_0, "g_rms_8Mpc_over_a0": g_rms_0 / A0}

# =====================================================================================
# 3.  THE GROWTH INTEGRATOR (A40's conventions, re-implemented) AND THE THREE BRANCHES
# =====================================================================================
banner("3.  THE GROWTH INTEGRATOR AND THE THREE BRANCHES")


def response(y):
    """G_eff/G = dg/dg_N = (1+s)^2/(4s), s = sqrt(1+4/y), y = g_N/a0."""
    y = np.asarray(y, dtype=float)
    s = np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300))
    return (1.0 + s) ** 2 / (4.0 * s)


def response_quad(y):
    y = np.asarray(y, dtype=float)
    return (1.0 + 1.0 / (2.0 * np.maximum(y, 1e-300))) / np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))


RESP = response_quad if MUT == "quad" else response


def E2(a, om=OM_M, ol=OM_L_EFF):
    return ol + om * a ** -3.0


def Om_of_a(a, om=OM_M, ol=OM_L_EFF):
    return om * a ** -3.0 / E2(a, om, ol)


X0 = math.log(1e-4)


def solve_growth(geff, om=OM_M, ol=OM_L_EFF, n=4000):
    x = np.linspace(X0, 0.0, n)

    def rhs(_x, y):
        aa = math.exp(_x)
        om_a = om * aa ** -3.0 / (ol + om * aa ** -3.0)
        return [y[1], 1.5 * om_a * float(geff(_x)) * y[0] - (2.0 - 1.5 * om_a) * y[1]]

    sol = solve_ivp(rhs, (X0, 0.0), [math.exp(X0), math.exp(X0)], t_eval=x,
                    rtol=1e-11, atol=1e-15, method="DOP853")
    d = sol.y[0]
    return x, d, sol.y[1] / d


one = lambda _x: 1.0
x_l, D_l, f_l = solve_growth(one, om=OM_M, ol=1.0 - OM_M)     # flat LCDM control
D_LCDM = float(D_l[-1])


def D_lcdm_integral(a, om, ol):
    I = quad(lambda ap: 1.0 / (ap * math.sqrt(ol + om * ap ** -3.0)) ** 3, 1e-9, a, limit=400)[0]
    return 2.5 * om * math.sqrt(ol + om * a ** -3.0) * I


# the same ODE on the theory's own background with G_eff = 1: the inert branch, and a
# second, independent check of the solver on a non-flat E(a)
x_i, D_i, f_i = solve_growth(one, om=OM_M, ol=OM_L_EFF)
check("K10", "the integrator reproduces the exact growing mode on BOTH backgrounds",
      f"flat LCDM: D(1) = {D_LCDM:.6f} vs integral {D_lcdm_integral(1.0, OM_M, 1.0-OM_M):.6f}, "
      f"f(0) = {float(f_l[-1]):.5f}; theory bg (G_eff=1): D(1) = {float(D_i[-1]):.6f} vs "
      f"integral {D_lcdm_integral(1.0, OM_M, OM_L_EFF):.6f}",
      abs(D_LCDM - D_lcdm_integral(1.0, OM_M, 1.0 - OM_M)) < 2e-4
      and abs(float(f_l[-1]) - 0.52833) < 1e-3
      and abs(float(D_i[-1]) - D_lcdm_integral(1.0, OM_M, OM_L_EFF)) < 2e-4,
      "|D_dop-D_int| < 2e-4 on both backgrounds; |f(0)-0.52833| < 1e-3",
      "the solver is A40's, re-implemented: flat LCDM at Omega_m = 0.3163 gives D(1) = 0.7886, "
      "f(0) = 0.5283; on the theory's E^2 = 1 + Omega_m a^-3 the same integral gives 0.7392. "
      "Every sigma8 below is 0.811 * D(1)/0.7886 (A40's anchor)")

S8_inert = SIG8_PLANCK * float(D_i[-1]) / D_LCDM


def geff_cH(a0):
    def g(x):
        return float(RESP(c_light * H0 * math.sqrt(E2(math.exp(x))) / a0))
    return g


x_a, D_a, f_a = solve_growth(geff_cH(A0))
S8_A = SIG8_PLANCK * float(D_a[-1]) / D_LCDM
check("K11", "branch (a), the cosmic reference field cH: reproduces A40's sigma8 = 0.7619",
      f"sigma8(0) = {S8_A:.4f} (A40: 0.7619); G_eff(0)/G = "
      f"{float(RESP(c_light*H0*math.sqrt(E2(1.0))/A0)):.4f}",
      abs(S8_A - 0.7619) < 2e-3, "|sigma8 - 0.7619| < 2e-3",
      "A40's branch (a) is reproduced. Note what it is: g_ref = cH is an acceleration the "
      "ACTION does not contain -- no term in A33 section 1 has an H in it. It is a posit, and "
      "this check certifies only that the number is reproducible")

Dn = D_a / D_a[-1]


def branch_pointwise(sig_guess=1.0, n=4000, tol=1e-4, maxit=200):
    """Fixed point of G_eff = RESP(g_rms(z)/a0), g_rms = (1/2) Om H^2 sigma8(z) R8."""
    x = np.linspace(X0, 0.0, n)
    ax = np.exp(x)
    s = sig_guess
    hist = []
    for _ in range(maxit):
        def rhs(_x, y):
            aa = math.exp(_x)
            om_a = OM_M * aa ** -3.0 / (OM_L_EFF + OM_M * aa ** -3.0)
            d8 = s * float(np.interp(aa, ax, Dn))
            gN = 0.5 * OM_M * H0 ** 2 * aa ** -3.0 * d8 * R8 * Mpc
            return [y[1], 1.5 * om_a * float(RESP(gN / A0)) * y[0] - (2.0 - 1.5 * om_a) * y[1]]
        sol = solve_ivp(rhs, (X0, 0.0), [math.exp(X0), math.exp(X0)], t_eval=x,
                        rtol=1e-9, atol=1e-13, method="DOP853")
        D = sol.y[0]
        new = SIG8_PLANCK * float(D[-1]) / D_LCDM
        hist.append(new)
        if not np.isfinite(new):
            break
        if abs(new - s) / max(new, 1e-30) < tol:
            s = new
            break
        s = 0.5 * s + 0.5 * new
    return s, D, sol.y[1] / D, hist


S8_B, D_b, f_b, hist_b = branch_pointwise(1.0)
check("K12", "branch (b), the perturbation's own rms field: reproduces A40's sigma8 = 2.267 (excluded)",
      f"sigma8(0) = {S8_B:.3f} (A40: 2.267); G_eff(0)/G = {float(RESP(g_rms_0/A0)):.2f}; "
      f"iterations {len(hist_b)}",
      abs(S8_B - 2.267) < 0.03 and S8_B > 1.5, "|sigma8 - 2.267| < 0.03",
      "A40's branch (b) is reproduced: applying the exact law pointwise to the perturbation's "
      "own field drives sigma8 to 2.267. This is the RESUMMED law (the sqrt branch), not a "
      "linearisation -- K1-K9 prove the latter does not exist")

if MUT == "pointwise":            # MUTATION: the pointwise branch adopted as the prediction
    x_v, D_v, f_v, S8_V = x_a, D_b, f_b, S8_B
elif MUT == "cH":                 # MUTATION: the cH branch adopted as the prediction
    x_v, D_v, f_v, S8_V = x_a, D_a, f_a, S8_A
else:
    x_v, D_v, f_v, S8_V = x_i, D_i, f_i, S8_inert

check("K13", "the adopted (inert) branch: G_eff = 1 at every linear scale, sigma8 and f(z)",
      f"sigma8(0) = {S8_inert:.4f} (adopted {S8_V:.4f}); D(1) = {float(D_i[-1]):.5f}; "
      f"f(0) = {float(f_i[-1]):.5f}",
      abs(S8_V - S8_inert) < 1e-6 and abs(S8_inert - 0.760) < 5e-3,
      "adopted == G_eff=1 to 1e-6; sigma8 in [0.755, 0.765]",
      "with the P sector left at its FRW value the theory grows exactly as GR on its own "
      "background: sigma8(0) = 0.760, 6.3% below Planck-2018's 0.811. The background does the "
      "suppressing: H(0) = 77.3 and Omega_m(a=1) = 0.2403 give D(1) = 0.7392 vs LCDM's 0.7886")


def f_at(z, xarr, farr):
    return float(np.interp(1.0 / (1.0 + z), np.exp(xarr), farr))


def s8_at(z, s80, xarr, Darr):
    return s80 * float(np.interp(1.0 / (1.0 + z), np.exp(xarr), Darr)) / float(Darr[-1])


def chi2_branch(xarr, Darr, farr, s80):
    tot = 0.0
    rows = []
    for z, o, e in FS8:
        fz = f_at(z, xarr, farr)
        th = fz * s8_at(z, s80, xarr, Darr)
        tot += ((th - o) / e) ** 2
        rows.append({"z": z, "obs": o, "err": e, "th": th, "pull": (th - o) / e})
    return tot, rows


chi2_v, rows_v = chi2_branch(x_v, D_v, f_v, S8_V)
chi2_a, _ = chi2_branch(x_a, D_a, f_a, S8_A)
chi2_L, _ = chi2_branch(x_l, D_l, f_l, SIG8_PLANCK)
print(f"      chi^2(f sigma8, 8 pts): inert {chi2_v:.2f}, cH {chi2_a:.2f}, LCDM control {chi2_L:.2f}")
print("        z      f(z)    sigma8(z)   f sigma8    obs      pull")
for r in rows_v:
    z = r["z"]
    print(f"      {z:5.3f}  {f_at(z, x_v, f_v):6.4f}  {s8_at(z, S8_V, x_v, D_v):8.4f}   "
          f"{r['th']:7.4f}  {r['obs']:6.3f}   {r['pull']:+5.2f}")
NUM["growth"] = {"sigma8_cH": S8_A, "sigma8_pointwise": S8_B, "sigma8_inert": S8_inert,
                 "D1_inert": float(D_i[-1]), "D1_cH": float(D_a[-1]),
                 "D1_pointwise": float(D_b[-1]), "D1_LCDM": D_LCDM,
                 "f0_inert": float(f_i[-1]), "f0_cH": float(f_a[-1]),
                 "chi2_inert": chi2_v, "chi2_cH": chi2_a, "chi2_LCDM": chi2_L,
                 "fs8_rows_inert": rows_v}

tab = {}
for z in Z_REQ:
    tab[z] = {"f": f_at(z, x_v, f_v), "s8": s8_at(z, S8_V, x_v, D_v),
              "fs8": f_at(z, x_v, f_v) * s8_at(z, S8_V, x_v, D_v)}
print("      verdict branch: " + " | ".join(
    f"z={z}: f={tab[z]['f']:.4f} s8={tab[z]['s8']:.4f} fs8={tab[z]['fs8']:.4f}" for z in Z_REQ[:3]))
NUM["fs8_table_verdict"] = {str(z): tab[z] for z in Z_REQ}

# =====================================================================================
# 4.  TASK 2 -- THE BOUND-SYSTEM READING: switch on above delta_c
# =====================================================================================
banner("4.  THE BOUND-SYSTEM READING: modification OFF below delta_c, ON above it")


def sigma8_with_cut(dc, n=4000, tol=2e-5, maxit=400, s_init=0.8):
    """Fixed point: G_eff = 1 while delta_8(a) < dc, RESP(g_8/a0) above.
    delta_8(a) = s * D(a)/D(1);  g_8 = (1/2) Om H^2 delta_8 R8  (the 8/h Mpc sphere)."""
    x = np.linspace(X0, 0.0, n)
    ax = np.exp(x)
    s = s_init
    D = D_i
    Dsh = D_i / D_i[-1]
    for _ in range(maxit):
        def rhs(_x, y):
            aa = math.exp(_x)
            om_a = OM_M * aa ** -3.0 / (OM_L_EFF + OM_M * aa ** -3.0)
            d8 = s * float(np.interp(aa, ax, Dsh))
            if d8 < dc:
                ge = 1.0
            else:
                gN = 0.5 * OM_M * H0 ** 2 * aa ** -3.0 * d8 * R8 * Mpc
                ge = float(RESP(gN / A0))
            return [y[1], 1.5 * om_a * ge * y[0] - (2.0 - 1.5 * om_a) * y[1]]
        sol = solve_ivp(rhs, (X0, 0.0), [math.exp(X0), math.exp(X0)], t_eval=x,
                        rtol=1e-9, atol=1e-13, method="DOP853")
        D = sol.y[0]
        Dsh = D / D[-1] if D[-1] > 0 else np.linspace(0, 1, n)
        new = SIG8_PLANCK * float(D[-1]) / D_LCDM
        if not np.isfinite(new) or new > 50:
            return float("inf"), D
        if abs(new - s) / max(new, 1e-30) < tol:
            return new, D
        s = 0.5 * s + 0.5 * new
    return s, D


dc_grid = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.686, 2.5, 4.0]
scan = {}
for dc in dc_grid:
    s, _ = sigma8_with_cut(dc)
    scan[dc] = s
    print(f"      delta_c = {dc:6.3f}   sigma8(0) = {s:8.4f}   "
          f"(offset vs Planck {s-SIG8_PLANCK:+.3f})")

if MUT == "nocut":                # MUTATION: no threshold, the pointwise law everywhere
    dc_star = 0.0
else:
    dc_star = brentq(lambda d: sigma8_with_cut(d)[0] - TARGET, 0.02, 6.0, xtol=1e-4)
s_star, _ = sigma8_with_cut(dc_star)
print(f"      delta_c that gives sigma8 = {TARGET}:  delta_c = {dc_star:.3f}  "
      f"(sigma8 = {s_star:.4f})")

mono = all(scan[dc_grid[i]] >= scan[dc_grid[i + 1]] - 1e-6 for i in range(len(dc_grid) - 1))
check("K14", "the threshold scan is monotone and brackets the target: delta_c(0.832) is well defined",
      f"sigma8: {scan[0.0]:.3f} at delta_c=0, {scan[1.0]:.3f} at 1.0, {scan[1.686]:.3f} at 1.686, "
      f"{scan[4.0]:.3f} at 4.0; delta_c(0.832) = {dc_star:.3f}",
      (MUT == "nocut") or (mono and 0.02 < dc_star < 6.0),
      "monotone decreasing, root in (0.02, 6)",
      "the threshold reading sweeps from the full pointwise law at delta_c -> 0 (sigma8 = 3.35: "
      "worse than A40's 2.267, because RESP ~ delta^-1/2 diverges as delta -> 0 and the 8/h Mpc "
      "mode starts from zero) to the inert branch at delta_c -> infinity. It has one free "
      "parameter and no derivation")

check("K15", "the delta_c that reproduces Planck's sigma8 is BELOW the nonlinear scale",
      f"delta_c(0.832) = {dc_star:.3f};  delta = 1 at 8/h Mpc;  delta_collapse = 1.686;  "
      f"ratio = {dc_star/1.686:.2f};  sigma8 at delta_c = 1.686: {scan[1.686]:.4f}",
      0.1 < dc_star < 1.0, "0.1 < delta_c(0.832) < 1",
      "*** the bound-system reading cannot deliver sigma8 = 0.832. ***  To reach Planck the "
      "modification must switch on in the QUASI-LINEAR regime, at delta ~ 0.5-0.8, a factor "
      "2-3 below the collapse threshold. At the bound-system scale (delta_c = 1.686) the sigma8 "
      "mode never triggers it and the prediction is the inert 0.760, 6.3% low. So 'the law acts "
      "only in bound systems' is consistent with the data but not preferred by them")

check("K16", "at delta_c = 1.686 the modification never fires for the sigma8 mode: sigma8 = inert",
      f"sigma8(delta_c=1.686) = {scan[1.686]:.4f} vs inert {S8_inert:.4f}; "
      f"diff = {scan[1.686]-S8_inert:+.4f}",
      abs(scan[1.686] - S8_inert) < 5e-3, "|diff| < 5e-3",
      "the 8/h Mpc sphere reaches delta = 0.76 at z = 0, so a threshold at 1.686 is never "
      "crossed and the growth is exactly the inert one. The reading is self-consistent and "
      "empty: it converts the fork into a nonlinear-scale statement with no linear signature")

NUM["delta_c"] = {"scan": {str(k): v for k, v in scan.items()}, "delta_c_star": dc_star,
                  "sigma8_at_star": s_star, "target": TARGET,
                  "delta_collapse": 1.686, "delta8_today": S8_inert,
                  "note": "G_eff = 1 for delta_8 < delta_c; full pointwise RESP(g_8/a0) above"}

# =====================================================================================
# 5.  TASK 3 -- THE FILTERED FIELD
# =====================================================================================
banner("5.  THE FILTERED FIELD: g_N smoothed on the scale R(a0) where <g_R> = a0")

NS = 0.965


def transfer_EH98(k, om=OM_M, h=0.674, Tcmb=2.7255):
    """Eisenstein & Hu 1998 no-wiggle, zero-baryon: T(q) = L/(L + C q^2),
    L = ln(2e + 1.8q), C = 14.2 + 731/(1+62.5q), q = k theta^2/Gamma, k in Mpc^-1."""
    th = Tcmb / 2.7
    Gam = om * h
    q = k * th ** 2 / Gam
    L = np.log(2 * math.e + 1.8 * q)
    C = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L / (L + C * q * q)


LK = np.linspace(math.log(1e-5), math.log(3e2), 40000)
KK = np.exp(LK)
D2_RAW = KK ** (3.0 + NS) * transfer_EH98(KK) ** 2


def _win(Rmpc):
    xr = KK * Rmpc
    W = 3.0 * (np.sin(xr) - xr * np.cos(xr)) / np.where(xr > 0, xr ** 3, 1.0)
    return np.where(xr < 1e-8, 1.0, W)


NORM8 = float(np.trapz(D2_RAW * _win(R8) ** 2, LK))     # sigma(8/h) = 1 units


def sigma_R(Rmpc):
    """rms of the linear density field in a top-hat of radius R [Mpc], sigma(8/h) = 1."""
    return math.sqrt(float(np.trapz(D2_RAW * _win(Rmpc) ** 2, LK)) / NORM8)


def sigR(R):
    return SIG8_PLANCK * sigma_R(R)


AMP = SIG8_PLANCK ** 2 / NORM8
D2_N = AMP * D2_RAW
k_nl = float(np.interp(1.0, D2_N, KK)) / 0.674          # h/Mpc, D2_N is monotone in k
print(f"      sigma(R): R=8/h Mpc {sigR(R8):.4f}; R=1 Mpc {sigR(1.0):.2f}; "
      f"R=10 Mpc {sigR(10.0):.3f}; R=100 Mpc {sigR(100.0):.4f};  k_NL = {k_nl:.3f} h/Mpc")
mono_R = all(sigR(a) > sigR(b) for a, b in zip([1, 5, 20, 60], [5, 20, 60, 200]))
check("K17", "the transfer function gives the Planck shape: k_NL and sigma(R) where they should be",
      f"sigma(1 Mpc) = {sigR(1.0):.2f}, sigma(10 Mpc) = {sigR(10.0):.3f}, "
      f"sigma(100 Mpc) = {sigR(100.0):.4f}, k_NL = {k_nl:.3f} h/Mpc; monotone = {mono_R}",
      abs(sigR(R8) - SIG8_PLANCK) < 1e-9 and 3 < sigR(1.0) < 8
      and 0.05 < sigR(100.0) < 0.15 and 0.12 < k_nl < 0.35 and mono_R,
      "3 < sigma(1 Mpc) < 8; 0.05 < sigma(100 Mpc) < 0.15; 0.12 < k_NL < 0.35 h/Mpc; monotone",
      "EH98 no-wiggle (zero-baryon), n_s = 0.965, amplitude fixed by the same Planck anchor A40 "
      "uses. k_NL = 0.22 h/Mpc is the standard Planck value, which calibrates the shape. The "
      "shape is only needed at the few-% level: the conclusion below is a factor 479")

RR = np.logspace(-3, 4, 400)          # Mpc
gR = np.array([0.5 * OM_M * H0 ** 2 * sigR(r) * r * Mpc for r in RR])
imax = int(np.argmax(gR))
print(f"      linear field: max_R g_R = {gR[imax]:.3e} m/s^2 = {gR[imax]/A0:.4f} a0 "
      f"at R = {RR[imax]:.2f} Mpc")
check("K18", "NO linear scale reaches a0: the filter scale R(a0) does not exist in the linear field",
      f"max g_R/a0 = {gR[imax]/A0:.4f} at R = {RR[imax]:.1f} Mpc; shortfall = {A0/gR[imax]:.0f}x",
      gR[imax] < A0, "max g_R < a0",
      "*** a0 is not a cosmic acceleration. ***  The rms smoothed linear field peaks at "
      "R ~ 20 Mpc at 0.21% of a0; at every other scale it is smaller (0.18% even at 100 Mpc, "
      "because sigma(R) R is almost flat past the turnover). There is no R "
      "at which 'the mean smoothed field equals a0' in the linear universe. Whatever sets the "
      "MOND transition in cosmology, it is not a linear smoothing of the density field")

GR = np.array([float(RESP(max(g, 1e-300) / A0)) for g in gR])
print(f"      forcing the filter on the linear field: G_eff/G in [{GR.min():.1f}, {GR.max():.1f}] "
      f"(deep MOND at every R)")
check("K19", "the filter on the LINEAR field does not rescue growth: G_eff ~ 11-15 at every R",
      f"G_eff/G in [{GR.min():.1f}, {GR.max():.1f}] for R in [1 kpc, 10 Gpc] -> "
      f"sigma8 ~ {S8_B:.2f}",
      GR.min() > 3.0, "G_eff > 3 at every linear scale",
      "smoothing a linear mode does not reduce its field: a 15 kpc filter applied to a 100 Mpc "
      "mode returns the mode's own field. So the filtered reading at linear scales IS branch "
      "(b); the filter changes nothing. This is the check that kills the naive 'environmental' "
      "rescue of linear growth")


def r_mond(v_kms):
    """r at which an isothermal halo of circular speed v has g = 2 sigma^2/r = a0."""
    return 2.0 * (v_kms * 1e3) ** 2 / A0


print("      nonlinear field: R(a0) from an isothermal halo with g = 2 sigma^2/r = a0:")
for v in (50.0, 100.0, 200.0, 300.0):
    print(f"        v_c = {v:5.1f} km/s -> R(a0) = {r_mond(v)/pc:8.1f} pc "
          f"= {r_mond(v)/pc/1e3:6.2f} kpc ;  k(a0) = {Mpc/(r_mond(v))/0.674:8.1f} h/Mpc")
R_A0 = r_mond(150.0)
k_A0 = Mpc / R_A0 / 0.674
check("K20", "R(a0) exists only in the NONLINEAR field, at galaxy radii: k(a0) ~ 1e2 h/Mpc",
      f"R(a0) = {R_A0/pc:.0f} pc for v_c = 150 km/s (range {r_mond(50)/pc:.0f}-"
      f"{r_mond(300)/pc:.0f} pc); k(a0) = {k_A0:.0f} h/Mpc",
      1e1 < k_A0 < 1e4, "k(a0) in [10, 1e4] h/Mpc",
      "the a0 transition happens where the field really is a0, and that is inside galaxies: "
      "R(a0) = 2 sigma^2/a0 = 1.4-52 kpc for v_c = 50-300 km/s. Hence k(a0) = 29-1037 h/Mpc, "
      "two to four decades above every linear scale (k <~ 0.2 h/Mpc). The modification is a sub-grid, "
      "object-by-object effect; the PM engine CFG960 applies it exactly this way "
      "(y = G M_b(<r)/r^2 at the local r)")

check("K21", "the filtered reading's growth prediction: G_eff = 1 on all linear scales",
      f"sigma8(0) = {S8_inert:.4f} (adopted {S8_V:.4f}); f(0) = {float(f_i[-1]):.5f}; "
      f"1/R(a0) = {k_A0:.0f} h/Mpc vs k_lin <= 0.2 h/Mpc",
      abs(S8_V - S8_inert) < 1e-6, "adopted == G_eff=1 to 1e-6",
      "the filtered and the inert branch coincide: both are GR on the theory's background, "
      "because the only places the filtered field reaches a0 are k ~ 1e2 h/Mpc, where the "
      "linear growth equation is not the right description anyway. sigma8 = 0.760, and f(z) is "
      "the LCDM shape on the theory's background")

NUM["filter"] = {"R8_Mpc": R8, "sigma_R8": sigR(R8), "sigma_1Mpc": sigR(1.0),
                 "sigma_100Mpc": sigR(100.0), "max_gR_ms2": float(gR[imax]),
                 "max_gR_over_a0": float(gR[imax] / A0), "R_at_max_Mpc": float(RR[imax]),
                 "shortfall": float(A0 / gR[imax]), "G_eff_linear_min": float(GR.min()),
                 "G_eff_linear_max": float(GR.max()),
                 "R_a0_pc_150kms": R_A0 / pc, "k_a0_hMpc": k_A0,
                 "R_a0_pc_range": [r_mond(50) / pc, r_mond(300) / pc],
                 "sigma8_filtered": S8_inert, "sigma8_if_forced_linear": S8_B}

# =====================================================================================
# 6.  THE DISCRIMINATORS
# =====================================================================================
banner("6.  WHAT DISCRIMINATES THE READINGS")


def sig_R_scale(R, n_eff=-2.4):
    return SIG8_PLANCK * (R / R8) ** (-(3.0 + n_eff) / 2.0)


gk = {}
for kh in (0.05, 0.2):
    Rk = (1.0 / kh) / 0.674
    gN = 0.5 * OM_M * H0 ** 2 * sig_R_scale(Rk) * Rk * Mpc
    gk[kh] = float(RESP(gN / A0))
check("K22", "branch (b) is BLUE (G_eff varies 30% across the linear range); the filtered reading is not",
      f"G_eff(0.05)/G_eff(0.2): pointwise {gk[0.05]/gk[0.2]:.3f}; filtered 1.000; inert 1.000",
      (MUT == "pointwise") or abs(gk[0.05] / gk[0.2] - 0.63) < 0.15,
      "ratio ~ 0.63 for (b), 1 for filtered",
      "the scale dependence is the cleanest discriminator: branch (b) boosts 5 h^-1 Mpc 60% more "
      "than 20 h^-1 Mpc; the filtered and inert readings are exactly scale-free. Measuring "
      "f sigma8 at two k at one z decides it, and so does the shape of P(k) at 0.05-0.3 h/Mpc")


def n_ratio(s8a, s8b, sig_M_over_s8=0.49, dc=1.686):
    """Ratio of the number density of M = 1e15 Msun clusters: exp(-dc^2/2sigma^2), sigma = 0.49 s8."""
    sa, sb = sig_M_over_s8 * s8a, sig_M_over_s8 * s8b
    return math.exp(-dc ** 2 / (2 * sb ** 2)) / math.exp(-dc ** 2 / (2 * sa ** 2))


ratio_cl = n_ratio(S8_inert, S8_B)
check("K23", "the amplitude discriminator: branch (b) over-produces 1e15 Msun clusters by ~1e3",
      f"N(1e15)|(b)/N(1e15)|(inert) = {ratio_cl:.0f} at z = 0; sigma8: {S8_B:.2f} vs {S8_inert:.2f}",
      ratio_cl > 100, "> 100",
      "sigma8 = 2.267 is not a 6% effect: with sigma(M) ~ 0.49 sigma8, exp(-delta_c^2/2sigma^2) "
      "changes by ~3 orders of magnitude at the cluster scale. Branch (b) is excluded by "
      "cluster counts alone, independently of any growth-rate measurement")

f0_L = float(f_l[-1])
check("K24", "the prediction is distinguishable from LCDM through the BACKGROUND, not through a0",
      f"f(0) = {float(f_i[-1]):.4f} (theory) vs {f0_L:.4f} (flat LCDM); "
      f"{100*(float(f_i[-1])/f0_L-1):+.1f}%; sigma8 = {S8_inert:.4f} vs {SIG8_PLANCK:.3f}",
      abs(float(f_i[-1]) / f0_L - 1) > 0.10, "|f(0) difference| > 10%",
      "on the literal beta = 0 background the growth rate is 14% below LCDM's at z = 0 and "
      "sigma8 is 6.3% low. That is the theory's real growth signature -- a background effect "
      "(H(0) = 77.3, Omega_m(a=1) = 0.2403), not an a0 effect. Testable with DESI DR2 at "
      "z < 0.6 where the errors are 1-2%")

NUM["discriminators"] = {"G_eff_k_ratio_pointwise": gk[0.05] / gk[0.2],
                         "G_eff_k": {str(k): v for k, v in gk.items()},
                         "cluster_ratio_b_over_inert": ratio_cl,
                         "f0_theory": float(f_i[-1]), "f0_LCDM": f0_L,
                         "sigma8_pulls": {
                             "pointwise": (S8_B - SIG8_PLANCK) / SIG8_PLANCK_ERR,
                             "cH": (S8_A - SIG8_PLANCK) / SIG8_PLANCK_ERR,
                             "inert": (S8_inert - SIG8_PLANCK) / SIG8_PLANCK_ERR,
                             "delta_c_star": (s_star - SIG8_PLANCK) / SIG8_PLANCK_ERR},
                         "S8_lagrangian_Om": {k: v * math.sqrt(OM_M / 0.3)
                                              for k, v in (("pointwise", S8_B),
                                                           ("cH", S8_A),
                                                           ("inert", S8_inert))}}

# =====================================================================================
# 7.  SUMMARY
# =====================================================================================
banner("7.  SUMMARY")
print(f"  algebra          : g_N = u^2/(a0(1-u/a0)); nu = a0/u; inverse is a square root")
print(f"  coefficient      : delta P_i = grad(delta Phi)/K * 1/(1+(k lambda_P)^2); "
      f"(k lambda_P)^2 = {gamk2_over_K:.1e} at 0.1 h/Mpc")
print(f"  linear order     : G_eff/G = 1+1/(k lambda_P)^2 = 7.6e11 -> k^-4 runaway. No linear eqn")
print(f"  branch (a) cH    : sigma8 = {S8_A:.4f}   [posit: no H anywhere in the action]")
print(f"  branch (b) rms   : sigma8 = {S8_B:.3f}   [resummation; EXCLUDED, "
      f"{(S8_B-SIG8_PLANCK)/SIG8_PLANCK_ERR:.0f} sigma]")
print(f"  inert / filtered : sigma8 = {S8_inert:.4f}   [G_eff = 1 on linear scales; "
      f"{100*(S8_inert/SIG8_PLANCK-1):.1f}% below Planck]")
print(f"  delta_c(0.832)   : {dc_star:.3f}  (delta_collapse = 1.686)")
print(f"  chi2(f sigma8)   : inert {chi2_v:.2f}/8 vs LCDM control {chi2_L:.2f}/8")
print(f"\n  {NP}/{NP+NF} PASS, {NF} FAIL, exit {0 if NF == 0 else 1}, {time.time()-t0:.1f} s")

NUM["meta"] = {"n_pass": NP, "n_fail": NF, "runtime_s": time.time() - t0,
               "mutation": MUT, "a0": A0, "L_star_pc": L_STAR / pc,
               "lambda_P_pc": LAMBDA_P / pc, "Omega_m": OM_M, "H0_kms": H0_kms,
               "Omega_L_eff": OM_L_EFF, "sigma8_anchor": SIG8_PLANCK}
NUM["checks"] = RES
NUM["verdict"] = {
    "reading": "inert at linear order == the filtered/environmental reading in its only consistent form",
    "coefficient_on_grad_dPhi": "1/K (1 in K=1 units), corrected by (k lambda_P)^2 < 1e-11",
    "sigma8_prediction": S8_inert,
    "f_sigma8": "LCDM-shaped on the theory's background; f(0) = %.4f" % float(f_i[-1]),
    "branch_b": S8_B, "branch_a": S8_A, "delta_c_star": dc_star,
    "discriminator": "scale dependence of f sigma8 (b: 0.63 between 0.05 and 0.2 h/Mpc; "
                     "filtered: 1.000) plus cluster abundance (b: x%.0f)" % ratio_cl}

with open(os.path.join(HERE, "a45_results%s.json" % (("_MUTATE_" + MUT) if MUT else "")), "w") as fh:
    json.dump(NUM, fh, indent=1, default=str)
print(f"  wrote a45_results{('_MUTATE_' + MUT) if MUT else ''}.json")
sys.exit(0 if NF == 0 else 1)
