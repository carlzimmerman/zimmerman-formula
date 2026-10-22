#!/usr/bin/env python3
"""
A28_turnoff_origin -- can the turn-off scale y_t = 66.30 be derived from a principle?

Lane A28 of deepseek_push/DS_FINAL_2026_10_21.  Deterministic, no network,
stdlib + numpy/scipy/sympy only.

The closure (A4 eq. 8/15, A25 eq. 1, Zenodo 23171085):

    nu_fix(y) = 1 + (nu_L(y) - 1)/(1 + (y/y_t)^2),     y = g_N/a0
    nu_L(y)   = (1 + sqrt(1 + 4/y))/2                  (Langmuir = canonical law)
    F(Y)      = int_0^inf y (nu_L-1)/(1+(y/Y)^2) dy  =  Lambda c^4 / a0^2

Every candidate principle is converted to a number and tested against the same
target, and against the alt-footing target (a0 = 1.13e-10).

Usage:  python3 a28_checks.py [--mutate=kernel|sat]
Exit 0 iff all declared checks pass (mutations are expected to fail).
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))

MUT = None
for arg in sys.argv[1:]:
    if arg == "--mutate":
        MUT = "kernel"
    elif arg.startswith("--mutate="):
        MUT = arg.split("=", 1)[1]

# ----------------------------------------------------------------------------
# constants (BRIEF section 4; every one is an external input, source labelled)
# ----------------------------------------------------------------------------
C_LIGHT = 2.99792458e8          # m/s        BRIEF 4
G_NEWT = 6.67430e-11            # m^3/kg/s^2 BRIEF 4
H0 = 2.1843e-18                 # 1/s        BRIEF 4 (67.4 km/s/Mpc)
LAMBDA = 1.0890e-52             # m^-2       BRIEF 4
A0_CAN = 9.36e-11               # m/s^2      BRIEF 4
A0_ALT = 1.13e-10               # m/s^2      BRIEF 4
HBAR = 1.054571817e-34          # J s        CODATA 2018 (exact by definition)
KAPPA_CAN = 0.5                 # BRIEF 4
C_CAN = -0.8862943611           # A4 eq. 13 (Richardson-extrapolated closure constant)

RHO_LAMBDA = LAMBDA * C_LIGHT**2 / (8 * math.pi * G_NEWT)
H_LAMBDA = C_LIGHT * math.sqrt(LAMBDA / 3.0)
CH_LAMBDA = C_LIGHT * H_LAMBDA          # = c^2 sqrt(Lambda/3), the vacuum acceleration
Z_CAN = CH_LAMBDA / A0_CAN              # hierarchy cH_Lambda/a0
Z_ALT = CH_LAMBDA / A0_ALT
N_CAN = LAMBDA * C_LIGHT**4 / A0_CAN**2
N_ALT = LAMBDA * C_LIGHT**4 / A0_ALT**2
TARGET_CAN = 66.2999                    # A4/A25, 4-digit target
TARGET_ALT = 46.0148                    # A4 eq. 18

# ----------------------------------------------------------------------------
# kernels and the closure integral
# ----------------------------------------------------------------------------
def h_langmuir(y):
    """y (nu_L - 1) = (sqrt(y^2+4y) - y)/2 ; -> 1 as y -> inf."""
    return 0.5 * (np.sqrt(y * y + 4.0 * y) - y)


def h_quadrature(y):
    """y (nu_Q - 1) = sqrt(y^2+y) - y ; -> 1/2.  Used only by --mutate=kernel."""
    return np.sqrt(y * y + y) - y


H_FUN = h_quadrature if MUT == "kernel" else h_langmuir


def F(Y):
    """F(Y) = int_0^inf h(y)/(1+(y/Y)^2) dy, via y = Y tan(theta)."""
    val, _ = quad(lambda t: H_FUN(Y * math.tan(t)), 0.0, math.pi / 2.0,
                  limit=400, epsabs=1e-13, epsrel=1e-12)
    return Y * val


def F_exact_langmuir(Y):
    """A4 eq. 11: exact rational form, v = sqrt(y^2+4y)-y, v in [0,2]."""
    val, _ = quad(lambda v: v * v * (4.0 - v) /
                  (4.0 * Y * Y * (2.0 - v)**2 + v**4), 0.0, 2.0,
                  limit=400, epsabs=1e-14, epsrel=1e-13)
    return Y * Y * val


def F_asym(Y):
    """A4 eq. 13: (pi/2)Y - ln(Y/4) + C_can + O(1/Y)."""
    return (math.pi / 2.0) * Y - math.log(Y / 4.0) + C_CAN


def root_F(target, lo=0.5, hi=400.0):
    return brentq(lambda Y: F(Y) - target, lo, hi, xtol=1e-12, rtol=1e-14)


Y_CAN = root_F(N_CAN)
Y_ALT = root_F(N_ALT)
Y_32PI = root_F(32 * math.pi)

# ----------------------------------------------------------------------------
# candidate principles
# ----------------------------------------------------------------------------
# (i) SATURATION: A1 section 6.  Elastic medium, modulus mu = rho_L c^2,
#     strain eps = a/(cH_L), cell volume V_cell = (4/3) G hbar/(c^2 H),
#     cell energy E_cell = hbar H/(2 pi).  u V_cell = E_cell  =>  a = sqrt(2) cH.
A_SAT = math.sqrt(2.0) * CH_LAMBDA
Y_SAT = A_SAT / A0_CAN                      # = sqrt(2) Z
Y_SAT_ALT = A_SAT / A0_ALT

# saturation family: the strain reference A in eps = a/A is a free constitutive
# choice; y_t = sqrt(2) A / a0 for each choice.
Y_SAT_FAMILY = {
    "ref=a0": math.sqrt(2.0) * A0_CAN / A0_CAN,
    "ref=sqrt(a0 cH)": math.sqrt(2.0) * math.sqrt(A0_CAN * CH_LAMBDA) / A0_CAN,
    "ref=cH": math.sqrt(2.0) * CH_LAMBDA / A0_CAN,
    "ref=(cH)^2/a0": math.sqrt(2.0) * CH_LAMBDA**2 / A0_CAN / A0_CAN,
}
if MUT == "sat":
    Y_SAT = Y_SAT_FAMILY["ref=(cH)^2/a0"]
    Y_SAT_ALT = Y_SAT * (A0_CAN / A0_ALT)

# (ii) RESPONSE TIME.  Lattice mass action (A2 eq. 7): k_a g (1-theta) = k_d theta,
#      k_d/k_a = a0.  Total exchange rate Gamma = k_a g + k_d = k_d (1 + y).
#      Only the ratio k_d/k_a is fixed; k_d is a free rate -> Gamma = H is one
#      equation in two unknowns.  The only rate the theory can build from the
#      acceleration alone is the Unruh/Rindler frequency omega = a/c:
#      omega = H_L  =>  a = cH_L  =>  y_t = Z.
Y_TIME = CH_LAMBDA / A0_CAN
Y_TIME_2PI = 2.0 * math.pi * CH_LAMBDA / A0_CAN   # Unruh frequency omega = a/(2 pi c)

# (iii) INFORMATION.  Modes per cell with acceleration above a:
#       N(>a) = V_cell (a/c)^3/(6 pi^2).  N = 1  =>  a = c (6 pi^2/V_cell)^{1/3}.
V_CELL = (4.0 / 3.0) * G_NEWT * HBAR / (C_LIGHT**2 * H_LAMBDA)
A_INFO = C_LIGHT * (6.0 * math.pi**2 / V_CELL)**(1.0 / 3.0)
Y_INFO = A_INFO / A0_CAN
Y_INFO_ALT = A_INFO / A0_ALT
N_MODE_AT_TARGET = V_CELL * (TARGET_CAN * A0_CAN / C_LIGHT)**3 / (6 * math.pi**2)

# (iv) SELF-CONSISTENCY.  The medium's description breaks at u -> a0, i.e. y = 1
#      (W'(u) = (u/K)/(1-u/a0) has its pole there).  Cutting the integral at the
#      breakdown gives F(1) -- a prediction for Lambda, not for y_t.
Y_SELF = 1.0
F_SELF = F(1.0)
A0_FROM_SELF = C_LIGHT**2 * math.sqrt(LAMBDA / F_SELF)

# numerology: the only expression in the exercise that lands within 1% on both
# footings -- the square of the saturation ratio.
Y_2Z2 = 2.0 * Z_CAN**2
Y_2Z2_ALT = 2.0 * Z_ALT**2

# implied kappa through the exact equivalence F(y_t) = 8 pi / kappa^2
def kappa_of(y):
    return math.sqrt(8.0 * math.pi / F(y))


CHECKS = []


def check(cid, ok, measured, threshold, note=""):
    CHECKS.append({"id": cid, "pass": bool(ok), "value": measured,
                   "threshold": threshold, "note": note})
    print(f"{cid} {'PASS' if ok else 'FAIL'} {measured} {threshold}"
          + (f"  [{note}]" if note else ""))


# ----------------------------------------------------------------------------
# K1 -- the closure normalization is exactly 8 pi / kappa^2  (sympy, exact)
# ----------------------------------------------------------------------------
Lam_s, c_s, G_s, kap_s = sp.symbols("Lambda c G kappa", positive=True)
rho_s = Lam_s * c_s**2 / (8 * sp.pi * G_s)
a0_s = kap_s * c_s * sp.sqrt(G_s * rho_s)
resid = sp.simplify(Lam_s * c_s**4 / a0_s**2 - 8 * sp.pi / kap_s**2)
Z_s = c_s**2 * sp.sqrt(Lam_s / 3) / a0_s
resid2 = sp.simplify(3 * Z_s**2 - 8 * sp.pi / kap_s**2)
r1 = float(abs(complex(resid)))
r2 = float(abs(complex(resid2)))
check("K1", r1 < 1e-50 and r2 < 1e-50, f"resid={max(r1, r2):.1e}",
      "resid<1e-50", "Lambda c^4/a0^2 = 3Z^2 = 8*pi/kappa^2 exactly")
N_KAPPA_HALF = float(8 * math.pi / 0.25)

# ----------------------------------------------------------------------------
# K2 -- the canonical closure root
# ----------------------------------------------------------------------------
check("K2", abs(Y_CAN - TARGET_CAN) < 5e-4, f"y_t={Y_CAN:.6f}",
      "|y_t-66.2999|<5e-4", "canonical Langmuir root at Lambda c^4/a0^2=100.4058")

# ----------------------------------------------------------------------------
# K3 -- three independent evaluations of the same integral
# ----------------------------------------------------------------------------
f_direct = F(Y_CAN)
f_exact = F_exact_langmuir(Y_CAN)
f_asym = F_asym(Y_CAN)
rel_exact = abs(f_direct - f_exact) / f_direct
rel_asym = abs(f_asym - f_direct) / f_direct
check("K3", rel_exact < 1e-10 and rel_asym < 1e-3,
      f"rel_exact={rel_exact:.2e}, rel_asym={rel_asym:.2e}",
      "rel<1e-10 and rel<1e-3", "quadrature vs exact rational vs asymptotic")

# ----------------------------------------------------------------------------
# K4 -- asymptotic inversion agrees, and the root is unique (F strictly increasing)
# ----------------------------------------------------------------------------
y_asym_inv = (2.0 / math.pi) * (N_CAN + math.log(Y_CAN / 4.0) - C_CAN)
rel_inv = abs(y_asym_inv - Y_CAN) / Y_CAN
grid = np.linspace(0.2, 200.0, 400)
dF = np.array([(F(y + 1e-4) - F(y - 1e-4)) / 2e-4 for y in grid[::20]])
check("K4", rel_inv < 1e-3 and dF.min() > 0,
      f"y_asym={y_asym_inv:.4f}, rel={rel_inv:.2e}, min dF/dy={dF.min():.4f}",
      "rel<1e-3 and dF/dy>0", "inversion of A4 eq. 13; monotone => root unique")

# ----------------------------------------------------------------------------
# K5 -- the framework's own 32 pi target (A25)
# ----------------------------------------------------------------------------
check("K5", abs(Y_32PI - 66.3803) < 5e-4, f"y_t(32pi)={Y_32PI:.6f}",
      "|y_t-66.3803|<5e-4", "32*pi = 3Z^2 at kappa=1/2; 0.121% above the observed-Lambda root")

# ----------------------------------------------------------------------------
# K6 -- alt footing (the free second data point)
# ----------------------------------------------------------------------------
ratio_targets = Y_CAN / Y_ALT
ratio_a0_sq = (A0_ALT / A0_CAN)**2
p_req = 2.0 * (N_CAN / Y_CAN) / (math.pi / 2.0 - 1.0 / Y_CAN)
check("K6", abs(Y_ALT - TARGET_ALT) < 2e-3 and abs(ratio_targets / ratio_a0_sq - 1) < 0.02,
      f"y_t_alt={Y_ALT:.6f}, ratio={ratio_targets:.5f} vs (a0a/a0)^2={ratio_a0_sq:.5f}",
      "|y_t_alt-46.0148|<2e-3", f"required exponent p=dln y/dln Z={p_req:.5f}")

# ----------------------------------------------------------------------------
# K7 -- candidate (i) SATURATION
# ----------------------------------------------------------------------------
err_sat = Y_SAT / Y_CAN - 1.0
resid_sat = Y_CAN / Y_SAT
K_SAT = kappa_of(Y_SAT)
check("K7", abs(Y_SAT - 8.1815) < 1e-3 and abs(err_sat) > 0.5,
      f"y_sat={Y_SAT:.6f}, err={100*err_sat:.2f}%, resid={resid_sat:.5f}",
      "y_sat=8.1815+-1e-3 and |err|>50%",
      f"implied kappa={K_SAT:.5f} (A1 P1: 4.09331)")

# ----------------------------------------------------------------------------
# K8 -- the saturation family spans 1.4..33 and still misses (normalization is free)
# ----------------------------------------------------------------------------
fam = {k: v for k, v in Y_SAT_FAMILY.items()}
fam_ok = all(abs(v / Y_CAN - 1.0) > 0.01 for v in fam.values())
min_err = min(abs(v / Y_CAN - 1.0) for v in fam.values())
check("K8", fam_ok, f"min|err|={100*min_err:.2f}% of {len(fam)} normalizations",
      "all |err|>1%",
      "strain ref a0/sqrt(a0cH)/cH/(cH)^2/a0 -> 1.41/3.40/8.18/47.33")

# ----------------------------------------------------------------------------
# K9 -- candidate (ii) RESPONSE TIME
# ----------------------------------------------------------------------------
err_time = Y_TIME / Y_CAN - 1.0
K_TIME = kappa_of(Y_TIME)
check("K9", abs(Y_TIME - Z_CAN) < 1e-9 and abs(err_time) > 0.5,
      f"y_time=Z={Y_TIME:.6f} (err {100*err_time:.2f}%), 2piZ={Y_TIME_2PI:.5f} "
      f"(err {100*(Y_TIME_2PI/Y_CAN-1):.2f}%), resid={Y_CAN/Y_TIME:.4f}",
      "y_time=Z+-1e-9 and |err|>50%",
      f"Gamma=k_d(1+y) leaves k_d free; Unruh reading; implied kappa={K_TIME:.5f}")

# ----------------------------------------------------------------------------
# K10 -- candidate (iii) INFORMATION
# ----------------------------------------------------------------------------
check("K10", Y_INFO / Y_CAN > 1e30,
      f"y_info={Y_INFO:.4e}, resid={Y_INFO/Y_CAN:.2e}, N(>a_t)={N_MODE_AT_TARGET:.2e}",
      "y_info/y_t>1e30", "one mode per cell needs a=3.02e23 m/s^2")

# ----------------------------------------------------------------------------
# K11 -- candidate (iv) SELF-CONSISTENCY
# ----------------------------------------------------------------------------
check("K11", F_SELF / N_CAN < 0.02 and A0_FROM_SELF / A0_CAN > 5,
      f"F(1)={F_SELF:.5f} vs {N_CAN:.3f}, short by {N_CAN/F_SELF:.2f}x, a0_impl={A0_FROM_SELF:.4e}",
      "F(1)/N<0.02 and a0_impl/a0>5", f"breakdown at y=1; implied a0={A0_FROM_SELF/A0_CAN:.2f} a0")

# ----------------------------------------------------------------------------
# K12 -- the equivalence: y_t is kappa in disguise
# ----------------------------------------------------------------------------
k_obs = math.sqrt(8 * math.pi / N_CAN)
k_root = kappa_of(Y_CAN)
k_32 = kappa_of(Y_32PI)
kk = [kappa_of(y) for y in (0.5, 2.0, 8.18, 66.3)]
monotone = all(kk[i] > kk[i + 1] for i in range(len(kk) - 1))
elasticity = -2.0 * (N_CAN / Y_CAN) / (math.pi / 2.0 - 1.0 / Y_CAN)
check("K12", abs(k_root - k_obs) < 1e-6 and abs(k_32 - 0.5) < 1e-4 and monotone
      and abs(elasticity + 1.9469) < 1e-3,
      f"kappa(y_t)={k_root:.6f} vs sqrt(8pi/N)={k_obs:.6f}; kappa(32pi)={k_32:.6f}; "
      f"dln y/dln kappa={elasticity:.5f}",
      "agree<1e-6, kappa(32pi)=0.5, monotone, elasticity=-1.9469",
      "F(y_t)=8*pi/kappa^2 => y_t and kappa are the same unknown")

# ----------------------------------------------------------------------------
# K13 -- alt-footing discrimination: no candidate is a constant factor away
# ----------------------------------------------------------------------------
drift = {
    "sat": (Y_CAN / Y_SAT) / (Y_ALT / Y_SAT_ALT),
    "time": (Y_CAN / Y_TIME) / (Y_ALT / (CH_LAMBDA / A0_ALT)),
    "info": (Y_CAN / Y_INFO) / (Y_ALT / Y_INFO_ALT),
    "self": (Y_CAN / Y_SELF) / (Y_ALT / Y_SELF),
}
worst = min(abs(v - 1.0) for v in drift.values())
check("K13", worst > 0.15,
      "drift=" + ",".join(f"{k}:{v:.4f}" for k, v in drift.items()),
      "min|drift-1|>0.15", "a constant-factor error needs drift=1")

# ----------------------------------------------------------------------------
# K14 -- numerology control: what a factor 2 / factor pi error gives
# ----------------------------------------------------------------------------
y_half_coef = brentq(lambda Y: (math.pi / 4) * Y - math.log(Y / 4) + C_CAN - N_CAN, 1, 400)
y_dbl_coef = brentq(lambda Y: math.pi * Y - math.log(Y / 4) + C_CAN - N_CAN, 1, 400)
y_nolog = brentq(lambda Y: (math.pi / 2) * Y + C_CAN - N_CAN, 1, 400)
y_noC = brentq(lambda Y: (math.pi / 2) * Y - math.log(Y / 4) - N_CAN, 1, 400)
y_lam_p = root_F(N_CAN * 1.01)
y_lam_m = root_F(N_CAN * 0.99)
y_h0tied = root_F(73.19)
ctrl = {
    "coef/2 -> 2y_t": y_half_coef,
    "coef*2 -> y_t/2": y_dbl_coef,
    "drop log": y_nolog,
    "drop C": y_noC,
    "Lambda+1%": y_lam_p,
    "Lambda-1%": y_lam_m,
    "32pi target": Y_32PI,
    "73.19 (H0-tied)": y_h0tied,
}
check("K14", abs(y_half_coef / Y_CAN - 2) < 0.05 and abs(y_dbl_coef / Y_CAN - 0.5) < 0.05,
      f"half={y_half_coef:.4f} dbl={y_dbl_coef:.4f} nolog={y_nolog:.4f} noC={y_noC:.4f} "
      f"L+1%={y_lam_p:.4f} 32pi={Y_32PI:.4f} 73.19={y_h0tied:.4f}",
      "factor-2 shifts y_t by ~2x", "sensitivity dln y/dln N=0.9735")

# ----------------------------------------------------------------------------
# K15 -- the only sub-1% expression: 2Z^2, the square of the saturation ratio
# ----------------------------------------------------------------------------
err_2z2 = Y_2Z2 / Y_CAN - 1.0
err_2z2_alt = Y_2Z2_ALT / Y_ALT - 1.0
K_2Z2 = kappa_of(Y_2Z2)
strain_2z2 = Y_2Z2 / Z_CAN
check("K15", abs(err_2z2) < 0.01 and abs(err_2z2_alt) < 0.01,
      f"2Z^2={Y_2Z2:.5f} ({100*err_2z2:+.3f}%), alt={Y_2Z2_ALT:.5f} ({100*err_2z2_alt:+.3f}%), "
      f"kappa_impl={K_2Z2:.6f}, strain={strain_2z2:.4f}",
      "|err|<1% both footings",
      "a two-parameter power law, not a principle; strain 11.57 at the turn-off")

# ----------------------------------------------------------------------------
# K16 -- what the saturation candidate predicts besides y_t
# ----------------------------------------------------------------------------
supp_target = 1.0 / (1.0 + (10.0 / Y_CAN)**2)
supp_sat = 1.0 / (1.0 + (10.0 / Y_SAT)**2)
K_P1 = 4.0 * math.sqrt(math.pi / 3.0)
check("K16", supp_sat < 0.5 and supp_target > 0.95,
      f"RAR(y=10): target={supp_target:.5f}, sat={supp_sat:.5f}; a_sat/a0={A_SAT/A0_CAN:.5f}; "
      f"kappa_P1={K_P1:.5f}",
      "supp_sat<0.5 and supp_target>0.95",
      "saturation also fixes a0=7.6579e-10 and kappa_P1=4.0933")

# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------
n_pass = sum(1 for c in CHECKS if c["pass"])
n_tot = len(CHECKS)

NUMBERS = {
    "Lambda_c4_over_a0sq_canonical": N_CAN,
    "Lambda_c4_over_a0sq_alt": N_ALT,
    "kappa_from_observed": k_obs,
    "cH_Lambda": CH_LAMBDA,
    "H_Lambda": H_LAMBDA,
    "Z_canonical": Z_CAN,
    "Z_alt": Z_ALT,
    "y_t_canonical": Y_CAN,
    "y_t_alt": Y_ALT,
    "y_t_32pi": Y_32PI,
    "y_t_asymptotic_inversion": y_asym_inv,
    "y_t_ratio_alt_over_can": ratio_targets,
    "a0_ratio_squared": ratio_a0_sq,
    "required_exponent_p": p_req,
    "F_at_target": f_direct,
    "F_exact_rational": f_exact,
    "F_asymptotic": f_asym,
    "F_prime_at_root": math.pi / 2 - 1 / Y_CAN,
    "sensitivity_dln_y_dln_N": (1.0 / (math.pi / 2 - 1 / Y_CAN)) * N_CAN / Y_CAN,
    "y_t_saturation": Y_SAT,
    "y_t_saturation_error": err_sat,
    "residual_best_candidate": resid_sat,
    "a_sat": A_SAT,
    "a_sat_over_a0": A_SAT / A0_CAN,
    "saturation_family": fam,
    "kappa_implied_saturation": K_SAT,
    "kappa_P1_A1": K_P1,
    "y_t_response_time": Y_TIME,
    "y_t_response_time_2pi": Y_TIME_2PI,
    "dln_y_dln_kappa": elasticity,
    "y_t_response_time_error": err_time,
    "residual_response_time": Y_CAN / Y_TIME,
    "kappa_implied_response": K_TIME,
    "V_cell": V_CELL,
    "ell_cell": V_CELL**(1.0 / 3.0),
    "a_information": A_INFO,
    "y_t_information": Y_INFO,
    "y_t_information_alt": Y_INFO_ALT,
    "N_modes_at_target_per_cell": N_MODE_AT_TARGET,
    "y_t_self_consistency": Y_SELF,
    "F_at_breakdown": F_SELF,
    "Lambda_shortfall_self": N_CAN / F_SELF,
    "a0_implied_self": A0_FROM_SELF,
    "a0_implied_self_over_a0": A0_FROM_SELF / A0_CAN,
    "kappa_implied_self": kappa_of(Y_SELF),
    "kappa_at_target": k_root,
    "kappa_at_32pi": k_32,
    "alt_footing_residual_drift": drift,
    "numerology_control": ctrl,
    "y_t_2Z2": Y_2Z2,
    "y_t_2Z2_error": err_2z2,
    "y_t_2Z2_alt": Y_2Z2_ALT,
    "y_t_2Z2_alt_error": err_2z2_alt,
    "kappa_implied_2Z2": K_2Z2,
    "strain_at_2Z2_turnoff": strain_2z2,
    "strain_at_target_turnoff": Y_CAN / Z_CAN,
    "Estrain_over_Ecell_at_target": (Y_CAN / (math.sqrt(2) * Z_CAN))**2,
    "RAR_suppression_at_y10_target": supp_target,
    "RAR_suppression_at_y10_saturation": supp_sat,
    "E_cell": HBAR * H_LAMBDA / (2 * math.pi),
    "y_t_over_Zsq": Y_CAN / Z_CAN**2,
    "six_over_pi": 6.0 / math.pi,
    "y_t_32pi_shift": Y_32PI / Y_CAN - 1.0,
    "kappa_shift": k_obs / 0.5 - 1.0,
    "a_t_canonical": Y_CAN * A0_CAN,
    "H_inverse": 1.0 / H_LAMBDA,
    "tau_required": 1.0 / (Y_CAN * H_LAMBDA),
    "N_at_32pi": 32 * math.pi,
    "leading_term_six_over_pi_Z2": (6.0 / math.pi) * Z_CAN**2,
    "log_correction": Y_CAN - (6.0 / math.pi) * Z_CAN**2,
    "residual_over_Z_saturation": (Y_CAN / Y_SAT) / Z_CAN,
    "residual_over_Z_response": (Y_CAN / Y_TIME) / Z_CAN,
    "kappa_2Z2_shift": 1.0 - K_2Z2 / 0.5,
    "twoZ2_over_N": Y_2Z2 / N_CAN,
    "min_dF_dy_grid": float(dF.min()),
    "tau_required_Myr": (1.0 / (Y_CAN * H_LAMBDA)) / (365.25 * 24 * 3600) / 1e6,
    "RAR_cost_at_y10_target": 1.0 - supp_target,
    "RAR_cost_at_y10_saturation": 1.0 - supp_sat,
    "F_exact_rel_error": rel_exact,
    "F_asym_rel_error": rel_asym,
    "y_asym_rel_error": rel_inv,
    "y_t_tolerance": 5e-4,
    "K1_residual": max(r1, r2),
    "y_t_saturation_alt": Y_SAT_ALT,
    "info_residual_ratio": Y_INFO / Y_CAN,
    "u_pole_denominator": Y_CAN - 1.0,
    "drift_2Z2": (Y_CAN / Y_2Z2) / (Y_ALT / Y_2Z2_ALT),
    "constants_si": {"a0_can": A0_CAN, "a0_alt": A0_ALT, "Lambda": LAMBDA, "C_can": C_CAN},
    "derived_pct": {
        "y_t_32pi_shift": 100 * (Y_32PI / Y_CAN - 1),
        "kappa_shift": 100 * (k_obs / 0.5 - 1),
        "saturation_error": 100 * err_sat,
        "saturation_alt_error": 100 * (Y_SAT_ALT / Y_ALT - 1),
        "response_error": 100 * err_time,
        "response_2pi_error": 100 * (Y_TIME_2PI / Y_CAN - 1),
        "self_error": 100 * (Y_SELF / Y_CAN - 1),
        "self_alt_error": 100 * (Y_SELF / Y_ALT - 1),
        "response_alt_error": 100 * ((CH_LAMBDA / A0_ALT) / Y_ALT - 1),
        "twoZ2_error": 100 * err_2z2,
        "twoZ2_alt_error": 100 * err_2z2_alt,
        "kappa_2Z2_shift": 100 * (1 - K_2Z2 / 0.5),
        "exponent_shift": 100 * (2.0 / p_req - 1),
        "saturation_family_min_error": 100 * min_err,
        "drift_mismatch_Zlinear": 100 * (drift["sat"] - 1),
        "drift_mismatch_self": 100 * (drift["self"] - 1),
        "coef_half_shift": 100 * (y_half_coef / Y_CAN - 1),
        "coef_double_shift": 100 * (y_dbl_coef / Y_CAN - 1),
        "drop_log_shift": 100 * (y_nolog / Y_CAN - 1),
        "drop_C_shift": 100 * (y_noC / Y_CAN - 1),
        "Lambda_p1_shift": 100 * (y_lam_p / Y_CAN - 1),
        "Lambda_m1_shift": 100 * (y_lam_m / Y_CAN - 1),
        "h0tied_shift": 100 * (y_h0tied / Y_CAN - 1),
        "RAR_cost_target": 100 * (1 - supp_target),
        "RAR_cost_saturation": 100 * (1 - supp_sat),
    },
    "rho_Lambda": RHO_LAMBDA,
    "a0_exact_from_kappa_half": C_LIGHT**2 * math.sqrt(LAMBDA / (32 * math.pi)),
}

RESULTS = {
    "lane": "A28_turnoff_origin",
    "status": "NO-GO(obstruction)",
    "checks": CHECKS,
    "numbers": NUMBERS,
    "external_inputs": {
        "B_E_earth_ephemeris_bound_m_s2": 3.66e-14,
        "canonical_anomaly_over_B_E": 2557.38,
        "quadrature_band_normalization_check": 1.00191,
        "y_t_at_73.19_H0_tied": 73.19,
        "y_t_32pi": 32 * math.pi,
        "planetary_cap_y_t": 605.96,
        "A1_dimensionless_invariant_hbar_G_Lambda_over_c3": 2.8448e-122,
        "A25_SPARC_dchi2_for_yt_48_79": 0.060,
        "quadrature_band_agreement_pct": 0.19,
        "planetary_yt_margin": 9.14,
        "A1_analytic_constancy_digits": 122,
    },
    "constants_used": [
        "c = 2.99792458e8 m/s (BRIEF 4)",
        "G = 6.67430e-11 (BRIEF 4)",
        "H0 = 2.1843e-18 1/s (BRIEF 4)",
        "Lambda = 1.0890e-52 m^-2 (BRIEF 4)",
        "a0_can = 9.36e-11 m/s^2 (BRIEF 4)",
        "a0_alt = 1.13e-10 m/s^2 (BRIEF 4)",
        "hbar = 1.054571817e-34 J s (CODATA 2018)",
        "kappa_can = 0.5 (BRIEF 4)",
        "C_can = -0.8862943611 (A4 eq. 13)",
        "targets y_t = 66.2999 / 66.3803 / 46.0148 (A4, A25)",
    ],
}

out_json = "a28_results_mutated.json" if MUT else "a28_results.json"
with open(os.path.join(HERE, out_json), "w") as fh:
    json.dump(RESULTS, fh, indent=2, default=float)

print()
if MUT:
    print(f"MUTATION CONFIRMED ({MUT}): {n_tot - n_pass}/{n_tot} checks broken.")
else:
    print(f"A28 COMPLETE: {n_pass}/{n_tot} checks PASS.")

sys.exit(0 if (n_pass == n_tot and not MUT) else 1)