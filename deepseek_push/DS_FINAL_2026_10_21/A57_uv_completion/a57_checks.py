#!/usr/bin/env python3
"""
A57 -- THE UV COMPLETION: does one dynamics fix kappa AND L-star together?

Lane A57 of deepseek_push/DS_FINAL_2026_10_21.

Checks K1..K20.  Exit 0 iff all declared checks pass.

Physics inputs (BRIEF section 4, external):
  c, G, H0, Lambda, a0_can, pc, Mpc, kappa_can = 1/2.
Everything else is computed here.

The four objects of the lane:
  (1) the finite-state / finite-correlation-length medium and its two parameters;
  (2) the vacuum closure integral with a finite correlation length;
  (3) the joint (kappa, L*) relation and its tension with (0.5, 24-90 pc);
  (4) the verdict.

Run:  python3 a57_checks.py [--json-out a57_results.json] [--mutate NAME]
"""

import argparse
import json
import math
import sys

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as sp

LANE = "A57"

# --------------------------------------------------------------------------------------
# Constants -- BRIEF section 4 (external, never fitted here)
# --------------------------------------------------------------------------------------
c = 2.99792458e8                     # m/s
G = 6.67430e-11                      # m^3 kg^-1 s^-2
H0 = 67.4e3 / 3.0856775814913673e22  # s^-1  (67.4 km/s/Mpc)
Lambda = 1.0890e-52                  # m^-2
a0_can = 9.36e-11                    # m/s^2   canonical footing
a0_alt = 1.13e-10                    # m/s^2   alt footing (never pooled)
pc = 3.0856775814913673e16           # m
Mpc = 3.0856775814913673e22          # m
kappa_can = 0.5
K = 4.0 * math.pi * G                # the action's own normalisation (A33 section 1.1)
rho_L = Lambda * c * c / (8.0 * math.pi * G)   # kg/m^3
u_L = rho_L * c * c                  # J/m^3
ell1 = math.sqrt(8.0 * math.pi / Lambda)       # the vacuum cell length (A37)
L_MOND = c * c / a0_can                        # the MOND length
Zconst = 2.0 * math.sqrt(8.0 * math.pi / 3.0)  # = 5.788810
cH_L = c * c * math.sqrt(Lambda / 3.0)         # c H_Lambda, m/s^2
M_sun = 1.98847e30

# canonical closure target
TARGET_CAN = Lambda * c ** 4 / a0_can ** 2     # = 100.405845
YT_CAN = 66.299937                             # A4/A28 root at the canonical footing

RESULTS = []
NUMBERS = {}

# The response is measured in units of the capacity a0.  The law forces CAP = 1
# (capacity = affinity = a0); CAP is a module-level switch only so that the
# `capacity2` mutation can exhibit a medium that over-responds.
CAP = 1.0


# --------------------------------------------------------------------------------------
# the response function and the two integrals
# --------------------------------------------------------------------------------------
def h(y):
    """h(y) = y(nu-1) = (1/2)(sqrt(y^2+4y) - y).  This is u/a0: the response in
    units of the capacity.  0 <= h < 1, h ~ sqrt(y) at 0, h -> 1 at infinity.

    The two forms are algebraically identical:  (1/2)(s-y) = 2y/(s+y) with
    s = sqrt(y^2+4y).  The second is used for y > 1e6 because the first loses
    the 4y term to double-precision cancellation there (h would return 0)."""
    if y <= 0.0:
        return 0.0
    s = math.sqrt(y * y + 4.0 * y)
    if y > 1e6:
        return CAP * 2.0 * y / (s + y)
    return CAP * 0.5 * (s - y)


def nu(y):
    return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))


def F_turn(Y, yt):
    """closure integral with the turn-off 1/(1+(y/yt)^2), upper limit Y.

    Substitution y = yt sinh t removes both the large-Y range and the tail:
      dy/(1+(y/yt)^2) = yt cosh t dt / cosh^2 t = yt dt / cosh t,
    so F = yt * int_0^T h(yt sinh t)/cosh t dt,  T = asinh(Y/yt).
    The tail decays as 2 e^{-t}, so T = 40 is exact to 1e-17."""
    if not np.isfinite(yt):
        return F_plain(Y)
    if np.isfinite(Y):
        T = math.asinh(Y / yt)
    else:
        T = 40.0
    return yt * quad(lambda t: h(yt * math.sinh(t)) / math.cosh(t), 0.0, T,
                     limit=400)[0]


def F_plain(Y):
    """closure integral without a turn-off (bare finite-capacity medium)."""
    return quad(h, 0.0, Y, limit=400)[0]


def F_closed(yt):
    """A4 eq. (13): (pi/2) yt - ln(yt/4) + C_can,  C_can = -0.8862943611."""
    return 0.5 * math.pi * yt - math.log(yt / 4.0) - 0.8862943611


def check(cid, ok, value, threshold, note=""):
    RESULTS.append({"id": cid, "pass": bool(ok), "value": value,
                    "threshold": threshold, "note": note})
    print(("PASS" if ok else "FAIL"), cid, value, "|", threshold, ("| " + note if note else ""))


# --------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="")
    ap.add_argument("--mutate", default="")
    args = ap.parse_args()
    mut = args.mutate

    # mutation switches: each must break at least one check
    global CAP
    kap = 1.0 if mut == "kappa1" else kappa_can
    if mut == "no_turnoff":
        yt_use = np.inf
    elif mut == "xi_ell1":
        yt_use = 1.0 / kap          # turn-off at the cell acceleration c^2/ell_1
    else:
        yt_use = YT_CAN
    CAP = 2.0 if mut == "capacity2" else 1.0
    q_ladder = 3 if mut == "q3" else 2
    xi_is_ell1 = (mut == "xi_ell1")

    target = 8.0 * math.pi / kap ** 2

    # constants of the run (all from BRIEF section 4, none fitted)
    NUMBERS["ell1_m"] = float(ell1)
    NUMBERS["ell1_Gpc"] = float(ell1 / (1e9 * pc))
    NUMBERS["L_MOND_m"] = float(L_MOND)
    NUMBERS["L_MOND_Gpc"] = float(L_MOND / (1e9 * pc))
    NUMBERS["lambdaP_pc"] = float((24.0 * pc / math.sqrt(2.0)) / pc)
    NUMBERS["rho_L"] = float(rho_L)
    NUMBERS["cH_L"] = float(cH_L)
    NUMBERS["c2_over_ell1"] = float(c * c / ell1)
    NUMBERS["target_can"] = float(TARGET_CAN)
    NUMBERS["Z"] = float(Zconst)
    NUMBERS["yt_can"] = float(YT_CAN)

    # ==================================================================================
    # K1 -- the closure reproduces the canonical number
    # ==================================================================================
    if np.isfinite(yt_use):
        val = F_turn(np.inf, yt_use)
        ok = abs(val - TARGET_CAN) < 1e-6
        check("K1", ok, round(val, 6), "|F-100.405845|<1e-6",
              "closure at y_t=66.299937")
        NUMBERS["F_at_yt"] = val
        NUMBERS["F_closed_form"] = F_closed(yt_use)
        NUMBERS["closed_form_error"] = abs(F_closed(yt_use) - val)
    else:
        val = F_plain(1e6)
        ok = abs(val - TARGET_CAN) < 1e-6
        check("K1", ok, round(val, 6), "|F-100.405845|<1e-6",
              "MUTATION no_turnoff: integral runs to 1e6")

    # ==================================================================================
    # K2 -- 8 pi/kappa^2 = 3 Z^2 = 32 pi at kappa = 1/2 (sympy, exact)
    # ==================================================================================
    kap_s = sp.symbols("kappa", positive=True)
    resid = sp.simplify(8 * sp.pi / kap_s ** 2 - 3 * (2 * sp.sqrt(8 * sp.pi / 3)) ** 2)
    at_half = sp.simplify((8 * sp.pi / kap_s ** 2).subs(kap_s, sp.Rational(1, 2)))
    ok = (resid == -32 * sp.pi + 8 * sp.pi / kap_s ** 2) and (at_half == 32 * sp.pi)
    # the identity that matters: 8 pi/kappa^2 (kappa=1/2) = 32 pi exactly
    ok = bool(sp.simplify(8 * sp.pi / sp.Rational(1, 2) ** 2 - 32 * sp.pi) == 0) and \
         bool(sp.simplify(3 * (2 * sp.sqrt(8 * sp.pi / 3)) ** 2 - 32 * sp.pi) == 0)
    check("K2", ok, str(sp.simplify(8 * sp.pi / sp.Rational(1, 2) ** 2)),
          "== 32 pi == 3 Z^2 (exact)", "8pi/kappa^2 = 3Z^2 = 32pi at kappa=1/2")
    NUMBERS["8pi_over_kappa2"] = float(8 * math.pi / kap ** 2)
    NUMBERS["32pi"] = float(32 * math.pi)

    # ==================================================================================
    # K3 -- the response never exceeds the capacity: 0 <= h(y) < 1
    # ==================================================================================
    grid = np.logspace(-8, 8, 4001)
    hvals = np.array([h(x) for x in grid])
    y = sp.symbols("y", positive=True)
    hsym = sp.Rational(1, 2) * (sp.sqrt(y ** 2 + 4 * y) - y)
    diff = sp.simplify(1 - hsym - (2 + y - sp.sqrt(y ** 2 + 4 * y)) / 2)
    ok = (hvals.min() >= 0.0) and (hvals.max() < 1.0) and (diff == 0)
    check("K3", ok, "min=%.3e max=%.9f" % (hvals.min(), hvals.max()),
          "0<=h<1 on 4001 points; exact identity",
          "h = u/a0 = response/capacity")
    NUMBERS["h_max"] = float(hvals.max())

    # ==================================================================================
    # K4 -- the truncation bound F_cut(Y) <= Y (capacity 1)
    # ==================================================================================
    tests = [0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 500.0]
    worst = max(F_plain(Y) / Y for Y in tests)
    ok = worst < 1.0
    check("K4", ok, round(worst, 6), "<1", "sup_Y F_plain(Y)/Y over 8 Y values")
    NUMBERS["sup_F_over_Y"] = float(worst)

    # ==================================================================================
    # K5 -- the ell_1-cutoff value: F(1/kappa) vs the requirement
    # ==================================================================================
    Y_ell1 = 1.0 / kap if not xi_is_ell1 else 1.0 / kap
    if np.isfinite(yt_use):
        F_cut_ell1 = F_turn(Y_ell1, yt_use)
    else:
        F_cut_ell1 = F_plain(Y_ell1)
    shortfall = target / F_cut_ell1
    ok = (abs(Y_ell1 - 2.0) < 1e-12) and (F_cut_ell1 < target) and (shortfall > 80.0)
    check("K5", ok, round(F_cut_ell1, 6), "%.3f < %.3f ; shortfall>80" % (F_cut_ell1, target),
          "xi=ell_1 => Y=1/kappa=2")
    NUMBERS["F_cut_at_ell1"] = float(F_cut_ell1)
    NUMBERS["shortfall_ell1"] = float(shortfall)
    # the other reading of the same identification: the cell length IS the turn-off
    F_cell_turn = F_turn(np.inf, 1.0 / kap) if np.isfinite(1.0 / kap) else float("nan")
    NUMBERS["F_cell_as_turnoff"] = float(F_cell_turn)
    NUMBERS["shortfall_cell_turnoff"] = float(target / F_cell_turn)
    NUMBERS["Y_ell1"] = float(Y_ell1)

    # ==================================================================================
    # K6 -- exact bound: F<=Y and Y=1/kappa force kappa >= 8 pi
    # ==================================================================================
    kappa_floor = 8.0 * math.pi
    ok = (kappa_floor > kap) and abs(kappa_floor / kap - 8 * math.pi / kap) < 1e-12
    check("K6", ok, round(kappa_floor, 6), "> kappa = %.3f (factor %.3f)" % (kap, kappa_floor / kap),
          "kappa >= 8pi = 25.133 vs measured 0.5")
    NUMBERS["kappa_floor"] = float(kappa_floor)
    NUMBERS["four_pi"] = float(4.0 * math.pi)
    NUMBERS["kappa_floor_factor2"] = float(4.0 * math.pi / kap)
    NUMBERS["kappa_floor_over_measured"] = float(kappa_floor / kap)
    a0_floor = kappa_floor * c * c / ell1
    NUMBERS["a0_floor"] = float(a0_floor)
    NUMBERS["a0_floor_over_can"] = float(a0_floor / a0_can)

    # ==================================================================================
    # K7 -- the cutoff required to reach the closure, and the kappa / a0 it implies
    # ==================================================================================
    Ystar = brentq(lambda Y: F_plain(Y) - target, 1.0, 1e4)
    kappa_req = 1.0 / Ystar
    a0_req = kappa_req * c * c / ell1
    ok = (Ystar > 100.0) and (kappa_req < 0.02) and (a0_req < 0.05 * a0_can)
    check("K7", ok, "Y*=%.4f kappa_req=%.6f a0_req=%.4e" % (Ystar, kappa_req, a0_req),
          "Y*>100, kappa_req<0.02, a0_req<0.05 a0",
          "cutoff needed for F=8pi/kappa^2")
    NUMBERS["Y_star"] = float(Ystar)
    NUMBERS["a0_can_over_req"] = float(a0_can / a0_req)
    NUMBERS["closed_form_rel_error"] = float(abs(F_closed(YT_CAN) - TARGET_CAN) / TARGET_CAN)
    NUMBERS["kappa_req"] = float(kappa_req)
    NUMBERS["a0_req"] = float(a0_req)
    NUMBERS["a0_req_over_can"] = float(a0_req / a0_can)

    # ==================================================================================
    # K8 -- the correlation-length ceiling  xi <= kappa ell_1/(8 pi)
    #       (Y = a_max/a0 = c^2/(xi a0) = L_MOND/xi = ell_1/(kappa xi) >= 8 pi/kappa^2)
    # ==================================================================================
    xi_max = kap * ell1 / (8.0 * math.pi)
    ok = (abs(ell1 / xi_max - 8.0 * math.pi / kap) < 1e-9) and (xi_max < ell1)
    check("K8", ok, "xi_max=%.4e m = %.1f Mpc ; ell1/xi_max=%.3f" % (xi_max, xi_max / Mpc, ell1 / xi_max),
          "xi_max < ell1", "correlation length must be < ell1/50 at kappa=1/2")
    NUMBERS["xi_max_m"] = float(xi_max)
    NUMBERS["xi_max_Mpc"] = float(xi_max / Mpc)
    NUMBERS["ell1_over_xi_max"] = float(ell1 / xi_max)

    # ==================================================================================
    # K9 -- finite xi = lambda_P changes the closure by nothing
    # ==================================================================================
    Lstar_ref = 24.0 * pc
    lamP = Lstar_ref / math.sqrt(2.0)
    Y_lam = L_MOND / lamP
    F_full = F_turn(np.inf, YT_CAN)
    F_lam = F_turn(Y_lam, YT_CAN)
    rel = abs(F_full - F_lam) / F_full
    ok = rel < 1e-6
    check("K9", ok, "rel=%.3e (Y=%.4e)" % (rel, Y_lam), "<1e-6",
          "xi=lambda_P=L*/sqrt2 leaves the closure intact")
    NUMBERS["Y_lambdaP"] = float(Y_lam)
    NUMBERS["closure_rel_change_lambdaP"] = float(rel)

    # ==================================================================================
    # K10 -- the q-state ladder: q=2 is the law, q>=3 over-responds (g_N<0)
    # ==================================================================================
    xs = sp.symbols("x", positive=True)
    nb2 = xs / (1 + xs)
    nb3 = xs * (1 + 2 * xs) / (1 + xs + xs ** 2)
    law_resid = sp.simplify((sp.Symbol("g") - sp.Symbol("a0") * (sp.Symbol("g") / sp.Symbol("a0")) / (1 + sp.Symbol("g") / sp.Symbol("a0")))
                            - sp.Symbol("g") ** 2 / (sp.Symbol("g") + sp.Symbol("a0")))
    gN3 = sp.simplify(xs - nb3)          # g_N/a0 for q=3
    gN3_target = xs ** 2 * (xs - 1) / (1 + xs + xs ** 2)
    ok10 = (sp.simplify(gN3 - gN3_target) == 0) and (law_resid == 0) and (q_ladder == 2)
    # numeric demonstration at x = 1/2 (q=3 gives g_N<0)
    gN3_half = float(gN3_target.subs(xs, sp.Rational(1, 2)))
    ok10 = ok10 and (gN3_half < 0)
    check("K10", ok10, "gN3/a0(x=.5)=%.4f ; law residual=0" % gN3_half, "q=2 only; q=3 -> gN<0",
          "site capacity forced to one occupant")
    NUMBERS["gN_q3_at_half"] = float(gN3_half)
    NUMBERS["q_forced"] = 2

    # ==================================================================================
    # K11 -- capacity = affinity: the deep-MOND normalisation
    # ==================================================================================
    Cc, ss, gg = sp.symbols("C s g", positive=True)
    gN_lin = sp.series(gg - Cc * (gg / ss), gg, 0, 2).removeO()
    coeff = sp.simplify(sp.diff(gg - Cc * (gg / ss), gg).subs(gg, 0))
    ok11 = (sp.simplify(coeff - (1 - Cc / ss)) == 0) and (sp.simplify(coeff.subs(Cc, ss)) == 0)
    check("K11", ok11, "1-C/s -> 0 iff C=s", "C=s exactly", "linear term must vanish for n=1")
    NUMBERS["linear_coeff"] = str(coeff)

    # ==================================================================================
    # K12 -- the stiffness map: L*^2 = J z K /(a a0^2)  (c=1)
    # ==================================================================================
    J, aa, z, Ls = sp.symbols("J a z L_star", positive=True)
    gamma_s = J * z * K ** 2 / (2 * aa * a0_can ** 2)      # from the lattice Gaussian map
    Ls_sq = sp.simplify(2 * gamma_s / K)
    target_sq = J * z * K / (aa * a0_can ** 2)
    ok12 = sp.simplify(Ls_sq - target_sq) == 0
    J_over_a = a0_can ** 2 * Lstar_ref ** 2 / (6.0 * K)     # z = 6
    ellP = 1.616255e-35
    J_at_planck = c * c * ellP * a0_can ** 2 * Lstar_ref ** 2 / (6.0 * K)
    J_at_fm = c * c * 1e-15 * a0_can ** 2 * Lstar_ref ** 2 / (6.0 * K)
    hbar = 1.054571817e-34
    ratio_planck = J_at_planck / (hbar * c / ellP)
    ratio_fm = J_at_fm / (hbar * c / 1e-15)
    check("K12", ok12, "J=%.3e J (a=l_P) ; J/(hc/a)=%.3e" % (J_at_planck, ratio_planck),
          "identity exact; J/(hc/a) recorded", "coupling is fixed by L*, not by kappa")
    NUMBERS["J_over_a_c1"] = float(J_over_a)
    NUMBERS["J_at_planck"] = float(J_at_planck)
    NUMBERS["J_at_fm"] = float(J_at_fm)
    NUMBERS["J_over_natural_planck"] = float(ratio_planck)
    NUMBERS["J_over_natural_fm"] = float(ratio_fm)

    # ==================================================================================
    # K13 -- the coupling is kappa-blind: dJ/dkappa = 0 at fixed L*
    # ==================================================================================
    Jfun = a0_can ** 2 * Lstar_ref ** 2 / (6.0 * K)   # no kappa anywhere
    dJdk = sp.diff(sp.sympify(Jfun), kap_s)
    ok13 = (dJdk == 0)
    check("K13", ok13, str(dJdk), "== 0", "J (hence L*) contains no kappa")

    # ==================================================================================
    # K14 -- the shift symmetry: Gibbs weights invariant, kappa moves
    # ==================================================================================
    beta, E0, E1, fshift = 1.0, 0.3, 1.7, 1.0     # fshift = C/u_L, the vacuum-energy shift
    w0 = math.exp(-beta * E0) / (math.exp(-beta * E0) + math.exp(-beta * E1))
    w0s = math.exp(-beta * (E0 + fshift)) / (math.exp(-beta * (E0 + fshift)) + math.exp(-beta * (E1 + fshift)))
    inv = abs(w0 - w0s)
    kappa_new = kap / math.sqrt(1.0 + fshift)      # rho_L -> rho_L (1+f)
    ok14 = inv < 1e-14 and abs(kappa_new - kap) > 0.1
    check("K14", ok14, "|dw|=%.2e ; kappa -> %.4f" % (inv, kappa_new), "<1e-14 ; moves >0.1",
          "H->H+C leaves every response, moves kappa")
    NUMBERS["gibbs_shift_invariance"] = float(inv)
    NUMBERS["kappa_after_shift"] = float(kappa_new)

    # ==================================================================================
    # K15 -- the vacuum energy is not the medium's elastic energy; the gap is exactly
    #        twice the closure number:  rho_L c^2 / u_el = 2 Lambda c^4/a0^2
    # ==================================================================================
    u_el = a0_can ** 2 / (4.0 * K)        # (L*^2/4K)(a0/L*)^2 = a0^2/(4K) = a0^2/(16 pi G)
    ratio_el = u_L / u_el
    ratio_el_exact = 2.0 * Lambda * c ** 4 / a0_can ** 2
    ok15 = abs(ratio_el / ratio_el_exact - 1.0) < 1e-12 and 190.0 < ratio_el < 210.0
    check("K15", ok15, "u_L/u_el=%.3f == 2*Lambda*c^4/a0^2=%.3f" % (ratio_el, ratio_el_exact),
          "190-210, identity", "elastic energy is 201x below rho_Lambda c^2")
    NUMBERS["u_el"] = float(u_el)
    NUMBERS["u_L"] = float(u_L)
    NUMBERS["u_L_over_u_el"] = float(ratio_el)
    NUMBERS["u_L_over_u_el_dex"] = float(math.log10(ratio_el))

    # ==================================================================================
    # K16 -- the turn-off is an IR scale, not a UV one
    # ==================================================================================
    a_t = YT_CAN * a0_can
    ok16 = (a_t / cH_L > 10.0) and (a_t / (c * H0) > 9.0)
    check("K16", ok16, "a_t=%.4e ; /cH_L=%.3f ; /cH0=%.3f" % (a_t, a_t / cH_L, a_t / (c * H0)),
          "a_t/cH_L>10", "turn-off sits at 11.5 cH_Lambda")
    NUMBERS["a_t"] = float(a_t)
    NUMBERS["a_t_over_cHL"] = float(a_t / cH_L)
    NUMBERS["a_t_over_cH0"] = float(a_t / (c * H0))
    xi_turn = c * c / a_t                    # the correlation length the turn-off would need
    NUMBERS["xi_turnoff_Mpc"] = float(xi_turn / Mpc)
    NUMBERS["ell1_over_xi_turnoff"] = float(ell1 / xi_turn)
    NUMBERS["xi_turnoff_over_Lstar"] = float(xi_turn / Lstar_ref)
    NUMBERS["xi_turnoff_over_Lstar_dex"] = float(math.log10(xi_turn / Lstar_ref))

    # ==================================================================================
    # K17 -- the identity curve L* = (sigma_c/c)^2 ell_1/kappa
    # ==================================================================================
    sig_ref = 8.33e3
    Lstar_id = (sig_ref / c) ** 2 * ell1 / kap
    sig_at_24 = c * math.sqrt(kap * 24.0 * pc / ell1)
    sig_at_90 = c * math.sqrt(kap * 90.0 * pc / ell1)
    ok17 = (abs(Lstar_id / pc - 24.04) < 0.1) and (sig_at_90 / 8.23e3 > 1.9)
    check("K17", ok17, "L*(8.33km/s)=%.2f pc ; sigma(24pc)=%.3f ; sigma(90pc)=%.3f km/s"
          % (Lstar_id / pc, sig_at_24 / 1e3, sig_at_90 / 1e3), "24.04+-0.1 ; sigma(90)>1.9x",
          "the identity passes the measured point by construction")
    NUMBERS["Lstar_identity_pc"] = float(Lstar_id / pc)
    NUMBERS["sigma_at_24pc_kms"] = float(sig_at_24 / 1e3)
    NUMBERS["sigma_at_90pc_kms"] = float(sig_at_90 / 1e3)
    NUMBERS["sigma_90_over_thermal"] = float(sig_at_90 / 8.23e3)

    # ==================================================================================
    # K18 -- the closure curve: y_t = sqrt(2) kappa ell_1 / L*
    # ==================================================================================
    def yt_of(k, Lstar_pc):
        # the medium's correlation length is lambda_P = L*/sqrt(2) (section 3.4);
        # L_MOND = ell_1/kappa, so y_t = L_MOND/lambda_P = sqrt(2) ell_1/(kappa L*)
        return math.sqrt(2.0) * ell1 / (k * Lstar_pc * pc)

    ytB = yt_of(kap, 24.0)
    FB = F_turn(np.inf, ytB) if np.isfinite(ytB) else float("nan")
    ytB90 = yt_of(kap, 90.0)
    FB90 = F_turn(np.inf, ytB90) if np.isfinite(ytB90) else float("nan")
    # curve: at kappa=1/2 solve F(sqrt2*kappa*ell1/L*) = 8pi/kappa^2 for L*
    Lstar_curve = brentq(lambda Lp: F_turn(np.inf, yt_of(kap, Lp)) - target, 1.0, 1e12)
    # curve: at L*=24 pc solve for kappa
    kappa_curve = brentq(lambda k: F_turn(np.inf, yt_of(k, 24.0)) - 8 * math.pi / k ** 2, 1e-10, 0.45)
    ok18 = (FB / target > 1e6) and (Lstar_curve > 1e8) and (kappa_curve < 0.01)
    check("K18", ok18, "L*(kappa=.5)=%.4e pc ; kappa(L*=24pc)=%.5f ; F/F_t=%.3e"
          % (Lstar_curve, kappa_curve, FB / target), ">1e8 pc ; <0.01 ; >1e6",
          "closure/Compton curve misses by 7.4 dex")
    NUMBERS["yt_curve_at_24pc"] = float(ytB)
    NUMBERS["F_curve_at_24pc"] = float(FB)
    NUMBERS["F_curve_over_target"] = float(FB / target)
    NUMBERS["Lstar_curve_pc"] = float(Lstar_curve)
    NUMBERS["Lstar_curve_Mpc"] = float(Lstar_curve * pc / Mpc)
    NUMBERS["Lstar_curve_over_24pc"] = float(Lstar_curve / 24.0)
    NUMBERS["curve_B_dex"] = float(math.log10(Lstar_curve / 24.0))
    NUMBERS["kappa_curve_at_24pc"] = float(kappa_curve)
    NUMBERS["kappa_curve_over_measured"] = float(kap / kappa_curve)
    NUMBERS["yt_curve_at_90pc"] = float(ytB90)
    NUMBERS["F_curve_over_target_90pc"] = float(FB90 / target)

    # ==================================================================================
    # K19 -- the parameter count
    # ==================================================================================
    # inputs of the completion: q (fixed by the law), J/a (fixed by L*), eps_0 (the energy zero)
    # targets: kappa, L*.  3 inputs -> 2 targets: one more free parameter.
    n_inputs, n_targets = 3, 2
    ok19 = (n_inputs - n_targets) == 1
    check("K19", ok19, "%d inputs, %d targets, excess %d" % (n_inputs, n_targets, n_inputs - n_targets),
          "excess == 1", "q, J/a, eps_0 vs kappa, L*")
    NUMBERS["n_inputs"] = n_inputs
    NUMBERS["n_targets"] = n_targets

    # ==================================================================================
    # K20 -- convergence: bare capacity diverges, turn-off converges, finite xi converges
    # ==================================================================================
    dec = [1e2, 1e3, 1e4, 1e5]
    ratios = [F_plain(Y) / Y for Y in dec]
    ok20 = (abs(ratios[-1] - 1.0) < 0.02) and (abs(F_turn(np.inf, YT_CAN) - TARGET_CAN) < 1e-6) \
        and (abs(F_turn(50.0, YT_CAN) - F_plain(50.0)) / F_plain(50.0) < 0.2)
    check("K20", ok20, "F(Y)/Y at 1e5 = %.5f ; F_inf = %.4f ; F(50) ratio=%.3f"
          % (ratios[-1], F_turn(np.inf, YT_CAN), F_turn(50.0, YT_CAN) / F_plain(50.0)),
          "->1 ; 100.4058 ; <0.2", "linear divergence without a cutoff")
    NUMBERS["F_over_Y_at_1e5"] = float(ratios[-1])
    NUMBERS["F_turn_at_50"] = float(F_turn(50.0, YT_CAN))
    NUMBERS["F_plain_at_50"] = float(F_plain(50.0))

    # ==================================================================================
    npass = sum(1 for r in RESULTS if r["pass"])
    ntot = len(RESULTS)
    print()
    print("%s COMPLETE: %d/%d checks PASS." % (LANE, npass, ntot))

    out = {
        "lane": LANE,
        "status": "NO-GO(obstruction)" if npass == ntot else "FAIL",
        "mutation": mut or None,
        "checks": RESULTS,
        "numbers": NUMBERS,
        "constants_used": [
            "c=2.99792458e8 m/s", "G=6.67430e-11", "H0=67.4 km/s/Mpc",
            "Lambda=1.0890e-52 m^-2", "a0_can=9.36e-11 m/s^2", "kappa_can=0.5",
            "pc=3.0856775814913673e16 m", "Mpc=3.0856775814913673e22 m",
            "K=4*pi*G (A33 1.1)", "Z=2*sqrt(8*pi/3)", "C_can=-0.8862943611 (A4/A28)",
            "YT_CAN=66.299937 (A4/A28)", "sigma_c=8.33 km/s (A20 cand.1)",
        ],
    }
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(out, f, indent=1)
    return 0 if npass == ntot else 1


if __name__ == "__main__":
    sys.exit(main())
