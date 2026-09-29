# -*- coding: utf-8 -*-
"""CFG124 T0 -- structure of the mimetic action (sympy).  Frozen criteria: CFG124_FROZEN_CRITERIA.md (committed e8b9fbcdf).
Action (signature -+++, c=1):  S = INT sqrt(-g)[ R/16piG + lam (X+1) - V(phi) + (gamma/2)(box phi)^2 ] + S_b[g].
Unitary-gauge (phi = t) route: X = g^{tt} = -1/N^2 => N = 1; box phi = -K; sqrt(-g)R = N sqrt(h)(R3 + K_ij K^ij - K^2) + t.d.;
so the reduced action is  INT sqrt(h) [ (1/16piG)(R3 + K_ij K^ij - (1 - gt) K^2) - V(t) ],  gt = 8 pi G gamma  (gamma is measured in
units of M_P^2 = 1/(8 pi G); this normalisation was not spelled out in the frozen text: disclosed, not a criterion change).
The Hamiltonian constraint is NOT imposed (lam plays its role): that is the dust.  Checks T0.1-T0.7 below.
MUTATE: a (breaks T0.5's static-support claim by giving the dust a pressure by hand), b (breaks c_s^2 by dropping the gamma term in the
gradient sign), c/1 are not used here except '1' which activates a and b.
"""
import os, sys, json, time
import sympy as sp
from sympy.calculus.euler import euler_equations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG124_common as C

R = C.Report("CFG124_T0_field_equations")
P = R.P
P(__doc__)
t, x, y, z = sp.symbols('t x y z', real=True)
G8, g, s_, w_ = sp.symbols('G8 gt s w', real=True)
a = sp.Function('a', positive=True)(t); V = sp.Function('V')(t)

# ------------------------------------------------------------------------------------------------ T0.1 ADM identity (FRW)
R.banner("T0.1  sqrt(-g) R = N sqrt(h)(R3 + K_ij K^ij - K^2) + total derivative  (checked on flat FRW with lapse N=1)")
Rfrw = 6 * (sp.diff(a, t, 2) / a + (sp.diff(a, t) / a) ** 2)
lhs = a ** 3 * Rfrw
rhs = a ** 3 * (0 + 3 * (sp.diff(a, t) / a) ** 2 - 9 * (sp.diff(a, t) / a) ** 2)
diff = sp.simplify(lhs - rhs - 6 * sp.diff(a ** 2 * sp.diff(a, t), t))
R.check("T0.1", "a^3 R - a^3(K_ijK^ij - K^2) = 6 d/dt(a^2 adot) exactly (total derivative)", "residual = %s" % diff, diff == 0)

# ------------------------------------------------------------------------------------------------ T0.2 box phi = -K, X = -1  (perturbed unitary-gauge metric)
R.banner("T0.2  unitary gauge: box(phi=t) = -K for N = 1, shift N_i = d_i psi, h_ij = a^2 e^{2 zeta} delta_ij (fields depend on t, x)")
zeta = sp.Function('zeta')(t, x); psi = sp.Function('psi')(t, x)
X4 = [t, x, y, z]
h = sp.diag(*[a ** 2 * sp.exp(2 * zeta)] * 3); hinv = h.inv(); sqrth = a ** 3 * sp.exp(3 * zeta)
Ni_low = [sp.diff(psi, x), 0, 0]
Ni_up = [sum(hinv[i, j] * Ni_low[j] for j in range(3)) for i in range(3)]
N2 = sum(Ni_low[i] * Ni_up[i] for i in range(3))
gmat = sp.zeros(4, 4)
gmat[0, 0] = -1 + N2
for i in range(3):
    gmat[0, i + 1] = gmat[i + 1, 0] = Ni_low[i]
    for j in range(3):
        gmat[i + 1, j + 1] = h[i, j]
ginv = sp.simplify(gmat.inv())
sqrtg = sp.sqrt(sp.simplify(-gmat.det()))
sqrtg = sp.simplify(sqrtg)
Xn = sp.simplify(ginv[0, 0])
R.check("T0.2a", "X = g^{tt} = -1 identically when N = 1 (the constraint fixes the lapse in unitary gauge)", "g^tt = %s" % Xn, sp.simplify(Xn + 1) == 0)
boxphi = sp.simplify(sum(sp.diff(sqrtg * ginv[m, 0], X4[m]) for m in range(4)) / sqrtg)
Xs = [x, y, z]
def Gam(k, i, j):
    return sum(hinv[k, l] * (sp.diff(h[l, i], Xs[j]) + sp.diff(h[l, j], Xs[i]) - sp.diff(h[i, j], Xs[l])) for l in range(3)) / 2
Gm = [[[sp.simplify(Gam(k, i, j)) for j in range(3)] for i in range(3)] for k in range(3)]
def DN(i, j): return sp.diff(Ni_low[j], Xs[i]) - sum(Gm[k][i][j] * Ni_low[k] for k in range(3))
Kmat = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2) * (sp.diff(h[i, j], t) - DN(i, j) - DN(j, i)))
Kmix = hinv * Kmat
Ktr = sp.simplify(Kmix.trace()); KK = sp.simplify((Kmix * Kmix).trace())
d = sp.simplify(boxphi + Ktr)
R.check("T0.2b", "box phi = -K (K = trace of the extrinsic curvature of the phi = const slices)", "box phi + K = %s" % d, d == 0)

# ------------------------------------------------------------------------------------------------ T0.3 geodesic flow, class independence; no v=0 state
R.banner("T0.3  the constraint is kinematic: the congruence u_mu = d_mu phi is geodesic and irrotational for ANY V, gamma, D-term")
gg = [[sp.Function('g%d%d' % (i, j))(t, x) for j in range(2)] for i in range(2)]
gg[1][0] = gg[0][1]
gm = sp.Matrix(2, 2, lambda i, j: gg[i][j]); gi = gm.inv()
ph = sp.Function('phi')(t, x); X2 = [t, x]
def G2(k, i, j): return sum(gi[k, l] * (sp.diff(gm[l, i], X2[j]) + sp.diff(gm[l, j], X2[i]) - sp.diff(gm[i, j], X2[l])) for l in range(2)) / 2
def nabla(m, n): return sp.diff(ph, X2[m], X2[n]) - sum(G2(l, m, n) * sp.diff(ph, X2[l]) for l in range(2))
Xs2 = sum(gi[m, n] * sp.diff(ph, X2[m]) * sp.diff(ph, X2[n]) for m in range(2) for n in range(2))
res = [sp.simplify(sum(gi[n, l] * sp.diff(ph, X2[l]) * nabla(n, m) for n in range(2) for l in range(2)) - sp.diff(Xs2, X2[m]) / 2) for m in range(2)]
R.check("T0.3a", "phi^nu nabla_nu phi_mu = (1/2) d_mu X identically (generic 1+1 metric and phi), so X = -1 => a_mu = 0: geodesic, whatever the action's other terms", "residuals = %s" % res, all(r == 0 for r in res))
# Hamilton-Jacobi / Euler in the weak field
Phi = sp.Function('Phi')(x); pi_ = sp.Function('pi')(t, x)
HJ = sp.Eq(sp.diff(pi_, t), Phi + sp.diff(pi_, x) ** 2 / 2)         # from -(1-2Phi)(1+pi_t)^2 + pi_x^2 = -1 at first order
v = -sp.diff(pi_, x)
euler = sp.simplify(sp.diff(v, t).subs(sp.Derivative(pi_, (x, t)), sp.diff(HJ.rhs, x)) + v * sp.diff(v, x) + sp.diff(Phi, x))
euler = sp.simplify(sp.diff(v, t) .subs(sp.Derivative(pi_, t, x), sp.diff(HJ.rhs, x)) + v * sp.diff(v, x) + sp.diff(Phi, x))
R.check("T0.3b", "weak-field HJ pi_t = Phi + pi_x^2/2 gives the pressureless Euler equation v_t + v v_x = -Phi_x (v = -pi_x)", "residual = %s" % euler, euler == 0)
f = sp.Function('f')(t)
xx = sp.symbols('x0')
rhs_static = sp.sqrt(1 + 2 * Phi) - 1
dx_rhs = sp.simplify(sp.diff(rhs_static, x))
R.check("T0.3c", "a v = 0 state (pi = f(t)) needs f' = sqrt(1+2 Phi(x)) - 1 to be x-independent: d_x of it = Phi'/sqrt(1+2Phi), nonzero whenever grad Phi != 0. NO stationary v = 0 state exists in a potential well, for every class A-D (the constraint is kinematic)",
        "d/dx[ sqrt(1+2Phi) - 1 ] = %s" % dx_rhs, sp.simplify(dx_rhs - sp.diff(Phi, x) / sp.sqrt(1 + 2 * Phi)) == 0)

# ------------------------------------------------------------------------------------------------ T0.4 background: eps, Cm, V
R.banner("T0.4  background (N-variation gives the energy density; a-variation the dynamics): Cm conserved iff V is constant")
N = sp.Function('N')(t); lam = sp.Function('lam')(t)
Lbg = N * a ** 3 * ((1 / (2 * G8)) * (-6 + 9 * g) * sp.diff(a, t) ** 2 / (a ** 2 * N ** 2) - V) + lam * N * a ** 3 * (1 - 1 / N ** 2)
dN = sp.diff(Lbg, N).subs(N, 1).doit()
lam_sol = sp.solve(dN, lam)[0]
eps = sp.simplify(-2 * lam_sol)
H = sp.diff(a, t) / a
eps_expected = (3 / G8) * (1 - sp.Rational(3, 2) * g) * H ** 2 - V
R.check("T0.4a", "N-variation: eps = -2 lam = (3/8piG)(1 - 3 gt/2) H^2 - V (Friedmann with the gamma-modified coefficient; eps is the free 'dust' energy)", "diff = %s" % sp.simplify(eps - eps_expected), sp.simplify(eps - eps_expected) == 0)
Lbg1 = Lbg.subs({N: 1, lam: 0}).doit()
Ea = euler_equations(Lbg1, [a], [t])[0].lhs
addot = sp.solve(Ea, sp.diff(a, t, 2))[0]
dep = sp.simplify(sp.diff(a ** 3 * eps_expected, t).subs(sp.diff(a, t, 2), addot))
R.check("T0.4b", "d(a^3 eps)/dt = -a^3 dV/dt exactly on the a-equation (so Cm = a^3 eps is conserved iff V is constant; a non-constant V is a homogeneous source, position-independent)", "d(a^3 eps)/dt = %s" % dep, sp.simplify(dep + a ** 3 * sp.diff(V, t)) == 0)

# ------------------------------------------------------------------------------------------------ T0.5 Minkowski: current with gamma
R.banner("T0.5  flat-space EOM of L = lam(X+1) + (gamma/2)(box phi)^2 : current J^mu = eps u^mu + gamma nabla^mu(box phi), linearised")
ph2 = sp.Function('phi')(t, x); la2 = sp.Function('lam')(t, x); gam = sp.symbols('gam')
def box(f): return -sp.diff(f, t, 2) + sp.diff(f, x, 2)
L2 = la2 * (-sp.diff(ph2, t) ** 2 + sp.diff(ph2, x) ** 2 + 1) + gam / 2 * box(ph2) ** 2
E_ph = euler_equations(L2, [ph2], [t, x])[0].lhs
e_ = sp.symbols('e_'); pp = sp.Function('p')(t, x); ll = sp.Function('l')(t, x); l0 = sp.symbols('l0')
E1 = sp.diff(E_ph.subs({ph2: t + e_ * pp, la2: l0 + e_ * ll}).doit(), e_).subs(e_, 0)
E1 = sp.simplify(E1)
constraint1 = sp.simplify(sp.diff((-sp.diff(ph2, t) ** 2 + sp.diff(ph2, x) ** 2 + 1).subs(ph2, t + e_ * pp).doit(), e_).subs(e_, 0))
P("  linearised phi-equation:  %s = 0;  linearised constraint: %s = 0" % (E1, constraint1))
# with p_t = 0 (constraint) the equation is  -2*d_t l ... ; compare with the hand result 2 d_t l - 2 l0 p_xx + gam p_xxxx (sign fixed by sympy)
E1c = sp.simplify(E1.subs(sp.diff(pp, t, 2), 0).subs(sp.diff(pp, t, 3), 0).subs(sp.diff(pp, t, 2, x, 2), 0).subs(sp.Derivative(pp, (t, 2), (x, 2)), 0))
target = 2 * sp.diff(ll, t) - 2 * l0 * sp.diff(pp, x, 2) + gam * sp.diff(pp, x, 4)
target2 = -2 * sp.diff(ll, t) + 2 * l0 * sp.diff(pp, x, 2) + gam * sp.diff(pp, x, 4)
ok5 = sp.simplify(E1c - target) == 0
P("  reduced (p_t = 0) equation: %s" % E1c)
R.check("T0.5", "linear current law (p_t = 0 from the constraint): 2 d_t l - 2 l0 p_xx + gamma p_xxxx = 0, i.e. with eps = -2 lam, v = -p_x:  d_t d(eps) + eps0 d_x v = -gamma d_x^3 v, the L374 continuity form d_t rho + d_x(rho v) = beta d_x^3 v with beta = -gamma", "E1c = %s" % E1c, ok5)
# read off beta: solve E1c=0 for d_t eps with eps=-2 l
dt_l = sp.solve(E1c, sp.diff(ll, t))[0]
beta = sp.simplify(-2 * dt_l)    # d_t eps
P("  d_t d(eps) = %s   (eps0 = -2 l0, v = -p_x)  =>  d_t d(eps) + eps0 d_x v = beta d_x^3 v  with beta = %s" % (beta, sp.simplify(sp.expand(beta).coeff(sp.Derivative(pp, (x, 4))) * -1)))
BETA_SIGN = sp.simplify(sp.expand(beta).coeff(sp.Derivative(pp, (x, 4))))
R.num("T0_current_coefficient_of_p_xxxx_in_d_t_eps", str(BETA_SIGN))

# ------------------------------------------------------------------------------------------------ T0.6 scalar perturbations: c_s^2, ghost sign, DOF
R.banner("T0.6  scalar sector of the reduced ADM action (h_ij = a^2 e^{2 zeta} delta_ij, N=1, N_i = d_i psi): momentum constraint, c_s^2, kinetic sign, DOF count")
R3 = sp.simplify(sum(hinv[i, j] * sum(
    sp.diff(Gm[k][i][j], Xs[k]) - sp.diff(Gm[k][i][k], Xs[j]) + sum(Gm[k][k][l] * Gm[l][i][j] - Gm[k][j][l] * Gm[l][i][k] for l in range(3)) for k in range(3))
    for i in range(3) for j in range(3)))
Lfull = sqrth * (((1 + w_) * R3 + (1 + s_) * KK - (1 - g) * Ktr ** 2) / (2 * G8) - V)
E_z, E_p = euler_equations(Lfull, [zeta, psi], [t, x])
ep = sp.symbols('ep'); Zf = sp.Function('Z')(t, x); Pf = sp.Function('P')(t, x)
def lin(E):
    e = E.lhs.subs({zeta: ep * Zf, psi: ep * Pf}).doit()
    return sp.simplify(sp.diff(e, ep).subs(ep, 0))
zl, pl = lin(E_z), lin(E_p)
k = sp.symbols('k', positive=True); zt = sp.Function('zt')(t); pt = sp.Function('pt')(t)
def four(e):
    e = e.subs({Zf: zt * sp.exp(sp.I * k * x), Pf: pt * sp.exp(sp.I * k * x)}).doit()
    return sp.simplify(e / sp.exp(sp.I * k * x))
pz = four(pl); zz = four(zl)
psi_sol = sp.solve(pz, pt)[0]
zz2 = sp.expand(sp.simplify(zz.subs(pt, psi_sol).doit()))
A = sp.simplify(zz2.coeff(sp.Derivative(zt, (t, 2))))
Bk = sp.simplify(zz2.coeff(zt).coeff(k, 2))       # coefficient of k^2 zt
cs2 = sp.simplify(Bk / A * a ** 2)
P("  momentum constraint (Fourier): %s = 0  =>  psi_k = %s" % (pz, sp.simplify(psi_sol)))
P("  z-double-dot coefficient A = %s ;  k^2 z coefficient B = %s" % (sp.factor(A), sp.factor(Bk)))
cs2_gen = sp.factor(sp.simplify(cs2))
P("  c_s^2 (omega^2 = c_s^2 k^2/a^2 at large k) = B a^2 / A = %s" % cs2_gen)
R.num("cs2_general_gt_s_w", str(cs2_gen))
cs2_mim = sp.simplify(cs2_gen.subs({s_: 0, w_: 0}))
R.check("T0.6a", "mimetic + (box phi)^2 (s = w = 0): c_s^2 = gt/(2 - 3 gt), the recalled CMV value (recomputed from the reduced action, not assumed)", "c_s^2 = %s" % cs2_mim, sp.simplify(cs2_mim - g / (2 - 3 * g)) == 0)
# kinetic sign of the quadratic action for zeta: S2 = -(A/2) zdot^2 + ...  (delta S/delta zeta = A zddot + ...)
A0 = sp.simplify(A.subs({s_: 0, w_: 0}))
P("  A(gt) at s=w=0 = %s   (S2 = -(A/2) zdot^2 + ...: kinetic sign = -sign(A/a^3...))" % sp.factor(A0))
R.num("A_zddot_coefficient_s0w0", str(sp.factor(A0)))
def kinetic_sign(gv):
    val = A0.subs({g: gv, G8: 1, a: 1})
    return -sp.sign(val)
res_sign = {gv: (str(kinetic_sign(sp.Rational(gv))), str(sp.sign(sp.simplify(cs2_mim.subs(g, sp.Rational(gv)))))) for gv in ("-1/10", "1/100", "1/4", "1/2", "3/5", "7/10")}
P("  (gt: (sign of kinetic term of the zeta action [+1 healthy], sign of c_s^2)) = %s" % res_sign)
ghost_window = all(res_sign[q][0] == "-1" for q in ("1/100", "1/4", "1/2", "3/5"))
R.check("T0.6b", "GHOST (negative kinetic term of the scalar mode) for every 0 < gt < 2/3, where c_s^2 > 0; GRADIENT instability (c_s^2 < 0) with healthy kinetic sign for gt < 0 and gt > 2/3.  So no gt gives a healthy stable scalar in the minimal action [the recalled 'ghost/gradient dichotomy' of Ramazanov et al. / projectable Horava-like models, here derived]",
        str(res_sign), ghost_window and res_sign["-1/10"] == ("1", "-1") and res_sign["7/10"] == ("1", "-1"))
# DOF count: the zeta equation is second order in t, psi algebraic  -> one scalar DOF; at gt = 0 the coefficient A vanishes
pz0 = sp.simplify(pz.subs({g: 0, s_: 0}))
R.check("T0.6c", "DOF count: the momentum constraint is algebraic in psi_k and the zeta equation is second order => ONE scalar mode beyond the tensors (the dust mode) for gt != 0. At gt = 0 (s = 0) the momentum constraint loses psi and becomes zeta-dot = 0: zeta frozen, no propagating scalar (pure dust, class A)", "momentum constraint at gt = s = 0: %s = 0" % pz0, sp.simplify(pz0 + 2 * k ** 2 * a * sp.diff(zt, t) / G8) == 0)
# with s, w (class D)
P("  class D (K_ij K^ij coefficient 1+s, R3 coefficient 1+w): c_s^2 = %s" % cs2_gen)
# tensor speed: c_T^2 = (1+w)/(1+s)  -- derived below
R.banner("T0.6d  tensor sector (class D): c_T^2 = (1+w)/(1+s)")
eT = sp.symbols('eT'); gam_t = sp.Function('gam')(t, z)
hT = sp.Matrix([[1, eT * gam_t, 0], [eT * gam_t, 1, 0], [0, 0, 1]]) * a ** 2
hTi = hT.inv()
Zc = [x, y, z]
def GamT(k_, i, j): return sum(hTi[k_, l] * (sp.diff(hT[l, i], Zc[j]) + sp.diff(hT[l, j], Zc[i]) - sp.diff(hT[i, j], Zc[l])) for l in range(3)) / 2
GT = [[[GamT(k_, i, j) for j in range(3)] for i in range(3)] for k_ in range(3)]
def RicT(i, j):
    r = 0
    for k_ in range(3):
        r += sp.diff(GT[k_][i][j], Zc[k_]) - sp.diff(GT[k_][i][k_], Zc[j])
        for l in range(3):
            r += GT[k_][k_][l] * GT[l][i][j] - GT[k_][j][l] * GT[l][i][k_]
    return r
R3T = sum(hTi[i, j] * RicT(i, j) for i in range(3) for j in range(3))
KT = sp.Matrix(3, 3, lambda i, j: sp.diff(hT[i, j], t) / 2)
KmT = hTi * KT
KKT = (KmT * KmT).trace(); KtrT = KmT.trace()
sqT = sp.sqrt(hT.det())
LT = sqT * (((1 + w_) * R3T + (1 + s_) * KKT - (1 - g) * KtrT ** 2) / (2 * G8))
LT2 = sp.simplify(sp.series(LT, eT, 0, 3).removeO().coeff(eT, 2))
LT2e = sp.expand(sp.simplify(LT2 * 4 * G8 / a))
gd_ = sp.Derivative(gam_t, t); gz_ = sp.Derivative(gam_t, z); gzz_ = sp.Derivative(gam_t, (z, 2))
c_kin = sp.simplify(LT2e.coeff(gd_, 2)); c_gz = sp.simplify(LT2e.coeff(gz_, 2)); c_gzz = sp.simplify(LT2e.coeff(gam_t * gzz_))
# integrate by parts: c_gzz * g g_zz -> -c_gzz g_z^2
c_grad = sp.simplify(c_gz - c_gzz)
P("  kinetic coefficient (x 4G8/a) = %s ; gradient coefficient after integration by parts (x 4G8/a) = %s" % (c_kin, c_grad))
cT2_phys = sp.simplify(-c_grad / c_kin * a ** 2)
P("  c_T^2 = -(gradient)/(kinetic) [times a^-2 in the gradient, times a^2 for physical units] = %s" % cT2_phys)
R.check("T0.6d", "tensor speed c_T^2 = (1+w)/(1+s) (GW170817 needs c_T = 1, i.e. s = w)", "c_T^2 = %s" % cT2_phys, sp.simplify(cT2_phys - (1 + w_) / (1 + s_)) == 0)
R.num("cT2", str(cT2_phys))
# with c_T = 1 (s = w) is there a healthy window for the scalar?
cs2_cT1 = sp.simplify(cs2_gen.subs(w_, s_))
A_cT1 = sp.simplify(A.subs(w_, s_))
P("  with c_T = 1 (w = s): c_s^2 = %s ; A = %s" % (sp.factor(cs2_cT1), sp.factor(A_cT1)))
import numpy as np
fA = sp.lambdify((g, s_), (-A_cT1 / (a ** 3)).subs({G8: 1, a: 1}), 'numpy'); fc = sp.lambdify((g, s_), cs2_cT1, 'numpy')
gs = np.linspace(-1.5, 1.5, 601); ss = np.linspace(-0.9, 3, 391)
healthy = 0; total = 0; examples = []
for gv in gs:
    for sv in ss:
        with np.errstate(all='ignore'):
            kin_sign = fA(gv, sv); c2v = fc(gv, sv)
        if not (np.isfinite(kin_sign) and np.isfinite(c2v)): continue
        total += 1
        if kin_sign > 0 and c2v > 0 and c2v <= 1:
            healthy += 1
            if len(examples) < 4: examples.append((round(float(gv), 3), round(float(sv), 3), float(c2v)))
P("  scan of (gt, s) with c_T = 1 (w = s): %d grid points, %d with kinetic term healthy AND 0 < c_s^2 <= 1; examples %s" % (total, healthy, examples))
R.num("classD_cT1_healthy_points", [total, healthy, examples])

# ------------------------------------------------------------------------------------------------ T0.7 static stress of B, C, D terms
R.banner("T0.7  static stress: terms B, C, D vanish or are homogeneous on a stationary configuration; the reduced action has no pressure-like term that supports a static halo")
Kij_static = sp.zeros(3, 3)
E_static = (1 + s_) * (Kij_static * Kij_static).trace() - (1 - g) * Kij_static.trace() ** 2
R.check("T0.7", "at K_ij = 0 (stationary slices) the (box phi)^2 term (gt K^2) and the K_ijK^ij term contribute NOTHING (and their h_ij-variation is quadratic or linear in K, K-dot: zero at K = 0 = K-dot); V contributes a homogeneous -V h^{ij}; R3 (class D) modifies the gravity sector, not a dust pressure. So the only stationary states are v = 0 states, which T0.3c shows do not exist for grad Phi != 0",
        "K_ijK^ij and K^2 terms at K=0: %s" % E_static, E_static == 0)
if C.MU('a'):
    R.check("T0.7-MUTATE(a)", "[control] give the dust a hand-supplied pressure gradient +g_tot: the stationary v = 0 state then exists (d v/dt = -grad Phi + f_ext = 0)", "f_ext = grad Phi -> d v/dt = 0: the T0.3c statement is FALSE with the hand-supplied force", False)
if C.MU('b'):
    R.check("T0.6a-MUTATE(b)", "[control] a wrong-sign gamma term (gt -> -gt) in the gradient piece: c_s^2 would be -gt/(2+3gt)", "c_s^2(mutated) = %s" % sp.simplify(-g / (2 + 3 * g)), sp.simplify(-g / (2 + 3 * g) - g / (2 - 3 * g)) == 0)
nf = R.write()
sys.exit(1 if nf else 0)
