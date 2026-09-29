#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG179 S1 -- Q-merge, symbolic (FROZEN_QUESTION.md M1-M4).  sympy only; under a minute.

M1  GR's river (Painleve-Gullstrand-de Sitter): the Einstein tensor of ds^2 = -dt^2 + (dr + v dt)^2 + r^2 dOmega^2 depends on
    f = v^2 only; the Einstein-Lambda vacuum is a LINEAR ODE in f, so v^2 adds (2M/r + Lambda r^2/3) and a linear velocity
    sum fails (its cross term pulls as r^-1/2).
M2  the Newtonian river law from L = |xdot - v|^2/2:  xddot = d_t v + (v.grad)v - w x (curl v),  w = xdot - v;  two point
    masses: the linear sum of the two infalls pulls with a spurious cross term grad(v1.v2) -- potentials (v^2) add, velocities
    do not; GR's own 1PN merge term is O(U/c^2).
M3  the no-go: a merged local law with NO external-field effect must be additive, F(z + z_e) - F(z_e) = F(z) for all z, z_e,
    hence F' constant (Newton).  P2 (deep limit F ~ sqrt z) violates it: merged rivers must interact.
M4  the external-field law this implies for P2: aligned 1-D AQUAL == QUMOND (Chae's eq. 6 construction), susceptibility -1;
    the equation book's E7 cubic re-derived, susceptibility -1/(2(1+b)) per unit sqrt2 g_ext/a0; the external-dominated
    limits.

MUTATE=1: the kernel is made linear (nu == 2): M3's 'merged rivers interact' check must fail (rc 1).
"""
import math
import sympy as sp
from cfg179_common import Run, MUTATE, C_SI

R = Run("cfg179_s1_merge_symbolic")


def is_zero(expr, syms):
    """exact zero test that survives sympy's reluctance with nested radicals: simplify; else square-root denesting with
    positive symbols (sqrt(u^2) -> u); else 40-digit evaluation at 6 fixed positive points (all |value| < 1e-30).
    Returns (bool, method).  (First run: plain simplify failed on sqrt((z+1)^2)-type radicals -- see *_firstrun.out.)"""
    if sp.simplify(expr) == 0:
        return True, "simplify"
    e2 = sp.simplify(sp.powdenest(sp.factor(sp.expand(expr)), force=True))
    e2 = sp.simplify(e2.replace(lambda q: q.is_Pow and q.exp == sp.Rational(1, 2),
                                lambda q: sp.sqrt(sp.factor(q.base))))
    if sp.simplify(sp.powdenest(e2, force=True)) == 0:
        return True, "factor+denest"
    vals = [sp.Rational(3, 17), sp.Rational(1, 3), sp.Rational(7, 5), sp.Rational(5, 2), sp.Rational(1, 50), 11]
    ok = True
    for k in range(6):
        sub = {s_: vals[(k + j) % 6] for j, s_ in enumerate(syms)}
        ok &= abs(sp.N(expr.subs(sub), 40)) < sp.Float("1e-30", 40)
    return ok, "40-digit numeric at 6 points"

# =============================================================================================== M1 PG-de Sitter
R.banner("M1  GR's river: Painleve-Gullstrand with a general flow speed v(r)  (c = 1, signature -+++)")
t, r, th, ph = sp.symbols("t r theta phi", positive=True)
M, Lam = sp.symbols("M Lambda", positive=True)
v = sp.Function("v")(r)
X = [t, r, th, ph]
g = sp.Matrix([[-(1 - v**2), v, 0, 0],
               [v, 1, 0, 0],
               [0, 0, r**2, 0],
               [0, 0, 0, r**2 * sp.sin(th)**2]])
ginv = sp.simplify(g.inv())
Gam = [[[sp.simplify(sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                         for d in range(4)) / 2) for c in range(4)] for b in range(4)] for a in range(4)]


def ricci(b, c):
    expr = 0
    for a in range(4):
        expr += sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
        for d in range(4):
            expr += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
    return sp.simplify(expr)


Ric = sp.Matrix(4, 4, lambda b, c: ricci(b, c))
Rs = sp.simplify(sum(ginv[b, c] * Ric[b, c] for b in range(4) for c in range(4)))
Gdn = sp.simplify(Ric - g * Rs / 2)
Gmix = sp.simplify(ginv * Gdn)                                    # G^a_c
f = v**2
Gtt_claim = -sp.diff(r * f, r) / r**2
Gthth_claim = -sp.diff(r * f, r, 2) / (2 * r)
ok_tt = sp.simplify(Gmix[0, 0] - Gtt_claim) == 0 and sp.simplify(Gmix[1, 1] - Gtt_claim) == 0
ok_thth = sp.simplify(Gmix[2, 2] - Gthth_claim) == 0 and sp.simplify(Gmix[3, 3] - Gthth_claim) == 0
offd = [sp.simplify(Gmix[a, c]) for a in range(4) for c in range(4) if a != c]
ok_off = all(o == 0 for o in offd)
R.check("M1a G^t_t = G^r_r = -(r f)'/r^2 and G^th_th = G^ph_ph = -(r f)''/(2r) with f = v^2; all off-diagonal G^a_c = 0 "
        "(the geometry depends on the flow only through v^2)", ok_tt and ok_thth and ok_off,
        f"G^t_t - claim = {sp.simplify(Gmix[0, 0] - Gtt_claim)}; G^th_th - claim = {sp.simplify(Gmix[2, 2] - Gthth_claim)}; "
        f"off-diagonal zero: {ok_off}")

fS = sp.Function("f")(r)
sol = sp.dsolve(sp.Eq(-sp.diff(r * fS, r) / r**2, -Lam), fS)
f_sds = 2 * M / r + Lam * r**2 / 3
C1 = sp.Symbol("C1")
ok_sol = sp.simplify(sol.rhs.subs(C1, 2 * M) - f_sds) == 0
res_tt = sp.simplify((-sp.diff(r * f_sds, r) / r**2) + Lam)
res_th = sp.simplify((-sp.diff(r * f_sds, r, 2) / (2 * r)) + Lam)
R.check("M1b the Einstein-Lambda vacuum G^a_c = -Lambda delta^a_c is LINEAR in f = v^2: general solution f = C1/r + Lambda r^2/3, "
        "i.e. v^2 = 2M/r + Lambda r^2/3 -- the squared flows ADD, no cross term", ok_sol and res_tt == 0 and res_th == 0,
        f"dsolve: f = {sol.rhs}; residuals of 2M/r + Lambda r^2/3: tt {res_tt}, thth {res_th}")

v_lin = sp.sqrt(2 * M / r) + sp.sqrt(Lam / 3) * r
f_lin = sp.expand(v_lin**2)
f_x = sp.simplify(f_lin - f_sds)
res_lin = sp.simplify(-sp.diff(r * f_lin, r) / r**2 + Lam)
a_x = sp.simplify(-sp.diff(f_x / 2, r))
slope = sp.simplify(r * sp.diff(sp.log(-a_x), r))
R.check("M1c a LINEAR velocity sum v = sqrt(2M/r) + sqrt(Lambda/3) r is NOT a solution: cross term f_x = 2 sqrt(2 M Lambda/3) r^(1/2), "
        "residual != 0, and the cross term's pull -d(f_x/2)/dr scales as r^(-1/2) (rotation speed ~ r^(1/4)), not deep-MOND r^(-1)",
        res_lin != 0 and slope == sp.Rational(-1, 2),
        f"f_x = {f_x}; G^t_t + Lambda = {res_lin}; cross-term acceleration = {a_x}; d ln|a|/d ln r = {slope}")
R.num("M1", dict(f_cross=str(f_x), residual=str(res_lin), a_cross=str(a_x), slope=str(slope)))

# =============================================================================================== M2 river law, two masses
R.banner("M2  the Newtonian river law, and two rivers added as velocities")
tt = sp.Symbol("t")
xs = [sp.Function(n)(tt) for n in ("x", "y", "z")]
vf = [sp.Function(n) for n in ("v1", "v2", "v3")]
vv = [vf[i](*xs, tt) for i in range(3)]
xd = [sp.diff(q, tt) for q in xs]
Lag = sum((xd[i] - vv[i])**2 for i in range(3)) / 2
EL = [sp.diff(sp.diff(Lag, xd[i]), tt) - sp.diff(Lag, xs[i]) for i in range(3)]
xdd = [sp.diff(q, tt, 2) for q in xs]
solx = sp.solve(EL, xdd, dict=True)[0]
# the claimed law: xddot = d_t v + (v.grad) v - w x curl v, with w = xdot - v
a1, a2, a3, a4 = sp.symbols("a1 a2 a3 a4")
Vs = [vf[i](a1, a2, a3, a4) for i in range(3)]
AA = [a1, a2, a3]
dV = lambda i, j: sp.diff(Vs[i], AA[j])                           # d v_i / d x_j
curl = [dV(2, 1) - dV(1, 2), dV(0, 2) - dV(2, 0), dV(1, 0) - dV(0, 1)]
w = [sp.Symbol(f"w{i}") for i in range(3)]
claim = []
for i in range(3):
    conv = sp.diff(Vs[i], a4) + sum(Vs[j] * dV(i, j) for j in range(3))
    wxc = [w[1] * curl[2] - w[2] * curl[1], w[2] * curl[0] - w[0] * curl[2], w[0] * curl[1] - w[1] * curl[0]]
    claim.append(conv - wxc[i])
subs_pt = {a1: xs[0], a2: xs[1], a3: xs[2], a4: tt}
ok_law = True
for i in range(3):
    cl = claim[i].subs({w[k]: xd[k] - vv[k] for k in range(3)})
    cl = cl.subs(subs_pt).doit()
    diff_ = sp.simplify(sp.expand(solx[xdd[i]] - cl))
    ok_law &= (diff_ == 0)
R.check("M2a Newtonian limit of the river metric ds^2 = -dt^2 + |dx - v dt|^2, L = |xdot - v|^2/2, gives exactly "
        "xddot = d_t v + (v.grad) v - w x (curl v), w = xdot - v (a body carried by the flow, plus a Coriolis-like term "
        "from the flow's vorticity)", ok_law, "Euler-Lagrange solved for xddot and compared component by component")

# two infalls: v_k = -sqrt(2 G M_k / r_k) rhat_k, GM = 1, d = 1
px, py, pz = sp.symbols("p_x p_y p_z", real=True)
P_ = sp.Matrix([px, py, pz])
cen = [sp.Matrix([sp.Rational(-1, 2), 0, 0]), sp.Matrix([sp.Rational(1, 2), 0, 0])]


def infall(c):
    dvec = P_ - c
    rr = sp.sqrt(dvec.dot(dvec))
    return -sp.sqrt(2 / rr) * dvec / rr, -1 / rr                 # (velocity, Newtonian potential)


(v1, Phi1), (v2, Phi2) = infall(cen[0]), infall(cen[1])
vsum = v1 + v2
PP = [px, py, pz]
jac = vsum.jacobian(PP)
curl_s = sp.Matrix([jac[2, 1] - jac[1, 2], jac[0, 2] - jac[2, 0], jac[1, 0] - jac[0, 1]])
a_lin = jac * vsum                                                 # (v.grad) v, steady
a_N = -sp.Matrix([sp.diff(Phi1 + Phi2, q) for q in PP])
cross = sp.Matrix([sp.diff(v1.dot(v2), q) for q in PP])
pt = {px: sp.Rational(3, 10), py: sp.Rational(2, 5), pz: 0}
curl_num = [float(c.subs(pt)) for c in curl_s]
aL = [float(c.subs(pt)) for c in a_lin]
aN = [float(c.subs(pt)) for c in a_N]
cr = [float(c.subs(pt)) for c in cross]
ident = max(abs(aL[i] - aN[i] - cr[i]) for i in range(3))
ratio = math.sqrt(sum(c * c for c in cr)) / math.sqrt(sum(c * c for c in aN))
R.check("M2b two point masses (GM = 1 each at x = -+1/2), field point (0.3, 0.4, 0): the summed infall v1 + v2 is irrotational, "
        "its pull (v.grad)v equals Newton + grad(v1.v2) exactly, and the cross term grad(v1.v2) is not small "
        "(pass line |cross|/|a_N| > 0.01)", max(abs(c) for c in curl_num) < 1e-12 and ident < 1e-12 and ratio > 0.01,
        f"|curl| = {max(abs(c) for c in curl_num):.1e}; a_lin = ({aL[0]:+.4f}, {aL[1]:+.4f}), a_N = ({aN[0]:+.4f}, {aN[1]:+.4f}); "
        f"identity residual {ident:.1e}; |grad(v1.v2)|/|a_N| = {ratio:.3f}")
R.P("    reading: in the weak field it is v^2 = -2 Phi that adds (the potentials add); the merged river is the solution of the "
    "eikonal |grad chi|^2 = v1^2 + v2^2, not v1 + v2.  No exact GR two-body river is known to this lane.")
R.num("M2", dict(cross_over_aN=ratio, a_lin=aL, a_N=aN))

Vsun = 220e3
R.check("M2c GR's own merge nonlinearity (1PN, beta = 1): g_00 carries -2 beta U^2/c^4 = -2(U1 + U2)^2/c^4, a cross term "
        "-4 U1 U2/c^4, i.e. relative size U_ext/c^2; for the Milky Way at the Sun V_c^2/c^2 (a floor on |Phi|/c^2)",
        (Vsun / C_SI)**2 < 1e-5, f"V_c^2/c^2 = {(Vsun / C_SI)**2:.2e} (|Phi|/c^2 is a few times this); GR obeys the strong "
        "equivalence principle, so beyond tides its merged rivers carry no external-field effect", load_bearing=False)

# =============================================================================================== M3 the no-go
R.banner("M3  THE NO-GO: a local merged law with no external-field effect must be linear")
z, ze, s_ = sp.symbols("z z_e s", positive=True)
Ff = sp.Function("F")
I_ = Ff(z + ze) - Ff(ze) - Ff(z)
dI = sp.diff(I_, ze)
R.check("M3a d/dz_e of the no-EFE identity F(z + z_e) - F(z_e) - F(z) = 0 is F'(z + z_e) - F'(z_e) = 0 for all z, z_e: "
        "F' takes one value on (0, inf), so F(z) = k z (Newton with G -> kG); any nonlinear F makes merged rivers interact",
        sp.simplify(dI - (sp.Subs(sp.Derivative(Ff(s_), s_), s_, z + ze).doit() - sp.Subs(sp.Derivative(Ff(s_), s_), s_, ze).doit())) == 0,
        f"d/dz_e I = {dI}")
F_P2 = (lambda q: 2 * q) if MUTATE else (lambda q: sp.sqrt(q**2 + q))
kern = "LINEAR nu == 2 (MUTATE)" if MUTATE else "P2 F(z) = sqrt(z^2 + z)"
pts = [(sp.Rational(1, 100), sp.Rational(1, 10)), (sp.Rational(1, 100), 1), (sp.Rational(1, 10), sp.Rational(1, 10)),
       (sp.Rational(1, 10), 1), (1, sp.Rational(1, 10)), (1, 1)]
resid = [float(F_P2(sp.Integer(0) + a + b) - F_P2(b) - F_P2(a)) for a, b in pts]
Fz = F_P2(z)
dF = sp.simplify(sp.diff(Fz, z))
lim0 = sp.limit(dF, z, 0, "+")
R.check(f"M3b [HEADLINE] merged P2 rivers interact: the no-EFE residual F(z + z_e) - F(z_e) - F(z) is nonzero at all 6 declared "
        f"points, F' is not constant, and F'(0+) is infinite (kernel: {kern})",
        all(abs(x) > 1e-6 for x in resid) and lim0 == sp.oo,
        "residuals " + ", ".join(f"({float(a):g},{float(b):g}): {x:+.4f}" for (a, b), x in zip(pts, resid))
        + f"; F'(z) = {dF}; F'(0+) = {lim0}")
lam = sp.Symbol("lambda", positive=True)
hom = sp.simplify(sp.sqrt(lam * z) / sp.sqrt(z))
R.check("M3c deep-MOND homogeneity: F_deep(lambda z) = lambda^(1/2) F_deep(z); two equal sources at one place give sqrt2, "
        "not 2, times one source's field -- the flow law is nonlinear in the source", hom == sp.sqrt(lam),
        f"F_deep(lambda z)/F_deep(z) = {hom}; at lambda = 2: {float(hom.subs(lam, 2)):.4f} vs linear 2")
R.num("M3", dict(residuals=resid, dF=str(dF), dF0=str(lim0), kernel=kern))

# =============================================================================================== M4 the implied EFE
R.banner("M4  the external-field law merged P2 rivers imply")
b, e, Xx, x = sp.symbols("b e X x", positive=True)
Fs = lambda q: sp.sqrt(q**2 + q)
Ms = lambda q: (sp.sqrt(1 + 4 * q**2) - 1) / 2
inv1, m1 = is_zero(Fs(Ms(Xx)) - Xx, [Xx])
inv2, m2 = is_zero(Ms(Fs(Xx)) - Xx, [Xx])
ok_inv = inv1 and inv2
x_aqual = Fs(b + Ms(e)) - e                                       # AQUAL-1D solved: M(x+e) - M(e) = b  =>  x + e = F(b + M(e))
aq0, m3 = is_zero(Ms(x_aqual + e) - Ms(e) - b, [b, e])
chi1d = sp.simplify(sp.limit(sp.diff(x_aqual, e), e, 0, "+"))
R.check("M4a aligned 1-D AQUAL [M(x+e) - M(e) = b] and QUMOND [x = F(b + z_e) - e, e = F(z_e)] are one law for P2 "
        "(F and M exact inverses) -- Chae 2020's eq. 6 construction, the one CFG8 fitted; its susceptibility dx/de at e = 0 is -1 "
        "for every b", ok_inv and aq0 and chi1d == -1,
        f"F(M(X)) = X: {inv1} ({m1}); M(F(X)) = X: {inv2} ({m2}); AQUAL residual zero: {aq0} ({m3}); dx/de|0 = {chi1d}")

E = sp.Symbol("E", nonnegative=True)
cubic = x**3 + E * x**2 - b * (b + 1) * x - b**2 * E
lhs = sp.expand((x * sp.sqrt(1 + 4 * (x + E)**2))**2 - (2 * b * (x + E) + x)**2)
fac = sp.simplify(lhs - 4 * (x + E) * cubic)
balance_ok = True
for bv, ev in [(0.1, 0.3), (3.0, 0.5), (0.02, 2.0), (10.0, 10.0)]:
    roots = sp.Poly(cubic.subs({b: bv, E: ev}), x).nroots()
    pos = [complex(q).real for q in roots if abs(complex(q).imag) < 1e-12 and complex(q).real > 0]
    xv = pos[0]
    mu = (math.sqrt(1 + 4 * (xv + ev)**2) - 1) / (2 * (xv + ev))
    balance_ok &= (len(pos) == 1 and abs(mu * xv - bv) < 1e-10)
xp = sp.Symbol("xp")
dx_de = sp.solve(sp.Eq(sp.diff(cubic, x) * xp + sp.diff(cubic, E), 0), xp)[0]
chi7 = sp.simplify(dx_de.subs({E: 0}).subs(x, sp.sqrt(b**2 + b)))
R.check("M4b E7 re-derived (independently of eqbook_S5_efe.py): clearing the radical of mu_fw(x + e7) x = b gives "
        "4(x + e7)[x^3 + e7 x^2 - b(b+1)x - b^2 e7]; its unique positive root satisfies the unsquared balance (4 points); "
        "susceptibility -1/(2(1+b)) per unit e7 = sqrt2 g_ext/a0, i.e. -1/(sqrt2 (1+b)) per unit g_ext/a0 "
        "(deep limit 0.707 of the 1-D law's -1)", fac == 0 and balance_ok and sp.simplify(chi7 + 1 / (2 * (1 + b))) == 0,
        f"factorisation residual {fac}; balance on 4 points {balance_ok}; chi_E7 = {chi7}")

c1 = sp.Symbol("c1")
ser = sp.Poly(sp.expand(cubic.subs(x, c1 * b)), b)
sol_c1 = [q for q in sp.solve(ser.coeff_monomial(b**2), c1) if q.subs(E, 1) > 0][0]
geff7 = sp.simplify(sol_c1 - (1 + sp.sqrt(1 + 4 * E**2)) / (2 * E))
zz = sp.Symbol("zeta", positive=True)
nu_ = sp.sqrt(1 + 1 / zz)
Lz = sp.simplify(zz * sp.diff(nu_, zz) / nu_)
par0, m4 = is_zero(sp.diff(Fs(zz), zz) - nu_ * (1 + Lz), [zz])
iso = sp.simplify((nu_ * (1 + Lz) + 2 * nu_) / 3 - nu_ * (1 + Lz / 3))
R.check("M4c external-dominated limits: E7 G_eff/G = 1/mu_fw(e7) = (1 + sqrt(1 + 4 e7^2))/(2 e7); P2 1-D (parallel) "
        "F'(z_e) = nu(1 + L) with L = -1/(2(1+z_e)); the isotropic average of (parallel, perp, perp) = (nu(1+L), nu, nu) is "
        "nu(1 + L/3) (L23's E3 coupling)",
        geff7 == 0 and par0 and iso == 0 and sp.simplify(Lz + 1 / (2 * (1 + zz))) == 0,
        f"E7 residual {geff7}; F' - nu(1+L) zero: {par0} ({m4}); L = {Lz}; isotropic residual {iso}")

R.banner("VERDICT (M1-M4)")
R.P("  GR's rivers add in v^2 (potentials add), never in v; GR's merge carries no external-field effect beyond tides (SEP).")
R.P("  Any flow law with the deep-MOND limit is nonlinear in its source, so a river inside a larger river obeys a modified")
R.P("  internal law (M3): merged rivers MUST interact unless the boost is keyed to something other than the local total flow")
R.P("  (e.g. candidate B's ownership of the enclosed baryons -- a nonlocal rule, not a merging flow).  For P2 the implied")
R.P("  quench is the aligned 1-D law (susceptibility -1) or the equation book's E7 (-1/(sqrt2 (1+b)) per unit g_ext/a0).")
R.finish()
