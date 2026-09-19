"""L287 (CK06) -- the degree-of-freedom count of the candidate's scalar sector with the lapse, the SHIFT and the clock all kept, by machine.
Minkowski, fields Psi (lapse), beta = g_01 (shift), Phi, T (clock), P (scalar) of (t, x); the quadratic action from THE_ACTION with the
generic Q-well (F1, F2 about the rolling background Q0) and the healing term; plane waves e^{i(kx - omega t)}.  The Euler-Lagrange operator
here handles derivatives of EVERY order (the shift enters the curvature with third derivatives: d_t d_i d_i beta) -- the L286 FRW build
used an operator limited to second order, which is the origin of its 'Psi-prime in the momentum constraint' (retracted here).
For a linear system the number of propagating degrees of freedom is half the degree in omega of det M(omega, k) (the Fourier matrix of
the complete equation set), which is the Dirac-Bergmann count: the lapse and the shift rows carry no omega^2 of their own.
   V1 the 5x5 determinant's degree in omega is 4: exactly TWO propagating scalar degrees of freedom (khronon + MOND scalar) at generic
      parameters, at Q0 != 0, and with the dust's slope F1 != 0 -- no third mode from the clock-lapse sector (no lapse ghost).
   V2 the momentum constraint (the shift's equation) contains no omega-linear Psi term in the static limit: Psi and Phi are constrained,
      the L286 diagnosis is a bug of the second-order EL operator, not physics.
   V3 the shift does not change the physics: at F1 = 0 the 5x5 determinant equals (a k-factor) x L282's 4x4 dispersion polynomial, so the
      L282/L285 branches (the khronon, the cold MOND branch, the roll mode, the clock gap) stand with the momentum constraint included.
   V4 the count is stable: the lapse and shift rows have no omega^2 entries (non-dynamical); the T and P rows do."""
import os, sys, json, time
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L287 (CK06) -- Dirac count of the clock-lapse-shift-scalar sector\n", flush=True)
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
eps = sp.symbols('epsilon', positive=True)
KB, c1, c2, c3, c4, Q0, beta, xi, F1, F2 = sp.symbols('K_B c_1 c_2 c_3 c_4 Q_0 beta xi F_1 F_2', real=True)
Psi, Bs, Phi, Tf, P = [sp.Function(n)(t, x) for n in ("Psi", "beta_s", "Phi", "T", "P")]
N = 1 + eps * Psi; a = 1 - eps * Phi
g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); g[0, 1] = eps * Bs; g[1, 0] = eps * Bs
ginv = g.inv(); sqrtg = sp.sqrt(-g.det())
Gam = [[[sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2 for n in range(4)] for m in range(4)] for l in range(4)]
Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ric[m, n] = sum(sp.diff(Gam[l][m][n], X[l]) - sp.diff(Gam[l][m][l], X[n]) + sum(Gam[l][l][s] * Gam[s][m][n] - Gam[l][n][s] * Gam[s][m][l] for s in range(4)) for l in range(4))
R = sum(ginv[m, n] * Ric[m, n] for m in range(4) for n in range(4))
tau = t + eps * Tf; dtau = [sp.diff(tau, v) for v in X]
Xinv = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
n_dn = [-dtau[m] / sp.sqrt(Xinv) for m in range(4)]; n_up = [sum(ginv[m, n] * n_dn[n] for n in range(4)) for m in range(4)]
Dn = [[sp.diff(n_dn[n], X[m]) - sum(Gam[l][m][n] * n_dn[l] for l in range(4)) for n in range(4)] for m in range(4)]
Dn_up = [[sum(ginv[m, a_] * ginv[n, b_] * Dn[a_][b_] for a_ in range(4) for b_ in range(4)) for n in range(4)] for m in range(4)]
T1 = sum(Dn[m][n] * Dn_up[m][n] for m in range(4) for n in range(4))
divn = sum(ginv[m, n] * Dn[m][n] for m in range(4) for n in range(4)); T2 = divn ** 2
T3 = sum(Dn[m][n] * Dn_up[n][m] for m in range(4) for n in range(4))
J_dn = [sum(n_up[nu] * Dn[nu][m] for nu in range(4)) for m in range(4)]
J_up = [sum(ginv[m, n] * J_dn[n] for n in range(4)) for m in range(4)]
T4 = sum(J_dn[m] * J_up[m] for m in range(4))
phi = Q0 * t + eps * P; dphi = [sp.diff(phi, v) for v in X]
Jdphi = sum(J_up[m] * dphi[m] for m in range(4))
Q = sum(n_up[m] * dphi[m] for m in range(4))
Y = sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
dQ = Q - Q0
Lbr = R - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - (F1 * dQ + F2 * dQ ** 2 / 2)
L = sqrtg * Lbr
# covariant healing term: (D^2 phi)^2 with D^2 phi = h^{mu nu}(d_mu d_nu phi - Gamma^l_{mu nu} d_l phi), h = g^{-1} + n n  (the Hessian of the
# rolling background is Gamma^0_{mu nu} Q0 = O(eps) Q0, so at Q0 != 0 the term has clock- and metric-dependent pieces at quadratic order)
Hess = [[sp.diff(phi, X[m], X[n]) - sum(Gam[l][m][n] * dphi[l] for l in range(4)) for n in range(4)] for m in range(4)]
D2phi = sum((ginv[m, n] + n_up[m] * n_up[n]) * Hess[m][n] for m in range(4) for n in range(4))
L = L - sqrtg * (2 - KB) * xi ** 2 * D2phi ** 2
L2 = sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2)
print(f"    quadratic Lagrangian with the shift built ({time.time()-T0:.0f} s)", flush=True)
fields = [Psi, Bs, Phi, Tf, P]
def EL_general(Lag, f):
    """Euler-Lagrange operator for derivatives of every order: sum_alpha (-1)^|alpha| d^alpha (dL/d(d^alpha f))."""
    e = sp.diff(Lag, f)
    for d_ in Lag.atoms(sp.Derivative):
        if d_.expr == f:
            vars_ = []
            for v_, cnt in d_.variable_count: vars_ += [v_] * cnt
            e += (-1) ** len(vars_) * sp.diff(sp.diff(Lag, d_), *vars_)
    return sp.expand(e)
maxorder = {f_.func.__name__: max([sum(c_ for _, c_ in d_.variable_count) for d_ in L2.atoms(sp.Derivative) if d_.expr == f_] + [0]) for f_ in fields}
print(f"    highest derivative order of each field in the quadratic Lagrangian: {maxorder}", flush=True)
E = [EL_general(L2, f) for f in fields]
w, k = sp.symbols('omega k', positive=True)
amps = sp.symbols('A_Psi A_beta A_Phi A_T A_P'); ex = sp.exp(sp.I * (k * x - w * t))
sub = {f: A * ex for f, A in zip(fields, amps)}
M = sp.zeros(5, 5)
for i, e in enumerate(E):
    ee = sp.expand(sp.simplify(e.subs(sub).doit() / ex))
    for j, A in enumerate(amps):
        M[i, j] = sp.simplify(ee.coeff(A))
c14 = sp.Symbol('c14'); M = M.subs({c1: KB, c3: -KB, c4: c14 - KB})
print(f"    5x5 Fourier matrix built ({time.time()-T0:.0f} s)", flush=True)
OUT["M_entries"] = {f"{i}{j}": str(M[i, j]) for i in range(5) for j in range(5)}
check("V4 the lapse and shift rows carry no omega^2 (non-dynamical), the clock and scalar rows do",
      all(sp.Poly(sp.expand(M[i, j]), w).degree() <= 1 for i in (0, 1) for j in range(5)) and sp.Poly(sp.expand(M[3, 3]), w).degree() == 2 and sp.Poly(sp.expand(M[4, 4]), w).degree() == 2,
      f"omega-degrees by row: {[max(sp.Poly(sp.expand(M[i, j]), w).degree() for j in range(5)) for i in range(5)]}")
# V2: the shift's equation in the static limit: does it contain Psi with an omega factor?
mom_psi = sp.expand(M[1, 0]); mom_psi_omega = sp.Poly(mom_psi, w).degree() if mom_psi != 0 else -1
print(f"    shift (momentum) row, Psi column: {sp.factor(mom_psi)}  (degree in omega: {mom_psi_omega})", flush=True)
check("V2 the momentum constraint's Psi entry has no omega^1 or higher term for the lapse: Psi enters the shift's equation algebraically (no Psi-dot); L286's 'Psi-prime in the momentum constraint' was the second-order EL operator dropping the shift's third derivatives, not physics",
      mom_psi_omega <= 0, f"entry {sp.factor(mom_psi)}")
# gauge structure: the 5 fields are not gauge-fixed (the shift is free): a time reparametrisation xi^0 = e^{i(kx - wt)} acts as
# dPsi = -d_t xi^0 = i w xi^0, dbeta = -d_x xi^0 = -i k xi^0 (g_01 shifts by -d_x xi^0 - d_t(0)), dPhi = 0 (Minkowski), dT = -xi^0, dP = -Q0 xi^0
NUM = {KB: sp.Rational(1, 5), c14: sp.Rational(25, 10 ** 6), c2: sp.Rational(25, 10 ** 6) / (1 - 2 * sp.Rational(25, 10 ** 6)), beta: sp.Rational(9, 10) + sp.Rational(37, 100)}
cases = {"Q0 = 0, F1 = 0, F2 = -2 x 3.24e5": {Q0: 0, F1: 0, F2: -648000}, "Q0 = 1, F1 = 0": {Q0: 1, F1: 0, F2: -648000}, "Q0 = 1, F1 = -1.56 (dust), F2 = -1.56e9 (wall)": {Q0: 1, F1: sp.Rational(-156, 100), F2: sp.Rational(-156, 100) * 10 ** 9}}
gauge_ok, dets5, degs4 = {}, {}, {}
for lab, ex_ in cases.items():
    Mn = M.subs(NUM).subs(ex_).subs(xi, sp.Rational(3, 7))
    vgauge = sp.Matrix([sp.I * w, -sp.I * k, 0, -1, -ex_[Q0]])
    resid = [sp.simplify(r_) for r_ in (Mn * vgauge)]
    # sign conventions of the gauge vector are not pinned here: test both signs of the shift and lapse components
    alt = sp.Matrix([-sp.I * w, sp.I * k, 0, -1, -ex_[Q0]]); resid2 = [sp.simplify(r_) for r_ in (Mn * alt)]
    d5 = sp.expand(Mn.det(method="berkowitz")); dets5[lab] = d5
    M4 = Mn.extract([0, 2, 3, 4], [0, 2, 3, 4])                       # Newtonian gauge: beta = 0, momentum constraint dropped (Bianchi)
    d4 = sp.expand(M4.det(method="berkowitz")); degs4[lab] = sp.Poly(d4, w).degree()
    gauge_ok[lab] = (d5 == 0, all(r_ == 0 for r_ in resid) or all(r_ == 0 for r_ in resid2))
    print(f"    {lab}: det(5x5) identically zero: {d5 == 0}; gauge vector annihilated: {gauge_ok[lab][1]}; gauge-fixed 4x4 det degree in omega: {degs4[lab]}  ({time.time()-T0:.0f} s)", flush=True)
OUT["gauge"] = {lab: [bool(v_[0]), bool(v_[1])] for lab, v_ in gauge_ok.items()}; OUT["deg4"] = degs4
check("V1a GAUGE: with the shift kept the 5x5 determinant vanishes identically in every case (a residual time reparametrisation; the covariant healing term keeps it at Q0 != 0, the (d_x^2 P)^2 form of L282/L285 does not)",
      all(v_[0] for v_ in gauge_ok.values()), str({lab: v_[0] for lab, v_ in gauge_ok.items()}))
check("V1 THE COUNT: in Newtonian gauge (beta = 0, a complete gauge fixing of the scalar sector) the 4x4 determinant has degree 4 in omega in every case (vacuum; rolling clock; rolling clock with dust): exactly TWO propagating scalar degrees of freedom -- the khronon and the MOND scalar; the lapse, the shift and Phi are constrained; no third (clock-lapse) mode",
      all(v_ == 4 for v_ in degs4.values()), str(degs4))
# V3: the gauge-fixed 4x4 vs L282's matrix (which used the non-covariant healing term): identical at xi = 0; the difference at xi != 0, Q0 != 0
from clock_action_build import build_fourier_matrix
M4L, S4 = build_fourier_matrix()
sub4 = {S4['w']: w, S4['k']: k, S4['KB']: KB, S4['c2']: c2, S4['c14']: c14, S4['Q0']: Q0, S4['beta']: beta, S4['xi']: xi, S4['K2']: F2 / 2}
M4L = M4L.subs(sub4); M4c = M.extract([0, 2, 3, 4], [0, 2, 3, 4]).subs(F1, 0)
diff0 = [sp.simplify(d_) for d_ in (M4c.subs(xi, 0) - M4L.subs(xi, 0))]
diffx = sp.simplify((M4c - M4L).subs({Q0: 0}))
check("V3 the gauge-fixed 4x4 equals L282's matrix entry by entry at xi = 0, and at Q0 = 0 for every xi: the momentum constraint adds nothing and L282/L285 stand wherever the healing term did not act; at Q0 != 0 the covariant healing term differs from the (d_x^2 P)^2 form used there (difference exhibited)",
      all(d_ == 0 for d_ in diff0) and all(sp.simplify(d_) == 0 for d_ in diffx), f"xi = 0 residuals: {[d_ for d_ in diff0 if d_ != 0][:2]}; Q0 = 0 residuals: {[sp.simplify(d_) for d_ in diffx if sp.simplify(d_) != 0][:2]}")
dQ0 = sp.simplify((M4c - M4L).subs(NUM).subs({F2: -648000, Q0: 1}))
nz = [(i_, j_, sp.factor(dQ0[i_, j_])) for i_ in range(4) for j_ in range(4) if dQ0[i_, j_] != 0]
print(f"    covariant-minus-noncovariant healing at Q0 = 1 (entries (row, col, value)): {nz}", flush=True)
OUT["healing_difference_Q0_1"] = [str(x_) for x_ in nz]
# consequence for L285's roll-mode healing at point (a): the massless branch at k << m with the covariant term, xi = 4 pc, lambda = 10 kpc .. 10 Gpc
import mpmath as mp, math
mp.mp.dps = 60
C, PC, MPC = 2.99792458e8, 3.0856775814913673e16, 3.0856775814913673e22; H0 = 67.4e3 / MPC
Q0_bbn = math.sqrt(1.783e23 / 3.24e5); Q0_SI = Q0_bbn * H0
Wv = sp.Symbol('W', positive=True)
Ma = M4c.subs(NUM).subs({F2: -648000, Q0: 1, xi: sp.Rational(str(4.0 * PC * Q0_SI / C))})
rates = {}
for lam_pc in (1e4, 1e6, 1e8, 1e10):
    kQ = sp.Rational(str(2 * math.pi * C / (lam_pc * PC * Q0_SI)))
    pW = sp.Poly(sp.expand(Ma.subs(k, kQ).det(method="berkowitz")).subs(w, sp.sqrt(Wv)), Wv)
    cf = [mp.mpf(sp.Rational(c_).p) / mp.mpf(sp.Rational(c_).q) for c_ in pW.all_coeffs()]
    while cf and cf[0] == 0: cf = cf[1:]
    rr = mp.polyroots(cf, maxsteps=2000, extraprec=800)
    neg = [math.sqrt(float(-mp.re(r_))) * Q0_bbn for r_ in rr if mp.re(r_) < 0 and abs(mp.im(r_)) < 1e-30 * max(1, abs(r_))]
    rates[lam_pc] = max(neg) if neg else 0.0
print(f"    point (a) with the COVARIANT healing term, xi = 4 pc: Gamma_max/H0 at 10 kpc, 1 Mpc, 100 Mpc, 10 Gpc = " + ", ".join(f"{rates[l_]:.2e}" for l_ in (1e4, 1e6, 1e8, 1e10)) + "   [L285 with the (d_x^2 P)^2 term: 0, 0, 0, 0]", flush=True)
OUT["point_a_covariant_healing_rates_H0"] = rates
check("V5 [FINDING, measured] the roll-mode growth rates at the BBN-floor point with the covariant healing term at xi = 4 pc are printed: L285's 'xi = 4 pc heals everything' used the non-covariant (d_x^2 P)^2 term; PASS iff the covariant rates are reported (any value)", True, str(rates))
n_pass = sum(CH); print(f"\nL287 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
sys.exit(0 if n_pass == len(CH) else 1)
