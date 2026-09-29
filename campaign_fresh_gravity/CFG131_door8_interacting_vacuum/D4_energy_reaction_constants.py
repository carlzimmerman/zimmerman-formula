#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D4 -- Door 8, G3 / G4 / G5 and the one channel D1 leaves for an M-dependence.

  A  G3 reaction on the baryons.  Hypothesis H3/H4: the baryons couple only through gravity and Q^mu = Q u_c^mu touches only the cold fluid and the vacuum.  The exchange terms cancel
     in the total (Q u^nu - Q u^nu = 0), so the baryon equation nabla_mu T_b^{mu nu} = 0 contains no Q: the non-gravitational reaction is ZERO by construction.  (A pass that costs
     nothing because the target is not produced; see D1/D3.)  The energy an exchange along u can inject is rest-mass energy only: the orthogonal (heating) component of Q^mu is zero (D1-A1).
  B  G3 energy: what the target would have to draw from the vacuum.  Rest mass in the target beyond the cosmic cold share, M_c(<r) - (Omega_c/Omega_b) M_b with the CFG44 point-mass
     M_c = M_b (sqrt(1+x^2) - 1), against the vacuum energy in the Lagrangian volume of the baryons, rho_L V_L c^2 = (Omega_L/Omega_b) M_b c^2 (creation before collapse is the upper bound: the
     vacuum energy density does not compress).  Reported against the baryons' orbital energy M_b V_c^2/2.  Independent of r_ta (evaluated at x = r/r_M, x in [0.3, 30]).
  C  G4: constants.  D  G5: the sign condition c_s^2 >= 0, hyperbolicity, Solar System.
  E  the channel D1 leaves: an M-dependence through the epoch of formation if Q makes Lambda dynamical and p = p(rho_c; Lambda).  The exponent s in p proportional to Lambda^s needed to span the
     required factor, against the Lambda range the flat-a0 law (D2) and the growth (D3) allow.  UNTESTED as a construction; the number is a requirement, not a result.

MUTATE=1: the vacuum budget is inflated tenfold; the claim 'the target's rest mass exceeds the vacuum budget at x = 30' must FAIL (exit 1).
Run: python3 D4_energy_reaction_constants.py
"""
import os, sys, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import Dcommon as C

R = C.Run("D4_energy_reaction_constants")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)

R.banner("A  reaction on the baryons (G3, first clause)")
Q = sp.Symbol('Q'); u = sp.Symbol('u')
tot = sp.simplify((Q * u) + (-Q * u))
check("A", "the exchange terms cancel in the total: nabla T_c = +Q u, nabla T_vac = -Q u, nabla T_b = 0 (no Q in the baryon equation)", "sum of exchange terms = %s" % tot, tot == 0,
      "reaction on the baryons beyond gravity = 0 <= 0.10 g_law: PASS at no cost (H3/H4); the dark mass still gravitates on the baryons as whatever fluid density results")

R.banner("B  rest-mass budget against the vacuum in the Lagrangian volume (G3, energy clause)")
Oc_over_Ob = 0.1200 / 0.02237                    # CFG44's cosmic ratio
h = 0.674
Ob_ = 0.02237 / h ** 2
OL_over_Ob = C.OL / Ob_ * (10.0 if M == 1 else 1.0)
P("  Omega_c/Omega_b = %.3f (CFG44), Omega_L/Omega_b = %.2f (Omega_L = %.3f, Omega_b = %.4f)%s" % (Oc_over_Ob, OL_over_Ob, C.OL, Ob_, "   [MUTATE=1: x10]" if M == 1 else ""))
x_cap = math.sqrt((1 + Oc_over_Ob) ** 2 - 1)
x_star = math.sqrt((1 + Oc_over_Ob + OL_over_Ob) ** 2 - 1)
P("  the target exhausts the cosmic cold share at x_cap = %.2f (CFG44: 6.29); it needs more rest mass than ALL the vacuum energy in the Lagrangian volume beyond x* = %.2f" % (x_cap, x_star))
P("   x       Mc/Mb = sqrt(1+x^2)-1   extra/Mb = max(0, Mc/Mb - Oc/Ob)   fraction f of the Lagrangian vacuum used   a0 factor sqrt(1-f)   extra c^2 / (V_c^2/2) at M = 1e11")
Msun_ = 1e11
for xx in (0.3, 1.0, 3.0, 6.29, 10.0, 20.0, 30.0):
    mc = math.sqrt(1 + xx ** 2) - 1
    ex = max(0.0, mc - Oc_over_Ob)
    f = ex / OL_over_Ob
    vc2 = math.sqrt(C.G_KPC * Msun_ * C.A0)                      # V_flat^2 = sqrt(G M a0): the orbital scale
    ratio = ex * C.C_KMS ** 2 / (vc2 / 2)
    P("  %5.2f   %8.3f                %8.3f                             %8.3f                      %s              %s" % (xx, mc, ex, f, ("%.3f" % math.sqrt(1 - f)) if f < 1 else "  (f>1)", "%.1e" % ratio if ex > 0 else "0 (no conversion needed)"))
mc30 = math.sqrt(1 + 30 ** 2) - 1
ok_b = (mc30 - Oc_over_Ob) / OL_over_Ob > 1.0
check("B1", "CLAIM: at x = 30 the target needs more rest mass than the whole vacuum energy of the baryons' Lagrangian volume (f > 1); the conversion is impossible without Lambda -> 0",
      "f(x = 30) = %.2f; x* = %.1f" % ((mc30 - Oc_over_Ob) / OL_over_Ob, x_star), ok_b,
      "and Lambda is uniform on the fluid-orthogonal slices (D1), so the depletion f is not local to the halo: a0 = kappa c sqrt(G rho_L) falls by sqrt(1 - f) everywhere: the tie is circular")
check("B2", "for x <= x_cap no conversion is needed (the cosmic share suffices): the exchange does nothing the standard cold fluid does not; beyond x_cap the energy demand is about c^2/V_c^2 ~ 1e6 times the orbital energy",
      "c^2/(V_f^2/2) at 1e11 Msun = %.1e" % (C.C_KMS ** 2 / (math.sqrt(C.G_KPC * Msun_ * C.A0) / 2)), C.C_KMS ** 2 / (math.sqrt(C.G_KPC * Msun_ * C.A0) / 2) > 1e5,
      "G3's energy line (<= the baryons' orbital energy) fails for any x > x_cap in both r_ta conventions (the number does not depend on r_ta)")

R.banner("C  G4 constants")
P("  Q = Q(Lambda) only (the only cold-safe entry, D1/D3): amplitude xi (1: not tied to kappa or Lambda in any derived way).")
P("  A Q with Q_rho != 0: the exponent n = rho Q_rho/Q is the sound speed; growth needs n <= 4.6e-12 (D3 R2, k = 30): a second constant, tuned below 1e-11.")
P("  The forced EOS p = n rho/(1-n) + C rho^n carries an integration constant C (dimensionful): a third.")
P("  The target itself: p_req(rho; M_b) is a function of M_b (D1): NO finite set of constants makes it a function of rho alone.")
check("C", "G4 count: xi, n, C are all new (kappa = 1/2 and Omega_c h^2 = 0.12 inherited); none is tied to Lambda or kappa by the action", "new constants >= 2 for the cold-safe entry (xi, C), 3 with n != 0", True,
      "G4 FAIL, and moot: G1 fails first")

R.banner("D  G5 well-posedness and Solar System")
csq = sp.Symbol('c_s2'); Qs, Qrs, rhs_, ps = sp.symbols('Q Q_rho rho p')
c2 = (rhs_ + ps) * Qrs / Qs
P("  c_s^2 = (rho + p) Q_rho/Q: real sound speed (no gradient instability) needs Q_rho Q >= 0; the target needs c_s^2 ~ 2e-8..6e-7 > 0, so the SIGN is fine; the vacuum has no kinetic term (no ghost).")
P("  Hyperbolicity: the u-adapted chart has N = -rho_L'/Q: the constraint d_mu rho_L = Q u_mu is first order and consistent (D1-B derivation closes); with c_s^2 > 0 the fluid system is hyperbolic.")
P("  Solar System: Q u_c^mu does not act on baryons (H4) and |grad rho_L| = Q = xi H_L rho_L ~ 0.03 H rho_L is far below any PPN scale; NO PPN calculation is done: an explicit STATEMENT conditional on H4 (as the gate allows).")
check("D", "G5: c_s^2 >= 0 iff Q_rho Q >= 0 (sympy: c_s^2 = %s); no ghost; hyperbolic; Solar System safe by statement" % c2, "the target's required c_s^2 is positive: PASS in sign", True, "G5: PASS as stated; G5 does not rescue G1/G2")

R.banner("E  the epoch channel (untested construction): how large an exponent would the Lambda-dependence need?")
P("  required factor F(rho) = p_req(1e12)/p_req(1e9) at matched density (D1): 31.6 at low density to 353 at the highest overlap (exp sphere, h = 2 kpc, D1); use the 31.6 (most generous).")
F_req = (1e12 / 1e9) ** 0.5                               # deep-regime scaling p_req proportional to M^(1/2) (D1): the most generous factor, 31.6
lam_ratio = {}
for xx in (0.03, 0.3):
    bgx = C.background(xx)
    lam_ratio[xx] = math.sqrt(C.bg_state(bgx, 1 / 3.5)[1] / C.bg_state(bgx, 1.0)[1])      # a0(z = 2.5)/a0(0) recomputed from the background
for xx, r in lam_ratio.items():
    lr = r ** 2
    P("  xi = %.2f: rho_L(z = 2.5)/rho_L(0) = %.4f -> s = ln F / ln(rho_L ratio) = %.1f (F = 31.6) or %.1f (F = 350)" % (xx, lr, math.log(F_req) / math.log(lr), math.log(350) / math.log(lr)))
s_best = math.log(F_req) / math.log(lam_ratio[0.3] ** 2)
check("E", "an M-dependence through the formation epoch needs p proportional to rho_L^s with s >= %.0f even at xi = 0.3 (where a0(2.5) is already 10%% off flat and growth is 13%% low), s ~ %.0f at the flat-a0 limit xi = 0.03" % (s_best, math.log(F_req) / math.log(lam_ratio[0.03] ** 2)),
      "s_min = %.1f (xi = 0.3), %.1f (xi = 0.03)" % (s_best, math.log(F_req) / math.log(lam_ratio[0.03] ** 2)), s_best > 10,
      "a huge tuned exponent (a new constant), a0(z) off flat, an M(z_f) map not derived, and the EOS would drift as Lambda evolves at fixed rho (halos would not stay in the target's equilibrium): an untested completion, not a route")
R.finish()
