#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_A1_point_mass_algebra -- sympy: point-mass charge function R(x) for V0, K1, K2 (=B2=B1), K3, B4; the uniqueness statement;
log-barrier Lagrangians; attempts to derive the constitutive function D(E) (grade M2) from stated families; controls C1-C4, C9.
Frozen: CFG231_FROZEN_CRITERIA.md sections 1.3, 2, 4, 6.   Exit 0 if every reproduction control passes.
MUTATE modes here: none (A1 is analytic).
"""
import sys, os, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C
from scipy.integrate import quad

R = C.Report("CFG231_A1_point_mass_algebra")
C.header(R, "CFG231 A1 -- point-mass algebra (sympy) and the constitutive-function derivation attempts")

x = sp.symbols("x", positive=True)
f = sp.Function("f")

# ---------------------------------------------------------------------------------------------------- charge function in general
R.banner("A1.0  the point-mass charge function for g_tot = g_N (1 + f(x)),  x = r/r_M,  r_M = sqrt(G M/a)")
# M_D = M f(x) (dark mass of the ADDED reading);  rho_D = M_D'/(4 pi r^2);  g_tot = a (1+f)/x^2;  a0_target = a
# C = rho_D r^3 g_tot = (M f'(x)/(4 pi r_M r^2)) r^3 a (1+f)/x^2 ;  C_T = a M/(4 pi)  =>  R = f'(1+f)/x
Rgen = lambda F: sp.simplify(sp.diff(F, x) * (1 + F) / x)
R.P("  general:  R(x) = f'(x)(1+f(x))/x = d[(1+f)^2]/d(x^2)")
uniq = sp.dsolve(sp.Eq(sp.Derivative(f(x), x) * (1 + f(x)) / x, 1), f(x))
R.P(f"  sympy dsolve of R = 1:  {uniq}")
# (1+f)^2 = x^2 + c, with f(0) = 0 (Newtonian limit) -> c = 1
c1 = sp.symbols("C1")
sol = [s_.rhs for s_ in (uniq if isinstance(uniq, list) else [uniq])]
R.P(f"  solutions: {sol}")
F_P2 = sp.sqrt(1 + x ** 2) - 1
F_V = x
F_K3 = (sp.sqrt(1 + 4 * x ** 2) - 1) / 2
R_P2, R_V, R_K3 = Rgen(F_P2), Rgen(F_V), Rgen(F_K3)
R.P(f"  K1 (P2): f = sqrt(1+x^2)-1      -> R = {R_P2}")
R.P(f"  K2/B1/B2 (Verlinde point mass): f = x -> R = {R_V}")
R.P(f"  K3 (simple wall): f = (sqrt(1+4x^2)-1)/2 -> R = {sp.simplify(R_K3)}")
# B4: total-mass reading, M_tot = M x, dark = M(x-1), g_tot = a/x (no added M_b): rho_D = M/(4 pi r_M r^2), R = x*... compute
Mtot = x   # in units of M
rhoD_B4 = sp.diff(Mtot, x)                        # M/(4 pi r_M r^2) up to the common factor
g_B4 = sp.Integer(1) / x                          # in units of a
R_B4 = sp.simplify(rhoD_B4 * x * g_B4)            # r^3 rho_D g / (a M /4pi) with r = x r_M  ->  (1)*(x)*(1/x)
R.P(f"  B4 (total-mass reading, point mass): M_tot = M x, g_tot = a/x -> R = {R_B4};  dark mass M(x-1) < 0 for x < 1; g_tot/g_N = x < 1 for x < 1")

# ---------------------------------------------------------------------------------------------------- C1
R.banner("C1  CFG44 point-mass identities (sympy, then numerics to 1e-6 against the read-only Bcommon target)")
res1 = sp.simplify(Rgen(F_P2) - 1)
Mc = sp.simplify(sp.sqrt(1 + x ** 2) - 1)
gsq = sp.simplify(((1 + F_P2) ** 2) - (1 + x ** 2))
R.P(f"  R(K1) - 1 = {res1};  M_c/M = {Mc};  (1+f)^2 - (1+x^2) = {gsq}")
a0k = C.AKPC(C.A0_SI["canonical"])
M = 1e10
pm = BC = C.BC.point_mass(M)
TF = C.BC.target_fields(pm, a0=a0k)
rr = np.asarray(TF["r"])
rM = C.r_M_kpc(M, a0k)
sel = (rr / rM > 0.05) & (rr / rM < 50)
rho_T = np.asarray(TF["rho"])[sel]
rho_cf = a0k / (4 * math.pi * C.G * rr[sel] * np.sqrt(1 + (rr[sel] / rM) ** 2))
dev = float(np.max(np.abs(rho_T / rho_cf - 1)))
cell = C.G1_cell("K1", "point", 1e10, C.a_V_si("HL"), "shape")
R.P(f"  Bcommon target rho_c vs closed form a0/(4 pi G r sqrt(1+x^2)): max rel dev {dev:.2e};  K1 numeric R: max|R-1| = {cell['maxdev']:.2e}")
R.check("C1 CFG44 point-mass identities: R(K1) = 1 exactly, M_c = M(sqrt(1+x^2)-1), g^2 = g_N^2 + a g_N (sympy); numerics and Bcommon target to 1e-6",
        f"sympy residuals {res1}, {gsq}; Bcommon dev {dev:.1e}; numeric max|R-1| {cell['maxdev']:.1e}", res1 == 0 and gsq == 0 and dev < 1e-6 and cell["maxdev"] < 1e-6)

# ---------------------------------------------------------------------------------------------------- C2
R.banner("C2  point-mass uniqueness: R = f'(1+f)/x = 1  <=>  (1+f)^2 = 1 + x^2")
ok2 = any(sp.simplify(sp.simplify(s_.subs(c1, 0)) - 0) is not None for s_ in sol)
# direct: d[(1+f)^2]/d(x^2) = f'(1+f)/x  (identity), so R=1 <=> (1+f)^2 = x^2 + const
u = sp.symbols("u", positive=True)  # u = x^2
ident = sp.simplify(sp.diff((1 + f(x)) ** 2, x) / (2 * x) - sp.diff(f(x), x) * (1 + f(x)) / x)
R.P(f"  identity  d[(1+f)^2]/d(x^2) - f'(1+f)/x = {ident}")
# check the dsolve family: (1+f)^2 - x^2 constant
fam_ok = True
for s_ in sol:
    val = sp.simplify((1 + s_) ** 2 - x ** 2)
    R.P(f"    (1+f)^2 - x^2 for dsolve branch {s_}: {val}")
    fam_ok = fam_ok and val.free_symbols <= {c1}
R.check("C2 the point-mass condition R = 1 pins (1+f)^2 - x^2 to a constant (sympy); Newtonian limit f(0) = 0 fixes it to 1, i.e. P2 exactly",
        f"identity residual {ident}; dsolve branches all have (1+f)^2 - x^2 = const", ident == 0 and fam_ok)

# ---------------------------------------------------------------------------------------------------- C3
R.banner("C3  Verlinde point mass: M_D = M x and R = (1+x)/x (derived independently)")
M_, r_, a_, G_ = sp.symbols("M r a G", positive=True)
MDv = sp.sqrt(a_ * r_ ** 2 * (M_ + r_ * 0) / G_)                 # point mass: d(M r)/dr = M, rho_b = 0 outside the origin
MDv_deriv_form = sp.sqrt(a_ * r_ ** 2 / G_ * sp.diff(M_ * r_, r_))
rM_ = sp.sqrt(G_ * M_ / a_)
xs_ = r_ / rM_
chk = sp.simplify(MDv_deriv_form / (M_ * xs_))
Cv = sp.diff(MDv, r_) / (4 * sp.pi * r_ ** 2) * r_ ** 3 * (G_ * (M_ + MDv) / r_ ** 2)
Rv = sp.simplify(Cv / (a_ * M_ / (4 * sp.pi)))
Rv_x = sp.simplify(Rv.subs(r_, x * rM_) )
R.P(f"  M_D/(M x) = {chk};  R(x) = {sp.simplify(Rv_x)}")
ok3 = sp.simplify(Rv_x - (1 + x) / x) == 0 and chk == 1
c3num = C.G1_cell("K2", "point", 1e10, C.a_V_si("HL"), "shape")
xn = [float(C.XGRID[int(np.argmin(np.abs(C.XGRID - xx)))]) for xx in (0.1, 1, 3, 10, 30)]      # the actual nodes used for R_at
d3 = max(abs(v - (1 + xx) / xx) for v, xx in zip(c3num['R_at'], xn))
R.P(f"  numeric K2 R at the nodes nearest x = 0.1, 1, 3, 10, 30 ({[round(t, 5) for t in xn]}): {[round(v, 6) for v in c3num['R_at']]} ; (1+x)/x at those nodes = {[round((1 + xx) / xx, 6) for xx in xn]}")
R.check("C3 Verlinde point mass: M_D = M x, R = (1+x)/x (sympy; numeric at the actual nodes to 1e-6)", f"symbolic ok {ok3}; numeric max dev {d3:.1e}", ok3 and d3 < 1e-6)

# ---------------------------------------------------------------------------------------------------- C4
R.banner("C4  K3: R = 1 + 1/sqrt(1+4x^2)")
ok4 = sp.simplify(sp.simplify(R_K3) - (1 + 1 / sp.sqrt(1 + 4 * x ** 2))) == 0
c4 = C.G1_cell("K3", "point", 1e10, C.a_V_si("HL"), "shape")
xs = (0.1, 1, 3, 10, 30)
xn4 = [float(C.XGRID[int(np.argmin(np.abs(C.XGRID - xx)))]) for xx in xs]
c4dev = max(abs(v - (1 + 1 / math.sqrt(1 + 4 * xx * xx))) for v, xx in zip(c4["R_at"], xn4))
inband = [xx for xx in np.geomspace(0.1, 30, 5000) if abs(1 / math.sqrt(1 + 4 * xx * xx)) <= 0.1]
R.P(f"  R(0.1, 1, 3, 10, 30) = {[round(v, 4) for v in c4['R_at']]};  within 10% only for x >= {min(inband):.3f}  (hand: 4.98)")
R.check("C4 K3 closed form R = 1 + 1/sqrt(1+4x^2) (sympy) and numerics to 1e-9", f"sympy ok {ok4}; numeric dev {c4dev:.1e}", ok4 and c4dev < 1e-9)
R.num("K3_in_band_from_x", min(inband))
R.num("R_point_mass", dict(K1=cell["R_at"], K2=c3num["R_at"], K3=c4["R_at"]))

# ---------------------------------------------------------------------------------------------------- Lagrangians
R.banner("A1.1  Lagrangians: D(E) = 4 pi G dL/dE  =>  L(E) = (1/4 pi G) int_0^E D dE'   (closed forms, sympy vs quadrature)")
E, a = sp.symbols("E a", positive=True)
Ds = {"K1": E ** 2 / (a - 2 * E), "K2": E ** 2 / a, "K3": E ** 2 / (a - E)}
allok = True
for k, D in Ds.items():
    IntD = sp.simplify(sp.integrate(D, (E, 0, E)))
    IntD2 = sp.simplify(sp.integrate(D.subs(E, sp.Symbol("t", positive=True)), (sp.Symbol("t", positive=True), 0, E)))
    R.P(f"  {k}: D = {D};  int_0^E D dE' = {IntD}")
    for Ev in (0.13, 0.31, 0.44):
        av = 1.0
        if k == "K3" and Ev >= av:
            continue
        num = quad(lambda t: float(D.subs({E: t, a: av})), 0, Ev)[0]
        cf = float(C.int_D(k, np.array(Ev), av))
        allok = allok and abs(num - cf) < 1e-9
R.check("A1.1 the closed-form int D dE (used by V2 and G3) equals quadrature for K1, K2, K3", f"all agree to 1e-9: {allok}", allok)
R.P("  K1: L = (1/4 pi G)[ -E^2/4 - aE/4 - (a^2/8) ln(1 - 2E/a) ]   (a logarithmic barrier at E = a/2; deep limit E^3/(6 a));  K3: barrier at E = a")

# ---------------------------------------------------------------------------------------------------- M2 attempts
R.banner("A1.2  attempts to DERIVE D(E) = E^2/(a-2E) (grade M2) from stated families (each attempt recorded; failures kept)")
# family (i) Born-Infeld / DBI: D = E/sqrt(1 - E^2/Em^2).  small E: D ~ E (Coulomb), no deep limit D ~ E^2/a  -> g_D ~ g_N, no MOND regime
Em = sp.symbols("E_m", positive=True)
DBI = E / sp.sqrt(1 - E ** 2 / Em ** 2)
lim_small = sp.limit(DBI / E, E, 0)
R.P(f"  (i) Born-Infeld-type: D/E -> {lim_small} as E -> 0 (linear response): E = g_N at small fields: the deep regime g ~ sqrt(a g_N) is absent for every E_m -> FAIL as a derivation")
fail_i = (lim_small == 1)
# family (ii) AQUAL power law: D = E^p/a^(p-1): p = 2 is K2; the wall is absent (no pole) -> no Newtonian regime
R.P("  (ii) AQUAL power law D = E^p/a^{p-1}: p = 2 gives K2 (deep-only); it has no wall and hence g_D -> sqrt(a g_N) >> g_N at every g_N (no Newtonian regime) -> FAIL for the inner regime")
# family (iii) walled power: D = (E^2/a)/(1 - E/E_w)^p; match to K1 at all E: unique (p, E_w) = (1, a/2)
p_, Ew = sp.symbols("p E_w", positive=True)
fam = (E ** 2 / a) / (1 - E / Ew) ** p_
ratio = sp.simplify(fam / (E ** 2 / (a - 2 * E)))
# require equality at three E values -> solve
eqs = [sp.Eq(fam.subs({E: e_, a: 1}), (e_ ** 2 / (1 - 2 * e_))) for e_ in (sp.Rational(1, 10), sp.Rational(1, 5))]
try:
    s_ = sp.nsolve(eqs, (p_, Ew), (1.2, 0.6))
    p_fit, Ew_fit = float(s_[0]), float(s_[1])
except Exception as e:                                                        # noqa
    p_fit, Ew_fit = float("nan"), float("nan")
third = float(fam.subs({E: sp.Rational(3, 10), a: 1, p_: p_fit, Ew: Ew_fit}) - (0.09 / (1 - 0.6)))
R.P(f"  (iii) walled power family (E^2/a)/(1-E/E_w)^p: matching K1 at two points gives (p, E_w) = ({p_fit:.6f}, {Ew_fit:.6f}) (a = 1), residual at a third point {third:.1e}:"
    " the family CONTAINS K1 only at the fitted point (p = 1, E_w = a/2); nothing stated (symmetry, action, Lambda-tie) fixes p or E_w -> declared, M1")
ok_iii = abs(p_fit - 1) < 1e-6 and abs(Ew_fit - 0.5) < 1e-6
# family (iv) dimensional analysis: with the single scale a, D/a is an arbitrary function of E/a
R.P("  (iv) dimensional analysis: with one scale a, D(E)/a = F(E/a) for an ARBITRARY F; the Lambda-tie fixes a, not F. No symmetry of the reduced electrostatic action fixes F. -> no M2 derivation.")
# family (v): what the point-mass condition R = 1 itself demands of D
Dt = sp.symbols("D_", positive=True)
gN_ = sp.symbols("g_N", positive=True)
Dp2 = sp.simplify(sp.solve(sp.Eq((gN_ + E) ** 2, gN_ ** 2 + a * gN_), gN_)[0])
R.P(f"  (v) inverting P2 for g_N(E): g_N = {Dp2}  (= D(E)); so D(E) = E^2/(a-2E) is EXACTLY the statement of P2: any derivation of it is a derivation of P2, not of anything independent")
ok_v = sp.simplify(Dp2 - E ** 2 / (a - 2 * E)) == 0
R.check("A1.2 M2 attempts (i)-(v): Born-Infeld has no deep regime, AQUAL power law has no wall, the walled family reproduces K1 only at its fitted point, dimensional analysis leaves F free, and D = g_N(E) of P2 is P2 itself",
        f"(i) linear limit {lim_small}; (iii) fitted (p, E_w) = ({p_fit:.4f}, {Ew_fit:.4f}); (v) P2 inverse = D: {ok_v}", fail_i and ok_iii and ok_v)
R.num("M2_attempts", dict(BI_linear_limit=str(lim_small), walled_fit=[p_fit, Ew_fit], P2_inverse_is_D=bool(ok_v)))
R.P("  verdict of A1.2: NO derivation of the constitutive function was found; K1 = M1 (declared), K2, K3 = M1, B-variants = M1/M0; nothing is graded M2.")

# ---------------------------------------------------------------------------------------------------- C9
R.banner("C9  the canonical-vector null: a Maxwell/Proca vector has no acceleration scale")
msym, r = sp.symbols("m r", positive=True)
Phi_pt = sp.exp(-msym * r) / r                                         # Yukawa potential of a point charge (units of q/4pi)
E_pt = sp.simplify(-sp.diff(Phi_pt, r))
ser = sp.series(sp.simplify(E_pt * r ** 2 - 1), msym, 0, 3).removeO()
R.P(f"  Yukawa E r^2 = {sp.simplify(E_pt * r ** 2)};  E r^2 - 1 = {ser} + ...  (leading correction -(m r)^2/2)")
rgal_kpc = 300.0                                                  # far outside a galaxy
m_over_c_kpc = (C.HL_SI / C.C_SI) * C.KPC_M                       # m = H_Lambda/c in 1/kpc
R.P(f"  m = H_Lambda/c = {m_over_c_kpc:.3e} /kpc; at 300 kpc (m r)^2/2 = {0.5 * (m_over_c_kpc * rgal_kpc) ** 2:.2e}")
cV = {}
for M_ in C.MASSES:
    cV[M_] = C.G1_cell("V0", "point", M_, C.a_V_si("HL"), "shape")["R_at"]
    v0 = C.variant("V0", C.PointMass(M_), np.geomspace(0.1, 30, 50) * C.r_M_kpc(M_, C.AKPC(C.a_V_si("HL"))), C.AKPC(C.a_V_si("HL")))
    ratio_E = v0["M_dark"] / (C.PointMass(M_).Mb(np.geomspace(0.1, 30, 50)))
    okc9 = np.max(np.abs(ratio_E - 1)) < 1e-9
r10 = 0.5 * (m_over_c_kpc * 10.0) ** 2
R.P(f"  (m r)^2/2 at 10 kpc = {r10:.2e}  (the frozen hand estimate said <~ 1e-12: WRONG by a factor {r10 / 1e-12:.1f}; kept, it changes nothing: the correction is inert)")
R.check("C9 V0: E is proportional to g_N (constant ratio to 1e-9 over the grid, so M_D = M_b and no a0 appears); the Yukawa correction (m r)^2/2 is < 1e-6 at 300 kpc",
        f"ratio E/g_N constant: {okc9}; correction {0.5 * (m_over_c_kpc * rgal_kpc) ** 2:.1e} at 300 kpc, {r10:.1e} at 10 kpc; point-mass R = 0 (rho_D = 0 away from the origin)",
        okc9 and 0.5 * (m_over_c_kpc * rgal_kpc) ** 2 < 1e-6 and all(v == [0.0] * 5 for v in cV.values()))
R.check("C9b (reported) the frozen hand estimate 'Yukawa effect at galactic r <~ 1e-12' holds", f"(m r)^2/2 at 10 kpc = {r10:.2e} > 1e-12", r10 <= 1e-12, load_bearing=False)

nf = R.write()
sys.exit(0 if nf == 0 else 1)
