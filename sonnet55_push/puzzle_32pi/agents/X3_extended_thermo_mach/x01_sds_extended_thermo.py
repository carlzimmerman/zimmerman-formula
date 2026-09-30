#!/usr/bin/env python3
"""x01: Extended black-hole chemistry of Schwarzschild-de Sitter, D = 4, G = c = hbar-free.
P = -Lambda/(8 pi) = -rho_L (thermodynamic pressure), M = enthalpy, V = 4 pi r^3/3.
Everything symbolic (sympy).  Predeclared list: PREDECLARED.md (A1-A4, A7).
Pass/fail counting with controls that must FAIL when the claim is mutated."""
import sympy as sp
from sympy import pi, sqrt, Rational as R, symbols, simplify, diff, solve, S, nsimplify
import mpmath as mp

PASS = 0
FAIL = 0
CTRL_OK = 0
CTRL_BAD = 0


def chk(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok   {name} {detail}")
    else:
        FAIL += 1
        print(f"  FAIL {name} {detail}")


def ctrl(name, cond_should_be_false, detail=""):
    """A control: the mutated claim must be REJECTED (condition False)."""
    global CTRL_OK, CTRL_BAD
    if not cond_should_be_false:
        CTRL_OK += 1
        print(f"  ctrl-ok  {name} (mutation rejected) {detail}")
    else:
        CTRL_BAD += 1
        print(f"  CTRL-BAD {name} (mutation NOT rejected) {detail}")


def zero(e):
    return sp.simplify(sp.together(e)) == 0


r, Lam, P, M, T_, x, y = symbols('r Lambda P M T x y', positive=True)
Pn = symbols('P_n', real=True)  # signed pressure symbol

print("== A3: first laws and Smarr relations, symbolic, f-normalisation ==")
# f = 1 - 2M/r - Lambda r^2/3 with Lambda = -8 pi P
Lm = -8 * pi * Pn
fexpr = lambda rr, MM: 1 - 2 * MM / rr - Lm * rr ** 2 / 3
# mass as function of horizon radius (f(r_h) = 0)
Mh = sp.solve(sp.Eq(fexpr(r, M), 0), M)[0]
chk("M(r,P) = r/2 + 4 pi P r^3/3 from f(r_h) = 0", zero(Mh - (r / 2 + 4 * pi * Pn * r ** 3 / 3)))
fp = diff(fexpr(r, M), r)                       # f'(r) at fixed M
kap_b = sp.simplify((fp / 2).subs(M, Mh))       # kappa_b = f'(r_b)/2 (f-norm), BH horizon
kap_c = sp.simplify(-(fp / 2).subs(M, Mh))      # kappa_c = -f'(r_c)/2, cosmological horizon
Sbh = pi * r ** 2
Vth = 4 * pi * r ** 3 / 3
Tb = kap_b / (2 * pi)
Tc = kap_c / (2 * pi)
# BH horizon: dM = T dS + V dP
chk("BH first law dM/dr = T_b dS/dr", zero(diff(Mh, r) - Tb * diff(Sbh, r)))
chk("BH first law dM/dP = V_b = 4 pi r^3/3", zero(diff(Mh, Pn) - Vth))
# cosmological: dM = -T_c dS_c + V_c dP
chk("cosm. first law dM/dr = -T_c dS_c/dr", zero(diff(Mh, r) + Tc * diff(Sbh, r)))
chk("cosm. first law dM/dP = V_c = 4 pi r^3/3", zero(diff(Mh, Pn) - Vth))
# Smarr
chk("Smarr (BH):  M = 2 T_b S_b - 2 P V_b", zero(Mh - (2 * Tb * Sbh - 2 * Pn * Vth)))
chk("Smarr (cosm): M = -2 T_c S_c - 2 P V_c", zero(Mh - (-2 * Tc * Sbh - 2 * Pn * Vth)))
# mutations
ctrl("Smarr with wrong sign of PV", zero(Mh - (2 * Tb * Sbh + 2 * Pn * Vth)))
ctrl("first law with V = 4 pi r^3 (wrong volume)", zero(diff(Mh, Pn) - 4 * pi * r ** 3))
ctrl("Smarr with coefficient 1 instead of 2", zero(Mh - (Tb * Sbh - Pn * Vth)))

# between horizons (Dolan et al 1301.5926 Eq 22/23, opened via ar5iv): 0 = T_b dS_b + T_c dS_c - V dP ; T_b S_b + T_c S_c + P V = 0
# use a two-horizon parametrisation at the same M, Lambda: (x, y) with x^2 + x y + y^2 = 1 (L = 1)
Lval = 1
xs = symbols('xs', positive=True)
ys = (-xs + sqrt(4 - 3 * xs ** 2)) / 2                 # y(x) with x^2+xy+y^2=1
Pval = -R(3, 8) / pi                                     # Lambda = 3 (L=1)
Mx = xs * (1 - xs ** 2) / 2
chk("x^2 + x y + y^2 = 1 for the paired root", zero(xs ** 2 + xs * ys + ys ** 2 - 1))
chk("same M from both horizons: y(1-y^2)/2 = x(1-x^2)/2", zero(ys * (1 - ys ** 2) / 2 - Mx))
Tbx = (1 - 3 * xs ** 2) / (4 * pi * xs)
Tcx = (3 * ys ** 2 - 1) / (4 * pi * ys)
Sbx, Scx = pi * xs ** 2, pi * ys ** 2
Vx = 4 * pi * (ys ** 3 - xs ** 3) / 3
chk("between-horizon Smarr  T_b S_b + T_c S_c + P V = 0",
    zero(Tbx * Sbx + Tcx * Scx + Pval * Vx))
ctrl("between-horizon Smarr with V = V_c + V_b (wrong)", zero(Tbx * Sbx + Tcx * Scx + Pval * 4 * pi * (ys ** 3 + xs ** 3) / 3))
# first law between horizons: 0 = T_b dS_b + T_c dS_c - V dP: at fixed L we vary L (i.e. P) -> use general L
Lg = symbols('L_', positive=True)
xg = symbols('xg', positive=True)   # r_b / L
# variables (r_b, r_c) both functions of (M, L); check identity via implicit differentiation numerically instead
# symbolic: use r_b, r_c as independent variables with constraint that they share M and L
rb, rc = symbols('rb rc', positive=True)
# solve (M, L^2) from the two horizon conditions: f(rb)=f(rc)=0
# f(rb) = f(rc) = 0 at the same (M, L^2): solve for (M, L^2) as functions of the two horizon radii
Msol, Lsol = symbols('Msol Lsol', positive=True)
sol = sp.solve([1 - 2 * Msol / rb - rb ** 2 / Lsol, 1 - 2 * Msol / rc - rc ** 2 / Lsol], [Msol, Lsol], dict=True)[0]
Mrr, Lrr = sp.simplify(sol[Msol]), sp.simplify(sol[Lsol])   # Lrr = L^2
Prr = -3 / (8 * pi * Lrr)                                      # P = -Lambda/8pi, Lambda = 3/L^2
Tb_rr = sp.simplify((diff(1 - 2 * Mrr / r - r ** 2 / Lrr, r)).subs(r, rb) / 2 / (2 * pi))
Tc_rr = sp.simplify(-(diff(1 - 2 * Mrr / r - r ** 2 / Lrr, r)).subs(r, rc) / 2 / (2 * pi))
# first law between horizons as differential 1-form identity in (rb, rc)
form = []
for v in (rb, rc):
    lhs = Tb_rr * diff(pi * rb ** 2, v) + Tc_rr * diff(pi * rc ** 2, v) - (4 * pi * (rc ** 3 - rb ** 3) / 3) * diff(Prr, v)
    form.append(sp.simplify(lhs))
chk("between-horizon first law  0 = T_b dS_b + T_c dS_c - V dP  (2-parameter family, both partials)",
    all(zero(fm) for fm in form))
chk("dM = T_b dS_b + V_b dP on the (r_b, r_c) family",
    all(zero(diff(Mrr, v) - (Tb_rr * diff(pi * rb ** 2, v) + (4 * pi * rb ** 3 / 3) * diff(Prr, v))) for v in (rb, rc)))
chk("dM = -T_c dS_c + V_c dP on the (r_b, r_c) family",
    all(zero(diff(Mrr, v) - (-Tc_rr * diff(pi * rc ** 2, v) + (4 * pi * rc ** 3 / 3) * diff(Prr, v))) for v in (rb, rc)))

print("\n== A1/A2: potentials, in units L = 1, BH horizon x in (0, 1/sqrt3), cosmological y in (1/sqrt3, 1) ==")
Pv = -R(3, 8) / pi
subsL = {Lg: 1}
# BH horizon at x
Mb = x * (1 - x ** 2) / 2
Tb_x = (1 - 3 * x ** 2) / (4 * pi * x)
Sb_x = pi * x ** 2
Vb_x = 4 * pi * x ** 3 / 3
PV_b = sp.simplify(Pv * Vb_x)
Ub = sp.simplify(Mb - PV_b)
Gb = sp.simplify(Mb - Tb_x * Sb_x)
Fb = sp.simplify(Ub - Tb_x * Sb_x)
chk("U_b = M - P V = x/2 (Misner-Sharp mass of the horizon)", zero(Ub - x / 2))
chk("G_b = M - T S = (x/4)(1 + x^2)", zero(Gb - x * (1 + x ** 2) / 4))
chk("F_b = U - T S = (x/4)(1 + 3 x^2)", zero(Fb - x * (1 + 3 * x ** 2) / 4))
# cosmological horizon at y
Mc = y * (1 - y ** 2) / 2
Tc_y = (3 * y ** 2 - 1) / (4 * pi * y)
Sc_y = pi * y ** 2
Vc_y = 4 * pi * y ** 3 / 3
PV_c = sp.simplify(Pv * Vc_y)
Ec = -Mc
Gc = sp.simplify(Ec - Tc_y * Sc_y)
Uc = sp.simplify(Ec + PV_c)   # H_c = -M = U_c + P (-V_c)  =>  U_c = -M + P V_c
chk("G_c = -M - T_c S_c = -(y/4)(1 + y^2)", zero(Gc + y * (1 + y ** 2) / 4))
chk("U_c = -M + P V_c = -y/2", zero(Uc + y / 2))
chk("pure dS (y = 1, M = 0): G = -1/2 (= -L/2)", zero(Gc.subs(y, 1) + R(1, 2)))
dG = sp.simplify(Gb.subs(x, x) + Gc.subs(y, ys.subs(xs, x)) + R(1, 2))
print("   excess pair Gibbs over pure dS  dG(x) =", sp.simplify(dG))

def roots_in(expr, var, lo, hi, n=4000):
    """sign changes + numeric roots of expr(var) on (lo, hi) with mpmath (detect interior zeros)."""
    f = sp.lambdify(var, expr, 'mpmath')
    pts = [lo + (hi - lo) * (k + R(1, 2)) / n for k in range(n)]
    vals = [f(mp.mpf(float(p))) for p in pts]
    changes = [(float(pts[i]), float(pts[i + 1])) for i in range(n - 1) if vals[i] * vals[i + 1] < 0]
    return changes, min(vals), max(vals)

xN = 1 / sqrt(3)
# detector control: a function with a planted interior zero must be found
ch, _, _ = roots_in(x - R(1, 5), x, R(1, 1000), xN)
chk("detector finds the planted zero of x - 1/5", len(ch) == 1)
ch0, _, _ = roots_in(x + R(1, 5), x, R(1, 1000), xN)
chk("detector reports no zero for x + 1/5 (no false positives)", len(ch0) == 0)
for nm, ex, lo, hi in [
        ("G_b(x)", Gb, R(1, 1000), xN), ("F_b(x)", Fb, R(1, 1000), xN), ("U_b(x)", Ub, R(1, 1000), xN),
        ("M(x)", Mb, R(1, 1000), xN)]:
    ch, mn, mxv = roots_in(ex, x, lo, hi)
    chk(f"{nm}: no sign change on the BH domain (min {float(mn):.4g}, max {float(mxv):.4g})", len(ch) == 0 and mn > 0)
for nm, ex in [("G_c(y)", Gc), ("U_c(y)", Uc)]:
    ch, mn, mxv = roots_in(ex, y, xN + R(1, 10 ** 4), 1)
    chk(f"{nm}: no sign change on the cosmological domain (max {float(mxv):.4g})", len(ch) == 0 and mxv < 0)
ch, mn, mxv = roots_in(dG, x, R(1, 1000), xN)
chk(f"pair Gibbs excess dG(x) over pure dS: no sign change (min {float(mn):.4g}); it is >0 => SdS never favoured over dS",
    len(ch) == 0 and mn > 0)
# off-shell free energy at a heat bath T: F(r;T) = M - T S ; extremum at T_b(r) = T, is a maximum (barrier)
TT = symbols('TT', positive=True)
Foff = Mb - TT * Sb_x
dF = diff(Foff, x)
chk("dF/dx = 0 <=> T = T_b(x)", zero(dF - (R(1, 2) - R(3, 2) * x ** 2 - 2 * pi * TT * x)) and
    zero((dF.subs(TT, Tb_x))))
chk("d2F/dx2 = -3x - 2 pi T < 0 at the extremum for every x (a barrier, not a minimum)",
    zero(diff(Foff, x, 2) - (-3 * x - 2 * pi * TT)) and
    all(float(diff(Foff, x, 2).subs(TT, Tb_x).subs(x, xv)) < 0 for xv in [0.01, 0.2, 0.4, 0.55, 0.577]))
# T_b = T_dS = 1/(2 pi) (L = 1)
xbath = [s_ for s_ in solve(sp.Eq(Tb_x, 1 / (2 * pi)), x) if s_.is_positive][0]
chk("bath temperature T = T_dS: x = 1/3 exactly", sp.simplify(xbath - R(1, 3)) == 0)
chk("barrier height at T = T_dS: F_ext = G_b(1/3) = 5/54 L, positive", sp.simplify(Gb.subs(x, R(1, 3))) == R(5, 54))

print("\n== A2: heat capacities and response functions (fixed P) ==")
rr_, PP = symbols('rr PP', real=True)
Tgen = (1 + 8 * pi * PP * rr_ ** 2) / (4 * pi * rr_)   # T_b(r, P) = (1 - Lambda r^2)/(4 pi r)
Sgen = pi * rr_ ** 2
Vgen = 4 * pi * rr_ ** 3 / 3
Mgen = rr_ / 2 + 4 * pi * PP * rr_ ** 3 / 3
CP_b = sp.simplify(Tgen * diff(Sgen, rr_) / diff(Tgen, rr_))
chk("C_P,b = -2 pi r^2 (1 - Lambda r^2)/(1 + Lambda r^2)", zero(CP_b - (-2 * pi * rr_ ** 2 * (1 + 8 * pi * PP * rr_ ** 2) / (1 - 8 * pi * PP * rr_ ** 2))))
CPx = sp.simplify(CP_b.subs(PP, Pv).subs(rr_, x))
chk("C_P,b/S = -2 (1 - 3x^2)/(1 + 3x^2)", zero(CPx / Sb_x + 2 * (1 - 3 * x ** 2) / (1 + 3 * x ** 2)))
ch, mn, mxv = roots_in(CPx, x, R(1, 1000), xN)
chk(f"C_P,b < 0 on the whole BH domain, no sign change (max {float(mxv):.3g}); zero only at Nariai x = 1/sqrt3",
    len(ch) == 0 and mxv < 0 and sp.simplify(CPx.subs(x, xN)) == 0)
ctrl("mutation: C_P,b with sign flipped is positive", float(CPx.subs(x, 0.3)) > 0)
# cosmological horizon: T_c(y,P) = (Lambda y^2 - 1)/(4 pi y); dM = -T_c dS_c  => energy E_c = -M; C = T dS/dT
Tcgen = (-1 - 8 * pi * PP * rr_ ** 2) / (4 * pi * rr_)
CP_c = sp.simplify(Tcgen * diff(Sgen, rr_) / diff(Tcgen, rr_))
CPcy = sp.simplify(CP_c.subs(PP, Pv).subs(rr_, y))
chk("C_P,c/S = 2 (3y^2 - 1)/(3y^2 + 1)", zero(CPcy / Sc_y - 2 * (3 * y ** 2 - 1) / (3 * y ** 2 + 1)))
ch, mn, mxv = roots_in(CPcy, y, xN + R(1, 10 ** 4), 1)
chk(f"C_P,c > 0 on the whole cosmological domain (min {float(mn):.3g}); zero only at Nariai", len(ch) == 0 and mn > 0)
# C_V = T (dS/dT)_V : S and V are both functions of r only
chk("(dS/dr)/(dV/dr) = 1/(2 r): S is a function of V alone => C_V = 0 identically (isochoric = isentropic)",
    zero(diff(Sgen, rr_) / diff(Vgen, rr_) - 1 / (2 * rr_)))
# thermal expansion, isothermal compressibility, Joule-Thomson (BH horizon)
# implicit differentiation
dr_dP_at_T = -diff(Tgen, PP) / diff(Tgen, rr_)                   # (dr/dP)_T
dr_dP_at_M = -diff(Mgen, PP) / diff(Mgen, rr_)                   # (dr/dP)_M
kT = sp.simplify(-(1 / Vgen) * diff(Vgen, rr_) * dr_dP_at_T)     # isothermal compressibility
alpha = sp.simplify((1 / Vgen) * diff(Vgen, rr_) / diff(Tgen, rr_))   # thermal expansion at fixed P
muJT = sp.simplify(diff(Tgen, PP) + diff(Tgen, rr_) * dr_dP_at_M)     # (dT/dP)_M
kTx = sp.simplify(kT.subs(PP, Pv).subs(rr_, x))
alx = sp.simplify(alpha.subs(PP, Pv).subs(rr_, x))
mux = sp.simplify(muJT.subs(PP, Pv).subs(rr_, x))
print("   kappa_T(x) =", sp.factor(kTx), "   alpha(x) =", sp.factor(alx), "   mu_JT(x) =", sp.factor(mux))
inv = [s_ for s_ in solve(sp.numer(sp.together(mux)), x) if s_.is_real and s_ > 0]
print("   Joule-Thomson inversion roots (x>0):", inv)
chk("Joule-Thomson: no inversion point inside the BH domain (x <= 1/sqrt3)", all(float(s_) > float(xN) for s_ in inv) or len(inv) == 0,
    f"roots {[float(s_) for s_ in inv]}")
chk("kappa_T sign is constant on the BH domain",
    all((float(kTx.subs(x, xv)) > 0) == (float(kTx.subs(x, 0.3)) > 0) for xv in [0.01, 0.1, 0.2, 0.4, 0.5, 0.57]))
chk("thermal expansion alpha < 0 on the BH domain (T falls as r rises)",
    all(float(alx.subs(x, xv)) < 0 for xv in [0.01, 0.1, 0.2, 0.4, 0.5, 0.57]))

print("\n== A3 (isoperimetric ratios) ==")
Riso_b = sp.simplify(((3 * Vb_x / (4 * pi)) ** R(1, 3)) / ((4 * pi * x ** 2 / (4 * pi)) ** R(1, 2)))
chk("isoperimetric ratio of the BH thermodynamic volume V_b = 4 pi r^3/3 against its own area is exactly 1 (saturated)", sp.simplify(Riso_b - 1) == 0)
Reff = ((ys ** 3 - xs ** 3) ** R(1, 3)) / sqrt(xs ** 2 + ys ** 2)      # R = (3V/4pi)^{1/3} (4 pi/A_tot)^{1/2}, A_tot = 4 pi (rb^2+rc^2)
vals = [float(Reff.subs(xs, xv)) for xv in [0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.5773]]
chk("between-horizon isoperimetric ratio R <= 1 and decreasing from 1 (pure dS) to 0 (Nariai) (Dolan et al. claim R <= 1)",
    all(v <= 1 + 1e-12 for v in vals) and all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)), f"R = {['%.4f' % v for v in vals]}")
ctrl("mutation: R >= 1 claimed", all(v >= 1 for v in vals))

print("\n== A4: natural equalities (BH horizon, cosmological horizon, flat probe) and the resulting a0^2/(G rho_L) ==")
# a0^2/(G rho_L) = kappa^2 * 8 pi / 3   (L = 1, G rho_L = 3/(8 pi))
def ratio_from_kappa(kap):
    return sp.simplify(kap ** 2 * 8 * pi / 3)
kb_x = (1 - 3 * x ** 2) / (2 * x)
kc_y = (3 * y ** 2 - 1) / (2 * y)
qb = {"M": Mb, "2TS": 2 * Tb_x * Sb_x, "2|PV|": -2 * PV_b, "TS": Tb_x * Sb_x, "|PV|": -PV_b, "U": Ub, "F": Fb, "G": Gb}
rows = []
import itertools
names = list(qb.keys())
for (n1, n2), (a, b) in itertools.product(itertools.combinations(names, 2), [(1, 1)]):
    eq = sp.simplify(qb[n1] - qb[n2])
    sols = [s_ for s_ in solve(sp.numer(sp.together(eq)), x) if s_.is_real and s_ > 0 and s_ < xN]
    for s_ in sols:
        rows.append((f"{n1} = {n2}", s_, sp.nsimplify(kb_x.subs(x, s_)), ratio_from_kappa(kb_x.subs(x, s_))))
print("   BH-horizon natural equalities (interior of BH domain):")
alg_ok = True
for nm, s_, K, rat in rows:
    print(f"     {nm:12s}  x = {sp.simplify(s_)}  kappa_b/H = {sp.simplify(K)}  a0^2/(G rho_L) = {sp.simplify(rat)} = {float(rat):.5f}")
    alg_ok = alg_ok and bool(sp.simplify(K).is_algebraic)
    # would need rat = 1/4: equivalent to pi = 3/(32 K^2), algebraic if K algebraic
    alg_ok = alg_ok and bool(sp.simplify(3 / (32 * K ** 2)).is_algebraic) and (abs(float(rat) - 0.25) > 1e-6)
chk(f"every BH-horizon natural equality selects an ALGEBRAIC kappa/H and a0^2/(G rho_L) != 1/4 ({len(rows)} equalities)", alg_ok and len(rows) >= 3)
# bath equalities
extra = [("T_b = T_dS (bath)", R(1, 3))]
for nm, s_ in extra:
    K = sp.simplify(kb_x.subs(x, s_))
    rat = ratio_from_kappa(K)
    print(f"     {nm:12s}  x = {s_}  kappa_b/H = {K}  a0^2/(G rho_L) = {sp.simplify(rat)} = {float(rat):.5f}")
    chk(f"{nm}: kappa_b/H = 1 exactly (a0 = H, i.e. Z times the framework's), a0^2/(G rho_L) = 8 pi/3", sp.simplify(K - 1) == 0 and sp.simplify(rat - 8 * pi / 3) == 0)
# T_b = T_c: Nariai
chk("T_b = T_c only at Nariai (x = y = 1/sqrt3)",
    sp.simplify((Tbx - Tcx).subs(xs, 1 / sqrt(3))) == 0 and abs(float((Tbx - Tcx).subs(xs, 0.4))) > 1e-3)
# cosmological horizon equalities
qc = {"M": Mc, "2TS": 2 * Tc_y * Sc_y, "2|PV|": -2 * PV_c, "TS": Tc_y * Sc_y, "|PV|": -PV_c}
rowsc = []
for (n1, n2) in itertools.combinations(list(qc.keys()), 2):
    eq = sp.simplify(qc[n1] - qc[n2])
    sols = [s_ for s_ in solve(sp.numer(sp.together(eq)), y) if s_.is_real and s_ > xN and s_ <= 1]
    for s_ in sols:
        rowsc.append((f"{n1} = {n2}", s_, sp.simplify(kc_y.subs(y, s_))))
print("   cosmological-horizon natural equalities (interior):")
okc = True
for nm, s_, K in rowsc:
    rat = ratio_from_kappa(K)
    print(f"     {nm:12s}  y = {sp.simplify(s_)}  kappa_c/H = {K}  a0^2/(G rho_L) = {sp.simplify(rat)} = {float(rat):.5f}")
    okc = okc and bool(sp.simplify(K).is_algebraic) and (abs(float(rat) - 0.25) > 1e-6)
chk(f"every cosmological-horizon natural equality: algebraic kappa_c/H, a0^2/(G rho_L) != 1/4 ({len(rowsc)} found)", okc)

# flat probe: M = r/2, TS = r/4, F = r/4, |PV| = s r/2, U = r(1+s)/2  with s = r^2/L^2 = (8 pi/3) G rho_L r^2
s_ = symbols('s', positive=True)
rr0 = symbols('r0', positive=True)
Mfl = rr0 / 2
TSfl = rr0 / 4
PVfl = s_ * rr0 / 2
Ufl = Mfl + PVfl
Ffl = Ufl - TSfl
Gfl = Mfl - TSfl
flat = {"M": Mfl, "2TS": 2 * TSfl, "2|PV|": 2 * PVfl, "TS": TSfl, "|PV|": PVfl, "U": Ufl, "F": Ffl, "G": Gfl}
Lsym = symbols('Lsym', positive=True)
PVdirect = (-3 / (8 * pi * Lsym ** 2)) * (4 * pi * rr0 ** 3 / 3)     # P = -Lambda/8pi, Lambda = 3/L^2, V = 4 pi r^3/3
chk("flat probe: |PV|/M = r^2/L^2 (computed from V = 4 pi r^3/3, P = -Lambda/8pi, M = r/2)",
    zero(-PVdirect / Mfl - rr0 ** 2 / Lsym ** 2))
# tie s to G rho r^2 explicitly
Grho, rsq = symbols('Grho rsq', positive=True)
sfun = 8 * pi * Grho * rsq / 3
chk("s = r^2/L^2 with L^2 = 3/Lambda = 3/(8 pi G rho): s = (8 pi/3) G rho r^2", zero(sfun - rsq / (3 / (8 * pi * Grho))))
rows_f = []
for (n1, n2) in itertools.combinations(list(flat.keys()), 2):
    eq = sp.simplify(flat[n1] - flat[n2])
    sols = [v for v in solve(sp.numer(sp.together(eq)), s_) if v.is_real and v > 0]
    for v in sols:
        rows_f.append((f"{n1} = {n2}", v))
print("   flat-probe natural equalities and a0^2/(G rho_L) = 2 pi/(3 s):")
okf = True
for nm, v in rows_f:
    rat = 2 * pi / (3 * v)
    print(f"     {nm:12s}  s = {v}  a0^2/(G rho_L) = {sp.simplify(rat)} = {float(rat):.5f}   (puzzle needs s = 8 pi/3 = {float(8*pi/3):.4f})")
    okf = okf and v.is_rational and abs(float(rat) - 0.25) > 1e-6
chk(f"every flat-probe natural equality gives RATIONAL s, hence G rho r^2 = 3s/(8 pi) and a0^2/(G rho_L) != 1/4 ({len(rows_f)} equalities)", okf and len(rows_f) >= 4)
chk("the puzzle is s = 8 pi/3 (irrational): 2 pi/(3 s) = 1/4 <=> s = 8 pi/3",
    sp.simplify(sp.solve(sp.Eq(2 * pi / (3 * s_), R(1, 4)), s_)[0] - 8 * pi / 3) == 0 and (8 * pi / 3).is_rational is False)
ctrl("mutation: a rational s reproduces 1/4", any(abs(2 * float(pi) / (3 * float(v)) - 0.25) < 1e-6 for _, v in rows_f))

print("\n== A7 theorem (Lambda-units): algebraic x  ==>  a0^2/(G rho_L) = (8 pi/3) K^2 transcendental ==")
Kg = symbols('K', positive=True)
sol_eq = solve(sp.Eq(8 * pi * Kg ** 2 / 3, R(1, 4)), Kg)
chk("a0^2/(G rho_L) = 1/4  <=>  K^2 = 3/(32 pi)", any(sp.simplify(sv - sqrt(3 / (32 * pi))) == 0 for sv in sol_eq))
chk("K = sqrt(3/(32 pi)) is NOT algebraic (sympy assumptions: pi transcendental)", sqrt(3 / (32 * pi)).is_algebraic is False)
chk("kappa_b L = K  <=>  x = (sqrt(K^2 + 3) - K)/3 (algebraic iff K is); K = 1/Z gives x_b = (sqrt(1+32 pi) - 1)/sqrt(96 pi)",
    sp.simplify(((sqrt(Kg ** 2 + 3) - Kg) / 3).subs(Kg, sqrt(3 / (32 * pi))) - (sqrt(1 + 32 * pi) - 1) / sqrt(96 * pi)) == 0)
chk("consistency: kappa_b(x) at that x equals K (round trip)", sp.simplify(kb_x.subs(x, (sqrt(Kg ** 2 + 3) - Kg) / 3) - Kg) == 0)
print(f"\n== TOTAL: {PASS} checks pass, {FAIL} fail; controls rejected {CTRL_OK}, not rejected {CTRL_BAD} ==")
import sys
sys.exit(0 if (FAIL == 0 and CTRL_BAD == 0) else 1)
