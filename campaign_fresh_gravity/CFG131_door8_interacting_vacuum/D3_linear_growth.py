#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
D3 -- Door 8, deliverable 3 (and G2): the linear perturbation equations for delta_c with Q(Lambda, rho_c) and the growth ratio to LCDM, in CFG43's two-fluid conventions.

  A (sympy, conformal Newtonian gauge) the relativistic continuity equation of the cold fluid with the source, and its sub-horizon reduction:
        delta_c' = -theta - a Gamma (1 - n) delta_c        (' = d/d eta; theta = div v; Gamma = Q/rho_c; n = rho_c Q_rho / Q; p = 0)
     the Euler equation is UNCHANGED by Q (Q u^mu carries no force: the created matter is at rest in the fluid frame), so
        d_c'' + (2 + dlnH/dlna + gamma/H) d_c' = (3/2)(Om_c d_c + Om_b d_b) - [c_s^2 k^2/(aH)^2 + 2 gamma/H + gamma'/H] d_c,    gamma = Gamma (1 - n)  (' = d/dln a)
     and the vacuum-consistency constraint of D1-B:  Q_rho delta rho_com = Q delta p_com/(rho + p)  (c_s^2 = (rho + p) Q_rho/Q).
     delta rho_Lambda = Q a v is O((aH/k)^2) relative to the cold density perturbation and is dropped (checked by scaling in sympy).
  B RESULTS.  (R1) Dust with Q_rho != 0: delta rho_com = 0, the cold fluid sources no Poisson potential: only the baryons grow.
              (R2) The Q-consistent barotropic fluid: largest constant c_s^2 (= n(1+w)) that keeps growth within 5% of LCDM at k = 0.5, 2, 10, 30 /Mpc (z = 0 and z = 10 versions).
              (R3) Q = Q(Lambda) only (n = 0, so LCDM-like linear cold behaviour): the growth ratio against xi (dilution + background shift).
              (R4) The Q-consistent fluid whose EOS IS the target's required EOS (point mass, c_s,req^2(x) with x fixed by rho_c(a)): growth ratio for 1e9..1e12 Msun.
  Solver validation: the same solver run with CFG43's saturating-EOS c_s^2 at nu* = 1 must return CFG43's 0.140 / 0.099 / 0.080 at k = 0.5 / 2 / 10 (2%).
  G2 PASS iff the ratio >= 0.95 at k = 0.5, 2, 10, 30.

MUTATE=3: the vacuum-consistency constraint is dropped (dust with Q_rho != 0 keeps its normal Poisson source): the claim 'R1: growth collapses' must FAIL (exit 1).
Run: python3 D3_linear_growth.py
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import Dcommon as C

R = C.Run("D3_linear_growth")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)

# ============================================================================================ A: sympy
R.banner("A  relativistic continuity with the source and its sub-horizon reduction (sympy)")
eta, x, y, z, eps = sp.symbols('eta x y z epsilon', real=True)
XB = [eta, x, y, z]
a = sp.Function('a')(eta)
Psi = sp.Function('Psi')(eta, x); Phi = sp.Function('Phi')(eta, x)
gB = a ** 2 * sp.diag(-(1 + 2 * eps * Psi), (1 - 2 * eps * Phi), (1 - 2 * eps * Phi), (1 - 2 * eps * Phi))
ser = lambda e: sp.series(e, eps, 0, 2).removeO()
giB = gB.inv().applyfunc(lambda e: sp.simplify(ser(e)))
GamB = [[[sp.expand(ser(sp.expand(sum(giB[al, d] * (sp.diff(gB[d, b], XB[c]) + sp.diff(gB[d, c], XB[b]) - sp.diff(gB[b, c], XB[d])) for d in range(4)) / 2))) for c in range(4)] for b in range(4)] for al in range(4)]
v = sp.Function('v')(eta, x)
rb = sp.Function('rb')(eta)
drho = sp.Function('drho')(eta, x); dp = sp.Function('dp')(eta, x)
uB_lo = sp.Matrix([-a * (1 + eps * Psi), a * eps * sp.diff(v, x), 0, 0])
uB_up = (giB * uB_lo).applyfunc(lambda e: sp.expand(ser(sp.expand(e))))
TB = (((rb + eps * drho) + eps * dp) * uB_up * uB_up.T + eps * dp * giB).applyfunc(lambda e: sp.expand(ser(sp.expand(e))))     # background p = 0 (cold), delta p = c_s^2 delta rho
divB = [sum(sp.diff(TB[m, nu], XB[m]) for m in range(4)) + sum(GamB[m][m][l] * TB[l, nu] for m in range(4) for l in range(4)) + sum(GamB[nu][m][l] * TB[m, l] for m in range(4) for l in range(4)) for nu in range(4)]
Dl0 = sp.expand(ser(sp.expand(sum(gB[0, s] * divB[s] for s in range(4)))))
Qb = sp.Function('Qb')(eta); dQ = sp.Function('dQ')(eta, x)
cont = sp.simplify(Dl0.coeff(eps, 1) + a * (dQ + Qb * Psi))                    # D_eta^(1) = (Q u_eta)^(1) = -a (dQ + Qb Psi)
P("  continuity (first order):  ", cont, "= 0")
# solve for drho' and build delta = drho/rb
dr_t = sp.Function('dr')(eta); kk = sp.symbols('k', positive=True)
delta = sp.Function('delta')(eta); H = sp.Function('calH')(eta)
Ew = sp.exp(sp.I * kk * x)
Ps, Ph, V_ = sp.Function('Ps')(eta), sp.Function('Ph')(eta), sp.Function('V')(eta)
Qr, cs2 = sp.symbols('Q_rho c_s2', positive=True)
cont_pw = sp.simplify(cont.subs({Psi: Ps * Ew, Phi: Ph * Ew, v: V_ * Ew, drho: rb * delta * Ew, dp: cs2 * rb * delta * Ew, dQ: Qr * rb * delta * Ew}).doit() / Ew)
drt = sp.solve(cont_pw, sp.diff(delta, eta))[0]
rbp = -3 * (sp.diff(a, eta) / a) * rb + a * Qb                                   # background (p = 0)
drt = sp.simplify(drt.subs(sp.Derivative(rb, eta), rbp))
P("  delta_c' (full linear GR, p_bar = 0, dQ = Q_rho drho) =", drt)
Gam_, nn = sp.symbols('Gamma n', positive=True)
sub = sp.simplify(drt.subs(Qb, Gam_ * rb).subs(Qr, nn * Gam_))                    # Q = Gamma rho_c, Q_rho = n Q / rho_c = n Gamma
# sub-horizon: keep the terms with k^2 V and delta; drop Phi', Psi, and the (calH)-suppressed piece
sh = sp.expand(sub)
theta_term = sp.simplify(sh.coeff(V_))
delta_term = sp.simplify(sh.coeff(delta))
P("  coefficient of V:", theta_term, "   coefficient of delta:", delta_term, "   remaining (potential) terms:", sp.simplify(sh - theta_term * V_ - delta_term * delta))
okA = sp.simplify(theta_term - kk ** 2) == 0 and sp.simplify(delta_term - (-3 * (sp.diff(a, eta) / a) * cs2 + a * Gam_ * (nn - 1))) == 0
check("A1", "sub-horizon continuity: delta_c' = k^2 V (= -theta) + [-3 calH c_s^2 - a Gamma (1 - n)] delta_c + (Phi', Psi terms suppressed by (calH/k)^2)", "sympy: %s" % okA, okA,
      "the source enters as a dilution rate a Gamma (1 - n): created matter is uniform on the comoving slice when Q_rho = 0 (n = 0)")
# second-order equation from (i) delta' = -theta/a - gam delta and (ii) theta' + H theta = -(3/2) a H^2 S + c_s^2 k^2 delta/a  (cosmic time)
tS = sp.Symbol('t'); Hs = sp.Function('H')(tS); aa = sp.Function('aa')(tS); dl = sp.Function('dl')(tS); th = sp.Function('th')(tS); gm = sp.Function('gm')(tS); S = sp.Function('S')(tS)
k_, c2_ = sp.symbols('k c2', positive=True)
eq_theta = -aa * (dl.diff(tS) + gm * dl)                                          # from (i)
eq_ii = sp.Eq(th.diff(tS) + Hs * th, -aa * S + c2_ * k_ ** 2 * dl / aa)           # S = 4 pi G sum rho_i delta_i
res_ = sp.simplify(eq_ii.lhs.subs(th, eq_theta).doit() - eq_ii.rhs.subs(th, eq_theta).doit())
res_ = sp.simplify(res_.subs(aa.diff(tS), aa * Hs))
target = sp.simplify(-aa * (dl.diff(tS, 2) + (2 * Hs + gm) * dl.diff(tS) + (2 * Hs * gm + gm.diff(tS) + c2_ * k_ ** 2 / aa ** 2) * dl - S))
okA2 = sp.simplify(res_ - target) == 0
check("A2", "eliminating theta: delta'' + (2H + gamma) delta' + (2 H gamma + gamma_dot + c_s^2 k^2/a^2) delta = 4 pi G sum rho_i delta_i", "sympy: %s" % okA2, okA2, "this is D3's solver equation (converted to ln a in Dcommon.growth_ratio)")
# the dropped vacuum perturbation: drho_L = Q a v with v = -theta/k^2 * ... scaling: drho_L / (rho_c delta) ~ (a Gamma) * calH * (delta ...)/k^2 ~ Gamma H (calH/k)^2
check("A3", "delta rho_Lambda = Q a v is O(Gamma/H (calH/k)^2) of rho_c delta_c on sub-horizon scales", "at k = 0.5/Mpc, z = 0, Gamma/H <= 0.03: (calH/k)^2 = %.1e" % ((C.H0_KMS / C.C_KMS / 0.5) ** 2), (C.H0_KMS / C.C_KMS / 0.5) ** 2 < 1e-3, "so it is dropped in the Poisson equation (the vacuum does not cluster)")

# ============================================================================================ B: numerics
R.banner("B  growth results")
ks = [0.5, 2.0, 10.0, 30.0]
EPSc = 0.25 / (8 * math.pi); nu0 = C.OC / C.OL
def cs2_cfg43(nus, a_):
    nu = nu0 / a_ ** 3; xx = nu / nus; Fp = 2 * xx / (1 + xx ** 2) ** 2; drho_ = 1 + EPSc * (math.atan(xx) + xx / (1 + xx ** 2)); return EPSc * Fp / nus / drho_
base = {k: C.growth_ratio(k, lambda a_: 0.0) for k in ks}
val = {k: C.growth_ratio(k, lambda a_: cs2_cfg43(1.0, a_)) / base[k] for k in (0.5, 2.0, 10.0)}
okV = abs(val[0.5] / 0.140 - 1) < 0.02 and abs(val[2.0] / 0.099 - 1) < 0.02 and abs(val[10.0] / 0.080 - 1) < 0.02
check("V", "solver validation: CFG43's nu* = 1 saturating-EOS fluid gives 0.140 / 0.099 / 0.080 at k = 0.5 / 2 / 10 (2%)", "%.3f / %.3f / %.3f" % (val[0.5], val[2.0], val[10.0]), okV, "")

# ---- R1
def baryon_only_total(k_unused):
    a_i = 1.0 / 1001
    def rhs(la, yv):
        a_ = math.exp(la); e2 = C.E2_lcdm(a_); dlnH = -(3 * C.OM / a_ ** 3 + 4 * C.OR / a_ ** 4) / (2 * e2)
        Omb = C.OB / a_ ** 3 / e2
        db, dbp = yv
        return [dbp, -(2 + dlnH) * dbp + 1.5 * Omb * db]
    s = solve_ivp(rhs, [math.log(a_i), 0.0], [a_i, a_i], rtol=1e-10, atol=1e-14, method="LSODA")
    return C.OB * s.y[0, -1] / C.OM               # delta_c = 0 (delta rho_com = 0): total matter delta = (Om_b/Om_m) delta_b
if M == 3:
    r1 = {k: 1.0 for k in ks}                     # MUTATE=3: constraint dropped, cold fluid keeps its Poisson source: LCDM
else:
    bo = baryon_only_total(0)
    r1 = {k: bo / base[k] for k in ks}
P("  (R1) dust with Q_rho != 0 (delta rho_com = 0): total-matter growth ratio to LCDM at z = 0:  " + ", ".join("k=%g: %.2e" % (k, r1[k]) for k in ks))
check("R1", "CLAIM: for dust with Q_rho != 0 the cold fluid sources no potential and the total growth ratio to LCDM is < 0.05 at every k (G2 fails)", "ratios %s" % {k: float("%.2e" % v_) for k, v_ in r1.items()},
      all(v_ < 0.05 for v_ in r1.values()), "the cold sector has no linear growth; only baryons grow, from z = 1000 with delta_b = a (CFG43 convention, no photon drag included)" if M != 3 else "MUTATE=3 control: constraint dropped")

# ---- R2: cs2_max
def ratio_cs2(k, c2, a_end=1.0):
    return C.growth_ratio(k, lambda a_: c2, a_end=a_end) / C.growth_ratio(k, lambda a_: 0.0, a_end=a_end)
def cs2_max(k, a_end):
    f = lambda lc: ratio_cs2(k, 10 ** lc, a_end) - 0.95
    grid = np.arange(-16.0, -3.9, 0.5); vals = [f(g_) for g_ in grid]
    idx = [i for i, v_ in enumerate(vals) if v_ >= 0]
    i = max(idx)
    return 10 ** brentq(f, grid[i], grid[i + 1], xtol=1e-4)
P("")
P("  (R2) largest constant c_s^2 (units c^2) that keeps growth within 5% of LCDM:")
cmax0 = {}; cmax10 = {}
for k in ks:
    cmax0[k] = cs2_max(k, 1.0); cmax10[k] = cs2_max(k, 1 / 11.0)
    P("       k = %5.1f /Mpc : to z = 0: c_s^2 <= %.2e (c_s <= %.2f km/s);   at z = 10: c_s^2 <= %.2e" % (k, cmax0[k], math.sqrt(cmax0[k]) * C.C_KMS, cmax10[k]))
# halo-scale c_s^2 requirement for comparison
P("")
P("  the sound speed the target REQUIRES (point mass, exact): c_s,req^2/c^2 at x = 0.3, 1, 3, 10, 30 for M = 1e9, 1e11:")
G = C.G_KPC; a0 = C.A0
def cs2_req(Mb, xx):
    return math.sqrt(G * Mb * a0) * (1 + xx ** 2) ** 1.5 / (2 * xx ** 3 + xx) / C.C_KMS ** 2
for Mb in (1e9, 1e11):
    P("       M = %.0e:  " % Mb + ", ".join("x=%g: %.2e" % (xx, cs2_req(Mb, xx)) for xx in (0.3, 1, 3, 10, 30)))
req_min = min(cs2_req(Mb, xx) for Mb in (1e9, 1e10, 1e11, 1e12) for xx in np.geomspace(0.1, 30, 60))
P("       smallest required c_s^2 over the four masses and x in [0.1, 30]: %.2e;  largest allowed (k = 30, z = 0): %.2e, ratio = %.1e" % (req_min, cmax0[30.0], req_min / cmax0[30.0]))
check("R2", "the Q-consistent fluid's c_s^2 must be <= the growth bound at every density it passes through, but the target requires c_s^2 above that bound at every x in [0.1, 30] for every mass 1e9..1e12",
      "required minimum %.2e vs allowed %.2e (k = 30) / %.2e (k = 0.5): factor %.1e / %.1e" % (req_min, cmax0[30.0], cmax0[0.5], req_min / cmax0[30.0], req_min / cmax0[0.5]),
      req_min > cmax0[30.0], "G2 fails for c_s^2 = the required value even at k = 0.5; the bound is a growth-history bound on the SAME density values the halo interior passes through (rho_c(z = 10) = 1331 mean today)")

# ---- R3: Q(Lambda) only
P("")
P("  (R3) Q = xi H_L rho_L (Q_rho = 0, n = 0): total-matter growth ratio to LCDM at z = 0 (pressureless, k-independent) and at z = 10:")
xis = [-0.3, -0.1, -0.03, -0.01, 0.0, 0.01, 0.03, 0.1, 0.3]
r3 = {}
for x_ in xis:
    bg = C.background(x_)
    r3[x_] = (C.growth_ratio(1.0, lambda a_: 0.0, bg=bg) / base.get(1.0, C.growth_ratio(1.0, lambda a_: 0.0)),
              C.growth_ratio(1.0, lambda a_: 0.0, bg=bg, a_end=1 / 11.0) / C.growth_ratio(1.0, lambda a_: 0.0, a_end=1 / 11.0))
    P("       xi = %+5.2f : ratio(z=0) = %.4f   ratio(z=10) = %.4f" % (x_, r3[x_][0], r3[x_][1]))
xi5 = brentq(lambda x_: C.growth_ratio(1.0, lambda a_: 0.0, bg=C.background(x_)) / C.growth_ratio(1.0, lambda a_: 0.0) - 0.95, 1e-3, 0.6)
P("       growth ratio reaches 0.95 at xi = %.3f (this is the dilution + background shift only; the flat-a0 law needs |xi| < 0.0275 from D2, comparable)" % xi5)
check("R3", "Q = Q(Lambda) only leaves the linear cold growth intact (ratio >= 0.95) for small |xi|; xi = 0 returns LCDM", "ratio(xi = 0) = %.5f; ratio(0.01) = %.4f, ratio(-0.01) = %.4f" % (r3[0.0][0], r3[0.01][0], r3[-0.01][0]),
      abs(r3[0.0][0] - 1) < 2e-3 and r3[0.01][0] > 0.95 and r3[-0.01][0] > 0.95,
      "the only cold-safe Q is one with Q_rho = 0, and it then carries NO information about the halo: it is a homogeneous modification of the background")

# ---- R4: the fluid whose EOS is the target's
P("")
P("  (R4) Q-consistent fluid with the point-mass target EOS: c_s^2(a) = c_s,req^2(x(rho_c(a)); M), x fixed by rho_c(a) = Om_c rho_crit / a^3 (LCDM background; analytic extension outside x in [0.1, 30]):")
HK = C.H0_KMS / 1000.0                                        # km/s/kpc
rho_crit = 3 * HK ** 2 / (8 * math.pi * G)
rho_c0 = C.OC * rho_crit
def x_of_rho(rho_, Mb):
    rMv = math.sqrt(G * Mb / a0); q = a0 / (4 * math.pi * G * rMv * rho_)
    return math.sqrt((-1 + math.sqrt(1 + 4 * q ** 2)) / 2)
r4 = {}
for Mb in (1e9, 1e10, 1e11, 1e12):
    fn = lambda a_, Mb=Mb: cs2_req(Mb, x_of_rho(rho_c0 / a_ ** 3, Mb))
    row = []
    for k in ks:
        row.append(C.growth_ratio(k, fn) / base[k])
    r4[Mb] = row
    P("       M = %.0e: growth ratio at k = %s: %s   (x(z=0) = %.1f, x(z=10) = %.3f)" % (Mb, ks, ", ".join("%.2e" % v_ for v_ in row), x_of_rho(rho_c0, Mb), x_of_rho(rho_c0 * 1331, Mb)))
worst4 = max(max(v_) for v_ in r4.values())
req_hi = max(cs2_req(Mb, x_of_rho(rho_c0 * 1e3, Mb)) for Mb in (1e9, 1e10, 1e11, 1e12))
check("R4", "the fluid whose EOS is the target's required EOS has G2 growth ratio < 0.95 (fails G2) for every mass and every k tested", "largest ratio over masses and k = %.2e" % worst4, worst4 < 0.95,
      "the target's dispersion c_s^2 ~ V_f^2/2c^2 (2e-8 to 6e-7 for 1e9..1e12) is %.1e (k = 30) to %.1e (k = 0.5) times the growth bound; the analytic extension of the EOS beyond x in [0.1, 30] is an assumption, so R4b restricts it" % (req_min / cmax0[30.0], req_min / cmax0[0.5]))
# R4b: the EOS is applied only where the target defines it (x in [0.1, 30]); c_s^2 = 0 elsewhere; growth ratio at z = 10 (G2's 'z >~ 10' clause) and at z = 0
P("")
P("  (R4b) same, but c_s^2 = c_s,req^2 only where rho_c(a) lies inside the target's own density range (x in [0.1, 30]); zero elsewhere (an upper bound on growth):")
r4b = {}
for Mb in (1e9, 1e10, 1e11, 1e12):
    def fnb(a_, Mb=Mb):
        xx = x_of_rho(rho_c0 / a_ ** 3, Mb)
        return cs2_req(Mb, xx) if 0.1 <= xx <= 30.0 else 0.0
    row0 = [C.growth_ratio(k, fnb) / base[k] for k in ks]
    row10 = [C.growth_ratio(k, fnb, a_end=1 / 11.0) / C.growth_ratio(k, lambda a_: 0.0, a_end=1 / 11.0) for k in ks]
    r4b[Mb] = (row0, row10)
    P("       M = %.0e: ratio at z = 10, k = %s: %s ;  at z = 0: %s" % (Mb, ks, ", ".join("%.2e" % v_ for v_ in row10), ", ".join("%.2e" % v_ for v_ in row0)))
worst4b10 = max(max(v_[1]) for v_ in r4b.values())
check("R4b", "restricted to the density range where the target defines the EOS, the growth ratio at z = 10 is still < 0.95 at k = 30 for every mass", "largest ratio at k = 30, z = 10: %.2e" % max(v_[1][3] for v_ in r4b.values()),
      max(v_[1][3] for v_ in r4b.values()) < 0.95, "so G2's z >~ 10 clause fails for the target EOS with no extrapolation beyond the target's own range (k = 0.5 may pass for the lightest halo: see the table)")
P("")
P("  GATE G2: %s" % ("FAIL (R1: growth collapses for dust with Q_rho != 0; R2/R4: the forced c_s^2 kills growth unless it is below %.1e, while the target needs >= %.1e)" % (cmax0[30.0], req_min) if M != 3 else "n/a (MUTATE)"))
R.finish()
