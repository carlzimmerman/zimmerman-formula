#!/usr/bin/env python3
"""r03_exact_finite_ball.py -- the NEW step: Jacobson's equilibrium for a ball that is NOT small compared with the de Sitter radius L.

Setting: time-symmetric (K = 0) slice of dS_d = S^n(L), n = d-1; geodesic ball of geodesic radius chi_b = x L.  Hamiltonian constraint on the slice: R_slice = 16 pi G rho
(so G_00 = R/2 = 8 pi G rho).  Reference: pure de Sitter (rho = rho_Lambda).  Perturbation: energy density delta rho, first order.

 E1  exact A(x), V(x) of the ball (d = 4: A = 4 pi L^2 sin^2 x, V = 2 pi L^3 (x - sin(2x)/2)); the task text's V lacks a factor 2 (V(pi) must equal Vol S^3 = 2 pi^2 L^3);
     dA/dV = (n-1) cot(x)/L (mean curvature); small-ball limit reproduces eq (22) with G_00 = lambda
 E2  PROPOSITION (spherical symmetry, any n, any x in (0,pi)):   dA|_V = - 8 pi G * int xi delta_rho dV_0,   xi = L (cos(chi/L) - cos x)/sin x
     i.e. the fixed-volume area response equals the modular energy of the exact conformal Killing vector of the ball, with coefficient EXACTLY 8 pi, at every radius.
     Verified (a) by the linearised geometry with random regular perturbations s(chi) = L sin(chi/L) + eps p(chi), n = 2..7, x from 0.2 to 3.0 (30 digits),
     (b) by the fully non-linear geometry (finite eps, root-finding for the fixed volume).  CONTROLS: the flat-space weight (l^2-r^2)/(2l) and the missing fixed-V term FAIL at finite x.
 E3  uniform density: exact closed-FRW family S^3(L') gives  d A|_V / d(L^{-2}) = -3 I_4(x) EXACTLY (independent of the conformal-Killing weight); response function
     F_d(x) = exact / small-ball, series and values
 E4  non-spherical perturbations (conformal factor, n = 3): the identity holds for a generic axisymmetric first-order perturbation (linearity + rotation averaging)
 E5  x = pi/2 (static patch): fixed-V term vanishes, xi = L cos(theta) is the static Killing weight, first law (1/8 pi G) dA + dE_K = 0 (paper eq C1)
Exit 0 = all pass.
"""
import sys
import mpmath as mp
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")
def must_fail(name, cond):
    ok.append(not bool(cond)); print(f"  [{'OK' if not cond else 'FAIL'}] CONTROL (wrong claim must be rejected): {name}")

mp.mp.dps = 30
def Om(k):   # area of unit k-sphere in R^{k+1}
    return 2 * mp.pi ** (mp.mpf(k + 1) / 2) / mp.gamma(mp.mpf(k + 1) / 2)

# ------------------------------------------------------------------------------------------------ E1
print("E1  exact ball in dS: A(x), V(x)")
x_, L_ = sp.symbols('x L', positive=True)
th_ = sp.symbols('theta', positive=True)
A4 = 4 * sp.pi * L_**2 * sp.sin(x_)**2
V4 = 2 * sp.pi * L_**3 * (x_ - sp.sin(2 * x_) / 2)
check("V'(x) = A(x) L  (d = 4: d/dx of 2 pi L^3 (x - sin(2x)/2) = 4 pi L^3 sin^2 x)", sp.simplify(sp.diff(V4, x_) - L_ * A4) == 0)
check("V(pi) = 2 pi^2 L^3 = Vol(S^3)", sp.simplify(V4.subs(x_, sp.pi) - 2 * sp.pi**2 * L_**3) == 0)
Vtask = sp.pi * L_**3 * (x_ - sp.sin(2 * x_) / 2)    # the expression as written in the task text
must_fail("E1c the task-text expression pi L^3 (x - sin(2x)/2) for V (its V(pi) is pi^2 L^3, half the volume of S^3)",
          sp.simplify(Vtask.subs(x_, sp.pi) - 2 * sp.pi**2 * L_**3) == 0)
check("dA/dV|_L = 2 cot(x)/L  (mean curvature of the ball boundary; vanishes at the equator)",
      sp.simplify(sp.diff(A4, x_) / sp.diff(V4, x_) - 2 * sp.cos(x_) / (L_ * sp.sin(x_))) == 0)
# small-ball limit against eq (22): A_dS(V) / A_flat(V) - 1 = -l^2 lambda/(d^2-1) = -(d-2) l^2/(2(d+1) L^2),  lambda = (d-1)(d-2)/(2L^2)  => d=4: -l^2/(5 L^2), l = flat radius of the same volume
# (my first hand value had an extra factor 1/(d-2): -1/10; the script caught it, see the control E1d)
lf = sp.symbols('lf', positive=True)
xs = sp.symbols('xs', positive=True)
Vf = 4 * sp.pi * lf**3 / 3
# solve V4(x) = Vf for x as a series in lf/L :  x = y (1 + c y^2 + ...), y = lf/L
y = sp.symbols('y', positive=True)
c1, c2 = sp.symbols('c1 c2')
xser = y * (1 + c1 * y**2 + c2 * y**4)
eq = sp.series(sp.expand((V4.subs(L_, 1)).subs(x_, xser) - sp.Rational(4, 3) * sp.pi * y**3), y, 0, 8).removeO()
solc = sp.solve([sp.expand(eq).coeff(y, 5), sp.expand(eq).coeff(y, 7)], [c1, c2], dict=True)[0]
xs_ser = xser.subs(solc)
Aratio = sp.series(sp.sin(xs_ser)**2 / y**2 - 1, y, 0, 4).removeO()
check(f"A_dS(V)/A_flat(V) - 1 = {sp.simplify(Aratio)} = -(d-2)/(2(d+1)) (l_f/L)^2 = -(1/5) (l_f/L)^2: eq (22) leading term with G_00 = lambda = 3/L^2, d = 4", sp.simplify(Aratio + y**2 / 5) == 0)
must_fail("E1d the coefficient -1/10 (my first, wrong, hand value: an extra 1/(d-2))", sp.simplify(Aratio + y**2 / 10) == 0)

# ------------------------------------------------------------------------------------------------ E2
print("E2  PROPOSITION: exact first-order fixed-V area response = -8 pi G int xi delta_rho dV_0   (spherical symmetry)")
chi, eps = sp.symbols('chi eps')
def build(n, Lv, p):
    s0 = Lv * sp.sin(chi / Lv)
    s = s0 + eps * p
    R = -2 * (n - 1) * sp.diff(s, chi, 2) / s + (n - 1) * (n - 2) * (1 - sp.diff(s, chi)**2) / s**2
    dR = sp.diff(R, eps).subs(eps, 0)          # = 16 pi G delta_rho for eps-derivative
    return s0, s, R, dR
# sanity: the unperturbed slice has R = n(n-1)/L^2
for n in (2, 3, 5):
    s0, s, R, dR = build(n, sp.Symbol('L', positive=True), chi**3)
    check(f"n={n}: R[L sin(chi/L)] = n(n-1)/L^2", sp.simplify(R.subs(eps, 0) - sp.Integer(n * (n - 1)) / sp.Symbol('L', positive=True)**2) == 0)

profiles = {
    "p = chi^3":                     lambda Lv: chi**3,
    "p = chi^3 cos(2 chi) + chi^5":  lambda Lv: chi**3 * sp.cos(2 * chi) + chi**5,
    "p = L^3 sin^3(chi/L) (1+chi)":  lambda Lv: Lv**3 * sp.sin(chi / Lv)**3 * (1 + chi),
}
def lhs_rhs(n, Lv, pexpr, xb):
    """returns (LHS dA|_V, RHS -int xi (8 pi G delta_rho) dV_0)/Omega, mp floats"""
    Lm = sp.nsimplify(Lv)
    s0, s, R, dR = build(n, Lm, pexpr)
    f_p = sp.lambdify(chi, pexpr, 'mpmath')
    f_s0 = sp.lambdify(chi, s0, 'mpmath')
    f_dR = sp.lambdify(chi, dR, 'mpmath')
    chib = mp.mpf(xb) * mp.mpf(Lv)
    s0b = f_s0(chib)
    cotfac = (n - 1) * mp.cos(chib / Lv) / s0b            # dA0/dV0 per Omega cancels: (n-1) s0'/s0
    dV = (n - 1) * mp.quad(lambda c: f_s0(c)**(n - 2) * f_p(c), [0, chib], method='gauss-legendre')
    dA = (n - 1) * s0b**(n - 2) * f_p(chib)
    lhs = dA - cotfac * dV
    xi = lambda c: mp.mpf(Lv) * (mp.cos(c / Lv) - mp.cos(chib / Lv)) / mp.sin(chib / Lv)
    rhs = -mp.quad(lambda c: xi(c) * f_dR(c) / 2 * f_s0(c)**(n - 1), [0, chib], method='gauss-legendre')
    return lhs, rhs, xi, f_s0, f_dR, chib
maxrel = 0
count = 0
for n in (2, 3, 4, 5, 6, 7):
    for Lv in (1, sp.Rational(23, 10)):
        for pname, pf in profiles.items():
            for xb in (0.2, 0.9, 1.5707963267948966, 2.1, 2.9):
                lhs, rhs, *_ = lhs_rhs(n, Lv, pf(sp.nsimplify(Lv)), xb)
                rel = abs(lhs - rhs) / max(abs(lhs), abs(rhs), mp.mpf('1e-30'))
                maxrel = max(maxrel, float(rel)); count += 1
check(f"{count} cases (n=2..7, L in {{1, 2.3}}, 3 profiles, x = 0.2 ... 2.9): max |LHS-RHS|/|LHS| = {maxrel:.2e}", maxrel < 1e-20)
# CONTROLS on one representative case (n=3, L=1, x=2.1, profile 2)
n, Lv, xb = 3, 1, 2.1
pexpr = profiles["p = chi^3 cos(2 chi) + chi^5"](1)
lhs, rhs, xi, f_s0, f_dR, chib = lhs_rhs(n, Lv, pexpr, xb)
xi_flat = lambda c: (chib**2 - c**2) / (2 * chib)
rhs_flat = -mp.quad(lambda c: xi_flat(c) * f_dR(c) / 2 * f_s0(c)**(n - 1), [0, chib], method='gauss-legendre')
must_fail(f"E2b flat-space weight (l^2-r^2)/(2l) at x = {xb} (rel err {float(abs(lhs - rhs_flat) / abs(lhs)):.2e})", abs(lhs - rhs_flat) < 1e-10 * abs(lhs))
# missing fixed-V term
f_p = sp.lambdify(chi, pexpr, 'mpmath')
dA_only = (n - 1) * f_s0(chib)**(n - 2) * f_p(chib)
must_fail(f"E2c fixed-radius area change (no fixed-V correction) (rel err {float(abs(dA_only - rhs) / abs(rhs)):.2e})", abs(dA_only - rhs) < 1e-10 * abs(rhs))
# wrong overall coefficient: 4 pi instead of 8 pi
must_fail("E2d coefficient 4 pi G (rhs/2) instead of 8 pi G", abs(lhs - rhs / 2) < 1e-10 * abs(lhs))

print("  (b) fully non-linear check: finite eps, exact V(chi') = V_0(chi_b) by root finding, derivative by central difference")
mp.mp.dps = 60
def nonlinear_dAV(n, Lv, pexpr, xb, e=mp.mpf('1e-20')):
    f_p = sp.lambdify(chi, pexpr, 'mpmath'); Lm = mp.mpf(Lv)
    chib = mp.mpf(xb) * Lm
    s0f = lambda c: Lm * mp.sin(c / Lm)
    V0 = mp.quad(lambda c: s0f(c)**(n - 1), [0, chib], method='gauss-legendre')
    def AV(ev):
        sf = lambda c: s0f(c) + ev * f_p(c)
        Vf = lambda cb: mp.quad(lambda c: sf(c)**(n - 1), [0, cb], method='gauss-legendre')
        cb = mp.findroot(lambda cb: Vf(cb) - V0, chib)
        return sf(cb)**(n - 1)                      # per Omega
    return (AV(e) - AV(-e)) / (2 * e), AV(0)
for (n, xb) in ((3, 2.1), (4, 1.0), (5, 2.7)):
    pexpr = profiles["p = chi^3 cos(2 chi) + chi^5"](1)
    lhs_l, rhs_l, *_ = lhs_rhs(n, 1, pexpr, xb)
    nl, _ = nonlinear_dAV(n, 1, pexpr, xb)
    check(f"n={n}, x={xb}: non-linear dA_V/d eps = {mp.nstr(nl, 12)} vs RHS {mp.nstr(rhs_l, 12)} (rel {mp.nstr(abs(nl - rhs_l) / abs(rhs_l), 3)})",
          abs(nl - rhs_l) < mp.mpf('1e-12') * abs(rhs_l))
mp.mp.dps = 30

# ------------------------------------------------------------------------------------------------ E3
print("E3  uniform density: exact closed family S^3(L'), and the response function F_d(x)")
Ls, s_ = sp.symbols('L s', positive=True)
V0s = sp.symbols('V0', positive=True)
# fixed V:  V = 2 pi L^3 (x - sin x cos x) constant; A = 4 pi L^2 sin^2 x;  derivative wrt s = L^{-2}
xL = sp.Function('xL')
Vexpr = 2 * sp.pi * Ls**3 * (x_ - sp.sin(x_) * sp.cos(x_))
dxdL = -sp.diff(Vexpr, Ls) / sp.diff(Vexpr, x_)
dAdL = sp.diff(4 * sp.pi * Ls**2 * sp.sin(x_)**2, Ls) + sp.diff(4 * sp.pi * Ls**2 * sp.sin(x_)**2, x_) * dxdL
dAds = sp.simplify(dAdL * (-Ls**3 / 2))               # dL/ds = -L^3/2
I4 = 4 * sp.pi / sp.sin(x_) * (sp.sin(x_)**3 / 3 - sp.cos(x_) * (x_ / 2 - sp.sin(2 * x_) / 4))    # int xi dV_0 (L = 1)
check("EXACT: dA_V/d(L^-2) = -3 L^4 I_4(x) with I_4 = int xi dV_0 (uniform density; first-order 8 pi G delta_rho = 3 delta(L^-2)); LHS uses only S^3 closed forms",
      sp.simplify(dAds + 3 * Ls**4 * I4) == 0)
must_fail("E3b same with the flat weight: -3 L^4 (4 pi x^4/15)", sp.simplify(dAds.subs(Ls, 1) + 3 * 4 * sp.pi * x_**4 / 15) == 0)
# response function F_d(x) = int_0^x (cos th - cos x) sin^{d-2} th dth / sin x   /  (x^d/(d^2-1))
def Fd_numeric(dd, xv):
    xv = mp.mpf(xv)
    I = mp.quad(lambda t: (mp.cos(t) - mp.cos(xv)) * mp.sin(t)**(dd - 2), [0, xv]) / mp.sin(xv)
    return I / (xv**dd / (dd**2 - 1))
F4 = sp.simplify(I4 / (4 * sp.pi * x_**4 / 15))
ser = sp.series(F4, x_, 0, 8).removeO()
print("      F_4(x) = 1 +", sp.simplify(ser - 1), "+ ...")
c1_4 = ser.coeff(x_, 2); c2_4 = ser.coeff(x_, 4)
check("F_4(x) -> 1 as x -> 0 (small ball reproduces eq (7)/(8) exactly)", sp.limit(F4, x_, 0) == 1)
c1_num = (Fd_numeric(4, mp.mpf('0.02')) - 1) / mp.mpf('0.02')**2
check(f"F_4 series: coefficient of x^2 = {c1_4} = {float(c1_4):.6f} (independent numeric estimate from F_4(0.02): {mp.nstr(c1_num, 6)})",
      abs(float(c1_4) - float(c1_num)) < 1e-3 and c1_4 < 0)
for dd in (3, 4, 5, 6, 8):
    cl = Fd_numeric(dd, 1e-3)
    check(f"d={dd}: F_d(1e-3) = {mp.nstr(cl, 10)} -> 1", abs(cl - 1) < 1e-4)
must_fail("E3c F_4 is identically 1 (i.e. the small-ball formula is exact at all radii)", abs(Fd_numeric(4, 1.0) - 1) < 1e-3)
print("      F_4 at x = 0.5, 1, pi/2, 2, 2.5:", [mp.nstr(Fd_numeric(4, xv), 8) for xv in (0.5, 1.0, mp.pi / 2, 2.0, 2.5)])

# ------------------------------------------------------------------------------------------------ E4
print("E4  non-spherical first-order perturbation (n = 3, conformal factor psi = 1 + eps phi, phi generic axisymmetric)")
th, vt = sp.symbols('theta vartheta', positive=True)
X4 = sp.cos(th); X3 = sp.sin(th) * sp.cos(vt)
phi = sp.Rational(3, 10) * X4 + sp.Rational(1, 2) * X3 + sp.Rational(7, 10) * X3**2 + sp.Rational(2, 5) * X4 * X3 + sp.Rational(1, 5) * X3**3 + sp.Rational(1, 10) * X4**2
lap = (sp.diff(sp.sin(th)**2 * sp.diff(phi, th), th) / sp.sin(th)**2
       + sp.diff(sp.sin(vt) * sp.diff(phi, vt), vt) / (sp.sin(th)**2 * sp.sin(vt)))
# spherical consistency of the conformal Hamiltonian constraint with the s(chi) form used in E2 (phi = a(theta))
aeps = sp.symbols('aeps')
aph = th**2 * sp.cos(th) + th**4                     # smooth even function of theta
psi = 1 + aeps * aph
chi_of_th = sp.Function('c')
# proper radius chi(theta) = int psi^2 dtheta ; s = psi^2 sin(theta).  first order: chi = th + 2 aeps A1(th), A1 = int aph
A1 = sp.integrate(aph, th)
s_first = sp.sin(th) * (1 + 2 * aeps * aph)
# express p(chi): s(chi) = sin(chi - 2 aeps A1) (1 + 2 aeps aph) = sin(chi) + aeps [ -2 A1 cos(chi) + 2 aph sin(chi) ] + O(aeps^2)   (theta -> chi at zeroth order)
p_conf = (-2 * A1 * sp.cos(th) + 2 * aph * sp.sin(th)).subs(th, chi)
_, _, _, dR_s = build(3, 1, p_conf)
dR_conf = (-8 * sp.diff(sp.sin(th)**2 * sp.diff(aph, th), th) / sp.sin(th)**2 - 24 * aph).subs(th, chi)
diff_test = [sp.N((dR_s - dR_conf).subs(chi, cv), 15) for cv in (0.3, 1.1, 2.0)]
check(f"the conformal constraint dR = -8 lap(phi) - 24 phi agrees with the s(chi)-form of E2 for a spherical phi (diffs {[float(v) for v in diff_test]})",
      all(abs(float(v)) < 1e-9 for v in diff_test))
# numerics via numpy Gauss-Legendre
lap_f = sp.lambdify((th, vt), lap, 'numpy')
phi_f = sp.lambdify((th, vt), phi, 'numpy')
def e4(xb, nq=80):
    gl_x, gl_w = np.polynomial.legendre.leggauss(nq)
    def to(a, b): return 0.5 * (b - a) * (gl_x + 1) + a, 0.5 * (b - a) * gl_w
    tq, tw = to(0.0, xb)                       # theta in [0,x]
    cq, cw = to(-1.0, 1.0)                     # cos(vartheta)
    vq = np.arccos(cq)
    T, VV = np.meshgrid(tq, vq, indexing='ij')
    TW = np.outer(tw, cw)                      # d(cos vartheta) = sin(vartheta) dvartheta
    # phi integrated in theta at fixed direction:  Phi(x, vartheta) = int_0^x phi dtheta
    Phi = np.array([np.sum(tw * phi_f(tq, v)) for v in vq])
    phi_b = phi_f(xb, vq)
    dth_b = -2 * Phi                                           # eps^1 shift of the coordinate radius of the boundary
    # 2 pi from the azimuth; weights cw for cos(vartheta)
    dA = 2 * np.pi * np.sum(cw * (4 * phi_b * np.sin(xb)**2 + 2 * np.sin(xb) * np.cos(xb) * dth_b))
    inner = np.array([np.sum(tw * 6 * phi_f(tq, v) * np.sin(tq)**2) for v in vq])
    dV = 2 * np.pi * np.sum(cw * (inner + np.sin(xb)**2 * dth_b))
    lhs = dA - 2 * np.cos(xb) / np.sin(xb) * dV
    # RHS = - int xi (8 pi G delta rho) dV_0 with 8 pi G delta rho = -4 lap phi - 12 phi
    src = -4 * lap_f(T, VV) - 12 * phi_f(T, VV)
    xi = (np.cos(T) - np.cos(xb)) / np.sin(xb)
    rhs = -2 * np.pi * np.sum(TW * xi * src * np.sin(T)**2)
    xi_fl = (xb**2 - T**2) / (2 * xb)
    rhs_fl = -2 * np.pi * np.sum(TW * xi_fl * src * np.sin(T)**2)
    return lhs, rhs, rhs_fl
for xb in (0.6, 1.4, 2.3):
    lhs, rhs, _ = e4(xb)
    check(f"x = {xb}: non-spherical dA|_V = {lhs:.10f}, RHS = {rhs:.10f} (rel {abs(lhs - rhs) / abs(rhs):.1e})", abs(lhs - rhs) < 1e-8 * abs(rhs))
lhs, rhs, rhs_fl = e4(1.4)
must_fail(f"E4b flat-space weight (l^2-r^2)/(2l) at x = 1.4 (rel err {abs(lhs - rhs_fl) / abs(lhs):.2e})", abs(lhs - rhs_fl) < 1e-6 * abs(lhs))
lhs2, rhs2, rhs2_fl = e4(1.4, nq=120)
check("E4c quadrature-order stability (80 vs 120 nodes)", abs(lhs - lhs2) < 1e-10 * abs(lhs) and abs(rhs - rhs2) < 1e-10 * abs(rhs))

# ------------------------------------------------------------------------------------------------ E5
print("E5  the equator x = pi/2: the ball is the static patch, xi is the static Killing weight, no fixed-V term")
check("mean curvature term 2 cot(x)/L vanishes at x = pi/2, so dA|_V = dA (paper: 'first law of dS horizons', eq C1)", sp.simplify((2 * sp.cos(x_) / (L_ * sp.sin(x_))).subs(x_, sp.pi / 2)) == 0)
check("xi(theta) at x = pi/2 equals L cos(theta) = L sqrt(f) (static patch lapse times L: unit surface gravity)",
      sp.simplify(((L_ * (sp.cos(th_) - sp.cos(x_)) / sp.sin(x_)).subs(x_, sp.pi / 2)) - L_ * sp.cos(th_)) == 0)
check("modular temperature at the centre T_c = 1/(2 pi xi_c) = 1/(2 pi L tan(x/2)) equals T_dS = 1/(2 pi L) at x = pi/2",
      sp.simplify((1 / (2 * sp.pi * L_ * sp.tan(x_ / 2))).subs(x_, sp.pi / 2) - 1 / (2 * sp.pi * L_)) == 0)

# ------------------------------------------------------------------------------------------------ E6
print("E6  matter side: the conformal Killing vector of a cap of the Einstein static universe (dS is conformal to it), unit surface gravity, t = 0 weight")
tau, tt_, vv, pp, xc = sp.symbols('tau theta vartheta varphi x', positive=True)
Xe = [tau, tt_, vv, pp]
ge = sp.diag(-1, 1, sp.sin(tt_)**2, sp.sin(tt_)**2 * sp.sin(vv)**2)
zc = [(sp.cos(tau) * sp.cos(tt_) - sp.cos(xc)) / sp.sin(xc), -sp.sin(tau) * sp.sin(tt_) / sp.sin(xc), 0, 0]
Lze = sp.Matrix(4, 4, lambda a, b: sp.simplify(
    sum(zc[c] * sp.diff(ge[a, b], Xe[c]) for c in range(4)) + sum(ge[c, b] * sp.diff(zc[c], Xe[a]) for c in range(4)) + sum(ge[a, c] * sp.diff(zc[c], Xe[b]) for c in range(4))))
lam_conf = -2 * sp.sin(tau) * sp.cos(tt_) / sp.sin(xc)
check("zeta = [(cos t cos th - cos x) d_t - sin t sin th d_th]/sin x is a conformal Killing vector of R x S^3: L_zeta g = -(2 sin t cos th / sin x) g", sp.simplify(Lze - lam_conf * ge) == sp.zeros(4, 4))
check("zeta vanishes on the edge of the cap (t = 0, th = x)", sp.simplify(zc[0].subs({tau: 0, tt_: xc})) == 0 and sp.simplify(zc[1].subs({tau: 0, tt_: xc})) == 0)
zsq = sp.simplify(-zc[0]**2 + zc[1]**2)
check("zeta^2 = 0 on the future null boundary t = x - th of the diamond", sp.simplify(zsq.subs(tau, xc - tt_)) == 0)
zl = [sp.simplify(sum(ge[a, b] * zc[b] for b in range(4))) for a in range(4)]
kap = [sp.simplify((-sp.diff(zsq, Xe[a]) / (2 * zl[a])).subs(tau, xc - tt_)) for a in range(2)]
kap = [sp.simplify(k) for k in kap]
check(f"surface gravity from d_a zeta^2 = -2 kappa zeta_a on that boundary: components give {kap}", kap[0] == 1 and kap[1] == 1)
check("restriction to t = 0: zeta^t = (cos th - cos x)/sin x (times the dS scale factor L at t = 0, the conformal factor of dS -> ESU): the weight used in E2-E4",
      sp.simplify(zc[0].subs(tau, 0) - (sp.cos(tt_) - sp.cos(xc)) / sp.sin(xc)) == 0)
check("small-x limit of the weight: L (cos th - cos x)/sin x -> (l^2 - r^2)/(2 l) (the flat-space weight of eq (10)): checked as the series in x at fixed th/x = q",
      sp.simplify(sp.limit(((sp.cos(xc * sp.Symbol('q')) - sp.cos(xc)) / sp.sin(xc)) / (xc * (1 - sp.Symbol('q')**2) / 2), xc, 0)) == 1)
print("   (NOT re-derived here: that the CFT modular Hamiltonian of a cap in the dS vacuum is 2 pi times the conformal-Killing charge of this vector; it is the conformal image of the flat")
print("    Hislop-Longo/Bisognano-Wichmann statement the paper uses, taken as an assumption, as is the state-independent UV term eta A)")

print(f"\nr03: {sum(ok)}/{len(ok)} checks passed")
sys.exit(0 if all(ok) else 1)
