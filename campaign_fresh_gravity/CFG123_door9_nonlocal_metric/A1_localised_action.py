#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A1_localised_action -- T0 of CFG123_FROZEN_CRITERIA.md (model integrity of the localised RR action), sympy, exact.

T0a  the covariant field equation E_mu nu (cfg123_geom.E_RR, derived by hand) equals the Euler-Lagrange equations of the REDUCED localised action
     on (i) a general FRW ansatz (lapse N(t), scale factor a(t)) and (ii) a general static spherical ansatz (alpha(r), beta(r)); scalar EOMs
     likewise.  Exact residual 0 on random rational polynomial fields (exact rational arithmetic) and symbolically on FRW.
     Also: the Friedmann constraint used by cfg123_common.rr_rhs equals E_00 on shell; the trace formula used by the nonlinear static system.
T0b  the Noether/Bianchi identity  nabla^mu E_mu nu = c * sum_phi E_phi d_nu phi  with c solved (must be a pure rational), so the total stress is
     conserved once the auxiliary-field equations hold.
T0c  linear static flat-space solution for a point mass: exact (all orders in m r) vacuum solution, its leading order in m^2, exponent of r in
     delta Phi, sign and value of c1.
T0d  DW: same T0a/T0b, plus the linear static point-mass solution with F-bar, f' (G renormalisation and slip gamma).
MUTATE=b : the sign of the m^2 S/6 term in the REDUCED action is flipped (covariant E unchanged) -> T0a must FAIL.
Nothing here says the theory is closed; kappa = 1/2 is FITTED and does not appear.
"""
import os, sys, random
import sympy as sp
from sympy.calculus.euler import euler_equations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import Report, mutate_mode, finish
import cfg123_geom as GM

MUT = mutate_mode()
if MUT not in ("", "b"):
    print("A1: MUTATE mode", MUT, "not applicable to this script"); sys.exit(3)
R = Report("A1_localised_action", MUT)
R.P(f"A1 localised action, MUTATE={MUT or 'none'}")
m2 = sp.Symbol("m2", positive=True)
sgn = -1 if MUT == "b" else 1                       # the mutated reduced action carries the wrong sign of the m^2 S/6 term


def rnd_poly(var, deg, seed, lo=1):
    rng = random.Random(seed)
    return sum(sp.Rational(rng.randint(-9, 9), rng.randint(2, 9)) * var ** k for k in range(deg + 1)) + lo


def zero_exact(expr, subs_funcs, var, pts):
    """substitute explicit functions, evaluate at rational points, return max |value| (exact rationals)"""
    e = expr
    for f, val in subs_funcs.items():
        e = e.subs(f, val)
    e = e.doit()
    worst = 0
    for p in pts:
        v = sp.nsimplify(e.subs(var, p).subs(m2, sp.Rational(3, 7)))
        worst = max(worst, abs(sp.N(v, 30)))
    return worst


# =============================================================================================================== T0a (i) FRW
R.banner("T0a(i)  FRW: covariant E_mu nu versus Euler-Lagrange of the reduced localised action")
t, x, y, z = sp.symbols("t x y z")
N = sp.Function("N")(t); a = sp.Function("a")(t)
U = sp.Function("U")(t); S = sp.Function("S")(t); x1 = sp.Function("xi1")(t); x2 = sp.Function("xi2")(t)
gF = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2)
geoF = GM.geometry(gF, [t, x, y, z])
EF = GM.E_RR(geoF, m2, U, S, x1, x2)
SEF = GM.scalar_eoms_RR(geoF, m2, U, S, x1, x2)
Rc, boxU, boxS = geoF["R"], GM.box(geoF, U), GM.box(geoF, S)
Lred = N * a ** 3 * (Rc * (1 + sgn * (-m2 * S / 6)) - x1 * (boxU + Rc) - x2 * (boxS + U))
ELs = euler_equations(Lred, [N, a, U, S, x1, x2], t)
EL = {k: e.lhs for k, e in zip(["N", "a", "U", "S", "x1", "x2"], ELs)}
pred = {"N": 2 * a ** 3 * EF[0, 0] / N ** 2, "a": -6 * N * EF[1, 1],
        "U": N * a ** 3 * SEF["U"], "S": N * a ** 3 * SEF["S"], "x1": N * a ** 3 * SEF["x1"], "x2": N * a ** 3 * SEF["x2"]}
worstF = 0
for seed in (1, 2, 3):
    fs = {N: 1 + rnd_poly(t, 2, seed + 10) / 20, a: 1 + rnd_poly(t, 3, seed + 20) / 9, U: rnd_poly(t, 3, seed + 30), S: rnd_poly(t, 3, seed + 40),
          x1: rnd_poly(t, 3, seed + 50), x2: rnd_poly(t, 3, seed + 60)}
    for k in EL:
        w = zero_exact(EL[k] - pred[k], fs, t, [sp.Rational(1, 3), sp.Rational(-2, 5), sp.Rational(7, 4)])
        worstF = max(worstF, w)
        R.P(f"    seed {seed}  {k:>2s}: |EL - covariant| = {float(w):.3e}")
R.check("T0a(i) FRW: covariant E_mu nu and the four scalar EOMs equal the reduced-action Euler-Lagrange equations (exact rationals, 3 random field sets x 3 points)",
        f"max |residual| = {float(worstF):.3e}", worstF < 1e-20)

# =============================================================================================================== T0a-bg : the Friedmann constraint used by the solver
R.banner("T0a-bg  E_00 on shell (xi1 = m^2 S/6, xi2 = m^2 U/6), N = 1, versus the constraint coded in cfg123_common.rr_rhs")
sub = lambda e: e.subs({x1: m2 * S / 6, x2: m2 * U / 6}).doit().subs(N, 1).doit()
E00 = sp.simplify(sub(EF[0, 0]))
Exx = sp.simplify(sub(EF[1, 1]))
H = sp.diff(a, t) / a
cons = 3 * H ** 2 * (1 - m2 * S / 3) - m2 * H * sp.diff(S, t) + m2 / 6 * sp.diff(S, t) * sp.diff(U, t) - m2 / 12 * U ** 2
res = sp.simplify(E00 - cons)
R.P(f"    E_00 on shell - [3H^2(1 - m^2 S/3) - m^2 H S' + (m^2/6) S' U' - (m^2/12) U^2] = {res}")
R.check("T0a-bg: E_00(on shell) equals the Friedmann constraint used by the background solver (symbolic)", f"residual = {res}", res == 0)
R.P("    E_xx on shell (used in A4 as a consistency check of the solver): " + str(Exx))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "A1_frw_Exx_onshell.txt"), "w").write(sp.srepr(Exx))

# =============================================================================================================== T0a (ii) static spherical
R.banner("T0a(ii)  static spherical: covariant E_mu nu versus Euler-Lagrange of the reduced action (areal gauge, g_tt = -alpha^2, g_rr = beta^2)")
r, th, ph = sp.symbols("r theta phi", positive=True)
al = sp.Function("alpha")(r); be = sp.Function("beta")(r)
Us = sp.Function("U")(r); Ss = sp.Function("S")(r); X1 = sp.Function("xi1")(r); X2 = sp.Function("xi2")(r)
gS = sp.diag(-al ** 2, be ** 2, r ** 2, r ** 2 * sp.sin(th) ** 2)
geoS = GM.geometry(gS, [t, r, th, ph])
ES = GM.E_RR(geoS, m2, Us, Ss, X1, X2)
SES = GM.scalar_eoms_RR(geoS, m2, Us, Ss, X1, X2)
RS = geoS["R"]
LS = al * be * r ** 2 * (RS * (1 + sgn * (-m2 * Ss / 6)) - X1 * (GM.box(geoS, Us) + RS) - X2 * (GM.box(geoS, Ss) + Us))
ELS = euler_equations(LS, [al, be, Us, Ss, X1, X2], r)
ELd = {k: e.lhs for k, e in zip(["al", "be", "U", "S", "x1", "x2"], ELS)}
predS = {"al": 2 * be * r ** 2 * ES[0, 0] / al ** 2, "be": -2 * al * r ** 2 * ES[1, 1] / be ** 2,
         "U": al * be * r ** 2 * SES["U"], "S": al * be * r ** 2 * SES["S"], "x1": al * be * r ** 2 * SES["x1"], "x2": al * be * r ** 2 * SES["x2"]}
worstS = 0
for seed in (1, 2, 3):
    fs = {al: 1 + rnd_poly(r, 2, seed + 110) / 15, be: 1 + rnd_poly(r, 2, seed + 120) / 13, Us: rnd_poly(r, 3, seed + 130), Ss: rnd_poly(r, 3, seed + 140),
          X1: rnd_poly(r, 3, seed + 150), X2: rnd_poly(r, 3, seed + 160)}
    for k in ELd:
        w = zero_exact(ELd[k] - predS[k], fs, r, [sp.Rational(1, 3), sp.Rational(3, 2), sp.Rational(5, 2)])
        worstS = max(worstS, w)
        R.P(f"    seed {seed}  {k:>2s}: |EL - covariant| = {float(w):.3e}")
R.check("T0a(ii) static spherical: covariant E_tt, E_rr and the four scalar EOMs equal the reduced-action Euler-Lagrange equations (exact, 3 sets x 3 points)",
        f"max |residual| = {float(worstS):.3e}", worstS < 1e-20)

# the trace formula used by the nonlinear static system (identity in S, U, off shell in the scalar equations)
Eos = lambda e: e.subs({X1: m2 * Ss / 6, X2: m2 * Us / 6}).doit()
trE = sum(geoS["gi"][i, i] * ES[i, i] for i in range(4))
Fq = 1 - m2 * Ss / 3
trace_formula = -Fq * RS + 3 * (-m2 / 3) * GM.box(geoS, Ss) - m2 / 3 * GM.dot(geoS, Ss, Us) + m2 / 3 * Us ** 2
trd = sp.simplify(Eos(trE) - trace_formula)
R.check("T0a-trace: g^{mu nu}E_mu nu (on shell in xi) = -F R + 3 box F - (m^2/3) dS.dU + (m^2/3) U^2, F = 1 - m^2 S/3 (used with box S = -U in A3)",
        f"residual = {trd}", trd == 0)

# =============================================================================================================== T0b Bianchi
R.banner("T0b  Noether / Bianchi identity: nabla^mu E_mu r = c * sum_phi E_phi d_r phi  (static spherical, off shell)")
n = 4
Gam, gi = geoS["Gam"], geoS["gi"]
Xc = geoS["X"]


def div_r(E):
    """nabla^mu E_{mu r} for a static diagonal-metric symmetric tensor"""
    tot = 0
    for mu in range(n):
        for al_ in range(n):
            if gi[mu, al_] == 0:
                continue
            term = sp.diff(E[mu, 1], Xc[al_]) - sum(Gam[l][al_][mu] * E[l, 1] for l in range(n)) - sum(Gam[l][al_][1] * E[mu, l] for l in range(n))
            tot += gi[mu, al_] * term
    return tot


div = div_r(ES)
cs = sp.Symbol("c")
ident = div - cs * (SES["U"] * sp.diff(Us, r) + SES["S"] * sp.diff(Ss, r) + SES["x1"] * sp.diff(X1, r) + SES["x2"] * sp.diff(X2, r))
cvals = []
worstB = 0
for seed in (1, 2, 3):
    fs = {al: 1 + rnd_poly(r, 2, seed + 210) / 15, be: 1 + rnd_poly(r, 2, seed + 220) / 13, Us: rnd_poly(r, 3, seed + 230), Ss: rnd_poly(r, 3, seed + 240),
          X1: rnd_poly(r, 3, seed + 250), X2: rnd_poly(r, 3, seed + 260)}
    e = ident
    for f_, v in fs.items():
        e = e.subs(f_, v)
    e = e.doit().subs(m2, sp.Rational(3, 7))
    pts = [sp.Rational(1, 3), sp.Rational(3, 2), sp.Rational(5, 2)]
    vals = [sp.nsimplify(sp.simplify(e.subs({r: p, th: sp.Rational(1, 2)}))) for p in pts]
    sol = sp.solve(vals[0], cs)
    cvals.append(sol[0] if sol else None)
    worstB = max(worstB, max(abs(sp.N(v.subs(cs, sol[0]), 30)) for v in vals))
    R.P(f"    seed {seed}: solved c = {sol}; max |residual| over 3 points at that c = {float(worstB):.2e}")
R.check("T0b: nabla^mu E_mu r = c sum_phi E_phi d_r phi with ONE pure rational c for all random field sets, exact residual 0",
        f"c = {cvals}, worst residual {float(worstB):.2e}", worstB < 1e-20 and len(set(cvals)) == 1 and cvals[0] is not None and cvals[0].is_rational)

# =============================================================================================================== T0c linear static flat space
R.banner("T0c  linear static point-mass solution about flat space (areal gauge): exact in m r, then leading order in m^2")
eps, Mg = sp.symbols("epsilon M", positive=True)                                  # Mg = G M
Ph = sp.Function("Phi")(r); La = sp.Function("Lam")(r); uf = sp.Function("u")(r); sf = sp.Function("s")(r)
gL = sp.diag(-(1 + eps * Ph) ** 2, (1 + eps * La) ** 2, r ** 2, r ** 2 * sp.sin(th) ** 2)
geoL = GM.geometry(gL, [t, r, th, ph])
EL_ = GM.E_RR(geoL, m2, eps * uf, eps * sf, m2 * eps * sf / 6, m2 * eps * uf / 6)
lin = lambda e: sp.simplify(sp.diff(e, eps).subs(eps, 0).doit())
Ett1, Err1 = lin(EL_[0, 0]), lin(EL_[1, 1])
R1 = lin(geoL["R"])
box_u1 = lin(GM.box(geoL, eps * uf)); box_s1 = lin(GM.box(geoL, eps * sf))
R.P("    E_tt^(1) = " + str(Ett1)); R.P("    E_rr^(1) = " + str(Err1)); R.P("    R^(1) = " + str(R1))
# exact linear vacuum solution for r>0
mm = sp.sqrt(m2)
u_sol = 2 * Mg * sp.cos(mm * r) / r
s_sol = 2 * Mg * (sp.cos(mm * r) - 1) / (m2 * r)
Lam_sol = Mg / r - m2 / 6 * r * sp.diff(s_sol, r)
Phip_sol = Mg / r ** 2 + m2 / 6 * sp.diff(s_sol, r)
Phi_sol = -Mg / r + Mg / 3 * (sp.cos(mm * r) - 1) / r          # = integral of Phip_sol (checked below through its derivative)
assert sp.simplify(sp.diff(Phi_sol, r) - Phip_sol) == 0
subsol = lambda e: e.subs({Ph: Phi_sol, La: Lam_sol, uf: u_sol, sf: s_sol}).doit()
res = [sp.simplify(subsol(Ett1)), sp.simplify(subsol(Err1)), sp.simplify(subsol(box_u1 + R1)), sp.simplify(subsol(box_s1 + uf))]
R.P("    residuals of [E_tt, E_rr, box u + R, box s + u] on the exact linear vacuum solution (u = 2GM cos(mr)/r, s = 2GM (cos(mr)-1)/(m^2 r)): " + str(res))
R.check("T0c: the exact linear static vacuum solution satisfies E_tt = 0, E_rr = 0, box u = -R, box s = -u (symbolic, r > 0)", f"residuals {res}", all(q == 0 for q in res))
dPhi = sp.series((Phip_sol - Mg / r ** 2), m2, 0, 2).removeO()
S_lead = sp.series(s_sol, m2, 0, 1).removeO()
R.P(f"    leading order in m^2:  s -> {sp.simplify(S_lead)},   delta Phi' = Phi' - GM/r^2 -> {sp.simplify(dPhi)}")
dPhi_int = sp.integrate(dPhi, r)
expo = sp.simplify(sp.diff(dPhi_int, r) * r / dPhi_int)
R.P(f"    delta Phi = {sp.simplify(dPhi_int)}  (exponent of r: {expo});  delta g = delta Phi' = {sp.simplify(dPhi)} = -(m^2 r^2/6) g_N")
rho_eff = sp.simplify(sp.diff(r ** 2 * dPhi, r) / (4 * sp.pi * r ** 2) / 1)     # in units G = 1: rho_eff G = ...
R.P(f"    effective density (G = 1 units): G*rho_eff = (1/4 pi r^2) d(r^2 dg)/dr = {rho_eff}  ->  rho_eff = -m^2 M/(12 pi r):  c1 = -1/3 in rho_eff = c1 m^2 M/(4 pi r)")
R.check("T0c: exponent of r in delta Phi is exactly +1 (frozen line, literature-consistency only)", f"exponent = {expo}", expo == 1)
R.check("T0c: G rho_eff = -m^2 (GM)/(12 pi r): the response has the SIGN of a NEGATIVE density (weakens gravity); c1 = -1/3", f"G rho_eff = {rho_eff}",
        sp.simplify(rho_eff + m2 * Mg / (12 * sp.pi * r)) == 0)
R.num("c1_rho_eff_over_m2M_over_4pi_r", -1 / 3)
# leading-order local formula G rho_eff = m^2 Psi_N/(12 pi) with Psi_N the Newtonian potential (used in A2 for extended baryons)
R.P("    for spherical extended baryons the same steps give  rho_eff(r) = m^2 Psi_N(r)/(12 pi G)  (Psi_N <= 0, Psi_N -> 0 at infinity; U -> 0 zero-data prescription P0)")

# =============================================================================================================== T0d DW
R.banner("T0d  Deser-Woodard localised: T0a/T0b analogues and the linear static point-mass solution")
Xb = sp.Symbol("Xbar"); f0, f1, f2 = sp.symbols("f0 f1 f2")
Xf = sp.Function("X")(r); xif = sp.Function("xi")(r)
fX = f0 + f1 * (Xf - Xb) + f2 * (Xf - Xb) ** 2 / 2
EDW = GM.E_DW(geoS, fX, Xf, xif)
SDW = GM.scalar_eoms_DW(geoS, f1 + f2 * (Xf - Xb), Xf, xif)
RD = geoS["R"]
LD = al * be * r ** 2 * (RD * (1 + fX - xif) - (1 / be ** 2) * sp.diff(xif, r) * sp.diff(Xf, r))
ELD = euler_equations(LD, [al, be, Xf, xif], r)
eld = {k: e.lhs for k, e in zip(["al", "be", "X", "xi"], ELD)}
pD = {"al": 2 * be * r ** 2 * EDW[0, 0] / al ** 2, "be": -2 * al * r ** 2 * EDW[1, 1] / be ** 2, "X": al * be * r ** 2 * SDW["X"], "xi": al * be * r ** 2 * SDW["xi"]}
worstD = 0
for seed in (1, 2, 3):
    fs = {al: 1 + rnd_poly(r, 2, seed + 310) / 15, be: 1 + rnd_poly(r, 2, seed + 320) / 13, Xf: rnd_poly(r, 3, seed + 330), xif: rnd_poly(r, 3, seed + 340)}
    for k in eld:
        e = eld[k] - pD[k]
        for f_, v in fs.items():
            e = e.subs(f_, v)
        e = e.doit()
        for p in [sp.Rational(1, 3), sp.Rational(3, 2)]:
            worstD = max(worstD, abs(sp.N(sp.nsimplify(e.subs({r: p, f0: sp.Rational(1, 5), f1: sp.Rational(2, 7), f2: sp.Rational(-3, 8), Xb: sp.Rational(1, 3)})), 30)))
R.check("T0d: DW covariant E_mu nu and scalar EOMs equal the reduced-action Euler-Lagrange equations (exact)", f"max |residual| = {float(worstD):.3e}", worstD < 1e-20)
divD = div_r(EDW)
identD = divD - cs * (SDW["X"] * sp.diff(Xf, r) + SDW["xi"] * sp.diff(xif, r))
cD = []
for seed in (1, 2):
    fs = {al: 1 + rnd_poly(r, 2, seed + 410) / 15, be: 1 + rnd_poly(r, 2, seed + 420) / 13, Xf: rnd_poly(r, 3, seed + 430), xif: rnd_poly(r, 3, seed + 440)}
    e = identD
    for f_, v in fs.items():
        e = e.subs(f_, v)
    e = e.doit().subs({f0: sp.Rational(1, 5), f1: sp.Rational(2, 7), f2: sp.Rational(-3, 8), Xb: sp.Rational(1, 3)})
    vals = [sp.nsimplify(sp.simplify(e.subs({r: p, th: sp.Rational(1, 2)}))) for p in (sp.Rational(1, 3), sp.Rational(3, 2), sp.Rational(5, 2))]
    sol = sp.solve(vals[0], cs)
    cD.append(sol[0])
    assert all(abs(sp.N(v.subs(cs, sol[0]), 30)) < 1e-20 for v in vals)
R.check("T0d: DW Noether identity nabla^mu E_mu r = c sum E_phi d_r phi with one rational c", f"c = {cD}", len(set(cD)) == 1 and cD[0].is_rational)
# linear static point mass, background Xbar constants (flat-space local reading; cosmological time dependence NOT included)
xb = sp.Symbol("xibar"); xf_ = sp.Function("x")(r); zf_ = sp.Function("z")(r)
gL2 = gL
Xl = Xb + eps * xf_; xil = xb + eps * zf_
fXl = f0 + f1 * (Xl - Xb) + f2 * (Xl - Xb) ** 2 / 2
EDl = GM.E_DW(geoL, fXl, Xl, xil)
Ett_D, Err_D = lin(EDl[0, 0]), lin(EDl[1, 1])
SDl = GM.scalar_eoms_DW(geoL, f1 + f2 * (Xl - Xb), Xl, xil)
sX, sxi = lin(SDl["X"]), lin(SDl["xi"])
Fb = 1 + f0 - xb
Dn = Fb - 6 * f1
x_sol = -2 * Mg / (r * Dn); z_sol = 2 * f1 * Mg / (r * Dn)
Lam_D = Mg / r * (Fb - 4 * f1) / (Fb * Dn)
Phip_D = Mg / r ** 2 * (Fb - 8 * f1) / (Fb * Dn)
sub2 = lambda e: sp.simplify(e.subs({xf_: x_sol, zf_: z_sol, La: Lam_D}).subs(sp.Derivative(Ph, r), Phip_D).doit())
# Phi appears only through Phi' at linear order in E_rr and E_tt: substitute derivative
resD = [sub2(Ett_D), sub2(Err_D), sub2(sX), sub2(sxi)]
R.P("    DW residuals [E_tt, E_rr, scalar X eq, scalar xi eq] for x = -2GM/(r (Fbar-6f1)), z = 2 f1 GM/(r (Fbar-6f1)), Lam = (GM/r)(Fbar-4f1)/(Fbar(Fbar-6f1)), Phi' = (GM/r^2)(Fbar-8f1)/(Fbar(Fbar-6f1)): " + str(resD))
R.check("T0d: the DW linear static point-mass solution (G renormalisation and slip only) satisfies all four linear equations (symbolic, r > 0)", f"residuals {resD}", all(q == 0 for q in resD))
R.P("    => Phi' = (G M/r^2) * const: M_eff/M is the SAME constant at every r and every M (a pure G renormalisation); PPN slip gamma - 1 = 4 f1/(Fbar - 8 f1) (areal-gauge reading)")
R.num("DW_gamma_minus_1", "4 f1/(Fbar - 8 f1)")
sys.exit(finish(R, MUT))
